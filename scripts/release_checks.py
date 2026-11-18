"""The release gates of release.yml: changelog, pins, bill, tag, merge, PyPI and version kind.

    uv run python scripts/release_checks.py changelog --version 0.1.0 [--final] [--notes out.md]
        [--controls .github/governance.toml@HASH --checked-at SHA [--controls-result conforming]]
    uv run python scripts/release_checks.py pins
    uv run python scripts/release_checks.py sbom --sbom sbom.cdx.json
    uv run python scripts/release_checks.py tag --tag v0.1.0 --sha SHA
    uv run python scripts/release_checks.py merge --sha SHA --from origin/dev
    uv run python scripts/release_checks.py pypi --version 0.1.0 --dist dist
    uv run python scripts/release_checks.py version-kind [--package tradespace]

``changelog`` needs a ``## [version]`` heading; with ``--final`` (a release) it must have
one, otherwise an ``## [Unreleased]`` heading also serves (a dry run, a candidate on TestPyPI).
With ``--controls`` the notes end with the attestation line of the ``controls`` job
(``GOVERNANCE.md``): the declaration's path and hash, the commit checked and the result.
``pins`` fails on any action in ``.github/workflows`` that is not pinned to a 40-character commit.
``sbom`` fails unless the CycloneDX file names every package, at its locked version, that
``uv.lock`` names.

``tag`` prints the state of the tag for the commit: ``new`` (no such tag), ``ours`` (the tag is on
this commit: a re-run), ``site-only`` (the tag is on an earlier commit and the package files,
``src/``, ``pyproject.toml`` and ``uv.lock``, are unchanged since it: the merge redeploys the site
only) or ``taken`` (anything else: a new version is needed), which exits 1. ``merge`` fails unless
the commit has two parents and its second parent is on the ``--from`` branch. ``pypi`` fails unless
the files PyPI holds for the version are the files of ``--dist``, by name and SHA-256.

``version-kind`` is the versioning rule of ``GOVERNANCE.md`` ("Versions"). It reads the version
from ``pyproject.toml`` and the highest ``v*`` tag below it (the previous release) and names the
bump. A patch release must leave the public surface (``tests/data/api_surface.json``, or the
surface computed from the previous tag's ``src`` when that tag has no record), the governed files
(the ``governed_files`` paths of ``.github/governance.toml``) and the changelog entry's ``Added``
and ``Removed`` sections untouched; each difference is one line, and any fails. A minor or major
bump passes with the kind printed. No previous tag (the first release) and a version that is
already tagged (a redeploy, which ``tag`` decides) pass with a notice.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import io
import json
import os
import re
import subprocess
import sys
import tarfile
import tempfile
import time
import tomllib
import urllib.error
import urllib.request
from collections.abc import Callable
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
USES = re.compile(r"^\s*(?:-\s+)?uses:\s*(\S+)", re.M)
PINNED = re.compile(r"^[\w.-]+/[\w.-]+(?:/[\w./-]+)?@[0-9a-f]{40}$")
# The files whose change needs a new version; a merge that leaves them unchanged since the tag
# redeploys the site only.
PACKAGE_FILES = ("src", "pyproject.toml", "uv.lock")
PYPI_JSON = "https://pypi.org/pypi/tradespace/{version}/json"
# The versioning rule (GOVERNANCE.md, "Versions"): the record of the public surface, the script
# that writes and compares it, and the version grammar of scripts/check_release_version.py.
SNAPSHOT_PATH = "tests/data/api_surface.json"
SURFACE_SCRIPT = Path(__file__).resolve().parent / "api_surface.py"
VERSION = re.compile(r"^(\d+)\.(\d+)\.(\d+)(?:(a|b|rc)(\d+))?(?:\.dev(\d+))?$")
PRE_ORDER = {"a": 1, "b": 2, "rc": 3}


def changelog_section(text: str, version: str) -> str | None:
    """The body of the ``## [version]`` entry, or None.

    >>> text = "# C\\n## [Unreleased]\\n- a\\n## [0.1.0] - 2026\\n- b\\n- c\\n## [0.0.1]\\n"
    >>> changelog_section(text, "0.1.0")
    '- b\\n- c'
    """
    m = re.search(rf"^## \[{re.escape(version)}\][^\n]*\n(.*?)(?=^## \[|\Z)", text, re.M | re.S)
    return m.group(1).strip() if m else None


def attestation(declaration: str, sha: str, result: str = "conforming") -> str:
    """The controls line of a release's notes and run summary (GOVERNANCE.md).

    >>> attestation(".github/governance.toml@3f2a1b9c0d4e", "0123456789ab")
    'Controls: .github/governance.toml@3f2a1b9c0d4e checked at 0123456789ab: conforming'
    """
    return f"Controls: {declaration} checked at {sha}: {result}"


def changelog_problems(root: Path, version: str, final: bool) -> list[str]:
    text = (root / "CHANGELOG.md").read_text(encoding="utf-8")
    if changelog_section(text, version):
        return []
    if not final and changelog_section(text, "Unreleased"):
        return []
    return [f"CHANGELOG.md has no entry `## [{version}]` with content"]


def pin_problems(root: Path) -> list[str]:
    problems = []
    for wf in sorted((root / ".github" / "workflows").glob("*.yml")):
        for ref in USES.findall(wf.read_text(encoding="utf-8")):
            if not (ref.startswith("./") or PINNED.match(ref)):
                problems.append(f"{wf.name}: `{ref}` is not pinned to a commit")
    return problems


def sbom_problems(root: Path, sbom: Path) -> list[str]:
    doc = json.loads(sbom.read_text(encoding="utf-8"))
    if doc.get("bomFormat") != "CycloneDX":
        return ["the file is not a CycloneDX bill of materials"]
    listed = {(c["name"], c.get("version")) for c in doc.get("components", [])}
    root_component = doc.get("metadata", {}).get("component")
    if root_component:
        listed.add((root_component["name"], root_component.get("version")))
    lock = tomllib.loads((root / "uv.lock").read_text(encoding="utf-8"))["package"]
    return [
        f"{p['name']} {p.get('version')} is in uv.lock and not in the bill of materials"
        for p in lock
        if (p["name"], p.get("version")) not in listed
    ]


def _git(root: Path, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run(["git", *args], cwd=root, capture_output=True, text=True)


def _commit(root: Path, ref: str) -> str | None:
    r = _git(root, "rev-parse", "-q", "--verify", f"{ref}^{{commit}}")
    return r.stdout.strip() if r.returncode == 0 else None


def tag_state(root: Path, tag: str, sha: str) -> tuple[str, str]:
    """The tag's state for the commit ``sha``, and the reason when it is ``taken``."""
    head = _commit(root, sha)
    if head is None:
        return "taken", f"commit {sha} is not in the repository"
    tagged = _commit(root, f"refs/tags/{tag}")
    if tagged is None:
        return "new", ""
    if tagged == head:
        return "ours", ""
    if _git(root, "merge-base", "--is-ancestor", tagged, head).returncode != 0:
        return "taken", f"{tag} is on {tagged[:12]}, which is not an ancestor of {head[:12]}"
    changed = _git(root, "diff", "--name-only", tagged, head, "--", *PACKAGE_FILES).stdout.split()
    if not changed:
        return "site-only", ""
    shown = ", ".join(changed[:5]) + (" ..." if len(changed) > 5 else "")
    return "taken", (
        f"{tag} exists on {tagged[:12]} and the package files changed since it ({shown}); "
        "set a new version"
    )


def merge_problems(root: Path, sha: str, source: str) -> list[str]:
    r = _git(root, "rev-list", "--parents", "-n", "1", sha)
    if r.returncode != 0:
        return [f"commit {sha} is not in the repository"]
    parents = r.stdout.split()[1:]
    if len(parents) != 2:
        return [f"{sha[:12]} has {len(parents)} parent(s); a release is a merge commit with two"]
    if _commit(root, source) is None:
        return [f"{source} is not in the repository"]
    if _git(root, "merge-base", "--is-ancestor", parents[1], source).returncode != 0:
        return [f"the merged parent {parents[1][:12]} of {sha[:12]} is not on {source}"]
    return []


def fetch_pypi(version: str) -> dict | None:
    """PyPI's JSON record of the version, or None when PyPI has none (404)."""
    try:
        with urllib.request.urlopen(PYPI_JSON.format(version=version), timeout=60) as r:
            return json.load(r)
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return None
        raise


def pypi_problems(
    version: str,
    dist: Path,
    fetch: Callable[[str], dict | None] = fetch_pypi,
    attempts: int = 6,
    wait: float = 20.0,
) -> list[str]:
    """Compare PyPI's files for the version with ``dist/*`` by name and SHA-256.

    PyPI's JSON can trail an upload by a little, so an absent or unreadable record is read again
    (``attempts`` times, ``wait`` seconds apart); a mismatch is final.
    """
    local = {
        f.name: hashlib.sha256(f.read_bytes()).hexdigest()
        for f in sorted(dist.iterdir())
        if f.name.endswith((".whl", ".tar.gz"))
    }
    if not local:
        return [f"{dist} holds no wheel or sdist"]
    record, reason = None, ""
    for i in range(attempts):
        try:
            record = fetch(version)
            reason = f"PyPI has no version {version}"
        except (OSError, ValueError) as e:
            record, reason = None, f"PyPI could not be read ({e})"
        if record is not None:
            break
        if i + 1 < attempts:
            time.sleep(wait)
    if record is None:
        return [reason]
    remote = {u["filename"]: u["digests"]["sha256"] for u in record.get("urls", [])}
    problems = [
        f"{name}: PyPI holds sha256 {remote[name][:16]}..., built {digest[:16]}..."
        for name, digest in local.items()
        if name in remote and remote[name] != digest
    ]
    problems += [f"{name} is built and not on PyPI" for name in local if name not in remote]
    problems += [f"{name} is on PyPI and not built here" for name in remote if name not in local]
    return problems


def parse_version(text: str) -> tuple | None:
    """A sortable key for ``major.minor.patch`` with an optional a, b, rc or dev suffix, or None.

    A final release sorts after its pre-releases: ``parse_version("0.2.0rc1") <
    parse_version("0.2.0")``.

    >>> parse_version("v0.1.0")[:3], parse_version("0.2.0rc1") < parse_version("0.2.0")
    ((0, 1, 0), True)
    >>> parse_version("paper-1") is None
    True
    """
    m = VERSION.match(text.removeprefix("v"))
    if not m:
        return None
    major, minor, patch, pre, number, dev = m.groups()
    final = pre is None and dev is None
    return (
        int(major),
        int(minor),
        int(patch),
        1 if final else 0,
        PRE_ORDER.get(pre, 0),
        int(number or 0),
        (1, 0) if dev is None else (0, int(dev)),
    )


def previous_release(tags: list[str], version: str) -> str | None:
    """The highest ``v*`` tag whose version is strictly below ``version``, or None.

    >>> previous_release(["v0.1.0", "v0.1.1", "v0.2.0", "paper-1"], "0.2.0")
    'v0.1.1'
    >>> previous_release(["v0.1.0"], "0.1.0") is None
    True
    """
    current = parse_version(version)
    below = [t for t in tags if (k := parse_version(t)) is not None and k < current]
    return max(below, key=parse_version) if below else None


def bump_kind(previous: str, version: str) -> str:
    """``major``, ``minor`` or ``patch``: the first of the three numbers that moved.

    >>> bump_kind("v0.1.0", "0.1.1"), bump_kind("v0.1.3", "0.2.0rc1"), bump_kind("v0.9.0", "1.0.0")
    ('patch', 'minor', 'major')
    """
    before, after = parse_version(previous)[:3], parse_version(version)[:3]
    for kind, b, a in zip(("major", "minor", "patch"), before, after, strict=True):
        if a != b:
            return kind
    return "patch"


def governed_paths(root: Path) -> list[str]:
    """The ``governed_files`` paths of the declaration (none when the tree has no declaration)."""
    declaration = root / ".github" / "governance.toml"
    if not declaration.is_file():
        return []
    doc = tomllib.loads(declaration.read_text(encoding="utf-8"))
    return [g["path"] for g in doc.get("governed_files", [])]


def _api_surface():
    spec = importlib.util.spec_from_file_location("api_surface", SURFACE_SCRIPT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def surface_from_source(src: Path, package: str) -> dict:
    """The public surface of ``package`` imported from ``src`` (a copy of a tag's ``src/``), read
    by ``scripts/api_surface.py`` in a fresh interpreter with ``src`` first on its path."""
    env = dict(os.environ, PYTHONPATH=str(src))
    r = subprocess.run(
        [sys.executable, str(SURFACE_SCRIPT), "--package", package],
        capture_output=True,
        text=True,
        env=env,
        cwd=src.parent,
    )
    if r.returncode != 0:
        raise RuntimeError(r.stderr.strip().splitlines()[-1] if r.stderr.strip() else "no output")
    return json.loads(r.stdout)


def previous_surface(root: Path, previous: str, package: str) -> dict:
    """The record ``tests/data/api_surface.json`` at the tag, or the surface computed from the
    tag's ``src/`` when the tag carries no record (the releases before the rule)."""
    shown = _git(root, "show", f"{previous}:{SNAPSHOT_PATH}")
    if shown.returncode == 0:
        return json.loads(shown.stdout)
    archive = subprocess.run(
        ["git", "archive", "--format=tar", previous, "src"], cwd=root, capture_output=True
    )
    if archive.returncode != 0:
        raise RuntimeError(f"{previous} has neither {SNAPSHOT_PATH} nor src/")
    with tempfile.TemporaryDirectory() as tmp:
        with tarfile.open(fileobj=io.BytesIO(archive.stdout)) as tar:
            tar.extractall(tmp, filter="data")
        return surface_from_source(Path(tmp) / "src", package)


def version_kind_problems(root: Path, package: str = "tradespace") -> tuple[list[str], list[str]]:
    """The notices to print and the problems that fail the check."""
    version = tomllib.loads((root / "pyproject.toml").read_text(encoding="utf-8"))["project"][
        "version"
    ]
    if parse_version(version) is None:
        return [], [f"version {version!r} is not major.minor.patch"]
    tags = _git(root, "tag", "--list", "v*").stdout.split()
    if any(parse_version(t) == parse_version(version) for t in tags):
        return [f"version-kind: v{version} is already a tag; the tag check decides"], []
    previous = previous_release(tags, version)
    if previous is None:
        return [f"version-kind: {version} is the first release; no previous v* tag"], []
    kind = bump_kind(previous, version)
    if kind != "patch":
        reason = "the major moved" if kind == "major" else "the minor moved"
        return [f"version-kind: {version} after {previous} is a {kind} release ({reason})"], []
    notices = [f"version-kind: {version} after {previous} is a patch release"]
    problems = []
    snapshot = root / SNAPSHOT_PATH
    if not snapshot.is_file():
        problems.append(f"{SNAPSHOT_PATH} is missing; run scripts/api_surface.py --write")
    else:
        current = json.loads(snapshot.read_text(encoding="utf-8"))
        try:
            before = previous_surface(root, previous, package)
        except RuntimeError as e:
            problems.append(f"the surface at {previous} could not be read: {e}")
        else:
            problems += [
                f"the public surface changed since {previous} ({line}); a patch release keeps it"
                for line in _api_surface().differences(before, current)
            ]
    for path in governed_paths(root):
        changed = _git(root, "diff", "--name-only", previous, "HEAD", "--", path).stdout.split()
        problems += [
            f"{name} changed since {previous}; a patch release changes no governed file"
            for name in changed
        ]
    text = (root / "CHANGELOG.md").read_text(encoding="utf-8")
    section = changelog_section(text, version)
    if section is None:
        notices.append(f"version-kind: no `## [{version}]` entry yet; its sections are not read")
    else:
        for heading in re.findall(r"^### (Added|Removed)\b", section, re.M):
            problems.append(
                f"CHANGELOG.md `## [{version}]` has a `### {heading}` section; "
                "a patch release adds and removes nothing"
            )
    return notices, problems


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sub = parser.add_subparsers(dest="check", required=True)
    c = sub.add_parser("changelog")
    c.add_argument("--version", required=True)
    c.add_argument("--final", action="store_true")
    c.add_argument("--notes", type=Path, help="write the entry here, for the release notes")
    c.add_argument("--controls", help="the declaration as <path>@<hash>; adds the attestation line")
    c.add_argument("--checked-at", help="the commit the controls job checked (with --controls)")
    c.add_argument("--controls-result", default="conforming", help="the controls job's result")
    sub.add_parser("pins")
    s = sub.add_parser("sbom")
    s.add_argument("--sbom", type=Path, required=True)
    t = sub.add_parser("tag")
    t.add_argument("--tag", required=True, help="v<version>")
    t.add_argument("--sha", required=True, help="the commit being released")
    m = sub.add_parser("merge")
    m.add_argument("--sha", required=True, help="the commit pushed to main")
    m.add_argument("--from", dest="source", default="origin/dev", help="the branch merged in")
    p = sub.add_parser("pypi")
    p.add_argument("--version", required=True)
    p.add_argument("--dist", type=Path, required=True)
    p.add_argument("--attempts", type=int, default=6)
    p.add_argument("--wait", type=float, default=20.0)
    v = sub.add_parser("version-kind")
    v.add_argument("--package", default="tradespace", help="the package whose surface is read")
    parser.add_argument("--root", type=Path, default=ROOT)
    args = parser.parse_args(argv)
    if args.check == "version-kind":
        notices, problems = version_kind_problems(args.root, args.package)
        for line in notices:
            print(line)
    elif args.check == "tag":
        state, reason = tag_state(args.root, args.tag, args.sha)
        print(state)
        problems = [reason] if state == "taken" else []
    elif args.check == "merge":
        problems = merge_problems(args.root, args.sha, args.source)
    elif args.check == "pypi":
        problems = pypi_problems(args.version, args.dist, attempts=args.attempts, wait=args.wait)
    elif args.check == "changelog":
        problems = changelog_problems(args.root, args.version, args.final)
        if args.controls and not args.checked_at:
            parser.error("--controls needs --checked-at")
        if args.notes and not problems:
            text = (args.root / "CHANGELOG.md").read_text(encoding="utf-8")
            body = changelog_section(text, args.version) or changelog_section(text, "Unreleased")
            notes = (body or "") + "\n"
            if args.controls:
                notes += (
                    "\n" + attestation(args.controls, args.checked_at, args.controls_result) + "\n"
                )
            args.notes.write_text(notes, encoding="utf-8")
    elif args.check == "pins":
        problems = pin_problems(args.root)
    else:
        problems = sbom_problems(args.root, args.sbom)
    for p in problems:
        print(f"refused: {p}", file=sys.stderr)
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())

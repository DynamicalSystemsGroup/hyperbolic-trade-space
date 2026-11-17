"""The release gates of release.yml: changelog, pins, bill of materials, tag, merge and PyPI.

    uv run python scripts/release_checks.py changelog --version 0.1.0 [--final] [--notes out.md]
    uv run python scripts/release_checks.py pins
    uv run python scripts/release_checks.py sbom --sbom sbom.cdx.json
    uv run python scripts/release_checks.py tag --tag v0.1.0 --sha SHA
    uv run python scripts/release_checks.py merge --sha SHA --from origin/dev
    uv run python scripts/release_checks.py pypi --version 0.1.0 --dist dist

``changelog`` needs a ``## [version]`` heading; with ``--final`` (a release) it must have
one, otherwise an ``## [Unreleased]`` heading also serves (a dry run, a candidate on TestPyPI).
``pins`` fails on any action in ``.github/workflows`` that is not pinned to a 40-character commit.
``sbom`` fails unless the CycloneDX file names every package, at its locked version, that
``uv.lock`` names.

``tag`` prints the state of the tag for the commit: ``new`` (no such tag), ``ours`` (the tag is on
this commit: a re-run), ``site-only`` (the tag is on an earlier commit and the package files,
``src/``, ``pyproject.toml`` and ``uv.lock``, are unchanged since it: the merge redeploys the site
only) or ``taken`` (anything else: a new version is needed), which exits 1. ``merge`` fails unless
the commit has two parents and its second parent is on the ``--from`` branch. ``pypi`` fails unless
the files PyPI holds for the version are the files of ``--dist``, by name and SHA-256.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
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


def changelog_section(text: str, version: str) -> str | None:
    """The body of the ``## [version]`` entry, or None.

    >>> text = "# C\\n## [Unreleased]\\n- a\\n## [0.1.0] - 2026\\n- b\\n- c\\n## [0.0.1]\\n"
    >>> changelog_section(text, "0.1.0")
    '- b\\n- c'
    """
    m = re.search(rf"^## \[{re.escape(version)}\][^\n]*\n(.*?)(?=^## \[|\Z)", text, re.M | re.S)
    return m.group(1).strip() if m else None


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


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sub = parser.add_subparsers(dest="check", required=True)
    c = sub.add_parser("changelog")
    c.add_argument("--version", required=True)
    c.add_argument("--final", action="store_true")
    c.add_argument("--notes", type=Path, help="write the entry here, for the release notes")
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
    parser.add_argument("--root", type=Path, default=ROOT)
    args = parser.parse_args(argv)
    if args.check == "tag":
        state, reason = tag_state(args.root, args.tag, args.sha)
        print(state)
        problems = [reason] if state == "taken" else []
    elif args.check == "merge":
        problems = merge_problems(args.root, args.sha, args.source)
    elif args.check == "pypi":
        problems = pypi_problems(args.version, args.dist, attempts=args.attempts, wait=args.wait)
    elif args.check == "changelog":
        problems = changelog_problems(args.root, args.version, args.final)
        if args.notes and not problems:
            text = (args.root / "CHANGELOG.md").read_text(encoding="utf-8")
            body = changelog_section(text, args.version) or changelog_section(text, "Unreleased")
            args.notes.write_text((body or "") + "\n", encoding="utf-8")
    elif args.check == "pins":
        problems = pin_problems(args.root)
    else:
        problems = sbom_problems(args.root, args.sbom)
    for p in problems:
        print(f"refused: {p}", file=sys.stderr)
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())

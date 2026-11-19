"""The release gates of release.yml: changelog, pins, bill, tag, merge, PyPI and version kind.

    uv run python scripts/release_checks.py changelog --version 0.1.0 [--final] [--notes out.md]
        [--controls .github/governance.toml@HASH --checked-at SHA [--controls-result conforming]]
    uv run python scripts/release_checks.py pins
    uv run python scripts/release_checks.py sbom --sbom sbom.cdx.json
    uv run python scripts/release_checks.py tag --tag v0.1.0 --sha SHA
    uv run python scripts/release_checks.py merge --sha SHA --from origin/dev
    uv run python scripts/release_checks.py pypi --version 0.1.0 --dist dist
    uv run python scripts/release_checks.py version-kind [--package tradespace]
    uv run python scripts/release_checks.py bump 0.2.0 --changelog final [--date 2026-11-20]
    uv run python scripts/release_checks.py gates [--release] [--since origin/dev]
    uv run python scripts/release_checks.py branches [--remote origin]

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

``bump`` writes a new version in every place it is written (``VERSION_PLACES``: ``pyproject.toml``,
``tradespace.__version__``, ``CITATION.cff``, the interface contract's manifest and the two values
its document quotes), runs ``uv lock`` so the lock's own entry follows, and edits ``CHANGELOG.md``
as ``--changelog`` says: ``final`` (a release) turns ``## [Unreleased]`` into ``## [<version>] -
<date>`` with a fresh empty ``## [Unreleased]`` above it; ``stub`` (a dry run on a ``qc/`` branch)
inserts a one-line throwaway entry below the unreleased section; ``none`` leaves it alone. With
``--date`` the citation file's ``date-released`` is set too; without it the heading carries today.
It prints each file it changed, refuses a version that is not PEP 440 or not above the current one
(nothing is written on a refusal), and never commits.

``gates`` runs locally, in order, what the Tests workflow runs on a push to ``dev`` (the
attribution grep over the commits since ``--since``, ``uv lock --check``, ``ruff check``, ``ruff
format --check``, the test modules that hold the repository's rules), the vocabulary check, the
public-surface record, the settings check and ``branches`` (the last two skipped with a line when
``gh`` is not authenticated), and with ``--release`` the release admissibility checks on the head
(``version``, ``tag`` at ``HEAD``, ``changelog --final``, ``version-kind``, ``pins``, the paper's
mode file). One line per check with its exit code, a verdict, exit 1 on any failure. It is the step
a unit runs before it reports, the driver before a push, and a code owner before a pull request or
a dry run.
A release check that refuses a head is reported as it is: a content branch at a released version is
refused by ``tag``, which is the rule doing its job, and ``bump`` is the answer.

``branches`` lists the remote's branches that are none of the long-lived three (``main``, ``dev``,
``paper``), the head of an open pull request, a ``qc/*`` branch (one dry run; named as a notice),
a ``talk/*`` branch (the material of a talk or demo, never merged; named as a notice),
a ``dependabot/*`` branch or the branch the check runs on (``HEAD``'s remote-tracking branch, or a
remote branch whose tip is ``HEAD``: its pull request comes next, so it is named as a notice), and
exits 1 naming them (``GOVERNANCE.md``, "Branches").
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
from dataclasses import dataclass
from datetime import date
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


# ------------------------------------------------------------------ the bump

# Every place the version is written, as (path, pattern whose group `v` is the value); each pattern
# matches exactly once in its file. tests/test_release_checks.py holds the list complete against the
# tree (every version assignment a tracked file carries is here). uv.lock follows by `uv lock`.
VERSION_PLACES = (
    ("pyproject.toml", r'^version = "(?P<v>[^"]+)"$'),
    ("src/tradespace/__init__.py", r'^__version__ = "(?P<v>[^"]+)"$'),
    ("CITATION.cff", r"^version: (?P<v>\S+)$"),
    ("work-packages/interface-contract.toml", r'^version = "(?P<v>[^"]+)"$'),
    ("work-packages/interface-contract.md", r'^package\.version = "(?P<v>[^"]+)"$'),
    ("work-packages/interface-contract.md", r"Current value: `(?P<v>[^`]+)`"),
)
DATE_PLACE = ("CITATION.cff", r"^date-released: (?P<v>\S+)$")
CHANGELOG_MODES = ("final", "stub", "none")
STUB_LINE = "- A dry-run stub for a `qc/` branch; the commit that carries it is never merged."


def version_values(root: Path) -> dict[str, str | None]:
    """The value each place holds, keyed ``path#n`` (None when the pattern does not match once).

    >>> sorted(version_values(ROOT))[:2]
    ['CITATION.cff#2', 'pyproject.toml#0']
    """
    out = {}
    for n, (path, pattern) in enumerate(VERSION_PLACES):
        found = re.findall(pattern, (root / path).read_text(encoding="utf-8"), re.M)
        out[f"{path}#{n}"] = found[0] if len(found) == 1 else None
    return out


def _replace_once(text: str, pattern: str, value: str) -> tuple[str, int]:
    """``text`` with the pattern's ``v`` group set to ``value``, and how many times it matched."""

    def sub(m: re.Match) -> str:
        return m.string[m.start() : m.start("v")] + value + m.string[m.end("v") : m.end()]

    return re.subn(pattern, sub, text, flags=re.M)


def bumped_changelog(text: str, version: str, day: str, mode: str) -> tuple[str, str | None]:
    """``CHANGELOG.md`` after the bump, and the reason to refuse (or None).

    >>> text = "# C\\n\\n## [Unreleased]\\n\\n### Fixed\\n\\n- a\\n\\n"
    >>> text += "## [0.1.0] - 2026-11-17\\n\\n- b\\n"
    >>> print(bumped_changelog(text, "0.2.0", "2026-11-20", "final")[0])
    # C
    <BLANKLINE>
    ## [Unreleased]
    <BLANKLINE>
    ## [0.2.0] - 2026-11-20
    <BLANKLINE>
    ### Fixed
    <BLANKLINE>
    - a
    <BLANKLINE>
    ## [0.1.0] - 2026-11-17
    <BLANKLINE>
    - b
    <BLANKLINE>
    >>> changelog_section(bumped_changelog(text, "0.1.1", "2026-11-20", "stub")[0], "0.1.1")
    '- A dry-run stub for a `qc/` branch; the commit that carries it is never merged.'
    """
    if mode == "none":
        return text, None
    if changelog_section(text, version) is not None:
        return text, f"CHANGELOG.md already has an entry `## [{version}]`"
    m = re.search(r"^## \[Unreleased\][^\n]*\n(.*?)(?=^## \[|\Z)", text, re.M | re.S)
    if m is None:
        return text, "CHANGELOG.md has no `## [Unreleased]` heading"
    heading = f"## [{version}] - {day}\n"
    body = m.group(1)
    if mode == "final":
        if not body.strip():
            return text, "CHANGELOG.md `## [Unreleased]` is empty; nothing to release"
        return text[: m.start()] + "## [Unreleased]\n\n" + heading + text[m.start(1) :], None
    sep = "" if body.endswith("\n\n") else ("\n" if body.endswith("\n") else "\n\n")
    stub = sep + heading + "\n" + STUB_LINE + "\n\n"
    return text[: m.end()] + stub + text[m.end() :], None


def bump(
    root: Path, version: str, day: str | None, changelog: str, lock: bool = True
) -> tuple[list[str], list[str]]:
    """Write ``version`` everywhere; the files changed and the problems (nothing written on any)."""
    current = tomllib.loads((root / "pyproject.toml").read_text(encoding="utf-8"))["project"][
        "version"
    ]
    problems = []
    if parse_version(version) is None:
        problems.append(
            f"version {version!r} is not major.minor.patch with an optional a, b, rc or dev suffix"
        )
    elif parse_version(version) <= parse_version(current):
        problems.append(f"version {version} is not above the current {current}")
    if day is not None:
        try:
            date.fromisoformat(day)
        except ValueError:
            problems.append(f"--date {day!r} is not YYYY-MM-DD")
    if changelog not in CHANGELOG_MODES:
        problems.append(f"--changelog must be one of {', '.join(CHANGELOG_MODES)}")
    if problems:
        return [], problems
    edits: dict[str, str] = {}
    for path, pattern in VERSION_PLACES:
        text = edits.get(path) or (root / path).read_text(encoding="utf-8")
        found = re.findall(pattern, text, re.M)
        if len(found) != 1 or found[0] != current:
            problems.append(
                f"{path} does not hold the current version {current} once "
                f"(found {found}); the tree is inconsistent, fix it by hand first"
            )
            continue
        edits[path], _ = _replace_once(text, pattern, version)
    if day is not None:
        path, pattern = DATE_PLACE
        text = edits.get(path) or (root / path).read_text(encoding="utf-8")
        edits[path], n = _replace_once(text, pattern, day)
        if n != 1:
            problems.append(f"{path} has no single `date-released:` line")
    log = (root / "CHANGELOG.md").read_text(encoding="utf-8")
    new_log, problem = bumped_changelog(log, version, day or date.today().isoformat(), changelog)
    if problem:
        problems.append(problem)
    elif new_log != log:
        edits["CHANGELOG.md"] = new_log
    if problems:
        return [], problems
    for path, text in edits.items():
        (root / path).write_text(text, encoding="utf-8")
    changed = list(edits)
    if lock:
        before = (root / "uv.lock").read_bytes() if (root / "uv.lock").is_file() else b""
        r = subprocess.run(["uv", "lock"], cwd=root, capture_output=True, text=True)
        if r.returncode != 0:
            problems.append(f"uv lock failed: {r.stderr.strip().splitlines()[-1:]}")
        elif (root / "uv.lock").read_bytes() != before:
            changed.append("uv.lock")
    return changed, problems


# ------------------------------------------------------------------ the remote's branches

LONG_LIVED = ("main", "dev", "paper")
# A branch for one dry run (deleted after it; named as a notice), a talk or demo branch (never
# merged; it stays until a code owner deletes it; named as a notice) and the update bot's branches
# (each goes with its pull request).
TOLERATED_PREFIXES = ("qc/", "talk/", "dependabot/")


def stray_branches(
    heads: list[str], open_heads: set[str], this: set[str] = frozenset()
) -> tuple[list[str], list[str]]:
    """The remote branches that should not be there, and the ``qc/`` branches as notices;
    ``this`` is the branch the check runs on, whose pull request comes next.

    >>> heads = ["main", "dev", "paper", "qc/release", "dependabot/uv/x", "wp-a", "old-b", "mine"]
    >>> stray_branches(heads + ["talk/demo"], {"wp-a"}, {"mine"})
    (['old-b'], ['qc/release'])
    """
    stray = [
        h
        for h in heads
        if h not in LONG_LIVED
        and h not in open_heads
        and h not in this
        and not h.startswith(TOLERATED_PREFIXES)
    ]
    return stray, [h for h in heads if h.startswith("qc/")]


def remote_heads(root: Path, remote: str) -> dict[str, str]:
    """The remote's branches and their tips, ``{name: sha}``."""
    r = _git(root, "ls-remote", "--heads", remote)
    if r.returncode != 0:
        raise RuntimeError(r.stderr.strip() or f"git ls-remote {remote} failed")
    tips = {}
    for line in r.stdout.splitlines():
        if "\t" in line:
            sha, ref = line.split("\t", 1)
            tips[ref.split("refs/heads/", 1)[1]] = sha
    return tips


def this_branch(root: Path, remote: str, tips: dict[str, str]) -> set[str]:
    """The remote branch the check runs on: ``HEAD``'s remote-tracking branch on ``remote`` when it
    has one, and any remote branch whose tip is ``HEAD``."""
    head = _commit(root, "HEAD")
    this = {name for name, sha in tips.items() if sha == head}
    upstream = _git(root, "rev-parse", "--abbrev-ref", "--symbolic-full-name", "@{upstream}")
    if upstream.returncode == 0 and upstream.stdout.strip().startswith(f"{remote}/"):
        this.add(upstream.stdout.strip()[len(remote) + 1 :])
    return this


def open_pull_request_heads(root: Path) -> set[str]:
    r = subprocess.run(
        ["gh", "pr", "list", "--state", "open", "--limit", "200", "--json", "headRefName"],
        cwd=root,
        capture_output=True,
        text=True,
    )
    if r.returncode != 0:
        raise RuntimeError(r.stderr.strip() or "gh pr list failed")
    return {p["headRefName"] for p in json.loads(r.stdout)}


def gh_authenticated() -> bool:
    try:
        return subprocess.run(["gh", "auth", "status"], capture_output=True).returncode == 0
    except FileNotFoundError:
        return False


def branch_problems(root: Path, remote: str = "origin") -> tuple[list[str], list[str]]:
    """The notices to print and the stray branches that fail the check."""
    tips = remote_heads(root, remote)
    this = this_branch(root, remote, tips)
    stray, dry_runs = stray_branches(list(tips), open_pull_request_heads(root), this)
    notices = [f"branches: {len(tips)} on {remote}; long-lived {', '.join(LONG_LIVED)}"]
    notices += [f"branches: {h} is this branch (its pull request comes next)" for h in sorted(this)]
    notices += [f"branches: {h} is a dry-run branch; delete it after its run" for h in dry_runs]
    notices += [
        f"branches: {h} is a talk branch; it stays until a code owner deletes it"
        for h in sorted(tips)
        if h.startswith("talk/")
    ]
    return notices, [
        f"{remote}/{h} is neither long-lived, an open pull request's head, qc/, talk/ nor "
        "dependabot/; delete it (GOVERNANCE.md, Branches)"
        for h in stray
    ]


# ------------------------------------------------------------------ the gates, run locally

# The test modules that hold the repository's rules (the fast shard in full is CI's).
RULE_MODULES = (
    "tests/test_release_checks.py",
    "tests/test_release_workflows.py",
    "tests/test_ci_shards.py",
    "tests/test_admissibility.py",
    "tests/test_repo_settings.py",
    "tests/test_api_surface.py",
    "tests/test_interface_contract.py",
    "tests/test_package.py",
    "tests/test_index.py",
    "tests/test_claims_register.py",
    "tests/test_site.py::test_hand_written_pages_carry_no_review_or_proof_content",
)
ATTRIBUTION = re.compile(r"\bco-authored-by\b|\bgenerated with\b|🤖", re.I)
Run = Callable[[Path], tuple[int | None, str]]


@dataclass
class Gate:
    """One check: its name, what it runs (for the table) and how; ``release`` marks the
    admissibility checks of ``--release``; ``needs_gh`` skips it when ``gh`` is not
    authenticated."""

    name: str
    run: Run
    argv: tuple[str, ...] = ()
    release: bool = False
    needs_gh: bool = False


def command(*argv: str) -> Run:
    def run(root: Path) -> tuple[int, str]:
        r = subprocess.run(list(argv), cwd=root, capture_output=True, text=True)
        # The ok line quotes stdout alone (a library's stderr chatter is not the result); a
        # failure shows both.
        text = r.stdout if r.returncode == 0 else r.stdout + r.stderr
        return r.returncode, text.strip()

    return run


def problems_of(fn: Callable[[Path], list[str]]) -> Run:
    def run(root: Path) -> tuple[int, str]:
        problems = fn(root)
        return (1 if problems else 0), "\n".join(problems)

    return run


def attribution_lines(root: Path, since: str) -> list[str]:
    """The commit-message lines since ``since`` that carry an attribution (the Tests workflow's
    grep); the whole log when the ref is absent."""
    rng = f"{since}..HEAD" if _commit(root, since) else "HEAD"
    log = _git(root, "log", "--format=%B", rng).stdout
    hits = [line for line in log.splitlines() if ATTRIBUTION.search(line)]
    return [f"{len(hits)} attribution line(s) in the commits of {rng}: {hits[:3]}"] if hits else []


def _release_version(root: Path) -> str:
    return tomllib.loads((root / "pyproject.toml").read_text(encoding="utf-8"))["project"][
        "version"
    ]


def _tag_check(root: Path) -> tuple[int, str]:
    version = _release_version(root)
    state, reason = tag_state(root, f"v{version}", "HEAD")
    return (1 if state == "taken" else 0), f"v{version} is {state}" + (
        f": {reason}" if reason else ""
    )


def gates(release: bool, since: str) -> list[Gate]:
    """The checks in order; ``release`` appends the admissibility checks."""
    uv = ("uv", "run")
    out = [
        Gate("attribution", problems_of(lambda r: attribution_lines(r, since)), ("git", "log")),
        Gate("uv lock --check", command("uv", "lock", "--check"), ("uv", "lock", "--check")),
        Gate("ruff check", command(*uv, "ruff", "check", "."), (*uv, "ruff", "check", ".")),
        Gate(
            "ruff format --check",
            command(*uv, "ruff", "format", "--check", "."),
            (*uv, "ruff", "format", "--check", "."),
        ),
        Gate(
            "pytest (the rule modules)",
            command(*uv, "pytest", "-q", "-p", "no:cacheprovider", "-n", "auto", *RULE_MODULES),
            (*uv, "pytest", *RULE_MODULES),
        ),
        Gate(
            "vocabulary",
            command(*uv, "python", "scripts/check_vocabulary.py"),
            (*uv, "python", "scripts/check_vocabulary.py"),
        ),
        Gate(
            "api surface record",
            command(*uv, "python", "scripts/api_surface.py", "--check"),
            (*uv, "python", "scripts/api_surface.py", "--check"),
        ),
        Gate(
            "repository settings",
            command(*uv, "--no-project", "python", "scripts/check_repo_settings.py"),
            (*uv, "--no-project", "python", "scripts/check_repo_settings.py"),
            needs_gh=True,
        ),
        Gate(
            "branches", problems_of(lambda r: branch_problems(r)[1]), ("branches",), needs_gh=True
        ),
    ]
    if release:
        out += [
            Gate(
                "version",
                command(*uv, "--no-project", "python", "scripts/check_release_version.py"),
                ("check_release_version.py",),
                release=True,
            ),
            Gate("tag", _tag_check, ("tag", "--sha", "HEAD"), release=True),
            Gate(
                "changelog --final",
                problems_of(lambda r: changelog_problems(r, _release_version(r), True)),
                ("changelog", "--final"),
                release=True,
            ),
            Gate(
                "version-kind",
                command(*uv, "--locked", "python", "scripts/release_checks.py", "version-kind"),
                ("version-kind",),
                release=True,
            ),
            Gate("pins", problems_of(pin_problems), ("pins",), release=True),
            Gate(
                "paper mode (served)",
                command(
                    *uv,
                    "--no-project",
                    "python",
                    "scripts/paper_mode.py",
                    "check",
                    "--stage",
                    "served",
                ),
                ("paper_mode.py", "check", "--stage", "served"),
                release=True,
            ),
        ]
    return out


def run_gates(root: Path, checks: list[Gate], out=sys.stdout, gh: bool | None = None) -> int:
    """Run the checks in order, one line each, a verdict; 1 when any fails."""
    head = _git(root, "rev-parse", "--short=12", "HEAD").stdout.strip()
    branch = _git(root, "rev-parse", "--abbrev-ref", "HEAD").stdout.strip()
    print(f"gates at {head} ({branch}): {len(checks)} checks", file=out)
    failed, skipped = [], []
    for gate in checks:
        if gate.needs_gh:
            gh = gh_authenticated() if gh is None else gh
            if not gh:
                skipped.append(gate.name)
                print(f"  skip  {gate.name}: gh is not authenticated", file=out)
                continue
        code, text = gate.run(root)
        first = text.splitlines()[-1] if text else ""
        if code == 0:
            print(f"  ok    {gate.name}" + (f": {first}" if first else ""), file=out)
            continue
        failed.append(gate)
        print(f"  FAIL  {gate.name} (exit {code})", file=out)
        for line in text.splitlines()[-12:]:
            print(f"        {line}", file=out)
    tail = f"; {len(skipped)} skipped ({', '.join(skipped)})" if skipped else ""
    if not failed:
        print(f"verdict: pass ({len(checks) - len(skipped)} checks{tail})", file=out)
        return 0
    names = ", ".join(g.name for g in failed)
    print(f"verdict: refused ({len(failed)} of {len(checks)}: {names}{tail})", file=out)
    if all(g.release for g in failed):
        print(
            "the Tests gates pass; the release gates refuse this head. A head at a released"
            " version is not releasable: `release_checks.py bump` first (`--changelog stub` for"
            " a dry run).",
            file=out,
        )
    return 1


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
    b = sub.add_parser("bump", help="write a new version in every place it is written")
    b.add_argument("version", help="the new version, PEP 440, above the current one")
    b.add_argument(
        "--date", help="YYYY-MM-DD: the changelog heading and CITATION.cff's release day"
    )
    b.add_argument(
        "--changelog",
        required=True,
        choices=CHANGELOG_MODES,
        help="final: release the unreleased entry; stub: a dry-run entry; none: leave it",
    )
    b.add_argument("--no-lock", action="store_true", help="do not run uv lock (the tests)")
    g = sub.add_parser("gates", help="run the repository's checks locally, in order")
    g.add_argument("--release", action="store_true", help="also the release admissibility checks")
    g.add_argument("--since", default="origin/dev", help="the attribution grep's base ref")
    br = sub.add_parser("branches", help="the remote branches that should not be there")
    br.add_argument("--remote", default="origin")
    parser.add_argument("--root", type=Path, default=ROOT)
    args = parser.parse_args(argv)
    if args.check == "gates":
        return run_gates(args.root, gates(args.release, args.since))
    if args.check == "bump":
        changed, problems = bump(
            args.root, args.version, args.date, args.changelog, lock=not args.no_lock
        )
        for path in changed:
            print(f"changed: {path}")
        for p in problems:
            print(f"refused: {p}", file=sys.stderr)
        if not problems:
            print(f"bump: {args.version} written in {len(changed)} files; nothing committed")
        return 1 if problems else 0
    if args.check == "branches":
        try:
            notices, problems = branch_problems(args.root, args.remote)
        except RuntimeError as e:
            print(f"refused: {e}", file=sys.stderr)
            return 2
        for line in notices:
            print(line)
    elif args.check == "version-kind":
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

"""The index of work packages dereferences; nothing outside the record names a removed path (WP73).

``work-packages/INDEX.md`` names, for every archived package, the commit its documents are read at
(``git show <hash>:work-packages/<file>``) and, for every removed note or spike output, its commit
and path. These tests run the dereference: each hash is a commit of this repository whose tree
holds that package's documents; each concrete path exists at its commit; each file the index says
is in place is in the working tree; and no tracked file outside ``work-packages/`` names, as a bare
path, a file that one of those commits held and the tree no longer does. A citation of a removed
document carries its commit, ``<hash>:work-packages/<file>`` or a ``blob/<hash>/`` URL, and that
form passes. A shallow clone has no history to dereference, so the tests skip there (CI checks out
depth 1).
"""

from __future__ import annotations

import re
import subprocess
from functools import cache
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "work-packages" / "INDEX.md"
RECORD = "work-packages/"

SHOW = re.compile(r"`git show ([0-9a-f]{7,40}):([^`]+)`")
IN_PLACE = re.compile(r"`([^`]+)` in place")
# a path of the record written bare: not after a hash and a colon, not inside a URL
BARE = re.compile(r"(?<![\w:/.-])work-packages/[\w./-]+")
# a URL to the record on main, which is bare in the same sense once the file has left main
ON_MAIN = re.compile(r"(?:blob|tree)/main/(work-packages/[\w./-]+)")
BINARY = {
    ".png",
    ".jpg",
    ".jpeg",
    ".gif",
    ".pdf",
    ".npz",
    ".gz",
    ".zip",
    ".whl",
    ".ico",
    ".woff",
    ".woff2",
    ".ttf",
}


def _git(*args: str) -> subprocess.CompletedProcess:
    return subprocess.run(["git", *args], cwd=ROOT, capture_output=True, text=True, check=False)


def _full_history() -> bool:
    return _git("rev-parse", "--is-shallow-repository").stdout.strip() == "false"


pytestmark = pytest.mark.skipif(
    not _full_history(),
    reason="no full git history to dereference (shallow clone or no repository)",
)


def _exists_at(hash_: str, path: str) -> bool:
    return _git("cat-file", "-e", f"{hash_}:{path}").returncode == 0


def _is_commit(hash_: str) -> bool:
    return _git("cat-file", "-e", f"{hash_}^{{commit}}").returncode == 0


@cache
def _package_rows() -> list[tuple[str, str]]:
    """``(wp, documents)`` for every row of the index's first table."""
    rows = []
    for line in INDEX.read_text(encoding="utf-8").splitlines():
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) == 6 and cells[0] not in {"WP", "---"}:
            rows.append((cells[0], cells[5]))
    return rows


@cache
def _index_hashes() -> set[str]:
    return {h for h, _ in SHOW.findall(INDEX.read_text(encoding="utf-8"))}


@cache
def _tracked() -> list[str]:
    return _git("ls-files", "-z").stdout.split("\0")[:-1]


@cache
def _removed() -> tuple[set[str], set[str]]:
    """The record's files held by a commit the index names and absent from the tree, and their
    directories."""
    tracked = set(_tracked())
    files: set[str] = set()
    for h in _index_hashes():
        held = _git("ls-tree", "-r", "--name-only", h, RECORD).stdout.split("\n")
        files.update(p for p in held if p and p not in tracked)
    dirs: set[str] = set()
    for f in files:
        parts = Path(f).parts
        dirs.update("/".join(parts[:k]) for k in range(2, len(parts)))
    return files, dirs


def test_every_in_history_row_dereferences():
    """Each archived package's hash is a commit whose record holds that package's documents."""
    problems = []
    for wp, documents in _package_rows():
        m = SHOW.search(documents)
        if "in history" not in documents or not m or not m.group(2).endswith("<file>"):
            continue
        h = m.group(1)
        if not _is_commit(h):
            problems.append(f"WP{wp}: {h} is not a commit")
            continue
        names = _git("ls-tree", "--name-only", h, RECORD).stdout.split()
        if not any(Path(n).name.startswith(f"WP{wp}-") for n in names):
            problems.append(f"WP{wp}: no WP{wp}- document under {RECORD} at {h}")
    assert problems == []


def test_every_concrete_path_exists_at_its_commit():
    """Each ``git show <hash>:<path>`` of the index with a real path (the removed notes and spike
    outputs, the moved files) dereferences."""
    problems = [
        f"{h}:{path}"
        for h, path in SHOW.findall(INDEX.read_text(encoding="utf-8"))
        if "<" not in path and not _exists_at(h, path)
    ]
    assert problems == []


def test_every_document_the_index_keeps_in_place_is_in_the_tree():
    missing = [
        name
        for _, documents in _package_rows()
        for name in IN_PLACE.findall(documents)
        if not (ROOT / RECORD / name).exists()
    ]
    assert missing == []


def _bare_mentions(text: str) -> list[tuple[int, str]]:
    out = []
    for n, line in enumerate(text.splitlines(), 1):
        found = [m.group(0) for m in BARE.finditer(line)] + ON_MAIN.findall(line)
        for raw in found:
            p = raw.rstrip(".,;:)").rstrip("/")
            if p == "work-packages":
                continue
            carried = re.search(
                rf"(?:[0-9a-f]{{7,40}}:|(?:blob|tree)/[0-9a-f]{{7,40}}/){re.escape(p)}", line
            )
            if not carried:
                out.append((n, p))
    return out


def test_nothing_outside_the_record_names_a_removed_path():
    """A bare path of a document that left the tree is a dangling reference; the citation carries
    the commit instead (``<hash>:work-packages/<file>``), or the file is moved and the reader
    repointed, or the mention is dropped."""
    files, dirs = _removed()
    assert files, "the index names no commit with removed documents"
    offenders = []
    for rel in _tracked():
        if rel.startswith(RECORD) or Path(rel).suffix.lower() in BINARY:
            continue
        try:
            text = (ROOT / rel).read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        for n, p in _bare_mentions(text):
            if (p in files or p in dirs) and not (ROOT / p).exists():
                offenders.append(f"{rel}:{n}: {p}")
    assert offenders == [], "\n".join(offenders)


# The scanner itself, on text it must and must not flag.


def test_bare_mention_scanner():
    text = (
        "see `work-packages/WP1-scope-of-work.md` and\n"
        "`git show abc1234:work-packages/WP1-scope-of-work.md` carried\n"
        "https://example/blob/abc1234/work-packages/WP2-review.md carried\n"
        "https://example/blob/main/work-packages/WP2-review.md on main\n"
        "work-packages/ alone; work-packages/WPn-decisions.md; (work-packages/WP3-rounds/).\n"
    )
    assert _bare_mentions(text) == [
        (1, "work-packages/WP1-scope-of-work.md"),
        (4, "work-packages/WP2-review.md"),
        (5, "work-packages/WPn-decisions.md"),
        (5, "work-packages/WP3-rounds"),
    ]

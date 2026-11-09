"""Append-only JSONL ledger of hashed experiment entries.

One JSON object per line. Each entry carries ``prev_hash`` (the previous entry's ``entry_hash``,
null for the first) and ``entry_hash`` (sha256 of the canonical JSON of the entry without that
field), so editing or deleting any line breaks the chain. File paths are relative to a root
directory; ``verify`` recomputes every file hash against that root.

Core modules import no modeling tool; tool versions come from ``importlib.metadata``.
"""

from __future__ import annotations

import datetime as dt
import hashlib
import importlib.metadata
import json
import platform
import subprocess
from dataclasses import dataclass
from pathlib import Path

import pandas as pd

LEDGER_PATH = Path(__file__).resolve().parent / "ledger" / "ledger.jsonl"
REPO_ROOT = Path(__file__).resolve().parents[3]
KINDS = ("generated", "adopted")
FIELDS = (
    "id",
    "kind",
    "time_utc",
    "git_commit",
    "git_dirty",
    "evidence_kind",
    "model_path",
    "model_sha256",
    "code",
    "output_path",
    "output_rows",
    "output_sha256",
    "versions",
    "platform",
    "inputs",
    "parents",
    "prev_hash",
    "entry_hash",
)


class LedgerError(RuntimeError):
    """The ledger refused an operation (rewrite, duplicate id, broken parent)."""


@dataclass(frozen=True)
class Drift:
    """One discrepancy found by ``verify``: the entry, what drifted, and the detail."""

    entry_id: str
    what: str
    detail: str

    def __str__(self) -> str:
        return f"{self.entry_id}: {self.what} ({self.detail})"


def sha256_file(path: Path) -> str:
    """Hex sha256 of a file's bytes."""
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def hash_entry(entry: dict) -> str:
    """sha256 of the canonical JSON of ``entry`` without its ``entry_hash``."""
    body = {k: v for k, v in entry.items() if k != "entry_hash"}
    blob = json.dumps(body, sort_keys=True, separators=(",", ":"), ensure_ascii=True)
    return hashlib.sha256(blob.encode()).hexdigest()


def read(ledger_path: Path) -> list[dict]:
    """All entries, in file order (empty when the file does not exist)."""
    p = Path(ledger_path)
    if not p.exists():
        return []
    return [json.loads(line) for line in p.read_text().splitlines() if line.strip()]


def find(entries: list[dict], entry_id: str) -> dict | None:
    """The entry with ``entry_id`` or ``None``."""
    return next((e for e in entries if e["id"] == entry_id), None)


def append(ledger_path: Path, entry: dict) -> dict:
    """Append ``entry``; link it to the chain and return it with ``prev_hash``, ``entry_hash``.

    Refuses a duplicate id, an unknown kind or evidence kind, missing fields, and a ledger whose
    chain is already broken. Existing lines are never rewritten.
    """
    p = Path(ledger_path)
    entries = read(p)
    if find(entries, entry.get("id")) is not None:
        raise LedgerError(f"entry {entry.get('id')!r} exists; the ledger is append-only")
    if entry.get("kind") not in KINDS:
        raise LedgerError(f"kind {entry.get('kind')!r} not in {KINDS}")
    missing = [k for k in FIELDS if k not in entry and k not in ("prev_hash", "entry_hash")]
    if missing:
        raise LedgerError(f"entry {entry.get('id')!r} lacks fields {missing}")
    prev = None
    for e in entries:
        if e["prev_hash"] != prev or e["entry_hash"] != hash_entry(e):
            raise LedgerError(f"ledger chain is broken at {e['id']!r}; run verify")
        prev = e["entry_hash"]
    out = {k: v for k, v in entry.items() if k not in ("prev_hash", "entry_hash")}
    out["prev_hash"] = prev
    out["entry_hash"] = hash_entry(out)
    p.parent.mkdir(parents=True, exist_ok=True)
    with open(p, "a") as f:
        f.write(json.dumps(out, sort_keys=True, ensure_ascii=True) + "\n")
    return out


def _git(root: Path, *args: str) -> str | None:
    try:
        r = subprocess.run(
            ["git", "-C", str(root), *args], capture_output=True, text=True, check=True
        )
    except (OSError, subprocess.CalledProcessError):
        return None
    return r.stdout.strip()


def git_state(root: Path) -> tuple[str | None, bool | None]:
    """``(commit, dirty)`` of the repository at ``root``; ``(None, None)`` outside one."""
    commit = _git(root, "rev-parse", "HEAD")
    if commit is None:
        return None, None
    status = _git(root, "status", "--porcelain")
    return commit, bool(status)


def last_commit_of(root: Path, path: str) -> str | None:
    """The newest commit that touched ``path``."""
    return _git(root, "log", "-1", "--format=%H", "--", path) or None


def versions() -> dict:
    """Runtime versions; ``opensysml`` is read from metadata, never imported."""
    import numpy
    import scipy

    try:
        osml = importlib.metadata.version("opensysml")
    except importlib.metadata.PackageNotFoundError:
        osml = None
    return {
        "opensysml": osml,
        "python": platform.python_version(),
        "numpy": numpy.__version__,
        "scipy": scipy.__version__,
        "pandas": pd.__version__,
    }


def platform_string() -> str:
    """Platform description recorded in every entry."""
    return platform.platform()


def utc_now() -> str:
    """UTC time, ISO 8601 with a ``Z`` suffix."""
    return dt.datetime.now(dt.UTC).strftime("%Y-%m-%dT%H:%M:%SZ")


def hash_files(root: Path, paths) -> dict[str, str]:
    """``{path: sha256}`` for root-relative paths."""
    return {str(p): sha256_file(Path(root) / p) for p in paths}


def count_rows(path: Path) -> int:
    """Data rows of a CSV file."""
    return len(pd.read_csv(path))


def verify(ledger_path: Path, root: Path) -> list[Drift]:
    """Recompute every hash; return one ``Drift`` per discrepancy (empty means consistent).

    Checks per entry: the entry hash and chain link, the model hash, each code file hash, the
    output hash and row count, and that each parent exists earlier with the recorded hashes.
    """
    root = Path(root)
    entries = read(ledger_path)
    drifts: list[Drift] = []
    prev = None
    seen: dict[str, dict] = {}

    def check(entry_id, what, rel, expected):
        path = root / rel
        if not path.exists():
            drifts.append(Drift(entry_id, f"{what} missing", rel))
        elif sha256_file(path) != expected:
            drifts.append(Drift(entry_id, f"{what} changed", rel))

    for e in entries:
        i = e.get("id", "?")
        if e.get("entry_hash") != hash_entry(e):
            drifts.append(Drift(i, "entry content edited", "entry_hash differs from content"))
        if e.get("prev_hash") != prev:
            drifts.append(Drift(i, "chain broken", "prev_hash is not the previous entry_hash"))
        prev = e.get("entry_hash")
        if e.get("model_path"):
            check(i, "model", e["model_path"], e["model_sha256"])
        for rel, h in e.get("code", {}).items():
            check(i, "code file", rel, h)
        check(i, "output", e["output_path"], e["output_sha256"])
        out = root / e["output_path"]
        if out.exists() and sha256_file(out) == e["output_sha256"]:
            rows = count_rows(out)
            if rows != e["output_rows"]:
                drifts.append(Drift(i, "output rows changed", f"{rows} != {e['output_rows']}"))
        for par in e.get("parents", []):
            pe = seen.get(par["id"])
            if pe is None:
                drifts.append(Drift(i, "parent not earlier in ledger", par["id"]))
            elif pe["entry_hash"] != par["entry_hash"]:
                drifts.append(Drift(i, "parent entry changed", par["id"]))
        seen[i] = e
    return drifts

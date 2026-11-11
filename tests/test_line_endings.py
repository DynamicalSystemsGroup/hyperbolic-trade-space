"""Hashed text files are LF on every checkout, and the hashing reads bytes as committed (WP34)."""

import subprocess
from pathlib import Path

from experiments import ledger as lg

REPO = Path(__file__).resolve().parents[1]


def test_gitattributes_keeps_text_at_lf():
    attrs = (REPO / ".gitattributes").read_text(encoding="utf-8").splitlines()
    assert "* text=auto eol=lf" in attrs


def test_every_file_the_ledger_hashes_has_no_crlf_in_this_checkout():
    hashed = set()
    for e in lg.read(lg.LEDGER_PATH):
        hashed.update(e.get("code", {}))
        for key in ("model_path", "output_path"):
            if e.get(key):
                hashed.add(e[key])
    assert hashed
    crlf = sorted(p for p in hashed if (REPO / p).is_file() and b"\r\n" in (REPO / p).read_bytes())
    assert crlf == []


def test_git_resolves_eol_lf_for_text_types():
    paths = ["a.csv", "a.sysml", "a.py", "a.md", "a.svg", "a.json", "a.jsonl", "a.toml"]
    out = subprocess.run(
        ["git", "-C", str(REPO), "check-attr", "eol", "--", *paths],
        capture_output=True,
        text=True,
        check=True,
    ).stdout.splitlines()
    assert len(out) == len(paths)
    assert all(line.endswith(": eol: lf") for line in out), out


def test_hash_is_of_the_bytes_as_committed(tmp_path):
    """The digest is over the bytes (LF and CRLF differ), so checkouts are held at LF."""
    lf, crlf = tmp_path / "lf.txt", tmp_path / "crlf.txt"
    lf.write_bytes(b"a\nb\n")
    crlf.write_bytes(b"a\r\nb\r\n")
    assert lg.sha256_file(lf) == lg.sha256_file(lf)
    assert lg.sha256_file(lf) != lg.sha256_file(crlf)

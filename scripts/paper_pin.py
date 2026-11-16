"""Write a pin into the paper's mode file (specification 2.4): before the tag and after its release.

    uv run --no-project python scripts/paper_pin.py prepare --tag T [--date YYYY-MM-DD] [--dry-run]
    uv run --no-project python scripts/paper_pin.py record --tag T --doi D [--repo R] [--dry-run]

``prepare`` (on ``paper``, before ``git tag``) writes ``mode``, ``pin``, ``venue``, ``round`` and
``date`` into ``paper/mode.toml`` from the tag and empties ``doi`` and ``sha256``; a working tag
carries its date, the other shapes take ``--date`` or today. ``record`` (after the tag's release
is published and Zenodo has minted the DOI) downloads ``paper-html.tar.gz`` from the release with
``gh``, writes its SHA-256 and the DOI, and checks ``--stage served``. Both check the result before
writing and, with ``--dry-run``, print the new file and change nothing. Exit 0 written, 1 a check
failed (the reason printed), 2 usage. It never commits or pushes.
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import os
import subprocess
import sys
import tempfile
import tomllib
from collections.abc import Callable
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import paper_mode as pm

ASSET = "paper-html.tar.gz"
Gh = Callable[[list[str]], int]


def run_gh(args: list[str]) -> int:
    """Run ``gh`` with ``args``; its exit status."""
    return subprocess.run(["gh", *args], check=False).returncode


def _report(bad: list[tuple[str, str]]) -> int:
    for key, reason in bad:
        print(f"paper_pin: {key}: {reason}")
    return 1


def _write(path: Path, fields: dict, stage: str, tag: str, dry_run: bool) -> int:
    bad = pm.problems(fields, stage, tag)
    if bad:
        return _report(bad)
    text = pm.render(fields)
    if dry_run:
        print(text, end="")
        return 0
    path.write_text(text, encoding="utf-8")
    print(f"paper_pin: {path} written: {fields['mode']} {fields['pin']}")
    return 0


def prepare(path: Path, tag: str, date: str | None, dry_run: bool) -> int:
    mode, groups = pm.parse_tag(tag)  # the caller has checked the shape
    if "date" in groups:
        d = groups["date"]
        tag_date = f"{d[:4]}-{d[4:6]}-{d[6:]}"
        if date is not None and date != tag_date:
            return _report([("date", f"--date {date} differs from the tag's {tag_date}")])
        date = tag_date
    fields = dict(
        schema=1,
        mode=mode,
        pin=tag,
        venue=groups.get("venue", ""),
        round=int(groups.get("round", 0)),
        date=date or dt.date.today().isoformat(),
        doi="",
        sha256="",
    )
    return _write(path, fields, "tag", tag, dry_run)


def record(path: Path, tag: str, doi: str, repo: str | None, dry_run: bool, gh: Gh) -> int:
    try:
        fields = pm.load(path)
    except (OSError, tomllib.TOMLDecodeError) as exc:
        return _report([("file", f"{path} unreadable ({exc})")])
    if fields.get("pin") != tag:
        return _report([("pin", f"is {fields.get('pin')!r}; run prepare --tag {tag} first")])
    with tempfile.TemporaryDirectory() as tmp:
        args = ["release", "download", tag, "--pattern", ASSET, "--dir", tmp]
        if repo:
            args += ["--repo", repo]
        if gh(args) != 0 or not (Path(tmp) / ASSET).is_file():
            return _report([("sha256", f"gh could not download {ASSET} from the release {tag}")])
        digest = hashlib.sha256((Path(tmp) / ASSET).read_bytes()).hexdigest()
    return _write(path, {**fields, "doi": doi, "sha256": digest}, "served", tag, dry_run)


def main(argv: list[str] | None = None, gh: Gh = run_gh) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    sub = ap.add_subparsers(dest="command", required=True)
    p = sub.add_parser("prepare", help="write the pin's mode, venue, round and date")
    p.add_argument("--tag", required=True)
    p.add_argument("--date")
    r = sub.add_parser("record", help="write the pin's checksum and DOI after its release")
    r.add_argument("--tag", required=True)
    r.add_argument("--doi", required=True)
    r.add_argument("--repo", default=os.environ.get("GITHUB_REPOSITORY"))
    for s in (p, r):
        s.add_argument("--file", type=Path, default=pm.MODE_FILE)
        s.add_argument("--dry-run", action="store_true")
    args = ap.parse_args(argv)
    if pm.parse_tag(args.tag) is None:
        print(f"paper_pin: {args.tag!r} is no paper tag", file=sys.stderr)
        return 2
    if args.command == "prepare":
        if args.date is not None and not pm._iso(args.date):
            print(f"paper_pin: --date {args.date!r} is not YYYY-MM-DD", file=sys.stderr)
            return 2
        return prepare(args.file, args.tag, args.date, args.dry_run)
    return record(args.file, args.tag, args.doi, args.repo, args.dry_run, gh)


if __name__ == "__main__":
    sys.exit(main())

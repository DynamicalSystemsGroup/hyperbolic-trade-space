"""The paper's mode file, ``paper/mode.toml``: its tag shapes, its validation and its banner line.

    uv run --no-project python scripts/paper_mode.py check [--stage tag|served] [--tag T] [--file F]
    uv run --no-project python scripts/paper_mode.py show [--json] [--file PATH]
    uv run --no-project python scripts/paper_mode.py parse TAG

The paper has four modes (``abstract``, ``working``, ``submitted``, ``revision``); every mode but
``abstract`` names a pin, a ``paper-*`` tag whose GitHub release holds the built paper
(``paper-html.tar.gz``) and its key manifest (``paper-keys.json``). ``check`` validates the file:
``--stage tag`` before the pin's release exists (the DOI and the checksum may be empty),
``--stage served`` when the site serves it (both required outside ``abstract``). ``check`` prints
``paper_mode: ok <mode> <pin>`` or one line per broken rule, ``paper_mode: <field>: <reason>``, and
exits 0 or 1. ``show`` prints the fields and the banner line. ``parse`` prints the mode and the
groups of a tag and exits 2 when it is no paper tag. Exit 2 is a usage error everywhere. Standard
library only.

>>> parse_tag("paper-revision-ieee-tse-r2")
('revision', {'venue': 'ieee-tse', 'round': '2'})
>>> parse_tag("v0.1.0") is None
True
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import sys
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MODE_FILE = ROOT / "paper" / "mode.toml"
MODES = ("abstract", "working", "submitted", "revision")
_VENUE = r"(?P<venue>[a-z0-9]+(?:-[a-z0-9]+)*)"
TAG_SHAPES = {
    "working": re.compile(r"^paper-working-(?P<date>\d{8})(?:-(?P<n>[2-9]|[1-9]\d+))?$"),
    "submitted": re.compile(rf"^paper-submitted-{_VENUE}$"),
    "revision": re.compile(rf"^paper-revision-{_VENUE}-r(?P<round>[1-9]\d*)$"),
}
# The fields and their types, in the file's order.
FIELDS = {
    "schema": int,
    "mode": str,
    "pin": str,
    "venue": str,
    "round": int,
    "date": str,
    "doi": str,
    "sha256": str,
}
COMMENTS = {
    "mode": "abstract | working | submitted | revision",
    "pin": "the paper tag served; empty in abstract mode",
    "venue": "slug; submitted and revision only",
    "round": "revision only, from 1",
    "date": "YYYY-MM-DD of the pin",
    "doi": "10.5281/zenodo.<n>, minted for the pin's release",
    "sha256": "SHA-256 of the pin's paper-html.tar.gz",
}
DOI = re.compile(r"^10\.5281/zenodo\.\d+$")
SHA256 = re.compile(r"^[0-9a-f]{64}$")
ISO_DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
STAGES = ("tag", "served")


def parse_tag(tag: str) -> tuple[str, dict] | None:
    """The mode a paper tag belongs to and its groups (only those the tag carries), or None."""
    for mode, shape in TAG_SHAPES.items():
        if m := shape.match(tag):
            return mode, {k: v for k, v in m.groupdict().items() if v is not None}
    return None


def _iso(value: str) -> bool:
    if not ISO_DATE.match(value):
        return False
    try:
        dt.date.fromisoformat(value)
    except ValueError:
        return False
    return True


def problems(fields: dict, stage: str = "tag", tag: str | None = None) -> list[tuple[str, str]]:
    """Every broken rule of specification 3.1, as ``(field, reason)``; empty when the file holds.

    >>> problems(dict(schema=1, mode="abstract", pin="", venue="", round=0, date="", doi="",
    ...               sha256=""), "served")
    []
    """
    out: list[tuple[str, str]] = []
    for key in fields.keys() - FIELDS.keys():
        out.append((key, "unknown key"))
    for key, typ in FIELDS.items():
        if key not in fields:
            out.append((key, "missing"))
        elif type(fields[key]) is not typ:
            out.append((key, f"must be {'an integer' if typ is int else 'a string'}"))
    if out:
        return sorted(out)
    f = fields
    if f["schema"] != 1:
        out.append(("schema", f"is {f['schema']}, must be 1"))
    mode = f["mode"]
    if mode not in MODES:
        return [*out, ("mode", f"{mode!r} is not one of {', '.join(MODES)}")]
    if mode == "abstract":
        for key in ("pin", "venue", "date", "doi", "sha256"):
            if f[key]:
                out.append((key, "must be empty in abstract mode"))
        if f["round"] != 0:
            out.append(("round", "must be 0 in abstract mode"))
    else:
        parsed = parse_tag(f["pin"])
        matched = parsed is not None and parsed[0] == mode
        groups = parsed[1] if matched else {}
        if not matched:
            out.append(("pin", f"{f['pin']!r} does not have the shape of a {mode} tag"))
        # The tag's groups where the pin has the shape; empty and 0 where the shape has none.
        if (matched or mode == "working") and f["venue"] != groups.get("venue", ""):
            out.append(("venue", f"is {f['venue']!r}, the tag's is {groups.get('venue', '')!r}"))
        if (matched or mode != "revision") and f["round"] != int(groups.get("round", 0)):
            out.append(("round", f"is {f['round']}, the tag's is {int(groups.get('round', 0))}"))
        if not _iso(f["date"]):
            out.append(("date", f"{f['date']!r} is not an ISO date (YYYY-MM-DD)"))
        elif "date" in groups:
            d = groups["date"]
            want = f"{d[:4]}-{d[4:6]}-{d[6:]}"
            if f["date"] != want:
                out.append(("date", f"is {f['date']}, the tag's is {want}"))
        for key, shape in (("doi", DOI), ("sha256", SHA256)):
            if f[key] and not shape.match(f[key]):
                out.append((key, f"{f[key]!r} does not match {shape.pattern}"))
            elif not f[key] and stage == "served":
                out.append((key, f"required when the site serves a pin ({mode} mode)"))
    if tag is not None and f["pin"] != tag:
        out.append(("pin", f"is {f['pin']!r}, not the tag {tag!r}"))
    return out


def banner(fields: dict) -> str:
    """The one line the site puts at the top of every page of a pin; empty in abstract mode.

    >>> banner(dict(mode="working", pin="paper-working-20261120", venue="", round=0,
    ...             date="2026-11-20", doi="10.5281/zenodo.123"))
    'Working paper · paper-working-20261120 · 2026-11-20 · DOI 10.5281/zenodo.123'
    """
    mode = fields["mode"]
    if mode == "abstract":
        return ""
    head = {
        "working": "Working paper",
        "submitted": f"Submitted to {fields['venue']}",
        "revision": f"Revision {fields['round']} for {fields['venue']}",
    }[mode]
    parts = [head, fields["pin"], fields["date"]]
    if fields.get("doi"):
        parts.append(f"DOI {fields['doi']}")
    return " · ".join(parts)


def render(fields: dict) -> str:
    """The file's text for ``fields``, in the committed form (one field a line, commented)."""
    lines = []
    for key in FIELDS:
        value = fields[key]
        text = f"{key} = {value}" if isinstance(value, int) else f"{key} = {json.dumps(value)}"
        if key in COMMENTS:
            text = f"{text:<19} # {COMMENTS[key]}"
        lines.append(text)
    return "\n".join(lines) + "\n"


def load(path: Path = MODE_FILE) -> dict:
    """The file's fields; raises ``OSError`` or ``tomllib.TOMLDecodeError``."""
    with open(path, "rb") as fh:
        return tomllib.load(fh)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    sub = ap.add_subparsers(dest="command", required=True)
    check = sub.add_parser("check", help="validate the mode file")
    check.add_argument("--stage", choices=STAGES, default="tag")
    check.add_argument("--tag")
    check.add_argument("--file", type=Path, default=MODE_FILE)
    show = sub.add_parser("show", help="print the fields and the banner line")
    show.add_argument("--json", action="store_true")
    show.add_argument("--file", type=Path, default=MODE_FILE)
    parse = sub.add_parser("parse", help="print the mode and the groups of a tag")
    parse.add_argument("tag")
    args = ap.parse_args(argv)

    if args.command == "parse":
        parsed = parse_tag(args.tag)
        if parsed is None:
            print(f"paper_mode: {args.tag!r} is no paper tag", file=sys.stderr)
            return 2
        mode, groups = parsed
        print(" ".join([mode, *(f"{k}={v}" for k, v in groups.items())]))
        return 0

    if not args.file.is_file():
        print(f"paper_mode: file: {args.file} not found", file=sys.stderr)
        return 2
    try:
        fields = load(args.file)
    except tomllib.TOMLDecodeError as exc:
        print(f"paper_mode: file: not valid TOML ({exc})")
        return 1

    if args.command == "show":
        bad = problems(fields, "tag")
        if bad:
            for key, reason in bad:
                print(f"paper_mode: {key}: {reason}")
            return 1
        if args.json:
            print(json.dumps({**fields, "banner": banner(fields)}, indent=2))
        else:
            for key in FIELDS:
                print(f"{key}: {fields[key]}")
            print(f"banner: {banner(fields) or '-'}")
        return 0

    bad = problems(fields, args.stage, args.tag)
    for key, reason in bad:
        print(f"paper_mode: {key}: {reason}")
    if bad:
        return 1
    print(f"paper_mode: ok {fields['mode']} {fields['pin'] or '-'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

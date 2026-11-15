"""The release gates that read files: the changelog, the action pins and the bill of materials.

    uv run python scripts/release_checks.py changelog --version 0.1.0 [--final] [--notes out.md]
    uv run python scripts/release_checks.py pins
    uv run python scripts/release_checks.py sbom --sbom sbom.cdx.json

``changelog`` needs a ``## [version]`` heading; with ``--final`` (a tag release) it must have
one, otherwise an ``## [Unreleased]`` heading also serves (a candidate on TestPyPI). ``pins``
fails on any action in ``.github/workflows`` that is not pinned to a 40-character commit.
``sbom`` fails unless the CycloneDX file names every package, at its locked version, that
``uv.lock`` names.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
USES = re.compile(r"^\s*(?:-\s+)?uses:\s*(\S+)", re.M)
PINNED = re.compile(r"^[\w.-]+/[\w.-]+(?:/[\w./-]+)?@[0-9a-f]{40}$")


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
    parser.add_argument("--root", type=Path, default=ROOT)
    args = parser.parse_args(argv)
    if args.check == "changelog":
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

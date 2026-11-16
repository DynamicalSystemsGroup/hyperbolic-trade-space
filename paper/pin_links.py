"""Point the built paper's links to repository files at the pin's tag (specification 2.7).

    uv run python paper/pin_links.py --ref paper-working-20261120 paper/_build/html

The committed notebooks link files as ``.../hyperbolic-trade-space/blob/main/<path>`` (and
``tree/main`` for folders), which is true once ``main`` carries the release. The artefact a pin
publishes links the files as they were at the pin: every ``blob/main/`` and ``tree/main/`` in each
``.html`` and ``.json`` file under the directory becomes ``blob/<ref>/`` and ``tree/<ref>/``. Prints
the count per file. Exit 0, or 1 when nothing was replaced (the generators' constant moved without
this script following); 2 a usage error.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

REPO = "https://github.com/DynamicalSystemsGroup/hyperbolic-trade-space"
KINDS = ("blob", "tree")
SUFFIXES = (".html", ".json")


def pin_text(text: str, ref: str) -> tuple[str, int]:
    """``text`` with the ``main`` links pointed at ``ref``, and the number replaced.

    >>> pin_text(REPO + "/blob/main/src/a.py and " + REPO + "/tree/main/docs/", "paper-x")[1]
    2
    """
    count = 0
    for kind in KINDS:
        old, new = f"{REPO}/{kind}/main/", f"{REPO}/{kind}/{ref}/"
        count += text.count(old)
        text = text.replace(old, new)
    return text, count


def pin_dir(root: Path, ref: str) -> dict[str, int]:
    """Rewrite every ``.html`` and ``.json`` file under ``root``; the count per file changed."""
    counts = {}
    for path in sorted(p for p in root.rglob("*") if p.is_file() and p.suffix in SUFFIXES):
        text = path.read_text(encoding="utf-8")
        new, n = pin_text(text, ref)
        if n:
            path.write_text(new, encoding="utf-8")
            counts[path.relative_to(root).as_posix()] = n
    return counts


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--ref", required=True, help="the tag the links point at")
    ap.add_argument("dir", type=Path, help="the built paper (paper/_build/html)")
    args = ap.parse_args(argv)
    if not args.dir.is_dir() or not args.ref.strip() or "/" in args.ref:
        print(f"pin_links: needs a directory and a tag name ({args.dir}, {args.ref!r})")
        return 2
    counts = pin_dir(args.dir, args.ref)
    for rel, n in counts.items():
        print(f"pin_links: {rel}: {n}")
    total = sum(counts.values())
    print(f"pin_links: {total} link(s) in {len(counts)} file(s) point at {args.ref}")
    return 0 if total else 1


if __name__ == "__main__":
    sys.exit(main())

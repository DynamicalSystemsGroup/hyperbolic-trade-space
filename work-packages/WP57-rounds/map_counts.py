"""Counts behind the WP57 map: words and cells per appendix subsection, and the citing sentences.

Usage (from the repository root, with the wp55 copy of the paper beside it or any path):

    uv run python work-packages/WP57-rounds/map_counts.py [--paper PATH] [--supp PATH] [--json]

Typed prose is the markdown of the supporting material (headings and MyST anchor lines excluded).
Generated words are the stored outputs of its code cells (text/markdown, text/plain, text/html
stripped of tags). A cell belongs to the subsection whose heading precedes it. The citing sentences
are the paper's markdown sentences that hold a ``{ref}`` to ``appendix-<x>`` or ``sub-<x>-<n>``,
with the ``(sect-...)=`` anchor they sit under.
"""

from __future__ import annotations

import argparse
import json
import re
from collections import defaultdict
from pathlib import Path

import nbformat

ROOT = Path(__file__).resolve().parents[2]
SUPP = ROOT / "paper" / "supporting_material.ipynb"
PAPER = ROOT / "paper-wp55.ipynb"

HEADING = re.compile(r"^(#{2,3})\s+(Appendix ([A-H])\.|([A-H])\.(\d+))\s*(.*)$", re.M)
ANCHOR = re.compile(r"^\(([a-z0-9-]+)\)=\s*$", re.M)
REF = re.compile(r"\{ref\}`([^`<]*)<((?:appendix-[a-h])|(?:sub-[a-h]-\d+))>`")
TAG = re.compile(r"<[^>]+>")
WORD = re.compile(r"\S+")
FENCES = {
    "::::",
    ":::",
    ":remove-input: true",
    "% container-paragraph:begin",
    "% container-paragraph:end",
}


def words(text: str) -> int:
    return len(WORD.findall(text))


def prose_of(md: str) -> str:
    lines = []
    for line in md.splitlines():
        if ANCHOR.match(line) or line.startswith("#") or line.startswith("---"):
            continue
        if line.strip() in FENCES:
            continue
        lines.append(line)
    return "\n".join(lines)


def output_text(cell) -> str:
    parts = []
    for out in cell.get("outputs", []):
        data = out.get("data", {})
        if "text/markdown" in data:
            parts.append("".join(data["text/markdown"]))
        elif "text/html" in data:
            parts.append(TAG.sub(" ", "".join(data["text/html"])))
        elif "text/plain" in data:
            parts.append("".join(data["text/plain"]))
        elif out.get("output_type") == "stream":
            parts.append("".join(out.get("text", "")))
    return "\n".join(parts)


def table_rows(text: str) -> int:
    """Rows of markdown tables in a rendered output (header and separator excluded)."""
    rows = 0
    for block in re.split(r"\n\s*\n", text):
        lines = [ln for ln in block.splitlines() if ln.strip().startswith("|")]
        if len(lines) >= 3 and set(lines[1].replace("|", "").strip()) <= set(":- "):
            rows += len(lines) - 2
    return rows


def _section(key: str, letter: str, title: str, anchor: str) -> dict:
    return {
        "key": key,
        "appendix": letter,
        "title": title,
        "anchor": anchor,
        "cells": [],
        "md": [],
        "out": [],
    }


def _call(source: str) -> str:
    lines = [ln.strip() for ln in source.splitlines() if ln.strip()]
    return " ".join(ln for ln in lines if not ln.startswith(("from", "import")))


def subsections(supp_path: Path) -> list[dict]:
    nb = nbformat.read(supp_path, as_version=4)
    current = _section("front", "front", "Front matter", "")
    sections = [current]
    for i, cell in enumerate(nb.cells):
        if cell.cell_type == "markdown":
            m = HEADING.search(cell.source)
            if m:
                letter = m.group(3) or m.group(4)
                num = m.group(5)
                key = f"{letter}" if not num else f"{letter}.{num}"
                a = ANCHOR.search(cell.source)
                current = _section(key, letter, m.group(6).strip(), a.group(1) if a else "")
                sections.append(current)
        current["cells"].append((i, cell.cell_type, cell.metadata.get("tags", [])))
        if cell.cell_type == "markdown":
            current["md"].append(prose_of(cell.source))
        else:
            current["out"].append(output_text(cell))
            current.setdefault("calls", []).append(_call(cell.source))
    rows = []
    for s in sections:
        md = "\n".join(s["md"])
        out = "\n".join(s["out"])
        rows.append(
            {
                "key": s["key"],
                "appendix": s["appendix"],
                "anchor": s["anchor"],
                "title": s["title"],
                "cells": len(s["cells"]),
                "md_cells": sum(1 for c in s["cells"] if c[1] == "markdown"),
                "code_cells": sum(1 for c in s["cells"] if c[1] == "code"),
                "cell_ids": [c[0] for c in s["cells"]],
                "prose_words": words(md),
                "generated_words": words(out),
                "table_rows": table_rows(out),
                "calls": s.get("calls", []),
            }
        )
    return rows


def sentences(text: str) -> list[str]:
    text = re.sub(r"\s+", " ", text)
    return [s.strip() for s in re.split(r"(?<=[.!?])\s+(?=[A-Z{*])", text) if s.strip()]


def citations(paper_path: Path) -> dict[str, list[dict]]:
    nb = nbformat.read(paper_path, as_version=4)
    section = "front"
    out: dict[str, list[dict]] = defaultdict(list)
    for i, cell in enumerate(nb.cells):
        if cell.cell_type != "markdown":
            continue
        for a in ANCHOR.finditer(cell.source):
            if a.group(1).startswith("sect-"):
                section = a.group(1)
        for sent in sentences(cell.source):
            for m in REF.finditer(sent):
                out[m.group(2)].append({"section": section, "cell": i, "sentence": sent})
    return out


SECTION_NUMBERS = {
    "sect-problem": 1,
    "sect-prior-art": 2,
    "sect-notation": 3,
    "sect-definitions": 4,
    "sect-methods": 5,
    "sect-results": 6,
    "sect-case-construction": 7,
    "sect-case-analysis": 8,
    "sect-discussion": 9,
    "sect-future": 10,
    "sect-process": 11,
    "sect-cited": 12,
}


def first_mention_order(paper_path: Path) -> list[tuple[str, int, int]]:
    """Appendix letters by the paper cell (and position) of their first mention."""
    nb = nbformat.read(paper_path, as_version=4)
    first: dict[str, tuple[int, int]] = {}
    for i, cell in enumerate(nb.cells):
        if cell.cell_type != "markdown":
            continue
        for m in REF.finditer(cell.source):
            target = m.group(2)
            letter = target.split("-")[1].upper()
            pos = (i, m.start())
            if letter not in first or pos < first[letter]:
                first[letter] = pos
    return sorted(((k, *v) for k, v in first.items()), key=lambda t: (t[1], t[2]))


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--paper", default=str(PAPER))
    ap.add_argument("--supp", default=str(SUPP))
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args(argv)
    rows = subsections(Path(args.supp))
    cites = citations(Path(args.paper))
    order = first_mention_order(Path(args.paper))
    if args.json:
        out = {"subsections": rows, "citations": cites, "first_mention": order}
        print(json.dumps(out, indent=1))
        return 0
    head = f"{'key':6} {'anchor':12} {'cells':>5} {'md':>3} {'code':>4} {'prose':>6} {'gener.':>7} "
    print(head + f"{'rows':>5}  cited by")
    totals: dict[str, list[int]] = defaultdict(lambda: [0, 0, 0, 0])
    for r in rows:
        secs = sorted({SECTION_NUMBERS.get(c["section"], 0) for c in cites.get(r["anchor"], [])})
        left = f"{r['key']:6} {r['anchor']:12} {r['cells']:5d} {r['md_cells']:3d} "
        left += f"{r['code_cells']:4d} "
        right = f"{r['prose_words']:6d} {r['generated_words']:7d} {r['table_rows']:5d}  "
        print(left + right + str(secs if secs else "-"))
        t = totals[r["appendix"]]
        t[0] += r["cells"]
        t[1] += r["prose_words"]
        t[2] += r["generated_words"]
        t[3] += r["table_rows"]
    print()
    print(f"{'appendix':8} {'cells':>5} {'prose':>6} {'gener.':>7} {'rows':>5}")
    for k, t in totals.items():
        print(f"{k:8} {t[0]:5d} {t[1]:6d} {t[2]:7d} {t[3]:5d}")
    tot = [sum(t[i] for t in totals.values()) for i in range(4)]
    print(f"{'all':8} {tot[0]:5d} {tot[1]:6d} {tot[2]:7d} {tot[3]:5d}")
    print()
    print("first mention in the paper (letter, paper cell, offset):", order)
    print()
    for target, lst in sorted(cites.items()):
        for c in lst:
            where = f"{target:12} S{SECTION_NUMBERS.get(c['section'], 0):<2} cell {c['cell']:3d}: "
            print(where + c["sentence"][:160])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

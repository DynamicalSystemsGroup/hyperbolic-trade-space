"""WP57e: the re-executed notebooks' outputs against the base, cell by cell.

    uv run python work-packages/WP57-rounds/e/output_diff.py

Pairs code cells by id (through ``reletter.IDS``) and compares each cell's outputs as JSON text. A
cell whose new outputs are what the letter map makes of the old (``reletter.rewrite``) changed
only in letters and numbers; any other change is listed. Exits 1 if there is one.
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import nbformat

sys.path.insert(0, str(Path(__file__).resolve().parent))
import reletter

ROOT = reletter.ROOT


def _strip(out: dict) -> dict:
    """An output without its execution count, which the new cell order renumbers."""
    return {k: v for k, v in out.items() if k != "execution_count"}


def _rows(text: str) -> list[str]:
    """A table's rows as a sorted list, the commit row (observed at each run) left out."""
    rows = json.loads(text)
    lines = []
    for out in rows:
        body = out.get("text") or "".join(out.get("data", {}).get("text/markdown", ""))
        lines += [ln for ln in body.splitlines() if not ln.startswith("| Commit |")]
    return sorted(lines)


def main() -> int:
    bad = 0
    for path in ("paper/paper.ipynb", "paper/supporting_material.ipynb"):
        text = subprocess.run(
            ["git", "-C", str(ROOT), "show", f"{reletter.BASE}:{path}"],
            capture_output=True,
            text=True,
            check=True,
        ).stdout
        old = nbformat.reads(text, as_version=4)
        new = {c.id: c for c in nbformat.read(ROOT / path, as_version=4).cells}
        same = letters = 0
        other = []
        for c in old.cells:
            if c.cell_type != "code":
                continue
            n = new[reletter.IDS.get(c.id, c.id)]
            a = json.dumps([_strip(o) for o in c.outputs], sort_keys=True)
            b = json.dumps([_strip(o) for o in n.outputs], sort_keys=True)
            if a == b:
                same += 1
            elif reletter.rewrite(a, path) == b:
                letters += 1
            elif _rows(reletter.rewrite(a, path)) == _rows(b):
                print(f"  {n.id}: same rows up to letters, their order and the commit observed")
                letters += 1
            else:
                other.append(n.id)
        print(f"{path}: {same} code cells' outputs unchanged, {letters} changed in letters only")
        for cid in other:
            print(f"  OTHER {cid}")
            bad += 1
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())

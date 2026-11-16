"""WP57e R-4: the two notebooks' sources against the base, word by word.

    uv run python work-packages/WP57-rounds/e/word_diff.py [--base 6d86038d]

Cells are paired by id through the re-lettering's id map (``reletter.IDS``; an id with no letter
is its own pair), so the reordering of the supporting material is not a difference. Each pair's
source is split into words and compared with ``difflib``; every changed run of words must be what
the letter map makes of the old run (``reletter.rewrite``), so a change that is not a letter or a
subsection number is reported. Prints, per notebook and cell type: cells paired, cells changed,
words changed, the distinct old -> new tokens with their counts, and every other change (none
expected); exits 1 if there is any, or if a cell was cut or added.
"""

from __future__ import annotations

import argparse
import difflib
import json
import re
import subprocess
import sys
from collections import Counter
from pathlib import Path

import nbformat

sys.path.insert(0, str(Path(__file__).resolve().parent))
import reletter

ROOT = reletter.ROOT
NOTEBOOKS = ("paper/paper.ipynb", "paper/supporting_material.ipynb")


def _base(path: str, base: str):
    out = subprocess.run(
        ["git", "-C", str(ROOT), "show", f"{base}:{path}"],
        capture_output=True,
        text=True,
        check=True,
    ).stdout
    return nbformat.reads(out, as_version=4)


def _letter_token(x: str, y: str, before: str, where: str) -> bool:
    """A word the letter map makes of the old one: a label, a subsection number, or the bare
    letter after the word "Appendix" ("Appendix B, L5", "## Appendix A.", "Appendix H's")."""
    if reletter.rewrite(x, where) == y:
        return True
    m = re.fullmatch(r"([A-H])(\W.*)?", x)
    after_appendix = before.rsplit("`", 1)[-1] in ("Appendix", "Appendices")
    return bool(m) and after_appendix and y == reletter.LETTER[x[0]] + x[1:]


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--base", default=reletter.BASE)
    args = ap.parse_args(argv)
    bad = 0
    for path in NOTEBOOKS:
        old = _base(path, args.base)
        new = nbformat.read(ROOT / path, as_version=4)
        new_by_id = {c.id: c for c in new.cells}
        mapped = [reletter.IDS.get(c.id, c.id) for c in old.cells]
        cut = [m for m in mapped if m not in new_by_id]
        added = sorted(set(new_by_id) - set(mapped))
        print(f"{path}: {len(old.cells)} cells at the base, {len(new.cells)} now")
        if cut or added:
            print(f"  cut {cut}, added {added}")
            bad += 1
        if path.endswith("supporting_material.ipynb"):
            order = [c.id for c in new.cells]
            print(f"  order changed: {order != mapped}")
        for kind in ("markdown", "code"):
            pairs = changed = words = 0
            tokens: Counter = Counter()
            other = []
            for oc in old.cells:
                if oc.cell_type != kind:
                    continue
                nc = new_by_id[reletter.IDS.get(oc.id, oc.id)]
                pairs += 1
                a, b = oc.source.split(), nc.source.split()
                if a == b:
                    continue
                changed += 1
                sm = difflib.SequenceMatcher(a=a, b=b, autojunk=False)
                for op, i1, i2, j1, j2 in sm.get_opcodes():
                    if op == "equal":
                        continue
                    was, now = " ".join(a[i1:i2]), " ".join(b[j1:j2])
                    words += max(i2 - i1, j2 - j1)
                    ok = (i2 - i1) == (j2 - j1) and all(
                        _letter_token(x, y, a[k - 1] if k else "", path)
                        for k, x, y in zip(range(i1, i2), a[i1:i2], b[j1:j2], strict=True)
                    )
                    if ok:
                        for x, y in zip(a[i1:i2], b[j1:j2], strict=True):
                            tokens[(x, y)] += 1
                    else:
                        other.append((nc.id, was, now))
            print(f"  {kind}: {pairs} cells paired, {changed} changed, {words} words changed")
            for (x, y), n in sorted(tokens.items(), key=lambda t: (-t[1], t[0])):
                print(f"    {n:4d}  {x}  ->  {y}")
            for cid, was, now in other:
                print(f"    OTHER {cid}: {was!r} -> {now!r}")
                bad += 1
    print(json.dumps({"other_changes": bad}))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())

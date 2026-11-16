"""WP57e R-4: every residual count equal to before under its renamed key.

    uv run python work-packages/WP57-rounds/e/residual_keys.py BEFORE.json AFTER.json

BEFORE is ``check_residuals.py --write-baseline`` on the base tree, AFTER the same on this tree.
Each appendix surface key of BEFORE is renamed by the letter map (``appendix/d-16`` to
``appendix/b-11``, ``appendix/appendix-g`` to ``appendix/appendix-a``, the old H's slug key to
``appendix/appendix-c``) and its counts compared with AFTER's; every other surface and the file
totals are compared as they are. Prints each difference; exits 1 if there is one.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import reletter


def rename(k: str) -> str:
    m = re.fullmatch(r"appendix/([a-h])-(\d+)", k)
    if m:
        L, n = m.group(1).upper(), int(m.group(2))
        return f"appendix/{reletter.LETTER[L].lower()}-{reletter.SUBMAP[(L, n)]}"
    if k.startswith("appendix/appendix-h-horopca"):
        return "appendix/appendix-c"
    m = re.fullmatch(r"appendix/appendix-([a-h])", k)
    if m:
        return f"appendix/appendix-{reletter.LETTER[m.group(1).upper()].lower()}"
    return k


def main() -> int:
    before = json.loads(Path(sys.argv[1]).read_text())
    after = json.loads(Path(sys.argv[2]).read_text())
    b = {rename(k): v for k, v in before["surfaces"].items()}
    a = after["surfaces"]
    if "appendix/appendix-a" in b and "appendix/appendix-a" not in a:
        # The front matter (two words) folds into the next piece of its status, now Appendix A.
        t, r = b.pop("appendix/title"), b.pop("appendix/appendix-a")
        b["appendix/title"] = {
            c: (max(t[c], r[c]) if c.startswith("max_") else t[c] + r[c])
            for c in t
            if isinstance(t[c], int)
        }
        print("front matter folded into Appendix A: compared as one surface, appendix/title")
    diffs = []
    for k in sorted(set(a) | set(b)):
        if k not in a or k not in b:
            diffs.append(f"{k}: only {'before' if k in b else 'after'}")
            continue
        for c in ("words", "prose_words", *sorted(x for x in a[k] if isinstance(a[k][x], int))):
            if a[k].get(c) != b[k].get(c):
                diffs.append(f"{k}: {c} {b[k].get(c)} -> {a[k].get(c)}")
    renamed = sum(1 for k in before["surfaces"] if rename(k) != k)
    print(f"{len(a)} surfaces after, {len(b)} before, {renamed} keys renamed")
    tb, ta = before.get("totals", {}), after.get("totals", {})
    for f in sorted(set(tb) | set(ta)):
        if tb.get(f) != ta.get(f):
            diffs.append(f"totals {f}: {tb.get(f)} -> {ta.get(f)}")
    for d in sorted(set(diffs)):
        print(" ", d)
    print(f"{len(set(diffs))} differences")
    return 1 if diffs else 0


if __name__ == "__main__":
    sys.exit(main())

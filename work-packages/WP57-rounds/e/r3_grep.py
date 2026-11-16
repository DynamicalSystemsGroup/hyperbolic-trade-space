"""WP57e R-3: every surviving letter occurrence in the tree, classified.

    uv run python work-packages/WP57-rounds/e/r3_grep.py

Greps the tracked tree (``git grep``; ``_build``, ``.venv``, ``site`` and ``_stage`` are not tracked
or are excluded) for ``appendix-x``, ``sub-x-n``, ``app-X``, ``tab-X-``, ``sent-X-``, "Appendix X"
and "X.n". Each occurrence is one of:

- dated: a file that records a state at a date (the list below), or a dated field of a live file
  (a ledger row's text, a register row's ``source`` and ``note``, a comment that says "the old");
- new: anything else, read in the new letters; a token naming a subsection the new structure lacks
  is reported as ``CHECK``, to be read (none expected outside dated text).
"""

from __future__ import annotations

import re
import subprocess
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
PATTERN = (
    r"appendix-[a-h]\b|sub-[a-h]-[0-9]+|\b(app|tab|sent)-[A-Ha-h]\b|\b(app|tab|sent)-[A-Ha-h]-"
    r"|Appendi(x|ces) [A-H]\b|\b[A-H]\.[0-9]+\b"
)
DATED = (
    "work-packages/",
    "paper/container/RECORD.md",
    "derivation/PROOF_MAP_FINDINGS.md",
    "docs/superpowers/notes/",
    "notes/directions/",
    "notes/user-journeys.md",
    "notes/references-verified.md",
    "notes/paper-prior-art-sources.md",
    "examples/adcs/experiments/reports/",
    "scripts/vocabulary_baseline.toml",
)
LIVE_NOTES = {"docs/superpowers/notes/abstraction-gaps.md"}  # the gaps ledger G.2 prints
NEW_SUBS = {"A": 1, "B": 14, "C": 4, "D": 0, "E": 3, "F": 8, "G": 3, "H": 4}
DATED_FIELDS = {
    "paper/length_ledger.toml": re.compile(
        r"^(job|reader|no_longer_did|authority|what|why|note) = |^#(?! And| The same| below|"
        r" The supporting)"
    ),
    "claims_register.toml": re.compile(r"^(source|note) = "),
}
OLD_MARK = re.compile(r"\b(the old|old|until WP57|since WP57|WP57[a-d]:)\b", re.I)
SUB = re.compile(r"\b([A-H])\.([0-9]+)\b|sub-([a-h])-([0-9]+)")


def main() -> int:
    out = subprocess.run(
        ["git", "-C", str(ROOT), "grep", "-n", "-I", "-P", PATTERN, "--", "."],
        capture_output=True,
        text=True,
    ).stdout
    per: dict[str, Counter] = defaultdict(Counter)
    checks = []
    for line in out.splitlines():
        path, num, text = line.split(":", 2)
        if path.endswith(".ipynb"):
            kind = "new"
        elif path.startswith(DATED) and path not in LIVE_NOTES:
            kind = "dated (file)"
        elif path in DATED_FIELDS and DATED_FIELDS[path].search(text):
            kind = "dated (row text)"
        elif path.startswith("tests/") and OLD_MARK.search(text):
            kind = "dated (history comment)"
        else:
            kind = "new"
        n = len(re.findall(PATTERN, text))
        per[path][kind] += n
        if kind == "new":
            for m in SUB.finditer(text):
                letter = (m.group(1) or m.group(3)).upper()
                k = int(m.group(2) or m.group(4))
                if k > NEW_SUBS[letter]:
                    checks.append(f"{path}:{num}: {m.group(0)} :: {text.strip()[:140]}")
    total = Counter()
    print("| File | new | dated | dated kind |")
    print("|---|---|---|---|")
    for path in sorted(per):
        c = per[path]
        total.update(c)
        dated = {k: v for k, v in c.items() if k != "new"}
        print(f"| `{path}` | {c['new']} | {sum(dated.values())} | {', '.join(dated)} |")
    print(f"\nTotals: {dict(total)}")
    print(f"CHECK (a new-sense line naming a subsection the new structure lacks): {len(checks)}")
    for c in checks:
        print("  CHECK", c)
    return 0


if __name__ == "__main__":
    sys.exit(main())

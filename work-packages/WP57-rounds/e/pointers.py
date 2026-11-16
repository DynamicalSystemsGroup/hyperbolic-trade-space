"""WP57e R-2: every pointer of the paper to the supporting material, its target before and after.

    uv run python work-packages/WP57-rounds/e/pointers.py

Reads the paper's ``{ref}`` roles at the base and now, paired in order (cell by cell), and the
generated links of ``generate_findings.py`` (its ``appendix_link`` constants); resolves each label
to its heading in the supporting material of the same commit, and prints a Markdown table. A row
whose two headings differ beyond their letter and number is marked; exits 1 if any is.
"""

from __future__ import annotations

import re
import subprocess
import sys
from collections import Counter
from pathlib import Path

import nbformat

sys.path.insert(0, str(Path(__file__).resolve().parent))
import reletter

ROOT = reletter.ROOT
ROLE = re.compile(r"\{ref\}`([^`<]*?)\s*<((?:appendix-[a-h])|(?:sub-[a-h]-\d+))>`")
LINK = re.compile(r'^(_\w+) = appendix_link\("([^"]+)", "([^"]+)"\)', re.M)


def _show(path: str) -> str:
    return subprocess.run(
        ["git", "-C", str(ROOT), "show", f"{reletter.BASE}:{path}"],
        capture_output=True,
        text=True,
        check=True,
    ).stdout


def headings(nb) -> dict[str, str]:
    out = {}
    for c in nb.cells:
        if c.cell_type != "markdown":
            continue
        for label, head in re.findall(r"^\(([\w-]+)\)=\n#+ (.+)$", c.source, re.M):
            out[label] = head.strip()
    return out


def _bare(head: str) -> str:
    return re.sub(r"^(Appendix [A-H]\.|[A-H]\.\d+) ", "", head)


def main() -> int:
    old_paper = nbformat.reads(_show("paper/paper.ipynb"), as_version=4)
    new_paper = nbformat.read(ROOT / "paper/paper.ipynb", as_version=4)
    old_h = headings(nbformat.reads(_show("paper/supporting_material.ipynb"), as_version=4))
    new_h = headings(nbformat.read(ROOT / "paper/supporting_material.ipynb", as_version=4))
    rows: Counter = Counter()
    bad = 0
    for oc, nc in zip(old_paper.cells, new_paper.cells, strict=True):
        if oc.cell_type != "markdown":
            continue
        olds, news = ROLE.findall(oc.source), ROLE.findall(nc.source)
        assert len(olds) == len(news), oc.id
        for (ot, ol), (nt, nl) in zip(olds, news, strict=True):
            rows[(nc.id, ot, ol, old_h[ol], nt, nl, new_h[nl])] += 1
    old_links = LINK.findall(_show("paper/generate_findings.py"))
    new_links = LINK.findall((ROOT / "paper/generate_findings.py").read_text(encoding="utf-8"))
    for (on, ol, ot), (nn, nl, nt) in zip(old_links, new_links, strict=True):
        rows[(f"generated `{on}` -> `{nn}`", ot, ol, old_h[ol], nt, nl, new_h[nl])] += 1
    targets: dict[tuple, list] = {}
    for (where, ot, ol, oh, nt, nl, nh), n in rows.items():
        targets.setdefault((ol, oh, nl, nh), []).append((where, ot, nt, n))
    head = (
        "| Before: label, heading | After: label, heading | Pointers (cell: text before -> after) |"
    )
    print(head)
    print("|---|---|---|")
    for (ol, oh, nl, nh), uses in targets.items():
        same = _bare(oh) == _bare(nh)
        bad += not same
        mark = "" if same else " **DIFFERS**"
        texts = Counter()
        for _where, ot, nt, n in uses:
            texts[(ot, nt)] += n
        cells = ", ".join(sorted({w for w, *_ in uses}))
        said = "; ".join(
            f"{o} -> {t}" + (f" (x{n})" if n > 1 else "") for (o, t), n in texts.items()
        )
        print(f"| `{ol}` {oh} | `{nl}` {nh}{mark} | {cells}: {said} |")
    print(f"\n{sum(rows.values())} pointers to {len(targets)} targets, {bad} differ")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())

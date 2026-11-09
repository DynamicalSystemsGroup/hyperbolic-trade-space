"""Appendix G and section 2's family table, compiled from ``prior_art.yaml``.

One source, two views: the register (every entry, grouped by family, with the four fields and the
"why this is not just X" sentence of the nearest neighbours) and section 2's table (the entries
flagged ``section2``, with the same wording).
"""

from __future__ import annotations

import yaml
from paper_common import Md, md_table
from paper_paths import PAPER

SOURCE = PAPER / "prior_art.yaml"
FIELDS = ("does", "shares", "differs", "cites")


def entries(path=SOURCE) -> list[dict]:
    """The entries of ``prior_art.yaml`` with whitespace of the folded scalars normalized."""
    raw = yaml.safe_load(path.read_text(encoding="utf-8"))["entries"]
    out = []
    for e in raw:
        e = dict(e)
        for k, v in e.items():
            if isinstance(v, str):
                e[k] = " ".join(v.split())
        out.append(e)
    return out


def cite(keys) -> str:
    """A pandoc-style citation of the keys, ``[@a; @b]``."""
    return "[" + "; ".join(f"@{k}" for k in keys) + "]"


def family_table(only_section2: bool = True) -> Md:
    """The family table: produces, shares, differs, cites.

    Parameters
    ----------
    only_section2 : bool, default True
        Section 2's table lists the entries flagged ``section2``; ``False`` lists them all.

    Returns
    -------
    Md
    """
    rows = [
        [e["family"], e["does"], e["shares"], e["differs"], cite(e["cites"])]
        for e in entries()
        if e.get("section2") or not only_section2
    ]
    return Md(md_table(["Family", "Produces", "Shares", "Differs", "Cites"], rows))


def register() -> Md:
    """The register of Appendix G: every entry, grouped by family, four fields each.

    Returns
    -------
    Md
        Markdown with one subsection per group and one block per entry.
    """
    es = entries()
    out, group = [], None
    for e in es:
        if e["group"] != group:
            group = e["group"]
            out.append(f"\n#### {group}\n")
        out.append(f"**{e['family']}**\n")
        out.append(f"- *What it does.* {e['does']}")
        out.append(f"- *What this work shares with it or takes from it.* {e['shares']}")
        out.append(f"- *What this work does differently, extends or adds.* {e['differs']}")
        if e.get("why_not_just"):
            out.append(f"- *Why this is not just the neighbour.* {e['why_not_just']}")
        out.append(f"- *Cites.* {cite(e['cites'])}\n")
    return Md("\n".join(out))

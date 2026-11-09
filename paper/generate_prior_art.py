"""Appendix G and section 2's family table, compiled from ``prior_art.yaml``.

One source, two views: the register (every entry, grouped by family, with the four fields and the
"why this is not just X" sentence of the nearest neighbours) and section 2's table (the entries
flagged ``section2``, with the same wording).
"""

from __future__ import annotations

import re

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


BIB = PAPER.parent / "docs" / "references.bib"
_ACCENTS = {'\\"': "\u0308", "\\'": "\u0301", "\\`": "\u0300", "\\^": "\u0302"}


def _plain(text: str) -> str:
    """BibTeX text as plain Unicode: accents composed, braces dropped."""
    import unicodedata

    for tex, mark in _ACCENTS.items():
        text = re.sub(re.escape(tex) + r"\{?(\w)\}?", lambda m, mk=mark: m.group(1) + mk, text)
    return unicodedata.normalize("NFC", text).replace("{", "").replace("}", "")


def author_year(key: str, path=BIB) -> str:
    """The author-year label of a bibliography entry: ``Charnes et al. 1978``.

    Parameters
    ----------
    key : str
        The BibTeX key in ``docs/references.bib``.
    path : pathlib.Path, optional
        The bibliography.

    Returns
    -------
    str
        First author's surname, ``and`` a second or ``et al.`` for more, then the year.
    """
    entry = re.search(rf"@\w+\{{{re.escape(key)},(.*?)\n\}}", path.read_text("utf-8"), re.S).group(
        1
    )
    authors = re.search(r"author\s*=\s*\{(.*?)\},?\s*\n", entry, re.S).group(1)
    year = re.search(r"year\s*=\s*\{(.*?)\}", entry).group(1)
    names = [_plain(" ".join(a.split())).split(",")[0] for a in authors.split(" and ")]
    who = (
        names[0]
        if len(names) == 1
        else f"{names[0]} and {names[1]}"
        if len(names) == 2
        else f"{names[0]} et al."
    )
    return f"{who} {year}"


# The site colours a link in an output cell dark blue in both themes, unreadable on the dark page;
# a link that takes the text colour and is underlined reads in light and dark.
LINK_STYLE = "color:inherit;text-decoration:underline"


def cite(keys, prefix: str = "#") -> str:
    """The citation of the keys as links to the reference list, ``Author Year`` each.

    The generated tables are output cells, which the site does not parse for citations; each
    key therefore becomes an author-year link to its entry in the reference list of the paper
    (``#cite-<key>``). ``prefix`` is ``"#"`` on the paper's page and ``"../#"`` on the
    supporting material's.
    """
    return "; ".join(
        f'<a href="{prefix}cite-{k}" target="_self" style="{LINK_STYLE}">{author_year(k)}</a>'
        for k in keys
    )


def all_cited_keys() -> list[str]:
    """Every bibliography key the tables cite, in order of first appearance.

    The paper cites them once, in a hidden cell, so that the site lists each in the reference
    list that the table's author-year links point to.
    """
    seen: dict[str, None] = {}
    for e in entries():
        seen.update(dict.fromkeys(e["cites"]))
    return list(seen)


def nocite() -> str:
    """The citation group of :func:`all_cited_keys`, ``[@a; @b]``, for the hidden cell."""
    return "[" + "; ".join(f"@{k}" for k in all_cited_keys()) + "]"


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
        out.append(f"- *Cites.* {cite(e['cites'], '../#')}\n")
    return Md("\n".join(out))

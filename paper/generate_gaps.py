"""Appendix E: the abstraction gaps G-1 to G-17, compiled from ``abstraction-gaps.md``.

The ledger's table is read, not retyped: one row per gap with the formal object, the bridging
assumption, what cannot be proved, the sensitivity evidence and the interpretive consequence.
"""

from __future__ import annotations

import re

from paper_common import Md, md_table
from paper_paths import ROOT

LEDGER = ROOT / "docs" / "superpowers" / "notes" / "abstraction-gaps.md"
COLUMNS = (
    "Formal object",
    "What the implementation does",
    "Bridging assumption",
    "What cannot be proved",
    "Sensitivity evidence",
    "Interpretive consequence",
)
ROW = re.compile(r"^\|\s*\*\*(G-\d+)\.\s*(.*?)\*\*\s*(.*)$")


def gap_rows(path=LEDGER) -> list[dict]:
    """The ledger's table as rows: ``id``, ``title`` and the six columns by name.

    Returns
    -------
    list of dict
        One dict per gap, in the ledger's order.
    """
    rows = []
    for line in path.read_text(encoding="utf-8").splitlines():
        m = ROW.match(line)
        if not m:
            continue
        gid, title, rest = m.groups()
        cells = [
            c.strip() for c in re.split(r"(?<!\\)\s\|\s", f"**{gid}. {title}** {rest}".rstrip(" |"))
        ]
        if len(cells) != len(COLUMNS):
            raise ValueError(f"{gid}: {len(cells)} cells, expected {len(COLUMNS)}")
        rows.append({"id": gid, "title": title, **dict(zip(COLUMNS, cells, strict=True))})
    return rows


MATH = re.compile(r"\$([^$]+)\$")


_PUNCT = re.compile(r"\\([!-/:-@\[-`{-~])")


def math_role(text: str) -> str:
    r"""Inline ``$...$`` kept intact through the Markdown-to-HTML step of the page.

    The table reaches the page as HTML (``paper_common.Md``, markdown-it), which reads the
    mathematics as Markdown: ``_`` and ``*`` as emphasis, a backslash before punctuation (``\,``,
    ``\{``) as an escape, ``|`` as a cell border. Inside each ``$...$`` those are escaped so the
    HTML carries the mathematics as written and the page typesets it; a pipe becomes ``\vert``.

    >>> print(math_role(r"a $\|s\|<1$ and $J_\tau\,x$ b"))
    a $\vert s\vert <1$ and $J\_\tau\\,x$ b
    """

    def safe(m):
        body = m.group(1).replace("\\|", "|").replace("|", "\\vert ")
        body = _PUNCT.sub(lambda p: "\\\\" + p.group(1), body)
        body = body.replace("_", "\\_").replace("*", "\\*")
        return "$" + body + "$"

    return MATH.sub(safe, text)


def gaps_table() -> Md:
    """The table of Appendix E: one row per gap, its mathematics typeset (:func:`math_role`).

    Returns
    -------
    Md
        Markdown pipe table; columns are the ledger's.
    """
    rows = gap_rows()
    cols = ("Formal object", "Bridging assumption", "What cannot be proved",
            "Sensitivity evidence", "Interpretive consequence")  # fmt: skip
    body = [[r["id"], *(math_role(r[c]) for c in cols)] for r in rows]
    return Md(md_table(["Gap", *cols], body))

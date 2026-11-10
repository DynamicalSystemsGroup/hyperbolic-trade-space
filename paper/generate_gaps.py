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


def math_role(text: str) -> str:
    r"""Inline ``$...$`` as the MyST ``{math}`` role, which a notebook's Markdown output typesets.

    A pipe inside the mathematics (the ledger escapes it as ``\|`` for its own table) becomes
    ``\vert``, so no pipe is left to split a cell of the pipe table.

    >>> print(math_role(r"a $\|s\|<1$ b"))
    a {math}`\vert s\vert <1` b
    """
    return MATH.sub(
        lambda m: "{math}`" + m.group(1).replace("\\|", "\\vert ").replace("|", "\\vert ") + "`",
        text,
    )


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

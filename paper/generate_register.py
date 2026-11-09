"""Appendix A: the register of notation and terms, compiled from ``glossary.yaml``.

The table is never typed. ``glossary.yaml`` (the shared source of the register's phrases) holds
the fields ``term``, ``symbol``, ``register``, ``formal``, ``not``, ``defined_in``; the table lists
one row per entry in the glossary's order. An optional ``anchor`` field (the scikit-learn or Boyd
and Vandenberghe usage an entry anchors to) is shown as a column when any entry has it.
"""

from __future__ import annotations

import yaml
from paper_common import Md, md_table
from paper_paths import ROOT

GLOSSARY = ROOT / "glossary.yaml"


def glossary_entries(path=GLOSSARY) -> list[dict]:
    """The entries of ``glossary.yaml`` exactly as written."""
    return yaml.safe_load(path.read_text(encoding="utf-8"))["entries"]


def register_rows(entries=None) -> tuple[list[str], list[list[str]]]:
    """Headers and rows of the register table, one row per glossary entry."""
    entries = glossary_entries() if entries is None else entries
    anchored = any(e.get("anchor") for e in entries)
    headers = ["Term", "Symbol", "Meaning in this paper", "Not", "Defined in"]
    if anchored:
        headers.append("Anchored to")
    rows = []
    for e in entries:
        row = [e["register"], f"${e['symbol']}$" if e.get("symbol") else "", e["formal"],
               e["not"], e.get("defined_in", "")]  # fmt: skip
        if anchored:
            row.append(e.get("anchor", ""))
        rows.append(row)
    return headers, rows


def register_table() -> Md:
    """The register table of Appendix A.

    Returns
    -------
    Md
        A Markdown pipe table, one row per entry of ``glossary.yaml``.
    """
    headers, rows = register_rows()
    return Md(md_table(headers, rows))

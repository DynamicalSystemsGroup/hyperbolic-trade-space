"""Appendix D: the register of notation and terms, compiled from ``glossary.yaml``.

The table is never typed. ``glossary.yaml`` (the shared source of the register's phrases) holds
the fields ``term``, ``symbol``, ``register``, ``formal``, ``not``, ``defined_in``; the table lists
one row per entry the paper or the appendices use, in the glossary's order. A use is a match of
the entry's term or an alias in the prose or the generated outputs of ``paper/paper.ipynb`` or
``paper/supporting_material.ipynb``, outside Appendix D, by the rule of
``scripts/check_vocabulary.py`` (the same matching that reports a dead entry); an entry no sentence
of the two documents uses stays in the glossary and off the page. An optional ``anchor`` field (the
scikit-learn or Boyd and Vandenberghe usage an entry anchors to) is shown as a column when any
listed entry has it.
"""

from __future__ import annotations

import re
import sys

import yaml
from paper_common import MdMath, md_table
from paper_paths import ROOT

GLOSSARY = ROOT / "glossary.yaml"
DOCUMENTS = ("paper/paper.ipynb", "paper/supporting_material.ipynb")
"""The two documents whose uses place an entry in the table."""

if str(ROOT / "scripts") not in sys.path:
    sys.path.insert(0, str(ROOT / "scripts"))
import check_vocabulary as cv  # noqa: E402  (the checker's matching; scripts/ is not a package)


def glossary_entries(path=GLOSSARY) -> list[dict]:
    """The entries of ``glossary.yaml`` exactly as written."""
    return yaml.safe_load(path.read_text(encoding="utf-8"))["entries"]


def _paragraphs(root, rel: str) -> list:
    """The paragraphs of a notebook as the checker reads them, less the cells of Appendix D.

    ``check_vocabulary.read_notebook`` marks Appendix D's paragraphs by the heading they sit under,
    which it misses when an anchor line (``(appendix-d)=``) precedes the heading in its cell; the
    cells are taken out here by position instead, from the heading of Appendix D to the next
    appendix heading.
    """
    import json

    cells = json.loads((root / rel).read_text(encoding="utf-8"))["cells"]
    out, skipping = [], False
    for cell in cells:
        source = "".join(cell["source"])
        if cell["cell_type"] == "markdown" and re.search(r"^## Appendix [A-Z]\.", source, re.M):
            skipping = bool(re.search(r"^## Appendix D\.", source, re.M))
        if skipping:
            continue
        chunks = (
            [source]
            if cell["cell_type"] == "markdown"
            else [
                "".join(md) if isinstance(md, list) else md
                for out_ in cell.get("outputs", [])
                if (md := out_.get("data", {}).get("text/markdown"))
            ]
        )
        for chunk in chunks:
            _meta, body = cv.front_matter(chunk)
            out += cv.split_paras(rel, body)
    return out


def used_entry_ids(root=ROOT, documents=DOCUMENTS) -> set[str]:
    """Ids of the glossary entries the paper or the appendices use.

    The rule is ``scripts/check_vocabulary.py``'s: a paragraph of a document (typed Markdown or a
    generated Markdown output) uses an entry when the entry's term or one of its aliases matches
    in it; the paragraphs of Appendix D, the table this filter builds, do not count.
    """
    glossary = cv.load_glossary(root)
    used: set[str] = set()
    for rel in documents:
        for para in _paragraphs(root, rel):
            for seg in cv.segments(para.text):
                spans = cv.match_spans(seg, glossary.phrases, glossary.max_len)
                used.update(ident for _s, _e, (kind, ident) in spans if kind == "entry")
    return used


def symbol_markup(symbol: str) -> str:
    """A symbol as the table prints it: mathematics, or code font for an attribute name.

    A name such as ``conditioning_`` (a fitted attribute of the estimator, with the trailing
    underscore of scikit-learn) is not mathematics; between dollar signs its underscore starts a
    subscript with nothing in it and the page prints a processing error.
    """
    return f"`{symbol}`" if re.fullmatch(r"[A-Za-z]\w*_", symbol) else f"${symbol}$"


def register_rows(entries=None, used=None) -> tuple[list[str], list[list[str]]]:
    """Headers and rows of the register table, one row per glossary entry in use.

    Parameters
    ----------
    entries : list of dict, optional
        The glossary's entries; default the file's.
    used : set of str, optional
        The ids of the entries to list; default :func:`used_entry_ids`.
    """
    entries = glossary_entries() if entries is None else entries
    used = used_entry_ids() if used is None else used
    listed = [e for e in entries if e["id"] in used]
    anchored = any(e.get("anchor") for e in listed)
    headers = ["Term", "Symbol", "Meaning in this paper", "Not", "Defined in"]
    if anchored:
        headers.append("Anchored to")
    rows = []
    for e in listed:
        row = [e["register"], symbol_markup(e["symbol"]) if e.get("symbol") else "", e["formal"],
               e["not"], e.get("defined_in", "")]  # fmt: skip
        if anchored:
            row.append(e.get("anchor", ""))
        rows.append(row)
    return headers, rows


def register_table() -> MdMath:
    """The register table of Appendix D.

    Returns
    -------
    MdMath
        A Markdown pipe table, one row per entry of ``glossary.yaml`` that the paper or the
        appendices use. As Markdown it is the text a notebook viewer typesets; its HTML writes each
        ``$...$`` span as MathML, because the page typesets nothing inside an HTML output.
    """
    headers, rows = register_rows()
    text = md_table(headers, rows)
    return MdMath(text, text)

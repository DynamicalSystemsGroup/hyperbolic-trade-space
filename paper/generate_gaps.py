"""Appendix G: the assumptions, from the derivation's ledger, and the abstraction gaps.

Nothing is retyped. The assumptions tables read ``derivation/axioms.py`` (each entry's statement and
citation), the proof map's record (the results that import each entry) and the paper (the section
whose sentence states it). The gaps table reads ``abstraction-gaps.md``: one row per gap with the
bridging assumption, what cannot be proved and the interpretive consequence, and a link to the
ledger's row, which keeps the formal object and the sensitivity evidence.
"""

from __future__ import annotations

import json
import re

from paper_common import REPO_BLOB, Md, MdMath, link_paths, md_table
from paper_paths import PAPER, ROOT

LEDGER = ROOT / "docs" / "superpowers" / "notes" / "abstraction-gaps.md"
LEDGER_PATH = "docs/superpowers/notes/abstraction-gaps.md"
RECORD = ROOT / "derivation" / "proof_map_record.json"
PAPER_NB = PAPER / "paper.ipynb"
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
        One dict per gap, in the ledger's order; ``line`` is the row's line in the ledger.
    """
    rows = []
    for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        m = ROW.match(line)
        if not m:
            continue
        gid, title, rest = m.groups()
        cells = [
            c.strip() for c in re.split(r"(?<!\\)\s\|\s", f"**{gid}. {title}** {rest}".rstrip(" |"))
        ]
        if len(cells) != len(COLUMNS):
            raise ValueError(f"{gid}: {len(cells)} cells, expected {len(COLUMNS)}")
        rows.append(
            {"id": gid, "title": title, "line": number, **dict(zip(COLUMNS, cells, strict=True))}
        )
    return rows


GAP_COLUMNS = ("Bridging assumption", "What cannot be proved", "Interpretive consequence")
"""The columns of the gaps table after the gap: the formal object and the sensitivity evidence stay
in the ledger's row, which each row links."""

WIDTHS = (120, 230, 230, 230)
"""Column widths in pixels of the table on the page, in the order of its columns (the gap, then the
three), which fit the page's column of about 820 px, each text column at about thirty characters a
line."""

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


def gaps_table() -> MdMath:
    """The gaps table of Appendix G: one row per gap, its mathematics typeset on the page.

    Returns
    -------
    MdMath
        Markdown pipe table: the gap (its id and title, a link to its row of the ledger), the
        bridging assumption, what cannot be proved and the interpretive consequence. As Markdown its
        mathematics is safe for the Markdown step (:func:`math_role`); its HTML writes each
        ``$...$`` as MathML, because the page typesets nothing inside an HTML output.
    """
    rows = gap_rows()
    head = ["Gap", *GAP_COLUMNS]

    def gap(r, body):
        url = f"{REPO_BLOB}{LEDGER_PATH}?plain=1#L{r['line']}"
        return f"[{r['id']}. {body(r['title'].rstrip('.'))}]({url})"

    body = [[gap(r, math_role), *(math_role(link_paths(r[c])) for c in GAP_COLUMNS)] for r in rows]
    raw = [[gap(r, str), *(link_paths(r[c]) for c in GAP_COLUMNS)] for r in rows]
    return MdMath(md_table(head, body), md_table(head, raw), WIDTHS)


# ---- the assumptions: the ledger of the derivation ----------------------------------------------

ASSUMPTION_KINDS = ("A", "R")
"""The entries the assumptions table lists: posited (A) and regularity (R). The results of the
literature (I) and the formal devices of the scripts (F) are the second table's."""

_NUMBERED = re.compile(r"^([AIRF])(\d+)$")


def _ledger():
    from derivation.axioms import AXIOMS

    return AXIOMS


def _key(name: str):
    letter, number = _NUMBERED.match(name).groups()
    return "AIRF".index(letter), int(number)


def _strip_closing_paren(text: str) -> str:
    """The text without a spaced parenthetical that closes it (the ledger's asides), keeping a
    closing argument list such as ``f(x)``."""
    text = " ".join(text.split())
    if text.endswith(")"):
        depth = 0
        for i in range(len(text) - 1, -1, -1):
            depth += {")": 1, "(": -1}.get(text[i], 0)
            if depth == 0:
                return text[:i].rstrip(" ,;") if text[i - 1 : i] == " " else text
    return text


def _first_clause(text: str, sep: str) -> str:
    """``text`` up to the first ``sep`` outside parentheses and brackets."""
    depth = 0
    for i, ch in enumerate(text):
        depth += {"(": 1, "[": 1, "{": 1, ")": -1, "]": -1, "}": -1}.get(ch, 0)
        if depth == 0 and text.startswith(sep, i):
            return text[:i]
    return text


def one_line(statement: str) -> str:
    """A ledger statement in one line: its headline, the words before the first colon when they
    are three or more, else the statement to its first semicolon, without a closing aside.

    >>> one_line("the fit temperature is positive: tau > 0")
    'the fit temperature is positive'
    >>> one_line("noise: eps_j are i.i.d. N(0, sigma^2), with sigma > 0 (an aside)")
    'noise: eps_j are i.i.d. N(0, sigma^2), with sigma > 0'
    >>> one_line("R1 holds; it does not imply the rest")
    'R1 holds'
    """
    text = _strip_closing_paren(statement)
    head = _first_clause(text, ": ")
    if head != text and len(head.split()) >= 3:
        return head.strip()
    return _strip_closing_paren(_first_clause(text, "; ")).strip()


def importing_results(path=RECORD) -> dict[str, list[int]]:
    """Ledger entry to the numbers of the lemma files that import it, from the proof map's record.

    Returns
    -------
    dict
        ``{"A1": [1, 2, 4, ...], ...}``; an entry no lemma imports is absent.
    """
    record = json.loads(path.read_text(encoding="utf-8"))
    out: dict[str, list[int]] = {}
    for lemma in sorted(record["lemmas"].values(), key=lambda lem: lem["number"]):
        for name in lemma["imports"]:
            out.setdefault(name, []).append(lemma["number"])
    return out


def _paper_markdown(path=PAPER_NB) -> list[tuple[int, str]]:
    """The paper's Markdown cells, each with the number of the section it sits in."""
    cells = json.loads(path.read_text(encoding="utf-8"))["cells"]
    out, section = [], 0
    for cell in cells:
        if cell["cell_type"] != "markdown":
            continue
        text = "".join(cell["source"])
        section += len(re.findall(r"^\(sect-[\w-]+\)=\s*\n## ", text, re.M))
        out.append((section, text))
    return out


def stated_in(name: str, path=PAPER_NB) -> int | None:
    """The number of the paper's section that states the entry: the first that writes it as an
    assumption (``{prf:assumption} A4, ...``) or names it with its statement (``A1: ...``)."""
    pattern = re.compile(rf"\{{prf:assumption\}} {name},|(?<![\w-]){name}: ")
    for section, text in _paper_markdown(path):
        if pattern.search(text):
            return section
    return None


def _used_by(name: str, imports: dict[str, list[int]]) -> str:
    from derivation.axioms import CITED_CONTEXT, SOLVER_LEVEL, STRUCTURAL

    if name in imports:
        return ", ".join(f"[L{n}](#proof-l{n})" for n in imports[name])
    if name in STRUCTURAL:
        return "none: it licenses the sizes and indices"
    if name in CITED_CONTEXT:
        return "none: cited as context"
    if name in SOLVER_LEVEL:
        return "none: it licenses the several-term solver"
    return "none"


def assumption_rows() -> list[list[str]]:
    """The rows of the assumptions table: A0 to A11 and R1 to R3, in order.

    Returns
    -------
    list of list of str
        Id, the statement in one line (:func:`one_line` of the ledger's), the section of the paper
        that states it, the results that import it.
    """
    from generate_proofs import POLYHEDRAL_MARK, _esc

    imports = importing_results()
    rows = []
    for name in sorted(_ledger(), key=_key):
        if name[0] not in ASSUMPTION_KINDS:
            continue
        entry = _ledger()[name]
        section = stated_in(name)
        mark = f" {POLYHEDRAL_MARK}" if re.search(r"\bfacet", entry.statement) else ""
        rows.append([
            f"**{name}**",
            _esc(one_line(entry.statement)) + mark,
            f"Section {section}" if section else "not in the main text",
            _used_by(name, imports),
        ])  # fmt: skip
    return rows


def assumptions_table() -> Md:
    """The assumptions of the derivation, posited (A) and regularity (R), from the ledger.

    Returns
    -------
    Md
        Markdown pipe table: id, statement, the section of the paper that states it, and the
        results that import it, each a link to its proof in Appendix E.
    """
    return Md(md_table(["Id", "Assumption", "Stated in", "Used by"], assumption_rows()))


def cited_rows() -> list[list[str]]:
    """The rows of the second table: I1 to I18 and the formal devices F, in order.

    Returns
    -------
    list of list of str
        Id, the statement in one line, the citation (empty for a formal device), the results.
    """
    from generate_proofs import _esc

    imports = importing_results()
    rows = []
    for name in sorted(_ledger(), key=_key):
        if name[0] in ASSUMPTION_KINDS:
            continue
        entry = _ledger()[name]
        rows.append([
            f"**{name}**",
            _esc(one_line(entry.statement)),
            _esc(entry.citation),
            _used_by(name, imports),
        ])  # fmt: skip
    return rows


def cited_table() -> Md:
    """The results of the literature (I) and the formal devices of the scripts (F), from the ledger.

    Returns
    -------
    Md
        Markdown pipe table: id, statement, citation and the results that import it.
    """
    return Md(md_table(["Id", "Result or device", "Citation", "Used by"], cited_rows()))

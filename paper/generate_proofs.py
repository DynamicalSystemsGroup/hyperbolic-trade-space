"""Appendix B: proofs, step for step with their scripts.

Compiled from ``derivation/proof_map_record.json``, the committed record of the proof-map checker,
and from the lemma scripts and the axiom ledger it points to. Nothing here is typed per proof: the
heading, the steps, their tags, kinds and prose come from the record; the statement of a result is
the ``STATEMENT`` of its script; the wording and citation of a declared axiom come from the ledger
(``derivation/axioms.py``); the line of a step and the line of an import are resolved from the
script's text at build time. The generator only reads ``derivation/``; it never writes there.
"""

from __future__ import annotations

import ast
import hashlib
import html
import json
import re
from functools import cache

from paper_common import Md, md_table
from paper_paths import ROOT

RECORD = ROOT / "derivation" / "proof_map_record.json"
DERIVATION = ROOT / "derivation"
BLOB = "https://github.com/DynamicalSystemsGroup/hyperbolic-trade-space/blob/main/derivation"
CHECK_COMMAND = "uv run python -m derivation.proofmap"
PARTS = (
    ("The fit and its geometry", 1, 11),
    ("The solver for K > 1 and its three levels of guarantee", 12, None),
)  # fmt: skip
"""Name, first and last lemma of each part; the last of the final part is the record's last."""
KIND_ORDER = ("computed", "axiom", "result")
_SPECIAL = re.compile(r"([\\`*_<>\[\]$])")  # the pipe is escaped by the table writer


def _esc(text: str) -> str:
    """Plain text made safe for Markdown (the prose and claims are math-flavoured plain text)."""
    return _SPECIAL.sub(r"\\\1", " ".join(str(text).split()))


_ENTITY = {
    ord(c): f"&{n};"
    for c, n in zip(
        "\\`*_[]$", ("bsol", "grave", "ast", "lowbar", "lsqb", "rsqb", "dollar"), strict=True
    )
}


def _code(text: str) -> str:
    """Inline code that wraps in a narrow column (raw HTML, so the style travels with it)."""
    text = html.escape(" ".join(str(text).split()), quote=False).translate(_ENTITY)
    return f'<code style="white-space:pre-wrap;overflow-wrap:anywhere">{text}</code>'


def _load(path=RECORD) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _heading(number: int, name: str) -> str:
    """The heading of a result, as it appears in the appendix (the test compares with it)."""
    return f"L{number}. {name}"


def result_headings(path=RECORD) -> list[str]:
    """The heading of every result of the record, in the record's order.

    Parameters
    ----------
    path : pathlib.Path, optional
        The record; default ``derivation/proof_map_record.json``.

    Returns
    -------
    list of str
        ``"L<n>. <name>"`` for each result of each lemma file (two for L14).
    """
    return [
        _heading(lem["number"], res["name"])
        for _, lem in _lemmas(_load(path))
        for res in lem["results"]
    ]


def _lemmas(record):
    return sorted(record["lemmas"].items(), key=lambda kv: kv[1]["number"])


@cache
def _source(file: str):
    text = (DERIVATION / file).read_text(encoding="utf-8")
    return text.splitlines(), ast.parse(text)


@cache
def _statement(file: str) -> str:
    """The ``STATEMENT`` constant of a lemma script, read from its syntax tree."""
    _, tree = _source(file)
    for node in tree.body:
        if (
            isinstance(node, ast.Assign)
            and isinstance(node.targets[0], ast.Name)
            and node.targets[0].id == "STATEMENT"
        ):
            return ast.literal_eval(node.value)
    raise KeyError(f"{file} has no STATEMENT")


@cache
def _tag_lines(file: str) -> dict[str, int]:
    """Tag -> the line of code the tag marks (the next code line when the tag stands alone)."""
    lines, _ = _source(file)
    out = {}
    for idx, line in enumerate(lines):
        m = re.search(r"#\s*\[(L\d+\.\d+)\]", line)
        if not m:
            continue
        at = idx
        if line.strip().startswith("#"):
            while at + 1 < len(lines) and lines[at].strip().startswith("#"):
                at += 1
        out[m.group(1)] = at + 1
    return out


@cache
def _import_lines(file: str) -> dict[str, int]:
    """Imported name -> the line of its ``from ... import`` entry (ledger names, proved results)."""
    _, tree = _source(file)
    return {
        alias.asname or alias.name: alias.lineno
        for node in ast.walk(tree)
        if isinstance(node, ast.ImportFrom)
        for alias in node.names
    }


def _link(file: str, line: int) -> str:
    return f"[line {line}]({BLOB}/{file}#L{line})"


def _ledger():
    from derivation.axioms import AXIOMS

    return AXIOMS


def _kind_text(step, lemma, file, owners, results) -> str:
    """The step's kind in words, the declaration compiled from the ledger or the earlier proof."""
    if step["kind"] == "computed":
        return "computed"
    ledger = _ledger()
    parts = []
    if step["kind"] == "axiom":
        for name in step["applies"]:
            entry = ledger[name]
            cite = f" [{_esc(entry.citation)}]" if entry.citation else ""
            where = _import_lines(file).get(name)
            at = f"; declared at {_link(file, where)}" if where else ""
            parts.append(
                f"by declared axiom **{name}** ({entry.tag.lower()}): "
                f"{_esc(entry.statement)}{cite}{at}"
            )
    else:
        for key in step["results"]:
            src_file = lemma["proved_results_imported"][key] + ".py"
            src = results[src_file]
            where = _import_lines(file).get(key)
            at = f"; imported at {_link(file, where)}" if where else ""
            parts.append(
                f"by proved result **L{src['number']}**: {_esc(src['results'][0]['name'])} "
                f"(see [L{src['number']}](#{owners[src_file]}){at})"
            )
    return "<br>".join(parts)


def _anchor(number: int, index: int = 0) -> str:
    """The id of a proof's heading: ``proof-l3``, and ``proof-l14-2`` for a file's second result."""
    return f"proof-l{number}" + (f"-{index + 1}" if index else "")


def _hypotheses(lemma) -> str:
    """The quoted hypotheses of the statement, one line per claim with the symbols that carry it."""
    by_claim: dict[str, list[str]] = {}
    for h in lemma["hypotheses"]:
        by_claim.setdefault(h["claim"], []).append(f"{h['symbol']} ({h['sign']})")
    if not by_claim:
        return "none beyond the declared axioms below."
    return "; ".join(
        f"{_esc(claim)} (carried by the symbols {', '.join(syms)})"
        for claim, syms in by_claim.items()
    )


def _proof(file, lemma, record, res_index, owners, results) -> str:
    res = lemma["results"][res_index]
    n = lemma["number"]
    heading = _heading(n, res["name"])
    steps = {s["tag"]: s for s in lemma["steps"]}
    order = [f"L{n}.{k}" for k in res["steps"]]
    tag_lines = _tag_lines(file)
    rows = []
    for tag in order:
        s = steps[tag]
        rows.append(
            [
                f"**{tag}**",
                _kind_text(s, lemma, file, owners, results),
                _esc(s["prose"]),
                f"{_code(s['code'])}<br>{_link(file, tag_lines[tag])}",
            ]
        )
    shared = len(lemma["results"]) > 1
    statement = _statement(file)
    if shared and res_index > 0:
        stated = (
            f"the file's one statement, given under {_esc(lemma['results'][0]['name'])} above; "
            f"{_esc(res['name'])} is the part of it that this proof's steps establish"
        )
    else:
        stated = _esc(statement)
    exported = ", ".join(lemma["proved_results_exported"]) or "none"
    imported = ", ".join(f"{k} (from {v})" for k, v in lemma["proved_results_imported"].items())
    ledger = (
        f"axioms imported and applied: {', '.join(lemma['imports']) or 'none'}; "
        f"proved results imported: {imported or 'none'}; exported: {exported}; "
        f"{len(order)} steps"
        + (f", in the file's one sequence of {len(lemma['steps'])}" if shared else "")
    )  # fmt: skip
    body = md_table(
        ["Step", "Kind", "Prose of the step", "Line checked (the script's text) and link"], rows
    )
    return (
        f'<a id="{_anchor(n, res_index)}"></a>\n\n#### {heading}\n\n'
        f"**File.** [{file}]({BLOB}/{file}). "
        f"**Statement.** {stated}\n\n"
        f"**Hypotheses** (quoted from the statement): {_hypotheses(lemma)}\n\n"
        f"**Ledger.** {ledger}.\n\n{body}"
    )


def _owners(record) -> dict[str, str]:
    """File -> the anchor of its first result's heading (where a later proof links to)."""
    return {f: _anchor(lem["number"]) for f, lem in _lemmas(record)}


def _part(numbers, path) -> Md:
    record = _load(path)
    results = dict(_lemmas(record))
    owners = _owners(record)
    out = []
    for file, lemma in _lemmas(record):
        if lemma["number"] not in numbers:
            continue
        for i in range(len(lemma["results"])):
            out.append(_proof(file, lemma, record, i, owners, results))
    return Md("\n\n".join(out))


def how_to_read(path=RECORD) -> Md:
    """The rule of the appendix, what the correspondence establishes, and the kinds of step.

    Parameters
    ----------
    path : pathlib.Path, optional
        The record; default ``derivation/proof_map_record.json``.

    Returns
    -------
    Md
        The rule (each proof one file, each step one line, the tag its address), the three kinds
        of step with their counts in the record, and what the checker cannot establish.
    """
    record = _load(path)
    steps = [s for _, lem in _lemmas(record) for s in lem["steps"]]
    counts = {k: sum(s["kind"] == k for s in steps) for k in KIND_ORDER}
    results = sum(len(lem["results"]) for _, lem in _lemmas(record))
    last = max(lem["number"] for lem in record["lemmas"].values())
    parts = "\n".join(f"- {name} (L{lo} to L{hi or last})" for name, lo, hi in PARTS)
    return Md(
        f"Each proof is one file of `derivation/`, and each step of the proof is one line of that "
        f"file. The address of a step is its file and its tag (`L2.1`, `L2.2`, ...), and the tag "
        f"is unique within the file. The record holds {results} results in {len(record['lemmas'])} "
        f"files and {len(steps)} steps. Every step is a line of code, including a step that cites "
        f"a result, and is of one of three kinds:\n\n"
        f"- **computed** ({counts['computed']} steps): SymPy derives the step's condition and the "
        f"line asserts it.\n"
        f"- **by a declared axiom** ({counts['axiom']} steps): the line applies an entry of the "
        f"axiom ledger that the script imported by name; the entry's wording and citation are "
        f"shown beside the step, and the link gives the import line, the declaration's address "
        f"in the proof's own file.\n"
        f"- **by a proved result** ({counts['result']} steps): the line applies the result of an "
        f"earlier proof that the script imported; the step names that proof's statement and "
        f"links to its entry.\n\n"
        f"There is no kind for an argument made only in prose. A step that SymPy cannot derive "
        f"is an explicit hypothesis or an entry of the ledger. Two results may share a file "
        f"(L14 proves Proposition 3 and Corollary 4): each names the same file and owns its own "
        f"steps. The appendix has two parts:\n\n{parts}\n\n"
        f"What the correspondence establishes: every step of the prose has exactly one line of "
        f"code, the lines are in the order of the prose, every computed line passes, and neither "
        f"a line nor a sentence can change without the checker reporting the step. What it "
        f"cannot establish is that a sentence means what its line computes; that reading is the "
        f"human validation, and the tool guarantees there is always exactly one line to read it "
        f"against."
    )


def proof_map(path=RECORD) -> Md:
    """The state of the proof-map record: counts per file and per kind of step.

    Parameters
    ----------
    path : pathlib.Path, optional
        The record; default ``derivation/proof_map_record.json``.

    Returns
    -------
    Md
        One row per result: its heading, file, steps and the kinds of those steps.
    """
    record = _load(path)
    rows = []
    for file, lem in _lemmas(record):
        by_tag = {s["tag"]: s for s in lem["steps"]}
        for res in lem["results"]:
            ks = [by_tag[f"L{lem['number']}.{k}"]["kind"] for k in res["steps"]]
            rows.append(
                [_heading(lem["number"], res["name"]), f"`{file}`", len(ks)]
                + [ks.count(k) for k in KIND_ORDER]
            )
    return Md(
        md_table(["Result", "File", "Steps", "Computed", "By axiom", "By proved result"], rows)
    )


def proofs_fit(path=RECORD) -> Md:
    """The proofs of the fit and its geometry (L1 to L11), step for step.

    Parameters
    ----------
    path : pathlib.Path, optional
        The record; default ``derivation/proof_map_record.json``.

    Returns
    -------
    Md
        Per result: the heading, file, statement, hypotheses, ledger status and the table of
        steps with tag, kind, prose, the script's own line and the link to it.
    """
    return _part(range(PARTS[0][1], PARTS[0][2] + 1), path)


def proofs_solver(path=RECORD) -> Md:
    """The proofs of the solver for K > 1 and its levels of guarantee (L12 to L15), step for step.

    Parameters
    ----------
    path : pathlib.Path, optional
        The record; default ``derivation/proof_map_record.json``.

    Returns
    -------
    Md
        As :func:`proofs_fit`, for L12 to L15 (L14 is Proposition 3 and Corollary 4).
    """
    return _part(range(PARTS[1][1], 10_000), path)


def checker(path=RECORD) -> Md:
    """What the checker verifies, the record's fingerprint, and the commands.

    Parameters
    ----------
    path : pathlib.Path, optional
        The record; default ``derivation/proof_map_record.json``.

    Returns
    -------
    Md
        The record's version, size and SHA-256, the commands, and a row per file with the
        imports the checker compares with the steps.
    """
    record = _load(path)
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    n_steps = sum(len(lem["steps"]) for _, lem in _lemmas(record))
    head = md_table(
        ["Item", "Value"],
        [
            ["Record", "`derivation/proof_map_record.json`"],
            ["Record version", record["version"]],
            ["SHA-256 of the record", f"`{digest}`"],
            ["Lemma files, steps", f"{len(record['lemmas'])}, {n_steps}"],
            ["Ledger entries fingerprinted", len(record["ledger"])],
            ["Check the scripts against the record", f"`{CHECK_COMMAND}`"],
            ["Also run every computed step", f"`{CHECK_COMMAND} --execute`"],
            ["Refresh the record (deliberate; prints what moved)", f"`{CHECK_COMMAND} --update`"],
        ],
    )  # fmt: skip
    rows = [
        [
            f"`{file}`",
            ", ".join(lem["imports"]) or "none",
            ", ".join(lem["proved_results_imported"]) or "none",
            ", ".join(lem["proved_results_exported"]) or "none",
            len(lem["steps"]),
            len(lem["hypotheses"]),
        ]
        for file, lem in _lemmas(record)
    ]
    per_file = md_table(
        ["File", "Ledger entries imported", "Proved results imported", "Exported",
         "Steps", "Signed symbols declared as hypotheses"],
        rows,
    )  # fmt: skip
    return Md(
        "The checker passes only when: every proof names one file; every step of every file "
        "belongs to exactly one proof; the prose steps and the script steps correspond one to "
        "one and in order; every step by a declared axiom applies an entry that exists in the "
        "ledger and that the file imports; the entries a file imports, applies and lists as used "
        "are the same set; a proved result is imported from an earlier proof and applied by a "
        "step; no premise hides in a signed symbol; and the fingerprint of each step (its tag, "
        "prose and line of code) and of each ledger entry equals the record's.\n\n"
        + head + "\n\n" + per_file
    )  # fmt: skip

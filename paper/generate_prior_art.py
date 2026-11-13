"""Appendix G and section 2's family table, compiled from ``prior_art.yaml``.

One source, two views: the register (every entry, grouped by family, with the four fields and the
"why this is not just X" sentence of the nearest neighbours) and section 2's table (the entries
flagged ``section2``, each cell a short extract of the register's sentence).
"""

from __future__ import annotations

import re

import yaml
from paper_common import LINK_STYLE, Md, md_table
from paper_paths import PAPER, ROOT

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


BIB = ROOT / "docs" / "references.bib"
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
# a link that takes the text colour and is underlined reads in light and dark (LINK_STYLE).


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
    """The family table: family with its sources, then three short extracts of the register.

    Parameters
    ----------
    only_section2 : bool, default True
        Section 2's table lists the entries flagged ``section2``; ``False`` lists them all.

    Returns
    -------
    Md
    """
    rows = [
        [
            f"{e['family']}<br><small>{cite(e['cites'])}</small>",
            *(e["short"][f] for f in FIELDS[:3]),
        ]
        for e in entries()
        if e.get("section2") or not only_section2
    ]
    return Md(md_table(["Family and sources", "Produces", "Shares", "Differs"], rows))


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


# ---- Appendix H: the HoroPCA comparison as a tested hypothesis (WP35, amendment 1) --------------

SPIKE_H = ROOT / "work-packages" / "WP35-rounds" / "spike-h"
"""The record of the pre-registered experiment: ``results.json`` (the cells), ``hypothesis.md``
(the hypothesis and its refutation conditions, committed at ``830cf54`` before any table was
generated) and ``readout.md``."""
HYPOTHESIS_COMMIT = "830cf54"
_METHODS = {
    "ours": ("This work", lambda cell: cell["ours_rec"]),
    "pca": ("PCA", lambda cell: cell["pca_pc1_rec"]),
    "horo0.25": ("HoroPCA, R = 0.25", lambda cell: cell["horo_R0.25_k1"]["best_rec"]),
    "horo1": ("HoroPCA, R = 1", lambda cell: cell["horo_R1.0_k1"]["best_rec"]),
}
_HORO = ("horo0.25", "horo1")
RHO = "\u03c1"
"""The spread ratio's symbol, as an escape because it is also what the linter takes for a ``p``."""
RATES = {
    "high": 0.9,
    "low": 0.1,
    "pca_far": 0.2,
    "no_edge": 0.2,
    "rho_high": 2.0,
    "rho_low": 0.5,
    "t_far": 0.9,
}
"""The rates and settings of the refutation conditions of ``hypothesis.md`` (committed at
``830cf54``): the one place they are typed, read by the rules and by the sentences that state
them."""


def hypothesis_record(spike=SPIKE_H) -> dict:
    """The pre-registered experiment's record, as stored (``results.json``)."""
    import json

    return json.loads((spike / "results.json").read_text(encoding="utf-8"))


def _cell_key(key: str) -> tuple[str, float]:
    """``"A/rho0.25"`` to ``("A", 0.25)``; ``"B/t0.9"`` to ``("B", 0.9)``."""
    arm, setting = key.split("/")
    return arm, float(setting.removeprefix("rho").removeprefix("t"))


def refutation_conditions(arm: str, x: float) -> list[tuple[str, str, str, float]]:
    """The pre-registered refutation conditions that apply to a cell, from ``hypothesis.md``.

    Parameters
    ----------
    arm : {"A", "B", "C"}
        The arm of the experiment.
    x : float
        The setting of the cell: the spread ratio rho (arms A and C) or the distance t of the
        planted vector from the all-ones direction (arm B).

    Returns
    -------
    list of (part, method, bound, rate)
        A cell *survives* when, for each entry, the method's recovery rate (recovered tables
        divided by tables) is at least ``rate`` (``bound == "min"``) or at most ``rate``
        (``"max"``). The parts are H1 to H4 of the hypothesis. No entry means the hypothesis makes
        no prediction there (the cell at rho = 1, where two directions tie).
    """
    q = RATES
    rules: list[tuple[str, str, str, float]] = []
    if arm in ("A", "B"):
        rules.append(("H1", "ours", "min", q["high"]))
    if arm == "A" and x >= q["rho_high"]:
        rules += [("H2", m, "min", q["high"]) for m in ("pca", *_HORO)]
    if arm == "A" and x <= q["rho_low"]:
        rules += [("H2", m, "max", q["low"]) for m in ("pca", *_HORO)]
    if arm == "B" and x == q["t_far"]:
        rules += [("H3", "pca", "max", q["pca_far"]), ("H3", "ours", "min", q["high"])]
    if arm == "C":
        rules.append(("H4", "ours", "max", q["no_edge"]))
        if x == q["rho_high"]:
            rules.append(("H4", "pca", "min", q["high"]))
    return rules


def horopca_verdicts(record: dict | None = None) -> list[dict]:
    """The cells of arms A, B and C with their counts and their verdicts.

    Parameters
    ----------
    record : dict, optional
        The parsed ``results.json``; read from ``SPIKE_H`` when omitted.

    Returns
    -------
    list of dict
        One per cell, in the record's order: ``cell``, ``arm``, ``x``, ``n`` (tables), ``rec``
        (recovered tables by method: ``ours``, ``pca``, ``horo0.25``, ``horo1``), ``checks`` (the
        applicable conditions as ``(part, method, bound, rate, held)``), ``parts`` (the parts of the
        hypothesis the cell tests, in order) and ``verdict`` (``"survives"`` or ``"refuted"``).
    """
    record = record or hypothesis_record()
    out = []
    for key, cell in record["cells"].items():
        if key[0] not in "ABC":  # arm D is context, with no refutation rule
            continue
        arm, x = _cell_key(key)
        n = cell["n"]
        rec = {m: get(cell) for m, (_, get) in _METHODS.items()}
        checks = []
        for part, method, bound, rate in refutation_conditions(arm, x):
            share = rec[method] / n
            held = share >= rate if bound == "min" else share <= rate
            checks.append((part, method, bound, rate, held))
        out.append(
            {
                "cell": key,
                "arm": arm,
                "x": x,
                "n": n,
                "rec": rec,
                "checks": checks,
                "parts": list(dict.fromkeys(c[0] for c in checks)),
                "verdict": "survives" if all(c[4] for c in checks) else "refuted",
            }
        )
    return out


def hypothesis_parts(rows: list[dict] | None = None) -> dict[str, str]:
    """The verdict on each part of the hypothesis: it survives when no cell refutes it."""
    rows = rows or horopca_verdicts()
    parts = {}
    for p in ("H1", "H2", "H3", "H4"):
        held = [c[4] for r in rows for c in r["checks"] if c[0] == p]
        parts[p] = "survives" if held and all(held) else "refuted"
    return parts


def _cell_label(row: dict) -> str:
    symbol = "t" if row["arm"] == "B" else RHO
    return f"{row['arm']}, {symbol} = {row['x']:g}"


def _parts_text(parts) -> str:
    return ", ".join(parts)


def horopca_hypothesis_table() -> Md:
    """The results table of Appendix H, generated from ``results.json``.

    One row per cell of arms A, B and C, then one row for the whole hypothesis. The verdict comes
    first (it is computed from the pre-registered refutation conditions applied to the cell, with
    the parts it tests in brackets), then the cell, then the recovered tables out of the tables of
    the cell for this work, for PCA's first component, and for HoroPCA's first direction at the two
    scales that are tested (R = 0.25 and R = 1).

    Returns
    -------
    Md
        A Markdown pipe table of five columns.
    """
    rows = horopca_verdicts()
    out = []
    for r in rows:
        n = r["n"]
        out.append(
            [
                f"{r['verdict']} ({_parts_text(r['parts'])})" if r["parts"] else "no prediction",
                _cell_label(r),
                f"{r['rec']['ours']}/{n}",
                f"{r['rec']['pca']}/{n}",
                ", ".join(f"{r['rec'][m]}/{n}" for m in _HORO),
            ]
        )
    parts = hypothesis_parts(rows)
    refuted = [p for p, v in parts.items() if v == "refuted"]
    out.append(
        [
            "refuted (" + _parts_text(refuted) + ")" if refuted else "survives",
            "All parts",
            "",
            "",
            "",
        ]
    )
    headers = ["Verdict", "Table", "This work", "PCA", "HoroPCA, R = 0.25 and 1"]
    return Md(md_table(headers, out))


def horopca_threshold_sentence() -> Md:
    """The threshold of *recovered* and the chance rates beside it, read from the record."""
    rec = hypothesis_record()
    return Md(
        f"The threshold is |cos| ≥ {rec['threshold']:g}, fixed before the run. Chance reaches it "
        f"with probability {rec['chance_direction']:.3f} for a random direction and "
        f"{rec['chance_simplex']:.3f} for a random point of the simplex, where this work's "
        f"exponents live."
    )


def horopca_verdict_sentence() -> Md:
    """How many pre-registered checks held, and the verdict on each part, from the record."""
    rows = horopca_verdicts()
    checks = [c for r in rows for c in r["checks"]]
    held = sum(c[4] for c in checks)
    parts = hypothesis_parts(rows)
    if all(v == "survives" for v in parts.values()):
        tail = "so every part of the hypothesis survives."
    else:
        bad = [p for p, v in parts.items() if v == "refuted"]
        tail = f"so the hypothesis is refuted in {_parts_text(bad)}."
    return Md(
        f"Of the {len(checks)} checks the refutation conditions set over the {len(rows)} cells, "
        f"{held} hold, {tail}"
    )


def horopca_contrast_sentence() -> Md:
    """The pair of tables that differ only in the edge: this work against PCA at the same spread."""
    rows = {r["cell"]: r for r in horopca_verdicts()}
    a, c = rows["A/rho2.0"], rows["C/rho2.0"]
    n = a["n"]
    assert c["n"] == n

    def change(m):
        return f"{a['rec'][m]} of {n} tables to {c['rec'][m]} of {n}"

    same = a["rec"]["pca"] == c["rec"]["pca"]
    return Md(
        f"At {RHO} = {a['x']:g}, removing the edge changes what this work recovers, from "
        f"{change('ours')}, "
        + (
            f"and does not change what PCA recovers ({a['rec']['pca']} of {n} in both)."
            if same
            else f"and changes what PCA recovers, from {change('pca')}."
        )
    )


def horopca_slab_sentences() -> Md:
    """The two sentences on the smallest-variance component, the part not in the hypothesis.

    The counts are the record's (``pca_last_rec``); the template is checked against them, so a
    record that no longer fits it raises instead of printing a false sentence.
    """
    record = hypothesis_record()
    cells = {k: v for k, v in record["cells"].items() if k[0] in "ABC"}
    slab = {k: v for k, v in cells.items() if v["pca_last_rec"] > 0}
    if set(slab) != {"A/rho0.25", "B/t0.9"} or len({v["pca_last_rec"] for v in slab.values()}) != 1:
        raise ValueError(f"the slab sentence does not fit the record: {sorted(slab)}")
    n = slab["A/rho0.25"]["n"]
    k = slab["A/rho0.25"]["pca_last_rec"]
    words = {9: "nine", 11: "eleven"}
    others = len(cells) - len(slab)
    return Md(
        f"PCA's component of least variance recovers the vector in {k} of {n} tables at "
        f"{RHO} = 0.25 and at t = 0.9, and in none of the other {words.get(others, others)} "
        f"cells. It is outside the hypothesis, because an analyst cannot pick it out without "
        f"knowing the vector."
    )


def horopca_conditions() -> Md:
    """The four parts of the hypothesis with the result that would refute each, from ``RATES``."""
    q = RATES
    return Md(
        f"- **H1** (A, B): this work's rate is at least {q['high']:g}. Refuted by any cell below.\n"
        f"- **H2** (A): the rates of PCA and of HoroPCA are at least {q['high']:g} at "
        f"{RHO} ≥ {q['rho_high']:g} and at most {q['low']:g} at {RHO} ≤ {q['rho_low']:g}. "
        f"Refuted by a rate above {q['low']:g} at {RHO} ≤ {q['rho_low']:g} or below "
        f"{q['high']:g} at {RHO} ≥ {q['rho_high']:g}.\n"
        f"- **H3** (B, t = {q['t_far']:g}): PCA's rate is at most {q['pca_far']:g} and this work's "
        f"at least {q['high']:g}. Refuted by PCA above {q['pca_far']:g}.\n"
        f"- **H4** (C): this work's rate is at most {q['no_edge']:g}, and PCA's at "
        f"{RHO} = {q['rho_high']:g} at least {q['high']:g}. Refuted by either failing."
    )

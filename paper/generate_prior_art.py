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


SPIKE = ROOT / "docs" / "superpowers" / "notes" / "spike-horopca"
"""The record of the HoroPCA spike (WP35): ``results.json`` (HoroPCA, run on the authors' code) and
``tables.npz`` (the log-metrics and exponent vectors it was run on)."""
HOROPCA_SCALE = "1.0"
"""The embedding scale of the table: the farthest point at distance 2 from the origin of the ball
(R = 1); the scales 0.25 and 3 are in ``results.json`` and summarized in a sentence."""
_PLANTED_LABEL = {
    "planted_K1_s0": "planted K = 1 (400 x 4, seed 0)",
    "planted_K2_s7": "planted K = 2 (300 x 3, seed 7)",
    "planted_K3_s0": "planted K = 3 (400 x 4, seed 0)",
    "planted_K3_s4": "planted K = 3 (400 x 4, seed 4)",
    "cubesat_primary": "cubesat primary",
    "cubesat_stock": "cubesat stock",
}


def horopca_rows(spike=SPIKE) -> list[dict]:
    """One record per (table, target) of the spike: PCA on every row, HoroPCA at ``HOROPCA_SCALE``.

    Parameters
    ----------
    spike : pathlib.Path, optional
        The spike folder holding ``results.json`` and ``tables.npz``.

    Returns
    -------
    list of dict
        Keys ``table``, ``target``, ``pca_pc`` (the principal component best aligned with the
        target, from 1), ``pca_cos`` (the absolute cosine), ``pca_span`` (the alignment of the
        span of the first two components with the target), ``horo_cos`` (HoroPCA with one
        direction) and ``horo_span`` (with two), all from the record, none retyped.
    """
    import json

    import numpy as np

    results = json.loads((spike / "results.json").read_text(encoding="utf-8"))
    tables = np.load(spike / "tables.npz")

    def unit(v):
        return v / np.linalg.norm(v)

    def span(basis, w):
        q, _ = np.linalg.qr(basis.T)
        return float(np.linalg.norm(q.T @ unit(w)))

    rows = []
    for name in sorted(results, key=lambda n: (n.startswith("cubesat"), n)):
        result = results[name]
        log_metrics = tables[f"{name}/logM"]
        _, _, vt = np.linalg.svd(log_metrics - log_metrics.mean(0), full_matrices=False)
        if name.startswith("planted"):
            targets = {f"planted t{i + 1}": w for i, w in enumerate(tables[f"{name}/planted"])}
            single = len(targets) == 1
            labels = {k: "planted w" if single else f"planted term&nbsp;{k[-1]}" for k in targets}
        else:
            targets = {"fit K=1 t1": tables[f"{name}/fitK1"][0]}
            targets.update({f"fit K=2 t{i + 1}": w for i, w in enumerate(tables[f"{name}/fitK2"])})
            labels = {
                "fit K=1 t1": "this work, K = 1 term",
                "fit K=2 t1": "this work, K = 2 term&nbsp;1",
                "fit K=2 t2": "this work, K = 2 term&nbsp;2",
            }
        horo = result["horopca"][HOROPCA_SCALE]
        for key, w in targets.items():
            c = np.abs(vt @ unit(w))
            label = f"{_PLANTED_LABEL[name]}"
            if name.startswith("cubesat"):
                label = f"{label} ({len(log_metrics):,} x {log_metrics.shape[1]})"
            rows.append(
                {
                    "table": label,
                    "target": labels[key],
                    "pca_pc": int(c.argmax()) + 1,
                    "pca_cos": float(c.max()),
                    "pca_span": span(vt[:2], w),
                    "horo_cos": horo["k1"]["best"]["scores_unreflected"][key]["best_cos"],
                    "horo_span": horo["k2"]["best"]["scores_unreflected"][key]["span"],
                }
            )
    return rows


def horopca_table() -> Md:
    """The results table of the HoroPCA passage of Appendix G, generated from the spike's record.

    Returns
    -------
    Md
        A Markdown pipe table: for each target exponent vector, the best single principal
        component (its index and absolute cosine) and the alignment of the first two with the
        target, then HoroPCA's one-direction cosine and two-direction alignment, to two decimals.
    """
    out, seen = [], None
    for r in horopca_rows():
        out.append(
            [
                r["table"] if r["table"] != seen else "",
                r["target"],
                f"PC{r['pca_pc']} ({r['pca_cos']:.2f})",
                f"{r['pca_span']:.2f}",
                f"{r['horo_cos']:.2f}",
                f"{r['horo_span']:.2f}",
            ]
        )
        seen = r["table"]
    headers = [
        "Table",
        "Target",
        "PCA: best component (abs. cosine)",
        "PCA: first two, alignment",
        "HoroPCA: one direction, abs. cosine",
        "HoroPCA: two directions, alignment",
    ]
    return Md(md_table(headers, out))

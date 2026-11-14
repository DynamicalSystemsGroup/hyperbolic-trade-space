"""Appendix G.2: what the paper took from where, from the reading pass of its attributions.

``reading_pass.yaml`` holds the fifty-six rows of the reading pass
(``work-packages/WP10-reading-pass.md``, read-only here): the sentence as it was read, the key, the
place read, the verdict and the reason, each verbatim, plus what the paper now does with the
sentence (``status`` and ``now``). The file is the record and is made from the Markdown table by
``uv run python paper/generate_reading_pass.py`` (which keeps the ``status`` and ``now`` already in
it); a test compares the two. The table of the appendix shows only what a reader needs to check a
citation: what we say (the paper's own sentence), the source, the place in it with the source's own
link. The record's verdict, reason, disposition and fetch addresses are not shown.
"""

# ruff: noqa: E501
from __future__ import annotations

import re
import sys

import yaml
from generate_prior_art import BIB, cite
from generate_proofs import _esc
from paper_common import Md, md_table
from paper_paths import PAPER, ROOT

SOURCE = PAPER / "reading_pass.yaml"
MARKDOWN = ROOT / "work-packages" / "WP10-reading-pass.md"
VERDICTS = (
    "supported",
    "partly supported",
    "not found",
    "not accessible",
    "accessible (own work)",
)
STATUS = {
    "kept": "kept as read",
    "reworded": "reworded to what was read",
    "confirm": "to be confirmed by the author",
    "supervisor": "listed for the supervisor, unchanged",
}
_ROW = re.compile(
    r"^\| (?P<n>\d+) \| (?P<sentence>.*?) \| `(?P<key>[^`]+)` \| (?P<read>.*?) \| "
    r"(?P<verdict>" + "|".join(re.escape(v) for v in VERDICTS) + r") \| (?P<why>.*) \|$"
)
FIELDS = ("n", "sentence", "key", "read", "verdict", "why")


def markdown_rows(path=MARKDOWN) -> list[dict]:
    """The rows of the Markdown table of the reading pass, fields verbatim."""
    rows = []
    for line in path.read_text(encoding="utf-8").splitlines():
        m = _ROW.match(line)
        if m:
            rows.append({k: (int(v) if k == "n" else v) for k, v in m.groupdict().items()})
    return rows


def rows(path=SOURCE) -> list[dict]:
    """The rows of ``reading_pass.yaml``."""
    return yaml.safe_load(path.read_text(encoding="utf-8"))["rows"]


def convert(md=MARKDOWN, out=SOURCE) -> None:
    """Write ``reading_pass.yaml`` from the Markdown table, keeping the annotations there."""
    old = {r["n"]: r for r in rows(out)} if out.exists() else {}
    merged = []
    for r in markdown_rows(md):
        prev = old.get(r["n"], {})
        merged.append({**r, "status": prev.get("status", ""), "now": prev.get("now", "")})
    head = (
        "# Rows of the reading pass (work-packages/WP10-reading-pass.md), verbatim, with what the\n"
        "# paper now does with each sentence. Made by paper/generate_reading_pass.py.\n"
    )
    out.write_text(
        head + yaml.safe_dump({"rows": merged}, sort_keys=False, allow_unicode=True, width=100),
        encoding="utf-8",
    )


REMOVED = (4, 14, 15)
"""Rows whose citation the paper no longer makes (their ``now`` says so): nothing is taken from the
source for a sentence, so the table has no row for them; the record keeps them."""

_DEA = "Data envelopment analysis (DEA) evaluates each unit against the observed data by mathematical programming."
_FRONTIER = (
    "Frontier production functions are estimated by programming, corrected ordinary least squares "
    "or maximum likelihood, and stochastic frontiers with one-sided error, as reviewed by Battese (1992)."
)
_LOGRATIO = "The chart is in the spirit of log-ratio coordinates for compositional data."
_TRADE = "Tradespace exploration is value-focused broad exploration of design alternatives."
SAID = {
    1: "Decision analysis seeks clear conversation with the decision-maker.",
    2: "Decision analysis seeks responsible choice among conflicting objectives.",
    3: "A trade study is a document: a grid, a table, a ranking by weighted criteria; surveys compare them.",
    5: "The weights are human judgments, susceptible to bias in trade studies.",
    6: "The weights are human judgments, susceptible to bias in trade studies.",
    7: "Systems engineering is moving to model-based practice.",
    8: "Systems engineering is moving from document-based practice.",
    9: "PCA reduces dimensionality and increases interpretability while minimizing information loss.",
    10: "Pareto methods find the members of a nondominated set by scalarization, for example the weighting method.",
    11: "Pareto methods find the members of a nondominated set by scalarization, for example the weighting method.",
    12: "Evolutionary algorithms generate nondominated sets.",
    13: "Evolutionary algorithms generate nondominated sets.",
    16: "DEA scores each unit against the data by mathematical programming.",
    17: "DEA scores each unit with weights obtained from the data rather than set in advance.",
    18: "A super-efficiency variant of DEA ranks efficient units against a reference technology spanned by all other units.",
    19: "DEA has Malmquist productivity indices across data sets.",
    20: _DEA,
    21: _DEA,
    22: "DEA has variants for scale and returns to scale.",
    23: "The weighted geometric mean with exponents summing to one has the constant-returns Cobb-Douglas form.",
    24: "Reading V as the factor that scales a design to the boundary is our distance-function reading, after Shephard's characterization of a technology by its distance function.",
    25: "Reading V as the factor that scales a design to the boundary is our distance-function reading, after Shephard's characterization of a technology by its distance function.",
    26: "Reading V as the factor that scales a design to the boundary is our distance-function reading, after Shephard's characterization of a technology by its distance function.",
    27: "Frontier estimation by programming, corrected least squares and one-sided error is the family of one-sided fits, reviewed by Battese (1992).",
    28: _FRONTIER,
    29: _FRONTIER,
    30: _FRONTIER,
    31: _FRONTIER,
    32: _FRONTIER,
    33: "PCA finds uncorrelated components that successively maximize variance, reducing dimensionality while keeping interpretability.",
    34: _LOGRATIO,
    35: "Compositional data are analysed by PCA and by isometric logratio transformations.",
    36: _LOGRATIO,
    37: "The model class and refit scheme come from geometric programming and max-affine fitting.",
    38: "Aircraft design is posed as geometric programs with fits compatible with them.",
    39: "The model class and refit scheme come from geometric programming and max-affine fitting, here with softmax-affine fits compatible with geometric programming.",
    40: "The model class and refit scheme come from geometric programming and max-affine fitting, here with convex piecewise-linear fits.",
    41: "The sparsity option is shared with reweighted ℓ₁ sparsity.",
    42: "The soft maximum is an entropic risk functional.",
    43: "Kernel PCA is the feature-engineering kin of the kernel direction.",
    44: "HoroPCA extends the components of PCA to hyperbolic space with horospherical projections, maximizing a variance.",
    45: _TRADE,
    46: "Tradespace exploration has user-guided samplers and linked visualization with the Pareto frontier displayed.",
    47: _TRADE,
    48: _TRADE,
    49: "Tradespace exploration has been applied to resilient systems.",
    50: "Decision analysis distinguishes the normative from the descriptive.",
    51: "Decision analysis covers multiple-objective preferences and value trade-offs.",
    52: "Weighted-criteria comparison methods (Pugh, AHP, Kepner-Tregoe) elicit the weights.",
    53: "A decision-management framework rests on decision theory and cost analysis.",
    54: "Model-based systems engineering is centred on the system model as the sole source of truth.",
    55: "A systematic review of the evidence for the benefits of model-based systems engineering opens from document-based practice.",
    56: "The process is modelled on the harness described there, whose deterministic checks and named human approver are the verification mechanism this paper inherits.",
}
"""The paper's sentence at each citation, as it stands now (not the record's ``sentence`` or ``now``)."""
WHERE = {
    1: "abstract, via Crossref",
    2: "publisher description; abstract via Crossref",
    3: "whole (a one-page poster)",
    5: "abstract, via Crossref",
    6: "article body",
    7: "abstract, via Crossref",
    8: "abstract, via Crossref",
    9: "abstract, via Crossref",
    10: "author's overview and contents page",
    11: "contents only (the publisher page is gated)",
    12: "abstract and introduction (p. 1)",
    13: "abstract (p. 1)",
    16: "title only (abstract not accessible)",
    17: "abstract, via Crossref",
    18: "abstract, via Crossref",
    19: "abstract",
    20: "abstract (repository record)",
    21: "abstract (repository record)",
    22: "abstract, via Crossref",
    23: "title only (the page did not load)",
    24: "publisher description",
    25: "chapter title (no abstract; publisher gated)",
    26: "title only (no abstract; publisher gated)",
    27: "body: deterministic frontiers, corrected OLS (footnote 2), stochastic frontiers",
    28: "as reviewed in Battese 1992; the primary is not online",
    29: "as reviewed in Battese 1992; no abstract",
    30: "as reviewed in Battese 1992",
    31: "as reviewed in Battese 1992",
    32: "as reviewed in Battese 1992; no abstract",
    33: "abstract, via Crossref",
    34: "title only (no abstract; publisher gated)",
    35: "book record only",
    36: "title only (no abstract; publisher gated)",
    37: "abstract; section 5.3 (generalized posynomials); section 8 (approximation and fitting)",
    38: "abstract and text",
    39: "abstract (full text not obtained)",
    40: "abstract and section 1",
    41: "abstract",
    42: "introduction, equations (1)-(2)",
    43: "abstract, via Crossref",
    44: "abstract",
    45: "abstract, via Crossref",
    46: "abstract, via Crossref",
    47: "abstract, via Semantic Scholar",
    48: "abstract",
    49: "abstract, via Semantic Scholar",
    50: "abstract, via Crossref",
    51: "publisher description; abstract via Crossref",
    52: "whole (a one-page poster)",
    53: "publisher description",
    54: "abstract, via Crossref",
    55: "abstract, via Crossref",
    56: "abstract, via Crossref",
}
"""Where in the source the place read lies, for a reader to open; the fetch addresses of the reading
(the Crossref and Semantic Scholar API calls) stay in ``reading_pass.yaml`` as the record of how it was read."""


def _left(text: str, width: int, small: bool = False) -> str:
    """A cell of running text: left aligned, wrapping inside a minimum width (long URLs break)."""
    size = ";font-size:0.85em" if small else ""
    return (
        f'<div style="text-align:left;overflow-wrap:anywhere;min-width:{width}em{size}">'
        f"{text}</div>"
    )


def _bib_link(key: str, path=BIB) -> tuple[str, str]:
    """The source's own link: its DOI where the bibliography has one, else its address."""
    text = path.read_text(encoding="utf-8")
    entry = re.search(r"^@\w+\{" + re.escape(key) + r",(.*?)^\}", text, re.S | re.M).group(1)
    doi = re.search(r"\bdoi\s*=\s*\{([^}]*)\}", entry)
    if doi:
        return f"https://doi.org/{doi.group(1)}", f"doi:{doi.group(1)}"
    url = re.search(r"\burl\s*=\s*\{([^}]*)\}", entry).group(1)
    return url, re.sub(r"^https?://(www\.)?", "", url).split("/")[0]


def citing_rows(rs=None) -> list[dict]:
    """One row per citing sentence still in the paper: what we say, the source, where in it.

    ``say`` is the paper's own sentence at the citation (``SAID``); ``place`` is where in the source
    it was read (``WHERE``), with the source's own link.
    """
    rs = rows() if rs is None else rs
    return [
        {"n": r["n"], "say": SAID[r["n"]], "key": r["key"], "place": WHERE[r["n"]]}
        for r in rs
        if r["n"] not in REMOVED
    ]


def _place_cell(key: str, place: str) -> str:
    href, label = _bib_link(key)
    return _left(f'{_esc(place)}; <a href="{href}">{_esc(label)}</a>', 18, small=True)


def reading_pass_table() -> Md:
    """What the paper took from where: the sentence, the source, the place in it.

    Returns
    -------
    Md
        One row per citing sentence still in the paper, for the reader to check against the source.
    """
    return Md(
        md_table(
            ["What we say", "Source", "Where in it"],
            [
                [
                    _left(_esc(r["say"]), 18),
                    cite([r["key"]], "../#"),
                    _place_cell(r["key"], r["place"]),
                ]
                for r in citing_rows()
            ],
        )
    )


if __name__ == "__main__":
    convert()
    print(f"wrote {SOURCE} ({len(rows())} rows)", file=sys.stderr)

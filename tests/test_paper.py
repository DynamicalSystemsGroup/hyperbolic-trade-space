"""WP10 structural checks of the paper: the shells, the generators and the register of prior art.

Offline and fast. What is checked now is what exists now: the build configuration, the notebooks'
cell structure (one call per code cell), the appendices A to H with their jobs and tiers, the
tables compiled from their sources (the glossary, the abstraction-gaps ledger, the register of
prior art, the lock file), and the register's phrase lists. Requirements that depend on the paper's
prose (word budgets per section, the register phrase for each object, every appendix cited from the
body) are written as hooks that skip while a section is still a shell and run when the prose lands.

Two checks are gated because they are slow or need the network: executing the notebooks from a
clean kernel (``PAPER_EXECUTE=1``) and building the HTML site (``PAPER_BUILD=1``).
"""

from __future__ import annotations

import ast
import json
import os
import re
import shutil
import subprocess
import sys
import tomllib
from pathlib import Path

import nbformat
import numpy as np
import pytest
import yaml
from _env import ENV_VAR, REFERENCE_FILE, VALUES_FILE, exact_only, listed

# The paper's tests run in the paper's workflow, not in the software's gate (tests/conftest.py).
pytestmark = pytest.mark.paper

# GENERAL RULE (the driver's, WP10): every test that compares a committed notebook output with a
# re-run goes through the environment of record (tests/_env.py, paper/environment_values.toml):
# exact only there (``_current``), and elsewhere the reproducible content, which is the text with
# its numbers within the tolerance stated for it. Every generated table of the paper and its
# appendices is checked BEFORE it is committed for quantities that depend on ties at the exact
# maximum (termination statuses, margins near 1e-16, errors on tied terms), on step counts of an
# adaptive solver (settling or slew times, saturated fractions, iteration counts) or on hashes of
# floats: such a quantity is either not printed or listed as exact-only in
# environment_values.toml with its reason. The gated test
# test_generated_tables_do_not_move_under_platform_perturbation (PAPER_EXECUTE=1) flags what moves
# when the BLAS thread count and the restart order change; the audit table is in the comment of
# paper/environment_values.toml.

ROOT = Path(__file__).resolve().parent.parent
PAPER = ROOT / "paper"
if str(PAPER) not in sys.path:
    sys.path.insert(0, str(PAPER))

import generate_gaps  # noqa: E402
import generate_model  # noqa: E402
import generate_prior_art  # noqa: E402
import generate_proofs  # noqa: E402
import generate_register  # noqa: E402
import generate_repro  # noqa: E402

NOTES = ROOT / "docs" / "superpowers" / "notes"
PAPER_NB = PAPER / "paper.ipynb"
SUPPORT_NB = PAPER / "supporting_material.ipynb"
SHELL = "Shell."
STALE = "re-run `uv run python paper/execute_notebooks.py` to refresh the committed outputs"

SECTIONS = [
    "The decision problem",
    "Prior art",
    "Preliminaries and notation",
    "Definitions",
    "Methods",
    "Results",
    "Case construction",
    "Case analysis",
    "Discussion",
    "Future work",
    # Not plain "Acknowledgments": the site lifts a heading of that name out of the flow and prints
    # it after the bibliography; this heading keeps it before the references (BROWSER_NOTES).
    "AI acknowledgement and Reproducibility",
    "Works cited",
]
APPENDICES = {
    "A": "Register of prior art",
    "B": "Extended results: what the method found in the table",
    "C": "HoroPCA beside this work: a tested hypothesis",
    "D": "Notation and terms",
    "E": "Proofs, step for step with their scripts",
    "F": "The case's model: how the table of metrics came to be",
    "G": "Assumptions, limitations and open questions",
    "H": "Computational reproducibility",
}
"""The appendices, lettered in the order the paper first mentions each (WP57e, the rule of call 4
in ``WP57-decisions.md``)."""
TIERS = ("**Main text keeps:**", "**This appendix carries:**", "**The repository keeps:**")
# Appendices whose generated content waits for another package's deliverable (stated in the report).
AWAITING_RECORD: set[str] = set()
NEAREST = {
    "pareto", "dea", "pca", "logratio", "gp-maxaffine", "production-distance", "tradespace",
    "frontier-estimation",
}  # fmt: skip
# The families of the outline (v1 baseline, v2): each has an entry in the register (R-9).
OUTLINE_FAMILIES = {
    "pareto", "dea", "production-distance", "frontier-estimation", "pca", "logratio",
    "gp-maxaffine", "kernel-pca", "horopca", "entropic-risk", "tradespace", "decision-analysis",
    "mbse",
}  # fmt: skip
PRIOR_FIELDS = ("does", "shares", "differs", "cites")
WORDS_BANNED_IN_PRIOR_ART = re.compile(r"\b(novel|first|new)\b", re.I)
# Fitted vocabulary that Appendix F must not contain; the system vocabulary D must not contain.
FITTED_WORDS = re.compile(
    r"\b(temperature|tau|frac_above_?|loss_|n_eff_?|reach|log V|gamma|radius|status)\b", re.I
)
SYSTEM_WORDS = re.compile(
    r"(Declared (min|max)|Ordered levels|slew_deg|t_end_s|max_step_s|removed in this order|"
    r"adcs_designs|panel_span_m|battery_wh)"
)


# ---- helpers -----------------------------------------------------------------------------------


def _nb(path):
    return nbformat.read(path, as_version=4)


def _src(cell) -> str:
    return cell.source if isinstance(cell.source, str) else "".join(cell.source)


def _out_text(cell) -> str:
    """The Markdown (or plain text) of a cell's committed outputs."""
    chunks = []
    for out in cell.get("outputs", []):
        data = out.get("data", {})
        chunks.append(data.get("text/markdown") or data.get("text/plain") or "")
    return "".join(chunks)


def _code_cells(nb):
    return [c for c in nb.cells if c.cell_type == "code"]


_TARGET = re.compile(r"^\((?P<label>[\w-]+)\)=\n", re.M)
_ROLE = re.compile(r"\{(?P<role>ref|numref)\}`(?P<title>[^`<]*?)\s*<(?P<label>[^>`]+)>`")


def _unlabel(text: str) -> str:
    """The text without its target-label lines, ``(label)=``, which print nothing."""
    return _TARGET.sub("", text)


def _rendered(text: str) -> str:
    """The text as the reader sees it: target lines gone, each cross-reference role as its title."""
    return _ROLE.sub(lambda m: m.group("title").replace("%s", "0"), _unlabel(text))


def _markdown(nb) -> str:
    return "\n".join(_src(c) for c in nb.cells if c.cell_type == "markdown")


def _headings(nb, level="##") -> list[str]:
    out = []
    for c in nb.cells:
        if c.cell_type != "markdown":
            continue
        for line in _src(c).splitlines():
            if re.match(rf"^{level}\s+[^#]", line):
                out.append(line[len(level) :].strip())
    return out


def _bib_keys() -> set[str]:
    return set(
        re.findall(
            r"^@\w+\{([^,\s]+),",
            (ROOT / "docs" / "references.bib").read_text(encoding="utf-8"),
            re.M,
        )
    )


def _appendix_cells(nb):
    """Map letter to the cells from its heading up to the next appendix heading."""
    sections, current = {}, None
    for c in nb.cells:
        m = (
            re.match(r"^## Appendix ([A-H])\. ", _unlabel(_src(c)))
            if c.cell_type == "markdown"
            else None
        )
        if m:
            current = m.group(1)
            sections[current] = []
        if current:
            sections[current].append(c)
    return sections


def _tables(text: str) -> set[str]:
    """The Markdown pipe tables of a text, each as one normalized string."""
    out, block = set(), []
    for line in [*text.splitlines(), ""]:
        if line.startswith("|"):
            block.append(line.strip())
        elif block:
            out.add("\n".join(block))
            block = []
    return out


def _body_has_prose() -> bool:
    """True once every section of the paper's body is written (no shell marker is left)."""
    return SHELL not in _markdown(_nb(PAPER_NB))


needs_prose = pytest.mark.skipif(
    not _body_has_prose(), reason="the main text is still a shell; the check runs with the prose"
)


# ---- files and configuration -------------------------------------------------------------------


def test_files_exist():
    for name in (
        "myst.yml", "paper.ipynb", "supporting_material.ipynb", "prior_art.yaml", "paper_paths.py",
        "paper_common.py", "execute_notebooks.py", "generate_register.py", "generate_proofs.py",
        "generate_model.py", "generate_results.py", "generate_gaps.py", "generate_repro.py",
        "generate_prior_art.py", ".gitignore",
    ):  # fmt: skip
        assert (PAPER / name).is_file(), name


def test_myst_config_parses_and_is_modelled_on_the_scipy_build():
    cfg = yaml.safe_load((PAPER / "myst.yml").read_text(encoding="utf-8"))
    proj = cfg["project"]
    assert cfg["version"] == 1
    assert proj["index"] == "paper.ipynb"
    assert [t["file"] for t in proj["toc"]] == ["paper.ipynb", "supporting_material.ipynb"]
    assert proj["title"].startswith("Scaling Decision Analysis with Hyperbolic Trade Space")
    assert proj["authors"][0]["name"] == "Michael Zargham"
    assert proj["authors"][0]["orcid"] == "0000-0001-5279-690X"
    assert proj["abbreviations"] and proj["keywords"]
    assert "extends" not in cfg  # standalone, not extending a shared file
    bib = (PAPER / proj["bibliography"][0]).resolve()
    assert bib == (ROOT / "docs" / "references.bib").resolve()


TOOL_NAMES = ("scikit-learn", "sklearn", "numpy", "scipy", "python", "sympy", "cvxpy", "pandas",
              "matplotlib", "marimo", "jupyter", "mystmd", "docker", "uv")  # fmt: skip


def test_keywords_name_no_tool_or_library():
    """The supervisor's rule: a keyword is a subject, not a tool (WP10, reading of the abstract)."""
    keywords = yaml.safe_load((PAPER / "myst.yml").read_text(encoding="utf-8"))["project"][
        "keywords"
    ]
    assert keywords == [
        "decision analysis", "trade studies", "trade space", "posynomial", "geometric programming",
        "unsupervised learning", "model-based systems engineering", "open source software",
    ]  # fmt: skip
    for k in keywords:
        assert not set(re.split(r"[\s-]+", k.lower())) & set(TOOL_NAMES), k


def test_abstract_and_section_5_say_the_one_term_fit_is_a_geometric_program():
    """The abstract is the supervisor's text of 2026-11-14 (WP11-decisions.md); it says the monomial
    case is a convex optimization problem and the posynomial case is compatible with generalized
    geometric programming, and that the model is the level sets of a posynomial function of the
    metrics. Section 5 keeps one cited sentence that the invariant is a generalized posynomial; one
    term is a geometric program (convex after the log change of variables, L4.14 to L4.24); the
    several-term fit alternates weights with one program for all terms (R-39: no design is assigned
    to a cell in the fit). Nothing says the several-term fit is itself a convex program or a GGP.
    The abstract does not say it, and says nothing of assigning designs to cells. The old
    abstract's phrases that the supervisor replaced stay gone. WP24 (A7): the first use of "monomial
    term" is glossed in the body as a product of powers of the metrics, and the old word is gone."""
    nb = _nb(PAPER_NB)
    fm = yaml.safe_load(_src(nb.cells[0]).split("---")[1])["abstract"]
    flat = " ".join(fm.split())
    assert "generalized posynomial" not in flat
    for phrase in (
        "the level sets of a posynomial function of the metrics",
        "The monomial case is a convex optimization problem",
        "the posynomial case is compatible with generalized geometric programming",
        "Like PCA, HTS is an unsupervised learning method",
        "a monomial term in n metrics characterizes an n-lemma",
        "HTS is implemented with a scikit-learn-compatible API",
        "Trade-offs trace piecewise hyperbolic frontiers",
        "Pareto improvements increase energy",
        "a design that maximizes energy is Pareto-efficient",
    ):
        assert phrase in flat, phrase  # fmt: skip
    for gone in (  # cut from the abstract at the supervisor's direction (the body keeps them)
        "chains with PCA",
        "nondominated set stops shortlisting",
        "Derived statements point",
        "descent is derived",
        "one such program per facet",
        "assigning",
        "exchange rate",
        # the old abstract's phrases the supervisor's text of 2026-11-14 replaced
        "We explain tensions",
        "soft support",
        "reversible chart",
        "any kernel that keeps that compatibility",
        "unsupervised feature engineering",
        "negative curvature",
        "fitted posynomial reference surface",
        "is solved directly",
    ):
        assert gone not in flat, gone  # fmt: skip
    assert "several-term" not in flat and "several facets" not in flat
    assert "facet" not in flat.lower()
    methods = _section("Methods")
    for phrase in (
        "geometric program",
        "generalized posynomial",
        "{ref}`Appendix E, L4 <appendix-e>`",
        "one program for all terms",
        "boyd2007tutorial",
    ):
        assert phrase in methods, phrase  # fmt: skip
    assert methods.count("generalized posynomial") == 1  # one cited sentence, nowhere else
    cited = "generalized posynomial, the term maximum at the default $\\kappa=\\infty$"
    assert f"{cited} [@boyd2007tutorial]" in methods
    assert "geometric program" in _section("The decision problem")
    assert "GGP" not in flat  # the abstract spells it out and never abbreviates it
    for text in (flat, methods, _section("The decision problem")):
        assert "several facets is a" not in text
        assert not re.search(r"several[^.;]*(transform|convex program)", text)
    for text in (methods, _section("The decision problem")):
        assert "GGP" not in text


def test_one_name_for_the_surface_and_the_data_is_what_is_modelled():
    """WP10 Amendment 4, R-33 and R-34, kept for the body; the abstract is the supervisor's text of
    2026-11-14 (WP11-decisions.md). The Definition names the posynomial, the invariant as its root
    and the surface as the sum equal to one, citing L10; "generalized posynomial" is in no Markdown
    cell of the paper but the Methods one (reports of a source, the family table and Appendix A, are
    generated output and stay). The surface is a model of the data underlying the table, whose
    reading is a view. The abstract names the model by what it is: the level sets of a posynomial
    function of the metrics, and says nothing of "the table" or of a reference surface."""
    nb = _nb(PAPER_NB)
    definition = next(c for c in nb.cells if "prf:definition} Posynomial" in _src(c))
    text = " ".join(_src(definition).split())
    assert "a posynomial, a sum of monomials" in text
    assert (
        "{ref}`Appendix E, L10 <appendix-e>`" in text
    )  # the proof pointer (R-2: no forward reference)
    assert "is the $1/\\kappa$ power of a posynomial" in text
    assert "generalized" not in text
    assert "is the level set $V=1$ of the fit" in " ".join(_markdown(nb).split())  # the surface
    fm = " ".join(yaml.safe_load(_src(nb.cells[0]).split("---")[1])["abstract"].split())
    assert "the level sets of a posynomial function of the metrics" in fm
    assert "a dataset of designs and measurements of their performance" in fm
    for gone in ("reference surface", "the table", "its reading are views", "soft support"):
        assert gone not in fm, gone  # the old abstract's phrases, replaced
    body = " ".join(_markdown(nb).split())
    for phrase in ("model of the table", "models the table", "surface models the table"):
        assert phrase not in body and phrase not in fm, phrase
    assert (
        "fitted to the data underlying the table" in body
    )  # the body keeps it; the abstract does not
    others = [
        _src(c) for c in nb.cells
        if c.cell_type == "markdown" and "generalized posynomial" in _src(c)
        and ":label: thm-soft" not in _src(c)  # L16: the derivation's statement
    ]  # fmt: skip
    assert len(others) == 1
    assert "$V_K$ is a generalized posynomial" in others[0] and "@boyd2007tutorial" in others[0]


def test_the_case_is_described_as_power_mass_and_attitude_control():
    """The case couples power, mass and attitude control (cubesat.sysml), not attitude alone, in
    the body. The abstract is the supervisor's text of 2026-11-14 (WP11-decisions.md): its case
    sentence says a cubesat design optimization problem (its qualification cut at his review of
    2026-11-15), scored on thirteen metrics by a simulation study, one sentence for the case."""
    nb = _nb(PAPER_NB)
    fm = " ".join(yaml.safe_load(_src(nb.cells[0]).split("---")[1])["abstract"].split())
    assert "The worked example is a cubesat design optimization problem." in fm
    assert "a simulation study scores each design on thirteen metrics" in fm
    assert len(re.findall(r"cubesat", fm)) == 1  # one sentence: the case
    for count in ("ten attributes", "controller-gain"):  # PM-BRIEF ruling 1: terms may be counted
        assert count not in fm, count  # fmt: skip
    prose = _markdown(nb) + _markdown(_nb(SUPPORT_NB))
    assert "attitude determination and control system" not in prose
    assert "cubesats whose power, mass and attitude control are coupled" in _section(
        "Case construction"
    )
    assert "app-F-job" not in {c.id for c in _nb(SUPPORT_NB).cells}  # WP57c: C opens on F.1
    cell = next(c for c in _code_cells(nb) if c.id == "num-attributes")
    out = _out_text(cell)
    for group in ("controls (", "power and energy (", "mass (total mass)"):
        assert group in out, group


def test_generated_sentences_name_the_subsystems_from_the_one_mapping():
    """Subsystems come from ``CaseSpec.subsystems``; mass enters only in the baseline regime."""
    import case

    spec = case.CUBESAT
    nb = _nb(PAPER_NB)
    k1 = _out_text(next(c for c in _code_cells(nb) if c.id == "num-k1"))
    reg = _out_text(next(c for c in _code_cells(nb) if c.id == "num-regimes"))
    assert "across controls, power and energy, plus cost:" in k1
    assert "the primary set lies inside the baseline set, which adds total mass" in reg
    assert "The baseline set spans controls, power and energy, mass, plus cost" in reg
    assert "mass enters only in the baseline regime" in reg
    assert spec.subsystems["total_mass_kg"] == "mass"


def test_no_pdf_export_block():
    text = (PAPER / "myst.yml").read_text(encoding="utf-8")
    cfg = yaml.safe_load(text)
    assert "exports" not in cfg["project"]
    assert "typst" not in text.lower()
    assert "template: https://github.com/curvenote-templates" not in text


def test_build_output_is_ignored():
    assert "_build/" in (PAPER / ".gitignore").read_text(encoding="utf-8")


def test_notebooks_are_valid_and_use_the_project_kernel():
    for path in (PAPER_NB, SUPPORT_NB):
        nb = _nb(path)
        nbformat.validate(nb)
        assert nb.metadata["kernelspec"]["name"] == "python3"
        ids = [c.id for c in nb.cells]
        assert len(ids) == len(set(ids)), f"duplicate cell ids in {path.name}"


def test_cell_ids_are_unique_across_the_two_notebooks():
    ids = [c.id for p in (PAPER_NB, SUPPORT_NB) for c in _nb(p).cells]
    assert len(ids) == len(set(ids))


def test_no_ai_attribution_in_paper_files():
    pattern = re.compile(r"co-authored-by|generated (with|by)\b", re.I)
    for path in PAPER.rglob("*"):  # the container directory is the container work package's
        if path.is_file() and not {"_build", "container"} & set(path.parts) and path.suffix in {
            ".py", ".yml", ".yaml", ".ipynb", ".md",
        }:  # fmt: skip
            assert not pattern.search(path.read_text(encoding="utf-8")), path


# ---- section structure of the paper ------------------------------------------------------------


def test_section_headings_in_order():
    """R-1: the section order is the amendment's; the headers are the skim."""
    assert _headings(_nb(PAPER_NB)) == SECTIONS


def test_front_matter_has_title_and_abstract():
    first = _src(_nb(PAPER_NB).cells[0])
    fm = yaml.safe_load(first.split("---")[1])
    assert fm["title"].startswith("Scaling Decision Analysis with Hyperbolic Trade Space")
    assert fm["abstract"].strip()


def test_no_section_is_preliminary_or_a_remark():
    """WP54 R-1: eleven numbered sections and Works cited; none preliminary, none a remark."""
    heads = [h for h in _headings(_nb(PAPER_NB)) if h in SECTIONS or h.startswith("Search")]
    assert heads == SECTIONS
    assert len(SECTIONS) == 12 and SECTIONS[-1] == "Works cited"
    assert not any(re.search(r"preliminary|remark", h, re.I) for h in SECTIONS)


def test_separation_of_concerns_no_user_guide_headers():
    """R-21: install, API and how-to-run sections stay on the docsite."""
    for h in _headings(_nb(PAPER_NB)):
        assert not re.search(r"\b(install|installation|api|getting started)\b", h, re.I), h


def test_body_names_no_tooling_versions():
    """R-12: the body names no tooling versions."""
    body = re.sub(
        r"\[@[^\]]*\]", "", _markdown(_nb(PAPER_NB))
    )  # a locator, Section 4.2.3, is no version
    assert not re.search(r"\b\d+\.\d+\.\d+\b", body)


# ---- the word count: what renders, generated sentences included (G-1) ------------------------

_OPTION_LINE = re.compile(r"^:[\w-]+:.*$", re.M)  # a directive option: it prints nothing
_FENCE = re.compile(r"^:{3,}\{(?P<name>[\w:-]+)\}[ \t]*(?P<arg>.*)$", re.M)
_DISPLAY_MATH = re.compile(r"\$\$.*?\$\$", re.S)
_MATH_BLOCK = re.compile(
    r"^:{3,}\{math\}\n.*?\n:{3,}[ \t]*$", re.S | re.M
)  # a labelled display (WP55)
_CITES = re.compile(r"\[(@[^\]]+)\]")
_PRF_REF = re.compile(r"\{prf:ref\}`[^`]+`")
GENERATED_SENTENCES = "num-"
"""Code cells whose id starts so print one or two sentences of prose built from the case."""
LEDGER = PAPER / "length_ledger.toml"
"""The length ledger: a baseline per section and a row for every raise (see the file's header)."""
NOT_A_JOB = ("fit", "to fit", "to fit the text", "fits", "fill", "to fill")


def _ledger() -> dict:
    return tomllib.loads(LEDGER.read_text(encoding="utf-8"))


def ledger_ceilings() -> tuple[int, dict[str, int]]:
    """The total ceiling and each section's: the baseline plus the rows that raise it, less the
    cut rows (a cut lowers the ceiling to the count after, OD5 (a) of WP28)."""
    ledger = _ledger()
    rows = ledger.get("raise", [])
    cuts = ledger.get("cut", [])
    sections = dict(ledger["baseline"]["sections"])
    for row in rows:
        sections[row["section"]] = sections[row["section"]] + row["words_added"]
    for row in cuts:
        sections[row["section"]] = sections[row["section"]] - row["words_removed"]
    total = ledger["baseline"]["total"]
    return total + sum(r["words_added"] for r in rows) - sum(
        r["words_removed"] for r in cuts
    ), sections


def rendered_words(text: str) -> int:
    """Words the reader meets in a cell's Markdown source.

    A cross-reference counts as its printed title (``Section 0``, ``Theorem 0``), a citation as an
    author and a year for each key, an inline formula and an inline code span as one token each.
    What prints nothing is not counted: the directive lines and their options, labels, display
    equations. Captions, hypotheses, sketches, script pointers and list items are counted.
    """
    text = _rendered(text)
    text = _MATH_BLOCK.sub(" ", text)
    text = re.sub(r"<[^>]+>", "", text)  # the tags of a link in a generated sentence print nothing
    text = re.sub(r"\]\([^)\s]*\)", "]", text)  # a link's target is not read, only its text
    text = _PRF_REF.sub("Theorem 0", text)
    text = _CITES.sub(lambda m: "Author 2000 " * (m.group(1).count("@")), text)
    text = _DISPLAY_MATH.sub(" ", text)
    text = _FENCE.sub(  # a title or a caption is read; a figure's path is not
        lambda m: (
            m.group("arg") if m.group("name").startswith(("prf:", "admonition", "table")) else ""
        ),
        text,
    )
    text = _OPTION_LINE.sub("", text)
    text = re.sub(r"^:{3,}\s*$", "", text, flags=re.M)
    return len(re.sub(r"[#>*`:{}\[\]|-]", " ", text).split())


def words_by_section() -> dict[str, int]:
    """Rendered words of the body, per section: the Markdown the page shows plus the generated
    sentences of the case. Not counted: the abstract (its own cap), cells the page does not show,
    the bibliography, and the tables (the family table and the candidates table are data, as the
    appendices' tables are)."""
    out: dict[str, int] = {}
    current = None
    for i, c in enumerate(_nb(PAPER_NB).cells):
        if i == 0:
            continue
        if c.cell_type == "markdown":
            if "remove-cell" in c.metadata.get("tags", []):
                continue
            head = _unlabel(_src(c))
            if head.startswith("## "):
                current = head.splitlines()[0][3:].strip()
            n = rendered_words(_src(c))
        elif c.id.startswith(GENERATED_SENTENCES):
            n = rendered_words(_out_text(c))
        else:
            continue
        out[current] = out.get(current, 0) + n
    return out


def test_counted_words_within_the_ledgers_total_ceiling():
    """R-2, G-1: the prose a reader meets, generated sentences included, is at most the baseline
    of the length ledger plus its rows. The cap is a regularizer: growth needs a row."""
    total, _ = ledger_ceilings()
    assert sum(words_by_section().values()) <= total, "add a [[raise]] row to length_ledger.toml"


def test_each_section_is_within_the_ledgers_ceiling():
    """R-2: a section's count is at most its baseline plus the rows that name it."""
    _, ceilings = ledger_ceilings()
    counted = words_by_section()
    assert set(counted) <= set(ceilings), set(counted) - set(ceilings)
    for name, count in counted.items():
        assert count <= ceilings[name], (name, count, ceilings[name], "needs a [[raise]] row")


def test_each_ledger_row_names_a_job_a_reader_and_a_section_of_the_paper():
    """A raise is admitted by what its words do and for whom; 'to fit the text' is no job."""
    import datetime

    ledger = _ledger()
    assert set(ledger["baseline"]["sections"]) >= set(words_by_section())
    assert sum(ledger["baseline"]["sections"].values()) == ledger["baseline"]["total"]
    assert sum(ledger["baseline"]["sections"].values()) == ledger["baseline"]["total"] or True
    for row in ledger.get("raise", []):
        assert set(row) == {"date", "section", "words_added", "job", "reader"}, row
        datetime.date.fromisoformat(str(row["date"]))
        assert row["section"] in ledger["baseline"]["sections"], row
        assert isinstance(row["words_added"], int) and row["words_added"] > 0, row
        assert len(row["reader"].split()) >= 2, row
        job = row["job"].strip().rstrip(".").lower()
        assert len(job.split()) >= 4 and job not in NOT_A_JOB, row
        assert not job.startswith(("to fit the text", "fit the text")), row
    for row in ledger.get("cut", []):  # a cut row records what left and what it no longer did
        assert set(row) == {"date", "section", "words_removed", "no_longer_did", "authority"}, row
        datetime.date.fromisoformat(str(row["date"]))
        assert row["section"] in ledger["baseline"]["sections"], row
        assert isinstance(row["words_removed"], int) and row["words_removed"] > 0, row
        assert len(row["no_longer_did"].split()) >= 4 and len(row["authority"].split()) >= 2, row


def test_generated_sentences_are_counted_not_excluded():
    """The counter reads the committed outputs of the sentence cells, so none is left out."""
    cells = [c for c in _code_cells(_nb(PAPER_NB)) if c.id.startswith(GENERATED_SENTENCES)]
    assert len(cells) >= 8
    assert rendered_words(" ".join(_out_text(c) for c in cells)) > 100


def test_register_forbidden_phrases_are_absent_from_all_prose():
    """R-5: the register's forbidden phrases appear nowhere in the paper's prose or appendices."""
    text = (NOTES / "notation.md").read_text(encoding="utf-8")
    block = text.split("## Forbidden phrases", 1)[1]
    phrases = re.findall(r"^- `([^`]+)`", block, re.M)
    assert len(phrases) >= 10
    prose = (_markdown(_nb(PAPER_NB)) + _markdown(_nb(SUPPORT_NB))).lower()
    for ph in phrases:
        assert ph.lower() not in prose, ph
    # the compiled tables are checked too, on the committed outputs
    for path in (PAPER_NB, SUPPORT_NB):
        out = " ".join(_out_text(c) for c in _code_cells(_nb(path))).lower()
        for ph in phrases:
            assert ph.lower() not in out, f"{ph!r} in the outputs of {path.name}"


@needs_prose
def test_register_phrases_are_used_in_the_body():
    """R-5 (hook, active with the prose): each register phrase appears in the paper."""
    text = (NOTES / "notation.md").read_text(encoding="utf-8")
    block = text.split("## Register phrases", 1)[1].split("## Forbidden phrases", 1)[0]
    phrases = re.findall(r"^- `([^`]+)`", block, re.M)
    prose = (_markdown(_nb(PAPER_NB)) + _markdown(_nb(SUPPORT_NB))).lower()
    missing = [p for p in phrases if p.lower() not in prose]
    assert not missing, missing


@needs_prose
def abstract_cap() -> int:
    """The abstract's bound: the ledger's target plus its tolerance (the ruling of 17:35)."""
    abstract = _ledger()["abstract"]
    return abstract["cap"] + abstract["tolerance"]


def test_abstract_within_its_target():
    """R-13 L-A (hook, active with the prose): the supervisor's target of 500 words with slight
    under or overshoot allowed (WP11-decisions.md, 2026-11-14 17:35): target plus tolerance."""
    fm = yaml.safe_load(_src(_nb(PAPER_NB).cells[0]).split("---")[1])
    assert _ledger()["abstract"]["cap"] == 500
    assert len(fm["abstract"].split()) <= abstract_cap()


@needs_prose
def test_every_appendix_is_cited_from_the_body():
    """R-25 (hook, active with the prose): each appendix is cited at least once from the body."""
    body = _markdown(_nb(PAPER_NB))
    for letter in APPENDICES:
        assert re.search(rf"Appendix {letter}\b", body), letter


# ---- cell structure: one call per code cell ----------------------------------------------------


def _calls(tree) -> list[ast.Call]:
    return [n for n in ast.walk(tree) if isinstance(n, ast.Call)]


def _check_cell(cell, setup: bool):
    tree = ast.parse(_src(cell))
    banned = (ast.FunctionDef, ast.ClassDef, ast.For, ast.While, ast.If, ast.With, ast.Try)
    assert not [n for n in ast.walk(tree) if isinstance(n, banned)], "a cell defines nothing"
    body = [n for n in tree.body if not isinstance(n, ast.Import | ast.ImportFrom)]
    calls = _calls(tree)
    if setup:
        return
    assert len(calls) <= 1, f"{cell.id}: more than one call in a cell"
    for stmt in body:
        assert isinstance(stmt, ast.Expr | ast.Assign), cell.id
    for call in calls:  # arguments are names, attributes or constants, never calls
        for arg in [*call.args, *[k.value for k in call.keywords]]:
            assert not _calls(arg), f"{cell.id}: a call nested in an argument"


@pytest.mark.parametrize("path", [PAPER_NB, SUPPORT_NB], ids=lambda p: p.name)
def test_code_cells_make_one_call_and_define_nothing(path):
    """R-3, R-24: a cell is imports and at most one call; the tables are calls, not typed."""
    for cell in _code_cells(_nb(path)):
        _check_cell(cell, setup=cell.id.startswith("setup"))


@pytest.mark.parametrize("path", [PAPER_NB, SUPPORT_NB], ids=lambda p: p.name)
def test_figure_and_table_cells_are_exactly_one_call(path):
    for cell in _code_cells(_nb(path)):
        if cell.id.startswith(("fig-", "tab-")):
            assert len(_calls(ast.parse(_src(cell)))) == 1, cell.id


def test_case_calls_go_through_the_case_module():
    """R-3: a figure cell of the paper calls case.py (or a generator), nothing else."""
    for cell in _code_cells(_nb(PAPER_NB)):
        if not cell.id.startswith(("fig-", "tab-")):
            continue
        tree = ast.parse(_src(cell))
        call = _calls(tree)[0]
        name = ast.unparse(call.func)
        assert name.startswith("case.") or name in {
            "family_table",
            "decision_table",
            "requirement_order_table",
        }, (
            cell.id,
            name,
        )


def test_paper_cells_have_committed_outputs_without_errors():
    """The shells that run headlessly are committed executed."""
    for path in (PAPER_NB, SUPPORT_NB):
        for cell in _code_cells(_nb(path)):
            if cell.id.startswith(("fig-", "tab-")):
                assert cell.outputs, f"{cell.id} has no committed output ({STALE})"
            assert not [o for o in cell.outputs if o.output_type == "error"], cell.id


_WARNING_TEXT = re.compile(r"\w*Warning\b|warnings\.warn|did not converge")


def test_committed_outputs_carry_no_stderr_or_warning():
    """No executed cell of either notebook carries a stderr stream or a warning's text: a
    solver's termination status is a fact for a table's status column, not a line on the page
    (driver-log, 2026-11-09, the B.9 recovery cell)."""
    problems = []
    for path in (PAPER_NB, SUPPORT_NB):
        for cell in _code_cells(_nb(path)):
            for out in cell.outputs:
                if out.output_type == "stream":
                    text = "".join(out.get("text", ""))
                else:
                    data = out.get("data", {})
                    text = "".join(data.get("text/markdown", "")) + "".join(
                        data.get("text/plain", "")
                    )
                found = _WARNING_TEXT.search(text)
                if out.get("name") == "stderr":
                    problems.append(f"{path.name}:{cell.id} has a stderr stream")
                elif found:
                    problems.append(f"{path.name}:{cell.id} prints {found.group(0)!r}")
    assert not problems, (problems, STALE)


def test_figures_have_numbered_self_contained_captions():
    """R-4: each figure and table cell is embedded in a directive with a label and a caption."""
    nb = _nb(PAPER_NB)
    md = _markdown(nb)
    for cell in _code_cells(nb):
        if not cell.id.startswith(("fig-", "tab-")):
            continue
        kind = "figure" if cell.id.startswith("fig-") else "table"
        embedded = re.search(rf"\{{({kind}|embed)\}}[^\n]*\n?[^\n]*#{cell.id}\b|#{cell.id}\b", md)
        assert embedded, f"{cell.id} is not embedded in a {kind}"
    for m in re.finditer(r"\{figure\}\s*#([\w-]+)\s*\n:label:\s*(\S+)\s*\n(.*?)\n:::", md, re.S):
        assert m.group(3).strip(), f"figure {m.group(1)} has no caption"
    for m in re.finditer(r"\{table\}\s*([^\n]*)\n:label:\s*(\S+)", md):
        assert m.group(1).strip(), f"table {m.group(2)} has no caption"
    labels = re.findall(r":label:\s*(\S+)", md)
    assert len(labels) == len(set(labels))


# ---- the appendices ----------------------------------------------------------------------------


def test_appendix_headings_a_to_h_in_order():
    heads = [h for h in _headings(_nb(SUPPORT_NB)) if h.startswith("Appendix")]
    assert heads == [f"Appendix {k}. {v}" for k, v in APPENDICES.items()]


def test_the_letters_are_the_order_of_first_mention_in_the_paper():
    """WP57e R-1: the first reference to an appendix or to any of its subsections, in the paper's
    cell order from the front matter to the works cited, meets the letters A to H in order."""
    first: list[str] = []
    for c in _nb(PAPER_NB).cells:
        if c.cell_type != "markdown":
            continue
        for m in re.finditer(r"\{ref\}`[^`<]*<(?:appendix-([a-h])|sub-([a-h])-\d+)>`", _src(c)):
            letter = (m.group(1) or m.group(2)).upper()
            if letter not in first:
                first.append(letter)
    assert first == list(APPENDICES)


def test_every_appendix_numbers_its_subsections_from_one():
    """WP57e G4: under each letter the subsections run 1, 2, 3, ... with no gap, in the order of
    the page (D, the notation table, has none)."""
    for letter, cells in _appendix_cells(_nb(SUPPORT_NB)).items():
        nums = [
            int(n) for c in cells if c.cell_type == "markdown"
            for n in re.findall(rf"^### {letter}\.(\d+) ", _unlabel(_src(c)), re.M)
        ]  # fmt: skip
        assert nums == list(range(1, len(nums) + 1)), (letter, nums)
    heads = [h.split(" ", 1)[0] for h in _headings(_nb(SUPPORT_NB), "###")]
    assert [h[0] for h in heads] == sorted(h[0] for h in heads)  # each under its own letter


def test_no_withdrawn_appendices():
    """The source map, the search's appendix and the verification audit are withdrawn."""
    all_heads = " ".join(_headings(_nb(SUPPORT_NB), "##") + _headings(_nb(SUPPORT_NB), "###"))
    assert not re.search(r"source map|search|audit|verification", all_heads, re.I)
    assert not (PAPER / "source_map.md").exists()
    assert not [p for p in PAPER.glob("*audit*")]


def test_no_appendix_opens_with_a_job_block():
    """WP57a to WP57d cut the Job block and its three tiers (R-25) from every appendix (the rule on
    metanarration): no appendix says what it carries or what the main text keeps."""
    sections = _appendix_cells(_nb(SUPPORT_NB))
    assert list(sections) == list(APPENDICES)
    for letter, cells in sections.items():
        text = "\n".join(_src(c) for c in cells if c.cell_type == "markdown")
        assert "**Job.**" not in text, letter
        assert not any(tier in text for tier in TIERS), letter


def test_no_appendix_is_a_stub():
    """R-25: every appendix has a generated table with a committed output, B excepted until its
    record is delivered (it states its parts and the state of the record)."""
    for letter, cells in _appendix_cells(_nb(SUPPORT_NB)).items():
        gen = [c for c in cells if c.cell_type == "code"]
        assert gen, f"Appendix {letter} has no generated content"
        for c in gen:
            assert _out_text(c).strip(), f"{c.id} has no committed output ({STALE})"
            if letter not in AWAITING_RECORD and not c.id.startswith(
                "sent-"
            ):  # sentences, not tables
                assert "|" in _out_text(c) or len(_out_text(c)) > 200, c.id


def test_appendix_cells_import_from_the_generators():
    for cell in _code_cells(_nb(SUPPORT_NB)):
        if cell.id.startswith("setup"):
            continue
        assert re.search(r"^from generate_\w+ import \w+$", _src(cell), re.M), cell.id


# -- D: the register table is compiled from glossary.yaml


def test_register_table_equals_the_glossary_entries_in_use():
    """WP57a: one row per glossary entry the paper or the appendices use, by the vocabulary
    checker's rule, in the glossary's order; an unused entry stays in the glossary and off the page;
    no Layer column."""
    all_entries = yaml.safe_load((ROOT / "glossary.yaml").read_text(encoding="utf-8"))["entries"]
    used = generate_register.used_entry_ids()
    entries = [e for e in all_entries if e["id"] in used]
    assert 0 < len(all_entries) - len(entries) < len(all_entries) // 4
    headers, rows = generate_register.register_rows()
    assert len(rows) == len(entries)
    assert "Layer" not in headers
    text = str(generate_register.register_table())
    for e in all_entries:
        if e["id"] not in used:
            assert f"| {e['register']} |" not in text, e["id"]
    for e, row in zip(entries, rows, strict=True):
        assert row[0] == e["register"] and row[2] == e["formal"] and row[3] == e["not"]
        assert e["register"] in text and e["formal"] in text
        if e.get("symbol"):
            sym = e["symbol"]  # mathematics, or code font for a fitted attribute such as `name_`
            shown = f"`{sym}`" if re.fullmatch(r"[A-Za-z]\w*_", sym) else f"${sym}$"
            assert shown in text
    assert headers[:5] == ["Term", "Symbol", "Meaning in this paper", "Not", "Defined in"]


def test_register_committed_output_is_current():
    cell = next(c for c in _code_cells(_nb(SUPPORT_NB)) if c.id == "tab-D-register")
    assert _out_text(cell) == str(generate_register.register_table()), STALE


# -- G: assumptions, limitations and open questions


def _e_cells():
    return _appendix_cells(_nb(SUPPORT_NB))["G"]


def test_appendix_e_has_its_three_parts_in_order():
    """WP57d G1: G.1 assumptions, G.2 limitations, G.3 open questions, anchored ``sub-g-1`` to
    ``sub-g-3``; each part is tables, the typed parts no prose outside them but their captions."""
    heads = [_src(c).splitlines()[:2] for c in _e_cells() if _src(c).startswith("(sub-g-")]
    assert heads == [
        ["(sub-g-1)=", "### G.1 Assumptions"],
        ["(sub-g-2)=", "### G.2 Limitations"],
        ["(sub-g-3)=", "### G.3 Open questions"],
    ]
    ids = [c.id for c in _e_cells()]
    assert ids.index("tab-G-assumptions") < ids.index("app-G-2") < ids.index("tab-G-gaps")
    assert ids.index("tab-G-gaps") < ids.index("app-G-3")
    for cid in ("app-G-2", "app-G-3"):
        body = _src(next(c for c in _e_cells() if c.id == cid)).split("\n", 3)[3]
        assert all(ln.startswith("|") for ln in body.splitlines()), cid


def test_the_assumptions_tables_are_the_ledger_of_the_derivation():
    """WP57d G5, R-4: one row per entry of ``derivation/axioms.py``, A and R in the first table and
    I and F in the second, each with the ledger's statement in one line, the citation, and the
    results whose scripts import it by the proof map's record; nothing typed."""
    from derivation.axioms import AXIOMS

    def rows(text):  # a cell may hold an escaped pipe (I9's norms)
        lines = [ln for ln in text.splitlines() if ln.startswith("|")][2:]
        return [[x.strip() for x in re.split(r"(?<!\\)\|", ln.strip("|"))] for ln in lines]

    first = rows(str(generate_gaps.assumptions_table()))
    second = rows(str(generate_gaps.cited_table()))
    names = [r[0].strip("*") for r in first + second]
    assert sorted(names) == sorted(AXIOMS) and len(names) == len(set(names))
    assert [n[0] for n in names[: len(first)]] == ["A"] * 12 + ["R"] * 3
    record = json.loads((ROOT / "derivation" / "proof_map_record.json").read_text(encoding="utf-8"))
    for row in first + second:
        name = row[0].strip("*")
        users = sorted(lem["number"] for lem in record["lemmas"].values() if name in lem["imports"])
        shown = [int(n) for n in re.findall(r"\[L(\d+)\]\(#proof-l\1\)", row[-1])]
        assert shown == users, name
        assert generate_gaps.one_line(AXIOMS[name].statement)[:20] in row[1].replace("\\", "")
    for row in second:
        name = row[0].strip("*")
        assert " ".join(AXIOMS[name].citation.split())[:30] in row[2].replace("\\", ""), name
    stated = {r[0].strip("*"): r[2] for r in first}
    assert stated["A1"] == stated["A2"] == stated["A3"] == "Section 3"
    assert stated["A4"] == stated["A6"] == stated["A8"] == "Section 5"
    assert all(stated[n] == "Section 6" for n in ("A5", "A7", "A9", "A10", "A11", "R1", "R2", "R3"))
    for cid, fn in (("tab-G-assumptions", "assumptions_table"), ("tab-G-cited", "cited_table")):
        cell = next(c for c in _code_cells(_nb(SUPPORT_NB)) if c.id == cid)
        assert _out_text(cell) == str(getattr(generate_gaps, fn)()), STALE


def _open_question_ids() -> tuple[list[str], list[str]]:
    """The ledger's open and closed entries, by their headings and a "Closed" line."""
    text = (ROOT / "work-packages" / "review" / "open-questions.md").read_text(encoding="utf-8")
    entries = re.split(r"^## ", text, flags=re.M)[1:]
    ids = [re.match(r"(OQ-\d+)\.", e).group(1) for e in entries]
    closed = [i for i, e in zip(ids, entries, strict=True) if "**Closed" in e]
    return [i for i in ids if i not in closed], closed


def test_e3_lists_every_open_question_of_the_ledger_once_and_no_closed_one():
    """WP57d G1, G5: each open OQ is one row of G.3, in the ledger's order; no closed entry is
    listed; the two research questions of Section 9 point at their records in the repository."""
    open_ids, closed = _open_question_ids()
    assert closed == ["OQ-11"] and "OQ-14" in open_ids
    text = _src(next(c for c in _e_cells() if c.id == "app-G-3"))
    listed = re.findall(r"\[(OQ-\d+)\]", text)
    assert listed == open_ids
    assert not any(f"[{c}]" in text for c in closed)
    assert "notes/directions/wp43-kernel-direction.md" in text
    assert "successive trade-offs" in text
    rows = [ln for ln in text.splitlines() if ln.startswith("| ") and "---" not in ln][1:]
    assert len(rows) == len(open_ids) + 2


def test_e2_places_every_line_of_the_queue_and_names_records_that_resolve():
    """WP57d G2, R-1: every queue line of ``tests/data/wp57/assumptions-queue.md`` is marked with
    where it landed; every G-id in G.2 is a row of the gaps table, every OQ-id an open entry of
    the ledger, every L-id a lemma of the proof map."""
    queue = (ROOT / "tests" / "data" / "wp57" / "assumptions-queue.md").read_text(encoding="utf-8")
    rows = [ln for ln in queue.splitlines() if ln.startswith("| ") and "---" not in ln][1:]
    # the queue is a dated record: it names the parts by the letter they had at WP57d
    assert len(rows) == 9 and all("E.2" in r or "E.3" in r for r in rows)
    text = _src(next(c for c in _e_cells() if c.id == "app-G-2"))
    gaps = {r["id"] for r in generate_gaps.gap_rows()}
    assert set(re.findall(r"\bG-\d+", text)) <= gaps
    assert set(re.findall(r"\bOQ-\d+", text)) <= set(_open_question_ids()[0])
    record = json.loads((ROOT / "derivation" / "proof_map_record.json").read_text(encoding="utf-8"))
    lemmas = {f"L{lem['number']}" for lem in record["lemmas"].values()}
    assert set(re.findall(r"\bL\d+\b", text)) <= lemmas
    for line in [ln for ln in text.splitlines() if ln.startswith("| ")][1:]:
        assert line.count("|") == 4, line  # section, what is not established, record
    assert "| Section" not in text.split("---|", 1)[1]  # a section is named by a role, not typed


def test_gaps_table_has_every_ledger_row():
    rows = generate_gaps.gap_rows()
    ledger_ids = re.findall(
        r"^\| \*\*(G-\d+)\.", (NOTES / "abstraction-gaps.md").read_text(encoding="utf-8"), re.M
    )
    assert [r["id"] for r in rows] == ledger_ids == [f"G-{i}" for i in range(1, len(rows) + 1)]
    for r in rows:
        for col in generate_gaps.COLUMNS:
            assert r[col].strip(), (r["id"], col)
    ledger = (NOTES / "abstraction-gaps.md").read_text(encoding="utf-8")
    assert len(re.findall(r"^\| \*\*G-\d+\.", ledger, re.M)) == len(rows)


def test_gaps_committed_output_is_current():
    cell = next(c for c in _code_cells(_nb(SUPPORT_NB)) if c.id == "tab-G-gaps")
    assert _out_text(cell) == str(generate_gaps.gaps_table()), STALE


def test_gaps_table_typesets_its_mathematics_on_the_page():
    """The page shows a notebook's HTML output as given and typesets no ``$...$`` in it, so the
    table writes each span of the ledger's columns as MathML: one ``<math>`` per span, no literal
    dollar sign left, and no emphasis made of an underscore inside a span."""
    cols = ("title", *generate_gaps.GAP_COLUMNS)
    spans = [m for r in generate_gaps.gap_rows() for c in cols
             for m in re.findall(r"\$[^$]+\$", r[c])]  # fmt: skip
    page = generate_gaps.gaps_table()._repr_html_()
    assert spans and "<em>" not in page and "MATHSPAN" not in page
    assert page.count("<math>") == len(spans)
    assert "$" not in re.sub(r"<[^>]+>", "", page)


def test_register_table_typesets_its_mathematics_on_the_page():
    """Appendix D's table, as Appendix G's: the page shows an HTML output as given, so each
    ``$...$`` span of the register is written as MathML, no literal dollar sign is left, and the
    Markdown a notebook viewer typesets is the glossary's text unchanged."""
    table = generate_register.register_table()
    spans = re.findall(r"\$[^$]+\$", str(table))
    page = table._repr_html_()
    assert len(spans) > 20 and "MATHSPAN" not in page and "<em>" not in page
    assert page.count("<math>") == len(spans)
    assert "$" not in re.sub(r"<[^>]+>", "", page)
    assert str(table) == table.raw


def test_gaps_table_keeps_four_columns_and_links_each_row_of_the_ledger():
    """WP57d G1: the gap, the bridging assumption, what cannot be proved and the interpretive
    consequence; the formal object and the sensitivity evidence stay in the ledger, whose row each
    gap links by its line."""
    table = str(generate_gaps.gaps_table())
    assert table.splitlines()[0] == (
        "| Gap | Bridging assumption | What cannot be proved | Interpretive consequence |"
    )
    lines = (NOTES / "abstraction-gaps.md").read_text(encoding="utf-8").splitlines()
    for r in generate_gaps.gap_rows():
        assert f"abstraction-gaps.md?plain=1#L{r['line']})" in table
        assert lines[r["line"] - 1].startswith(f"| **{r['id']}.")
    assert "Formal object" not in table and "Sensitivity evidence" not in table


def test_gaps_table_gives_every_column_a_width_hint():
    """The bridging-assumption column is not left to the browser, which squeezed it to a word a
    line beside a column of 940 px: one width per column, none narrower than the gap's."""
    page = generate_gaps.gaps_table()._repr_html_()
    widths = [int(w) for w in re.findall(r'<col style="width:(\d+)px">', page)]
    assert len(widths) == len(generate_gaps.gaps_table().raw.splitlines()[0].strip("|").split("|"))
    assert widths == list(generate_gaps.WIDTHS) and "table-layout:fixed" in page
    assert min(widths[2:]) >= 200  # every text column reads at about thirty characters or more


def test_no_repository_path_stands_in_parentheses_in_the_paper_or_its_appendices():
    """A path in parentheses reads as machine-written prose: the paper and the appendices carry
    each as a link with words (``link_paths``, ``repo_link``). The residual pass's own counter."""
    import sys

    sys.path.insert(0, str(ROOT / "scripts"))
    import check_residuals as cr
    import prose_surfaces as ps

    hits = [
        (s.id, b.loc)
        for s in ps.collect()
        if s.kind in ("paper", "appendix")
        for b in s.blocks
        if cr.path_parens(b.raw)
    ]
    assert hits == []


def test_the_tex_subset_of_the_tables_becomes_mathml():
    from paper_common import tex_to_mathml

    assert tex_to_mathml(r"J_\tau(Uw)").startswith("<math><msub><mi>J</mi><mi>τ</mi></msub>")
    assert "<msubsup>" in tex_to_mathml(r"\max_k^2 x")
    assert "<mfrac>" in tex_to_mathml(r"\tfrac1\tau")
    with pytest.raises(ValueError, match="unsupported"):
        tex_to_mathml(r"\frac{a}{b}")


# -- H: the pinned toolchain is generated from the lock


def _lock_versions():
    data = tomllib.loads((ROOT / "uv.lock").read_text(encoding="utf-8"))
    return {p["name"]: p["version"] for p in data["package"] if "version" in p}


def test_toolchain_matches_the_lock_pyproject_and_python_version():
    """R-30: the stated versions are the lock's."""
    locked = _lock_versions()
    text = str(generate_repro.toolchain())
    pp = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    names = [
        re.match(r"[A-Za-z0-9_.-]+", r).group(0).lower() for r in pp["project"]["dependencies"]
    ]
    names += [
        re.match(r"[A-Za-z0-9_.-]+", r).group(0).lower() for r in pp["dependency-groups"]["paper"]
    ]
    assert {"numpy", "scipy", "scikit-learn", "sympy", "pandas", "matplotlib", "mystmd"} <= set(
        names
    )
    for name in names:
        assert f"| {name} | {locked[name]} |" in text, name
    py = (ROOT / ".python-version").read_text(encoding="utf-8").strip()
    assert f"| Python | {py} |" in text
    assert "| Package manager | uv " in text
    assert f"| Locked packages | {len(locked)} |" in text
    assert "uv.lock" in text and "pyproject.toml" in text and ".python-version" in text
    assert re.search(r"\| Commit \| ([0-9a-f]{40}|not found|)", text)


def test_f_prose_types_no_versions():
    """R-24, R-30: the versions come from the generator, never from typed prose."""
    cells = _appendix_cells(_nb(SUPPORT_NB))["H"]
    for c in cells:
        if c.cell_type == "markdown":
            assert not re.search(r"\b\d+\.\d+(\.\d+)?\b", _src(c)), c.id


def test_f_toolchain_committed_output_matches_the_lock():
    cell = next(c for c in _code_cells(_nb(SUPPORT_NB)) if c.id == "tab-H-toolchain")
    out = _out_text(cell)
    for name in ("numpy", "scipy", "scikit-learn", "sympy", "pandas", "matplotlib", "mystmd"):
        assert f"| {name} | {_lock_versions()[name]} |" in out, f"{name}: {STALE}"


def test_f_container_paragraph_is_a_marked_placeholder_region():
    cells = _appendix_cells(_nb(SUPPORT_NB))["H"]
    text = "\n".join(_src(c) for c in cells if c.cell_type == "markdown")
    assert text.count("% container-paragraph:begin") == 1
    assert text.count("% container-paragraph:end") == 1
    assert text.index("container-paragraph:begin") < text.index("container-paragraph:end")


def test_f_commands_exist_in_the_repository():
    """R-23 (structural): every command in the table names a target that exists."""
    text = str(generate_repro.commands())
    assert "uv run pytest" in text and "myst build --html" in text
    for module in re.findall(r"python -m (derivation\.\w+)", text):
        assert (ROOT / (module.replace(".", "/") + ".py")).is_file(), module
    for script in re.findall(r"python (paper/\w+\.py)", text):
        assert (ROOT / script).is_file(), script


def test_f_has_a_row_for_every_figure_and_table_cell():
    """R-23 (structural): one row per figure or table cell of both notebooks."""
    labelled = [
        c.id
        for p in (PAPER_NB, SUPPORT_NB)
        for c in _code_cells(_nb(p))
        if c.id.startswith(("fig-", "tab-"))
    ]
    rows = {r[0]: r for r in generate_repro.reproduction_rows()}
    assert set(rows) == set(labelled)
    for r in rows.values():
        assert all(cell.strip() for cell in r)


# -- F and B: disjoint and complementary at the metric table


def _cells_of(letter):
    return [c for c in _appendix_cells(_nb(SUPPORT_NB))[letter] if c.cell_type == "code"]


def test_c_defines_the_dataset_labels_and_names_each_dataset_once():
    out = "\n".join(_out_text(c) for c in _cells_of("F"))
    labels = set(generate_model.DATASET_LABELS.values())
    assert len(labels) == 3
    table = next(c for c in _cells_of("F") if c.id == "tab-F-datasets")
    for label in labels:
        assert _out_text(table).count(f"| {label} |") == 1, label
        assert label in out


def test_c_contains_no_fitted_quantity():
    """R-26: no exponent fitted, temperature, value of V, term found, reach or share in C."""
    for c in _cells_of("F"):
        text = _out_text(c)
        assert not FITTED_WORDS.search(text), (c.id, FITTED_WORDS.search(text).group(0))


def test_d_contains_no_definition_of_the_system():
    """R-26: no variable range, constraint, scenario constant or conditioning rule in D."""
    for c in _cells_of("B"):
        m = SYSTEM_WORDS.search(_out_text(c))
        assert not m, (c.id, m and m.group(0))


def test_every_table_of_d_cites_its_dataset_by_cs_label():
    labels = set(generate_model.DATASET_LABELS.values())
    moved = {cell for cell, _ in MOVED_TO_D.values()}  # sentences under a table that cites it
    for c in _cells_of("B"):
        if c.id in moved:
            continue
        text = _out_text(c)
        cited = set(re.findall(r"\b(cubesat-\w+|planted-[\w-]+)", text))
        assert cited and cited <= labels, (c.id, cited)
        assert re.search(r"Datasets? ", text), c.id


def test_no_table_or_figure_appears_in_both_c_and_d():
    c_calls = {ast.unparse(_calls(ast.parse(_src(c)))[0]) for c in _cells_of("F")}
    d_calls = {ast.unparse(_calls(ast.parse(_src(c)))[0]) for c in _cells_of("B")}
    assert not c_calls & d_calls
    c_tables = set().union(*[_tables(_out_text(c)) for c in _cells_of("F")])
    d_tables = set().union(*[_tables(_out_text(c)) for c in _cells_of("B")])
    assert not c_tables & d_tables


_TOKEN = re.compile(r"([0-9a-f]{64}|[-+]?\d+(?:\.\d+)?(?:[eE][-+]?\d+)?)")
_PLANTED_LABEL = re.escape(generate_model.DATASET_LABELS["planted"])
_PLANTED_ROW = re.compile(rf"^(\| {_PLANTED_LABEL} \|.*?)\b[0-9a-f]{{64}}\b", re.M)


def _mask_exact_only(text: str) -> str:
    """Blank the digest of the planted table's row: exact only in the environment of record."""
    return _PLANTED_ROW.sub(r"\1<planted_table_sha256>", text)


def _same_text(a: str, b: str, rtol: float) -> bool:
    """Equal text whose numbers agree within ``rtol`` (digests and everything else must match)."""
    pa, pb = _TOKEN.split(a), _TOKEN.split(b)
    if len(pa) != len(pb):
        return False
    for i, (x, y) in enumerate(zip(pa, pb, strict=True)):
        if i % 2 == 0 or len(x) == 64 or len(y) == 64:  # between tokens, or a digest
            if x != y:
                return False
        elif not np.isclose(float(x), float(y), rtol=rtol, atol=0.0):
            return False
    return True


def _current(committed: str, fresh: str, what: str) -> None:
    """A committed output against its re-run: byte-equal in the environment of record, elsewhere
    the same text with its numbers within the stated tolerance (the digest left uncompared)."""
    if exact_only("planted_table_sha256"):
        assert committed == fresh, f"{what}: {STALE}"
    else:
        rtol = listed()["planted_table_sha256"]["text_rtol"]
        assert _same_text(_mask_exact_only(committed), _mask_exact_only(fresh), rtol), (
            f"{what}: {STALE}"
        )


_TERM_NUMBERED = (
    ("tab-B-exponents_and_terms", "exponents_and_terms"),
    ("tab-B-termination_records", "termination_records"),
)


def _cells_of_table(text: str) -> list[str]:
    """The cells of every table row, whitespace-normalised and sorted: the order-free content."""
    cells = (c.strip() for line in text.splitlines() if line[:1] == "|" for c in line.split("|"))
    return sorted(cells)


@pytest.mark.slow
def test_term_numbered_tables_are_current():
    """The tables whose rows follow the term numbering: exact in the environment of record,
    elsewhere the same cells in whatever order the terms are numbered (gap G-10)."""
    import generate_results

    exact = exact_only("term_numbered_tables")
    by_id = {c.id: c for c in _code_cells(_nb(SUPPORT_NB))}
    for cid, fn in _TERM_NUMBERED:
        committed, fresh = _out_text(by_id[cid]), str(getattr(generate_results, fn)())
        if exact:
            assert committed == fresh, f"{cid}: {STALE}"
        else:
            assert _cells_of_table(committed) == _cells_of_table(fresh), f"{cid}: {STALE}"


@pytest.mark.slow
def test_d2_lists_follow_the_estimators_term_order_for_every_k():
    """The old D.2's per-term lists (now B.4's) are the estimator's own: ``term rows`` are the
    cell sizes and ``term shares`` the ``term_share_`` (to three digits) of each fit, in the order
    the fit returns them."""
    import case
    import generate_results as gr

    for regime in ("primary", "stock"):
        study, fits = gr._study(regime), gr._fits(regime)
        kt = case.k_table(study, fits)
        for i, K in enumerate(kt["K"]):
            if K < 2:
                continue
            est = fits[int(K)].estimator
            assert list(kt.iloc[i]["term shares"]) == [round(float(v), 3) for v in est.term_share_]
            assert list(kt.iloc[i]["term rows"]) == [
                int(v) for v in np.bincount(est.cell_, minlength=int(K))
            ]


def test_a_count_in_the_regime_sentence_has_its_thousands_separator_and_the_attributes_are_words():
    from types import SimpleNamespace as NS

    import generate_findings as gf

    def regime(raw, kept):
        return NS(raw=range(raw), feasible=range(kept), attrs=range(13))

    text = str(gf.datasets_sentence(regime(3000, 2134), regime(3000, 2355)))
    assert text.startswith(
        "The primary regime evaluates 3,000 designs and keeps 2,134 as feasible; the baseline "
        "regime evaluates 3,000 and keeps 2,355. Each design carries thirteen attributes. "
        "The designs are drawn at random, 3,000 per regime"
    )
    import paper_common

    assert [paper_common.thousands(v) for v in (999, 1000, 2134, "145 to 2200", "0.2036")] == [
        "999", "1,000", "2,134", "145 to 2,200", "0.2036",
    ]  # fmt: skip


def test_an_exact_zero_and_a_residue_have_one_spelling_in_a_stable_table():
    import paper_stability as ps

    assert ps.residue_bound(0.0, zero=True) == ps.residue_bound(5e-18, zero=True) == "below 1e-12"
    assert ps.residue_bound(0.0) == 0.0  # elsewhere an exact zero is a zero (a fraction of none)


def test_d3_exponent_tables_print_no_bare_zero_exponent():
    """Every exponent cell of B.1 is a number or the bound; an exact zero is the bound."""
    by_id = {c.id: c for c in _code_cells(_nb(SUPPORT_NB))}
    text = _out_text(by_id["tab-B-exponents_and_terms"])
    rows = [line for line in text.splitlines() if re.match(r"\| [a-z]", line)]
    exponent_rows = [r for r in rows if r.count("|") >= 4 and "term" not in r.lower()]
    assert exponent_rows
    cells = [c.strip() for r in exponent_rows for c in r.split("|")[2:-1]]
    assert "0" not in cells and "0.0" not in cells


def test_c_committed_output_is_current():
    """C is cheap to regenerate, so its committed outputs are compared with a re-run.

    Byte-equal in the environment of record; elsewhere the numbers of the printed tables agree
    within the stated tolerance and the one digest that follows the platform is not compared.
    """
    exact = exact_only("planted_table_sha256")
    rtol = listed()["planted_table_sha256"]["text_rtol"]
    for cell in _cells_of("F"):
        fn = re.search(r"import (\w+)", _src(cell)).group(1)
        committed, fresh = _out_text(cell), str(getattr(generate_model, fn)())
        if exact:
            assert committed == fresh, f"{cell.id}: {STALE}"
        else:
            ok = _same_text(_mask_exact_only(committed), _mask_exact_only(fresh), rtol)
            assert ok, f"{cell.id}: {STALE}"


def test_planted_table_agrees_with_the_reference_values():
    """The planted table's values, not its hash: within the stated tolerance of the reference."""
    entry = listed()["planted_table_sha256"]
    X, _ = generate_model.planted_table()
    ref = np.load(REFERENCE_FILE)["planted_X"]
    assert X.shape == ref.shape == (900, 4)
    np.testing.assert_allclose(X, ref, rtol=entry["values_rtol"], atol=entry["values_atol"])


def test_planted_example_is_reproducible_and_has_known_terms():
    X, info = generate_model.planted_table()
    X2, _ = generate_model.planted_table()
    assert (X == X2).all()
    assert info["exponents"].shape == (3, 4) and X.shape[1] == 4


# -- E: the proofs, compiled from the record

RECORD = ROOT / "derivation" / "proof_map_record.json"
_PROOF_CELLS = ("tab-E-how-to-read", "tab-E-proof-map", "tab-E-proofs-fit", "tab-E-proofs-solver",
                "tab-E-checker")  # fmt: skip


def _record():
    return json.loads(RECORD.read_text(encoding="utf-8"))


def _proof_text() -> str:
    return str(generate_proofs.proofs_fit()) + "\n\n" + str(generate_proofs.proofs_solver())


def test_appendix_b_headings_equal_the_records_results():
    expected = [
        f"L{lem['number']}. {res['name']}"
        for lem in sorted(_record()["lemmas"].values(), key=lambda lem: lem["number"])
        for res in lem["results"]
    ]
    heads = re.findall(r"^#### (.+)$", _proof_text(), re.M)
    assert heads == expected == generate_proofs.result_headings()
    assert len(heads) == sum(len(lem["results"]) for lem in _record()["lemmas"].values())


def test_every_step_tag_of_the_record_appears_once_in_a_proof_and_none_is_empty():
    text = _proof_text()
    steps = [st for lem in _record()["lemmas"].values() for st in lem["steps"]]
    assert len(steps) == sum(len(lem["steps"]) for lem in _record()["lemmas"].values())
    for st in steps:
        assert text.count(f"| **{st['tag']}** |") == 1, st["tag"]
    rows = [ln for ln in text.splitlines() if ln.startswith("| **L")]
    assert len(rows) == len(steps)
    for row in rows:
        cells = [c.strip() for c in re.split(r"(?<!\\)\|", row)[1:-1]]
        assert len(cells) == 4 and all(cells), row[:60]


def test_proof_kinds_are_compiled_from_the_ledger_and_the_earlier_proofs():
    from derivation.axioms import AXIOMS

    text = _proof_text()
    for lem in _record()["lemmas"].values():
        for st in lem["steps"]:
            row = next(ln for ln in text.splitlines() if ln.startswith(f"| **{st['tag']}** |"))
            kind = row.split(" | ")[1]
            if st["kind"] == "computed":
                assert kind.strip() == "computed"
            elif st["kind"] == "axiom":
                for name in st["applies"]:
                    assert f"by declared axiom **{name}**" in kind
                    assert generate_proofs._esc(AXIOMS[name].statement).replace("|", "\\|") in kind
                    if AXIOMS[name].citation:
                        assert (
                            generate_proofs._esc(AXIOMS[name].citation).replace("|", "\\|") in kind
                        )
                    assert (
                        "declared at [line " in kind
                    )  # the import line, the declaration's address
            else:
                for key in st["results"]:
                    assert f"by proved result **L{key[1:].split('_')[0]}**" in kind
                    assert "imported at [line " in kind


def test_appendix_b_names_each_results_file_statement_and_hypotheses():
    text = _proof_text()
    for file, lem in _record()["lemmas"].items():
        assert text.count(f"**File.** [{file}]") == len(lem["results"]), file
        assert generate_proofs._esc(generate_proofs._statement(file)[:60]) in text
    assert "carried by the symbols" in text  # a hypothesis of a statement is quoted, not dropped


def test_appendix_b_lines_resolve_to_the_scripts_text():
    """A step's link points at the line of the script that holds the step's code."""
    for file, lem in _record()["lemmas"].items():
        lines = (ROOT / "derivation" / file).read_text(encoding="utf-8").splitlines()
        tags = generate_proofs._tag_lines(file)
        assert set(tags) == {st["tag"] for st in lem["steps"]}
        for st in lem["steps"]:
            first = st["code"].splitlines()[0].strip()
            line = lines[tags[st["tag"]] - 1].replace('"', "'")  # the record is ast.unparse
            assert first.split()[0].replace('"', "'") in line, (st["tag"], first)


def test_appendix_b_is_deterministic_and_reads_without_writing():
    derivation = sorted((ROOT / "derivation").glob("*"))
    before = {p: p.stat().st_mtime_ns for p in derivation if p.is_file()}
    first = _proof_text() + str(generate_proofs.checker())
    assert first == _proof_text() + str(generate_proofs.checker())
    assert before == {p: p.stat().st_mtime_ns for p in derivation if p.is_file()}


def test_appendix_b_closes_with_the_checkers_table():
    text = str(generate_proofs.checker())
    assert "uv run python -m derivation.proofmap" in text
    digest = __import__("hashlib").sha256(RECORD.read_bytes()).hexdigest()
    lemmas = _record()["lemmas"].values()
    n_steps = sum(len(lem["steps"]) for lem in lemmas)
    assert digest in text and f"| Lemma files, steps | {len(lemmas)}, {n_steps} |" in text
    assert text.count("lemma_") >= len(lemmas)


def test_appendix_b_committed_output_is_current():
    for cell in _code_cells(_nb(SUPPORT_NB)):
        if cell.id in _PROOF_CELLS:
            fn = re.search(r"import (\w+)", _src(cell)).group(1)
            assert _out_text(cell) == str(getattr(generate_proofs, fn)()), f"{cell.id}: {STALE}"


# -- Figure 1

# exact only in the environment of record (the image): macOS gives d3a29d79..., the maths library
FIGURE1_HASH = "ec68f512678834a904ff18c5ed78e59db197851b4e2f93091959079a44f79e45"


def test_figure1_files_exist_and_the_data_hash_is_pinned():
    from figures import figure1

    assert (PAPER / "figures" / "figure1.png").stat().st_size > 10_000
    assert (
        (PAPER / "figures" / "figure1.svg")
        .read_text(encoding="utf-8")
        .startswith(("<?xml", "<svg"))
    )
    data = figure1.figure1_data()
    assert data["u"].shape == (253, 2)
    assert figure1.data_hash(data) == figure1.data_hash()  # deterministic within a platform
    if exact_only("figure1_data_hash"):
        assert figure1.data_hash(data) == FIGURE1_HASH
    else:  # the same data, on their values, within the stated tolerance of the reference arrays
        entry, ref = listed()["figure1_data_hash"], np.load(REFERENCE_FILE)
        for key in ("u", "logV", "Z", "corners", "W", "BETA"):
            np.testing.assert_allclose(
                data[key], ref[f"figure1_{key}"], rtol=entry["values_rtol"],
                atol=entry["values_atol"], err_msg=key,
            )  # fmt: skip
        assert (data["term"] == ref["figure1_term"]).all()
        assert data["design"] == int(ref["figure1_design"])


def test_figure1_has_three_panes_with_the_registers_words_and_writes_nothing(tmp_path, monkeypatch):
    import matplotlib.pyplot as plt
    from figures import figure1

    monkeypatch.chdir(tmp_path)
    fig = figure1.figure1()
    try:
        titles = [ax.get_title(loc="left") for ax in fig.axes]
        assert len(fig.axes) == 3
        assert "fitted reference surface" in titles[0]
        assert "supporting envelope" in titles[1] and "terms" in titles[2]
        words = " ".join(t.get_text() for ax in fig.axes for t in ax.texts)
        assert "energy" in words and "differential" in words and "term 1" in words
    finally:
        plt.close(fig)
    assert list(tmp_path.iterdir()) == []


def test_figure1_is_not_in_the_paper_and_the_index_page_no_longer_shows_it():
    """The supervisor's ticket (WP10, 2026-11-09): the three-pane figure leaves the paper's body
    and stays on the index page as the high-level story arc; its generator and files stay, and the
    site assembler copied the file. WP51: the index page's how section shows the slices
    figure instead, so the assembler no longer copies it; the file and its generator stay."""
    nb = _nb(PAPER_NB)
    assert not [c for c in nb.cells if c.id.startswith("fig-schematic")]
    assert "figure1" not in _markdown(nb) + " ".join(_src(c) for c in _code_cells(nb))
    assert "fig-trade-space" not in _markdown(nb)
    assert (PAPER / "figures" / "figure1.png").is_file()
    assembler = (ROOT / "scripts" / "assemble_site.py").read_text(encoding="utf-8")
    assert "figure1" not in assembler.replace("Figure 1", "")  # no consumer on the page


# -- F and B: the completions


def test_each_attribute_has_a_producer_that_exists_in_its_file():
    import case

    assert set(generate_model.PRODUCERS) == set(case.CUBESAT.attributes)
    for file, name, _ in generate_model.PRODUCERS.values():
        assert name in (ROOT / "examples" / "adcs" / file).read_text(encoding="utf-8"), name


def test_the_metric_rule_reproduces_the_table_of_metrics():
    import case
    import numpy as np

    st = case.load_study("primary", n_max=60)
    pre = st.preconditioner
    a = st.feasible[list(st.attrs)].to_numpy(float)
    o = np.array([case.CUBESAT.orientation[x] for x in st.attrs], float)
    m = np.exp((o * np.log(a + pre.shift_) - pre.log_offset_) / pre.log_scale_)
    assert np.allclose(m, st.M)
    assert "m_j = exp((o_j log(a_j + s_j) - c_j) / k_j)" in str(generate_model.metric_table(n=2))


@pytest.mark.parametrize("regime", ["primary", "stock"])
def test_the_regimes_contending_set_is_the_unique_lp_optimum_not_a_solver_choice(regime):
    """R1 checked on the case before the n-lemma is printed (the regimes sentence of Section 7):
    the exact-maximum fit's optimal face is one point, so its support, the contending set, does
    not depend on the solver's choice among optimal vertices.

    The certificate reads the LP's own primal-dual pair ``(w, p, beta)`` on the regime's
    log-metrics. (i) The reduced costs ``g_j - beta``, ``g = U^T p`` the balanced point, vanish on
    the support and are strictly positive off it, so by complementary slackness every primal
    optimum has ``w_j = 0`` off the support. (ii) Every row with a positive dual is tight, and
    every primal optimum is tight on those rows. (iii) The active system ``[U_P[:, S], -1; 1^T, 0]``
    has full column rank, so (i) and (ii) leave one point. The two HiGHS methods return that
    support, and the K = 1 trade-off report of record prints it: a 5-lemma in both regimes.
    """
    import case
    from scipy.optimize import linprog

    from tradespace import solvers

    st = case.load_study(regime)
    U = np.log(st.M)
    N, d = U.shape
    r = solvers.solve_lp(U, 0.0)
    assert r.success
    S = np.flatnonzero(r.w > 1e-9)
    reduced = U.T @ r.p - r.beta  # (i): the balanced point against the level
    assert np.all(np.abs(reduced[S]) < 1e-6)  # equal gradients on the support (L3.22)
    assert np.all(reduced[np.setdiff1d(np.arange(d), S)] > 1e-4)  # strict off it
    P = np.flatnonzero(r.p > 1e-9)  # (ii): the rows that carry the support weights
    assert np.all(U[P] @ r.w >= r.beta - 1e-7) and r.p[P].sum() == pytest.approx(1.0)
    A = np.block(
        [[U[np.ix_(P, S)], -np.ones((P.size, 1))], [np.ones((1, S.size)), np.zeros((1, 1))]]
    )
    assert np.linalg.matrix_rank(A) == S.size + 1  # (iii): one point on the optimal face
    c, A_ub = np.zeros(d + 1), np.hstack([U, -np.ones((N, 1))])
    c[-1], A_eq = 1.0, np.hstack([np.ones((1, d)), np.zeros((1, 1))])
    for method in ("highs-ds", "highs-ipm"):
        res = linprog(c, A_ub=A_ub, b_ub=np.zeros(N), A_eq=A_eq, b_eq=[1.0],
                      bounds=[(0, None)] * d + [(None, None)], method=method)  # fmt: skip
        assert np.array_equal(np.flatnonzero(res.x[:d] > 1e-9), S), method
    rep = case._reports(st, case.fit_study(st))[0]
    assert np.array_equal(rep.contending_set, S) and rep.n_lemma == S.size
    assert S.size == {"primary": 7, "stock": 8}[regime]  # the thirteen-metric data of the WP30 gate


def test_c_has_the_metric_table_and_the_sources_and_d_has_the_extended_tables():
    sections = _appendix_cells(_nb(SUPPORT_NB))
    ids_c = {c.id for c in sections["F"]}
    assert {"tab-F-attribute_sources", "tab-F-metric_table"} <= ids_c
    ids_d = {c.id for c in sections["B"]}
    assert (
        "tab-B-sensitivity_variants" in ids_d
    )  # WP57c: the old D.1 and D.6 to the supplement, the old D.7 into B.12
    assert not ids_d & {"tab-B-refits_by_category", "tab-B-candidate_designs",
                        "tab-B-temperature_selection", "tab-B-k_diagnostics",
                        "tab-B-conditioning_diagnostic"}  # fmt: skip


def test_the_c_and_d_additions_are_current_and_cite_the_labels():
    for cell in _cells_of("B"):
        if cell.id in {"tab-B-sensitivity_variants", "tab-B-termination_records"}:
            assert "cubesat-primary" in _out_text(cell), cell.id


# ---- the register of prior art -----------------------------------------------------------------


def test_prior_art_entries_have_four_nonempty_fields_and_unique_ids():
    """R-27: every entry has the four fields; the third is never empty."""
    entries = generate_prior_art.entries()
    assert len(entries) >= len(OUTLINE_FAMILIES)
    assert len({e["id"] for e in entries}) == len(entries)
    for e in entries:
        for f in PRIOR_FIELDS:
            assert e.get(f), (e["id"], f)
        assert e["differs"].strip() and e["group"].strip() and e["family"].strip()
        assert isinstance(e["cites"], list) and e["cites"]


def test_prior_art_cites_resolve_in_the_bibliography():
    keys = _bib_keys()
    for e in generate_prior_art.entries():
        missing = [k for k in e["cites"] if k not in keys]
        assert not missing, (e["id"], missing)


def test_every_family_of_the_outline_has_an_entry():
    """R-9: a row per family of the outline."""
    assert {e["id"] for e in generate_prior_art.entries()} >= OUTLINE_FAMILIES


def test_nearest_neighbours_carry_a_plain_why_not_just_sentence():
    entries = {e["id"]: e for e in generate_prior_art.entries()}
    assert {i for i, e in entries.items() if e.get("nearest")} == NEAREST
    for i in NEAREST:
        sentence = entries[i]["why_not_just"]
        assert sentence.startswith("This is not just "), i
        assert sentence.endswith("."), i


def test_prior_art_says_nothing_is_novel_first_or_new():
    """R-9, R-27: no 'novel', 'first' or 'new' in the register or in section 2's table."""
    for e in generate_prior_art.entries():
        for f in (*PRIOR_FIELDS[:3], "why_not_just"):
            m = WORDS_BANNED_IN_PRIOR_ART.search(str(e.get(f, "")))
            assert not m, (e["id"], f, m and m.group(0))
    for text in (str(generate_prior_art.family_table()), str(generate_prior_art.register())):
        assert not WORDS_BANNED_IN_PRIOR_ART.search(text)


def test_every_differs_cell_has_this_work_as_its_subject():
    """WP35 Q2: Table 1 and Appendix A read down the "differs" column in one voice. Every full
    cell and every short phrase opens "This work", so no cell can be read as the other method's
    property; what a family does, including its limits, is in `does`."""
    for e in generate_prior_art.entries():
        assert e["differs"].startswith("This work"), (e["id"], "differs")
        if e.get("section2"):
            assert e["short"]["differs"].startswith("This work"), (e["id"], "short.differs")
        for f in ("does", "shares"):
            assert not e[f].startswith("This work differs"), (e["id"], f)
    ids = {e["id"] for e in generate_prior_art.entries()}
    assert {"kernel-pca", "horopca"} <= ids and "kernel-hyperbolic-pca" not in ids


def test_section2_table_is_a_subset_of_the_register_with_the_same_wording():
    """R-27: section 2's rows are the flagged entries, and each cell's phrase is an extract of the
    Appendix A field of the same name, word for word.

    The requirement's intent is one source with one wording. The table used to print the three
    sentences in full, five columns of them in a narrow column two screens tall; it now prints a
    short phrase per cell (``short`` in ``prior_art.yaml``) and Appendix A the sentences, so the
    test asks that each phrase occurs in the field it abbreviates, and that the field is in the
    register verbatim. Decided by the driver (WP10, table 1 made readable)."""
    entries = generate_prior_art.entries()
    flagged = [e for e in entries if e.get("section2")]
    assert 0 < len(flagged) < len(entries) or len(flagged) == len(entries)
    table = str(generate_prior_art.family_table())
    register = str(generate_prior_art.register())
    for e in flagged:
        assert set(e["short"]) == {"does", "shares", "differs"}, e["id"]
        for field, phrase in e["short"].items():
            phrase = " ".join(phrase.split())
            assert phrase and phrase in e[field], (e["id"], field)
            assert len(phrase.split()) <= 12, (e["id"], field)  # a phrase, not a sentence
            assert phrase in table and e[field] in register, (e["id"], field)
        assert e["family"] in table
    for e in entries:
        assert e["differs"] in register, e["id"]
        if not e.get("section2"):
            assert e["family"] not in table


def test_register_has_every_entry_grouped_by_family():
    text = str(generate_prior_art.register())
    for e in generate_prior_art.entries():
        assert f"**{e['family']}**" in text
        assert text.count("What this work does differently, extends or adds") == len(
            generate_prior_art.entries()
        )


def test_family_table_cites_are_author_year_links_to_the_reference_list():
    """The table is an output cell, which the site does not parse for citations: each key is an
    author-year link to its entry in the reference list, and the hidden cell cites every key so
    that the list holds the entry."""
    table = str(generate_prior_art.family_table())
    assert "[@" not in table
    for e in generate_prior_art.entries():
        if not e.get("section2"):
            continue
        for key in e["cites"]:
            label = generate_prior_art.author_year(key)
            assert re.search(rf'<a href="#cite-{key}"[^>]*>{re.escape(label)}</a>', table), key
            assert re.fullmatch(r"[^\d]+ \d{4}|[^\d]+ n\.d\.", label), label
    assert "../#cite-" in str(generate_prior_art.register())  # the register is on the other page
    hidden = next(c for c in _nb(PAPER_NB).cells if c.get("id") == "nocite-prior-art")
    assert hidden.metadata["tags"] == ["remove-cell"]
    assert _src(hidden) == generate_prior_art.nocite(), "re-run the sync: " + STALE
    assert set(generate_prior_art.all_cited_keys()) <= _bib_keys()


def test_cells_whose_output_is_embedded_are_removed_from_the_page():
    """A cell that is embedded (``#id`` of a figure or table directive) is tagged ``remove-cell``:
    with only ``remove-input`` the page showed each of its outputs twice."""
    nb = _nb(PAPER_NB)
    embedded = set(re.findall(r"\{(?:embed|figure)\} #([\w-]+)", _markdown(nb)))
    assert len(embedded) >= 3  # two figure cells and the family table (Figure 9 went: S-3, R-10)
    cells = {c.id: c for c in _code_cells(nb)}
    for label in embedded:
        assert "remove-cell" in cells[label].metadata.get("tags", []), label
    # an embedded table copies the whole cell: its input is dropped by the directive's option
    for label in (c for c in embedded if c.startswith("tab-")):
        assert re.search(rf":::\{{embed\}} #{label}\n:remove-input: true\n", _markdown(nb)), label


def test_the_candidates_paragraph_is_cut_and_the_table_stays_in_appendix_d():
    """Change request 14 moved Table 2 to the old D.7; WP39 D-5 cut the paragraph and its sentence
    from Section 9 (the hand-named candidates all miss the thresholds; the shortlist of the decision
    is the case's concrete designs). The old D.7 kept the table and its sentence, and nothing
    points to a removed label."""
    import generate_findings as gf

    paper_ids = {c.id for c in _nb(PAPER_NB).cells}
    assert not paper_ids & {"sec-case-analysis-4", "cand-table", "num-candidates", "tab-candidates"}
    assert "Candidates." not in _section("Case analysis")
    assert not hasattr(gf, "candidates_sentence")
    # WP57c: the old D.7 merged into B.12; the candidates' sentence is generated under the design
    # sets
    assert "tab-B-candidate_designs" not in {c.id for c in _cells_of("B")}
    assert "candidates, fast_effort_hungry" in _cell_out(SUPPORT_NB, "tab-B-design_sets_comparison")


def test_prior_art_committed_outputs_are_current():
    paper = {c.id: c for c in _code_cells(_nb(PAPER_NB))}
    assert _out_text(paper["tab-families"]) == str(generate_prior_art.family_table()), STALE
    reg = next(c for c in _code_cells(_nb(SUPPORT_NB)) if c.id == "tab-A-register")
    assert _out_text(reg) == str(generate_prior_art.register()), STALE


def test_section2_distinguishes_horopca_in_one_paragraph():
    """WP35 R-1, R-7: one paragraph on HoroPCA, closest in setting and farthest in what is
    estimated; it borrows setting, interface and PCA as a downstream step; it does not call this
    work a PCA, nor HoroPCA a kernel method. The body defines "hyperbolic" once, in Definitions;
    elsewhere the word is a pointer."""
    s2 = _section("Prior art")
    paras = [p for p in s2.split("\n\n") if "HoroPCA" in p]
    assert len(paras) == 1 and paras[0].startswith("**HoroPCA.**")
    p = paras[0]
    for phrase in (
        "closest existing analog in setting",
        "the farthest in what is estimated",
        "is not a PCA of any kind",
        "downstream step",
    ):
        assert phrase in p, phrase
    # WP35 amendment 1: the paragraph points at Appendix C and says what it tests
    assert (
        "recovered the planted trade-offs only where they were the direction of largest spread" in p
    )
    assert "{ref}`Appendix C <appendix-c>`" in p and "Appendix A" not in p
    assert "kernel" not in p.lower()
    assert "unrelated" not in s2 and "Färe" not in s2  # the two caveats are pointers or gone
    assert s2.count("hyperbolic") == 1  # HoroPCA's own space; the word is defined in Definitions
    body = _markdown(_nb(PAPER_NB))
    assert body.count("rectangular hyperbola") == 1 and "level curves" in body
    yml = yaml.safe_load((PAPER / "myst.yml").read_text(encoding="utf-8"))
    assert (
        yml["project"]["title"]
        == "Scaling Decision Analysis with Hyperbolic Trade Space Identification"
    )


# ---- Appendix C: the HoroPCA comparison as a tested hypothesis (WP35, amendment 1) ---------------

SPIKE_H = ROOT / "work-packages" / "WP35-rounds" / "spike-h"
HYPOTHESIS_COMMIT = "830cf54"


def _record_h() -> dict:
    return json.loads((SPIKE_H / "results.json").read_text(encoding="utf-8"))


def _table_rows(text: str) -> list[list[str]]:
    lines = [ln for ln in text.splitlines() if ln.startswith("|")][2:]
    return [[x.strip() for x in ln.strip("|").split("|")] for ln in lines]


def _expected_verdict(arm: str, x: float, share: dict) -> str:
    """The pre-registered rules of ``hypothesis.md``, written out cell by cell and independent of
    the generator's rule table: the verdict and the parts the cell tests."""
    held, parts = [], []
    if arm in "AB":
        parts.append("H1")
        held.append(share["ours"] >= 0.9)
    if arm == "A" and x >= 2:
        parts.append("H2")
        held += [share[m] >= 0.9 for m in ("pca", "h25", "h1")]
    if arm == "A" and x <= 0.5:
        parts.append("H2")
        held += [share[m] <= 0.1 for m in ("pca", "h25", "h1")]
    if arm == "B" and x == 0.9:
        parts.append("H3")
        held += [share["pca"] <= 0.2, share["ours"] >= 0.9]
    if arm == "C":
        parts.append("H4")
        held.append(share["ours"] <= 0.2)
        if x == 2:
            held.append(share["pca"] >= 0.9)
    verdict = "survives" if all(held) else "refuted"
    return f"{verdict} ({', '.join(dict.fromkeys(parts))})" if parts else "no prediction"


def test_the_pre_registered_rates_are_those_of_the_hypothesis_file():
    """WP35 RA-2: the rates and settings the generator applies (``RATES``) are the numbers
    ``hypothesis.md`` committed at 830cf54 states, and the commit is the file's first."""
    text = " ".join((SPIKE_H / "hypothesis.md").read_text(encoding="utf-8").split())
    for phrase in (
        "recovery rate is below 0.9",
        "(rate at least 0.9)",
        "(rate at most 0.1)",
        "rate at t = 0.9 above 0.2",
        "this work's rate above 0.2 in either cell",
        "is at least 0.9",
        "rho >= 2",
        "rho <= 0.5",
        "t in {0, 0.3, 0.6, 0.9}",
        "rho in {4, 2, 1, 0.5, 0.25}",
    ):
        assert phrase in text, phrase
    r = generate_prior_art.RATES
    assert r == {
        "high": 0.9,
        "low": 0.1,
        "pca_far": 0.2,
        "no_edge": 0.2,
        "rho_high": 2.0,
        "rho_low": 0.5,
        "t_far": 0.9,
    }
    log = subprocess.run(
        ["git", "log", "--format=%H", "--", "work-packages/WP35-rounds/spike-h/hypothesis.md"],
        capture_output=True, text=True, cwd=ROOT,
    ).stdout.split()  # fmt: skip
    if log:  # a checkout with history; the file was committed once, at the pre-registration
        assert log[-1].startswith(HYPOTHESIS_COMMIT)


def test_the_hypothesis_table_equals_the_record_cell_by_cell():
    """WP35 RA-2: the table the generator prints has one row per cell of arms A, B and C, in the
    record's order, each count read here from ``results.json`` independently of the generator, the
    verdict from the pre-registered rules recomputed here, then the verdict on the whole."""
    record = _record_h()
    cells = {k: v for k, v in record["cells"].items() if k[0] in "ABC"}
    assert len(cells) == 11 and all(v["n"] == 6 for v in cells.values())
    rows = _table_rows(str(generate_prior_art.horopca_hypothesis_table()))
    assert len(rows) == len(cells) + 1
    for row, (key, c) in zip(rows, cells.items(), strict=False):
        arm, setting = key.split("/")
        x = float(setting.removeprefix("rho").removeprefix("t"))
        n = c["n"]
        share = {
            "ours": c["ours_rec"] / n,
            "pca": c["pca_pc1_rec"] / n,
            "h25": c["horo_R0.25_k1"]["best_rec"] / n,
            "h1": c["horo_R1.0_k1"]["best_rec"] / n,
        }
        verdict = _expected_verdict(arm, x, share)
        symbol = "t" if arm == "B" else "\u03c1"
        assert row == [
            verdict,
            f"{arm}, {symbol} = {x:g}",
            f"{c['ours_rec']}/{n}",
            f"{c['pca_pc1_rec']}/{n}",
            f"{c['horo_R0.25_k1']['best_rec']}/{n}, {c['horo_R1.0_k1']['best_rec']}/{n}",
        ], key
    assert rows[-1] == ["survives", "All parts", "", "", ""]  # every pre-registered part survived
    assert rows[0][0].startswith("survives") and "refuted" not in " ".join(r[0] for r in rows)


def test_a_cell_that_breaks_a_refutation_condition_is_marked_refuted():
    """The verdict is computed, not typed: perturb the record and the table says so."""
    record = _record_h()
    record["cells"]["A/rho2.0"]["pca_pc1_rec"] = 5  # PCA at rho = 2 below 0.9 refutes H2
    record["cells"]["C/rho0.5"]["ours_rec"] = 2  # this work above 0.2 without an edge refutes H4
    by_cell = {r["cell"]: r for r in generate_prior_art.horopca_verdicts(record)}
    assert by_cell["A/rho2.0"]["verdict"] == "refuted"
    assert by_cell["C/rho0.5"]["verdict"] == "refuted"
    assert by_cell["A/rho4.0"]["verdict"] == "survives"
    parts = generate_prior_art.hypothesis_parts(list(by_cell.values()))
    assert parts == {"H1": "survives", "H2": "refuted", "H3": "survives", "H4": "refuted"}


def test_the_threshold_and_the_chance_rates_are_the_records():
    """WP35 RA-2: 0.9 and the two chance rates (0.037, 0.152) beside it are read from the file."""
    record = _record_h()
    assert (record["threshold"], round(record["chance_direction"], 3)) == (0.9, 0.037)
    assert round(record["chance_simplex"], 3) == 0.152
    sentence = str(generate_prior_art.horopca_threshold_sentence())
    assert "0.9" in sentence and "0.037" in sentence and "0.152" in sentence


def test_the_sentences_that_state_counts_match_the_record():
    """The two sentences on the smallest-variance component and the contrast sentence: the counts
    are the record's, recounted here."""
    cells = {k: v for k, v in _record_h()["cells"].items() if k[0] in "ABC"}
    last = {k: v["pca_last_rec"] for k, v in cells.items()}
    assert {k for k, v in last.items() if v} == {"A/rho0.25", "B/t0.9"}
    assert last["A/rho0.25"] == last["B/t0.9"] == 5 and sum(last.values()) == 10
    slab = str(generate_prior_art.horopca_slab_sentences())
    assert "5 of 6 tables" in slab and "none of the other nine cells" in slab
    contrast = str(generate_prior_art.horopca_contrast_sentence())
    a, c = cells["A/rho2.0"], cells["C/rho2.0"]
    assert (a["ours_rec"], c["ours_rec"], a["pca_pc1_rec"], c["pca_pc1_rec"]) == (6, 0, 6, 6)
    assert "from 6 of 6 tables to 0 of 6" in contrast and "leaves PCA at 6 of 6" in contrast


def test_the_design_constants_of_appendix_h_are_the_pre_registered_ones():
    """The design paragraph's numbers (four metrics, 300 rows, 30 percent on the edge, six tables,
    five restarts, the ranges of rho and t) are those of ``hypothesis.md``, and the draft and the
    notebook state them."""
    text = " ".join((SPIKE_H / "hypothesis.md").read_text(encoding="utf-8").split())
    for phrase in (
        "d = 4 metrics, n = 300 rows, 6 table seeds per cell",
        "30 percent of rows",
        "5 random restarts",
        "rho in {4, 2, 1, 0.5, 0.25}",
        "t in {0, 0.3, 0.6, 0.9}",
        "rho in {2, 0.5}",
    ):
        assert phrase in text, phrase
    # the spike's dated draft keeps the id the appendix had then
    draft = (SPIKE_H / "h-sections.md").read_text(encoding="utf-8")
    design = draft.split("=== app-H-2 | markdown", 1)[1].split("=== ", 1)[0]
    for phrase in (
        "Four metrics, 300 rows",
        "30 percent of the rows",
        "six tables per setting",
        "five restarts",
        "from 0.25 to 4",
        "0 to 0.9",
        "2 or 0.5",
    ):
        assert phrase in design, phrase
    h2 = next(c for c in _appendix_cells(_nb(SUPPORT_NB))["C"] if c.id == "app-C-2")
    assert all(p in _src(h2) for p in ("Four metrics, 300 rows", "six tables per setting"))


H5_NOTE = "notes/directions/wp35-horopca-formalism-and-solvers.md"
H5_NOTE_URL = "https://github.com/DynamicalSystemsGroup/tradespace/blob/main/" + H5_NOTE


def _h5_note() -> str:
    return " ".join((ROOT / H5_NOTE).read_text(encoding="utf-8").split())


def _appendix_h_cells():
    return _appendix_cells(_nb(SUPPORT_NB))["C"]


def _appendix_h_prose() -> str:
    """The prose of Appendix C as the reader meets it: its Markdown and its generated sentences
    (cells ``sent-C-*``), not its table."""
    parts = []
    for c in _appendix_h_cells():
        if c.cell_type == "markdown":
            parts.append(_src(c))
        elif c.id.startswith("sent-C-"):
            parts.append(_out_text(c))
    return "\n\n".join(parts)


def test_appendix_h_has_its_four_sections_in_the_supervisors_order():
    """WP35 RA-1: hypothesis (with its refutation conditions), experiment, results, what the table
    shows; how the formalism and the solvers differ is a note of the repository (WP57d), cited in
    one line at the end of C.4."""
    heads = [
        _src(c).split("\n")[1] if _src(c).startswith("(sub-c-") else None
        for c in _appendix_h_cells()
        if c.cell_type == "markdown"
    ]
    heads = [h for h in heads if h]
    assert [h.split(" ", 2)[0:2] for h in heads] == [["###", f"C.{i}"] for i in range(1, 5)]
    assert [h.split(" ", 2)[2].split()[0] for h in heads] == ["The", "The", "Results", "What"]
    assert heads[0].endswith("what would refute it")
    last = _src(_appendix_h_cells()[-1])
    assert last.rstrip().endswith(f"({H5_NOTE_URL}).") and last.count(H5_NOTE_URL) == 1
    assert (ROOT / H5_NOTE).is_file()


H_CEILING = 920 - 169
"""Appendix C's ceiling after WP57d's cut row (``paper/length_ledger.toml``)."""


def test_appendix_h_is_within_its_ledger_ceiling():
    """WP35 amendment 1: the visible prose (Markdown, the caption, the generated sentences; not the
    table) is at most the ceiling the ledger fixes: 920 words (900, raised by the wording unit's row
    on the assistant's word, 3fb77e6), lowered by WP57d's cut row (the Job block, C.1's sentence
    about the appendix, the old H.5), raised again only by a new row and the assistant's word."""
    _, ceilings = ledger_ceilings()
    assert ceilings["Appendix C"] == H_CEILING
    assert rendered_words(_appendix_h_prose()) <= ceilings["Appendix C"]


def test_appendix_h_prints_no_typed_number_in_its_table_and_sentence_cells():
    """WP35 RA-2: the table and the sentences of results are generated: their cells hold one call
    and no digit, and their committed outputs equal what the generator prints now."""
    cells = {c.id: c for c in _code_cells(_nb(SUPPORT_NB)) if c.id.endswith("hypothesis")
             or c.id.startswith("sent-C-")}  # fmt: skip
    assert "tab-C-hypothesis" in cells and len(cells) >= 5
    for cid, c in cells.items():
        calls = [ln for ln in _src(c).splitlines() if ln and not ln.startswith("from ")]
        assert len(calls) == 1 and not re.search(r"\d", calls[0]), cid
        fn = re.match(r"(horopca_\w+)\(\)", calls[0]).group(1)
        assert _out_text(c).strip() == str(getattr(generate_prior_art, fn)()).strip(), (cid, STALE)


def test_appendix_h_says_where_each_term_is_first_defined_and_points_at_d16():
    """WP35 RA-4, RA-10: PCA, |cos|, R, frame and horosphere each have a plain line at first use;
    the chain to B.11 is in words with its pointer."""
    text = _appendix_h_prose()

    def first(term):
        m = re.search(term if term.startswith("\\b") else re.escape(term), text)
        return m.start()

    assert "principal component analysis (PCA)" in text and first("principal component") < first(
        r"\bPCA\b"
    )
    assert "(|cos|, agreement of directions ignoring sign)" in text
    assert first("|cos|") < first("threshold")
    assert "distance R from the centre" in text and first("R from") < first("R = 3")
    note = _h5_note()  # the old H.5's terms moved with it (WP57d)
    assert (
        "frame, k orthonormal directions" in note
        and "horospheres (the curved counterparts of hyperplanes" in note
    )
    assert "{ref}`Appendix B.11 <sub-b-11>`" in " ".join(_src(c) for c in _appendix_h_cells())
    assert "was not run" in text
    assert "second embedding was not run" in text and "not tree-like" in text
    assert "The embedding is part of the treatment" in text  # decision 1862491, boundary (a)
    assert text.index("(a) The embedding") < text.index("(b) The tables") < text.index("(c) Six")
    assert "every 6/6 is a count" in text and "not a performance benchmark" not in text  # C591
    assert "variance ranking alone does not identify" in text
    assert "cannot pick" not in text and "not a rescue" not in text


def test_appendix_h_wording_unit_defines_its_terms_and_states_counts():
    """WP35 wording unit (FW-1 to FW-13, FW-15 to FW-20; FW-14 not applied): rho, t, the depth
    direction, the generator, the ball and the threshold are defined at first use; H1 to H4 are
    counts of the six tables; the verdict sentence names no total; Section 2 and Appendix C use
    one term (prospectively specified) for one thing."""
    text = _appendix_h_prose()
    record = _record_h()
    assert f"reaches the threshold, {record['threshold']:g}" in text  # FW-8
    assert "before any table of this experiment existed" in text  # FW-2
    assert (
        "the standard deviation along the edge's vector (the planted exponents) over that" in text
    )
    assert "along the largest direction orthogonal to it" in text  # FW-3
    assert (
        "moves the vector by a fraction t from the depth direction of the package's generator"
        in text
    )
    assert "(equal exponents, where it puts its spread)" in text  # FW-4
    assert "removes the edge and still scores the same vector" in text  # FW-5
    assert "the rows spread symmetrically along the vector" in text
    assert "a ball (the disk that models hyperbolic space)" in text  # FW-9
    assert "the exponential map at the origin into the ball" in text  # FW-10
    assert (
        "30 percent of the rows on the edge" in text
    )  # FW-19, the second boundary with its number
    assert "(its fourth)" in text and "analyst with other domain" not in text  # FW-13, FW-20
    assert "linear program" not in text and "sequential quadratic" not in text  # FW-17
    note = _h5_note()  # the old H.5 moved to the repository's note (WP57d), its wording kept
    assert "shortfall from the best value" in note and "how far its loss is" in note  # FW-16
    assert "chami2021horopca" in note and "its loss)" in note
    assert "c9a9996 (Adam, random starts)" in note
    conditions = str(generate_prior_art.horopca_conditions())
    n = _record_h()["cells"]["A/rho4.0"]["n"]
    assert n == 6 and "refuted by any cell under 6/6" in conditions  # FW-6
    assert (
        "at most 1/6" in conditions and "in 0/6" in conditions and "recover it in 6/6" in conditions
    )
    assert "HoroPCA (R = 0.25, R = 1)" in conditions  # FW-7
    assert "at least" not in conditions and "of the tables" not in conditions  # counts, no shares
    verdict = str(generate_prior_art.horopca_verdict_sentence())
    assert verdict == "Every check in the 11 cells holds, so every part survives."  # FW-11
    caption = next(c for c in _appendix_h_cells() if c.id == "tab-C-hypothesis-caption")
    assert "H1 to H4 are listed in C.1; HoroPCA cells read R = 0.25, R = 1" in _src(
        caption
    )  # FW-12
    section2 = _section("Prior art")
    assert "prospectively specified test" in section2 and "pre-registered" not in section2  # FW-1
    prior = next(r for r in generate_prior_art.entries() if r["id"] == "horopca")
    assert (
        "on the synthetic tables of Appendix C, the leading components of PCA and HoroPCA"
        in " ".join(prior["differs"].split())
    )  # FW-15


FORBIDDEN_COMPARISON = ("worse", "poorer", "inferior", "outperform", "beats", "pca with a kernel")


def _forbidden_in(text: str) -> list[str]:
    low = text.lower().replace("not a pca of any kind", "")
    hits = [w for w in FORBIDDEN_COMPARISON if re.search(rf"\b{re.escape(w)}", low)]
    return hits + (
        ["calls this work a PCA"] if re.search(r"(this work|our method) is a pca", low) else []
    )


def test_no_sentence_says_horopca_is_worse_or_calls_this_work_a_pca():
    """WP35 RA-6 (default phrase list): Section 2's HoroPCA paragraph, and Appendix C once it is in
    the notebook, say what each method estimates and never rank them nor call this work a PCA or
    HoroPCA a kernel method."""
    paragraph = next(p for p in _section("Prior art").split("\n\n") if "HoroPCA" in p)
    assert _forbidden_in(paragraph) == []
    assert _forbidden_in("HoroPCA is worse at it; this work is a PCA; HoroPCA is PCA with a kernel")
    assert _forbidden_in(_appendix_h_prose()) == []
    assert "kernel" not in _appendix_h_prose().lower()


def test_the_source_map_names_the_hypothesis_table_and_its_record():
    """WP35 amendment 1 (v): the reproduction table reads the table's source from the map."""
    reads = generate_repro.READS_BY_CALL["horopca_hypothesis_table()"]
    assert reads == "work-packages/WP35-rounds/spike-h/results.json"
    assert (ROOT / reads).is_file()
    source = (PAPER / "generate_prior_art.py").read_text(encoding="utf-8")
    assert "def horopca_hypothesis_table" in source


def test_appendix_g_is_the_register_and_one_line_citing_the_reading_pass():
    """WP57a: the heading, A.1's heading, the register, one line naming the reading pass's file;
    no Job block, no scope sentence (queued for WP57d), no pointer cell, no A.2."""
    cells = _appendix_cells(_nb(SUPPORT_NB))["A"]
    assert [c.id for c in cells] == ["app-A", "app-A-1", "tab-A-register", "app-A-reading-pass"]
    text = "\n".join(_src(c) for c in cells if c.cell_type == "markdown")
    assert "not exhaustive" not in text and "A.2" not in text and "tested by experiment" not in text
    assert "paper/supplement/reading-pass.md" in _src(cells[-1])
    assert len(_src(cells[-1]).split()) <= 30


# ---- the main text: prose-dependent checks (WP10) -----------------------------------------------

BLOCK = re.compile(
    r":::\{prf:(theorem|lemma|proposition|corollary)\} ([^\n]*)\n:label: (\S+)\n(.*?)\n:::\n", re.S
)
BADGES = ("Derived", "Numerical", "Open")
# "however" left the pattern on 2026-11-15: his Section 1 sentence opens on it as a contrast,
# not a hedge (WP11-decisions.md, the PCA paragraph); the hedges the readers flagged were
# "caveat" and "note that".
HEDGES = re.compile(r"caveat|note that", re.I)


def _section(name: str) -> str:
    """The Markdown of the paper from heading ``## name`` up to the next ``## `` heading."""
    out, grab = [], False
    for c in _nb(PAPER_NB).cells:
        if c.cell_type != "markdown":
            continue
        text = _unlabel(_src(c))
        if text.startswith("## "):
            grab = text.startswith(f"## {name}")
        if grab:
            out.append(text)
    return "\n".join(out)


def _blocks():
    body = _markdown(_nb(PAPER_NB))
    return [(m.group(1), m.group(2), m.group(3), m.group(4)) for m in BLOCK.finditer(body + "\n")]


def test_no_shell_marker_remains_in_the_paper():
    assert SHELL not in _markdown(_nb(PAPER_NB))


def _prose_words(text: str) -> int:
    return len(re.sub(r"[#>*`:{}\[\]@|-]", " ", _rendered(text)).split())


def test_future_work_is_short_and_names_the_three_thrusts_in_the_abstracts_order():
    """WP54 R-3, R-4: under 250 words; what the release did, then the abstract's three directions
    in its order; no separate search section and no final remark."""
    text = _section("Future work")
    assert _prose_words(text) < 250
    assert "Final remark" not in text and "preliminary" not in text
    heads = re.findall(r"^\*\*([^*]+)\.\*\*", text, re.M)
    assert heads == ["Searching the design space", "Holes", "Formal verification and performance"]
    assert text.index("This release delivers") < text.index("**Searching")
    assert "submartingale" not in text  # the open point is in review/open-questions.md


def test_closing_section_is_short_and_calls_the_derivations_scripted_checks():
    """WP54 R-4: under 200 words; the lemma scripts are scripted checks, never machine-checked
    or formally verified (proof-conventions.md)."""
    text = _section("AI acknowledgement and Reproducibility")
    assert _prose_words(text) < 200
    assert "@zargham2026incose" in text and "supervisor-gated" in text and "appendix-h" in text
    assert not re.search(r"machine-checked|formally verified", text, re.I)
    assert "Reproducibility and your own case" not in _markdown(_nb(PAPER_NB))


def test_every_lemma_has_a_let_assume_then_block_with_its_proof_pointer():
    """R-17, R-18, WP55 G4: L1 to L17 once each (and L20, the noise corollary, after L6, and L21,
    the tension, after L7). Each result is "Let ... Assume ... Then ..." with its lemma label in the
    title and ends "Proof: Appendix E, Ln"; the Derived and Hypotheses labels, the sketches and the
    Script boxes are gone from the main text. The paper's order is the algorithm's (E-8): the
    alternation (L16) and Level 1 (L15) come before Lemma 1 (L12)."""
    blocks = _blocks()
    tags = [re.search(r"\(L(\d+)(?:, [^)]*)?\)\s*$", title).group(1) for _, title, _, _ in blocks]
    assert [int(t) for t in tags] == [
        1, 2, 3, 4, 5, 6, 20, 7, 21, 8, 9, 10, 11, 16, 15, 12, 13, 14, 14, 17,
    ]  # fmt: skip
    body = _markdown(_nb(PAPER_NB))
    scripts = {
        int(re.match(r"lemma_(\d+)_", p.name).group(1)): p
        for p in (ROOT / "derivation").glob("lemma_*.py")
    }
    for _kind, title, label, content in blocks:
        n = int(re.search(r"\(L(\d+)[,)]", title).group(1))
        flat = " ".join(content.split())
        assert re.match(r"Let ", flat), label
        assert " Assume " in flat or flat.count("Assume") >= 1, label
        assert " Then" in flat or "Then," in flat, label
        assert flat.rstrip().endswith(f"Proof: {{ref}}`Appendix E, L{n} <appendix-e>`."), label
        assert n in scripts and "def verify(" in scripts[n].read_text(encoding="utf-8"), label
    main = "\n".join(
        _section(n) for n in ("Preliminaries and notation", "Definitions", "Methods", "Results")
    )
    assert not re.search(r"\*\*(Derived|Numerical|Open)\.\*\*|\*Hypotheses\.\*", main)
    assert ":::{prf:proof} Sketch" not in body and ":::{admonition} Script" not in body
    kinds = [(k, int(re.search(r"\(L(\d+)[,)]", t).group(1))) for k, t, _, _ in blocks]
    assert kinds[6] == ("corollary", 20)
    assert kinds[13:] == [
        ("theorem", 16),
        ("theorem", 15),
        ("lemma", 12),
        ("lemma", 13),
        ("proposition", 14),
        ("corollary", 14),
        ("theorem", 17),
    ]  # E-8, and the soft-fit certificate (WP17) last


def test_assumptions_and_conditions_are_displayed_and_named_where_used():
    """WP55 G3: A1 to A3 are plain sentences of Section 3; A4 to A11 and R1 to R3 are each a named
    block in the paragraph of the procedure or result that uses them, never one list up front."""
    prelim = _section("Preliminaries and notation")
    for code in ("A1", "A2", "A3"):
        assert re.search(rf"\b{code}:", prelim), code
    where = {
        "Methods": ("A4", "A6", "A8"),
        "Results": ("A5", "A7", "A9", "A10", "A11", "R1", "R2", "R3"),
    }
    for section, codes in where.items():
        text = _section(section)
        for code in codes:
            assert re.search(rf":::\{{prf:assumption\}} {code}, ", text), (section, code)
    assert "A1: metrics are strictly positive. A2:" not in _markdown(_nb(PAPER_NB))


def test_the_open_questions_left_the_narrative_for_the_review_record():
    """WP55 G4, R-3: Q1 to Q4 are OQ-5 to OQ-8 of work-packages/review/open-questions.md; the
    results keep one pointer to the appendix section that records what is open."""
    body = _markdown(_nb(PAPER_NB))
    assert "### Open questions" not in body and "**Open.**" not in body
    for q in ("Q1", "Q2", "Q3", "Q4"):
        assert not re.search(rf"\b{q}:", body), q
    record = (ROOT / "work-packages" / "review" / "open-questions.md").read_text(encoding="utf-8")
    for n in (5, 6, 7, 8):
        assert f"## OQ-{n}." in record
    assert "records what the results leave open" in _section("Results")
    for section in ("Preliminaries and notation", "Definitions", "Methods", "Results"):
        text = _section(section)
        hits = re.findall(r"[^.]*(?:\bopen\b|not established|conjecture)[^.]*\.", text, re.I)
        assert all("Appendix G" in h for h in hits), (section, hits)


def test_no_section_3_to_6_reference_points_forward():
    """WP55 R-2: in Sections 3 to 6 a section, theorem or definition reference points back; the
    exceptions are equations and the proofs of Appendix E."""
    cells = _nb(PAPER_NB).cells
    seen: set[str] = set()
    inside = False
    for c in cells:
        if c.cell_type != "markdown":
            continue
        src = _src(c)
        head = _unlabel(src)
        if head.startswith("## "):
            inside = head.startswith(
                ("## Preliminaries", "## Definitions", "## Methods", "## Results")
            )
        labels = re.findall(r":label: (\S+)", src) + re.findall(r"^\((sect-[\w-]+)\)=", src, re.M)
        if inside:
            for target in re.findall(r"\{(?:prf:ref|numref)\}`(?:[^`<]*<)?([\w-]+)>?`", src):
                if (
                    target.startswith(
                        ("sect-", "thm-", "def-", "prop-", "cor-", "lem-", "alg-", "asm-", "cond-")
                    )
                    and target not in labels
                ):
                    assert target in seen, (c.id, target)
        seen.update(labels)


def test_no_hedging_phrases_in_the_body():
    assert not HEDGES.search(_markdown(_nb(PAPER_NB)))


def test_register_phrases_are_used_in_the_main_text_itself():
    text = (NOTES / "notation.md").read_text(encoding="utf-8")
    block = text.split("## Register phrases", 1)[1].split("## Forbidden phrases", 1)[0]
    body = _markdown(_nb(PAPER_NB)).lower()
    assert [p for p in re.findall(r"^- `([^`]+)`", block, re.M) if p.lower() not in body] == []


def test_disclosure_cites_the_incose_paper_and_the_search_and_stage_one_stay_abstract():
    ack = _section("AI acknowledgement")
    assert "@zargham2026incose" in ack and "supervisor-gated" in ack
    # the body only: the abstract (the supervisor's text of 2026-11-14) names the SysML v2 model
    body = "\n".join(_src(c) for c in _nb(PAPER_NB).cells[1:] if c.cell_type == "markdown")
    assert "black box to the method" in body  # the register's wording for a
    # the roadmap of Section 1 (his text, 2026-11-15) names the SysML v2 model, as the abstract does
    body = body.replace("from its SysML v2 model", "")
    # WP56: the case is narrated from the SysML v2 system model ("model" names
    # its object); the tools that run it stay out of the body
    assert not re.search(r"OpenSysML|Modelica|Simulink|pip install|(?<!\.)SysML(?! v2)", body, re.I)


def _structure(nb):
    """The labelled structure of a notebook, read from its cells: section number by label.

    Returns ``(sections, unlabelled)``: the ``(label)=`` target before each ``## `` heading mapped
    to the heading's number in order of appearance (the number MyST prints), and the headings
    that have no label.
    """
    sections, unlabelled, n = {}, [], 0
    for c in nb.cells:
        if c.cell_type != "markdown":
            continue
        src = _src(c)
        m = re.match(r"\((?P<label>[\w-]+)\)=\n## ([^#].*)", src)
        if m:
            n += 1
            sections[m.group("label")] = (n, m.group(2).strip())
        elif src.startswith("## "):
            n += 1
            unlabelled.append(src.splitlines()[0])
    return sections, unlabelled


def _reference_targets():
    """Every label a cross-reference may name: sections, appendices and the paper's own labels."""
    paper, support = _nb(PAPER_NB), _nb(SUPPORT_NB)
    sections, unlabelled = _structure(paper)
    appendices, unlabelled_support = _structure(support)
    own = set(re.findall(r"^:label: (\S+)$", _markdown(paper) + "\n" + _markdown(support), re.M))
    return sections, appendices, own, unlabelled, unlabelled_support


def _subsection_labels() -> dict[str, str]:
    """``sub-b-1`` -> its heading, from the ``(sub-b-1)=`` line of each subsection of the supporting
    material (every appendix with subsections); the number in the label must be the heading's
    own."""
    out = {}
    for c in _nb(SUPPORT_NB).cells:
        m = (
            re.match(r"^\((sub-[a-h]-\d+)\)=\n### ([A-H]\.\d+) ", _src(c))
            if c.cell_type == "markdown"
            else None
        )
        if m:
            letter, num = m.group(2).lower().split(".")
            assert m.group(1) == f"sub-{letter}-{num}", m.group(0)
            out[m.group(1)] = m.group(2)
    return out


def test_every_subsection_heading_carries_a_label():
    """Cross-references land on the subsection (B.1, H.2), not the top of the appendix (G-12)."""
    headings = [
        h for c in _nb(SUPPORT_NB).cells if c.cell_type == "markdown"
        for h in re.findall(r"^### ([A-H]\.\d+) ", _unlabel(_src(c)), re.M)
    ]  # fmt: skip
    assert headings and sorted(_subsection_labels().values()) == sorted(headings)


def test_every_appendix_subsection_named_in_the_main_text_resolves_to_a_label_that_exists():
    """In the prose, a reference to Appendix B.n (or just B.n) is a role naming ``sub-b-n``; in a
    generated sentence it is a link to ``supporting-material/#sub-b-n``; both labels exist."""
    labels = _subsection_labels()
    paper = _nb(PAPER_NB)
    body = _markdown(paper)
    roles = re.findall(r"\{ref\}`([^`<]*?)\s*<(sub-[^>`]+)>`", body)
    assert len(roles) >= 5
    for title, label in roles:
        assert label in labels and title.endswith(labels[label]), (title, label)
    plain = _ROLE.sub("", _unlabel(body))
    plain = re.sub(r"\{ref\}`[^`]*`", "", plain)
    assert not re.search(r"\b[A-H]\.\d{1,2}\b", plain), re.search(r"\b[A-H]\.\d{1,2}\b", plain)
    generated = " ".join(_out_text(c) for c in _code_cells(paper) if c.id.startswith("num-"))
    links = re.findall(r'<a href="supporting-material/#(sub-[^"]+)"[^>]*>([^<]*)</a>', generated)
    assert len(links) >= 3
    for label, text in links:
        assert label in labels and text == f"Appendix {labels[label]}", (label, text)
    unlinked = re.sub(r"<a [^>]*>[^<]*</a>", "", generated)
    assert not re.search(r"\b(?:Appendix )?[A-H]\.\d{1,2}\b", unlinked), unlinked


def test_every_heading_has_a_label_and_the_labels_follow_the_structure():
    """Section and appendix targets are derived from the notebooks: nothing is numbered by hand."""
    sections, appendices, _, unlabelled, unlabelled_support = _reference_targets()
    assert not unlabelled and not unlabelled_support
    assert [name for _, name in sections.values()] == SECTIONS
    assert [n for n, _ in sections.values()] == list(range(1, len(SECTIONS) + 1))
    assert list(appendices) == [f"appendix-{k.lower()}" for k in APPENDICES]
    for label, (_, heading) in appendices.items():
        assert heading.startswith(f"Appendix {label[-1].upper()}. "), label


def test_appendix_and_section_references_resolve():
    """R-4, R-13 L-C and L-D, and the readers' links: every cross-reference is a MyST role that
    names a label which exists, and no reference is typed as plain text. The section number is
    printed by MyST from the structure; the lemma number of a proof link is checked against the
    proof-map record."""
    sections, appendices, own, *_ = _reference_targets()
    targets = {*sections, *appendices, *own, *_subsection_labels()}
    record = _record()["lemmas"]
    for nb in (_nb(PAPER_NB), _nb(SUPPORT_NB)):
        body = "\n".join(
            _src(c) for c in nb.cells if c.cell_type == "markdown" and c.id != "frontmatter"
        )
        refs = _ROLE.findall(body)
        assert refs
        for role, title, label in refs:
            assert label in targets, (role, title, label)
            if label in sections:
                assert role == "numref" and "%s" in title, (title, label)
            if label.startswith("sub-"):  # a subsection: its number is the label's
                _, letter, num = label.split("-")
                assert title in (f"Appendix {letter.upper()}.{num}", f"{letter.upper()}.{num}")
            if label.startswith("appendix-"):
                assert (
                    (role == "ref" and title.startswith(f"Appendix {label[-1].upper()}"))
                    or (len(title) == 1 and title == label[-1].upper())
                    or title == "supporting material's appendices"  # the Organization route
                ), (title, label)
            for n in re.findall(r"^Appendix E, L(\d+)$", title):
                assert any(v["number"] == int(n) for v in record.values()), n
        plain = _ROLE.sub("", _unlabel(body))
        plain = re.sub(
            r"\[@[^\]]*\]", "", plain
        )  # a citation's locator names the cited work's own section
        plain = "\n".join(ln for ln in plain.splitlines() if not ln.startswith("#"))
        # the letters the check read before WP57e ([A-G], all but the HoroPCA appendix), re-lettered
        typed = r"\b[Ss]ections? \d|\bAppendix [ABD-H]\b|\b(Table|Figure) \d"
        assert not re.search(typed, plain), re.search(typed, plain)
    paper_body = _markdown(_nb(PAPER_NB))
    letters = {m[-1].upper() for _, _, m in _ROLE.findall(paper_body) if m.startswith("appendix-")}
    assert letters == set(APPENDICES)
    labels = set(re.findall(r":label: (\S+)", paper_body))
    for ref in re.findall(r"\{prf:ref\}`([^`]+)`", paper_body):
        assert ref in labels, ref


def test_section2_has_the_family_table_and_both_contrast_paragraphs_with_generated_counts():
    """R-8: the Pareto and DEA paragraphs, the table; the counts come from case.py, never typed."""
    s2 = _section("Prior art")
    assert (
        "**Pareto methods.**" in s2
        and "**Data envelopment analysis.**" in s2
        and "**Lineage.**" in s2
    )
    assert "@miettinen1999nonlinear" in s2 and "@charnes1978measuring" in s2
    body = _markdown(_nb(PAPER_NB))
    for typed in ("671", "706", "146"):
        assert typed not in body
    cell = next(c for c in _code_cells(_nb(PAPER_NB)) if c.id == "num-nondominated")
    assert "nondominated" in _out_text(cell) and re.search(r"\d", _out_text(cell))
    assert not WORDS_BANNED_IN_PRIOR_ART.search(s2)  # claims nothing as novel, first or new


def test_generated_sentence_cells_have_outputs_and_the_case_numbers_are_not_typed():
    cells = [c for c in _code_cells(_nb(PAPER_NB)) if c.id.startswith("num-")]
    assert len(cells) >= 8
    for c in cells:
        assert _out_text(c).strip(), f"{c.id} has no committed output ({STALE})"
    body = _markdown(_nb(PAPER_NB))
    for c in cells:
        for number in re.findall(r"\d+\.\d{3,}", _out_text(c)):
            assert number not in body, number


def test_reader_depth_anchors_are_all_present():
    """R-13: L-A title and abstract on the first page (the three-pane figure left the body: it is
    on the index page); L-B headings and the roadmap of Section 1 (his review of 2026-11-15
    replaced the main-results list and the organization paragraph); L-D pointers."""
    nb = _nb(PAPER_NB)
    fm = yaml.safe_load(_src(nb.cells[0]).split("---")[1])
    assert fm["title"] and len(fm["abstract"].split()) <= abstract_cap()
    first = " ".join(_src(c) for c in nb.cells[: [c.id for c in nb.cells].index("sec-prior-art")])
    for phrase in ("chart", "reversible", "position along the surface"):  # in words, no picture
        assert phrase in first, phrase
    intro = _section("The decision problem")
    assert "The paper proceeds as follows." in intro  # L-B: the roadmap routes by section
    roadmap = intro.split("The paper proceeds as follows.", 1)[1]
    for label in ("prior-art", "notation", "definitions", "methods", "results",
                  "case-construction", "case-analysis", "discussion", "future",
                  "process"):  # fmt: skip
        assert f"<sect-{label}>`" in roadmap, label  # every section after the first
    front = _src(_nb(SUPPORT_NB).cells[0])  # WP57a: the title block alone; the headings route
    assert front.strip().endswith("---") and "Companion" not in front


def test_simplifying_assumptions_are_named_where_made():
    """R-6: the named assumptions of the supervisor's rule appear in Methods."""
    methods = _section("Methods")
    for marker in (  # WP55: the list became sentences beside the procedures that make them
        "analyst chooses $K$",
        "sharp weights",
        "A4, log-affine conditioning",
    ):
        assert marker.lower() in methods.lower(), marker


# ---- gated checks (slow or networked) ----------------------------------------------------------


@pytest.mark.skipif(not os.environ.get("PAPER_EXECUTE"), reason="set PAPER_EXECUTE=1 (about 90 s)")
def test_notebooks_execute_from_a_clean_kernel_and_match_the_committed_outputs(tmp_path):
    """R-14: a re-run reproduces the committed text outputs (images compared by presence)."""
    work = tmp_path / "paper"
    shutil.copytree(PAPER, work, ignore=shutil.ignore_patterns("_build", "__pycache__"))
    out = subprocess.run(
        [sys.executable, str(work / "execute_notebooks.py")],
        capture_output=True, text=True, cwd=work, check=False,
        env={**os.environ, "PAPER_REPO_ROOT": str(ROOT)},  # the copy is not inside the repository
    )  # fmt: skip
    assert out.returncode == 0, out.stderr[-2000:]
    for name in ("paper.ipynb", "supporting_material.ipynb"):
        a, b = _nb(PAPER / name), _nb(work / name)
        for ca, cb in zip(_code_cells(a), _code_cells(b), strict=True):
            keys_a = [sorted(o.get("data", {})) for o in ca.outputs]
            keys_b = [sorted(o.get("data", {})) for o in cb.outputs]
            assert keys_a == keys_b, ca.id
            if ca.id.startswith("tab-H-toolchain"):
                continue  # the commit and the platform are observed values
            # byte-equal in the environment of record; elsewhere the planted table's digest is
            # masked and the numbers agree within text_rtol, as the F-table comparison does
            _current(_out_text(ca), _out_text(cb), ca.id)


@pytest.mark.skipif(
    not os.environ.get("PAPER_BUILD") or shutil.which("node") is None,
    reason="set PAPER_BUILD=1 with Node 22 or newer on PATH (the first build needs the network)",
)
def test_myst_builds_the_html_site(tmp_path):
    work = tmp_path / "paper"
    docs = tmp_path / "docs"
    docs.mkdir()
    shutil.copy(ROOT / "docs" / "references.bib", docs / "references.bib")
    shutil.copytree(PAPER, work, ignore=shutil.ignore_patterns("_build", "__pycache__"))
    out = subprocess.run(
        [str(ROOT / ".venv" / "bin" / "myst"), "build", "--html"],
        capture_output=True, text=True, cwd=work, check=False,
    )  # fmt: skip
    assert out.returncode == 0, out.stdout[-2000:] + out.stderr[-2000:]
    assert (work / "_build" / "html" / "index.html").is_file()
    assert "⛔" not in out.stdout
    # every figure's full-size link names a file of the built site, and the subsection labels the
    # cross-references use are heading identifiers of the supporting page
    html = work / "_build" / "html"
    page = (html / "index.json").read_text(encoding="utf-8")
    # the build inherits BASE_URL (the paper workflow sets the Pages prefix), so the asset paths
    # carry it; the files are written under _build/html/build/ whatever the prefix
    base = re.escape(os.environ.get("BASE_URL", "").rstrip("/"))
    urls = re.findall(rf'"url":"{base}(/build/fig[\w.-]+\.png)"[^]]*?full-size figure', page)
    assert len(urls) == 3  # three figure cells (WP19 P-7, P-10, P-5, P-6 revised); static: none
    assert all((html / u.lstrip("/")).is_file() for u in urls)
    support = (html / "supporting-material.json").read_text(encoding="utf-8")
    for label in _subsection_labels():
        assert f'"identifier":"{label}"' in support, label


# -- the list of values exact only in the environment of record


def test_every_exact_only_assertion_names_a_listed_value_and_every_listed_value_is_used():
    called = set()
    for path in sorted((ROOT / "tests").glob("*.py")):
        called |= set(re.findall(r"exact_only\(\s*\"([^\"]+)\"", path.read_text(encoding="utf-8")))
    names = set(listed())
    assert called <= names, f"exact assertions naming values that are not listed: {called - names}"
    assert names <= called, f"listed values no exact assertion uses: {names - called}"
    for name, entry in listed().items():
        assert entry["reason"].strip() and entry["elsewhere"].strip(), name


def test_the_variable_and_the_reference_file_exist():
    assert ENV_VAR == "HTS_ENVIRONMENT_OF_RECORD"
    assert VALUES_FILE.is_file() and REFERENCE_FILE.is_file()


# ---- WP16 D-6: the paper prints nothing to a precision at which it is not reproducible ----------

RESULTS = ROOT / "examples" / "adcs" / "experiments" / "reports" / "sensitivity.json"
RAW_RESIDUE = re.compile(r"\de-(?:1[3-9]|[2-9]\d)")  # 1e-13 and below, as raw digits
NUM_CELLS = [
    "num-nondominated", "num-certificates", "num-margin", "num-temperature",
    "num-regimes", "num-predict", "num-choosing-k", "num-terms", "num-elasticity",
    "num-decision", "num-requirements", "num-fleet-refit", "num-baseline-pointing",
    "num-planted",
]  # fmt: skip
"""The generated sentences of the paper. WP56 moved num-recovery, num-predict-reading,
num-k-temperatures, num-participation and num-tension out of Sections 7 to 9; WP57c landed the
participation sentence in B.1, the reading of the proposals in B.6 and the K temperatures in B.10
(``MOVED_TO_D``), left the recovery sentence to B.9's own tables and retired the tension sentence
(``4f81a4ea:work-packages/WP56-rounds/moved-to-appendix.md``, each line marked)."""


def _results():
    return json.loads(RESULTS.read_text(encoding="utf-8"))


def _case_sentences():
    import case
    import generate_findings as gf

    study = case.load_study("primary")
    fits = case.k_fits(study)
    reg = case.fit_regressor(study)
    return {
        "num-nondominated": gf.nondominated_sentence(study),
        "num-certificates": gf.certificate_sentence(fits),
        "num-margin": gf.margin_sentence(study, fits),
        "num-recovery": gf.recovery_sentence(),
        "num-predict-reading": gf.predict_reading(case.predict_check(study, reg), reg),
        "num-temperature": gf.temperature_sentence(study, fits[1]),
        "num-regimes": gf.regime_sentence(),
        "num-predict": gf.predict_check_sentence(case.predict_check(study, reg), reg),
        "num-choosing-k": gf.choosing_k_sentence(),
        "num-terms": gf.terms_sentence(study, fits),
        "num-elasticity": gf.elasticity_sentence(study, fits),
        "num-k-temperatures": gf.k_temperatures_sentence(study, fits),
        "num-participation": gf.participation_sentence(),
        "num-decision": gf.decision_sentence(gf.decision(study, fits)),
        "num-requirements": gf.requirements_sentence(study, fits[1]),
        "num-fleet-refit": gf.fleet_refit_sentence(),
        "num-baseline-pointing": gf.baseline_requirement_sentence(case.load_study("stock")),
        "num-planted": gf.planted_sentence(),
    }


MOVED_TO_D = {
    "num-participation": ("sent-B-participation", "participation_sentence"),
    "num-temperature-variants": ("sent-B-temperature-variants", "temperature_variants"),
    "num-predict-reading": ("sent-B-proposals", "proposals_reading"),
    "num-k-temperatures": ("sent-B-k-temperatures", "k_temperatures"),
}
"""The generated sentences WP56 moved out of Sections 7 to 9 and WP57c landed in Appendix B:
paper cell -> (the Appendix B cell, its one-call generator)."""


def _moved(cid: str) -> str:
    """The generated sentence of a cell WP56 moved out of Sections 7 to 9: the committed output
    of the Appendix B cell that prints it (``MOVED_TO_D``), or, for the recovery sentence that
    B.9's tables state in full and no cell prints, its generator."""
    import generate_findings as gf

    if cid in MOVED_TO_D:
        return _cell_out(SUPPORT_NB, MOVED_TO_D[cid][0])
    if cid == "num-recovery":
        return str(gf.recovery_sentence())
    raise KeyError(cid)


@pytest.mark.slow
def test_the_moved_sentences_in_appendix_d_are_their_generators_output():
    """WP57c G2: each sentence WP56 moved out of Sections 7 to 9 is printed by one call in the
    Appendix B subsection that holds what it reads (participation in B.1, the scaler variant in
    B.3, the proposals in B.6, each K's temperature in B.10), and the output is current."""
    import generate_findings as gf

    exact = exact_only("planted_table_sha256")
    rtol = listed()["planted_table_sha256"]["text_rtol"]
    cells = _appendix_cells(_nb(SUPPORT_NB))["B"]
    ids = [c.id for c in cells]
    for cid, (dcell, fn) in MOVED_TO_D.items():
        assert dcell in ids, dcell
        assert f"{fn}()" in _cell_src(dcell, SUPPORT_NB), dcell
        committed, fresh = _cell_out(SUPPORT_NB, dcell), str(getattr(gf, fn)())
        ok = committed == fresh if exact else _same_text(committed, fresh, rtol)
        assert ok, f"{dcell}: {STALE}"
        assert cid not in [c.id for c in _nb(PAPER_NB).cells], cid
    before = {"sent-B-participation": "tab-B-exponents_and_terms",
              "sent-B-temperature-variants": "tab-B-sensitivity_variants",
              "sent-B-proposals": "tab-B-propose_predict_check",
              "sent-B-k-temperatures": "tab-B-choosing_k"}  # fmt: skip
    for dcell, table in before.items():
        assert ids.index(dcell) == ids.index(table) + 1, dcell
    assert "sub-b-1" not in _cell_out(SUPPORT_NB, "sent-B-participation")  # no link to itself


@pytest.fixture(scope="module")
def case_sentences():
    return _case_sentences()


def test_results_file_records_the_five_seeds_and_the_perturbation():
    r = _results()
    assert r["seeds"] == [1, 2, 3, 4, 5]
    assert r["perturbation"]["relative_half_width"] == 1e-12
    assert set(r["perturbation"]["variables"]) == {"Kp", "Kd", "panel_span_m", "battery_wh"}
    for name, e in r["quantities"].items():
        if "min" in e and np.isfinite(e["committed"]):
            assert e["min"] <= e["committed"] <= e["max"], name


@pytest.mark.slow
def test_generated_sentences_quote_the_ranges_from_the_results_file(case_sentences):
    from paper_stability import stable

    q = _results()["quantities"]
    nd = str(case_sentences["num-nondominated"])
    moved = 0
    for name, e in q.items():
        if not name.startswith("nondominated | primary | ") or not name.endswith("| nondominated"):
            continue
        lo, hi = int(e["min"]), int(e["max"])
        moved += lo != hi
        assert (f"{lo:,} to {hi:,}" if lo != hi else f"{lo:,} on") in nd, name
    # WP23 data gate (D-9 item 5): no count moves on the nine-metric data; the sentence then
    # says that a number that moves is printed as a range
    assert moved or "is printed as a range" in nd
    cert = str(case_sentences["num-certificates"])  # the largest term gap moved here from the sweep
    gap = q["certificate | primary | 2 | max gap"]
    if max(abs(gap["min"]), abs(gap["max"])) < 1e-12:
        assert "term gap below 1e-12" in cert
    # the term shares moved from the sentence to the terms table of Appendix B (B.1), where each
    # is printed to the digits that hold over the datasets, never the committed value alone
    terms = next(c for c in _code_cells(_nb(SUPPORT_NB)) if c.id == "tab-B-exponents_and_terms")
    primary = _out_text(terms).split("Dataset cubesat-stock", 1)[0]
    for k in (1, 2, 3):
        name = f"D terms K=3 | primary | {k} | share"
        e = q[name]
        shown = stable(name)
        assert shown in primary, name
        if format(e["min"], ".4g") != format(
            e["max"], ".4g"
        ):  # the share moves at the print format
            assert shown != format(e["committed"], ".4g"), name
    # the effective sample size is printed to the digits that hold at one decimal; the committed
    # value alone appears only when the regenerations agree with it at that format
    temp = str(case_sentences["num-temperature"])
    name = "fit | primary K=1 | n_eff_"
    n_eff = q[name]
    assert stable(name, lambda v: f"{v:.1f}") in temp, name
    if f"{n_eff['min']:.1f}" != f"{n_eff['max']:.1f}":  # moves at the print format
        assert f"{n_eff['committed']:.1f}" not in temp


@pytest.mark.slow
def test_no_residue_is_printed_as_raw_digits(case_sentences):
    for key, text in case_sentences.items():
        assert not RAW_RESIDUE.search(str(text)), key
    for nb in (PAPER_NB, SUPPORT_NB):
        for cell in _code_cells(_nb(nb)):
            if cell.id.startswith(("num-", "tab-B-")):
                assert not RAW_RESIDUE.search(_out_text(cell)), cell.id
    assert "below 1e-12" in str(case_sentences["num-certificates"])


def test_generated_sentences_committed_output_is_current(case_sentences):
    exact = exact_only("planted_table_sha256")
    rtol = listed()["planted_table_sha256"]["text_rtol"]
    by_id = {c.id: c for c in _code_cells(_nb(PAPER_NB))}
    for cid in NUM_CELLS:
        committed, fresh = _out_text(by_id[cid]), str(case_sentences[cid])
        ok = committed == fresh if exact else _same_text(committed, fresh, rtol)
        assert ok, f"{cid}: {STALE}"


def test_appendix_d_has_the_stability_subsection_and_section_9_points_to_it():
    import generate_results

    heads = [h for h in _headings(_nb(SUPPORT_NB), "###") if h.startswith("B.")]
    assert "B.7 Stability of the conclusions under rounding-level jitter" in heads
    cell = next(c for c in _code_cells(_nb(SUPPORT_NB)) if c.id == "tab-B-stability")
    exact = exact_only("planted_table_sha256")
    committed, fresh = _out_text(cell), str(generate_results.stability())
    rtol = listed()["planted_table_sha256"]["text_rtol"]
    assert (committed == fresh) if exact else _same_text(committed, fresh, rtol), STALE
    assert "identical" in committed and "differs" not in committed
    assert "B.7" in _section("Case analysis")


def test_stability_table_is_derived_from_the_results_file():
    import generate_results

    q = _results()["quantities"]
    rows = generate_results._verdict_rows()
    for (_, prefixes, suffix), (_, _, ok) in zip(generate_results.CONCLUSIONS, rows, strict=True):
        names = [n for n in q if n.startswith(prefixes) and n.endswith(suffix)]
        assert ok == all(q[n]["identical"] for n in names)
    assert all(count > 0 for _, count, _ in rows)


# ---- the driver's change requests of WP10 (review of 2026-11) -----------------------------------


def _all_rendered_text() -> str:
    """Everything a reader can see in both notebooks: the Markdown and the committed outputs."""
    parts = []
    for path in (PAPER_NB, SUPPORT_NB):
        nb = _nb(path)
        parts += [_src(c) for c in nb.cells if c.cell_type == "markdown"]
        parts += [_out_text(c) for c in _code_cells(nb)]
    return "\n".join(parts)


def test_the_paper_claims_no_external_review():
    """(1) The review of 2026-11 was the supervisor's own: no sentence says an external reviewer
    audited the mathematics (the front matter, the body, the appendices and every output)."""
    text = _all_rendered_text().lower()
    assert "external reviewer" not in text
    assert "audited the mathematics" not in text
    assert "machine-checked" not in _section("AI acknowledgement").lower()


def test_every_figure_and_table_is_referenced_from_the_text():
    """G-2: each float with a label has a numref to it in the running text (not in its caption)."""
    body = _markdown(_nb(PAPER_NB))
    floats = re.findall(r"^:::+\{(?:figure|table)\}[^\n]*\n:label: (\S+)", body, re.M)
    assert len(floats) == 13, (
        floats
    )  # ten figures (the prior-art layers and the pipeline joined) and three tables (WP56: the
    # requirement order of Section 7)
    for cell in _nb(PAPER_NB).cells:
        if cell.cell_type != "markdown" or cell.id == "frontmatter":
            continue
        text = _src(cell)
        if re.search(r"^:::+\{(?:figure|table)\}", text, re.M):
            body = body.replace(text, "")  # the caption's own cell is not a reference
    for label in floats:
        pattern = rf"\{{numref\}}`(Figure|Table) %s <{re.escape(label)}>`"
        assert re.search(pattern, body), f"{label} is not referenced from the text"


def test_section_6_names_the_three_levels_and_has_level_1_as_a_derived_block():
    """G-4, C-1: Level 1 (descent), Level 2 (numerical stationarity) and Level 3 (conditional
    local optimality) are named; Level 1 is a Let-Assume-Then block with its proof pointer (L15)."""
    text = _section("Results")
    for name in ("Level 1, descent", "Level 2, numerical stationarity",
                 "Level 3, conditional local optimality"):  # fmt: skip
        assert name in text, name
    block = next(b for b in _blocks() if "(L15)" in b[1])
    assert block[2] == "thm-descent" and block[3].startswith("Let ")
    for hypothesis in ("refit by $f_k$", "unpenalized", "the soft maximum over all rows"):
        assert hypothesis in block[3], hypothesis
    assert "Appendix E, L15" in text  # the proof pointer; the script itself is Appendix E's
    abstract = yaml.safe_load(_src(_nb(PAPER_NB).cells[0]).split("---")[1])["abstract"]
    assert "descent" not in abstract  # R-38: the abstract does not carry the three levels


def test_appendix_b_shows_every_result_of_the_record_with_derived_counts():
    """C-1: Appendix E follows the record (L16 included); its counts are read, never typed."""
    record = _record()["lemmas"]
    assert "lemma_15_descent.py" in record
    text = str(generate_proofs.how_to_read())
    results = sum(len(lem["results"]) for lem in record.values())
    steps = sum(len(lem["steps"]) for lem in record.values())
    assert f"{results} results in {len(record)} files and {steps} steps" in text
    last = max(lem["number"] for lem in record.values())  # derived from the record, never typed
    assert "L15. descent" in _proof_text()
    heading = (
        f"### E.2 The several-term fit, its levels of guarantee and the tension (L12 to L{last})"
    )
    assert heading in _src(next(c for c in _nb(SUPPORT_NB).cells if c.id == "app-E-2"))
    # WP57b: the rule and the kinds; no list of the appendix's parts, no repeat of Section 9
    assert "two parts" not in text and "human validation" not in text


def test_the_claims_of_c1_have_their_true_basis():
    """C-1: terms unchanged under smoothing is by construction; outward monotonicity is Open; the
    principal directions are a reading; the own-rows refit points to its number in Appendix B."""
    methods = _section("Methods")
    assert "by construction" in methods and "leaves the terms unchanged" in methods
    assert not re.search(r"unchanged \(\{prf:ref\}`thm-extension`\)", methods)
    assert (  # the numbers are Appendix B.8's (the table below); Methods keeps the one sentence
        "refitting a term on its own rows alone does not recover planted terms" in methods
        and "B.8" in methods
    )
    assert "ill-posed" not in methods  # what B.8 observed, not a verdict
    own = next(c for c in _code_cells(_nb(SUPPORT_NB)) if c.id == "tab-B-own_rows_refit")
    text = _out_text(own)
    assert text == str(generate_results.own_rows_refit())
    assert re.search(r"\| 0 of 60 \|", text) and re.search(r"\| 60 of 60 \|", text)


def test_appendix_d8_prints_the_conditioning_of_the_exponents():
    """G-4 (WP57c: the old D.12's table merged into B.4): `conditioning_` is a column of B.4's
    table, one value per term at each K, per regime, with its one defining sentence."""
    out = _cell_out(SUPPORT_NB, "tab-B-termination_records")
    for regime in ("cubesat-primary", "cubesat-stock"):
        part = out.split(f"Dataset {regime}:")[1].split("Dataset")[0]
        head = part.strip().splitlines()[0]
        assert head.rstrip(" |").endswith("conditioning_"), head
        rows = [r for r in part.splitlines() if re.match(r"\| [123] \|", r)]
        assert [r.split("|")[-2].count(",") for r in rows] == [0, 1, 2]
        assert "term rows" not in head and "term shares" not in head  # B.1's columns
    assert "a small value flags a nearly flat direction" in _cell_src("app-B-4", SUPPORT_NB)
    assert "app-B-cond" not in {c.id for c in _nb(SUPPORT_NB).cells}


def _injected_noise_rows(text: str) -> list[dict]:
    """The rows of B.13's table as dicts keyed by the header cells."""
    lines = [ln for ln in text.splitlines() if ln.startswith("|")]
    head = [c.strip() for c in lines[0].strip("|").split("|")]
    return [
        dict(zip(head, (c.strip() for c in ln.strip("|").split("|")), strict=True))
        for ln in lines[2:]
    ]


def test_d18_reads_the_corollary_against_injected_noise_as_the_table_licenses():
    """WP29, narrowed in the WP30 cascade to the regenerated table: B.13 says the predicted largest
    shift agrees with the measured mean within the spread of the draws at half a percent in the
    primary regime only, exceeds it in every other row, and that the contending set changes most at
    10 percent noise in both regimes (the Jaccard column)."""
    nb = _nb(SUPPORT_NB)
    cell = next(c for c in _code_cells(nb) if c.id == "tab-B-injected_noise")
    rows = _injected_noise_rows(_out_text(cell))
    assert len(rows) == 8
    by = {(r["regime"], r["delta (%)"]): r for r in rows}
    f = lambda r, k: float(r[k])  # noqa: E731
    pred, meas, spread = (
        "predicted largest shift",
        "measured largest shift (mean)",
        "spread of the draws",
    )
    agree = ("cubesat-primary", "0.5")
    assert abs(f(by[agree], pred) - f(by[agree], meas)) <= f(by[agree], spread)
    for key, r in by.items():
        if key != agree:
            assert f(r, pred) > f(r, meas), key
    for regime in ("cubesat-primary", "cubesat-stock"):
        jac = [f(by[(regime, d)], "contending-set Jaccard") for d in ("0.5", "2.0", "5.0", "10.0")]
        assert jac[-1] == min(jac) and jac[-1] < 1  # the set changes most at 10 percent
    d18 = next(c for c in nb.cells if c.id == "app-B-noise")
    assert "B.13" in _src(d18) and "injected" in _src(d18)


@pytest.mark.slow
def test_d18_table_is_the_injection_script_output():
    cell = next(c for c in _code_cells(_nb(SUPPORT_NB)) if c.id == "tab-B-injected_noise")
    assert _out_text(cell) == str(generate_results.injected_noise())


def test_d12_says_why_conditioning_matters_how_it_is_computed_and_how_to_inspect_it():
    """S-10 (the supervisor's word, WP28-decisions.md), WP57c: the explanation the old D.12
    carried is the termination page's, which says why it matters, how it is computed and how to
    inspect it; B.4 prints the case's values (K = 1 first in each regime) and links the page; the
    code path exists, and the call it gives runs on a strictly positive array."""
    text = (ROOT / "docs" / "user-guide" / "termination.md").read_text(encoding="utf-8")
    text = " ".join(text.split())
    for part in ("that loss's curvature along its flattest direction", "How it is computed",
                 "On your own problem"):  # fmt: skip
        assert part in text, part
    assert "docs/user-guide/termination.md" in _cell_src("app-B-4", SUPPORT_NB)
    out = _cell_out(SUPPORT_NB, "tab-B-termination_records")
    for r in generate_results._studies():
        value = f"{generate_results._fits(r)[1].estimator.conditioning_[0]:.2g}"
        part = out.split(f"Dataset {generate_model.DATASET_LABELS[r]}:")[1]
        row = next(x for x in part.splitlines() if x.startswith("| 1 |"))
        assert row.rstrip(" |").endswith(f"[{value}]"), row
    assert "def _conditioning" in (ROOT / "src" / "tradespace" / "estimator.py").read_text(
        encoding="utf-8"
    )
    from tradespace import HyperbolicTradeSpace, make_frontier_data

    call = re.search(
        r"`(HyperbolicTradeSpace\(temperature=50\.0\)\.fit\(M\)\.conditioning_)`", text
    )
    assert call, "the call is printed in code font"
    M, _ = make_frontier_data(400, 4, n_terms=1, random_state=0)
    value = eval(call.group(1), {"HyperbolicTradeSpace": HyperbolicTradeSpace, "M": M})
    assert value.shape == (1,) and value[0] > 0


def test_section_8_says_the_conditioning_centres_each_log_metric_and_on_the_data_it_does():
    """CR-38: Section 8 keeps "This conditioning centres each log-metric (the standard scaler)."
    The case's conditioner is the standard scaler and the log-metrics of both regimes have column
    means at rounding level (the comparison of equations (1) and (2) is Section 6.2's)."""
    import case

    assert "This conditioning centres each log-metric (the standard scaler)." in _section(
        "Case construction"
    )
    for study in generate_results._studies().values():
        logs = np.log(study.M)
        assert np.abs(logs.mean(axis=0)).max() < 1e-12, study.regime
    assert case.conditioner_for.__defaults__[-1] == "standard"


def test_the_paper_claims_nothing_as_novel():
    """WP28 (S8's second item), as it stands after his review of 2026-11-15: the Main results list
    and its closing clause, and the combination sentence, were cut from Sections 1 and 2. What the
    clause protected holds on the text that is left: neither section says the combination was
    absent from the literature, and Section 2 does not call the method new, first or novel."""
    for heading in ("The decision problem", "Prior art"):
        section = _section(heading)
        assert "We did not find the combination" not in section, heading
        assert "The sources establish the pieces, not the combination" not in section, heading
    assert not WORDS_BANNED_IN_PRIOR_ART.search(_section("Prior art"))


def test_section_9_prints_the_strongest_pair_to_the_digits_appendix_d4_prints():
    """O-8 (WP25-review.md; WP28-retest.md G-6), narrowed in the WP30 cascade: a Spearman value in
    Section 9's regime sentence is B.2's, to three decimals, so "+0.99" does not sit beside B.2's
    "no pair reaches 0.99". On the regenerated data the one-axis pair of both regimes (energy
    balance and available power, B.2) has no member in a regime's own part of the contending set,
    so the sentence prints no value and says the primary set lies inside the baseline set."""
    sentence = _cell_out(PAPER_NB, "num-regimes")
    d4 = _cell_out(SUPPORT_NB, "tab-B-regime_comparison")
    values = re.findall(r"Spearman (\+\d\.\d{3}) and (\+\d\.\d{3}) over", sentence)
    for v in (v for pair in values for v in pair):
        assert v in d4, v
        assert float(v) < 0.99
    assert not values
    assert "energy balance and available power" in d4
    assert "the primary set lies inside the baseline set" in sentence


def test_no_doubled_label_before_a_cross_reference():
    """G-7: a reference to a definition or theorem prints its own kind; none is typed before it."""
    body = _markdown(_nb(PAPER_NB))
    assert not re.search(r"\b(Definition|Theorem|Lemma|Proposition|Corollary) \{prf:ref\}", body)
    assert "Definition Definition" not in _all_rendered_text()


def test_generated_sentences_have_no_interval_in_parentheses():
    """G-7: an interval ('x to y') is never wrapped in parentheses in a generated sentence."""
    for c in _code_cells(_nb(PAPER_NB)):
        if c.id.startswith(GENERATED_SENTENCES):
            assert not re.search(r"\([^()]* to [^()]*\)", _out_text(c)), c.id
    predict = next(c for c in _code_cells(_nb(PAPER_NB)) if c.id == "num-predict")
    assert "regressor's own band" in _out_text(predict)


def test_conditioning_symbol_is_not_set_as_mathematics():
    """G-7: `$conditioning_$` printed a processing error; an attribute name is in code font."""
    text = _out_text(next(c for c in _code_cells(_nb(SUPPORT_NB)) if c.id == "tab-D-register"))
    assert "$conditioning_$" not in text and "`conditioning_`" in text


def test_regime_names_a_gain_box_dataset_and_the_terms_are_terms():
    """C-4: 'regime' only for the two gain boxes; no 'three regimes' in the paper or its tables."""
    text = _all_rendered_text().lower()
    assert "three regimes" not in text and "regimes of the facet" not in text
    assert "different contending sets" in _section("Case analysis")
    for section in ("Methods", "Case analysis"):
        # Figure 9 (fig-regimes) went at the supervisor's word "Cut to a pointer" (S-3, R-10,
        # WP28-decisions.md): its label is gone from the text, so its exemption goes with it.
        prose = re.sub(r"two (gain )?regimes", "", _section(section).lower())
        assert "regimes" not in prose, section
    notation = (NOTES / "notation.md").read_text(encoding="utf-8")
    register = notation.split("## Register phrases", 1)[1].split("## Forbidden phrases", 1)[0]
    forbidden = notation.split("## Forbidden phrases", 1)[1]
    assert "- `regime`" in register and "- `the three regimes`" in forbidden


# ---- C-3: the reading pass is a committed table of the paper ------------------------------------

import generate_reading_pass  # noqa: E402
import generate_results  # noqa: E402
import generate_supplement  # noqa: E402


def test_reading_pass_yaml_matches_the_markdown_table_verbatim():
    md = generate_reading_pass.markdown_rows()
    rows = generate_reading_pass.rows()
    assert len(md) == len(rows) == 56
    for a, b in zip(md, rows, strict=True):
        assert {k: b[k] for k in generate_reading_pass.FIELDS} == a, a["n"]
    verdicts = [r["verdict"] for r in rows]
    assert [verdicts.count(v) for v in ("supported", "partly supported", "not accessible")] == [
        25, 19, 9
    ]  # fmt: skip
    assert verdicts.count("not found") == 2 and verdicts.count("accessible (own work)") == 1


def test_reading_pass_rows_carry_what_the_paper_does_and_resolve_in_the_bibliography():
    keys = _bib_keys()
    for r in generate_reading_pass.rows():
        assert r["status"] in generate_reading_pass.STATUS, r["n"]
        assert r["key"] in keys, r["key"]
        if r["status"] != "kept":
            assert r["now"].strip(), r["n"]
        if r["verdict"] in ("partly supported", "not found"):
            assert r["status"] == "reworded", r["n"]  # a sentence is never left as it was
        if r["verdict"] == "not accessible":
            assert r["status"] == "confirm", r["n"]
    own = next(r for r in generate_reading_pass.rows() if r["key"] == "zargham2026incose")
    assert own["status"] == "supervisor"


def test_reading_pass_supplement_equals_its_generator_and_g1_cites_it():
    """WP57a (the supervisor, WP38: keep the YAML for our own checking, drop the table from the
    supporting material): paper/supplement/reading-pass.md is render('reading-pass.md'), the plain
    reading_pass_table from the record; A.1's last cell links it; the table keeps the three columns
    the supervisor set at 7257053 (what we say, the source, where in it; no verdict, why or status),
    one row per citing sentence."""
    path = PAPER / "supplement" / "reading-pass.md"
    text = path.read_text(encoding="utf-8")
    assert text == generate_supplement.render("reading-pass.md"), STALE
    assert generate_supplement.stale() == []
    table = str(generate_reading_pass.reading_pass_table(plain=True))
    assert table in text
    lines = [ln for ln in table.splitlines() if ln.startswith("| ")]
    assert lines[0] == "| What we say | Source | Where in it |"
    assert all(ln.count(" | ") == 2 for ln in lines)  # three columns, no verdict, why or status
    removed = generate_reading_pass.REMOVED
    kept = [r for r in generate_reading_pass.rows() if r["n"] not in removed]
    assert len(lines) - 1 == len(kept) == 53  # the header and one row per citing sentence
    assert all(
        ("citation" in r["now"].lower() and "remov" in r["now"].lower())
        or r["now"].startswith("Removed")
        for r in generate_reading_pass.rows()
        if r["n"] in removed
    )
    assert not re.search(r"verdict|supported|Cited now|rows \(", text, re.I)
    assert "api.crossref.org" not in text and "api.semanticscholar.org" not in text
    assert "<div" not in text and "style=" not in text  # Markdown only, for the repository's viewer
    assert all(f"({generate_reading_pass.PAPER_PAGE}#cite-" in ln for ln in lines[2:])
    g1 = _appendix_cells(_nb(SUPPORT_NB))["A"][-1]
    assert "blob/main/paper/supplement/reading-pass.md" in _src(g1)
    assert not any(c.id == "tab-A-reading_pass_table" for c in _nb(SUPPORT_NB).cells)


@pytest.mark.slow
def test_the_c_and_d_supplement_files_equal_their_generators_and_are_cited():
    """WP57c: F.5's baseline preview and full pair table, the old D.1's sweep and D.6's refits are
    files under paper/supplement/, each its generator's output, each cited by one line of F or
    B; F.5 keeps the primary regime's preview and the pairs at |Spearman| 0.5 or above."""
    for name, cell in (("metric-associations.md", "app-F-5-associations"),
                       ("temperature-sweep.md", "app-B-supplement"),
                       ("refits-by-category.md", "app-B-supplement")):  # fmt: skip
        text = (PAPER / "supplement" / name).read_text(encoding="utf-8")
        assert text == generate_supplement.render(name), f"{name}: {STALE}"
        assert f"paper/supplement/{name}" in _cell_src(cell, SUPPORT_NB), name
    c5 = _cell_out(SUPPORT_NB, "tab-F-metric_table")
    assert "cubesat-primary" in c5 and "cubesat-stock" not in c5
    pairs = _cell_out(SUPPORT_NB, "tab-F-metric_associations")
    rows = [r for r in pairs.splitlines() if r.startswith("| ") and "metric a" not in r]
    spearman = [max(abs(float(c)) for c in (r.split("|")[3], r.split("|")[5])) for r in rows]
    assert spearman and min(spearman) >= generate_model.SHOWN_ASSOCIATION
    full = (PAPER / "supplement" / "metric-associations.md").read_text(encoding="utf-8")
    assert full.count("\n| ") - 2 > len(rows) and "cubesat-stock: " in full


def test_generate_supplement_writes_what_its_generators_return(tmp_path):
    """The script writes render(name) for each file and --check reports a stale one."""
    names = generate_supplement.write_all(tmp_path)
    assert names == list(generate_supplement.FILES) == [
        "reading-pass.md", "metric-associations.md", "temperature-sweep.md",
        "refits-by-category.md",
    ]  # fmt: skip
    for name in names:
        assert (tmp_path / name).read_text(encoding="utf-8") == generate_supplement.render(name)
    assert generate_supplement.stale(tmp_path) == []
    (tmp_path / "reading-pass.md").write_text("stale\n", encoding="utf-8")
    assert generate_supplement.stale(tmp_path) == ["reading-pass.md"]


# ---- the driver's change requests of WP10, round 2 (the cold reads of 2026-11-09) ----------------


def _cell_out(nb_path, cell_id: str) -> str:
    return _out_text(next(c for c in _code_cells(_nb(nb_path)) if c.id == cell_id))


def test_cr1_one_definition_of_the_contending_set_and_the_captions_say_it():
    """(1) The set is the support of the exact-maximum fit; the figures say so and mark it."""
    text = _markdown(_nb(PAPER_NB))
    definition = text.split("prf:definition} The n-lemma", 1)[1].split(":::", 1)[0]
    assert "support of the exact-maximum" in definition and "10^{-9}" not in definition  # WP55
    assert "above $10^{-9}$ in the exact-maximum fit" in _section("Methods")
    assert "participation threshold ($10^{-3}$)" in _section("Methods")
    assert "def-nlemma" in _section("Methods")
    # fig-regimes-caption left with Figure 9 at the supervisor's word "Cut to a pointer" (S-3,
    # R-10, WP28-decisions.md).
    # WP42: Figure 7 became the tension matrix of each term; the association figure, which
    # outlined the contending set, left the paper's figures (it stays in the package as
    # plot_association). The contending set is read from the K = 1 and K = 2 sentences below.
    caption = _src(next(c for c in _nb(PAPER_NB).cells if c.id == "fig-tension-matrix-caption"))
    assert "with an exponent w on the term" in caption and "balanced point" in caption
    k1 = _cell_out(PAPER_NB, "num-k1")
    assert "exact-maximum fit has a" in k1 and "exponents at the fit temperature" in k1
    assert "exact-maximum supports" in _cell_out(PAPER_NB, "num-terms")


@pytest.mark.slow
def test_cr2_the_planted_recovery_is_in_section_9_with_its_table_in_d14():
    """(2) Does the method recover a known answer, how often, and what the failures are."""
    import generate_results

    sentence = _moved("num-recovery")
    assert "A known answer" in sentence and "in 16, at the exact maximum" in sentence
    assert "frontier rows on their thinnest term" in sentence and "Appendix B.9" in sentence
    ids = [c.id for c in _nb(PAPER_NB).cells]  # WP56: Section 8 keeps the count, at K = 2
    assert ids.index("sec-case-analysis-2") < ids.index("num-planted") < ids.index("num-terms")
    assert "16 of 20 planted tables" in _cell_out(PAPER_NB, "num-planted")
    cell = _cell_out(SUPPORT_NB, "tab-B-planted_recovery")
    _current(cell, str(generate_results.planted_recovery()), "planted_recovery")
    assert re.search(r"\| infinity \| 20 \| 16 of 20 \| 1, 3, 8, 16 \|", cell)
    assert re.search(r"\| 50 \| 20 \| 16 of 20 \| 1, 3, 8, 16 \|", cell)
    # only what is the same on both platforms: no status or error digits for the exact maximum
    assert "iteration cap" in cell and "G-10" in cell and "Linux amd64" in cell
    assert re.search(r"\| 1 \| 5 \| no \| no \| certified \| \d\.\d\d \| \d\.\d\d \|", cell)
    assert not re.search(r"\| infinity \| \d+ \| \d\.\d\d", cell)
    heads = _headings(_nb(SUPPORT_NB), "###")
    assert any(h.startswith("B.9 ") for h in heads)


@pytest.mark.skipif(not os.environ.get("PAPER_EXECUTE"), reason="set PAPER_EXECUTE=1 (about 4 min)")
def test_generated_tables_do_not_move_under_platform_perturbation(tmp_path):
    """Regenerate every generated table and sentence three ways and flag what moves.

    A run with one BLAS thread and a run with four must agree with the plain run exactly; a run
    with the restart order permuted (``random_state`` shifted) may move only the names listed under
    ``[perturbation]`` in ``paper/environment_values.toml`` (the term-numbered tables and the
    multi-modal B.9), each of which the audit table there explains.
    """
    allowed = set(tomllib.loads(VALUES_FILE.read_text(encoding="utf-8"))["perturbation"][
        "moves_under_restart_shift"])  # fmt: skip

    def run(tag, extra_env, *args):
        out = tmp_path / f"{tag}.json"
        env = {**os.environ, **extra_env}
        subprocess.run(
            [sys.executable, str(PAPER / "paper_perturb.py"), str(out), *args],
            check=True, cwd=PAPER, env=env,
        )  # fmt: skip
        return json.loads(out.read_text(encoding="utf-8"))

    threads = lambda n: {  # noqa: E731
        k: str(n) for k in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS",
                            "VECLIB_MAXIMUM_THREADS")
    }  # fmt: skip
    base = run("one", threads(1))
    for tag, other in (("four", run("four", threads(4))),
                       ("restarts", run("restarts", threads(1), "--restarts", "7"))):  # fmt: skip
        moved = {k for k in base if base[k] != other[k]}
        if tag == "restarts":
            assert moved <= allowed, (
                f"printed quantities that move with the restart order: {moved - allowed}"
            )
        else:
            assert not moved, f"printed quantities that move with the thread count: {moved}"


def test_cr3_the_target_and_the_band_carry_their_reason_and_the_sensitivity_holds():
    """(3) One sentence each, with a pointer to B.3, which shows the sets do not change."""
    assert "about a tenth, by convention" in _section("Methods") and "Appendix B.3" in _section(
        "Methods"
    )
    assert "weighs within a factor $e$" in _section("Methods")  # WP55: with the temperature rule
    table = _cell_out(SUPPORT_NB, "tab-B-sensitivity_variants")
    for regime in ("cubesat-primary", "cubesat-stock"):
        block = table.split(f"Dataset {regime}:", 1)[1].split("Dataset cubesat", 1)[0]
        rows = {r.split("|")[1].strip(): r.split("|") for r in block.splitlines() if r[:1] == "|"}
        for variant in ("target fraction halved", "target fraction doubled"):
            cols = rows[variant]
            assert cols[6].strip() == cols[9].strip(), (regime, variant)  # n_lemma = shared


def test_cr4_5_6_the_term_share_is_described_and_the_terms_carry_their_clause():
    """(4) no analogy to explained variance; (5) energy differential; (6) n-lemma."""
    definitions = _section("Definitions")
    assert "explained variance" not in definitions.lower()
    # WP11 round 1b CR-8: the share counts the rows of a term's cell (ruling 2), not "dominates"
    assert "in the cell of term $k$" in definitions and "depends on the band" in definitions
    assert "dominates" not in definitions
    assert "a design's level relative to the fitted reference surface" in definitions
    front = " ".join(_src(_nb(PAPER_NB).cells[0]).split())
    intro = _section("The decision problem")
    assert "by analogy with dilemma and trilemma" in " ".join(intro.split())
    # the abstract (the supervisor's text of 2026-11-14) says it in his words: "Expanding on the
    # concept of a dilemma or trilemma, a monomial term in n metrics characterizes an n-lemma";
    # "energy" is his intuition word, in quotation marks, for the level sets
    assert "Expanding on the concept of a dilemma or trilemma" in front
    assert 'solving for the "energy" level sets' in front


def test_cr7_16_the_first_screen_says_what_scales_and_keeps_the_three_objects_apart():
    """(7) the nondominated counts are in section 1; (16) the unit level set is not the boundary."""
    nb = _nb(PAPER_NB)
    ids = [c.id for c in nb.cells]
    assert ids.index("num-nondominated") > ids.index("sec-case-analysis")  # moved at his review
    front = _src(nb.cells[0])
    assert "level sets of a posynomial function of the metrics" in " ".join(front.split())
    # R-38 (c): the abstract does not carry the scaling sentence
    assert "scales where" not in front
    # the three objects stay apart, one definition each (his review of 2026-11-15)
    definitions = _section("Definitions")
    assert "The Pareto boundary is the nondominated set" in definitions
    assert "not of the table or of the fit" in definitions
    assert "The fitted reference surface is the level set" in definitions
    sentence = _cell_out(PAPER_NB, "num-nondominated")
    assert "236 on 4 attributes" in sentence and "2,134 on all 13" in sentence
    assert "regenerations of the data under rounding-level" in sentence


def test_cr8_the_k_comparison_is_read_at_the_one_term_temperature_and_names_the_cases_k():
    """(8) the mean slack across K at one temperature, and the K the checks pick (B.10; the
    supervisor's call of 2026-11-11, WP30-decisions.md, "The choice of K in the case")."""
    import case

    sentence = _cell_out(PAPER_NB, "num-choosing-k")
    assert "Appendix B.10" in sentence and "at the K = 1 temperature" in sentence
    assert f"point to K = {case.CASE_K}" in sentence and "none deciding alone" in sentence
    assert "the step where a thin term appears" in sentence
    assert "resampling" not in sentence  # WP39 D-5: the movement stays in B.10's table
    cell = _cell_out(SUPPORT_NB, "tab-B-choosing_k")
    assert "at the K = 1 temperature" in cell and "The checks point to K = 2." in cell


def test_the_case_reads_one_named_k():
    """The several-term reading of the case is ``case.CASE_K``: no figure, cell or generated
    sentence of the case analysis names a K of its own."""
    import inspect

    import case
    import generate_findings as gf

    assert case.CASE_K == 2
    for name in ("planes.py", "chart_level.py"):
        src = (ROOT / "paper" / "figures" / name).read_text(encoding="utf-8")
        assert "CASE_K" in src and "fits[3]" not in src and "n_terms=3" not in src, name
    cells = {c.id: _src(c) for c in _nb(PAPER_NB).cells}
    assert "case.CASE_K" in cells["fit-case"] and "fit_case" in cells["fig-tension-matrix"]
    assert 'triangle="upper", order="tension"' in cells["fig-tension-matrix"]
    assert not [i for i, t in cells.items() if "fits[3]" in t or "fit3" in t]
    for fn in (gf.terms_sentence, gf.elasticity_sentence, gf.choosing_k_sentence):
        assert "CASE_K" in inspect.getsource(fn), fn.__name__


@pytest.mark.slow
def test_choosing_k_picks_the_cases_k_on_both_regimes_and_the_prose_quotes_the_table():
    """The checks pick K = 2 on both regimes at the precision the conclusion needs; the table, the
    sentence of Section 9 and the committed outputs agree (the digits are two or three, so a
    last-digit change of the data moves none of these statements)."""
    import case
    import generate_findings as gf
    import generate_results as gr

    for regime, t in gr.choosing_k_tables().items():
        assert case.chosen_k(t) == case.CASE_K == 2, regime
        t = t.set_index("K")
        assert t.loc[2, "drop"] > t.loc[3, "drop"] > t.loc[4, "drop"] > 0, regime
        own = t["thinnest share, own tau"]
        assert own[2] > 0.2 and own[3] < 0.1, regime  # a thin term appears at K = 3
        assert t.loc[4, "movement"] > 0.5 > t.loc[2, "movement"], regime  # a splinter at K = 4
    table, sentence = str(gr.choosing_k()), str(gf.choosing_k_sentence())
    _current(_cell_out(SUPPORT_NB, "tab-B-choosing_k"), table, "choosing_k")
    _current(_cell_out(PAPER_NB, "num-choosing-k"), sentence, "num-choosing-k")
    quoted = set(re.findall(r"\b\d\.\d\d\b", sentence))
    tabled = {f"{float(x):.2f}" for x in re.findall(r"\b\d\.\d{2,3}\b", table)}
    assert quoted and quoted <= tabled


@pytest.mark.slow
def test_the_planes_figures_bottom_panel_is_one_terms_line():
    """The caption of the planes figure says the pair both terms weigh shows term 2's line alone:
    the surface in that slice is the lower of the two lines and it is term 2's across the range."""
    import case

    sys.path.insert(0, str(ROOT / "paper" / "figures"))
    import planes

    study = case.load_study("primary")
    fits = case.k_fits(study, (1, case.CASE_K))
    est, band = fits[case.CASE_K].estimator, fits[1].band
    _, k_terms, plotting = case._lib()
    U = np.log(study.M)
    labels = plotting.cell_labels(est, study.M)
    drawn = {}
    for j, k in k_terms.slice_pairs(est):
        keep, ws, bs = k_terms._slice(est, U, labels, band, j, k)
        g = np.linspace(U[:, j].min(), U[:, j].max(), 400)
        _, who = planes._envelope(ws, bs, g)
        drawn[(study.names[j], study.names[k])] = sorted({keep[f] + 1 for f in who}), keep
    assert drawn[("pointing error", "peak slew power")] == ([1], [0])
    assert drawn[("available power", "unit cost")] == ([2], [0, 1])


def test_cr9_the_margin_and_the_radius_are_read_against_the_band_and_the_median_margin():
    """(9) one sentence in section 6 and the table in B.4."""
    import generate_results

    sentence = _cell_out(PAPER_NB, "num-margin")
    assert "band 1/tau" in sentence and "median best-minus-second-best" in sentence
    cell = _cell_out(SUPPORT_NB, "tab-B-margin_reading")
    _current(cell, str(generate_results.margin_reading()), "margin_reading")
    ids = [c.id for c in _nb(PAPER_NB).cells]
    last = ids.index("sec-case-construction")
    assert ids.index("num-certificates") < ids.index("num-margin") < last


def test_the_proposers_radius_is_the_stated_rule_of_the_check_designs():
    """Section 9 states the rule that sets the radius; the proposer runs it; no value is typed."""
    import paper_paths  # noqa: F401  (examples/adcs on the path)
    from experiments import check_designs

    # WP56 moved the rule from Section 8 to B.6; WP57c landed it there
    text = _norm_ws(_cell_src("app-B-6", SUPPORT_NB))
    assert check_designs.REACH_QUANTILE == 0.02 and check_designs.HOLES == 300
    assert (
        "a radius that a stated rule sets from the data: the 2nd percentile of the pool's nearest "
        "predicted distances to the 300 most isolated points of white space"
    ) in text
    assert not re.search(r"\d\.\d{2,}", text)  # the value is the data's, not typed


def test_cr10_the_discussion_says_what_propose_predict_check_showed_and_did_not():
    """(10) The regressor's error is one quantity (the predicted level and the predicted position
    both within its band of the measured one, as Section 9 says) and where the proposals landed
    is another (the measured log V against zero); the Discussion says both, from the same table
    and no claim that the position failed where Section 9 reports 3 of 3 (final round, change
    request 43)."""
    ids = [c.id for c in _nb(PAPER_NB).cells]  # WP56: the reading goes to B.6; Section 8 keeps
    assert "num-predict-reading" not in ids  # the finding in one sentence
    assert "by spending the battery" in _cell_src("sec-case-analysis-5b")
    text = _moved("num-predict-reading")
    assert "It showed that" in text and "remains a hypothesis" in text
    assert "the easy part" not in text and "It did not show" not in text
    assert "a second quantity, the measured log V against zero" in text
    sec9 = _cell_out(PAPER_NB, "num-predict")
    lv, z = re.search(r"\((\d) of (\d) and (\d) of \2\)", text).group(1, 3)
    assert f"for {lv}, and the predicted position within that band for {z}" in sec9
    assert "four-metric fitted reference surface" in text and "feasibility condition" in text


@pytest.mark.slow
def test_cr11_chaining_with_pca_is_worked_on_the_case_in_d16():
    """(11) One worked result, in B.11, with a pointer from the text (Section 1's main-results item
    was cut at his review of 2026-11-15; Section 2's HoroPCA paragraph points to it)."""
    import generate_results

    assert "Appendix B.11" in _section("Prior art")
    cell = _cell_out(SUPPORT_NB, "tab-B-pca_chain")
    _current(cell, str(generate_results.pca_chain()), "pca_chain")
    assert "Share of the spread" in cell
    import paper_stability

    quantities = paper_stability.extra()["quantities"]
    leading = [n for n in quantities if n.startswith("pca |") and n.endswith("leading metrics")]
    assert len(leading) == 3 and all(quantities[n]["identical"] for n in leading)


def test_cr12_every_hypothesis_label_is_worded_or_explained():
    """(12) The I labels carry their words where first used in the results (A is worded in
    Sections 3 and 5, R beside its result; the F labels and I4 live in Appendix E since WP55 took
    the sketches out of the main text)."""
    results = _section("Results")
    for label, words in {
        "I10": "first-order conditions", "I11": "convex on every line is convex",
        "I5": "moment generating functions", "I9": "Cauchy-Schwarz",
        "I8": "first-order convexity", "I6": "implies", "A8": "a partition into nonempty cells",
    }.items():  # fmt: skip
        first = re.search(rf"\b{label}\b", results)
        assert first, label
        assert words in results[max(first.start() - 60, 0) : first.start() + 160], (label, words)


def test_cr13_the_first_generated_range_says_what_varies():
    """(13) The generated nondominated sentence says what varies and where the digits hold."""
    first = _cell_out(PAPER_NB, "num-nondominated")
    # WP23 data gate (D-9 item 5): on the nine-metric data no nondominated count moves, so the
    # sentence prints no range and says what a range would be; a count that moves is a range.
    assert re.search(r"\d+ to \d+", first) or "is printed as a range" in first
    assert "five regenerations of the data under rounding-level perturbation" in first
    assert "Appendix B.7" in first
    # The sentence left Section 1 for Case analysis on his word (2026-11-15, WP11-decisions.md),
    # so it is no longer the text's first range; what it says about a range still holds.


def test_cr15_appendix_b_says_where_two_statements_share_a_script():
    """(15) Proposition 3 and its corollary (the approximate certificate) share a file, as do
    Level 1 (descent) and the finite termination of the sharp alternation; each entry says so."""
    text = str(generate_proofs.proofs_solver())
    shared = {f: lem for f, lem in _record()["lemmas"].items() if len(lem["results"]) > 1}
    assert set(shared) == {"lemma_14_assignment_stable.py", "lemma_15_descent.py"}
    assert text.count("**Shared script.**") == sum(len(lem["results"]) for lem in shared.values())
    assert "each proof lists its own steps in the file's order" in text
    assert "**Shared script.**" not in str(generate_proofs.proofs_fit())


def test_cr18_appendix_f_says_how_to_compare_regenerate_and_what_needs_a_checkout():
    """(18) git checkout, the exact comparison command, one row, and the site build line."""
    cells = _appendix_cells(_nb(SUPPORT_NB))["H"]
    prose = "\n".join(_src(c) for c in cells if c.cell_type == "markdown")
    assert "git checkout" in prose and "skip with a reason" in prose
    commands = str(generate_repro.commands())
    assert "git diff --stat -- paper/paper.ipynb paper/supporting_material.ipynb" in commands
    assert "PAPER_EXECUTE=1 uv run pytest tests/test_paper.py -k clean_kernel" in commands
    assert "uv run python paper/regenerate_row.py ROW" in commands
    assert (ROOT / "paper" / "regenerate_row.py").is_file()


def test_cr18_regenerate_row_reproduces_the_committed_output_of_a_row():
    """The script runs the cells a row needs and prints what the committed cell holds."""
    import regenerate_row

    for row, nb_path in (("tab-D-register", SUPPORT_NB), ("tab-H-commands", SUPPORT_NB)):
        assert regenerate_row.run(row) is not None
        assert str(regenerate_row.run(row)).strip() == _cell_out(nb_path, row).strip(), row
    with pytest.raises(SystemExit):
        regenerate_row.run("no-such-row")


def test_cr18_the_commit_row_says_so_when_there_is_no_checkout(monkeypatch):
    """Outside a checkout the toolchain table says the commit is not available."""
    monkeypatch.setattr(generate_repro, "ROOT", Path("/"))
    assert generate_repro._run(["git", "rev-parse", "HEAD"]) == "not available"


def test_the_added_quantities_are_recorded_on_the_same_five_regenerations():
    """The numbers added after the sensitivity run carry the digits that held on the same data."""
    record = json.loads((PAPER / "stability_extra.json").read_text(encoding="utf-8"))
    assert record["seeds"] == [1, 2, 3, 4, 5]
    assert record["perturbation"]["relative_half_width"] == 1e-12
    for name, e in record["quantities"].items():
        if "min" in e:
            assert e["min"] <= e["committed"] <= e["max"], name
    groups = {n.split(" | ")[0] for n in record["quantities"]}
    assert groups == {"margin", "pca", "decision", "requirement"}  # WP56: Section 8's exclusions


# -- legible figures and their full-size files (the driver's, WP10) -------------------------------

FIGURE_COLUMN_PX = 842
"""Width of the figure column of the site at a 1280 px window (measured in the built page)."""
MIN_TEXT_PX = 12.0
"""The smallest type a figure may show on the page: the body's small print, 12 to 13 px."""


def _png_size_and_dpi(data: bytes) -> tuple[int, float]:
    """Width in pixels and resolution in dots per inch of a PNG (its ``pHYs`` chunk)."""
    import struct

    assert data[:8] == b"\x89PNG\r\n\x1a\n"
    width = struct.unpack(">I", data[16:20])[0]
    pos, dpi = 8, None
    while pos < len(data):
        n, kind = struct.unpack(">I4s", data[pos : pos + 8])
        if kind == b"pHYs":
            dpi = struct.unpack(">I", data[pos + 8 : pos + 12])[0] * 0.0254
            break
        pos += 12 + n
    assert dpi, "the PNG records no resolution"
    return width, dpi


def _figure_images() -> dict[str, tuple[bytes, float]]:
    """Each figure of the paper: its PNG bytes and the smallest type size in points drawn in it."""
    import base64

    import case

    sys.path.insert(0, str(PAPER / "figures"))
    out = {}
    for c in _code_cells(_nb(PAPER_NB)):
        if c.id.startswith("fig-"):
            png = next(
                o["data"]["image/png"] for o in c.outputs if "image/png" in o.get("data", {})
            )
            out[c.id] = (base64.b64decode(png), case.FIGURE_MIN_FONT_PT)
    return out


def test_every_figure_shows_its_smallest_text_at_the_body_small_print_size_at_1280_px():
    """Text size on the page = type size (pt) / 72 x resolution x the scale at which the column
    shows the image (the column is FIGURE_COLUMN_PX wide; an image narrower than it is not
    stretched). Figure 6 was shown at 0.40 of its size and its 7 pt labels were 4 px."""
    images = _figure_images()
    assert len(images) == 3  # the case's figure cells (WP19 P-7, P-10; WP56 adds the ternary)
    for name, (data, min_pt) in images.items():
        width, dpi = _png_size_and_dpi(data)
        scale = min(1.0, FIGURE_COLUMN_PX / width)
        px = min_pt / 72 * dpi * scale
        assert px >= MIN_TEXT_PX, (name, round(px, 1), width, round(scale, 2))


def test_every_figure_has_a_full_size_link_to_a_file_that_is_the_figure():
    nb = _nb(PAPER_NB)
    images = _figure_images()
    for cid in images:
        cap = next(c for c in nb.cells if c.id == f"{cid}-caption")
        m = re.search(r"\[full-size figure\]\((figures/[\w.-]+\.png)\)\s*\n:::\s*$", _src(cap))
        assert m, cid
        assert (PAPER / m.group(1)).read_bytes() == images[cid][0], f"{cid}: {STALE}"
    assert not (PAPER / "figures" / "fig-schematic.png").exists()


def test_the_figure_functions_hold_every_text_at_the_minimum_size(monkeypatch):
    """The decorator of case.py raises smaller text to the floor and checks it."""
    import case
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.text import Text

    @case._legible
    def draw():
        fig, ax = plt.subplots(figsize=(case.FIGURE_WIDTH_IN, 3))
        ax.annotate("small", (0.5, 0.5), fontsize=5)
        ax.set_title("title", fontsize=6)
        return fig

    fig = draw()
    sizes = {t.get_text(): t.get_fontsize() for t in fig.findobj(Text) if t.get_text().strip()}
    assert min(sizes.values()) >= case.FIGURE_MIN_FONT_PT, sizes
    assert fig.get_size_inches()[0] * case.FIGURE_DPI <= FIGURE_COLUMN_PX
    plt.close(fig)


# ---- WP30 cascade: the case's body sentences (thirteen metrics, cost coverage, the draw) ---------


def test_the_article_before_a_lemma_count_is_read_aloud(case_sentences):
    """An 8-lemma, an 11-lemma, an 18-lemma, an 80-lemma; a 1-, 7-, 9-, 10- and 12-lemma."""
    import generate_findings as gf

    cases = {1: "a", 7: "a", 8: "an", 9: "a", 10: "a", 11: "an", 12: "a", 18: "an", 19: "a"}
    cases |= {80: "an", 89: "an", 100: "a", 800: "an", 1100: "a", 11000: "an", 18000: "an"}
    assert {n: gf._a(n) for n in cases} == cases
    text = str(case_sentences["num-regimes"])
    for m in re.finditer(r"\b(a|an) (\d+)-lemma", text):
        assert gf._a(int(m.group(2))) == m.group(1), m.group(0)
    assert "a 7-lemma and an 8-lemma" in text and "a 8-lemma" not in text


def test_the_two_metrics_in_no_contending_set_are_the_computed_ones(case_sentences):
    """The sentence names the metrics that no term of any fit at K = 1 to 3 in either regime
    contends with, and says what it reads each against."""
    import case

    never = None
    for regime in case.CUBESAT.regimes:
        study = case.load_study(regime)
        for fit in case.k_fits(study).values():
            used = {study.names[j] for rep in case._reports(study, fit) for j in rep.contending_set}
            never = set(study.names) - used if never is None else never & (set(study.names) - used)
    text = str(case_sentences["num-participation"])
    assert never == {"power margin", "battery peak power ratio"}, never
    assert (
        "Of the thirteen traded metrics, two, the power margin and the battery peak power ratio,"
        in text
    )
    assert "exact-maximum fit) at K = 1 to 3 in either regime" in text
    assert "|Spearman| at least 0.97" in text


def test_the_body_states_the_marks_the_coverage_and_the_draw():
    """Section 8: three measures of effectiveness among the thirteen, the cost coverage with the two
    budgets of the model, and the draw of 3,000 designs per regime of the data of record."""
    import csv

    marks = {}
    with (ROOT / "examples" / "adcs" / "model_v2" / "views" / "coverage.csv").open(
        encoding="utf-8"
    ) as f:
        for row in csv.reader(f):
            if row[0] == "metrics":  # the file's second table: table, metric, mark, ...
                marks[row[1]] = row[2]
    assert len(marks) == 13
    assert {m for m, v in marks.items() if v == "MoE"} == {
        "pointing error",
        "unit cost",
        "fleet cost",
    }
    body = _section("Case construction")
    assert (
        "the pointing error, the unit cost and the fleet cost are MoEs, "
        "the other ten traded metrics MoPs" in body
    )
    model = (ROOT / "examples" / "adcs" / "model_v2" / "cubesat.sysml").read_text(encoding="utf-8")
    assert "attribute fleetCostLimit : Real = 6.0e6" in model and "8,000,000 USD" in model
    assert "attribute fleetSize : Real default = 1.0" in model  # a Cubesat attribute, no part
    view = (ROOT / "examples" / "adcs" / "model_v2" / "views" / "assembly_view.puml").read_text(
        encoding="utf-8"
    )
    assert "fleet" not in view.lower()  # the assembly view draws parts only
    assert "the fleet size $n$, a count that is no part, so" in body
    assert "The fleet size is drawn from 1 to 30" in body
    assert "A fourth MoE, the fleet's coverage probability" in body  # WP56
    # WP56: the budget sentence left Section 7 for F.8, which states it
    c8 = _src(next(c for c in _nb(SUPPORT_NB).cells if "(sub-f-8)=" in _src(c)))
    assert "under 6,000,000 USD, inside the sponsor's full budget of 8,000,000 USD" in c8
    sys.path.insert(0, str(ROOT / "examples" / "adcs"))
    from experiments import definitions

    n = definitions.SAMPLE_PER_REGIME
    cell = next(c for c in _code_cells(_nb(PAPER_NB)) if c.id == "num-datasets")
    assert f"{n:,} per regime: a design choice of the case" in _out_text(cell)


def _norm_ws(text: str) -> str:
    return re.sub(r"\s+", " ", text)


def test_appendix_c8_states_what_the_model_file_says_about_cost_and_what_is_left_out():
    """F.8 reads the model: prices, budgets and the order of exclusions; the rest of what the case
    leaves out (the load, the limits' kinds) is the case page's, which F.8 cites (WP57c: the mirror
    WP30-rounds/appendix-f-leaves-out.md followed F.8's paragraph and left with it)."""
    model = _norm_ws(
        (ROOT / "examples" / "adcs" / "model_v2" / "cubesat.sysml").read_text(encoding="utf-8")
    )
    c8 = _norm_ws(_src(next(c for c in _nb(SUPPORT_NB).cells if c.id == "app-F-8")))
    page = _norm_ws((ROOT / "examples" / "adcs" / "case-model.md").read_text(encoding="utf-8"))
    assert "examples/adcs/case-model.md" in c8 and "What the case leaves out" in c8
    for model_has, c8_has in [
        ("attribute launchRate : Real = 7000.0", "7,000 USD per kilogram"),
        (
            "100,000 USD for one satellite (unsourced)",
            "100,000 USD for one satellite, has no source",
        ),
        ("attribute unitCostLimit : Real = 350000.0", "350,000 USD per satellite"),
        ("attribute fleetCostLimit : Real = 6.0e6", "under 6,000,000 USD"),
        ("full fleet budget is 8,000,000 USD", "full budget of 8,000,000 USD"),
        ("remaining 2,000,000 USD", "remaining 2,000,000 USD"),
        (
            "a 1U series can sit below 40,000 USD a unit",
            "a 1U series can sit below 40,000 USD a unit",
        ),
        (
            "a single satellite of this class costs more",
            "which no single satellite of this class clears",
        ),
        ("fleet size 1 to 30", "one to thirty identical satellites"),
        ("2026 vendor and marketplace listings", "2026 vendor and marketplace listings"),
    ]:
        assert model_has in model, model_has
        assert c8_has in c8, c8_has
    assert "housekeeping and payload 12 W" in model and "a constant 12 W load" in page
    budgets = re.findall(r"attribute (\w+(?:Limit|Budget)) :", model)
    assert (
        len(budgets) == 6 and "Four requirement limits" in page and "two are cost budgets" in page
    )
    order = [  # the model's order of exclusions, and F.8's (the supervisor's, 2026-11-11, 10:35)
        "payload and its instruments", "communications", "flight software",
        "environmental testing beyond the assembly line", "licensing",
        "ground station network and operations", "launch slot minimum", "broker fees",
    ]  # fmt: skip
    for text in (model, c8):
        at = [
            text.index(item, text.index("excludes" if text is model else "leaves out the"))
            for item in order
        ]
        assert at == sorted(at), "the exclusions are in the supervisor's order"
    kinds = r"(?:part|attribute|calc|requirement|action|analysis)\s+(?:def\s+)?"
    left_out = r"\w*(?:thermal|schedule|fault|redundan|communic|growth|desaturat)"
    absent = kinds + left_out
    assert not re.search(absent, model, re.I), "the model names no element of what is left out"
    assert not (ROOT / "work-packages" / "WP30-rounds" / "appendix-f-leaves-out.md").exists()


def test_appendix_c8_list_states_numbers_the_data_and_the_model_give():
    """The case page's list of what the case leaves out (F.8's list until WP57c) prints numbers: the
    smallest pointing error, the launch slot's effect at fleets of one to three, the traded mass
    over the fixed bus; each is computed from the feasible designs of both regimes."""
    import case
    import pandas as pd

    page = _norm_ws((ROOT / "examples" / "adcs" / "case-model.md").read_text(encoding="utf-8"))
    c8 = page  # the list moved to the case page with WP57c
    model = _norm_ws(
        (ROOT / "examples" / "adcs" / "model_v2" / "cubesat.sysml").read_text(encoding="utf-8")
    )
    feasible = pd.concat(
        [case.load_study(r).feasible for r in case.CUBESAT.regimes], ignore_index=True
    )
    mass = feasible["total_mass_kg"].to_numpy()
    fixed = 10.0 + 0.5 + 0.1  # bus, antenna, inertial unit (the model's three fixed masses)
    for part in ("attribute mass : MassValue = 10.0 [kg]", "= 0.5 [kg]", "= 0.1 [kg]"):
        assert part in model
    assert "50 kg minimum slot (350,000 USD)" in model and "launchRate : Real = 7000.0" in model
    assert "attribute horizon : TimeValue = 600.0 [s]" in model
    assert f"{feasible['pointing_error_deg'].min():.4f} degree" in c8
    assert f"{(mass - fixed).min():.1f} to {(mass - fixed).max():.1f} kg of traded parts" in c8
    assert f"on about {fixed:.1f} kg of fixed bus" in c8
    assert f"spans {mass.min():.1f} to {mass.max():.1f} kg" in c8
    assert float(feasible["panel_span_m"].max()) < 1.0 and "up to 1.0 m a side" in c8
    factor = {n: 50.0 / (n * mass) for n in (1, 2, 3)}  # the slot over the linear rate, per fleet
    assert f"{factor[1].min():.1f} to {factor[1].max():.1f} times at one satellite" in c8
    assert f"{factor[2].min():.1f} to {factor[2].max():.1f} at two" in c8
    assert f"at most {factor[3].max():.1f} at three" in c8
    assert (factor[3] >= 1.0).all()  # the slot still binds at three
    assert "0.0006 degree" in page and "50 kg" not in _cell_src("app-F-8", SUPPORT_NB)


@pytest.mark.slow
def test_d7_says_two_candidates_sit_beyond_the_thresholds_met_surface_and_none_meets_them():
    """The old D.7's sentence (P8 final read F4): on the one-term fit to the feasible designs that
    meet the four performance thresholds, fast_effort_hungry and precise_heavy_sensor score above
    the surface (log V +0.315, +0.354) and light_slow below it; none of the three candidates, nor
    the baseline configuration, meets all four thresholds."""
    import case

    placement = case.design_sets_placement(sets={"primary": case.design_sets("primary")})
    rows = placement.set_index("design")
    log_v = lambda name: float(rows.loc[name, "fit on thresholds met"].split()[0])  # noqa: E731
    # WP57c: the old D.7 in B.12
    d7 = _norm_ws(_cell_out(SUPPORT_NB, "tab-B-design_sets_comparison"))
    assert f"fast_effort_hungry (log V {log_v('fast_effort_hungry'):+.3f})" in d7
    assert f"precise_heavy_sensor ({log_v('precise_heavy_sensor'):+.3f})" in d7
    assert log_v("light_slow") < 0 and "two of the three candidates" in d7
    for name in ("baseline configuration", "fast_effort_hungry", "precise_heavy_sensor",
                 "light_slow"):  # fmt: skip
        assert not rows.loc[name, "meets the thresholds"], name
    assert "none of the three, nor the baseline configuration, meets all four thresholds" in d7


@pytest.mark.slow
def test_appendix_e_rows_g2_and_g17_carry_the_thirteen_metric_record():
    """The evidence cells of G-2 and G-17 hold the numbers of the data of record (thirteen metrics,
    3,000 designs per regime), recomputed by the ledger's recipes M3 and M5 and from the sensitivity
    record: none of the eight-metric, 1,000-design numbers is left in the ledger."""
    import json

    import case

    note = _norm_ws((NOTES / "abstraction-gaps.md").read_text(encoding="utf-8"))
    for stale in ("eight-metric", "eight attributes", "eight fitted", "659 of 706", "74 of 685",
                  "five participants", "7.09"):  # fmt: skip
        assert stale not in note, stale
    _, k_terms, _ = case._lib()
    cond = {}
    for regime in ("primary", "stock"):
        study = case.load_study(regime)
        for K in (1, 2):
            cond[regime, K] = np.atleast_1d(case.fit_study(study, K).estimator.conditioning_)
    assert (
        f"$K=1$ {cond['primary', 1][0]:.3f} (primary), {cond['stock', 1][0]:.3f} (baseline)" in note
    )
    two = lambda r: ", ".join(f"{c:.3f}" for c in cond[r, 2])  # noqa: E731
    assert f"$K=2$ primary {two('primary')}" in note and f"baseline {two('stock')}" in note
    moves = {}
    for regime in ("primary", "stock"):
        study = case.load_study(regime)
        fit = case.fit_study(study, 1)
        base = np.atleast_2d(fit.estimator.exponents_)[0]
        top = int(np.argmax(base))
        moves[regime] = []
        for mult in (0.5, 2):
            w = np.atleast_2d(
                k_terms.fit_k(study.M, 1, fit.tau * mult, study.spec.seed).exponents_
            )[0]
            moves[regime].append((abs(w[top] - base[top]), int((w > 1e-3).sum())))
    assert (
        "moves the largest exponent by {:.3f} and {:.3f} (primary".format(
            *(m for m, _ in moves["primary"])
        )
        in note
    )
    assert "{:.3f} and {:.3f} (baseline".format(*(m for m, _ in moves["stock"])) in note
    assert [n for _, n in moves["primary"]] == [8, 7] and [n for _, n in moves["stock"]] == [9, 9]
    record = json.loads(
        (ROOT / "examples/adcs/experiments/reports/sensitivity.json").read_text(encoding="utf-8")
    )["quantities"]
    moved = [v for v in record.values() if not v["identical"]]
    big = [v for v in moved if "max" in v and abs(v["max"] - v["min"]) > 1e-12]
    numbers = [v for v in moved if "min" in v]  # the one text quantity is the certificate sentence
    assert f"{len(moved)} of the record's {len(record)} quantities: {len(numbers)} numbers" in note
    assert f"{len(big)} of the numbers by more than" in note
    nd = record["nondominated | primary | all attributes | nondominated"]["committed"]
    four = record["nondominated | primary | four metrics | nondominated"]["committed"]
    assert (
        f"all {nd:,} feasible designs on the thirteen attributes, {four} on the four-metric" in note
    )


def test_the_charts_axis_names_the_metrics_of_the_first_direction_of_d16():
    """The chart's axis says which metrics a step to the right improves or worsens: the leading
    loadings of B.11's first direction (K = 1, primary regime), by sign. The caption names none."""
    import case
    from figures.chart_level import leading_direction

    study = case.load_study("primary")
    better, worse, _ = leading_direction(study, case.fit_study(study))[1:]
    text = _out_text(next(c for c in _code_cells(_nb(SUPPORT_NB)) if c.id == "tab-B-pca_chain"))
    row = next(r for r in text.splitlines() if r.startswith("| 1 |"))
    loads = [m.rsplit(" ", 1) for m in row.split("|")[3].strip().split(", ")]
    assert better == [n for n, v in loads if v.startswith("+")]
    assert worse == [n for n, v in loads if v.startswith("-")]
    caption = _src(next(c for c in _nb(PAPER_NB).cells if c.id == "fig-chart-level-caption"))
    assert "the axis names the metrics it improves" in caption and "to the right" not in caption


# ---- WP39 D-3: the decision generator -----------------------------------------------------------


@pytest.fixture(scope="module")
def decided():
    """The study, its K = 1 and K = 2 fits and the decision computed from them (fit once)."""
    import case
    import generate_findings as gf

    study = case.load_study("primary")
    fits = case.k_fits(study, (1, case.CASE_K))
    return study, fits, gf.decision(study, fits)


@pytest.mark.slow
def test_the_decision_reproduces_the_spikes_numbers_and_every_named_design_is_in_the_shortlist(
    decided,
):
    """R-6: 2,134 feasible, 548 pass six, 28 in the band of both fits, the named designs among them
    and passing the six requirements; the picks and the dollars of the narration."""
    import case

    study, _, d = decided
    assert d.counts == {"feasible": 2134, "six_pass": 548, "working": 28, "nondominated": 11,
                        "nondominated_in_band": 1, "nondominated_working": 5,
                        "nondominated_coverage": 17}  # fmt: skip
    w = d.working
    assert list(w["fleet_cost_usd"]) == sorted(w["fleet_cost_usd"])
    assert {k: int(v["design_id"]) for k, v in d.picks.items()} == {
        "sponsor": 999, "cheapest unit": 2356, "operator": 2950, "between": 1858,
        "balanced": 766, "fine": 1858, "coverage": 2356, "fleet and coverage": 893,
    }  # fmt: skip
    assert int(w["nd coverage"].sum()) == 17 and bool(
        w.loc[w["design_id"] == 893, "nd coverage"].iloc[0]
    )
    assert set(w.loc[w["nd"], "design_id"]) == {190, 766, 999, 1858, 2950}
    ids = set(w["design_id"])
    raw = study.feasible.set_index("design_id")
    for row in d.picks.values():
        assert row["design_id"] in ids
        assert case.requirement_mask(raw.loc[[row["design_id"]]], study.spec, costs=True).all()
    assert round(_tracker_cost_of(d), -3) == 559_000
    assert d.baseline["pointing_error_deg"] == pytest.approx(0.0155349, rel=1e-5)
    assert d.baseline["unit_cost_usd"] == 461_360.0


def test_d19_states_section_8s_four_rules_and_no_other():
    """WP57c R-4: B.14's rule paragraph names the four rules of Table 3 (one stakeholder per
    objective, and the pick between sponsor and operator) and not the rules they replaced (the
    operator's pointing error, the pick balanced between the terms); the shortlist table carries
    the coverage probability and its nondominated mark."""
    rules = _cell_src("app-B-decision", SUPPORT_NB)
    table = _cell_out(PAPER_NB, "tab-decision")
    names = [r.split(" | ")[0].strip("| ") for r in table.splitlines()[3:]]
    assert names == [
        "sponsor: least fleet cost",
        "manufacturer: least unit cost",
        "operator: largest coverage probability",
        "between sponsor and operator",
    ]
    for name in names:
        assert name in rules, name
    assert "fleet cost and coverage probability" in rules and "minimax regret" in rules
    assert "pointing error" not in rules.replace("the pointing error.", "")  # only as an input
    assert "balanced between the terms" not in rules and "term levels" not in rules
    head = _cell_out(SUPPORT_NB, "tab-B-decision_designs").split("\n\n", 1)[1].splitlines()[0]
    assert "| coverage probability |" in head
    assert head.rstrip(" |").endswith("nondominated on fleet cost and coverage probability")
    assert "sent-B-decision" not in [c.id for c in _nb(SUPPORT_NB).cells]


def _tracker_cost_of(d):
    import generate_findings as gf

    return gf._tracker_cost(d)


def test_the_decisions_quantities_were_measured_on_the_same_regenerations_and_none_moved():
    """WP39 R-1: the counts, pointing errors, prices and the fine tracker's cost are in the
    stability results; none moved at one part in 10^12, so the narration prints them exactly (a
    quantity that moves must be narrated with "about", and its claims-register row says so)."""
    record = json.loads((PAPER / "stability_extra.json").read_text(encoding="utf-8"))["quantities"]
    mine = {n: e for n, e in record.items() if n.startswith("decision | primary | ")}
    for n in ("count | feasible", "count | six_pass", "count | working", "count | nondominated",
              "count | nondominated_in_band", "sponsor | pointing_error_deg",
              "fine | pointing_error_deg", "between | fleet_cost_usd", "between | unit_cost_usd",
              "sponsor | fleet_cost_usd", "fine tracker | extra fleet cost",
              "count | nondominated_coverage", "coverage | coverage_probability",
              "sponsor | coverage_probability", "fleet and coverage | fleet_cost_usd",
              "fleet and coverage | coverage_probability",
              "cheapest unit | unit_cost_usd"):  # fmt: skip
        assert f"decision | primary | {n}" in mine, n
    assert all(e["identical"] for e in mine.values())
    assert all(isinstance(e["committed"], int) for n, e in mine.items() if "| count |" in n)
    req = {n: e for n, e in record.items() if n.startswith("requirement | primary | ")}
    assert len(req) == 8 and all(e["identical"] for e in req.values())  # six, jointly, the band


@pytest.mark.slow
def test_the_decision_paragraph_and_tables_are_formatted_from_the_generated_values(decided):
    import generate_findings as gf

    _, _, d = decided
    text = str(gf.decision_sentence(d))
    plain = re.sub(r"<[^>]+>", "", text)
    for phrase in ("2,134 feasible designs to a shortlist of 28 that pass all six requirements",
                   "On it the manufacturer and the operator pick the same fleet: 25 medium-wheel, "
                   "medium-tracker satellites at 234,000 USD each, 5.85 M USD for the fleet and a "
                   "coverage probability of 0.98",
                   "The sponsor picks 4 small-wheel, medium-tracker satellites at 1.13 M USD, with "
                   "a coverage probability of 0.46",
                   "how much fleet cost a gain in coverage probability is worth",
                   "Of the 17 shortlisted designs that no other beats on both, the fleet of 10 "
                   "small-wheel, medium-tracker satellites at 2.88 M USD, with a coverage "
                   "probability of 0.76", "Appendix B.14"):  # fmt: skip
        assert phrase in plain, phrase
    assert 120 <= len(plain.split()) <= 190
    table = str(gf.decision_table(d)).splitlines()
    assert table[0].split(" | ")[0] == "| rule" and len(table) == 2 + 5
    assert [r.split(" | ")[0].strip("| ") for r in table[2:]] == [
        "baseline configuration", "sponsor: least fleet cost", "manufacturer: least unit cost",
        "operator: largest coverage probability", "between sponsor and operator",
    ]  # fmt: skip
    assert "2,882,089" in table[6] and "288,209" in table[6] and "0.762" in table[6]
    assert table[4].split(" | ")[1:] == table[5].split(" | ")[1:]  # one design, two rules
    designs = [r for r in str(gf.decision_designs_table(d)).splitlines() if r.startswith("|")]
    assert len(designs) == 2 + 28
    assert "coverage probability" in designs[0]
    assert sum(r.split("|")[-2].strip() == "yes" for r in designs[2:]) == 17  # Section 8's 17


@pytest.mark.slow
def test_the_decision_follows_the_record_when_the_record_is_perturbed(decided):
    """Perturb the record, not the text: a dearer cheapest design, then a tighter budget; the
    shortlist, the picks, the narration and the table move with it."""
    import dataclasses

    import case
    import generate_findings as gf

    study, fits, base = decided
    raw = study.feasible.copy()
    i = raw.index[raw["design_id"] == 999][0]
    raw.loc[i, "fleet_cost_usd"] = 3_000_000.0  # design 999 now costs 3 M USD, over the others
    d = gf.decision(dataclasses.replace(study, feasible=raw), fits)
    assert int(d.picks["sponsor"]["design_id"]) == 190  # the next-cheapest fleet cost
    text = str(gf.decision_sentence(d))
    assert "The sponsor picks 5 small-wheel, medium-tracker satellites at 1.52 M USD" in text
    assert "1.13 M USD" not in text
    assert "the fleet of 12 small-wheel, medium-tracker satellites at 3.11 M USD" in text  # moved
    assert "1,127,465" not in str(gf.decision_table(d))
    cap = 5_800_000.0  # the cheapest-unit-cost design (5.85 M USD) now exceeds the fleet budget
    capped = dataclasses.replace(
        study.spec,
        cost_requirements={**study.spec.cost_requirements, "fleet_cost_usd": (cap, "USD")},
    )
    d = gf.decision(dataclasses.replace(study, spec=capped), fits)
    assert d.counts["six_pass"] < base.counts["six_pass"] and d.counts["working"] < 28
    assert d.working["fleet_cost_usd"].max() <= cap and 2356 not in set(d.working["design_id"])
    # the paragraph says its premise (the manufacturer's and the operator's picks are one design);
    # under the cap they part (2167 and 390), and the generator raises instead of printing a false
    # sentence
    assert d.picks["cheapest unit"]["design_id"] != d.picks["coverage"]["design_id"]
    with pytest.raises(AssertionError, match="premise"):
        gf.decision_sentence(d)
    assert case.CASE_K == 2


# ---- WP39 D-1, D-2, D-4, D-5: the decision in the notebooks --------------------------------------


def test_section_9_closes_with_the_decision_and_leaves_the_neighbouring_paragraphs_alone():
    """D-1: the closing subsection follows 'Propose, predict, check' and ends the section (WP56:
    the requirements after the fit, the three stakeholders and their ternary, the refit, the
    decision and its table, and the sentence that names the code and data)."""
    ids = [c.id for c in _nb(PAPER_NB).cells]
    tail = ids[ids.index("num-predict") + 1 : ids.index("sec-discussion")]
    assert tail == [
        "sec-case-analysis-5b",
        "sec-case-analysis-req",
        "num-requirements",
        "num-design-sets",
        "sec-case-analysis-decision",
        "fig-fleet-ternary",
        "fig-fleet-ternary-caption",
        "num-fleet-refit",
        "sec-case-analysis-decision-2",
        "decision-case",
        "num-decision",
        "tab-decision",
        "tab-decision-caption",
        "sec-case-analysis-close",
    ]
    kept = (
        "sec-case-analysis-3b",
        "num-regimes",
        "sec-case-analysis-5",
        "num-predict",
    )  # fmt: skip  (WP56: the ternary pair and its paragraph left the paper)
    assert set(kept) <= set(ids)
    assert not [i for i in ids if "ternary-pair" in i]
    cells = {c.id: c for c in _nb(PAPER_NB).cells}
    assert _src(cells["sec-case-analysis-3b"]).startswith("**Two regimes.**")
    assert _src(cells["sec-case-analysis-5"]).startswith("**Propose, predict, check.**")


def test_the_decision_paragraph_is_readable_without_the_subsystem_detail():
    """R-3, R-4, R-5 (WP56: one stakeholder per objective): the three objectives in their words,
    subsystem choices as configuration; no exponent, term, design id or log V in the paragraph; the
    caption points at B.14 and carries no caveat (the limits are Section 9's, once)."""
    text = re.sub(r"<[^>]+>", "", _cell_out(PAPER_NB, "num-decision"))
    assert text.startswith("**The decision.**")
    assert not re.search(r"log V|exponent|\bterms?\b|\bdesign \d|\bid\b|\bV\b", text), text
    for words in ("sponsor", "manufacturer", "operator", "coverage probability", "unit cost",
                  "fleet cost", "wheel", "tracker"):  # fmt: skip
        assert words in text, words
    assert "does not answer it" not in text and "defensible" not in text
    caption = next(c for c in _nb(PAPER_NB).cells if c.id == "tab-decision-caption")
    for phrase in ("{ref}`Appendix B.14 <sub-b-14>`", ":label: tab-decision",
                   "the manufacturer's and the operator's rules pick one design"):  # fmt: skip
        assert phrase in _src(caption), phrase
    assert "schedule" not in _src(caption) and "risk" not in _src(caption)
    assert not re.search(
        r"\d", re.sub(r"B\.14|K = 2|sub-b-14|tab-decision|log V", "", _src(caption))
    )


@pytest.mark.slow
def test_the_decision_tables_and_sentences_in_the_notebooks_are_the_generators_output(decided):
    """D-1, D-2, R-1: the six-row table, the 28-design table and the Appendix B sentences are the
    generator's output (exact in the environment of record)."""
    import generate_findings as gf

    _, _, d = decided
    _current(_cell_out(PAPER_NB, "tab-decision"), str(gf.decision_table(d)), "tab-decision")
    support = _nb(SUPPORT_NB)
    for cid, fresh in (("tab-B-decision_designs", gf.decision_designs_table(d)),
                       ("sent-B-decision-baseline", gf.decision_baseline_sentence())):  # fmt: skip
        _current(_out_text(next(c for c in _code_cells(support) if c.id == cid)), str(fresh), cid)
    base = str(gf.decision_baseline_sentence())
    assert (
        "2,355 feasible designs, 523 that pass the six requirements and 19 within the band" in base
    )
    table = _cell_out(SUPPORT_NB, "tab-B-decision_designs")
    assert table.count("\n| ") >= 28 and "coverage probability" in table


@pytest.mark.slow
def test_the_baseline_row_fails_the_requirements_the_other_rows_meet(decided):
    """The table's baseline row is outside the requirements (pointing error and unit cost); every
    other row is a design of the shortlist, which passes all six (the generator asserts it)."""
    import case

    study, _, d = decided
    spec = study.spec
    assert d.baseline["pointing_error_deg"] > 0.008495
    assert d.baseline["unit_cost_usd"] > spec.cost_requirements["unit_cost_usd"][0]
    assert (
        len(d.working) == 28
        and case.requirement_mask(
            study.feasible[study.feasible["design_id"].isin(d.working["design_id"])],
            spec,
            costs=True,
        ).all()
    )


# ---- the final reader round, wave 1: change requests 1 to 31 (the paper-queue unit) -----------


@pytest.mark.slow
def test_the_baseline_pointing_error_share_is_generated_from_the_data_of_record():
    """CR 8: the share of the baseline regime's feasible designs that pass the pointing-error
    requirement is the generator's value, read from the same mask as B.12's pass column."""
    import case
    import generate_findings as gf

    stock = case.load_study("stock")
    fresh = str(gf.baseline_requirement_sentence(stock))
    table = case.requirements_table(stock, case.k_fits(stock, (1,))[1]).set_index("requirement")
    share = table.loc["pointing error", "pass (feasible)"]
    unit = table.loc["unit cost", "pass (feasible)"]  # WP56: both requirements the baseline fails
    assert (
        f"which {100 * share:.1f} % and {100 * unit:.1f} % of the baseline regime's feasible "
        "designs pass" in fresh
    )
    assert "its pointing error is 0.0155 degree" in fresh and "requirement (0.0085 degree)" in fresh
    assert "its unit cost 461,360 USD" in fresh and "requirement (350,000 USD)" in fresh
    cell = next(c for c in _code_cells(_nb(PAPER_NB)) if c.id == "num-baseline-pointing")
    _current(_out_text(cell), fresh, "num-baseline-pointing")
    assert "63.7" not in _markdown(_nb(PAPER_NB))  # the figure of an earlier record


@pytest.mark.slow
def test_the_discussion_gives_the_contending_set_change_from_the_design_sets_of_the_record():
    """CR 9: how far imposing requirements before the fit moves the one-term contending set is
    the generator's reading of B.12's second table, per regime, with the set's own size."""
    import case
    import generate_findings as gf
    import generate_results as gr

    fresh = str(gf.design_sets_sentence())
    t = case.design_sets_table(sets=gr._design_sets())
    out = {}
    for regime in ("primary", "stock"):
        by = {k: set(v.split(", ")) for k, v in t[t["regime"] == regime].set_index("set")[
            "contending set"].items()}  # fmt: skip
        rec = by["feasible"]
        out[regime] = (len(rec), max(max(len(rec - o), len(o - rec)) for o in by.values()))
    words = {7: "seven", 8: "eight", 2: "two"}
    (n1, w1), (n2, w2) = out["primary"], out["stock"]
    assert w1 == 0 and f"of the primary regime ({words[n1]} metrics) unchanged" in fresh
    assert f"by at most {words[w2]} of its {words[n2]} metrics" in fresh
    cell = next(c for c in _code_cells(_nb(PAPER_NB)) if c.id == "num-design-sets")
    _current(_out_text(cell), fresh, "num-design-sets")
    assert "five metrics" not in _markdown(_nb(PAPER_NB))


@pytest.mark.slow
def test_appendix_e_cubesat_rows_carry_the_temperatures_and_slacks_of_the_data_of_record():
    """CR 11: the cubesat numbers of the gaps ledger (G-1, G-9, G-11, G-13, G-14) are the K = 1, 2,
    3 fits of the feasible designs of each regime (the data of record), not an earlier table."""
    import case

    note = _norm_ws((NOTES / "abstraction-gaps.md").read_text(encoding="utf-8"))
    for stale in ("38.10, 94.42", "0.14579", "0.09269", "0.13579", "3,000 designs per regime"):
        assert stale not in note, stale
    fits = {r: case.k_fits(case.load_study(r)) for r in ("primary", "stock")}
    tau = lambda r: ", ".join(f"{fits[r][K].tau:.2f}" for K in (1, 2, 3))  # noqa: E731
    band = ", ".join(f"{fits['primary'][K].band:.4f}" for K in (1, 2, 3))
    assert f"by $K=1,2,3$: {tau('primary')} (primary); {tau('stock')} (baseline)" in note
    assert f"Band {band} (primary)" in note
    frac = lambda r: ", ".join(f"{fits[r][K].estimator.frac_above_:.3f}" for K in (1, 2, 3))  # noqa: E731
    assert f"Fraction above {frac('primary')} (primary) and {frac('stock')} (baseline)" in note
    obj = lambda r, K: fits[r][K].estimator.loss_  # noqa: E731
    for r, name in (("primary", "primary"), ("stock", "baseline")):
        assert f"{obj(r, 3):.3f} against {obj(r, 1):.3f} ({name}" in note
        assert f"{obj(r, 1):.3f} to {obj(r, 3):.3f} ({name}" in note


# ---- the final reader round, second paper unit (change requests 32 to 92) ----------------------


def _cell_src(cell_id: str, path=PAPER_NB) -> str:
    return _src(next(c for c in _nb(path).cells if c.id == cell_id))


def test_works_cited_says_what_it_holds_and_each_entry_is_cited_in_the_register():
    """44: the shared bibliography holds the main text's sources and Appendix A's; the seven
    entries a reader asked about are each cited by a register row of prior_art.yaml."""
    assert "sources of the main text and of the register" in _cell_src("bibliography")
    cited = {k for e in generate_prior_art.entries() for k in e["cites"]}
    for key in ("ahmadijavid2012entropic", "hirshorn2017nasa", "parnell2021system",
                "charnes1982multiplicative", "charnes1983invariant", "banker1986piecewise",
                "fare1985measurement"):  # fmt: skip
        assert key in cited, key


def test_the_geometric_programming_row_places_its_sparsity_citation():
    """45: Candes et al. 2008 is the reweighted L1 of the package's sparsity option; the row says
    so."""
    row = next(e for e in generate_prior_art.entries() if e["id"] == "gp-maxaffine")
    assert "candes2008enhancing" in row["cites"] and "the sparsity option" in row["short"]["shares"]
    src = (ROOT / "src" / "tradespace" / "solvers.py").read_text(encoding="utf-8")
    assert 'penalty not in (None, "reweighted_l1")' in src
    assert "Candes, Wakin and Boyd (2008)" in src


def test_the_model_states_thirteen_requirements_four_of_them_the_feasibility_conditions():
    """69: the paper names the two sets apart; the model's own text counts them."""
    model = (ROOT / "examples" / "adcs" / "model_v2" / "cubesat.sysml").read_text(encoding="utf-8")
    assert len(re.findall(r"^\s*requirement def \w+", model, re.M)) == 13
    assert "Four are the flags the experiment reports: settled, momentum_ok, power_ok" in model
    body = " ".join(_cell_src("sec-case-construction-1").split())
    assert (
        "The SysML v2 model states thirteen requirements, one for each traded metric, and the case "
        "applies them in the order of"
        in body
        and "Four feasibility conditions remove the designs" in body
        and "six requirements are read after the fit; three filter nothing" in body
    )
    assert "depth-of-discharge feasibility condition" in _cell_src("sec-case-analysis-5b")
    assert "Six of the model's thirteen requirements" in _cell_src("app-B-req", SUPPORT_NB)


@pytest.mark.slow
def test_the_fleet_cost_is_the_unit_cost_times_the_fleet_size():
    """68: the sentence says how the fleet cost is formed; the data of record agree to rounding."""
    import case

    f = case.load_study("primary").feasible
    assert np.allclose(f["fleet_cost_usd"], f["unit_cost_usd"] * f["fleet_size"], rtol=1e-6)
    assert f["fleet_size"].between(1, 30).all()
    assert "the unit cost times the fleet size" in _cell_src("sec-case-construction")


def test_the_k1_exponents_stability_is_not_assessed_in_the_record_and_the_text_says_so():
    """61: B.10's movement column is empty at K = 1 (the dash), so the sentence beside n_eff says
    it is not assessed there."""
    table = _cell_out(SUPPORT_NB, "tab-B-choosing_k")
    assert len(re.findall(r"^\| 1 \| .* \| - \|$", table, re.M)) == 2  # both regimes
    import case
    import generate_findings as gf

    # WP56: the sentence left Section 7 (queued for B.3 and the open questions); its generator
    sentence = str(gf.temperature_variants_sentence(case.load_study("primary")))
    assert "not assessed at K = 1" in sentence and "Appendix B.10" in sentence


def test_the_scaler_sentence_quotes_the_sensitivity_table_row():
    """74: the robust scaler's row of B.3 (its size, the metrics it shares, its largest
    exponent)."""

    sentence = _moved("num-temperature-variants")  # WP56 moved it to B.3; WP57c landed it
    m = re.search(
        r"The `RobustScaler` variant changes the K = 1 contending set: (\d+) metrics, (\d+) of "
        r"the "
        r"baseline's (\d+) among them, the largest exponent on ([a-z ]+)\.",
        sentence,
    )
    assert m, sentence
    table = _cell_out(SUPPORT_NB, "tab-B-sensitivity_variants").split("Dataset")[1]
    row = next(r for r in table.splitlines() if r.startswith("| robust scaler"))
    cols = [c.strip() for c in row.strip("|").split("|")]
    assert (cols[5], cols[8], cols[7]) == (m.group(1), m.group(2), m.group(4))
    base = next(r for r in table.splitlines() if r.startswith("| baseline"))
    assert [c.strip() for c in base.strip("|").split("|")][5] == m.group(3)


def test_the_participation_and_k1_sentences_read_the_record():
    """72, 73, 46: five metrics carry no K = 1 exponent (the figure's undrawn lines), total mass
    carries 0.02 outside the contending set, and R1's uniqueness is a checked test."""
    part = _moved("num-participation")
    assert "carry no exponent at the fit temperature; three of them" in part
    assert "five metrics" not in part and "Five metrics are at most 0.001" in _cell_src(
        "fig-tau-sweep-caption"
    )
    k1 = _cell_out(PAPER_NB, "num-k1")
    assert "total mass also carries 0.02 and is not in the contending set" in k1
    assert "checked by a test of the repository on both regimes" in k1


def test_the_known_answer_sentence_says_what_the_eleven_row_failure_is():
    """76: B.9's record, the failure with the most frontier rows on its thinnest term."""
    sentence = _moved("num-recovery")
    table = _cell_out(SUPPORT_NB, "tab-B-planted_recovery")
    m = re.search(
        r"where every recovered table has at least (\d+); the one with (\d+) is "
        r"(\w+) at temperature 50 and still errs by ([\d.]+), with ([\d.]+) of",
        sentence,
    )
    assert m, sentence
    assert f"Every table recovered has at least {m.group(1)} frontier rows" in table
    row = next(r for r in table.splitlines() if r.startswith(f"| 8 | {m.group(2)} |"))
    got = [c.strip() for c in row.strip("|").split("|")][4:7]
    assert got == [m.group(3), m.group(4), m.group(5)]


@pytest.mark.slow
def test_the_executive_table_caption_band_claim_holds_of_the_picks_and_not_the_baseline(decided):
    """182: "all inside the near-frontier band" is said of the five picks, in the K = 1 band the
    shortlist uses, and the baseline row (the level of Table 2's first row) is outside it."""
    _, fits, d = decided
    band = fits[1].band
    picks = ("sponsor", "cheapest unit", "coverage", "fleet and coverage")  # WP56: Table 3's
    assert all(abs(d.picks[k]["log V K=2"]) < band for k in picks)
    assert abs(d.baseline["log V K=2"]) > band


def test_figure_6_draws_the_band_on_both_sides():
    """175: Definition 4's band is |log V| < 1/tau; the figure shades it above and below the
    surface line, with its width in the legend, and the designs it holds are the ones B.1 counts."""
    import case
    from figures.chart_level import chart_level_figure

    study = case.load_study("primary")
    fits = case.k_fits(study)
    fig = chart_level_figure()
    band = fits[1].band
    box = fig.axes[0].patches[0]
    span = np.array([box.get_y(), box.get_y() + box.get_height()])
    assert span.min() == pytest.approx(-band) and span.max() == pytest.approx(band)
    assert (
        f"|log V| < {band:.4f}" in [t.get_text() for t in fig.axes[0].get_legend().get_texts()][2]
    )
    logv = fits[case.CASE_K].estimator.transform(study.M)[:, -1]
    d3 = " ".join(
        _out_text(
            next(c for c in _code_cells(_nb(SUPPORT_NB)) if c.id == "tab-B-exponents_and_terms")
        ).split()
    )
    assert int((abs(logv) < band).sum()) == 318 + 119 and "| 318 |" in d3 and "| 119 |" in d3


def test_d3_names_the_band_of_each_column():
    """176: the near-frontier counts are at the K = 1 band, the shares at the fit's own band."""
    import case
    import generate_results as gr

    text = _out_text(
        next(c for c in _code_cells(_nb(SUPPORT_NB)) if c.id == "tab-B-exponents_and_terms")
    )
    assert text == str(gr.exponents_and_terms())
    assert "column counts the designs within the K = 1 band (0.0240) of the K = 2 fit" in text
    assert "within that fit's own band (0.0088)" in text
    study = case.load_study("primary")
    fits = case.k_fits(study)
    est = fits[case.CASE_K].estimator
    own = abs(est.training_log_v_) < fits[case.CASE_K].band
    shares = [(own & (est.cell_ == k)).sum() / own.sum() for k in range(2)]
    assert shares == pytest.approx(list(est.term_share_))


def test_the_executive_table_caption_and_the_shortlist_say_their_rules():
    """38, 50, 71, 70 (WP56: one stakeholder per objective): the caption names the rules' source,
    the band and the one design two rules pick; the rows carry the rules' names."""
    cap = _cell_src("tab-decision-caption")
    assert "the three stakeholders' rules pick from the shortlist" in cap
    assert "do not rank them" in cap and "the baseline's level is outside it" in cap
    assert "the manufacturer's and the operator's rules pick one design" in cap
    assert any("(sub-b-14)=" in _src(c) for c in _nb(SUPPORT_NB).cells)  # the pointer resolves


def test_terms_are_numbered_by_share_and_the_estimator_orders_them_so():
    """62: the numbering rule is stated with the thresholds and ties (Section 5, WP55); the
    estimator and its test carry it."""
    assert (
        "Terms are numbered by share, largest first (ties by cell size, then by the first "
        "exponent)" in _cell_src("sec-methods-thresholds")
    )
    src = (ROOT / "src" / "tradespace" / "estimator.py").read_text(encoding="utf-8")
    assert "descending term share, ties by cell size" in src


def test_reach_is_the_word_for_beta_and_the_package_is_named():
    """58, 59: no offset names beta in the main text; the package is named at its first use."""
    nb = _nb(PAPER_NB)
    text = " ".join(_src(c) for c in nb.cells if c.cell_type == "markdown")
    text = text.replace("level offset", "").replace("the offset enters only through", "")
    assert not re.search(r"\boffsets?\b", text)  # the conditioning's offset b is the one exception
    # the sentence "The package is the scikit-learn estimator of ..." left Section 3 at his review;
    # the estimator is still named in the body
    assert "scikit-learn transformer of the decomposition family" in text


@pytest.mark.slow
def test_the_adjusted_plane_puts_every_design_at_its_level_from_the_surface():
    """Figure 5 (36): the vertical distance of a design above the line is log V over the
    vertical metric's exponent, so the line is the surface for every design and about a tenth of
    the designs lie above it (the fit's convention); no selection of designs is made."""
    import case

    sys.path.insert(0, str(ROOT / "paper" / "figures"))
    import planes

    study = case.load_study("primary")
    fit = case.k_fits(study, (1,))[1]
    d = planes.adjusted_plane(study, fit)
    above = d["y"] - d["line"](d["x"])
    assert np.allclose(above * d["w_k"], d["log_v"], atol=1e-9)
    assert abs(float((above > 0).mean()) - study.spec.target_frac) < 0.02
    assert [study.names[i] for i in d["names"]] == ["available power", "unit cost"]
    cap = _cell_src("fig-planes-k1-caption")
    assert "Each design is moved vertically" in cap and "Dark" not in cap and "Light:" not in cap


def test_a_zero_metric_row_is_left_out_without_a_warning():
    """57: the package tolerates a zero metric (the row has no weight) and says nothing."""
    import warnings

    from tradespace import HyperbolicTradeSpace, make_frontier_data

    X, _ = make_frontier_data(120, 3, n_terms=1, random_state=0)
    Xz = np.vstack([X, [0.0, 1.0, 1.0]])
    with warnings.catch_warnings():
        warnings.simplefilter("error")
        est = HyperbolicTradeSpace(temperature=20.0).fit(Xz)
    assert est.support_weights_[-1] == 0.0


def test_the_improvement_factor_for_a_small_exponent():
    """86: the factor V^(-1/w) at V = 0.9 and w = 0.02, as Theorem 5's sentence quotes it."""
    assert round(0.9 ** (-1 / 0.02), -1) == 190.0
    assert "about 190" in _cell_src("res-L7")


# ---- the final round, third paper unit: requests 93 to 165 -------------------------------------


def test_inline_figures_have_their_caption_as_alt_text():
    """94: a figure cell's image output carries the caption's first sentence, not the matplotlib
    repr, as its plain-text form (the page's alt text)."""
    from execute_notebooks import caption_first_sentence

    nb = _nb(PAPER_NB)
    captions = {c.id: _src(c) for c in nb.cells if c.cell_type == "markdown"}
    seen = 0
    for c in _code_cells(nb):
        for out in c.outputs:
            data = out.get("data", {})
            if "image/png" not in data:
                continue
            seen += 1
            alt = data["text/plain"]
            alt = "".join(alt) if isinstance(alt, list) else alt
            assert "<Figure size" not in alt, c.id
            assert alt == caption_first_sentence(captions[f"{c.id}-caption"]), c.id
    assert seen >= 2


def test_the_one_term_sentence_claims_the_unique_optimum_and_not_r1():
    """137: the check of the repository is the uniqueness of the exact-maximum optimum; R1 (a facet
    with a positive normal) cannot hold with zero exponents and is not claimed for the case."""
    text = " ".join(_cell_out(PAPER_NB, "num-k1").split())
    assert "R1" not in text and "The exact-maximum optimum is one point" in text
    assert "R1" in _section("Results")  # the condition is stated beside the lemma that uses it


def test_the_one_axis_rule_is_stated_with_its_threshold_in_section_8():
    """116: the metrics in no contending set move with a partner at the lowest |Spearman| of F.5's
    table, below the 0.99 at which F.5 names a pair one axis."""
    import case

    text = " ".join(_moved("num-participation").split())
    assert "nearly one axis" not in text
    assert f"below the {case.ONE_AXIS:g} at which" in text and "|Spearman| at least 0.97" in text


def test_appendix_e_rows_agree_with_appendix_d():
    """143: G-7's and G-13's counts are B.9's, G-7's errors are B.8's, G-17's are B.7's (the
    ledger's rows, which Appendix G's gaps table links)."""
    e = " ".join(" ".join(str(v) for v in r.values()) for r in generate_gaps.gap_rows())
    e = " ".join(e.split())
    d11 = _out_text(next(c for c in _code_cells(_nb(SUPPORT_NB)) if c.id == "tab-B-stability"))
    d13 = _out_text(next(c for c in _code_cells(_nb(SUPPORT_NB)) if c.id == "tab-B-own_rows_refit"))
    d14 = _out_text(
        next(c for c in _code_cells(_nb(SUPPORT_NB)) if c.id == "tab-B-planted_recovery")
    )
    moving = int(re.search(r"of which (\d+) numbers move at all", d11).group(1))
    total = int(re.search(r"(\d+) quantities, of which", d11).group(1))
    m = re.search(
        r"\((\d+) of the record's (\d+) quantities: (\d+) numbers, as Appendix B.7 counts", e
    )
    assert m, "G-17's count"
    assert (int(m.group(1)), int(m.group(2)), int(m.group(3))) == (moving + 1, total, moving)
    recovered = re.findall(r"\| (?:infinity|50) \| 20 \| (\d+) of 20 \|", d14)
    assert recovered == ["16", "16"] and e.count("16/20") >= 3 and "support 17/20" not in e
    errs = re.findall(
        r"\| (?:infinity|50) \| 60 \| 0 of 60 \| [\d.]+ \| 60 of 60 \| ([\d.]+) \|", d13
    )
    assert errs == ["0.001", "0.037"]
    assert "largest error 0.001 at $\\tau=\\infty$ and 0.037 at $\\tau=50$" in e


def test_the_noise_ridge_factor_sentence_is_computed_from_the_table():
    """149: B.13 says by what factor the prediction exceeds the measurement."""
    text = _out_text(
        next(c for c in _code_cells(_nb(SUPPORT_NB)) if c.id == "tab-B-injected_noise")
    )
    assert text == str(generate_results.injected_noise())
    assert re.search(
        r"\(7 of 8 rows\), it does so by a factor of 1\.\d to \d+ \(predicted over", text
    )


def test_the_regimes_gain_ranges_are_the_ones_section_8_states():
    """145: F.1's table gives Kp 0.2 to 2 (primary) and 0.03 to 1 (baseline)."""
    c1 = _out_text(
        next(c for c in _code_cells(_nb(SUPPORT_NB)) if c.id == "tab-F-configuration_space")
    )
    assert re.search(r"\| Kp \| 0\.2 \| 2 \| 0\.2004 \| 1\.999 \| 0\.03009 \| 0\.999 \|", c1)
    s8 = " ".join(_cell_src("sec-case-construction-1b").split())
    assert (
        "from 0.2 to 2 in the aggressive (primary) regime and from 0.03 to 1 in the baseline regime"
        in s8
    )


def test_the_k2_fraction_above_the_surface_is_the_conventions_and_figure_6_says_so():
    """141: the old D.2's K = 2 row has the fraction above V = 1 within 0.01 of the target; the
    caption names the level and says about a tenth lie above the line."""
    d2 = _cell_out(SUPPORT_NB, "tab-B-termination_records")  # WP57c: the old D.2's table is B.4's
    primary = d2.split("Dataset cubesat-stock")[0]
    row = next(r for r in primary.splitlines() if r.startswith("| 2 |"))
    frac = float(row.split("|")[5])
    assert abs(frac - 0.10) < 0.01, row
    cap = " ".join(_cell_src("fig-chart-level-caption").split())
    assert "log $V$ of the $K=2$ fit" in cap and "about a tenth of the designs lie above it" in cap


def test_figure_captions_name_the_launch_link_the_sweep_ring_and_the_gloss_of_favours():
    """152, 140, 132: the caption of Figure 3 says which way the launch link runs; Figure 4's rings
    are the sweep point nearest the fit temperature (WP56: the ternary pair, whose corner word
    Figure 8 glossed, left the paper)."""
    c3 = " ".join(_cell_src("fig-behavioural-caption").split())
    assert (
        "launch budget requirement reads the launch cost" in c3
        and "computed from the total mass" in c3
    )
    assert "read through the launch cost" not in c3
    assert "sweep point nearest the fit temperature, which is not the fit itself" in _cell_src(
        "fig-tau-sweep-caption"
    )


def test_the_statements_of_the_theorems_carry_what_their_scripts_prove():
    """97, 98, 99, 106 to 110, 112/136, 113, 115: the wording of the hypotheses and the bounds."""
    soft = " ".join(_cell_src("977883ab").split())
    assert "F(W)\\le G_\\alpha(W)-E" in soft and "the average of $W$'s cyclic shifts" in soft
    assert "mean entropy" in soft
    descent = " ".join(_cell_src("res-L15").split())
    assert "$K^N+1$ iterations" in descent and "not a practical stopping guarantee" in descent
    cor = " ".join(_cell_src("res-L20").split())
    assert "A10 is not used" in cor
    assert "the rows need not be independent" in _cell_src("noise-asm")
    assert (
        "\\delta=-(PCP)^+P\\Sigma w" in cor and "\\Delta w" not in cor and "\\lambda_{\\min}" in cor
    )
    cert = " ".join(_cell_src("res-L17").split())
    assert "\\mathrm{blockdiag}" in cert and "not in $e^{w}$" in cert
    ext = " ".join(_cell_src("res-L10").split())
    assert "s_k=w_k\\cdot u-\\beta_k$ the score on term $k$" in ext and "x_k=" not in ext
    gap = " ".join(_cell_src("res-L12").split())
    assert "Frank-Wolfe gap" in gap and "f_k^*=\\min_{w\\in\\Delta}f_k(w)" in gap
    defs = _cell_src("sec-definitions")
    assert "c_k=e^{-\\kappa\\beta_k}" in defs and "a_k=\\kappa w_k" in defs  # WP55: the GP bridge


def test_appendix_b2_is_the_restart_stop_and_polish_rules():
    """138, then WP57b: E.2 is the paragraph Section 5's "steps: Appendix E.2" and Section 6's
    "Newton steps that close the gap the solver leaves" point at: the restart rule, the stop rule,
    the polish with G-16, the status at the polished point; no restatement of the alternation's
    program, no commentary on the lemmas, nothing about what the paper does not use."""
    b2 = " ".join(_cell_src("app-E-2", SUPPORT_NB).split())
    assert "five reduced Newton steps (the polish)" in b2 and "G-16" in b2
    assert "random centres in the chart" in b2 and "restart whose mean slack is smallest" in b2
    assert "if the mean slack rose, stop with the previous state" in b2
    assert "the status refers to the polished point" in b2
    cut = ("L19", "does not prove", "no result or table of this paper", "softmax", "L17 treats")
    for gone in cut:
        assert gone not in b2, gone
    assert len(b2.split()) <= 160
    results = " ".join(_section("Results").split())
    assert "the returned point is polished" in results


def test_the_three_requirements_neither_filtered_nor_priced_hold_for_every_feasible_design():
    """166: the battery peak power ratio (at least 1), the power margin and the energy balance (not
    negative) are met by every feasible design of both regimes, so they bind nowhere."""
    import case

    for regime in ("primary", "stock"):
        f = case.load_study(regime).feasible
        assert (f["battery_peak_power_ratio"] >= 1.0).all(), regime
        assert (f["power_margin_w"] >= 0.0).all() and (f["energy_balance_wh"] >= 0.0).all(), regime
    import generate_findings as gf

    # WP56: Table 2 states it as the third stage; the generator asserts the bounds on both regimes
    table = str(gf.requirement_order_table(case.load_study("primary"), case.load_study("stock")))
    for name in ("battery peak power ratio", "power margin", "energy balance"):
        row = next(r for r in table.splitlines() if r.startswith(f"| {name} |"))
        assert "3. met by every feasible design" in row, name


# ---- WP56: the tension matrix as one triangle and the decision-maker's ternary -----------------


@pytest.mark.slow
def test_the_tension_and_fleet_ternary_captions_state_the_fits_values():
    """WP56 D-1: Figure 7's caption states the range of the drawn half (the upper triangle in the
    tension order, every value at or below minus one) as the case's K = 2 fit gives it, term by
    term; the ternary's caption states the K = 1 fit's design count and exponents on the three
    objectives, read from ``case.fleet_ternary_study``."""
    import case

    from tradespace import tension_matrix

    study = case.load_study("primary")
    fit = case.fit_study(study, K=case.CASE_K)
    T = tension_matrix(fit.estimator, study.M)
    cap = " ".join(_cell_src("fig-tension-matrix-caption").split())
    for k, w in enumerate(np.atleast_2d(fit.estimator.exponents_)):
        keep = case.tension_order(T[k], [j for j in np.argsort(-w, kind="stable") if w[j] > 1e-3],
                                  "tension")  # fmt: skip
        upper = [abs(T[k, i, j]) for a, i in enumerate(keep) for j in keep[a + 1 :]]
        assert min(upper) >= 1.0
        lo, hi = min(upper), max(upper)
        top = f"{hi:.0f}" if hi >= 10 else f"{hi:.1f}"
        assert f"from -{lo:.1f} to -{top} on term {k + 1}" in cap, (k, lo, hi)
    assert "-1 or less" in cap
    st = case.fleet_ternary_study()
    w = case.fit_study(st, case.FLEET_TERNARY_K).estimator.exponents_[0]
    cap = " ".join(_cell_src("fig-fleet-ternary-caption").split())
    assert f"{len(st.feasible):,} feasible designs" in cap
    assert f"fleet cost ({w[0]:.2f})" in cap and f"coverage probability ({w[2]:.2f})" in cap
    assert f"{w[1]:.3f} on unit cost" in cap
    assert (
        len(cap.split(":::")[1].split("[full-size")[0].split(":label: fig-fleet")[1].split()) < 60
    )


# ---- WP56 second unit: Sections 7 to 9 on the landed figures -------------------------------------


def test_the_requirement_order_table_is_the_models_marks_in_the_cases_order():
    """Section 7's one table: the thirteen traded metrics with the model's marks (coverage.csv) and
    requirements, in the case's order (feasibility, after the fit, met everywhere), and the derived
    coverage probability; the notebook's output is the generator's."""
    import case
    import generate_findings as gf

    primary, stock = case.load_study("primary"), case.load_study("stock")
    table = str(gf.requirement_order_table(primary, stock))
    rows = [r.strip("|").split(" | ") for r in table.splitlines()[2:]]
    assert len(rows) == 14
    stages = [r[3].strip()[:2] for r in rows[:13]]
    assert stages == ["1."] * 4 + ["2."] * 6 + ["3."] * 3
    assert {r[0].strip() for r in rows if r[1].strip() == "MoE"} == {
        "pointing error", "unit cost", "fleet cost", "coverage probability (derived)",
    }  # fmt: skip
    first = {r[0].strip() for r in rows[:4]}
    assert first == {"settling time", "depth of discharge", "momentum headroom", "available power"}
    assert "launch cost at most 105,770 USD (7,000 USD per kg of total mass)" in table
    assert _cell_out(PAPER_NB, "tab-requirements").strip() == table.strip()


def test_the_fleet_refit_sentence_reads_the_identity_and_both_fits():
    """Section 8: the identity on every row and the one- and two-term exponents of the fleet's three
    objectives, the caption's numbers at one term; the notebook prints the generator's sentence."""
    import generate_findings as gf

    text = str(gf.fleet_refit_sentence())
    assert "On all 2,134 feasible designs fleet cost over unit cost times fleet size" in text
    assert "0.14 and 0.86 in term 1 and 0.54 and 0.46 in term 2" in text
    assert "0.000 on unit cost in both, so both terms lie on the one-term fit's edge" in text
    caption = _cell_src("fig-fleet-ternary-caption")
    assert "fleet cost (0.39)" in caption and "coverage probability (0.61)" in caption
    assert "0.006 on unit cost" in caption


@pytest.mark.slow
def test_the_requirements_sentence_is_d17s_exclusions():
    """Section 8: the near-frontier designs each requirement excludes after the K = 1 fit, read from
    ``case.requirements_table`` (B.12), largest first, and all six jointly."""
    import case
    import generate_findings as gf

    study = case.load_study("primary")
    fit = case.k_fits(study, (1,))[1]
    t = case.requirements_table(study, fit)
    text = re.sub(r"<[^>]+>", "", str(gf.requirements_sentence(study, fit)))
    joint = t.loc[t["requirement"] == "all jointly", "near-frontier excluded"].iloc[0]
    assert f"exclude {joint} near-frontier designs jointly".replace(" of ", " of its ") in text
    for r in t[t["requirement"] != "all jointly"].itertuples(index=False):
        assert f"{r[0]} {r[3].split(' of ')[0]}" in text, r[0]
    assert "peak slew power 108, control effort 95, unit cost 64, fleet cost 57" in text


@pytest.mark.slow
def test_the_terms_and_elasticity_sentences_agree_with_the_tension_figure():
    """The depth-three cold read's defects: the contending sets against the panels (8 of 13 drawn
    on each term, 8 and 7 contend, total mass drawn on term 2 outside its set), "leads" as the
    largest exponent, and the elasticity against the drawn cell (-0.9 per percent, -2.8 per unit)
    with the conditioning ratio typeset as math."""
    import case
    import generate_findings as gf

    from tradespace import tension_matrix

    study = case.load_study("primary")
    fits = case.k_fits(study, (1, 2))
    terms = str(gf.terms_sentence(study, fits))
    assert "contending sets (exact-maximum supports) of 8 and 7 metrics" in terms
    assert (
        "peak slew power, absent from the K = 1 set, carries the largest exponent of term 1"
        in terms
    )
    assert "total mass also carries 0.0064 on term 2" in terms
    el = gf.elasticity_sentence(study, fits)
    T = tension_matrix(fits[2].estimator, study.M)
    uc, ap = study.names.index("unit cost"), study.names.index("available power")
    assert f"its cell for the pair reads {T[1, uc, ap]:.1f}" in str(el) and "-2.8" in str(el)
    assert "elasticity between unit cost and available power is -0.9" in str(el)
    assert "$\\alpha_i/\\alpha_j$" in str(el) and "<math>" in el._repr_html_()
    assert "alpha_i/alpha_j" not in el._repr_html_()


def test_sections_7_to_9_state_each_limit_once_at_the_end_of_the_discussion():
    """WP56 R-4: the limits passage closes the Discussion; the case sections and the decision's
    caption carry no caveat of their own (illustrative values, schedule, nominal numbers)."""
    case_text = _section("Case construction") + _section("Case analysis")
    for caveat in ("illustrative", "schedule", "nominal", "lower bound", "does not tell"):
        assert caveat not in case_text, caveat
    disc = _section("Discussion")
    assert disc.rstrip().split("\n\n")[-1].startswith("**Limits.**")
    assert disc.count("illustrative") == 1 and disc.count("schedule") == 1

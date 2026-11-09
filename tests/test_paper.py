"""WP10 structural checks of the paper: the shells, the generators and the register of prior art.

Offline and fast. What is checked now is what exists now: the build configuration, the notebooks'
cell structure (one call per code cell), the appendices A to G with their jobs and tiers, the
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
import pytest
import yaml

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
    "Prior art, by family",
    "Preliminaries and notation",
    "Definitions",
    "Methods",
    "Results",
    "Search of the design space (preliminary)",
    "Case construction",
    "Case analysis",
    "Discussion",
    "Reproducibility and your own case",
    "Future work and final remark",
    "Acknowledgments",
    "Works cited",
]
APPENDICES = {
    "A": "Notation and terms",
    "B": "Proofs, step for step with their scripts",
    "C": "The case's model: how the table of metrics came to be",
    "D": "Extended results: what the method found in the table",
    "E": "Assumptions and abstraction gaps",
    "F": "Computational reproducibility",
    "G": "Register of prior art",
}
TIERS = ("**Main text keeps:**", "**This appendix carries:**", "**The repository keeps:**")
# Appendices whose generated content waits for another package's deliverable (stated in the report).
AWAITING_RECORD: set[str] = set()
NEAREST = {"pareto", "dea", "pca", "logratio", "gp-maxaffine", "production-distance", "tradespace"}
# The families of the outline (v1 baseline, v2): each has an entry in the register (R-9).
OUTLINE_FAMILIES = {
    "pareto", "dea", "production-distance", "frontier-estimation", "pca", "logratio",
    "gp-maxaffine", "kernel-hyperbolic-pca", "entropic-risk", "tradespace", "decision-analysis",
    "mbse",
}  # fmt: skip
PRIOR_FIELDS = ("does", "shares", "differs", "cites")
WORDS_BANNED_IN_PRIOR_ART = re.compile(r"\b(novel|first|new)\b", re.I)
# Fitted vocabulary that Appendix C must not contain; the system vocabulary D must not contain.
FITTED_WORDS = re.compile(
    r"\b(temperature|tau|frac_above_?|objective_|n_eff_?|reach|log V|gamma|radius|status)\b", re.I
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
        re.findall(r"^@\w+\{([^,\s]+),", (ROOT / "docs" / "references.bib").read_text(), re.M)
    )


def _appendix_cells(nb):
    """Map letter to the cells from its heading up to the next appendix heading."""
    sections, current = {}, None
    for c in nb.cells:
        m = re.match(r"^## Appendix ([A-G])\. ", _src(c)) if c.cell_type == "markdown" else None
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
    cfg = yaml.safe_load((PAPER / "myst.yml").read_text())
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


def test_no_pdf_export_block():
    text = (PAPER / "myst.yml").read_text()
    cfg = yaml.safe_load(text)
    assert "exports" not in cfg["project"]
    assert "typst" not in text.lower()
    assert "template: https://github.com/curvenote-templates" not in text


def test_build_output_is_ignored():
    assert "_build/" in (PAPER / ".gitignore").read_text()


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
            assert not pattern.search(path.read_text()), path


# ---- section structure of the paper ------------------------------------------------------------


def test_section_headings_in_order():
    """R-1: the section order is the amendment's; the headers are the skim."""
    assert _headings(_nb(PAPER_NB)) == SECTIONS


def test_front_matter_has_title_and_abstract():
    first = _src(_nb(PAPER_NB).cells[0])
    fm = yaml.safe_load(first.split("---")[1])
    assert fm["title"].startswith("Scaling Decision Analysis with Hyperbolic Trade Space")
    assert fm["abstract"].strip()


def test_search_section_is_labelled_preliminary():
    """R-15: section 7 is labelled preliminary and carries no result numbers."""
    nb = _nb(PAPER_NB)
    heading = next(h for h in _headings(nb) if h.startswith("Search of the design space"))
    assert "(preliminary)" in heading
    cells, grab = [], False
    for c in nb.cells:
        if c.cell_type != "markdown":
            continue
        text = _src(c)
        if text.startswith("## "):
            grab = text.startswith("## Search of the design space")
        if grab:
            cells.append(text)
    assert not re.search(r"\d+\.\d+|\d+\s*%", "\n".join(cells).replace("Section 7", ""))


def test_separation_of_concerns_no_user_guide_headers():
    """R-21: install, API and how-to-run sections stay on the docsite."""
    for h in _headings(_nb(PAPER_NB)):
        assert not re.search(r"\b(install|installation|api|getting started)\b", h, re.I), h


def test_body_names_no_tooling_versions():
    """R-12: the body names no tooling versions."""
    assert not re.search(r"\b\d+\.\d+\.\d+\b", _markdown(_nb(PAPER_NB)))


def test_counted_words_within_the_cap():
    """R-2: counted prose (the abstract and code excluded) is at most 6,000 words."""
    words = 0
    for i, c in enumerate(_nb(PAPER_NB).cells):
        if c.cell_type != "markdown" or i == 0:
            continue
        words += len(re.sub(r"[#>*`:{}\[\]@|-]", " ", _src(c)).split())
    assert words <= 6000


def test_register_forbidden_phrases_are_absent_from_all_prose():
    """R-5: the register's forbidden phrases appear nowhere in the paper's prose or appendices."""
    text = (NOTES / "notation.md").read_text()
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
    text = (NOTES / "notation.md").read_text()
    block = text.split("## Register phrases", 1)[1].split("## Forbidden phrases", 1)[0]
    phrases = re.findall(r"^- `([^`]+)`", block, re.M)
    prose = (_markdown(_nb(PAPER_NB)) + _markdown(_nb(SUPPORT_NB))).lower()
    missing = [p for p in phrases if p.lower() not in prose]
    assert not missing, missing


@needs_prose
def test_abstract_within_200_words():
    """R-13 L-A (hook, active with the prose)."""
    fm = yaml.safe_load(_src(_nb(PAPER_NB).cells[0]).split("---")[1])
    assert len(fm["abstract"].split()) <= 200


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
        assert name.startswith("case.") or name in {"family_table", "figure1"}, (cell.id, name)


def test_paper_cells_have_committed_outputs_without_errors():
    """The shells that run headlessly are committed executed."""
    for path in (PAPER_NB, SUPPORT_NB):
        for cell in _code_cells(_nb(path)):
            if cell.id.startswith(("fig-", "tab-")):
                assert cell.outputs, f"{cell.id} has no committed output ({STALE})"
            assert not [o for o in cell.outputs if o.output_type == "error"], cell.id


def test_figures_have_numbered_self_contained_captions():
    """R-4: each figure and table cell is embedded in a directive with a label and a caption."""
    nb = _nb(PAPER_NB)
    md = _markdown(nb)
    for cell in _code_cells(nb):
        if not cell.id.startswith(("fig-", "tab-")):
            continue
        kind = "figure" if cell.id.startswith("fig-") else "table"
        embedded = re.search(rf"\{{({kind}|embed)\}}[^\n]*\n?[^\n]*#{cell.id}\b|#{cell.id}\b", md)
        if cell.id == "fig-schematic":  # drawn from the committed file, see the figure-once test
            embedded = "{figure} figures/figure1.png" in md
        assert embedded, f"{cell.id} is not embedded in a {kind}"
    for m in re.finditer(r"\{figure\}\s*#([\w-]+)\s*\n:label:\s*(\S+)\s*\n(.*?)\n:::", md, re.S):
        assert m.group(3).strip(), f"figure {m.group(1)} has no caption"
    for m in re.finditer(r"\{table\}\s*([^\n]*)\n:label:\s*(\S+)", md):
        assert m.group(1).strip(), f"table {m.group(2)} has no caption"
    labels = re.findall(r":label:\s*(\S+)", md)
    assert len(labels) == len(set(labels))


# ---- the appendices ----------------------------------------------------------------------------


def test_appendix_headings_a_to_g_in_order():
    heads = [h for h in _headings(_nb(SUPPORT_NB)) if h.startswith("Appendix")]
    assert heads == [f"Appendix {k}. {v}" for k, v in APPENDICES.items()]


def test_no_withdrawn_appendices():
    """The source map, the search's appendix and the verification audit are withdrawn."""
    all_heads = " ".join(_headings(_nb(SUPPORT_NB), "##") + _headings(_nb(SUPPORT_NB), "###"))
    assert not re.search(r"source map|search|audit|verification", all_heads, re.I)
    assert not (PAPER / "source_map.md").exists()
    assert not [p for p in PAPER.glob("*audit*")]


def test_each_appendix_opens_with_its_job_and_three_tiers():
    """R-25: each appendix opens with its job and the three tiers; none is empty."""
    sections = _appendix_cells(_nb(SUPPORT_NB))
    assert list(sections) == list(APPENDICES)
    for letter, cells in sections.items():
        job = _src(cells[1])
        assert job.startswith("**Job.** To "), letter
        for tier in TIERS:
            assert tier in job, (letter, tier)
        assert len(job.split()) > 40, letter


def test_c_and_d_each_point_to_the_other_in_their_opening():
    """R-26: the opening sentence of C names D and the opening sentence of D names C."""
    sections = _appendix_cells(_nb(SUPPORT_NB))
    assert "Appendix D" in _src(sections["C"][1]).split("\n")[0]
    assert "Appendix C" in _src(sections["D"][1]).split("\n")[0]


def test_no_appendix_is_a_stub():
    """R-25: every appendix has a generated table with a committed output, B excepted until its
    record is delivered (it states its parts and the state of the record)."""
    for letter, cells in _appendix_cells(_nb(SUPPORT_NB)).items():
        gen = [c for c in cells if c.cell_type == "code"]
        assert gen, f"Appendix {letter} has no generated content"
        for c in gen:
            assert _out_text(c).strip(), f"{c.id} has no committed output ({STALE})"
            if letter not in AWAITING_RECORD:
                assert "|" in _out_text(c) or len(_out_text(c)) > 200, c.id


def test_appendix_cells_import_from_the_generators():
    for cell in _code_cells(_nb(SUPPORT_NB)):
        if cell.id.startswith("setup"):
            continue
        assert re.search(r"^from generate_\w+ import \w+$", _src(cell), re.M), cell.id


# -- A: the register table is compiled from glossary.yaml


def test_register_table_equals_the_glossary():
    entries = yaml.safe_load((ROOT / "glossary.yaml").read_text())["entries"]
    headers, rows = generate_register.register_rows()
    assert len(rows) == len(entries)
    text = str(generate_register.register_table())
    for e, row in zip(entries, rows, strict=True):
        assert row[0] == e["register"] and row[2] == e["formal"] and row[3] == e["not"]
        assert e["register"] in text and e["formal"] in text
        if e.get("symbol"):
            assert f"${e['symbol']}$" in text
    assert headers[:5] == ["Term", "Symbol", "Meaning in this paper", "Not", "Defined in"]


def test_register_committed_output_is_current():
    cell = next(c for c in _code_cells(_nb(SUPPORT_NB)) if c.id == "tab-A-register")
    assert _out_text(cell) == str(generate_register.register_table()), STALE


# -- E: the abstraction gaps


def test_gaps_table_has_g1_to_g16_from_the_ledger():
    rows = generate_gaps.gap_rows()
    ledger_ids = re.findall(r"^\| \*\*(G-\d+)\.", (NOTES / "abstraction-gaps.md").read_text(), re.M)
    assert [r["id"] for r in rows] == ledger_ids == [f"G-{i}" for i in range(1, len(rows) + 1)]
    for r in rows:
        for col in generate_gaps.COLUMNS:
            assert r[col].strip(), (r["id"], col)
    ledger = (NOTES / "abstraction-gaps.md").read_text()
    assert len(re.findall(r"^\| \*\*G-\d+\.", ledger, re.M)) == len(rows)


def test_gaps_committed_output_is_current():
    cell = next(c for c in _code_cells(_nb(SUPPORT_NB)) if c.id == "tab-E-gaps")
    assert _out_text(cell) == str(generate_gaps.gaps_table()), STALE


# -- F: the pinned toolchain is generated from the lock


def _lock_versions():
    data = tomllib.loads((ROOT / "uv.lock").read_text())
    return {p["name"]: p["version"] for p in data["package"] if "version" in p}


def test_toolchain_matches_the_lock_pyproject_and_python_version():
    """R-30: the stated versions are the lock's."""
    locked = _lock_versions()
    text = str(generate_repro.toolchain())
    pp = tomllib.loads((ROOT / "pyproject.toml").read_text())
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
    py = (ROOT / ".python-version").read_text().strip()
    assert f"| Python | {py} |" in text
    assert "| Package manager | uv " in text
    assert f"| Locked packages | {len(locked)} |" in text
    assert "uv.lock" in text and "pyproject.toml" in text and ".python-version" in text
    assert re.search(r"\| Commit \| ([0-9a-f]{40}|not found|)", text)


def test_f_prose_types_no_versions():
    """R-24, R-30: the versions come from the generator, never from typed prose."""
    cells = _appendix_cells(_nb(SUPPORT_NB))["F"]
    for c in cells:
        if c.cell_type == "markdown":
            assert not re.search(r"\b\d+\.\d+(\.\d+)?\b", _src(c)), c.id


def test_f_toolchain_committed_output_matches_the_lock():
    cell = next(c for c in _code_cells(_nb(SUPPORT_NB)) if c.id == "tab-F-toolchain")
    out = _out_text(cell)
    for name in ("numpy", "scipy", "scikit-learn", "sympy", "pandas", "matplotlib", "mystmd"):
        assert f"| {name} | {_lock_versions()[name]} |" in out, f"{name}: {STALE}"


def test_f_container_paragraph_is_a_marked_placeholder_region():
    cells = _appendix_cells(_nb(SUPPORT_NB))["F"]
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


# -- C and D: disjoint and complementary at the metric table


def _cells_of(letter):
    return [c for c in _appendix_cells(_nb(SUPPORT_NB))[letter] if c.cell_type == "code"]


def test_c_defines_the_dataset_labels_and_names_each_dataset_once():
    out = "\n".join(_out_text(c) for c in _cells_of("C"))
    labels = set(generate_model.DATASET_LABELS.values())
    assert len(labels) == 3
    table = next(c for c in _cells_of("C") if c.id == "tab-C-datasets")
    for label in labels:
        assert _out_text(table).count(f"| {label} |") == 1, label
        assert label in out


def test_c_contains_no_fitted_quantity():
    """R-26: no exponent fitted, temperature, value of V, facet found, reach or share in C."""
    for c in _cells_of("C"):
        text = _out_text(c)
        assert not FITTED_WORDS.search(text), (c.id, FITTED_WORDS.search(text).group(0))


def test_d_contains_no_definition_of_the_system():
    """R-26: no variable range, constraint, scenario constant or conditioning rule in D."""
    for c in _cells_of("D"):
        m = SYSTEM_WORDS.search(_out_text(c))
        assert not m, (c.id, m and m.group(0))


def test_every_table_of_d_cites_its_dataset_by_cs_label():
    labels = set(generate_model.DATASET_LABELS.values())
    for c in _cells_of("D"):
        text = _out_text(c)
        cited = set(re.findall(r"\b(cubesat-\w+|planted-[\w-]+)", text))
        assert cited and cited <= labels, (c.id, cited)
        assert re.search(r"Datasets? ", text), c.id


def test_no_table_or_figure_appears_in_both_c_and_d():
    c_calls = {ast.unparse(_calls(ast.parse(_src(c)))[0]) for c in _cells_of("C")}
    d_calls = {ast.unparse(_calls(ast.parse(_src(c)))[0]) for c in _cells_of("D")}
    assert not c_calls & d_calls
    c_tables = set().union(*[_tables(_out_text(c)) for c in _cells_of("C")])
    d_tables = set().union(*[_tables(_out_text(c)) for c in _cells_of("D")])
    assert not c_tables & d_tables


def test_c_committed_output_is_current():
    """C is cheap to regenerate, so its committed outputs are compared with a re-run."""
    for cell in _cells_of("C"):
        fn = re.search(r"import (\w+)", _src(cell)).group(1)
        assert _out_text(cell) == str(getattr(generate_model, fn)()), f"{cell.id}: {STALE}"


def test_planted_example_is_reproducible_and_has_known_facets():
    X, info = generate_model.planted_table()
    X2, _ = generate_model.planted_table()
    assert (X == X2).all()
    assert info["exponents"].shape == (3, 4) and X.shape[1] == 4


# -- B: the proofs, compiled from the record

RECORD = ROOT / "derivation" / "proof_map_record.json"
_PROOF_CELLS = ("tab-B-how-to-read", "tab-B-proof-map", "tab-B-proofs-fit", "tab-B-proofs-solver",
                "tab-B-checker")  # fmt: skip


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

FIGURE1_HASH = "f9d7219deb39227ee8d016bfe396cdd92be903ed5eb329e1743e24e56db60054"


def test_figure1_files_exist_and_the_data_hash_is_pinned():
    from figures import figure1

    assert (PAPER / "figures" / "figure1.png").stat().st_size > 10_000
    assert (PAPER / "figures" / "figure1.svg").read_text().startswith(("<?xml", "<svg"))
    data = figure1.figure1_data()
    assert data["u"].shape == (253, 2)
    assert figure1.data_hash(data) == figure1.data_hash() == FIGURE1_HASH


def test_figure1_has_three_panes_with_the_registers_words_and_writes_nothing(tmp_path, monkeypatch):
    import matplotlib.pyplot as plt
    from figures import figure1

    monkeypatch.chdir(tmp_path)
    fig = figure1.figure1()
    try:
        titles = [ax.get_title(loc="left") for ax in fig.axes]
        assert len(fig.axes) == 3
        assert "fitted reference surface" in titles[0]
        assert "supporting envelope" in titles[1] and "facets" in titles[2]
        words = " ".join(t.get_text() for ax in fig.axes for t in ax.texts)
        assert "energy" in words and "differential" in words and "facet 1" in words
    finally:
        plt.close(fig)
    assert list(tmp_path.iterdir()) == []


def test_figure1_is_in_the_paper_with_a_placeholder_caption():
    nb = _nb(PAPER_NB)
    cell = next(c for c in _code_cells(nb) if c.id == "fig-schematic")
    assert "figure1()" in _src(cell) and cell.outputs
    caption = next(c for c in nb.cells if c.id == "fig-schematic-caption")
    assert "figures/figure1.png" in _src(caption) and ":label:" in _src(caption)


def test_figure1_appears_once_in_the_built_page():
    """The captioned directive draws the committed file; the code cell is removed from the page.

    An embed of the cell (``#fig-schematic``) renders the cell's own output as well, which showed
    the figure twice; ``remove-output`` leaves the embed without its image, so the directive
    takes the file and the cell (kept to check that the figure still draws) is ``remove-cell``.
    """
    nb = _nb(PAPER_NB)
    cell = next(c for c in _code_cells(nb) if c.id == "fig-schematic")
    assert "remove-cell" in cell.metadata.get("tags", [])
    md = _markdown(nb)
    assert md.count("figures/figure1.png") == 1
    assert "#fig-schematic" not in md
    assert (PAPER / "figures" / "figure1.png").is_file()


# -- C and D: the completions


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


def test_c_has_the_metric_table_and_the_sources_and_d_has_the_extended_tables():
    sections = _appendix_cells(_nb(SUPPORT_NB))
    ids_c = {c.id for c in sections["C"]}
    assert {"tab-C-attribute_sources", "tab-C-metric_table"} <= ids_c
    ids_d = {c.id for c in sections["D"]}
    assert {"tab-D-sensitivity_variants", "tab-D-refits_by_category",
            "tab-D-candidate_designs"} <= ids_d  # fmt: skip
    heads = [h for h in _headings(_nb(SUPPORT_NB), "###") if h.startswith(("C.", "D."))]
    assert heads == [f"C.{k}" + h[3:] for k, h in enumerate(heads[: len(heads)], 1) if h[0] == "C"][
        : sum(h[0] == "C" for h in heads)
    ] + [h for h in heads if h[0] == "D"]  # C numbered in order
    d_nums = [int(re.match(r"D\.(\d+)", h).group(1)) for h in heads if h[0] == "D"]
    assert d_nums == list(range(1, len(d_nums) + 1))


def test_the_c_and_d_additions_are_current_and_cite_the_labels():
    for cell in _cells_of("D"):
        if cell.id in {"tab-D-sensitivity_variants", "tab-D-refits_by_category",
                       "tab-D-candidate_designs"}:  # fmt: skip
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


def test_section2_table_is_a_subset_of_the_register_with_the_same_wording():
    """R-27: section 2's rows are the flagged entries, word for word."""
    entries = generate_prior_art.entries()
    flagged = [e for e in entries if e.get("section2")]
    assert 0 < len(flagged) < len(entries) or len(flagged) == len(entries)
    table = str(generate_prior_art.family_table())
    register = str(generate_prior_art.register())
    for e in flagged:
        assert e["differs"] in table and e["differs"] in register
        assert e["does"] in table and e["does"] in register
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


def test_prior_art_committed_outputs_are_current():
    paper = {c.id: c for c in _code_cells(_nb(PAPER_NB))}
    assert _out_text(paper["tab-families"]) == str(generate_prior_art.family_table()), STALE
    reg = next(c for c in _code_cells(_nb(SUPPORT_NB)) if c.id == "tab-G-register")
    assert _out_text(reg) == str(generate_prior_art.register()), STALE


def test_register_opens_by_saying_it_is_not_exhaustive():
    cells = _appendix_cells(_nb(SUPPORT_NB))["G"]
    assert "not exhaustive" in _src(cells[2])


# ---- gated checks (slow or networked) ----------------------------------------------------------


@pytest.mark.skipif(not os.environ.get("PAPER_EXECUTE"), reason="set PAPER_EXECUTE=1 (about 90 s)")
def test_notebooks_execute_from_a_clean_kernel_and_match_the_committed_outputs(tmp_path):
    """R-14: a re-run reproduces the committed text outputs (images compared by presence)."""
    work = tmp_path / "paper"
    shutil.copytree(PAPER, work, ignore=shutil.ignore_patterns("_build", "__pycache__"))
    out = subprocess.run(
        [sys.executable, str(work / "execute_notebooks.py")],
        capture_output=True, text=True, cwd=work, check=False,
    )  # fmt: skip
    assert out.returncode == 0, out.stderr[-2000:]
    for name in ("paper.ipynb", "supporting_material.ipynb"):
        a, b = _nb(PAPER / name), _nb(work / name)
        for ca, cb in zip(_code_cells(a), _code_cells(b), strict=True):
            keys_a = [sorted(o.get("data", {})) for o in ca.outputs]
            keys_b = [sorted(o.get("data", {})) for o in cb.outputs]
            assert keys_a == keys_b, ca.id
            if ca.id.startswith("tab-F-toolchain"):
                continue  # the commit and the platform are observed values
            assert _out_text(ca) == _out_text(cb), ca.id


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

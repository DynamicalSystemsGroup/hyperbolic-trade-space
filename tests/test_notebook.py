"""Structure and output checks on the committed, executed ADCS trade-study notebook (WP7).

Reads the notebook JSON with ``json`` and ``re`` only; nothing is executed. Each test states the
requirement of ``work-packages/WP7-scope-of-work.md`` that it checks.
"""

import json
import pathlib
import re

import pandas as pd
import pytest

ADCS = pathlib.Path(__file__).resolve().parents[1] / "examples" / "adcs"
NOTEBOOK = ADCS / "adcs_trade_study.ipynb"
FIGURES = [
    "01_two_designs",
    "02_tau_sweep",
    "03_frontier_surfaces",
    "04_log_planes",
    "05_coordinates_holes",
    "06_tension_association",
    "07_v_by_category",
    "08_predict_check",
    "09_regime_comparison",
]


@pytest.fixture(scope="module")
def nb():
    return json.loads(NOTEBOOK.read_text())


def source(cell):
    return "".join(cell["source"])


def text_output(cell):
    out = []
    for o in cell.get("outputs", []):
        if o["output_type"] == "stream":
            out.append("".join(o["text"]))
    return "".join(out)


def cell_with(nb, marker):
    hits = [
        i for i, c in enumerate(nb["cells"]) if c["cell_type"] == "code" and marker in source(c)
    ]
    assert len(hits) == 1, f"expected one code cell with {marker!r}, found {len(hits)}"
    return hits[0]


def markdown(nb):
    return "\n".join(source(c) for c in nb["cells"] if c["cell_type"] == "markdown")


def test_sections_in_order(nb):
    """R-3: the stage headings appear in order."""
    heads = []
    for c in nb["cells"]:
        if c["cell_type"] == "markdown":
            heads += re.findall(r"^## (\d+) · (.+)$", source(c), flags=re.M)
    assert [int(n) for n, _ in heads] == list(range(1, 17))
    expected = [
        "designer's question", "feasible set", "Conditioning", "Temperature", "frontier in figures",
        "coordinates, holes", "tension report", "Sensitivity", "Interpretation", "V by category",
        "Candidates", "attribute units", "Propose, predict", "regime comparison", "Limits",
        "Verification and validation",
    ]  # fmt: skip
    for (_, title), key in zip(heads, expected, strict=True):
        assert key.lower() in title.lower(), (title, key)


def test_executed_without_errors_and_with_figures(nb):
    """R-2: every code cell has outputs, none is an error, figures are embedded."""
    n_png = 0
    for i, c in enumerate(nb["cells"]):
        if c["cell_type"] != "code":
            continue
        assert c["outputs"], f"cell {i} has no output"
        assert c["execution_count"] is not None
        for o in c["outputs"]:
            assert o["output_type"] != "error", f"cell {i} has an error output"
            if o["output_type"] == "stream" and o["name"] == "stderr":
                pytest.fail(f"cell {i} wrote to stderr")
            if o["output_type"] in ("display_data", "execute_result") and "image/png" in o["data"]:
                n_png += 1
    assert n_png >= len(FIGURES)


def test_png_copies_exist():
    """R-2, D-2: static copies of the figures."""
    for name in FIGURES:
        p = ADCS / "figures" / f"{name}.png"
        assert p.is_file() and p.stat().st_size > 5000, p


def _contending_line(cell):
    out = text_output(cell)
    m = re.search(r"^contending set at tau = inf: (.+)$", out, flags=re.M)
    assert m, out
    return out, m.group(1)


def test_report_outputs(nb):
    """R-7, R-9: n_lemma >= 2; total mass contends in the primary report only."""
    out, line = _contending_line(nb["cells"][cell_with(nb, "# CELL: tension-report-primary")])
    assert int(re.search(r"n_lemma = (\d+)", out).group(1)) >= 2
    assert "total mass" in line
    out_b, line_b = _contending_line(nb["cells"][cell_with(nb, "# CELL: tension-report-baseline")])
    assert int(re.search(r"n_lemma = (\d+)", out_b).group(1)) >= 2
    assert "total mass" not in line_b
    assert "total mass" not in out_b.split("working-tau exponents")[1].split("\n")[0]


def test_nothing_named_before_the_report(nb):
    """R-7: no dilemma, trilemma, n-lemma or exposed tension is named before the report cell."""
    stop = cell_with(nb, "# CELL: tension-report-primary")
    before = "\n".join(source(c) for c in nb["cells"][:stop]).lower()
    words = r"dilemma|trilemma|n-lemma|\d-lemma"
    assert not re.search(words, before)
    names = [
        "effort against", "against effort", "against mass", "mass against", "against slew",
        "slew against", "against settling", "settling against", "agility against",
        "against agility", "against pointing", "pointing against", "against control",
        "versus effort", "versus mass", "vs effort", "vs mass",
    ]  # fmt: skip
    for n in names:
        assert n not in before, n


def test_wheel_class_statement_and_disclosures(nb):
    """R-9, R-12: the wheel-class statement and the disclosures are present."""
    md = markdown(nb)
    flat = re.sub(r"\s+", " ", md)
    assert (
        "both a feasibility boundary and a frontier tension when the wheel is the bottleneck"
        in flat
    )
    assert "a feasibility boundary only in the baseline regime" in flat
    assert "depends on the operating regime" in flat
    for phrase in [
        "stratified", "censored", "illustrative", "stiff-loop", "underdamped", "4.7 %", "37.2 %",
        "Power never limits a slew", "thin", "near-frontier", "What remains for a human",
        "What the machine verified", "R1", "A4", "F5", "F10", "Cached data, no simulation",
        "author's interpretation",
    ]:  # fmt: skip
        assert phrase.lower() in flat.lower(), phrase


def test_interpretation_follows_the_report(nb):
    """R-8: the interpretation section comes after the report output."""
    rep = cell_with(nb, "# CELL: tension-report-primary")
    interp = next(
        i
        for i, c in enumerate(nb["cells"])
        if c["cell_type"] == "markdown" and "## 9 · Interpretation" in source(c)
    )
    assert interp > rep


def test_comparison_tables_present(nb):
    """R-9, R-11: the regime table and the predicted-versus-measured table are in the outputs."""
    t = text_output(nb["cells"][cell_with(nb, "# CELL: regime-table")])
    for key in ["baseline (stock gains)", "total mass in the contending set", "median Kd/Kp"]:
        assert key in t
    c = text_output(nb["cells"][cell_with(nb, "# CELL: predict-check-comparison")])
    for key in ["proposal_1", "proposal_2", "proposal_3", "log V within band", "predicted log V"]:
        assert key in c


def test_predictions_precede_the_check(nb):
    """R-11: the recorded predictions are shown before the comparison with the measurements."""
    assert cell_with(nb, "# CELL: predictions-recorded") < cell_with(
        nb, "# CELL: predict-check-comparison"
    )
    assert cell_with(nb, "# CELL: regressor-fit") < cell_with(nb, "# CELL: predictions-recorded")


def test_check_data_roles():
    """R-11: six check designs with roles."""
    df = pd.read_csv(ADCS / "data" / "check_designs_cubesat.csv")
    assert len(df) == 6
    assert df.role.value_counts().to_dict() == {"candidate": 3, "proposal": 3}


def test_inputs_are_the_cached_files(nb):
    """R-1: the notebook reads only the four cached files and runs no simulation."""
    code = "\n".join(source(c) for c in nb["cells"] if c["cell_type"] == "code")
    read = set(re.findall(r'DATA / "([^"]+)"', code))
    assert read == {
        "adcs_designs_cubesat_gains.csv",
        "adcs_designs_cubesat.csv",
        "check_designs_cubesat.csv",
        "check_predictions_cubesat.csv",
    }
    imports = re.findall(r"^\s*(?:import|from)\s+(\S+)", code, flags=re.M)
    for banned in [
        "opensysml",
        "cubesat_model",
        "generate_dataset",
        "make_check_designs",
        "adcs_sim",
    ]:
        assert not any(banned in m for m in imports), banned
    assert "measure(" not in code


def test_no_machine_specific_paths(nb):
    """R-16: no absolute paths, user names or credentials in the notebook JSON."""
    raw = NOTEBOOK.read_text()
    for bad in ["/Users/", "/private/", "/home/", "C:\\\\", "token", "password", "secret"]:
        assert bad not in raw, bad


def test_figure_axis_labels_are_in_attribute_terms(nb):
    """Editing pass (G-2): no bare '(m)' axis label in figure code; conditioned axes say so."""
    figure_code = [
        source(c)
        for c in nb["cells"]
        if c["cell_type"] == "code" and "save(fig" in source(c) and "def save" not in source(c)
    ]
    assert len(figure_code) >= len(FIGURES) - 3
    for code in figure_code:
        assert "(m)" not in code
    surfaces = source(nb["cells"][cell_with(nb, "# CELL: surfaces")])
    assert "short_label" in surfaces and "cond_label" in surfaces
    names = source(nb["cells"][cell_with(nb, "# CELL: names")])
    assert "conditioned" in names and "larger is better" in names


def test_colour_words_match_the_plotting_vocabulary(nb):
    """Editing pass (G-2): holes are vermillion (HOLE_COLOR #D55E00), never called red."""
    everything = "\n".join(source(c) for c in nb["cells"])
    assert re.search(r"vermillion", everything)
    assert not re.search(r"\bred\b", everything, flags=re.I)


def test_closing_call_to_action_with_source_links(nb):
    """Editing pass (G-7): the notebook ends with a call to action and plain source links."""
    last = nb["cells"][-1]
    assert last["cell_type"] == "markdown"
    flat = source(last)
    assert flat.startswith("## Where to go from here")
    assert "start wherever suits you" in flat.lower()
    repo = "https://github.com/DynamicalSystemsGroup/hyperbolic-trade-space"
    assert repo in flat and "docs/method.md" in flat and "design.md" in flat
    for word in ["Derivations", "Toolkit", "Limitations", "SysML", "Your own data"]:
        assert word in flat
    # plain text and markdown links only
    assert not re.search(r"[\U0001F300-\U0001FAFF\u2600-\u27BF]", flat)


def test_hook_figure_is_early_and_names_no_tension(nb):
    """Editing pass (G-7): an embodied hook figure precedes section 2."""
    hook = cell_with(nb, "# CELL: hook-figure")
    sec2 = next(
        i
        for i, c in enumerate(nb["cells"])
        if c["cell_type"] == "markdown" and "## 2 · " in source(c)
    )
    assert hook < sec2
    assert any("image/png" in o.get("data", {}) for o in nb["cells"][hook]["outputs"])


def test_prediction_columns_are_named_for_what_they_hold():
    """Editing pass (G-4): predicted-metric standard deviations are named by metric."""
    preds = pd.read_csv(ADCS / "data" / "check_predictions_cubesat.csv")
    assert not any(c.startswith("pred_std_z") or c == "pred_std_log_v" for c in preds.columns)
    for c in [
        "pred_std_slew_time_s",
        "pred_std_pointing_error_deg",
        "pred_std_control_effort",
        "pred_std_total_mass_kg",
    ]:
        assert c in preds.columns


def test_prose_says_elasticities_not_exchange_rates(nb):
    """WP10 Amendment 4 (R-37): the term is elasticity in the notebook's prose too."""
    prose = " ".join(source(c) for c in nb["cells"] if c["cell_type"] == "markdown")
    assert "exchange rate" not in prose.lower()
    assert "constant elasticities" in prose and "read as elasticities" in prose

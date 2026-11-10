"""The coverage table of the cubesat model (WP23 D-2; R-1, R-2, R-10).

``examples/adcs/model_v2/coverage.py`` writes ``views/coverage.md`` and ``views/coverage.csv`` from
the model (default ``cubesat_r2.sysml`` until the data gate). Checked here: every decision element
of the assembly view (two swaps, four tunes) has a non-empty row (R-1); every traded metric has a
requirement that reads its quantity and is marked MoE or MoP (R-2); the committed table equals a
fresh generation and three runs are byte-identical (R-10). The structural checks run on every test
run; the empirical column needs the slews, so the full regeneration is a ``slow`` test. Fixtures
FAIL
by name, never skip, when the opensysml client cannot start.
"""

from __future__ import annotations

import csv
import importlib.util
import io
import pathlib
import sys

import cubesat_model as cm
import pytest

ADCS_DIR = pathlib.Path(__file__).resolve().parents[1] / "examples" / "adcs"
MODEL_DIR = ADCS_DIR / "model_v2"
VIEWS = MODEL_DIR / "views"
SWAPS = {"WheelClass", "TrackerGrade"}
TUNES = {"panelSpan", "batteryCapacity", "Kp", "Kd"}
METRICS = [
    "settling time",
    "pointing error",
    "total mass",
    "control effort",
    "power margin",
    "energy balance",
    "eclipse reserve",
    "peak slew power",
    "depth of discharge",
]


@pytest.fixture(scope="module")
def coverage():
    spec = importlib.util.spec_from_file_location("coverage_table", MODEL_DIR / "coverage.py")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module  # dataclasses resolve annotations through sys.modules
    spec.loader.exec_module(module)
    return module


@pytest.fixture(scope="module")
def structural(coverage):
    """The table built from the default model without the slews (the structural column)."""
    try:
        return coverage.build(coverage.DEFAULT_MODEL, with_empirical=False)
    except cm.OpenSysMLUnavailable as exc:
        pytest.fail(f"the opensysml client could not start: {exc}", pytrace=False)


def _committed_rows() -> tuple[list[dict], list[dict]]:
    """The committed CSV's two tables as lists of dicts."""
    text = (VIEWS / "coverage.csv").read_text()
    blocks = text.split("table,metric,mark,element,kind,requirement,how,verified_in\n")
    assert len(blocks) == 2, "the CSV has the two tables"
    one = list(csv.DictReader(io.StringIO(blocks[0])))
    header = "table,metric,mark,element,kind,requirement,how,verified_in\n"
    two = list(csv.DictReader(io.StringIO(header + blocks[1])))
    return one, [{k: v for k, v in t.items() if k != "table"} for t in two]


# ---------------------------------------------------------------------------------------------
# R-1: every decision element reaches a metric
# ---------------------------------------------------------------------------------------------
def test_decision_elements_are_the_assembly_views_swaps_and_tunes(structural):
    elements = dict(structural["elements"])
    assert set(elements) == SWAPS | TUNES
    assert {e for e, k in elements.items() if k == "swap"} == SWAPS
    assert {e for e, k in elements.items() if k == "tune"} == TUNES


def test_no_decision_element_row_is_empty_structurally(structural):
    """R-1: every swap and tune has a model path to at least one traded metric."""
    for element, _ in structural["elements"]:
        reached = [
            r["metric"]
            for r in structural["rows"]
            if r["decision_element"] == element and r["structural"]
        ]
        assert reached, f"{element} reaches no traded metric in the model"


def test_no_decision_element_row_is_empty_empirically():
    """R-1 on the committed table: every element moves at least one metric through the oracle,
    and the structural and empirical columns agree on every cell (a disagreement is a finding
    recorded in WP23-review.md, and would be asserted here by name)."""
    rows, _ = _committed_rows()
    assert {r["decision_element"] for r in rows} == SWAPS | TUNES
    for element in SWAPS | TUNES:
        moved = [
            r["metric"]
            for r in rows
            if r["decision_element"] == element and r["empirical"] == "yes"
        ]
        assert moved, f"{element} moves no traded metric at the three named configurations"
    disagreements = [(r["decision_element"], r["metric"]) for r in rows if r["agree"] == "no"]
    assert disagreements == EXPECTED_DISAGREEMENTS


# The cells where the model's path exists but the one-at-a-time change moves nothing at the three
# named configurations (WP23-review.md, "Coverage findings"): the peak slew power and the power
# margin read the measured peak torque, and at every named configuration the wheels saturate at
# their class's maximum torque, so the gains, the battery and (for the peak power) the panel span
# move neither. In the CSV's row order.
EXPECTED_DISAGREEMENTS: list[tuple[str, str]] = [
    ("panelSpan", "peak slew power"),
    ("batteryCapacity", "power margin"),
    ("batteryCapacity", "peak slew power"),
    ("Kp", "power margin"),
    ("Kp", "peak slew power"),
    ("Kd", "power margin"),
    ("Kd", "peak slew power"),
]


def test_the_gains_do_not_reach_the_mass_and_kd_does_not_reach_the_pointing_error(structural):
    """The walk reads the model, not a typed map: the mass accounting has no gain in it and the
    pointing error's closed form has Kp but not Kd."""
    by = {(r["decision_element"], r["metric"]): r["structural"] for r in structural["rows"]}
    assert not by[("Kp", "total mass")] and not by[("Kd", "total mass")]
    assert by[("Kp", "pointing error")] and not by[("Kd", "pointing error")]
    assert all(by[(e, "settling time")] for e in SWAPS | TUNES)  # the slew reads every input


# ---------------------------------------------------------------------------------------------
# R-2: every traded metric has a requirement on its quantity and is marked MoE or MoP
# ---------------------------------------------------------------------------------------------
def test_traded_metrics_are_the_nine_of_the_case(structural):
    assert [m.name for m in structural["metrics"]] == METRICS


def test_every_traded_metric_has_a_requirement_that_reads_it_and_a_mark(structural):
    """R-2, read through the client: a requirement invokes the metric's calc, reads its measured
    quantity, or reads it through the MoE calc (the launch cost on the total mass); each requirement
    is verified in a verification case; each metric is marked MoE or MoP."""
    for t in structural["table2"]:
        assert t["mark"] in ("MoE", "MoP"), t
        assert t["requirement"] != "none", t
        assert t["verified_in"] != "none", t
    marks = {t["metric"]: t["mark"] for t in structural["table2"]}
    assert marks["pointing error"] == "MoE" and marks["total mass"] == "MoP"
    total = next(t for t in structural["table2"] if t["metric"] == "total mass")
    assert total["requirement"] == "LaunchBudgetRequirement" and "LaunchCost" in total["how"]


# ---------------------------------------------------------------------------------------------
# R-10: the committed table is a fresh generation; three runs are byte-identical
# ---------------------------------------------------------------------------------------------
def test_committed_structural_columns_equal_a_fresh_generation(coverage, structural):
    """The committed CSV's structural column and metrics table equal a fresh structural build."""
    rows, table2 = _committed_rows()
    fresh = {(r["decision_element"], r["metric"]): r["structural"] for r in structural["rows"]}
    assert {(r["decision_element"], r["metric"]): r["structural"] == "yes" for r in rows} == fresh
    want = [{k: str(v) for k, v in t.items()} for t in structural["table2"]]
    assert table2 == want
    text = (VIEWS / "coverage.md").read_text()
    assert structural["sha256"][:12] in text, "the committed table names the committed model"


def test_three_structural_runs_are_byte_identical(coverage, structural):
    runs = [
        coverage.render_md(coverage.build(coverage.DEFAULT_MODEL, with_empirical=False))
        for _ in range(2)
    ]
    assert runs[0] == runs[1] == coverage.render_md(structural)


@pytest.mark.slow
def test_committed_table_equals_a_full_regeneration_three_times(coverage):
    """R-10 in full: three regenerations with the empirical column are byte-identical and equal
    the committed files."""
    results = [coverage.build(coverage.DEFAULT_MODEL, with_empirical=True) for _ in range(3)]
    mds = [coverage.render_md(r) for r in results]
    csvs = [coverage.render_csv(r) for r in results]
    assert mds[0] == mds[1] == mds[2] and csvs[0] == csvs[1] == csvs[2]
    assert (VIEWS / "coverage.md").read_text() == mds[0]
    assert (VIEWS / "coverage.csv").read_text() == csvs[0]

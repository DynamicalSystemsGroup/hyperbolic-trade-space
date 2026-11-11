"""The coverage table of the cubesat model (WP23 D-2; R-1, R-2, R-10).

``examples/adcs/model_v2/coverage.py`` writes ``views/coverage.md`` and ``views/coverage.csv`` from
the model (the adopted ``cubesat.sysml``). Checked here: every decision element
of the assembly view (two swaps, four tunes) has a non-empty row (R-1); every traded metric has a
requirement that reads its quantity and is marked MoE or MoP (R-2); the coupling graph (the design
structure matrix of the third table) is connected, every configuration value feeds a subsystem and
every metric is read off one, and the coupling variables between the subsystems are the model's
named quantities (G1, G3; the supervisor's connected-graph reading, ``WP23-decisions.md``); the
committed table equals a fresh generation and three runs are byte-identical (R-10). The structural
checks run on every test run; the empirical column needs the slews, so the full regeneration is a
``slow`` test. Fixtures FAIL by name, never skip, when the opensysml client cannot start.
"""

from __future__ import annotations

import csv
import importlib.util
import io
import pathlib
import re
import sys

import cubesat_model as cm
import pytest
from _env import of_record

ADCS_DIR = pathlib.Path(__file__).resolve().parents[1] / "examples" / "adcs"
MODEL_DIR = ADCS_DIR / "model_v2"
VIEWS = MODEL_DIR / "views"
SWAPS = {"wheelClass", "grade"}  # the swaps by their selecting attribute, as the view tags them
TUNES = {"panelSpan", "batteryCapacity", "Kp", "Kd", "fleetSize"}
METRICS = [
    "settling time",
    "pointing error",
    "total mass",
    "control effort",
    "power margin",
    "energy balance",
    "peak slew power",
    "depth of discharge",
    "momentum headroom",
    "available power",
    "battery peak power ratio",
    "unit cost",
    "fleet cost",
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


METRICS_HEADER = "table,metric,mark,element,kind,requirement,how,limit,verified_in\n"
COUPLING_HEADER = "table,from,to,variables\n"


def _tables(text: str) -> dict[str, list[dict]]:
    """The CSV's tables by the label in their first column (``coverage``, ``metrics``,
    ``coupling``, ``reasons``): a line that starts ``table,`` is a header, the rows after it
    carry the label."""
    out: dict[str, list[dict]] = {}
    header = None
    for line in text.splitlines():
        if line.startswith("table,"):
            header = next(csv.reader([line]))
            continue
        row = dict(zip(header, next(csv.reader([line])), strict=True))
        out.setdefault(row["table"], []).append(row)
    return out


def _committed_rows() -> tuple[list[dict], list[dict]]:
    """The committed CSV's first two tables as lists of dicts."""
    tables = _tables((VIEWS / "coverage.csv").read_text(encoding="utf-8"))
    drop = lambda rows: [{k: v for k, v in r.items() if k != "table"} for r in rows]  # noqa: E731
    return tables["coverage"], drop(tables["metrics"])


def _committed_coupling() -> list[dict]:
    """The committed CSV's third table (the design structure matrix) as a list of dicts."""
    return _tables((VIEWS / "coverage.csv").read_text(encoding="utf-8"))["coupling"]


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
    # the slew reads every input but the fleet size, which only the cost model reads (WP30)
    assert all(by[(e, "settling time")] for e in (SWAPS | TUNES) - {"fleetSize"})
    assert {m for (e, m), v in by.items() if e == "fleetSize" and v} == {"unit cost", "fleet cost"}
    assert not any(by[(e, m)] for e in ("Kp", "Kd") for m in ("unit cost", "fleet cost"))


# ---------------------------------------------------------------------------------------------
# R-2: every traded metric has a requirement on its quantity and is marked MoE or MoP
# ---------------------------------------------------------------------------------------------
def test_traded_metrics_are_the_thirteen_of_the_case(structural):
    """The thirteen traded metrics: the eight of the WP23 close-out (the eclipse reserve left), the
    momentum headroom (WP30, D-1 (a) of spike C; the supervisor's "Confirm"), the available power
    and the battery peak power ratio ("No floating requirements") and the unit cost and the fleet
    cost (WP30 OD1 (a)), the last two returned by an analysis each."""
    assert [m.name for m in structural["metrics"]] == METRICS


def test_the_four_thresholds_are_listed_with_their_requirements(structural):
    """R-16 of the WP23 close-out: the table lists the supervisor's four values, read from the
    model's ``budgets`` part beside the requirement that reads each."""
    limits = {t["metric"]: t["limit"] for t in structural["table2"]}
    assert limits == {
        "settling time": "-",
        "pointing error": "budgets.pointingErrorLimit = 0.008495 [degree]",
        "total mass": "budgets.launchBudget = 105770.0",
        "control effort": "budgets.controlEffortLimit = 0.05922 [N*m*s]",
        "power margin": "-",
        "energy balance": "-",
        "peak slew power": "budgets.peakSlewPowerLimit = 2.6 [W]",
        "depth of discharge": "-",
        "momentum headroom": "-",
        "available power": "-",
        "battery peak power ratio": "-",
        "unit cost": "budgets.unitCostLimit = 350000.0",
        "fleet cost": "budgets.fleetCostLimit = 6.0e6",
    }


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
# G1, G3: the coupling graph (configuration values -> subsystems -> metrics) is connected
# ---------------------------------------------------------------------------------------------
SUBSYSTEMS = ["controls", "power and energy", "mass", "cost"]
# The coupling variables between the subsystems, as the model names them (WP23-review.md,
# "Round 2"): a change in the model that adds or removes one is seen here by name.
EXPECTED_COUPLING = {
    ("controls", "power and energy"): ["peakTorque", "torqueSquaredIntegral"],
    ("power and energy", "controls"): ["panelPlus.mass", "usableWheelTorque"],
    ("power and energy", "mass"): ["battery.mass", "panelMinus.mass", "panelPlus.mass"],
    ("mass", "controls"): ["InertiaX", "InertiaY", "InertiaZ", "structureMass"],
    # the cost model reads the panels' area (the panel price) and the total mass (the launch cost)
    ("power and energy", "cost"): ["panelMinus.area", "panelPlus.area"],
    ("mass", "cost"): ["totalMass"],
}


def test_every_configuration_value_feeds_a_subsystem_and_the_graph_is_connected(structural):
    """The supervisor's test (WP23-decisions.md, 22:15): a connected graph, not all-to-all. Every
    configuration value feeds at least one subsystem's calcs and reaches at least one traded
    metric; every traded metric is read off a subsystem; the graph is connected."""
    c = structural["coupling"]
    assert c["subsystems"] == SUBSYSTEMS
    assert c["unfed"] == [] and c["unreached_metrics"] == []
    assert c["connected"]
    for element in SWAPS | TUNES:
        assert c["feeds"][element], f"{element} feeds no subsystem"
        assert c["reached"][element], f"{element} reaches no traded metric"
    # the battery feeds the power subsystem and the cost (its price); the gains feed the controls
    # alone; the fleet size feeds the cost alone
    assert c["feeds"]["batteryCapacity"] == ["power and energy", "cost"]
    assert c["feeds"]["fleetSize"] == ["cost"]
    assert c["feeds"]["Kp"] == c["feeds"]["Kd"] == ["controls"]


def test_every_traded_metric_is_read_off_one_subsystem(structural):
    c = structural["coupling"]
    read_off = [m for s in SUBSYSTEMS for m in c["metrics_read_off"][s]]
    assert sorted(read_off) == sorted(METRICS)
    assert c["metrics_read_off"]["mass"] == ["total mass"]
    assert c["metrics_read_off"]["controls"] == [
        "settling time",
        "pointing error",
        "control effort",
        "momentum headroom",
    ]


def test_coupling_variables_between_subsystems_are_the_models_named_quantities(structural):
    """The cells off the diagonal name the quantities one subsystem reads from another, as the
    model names them; the configuration rows name the configuration attributes each subsystem
    reads (a tune reaches a subsystem through the part attribute bound to it)."""
    c = structural["coupling"]
    off_diagonal = {k: v for k, v in c["cells"].items() if k[0] in SUBSYSTEMS}
    assert off_diagonal == EXPECTED_COUPLING
    assert c["cells"][("batteryCapacity", "power and energy")] == ["battery.capacity"]
    assert c["cells"][("wheelClass", "mass")] == ["wheel.mass"]
    assert c["cells"][("grade", "controls")] == ["tracker.accuracy"]
    assert c["cells"][("panelSpan", "mass")] == ["panelPlus.span"]  # the inertia's geometry


def test_every_requirement_is_read_off_a_subsystem(structural):
    c = structural["coupling"]
    reqs = sorted(r for s in SUBSYSTEMS for r in c["requirements_read_off"][s])
    assert len(reqs) == len(set(reqs)) and len(reqs) >= 13
    assert {t["requirement"] for t in structural["table2"]} <= set(reqs)


def test_committed_coupling_table_equals_a_fresh_generation(coverage, structural):
    rows = _committed_coupling()
    assert rows == _tables(coverage.render_csv(structural))["coupling"]
    assert rows[-1]["to"] == "connected"


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
    text = (VIEWS / "coverage.md").read_text(encoding="utf-8")
    assert structural["sha256"][:12] in text, "the committed table names the committed model"


def test_three_structural_runs_are_byte_identical(coverage, structural):
    runs = [
        coverage.render_md(coverage.build(coverage.DEFAULT_MODEL, with_empirical=False))
        for _ in range(2)
    ]
    assert runs[0] == runs[1] == coverage.render_md(structural)


MAGNITUDE = re.compile(r"\(\d\.\de[+-]\d\d\)")


def _without_magnitudes(md: str) -> str:
    return MAGNITUDE.sub("(#)", md)


def _rows_without_magnitudes(csv_text: str) -> list[dict]:
    rows = list(csv.DictReader(io.StringIO(csv_text.split(METRICS_HEADER)[0])))
    return [{k: v for k, v in r.items() if k != "max_relative_change"} for r in rows]


@pytest.mark.slow
def test_committed_table_equals_a_full_regeneration_three_times(coverage):
    """R-10 in full: three regenerations with the empirical column are byte-identical to each
    other on any platform. The committed files are the environment of record's (regenerated
    inside ``hts-paper``; WP23-review.md, "Coverage table, platform stability"): there the
    regeneration equals them byte for byte. Elsewhere the structure is asserted, the rows and
    columns, every structural cell, the empirical yes/no pattern and the disagreements (the
    recorded cause leaves them platform-stable: the cells at exactly zero are configuration-only
    quantities at a saturated torque; the smallest non-zero effect, 7.8e-07, is three orders
    above the threshold and the platforms differ in such a quantity below 1e-9), the metrics
    table and the coupling table; the magnitudes are printed where they
    differ and not asserted, because the settling time is read on the integrator's time grid and
    its relative changes at a 10 % tune are order-of-magnitude statements."""
    results = [coverage.build(coverage.DEFAULT_MODEL, with_empirical=True) for _ in range(3)]
    mds = [coverage.render_md(r) for r in results]
    csvs = [coverage.render_csv(r) for r in results]
    assert mds[0] == mds[1] == mds[2] and csvs[0] == csvs[1] == csvs[2]
    committed_md = (VIEWS / "coverage.md").read_text(encoding="utf-8")
    committed_csv = (VIEWS / "coverage.csv").read_text(encoding="utf-8")
    if of_record():
        assert committed_md == mds[0]
        assert committed_csv == csvs[0]
        return
    assert _without_magnitudes(committed_md) == _without_magnitudes(mds[0])
    assert _rows_without_magnitudes(committed_csv) == _rows_without_magnitudes(csvs[0])
    assert committed_csv.split(METRICS_HEADER)[1] == csvs[0].split(METRICS_HEADER)[1]
    fresh = {
        (r["decision_element"], r["metric"]): f"{r['max_relative_change']:.1e}"
        for r in results[0]["rows"]
    }
    differing = []
    for r in csv.DictReader(io.StringIO(committed_csv.split(METRICS_HEADER)[0])):
        here = fresh[(r["decision_element"], r["metric"])]
        if r["max_relative_change"] != here:
            differing.append((r["decision_element"], r["metric"], r["max_relative_change"], here))
    print(
        "magnitudes that differ from the environment of record (committed, here): "
        + ("; ".join(f"{e} -> {m}: {a}, {b}" for e, m, a, b in differing) or "none")
    )


def test_repository_paths_print_with_forward_slashes(coverage):
    root = pathlib.PureWindowsPath("C:/work/repo")
    path = root / "examples" / "adcs" / "model_v2" / "cubesat.sysml"
    assert coverage.repo_path(path, root) == "examples/adcs/model_v2/cubesat.sysml"
    outside = pathlib.PureWindowsPath("D:/other/cubesat.sysml")
    assert coverage.repo_path(outside, root) == "D:/other/cubesat.sysml"


# ---------------------------------------------------------------------------------------------
# "No floating requirements" (WP30): every requirement reads a traded metric; the three whose metric
# the fit may give no weight carry a computed reason
# ---------------------------------------------------------------------------------------------
REASONED = {"MomentumRequirement", "PowerRequirement", "BatteryPeakPowerRequirement"}


def _project():
    spec = importlib.util.spec_from_file_location(
        "wp30_project",
        MODEL_DIR.parents[2] / "docs/superpowers/notes/spike-sysml-diagrams/project.py",
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _unexplained(result) -> list[str]:
    """The requirements in the view's box with no stated reason."""
    return [r["requirement"] for r in result["reasons"] if r["requirement"] in result["box"]
            and not r["sentence"]]  # fmt: skip


def test_no_requirement_floats_free_of_the_traded_metrics(structural):
    """The supervisor's word ("No floating requirements", WP30-decisions.md): the box of
    requirements that read no traded metric is empty; the three that used to stand there read the
    momentum headroom, the available power and the battery peak power ratio."""
    assert structural["box"] == []
    reads = {t["metric"]: t["requirement"] for t in structural["table2"]}
    assert reads["momentum headroom"] == "MomentumRequirement"
    assert reads["available power"] == "PowerRequirement"
    assert reads["battery peak power ratio"] == "BatteryPeakPowerRequirement"
    assert {r["requirement"] for r in structural["reasons"]} == REASONED
    claims = {r["requirement"]: r["claim"] for r in structural["reasons"]}
    for name in ("PowerRequirement", "BatteryPeakPowerRequirement"):
        assert (claims[name]["status"], claims[name]["strength"]) == ("holds", "proved")
    assert (
        claims["MomentumRequirement"] is None
    )  # it can fail: 188 and 81 designs of the first sample


def test_a_requirement_that_reads_no_traded_metric_is_found(coverage, tmp_path):
    """Negative control: a planted requirement that reads no traded metric stands in the box with no
    reason, and the check names it; the model as committed has none."""
    text = coverage.DEFAULT_MODEL.read_text(encoding="utf-8")
    planted = text.rstrip()[:-1] + (
        "\n    requirement def PlantedRequirement {\n        subject c : Cubesat;\n"
        "        require constraint { c.panelSpan > 0.0 [m] }\n    }\n}\n"
    )
    path = tmp_path / "planted.sysml"
    path.write_text(planted, encoding="utf-8")
    result = coverage.build(path, with_empirical=False)
    assert result["box"] == ["PlantedRequirement"]
    assert _unexplained(result) == ["PlantedRequirement"]
    assert {r["requirement"] for r in result["reasons"]} == REASONED | {"PlantedRequirement"}


def test_the_view_draws_no_box_because_every_requirement_reads_a_traded_metric(structural):
    project = _project()
    m, byid = project.load(MODEL_DIR / "cubesat.sysml")
    _, facts = project.behavioural(m, byid, "CubesatTradeSpaceV2")
    boxed = {project.short(r) for r in facts["reqs"] if facts["band"][r] is None}
    assert boxed == set(structural["box"]) == set()


# The tests below read the regenerated data of the WP30 gate (thirteen columns, the first
# 2,000 designs per regime); they are red until the gate regenerates it.
def test_every_reasoned_requirement_has_a_computed_reading(structural):
    """Each of the three carries one of the three readings, computed from the K = 1 fit and the
    Spearman correlation of the data of record. Host-recorded at the gate (spike C's values, from
    the first 1,000 designs: the power requirement's metric one axis with the energy balance at
    0.9996 and 0.9997; the battery peak power ratio tracking the depth of discharge at 0.970 and
    0.975, exponent zero; the momentum headroom taking part)."""
    reasons = {r["requirement"]: r for r in structural["reasons"]}
    assert all(r["sentence"] for r in reasons.values()), "the data lack the thirteen columns"
    power = reasons["PowerRequirement"]
    assert (power["partner"], power["reading"]) == ("energy balance", "one axis")
    assert min(power["spearman"].values()) >= 0.99
    battery = reasons["BatteryPeakPowerRequirement"]
    assert battery["reading"] == "exponent zero" and battery["partner"] == "depth of discharge"
    assert max(battery["exponent"].values()) <= 1e-9
    assert reasons["MomentumRequirement"]["reading"] == "participates"


def test_the_reason_numbers_are_the_spearman_of_the_stated_pair(coverage, structural):
    """The printed correlation is the one an independent reading of the data gives: the available
    power against the energy balance, over the feasible designs (every flag true, every traded
    attribute positive), the two oriented larger-is-better."""
    import pandas as pd
    from scipy.stats import spearmanr

    sys.path.insert(0, str(ADCS_DIR))
    import case

    got = next(r for r in structural["reasons"] if r["requirement"] == "PowerRequirement")
    assert got["spearman"], "the data lack the thirteen columns"
    for regime, name in case.CUBESAT.regimes.items():
        raw = pd.read_csv(case.CUBESAT.data_dir / name)
        ok = raw[list(case.CUBESAT.flags)].all(axis=1)
        for a in case.CUBESAT.attributes:
            ok &= raw[a] > 0
        f = raw[ok]
        rho = spearmanr(f["available_power_w"], f["energy_balance_wh"]).statistic
        assert got["spearman"][case._REGIME_WORDS.get(regime, regime)] == pytest.approx(rho)


def test_the_caption_the_table_and_the_csv_print_one_reason(structural):
    """The committed caption, ``coverage.md`` and ``coverage.csv`` carry each reason sentence as the
    computation prints it."""
    caption = (VIEWS / "behavioural_caption.md").read_text(encoding="utf-8")
    table = (VIEWS / "coverage.md").read_text(encoding="utf-8")
    reasons_csv = {
        r["requirement"]: r["reason"]
        for r in _tables((VIEWS / "coverage.csv").read_text(encoding="utf-8"))["reasons"]
    }
    for r in structural["reasons"]:
        assert f"- {r['sentence']}\n" in caption and f"- {r['sentence']}\n" in table
        assert reasons_csv[r["requirement"]] == r["sentence"]

"""The SysML-backed cubesat oracle and sampler of the v2 generation (WP15 15.4).

* R-9: the output keys equal the frozen ``measure`` keys, in the frozen CSV column order; a
  configuration outside the model's ranges or with an unknown categorical value raises
  ``ValueError`` naming the variable; construction names the cause when the runtime cannot start.
* R-2: no model constant is copied into the experiment layer, and editing the model changes the
  sampler's draws and the scenario the oracle uses.
* R-3: the four flags are the verdicts of the model's requirements (not Python inequalities).
* Solver exclusion: the experiment's ledger input records the classification of the declared
  space; designs sampled in a region the solver excludes simulate with the matching flag False.

Fixtures FAIL by name (never skip) when the opensysml client cannot start or ``z3`` is not on
``PATH``.
"""

from __future__ import annotations

import dataclasses
import os
import pathlib
import re
import subprocess
import sys

import cubesat_model as cm
import numpy as np
import pandas as pd
import pytest
from _env import exact_only, listed
from experiments import compare as cmp
from experiments import cubesat_oracle as co
from experiments import definitions as df
from experiments import exclusion as ex
from experiments import ledger as lg
from experiments.exclusion import battery_region, classify_region

ADCS = pathlib.Path(__file__).resolve().parents[1] / "examples" / "adcs"
MODEL = ADCS / "model_v2" / "cubesat.sysml"
TEXT = MODEL.read_text()
FROZEN_CSV = ADCS / "data" / "adcs_designs_cubesat_gains.csv"
FLAGS = co.FLAG_NAMES


@pytest.fixture(scope="module")
def oracle():
    try:
        return co.CubesatOracle(TEXT, "nominalSlew", "aggressive", workers=1)
    except cm.OpenSysMLUnavailable as exc:
        pytest.fail(f"the opensysml client could not start: {exc}", pytrace=False)


@pytest.fixture(scope="module")
def solver():
    if not ex.solver_available():
        pytest.fail(
            "the solve engine needs z3 or cvc5 on PATH and none was found: run through `uv run`",
            pytrace=False,
        )


@pytest.fixture(scope="module")
def exp():
    return dataclasses.replace(df.EXPERIMENTS["v2-primary"], inputs={})


@pytest.fixture(scope="module")
def designs(exp):
    return co.build_sampler(exp).draw(12, 0)


def test_the_sampler_reproduces_the_frozen_designs(designs):
    """Same draws as the frozen generator: design ids, seeds, categoricals, continuous values."""
    frozen = pd.read_csv(FROZEN_CSV).head(len(designs))
    assert list(designs.columns) == list(frozen.columns[:8])
    assert designs["design_id"].tolist() == frozen["design_id"].tolist()
    assert designs["seed"].tolist() == frozen["seed"].tolist()
    for c in ("wheel_class", "st_grade"):
        assert designs[c].tolist() == frozen[c].tolist()
    for c in ("panel_span_m", "battery_wh", "Kp", "Kd"):
        np.testing.assert_allclose(designs[c], frozen[c], rtol=1e-8)


def test_keys_and_order_equal_the_frozen_measure_on_three_configurations(oracle, designs):
    """R-9: keys of ``__call__`` equal the keys of ``cubesat_model.measure`` (values agree)."""
    frozen = cm.load_model(gain_box="aggressive")
    for _, row in designs.head(3).iterrows():
        cfg = row.to_dict()
        got, want = oracle(cfg), frozen.measure(cfg)
        assert list(got) == list(want)
        for k, v in want.items():
            if isinstance(v, bool):
                assert got[k] is v, k
            else:
                assert got[k] == pytest.approx(v, rel=1e-6, abs=1e-9), k


def test_evaluate_gives_the_frozen_column_order(oracle, designs):
    """R-9: ``evaluate`` is the design columns, the measure keys, then the scenario columns."""
    out = oracle.evaluate(designs.head(4))
    frozen = pd.read_csv(FROZEN_CSV, nrows=1)
    assert list(out.columns) == list(frozen.columns)
    assert out["design_id"].tolist() == [0, 1, 2, 3]
    assert out[["slew_deg", "t_end_s", "max_step_s"]].iloc[0].tolist() == [30.0, 600.0, 0.5]
    assert tuple(out[list(co.FLAG_NAMES)].dtypes.astype(str)) == ("bool",) * 4


@pytest.mark.parametrize(
    ("change", "name"),
    [
        ({"panel_span_m": 2.0}, "panel_span_m"),
        ({"battery_wh": 1.0}, "battery_wh"),
        ({"Kp": 5.0}, "Kp"),
        ({"Kd": 0.01}, "Kd"),
        ({"wheel_class": "huge"}, "wheel_class"),
        ({"st_grade": "perfect"}, "st_grade"),
    ],
)
def test_out_of_range_or_unknown_value_raises_naming_the_variable(oracle, designs, change, name):
    cfg = {**designs.iloc[0].to_dict(), **change}
    with pytest.raises(ValueError, match=name):
        oracle(cfg)
    with pytest.raises(ValueError, match=name):
        oracle.evaluate(pd.DataFrame([cfg]))


def test_the_baseline_gain_box_rejects_aggressive_gains(designs):
    base = co.CubesatOracle(TEXT, "nominalSlew", "baseline", workers=1)
    cfg = {**designs.iloc[0].to_dict(), "Kp": 1.9}
    with pytest.raises(ValueError, match="Kp"):
        base(cfg)


def test_unknown_scenario_or_gain_box_is_a_named_error():
    with pytest.raises(co.ScenarioError, match="nowhere"):
        co.CubesatOracle(TEXT, "nowhere", "aggressive", workers=1)
    with pytest.raises(co.ScenarioError, match="gentle"):
        co.CubesatOracle(TEXT, "nominalSlew", "gentle", workers=1)


def test_construction_names_the_cause_when_the_runtime_cannot_start():
    """R-9: a bad OPENSYSML_BINARY fails construction with the cause named (fresh interpreter:
    a client already connected in this process would be reused)."""
    code = (
        "import cubesat_model, pathlib\n"
        "from experiments import cubesat_oracle as co\n"
        f"text = pathlib.Path({str(MODEL)!r}).read_text()\n"
        "try:\n"
        "    co.CubesatOracle(text, 'nominalSlew', 'aggressive')\n"
        "except cubesat_model.OpenSysMLUnavailable as exc:\n"
        "    print('NAMED:', exc)\n"
    )
    env = dict(os.environ, OPENSYSML_BINARY="/nonexistent/sysml-grpc", PYTHONPATH=str(ADCS))
    done = subprocess.run(
        [sys.executable, "-c", code],
        env=env,
        cwd=ADCS,
        capture_output=True,
        text=True,
        timeout=120,
        check=False,
    )
    assert "NAMED: opensysml service binary unavailable" in done.stdout, done.stdout + done.stderr


@pytest.mark.slow
def test_worker_pool_gives_the_serial_result(oracle, designs):
    """Chunks measured in spawned processes equal the serial run (deterministic)."""
    serial = oracle.evaluate(designs)
    pooled = co.CubesatOracle(TEXT, "nominalSlew", "aggressive", workers=2).evaluate(designs)
    pd.testing.assert_frame_equal(serial, pooled)


# -- R-2: nothing about the case is copied into the experiment layer ---------------------------
CORE = (
    "cubesat_oracle",
    "check_designs",
    "feasibility",
    "runner",
    "experiment",
    "ledger",
    "oracle",
)
COPIES = [
    r"1361",
    r"1\.13e-3",
    r"\b5\.0?e4\b",
    r"\b0\.0003\b",
    r"\b0\.226\b",
    r"\b0\.340?\b",
    r"81\.627",
    r"\b140\.0\b",
    r"\b200\.0\b",
    r"\b20\.0\b",
    r"\b0\.03\b",
    r"\b600(\.0)?\b",
    r"\b0\.3 \[",
    r"['\"](small|medium|large|coarse|fine)['\"]",
]


@pytest.mark.parametrize("module", CORE)
def test_no_model_constant_is_copied_into_the_experiment_layer(module):
    """R-2: a grep of the experiment modules finds no enumeration literal, range, gain box,
    scenario number or accounting constant of the model."""
    text = (ADCS / "experiments" / f"{module}.py").read_text()
    code = re.sub(r'""".*?"""', "", text, flags=re.S)  # docstrings may quote the model
    hits = [p for p in COPIES if re.search(p, code)]
    assert not hits, f"{module}.py copies model constants matching {hits}"


def test_editing_the_model_changes_the_sampler_and_the_scenario(tmp_path):
    """R-2: a range, an enum literal and a scenario value edited in a copy reach the Python."""
    edited = (
        TEXT.replace("panelSpanMax : LengthValue = 1.0 [m]", "panelSpanMax : LengthValue = 1.2 [m]")
        .replace("slewAngle : PlaneAngleValue = 30.0", "slewAngle : PlaneAngleValue = 45.0")
        .replace("timeStep : TimeValue = 0.5 [s]", "timeStep : TimeValue = 1.0 [s]")
        .replace("fine", "sharp")
    )
    assert edited != TEXT
    path = tmp_path / "copy.sysml"
    path.write_text(edited)
    exp = dataclasses.replace(
        df.EXPERIMENTS["v2-primary"], model_path="copy.sysml", inputs={}, scenario="nominalSlew"
    )
    smp = co.build_sampler(exp, root=tmp_path)
    assert smp.log_ranges["panel_span_m"][1] == pytest.approx(1.2)
    assert smp.categorical["st_grade"] == ["coarse", "medium", "sharp"]
    base = co.build_sampler(df.EXPERIMENTS["v2-primary"]).draw(30, 0)
    assert smp.draw(30, 0)["panel_span_m"].max() > base["panel_span_m"].max()
    oracle = co.CubesatOracle(edited, workers=1)
    assert oracle.scenario["slew_deg"] == pytest.approx(45.0)
    assert oracle.scenario["max_step_s"] == pytest.approx(1.0)
    assert oracle.ranges["panel_span_m"][1] == pytest.approx(1.2)


# -- R-3: the flags are verdicts of the model's requirements ---------------------------------
def test_the_flags_come_from_the_requirements_not_from_python(oracle, designs, monkeypatch):
    """Replacing the checker's verdicts replaces the flags: nothing else decides them."""

    def inverted(self, subject, measured=None):
        return {f: True for f in FLAGS}

    monkeypatch.setattr(co.FeasibilityChecker, "flags", inverted)
    out = oracle(designs.iloc[0].to_dict())
    assert all(out[f] is True for f in FLAGS)
    monkeypatch.setattr(
        co.FeasibilityChecker, "flags", lambda s, sub, m=None: dict.fromkeys(FLAGS, False)
    )
    out = oracle(designs.iloc[0].to_dict())
    assert all(out[f] is False for f in FLAGS)


def test_no_flag_inequality_in_the_oracle_module():
    """R-3: the oracle compares none of the quantities the requirements read."""
    text = (ADCS / "experiments" / "cubesat_oracle.py").read_text()
    for quantity in ("peak_momentum", "settling_time", "available_power", "dod_eclipse"):
        assert not re.search(rf"{quantity}\w*\s*(<=|>=|<|>)", text), quantity
        assert not re.search(rf"(<=|>=|<|>)\s*\w*{quantity}", text), quantity


# -- the solver's exclusion is recorded, and the flags observe it ----------------------------
def test_the_exclusion_block_records_the_classification_of_the_declared_space(solver):
    block = co.exclusion_block(TEXT)
    assert block["engine"] == "solve" and block["excluded_regions"] == []
    assert block["variant_excluded"] is False
    assert block["verdicts"] == {
        "design-space power": "all-feasible",
        "design-space battery": "mixed",
    }
    assert {r["kind"] for r in block["regions"]} == {"exclusion"}
    assert all(r["satisfiable"][1] in ("proved", "witnessed") for r in block["regions"])
    assert "observations" in block["policy"]
    assert len(block["model_sha256"]) == 64


def test_build_stores_the_exclusion_block_for_the_ledger_entry(solver):
    exp = dataclasses.replace(df.EXPERIMENTS["v2-primary"], inputs={})
    oracle = co.build(exp, workers=1)
    assert (
        oracle.runtime_info["runtime"].startswith("v") and "solve" in oracle.runtime_info["engines"]
    )
    assert exp.inputs["exclusion"]["verdicts"]["design-space battery"] == "mixed"
    again = co.build(exp, workers=1)  # not classified twice
    assert again is not oracle and exp.inputs["exclusion"]["verdicts"]


def test_a_variant_without_a_feasible_configuration_is_not_simulated(solver, tmp_path):
    variant = ex.model_variant(
        TEXT,
        {
            "attribute maxDepthOfDischarge : Real = 0.3;": (
                "attribute maxDepthOfDischarge : Real = 0.03;"
            )
        },
    )
    (tmp_path / "variant.sysml").write_text(variant)
    exp = dataclasses.replace(
        df.EXPERIMENTS["v2-primary"], model_path="variant.sysml", inputs={}, model_sha256=None
    )
    with pytest.raises(co.ExcludedVariant, match="not simulated"):
        co.build(exp, root=tmp_path, workers=1)
    assert exp.inputs["exclusion"]["variant_excluded"] is True
    assert exp.inputs["exclusion"]["excluded_regions"]


def test_a_proved_infeasible_variant_is_recorded_in_the_ledger_before_the_error(solver, tmp_path):
    from experiments import runner

    old = "attribute maxDepthOfDischarge : Real = 0.3;"
    edits = {old: old.replace("0.3;", "0.03;")}
    (tmp_path / "variant.sysml").write_text(ex.model_variant(TEXT, edits))
    exp = dataclasses.replace(
        df.EXPERIMENTS["v2-primary"],
        model_path="variant.sysml",
        model_sha256=None,
        output="out/variant.csv",
        code=(),
        inputs={"variant_edits": edits},
    )
    led = tmp_path / "ledger.jsonl"
    with pytest.raises(co.ExcludedVariant, match="not simulated"):
        runner.run(exp, lambda e: co.build(e, tmp_path, 1), co.build_sampler, tmp_path, led)
    entries = lg.read(led)
    assert len(entries) == 1 and not (tmp_path / "out").exists()  # nothing was simulated
    e = entries[0]
    assert e["kind"] == "exclusion" and e["id"].startswith("v2-primary:exclusion@")
    assert e["output_path"] is None and e["output_sha256"] is None and e["output_rows"] == 0
    assert e["model_sha256"] == lg.sha256_file(tmp_path / "variant.sysml")
    inp = e["inputs"]
    assert inp["variant_edits"] == edits and inp["engine"] == "solve"
    assert inp["excluded_regions"] and inp["claims"] and inp["reason"]
    name = inp["excluded_regions"][0]
    assert inp["verdicts"][name] == "excluded" and set(inp["witnesses"][name]) == {
        "feasible",
        "violation",
    }
    region = next(r for r in inp["regions"] if r["region"]["name"] == name)
    assert region["satisfiable"][0] == "unsatisfiable" and region["model_sha256"]
    assert lg.verify(led, tmp_path) == []
    fresh = dataclasses.replace(exp, inputs={"variant_edits": edits})
    with pytest.raises(co.ExcludedVariant):  # again, a new declaration: recorded once
        runner.run(fresh, lambda e: co.build(e, tmp_path, 1), co.build_sampler, tmp_path, led)
    assert len(lg.read(led)) == 1


def _in_battery(designs: pd.DataFrame, lo: float, hi: float, n: int, seed: int) -> pd.DataFrame:
    """``n`` sampled designs with the battery log-uniform in ``[lo, hi]``."""
    g = np.random.default_rng(seed)
    out = designs.head(n).copy()
    out["battery_wh"] = np.exp(g.uniform(np.log(lo), np.log(hi), n))
    return out


def test_flags_observe_the_excluded_battery_region(oracle, designs, solver):
    """A battery region the solver proves infeasible: every sampled design has dod_ok False."""
    assert classify_region(TEXT, battery_region((20, 26)), connection=oracle.connection).excluded
    out = oracle.evaluate(_in_battery(designs, 20.0, 26.0, 6, seed=1))
    assert not out["dod_ok"].any(), out[["battery_wh", "dod_eclipse", "dod_ok"]]
    assert (out["eclipse_reserve_wh"] <= 0).all()


def test_flags_observe_the_all_feasible_battery_region(oracle, designs, solver):
    """With the slew loss bounded, 40 Wh and up is proved feasible: dod_ok True throughout."""
    region = battery_region((40, 200), slew_energy_wh=(0, 2))
    assert classify_region(TEXT, region, connection=oracle.connection).verdict == "all-feasible"
    out = oracle.evaluate(_in_battery(designs, 40.0, 200.0, 6, seed=2))
    assert out["dod_ok"].all()
    assert (out["slew_loss_energy_wh"] <= 2).all()


def test_ledger_ready_record_of_an_excluded_region(oracle, solver):
    rec = ex.exclusion_record(
        classify_region(TEXT, battery_region((20, 26)), connection=oracle.connection)
    )
    assert rec["excluded"] is True and rec["verdict"] == "excluded"
    assert (
        rec["satisfiable"] == ["unsatisfiable", "proved"] and "none is simulated" in rec["reason"]
    )
    assert lg.hash_entry({"x": rec})  # serialisable into the ledger


def test_equal_settling_and_slew_times_are_analysed(oracle, designs):
    """The analysis returns computed attributes only, so a stiff loop that crosses both thresholds
    in one step (equal settling and slew times) is analysed in one call and both times enter the
    row exactly as measured."""
    loaded, symbols = oracle._configure([{**designs.iloc[0].to_dict(), "design_id": 0}])
    measured = {
        "torque_squared_integral": 1e-5,
        "peak_torque": 1e-3,
        "peak_momentum": 4e-3,
        "settling_time": 14.398119154048933,
        "slew_time": 14.398119154048933,
        "control_effort": 1e-2,
        "censored": False,
    }
    got = oracle._analyse(loaded, symbols[0], measured)
    assert got["settling_time_s"] == got["slew_time_s"] == 14.398119154048933
    assert list(got) == list(co.ATTRIBUTE_NAMES)
    distinct = oracle._analyse(loaded, symbols[0], {**measured, "slew_time": 10.0})
    for k in co.ATTRIBUTE_NAMES[2:]:
        assert got[k] == pytest.approx(distinct[k], rel=1e-12), k
    assert "nextafter" not in pathlib.Path(co.__file__).read_text()


# -- the sampler consumes the regions the solver excludes (B2) -------------------------------------
def test_sampler_skips_a_solver_excluded_battery_region(oracle, exp, solver):
    """Constructed space, 20 to 26 Wh excluded: draws avoid it and equal the base minus it."""
    from experiments.runner import ExcludingSampler

    rec = ex.exclusion_record(
        classify_region(TEXT, battery_region((20, 26)), connection=oracle.connection)
    )
    assert rec["excluded"]
    base = co.build_sampler(exp)
    smp = ExcludingSampler(base, [rec], {"capacity_wh": "battery_wh"})
    got = smp.draw(60, 0)
    assert not got["battery_wh"].between(20.0, 26.0).any()
    wide = base.draw(smp.examined, 0)
    inside = wide["battery_wh"].between(20.0, 26.0)
    pd.testing.assert_frame_equal(got, wide[~inside].head(60).reset_index(drop=True))
    assert smp.avoided == int(inside.sum()) > 0
    assert smp.record()["avoided_by_region"] == {"battery": smp.avoided}


@pytest.mark.slow
def test_declared_space_excludes_nothing_so_the_first_designs_are_unchanged(tmp_path):
    """The v2 block excludes no region: the runner's draws and rows equal the committed dataset."""
    from experiments import runner

    cell = dataclasses.replace(
        df.EXPERIMENTS["v2-primary"],
        count=20,
        inputs={},
        code=(),
        model_path=str(MODEL),
        model_sha256=None,
        output="primary20.csv",
    )
    [e] = runner.run(cell, co.build, co.build_sampler, tmp_path, tmp_path / "ledger.jsonl")
    assert "excluded_sampling" not in e["inputs"]
    got = pd.read_csv(tmp_path / "primary20.csv")
    want = pd.read_csv(ADCS / "data" / "v2" / "adcs_designs_cubesat_gains.csv").head(20)
    assert got.columns.tolist() == want.columns.tolist()
    if exact_only("v2_first_designs_rows"):  # the environment of record: byte-equal rows
        pd.testing.assert_frame_equal(got, want, check_exact=False, rtol=1e-6)
        got_text = (tmp_path / "primary20.csv").read_text().splitlines()
        want_text = (
            (ADCS / "data" / "v2" / "adcs_designs_cubesat_gains.csv").read_text().splitlines()
        )
        assert got_text == want_text[:21]
        return
    # elsewhere: the frozen reproducibility tolerances (paper/environment_values.toml)
    tol = listed()["v2_first_designs_rows"]
    labels = ["design_id", "seed", "wheel_class", "st_grade", *cmp.FLAGS]
    for col in labels:
        assert (got[col].to_numpy() == want[col].to_numpy()).all(), col
    for col in got.columns:
        if col in labels:
            continue
        if col in cmp.TIME_COLUMNS:
            kw = {"rtol": 0, "atol": tol["time_atol"]}
        elif col == "torque_saturated_frac":
            kw = {"rtol": 0, "atol": tol["saturation_atol"]}
        else:
            kw = {"rtol": tol["values_rtol"], "atol": 1e-6}
        np.testing.assert_allclose(got[col], want[col], err_msg=col, **kw)

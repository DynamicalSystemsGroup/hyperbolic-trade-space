"""WP16 D-6: the sensitivity module's perturbation, comparison and write guard (fast, no oracle)."""

import hashlib
import json
import types
from pathlib import Path

import numpy as np
import pandas as pd
import pytest
from experiments import sensitivity as sens
from experiments.cubesat_oracle import ATTRIBUTE_NAMES, OUTPUT_NAMES, SCENARIO_COLUMNS

DATA = Path(__file__).resolve().parents[1] / "examples" / "adcs" / "data"


def _designs(n=50):
    g = np.random.default_rng(7)
    return pd.DataFrame({
        "design_id": range(n),
        "wheel_class": ["small"] * n,
        "panel_span_m": g.uniform(0.3, 1.0, n),
        "battery_wh": g.uniform(20, 200, n),
        "Kp": g.uniform(0.2, 2.0, n),
        "Kd": g.uniform(0.3, 1.5, n),
    })  # fmt: skip


def test_perturbation_is_bounded_and_touches_only_the_four_variables():
    d = _designs()
    p = sens.perturb(d, 3)
    for c in sens.PERTURBED:
        rel = np.abs(p[c] / d[c] - 1)
        assert rel.max() <= 1e-12
        assert rel.max() > 1e-14  # actually perturbed, and not by a constant
    assert p["design_id"].equals(d["design_id"]) and p["wheel_class"].equals(d["wheel_class"])
    assert list(p.columns) == list(d.columns)


def test_perturbation_is_seeded_and_reproducible_and_leaves_its_input_alone():
    d = _designs()
    before = d.copy()
    a, b = sens.perturb(d, 1), sens.perturb(d, 1)
    assert a.equals(b)
    assert d.equals(before)
    assert not a.equals(sens.perturb(d, 2))
    # one (n, 4) draw of default_rng(seed), uniform in [-1e-12, 1e-12], columns in order
    e = np.random.default_rng(1).uniform(-1e-12, 1e-12, size=(len(d), 4))
    for j, c in enumerate(sens.PERTURBED):
        assert np.array_equal(a[c].to_numpy(), d[c].to_numpy() * (1.0 + e[:, j]))


def test_perturbation_signs_and_the_control_seed():
    d = _designs(400)
    p = sens.perturb(d, 5)
    rel = (p["Kp"] / d["Kp"] - 1).to_numpy()
    assert (rel > 0).any() and (rel < 0).any()  # both signs, as a symmetric interval gives
    assert sens.perturb(d, 0).equals(d)  # seed 0: the unperturbed control
    assert sens.perturb(d, 1, eps=0.0).equals(d)


def _table(settling, slew, ok=True):
    return pd.DataFrame({
        "settling_time_s": settling, "slew_time_s": slew, "total_mass_kg": [10.0, 12.0, 0.0],
        "settled": [True, True, ok], "power_ok": [True] * 3, "momentum_ok": [True] * 3,
        "dod_ok": [True] * 3, "wheel_class": ["s", "m", "l"], "st_grade": ["c", "m", "f"],
    })  # fmt: skip


def test_column_deviation_on_two_synthetic_tables():
    a, b = _table([10.0, 20.0, 30.0], [5.0, 6.0, 7.0]), _table([10.0, 20.2, 30.0], [5.0, 6.0, 7.5])
    dev = sens.column_deviation(
        b, a, ["settling_time_s", "slew_time_s", "total_mass_kg"]
    )  # zeros in the reference are skipped for the relative figure
    assert dev.loc["settling_time_s", "max abs"] == pytest.approx(0.2)
    assert dev.loc["settling_time_s", "max rel"] == pytest.approx(0.2 / 20.0)
    assert dev.loc["slew_time_s", "max rel"] == pytest.approx(0.5 / 7.0)
    assert dev.loc["total_mass_kg", "max abs"] == 0.0
    d = sens.table_differences(_table([1.0] * 3, [1.0] * 3, ok=False), a)
    assert d["flag cells changed"] == 1 and d["feasible designs changed"] == 1
    assert d["label cells changed"] == 0 and d["rows"] == (3, 3)


def test_comparison_separates_printed_change_from_exact_change():
    committed = {
        "tau | primary K=1 | tau selected (printed .1f)": "49.3",
        "contending | primary K=1 term 1 | set": "a, b",
        "D k_table | primary | 1 | objective_": 0.123456,
        "D k_table | primary | 2 | objective_": 0.5,
        "predict | proposal_1 | outcome": "log V pass, position miss",
        "tension | primary | x, y | pearson sign": "-",
    }
    runs = {
        "1": {**committed, "D k_table | primary | 1 | objective_": 0.123457},  # same at .4g
        "2": {**committed, "D k_table | primary | 2 | objective_": 0.5001},  # differs at .4g
    }
    t = sens.compare_runs(committed, runs).set_index("quantity")
    same_printed = t.loc["D k_table | primary | 1 | objective_"]
    assert not same_printed["printed change"] and not same_printed["identical"]
    assert same_printed["min"] == 0.123456 and same_printed["max"] == 0.123457
    assert t.loc["D k_table | primary | 2 | objective_", "printed change"]
    assert t.loc["contending | primary K=1 term 1 | set", "identical"]
    assert t.loc["contending | primary K=1 term 1 | set", "runs equal"] == 2
    assert not t.loc["contending | primary K=1 term 1 | set", "numeric"]


def test_verdicts_name_the_conclusion_that_differs():
    committed = {
        "contending | primary K=1 term 1 | set": "a, b",
        "tension | primary | x, y | pearson sign": "-",
        "tension | primary | x, y | pearson": -0.30,
        "predict | proposal_1 | outcome": "log V pass, position miss",
    }
    runs = {"1": dict(committed), "2": {**committed, "tension | primary | x, y | pearson": -0.4}}
    ver = sens.verdicts(sens.compare_runs(committed, runs)).set_index("conclusion")
    tension = next(i for i in ver.index if i.startswith("the signs of the tensions"))
    assert ver.loc[tension, "identical"]  # the value moved, the sign did not
    assert ver.loc[next(i for i in ver.index if "contending" in i), "identical"]
    runs["2"]["contending | primary K=1 term 1 | set"] = "a, c"
    ver = sens.verdicts(sens.compare_runs(committed, runs)).set_index("conclusion")
    bad = ver[~ver["identical"]]
    assert any("contending sets" in i for i in bad.index)
    assert any("contending | primary K=1 term 1 | set" in q for q in bad["differing"].sum())


def _sha_tree(root: Path) -> dict:
    return {
        str(p): hashlib.sha256(p.read_bytes()).hexdigest()
        for p in sorted(root.rglob("*"))
        if p.is_file() and "__pycache__" not in p.parts
    }


def test_the_guard_refuses_the_committed_data_directories(tmp_path):
    for bad in (DATA, DATA / "v2", DATA / "v2" / "new", DATA / "scope-sensitivity"):
        with pytest.raises(ValueError, match="refusing to write inside examples/adcs/data"):
            sens.guard(bad)
    assert sens.guard(tmp_path / "x") == (tmp_path / "x").resolve()
    before = _sha_tree(DATA)
    with pytest.raises(ValueError):
        sens.main(["regenerate", "--out", str(DATA / "v2")])
    with pytest.raises(ValueError):
        sens.regenerate(DATA, 1)
    with pytest.raises(ValueError):
        sens.main(["analyse", "--out", str(tmp_path), "--md", str(DATA / "v2" / "x.md")])
    assert _sha_tree(DATA) == before  # nothing created, nothing changed


class _StubOracle:
    """Stands in for the model-backed oracle: the designs, zeros for every measured column."""

    config_names = ("panel_span_m", "battery_wh", "wheel_class", "st_grade", "Kp", "Kd")
    attribute_names = ATTRIBUTE_NAMES
    flag_names = ("settled", "momentum_ok", "power_ok", "dod_ok")

    def __init__(self, *a, **k):
        pass

    def evaluate(self, designs):
        out = designs.sort_values("design_id").reset_index(drop=True)
        meas = pd.DataFrame({c: [1.0] * len(out) for c in OUTPUT_NAMES})
        for c in self.flag_names:
            meas[c] = True
        scen = pd.DataFrame({c: [0.0] * len(out) for c in SCENARIO_COLUMNS})
        return pd.concat([out, meas, scen], axis=1)


def test_regenerate_writes_only_under_the_scratch_directory(tmp_path, monkeypatch):
    def draw(n, seed):
        d = _designs(n)
        d["st_grade"] = "coarse"
        d["seed"] = seed
        return d

    monkeypatch.setattr(sens, "build_sampler", lambda exp: types.SimpleNamespace(draw=draw))
    monkeypatch.setattr(sens, "CubesatOracle", _StubOracle)
    before = _sha_tree(DATA)
    ledger = DATA.parent / "experiments" / "ledger" / "ledger.jsonl"
    ledger_sha = hashlib.sha256(ledger.read_bytes()).hexdigest()
    target = sens.regenerate(tmp_path, 2, workers=1, n=12)
    assert target == (tmp_path / "seed2").resolve()
    written = sorted(p.name for p in tmp_path.rglob("*") if p.is_file())
    assert written == sorted([
        sens.PRIMARY_FILE, sens.BASELINE_FILE, sens.CHECKS_FILE,
        sens.PREDICTIONS_FILE, sens.COMMITTED_CHECKS_FILE,
    ])  # fmt: skip
    assert len(pd.read_csv(target / sens.PRIMARY_FILE)) == 12
    assert len(pd.read_csv(target / sens.CHECKS_FILE)) == 6
    assert _sha_tree(DATA) == before
    assert hashlib.sha256(ledger.read_bytes()).hexdigest() == ledger_sha


def test_the_module_names_no_write_to_the_ledger_or_the_data_directory():
    src = (Path(sens.__file__)).read_text(encoding="utf-8")
    assert "lg.append" not in src and "runner.run" not in src and "ledger.jsonl" not in src
    # the only writers are the guarded ones
    assert (
        src.count(".to_csv(") == 1 and src.count(".write_text(") == 3
    )  # the cache, the report, the summary


# -- the compact results file the paper reads ------------------------------------------------------


def test_summary_keeps_the_committed_value_inside_its_range_and_flags_identity():
    committed = {"a | r | x": 1.0, "a | r | n": 7, "a | r | s": "u", "a | r | f": True}
    runs = {
        "1": {"a | r | x": 1.5, "a | r | n": 7, "a | r | s": "u", "a | r | f": True},
        "2": {"a | r | x": 0.5, "a | r | n": 8, "a | r | s": "v", "a | r | f": True},
    }
    r = sens.summarise(committed, runs)
    q = r["quantities"]
    assert r["seeds"] == [1, 2] and r["perturbation"]["relative_half_width"] == sens.EPS
    assert q["a | r | x"] == {"committed": 1.0, "min": 0.5, "max": 1.5, "identical": False}
    assert q["a | r | n"]["min"] == 7 and q["a | r | n"]["max"] == 8
    assert q["a | r | s"] == {"identical": False} and q["a | r | f"] == {"identical": True}
    assert list(q) == sorted(q)  # deterministic order


def test_the_results_file_is_written_deterministically_and_guarded(tmp_path):
    committed, runs = {"a | r | x": 1.0 / 3.0}, {"1": {"a | r | x": 2.0 / 3.0}}
    one, two = tmp_path / "one.json", tmp_path / "two.json"
    sens.write_summary(one, committed, runs)
    sens.write_summary(two, committed, runs)
    assert one.read_bytes() == two.read_bytes()
    assert (
        json.loads(one.read_text(encoding="utf-8"))["quantities"]["a | r | x"]["min"]
        == 0.3333333333
    )
    with pytest.raises(ValueError, match="refusing to write inside examples/adcs/data"):
        sens.write_summary(DATA / "v2" / "x.json", committed, runs)


@pytest.fixture(scope="module")
def recomputed():
    return sens.quantities(DATA / "v2")  # the data of record the paper reads (WP23)


@pytest.mark.slow
def test_the_results_file_committed_values_equal_the_committed_case_results(recomputed):
    """Every number of the file's ``committed`` column is what ``case.py`` gives on the data."""
    saved = json.loads(sens.SUMMARY_FILE.read_text(encoding="utf-8"))
    assert set(saved["quantities"]) == set(recomputed)
    for name, e in saved["quantities"].items():
        now = recomputed[name]
        if "committed" not in e:
            continue
        if isinstance(now, (bool, str)):
            continue
        if isinstance(e["committed"], int):
            assert now == e["committed"], name
        else:  # floats: the file keeps ten digits; solver residues follow the platform
            assert now == pytest.approx(e["committed"], rel=1e-6, abs=1e-9, nan_ok=True), name

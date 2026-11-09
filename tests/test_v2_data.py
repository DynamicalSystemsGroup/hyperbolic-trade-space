"""The v2 generation (WP15 15.4): files, ledger, reproducibility and the comparison report.

R-11 every file in ``data/`` and ``data/v2/`` has a ledger entry with equal hashes, and the frozen
files are untouched; R-13 the v2 files have the frozen columns, order and row counts, and the
predictions entry precedes the check-design simulation; R-14 the first designs of each file
regenerate within the frozen tolerances and 40 designs regenerated twice are identical; R-15 the
change register covers every difference beyond tolerance and names no difference that does not
exist (equality of the generations is not required).

Tests that regenerate need the opensysml runtime: they FAIL with the named cause, never skip
(also without ``REQUIRE_OPENSYSML``).
"""

from __future__ import annotations

import pathlib
import subprocess

import cubesat_model as cm
import numpy as np
import pandas as pd
import pytest
from experiments import check_designs as cd
from experiments import compare as cmp
from experiments import cubesat_oracle as co
from experiments import definitions as df
from experiments import ledger as lg
from experiments.__main__ import main as cli

ROOT = pathlib.Path(__file__).resolve().parents[1]
ADCS = ROOT / "examples" / "adcs"
FROZEN = ADCS / "data"
V2 = FROZEN / "v2"
LEDGER = ADCS / "experiments" / "ledger" / "ledger.jsonl"
REGISTER = ADCS / "experiments" / "reports" / cmp.REGISTER
REPORT = ADCS / "experiments" / "reports" / cmp.REPORT
# the commit from which the frozen CSVs must be unchanged (the WP15 scope's start)
START = "fc2363e"
ROWS = {
    "adcs_designs_cubesat_gains.csv": 1000,
    "adcs_designs_cubesat.csv": 1000,
    "check_predictions_cubesat.csv": 3,
    "check_designs_cubesat.csv": 6,
}
ENTRY = {
    "adcs_designs_cubesat_gains.csv": "v2-primary",
    "adcs_designs_cubesat.csv": "v2-baseline",
    "check_predictions_cubesat.csv": "v2-check-predictions",
    "check_designs_cubesat.csv": "v2-check-designs",
}

SAT_ATOL = 0.01  # torque_saturated_frac: absolute tolerance, evidence in swap-evidence.md


@pytest.fixture(scope="module")
def entries():
    return lg.read(LEDGER)


@pytest.fixture(scope="module")
def text():
    return (ADCS / "model_v2" / "cubesat.sysml").read_text()


def _git(*args) -> str | None:
    try:
        done = subprocess.run(
            ["git", "-C", str(ROOT), *args], capture_output=True, text=True, check=True
        )
    except (OSError, subprocess.CalledProcessError):
        return None
    return done.stdout.strip()


# ---------------------------------------------------------------------------------------------
# R-13: the files
# ---------------------------------------------------------------------------------------------
@pytest.mark.parametrize("name", sorted(ROWS))
def test_v2_file_has_the_frozen_columns_in_order_and_the_stated_rows(name):
    v2, frozen = pd.read_csv(V2 / name), pd.read_csv(FROZEN / name)
    assert list(v2.columns) == list(frozen.columns)
    assert len(v2) == ROWS[name]
    assert len(frozen) == ROWS[name]
    assert v2["design_id"].tolist() == frozen["design_id"].tolist()


def test_the_v2_directory_holds_exactly_the_four_files():
    assert sorted(p.name for p in V2.glob("*")) == sorted(ROWS)


@pytest.mark.parametrize("name", ["adcs_designs_cubesat_gains.csv", "adcs_designs_cubesat.csv"])
def test_scenario_seed_and_count_of_the_main_datasets(name, entries):
    v2 = pd.read_csv(V2 / name)
    assert v2["design_id"].tolist() == list(range(1000))
    assert set(v2["slew_deg"]) == {30.0} and set(v2["t_end_s"]) == {600.0}
    assert set(v2["max_step_s"]) == {0.5}
    inp = lg.latest(entries, ENTRY[name])["inputs"]
    assert (inp["count"], inp["seed"], inp["scenario"]) == (1000, 0, "nominalSlew")


def test_the_check_designs_are_the_candidates_and_the_proposals():
    checks = pd.read_csv(V2 / "check_designs_cubesat.csv")
    assert checks["role"].tolist() == ["candidate"] * 3 + ["proposal"] * 3
    assert checks["design_id"].tolist() == [1001, 1002, 1003, 1004, 1005, 1006]
    props = pd.read_csv(V2 / "check_predictions_cubesat.csv")
    assert checks["name"].tolist()[3:] == props["name"].tolist()
    assert set(checks["seed"]) == {df.CHECK_SEED}


def test_the_declared_candidates_are_the_frozen_candidates():
    import make_check_designs as frozen

    assert [dict(c) for c in df.CANDIDATES] == frozen.CANDIDATES


# ---------------------------------------------------------------------------------------------
# R-11: every data file has an entry; hashes equal; the frozen files are untouched
# ---------------------------------------------------------------------------------------------
def test_every_frozen_and_v2_file_has_a_ledger_entry_with_the_file_hash(entries):
    files = sorted(FROZEN.glob("*.csv")) + sorted(V2.glob("*.csv"))
    assert len(files) == 9
    by_path = {e["output_path"]: e for e in entries}
    for f in files:
        rel = f.relative_to(ROOT).as_posix()
        assert rel in by_path, f"{rel} has no ledger entry"
        e = by_path[rel]
        assert e["output_sha256"] == lg.sha256_file(f), rel
        assert e["output_rows"] == len(pd.read_csv(f)), rel
        assert e["kind"] == ("generated" if f.parent == V2 else "adopted"), rel


def test_each_generated_entry_records_the_model_code_and_exclusion(entries):
    for entry_id in ENTRY.values():
        e = lg.latest(entries, entry_id)
        assert e["kind"] == "generated" and e["evidence_kind"] == "simulation"
        assert e["model_path"] == df.V2_MODEL and len(e["model_sha256"]) == 64
        assert set(e["code"]) >= {f"{df.ADCS}/experiments/cubesat_oracle.py"}
        if entry_id in ("v2-primary", "v2-baseline", "v2-check-designs"):
            block = e["inputs"]["exclusion"]
            assert block["engine"] == "solve" and block["excluded_regions"] == []
            assert block["verdicts"] == {
                "design-space power": "all-feasible",
                "design-space battery": "mixed",
            }
            assert "observations" in block["policy"]
            assert e["versions"]["runtime"]["runtime"].startswith("v")


def test_predict_precedes_simulate_in_the_ledger_and_in_the_history(entries):
    ids = [e["id"] for e in entries]
    prim = lg.latest(entries, "v2-primary")
    pred, sim = lg.latest(entries, "v2-check-predictions"), lg.latest(entries, "v2-check-designs")
    assert ids.index(prim["id"]) < ids.index(pred["id"]) < ids.index(sim["id"])
    assert [p["id"] for p in pred["parents"]] == [prim["id"]]
    assert [p["id"] for p in sim["parents"]] == [pred["id"]]
    assert sim["parents"][0]["output_sha256"] == pred["output_sha256"]
    assert sim["parents"][0]["entry_hash"] == pred["entry_hash"]
    assert pred["time_utc"] <= sim["time_utc"]
    first = {
        name: (
            _git("log", "--reverse", "--format=%H", "--", f"examples/adcs/data/v2/{name}") or ""
        ).splitlines()[:1]
        for name in ("check_predictions_cubesat.csv", "check_designs_cubesat.csv")
    }
    p, s = first["check_predictions_cubesat.csv"], first["check_designs_cubesat.csv"]
    if p and s:  # a shallow clone has no history to read
        assert p != s, "the predictions and the check designs were committed together"
        assert _git("merge-base", "--is-ancestor", p[0], s[0]) is not None, (
            "the predictions file was not committed before the check designs"
        )


def test_experiments_verify_passes(capsys):
    assert lg.verify(LEDGER, ROOT) == []
    assert cli(["--root", str(ROOT), "--ledger", str(LEDGER), "verify"]) == 0
    assert "0 drifts" in capsys.readouterr().out


def test_the_frozen_csvs_are_untouched_since_the_start():
    if _git("cat-file", "-e", f"{START}^{{commit}}") is None:
        pytest.fail(f"the history lacks the start commit {START}; fetch full history")
    changed = _git("diff", "--stat", f"{START}..HEAD", "--", ":(glob)examples/adcs/data/*.csv")
    assert changed == "", changed


# ---------------------------------------------------------------------------------------------
# R-14: reproducibility (needs the runtime)
# ---------------------------------------------------------------------------------------------
def _oracle(text, gain_box, workers=1):
    try:
        return co.CubesatOracle(text, "nominalSlew", gain_box, workers=workers)
    except cm.OpenSysMLUnavailable as exc:
        pytest.fail(f"the opensysml client could not start: {exc}", pytrace=False)


def _assert_within_frozen_tolerances(committed: pd.DataFrame, fresh: pd.DataFrame, box: str):
    """The tolerances of ``test_cubesat_model.test_dataset_reproducible_first_20``."""
    assert list(committed.columns) == list(fresh.columns)
    exact = ["design_id", "seed", "wheel_class", "st_grade", *cmp.FLAGS]
    for col in exact:
        assert (committed[col].to_numpy() == fresh[col].to_numpy()).all(), col
    rtol = 1e-4 if box == "baseline" else 1e-3
    special = {*cmp.TIME_COLUMNS, "torque_saturated_frac"}
    for col in committed.columns:
        if col in exact or col in special:
            continue
        np.testing.assert_allclose(committed[col], fresh[col], rtol=rtol, atol=1e-6, err_msg=col)
    # torque_saturated_frac is a step count over about 1340 accepted steps of an adaptive solver
    # (a diagnostic, not a fitted attribute): compared with an absolute tolerance of 0.01 and no
    # relative term (work-packages/swap-evidence.md).
    np.testing.assert_allclose(
        committed.torque_saturated_frac, fresh.torque_saturated_frac, rtol=0, atol=SAT_ATOL
    )
    for col in cmp.TIME_COLUMNS:
        np.testing.assert_allclose(committed[col], fresh[col], atol=0.5, err_msg=col)


@pytest.mark.slow
@pytest.mark.parametrize(
    ("name", "box"),
    [("adcs_designs_cubesat_gains.csv", "aggressive"), ("adcs_designs_cubesat.csv", "baseline")],
)
def test_first_20_designs_regenerate_within_the_frozen_tolerances(name, box, text):
    oracle = _oracle(text, box)
    exp = df.EXPERIMENTS[ENTRY[name]]
    designs = co.build_sampler(exp).draw(20, exp.seed)
    _assert_within_frozen_tolerances(pd.read_csv(V2 / name).head(20), oracle.evaluate(designs), box)


def test_the_check_designs_regenerate_within_the_tolerances(text):
    exp = df.EXPERIMENTS["v2-check-designs"]
    designs = cd.Checks(exp).draw(exp.count, exp.seed)
    oracle = cd.CheckOracle(_oracle(text, "aggressive"))
    fresh = oracle.evaluate(designs)
    committed = pd.read_csv(V2 / "check_designs_cubesat.csv")
    assert list(fresh.columns) == list(committed.columns)
    for col in ("role", "name", "wheel_class", "st_grade", *cmp.FLAGS):
        assert (committed[col].to_numpy() == fresh[col].to_numpy()).all(), col
    for col in committed.columns:
        if col in ("role", "name", "wheel_class", "st_grade", *cmp.FLAGS):
            continue
        atol = 0.5 if col in cmp.TIME_COLUMNS else 1e-6
        if col == "torque_saturated_frac":  # absolute 0.01, no relative term (swap-evidence.md)
            rtol, atol = 0, SAT_ATOL
        else:
            rtol = 1e-3
        np.testing.assert_allclose(committed[col], fresh[col], rtol=rtol, atol=atol, err_msg=col)


@pytest.mark.slow
def test_the_predictions_regenerate_within_the_tolerances(text):
    """Re-proposing from the committed primary data gives the committed proposals."""
    _oracle(text, "aggressive")  # names the cause when the runtime cannot start
    exp = df.EXPERIMENTS["v2-check-predictions"]
    fresh = cd.Proposer(exp).draw(exp.count, exp.seed)
    committed = pd.read_csv(V2 / "check_predictions_cubesat.csv")
    assert list(fresh.columns) == list(committed.columns)
    for col in ("role", "name", "wheel_class", "st_grade"):
        assert (committed[col].to_numpy() == fresh[col].to_numpy()).all(), col
    for col in committed.columns:
        if col not in ("role", "name", "wheel_class", "st_grade"):
            np.testing.assert_allclose(
                committed[col], fresh[col], rtol=1e-3, atol=1e-6, err_msg=col
            )


@pytest.mark.slow
@pytest.mark.parametrize(("gain_box"), ["aggressive", "baseline"])
def test_40_designs_regenerated_twice_are_identical(gain_box, text):
    oracle = _oracle(text, gain_box, workers=3)
    designs = co.build_sampler(
        df.EXPERIMENTS["v2-primary" if gain_box == "aggressive" else "v2-baseline"]
    ).draw(40, 0)
    pd.testing.assert_frame_equal(oracle.evaluate(designs), oracle.evaluate(designs))


# ---------------------------------------------------------------------------------------------
# R-15: the comparison report is a report, and the change register covers its differences
# ---------------------------------------------------------------------------------------------
def test_the_register_covers_every_difference_beyond_tolerance_and_none_other():
    exceeded = cmp.exceeded_differences(ROOT)
    assert set(exceeded) == set(ROWS_BY_DATASET)
    rows = cmp.register_rows(REGISTER)
    unexplained, stale = cmp.check_register(exceeded, rows)
    assert unexplained == [], f"differences beyond tolerance without a register row: {unexplained}"
    assert stale == [], f"register rows that name no existing difference: {stale}"


ROWS_BY_DATASET = {"primary": 1, "baseline": 1, "check_predictions": 1, "check_designs": 1}


def _frames():
    base = pd.read_csv(V2 / "adcs_designs_cubesat_gains.csv")
    return base, base.copy()


def test_a_difference_beyond_tolerance_is_found_and_needs_a_row():
    """Negative control: unexplained differences and stale rows fail; a covering row passes."""
    v1, v2 = _frames()
    v2.loc[3, "total_mass_kg"] *= 1.01  # 1 percent, beyond rtol 1e-3
    v2.loc[5, "dod_ok"] = not v2.loc[5, "dod_ok"]  # a flag flips
    v2.loc[7, "settling_time_s"] += 2.0  # beyond 0.5 s
    got = cmp.compare_dataset("primary", v1, v2, dict(cmp.DEFAULT_TOL))
    assert {"primary:total_mass_kg", "primary:dod_ok", "primary:settling_time_s"} <= set(
        got.exceeded
    )
    unexplained, stale = cmp.check_register({"primary": got.exceeded}, [])
    assert set(unexplained) == set(got.exceeded) and stale == []
    covering = [{"n": "CR-1", "covers": list(got.exceeded)}]
    assert cmp.check_register({"primary": got.exceeded}, covering) == ([], [])
    stale_row = [*covering, {"n": "CR-2", "covers": ["primary:Kp"]}, {"n": "CR-3", "covers": []}]
    assert cmp.check_register({"primary": got.exceeded}, stale_row) == ([], ["CR-2", "CR-3"])


def test_a_difference_within_tolerance_is_not_a_difference():
    v1, v2 = _frames()
    v2["total_mass_kg"] *= 1 + 1e-5
    v2["settling_time_s"] += 0.1
    got = cmp.compare_dataset("primary", v1, v2, dict(cmp.DEFAULT_TOL))
    assert got.exceeded == []
    assert max(s.max_rel for s in got.stats if s.column == "total_mass_kg") == pytest.approx(
        1e-5, rel=0.1
    )


def test_changed_columns_and_design_ids_are_reported():
    v1, v2 = _frames()
    got = cmp.compare_dataset(
        "primary", v1, v2.drop(columns=["Kd"]).iloc[1:], dict(cmp.DEFAULT_TOL)
    )
    assert "primary:columns" in got.exceeded and "primary:ids" in got.exceeded
    assert got.only_v1 == ["Kd"] and not got.ids_equal and got.n_shared_ids == 999


def test_register_rows_are_parsed_from_the_table(tmp_path):
    reg = tmp_path / "r.md"
    reg.write_text(
        "| Row | What | Why | Covers | Moves |\n|---|---|---|---|---|\n"
        "| CR-1 | a | b | `primary:Kp`, `primary:Kd` | c |\n| NC-1 | x | y | z |\n"
    )
    rows = cmp.register_rows(reg)
    assert [r["n"] for r in rows] == ["CR-1"] and rows[0]["covers"] == ["primary:Kp", "primary:Kd"]


@pytest.mark.slow
def test_the_report_has_every_section_and_includes_the_register_verbatim(tmp_path):
    before = REGISTER.read_text()
    out = tmp_path / "report.md"
    assert cmp.main(["--root", str(ROOT), "--out", str(out), "--no-runtime"]) == 0
    report = out.read_text()
    assert REGISTER.read_text() == before, "the generator rewrote the hand-written register"
    assert before.rstrip() in report
    for heading in (
        "## Ledger entries of the v2 generation",
        "## Per dataset",
        "## Swap checklist",
        "## Richness conditions on v2",
        "## Closed-form slew against the ODE",
        "## Exclusion by the solver",
        "## Change register",
    ):
        assert heading in report, heading
    for name in ROWS:
        assert name in report
    for cond in ("(a)", "(b)", "(c)", "(d)", "(e)"):
        assert cond in report
    assert "`tests/test_cubesat_model.py`" in report  # a frozen consumer, found by grep


def test_the_committed_report_exists_and_includes_the_register():
    report = REPORT.read_text()
    assert REGISTER.read_text().rstrip() in report
    assert "Ratio estimate/ODE" in report


def test_the_swap_checklist_finds_the_frozen_consumers():
    consumers = cmp.frozen_consumers(ROOT)
    for expected in (
        "examples/adcs/case.py",
        "examples/adcs/k_terms.py",
        "examples/adcs/make_check_designs.py",
        "tests/test_adcs_enrichment.py",
        "tests/test_check_designs.py",
        "tests/test_notebook.py",
    ):
        assert expected in consumers, expected
    assert not any(f.startswith("examples/adcs/data/") for f in consumers)

"""WP15 OD1: the legacy geostationary oracle behind the protocol, and the shared-subspace run.

* the frozen ``design_space.evaluate_design`` satisfies the tool-free ``Oracle`` protocol, with the
  frozen key order (the CSV columns of ``data/adcs_designs.csv`` after the configuration);
* ``scope-sensitivity-shared-subspace`` runs the v2 oracle and the legacy oracle on the same
  designs of the variables the variants share, into a temporary directory, and writes one ledger
  entry per oracle that names the shared subspace;
* the frozen CSV is not touched; the legacy oracle and the core import without ``opensysml``.

The v2 half needs the opensysml client and the solver and fails by name when either is missing.
"""

from __future__ import annotations

import dataclasses
import pathlib
import shutil
import subprocess
import sys

import cubesat_model as cm
import design_space as ds
import pandas as pd
import pytest
from experiments import definitions as df
from experiments import ledger as lg
from experiments import legacy_oracle as lo
from experiments import runner
from experiments.oracle import Oracle

REPO = pathlib.Path(__file__).resolve().parents[1]
ADCS = REPO / "examples" / "adcs"
FROZEN = ADCS / "data" / "adcs_designs.csv"


def _frozen_rows(n=3):
    return pd.read_csv(FROZEN).head(n)


# -- the protocol ------------------------------------------------------------------------------
def test_the_legacy_oracle_satisfies_the_protocol():
    assert isinstance(lo.LegacyGeostationaryOracle(), Oracle)
    assert df.resolve_oracle("legacy-geostationary") is lo.build
    assert df.SHARED_LEGACY.id in df.SHARED_EXPERIMENTS
    assert df.SHARED_LEGACY.evidence_kind == "simulation"


def test_keys_and_order_equal_the_frozen_csv_columns_for_three_designs():
    frozen = _frozen_rows(3)
    oracle = lo.LegacyGeostationaryOracle()
    designs = frozen[["design_id", "seed", *oracle.config_names]]
    out = oracle.evaluate(designs)
    assert list(out.columns) == list(frozen.columns)
    assert (*oracle.attribute_names, *oracle.flag_names) == tuple(
        c for c in frozen.columns if c in (*oracle.attribute_names, *oracle.flag_names)
    )
    one = oracle(designs.iloc[0].to_dict())
    assert tuple(one) == tuple(frozen.columns[len(["design_id", "seed", *oracle.config_names]) :])
    # same numbers as the frozen generator wrote (a single platform: tight but not bitwise)
    for c in ("pointing_error_deg", "adcs_mass_kg", "peak_momentum_nms"):
        assert out[c].tolist() == pytest.approx(frozen[c].tolist(), rel=1e-4)
    assert out["settled"].tolist() == frozen["settled"].tolist()
    assert out["momentum_ok"].tolist() == frozen["momentum_ok"].tolist()


def test_configuration_errors_name_the_variable():
    o, row = lo.LegacyGeostationaryOracle(), _frozen_rows(1).iloc[0].to_dict()
    for name, bad in (("wheel_class", "huge"), ("st_grade", "x"), ("Kp", 100.0), ("Kd", 0.1)):
        with pytest.raises(ValueError, match=name):
            o({**row, name: bad})
    with pytest.raises(ValueError, match="panel_mass_kg"):
        o({**row, "panel_mass_kg": -1.0})


def test_the_legacy_modules_import_without_opensysml():
    code = (
        "import sys; sys.modules['opensysml'] = None; "
        "from experiments import legacy_oracle as lo; "
        "o = lo.LegacyGeostationaryOracle(); print(o.config_names)"
    )
    env_path = f"{ADCS}"
    out = subprocess.run(
        [sys.executable, "-c", code],
        capture_output=True,
        text=True,
        env={"PYTHONPATH": env_path, "PATH": "/usr/bin:/bin"},
    )
    assert out.returncode == 0, out.stderr
    assert "wheel_class" in out.stdout


# -- the shared-subspace experiment, end to end --------------------------------------------------
def _copy_tree(root: pathlib.Path, *exps) -> None:
    paths = {df.V2_MODEL}
    for e in exps:
        paths.update(e.code)
    for rel in paths:
        (root / rel).parent.mkdir(parents=True, exist_ok=True)
        shutil.copy(REPO / rel, root / rel)


@pytest.fixture(scope="module")
def shared_run(tmp_path_factory):
    root = tmp_path_factory.mktemp("shared")
    frozen_before = lg.sha256_file(FROZEN)
    _copy_tree(root, *df.GROUPS[df.SHARED_ID])
    led = root / "ledger.jsonl"
    import os

    os.environ["EXPERIMENTS_WORKERS"] = "1"
    members = [
        dataclasses.replace(e, count=4, inputs=dict(e.inputs)) for e in df.GROUPS[df.SHARED_ID]
    ]
    try:
        entries = []
        for e in members:
            entries += runner.run(
                e, df.resolve_oracle(e.oracle), df.resolve_sampler(e.sampler), root, led
            )
    except cm.OpenSysMLUnavailable as exc:
        pytest.fail(f"the opensysml client could not start: {exc}", pytrace=False)
    finally:
        os.environ.pop("EXPERIMENTS_WORKERS", None)
    return root, led, entries, frozen_before


def test_the_default_run_is_small():
    assert df.SHARED_COUNT == 20
    assert {e.count for e in df.GROUPS[df.SHARED_ID]} == {20}


@pytest.mark.slow
def test_two_ledger_entries_differing_in_oracle_name_the_shared_subspace(shared_run):
    root, led, entries, _ = shared_run
    assert [e["inputs"]["oracle"] for e in entries] == ["cubesat-v2", "legacy-geostationary"]
    assert {e["kind"] for e in entries} == {"generated"}
    assert {e["evidence_kind"] for e in entries} == {"simulation"}
    subs = [e["inputs"]["shared_subspace"] for e in entries]
    assert subs[0] == subs[1]
    varied = subs[0]["varied"]
    assert set(varied["categorical"]) == {"wheel_class", "st_grade"}
    assert list(varied["log_ranges"]) == ["Kp"]
    assert {e["inputs"]["group"] for e in entries} == {df.SHARED_ID}
    assert entries[0]["inputs"]["config_names"] != entries[1]["inputs"]["config_names"]
    assert lg.verify(led, root) == []


def test_the_outputs_are_for_the_same_designs_side_by_side(shared_run):
    root, _, entries, _ = shared_run
    v2, legacy = (pd.read_csv(root / e["output_path"]) for e in entries)
    both = lo.side_by_side(v2, legacy)
    assert len(both) == 4
    for c in ("settling_time_s", "control_effort", "settled", "momentum_ok"):
        assert f"{c}_v2" in both.columns and f"{c}_legacy" in both.columns
    sub = entries[0]["inputs"]["shared_subspace"]["varied"]["log_ranges"]["Kp"]
    assert both["Kp"].between(*sub).all()
    # the legacy half is what the frozen function returns for those configurations
    row = legacy.iloc[0].to_dict()
    again = ds.evaluate_design(row)
    assert again["pointing_error_deg"] == pytest.approx(row["pointing_error_deg"], rel=1e-6)


def test_the_frozen_csv_is_not_touched(shared_run):
    *_, frozen_before = shared_run
    assert lg.sha256_file(FROZEN) == frozen_before
    out = subprocess.run(
        ["git", "-C", str(REPO), "diff", "--stat", "--", "examples/adcs/data/*.csv"],
        capture_output=True,
        text=True,
    )
    assert out.stdout.strip() == ""


def test_the_committed_ledger_registers_the_small_run():
    entries = lg.read(lg.LEDGER_PATH)
    ids = [e["id"] for e in entries]
    assert ids.index("adopted-adcs_designs") < ids.index(df.SHARED_LEGACY.id)
    legacy = lg.find(entries, df.SHARED_LEGACY.id)
    assert legacy["inputs"]["legacy_dataset"] == "adopted-adcs_designs"
    assert legacy["output_rows"] == df.SHARED_COUNT
    assert lg.find(entries, "adopted-adcs_designs")["kind"] == "adopted"

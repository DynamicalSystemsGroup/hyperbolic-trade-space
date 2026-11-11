"""The WP30 cost ladders: the spike's shares reproduced, the repricing check, a small fixture."""

from __future__ import annotations

import ast
import importlib.util
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts/wp30_cost_ladders.py"
SPIKE_DIR = ROOT / "work-packages/WP23-rounds/spikes/spike-D-cubesat-economics"
DATA = ROOT / "examples/adcs/data/v2"


@pytest.fixture(scope="module")
def lad():
    spec = importlib.util.spec_from_file_location("wp30_cost_ladders", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.fixture(scope="module")
def econ(lad):
    return lad.load_prices()


def _fixture(econ, launch=True):
    """Five designs, four feasible, with cost columns priced by the spike's own functions."""
    rows = [
        ("medium", "medium", 0.6, 80.0, 13.291, 1),
        ("small", "coarse", 0.35, 40.0, 11.0, 3),
        ("large", "fine", 0.8, 140.0, 15.0, 10),
        ("medium", "fine", 0.5, 60.0, 12.5, 30),
        ("large", "fine", 0.8, 140.0, 15.0, 2),
    ]
    frame = pd.DataFrame(
        rows,
        columns=[
            "wheel_class",
            "st_grade",
            "panel_span_m",
            "battery_wh",
            "total_mass_kg",
            "fleet_size",
        ],
    )
    for flag in ("settled", "momentum_ok", "power_ok", "dod_ok"):
        frame[flag] = True
    frame.loc[4, "dod_ok"] = False
    fleet = [
        econ["fleet_build"](r.wheel_class, r.st_grade, r.panel_span_m, r.battery_wh, r.fleet_size)
        + econ["LAUNCH_RATE"] * r.total_mass_kg * r.fleet_size * launch
        for r in frame.itertuples()
    ]
    frame["fleet_cost_usd"] = fleet
    frame["unit_cost_usd"] = frame["fleet_cost_usd"] / frame["fleet_size"]
    return frame


def test_no_launch_ladders_reproduce_the_spikes_admit_shares(lad, econ):
    lines = (SPIKE_DIR / "admit-shares.txt").read_text(encoding="utf-8").splitlines()
    seen = 0
    for line in lines:
        name, n, count, rest = line.split(" ", 3)
        regime = "baseline" if name == "adcs_designs_cubesat.csv" else "primary"
        feasible = lad.feasible_rows(pd.read_csv(DATA / lad.REGIMES[regime]))
        assert len(feasible) == int(count)
        _, unit = lad.price(econ, feasible, int(n), launch=False)
        want = ast.literal_eval(rest)
        got = dict(zip(lad.UNIT_LIMITS, lad.shares(unit, lad.UNIT_LIMITS), strict=True))
        for limit, percent in want.items():
            assert round(got[int(limit)], 1) == percent, (name, n, limit)
        seen += 1
    assert seen == 8


def test_feasible_rows_keep_only_designs_where_every_flag_holds(lad, econ):
    assert len(lad.feasible_rows(_fixture(econ))) == 4


def test_repricing_matches_the_data_cost_columns_and_flags_a_difference(lad, econ):
    frame = _fixture(econ)
    assert lad.check_against_data(econ, frame) < 1e-12
    frame.loc[2, "unit_cost_usd"] *= 1.01
    assert lad.check_against_data(econ, frame) == pytest.approx(0.01, rel=0.2)
    assert lad.check_against_data(econ, frame.drop(columns=["unit_cost_usd"])) is None


def test_unit_cost_is_the_fleet_cost_over_n_and_equal_at_one_satellite(lad, econ):
    feasible = lad.feasible_rows(_fixture(econ))
    fleet1, unit1 = lad.price(econ, feasible, 1)
    fleet10, unit10 = lad.price(econ, feasible, 10)
    assert np.allclose(fleet1, unit1) and np.allclose(unit10 * 10, fleet10)
    assert (unit10 < unit1).all()


def test_ladders_are_monotone_in_the_limit_and_n_free_is_the_mean_over_thirty(lad, econ):
    feasible = lad.feasible_rows(_fixture(econ))
    out = lad.ladders(econ, feasible)
    for key in ("unit", "fleet"):
        for row in out[key].values():
            assert row == sorted(row) and row[0] >= 0.0 and row[-1] <= 100.0
    _, unit = lad.price(econ, feasible, 30)
    assert out["unit"][30] == lad.shares(unit, lad.UNIT_LIMITS)
    free = np.mean(
        [lad.shares(lad.price(econ, feasible, n)[1], lad.UNIT_LIMITS) for n in lad.ALL_SIZES],
        axis=0,
    )
    assert np.allclose(out["unit"]["free"], free)


def test_main_writes_the_ladders_and_stops_on_a_mismatch(lad, econ, tmp_path, monkeypatch, capsys):
    data = tmp_path / "v2"
    data.mkdir()
    frame = _fixture(econ)
    for file in lad.REGIMES.values():
        frame.to_csv(data / file, index=False)
    out = tmp_path / "ladders.md"
    monkeypatch.setattr(lad, "OUT", out)
    # OUT.relative_to(ROOT) would fail outside the repository; the message uses it only on write
    monkeypatch.setattr(lad, "ROOT", tmp_path)
    assert lad.main(["--data", str(data), "--write"]) == 0
    text = out.read_text(encoding="utf-8")
    assert "Regime: baseline (4 feasible designs)" in text and "max relative" in text
    frame.loc[0, "fleet_cost_usd"] *= 2
    frame.to_csv(data / lad.REGIMES["baseline"], index=False)
    assert lad.main(["--data", str(data)]) == 2
    assert "differs" in capsys.readouterr().out

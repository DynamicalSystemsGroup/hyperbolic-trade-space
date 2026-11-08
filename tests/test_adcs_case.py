"""Tests for the ADCS case generator (WP4): port pins, design space, dataset."""

from __future__ import annotations

import pathlib
import re

import adcs_sim
import pytest
from adcs_sim import BASELINE, inertia_tensor, run_step_response

ADCS_DIR = pathlib.Path(__file__).resolve().parents[1] / "examples" / "adcs"


def test_inertia_baseline():
    """R-1."""
    jxx, jyy, jzz = inertia_tensor(BASELINE)
    assert jxx == pytest.approx(327.14, abs=0.01)
    assert jyy == pytest.approx(107.48, abs=0.01)
    assert jzz == pytest.approx(303.45, abs=0.01)


def _settling(kp, kd):
    return run_step_response(BASELINE, kp, kd, t_end=360.0).summary()["settling_time_s"]


@pytest.mark.parametrize(
    ("kp", "kd", "expected", "tol"),
    [
        (4, 30, 77.97, 0.2),
        (8, 30, 87.40, 0.2),
        (4, 25, 120.50, 0.2),
        # scope R-2 says 201.6; source repo pins 310.6; amendment pending with supervisor
        (1, 10, 310.6, 0.5),
    ],
)
def test_regression_pins(kp, kd, expected, tol):
    """R-2: settling-time pins of the source repo (10 deg X slew, 360 s)."""
    assert _settling(kp, kd) == pytest.approx(expected, abs=tol)


def test_no_forbidden_imports_and_license():
    """R-3."""
    text = (ADCS_DIR / "adcs_sim.py").read_text()
    for mod in ("rdflib", "sympy", "opensysml", "flexo"):
        assert not re.search(rf"^\s*(import|from)\s+{mod}", text, re.I | re.M)
    assert "Apache License, Version 2.0" in text
    assert adcs_sim.BASELINE["Kp"] == 1.0


# ---------------------------------------------------------------------------------------------
# Design space (R-4..R-7)
# ---------------------------------------------------------------------------------------------
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402
from design_space import (  # noqa: E402
    FAST_SIM,
    KD_RANGE,
    KP_RANGE,
    STAR_TRACKERS,
    WHEEL_CLASSES,
    evaluate_design,
    sample_designs,
)

ATTRS = ["settling_time_s", "pointing_error_deg", "adcs_mass_kg", "control_effort"]


def test_evaluate_design_three_fast():
    """R-4: three designs with FAST_SIM."""
    designs = sample_designs(3, 0)
    out = pd.DataFrame([evaluate_design(r, **FAST_SIM) for _, r in designs.iterrows()])
    for col in ATTRS:
        assert np.isfinite(out[col]).all() and (out[col] > 0).all()
    for flag in ("settled", "momentum_ok", "torque_saturated_frac"):
        assert flag in out
    for (_, r), (_, o) in zip(designs.iterrows(), out.iterrows(), strict=True):
        expected = 3 * WHEEL_CLASSES[r.wheel_class][2] + STAR_TRACKERS[r.st_grade][1] + 0.5
        assert o.adcs_mass_kg == pytest.approx(expected)


def test_pointing_decreases_with_kp_above_floor():
    """R-5: continuous in Kp, strictly above the star-tracker floor."""
    row = {
        "wheel_class": "medium",
        "st_grade": "fine",
        "Kp": 1.0,
        "Kd": 20.0,
        "panel_mass_kg": 30.0,
        "antenna_mass_kg": 18.0,
    }
    floor = STAR_TRACKERS["fine"][0] / 3600
    vals = []
    for kp in np.geomspace(*KP_RANGE, 8):
        row["Kp"] = kp
        vals.append(evaluate_design(row, t_end=20.0, max_step=2.0)["pointing_error_deg"])
    assert np.all(np.diff(vals) < 0)
    assert min(vals) > floor


def test_effort_and_momentum_flag():
    """R-6: effort positive; momentum is a flag against the wheel class limit, not an attribute."""
    row = {
        "wheel_class": "small",
        "st_grade": "medium",
        "Kp": 8.0,
        "Kd": 30.0,
        "panel_mass_kg": 30.0,
        "antenna_mass_kg": 18.0,
    }
    out = evaluate_design(row, **FAST_SIM)
    assert out["control_effort"] > 0
    assert out["momentum_ok"] == (out["peak_momentum_nms"] <= WHEEL_CLASSES["small"][1])
    assert "peak_momentum_nms" not in ATTRS


def test_sampling_reproducible_and_prefix_stable():
    """R-7."""
    a, b, c = sample_designs(50, 7), sample_designs(50, 7), sample_designs(20, 7)
    pd.testing.assert_frame_equal(a, b)
    pd.testing.assert_frame_equal(a.iloc[:20], c)
    assert not a.equals(sample_designs(50, 8))
    g = sample_designs(30, np.random.default_rng(1))
    pd.testing.assert_frame_equal(g, sample_designs(30, np.random.default_rng(1)))
    big = sample_designs(2000, 0)
    assert big.Kp.between(*KP_RANGE).all() and big.Kd.between(*KD_RANGE).all()
    assert set(big.wheel_class) == set(WHEEL_CLASSES) and set(big.st_grade) == set(STAR_TRACKERS)
    # log-uniform: median of log Kp near the middle of the log range
    assert np.log(big.Kp).median() == pytest.approx(np.log(KP_RANGE).mean(), abs=0.1)
    # lognormal mass perturbation, sigma about 0.10
    assert np.log(big.panel_mass_kg / 30.0).std() == pytest.approx(0.10, abs=0.01)
    assert np.log(big.antenna_mass_kg / 18.0).std() == pytest.approx(0.10, abs=0.01)

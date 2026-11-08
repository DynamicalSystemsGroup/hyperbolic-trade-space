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

"""WP56 D-1: the coverage probability in the case's pipeline and the tension matrix's row order.

The coverage probability is defined in the SysML v2 model (``CoverageProbability`` in
``examples/adcs/model_v2/stakeholders.sysml``; the model-side test is in
``test_system_model_v2.py``); here its Python form, its column beside the data of record and the
identity that collapses the decision-maker's ternary onto one trade-off.
"""

from __future__ import annotations

from pathlib import Path

import case
import numpy as np
import pandas as pd
import pytest

DATA = Path(case.CUBESAT.data_dir) / case.CUBESAT.regimes["primary"]


def test_coverage_probability_reads_as_its_definition():
    """One satellite at zero error covers with p0; at e = e0 with p0/e; a fleet of n is
    1 - (1 - p)^n; it rises with the fleet size at a falling rate and falls with the error."""
    e0 = case.CUBESAT.requirements["pointing_error_deg"][0]
    assert case.coverage_probability(1, 0.0) == pytest.approx(case.COVERAGE_P0)
    assert case.coverage_probability(1, e0) == pytest.approx(case.COVERAGE_P0 / np.e)
    p = case.COVERAGE_P0 * np.exp(-0.5)
    assert case.coverage_probability(7, e0 / 2) == pytest.approx(1 - (1 - p) ** 7)
    n = np.arange(1, 31)
    P = case.coverage_probability(n, 0.002)
    assert (np.diff(P) > 0).all() and (np.diff(P, 2) < 0).all()
    e = np.linspace(0.0, 0.02, 21)
    assert (np.diff(case.coverage_probability(10, e)) < 0).all()


def test_coverage_column_on_the_data_of_record():
    """``with_coverage`` adds the column without touching the others; on the primary regime's
    feasible designs it is a probability; fleet cost is unit cost times fleet size on every row
    (the identity behind the ternary's one trade-off)."""
    raw = pd.read_csv(DATA)
    feasible = raw[case.feasible_mask(raw)].reset_index(drop=True)
    out = case.with_coverage(feasible)
    assert list(out.columns) == [*feasible.columns, case.COVERAGE]
    pd.testing.assert_frame_equal(out[feasible.columns], feasible)
    assert out[case.COVERAGE].between(0.0, 1.0).all()
    assert case.COVERAGE not in raw.columns  # computed, not part of the data of record
    ratio = feasible["fleet_cost_usd"] / (feasible["unit_cost_usd"] * feasible["fleet_size"])
    assert np.allclose(ratio, 1.0, rtol=1e-7)


def test_the_ternary_names_one_stakeholder_per_objective():
    assert case.FLEET_TERNARY == ("fleet_cost_usd", "unit_cost_usd", case.COVERAGE)
    assert case.STAKEHOLDER_OF == {
        "fleet_cost_usd": "sponsor",
        "unit_cost_usd": "manufacturer",
        case.COVERAGE: "operator",
    }
    assert "coverage probability" in case.FLEET_TERNARY_TITLE
    assert not set("^=()/") & set(case.FLEET_TERNARY_TITLE)  # the measure's name, no formula


def test_tension_order_puts_every_upper_cell_at_one_or_more():
    """With ``|T[i, j]| = s_i / s_j`` the "tension" order sorts by ``s``, largest first, so every
    cell right of the diagonal is at least one in size; "exponent" keeps the given order."""
    rng = np.random.default_rng(0)
    s = rng.uniform(0.1, 10.0, 6)
    T = -s[:, None] / s[None, :]
    keep = [3, 0, 5, 1, 4, 2]
    assert case.tension_order(T, keep, "exponent") == keep
    order = case.tension_order(T, keep, "tension")
    assert order == sorted(keep, key=lambda i: -s[i])
    assert all(abs(T[i, j]) >= 1 for a, i in enumerate(order) for j in order[a + 1 :])
    with pytest.raises(ValueError, match="order must be one of"):
        case.tension_order(T, keep, "size")

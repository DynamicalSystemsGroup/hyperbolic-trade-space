"""Tests for solvers: R-1 to R-4."""

import numpy as np
import pytest
from scipy.optimize import check_grad

from hyperbolic_trade_space.coordinates import helmert_basis
from hyperbolic_trade_space.datasets import make_frontier_data
from hyperbolic_trade_space.solvers import (
    SolveResult,
    log_mean_exp,
    objective_and_grad,
    solve_lp,
    solve_slsqp,
    support_weights,
)


@pytest.mark.parametrize("tau", [0.1, 1.0, 10.0])
def test_lme_matches_naive(tau):
    s = np.random.default_rng(0).normal(size=50)
    naive = np.log(np.mean(np.exp(tau * s))) / tau
    assert log_mean_exp(s, tau) == pytest.approx(naive, rel=1e-12)


def test_lme_stable_and_inf():
    s = np.array([100.0, 99.0, -5.0])
    assert np.isfinite(log_mean_exp(s, 1e5))
    assert log_mean_exp(s, 1e5) == pytest.approx(100.0 - np.log(3) / 1e5, abs=1e-6)
    assert log_mean_exp(s, np.inf) == 100.0
    assert log_mean_exp(np.array([-np.inf, 1.0]), 2.0) == pytest.approx(1.0 - np.log(2) / 2)


def test_support_weights():
    s = np.array([0.3, 1.0, 1.0 + 1e-14, -2.0])
    p = support_weights(s, np.inf)
    assert p.tolist() == [0.0, 0.5, 0.5, 0.0]
    for tau in (0.5, 10.0, 1e4):
        p = support_weights(s, tau)
        assert (p >= 0).all() and p.sum() == pytest.approx(1.0)
    assert support_weights(np.array([-np.inf, 0.0]), 3.0).tolist() == [0.0, 1.0]


@pytest.mark.parametrize("tau", [0.5, 5.0, 100.0])
def test_gradient_check(tau):
    rng = np.random.default_rng(1)
    U = rng.normal(size=(30, 4))
    w = rng.dirichlet(np.ones(4))
    err = check_grad(
        lambda x: objective_and_grad(x, U, tau)[0], lambda x: objective_and_grad(x, U, tau)[1], w
    )
    assert err < 1e-5 * max(1.0, tau)


def test_lp_hand_built():
    # u = (1,0), (0,1), (0.2,0.2): min over simplex of max -> w=(.5,.5), t=.5; third row slack
    U = np.array([[1.0, 0.0], [0.0, 1.0], [0.2, 0.2]])
    r = solve_lp(U)
    assert isinstance(r, SolveResult) and r.success
    np.testing.assert_allclose(r.w, [0.5, 0.5], atol=1e-9)
    assert r.beta == pytest.approx(0.5) and r.objective == pytest.approx(0.5)
    np.testing.assert_allclose(r.p, [0.5, 0.5, 0.0], atol=1e-9)
    assert r.p.sum() == pytest.approx(1.0) and r.n_iter >= 1


def test_lp_asymmetric_and_floor():
    # rows (2,0),(0,1): min_w max(2 w1, w2) -> w1=1/3, t=2/3; with floor 0.5 -> w1=.5
    U = np.array([[2.0, 0.0], [0.0, 1.0]])
    r = solve_lp(U)
    np.testing.assert_allclose(r.w, [1 / 3, 2 / 3], atol=1e-9)
    assert r.beta == pytest.approx(2 / 3)
    np.testing.assert_allclose(r.p @ U, [r.beta, r.beta], atol=1e-9)  # KKT: U^T p equal
    r = solve_lp(U, min_exponent=0.5)
    np.testing.assert_allclose(r.w, [0.5, 0.5], atol=1e-9)
    assert r.p.sum() == pytest.approx(1.0)


@pytest.mark.parametrize("d", [2, 3, 5])
def test_slsqp_agrees_with_lp(d):
    X, info = make_frontier_data(300, d, noise=0.0, random_state=d)
    U = np.log(X)
    lp = solve_lp(U)
    sq = solve_slsqp(U, 1e3, tol=1e-12)
    assert sq.success
    np.testing.assert_allclose(sq.w, lp.w, atol=2e-2)
    np.testing.assert_allclose(lp.w, info["exponents"], atol=1e-6)
    assert lp.beta - sq.beta >= -1e-9 and lp.beta - sq.beta <= np.log(300) / 1e3 + 1e-9
    assert sq.p.sum() == pytest.approx(1.0) and (sq.p >= 0).all()
    assert sq.objective == pytest.approx(sq.beta)
    assert sq.n_iter >= 1


def test_slsqp_properties_and_tau_inf():
    U = np.log(make_frontier_data(80, 3, random_state=0)[0])
    r = solve_slsqp(U, 20.0, min_exponent=0.1)
    assert (r.w >= 0.1 - 1e-12).all() and r.w.sum() == pytest.approx(1.0)
    assert solve_slsqp(U, np.inf).beta == pytest.approx(solve_lp(U).beta)


def test_chart_free_balance():
    # solver only sees U; sanity that helmert import works with datasets
    assert helmert_basis(2).shape == (1, 2)

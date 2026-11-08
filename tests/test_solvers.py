"""Tests for solvers: R-1 to R-4."""

import numpy as np
import pytest
from scipy.optimize import check_grad, linear_sum_assignment

from hyperbolic_trade_space.coordinates import helmert_basis
from hyperbolic_trade_space.datasets import make_frontier_data
from hyperbolic_trade_space.solvers import (
    SolveResult,
    log_mean_exp,
    objective_and_grad,
    solve_lp,
    solve_slsqp,
    solve_terms,
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


def test_penalty_validation_and_alpha_zero_exact():
    U = np.log(make_frontier_data(80, 3, random_state=0)[0])
    with pytest.raises(ValueError):
        solve_slsqp(U, 20.0, penalty="l2", alpha=1.0)
    with pytest.raises(ValueError):
        solve_slsqp(U, 20.0, penalty="reweighted_l1", alpha=-1.0)
    base = solve_slsqp(U, 20.0)
    for kw in ({"penalty": "reweighted_l1", "alpha": 0.0}, {"penalty": None, "alpha": 5.0}):
        r = solve_slsqp(U, 20.0, **kw)
        np.testing.assert_array_equal(r.w, base.w)
        assert r.beta == base.beta
    lp = solve_slsqp(U, np.inf, penalty="reweighted_l1", alpha=5.0)
    np.testing.assert_array_equal(lp.w, solve_lp(U).w)


def test_reweighted_l1_gives_exact_zeros_on_planted_sparse_facet():
    # d=4, planted exponents [0.6, 0.4, 0, 0], noisy frontier, tau=20, alpha=0.01 (R-11)
    X, _ = make_frontier_data(300, 4, exponents=[0.6, 0.4, 0, 0], noise=0.1, random_state=0)
    U = np.log(X)
    plain = solve_slsqp(U, 20.0)
    pen = solve_slsqp(U, 20.0, penalty="reweighted_l1", alpha=0.01)
    assert plain.w[2] > 1e-3  # small but positive without the penalty
    assert (pen.w[2:] == 0.0).all()  # exact zeros with it
    assert pen.w.sum() == pytest.approx(1.0)
    np.testing.assert_allclose(pen.w[:2], [0.6, 0.4], atol=0.02)
    assert pen.beta == pytest.approx(log_mean_exp(U @ pen.w, 20.0))
    assert pen.p.sum() == pytest.approx(1.0)


_W3 = np.array([[0.7, 0.1, 0.1, 0.1], [0.1, 0.7, 0.1, 0.1], [0.1, 0.1, 0.7, 0.1]])


def _planted_k3(n=400, frac=0.4, seed=0):
    rng = np.random.default_rng(seed)
    base = rng.standard_normal((n, 3)) @ helmert_basis(4)
    log_v = np.where(rng.random(n) < frac, 0.0, -rng.exponential(1.0, n))
    return base + (log_v - (base @ _W3.T).max(axis=1))[:, None]


def _match_error(W):
    import itertools

    return min(np.abs(W[list(p)] - _W3).max() for p in itertools.permutations(range(3)))


@pytest.mark.parametrize("tau", [np.inf, 50.0])
def test_terms_recovers_planted_k3(tau):
    # N=400, 40% of rows on the frontier; the recovery needs a few restarts at moderate tau
    for seed in range(3):
        r = solve_terms(_planted_k3(seed=seed), 3, tau, random_state=seed)
        assert _match_error(r.W) < 0.05
        assert set(np.unique(r.labels)) == {0, 1, 2}


def test_terms_monotone_history_and_stops():
    U = _planted_k3()
    r = solve_terms(U, 3, np.inf, n_restarts=1, random_state=1, max_iter=50)
    assert (np.diff(r.history) <= 1e-12).all() and r.history[-1] == pytest.approx(r.objective)
    assert r.success and r.n_iter < 50  # stopped at a fixed assignment
    assert (np.argmax(U @ r.W.T - r.beta, axis=1) == r.labels).all()
    short = solve_terms(U, 3, np.inf, n_restarts=1, random_state=1, max_iter=1)
    assert short.n_iter == 1 and not short.success  # stopped at max_iter


def test_terms_k1_equals_slsqp_and_degenerate():
    U = np.log(make_frontier_data(80, 3, random_state=0)[0])
    one = solve_terms(U, 1, 20.0)
    ref = solve_slsqp(U, 20.0)
    np.testing.assert_array_equal(one.W[0], ref.w)
    assert one.beta[0] == ref.beta and one.objective == ref.beta and (one.labels == 0).all()
    few = solve_terms(U[:2], 3, 20.0)  # fewer rows than facets: the K=1 fit repeated
    assert few.W.shape == (3, 3)
    single = solve_terms(U[:, :1], 2, 20.0)  # d = 1
    np.testing.assert_array_equal(single.W, [[1.0], [1.0]])


def test_terms_deterministic_and_sparse():
    U = _planted_k3()
    a = solve_terms(U, 3, 50.0, random_state=7)
    b = solve_terms(U, 3, 50.0, random_state=7)
    np.testing.assert_array_equal(a.W, b.W)
    np.testing.assert_array_equal(a.labels, b.labels)
    s = solve_terms(U, 3, 50.0, penalty="reweighted_l1", alpha=0.05, random_state=7)
    assert s.W.shape == (3, 4) and np.allclose(s.W.sum(axis=1), 1.0)


# ------------------------------------------------ WP9 Amendment 1: the facet step
def test_default_facet_step_is_unchanged_literals():
    # stored from the pre-amendment code: the default path must not change (facet order is
    # arbitrary, so the rows are compared sorted)
    X, _ = make_frontier_data(400, 4, n_terms=3, random_state=0)
    r = solve_terms(np.log(X), 3, np.inf, random_state=0)
    assert r.objective == pytest.approx(0.708229464326431, rel=1e-9)
    ref = np.array([[0.54164484, 0.07901886, 0.25635204, 0.12298427],
                    [0.21154331, 0.33382619, 0.24539256, 0.20923794],
                    [0.12557359, 0.23657699, 0.13115001, 0.50669941]])  # fmt: skip
    np.testing.assert_allclose(r.W[np.argsort(r.W[:, 0])], ref[np.argsort(ref[:, 0])], atol=1e-7)
    same = solve_terms(np.log(X), 3, np.inf, random_state=0, facet_step="support")
    np.testing.assert_array_equal(same.W, r.W)


def test_facet_step_validated():
    with pytest.raises(ValueError, match="facet_step"):
        solve_terms(_planted_k3(), 3, 50.0, facet_step="best")


@pytest.mark.parametrize("tau,seed", [(np.inf, 0), (np.inf, 2), (50.0, 0), (50.0, 4)])
def test_tangent_recovers_planted_facets(tau, seed):
    X, info = make_frontier_data(400, 4, n_terms=3, random_state=seed)
    fm, facet = info["frontier_mask"], info["facet"]
    assert np.bincount(facet[fm], minlength=3).min() >= 5  # identifiability: >= d + 1 per facet
    r = solve_terms(np.log(X), 3, tau, random_state=0, facet_step="tangent")
    C = np.abs(r.W[:, None] - info["exponents"][None]).sum(-1)
    rows, cols = linear_sum_assignment(C)
    assert np.abs(r.W[rows] - info["exponents"][cols]).max() < 0.05
    perm = dict(zip(rows, cols, strict=True))
    assert (np.array([perm[k] for k in r.labels]) == facet)[fm].mean() >= 0.9


def test_tangent_keeps_best_iterate_and_is_deterministic():
    U = _planted_k3()
    a = solve_terms(U, 3, 50.0, n_restarts=1, random_state=1, facet_step="tangent")
    b = solve_terms(U, 3, 50.0, n_restarts=1, random_state=1, facet_step="tangent")
    np.testing.assert_array_equal(a.W, b.W)
    assert a.objective == pytest.approx(a.history.min())  # not monotone: the best is returned


def test_tangent_falls_back_to_support_without_enough_near_rows():
    U = _planted_k3(n=12)  # at most a few rows per facet: fewer than d + 1 = 5 near rows
    sup = solve_terms(U, 3, np.inf, random_state=3)
    tan = solve_terms(U, 3, np.inf, random_state=3, facet_step="tangent")
    np.testing.assert_allclose(tan.W, sup.W, atol=1e-9)
    assert tan.objective == pytest.approx(sup.objective, abs=1e-9)  # ties in labels are not tested

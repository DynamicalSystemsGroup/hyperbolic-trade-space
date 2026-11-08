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


# ------------------------------------------------ WP13 (E-1): gap, margin, polish, termination
import warnings  # noqa: E402

from scipy.optimize import linprog  # noqa: E402

from hyperbolic_trade_space import solvers as S  # noqa: E402
from hyperbolic_trade_space.solvers import (  # noqa: E402
    EPS_FEAS,
    EPS_KKT,
    GUARD_TOL,
    POLISH_STEPS,
    Termination,
    assignment_margin,
    facet_gap,
    fixed_assignment_bound,
    simplex_gap,
)

INF = np.inf
_SEEDS = range(20)
_FITS: dict = {}


def _planted_fit(seed, tau):
    """The estimator's call on the planted data, cached for the module."""
    if (seed, tau) not in _FITS:
        U = np.log(make_frontier_data(400, 4, n_terms=3, random_state=seed)[0])
        _FITS[seed, tau] = (U, solve_terms(U, 3, tau, random_state=0))
    return _FITS[seed, tau]


def _facet_optimum(U, ubar, tau, m=0.0):
    """Independent minimizer of f_k(w) = J_tau(Uw) - ubar.w: best of Dirichlet-started SLSQP,
    polished; at tau = inf the LP on the centred rows."""
    Uc = U - ubar
    if np.isinf(tau):
        r = solve_lp(Uc, m)
        return r.w, r.beta
    best = None
    rng = np.random.default_rng(0)
    for w0 in [None, *rng.dirichlet(np.ones(U.shape[1]), size=4)]:
        w = solve_slsqp(Uc, tau, m, w0=w0, tol=1e-15, max_iter=1000).w
        w = S._newton_polish(Uc, w, tau, m)
        f = log_mean_exp(Uc @ w, tau)
        if best is None or f < best[1]:
            best = (w, f)
    return best


def _gap_case(kind, tau=20.0):
    rng = np.random.default_rng(3)
    U = rng.normal(size=(60, 3))
    ubar, m = U.mean(0), 0.0
    if kind in ("boundary", "floor"):
        ubar[2] -= 5.0  # coordinate 2 is penalized: inactive (or at the floor) at the optimum
    if kind == "floor":
        m = 0.1
    return U, ubar, tau, m


def test_simplex_gap_formula():
    g = np.array([0.1, 0.5, 0.9])
    assert simplex_gap(g, np.array([1.0, 0.0, 0.0])) == 0.0  # vertex on the argmin
    assert simplex_gap(g, np.array([0.5, 0.5, 0.0])) == pytest.approx(0.2)
    w = np.array([0.8, 0.1, 0.1])  # floored optimum: m sum(g) + (1 - 3m) min(g) = g.w
    assert simplex_gap(g, w, 0.1) == pytest.approx(0.0, abs=1e-15)
    assert simplex_gap(np.full(3, 0.4), np.array([0.2, 0.3, 0.5])) == pytest.approx(0.0, abs=1e-15)


@pytest.mark.parametrize("kind", ["interior", "boundary", "floor"])
def test_gap_is_zero_at_the_optimum_and_bounds_suboptimality(kind):
    U, ubar, tau, m = _gap_case(kind)
    w, fstar = _facet_optimum(U, ubar, tau, m)
    if kind == "interior":
        assert w.min() > 1e-3
    elif kind == "boundary":
        assert w[2] < 1e-9  # inactive coordinate with g_j > lambda
    else:
        assert w[2] == pytest.approx(m, abs=1e-12)
    assert facet_gap(U, w, ubar, tau, m) < 1e-9
    rng = np.random.default_rng(5)
    d = U.shape[1]
    for v in m + (1 - d * m) * rng.dirichlet(np.ones(d) * 0.7, size=300):
        f = log_mean_exp(U @ v, tau) - ubar @ v
        G = facet_gap(U, v, ubar, tau, m)
        assert f - fstar >= -1e-10 and f - fstar <= G + 1e-10


def test_lp_gap_equals_duality_gap_and_uniform_ties_is_a_valid_bound():
    for seed in range(5):
        U = np.log(make_frontier_data(150, 4, random_state=seed)[0])
        ubar = U.mean(0)
        Uc = U - ubar
        lp = solve_lp(Uc)
        # independent dual: max_p min_j (Uc^T p)_j over the simplex
        n = U.shape[0]
        c = np.zeros(n + 1)
        c[-1] = -1.0
        A = np.hstack([-Uc.T, np.ones((4, 1))])
        res = linprog(
            c, A_ub=A, b_ub=np.zeros(4), A_eq=[[*np.ones(n), 0.0]], b_eq=[1.0],
            bounds=[(0, None)] * n + [(None, None)], method="highs",
        )  # fmt: skip
        dual = -res.fun
        primal = float(np.max(Uc @ lp.w))
        gap = facet_gap(U, lp.w, ubar, INF, p=lp.p)
        assert gap == pytest.approx(primal - dual, abs=1e-12)
        assert facet_gap(U, lp.w, ubar, INF) == pytest.approx(gap, abs=1e-12)  # p from an LP solve
        uniform = facet_gap(U, lp.w, ubar, INF, p=support_weights(U @ lp.w, INF))
        assert uniform >= gap - 1e-12  # valid (weak duality), not tighter than the LP duals
        w = 0.7 * lp.w + 0.3 / 4  # a non-optimal point: the bound still holds
        assert facet_gap(U, w, ubar, INF) >= np.max(Uc @ w) - primal - 1e-12


def test_assignment_margin_values_and_duplicate_facets():
    U = np.array([[0.0, 0.0], [1.0, 0.0], [0.0, 1.0]])
    W = np.array([[1.0, 0.0], [0.0, 1.0]])
    gamma, radius = assignment_margin(U, W, np.zeros(2))
    assert gamma == 0.0 and radius == 0.0  # row 0 ties
    gamma, radius = assignment_margin(U + 0.5 * np.array([1.0, -1.0]) * 0, W, np.array([0.0, 0.4]))
    assert gamma == pytest.approx(0.4) and radius == pytest.approx(0.4 / (2 * np.sqrt(2.0)))
    dup = np.array([[0.3, 0.7], [0.3, 0.7]])  # two identical facets: every row ties
    assert assignment_margin(U, dup, np.zeros(2))[0] == 0.0
    t = S._termination(U, dup, np.zeros(2), np.zeros(3, int), np.full((2, 3), np.nan), INF, 0.0,
                       2, np.array([0.0]), "x", "fixed", True)  # fmt: skip
    assert t.gamma == 0.0 and t.status != "certified" and t.n_empty == 1


@pytest.mark.parametrize("tau", [INF, 50.0])
def test_margin_lemma_perturbations_inside_the_radius_keep_labels(tau):
    rng = np.random.default_rng(11)
    checked = 0
    for seed in _SEEDS:
        U, r = _planted_fit(seed, tau)
        t = r.termination
        if t.gamma <= EPS_FEAS:
            continue
        theta = np.hstack([r.W, r.beta[:, None]])  # (K, d + 1)
        base = np.argmax(U @ r.W.T - r.beta, axis=1)
        U1 = np.hstack([U, -np.ones((U.shape[0], 1))])
        for _ in range(100):
            delta = rng.normal(size=theta.shape)
            delta *= rng.uniform(0.5, 0.999) * t.radius / np.linalg.norm(delta, axis=1)[:, None]
            assert (np.argmax(U1 @ (theta + delta).T, axis=1) == base).all()
        checked += 1
    assert checked == (16 if np.isinf(tau) else 20)


@pytest.mark.parametrize("tau", [INF, 50.0])
def test_corollary_bound_on_every_planted_fit(tau):
    for seed in _SEEDS:
        U, r = _planted_fit(seed, tau)
        t = r.termination
        N = U.shape[0]
        fixed = fstar = 0.0
        for k in range(3):
            rows = r.labels == k
            ubar = U[rows].mean(0)
            _, fk = _facet_optimum(U, ubar, tau)
            fstar += rows.sum() / N * fk
            fixed += rows.sum() / N * (log_mean_exp(U @ r.W[k], tau) - ubar @ r.W[k])
        assert fixed == pytest.approx(r.objective, abs=1e-12)  # the mean slack is F(W)
        assert -1e-11 <= r.objective - fstar <= t.bound + 1e-11
        bound, _, f_fixed = fixed_assignment_bound(U, r.W, r.labels, tau)
        assert f_fixed == pytest.approx(fixed, abs=1e-12)
        assert bound == pytest.approx(t.bound, abs=1e-12)


@pytest.mark.parametrize("tau", [INF, 50.0])
def test_r1_planted_certificates(tau):
    zero_margin = []
    for seed in _SEEDS:
        _, r = _planted_fit(seed, tau)
        t = r.termination
        assert isinstance(t, Termination) and t.assignment_changes == 0 and t.n_empty == 0
        assert t.max_gap <= 1e-12 <= EPS_KKT and t.sum_residual <= EPS_FEAS
        assert t.offset_residual <= 1e-12 and t.floor_residual == 0.0
        assert (t.eps_kkt, t.eps_feas, t.guard_tol) == (EPS_KKT, EPS_FEAS, GUARD_TOL)
        assert t.gaps.shape == (3,) and np.nanmax(t.gaps) == t.max_gap
        if t.gamma > EPS_FEAS:
            assert t.status == "certified" and t.radius > 0
        else:
            assert t.status == "stationary_without_margin"
            zero_margin.append(seed)
        if np.isfinite(tau):
            assert 1e-4 < t.gamma < 1e-2 and 1e-6 < t.radius < 1e-3
    # the spike's seeds 1, 3, 16 plus seed 8, whose chosen restart the guard tolerance now carries on
    assert zero_margin == ([1, 3, 8, 16] if np.isinf(tau) else [])


def test_polish_never_increases_the_facet_objective_and_closes_the_gap():
    U, r = _planted_fit(0, 50.0)
    for k in range(3):
        ubar = U[r.labels == k].mean(0)
        Uc = U - ubar
        w0 = solve_slsqp(Uc, 50.0, tol=1e-10).w
        w1 = S._newton_polish(Uc, w0, 50.0)
        f0, f1 = log_mean_exp(Uc @ w0, 50.0), log_mean_exp(Uc @ w1, 50.0)
        assert f1 <= f0 + 1e-15
        assert facet_gap(U, w0, ubar, 50.0) > 1e-8 > facet_gap(U, w1, ubar, 50.0)
        assert w1.sum() == pytest.approx(1.0) and (w1 >= 0).all()
    assert POLISH_STEPS == 5 and GUARD_TOL == 1e-12


def test_iteration_cap_status():
    U = _planted_k3()
    r = solve_terms(U, 3, INF, n_restarts=1, random_state=1, max_iter=1)
    t = r.termination
    assert t.status == "iteration_cap" and t.n_iter == 1 and t.reason == "max_iter reached"


def test_guard_stop_returns_the_consistent_previous_state(monkeypatch):
    U = _planted_k3()
    real, calls = S._refit, []

    def worse(*args, **kw):
        W, beta, obj, P = real(*args, **kw)
        calls.append(1)
        return (W, beta, obj, P) if len(calls) == 1 else (W, beta, obj + 10.0, P)

    monkeypatch.setattr(S, "_refit", worse)
    r = solve_terms(U, 3, INF, n_restarts=1, random_state=1)
    t = r.termination
    assert t.status == "guard_stop" and len(calls) == 2
    assert r.objective == r.history[-1] == r.history[0] and len(r.history) == 1
    changes = int((np.argmax(U @ r.W.T - r.beta, axis=1) != r.labels).sum())
    assert t.assignment_changes == changes > 0
    # a rejection below the tolerance is accepted, one above is not
    monkeypatch.setattr(S, "_refit", real)
    ok = solve_terms(U, 3, INF, n_restarts=1, random_state=1)
    assert ok.termination.status in ("certified", "stationary_without_margin")


def test_not_applicable_statuses():
    U = _planted_k3()
    assert solve_terms(U, 3, 50.0, facet_step="tangent", random_state=0).termination.status == (
        "not_applicable"
    )
    for kw in ({"penalty": "reweighted_l1", "alpha": 0.05}, {"penalty": "reweighted_l1"}):
        assert solve_terms(U, 3, 50.0, random_state=0, **kw).termination.status == "not_applicable"
    one = solve_terms(U, 1, 20.0)
    ref = solve_slsqp(U, 20.0)
    np.testing.assert_array_equal(one.W[0], ref.w)
    t = one.termination
    assert t.status == "not_applicable" and t.n_iter == one.n_iter and np.isfinite(t.max_gap)
    assert solve_terms(U[:2], 3, 20.0).termination.status == "not_applicable"
    assert solve_terms(U[:, :1], 2, 20.0).termination.status == "not_applicable"


def test_default_path_has_no_warnings_and_constants():
    with warnings.catch_warnings():
        warnings.simplefilter("error")
        solve_terms(_planted_k3(), 3, 50.0, random_state=0)
    assert (EPS_KKT, EPS_FEAS) == (1e-8, 1e-9)

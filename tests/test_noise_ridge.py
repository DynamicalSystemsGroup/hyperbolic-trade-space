"""Planted-data tests for L20: noise on the metrics is a ridge on the exponents.

L20 proves, for symbolic d and n, the ridge identity and the first-order shift
delta = -(P C P)^+ P Sigma w* of the exponents (P the projector of the tangent space of the active
face, C the softmax-weighted covariance at the clean fit). These tests check the statement on
planted frontier data of the spike `work-packages/WP23-rounds/spikes/spike-E-noise/
check2_noise_is_ridge.py` (N = 20000, d = 4, w* = (.4, .3, .2, .1), the data of seed 0 and the
log-normal noise of seed 1), reproduce its numbers, and record where the formula stops holding:
at an exponent on the boundary of the simplex and at a temperature where the noisy fit no longer
follows the ridge. The ridge minimiser is the fit of the clean table with the ridge added; the
noisy fit is the package's fit of the noisy table. Nothing here says the fitted rates are right.
"""

import copy
import importlib

import numpy as np
import pytest
from scipy.optimize import minimize

from derivation.run import run_chain
from hyperbolic_trade_space import HyperbolicTradeSpace
from hyperbolic_trade_space import coordinates as coords
from hyperbolic_trade_space.datasets import make_frontier_data
from hyperbolic_trade_space.solvers import objective_and_grad

W = np.array([0.4, 0.3, 0.2, 0.1])
N = 20000
TAUS = (5.0, 20.0, 50.0)
SIGMAS = (0.05, 0.10, 0.20)
FIRST_ORDER_TOL = 3e-4  # the spike's bound: first-order formula against the ridge minimiser


def minimise(U, tau, ridge=None, w0=None):
    """Minimiser of J_tau on the simplex, with the ridge (tau/2) w'Sigma w added if given."""
    d = U.shape[1]

    def f(w):
        j, g = objective_and_grad(w, U, tau)
        if ridge is not None:
            j = j + tau * 0.5 * w @ ridge @ w
            g = g + tau * ridge @ w
        return j, g

    res = minimize(
        f,
        np.full(d, 1 / d) if w0 is None else w0,
        jac=True,
        method="SLSQP",
        bounds=[(0, 1)] * d,
        constraints=[{"type": "eq", "fun": lambda w: w.sum() - 1}],
        options={"ftol": 1e-14, "maxiter": 500},
    )
    return res.x


def softmax_covariance(U, w, tau):
    z = tau * (U @ w)
    p = np.exp(z - z.max())
    p /= p.sum()
    mu = U.T @ p
    return (U - mu).T @ ((U - mu) * p[:, None])


def first_order(U, w, tau, Sigma, active=None):
    """delta = -(P C P)^+ P Sigma w on the face spanned by `active` (all coordinates if None)."""
    d = len(w)
    a = np.arange(d) if active is None else np.flatnonzero(active)
    C = softmax_covariance(U, w, tau)
    P = np.eye(len(a)) - np.ones((len(a), len(a))) / len(a)
    delta = np.zeros(d)
    delta[a] = -np.linalg.pinv(P @ C[np.ix_(a, a)] @ P) @ P @ Sigma[np.ix_(a, a)] @ w[a]
    return delta


@pytest.fixture(scope="module")
def planted():
    X, _ = make_frontier_data(N, 4, exponents=W, frontier_fraction=0.3, random_state=0)
    return X, np.log(X)


def fit(X, tau):
    return HyperbolicTradeSpace(temperature=tau).fit(X)


def noisy(X, sigma):
    rng = np.random.default_rng(1)
    return X * np.exp(sigma * rng.standard_normal(X.shape))


# ------------------------------------------------------------------------ the lemma itself
@pytest.fixture(scope="module")
def chain():
    ctx, _ = run_chain(verbose=False)
    return ctx


def _reverify(ctx, **changed):
    mod = importlib.import_module("derivation.lemma_20_noise_ridge")
    saved = copy.copy(ctx["L20"])
    ctx["L20"].update(changed)
    try:
        mod.verify(ctx)
    finally:
        ctx["L20"] = saved


def test_L20_statement_says_what_it_claims_and_no_more():
    mod = importlib.import_module("derivation.lemma_20_noise_ridge")
    assert "- (P C P)^+ P Sigma w*" in mod.STATEMENT
    assert "First order only" in mod.STATEMENT and "no bound on the remainder" in mod.STATEMENT
    assert "no statement that the noisy fit" in mod.STATEMENT
    doc = " ".join((mod.__doc__ or "").split())
    assert "does not say each exponent moves toward 1/d" in doc
    assert "anything at an exponent on the boundary" in doc
    assert "that the fitted rates are right" in doc


@pytest.mark.parametrize(
    ("change", "match"),
    [
        ("B_sym_not_symmetric", "L20 FAIL ridge gradient is tau Sigma w"),
        ("pair_matrix_sign", "L20 FAIL pair form is v'C delta"),
        ("range_not_ok", "L20 FAIL pseudoinverse closed form"),
        ("wrong_norm_bound", "L20 FAIL Cauchy-Schwarz chain"),
    ],
)
def test_L20_negative_controls_a_wrong_statement_fails_its_step(chain, change, match):
    r = chain["L20"]
    changes = {
        "B_sym_not_symmetric": {"B_sym": r["B_f"]},
        "pair_matrix_sign": {"pair_matrix": -r["pair_matrix"]},
        "range_not_ok": {"range_ok": False},
        "wrong_norm_bound": {"cs_slack": r["cs_slack"] + r["mc"]},
    }[change]
    with pytest.raises(AssertionError, match=match):
        _reverify(chain, **changes)


# ----------------------------------------- the first-order formula against the ridge minimiser
@pytest.mark.parametrize("tau", TAUS)
@pytest.mark.parametrize("sigma", SIGMAS)
def test_first_order_formula_is_within_3e_4_of_the_ridge_minimiser(planted, sigma, tau):
    """The spike's check 2 (nine cells): w + delta against the minimiser of J + ridge."""
    X, U = planted
    w = fit(X, tau).exponents_[0]
    Sigma = sigma**2 * np.eye(4)
    ridge_min = minimise(U, tau, Sigma, w0=w)
    delta = first_order(U, w, tau, Sigma)
    assert np.abs(w + delta - ridge_min).max() < FIRST_ORDER_TOL


def test_the_clean_fit_of_the_package_is_the_unridged_minimiser(planted):
    """The spike's last column: the package's fit equals the SLSQP minimiser of J_tau."""
    X, U = planted
    for tau in TAUS:
        assert np.abs(fit(X, tau).exponents_[0] - minimise(U, tau)).max() < 1e-4


def test_the_shift_scales_as_sigma_squared(planted):
    """The formula is linear in Sigma; the ridge minimiser's shift follows it (ratio 4 per 2x)."""
    X, U = planted
    tau = 5.0
    w = fit(X, tau).exponents_[0]
    shifts = [np.linalg.norm(first_order(U, w, tau, s**2 * np.eye(4))) for s in SIGMAS]
    assert shifts[1] / shifts[0] == pytest.approx(4.0, rel=1e-9)
    assert shifts[2] / shifts[1] == pytest.approx(4.0, rel=1e-9)
    moved = [np.abs(minimise(U, tau, s**2 * np.eye(4), w0=w) - w).max() for s in SIGMAS]
    assert 3.5 < moved[1] / moved[0] < 4.2 and 3.5 < moved[2] / moved[1] < 4.2


@pytest.mark.parametrize("sigma", (0.10, 0.20))
def test_diagonal_covariance_unequal_levels(planted, sigma):
    """Sigma = diag(sigma_j^2) (the L18 map with unequal measurement errors) obeys the same
    formula, delta = -(P C P)^+ P Sigma w, within the same bound."""
    X, U = planted
    tau = 5.0
    levels = sigma * np.array([0.2, 0.5, 1.0, 0.5])
    Sigma = np.diag(levels**2)
    w = fit(X, tau).exponents_[0]
    ridge_min = minimise(U, tau, Sigma, w0=w)
    delta = first_order(U, w, tau, Sigma)
    assert np.abs(w + delta - ridge_min).max() < FIRST_ORDER_TOL


# ------------------------------------ the noisy fit against the ridge (the fit, not the model)
@pytest.mark.parametrize("sigma", (0.10, 0.20))
def test_the_noisy_fit_tracks_the_ridge_at_small_tau(planted, sigma):
    """At tau = 5 the noisy fit is nearer the ridge minimiser than the clean fit is (spike: 0.0006
    against 0.0020 at sigma = 0.10, 0.0013 against 0.0065 at 0.20)."""
    X, U = planted
    tau = 5.0
    w = fit(X, tau).exponents_[0]
    w_noisy = fit(noisy(X, sigma), tau).exponents_[0]
    ridge_min = minimise(U, tau, sigma**2 * np.eye(4), w0=w)
    noisy_ridge = np.abs(w_noisy - ridge_min).max()
    noisy_clean = np.abs(w_noisy - w).max()
    assert noisy_ridge < 0.5 * noisy_clean and noisy_ridge < 2e-3


def test_the_noisy_fit_no_longer_follows_the_ridge_at_large_tau_and_noise(planted):
    """Recorded limit, not a requirement of the lemma: at tau = 50 and sigma = 0.20 the noisy fit
    is no nearer the ridge minimiser than the clean fit is (spike: 0.0078 against 0.0067). The
    lemma says nothing about a finite noisy table; this is where the surrogate (the logarithm of
    an expectation) stops describing it. The cause is not established here."""
    X, U = planted
    tau, sigma = 50.0, 0.20
    w = fit(X, tau).exponents_[0]
    w_noisy = fit(noisy(X, sigma), tau).exponents_[0]
    ridge_min = minimise(U, tau, sigma**2 * np.eye(4), w0=w)
    assert np.abs(w_noisy - ridge_min).max() >= np.abs(w_noisy - w).max()


# -------------------------------------------------------- the size of the shift and its direction
@pytest.mark.parametrize("sigma", SIGMAS)
def test_the_shift_obeys_the_norm_bound_with_conditioning_and_lowers_the_ridge(planted, sigma):
    """||delta|| <= ||P Sigma w|| / m with m = conditioning_ / tau (L20.48), and delta'Sigma w <=
    -m ||delta||^2 <= 0, so ||w||^2 falls at first order."""
    X, U = planted
    tau = 5.0
    est = fit(X, tau)
    w = est.exponents_[0]
    m = est.conditioning_[0] / tau
    T = coords.helmert_basis(4)
    assert m == pytest.approx(np.linalg.eigvalsh(T @ softmax_covariance(U, w, tau) @ T.T)[0])
    Sigma = sigma**2 * np.eye(4)
    delta = first_order(U, w, tau, Sigma)
    P = np.eye(4) - np.ones((4, 4)) / 4
    y = P @ Sigma @ w
    assert np.linalg.norm(delta) <= np.linalg.norm(y) / m
    assert delta @ Sigma @ w <= -m * np.linalg.norm(delta) ** 2 + 1e-12
    assert delta @ Sigma @ w <= 0 and w @ delta <= 0


def test_the_component_along_the_weakest_direction_is_set_by_the_smallest_eigenvalue(planted):
    """delta = -sum_k (q_k.y / lambda_k) q_k over the tangent eigenvectors: the part along the
    weakest direction is q.y / lambda_min, so a small conditioning_ enlarges it when y has a part
    there (the identity of the pseudoinverse; the lemma gives the bound, this the equality)."""
    X, U = planted
    tau = 5.0
    w = fit(X, tau).exponents_[0]
    Sigma = 0.1**2 * np.eye(4)
    C = softmax_covariance(U, w, tau)
    T = coords.helmert_basis(4)
    vals, vecs = np.linalg.eigh(T @ C @ T.T)
    y = T @ (Sigma @ w)  # P Sigma w in the tangent basis
    delta = first_order(U, w, tau, Sigma)
    assert T @ delta @ vecs[:, 0] == pytest.approx(-(vecs[:, 0] @ y) / vals[0], rel=1e-8)


# ------------------------------------------------------------------- where the formula stops
@pytest.fixture(scope="module")
def boundary_data():
    """Three planted exponents (.5, .3, .2) and a fourth, uninformative metric: the clean fit puts
    the fourth exponent exactly on the boundary of the simplex."""
    X3, _ = make_frontier_data(
        N, 3, exponents=np.array([0.5, 0.3, 0.2]), frontier_fraction=0.3, random_state=0
    )
    z = np.random.default_rng(5).standard_normal((N, 1))
    X4 = np.hstack([X3, np.exp(0.5 * z)])
    return X4, np.log(X4)


def test_at_a_boundary_exponent_the_full_simplex_formula_is_wrong_and_the_face_formula_holds(
    boundary_data,
):
    """w*_4 = 0 and the fit stays there under noise (strict complementarity holds): the projector
    of the full simplex pushes the fourth exponent to 0.014, the constrained ridge minimiser keeps
    it at 0, and the formula on the face of the first three coordinates agrees with it."""
    X, U = boundary_data
    tau, sigma = 5.0, 0.10
    w = fit(X, tau).exponents_[0]
    assert w[3] < 1e-3  # the clean fit is on the boundary
    Sigma = sigma**2 * np.eye(4)
    ridge_min = minimise(U, tau, Sigma, w0=w)
    assert ridge_min[3] < 1e-3  # and so is the minimiser of J + ridge
    full = w + first_order(U, w, tau, Sigma)
    face = w + first_order(U, w, tau, Sigma, active=w > 1e-3)
    assert np.abs(face - ridge_min).max() < FIRST_ORDER_TOL
    assert np.abs(full - ridge_min).max() > 10 * FIRST_ORDER_TOL
    assert full[3] > 0.01  # a spurious exponent where the fit keeps zero


@pytest.mark.parametrize(("tau", "sigma"), [(5.0, 0.20), (20.0, 0.10)])
def test_when_the_noise_overcomes_the_complementarity_margin_neither_formula_holds(
    boundary_data, tau, sigma
):
    """Where the ridge lifts the fourth exponent off zero (the face changes), strict
    complementarity has failed for this noise: the face formula misses the lifted exponent by
    more than the bound, and so does the full-simplex formula."""
    X, U = boundary_data
    w = fit(X, tau).exponents_[0]
    Sigma = sigma**2 * np.eye(4)
    ridge_min = minimise(U, tau, Sigma, w0=w)
    assert ridge_min[3] > 0.01
    face = w + first_order(U, w, tau, Sigma, active=w > 1e-3)
    full = w + first_order(U, w, tau, Sigma)
    assert np.abs(face - ridge_min).max() > 10 * FIRST_ORDER_TOL
    assert np.abs(full - ridge_min).max() > 10 * FIRST_ORDER_TOL

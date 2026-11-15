"""Trade-off report (R-7 link, R-8, R-8a, R-9, R-10, R-11) on planted data built here.

Planted data: a chosen distribution of the tangent vector ``t`` of the frontier hyperplane
(``w.t = 0``) is mapped to chart coordinates ``Z = B t`` and to metrics with
``coordinates.from_frontier_coordinates`` (so ``log V`` is set exactly, 40% of rows on the
frontier, 30% inside the band, 30% far below). ``datasets.py`` is not used or modified.

Stated tolerances (seeds 0, 1, 2; n = 500..600):

* supports at tau = inf: exact set equality, exponents to 1e-6;
* aligned pair: association > +0.5; traded pair: association < -0.5;
* first spread direction within 5 degrees of the planted spread direction;
* the tension matrix and a design's tensions against central finite differences of the fitted
  surface (WP42): relative error below 1e-5 in the metrics and the attributes' units.
"""

import dataclasses

import numpy as np
import pytest
from scipy.optimize import brentq

from hyperbolic_trade_space import (
    HyperbolicTradeSpace,
    LogAffinePreconditioner,
    design_tensions,
    make_frontier_data,
    tension_matrix,
    trade_off_report,
)
from hyperbolic_trade_space.coordinates import (
    from_frontier_coordinates,
    helmert_basis,
)
from hyperbolic_trade_space.gaps import orient_by_pca
from hyperbolic_trade_space.tensions import TradeOffReport

INF = np.inf
BETA = 0.3


def planted(w, n=500, seed=0, sigma=0.5, spread=None, band=0.1):
    """Planted metrics on/under the frontier ``w.u = BETA`` (see module docstring).

    ``spread`` is a list of (tangent vector, std) pairs added to isotropic tangent noise of std
    ``sigma``; returns ``(X, info)``.
    """
    rng = np.random.default_rng(seed)
    w = np.asarray(w, float)
    d = w.size
    e = rng.normal(size=(n, d)) * sigma
    for vec, sd in spread or []:
        e = e + rng.normal(size=(n, 1)) * sd * np.asarray(vec, float)[None, :]
    t = e - np.outer(e @ w, w) / (w @ w)  # project to w.t = 0
    kind = rng.choice(3, size=n, p=[0.4, 0.3, 0.3])
    log_v = np.where(
        kind == 0,
        0.0,
        np.where(kind == 1, -rng.uniform(0, 0.9 * band, n), -rng.uniform(3 * band, 2.0, n)),
    )
    B = helmert_basis(d)
    U = from_frontier_coordinates(t @ B.T, log_v, w, BETA, B)
    return np.exp(U), {"w": w, "t": t, "log_v": log_v, "B": B}


# ------------------------------------------------------------------ R-8a contending set
SUPPORTS = {
    "size2": [0.5, 0.5, 0.0, 0.0, 0.0],
    "size3": [0.5, 0.3, 0.2, 0.0, 0.0],
    "size4_free_metric": [0.3, 0.3, 0.2, 0.2, 0.0],
    "size5": [0.3, 0.25, 0.2, 0.15, 0.1],
}
NAMES = {2: "dilemma", 3: "trilemma", 4: "4-lemma", 5: "5-lemma"}


@pytest.mark.parametrize("case", list(SUPPORTS))
@pytest.mark.parametrize("seed", [0, 1, 2])
def test_contending_set_recovers_planted_support(case, seed):
    w = np.array(SUPPORTS[case])
    X, _ = planted(w, 500, seed)
    est = HyperbolicTradeSpace(temperature=INF).fit(X)
    rep = trade_off_report(est, X)
    support = np.flatnonzero(w > 0)
    assert rep.contending_set.tolist() == support.tolist()
    assert np.allclose(rep.contending_exponents, w[support], atol=1e-6)
    assert rep.n_lemma == support.size and rep.lemma_name == NAMES[support.size]
    assert rep.participating.tolist() == (w > 0).tolist()


@pytest.mark.parametrize("seed", [0, 1, 2])
def test_finite_tau_smooths_weights_and_contending_set_stays_exact(seed):
    w = np.array(SUPPORTS["size3"])
    X, _ = planted(w, 600, seed)
    est = HyperbolicTradeSpace(temperature=5.0).fit(X)
    rep = trade_off_report(est, X)
    # the contending set comes from the tau = inf LP, independent of the working tau
    assert rep.contending_set.tolist() == [0, 1, 2]
    assert rep.n_lemma == 3
    assert np.allclose(rep.contending_exponents, w[:3], atol=1e-6)
    # working-tau weights are smoothed: they differ from the exact LP weights, stay near them,
    # and any weight on the free metrics is weak participation (well below the members' weights)
    diff = np.abs(rep.exponents - w).max()
    assert 1e-3 < diff < 0.05
    assert np.all(rep.exponents[3:] < 0.5 * rep.exponents[:3].min())
    assert rep.exponents.sum() == pytest.approx(1.0)
    # participation at the working tau depends on the threshold; membership at tau = inf does not
    weak = trade_off_report(est, X, threshold=1e-9)
    assert weak.participating.sum() >= 3 and weak.contending_set.tolist() == [0, 1, 2]


def test_monolemma_and_names():
    X = np.exp(np.random.default_rng(0).normal(size=(80, 2)))
    X[:, 0] = np.minimum(X[:, 0], 1.0)  # metric 0 caps: only metric 0 binds
    X[:, 1] = X[:, 1] * 0 + 1e-3 + 1e-4 * np.arange(80)
    est = HyperbolicTradeSpace(temperature=INF).fit(X)
    rep = trade_off_report(est, X, min_near_frontier=2, band=50.0)
    assert rep.lemma_name in {"monolemma", "dilemma"}
    assert rep.n_lemma == rep.contending_set.size


def test_warns_when_min_exponent_positive():
    X, _ = planted(SUPPORTS["size3"], 400, 0)
    est = HyperbolicTradeSpace(temperature=INF, min_exponent=0.05).fit(X)
    with pytest.warns(UserWarning, match="min_exponent"):
        rep = trade_off_report(est, X)
    # the LP reading is still exact because it is recomputed with min_exponent = 0
    assert rep.contending_set.tolist() == [0, 1, 2]


def test_no_warning_when_min_exponent_zero(recwarn):
    X, _ = planted(SUPPORTS["size2"], 400, 0)
    trade_off_report(HyperbolicTradeSpace(temperature=INF).fit(X), X)
    assert not [r for r in recwarn if issubclass(r.category, UserWarning)]


# ------------------------------------------------------------------ R-8 part 1
@pytest.mark.parametrize("seed", [0, 1, 2])
def test_exponents_and_elasticities_consistent(seed):
    w = np.array([0.6, 0.4, 0.0])
    X, _ = planted(w, 400, seed)
    est = HyperbolicTradeSpace(temperature=INF).fit(X)
    rep = trade_off_report(est, X)
    assert np.array_equal(rep.exponents, est.exponents_[0])
    assert rep.participating.tolist() == [True, True, False]
    R = rep.elasticities
    assert R.shape == (3, 3)
    for j in range(3):
        for k in range(3):
            if rep.exponents[j] <= 1e-3:
                assert np.isnan(R[j, k])
            else:
                assert R[j, k] == pytest.approx(-rep.exponents[k] / rep.exponents[j])
    assert R[0, 1] * R[1, 0] == pytest.approx(1.0)  # reciprocal elasticities
    assert np.all(R[~np.isnan(R)] <= 0)


# ------------------------------------------------------------------ R-9 association
ALIGNED, TRADED = (0, 1), (2, 3)
W5 = np.array([0.25, 0.25, 0.2, 0.2, 0.1])
T_ALIGN = np.array([1.0, 1.0, 0.0, 0.0, -5.0])  # w.t = 0; metrics 0 and 1 move together
T_TRADE = np.array([0.0, 0.0, 1.0, -1.0, 0.0])  # w.t = 0; metrics 2 and 3 trade


@pytest.mark.parametrize("kind", ["pearson", "spearman"])
@pytest.mark.parametrize("seed", [0, 1, 2])
def test_association_signs_aligned_and_traded(kind, seed):
    X, _ = planted(W5, 600, seed, sigma=0.1, spread=[(T_ALIGN, 0.4), (T_TRADE, 0.6)])
    est = HyperbolicTradeSpace(temperature=INF).fit(X)
    rep = trade_off_report(est, X, association=kind)
    A = rep.association
    assert A.shape == (5, 5) and np.allclose(A, A.T) and np.allclose(np.diag(A), 1.0)
    assert A[ALIGNED] > 0.5
    assert A[TRADED] < -0.5
    assert "closure" in rep.closure_note.lower() and "negative" in rep.closure_note.lower()


def test_closure_induces_negative_association_without_trade():
    # t varies only in an aligned direction plus its closing counter-move: any two participating
    # metrics that are not moved together show negative association (the closure effect)
    X, _ = planted(W5, 600, 0, sigma=0.03, spread=[(T_ALIGN, 0.5)])
    est = HyperbolicTradeSpace(temperature=INF).fit(X)
    A = trade_off_report(est, X).association
    assert A[0, 4] < -0.9 and A[0, 1] > 0.9


# ------------------------------------------------------------------ R-10 directions
@pytest.mark.parametrize("seed", [0, 1, 2])
def test_first_direction_recovers_planted_spread(seed):
    X, info = planted(W5, 600, seed, sigma=0.05, spread=[(T_TRADE, 1.0)])
    est = HyperbolicTradeSpace(temperature=INF).fit(X)
    rep = trade_off_report(est, X)
    v_true = info["B"] @ T_TRADE
    v_true /= np.linalg.norm(v_true)
    cos = abs(rep.spread_directions[0] @ v_true)
    assert np.degrees(np.arccos(min(cos, 1.0))) < 5.0
    # loadings map back to metrics through the chart basis: proportional to T_TRADE
    load = rep.spread_loadings[0]
    load_true = T_TRADE / np.linalg.norm(T_TRADE)
    assert abs(load @ load_true) > np.cos(np.radians(5.0))
    assert rep.explained_spread[0] > 0.9
    assert rep.explained_spread.sum() == pytest.approx(1.0)
    assert rep.spread_directions.shape == (4, 4) and rep.spread_loadings.shape == (4, 5)
    assert np.allclose(np.linalg.norm(rep.spread_directions, axis=1), 1.0)


def test_orient_by_pca_equals_report_directions():  # R-7
    X, _ = planted(W5, 600, 1, sigma=0.1, spread=[(T_ALIGN, 0.4), (T_TRADE, 0.6)])
    est = HyperbolicTradeSpace(temperature=INF).fit(X)
    rep = trade_off_report(est, X)
    T = est.transform(X)
    near = np.abs(T[:, -1]) < rep.band
    _, comps, evr = orient_by_pca(T[:, :-1], near)
    assert np.allclose(comps, rep.spread_directions)
    assert np.allclose(evr, rep.explained_spread)
    assert near.sum() == rep.n_near_frontier


# ------------------------------------------------------------------ R-11 degenerate input
def test_band_default_and_report_fields():
    X, _ = planted(W5, 500, 0)
    assert trade_off_report(HyperbolicTradeSpace(temperature=INF).fit(X), X).band == 0.1
    assert trade_off_report(HyperbolicTradeSpace(temperature=20.0).fit(X), X).band == 0.05
    assert trade_off_report(HyperbolicTradeSpace(temperature=20.0).fit(X), X, band=0.2).band == 0.2


def test_too_few_near_frontier_raises():
    X, info = planted(W5, 500, 0)
    est = HyperbolicTradeSpace(temperature=INF).fit(X)
    with pytest.raises(ValueError, match="larger band"):
        trade_off_report(est, X[info["log_v"] < -0.3])
    with pytest.raises(ValueError, match="min_near_frontier"):
        trade_off_report(est, X, min_near_frontier=10_000)
    assert trade_off_report(est, X[info["log_v"] < -0.3], band=5.0).n_near_frontier > 10


def test_d1_trivial_report():
    X = np.abs(np.random.default_rng(0).normal(size=(50, 1))) + 0.1
    est = HyperbolicTradeSpace(temperature=INF).fit(X)
    rep = trade_off_report(est, X)
    assert rep.exponents.tolist() == [1.0] and rep.participating.tolist() == [True]
    assert rep.spread_directions.shape == (0, 0) and rep.spread_loadings.shape == (0, 1)
    assert rep.explained_spread.shape == (0,)
    assert rep.n_lemma == 1 and rep.lemma_name == "monolemma"
    assert rep.association.shape == (1, 1)


def test_d2_single_direction():
    X, _ = planted([0.5, 0.5], 400, 0)
    est = HyperbolicTradeSpace(temperature=INF).fit(X)
    rep = trade_off_report(est, X)
    assert rep.spread_directions.shape == (1, 1) and rep.n_lemma == 2
    assert rep.explained_spread.tolist() == [1.0]


def test_deterministic_frozen_and_validation():
    X, _ = planted(W5, 500, 0, spread=[(T_TRADE, 0.5)])
    est = HyperbolicTradeSpace(temperature=INF).fit(X)
    a, b = trade_off_report(est, X), trade_off_report(est, X)
    for f in dataclasses.fields(a):
        va, vb = getattr(a, f.name), getattr(b, f.name)
        assert np.array_equal(va, vb, equal_nan=True) if isinstance(va, np.ndarray) else va == vb
    with pytest.raises(dataclasses.FrozenInstanceError):
        a.band = 1.0
    with pytest.raises(ValueError, match="association"):
        trade_off_report(est, X, association="kendall")
    from sklearn.exceptions import NotFittedError

    with pytest.raises(NotFittedError):
        trade_off_report(HyperbolicTradeSpace(), X)


# ---- K > 1: one report per term (WP9 R-4) -------------------------------------------------
_PLANTED = [[0.5, 0.5, 0, 0], [0, 0.5, 0.5, 0], [0, 0, 0.5, 0.5]]


@pytest.mark.slow
@pytest.mark.parametrize("seed", [0, 1, 2])
def test_k3_reports_one_per_term_recover_planted_supports(seed):
    X, _ = make_frontier_data(1500, 4, exponents=_PLANTED, n_terms=3, random_state=seed)
    est = HyperbolicTradeSpace(n_terms=3, temperature=20.0, random_state=0).fit(X)
    reps = trade_off_report(est, X)
    assert isinstance(reps, list) and len(reps) == 3
    assert all(r.n_near_frontier >= 10 and r.band == 0.05 for r in reps)
    assert all(r.spread_loadings.shape == (3, 4) for r in reps)
    assert sorted(r.contending_set.tolist() for r in reps) == [[0, 1], [1, 2], [2, 3]]


def test_k1_is_a_single_report_and_term_error_names_term():
    X, _ = make_frontier_data(300, 3, random_state=0)
    assert isinstance(
        trade_off_report(HyperbolicTradeSpace(temperature=INF).fit(X), X), TradeOffReport
    )
    X, _ = make_frontier_data(900, 4, exponents=_PLANTED, n_terms=3, random_state=0)
    est = HyperbolicTradeSpace(n_terms=3, temperature=20.0, random_state=0).fit(X)
    with pytest.raises(ValueError, match="term 0"):
        trade_off_report(est, X, min_near_frontier=10**6)


def test_first_report_at_several_terms_names_a_workable_band():
    """WP10 item 21: the default band 1/tau leaves a term with too few rows on this table; the
    message names a band (and the matching temperature) that works."""
    import re

    from hyperbolic_trade_space import make_frontier_data

    X, _ = make_frontier_data(300, 4, n_terms=2, random_state=777)
    est = HyperbolicTradeSpace(n_terms=2, temperature=50.0, random_state=0).fit(X)
    with pytest.raises(ValueError, match="near-frontier rows") as err:
        trade_off_report(est, X)
    msg = str(err.value)
    assert "term" in msg and "larger band" in msg and "temperature=" in msg
    band = float(re.search(r"band=([0-9.e-]+)", msg).group(1))
    # the named band holds min_near_frontier rows on the named term
    k = int(re.search(r"term (\d+)", msg).group(1))
    _, lv = est._coordinates(X)
    mine = est.assign_cells(X) == k
    assert (np.abs(lv[mine & np.isfinite(lv)]) < band).sum() >= 10


# ---- the tension matrix and a design's tensions (WP42) -----------------------------------
# The check treats the fitted estimator as a black box: ``score_samples`` is the level; for a step
# h in the metric i it solves for the metric j that keeps the level, and takes the central slope.
H = 1e-4
FD_TOL = 1e-5  # the spike's largest relative error was 2.7e-6 on 288 cells of the case study


def _level(est, m):
    return float(est.score_samples(np.asarray(m, float)[None])[0])


def _fd_slope(est, m0, i, j):
    """Central finite difference of d m_j / d m_i along the level set through ``m0``; ``None`` if a
    step leaves the term's cell."""
    target, pts = _level(est, m0), []
    for sgn in (+1, -1):
        m = np.array(m0, float)
        m[i] *= 1 + sgn * H

        def f(lj, m=m):
            mm = m.copy()
            mm[j] = np.exp(lj)
            return _level(est, mm) - target

        lj0 = np.log(m0[j])
        lj = brentq(f, lj0 - 0.05, lj0 + 0.05, xtol=1e-14, rtol=1e-14)
        mm = m.copy()
        mm[j] = np.exp(lj)
        pts.append((m[i], mm[j], int(est.assign_cells(mm[None])[0])))
    (xi1, xj1, c1), (xi2, xj2, c2) = pts
    return None if c1 != c2 else (xj1 - xj2) / (xi1 - xi2)


def _check_cells(est, T, m0, rows_term):
    """Every cell of ``T`` (d x d) at ``m0`` against finite differences; returns the count."""
    d = T.shape[0]
    w = est.exponents_[rows_term]
    checked = 0
    for i in range(d):
        for j in range(d):
            if i == j:
                assert np.isnan(T[i, j])
            elif w[j] <= 1e-3:
                assert np.isnan(T[i, j])  # blank, not zero
            elif w[i] <= 1e-3:
                assert T[i, j] == 0.0  # zero
            else:
                fd = _fd_slope(est, m0, i, j)
                if fd is None:
                    continue
                assert T[i, j] < 0
                assert T[i, j] == pytest.approx(fd, rel=FD_TOL)
                checked += 1
    return checked


_W_SPARSE = [[0.5, 0.3, 0.2, 0.0], [0.0, 0.0, 0.5, 0.5]]


@pytest.fixture(scope="module")
def sparse_fits():
    X, _ = make_frontier_data(600, 4, exponents=_W_SPARSE, n_terms=2, random_state=1)
    one = HyperbolicTradeSpace(temperature=20.0).fit(X)
    two = HyperbolicTradeSpace(n_terms=2, temperature=40.0, random_state=0).fit(X)
    return X, one, two


def test_the_tension_matrix_agrees_with_finite_differences_at_k1(sparse_fits):
    X, est, _ = sparse_fits
    T = tension_matrix(est, X)
    assert T.shape == (1, 4, 4)
    U = np.log(X)
    w, tau = est.exponents_[0], float(est.temperature)
    s = U @ w
    p = np.exp(tau * (s - s.max()))
    m_star = np.exp((p / p.sum()) @ U)  # the balanced point
    assert _check_cells(est, T[0], m_star, 0) >= 6


def test_the_tension_matrix_agrees_with_finite_differences_at_k2(sparse_fits):
    X, _, est = sparse_fits
    T = tension_matrix(est, X)
    assert T.shape == (2, 4, 4)
    cells, U, tau = est.assign_cells(X), np.log(X), float(est.temperature)
    checked = 0
    for k in range(2):
        w = est.exponents_[k]
        s = U[cells == k] @ w
        p = np.exp(tau * (s - s.max()))
        m_star = np.exp((p / p.sum()) @ U[cells == k])
        if est.assign_cells(m_star[None])[0] == k:
            checked += _check_cells(est, T[k], m_star, k)
    assert checked >= 4


def test_the_cases_of_the_definition(sparse_fits):
    X, _, est = sparse_fits
    T = tension_matrix(est, X)
    W = est.exponents_
    for k in range(2):
        part = W[k] > 1e-3
        for i in range(4):
            for j in range(4):
                if i == j or not part[j]:
                    assert np.isnan(T[k, i, j])
                elif not part[i]:
                    assert T[k, i, j] == 0.0
                else:
                    assert T[k, i, j] < 0
                    # reciprocal, and the elasticity is the log-log form: constant on the term
                    assert T[k, i, j] * T[k, j, i] == pytest.approx(1.0, rel=1e-12)
    off = ~np.eye(4, dtype=bool)
    assert any(np.isnan(T[k][off]).any() for k in range(2))  # a term with blank cells
    assert any((T[k][off] == 0.0).any() for k in range(2))  # and one with zero cells


def test_a_designs_tensions_agree_with_finite_differences_and_the_level_does_not_matter(
    sparse_fits,
):
    X, _, est = sparse_fits
    dt = design_tensions(est, X)
    assert dt.tensions.shape == (len(X), 4, 4) and dt.by_term.shape == (len(X), 2, 4, 4)
    assert dt.attribute_tensions is None
    assert (dt.term == est.assign_cells(X)).all()
    safe = np.flatnonzero(dt.margin > 0.3)[:3]
    assert len(safe) == 3
    for r in safe:
        assert _check_cells(est, dt.tensions[r], X[r], int(dt.term[r])) >= 1
        # a design scaled to another level has the same tensions (Theorem 1: ratios unchanged)
        scaled = design_tensions(est, X[r : r + 1] * 3.0)
        np.testing.assert_allclose(scaled.tensions[0], dt.tensions[r], rtol=1e-12)
    # the assigned term's matrix is by_term at the term, never merged with the other term's
    own = dt.by_term[np.arange(len(X)), dt.term]
    np.testing.assert_array_equal(own, dt.tensions)
    assert not np.allclose(dt.by_term[safe[0], 0], dt.by_term[safe[0], 1], equal_nan=True)


def test_a_designs_tensions_in_the_attributes_units_agree_with_finite_differences():
    """d s_j / d s_i through the conditioning, against differences of the fitted surface in the
    raw attributes (one orientation: negative; mixed: positive)."""
    rng = np.random.default_rng(0)
    S = rng.uniform(1.0, 5.0, size=(300, 3))
    pre = LogAffinePreconditioner(orientation=[-1, -1, 1], shift=[0.5, 0.0, 0.0]).fit(S)
    M = pre.transform(S)
    est = HyperbolicTradeSpace(temperature=10.0).fit(M)
    dt = design_tensions(est, M, preconditioner=pre, attributes=S)
    TA = dt.attribute_tensions
    assert TA.shape == (300, 3, 3) and np.isnan(TA[:, 0, 0]).all()
    r = 7
    for i, j in [(0, 1), (0, 2), (2, 1)]:
        target = _level(est, M[r])

        def level_at(si, sj, i=i, j=j, target=target):
            s = S[r].copy()
            s[i], s[j] = si, sj
            return _level(est, pre.transform(s[None])[0]) - target

        slopes = []
        for sgn in (+1, -1):
            si = S[r, i] * (1 + sgn * H)
            sj = brentq(lambda v, si=si: level_at(si, v), S[r, j] * 0.5, S[r, j] * 1.5, xtol=1e-14)
            slopes.append((si, sj))
        fd = (slopes[0][1] - slopes[1][1]) / (slopes[0][0] - slopes[1][0])
        assert TA[r, i, j] == pytest.approx(fd, rel=FD_TOL)
    alpha = pre.orientation_ / pre.log_scale_
    # the sign is minus the sign of alpha_i alpha_j
    assert TA[r, 0, 1] < 0 and TA[r, 0, 2] > 0 and np.sign(alpha[0] * alpha[1]) > 0


def test_zero_metric_rows_have_no_tensions_and_validation(sparse_fits):
    X, est1, _ = sparse_fits
    Xz = X[:3].copy()
    Xz[1, 2] = 0.0
    dt = design_tensions(est1, Xz)
    assert dt.term.tolist()[1] == -1 and np.isnan(dt.tensions[1]).all()
    assert not np.isnan(dt.tensions[0, 0, 1]) and np.isinf(dt.margin[0])
    with pytest.raises(ValueError, match="Negative values in data"):
        tension_matrix(est1, -X[:3])
    with pytest.raises(ValueError, match="Negative values in data"):
        design_tensions(est1, -X[:3])
    with pytest.raises(ValueError, match="both preconditioner and attributes"):
        design_tensions(est1, X[:3], attributes=X[:3])
    with pytest.raises(ValueError, match="features"):
        tension_matrix(est1, X[:, :3])
    from sklearn.exceptions import NotFittedError

    with pytest.raises(NotFittedError):
        tension_matrix(HyperbolicTradeSpace(), X)
    with pytest.raises(NotFittedError):
        design_tensions(HyperbolicTradeSpace(), X)

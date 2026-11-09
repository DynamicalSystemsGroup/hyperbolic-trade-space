"""WP17: the several-term fit with soft weights (finite ``term_temperature``).

R-1 descent, R-2 the default is untouched (against values recorded before the change), R-3 the
limit, R-4 the fit serves its model, R-5 recovery at kappa = tau, R-6 analysis stays analysis,
R-7 the second-order certificate (Hessian against finite differences, saddle, certified fits).
"""

import platform
import sys
import warnings
from pathlib import Path

import numpy as np
import pytest
from _env import of_record
from scipy.linalg import eigh
from scipy.optimize import linear_sum_assignment

from hyperbolic_trade_space import HyperbolicTradeSpace, make_frontier_data
from hyperbolic_trade_space import solvers as S

# Slow module: shared fixtures cost minutes (verification in tiers); not in the fast suite.
pytestmark = pytest.mark.slow

REFERENCE = Path(__file__).parent / "data" / "soft_fit_default_reference.npz"
TERM_NUM = (
    "n_iter", "sum_residual", "floor_residual", "offset_residual", "max_gap", "bound",
    "objective_change", "assignment_changes", "n_empty", "gamma", "radius", "eps_kkt",
    "eps_feas", "guard_tol",
)  # fmt: skip
# The reference was recorded on an arm64 Mac: (sys.platform, platform.machine()) below. Exact
# (bit-identical) equality is asserted there and in the environment of record; elsewhere the floats
# agree within 1e-12 (tests/_env.py), and the tau = inf planted fits within the stated tolerances.
RECORDED_ON = ("darwin", "arm64")
EXACT = of_record() or (sys.platform, platform.machine()) == RECORDED_ON
TOL_FIT = 1e-6  # exponents and offsets of the tau = inf planted fits off the recording's platform


def _cases():
    """The fits recorded before the change (planted tables, default ``term_temperature``)."""
    out = {}
    for s in range(6):
        X, _ = make_frontier_data(400, 4, n_terms=3, random_state=s)
        for K in (1, 2, 3):
            for tau in (np.inf, 50.0):
                out[f"planted{s}_K{K}_tau{tau}_support"] = (X, K, tau, "support")
        out[f"planted{s}_K3_tau50.0_tangent"] = (X, 3, 50.0, "tangent")
    X, _ = make_frontier_data(300, 3, n_terms=2, random_state=7)
    out["planted7_K2_tau10.0_support"] = (X, 2, 10.0, "support")
    return out


def _record(est):
    t = est.termination_
    d = {
        "exponents_": est.exponents_, "log_offset_": est.log_offset_,
        "objective_": est.objective_, "mean_slack_": est.mean_slack_, "facet_": est.facet_,
        "support_weights_": est.support_weights_, "n_iter_": est.n_iter_,
        "facet_share_": est.facet_share_, "conditioning_": est.conditioning_,
        "status": t.status, "reason": t.reason, "gaps": t.gaps, "shares": t.shares,
    }  # fmt: skip
    d.update({"term_" + f: getattr(t, f) for f in TERM_NUM})
    return d


def _same(key, got, ref):
    got, ref = np.asarray(got), np.asarray(ref)
    if ref.dtype.kind in "US" or key.split("/")[-1] in ("facet_", "status"):
        assert np.array_equal(got, ref), key
    elif EXACT:
        assert np.array_equal(got, ref, equal_nan=True), key
    elif not key.endswith(("n_iter_", "term_n_iter", "reason")):
        np.testing.assert_allclose(got, ref, rtol=1e-12, atol=1e-12, equal_nan=True, err_msg=key)


@pytest.fixture(scope="module")
def reference():
    return np.load(REFERENCE)


@pytest.mark.parametrize("name", list(_cases()))
def test_r2_default_planted_fits_equal_the_recording(name, reference):
    """The default fit equals the recording: exactly on its platform, within tolerances off it.

    The recording was made on an arm64 Mac (``RECORDED_ON``). The tau = inf fit is a linear
    program whose solution, and the facet assignment built on it, follow the platform's maths
    library, so a bit-identical comparison off that platform (or the environment of record) fails
    on Linux without any change in the method. There, only for tau = inf, the exponents and
    offsets agree within ``TOL_FIT`` and the facet labels may differ only on rows whose two best
    scores tie within ``EPS_FEAS``; every other quantity keeps its comparison above.
    """
    X, K, tau, step = _cases()[name]
    est = HyperbolicTradeSpace(n_terms=K, temperature=tau, facet_step=step, random_state=0).fit(X)
    relaxed = not EXACT and np.isinf(tau)
    for k, v in _record(est).items():
        ref = reference[f"{name}/{k}"]
        if relaxed and k in ("exponents_", "log_offset_", "objective_"):
            np.testing.assert_allclose(v, ref, rtol=0, atol=TOL_FIT, err_msg=f"{name}/{k}")
        elif relaxed and k == "facet_":
            differ = np.asarray(v) != np.asarray(ref)
            if differ.any():
                U = est._log_metrics(X, reset=False)
                top = np.sort(U @ est.exponents_.T - est.log_offset_, axis=1)[:, -2:]
                assert (top[differ, 1] - top[differ, 0] <= S.EPS_FEAS).all(), f"{name}/{k}"
        else:
            _same(f"{name}/{k}", v, ref)


@pytest.mark.slow
@pytest.mark.parametrize("regime", ["primary", "stock"])
def test_r2_default_cubesat_fits_equal_the_recording(regime, reference):
    import case as C

    st = C.load_study(regime)
    for K in (2, 3):
        ft = C.fit_study(st, K=K)
        name = f"cubesat_{regime}_K{K}"
        _same(f"{name}/tau", ft.tau, reference[f"{name}/tau"])
        for k, v in _record(ft.estimator).items():
            _same(f"{name}/{k}", v, reference[f"{name}/{k}"])


def test_r2_the_default_is_the_explicit_infinity_and_leaves_one_term_alone():
    X, _ = make_frontier_data(300, 4, n_terms=3, random_state=2)
    a = HyperbolicTradeSpace(n_terms=3, temperature=50.0, random_state=0).fit(X)
    b = HyperbolicTradeSpace(
        n_terms=3, temperature=50.0, term_temperature=np.inf, random_state=0
    ).fit(X)
    assert np.array_equal(a.exponents_, b.exponents_) and a.termination_.status == "certified"
    assert np.isnan(a.termination_.min_curvature)
    # K = 1: a finite term temperature changes nothing in the fit (nor in any attribute)
    one = HyperbolicTradeSpace(temperature=20.0).fit(X)
    soft = HyperbolicTradeSpace(temperature=20.0, term_temperature=5.0).fit(X)
    for k, v in _record(one).items():
        np.testing.assert_array_equal(_record(soft)[k], v)
    # the tangent step ignores kappa in the fit
    t0 = HyperbolicTradeSpace(n_terms=3, temperature=50.0, facet_step="tangent", random_state=0)
    t1 = HyperbolicTradeSpace(
        n_terms=3, temperature=50.0, facet_step="tangent", term_temperature=50.0, random_state=0
    )
    assert np.array_equal(t0.fit(X).exponents_, t1.fit(X).exponents_)


# ------------------------------------------------------------------------------------ benchmark
TAU = 50.0


def _recovered(est, info):
    """The spike's criterion: error < 0.05 after matching, 90% of frontier rows on their facet."""
    T = np.asarray(info["exponents"])
    r, col = linear_sum_assignment(np.abs(est.exponents_[:, None, :] - T[None]).sum(-1))
    err = float(np.abs(est.exponents_[r] - T[col]).max())
    m = dict(zip(r, col, strict=True))
    lab = np.array([m[k] for k in est.facet_])
    fm = np.asarray(info["frontier_mask"], bool)
    return err < 0.05 and (lab[fm] == np.asarray(info["facet"])[fm]).mean() >= 0.9


@pytest.fixture(scope="module")
def bench():
    """Twenty planted tables, tau = 50: the label fit and the soft fit at kappa = tau."""
    out = []
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        for s in range(20):
            X, info = make_frontier_data(400, 4, n_terms=3, random_state=s)
            kw = {"n_terms": 3, "temperature": TAU, "random_state": 0}
            hard = HyperbolicTradeSpace(**kw).fit(X)
            soft = HyperbolicTradeSpace(term_temperature=TAU, **kw).fit(X)
            out.append((X, info, hard, soft))
    return out


@pytest.mark.slow
def test_r5_recovery_at_kappa_equals_tau_is_no_worse(bench):
    hard = sum(_recovered(h, i) for _, i, h, _ in bench)
    soft = sum(_recovered(s, i) for _, i, _, s in bench)
    assert hard == 16 and soft >= hard


@pytest.mark.slow
def test_r1_the_soft_objective_never_rises_across_the_history(bench):
    for X, _, _, soft in bench:
        r = S.solve_terms(np.log(X), 3, TAU, random_state=0, term_temperature=TAU)
        assert (np.diff(r.history) <= S.GUARD_TOL).all() and r.history.size > 2
        assert r.objective == soft.objective_


def test_r4_the_soft_fit_serves_its_model(bench):
    for X, _, hard, soft in bench:
        U = np.log(X)
        f_soft = S.soft_objective(U, soft.exponents_, soft.log_offset_, TAU)
        f_hard = S.soft_objective(U, hard.exponents_, hard.log_offset_, TAU)
        assert f_soft <= f_hard + 1e-12
        assert soft.mean_slack_ == pytest.approx(f_soft, abs=1e-12)  # the slack of the model
        assert soft.objective_ == pytest.approx(f_soft, abs=1e-12)


def test_r7_the_benchmark_tables_are_certified(bench):
    for _, _, _, soft in bench:
        t = soft.termination_
        assert t.status == "certified", (t.status, t.max_gap, t.min_curvature)
        assert t.max_gap <= S.EPS_KKT and t.min_curvature > S.EPS_FEAS
        assert np.isnan([t.bound, t.gamma, t.radius]).all() and t.assignment_changes == 0
        assert t.shares.sum() == pytest.approx(1.0)


@pytest.mark.slow
def test_r6_analysis_stays_analysis(bench):
    for X, _, _, soft in bench[:6]:
        U = np.log(X)
        np.testing.assert_array_equal(
            soft.facet_, np.argmax(U @ soft.exponents_.T - soft.log_offset_, axis=1)
        )
        assert soft.facet_share_.sum() == pytest.approx(1.0)


@pytest.mark.slow
def test_r3_the_limit_kappa_to_infinity_is_the_label_fit():
    X, _ = make_frontier_data(400, 4, n_terms=3, random_state=4)
    kw = {"n_terms": 3, "temperature": TAU, "random_state": 0}
    hard = HyperbolicTradeSpace(**kw).fit(X)
    gaps = []
    for kappa in (50.0, 500.0, 5000.0):
        soft = HyperbolicTradeSpace(term_temperature=kappa, **kw).fit(X)
        gaps.append(
            np.abs(np.sort(soft.exponents_, axis=0) - np.sort(hard.exponents_, axis=0)).max()
        )
    assert gaps[-1] < 1e-3 and gaps[-1] <= gaps[0]
    soft = HyperbolicTradeSpace(term_temperature=5000.0, **kw).fit(X)
    r, col = linear_sum_assignment(np.abs(soft.exponents_[:, None] - hard.exponents_[None]).sum(-1))
    perm = np.empty(3, int)
    perm[r] = col  # soft facet -> the matching hard facet
    assert (perm[soft.facet_] == hard.facet_).mean() > 0.99


# ------------------------------------------------------------------------------------ certificate
def _hessian_instance():
    X, _ = make_frontier_data(300, 3, n_terms=3, random_state=11)
    U = np.log(X)
    est = HyperbolicTradeSpace(
        n_terms=3, temperature=TAU, term_temperature=TAU, random_state=0
    ).fit(X)
    return U, est.exponents_


def test_r7_gradient_and_hessian_match_finite_differences():
    U, W = _hessian_instance()
    rng = np.random.default_rng(0)
    g, D, M = S.soft_hessian(U, W, TAU, TAU)
    H = D - TAU * M

    def f(W_):
        b = np.array([S.log_mean_exp(U @ w, TAU) for w in W_])
        return S.soft_objective(U, W_, b, TAU)

    h = 1e-6
    for _ in range(10):
        dv = rng.normal(size=W.shape)
        dv -= dv.mean(axis=1, keepdims=True)  # tangent to the simplices
        dv /= np.linalg.norm(dv)
        fd = (f(W + h * dv) - f(W - h * dv)) / (2 * h)
        assert fd == pytest.approx(float(np.sum(g * dv)), abs=1e-8)
        gd = S.soft_hessian(U, W + h * dv, TAU, TAU)[0] - S.soft_hessian(U, W - h * dv, TAU, TAU)[0]
        fdH = gd.ravel() / (2 * h)
        assert np.abs(fdH - H @ dv.ravel()).max() <= 1e-7 * np.abs(H @ dv.ravel()).max()
    # D and M are positive semidefinite (a covariance; a variance over the terms)
    assert eigh(D, eigvals_only=True)[0] > -1e-10 and eigh(M, eigvals_only=True)[0] > -1e-10


def test_r7_all_terms_equal_is_stationary_and_not_certified():
    X, _ = make_frontier_data(400, 4, n_terms=3, random_state=0)
    U = np.log(X)
    Uc = U - U.mean(axis=0)
    one = S._newton_polish(Uc, S.solve_slsqp(Uc, TAU, tol=1e-13).w, TAU, 0.0)
    W = np.tile(one, (3, 1))
    gap, curvature = S.soft_certificate(U, W, TAU, TAU)
    assert gap <= S.EPS_KKT and curvature < -1.0  # stationary, and a saddle
    # the objective falls from it in some feasible direction
    beta = np.array([S.log_mean_exp(U @ w, TAU) for w in W])
    f0 = S.soft_objective(U, W, beta, TAU)
    fit = HyperbolicTradeSpace(
        n_terms=3, temperature=TAU, term_temperature=TAU, random_state=0
    ).fit(X)
    assert S.soft_objective(U, fit.exponents_, fit.log_offset_, TAU) < f0 - 0.1


def test_r7_a_soft_fit_at_infinite_tau_is_not_applicable():
    X, _ = make_frontier_data(300, 4, n_terms=3, random_state=0)
    est = HyperbolicTradeSpace(
        n_terms=3, temperature=np.inf, term_temperature=20.0, random_state=0
    ).fit(X)
    assert est.termination_.status == "not_applicable" and np.isnan(est.termination_.min_curvature)
    assert est.mean_slack_ == pytest.approx(
        S.soft_objective(np.log(X), est.exponents_, est.log_offset_, 20.0), abs=1e-12
    )


def test_r7_a_soft_fit_with_a_penalty_is_not_applicable():
    X, _ = make_frontier_data(300, 4, n_terms=3, random_state=0)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        est = HyperbolicTradeSpace(
            n_terms=3,
            temperature=TAU,
            term_temperature=TAU,
            penalty="reweighted_l1",
            alpha=0.01,
            random_state=0,
        ).fit(X)
    assert est.termination_.status == "not_applicable"


@pytest.mark.slow
@pytest.mark.parametrize("regime", ["primary", "stock"])
def test_r7_the_cubesat_fits_at_kappa_equal_tau_are_certified(regime):
    import case as C

    st = C.load_study(regime)
    for K in (2, 3):
        ft = C.fit_study(st, K=K)
        hard = ft.estimator
        soft = HyperbolicTradeSpace(
            temperature=ft.tau, n_terms=K, term_temperature=ft.tau, random_state=C.CUBESAT.seed
        ).fit(st.M)
        t = soft.termination_
        assert t.status == "certified", (regime, K, t.status, t.max_gap, t.min_curvature)
        assert t.max_gap <= S.EPS_KKT and t.min_curvature > 0.01
        r, col = linear_sum_assignment(
            np.abs(soft.exponents_[:, None] - hard.exponents_[None]).sum(-1)
        )
        assert np.abs(soft.exponents_[r] - hard.exponents_[col]).max() < 0.01  # the spike: 0.003
        for a, b in zip(r, col, strict=True):  # the same contending sets and leading metrics
            sa, sb = soft.exponents_[a], hard.exponents_[b]
            assert set(np.flatnonzero(sa > 0.05)) == set(np.flatnonzero(sb > 0.05))
            assert sa.argmax() == sb.argmax()

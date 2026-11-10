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
# The reference was recorded in the environment of record (linux/arm64 container) and carries its
# platform as the array "recorded_on" = (sys.platform, platform.machine()). Exact (bit-identical)
# equality is asserted there and in the environment of record; elsewhere the floats agree within
# 1e-12 (tests/_env.py), and the tau = inf planted fits within the stated tolerances.
RECORDED_ON = tuple(np.load(REFERENCE)["recorded_on"].tolist())
EXACT = of_record() or (sys.platform, platform.machine()) == RECORDED_ON
RELAXED_SKIP = (
    "status", "reason", "n_iter_", "term_n_iter", "term_objective_change", "support_weights_",
)  # fmt: skip
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
        "objective_": est.objective_, "mean_slack_": est.mean_slack_, "cell_": est.cell_,
        "support_weights_": est.support_weights_, "n_iter_": est.n_iter_,
        "term_share_": est.term_share_, "conditioning_": est.conditioning_,
        "status": t.status, "reason": t.reason, "gaps": t.gaps, "shares": t.shares,
    }  # fmt: skip
    d.update({"term_" + f: getattr(t, f) for f in TERM_NUM})
    return d


def _same(key, got, ref):
    got, ref = np.asarray(got), np.asarray(ref)
    if ref.dtype.kind in "US" or key.split("/")[-1] in ("cell_", "status"):
        assert np.array_equal(got, ref), f"{key}: recorded {_show(ref)} observed {_show(got)}"
    elif EXACT:
        same = np.array_equal(got, ref, equal_nan=True)
        assert same, f"{key} (exact): recorded {_show(ref)} observed {_show(got)}"
    elif not key.endswith(("n_iter_", "term_n_iter", "reason")):
        np.testing.assert_allclose(got, ref, rtol=1e-12, atol=1e-12, equal_nan=True, err_msg=key)


@pytest.fixture(scope="module")
def reference():
    return np.load(REFERENCE)


def _match_to_recording(W, ref_exponents):
    """The recorded term matched to each fitted term, by exponent vector (as the paper does)."""
    r, col = linear_sum_assignment(np.abs(W[:, None, :] - ref_exponents[None]).sum(-1))
    to_ref = np.empty(len(r), int)
    to_ref[r] = col
    return to_ref


@pytest.mark.parametrize("name", list(_cases()))
def test_r2_default_planted_fits_equal_the_recording(name, reference):
    """The default fit equals the recording: exactly on its platform, matched by term off it.

    The recording was made in the linux/arm64 container of record (``RECORDED_ON``). The tau = inf
    fit is a linear program whose solution, and the numbering of the terms it finds, follow the
    platform's maths library: another platform finds the same terms in another order (and then a
    different ``cell_`` array), so a bit-identical comparison there fails without any change in
    the method.
    Off that platform (and outside the environment of record), for tau = inf only, the fitted terms
    are first matched to the recorded ones by exponent vector, as the paper's tables do; then the
    exponents and offsets agree within ``TOL_FIT`` (no wider), the labels agree after the matching
    except on rows whose two best scores tie within ``EPS_FEAS``, and the term-indexed arrays
    follow the matching. The planted table itself differs by rounding between platforms (the maths
    library), and a row on two term planes is then labelled either way. The label-derived arrays
    therefore carry the tolerance that the tie allows and no more: ``term_share_`` (taken from
    ``cell_``) within 0.01 per relabelled row, and the termination ``shares`` (taken from the
    solver's own last labels, which can differ from ``cell_`` on a tied row) within ``1/N`` per
    tied row, plus 1e-12 each. The ``gaps`` stay within 1e-12.
    Cause of the failure this replaces (seed 3, linux/amd64): ``shares`` was compared with the
    ``term_share_`` allowance, which counts the rows relabelled in ``cell_``; the solver's
    labels moved a tied row that ``cell_`` did not, so ``shares`` differed by 1/N = 0.0025
    against an allowance of 1e-12 with no change in the fitted terms. One-ulp perturbations of
    the table reproduce it (25 of 30 on the previous test) and pass with this allowance.
    The quantities of the final steps of a degenerate linear program are not compared off the
    recording's platform; the exact list is ``RELAXED_SKIP``: ``status``, ``reason``, ``n_iter_``,
    ``term_n_iter``, ``term_objective_change`` and ``support_weights_``. They differ between
    platforms while the fitted terms agree (gap G-10). Every other quantity keeps its comparison
    above.
    """
    X, K, tau, step = _cases()[name]
    est = HyperbolicTradeSpace(n_terms=K, temperature=tau, refit_step=step, random_state=0).fit(X)
    _compare_planted(name, est, X, relaxed=not EXACT and np.isinf(tau), reference=reference)


def _show(a):
    return np.array2string(np.asarray(a), precision=17, threshold=60, max_line_width=110)


def _close(key, got, ref, atol, note=""):
    """Assert ``got`` within ``atol`` of ``ref``; the message names the quantity and both values."""
    got, ref = np.asarray(got, float), np.asarray(ref, float)
    if got.shape != ref.shape:
        raise AssertionError(f"{key}{note}: shape {got.shape} observed vs {ref.shape} recorded")
    diff = np.abs(got - ref)
    both_nan = np.isnan(got) & np.isnan(ref)
    bad = ~both_nan & ~(diff <= atol)
    if bad.any():
        raise AssertionError(
            f"{key}{note}: max abs difference {np.nanmax(np.where(both_nan, 0, diff)):.3e} > "
            f"{atol:.1e} at {np.argwhere(bad).tolist()[:10]}\n"
            f"recorded: {_show(ref)}\nobserved: {_show(got)}"
        )


def _compare_planted(name, est, X, relaxed, reference):
    rec = _record(est)
    if relaxed:
        to_ref = _match_to_recording(est.exponents_, reference[f"{name}/exponents_"])
        back = np.argsort(to_ref)  # back[j]: the fitted term matched to recorded term j
        n_relabelled = int((to_ref[est.cell_] != reference[f"{name}/cell_"]).sum())
        U = est._log_metrics(X, reset=False)
        top = np.sort(U @ est.exponents_.T - est.log_offset_, axis=1)[:, -2:]
        if top.shape[1] < 2:  # one term: no row is on two planes
            top = np.full((len(X), 2), np.inf) * np.array([-1.0, 1.0])
        n_tied = int((top[:, 1] - top[:, 0] <= S.EPS_FEAS).sum())  # rows on two term planes
    for k, v in rec.items():
        ref = reference[f"{name}/{k}"]
        if relaxed and k in RELAXED_SKIP:
            continue
        if relaxed and k in ("exponents_", "log_offset_", "term_share_", "shares", "gaps"):
            tol = TOL_FIT if k in ("exponents_", "log_offset_") else 1e-12
            if k == "term_share_":
                tol += 0.01 * n_relabelled
            elif k == "shares":
                tol += n_tied / len(X)
            _close(f"{name}/{k}", np.asarray(v)[back], ref, tol, " (after matching by exponent)")
        elif relaxed and k == "objective_":
            _close(f"{name}/{k}", v, ref, TOL_FIT)
        elif relaxed and k == "cell_":
            differ = to_ref[np.asarray(v)] != np.asarray(ref)
            if differ.any():
                tie = top[differ, 1] - top[differ, 0]
                assert (tie <= S.EPS_FEAS).all(), (
                    f"{name}/{k}: {int(differ.sum())} rows relabelled after matching, rows "
                    f"{np.flatnonzero(differ).tolist()[:20]}; gap of the two best scores "
                    f"{_show(tie)} > EPS_FEAS {S.EPS_FEAS:.1e} on some"
                )
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
    t0 = HyperbolicTradeSpace(n_terms=3, temperature=50.0, refit_step="tangent", random_state=0)
    t1 = HyperbolicTradeSpace(
        n_terms=3, temperature=50.0, refit_step="tangent", term_temperature=50.0, random_state=0
    )
    assert np.array_equal(t0.fit(X).exponents_, t1.fit(X).exponents_)


# ------------------------------------------------------------------------------------ benchmark
TAU = 50.0


def _recovered(est, info):
    """The spike's criterion: error < 0.05 after matching, 90% of frontier rows on their term."""
    T = np.asarray(info["exponents"])
    r, col = linear_sum_assignment(np.abs(est.exponents_[:, None, :] - T[None]).sum(-1))
    err = float(np.abs(est.exponents_[r] - T[col]).max())
    m = dict(zip(r, col, strict=True))
    lab = np.array([m[k] for k in est.cell_])
    fm = np.asarray(info["frontier_mask"], bool)
    return err < 0.05 and (lab[fm] == np.asarray(info["term"])[fm]).mean() >= 0.9


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
            soft.cell_, np.argmax(U @ soft.exponents_.T - soft.log_offset_, axis=1)
        )
        assert soft.term_share_.sum() == pytest.approx(1.0)


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
    perm[r] = col  # soft term -> the matching hard term
    assert (perm[soft.cell_] == hard.cell_).mean() > 0.99


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

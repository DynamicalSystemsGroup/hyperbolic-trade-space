"""Estimator behaviour: recovery, invariants, shape tests, chart, novelty, edges, composition."""

import warnings

import numpy as np
import pandas as pd
import pytest
from sklearn.base import clone
from sklearn.compose import ColumnTransformer
from sklearn.exceptions import ConvergenceWarning
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from hyperbolic_trade_space import HyperbolicTradeSpace, make_frontier_data

INF = np.inf


def planted(n=400, d=3, seed=0, **kw):
    return make_frontier_data(n, d, random_state=seed, **kw)


# ---------------------------------------------------------------- R-7 recovery
@pytest.mark.parametrize("d", [2, 3, 5])
def test_recovery_tau_inf(d):
    X, info = planted(600, d, seed=d)
    est = HyperbolicTradeSpace(temperature=INF).fit(X)
    assert np.abs(est.exponents_[0] - info["exponents"]).max() < 1e-6
    assert abs(est.log_offset_[0] - info["log_offset"]) < 1e-6


@pytest.mark.parametrize("d", [2, 3, 5])
def test_recovery_tau_1e3(d):
    X, info = planted(600, d, seed=d)
    est = HyperbolicTradeSpace(temperature=1e3).fit(X)
    assert np.abs(est.exponents_[0] - info["exponents"]).max() < 2e-2


# ---------------------------------------------------------------- R-8 invariants
@pytest.mark.parametrize("tau", [INF, 10.0, 1e3])
@pytest.mark.parametrize("min_exponent", [0.0, 0.1])
def test_fit_invariants(tau, min_exponent):
    X, _ = planted(300, 4, seed=1, noise=0.05)
    est = HyperbolicTradeSpace(temperature=tau, min_exponent=min_exponent).fit(X)
    w = est.exponents_[0]
    assert est.exponents_.shape == (1, 4) and est.log_offset_.shape == (1,)
    assert abs(w.sum() - 1) < 1e-9 and w.min() >= min_exponent - 1e-12
    p = est.support_weights_
    assert p.min() >= 0 and abs(p.sum() - 1) < 1e-9
    assert 1 <= est.n_eff_ <= X.shape[0]
    V = est.invariant_value(X)
    if np.isinf(tau):
        assert est.frac_above_ == 0 and V.max() <= 1 + 1e-9
    else:
        assert 0 < est.frac_above_ < 0.5
    assert est.objective_ == pytest.approx(est.log_offset_[0])
    assert est.n_iter_ >= 1


# ---------------------------------------------------------------- R-9 shape tests
@pytest.mark.parametrize("tau", [INF, 20.0])
def test_uniform_rescaling_shifts_beta(tau):
    X, _ = planted(200, 3, seed=2, noise=0.05)
    a = HyperbolicTradeSpace(temperature=tau).fit(X)
    b = HyperbolicTradeSpace(temperature=tau).fit(3.0 * X)
    assert b.log_offset_[0] == pytest.approx(a.log_offset_[0] + np.log(3.0), abs=1e-8)
    np.testing.assert_allclose(b.exponents_, a.exponents_, atol=1e-6)
    np.testing.assert_allclose(b.score_samples(3.0 * X), a.score_samples(X), atol=1e-7)


@pytest.mark.parametrize("tau", [INF, 20.0])
def test_row_replication_leaves_fit_unchanged(tau):
    X, _ = planted(150, 3, seed=2, noise=0.05)
    a = HyperbolicTradeSpace(temperature=tau).fit(X)
    b = HyperbolicTradeSpace(temperature=tau).fit(np.vstack([X, X, X]))
    np.testing.assert_allclose(b.exponents_, a.exponents_, atol=1e-6)
    assert b.log_offset_[0] == pytest.approx(a.log_offset_[0], abs=1e-7)


def test_interior_density_insensitive_at_tau_inf_and_large_tau():
    X1, i1 = make_frontier_data(500, 3, exponents=[0.2, 0.3, 0.5], interior_scale=0.3,
                                random_state=4)  # fmt: skip
    # same frontier rows, interior rows replaced by much deeper (sparser near the frontier) ones
    X2, i2 = make_frontier_data(500, 3, exponents=[0.2, 0.3, 0.5], interior_scale=3.0,
                                random_state=4)  # fmt: skip
    assert np.array_equal(i1["frontier_mask"], i2["frontier_mask"])
    a = HyperbolicTradeSpace(temperature=INF).fit(X1)
    b = HyperbolicTradeSpace(temperature=INF).fit(X2)
    np.testing.assert_allclose(a.exponents_, b.exponents_, atol=1e-6)
    c = HyperbolicTradeSpace(temperature=2e3).fit(X1)
    e = HyperbolicTradeSpace(temperature=2e3).fit(X2)
    np.testing.assert_allclose(c.exponents_, e.exponents_, atol=2e-2)


@pytest.mark.parametrize("tau", [INF, 10.0])
def test_permutation_equivariance(tau):
    X, _ = planted(200, 4, seed=3, noise=0.05)
    perm = np.array([2, 0, 3, 1])
    a = HyperbolicTradeSpace(temperature=tau).fit(X)
    b = HyperbolicTradeSpace(temperature=tau).fit(X[:, perm])
    np.testing.assert_allclose(b.exponents_[0], a.exponents_[0][perm], atol=1e-6)
    assert b.log_offset_[0] == pytest.approx(a.log_offset_[0], abs=1e-7)
    rows = np.random.RandomState(0).permutation(X.shape[0])
    c = HyperbolicTradeSpace(temperature=tau).fit(X[rows])
    np.testing.assert_allclose(c.exponents_, a.exponents_, atol=1e-6)


def test_gaussian_noise_offset():
    """beta shifts by about tau sigma^2 ||w||^2 / 2 (lemma L6) for i.i.d. Gaussian log-noise."""
    tau, sigma = 5.0, 0.2
    w = np.array([0.2, 0.3, 0.5])
    X, _ = make_frontier_data(40000, 3, exponents=w, frontier_fraction=1.0, random_state=0)
    rng = np.random.RandomState(1)
    Xn = X * np.exp(sigma * rng.standard_normal(X.shape))
    clean = HyperbolicTradeSpace(temperature=tau).fit(X)
    noisy = HyperbolicTradeSpace(temperature=tau).fit(Xn)
    shift = noisy.log_offset_[0] - clean.log_offset_[0]
    expected = tau * sigma**2 * float(w @ w) / 2
    assert shift == pytest.approx(expected, rel=5e-2)


# ---------------------------------------------------------------- R-10 chart and domain
@pytest.mark.parametrize("coords", ["ilr", "alr"])
@pytest.mark.parametrize("tau", [INF, 10.0])
def test_chart_roundtrip_and_score_samples(coords, tau):
    X, _ = planted(200, 4, seed=5, noise=0.05)
    est = HyperbolicTradeSpace(temperature=tau, coordinates=coords).fit(X)
    T = est.transform(X)
    assert T.shape == X.shape
    np.testing.assert_allclose(est.inverse_transform(T), X, rtol=1e-9)
    np.testing.assert_allclose(T[:, -1], est.score_samples(X))
    np.testing.assert_allclose(est.fit_transform(X), T)


def test_project_and_improvement_factors_land_on_frontier():
    X, _ = planted(100, 4, seed=6, noise=0.05)
    est = HyperbolicTradeSpace(temperature=10.0).fit(X)
    np.testing.assert_allclose(est.invariant_value(est.project(X)), 1.0, atol=1e-9)
    F = est.improvement_factors(X)
    assert F.shape == X.shape
    for j in range(X.shape[1]):
        Y = X.copy()
        Y[:, j] *= F[:, j]
        np.testing.assert_allclose(est.invariant_value(Y), 1.0, atol=1e-9)


def test_improvement_factor_inf_at_zero_exponent():
    X, _ = make_frontier_data(100, 3, exponents=[0.5, 0.5, 0.0], random_state=0)
    est = HyperbolicTradeSpace(temperature=INF).fit(X)
    assert est.exponents_[0, 2] < 1e-6
    est.exponents_[0] = [0.5, 0.5, 0.0]
    assert np.isinf(est.improvement_factors(X)[:, 2]).all()


@pytest.mark.parametrize("coords", ["ilr", "alr"])
def test_level_set(coords):
    X, _ = planted(100, 3, seed=7)
    est = HyperbolicTradeSpace(coordinates=coords).fit(X)
    Z = est.transform(X)[:, :-1]
    for value in (1.0, 0.5, 2.0):
        M = est.level_set(Z, value)
        np.testing.assert_allclose(est.invariant_value(M), value, rtol=1e-9)
        np.testing.assert_allclose(est.transform(M)[:, :-1], Z, atol=1e-9)
    with pytest.raises(ValueError):
        est.level_set(Z, 0.0)
    with pytest.raises(ValueError):
        est.level_set(Z[:, :1])


# ---------------------------------------------------------------- R-11 novelty
def test_novelty_score():
    X, _ = planted(200, 3, seed=8, noise=0.05)
    est = HyperbolicTradeSpace(temperature=10.0).fit(X)
    np.testing.assert_allclose(est.novelty_score(X), est.invariant_value(X) - 1)
    C = est.novelty_score(X, calibrated=True)
    assert C.shape == (200, 2)
    lv = est.score_samples(X)
    np.testing.assert_allclose(C[:, 1], 10.0 * lv)
    expected = np.array([(est.training_log_v_ <= v).mean() for v in lv])
    np.testing.assert_allclose(C[:, 0], expected)
    assert C[:, 0].max() == 1.0
    inf_est = HyperbolicTradeSpace(temperature=INF).fit(X)
    np.testing.assert_allclose(
        inf_est.novelty_score(X, calibrated=True)[:, 1], inf_est.score_samples(X)
    )


def test_leave_one_out_super_efficiency():
    """Removing a frontier point (a support row) and refitting at tau=inf scores it >= 1."""
    X, _ = planted(300, 3, seed=9)
    full = HyperbolicTradeSpace(temperature=INF).fit(X)
    top = np.flatnonzero(full.support_weights_ > 1e-9)
    assert top.size >= 1
    for i in top:
        rest = np.delete(X, i, axis=0)
        refit = HyperbolicTradeSpace(temperature=INF).fit(rest)
        assert refit.invariant_value(X[i : i + 1])[0] >= 1 - 1e-9


# ---------------------------------------------------------------- R-12 edge cases
def test_d1():
    X = np.abs(np.random.RandomState(0).randn(30, 1)) + 0.1
    est = HyperbolicTradeSpace(temperature=INF).fit(X)
    assert est.exponents_.tolist() == [[1.0]]
    assert est.log_offset_[0] == pytest.approx(np.log(X.max()))
    T = est.transform(X)
    assert T.shape == (30, 1)
    np.testing.assert_allclose(est.inverse_transform(T), X)
    assert est.get_feature_names_out().tolist() == ["log_v"]
    assert est.level_set(np.empty((2, 0)), 0.5).shape == (2, 1)
    assert est.basis_.shape == (0, 1)
    fin = HyperbolicTradeSpace(temperature=5.0).fit(X)
    assert fin.log_offset_[0] < np.log(X.max())


def test_single_sample_gives_balanced_exponents():
    with pytest.warns(UserWarning, match="single valid row"):
        est = HyperbolicTradeSpace().fit(np.array([[1.0, 2.0, 3.0]]))
    np.testing.assert_allclose(est.exponents_[0], 1 / 3)
    assert est.score_samples(np.array([[1.0, 2.0, 3.0]]))[0] == pytest.approx(0.0, abs=1e-12)


@pytest.mark.parametrize("tau", [INF, 10.0])
def test_zero_metric_row(tau):
    X, _ = planted(100, 3, seed=10, noise=0.05)
    ref = HyperbolicTradeSpace(temperature=tau).fit(X)
    Xz = np.vstack([X, [0.0, 1.0, 1.0]])
    est = HyperbolicTradeSpace(temperature=tau).fit(Xz)
    np.testing.assert_allclose(est.exponents_, ref.exponents_, atol=1e-9)
    assert est.support_weights_[-1] == 0.0
    assert est.score_samples(Xz)[-1] == -np.inf
    assert est.invariant_value(Xz)[-1] == 0.0
    T = est.transform(Xz)
    assert np.isnan(T[-1, :-1]).all() and T[-1, -1] == -np.inf
    assert np.isnan(est.inverse_transform(T)[-1]).all()
    assert np.isnan(est.project(Xz)[-1]).all()
    assert np.isinf(est.improvement_factors(Xz)[-1]).all()
    assert est.frac_above_ == pytest.approx(ref.frac_above_)
    assert est.training_log_v_[-1] == -np.inf


def test_all_rows_zero_raises():
    with pytest.raises(ValueError, match="zero metric"):
        HyperbolicTradeSpace().fit(np.zeros((4, 2)))


def test_negative_and_nonfinite_raise():
    X, _ = planted(50, 3)
    bad = X.copy()
    bad[0, 0] = -1.0
    with pytest.raises(ValueError, match="Negative values in data"):
        HyperbolicTradeSpace().fit(bad)
    est = HyperbolicTradeSpace().fit(X)
    with pytest.raises(ValueError, match="Negative values in data"):
        est.transform(bad)
    for v in (np.nan, np.inf):
        bad[0, 0] = v
        with pytest.raises(ValueError, match=r"NaN|inf"):
            HyperbolicTradeSpace().fit(bad)


def test_n_terms_above_one_is_implemented():
    # WP9 (R-6): the NotImplementedError of WP2 is gone; the K = 1 path is unchanged
    X, _ = planted(50, 3)
    assert HyperbolicTradeSpace(n_terms=2, random_state=0).fit(X).exponents_.shape == (2, 3)


@pytest.mark.parametrize(
    "params",
    [
        {"temperature": 0.0},
        {"temperature": -1.0},
        {"temperature": np.nan},
        {"min_exponent": -0.1},
        {"min_exponent": 0.5},
        {"coordinates": "clr"},
        {"n_terms": 0},
        {"tol": 0.0},
        {"max_iter": 0},
        {"term_temperature": 0.0},
        {"term_temperature": np.nan},
        {"penalty": "l1"},
        {"alpha": -1.0},
        {"random_state": "a"},
    ],
)
def test_invalid_params_raise_in_fit_not_init(params):
    est = HyperbolicTradeSpace(**params)
    with pytest.raises(ValueError):
        est.fit(planted(30, 3)[0])


def test_width_mismatch_raises():
    X, _ = planted(40, 3)
    est = HyperbolicTradeSpace().fit(X)
    for method in (est.transform, est.score_samples, est.inverse_transform):
        with pytest.raises(ValueError, match="features"):
            method(X[:, :2])


# ---------------------------------------------------------------- R-13 composition
def test_pipeline_and_feature_names():
    X, _ = planted(120, 3, seed=11)
    pipe = Pipeline([("scale", StandardScaler(with_mean=False)), ("hts", HyperbolicTradeSpace())])
    T = pipe.fit_transform(X)
    assert T.shape == (120, 3)
    assert pipe.get_feature_names_out().tolist() == ["ilr0", "ilr1", "log_v"]
    assert clone(pipe).fit(X).transform(X).shape == (120, 3)
    alr = HyperbolicTradeSpace(coordinates="alr").fit(X)
    assert alr.get_feature_names_out().tolist() == ["alr0", "alr1", "log_v"]
    with pytest.raises(ValueError, match="input_features should have length equal"):
        alr.get_feature_names_out(["a", "b"])


def test_column_transformer_passes_metrics_and_covariates():
    X, _ = planted(100, 3, seed=12)
    df = pd.DataFrame(X, columns=["m0", "m1", "m2"])
    df["cat"] = np.arange(100) % 4
    ct = ColumnTransformer(
        [("hts", HyperbolicTradeSpace(), ["m0", "m1", "m2"])], remainder="passthrough"
    )
    out = ct.fit_transform(df)
    assert out.shape == (100, 4)
    np.testing.assert_allclose(out[:, 3], df["cat"])
    names = ct.get_feature_names_out().tolist()
    assert names == ["hts__ilr0", "hts__ilr1", "hts__log_v", "remainder__cat"]
    ct.set_output(transform="pandas")
    assert list(ct.fit_transform(df).columns) == names
    est = ct.named_transformers_["hts"]
    assert est.feature_names_in_.tolist() == ["m0", "m1", "m2"]


def test_improvement_factors_inf_for_numerically_zero_exponent_without_warning():
    est = HyperbolicTradeSpace(temperature=10.0).fit(make_frontier_data(80, 3, random_state=0)[0])
    est.exponents_ = np.array([[0.5, 0.5, 3.4e-17]])  # solver noise on a planted zero
    X = make_frontier_data(20, 3, random_state=1)[0]
    import warnings

    with warnings.catch_warnings():
        warnings.simplefilter("error")
        F = est.improvement_factors(X)
    assert np.isinf(F[:, 2]).all()
    assert np.isfinite(F[:, :2]).all()


# ---------------------------------------------------------------- WP9: K > 1 terms
from scipy.optimize import linear_sum_assignment  # noqa: E402


def _planted_k3(seed=0, tau=np.inf, n=400):
    X, info = make_frontier_data(n, 4, n_terms=3, random_state=seed)
    est = HyperbolicTradeSpace(n_terms=3, temperature=tau, random_state=0).fit(X)
    C = np.abs(est.exponents_[:, None] - info["exponents"][None]).max(-1)
    r, c = linear_sum_assignment(C)
    return X, info, est, C[r, c].max(), dict(zip(r, c, strict=True))


@pytest.mark.parametrize("seed,tau", [(0, np.inf), (2, np.inf), (0, 50.0), (4, 50.0)])
def test_k_terms_recovers_planted_facets(seed, tau):
    X, info, est, err, perm = _planted_k3(seed, tau)
    assert err < 0.05  # exponents recovered after matching facets
    lab = np.array([perm[k] for k in est.facet_])
    fm = info["frontier_mask"]
    assert (lab == info["facet"])[fm].mean() >= 0.9  # frontier rows on the right facet
    if np.isinf(tau):
        # statistic: mean depth -log V of the frontier rows. K = 1 leaves them loose
        # (measured 0.158 to 0.245); K = 3 puts them on V = 1 (0 to 1e-6): a factor > 1e5.
        # At tau = 50 both carry the soft offset, so only recovery is asserted there.
        one = HyperbolicTradeSpace(temperature=tau).fit(X)
        loose1 = -one.score_samples(X)[fm].mean()
        loose3 = -est.score_samples(X)[fm].mean()
        assert loose1 > 0.15 and abs(loose3) < 1e-6


@pytest.mark.slow
@pytest.mark.parametrize("K", [2, 3])
@pytest.mark.parametrize("kappa", [np.inf, 5.0])
def test_k_terms_round_trip_and_scores(K, kappa):
    X, _ = make_frontier_data(150, 4, n_terms=K, random_state=1)
    est = HyperbolicTradeSpace(n_terms=K, term_temperature=kappa, random_state=0).fit(X)
    T = est.transform(X)
    U = np.log(X)
    S = U @ est.exponents_.T - est.log_offset_
    gap = T[:, -1] - S.max(axis=1)
    assert (gap >= -1e-12).all() and (gap <= np.log(K) / kappa + 1e-12).all()
    np.testing.assert_allclose(est.score_samples(X), T[:, -1], atol=1e-12)
    np.testing.assert_allclose(est.inverse_transform(T), X, rtol=1e-8)
    lab = est.assign_facets(X)
    assert lab.min() >= 0 and lab.max() < K
    np.testing.assert_array_equal(lab, est.facet_)
    np.testing.assert_allclose(est.training_log_v_, T[:, -1])
    M = est.level_set(T[:3, :-1], value=0.5)
    np.testing.assert_allclose(est.invariant_value(M), 0.5)
    assert est.basis_.shape == (K, 3, 4) and est.exponents_.shape == (K, 4)


@pytest.mark.slow
def test_k_terms_attributes_conventions():
    X, _ = make_frontier_data(300, 4, n_terms=3, random_state=0)
    for kappa, kf in ((np.inf, 1.0), (4.0, 4.0)):
        est = HyperbolicTradeSpace(n_terms=3, term_temperature=kappa, random_state=0).fit(X)
        np.testing.assert_allclose(est.coefficients_, np.exp(-kf * est.log_offset_))
        assert est.facet_share_.sum() == pytest.approx(1.0)
        assert est.support_weights_.sum() == pytest.approx(1.0)
        assert est.n_eff_ == pytest.approx(1.0 / np.sum(est.support_weights_**2))
        assert est.facet_.shape == (300,) and est.n_iter_ >= 1
        assert 0.0 <= est.frac_above_ <= 1.0
    # K = 1: the same attributes exist (WP10 item 19, recorded in contract version 3)
    k1 = HyperbolicTradeSpace().fit(X)
    assert all(hasattr(k1, a) for a in ("facet_", "coefficients_", "facet_share_", "mean_slack_"))
    far = HyperbolicTradeSpace(n_terms=3, temperature=1000.0, random_state=0).fit(X * 1e3)
    assert far.facet_share_.sum() in (0.0, pytest.approx(1.0))


def test_k_terms_improvement_factors_use_assigned_facet():
    X, _ = make_frontier_data(150, 4, n_terms=3, random_state=0)
    est = HyperbolicTradeSpace(n_terms=3, random_state=0).fit(X)
    x = X[:1].copy()
    j = int(np.argmax(est.exponents_[est.assign_facets(x)[0]]))
    x[0, j] *= est.improvement_factors(x)[0, j]
    assert est.invariant_value(x)[0] == pytest.approx(1.0)


def test_k_terms_zero_rows_and_determinism():
    X, _ = make_frontier_data(120, 3, n_terms=2, random_state=2)
    X[3, 1] = 0.0
    a = HyperbolicTradeSpace(n_terms=2, random_state=7).fit(X)
    b = HyperbolicTradeSpace(n_terms=2, random_state=7).fit(X)
    np.testing.assert_array_equal(a.exponents_, b.exponents_)
    assert a.facet_[3] == -1 and a.assign_facets(X)[3] == -1
    assert a.support_weights_[3] == 0 and np.isneginf(a.score_samples(X)[3])
    assert np.isnan(a.inverse_transform(a.transform(X))[3]).all()


@pytest.mark.parametrize("shape", [(30, 1), (1, 3), (2, 3)])
def test_k_terms_degenerate_inputs_replicate(shape):
    X = np.abs(np.random.default_rng(0).standard_normal(shape)) + 0.5
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", UserWarning)  # the single-row convention warns (tested)
        est = HyperbolicTradeSpace(n_terms=3, random_state=0).fit(X)
    assert est.exponents_.shape == (3, shape[1]) and est.log_offset_.shape == (3,)
    np.testing.assert_allclose(est.inverse_transform(est.transform(X)), X)


def test_penalty_gives_exact_zero_exponents_at_the_estimator():
    # R-11 at the estimator: planted sparse facet d=4, as tests/test_solvers.py
    X, _ = make_frontier_data(300, 4, exponents=[0.6, 0.4, 0, 0], noise=0.1, random_state=0)
    plain = HyperbolicTradeSpace(temperature=20.0).fit(X)
    pen = HyperbolicTradeSpace(temperature=20.0, penalty="reweighted_l1", alpha=0.01).fit(X)
    zero = HyperbolicTradeSpace(temperature=20.0, penalty="reweighted_l1", alpha=0.0).fit(X)
    assert plain.exponents_[0, 2] > 1e-3
    assert (pen.exponents_[0, 2:] == 0.0).all()
    np.testing.assert_allclose(pen.exponents_[0, :2], [0.6, 0.4], atol=0.02)
    np.testing.assert_array_equal(zero.exponents_, plain.exponents_)


# ------------------------------------------- WP9 Amendment 1: facet_step
@pytest.mark.slow
@pytest.mark.parametrize("step", ["support", "tangent"])
@pytest.mark.parametrize("seed,tau", [(0, np.inf), (2, np.inf), (0, 50.0), (4, 50.0)])
def test_k_terms_both_steps_recover_under_identifiability(step, seed, tau):
    # R-1 with the condition: every planted facet has >= d + 1 frontier rows (the generator
    # guarantees it); recovery within 0.05 after matching, >= 90% of frontier rows right
    X, info = make_frontier_data(400, 4, n_terms=3, random_state=seed)
    assert np.bincount(info["facet"][info["frontier_mask"]], minlength=3).min() >= 5
    est = HyperbolicTradeSpace(n_terms=3, temperature=tau, random_state=0, facet_step=step).fit(X)
    C = np.abs(est.exponents_[:, None] - info["exponents"][None]).max(-1)
    r, c = linear_sum_assignment(C)
    assert C[r, c].max() < 0.05
    perm = dict(zip(r, c, strict=True))
    lab = np.array([perm[k] for k in est.facet_])
    assert (lab == info["facet"])[info["frontier_mask"]].mean() >= 0.9


def test_facet_step_validated_and_inert_at_k1():
    X, _ = make_frontier_data(100, 3, random_state=0)
    with pytest.raises(ValueError, match="facet_step"):
        HyperbolicTradeSpace(facet_step="nope").fit(X)
    a = HyperbolicTradeSpace().fit(X)
    b = HyperbolicTradeSpace(facet_step="tangent").fit(X)
    np.testing.assert_array_equal(a.exponents_, b.exponents_)
    assert HyperbolicTradeSpace().get_params()["facet_step"] == "support"


def test_n_restarts_default_and_validation():
    X, _ = make_frontier_data(150, 4, n_terms=3, random_state=0)
    one = HyperbolicTradeSpace(n_terms=3, random_state=0, n_restarts=1).fit(X)
    assert one.exponents_.shape == (3, 4)
    five = HyperbolicTradeSpace(n_terms=3, random_state=0, n_restarts=5).fit(X)
    default = HyperbolicTradeSpace(n_terms=3, random_state=0).fit(X)
    np.testing.assert_array_equal(five.exponents_, default.exponents_)
    for bad in (0, -1, 2.5, None):
        with pytest.raises(ValueError, match="n_restarts"):
            HyperbolicTradeSpace(n_terms=3, n_restarts=bad).fit(X)


# ------------------------------------------------ WP13 (E-1, E-5, E-7): record, warning, limit
from hyperbolic_trade_space import estimator as _est  # noqa: E402
from hyperbolic_trade_space import solvers as _solvers  # noqa: E402


def _k3(seed, tau=INF, **kw):
    X, _ = make_frontier_data(400, 4, n_terms=3, random_state=seed)
    return X, HyperbolicTradeSpace(n_terms=3, temperature=tau, random_state=0, **kw)


def test_constants_are_reexported():
    assert (_est.EPS_KKT, _est.EPS_FEAS, _est.GUARD_TOL, _est.POLISH_STEPS) == (
        1e-8, 1e-9, 1e-12, 5,
    )  # fmt: skip
    assert _est.EPS_ZERO_EXPONENT == 1e-12 and _est.PARTICIPATION_THRESHOLD == 1e-3


@pytest.mark.slow
@pytest.mark.parametrize(
    "seed,tau,status",
    [(0, INF, "certified"), (1, INF, "stationary_without_margin"), (0, 50.0, "certified")],
)
def test_termination_record_for_k_terms(seed, tau, status):
    X, est = _k3(seed, tau)
    with warnings.catch_warnings():
        warnings.simplefilter("error")  # certified and stationary-without-margin do not warn
        est.fit(X)
    t = est.termination_
    ref = _solvers.solve_terms(np.log(X), 3, tau, random_state=0)
    assert t.status == status and t.max_gap <= _est.EPS_KKT and t.assignment_changes == 0
    assert t.n_iter == ref.n_iter and t.gamma == ref.termination.gamma
    assert (t.eps_kkt, t.eps_feas, t.guard_tol) == (1e-8, 1e-9, 1e-12)
    np.testing.assert_array_equal(est.exponents_, ref.W)


def test_termination_not_applicable_cases_do_not_warn():
    X, _ = make_frontier_data(300, 4, n_terms=3, random_state=0)
    d1 = np.abs(np.random.default_rng(0).standard_normal((20, 1))) + 0.5
    cases = [
        (HyperbolicTradeSpace(), X),
        (HyperbolicTradeSpace(temperature=INF), X),
        (HyperbolicTradeSpace(n_terms=3, facet_step="tangent", random_state=0), X),
        (HyperbolicTradeSpace(n_terms=3, penalty="reweighted_l1", alpha=0.01, random_state=0), X),
        (HyperbolicTradeSpace(n_terms=2), d1),
    ]
    for est, data in cases:
        with warnings.catch_warnings():
            warnings.simplefilter("error")
            est.fit(data)
        assert est.termination_.status == "not_applicable"
    # K = 1 gap is read only: the fit is the unchanged single-term fit
    ref = _solvers.solve_slsqp(np.log(X), 10.0, w0=_solvers.solve_lp(np.log(X)).w)
    est = HyperbolicTradeSpace().fit(X)
    np.testing.assert_array_equal(est.exponents_[0], ref.w)
    assert est.log_offset_[0] == ref.beta and np.isfinite(est.termination_.max_gap)


def _one_warning(est, X, pattern):
    with warnings.catch_warnings(record=True) as rec:
        warnings.simplefilter("always")
        est.fit(X)
    cw = [w for w in rec if issubclass(w.category, ConvergenceWarning)]
    assert len(cw) == 1 and pattern in str(cw[0].message), [str(w.message) for w in rec]
    assert "max facet gap" in str(cw[0].message)


def test_convergence_warning_keyed_to_iteration_cap(monkeypatch):
    real = _solvers.solve_terms
    monkeypatch.setattr(_solvers, "solve_terms", lambda *a, **k: real(*a, max_iter=1, **k))
    X, est = _k3(1)
    _one_warning(est, X, "iteration_cap")
    assert est.termination_.status == "iteration_cap"


def test_convergence_warning_keyed_to_guard_stop(monkeypatch):
    real, calls = _solvers._refit, []

    def worse(*args, **kw):
        W, beta, obj, P = real(*args, **kw)
        calls.append(1)
        return (W, beta, obj, P) if len(calls) % 2 else (W, beta, obj + 10.0, P)

    monkeypatch.setattr(_solvers, "_refit", worse)
    X, est = _k3(1, n_restarts=1)
    _one_warning(est, X, "guard_stop")
    assert est.termination_.status == "guard_stop"


def test_conditioning_is_the_restricted_hessian_eigenvalue():
    X, _ = planted(300, 3, seed=2)
    tau = 20.0
    est = HyperbolicTradeSpace(temperature=tau).fit(X)
    cond = est.conditioning_
    assert cond.shape == (1,) and cond[0] > 0
    U = np.log(X)
    p = _solvers.support_weights(U @ est.exponents_[0], tau)
    H = tau * np.cov(U.T, aweights=p, ddof=0)  # Hessian of J_tau: tau * weighted covariance
    B = _coords_helmert(3)
    assert cond[0] == pytest.approx(np.linalg.eigvalsh(B @ H @ B.T).min(), rel=1e-6)
    # read only: the fit is the unchanged one
    ref = _solvers.solve_slsqp(U, tau, w0=_solvers.solve_lp(U).w)
    np.testing.assert_array_equal(est.exponents_[0], ref.w)


def _coords_helmert(d):
    from hyperbolic_trade_space.coordinates import helmert_basis

    return helmert_basis(d)


def test_conditioning_drops_for_nearly_collinear_metrics():
    X, _ = planted(300, 3, seed=2, noise=0.05)
    Xc = X.copy()
    Xc[:, 1] = Xc[:, 0] * np.exp(1e-3 * np.random.default_rng(0).standard_normal(len(X)))
    kw = {"temperature": 20.0, "min_exponent": 0.1}  # the floor keeps every metric participating
    good = HyperbolicTradeSpace(**kw).fit(X).conditioning_[0]
    bad = HyperbolicTradeSpace(**kw).fit(Xc).conditioning_[0]
    assert 0 < bad < 1e-2 * good


def test_conditioning_per_facet_and_nan_cases():
    X, est = _k3(0, 50.0)
    est.fit(X)
    assert est.conditioning_.shape == (3,) and (est.conditioning_ > 0).all()
    assert np.isnan(HyperbolicTradeSpace(temperature=INF).fit(X).conditioning_).all()  # tau = inf
    d1 = np.abs(np.random.default_rng(0).standard_normal((20, 1))) + 0.5
    assert np.isnan(HyperbolicTradeSpace(temperature=5.0).fit(d1).conditioning_).all()
    sparse, _ = make_frontier_data(300, 4, exponents=[0.7, 0.3, 0, 0], noise=0.05, random_state=0)
    one_dim = HyperbolicTradeSpace(temperature=20.0, penalty="reweighted_l1", alpha=0.05)
    assert np.isfinite(one_dim.fit(sparse).conditioning_).all()  # two coordinates participate


def test_zero_metric_with_zero_exponent_equals_the_formal_limit():
    X, _ = make_frontier_data(300, 4, exponents=[0.6, 0.4, 0, 0], noise=0.1, random_state=0)
    est = HyperbolicTradeSpace(temperature=20.0, penalty="reweighted_l1", alpha=0.01).fit(X)
    w = est.exponents_[0]
    assert w[2] <= _est.EPS_ZERO_EXPONENT and w[3] <= _est.EPS_ZERO_EXPONENT
    Xz = X[:20].copy()
    Xz[:10, 2] = 0.0  # zero metric on a zero exponent
    Xz[10:15, 0] = 0.0  # zero metric on a participating exponent
    got = est.score_samples(Xz)
    limit = est.score_samples(np.where(Xz == 0, 1.0, Xz))  # m^0 = 1: the continuous extension
    np.testing.assert_allclose(got[:10], limit[:10], atol=1e-12)
    assert np.isfinite(got[:10]).all()
    assert np.isneginf(got[10:15]).all() and np.isfinite(got[15:]).all()
    T = est.transform(Xz)
    assert np.isnan(T[:15, :-1]).all() and T[:10, -1].tolist() == got[:10].tolist()
    np.testing.assert_allclose(est.invariant_value(Xz)[:10], np.exp(limit[:10]))
    assert np.isnan(est.inverse_transform(T)[:15]).all()


def test_zero_metric_limit_for_k_terms_follows_each_facet():
    W = np.array([[0.5, 0.5, 0.0], [0.0, 0.5, 0.5]])
    est = HyperbolicTradeSpace(n_terms=2)
    est.fit(make_frontier_data(60, 3, n_terms=2, random_state=0)[0])
    est.exponents_, est.log_offset_ = W, np.zeros(2)
    X = np.array([[0.0, 2.0, 3.0], [2.0, 2.0, 0.0], [0.0, 2.0, 0.0], [2.0, 3.0, 4.0]])
    lv = est.score_samples(X)
    assert lv[0] == pytest.approx(0.5 * np.log(6.0))  # only facet 1 has no zero metric
    assert lv[1] == pytest.approx(np.log(2.0))  # only facet 0
    assert np.isneginf(lv[2])  # a zero on a participating exponent of both facets
    assert np.isfinite(lv[3])


def test_degenerate_single_valid_row_warns_with_the_convention():
    X = np.array([[1.0, 2.0, 3.0], [0.0, 1.0, 1.0]])  # one valid row among two
    for k in (1, 3):
        with pytest.warns(UserWarning, match="single valid row.*convention"):
            est = HyperbolicTradeSpace(n_terms=k).fit(X)
        np.testing.assert_allclose(est.exponents_, 1 / 3)
        assert est.termination_.status == "not_applicable"
    assert "single valid row" in HyperbolicTradeSpace.__doc__


def test_attributes_exist_for_every_k_and_k1_numbers_are_unchanged():
    X, _ = make_frontier_data(300, 4, n_terms=2, random_state=777)
    for tau in (np.inf, 50.0):
        e = HyperbolicTradeSpace(temperature=tau).fit(X)
        assert e.facet_.shape == (300,) and not e.facet_.any()
        np.testing.assert_array_equal(e.facet_share_, [1.0])
        np.testing.assert_allclose(e.coefficients_, np.exp(-e.log_offset_))  # kappa = inf -> 1
        assert e.coefficients_.shape == (1,)
    Xz = X.copy()
    Xz[5, 1] = 0.0
    assert HyperbolicTradeSpace().fit(Xz).facet_[5] == -1  # zero metric, as at K > 1
    # the fitted numbers of the K = 1 fit are those of the pre-change code (literals)
    e = HyperbolicTradeSpace(temperature=50.0).fit(X)
    assert e.objective_ == pytest.approx(-0.06947951610557283, rel=1e-12)
    assert e.log_offset_[0] == pytest.approx(e.objective_, rel=1e-12)


def test_mean_slack_is_defined_for_every_k_and_objective_documents_what_was_minimized():
    X, _ = make_frontier_data(300, 4, n_terms=2, random_state=777)
    U = np.log(X)
    # K = 1: beta - mean(w . u); not the soft maximum
    e1 = HyperbolicTradeSpace(temperature=50.0).fit(X)
    expected = e1.log_offset_[0] - np.mean(U @ e1.exponents_[0])
    assert e1.mean_slack_ == pytest.approx(expected, rel=1e-12)
    assert e1.mean_slack_ > 0 and e1.objective_ < e1.mean_slack_
    # K > 1: the mean slack is what the solver minimized
    for tau in (np.inf, 50.0):
        e2 = HyperbolicTradeSpace(n_terms=2, temperature=tau, random_state=0).fit(X)
        k = e2.facet_
        slack = e2.log_offset_[k] - np.einsum("ij,ij->i", e2.exponents_[k], U)
        assert e2.mean_slack_ == pytest.approx(slack.mean(), rel=1e-12)
        assert e2.mean_slack_ == pytest.approx(e2.objective_, rel=1e-9)
    # zero-metric rows are masked
    Xz = X.copy()
    Xz[7, 2] = 0.0
    ez = HyperbolicTradeSpace(temperature=50.0).fit(Xz)
    v = np.log(np.delete(Xz, 7, axis=0))
    assert ez.mean_slack_ == pytest.approx(
        ez.log_offset_[0] - np.mean(v @ ez.exponents_[0]), rel=1e-12
    )
    assert np.isfinite(ez.mean_slack_)


# ---------------------------------------------------------------------------- WP21 D-1
def test_term_aggregation_default_and_params_roundtrip():
    est = HyperbolicTradeSpace()
    assert est.term_aggregation == "sum"
    assert est.get_params()["term_aggregation"] == "sum"
    est2 = HyperbolicTradeSpace(**est.set_params(term_aggregation="mean").get_params())
    assert est2.term_aggregation == "mean"
    HyperbolicTradeSpace(term_aggregation="bad")  # stored verbatim, not validated in __init__


@pytest.mark.parametrize("bad", ["bad", None, 1, "Sum"])
def test_term_aggregation_invalid_raises_in_fit(bad):
    with pytest.raises(ValueError, match="term_aggregation"):
        HyperbolicTradeSpace(term_aggregation=bad).fit(planted(30, 3)[0])


@pytest.mark.slow
@pytest.mark.parametrize(("K", "kappa", "d"), [(2, 5.0, 3), (3, 2.0, 4), (4, 20.0, 5)])
def test_term_aggregation_mean_shifts_score_by_log_k_over_kappa(K, kappa, d):
    X, _ = make_frontier_data(120, d, n_terms=K, random_state=3)
    kw = dict(n_terms=K, term_temperature=kappa, temperature=20.0, random_state=0)
    s = HyperbolicTradeSpace(term_aggregation="sum", **kw).fit(X)
    m = HyperbolicTradeSpace(term_aggregation="mean", **kw).fit(X)
    shift = np.log(K) / kappa
    np.testing.assert_allclose(m.exponents_, s.exponents_, atol=1e-10)
    np.testing.assert_allclose(m.log_offset_, s.log_offset_, atol=1e-10)
    np.testing.assert_allclose(s.score_samples(X) - m.score_samples(X), shift, atol=1e-10)
    np.testing.assert_allclose(m.mean_slack_ - s.mean_slack_, shift, atol=1e-10)
    assert m.termination_.status == s.termination_.status
    np.testing.assert_allclose(m.inverse_transform(m.transform(X)), X, rtol=1e-8)
    S_ = np.log(X) @ m.exponents_.T - m.log_offset_
    gap = m.score_samples(X) - S_.max(axis=1)
    assert (gap <= 1e-12).all() and (gap >= -shift - 1e-12).all()


@pytest.mark.parametrize("params", [{"n_terms": 3, "term_temperature": np.inf}, {"n_terms": 1}])
def test_term_aggregation_mean_equals_sum_at_kappa_inf_or_k1(params):
    X, _ = make_frontier_data(80, 3, n_terms=3, random_state=2)
    kw = dict(random_state=0, **params)
    a = HyperbolicTradeSpace(term_aggregation="sum", **kw).fit(X)
    b = HyperbolicTradeSpace(term_aggregation="mean", **kw).fit(X)
    np.testing.assert_array_equal(a.score_samples(X), b.score_samples(X))
    np.testing.assert_array_equal(a.exponents_, b.exponents_)
    assert a.mean_slack_ == b.mean_slack_


def test_term_aggregation_duplicated_term_shift_is_log2_over_kappa():
    # sum: a repeated term raises Phi by log 2 / kappa where it ties the maximum
    est = HyperbolicTradeSpace(n_terms=2, term_temperature=4.0).fit(planted(40, 3)[0])
    one = est.exponents_[:1], est.log_offset_[:1]
    est.exponents_, est.log_offset_ = np.repeat(one[0], 2, axis=0), np.repeat(one[1], 2)
    est.basis_ = est.basis_[:2]
    U = np.log(planted(40, 3)[0])
    s = U @ est.exponents_.T - est.log_offset_
    sum_phi = est._phi(s)
    est.term_aggregation = "mean"
    np.testing.assert_allclose(sum_phi - est._phi(s), np.log(2) / 4.0, atol=1e-12)
    np.testing.assert_allclose(est._phi(s), s[:, 0], atol=1e-12)

"""Estimator behaviour: recovery, invariants, shape tests, chart, novelty, edges, composition."""

import numpy as np
import pandas as pd
import pytest
from sklearn.base import clone
from sklearn.compose import ColumnTransformer
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


def test_n_terms_not_implemented():
    X, _ = planted(50, 3)
    with pytest.raises(NotImplementedError, match="documented extension"):
        HyperbolicTradeSpace(n_terms=2).fit(X)


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

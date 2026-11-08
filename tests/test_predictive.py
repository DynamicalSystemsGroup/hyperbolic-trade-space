"""TradeSpaceRegressor (spec section 4, WP3 R-12..R-14) on planted configuration data.

Stated tolerances (seeds 0, 1, 2; n = 400 train / 150 held out; GP with fixed RBF kernel):

* tau = inf, noise free: the chart recovers the planted one, so predicted ``Z`` and ``log V`` match
  the planted truth with median absolute error < 1e-3 and 90th percentile < 1e-2, and the
  coordinate-space R^2 on held-out rows is > 0.999.
* tau = 10: held-out frontier configurations are predicted beyond the learned (soft) frontier
  (novelty > 0), configurations with true log V < -0.5 are predicted inside it (novelty < 0).
"""

import numpy as np
import pytest
from sklearn.compose import TransformedTargetRegressor
from sklearn.exceptions import NotFittedError
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import RBF
from sklearn.linear_model import LinearRegression
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import PolynomialFeatures

from hyperbolic_trade_space import (
    HyperbolicTradeSpace,
    TradeSpaceRegressor,
    make_configured_frontier_data,
)

SEEDS = (0, 1, 2)


def gp():
    return GaussianProcessRegressor(RBF(2.0), alpha=1e-8, optimizer=None, normalize_y=True)


def planted(seed, n=550, d=3, k=3):
    C, Y, info = make_configured_frontier_data(n, d, k, random_state=seed)
    return C, Y, info, 400


@pytest.mark.parametrize("seed", SEEDS)
def test_recovers_planted_coordinates(seed):
    C, Y, info, n = planted(seed)
    reg = TradeSpaceRegressor(gp(), HyperbolicTradeSpace(np.inf)).fit(C[:n], Y[:n])
    Z, log_v = reg.predict_coordinates(C[n:])
    Zt, lt = info["config_map"](C[n:])
    assert np.median(np.abs(Z - Zt)) < 1e-3 and np.percentile(np.abs(Z - Zt), 90) < 1e-2
    assert np.median(np.abs(log_v - lt)) < 1e-3 and np.percentile(np.abs(log_v - lt), 90) < 1e-2
    assert reg.score(C[n:], Y[n:]) > 0.999
    # predict is inverse_transform of the predicted coordinates
    np.testing.assert_allclose(
        reg.predict(C[n:]), reg.trade_space_.inverse_transform(np.column_stack([Z, log_v]))
    )


@pytest.mark.parametrize("seed", SEEDS)
def test_novelty_beyond_the_soft_frontier(seed):
    C, Y, info, n = planted(seed)
    reg = TradeSpaceRegressor(gp(), HyperbolicTradeSpace(10.0)).fit(C[:n], Y[:n])
    assert reg.trade_space_.frac_above_ > 0
    nov = reg.predict_novelty(C[n:])
    on = info["frontier_mask"][n:]
    _, lt = info["config_map"](C[n:])
    assert on.any() and (lt < -0.5).any()
    assert nov[on].min() > 0
    assert nov[lt < -0.5].max() < 0
    np.testing.assert_allclose(np.log1p(nov), reg.predict_coordinates(C[n:])[1])


def test_score_is_coordinate_space_r2_and_order_independent():
    C, Y, _, n = planted(0)
    reg = TradeSpaceRegressor(gp(), HyperbolicTradeSpace(np.inf)).fit(C[:n], Y[:n])
    T = reg.trade_space_.transform(Y[n:])
    Z, log_v = reg.predict_coordinates(C[n:])
    P = np.column_stack([Z, log_v])
    r2 = np.mean(1 - ((T - P) ** 2).sum(0) / ((T - T.mean(0)) ** 2).sum(0))
    assert reg.score(C[n:], Y[n:]) == pytest.approx(r2)
    perm = np.random.default_rng(0).permutation(len(C) - n)
    np.testing.assert_allclose(reg.predict(C[n:])[perm], reg.predict(C[n:][perm]))


def test_predict_std_plumbing_with_gaussian_process():
    C, Y, _, n = planted(1)
    reg = TradeSpaceRegressor(gp(), HyperbolicTradeSpace(np.inf)).fit(C[:n], Y[:n])
    s = reg.predict_std(C[n:])
    assert s.shape == (len(C) - n, 3) and np.all(s >= 0) and np.all(np.isfinite(s))
    # far from the data the surrogate is uncertain: std grows
    assert reg.predict_std(10 * C[n : n + 5]).mean() > s.mean()
    # delta method agrees with Monte Carlo through inverse_transform (small s: affine in log)
    X = 3 * C[n : n + 1]
    _, std = reg.regressor_.predict(X, return_std=True)
    mu = reg.regressor_.predict(X)
    draws = mu + np.asarray(std).reshape(1, -1) * np.random.default_rng(0).standard_normal(
        (40000, 3)
    )
    mc = reg.trade_space_.inverse_transform(draws).std(0)
    delta = reg.predict_std(X)[0]
    np.testing.assert_allclose(delta, mc, rtol=0.05)


def test_predict_std_absent_without_return_std():
    C, Y, _, n = planted(0)
    reg = TradeSpaceRegressor(LinearRegression(), HyperbolicTradeSpace()).fit(C[:n], Y[:n])
    assert not hasattr(reg, "predict_std")
    with pytest.raises(AttributeError):
        reg.predict_std(C[:2])


def test_transformed_target_regressor_interoperates():
    C, Y, _, n = planted(0)
    kw = dict(temperature=np.inf)
    reg = TradeSpaceRegressor(LinearRegression(), HyperbolicTradeSpace(**kw)).fit(C[:n], Y[:n])
    ttr = TransformedTargetRegressor(
        regressor=LinearRegression(), transformer=HyperbolicTradeSpace(**kw), check_inverse=False
    ).fit(C[:n], Y[:n])
    np.testing.assert_allclose(ttr.predict(C[n:]), reg.predict(C[n:]), rtol=1e-8)


def test_trade_space_can_be_a_pipeline_and_regressor_a_pipeline():
    C, Y, _, n = planted(0)
    from sklearn.preprocessing import FunctionTransformer

    chart = make_pipeline(FunctionTransformer(validate=False), HyperbolicTradeSpace(np.inf))
    poly = make_pipeline(PolynomialFeatures(2), LinearRegression())
    reg = TradeSpaceRegressor(poly, chart).fit(C[:n], Y[:n])
    assert reg.predict(C[n:]).shape == (len(C) - n, 3)
    assert reg.score(C[n:], Y[n:]) > 0.9


def test_single_metric_accepts_1d_y():
    rng = np.random.default_rng(0)
    X = rng.standard_normal((60, 2))
    y = np.exp(0.5 * X[:, 0] + 0.05 * rng.standard_normal(60))
    reg = TradeSpaceRegressor(LinearRegression(), HyperbolicTradeSpace(np.inf)).fit(X, y)
    assert reg.predict(X).shape == (60,)
    Z, log_v = reg.predict_coordinates(X)
    assert Z.shape == (60, 0) and log_v.shape == (60,)
    reg2 = TradeSpaceRegressor(LinearRegression(), HyperbolicTradeSpace(np.inf)).fit(X, y[:, None])
    np.testing.assert_allclose(reg2.predict(X), reg.predict(X)[:, None])


def test_inputs_validated():
    C, Y, _, n = planted(0)
    reg = TradeSpaceRegressor(LinearRegression(), HyperbolicTradeSpace())
    with pytest.raises(NotFittedError):
        reg.predict(C[:2])
    bad = Y[:n].copy()
    bad[0, 0] = 0.0
    with pytest.raises(ValueError, match="strictly positive"):
        reg.fit(C[:n], bad)
    reg.fit(C[:n], Y[:n])
    with pytest.raises(ValueError, match="features"):
        reg.predict(C[:2, :2])


def test_clones_leave_parameters_untouched():
    C, Y, _, n = planted(0)
    chart, lin = HyperbolicTradeSpace(), LinearRegression()
    reg = TradeSpaceRegressor(lin, chart).fit(C[:n], Y[:n])
    assert reg.trade_space is chart and reg.regressor is lin
    assert not hasattr(chart, "exponents_") and not hasattr(lin, "coef_")
    assert hasattr(reg.trade_space_, "exponents_") and hasattr(reg.regressor_, "coef_")

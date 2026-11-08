"""Preconditioner round trip, unit log-spread, zeros and negatives, pull-back (R-1 to R-3).

Tolerances: round trip 1e-10; unit log-std 1e-10; pull-back versus the pipeline 1e-9; versus the
WP1 L9 chain expression 1e-10. Seeds 0, 1, 2.
"""

import numpy as np
import pandas as pd
import pytest
import sympy as sp
from sklearn.compose import ColumnTransformer
from sklearn.exceptions import NotFittedError
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import MinMaxScaler

from derivation.run import run_chain
from hyperbolic_trade_space import (
    HyperbolicTradeSpace,
    LogAffinePreconditioner,
    frontier_in_original_units,
    make_frontier_data,
)


def attributes(seed, n=80, d=4):
    rng = np.random.RandomState(seed)
    return np.exp(rng.randn(n, d) * np.array([0.5, 1.0, 2.0, 0.3][:d]) + rng.randn(d))


# ---------------------------------------------------------------- R-1 round trip
@pytest.mark.parametrize("seed", [0, 1, 2])
@pytest.mark.parametrize("scaler", ["standard", "robust", None, MinMaxScaler()])
def test_round_trip_mixed_orientation_and_shift(seed, scaler):
    X = attributes(seed)
    pre = LogAffinePreconditioner(
        orientation=[1, -1, -1, 1], shift=[0.0, 0.5, 2.0, 0.1], scaler=scaler
    ).fit(X)
    M = pre.transform(X)
    assert (M > 0).all()
    np.testing.assert_allclose(pre.inverse_transform(M), X, rtol=1e-10, atol=1e-10)


def test_fitted_attributes_and_larger_is_better_direction():
    X = attributes(0)
    pre = LogAffinePreconditioner(orientation=[1, -1, 1, 1], shift=0.25).fit(X)
    for name in ("scaler_", "log_scale_", "log_offset_", "orientation_", "shift_"):
        assert hasattr(pre, name)
    assert pre.log_scale_.shape == pre.log_offset_.shape == (4,)
    np.testing.assert_array_equal(pre.orientation_, [1, -1, 1, 1])
    np.testing.assert_allclose(pre.shift_, 0.25)
    M = pre.transform(X)
    assert np.corrcoef(M[:, 0], X[:, 0])[0, 1] > 0  # larger-is-better
    assert np.corrcoef(M[:, 1], X[:, 1])[0, 1] < 0  # smaller-is-better flips
    # log m = (z - offset)/scale
    z = pre.orientation_ * np.log(X + 0.25)
    np.testing.assert_allclose(np.log(M), (z - pre.log_offset_) / pre.log_scale_, atol=1e-12)


# ---------------------------------------------------------------- R-2 unit spread, errors
@pytest.mark.parametrize("seed", [0, 1, 2])
def test_unit_log_standard_deviation(seed):
    X = attributes(seed)
    M = LogAffinePreconditioner(orientation=[1, -1, 1, -1], shift=0.5).fit_transform(X)
    np.testing.assert_allclose(np.log(M).std(axis=0), 1.0, atol=1e-10)


def test_robust_normalizes_log_iqr_and_ignores_zeros():
    X = attributes(1)
    X[3, 2] = 0.0
    pre = LogAffinePreconditioner(scaler="robust").fit(X)
    with np.errstate(divide="ignore"):
        L = np.log(pre.transform(X))
    keep = np.isfinite(L[:, 2])
    q75, q25 = np.percentile(L[keep, 2], [75, 25])
    assert q75 - q25 == pytest.approx(1.0, abs=1e-10)
    q75, q25 = np.percentile(L[:, 0], [75, 25])
    assert q75 - q25 == pytest.approx(1.0, abs=1e-10)


@pytest.mark.parametrize("orientation", [None, -1])
def test_zeros_map_to_zero_and_invert(orientation):
    X = attributes(0)
    X[2, 1] = 0.0
    pre = LogAffinePreconditioner(orientation=orientation).fit(X)
    M = pre.transform(X)
    assert M[2, 1] == 0.0 and (np.delete(M, [2], axis=0) > 0).all()
    np.testing.assert_allclose(pre.inverse_transform(M), X, rtol=1e-10, atol=1e-12)
    # the fit ignores the zero: same scale as fitting without that entry
    ref = LogAffinePreconditioner(orientation=orientation).fit(X[[i for i in range(80) if i != 2]])
    assert pre.log_scale_[1] == pytest.approx(ref.log_scale_[1])


def test_zero_after_shift_maps_to_zero_and_inverts_to_minus_shift():
    X = np.abs(attributes(2))
    X[0, 0] = -0.5
    pre = LogAffinePreconditioner(shift=0.5).fit(X)
    M = pre.transform(X)
    assert M[0, 0] == 0.0
    assert pre.inverse_transform(M)[0, 0] == -0.5


def test_negative_after_shift_raises():
    X = attributes(0)
    X[0, 0] = -1.0
    with pytest.raises(ValueError, match="Negative values in data"):
        LogAffinePreconditioner().fit(X)
    with pytest.raises(ValueError, match="Negative values in data"):
        LogAffinePreconditioner(shift=0.5).fit(X)  # -0.5 after shift
    LogAffinePreconditioner(shift=1.0).fit(X)  # 0 after shift: allowed
    pre = LogAffinePreconditioner().fit(attributes(0))
    with pytest.raises(ValueError, match="Negative values in data"):
        pre.transform(X)
    with pytest.raises(ValueError, match="Negative values in data"):
        pre.inverse_transform(-np.ones((2, 4)))


@pytest.mark.parametrize(
    "kw",
    [
        {"orientation": [1, 2, 1, 1]},
        {"orientation": [1, 1]},
        {"shift": [1.0, 2.0]},
        {"shift": np.nan},
        {"scaler": "bogus"},
        {"scaler": 3},
    ],
)
def test_parameter_validation_in_fit(kw):
    est = LogAffinePreconditioner(**kw)  # construction never raises
    with pytest.raises(ValueError):
        est.fit(attributes(0))


def test_all_zero_column_is_identity_and_input_width_is_checked():
    X = attributes(0)
    X[:, 1] = 0.0
    pre = LogAffinePreconditioner().fit(X)
    assert pre.log_offset_[1] == 0.0 and pre.log_scale_[1] == 1.0
    assert (pre.transform(X)[:, 1] == 0).all()
    pre = LogAffinePreconditioner().fit(attributes(0))
    with pytest.raises(ValueError, match="features"):
        pre.transform(attributes(0)[:, :3])
    with pytest.raises(ValueError, match="features"):
        pre.inverse_transform(attributes(0)[:, :3])


def test_dataframe_names_and_composition():
    df = pd.DataFrame(attributes(0), columns=["mass", "power", "cost", "gain"])
    pre = LogAffinePreconditioner(orientation=[-1, -1, -1, 1]).set_output(transform="pandas")
    out = pre.fit_transform(df)
    assert list(out.columns) == ["mass", "power", "cost", "gain"]
    ct = ColumnTransformer(
        [("p", LogAffinePreconditioner(orientation=[-1, 1]), ["mass", "gain"])],
        remainder="passthrough",
    )
    assert ct.fit_transform(df).shape == (80, 4)
    pipe = make_pipeline(LogAffinePreconditioner(orientation=-1), HyperbolicTradeSpace())
    assert pipe.fit_transform(df).shape == (80, 4)


# ---------------------------------------------------------------- R-3 pull-back
def pipeline_case(seed, d, tau, scaler, orientation):
    rng = np.random.RandomState(seed)
    M, _ = make_frontier_data(60, d, noise=0.05, random_state=seed)
    shift = rng.uniform(0.0, 1.0, d)
    X = np.exp(np.log(M) * rng.uniform(0.5, 2.0, d)) * 3.0 - shift + 0.3  # positive attributes
    X = np.abs(X)
    pre = LogAffinePreconditioner(orientation=orientation, shift=shift, scaler=scaler).fit(X)
    est = HyperbolicTradeSpace(temperature=tau).fit(pre.transform(X))
    return X, pre, est


@pytest.mark.parametrize("seed", [0, 1, 2])
@pytest.mark.parametrize("scaler", ["standard", "robust", None])
@pytest.mark.parametrize("tau", [4.0, np.inf])
def test_pullback_reproduces_pipeline_score_samples(seed, scaler, tau):
    d = 3
    orientation = [1, -1, 1] if seed % 2 == 0 else [-1, -1, 1]
    X, pre, est = pipeline_case(seed, d, tau, scaler, orientation)
    f = frontier_in_original_units(est, pre)
    assert set(f) == {"exponents_orig", "log_const", "shift"}
    logv = f["log_const"] + np.log(X + f["shift"]) @ f["exponents_orig"]
    np.testing.assert_allclose(logv, est.score_samples(pre.transform(X)), atol=1e-9)
    # smaller-is-better attributes carry negative exponents (A4: alpha_j < 0)
    assert (f["exponents_orig"] * pre.orientation_ >= 0).all()


def test_pullback_zero_attribute_gives_minus_inf_in_both():
    X, pre, est = pipeline_case(0, 3, 4.0, "standard", [1, 1, 1])
    X = X.copy()
    X[0] = -pre.shift_  # X + shift == 0 in every column
    f = frontier_in_original_units(est, pre)
    with np.errstate(divide="ignore"):
        logv = f["log_const"] + np.log(X[:1] + f["shift"]) @ f["exponents_orig"]
    assert logv[0] == -np.inf and est.score_samples(pre.transform(X[:1]))[0] == -np.inf


@pytest.fixture(scope="module")
def ctx():
    return run_chain(verbose=False)[0]


@pytest.mark.parametrize("seed", [0, 1, 2])
def test_pullback_matches_L9_chain_formula(ctx, seed):
    """Cross-check (labelled, not a proof): evaluate the WP1 L9 expression at the fitted values.

    The chain's V_derived is ``exp(sum_j w_j (alpha_j log(a_j + r_j) + b_j - beta0))`` with the
    simplex substituted; its target is ``e^{w.b - beta0} prod_j (a_j + r_j)^{w_j alpha_j}``.
    Here a_j = shift_j, alpha_j = o_j / log_scale_j, b_j = -log_offset_j / log_scale_j, beta0 =
    log_offset_ of the estimator, r_j the raw attribute.
    """
    S, L9 = ctx["S"], ctx["L9"]
    d = 3
    X, pre, est = pipeline_case(seed, d, 4.0, "standard", [1, -1, 1])
    w = est.exponents_[0]
    alpha = pre.orientation_ / pre.log_scale_
    b = -pre.log_offset_ / pre.log_scale_
    beta = est.log_offset_[0]
    row = X[0]
    tables = {
        "w": lambda j: w[int(j) - 1],
        "alpha": lambda j: alpha[int(j) - 1],
        "b": lambda j: b[int(j) - 1],
        "a": lambda j: pre.shift_[int(j) - 1],
        "r": lambda j: row[int(j) - 1],
    }

    def ev(expr):
        e = expr.subs({S.d: d, L9["beta0"]: beta}).doit()
        e = e.replace(
            lambda x: isinstance(x, sp.Indexed) and str(x.base) in tables,
            lambda x: sp.Float(tables[str(x.base)](*x.indices), 30),
        )
        return float(sp.N(e.doit(), 30))

    f = frontier_in_original_units(est, pre)
    v_chain = ev(L9["target"])
    v_pull = np.exp(f["log_const"] + np.log(row + f["shift"]) @ f["exponents_orig"])
    assert v_pull == pytest.approx(v_chain, rel=1e-10)
    # and with the pipeline's V
    v_pipe = est.invariant_value(pre.transform(row[None, :]))[0]
    assert v_pull == pytest.approx(v_pipe, rel=1e-9)
    assert ev(L9["V_derived"]) == pytest.approx(v_chain, rel=1e-10)
    # negative control: a perturbed exponent breaks agreement
    bad = np.exp(f["log_const"] + np.log(row + f["shift"]) @ (f["exponents_orig"] * 1.001))
    assert abs(bad / v_chain - 1) > 1e-6


def test_pullback_errors():
    X, pre, _ = pipeline_case(0, 3, 4.0, "standard", None)
    with pytest.raises(ValueError, match="attributes"):
        frontier_in_original_units(HyperbolicTradeSpace().fit(pre.transform(X)[:, :2]), pre)
    with pytest.raises(NotFittedError):
        frontier_in_original_units(HyperbolicTradeSpace(), pre)

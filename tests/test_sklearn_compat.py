"""scikit-learn conformance (spec section 7, docs/superpowers/notes/sklearn-conformance.md)."""

import inspect

import numpy as np
from sklearn.utils.estimator_checks import parametrize_with_checks

from hyperbolic_trade_space import HyperbolicTradeSpace, make_frontier_data

# Bare check name -> written reason. The goal is an empty dict.
EXPECTED_FAILURES: dict[str, str] = {}


@parametrize_with_checks(
    [
        HyperbolicTradeSpace(),
        HyperbolicTradeSpace(temperature=np.inf),
        HyperbolicTradeSpace(coordinates="alr"),
        HyperbolicTradeSpace(n_terms=3),  # WP9 (R-5): the same expected failures (none)
        HyperbolicTradeSpace(n_terms=3, temperature=np.inf, term_temperature=5.0),
        HyperbolicTradeSpace(n_terms=3, temperature=20.0, term_temperature=20.0),  # WP17: soft fit
        HyperbolicTradeSpace(n_terms=3, refit_step="tangent"),  # Amendment 1: same (empty) failures
    ],
    expected_failed_checks=lambda est: EXPECTED_FAILURES,
    xfail_strict=True,
)
def test_sklearn_compatible_estimator(estimator, check):
    check(estimator)


def test_expected_failures_have_reasons():
    assert all(isinstance(r, str) and r.strip() for r in EXPECTED_FAILURES.values())


def test_no_predict_decision_function_or_score():
    for name in ("predict", "decision_function", "score", "predict_proba"):
        assert not hasattr(HyperbolicTradeSpace, name)
    for name in (
        "score_samples",
        "transform",
        "inverse_transform",
        "fit_transform",
        "get_feature_names_out",
    ):
        assert hasattr(HyperbolicTradeSpace, name)


def test_tags_only_through_sklearn_tags():
    assert not hasattr(HyperbolicTradeSpace, "_more_tags")
    assert not hasattr(HyperbolicTradeSpace, "_get_tags")
    tags = HyperbolicTradeSpace().__sklearn_tags__()
    assert tags.input_tags.positive_only is True
    assert tags.input_tags.sparse is False


def test_init_stores_parameters_verbatim():
    params = inspect.signature(HyperbolicTradeSpace.__init__).parameters
    odd = {name: object() for name in params if name != "self"}
    est = HyperbolicTradeSpace(**odd)
    for name, value in odd.items():
        assert getattr(est, name) is value
    assert est.get_params() == odd


def test_fitted_attributes_end_in_underscore_and_n_iter_positive():
    for tau in (np.inf, 10.0):
        X, _ = make_frontier_data(80, 3, random_state=0)
        before = set(vars(HyperbolicTradeSpace(temperature=tau)))
        est = HyperbolicTradeSpace(temperature=tau).fit(X)
        new = set(vars(est)) - before
        assert new and all(n.endswith("_") for n in new)
        assert est.n_iter_ >= 1


# --- WP3 preconditioner ---
from hyperbolic_trade_space import LogAffinePreconditioner  # noqa: E402

PRECONDITIONER_EXPECTED_FAILURES: dict[str, str] = {}


# A per-column orientation list fixes the width, but the checks fit several widths, so the
# oriented instances use the scalar form (-1 for every column) and a shift/scaler variant.
@parametrize_with_checks(
    [
        LogAffinePreconditioner(),
        LogAffinePreconditioner(orientation=-1),
        LogAffinePreconditioner(orientation=-1, shift=0.5, scaler="robust"),
        LogAffinePreconditioner(scaler=None),
    ],
    expected_failed_checks=lambda est: PRECONDITIONER_EXPECTED_FAILURES,
    xfail_strict=True,
)
def test_sklearn_compatible_preconditioner(estimator, check):
    check(estimator)


def test_preconditioner_expected_failures_have_reasons():
    assert all(isinstance(r, str) and r.strip() for r in PRECONDITIONER_EXPECTED_FAILURES.values())


def test_preconditioner_conformance_surface():
    assert not hasattr(LogAffinePreconditioner, "_more_tags")
    for name in ("predict", "decision_function", "score_samples"):
        assert not hasattr(LogAffinePreconditioner, name)
    tags = LogAffinePreconditioner().__sklearn_tags__()
    assert tags.input_tags.positive_only is True and tags.input_tags.sparse is False
    params = inspect.signature(LogAffinePreconditioner.__init__).parameters
    odd = {name: object() for name in params if name != "self"}
    est = LogAffinePreconditioner(**odd)
    assert est.get_params() == odd and all(getattr(est, k) is v for k, v in odd.items())


# --- WP3 regressor ---
from sklearn.linear_model import LinearRegression  # noqa: E402

from hyperbolic_trade_space import TradeSpaceRegressor  # noqa: E402

# Bare check name -> written reason. The goal is an empty dict.
REGRESSOR_EXPECTED_FAILURES: dict[str, str] = {
    "check_regressor_multioutput": (
        "scikit-learn 1.9.1 builds y with make_regression (negative values) and never applies "
        "_enforce_estimator_tags_y here, ignoring target_tags.positive_only=True that the other "
        "regressor checks honour. Metrics are log-transformed by the chart, so negative y must "
        "raise ValueError; multi-output fit/predict shapes are covered by tests/test_predictive.py "
        "(d=3 and d=1)."
    ),
}


@parametrize_with_checks(
    [TradeSpaceRegressor(LinearRegression(), HyperbolicTradeSpace())],
    expected_failed_checks=lambda est: REGRESSOR_EXPECTED_FAILURES,
    xfail_strict=True,
)
def test_sklearn_compatible_trade_space_regressor(estimator, check):
    check(estimator)


def test_regressor_expected_failures_have_reasons():
    assert all(isinstance(r, str) and r.strip() for r in REGRESSOR_EXPECTED_FAILURES.values())


def test_regressor_tags():
    tags = TradeSpaceRegressor(LinearRegression(), HyperbolicTradeSpace()).__sklearn_tags__()
    assert tags.target_tags.positive_only is True
    assert tags.target_tags.multi_output is True
    assert tags.estimator_type == "regressor"


# --- end WP3 regressor ---

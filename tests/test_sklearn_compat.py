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

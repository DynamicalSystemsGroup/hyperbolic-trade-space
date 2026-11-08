# Note: scikit-learn conformance rules (WP2, WP3)

Verified 2026-11-07 against scikit-learn 1.9.1 documentation and the `main` branch source
(https://scikit-learn.org/stable/developers/develop.html, the glossary,
`sklearn/utils/estimator_checks.py`, `sklearn/utils/_tags.py`, `sklearn/base.py`). The supervisor
will check conformance; reviewers run these as acceptance checks.

## Versions

- Stable: 1.9.1 (Sept 2026). `validate_data` public since 1.6; `BaseEstimator._validate_data`
  deprecated 1.6, removed 1.7. `__sklearn_tags__` / `Tags` dataclass since 1.6; `_more_tags` /
  `_get_tags` deprecated 1.6, removed 1.7 (`check_estimator_tags_renamed` raises `TypeError` if a
  class defines them without `__sklearn_tags__`). `expected_failed_checks` since 1.6;
  `xfail_strict` since 1.8. **Pin `scikit-learn>=1.8`.**

## Constructor, params, fit, attributes

- `__init__`: keyword arguments with defaults; every argument stored verbatim as an attribute; no
  logic, no validation; defaults must be str/int/float/bool/tuple/None/type or callable (no list or
  dict defaults: `check_parameters_default_constructible`); params never mutated
  (`check_estimators_overwrite_params` hashes them); `set_params` must not raise on odd values
  (`check_do_not_raise_errors_in_init_or_set_params`). No `*args`/`**kwargs`.
- `fit(X, y=None)` returns `self`; `y` is the second positional argument; refit == fresh fit
  (`check_fit_idempotent`). Fit may only add/change attributes starting or ending with `_`.
- Fitted attributes end in a single `_`; private learned state starts with `_`. A public attribute
  may mirror a parameter with `_` appended (validated version).
- `n_features_in_` and `feature_names_in_` are set by `validate_data(self, X, ...)` in `fit`
  (`reset=True`) and checked by `validate_data(self, X, reset=False)` in every other method (error
  "X has 1 features, but ... is expecting 4 features as input").
- `_parameter_constraints` / `_validate_params` / `_fit_context` are private; do not rely on them.
  Validate parameters in `fit` with `ValueError`.
- `random_state` convention (if ever needed): store verbatim, `check_random_state` in `fit`.

## Tags (only via `__sklearn_tags__`)

```python
def __sklearn_tags__(self):
    tags = super().__sklearn_tags__()
    tags.input_tags.positive_only = True
    tags.input_tags.sparse = False
    return tags
```
Fields: `estimator_type` (None for a plain transformer; `TransformerMixin` sets `transformer_tags`),
`requires_fit=True`, `non_deterministic=False`, `array_api_support=False`,
`transformer_tags.preserves_dtype=["float64"]`.

**`positive_only=True` ⇒ check data has minimum exactly 0** (`X = X - X.min()`). Every check,
including `check_transformer_general` on scaled blobs and the dtype checks, feeds zeros. Therefore:
tolerate zeros (log 0 = −∞ ⇒ infinitely dominated row, V = 0, log V = −∞, support weight 0,
excluded from the log-mean-exp) and keep outputs consistent across subsets and sample orders.
`check_positive_only_tag_during_fit` requires `fit` on negative data to raise `ValueError` matching
"Negative values in data": use `sklearn.utils.validation.check_non_negative(X, "<ClassName> (input X)")`.
NaN/inf must raise `ValueError` matching `inf|NaN` (default `ensure_all_finite=True`).

## Mixins, methods, output

- Mixins on the left, `BaseEstimator` on the right (`check_mixin_order`).
- `TransformerMixin` gives `fit_transform` and `set_output`; `set_output` is available only if
  `get_feature_names_out` exists. `get_feature_names_out(input_features=None)` returns an object
  ndarray of str with the transform width and raises `ValueError` "input_features should have
  length equal" on mismatch. `inverse_transform` is never wrapped by `set_output`; it still calls
  `check_is_fitted` and checks its input width.
- `OneToOneFeatureMixin` for transformers whose columns map one-to-one (the preconditioner).
- Checks that iterate over implemented methods: `predict`, `transform`, `decision_function`,
  `score_samples`, `predict_proba` must be per-row (`check_methods_subset_invariance`,
  `check_methods_sample_order_invariance`), raise "Reshape your data" on 1-D input, raise
  `NotFittedError` before fit (`check_estimators_unfitted` for predict/decision_function;
  `transform` may raise AttributeError/ValueError), accept float32/float64/int32/int64.
- With a `max_iter` parameter, `n_iter_ >= 1` after fit (`check_transformer_n_iter`).
- One-sample / one-feature fits must work or raise `ValueError` with an accepted message
  (`ensure_min_samples=2` yields one). `transform(X[:, :-1])` must raise `ValueError`.
- Semantics (glossary): `score_samples` is the sanctioned unsupervised per-sample score;
  `decision_function` is for classifiers/outlier detectors with "≥ 0 means inlier" (opposite to our
  log V sign) — not implemented; `predict` is for labels/targets — not on the transformer; the
  regressor wrapper implements `predict` and `score` (R²) per `RegressorMixin`.
- `TransformedTargetRegressor(regressor=..., transformer=...)` fits the regressor on
  `transformer.fit_transform(y)` and inverts predictions; verify its 2-D `y` handling with our
  transformer at implementation.

## Running the checks

```python
from sklearn.utils.estimator_checks import parametrize_with_checks


@parametrize_with_checks(
    [PosynomialInvariantForm(), ...],
    expected_failed_checks=lambda est: {},  # {"check_name": "reason"}
    xfail_strict=True,
)
def test_sklearn_compatible(estimator, check):
    check(estimator)
```
Keys are bare check names (partials unwrapped). Goal: empty dict; any entry needs a written reason.

## Docstrings and layout

numpydoc order: Parameters, Attributes (classes), Returns, See Also, Notes, Examples; `name : type,
default=value`; document `n_features_in_ : int` and `feature_names_in_ : ndarray of shape
(n_features_in_,)`; Examples runnable as doctests (`pytest --doctest-modules`). The
scikit-learn-contrib project template (last updated Oct 2024) still uses `_validate_data` and
`_more_tags`; borrow only its `test_common.py` pattern.

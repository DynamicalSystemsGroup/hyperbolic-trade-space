"""Prediction from configuration: a supervised composition on the learned chart.

Given designs with a configuration ``c`` (decisions known before anything is measured) and
measured metrics ``m``, ``TradeSpaceRegressor`` fits the chart ``m -> (Z, log V)`` with a
``trade_space`` (a ``HyperbolicTradeSpace``, or a ``Pipeline`` of a
preconditioner and one), then fits an ordinary regressor ``c -> (Z, log V)``. Predicting where a
proposed configuration would fall therefore inherits the regression error in *coordinates*
(position along the frontier and distance to it), never in raw metrics.
"""

import inspect

import numpy as np
from sklearn.base import BaseEstimator, RegressorMixin, clone
from sklearn.metrics import r2_score
from sklearn.utils.metaestimators import available_if
from sklearn.utils.validation import check_array, check_is_fitted, validate_data


def _regressor_supports_std(self):
    reg = getattr(self, "regressor_", self.regressor)
    try:
        return "return_std" in inspect.signature(reg.predict).parameters
    except (TypeError, ValueError, AttributeError):
        return False


class TradeSpaceRegressor(RegressorMixin, BaseEstimator):
    """Predict metrics, chart coordinates and novelty from configuration variables.

    Parameters
    ----------
    regressor : estimator
        scikit-learn regressor mapping configuration to chart coordinates ``[Z | log V]``. It is
        cloned at fit. Multi-output is required when the number of metrics is above 2 (its
        target has ``d`` columns, or one when ``d = 1``).
    trade_space : estimator
        Fitted on the metrics ``Y`` to define the chart: a
        ``HyperbolicTradeSpace`` or a ``Pipeline`` whose last step
        is one (for example a preconditioner followed by the estimator). It is cloned at fit.

    Attributes
    ----------
    regressor_ : estimator
        The fitted clone of ``regressor``.
    trade_space_ : estimator
        The fitted clone of ``trade_space``.
    n_outputs_ : int
        Number of metrics ``d``.
    n_features_in_ : int
        Number of configuration variables seen in ``fit``.
    feature_names_in_ : ndarray of shape (n_features_in_,)
        Configuration names, when ``X`` has string column names.

    See Also
    --------
    hyperbolic_trade_space.HyperbolicTradeSpace : the chart this regressor composes with.
    sklearn.compose.TransformedTargetRegressor : the generic pattern this specializes.

    Notes
    -----
    ``score`` is the coefficient of determination in **coordinate space** (uniform average over
    the ``d`` coordinates ``Z`` and ``log V``), not in metric units. Metrics ``y`` must be
    strictly positive (target tag ``positive_only``); a one-dimensional ``y`` is a single metric
    (``d = 1``) and ``predict`` then returns a one-dimensional array. The chart is fitted on the
    training metrics only, so predictions are per-row and independent of sample order.

    Why not ``TransformedTargetRegressor``? It would work for ``predict`` (the chart is an
    invertible transformer with 2-D support), but it has no ``predict_coordinates``,
    ``predict_novelty`` or coordinate-space ``score``, which are the point here.
    ``test_predictive.py`` verifies that the wrapper still composes with this chart.

    Examples
    --------
    >>> import numpy as np
    >>> from sklearn.linear_model import LinearRegression
    >>> from hyperbolic_trade_space import (
    ...     HyperbolicTradeSpace, TradeSpaceRegressor,
    ...     make_configured_frontier_data)
    >>> C, Y, info = make_configured_frontier_data(
    ...     200, 3, 3, nonlinearity=0.0, random_state=0)
    >>> reg = TradeSpaceRegressor(
    ...     LinearRegression(), HyperbolicTradeSpace(np.inf)).fit(C, Y)
    >>> reg.predict(C[:2]).shape
    (2, 3)
    >>> Z, log_v = reg.predict_coordinates(C[:2])
    >>> Z.shape, log_v.shape
    ((2, 2), (2,))
    >>> reg.predict_novelty(C[:2]).shape
    (2,)
    """

    def __init__(self, regressor, trade_space):
        self.regressor = regressor
        self.trade_space = trade_space

    def __sklearn_tags__(self):
        tags = super().__sklearn_tags__()
        tags.target_tags.positive_only = True
        tags.target_tags.multi_output = True
        tags.input_tags.sparse = False
        return tags

    # ------------------------------------------------------------------ helpers
    @staticmethod
    def _as_metrics(y):
        y = np.asarray(y, dtype=np.float64)
        one_d = y.ndim == 1
        Y = y.reshape(-1, 1) if one_d else y
        if not np.all(Y > 0):
            raise ValueError("TradeSpaceRegressor requires strictly positive metrics y (> 0).")
        return Y, one_d

    def _target_coordinates(self, Y):
        T = np.asarray(self.trade_space_.transform(Y), dtype=np.float64)
        if not np.all(np.isfinite(T)):
            raise ValueError("The chart of y has non-finite coordinates; metrics must be > 0.")
        return T

    def _coordinates(self, X):
        check_is_fitted(self, "regressor_")
        X = validate_data(self, X, reset=False)
        return X, self._columns(self.regressor_.predict(X))

    @staticmethod
    def _columns(pred):
        pred = np.asarray(pred, dtype=np.float64)
        return pred.reshape(-1, 1) if pred.ndim == 1 else pred

    def _out(self, M):
        return M.ravel() if self._y_1d_ else M

    # ------------------------------------------------------------------ API
    def fit(self, X, y):
        """Fit the chart on ``y``, then the regressor on ``X`` -> chart coordinates.

        Parameters
        ----------
        X : array-like of shape (n_samples, n_config)
            Configuration variables.
        y : array-like of shape (n_samples,) or (n_samples, n_metrics)
            Measured metrics, strictly positive.

        Returns
        -------
        self : TradeSpaceRegressor
        """
        X, y = validate_data(self, X, y, multi_output=True, y_numeric=True, ensure_min_samples=2)
        Y, one_d = self._as_metrics(y)
        self._y_1d_ = one_d
        self.n_outputs_ = Y.shape[1]
        self.trade_space_ = clone(self.trade_space).fit(Y)
        T = self._target_coordinates(Y)
        self.regressor_ = clone(self.regressor).fit(X, T[:, 0] if T.shape[1] == 1 else T)
        return self

    def predict_coordinates(self, X):
        """Predicted chart coordinates of configurations.

        Parameters
        ----------
        X : array-like of shape (n_samples, n_config)

        Returns
        -------
        Z : ndarray of shape (n_samples, n_metrics - 1)
            Position along the frontier (log-ratio coordinates).
        log_v : ndarray of shape (n_samples,)
            Predicted log V (zero on the frontier, positive beyond it).
        """
        _, T = self._coordinates(X)
        return T[:, :-1], T[:, -1]

    def predict(self, X):
        """Predicted metrics (chart coordinates mapped back by ``inverse_transform``).

        Parameters
        ----------
        X : array-like of shape (n_samples, n_config)

        Returns
        -------
        ndarray of shape (n_samples,) or (n_samples, n_metrics)
            One-dimensional when ``y`` was one-dimensional in ``fit``.
        """
        _, T = self._coordinates(X)
        return self._out(self.trade_space_.inverse_transform(T))

    def predict_novelty(self, X):
        """Predicted novelty ``V - 1`` of configurations (zero on the frontier).

        Parameters
        ----------
        X : array-like of shape (n_samples, n_config)

        Returns
        -------
        ndarray of shape (n_samples,)
            ``expm1(predicted log V)``; positive means predicted beyond the frontier.
        """
        return np.expm1(self.predict_coordinates(X)[1])

    @available_if(_regressor_supports_std)
    def predict_std(self, X):
        """Standard deviation of the predicted metrics, by the delta method.

        Available only when the regressor's ``predict`` accepts ``return_std`` (for example
        ``GaussianProcessRegressor``); otherwise accessing it raises ``AttributeError``.

        Parameters
        ----------
        X : array-like of shape (n_samples, n_config)

        Returns
        -------
        ndarray of shape (n_samples,) or (n_samples, n_metrics)
            ``m_j * sqrt(sum_k J_jk^2 s_k^2)`` where ``s_k`` is the regressor's standard
            deviation of coordinate ``k`` and ``J = d log m / d coordinates`` (exact: the chart
            is affine in log-metrics). Coordinates are treated as independent, and a regressor
            returning one standard deviation per row shares it across coordinates.
        """
        X, mu = self._coordinates(X)
        _, s = self.regressor_.predict(X, return_std=True)
        s = np.asarray(s, dtype=np.float64)
        s = np.broadcast_to(s.reshape(-1, 1) if s.ndim == 1 else s, mu.shape)
        base = mu[:1]
        log0 = np.log(self.trade_space_.inverse_transform(base))
        J = np.empty((log0.shape[1], mu.shape[1]))
        for k in range(mu.shape[1]):
            e = base.copy()
            e[0, k] += 1.0
            J[:, k] = (np.log(self.trade_space_.inverse_transform(e)) - log0)[0]
        m = self.trade_space_.inverse_transform(mu)
        return self._out(m * np.sqrt((s**2) @ (J**2).T))

    def score(self, X, y, sample_weight=None):
        """R^2 in coordinate space, uniformly averaged over ``Z`` and ``log V``.

        Parameters
        ----------
        X : array-like of shape (n_samples, n_config)
        y : array-like of shape (n_samples,) or (n_samples, n_metrics)
            True metrics (positive); mapped through the fitted chart for comparison.
        sample_weight : array-like of shape (n_samples,), default=None

        Returns
        -------
        float
        """
        _, pred = self._coordinates(X)
        Y, _ = self._as_metrics(check_array(y, ensure_2d=False))
        return float(r2_score(self._target_coordinates(Y), pred, sample_weight=sample_weight))

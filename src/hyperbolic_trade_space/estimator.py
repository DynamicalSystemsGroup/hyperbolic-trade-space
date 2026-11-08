"""The ``HyperbolicTradeSpace`` estimator: a monomial (K = 1) frontier in a log-ratio chart.

The model is ``V(m) = prod_j m_j^{w_j} e^{-beta}`` with ``w`` on the simplex (lemmas L1, L2);
the fit minimizes the log-mean-exp objective ``J_tau`` (L3 to L5); the chart ``(Z, log V)`` is the
linear bijection of log space of lemma L8. Mathematics: ``docs`` and spec section 4.
"""

from __future__ import annotations

import numbers
import warnings

import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.exceptions import ConvergenceWarning
from sklearn.utils.validation import check_array, check_is_fitted, check_non_negative, validate_data

from . import coordinates as _coords
from . import solvers as _solvers

__all__ = ["HyperbolicTradeSpace"]

_ABOVE_TOL = 1e-9  # V > 1 + tol counts as "above the frontier" at tau = inf


class HyperbolicTradeSpace(TransformerMixin, BaseEstimator):
    """Posynomial invariant form: learn the shape of a design trade space (K = 1, monomial).

    Fits ``V(m) = prod_j m_j^{w_j} / e^{beta}`` to strictly positive, larger-is-better metrics so
    that ``V <= 1`` is the attainable region and ``V = 1`` the frontier, by minimizing the
    entropic soft maximum of ``w . log m`` over the simplex. The transform is the invertible chart
    ``[Z | log V]`` (log-ratio coordinates along the frontier, and the depth below it).

    Parameters
    ----------
    temperature : float, default=10.0
        Softness ``tau`` of the soft maximum, ``tau > 0`` or ``np.inf`` (an exact LP). Units are
        1 / (log-spread of the metrics), so condition the metrics first; useful range 3 to 100.
    min_exponent : float, default=0.0
        Lower bound on each exponent, in ``[0, 1/d)``.
    coordinates : {"ilr", "alr"}, default="ilr"
        Chart basis: Helmert (orthonormal, the lemma L8 hypotheses hold) or additive log-ratio
        (invertible, not orthonormal; last metric is the reference).
    n_terms : int, default=1
        Number of monomial terms. Only 1 is implemented; larger values raise
        ``NotImplementedError`` (documented extension, spec section 4).
    term_temperature : float, default=np.inf
        Reserved for ``n_terms > 1``; stored and ignored.
    tol : float, default=1e-10
        Solver tolerance (SLSQP ``ftol``).
    max_iter : int, default=500
        Maximum SLSQP iterations.

    Attributes
    ----------
    exponents_ : ndarray of shape (1, n_features_in_)
        Fitted exponents ``w`` on the simplex.
    log_offset_ : ndarray of shape (1,)
        The offset ``beta = J_tau(w)``.
    support_weights_ : ndarray of shape (n_samples,)
        Softmax weights ``p`` at the solution (LP duals at ``tau = inf``); zero for rows with a
        zero metric.
    n_eff_ : float
        Effective number of supporting rows, ``1 / sum p_i^2``.
    frac_above_ : float
        Fraction of (non-degenerate) training rows with ``V > 1``.
    objective_ : float
        ``J_tau(w)`` at the solution (equals ``beta``).
    n_iter_ : int
        Solver iterations (at least 1; 1 on the LP-only path).
    basis_ : ndarray of shape (n_features_in_ - 1, n_features_in_)
        Chart matrix ``B`` (``Z = log(X) @ B.T``).
    training_log_v_ : ndarray of shape (n_samples,)
        ``log V`` of the training rows (``-inf`` for rows with a zero metric).
    n_features_in_ : int
        Number of metrics seen in ``fit``.
    feature_names_in_ : ndarray of shape (n_features_in_,)
        Names of the metrics seen in ``fit``; defined only for string column names.

    See Also
    --------
    hyperbolic_trade_space.make_frontier_data : Synthetic data with a planted frontier.

    Notes
    -----
    Zero metrics are tolerated: ``log 0 = -inf``, so the row has ``V = 0``, ``log V = -inf``,
    support weight 0, and is excluded from the objective; its ``Z`` is ``nan`` and it has no
    inverse. Negative values raise ``ValueError``. Grounding: homogeneity and the invariant form
    (L1), the offset (L2), gradient and support weights (L3), convexity (L4), log-mean-exp
    (L5), noise offset (L6), elasticities and improvement factors (L7), the chart (L8).

    Examples
    --------
    >>> import numpy as np
    >>> from hyperbolic_trade_space import HyperbolicTradeSpace, make_frontier_data
    >>> X, info = make_frontier_data(300, 3, random_state=0)
    >>> hts = HyperbolicTradeSpace(temperature=np.inf).fit(X)
    >>> np.allclose(hts.exponents_[0], info["exponents"], atol=1e-3)
    True
    >>> hts.transform(X).shape
    (300, 3)
    >>> hts.get_feature_names_out().tolist()
    ['ilr0', 'ilr1', 'log_v']
    >>> bool(np.allclose(hts.inverse_transform(hts.transform(X)), X))
    True
    """

    def __init__(
        self,
        temperature=10.0,
        min_exponent=0.0,
        coordinates="ilr",
        n_terms=1,
        term_temperature=np.inf,
        tol=1e-10,
        max_iter=500,
    ):
        self.temperature = temperature
        self.min_exponent = min_exponent
        self.coordinates = coordinates
        self.n_terms = n_terms
        self.term_temperature = term_temperature
        self.tol = tol
        self.max_iter = max_iter

    def __sklearn_tags__(self):
        tags = super().__sklearn_tags__()
        tags.input_tags.positive_only = True
        tags.input_tags.sparse = False
        return tags

    # ------------------------------------------------------------------ validation helpers
    def _check_params(self, d):
        t = self.temperature
        if not (isinstance(t, numbers.Real) and not isinstance(t, bool) and t > 0):
            raise ValueError(f"temperature must be a float > 0 or np.inf, got {t!r}")
        m = self.min_exponent
        if not (isinstance(m, numbers.Real) and 0.0 <= m < 1.0 / d):
            raise ValueError(f"min_exponent must be in [0, 1/d) = [0, {1.0 / d:.4g}), got {m!r}")
        if self.coordinates not in ("ilr", "alr"):
            raise ValueError(f"coordinates must be 'ilr' or 'alr', got {self.coordinates!r}")
        if not (isinstance(self.n_terms, numbers.Integral) and self.n_terms >= 1):
            raise ValueError(f"n_terms must be an integer >= 1, got {self.n_terms!r}")
        if not (isinstance(self.tol, numbers.Real) and self.tol > 0):
            raise ValueError(f"tol must be > 0, got {self.tol!r}")
        if not (isinstance(self.max_iter, numbers.Integral) and self.max_iter >= 1):
            raise ValueError(f"max_iter must be an integer >= 1, got {self.max_iter!r}")
        if self.n_terms != 1:
            raise NotImplementedError(
                "n_terms > 1 is a documented extension (spec section 4); "
                "only n_terms=1 is implemented"
            )

    def _log_metrics(self, X, reset):
        X = validate_data(self, X, reset=reset, dtype=np.float64)
        check_non_negative(X, "HyperbolicTradeSpace (input X)")
        with np.errstate(divide="ignore"):
            return np.log(X)

    # ------------------------------------------------------------------ fit
    def fit(self, X, y=None):
        """Fit the frontier ``w``, ``beta`` and the chart.

        Parameters
        ----------
        X : array-like of shape (n_samples, n_features)
            Strictly positive (zeros tolerated) larger-is-better metrics.
        y : None
            Ignored.

        Returns
        -------
        self : HyperbolicTradeSpace
            The fitted estimator.

        Examples
        --------
        >>> from hyperbolic_trade_space import HyperbolicTradeSpace, make_frontier_data
        >>> X, _ = make_frontier_data(100, 2, random_state=1)
        >>> HyperbolicTradeSpace().fit(X).exponents_.shape
        (1, 2)
        """
        U = self._log_metrics(X, reset=True)
        n, d = U.shape
        self._check_params(d)
        tau = float(self.temperature)
        valid = np.isfinite(U).all(axis=1)
        if not valid.any():
            raise ValueError(f"every row contains a zero metric (n_samples = {n}); nothing to fit")
        Uv = U[valid]
        nv = Uv.shape[0]

        if d == 1:
            w = np.ones(1)
            beta = _solvers.log_mean_exp(Uv[:, 0], tau)
            p = _solvers.support_weights(Uv[:, 0], tau)
            n_iter = 1
        elif nv == 1:
            w = np.full(d, 1.0 / d)
            beta = float(Uv[0] @ w)
            p = np.ones(1)
            n_iter = 1
        else:
            res = _solvers.solve_lp(Uv, self.min_exponent)
            if np.isfinite(tau):
                res = _solvers.solve_slsqp(
                    Uv, tau, self.min_exponent, w0=res.w, tol=self.tol, max_iter=self.max_iter
                )
            if not res.success:
                warnings.warn(
                    f"solver did not converge: {res.message}", ConvergenceWarning, stacklevel=2
                )
            w, beta, p, n_iter = res.w, res.beta, res.p, res.n_iter

        B = _coords.helmert_basis(d) if self.coordinates == "ilr" else _coords.alr_basis(d)
        _, log_v = _coords.to_frontier_coordinates(U, w, beta, B)
        support = np.zeros(n)
        support[valid] = p
        above = log_v[valid] > (_ABOVE_TOL if np.isinf(tau) else 0.0)

        self.exponents_ = w[None, :]
        self.log_offset_ = np.array([beta])
        self.support_weights_ = support
        self.n_eff_ = float(1.0 / np.sum(p**2))
        self.frac_above_ = float(np.mean(above))
        self.objective_ = float(beta)
        self.n_iter_ = max(int(n_iter), 1)
        self.basis_ = B
        self.training_log_v_ = log_v
        return self

    # ------------------------------------------------------------------ chart
    def _coordinates(self, X):
        check_is_fitted(self)
        U = self._log_metrics(X, reset=False)
        return _coords.to_frontier_coordinates(
            U, self.exponents_[0], self.log_offset_[0], self.basis_
        )

    def transform(self, X):
        """Map metrics to the chart ``[Z | log V]``.

        Parameters
        ----------
        X : array-like of shape (n_samples, n_features)
            Metrics, nonnegative.

        Returns
        -------
        ndarray of shape (n_samples, n_features)
            ``Z`` (``n_features - 1`` log-ratio coordinates) then ``log V``. Rows with a zero
            metric give ``nan`` in ``Z`` and ``-inf`` in ``log V``.

        Examples
        --------
        >>> from hyperbolic_trade_space import HyperbolicTradeSpace, make_frontier_data
        >>> X, _ = make_frontier_data(50, 3, random_state=0)
        >>> HyperbolicTradeSpace().fit(X).transform(X[:2]).shape
        (2, 3)
        """
        Z, log_v = self._coordinates(X)
        return np.column_stack([Z, log_v])

    def inverse_transform(self, Xt):
        """Map chart coordinates ``[Z | log V]`` back to metrics.

        Parameters
        ----------
        Xt : array-like of shape (n_samples, n_features)
            Chart coordinates as returned by :meth:`transform`.

        Returns
        -------
        ndarray of shape (n_samples, n_features)
            Metrics ``exp(u)`` (lemma L8 inverse). Rows with non-finite coordinates (a zero
            metric in the original) are not invertible and give ``nan``.

        Examples
        --------
        >>> import numpy as np
        >>> from hyperbolic_trade_space import HyperbolicTradeSpace, make_frontier_data
        >>> X, _ = make_frontier_data(50, 3, random_state=0)
        >>> hts = HyperbolicTradeSpace().fit(X)
        >>> bool(np.allclose(hts.inverse_transform(hts.transform(X)), X))
        True
        """
        check_is_fitted(self)
        Xt = check_array(Xt, dtype=np.float64, ensure_all_finite=False)
        if Xt.shape[1] != self.n_features_in_:
            raise ValueError(
                f"X has {Xt.shape[1]} features, but {self.__class__.__name__} is expecting "
                f"{self.n_features_in_} features as input"
            )
        U = _coords.from_frontier_coordinates(
            Xt[:, :-1], Xt[:, -1], self.exponents_[0], self.log_offset_[0], self.basis_
        )
        return np.exp(U)

    def get_feature_names_out(self, input_features=None):
        """Names of the transform columns: ``ilr0..`` (or ``alr0..``) then ``log_v``.

        Parameters
        ----------
        input_features : array-like of str or None, default=None
            Checked against ``feature_names_in_`` and ``n_features_in_`` when given.

        Returns
        -------
        ndarray of str, shape (n_features_in_,)
            Output feature names.

        Examples
        --------
        >>> from hyperbolic_trade_space import HyperbolicTradeSpace, make_frontier_data
        >>> X, _ = make_frontier_data(30, 2, random_state=0)
        >>> HyperbolicTradeSpace(coordinates="alr").fit(X).get_feature_names_out().tolist()
        ['alr0', 'log_v']
        """
        check_is_fitted(self)
        if input_features is not None:
            names = np.asarray(input_features, dtype=object)
            if names.shape != (self.n_features_in_,):
                raise ValueError(
                    f"input_features should have length equal to number of features "
                    f"({self.n_features_in_}), got {names.size}"
                )
            fitted = getattr(self, "feature_names_in_", None)
            if fitted is not None and not np.array_equal(names, fitted):
                raise ValueError("input_features is not equal to feature_names_in_")
        prefix = "ilr" if self.coordinates == "ilr" else "alr"
        out = [f"{prefix}{k}" for k in range(self.n_features_in_ - 1)] + ["log_v"]
        return np.asarray(out, dtype=object)

    # ------------------------------------------------------------------ scores and domain methods
    def score_samples(self, X):
        """Log invariant value ``log V(m) = w . log m - beta`` of each row (lemma L1).

        Parameters
        ----------
        X : array-like of shape (n_samples, n_features)

        Returns
        -------
        ndarray of shape (n_samples,)
            ``log V``; ``-inf`` for a zero metric. Positive means beyond the fitted frontier.

        Examples
        --------
        >>> from hyperbolic_trade_space import HyperbolicTradeSpace, make_frontier_data
        >>> X, _ = make_frontier_data(60, 3, random_state=0)
        >>> HyperbolicTradeSpace().fit(X).score_samples(X).shape
        (60,)
        """
        return self._coordinates(X)[1]

    def invariant_value(self, X):
        """Invariant value ``V = exp(log V)``; ``V = 1`` on the frontier, ``V < 1`` inside.

        Parameters
        ----------
        X : array-like of shape (n_samples, n_features)

        Returns
        -------
        ndarray of shape (n_samples,)
            ``V``; 0 for a zero metric.

        Examples
        --------
        >>> from hyperbolic_trade_space import HyperbolicTradeSpace, make_frontier_data
        >>> X, _ = make_frontier_data(60, 3, random_state=0)
        >>> bool((HyperbolicTradeSpace(temperature=float("inf")).fit(X)
        ...       .invariant_value(X) <= 1 + 1e-9).all())
        True
        """
        return np.exp(self.score_samples(X))

    def project(self, X):
        """Project onto the frontier along the diagonal: ``m / V`` (invariant form, lemma L1).

        Parameters
        ----------
        X : array-like of shape (n_samples, n_features)

        Returns
        -------
        ndarray of shape (n_samples, n_features)
            ``m / V``, which has ``V = 1`` (homogeneity); ``nan`` rows where ``V = 0``.

        Examples
        --------
        >>> import numpy as np
        >>> from hyperbolic_trade_space import HyperbolicTradeSpace, make_frontier_data
        >>> X, _ = make_frontier_data(60, 3, random_state=0)
        >>> hts = HyperbolicTradeSpace().fit(X)
        >>> bool(np.allclose(hts.invariant_value(hts.project(X)), 1.0))
        True
        """
        V = self.invariant_value(X)
        X = check_array(X, dtype=np.float64)
        with np.errstate(divide="ignore", invalid="ignore"):
            out = X / V[:, None]
        out[V == 0] = np.nan
        return out

    def improvement_factors(self, X):
        """Per-metric improvement factor ``V^(-1/w_j)`` that lands on the frontier (lemma L7).

        Parameters
        ----------
        X : array-like of shape (n_samples, n_features)

        Returns
        -------
        ndarray of shape (n_samples, n_features)
            Entry ``(i, j)``: the factor by which metric ``j`` alone must be multiplied to reach
            ``V = 1``. ``inf`` where ``w_j`` is below ``1e-12`` (numerically zero) or ``V = 0``.

        Examples
        --------
        >>> import numpy as np
        >>> from hyperbolic_trade_space import HyperbolicTradeSpace, make_frontier_data
        >>> X, _ = make_frontier_data(60, 3, random_state=0)
        >>> hts = HyperbolicTradeSpace().fit(X)
        >>> x = X[:1].copy()
        >>> f = hts.improvement_factors(x)[0, 1]
        >>> x[0, 1] *= f
        >>> round(float(hts.invariant_value(x)[0]), 6)
        1.0
        """
        log_v = self.score_samples(X)
        w = self.exponents_[0]
        out = np.full((log_v.shape[0], w.shape[0]), np.inf)
        pos = w > 1e-12  # exponents below 1e-12 are numerically zero (solver noise)
        with np.errstate(divide="ignore", invalid="ignore", over="ignore"):
            out[:, pos] = np.exp(-log_v[:, None] / w[None, pos])
        out[~np.isfinite(log_v), :] = np.inf
        return out

    def novelty_score(self, X, calibrated=False):
        """Novelty of each row relative to the fitted frontier.

        Parameters
        ----------
        X : array-like of shape (n_samples, n_features)
        calibrated : bool, default=False
            If False return ``V - 1`` (the uniform factor by which a frontier design must improve
            to reach the point, lemma L1). If True return an array whose first column is the
            fraction of training ``log V`` (finite ones) that are ``<=`` the query's, and whose
            second is ``tau * log V`` (``log V`` itself when ``tau`` is infinite).

        Returns
        -------
        ndarray of shape (n_samples,) or (n_samples, 2)

        Notes
        -----
        Training rows exceed ``V = 1`` by construction at finite ``tau`` (``frac_above_``), so
        the calibrated form is the fair comparison. Far from the balanced region ``V - 1`` is
        conservative.

        Examples
        --------
        >>> import numpy as np
        >>> from hyperbolic_trade_space import HyperbolicTradeSpace, make_frontier_data
        >>> X, _ = make_frontier_data(80, 3, random_state=0)
        >>> hts = HyperbolicTradeSpace().fit(X)
        >>> hts.novelty_score(X[:3]).shape, hts.novelty_score(X[:3], calibrated=True).shape
        ((3,), (3, 2))
        """
        log_v = self.score_samples(X)
        if not calibrated:
            return np.exp(log_v) - 1.0
        train = np.sort(self.training_log_v_[np.isfinite(self.training_log_v_)])
        rank = np.searchsorted(train, log_v, side="right") / train.size
        tau = self.temperature
        scaled = log_v if np.isinf(tau) else tau * log_v
        return np.column_stack([rank, scaled])

    def level_set(self, Z, value=1.0):
        """Metric points on the level set ``{V = value}`` above chart coordinates ``Z``.

        Parameters
        ----------
        Z : array-like of shape (n_points, n_features - 1)
            Log-ratio coordinates (the leading columns of :meth:`transform`).
        value : float, default=1.0
            Target invariant value ``V > 0``; 1 is the frontier.

        Returns
        -------
        ndarray of shape (n_points, n_features)
            Metrics ``m`` with ``V(m) = value`` whose chart coordinates are ``Z``.

        Examples
        --------
        >>> import numpy as np
        >>> from hyperbolic_trade_space import HyperbolicTradeSpace, make_frontier_data
        >>> X, _ = make_frontier_data(60, 3, random_state=0)
        >>> hts = HyperbolicTradeSpace().fit(X)
        >>> M = hts.level_set(np.zeros((1, 2)), value=0.5)
        >>> round(float(hts.invariant_value(M)[0]), 6)
        0.5
        """
        check_is_fitted(self)
        if not value > 0:
            raise ValueError("value must be > 0")
        d = self.n_features_in_
        Z = check_array(Z, dtype=np.float64, ensure_min_features=0, ensure_min_samples=1)
        if Z.shape[1] != d - 1:
            raise ValueError(f"Z must have {d - 1} columns, got {Z.shape[1]}")
        log_v = np.full(Z.shape[0], np.log(value))
        U = _coords.from_frontier_coordinates(
            Z, log_v, self.exponents_[0], self.log_offset_[0], self.basis_
        )
        return np.exp(U)

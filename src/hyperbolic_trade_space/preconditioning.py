"""Conditioning of attributes into larger-is-better metrics, and the pull-back to attributes.

The analyst's conditioning is ``log m_j = alpha_j log(a_j + s_j) + b_j`` with
``alpha_j != 0``. ``LogAffinePreconditioner`` is that map with ``alpha_j = o_j / scale_j``
(``o_j = +1`` for larger-is-better, ``-1`` for smaller-is-better attributes), so metrics come out
strictly positive and larger-is-better. ``frontier_in_original_units`` is the closed form of
the pull-back: the fitted frontier as a monomial in the raw attributes.
"""

from __future__ import annotations

import numpy as np
from sklearn.base import BaseEstimator, OneToOneFeatureMixin, TransformerMixin, clone
from sklearn.preprocessing import RobustScaler, StandardScaler
from sklearn.utils.validation import check_array, check_is_fitted, check_non_negative, validate_data

__all__ = ["LogAffinePreconditioner", "frontier_in_original_units"]


class LogAffinePreconditioner(OneToOneFeatureMixin, TransformerMixin, BaseEstimator):
    """Condition attributes into strictly positive, larger-is-better metrics (log-affine map).

    Computes ``z = o * log(X + shift)`` per column, fits a scaler on the finite entries of ``z``,
    and returns ``m = exp(scaled z)``. Entries with ``X + shift == 0`` map to ``0`` (an infinitely
    dominated row for the estimator, whatever the orientation). The map is invertible
    (``inverse_transform`` is exact) and affine in log space, which is the conditioning of
    attributes.

    Parameters
    ----------
    orientation : array-like of {+1, -1}, int, or None, default=None
        ``+1`` larger-is-better, ``-1`` smaller-is-better, per column; a single ``+1``/``-1``
        applies to every column; ``None`` means all ``+1``.
    shift : float or array-like of shape (n_features,), default=0.0
        Offset ``s_j`` added before the logarithm; ``X + shift`` must be nonnegative.
    scaler : {"standard", "robust"}, None or scikit-learn scaler instance, default="standard"
        Affine scaler fitted on the finite ``z`` of each column. ``"standard"`` gives unit
        log-standard-deviation, ``"robust"`` unit log-IQR, ``None`` no scaling (pure log).
        An instance must be affine per column (cloned at fit).

    Attributes
    ----------
    scaler_ : fitted scaler or None
        The fitted scaler (``None`` when ``scaler=None``).
    log_offset_ : ndarray of shape (n_features_in_,)
        ``c_j``: the log value ``z_j`` that maps to metric ``1`` (the center removed by the
        scaler); scaled ``z = (z - log_offset_) / log_scale_``.
    log_scale_ : ndarray of shape (n_features_in_,)
        ``k_j``: log-units per scaled unit (the standard deviation for ``"standard"``).
    orientation_ : ndarray of shape (n_features_in_,)
        Validated orientation, entries ``+1`` or ``-1``.
    shift_ : ndarray of shape (n_features_in_,)
        Validated shift.
    n_features_in_ : int
        Number of columns seen in ``fit``.
    feature_names_in_ : ndarray of shape (n_features_in_,)
        Column names seen in ``fit`` (only when ``X`` has string column names).

    See Also
    --------
    frontier_in_original_units : Pull the fitted frontier back to raw attributes.

    Notes
    -----
    The map is ``log m_j = alpha_j log(a_j + s_j) + b_j`` with ``alpha_j = o_j / log_scale_j``,
    ``b_j = -log_offset_j / log_scale_j`` and ``a_j = shift_j``. Which orientation, shift and
    scaling are appropriate is the analyst's decision, not derived. Entries with ``X + shift == 0``
    are ignored by the scaler; a column consisting only of such entries gets the identity scaling
    (offset 0, scale 1).

    Examples
    --------
    >>> import numpy as np
    >>> from hyperbolic_trade_space import LogAffinePreconditioner
    >>> X = np.array([[1.0, 10.0], [2.0, 5.0], [4.0, 2.5], [8.0, 1.25]])
    >>> pre = LogAffinePreconditioner(orientation=[1, -1]).fit(X)
    >>> M = pre.transform(X)
    >>> bool(np.allclose(np.log(M).std(axis=0), 1.0))
    True
    >>> bool(np.allclose(pre.inverse_transform(M), X))
    True
    """

    def __init__(self, orientation=None, shift=0.0, scaler="standard"):
        self.orientation = orientation
        self.shift = shift
        self.scaler = scaler

    def __sklearn_tags__(self):
        tags = super().__sklearn_tags__()
        tags.input_tags.positive_only = True
        tags.input_tags.sparse = False
        return tags

    # ------------------------------------------------------------------ helpers
    def _per_column(self, value, d, name, default):
        if value is None:
            return np.full(d, default, dtype=float)
        arr = np.asarray(value, dtype=float)
        if arr.ndim == 0:
            return np.full(d, float(arr))
        if arr.shape != (d,):
            raise ValueError(f"{name} must be a scalar or have length {d}, got shape {arr.shape}")
        return arr

    def _check_params(self, d):
        o = self._per_column(self.orientation, d, "orientation", 1.0)
        if not np.all(np.abs(o) == 1):
            raise ValueError("orientation entries must be +1 or -1")
        s = self._per_column(self.shift, d, "shift", 0.0)
        if not np.all(np.isfinite(s)):
            raise ValueError("shift must be finite")
        sc = self.scaler
        if sc is None:
            scaler = None
        elif isinstance(sc, str):
            if sc == "standard":
                scaler = StandardScaler()
            elif sc == "robust":
                scaler = RobustScaler()
            else:
                raise ValueError(
                    f"scaler must be 'standard', 'robust', None or an instance, got {sc!r}"
                )
        elif hasattr(sc, "fit") and hasattr(sc, "transform") and hasattr(sc, "inverse_transform"):
            scaler = clone(sc)
        else:
            raise ValueError(
                f"scaler must be 'standard', 'robust', None or an instance, got {sc!r}"
            )
        return o, s, scaler

    def _log_z(self, X, o, s):
        """Return ``(z, zero_mask)`` with ``z = o log(X + shift)``, zero entries as nan."""
        Xs = X + s
        check_non_negative(Xs, f"{self.__class__.__name__} (input X)")
        zero = Xs == 0
        with np.errstate(divide="ignore"):
            z = o * np.log(Xs)
        z[zero] = np.nan
        return z, zero

    # ------------------------------------------------------------------ fit
    def fit(self, X, y=None):
        """Fit the scaler on the finite log values of each column.

        Parameters
        ----------
        X : array-like of shape (n_samples, n_features)
            Raw attributes with ``X + shift >= 0``.
        y : None
            Ignored.

        Returns
        -------
        self : LogAffinePreconditioner
            The fitted transformer.

        Examples
        --------
        >>> import numpy as np
        >>> from hyperbolic_trade_space import LogAffinePreconditioner
        >>> X = np.array([[1.0, 2.0], [2.0, 4.0], [4.0, 8.0]])
        >>> LogAffinePreconditioner().fit(X).log_scale_.shape
        (2,)
        """
        X = validate_data(self, X, reset=True, dtype=np.float64)
        o, s, scaler = self._check_params(X.shape[1])
        z, _ = self._log_z(X, o, s)
        d = X.shape[1]
        self.orientation_, self.shift_ = o, s
        empty = np.all(np.isnan(z), axis=0)  # all-zero column: nothing to learn, identity
        z = np.where(empty, 0.0, z)
        if scaler is None:
            self.scaler_ = None
            self.log_offset_ = np.zeros(d)
            self.log_scale_ = np.ones(d)
        else:
            scaler.fit(z)
            self.scaler_ = scaler
            origin = np.asarray(scaler.inverse_transform(np.zeros((1, d))))[0]
            unit = np.asarray(scaler.inverse_transform(np.ones((1, d))))[0]
            self.log_offset_ = origin
            self.log_scale_ = unit - origin
        return self

    # ------------------------------------------------------------------ maps
    def transform(self, X):
        """Condition attributes to metrics ``exp(scaled z)``; ``X + shift == 0`` gives ``0``.

        Parameters
        ----------
        X : array-like of shape (n_samples, n_features)
            Raw attributes with ``X + shift >= 0``.

        Returns
        -------
        ndarray of shape (n_samples, n_features)
            Strictly positive larger-is-better metrics (zeros where ``X + shift == 0``).

        Examples
        --------
        >>> import numpy as np
        >>> from hyperbolic_trade_space import LogAffinePreconditioner
        >>> X = np.array([[0.0, 2.0], [2.0, 4.0], [4.0, 8.0]])
        >>> M = LogAffinePreconditioner().fit(X).transform(X)
        >>> M[0].tolist()[0]
        0.0
        """
        check_is_fitted(self, "log_scale_")
        X = validate_data(self, X, reset=False, dtype=np.float64)
        z, zero = self._log_z(X, self.orientation_, self.shift_)
        u = (z - self.log_offset_) / self.log_scale_
        with np.errstate(over="ignore"):
            M = np.exp(u)
        M[zero] = 0.0
        return M

    def inverse_transform(self, Xt):
        """Exact inverse of ``transform`` (``0`` maps to ``X = -shift``).

        Parameters
        ----------
        Xt : array-like of shape (n_samples, n_features)
            Metrics, nonnegative.

        Returns
        -------
        ndarray of shape (n_samples, n_features)
            Raw attributes.

        Examples
        --------
        >>> import numpy as np
        >>> from hyperbolic_trade_space import LogAffinePreconditioner
        >>> X = np.array([[1.0, 2.0], [2.0, 4.0], [4.0, 8.0]])
        >>> pre = LogAffinePreconditioner(shift=0.5).fit(X)
        >>> bool(np.allclose(pre.inverse_transform(pre.transform(X)), X))
        True
        """
        check_is_fitted(self, "log_scale_")
        Xt = check_array(Xt, dtype=np.float64)
        if Xt.shape[1] != self.n_features_in_:
            raise ValueError(
                f"X has {Xt.shape[1]} features, but {self.__class__.__name__} is expecting "
                f"{self.n_features_in_} features as input"
            )
        check_non_negative(Xt, f"{self.__class__.__name__} (input Xt)")
        zero = Xt == 0
        with np.errstate(divide="ignore"):
            u = np.log(Xt)
        u[zero] = 0.0
        z = u * self.log_scale_ + self.log_offset_
        with np.errstate(over="ignore"):
            X = np.exp(self.orientation_ * z) - self.shift_
        X[zero] = np.broadcast_to(-self.shift_, X.shape)[zero]
        return X


def frontier_in_original_units(estimator, preconditioner):
    """Pull the fitted frontier back to raw attributes (closed form).

    With ``log m_j = alpha_j log(a_j + s_j) + b_j`` and ``log V = w . log m - beta`` the frontier
    is ``V = exp(log_const) * prod_j (s_j + shift_j)^(exponents_orig_j)`` for raw attributes
    ``s_j``, where ``exponents_orig_j = w_j alpha_j`` and ``log_const = w . b - beta``. A negative
    exponent marks a smaller-is-better attribute.

    Parameters
    ----------
    estimator : HyperbolicTradeSpace
        Fitted on the preconditioner's output (``n_terms = 1``).
    preconditioner : LogAffinePreconditioner
        Fitted preconditioner that produced the estimator's input.

    Returns
    -------
    dict
        ``exponents_orig`` (ndarray ``(d,)``), ``log_const`` (float), ``shift`` (ndarray ``(d,)``).
        Evaluate ``log V = log_const + exponents_orig @ log(X + shift)``.

    Examples
    --------
    >>> import numpy as np
    >>> from hyperbolic_trade_space import (
    ...     HyperbolicTradeSpace, LogAffinePreconditioner,
    ...     frontier_in_original_units)
    >>> rng = np.random.RandomState(0)
    >>> X = np.exp(rng.randn(40, 3))
    >>> pre = LogAffinePreconditioner(orientation=[1, -1, 1]).fit(X)
    >>> est = HyperbolicTradeSpace().fit(pre.transform(X))
    >>> f = frontier_in_original_units(est, pre)
    >>> logv = f["log_const"] + np.log(X + f["shift"]) @ f["exponents_orig"]
    >>> bool(np.allclose(logv, est.score_samples(pre.transform(X))))
    True
    """
    check_is_fitted(estimator, "exponents_")
    check_is_fitted(preconditioner, "log_scale_")
    w = np.asarray(estimator.exponents_)
    if w.shape[0] != 1:
        raise ValueError("only a single-term (n_terms = 1) frontier can be pulled back")
    w = w[0]
    d = preconditioner.n_features_in_
    if w.shape[0] != d:
        raise ValueError(
            f"estimator has {w.shape[0]} metrics but the preconditioner has {d} attributes"
        )
    alpha = preconditioner.orientation_ / preconditioner.log_scale_
    b = -preconditioner.log_offset_ / preconditioner.log_scale_
    beta = float(np.asarray(estimator.log_offset_)[0])
    return {
        "exponents_orig": w * alpha,
        "log_const": float(w @ b - beta),
        "shift": np.array(preconditioner.shift_, dtype=float),
    }

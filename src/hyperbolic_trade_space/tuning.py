"""Temperature selection for the soft-maximum fit (spec section 4, lemma L5)."""

from __future__ import annotations

import warnings

import numpy as np

from .estimator import HyperbolicTradeSpace

__all__ = ["select_temperature"]


def select_temperature(X, target_frac_above=0.10, bounds=(1e-1, 1e4), tol=0.01, **params):
    """Choose the temperature ``tau`` whose fit has a target fraction of designs above V = 1.

    The fitted ``frac_above_`` falls as ``tau`` grows (a harder maximum leaves fewer designs
    beyond the frontier; lemma L5 gives the ``log(n)/tau`` softening). This bisects ``log tau``
    on ``bounds`` (at most 60 iterations) until ``|frac_above_ - target_frac_above| <= tol``.
    Monotonicity is assumed and checked at the bracket ends.

    Parameters
    ----------
    X : array-like of shape (n_samples, n_features)
        Strictly positive larger-is-better metrics (already conditioned).
    target_frac_above : float, default=0.10
        Target fraction of training rows with ``V > 1``, in ``(0, 1)``.
    bounds : tuple of float, default=(1e-1, 1e4)
        ``(low, high)`` search interval for ``tau``, ``0 < low < high``.
    tol : float, default=0.01
        Accepted absolute error of ``frac_above_``.
    **params
        Other :class:`~hyperbolic_trade_space.HyperbolicTradeSpace` parameters
        (``min_exponent``, ``coordinates``, ...); ``temperature`` is not allowed.

    Returns
    -------
    temperature : float
        The selected ``tau``. If ``frac_above_`` is a step function and no ``tau`` is within
        ``tol`` (few samples), the closest one is returned with a ``UserWarning``.

    Raises
    ------
    ValueError
        If the target is not bracketed by the fits at ``bounds``.

    Notes
    -----
    ``tau`` has units of 1 / (log-spread of the metrics), so the answer depends on the
    conditioning of ``X``.

    Examples
    --------
    >>> from hyperbolic_trade_space import HyperbolicTradeSpace, make_frontier_data
    >>> from hyperbolic_trade_space import select_temperature
    >>> X, _ = make_frontier_data(300, 3, noise=0.05, random_state=0)
    >>> tau = select_temperature(X, 0.10)
    >>> est = HyperbolicTradeSpace(temperature=tau).fit(X)
    >>> abs(est.frac_above_ - 0.10) <= 0.01
    True
    """
    if "temperature" in params:
        raise ValueError("temperature is selected, not passed")
    if not 0.0 < target_frac_above < 1.0:
        raise ValueError("target_frac_above must be in (0, 1)")
    lo, hi = float(bounds[0]), float(bounds[1])
    if not 0.0 < lo < hi:
        raise ValueError("bounds must satisfy 0 < low < high")

    def frac(tau):
        return HyperbolicTradeSpace(temperature=tau, **params).fit(X).frac_above_

    f_lo, f_hi = frac(lo), frac(hi)
    if abs(f_lo - target_frac_above) <= tol:
        return lo
    if abs(f_hi - target_frac_above) <= tol:
        return hi
    if not (f_hi < target_frac_above < f_lo):
        raise ValueError(
            f"target frac_above {target_frac_above} is not bracketed by bounds {bounds}: "
            f"frac_above_ is {f_lo:.3f} at tau={lo:g} and {f_hi:.3f} at tau={hi:g}"
        )
    llo, lhi = np.log(lo), np.log(hi)
    best, best_err = lo, abs(f_lo - target_frac_above)
    for _ in range(60):
        mid = 0.5 * (llo + lhi)
        tau = float(np.exp(mid))
        f = frac(tau)
        err = abs(f - target_frac_above)
        if err < best_err:
            best, best_err = tau, err
        if err <= tol:
            return tau
        if f > target_frac_above:
            llo = mid
        else:
            lhi = mid
        if lhi - llo < 1e-12:
            break
    warnings.warn(
        f"no temperature within tol={tol} of the target; closest tau={best:g} "
        f"(error {best_err:.3g})",
        UserWarning,
        stacklevel=2,
    )
    return best

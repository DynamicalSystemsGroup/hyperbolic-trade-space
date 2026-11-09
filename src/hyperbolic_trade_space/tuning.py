"""Temperature selection for the soft-maximum fit."""

from __future__ import annotations

import warnings

import numpy as np

from .estimator import HyperbolicTradeSpace

__all__ = ["select_temperature"]


def select_temperature(X, target_frac_above=0.10, bounds=(1e-1, 1e4), tol=0.01, **params):
    """Choose the temperature ``tau`` whose fit has a target fraction of designs above V = 1.

    For ``tau`` of about 3 and above, the fitted ``frac_above_`` falls as ``tau`` grows (a harder
    maximum leaves fewer designs beyond the frontier; the log-mean-exp is within ``log(n)/tau`` of
    the maximum). It is not monotone for small ``tau``: the log-mean-exp lies between the mean and
    the maximum of the scores and tends to the mean as ``tau -> 0``, so ``frac_above_`` can
    overshoot 0.5 below ``tau`` of about 3 (the project's reading: the soft maximum tends to the
    mean of the scores, not the median) before decreasing toward 0 as ``tau`` grows. ``tau`` below
    about 3 is outside the documented useful range. Bisection only needs the target bracketed by the
    fractions at the ends of ``bounds`` (checked, ``ValueError`` otherwise); it returns a ``tau``
    with ``|frac_above_ - target_frac_above| <= tol`` found in at most 60
    iterations on ``log tau``. Keep ``bounds[0]`` near or above 3 for a unique answer.
    The default ``bounds[0] = 0.1`` is wider than the recommended ``tau`` of about 3 or more:
    bisection tolerates it because it needs only that the target be bracketed by the ends of
    ``bounds`` (``ValueError`` otherwise), but below ``tau`` of about 3 the ``frac_above_``
    response is not monotone, so the returned ``tau`` is a root of the bracket search; callers
    who need the useful range should pass ``bounds=(3, ...)``.

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
        Other ``HyperbolicTradeSpace`` parameters
        (``min_exponent``, ``coordinates``, ...); ``temperature`` is not allowed.

    Returns
    -------
    temperature : float
        The selected ``tau``. If ``frac_above_`` is a step function and no ``tau`` is within
        ``tol`` (few samples), the closest one is returned with a ``UserWarning``.

    Raises
    ------
    ValueError
        If the target is not bracketed by the fits at ``bounds``. The message gives the fractions at
        both ends and what to try (a target within the achieved range, a fixed
        ``temperature``, wider ``bounds``). For ``n_terms > 1`` the facets are not supporting planes
        (rows can lie above them),
        so ``frac_above_`` levels off above zero as ``tau`` grows and the default target 0.10
        may be out of reach.

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
        n_terms = int(params.get("n_terms", 1))
        lo_f, hi_f = min(f_lo, f_hi), max(f_lo, f_hi)
        if target_frac_above <= lo_f:  # the target is below every fraction the interval reaches
            near = hi if f_hi <= f_lo else lo
            if n_terms > 1:
                what = f"raise the target to about {lo_f + 0.02:.2f} or more"
                why = (
                    f"with n_terms={n_terms} the facets are not supporting planes (rows can lie "
                    f"above them), so frac_above_ levels off near {lo_f:.2f} as tau grows"
                )
            else:
                what = "raise the target or raise the upper bound"
                why = "frac_above_ is still above the target at the largest tau"
        else:  # the target is above every fraction the interval reaches
            near = lo if f_lo >= f_hi else hi
            what = f"lower the target to about {hi_f - 0.02:.2f} or less, or lower the lower bound"
            why = "frac_above_ stays below the target over the whole interval"
        raise ValueError(
            f"target frac_above {target_frac_above} is not bracketed by bounds {bounds}: "
            f"frac_above_ is {f_lo:.3f} at tau={lo:g} and {f_hi:.3f} at tau={hi:g} ({why}). "
            f"Try: {what}; or fit at a fixed temperature (the closest end of bounds is "
            f"temperature={near:g}, or select it at n_terms=1 and compare fits with "
            f"mean_slack_); or widen bounds."
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

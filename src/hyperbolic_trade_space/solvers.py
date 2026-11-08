"""Solvers for the entropic soft-maximum fit (numpy and scipy only, no scikit-learn).

The fit minimizes the log-mean-exp objective ``J_tau(w) = (1/tau) log((1/N) sum_i exp(tau w.u_i))``
over the simplex (derivation lemmas L1 to L5, spec section 4). At ``tau = inf`` it is the linear
program ``min_w max_i w.u_i``; at finite ``tau`` it is a smooth convex program solved by SLSQP,
warm-started from the linear program.

Rows with ``-inf`` entries (zero metrics) must be masked by the caller before solving.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from scipy.optimize import linprog, minimize
from scipy.special import logsumexp

__all__ = [
    "SolveResult",
    "log_mean_exp",
    "objective_and_grad",
    "solve_lp",
    "solve_slsqp",
    "support_weights",
]

_TIE_TOL = 1e-12


@dataclass(frozen=True)
class SolveResult:
    """Result of a simplex solve.

    Attributes
    ----------
    w : ndarray of shape (d,)
        Minimizer on the simplex.
    beta : float
        Offset, ``J_tau(w)`` (the log-mean-exp of ``U @ w``).
    p : ndarray of shape (N,)
        Support weights (softmax weights; LP duals at ``tau = inf``). Nonnegative, sum 1.
    objective : float
        Objective value at ``w`` (equal to ``beta``).
    n_iter : int
        Solver iterations (at least 1).
    success : bool
        Whether the solver reported success.
    message : str
        Solver message.
    """

    w: np.ndarray
    beta: float
    p: np.ndarray
    objective: float
    n_iter: int
    success: bool
    message: str


def log_mean_exp(s, tau):
    """Entropic soft maximum ``(1/tau) log mean(exp(tau s))`` (lemmas L1, L5).

    Parameters
    ----------
    s : array-like of shape (N,)
        Scores; ``-inf`` entries contribute weight zero.
    tau : float
        Temperature, ``tau > 0`` or ``np.inf``. At ``np.inf`` the result is ``max(s)``.

    Returns
    -------
    float
        The log-mean-exp, stable for large ``tau * s``.

    Notes
    -----
    Computed as ``logsumexp(tau*s, b=1/N)/tau``; it never exceeds ``max(s)`` and is at least
    ``mean(s)``.

    Examples
    --------
    >>> import numpy as np
    >>> s = np.array([0.0, 1.0, 2.0])
    >>> round(float(log_mean_exp(s, 1.0)), 6)
    1.308994
    >>> float(log_mean_exp(s, np.inf))
    2.0
    >>> round(float(log_mean_exp(s, 1e6)), 4)
    2.0
    """
    s = np.asarray(s, dtype=float)
    if np.isinf(tau):
        return float(np.max(s))
    with np.errstate(invalid="ignore", divide="ignore"):
        return float(logsumexp(tau * s, b=1.0 / s.size) / tau)


def support_weights(s, tau):
    """Softmax support weights ``p_i`` of the scores (lemma L3).

    Parameters
    ----------
    s : array-like of shape (N,)
        Scores.
    tau : float
        Temperature, ``tau > 0`` or ``np.inf``. At ``np.inf`` the weight is uniform over the
        argmax set (ties within relative tolerance 1e-12 are averaged).

    Returns
    -------
    ndarray of shape (N,)
        Nonnegative weights summing to 1.

    Examples
    --------
    >>> import numpy as np
    >>> support_weights(np.array([1.0, 1.0, 0.0]), np.inf).round(3).tolist()
    [0.5, 0.5, 0.0]
    >>> round(float(support_weights(np.array([0.0, 1.0, 2.0]), 2.0).sum()), 12)
    1.0
    """
    s = np.asarray(s, dtype=float)
    if np.isinf(tau):
        m = np.max(s)
        top = np.isclose(s, m, rtol=_TIE_TOL, atol=_TIE_TOL)
        return top / top.sum()
    with np.errstate(invalid="ignore", divide="ignore"):
        ts = tau * s
        p = np.exp(ts - logsumexp(ts))
    return p / p.sum()


def objective_and_grad(w, U, tau):
    """Objective ``J_tau(w)`` and gradient ``U^T p`` (lemma L3).

    Parameters
    ----------
    w : ndarray of shape (d,)
        Exponents.
    U : ndarray of shape (N, d)
        Log metrics (finite).
    tau : float
        Temperature, ``tau > 0`` or ``np.inf`` (then the gradient is a subgradient).

    Returns
    -------
    objective : float
    grad : ndarray of shape (d,)

    Examples
    --------
    >>> import numpy as np
    >>> U = np.array([[0.0, 1.0], [1.0, 0.0]])
    >>> f, g = objective_and_grad(np.array([0.5, 0.5]), U, 5.0)
    >>> round(f, 4), g.round(4).tolist()
    (0.5, [0.5, 0.5])
    """
    s = U @ w
    p = support_weights(s, tau)
    return log_mean_exp(s, tau), U.T @ p


def solve_lp(U, min_exponent=0.0):
    """Solve ``min t  s.t.  U w <= t 1, sum w = 1, w >= min_exponent`` (the ``tau = inf`` fit).

    Parameters
    ----------
    U : ndarray of shape (N, d)
        Log metrics (finite).
    min_exponent : float, default=0.0
        Lower bound on every exponent, in ``[0, 1/d)``.

    Returns
    -------
    SolveResult
        ``beta = t = max_i w.u_i``; ``p`` are the LP duals of the ``N`` inequality constraints
        (sign and scale fixed so they are the support weights; they sum to 1 because the
        cost on ``t`` is 1).

    Examples
    --------
    >>> import numpy as np
    >>> U = np.array([[1.0, 0.0], [0.0, 1.0]])
    >>> r = solve_lp(U)
    >>> r.w.round(6).tolist(), round(r.beta, 6), r.p.round(6).tolist()
    ([0.5, 0.5], 0.5, [0.5, 0.5])
    """
    U = np.asarray(U, dtype=float)
    n, d = U.shape
    c = np.zeros(d + 1)
    c[-1] = 1.0
    A_ub = np.hstack([U, -np.ones((n, 1))])
    A_eq = np.hstack([np.ones((1, d)), np.zeros((1, 1))])
    bounds = [(min_exponent, None)] * d + [(None, None)]
    res = linprog(
        c, A_ub=A_ub, b_ub=np.zeros(n), A_eq=A_eq, b_eq=[1.0], bounds=bounds, method="highs"
    )
    if res.x is None:
        return SolveResult(
            np.full(d, 1.0 / d), float("nan"), np.full(n, 1.0 / n), float("nan"), 1, False,
            str(res.message),
        )  # fmt: skip
    w = np.clip(res.x[:d], min_exponent, None)
    w = w / w.sum()
    p = np.clip(-np.asarray(res.ineqlin.marginals), 0.0, None)
    total = p.sum()
    p = p / total if total > 0 else support_weights(U @ w, np.inf)
    beta = float(np.max(U @ w))
    return SolveResult(
        w, beta, p, beta, max(int(getattr(res, "nit", 1)), 1), bool(res.success), str(res.message)
    )


def solve_slsqp(U, tau, min_exponent=0.0, w0=None, tol=1e-10, max_iter=500):
    """Minimize ``J_tau`` over the simplex by SLSQP with analytic Jacobian.

    Parameters
    ----------
    U : ndarray of shape (N, d)
        Log metrics (finite).
    tau : float
        Temperature, ``tau > 0``. At ``np.inf`` this returns the LP solution.
    min_exponent : float, default=0.0
        Lower bound on every exponent.
    w0 : ndarray of shape (d,), optional
        Start point; defaults to the LP solution (warm start).
    tol : float, default=1e-10
        SLSQP ``ftol``.
    max_iter : int, default=500
        SLSQP ``maxiter``.

    Returns
    -------
    SolveResult
        ``p`` are the softmax weights at the solution.

    Examples
    --------
    >>> import numpy as np
    >>> U = np.array([[1.0, 0.0], [0.0, 1.0], [0.4, 0.4]])
    >>> r = solve_slsqp(U, 50.0)
    >>> r.w.round(3).tolist(), bool(r.success)
    ([0.5, 0.5], True)
    """
    U = np.asarray(U, dtype=float)
    d = U.shape[1]
    if np.isinf(tau):
        return solve_lp(U, min_exponent)
    if w0 is None:
        w0 = solve_lp(U, min_exponent).w
    w0 = np.clip(np.asarray(w0, dtype=float), min_exponent, None)
    w0 = w0 / w0.sum()
    res = minimize(
        objective_and_grad,
        w0,
        args=(U, tau),
        jac=True,
        method="SLSQP",
        bounds=[(min_exponent, 1.0)] * d,
        constraints=[{"type": "eq", "fun": lambda w: w.sum() - 1.0, "jac": lambda w: np.ones(d)}],
        options={"ftol": tol, "maxiter": max_iter},
    )
    w = np.clip(res.x, min_exponent, None)
    w = w / w.sum()
    f, _ = objective_and_grad(w, U, tau)
    f0, _ = objective_and_grad(w0, U, tau)
    if f0 < f:  # never return worse than the warm start
        w, f = w0, f0
    p = support_weights(U @ w, tau)
    return SolveResult(w, f, p, f, max(int(res.nit), 1), bool(res.success), str(res.message))

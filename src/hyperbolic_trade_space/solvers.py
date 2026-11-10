"""Solvers for the entropic soft-maximum fit (numpy and scipy only, no scikit-learn).

The fit minimizes the log-mean-exp objective ``J_tau(w) = (1/tau) log((1/N) sum_i exp(tau w.u_i))``
over the simplex (see the documentation). At ``tau = inf`` it is the linear
program ``min_w max_i w.u_i``; at finite ``tau`` it is a smooth convex program solved by SLSQP,
warm-started from the linear program.

Rows with ``-inf`` entries (zero metrics) must be masked by the caller before solving.
"""

from __future__ import annotations

from dataclasses import dataclass, replace

import numpy as np
from scipy.linalg import block_diag, eigh, null_space
from scipy.optimize import linprog, minimize
from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import connected_components
from scipy.special import logsumexp, softmax
from sklearn.utils import check_random_state

from .coordinates import helmert_basis

__all__ = [
    "DISTINCT_TERMS_DISTANCE",
    "EPS_FEAS",
    "EPS_KKT",
    "GUARD_TOL",
    "POLISH_STEPS",
    "SolveResult",
    "Termination",
    "TermsResult",
    "assignment_margin",
    "distinct_terms",
    "facet_gap",
    "facet_objective",
    "fixed_assignment_bound",
    "log_mean_exp",
    "objective_and_grad",
    "simplex_gap",
    "single_facet_termination",
    "soft_certificate",
    "soft_hessian",
    "soft_objective",
    "soft_weights",
    "solve_lp",
    "solve_slsqp",
    "solve_terms",
    "support_weights",
]

_TIE_TOL = 1e-12
EPS_KKT = 1e-8  # first-order gap tolerance of the stopping declaration
EPS_FEAS = 1e-9  # feasibility and margin-positivity tolerance
GUARD_TOL = 1e-12  # the monotone guard rejects an objective increase above this
POLISH_STEPS = 5  # reduced-Newton steps after each finite-tau facet refit
_ACTIVE_TOL = 1e-10
DISTINCT_TERMS_DISTANCE = 1e-3  # exponent vectors closer than this (Euclidean) are one term
_SOFT_STOP = 1e-10  # the soft alternation stops when the soft objective falls by less than this
_SOFT_EMPTY = 1e-9  # a term whose weight mass is below this (in rows) is empty
_SOFT_POLISH_STEPS = 30  # joint reduced-Newton steps after the soft alternation


@dataclass(frozen=True)
class SolveResult:
    """Result of a simplex solve.

    Parameters
    ----------
    w : ndarray of shape (d,)
        Minimizer on the simplex.
    beta, p, objective, n_iter, success, message
        As in Attributes below; the fields are set once by the solvers and are read-only in use.

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

    Examples
    --------
    >>> import numpy as np
    >>> from hyperbolic_trade_space.solvers import SolveResult
    >>> r = SolveResult(np.array([1.0]), 0.0, np.array([1.0]), 0.0, 1, True, "ok")
    >>> r.success, r.w.tolist()
    (True, [1.0])
    """

    w: np.ndarray
    beta: float
    p: np.ndarray
    objective: float
    n_iter: int
    success: bool
    message: str


def log_mean_exp(s, tau):
    """Entropic soft maximum ``(1/tau) log mean(exp(tau s))``, the log-mean-exp.

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
    """Softmax support weights ``p_i`` of the scores.

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
    """Objective ``J_tau(w)`` and gradient ``U^T p``.

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


def _simplex_min(fun, w0, args, min_exponent, tol, max_iter):
    """SLSQP of ``fun`` (returning value and gradient) over the simplex with a floor."""
    d = w0.size
    return minimize(
        fun,
        w0,
        args=args,
        jac=True,
        method="SLSQP",
        bounds=[(min_exponent, 1.0)] * d,
        constraints=[{"type": "eq", "fun": lambda w: w.sum() - 1.0, "jac": lambda w: np.ones(d)}],
        options={"ftol": tol, "maxiter": max_iter},
    )


def _reweighted(w, U, tau, prev, alpha, eps):
    f, g = objective_and_grad(w, U, tau)
    return f + alpha * np.sum(w / (prev + eps)), g + alpha / (prev + eps)


def solve_slsqp(
    U, tau, min_exponent=0.0, w0=None, tol=1e-10, max_iter=500, penalty=None, alpha=0.0
):
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
    penalty : {None, "reweighted_l1"}, default=None
        Sparsity option. On the simplex the plain L1 norm is constant, so the penalty is the
        reweighted L1 of Candes, Wakin and Boyd (2008): after the unpenalized solve, three rounds
        (``eps = 1e-4``) minimize ``J_tau(w) + alpha * sum_j w_j / (w_prev_j + eps)`` from the
        previous round's solution. Entries below ``1e-8`` are set to exact zero (when
        ``min_exponent == 0``) and ``w`` is renormalized.
    alpha : float, default=0.0
        Penalty weight, ``alpha >= 0``. With ``alpha = 0`` or ``penalty=None`` the result is the
        unpenalized one, by the same code path.

    Returns
    -------
    SolveResult
        ``p`` are the softmax weights at the solution; ``beta`` and ``objective`` are the
        unpenalized ``J_tau`` at the returned ``w`` (so ``beta`` stays the log-mean-exp offset).

    Notes
    -----
    The penalty acts at finite ``tau`` only; at ``tau = inf`` the linear program is returned
    unchanged.

    Examples
    --------
    >>> import numpy as np
    >>> U = np.array([[1.0, 0.0], [0.0, 1.0], [0.4, 0.4]])
    >>> r = solve_slsqp(U, 50.0)
    >>> r.w.round(3).tolist(), bool(r.success)
    ([0.5, 0.5], True)
    """
    U = np.asarray(U, dtype=float)
    if penalty not in (None, "reweighted_l1") or alpha < 0:
        raise ValueError("penalty must be None or 'reweighted_l1' and alpha >= 0")
    if np.isinf(tau):
        return solve_lp(U, min_exponent)
    if w0 is None:
        w0 = solve_lp(U, min_exponent).w
    w0 = np.clip(np.asarray(w0, dtype=float), min_exponent, None)
    w0 = w0 / w0.sum()
    res = _simplex_min(objective_and_grad, w0, (U, tau), min_exponent, tol, max_iter)
    w = np.clip(res.x, min_exponent, None)
    w = w / w.sum()
    f, _ = objective_and_grad(w, U, tau)
    f0, _ = objective_and_grad(w0, U, tau)
    if f0 < f:  # never return worse than the warm start
        w, f = w0, f0
    if penalty == "reweighted_l1" and alpha > 0:
        for _ in range(3):
            r = _simplex_min(_reweighted, w, (U, tau, w, alpha, 1e-4), min_exponent, tol, max_iter)
            w = np.clip(r.x, min_exponent, None)
            w = w / w.sum()
        if min_exponent == 0:
            w = np.where(w < 1e-8, 0.0, w)
            w = w / w.sum()
        f = log_mean_exp(U @ w, tau)
    p = support_weights(U @ w, tau)
    return SolveResult(w, f, p, f, max(int(res.nit), 1), bool(res.success), str(res.message))


def _dual_value(g, min_exponent):
    """``min_{v >= m, 1.v = 1} g.v = m sum(g) + (1 - d m) min(g)``."""
    d = g.size
    return float(min_exponent * g.sum() + (1.0 - d * min_exponent) * g.min())


def simplex_gap(g, w, min_exponent=0.0):
    """First-order gap ``G = g.w - min_{v >= m, 1.v = 1} g.v`` of a convex function on the simplex.

    Parameters
    ----------
    g : ndarray of shape (d,)
        Gradient (or certifying subgradient) at ``w``.
    w : ndarray of shape (d,)
        Feasible point.
    min_exponent : float, default=0.0
        Floor ``m`` on every coordinate, in ``[0, 1/d)``.

    Returns
    -------
    float
        ``g.w - min_j g_j`` for ``m = 0`` (``sum_j w_j (g_j - min g)``, the residual of the
        simplex KKT conditions); for ``m > 0`` the minimizing ``v`` puts ``1 - d m`` on the
        smallest component and ``m`` on the rest. By convexity ``0 <= f(w) - f* <= G``.

    Examples
    --------
    >>> import numpy as np
    >>> g = np.array([0.1, 0.5, 0.9])
    >>> round(simplex_gap(g, np.array([0.5, 0.5, 0.0])), 12)
    0.2
    >>> simplex_gap(g, np.array([1.0, 0.0, 0.0]))
    0.0
    """
    g = np.asarray(g, dtype=float)
    return float(g @ np.asarray(w, dtype=float) - _dual_value(g, min_exponent))


def facet_objective(U, w, ubar, tau):
    """Facet refit objective ``f_k(w) = J_tau(U w) - ubar . w``.

    Parameters
    ----------
    U : ndarray of shape (N, d)
        Log metrics (finite).
    w : ndarray of shape (d,)
        Exponents on the simplex.
    ubar : ndarray of shape (d,)
        Mean log metric of the facet's rows.
    tau : float
        Temperature, ``tau > 0`` or ``np.inf``.

    Returns
    -------
    float

    Examples
    --------
    >>> import numpy as np
    >>> U = np.array([[0.0, 1.0], [1.0, 0.0]])
    >>> round(facet_objective(U, np.array([0.5, 0.5]), U.mean(0), np.inf), 6)
    0.0
    """
    return float(log_mean_exp(U @ w, tau) - np.asarray(ubar) @ w)


def facet_gap(U, w, ubar, tau, min_exponent=0.0, p=None):
    """First-order gap ``G_k`` of the facet refit ``f_k`` at ``w`` (Lemma 1).

    Parameters
    ----------
    U : ndarray of shape (N, d)
        Log metrics (finite).
    w : ndarray of shape (d,)
        Feasible exponents.
    ubar : ndarray of shape (d,)
        Mean log metric of the facet's rows.
    tau : float
        Temperature, ``tau > 0`` or ``np.inf``.
    min_exponent : float, default=0.0
        Floor on every exponent.
    p : ndarray of shape (N,), optional
        Used at ``tau = inf`` only: dual weights (a point of the simplex). Default: the dual of
        the facet's linear program, re-solved. At finite ``tau`` the softmax weights are used.

    Returns
    -------
    float
        Finite ``tau``: ``simplex_gap`` of ``grad f_k = U^T softmax(tau U w) - ubar``.
        ``tau = inf``: ``f_k(w) - min_j (U^T p - ubar)_j`` (with the floor, the dual value of
        ``simplex_gap``), the linear-programming duality gap for the duals ``p``; it is a
        valid bound ``f_k(w) - f_k* <= G_k`` for every ``p`` in the simplex (weak duality), and
        zero at an optimum with the LP duals. Uniform weights on the argmax set
        (``support_weights(U @ w, np.inf)``) give a valid but loose bound.

    Examples
    --------
    >>> import numpy as np
    >>> U = np.array([[1.0, 0.0], [0.0, 1.0]])
    >>> round(facet_gap(U, np.array([0.5, 0.5]), U.mean(0), 5.0), 12)
    0.0
    >>> round(facet_gap(U, np.array([0.5, 0.5]), U.mean(0), np.inf), 12)
    0.0
    """
    U = np.asarray(U, dtype=float)
    w = np.asarray(w, dtype=float)
    ubar = np.asarray(ubar, dtype=float)
    if np.isinf(tau):
        if p is None:
            p = solve_lp(U - ubar, min_exponent).p
        g = U.T @ np.asarray(p) - ubar
        return float(facet_objective(U, w, ubar, tau) - _dual_value(g, min_exponent))
    g = U.T @ support_weights(U @ w, tau) - ubar
    return simplex_gap(g, w, min_exponent)


def assignment_margin(U, W, beta):
    """Assignment margin ``gamma`` and the explicit stable radius (Lemma 2).

    Parameters
    ----------
    U : ndarray of shape (N, d)
        Log metrics.
    W : ndarray of shape (K, d)
        Facet exponents.
    beta : ndarray of shape (K,)
        Facet offsets.

    Returns
    -------
    gamma : float
        ``min_i [s_{i k(i)} - max_{k != k(i)} s_{ik}]`` with ``s = U W^T - beta``: zero when a row
        ties between two facets (for example two identical facets). ``inf`` for ``K = 1``.
    radius : float
        ``gamma / (2 max_i ||(u_i, -1)||_2)``: any perturbation of every ``(w_k, beta_k)`` of
        Euclidean norm below it changes each score by less than ``gamma / 2``, so the
        assignment is unchanged.

    Examples
    --------
    >>> import numpy as np
    >>> U = np.array([[0.0, 0.0], [1.0, 0.0]])
    >>> gamma, radius = assignment_margin(U, np.eye(2), np.array([0.0, 0.5]))
    >>> round(gamma, 6), round(radius, 6)
    (0.5, 0.176777)
    """
    U = np.asarray(U, dtype=float)
    S = U @ np.asarray(W, dtype=float).T - np.asarray(beta, dtype=float)
    if S.shape[1] < 2:
        return float("inf"), float("inf")
    top = np.sort(S, axis=1)[:, -2:]
    gamma = float(np.min(top[:, 1] - top[:, 0]))
    norms = np.sqrt((U**2).sum(axis=1) + 1.0)
    return gamma, gamma / (2.0 * float(norms.max()))


def fixed_assignment_bound(U, W, labels, tau, min_exponent=0.0, P=None):
    """Fixed-assignment objective ``F`` and the Corollary 4 bound ``sum_k |C_k|/N G_k``.

    Parameters
    ----------
    U : ndarray of shape (N, d)
        Log metrics.
    W : ndarray of shape (K, d)
        Facet exponents.
    labels : ndarray of shape (N,), dtype int
        Assignment ``C_k = {i : labels[i] = k}``.
    tau : float
        Temperature.
    min_exponent : float, default=0.0
        Floor on every exponent.
    P : ndarray of shape (K, N), optional
        Dual weights per facet (rows of ``nan`` for an empty facet), used at ``tau = inf``.

    Returns
    -------
    bound : float
        ``sum_k |C_k|/N G_k`` over the nonempty facets: ``F(W) - F*_fixed <= bound``.
    gaps : ndarray of shape (K,)
        ``G_k``, ``nan`` for an empty facet.
    F : float
        ``sum_k |C_k|/N f_k(w_k)``, equal to the mean slack of the returned fit.

    Examples
    --------
    >>> import numpy as np
    >>> U = np.array([[1.0, 0.0], [0.0, 1.0], [1.0, 1.0]])
    >>> W = np.array([[0.5, 0.5]])
    >>> bound, gaps, F = fixed_assignment_bound(
    ...     U, W, np.zeros(3, dtype=int), np.inf)
    >>> round(bound, 6), round(F, 6)
    (0.0, 0.333333)
    """
    U = np.asarray(U, dtype=float)
    N, K = U.shape[0], W.shape[0]
    shares = np.bincount(labels, minlength=K) / N
    gaps, F = np.full(K, np.nan), 0.0
    for k in np.flatnonzero(shares):
        ubar = U[labels == k].mean(axis=0)
        gaps[k] = facet_gap(U, W[k], ubar, tau, min_exponent, None if P is None else P[k])
        F += shares[k] * facet_objective(U, W[k], ubar, tau)
    return float(np.nansum(shares * gaps)), gaps, float(F)


def _newton_polish(Uc, w, tau, min_exponent=0.0, n_steps=POLISH_STEPS):
    """Reduced-Newton steps on the active set of ``J_tau(Uc w)`` over the simplex (finite tau).

    The active set is ``w > m`` (coordinates at the floor are held); each step solves the KKT
    system of the Hessian restricted to it and the equality ``1.step = 0``, then backtracks so
    the objective never increases.
    """
    w = np.asarray(w, dtype=float).copy()
    m = min_exponent
    for _ in range(n_steps):
        p = support_weights(Uc @ w, tau)
        act = w > m + _ACTIVE_TOL
        na = int(act.sum())
        if na < 2:
            break
        Ua = Uc[:, act]
        pa = Ua.T @ p
        H = tau * (Ua.T @ (p[:, None] * Ua) - np.outer(pa, pa))
        KKT = np.block([[H, np.ones((na, 1))], [np.ones((1, na)), np.zeros((1, 1))]])
        sol = np.linalg.lstsq(KKT, np.concatenate([-(Uc.T @ p)[act], [0.0]]), rcond=None)[0]
        step = np.zeros_like(w)
        step[act] = sol[:na]
        f0, t = log_mean_exp(Uc @ w, tau), 1.0
        while t > 1e-6:
            w1 = w + t * step
            w1 = w1 / w1.sum()
            if (w1 >= m).all() and log_mean_exp(Uc @ w1, tau) <= f0 + 1e-15:
                break
            t *= 0.5
        else:
            break
        w = w1
    return w


def distinct_terms(W, distance=DISTINCT_TERMS_DISTANCE):
    """Number of distinct terms: exponent vectors within ``distance`` (Euclidean) count as one.

    Single linkage: two terms are one when a chain of terms, each step at most ``distance`` apart,
    joins them. A requested ``K`` that repeats terms gives a count below ``K``; the offsets
    ``beta_k`` are not compared (a repeated exponent vector is a repeated term).

    Parameters
    ----------
    W : ndarray of shape (K, d)
        Term exponent vectors.
    distance : float, default=DISTINCT_TERMS_DISTANCE
        Distance at or below which two exponent vectors are the same term.

    Returns
    -------
    int
        Between 1 and ``K``.

    Examples
    --------
    >>> import numpy as np
    >>> distinct_terms(np.array([[0.5, 0.5], [0.5, 0.5], [0.9, 0.1]]))
    2
    >>> distinct_terms(np.eye(3))
    3
    """
    W = np.atleast_2d(np.asarray(W, dtype=float))
    gap = np.linalg.norm(W[:, None, :] - W[None, :, :], axis=-1)
    return int(connected_components(csr_matrix(gap <= distance), directed=False)[0])


@dataclass(frozen=True, eq=False)
class Termination:
    """Stopping record of a multi-facet fit: the three levels of guarantee, with tolerances.

    Attributes
    ----------
    status : str
        ``"certified"``: the assignment is fixed (zero assignment changes), the feasibility
        residuals are at most ``eps_feas``, ``max_gap <= eps_kkt``, no facet is empty and the
        margin is positive (``gamma > eps_feas``). ``"stationary_without_margin"``: the same with
        ``gamma <= eps_feas`` (a row ties between facets, for example two identical facets) or an
        empty facet. ``"uncertified"``: the assignment is fixed but a residual or the gap exceeds
        its tolerance. ``"guard_stop"``: an iteration raised the objective by more than
        ``guard_tol`` and the previous state was returned. ``"iteration_cap"``: ``max_iter`` was
        reached. ``"not_applicable"``: ``facet_step="tangent"``, a ``penalty``, or the
        ``K = 1`` / ``d = 1`` / ``N < K`` shortcut, or a soft fit at ``tau = inf``; the gaps are
        then diagnostics.

        A *soft* fit (finite ``term_temperature``, weights in place of labels) has two more
        outcomes and a different meaning of ``"certified"``. ``"certified"``: every term's
        facet gap is at most ``eps_kkt`` and ``min_curvature > eps_feas`` (the second-order
        sufficient condition: a strict local minimizer of the soft objective).
        ``"stationary"``: the gaps hold and ``min_curvature <= eps_feas`` (a saddle or a flat
        direction). ``"uncertified"`` as above (a residual or a gap exceeds its tolerance).
        ``"stationary_without_margin"`` is the label-fit status and never occurs for a soft fit.
    reason : str
        The solver's stop message.
    n_iter : int
        Partition-and-refit iterations of the returned run.
    sum_residual, floor_residual : float
        ``max_k |1.w_k - 1|`` and ``max_k max(0, min_exponent - min_j w_kj)``.
    offset_residual : float
        ``max_k |beta_k - J_tau(U w_k)|`` over the nonempty facets.
    max_gap : float
        ``max_k G_k`` over the nonempty facets.
    bound : float
        Corollary 4: ``sum_k |C_k|/N G_k``, a bound on ``F(W) - F*_fixed`` for the assignment of
        this run (not across restarts).
    objective_change : float
        Absolute change of the objective at the last accepted step (``nan`` with none).
    assignment_changes : int
        Rows whose returned label trails the maximum score under ``(W, beta)`` by more than
        ``EPS_FEAS`` (exact ties are not changes).
    n_empty : int
        Facets with no assigned row (their gap is ``nan`` and their share 0).
    gamma, radius : float
        Assignment margin and the explicit stable radius (``assignment_margin``).
    eps_kkt, eps_feas, guard_tol : float
        The tolerances used (``EPS_KKT``, ``EPS_FEAS``, ``GUARD_TOL``).
    gaps, shares : ndarray of shape (K,)
        Per-facet gap (``nan`` for an empty facet) and row share ``|C_k|/N``.
    min_curvature : float
        Soft fit only (finite ``term_temperature`` with ``facet_step="support"``, unpenalized):
        the smallest eigenvalue of the Hessian ``H = D - kappa M`` of the soft objective on the
        tangent space of the active face (``soft_certificate``). ``nan`` for every other fit.
    n_distinct_terms : int
        Distinct terms of the returned model: the exponent vectors, counted as one when within
        ``DISTINCT_TERMS_DISTANCE`` (``distinct_terms``). Below the requested ``K`` when terms
        repeat, whatever the status; ``-1`` for a record built without the exponents.

    Notes
    -----
    For a soft fit there is no assignment: ``bound``, ``gamma`` and ``radius`` are ``nan``
    (the margin, the stable radius and the fixed-assignment bound are not asserted),
    ``assignment_changes`` is 0, ``shares`` are the terms' weight masses ``n_k / N``, a term with
    weight mass below ``1e-9`` rows counts in ``n_empty`` and its gap is ``nan``, and ``gaps`` are
    the first-order gaps ``G_k`` of the weighted refits.

    Level 3 (Proposition 3, conditional local optimality of the fixed assignment) holds for
    ``facet_step="support"`` (step B), unpenalized, with support offsets
    ``beta_k = J_tau(U w_k)``; under step D or a penalty the gap is a diagnostic. The record
    describes the returned run's own fixed assignment, not the choice among restarts.

    ``gamma`` and ``radius`` are ``nan`` (not ``inf``) at ``K = 1`` and in the degenerate shortcuts.
    The margin is the smallest gap by which a row's facet beats the runner-up; with one facet there
    is no runner-up, so the margin does not exist. ``inf`` would assert a guarantee (no perturbation
    can change an assignment) that was never examined, and a minimum over an empty set is undefined,
    so ``nan`` is the honest value and the documentation says the same.
    """

    status: str
    reason: str
    n_iter: int
    sum_residual: float
    floor_residual: float
    offset_residual: float
    max_gap: float
    bound: float
    objective_change: float
    assignment_changes: int
    n_empty: int
    gamma: float
    radius: float
    eps_kkt: float
    eps_feas: float
    guard_tol: float
    gaps: np.ndarray
    shares: np.ndarray
    min_curvature: float = float("nan")
    n_distinct_terms: int = -1


@dataclass(frozen=True)
class TermsResult:
    """Result of ``solve_terms``.

    Attributes
    ----------
    W : ndarray of shape (K, d)
        Facet exponent vectors on the simplex.
    beta : ndarray of shape (K,)
        Facet offsets ``J_tau(w_k)`` over all rows (each facet is a supporting hyperplane).
    labels : ndarray of shape (N,), dtype int
        Facet of each row (argmax of ``w_k . u - beta_k``); for a soft fit the dominant term, an
        analysis (the fit used weights).
    objective : float
        Mean slack ``(1/N) sum_i (beta_k(i) - w_k(i) . u_i)``; ``beta`` for ``n_terms = 1``; for a
        soft fit the mean slack of the soft model, ``-mean_i Phi_kappa(u_i)``.
    n_iter : int
        Partition-and-refit iterations performed.
    success : bool
        True if the assignment became fixed before ``max_iter``.
    message : str
        Stop reason.
    history : ndarray
        Objective after the initial fit and after each accepted iteration (non-increasing up to
        ``GUARD_TOL``).
    termination : Termination
        Stopping record of the returned run (status, gaps, margin, tolerances).
    """

    W: np.ndarray
    beta: np.ndarray
    labels: np.ndarray
    objective: float
    n_iter: int
    success: bool
    message: str
    history: np.ndarray
    termination: Termination


def _termination(
    U, W, beta, labels, P, tau, min_exponent, n_iter, history, reason, stop, applicable
):
    """Build the ``Termination`` of a run (``stop``: ``"fixed"``, ``"guard"``, ``"cap"``)."""
    N, K = U.shape[0], W.shape[0]
    bound, gaps, _ = fixed_assignment_bound(U, W, labels, tau, min_exponent, P)
    shares = np.bincount(labels, minlength=K) / N
    full = shares > 0
    max_gap = float(np.max(gaps[full])) if full.any() else float("nan")
    S = U @ W.T - beta
    # a label counts as changed only when its score trails the maximum by more than EPS_FEAS;
    # exact ties (a row on two facet planes) resolve differently across platforms
    changes = int((S.max(axis=1) - S[np.arange(N), labels] > EPS_FEAS).sum())
    gamma, radius = assignment_margin(U, W, beta)
    sum_res = float(np.abs(W.sum(axis=1) - 1.0).max())
    floor_res = float(max(0.0, min_exponent - W.min()))
    offs = [abs(beta[k] - log_mean_exp(U @ W[k], tau)) for k in np.flatnonzero(full)]
    hist = np.asarray(history)
    n_empty = int(K - full.sum())
    if not applicable:
        status = "not_applicable"
    elif stop == "cap":
        status = "iteration_cap"
    elif stop == "guard":
        status = "guard_stop"
    elif changes or sum_res > EPS_FEAS or floor_res > EPS_FEAS or not max_gap <= EPS_KKT:
        status = "uncertified"
    elif gamma > EPS_FEAS and n_empty == 0:
        status = "certified"
    else:
        status = "stationary_without_margin"
    return Termination(
        status, reason, int(n_iter), sum_res, floor_res, float(max(offs, default=0.0)), max_gap,
        bound, float(abs(hist[-1] - hist[-2])) if hist.size > 1 else float("nan"), changes,
        n_empty, gamma, radius, EPS_KKT, EPS_FEAS, GUARD_TOL, gaps, shares,
        n_distinct_terms=distinct_terms(W),
    )  # fmt: skip


def single_facet_termination(U, w, beta, p, tau, min_exponent, n_iter, reason, n_terms=1):
    """``"not_applicable"`` record of a single-facet fit (``K = 1`` and the degenerate shortcuts).

    Parameters
    ----------
    U : ndarray of shape (N, d)
        Log metrics (finite).
    w : ndarray of shape (d,)
        Fitted exponents.
    beta : float
        Fitted offset.
    p : ndarray of shape (N,)
        Support weights (LP duals at ``tau = inf``).
    tau, min_exponent : float
        Temperature and floor.
    n_iter : int
        Solver iterations.
    reason : str
        Solver message.
    n_terms : int, default=1
        Requested ``K``; the other ``K - 1`` facets repeat the fit and count as empty.

    Returns
    -------
    Termination
        ``max_gap`` is the first-order gap of ``J_tau(U w)`` itself (read only).

    Examples
    --------
    >>> import numpy as np
    >>> U = np.array([[1.0, 0.0], [0.0, 1.0]])
    >>> t = single_facet_termination(
    ...     U, np.array([0.5, 0.5]), 0.5, np.array([0.5, 0.5]),
    ...     np.inf, 0.0, 1, "ok")
    >>> t.status, round(t.max_gap, 9)
    ('not_applicable', 0.0)
    """
    U = np.asarray(U, dtype=float)
    gap = facet_gap(U, w, np.zeros(U.shape[1]), tau, min_exponent, p)
    gaps = np.full(n_terms, np.nan)
    gaps[0] = gap
    shares = np.zeros(n_terms)
    shares[0] = 1.0
    return Termination(
        "not_applicable", str(reason), int(n_iter), float(abs(np.sum(w) - 1.0)),
        float(max(0.0, min_exponent - np.min(w))),
        float(abs(beta - log_mean_exp(U @ w, tau))), gap, gap, float("nan"), 0, n_terms - 1,
        float("nan"), float("nan"), EPS_KKT, EPS_FEAS, GUARD_TOL, gaps, shares,
        n_distinct_terms=1,
    )  # fmt: skip


def soft_weights(U, W, beta, kappa):
    """Weights ``alpha_ik = softmax_k(kappa * (w_k . u_i - beta_k))`` of the soft several-term fit.

    Parameters
    ----------
    U : ndarray of shape (N, d)
        Log metrics (finite).
    W : ndarray of shape (K, d)
        Term exponents.
    beta : ndarray of shape (K,)
        Term offsets.
    kappa : float
        Term temperature, ``kappa > 0`` (finite).

    Returns
    -------
    ndarray of shape (N, K)
        Nonnegative, each row sums to 1.

    Examples
    --------
    >>> import numpy as np
    >>> U = np.array([[1.0, 0.0], [0.0, 1.0]])
    >>> a = soft_weights(U, np.eye(2), np.zeros(2), 1.0)
    >>> a.round(3).tolist(), a.sum(axis=1).round(6).tolist()
    ([[0.731, 0.269], [0.269, 0.731]], [1.0, 1.0])
    """
    return softmax(kappa * (np.asarray(U) @ np.asarray(W).T - np.asarray(beta)), axis=1)


def aggregation_shift(n_terms, kappa, aggregation="sum"):
    """Constant subtracted from ``Phi_kappa`` by the term aggregation (``log K / kappa`` for mean).

    The weights ``softmax_k(kappa x_k)``, the Hessian and the certificate do not depend on it
    (a constant in ``Phi``), so the minimizers of the two forms coincide.

    Examples
    --------
    >>> round(aggregation_shift(4, 2.0, "mean"), 6), aggregation_shift(4, 2.0, "sum")
    (0.693147, 0.0)
    """
    if aggregation not in ("sum", "mean"):
        raise ValueError(f"aggregation must be 'sum' or 'mean', got {aggregation!r}")
    if aggregation == "sum" or not np.isfinite(kappa):
        return 0.0
    return float(np.log(n_terms) / kappa)


def soft_objective(U, W, beta, kappa, aggregation="sum"):
    """Soft objective ``F = mean_i (-Phi_kappa(u_i))``, the mean slack of the soft model.

    Parameters
    ----------
    U : ndarray of shape (N, d)
        Log metrics (finite).
    W : ndarray of shape (K, d)
        Term exponents.
    beta : ndarray of shape (K,)
        Term offsets.
    kappa : float
        Term temperature, ``kappa > 0`` (finite).
    aggregation : {"sum", "mean"}, default="sum"
        Term aggregation: ``"sum"`` the log-sum-exp over the K terms, ``"mean"`` the log-mean-exp
        (the same minus ``log K / kappa``).

    Returns
    -------
    float
        ``-(1/N) sum_i (1/kappa) log sum_k exp(kappa (w_k . u_i - beta_k))`` for ``"sum"``;
        ``"mean"`` adds ``log K / kappa``.

    Examples
    --------
    >>> import numpy as np
    >>> U = np.array([[1.0, 0.0], [0.0, 1.0]])
    >>> round(soft_objective(U, np.eye(2), np.zeros(2), 1e6), 6)
    -1.0
    """
    S = np.asarray(U) @ np.asarray(W).T - np.asarray(beta)
    shift = aggregation_shift(S.shape[1], kappa, aggregation)
    return float(-np.mean(logsumexp(kappa * S, axis=1)) / kappa + shift)


def soft_hessian(U, W, tau, kappa):
    """Gradient and Hessian ``H = D - kappa M`` of the soft objective in the exponents.

    The offsets are tied to the exponents, ``beta_k = J_tau(U w_k)``. With weights ``alpha``
    (``soft_weights``), support weights ``p_k`` of term ``k``, ``utilde_k = U^T p_k``,
    ``v_ik = u_i - utilde_k`` and ``n_k = sum_i alpha_ik``:

    * gradient of term ``k``: ``(n_k / N) (utilde_k - ubar_k)``, ``ubar_k`` the weighted mean of
      the rows (the gradient of the term's weighted refit, scaled by its weight mass);
    * ``D = blockdiag((n_k / N) tau Cov_{p_k}(u))``, positive semidefinite;
    * ``d' M d = mean_i Var_{k ~ alpha_i}(v_ik . d_k)``, positive semidefinite.

    Parameters
    ----------
    U : ndarray of shape (N, d)
        Log metrics (finite).
    W : ndarray of shape (K, d)
        Term exponents.
    tau : float
        Fit temperature, ``0 < tau < inf``.
    kappa : float
        Term temperature, ``0 < kappa < inf``.

    Returns
    -------
    g : ndarray of shape (K, d)
        Gradient of ``F`` with respect to ``W``.
    D, M : ndarray of shape (K d, K d)
        The two parts; the Hessian is ``D - kappa M`` (term-major order of ``W.ravel()``).

    Examples
    --------
    >>> import numpy as np
    >>> U = np.log(np.array([[1.0, 2.0], [2.0, 1.0], [1.5, 1.5], [1.0, 1.0]]))
    >>> g, D, M = soft_hessian(U, np.array([[0.7, 0.3], [0.3, 0.7]]), 5.0, 3.0)
    >>> g.shape, D.shape, bool(np.allclose(M, M.T))
    ((2, 2), (4, 4), True)
    """
    U = np.asarray(U, dtype=float)
    W = np.asarray(W, dtype=float)
    N, d = U.shape
    K = W.shape[0]
    beta = np.array([log_mean_exp(U @ w, tau) for w in W])
    P = np.array([support_weights(U @ w, tau) for w in W])  # K x N
    ut = P @ U  # K x d
    A = soft_weights(U, W, beta, kappa)
    n = A.sum(axis=0)
    g = (n[:, None] * ut - A.T @ U) / N  # (n_k / N)(utilde_k - ubar_k)
    D = block_diag(
        *[(n[k] / N) * tau * ((U.T * P[k]) @ U - np.outer(ut[k], ut[k])) for k in range(K)]
    )
    V = U[:, None, :] - ut[None, :, :]  # N x K x d
    M = np.zeros((K * d, K * d))
    for k in range(K):
        for q in range(K):
            wgt = A[:, k] * ((k == q) - A[:, q])
            M[k * d : (k + 1) * d, q * d : (q + 1) * d] = (V[:, k, :].T * wgt) @ V[:, q, :] / N
    return g, D, M


def _tangent_basis(W, g, min_exponent, tol=1e-6, eps=1e-7):
    """Orthonormal basis of the tangent space of the active face of the product of simplices.

    Per term, an exponent at its bound whose multiplier ``g_j - nu`` is strictly positive (larger
    than ``eps``) is fixed; every other exponent is free, with the sum of the free changes zero.
    An exponent at its bound with a multiplier of zero is kept free (the conservative choice).
    """
    K, d = W.shape
    m = min_exponent
    blocks = []
    for k in range(K):
        nu = float(g[k] @ (W[k] - m)) / (1.0 - d * m)  # the multiplier of the sum constraint
        free = (W[k] > m + tol) | (g[k] - nu <= eps)
        E = np.eye(d)[:, free]
        blocks.append(E @ null_space(np.ones((1, int(free.sum())))))
    return block_diag(*blocks)


def soft_certificate(U, W, tau, kappa, min_exponent=0.0):
    """Second-order test of a soft fit: the facet gaps and the smallest curvature.

    Parameters
    ----------
    U : ndarray of shape (N, d)
        Log metrics (finite).
    W : ndarray of shape (K, d)
        Term exponents.
    tau, kappa : float
        Fit and term temperatures, both finite and positive.
    min_exponent : float, default=0.0
        Floor on every exponent.

    Returns
    -------
    gap : float
        ``max_k G_k``, the first-order gaps of the terms' weighted refits (terms with weight mass
        below ``1e-9`` rows are left out).
    curvature : float
        Smallest eigenvalue of ``B' (D - kappa M) B``, ``B`` an orthonormal basis of the tangent
        space of the active face (``inf`` if the face is a point). If ``gap`` is within
        ``EPS_KKT`` and the curvature is positive, the point is a strict local minimizer of the
        soft objective (second-order sufficient condition, Nocedal and Wright, chapter 12).

    Examples
    --------
    >>> import numpy as np
    >>> U = np.log(np.array([[1.0, 2.0], [2.0, 1.0], [1.5, 1.5], [1.0, 1.0]]))
    >>> W = np.array([[0.5, 0.5], [0.5, 0.5]])
    >>> gap, curvature = soft_certificate(U, W, 5.0, 2.0)
    >>> bool(gap < 1e-8), bool(np.isfinite(curvature))
    (True, True)
    """
    U = np.asarray(U, dtype=float)
    W = np.asarray(W, dtype=float)
    g, D, M = soft_hessian(U, W, tau, kappa)
    beta = np.array([log_mean_exp(U @ w, tau) for w in W])
    A = soft_weights(U, W, beta, kappa)
    n = A.sum(axis=0)
    gaps = [
        facet_gap(U, W[k], A[:, k] @ U / n[k], tau, min_exponent)
        for k in range(W.shape[0])
        if n[k] >= _SOFT_EMPTY
    ]
    gap = float(max(gaps)) if gaps else float("nan")
    B = _tangent_basis(W, g, min_exponent)
    if B.shape[1] == 0:
        return gap, float("inf")
    return gap, float(eigh(B.T @ (D - kappa * M) @ B, eigvals_only=True)[0])


def _soft_polish(U, W, tau, kappa, min_exponent, n_steps=_SOFT_POLISH_STEPS):
    """Joint reduced-Newton steps on the active face, with the Hessian the certificate tests."""
    W = W.copy()
    for _ in range(n_steps):
        g, D, M = soft_hessian(U, W, tau, kappa)
        B = _tangent_basis(W, g, min_exponent)
        if B.shape[1] == 0:
            break
        Hr, gr = B.T @ (D - kappa * M) @ B, B.T @ g.ravel()
        if np.abs(gr).max() < 1e-13 or eigh(Hr, eigvals_only=True)[0] <= 0:
            break
        step = (B @ np.linalg.solve(Hr, gr)).reshape(W.shape)
        beta = np.array([log_mean_exp(U @ w, tau) for w in W])
        f0, t = soft_objective(U, W, beta, kappa), 1.0
        while t > 1e-6:
            W1 = W - t * step
            b1 = np.array([log_mean_exp(U @ w, tau) for w in W1])
            if (min_exponent <= W1).all() and soft_objective(U, W1, b1, kappa) <= f0 + 1e-15:
                break
            t *= 0.5
        else:
            break
        W = W1
    return W


def _refit_soft(U, A, W, beta, tau, kw):
    """Refit every term with weights ``A``: a supporting hyperplane centred at the weighted mean."""
    W, beta, P = W.copy(), beta.copy(), np.full((W.shape[0], U.shape[0]), np.nan)
    polish = np.isfinite(tau) and not (kw["penalty"] and kw["alpha"] > 0)
    for k in range(W.shape[0]):
        nk = A[:, k].sum()
        if nk < _SOFT_EMPTY:
            P[k] = support_weights(U @ W[k], tau)
            continue
        Uc = U - (A[:, k] @ U) / nk
        r = solve_slsqp(Uc, tau, **kw)
        w, p = r.w, r.p
        if polish:
            w = _newton_polish(Uc, w, tau, kw["min_exponent"])
            p = support_weights(U @ w, tau)
        W[k], beta[k], P[k] = w, log_mean_exp(U @ w, tau), p
    return W, beta, P


def _soft_termination(U, W, beta, P, tau, kappa, min_exponent, n_iter, history, reason, stop, ok):
    """``Termination`` of a soft run (``ok``: the soft certificate applies)."""
    N, K = U.shape[0], W.shape[0]
    A = soft_weights(U, W, beta, kappa)
    n = A.sum(axis=0)
    full = n >= _SOFT_EMPTY
    gaps = np.full(K, np.nan)
    for k in np.flatnonzero(full):
        gaps[k] = facet_gap(U, W[k], A[:, k] @ U / n[k], tau, min_exponent, P[k])
    max_gap = float(np.max(gaps[full])) if full.any() else float("nan")
    sum_res = float(np.abs(W.sum(axis=1) - 1.0).max())
    floor_res = float(max(0.0, min_exponent - W.min()))
    offs = [abs(beta[k] - log_mean_exp(U @ W[k], tau)) for k in np.flatnonzero(full)]
    curvature = float("nan")
    if not ok:
        status = "not_applicable"
    elif stop == "guard":
        status = "guard_stop"
    elif sum_res > EPS_FEAS or floor_res > EPS_FEAS or not max_gap <= EPS_KKT:
        status = "iteration_cap" if stop == "cap" else "uncertified"
    else:  # the first- and second-order tests do not depend on how the point was reached
        _, curvature = soft_certificate(U, W, tau, kappa, min_exponent)
        status = "certified" if curvature > EPS_FEAS else "stationary"
    hist = np.asarray(history)
    return Termination(
        status, reason, int(n_iter), sum_res, floor_res, float(max(offs, default=0.0)), max_gap,
        float("nan"), float(abs(hist[-1] - hist[-2])) if hist.size > 1 else float("nan"), 0,
        int(K - full.sum()), float("nan"), float("nan"), EPS_KKT, EPS_FEAS, GUARD_TOL, gaps,
        n / N, curvature, distinct_terms(W),
    )  # fmt: skip


def _solve_terms_soft(U, K, tau, kappa, seed, max_iter, kw):
    """The several-term fit with weights ``softmax_k(kappa score_ik)`` in place of labels.

    The same start and first refit as ``_solve_terms_once``; then the weights come from the
    current model, each term is refit as the supporting hyperplane centred at its weighted mean
    (the monotone guard watches the soft objective), and a joint Newton polish on the Hessian of
    the soft objective follows the alternation.
    """
    N, d = U.shape
    Z = U @ helmert_basis(d).T
    centers = Z[check_random_state(seed).choice(N, K, replace=False)]
    labels = np.argmin(((Z[:, None] - centers) ** 2).sum(-1), axis=1)
    W, beta = np.full((K, d), 1.0 / d), np.zeros(K)
    W, beta, _, P = _refit(U, labels, W, beta, tau, kw)  # the first refit is hard (step B)
    obj = soft_objective(U, W, beta, kappa)
    history, n_iter, stop, message = [obj], 0, "cap", "max_iter reached"
    while n_iter < max_iter:
        n_iter += 1
        A = soft_weights(U, W, beta, kappa)
        W2, beta2, P2 = _refit_soft(U, A, W, beta, tau, kw)
        obj2 = soft_objective(U, W2, beta2, kappa)
        if obj2 > obj + GUARD_TOL:  # monotone guard on the soft objective: reject, stop
            stop, message = "guard", "no further decrease"
            break
        W, beta, P = W2, beta2, P2
        history.append(obj2)
        done = obj - obj2 < _SOFT_STOP
        obj = obj2
        if done:
            stop, message = "fixed", "soft objective stationary"
            break
    ok = np.isfinite(tau) and kw["penalty"] is None
    if stop != "guard" and ok:
        W2 = _soft_polish(U, W, tau, kappa, kw["min_exponent"])
        beta2 = np.array([log_mean_exp(U @ w, tau) for w in W2])
        obj2 = soft_objective(U, W2, beta2, kappa)
        if obj2 <= obj + GUARD_TOL:
            W, beta, obj = W2, beta2, obj2
            P = np.array([support_weights(U @ w, tau) for w in W])
            history.append(obj)
    term = _soft_termination(
        U, W, beta, P, tau, kappa, kw["min_exponent"], n_iter, history, message, stop, ok
    )
    labels = np.argmax(U @ W.T - beta, axis=1)  # the analysis: the dominant term of each row
    done = stop != "cap" or term.status in ("certified", "stationary")
    if done and stop == "cap":
        message = "max_iter reached; the joint Newton polish met the first-order test"
    return TermsResult(W, beta, labels, obj, n_iter, done, message, np.array(history), term)


def _tls_normal(Uk, w0, min_exponent):
    """Smallest-variance direction of the rows ``Uk`` on the simplex (constrained TLS normal)."""
    S = np.cov(Uk, rowvar=False)
    S = S / max(np.trace(S), 1e-12)
    res = _simplex_min(lambda w: (w @ S @ w, 2 * S @ w), w0, (), min_exponent, 1e-14, 500)
    w = np.clip(res.x, min_exponent, None)
    return w / w.sum()


def _refit(U, labels, W, beta, tau, kw, tangent=False):
    W, beta, P = W.copy(), beta.copy(), np.full((W.shape[0], U.shape[0]), np.nan)
    band = 0.1 if np.isinf(tau) else 1.0 / tau
    # the polish acts on the unpenalized step-B refit at finite tau only
    polish = np.isfinite(tau) and not tangent and not (kw["penalty"] and kw["alpha"] > 0)
    for k in np.unique(labels):
        # centering on the facet's mean makes J_tau(Uc w) = J_tau(U w) - mean_k(U) . w
        Uc = U - U[labels == k].mean(0)
        r = solve_slsqp(Uc, tau, **kw)
        w, p = r.w, r.p  # p: softmax weights, or the LP duals at tau = inf
        if polish:
            w = _newton_polish(Uc, w, tau, kw["min_exponent"])
            p = support_weights(U @ w, tau)
        if tangent:  # rows of the facet within the band of the support plane (step B)
            near = (labels == k) & (log_mean_exp(U @ w, tau) - U @ w < band)
            if near.sum() > U.shape[1]:
                w = _tls_normal(U[near], w, kw["min_exponent"])
                p = support_weights(U @ w, tau)
        W[k], beta[k], P[k] = w, log_mean_exp(U @ w, tau), p
    return W, beta, float(np.mean(beta[labels] - np.sum(W[labels] * U, axis=1))), P


def _solve_terms_once(U, K, tau, seed, max_iter, kw, tangent=False, kappa=np.inf):
    if np.isfinite(kappa) and not tangent:  # weights in place of labels
        return _solve_terms_soft(U, K, tau, kappa, seed, max_iter, kw)
    N, d = U.shape
    Z = U @ helmert_basis(d).T  # frontier positions; the depth direction 1 is projected out
    centers = Z[check_random_state(seed).choice(N, K, replace=False)]
    labels = np.argmin(((Z[:, None] - centers) ** 2).sum(-1), axis=1)
    W, beta = np.full((K, d), 1.0 / d), np.zeros(K)
    W, beta, obj, P = _refit(U, labels, W, beta, tau, kw)  # the first refit is step B
    history, n_iter, stop, message = [obj], 0, "cap", "max_iter reached"
    best = (obj, labels, W, beta, P)
    while n_iter < max_iter:
        n_iter += 1
        new = np.argmax(U @ W.T - beta, axis=1)
        if np.array_equal(new, labels):
            stop, message = "fixed", "assignment fixed"
            break
        W2, beta2, obj2, P2 = _refit(U, new, W, beta, tau, kw, tangent)
        if obj2 > obj + GUARD_TOL and not tangent:  # monotone guard (step B): reject, stop
            stop, message = "guard", "no further decrease"
            break
        labels, W, beta, obj, P = new, W2, beta2, obj2, P2
        history.append(obj)
        best = min(best, (obj, labels, W, beta, P), key=lambda t: t[0])
    if tangent:  # the objective is not monotone under step D: keep the best iterate seen
        obj, labels, W, beta, P = best
    applicable = not tangent and kw["penalty"] is None
    term = _termination(
        U, W, beta, labels, P, tau, kw["min_exponent"], n_iter, history, message, stop, applicable
    )
    return TermsResult(
        W, beta, labels, obj, n_iter, stop != "cap", message, np.array(history), term
    )


def solve_terms(
    U,
    n_terms,
    tau,
    min_exponent=0.0,
    penalty=None,
    alpha=0.0,
    n_restarts=5,
    max_iter=50,
    random_state=None,
    tol=1e-10,
    slsqp_max_iter=500,
    facet_step="support",
    term_temperature=np.inf,
    aggregation="sum",
):
    """Fit ``K`` monomial facets by alternating partition and entropic refit.

    Parameters
    ----------
    U : ndarray of shape (N, d)
        Log metrics (finite).
    n_terms : int
        Number of facets ``K >= 1``.
    tau : float
        Temperature of every facet's fit, ``tau > 0`` or ``np.inf``.
    min_exponent, penalty, alpha, tol
        Passed to ``solve_slsqp`` for every facet.
    n_restarts : int, default=5
        Initializations (seeds drawn from ``random_state``); the lowest objective is kept.
    max_iter : int, default=50
        Maximum partition-and-refit iterations per restart.
    random_state : int, RandomState or None
        Seed.
    slsqp_max_iter : int, default=500
        SLSQP iteration cap per facet fit.
    facet_step : {"support", "tangent"}, default="support"
        Per-facet step. ``"support"`` (step B, below) is the default and the monotone one.
        ``"tangent"`` (step D) replaces ``w_k`` by the smallest-variance direction of the facet's
        near-frontier rows (its own rows within ``1/tau`` of its support plane; ``0.1`` at
        ``tau = inf``), a constrained total-least-squares normal on the simplex, when there are at
        least ``d + 1`` such rows, and keeps step B's ``w_k`` otherwise; ``beta_k`` is the support
        value over all rows in both. The first refit is always step B. ``penalty`` and ``alpha``
        act on step B only. The mean slack is *not* monotone under ``"tangent"`` (the guard is
        applied to ``"support"`` only): the iteration stops at a fixed assignment or ``max_iter``
        and returns the lowest-objective iterate seen, so ``history`` need not be non-increasing.
    term_temperature : float, default=np.inf
        Softness ``kappa`` of the weights. At ``np.inf`` every row has the label of its dominant
        facet (the fit above). Finite ``kappa`` (with ``facet_step="support"``) fits the soft
        model: every row carries the weights ``softmax_k(kappa (w_k . u_i - beta_k))`` on every
        term, the refit of term ``k`` is the supporting hyperplane centred at the *weighted*
        mean of the rows, and the objective is the mean slack of the soft model,
        ``-mean_i Phi_kappa(u_i)`` (``soft_objective``), which the monotone guard watches. The
        alternation is followed by a joint reduced-Newton polish on the Hessian
        ``D - kappa M`` (``soft_hessian``). ``labels`` stay the analysis: the dominant term of
        each row. Read ``kappa`` on the scale of ``tau``; ``kappa`` far below ``tau`` merges facets.
        ``facet_step="tangent"`` ignores ``kappa``.
    aggregation : {"sum", "mean"}, default="sum"
        Term aggregation of the soft model. The fit is carried out on the sum form (the weights,
        Hessian and certificate are the same for both: ``Phi`` differs by the constant
        ``log K / kappa``), and for ``"mean"`` the reported ``objective`` and ``history`` are
        shifted by ``+ log K / kappa``, the mean slack of the log-mean-exp model.

    Returns
    -------
    TermsResult

    Notes
    -----
    Partition-and-refit in the style of the max-affine scheme of Magnani and Boyd (2009).
    Refitting a facet by the plain ``K = 1`` fit (minimize ``J_tau`` on the facet's own rows) is
    ill-posed: the rows of one facet lie in a cone of the Helmert chart that does not enclose the
    origin, so ``w`` tilts to a simplex vertex (checked: the linear program on the true rows of a
    planted ``K = 3``, ``d = 4`` frontier returns vertices, not the planted exponents). The facet
    is therefore fitted as a supporting hyperplane: ``w_k`` minimizes
    ``J_tau(U w) - mean_k(U) . w`` over *all* rows, which is ``solve_slsqp`` on ``U`` centered at
    the facet's mean; ``beta_k = J_tau(U w_k)``. The objective is the mean slack
    ``(1/N) sum_i (beta_{k(i)} - w_{k(i)} . u_i)``, which both steps decrease (refit by convexity,
    reassignment to ``argmax_k (w_k . u - beta_k)`` by the choice of the largest score); a guard
    additionally rejects any iteration whose objective increased and returns the previous state.
    It stops at a fixed assignment or ``max_iter``. For ``K = 1`` (and degenerate input
    ``d = 1``, ``N < K``, where the ``K = 1`` solution is repeated) it returns exactly the
    ``solve_slsqp`` result, with ``objective = beta``.

    Step D (``facet_step="tangent"``) is the evidence-driven alternative measured in the research
    spikes; the objective is not monotone under it (see ``facet_step``). Recovery rate on the
    planted data, ``make_frontier_data(400, 4, n_terms=3, random_state=s)``, ``s = 0..19`` (every
    facet has at least ``d + 1`` frontier rows), estimator defaults, ``random_state=0``, five
    restarts, pass = exponent error below 0.05 after matching and at least 90% of the frontier rows
    on the right facet: ``"support"`` 16/20 at ``tau = inf`` (fails: seeds 1, 3, 8, 16) and 16/20 at
    ``tau = 50`` (fails: 1, 3, 8, 16); ``"tangent"`` 16/20 at ``tau = inf`` (fails: 1, 3, 8, 16)
    and 17/20 at ``tau = 50`` (fails: 1, 3, 16). Seeds 1, 3 and 16 have a facet with only 5 or 6
    frontier rows (``d + 1 = 5``): identifiable, but a thin facet leaves local optima that no
    restart escaped. Seed 8 is a local optimum with a well-populated facet (11 frontier rows).

    Initialization: ``K`` random rows are the centers and every row takes its nearest center in
    the Helmert coordinates ``Z = U B^T``. K-means on the near-frontier rows of the ``K = 1`` fit
    was compared on a planted ``K = 3``, ``d = 4`` frontier (20 seeds, exponents recovered to
    0.05): N=600, half the rows on the frontier, one restart, ``tau = inf``: K-means 19/20,
    random 19/20; N=300, 20% on the frontier, ``tau = 50``, five restarts: K-means 19/20, random
    20/20. Random is as reliable, needs no ``K = 1`` pre-fit and is shorter, so it is the
    default. The result is a local optimum, hence the restarts.

    Examples
    --------
    >>> import numpy as np
    >>> from hyperbolic_trade_space.datasets import make_frontier_data
    >>> U = np.log(make_frontier_data(60, 3, random_state=0)[0])
    >>> r = solve_terms(U, 1, 20.0)
    >>> r.W.shape, r.labels.tolist() == [0] * 60
    ((1, 3), True)
    """
    U = np.asarray(U, dtype=float)
    N, d = U.shape
    K = int(n_terms)
    if facet_step not in ("support", "tangent"):
        raise ValueError(f"facet_step must be 'support' or 'tangent', got {facet_step!r}")
    kw = {
        "min_exponent": min_exponent, "penalty": penalty, "alpha": alpha, "tol": tol,
        "max_iter": slsqp_max_iter,
    }  # fmt: skip
    if K == 1 or d == 1 or N < K:
        r = solve_slsqp(U, tau, **kw)
        term = single_facet_termination(
            U, r.w, r.beta, r.p, tau, min_exponent, r.n_iter, r.message, K
        )
        return TermsResult(
            np.tile(r.w, (K, 1)), np.full(K, r.beta), np.zeros(N, dtype=int), r.beta, r.n_iter,
            r.success, r.message, np.array([r.beta]), term,
        )  # fmt: skip
    seeds = check_random_state(random_state).randint(0, 2**31 - 1, size=n_restarts)
    kappa = float(term_temperature)
    runs = [
        _solve_terms_once(U, K, tau, s, max_iter, kw, facet_step == "tangent", kappa) for s in seeds
    ]
    best = min(runs, key=lambda r: r.objective)
    shift = aggregation_shift(K, kappa, aggregation) if facet_step == "support" else 0.0
    if shift:
        best = replace(best, objective=best.objective + shift, history=best.history + shift)
    return best

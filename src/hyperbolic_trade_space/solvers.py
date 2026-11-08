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
from sklearn.utils import check_random_state

from .coordinates import helmert_basis

__all__ = [
    "SolveResult",
    "TermsResult",
    "log_mean_exp",
    "objective_and_grad",
    "solve_lp",
    "solve_slsqp",
    "solve_terms",
    "support_weights",
]

_TIE_TOL = 1e-12


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


@dataclass(frozen=True)
class TermsResult:
    """Result of :func:`solve_terms`.

    Attributes
    ----------
    W : ndarray of shape (K, d)
        Facet exponent vectors on the simplex.
    beta : ndarray of shape (K,)
        Facet offsets ``J_tau(w_k)`` over all rows (each facet is a supporting hyperplane).
    labels : ndarray of shape (N,), dtype int
        Facet of each row (argmax of ``w_k . u - beta_k``).
    objective : float
        Mean slack ``(1/N) sum_i (beta_k(i) - w_k(i) . u_i)``; ``beta`` for ``n_terms = 1``.
    n_iter : int
        Partition-and-refit iterations performed.
    success : bool
        True if the assignment became fixed before ``max_iter``.
    message : str
        Stop reason.
    history : ndarray
        Objective after the initial fit and after each accepted iteration (non-increasing).
    """

    W: np.ndarray
    beta: np.ndarray
    labels: np.ndarray
    objective: float
    n_iter: int
    success: bool
    message: str
    history: np.ndarray


def _tls_normal(Uk, w0, min_exponent):
    """Smallest-variance direction of the rows ``Uk`` on the simplex (constrained TLS normal)."""
    S = np.cov(Uk, rowvar=False)
    S = S / max(np.trace(S), 1e-12)
    res = _simplex_min(lambda w: (w @ S @ w, 2 * S @ w), w0, (), min_exponent, 1e-14, 500)
    w = np.clip(res.x, min_exponent, None)
    return w / w.sum()


def _refit(U, labels, W, beta, tau, kw, tangent=False):
    W, beta = W.copy(), beta.copy()
    band = 0.1 if np.isinf(tau) else 1.0 / tau
    for k in np.unique(labels):
        # centering on the facet's mean makes J_tau(Uc w) = J_tau(U w) - mean_k(U) . w
        w = solve_slsqp(U - U[labels == k].mean(0), tau, **kw).w
        if tangent:  # rows of the facet within the band of the support plane (step B)
            near = (labels == k) & (log_mean_exp(U @ w, tau) - U @ w < band)
            if near.sum() > U.shape[1]:
                w = _tls_normal(U[near], w, kw["min_exponent"])
        W[k], beta[k] = w, log_mean_exp(U @ w, tau)
    return W, beta, float(np.mean(beta[labels] - np.sum(W[labels] * U, axis=1)))


def _solve_terms_once(U, K, tau, seed, max_iter, kw, tangent=False):
    N, d = U.shape
    Z = U @ helmert_basis(d).T  # frontier positions; the depth direction 1 is projected out
    centers = Z[check_random_state(seed).choice(N, K, replace=False)]
    labels = np.argmin(((Z[:, None] - centers) ** 2).sum(-1), axis=1)
    W, beta = np.full((K, d), 1.0 / d), np.zeros(K)
    W, beta, obj = _refit(U, labels, W, beta, tau, kw)  # the first refit is step B
    history, n_iter, success, message = [obj], 0, False, "max_iter reached"
    best = (obj, labels, W, beta)
    while n_iter < max_iter:
        n_iter += 1
        new = np.argmax(U @ W.T - beta, axis=1)
        if np.array_equal(new, labels):
            success, message = True, "assignment fixed"
            break
        W2, beta2, obj2 = _refit(U, new, W, beta, tau, kw, tangent)
        if obj2 > obj and not tangent:  # monotone guard (step B): reject an increase and stop
            success, message = True, "no further decrease"
            break
        labels, W, beta, obj = new, W2, beta2, obj2
        history.append(obj)
        best = min(best, (obj, labels, W, beta), key=lambda t: t[0])
    if tangent:  # the objective is not monotone under step D: keep the best iterate seen
        obj, labels, W, beta = best
    return TermsResult(W, beta, labels, obj, n_iter, success, message, np.array(history))


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
        Passed to :func:`solve_slsqp` for every facet.
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
    :func:`solve_slsqp` result, with ``objective = beta``.

    Step D (``facet_step="tangent"``) is the evidence-driven alternative measured in the research
    spikes; the objective is not monotone under it (see ``facet_step``). Recovery rate on the
    planted data, ``make_frontier_data(400, 4, n_terms=3, random_state=s)``, ``s = 0..19`` (every
    facet has at least ``d + 1`` frontier rows), estimator defaults, ``random_state=0``, five
    restarts, pass = exponent error below 0.05 after matching and at least 90% of the frontier rows
    on the right facet: ``"support"`` 17/20 at ``tau = inf`` (fails: seeds 1, 3, 16) and 16/20 at
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
        return TermsResult(
            np.tile(r.w, (K, 1)), np.full(K, r.beta), np.zeros(N, dtype=int), r.beta, r.n_iter,
            r.success, r.message, np.array([r.beta]),
        )  # fmt: skip
    seeds = check_random_state(random_state).randint(0, 2**31 - 1, size=n_restarts)
    runs = [_solve_terms_once(U, K, tau, s, max_iter, kw, facet_step == "tangent") for s in seeds]
    return min(runs, key=lambda r: r.objective)

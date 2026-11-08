"""Spike round 2 (throwaway): candidate objectives for the K > 1 alternation, a traced alternation,
and step G (the per-facet step that minimizes O4's facet term).

Reuses round 1's methods.py (steps B, D/E, matching, scoring, initializations) unchanged.
"""

import sys
from pathlib import Path

import numpy as np
from scipy.special import logsumexp

REPO = Path("/Users/z/Documents/GitHub/posynomial-invariant-form")
sys.path.insert(0, str(REPO / "docs/superpowers/notes/spike-facet-refit"))
from methods import band_of, refit_B, support_beta  # noqa: E402

from hyperbolic_trade_space.solvers import _simplex_min, log_mean_exp  # noqa: E402

TOUCH_TOL = 1e-9


def slacks(U, W, beta, labels):
    """slack_i = beta_{k(i)} - w_{k(i)} . u_i for the given labels (any labels, not only argmax)."""
    return beta[labels] - np.sum(W[labels] * U, axis=1)


# --------------------------------------------------------------------------------- objectives
def O0(U, W, beta, labels, tau):
    """Mean slack over all rows (the built objective)."""
    return float(slacks(U, W, beta, labels).mean())


def O1(U, W, beta, labels, tau):
    """Mean slack over the near-frontier rows |slack| < band (band = 1/tau; 0.1 at tau = inf)."""
    s = slacks(U, W, beta, labels)
    m = np.abs(s) < band_of(tau)
    return float(s[m].mean()) if m.any() else np.nan


def T_band(U, W, beta, labels, tau):
    """Touch count: rows with |slack| < band (larger is better)."""
    s = slacks(U, W, beta, labels)
    return int((np.abs(s) < band_of(tau)).sum())


def T_exact(U, W, beta, labels, tau):
    """Exact touches: rows with slack < 1e-9 (larger is better; at finite tau: rows at or above
    the soft frontier)."""
    s = slacks(U, W, beta, labels)
    return int((s < TOUCH_TOL).sum())


def O2(U, W, beta, labels, tau):
    """Support-weighted slack sum_i p_i slack_i, p = softmax(-tau slack) over all rows.

    At tau = inf: p uniform on the rows with slack < 1e-9, so the value is identically 0."""
    s = slacks(U, W, beta, labels)
    if np.isinf(tau):
        top = s < TOUCH_TOL
        return float(s[top].mean()) if top.any() else np.nan
    ls = -tau * s
    p = np.exp(ls - logsumexp(ls))
    return float(p @ s)


def O3(U, W, beta, labels, tau):
    """Entropic soft minimum of the slacks, -(1/tau) log mean exp(-tau slack); at tau = inf it is
    min slack = 0 identically (reported as nan)."""
    if np.isinf(tau):
        return np.nan
    s = slacks(U, W, beta, labels)
    return float(-log_mean_exp(-s, tau))


def O4_terms(U, W, beta, labels, tau):
    """Per facet: J_tau(U w_k) - LME_{i in k}(U w_k) = soft minimum of the facet's own-row slacks
    (zero at tau = inf when the support row is the facet's own, which the argmax guarantees)."""
    K = W.shape[0]
    out = np.full(K, np.nan)
    for k in range(K):
        rows = labels == k
        if not rows.any():
            continue
        s = U @ W[k]
        out[k] = log_mean_exp(s, tau) - log_mean_exp(s[rows], tau)
    return out


def O4(U, W, beta, labels, tau):
    """Sum over facets of O4_terms (nan at tau = inf: identically 0)."""
    if np.isinf(tau):
        return np.nan
    t = O4_terms(U, W, beta, labels, tau)
    return float(np.nansum(t))


def O5(U, W, beta, labels, tau):
    """Own candidate: lexicographic (touch count in the band, then mean slack): -T + 0.1 * O0,
    exact lexicographic while O0 < 10 (always here). Edge first, interior only to break ties."""
    return float(-T_band(U, W, beta, labels, tau) + 0.1 * O0(U, W, beta, labels, tau))


OBJECTIVES = {
    "O0": O0,
    "O1": O1,
    "T": T_band,
    "T0": T_exact,
    "O2": O2,
    "O3": O3,
    "O4": O4,
    "O5": O5,
}
MINIMIZE = {
    "O0": True,
    "O1": True,
    "T": False,
    "T0": False,
    "O2": True,
    "O3": True,
    "O4": True,
    "O5": True,
}


def evaluate_all(U, W, beta, labels, tau):
    return {name: f(U, W, beta, labels, tau) for name, f in OBJECTIVES.items()}


def better(name, a, b, tol=1e-12):
    """True if value a is strictly better than b for objective `name`."""
    if np.isnan(a):
        return False
    if np.isnan(b):
        return True
    return (a < b - tol) if MINIMIZE[name] else (a > b + tol)


def planted_state(U, W_true, tau):
    """The planted partition: planted W, support offsets recomputed, labels by argmax."""
    bt = support_beta(U, W_true, tau)
    labt = np.argmax(U @ W_true.T - bt, axis=1)
    return W_true, bt, labt


# ------------------------------------------------------------------------------------ step G
def _gap_fun(w, U, rows, t):
    """J_t(Uw) - LME_own(Uw) with gradient U^T (p_all - p_own)."""
    s = U @ w
    ts = tau_s = t * s
    la = logsumexp(ts)
    lo = logsumexp(ts[rows])
    p_all = np.exp(ts - la)
    p_own = np.zeros_like(s)
    p_own[rows] = np.exp(tau_s[rows] - lo)
    f = (la - np.log(len(s))) / t - (lo - np.log(rows.sum())) / t
    return f, U.T @ (p_all - p_own)


def make_refit_G(tau_inf_step=10.0):
    def refit_G(U, labels, K, tau, W, beta, it):
        """G. Per facet: min_w J_t(Uw) - LME_own(Uw) (the soft minimum of the facet's own-row
        slacks, O4's term), warm-started from B and accepted only if it improves that term;
        beta_k = support value J_tau(U w_k) over all rows. At tau = inf the step uses
        t = 1/band = 10 for its own objective (the term is flat at tau = inf)."""
        t = tau if np.isfinite(tau) else tau_inf_step
        WB, betaB = refit_B(U, labels, K, tau, W, beta, it)
        W, beta = WB.copy(), betaB.copy()
        for k in range(K):
            rows = labels == k
            if rows.sum() < 2:
                continue
            f0, _ = _gap_fun(WB[k], U, rows, t)
            res = _simplex_min(_gap_fun, WB[k], (U, rows, t), 0.0, 1e-12, 500)
            w = np.clip(res.x, 0, None)
            w = w / w.sum()
            f1, _ = _gap_fun(w, U, rows, t)
            if f1 < f0 - 1e-12:
                W[k], beta[k] = w, log_mean_exp(U @ w, tau)
        return W, beta

    refit_G.__name__ = f"G_t{tau_inf_step:g}"
    return refit_G


# ------------------------------------------------------------------------- traced alternation
def alternate_traced(U, labels0, K, tau, refit, max_iter=50, guard=None, keep_best=None):
    """Round 1's loop with a trace of every objective after each half-step.

    guard: objective name; an iteration whose value of it got worse (after the refit) is rejected
    and the loop stops with the previous state (the built solver's rule, with O0).
    keep_best: objective name; the best iterate along the path (by it) is returned instead of the
    last. Returns (W, beta, labels, converged, n_iter, trace) where trace is a list of dicts with
    keys 'it', 'half' in {'init', 'assign', 'refit'} and the objective values.
    """
    _, d = U.shape
    labels = labels0.copy()
    W, beta = np.full((K, d), 1.0 / d), np.zeros(K)
    W, beta = refit(U, labels, K, tau, W, beta, 0)
    cur = evaluate_all(U, W, beta, labels, tau)
    trace = [dict(it=0, half="init", **cur)]
    best = (W.copy(), beta.copy(), labels.copy(), cur)
    converged, n_iter = False, 0
    for it in range(1, max_iter + 1):
        n_iter = it
        new = np.argmax(U @ W.T - beta, axis=1)
        if np.array_equal(new, labels):
            converged = True
            break
        mid = evaluate_all(U, W, beta, new, tau)
        trace.append(dict(it=it, half="assign", **mid))
        W2, beta2 = refit(U, new, K, tau, W, beta, it)
        nxt = evaluate_all(U, W2, beta2, new, tau)
        trace.append(dict(it=it, half="refit", **nxt))
        if guard is not None and better(guard, cur[guard], nxt[guard]):
            converged = True  # "no further decrease"
            break
        labels, W, beta, cur = new, W2, beta2, nxt
        if keep_best is not None and better(keep_best, cur[keep_best], best[3][keep_best]):
            best = (W.copy(), beta.copy(), labels.copy(), cur)
    if keep_best is not None:
        W, beta, labels, cur = best
    return W, beta, labels, converged, n_iter, trace

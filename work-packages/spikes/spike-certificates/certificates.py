"""Throwaway prototype of the E-1 certificates on top of the built solvers (spike 3).

Nothing here is imported by the package. Run from the repository root with
``uv run python <folder>/<script>.py``.
"""

from __future__ import annotations

from dataclasses import dataclass, asdict

import numpy as np

from hyperbolic_trade_space.solvers import (
    log_mean_exp,
    objective_and_grad,
    solve_lp,
    support_weights,
)


# ----------------------------------------------------------------------------- Lemma 1
def facet_objective(U, w, ubar, tau):
    """f_k(w) = J_tau(U w) - ubar . w."""
    return log_mean_exp(U @ w, tau) - float(ubar @ w)


def facet_gradient(U, w, ubar, tau, p=None):
    """grad f_k(w) = U^T p - ubar.  At tau = inf the LP duals ``p`` must be supplied (a
    certifying subgradient); otherwise p = softmax(tau U w) (L3)."""
    if p is None:
        if np.isinf(tau):
            raise ValueError("tau = inf: pass the LP duals p (a certifying subgradient)")
        p = support_weights(U @ w, tau)
    return U.T @ p - ubar, p


def simplex_gap(g, w, min_exponent=0.0):
    """G = max_{v feasible} g^T (w - v) over {v >= m, 1^T v = 1}.

    m = 0: g^T w - min_j g_j.  m > 0: the minimizing v puts 1 - d m on the argmin and m on
    the rest, so min_v g^T v = m sum(g) + (1 - d m) min(g).
    """
    d = g.size
    m = min_exponent
    gv_min = m * g.sum() + (1.0 - d * m) * g.min()
    return float(g @ w - gv_min)


def facet_gap(U, w, ubar, tau, min_exponent=0.0, p=None):
    """Return (G_k, grad f_k, p) at w for facet with row mean ubar.

    At tau = inf, if p is None the LP on the centred rows is re-solved for its duals (the
    estimator discards them); the gap with LP duals is the LP duality gap.
    """
    U = np.asarray(U, float)
    if np.isinf(tau) and p is None:
        p = solve_lp(U - ubar, min_exponent).p
    g, p = facet_gradient(U, w, ubar, tau, p)
    return simplex_gap(g, w, min_exponent), g, p


def lp_gap_uniform_ties(U, w, ubar, tau=np.inf, min_exponent=0.0):
    """tau = inf gap using support_weights (uniform on the argmax set) instead of LP duals:
    valid (p is supported on the active set so U_c^T p is a subgradient) but not certifying."""
    p = support_weights(U @ w, np.inf)
    g, _ = facet_gradient(U, w, ubar, tau, p)
    return simplex_gap(g, w, min_exponent)


# ----------------------------------------------------------------------------- Lemma 2
def assignment_margin(U, W, beta):
    """gamma = min_i [ s_{i,k(i)} - max_{k != k(i)} s_ik ], s = U W^T - beta; and the radius
    gamma / (2 max_i ||(u_i, -1)||_2).  Returns (gamma, radius, labels, i_argmin)."""
    S = U @ W.T - beta
    order = np.sort(S, axis=1)
    margins = order[:, -1] - order[:, -2]
    i = int(np.argmin(margins))
    gamma = float(margins[i])
    norms = np.sqrt((U**2).sum(1) + 1.0)
    radius = gamma / (2.0 * norms.max())
    return gamma, radius, np.argmax(S, axis=1), i


# ----------------------------------------------------------------------------- Corollary 4
def fixed_assignment_bound(U, W, beta, labels, tau, min_exponent=0.0, p_list=None):
    """sum_k (|C_k|/N) G_k(w_k) with ubar_k over C_k; also returns per-facet gaps, f_k values,
    the fixed-assignment objective F = sum_k (|C_k|/N) f_k(w_k) and the solver's mean slack."""
    N = U.shape[0]
    K = W.shape[0]
    gaps, fvals, shares = np.zeros(K), np.zeros(K), np.zeros(K)
    for k in range(K):
        rows = labels == k
        shares[k] = rows.sum() / N
        if not rows.any():
            gaps[k], fvals[k] = np.nan, np.nan
            continue
        ubar = U[rows].mean(0)
        p = None if p_list is None else p_list[k]
        gaps[k], _, _ = facet_gap(U, W[k], ubar, tau, min_exponent, p)
        fvals[k] = facet_objective(U, W[k], ubar, tau)
    F_fixed = float(np.nansum(shares * fvals))
    mean_slack = float(np.mean(beta[labels] - np.sum(W[labels] * U, axis=1)))
    bound = float(np.nansum(shares * gaps))
    return bound, gaps, fvals, shares, F_fixed, mean_slack


# ----------------------------------------------------------------------------- termination
@dataclass
class Termination:
    reason: str  # solver message
    n_iter: int
    feas_sum: float  # max_k |1^T w_k - 1|
    feas_box: float  # max_k max(0, min_exponent - min_j w_kj)
    offset_resid: float  # max_k |beta_k - J_tau(U w_k)|
    max_gap: float  # max_k G_k over nonempty facets
    bound: float  # Corollary 4 weighted bound
    objective_change: float  # |history[-1] - history[-2]| (nan if one entry)
    assignment_changes: int  # rows whose argmax under (W, beta) differs from returned labels
    n_empty: int  # facets with no assigned row
    gamma: float
    radius: float
    status: str  # certified / stationary_unstable / guard_stop / iteration_cap / uncertified

    def as_dict(self):
        return asdict(self)


def termination_report(U, result, tau, min_exponent=0.0, eps_kkt=1e-6, eps_feas=1e-9):
    """Build the quantities of review 3.1.1 from a TermsResult on log-metrics U."""
    W, beta, labels = result.W, result.beta, result.labels
    K = W.shape[0]
    feas_sum = float(np.abs(W.sum(1) - 1.0).max())
    feas_box = float(np.clip(min_exponent - W.min(1), 0, None).max())
    offset_resid = float(max(abs(beta[k] - log_mean_exp(U @ W[k], tau)) for k in range(K)))
    bound, gaps, fvals, shares, F_fixed, ms = fixed_assignment_bound(
        U, W, beta, labels, tau, min_exponent
    )
    max_gap = float(np.nanmax(gaps))
    gamma, radius, argmax_labels, _ = assignment_margin(U, W, beta)
    changes = int((argmax_labels != labels).sum())
    hist = np.asarray(result.history)
    dobj = float(abs(hist[-1] - hist[-2])) if hist.size > 1 else float("nan")
    n_empty = int((shares == 0).sum())
    feasible = feas_sum <= eps_feas and feas_box <= eps_feas
    if result.message == "max_iter reached":
        status = "iteration_cap"
    elif result.message == "no further decrease":
        status = "guard_stop"
    elif changes == 0 and feasible and max_gap <= eps_kkt and gamma > 0 and n_empty == 0:
        status = "certified"
    elif changes == 0 and feasible and max_gap <= eps_kkt:
        status = "stationary_margin_zero_or_empty"
    else:
        status = "uncertified"
    return Termination(
        result.message, result.n_iter, feas_sum, feas_box, offset_resid, max_gap, bound, dobj,
        changes, n_empty, gamma, radius, status,
    ), gaps, fvals, shares, F_fixed, ms  # fmt: skip

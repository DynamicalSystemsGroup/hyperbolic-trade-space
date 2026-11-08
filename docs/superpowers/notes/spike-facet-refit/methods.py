"""Spike: candidate per-facet refit steps for the K > 1 alternation (throwaway code).

Every candidate is a function ``refit(U, labels, K, tau, W, beta, it) -> (W, beta)`` that, given a
hard assignment, returns facet directions on the simplex and offsets. They all plug into the same
alternation ``alternate`` and start from the same labels.
"""

import inspect

import numpy as np
from scipy.optimize import linear_sum_assignment
from scipy.special import logsumexp
from sklearn.utils import check_random_state

from hyperbolic_trade_space.coordinates import helmert_basis
from hyperbolic_trade_space.solvers import (
    _simplex_min,
    log_mean_exp,
    solve_lp,
    solve_slsqp,
)


def band_of(tau):
    return 0.1 if np.isinf(tau) else 1.0 / tau


def support_beta(U, W, tau):
    return np.array([log_mean_exp(U @ w, tau) for w in W])


# --------------------------------------------------------------------------------------- A
def refit_A(U, labels, K, tau, W, beta, it):
    """A. Approved default: K = 1 fit on the facet's own rows (direction and offset)."""
    W, beta = W.copy(), beta.copy()
    for k in range(K):
        rows = labels == k
        if rows.sum() < 2:
            continue
        r = solve_slsqp(U[rows], tau)
        W[k], beta[k] = r.w, r.beta
    return W, beta


# --------------------------------------------------------------------------------------- B
def refit_B(U, labels, K, tau, W, beta, it):
    """B. Built: supporting hyperplane of all rows tightest (mean slack) on the facet's rows."""
    W, beta = W.copy(), beta.copy()
    for k in range(K):
        rows = labels == k
        if not rows.any():
            continue
        w = solve_slsqp(U - U[rows].mean(0), tau).w
        W[k], beta[k] = w, log_mean_exp(U @ w, tau)
    return W, beta


# --------------------------------------------------------------------------------------- C
def _weighted_lme(w, U, tau, q):
    s = U @ w
    ts = tau * s
    f = logsumexp(ts, b=q) / tau
    p = q * np.exp(ts - logsumexp(ts, b=q))
    return f, U.T @ p


def _refit_weighted(U, Q, K, tau, W, beta):
    """Shared body of C: minimize the q-weighted soft maximum per facet; beta = support value."""
    W, beta = W.copy(), beta.copy()
    for k in range(K):
        q = Q[:, k] / Q[:, k].sum()
        w0 = solve_lp(U).w
        res = _simplex_min(_weighted_lme, w0, (U, tau, q), 0.0, 1e-10, 500)
        w = np.clip(res.x, 0, None)
        W[k] = w / w.sum()
        beta[k] = log_mean_exp(U @ W[k], tau)
    return W, beta


def make_refit_C_hard(eps):
    def refit_C_hard(U, labels, K, tau, W, beta, it):
        """C1. Hard membership with a floor eps on every row (eps = 0 is A; eps -> inf is K = 1)."""
        if np.isinf(tau):
            raise ValueError("C needs finite tau: a weighted max ignores the weights")
        Q = (labels[:, None] == np.arange(K)) + eps
        return _refit_weighted(U, Q.astype(float), K, tau, W, beta)

    refit_C_hard.__name__ = f"C_hard_eps{eps:g}"
    return refit_C_hard


def make_refit_C_soft(kappa_factor, floor):
    def refit_C_soft(U, labels, K, tau, W, beta, it):
        """C2. Soft responsibilities softmax_k(kappa (w_k.u - beta_k)) with a floor."""
        if np.isinf(tau):
            raise ValueError("C needs finite tau")
        if it == 0:  # no planes yet: hard membership
            Q = (labels[:, None] == np.arange(K)).astype(float) + floor
        else:
            S = kappa_factor * tau * (U @ W.T - beta)
            Q = np.exp(S - logsumexp(S, axis=1, keepdims=True)) + floor
        return _refit_weighted(U, Q, K, tau, W, beta)

    refit_C_soft.__name__ = f"C_soft_k{kappa_factor:g}_f{floor:g}"
    return refit_C_soft


# --------------------------------------------------------------------------------------- D
def _tls_normal(Uk, w0, ridge=0.0, w_ref=None):
    """Smallest-variance direction of rows Uk, constrained to the simplex (QP by SLSQP)."""
    S = np.cov(Uk, rowvar=False)
    S = S / max(np.trace(S), 1e-12)
    ref = w0 if w_ref is None else w_ref

    def fun(w, S, ridge, ref):
        return w @ S @ w + ridge * np.sum((w - ref) ** 2), 2 * S @ w + 2 * ridge * (w - ref)

    res = _simplex_min(fun, w0, (S, ridge, ref), 0.0, 1e-14, 500)
    w = np.clip(res.x, 0, None)
    return w / w.sum()


def _near_rows(U, labels, k, W, beta, tau):
    rows = labels == k
    slack = beta[k] - U @ W[k]
    return rows & (slack < band_of(tau))


def refit_D(U, labels, K, tau, W, beta, it):
    """D. Tangent plane of the facet's near-frontier rows; beta = support over all rows.

    The first refit (no planes yet) is B; afterwards near-frontier = own rows within the band of
    the current facet plane. Fewer than d + 1 near rows: fall back to B for that facet.
    """
    d = U.shape[1]
    WB, betaB = refit_B(U, labels, K, tau, W, beta, it)
    if it == 0:
        return WB, betaB
    W, beta = WB.copy(), betaB.copy()
    for k in range(K):
        near = _near_rows(U, labels, k, W, beta, tau)
        if near.sum() < d + 1:
            continue
        w = _tls_normal(U[near], WB[k])
        W[k], beta[k] = w, log_mean_exp(U @ w, tau)
    return W, beta


# --------------------------------------------------------------------------------------- E
def make_refit_E(lam0):
    def refit_E(U, labels, K, tau, W, beta, it):
        """E. D shrunk toward B's direction with weight lam0 / n_near (small facets lean on B)."""
        d = U.shape[1]
        WB, betaB = refit_B(U, labels, K, tau, W, beta, it)
        if it == 0:
            return WB, betaB
        W, beta = WB.copy(), betaB.copy()
        for k in range(K):
            near = _near_rows(U, labels, k, W, beta, tau)
            if near.sum() < d + 1:
                continue
            w = _tls_normal(U[near], WB[k], ridge=lam0 / near.sum(), w_ref=WB[k])
            W[k], beta[k] = w, log_mean_exp(U @ w, tau)
        return W, beta

    refit_E.__name__ = f"E_lam{lam0:g}"
    return refit_E


# --------------------------------------------------------------------------------------- F
class RefitF:
    """F. No direction refit: fixed candidate directions (Dirichlet sample + K = 1 fit), each with
    its support value; a facet takes the candidate that touches (slack < band) most of its rows,
    ties by mean slack on its rows."""

    def __init__(self, n_candidates=4000, seed=0):
        self.M, self.seed, self.cache = n_candidates, seed, None
        self.__name__ = f"F_grid{n_candidates}"

    def _prepare(self, U, tau):
        d = U.shape[1]
        Wc = np.vstack([check_random_state(self.seed).dirichlet(np.ones(d), self.M), solve_lp(U).w])
        S = U @ Wc.T
        bc = np.max(S, axis=0) if np.isinf(tau) else logsumexp(tau * S, axis=0, b=1 / len(U)) / tau
        self.cache = (Wc, bc, bc - S)  # slack matrix N x M, >= 0

    def __call__(self, U, labels, K, tau, W, beta, it):
        if self.cache is None:
            self._prepare(U, tau)
        Wc, bc, slack = self.cache
        W, beta = W.copy(), beta.copy()
        for k in range(K):
            rows = labels == k
            if not rows.any():
                continue
            touches = (slack[rows] < band_of(tau)).sum(0)
            score = touches - slack[rows].mean(0) / (slack[rows].mean(0).max() + 1e-12)
            j = int(np.argmax(score))
            W[k], beta[k] = Wc[j], bc[j]
        return W, beta


# ------------------------------------------------------------------------------ alternation
def alternate(U, labels0, K, tau, refit, max_iter=50):
    """Common loop: refit -> reassign by argmax(w_k.u - beta_k) until fixed."""
    _, d = U.shape
    labels = labels0.copy()
    W, beta = np.full((K, d), 1.0 / d), np.zeros(K)
    W, beta = refit(U, labels, K, tau, W, beta, 0)
    converged, n_iter = False, 0
    for it in range(1, max_iter + 1):
        n_iter = it
        new = np.argmax(U @ W.T - beta, axis=1)
        if np.array_equal(new, labels):
            converged = True
            break
        labels = new
        W, beta = refit(U, labels, K, tau, W, beta, it)
    return W, beta, labels, converged, n_iter


def solver_init(U, K, seed):
    """The built solver's initialization: K random rows as centres in the Helmert chart."""
    N, d = U.shape
    Z = U @ helmert_basis(d).T
    centers = Z[check_random_state(seed).choice(N, K, replace=False)]
    return np.argmin(((Z[:, None] - centers) ** 2).sum(-1), axis=1)


def flipped_init(true_labels, K, frac, seed):
    rng = check_random_state(seed)
    lab = true_labels.copy()
    flip = rng.rand(len(lab)) < frac
    lab[flip] = (lab[flip] + rng.randint(1, K, flip.sum())) % K
    return lab


# ------------------------------------------------------------------------------- evaluation
def match(W, W_true):
    cost = np.abs(W[:, None, :] - W_true[None, :, :]).sum(-1)
    r, c = linear_sum_assignment(cost)
    perm = np.empty(len(W), dtype=int)
    perm[r] = c  # fitted facet r corresponds to planted facet perm[r]
    return perm


def evaluate(U, W, beta, labels, tau, info):
    """Exponent error (max abs after matching), frontier rows right, common mean slack."""
    W_true, facet, mask = info["exponents"], info["facet"], info["frontier_mask"]
    perm = match(W, W_true)
    err = float(np.abs(W - W_true[perm]).max())
    right = float(np.mean(perm[labels[mask]] == facet[mask]))
    bs = support_beta(U, W, tau)
    lab = np.argmax(U @ W.T - bs, axis=1)
    slack = float(np.mean(bs[lab] - np.sum(W[lab] * U, axis=1)))
    return err, right, slack


def code_lines(fn):
    src = inspect.getsource(fn if not isinstance(fn, RefitF) else RefitF)
    lines = [ln for ln in src.splitlines() if ln.strip() and not ln.strip().startswith("#")]
    # strip docstring lines roughly: count lines not inside triple quotes
    out, in_doc = 0, False
    for ln in lines:
        s = ln.strip()
        if s.startswith('"""') or s.startswith('r"""'):
            if s.count('"""') == 2:
                continue
            in_doc = not in_doc
            continue
        if in_doc:
            continue
        out += 1
    return out

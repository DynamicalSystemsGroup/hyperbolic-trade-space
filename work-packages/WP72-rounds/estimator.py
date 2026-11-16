"""WP72 spike: the invariant fit, a two-sided estimator of the posynomial invariant form.

The frontier fit of the package (``HyperbolicTradeSpace``) finds exponents ``w`` on the simplex by a
one-sided loss, the log-mean-exp of the scores ``w . u_i``: the data lie on or below the level set.
The invariant fit uses the same form, ``log V = w . u`` with ``u = log m`` and ``w`` on the simplex,
and a two-sided loss: within groups of rows that share the invariant, the variance of ``log V``.

    minimize    w^T S_W w
    subject to  w >= 0,  1^T w = 1,

with ``S_W`` the pooled within-group scatter of ``U = log M``. With one group, ``S_W`` is the total
covariance and the problem is the long-only minimum-variance portfolio of the log columns.

Because ``w . 1 = 1`` on the simplex (homogeneity, L1), a move of a row along ``1`` (every metric
scaled by one factor) changes ``log V`` by the same amount for every candidate ``w``. Group offsets
that are pure scalings therefore add one constant to the loss and do not move its minimizer; plain
PCA on the pooled table, normalized by ``||v|| = 1`` instead, is pulled off the invariant by them.

Nothing in ``src/`` is changed; the package supplies the chart basis.
"""

from __future__ import annotations

import numpy as np
from scipy.optimize import minimize
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.utils.validation import check_is_fitted, validate_data

from hyperbolic_trade_space.coordinates import helmert_basis

__all__ = [
    "InvariantFit",
    "column_null",
    "pca_minor",
    "simplex_min_variance",
    "two_term_invariant",
    "within_scatter",
]


def within_scatter(U, groups):
    """Pooled within-group scatter ``S_W`` and total scatter ``S_T`` of the rows of ``U``.

    Groups with a single row carry no within-group information and are dropped from ``S_W``.

    Examples
    --------
    >>> U = np.array([[0.0, 1.0], [1.0, 0.0], [2.0, 3.0], [3.0, 2.0]])
    >>> S_W, S_T, n = within_scatter(U, np.array([0, 0, 1, 1]))
    >>> np.round(S_W, 3).tolist(), n
    ([[0.25, -0.25], [-0.25, 0.25]], 4)
    """
    U = np.asarray(U, float)
    groups = np.asarray(groups)
    Uc = np.empty_like(U)
    keep = np.zeros(len(U), bool)
    for g in np.unique(groups):
        idx = groups == g
        if idx.sum() >= 2:
            Uc[idx] = U[idx] - U[idx].mean(axis=0)
            keep[idx] = True
    n = int(keep.sum())
    S_W = Uc[keep].T @ Uc[keep] / max(n, 1)
    T = U - U.mean(axis=0)
    S_T = T.T @ T / len(U)
    return S_W, S_T, n


def simplex_min_variance(S, n_starts=None):
    """Minimize ``w^T S w`` over the probability simplex (a convex quadratic program).

    Solved by SLSQP from the barycentre and every vertex; the best is returned.

    Examples
    --------
    >>> S = np.array([[1.0, -1.0], [-1.0, 1.0]])
    >>> np.round(simplex_min_variance(S), 6).tolist()
    [0.5, 0.5]
    """
    S = np.asarray(S, float)
    d = S.shape[0]
    starts = [np.full(d, 1.0 / d)] + [np.eye(d)[j] for j in range(d)]
    cons = ({"type": "eq", "fun": lambda w: w.sum() - 1.0, "jac": lambda w: np.ones_like(w)},)
    best, best_f = None, np.inf
    for w0 in starts[: n_starts or len(starts)]:
        r = minimize(
            lambda w: w @ S @ w,
            w0,
            jac=lambda w: 2 * S @ w,
            bounds=[(0.0, 1.0)] * d,
            constraints=cons,
            method="SLSQP",
            options={"ftol": 1e-15, "maxiter": 500},
        )
        w = np.clip(r.x, 0, None)
        w = w / w.sum()
        f = w @ S @ w
        if f < best_f:
            best, best_f = w, f
    return best


def pca_minor(S):
    """The smallest-variance direction of ``S``, renormalized to the simplex when its signs allow.

    Returns ``(w, on_simplex)``; ``w`` is the unit eigenvector when its entries have mixed signs.

    Examples
    --------
    >>> w, ok = pca_minor(np.array([[1.0, -0.9], [-0.9, 1.0]]))
    >>> np.round(w, 6).tolist(), ok
    ([0.5, 0.5], True)
    """
    _, vecs = np.linalg.eigh(np.asarray(S, float))
    v = vecs[:, 0]
    if np.all(v >= -1e-12) or np.all(v <= 1e-12):
        v = np.abs(v)
        return v / v.sum(), True
    return v, False


def _cluster_levels(s, n_levels, seed=0):
    """One-dimensional k-means of the levels ``s`` into ``n_levels`` groups (quantile start)."""
    centers = np.quantile(s, (np.arange(n_levels) + 0.5) / n_levels)
    for _ in range(100):
        lab = np.argmin(np.abs(s[:, None] - centers[None, :]), axis=1)
        new = np.array(
            [s[lab == k].mean() if np.any(lab == k) else centers[k] for k in range(n_levels)]
        )
        if np.allclose(new, centers):
            break
        centers = new
    return lab


def _breaks_from_differences(U, w, threshold):
    """Cut an ordered table where ``|w . (u_t - u_{t-1})|`` exceeds ``threshold`` robust scales."""
    dv = np.diff(U @ w)
    scale = 1.4826 * np.median(np.abs(dv - np.median(dv))) + 1e-300
    jump = np.abs(dv) > threshold * scale
    return np.concatenate([[0], np.cumsum(jump)])


class InvariantFit(TransformerMixin, BaseEstimator):
    """Two-sided fit of the invariant form: the monomial with least within-group variance of log V.

    Parameters
    ----------
    fallback : {"order", "levels"}, default="order"
        How groups are found when ``fit`` is not given them. ``"order"``: the rows are in an order
        (time); ``w`` is first fitted to the first differences of ``U`` (a scale move adds the same
        variance to every ``w`` on the simplex), and the rows are cut where ``|Delta log V|``
        exceeds ``break_threshold`` robust scales. ``"levels"``: the values of ``log V`` are
        clustered into ``n_levels`` groups and ``w`` refitted, alternating ``max_iter`` times.
        Clustering the levels manufactures groups of small level spread; compare
        ``within_share_`` with ``column_null``.
    n_levels : int, default=5
        Number of level groups for ``fallback="levels"``.
    break_threshold : float, default=8.0
        Robust-scale multiple that marks a break for ``fallback="order"``.
    max_iter : int, default=20
        Alternations for ``fallback="levels"``.

    Attributes
    ----------
    exponents_ : ndarray of shape (n_features_in_,)
        ``w`` on the simplex.
    group_labels_ : ndarray of shape (n_samples,)
        The groups used (given, or found).
    levels_ : dict
        Mean ``log V`` per group.
    within_var_ : float
        ``w^T S_W w``, the pooled within-group variance of ``log V``.
    within_share_ : float
        ``w^T S_W w / w^T S_T w``: the share of the variance of ``log V`` left within groups
        (0 for an exact invariant whose level differs between groups; 1 when the groups explain
        nothing).
    flatness_ : float
        Within-group standard deviation of ``log V`` along the unit vector ``w / ||w||``, over the
        largest within-group standard deviation along the level set (0 for an exact invariant).
    trade_directions_ : ndarray of shape (d - 1, d)
        Principal directions of the within-group scatter projected on the level set's tangent
        space ``{x : w . x = 0}``, largest variance first, unit length.
    trade_sd_ : ndarray of shape (d - 1,)
        Within-group standard deviation along each trade direction.
    basis_ : ndarray of shape (d - 1, d)
        The chart basis (Helmert), as in the package.

    Examples
    --------
    >>> rng = np.random.default_rng(0)
    >>> z = rng.normal(size=(200, 1)) @ helmert_basis(2)
    >>> g = np.repeat(np.arange(4), 50)
    >>> U = z + (np.array([0.0, 1.0, 2.0, 3.0])[g] - z @ [0.7, 0.3])[:, None]
    >>> fit = InvariantFit().fit(np.exp(U), groups=g)
    >>> np.round(fit.exponents_, 4).tolist(), bool(fit.within_share_ < 1e-8)
    ([0.7, 0.3], True)
    """

    def __init__(self, fallback="order", n_levels=5, break_threshold=8.0, max_iter=20):
        self.fallback = fallback
        self.n_levels = n_levels
        self.break_threshold = break_threshold
        self.max_iter = max_iter

    def _validate(self, X, reset):
        X = validate_data(self, X, reset=reset, dtype=np.float64)
        if np.any(X <= 0):
            raise ValueError("The invariant fit needs strictly positive metrics.")
        return X

    def fit(self, X, y=None, groups=None):
        """Fit ``w`` on a positive table ``X``; ``groups`` labels rows that share the invariant."""
        if self.fallback not in ("order", "levels"):
            raise ValueError("fallback must be 'order' or 'levels'")
        X = self._validate(X, reset=True)
        U = np.log(X)
        d = U.shape[1]
        if groups is not None:
            groups = np.asarray(groups)
            S_W, S_T, _ = within_scatter(U, groups)
            w = simplex_min_variance(S_W)
        elif self.fallback == "order":
            dU = np.diff(U, axis=0)
            w = simplex_min_variance(dU.T @ dU / len(dU))
            for _ in range(3):  # drop the jumps and refit on the swaps alone
                groups = _breaks_from_differences(U, w, self.break_threshold)
                S_W, S_T, _ = within_scatter(U, groups)
                w = simplex_min_variance(S_W)
        else:
            S_W, S_T, _ = within_scatter(U, np.zeros(len(U)))
            w = simplex_min_variance(S_T)
            for _ in range(self.max_iter):
                groups = _cluster_levels(U @ w, self.n_levels)
                S_W, S_T, _ = within_scatter(U, groups)
                w_new = simplex_min_variance(S_W)
                if np.allclose(w_new, w, atol=1e-10):
                    break
                w = w_new
        S_W, S_T, _ = within_scatter(U, groups)
        self.exponents_ = w
        self.group_labels_ = groups
        s = U @ w
        self.levels_ = {g: float(s[groups == g].mean()) for g in np.unique(groups)}
        self.within_var_ = float(w @ S_W @ w)
        tot = float(w @ S_T @ w)
        self.within_share_ = self.within_var_ / tot if tot > 0 else np.nan
        # trades: within-group scatter on the tangent space of the level set
        wh = w / np.linalg.norm(w)
        P = np.eye(d) - np.outer(wh, wh)
        vals, vecs = np.linalg.eigh(P @ S_W @ P)
        order = np.argsort(vals)[::-1][: d - 1]
        self.trade_directions_ = vecs[:, order].T
        self.trade_sd_ = np.sqrt(np.clip(vals[order], 0, None))
        sd_level = np.sqrt(max(wh @ S_W @ wh, 0.0))
        self.flatness_ = sd_level / self.trade_sd_[0] if self.trade_sd_[0] > 0 else np.nan
        self.basis_ = helmert_basis(d)
        return self

    def score_samples(self, X):
        """``log V = w . log m`` (no reach: the level is reported, not offset)."""
        check_is_fitted(self)
        X = self._validate(X, reset=False)
        return np.log(X) @ self.exponents_

    def transform(self, X):
        """The chart ``(Z, log V)`` with the package's Helmert basis."""
        check_is_fitted(self)
        X = self._validate(X, reset=False)
        U = np.log(X)
        return np.column_stack([U @ self.basis_.T, U @ self.exponents_])


def _softmax(a):
    e = np.exp(a - a.max())
    return e / e.sum()


def two_term_invariant(U, groups, kappa=1.0, n_restarts=20, random_state=0):
    """K = 2: the posynomial ``Phi = (1/kappa) log(e^{kappa w1.u} + e^{kappa (w2.u + b)})``.

    Minimizes the pooled within-group variance of ``Phi`` over ``w1, w2`` on the simplex (softmax
    parameters) and ``b``; nonconvex, so the best of ``n_restarts`` BFGS runs is returned. The two
    terms are unordered: the result is sorted by the first exponent of each term.

    Returns ``(W, b, within_var)``.
    """
    U = np.asarray(U, float)
    groups = np.asarray(groups)
    d = U.shape[1]
    rng = np.random.default_rng(random_state)
    ids = [np.flatnonzero(groups == g) for g in np.unique(groups)]
    ids = [i for i in ids if len(i) >= 2]

    def phi(p):
        w1, w2, b = _softmax(p[:d]), _softmax(p[d : 2 * d]), p[-1]
        return np.logaddexp(kappa * U @ w1, kappa * (U @ w2 + b)) / kappa

    def loss(p):
        f = phi(p)
        return sum(((f[i] - f[i].mean()) ** 2).sum() for i in ids) / sum(len(i) for i in ids)

    best = None
    for _ in range(n_restarts):
        p0 = np.concatenate([rng.normal(scale=2, size=2 * d), [rng.normal()]])
        r = minimize(loss, p0, method="BFGS", options={"gtol": 1e-12, "maxiter": 5000})
        if best is None or r.fun < best.fun:
            best = r
    W = np.vstack([_softmax(best.x[:d]), _softmax(best.x[d : 2 * d])])
    b = best.x[-1]
    if W[0, 0] < W[1, 0]:  # order the terms; swapping them flips the sign of b
        W, b = W[::-1], -b
    return W, b, float(best.fun)


def column_null(X, estimator, n_perm=20, random_state=0, **fit_params):
    """``within_share_`` of ``estimator`` refitted on tables with independently permuted columns.

    The permutation destroys any dependence among the metrics, so a found invariant whose
    ``within_share_`` is no smaller than the null's is not evidence of conservation.
    """
    rng = np.random.default_rng(random_state)
    X = np.asarray(X, float)
    out = []
    for _ in range(n_perm):
        Xp = np.column_stack([rng.permutation(X[:, j]) for j in range(X.shape[1])])
        out.append(estimator.fit(Xp, **fit_params).within_share_)
    return np.array(out)

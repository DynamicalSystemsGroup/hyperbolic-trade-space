"""Synthetic frontier data with a planted monomial frontier (spec section 5)."""

from __future__ import annotations

import numpy as np
from sklearn.utils import check_random_state

from .coordinates import from_frontier_coordinates, helmert_basis

__all__ = ["make_configured_frontier_data", "make_frontier_data"]


def _planted_exponents(exponents, d, rng):
    if exponents is None:
        # bounded away from the boundary: every w_j >= 0.5/d
        return 0.5 * rng.dirichlet(np.ones(d)) + 0.5 / d
    w = np.asarray(exponents, dtype=float)
    if w.shape != (d,) or np.any(w < 0) or abs(w.sum() - 1.0) > 1e-9:
        raise ValueError("exponents must be a nonnegative vector of length n_features summing to 1")
    return w


def _planted_terms(exponents, n_terms, d, rng, min_apart=0.3, tries=1000):
    if exponents is not None:
        W = np.asarray(exponents, dtype=float)
        if W.shape != (n_terms, d) or np.any(W < 0) or not np.allclose(W.sum(axis=1), 1.0):
            raise ValueError(
                "exponents must be (n_terms, n_features), nonnegative, rows summing to 1"
            )
        return W
    for _ in range(tries):
        W = rng.dirichlet(np.ones(d), n_terms)
        if np.abs(W[:, None] - W[None]).sum(-1)[np.triu_indices(n_terms, 1)].min() >= min_apart:
            return W
    raise ValueError(f"no {n_terms} exponent vectors {min_apart} apart (L1) found in d={d}")


def _frontier_mask(n, fraction, rng):
    if not 0.0 < fraction <= 1.0:
        raise ValueError("frontier_fraction must be in (0, 1]")
    mask = np.zeros(n, dtype=bool)
    mask[rng.permutation(n)[: max(1, round(fraction * n))]] = True
    return mask


def _identifiable(mask, facet, log_v, noise, d, rng):
    """Put at least ``d + 1`` frontier rows on every planted facet (extra rows, drawn from rng)."""
    for k in range(int(facet.max()) + 1):
        own = facet == k
        extra = np.flatnonzero(own & ~mask)
        need = d + 1 - int((own & mask).sum())
        if need > 0:
            if need > extra.size:
                raise ValueError(
                    f"facet {k} has {own.sum()} rows, fewer than n_features + 1 = {d + 1}; "
                    "increase n_samples"
                )
            pick = rng.permutation(extra)[:need]
            mask[pick] = True
            log_v[pick] = noise * rng.standard_normal(need)


def make_frontier_data(
    n_samples,
    n_features,
    exponents=None,
    log_offset=0.0,
    frontier_fraction=0.3,
    interior_scale=1.0,
    noise=0.0,
    random_state=None,
    n_terms=1,
):
    """Sample metrics around a planted monomial frontier ``prod m_j^{w_j} = e^{beta}``.

    Parameters
    ----------
    n_samples : int
        Number of rows.
    n_features : int
        Number of metrics ``d`` (``d = 1`` gives a single column and no ``Z``).
    exponents : array-like of shape (n_features,) or (n_terms, n_features), optional
        Planted exponents on the simplex (one row per term for ``n_terms > 1``). Default for
        ``n_terms = 1``: a seeded random point with every ``w_j >= 0.5/d``. Default for
        ``n_terms = K > 1``: K Dirichlet(1) draws, redrawn (at most 1000 tries, then
        ``ValueError``) until every pair is at least 0.3 apart in L1.
    log_offset : float, default=0.0
        Planted ``beta``.
    frontier_fraction : float, default=0.3
        Fraction of rows placed on the frontier (``log V`` equal to ``noise * N(0,1)``).
    interior_scale : float, default=1.0
        Interior rows have ``log V = -Exp(interior_scale)`` (mean depth ``interior_scale``).
    noise : float, default=0.0
        Standard deviation of the log-V noise of frontier rows.
    random_state : int, RandomState or None, default=None
        Seed.
    n_terms : int, default=1
        Number of planted monomials K. ``1`` reproduces the single-facet frontier exactly; ``K > 1``
        plants the envelope ``Phi(u) = max_k (w_k . u - beta)`` and puts ``log V = Phi(u)``.

    Returns
    -------
    X : ndarray of shape (n_samples, n_features)
        Strictly positive metrics.
    info : dict
        Keys ``exponents`` (shape ``(d,)`` at K = 1, ``(K, d)`` otherwise), ``log_offset``,
        ``basis`` (ILR chart), ``frontier_mask``, ``Z``, ``log_v``, ``noise``, ``interior_scale``;
        for ``n_terms > 1`` also ``facet``, an integer array of shape ``(n_samples,)`` holding
        ``argmax_k w_k . log x`` (the facet each row lies on or under).

    Notes
    -----
    For ``n_terms > 1`` every planted facet gets at least ``n_features + 1`` frontier rows
    (identifiability: a facet with fewer frontier rows than dimensions is not determined by them).
    If a facet falls short after the draw, further rows of that facet, chosen by the seeded
    generator, are moved onto the frontier (so the frontier fraction can slightly exceed
    ``frontier_fraction``); a facet with too few rows overall raises ``ValueError``.

    ``Z ~ N(0, I)`` and the rows are mapped back through the ILR chart (lemma L8); the frontier is
    identifiable when the Z-hull of the frontier rows contains 0 (spec section 4). For K > 1 the
    rows are ``u = C Z + s 1`` with ``s = log V + beta - max_k w_k . C Z`` (the K-term form of
    ``from_frontier_coordinates``; ``sum w_k = 1`` makes ``Phi(u) = log V`` exact).

    Examples
    --------
    >>> X, info = make_frontier_data(200, 3, random_state=0)
    >>> X.shape, bool((X > 0).all()), round(float(info["exponents"].sum()), 6)
    ((200, 3), True, 1.0)
    >>> X, info = make_frontier_data(200, 4, n_terms=3, random_state=0)
    >>> info["exponents"].shape, int(info["facet"].max()) < 3
    ((3, 4), True)
    """
    if n_samples < 1 or n_features < 1 or n_terms < 1:
        raise ValueError("n_samples, n_features and n_terms must be >= 1")
    if noise < 0 or interior_scale <= 0:
        raise ValueError("noise must be >= 0 and interior_scale > 0")
    rng = check_random_state(random_state)
    d = int(n_features)
    if n_terms == 1:
        w = _planted_exponents(exponents, d, rng)
    else:
        w = _planted_terms(exponents, n_terms, d, rng)
    B = helmert_basis(d)
    mask = _frontier_mask(n_samples, frontier_fraction, rng)
    Z = rng.standard_normal((n_samples, d - 1))
    log_v = np.where(
        mask,
        noise * rng.standard_normal(n_samples),
        -rng.exponential(interior_scale, n_samples),
    )
    if n_terms == 1:
        U = from_frontier_coordinates(Z, log_v, w, log_offset, B)
    else:
        base = Z @ np.linalg.pinv(B).T
        facet, top = (base @ w.T).argmax(axis=1), (base @ w.T).max(axis=1)
        _identifiable(mask, facet, log_v, noise, d, rng)
        U = base + (log_v + log_offset - top)[:, None]
    X = np.exp(U)
    info = {
        "exponents": w,
        "log_offset": float(log_offset),
        "basis": B,
        "frontier_mask": mask,
        "Z": Z,
        "log_v": log_v,
        "noise": float(noise),
        "interior_scale": float(interior_scale),
    }
    if n_terms > 1:
        info["facet"] = facet
    return X, info


def make_configured_frontier_data(
    n_samples,
    n_features,
    n_config,
    exponents=None,
    log_offset=0.0,
    frontier_fraction=0.3,
    interior_scale=1.0,
    nonlinearity=0.1,
    noise=0.0,
    random_state=None,
):
    """Frontier data whose metrics are a known smooth map of a configuration.

    Parameters
    ----------
    n_samples, n_features : int
        Rows and metrics ``d``.
    n_config : int
        Number of configuration variables, ``>= 2``.
    exponents, log_offset, frontier_fraction, noise, random_state :
        As in :func:`make_frontier_data`.
    interior_scale : float, default=1.0
        Depth scale: ``log V = -interior_scale * (c . g)^2`` for a fixed unit vector ``g``;
        frontier rows are projected onto ``c . g = 0`` so they lie exactly on the frontier.
    nonlinearity : float, default=0.1
        Amplitude of the nonlinear term in ``Z(c) = c A + nonlinearity * sin(c A2)``.

    Returns
    -------
    X_config : ndarray of shape (n_samples, n_config)
        Configurations ``c ~ N(0, I)`` (frontier rows projected).
    Y_metrics : ndarray of shape (n_samples, n_features)
        Strictly positive metrics ``exp(from_frontier_coordinates(Z(c), log V(c) + noise))``.
    info : dict
        As in :func:`make_frontier_data` (without noise-free redundancy), plus ``config_map``: a
        callable ``c -> (Z, log_v)`` giving the noise-free truth for any configuration, and
        ``Z``, ``log_v`` of the training rows (noise included in ``log_v`` for frontier rows).

    Examples
    --------
    >>> C, Y, info = make_configured_frontier_data(100, 3, 4, random_state=1)
    >>> C.shape, Y.shape, bool((Y > 0).all())
    ((100, 4), (100, 3), True)
    >>> Z, lv = info["config_map"](C)
    >>> bool(abs(lv[info["frontier_mask"]]).max() < 1e-12)
    True
    """
    if n_samples < 1 or n_features < 1:
        raise ValueError("n_samples and n_features must be >= 1")
    if n_config < 2:
        raise ValueError("n_config must be >= 2")
    if noise < 0 or interior_scale <= 0:
        raise ValueError("noise must be >= 0 and interior_scale > 0")
    rng = check_random_state(random_state)
    d, k = int(n_features), int(n_config)
    w = _planted_exponents(exponents, d, rng)
    B = helmert_basis(d)
    mask = _frontier_mask(n_samples, frontier_fraction, rng)
    g = rng.standard_normal(k)
    g /= np.linalg.norm(g)
    A = rng.standard_normal((k, d - 1))
    A2 = rng.standard_normal((k, d - 1))
    C = rng.standard_normal((n_samples, k))
    C[mask] -= np.outer(C[mask] @ g, g)

    def config_map(c):
        c = np.atleast_2d(np.asarray(c, dtype=float))
        return c @ A + nonlinearity * np.sin(c @ A2), -interior_scale * (c @ g) ** 2

    Z, log_v = config_map(C)
    log_v = log_v + np.where(mask, noise * rng.standard_normal(n_samples), 0.0)
    Y = np.exp(from_frontier_coordinates(Z, log_v, w, log_offset, B))
    info = {
        "exponents": w,
        "log_offset": float(log_offset),
        "basis": B,
        "frontier_mask": mask,
        "Z": Z,
        "log_v": log_v,
        "noise": float(noise),
        "interior_scale": float(interior_scale),
        "config_map": config_map,
    }
    return C, Y, info

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


def _frontier_mask(n, fraction, rng):
    if not 0.0 < fraction <= 1.0:
        raise ValueError("frontier_fraction must be in (0, 1]")
    mask = np.zeros(n, dtype=bool)
    mask[rng.permutation(n)[: max(1, round(fraction * n))]] = True
    return mask


def make_frontier_data(
    n_samples,
    n_features,
    exponents=None,
    log_offset=0.0,
    frontier_fraction=0.3,
    interior_scale=1.0,
    noise=0.0,
    random_state=None,
):
    """Sample metrics around a planted monomial frontier ``prod m_j^{w_j} = e^{beta}``.

    Parameters
    ----------
    n_samples : int
        Number of rows.
    n_features : int
        Number of metrics ``d`` (``d = 1`` gives a single column and no ``Z``).
    exponents : array-like of shape (n_features,), optional
        Planted exponents on the simplex; default a seeded random point with every
        ``w_j >= 0.5/d``.
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

    Returns
    -------
    X : ndarray of shape (n_samples, n_features)
        Strictly positive metrics.
    info : dict
        Keys ``exponents``, ``log_offset``, ``basis`` (ILR chart), ``frontier_mask``, ``Z``,
        ``log_v``, ``noise``, ``interior_scale``.

    Notes
    -----
    ``Z ~ N(0, I)`` and the rows are mapped back through the ILR chart (lemma L8); the frontier is
    identifiable when the Z-hull of the frontier rows contains 0 (spec section 4).

    Examples
    --------
    >>> X, info = make_frontier_data(200, 3, random_state=0)
    >>> X.shape, bool((X > 0).all()), round(float(info["exponents"].sum()), 6)
    ((200, 3), True, 1.0)
    """
    if n_samples < 1 or n_features < 1:
        raise ValueError("n_samples and n_features must be >= 1")
    if noise < 0 or interior_scale <= 0:
        raise ValueError("noise must be >= 0 and interior_scale > 0")
    rng = check_random_state(random_state)
    d = int(n_features)
    w = _planted_exponents(exponents, d, rng)
    B = helmert_basis(d)
    mask = _frontier_mask(n_samples, frontier_fraction, rng)
    Z = rng.standard_normal((n_samples, d - 1))
    log_v = np.where(
        mask,
        noise * rng.standard_normal(n_samples),
        -rng.exponential(interior_scale, n_samples),
    )
    X = np.exp(from_frontier_coordinates(Z, log_v, w, log_offset, B))
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

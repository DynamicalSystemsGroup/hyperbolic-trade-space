"""Gap and white-space tools on the learned chart (stage 4 of the method).

The chart coordinates ``Z`` (``d - 1`` log ratios) are blind to the common scale of the
metrics, so a *gap* in ``Z`` is a ratio profile no design has explored, whatever its quality. These
functions find such gaps (``knn_gap_scores``, ``find_holes``), place frontier targets over
them (``frontier_targets``, using ``V = 1`` and the inverse chart, and the pull-back
to attributes through a preconditioner when one is given), and orient the near-frontier spread
(``orient_by_pca``, shared with ``hyperbolic_trade_space.tensions.tension_report``).
"""

from __future__ import annotations

import numpy as np
from scipy.spatial import Delaunay, cKDTree

__all__ = ["find_holes", "frontier_targets", "knn_gap_scores", "orient_by_pca"]


def _as_2d(Z, name="Z"):
    Z = np.asarray(Z, dtype=float)
    if Z.ndim == 1:
        Z = Z[:, None]
    if Z.ndim != 2:
        raise ValueError(f"{name} must be 2-D, got shape {Z.shape}")
    return Z


def knn_gap_scores(Z, k=5):
    """Isolation score of each point: mean distance to its ``k`` nearest neighbours.

    Parameters
    ----------
    Z : array-like of shape (n_points, n_coords)
        Chart coordinates.
    k : int, default=5
        Number of neighbours, ``1 <= k < n_points``.

    Returns
    -------
    ndarray of shape (n_points,)
        Mean neighbour distance divided by its median over the points (median score = 1);
        large values flag points sitting beside a gap.

    Examples
    --------
    >>> import numpy as np
    >>> rng = np.random.default_rng(0)
    >>> Z = np.vstack([rng.normal(size=(100, 2)), [[10.0, 10.0]]])
    >>> s = knn_gap_scores(Z, k=5)
    >>> int(np.argmax(s)), bool(s[-1] > 5)
    (100, True)
    """
    Z = _as_2d(Z)
    if not (isinstance(k, (int, np.integer)) and 1 <= k < Z.shape[0]):
        raise ValueError(f"k must be an integer in [1, n_points - 1], got {k!r}")
    dist, _ = cKDTree(Z).query(Z, k=k + 1)
    mean = dist[:, 1:].mean(axis=1)
    med = np.median(mean)
    return mean / med if med > 0 else mean


def find_holes(Z, resolution=50, threshold=2.0):
    """Grid cells inside the data's hull that lie far from every data point.

    Parameters
    ----------
    Z : array-like of shape (n_points, p)
        Chart coordinates with ``p = d - 1`` in {1, 2, 3}.
    resolution : int, default=50
        Grid points per axis over the bounding box.
    threshold : float, default=2.0
        A grid point is a hole when its distance to the nearest data point exceeds ``threshold``
        times the median nearest-neighbour distance among the data points.

    Returns
    -------
    points : ndarray of shape (n_holes, p)
        Hole grid points, most isolated first.
    scores : ndarray of shape (n_holes,)
        Their distance to the nearest data point over the median nearest-neighbour distance.

    Raises
    ------
    ValueError
        If ``p`` is not 1, 2 or 3.

    Notes
    -----
    The hull restriction uses ``scipy.spatial.Delaunay.find_simplex`` (an interval for ``p = 1``),
    so empty space outside the explored region is not reported as a hole.

    Examples
    --------
    >>> import numpy as np
    >>> rng = np.random.default_rng(0)
    >>> Z = rng.uniform(-3, 3, size=(2000, 2))
    >>> Z = Z[np.linalg.norm(Z - [1.0, 0.0], axis=1) > 1.0]
    >>> pts, sc = find_holes(Z, resolution=40, threshold=3.0)
    >>> bool(np.linalg.norm(pts[0] - [1.0, 0.0]) < 0.5)
    True
    """
    Z = _as_2d(Z)
    p = Z.shape[1]
    if p not in (1, 2, 3):
        raise ValueError(f"find_holes supports d - 1 in 1, 2 or 3 chart coordinates, got {p}")
    if not (isinstance(resolution, (int, np.integer)) and resolution >= 2):
        raise ValueError("resolution must be an integer >= 2")
    lo, hi = Z.min(axis=0), Z.max(axis=0)
    axes = [np.linspace(a, b, resolution) for a, b in zip(lo, hi, strict=True)]
    grid = np.stack(np.meshgrid(*axes, indexing="ij"), axis=-1).reshape(-1, p)
    inside = (
        (grid[:, 0] >= lo[0]) & (grid[:, 0] <= hi[0])
        if p == 1
        else Delaunay(Z).find_simplex(grid) >= 0
    )
    grid = grid[inside]
    tree = cKDTree(Z)
    nn = tree.query(Z, k=2)[0][:, 1]
    med = np.median(nn)
    if grid.shape[0] == 0 or med <= 0:
        return np.empty((0, p)), np.empty(0)
    score = tree.query(grid, k=1)[0] / med
    sel = score > threshold
    order = np.argsort(-score[sel], kind="stable")
    return grid[sel][order], score[sel][order]


def frontier_targets(Z_points, estimator, preconditioner=None):
    """Frontier designs (``V = 1``) above given chart coordinates, in metrics and attributes.

    Parameters
    ----------
    Z_points : array-like of shape (n_points, d - 1)
        Chart coordinates, for example hole centres from ``find_holes``.
    estimator : HyperbolicTradeSpace
        Fitted estimator; ``log V = 0`` is set and the chart is inverted.
    preconditioner : transformer with ``inverse_transform``, optional
        Fitted conditioner of attributes into metrics (``LogAffinePreconditioner``); when given,
        the metric targets are mapped back to attribute units.

    Returns
    -------
    dict
        ``"metrics"`` : ndarray of shape (n_points, d), with ``V = 1`` and chart coordinates
        ``Z_points``; ``"attributes"`` : ``preconditioner.inverse_transform(metrics)`` or ``None``.

    Examples
    --------
    >>> import numpy as np
    >>> from hyperbolic_trade_space import HyperbolicTradeSpace, make_frontier_data
    >>> X, _ = make_frontier_data(100, 3, random_state=0)
    >>> est = HyperbolicTradeSpace(temperature=np.inf).fit(X)
    >>> out = frontier_targets(np.zeros((1, 2)), est)
    >>> round(float(est.invariant_value(out["metrics"])[0]), 9), out["attributes"]
    (1.0, None)
    """
    Z = _as_2d(Z_points, "Z_points")
    d = estimator.n_features_in_
    if Z.shape[1] != d - 1:
        raise ValueError(f"Z_points must have {d - 1} columns, got {Z.shape[1]}")
    metrics = estimator.level_set(Z, 1.0)
    attributes = None if preconditioner is None else preconditioner.inverse_transform(metrics)
    return {"metrics": metrics, "attributes": attributes}


def orient_by_pca(Z, mask=None):
    """Rotate chart coordinates onto the principal axes of the masked (near-frontier) rows.

    Parameters
    ----------
    Z : array-like of shape (n_points, p)
        Chart coordinates.
    mask : array-like of bool of shape (n_points,), optional
        Rows that define the axes (for example ``|log V| < band``); all rows by default.

    Returns
    -------
    Z_rotated : ndarray of shape (n_points, p)
        ``Z @ components.T``, a pure rotation (and reflection) of all rows.
    components : ndarray of shape (p, p)
        Orthonormal principal directions in ``Z`` as rows, by decreasing variance of the masked
        rows. Sign convention: the largest-magnitude loading of each row is positive (the first
        such entry on ties).
    explained_variance_ratio : ndarray of shape (p,)
        Share of the masked rows' variance along each direction (zeros if there is none).

    Examples
    --------
    >>> import numpy as np
    >>> rng = np.random.default_rng(0)
    >>> Z = rng.normal(size=(300, 2)) * [3.0, 0.3]
    >>> Zr, comps, evr = orient_by_pca(Z)
    >>> np.abs(comps).round(2).tolist(), bool(evr[0] > 0.98)
    ([[1.0, 0.0], [0.0, 1.0]], True)
    """
    Z = _as_2d(Z)
    n, p = Z.shape
    if mask is None:
        mask = np.ones(n, dtype=bool)
    mask = np.asarray(mask, dtype=bool)
    if mask.shape != (n,):
        raise ValueError(f"mask must have shape ({n},), got {mask.shape}")
    if mask.sum() < 2:
        raise ValueError("orient_by_pca needs at least 2 masked rows")
    if p == 0:
        return Z.copy(), np.empty((0, 0)), np.empty(0)
    S = Z[mask] - Z[mask].mean(axis=0)
    _, sv, Vt = np.linalg.svd(S, full_matrices=True)
    comps = Vt.copy()
    var = np.zeros(p)
    var[: sv.size] = sv**2
    for i in range(p):
        a = np.abs(comps[i])
        if comps[i, np.flatnonzero(a >= a.max() - 1e-12)[0]] < 0:
            comps[i] = -comps[i]
    total = var.sum()
    evr = var / total if total > 0 else np.zeros(p)
    return Z @ comps.T, comps, evr

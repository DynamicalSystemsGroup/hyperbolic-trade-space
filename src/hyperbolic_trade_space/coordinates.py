"""Invertible chart of log-metric space: ``log V`` and ``d - 1`` log-ratio coordinates ``Z``.

With ``u = log m`` and a basis ``B`` of shape ``(d-1, d)`` whose rows span ``1^perp`` (``B 1 = 0``),
``Z = B u`` is blind to the common shift ``u + c 1`` (lemma L8) and ``log V = w.u - beta`` carries
the scale. For the ILR (Helmert) basis ``B B^T = I`` (axiom A7), so ``u = B^T Z + (log V + beta -
w.B^T Z) 1``; the ALR basis is invertible but not orthonormal.
"""

from __future__ import annotations

import numpy as np

__all__ = ["alr_basis", "from_frontier_coordinates", "helmert_basis", "to_frontier_coordinates"]


def helmert_basis(d):
    """Helmert (ILR) basis: rows ``(1,..,1,-k,0,..)/sqrt(k(k+1))`` for ``k = 1..d-1``.

    Parameters
    ----------
    d : int
        Number of metrics, ``d >= 1``.

    Returns
    -------
    ndarray of shape (d-1, d)
        ``B B^T = I`` and ``B 1 = 0`` (lemma L8, axiom A7). For ``d = 1`` the shape is ``(0, 1)``.

    Examples
    --------
    >>> import numpy as np
    >>> B = helmert_basis(3)
    >>> bool(np.allclose(B @ B.T, np.eye(2))), bool(np.allclose(B.sum(axis=1), 0))
    (True, True)
    """
    if d < 1:
        raise ValueError("d must be >= 1")
    B = np.zeros((d - 1, d))
    for k in range(1, d):
        B[k - 1, :k] = 1.0
        B[k - 1, k] = -float(k)
        B[k - 1] /= np.sqrt(k * (k + 1.0))
    return B


def alr_basis(d):
    """Additive log-ratio basis with the last metric as reference: ``Z_j = u_j - u_d``.

    Parameters
    ----------
    d : int
        Number of metrics, ``d >= 1``.

    Returns
    -------
    ndarray of shape (d-1, d)
        ``[I | -1]``; ``B 1 = 0`` but ``B B^T != I`` (not orthonormal).

    Examples
    --------
    >>> alr_basis(3).tolist()
    [[1.0, 0.0, -1.0], [0.0, 1.0, -1.0]]
    """
    if d < 1:
        raise ValueError("d must be >= 1")
    return np.hstack([np.eye(d - 1), -np.ones((d - 1, 1))])


def to_frontier_coordinates(U, w, beta, B):
    """Map log metrics to chart coordinates ``(Z, log V)``.

    Parameters
    ----------
    U : ndarray of shape (n, d)
        Log metrics; rows with ``-inf`` (zero metrics) give ``Z = nan`` and ``log V = -inf``.
    w : ndarray of shape (d,)
        Exponents on the simplex.
    beta : float
        Offset.
    B : ndarray of shape (d-1, d)
        Chart basis.

    Returns
    -------
    Z : ndarray of shape (n, d-1)
        ``U @ B.T``.
    log_v : ndarray of shape (n,)
        ``U @ w - beta``.

    Examples
    --------
    >>> import numpy as np
    >>> U = np.array([[0.0, 1.0], [2.0, 2.0]])
    >>> Z, lv = to_frontier_coordinates(U, np.array([0.5, 0.5]), 0.5, helmert_basis(2))
    >>> Z.round(4).tolist(), lv.round(4).tolist()
    ([[-0.7071], [0.0]], [0.0, 1.5])
    """
    U = np.atleast_2d(np.asarray(U, dtype=float))
    w = np.asarray(w, dtype=float)
    bad = (-np.inf == U).any(axis=1)
    Uf = np.where(bad[:, None], 0.0, U)
    Z = Uf @ B.T
    log_v = Uf @ w - beta
    Z[bad] = np.nan
    log_v[bad] = -np.inf
    return Z, log_v


def from_frontier_coordinates(Z, log_v, w, beta, B):
    """Inverse of :func:`to_frontier_coordinates`: ``u = C Z + (log V + beta - w.C Z) 1``.

    Parameters
    ----------
    Z : ndarray of shape (n, d-1)
    log_v : ndarray of shape (n,)
    w : ndarray of shape (d,)
        Exponents on the simplex (``sum w = 1``).
    beta : float
    B : ndarray of shape (d-1, d)

    Returns
    -------
    ndarray of shape (n, d)
        Log metrics ``U``. Rows with non-finite ``Z`` or ``log V`` are returned as ``nan``.

    Notes
    -----
    ``C = pinv(B)`` (``B^T`` for ILR) satisfies ``B C = I``, and ``u - C Z`` lies in
    ``span(1)``; the scale is fixed by ``w.u = log V + beta``.

    Examples
    --------
    >>> import numpy as np
    >>> B, w = helmert_basis(3), np.array([0.2, 0.3, 0.5])
    >>> U = np.array([[0.1, -0.4, 0.7]])
    >>> Z, lv = to_frontier_coordinates(U, w, 0.2, B)
    >>> bool(np.allclose(from_frontier_coordinates(Z, lv, w, 0.2, B), U))
    True
    """
    Z = np.asarray(Z, dtype=float).reshape(np.size(log_v), np.shape(B)[0])
    log_v = np.atleast_1d(np.asarray(log_v, dtype=float))
    w = np.asarray(w, dtype=float)
    d = w.size
    bad = ~np.isfinite(log_v) | ~np.isfinite(Z).all(axis=1)
    Zf = np.where(bad[:, None], 0.0, Z)
    base = Zf @ np.linalg.pinv(B).T if d > 1 else np.zeros((Z.shape[0], 1))
    shift = np.where(bad, 0.0, log_v) + beta - base @ w
    U = base + shift[:, None]
    U[bad] = np.nan
    return U

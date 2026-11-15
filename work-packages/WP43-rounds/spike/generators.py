"""Planted tables of the WP43 spike (protocol.md): kinds T, Q and D, each with its truth known.

Every generator returns ``(X, truth)``; ``truth`` holds ``log_v`` (the planted level of each row)
and the planted objects, so a fresh test sample of the same truth can be drawn with ``test_sample``.
"""

from __future__ import annotations

import numpy as np
from models import ROOT  # noqa: F401  (puts src on the path)

from hyperbolic_trade_space import make_frontier_data
from hyperbolic_trade_space.coordinates import helmert_basis

D = 4
T_EXPONENTS = [[0.5, 0.5, 0, 0], [0, 0.5, 0.5, 0], [0, 0, 0.5, 0.5]]
Q_SCALE = 0.5
RHO = 1.0


def planted_t(seed, n=400):
    X, info = make_frontier_data(
        n, D, n_terms=3, exponents=T_EXPONENTS, noise=0.0, random_state=seed
    )
    return X, {"kind": "T", "log_v": info["log_v"], "info": info}


def _q_truth(seed, rank, w):
    rng = np.random.default_rng(500 + seed)
    V, _ = np.linalg.qr(rng.normal(size=(D - 1, rank)))
    return Q_SCALE * V @ V.T


def planted_q(seed, n=400, w=None, S=None, data_seed=None):
    rank = 1 if seed < 10 else 2
    _, info = make_frontier_data(
        n, D, exponents=w, random_state=seed if data_seed is None else data_seed
    )
    w = info["exponents"] if w is None else np.asarray(w)
    S = _q_truth(seed, rank, w) if S is None else S
    B, Z, lv = info["basis"], info["Z"], info["log_v"]
    base = Z @ B  # B'z, shape (n, d)
    s = lv - base @ w - 0.5 * np.einsum("ij,jk,ik->i", Z, S, Z)
    X = np.exp(base + s[:, None])
    return X, {"kind": "Q", "log_v": lv, "w": w, "S": S, "rank": rank, "Z": Z, "info": info}


def _z_c(seed):
    v = np.random.default_rng(700 + seed).normal(size=D - 1)
    return v / np.linalg.norm(v)


def planted_d(seed, n=450):
    X, info = make_frontier_data(n, D, random_state=seed)
    zc = _z_c(seed)
    dist = np.sqrt(((info["Z"] - zc) ** 2).sum(axis=1) + info["log_v"] ** 2)
    keep = dist >= RHO
    truth = {
        "kind": "D",
        "log_v": info["log_v"][keep],
        "w": info["exponents"],
        "Z": info["Z"][keep],
        "z_c": zc,
        "removed": int((~keep).sum()),
        "info": info,
    }
    return X[keep], truth


def test_sample(kind, seed, truth, n=2000):
    """A fresh sample of the same planted truth (the undented truth for kind D)."""
    if kind == "T":
        return planted_t(1000 + seed, n)
    if kind == "Q":
        return planted_q(seed, n, w=truth["w"], S=truth["S"], data_seed=1000 + seed)
    X, info = make_frontier_data(n, D, exponents=truth["w"], random_state=1000 + seed)
    return X, {"kind": "D", "log_v": info["log_v"], "w": truth["w"], "Z": info["Z"]}


def notch_point(truth):
    """The truth's frontier point at ``z_c`` as log metrics (kind D)."""
    B = helmert_basis(D)
    w, zc = truth["w"], truth["z_c"]
    base = zc @ B
    return base + (0.0 - base @ w)


def rim_mask(truth):
    dist = np.sqrt(((truth["Z"] - truth["z_c"]) ** 2).sum(axis=1) + truth["log_v"] ** 2)
    return (dist >= RHO) & (dist < 2 * RHO)

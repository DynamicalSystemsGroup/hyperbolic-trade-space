"""Gap tools (R-5, R-6, R-7): k-NN scores, holes, frontier targets, PCA orientation.

Tolerances: planted holes are located to within one grid cell; frontier targets satisfy V = 1 and
round-trip to 1e-9; seeds 0, 1, 2.
"""

import numpy as np
import pytest

from hyperbolic_trade_space import HyperbolicTradeSpace, make_frontier_data
from hyperbolic_trade_space.gaps import find_holes, frontier_targets, knn_gap_scores, orient_by_pca


class _Stand:
    """Lightweight stand-in preconditioner: x = m * scale (inverse_transform only)."""

    def __init__(self, scale):
        self.scale = np.asarray(scale, dtype=float)

    def inverse_transform(self, M):
        return np.asarray(M) * self.scale


# ------------------------------------------------------------------ R-5 knn_gap_scores
@pytest.mark.parametrize("seed", [0, 1, 2])
def test_knn_flags_isolated_point(seed):
    rng = np.random.default_rng(seed)
    Z = np.vstack([rng.normal(size=(200, 2)), [[12.0, 12.0]]])
    s = knn_gap_scores(Z, k=5)
    assert s.shape == (201,)
    assert np.argmax(s) == 200 and s[200] > 5 * np.median(s[:200])
    assert np.median(s) == pytest.approx(1.0)


def test_knn_1d_and_validation():
    Z = np.r_[np.linspace(0, 1, 50), 5.0][:, None]
    assert np.argmax(knn_gap_scores(Z, k=3)) == 50
    with pytest.raises(ValueError, match="k"):
        knn_gap_scores(Z, k=0)
    with pytest.raises(ValueError, match="k"):
        knn_gap_scores(Z[:4], k=4)


# ------------------------------------------------------------------ R-5 find_holes
def _disc_data(seed, n=3000):
    rng = np.random.default_rng(seed)
    Z = rng.uniform(-3, 3, size=(n, 2))
    keep = np.linalg.norm(Z - [0.5, -0.5], axis=1) > 1.0
    return Z[keep]


@pytest.mark.parametrize("seed", [0, 1, 2])
def test_find_holes_2d_planted_disc(seed):
    Z = _disc_data(seed)
    pts, score = find_holes(Z, resolution=60, threshold=8.0)
    assert len(pts) > 0 and np.all(score > 3.0)
    centre = pts[np.argmax(score)]
    assert np.linalg.norm(centre - [0.5, -0.5]) < 0.35
    # every reported hole point lies inside the planted disc (it is the only hole)
    assert np.all(np.linalg.norm(pts - [0.5, -0.5], axis=1) < 1.0 + 0.2)


def test_find_holes_restricts_to_hull():
    rng = np.random.default_rng(0)
    th = rng.uniform(0, 2 * np.pi, 400)
    r = np.sqrt(rng.uniform(0, 1, 400))
    Z = np.c_[r * np.cos(th), r * np.sin(th)]  # a disc: bbox corners are outside the hull
    pts, _ = find_holes(Z, resolution=40, threshold=0.0)
    assert np.all(np.linalg.norm(pts, axis=1) <= 1.0 + 1e-9)
    assert np.all(np.abs(pts).max(axis=1) <= 1.0)
    assert np.any(np.linalg.norm(pts, axis=1) > 0.9)


def test_find_holes_1d_planted_gap():
    rng = np.random.default_rng(1)
    Z = np.r_[rng.uniform(-3, -0.5, 200), rng.uniform(1.0, 3, 200)][:, None]
    pts, score = find_holes(Z, resolution=200, threshold=10.0)
    assert len(pts) > 0
    assert np.all((pts > -0.6) & (pts < 1.1))
    assert abs(pts[np.argmax(score), 0] - 0.25) < 0.2


def test_find_holes_3d_runs_and_other_dims_raise():
    rng = np.random.default_rng(2)
    Z = rng.uniform(-2, 2, size=(4000, 3))
    Z = Z[np.linalg.norm(Z, axis=1) > 1.0]
    pts, score = find_holes(Z, resolution=15, threshold=4.0)
    assert pts.shape[1] == 3 and len(pts) == len(score)
    assert np.all(np.linalg.norm(pts, axis=1) < 1.3)
    with pytest.raises(ValueError, match="1, 2 or 3"):
        find_holes(rng.normal(size=(50, 4)))
    with pytest.raises(ValueError, match="1, 2 or 3"):
        find_holes(rng.normal(size=(50, 0)))


def test_find_holes_none_found_returns_empty():
    g = np.linspace(0, 1, 20)
    Z = np.array([(a, b) for a in g for b in g])
    pts, score = find_holes(Z, resolution=40, threshold=5.0)
    assert pts.shape == (0, 2) and score.shape == (0,)


# ------------------------------------------------------------------ R-6 frontier_targets
@pytest.mark.parametrize("seed", [0, 1, 2])
def test_frontier_targets_on_frontier_and_round_trip(seed):
    X, _ = make_frontier_data(300, 3, random_state=seed)
    est = HyperbolicTradeSpace(temperature=np.inf).fit(X)
    Z = est.transform(X)[:3, :-1] + 0.1
    out = frontier_targets(Z, est)
    M = out["metrics"]
    assert out["attributes"] is None
    assert np.allclose(est.invariant_value(M), 1.0, atol=1e-9)
    assert np.allclose(est.transform(M)[:, :-1], Z, atol=1e-9)
    assert np.allclose(est.transform(M)[:, -1], 0.0, atol=1e-9)


def test_frontier_targets_with_preconditioner_stand_in():
    X, _ = make_frontier_data(200, 3, random_state=0)
    est = HyperbolicTradeSpace(temperature=np.inf).fit(X)
    scale = np.array([2.0, 0.5, 10.0])
    Z = np.array([[0.0, 0.0], [0.3, -0.2]])
    out = frontier_targets(Z, est, _Stand(scale))
    assert np.allclose(out["attributes"], out["metrics"] * scale)
    assert np.allclose(est.invariant_value(out["attributes"] / scale), 1.0)


def test_frontier_targets_with_real_preconditioner():
    LogAffinePreconditioner = pytest.importorskip(
        "hyperbolic_trade_space.preconditioning"
    ).LogAffinePreconditioner
    rng = np.random.default_rng(0)
    A = np.exp(rng.normal(size=(300, 3)))
    pre = LogAffinePreconditioner(orientation=[1, -1, 1]).fit(A)
    est = HyperbolicTradeSpace(temperature=np.inf).fit(pre.transform(A))
    Z = est.transform(pre.transform(A))[:4, :-1]
    out = frontier_targets(Z, est, pre)
    assert np.allclose(pre.transform(out["attributes"]), out["metrics"], rtol=1e-8)
    assert np.allclose(est.invariant_value(pre.transform(out["attributes"])), 1.0)


def test_frontier_targets_bad_shape():
    X, _ = make_frontier_data(100, 3, random_state=0)
    est = HyperbolicTradeSpace().fit(X)
    with pytest.raises(ValueError, match="columns"):
        frontier_targets(np.zeros((2, 3)), est)


# ------------------------------------------------------------------ R-7 orient_by_pca
def test_orient_by_pca_rotation_and_sign():
    rng = np.random.default_rng(0)
    th = 0.6
    R = np.array([[np.cos(th), -np.sin(th)], [np.sin(th), np.cos(th)]])
    Z = (rng.normal(size=(500, 2)) * [3.0, 0.5]) @ R.T
    Zr, comps, evr = orient_by_pca(Z)
    assert np.allclose(comps @ comps.T, np.eye(2), atol=1e-12)
    assert np.allclose(Zr, Z @ comps.T)
    assert evr[0] > 0.95 and evr.sum() == pytest.approx(1.0)
    assert abs(abs(comps[0] @ R[:, 0]) - 1) < 0.02
    for row in comps:  # sign convention: largest-magnitude loading positive
        assert row[np.argmax(np.abs(row))] > 0
    # deterministic and invariant to a sign flip of the data
    assert np.allclose(orient_by_pca(-Z)[1], comps)


def test_orient_by_pca_mask_uses_only_masked_rows():
    rng = np.random.default_rng(1)
    near = rng.normal(size=(200, 2)) * [1.0, 0.1]
    far = rng.normal(size=(200, 2)) * [0.1, 5.0]
    Z = np.vstack([near, far])
    mask = np.r_[np.ones(200, bool), np.zeros(200, bool)]
    _, comps, _ = orient_by_pca(Z, mask)
    assert abs(comps[0, 0]) > 0.99
    _, comps_all, _ = orient_by_pca(Z)
    assert abs(comps_all[0, 1]) > 0.99


def test_orient_by_pca_validation():
    with pytest.raises(ValueError, match="at least 2"):
        orient_by_pca(np.zeros((5, 2)), np.r_[True, np.zeros(4, bool)])
    with pytest.raises(ValueError, match="mask"):
        orient_by_pca(np.zeros((5, 2)), np.ones(4, bool))

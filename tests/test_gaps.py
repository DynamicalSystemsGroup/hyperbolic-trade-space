"""Gap tools (R-5, R-6, R-7): k-NN scores, holes, frontier targets, PCA orientation.

Tolerances: planted holes are located to within one grid cell; frontier targets satisfy V = 1 and
round-trip to 1e-9; seeds 0, 1, 2.
"""

from pathlib import Path

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


# ------------------------------------------------------------------ WP21 D-8, ledger gap G-18
# Equal mean slack does not identify the boundary: two supporting envelopes over the same 48 rows,
# the two-term envelope A and the three-term envelope B = A plus one plane that lies below A at
# every row and above it in the unsampled gap between the two clusters of rows.
G18 = Path(__file__).parent / "data" / "g18_equal_slack_fixture.npz"
LEDGER = Path(__file__).parents[1] / "docs" / "superpowers" / "notes" / "abstraction-gaps.md"
SLACK_TOL = 1e-12  # the two mean slacks agree to this (the envelopes agree at every row)
BOUNDARY_MARGIN = 0.25  # the boundaries differ by more than this in log V at the gap's centre


def _envelope(template, W, beta):
    """The template estimator carrying the envelope ``(W, beta)`` (the package's own chart)."""
    est = HyperbolicTradeSpace(n_terms=len(W)).fit(template)
    est.exponents_, est.log_offset_ = np.asarray(W, float), np.asarray(beta, float)
    est.basis_ = np.repeat(est.basis_[:1], len(W), axis=0)
    return est


@pytest.fixture(scope="module")
def g18():
    f = np.load(G18)
    X = f["X"]
    return X, _envelope(X, f["W_A"], f["beta_A"]), _envelope(X, f["W_B"], f["beta_B"]), f


def test_g18_the_fixture_is_the_frozen_planted_data(g18):
    X, _, _, f = g18
    assert X.shape == (48, 2) and (X > 0).all()
    assert f["W_A"].shape == (2, 2) and f["W_B"].shape == (3, 2)
    np.testing.assert_allclose(f["W_A"].sum(axis=1), 1.0)
    np.testing.assert_allclose(f["W_B"].sum(axis=1), 1.0)
    assert "default_rng(18)" in str(f["recipe"])


def test_g18_two_envelopes_have_equal_mean_slack(g18):
    X, A, B, _ = g18
    for est in (A, B):  # both support every row: V <= 1, with the frontier rows on it
        log_v = est.score_samples(X)
        assert (log_v <= 1e-12).all() and (log_v > -1e-9).sum() >= 16
    slack_a, slack_b = -A.score_samples(X).mean(), -B.score_samples(X).mean()
    assert slack_a == pytest.approx(slack_b, abs=SLACK_TOL) and slack_a > 0.1
    # the K = 2 fit of the package finds envelope A on these rows, with the same mean slack
    fit = HyperbolicTradeSpace(n_terms=2, temperature=np.inf, random_state=0).fit(X)
    assert fit.mean_slack_ == pytest.approx(slack_a, abs=1e-9)
    np.testing.assert_allclose(
        np.sort(fit.exponents_, axis=0), np.sort(A.exponents_, axis=0), atol=1e-9
    )


def test_g18_the_boundaries_differ_where_there_are_no_rows(g18):
    X, A, B, _ = g18
    s = np.log(X[:, 0]) - np.log(X[:, 1])
    assert not ((s > -1.2) & (s < 1.2)).any()  # the gap is unsampled
    gap = np.linspace(-1.0, 1.0, 41)
    base = np.exp(np.column_stack([gap / 2, -gap / 2]))  # metrics across the gap
    diff = B.score_samples(base) - A.score_samples(base)
    assert (diff >= -1e-12).all() and diff.max() > BOUNDARY_MARGIN  # B lies above A in the gap
    assert diff.max() == pytest.approx(0.3, abs=1e-9)  # at the corner of A, s = 0
    # the surfaces V = 1 differ by the same margin in the metrics (the package's level set)
    Z = A.transform(base)[:, :-1]
    gap_log_m = np.log(A.level_set(Z)) - np.log(B.level_set(Z))
    assert np.abs(gap_log_m).max() > BOUNDARY_MARGIN
    # at the rows the two agree exactly: the loss cannot tell them apart
    np.testing.assert_allclose(B.score_samples(X), A.score_samples(X), atol=SLACK_TOL)


def test_g18_is_in_the_ledger_with_the_assessment_as_evidence():
    row = next(
        line for line in LEDGER.read_text(encoding="utf-8").splitlines() if "**G-18." in line
    )
    assert "external-assessment-2026-11-09" in row and "g18_equal_slack_fixture" in row
    assert "tests/test_gaps.py" in row

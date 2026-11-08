"""Tests for datasets: R-6."""

import numpy as np
import pytest

from hyperbolic_trade_space.coordinates import to_frontier_coordinates
from hyperbolic_trade_space.datasets import make_configured_frontier_data, make_frontier_data


def test_frontier_info_and_planting():
    X, info = make_frontier_data(500, 4, log_offset=0.7, random_state=3)
    assert X.shape == (500, 4) and (X > 0).all()
    assert set(info) >= {"exponents", "log_offset", "basis", "frontier_mask", "Z", "log_v", "noise"}
    w = info["exponents"]
    assert w.sum() == pytest.approx(1.0) and (w >= 0.5 / 4 - 1e-12).all()
    Z, lv = to_frontier_coordinates(np.log(X), w, 0.7, info["basis"])
    np.testing.assert_allclose(lv, info["log_v"], atol=1e-12)
    np.testing.assert_allclose(Z, info["Z"], atol=1e-12)
    mask = info["frontier_mask"]
    assert mask.sum() == 150 and np.abs(lv[mask]).max() < 1e-12 and (lv[~mask] < 0).all()


def test_reproducible_and_noise():
    a, ia = make_frontier_data(50, 3, noise=0.1, random_state=7)
    b, _ = make_frontier_data(50, 3, noise=0.1, random_state=7)
    c, _ = make_frontier_data(50, 3, noise=0.1, random_state=8)
    np.testing.assert_array_equal(a, b)
    assert not np.allclose(a, c)
    assert ia["noise"] == 0.1 and ia["log_v"][ia["frontier_mask"]].std() > 0


def test_given_exponents_and_validation():
    _, info = make_frontier_data(10, 2, exponents=[0.25, 0.75], random_state=0)
    np.testing.assert_array_equal(info["exponents"], [0.25, 0.75])
    with pytest.raises(ValueError):
        make_frontier_data(10, 2, exponents=[0.5, 0.6])
    with pytest.raises(ValueError):
        make_frontier_data(10, 2, frontier_fraction=0.0)


def test_d1():
    X, info = make_frontier_data(20, 1, random_state=0)
    assert X.shape == (20, 1) and info["Z"].shape == (20, 0)


def test_configured():
    C, Y, info = make_configured_frontier_data(300, 3, 4, noise=0.0, random_state=1)
    assert C.shape == (300, 4) and Y.shape == (300, 3) and (Y > 0).all()
    Z, lv = info["config_map"](C)
    np.testing.assert_allclose(Z, info["Z"])
    mask = info["frontier_mask"]
    assert np.abs(lv[mask]).max() < 1e-12 and (lv <= 1e-12).all()
    Zc, lvc = to_frontier_coordinates(
        np.log(Y), info["exponents"], info["log_offset"], info["basis"]
    )
    np.testing.assert_allclose(Zc, Z, atol=1e-10)
    np.testing.assert_allclose(lvc, lv, atol=1e-10)
    _, Y2, _ = make_configured_frontier_data(300, 3, 4, random_state=1)
    np.testing.assert_array_equal(Y, Y2)
    with pytest.raises(ValueError):
        make_configured_frontier_data(10, 3, 1)


def test_n_terms_one_is_unchanged():
    X, info = make_frontier_data(50, 3, noise=0.1, random_state=2)
    X1, info1 = make_frontier_data(50, 3, noise=0.1, random_state=2, n_terms=1)
    np.testing.assert_array_equal(X, X1)
    assert set(info) == set(info1) and "facet" not in info1
    for key in info:
        np.testing.assert_array_equal(info[key], info1[key])
    assert info1["exponents"].shape == (3,)
    np.testing.assert_allclose(X[0], [1.60881165, 1.53768322, 0.36959939], atol=1e-8)
    np.testing.assert_allclose(info["exponents"], [0.37168011, 0.17607022, 0.45224967], atol=1e-8)
    np.testing.assert_allclose(info["log_v"][:2], [-0.19764891, -0.09263645], atol=1e-8)


def _phi(U, W, beta):
    return (U @ W.T).max(axis=1) - beta


def test_k_terms_planted_envelope():
    n, d, K = 600, 4, 3
    X, info = make_frontier_data(n, d, log_offset=0.4, n_terms=K, random_state=5)
    W, mask, facet = info["exponents"], info["frontier_mask"], info["facet"]
    assert X.shape == (n, d) and (X > 0).all() and W.shape == (K, d)
    assert (W >= 0).all() and np.allclose(W.sum(axis=1), 1.0)
    dist = np.abs(W[:, None] - W[None]).sum(-1)[np.triu_indices(K, 1)]
    assert dist.min() >= 0.3
    np.testing.assert_allclose(_phi(np.log(X), W, 0.4), info["log_v"], atol=1e-9)
    assert np.abs(info["log_v"][mask]).max() < 1e-9 and (info["log_v"][~mask] < 0).all()
    assert facet.shape == (n,) and facet.min() >= 0 and facet.max() < K
    np.testing.assert_array_equal(facet, (np.log(X) @ W.T).argmax(axis=1))
    counts = np.bincount(facet[mask], minlength=K)
    assert (counts >= 0.1 * mask.sum()).all()
    X2, info2 = make_frontier_data(n, d, log_offset=0.4, n_terms=K, random_state=5)
    np.testing.assert_array_equal(X, X2)
    np.testing.assert_array_equal(info["facet"], info2["facet"])


def test_k_terms_errors_and_explicit_exponents():
    with pytest.raises(ValueError, match="apart"):
        make_frontier_data(10, 2, n_terms=12, random_state=0)
    with pytest.raises(ValueError):
        make_frontier_data(10, 1, n_terms=2, random_state=0)
    with pytest.raises(ValueError):
        make_frontier_data(10, 3, n_terms=2, exponents=[0.2, 0.3, 0.5])
    with pytest.raises(ValueError):
        make_frontier_data(10, 3, n_terms=2, exponents=[[0.5, 0.5, 0.1], [0.2, 0.3, 0.5]])
    with pytest.raises(ValueError):
        make_frontier_data(10, 3, n_terms=0)
    W = [[0.7, 0.2, 0.1], [0.1, 0.2, 0.7]]
    _, info = make_frontier_data(10, 3, n_terms=2, exponents=W, random_state=0)
    np.testing.assert_array_equal(info["exponents"], W)

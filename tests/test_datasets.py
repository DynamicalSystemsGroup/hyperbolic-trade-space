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

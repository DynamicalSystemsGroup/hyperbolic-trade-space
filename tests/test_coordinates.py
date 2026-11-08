"""Tests for coordinates: R-5."""

import numpy as np
import pytest

from hyperbolic_trade_space.coordinates import (
    alr_basis,
    from_frontier_coordinates,
    helmert_basis,
    to_frontier_coordinates,
)


@pytest.mark.parametrize("d", range(2, 9))
def test_helmert_orthonormal_kernel(d):
    B = helmert_basis(d)
    assert B.shape == (d - 1, d)
    np.testing.assert_allclose(B @ B.T, np.eye(d - 1), atol=1e-12)
    np.testing.assert_allclose(B @ np.ones(d), 0.0, atol=1e-12)


@pytest.mark.parametrize("d", range(2, 9))
@pytest.mark.parametrize("basis", [helmert_basis, alr_basis])
def test_round_trip_and_invariance(d, basis):
    rng = np.random.default_rng(d)
    B = basis(d)
    w = rng.dirichlet(np.ones(d))
    U = rng.normal(size=(20, d))
    beta = 0.37
    Z, lv = to_frontier_coordinates(U, w, beta, B)
    np.testing.assert_allclose(from_frontier_coordinates(Z, lv, w, beta, B), U, atol=1e-12)
    Z2, lv2 = to_frontier_coordinates(U + 1.7, w, beta, B)
    np.testing.assert_allclose(Z2, Z, atol=1e-12)
    np.testing.assert_allclose(lv2, lv + 1.7, atol=1e-12)  # sum w = 1


def test_alr_not_orthonormal_but_kernel():
    B = alr_basis(4)
    np.testing.assert_allclose(B @ np.ones(4), 0.0)
    assert not np.allclose(B @ B.T, np.eye(3))
    assert alr_basis(3).tolist() == [[1.0, 0.0, -1.0], [0.0, 1.0, -1.0]]


def test_d1():
    B = helmert_basis(1)
    assert B.shape == (0, 1) and alr_basis(1).shape == (0, 1)
    U = np.array([[0.3], [-1.0]])
    Z, lv = to_frontier_coordinates(U, np.array([1.0]), 0.1, B)
    assert Z.shape == (2, 0)
    np.testing.assert_allclose(lv, [0.2, -1.1])
    np.testing.assert_allclose(from_frontier_coordinates(Z, lv, np.array([1.0]), 0.1, B), U)


def test_minus_inf_rows():
    B, w = helmert_basis(3), np.array([0.2, 0.3, 0.5])
    U = np.array([[0.1, -np.inf, 0.2], [0.1, 0.2, 0.3]])
    Z, lv = to_frontier_coordinates(U, w, 0.0, B)
    assert np.isnan(Z[0]).all() and lv[0] == -np.inf and np.isfinite(Z[1]).all()
    back = from_frontier_coordinates(Z, lv, w, 0.0, B)
    assert np.isnan(back[0]).all()
    np.testing.assert_allclose(back[1], U[1], atol=1e-12)


def test_invalid_d():
    with pytest.raises(ValueError):
        helmert_basis(0)

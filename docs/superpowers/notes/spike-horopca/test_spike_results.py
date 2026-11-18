"""Checks on the recorded spike results; needs only numpy and pytest, not the spike's venv.

    uv run pytest docs/superpowers/notes/spike-horopca/test_spike_results.py

Regenerate results.json first (see README.md in this folder): make_tables.py in the repository
environment, run_horopca.py in the spike's own venv.
"""
import json
from pathlib import Path

import numpy as np
import pytest

HERE = Path(__file__).parent
RES = HERE / "results.json"
pytestmark = pytest.mark.skipif(not RES.exists(), reason="results.json not recorded")


@pytest.fixture(scope="module")
def results():
    return json.loads(RES.read_text(encoding="utf-8"))


def test_logmap_inverts_expmap_so_tangent_pca_is_ordinary_pca(results):
    # the repository's TangentPCA is PCA on logmap0 of the embedded points, which are the scaled
    # centred log-metrics: the round trip is exact, so tangent PCA is ordinary PCA of the table
    for table in results.values():
        for entry in table["horopca"].values():
            assert entry["logmap_expmap_roundtrip_err"] < 1e-9


def test_near_origin_horopca_explains_what_pca_explains(results):
    # at the smallest scale the ball is nearly flat: the variance HoroPCA keeps (k = 1, best of
    # five runs) is within five points of PCA's first component on the same rows
    for table in results.values():
        small = table["horopca"][min(table["horopca"], key=float)]
        # not identical: the repository's objective is the variance of Busemann values, measured here as
        # mean squared pairwise distance in the ball
        assert abs(small["k1"]["best"]["explained"] - table["pca"]["k1"]["explained"]) < 0.05


def test_explained_fractions_are_fractions(results):
    for table in results.values():
        for entry in table["horopca"].values():
            for k in ("k1", "k2"):
                assert all(0 < e <= 1 + 1e-9 for e in entry[k]["explained_all_runs"])


def test_pca_components_mix_signs_so_are_not_exponents(results):
    # an exponent vector lies on the simplex (nonnegative); a principal direction does not
    for name, table in results.items():
        assert not all(table["pca"]["sign_pure_pc"][:2]), name

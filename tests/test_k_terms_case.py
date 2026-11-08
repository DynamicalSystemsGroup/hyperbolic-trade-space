"""WP9 D-6: the K = 1, 2, 3 cubesat case script runs, and its figures and labels are sound."""

import re
from pathlib import Path

import k_terms
import numpy as np
import pytest

SCRIPT = Path(k_terms.__file__)


@pytest.fixture(scope="module", params=list(k_terms.REGIMES))
def result(request, tmp_path_factory):
    out = k_terms.run_regime(
        request.param, seeds=[0], figs=tmp_path_factory.mktemp("figs"), verbose=False
    )
    return request.param, out


def test_k3_fits_and_three_reports(result):
    _, out = result
    est, reps = out["fits"][3], out["reports"][3]
    assert est.exponents_.shape == (3, 10)
    assert len(reps) == 3 and len(out["reports"][1]) == 1
    assert np.isclose(est.facet_share_.sum(), 1.0)
    assert (np.bincount(est.facet_, minlength=3) > 0).all()
    assert all(r.n_lemma == len(r.contending_set) >= 1 for r in reps)
    assert list(out["diag"].K) == [1, 2, 3]
    assert out["diag"].objective_.is_monotonic_decreasing


def test_figures_written(result):
    regime, out = result
    figs = out["figs"]
    for name in ("log_planes", "frontier_coordinates", "tensions"):
        assert (figs / f"k3_{name}_{regime}.png").stat().st_size > 0


def test_committed_figures_exist_if_script_was_run():
    paths = [
        k_terms.FIGS / f"k3_{n}_{r}.png"
        for n in ("log_planes", "frontier_coordinates", "tensions")
        for r in k_terms.REGIMES
    ]
    if not any(p.exists() for p in paths):
        pytest.skip("k_terms.py has not been run")
    assert all(p.exists() and p.stat().st_size > 0 for p in paths)


def test_no_word_red_in_script():
    assert not re.search(r"\bred\b", SCRIPT.read_text(), flags=re.I)

"""WP9 D-6 / Amendment 3: the K = 1, 2, 3 cubesat script (tau re-selected at each K) runs."""

import re
from pathlib import Path

import k_terms
import numpy as np
import pytest

# Slow module: shared fixtures cost minutes (verification in tiers); not in the fast suite.
pytestmark = pytest.mark.slow

SCRIPT = Path(k_terms.__file__)


@pytest.fixture(scope="module", params=list(k_terms.REGIMES))
def result(request):
    return request.param, k_terms.run_regime(request.param, seeds=[0], verbose=False)


@pytest.mark.slow
def test_k3_fits_and_three_reports(result):
    _, out = result
    est, reps = out["fits"][3], out["reports"][3]
    assert est.exponents_.shape == (3, 8)  # the eight traded metrics (WP23 close-out)
    assert len(reps) == 3 and len(out["reports"][1]) == 1 and len(out["reports"][2]) == 2
    assert np.isclose(est.term_share_.sum(), 1.0)
    assert (np.bincount(est.cell_, minlength=3) > 0).all()
    assert all(r.n_lemma == len(r.contending_set) >= 1 for r in reps)
    assert list(out["diag"].K) == [1, 2, 3] and list(out["fixed_diag"].K) == [1, 2, 3]
    assert out["diag"].objective_.is_monotonic_decreasing


def test_tau_reselected_at_each_k_holds_the_fraction(result):
    regime, out = result
    for K in (1, 2, 3):
        assert abs(out["fits"][K].frac_above_ - 0.10) <= 0.011  # tool tolerance 0.01
        assert out["fits"][K].temperature == out["taus"][K]
    assert out["taus"][1] == pytest.approx({"primary": 38.10, "stock": 45.68}[regime], abs=0.01)
    # the diagnostic reuses K = 1's tau and shows the fraction rising with K
    assert (out["fixed_diag"]["tau"] == round(out["taus"][1], 2)).all()
    assert out["fixed_diag"].frac_above_.iloc[-1] > 0.25


# margin gamma and stable radius of the re-selected fits, as printed (six decimals), on the
# eight-metric data of record (WP23 close-out; the radius scales with the number of metrics)
MARGIN = {
    ("primary", 2): (0.000697, 0.000069), ("primary", 3): (0.001213, 0.000121),
    ("stock", 2): (0.001413, 0.000133), ("stock", 3): (0.000350, 0.000033),
}  # fmt: skip


def test_certificate_margin_and_radius_columns(result):
    regime, out = result
    for table in (out["diag"], out["fixed_diag"]):
        assert {"max gap", "status", "gamma", "radius", "bound"} <= set(table.columns)
        k1, rest = table.iloc[0], table.iloc[1:]
        assert k1.status == "not_applicable" and np.isnan(k1.gamma) and np.isnan(k1.radius)
        assert (rest.status == "certified").all()
        assert (rest["max gap"] < 1e-12).all() and (rest.bound <= rest["max gap"] + 1e-15).all()
        assert (rest.gamma > 0).all() and (rest.radius > 0).all()
    for K in (2, 3):
        row = out["diag"].set_index("K").loc[K]
        gamma, radius = MARGIN[regime, K]
        assert row.gamma == pytest.approx(gamma, abs=5e-7)
        assert row.radius == pytest.approx(radius, abs=5e-7)
    # the per-term gap column of the K = 3 record is the termination record's gaps
    est = out["fits"][3]
    assert np.allclose(out["record"]["gap G_k"], est.termination_.gaps)
    assert (out["record"]["gap G_k"] < 1e-12).all()
    assert (out["stab"].status == "certified").all()


def test_no_word_red_in_script():
    assert not re.search(r"\bred\b", SCRIPT.read_text(encoding="utf-8"), flags=re.I)

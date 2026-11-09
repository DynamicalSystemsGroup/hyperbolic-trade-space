"""Temperature selection (R-4). Planted data, seeds 0, 1, 2; target tolerance 0.01 (n = 400)."""

import numpy as np
import pytest

from hyperbolic_trade_space import HyperbolicTradeSpace, make_frontier_data, select_temperature


def planted(seed, n=400, d=3):
    X, _ = make_frontier_data(n, d, noise=0.05, random_state=seed)
    return X


@pytest.mark.parametrize("seed", [0, 1, 2])
@pytest.mark.parametrize("target", [0.05, 0.10, 0.20])
def test_selected_temperature_hits_target(seed, target):
    X = planted(seed)
    tau = select_temperature(X, target)
    assert 1e-1 <= tau <= 1e4
    frac = HyperbolicTradeSpace(temperature=tau).fit(X).frac_above_
    assert abs(frac - target) <= 0.01


def test_passes_estimator_params_and_default_target():
    X = planted(0)
    tau = select_temperature(X, min_exponent=0.05)
    est = HyperbolicTradeSpace(temperature=tau, min_exponent=0.05).fit(X)
    assert abs(est.frac_above_ - 0.10) <= 0.01
    assert est.exponents_.min() >= 0.05 - 1e-12


def test_tau_sweep_is_monotone_from_half_toward_zero():
    X = planted(1)
    taus = np.logspace(-1, 4, 16)
    fits = [HyperbolicTradeSpace(temperature=t).fit(X) for t in taus]
    frac = np.array([f.frac_above_ for f in fits])
    n_eff = np.array([f.n_eff_ for f in fits])
    # Measured: frac_above_ is near 1/2 at small tau (it can overshoot 1/2 slightly, since the
    # soft maximum tends to the mean of the scores, not the median) and is nonincreasing for
    # tau >= 3, the documented useful range. It is not monotone on the whole of (0.1, 3).
    useful = taus >= 3
    assert (np.diff(frac[useful]) <= 1e-12).all()
    assert 0.4 < frac[0] < 0.65 and frac[-1] < 0.05
    # n_eff moves from N (uniform weights at small tau) toward d (LP vertex support)
    assert n_eff[0] > 0.95 * X.shape[0]
    assert n_eff[-1] < 0.1 * X.shape[0] and n_eff[-1] >= 1
    assert (np.diff(n_eff) <= 0.01).all()  # solver-tolerance slack


def test_not_bracketed_raises():
    X = planted(0)
    with pytest.raises(ValueError, match="not bracketed"):
        select_temperature(X, 0.10, bounds=(500.0, 1e4))  # frac already below target
    with pytest.raises(ValueError, match="not bracketed"):
        select_temperature(X, 0.10, bounds=(0.1, 0.2))  # frac still near 1/2


@pytest.mark.parametrize(
    "kw",
    [
        {"target_frac_above": 0.0},
        {"target_frac_above": 1.0},
        {"bounds": (1.0, 1.0)},
        {"bounds": (-1.0, 10.0)},
        {"temperature": 3.0},
    ],
)
def test_bad_arguments(kw):
    with pytest.raises(ValueError):
        select_temperature(planted(0, n=100), **kw)


def test_step_function_gives_warning_when_tol_unreachable():
    X = planted(0, n=30)
    with pytest.warns(UserWarning, match="closest tau"):
        tau = select_temperature(X, 0.105, tol=1e-6)
    assert np.isfinite(tau)


def test_several_terms_unreachable_target_says_what_to_try():
    """WP10 item 21: at K > 1 the facets are not supporting planes, so frac_above_ levels off
    above zero; the default target is out of reach here and the message says what to try."""
    from hyperbolic_trade_space import HyperbolicTradeSpace, make_frontier_data

    X, _ = make_frontier_data(300, 4, n_terms=2, random_state=777)
    with pytest.raises(ValueError, match="not bracketed") as err:
        select_temperature(X, n_terms=2, random_state=0)
    msg = str(err.value)
    for phrase in ("raise the target to about", "fixed temperature", "widen bounds", "mean_slack_"):
        assert phrase in msg
    # the suggested target is reachable
    floor = HyperbolicTradeSpace(n_terms=2, temperature=1e4, random_state=0).fit(X).frac_above_
    tau = select_temperature(X, floor + 0.04, bounds=(3.0, 1e4), n_terms=2, random_state=0)
    fit = HyperbolicTradeSpace(n_terms=2, temperature=tau, random_state=0).fit(X)
    assert abs(fit.frac_above_ - (floor + 0.04)) <= 0.01

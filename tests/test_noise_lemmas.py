"""Planted-data tests for L18 (noise covariance, conditioning map) and L19 (noise shift bound).

The lemma scripts prove the statements for symbolic d and n; these tests check them on planted
data with fixed seeds, and check that a wrong statement is rejected by the same comparison (the
negative controls). Tolerances are Monte Carlo standard errors, stated in each test.
"""

import importlib
import os

import numpy as np
import pytest
from scipy.special import logsumexp

from derivation.symbols import make_symbols

SEEDS = tuple(
    int(x) for x in os.environ.get("WP29_SEEDS", "0,1").split(",")
)  # a reviewer reruns with others


def _lemma(name):
    mod = importlib.import_module(f"derivation.{name}")
    ctx = {"S": make_symbols()}
    mod.derive(ctx)
    mod.verify(ctx)
    return mod, ctx


def test_both_lemmas_verify_symbolically_and_fail_loudly_when_broken():
    for name, key, fact, bad in (
        ("lemma_18_noise_covariance", "L18", "cumulant", 0),
        ("lemma_19_noise_shift_bound", "L19", "tau_star", 1),
    ):
        mod, ctx = _lemma(name)
        ctx[key][fact] = bad
        with pytest.raises(AssertionError, match=f"{key} FAIL"):
            mod.verify(ctx)


def test_symbolic_negative_controls_a_wrong_statement_fails_loudly():
    """A wrong covariance form, a wrong crossover and a reversed bound each fail their step."""
    import sympy as sp

    mod, ctx = _lemma("lemma_18_noise_covariance")
    S, r = ctx["S"], ctx["L18"]
    wrong = sp.Sum(S.w[S.j] * r["sg"][S.j] ** 2, (S.j, 1, S.d))  # w_j instead of w_j^2
    r["diag_sum"] = wrong
    with pytest.raises(AssertionError, match="L18 FAIL diagonal quadratic form"):
        mod.verify(ctx)
    mod, ctx = _lemma("lemma_18_noise_covariance")
    ctx["L18"]["spread"] = sp.Abs(
        ctx["L18"]["alpha"][ctx["S"].j]
    )  # s_j = |alpha_j|, not its inverse
    with pytest.raises(AssertionError, match="L18 FAIL sigma_j = delta_j / s_j"):
        mod.verify(ctx)
    mod, ctx = _lemma("lemma_19_noise_shift_bound")
    ctx["L19"]["tau_star"] = ctx["L19"]["tau_star"] / 2
    with pytest.raises(AssertionError, match="L19 FAIL crossover"):
        mod.verify(ctx)
    mod, ctx = _lemma("lemma_19_noise_shift_bound")
    ctx["L19"]["first_gap"] = 1  # the shift sits above LME(s) + tau v^2/2 by the Jensen slack
    with pytest.raises(AssertionError, match="L19 FAIL Jensen with the L6 value"):
        mod.verify(ctx)


def test_statements_say_what_they_claim():
    l18 = importlib.import_module("derivation.lemma_18_noise_covariance")
    l19 = importlib.import_module("derivation.lemma_19_noise_shift_bound")
    assert "w'Sigma w / 2" in l18.STATEMENT and "delta_j / s_j" in l18.STATEMENT
    assert "not tight" in l19.STATEMENT and "tau* = 2 sqrt(2 log n) / v" in l19.STATEMENT
    assert "equals neither" in l19.STATEMENT  # no sentence claims equality with a bound
    assert "no noise of their own" in (l18.__doc__ or "").replace("\n", " ")


# ------------------------------------------------------------------ L18: the covariance form
def _cumulant_mc(w, cov, tau, n, seed):
    """(1/tau) log of the sample mean of exp(tau w.eps), eps ~ N(0, cov), and its standard error."""
    rng = np.random.default_rng(seed)
    x = rng.multivariate_normal(np.zeros(len(w)), cov, size=n) @ w
    est = (logsumexp(tau * x) - np.log(n)) / tau
    q = float(w @ cov @ w)
    se = np.sqrt((np.exp(tau**2 * q) - 1) / n) / tau  # delta method on the log of the mean
    return est, se


def _planted(d, seed, diagonal):
    rng = np.random.default_rng(100 + seed)
    w = rng.dirichlet(np.ones(d))
    if diagonal:
        cov = np.diag(rng.uniform(0.01, 0.30, d) ** 2)
        cov[0, 0] = 0.02**2  # unequal levels: one small, the rest larger
    else:
        a = rng.normal(size=(d, d)) * 0.12
        cov = a @ a.T  # symmetric positive semi-definite, correlated
    return w, cov


@pytest.mark.parametrize("seed", SEEDS)
@pytest.mark.parametrize("diagonal", [True, False])
def test_L18_cumulant_is_tau_wSw_over_2_on_planted_noise(seed, diagonal):
    w, cov = _planted(4, seed, diagonal)
    tau = 3.0 / np.sqrt(
        float(w @ cov @ w) * 3.0
    )  # tau^2 q = 3 / 1: moderate, so the mean is stable
    tau = min(tau, 6.0)
    est, se = _cumulant_mc(w, cov, tau, 2_000_000, seed)
    assert abs(est - tau * float(w @ cov @ w) / 2) < 5 * se


@pytest.mark.parametrize("seed", SEEDS)
def test_L18_diagonal_form_matches_the_sum(seed):
    w, cov = _planted(5, seed, True)
    assert np.isclose(w @ cov @ w, np.sum(w**2 * np.diag(cov)))


def _isotropic_reading(w, cov, tau):
    """The L6 form with one sigma, the mean of the sigma_j^2: the A5 reading of unequal noise."""
    return tau * np.mean(np.diag(cov)) * float(w @ w) / 2


@pytest.mark.parametrize("seed", SEEDS)
def test_L18_negative_control_isotropic_form_is_rejected_for_unequal_levels(seed):
    w, cov = _planted(4, seed, True)
    # put the weight where the noise is large: the isotropic reading underestimates the shift
    cov = np.diag([0.02**2, 0.2**2, 0.02**2, 0.02**2])
    w = np.array([0.1, 0.7, 0.1, 0.1])
    tau = 6.0
    est, se = _cumulant_mc(w, cov, tau, 2_000_000, seed)
    right = tau * float(w @ cov @ w) / 2
    wrong = _isotropic_reading(w, cov, tau)
    assert abs(est - right) < 5 * se  # the covariance form holds
    assert abs(est - wrong) > 20 * se  # the isotropic form is rejected by a stated margin
    assert wrong / right < 0.5 or wrong / right > 2  # and it is off by a factor, not a rounding


@pytest.mark.xfail(strict=True, reason="the isotropic reading is wrong for unequal noise levels")
def test_L18_wrong_covariance_form_is_an_expected_failure():
    w = np.array([0.1, 0.7, 0.1, 0.1])
    cov = np.diag([0.02**2, 0.2**2, 0.02**2, 0.02**2])
    est, se = _cumulant_mc(w, cov, 6.0, 2_000_000, 0)
    assert abs(est - _isotropic_reading(w, cov, 6.0)) < 5 * se


# ------------------------------------------------------- L18: the conditioning as a map
def _condition(raw):
    """Log, then standardise by the log spread s_j (the case's log-affine conditioning, a_j = 0)."""
    logs = np.log(raw)
    s = logs.std(axis=0)
    return (logs - logs.mean(axis=0)) / s, s


@pytest.mark.parametrize("seed", SEEDS)
def test_L18_conditioning_maps_log_error_to_sigma_j_equal_delta_over_spread(seed):
    rng = np.random.default_rng(seed)
    n, d = 400_000, 4
    spreads = np.array([0.07, 0.5, 0.8, 0.3])  # the log spread of each raw attribute
    raw = np.exp(rng.normal(size=(n, d)) * spreads + 1.0)
    clean, s = _condition(raw)
    delta = np.array([0.01, 0.01, 0.02, 0.05])
    noisy_raw = raw * np.exp(delta * rng.standard_normal((n, d)))
    # the analyst conditions the noisy table with the clean scaler (the same map u_j(r))
    noisy = (np.log(noisy_raw) - np.log(raw).mean(axis=0)) / s
    sigma = (noisy - clean).std(axis=0)
    assert np.allclose(sigma, delta / s, rtol=0.01)
    # one percent of error on the attribute of spread 0.07 is as large as 0.07/0.8 of that on 0.8
    assert sigma[0] / sigma[2] > 5 * 0.5  # the narrow attribute is the noisy one in the metric
    # negative control: delta without the spread (the unconditioned reading) is off by 1/s
    assert not np.allclose(sigma, delta, rtol=0.2)


# ------------------------------------------------------------------ L19: the sandwich
def _lme(x, tau):
    return (logsumexp(tau * x, axis=-1) - np.log(x.shape[-1])) / tau


def _cell(kind, n, v, tau, reps, seed):
    """(shift, its standard error, lower, L6 bound, E max z, v sqrt(2 log n)) for one cell."""
    rng = np.random.default_rng(seed)
    s = np.zeros(n) if kind == "surface" else -rng.exponential(1.0, n)
    z = v * rng.standard_normal((reps, n))
    per = _lme(s + z, tau) - _lme(s, tau)
    return (
        per.mean(),
        per.std(ddof=1) / np.sqrt(reps),
        s.mean() - _lme(s, tau),
        tau * v**2 / 2,
        z.max(axis=1).mean(),
        v * np.sqrt(2 * np.log(n)),
    )


CELLS = [
    (kind, n, v, tau)
    for kind in ("surface", "interior")
    for n in (100, 1000)
    for v in (0.05, 0.2)
    for tau in (1, 5, 20, 50, 200)
]


@pytest.mark.parametrize("seed", SEEDS)
def test_L19_sandwich_and_the_max_bound_hold_on_planted_cells(seed):
    for kind, n, v, tau in CELLS:
        shift, se, lower, l6, emax, vb = _cell(kind, n, v, tau, 400, 10 * seed + n)
        assert shift >= lower - 4 * se, (kind, n, v, tau)
        assert shift <= min(l6, emax) + 4 * se, (kind, n, v, tau)
        assert emax <= vb  # E max z <= v sqrt(2 log n)


def test_L19_crossover_rule_of_thumb():
    for n, v in ((100, 0.05), (1000, 0.2)):
        tau_star = 2 * np.sqrt(2 * np.log(n)) / v
        assert np.isclose(tau_star * v**2 / 2, v * np.sqrt(2 * np.log(n)))
        # below tau* the L6 value is the smaller upper bound, above it the max bound is
        assert 0.5 * tau_star * v**2 / 2 < v * np.sqrt(2 * np.log(n)) < 2 * tau_star * v**2 / 2


def test_L19_the_bound_is_not_tight():
    """On interior scores at tau = 200 the smaller upper bound exceeds the shift by 1.3 or more,
    and the L6 value alone by 2.5 or more; where tau v^2 / 2 is the smaller bound it is close."""
    for n in (100, 1000):
        for v in (0.05, 0.2):
            shift, _, _, l6, emax, _ = _cell("interior", n, v, 200, 400, n)
            assert min(l6, emax) / shift > 1.3, (n, v)
            assert l6 / shift > 2.5, (n, v)
    shift, _, _, l6, emax, _ = _cell("interior", 1000, 0.05, 5, 400, 5)
    assert l6 < emax and 0.95 < l6 / shift < 1.1  # near equality in the small-tau regime


def test_L19_negative_controls_a_reversed_or_shifted_bound_fails():
    # reversed: "the shift is at most mean - LME" is false where the lower bound is below the shift
    shift, se, lower, l6, _, _ = _cell("surface", 1000, 0.2, 1, 400, 3)
    assert shift > lower + 10 * se
    # tau-shifted: tau v^2 / 8 in place of tau v^2 / 2 is violated where the L6 branch is active
    shift, se, _, l6, emax, _ = _cell("surface", 1000, 0.2, 1, 400, 3)
    assert l6 < emax  # the L6 branch is the active one here
    assert shift > l6 / 4 + 10 * se

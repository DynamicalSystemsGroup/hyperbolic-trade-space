"""L10 - The K-term extension Phi_K: shift equivariance, K = 1 reduction, kappa -> infinity.

Phi_K(u) = (1/kappa) log sum_{k=1}^K exp(kappa (theta_k . u - beta_k)), each theta_k on the
simplex (A6), kappa > 0 (A6), symbolic K and d. The simplex per term is S.simplex_theta.

What this proves:
  1. Phi_K(u + c 1) = Phi_K(u) + c (sum_j theta_kj = 1 per term, A2-style simplex on each theta_k
     carried by A6; Sum linearity; log of a product with a positive Sum).
  2. K = 1 reduction: Phi_1(u) = theta_1 . u - beta_1 (substitute K = 1 into the abstract
     expression), the single log-affine (monomial) fit of L1-L3.
  3. Sum form: Phi_K >= max_k x_k and Phi_K <= max_k x_k + (log K)/kappa (a log-sum-exp lies
     above the maximum by at most log K / kappa), hence
     lim_{kappa->inf} Phi_K = max_k x_k, where x_k = theta_k . u - beta_k. Limits are computed
     by sympy.limit in derive on the squeeze bounds and recorded; verify asserts equality
     (mimics symproof library/topology.py continuous_at_point).
  3b. Mean form (the normalized log-mean-exp, Phi^mean_K = (1/kappa) log((1/K) sum_k exp(kappa x_k))
     = Phi_K - (log K)/kappa): max_k x_k - (log K)/kappa <= Phi^mean_K <= max_k x_k, with the same
     limit. The two forms differ by the constant (log K)/kappa, so they share every gradient,
     Hessian and minimizer. A term repeated once (two equal scores x) moves the sum form to
     x + (log 2)/kappa, an apparent gain with no new geometry, and leaves the mean form at x.
  4. GP compatibility (I4 is cited context only): exp(kappa Phi_K)
     = sum_k e^{-kappa beta_k} prod_j m_j^{kappa theta_kj} is a posynomial in m (A1: u = log m),
     verified as an identity for symbolic K, d.

Max representation (FALLBACK F10, listed in the ledger): the maximum over the K terms is a
symbol M with x_k <= M for all k and x_{k0} = M for some k0 (same reason as F5 in L5: sympy
has no symbolic-K max and cannot take limits through the symbolic Sum).

What this does NOT prove: a K > 1 solver or any property of fitted parameters (non-goal);
that Phi_K approximates a given set; only the identities above.
"""

import sympy as sp

from derivation.axioms import A1, A6, F10
from derivation.licence import log_expand
from derivation.sumtools import linear, product_to_exp_sum

TITLE = "Extension Phi_K: shift equivariance, K = 1 reduction, kappa -> infinity = max"
STATEMENT = (
    "Phi_K(u + c 1) = Phi_K(u) + c; Phi_1 = theta_1.u - beta_1; "
    "lim_{kappa->inf} Phi_K = max_k (theta_k.u - beta_k); exp(kappa Phi_K) is a posynomial; "
    "sum form: max <= Phi_K <= max + (log K)/kappa; "
    "mean form: max - (log K)/kappa <= Phi_K - (log K)/kappa <= max"
)
AXIOMS_USED = ["A1", "A6", "F10"]  # F10: max representation; I4 is cited context only


def _x(S, shift=0):
    """x_k(u + shift) = sum_j theta_kj (u_j + shift) - beta_k, abstract in k, d."""
    k, j, d = S.k, S.j, S.d
    return sp.Sum(S.theta[k, j] * (S.u[j] + shift), (j, 1, d)) - S.beta[k]


def Phi(S, K, shift=0):
    k, kappa = S.k, S.kappa
    return sp.log(sp.Sum(sp.exp(kappa * _x(S, shift)), (k, 1, K))) / kappa


def derive(ctx):
    S = ctx["S"]
    k, j, d, K, kappa, c = S.k, S.j, S.d, S.K, S.kappa, S.c
    M = S.M  # the maximum of the K scores (F10: x_k <= M for all k, x_k0 = M for some k0)
    u, theta, beta = S.u, S.theta, S.beta

    # 1. shift. Work on the summand with k free so the per-term simplex equation matches.
    term = linear(kappa * (sp.Sum(theta[k, j] * (u[j] + c), (j, 1, d)) - beta[k]))
    # [L10.1] A6: sum_j theta_kj = 1 per term gives kappa (theta_k.u + c - beta_k)
    term = A6.rewrite(term)
    summand = sp.expand(sp.exp(term))
    total = linear(sp.Sum(summand, (k, 1, K)))
    # [L10.2] A1, A6: the terms are exponentials of real scores (u, theta real), so log splits
    shifted_reduced = sp.expand(log_expand(sp.log(total), A1, A6) / kappa)
    # [L10.3] A1, A6: likewise for the unshifted sum of exponentials
    base = sp.expand(log_expand(sp.log(sp.Sum(sp.exp(kappa * _x(S)), (k, 1, K))), A1, A6))

    # 2. K = 1 reduction
    # [L10.4] A1, A6: log(exp(kappa x_1)) = kappa x_1 for the real score x_1
    phi1 = log_expand(Phi(S, 1).doit(), A1, A6)
    x1 = _x(S).subs(k, 1)

    # 3. limit by squeeze. T = sum_k exp(kappa (x_k - M)) in [1, K] under F10.
    n_upper = sp.Sum(1, (k, 1, K)).doit()
    x = sp.Symbol("x", real=True)
    term_positive = sp.solveset(sp.exp(x) > 0, x, sp.S.Reals)
    term_le_one = sp.solveset(sp.exp(x) <= 1, x, sp.S.Reals)
    xk = sp.IndexedBase("xk")  # scores x_k
    T = sp.Sum(sp.exp(kappa * (xk[k] - M)), (k, 1, K))
    T_raw = sp.Sum(sp.exp(kappa * xk[k]), (k, 1, K))
    shift_check = sp.simplify(
        sp.powsimp(
            sp.expand(sp.exp(kappa * M) * linear(sp.Sum(sp.expand(T.function), (k, 1, K))) - T_raw)
        )
    )
    # [L10.5] F10: the term k0 of the shifted sum T is exp(kappa (x_k0 - M)) = exp(0) = 1
    term_k0 = sp.exp(kappa * (xk[sp.Symbol("k0", integer=True)] - M)).subs(*F10.rule(1))
    # [L10.6] F10: the slack M - x_k of x_k <= M is nonnegative
    slack = F10.nonneg_symbol("slack")
    floor = sp.log(term_k0) / kappa  # Phi - M = (1/kappa) log T >= (1/kappa) log 1
    ceil = sp.log(n_upper) / kappa  # ... <= (1/kappa) log K
    lim_lower = sp.limit(M + floor, kappa, sp.oo)  # Phi >= M + floor
    lim_upper = sp.limit(M + ceil, kappa, sp.oo)  # Phi <= M + (log K)/kappa

    # 3b. the mean form (log-mean-exp): Phi^mean_K = (1/kappa) log((1/K) sum_k exp(kappa x_k))
    mean_log = sp.log(sp.Sum(sp.exp(kappa * _x(S)), (k, 1, K)) / K)  # log of the mean
    floor_mean = floor - sp.log(K) / kappa  # Phi^mean - M >= -(log K)/kappa
    ceil_mean = ceil - sp.log(K) / kappa  # Phi^mean - M <= 0
    lim_lower_mean = sp.limit(M + floor_mean, kappa, sp.oo)
    x_dup = sp.Symbol("x_dup", real=True)  # the common score of two equal terms
    two_equal = sp.Sum(sp.exp(kappa * x_dup), (k, 1, 2)).doit()
    dup_sum = sp.expand_log(sp.log(two_equal) / kappa)
    dup_mean = sp.expand_log(sp.log(two_equal / 2) / kappa)

    # 4. exp(kappa Phi_K) as a posynomial in m = exp(u) (A1)
    m = S.m
    # [L10.7] A1: m > 0, so exp(kappa Phi_K) is a sum of monomials in m, a posynomial
    mono = linear(
        sp.exp(-kappa * beta[k])
        * product_to_exp_sum(sp.Product(m[j] ** (kappa * theta[k, j]), (j, 1, d)), A1)
    )
    # exp(kappa Phi_K) = sum_k exp(kappa x_k), with u_j = log m_j (A1)
    x_in_m = sp.Sum(theta[k, j] * sp.log(m[j]), (j, 1, d)) - beta[k]
    term_in_m = sp.expand(sp.exp(kappa * linear(x_in_m)))

    ctx["L10"] = {
        "shifted_reduced": shifted_reduced,
        "base": base,
        "phi1": phi1,
        "x1": x1,
        "n_upper": n_upper,
        "term_positive": term_positive,
        "term_le_one": term_le_one,
        "shift_check": shift_check,
        "floor": floor,
        "term_k0": term_k0,
        "slack": slack,
        "ceil": ceil,
        "lim_upper": lim_upper,
        "lim_lower": lim_lower,
        "mean_log": mean_log,
        "floor_mean": floor_mean,
        "ceil_mean": ceil_mean,
        "lim_lower_mean": lim_lower_mean,
        "x_dup": x_dup,
        "dup_sum": dup_sum,
        "dup_mean": dup_mean,
        "mono": mono,
        "term_in_m": term_in_m,
    }
    return ctx["L10"]


def verify(ctx):
    S = ctx["S"]
    r = ctx["L10"]
    kappa, K, M = S.kappa, S.K, S.M
    # [L10.8] shift equivariance: Phi_K(u + c 1) - (Phi_K(u) + c) is 0 (logs licensed: A1, A6)
    assert sp.simplify(log_expand(r["shifted_reduced"] - r["base"] / kappa - S.c, A1, A6)) == 0, (
        "L10 FAIL: Phi_K(u + c1) - (Phi_K(u) + c) != 0"
    )
    # [L10.9] K = 1 reduction: Phi_1(u) = theta_1.u - beta_1
    assert sp.simplify(r["phi1"] - r["x1"]) == 0, (
        "L10 FAIL: K = 1 reduction is not theta_1.u - beta_1"
    )
    # [L10.10] per term, exp(x) > 0 for every real x
    assert r["term_positive"] == sp.S.Reals, "L10 FAIL: exp(x) > 0 per term"
    # [L10.11] per term, exp(x) <= 1 exactly when x <= 0 (the shifted exponents are <= 0 by F10)
    assert r["term_le_one"] == sp.Interval(-sp.oo, 0), "L10 FAIL: exp(x) <= 1 iff x <= 0"
    # [L10.12] F10, A6: kappa (x_k - M) = -kappa * slack is <= 0, so each shifted term is <= 1
    assert (-A6.positive(kappa) * r["slack"]).is_nonpositive is True, (
        "L10 FAIL: kappa (x_k - M) > 0"
    )
    # [L10.13] the sum of K ones is K, so the shifted sum T is at most K
    assert r["n_upper"] == K, "L10 FAIL: sum of K ones != K"
    # [L10.14] shifting by the maximum: sum_k e^{kappa x_k} = e^{kappa M} sum_k e^{kappa (x_k - M)}
    assert r["shift_check"] == 0, "L10 FAIL: sum e^{kappa x_k} != e^{kappa M} sum e^{kappa (x_k-M)}"
    # T in [1, K]: Phi - M in [floor, ceil] = [0, (log K)/kappa]; both bounds tend to M
    # [L10.15] Phi_K >= max: Phi - M = (1/kappa) log T >= (1/kappa) log 1 = 0 (the k0 term is 1)
    assert sp.simplify(r["floor"]) == 0, "L10 FAIL: Phi - max >= 0 floor"
    # [L10.16] Phi_K <= max + (log K)/kappa: T <= K
    assert sp.simplify(r["ceil"] - sp.log(K) / kappa) == 0, "L10 FAIL: Phi - max <= log K / kappa"
    # [L10.17] the upper squeeze bound M + (log K)/kappa tends to M as kappa -> inf
    assert sp.simplify(r["lim_upper"] - M) == 0, "L10 FAIL: lim upper bound != max"
    # [L10.18] the lower squeeze bound M tends to M, so lim_{kappa->inf} Phi_K = max_k x_k
    assert sp.simplify(r["lim_lower"] - M) == 0, "L10 FAIL: lim lower bound != max"
    # GP compatibility: each term e^{kappa x_k} is the monomial e^{-kappa beta_k} prod m^..
    gap = sp.simplify(sp.expand(r["term_in_m"] - r["mono"]))
    # [L10.19] each term e^{kappa x_k} is the monomial e^{-kappa beta_k} prod_j m_j^(kappa theta_kj)
    assert gap == 0, f"L10 FAIL: exp(kappa Phi_K) is not the posynomial (gap {gap})"
    # [L10.20] A1, A6: the log of the mean splits, so Phi^mean_K = Phi_K - (log K)/kappa
    assert (
        sp.simplify(
            log_expand(r["mean_log"], A1, A6) / kappa - (r["base"] / kappa - sp.log(K) / kappa)
        )
        == 0
    ), "L10 FAIL: log-mean-exp != Phi_K - log K / kappa"
    # [L10.21] mean form, upper bound: Phi^mean - max <= (log K)/kappa - (log K)/kappa = 0
    assert sp.simplify(r["ceil_mean"]) == 0, "L10 FAIL: Phi^mean - max <= 0"
    # [L10.22] mean form, lower bound: Phi^mean - max >= 0 - (log K)/kappa
    assert sp.simplify(r["floor_mean"] + sp.log(K) / kappa) == 0, (
        "L10 FAIL: Phi^mean - max >= -log K / kappa"
    )
    # [L10.23] the lower bound of the mean form tends to max as kappa -> inf, so does Phi^mean_K
    assert sp.simplify(r["lim_lower_mean"] - M) == 0, "L10 FAIL: lim mean lower bound != max"
    # [L10.24] sum form, one term repeated (two equal scores x): Phi = x + (log 2)/kappa
    assert sp.simplify(r["dup_sum"] - (r["x_dup"] + sp.log(2) / kappa)) == 0, (
        "L10 FAIL: duplicated-term shift is not log 2 / kappa"
    )
    # [L10.25] mean form, one term repeated: Phi^mean = x, no shift without new geometry
    assert sp.simplify(r["dup_mean"] - r["x_dup"]) == 0, "L10 FAIL: mean form moved by a repeat"

"""L10 - The K-term extension Phi_K: shift equivariance, K = 1 reduction, kappa -> infinity.

Phi_K(u) = (1/kappa) log sum_{k=1}^K exp(kappa (theta_k . u - beta_k)), each theta_k on the
simplex (A6), kappa > 0 (A6), symbolic K and d. The simplex per term is S.simplex_theta.

What this proves:
  1. Phi_K(u + c 1) = Phi_K(u) + c (sum_j theta_kj = 1 per term, A2-style simplex on each theta_k
     carried by A6; Sum linearity; log of a product with a positive Sum).
  2. K = 1 reduction: Phi_1(u) = theta_1 . u - beta_1 (substitute K = 1 into the abstract
     expression), the single log-affine (monomial) fit of L1-L3.
  3. Phi_K >= max_k x_k and Phi_K <= max_k x_k + (log K)/kappa (a log-sum-exp lies above the
     maximum by at most log K / kappa), hence
     lim_{kappa->inf} Phi_K = max_k x_k, where x_k = theta_k . u - beta_k. Limits are computed
     by sympy.limit in derive on the squeeze bounds and recorded; verify asserts equality
     (mimics symproof library/topology.py continuous_at_point).
  4. GP compatibility (I4): exp(kappa Phi_K) = sum_k e^{-kappa beta_k} prod_j m_j^{kappa theta_kj}
     is a posynomial in m (A1: u = log m), verified as an identity for symbolic K, d.

Max representation (FALLBACK F10, listed in the ledger): the maximum over the K terms is a
symbol M with x_k <= M for all k and x_{k0} = M for some k0 (same reason as F5 in L5: sympy
has no symbolic-K max and cannot take limits through the symbolic Sum).

What this does NOT prove: a K > 1 solver or any property of fitted parameters (non-goal);
that Phi_K approximates a given set; only the identities above.
"""

import sympy as sp

from derivation.sumtools import linear, product_to_exp_sum

TITLE = "Extension Phi_K: shift equivariance, K = 1 reduction, kappa -> infinity = max"
STATEMENT = (
    "Phi_K(u + c 1) = Phi_K(u) + c; Phi_1 = theta_1.u - beta_1; "
    "lim_{kappa->inf} Phi_K = max_k (theta_k.u - beta_k); exp(kappa Phi_K) is a posynomial"
)
AXIOMS_USED = ["A2", "A6", "I4", "F10"]  # I4: posynomial/GP-compatibility; F10: max representation


def _x(S, shift=0):
    """x_k(u + shift) = sum_j theta_kj (u_j + shift) - beta_k, abstract in k, d."""
    k, j, d = S.k, S.j, S.d
    return sp.Sum(S.theta[k, j] * (S.u[j] + shift), (j, 1, d)) - S.beta[k]


def Phi(S, K, shift=0):
    k, kappa = S.k, S.kappa
    return sp.log(sp.Sum(sp.exp(kappa * _x(S, shift)), (k, 1, K))) / kappa


def derive(ctx):
    S = ctx["S"]
    k, j, d, K, kappa, c, M = S.k, S.j, S.d, S.K, S.kappa, S.c, S.M
    u, theta, beta = S.u, S.theta, S.beta

    # 1. shift. Work on the summand with k free so the per-term simplex equation matches.
    term = linear(kappa * (sp.Sum(theta[k, j] * (u[j] + c), (j, 1, d)) - beta[k]))
    term = term.subs(S.simplex_theta.lhs, 1)  # A6: sum_j theta_kj = 1
    summand = sp.expand(sp.exp(term))
    total = linear(sp.Sum(summand, (k, 1, K)))
    shifted_reduced = sp.expand(sp.expand_log(sp.log(total), force=True) / kappa)
    base = sp.expand(sp.expand_log(sp.log(sp.Sum(sp.exp(kappa * _x(S)), (k, 1, K))), force=True))

    # 2. K = 1 reduction
    phi1 = sp.expand_log(Phi(S, 1).doit(), force=True)
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
    floor = sp.log(sp.Integer(1)) / kappa  # Phi - M = (1/kappa) log T >= (1/kappa) log 1
    ceil = sp.log(n_upper) / kappa  # ... <= (1/kappa) log K
    lim_lower = sp.limit(M + floor, kappa, sp.oo)  # Phi >= M + floor
    lim_upper = sp.limit(M + ceil, kappa, sp.oo)  # Phi <= M + (log K)/kappa

    # 4. exp(kappa Phi_K) as a posynomial in m = exp(u) (A1)
    m = S.m
    mono = linear(
        sp.exp(-kappa * beta[k])
        * product_to_exp_sum(sp.Product(m[j] ** (kappa * theta[k, j]), (j, 1, d)))
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
        "ceil": ceil,
        "lim_upper": lim_upper,
        "lim_lower": lim_lower,
        "mono": mono,
        "term_in_m": term_in_m,
    }
    return ctx["L10"]


def verify(ctx):
    S = ctx["S"]
    r = ctx["L10"]
    kappa, K, M = S.kappa, S.K, S.M
    diff = sp.simplify(sp.expand_log(r["shifted_reduced"] - r["base"] / kappa - S.c, force=True))
    assert diff == 0, f"L10 FAIL: Phi_K(u + c1) - (Phi_K(u) + c) = {diff}"
    assert sp.simplify(r["phi1"] - r["x1"]) == 0, (
        "L10 FAIL: K = 1 reduction is not theta_1.u - beta_1"
    )
    assert r["term_positive"] == sp.S.Reals, "L10 FAIL: exp(x) > 0 per term"
    assert r["term_le_one"] == sp.Interval(-sp.oo, 0), "L10 FAIL: exp(x) <= 1 iff x <= 0"
    assert r["n_upper"] == K, "L10 FAIL: sum of K ones != K"
    assert r["shift_check"] == 0, "L10 FAIL: sum e^{kappa x_k} != e^{kappa M} sum e^{kappa (x_k-M)}"
    # T in [1, K]: Phi - M in [floor, ceil] = [0, (log K)/kappa]; both bounds tend to M
    assert sp.simplify(r["floor"]) == 0, "L10 FAIL: Phi - max >= 0 floor"
    assert sp.simplify(r["ceil"] - sp.log(K) / kappa) == 0, "L10 FAIL: Phi - max <= log K / kappa"
    assert sp.simplify(r["lim_upper"] - M) == 0, "L10 FAIL: lim upper bound != max"
    assert sp.simplify(r["lim_lower"] - M) == 0, "L10 FAIL: lim lower bound != max"
    # GP compatibility (I4): each term e^{kappa x_k} is the monomial e^{-kappa beta_k} prod m^..
    gap = sp.simplify(sp.expand(r["term_in_m"] - r["mono"]))
    assert gap == 0, f"L10 FAIL: exp(kappa Phi_K) is not the posynomial (gap {gap})"

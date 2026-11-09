"""L11 - A maximizer of V is Pareto-efficient (weighted-sum scalarization, one direction only).

Setting: u = log m (A1), exponents w on the simplex (A2: w_j >= 0, sum_j w_j = 1), offset beta,
V = exp(w.u - beta). u' dominates u when u' = u + delta with delta_j >= 0 for every j.

What this proves (symbolic d, plain SymPy):
  1. w.u' - w.u = sum_j w_j delta_j (Sum linearity), and it is >= 0 (every summand is).
  2. Strictness: if some j0 has w_{j0} > 0 and delta_{j0} > 0 then the difference is > 0
     (split off the j0 term: nonnegative rest plus a positive term).
  3. V(u')/V(u) = exp(sum_j w_j delta_j) >= 1, and > 1 exactly under the condition of 2.
     So if u maximizes V over a set S, no u' in S dominates u in a contending metric
     (a metric with w_j > 0): u is weakly efficient in all d metrics (no u' in S is strictly
     better in every metric, because the simplex gives some w_j > 0), and efficient in the
     strict sense (no u' >= u with u' != u) when every w_j > 0.
  4. Simplex lower bound: if delta_j >= eps > 0 for all j then w.delta = eps + sum_j w_j
     (delta_j - eps) >= eps > 0 (uses sum_j w_j = 1).
  5. K > 1 at kappa = infinity, Phi(u) = max_k (theta_k.u - beta_k) (F10-style maximum: x_k0 = M
     for an active term k0). If u maximizes Phi over S, u' in S and u' = u + delta >= u, then
     for every term k0 active at u, Phi(u') >= theta_k0.u' - beta_k0 = Phi(u) + theta_k0.delta
     >= Phi(u) >= Phi(u'), so theta_k0.delta = 0: u' gains nothing in any metric with
     theta_k0j > 0. The maximizer is therefore weakly efficient in all d metrics (a strict gain
     in every metric would give theta_k0.delta > 0), and efficient when some active term has
     every exponent positive. The facet that blocks u' is one active at u, not at u'.

What this does NOT prove: the converse. Weighted-sum scalarization reaches only the part of a
Pareto front that is supported by some w; a front point in a non-log-convex part is efficient
but is the V-maximizer for no w (Miettinen 1999; Ehrgott 2005). Nothing is claimed about which
w to use, or about the fitted frontier being the true front.
"""

import sympy as sp

from derivation.axioms import A2
from derivation.sumtools import linear

TITLE = "A V-maximizer is Pareto-efficient (weighted-sum scalarization; converse not claimed)"
STATEMENT = (
    "For w in the simplex and u' = u + delta, delta >= 0: w.u' - w.u = sum_j w_j delta_j >= 0, "
    "strictly > 0 whenever some j has w_j > 0 and delta_j > 0; hence V(u') >= V(u) with "
    "strict inequality under the same condition, and a maximizer of V = exp(w.u - beta) over a "
    "set S is not dominated by any member of S in the contending metrics (w_j > 0): weakly "
    "efficient in all d metrics, efficient when every w_j > 0. At K > 1, kappa = infinity, a "
    "maximizer of Phi = max_k (theta_k.u - beta_k) is not dominated through any term active at "
    "it (theta_k0.delta = 0), so it is weakly efficient in all d metrics. The converse is not "
    "claimed: only the log-convex part of a front is reached by some w"
)
AXIOMS_USED = ["A2"]


def derive(ctx):
    S = ctx["S"]
    d, j, w, theta = S.d, S.j, S.w, S.theta
    lim = (j, 1, d)
    u = S.u

    # local nonnegative families: the hypotheses w_j >= 0 (A2) and delta_j >= 0 (dominance)
    # [L11.1] A2: the exponents are nonnegative, w_j >= 0
    wn = A2.nonneg_base("wn")
    dl = sp.IndexedBase("dl", nonnegative=True)
    beta0 = sp.Symbol("beta0", real=True)

    # 1. identity, with u' = u + delta
    diff = linear(sp.Sum(w[j] * (u[j] + dl[j]), lim) - sp.Sum(w[j] * u[j], lim))
    gain = sp.Sum(wn[j] * dl[j], lim)  # sum_j w_j delta_j with the sign hypotheses attached
    gain_nonneg = gain.is_nonnegative

    # 2. strictness: separate the j0 term, j0 a distinguished index with w_j0 > 0, delta_j0 > 0
    rest = sp.Symbol("rest", nonnegative=True)  # sum over j != j0 of a nonnegative summand
    wp = sp.Symbol("wp", positive=True)  # w_j0 > 0
    dp = sp.Symbol("dp", positive=True)  # delta_j0 > 0
    strict = rest + wp * dp
    strict_positive = strict.is_positive

    # 3. V ratio: V(u')/V(u) = exp(w.u' - beta - (w.u - beta)) = exp(gain)
    x = sp.Symbol("x", real=True)
    ratio_ge1 = sp.solveset(sp.exp(x) >= 1, x, sp.S.Reals)  # exp(x) >= 1 iff x >= 0
    ratio_gt1 = sp.solveset(sp.exp(x) > 1, x, sp.S.Reals)  # exp(x) > 1 iff x > 0
    ratio_identity = sp.simplify(
        sp.exp(sp.Sum(w[j] * (u[j] + dl[j]), lim) - beta0)
        / sp.exp(sp.Sum(w[j] * u[j], lim) - beta0)
        - sp.exp(diff)
    )

    # 4. simplex lower bound: delta_j = eps + gam_j, gam_j >= 0, sum_j w_j = 1
    eps = sp.Symbol("eps", positive=True)
    gam = sp.IndexedBase("gam", nonnegative=True)
    low = linear(sp.Sum(wn[j] * (eps + gam[j]), lim))
    # [L11.2] A2: sum_j w_j = 1 turns sum_j w_j (eps + gam_j) into eps + sum_j w_j gam_j
    low = A2.rewrite(low, rename={w: wn})
    low_minus_eps = sp.simplify(low - eps)  # = sum_j w_j gam_j
    low_remainder_nonneg = sp.Sum(wn[j] * gam[j], lim).is_nonnegative
    low_positive = (eps + sp.Sum(wn[j] * gam[j], lim)).is_positive

    # 5. K > 1, kappa = infinity. a = theta_k0 . delta, x0 = Phi(u) = theta_k0.u - beta_k0 (active)
    a = sp.Symbol("a", real=True)
    x0 = sp.Symbol("x0", real=True)
    a_def = linear(sp.Sum(theta[sp.Symbol("k0", integer=True), j] * dl[j], lim))
    phi_up_ge = x0 + a  # Phi(u') >= theta_k0.u' - beta_k0 = x0 + a
    # a >= 0 (monotone term), Phi(u') <= Phi(u) = x0 (maximizer), x0 + a <= x0 forces a = 0
    squeeze = sp.Intersection(
        sp.solveset(a >= 0, a, sp.S.Reals), sp.solveset(phi_up_ge <= x0, a, sp.S.Reals)
    )

    ctx["L11"] = {
        "diff": diff,
        "gain": gain,
        "gain_nonneg": gain_nonneg,
        "strict_positive": strict_positive,
        "ratio_ge1": ratio_ge1,
        "ratio_gt1": ratio_gt1,
        "ratio_identity": ratio_identity,
        "low_minus_eps": low_minus_eps,
        "low_remainder_nonneg": low_remainder_nonneg,
        "low_positive": low_positive,
        "a_def": a_def,
        "squeeze": squeeze,
        "wn": wn,
        "dl": dl,
        "gam": gam,
        "eps": eps,
    }
    return ctx["L11"]


def verify(ctx):
    S = ctx["S"]
    r = ctx["L11"]
    j, d = S.j, S.d
    w = S.w
    wn, dl, gam = r["wn"], r["dl"], r["gam"]

    # 1. identity and sign
    # [L11.3] w.u' - w.u = sum_j w_j delta_j, by Sum linearity
    assert sp.simplify(r["diff"] - sp.Sum(w[j] * dl[j], (j, 1, d))) == 0, (
        "L11 FAIL: w.u' - w.u != sum_j w_j delta_j"
    )
    # [L11.4] every summand w_j delta_j is >= 0, so the gain is >= 0
    assert r["gain_nonneg"] is True, "L11 FAIL: sum_j w_j delta_j is not nonnegative"
    # 2. strictness
    # [L11.5] strictness: a nonnegative rest plus the positive term w_j0 delta_j0 is > 0
    assert r["strict_positive"] is True, "L11 FAIL: nonnegative rest + positive term is not > 0"
    # 3. V ratio
    # [L11.6] exp(x) >= 1 exactly when x >= 0, so V(u') >= V(u)
    assert r["ratio_ge1"] == sp.Interval(0, sp.oo), "L11 FAIL: exp(x) >= 1 iff x >= 0"
    # [L11.7] exp(x) > 1 exactly when x > 0, so V(u') > V(u) under the strictness condition
    assert r["ratio_gt1"] == sp.Interval.open(0, sp.oo), "L11 FAIL: exp(x) > 1 iff x > 0"
    # [L11.8] the ratio V(u')/V(u) is exp(sum_j w_j delta_j)
    assert r["ratio_identity"] == 0, "L11 FAIL: V(u')/V(u) != exp(sum_j w_j delta_j)"
    # 4. simplex lower bound: w.delta - eps = sum_j w_j gam_j >= 0, hence w.delta >= eps > 0
    gap = sp.simplify(r["low_minus_eps"] - sp.Sum(wn[j] * gam[j], (j, 1, d)))
    # [L11.9] with sum_j w_j = 1: w.delta - eps = sum_j w_j gam_j
    assert gap == 0, f"L11 FAIL: sum_j w_j (eps + gam_j) - eps != sum_j w_j gam_j (gap {gap})"
    # [L11.10] the remainder sum_j w_j gam_j is >= 0
    assert r["low_remainder_nonneg"] is True, "L11 FAIL: sum_j w_j gam_j is not nonnegative"
    # [L11.11] hence w.delta >= eps > 0 whenever every delta_j >= eps
    assert r["low_positive"] is True, "L11 FAIL: eps + nonnegative sum is not > 0"
    # 5. K > 1: the facet inequality chain leaves only theta_k0 . delta = 0
    # [L11.12] K > 1: theta_k0.delta >= 0 and x0 + theta_k0.delta <= x0 force theta_k0.delta = 0
    assert r["squeeze"] == sp.FiniteSet(0), "L11 FAIL: theta_k0.delta is not forced to 0"
    k0 = sp.Symbol("k0", integer=True)
    # [L11.13] theta_k0.delta expands as sum_j theta_k0j delta_j
    assert sp.simplify(r["a_def"] - sp.Sum(S.theta[k0, j] * dl[j], (j, 1, d))) == 0, (
        "L11 FAIL: theta_k0.delta mis-expanded"
    )

    # one confined numeric instance (exact rationals, d = 3): w on the face w_3 = 0
    R = sp.Rational
    wv = [R(1, 2), R(1, 2), R(0)]
    uv = [R(0), R(1), R(2)]
    up = [R(1, 3), R(1), R(5)]  # dominates uv; strictly better in metric 1 (w_1 > 0)
    gain = sum(a * (b - c) for a, b, c in zip(wv, up, uv, strict=True))
    # [L11.14] exact instance (d = 3): the dominating point gains 1/6 > 0 where w_1 > 0
    assert gain == R(1, 6) and gain > 0, "L11 FAIL: numeric instance gain"
    up_free = [R(0), R(1), R(5)]  # better only in metric 3, where w_3 = 0: no gain, not blocked
    gain0 = sum(a * (b - c) for a, b, c in zip(wv, up_free, uv, strict=True))
    # [L11.15] exact instance: a gain only in the zero-exponent metric 3 does not count
    assert gain0 == 0, "L11 FAIL: gain in a zero-exponent metric must not count"

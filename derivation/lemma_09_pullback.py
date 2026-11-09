"""L9 - Pull-back through the conditioning: V in terms of the raw attributes.

Conditioning (A4): log m_j = alpha_j log(a_j + s_j) + b_j with alpha_j != 0, where s_j is the
raw attribute (the score s here is the raw attribute, not the L5 score) and a_j + s_j > 0.
Model (L1): log V = w.u - beta, with u_j = log m_j (A1).

What this proves (symbolic d):
  V = e^{w.b - beta} * prod_j (a_j + s_j)^{w_j alpha_j}, using sum_j w_j = 1 (A2) where the
  offset beta is absorbed through the invariant form m~ = m e^{-beta} (each factor
  (m_j e^{-beta})^{w_j}, total e^{-beta sum_j w_j} = e^{-beta}).
  Also the conditioning is invertible (alpha_j != 0): s_j = exp((u_j - b_j)/alpha_j) - a_j, so
  the pull-back is a bijection between raw attributes and log metrics. A negative alpha_j
  gives a negative exponent w_j alpha_j on (a_j + s_j): a cost attribute (smaller is better).

What this does NOT prove: that a given conditioning (a, alpha, b) is appropriate, or any
statistical property of the pulled-back fit; A4 is posited, not derived.

Route: log space; the Product is rewritten as exp of Sum (sumtools.product_to_exp_sum, the
log of a power expanded because a_j + s_j > 0 is part of A4's domain), Sum linearity, simplex
substitution. No differentiation or limits.
"""

import sympy as sp

from derivation.axioms import A1, A2, A4
from derivation.sumtools import linear, product_to_exp_sum

TITLE = "Pull-back: V = e^{w.b - beta} prod_j (a_j + s_j)^{w_j alpha_j}"
STATEMENT = "V = e^{w.b - beta} Prod_j (a_j + s_j)^{w_j alpha_j}; conditioning invertible"
AXIOMS_USED = ["A1", "A2", "A4"]


def derive(ctx):
    S = ctx["S"]
    d, j, w, a, alpha, b, beta0 = S.d, S.j, S.w, S.a, S.alpha, S.b, sp.Symbol("beta0", real=True)
    s_raw = sp.IndexedBase("r")  # raw attribute r_j; a_j + r_j > 0 (domain of A4)
    lim = (j, 1, d)

    # [L9.1] A1: u_j = log m_j is defined because m_j > 0
    u_j = A1.invoke(S.u[j])
    # [L9.2] A4: log m_j = alpha_j log(a_j + r_j) + b_j for the raw attribute r_j
    u = A4.rewrite(u_j)
    # invariant form: m~_j = m_j e^{-beta}; log of (m~_j)^{w_j}
    # [L9.3] A2: sum_j w_j = 1 absorbs the offset: sum_j w_j (u_j - beta) = w.u - beta
    logV = A2.rewrite(linear(sp.Sum(w[j] * (u - beta0), lim)))
    V_derived = sp.exp(logV)

    prod = sp.Product((a[j] + s_raw[j]) ** (w[j] * alpha[j]), lim)
    # [L9.4] A4: a_j + r_j > 0 licenses the log of the power (a_j + r_j)^(w_j alpha_j)
    target_exp = sp.exp(sp.Sum(w[j] * b[j], lim) - beta0) * product_to_exp_sum(prod, A4)

    # invertibility (alpha_j != 0): u_j -> s_j -> u_j
    uj = sp.Symbol("uj", real=True)
    s_back = sp.exp((uj - b[j]) / alpha[j]) - a[j]
    # [L9.5] A4: alpha_j != 0 and a_j + r_j > 0, so the conditioning inverts: u -> r -> u
    u_again = alpha[j] * A4.force_log(sp.log(a[j] + s_back)) + b[j]

    ctx["L9"] = {
        "V_derived": V_derived,
        "target": target_exp,
        "beta0": beta0,
        "u_again": u_again,
        "uj": uj,
        "s_raw": s_raw,
    }
    return ctx["L9"]


def verify(ctx):
    S = ctx["S"]
    r = ctx["L9"]
    lhs = sp.expand(sp.expand_power_exp(r["V_derived"]))
    rhs = sp.expand(sp.expand_power_exp(r["target"]))
    # [L9.6] V = e^{w.b - beta} prod_j (a_j + r_j)^{w_j alpha_j}
    assert sp.simplify(lhs - rhs) == 0, "L9 FAIL: V != e^{w.b-beta} prod (a_j+s_j)^{w_j alpha_j}"
    # [L9.7] the conditioning is invertible: the round trip returns u_j
    assert sp.simplify(r["u_again"] - r["uj"]) == 0, "L9 FAIL: conditioning is not invertible"
    # simplex substitution was actually needed: beta enters only through sum_j w_j
    # [L9.8] the offset enters only through sum_j w_j, which A2 sets to 1
    assert S.simplex.lhs not in r["V_derived"].atoms(sp.Sum), "L9 FAIL: simplex not substituted"

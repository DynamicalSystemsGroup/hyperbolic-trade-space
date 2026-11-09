"""L1 - Homogeneity and the invariant form of the weighted geometric mean.

What this proves (for symbolic d, all w on the simplex):
  * V(m) = prod_j m_j^{w_j} = exp(sum_j w_j log m_j) (A1 licenses the log).
  * V(k m) = k V(m) for every scale k > 0 (homogeneity of degree 1), using sum_j w_j = 1 (A2).
  * V(m / V(m)) = 1: dividing by V puts the point on the frontier (the invariant form).
  * Corollary: with the offset beta, m~ = m e^{-beta} gives V(m~) = e^{-beta} V(m), so
    log V = w.u - beta and V(m~) = 1 exactly when V(m) = e^{beta}.

What this does NOT prove: anything about how w or beta are fitted (L3-L5), or non-simplex
exponents (the degree of homogeneity would then be sum_j w_j, not 1).

Route: log space. Products are rewritten as exp of Sum (sumtools.product_to_exp_sum), Sum
linearity and constant factoring are done by sumtools.linear, and the simplex equation
(S.simplex) is substituted. No differentiation, no limits, no enumeration.
"""

import sympy as sp

from derivation.axioms import A1, A2
from derivation.sumtools import linear, product_to_exp_sum

TITLE = "Homogeneity and invariant form: V(k m) = k V(m), V(m / V) = 1"
STATEMENT = (
    "V(m) = prod_j m_j^{w_j}; V(k m) = k V(m) for k > 0; V(m / V(m)) = 1; "
    "V(m e^{-beta}) = e^{-beta} V(m)"
)
AXIOMS_USED = ["A1", "A2"]


def _subs_simplex(expr, S):
    # [L1.1] A2: the simplex sum_j w_j is replaced by 1 wherever it appears
    return A2.rewrite(expr)


def derive(ctx):
    S = ctx["S"]
    d, j, w, m, k = S.d, S.j, S.w, S.m, S.k_scale
    lim = (j, 1, d)

    # V as a Product, and in log space (A1: m_j > 0 so log(m_j^{w_j}) = w_j log m_j).
    V_prod = sp.Product(m[j] ** w[j], lim)
    logV = sp.Sum(w[j] * sp.log(m[j]), lim)
    V = sp.exp(logV)
    # [L1.2] A1 (m_j > 0) licenses log(m_j^w_j) = w_j log m_j: V is exp of a Sum
    V_prod_as_exp = product_to_exp_sum(V_prod, A1)

    # Homogeneity: V(k m).
    # [L1.3] A1 again for the scaled point k m: (k m_j)^w_j in log space
    Vk_exp = product_to_exp_sum(sp.Product((k * m[j]) ** w[j], lim), A1)
    Vk = sp.expand(_subs_simplex(linear(Vk_exp), S))  # -> k * exp(sum w log m)

    # Invariant form: m / V(m), with log(m_j / V) = log m_j - logV (V = exp(logV) > 0).
    LV = sp.Symbol("LV", real=True)  # stands for log V(m); real since V > 0
    inv_exp = sp.exp(sp.Sum(w[j] * (sp.log(m[j]) - LV), lim))
    inv_lin = _subs_simplex(linear(inv_exp), S)  # exp(logV - LV)
    V_inv_form = sp.expand(inv_lin.subs(LV, logV))

    # Offset: m~ = m e^{-beta}, scale k = e^{-beta}.
    beta0 = sp.Symbol("beta0", real=True)
    Vt = Vk.subs(k, sp.exp(-beta0))

    ctx["L1"] = {
        "V_prod_as_exp": V_prod_as_exp,
        "V": V,
        "Vk": Vk,
        "V_inv_form": V_inv_form,
        "V_tilde": Vt,
        "beta0": beta0,
    }
    return ctx["L1"]


def verify(ctx):
    S = ctx["S"]
    r = ctx["L1"]
    V = r["V"]
    # [L1.4] V(m) = prod_j m_j^w_j equals exp(sum_j w_j log m_j)
    assert sp.simplify(r["V_prod_as_exp"] - V) == 0, "L1 FAIL: V is not exp(sum w log m)"
    # [L1.5] homogeneity of degree 1: V(k m) = k V(m), using sum_j w_j = 1
    assert sp.simplify(r["Vk"] - S.k_scale * V) == 0, "L1 FAIL: V(k m) != k V(m)"
    # [L1.6] invariant form: V(m / V(m)) = 1, the point lies on the frontier
    assert sp.simplify(r["V_inv_form"] - 1) == 0, "L1 FAIL: V(m / V(m)) != 1"
    # [L1.7] offset: V(m e^-beta) = e^-beta V(m), so log V = w.u - beta
    assert sp.simplify(r["V_tilde"] - sp.exp(-r["beta0"]) * V) == 0, (
        "L1 FAIL: V(m e^-beta) != e^-beta V(m)"
    )
    # Degree of homogeneity is the simplex total: without sum w = 1 it would not be 1.
    # [L1.8] the degree of homogeneity passes through sum_j w_j (without it, not degree 1)
    assert S.simplex.lhs in linear(
        product_to_exp_sum(sp.Product((S.k_scale * S.m[S.j]) ** S.w[S.j], (S.j, 1, S.d)), A1)
    ).atoms(sp.Sum), "L1 FAIL: homogeneity must pass through sum_j w_j"

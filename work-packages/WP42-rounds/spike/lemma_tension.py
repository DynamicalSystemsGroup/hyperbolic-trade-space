"""L21 (draft) - Tension: the derivative of one metric along the surface as another moves.

Draft for the build stage; plain SymPy, a pencil-and-paper substitute and not a formal proof.
It lives in the spike folder (``derivation/`` is not touched in this scope); the build moves it
to ``derivation/lemma_21_tension.py`` and registers its hypotheses in the ledger.

Setting (one term k, K >= 1).  In log-metrics u_j = log m_j (A1: m_j > 0) the term's surface is the
hyperplane G(m) = sum_j w_j log m_j - beta = 0 (L1, L7), and a design's level set is a parallel
hyperplane. Fix every metric but m_i and m_j; their other terms are one constant R.

Definition.  The tension between i and j on term k at a point is
    T_ij = d m_j / d m_i along the term's surface, other metrics held,
in the metrics themselves; the elasticity is its log-log form, (m_i/m_j) T_ij.

What this derives (symbolic w_i, w_j, m_i, m_j, R, beta; the other coordinates enter only as R):
  1. Chain rule from L7 in metrics: T_ij = -(w_i / w_j)(m_j / m_i), by the implicit-function
     derivative of G; its log-log form is L7's elasticity -w_i / w_j.
  2. The cases: w_i = 0 gives T_ij = 0 (zero); w_j = 0 makes dG/dm_j vanish, so m_j is not
     determined by m_i on the surface and T_ij is undefined (blank); where w_i and w_j are
     positive T_ij < 0 (negative); and T_ij T_ji = 1 where both are nonzero (reciprocal).
  3. Pull-back from L9 to attribute units: with m_k = e^{b_k} (a_k + s_k)^{alpha_k},
        d s_j / d s_i = T_ij (dm_i/ds_i) / (dm_j/ds_j)
                      = -(w_i alpha_i)/(w_j alpha_j) * (a_j + s_j)/(a_i + s_i),
     found two ways (the chain rule on T_ij and the implicit derivative of L9's surface
     sum_k w_k alpha_k log(a_k + s_k) = const), which agree. Its sign is minus the sign of
     alpha_i alpha_j: negative for two attributes of one orientation, positive for mixed.
  4. A design on the level set V = v has the same slope at its own metric ratios: the level set is
     the surface scaled by v (L1), which leaves the ratios m_j / m_i alone.

What this does NOT prove: that the fit is the right surface; that the derivative is the effect of
changing a design variable (it is a derivative along the fitted surface, not an intervention); the
seam of a K > 1 surface, where the two one-sided values differ (reported, not smoothed).

Hypotheses: A1 (m > 0), A2/L1 (the surface is the term's hyperplane), A4 (log-affine, alpha != 0).
"""

import sympy as sp

TITLE = "Tension: dm_j/dm_i = -(w_i/w_j)(m_j/m_i) along a term, and in attribute units"
STATEMENT = (
    "Along term k, d m_j / d m_i = -(w_ki / w_kj)(m_j / m_i) (zero if w_ki = 0, undefined if "
    "w_kj = 0, negative if both are positive, reciprocal across the diagonal); in attribute units "
    "d s_j / d s_i = -(w_ki alpha_i)/(w_kj alpha_j) (a_j + s_j)/(a_i + s_i)"
)
AXIOMS_USED = ["A1", "A2", "A4"]


def derive():
    mi, mj = sp.symbols("m_i m_j", positive=True)  # A1
    wi, wj = sp.symbols("w_i w_j", real=True)
    R, beta = sp.symbols("R beta", real=True)
    G = wi * sp.log(mi) + wj * sp.log(mj) + R - beta
    # [L21.1] implicit derivative of G(m_i, m_j) = 0: dm_j/dm_i = -G_i / G_j
    T_ij = sp.simplify(-sp.diff(G, mi) / sp.diff(G, mj))
    elasticity = sp.simplify(mi / mj * T_ij)
    # the reverse pair
    T_ji = sp.simplify(-sp.diff(G, mj) / sp.diff(G, mi))

    # pull-back (A4): m_k = exp(b_k) (a_k + s_k)^alpha_k, written with x_k = a_k + s_k > 0
    xi, xj = sp.symbols("x_i x_j", positive=True)
    ai, aj = sp.symbols("alpha_i alpha_j", real=True)
    bi, bj = sp.symbols("b_i b_j", real=True)
    m_of_x = {mi: sp.exp(bi) * xi**ai, mj: sp.exp(bj) * xj**aj}
    # route 1: chain rule on T_ij (ds = dx because s_k = x_k - a_k with a_k a constant)
    T_x = sp.simplify(T_ij.subs(m_of_x) * sp.diff(m_of_x[mi], xi) / sp.diff(m_of_x[mj], xj))
    # route 2: implicit derivative of L9's surface  w_i a_i log x_i + w_j a_j log x_j + R' = 0
    Gx = wi * ai * sp.log(xi) + wj * aj * sp.log(xj) + R - beta + wi * bi + wj * bj
    T_x2 = sp.simplify(-sp.diff(Gx, xi) / sp.diff(Gx, xj))
    return {
        "mi": mi, "mj": mj, "wi": wi, "wj": wj, "G": G, "T_ij": T_ij, "T_ji": T_ji,
        "elasticity": elasticity, "xi": xi, "xj": xj, "ai": ai, "aj": aj, "T_x": T_x,
        "T_x2": T_x2,
    }  # fmt: skip


def verify(r):
    mi, mj, wi, wj = r["mi"], r["mj"], r["wi"], r["wj"]
    ai, aj, xi, xj = r["ai"], r["aj"], r["xi"], r["xj"]
    # [L21.2] the metric-space tension is -(w_i/w_j)(m_j/m_i)
    assert sp.simplify(r["T_ij"] + (wi / wj) * (mj / mi)) == 0, "L21 FAIL: T_ij formula"
    # [L21.3] its log-log form is L7's elasticity -w_i/w_j
    assert sp.simplify(r["elasticity"] + wi / wj) == 0, "L21 FAIL: elasticity != -w_i/w_j"
    # [L21.4] zero case: w_i = 0 gives T_ij = 0 (j positive exponent)
    assert sp.simplify(r["T_ij"].subs(wi, 0)) == 0, "L21 FAIL: zero case"
    # [L21.5] blank case: w_j = 0 makes dG/dm_j vanish, T_ij has no finite value
    assert sp.diff(r["G"], mj).subs(wj, 0) == 0, "L21 FAIL: blank case"
    assert sp.denom(sp.together(r["T_ij"])).subs(wj, 0) == 0, "L21 FAIL: blank not undefined"
    # [L21.6] reciprocal across the diagonal: T_ij T_ji = 1 where both are nonzero
    assert sp.simplify(r["T_ij"] * r["T_ji"] - 1) == 0, "L21 FAIL: reciprocal"
    # [L21.7] negative where both exponents are positive (A2: exponents on the simplex)
    p, q = sp.symbols("p q", positive=True)
    sign = r["T_ij"].subs({wi: p, wj: q})
    assert sign.is_negative, "L21 FAIL: tension not negative for positive exponents"
    # [L21.8] attribute units: the chain rule on T_ij and the implicit derivative of L9's surface
    # agree, and equal -(w_i alpha_i)/(w_j alpha_j) (x_j / x_i)
    assert sp.simplify(r["T_x"] - r["T_x2"]) == 0, "L21 FAIL: two routes to the pull-back differ"
    assert sp.simplify(r["T_x2"] + (wi * ai) / (wj * aj) * (xj / xi)) == 0, (
        "L21 FAIL: attribute-unit formula"
    )
    # [L21.9] its sign is minus the sign of alpha_i alpha_j (positive exponents)
    s_same = r["T_x2"].subs({wi: p, wj: q, ai: -sp.Symbol("c1", positive=True),
                             aj: -sp.Symbol("c2", positive=True)})  # fmt: skip
    s_mixed = r["T_x2"].subs({wi: p, wj: q, ai: sp.Symbol("c1", positive=True),
                              aj: -sp.Symbol("c2", positive=True)})  # fmt: skip
    assert s_same.is_negative and s_mixed.is_positive, "L21 FAIL: orientation sign"
    # [L21.10] a design on the level set V = v: the level set is the surface scaled by v
    # (L1), which multiplies m_i and m_j alike and leaves T_ij unchanged
    v = sp.Symbol("v", positive=True)
    scaled = r["T_ij"].subs({mi: v * mi, mj: v * mj}, simultaneous=True)
    assert sp.simplify(scaled - r["T_ij"]) == 0, "L21 FAIL: level-set scaling"


if __name__ == "__main__":
    res = derive()
    verify(res)
    print(f"[L21] PASS  {TITLE}")
    print(f"       {STATEMENT}")
    print(f"       axioms: {', '.join(AXIOMS_USED)}; 10 tagged steps")

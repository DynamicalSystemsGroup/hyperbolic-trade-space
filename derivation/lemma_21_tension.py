"""L21 - Tension: the derivative of one metric along the surface as another moves.

Setting (one term k, K >= 1).  In log-metrics u_j = log m_j (A1: m_j > 0) the term's surface is the
hyperplane G(m) = sum_j w_j log m_j - beta = 0 (L1, L7), and a design's level set is a parallel
hyperplane. Fix every metric but m_i and m_j; their other terms are one constant R.

Definition.  The tension between i and j on term k at a point is T_ij = d m_j / d m_i along the
term's surface, other metrics held, in the metrics themselves; the elasticity is its log-log form,
(m_i / m_j) T_ij.

What this proves (symbolic w_i, w_j, m_i, m_j, R, beta; the other coordinates enter only as R):
  * Chain rule from L7 in metrics: T_ij = -(w_i / w_j)(m_j / m_i), the implicit-function
    derivative of G; its log-log form is L7's elasticity -w_i / w_j.
  * The cases: w_i = 0 gives T_ij = 0 (zero); w_j = 0 makes dG/dm_j vanish, so m_j is not
    determined by m_i on the surface and T_ij is undefined (blank); where w_i and w_j are positive
    T_ij < 0 (negative); and T_ij T_ji = 1 where both are nonzero (reciprocal).
  * Pull-back from L9 to attribute units: with m_k = e^{b_k} (a_k + s_k)^{alpha_k},
    d s_j / d s_i = T_ij (dm_i/ds_i) / (dm_j/ds_j)
    = -(w_i alpha_i)/(w_j alpha_j) (a_j + s_j)/(a_i + s_i),
    found two ways (the chain rule on T_ij and the implicit derivative of L9's surface
    sum_k w_k alpha_k log(a_k + s_k) = const), which agree. Its sign is minus the sign of
    alpha_i alpha_j: negative for two attributes of one orientation, positive for mixed.
  * A design on the level set V = v has the same slope at its own metric ratios: the level set is
    the surface scaled by v (L1), which leaves the ratios m_j / m_i alone.

Hypotheses of the statement (declared, not derived): w_i > 0 and w_j > 0 (both metrics carry an
exponent on the term) for the sign; c_i > 0 and c_j > 0 (the sizes of alpha_i and alpha_j, whose
signs are the orientations) for the sign in attribute units.

What this does NOT prove: that the fit is the right surface; that the derivative is the effect of
changing a design variable (it is a derivative along the fitted surface, not an intervention); the
seam of a K > 1 surface, where the two one-sided values differ (reported, not smoothed).

It is a pencil-and-paper substitute for the derivation, not a formal verification.
"""

import sympy as sp

from derivation.axioms import A1, A4
from derivation.licence import hypothesis_symbol

TITLE = "Tension: dm_j/dm_i = -(w_i/w_j)(m_j/m_i) along a term, and in attribute units"
STATEMENT = (
    "Along term k, d m_j / d m_i = -(w_ki / w_kj)(m_j / m_i) (zero if w_ki = 0, undefined if "
    "w_kj = 0, negative if both are positive, reciprocal across the diagonal); in attribute units "
    "d s_j / d s_i = -(w_ki alpha_i)/(w_kj alpha_j) (a_j + s_j)/(a_i + s_i)"
)
AXIOMS_USED = ["A1", "A4"]

W_I = hypothesis_symbol(
    "p", "positive", "w_i > 0 and w_j > 0 (both metrics carry an exponent on the term)"
)
W_J = hypothesis_symbol(
    "q", "positive", "w_i > 0 and w_j > 0 (both metrics carry an exponent on the term)"
)
C_I = hypothesis_symbol(
    "c1",
    "positive",
    "c_i > 0 and c_j > 0 (the sizes of alpha_i and alpha_j, whose signs are the orientations)",
)
C_J = hypothesis_symbol(
    "c2",
    "positive",
    "c_i > 0 and c_j > 0 (the sizes of alpha_i and alpha_j, whose signs are the orientations)",
)


def derive(ctx):
    S = ctx["S"]
    i0, j0 = sp.symbols("i0 j0", integer=True)
    # [L21.1] A1: the metric m_i is strictly positive
    mi = A1.positive_symbol("m_i")
    # [L21.2] A1: the metric m_j is strictly positive
    mj = A1.positive_symbol("m_j")
    # [L21.3] A4: x_i = a_i + s_i is strictly positive, the domain of the conditioning
    xi = A4.positive_symbol("x_i")
    # [L21.4] A4: x_j = a_j + s_j is strictly positive, the domain of the conditioning
    xj = A4.positive_symbol("x_j")
    wi, wj, R, beta = sp.symbols("w_i w_j R beta", real=True)
    G = wi * sp.log(mi) + wj * sp.log(mj) + R - beta
    # implicit derivative of G(m_i, m_j) = 0: dm_j/dm_i = -G_i / G_j
    T_ij = sp.simplify(-sp.diff(G, mi) / sp.diff(G, mj))
    T_ji = sp.simplify(-sp.diff(G, mj) / sp.diff(G, mi))
    elasticity = sp.simplify(mi / mj * T_ij)

    # the conditioning of the two metrics, written in x = a + s (the log's argument stands as x)
    # [L21.5] A4: u_i = alpha_i log(a_i + s_i) + b_i, so m_i = exp(u_i)
    u_i = A4.rewrite(S.u[i0]).replace(sp.log, lambda arg: sp.log(xi))
    # [L21.6] A4: u_j = alpha_j log(a_j + s_j) + b_j, so m_j = exp(u_j)
    u_j = A4.rewrite(S.u[j0]).replace(sp.log, lambda arg: sp.log(xj))
    m_of_x = {mi: sp.exp(u_i), mj: sp.exp(u_j)}
    # route 1: chain rule on T_ij (ds = dx because s_k = x_k - a_k with a_k a constant)
    T_x = sp.simplify(
        sp.powsimp(
            T_ij.subs(m_of_x) * sp.diff(m_of_x[mi], xi) / sp.diff(m_of_x[mj], xj), force=True
        )
    )
    # route 2: implicit derivative of L9's surface  w_i u_i + w_j u_j + R - beta = 0
    Gx = wi * u_i + wj * u_j + R - beta
    T_x2 = sp.simplify(-sp.diff(Gx, xi) / sp.diff(Gx, xj))
    ctx["L21"] = {
        "mi": mi, "mj": mj, "xi": xi, "xj": xj, "wi": wi, "wj": wj, "G": G,
        "T_ij": T_ij, "T_ji": T_ji, "elasticity": elasticity, "T_x": T_x, "T_x2": T_x2,
        "ai": S.alpha[i0], "aj": S.alpha[j0],
    }  # fmt: skip
    return ctx["L21"]


def verify(ctx):
    r = ctx["L21"]
    mi, mj, wi, wj, xi, xj = r["mi"], r["mj"], r["wi"], r["wj"], r["xi"], r["xj"]
    ai, aj = r["ai"], r["aj"]
    # [L21.7] the metric-space tension is -(w_i/w_j)(m_j/m_i)
    assert sp.simplify(r["T_ij"] + (wi / wj) * (mj / mi)) == 0, "L21 FAIL: T_ij formula"
    # [L21.8] its log-log form is L7's elasticity -w_i/w_j
    assert sp.simplify(r["elasticity"] + wi / wj) == 0, "L21 FAIL: elasticity != -w_i/w_j"
    # [L21.9] zero case: w_i = 0 gives T_ij = 0 (w_j nonzero)
    assert sp.simplify(r["T_ij"].subs(wi, 0)) == 0, "L21 FAIL: zero case"
    # [L21.10] blank case: w_j = 0 makes dG/dm_j vanish, so m_j is not determined by m_i
    assert sp.diff(r["G"], mj).subs(wj, 0) == 0, "L21 FAIL: blank case"
    # [L21.11] blank case: the tension has w_j in its denominator, so it has no finite value
    assert sp.denom(sp.together(r["T_ij"])).subs(wj, 0) == 0, "L21 FAIL: blank not undefined"
    # [L21.12] reciprocal across the diagonal: T_ij T_ji = 1 where both are nonzero
    assert sp.simplify(r["T_ij"] * r["T_ji"] - 1) == 0, "L21 FAIL: reciprocal"
    # [L21.13] negative where both exponents are positive (hypothesis of the statement)
    assert r["T_ij"].subs({wi: W_I, wj: W_J, mi: mi, mj: mj}).is_negative, (
        "L21 FAIL: tension not negative for positive exponents"
    )
    # [L21.14] attribute units: the chain rule on T_ij and the implicit derivative of L9's V agree
    assert sp.simplify(r["T_x"] - r["T_x2"]) == 0, "L21 FAIL: two routes to the pull-back differ"
    # [L21.15] attribute units: d s_j / d s_i = -(w_i alpha_i)/(w_j alpha_j) (x_j / x_i)
    assert sp.simplify(r["T_x2"] + (wi * ai) / (wj * aj) * (xj / xi)) == 0, (
        "L21 FAIL: attribute-unit formula"
    )
    # [L21.16] its sign is minus the sign of alpha_i alpha_j: negative for one orientation
    assert r["T_x2"].subs({wi: W_I, wj: W_J, ai: -C_I, aj: -C_J}).is_negative, (
        "L21 FAIL: orientation sign (same orientation)"
    )
    # [L21.17] its sign is minus the sign of alpha_i alpha_j: positive for mixed orientation
    assert r["T_x2"].subs({wi: W_I, wj: W_J, ai: C_I, aj: -C_J}).is_positive, (
        "L21 FAIL: orientation sign (mixed orientation)"
    )
    v = sp.Dummy("v")
    # [L21.18] a design on the level set V = v: the level set is the surface scaled by v (L1),
    # which multiplies m_i and m_j alike and leaves T_ij unchanged
    assert (
        sp.simplify(r["T_ij"].subs({mi: v * mi, mj: v * mj}, simultaneous=True) - r["T_ij"]) == 0
    ), "L21 FAIL: level-set scaling"


if __name__ == "__main__":
    from derivation.symbols import make_symbols

    context = {"S": make_symbols()}
    derive(context)
    verify(context)
    print(f"[L21] PASS  {TITLE}")

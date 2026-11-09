"""L7 - Elasticities on the frontier and the single-metric improvement factor.

Frontier in log space: F = { u : G(u) = sum_j w_j u_j - beta = 0 }, u_j = log m_j (A1).

What this proves (symbolic d, coordinates j0 != k0 in 1..d):
  * Elasticity: d log m_{j0} / d log m_{k0} = -w_{k0} / w_{j0} along F. Tangent directions v of
    F satisfy dG(v) = sum_j w_j v_j = 0; take v = e_{k0} + x e_{j0} (KroneckerDelta
    directions) and solve for x.
  * Improvement factor: scaling m_{j0} by f gives V -> f^{w_{j0}} V; the factor that reaches
    the frontier (V = 1) is f = V^{-1/w_{j0}} (valid for w_{j0} != 0; R1 supplies w_{j0} > 0
    at the balanced point).
  * Uniform improvement: scaling every metric by V^{-1} reaches V = 1 (via L1, simplex A2).

Differentiation route: DIRECTIONAL derivative with a KroneckerDelta coordinate direction
(scope default for L7), d/dt G(u + t v) at t = 0 computed by sympy for symbolic d. The
index-range conditions 1 <= j0, k0 <= d (the indices name coordinates; A0 structural) select
the first branch of the Piecewise that sympy returns for the KroneckerDelta sums.

What this does NOT prove: that the elasticities are the ones at the balanced point (needs
the fit, L3 + R1), or anything off F; they are shape quantities, not preferences.
"""

import sympy as sp

from derivation.axioms import A1, A2
from derivation.licence import licensed_power
from derivation.sumtools import linear

TITLE = "Elasticities -w_k/w_j on the frontier; improvement factor V^(-1/w_j)"
STATEMENT = (
    "d log m_j / d log m_k = -w_k / w_j on F; improving metric j alone by f = V^(-1/w_j) "
    "reaches V = 1"
)
AXIOMS_USED = ["A1", "A2"]


def _impose_index_bounds(expr):
    """Impose 1 <= index <= d on the Piecewise from KroneckerDelta sums (A0 index meaning)."""
    return expr.replace(
        lambda e: isinstance(e, sp.Piecewise),
        lambda e: e.subs({r: True for r in e.atoms(sp.Rel)}),
    )


def derive(ctx):
    S = ctx["S"]
    d, j, w, t = S.d, S.j, S.w, S.t
    j0, k0 = sp.symbols("j0 k0", integer=True)
    x = sp.Symbol("x", real=True)  # change of u_{j0} per unit change of u_{k0}
    lim = (j, 1, d)

    # [L7.1] A1: a point of F is a point of log-metrics u = log m, a real family
    uu = A1.real_base("u_pt")
    delta = sp.KroneckerDelta
    v = lambda jj: delta(jj, k0) + x * delta(jj, j0)  # noqa: E731  direction e_k0 + x e_j0
    G_t = sp.Sum(w[j] * (uu[j] + t * v(j)), lim)
    dG = _impose_index_bounds(sp.diff(G_t, t).doit().subs(t, 0))
    dG = sp.simplify(dG)  # w_k0 + x w_j0
    x_sol = sp.solve(sp.Eq(dG, 0), x)[0]

    # Improvement factor: u_{j0} -> u_{j0} + log f.
    logf = sp.Symbol("logf", real=True)
    logV = sp.Sum(w[j] * uu[j], lim)
    logV_new = linear(sp.Sum(w[j] * (uu[j] + logf * delta(j, j0)), lim))
    logV_new = _impose_index_bounds(logV_new.doit())
    w_j0 = w[j0]
    logf_star = -logV / w_j0
    # V = exp(logV) > 0 (A1: u real, A2: w real), so V**(-1/w) = exp(-logV/w)
    # [L7.2] A1, A2: V = exp(log V) > 0, so the power V^(-1/w_j) is exp(-log V / w_j)
    f_star = licensed_power(sp.exp(logV) ** (-1 / w_j0), A1, A2)

    # Uniform improvement: f = 1/V in L1's V(k m) = k V(m) gives V = 1.
    L1 = ctx["L1"]
    # L1's V(k m) already carries sum_j w_j = 1; at k = 1/V it gives V(m / V)
    uniform = sp.simplify(L1["Vk"].subs(S.k_scale, 1 / L1["V"]))

    ctx["L7"] = {
        "dG": dG,
        "x_sol": x_sol,
        "j0": j0,
        "k0": k0,
        "logV_new": logV_new,
        "logV": logV,
        "logf_star": logf_star,
        "logf": logf,
        "w_j0": w_j0,
        "f_star": f_star,
        "uniform": uniform,
    }
    return ctx["L7"]


def verify(ctx):
    S = ctx["S"]
    r = ctx["L7"]
    w, j0, k0 = S.w, r["j0"], r["k0"]
    x = sp.Symbol("x", real=True)
    # [L7.3] the tangent direction e_k0 + x e_j0 has dG(v) = w_k0 + x w_j0
    assert sp.simplify(r["dG"] - (w[k0] + x * w[j0])) == 0, "L7 FAIL: dG(v) != w_k + x w_j"
    # [L7.4] dG(v) = 0 gives the elasticity x = d log m_j0 / d log m_k0 = -w_k0 / w_j0
    assert sp.simplify(r["x_sol"] + w[k0] / w[j0]) == 0, "L7 FAIL: elasticity != -w_k/w_j"
    # scaling m_j0 by f adds w_j0 log f to log V
    # [L7.5] scaling m_j0 by f adds w_j0 log f to log V, so V -> f^w_j0 V
    assert sp.simplify(r["logV_new"] - (r["logV"] + w[j0] * r["logf"])) == 0, (
        "L7 FAIL: V(f m_j) != f^{w_j} V"
    )
    # at f = V^(-1/w_j0) the new log V vanishes: V = 1 (frontier)
    new_logV = r["logV_new"].subs(r["logf"], r["logf_star"])
    # [L7.6] at f = V^(-1/w_j0) the new log V is 0: the point reaches the frontier V = 1
    assert sp.simplify(new_logV) == 0, "L7 FAIL: improvement factor does not reach V = 1"
    # [L7.7] the improvement factor V^(-1/w_j0) equals exp(-log V / w_j0)
    assert sp.simplify(r["f_star"] - sp.exp(r["logf_star"])) == 0, (
        "L7 FAIL: V^(-1/w_j) != exp(-log V / w_j)"
    )
    # [L7.8] uniform improvement: scaling every metric by 1/V gives V = 1
    assert sp.simplify(r["uniform"] - 1) == 0, "L7 FAIL: uniform improvement 1/V does not give V=1"

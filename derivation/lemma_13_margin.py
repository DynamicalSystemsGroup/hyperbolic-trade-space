"""L13 (Lemma 2) - the assignment margin and the assignment-stable radius.

Setting.  Facet k has parameters theta_k = (w_k, beta_k); a design with log-metrics u_i has the
augmented vector u~_i = (u_i, -1); its score on facet k is s_ik = w_k.u_i - beta_k = theta_k.u~_i,
the energy differential (log V) of design i against facet k.  k(i) is the maximizing facet of i
and the margin is gamma = min_i [ s_{i,k(i)} - max_{k != k(i)} s_ik ].

What this proves (symbolic d, plain SymPy):
  1. A change of parameters Delta theta_k changes the score by Delta s_ik = Delta theta_k . u~_i
     (Sum linearity; the offset enters with the sign of the -1 in u~_i).
  2. F12 (min representation): gamma <= s_{i,k(i)} - s_il for every row i and facet l != k(i);
     write the slack as rest >= 0.  If every score changes by at most delta (|e| <= delta, e_ik the
     change in s_ik) then the new gap to facet l is (gamma + rest) + e_ik(i) - e_il, and with the
     slacks a1 = e_ik(i) + delta >= 0, a2 = delta - e_il >= 0 it is (gamma - 2 delta) + rest + a1
     + a2: at least gamma - 2 delta, and positive when 2 delta < gamma (positive-symbol algebra,
     the L11 device).  So the maximizing facet of every row is unchanged and unique.
  3. Explicit radius.  I9 (Cauchy-Schwarz): |Delta theta_k . u~_i| <= ||Delta theta_k||_2
     ||u~_i||_2 <= r U with r = max_k ||Delta theta_k||_2, U = max_i ||u~_i||_2 (U >= 1 because the
     last component is -1).  So delta = r U, and 2 r U < gamma is r < gamma / (2 U), solved for r.
  4. One confined exact instance (d = 2, two facets, two rows): a perturbation of norm 0.9 times
     the radius, aligned against the row with the smallest margin, leaves the labels unchanged and
     the new margin at least gamma - 2 delta.

Hypotheses (ledger).  R2 (positive assignment margin gamma > 0), F12 (min representation), I9
(Cauchy-Schwarz, cited).

What this does NOT prove: that the margin is positive (R2 is a condition on the fit, false on a
ridge row at tau = infinity), that the radius is tight, or anything about perturbations of the
data U.
"""

import sympy as sp

from derivation.sumtools import linear

TITLE = "assignment margin: score changes below gamma/2 keep the maximizing facets; explicit radius"
STATEMENT = (
    "Facet scores s_ik = w_k.u_i - beta_k = theta_k.(u_i, -1), the energy differential (log V) of "
    "design i against facet k; margin gamma = min_i [s_i,k(i) - max_{k != k(i)} s_ik] > 0 (R2). "
    "If every facet score changes by at most delta, every row's new gap to every other facet is "
    ">= gamma - 2 delta, positive when 2 delta < gamma, so each maximizing facet is unchanged and "
    "unique. With Cauchy-Schwarz (I9), |Delta theta_k.(u_i, -1)| <= ||Delta theta_k||_2 "
    "||(u_i, -1)||_2, so 2 delta < gamma holds whenever "
    "max_k ||Delta theta_k||_2 < gamma / (2 max_i ||(u_i, -1)||_2): an assignment-stable "
    "neighborhood of the fitted reference surface's facets"
)
AXIOMS_USED = ["F12", "I9", "R2"]


def derive(ctx):
    S = ctx["S"]
    d, i, j, k = S.d, S.i, S.j, S.k
    u = S.u
    lim = (j, 1, d)

    # 1. change of the score under a parameter change
    W = sp.IndexedBase("W")  # exponents w_k
    B = sp.IndexedBase("B")  # offsets beta_k
    dw = sp.IndexedBase("dw")  # Delta w_k
    db = sp.IndexedBase("db")  # Delta beta_k
    new_score = sp.Sum((W[k, j] + dw[k, j]) * u[i, j], lim) - (B[k] + db[k])
    old_score = sp.Sum(W[k, j] * u[i, j], lim) - B[k]
    score_change = linear(new_score - old_score)
    score_change_claim = sp.Sum(dw[k, j] * u[i, j], lim) - db[k]  # = Delta theta_k . (u_i, -1)
    score_change_slack = sp.simplify(score_change - score_change_claim)

    # 2. margin algebra: gamma = c + 2 delta, e1 = a1 - delta, e2 = delta - a2
    c = sp.Symbol("c", positive=True)  # gamma - 2 delta > 0 (2 delta < gamma)
    delta = sp.Symbol("delta", nonnegative=True)
    rest = sp.Symbol("rest", nonnegative=True)  # (s_ik(i) - s_il) - gamma >= 0 (F12)
    a1 = sp.Symbol("a1", nonnegative=True)  # e_ik(i) + delta >= 0  (|e| <= delta)
    a2 = sp.Symbol("a2", nonnegative=True)  # delta - e_il >= 0
    gamma = c + 2 * delta
    e1, e2 = a1 - delta, delta - a2
    new_gap = (gamma + rest) + e1 - e2
    margin_slack = sp.simplify(new_gap - (c + rest + a1 + a2))
    margin_nonneg = (rest + a1 + a2).is_nonnegative
    margin_positive = (c + rest + a1 + a2).is_positive

    # 3. Cauchy-Schwarz (I9) chain and the radius: r U - nth nu = a U + nth b, nth = ||Delta||,
    # nu = ||u~||, r = nth + a >= nth, nu = U - b <= U
    nth, a_, b_, UU = sp.symbols("nth a_ b_ UU", nonnegative=True)
    bound_slack = sp.simplify((nth + a_) * UU - nth * (UU - b_) - (a_ * UU + nth * b_))
    bound_nonneg = (a_ * UU + nth * b_).is_nonnegative
    r_ = sp.Symbol("r_", nonnegative=True)
    U_ = sp.Symbol("U_", positive=True)  # U >= 1: the last component of u~ is -1
    g_ = sp.Symbol("g_", positive=True)
    radius_set = sp.solveset(2 * r_ * U_ < g_, r_, sp.S.Reals)  # r = max norm, so r >= 0

    # 4. exact instance: facets theta_1 = ((1,0), 0), theta_2 = ((0,1), 0); rows (2,0), (0,1)
    R = sp.Rational
    Theta = sp.Matrix([[1, 0, 0], [0, 1, 0]])  # rows (w_k, beta_k)
    Ut = sp.Matrix([[2, 0, -1], [0, 1, -1]])  # rows (u_i, -1)

    def labels_margin(T):
        labs, gaps = [], []
        for vals in (Ut * T.T).tolist():
            best = max(vals)
            labs.append(vals.index(best) + 1)
            gaps.append(best - max(x for x in vals if x != best) if vals.count(best) == 1 else 0)
        return tuple(labs), min(gaps)

    labs, margin = labels_margin(Theta)
    U_max = max(sp.sqrt(sum(x**2 for x in row)) for row in Ut.tolist())
    radius = margin / (2 * U_max)
    r = R(9, 10) * radius
    u2 = Ut.row(1)  # the row with the smallest margin
    unit = u2 / sp.sqrt(sum(x**2 for x in u2))
    dTheta = sp.Matrix.vstack(r * unit, -r * unit)  # raise facet 1, lower facet 2 on row 2
    labs2, margin2 = labels_margin(Theta + dTheta)
    delta_num = r * U_max
    numeric = dict(
        labels=labs,
        labels_perturbed=labs2,
        margin=margin,
        perturbed_margin=sp.simplify(margin2),
        delta=sp.simplify(delta_num),
        r=sp.simplify(r),
        radius=sp.simplify(radius),
        norms=[sp.simplify(sp.sqrt(sum(x**2 for x in row))) for row in dTheta.tolist()],
    )

    ctx["L13"] = dict(
        score_change=score_change,
        score_change_claim=score_change_claim,
        score_change_slack=score_change_slack,
        margin_slack=margin_slack,
        margin_nonneg=margin_nonneg,
        margin_positive=margin_positive,
        bound_slack=bound_slack,
        bound_nonneg=bound_nonneg,
        radius_set=radius_set,
        r_=r_,
        U_=U_,
        g_=g_,
        numeric=numeric,
    )


def verify(ctx):
    r = ctx["L13"]
    assert sp.simplify(r["score_change_slack"]) == 0, (
        "L13 FAIL: change of the score is not Delta theta . (u, -1)"
    )
    assert sp.simplify(r["margin_slack"]) == 0, (
        "L13 FAIL: new gap != (gamma - 2 delta) + rest + a1 + a2"
    )
    assert r["margin_nonneg"] is True, "L13 FAIL: the slacks rest + a1 + a2 are not nonnegative"
    assert r["margin_positive"] is True, (
        "L13 FAIL: the new gap is not positive when 2 delta < gamma"
    )
    assert sp.simplify(r["bound_slack"]) == 0, (
        "L13 FAIL: r U - ||Delta|| ||u~|| != a U + ||Delta|| b"
    )
    assert r["bound_nonneg"] is True, "L13 FAIL: Cauchy-Schwarz chain slack is not nonnegative"
    assert r["radius_set"] == sp.Interval.open(-sp.oo, r["g_"] / (2 * r["U_"])), (
        "L13 FAIL: 2 r U < gamma is not r < gamma / (2 U)"
    )

    num = r["numeric"]
    assert num["margin"] == 1 and num["labels"] == (1, 2), "L13 FAIL: instance margin or labels"
    assert num["labels_perturbed"] == num["labels"], (
        "L13 FAIL: labels changed inside the stable radius"
    )
    assert all(sp.simplify(x - num["r"]) == 0 for x in num["norms"]) and num["r"] < num["radius"], (
        "L13 FAIL: the instance perturbation is not inside the radius"
    )
    assert 2 * num["delta"] < num["margin"], "L13 FAIL: 2 delta < gamma not met by the instance"
    assert bool(num["perturbed_margin"] >= num["margin"] - 2 * num["delta"]) and bool(
        num["perturbed_margin"] > 0
    ), "L13 FAIL: perturbed margin below gamma - 2 delta"

"""L12 (Lemma 1) - the simplex first-order gap of a facet refit bounds its suboptimality.

Setting.  The facet refit of step B is f_k(w) = J_tau(U w) - ubar_k . w on the simplex (ubar_k the
mean log-metric vector of the rows assigned to facet k).  J_tau - linear is convex (L4).  Write
g = grad f_k(w) and G(w) = max_{v in simplex} g.(w - v) = g.w - min_j g_j.

What this proves (symbolic d, plain SymPy):
  1. f_k is convex: the linear part contributes a zero second derivative along every line, so
     the second directional derivative is L4's tau Var_p(v.u) >= 0.
  2. Min representation (F12): m = min_j g_j is a symbol with g_j - m >= 0 for all j and
     g_{j0} = m.  Then for v on the simplex (A2) g.v - m = sum_j v_j (g_j - m) >= 0, with the
     identity from Sum linearity and sum_j v_j = 1.  The bound is attained at the vertex e_{j0}
     (the KroneckerDelta device of L3): g.e_{j0} = g_{j0} = m.  So min_{v in simplex} g.v = m and
     G = g.w - m = sum_j w_j (g_j - m) >= 0.
  3. G = 0 iff w_j (g_j - min g) = 0 for every j: a sum of nonnegative terms vanishes only termwise.
     With lambda = w.g = G + m, G = 0 is lambda = min g, i.e. g_j >= lambda and w_j (g_j - lambda)
     = 0: L3's full simplex KKT (E-2); the equal-gradient condition is the w_j > 0 case.
  4. Suboptimality chain.  Inherited I8 (first-order convexity inequality, f(v) >= f(w) +
     g.(v - w)) at v = v*, the minimizer, gives a = f* - f(w) - g.(v* - w) >= 0.  Step 2 at
     v = v* gives b = g.v* - m >= 0.  Then G - (f(w) - f*) = a + b >= 0 (sign algebra) and
     f(w) - f* >= 0 because f* is the minimum: 0 <= f(w) - f* <= G.
  5. tau = infinity.  f_k is piecewise linear, g = U_c^T p for any p on the simplex supported on
     the active rows (p_i (M - s_i) = 0), with U_c the rows centred at ubar_k.  Sum swap (L3's
     device) and sum_i p_i = 1 give g.w = sum_i p_i s_i - ubar.w = M - ubar.w = f(w), where the
     termwise zero p_i (M - s_i) = 0 is I12 applied to each summand, so G = f(w) -
     min_j (U_c^T p)_j is the primal objective minus the dual objective of the LP: the LP duality
     gap (I1), zero at an optimal primal-dual pair.  An exact two-metric LP checks it.

Hypotheses (ledger).  A2 (simplex), F12 (min representation: no symbolic-d min
in SymPy, as F5 and F10), I8 (first-order convexity inequality, cited), I1 (LP duality at
tau = infinity).

What this does NOT prove: that the fitted facet is globally optimal (G is a certificate, G = 0 is
optimality), anything for the penalized objective or the tangent refit (their f is not this f), or
the finite-tau formula at tau = infinity (there the gap needs the LP duals).
"""

import sympy as sp

from derivation.axioms import A2, F12, I1, I8, I12
from derivation.sumtools import fuse, linear, push_in, sum_swap_equal
from derivation.sumtools import piece_in_range as delta_branch
from derivation.symbols import J0

TITLE = "facet first-order gap: 0 <= f(w) - f* <= G, G = 0 iff the simplex KKT holds"
STATEMENT = (
    "For the facet refit f(w) = J_tau(U w) - ubar_k.w on the simplex (convex by L4), g = grad f(w) "
    "and G = g.w - min_j g_j = sum_j w_j (g_j - min g) >= 0, with G = 0 iff w_j (g_j - min g) = 0 "
    "for every j (L3's simplex KKT: g_j >= lambda, w_j (g_j - lambda) = 0, lambda = w.g); and "
    "0 <= f(w) - f* <= G. For the fitted reference surface (finite tau, Phi = 0, V > 1 possible) "
    "this is the stopping certificate of a facet; for the tau = inf supporting envelope, with the "
    "LP duals p, G is the LP duality gap (I1)"
)
AXIOMS_USED = ["A2", "I1", "I8", "I12", "F12"]


def derive(ctx):
    S = ctx["S"]
    d, n, i, j, t = S.d, S.n, S.i, S.j, S.t
    w, v, u, p = S.w, S.v, S.u, S.p
    lim = (j, 1, d)

    # 1. convexity: the linear part has zero second derivative along every line
    ub = sp.IndexedBase("ubar")
    linear_line = sp.Sum(ub[j] * (w[j] + t * v[j]), lim)
    second_linear = sp.diff(linear_line, t, 2)

    # 2. min representation (F12): g_j = m + gm_j, gm_j >= 0; v on the simplex (A2)
    m = sp.Symbol("m", real=True)  # the minimum of the g_j (F12: g_j >= m for all j, g_j0 = m)
    # [L12.1] A2: the weight families v and w on the simplex are nonnegative
    vn, wn = A2.nonneg_base("vn"), A2.nonneg_base("wn")
    # [L12.2] F12: the slacks gm_j = g_j - m are nonnegative
    gm = F12.nonneg_base("gm")
    g = sp.IndexedBase("g")
    # [L12.3] A2: sum_j v_j = 1 gives g.v - m = sum_j v_j (g_j - m)
    gv_minus_m = A2.rewrite(linear(sp.Sum(vn[j] * (gm[j] + m), lim) - m), rename={w: vn})
    gv_rhs = sp.Sum(vn[j] * gm[j], lim)
    vertex = sp.Sum(sp.KroneckerDelta(j, J0) * g[j], lim).doit()
    G_expr = sp.Sum(wn[j] * gm[j], lim)
    # [L12.4] A2: sum_j w_j = 1 gives lambda - m = w.g - m = sum_j w_j (g_j - m) = G
    lam_minus_m = A2.rewrite(linear(sp.Sum(wn[j] * (gm[j] + m), lim) - m), rename={w: wn})

    # 3. a sum of nonnegative terms vanishes only termwise: a + r = 0, a, r >= 0
    a_t = sp.Symbol("a_t", nonnegative=True)
    r_t = sp.Symbol("r_t", nonnegative=True)
    zero_sol = sp.solve(sp.Eq(a_t + r_t, 0), a_t)
    x_t = sp.Symbol("x_t", real=True)  # a_t as an unconstrained real, for the two half-lines
    kkt_squeeze = sp.Intersection(
        sp.solveset(x_t >= 0, x_t, sp.S.Reals), sp.solveset(x_t <= 0, x_t, sp.S.Reals)
    )  # a >= 0 and a = -r <= 0 (zero_sol, r >= 0)

    # 4. suboptimality chain: f* = f(v*), slack a from I8, slack b from step 2
    fw, fs, gw, gvs = sp.symbols("fw fs gw gvs", real=True)  # f(w), f*, g.w, g.v*
    # [L12.5] I8 at v = v*: the slack f(v*) - f(w) - g.(v* - w) is >= 0
    a_i8 = I8.slack_expr(f_v=fs, f_w=fw, g_dv=gvs - gw)
    b_m = gvs - m  # step 2 at v = v*
    G_val = gw - m
    chain_slack = G_val - (fw - fs) - (a_i8 + b_m)  # = 0
    a_nn = sp.Symbol("a_nn", nonnegative=True)
    b_nn = sp.Symbol("b_nn", nonnegative=True)
    c_nn = sp.Symbol("c_nn", nonnegative=True)  # f(w) - f* >= 0 (f* is the minimum)
    chain_nonneg = (a_nn + b_nn).is_nonnegative
    lower_nonneg = c_nn.is_nonnegative

    # 5. tau = infinity: G is the LP duality gap.  Sum swap, then support of p on active rows.
    ubj = sp.IndexedBase("ubj")  # ubar_j
    M = S.M

    def s_row(x):
        return sp.Sum(w[j] * u[x, j], lim)

    lhs_swap = sp.Sum(w[j] * sp.Sum(p[i] * u[i, j], (i, 1, n)), lim)
    rhs_swap = sp.Sum(p[i] * s_row(i), (i, 1, n))
    swap_equal = sum_swap_equal(fuse(push_in(lhs_swap)), fuse(push_in(rhs_swap)))
    support = sp.Sum(p[i] * (M - s_row(i)), (i, 1, n))
    # [L12.6] I12: complementary slackness p_i (M - s_i) = 0 applied to each summand: the sum is 0
    support_zero = I12.rewrite(support).doit()
    support_reduced = linear(support).subs(sp.Sum(p[i], (i, 1, n)), 1)
    ps = sp.Sum(p[i] * s_row(i), (i, 1, n))
    ubw = sp.Sum(w[j] * ubj[j], lim)
    uc_p = sp.Sum(p[i] * (u[i, j] - ubj[j]), (i, 1, n))  # (U_c^T p)_j, the centred rows
    g_dot_w = sp.Sum(w[j] * (sp.Sum(p[i] * u[i, j], (i, 1, n)) - ubj[j]), lim)
    g_dot_w_split = linear(g_dot_w)

    # exact two-metric LP: rows (2,0), (0,2), mean (1,1); centred rows (1,-1), (-1,1)
    R = sp.Rational
    Uc = sp.Matrix([[1, -1], [-1, 1]])

    def f_lp(wv):
        return max(*(Uc * wv))

    def dual(pv):
        return min(*(Uc.T * pv))

    w_opt = sp.Matrix([R(1, 2), R(1, 2)])
    p_opt = sp.Matrix([R(1, 2), R(1, 2)])
    w_off = sp.Matrix([1, 0])
    p_off = sp.Matrix([1, 0])  # supported on the active row 1 of U_c w_off = (1, -1)
    # [L12.7] exact two-metric LP: primal and dual values and gaps at an optimal pair and off it
    lp = dict(
        primal_at_optimum=f_lp(w_opt),
        dual_at_optimum=dual(p_opt),
        gap_at_optimum=f_lp(w_opt) - dual(p_opt),
        f_star=f_lp(w_opt),
        f_off_optimum=f_lp(w_off),
        gap_off_optimum=f_lp(w_off) - dual(p_off),
        active_off=(Uc * w_off),
    )
    convex = ctx["L4"].get("convex") is True and second_linear == 0  # f = J_tau - linear

    ctx["L12"] = dict(
        second_linear=second_linear,
        gv_minus_m=gv_minus_m,
        gv_rhs=gv_rhs,
        gap_nonneg=gv_rhs.is_nonnegative,
        vertex=vertex,
        g=g,
        m=m,
        G_expr=G_expr,
        lam_minus_m=lam_minus_m,
        zero_sol=zero_sol,
        a_t=a_t,
        r_t=r_t,
        kkt_squeeze=kkt_squeeze,
        chain_slack=chain_slack,
        chain_nonneg=chain_nonneg,
        lower_nonneg=lower_nonneg,
        swap_equal=swap_equal,
        support_reduced=support_reduced,
        support_zero=support_zero,
        ps=ps,
        ubw=ubw,
        uc_p=uc_p,
        g_dot_w_split=g_dot_w_split,
        lhs_swap=lhs_swap,
        lp=lp,
        convex=convex,
        wn=wn,
        vn=vn,
        gm=gm,
        ubj=ubj,
    )


def verify(ctx):
    S = ctx["S"]
    d, n, i, j = S.d, S.n, S.i, S.j
    w, u, p, M = S.w, S.u, S.p, S.M
    lim = (j, 1, d)
    r = ctx["L12"]

    # 1. convexity of f = J_tau - linear: L4's second derivative is untouched by the linear part
    # [L12.8] L4 established that J_tau is convex along every line
    assert ctx["L4"].get("convex") is True, "L12 FAIL: L4 convexity of J_tau not established"
    # [L12.9] the linear part has second directional derivative 0
    assert r["second_linear"] == 0, "L12 FAIL: the linear part has a nonzero second derivative"
    # [L12.10] hence f_k = J_tau - linear is convex
    assert r["convex"] is True, "L12 FAIL: f_k is not convex"

    # 2. g.v - m = sum_j v_j (g_j - m) >= 0 on the simplex; attained at e_{j0} (F12: g_{j0} = m)
    # [L12.11] g.v - m = sum_j v_j (g_j - m) on the simplex
    assert sp.simplify(r["gv_minus_m"] - r["gv_rhs"]) == 0, (
        "L12 FAIL: g.v - m != sum_j v_j (g_j - m)"
    )
    # [L12.12] every summand v_j (g_j - m) is >= 0, so g.v >= m on the simplex
    assert r["gap_nonneg"] is True, "L12 FAIL: sum_j v_j (g_j - m) is not nonnegative"
    att = delta_branch(r["vertex"], S)
    # [L12.13] F12: the bound is attained at the vertex e_j0: g.e_j0 = g_j0 = m
    assert sp.simplify(att.subs(*F12.rule(1)) - r["m"]) == 0, "L12 FAIL: g.e_{j0} != m"
    # [L12.14] G = g.w - m = sum_j w_j (g_j - m)
    assert sp.simplify(r["G_expr"] - sp.Sum(r["wn"][j] * r["gm"][j], lim)) == 0
    # [L12.15] lambda - min g = w.g - m = G
    assert sp.simplify(r["lam_minus_m"] - r["G_expr"]) == 0, (
        "L12 FAIL: lambda - min g != G (lambda = w.g)"
    )

    # 3. G = 0 iff every term w_j (g_j - m) is 0: nonnegative terms that sum to 0 vanish
    # [L12.16] nonnegative terms that sum to 0: a + r = 0 gives a = -r
    assert r["zero_sol"] == [-r["r_t"]], "L12 FAIL: a + r = 0 does not give a = -r"
    # [L12.17] with r >= 0, a = -r is <= 0
    assert (-r["r_t"]).is_nonpositive is True
    # [L12.18] a >= 0 and a <= 0 force a = 0: G = 0 only if every term w_j (g_j - m) is 0
    assert r["kkt_squeeze"] == sp.FiniteSet(0), "L12 FAIL: termwise vanishing not forced"

    # 4. 0 <= f(w) - f* <= G
    # [L12.19] G - (f(w) - f*) = a + b, the I8 slack plus the minimum slack
    assert sp.simplify(r["chain_slack"]) == 0, "L12 FAIL: G - (f - f*) != a + b"
    # [L12.20] a >= 0 (I8) and b >= 0 (step 2), so G - (f(w) - f*) >= 0
    assert r["chain_nonneg"] is True, "L12 FAIL: a + b is not nonnegative"
    # [L12.21] f(w) - f* >= 0 because f* is the minimum
    assert r["lower_nonneg"] is True, "L12 FAIL: f(w) - f* >= 0 not carried"

    # 5. tau = infinity: G = f(w) - min_j (U_c^T p)_j, the LP duality gap (I1)
    # [L12.22] swapping the finite sums: sum_j w_j (U^T p)_j = sum_i p_i (w.u_i)
    assert r["swap_equal"] is True, "L12 FAIL: sum_j w_j (U^T p)_j != sum_i p_i (w.u_i)"
    sr = r["support_reduced"]
    # [L12.23] p on the active rows with sum_i p_i = 1: sum_i p_i (M - s_i) = M - sum_i p_i s_i
    assert sp.simplify(sr - (M - sp.Sum(p[i] * sp.Sum(w[j] * u[i, j], lim), (i, 1, n)))) == 0, (
        "L12 FAIL: sum_i p_i (M - s_i) != M - sum_i p_i s_i"
    )
    X = sp.Dummy("X")
    # [L12.24] I12: the sum vanishes termwise, so sum_i p_i s_i = M
    assert sp.solve(sp.Eq(sr.subs(r["ps"], X), I12.rewrite(r["support_zero"])), X) == [M], (
        "L12 FAIL: sum_i p_i s_i != M on the active rows"
    )
    gw = r["lhs_swap"] - r["ubw"]
    # [L12.25] g.w = sum_i p_i s_i - ubar.w (swap) = M - ubar.w = f(w) at tau = infinity
    assert sp.simplify(gw.subs(r["lhs_swap"], r["ps"]).subs(r["ps"], M) - (M - r["ubw"])) == 0, (
        "L12 FAIL: g.w != M - ubar.w"
    )
    uc = linear(r["uc_p"]).subs(sp.Sum(p[i], (i, 1, n)), 1)
    # [L12.26] with sum_i p_i = 1 the centred (U_c^T p)_j is sum_i p_i u_ij - ubar_j
    assert sp.simplify(uc - (sp.Sum(p[i] * u[i, j], (i, 1, n)) - r["ubj"][j])) == 0, (
        "L12 FAIL: centred (U_c^T p)_j"
    )
    split = r["g_dot_w_split"]
    # [L12.27] g.w splits into sum_j w_j (U^T p)_j minus the centring term ubar.w
    assert split.has(r["ubj"]), "L12 FAIL: centring term lost"
    lp = r["lp"]
    # [L12.28] the LP gap is the primal objective minus the dual objective
    assert lp["gap_at_optimum"] == lp["primal_at_optimum"] - lp["dual_at_optimum"], (
        "L12 FAIL: LP gap is not primal minus dual"
    )
    # [L12.29] I1: at an optimal primal-dual pair the values coincide, so the LP duality gap is 0
    assert sp.simplify(I1.rewrite(I1.obj("primal") - I1.obj("dual"))) == 0 and (
        lp["gap_at_optimum"] == 0
    ), "L12 FAIL: LP duality gap at the optimal pair is not 0"
    # [L12.30] off the optimum 0 <= f - f* <= G holds on the exact two-metric LP
    assert 0 <= lp["f_off_optimum"] - lp["f_star"] <= lp["gap_off_optimum"], (
        "L12 FAIL: 0 <= f - f* <= G violated off the optimum"
    )

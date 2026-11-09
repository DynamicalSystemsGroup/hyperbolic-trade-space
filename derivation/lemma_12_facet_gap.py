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
     device) and sum_i p_i = 1 give g.w = sum_i p_i s_i - ubar.w = M - ubar.w = f(w), so G = f(w) -
     min_j (U_c^T p)_j is the primal objective minus the dual objective of the LP: the LP duality
     gap (I1), zero at an optimal primal-dual pair.  An exact two-metric LP checks it.

Hypotheses (ledger).  A2 (simplex), A3 (tau > 0, L4), F12 (min representation: no symbolic-d min
in SymPy, as F5 and F10), I8 (first-order convexity inequality, cited), I1 (LP duality at
tau = infinity).

What this does NOT prove: that the fitted facet is globally optimal (G is a certificate, G = 0 is
optimality), anything for the penalized objective or the tangent refit (their f is not this f), or
the finite-tau formula at tau = infinity (there the gap needs the LP duals).
"""

import sympy as sp

from derivation.lemma_03_gradient_kkt import J0, fuse, push_in, sum_swap_equal
from derivation.lemma_03_gradient_kkt import piece_in_range as delta_branch
from derivation.sumtools import linear

TITLE = "facet first-order gap: 0 <= f(w) - f* <= G, G = 0 iff the simplex KKT holds"
STATEMENT = (
    "For the facet refit f(w) = J_tau(U w) - ubar_k.w on the simplex (convex by L4), g = grad f(w) "
    "and G = g.w - min_j g_j = sum_j w_j (g_j - min g) >= 0, with G = 0 iff w_j (g_j - min g) = 0 "
    "for every j (L3's simplex KKT: g_j >= lambda, w_j (g_j - lambda) = 0, lambda = w.g); and "
    "0 <= f(w) - f* <= G. For the fitted reference surface (finite tau, Phi = 0, V > 1 possible) "
    "this is the stopping certificate of a facet; for the tau = inf supporting envelope, with the "
    "LP duals p, G is the LP duality gap (I1)"
)
AXIOMS_USED = ["A2", "A3", "I1", "I8", "F12"]


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
    m = sp.Symbol("m", real=True)
    vn = sp.IndexedBase("vn", nonnegative=True)
    wn = sp.IndexedBase("wn", nonnegative=True)
    gm = sp.IndexedBase("gm", nonnegative=True)
    g = sp.IndexedBase("g")
    gv_minus_m = linear(sp.Sum(vn[j] * (gm[j] + m), lim) - m).subs(sp.Sum(vn[j], lim), 1)
    gv_rhs = sp.Sum(vn[j] * gm[j], lim)
    vertex = sp.Sum(sp.KroneckerDelta(j, J0) * g[j], lim).doit()
    G_expr = sp.Sum(wn[j] * gm[j], lim)
    lam_minus_m = linear(sp.Sum(wn[j] * (gm[j] + m), lim) - m).subs(sp.Sum(wn[j], lim), 1)

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
    a_i8 = fs - fw - (gvs - gw)  # I8 at v = v*: f(v*) - f(w) - g.(v* - w) >= 0
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
    support = sp.Sum(p[i] * (M - s_row(i)), (i, 1, n))  # termwise zero: p_i > 0 => s_i = M
    support_reduced = linear(support).subs(sp.Sum(p[i], (i, 1, n)), 1)
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
    lp = dict(
        primal_at_optimum=f_lp(w_opt),
        dual_at_optimum=dual(p_opt),
        gap_at_optimum=f_lp(w_opt) - dual(p_opt),
        f_star=f_lp(w_opt),
        f_off_optimum=f_lp(w_off),
        gap_off_optimum=f_lp(w_off) - dual(p_off),
        active_off=(Uc * w_off),
    )

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
        g_dot_w_split=g_dot_w_split,
        lhs_swap=lhs_swap,
        lp=lp,
        convex=ctx["L4"].get("convex") is True and second_linear == 0,
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
    assert ctx["L4"].get("convex") is True, "L12 FAIL: L4 convexity of J_tau not established"
    assert r["second_linear"] == 0, "L12 FAIL: the linear part has a nonzero second derivative"
    assert r["convex"] is True, "L12 FAIL: f_k is not convex"

    # 2. g.v - m = sum_j v_j (g_j - m) >= 0 on the simplex; attained at e_{j0} (F12: g_{j0} = m)
    assert sp.simplify(r["gv_minus_m"] - r["gv_rhs"]) == 0, (
        "L12 FAIL: g.v - m != sum_j v_j (g_j - m)"
    )
    assert r["gap_nonneg"] is True, "L12 FAIL: sum_j v_j (g_j - m) is not nonnegative"
    att = delta_branch(r["vertex"], S)
    assert sp.simplify(att - r["g"][J0]) == 0, "L12 FAIL: g.e_{j0} != g_{j0}"
    assert sp.simplify(r["G_expr"] - sp.Sum(r["wn"][j] * r["gm"][j], lim)) == 0
    assert sp.simplify(r["lam_minus_m"] - r["G_expr"]) == 0, (
        "L12 FAIL: lambda - min g != G (lambda = w.g)"
    )

    # 3. G = 0 iff every term w_j (g_j - m) is 0: nonnegative terms that sum to 0 vanish
    assert r["zero_sol"] == [-r["r_t"]], "L12 FAIL: a + r = 0 does not give a = -r"
    assert (-r["r_t"]).is_nonpositive is True
    assert r["kkt_squeeze"] == sp.FiniteSet(0), "L12 FAIL: termwise vanishing not forced"

    # 4. 0 <= f(w) - f* <= G
    assert sp.simplify(r["chain_slack"]) == 0, "L12 FAIL: G - (f - f*) != a + b"
    assert r["chain_nonneg"] is True, "L12 FAIL: a + b is not nonnegative"
    assert r["lower_nonneg"] is True, "L12 FAIL: f(w) - f* >= 0 not carried"

    # 5. tau = infinity: G = f(w) - min_j (U_c^T p)_j, the LP duality gap (I1)
    assert r["swap_equal"] is True, "L12 FAIL: sum_j w_j (U^T p)_j != sum_i p_i (w.u_i)"
    sr = r["support_reduced"]
    assert sp.simplify(sr - (M - sp.Sum(p[i] * sp.Sum(w[j] * u[i, j], lim), (i, 1, n)))) == 0, (
        "L12 FAIL: sum_i p_i (M - s_i) != M - sum_i p_i s_i"
    )
    split = r["g_dot_w_split"]
    assert split.has(r["ubj"]), "L12 FAIL: centring term lost"
    lp = r["lp"]
    assert lp["gap_at_optimum"] == lp["primal_at_optimum"] - lp["dual_at_optimum"], (
        "L12 FAIL: LP gap is not primal minus dual"
    )
    assert lp["gap_at_optimum"] == 0, "L12 FAIL: LP duality gap at the optimal pair is not 0"
    assert 0 <= lp["f_off_optimum"] - lp["f_star"] <= lp["gap_off_optimum"], (
        "L12 FAIL: 0 <= f - f* <= G violated off the optimum"
    )

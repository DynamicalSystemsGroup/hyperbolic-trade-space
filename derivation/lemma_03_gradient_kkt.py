"""L3 - gradient of J_tau is the softmax-weighted mean of the rows u_i; balanced KKT.

What this proves (symbolic d and n; Sum with symbolic bounds, no enumeration):
  1. J_tau(w) = (1/tau) log( (1/n) sum_i exp(tau sum_j w_j u_ij) ).  For an arbitrary direction
     v (an IndexedBase) the directional derivative d/dt J_tau(w + t v) at t = 0, obtained by
     SymPy differentiation through the Sums, equals sum_i p_i (v . u_i) with
     p_i = exp(tau w.u_i) / sum_l exp(tau w.u_l) = softmax(tau U w)_i.
  2. By Sum algebra (swap of the two finite sums, linearity) sum_i p_i (v . u_i) =
     sum_j v_j G_j with G_j = sum_i p_i u_ij.  Since this holds for arbitrary v, G is the
     gradient: grad J_tau = sum_i p_i u_i.
  3. Balanced KKT.  Stationarity of the Lagrangian J_tau(w) - lambda (sum_j w_j - 1) in the
     direction v reads sum_j v_j (G_j - lambda) = 0.  Instantiating v = e_{j0} (a
     KroneckerDelta direction, used only here) gives (U^T p)_{j0} = lambda for every index j0,
     hence all components of U^T p are equal.
  4. Full simplex KKT (E-2).  The Lagrangian carries a multiplier lambda for sum_j w_j = 1 and
     mu_j >= 0 for w_j >= 0.  Stationarity along e_{j0} gives mu_{j0} = G_{j0} - lambda for every
     j0, so G_j >= lambda (mu_j >= 0).  Complementary slackness w_j mu_j = 0 is
     w_j (G_j - lambda) = 0.  Summing over j with sum_j w_j = 1 (A2) gives lambda = w.G, and for
     a coordinate with w_j > 0 it forces mu_j = 0, i.e. G_j = lambda: the equal-gradient
     condition of step 3 is the w_j > 0 case.  All at symbolic d.
  5. Constructed instance (exact arithmetic, d = 2): rows (2,0) once and (0,2) ten times.  At
     tau = infinity the geometry is balanced (the minimax weights (1/2, 1/2) and the LP dual
     p = (1/2, 1/2) have equal primal and dual value 1 and U^T p = (1, 1)); at tau = 1 the
     minimizer of J_tau on the simplex is w = (1, 0), where G_2 - lambda > 0.  Balanced
     hard-support geometry does not imply an interior finite-tau minimizer: J_tau depends on the
     multiplicity of the observations, the hard maximum only on their extreme support.

Route: directional derivatives d/dt J(w + t v) at t = 0 along a symbolic IndexedBase v (scope
default), not componentwise partials with KroneckerDelta bookkeeping; the single coordinate
direction is used only in step 3.

Hypotheses and honesty about what is used (interpretive conditions, not defects):
  * A2 supplies the simplex constraint sum_j w_j = 1 whose derivative is sum_j v_j.
  * I10 (inherited, Boyd and Vandenberghe 5.5.3) is the first-order necessary condition for a
    minimizer on the simplex: multipliers lambda and mu_j >= 0 with g_j - lambda - mu_j = 0 and
    w_j mu_j = 0.  It is applied by import in steps 3 and 4; it is not re-proved here.
  * R1 supplies the premise of step 3: the minimizer has w_j > 0 for all j, so by
    complementary slackness w_j mu_j = 0 every mu_j vanishes and the stationarity equation
    reads g_j = lambda.  The derivation takes "w* is such a point" as the hypothesis; it does
    not prove that the minimizer is interior.  Step 4 holds without R1.
  * Real-valuedness of w, v, u is not asserted on the IndexedBases (A1: u = log m is real).
    No fallback was needed: every step is proved abstractly.

What this does NOT prove: existence or uniqueness of the minimizer, that the minimizer is
interior (that is R1, and step 5 shows it does not follow from hard-support geometry),
second-order conditions (L4), or anything about the sign of lambda.  The KKT conditions are
necessary at a minimizer (standard calculus); sufficiency at a convex J_tau is L12.

Mimicked from symproof: library/convex.py ``convex_scalar``/``convex_hessian`` (differentiate
symbolically, simplify, then certify) for the derivative step; tactics.py ``signed_sum_lemmas``
is used in L4, not here.
"""

import sympy as sp

from derivation.axioms import A2, I10, R1
from derivation.sumtools import (
    fuse,
    linear,
    linearize,
    piece_in_range,
    push_in,
    replace_indexed,
    sum_swap_equal,
)
from derivation.symbols import J0, L

TITLE = "gradient of the soft-maximum objective and the full simplex KKT conditions"
STATEMENT = (
    "d/dt J_tau(w + t v)|_0 = sum_i p_i (v . u_i) = sum_j v_j (sum_i p_i u_ij), "
    "p = softmax(tau U w), "
    "so grad J_tau = g = U^T p. At a minimizer w of J_tau on the simplex, with lambda = w.g: "
    "g_j >= lambda for all j and w_j (g_j - lambda) = 0 (complementary slackness); the "
    "equal-gradient condition (U^T p)_j = lambda is the case w_j > 0, so all components are "
    "equal at an interior minimizer. Balanced hard-support geometry (tau = infinity) does not "
    "imply an interior finite-tau minimizer: a constructed instance has a balanced hard "
    "optimum and a finite-tau minimizer on the boundary with g_j > lambda at the inactive j"
)
AXIOMS_USED = ["A2", "I10", "R1"]

# the multiplier (the index dummies L and J0 are in derivation/symbols.py)
LAM = sp.Symbol("lambda", real=True)  # Lagrange multiplier of the simplex constraint


# --------------------------------------------------------------------------- derive
def derive(ctx):
    S = ctx["S"]
    d, n, i, j, t = S.d, S.n, S.i, S.j, S.t
    tau = S.tau
    w, v, u = S.w, S.v, S.u

    def a0(x):  # w . u_x
        return sp.Sum(u[x, j] * w[j], (j, 1, d))

    def sv(x):  # v . u_x
        return sp.Sum(u[x, j] * v[j], (j, 1, d))

    def line(x):  # (w + t v) . u_x
        return sp.Sum((w[j] + t * v[j]) * u[x, j], (j, 1, d))

    Z0 = sp.Sum(sp.exp(tau * a0(L)), (L, 1, n))

    def p_def(x):  # softmax(tau U w)_x
        return sp.exp(tau * a0(x)) / Z0

    # J_tau(w + t v), literally (1/tau) log((1/n) sum exp(tau (w + t v).u_l))
    J_line = sp.log(sp.Sum(sp.exp(tau * line(L)), (L, 1, n)) / n) / tau
    # SymPy differentiates through the Sums (symbolic bounds); then t -> 0.
    dJ = sp.diff(J_line, t).subs(t, 0)

    # abstract swap identity (any weights p): sum_i p_i (v.u_i) = sum_j v_j (sum_i p_i u_ij)
    p = S.p
    lhs_abs = sp.Sum(p[i] * sp.Sum(u[i, j] * v[j], (j, 1, d)), (i, 1, n))
    rhs_abs = sp.Sum(v[j] * sp.Sum(p[i] * u[i, j], (i, 1, n)), (j, 1, d))

    # constraint derivative: d/dt sum_j (w_j + t v_j) at 0
    dsimplex = sp.diff(sp.Sum(w[j] + t * v[j], (j, 1, d)), t).subs(t, 0)

    # --- step 4: full simplex KKT.  gr: any gradient family; mu_j >= 0 multiplies w_j >= 0 (A2).
    delta = sp.KroneckerDelta(j, J0)
    # [L3.1] I10: the first-order conditions have gradient components g_j and multipliers mu_j >= 0
    gr, mu = I10.obj("gradient"), I10.obj("mu")
    # [L3.2] I10: stationarity of J - lambda (sum_j w_j - 1) - sum_j mu_j w_j along e_{j0}
    stat_full = sp.Sum(delta * I10.rule(0)[0], (j, 1, d)).doit()
    # [L3.3] I10: g_j = lambda + mu_j and w_j mu_j = 0 termwise, so sum_j w_j (g_j - lambda) = 0
    zero_sum = I10.rewrite(
        sp.Sum(w[j] * (sp.solve(I10.rule(0)[0], gr[j])[0] - LAM), (j, 1, d)), only=(2,)
    ).doit()
    # [L3.4] A2: sum_j w_j = 1 reduces sum_j w_j (g_j - lambda) to w.g - lambda
    reduced = A2.rewrite(linear(sp.Sum(w[j] * (gr[j] - LAM), (j, 1, d))))
    lam_solved = sp.solve(sp.Eq(reduced, zero_sum), LAM)
    # [L3.5] R1: the balanced point has w_j > 0, so w_j is a positive coordinate
    wp = R1.positive_symbol("wp")
    # [L3.6] I10: the multiplier mu_j >= 0 of a coordinate
    mup = I10.nonneg_symbol("mup")
    # [L3.7] I10 with R1: w_j mu_j = 0 and w_j > 0 (so w_j != 0) force mu_j = 0
    mu_zero = [sp.simplify(I10.rule(2)[1] / wp)] if wp.is_nonzero is True else []
    lam_abs = sp.Sum(w[j] * gr[j], (j, 1, d))

    # --- step 5: constructed instance, exact: rows (2,0) once and (0,2) ten times, tau = 1
    R = sp.Rational
    s_ = sp.Symbol("s", real=True)  # w = (s, 1 - s)
    J_s = sp.log((sp.exp(2 * s_) + 10 * sp.exp(2 * (1 - s_))) / 11)
    U_h = sp.Matrix([[2, 0], [0, 2]])
    half = sp.Matrix([R(1, 2), R(1, 2)])
    z = sp.exp(2) + 10  # normalizer at w = (1, 0): scores 2 (once) and 0 (ten times)
    g_b = sp.Matrix([2 * sp.exp(2) / z, 20 / z])  # g = sum_i p_i u_i at w = (1, 0)
    boundary_example = dict(
        s=s_,
        J_s=J_s,
        dJ_at_1=sp.diff(J_s, s_).subs(s_, 1),
        d2J=sp.simplify(sp.diff(J_s, s_, 2)),
        hard_primal=max(*(U_h * half)),
        hard_dual=min(*(U_h.T * half)),
        balanced=U_h.T * half,
        w_star=(1, 0),
        g=g_b,
        lam=g_b[0],  # lambda = w.g at w = (1, 0)
        g_inactive_minus_lambda=g_b[1] - g_b[0],
    )
    KKT_boundary = dict(
        mu=mu,
        gr=gr,
        stat_full=stat_full,
        lambda_abstract=lam_abs,
        lambda_solved=lam_solved,
        mu_of_positive_w=mup,
        positive_case_solution=mu_zero,
    )

    ctx["L3"] = dict(
        a0=a0, sv=sv, p_def=p_def, Z0=Z0, dJ=dJ, lhs_abs=lhs_abs, rhs_abs=rhs_abs,
        dsimplex=dsimplex, boundary_example=boundary_example, KKT_boundary=KKT_boundary,
    )  # fmt: skip


# --------------------------------------------------------------------------- verify
def verify(ctx):
    S = ctx["S"]
    d, n, i, j = S.d, S.n, S.i, S.j
    u, v = S.u, S.v
    c = ctx["L3"]
    p_def, sv = c["p_def"], c["sv"]

    # 1. directional derivative = sum_i p_i (v.u_i)   [equality; dJ computed in derive]
    # (same bound-variable name L as in derive so that structural equality is meaningful)
    claim_L = sp.Sum(p_def(L) * sv(L), (L, 1, n))
    # [L3.8] d/dt J_tau(w + t v) at 0 equals sum_i p_i (v.u_i), p the softmax of tau U w
    assert sp.simplify(linearize(c["dJ"]) - linearize(claim_L)) == 0, (
        "L3 FAIL: d/dt J(w+tv)|0 != sum_i p_i (v.u_i)"
    )
    claim = sp.Sum(p_def(i) * sv(i), (i, 1, n))

    # 2. sum_i p_i (v.u_i) = sum_j v_j G_j for arbitrary weights p, then instantiate p = softmax
    lhs = fuse(push_in(c["lhs_abs"]))
    rhs = fuse(push_in(c["rhs_abs"]))
    # [L3.9] swapping the finite sums: sum_i p_i (v.u_i) = sum_j v_j sum_i p_i u_ij for any p
    assert sum_swap_equal(lhs, rhs), "L3 FAIL: sum_i p_i (v.u_i) != sum_j v_j sum_i p_i u_ij"
    G_abs = lambda x: sp.Sum(S.p[i] * u[i, x], (i, 1, n))  # noqa: E731
    G = lambda x: replace_indexed(G_abs(x), S.p, p_def)  # noqa: E731
    grad_form = sp.Sum(v[j] * G(j), (j, 1, d))
    inst_lhs = replace_indexed(c["lhs_abs"], S.p, p_def)
    # [L3.10] the swap identity holds at the softmax weights p = softmax(tau U w)
    assert linearize(inst_lhs) == linearize(
        sp.Sum(p_def(i) * sp.Sum(u[i, j] * v[j], (j, 1, d)), (i, 1, n))
    ) and linearize(inst_lhs) == linearize(claim), "L3 FAIL: softmax instance of the swap identity"
    # [L3.11] hence the gradient is G_j = sum_i p_i u_ij, as v is arbitrary
    assert linearize(replace_indexed(c["rhs_abs"], S.p, p_def)) == linearize(grad_form), (
        "L3 FAIL: gradient form"
    )

    # 3. balanced KKT.  D_v J = sum_j v_j G_j and D_v(sum_j w_j) = sum_j v_j.
    # [L3.12] the constraint sum_j w_j has directional derivative sum_j v_j
    assert sp.simplify(c["dsimplex"] - sp.Sum(v[j], (j, 1, d)).doit()) == 0, (
        "L3 FAIL: derivative of the simplex constraint"
    )
    # stationarity of the Lagrangian in direction v = e_{j0} (I10), at the softmax gradient G
    kb = c["KKT_boundary"]
    # [L3.13] I10, R1: along e_j0 it reads G_j0 - lambda - mu_j0, and w_j0 > 0 forces mu_j0 = 0
    val = replace_indexed(piece_in_range(kb["stat_full"], S), kb["gr"], G).subs(
        I10.obj("mu")[J0], kb["positive_case_solution"][0]
    )
    # [L3.14] the stationarity condition along e_j0 evaluates to G_j0 - lambda = 0
    assert sp.simplify(val - (G(J0) - LAM)) == 0, "L3 FAIL: stationarity along e_{j0}"
    # hence (U^T p)_{j0} = lambda for every index j0; two indices then give equal components
    K0 = sp.Symbol("k0", integer=True)
    gap = (G(J0) - LAM) - (G(K0) - LAM)
    # [L3.15] G_j0 = lambda for every j0, so all components of U^T p are equal
    assert sp.simplify(gap - (G(J0) - G(K0))) == 0, "L3 FAIL: components of U^T p not equal"
    ctx["L3"]["KKT"] = sp.Eq(G(J0), LAM)

    # 4. full simplex KKT: mu_{j0} = G_{j0} - lambda >= 0, w_j (G_j - lambda) = 0, lambda = w.G
    mu = kb["mu"]
    val_full = piece_in_range(kb["stat_full"], S)
    # [L3.16] full simplex KKT: stationarity along e_j0 gives mu_j0 = G_j0 - lambda
    assert sp.simplify(val_full - (kb["gr"][J0] - LAM - mu[J0])) == 0, (
        "L3 FAIL: stationarity of the full Lagrangian along e_{j0}"
    )
    # [L3.17] mu_j >= 0, hence G_j >= lambda for every j
    assert mu[J0].is_nonnegative is True, "L3 FAIL: mu_j >= 0 not carried (g_j >= lambda)"
    # [L3.18] complementary slackness summed with sum_j w_j = 1 gives lambda = w.G
    assert kb["lambda_solved"] == [kb["lambda_abstract"]], (
        "L3 FAIL: complementary slackness with sum_j w_j = 1 does not give lambda = w.g"
    )
    # [L3.19] a coordinate with w_j > 0 and w_j mu_j = 0 forces mu_j = 0, i.e. G_j = lambda
    assert kb["positive_case_solution"] == [0], (
        "L3 FAIL: w_j > 0 and w_j mu_j = 0 do not force mu_j = 0"
    )
    # the abstract lambda = w.g instantiates at the softmax gradient G = U^T p
    # [L3.20] lambda = w.G instantiates at the softmax gradient G = U^T p
    assert replace_indexed(kb["lambda_abstract"], kb["gr"], G) == sp.Sum(
        S.w[j] * G(j), (j, 1, d)
    ), "L3 FAIL: lambda = w.G at the softmax gradient"

    # 5. balanced hard support, boundary finite-tau minimizer (exact arithmetic).
    ex = c["boundary_example"]
    # hard support: equal primal (w = (1/2, 1/2)) and dual (p = (1/2, 1/2)) values, balanced U^T p
    # [L3.21] constructed instance: at tau = inf primal and dual values are equal (both 1)
    assert ex["hard_primal"] == ex["hard_dual"] == 1, "L3 FAIL: hard-support instance not optimal"
    # [L3.22] the hard-support geometry is balanced: U^T p = (1, 1)
    assert ex["balanced"][0] == ex["balanced"][1], "L3 FAIL: hard-support instance not balanced"
    # finite tau: J(s) is convex (J'' > 0) and decreasing at s = 1, so the minimizer is s = 1
    # [L3.23] at tau = 1, J is strictly convex in s on the simplex segment
    assert ex["d2J"].is_positive is True, "L3 FAIL: instance J_tau not convex in s"
    # [L3.24] J is decreasing at s = 1, so the finite-tau minimizer is w = (1, 0)
    assert bool(ex["dJ_at_1"].evalf() < 0), "L3 FAIL: J_tau not decreasing toward w = (1, 0)"
    # [L3.25] the finite-tau minimizer of the instance is the boundary point w = (1, 0)
    assert ex["w_star"] == (1, 0)
    # at w = (1, 0): lambda = w.g and the inactive coordinate has g_2 > lambda, w_2 = 0
    # [L3.26] at w = (1, 0), lambda = w.g equals g_1
    assert sp.simplify(ex["lam"] - ex["g"][0]) == 0
    # [L3.27] g_2 - lambda equals minus the boundary slope of J at s = 1
    assert sp.simplify(ex["g_inactive_minus_lambda"] + ex["dJ_at_1"]) == 0, (
        "L3 FAIL: g_2 - lambda is not minus the boundary slope"
    )
    # [L3.28] g_2 > lambda at the inactive coordinate: balanced hard support, boundary minimizer
    assert bool(ex["g_inactive_minus_lambda"].evalf() > 0), (
        "L3 FAIL: boundary instance has g_2 <= lambda"
    )

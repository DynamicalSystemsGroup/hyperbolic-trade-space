"""L4 - convexity of J_tau: second directional derivative = tau * Var_p(v.u) >= 0.

What this proves (symbolic d and n; Sum with symbolic bounds, no enumeration):
  1. For an arbitrary direction v, with s_i = v . u_i = sum_j v_j u_ij and
     p_i = exp(tau w.u_i) / sum_l exp(tau w.u_l), SymPy's second derivative of
     J_tau(w + t v) at t = 0 (differentiated through the Sums) equals
     tau * ( sum_i p_i s_i^2 - (sum_i p_i s_i)^2 ) = tau * Var_p(v . u).
  2. With weights p abstract and sum_i p_i = 1 carried as S.p_normalized (a substitution rule,
     not a Python loop), Sum algebra shows
     Var_p(s) = (1/2) sum_i sum_k p_i p_k (s_i - s_k)^2; hence the second derivative is
     (tau/2) sum_i sum_k p_i p_k (s_i - s_k)^2.  The softmax weights satisfy the
     normalization (checked), so the identity applies to them.
  3. Nonnegativity by signed accumulation: each exp term is positive (real argument, A1/A3),
     so Z > 0 and each p_i > 0 (per-term sign), each summand p_i p_k (s_i - s_k)^2 >= 0
     (positive times a square), and the double sum is >= 0 (net direction); tau > 0 (A3)
     finishes.  Hence J_tau is convex along every line, so convex on its domain.

Route: second directional derivative d^2/dt^2 J(w + t v) at t = 0 along a symbolic IndexedBase
v (no Hessian matrix with a symbolic index set).  Convexity of a function is equivalent to
nonnegativity of its second derivative along every line.

I11 (inherited, Boyd and Vandenberghe 3.1.1 and 3.1.4) closes the convexity argument (L4.13):
nonnegativity of the second directional derivative at an arbitrary point in an arbitrary direction
is convexity.

The geometric program (L4.14 to L4.24).  With x_j = exp(w_j) the fit of ONE facet,
minimize J_tau(w) over the simplex, is a geometric program in standard form (Boyd, Kim,
Vandenberghe and Hassibi 2007, I13), and the problem in w is its convex form:
  * exp(tau w.u_i) = prod_j x_j^(tau u_ij) (L4.16), so the objective (1/n) sum_i prod_j
    x_j^(tau u_ij) is a posynomial in x: n terms, coefficient 1/n > 0, real exponents tau u_ij that
    do not depend on x (L4.17);
  * sum_j w_j = 1 is the monomial equality prod_j x_j = e (L4.18, L4.19), and w_j >= 0 is the
    monomial inequality x_j >= 1, that is 1/x_j <= 1 (L4.20, L4.21);
  * the logarithm of the objective in w is tau J_tau(w) (L4.22), which L4.13 shows convex, so the
    problem in w is the convex form of this program (L4.23); I13 concludes that it is a geometric
    program in standard form (L4.24).
Not claimed: the fit of SEVERAL facets is not a geometric program as a whole (each design counts
against its nearest facet, a minimum over facets, and the objective is neither a posynomial nor
convex); each facet's refit with its assigned rows is a program of the one-facet kind.

Real-valuedness: the sign argument needs w.u_i and v.u_i real.  That is A1 (u = log m with
m > 0 is real) with w, v real vectors; the IndexedBases u, w, v of the shared namespace carry
no assumption, so the sign step uses real-valued placeholder families a_r[i] (for w.u_i) and
s_r[i] (for v.u_i).  This is an explicit modelling step, not a fallback; no fallback axiom was
needed.

What this does NOT prove: strict convexity or uniqueness of the minimizer over the simplex
(that needs Var > 0 on the tangent space, a rank condition on the row differences u_i - u_k),
or anything about the constrained problem beyond convexity of the objective.

Mimicked from symproof: library/convex.py ``convex_scalar`` / ``convex_hessian`` (compute the
second derivative, simplify, certify it is nonnegative) and ``gp_to_convex`` (the log-sum-exp
of affine terms pattern: here exp(tau * affine in w) summed over i); tactics.py
``signed_sum_lemmas`` (per-term sign assertion for each term, then the net-direction assertion
for the sum).
"""

import sympy as sp

from derivation.axioms import A1, A2, A3, I11, I13
from derivation.lemma_03_gradient_kkt import L3_RESULT
from derivation.results import ProvedResult
from derivation.sumtools import linearize, posynomial_term, product_to_exp_sum
from derivation.symbols import L

TITLE = "convexity of the soft-maximum objective (second directional derivative = tau Var_p)"
STATEMENT = (
    "d^2/dt^2 J_tau(w + t v)|_0 = tau Var_p(v.u) = (tau/2) sum_i sum_k p_i p_k (s_i - s_k)^2 "
    ">= 0 with p = softmax(tau U w), s_i = v.u_i, so J_tau is convex"
)
AXIOMS_USED = ["A1", "A2", "A3", "I11", "I13"]
L4_RESULT = ProvedResult("L4", STATEMENT)  # taken by L12


def canon_bound(expr, name):
    """Rename the bound variable of every closed single-limit Sum to ``name`` (alpha-renaming),
    so that products of sums over the same range compare and combine structurally."""
    x0 = sp.Symbol(name, integer=True)

    def _ren(s):
        if len(s.limits) != 1 or len(s.limits[0]) != 3:
            return s
        x, a, b = s.limits[0]
        if x == x0 or x0 in s.function.free_symbols:
            return s
        return sp.Sum(s.function.xreplace({x: x0}), (x0, a, b))

    return expr.replace(lambda e: isinstance(e, sp.Sum), _ren)


def apply_normalization(expr, norm):
    """Substitute sum_x p[x] -> 1 using the carried equation ``norm`` (p_normalized)."""
    (lim,) = norm.lhs.limits
    base = norm.lhs.function.base

    def _is_norm(e):
        return (
            isinstance(e, sp.Sum)
            and len(e.limits) == 1
            and e.limits[0][1:] == lim[1:]
            and isinstance(e.function, sp.Indexed)
            and e.function.base == base
            and e.function.indices == (e.limits[0][0],)
        )

    return expr.replace(_is_norm, lambda e: norm.rhs)


def derive(ctx):
    S = ctx["S"]
    n, i, k, t = S.n, S.i, S.k, S.t
    tau = S.tau
    # [L4.1] by L3: the scores w.u_i and v.u_i and the softmax weights p, as L3 defined and proved
    a0, sv, p_def = L3_RESULT.take(ctx, "a0", "sv", "p_def")
    d, j, w, v, u = S.d, S.j, S.w, S.v, S.u

    def line(x):
        return sp.Sum((w[j] + t * v[j]) * u[x, j], (j, 1, d))

    J_line = sp.log(sp.Sum(sp.exp(tau * line(L)), (L, 1, n)) / n) / tau
    d2 = sp.diff(J_line, t, 2).subs(t, 0)  # convex_scalar: second derivative, then certify

    # abstract identity in (p, s): 2 Var = sum_i sum_k p_i p_k (s_i - s_k)^2 given sum p = 1
    p, s = S.p, S.s
    var_abs = sp.Sum(p[i] * s[i] ** 2, (i, 1, n)) - sp.Sum(p[i] * s[i], (i, 1, n)) ** 2
    dbl_abs = sp.Sum(sp.Sum(p[i] * p[k] * (s[i] - s[k]) ** 2, (k, 1, n)), (i, 1, n))

    # real placeholders for the sign step (A1: w.u_i, v.u_i are real)
    # [L4.2] A1: u = log m is real, so the scores w.u_i and v.u_i are real families
    a_r, s_r = A1.real_base("a_r"), A1.real_base("s_r")

    ctx["L4"] = dict(d2=d2, var_abs=var_abs, dbl_abs=dbl_abs, a_r=a_r, s_r=s_r, a0=a0, sv=sv)
    ctx["L4"]["p_def"] = p_def


def verify(ctx):
    S = ctx["S"]
    n, i, k, tau = S.n, S.i, S.k, S.tau
    c = ctx["L4"]
    p_def, sv = c["p_def"], c["sv"]

    # 1. d2 = tau * Var_p(v.u) with softmax weights   [equality]
    var_L = sp.Sum(p_def(L) * sv(L) ** 2, (L, 1, n)) - sp.Sum(p_def(L) * sv(L), (L, 1, n)) ** 2
    # [L4.3] d^2/dt^2 J_tau(w + t v) at 0 equals tau Var_p(v.u) for the softmax weights p
    assert sp.simplify(linearize(c["d2"]) - tau * linearize(var_L)) == 0, (
        "L4 FAIL: second directional derivative != tau * Var_p(v.u)"
    )

    # softmax satisfies the carried normalization sum_i p_i = 1
    norm_lhs = linearize(sp.Sum(p_def(L), (L, 1, n)))
    # [L4.4] the softmax weights satisfy the normalization sum_i p_i = 1
    assert sp.simplify(norm_lhs - S.p_normalized.rhs) == 0, "L4 FAIL: softmax not normalized"

    # 2. 2 Var = double sum, by Sum algebra and p_normalized (abstract p, s)
    expanded = canon_bound(linearize(c["dbl_abs"]), "i")
    expanded = sp.expand(apply_normalization(expanded, S.p_normalized))
    two_var = sp.expand(2 * canon_bound(c["var_abs"], "i"))
    # [L4.5] with sum_i p_i = 1: 2 Var_p(s) = sum_i sum_k p_i p_k (s_i - s_k)^2
    assert sp.simplify(expanded - two_var) == 0, "L4 FAIL: Var_p(s) != (1/2) double sum"
    # (without the normalization the identity must fail: the equation is genuinely used)
    unnormalized = sp.expand(canon_bound(linearize(c["dbl_abs"]), "i"))
    # [L4.6] negative control: without sum_i p_i = 1 the identity fails, so it is used
    assert sp.simplify(unnormalized - two_var) != 0, "L4 FAIL: normalization not load-bearing"

    # 3. signed accumulation (tactics.signed_sum_lemmas): per-term sign, then net direction
    a_r, s_r = c["a_r"], c["s_r"]
    term_exp = sp.exp(tau * a_r[L])
    # [L4.7] each term exp(tau a_i) of the normalizer is positive (real argument, tau > 0)
    assert term_exp.is_positive is True, "L4 FAIL: exp term not positive"
    Z_r = sp.Sum(term_exp, (L, 1, n))
    # [L4.8] the normalizer Z, a net sum of positive terms, is positive
    assert Z_r.is_positive is True, "L4 FAIL: normalizer not positive (net of positive terms)"

    def p_r(x):
        return sp.exp(tau * a_r[x]) / Z_r

    # [L4.9] each softmax weight p_i = exp(tau a_i) / Z is positive
    assert p_r(i).is_positive is True, "L4 FAIL: softmax weight not positive"
    summand = p_r(i) * p_r(k) * (s_r[i] - s_r[k]) ** 2
    # [L4.10] each summand p_i p_k (s_i - s_k)^2 is a positive factor times a square, so >= 0
    assert summand.is_nonnegative is True, "L4 FAIL: per-term p_i p_k (s_i-s_k)^2 not >= 0"
    double = sp.Sum(summand, (i, 1, n), (k, 1, n))
    # [L4.11] the double sum of nonnegative summands is nonnegative
    assert double.is_nonnegative is True, "L4 FAIL: net double sum not >= 0"
    # [L4.12] A3: tau > 0, so (tau / 2) times the double sum is nonnegative: convex along every line
    assert (A3.positive(tau) / 2 * double).is_nonnegative is True, (
        "L4 FAIL: (tau/2) * double sum not >= 0"
    )
    nonneg_everywhere = sp.true if (tau / 2 * double).is_nonnegative is True else sp.false
    # [L4.13] I11: the second derivative along every line is >= 0, so J_tau is convex
    assert I11.entails(
        [sp.Equivalent(I11.obj("premise"), nonneg_everywhere)], I11.obj("conclusion")
    ), "L4 FAIL: convexity does not follow from the sign of the second derivative"
    ctx["L4"]["convex"] = True

    # ---- the one-facet fit is a geometric program in x = exp(w) (I13)
    d, j = S.d, S.j
    lim = (j, 1, d)
    # [L4.14] A2: the exponents satisfy w_j >= 0, so they are real and x_j = exp(w_j) is positive
    wn = A2.nonneg_base("wn")
    # [L4.15] A1: the log-metrics u_ij = log m_ij are real, so the exponents tau u_ij are real
    ur = A1.real_base("ur")
    score_term = sp.Product(sp.exp(wn[j]) ** (tau * ur[i, j]), lim)
    # [L4.16] A2 licenses the logarithm of the positive x_j: prod_j x_j^(tau u_ij) = exp(tau w.u_i)
    assert (
        sp.simplify(
            product_to_exp_sum(score_term, A2) - sp.exp(tau * sp.Sum(wn[j] * ur[i, j], lim))
        )
        == 0
    )
    posy = posynomial_term(1 / n, tau * ur[i, j], wn)
    # [L4.17] the objective (1/n) sum_i prod_j x_j^(tau u_ij) is a posynomial: coefficient 1/n > 0
    assert posy, "L4 FAIL: the objective is not a posynomial in x = exp(w)"
    x_prod = sp.Product(sp.exp(wn[j]), lim)
    # [L4.18] A2: sum_j w_j = 1 is prod_j x_j = e (the product is exp of the sum, which is 1)
    assert A2.rewrite(product_to_exp_sum(x_prod, A2), rename={S.w: wn}) == sp.E
    mono_eq = posynomial_term(sp.exp(-1), sp.Integer(1), wn)
    # [L4.19] prod_j x_j = e is the monomial equality (1/e) prod_j x_j = 1: positive coefficient 1/e
    assert mono_eq, "L4 FAIL: the simplex is not a monomial equality in x"
    y = sp.Symbol("y", real=True)
    # [L4.20] w_j >= 0 is x_j >= 1: exp(y) >= 1 holds exactly for y in [0, oo)
    assert sp.solve_univariate_inequality(
        sp.exp(y) >= 1, y, relational=False, domain=sp.S.Reals
    ) == sp.Interval(0, sp.oo)
    mono_ineq = posynomial_term(sp.Integer(1), sp.Integer(-1), wn)
    # [L4.21] x_j >= 1 is the monomial inequality x_j^(-1) <= 1: coefficient 1, exponent -1
    assert mono_ineq, "L4 FAIL: x_j >= 1 is not a monomial bounded by one"
    J_w = sp.log(sp.Sum(sp.exp(tau * sp.Sum(wn[j] * ur[L, j], lim)), (L, 1, n)) / n) / tau
    f0_terms = sp.Product(sp.exp(wn[j]) ** (tau * ur[L, j]), lim)
    # [L4.22] A2 licenses the logs: the logarithm of the objective f0 in w is tau J_tau(w)
    assert (
        sp.simplify(sp.log(sp.Sum(product_to_exp_sum(f0_terms, A2), (L, 1, n)) / n) - tau * J_w)
        == 0
    ), "L4 FAIL: log f0(exp w) != tau J_tau(w)"
    # [L4.23] the problem in w (minimize log f0(exp w) = tau J_tau(w)) is convex, by L4.13
    assert ctx["L4"]["convex"] is True, "L4 FAIL: the convex form is not convex"
    # [L4.24] I13: a posynomial objective, monomial equality and monomial inequalities make the
    # one-facet fit a geometric program in standard form
    assert I13.entails(
        [
            sp.Equivalent(I13.obj("objective"), sp.true if posy else sp.false),
            sp.Equivalent(I13.obj("equalities"), sp.true if mono_eq else sp.false),
            sp.Equivalent(I13.obj("inequalities"), sp.true if mono_ineq else sp.false),
        ],
        I13.obj("conclusion"),
    ), "L4 FAIL: the one-facet fit is not a geometric program in standard form"
    ctx["L4"]["geometric_program"] = True
    L4_RESULT.certify(ctx)

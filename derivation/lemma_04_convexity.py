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

from derivation.lemma_03_gradient_kkt import L, linearize

TITLE = "convexity of the soft-maximum objective (second directional derivative = tau Var_p)"
STATEMENT = (
    "d^2/dt^2 J_tau(w + t v)|_0 = tau Var_p(v.u) = (tau/2) sum_i sum_k p_i p_k (s_i - s_k)^2 "
    ">= 0 with p = softmax(tau U w), s_i = v.u_i, so J_tau is convex"
)
AXIOMS_USED = ["A1", "A3"]


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
    n, i, k, t, tau = S.n, S.i, S.k, S.t, S.tau
    c3 = ctx["L3"]  # a0, sv, p_def, Z0 from L3
    a0, sv, p_def = c3["a0"], c3["sv"], c3["p_def"]
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
    a_r = sp.IndexedBase("a_r", real=True)
    s_r = sp.IndexedBase("s_r", real=True)

    ctx["L4"] = dict(d2=d2, var_abs=var_abs, dbl_abs=dbl_abs, a_r=a_r, s_r=s_r, a0=a0, sv=sv)
    ctx["L4"]["p_def"] = p_def


def verify(ctx):
    S = ctx["S"]
    n, i, k, tau = S.n, S.i, S.k, S.tau
    c = ctx["L4"]
    p_def, sv = c["p_def"], c["sv"]

    # 1. d2 = tau * Var_p(v.u) with softmax weights   [equality]
    var_L = sp.Sum(p_def(L) * sv(L) ** 2, (L, 1, n)) - sp.Sum(p_def(L) * sv(L), (L, 1, n)) ** 2
    assert sp.simplify(linearize(c["d2"]) - tau * linearize(var_L)) == 0, (
        "L4 FAIL: second directional derivative != tau * Var_p(v.u)"
    )

    # softmax satisfies the carried normalization sum_i p_i = 1
    norm_lhs = linearize(sp.Sum(p_def(L), (L, 1, n)))
    assert sp.simplify(norm_lhs - S.p_normalized.rhs) == 0, "L4 FAIL: softmax not normalized"

    # 2. 2 Var = double sum, by Sum algebra and p_normalized (abstract p, s)
    expanded = canon_bound(linearize(c["dbl_abs"]), "i")
    expanded = sp.expand(apply_normalization(expanded, S.p_normalized))
    two_var = sp.expand(2 * canon_bound(c["var_abs"], "i"))
    assert sp.simplify(expanded - two_var) == 0, "L4 FAIL: Var_p(s) != (1/2) double sum"
    # (without the normalization the identity must fail: the equation is genuinely used)
    unnormalized = sp.expand(canon_bound(linearize(c["dbl_abs"]), "i"))
    assert sp.simplify(unnormalized - two_var) != 0, "L4 FAIL: normalization not load-bearing"

    # 3. signed accumulation (tactics.signed_sum_lemmas): per-term sign, then net direction
    a_r, s_r = c["a_r"], c["s_r"]
    term_exp = sp.exp(tau * a_r[L])
    assert term_exp.is_positive is True, "L4 FAIL: exp term not positive"
    Z_r = sp.Sum(term_exp, (L, 1, n))
    assert Z_r.is_positive is True, "L4 FAIL: normalizer not positive (net of positive terms)"

    def p_r(x):
        return sp.exp(tau * a_r[x]) / Z_r

    assert p_r(i).is_positive is True, "L4 FAIL: softmax weight not positive"
    summand = p_r(i) * p_r(k) * (s_r[i] - s_r[k]) ** 2
    assert summand.is_nonnegative is True, "L4 FAIL: per-term p_i p_k (s_i-s_k)^2 not >= 0"
    double = sp.Sum(summand, (i, 1, n), (k, 1, n))
    assert double.is_nonnegative is True, "L4 FAIL: net double sum not >= 0"
    assert (tau / 2 * double).is_nonnegative is True, "L4 FAIL: (tau/2) * double sum not >= 0"
    ctx["L4"]["convex"] = True

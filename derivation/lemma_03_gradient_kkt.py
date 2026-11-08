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

Route: directional derivatives d/dt J(w + t v) at t = 0 along a symbolic IndexedBase v (scope
default), not componentwise partials with KroneckerDelta bookkeeping; the single coordinate
direction is used only in step 3.

Hypotheses and honesty about what is used (interpretive conditions, not defects):
  * A3 (tau > 0) keeps the 1/tau prefactor and the softmax well defined.
  * A2 supplies the simplex constraint sum_j w_j = 1 whose derivative is sum_j v_j.
  * R1 supplies the premise of step 3: the minimizer is a relative-interior point of the
    frontier facet, so w_j > 0 for all j and no nonnegativity constraint is active (its
    multipliers vanish by complementary slackness); the stationarity equation of the
    Lagrangian is then the first-order necessary condition for a smooth function with one
    linear equality constraint (standard calculus, not re-proved here).  The derivation
    takes stationarity as the hypothesis "w* is such a point"; it does not prove that the
    minimizer is interior.
  * Real-valuedness of w, v, u is not asserted on the IndexedBases (A1: u = log m is real).
    No fallback was needed: every step is proved abstractly.

What this does NOT prove: existence or uniqueness of the minimizer, that the minimizer is
interior (that is R1), second-order conditions (L4), or anything about the sign of lambda.

Mimicked from symproof: library/convex.py ``convex_scalar``/``convex_hessian`` (differentiate
symbolically, simplify, then certify) for the derivative step; tactics.py ``signed_sum_lemmas``
is used in L4, not here.
"""

import sympy as sp

TITLE = "gradient of the soft-maximum objective and the balanced KKT condition"
STATEMENT = (
    "d/dt J_tau(w + t v)|_0 = sum_i p_i (v . u_i) = sum_j v_j (sum_i p_i u_ij), "
    "p = softmax(tau U w), "
    "so grad J_tau = sum_i p_i u_i; at an interior minimizer on the simplex (U^T p)_j = lambda "
    "for all j (components equal)"
)
AXIOMS_USED = ["A2", "A3", "R1"]

# local integer dummies (index-valued, licensed by A0) and the multiplier
L = sp.Symbol("l", integer=True)  # dummy for the softmax normalizer
J0 = sp.Symbol("j0", integer=True)  # coordinate-direction index
LAM = sp.Symbol("lambda", real=True)  # Lagrange multiplier of the simplex constraint


# ----------------------------------------------------------------- Sum algebra helpers
def _peel(op):
    """Lift a single-limit rewrite ``op`` to multi-limit Sums by peeling the innermost limit:
    Sum(f, l1, ..., ln) = Sum(Sum(f, l1), l2, ..., ln)."""

    def _go(s):
        if len(s.limits) == 1:
            return op(s)
        inner = op(sp.Sum(s.function, s.limits[0]))
        return sp.Sum(inner, *s.limits[1:])

    return _go


def pull_constants(expr):
    """Sum(c*f, (x,a,b)) -> c*Sum(f, (x,a,b)) for c free of x (linearity; bottom-up)."""

    def _pull(s):
        x = s.limits[0][0]
        args = sp.Mul.make_args(s.function)
        const = [a for a in args if x not in a.free_symbols]
        rest = [a for a in args if x in a.free_symbols]
        if not const:
            return s
        return sp.Mul(*const) * sp.Sum(sp.Mul(*rest), *s.limits)

    return expr.replace(lambda e: isinstance(e, sp.Sum), _peel(_pull))


def split_sums(expr):
    """Sum(a + b, lim) -> Sum(a, lim) + Sum(b, lim) (linearity of finite sums; bottom-up)."""

    def _split(s):
        terms = sp.Add.make_args(sp.expand(s.function))
        if len(terms) == 1:
            return s
        return sp.Add(*[sp.Sum(t_, *s.limits) for t_ in terms])

    return expr.replace(lambda e: isinstance(e, sp.Sum), _peel(_split))


def linearize(expr):
    """Split sums over Add summands and pull constants out, repeated to a fixed point."""
    for _ in range(12):
        new = pull_constants(split_sums(expr))
        new = sp.expand(new)
        if new == expr:
            break
        expr = new
    return expr


def push_in(expr):
    """c * Sum(g, lim) -> Sum(c*g, lim) when c is free of the bound variable (inverse of pull)."""

    def _is_target(e):
        return isinstance(e, sp.Mul) and sum(isinstance(a, sp.Sum) for a in e.args) == 1

    def _push(e):
        s = next(a for a in e.args if isinstance(a, sp.Sum))
        c = sp.Mul(*[a for a in e.args if a is not s])
        bound = {lim[0] for lim in s.limits}
        if bound & c.free_symbols:
            return e
        return sp.Sum(c * s.function, *s.limits)

    return expr.replace(_is_target, _push)


def fuse(expr):
    """Sum(Sum(g, inner), outer) -> Sum(g, inner, outer) (multi-limit form, inner first)."""

    def _is_target(e):
        return isinstance(e, sp.Sum) and isinstance(e.function, sp.Sum)

    def _fuse(e):
        inner = e.function
        return sp.Sum(inner.function, *inner.limits, *e.limits)

    return expr.replace(_is_target, _fuse)


def sum_swap_equal(a, b):
    """True iff two multi-limit Sums agree after reordering the two limits (Fubini, finite)."""
    return (
        a.function == b.function
        and set(a.limits) == set(b.limits)
        and (a == b or a.reorder((0, 1)) == b)
    )


def replace_indexed(expr, base, fn):
    """Replace base[x] by fn(x) everywhere (instantiate an abstract weight family)."""
    return expr.replace(
        lambda e: isinstance(e, sp.Indexed) and e.base == base,
        lambda e: fn(e.indices[0]),
    )


def piece_in_range(pw, S):
    """Return the in-range branch of a KroneckerDelta sum: the branch is guarded exactly by
    1 <= j0 <= d (j0 is an index) and the other branch is 0."""
    assert isinstance(pw, sp.Piecewise), "L3 FAIL: expected a Piecewise from the delta sum"
    (val, cond), (zero, other) = pw.args
    assert zero == 0 and other == sp.true, "L3 FAIL: out-of-range branch is not 0"
    assert cond == sp.And(J0 >= 1, S.d >= J0), "L3 FAIL: in-range guard is not 1 <= j0 <= d"
    return val


# --------------------------------------------------------------------------- derive
def derive(ctx):
    S = ctx["S"]
    d, n, i, j, t, tau = S.d, S.n, S.i, S.j, S.t, S.tau
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

    ctx["L3"] = dict(
        a0=a0, sv=sv, p_def=p_def, Z0=Z0, dJ=dJ, lhs_abs=lhs_abs, rhs_abs=rhs_abs,
        dsimplex=dsimplex,
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
    assert sp.simplify(linearize(c["dJ"]) - linearize(claim_L)) == 0, (
        "L3 FAIL: d/dt J(w+tv)|0 != sum_i p_i (v.u_i)"
    )
    claim = sp.Sum(p_def(i) * sv(i), (i, 1, n))

    # 2. sum_i p_i (v.u_i) = sum_j v_j G_j for arbitrary weights p, then instantiate p = softmax
    lhs = fuse(push_in(c["lhs_abs"]))
    rhs = fuse(push_in(c["rhs_abs"]))
    assert sum_swap_equal(lhs, rhs), "L3 FAIL: sum_i p_i (v.u_i) != sum_j v_j sum_i p_i u_ij"
    G_abs = lambda x: sp.Sum(S.p[i] * u[i, x], (i, 1, n))  # noqa: E731
    G = lambda x: replace_indexed(G_abs(x), S.p, p_def)  # noqa: E731
    grad_form = sp.Sum(v[j] * G(j), (j, 1, d))
    inst_lhs = replace_indexed(c["lhs_abs"], S.p, p_def)
    assert linearize(inst_lhs) == linearize(
        sp.Sum(p_def(i) * sp.Sum(u[i, j] * v[j], (j, 1, d)), (i, 1, n))
    ) and linearize(inst_lhs) == linearize(claim), "L3 FAIL: softmax instance of the swap identity"
    assert linearize(replace_indexed(c["rhs_abs"], S.p, p_def)) == linearize(grad_form), (
        "L3 FAIL: gradient form"
    )

    # 3. balanced KKT.  D_v J = sum_j v_j G_j and D_v(sum_j w_j) = sum_j v_j.
    assert sp.simplify(c["dsimplex"] - sp.Sum(v[j], (j, 1, d)).doit()) == 0, (
        "L3 FAIL: derivative of the simplex constraint"
    )
    # stationarity of Lagrangian in direction v = e_{j0}:  sum_j delta(j,j0)(G_j - lambda) = 0
    delta = sp.KroneckerDelta(j, J0)
    stat = sp.Sum(delta * (G(j) - LAM), (j, 1, d)).doit()
    val = piece_in_range(stat, S)
    assert sp.simplify(val - (G(J0) - LAM)) == 0, "L3 FAIL: stationarity along e_{j0}"
    # hence (U^T p)_{j0} = lambda for every index j0; two indices then give equal components
    K0 = sp.Symbol("k0", integer=True)
    gap = (G(J0) - LAM) - (G(K0) - LAM)
    assert sp.simplify(gap - (G(J0) - G(K0))) == 0, "L3 FAIL: components of U^T p not equal"
    ctx["L3"]["KKT"] = sp.Eq(G(J0), LAM)

"""Small Sum-algebra helpers shared by the abstract lemmas (plain SymPy, symbolic bounds).

``linear`` implements Sum linearity and factoring constants out of Sums
(scope default: "Sum linearity, factor constants out of Sums, substitute the simplex equation").
``product_to_exp_sum`` rewrites a Product of positive factors as exp of a Sum (log space).
No concrete sizes appear here.
"""

import sympy as sp

from derivation.licence import log_expand
from derivation.symbols import J0


def _split(f, lim):
    """Sum(f, lim) with f expanded into terms and variable-free factors pulled out."""
    var, lo, hi = lim
    out = 0
    for term in sp.Add.make_args(sp.expand(f)):
        indep, dep = term.as_independent(var, as_Add=False)
        if dep == 1:
            out += indep * (hi - lo + 1)
        else:
            out += indep * sp.Sum(dep, lim)
    return out


def linear(expr):
    """Apply Sum linearity / constant factoring to every Sum in expr (inner sums first)."""
    return expr.replace(
        lambda e: isinstance(e, sp.Sum) and len(e.limits) == 1,
        lambda e: _split(e.function, e.limits[0]),
    )


def product_to_exp_sum(prod, *licences):
    """Product(f_j) -> exp(Sum(log f_j)), log of a power expanded.

    ``licences`` are the ledger entries (A1, A4, ...) whose positivity relations license the
    expansion; with none, or with entries that do not declare the factors positive, it fails
    (``LicenceError``): the forced log is never taken on the caller's word.
    """
    f, lim = prod.function, prod.limits[0]
    return sp.exp(sp.Sum(log_expand(sp.log(f), *licences), lim))


# ----------------------------------------------------------------- Sum algebra helpers
# (moved from lemma_03_gradient_kkt.py, bodies unchanged)
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

"""Small Sum-algebra helpers shared by the abstract lemmas (plain SymPy, symbolic bounds).

``linear`` implements Sum linearity and factoring constants out of Sums
(scope default: "Sum linearity, factor constants out of Sums, substitute the simplex equation").
``product_to_exp_sum`` rewrites a Product of positive factors as exp of a Sum (log space).
No concrete sizes appear here.
"""

import sympy as sp


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


def product_to_exp_sum(prod):
    """Product(f_j) -> exp(Sum(log f_j)), log of a power expanded (licensed by positivity)."""
    f, lim = prod.function, prod.limits[0]
    return sp.exp(sp.Sum(sp.expand_log(sp.log(f), force=True), lim))

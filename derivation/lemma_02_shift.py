"""L2 - Uniform shift of the data shifts the soft-max fit by the same constant.

What this proves (symbolic d, n; w on the simplex, tau > 0):
  J_tau(w; U + c 1^T) = J_tau(w; U) + c, where
  J_tau(w; U) = (1/tau) log( (1/n) sum_{i=1}^n exp(tau sum_j w_j u_ij) ).
  Hence beta = J_tau(w*) shifts by c and w* is unchanged (the minimizer of J + c).

What this does NOT prove: that w* exists or is unique (L3/L4, R1), nor any statement for
non-uniform (per-metric) shifts, which change the facet (spec section 4, item 6).

Route: Sum linearity / constant factoring (sumtools.linear), substitution of the simplex
equation, log space. The step log(e^{tau c} X) = tau c + log X needs X > 0; X is a sum of
exponentials of real numbers, each term positive (A3 does not enter here, A2 and tau > 0 do),
so expand_log(force=True) is licensed.
"""

import sympy as sp

from derivation.sumtools import linear

TITLE = "Uniform shift: J_tau(w; U + c 1^T) = J_tau(w; U) + c"
STATEMENT = "J_tau(w; U + c 1^T) = J_tau(w; U) + c for all n, d, w in the simplex, tau > 0"
AXIOMS_USED = ["A2", "A3"]


def J(S, shift=0):
    """J_tau(w; U + shift) as an abstract expression in symbolic n, d."""
    i, j, n, d, w, u, tau = S.i, S.j, S.n, S.d, S.w, S.u, S.tau
    score = sp.Sum(w[j] * (u[i, j] + shift), (j, 1, d))
    return sp.log(sp.Sum(sp.exp(tau * score), (i, 1, n)) / n) / tau


def derive(ctx):
    S = ctx["S"]
    i, n, d, w, u, tau, c, j = S.i, S.n, S.d, S.w, S.u, S.tau, S.c, S.j
    base = J(S)
    shifted = J(S, c)

    # Per-term: tau * sum_j w_j (u_ij + c) = tau * s_i + tau * c  (A2: sum_j w_j = 1).
    term_lin = linear(tau * sp.Sum(w[j] * (u[i, j] + c), (j, 1, d))).subs(S.simplex.lhs, 1)
    s_i = sp.Sum(w[j] * u[i, j], (j, 1, d))
    term_ok = sp.expand(term_lin - (tau * s_i + tau * c))

    # exp(tau s_i + tau c) = e^{tau c} exp(tau s_i): factor e^{tau c} out of the sum over i.
    summand = sp.expand(sp.exp(term_lin))
    total = linear(sp.Sum(summand, (i, 1, n)))
    # log of product: positivity of the Sum of exponentials licenses the force (see docstring).
    shifted_lin = sp.expand_log(sp.log(total / n), force=True) / tau

    ctx["L2"] = {
        "J": base,
        "J_shifted": shifted,
        "term_diff": term_ok,
        "J_shifted_reduced": sp.expand(shifted_lin),
    }
    return ctx["L2"]


def verify(ctx):
    S = ctx["S"]
    r = ctx["L2"]
    assert r["term_diff"] == 0, "L2 FAIL: per-term shift tau*(s_i + c) not obtained from simplex"
    # J(U + c) after Sum algebra equals J(U) + c.
    lhs = r["J_shifted_reduced"]
    rhs = sp.expand(sp.expand_log(r["J"], force=True) + S.c)
    diff = sp.simplify(sp.expand_log(lhs - rhs, force=True))
    assert diff == 0, f"L2 FAIL: J(U + c1^T) - (J(U) + c) = {diff}"

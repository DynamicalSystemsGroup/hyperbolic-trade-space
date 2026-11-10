"""L2 - Uniform shift of the data shifts the soft-max fit by the same constant.

What this proves (symbolic d, n; w on the simplex, tau > 0):
  J_tau(w; U + c 1^T) = J_tau(w; U) + c, where
  J_tau(w; U) = (1/tau) log( (1/n) sum_{i=1}^n exp(tau sum_j w_j u_ij) ).
  Hence beta = J_tau(w*) shifts by c and w* is unchanged (the minimizer of J + c).

What this does NOT prove: that w* exists or is unique (L3/L4, R1), nor any statement for
non-uniform (per-metric) shifts, which change the term (spec section 4, item 6).

Route: Sum linearity / constant factoring (sumtools.linear), substitution of the simplex
equation, log space. The step log(e^{tau c} X) = tau c + log X needs X > 0; X is a sum of
exponentials of real numbers (u = log m is real by A1, w by A2, tau > 0 by A3), each term
positive, so the forced expansion is licensed by A1, A2 and A3 together (it raises without them).
"""

import sympy as sp

from derivation.axioms import A1, A2, A3
from derivation.licence import log_expand
from derivation.sumtools import linear

TITLE = "Uniform shift: J_tau(w; U + c 1^T) = J_tau(w; U) + c"
STATEMENT = "J_tau(w; U + c 1^T) = J_tau(w; U) + c for all n, d, w in the simplex, tau > 0"
AXIOMS_USED = ["A1", "A2", "A3"]


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
    # [L2.1] A2: sum_j w_j = 1 turns tau sum_j w_j (u_ij + c) into tau s_i + tau c
    term_lin = A2.rewrite(linear(tau * sp.Sum(w[j] * (u[i, j] + c), (j, 1, d))))
    s_i = sp.Sum(w[j] * u[i, j], (j, 1, d))
    term_ok = sp.expand(term_lin - (tau * s_i + tau * c))

    # exp(tau s_i + tau c) = e^{tau c} exp(tau s_i): factor e^{tau c} out of the sum over i.
    summand = sp.expand(sp.exp(term_lin))
    total = linear(sp.Sum(summand, (i, 1, n)))
    # log of product: positivity of the Sum of exponentials licenses the force (see docstring).
    # [L2.2] A1, A2, A3: log(e^{tau c} X) = tau c + log X for the positive sum X, then / tau
    shifted_lin = log_expand(sp.log(total / n), A1, A2, A3) / tau

    # the corollary: the shift J_tau(w; U + c 1^T) - J_tau(w; U), for any w, and two values of J
    # [L2.3] A1, A2, A3: the shift amount J(w; U + c 1^T) - J(w; U) after the Sum algebra
    shift_amount = sp.simplify(
        log_expand(sp.expand(shifted_lin) - log_expand(base, A1, A2, A3), A1, A2, A3)
    )
    Jw, Jw2 = sp.symbols("J_w J_w2", real=True)  # J_tau(w; U) and J_tau(w'; U), any two weights

    ctx["L2"] = {
        "shift_amount": shift_amount,
        "J_w": Jw,
        "J_w2": Jw2,
        "J": base,
        "J_shifted": shifted,
        "term_diff": term_ok,
        "J_shifted_reduced": sp.expand(shifted_lin),
    }
    return ctx["L2"]


def verify(ctx):
    S = ctx["S"]
    r = ctx["L2"]
    # [L2.4] per term, tau sum_j w_j (u_ij + c) - (tau s_i + tau c) is 0
    assert r["term_diff"] == 0, "L2 FAIL: per-term shift tau*(s_i + c) not obtained from simplex"
    # J(U + c) after Sum algebra equals J(U) + c.
    lhs = r["J_shifted_reduced"]
    # [L2.5] J_tau(U + c 1^T) - (J_tau(U) + c) is 0 after the Sum algebra (logs: A1, A2, A3)
    assert (
        sp.simplify(log_expand(lhs - sp.expand(log_expand(r["J"], A1, A2, A3) + S.c), A1, A2, A3))
        == 0
    ), "L2 FAIL: J(U + c1^T) - (J(U) + c) != 0"
    # Corollary: beta = J_tau(w*; U) shifts by c, and w* is unchanged.
    shift, Jw, Jw2 = r["shift_amount"], r["J_w"], r["J_w2"]
    # [L2.6] beta shifts by c: the shift amount of J(w*; .) is c
    assert sp.simplify(shift - S.c) == 0, "L2 FAIL: beta does not shift by c"
    # [L2.7] for any weights w, w' the gap of the shifted objective equals the unshifted gap
    assert sp.simplify(((Jw2 + shift) - (Jw + shift)) - (Jw2 - Jw)) == 0, (
        "L2 FAIL: the shift does not cancel in the gap J(w') - J(w)"
    )
    # [L2.8] so J(w') >= J(w) for every w' exactly when the shifted J(w') >= J(w) does: w* unchanged
    assert sp.Ge((Jw2 + shift) - (Jw + shift), 0) == sp.Ge(Jw2 - Jw, 0), (
        "L2 FAIL: the minimizer moved under the shift"
    )

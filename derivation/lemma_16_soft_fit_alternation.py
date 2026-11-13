"""L16 - soft-weight alternation: the symmetry argument, the bound by the fixed-weight objective,
and the fixed-weight objective as a generalized posynomial.

Setting.  K terms with exponents w_k on the simplex and offsets beta_k = J_tau(U w_k) (the log-mean-
exp over ALL N designs, so every design constrains every term).  Row i has score x_ik = w_k.u_i -
beta_k under term k and slack s_ik = -x_ik.  The soft model is Phi_i = (1/kappa) log sum_k
exp(kappa x_ik) (L10) and the fit minimizes the mean slack F(W) = -(1/N) sum_i Phi_i.  No design is
assigned to a term: every design has a score under every term.

The weights.  alpha_ik = softmax_k(kappa x0_ik), the softmax of the scores of the CURRENT model x0
(alpha_ik > 0 and sum_k alpha_ik = 1).  They stay fixed while W moves.

What this proves (symbolic K, d, N; plain SymPy):
  (i) Symmetry.  F depends on the terms only through sum_k h_k, h_k = exp(kappa x_ik) with term k's
     own data, so cyclically shifting the terms by any s in 0..K-1 leaves F unchanged (the two
     index ranges of the shifted sum re-index to the sum over 1..K).  The average of the K cyclic
     shifts of any W puts the mean of the terms at every position, so it is the point with all
     terms equal.  By Jensen (I14, taken as a declared inherited result) a CONVEX function that is
     symmetric in the terms is, at the all-equal point, at most its value at W: F(all equal) =
     F(W) - J with J >= 0.  So such a program attains its minimum with all terms equal.  What this
     does NOT say is that the fit has no distinct-term optimum; it says F, a symmetric function
     that is lower at distinct terms than at the all-equal point on the planted data, is not
     convex.  A small exact instance (N = 4 designs, K = 2 terms, d = 2, tau = kappa = 1) is
     computed: F(W) = F(W with its terms swapped), and F at their midpoint, which is the all-equal
     point, is larger by 0.0046, a violation of convexity.  The all-equal point is a stationary
     point of F that is not the planted answer.
 (ii) The bound.  For any positive weights alpha on the simplex, Gibbs' inequality log sum_k
     exp(a_k) >= sum_k alpha_k a_k - sum_k alpha_k log alpha_k holds (Jensen, I14, applied to the
     convex -log at the points exp(a_k)/alpha_k with weights alpha_k), with equality when alpha =
     softmax(a).  With a_k = kappa x_ik this reads, for the slack -Phi_i of the soft model,
         -Phi_i  <=  sum_k alpha_ik s_ik  -  H_i / kappa,        H_i = -sum_k alpha_ik log alpha_ik,
     with equality when x_i = x0_i (the weights' own model).  Averaged over the rows, the
     alpha-weighted slack regroups as sum_k (n_k/N)(beta_k - ubar_k . w_k) with n_k = sum_i alpha_ik
     and n_k ubar_k = sum_i alpha_ik u_i.  The fixed-weight objective is this sum less the constant
     E = (1/(kappa N)) sum_i H_i, which does not depend on W (so it has the same minimizers as
     the sum): F(W) <= G_alpha(W) for every W, with F = G_alpha at the weights' own model.  This is
     the arithmetic-geometric mean inequality applied to the sum over terms.
(iii) The program.  With x_kj = exp(w_kj), the exponential of the fixed-weight objective is a
     product over terms of positive powers of the posynomial P_k(x) = (1/N) sum_i prod_j
     x_kj^(tau u_ij) and of the monomial prod_j x_kj^(-ubar_kj): a generalized posynomial in x
     (the tutorial's section 5.3; I15).  The program minimizes its logarithm, as in L4.22.

What this does NOT prove: that the alternation converges, that its limit is a local or global
minimizer, or any property of the fit for an infinite kappa (the weights are then a one-label
assignment, L14 and L15); that every permutation (rather than the cyclic shifts) leaves F
unchanged; that the all-equal point is the only symmetric optimum.  The numbers of the research
sprint that preceded it (its report is in history at 73c5bff) are the numerical check this lemma
reproduces in its exact instance.
"""

import sympy as sp

from derivation.axioms import A1, A2, A3, A6, I14, I15
from derivation.licence import log_expand
from derivation.sumtools import fuse, linearize, posynomial_term, push_in

TITLE = "soft-weight alternation: symmetry, the fixed-weight bound and the generalized posynomial"
STATEMENT = (
    "Soft-weight alternation: with weights alpha_ik = softmax_k(kappa score_ik) from the current "
    "model, (i) a convex program symmetric in the terms attains its minimum with all terms "
    "equal, so the objective over all terms is not convex in them in general; (ii) the soft "
    "model's slack is bounded above by the fixed-weight objective, with equality at the weights' "
    "own model; (iii) the fixed-weight objective is a generalized posynomial in exp(w)."
)
AXIOMS_USED = ["A1", "A2", "A3", "A6", "I14", "I15"]


def _canon(expr):
    """Sum linearity, constants pulled in, multi-limit form with the limits in a fixed order."""
    expr = sp.expand(linearize(expr))
    for _ in range(4):
        expr = sp.expand(fuse(push_in(expr)))

    def _sort(s):
        return sp.Sum(s.function, *sorted(s.limits, key=lambda lim: str(lim[0])))

    return expr.replace(lambda e: isinstance(e, sp.Sum) and len(e.limits) > 1, _sort)


def _rename(expr, old, new):
    """Rename the bound variable ``old`` of every Sum to ``new`` (the same sum, one dummy)."""
    return expr.replace(
        lambda e: isinstance(e, sp.Sum) and e.limits[0][0] == old,
        lambda e: sp.Sum(e.function.xreplace({old: new}), (new, *e.limits[0][1:])),
    )


def _F(T, n, kappa):
    """F = -(1/N) sum_i (1/kappa) log T_i, T_i the sum over terms of exp(kappa score)."""
    i = sp.Symbol("i", integer=True)
    return -sp.Sum(sp.log(T[i]), (i, 1, n)) / (n * kappa)


def derive(ctx):
    S = ctx["S"]
    n, K, d = S.n, S.K, S.d
    i, j, k, kappa, tau = S.i, S.j, S.k, S.kappa, S.tau
    s, t = sp.symbols("s t", integer=True)
    out = {}

    # ---------------------------------------------------------------- (i) symmetry
    h = sp.IndexedBase("h")  # h[i, k] = exp(kappa x_ik): term k's contribution to row i's sum
    # [L16.1] shifting the K terms by s in 0..K-1 sends position k to term k+s, wrapped: the head
    # is positions 1..K-s and the tail positions K-s+1..K; re-indexed, the head is the terms
    # s+1..K and the tail the terms 1..s
    head = sp.Sum(h[i, k + s], (k, 1, K - s)).change_index(k, k + s, t)
    tail = sp.Sum(h[i, k + s - K], (k, K - s + 1, K)).change_index(k, k + s - K, t)
    # [L16.2] the shifted sum over the terms equals the unshifted sum, so row i's soft slack is
    # unchanged
    out["shift_gap"] = sp.simplify(head + tail - sp.Sum(h[i, t], (t, 1, K)))
    T = sp.IndexedBase("T")  # T[i] = sum_k h[i, k], the soft maximum's argument for row i
    # [L16.3] F is a function of the sums T_i alone, so F(shifted terms) - F = 0
    out["F_shift_gap"] = sp.simplify(
        _F(T, n, kappa).subs(T[i], head + tail)
        - _F(T, n, kappa).subs(T[i], sp.Sum(h[i, t], (t, 1, K)))
    )
    th = sp.IndexedBase("th")  # th[k, j]: coordinate j of term k
    # [L16.4] the average over the K cyclic shifts puts at position k the sum of the terms
    # k..K (shifts 0..K-k) and 1..k-1 (shifts K-k+1..K-1); together every term once
    shift_head = sp.Sum(th[k + s, j], (s, 0, K - k)).change_index(s, k + s, t)
    shift_tail = sp.Sum(th[k + s - K, j], (s, K - k + 1, K - 1)).change_index(s, k + s - K, t)
    # [L16.5] the average at every position is (1/K) sum_t th_tj, the mean of the terms
    out["average_gap"] = sp.simplify(
        (shift_head + shift_tail) / K - sp.Sum(th[t, j], (t, 1, K)) / K
    )
    Fth, Feq = sp.symbols("F_theta F_equal", real=True)  # F(W) and F(all terms equal)
    # [L16.6] I14, F convex: the slack J = (1/K) sum_s F(shift_s W) - F(average) is >= 0
    J = I14.slack_symbol("J")
    # [L16.7] by [L16.2]/[L16.3] each shifted value is F(W): the mean of K copies of F(W) is F(W)
    mean_of_shifts = sp.Sum(Fth / K, (s, 0, K - 1)).doit()
    # [L16.8] I14: F(all equal) = F(W) - J, with J >= 0
    out["equal_value"] = sp.solve(
        sp.Eq(I14.slack_expr(jen_f_of_mean=Feq, jen_mean_of_f=mean_of_shifts), J), Feq
    )[0]
    out["J"] = J
    out["Fth"] = Fth
    # [L16.9] exact instance: designs (1,0), (1,1/2), (0,1), (1/2,1), tau = kappa = 1, two terms
    out["instance"] = _instance()

    # ---------------------------------------------------------------- (ii) the bound
    # [L16.10] A1: the log-metrics are real, so the scores x_ik, x0_ik (current model) are real
    x, x0 = A1.real_base("x"), A1.real_base("x0")
    lsum = sp.Symbol("l", integer=True)
    Z0 = sp.Sum(sp.exp(kappa * x0[i, lsum]), (lsum, 1, K))
    al = sp.exp(kappa * x0[i, k]) / Z0  # alpha_ik = softmax_k(kappa x0_ik), positive
    # [L16.11] A6: kappa > 0; the weights sum to one
    out["alpha_sum"] = (
        sp.simplify(_rename(sp.Sum(al, (k, 1, K)).doit(), lsum, k) - 1)
        if A6.positive(kappa)
        else None
    )
    # Gibbs by Jensen: points y_k = exp(kappa x_ik)/alpha_ik, weights alpha_ik, convex f = -log
    y = sp.exp(kappa * x[i, k]) / al
    # [L16.12] the points y_k = exp(kappa x_ik)/alpha_ik have weighted mean sum_k exp(kappa x_ik)
    out["mean_y"] = sp.simplify(
        sp.Sum(al * y, (k, 1, K)).doit() - sp.Sum(sp.exp(kappa * x[i, k]), (k, 1, K))
    )
    f_mean = -sp.log(sp.Sum(sp.exp(kappa * x[i, k]), (k, 1, K)))  # f(sum alpha y), f = -log
    # [L16.13] A1, A6: the licensed logarithm of y_k = exp(kappa x_k)/alpha_k: the sum alpha f(y)
    mean_f = sp.Sum(al * -log_expand(sp.log(y), A1, A6), (k, 1, K))
    # [L16.14] I14 with f = -log: the row's Jensen slack sum_k alpha (-log y_k) + LSE
    gibbs_slack = I14.slack_expr(jen_f_of_mean=f_mean, jen_mean_of_f=mean_f)
    # [L16.15] A1, A6: the same slack with the logarithms expanded (each argument is positive)
    Jrow = log_expand(gibbs_slack, A1, A6)
    # [L16.16] A1, A6: the right side of Gibbs' inequality, with log alpha expanded
    gibbs_rhs = sp.log(sp.Sum(sp.exp(kappa * x[i, k]), (k, 1, K))) - sp.Sum(
        al * (kappa * x[i, k] - log_expand(sp.log(al), A1, A6)), (k, 1, K)
    )
    # [L16.17] Gibbs: log sum_k exp(kappa x) - sum_k alpha (kappa x - log alpha) = Jensen slack
    out["gibbs_gap"] = sp.simplify(Jrow - gibbs_rhs)
    # [L16.18] tightness: at x = x0 the same slack is 0 (log alpha = kappa x0 - log Z0)
    out["tight"] = sp.simplify(_rename(Jrow.subs(x, x0).doit(), lsum, k))
    # the soft model's slack of row i, and its bound by the alpha-weighted slack less H_i / kappa
    row_slack = -sp.log(sp.Sum(sp.exp(kappa * x[i, k]), (k, 1, K))) / kappa
    # [L16.19] A1, A6: H_i = -sum_k alpha_ik log alpha_ik, the entropy of the weights
    H_row = -sp.Sum(al * log_expand(sp.log(al), A1, A6), (k, 1, K))
    row_bound = sp.Sum(al * -x[i, k], (k, 1, K)) - H_row / kappa  # sum alpha s - H/kappa, s = -x
    # [L16.20] A6: kappa > 0; the bound minus the soft slack is (Jensen slack) / kappa
    out["bound_gap"] = sp.simplify(row_bound - row_slack - Jrow / A6.positive(kappa))
    # [L16.21] I14: the Jensen slacks Jf_i of the rows are nonnegative, so every row obeys the bound
    Jf = I14.nonneg_base("Jf")
    # [L16.22] A6: kappa > 0, so the mean over the rows of Jf_i / kappa is nonnegative
    out["rows_nonneg"] = sp.Sum(Jf[i] / (n * A6.positive(kappa)), (i, 1, n)).is_nonnegative
    out["x"], out["x0"], out["al"] = x, x0, al

    # regrouping the alpha-weighted mean slack by terms (cf. L14), alpha_ik = softmax_k(kappa x0_ik)
    beta, W = S.beta, sp.IndexedBase("W")
    u = S.u

    def alpha(a, b):
        z = sp.Symbol("l", integer=True)
        return sp.exp(kappa * x0[a, b]) / sp.Sum(sp.exp(kappa * x0[a, z]), (z, 1, K))

    mean_slack = (
        sp.Sum(
            sp.Sum(alpha(i, k) * (beta[k] - sp.Sum(W[k, j] * u[i, j], (j, 1, d))), (k, 1, K)),
            (i, 1, n),
        )
        / n
    )
    nk = sp.Sum(alpha(i, k), (i, 1, n))
    grouped = sp.Sum(
        (nk * beta[k] - sp.Sum(W[k, j] * sp.Sum(alpha(i, k) * u[i, j], (i, 1, n)), (j, 1, d))) / n,
        (k, 1, K),
    )
    # [L16.23] the mean over rows of the alpha-weighted slack is sum_k (n_k/N)(beta_k - ubar_k.w_k)
    out["regroup_gap"] = sp.expand(_canon(mean_slack) - _canon(grouped))

    # ---------------------------------------------------------------- (iii) the program
    # [L16.24] A2: the exponents w_kj are real (on the simplex), so x_kj = exp(w_kj) > 0
    wn = A2.nonneg_base("wn")
    ur = A1.real_base("ur")  # [L16.25] A1: the log-metrics u_ij are real
    # [L16.26] A1: the weighted mean log metrics ubar_kj are real
    ub = A1.real_base("ub")
    lim = (j, 1, d)
    nk_pos = sp.Sum(sp.exp(kappa * x0[i, k]) / Z0, (i, 1, n))
    # [L16.27] A3: the power n_k/(N tau) of the posynomial is positive (alpha > 0, tau > 0)
    power = nk_pos / (n * A3.positive(tau))
    out["power_positive"] = power.is_positive
    P_k = sp.Sum(sp.Product(sp.exp(wn[k, j]) ** (tau * ur[i, j]), lim), (i, 1, n)) / n
    # [L16.28] the posynomial P_k(x) = (1/N) sum_i prod_j x_kj^(tau u_ij): coefficient 1/N > 0
    out["posy"] = posynomial_term(1 / n, tau * ur[i, j], wn)
    # [L16.29] the monomial prod_j x_kj^(-ubar_kj n_k/N): coefficient 1, exponents real
    out["mono"] = posynomial_term(sp.Integer(1), -ub[k, j] * nk_pos / n, wn)
    Mono = sp.Product(sp.exp(wn[k, j]) ** (-ub[k, j] * nk_pos / n), lim)
    G_w = sp.Sum(
        (nk_pos / n) * (sp.log(P_k) / tau - sp.Sum(wn[k, j] * ub[k, j], lim)),
        (k, 1, K),
    )
    factor_k = P_k ** (nk_pos / (n * tau)) * Mono
    # [L16.30] A2 licenses the logarithms: log prod_k P_k^(n_k/(N tau)) * Mono_k = G_alpha(W)
    logged = sp.Sum(log_expand(sp.log(factor_k), A1, A2, A3, A6), (k, 1, K))
    out["log_gap"] = sp.simplify(logged - G_w)
    # [L16.31] I15: positive powers of posynomials times monomials, multiplied over the terms,
    # are a generalized posynomial
    out["generalized_posynomial"] = I15.entails(
        [
            sp.Equivalent(
                I15.obj("premise"),
                sp.true if out["posy"] and out["mono"] and out["power_positive"] else sp.false,
            )
        ],
        I15.obj("conclusion"),
    )
    ctx["L16"] = out
    return out


def _instance():
    """F(W), F(swapped W) and F(midpoint) for the designs (1,0), (1,1/2), (0,1), (1/2,1)."""
    R = sp.Rational
    U = [(1, 0), (1, R(1, 2)), (0, 1), (R(1, 2), 1)]
    tau = kappa = 1

    def beta(w):
        return sp.log(sum(sp.exp(tau * (w[0] * a + w[1] * b)) for a, b in U) / len(U)) / tau

    def F(W):
        bet = [beta(w) for w in W]
        rows = [
            sp.log(
                sum(
                    sp.exp(kappa * (w[0] * a + w[1] * b - bk)) for w, bk in zip(W, bet, strict=True)
                )
            )
            / kappa
            for a, b in U
        ]
        return -sum(rows) / len(U)

    W = [(1, 0), (0, 1)]
    swapped = [(0, 1), (1, 0)]
    mid = [(R(1, 2), R(1, 2))] * 2
    return {
        "F": sp.N(F(W), 40),
        "F_swapped": sp.N(F(swapped), 40),
        "F_mid": sp.N(F(mid), 40),
    }


def verify(ctx):
    r = ctx["L16"]
    # [L16.32] the shifted and unshifted sums over the terms agree for every row
    assert r["shift_gap"] == 0, "L16 FAIL: the shifted sum over the terms differs from the sum"
    # [L16.33] F, a function of the sums T_i, is unchanged by a cyclic shift of the terms
    assert r["F_shift_gap"] == 0, "L16 FAIL: F changes under a cyclic shift of the terms"
    # [L16.34] the average of the K cyclic shifts has the mean of the terms at every position
    assert r["average_gap"] == 0, "L16 FAIL: the shift average is not the mean at every position"
    # [L16.35] F(all terms equal) = F(W) - J, so F(all equal) <= F(W) for a convex symmetric F
    assert (
        sp.simplify(r["equal_value"] - (r["Fth"] - r["J"])) == 0
        and (r["Fth"] - r["equal_value"]).is_nonnegative is True
    ), "L16 FAIL: the all-equal point is not F(W) - J with J >= 0"
    ins = r["instance"]
    # [L16.36] exact instance: F is unchanged by swapping the two terms
    assert abs(ins["F"] - ins["F_swapped"]) < sp.Float("1e-30"), "L16 FAIL: F(swapped) != F(W)"
    # [L16.37] exact instance: F at the midpoint (all terms equal) exceeds F(W), so F is not convex
    assert ins["F_mid"] - ins["F"] > sp.Float("0.004"), (
        "L16 FAIL: the midpoint does not exceed F(W)"
    )
    # [L16.38] the weights alpha_ik sum to one over the terms
    assert r["alpha_sum"] == 0, "L16 FAIL: the weights do not sum to one"
    # [L16.39] the weighted mean of the points y_k is sum_k exp(kappa x_ik)
    assert r["mean_y"] == 0, "L16 FAIL: sum_k alpha y_k != sum_k exp(kappa x_k)"
    # [L16.40] Gibbs: the I14 slack equals log sum exp - sum alpha (kappa x - log alpha)
    assert r["gibbs_gap"] == 0, "L16 FAIL: Gibbs' slack is not the Jensen slack"
    # [L16.41] at the weights' own model the Jensen slack is 0: the bound is tight there
    assert r["tight"] == 0, "L16 FAIL: the bound is not tight at the weights' own model"
    # [L16.42] the bound minus the soft slack of row i is (Jensen slack) / kappa
    assert r["bound_gap"] == 0, (
        "L16 FAIL: the bound minus the soft slack is not Jensen slack / kappa"
    )
    # [L16.43] the mean of the nonnegative Jensen slacks is nonnegative: F <= G_alpha - E
    assert r["rows_nonneg"] is True, (
        "L16 FAIL: the soft slack is not bounded by the fixed-weight objective"
    )
    # [L16.44] the alpha-weighted mean slack regroups by terms
    assert r["regroup_gap"] == 0, "L16 FAIL: the weighted mean slack does not regroup by terms"
    # [L16.45] the posynomial P_k has positive coefficient and real exponents independent of x
    assert r["posy"], "L16 FAIL: P_k is not a posynomial in x = exp(w)"
    # [L16.46] the monomial factor has coefficient 1 and real exponents
    assert r["mono"], "L16 FAIL: the weighted mean term is not a monomial in x"
    # [L16.47] the power n_k/(N tau) is positive
    assert r["power_positive"] is True, "L16 FAIL: the power of P_k is not positive"
    # [L16.48] the logarithm of the product over terms is the fixed-weight objective
    assert r["log_gap"] == 0, "L16 FAIL: log of the product is not G_alpha"
    # [L16.49] the product over the terms is a generalized posynomial (I15's premise held at L16.31)
    assert r["generalized_posynomial"], "L16 FAIL: not a generalized posynomial"

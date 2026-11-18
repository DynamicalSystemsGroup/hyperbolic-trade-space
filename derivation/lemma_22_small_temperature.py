"""L22: the small-temperature expansion of the log-mean-exp; on centred metrics, the variance.

Setting (symbolic d, n). Scores s_i = w.u_i for rows i = 1..n, tau > 0 (A3), the log-mean-exp
LME(tau) = (1/tau) log((1/n) Sum_i exp(tau s_i)) (the soft maximum beta of the fit; L5).

What this proves (symbolic d, n):
  1. N(tau) = log((1/n) Sum_i exp(tau s_i)) has N(0) = 0 and the derivatives at zero N'(0) = mean,
     N''(0) = (1/n) Sum_i (s_i - mean)^2 (the variance of the scores over the rows, the second
     cumulant) and N'''(0) = (1/n) Sum_i (s_i - mean)^3 (the third central moment). So the Taylor
     polynomial of LME(tau) = N(tau)/tau at tau = 0 is mean + (tau/2) variance + (tau^2/6) mu_3.
  2. When the log-metrics are centred, Sum_i u_ij = 0 for every metric j (the standardising
     conditioning of the case), the mean of the scores is zero for every w, so
     LME(tau) = (tau/2) w'Cw + (tau^2/6) mu_3 + ..., with C_jl = (1/n) Sum_i u_ij u_il the second
     moment of the log-metrics: the first term of the objective that depends on w is the
     variance of the score, a quadratic form on the exponents.
  3. The variance is nonnegative (a mean of squares of real scores), so C is positive
     semidefinite as a quadratic form, and the minimum over the simplex of the leading term is
     the minimum-variance combination of the metrics.

What this does NOT prove: that the remainder is bounded uniformly in w on the simplex (a bound
needs the range of the scores and is not scripted here), so it does not prove that the minimizers
of the fit tend to the minimizers of w'Cw as tau tends to zero; that the minimum-variance
combination is unique (C may be singular); anything for tau not small: the neglected term mu_3
is the size of the skew of the scores, and the check of the fit at tau = 3 against the
minimum-variance combination is a number on the data of record (WP46-rounds), not a step here.

Route: SymPy differentiation through the Sum with symbolic n (as L5) for the cumulants at zero;
linearity of finite sums; the centring hypothesis as a rewrite rule on the sum of a column;
Fubini for the quadratic form.
"""

import sympy as sp

from derivation.axioms import A1, A3
from derivation.sumtools import fuse, linear, pull_constants, push_in, replace_indexed

TITLE = "Small-temperature expansion of the log-mean-exp; the variance on centred metrics"
STATEMENT = (
    "For scores s_i = w.u_i over n rows and tau > 0: N(tau) = log((1/n) Sum_i exp(tau s_i)) has "
    "N(0) = 0, N'(0) = mean, N''(0) = variance, N'''(0) = third central moment, so "
    "the log-mean-exp N(tau)/tau has the Taylor polynomial mean + (tau/2) variance + (tau^2/6) "
    "mu_3 at zero. On "
    "centred log-metrics (Sum_i u_ij = 0) the mean is zero and the variance is the quadratic form "
    "w'Cw with C_jl = (1/n) Sum_i u_ij u_il, nonnegative for real scores. The neglected term and "
    "the uniformity of the remainder on the simplex are not bounded here"
)
AXIOMS_USED = ["A1", "A3"]


def derive(ctx):
    S = ctx["S"]
    i, j, n, d, w = S.i, S.j, S.n, S.d, S.w
    # [L22.1] A3: the temperature tau is positive
    tau = A3.positive(S.tau)
    # [L22.2] A1: the log-metrics are real
    u = A1.real_base("u")
    # [L22.3] A1: the scores s_i = w.u_i of real log-metrics are real
    s = A1.real_base("s")
    lim = (i, 1, n)
    mean = sp.Sum(s[i], lim) / n

    N = sp.log(sp.Sum(sp.exp(tau * s[i]), lim) / n)
    # [L22.4] N(0) = log((1/n) n) = 0
    N0 = sp.simplify(N.subs(tau, 0).doit())
    # [L22.5] the first derivative of N at zero (differentiating the Sum termwise)
    N1 = sp.simplify(sp.diff(N, tau).subs(tau, 0).doit())
    # [L22.6] the second derivative of N at zero
    N2 = sp.simplify(sp.diff(N, tau, 2).subs(tau, 0).doit())
    # [L22.7] the third derivative of N at zero
    N3 = sp.simplify(sp.diff(N, tau, 3).subs(tau, 0).doit())
    var = sp.Sum((s[i] - mean) ** 2, lim) / n
    mu3 = sp.Sum((s[i] - mean) ** 3, lim) / n
    # [L22.8] the variance expanded by linearity of the finite sum: (1/n) Sum s^2 - mean^2
    var_moment = linear(sp.Sum(sp.expand((s[i] - mean) ** 2), lim) / n)
    # [L22.9] the third central moment expanded by linearity
    mu3_moment = linear(sp.Sum(sp.expand((s[i] - mean) ** 3), lim) / n)

    # centred log-metrics: the column sums vanish (hypothesis), the scores are s_i = w.u_i
    ell = sp.Symbol("l", integer=True)
    row = sp.Sum(w[j] * u[i, j], (j, 1, d))  # the score of row i
    # [L22.10] the mean score is Sum_j w_j (Sum_i u_ij) / n: the order of the two finite sums swaps
    rows_first = fuse(sp.Sum(row, lim)).reorder((0, 1))
    mean_score = pull_constants(rows_first) / n
    column = sp.Sum(u[i, j], lim)
    # [L22.11] the centring hypothesis: every column sum Sum_i u_ij is zero
    centred = mean_score.replace(lambda x: x == column, lambda x: sp.Integer(0)).doit()
    # [L22.12] the variance of the row scores: the score family replaced by the row score, and the
    # mean score replaced by zero (L22.10)
    mean_rows = replace_indexed(mean, s, lambda k: row.subs(i, k))
    var_centred = replace_indexed(var_moment, s, lambda k: row.subs(i, k)).subs(mean_rows, 0)
    # [L22.13] the squared score as a double sum over j and l: the factor free of the summed
    # index goes inside the sum, first over j and then over l
    other = sp.Symbol("other")
    other_row = sp.Sum(
        row.function.subs(j, ell), (ell, 1, d)
    )  # the square of the sum is its product with a renamed copy
    inside_j = push_in(row * other).subs(other, other_row)
    score_sq = push_in(inside_j)
    # [L22.14] the second moment of the scores over the rows, the sum over the rows innermost
    second = pull_constants(sp.Sum(score_sq.function, lim, (ell, 1, d), (j, 1, d)))
    # [L22.15] the mean of squares of real scores is nonnegative (n > 0)
    nonneg = (sp.Sum(s[i] ** 2, lim) / n).is_nonnegative

    ctx["L22"] = {
        "tau": tau,
        "s": s,
        "u": u,
        "mean": mean,
        "var": var,
        "mu3": mu3,
        "N0": N0,
        "N1": N1,
        "N2": N2,
        "N3": N3,
        "var_moment": var_moment,
        "mu3_moment": mu3_moment,
        "mean_score": mean_score,
        "centred": centred,
        "score_sq": score_sq,
        "second": second,
        "ell": ell,
        "row": row,
        "other_row": other_row,
        "var_centred": var_centred,
        "nonneg": nonneg,
        "lim": lim,
    }


def verify(ctx):
    S = ctx["S"]
    r = ctx["L22"]
    i, j, n, d, w = S.i, S.j, S.n, S.d, S.w
    s, u, mean, ell, lim = r["s"], r["u"], r["mean"], r["ell"], r["lim"]
    # [L22.16] N(0) = 0, so LME = N(tau)/tau has the Taylor coefficients of N shifted by one
    assert r["N0"] == 0, "L22 FAIL: N(0) != 0"
    # [L22.17] N'(0) is the mean of the scores: lim_{tau->0} LME = mean (L5.22)
    assert sp.simplify(r["N1"] - mean) == 0, "L22 FAIL: N'(0) != mean"
    # [L22.18] N''(0) is the variance of the scores, (1/n) Sum (s_i - mean)^2
    assert sp.simplify(r["N2"] - r["var_moment"]) == 0, "L22 FAIL: N''(0) != variance"
    # [L22.19] the variance is the mean of squares minus the squared mean
    assert sp.simplify(r["var_moment"] - (sp.Sum(s[i] ** 2, lim) / n - mean**2)) == 0, (
        "L22 FAIL: variance != mean of squares - mean^2"
    )
    # [L22.20] N'''(0) is the third central moment, (1/n) Sum (s_i - mean)^3
    assert sp.simplify(r["N3"] - r["mu3_moment"]) == 0, "L22 FAIL: N'''(0) != third central moment"
    # [L22.21] the centring hypothesis gives a zero mean score for every exponent vector
    assert r["centred"] == 0, "L22 FAIL: the mean score is not zero on centred metrics"
    # [L22.22] on centred metrics the variance of the scores is (1/n) Sum_i (row score)^2
    assert sp.simplify(r["var_centred"] - sp.Sum(r["row"] ** 2, lim) / n) == 0, (
        "L22 FAIL: the centred variance is not the mean of squared row scores"
    )
    # [L22.23] renaming the bound index j to l and back returns the row score: the copy is faithful
    assert sp.Sum(r["other_row"].function.subs(ell, j), (j, 1, d)) == r["row"], (
        "L22 FAIL: the renamed copy differs"
    )
    # [L22.24] the squared score is the double sum over j and l of w_j w_l u_ij u_il, one row
    assert r["score_sq"].function == w[j] * w[ell] * u[i, j] * u[i, ell] and set(
        r["score_sq"].limits
    ) == {(j, 1, d), (ell, 1, d)}, "L22 FAIL: the squared score is not the double sum"
    quad = sp.Sum(w[j] * w[ell] * sp.Sum(u[i, j] * u[i, ell], lim), (ell, 1, d), (j, 1, d))
    # [L22.25] summed over the rows the squares make n w'Cw, Sum_jl w_j w_l (Sum_i u_ij u_il), C_jl
    # the mean of the products (Fubini for finite sums: the same summand over the same ranges)
    assert r["second"] == quad, "L22 FAIL: the second moment of the scores is not w'Cw"
    # [L22.26] a square of a real score is nonnegative, so the variance is nonnegative
    assert r["nonneg"] is True, "L22 FAIL: a squared real score is not nonnegative"

"""L14 (Proposition 3 and the approximate-certificate corollary) - assignment-stable local
optimality, step B.

Setting.  K terms with exponents w_k on the simplex, cells C_1..C_K a partition of the N rows,
n_k = |C_k|, reaches beta_k = J_tau(U w_k), mean slack
F(W) = (1/N) sum_i (beta_k(i) - w_k(i).u_i) for the unpenalized step-B objective.  f_k(w) =
J_tau(U w) - ubar_k.w (ubar_k the mean of the rows of C_k) is the term refit of L12.

What this proves (symbolic d, n_k, K; plain SymPy):
  1. Per-term regrouping: sum_{i in C_k} (beta_k - w_k.u_i) = n_k (beta_k - w_k.ubar_k), at
     symbolic n_k (the cell's rows listed 1..n_k).  Sum linearity leaves a double sum that
     equals its mirror by a Fubini swap (L3's ``sum_swap_equal``).  Since beta_k = J_tau(U w_k),
     beta_k - w_k.ubar_k = f_k(w_k).
  2. The regrouping of the N-row sum over the K cells, sum_i = sum_k sum_{i in C_k}: the partition
     is the declared relation A8 (a membership family chi_ki with sum_k chi_ki = 1, n_k = sum_i
     chi_ki >= 1), applied by import; the swap of the row and cell sums is Fubini (L3's
     ``sum_swap_equal``) and the cell sum is n_k f_k(w_k).  With share_k = n_k/N it gives
     F(W) = sum_k share_k f_k(w_k), and beta_k = J_tau(U w_k) is the reach itself.
  3. The full objective (1/N) sum_i min_k (beta_k - w_k.u_i) equals the fixed-assignment
     expression on the assignment-stable neighborhood: R2 (positive margin) and L13 keep k(i)
     the unique maximizing term of every row, so the max score of row i is its score on k(i)
     and the termwise difference vanishes.
  4. Proposition 3.  Hypotheses (ledger): R2 positive margin; every cell nonempty (n_k >= 1, so
     share_k >= 0 and ubar_k is defined); every w_k minimizes f_k over the simplex (exact term
     optima, so f_k(w'_k) - f_k(w_k) >= 0); beta_k = J_tau(U w_k) (step B, unpenalized).  Then
     F(W') - F(W) = sum_k share_k (f_k(w'_k) - f_k(w_k)) is a sum of nonnegative terms: a local
     minimizer on the neighborhood.
  5. The approximate-certificate corollary.  F(W) - F*_fixed = sum_k share_k (f_k(w_k) - f_k*)
     (the fixed-assignment objective is separable, so its minimum is the sum of the term
     minima), and L12 gives f_k(w_k) - f_k* <= G_k termwise, so
     F(W) - F*_fixed <= sum_k share_k G_k: a sum of nonnegative terms share_k (G_k - (f_k - f_k*)).

What this does NOT prove: global optimality or global convergence of the several-term problem; any
statement for the tangent refit (step D), the sparsity penalty or a freely varying beta_k, where
hypothesis beta_k = J_tau(U w_k) or exact term optimality fails; that R2 holds for a given fit
(a ridge row or duplicate terms make it fail).
"""

import sympy as sp

from derivation.axioms import A8, R2
from derivation.lemma_12_term_gap import L12_RESULT
from derivation.lemma_13_margin import L13_RESULT
from derivation.licence import hypothesis_base
from derivation.results import ProvedResult
from derivation.sumtools import fuse, linear, push_in, sum_swap_equal

TITLE = (
    "assignment-stable local optimality of the several-term fit "
    "(Proposition 3, approximate-certificate corollary)"
)
STATEMENT = (
    "Level 3 is for step B, unpenalized, with reaches beta_k = J_tau(U w_k) only. "
    "Per term, sum_{i in C_k} (beta_k - w_k.u_i) = n_k (beta_k - w_k.ubar_k) = n_k f_k(w_k), "
    "n_k = |C_k|, so "
    "the mean slack is F(W) = sum_k (n_k/N) f_k(w_k). Proposition 3: if the margin is positive "
    "(R2), every cell is nonempty and every w_k minimizes f_k, then on the assignment-stable "
    "neighborhood of the fitted reference surface (finite tau, Phi = 0, V > 1 possible; or the "
    "tau = inf supporting envelope) F(W') - F(W) = sum_k (n_k/N) (f_k(w'_k) - f_k(w_k)) >= 0, a "
    "local minimizer. The approximate-certificate corollary: F(W) - F*_fixed <= "
    "sum_k (n_k/N) G_k with G_k the term gaps of L12 (nonnegative sums)"
)
AXIOMS_USED = ["A8", "R2"]
L14_RESULT = ProvedResult("L14", STATEMENT)  # taken by L15
# Two results share this file (the step tags run in one sequence; each step is owned by one result).
# Hypotheses of the statement (each quotes it): the symbols that carry a sign stand for these.
EXACT_TERM_OPTIMUM = hypothesis_base("dfk", "nonnegative", "every w_k minimizes f_k")
PROOF_RESULTS = (
    ("Proposition 3", (1, 2, 3, 4, 5, 6, 7, 9, 11, 12, 13, 14, 15, 16, 17, 18)),
    ("Approximate-certificate corollary", (8, 10, 19, 20)),
)


def _is_fubini_residual(leftover):
    """True iff ``leftover`` is exactly two double sums that are each other's mirror (Fubini)."""
    dbl = [t for t in sp.Add.make_args(leftover) if t.has(sp.Sum)]
    pos = [t for t in dbl if not t.could_extract_minus_sign()]
    neg = [-t for t in dbl if t.could_extract_minus_sign()]
    return (
        len(dbl) == len(sp.Add.make_args(leftover))
        and len(pos) == 1
        and len(neg) == 1
        and sum_swap_equal(fuse(push_in(pos[0])), fuse(push_in(neg[0])))
    )


def derive(ctx):
    S = ctx["S"]
    d, i, j, k, K = S.d, S.i, S.j, S.k, S.K
    u = S.u
    w = S.w
    lim = (j, 1, d)

    # 1. per-term regrouping at symbolic cell size n_k
    nk = S.n  # the cell size, a symbolic positive integer (A0)
    beta = sp.Symbol("beta_k", real=True)

    def dot(x):
        return sp.Sum(w[j] * u[x, j], lim)

    total = sp.Sum(beta - dot(i), (i, 1, nk))
    claim = nk * (beta - sp.Sum(w[j] * sp.Sum(u[i, j], (i, 1, nk)) / nk, lim))
    leftover = sp.simplify(linear(total) - linear(sp.expand(claim)))
    regroup_swap_equal = _is_fubini_residual(leftover)

    # 2. the regrouping of the N rows over the K cells, from the declared partition relation A8
    # [L14.1] A8: the membership family chi_ki, the cell counts n_k and the number N of rows
    chi, ncell, N = A8.obj("membership"), A8.obj("count"), A8.obj("rows")
    h = sp.IndexedBase("h")  # a quantity of row i, free of the cell
    by_rows = sp.Sum(h[i] * sp.Sum(chi[k, i], (k, 1, K)), (i, 1, N))
    # [L14.2] A8: every row lies in one cell, sum_k chi_ki = 1, so the row sum is unchanged
    rows_to_cells = (
        sp.simplify(A8.rewrite(by_rows, only=(0,)) - sp.Sum(h[i], (i, 1, N))),
        len(fuse(push_in(by_rows)).limits),
    )
    gc = sp.IndexedBase("gc")  # gc[k, i]: the slack of row i on term k
    row_major = sp.Sum(sp.Sum(chi[k, i] * gc[k, i], (k, 1, K)), (i, 1, N))
    cell_major = sp.Sum(sp.Sum(chi[k, i] * gc[k, i], (i, 1, N)), (k, 1, K))
    # [L14.3] the sum over rows of the slack on the row's own cell is the sum over the cells
    cells_swap_equal = sum_swap_equal(fuse(push_in(row_major)), fuse(push_in(cell_major)))
    Jk, Wk = sp.IndexedBase("Jk"), sp.IndexedBase("Wk")  # Jk[k] = beta_k = J_tau(U w_k)
    cell_sum = sp.Sum(chi[k, i] * (Jk[k] - sp.Sum(Wk[k, j] * u[i, j], lim)), (i, 1, N))
    # [L14.4] A8: n_k = sum_i chi_ki, so the cell sum is n_k (beta_k - w_k.ubar_k) = n_k f_k(w_k)
    n_k = A8.rewrite(ncell[k], only=(2,))
    f_k = Jk[k] - sp.Sum(Wk[k, j] * sp.Sum(chi[k, i] * u[i, j], (i, 1, N)) / n_k, lim)
    cell_leftover = sp.simplify(linear(cell_sum) - linear(sp.expand(n_k * f_k)))
    cell_regroup_ok = _is_fubini_residual(cell_leftover)
    # [L14.5] A8: F(W) = (1/N) sum_k n_k f_k(w_k) = sum_k share_k f_k(w_k) with share_k = n_k / N
    shares = A8.rewrite(ncell[k] / N, only=(2,))
    F_regroup = sp.simplify(sp.Sum(n_k * f_k, (k, 1, K)) / N - sp.Sum(shares * f_k, (k, 1, K)))

    # 2-3. the objective on the neighborhood: scores s_fixed[i] on k(i), max score M[i]
    sfix = sp.IndexedBase("sfix")
    Mx = sp.IndexedBase("Mx")
    # [L14.6] R2: the margin is positive, so row i's maximum score M_i is its score s_i,k(i)
    agree = R2.rewrite(sp.Sum(sfix[i] - Mx[i], (i, 1, N)))
    objective_agrees = sp.simplify(agree.doit())

    # 4. local minimality: F(W') - F(W) = sum_k share_k (f_k(w'_k) - f_k(w_k)), terms >= 0
    # [L14.7] A8: share_x = n_x / N = sum_i chi_xi / N, nonnegative because chi >= 0
    share = lambda x: A8.rewrite(ncell[x] / N, only=(2,))  # noqa: E731

    fold = sp.IndexedBase("fold")
    dfk = EXACT_TERM_OPTIMUM  # f_k(w'_k) = f_k(w_k) + dfk_k, dfk_k >= 0 (exact optimum)
    local_min_slack = sp.simplify(
        linear(
            sp.Sum(share(k) * (fold[k] + dfk[k]), (k, 1, K)) - sp.Sum(share(k) * fold[k], (k, 1, K))
        )
        - linear(sp.Sum(share(k) * dfk[k], (k, 1, K)))
    )
    local_min_nonneg = sp.Sum(share(k) * dfk[k], (k, 1, K)).is_nonnegative

    # 5. The approximate-certificate corollary: F - F* = sum share (f - f*), bounded termwise
    # by sum share G
    fk = sp.IndexedBase("fk")
    fstar = sp.IndexedBase("fstar")
    # [L14.8] by L12: G_k - (f_k - f_k*) >= 0, so G_k = (f_k - f_k*) + slackG_k with slackG_k >= 0
    slackG = L12_RESULT.family(ctx, "chain_nonneg", "slackG")
    cor_slack = sp.simplify(
        linear(sp.Sum(share(k) * ((fk[k] - fstar[k]) + slackG[k]), (k, 1, K)))
        - linear(sp.Sum(share(k) * (fk[k] - fstar[k]), (k, 1, K)))
        - linear(sp.Sum(share(k) * slackG[k], (k, 1, K)))
    )
    cor_nonneg = sp.Sum(share(k) * slackG[k], (k, 1, K)).is_nonnegative

    ctx["L14"] = dict(
        nk=nk,
        regroup_leftover=leftover,
        regroup_swap_equal=regroup_swap_equal,
        objective_agrees=objective_agrees,
        rows_to_cells=rows_to_cells,
        cells_swap_equal=cells_swap_equal,
        cell_regroup_ok=cell_regroup_ok,
        F_regroup=F_regroup,
        partition_identity=bool(F_regroup == 0 and cell_regroup_ok is True),
        local_min_slack=local_min_slack,
        local_min_nonneg=local_min_nonneg,
        cor_slack=cor_slack,
        cor_nonneg=cor_nonneg,
    )


def verify(ctx):
    r = ctx["L14"]
    # hypotheses carried from the earlier lemmas
    # [L14.9] by L13 (under R2): the margin is positive, so an assignment-stable neighborhood exists
    assert L13_RESULT.holds(ctx, "margin_positive"), (
        "L14 FAIL: no assignment-stable neighborhood (R2 positive margin, L13)"
    )
    # [L14.10] by L12 (Lemma 1): 0 <= f_k(w_k) - f_k* <= G_k for every term
    assert L12_RESULT.holds(ctx, "chain_nonneg") and L12_RESULT.holds(ctx, "lower_nonneg"), (
        "L14 FAIL: Lemma 1 (0 <= f - f* <= G) not established"
    )
    # [L14.11] per term, sum_i (beta_k - w_k.u_i) = n_k (beta_k - w_k.ubar_k) by a Fubini swap
    assert r["regroup_swap_equal"] is True, (
        "L14 FAIL: per-term regrouping is not a Fubini swap of the double sum"
    )
    # [L14.12] A8: every row lies in one cell (sum_k chi_ki = 1): the row sum is unchanged
    assert r["rows_to_cells"] == (0, 2), "L14 FAIL: the rows are not partitioned over the cells"
    # [L14.13] the sum over rows of the slack on the row's own cell is the sum over the cells
    assert r["cells_swap_equal"] is True, "L14 FAIL: sum_i sum_k != sum_k sum_i (Fubini)"
    # [L14.14] A8: with n_k = sum_i chi_ki the cell sum is n_k (beta_k - w_k.ubar_k) = n_k f_k(w_k)
    assert r["cell_regroup_ok"] is True, "L14 FAIL: the cell sum is not n_k f_k(w_k)"
    # [L14.15] A8: F(W) = (1/N) sum_k n_k f_k(w_k) = sum_k share_k f_k(w_k), share_k = n_k / N
    assert r["F_regroup"] == 0, "L14 FAIL: F(W) != sum_k share_k f_k(w_k)"
    # [L14.16] on the neighborhood the full objective equals the fixed-assignment expression
    assert r["objective_agrees"] == 0, (
        "L14 FAIL: full objective differs from the fixed-assignment expression"
    )
    # [L14.17] F(W') - F(W) = sum_k share_k (f_k(w'_k) - f_k(w_k))
    assert sp.simplify(r["local_min_slack"]) == 0, (
        "L14 FAIL: F(W') - F(W) != sum_k share_k (f_k(w'_k) - f_k(w_k))"
    )
    # [L14.18] each term share_k (f_k' - f_k) is >= 0 (exact term optima), so W is a local minimum
    assert r["local_min_nonneg"] is True, "L14 FAIL: sum_k share_k (f_k' - f_k) is not nonnegative"
    # [L14.19] sum share G - sum share (f - f*) = sum share (G - (f - f*))
    assert sp.simplify(r["cor_slack"]) == 0, (
        "L14 FAIL: sum share G - sum share (f - f*) != sum share (G - (f - f*))"
    )
    # [L14.20] each term share_k (G_k - (f_k - f_k*)) is >= 0 (L12): F(W) - F*_fixed <= sum share G
    assert r["cor_nonneg"] is True, "L14 FAIL: sum_k share_k (G_k - (f_k - f_k*)) not nonnegative"
    L14_RESULT.certify(ctx)

"""L14 (Proposition 3 and Corollary 4) - assignment-stable local optimality, step B.

Setting.  K facets with exponents w_k on the simplex, cells C_1..C_K a partition of the N rows,
n_k = |C_k|, offsets beta_k = J_tau(U w_k) (the support offset), mean slack
F(W) = (1/N) sum_i (beta_k(i) - w_k(i).u_i) for the unpenalized step-B objective.  f_k(w) =
J_tau(U w) - ubar_k.w (ubar_k the mean of the rows of C_k) is the facet refit of L12.

What this proves (symbolic d, n_k, K; plain SymPy):
  1. Per-facet regrouping: sum_{i in C_k} (beta_k - w_k.u_i) = n_k (beta_k - w_k.ubar_k), at
     symbolic n_k (the cell's rows listed 1..n_k).  Sum linearity leaves a double sum that
     equals its mirror by a Fubini swap (L3's ``sum_swap_equal``).  Since beta_k = J_tau(U w_k),
     beta_k - w_k.ubar_k = f_k(w_k).
  2. The regrouping of the N-row sum over the K cells, sum_i = sum_k sum_{i in C_k}, is a
     one-line finite-sum argument (every row lies in exactly one cell). SymPy has no
     symbolic partition object, so this step is stated, not derived, and it needs no ledger
     entry. With share_k = n_k/N it gives F(W) = sum_k share_k f_k(w_k).
  3. The full objective (1/N) sum_i min_k (beta_k - w_k.u_i) equals the fixed-assignment
     expression on the assignment-stable neighborhood: R2 (positive margin) and L13 keep k(i)
     the unique maximizing facet of every row, so the max score of row i is its score on k(i)
     and the termwise difference vanishes.
  4. Proposition 3.  Hypotheses (ledger): R2 positive margin; every facet nonempty (n_k >= 1, so
     share_k >= 0 and ubar_k is defined); every w_k minimizes f_k over the simplex (exact facet
     optima, so f_k(w'_k) - f_k(w_k) >= 0); beta_k = J_tau(U w_k) (step B, unpenalized).  Then
     F(W') - F(W) = sum_k share_k (f_k(w'_k) - f_k(w_k)) is a sum of nonnegative terms: a local
     minimizer on the neighborhood.
  5. Corollary 4.  F(W) - F*_fixed = sum_k share_k (f_k(w_k) - f_k*) (the fixed-assignment
     objective is separable, so its minimum is the sum of the facet minima), and L12 gives
     f_k(w_k) - f_k* <= G_k termwise, so F(W) - F*_fixed <= sum_k share_k G_k: a sum of
     nonnegative terms share_k (G_k - (f_k - f_k*)).

What this does NOT prove: global optimality or global convergence of the multi-facet problem; any
statement for the tangent refit (step D), the sparsity penalty or freely varying offsets, where
hypothesis beta_k = J_tau(U w_k) or exact facet optimality fails; that R2 holds for a given fit
(a ridge row or duplicate facets make it fail).
"""

import sympy as sp

from derivation.lemma_03_gradient_kkt import fuse, push_in, replace_indexed, sum_swap_equal
from derivation.sumtools import linear

TITLE = "assignment-stable local optimality of the multi-facet fit (Proposition 3, Corollary 4)"
STATEMENT = (
    "Level 3 is for step B, unpenalized, with support offsets beta_k = J_tau(U w_k) only. "
    "Per facet, sum_{i in C_k} (beta_k - w_k.u_i) = n_k (beta_k - w_k.ubar_k) = n_k f_k(w_k), "
    "n_k = |C_k|, so "
    "the mean slack is F(W) = sum_k (n_k/N) f_k(w_k). Proposition 3: if the margin is positive "
    "(R2), every facet is nonempty and every w_k minimizes f_k, then on the assignment-stable "
    "neighborhood of the fitted reference surface (finite tau, Phi = 0, V > 1 possible; or the "
    "tau = inf supporting envelope) F(W') - F(W) = sum_k (n_k/N) (f_k(w'_k) - f_k(w_k)) >= 0, a "
    "local minimizer. Corollary 4: F(W) - F*_fixed <= sum_k (n_k/N) G_k with G_k the facet gaps "
    "of L12 (nonnegative sums)"
)
AXIOMS_USED = ["A2", "R2"]


def derive(ctx):
    S = ctx["S"]
    d, i, j, k, K = S.d, S.i, S.j, S.k, S.K
    w, u = S.w, S.u
    lim = (j, 1, d)

    # 1. per-facet regrouping at symbolic cell size n_k
    nk = sp.Symbol("n_k", integer=True, positive=True)
    beta = sp.Symbol("beta_k", real=True)

    def dot(x):
        return sp.Sum(w[j] * u[x, j], lim)

    total = sp.Sum(beta - dot(i), (i, 1, nk))
    claim = nk * (beta - sp.Sum(w[j] * sp.Sum(u[i, j], (i, 1, nk)) / nk, lim))
    leftover = sp.simplify(linear(total) - linear(sp.expand(claim)))
    dbl = [t for t in sp.Add.make_args(leftover) if t.has(sp.Sum)]
    pos = [t for t in dbl if not t.could_extract_minus_sign()]
    neg = [-t for t in dbl if t.could_extract_minus_sign()]
    regroup_swap_equal = (
        len(pos) == 1
        and len(neg) == 1
        and sum_swap_equal(fuse(push_in(pos[0])), fuse(push_in(neg[0])))
    )

    # 2-3. the objective on the neighborhood: scores s_fixed[i] on k(i), max score M[i]
    sfix = sp.IndexedBase("sfix")
    Mx = sp.IndexedBase("Mx")
    N = sp.Symbol("N", integer=True, positive=True)
    agree = replace_indexed(
        sp.Sum(sfix[i] - Mx[i], (i, 1, N)), Mx, lambda x: sfix[x]
    )  # M_i = s_ik(i)
    objective_agrees = sp.simplify(agree.doit())

    # 4. local minimality: F(W') - F(W) = sum_k share_k (f_k(w'_k) - f_k(w_k)), terms >= 0
    share = sp.IndexedBase("share", nonnegative=True)  # n_k / N, n_k >= 1
    fnew = sp.IndexedBase("fnew")
    fold = sp.IndexedBase("fold")
    dfk = sp.IndexedBase("dfk", nonnegative=True)  # f_k(w'_k) - f_k(w_k) >= 0 (exact optimum)
    local_min_slack = sp.simplify(
        linear(sp.Sum(share[k] * fnew[k], (k, 1, K)) - sp.Sum(share[k] * fold[k], (k, 1, K)))
        - linear(sp.Sum(share[k] * (fnew[k] - fold[k]), (k, 1, K)))
    )
    local_min_nonneg = sp.Sum(share[k] * dfk[k], (k, 1, K)).is_nonnegative

    # 5. Corollary 4: F - F* = sum share (f - f*), bound by sum share G termwise
    fk = sp.IndexedBase("fk")
    fstar = sp.IndexedBase("fstar")
    Gk = sp.IndexedBase("Gk")
    slackG = sp.IndexedBase("slackG", nonnegative=True)  # G_k - (f_k - f_k*) >= 0 (L12)
    cor_slack = sp.simplify(
        linear(sp.Sum(share[k] * Gk[k], (k, 1, K)))
        - linear(sp.Sum(share[k] * (fk[k] - fstar[k]), (k, 1, K)))
        - linear(sp.Sum(share[k] * (Gk[k] - (fk[k] - fstar[k])), (k, 1, K)))
    )
    cor_nonneg = sp.Sum(share[k] * slackG[k], (k, 1, K)).is_nonnegative

    ctx["L14"] = dict(
        nk=nk,
        regroup_leftover=leftover,
        regroup_swap_equal=regroup_swap_equal,
        objective_agrees=objective_agrees,
        local_min_slack=local_min_slack,
        local_min_nonneg=local_min_nonneg,
        cor_slack=cor_slack,
        cor_nonneg=cor_nonneg,
    )


def verify(ctx):
    r = ctx["L14"]
    # hypotheses carried from the earlier lemmas
    assert ctx["L13"].get("margin_positive") is True, (
        "L14 FAIL: no assignment-stable neighborhood (R2 positive margin, L13)"
    )
    assert ctx["L12"].get("chain_nonneg") is True and ctx["L12"].get("lower_nonneg") is True, (
        "L14 FAIL: Lemma 1 (0 <= f - f* <= G) not established"
    )
    assert r["regroup_swap_equal"] is True, (
        "L14 FAIL: per-facet regrouping is not a Fubini swap of the double sum"
    )
    assert r["objective_agrees"] == 0, (
        "L14 FAIL: full objective differs from the fixed-assignment expression"
    )
    assert sp.simplify(r["local_min_slack"]) == 0, (
        "L14 FAIL: F(W') - F(W) != sum_k share_k (f_k(w'_k) - f_k(w_k))"
    )
    assert r["local_min_nonneg"] is True, "L14 FAIL: sum_k share_k (f_k' - f_k) is not nonnegative"
    assert sp.simplify(r["cor_slack"]) == 0, (
        "L14 FAIL: sum share G - sum share (f - f*) != sum share (G - (f - f*))"
    )
    assert r["cor_nonneg"] is True, "L14 FAIL: sum_k share_k (G_k - (f_k - f_k*)) not nonnegative"

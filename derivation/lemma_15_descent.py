"""L15 (Level 1) - descent: one accepted iteration of the unpenalized step B does not raise F.

Setting.  As in L14: K terms with exponents w_k on the simplex, reaches beta_k = J_tau(U w_k),
cells C_1..C_K a partition of the N rows (the membership family chi of A8), slack of row i on term
k s_ki = beta_k - w_k.u_i, and the mean slack F(W) = (1/N) sum_i s_{k(i) i}.  One iteration is
(i) reassign every row to its maximizing term, which is the term of least slack, then (ii) refit
each term to a minimizer of its convex term objective f_k (L12's setting) on the new cells.

What this proves (symbolic K, N; plain SymPy):
  1. Reassignment (i).  Write m_i = min_k s_ki, so r_ki = s_ki - m_i >= 0 with equality at the
     maximizing term (F12, the min representation).  Because every row lies in one cell
     (sum_k chi_ki = 1, A8), the current mean slack is (1/N) sum_i m_i + (1/N) sum_i sum_k chi_ki
     r_ki, and the reassigned mean slack is (1/N) sum_i m_i (the slack of row i on its maximizing
     term is m_i).  So F(current) - F(reassigned) = (1/N) sum_i sum_k chi_ki r_ki, a sum of
     nonnegative terms.
  2. Refit (ii).  On the new cells (A8 again, now with membership chi'), L14's identity gives
     F = sum_k share'_k f'_k(w_k) with share'_k = n'_k/N >= 0.  A refit w+_k that minimizes f'_k
     has f'_k(w_k) - f'_k(w+_k) = f'_k(w_k) - f'_k* >= 0 (L12), so F(reassigned) - F(refit) =
     sum_k share'_k (f'_k(w_k) - f'_k(w+_k)), a sum of nonnegative terms.
  3. The two differences add: F(current) - F(refit) >= 0 for every accepted iteration, so the
     sequence of accepted iterates is non-increasing in F.

What this does NOT prove: that F converges, that the limit is a local or global minimizer, or any
statement for the penalized objective or the tangent refit (step D), where beta_k is not the reach
J_tau(U w_k) or the refit is not an exact term minimizer; that every cell stays nonempty
after reassignment (A8 requires it: an iteration that empties a cell is not an accepted one).

Second result (steps L15.17 to L15.22): finite termination of the sharp alternation.  The loop
is: assign every row to its maximizing term (a fixed tie rule), stop if the assignment is
unchanged, else refit each term on its new cell and repeat.  Write chi_t for the partition at
iteration t and Phi_t for the mean slack after the refit on chi_t.  Two hypotheses of this result:
(H1) unique term minimizers: each cell's term objective has one minimizer, so the refit on a cell
set is a function of the cells and of nothing else (fails when a cell's centred log-metrics do not
span, where the term objective is flat along a direction); (H2) a fixed tie rule: the assignment
is a function of the exponents and their reaches (the implementation's argmax takes the lowest
index on a tie).  The argument: Phi is non-increasing (the first result), and a repeated
partition chi_t = chi_s, t > s, pins Phi_{s+1} = Phi_s, so both drops of iteration s are zero; a
zero refit drop means every nonempty cell's term was already at its minimum value, so by H1 the
refit returns the exponents it started from (an empty cell keeps its exponents), by H2 the next
assignment is the same assignment, and the loop stops.  Hence the partitions before the stop are
pairwise distinct; there are K^N partitions (one cell per row), so the loop stops within K^N + 1
iterations, ties included.  What this does NOT prove: that the stopping point is a local or global
minimizer (Q1 stays open; I7 is the solver-level citation); anything about the monotone guard,
which rejects a floating-point increase that exact arithmetic excludes; a useful rate (K^N is a
count); or termination of the soft alternation, whose weights are not a finite state.
"""

import sympy as sp
from sympy.logic.inference import satisfiable

from derivation.axioms import A8, F12
from derivation.lemma_12_term_gap import L12_RESULT
from derivation.lemma_14_assignment_stable import L14_RESULT
from derivation.sumtools import linear

TITLE = "descent (Level 1): reassignment and term refit do not increase the mean slack"
STATEMENT = (
    "Level 1 (descent), step B unpenalized: reassigning every row to its maximizing term does "
    "not increase the mean slack F, and refitting each term to a minimizer of its convex term "
    "objective does not increase F; so F is non-increasing along accepted iterations."
)
AXIOMS_USED = ["A8", "F12"]
# Two results share this file (as L14): the step tags run in one sequence, each owned by one.
PROOF_RESULTS = (
    (
        "descent (Level 1): reassignment and term refit do not increase the mean slack",
        (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16),
    ),
    (
        "finite termination of the sharp alternation: at most K^N + 1 iterations, given unique "
        "term minimizers and a fixed tie rule",
        (17, 18, 19, 20, 21, 22),
    ),
)


def derive(ctx):
    S = ctx["S"]
    i, k, K = S.i, S.k, S.K
    # [L15.1] A8: the membership family chi_ki, the cell counts n_k and the number N of rows
    chi, ncell, N = A8.obj("membership"), A8.obj("count"), A8.obj("rows")

    # 1. reassignment (i): m_i = min_k s_ki, r_ki = s_ki - m_i, one row at a time
    mrow = sp.IndexedBase("mrow")  # m_i, the least slack of row i over the terms
    # [L15.2] F12: r_ki = s_ki - m_i >= 0 for every row i and term k, with equality at k*(i)
    r = F12.nonneg_base("r")
    row_now = sp.Sum(chi[k, i] * (mrow[i] + r[k, i]), (k, 1, K))
    row_drop = sp.Sum(chi[k, i] * r[k, i], (k, 1, K))
    # [L15.3] A8: sum_k chi_ki = 1, so row i's slack on its own cell is m_i + sum_k chi_ki r_ki
    row_split = sp.simplify(A8.rewrite(linear(row_now), only=(0,)) - (mrow[i] + row_drop))
    sx, kstar = sp.IndexedBase("sx"), sp.Symbol("kstar", integer=True)
    # [L15.4] F12: the slack of row i on its maximizing term k*(i) is m_i, the least over terms
    on_maximizing = F12.rewrite(
        sx[kstar],
        rename={
            sp.IndexedBase("g"): sx,
            sp.Symbol("j0", integer=True): kstar,
            sp.Symbol("m", real=True): mrow[i],
        },
    )
    # the mean over the rows: F(current) - F(reassigned) = (1/N) sum_i sum_k chi_ki r_ki
    F_now = sp.Sum(mrow[i] + row_drop, (i, 1, N)) / N
    F_reassigned = sp.Sum(on_maximizing, (i, 1, N)) / N
    F_drop = sp.Sum(row_drop, (i, 1, N)) / N
    reassign_diff = sp.simplify(linear(F_now - F_reassigned) - linear(F_drop))
    reassign_nonneg = F_drop.is_nonnegative

    # 2. refit (ii) on the new cells chi', with new counts n'_k
    # [L15.5] A8: the new membership chi'_ki >= 0 and the new cell counts n'_k
    chip, ncellp = A8.nonneg_base("chip"), sp.IndexedBase("ncellp")
    new_cells = {chi: chip, ncell: ncellp}
    # [L15.6] A8 on the new cells: share'_k = n'_k / N = sum_i chi'_ki / N >= 0
    share = A8.rewrite(ncellp[k] / N, only=(2,), rename=new_cells)
    # [L15.7] by L14: on any partition of the rows, F = sum_k share_k f_k(w_k)
    partition_identity = L14_RESULT.holds(ctx, "partition_identity")
    # [L15.8] by L12: a minimizing refit has e_k = f'_k(w_k) - f'_k* >= 0
    e = L12_RESULT.family(ctx, "lower_nonneg", "e")
    fnew = sp.IndexedBase("fnew")  # f'_k(w_k), the term objective on the new cells at the old fit
    F_cells = sp.Sum(share * fnew[k], (k, 1, K))
    F_refit = sp.Sum(share * (fnew[k] - e[k]), (k, 1, K))
    refit_diff = sp.simplify(linear(F_cells - F_refit) - linear(sp.Sum(share * e[k], (k, 1, K))))
    refit_nonneg = sp.Sum(share * e[k], (k, 1, K)).is_nonnegative

    # 3. the two drops add: F(current) - F(refit) = drop + refit drop, both nonnegative
    Fc, Fn, Fr, D1, D2 = sp.symbols("Fc Fn Fr D1 D2", real=True)
    total = sp.simplify((Fc - Fr).subs({Fc: Fn + D1}).subs({Fn: Fr + D2}) - (D1 + D2))
    ctx["L15"] = dict(
        row_split=row_split,
        on_maximizing=sp.simplify(on_maximizing - mrow[i]),
        reassign_diff=reassign_diff,
        reassign_nonneg=reassign_nonneg,
        partition_identity=partition_identity,
        refit_diff=refit_diff,
        refit_nonneg=refit_nonneg,
        total=total,
        nonincreasing=bool(reassign_nonneg is True and refit_nonneg is True and total == 0),
    )


def verify(ctx):
    r = ctx["L15"]
    # [L15.9] the slack of row i on its own cell splits as m_i + sum_k chi_ki r_ki (A8)
    assert r["row_split"] == 0, "L15 FAIL: the row slack does not split as m_i + sum_k chi_ki r_ki"
    # [L15.10] the slack on the maximizing term is the least slack m_i (F12)
    assert r["on_maximizing"] == 0, "L15 FAIL: the maximizing term's slack is not m_i"
    # [L15.11] F(current) - F(reassigned) = (1/N) sum_i sum_k chi_ki r_ki
    assert r["reassign_diff"] == 0, "L15 FAIL: F(current) - F(reassigned) != the mean of chi r"
    # [L15.12] each term chi_ki r_ki / N is >= 0, so reassignment does not increase F
    assert r["reassign_nonneg"] is True, "L15 FAIL: the reassignment drop is not nonnegative"
    # [L15.13] by L14: F = sum_k share_k f_k(w_k) holds on the new cells
    assert r["partition_identity"] is True, "L15 FAIL: L14's cell identity is not established"
    # [L15.14] F(reassigned) - F(refit) = sum_k share'_k (f'_k(w_k) - f'_k(w+_k))
    assert r["refit_diff"] == 0, "L15 FAIL: F(reassigned) - F(refit) != sum_k share'_k e_k"
    # [L15.15] each term share'_k e_k is >= 0 (L12), so the term refit does not increase F
    assert r["refit_nonneg"] is True, "L15 FAIL: the refit drop is not nonnegative"
    # [L15.16] F(current) - F(refit) = drop + refit drop, both >= 0: F is non-increasing
    assert r["total"] == 0 and r["nonincreasing"] is True, (
        "L15 FAIL: F(current) - F(refit) is not the sum of the two nonnegative drops"
    )

    # --- second result: finite termination of the sharp alternation (the docstring's setting,
    # hypotheses H1 and H2).  x is the drop of iteration s, D1 and D2 its two parts (L15.16).
    S = ctx["S"]
    i, K = S.i, S.K
    x, D1, D2 = sp.symbols("x D1 D2", real=True)
    # [L15.17] a repeat chi_t = chi_s (t > s) pins the drop x = Phi_s - Phi_{s+1}: x >= 0 (L15.16)
    # and x <= Phi_s - Phi_t = 0 (the later drops are >= 0 too), so x = 0
    assert sp.reduce_inequalities([x >= 0, x <= 0], x) == sp.Eq(x, 0), (
        "L15 FAIL: a drop that is >= 0 and <= 0 is not 0"
    )
    # [L15.18] the zero drop is D1 + D2 with D1, D2 >= 0 (L15.12, L15.15): D1 = -D2 <= 0 pins
    # D2 = 0, and then D1 = 0: both the reassignment drop and the refit drop vanish
    assert sp.reduce_inequalities([D2 >= 0, sp.solve(sp.Eq(D1 + D2, 0), D1)[0] >= 0], D2) == sp.Eq(
        D2, 0
    ), "L15 FAIL: two nonnegative drops with zero sum are not both zero"
    zero_refit, same_w, same_a, stop = sp.symbols(
        "zero_refit_drop same_exponents same_assignment stop"
    )
    by_h1 = sp.Implies(zero_refit, same_w)  # H1: a zero refit drop returns the same exponents
    by_h2 = sp.Implies(same_w, same_a)  # H2: the same exponents give the same assignment
    rule = sp.Implies(same_a, stop)  # the loop stops when the assignment is unchanged
    # [L15.19] with H1, H2 and the stop rule, a zero refit drop (L15.18, after a repeat) forces the
    # stop: the partitions before the stop are pairwise distinct
    assert satisfiable(sp.And(by_h1, by_h2, rule, zero_refit, sp.Not(stop))) is False, (
        "L15 FAIL: a repeated partition does not force the stop"
    )
    # [L15.20] negative control: without H1 (a flat term objective, several minimizers) the stop
    # does not follow, so H1 is load-bearing
    assert satisfiable(sp.And(by_h2, rule, zero_refit, sp.Not(stop))) is not False, (
        "L15 FAIL: the stop followed without the unique-minimizer hypothesis"
    )
    # [L15.21] A8: one cell per row, so a partition is a map from the N rows to the K terms, one
    # of prod_i K = K^N
    n_partitions, N = sp.Product(K, (i, 1, A8.obj("rows"))).doit(), A8.obj("rows")
    # [L15.22] there are K^N partitions and no K^N + 1 of them are pairwise distinct, so the loop,
    # whose partitions before the stop are pairwise distinct (L15.19), runs at most K^N + 1 times
    assert n_partitions == K**N and sp.binomial(n_partitions, n_partitions + 1) == 0, (
        "L15 FAIL: the partitions do not number K^N, or more than K^N are pairwise distinct"
    )
    ctx["L15"]["terminates"] = True

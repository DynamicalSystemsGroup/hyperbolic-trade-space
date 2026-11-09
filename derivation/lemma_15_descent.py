"""L15 (Level 1) - descent: one accepted iteration of the unpenalized step B does not raise F.

Setting.  As in L14: K facets with exponents w_k on the simplex, offsets beta_k = J_tau(U w_k),
cells C_1..C_K a partition of the N rows (the membership family chi of A8), slack of row i on facet
k s_ki = beta_k - w_k.u_i, and the mean slack F(W) = (1/N) sum_i s_{k(i) i}.  One iteration is
(i) reassign every row to its maximizing facet, which is the facet of least slack, then (ii) refit
each facet to a minimizer of its convex facet objective f_k (L12's setting) on the new cells.

What this proves (symbolic K, N; plain SymPy):
  1. Reassignment (i).  Write m_i = min_k s_ki, so r_ki = s_ki - m_i >= 0 with equality at the
     maximizing facet (F12, the min representation).  Because every row lies in one cell
     (sum_k chi_ki = 1, A8), the current mean slack is (1/N) sum_i m_i + (1/N) sum_i sum_k chi_ki
     r_ki, and the reassigned mean slack is (1/N) sum_i m_i (the slack of row i on its maximizing
     facet is m_i).  So F(current) - F(reassigned) = (1/N) sum_i sum_k chi_ki r_ki, a sum of
     nonnegative terms.
  2. Refit (ii).  On the new cells (A8 again, now with membership chi'), L14's identity gives
     F = sum_k share'_k f'_k(w_k) with share'_k = n'_k/N >= 0.  A refit w+_k that minimizes f'_k
     has f'_k(w_k) - f'_k(w+_k) = f'_k(w_k) - f'_k* >= 0 (L12), so F(reassigned) - F(refit) =
     sum_k share'_k (f'_k(w_k) - f'_k(w+_k)), a sum of nonnegative terms.
  3. The two differences add: F(current) - F(refit) >= 0 for every accepted iteration, so the
     sequence of accepted iterates is non-increasing in F.

What this does NOT prove: that F converges, that the limit is a local or global minimizer, or any
statement for the penalized objective or the tangent refit (step D), where the offsets are not
beta_k = J_tau(U w_k) or the refit is not an exact facet minimizer; that every cell stays nonempty
after reassignment (A8 requires it: an iteration that empties a facet is not an accepted one).
"""

import sympy as sp

from derivation.axioms import A8, F12
from derivation.lemma_12_facet_gap import L12_RESULT
from derivation.lemma_14_assignment_stable import L14_RESULT
from derivation.sumtools import linear

TITLE = "descent (Level 1): reassignment and facet refit do not increase the mean slack"
STATEMENT = (
    "Level 1 (descent), step B unpenalized: reassigning every row to its maximizing facet does "
    "not increase the mean slack F, and refitting each facet to a minimizer of its convex facet "
    "objective does not increase F; so F is non-increasing along accepted iterations."
)
AXIOMS_USED = ["A8", "F12"]


def derive(ctx):
    S = ctx["S"]
    i, k, K = S.i, S.k, S.K
    # [L15.1] A8: the membership family chi_ki, the cell counts n_k and the number N of rows
    chi, ncell, N = A8.obj("membership"), A8.obj("count"), A8.obj("rows")

    # 1. reassignment (i): m_i = min_k s_ki, r_ki = s_ki - m_i, one row at a time
    mrow = sp.IndexedBase("mrow")  # m_i, the least slack of row i over the facets
    # [L15.2] F12: r_ki = s_ki - m_i >= 0 for every row i and facet k, with equality at k*(i)
    r = F12.nonneg_base("r")
    row_now = sp.Sum(chi[k, i] * (mrow[i] + r[k, i]), (k, 1, K))
    row_drop = sp.Sum(chi[k, i] * r[k, i], (k, 1, K))
    # [L15.3] A8: sum_k chi_ki = 1, so row i's slack on its own cell is m_i + sum_k chi_ki r_ki
    row_split = sp.simplify(A8.rewrite(linear(row_now), only=(0,)) - (mrow[i] + row_drop))
    sx, kstar = sp.IndexedBase("sx"), sp.Symbol("kstar", integer=True)
    # [L15.4] F12: the slack of row i on its maximizing facet k*(i) is m_i, the least over facets
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
    fnew = sp.IndexedBase("fnew")  # f'_k(w_k), the facet objective on the new cells at the old fit
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
    # [L15.10] the slack on the maximizing facet is the least slack m_i (F12)
    assert r["on_maximizing"] == 0, "L15 FAIL: the maximizing facet's slack is not m_i"
    # [L15.11] F(current) - F(reassigned) = (1/N) sum_i sum_k chi_ki r_ki
    assert r["reassign_diff"] == 0, "L15 FAIL: F(current) - F(reassigned) != the mean of chi r"
    # [L15.12] each term chi_ki r_ki / N is >= 0, so reassignment does not increase F
    assert r["reassign_nonneg"] is True, "L15 FAIL: the reassignment drop is not nonnegative"
    # [L15.13] by L14: F = sum_k share_k f_k(w_k) holds on the new cells
    assert r["partition_identity"] is True, "L15 FAIL: L14's cell identity is not established"
    # [L15.14] F(reassigned) - F(refit) = sum_k share'_k (f'_k(w_k) - f'_k(w+_k))
    assert r["refit_diff"] == 0, "L15 FAIL: F(reassigned) - F(refit) != sum_k share'_k e_k"
    # [L15.15] each term share'_k e_k is >= 0 (L12), so the facet refit does not increase F
    assert r["refit_nonneg"] is True, "L15 FAIL: the refit drop is not nonnegative"
    # [L15.16] F(current) - F(refit) = drop + refit drop, both >= 0: F is non-increasing
    assert r["total"] == 0 and r["nonincreasing"] is True, (
        "L15 FAIL: F(current) - F(refit) is not the sum of the two nonnegative drops"
    )

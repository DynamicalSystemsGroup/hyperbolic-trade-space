# Proof-map findings and how each was closed (WP10 Amendment 2, R-32)

The tagging (D-12, commits d45ef4d and 78b29e2) recorded what it found instead of relabelling it.
This file is the record of how Amendment 2 closed each finding. Addresses are file and tag
(`uv run python -m derivation.proofmap` lists them; the committed record is
`proof_map_record.json`). No `TITLE` or `STATEMENT` changed in any of the fourteen scripts (checked
by comparing the module literals with those at commit 093dc7a), and nothing proved changed.

Commits, in order: 56ba9aa (helper functions to `sumtools.py`, shared index symbols `L` and `J0` to
`symbols.py` under A0, no change in behaviour); 9d58e5f (principles 1 and 4); 5152db3 (principle 2);
72b6d5a (principle 3); 3626aad (principle 5).

## What the checker now enforces (and its negative controls, `tests/test_proof_map.py`)

| Rule | Where | Negative control |
|---|---|---|
| imported ledger names = names applied by tagged steps = `AXIOMS_USED` | `proofmap.parse_lemma` (as before) | import an unapplied name; drop a name from `AXIOMS_USED` |
| no `Axiom.invoke` (a do-nothing application; the method is removed from `Axiom`) | `proofmap._check_symbols` | a scratch copy with `A3.invoke(...)` fails |
| no signed symbol made directly (`positive`, `nonnegative`, `negative`, `nonpositive`; and no real-valued `IndexedBase`): it comes from a ledger entry's factory (a tagged step), from an earlier result (`ProvedResult.family`), or is a module-level hypothesis of the statement whose quoted claim must occur in the lemma's `STATEMENT` or docstring | `proofmap._check_symbols` | direct `Symbol(..., nonnegative=True)`; `IndexedBase(..., real=True)`; `symbols(..., positive=True)`; a hypothesis inside a function; a hypothesis whose quotation is not in the statement |
| a lemma script may import from another lemma script only `L<m>_RESULT`, of a lemma earlier in `CHAIN_NAMES`, which that script exports (`L<m>_RESULT = ProvedResult(...)`) and certifies in its `verify`; the import must be applied by a step of kind "result" and not used on an untagged line | `proofmap._result_imports` | an extra name; a whole-script import; a later lemma's result; an unapplied import; an uncertified export (fails exporter and importer); a name the script does not export; an untagged use |
| a forced logarithm or power takes its licence from ledger entries that declare the positivity (`LicenceError` otherwise) | `derivation/licence.py` | each call site is run without its entry or with the wrong one (`test_proof_map.py`, "principle 1") |

## 1. The seven prose-only steps (findings section 1): closed

| Was | Now |
|---|---|
| L14, regrouping of the N rows over the K cells ("stated, not derived") | A8 (new, posited): the partition relation (`chi` with `sum_k chi_ki = 1`, `chi >= 0`, `n_k = sum_i chi_ki >= 1`) applied by import: L14.1, L14.2, L14.4, L14.5, L14.7; checked at L14.12 to L14.15 (Fubini swap of the row and cell sums; the cell sum is `n_k f_k(w_k)`; `F(W) = sum_k share_k f_k(w_k)`; `share_k` nonnegative because `chi >= 0`) |
| L12, complementary slackness `p_i (M - s_i) = 0` (a comment) | I12 (new, inherited, Boyd and Vandenberghe 5.5.2) applied termwise by `rewrite` inside the sum: L12.8 (sum is 0), L12.27 (`sum_i p_i s_i = M`); then L12.28 (`g.w = M - ubar.w = f(w)`) and L12.29 (centred `(U_c^T p)_j`); the LP duality gap is zero by I1 at L12.32 |
| L5, strictness of `LSE - max > 0` for n >= 2 (a comment) | coded, the statement unchanged: the i0 term is 1 by F5 (L5.3), a second shifted term is positive on real scores (L5.5, L5.19), `T >= 1 + (second term) > 1` so `(1/tau) log T > 0` (L5.20); L5.18 records that indices 1 and 2 are in range and differ when n >= 2. The statement claims strict for n >= 2 and the script now asserts exactly that; the n = 1 equality case is unchanged. No STOP was needed |
| L11, contrapositive and efficiency deductions (prose) | propositional steps SymPy checks by showing the negated goal unsatisfiable (`sumtools.entails`): L11.17 (a maximizer is not dominated in a contending metric), L11.18 (weakly efficient in all d metrics, with "some w_j > 0" derived from the simplex by A2 at L11.3), L11.19 (efficient when every w_j > 0), L11.20 (the chain is not vacuous). The premises are built from the computed facts (L11.5 to L11.9); a falsified fact makes the step fail |
| L2, "hence beta shifts by c and w* is unchanged" | L2.3 (shift amount of `J` computed under A1, A2, A3), L2.6 (it equals c), L2.7 (the shift cancels in `J(w') - J(w)`), L2.8 (so `J(w') >= J(w)` iff the shifted inequality) |
| L4, convexity is nonnegativity of the second derivative along every line | I11 (new, inherited, Boyd and Vandenberghe 3.1.1 and 3.1.4), L4.13: `Equivalent(second derivative >= 0 on every line, convex)` applied by `entails` to the computed sign; with the sign false there is no conclusion |
| L3, first-order necessary condition with a linear equality constraint | I10 (new, inherited; first cited to Boyd and Vandenberghe 5.5.3 and 5.2.3, re-based on Nocedal and Wright 12.1 with the LICQ of 12.4, section 4): the KKT conditions on the simplex, `g_j - lambda - mu_j = 0`, `mu_j >= 0`, `w_j mu_j = 0`, applied in L3.6 (stationarity along `e_j0`), L3.7 (complementary slackness termwise gives `sum_j w_j (g_j - lambda) = 0`), L3.11 and L3.20 (with R1) |

Note on I10 (reported to the PM). The citation is to the KKT conditions as necessary for a
differentiable problem with strong duality (5.5.3), and to refined Slater for affine constraints
(5.2.3); for the convex `J_tau` the conditions are therefore necessary. Convexity of `J_tau` is L4,
which comes after L3 in the chain, and the checker allows L3 to import nothing from L4. The entry's
statement and failure mode say so; the dependency is on the textbook theorem, not on L4's script.

## 2. Premises carried as symbol assumptions (findings section 2): closed

Every signed symbol is now one of: made by a ledger factory on a tagged step; taken from an earlier
result; or a module-level hypothesis of the statement that quotes it (listed per lemma in the record
under `hypotheses`).

| Lemma | Symbols | Licence |
|---|---|---|
| L3 | `wp`, `mup`, `mu` | R1 (`w_j > 0`), I10 (multipliers) |
| L4 | `a_r`, `s_r` (real) | A1 (`A1.real_base`) |
| L5 | `slack`, `sr` | F5 |
| L7 | `uu` (real) | A1 |
| L10 | `slack` | F10 |
| L11 | `wn` (A2); `dl`, `wp`, `dp`, `eps`, `gam` | hypotheses quoted from the statement/docstring; `rest` is now the computed sum over `j != j0` |
| L12 | `vn`, `wn` (A2), `gm`, `b_nn` (F12), `a_nn` (I8); `c_nn` | hypothesis "f(w) - f* >= 0 because f* is the minimum"; `a_t`, `r_t` are now the term `w_j0 (g_j0 - m)` and the sum of the others; the chain `G - (f - f*) = a + b` is now computed from I8's slack equation and F12's slack, not from separate symbols |
| L13 | `rest` (F12), `cs` (I9), `g_` (R2); `delta`, `a1`, `a2`, `c`, `nth`, `a_`, `b_`, `UU`, `r_`, `U_` | hypotheses quoted from the statement/docstring |
| L14 | `share` (from A8: `n_k / N`, nonnegative because `chi >= 0`), `slackG` (L12's result), `dfk` (hypothesis "every w_k minimizes f_k"), `n_k` is the shared size `S.n` | |

Forced logarithms and powers (findings section 4, second item): L2 (A1, A2, A3), L5 (A3, F5), L6
(A2, A3, A5), L7 (A1, A2), L9 (A4), L10 (A1, A6), L1 (A1): each takes its licence and raises
`LicenceError` without it.

## 3. Entries in `AXIOMS_USED` that no step depended on (findings section 3): closed

Do-nothing lines (`invoke`) removed; `AXIOMS_USED` corrected. Before, after, why:

| Lemma | Before | After | Why |
|---|---|---|---|
| L1 | A1, A2 | A1, A2 | both real (A1 licenses the logs; A2 rewrites the simplex); now `product_to_exp_sum` requires its licence |
| L2 | A2, A3 | A1, A2, A3 | the forced log of a sum of exponentials needs `u` real (A1), `w` real (A2), `tau > 0` (A3); the docstring said A3 did not enter, it enters through the licence |
| L3 | A2, A3, R1 | A2, I10, R1 (unchanged by the follow-up: the LICQ steps apply A2) | A3 stated the premise only (a division by `tau` needs no sign); R1 now a real premise (forces `mu_j = 0`); I10 added (section 1) |
| L4 | A1, A3 | A1, A3, I11 | A1 supplies the real families, A3 the sign of `tau` at L4.12 (`A3.positive(tau)`); I11 added |
| L5 | A3, I1, I2, I3, F5 | A3, F5 | I1, I2, I3 were remarks no step used (reported apart below); F5 now used by its second relation, its slack and the real scores |
| L6 | A2, A5, I5 | A2, A3, A5, I5 | A2 was only declared; now A2, A3, A5 license the log of the MGF factor; I5 now supplies the product (a form) |
| L7 | A1, A2 | A1, A2 | A1 makes the point of F real; A1 and A2 license the power `V^(-1/w)`; the A2 rewrite on L1's `Vk` was a no-op and is removed |
| L8 | A7, I6 | A7, I6 | unchanged |
| L9 | A1, A2, A4 | A2, A4 | the A1 line was a no-op; A4's own relation rewrites `u` |
| L10 | A2, A6, I4, F10 | A1, A6, F10 | the A2 line (K = 1) was a no-op; I4 is cited context; A1 licenses the logs and the powers of `m`; F10 now used (second relation gives the unit term, slack) |
| L11 | A1, A2 | A2 | the A1 line was a no-op |
| L12 | A2, A3, I1, I8, F12 | A2, I1, I8, I12, F12 | the A3 line was a no-op (convexity is L4's); I1 now applied by `rewrite` (primal and dual values coincide); I12 added |
| L13 | F12, I9, R2 | F12, I9, R2 | R2 now real: `g_` is R2's positive margin and the stable radius `g/(2U)` is positive only through it (L13.12) |
| L14 | A2, R2 | A8, R2 | the A2 line was a no-op; R2 now supplies the equation `M_i = s_i,k(i)` (a form); A8 added |

## 4. Ledger changes (new, changed, reclassified) and test edits

| Entry | Change | Why |
|---|---|---|
| A8 | new, POSITED | the partition relation of L14 (section 1) |
| I10 | new, INHERITED; Boyd and Vandenberghe 5.5.3 and 5.2.3 (read in the PDF of the authors' site: 5.5.3 "KKT optimality conditions", 5.2.3 "Strong duality and Slater's constraint qualification") | L3's first-order condition |
| I10 (follow-up, 2026-11-09) | re-based: Nocedal and Wright, Theorem 12.1 under the LICQ of Definition 12.4 (text of Chapter 12 read); Boyd and Vandenberghe 5.5.3 kept only as a convex-case remark; statement and failure mode no longer mention strong duality or convexity | the first version made KKT necessary through strong duality, hence through convexity (L4, which imports L3): a proof must not lean on a later lemma even through a textbook. LICQ is computed in L3 (steps L3.1 to L3.4 and their checks L3.16 to L3.18), with a negative control |
| I11 | new, INHERITED; Boyd and Vandenberghe 3.1.1 (restriction to a line) and 3.1.4 (second-order conditions) | L4's convexity |
| I12 | new, INHERITED; Boyd and Vandenberghe 5.5.2 ("Complementary slackness") | L12's termwise zero |
| I1 | from named proposition to a form `v_primal = v_dual` | applied by `rewrite` at L12.32 |
| I5 | from named proposition to a form (the MGF of the sum is the product of the MGFs) | applied by `specialize` at L6.2 |
| R1 | from named proposition to a form `w_j > 0` | `R1.positive_symbol` at L3.9 (was L3.5) |
| R2 | relation extended with `M_i = s_i,k(i)` | applied by `rewrite` at L14.6 |
| A6 | relation extended with `theta_kj >= 0` (the statement already says "on the simplex") | the simplex is a sum of 1 and nonnegativity; needed for the reality of `theta` in the licence |
| I2, I3, I4 | reclassified: `CITED_CONTEXT` in `axioms.py`, a class reported apart in the audit with the reason for each (no step of L5 uses I2, I3; I4's reading "GP-compatible" is not a premise of L10's identity); like `SOLVER_LEVEL` (I7) they are exempt from the every-axiom-is-used test | principle 4 |
| shared symbols | `S.beta` is declared `real=True` (a type, not a sign; not policed by the hygiene test); `L` and `J0` added to the namespace under A0 | licences need `beta` real; step 0 |

Edits to `tests/test_derivation.py` (each pins something this amendment corrects; no negative control
removed): the every-axiom-is-used exemption adds `AX.CITED_CONTEXT`; `"A3" in _L3.AXIOMS_USED` removed
(L3); `L11.AXIOMS_USED == ["A2"]`; `L12 >= {A2, I1, I8, F12}` (A3 dropped); `L14 >= {R2}` (A2
dropped); the L14 docstring-wording test now asserts A8 and "declared relation A8" instead of the
words "symbolic partition" and "one-line finite-sum argument" (the prose the step replaced).

## 5. Entries no proof consumes (principle 4)

| Entry | Class | Reason |
|---|---|---|
| I7 | `SOLVER_LEVEL` (unchanged) | the K > 1 solver stops at a local optimum; no lemma consumes it |
| I2 | `CITED_CONTEXT` | a remark on the consistency of the sample LME (L5); no step uses it |
| I3 | `CITED_CONTEXT` | a remark on the support function (L5); no step uses it |
| I4 | `CITED_CONTEXT` | L10 shows exp(kappa Phi_K) is a sum of monomials with positive coefficients (a posynomial); GP-compatibility is a reading, not a premise |
| A0 | `STRUCTURAL` (unchanged) | licenses the sizes and indices |

## 6. Earlier lemmas' results by import (principle 5)

L4 on L3 (`L3_RESULT`), L7 on L1 (`L1_RESULT`), L12 on L4 (`L4_RESULT`), L14 on L12 and L13
(`L12_RESULT`, `L13_RESULT`). The exporter declares `L<n>_RESULT = ProvedResult(...)` and certifies it
as the last line of `verify` (`derivation/results.py`); the importer applies it in a tagged step of
kind "result" (L4.1, L7.3, L12.10 and L12.11, L14.8 to L14.10). The objects still travel through the
runner's `ctx`; a result taken before it is certified raises `UnprovedResultError`.

## 7. Shape of the work now

- Ledger: 26 entries (A0 to A8, I1 to I12, R1, R2, F5, F10, F12). 236 tagged steps in 14 files (L3 has 35 since the I10 follow-up).
- Step kinds: computed, by a declared axiom (the line applies a ledger entry, from the ledger), by a
  proved result.
- `PROOF_RESULTS` of L14: Proposition 3 and Corollary 4 partition its 20 steps.

## 8. L3 tags moved by the I10 follow-up (LICQ steps added)

Seven steps are new: L3.1 to L3.4 (derive: the zero set is proper by A2, the component of the
combination of the active gradients, the solution, the negative control) and L3.16 to L3.18 (verify:
their checks). Old L3.1 to L3.11 are now L3.5 to L3.15 (+4); old L3.12 to L3.28 are now L3.19 to
L3.35 (+7). Nothing else in the record moved; the statement, title and `AXIOMS_USED` of every lemma are
unchanged. Only the ledger fingerprint of I10 changed.

## 9. L15, Level 1 (descent): a new lemma, and the pins it corrects (WP10, C-1)

Level 1 (accepted iterations do not increase the mean slack F) had neither a badge nor a script.
`lemma_15_descent.py` (L15, 16 steps) scripts it for step B unpenalized: reassignment to the
maximizing facet does not increase F (F12 min representation, A8 partition; `F(current) -
F(reassigned) = (1/N) sum_i sum_k chi_ki r_ki`, nonnegative terms), and a minimizing facet refit
does not increase F (L14's cell identity, L12's `f - f* >= 0`; `F(reassigned) - F(refit) = sum_k
share'_k e_k`, nonnegative terms). Its STATEMENT is new; no existing `TITLE` or `STATEMENT`
changed. L14 now exports `L14_RESULT` (certified at the end of its `verify`, with the fact
`partition_identity` added to its context); no L14 step changed. Steps by kind: tagged A8 (L15.1,
3, 5, 6), F12 (L15.2, 4), by a proved result (L15.7 from L14, L15.8 from L12), computed (L15.9 to
L15.16). Not proved, stated in the docstring: convergence, nonemptiness of cells after
reassignment (an accepted iteration is one that keeps every facet nonempty, as A8 requires).

| Pin | Before | After | Why |
|---|---|---|---|
| `test_derivation.py` WP13 chain order | `CHAIN_NAMES[-3:]` is L12, L13, L14 | `CHAIN_NAMES[-4:-1]`; `CHAIN_NAMES[-1]` is L15 | L15 is appended to the chain |
| `test_derivation.py` run header | `L1 -> L14` | `L1 -> L15` | `run.py` banner counts the chain |
| `test_build_generated.py` chain length | 14 | 15 | one more lemma |
| `test_proof_map.py` imports | L14 imports L12, L13 | plus `lemma_15_descent.py` imports L12, L14 | L15 uses the results |
| `test_proof_map.py` exports | L1, L3, L4, L12, L13 | plus L14 | L14 exports its result for L15 |

No negative control was removed; new controls for L15 are in `test_derivation.py`.

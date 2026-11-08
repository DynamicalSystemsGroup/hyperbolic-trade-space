# WP1 — Review report (third pass, after the L8 fix and the attribution rewrite)

| | |
|---|---|
| **Scope of work** | `work-packages/WP1-scope-of-work.md` (approved at 0b181d7, draft 3) |
| **Scope approval verified** | Verbal approval recorded in `work-packages/WP1-decisions.md` (section "Scope approval", commit 5d2b0ec): supervisor (mzargham), verbatim "OK", 2026-11-07; defaults list approved as one item; open decisions none. The project has no PRs; this is the recorded act the scope names. The record is typed by the agent, so the review cannot confirm the chat itself. The same file records G-5 "Fix L8 before acceptance" (6ca990e) and G-9 "Rewrite the message and force-push" (9b8a7e9), which this pass follows. |
| **Work reviewed** | `main` at `9b8a7e9` after `git fetch origin && git reset --hard origin/main`. Delivery `5e901aa..82fdd47` (rewritten history; L8 fix is now `82fdd47`), plus review/status/record commits `2d12409`, `e534dee`, `9b8a7e9`. Diff base for the out-of-scope check: `5d2b0ec`. Working tree clean at start; all trial edits restored with `git checkout`, none committed. |
| **Supervisor (accepts)** | mzargham |
| **Acceptance record** | Verbal acceptance in chat, quoted verbatim in `work-packages/WP1-decisions.md`, after this report |

This is a complete third review from step 1 by a reviewer who did not build the work or write either earlier review. Every command below was run in this session (`unset VIRTUAL_ENV`, `uv run ...`). Gap IDs in this pass are prefixed `G3-` to avoid clashing with the G-5 and G-9 IDs already used in `WP1-decisions.md`.

## Deliverables

| ID | Verdict | Evidence |
|---|---|---|
| D-1 | met | `derivation/__init__.py`, `derivation/symbols.py` (98 lines): `make_symbols()` takes no size arguments; `SYMBOL_ASSUMPTIONS` present. |
| D-2 | met | `derivation/axioms.py` (194 lines): frozen `Axiom`; POSITED A0 to A7, INHERITED I1 to I6, REGULARITY R1, fallbacks F5 and F10; `role`, `failure_mode`, `fallback` fields. |
| D-3 | met | `derivation/lemma_01_homogeneity.py` through `lemma_10_extension.py`, ten modules with the default names. |
| D-4 | met | `derivation/run.py` (`CHAIN`, `run_chain`, `print_audit`, CLI). |
| D-5 | met | `tests/test_derivation.py` (701 lines): chain, per lemma, crosschecks, hygiene, I1, I2, L8 negative controls. |
| D-6 | met | `work-packages/WP1-decisions.md` holds the approval record (verbatim "OK") and the two later gap dispositions. |

## Requirements

| ID | Verdict | Evidence |
|---|---|---|
| R-1 | met, with wording gap (G3-3) | `symbols.py` read: d, n, K `Symbol(integer=True, positive=True)`; i, j, k; `IndexedBase` m, u, w, theta, beta (plus s, a, alpha, b, v, p, eps); tau, kappa, sigma, c, k_scale; `B = MatrixSymbol("B", d - 1, d)`; `simplex = Eq(Sum(w[j], (j, 1, d)), 1)`. Grep of `derivation/lemma_*.py` for `Symbol(`/`MatrixSymbol(`/`IndexedBase(` lines containing digits finds no size (only names such as `beta0`, `k0`, `j0`, `u_pt`). The `Identity(1)`/`ZeroMatrix(1, …)` block shapes in L8 are the 1x1 block. No x, y, z or a, b, c shared names. |
| R-2 | met | `test_load_bearing_symbol_assumptions_are_declared` passes. Trial (a): I inserted `zzz = sp.Symbol("zzz", positive=True)` into the returned namespace; the test failed: "AssertionError: zzz is positive but is not registered in SYMBOL_ASSUMPTIONS with a licensing axiom" (1 failed); restored with `git checkout derivation/symbols.py`. |
| R-3 | met | Ledger printed by `run.py`: A1 to A6 POSITED; I1 to I4 INHERITED with citations (Boyd & Vandenberghe §5.2; Kolmogorov SLLN / Billingsley; Rockafellar §13; Hoburg, Kirschen & Abbeel 2016); R1 REGULARITY. A5 reads "eps_j are i.i.d. N(0, sigma^2), independent across j, with sigma > 0"; I5 (MGF of independent sums, Billingsley) is the named ledger addition. `test_inherited_axioms_are_cited` passes (part of the 75). |
| R-4 | met except the L8 axiom list (G3-4) | All ten modules define `TITLE`, `STATEMENT`, `AXIOMS_USED`, `derive`, `verify` and a proved / not-proved docstring. Printed `axioms:` lines: L1 [A1,A2], L2 [A2,A3], L3 [A2,A3,R1], L4 [A1,A3], L5 [A3,I1,I2,I3,F5], L6 [A2,A5,I5], L7 [A1,A2], L8 [A7,I6], L9 [A1,A2,A4], L10 [A2,A6,I4,F10]. All are supersets of spec §6 except L8, where spec §6 lists [A2] and the code lists [A7, I6]; A2 (simplex) is not used by L8. `test_each_lemma_verifies` passes. |
| R-5 | met with documented weaknesses (G3-7); see "R-5 reading" | Each `verify` read against the R-5 list. All ten assert the stated identities with messages beginning "L<n> FAIL". |
| R-6 | met | `grep -niE 'logsumexp|LSE' derivation/`: LSE appears in `lemma_05_lse_lme.py` (17 lines), `lemma_08` (2, a docstring/comment), `run.py` (3, text), `axioms.py` (2), `sumtools.py` (2); no LSE fit objective anywhere. β is the log-mean-exp throughout. |
| R-7 | met | `uv run python derivation/run.py` exit 0; PASS for L1 to L10 with no sizes supplied; ends "ALL LEMMAS PASS." |
| R-8 | met | Output has DERIVED, POSITED, INHERITED (with citations), REGULARITY, FALLBACKS (F5, F10), "interpretive role" / "failure mode" on R1, F5, F10, a HEADLINE ("proved for symbolic d, n, K"; "The frontier reading of the balanced point requires R1") with one buys / when-it-fails line per condition, and "ALL LEMMAS PASS." |
| R-9 | met | `test_no_phantom_axioms`, `test_inherited_axioms_are_cited`, `test_every_used_axiom_resolves_and_all_tags_valid`, `test_every_axiom_is_used` pass (A0 excluded as structural). A1 to A6, I1 to I4, R1 each appear in some `AXIOMS_USED`. I1, I2, I3 are used in L5 as recorded remarks, not consumed by an assertion (O-3). |
| R-10 | met on substance; literal grep has hits (G3-6) | No `verify` loops over concrete sizes. `grep -n 'range(' derivation/*.py`: `lemma_08_helmert_chart.py:47` (`for b in range(2)`, indexing the 2x2 block grid), `lemma_03_gradient_kkt.py:101` (`for _ in range(12)`, iteration cap in a rewrite helper), `lemma_03:157,244` (the name `piece_in_range`). `test_fallbacks_are_declared` passes. |
| R-11 | met | `pytest tests/test_derivation.py -k crosscheck`: 31 passed, 43 deselected. The Helmert realization at d = 4 is a labelled realization check. |
| R-12 | met | `-k lp_duality`: 3 passed. |
| R-13 | met | `-k replication`: 1 passed. |
| R-14 | met | `grep -nE 'numpy|scipy|import random|random\.' derivation/*.py`: no matches. |
| R-15 | met, with out-of-scope observations (G3-1, G3-2, G3-8) | `uv run pytest`: 75 passed in 7.95 s. `uv run ruff check .`: All checks passed. `uv run ruff format --check .`: 35 files already formatted. `uv lock --check`: Resolved 153 packages. `git diff --stat 5d2b0ec..HEAD`: 22 files, 2582 insertions; covers `derivation/`, `tests/test_derivation.py`, `pyproject.toml` (`pythonpath = [".", "src"]`), `work-packages/`, plus `.github/workflows/test.yml` and the spec file (see Outside the scope). No `src/` change. |
| R-16 | **met** (was not met in the second pass) | `git log --format=%B \| grep -ciE 'co-authored-by\|generated with'` over 5d2b0ec..HEAD returns 0, and over ALL commit messages on main also returns 0. `git log --format='%an\|%cn\|%h' 5d2b0ec..HEAD`: all 14 commits have author and committer "Michael Zargham". The rewritten L8 commit is `82fdd47`; `bd953c4` and `cc2453a` are no longer on any branch (`git branch -a --contains bd953c4` empty). |

### R-5 reading: do the `verify` functions prove the claim for symbolic d, n, K?

I read each `verify` and judged whether it proves the claim or is weaker.

- **L1, L2, L7, L9: proved.** `Sum`/`Product` over `(j, 1, d)` rewritten to exp of a Sum, constants factored out, the simplex equation substituted, all at symbolic d. No weakness found.
- **L6: proved given I5.** The Normal MGF comes from `sympy.stats`; the product over symbolic d rests on the cited, declared I5.
- **L3: weaker on the KKT step.** The directional derivative is obtained by SymPy through the symbolic `Sum`s and asserted equal to Σ_i p_i (v·u_i) and to Σ_j v_j (Σ_i p_i u_ij) (sum swap), so ∇J = Σ_i p_i u_i is proved for symbolic d, n. The balanced KKT claim is conditional: `verify` takes stationarity along e_{j0} as the premise (R1 plus the first-order condition), shows the `KroneckerDelta` instantiation gives G(j0) − λ, and concludes equal components. Interiority of the minimizer is not proved; the docstring says so, and R1 is declared with a role and failure mode.
- **L4: derivative identity proved; sign step on unlinked placeholders.** The second directional derivative equals τ·Var_p(v·u) is asserted through the sums; the Var to double-sum identity is asserted with `p_normalized`, with a control (`!= 0`) showing the identity fails without normalization. The nonnegativity step runs on real placeholder families `a_r`, `s_r` that are not linked in code to the `u`, `w`, `v` of step 1; the docstring says this ("explicit modelling step, not a fallback") and attributes realness to A1. Documented accurately, but the link is prose only.
- **L5: identities proved; limits by a squeeze under F5.** LSE = LME + (log n)/τ is asserted. The bounds T ∈ [1, n] are assembled from `solveset` facts on one exp term, `Sum(1) = n`, and the F5 hypothesis, with the final inequality chain written as comments rather than one machine-checked inequality over the Sum. The two bounding functions are constant in the Sum, and `sympy.limit` handles each; τ → 0 goes through N(0) = 0 and N′(0) = mean. "Strict for n ≥ 2" is in the STATEMENT, the docstring and the spec line, but `verify` asserts only the floor `lse_minus_M_floor == 0` (LSE − max ≥ 0); strictness is argued in a comment.
- **L10: same shape as L5 under F10.** Shift equivariance, K = 1 reduction (substituted into the abstract expression), posynomial form, and the K-term squeeze assembled as in L5.
- **L8: genuinely derived.** See next section.

### L8 round trip, read closely

I read `lemma_08_helmert_chart.py` in full and the six L8 tests.

- (a) Z(u + c1) = Z(u): `block_collapse((B*(u + c*one)).expand())` yields terms; only the term whose matrix product equals `B*one` is dropped (that is exactly A7's B1 = 0); the remainder is asserted `== Z`.
- (b) Q Q^T = I: `Q = BlockMatrix([[B],[1^T/sqrt(d)]])`, `block_collapse(Q*Q.T)` gives the four blocks; `B*B.T` is replaced by `Identity(d-1)` (A7 orthonormality), the off-diagonal blocks (`B*1/√d`, `1^T B^T/√d`, matched through scalar coefficients) by `ZeroMatrix` (A7 kernel), and (1/d)·1^T 1 is simplified to the 1x1 identity by SymPy. `verify` asserts each block with strict `==` (the only `or`/`in` tolerance is between two SymPy spellings of the same zero block, `ZeroMatrix(...)` or `0`).
- (c) Q^T Q = I via I6: `roundtrip_holds` returns False unless the Gram blocks equal the identity first; only then does it rewrite `Q^T Q` to `Identity(d)` (applied only when `use_I6` is on) and compute `(Q^T Q) u` to compare with `u`. `verify` separately asserts the expansion `Q^T Q == B^T B + OneMatrix(d, d)/d`. The test file has `test_L8_roundtrip_derived_positive` and three negative controls (`..._fails_without_orthonormality`, `..._fails_without_kernel`, `..._fails_without_I6`) that pass, so the round trip fails when A7 (either part) or I6 is removed. No self-comparison and no permissive `or` that can mask a false result.
- Residual, not defects: the bridge from "B^T Z + ell 1" (STATEMENT) to "(Q^T Q) u" (code) is matrix associativity, not asserted separately; existence of a B satisfying A7 for every d is not proved (docstring says so; the d = 4 Helmert check is the labelled realization check). I6 is applied by whole-expression replacement under a hypothesis already checked, which is the intended meaning of the axiom.

### Trial (b): broken formulas (restored with `git checkout derivation`, never committed)

| Lemma | Edit | Result |
|---|---|---|
| L3 | stationarity claim `G(J0) - LAM` changed to `G(J0) - 2*LAM` | `AssertionError: L3 FAIL: stationarity along e_{j0}` |
| L4 | second-derivative claim `tau * Var` changed to `2 * tau * Var` | `AssertionError: L4 FAIL: second directional derivative != tau * Var_p(v.u)` |
| L8 | A7 orthonormality substituted as `2*Identity(d-1)` | `AssertionError: L8 FAIL B B^T != I` |
| L8 | A7 kernel rewrite disabled (`if False:` in place of `if prod == B * one:`) | `AssertionError: L8 FAIL Z(u + c 1) != Z(u)` |

`git status --short` was empty after each restore, and the full suite then gave 75 passed. (The second pass additionally broke L1 and L10; I did L3 and L4, the two the brief asked for, and both L8 halves.)

## Definition of good enough

| Item | Verdict | Evidence |
|---|---|---|
| Deliverables D-1 to D-6 exist at the stated paths | met | Table above. |
| R-1 to R-16 pass as checked, with evidence | met, with wording gaps | Every requirement passes as run; R-4's L8 axiom list differs from spec §6 (G3-4), R-1 and R-10 have wording gaps (G3-3, G3-6). R-16 now passes. |
| Every lemma L1 to L10 passes in abstract form and every fallback is declared in the ledger (R-10) | met | `run.py`: PASS L1 to L10, FALLBACKS lists F5 and F10 with role and failure mode. The L3 KKT premise (R1), L4 placeholder reals (docstring) and the L5/L10 assembled squeeze (F5/F10) are stated conditions, not hidden ones. |
| Non-goals untouched | met | No `src/` change, no docs page, no `symproof` import (`grep symproof` finds comments and docstrings only), no enumeration in any `verify`, no K > 1 solver or kernels, no bibliography entries. |

Definition of good: docstrings give proved / not proved and cite symproof mimicry; broken formulas fail loudly with lemma numbers; every hypothesis (R1, F5, F10, A7, I5, I6) is explicit; the suite runs in about 8 s; the layout follows hc-marimo.

### Ledger entries judged

- **R1 (REGULARITY):** substantive. Role: makes the balanced KKT point a genuine interior frontier point so facet normal, improvement factors and elasticities read as trade-offs. Failure mode: at a vertex, edge or zero-normal-component facet the condition is only a subgradient inclusion, w* is not unique, some elasticities are undefined, and the reading degrades to the weaker invariant-form reading. Concrete, correct, and exactly what L3 assumes.
- **F5:** substantive. Role: gives a symbolic-n max symbol M (s_i ≤ M, s_{i0} = M) because SymPy has no symbolic-n max and cannot take limits through the `Sum`. Failure mode: if M is only a non-attained upper bound the lower squeeze bound is lost and the limit is only an upper bound. Matches the code.
- **F10:** substantive, same structure over K terms and κ (lower bound M − (log K)/κ). Matches the code.

## Outside the scope

- **Out-of-scope changes:**
  - `.github/workflows/test.yml` (not a deliverable). Two driver changes: `0d2f0bd` (checkout@v5, setup-uv@v7, `ubuntu-24.04` pin, removed an invalid input) and `9b8a7e9` (new step "No AI attribution lines in commit messages", `fetch-depth: 0`, runs `git log --format=%B | grep -ciE 'co-authored-by|generated with'` and fails if non-zero). I read the file: it is syntactically ordinary and does what it says. Observations only: it scans the entire history on every run, so any future commit message that merely mentions those phrases fails CI forever until history is rewritten; it checks messages only, not authorship or file content; it is a policy change to repository CI that the scope did not list.
  - `derivation/sumtools.py` (36 lines, helper; not a listed deliverable).
  - Spec file `docs/superpowers/specs/2026-11-07-posynomial-invariant-form-design.md`, one line (L5: "LSE − max ≥ 0 (strictly > 0 for n ≥ 2)"), made as the approved "Fix L8" disposition. The scope says no change to spec §4 or §6.
  - Axioms beyond spec §6: A0 (sizes, anticipated), A7 (chart, anticipated), I5 (named in advance), I6 (new, introduced by the L8 fix, covered by the recorded "Fix L8" disposition), F5, F10 (allowed by the defaults).
  - Permitted: `pyproject.toml` (`pythonpath`), `work-packages/` (including the README Status row).
- **Non-goals touched:** none.

## Observations (not counted as failures)

- O-1. The README Status row (`work-packages/README.md:52`) still names the pre-rewrite SHAs: delivery `5e901aa..bd953c4` and review `cc2453a`. Both objects are no longer on `main` (the rewrite produced `82fdd47` and `2d12409`; later `e534dee` updated nothing in this row that I could find). The row should name `5e901aa..82fdd47` and the current review commit.
- O-2. L5 strictness for n ≥ 2 is argued in a comment, in the STATEMENT, docstring and spec line, but `verify` asserts only the ≥ 0 floor.
- O-3. I1, I2, I3 are "used" in L5 as recorded remarks (in `AXIOMS_USED`, no assertion consumes them); I1 and I2 are numerically checked in pytest as the scope requires.
- O-4. Lemma-local real or integer Symbols (`beta0`, `LV`, `x`, `t`, `l`, `j0`, `k0`, `lambda`, `a_r`, `s_r`) sit outside `SYMBOL_ASSUMPTIONS`; the hygiene test polices only the shared namespace.
- O-5. The L3 KKT premise, L4 placeholder real families and L5/L10 squeeze are accurately documented, but they are weaker than a single closed derivation; WP6 should carry them as stated conditions.

## Open decisions (for the supervisor)

- **G3-1.** Out-of-scope CI workflow changes in `.github/workflows/test.yml` (`0d2f0bd` action pins; `9b8a7e9` attribution check scanning the whole history). — options: accept as is / fix before acceptance / follow-up work package
- **G3-2.** Added file and axioms beyond spec §6: `derivation/sumtools.py`; A0, A7, I5, I6, F5, F10. — options: accept as is / fix before acceptance / follow-up work package
- **G3-3.** R-1 wording: extra shared symbols (i0, s, a, alpha, b, v, p, eps, t, M, simplex_theta, p_normalized) beyond the R-1 list. — options: accept as is / fix before acceptance / follow-up work package
- **G3-4.** R-4: L8 `AXIOMS_USED` is [A7, I6] against spec §6's [A2]; A2 is not used by L8. — options: accept as is / fix before acceptance / follow-up work package
- **G3-5.** Ledger placement: F5/F10 are tagged POSITED with `fallback=True` but printed only under FALLBACKS, not under POSITED. Roles and failure modes are substantive. — options: accept as is / fix before acceptance / follow-up work package
- **G3-6.** R-10 literal grep: `range(` hits in helpers (`lemma_03:101` iteration cap, `lemma_08:47` block-grid indexing); neither loops over a concrete size. — options: accept as is / fix before acceptance / follow-up work package
- **G3-7.** Remaining weak spots in R-5, documented in docstrings and ledger: L3 balanced-KKT premise (R1 plus first-order condition); L4 sign step on unlinked real placeholders; L5/L10 squeeze assembled by comment under F5/F10; L5 strictness for n ≥ 2 in STATEMENT/spec but not asserted. This touches a good-enough item (R-5). — options: accept as is / fix before acceptance / follow-up work package
- **G3-8.** Minor observations: O-1 (README Status row names SHAs that no longer exist on main), O-3 (I1 to I3 as remarks), O-4 (helper-local symbols), the one-line spec edit to §6, and the CI history-scan behaviour noted under G3-1. — options: accept as is / fix before acceptance / follow-up work package

Resolved in earlier rounds and verified closed in this pass: G-5 "Fix L8 before acceptance" (L8 now derived, three negative controls pass) and G-9 "Rewrite the message and force-push" (R-16 returns 0 over all history).

## Gap dispositions

Each gap (any item not met, any out-of-scope change, touched non-goal or observation) is resolved through the
decision loop (`~/.claude/skills/CLAUDE.md`). The decision records are in the PR thread, or in `WPn-decisions.md`
next to the scope if the project has no PRs.

| Gap | Disposition (accept as is / fix before acceptance / follow-up work package) | Reason or follow-up |
|---|---|---|
| G3-1 CI workflow changes outside deliverables | pending | pending |
| G3-2 sumtools.py, A0/A7/I5/I6/F5/F10 | pending | pending |
| G3-3 extra shared symbols | pending | pending |
| G3-4 L8 axiom list vs spec | pending | pending |
| G3-5 F5/F10 ledger placement | pending | pending |
| G3-6 `range(` grep hits | pending | pending |
| G3-7 remaining weak spots L3/L4/L5/L10 | pending | pending |
| G3-8 minor observations | pending | pending |

## Recommendation

Provisional, pending the gap dispositions: recommend acceptance with the listed gaps noted. Every requirement R-1 to R-16 passes as run in this session: 75 tests green, `run.py` PASS L1 to L10 with exit 0, ruff and lock clean, the hygiene trial and four broken-formula trials (L3, L4, and both halves of L8) fail loudly with lemma numbers, R-16 now returns 0 over all history with all WP1 commits authored by Michael Zargham, and the L8 round trip is genuinely derived (Q Q^T = I from A7 block-wise, Q^T Q = I via I6, three negative controls, no self-comparison). The remaining weak spots (G3-7) are accurately documented as stated conditions and affect the strength, not the honesty, of R-5; the supervisor should read them as such. The other gaps are scope-hygiene items that do not affect any good-enough item. If any gap is dispositioned "fix before acceptance", the whole review reruns.

Acceptance is the supervisor's act, recorded as named above. This report does not accept the work.

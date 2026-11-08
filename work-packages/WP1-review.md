# WP1 — Review report (rerun after the L8 fix)

| | |
|---|---|
| **Scope of work** | `work-packages/WP1-scope-of-work.md` (approved at 0b181d7, draft 3) |
| **Scope approval verified** | Verbal approval recorded in `work-packages/WP1-decisions.md` (section "Scope approval", commit 5d2b0ec): supervisor (mzargham), verbatim "OK", 2026-11-07; defaults list approved as one item; open decisions none. The project has no PRs; this is the recorded act the scope names. The record is typed by the agent, so the review cannot confirm the chat itself. The same file records the first review's G-5 disposition, verbatim "Fix L8 before acceptance" (commit 6ca990e), which this rerun follows. |
| **Work reviewed** | `main` at `bd953c4`: delivery `5e901aa..HEAD` (11 commits since the approval record 5d2b0ec, including the L8 fix `bd953c4`). Working tree clean at start; all trial edits restored with `git checkout`. |
| **Supervisor (accepts)** | mzargham |
| **Acceptance record** | Verbal acceptance in chat, quoted verbatim in `work-packages/WP1-decisions.md`, after this report |

This is a complete rerun from step 1 by a reviewer who did not build the work. Every command below was run in this session (`unset VIRTUAL_ENV`, `uv run ...`).

## Deliverables

| ID | Verdict | Evidence |
|---|---|---|
| D-1 | met | `derivation/__init__.py`, `derivation/symbols.py` (98 lines): `make_symbols()` with no size arguments, `SYMBOL_ASSUMPTIONS` (15 tags). |
| D-2 | met | `derivation/axioms.py`: frozen `Axiom`; POSITED A0–A7, INHERITED I1–I6, REGULARITY R1, fallbacks F5, F10; `role`, `failure_mode`, `fallback` fields. |
| D-3 | met | `derivation/lemma_01_homogeneity.py` … `lemma_10_extension.py`, ten modules with the default names. |
| D-4 | met | `derivation/run.py` (`CHAIN`, `run_chain`, `print_audit`, CLI). |
| D-5 | met | `tests/test_derivation.py` (701 lines): chain, per lemma, crosschecks, hygiene, I1, I2. |
| D-6 | met | `work-packages/WP1-decisions.md` holds the approval record (verbatim "OK") and the round-1 gap disposition. |

## Requirements

| ID | Verdict | Evidence |
|---|---|---|
| R-1 | met | `symbols.py` read: d, n, K are `Symbol(integer=True, positive=True)`; i, j, k (and i0); `IndexedBase` m, u, w, theta, beta, plus s, a, alpha, b, v, p, eps; tau, kappa, sigma, c, k_scale; `B = MatrixSymbol("B", d - 1, d)`; `simplex = Eq(Sum(w[j], (j, 1, d)), 1)`. Grep of `derivation/lemma_*.py` for integer literals in `Symbol`/`MatrixSymbol`/`Eq` finds no size; the only digits are `Identity(1)`, `ZeroMatrix(1, …)` block shapes in L8 and `solve(...)[0]` in L7. No x, y, z names. Extra shared symbols: see G-3. |
| R-2 | met | `test_load_bearing_symbol_assumptions_are_declared` passes. Trial (a): I added `zzz = sp.Symbol("zzz", positive=True)` to the namespace in `symbols.py`; the test failed (`assert ('zzz', 'positive') in {...}`, tests/test_derivation.py:78); restored with `git checkout`. |
| R-3 | met | A1–A6 POSITED, I1–I4 INHERITED with the required citations (printed in the ledger: Boyd & Vandenberghe §5.2; SLLN, Kolmogorov / Billingsley; Rockafellar §13; Hoburg, Kirschen & Abbeel 2016), R1 REGULARITY. A5 reads "eps_j are i.i.d. N(0, sigma^2), independent across j, with sigma > 0"; I5 (MGF of independent sums, Billingsley) is the named ledger addition. `test_inherited_axioms_are_cited` passes. |
| R-4 | met except L8's axiom list | All ten modules define `TITLE`, `STATEMENT`, `AXIOMS_USED`, `derive`, `verify` and a proved / not-proved docstring. `AXIOMS_USED` supersets spec §6 for L1 [A1,A2], L2 [A2,A3], L3 [A2,A3,R1], L4 [A1,A3], L5 [A3,I1,I2,I3,F5], L6 [A2,A5,I5], L7, L9, L10 [A2,A6,I4,F10]. L8 is `["A7","I6"]`, whereas spec §6 lists [A2] and R-4 says "as a minimum". A2 (the simplex) is genuinely unused by L8, so the spec list looks like a spec slip (G-4). `test_each_lemma_verifies` passes. |
| R-5 | met with documented weaknesses; see "R-5 reading" below | Each `verify` read against the R-5 list. All ten assert the stated identities with "L<n> FAIL" messages. |
| R-6 | met | `grep -niE 'logsumexp|LSE' derivation/` (26 hits): LSE appears in L5 and L10 only (plus axioms/run text). β is the LME everywhere else. |
| R-7 | met | `uv run python derivation/run.py` exits 0; PASS for L1–L10 with no sizes supplied. |
| R-8 | met | Output has DERIVED, POSITED, INHERITED (with citations), REGULARITY, FALLBACKS (F5, F10), "interpretive role" / "failure mode" on each REGULARITY and FALLBACKS entry, a HEADLINE stating symbolic d, n, K and that the frontier reading requires R1, and the closing "ALL LEMMAS PASS." |
| R-9 | met | `test_no_phantom_axioms`, `test_inherited_axioms_are_cited`, `test_every_used_axiom_resolves_and_all_tags_valid`, `test_every_axiom_is_used` pass (A0 is excluded as STRUCTURAL). A1–A6, I1–I4, R1 each appear in some `AXIOMS_USED`. Note I1, I2, I3 are used as recorded remarks in L5 (not consumed by an assertion). |
| R-10 | met on substance; literal grep has hits (G-7) | No lemma `verify` loops over concrete sizes. `grep range\(` hits: `lemma_03:101` (`for _ in range(12)` iteration cap in `linearize`), `lemma_08:47` (`for b in range(2)` indexing the 2x2 block matrix), plus the name `piece_in_range`. `test_fallbacks_are_declared` passes. |
| R-11 | met | `pytest -k crosscheck`: 31 passed. `test_crosscheck_L8_helmert_realization_d4` checks the Helmert realization as a labelled realization check. |
| R-12 | met | `pytest -k lp_duality`: 3 passed (d = 2, 3, 4). |
| R-13 | met | `pytest -k replication`: 1 passed. |
| R-14 | met | `grep -nE 'numpy|scipy|random'` in `derivation/` finds only the word "random" in an `axioms.py` string (the MGF axiom text, "random variables"); no imports. |
| R-15 | met | `pytest -q`: 75 passed in 8.8 s. `ruff check .`: All checks passed. `ruff format --check .`: 35 files already formatted. `uv lock --check`: Resolved 153 packages. `git diff --stat 5d2b0ec..HEAD` covers `derivation/`, `tests/test_derivation.py`, `pyproject.toml` (`pythonpath = [".", "src"]`), `work-packages/`, plus two unlisted paths: `.github/workflows/test.yml` and the spec file (G-1, G-8). No `src/` change. |
| R-16 | **not met** | All 11 commits since 5d2b0ec are authored and committed by Michael Zargham. `git log --format=%B 5d2b0ec..HEAD \| grep -ciE 'co-authored-by\|generated with'` returns **1**: commit `bd953c4` (the L8 fix) ends with `Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>`. Its parent commits are clean. (G-9) |

### R-5 reading: do the `verify` functions prove the claim for symbolic d, n, K?

I read each `verify` and judged whether it proves the claim or is weaker.

- **L1, L2, L7, L9: proved.** `Sum`/`Product` over `(j, 1, d)` rewritten to exp of a Sum, constants factored out, the simplex equation substituted. L1 asserts V(km) = kV(m), V(m/V) = 1 and V(m e^-β) = e^-β V(m), and also asserts that homogeneity passes through Σ w_j. No weakness found.
- **L6: proved given I5.** The Normal MGF is computed by `sympy.stats`; the product over symbolic d relies on the cited I5, which is declared.
- **L3: sub-claim 1 and 2 proved, KKT is conditional.** The directional derivative is obtained by SymPy differentiating through the symbolic `Sum`s and is asserted equal to Σ p_i (v·u_i); the swap of sums gives the gradient. The balanced KKT step is not derived. `verify` shows that the `KroneckerDelta` instantiation of the stationarity expression gives G(j0) − λ, and then stores `Eq(G(J0), LAM)` in ctx. The premise "w* is an interior stationary point" is R1 plus the textbook first-order condition; the docstring says so plainly ("takes stationarity as the hypothesis ... does not prove that the minimizer is interior"). Accurately documented; R1 is declared, so this is a stated condition, not a hidden one.
- **L4: derivative identity proved, sign step uses placeholders.** The second derivative equals τ·Var_p is asserted through the sums; the variance to double-sum identity is asserted with `p_normalized` and a control showing the identity fails without it. The nonnegativity step runs on real placeholder families `a_r`, `s_r` that are not linked in code to the `u`, `w`, `v` of the first step; the docstring states this ("explicit modelling step, not a fallback") and attributes realness to A1. Accurately documented; the link is argued in prose only.
- **L5: identities proved, limits proved via a squeeze under F5.** LSE = LME + (log n)/τ is asserted. The bounds T ∈ [1, n] are assembled from `solveset` facts about a single exp term (exp(x) > 0; exp(x) ≤ 1 iff x ≤ 0), `Sum(1) = n`, and the F5 hypothesis, with the final inequality chain written in comments rather than as one machine-checked inequality over the Sum. The limits are `sympy.limit` of the two constant-in-the-Sum bounds; τ → 0 goes through N(0) = 0 and N′(0) = mean. The conclusion about the real maximum holds exactly when M is attained (F5); this is the ledger's failure mode for F5 and is accurate. The spec note and STATEMENT now read "LSE − max ≥ 0 (strict for n ≥ 2)"; the docstring explains it (equality iff n = 1) and the strictness is argued in a comment, but `verify` asserts only the ≥ 0 floor (`lse_minus_M_floor == 0`), not the strict part.
- **L10: same shape as L5 under F10.** Shift equivariance, K = 1 reduction (substituted into the abstract expression) and the posynomial form are asserted; the K-term squeeze is assembled the same way as L5. Accurately declared.
- **L8: now genuinely derived.** Details below.

#### L8, in particular

I read `lemma_08_helmert_chart.py` and the tests that guard it.

- (a) Z(u + c1) = Z(u): the raw `B*(u + c*1)` is expanded with `block_collapse`; the term `c*B*1` is removed only by a rewrite that matches `B*OneMatrix`, which is exactly A7's B1 = 0; the result is asserted equal to `B*u`. Trial: replacing that rewrite with `if False:` made `run.py`/`test_full_chain_runs` fail with "L8 FA…" (message "L8 FAIL Z(u + c 1) != Z(u)").
- (b) Q Q^T = I: `Q = BlockMatrix([[B],[1^T/sqrt(d)]])`, `block_collapse(Q*Q.T)` gives blocks B B^T, B 1/√d, 1^T B^T/√d, 1^T 1/d; the first is replaced by `Identity(d-1)` (A7 orthonormality), the off-diagonal blocks by zero (A7 kernel), and (1/d)·1^T1 = 1 is simplified by SymPy. Trial: changing the substitution to `2*Identity(d-1)` made the chain fail with an "L8 FAIL" assertion.
- (c) Q^T Q = I by I6 (square matrix, left inverse is right inverse, cited to Horn & Johnson) and only then `(Q^T Q) u = u`. `roundtrip_holds` returns False unless the Gram blocks equal the identity first; it then rewrites Q^T Q to `Identity(d)` only under the `use_I6` switch, and `verify` separately asserts the expansion Q^T Q = B^T B + (1/d)·11^T. The three negative controls (`test_L8_roundtrip_fails_without_orthonormality`, `..._without_kernel`, `..._without_I6`) pass, i.e. the round trip fails when either A7 part or I6 is switched off, so it is no longer a self-comparison.
- Residual looseness, not a defect: the zero-block tests use `in (ZeroMatrix(...), 0)`, which tolerates two SymPy representations of zero (it is not an escape hatch for a false result; the negative controls show the check fails). The reading "B^T Z + ell·1" in the STATEMENT versus "(Q^T Q)u" in code is bridged by matrix associativity, which is not asserted separately. Existence of a B satisfying A7 for every d is not proved (docstring says so; Helmert realization at d = 4 is the labelled realization check). I6 and A7 are in the ledger with citations / roles.

Verdict on L8: genuinely derived from A7 and I6 with no self-comparison and no permissive `or`-escape that could mask a failure.

#### Trial (b), broken formulas (restored with `git checkout`, never committed)

| Lemma | Edit | Result |
|---|---|---|
| L1 | `Vt = Vk.subs(k, sp.exp(-2 * beta0))` | `AssertionError: L1 FAIL: V(m e^-beta) != e^-beta V(m)`; `test_full_chain_runs` failed |
| L8 | disabled the `B*1 = 0` rewrite (`if False: continue`) | chain fails at L8 ("L8 FAIL Z(u + c 1) != Z(u)") |
| L8 | Identity substitution altered to `2*Identity(d-1)` | chain fails at L8 ("L8 FAIL B B^T != I") |
| L10 | `ceil = log(n_upper + 1)/kappa` | chain fails at L10 ("L10 FAIL: Phi - max <= log K / kappa") |

`git status --short` was empty after each restore.

## Definition of good enough

| Item | Verdict | Evidence |
|---|---|---|
| Deliverables D-1 to D-6 exist at the stated paths | met | Table above. |
| R-1 to R-16 pass as checked, with evidence | not met as written | R-16 fails on `bd953c4` (one attribution trailer); R-4 has the L8 list difference (G-4); R-10 and R-1 have wording gaps (G-3, G-7). Everything else passes on re-run. |
| Every lemma L1–L10 passes in abstract form and every fallback is declared in the ledger (R-10) | met | `run.py`: PASS L1–L10, FALLBACKS lists F5 and F10 with role and failure mode. The L3 KKT premise (covered by R1), L4 placeholder reals (docstring) and the L5/L10 assembled squeeze (F5/F10) are conditions stated in docstrings and the ledger, not hidden. |
| Non-goals untouched (no `src/` code, no docs pages, no `symproof` dependency, no enumeration proofs) | met | No `src/` change in `git diff --stat`; no docs page; `grep symproof` finds comments and docstrings only; no loop over concrete sizes in any `verify`. |

Definition of good: docstrings give proved / not proved and cite symproof mimicry; broken formulas fail loudly with lemma numbers (trials above); every hypothesis (R1, F5, F10, A7, I5, I6) is explicit; the whole suite runs in about 9 s.

### Ledger entries judged

- **R1 (REGULARITY):** substantive. Role: makes the KKT balanced point a genuine interior frontier point so facet normal, improvement factors and elasticities read as trade-offs. Failure mode: at a vertex, an edge or a facet with a zero normal component the gradient condition is only a subgradient inclusion, w* not unique, some elasticities undefined, reading degrades to the weaker invariant-form reading. Concrete, correct, and matches what L3 actually assumes.
- **F5:** substantive. Role: gives a symbolic-n max symbol M with s_i ≤ M and s_{i0} = M, since sympy has no symbolic-n max and cannot take limits through the `Sum`. Failure mode: if M is only an upper bound that is not attained, the lower squeeze bound is lost and only an upper bound on the limit remains. Accurate to the code.
- **F10:** substantive, same structure over K terms and κ (lower bound M − (log K)/κ). Accurate to the code.

## Outside the scope

- **Out-of-scope changes:** `.github/workflows/test.yml` (checkout@v5, setup-uv@v7, `ubuntu-24.04` pin, invalid input removed; commit `0d2f0bd`); `derivation/sumtools.py` (36 lines, not a listed deliverable); the spec file `docs/superpowers/specs/2026-11-07-posynomial-invariant-form-design.md` (one line: L5 "LSE − max ≥ 0 (strictly > 0 for n ≥ 2)", a spec edit where the scope says "no change to spec §4 or §6"; made as the approved G-5 fix); `work-packages/README.md` Status row (permitted: Status table). Axioms beyond spec §6: A0 (sizes, anticipated in the defaults), A7 (chart, anticipated for L8), I5 (named in advance), I6 (new, introduced by the L8 fix, covered by the recorded "Fix L8" disposition), F5, F10 (allowed by the defaults).
- **Non-goals touched:** None. No `src/` code, no docs pages, no `symproof` dependency, no enumeration proofs, no K > 1 solver or kernels, no bibliography entries.

## Observations (not counted as failures)

- O-1. The README Status row still names delivery `5e901aa..2e2eafc` and review `dcfd527`, and does not include the L8 fix `bd953c4`.
- O-2. L5's "strict for n ≥ 2" is in the STATEMENT and the docstring but `verify` asserts only the ≥ 0 floor.
- O-3. I1, I2, I3 are "used" in L5 as recorded remarks (they are in `AXIOMS_USED` and the context, but no assertion consumes them); I1 and I2 are numerically checked in pytest as the scope requires.
- O-4. Lemma-local real `Symbol`s (`beta0`, `LV`, `logf`, `x`, `M`-style helpers) sit outside `SYMBOL_ASSUMPTIONS`; the hygiene test polices only the shared namespace.
- O-5. L5/L10 squeeze, L3 KKT premise and L4 placeholder real families are accurately documented as weaker than a single closed derivation, but they are weaker; WP6 should carry them as stated conditions.

## Open decisions (for the supervisor)

- **G-1.** Out-of-scope `.github/workflows/test.yml` CI fix (`0d2f0bd`). — options: accept as is / fix before acceptance / follow-up work package
- **G-2.** Added file and axioms beyond spec §6: `derivation/sumtools.py`; A0, A7, I5, I6, F5, F10. — options: accept as is / fix before acceptance / follow-up work package
- **G-3.** R-1 wording: extra shared symbols (i0, s, a, alpha, b, v, p, eps, M, t, simplex_theta, p_normalized) beyond the R-1 list. — options: accept as is / fix before acceptance / follow-up work package
- **G-4.** R-4: L8 `AXIOMS_USED` is `["A7","I6"]`; spec §6 lists [A2]; A2 is not used by L8. — options: accept as is / fix before acceptance / follow-up work package
- **G-5.** Ledger placement: F5/F10 are tagged POSITED with `fallback=True` but printed only under FALLBACKS (not under POSITED). Roles and failure modes are substantive. — options: accept as is / fix before acceptance / follow-up work package
- **G-6.** R-10 literal grep: `range(` hits in helpers (`lemma_03:101` iteration cap, `lemma_08:47` block indexing); neither loops over a concrete size. — options: accept as is / fix before acceptance / follow-up work package
- **G-7.** Remaining weak spots in R-5, accurately documented in docstrings and ledger: L3 balanced-KKT premise (R1 plus first-order condition, not derived); L4 sign step on unlinked real placeholder families; L5 and L10 squeeze assembled by comment under F5/F10; L5 strictness for n ≥ 2 argued but not asserted. This touches a good-enough item (R-5). — options: accept as is / fix before acceptance / follow-up work package
- **G-8.** Observations O-1 to O-4 (stale Status row, spec text change to §6 line, helper-local symbols, I1–I3 as remarks). — options: accept as is / fix before acceptance / follow-up work package
- **G-9.** R-16 not met: commit `bd953c4` carries a `Co-Authored-By: Claude Sonnet 5.5` trailer. Fixing means rewriting that commit message (history rewrite on `main`), which only the supervisor can authorize. — options: accept as is / fix before acceptance / follow-up work package

## Gap dispositions

Each gap (any item not met, any out-of-scope change, touched non-goal or observation) is resolved through the
decision loop (`~/.claude/skills/CLAUDE.md`). The decision records are in the PR thread, or in `WPn-decisions.md`
next to the scope if the project has no PRs.

| Gap | Disposition (accept as is / fix before acceptance / follow-up work package) | Reason or follow-up |
|---|---|---|
| G-1 CI workflow change | pending | pending |
| G-2 sumtools.py, A0/A7/I5/I6/F5/F10 | pending | pending |
| G-3 extra shared symbols | pending | pending |
| G-4 L8 axiom list vs spec | pending | pending |
| G-5 F5/F10 ledger placement | pending | pending |
| G-6 `range(` grep hits | pending | pending |
| G-7 remaining weak spots L3/L4/L5/L10 | pending | pending |
| G-8 observations O-1 to O-4 | pending | pending |
| G-9 R-16 attribution trailer in bd953c4 | pending | pending |

## Recommendation

Provisional, pending the gap dispositions: recommend acceptance with the listed gaps noted, once G-9 is resolved. The substance is sound: all deliverables exist, every stated check ran green on re-run (75 tests, `run.py` PASS L1–L10 with exit 0, ruff and lock clean), the hygiene trial and four broken-formula trials fail loudly with lemma numbers, and the L8 defect from the first review is genuinely fixed (Q Q^T = I from A7 block-wise, Q^T Q = I via I6, three negative controls, no self-comparison). The remaining weak spots (G-7) are accurately documented as stated conditions. The one requirement that is plainly not met is R-16: the L8 fix commit `bd953c4` has an AI co-author trailer. If the supervisor dispositions G-9 as "fix before acceptance" (reword the commit), the whole review is rerun after that fix; if they accept it as is, the recommendation stands as above.

Acceptance is the supervisor's act, recorded as named above. This report does not accept the work.

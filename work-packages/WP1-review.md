# WP1 — Review report

| | |
|---|---|
| **Scope of work** | `work-packages/WP1-scope-of-work.md` (approved at `0b181d7`) |
| **Scope approval verified** | Verbal approval recorded in `work-packages/WP1-decisions.md` (section "Scope approval"): supervisor (mzargham), verbatim, "OK", 2026-11-07; disposition "approved; defaults list approved as one item; open decisions: none". The file exists and names the scope at `0b181d7`. The project has no PRs, so this is the recorded act the scope names. The record is typed by the agent; the review cannot confirm the chat itself. |
| **Work reviewed** | `main` at `2e2eafc`; delivery commits `5e901aa..2e2eafc` (7 commits), diff base `5d2b0ec`. Working tree clean before and after the reviewer trials. |
| **Supervisor (accepts)** | mzargham |
| **Acceptance record** | Verbal acceptance in chat, quoted verbatim in `work-packages/WP1-decisions.md`, after this report |

## Deliverables

| ID | Verdict | Evidence |
|---|---|---|
| D-1 | met | `derivation/__init__.py` (11 lines) and `derivation/symbols.py` (98 lines): `make_symbols()` (no size arguments) and `SYMBOL_ASSUMPTIONS` (15 entries). |
| D-2 | met | `derivation/axioms.py` (187 lines): frozen `Axiom` with `role`, `failure_mode`, `fallback`; tags POSITED/INHERITED/REGULARITY; A1–A6, I1–I4, R1 present, plus additions listed under G-2. |
| D-3 | met | `ls derivation/`: `lemma_01_homogeneity.py` … `lemma_10_extension.py`, all ten at the default names. |
| D-4 | met | `derivation/run.py` (134 lines): `CHAIN`, `run_chain`, `print_audit`, `main`; `sys.path` insertion present. |
| D-5 | met | `tests/test_derivation.py` (661 lines, 70 tests). All default test names in the scope collect (checked with `--collect-only`). |
| D-6 | met | `work-packages/WP1-decisions.md` exists (approval section; acceptance section says "pending"). |

## Requirements

| ID | Verdict | Evidence |
|---|---|---|
| R-1 | met (see G-3) | `symbols.py` inspected: d, n, K positive-integer symbols; i, j, k (plus i0); `IndexedBase` m, u, w, theta, beta (plus s, a, alpha, b, v, p, eps); tau, kappa, sigma, c, k_scale; `simplex = Eq(Sum(w[j],(j,1,d)),1)`; `B = MatrixSymbol("B", d-1, d)`. Grep of the lemma modules for integer size literals found only `1` (limits, bounds) and `K = 1` / `Integer(1)` in the L10 reduction and bound arithmetic; no concrete dimension. Lemma-local symbols (beta0, x, j0, k0, lambda) are outside `symbols.py`, as the defaults allow. |
| R-2 | met | `pytest -k load_bearing` passes. Trial (a): I added `zeta = Symbol("zeta", positive=True)` to the namespace; the test failed with "zeta is positive but is not registered in SYMBOL_ASSUMPTIONS with a licensing axiom". Restored with `git checkout`. |
| R-3 | met | A1–A6 POSITED, I1–I4 INHERITED with citations in the required form (I1 Boyd & Vandenberghe §5.2; I2 Kolmogorov SLLN / Billingsley; I3 Rockafellar §13; I4 Hoburg, Kirschen & Abbeel 2016), R1 REGULARITY. A5 reads "eps_j i.i.d. N(0, sigma^2), independent across j, with sigma > 0". I5 (MGF of independent sums, Billingsley) is the cited ledger item. `test_inherited_axioms_are_cited` passes. |
| R-4 | met, with discrepancies (G-4) | All ten modules define TITLE, STATEMENT, AXIOMS_USED, derive, verify and a "does NOT prove" docstring (script check printed True for all). Axiom lists are supersets of the spec minimum except L8: spec says [A2], delivered `["A7"]` (A2 absent); L4 delivers [A1, A3], L1/L7 [A1, A2], L2 [A2, A3], L5 [A3 + I1, I2, I3, F5], L6 [A2, A5, I5], L9 [A1, A2, A4], L10 [A2, A6, I4, F10]. `test_each_lemma_verifies` passes. |
| R-5 | met for the identities; weaker on several sub-claims (G-5) | See the per-lemma reading below. |
| R-6 | met | `grep -i logsumexp\|LSE derivation/`: LSE appears only in `lemma_05` (and L10 as Phi_K, which is the log-sum-exp by definition). β is log-mean-exp (`log(T_raw/n)`) throughout; the fit objective in L2/L3/L4 is `log(Sum(...)/n)/tau`. |
| R-7 | met | `uv run python derivation/run.py` exit 0; PASS for L1–L10; ends "ALL LEMMAS PASS."; no concrete d, n, K supplied. |
| R-8 | met | Output contains the ASSUMPTION AUDIT with DERIVED, POSITED, INHERITED (with citations), REGULARITY (R1 with "interpretive role" and "failure mode"), FALLBACKS (F5, F10 with both fields), HEADLINE (symbolic d, n, K; frontier reading requires R1; role and failure mode of R1, F5, F10), closing "ALL LEMMAS PASS." The ledger prints once. Quality of the entries is judged under G-6. |
| R-9 | met | `pytest` selectors `test_no_phantom_axioms`, `test_inherited_axioms_are_cited`, `test_every_used_axiom_resolves_and_all_tags_valid`, `test_every_axiom_is_used` all pass (full suite 71 passed). A0 is exempt through a `STRUCTURAL` tuple (G-2). |
| R-10 | partly met (G-7) | No step is replaced by enumeration; F5 and F10 are stated, tagged and shown in FALLBACKS and HEADLINE; `test_fallbacks_are_declared` passes. The scope's grep for `range(` inside `derivation/` is not clean: `lemma_03:101` `for _ in range(12)` (fixed-point iteration cap in `linearize`, not a size), `lemma_08:44` and `:56` (`range(len(facs)-1)`, `range(2)` over expression factors and block indices). None loops over a concrete d, n or K and none sits in a `verify` body (the L3 and L8 ones are helpers called from `verify`/`derive`). |
| R-11 | met | `pytest -k crosscheck`: 31 passed (L1–L10 over (2,2,1), (3,3,2), (4,3,3), plus the Helmert d=4 realization check `test_crosscheck_L8_helmert_realization_d4`). |
| R-12 | met | `pytest -k lp_duality`: 3 passed (d = 2, 3, 4; tolerance `< 1e-7`). |
| R-13 | met | `pytest -k replication`: 1 passed (1e-9 on J, 1e-6 on w*). |
| R-14 | met | `grep -E 'numpy\|scipy\|random' derivation/*.py` hits only the word "random" in the A5 and I5 statements in `axioms.py`; no imports. |
| R-15 | met | `pytest`: 71 passed in 8.2 s. `ruff check .`: All checks passed. `ruff format --check .`: 34 files already formatted. `uv lock --check`: Resolved 153 packages, exit 0. `git diff --stat 5d2b0ec..HEAD`: `derivation/*`, `tests/test_derivation.py`, `pyproject.toml` (1 line), plus `.github/workflows/test.yml` (outside the list, G-1). `work-packages/` changed only by files committed before the base; the Status table row for WP1 still reads "in progress". |
| R-16 | met | `git log 5d2b0ec..HEAD --format=%B \| grep -ciE 'co-authored-by\|generated with'` returns 0; all 7 commits authored "Michael Zargham". |

### R-5: lemma-by-lemma reading of `verify`

Trial (b): changing the L9 target exponent from `w*alpha` to `w+alpha` made `run.py` abort with "AssertionError: L9 FAIL: V != e^{w.b-beta} prod (a_j+s_j)^{w_j alpha_j}", and 6 tests failed plus 30 fixture errors in the suite. Doubling the L5 offset gave "L5 FAIL: LSE - LME != log(n)/tau". Both restored; tree clean.

- **L1** strong. V(km)=kV, V(m/V)=1, V(m e^-beta) = e^-beta V proved with `Sum`/`Product` over (j,1,d), simplex substituted; a check that the simplex sum is load-bearing.
- **L2** strong. Linearity plus simplex over symbolic d and n; log of a positive sum.
- **L3** mixed. The gradient identity (directional derivative equals the softmax mean, swap of sums, arbitrary v) is genuinely derived for symbolic d, n. The balanced-KKT part is weak: the stationarity equation of the Lagrangian is taken as the hypothesis (docstring says so), and the verify checks only that along e_j0 the delta sum reduces to G(j0) − λ and that two such components differ trivially. R1 is cited in `AXIOMS_USED` but no code step uses it as a hypothesis. It is honestly documented, but the claim "components of U^T p equal at an interior minimizer" is not proved from the objective.
- **L4** mixed. The second directional derivative equals τ·Var_p is derived by SymPy through the Sums. The double-sum identity uses the carried normalization and a negative control. The final sign argument runs on placeholder real families (`a_r`, `s_r`) and `p_r`, not on the actual `p_def`/`sv` of the lemma; the link "s_i = v·u_i is real" is argued in prose (A1), not enforced by the code. It proves nonnegativity for any real a, s, which is the right general fact, but the connection to the objective is by docstring.
- **L5** mixed. Offset, `mean <= LME` (tangent line), and the τ→0 limit (via N'(0) = mean, since `sympy.limit` cannot take Sums) are derived. The bounds `T in [1, n]` and `LME <= max` rest on the max symbol M (F5) and on constant arithmetic (`log(1)/tau == 0`, `log(n_upper/n)`); the squeeze is not assembled into a formal inequality chain, and the τ→∞ limit is taken of the bounds, not of LME. The spec item "LSE − max > 0" has no assertion in `verify`; it appears only in a comment and the STATEMENT, and holds only for n >= 2 (equality at n = 1; the docstring notes this, STATEMENT says "(n >= 2)").
- **L6** adequate. One-variable MGF from `sympy.stats`; independence via the cited rule I5; Product collapsed to exp(Sum) for symbolic d. Needs `expand_log(force=True)`, which assumes branch conditions that hold for real arguments; w is not declared real.
- **L7** adequate. Elasticity −w_k/w_j via a tangent direction with KroneckerDelta, index bounds imposed by substituting the Piecewise guards; improvement factor and uniform improvement verified. Requires w_j0 != 0 (not enforced in code).
- **L8** weakest. Shift invariance and Q Qᵀ = I (block Gram) are checked with a hand-written rewrite rule for B·1 = 0. The `(1,2)` block check only tests that B and 1 are adjacent factors. The claimed round trip u = Bᵀ Z + (1/d)(1ᵀu)1 is stated by deduction ("Q square, Q Qᵀ = I, hence QᵀQ = I") and the verify's last assertion compares `recon` with its own definition; the Qᵀ Q expansion assertion has a permissive `or` disjunction. The reconstruction identity is therefore not machine-verified from A7. Its negative-control test asserts only that the unreduced expression differs.
- **L9** strong. Closed form with Product→exp(Sum), simplex substituted, and conditioning invertibility; broken-formula trial failed correctly. Uses lemma-local `beta0`, `r`.
- **L10** mixed (as L5): shift equivariance over symbolic K, d with per-term simplex, K = 1 reduction by substitution, GP/posynomial identity (strong); the κ→∞ squeeze rests on F10 and constant bounds, not a formal chain.

## Definition of good enough

| Item | Verdict | Evidence |
|---|---|---|
| Deliverables D-1 to D-6 exist at the stated paths | met | Table above. |
| R-1 to R-16 pass as checked, with evidence | met with the caveats G-3 to G-7 (R-10 grep literal, R-5 sub-claims) | Table above. |
| Every lemma L1–L10 passes in abstract form and every fallback is declared in the ledger | met | `run.py` output: PASS L1–L10; FALLBACKS lists F5, F10. No other step uses enumeration or a hidden placeholder, but the placeholder real families in L4 and the KKT premise in L3 are not in the FALLBACKS list (G-5). |
| Non-goals untouched | met, see below | No `src/` change, no docs, no `symproof` import, no enumeration proof. |

Definition of good (not a stopping criterion): docstrings state proved / not proved and cite symproof mimicry (`library/convex.py`, `library/topology.py continuous_at_point`, `tactics.py signed_sum_lemmas` in L3, L4, L5, L6, L8, L10). `symproof` is only mentioned in comments and docstrings; `grep import.*symproof` finds nothing. Broken-formula trials failed loudly with lemma numbers. Runtime 8 s for the full suite.

## Outside the scope

- **Out-of-scope changes:** `.github/workflows/test.yml` (checkout@v5, setup-uv@v7, `ubuntu-24.04` pin, invalid `python-version-file` input removed): a CI fix not in D-1..D-6 (commit `0d2f0bd`). `derivation/sumtools.py` (36 lines, Sum-linearity helpers) is not a listed deliverable. `pyproject.toml` `pythonpath = [".", "src"]` is permitted by R-15. Added axioms beyond spec §6 and the named I5: A0 (sizes structural axiom, anticipated by the defaults), A7 (chart hypotheses B Bᵀ = I, B1 = 0; the defaults allow "POSITED or fallback hypotheses on B"), F5 and F10 (max representations; allowed by the defaults). `work-packages/README.md` Status row not updated beyond "in progress".
- **Non-goals touched:** None. No `src/` change; no docs pages or generated ledger page; no `symproof` dependency or seal; no enumeration proofs (no loops over concrete d, n, K); no new mathematics beyond L1–L10; no bibliography entries; spec §4/§6 unchanged.

## Observations (not counted as failures)

- O-1. Spec discrepancy: "LSE − max > 0" holds only for n >= 2. The delivered STATEMENT says so, but `verify` contains no assertion for it.
- O-2. F5 and F10 are tagged POSITED with `fallback=True`, so they appear in the FALLBACKS section only (the POSITED section excludes them). Their role and failure_mode are substantive: they say the limit and upper bound need the sympy-lacking symbolic max and lose the lower squeeze bound if M is not attained. R1's entries are likewise concrete (vertex/edge/zero-normal facet leads to subgradient inclusion, non-unique w*, undefined elasticities).
- O-3. The Status table row in `work-packages/README.md` still reads "in progress".
- O-4. The pull-back (L9) and L7 use lemma-local real Symbols (`beta0`, `logf`, `x`) outside `SYMBOL_ASSUMPTIONS`; the hygiene test polices only the shared namespace.

## Open decisions (for the supervisor)

- **G-1.** Out-of-scope `.github/workflows/test.yml` CI fix (`0d2f0bd`). — options: accept as is / fix before acceptance / follow-up work package
- **G-2.** Out-of-scope or added files and axioms: `derivation/sumtools.py`; A0, A7, F5, F10 beyond spec §6 (anticipated in the defaults). — options: accept as is / fix before acceptance / follow-up work package
- **G-3.** R-1 wording: extra shared symbols (i0, s, a, alpha, b, v, p, eps, M, t) beyond the R-1 list. — options: accept as is / fix before acceptance / follow-up work package
- **G-4.** R-4: L8 `AXIOMS_USED` is `["A7"]`; spec §6 lists [A2]. A2 (the simplex) is not used by L8, so the spec list is not a minimum met. — options: accept as is / fix before acceptance / follow-up work package
- **G-5.** R-5 weak verification: L3 balanced KKT assumes stationarity (R1 not used in code); L4 sign step uses placeholder real families unlinked in code; L5/L10 squeeze is not a formal chain and "LSE − max > 0" is unasserted; L8 round trip `recon = u` is not machine-verified (self-comparison, permissive `or` assertion). None of these is listed in FALLBACKS. This affects good enough ("every fallback declared in the ledger"). — options: accept as is / fix before acceptance / follow-up work package
- **G-6.** Ledger placement: F5/F10 are tagged POSITED yet only printed under FALLBACKS (POSITED section filters them out). Roles and failure modes are substantive. — options: accept as is / fix before acceptance / follow-up work package
- **G-7.** R-10 literal grep: three `range(` hits in helpers (L3 iteration cap, L8 factor and block indexing); none loops over a concrete size. — options: accept as is / fix before acceptance / follow-up work package
- **G-8.** Observations O-1, O-3, O-4 (spec n >= 2 note, Status table, lemma-local symbols). — options: accept as is / fix before acceptance / follow-up work package

## Gap dispositions

Each gap (any item not met, any out-of-scope change, touched non-goal or observation) is resolved through the
decision loop (`~/.claude/skills/CLAUDE.md`). The decision records are in the PR thread, or in `WPn-decisions.md`
next to the scope if the project has no PRs.

| Gap | Disposition (accept as is / fix before acceptance / follow-up work package) | Reason or follow-up |
|---|---|---|
| G-1 CI workflow change | pending | pending |
| G-2 sumtools.py, A0/A7/F5/F10 | pending | pending |
| G-3 extra shared symbols | pending | pending |
| G-4 L8 axiom list vs spec | pending | pending |
| G-5 weak verification sub-claims (L3, L4, L5, L8, L10) | pending | pending |
| G-6 fallback ledger placement | pending | pending |
| G-7 `range(` grep hits | pending | pending |
| G-8 observations O-1, O-3, O-4 | pending | pending |

## Recommendation

Provisional, pending the gap dispositions: recommend acceptance with the listed gaps noted, because all deliverables exist, every requirement's stated check ran green (71 tests, `run.py` PASS L1–L10 with exit 0, ruff and lock clean, no attribution lines, no non-goal touched), and both reviewer trials behaved as the scope requires (unregistered assumption fails the hygiene test; a broken formula fails with "L9 FAIL"/"L5 FAIL"). The main caveat is G-5: several lemma sub-claims (L3 KKT, L4 sign step, L5/L10 squeeze, L8 round trip, the unasserted "LSE − max > 0") are weaker than "proved for symbolic d, n, K" suggests, and are not all declared in FALLBACKS. If the supervisor dispositions G-5 as "fix before acceptance", the recommendation becomes do not recommend acceptance yet, and the whole review is rerun after the fix.

Acceptance is the supervisor's act, recorded as named above. This report does not accept the work.

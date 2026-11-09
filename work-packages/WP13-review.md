# WP13 — Review report

| | |
|---|---|
| **Scope of work** | `work-packages/WP13-scope-of-work.md` |
| **Scope approval verified** | `work-packages/WP13-decisions.md`, "Scope approval": supervisor (mzargham), verbatim "Approved", 2026-11-08, scope at commit 093e8d3; defaults approved as one item ("Approve the defaults as listed"). Verbal record, as the scope names; no PR. |
| **Work reviewed** | `git diff fc2363e..HEAD` on `dev` (HEAD e85f882; the 20 commits "WP13: ..." plus interleaved Records/Process/WP14, WP8a, WP10, WP15 commits) |
| **Supervisor (accepts)** | mzargham |
| **Acceptance record** | Verbal acceptance in chat, quoted verbatim in `work-packages/WP13-decisions.md`, after this report |

Reviewer: fresh context, did not build the work. Nothing fixed; the only file written is this report. Scratch scripts and the `git archive` of fc2363e live under the session scratchpad, outside the repository.

## Checks run (summary)

| Check | Command | Result |
|---|---|---|
| Derivation | `uv run python derivation/run.py` | exit 0; `[L1]`..`[L14] PASS` (header "L1 -> L14"); audit lists `I8 (INHERITED)`, `I9 (INHERITED)`, `R2 (REGULARITY)`, `F12 (POSITED)` each with role and failure mode; `ALL LEMMAS PASS.` |
| Suite (named files) | `uv run pytest tests/test_derivation.py tests/test_solvers.py tests/test_estimator.py tests/test_docs.py tests/test_narrative.py tests/test_sklearn_compat.py tests/test_k_terms_case.py -q` | `807 passed, 11 skipped, 1 xfailed, 23 warnings in 177.76s` (the xfail is the unchanged, pre-existing expected-failure entry; `tests/test_sklearn_compat.py` is untouched by the range) |
| Docs after last commit | `uv run pytest tests/test_docs.py tests/test_narrative.py -q` (rerun at e85f882) | `24 passed` |
| Doctests | `uv run pytest src -q` | `49 passed` |
| Lint | `uv run ruff check .` | `All checks passed!` |
| Format | `uv run ruff format --check .` | **FAILS**: `1 file would be reformatted, 126 already formatted`; the file is `work-packages/WP15-scope-of-work.md` (a Python code block inside a draft scope for another package, commit 9ddf1e1/de31bf6). No WP13 file is unformatted. See gap G-A. |
| Lock | `uv lock --check` | `Resolved 173 packages in 5ms`; `git diff fc2363e..HEAD -- pyproject.toml uv.lock` empty |
| Attribution | `git log fc2363e..HEAD --format=%B \| grep -ci 'co-authored\|generated'` | `0` |
| Notebook, K = 1 files | `git diff fc2363e -- tests/test_notebook.py examples/adcs/adcs_trade_study.ipynb \| wc -l` | `0` |
| CI | `gh run list --branch dev` | one run, `workflow_dispatch`, success, headSha c4133c8, which predates the range. No run on any WP13 commit (R-11 manual run is pending). |

Net size, `git diff --shortstat fc2363e..HEAD`: **36 files changed, +3978 / -349 (net +3629)**. By area: `src/` +548/-34 (2 files); `derivation/` +728/-22 (7); `tests/` +868/-11 (6); `docs/` (all, incl. notes and spec) +904/-196 (10), of which `docs/superpowers/notes/system-model-tidy.md` is +163 and belongs to WP15; `examples/` +12/-3 (3 files, two are PNGs); `work-packages/` +918/-83 (8), of which about 780 lines are the draft scopes of WP14, WP8a, WP10, WP15 plus process records.

## Goals

| ID | Verdict | Evidence |
|---|---|---|
| G1 | met | Three levels stated in `docs/method.md` ("Three levels of guarantee", "Level 1: descent", "Level 2: numerical stationarity", "Level 3: conditional local optimality", "The stopping declaration", lines 732-842) in the order Lemma 1, Lemma 2, Proposition 3, Corollary 4, declaration; certified in code by `Termination` on `TermsResult` and `termination_`; four statements with hypotheses in the ledger as L12, L13, L14 (+ I8, I9, F12, R2). `test_method_headings_for_three_levels_and_declaration` passes. |
| G2 | met | Full simplex KKT (L3, method.md "Existence" etc.), L6 as population identity, existence / uniqueness / stability separated (method.md item 7, lines 337-362), no consistency claim (method.md line 319 negates it; grep below). |
| G3 | met | `docs/superpowers/notes/abstraction-gaps.md`: 16 rows G-1..G-16, each with six non-empty cells (script splitting on unescaped `|`: every row 6 cells, shortest cell 12 chars, G-14 "None sought."); policy paragraph once in method.md. Spot check of numbers: see gap G-B. |
| G4 | met | Degenerate-input warning (estimator.py), zero-metric limit (`_zero_limit_scores`), sliver statement in method.md "only observed" item (iv) with "is the reading of that measurement and not a theorem". |
| G5 | met | `notation.md` has the three objects, "energy differential", facet gap etc., "Register phrases" and "Forbidden phrases" subsections that `tests/test_docs.py` reads. |
| G6 | pending, written after review | D-9. |

## Deliverables

| ID | Verdict | Evidence |
|---|---|---|
| D-1 | met, with two deviations (see below) | `solvers.py`: `simplex_gap`, `facet_gap`, `assignment_margin`, `fixed_assignment_bound`, `facet_objective`, `_newton_polish` (called in `_refit` for step B, finite tau, unpenalized only), `P` per-facet duals kept, guard `obj2 > obj + GUARD_TOL and not tangent`, `Termination` with every field the scope lists (status, reason, n_iter, residuals, max_gap, bound, objective_change, assignment_changes, n_empty, gamma, radius, tolerances, gaps, shares), tau = inf gap = LP duality gap. Deviation 1: sixth status `uncertified`. Deviation 2: margin positivity is `gamma > EPS_FEAS` (1e-9), not `> 0`. |
| D-2 | met | `estimator.py`: `termination_`, `conditioning_`, module constants re-exported (`EPS_KKT`, `EPS_FEAS`, `GUARD_TOL`, `POLISH_STEPS`, `EPS_ZERO_EXPONENT`, `PARTICIPATION_THRESHOLD`), `ConvergenceWarning` keyed to `_WARN_STATUSES = (iteration_cap, guard_stop, uncertified)` with status and max gap in the message, UserWarning on a single valid row, docstring says convention, `_zero_limit_scores`, masking unchanged. `parametrize_with_checks` unchanged and passing. |
| D-3 | met | `derivation/lemma_12_facet_gap.py`, `lemma_13_margin.py`, `lemma_14_assignment_stable.py` use `IndexedBase`, symbolic `d`, `n_k`, `N`, `K`; `lemma_03` has `KKT_boundary` and `boundary_example`; `lemma_06` restated as population identity; `axioms.py` has I8, I9, F12, R2 (run.py audit above); `run.py` ends in ALL LEMMAS PASS. |
| D-4 | met | Ledger above; each D-4 named entry present: three objects G-1, stability/identifiability G-2 and G-12, finite sample G-3 and G-11, conventions G-4 to G-6, Q2-Q4 G-11 to G-13, Q1 not pursued G-14, WP9 gaps G-7 to G-10 (thin facets, tangent/penalty, tau per K, ties), plus G-15 and G-16. Evidence column cites spikes, tests, cubesat seeds, recipes M1-M5. |
| D-5 | met | method.md restructured as G1 shows; `docs/api.md`, `docs/limitations.md`, `docs/why-and-how.md`, `proof-conventions.md` all changed in the range. One stale line remains in proof-conventions.md (gap G-C). |
| D-6 | met | `notation.md` rewritten (+132/-): three objects, energy differential, facet/term/reach/share, certificate quantities, "what it is not" and "where defined" columns. |
| D-7 | met | Tests listed in R-1 to R-9 below all exist and pass: gap zero at interior / boundary / floor (`test_gap_is_zero_at_the_optimum_and_bounds_suboptimality`), `0 <= f - f* <= G`, LP duality gap, margin lemma perturbations, Corollary, statuses, duplicate facets, zero-metric limit, degenerate warning, `conditioning_`, derivation tests for L3, L6, L12-L14 and the ledger, register phrases. |
| D-8 | met | `k_terms.py` adds `certificate()` columns and `gap G_k`; `k3-cubesat.md` "Changes from WP13" verified by re-run (R-6 below): exactly the ten listed reach values change, all else identical. |
| D-9 | pending, written after review | `work-packages/external-review-2026-11.md` has a "Response letter" heading (line 204) but the letter is the next step. |
| D-10 | met | `work-packages/WP13-decisions.md` exists with approval record and process note. |

## Requirements

| ID | Verdict | Evidence |
|---|---|---|
| R-1 | met | My own script (independent LP dual / softmax gradient; `scratchpad/r14.py`), 20 seeds `make_frontier_data(400,4,n_terms=3,random_state=s)`, `HyperbolicTradeSpace(n_terms=3, temperature=tau, random_state=0)`: **tau = inf**: `{'certified': 16, 'stationary_without_margin': 4}` (seeds 1, 3, 8, 16, gamma about 1e-17), max facet gap 8.9e-16, 0 ConvergenceWarnings. **tau = 50**: `{'certified': 20}`, max gap 5.3e-15, 0 warnings. gamma at tau = 50: 2.5e-4 to 2.2e-3. Also `tests/test_solvers.py::test_r1_planted_certificates` passes. |
| R-2 | met | `test_lp_gap_equals_duality_gap_and_uniform_ties_is_a_valid_bound` (independent `linprog` dual, tolerance 1e-12) passes; my script's tau = inf gaps via my own LP dual are <= 9e-16. Uniform-ties gap documented as "valid but loose bound" in `facet_gap`. |
| R-3 | met | Own script: tau = inf 1600 perturbation draws (16 positive-margin fits x 100), 0 label changes; tau = 50 2000 draws, 0 label changes. radius range at tau = 50: 1.0e-5 to 8.4e-5. |
| R-4 | met | Own per-facet solves (LP, and 5-start SLSQP at tau = 50): `0 <= F - F*_fixed <= bound` on all 40 fits; max F - F* = 5.6e-16 (tau = inf), 0 (tau = 50). Observation: these fits are already at the optimum, so the bound is exercised near 1e-15 only; the non-trivial case is the pre-polish gap in `test_polish_never_increases_the_facet_objective_and_closes_the_gap`. |
| R-5 | met | derivation run and tests above; L3 states and checks the boundary KKT with the finite-tau counterexample; fallbacks F12 recorded with role and failure mode. |
| R-6 | met | (a) Estimator outputs (exponents_, log_offset_, transform, score_samples, inverse_transform, basis_; 5 seeds x 5 configs: tau in {inf, 20, 5}, reweighted-L1 penalty, min_exponent) hashed at fc2363e (`git archive`, PYTHONPATH) and at HEAD: both `854c8240dd2f1b1932db8f6163792c39255259e0d0e41536b1fc938575d002c5`, byte-identical on positive data. (b) `git diff fc2363e -- tests/test_notebook.py examples/adcs/adcs_trade_study.ipynb` is empty. (c) Cubesat re-run of `k_terms.py` at fc2363e and at HEAD (HEAD copy run in scratch so no figure was touched): same 118 lines; the only numeric changes in the old columns are the ten reach values 0.321029->0.321030, 0.492784->0.492783, 0.477358->0.477357, 0.450506->0.450505, 0.416293->0.416292, 0.258447->0.258448, 0.218955->0.218954, 0.256436->0.256435, 0.287391->0.287390, 0.547746->0.547745, exactly the table in `k3-cubesat.md`. |
| R-7 | met | Ledger: 16 rows, six cells each (G-1..G-14 required). `grep -c 'Map and territory' docs/method.md` gives 1 (paragraph at line 15); "All models are wrong" appears once in docs/, in method.md; other pages point to it. Hedging count: `git diff fc2363e..HEAD -- docs src derivation README.md \| grep '^+' \| grep -ciE 'caveat\|note that\|however'` = **0** (no lines to list). Observation: limitations.md gains a bold "Local optimality is conditional" entry; it is a statement of level 3's condition, not a hedge phrase. |
| R-8 | partly | `test_register_phrases_present`, `test_forbidden_phrases_absent` pass (10 register phrases present, 10 forbidden phrases absent from `docs/*.md`). Manual grep of "distance" in docs/*.md: all remaining uses are the register-allowed signed Euclidean distance (method.md 140), unrelated distances (kNN, Shephard distance function in literature.md), or quoted axioms. But outside the test's scope (`docs/*.md` only) the stale reading remains: `README.md` line 9 "log V, the distance from it" and the design spec line 17 "log V (distance from the frontier)" (the spec was edited by WP13 but this line missed). See gap G-D. |
| R-9 | met | `test_zero_metric_with_zero_exponent_equals_the_formal_limit`, `test_zero_metric_limit_for_k_terms_follows_each_facet`, `test_degenerate_single_valid_row_warns_with_the_convention` pass; docstring contains "declared convention". |
| R-10 | pending, written after review | D-9. |
| R-11 | partly | Suite, lint, lock and attribution pass at HEAD; **format fails at HEAD** (WP15 draft file, out of scope, G-A); not verified commit by commit (only HEAD run). Manual Tests run on dev: **pending** (the only run is c4133c8, before the range). |

## Specific content checks asked for

- **Sliver (E-7)**: moved to "what is only observed", item (iv), wording "the reading of that measurement and not a theorem" (method.md 961-965); ledger G-6 titled "(observed, not proved)". Met.
- **E-2 / E-5 / E-6**: full simplex KKT in L3 and method.md; existence / uniqueness / stability in method.md item 7 with the restricted Hessian and `conditioning_`; L6 scope in method.md item 4; `grep -rn -i 'unbiased' docs src` only hits method.md 319 ("No statement of consistency or finite-sample unbiasedness is made"), the ledger and the register's forbidden list; `consistent` hits are unrelated (references.bib, literature.md citing others' work).
- **Cubesat record**: "Changes from WP13" list verified by re-run (R-6c). One unverifiable line: "Run time 60 s (50 s before)" (not timed).
- **Stale-text sweep**: no "17/20" in live docs (method.md line 894 states the 17 -> 16 move, the solvers docstring and api.md agree with method.md 873/892-893); no "eleven lemmas"; remaining stale items: `docs/superpowers/notes/proof-conventions.md` line 52 ("Axioms A1-A6 ..., I1-I4, R1; lemmas L1-L10", now I1-I9, R1-R2, F12, L1-L14); spec line 435 (WP1 acceptance wording "L1-L10", historical, defensible); spec line 17 and README line 9 ("distance"); notebook line 2540 "distance from the frontier" (untouchable under R-6); `paper-outline-v1-baseline.md` (a frozen baseline). The sentence in `docs/why-and-how.md` listing statuses omits `uncertified` (it says "certified, stationary without margin, or a stop at the iteration cap or on the guard").

## Code review (solvers.py, estimator.py)

- **Margin and radius**: `gamma = min_i(top1 - top2)` of scores, radius `gamma / (2 max ||(u_i,-1)||)`. Correct by Cauchy-Schwarz (a perturbation of norm < radius moves each score by < gamma/2); my 3600 draws agree. The perturbation is not restricted to the simplex, a superset of what the lemma needs. Note the radii are small (1e-5 to 1e-4 on the cubesat and planted data), so "certified" is a true but very local claim; the record prints it and `limitations.md` mentions "the size of change that is safe".
- **Guard**: rejects only when the new objective exceeds the old by more than 1e-12, returning the previous consistent (W, beta, labels, P). Tested with a monkeypatched worse refit. Tangent step is exempt and keeps its best-iterate rule. Correct.
- **Polish**: reduced Newton on `w > m + 1e-10`, five steps, backtracking never increases the objective (tolerance 1e-15 absolute); stalls silently if no step is accepted, which then surfaces as `uncertified`, not a wrong certificate. Acts only on step B, finite tau, unpenalized. Planted-data evidence: gaps from ~1e-5 before to <= 1e-14 after.
- **Status logic**: order not_applicable > iteration_cap > guard_stop > uncertified > certified / stationary_without_margin is sound; an empty facet maps to stationary_without_margin (consistent with the scope's "empty facets" field). `iteration_cap` sets `success=False`, so the warning and `n_iter` behave as before.
- **Deviation 1, `uncertified`**: the scope lists five statuses. A fixed assignment with a residual or gap above tolerance fits none of them; the sixth is needed and honest, is warned on, documented in method.md, api.md and the Termination docstring. It extends a scope list, so it should be recorded as an amendment note.
- **Deviation 2, margin positive means `gamma > EPS_FEAS = 1e-9`**: R-1 says "certified wherever the margin is positive". A margin in (0, 1e-9] reports `stationary_without_margin`. On the 40 planted fits the two readings coincide (zero-margin gammas are ~1e-17; positive ones >= 6.8e-5), and the docstring and method.md state the tolerance; it is the numerically honest choice but changes a stated requirement's wording. Record as an amendment note.
- **Behavior change to note**: `guard_stop` now emits a ConvergenceWarning (D-2 asked for a warning keyed to the status). Not observed in any planted or cubesat fit.
- **Recovery**: the 1e-12 guard tolerance moved step B at tau = inf from 17 to 16 of 20 (seed 8 now fails); listed in method.md (line 894) and tests, as the scope allows ("every such change listed"). A K > 1 outcome moved, not only a residual.
- **sklearn conformance**: `fit` stores params verbatim, attributes set in `fit` only (`termination_`, `conditioning_`), `validate_data` pattern unchanged, `parametrize_with_checks` unchanged with `xfail_strict=True` (807 passed), no `predict`; the single-row UserWarning does not trip the checks. Met.

## Outside the scope

- **Out-of-scope changes (in the range, not WP13 deliverables)**: draft scopes `work-packages/WP14-scope-of-work.md`, `WP8a-scope-of-work.md`, `WP15-scope-of-work.md`, large edits to `WP10-scope-of-work.md` (+250/-), `WP10-decisions.md`, `work-packages/PM-BRIEF.md`, `work-packages/README.md`, `docs/superpowers/notes/system-model-tidy.md`, and the register line changed in e85f882 ("configuration-to-attributes abstraction" wording). These are supervisor-directed process and planning records (commits cc83d1d, 16bea38, 9ddf1e1, f0f5279, de31bf6, 59d8ca9, e85f882), but they sit in the WP13 review range and one of them breaks the format check. Two PNG figures changed (`k3_log_planes_primary.png`, `..._stock.png`), the listed pixel-level regeneration.
- **Non-goals touched**: none. K = 1 results and WP7 notebook untouched (R-6); no global-convergence claim (G-14 not pursued); no paper, site, search or release work; "no new caveats" holds by the grep (0).

## Observations (not counted as failures)

- Ledger G-3: "ratio ... is 1.072 (N=400, sd 0.0061), 1.023 (N=4000, sd 0.0014)". I reproduced the means exactly with recipe M1 (1.072, 1.023) but the seed-to-seed sd of the ratio is 0.179 and 0.041 (ddof 1); the quoted 0.0061 and 0.0014 equal the sd of the absolute shift (0.179 x 0.038 x sqrt(4/5) = 0.0061). The sentence therefore understates the variability of the ratio by about 30x. (G-B)
- The Corollary bound check (R-4) is nearly vacuous on polished fits (F - F* about 1e-16); the polish test supplies the non-trivial case.
- The only CI evidence (c4133c8) predates the work; the suite takes about 3 minutes locally.
- The scope names 14 ledger ids in the review brief; the ledger has 16 (G-15, G-16 added), which is within the scope.

## Open decisions (for the supervisor)

- **G-A. `ruff format --check .` fails at HEAD** on `work-packages/WP15-scope-of-work.md` (a draft scope for another package, committed in the WP13 range). R-11 says format passes on every commit. Options: accept as is (not a WP13 file) / fix before acceptance (format that one file; the fix belongs to WP15's drafter) / follow-up work package. Suggested: **fix before acceptance** (one-line format run), since R-11 is a stated requirement and a red format check blocks the merge gate.
- **G-B. Ledger G-3 sd figures mislabelled** (see observations). Suggested: **fix before acceptance** (two numbers in one cell, or relabel as "sd of the shift"); it is a factual statement about sensitivity evidence, the ledger's purpose.
- **G-C. Stale ranges in `docs/superpowers/notes/proof-conventions.md` line 52** (A1-A6, I1-I4, L1-L10) and the `docs/why-and-how.md` status sentence omitting `uncertified`. Suggested: **fix before acceptance** (two-line edits), same pass as G-B.
- **G-D. "distance from the frontier" survives in `README.md` line 9 and spec line 17**, outside the register test's scope (`docs/*.md`). Suggested: **fix before acceptance** for README and the spec line (R-8), and **accept as is** for the WP7 notebook (untouchable) and the frozen v1 outline; optionally extend the forbidden-phrase test to README and the spec.
- **G-E. Two deviations from the scope's wording**: sixth status `uncertified`; margin positive taken as `gamma > 1e-9`. Suggested: **accept as is** with a one-line amendment note in `WP13-decisions.md` for each (no evidence on the planted data or the cubesat that they change a verdict).
- **G-F. Out-of-scope planning and process commits inside the review range** (WP14, WP8a, WP10, WP15 drafts, PM-BRIEF, README, system-model-tidy.md). Suggested: **accept as is** (supervisor-directed records, draft and unapproved); the acceptance merge to `main` will carry them, which the supervisor should know.
- **G-G. R-11's manual Tests run on dev has not been done** and no commit in the range has been CI-checked. Suggested: **fix before acceptance** in the sense of running `gh workflow run` on dev after G-A to G-D are fixed; it is the scope's own gate.
- **G-H. D-9 / R-10 / G6 (response letter) not yet written.** Suggested: write after this review as the scope orders; then re-check R-10 against E-1..E-10.
- **G-I. Step B at tau = inf now fails seed 8 (17 -> 16 of 20)** because of the 1e-12 guard tolerance; disclosed and permitted by the scope. Suggested: **accept as is**, with a **follow-up work package** only if the paper (WP10) needs the K > 1 recovery rate stated higher.

## Gap dispositions

Not yet decided by the supervisor; the suggested dispositions above are suggestions, not decisions. Decision records belong in `work-packages/WP13-decisions.md`.

| Gap | Disposition | Reason or follow-up |
|---|---|---|
| G-A to G-I | open | see above |

## Recommendation

Do not recommend acceptance yet. The mathematics, code, tests, derivations and ledger are sound and every numeric claim I could re-run held (R-1 to R-6, R-9, the cubesat change list), but three requirements are not closed: R-11 (format check fails at HEAD, manual Tests run not done), R-8 (stale "distance" in README and spec), and D-9 / R-10 / G6 (the response letter, pending by design). After the small fixes in G-A to G-D and the CI run (G-G), and the letter (G-H), the whole review should be rerun once, and I would then expect to recommend acceptance with G-E, G-F and G-I noted.

Acceptance is the supervisor's act, recorded as named above. This report does not accept the work.

## R-10 re-check (letter against the review)

Fresh-context check of "Response letter" in `work-packages/external-review-2026-11.md` against "The
review, verbatim", the item index and the dispositions. Every cited hash exists (`git cat-file -t`
gives commit for 03c8b1a, 1e9ae03, a9f142f, c0b4e9c, d8fa513, 4bfe591, c61ff49, b5467f0, a15566b,
c3cbec4) and each touches what the letter says (`git show --stat`: solvers and tests; estimator and
tests; L12/I8/F12; L13/I9/R2; L14; method.md; L3/L6/R1; ledger, register, proof conventions; E-4 in
L10 docstring, axioms, api.md, method.md; c3cbec4 README and why-and-how wording). Headings "The fit",
"Three levels of guarantee" and "The stopping declaration" exist in `docs/method.md`; existence,
uniqueness and stability are item 7 of "What the stage learns"; ledger ids G-1 to G-16 exist (G-11 to
G-14 = Q2, Q3, Q4, Q1; G-14 not pursued). Tests ran: `tests/test_docs.py`, `test_gaps.py`,
`test_derivation.py`, 136 passed.

Numbers re-measured (`solve_terms(U,3,tau,random_state=0)` on `make_frontier_data(400,4,n_terms=3,
random_state=s)`, s=0..19): tau=50: 20/20 certified, max gap 5.1e-15; tau=inf: 16 certified, 4
stationary_without_margin (seeds 1, 3, 8, 16), max gap 2.0e-15. 3,600 = (16+20 fits with positive
margin) x 100 perturbations in `test_margin_lemma_perturbations_inside_the_radius_keep_labels`; the
Corollary bound is asserted on all 40 fits (`test_corollary_bound_on_every_planted_fit`). Constants
EPS_KKT 1e-8, EPS_FEAS 1e-9, GUARD_TOL 1e-12, participation threshold 1e-3, statuses and Termination
fields match the code. Cubesat K = 2, 3: all certified, max gap 1.1e-14 in the record tables
(1.2e-14 in the seed-stability paragraph), gamma 2.2e-4 to 1.575e-3 (letter: 1.6e-3, rounded).

| Item | Verdict | Notes and exact fix |
|---|---|---|
| E-1 | ok | Restated, all hashes and numbers verified; includes the guard-tolerance side effect (seed 8) and the extra status, matching the recovery paragraph in the method page. Optional: "max gap 1.1e-14" could read "1.1e-14 to 1.2e-14" to cover the seed-stability run. |
| E-2 | ok | L3 STATEMENT, the constructed instance (d = 2, exact arithmetic) and R1 wording are in c61ff49; method page "The fit" in 4bfe591. |
| E-3 | needs fix (minor) | The letter says the STATEMENTs of "L12 to L14, L3" name the object; L12 to L14 do ("fitted reference surface", "supporting envelope"), L3 does not (it separates tau = infinity from finite tau, but names none of the three objects). Fix: write "L12 to L14" and drop ", L3" (or "L3 separates tau = inf from finite tau"). |
| E-4 | ok | a15566b touches method.md, api.md, the L10 docstring and axioms; the bound text matches the review. |
| E-5 | ok | Threshold 1e-3 (`PARTICIPATION_THRESHOLD`), `conditioning_` (nan at tau = inf), G-2 verified. |
| E-6 | ok | L6 STATEMENT reads as quoted; G-3, G-11, G-12 and `test_forbidden_phrases_absent` exist. |
| E-7 | ok | Matches the classification (i) to (iv); tests `test_degenerate_single_valid_row_warns_with_the_convention`, `test_zero_metric_with_zero_exponent_equals_the_formal_limit`; G-4, G-5, G-6 exist. |
| E-8 | needs fix (minor) | No restatement of the reviewer's point, and the disposition says the structure is adopted for the Results section of the paper. Fix: begin with "You asked that the optimization discussion be a short sequence of formal statements." and end with "WP10 carries the same structure into the Results section." |
| E-9 | ok | Restates the five strengths; where: WP10 framing. |
| E-10 | needs fix (minor) | No restatement of the reviewer's point and the reconciliation with outline v2 (in the disposition) is missing. Fix: begin with "You offered a structure of the mathematics (assumptions A1 to A6, core, extensions, algorithm, open questions Q1 to Q4, with Derived / Numerical / Open badges)." and add "The map is reconciled with outline v2 in WP10's scope." |

Tone against the standing position: no overclaiming (statuses and the four zero-margin seeds are
stated plainly; "Accepted in full" matches the disposition); no caveat sprinkling; two disclosed
implementation choices are factual, not hedges.

**Overall verdict: pass with three minor wording fixes (E-3, E-8, E-10).** No factual or numerical
error, no missing or wrong hash, no overclaim. R-10 is met once the three edits are made; none
changes a disposition or a number.

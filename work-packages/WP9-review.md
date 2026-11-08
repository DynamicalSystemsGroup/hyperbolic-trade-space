# WP9 — Review report

| | |
|---|---|
| **Scope of work** | `work-packages/WP9-scope-of-work.md` |
| **Scope approval verified** | `work-packages/WP9-decisions.md`, "Scope approval": supervisor (mzargham), verbatim "Approved", 2026-11-08, scope at commit d3abf28. Verbal record, as the scope names; no PR. |
| **Work reviewed** | `git diff 3bebe3e 6c304a8` on `main` (commits cbd618c, a86a4d3, 6c304a8; 35 files, +1942/-204) |
| **Supervisor (accepts)** | mzargham |
| **Acceptance record** | Verbal acceptance in chat, quoted verbatim in `work-packages/WP9-decisions.md`, after this report |

Reviewer: fresh context, did not build the work. Nothing fixed; the only file written is this report; `git status --short` was empty after all runs.

## Checks run (summary)

| Check | Command | Result |
|---|---|---|
| Suite | `uv run pytest -q` (twice) | `1049 passed, 10 skipped, 1 xfailed` (both runs, about 2 min). The 10 skips are "SCIPY_ARRAY_API is not set"; the 1 xfail is `TradeSpaceRegressor(...)-check_regressor_multioutput` (the WP-earlier wrapper, not `n_terms`). |
| Lint | `uv run ruff check .` | `All checks passed!` |
| Format | `uv run ruff format --check .` | `115 files already formatted` |
| Lock | `uv lock --check` | `Resolved 173 packages`; `git diff --stat -- pyproject.toml uv.lock` empty (no new dependency) |
| Derivation | `uv run python derivation/run.py` | `[L11] PASS ...`; `ALL LEMMAS PASS.`; I7 printed under "INHERITED, solver level" |
| Attribution | `git log 3bebe3e..6c304a8 --format=%B \| grep -i -c "co-authored-by\|generated"` | `0` |
| Notebook/K=1 | `git diff --stat 3bebe3e 6c304a8 -- examples/adcs/adcs_trade_study.ipynb tests/test_notebook.py` | empty (untouched) |

## Deliverables

| ID | Verdict | Evidence |
|---|---|---|
| D-1 | met, with deviation (a) | `solvers.py`: `solve_slsqp(..., penalty, alpha)`, `TermsResult`, `solve_terms`, `_refit`, `_solve_terms_once` all present (read in diff). Facet refit is a supporting hyperplane over all rows, not a refit on the facet's own rows (see G-1). |
| D-2 | met | `estimator.py` diff: `n_terms>1`, `penalty`, `alpha`, `random_state`, `term_temperature`; attributes `exponents_` (K,d), `log_offset_` (K,), `facet_`, `coefficients_`, `facet_share_`, `basis_` (K,d-1,d), `assign_facets`. Tests `test_k_terms_attributes_conventions`, `test_k_terms_round_trip_and_scores` pass. |
| D-3 | met | `tests/test_tensions.py::test_k3_reports_one_per_facet_recover_planted_supports` (3 seeds) and `test_k1_is_a_single_report_and_facet_error_names_facet` pass. |
| D-4 | met, with a legibility remark | `plotting.py` takes facet colouring and draws the facet envelope; no new figure types. See R-7 on figures. |
| D-5 | met | `make_frontier_data(..., n_terms=K, exponents=...)` returns `info["facet"]`, `info["exponents"]`, `info["frontier_mask"]`; K=1 unchanged (tests pass). |
| D-6 | met | `examples/adcs/k_terms.py`; six `k3_*_{primary,stock}.png` exist; `docs/superpowers/notes/k3-cubesat.md` exists. I re-ran `run_regime` for both regimes into a scratch directory (so the committed figures were not overwritten): every number in the note reproduces (e.g. primary objective_ 0.2036/0.0900/0.0529, frac_above_ 0.096/0.261/0.382; stock 0.1312/0.0678/0.0326, frac_above_ 0.104/0.204/0.338; facet tables and K=1 relations identical; seeds 0-4 stable). Run time 20 s. |
| D-7 | met | Tests added in all seven listed files; L10 numeric instance in `tests/test_matches_derivation.py` (`test_L10_phi_k_bounds_shift_and_limit_at_numeric_instance`); `test_sklearn_compat.py` has two `n_terms=3` cases. Plus `tests/test_k_terms_case.py` (not listed, see Outside the scope). K=1 regression tests: see R-6 for the edits to old tests. |
| D-8a | met | `derivation/lemma_11_pareto.py` has `TITLE, STATEMENT, AXIOMS_USED=["A1","A2"], derive, verify`; in `CHAIN_NAMES`; `tests/test_derivation.py` has five L11/I7 tests; ledger lists it (run output above). Note: lemma part 5 (K>1) is a short `solveset` squeeze on symbols, adequate for the stated claim. |
| D-8 | met, deviations (c) | `docs/method.md` ("The solver for small K", simplifying assumptions 1-6, "What is proved, inherited, observed"), `docs/api.md`, `docs/limitations.md`, `docs/literature.md`, `axioms.py` I7 entry; `docs/references.bib` gained 31 lines (new sources under the WP5 rule: `references-verified.md` +6 lines; see Outside the scope). |
| D-9 | met | `work-packages/WP9-decisions.md` holds the approval, decision loop and push-hold lift; the acceptance entry is pending by design. |

## Requirements

| ID | Verdict | Evidence |
|---|---|---|
| R-1 | met as written; recovery is not universal | `test_k_terms_recovers_planted_facets` (seeds 0, 2 at tau=inf; 0, 4 at tau=50) passes: exponent error < 0.05, >= 90% frontier rows on the right facet, K=1 depth 0.15+ vs K=3 under 1e-6. **My re-run on seeds 0-19** (N=400, d=4, K=3, `random_state=0`): tau=inf 17/20 pass (median error 1.7e-16; fails seeds 1, 3, 16 with errors 0.51, 0.12, 0.26); tau=50 16/20 (fails 1, 3, 8, 16; seed 8 also only 73% row assignment). Estimator `random_state` 1, 2, 3 at tau=inf: 17/20, 18/20, 17/20. Cause (checked): the failing seeds are those where a planted facet has almost no frontier rows (frontier rows per facet: seed 1 `[58 59 3]`, seed 3 `[6 56 58]`, seed 16 `[2 66 52]`, seed 8 `[53 56 11]`); a facet with 2-6 frontier rows is barely identifiable, so this is a data limit, not evidently a solver defect. The test seeds are a favourable subset of 4 and the pass claim in the docs ("19 or 20 of 20") comes from different settings (N=600, half on the frontier). See G-5. |
| R-2 | met | `test_terms_monotone_history_and_stops`, `test_terms_k1_equals_slsqp_and_degenerate` pass. The monotone objective is the mean slack, and a guard rejects increases (code read). See G-1. |
| R-3 | met | `test_k_terms_round_trip_and_scores[K in 2,3 x kappa in inf,5]` pass: round trip rtol 1e-8, `score_samples == transform[:, -1]`, gap within [0, log K / kappa]. |
| R-4 | met | Three seeds: K=3 list of 3 reports, `n_near_frontier >= 10`, contending sets `[[0,1],[1,2],[2,3]]` recovered (differ per facet). |
| R-5 | met | `test_sklearn_compat.py` with `HyperbolicTradeSpace(n_terms=3)` and `(n_terms=3, temperature=inf, term_temperature=5.0)`; `EXPECTED_FAILURES` still `{}`; all pass, `xfail_strict=True`. |
| R-6 | met for K=1 behaviour; not met literally ("without edits to assertions", "additions only") | Notebook and `tests/test_notebook.py` untouched (empty diff above); all pre-existing tests pass. But `git diff 3bebe3e 6c304a8 -- tests/ \| grep '^-'` shows 6 removed/edited old lines, all listed below with judgements. |
| R-7 | met, figures partly weak | The record states, per regime and facet: size, contending set, n-lemma, largest exponents, near-frontier count, plus reach, share and the K=1 relation (verified by my re-run). Figures: all six viewed (primary: log planes, frontier coordinates, tensions; stock: log planes). Text is legible at full resolution; the word "red" appears in no label (red is only `HOLE_COLOR`; facet colours are the colour-blind-safe blue/orange/green). Weaknesses: in the stock log-plane figure the third panel shows no envelope line, the second panel's line lies far left of the data, so the envelope is not visible in two of three stock panels; the tension heat maps have small tick labels at the saved size. The record itself says log-plane slices of a ten-metric fit are hard to read. See G-6. I did not view `k3_frontier_coordinates_stock`, `k3_tensions_stock` (same code path). |
| R-8 | met | Net added code lines in `src/hyperbolic_trade_space/` vs 3bebe3e, non-blank, non-comment, AST-excluded docstrings: datasets +25, estimator +66, plotting +28, solvers +88, tensions +11 = **218 net** (multiset gross added 298, removed 80). Budget 300. `uv lock --check` passes; `pyproject.toml`/`uv.lock` unchanged. |
| R-9 | met | `docs/method.md` gives the algorithm in given/repeat/until form, cites L10, F10, I7, and states "**Nothing is claimed about global optimality.**" (line 670; again in assumption 2). `grep -rn -i "documented, not built"`: remaining hits only for kernel methods (`docs/api.md` lines 4 and 236). `tests/test_docs.py` and `tests/test_narrative.py` pass. Truthfulness of `solve_terms` description: matches the code (random-row init, Helmert nearest-centre labelling, centred refit over all rows, beta = J over all rows, mean-slack objective with guard, 50 iterations, best of restarts, default 5). One caveat on I7: the docs say plainly it is the pattern and not a theorem for this objective. |
| R-10 | met on the final commit, not run per commit | Suite, ruff, format, lock, attribution (0) all pass at 6c304a8. I did not check out and run the suite at cbd618c and a86a4d3 separately. |
| R-11 | met | `test_reweighted_l1_gives_exact_zeros_on_planted_sparse_facet`, `test_penalty_validation_and_alpha_zero_exact` (solvers) and `test_penalty_gives_exact_zero_exponents_at_the_estimator` (plain exponent on the zero metric `> 1e-3`, penalized exactly 0, `alpha=0` equals unpenalized via `assert_array_equal`) pass. |
| R-12 | met | `derivation/run.py` prints `[L11] PASS` with chain "L1 -> L11", axioms A1, A2; `tests/test_derivation.py` L11 tests pass; method page cites L11 (Interpretation and proved paragraph); `test_narrative.py` tag check passes (ceiling raised to 11). |

### R-6: every removed or edited old assertion

| Where | Change | Judgement |
|---|---|---|
| `tests/test_estimator.py::test_n_terms_not_implemented` | removed `pytest.raises(NotImplementedError, match="documented extension")` for `n_terms=2`; replaced by `test_n_terms_above_one_is_implemented` | Justified: the behaviour it asserted is what WP9 removes (G2). It does breach R-6's literal "additions only" wording; the scope contradicts itself here. |
| `tests/test_derivation.py::test_every_axiom_is_used` | exemption `and n not in AX.SOLVER_LEVEL` added | Justified but weakens an audit: I7 is cited by the solver and no lemma consumes it. The exemption is a named tuple (`SOLVER_LEVEL = ("I7",)`) printed under its own ledger heading. |
| `tests/test_docs.py::test_lemma_tags_in_range` | `1 <= n <= 10` -> `<= 11` | Justified (L11 exists). |
| `tests/test_narrative.py` | `range(1, 11)` -> `range(1, 12)` | Justified (same). |
| `tests/test_tensions.py` import line | `from hyperbolic_trade_space import HyperbolicTradeSpace, tension_report` -> adds `make_frontier_data` | Justified, no assertion change. |
| `tests/test_derivation.py` skip reason `"needs all ten lemma modules"` unchanged | n/a | Stale wording only (observation). |

## Definition of good enough

| Item | Verdict | Evidence |
|---|---|---|
| D-1..D-9 exist at stated paths | met | table above |
| R-1..R-12 pass as checked, with evidence | met, with R-6 literal wording and R-1 reliability disclosed | above |
| Planted K=3 frontier recovered; cubesat K=3 record with figures exists | met | R-1 (17/20 or 16/20 on 20 seeds, with the failures explained); record and six figures exist and reproduce |
| Non-goals untouched | met | below |

Definition of good: the code reads as a loop around `solve_slsqp` (`_refit` calls it on centred data; `_solve_terms_once` is about 20 lines): met. Docs separate proved (L10, L11), inherited (I7) and observed: met. "Three facets with their own contending sets, seen in figures where facets meet": largely met in the record; the figures show it only weakly (G-6).

## Outside the scope

- **Out-of-scope changes (none harmful):** `tests/test_k_terms_case.py` (+52, not a listed test file: a test of `k_terms.py`); `docs/literature.md`, `docs/superpowers/notes/notation.md`, `docs/superpowers/notes/references-verified.md`, `docs/references.bib` (+31, `candes2008enhancing` and others; scope allowed new sources under the WP5 rule, and the Candès DOI was anticipated); the spec's section 6 (+/-4 lines; D-8 names the ledger, the spec section mirrors it); `derivation/axioms.py` gained a `SOLVER_LEVEL` mechanism and `derivation/run.py` a new audit heading (needed for I7 but not named in the scope).
- **Non-goals touched:** none. No performance/scalability code (the solver is a plain loop), no kernels, K=1 results and notebook untouched (empty `git diff --stat`), no paper or site files, no push issue (the hold was lifted by the supervisor, recorded in `WP9-decisions.md`).

## Observations (not counted as failures)

- `frac_above_` rises with K at fixed tau: 0.096, 0.261, 0.382 (primary), 0.104, 0.204, 0.338 (stock), where tau was tuned at K=1 for 0.10. The envelope sits lower relative to the cloud, so a K=3 "frontier" has a third of designs above it. Disclosed in the record, `method.md` ("Only observed (iii)") and `limitations.md`. It undercuts reading the K=3 `objective_` drop as a better frontier fit.
- `objective_` (mean slack) falls with K by construction (docs say so); it is not a selection criterion.
- A facet can hold very few frontier rows on planted data; recovery then fails (R-1 numbers).
- Recovery numbers in the docs (19 or 20 of 20) and in the `solve_terms` docstring are for N=600 with half on the frontier; at the test's default (N=400) I measured 17/20. The words "in most seeds, not in every seed" are accurate; the specific counts are condition-bound.
- Scope contradiction: R-6 "additions only" versus G2's removal of `NotImplementedError`.
- Primary regime facet 3 has 27 near-frontier designs, only 2.7x the default minimum of 10.
- The record's primary-regime contending set of the control-effort facet differs by one metric across seeds (settling time); the record says so.

## Open decisions (for the supervisor)

Each is a gap; options: accept as is / fix before acceptance / follow-up work package. My suggested disposition is given per item.

- **G-1 (deviation a, facet refit and objective).** The facet is refit as a supporting hyperplane over all rows (centred data), with objective mean slack, instead of "refit by `solve_slsqp` on its rows", and the objective is mean slack, not size-weighted reach. The code, the docstring and the method page (assumption 5) all disclose it, with the observed reason (own-row fit tilts to a simplex vertex; the PM checked it). It is also what lets the monotone claim and R-2 hold, and `beta_k` keeps meaning "offset of J over all rows" so `tension_report` and `coefficients_` remain coherent. Judgement: a justified, documented deviation; suggest **accept as is**. Related: `TermsResult.objective` docstring says `sum_k (n_k/N) beta_k` while the code and the docs use mean slack `mean(beta[labels] - W[labels]·u)`; the docstring in `TermsResult` is therefore out of line (minor). Suggest **accept**, and fold the one-line docstring fix into the next code change (or **fix before acceptance** if you want zero residue).
- **G-2 (deviation b, random-row initialization instead of K-means).** Chosen on a recorded comparison (20 seeds: 19/20 vs 19/20 and 20/20 vs 19/20, in the `solve_terms` docstring); the scope allowed "whichever recovers more reliably, recorded". Shorter code. I did not re-run the K-means comparison. Suggest **accept as is**.
- **G-3 (deviation c, ledger id I7 instead of I5).** I5 and I6 were already taken (MGF, orthogonal inverse); I7 is the next free id and the scope's "I5" was a stale guess. Also added a `SOLVER_LEVEL` heading and a test exemption. Suggest **accept as is**.
- **G-4 (deviation d, old-test edits).** Listed with judgements above. The `NotImplementedError` replacement and ceiling raises are required by the feature; the every-axiom-used exemption is a small weakening of an audit with a named, printed reason. Suggest **accept as is**, with you noting that R-6's literal wording ("additions only") was not achievable.
- **G-5 (R-1 reliability and doc wording).** Measured recovery on 20 seeds is 17/20 (tau=inf) and 16/20 (tau=50); the failures are facets with 2-11 frontier rows; the test uses four favourable seeds. The docs say "19 or 20 of 20 in the comparisons recorded" which is true of another setting but reads stronger than the default setting gives. Options: (i) accept as is (docs already say "not in every seed"); (ii) fix before acceptance: one sentence in `method.md` "Only observed (i)" and the docstring giving the 17/20 figure at the default N=400 and its cause. Suggest **fix before acceptance** (a one-sentence docs change) or at minimum **accept** with the paper (WP10) quoting the measured rate, not the docs' wording.
- **G-6 (R-7 figures).** In `k3_log_planes_stock.png` two of three panels show no visible envelope near the data (panel 3 shows no line at all), and tick labels in the tension maps are small; the record already says log-plane slices are hard to read. The coordinates and tension figures carry the story. Suggest **follow-up work package** (choose better slice axes or draw the max-envelope only where facets have weight, a WP10 figure task), or **accept as is** if the paper builds its own figures.
- **G-7 (finding e, `frac_above_` rises with K).** Real, reported in three places, not re-tuned; changes how the paper may describe the K=3 fit ("tighter envelope" is not what it shows; mean slack falls but a third of designs lie above the envelope). Suggest **follow-up work package** (K-specific temperature selection, already named in the limitations as open) and **accept as is** for WP9 since disclosing it was the stated plan.
- **G-8 (R-10 per commit).** I verified the final commit only, not each of the three local commits separately. Suggest **accept as is** (history is local-then-pushed, the final tree is green), or ask the driver to confirm the per-commit runs it recorded.
- **G-9 (out-of-scope and minor items).** `tests/test_k_terms_case.py`, `SOLVER_LEVEL`, the `TermsResult.objective` docstring mismatch (G-1), the stale "ten lemma modules" skip reason in `test_derivation.py`. Suggest **accept as is**, one item.

## Gap dispositions

Pending the supervisor, through the decision loop. Reviewer's suggestions:

| Gap | Disposition (suggested) | Reason or follow-up |
|---|---|---|
| G-1 | accept as is | disclosed, defended, observed reason; fix the one-line `TermsResult.objective` docstring when next touching `solvers.py` |
| G-2 | accept as is | recorded comparison; equal reliability, less code |
| G-3 | accept as is | next free id; helper heading is small |
| G-4 | accept as is | all edits forced by the feature or a documented exemption |
| G-5 | fix before acceptance (one docs sentence) | docs state recovery rates under different conditions than the default |
| G-6 | follow-up work package (or accept) | figure legibility is a WP10 presentation task |
| G-7 | follow-up work package | K-specific temperature is an open choice; disclosed |
| G-8 | accept as is | final tree verified |
| G-9 | accept as is | minor |

## Recommendation

Recommend acceptance with the listed gaps noted, once G-5 is dispositioned (suggested: the one-sentence docs fix, after which the whole review is rerun as the skill requires, or you accept it as is). Reasons: every deliverable and requirement is met with run evidence (1049 tests pass, lint, format, lock, derivation and attribution checks clean; 218 of 300 budgeted lines; K=1 notebook and tests untouched; the cubesat record reproduces exactly), the PM's disclosed deviations are documented and defensible, and no non-goal was touched. The honest limits are that planted recovery is 16-17 of 20 seeds (failing where a facet has almost no frontier rows) and that `frac_above_` rises with K.

Acceptance is the supervisor's act, recorded as named above. This report does not accept the work.

## Post-review fix 2 (CI on Linux)

- **What failed.** GitHub runs 42517718511 and 42518318170 (commits 6c304a8, 28caf5b):
  `tests/test_plotting.py::test_log_plane_k3_draws_envelope_and_facet_legend` got legend labels
  `['facet 1', 'facet 3']` where it expected `['facet 1', 'facet 2']`. It was the only failure.
- **Cause.** The test plants K = 3 facets in d = 2, where only two distinct facets exist; the fit
  returns two near-identical facets (locally exponents [.87,.13], [.21,.79], [.21,.79]) and which
  of the duplicates takes the rows is a tie that differs by platform. A relabelling of equal
  fits, not a different optimum; the other K = 3 tests (recovery, tensions, sklearn, cubesat) passed
  on Linux. The test wrongly assumed the legend labels are consecutive.
- **Change.** The test now asserts that the labels are a set of at least two names within
  `facet 1..K`. No solver change (the K = 1 path and facet order in `solve_terms` are untouched);
  `tests/test_k_terms_case.py` and the cubesat record assert nothing on facet order (shares, counts
  and exponents per facet are reported as fitted; numbering is by fit and may differ by platform).
- **Green run:** GitHub run 42518908382 (commit 0a91cb7), success.

## Second review (after Amendment 1)

Reviewer: fresh context, did not build the work. Reviewed `main` at 6b4e773 (`git log 3bebe3e..HEAD`, 13 commits; the amendment is 98d8329, code 19383f8, docs 6b4e773). Nothing fixed; this section is the only file edited (`git status --short` empty before writing). The first review above is not relied on: every item below was re-run.

### Checks run

| Check | Command | Result |
|---|---|---|
| Suite | `uv run pytest -q` | `1115 passed, 11 skipped, 1 xfailed` (175 s). The 11 skips are all "SCIPY_ARRAY_API is not set" (one more than before: the new `n_terms=3, facet_step="tangent"` sklearn case); the xfail is the earlier wrapper's `check_regressor_multioutput`. |
| Lint / format | `uv run ruff check .`; `uv run ruff format --check .` | `All checks passed!`; `116 files already formatted` |
| Lock | `uv lock --check` | `Resolved 173 packages`; `git diff 3bebe3e HEAD -- pyproject.toml uv.lock`: only the two-line `extend-exclude = ["docs/superpowers/notes/spike-*"]` in `[tool.ruff]` (no dependency, `uv.lock` untouched) |
| Derivation | `uv run python derivation/run.py` | ends `ALL LEMMAS PASS.` (L11 PASS, I7 listed) |
| Attribution | `git log 3bebe3e..HEAD --format=%B \| grep -i -c "co-authored-by\|generated"` | `0` (also no matching lines with `-n`) |
| K = 1 untouched | `git diff --stat 3bebe3e HEAD -- examples/adcs/adcs_trade_study.ipynb tests/test_notebook.py` | empty |
| R-8 | AST docstring exclusion, non-blank, non-comment lines, per file, HEAD vs 3bebe3e | datasets +40, estimator +71, plotting +28, solvers +106, tensions +11 = **256 net** (budget 300; was 218 at the first review, the amendment added 38: D, the generator top-up, `facet_step` plumbing). Script: `/private/tmp/claude-501/r8.py`. |
| CI | `gh run list --branch main --limit 5` | 42524561753 (6b4e773, docs commit) success; 42524420226 (19383f8, code commit) success; 42523357419 (98d8329) success; 42522968839 and 42521162005 success. Both amendment commits that changed behaviour are green on Linux. |

### Amendment 1 items, each checked

| Item | Verdict | Evidence |
|---|---|---|
| `facet_step="support"` default is byte-identical to the pre-amendment code | met | I extracted the pre-amendment tree (`git archive 322fd85 src`) and ran both trees on 6 synthetic tables x tau in {inf, 50} (12 cases), comparing `solve_terms(...)` `W, beta, labels, objective, history` and `HyperbolicTradeSpace(n_terms=3).fit` `exponents_, facet_` with `np.array_equal`: **all 12 identical**. The generator change (below) alters only K > 1 planted data where a facet had < d+1 frontier rows, so the old-tree comparison used generator-independent tables. In-repo guard: `tests/test_solvers.py::test_default_facet_step_is_unchanged_literals` (stored literals, objective 0.708229464326431 to 1e-9). `HyperbolicTradeSpace().get_params()["facet_step"] == "support"` asserted. |
| `"tangent"` is the spike's D | met | `_tls_normal` (smallest-variance direction of the facet's near rows, constrained to the simplex via SLSQP) inside `_refit(..., tangent=True)`; near rows = own rows with `J_tau(Uw) - U w < band`, band `0.1` at tau = inf else `1/tau`, as the docs say; `beta_k` = support value over all rows in both steps; guard applied to B only, D returns the lowest-objective iterate seen (`test_tangent_keeps_best_iterate_and_is_deterministic`). I compared to the spike's description in `spike-facet-refit/README.md`, not to its code line by line. |
| Fallback below d+1 near rows | met | `if near.sum() > U.shape[1]` is exactly `>= d+1`; `test_tangent_falls_back_to_support_without_enough_near_rows` passes (D equals B to 1e-9 on a 12-row table). |
| First iteration is B | met | `_solve_terms_once` calls `_refit(U, labels, W, beta, tau, kw)` (no `tangent`) for the initial fit; only in-loop refits pass `tangent`. Docstring and method page say so. |
| beta over all rows | met | `W[k], beta[k] = w, log_mean_exp(U @ w, tau)` on the full `U` in both steps. |
| Generator guarantees >= d+1 frontier rows per facet; K = 1 identical | met | `_identifiable` is called only in the `else` (K > 1) branch; `test_k_terms_every_facet_has_d_plus_one_frontier_rows` (20 seeds, d = 4, plus a noisy d = 3 K = 2 case, determinism) and `..._too_few_rows_..._raises` pass; the K = 1 datasets tests (unchanged) pass; the old-tree comparison above and the empty notebook diff cover K = 1. A side effect, disclosed in the docstring Notes: the realized frontier fraction can slightly exceed `frontier_fraction` for K > 1. |
| Docs: per-facet problem, both steps | met | `docs/method.md` "The per-facet problem as step 2 solves it" (B, the support-function objective), "Step D, the evidence-driven alternative", the pseudocode in given/repeat/until form with the guard; own-rows ill-posedness with the 0/60 vs 60/60 oracle numbers cited to spike section 3a. |
| Docs: objective | met | "The objective" paragraph: mean slack as the K > 1 analogue of the K = 1 reach, why the sum of reaches is degenerate, the measured 0.000 worsening fraction for B cited to spike-objective table 1. I spot-checked `spike-objective/mono.csv` (header and first rows: `worse` 0.0 for B); I did not recompute the 35-50 % D figure. |
| Docs: monotone-guarantee sentence and the paper presents mean slack | met | `method.md` "Which step the paper presents": "the paper presents the mean-slack approach, step B, because of its monotone guarantee"; same in `docs/api.md` ("this is the step the paper presents"), assumption 5 and `limitations.md`. |
| Docs and docstring: measured recovery for BOTH steps | met, numbers verified | `solve_terms` docstring, `method.md` ("Measured recovery", "Only observed (i)"), `api.md`: B 17/20 (tau inf; fails 1, 3, 16) and 16/20 (tau 50; fails 1, 3, 8, 16); D 16/20 (inf; fails 1, 3, 8, 16) and 17/20 (50; fails 1, 3, 16). Independent re-measurement below matches every count and every failing seed. |
| Docs: simplifying assumptions with parked alternatives | met | `method.md` assumption 5 ("The per-facet step") names the choice, defends it, and parks D (kept in code) and the frontier-weighted objective (slack on near rows only, entropic variant), with the reason; `limitations.md` repeats it. |
| `docs/api.md` documents `facet_step` | met | paragraph at the `HyperbolicTradeSpace` section, both values, fallback, non-monotonicity, measured rates, `ValueError` for other values; estimator numpydoc has the parameter. |
| Stale text from the first review | fixed | `TermsResult.objective` docstring now says mean slack; no `19 or 20` claim left except the correctly conditioned "At N=600 with half the rows on the frontier" sentence; `grep` for `sum_k (n_k` and `n_k/N` finds nothing. |

### Independent recovery re-measurement

Script `/private/tmp/claude-501/scratch/rec.py`: `make_frontier_data(400, 4, n_terms=3, random_state=s)`, s = 0..19, `HyperbolicTradeSpace(n_terms=3, temperature=tau, random_state=0, facet_step=step)` defaults otherwise; pass = max exponent error < 0.05 after `linear_sum_assignment` matching and >= 90 % of frontier rows on the matched facet.

| step | tau | passes | failing seeds (error, row fraction, fewest frontier rows on a facet) |
|---|---|---|---|
| support | inf | **17/20** | 1 (0.468, 0.96, 5), 3 (0.118, 0.95, 6), 16 (0.437, 0.94, 5) |
| support | 50 | **16/20** | 1 (0.32, 0.54, 5), 3 (0.113, 0.94, 6), 8 (0.218, 0.73, 11), 16 (0.363, 0.85, 5) |
| tangent | inf | **16/20** | 1 (0.325, 0.49, 5), 3 (0.118, 0.93, 6), 8 (0.054, 0.99, 11), 16 (0.437, 0.93, 5) |
| tangent | 50 | **17/20** | 1 (0.327, 0.54, 5), 3 (0.099, 0.94, 6), 16 (0.33, 0.83, 5) |

All four rows equal the docs exactly (counts and seed lists). Note: tangent at tau = inf seed 8 fails by 0.004 (error 0.054 against 0.05), so that count is threshold-sensitive; the docs state the threshold. The docs' explanation (seeds 1, 3, 16 have a facet with only 5 or 6 frontier rows, which is the minimum the generator now guarantees; seed 8 has 11) agrees with the last column. The claim "D recovers about as often as B" is borne out; D does not recover more at the defaults, so the gain the first spike measured (16 to 19 vs 12 to 19 from one start) does not show up in the five-restart default, which the docs do not hide.

### Requirements, re-verified (original IDs, amended where the amendment says)

| ID | Verdict | Evidence |
|---|---|---|
| R-1 (amended: states the >= d+1 condition) | met as amended | `test_k_terms_recovers_planted_facets` and the new `test_k_terms_both_steps_recover_under_identifiability` (both steps x seeds 0, 2 at inf, 0, 4 at 50; each asserts the generator's >= 5 frontier rows per facet) pass. The measured rate on 20 seeds is the table above, quoted in the docs, with the cause. Not universal: stated honestly. |
| R-2 | met | `test_terms_monotone_history_and_stops`, `test_terms_k1_equals_slsqp_and_degenerate` pass (full suite). Monotone for B; D's non-monotonicity tested and documented. |
| R-3 | met | `test_k_terms_round_trip_and_scores` (K in 2, 3 x kappa in inf, 5) pass. |
| R-4 | met | `test_k3_reports_one_per_facet_recover_planted_supports` (3 seeds) pass; comparison is `sorted(...)`, order-free. |
| R-5 | met | `parametrize_with_checks` for `n_terms=3`, `n_terms=3` with finite kappa, and the new `n_terms=3, facet_step="tangent"`; `EXPECTED_FAILURES` still empty; all pass with `xfail_strict=True`. |
| R-6 | met for K = 1 behaviour; literal wording unmet as before | See the old-assertion list below. Notebook and `tests/test_notebook.py` diff empty. |
| R-7 | met (unchanged by the amendment) | `tests/test_k_terms_case.py` (default step only, per the amendment) passes; figures and record not regenerated by the amendment (`git diff --stat 6c304a8 HEAD -- examples docs/superpowers/notes/k3-cubesat.md` shows no change). First review's remark on figure weakness (G-6) stands. |
| R-8 | met | 256 of 300 net lines; no new dependency. |
| R-9 (amended: both steps) | met | method page states the algorithm for both steps, B default with the reason; claims no global optimality ("Nothing is claimed about global optimality", assumption 2, `api.md`); `tests/test_docs.py`, `tests/test_narrative.py` pass; `grep -rn -i "documented, not built"` hits only kernel methods. |
| R-10 | met on HEAD and on the two amendment code/docs commits (CI success on 19383f8 and 6b4e773) | commands above; earlier-commit runs also success per `gh run list`. |
| R-11, R-12 | met | `test_reweighted_l1_*`, `test_penalty_*`, L11 derivation and narrative tests pass in the suite; `derivation/run.py` ends `ALL LEMMAS PASS.` |

### Old-test assertions removed or edited (`git diff 3bebe3e HEAD -- tests/`)

Unchanged list from the first review; no new removals since 6c304a8 except the import line in `test_solvers.py`.

1. `tests/test_estimator.py::test_n_terms_not_implemented` removed (`pytest.raises(NotImplementedError ...)` for `n_terms=2`): required by G2; replaced by a passing-behaviour test. Conflicts with R-6's "additions only" wording.
2. `tests/test_derivation.py` `unused = [n for n in AX.AXIOMS if n not in used and n not in AX.STRUCTURAL]` gained `and n not in AX.SOLVER_LEVEL` (I7): a small weakening of an audit, named and printed.
3. `tests/test_docs.py` `1 <= n <= 10` -> `<= 11` (L11).
4. `tests/test_narrative.py` `range(1, 11)` -> `range(1, 12)` (L11).
5. `tests/test_tensions.py` import line adds `make_frontier_data` (no assertion change).
6. `tests/test_solvers.py` import line `from scipy.optimize import check_grad` -> `check_grad, linear_sum_assignment` (new in the amendment; no assertion change).

### Order and platform tie-breaks (the Linux failure class of run 42518318170)

Searched the K > 1 tests for assertions on facet labels or order. Findings:

- Order-free (good): recovery tests use `linear_sum_assignment` and compare after matching (`test_estimator.py`, `test_solvers.py` tangent test); `test_tensions.py` compares `sorted(contending sets)`; the literal-pinning test `test_default_facet_step_is_unchanged_literals` sorts rows by first column before comparing (its comment says facet order is arbitrary); `test_k_terms_improvement_factors_use_assigned_facet` uses the assigned facet's own argmax; `test_k_terms_zero_rows...` compares two same-seed fits; `test_log_plane_k3_draws_envelope_and_facet_legend` was already made a set test. All K > 1 tests, including the Amendment 1 ones, passed on Linux CI (runs 42524420226 and 42524561753).
- Residual order dependence, low risk, not currently failing:
  1. `tests/test_plotting.py::test_surface_k3_and_coordinates_facet_colouring` asserts `"facet 1" in _texts(ax)` (K = 3, d = 3, one seed): it assumes facet index 0 owns at least one row. A platform tie-break that emptied facet 0 (as happened to a facet in the d = 2 duplicate case) would fail it. It passed on macOS and on Linux CI.
  2. `tests/test_plotting.py::test_plot_tensions_list_of_reports_side_by_side` asserts `axs[1].get_title().startswith("facet 2: dilemma")`; this is about the report list index, which is deterministic by construction (not a label permutation issue).
  3. `tests/test_k_terms_case.py` asserts `(np.bincount(est.facet_, minlength=3) > 0).all()` (no empty facet in the cubesat K = 3 fit, seed 0) and `diag.objective_.is_monotonic_decreasing` over K = 1, 2, 3. Both are about outcome, not order, and are numeric-platform sensitive in principle; they passed on CI. The cubesat tests use the default step only, as the amendment says.
  4. `tests/test_tensions.py` `match="facet 0"` names the first facet checked, deterministic.
- No `argsort`-free ordered comparison of exponents across facets, and no assertion like `labels[...] == k` against planted labels without matching, was found.

### Outside the scope (amendment-era)

Out-of-scope but expected: the two spike folders `docs/superpowers/notes/spike-facet-refit/` and `spike-objective/` (+30 k lines of scripts, CSV and READMEs; the research the supervisor requested at the gate; ~23 k lines are one CSV, `mono.csv`), the ruff `extend-exclude` in `pyproject.toml` to keep throwaway scripts out of lint, and the decision-record entries in `WP9-decisions.md`. No non-goal touched: no performance or scalability code, no kernels, K = 1 results, notebook and datasets untouched, no paper or site files, no change to the cubesat record or figures.

### New gap list

| Gap | Description | Suggested disposition |
|---|---|---|
| G2-1 | Recovery is 16 to 17 of 20 seeds for either step and either tau. Failures are facets with exactly 5 to 6 frontier rows (the generator's minimum) plus one seed (8) with a well-populated facet in a local optimum. The amendment's "evidence-driven" D does not beat B at the defaults (16/17 vs 17/16). Fully disclosed in docstring, method, api and limitations. | accept as is; the paper (WP10) should quote the measured rates, not "recovers" |
| G2-2 | D's seed-8 result at tau = inf misses the 0.05 criterion by 0.004 (error 0.054); the "16/20" count is threshold-sensitive. | accept as is (docs state the threshold); optional follow-up |
| G2-3 | R-6 literal wording ("additions only") still not achievable: `NotImplementedError` test removed, ceilings raised, one audit exemption. | accept as is (same as G-4 of the first review) |
| G2-4 | Plotting test `"facet 1" in _texts(ax)` assumes facet index 0 is non-empty; the cubesat case test asserts no empty facet. Not failing on macOS or Linux CI, but the same class as the 42518318170 failure. | accept as is, or follow-up (make `test_surface_k3_and_coordinates_facet_colouring` assert any `facet \d` label). Not worth blocking acceptance. |
| G2-5 | The generator now moves extra rows onto the frontier for K > 1, so the realized frontier fraction can exceed `frontier_fraction` and K > 1 planted data differ from pre-amendment data on seeds that needed a top-up (any pre-amendment K > 1 numbers outside the repo, such as WP10 drafts, would not reproduce on those seeds). Documented in the docstring Notes. | accept as is |
| G2-6 | The D-related percentages in the docs (35 to 50 % worse refits; 16 vs 12 of 20 from one start) come from the spike tables and were not recomputed by me; B's 0.000 was spot-checked in `mono.csv` only. | accept as is (sources cited); or follow-up to add a one-line recompute test |
| G2-7 | First-review gaps G-6 (figure legibility) and G-7 (`frac_above_` rises with K) are unchanged by the amendment and remain open follow-ups for WP10. | follow-up work package, as before |
| G2-8 | Spike folders add about 30 k lines (mostly CSV) to the repo. | accept as is (requested research, ruff-excluded); note for the supervisor |

No gap is suggested as "fix before acceptance".

### Recommendation

Recommend acceptance with the listed gaps noted. Reasons: every amendment item is present in code and docs and was verified by running it (the default step is bit-identical to the pre-amendment code on 12 cases; D is implemented as specified with its fallback and best-iterate return; the generator guarantees >= d+1 frontier rows per facet and leaves K = 1 untouched); the recovery rates quoted for both steps were independently reproduced to the count and the seed; the full suite (1115 passed), lint, format, lock, derivation and attribution checks are clean; the code budget is 256 of 300; CI is green on the amendment's code and docs commits; K = 1 notebook and tests are untouched. The honest limits are unchanged in kind: 16 to 17 of 20 planted seeds recovered, failing where a facet has only 5 to 6 frontier rows, and the supervisor's chosen default (monotone B) is not more accurate than D, only guaranteed monotone.

Acceptance is the supervisor's act, recorded as named at the top. This report does not accept the work.

## Third review (after Amendment 2 and the G2-1/G2-3 fix)

Reviewer: fresh context, did not build the work. Reviewed `main` at bdf17b2 (`git log 27d5b04..HEAD`: 2bb5179 Amendment 2, d5ba7c0 dispositions, bdf17b2 fix). Nothing fixed; this section is the only file edited, nothing committed (`git status --short` empty before writing). Everything below was re-run.

### Checks run

| Check | Command | Result |
|---|---|---|
| Suite | `uv run pytest -q` | `1116 passed, 11 skipped, 1 xfailed` (178 s); +1 is `test_n_restarts_default_and_validation` |
| Lint / format / lock | `ruff check .`; `ruff format --check .`; `uv lock --check` | `All checks passed!`; `116 files already formatted`; `Resolved 173 packages` |
| Derivation | `uv run python derivation/run.py` | `ALL LEMMAS PASS.` |
| Attribution | `git log 3bebe3e..HEAD --format=%B \| grep -i -c "co-authored-by\|generated"` | `0` |
| K = 1 untouched | `git diff --stat 3bebe3e HEAD -- examples/adcs/adcs_trade_study.ipynb tests/test_notebook.py` | empty |
| R-8 | AST docstring-excluding count, HEAD vs 3bebe3e (`/private/tmp/claude-501/r8.py`) | **260 net** (budget 300): the 256 of the second review plus 4 for `n_restarts` in the estimator (+75 there); `solvers.py` unchanged by this fix (it already had `n_restarts`) |
| CI | `gh run list --branch main --limit 4` | 42527548929 (bdf17b2) success; 42527139679, 42527080205, 42525071154 success |

### (1) Ledger rule: met, no restructuring

- `git diff 27d5b04 HEAD --stat`: docs (api, limitations, method, proof-conventions), `estimator.py` (+9/-1), `tests/test_estimator.py` (+12), `WP9-decisions.md`, `WP9-scope-of-work.md`. Nothing under `derivation/`, nothing in `tests/test_derivation.py`, `tests/test_docs.py` or `tests/test_narrative.py`. So no code, test or ledger restructuring was done to satisfy a count.
- `proof-conventions.md` has the paragraph "Solver-level inherited entries". Accuracy against the code: `SOLVER_LEVEL = ("I7",)` in `derivation/axioms.py:31` (matches "today I7, Magnani and Boyd 2009"); `tests/test_derivation.py:118` exempts it from the every-axiom-is-used audit and `test_I7_solver_level_inherited_entry` (line 754) asserts citation, role, failure mode, membership and the printed audit (matches "carries a role and a failure mode", "listed instead of being checked for consumption", "the every-axiom-is-used audit covers the lemma-consumed entries only"); `derivation/run.py:100-102` prints it in its own section, and the run shows `INHERITED, solver level (cited by the K > 1 solver, not consumed by a lemma)` with I7's statement, role and failure mode (matches "printed in its own audit section"). The claim that a normal inherited entry is consumed by a lemma via `AXIOMS_USED` and checked by the audit is consistent with the old line `n not in used and n not in AX.STRUCTURAL`. Accurate.
- Method page: `docs/method.md:726` has the pointer sentence at I7 ("I7 is a solver-level inherited entry ... the rule is in the proof conventions, "Solver-level inherited entries""). Met. Cosmetic: it is one very long line, unlike the wrapped neighbours.

### (2) `n_restarts`: implementation met; the limitations claim is only partly supported

- Estimator: `n_restarts=5` in `__init__`, stored verbatim (`self.n_restarts = n_restarts`), validated in `fit` (`isinstance(.., numbers.Integral) and >= 1`, message names `n_restarts`), passed as `n_restarts=self.n_restarts` to `solve_terms` (which already took the keyword; `solvers.py` is not in the diff). Test rejects 0, -1, 2.5, None. Numpydoc entry present; `api.md` documents it (default, no effect at K = 1, first remedy).
- Default path byte-identical: I ran `HyperbolicTradeSpace(n_terms=3, temperature=tau, random_state=0, facet_step=step).fit` on `make_frontier_data(400, 4, n_terms=3, random_state=s)` for s in {0,1,3,8} x tau in {inf, 50} x step in {support, tangent} = 16 cases at 27d5b04 (git worktree, `PYTHONPATH` to its `src`, verified it imported the worktree) and at HEAD, and compared `exponents_` and `facet_` with `np.array_equal`: **all 16 identical**. (Worktree removed.) The in-repo test also asserts `n_restarts=5` equals the default.
- Limitations text names more restarts, a better start and the tangent step, and states the seed claim. Checked against `spike-objective/README.md` line 104 ("Passing restarts of 5 on the bad seeds"): inf: s1 B 0 D 0; **s3 B 3 D 3; s8 B 2 D 3**; s16 0/0. tau 50: s1 0/0; **s3 B 0 D 3; s8 B 0 D 5**; s16 0/0. So:
  - "seeds 1 and 16 none" is supported exactly (0 of 5 for B and D, both tau).
  - "seeds 3 and 8 two or three of the five pass" is supported **only at tau = inf** (B: 3 and 2; D: 3 and 3). At tau = 50 for the default step B it is 0 and 0 (D: 3 and 5). The text does not say tau or step. Not exactly supported as written.
  - The consequence drawn, "so more restarts or a better selection rule would recover them", is **not supported for more restarts**. I measured the built solver with `n_restarts` 5, 20 and 50 on seeds 1, 3, 8, 16 (same pass criterion as the earlier re-measurement; script `/private/tmp/claude-501/scratch/rec2.py`). Seed 3 fails at every count, both steps, both tau. Seed 8 with the default step at tau = inf passes at 5 restarts and **fails at 20 and 50** (error 0.507): more restarts moved the mean-slack winner to a worse-recovering partition. Tangent at tau = 50 passes seed 8 at 5 (the one pass in those four seeds) and fails at 20 and 50. Seeds 1 and 16 fail throughout. So extra restarts did not recover a single failing seed and cost one recovery. The spikes' passing restarts exist among the five, but the mean-slack selector does not pick them (the README says an edge-count selector at tau = inf recovers 3 and 8, 18/20). The docs' "better selection rule" half is right; "more restarts" is not, and the `api.md` sentence "More restarts are the analyst's first remedy for a local optimum" and the limitations line "the analyst's options are more restarts ..." overstate it for this selector. In the second paragraph, "More restarts do not cure this (no restart passes on seeds 1 and 16)" is correct.

### (3) R-6 as restated in Amendment 2: met; the six edits, again (`git diff 3bebe3e HEAD -- tests/`, removed or edited lines)

Restated R-6: K = 1 behaviour and the notebook unchanged, pre-existing K = 1 assertions intact, edits forced by approved deliverables listed with reasons. Notebook and `tests/test_notebook.py` diff is empty; the full suite passes; the K = 1 path is also byte-identical (second review's old-tree comparison; unchanged by this fix).

| # | Edit | Reason, against the new wording |
|---|---|---|
| 1 | `test_estimator.py::test_n_terms_not_implemented` removed (`NotImplementedError` for `n_terms=2`) | A feature that now exists (the package's deliverable D-1); the assertion is false by design. Not a K = 1 assertion. |
| 2 | `test_derivation.py` unused-axiom audit gains `and n not in AX.SOLVER_LEVEL` | A lemma-less inherited entry (I5/I7) that the approved derivation default requires; documented by the new proof-conventions paragraph. A narrowing of an audit, named and tested (`test_I7_...`); K = 1 untouched. |
| 3 | `test_docs.py` `1 <= n <= 10` to `<= 11` | L11 now exists (R-11). |
| 4 | `test_narrative.py` `range(1, 11)` to `range(1, 12)` | L11 now exists. |
| 5 | `test_tensions.py` import adds `make_frontier_data` | No assertion change. |
| 6 | `test_solvers.py` import adds `linear_sum_assignment` | No assertion change. |

Edits 1 to 4 are forced by approved deliverables; 5 and 6 are imports. Each fits the restated R-6. Also in the diff, the new `test_n_restarts_default_and_validation` is an addition. No K = 1 assertion was removed or weakened.

### (4) Non-goals and out-of-scope

No non-goal touched (no kernels, performance code, K = 1 results, paper or site). The fix touched only the files listed in (1). No new dependency.

### (5) Gaps

Beyond G2-7 (figure legibility, `frac_above_` by K; follow-up) and the accepted minors G2-2, G2-4 to G2-6, G2-8, **one new gap**:

| Gap | Description | Suggested disposition |
|---|---|---|
| G3-1 | The G2-1 documentation condition says "more restarts" is a remedy and cites seeds 3 and 8 as recoverable that way. The spikes' counts hold only at tau = inf (at tau = 50 the default step has 0 passing restarts of 5 on both seeds), and with the built mean-slack selector more restarts did not recover any failing seed (3 never; 8 passes at 5, fails at 20 and 50; 1 and 16 never). The restarts that pass exist but the selector does not choose them. `api.md` ("first remedy") and `limitations.md` (twice) overstate it. The condition the supervisor set was that the understanding be recorded accurately. | Fix before acceptance, docs only, a few lines: say that at tau = inf the spikes found passing restarts among five on seeds 3 and 8 (at tau = 50 only for the tangent step), that mean-slack selection does not pick them and extra restarts can lose a recovery (seed 8 at 20 restarts), so `n_restarts` is a cost-for-robustness knob and the remedy that worked in the spikes is a different selection rule or a better start. Reword "first remedy" in `api.md`. Alternative: accept as is and record the caveat in the decision log. |

Everything else requested is met: the ledger rule and its pointer, the keyword and its test, the default path unchanged, R-6 restated and satisfied, the full checks green, CI green.

### Recommendation

Accept after G3-1 is either fixed (docs only) or knowingly accepted by the supervisor; no other open item blocks. The acceptance act remains the supervisor's; this report does not accept the work.

### G3-1 disposition (PM, after the third review)

The overstatement in `docs/api.md` and `docs/limitations.md` ("more restarts" as a remedy) is
corrected to the reviewer's measurements: scope tau = infinity for the spike restarts; selection by
mean slack, not the restart count, is the limit; extra restarts can lose a recovery (seed 8, step
B, tau = infinity); `n_restarts` is a cost-for-robustness knob. Docs only; no code or test change.

## Fourth review (after Amendment 3)

Reviewer: fresh context, did not build the work. Reviewed `dev` at 48f241a (delta `git diff 0b0bcbc HEAD`: a15566b E-4, 094e86d Amendment 3, 48f241a branching process). Nothing fixed; this section is the only file edited, nothing committed (`git status --short` empty before writing). Everything below was re-run. Scratch: `/private/tmp/claude-501/-Users-z--claude-spares-spare-4Zb8mW/71474a52-35d3-48fa-82b0-c1328e96b5d6/scratchpad/` (`runk.py`, `k_out.txt`, `figs/`, `band.py`).

### Checks run

| Check | Command | Result |
|---|---|---|
| Suite | `uv run pytest -q` | `1122 passed, 11 skipped, 1 xfailed` (206 s); +6 over the third review (new: tau-reselection, every-facet-drawn, two plotting tests, and the split of the figures test) |
| Lint / format / lock | `ruff check .`; `ruff format --check .`; `uv lock --check` | `All checks passed!`; `117 files already formatted`; `Resolved 173 packages` |
| Derivation | `uv run python derivation/run.py` | `ALL LEMMAS PASS.` (diff to `derive`/`verify` is prose only: docstring and ledger role/failure-mode text in `axioms.py`, `lemma_10_extension.py` lines 11-12; the executable asserts `ceil - log K/kappa == 0` at line 129 are untouched) |
| Attribution | `git log 3bebe3e..HEAD --format=%B \| grep -i -c "co-authored-by\|generated"` | `0` |
| K = 1 / notebook | `git diff --stat 3bebe3e HEAD -- examples/adcs/adcs_trade_study.ipynb tests/test_notebook.py` | empty |
| R-8 | AST docstring/comment/blank-excluded count, HEAD vs 3bebe3e (`/private/tmp/claude-501/r8.py`) | **262 net** (budget 300): 260 of the third review plus 2 (the `PARTICIPATION` constant and the `if ok.any():` guard in `plotting.py`) |
| CI | `gh run list --branch main --limit 4` | 42530244023 (094e86d) success, 42530248162 (48f241a) success (after finishing while I reviewed), 42529690560, 42529624440 success. Note `main` already carries these commits; `dev` is the same tip |

### (1) Amendment 3, item by item

**D-6, re-selection at each K: met.** I ran `k_terms.run_regime(regime, figs=<scratch>)` for both regimes (the script's own function; committed figures untouched; `git status` clean) and compared every number of `docs/superpowers/notes/k3-cubesat.md` with the printout.

- Re-selected tau, band, objective_, frac_above_, facet rows, shares, all identical to the record. Primary: K=1 38.10 / 0.0262 / 0.2036 / 0.096 / 706; K=2 113.22 / 0.0088 / 0.1384 / 0.096 / 332, 374 / 0.371, 0.629; K=3 195.18 / 0.0051 / 0.1173 / 0.098 / 201, 188, 317 / 0.089, 0.133, 0.778. Stock: K=1 41.72 / 0.0240 / 0.1312 / 0.104 / 780; K=2 78.75 / 0.0127 / 0.1059 / 0.092 / 390, 390 / 0.694, 0.306; K=3 162.78 / 0.0061 / 0.0929 / 0.094 / 284, 149, 347 / 0.077, 0.590, 0.333. **K=1 tau 38.10 and 41.72 unchanged.** No warnings in the run (stdout and stderr captured), consistent with "bracketed at every K, no warning".
- Facet tables (K=3 and K=2, both regimes): every row, contending set (in order), n-lemma, three largest exponents, near-frontier count (17, 33, 126; 35, 88; 20, 71, 47; 67, 29), reach beta_k and share match.
- K=1 vs K=3/K=2 relation paragraphs (shares "five of six", "four of seven", union of nine and ten, K=1 subset of the union in primary, not in stock, eclipse reserve and power margin absent) match the script's `relation` output line by line. "Only facet containing total mass (K=3, both regimes)" holds (primary facet 3, stock facet 2).
- Fixed-tau diagnostic table matches (primary 0.261, 0.382; stock 0.204, 0.338; objective_ 0.0900, 0.0529, 0.0678, 0.0326; sizes and shares). The "re-selection changed" paragraph (302,190,214 to 201,188,317; 0.669 to 0.778; settling time now in both control-effort facets; stock sizes, unchanged sets, 0.161 to 0.590, 0.307 to 0.077; objective ratio about a quarter at fixed tau: 0.0529/0.2036 = 0.26, 0.0326/0.1312 = 0.25) matches the fixed-tau per-facet table the script prints.
- Seed stability (seeds 0-4): primary objective_ 0.117334/0.117333 (below 2e-6), frac_above_ 0.0977 (0.0991 for seeds 2, 4), shares identical, sets identical; stock seeds 0, 1, 3, 4 agree (0.092872, 0.09359), seed 2 differs (0.114273, 0.0756, shares 0.2, 0.24, 0.56, different sets). Matches the text.
- The "own band" claim that some K=2/3 facets have 3 to 6 designs in their own band 1/tau_K: I counted (`band.py`): primary K=3 [4, 6, 35], K=2 [13, 22]; stock K=3 [3, 23, 13], K=2 [34, 15]. So at K=3 three facets are below 10 (4, 6, 3), and `tension_report` would refuse them; the statement is true for K=3 (the record's "3 to 6" is exact) and not for K=2.

**Use of K=1's band for reports, slices and shading: disclosed and defensible, with one reading cost.** Disclosed in the record's header paragraph, in the script's comments and in the figure section. It is defensible: it makes near-frontier counts comparable across K and avoids a refusal. Cost: for K=3 the shaded band is about five times wider than the fit's own band (0.0262 against 0.0051, primary), so "near-frontier" in the reports and the panel shading is not "within the K-facet fit's band". The record says this ("the fit itself uses 1/tau_K"), so no hidden effect; WP10 should carry the sentence.

**D-4/R-7, envelope drawn only where both weights exceed 1e-3: met.**
- `plotting.py`: `PARTICIPATION = 1e-3`; `ok = W.min(axis=1) > PARTICIPATION`; `fill_between` and `plot` guarded by `if ok.any()`. K=1 `else` branch untouched (diff shows no change there). Tests: `test_log_plane_k3_draws_facet_only_where_it_has_weight_on_both_metrics` (a facet at 0.0005 excluded though it would dominate; no lines when none qualifies) and `test_log_plane_k1_unchanged_by_the_envelope_rule` (one line, legend present). Notebook and its test unchanged.
- Consistency of the two thresholds: `_slice` in `k_terms.py` skips facets with raw `min(W[f,j], W[f,k]) <= PARTICIPATION` and passes weights renormalised by their sum, which are at least the raw ones, so plot_log_plane's own filter admits every facet `_slice` keeps. Not a defect.
- Every facet is the top-two pair of at least one panel (`slice_pairs`); `test_every_facet_is_drawn_in_some_panel` asserts the union of "facets drawn" is {1,2,3} and at most 3 panels. The script printed: primary panels (slew time, control effort) facets [1,2]; (control effort, energy balance) [1,2]; (total mass, peak slew power) [3]; stock (slew time, control effort) [1,2,3]; (pointing error, peak slew power) [2]; (control effort, energy balance) [1,3].

**The six committed `k3_*.png`, viewed.**

| Figure | Panel | Envelope visible? | Title names |
|---|---|---|---|
| log_planes_primary | slew time / control effort | Yes, one black line (the narrow grey band is hardly visible) through the lower edge of the data | "facets 1, 2 drawn" |
| | control effort / energy balance | Yes, a kinked line through the lower-left of the cloud | "facets 1, 2 drawn" |
| | total mass / peak slew power | Yes, a straight line at the upper right, above all but the last few points; data sit on discrete peak-slew-power levels | "facets 3 drawn" |
| log_planes_stock | slew time / control effort | Yes, kinked, with a steep right-hand segment | "facets 1, 2, 3 drawn" |
| | pointing error / peak slew power | Yes, a straight line well above the data (discrete levels, two clusters) | "facets 2 drawn" |
| | control effort / energy balance | Yes, kinked, bounding the upper-left | "facets 1, 3 drawn" |
| frontier_coordinates (primary, stock) | Z0-Z1 and Z0-Z2 | no envelope by construction (chart coordinates); faceted colour, band-points outlined | n/a, facet colours in legend |
| tensions (primary, stock) | one heat map per facet | n/a; contending set outlined; titles "facet k: n-lemma (n metrics contend)" | k = 1, 2, 3 |

All six log-plane panels have a visible envelope (the G-6 defect, panels with no envelope, is gone). The least informative are the two peak-slew-power slices (primary facet 3, stock facet 2): the envelope lies above nearly all of the data on a few discrete levels, which the record states. The frontier-coordinates figures read as cloud-with-structure plots; the tension maps are legible at the size shown.

**Committed PNGs against a fresh run (`ImageChops.difference`).** The four coordinates and tensions PNGs are pixel-identical to the regenerated ones. The two `k3_log_planes_*.png` differ only in a 15-pixel title line: committed shows "facets 3 drawn" and "facets 2 drawn", the script as committed now produces "facet 3 drawn" and "facet 2 drawn" (the singular `noun` branch in `log_plane_slices`). The committed log-plane figures were generated before that grammar edit and not regenerated (gap G4-1, cosmetic).

**Docs wording.** `docs/limitations.md` has the new bullet "Temperature across K": "tau is re-selected at each K by the K = 1 criterion; whether the target fraction should differ by K is open", as the amendment words it; the "Selection of K" bullet is updated too. Greps over `docs/`, `README.md`, `src`, `examples/adcs/*.py`: `'0.382'` appears only in `method.md:737` (framed as the effect of reusing K=1's tau), the record's diagnostic table and its explanation; `'rises with'` appears only in the record's diagnostic paragraph; `'fixed tau'` only in the record and in script labels; `'K-specific'` nowhere. No sentence contradicts the new record. `docs/method.md` item (ii)-(iii) numbers (0.117/0.204, 0.093/0.131, 38.1/113/195, 0.096/0.096/0.098, fixed 0.096/0.261/0.382, stock seed with 0.114 against 0.093) all match the run. Formatting nit: those new sentences are very long single lines in `method.md` (lines 735-738), unlike the wrapped neighbours.

### (2) E-4

- Grep `log K`, `\log K`, `(log K)`, `log(K)` over `docs/`, `derivation/`, `src/`, `docs/superpowers/notes/notation.md`: statements are `docs/method.md:554` (displayed bound, now `max <= Phi_K <= max + log K/kappa`), `:693` and `:750` ("within (log K)/kappa above the maximum", "moves the score by at most (log K)/kappa", both correct), `docs/api.md:190` (bound, corrected), `:199` ("within (log K)/kappa above the maximum", correct), `estimator.py:52` (docstring already correct), the F10 ledger row in `method.md:63` and `axioms.py:190-197` (reworded: lower bound is `Phi_K >= M`, failure mode is the lost lower bound and the remaining upper bound `M + log K/kappa`), `lemma_10_extension.py:11-12` (docstring corrected), tests `test_estimator.py:380` (`-1e-12 <= gap <= log K/kappa`) and `test_derivation.py:693,695` (correct). `notation.md:28` states no bound (only the hard-max limit), so nothing to correct there. The derivation `derive`/`verify` is unchanged; `derivation/run.py` passes. Met; no remaining wrong-direction statement found (`max.*- (log K)` grep empty).
- The L10 L5 distinction is intact: the L5 log-mean-exp bound `M - log n/tau <= LME <= M` remains in `lemma_05_lse_lme.py` and the F5 row, correctly (beta is the log-mean-exp).

### (3) R-7, D-4/D-6 as amended, R-8

- R-7 "both cubesat datasets at K = 3 fit" at the re-selected tau: met (`test_k3_fits_and_three_reports` for both regimes, plus `test_tau_reselected_at_each_k_holds_the_fraction`: |frac_above_ - 0.10| <= 0.011 at every K, tau K=1 equal to 38.10 / 41.72, fixed-tau diagnostic present with last fraction above 0.25); the fixed-tau diagnostic is in the script output and the record.
- D-4 as amended: the envelope rule, every facet visible in a panel, titles naming the facets drawn (met above). The Amendment's "the caption of each figure names the facets it shows" is met through the panel titles (the record's prose also lists them per panel); the figure suptitle states the rule, not facet names.
- D-6 "`select_temperature` accepts the estimator parameters it needs (`n_terms`, `facet_step`, `n_restarts`, `random_state`)": met through the existing `**params`; `tuning.py` is unchanged and the script passes `n_terms` and `random_state` (the others stay at estimator defaults, as the record says). No code change was needed.
- R-8: 262 net, within 300.

### (4) Non-goals and out-of-scope

No non-goal touched: no kernels, no K=1 numeric change, no notebook change, no paper or site. Files outside Amendment 3 and E-4 in the delta: `CLAUDE.md` and `work-packages/README.md` (the branching convention of 48f241a; a process change the supervisor directed verbatim and the README quotes). It is not WP9 deliverable content and not covered by a WP9 amendment, so the supervisor should see it, as the skill requires. The six committed figure binaries changed as Amendment 3 requires.

### (5) Tests: no assertion on facet order or on which of two equal fits a platform picks

Grep of the added test lines (`git diff 0b0bcbc HEAD -U0 -- tests | grep '^+'`) for `facet_[`, `argsort`, `order`, `sorted`, `[0]`, `equal`: only `ax.lines[0].get_data()` (the first drawn line of a hand-constructed fit). `test_every_facet_is_drawn_in_some_panel` compares a set; the K=3 test checks sizes through `np.bincount > 0` and `facet_share_.sum()`; the tau test asserts a tolerance, not a facet. The old order-insensitive tests are untouched. One platform risk remains in principle: `select_temperature` bisects on `frac_above_`, a step function of tau, and at K=3 the fit can sit at different local optima (stock seed 2 does), so the Linux value of tau or the 0.011 tolerance could differ. CI on Linux passed both pushes (runs above), so it is a watch item, not a failure.

### (6) Gaps

| Gap | Description | Suggested disposition |
|---|---|---|
| G4-1 | The committed `k3_log_planes_primary.png` and `_stock.png` carry "facets 3 drawn" and "facets 2 drawn"; the script now writes "facet 3 drawn" and "facet 2 drawn". Cosmetic. | Regenerate the two PNGs before acceptance (one command, no content change), or accept as is |
| G4-2 | The reports, slices and shading use K=1's band (about five times the K=3 fit's own band 1/tau_K); disclosed, defensible, but "near-frontier" is then not "within the K-facet band". Using 1/tau_K leaves three K=3 facets with 3 to 6 rows (I measured 4, 6, 3). | Accept as is (disclosed), and carry the sentence into WP10 |
| G4-3 | The two peak-slew-power slices (primary facet 3, stock facet 2) show the envelope above nearly all of the discrete data; legible but uninformative. The record says so; the coordinates and tensions figures carry those facets. | Accept as is; WP10 may pick other slices |
| G4-4 | `docs/method.md` lines 735-738 are very long single lines; `README`/`CLAUDE.md` branching change sits in the delta without a WP9 item. | Observations: accept as is, or reflow the paragraph at the next docs pass |
| G4-5 | Platform sensitivity of the re-selected tau at K=3 (step function, local optima) is untested beyond CI passing. | Accept as is; revisit if a Linux run ever fails |
| (carried) | G2-2, G2-4 to G2-6, G2-8 accepted minors from the earlier reviews | unchanged |

**G2-7 components.** Figure legibility: resolved (every panel of the six has a visible envelope, every facet appears in at least one panel, titles name the facets; two peak-slew-power slices remain low-information, G4-3). `frac_above_` by K: resolved (0.096, 0.096, 0.098 primary; 0.104, 0.092, 0.094 stock, within the 0.01 tolerance; the fixed-tau table is kept as the diagnostic). No component of G2-7 remains open; the K-specific target fraction is recorded as an open question in `limitations.md`.

### Recommendation

Recommend acceptance with the listed gaps noted. Amendment 3 and E-4 are met with evidence, the figures and every number of the record reproduce, the full checks and CI are green, and no K=1 result or non-goal was touched. G4-1 is the only item I would fix first (regenerating two PNGs); the rest are observations. The acceptance act remains the supervisor's; this report does not accept the work.

### G4-1 disposition (PM)

The two log-plane PNGs were regenerated by `examples/adcs/k_terms.py` (titles now "facet 3 drawn" and
"facet 2 drawn"); no content change. G4-2 to G4-5 accepted as is (G4-2 to be carried into WP10).

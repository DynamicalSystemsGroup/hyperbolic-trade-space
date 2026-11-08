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

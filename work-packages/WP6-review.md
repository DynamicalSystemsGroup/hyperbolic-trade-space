# WP6 — Review report (second pass)

| | |
|---|---|
| **Scope of work** | `work-packages/WP6-scope-of-work.md` |
| **Scope approval verified** | The named record is verbal approval quoted in `work-packages/WP6-decisions.md` (added in 83f4038): supervisor mzargham, 2026-11-08, "okay proceed", defaults approved as one item, open decisions none. The project has no PRs, so there is no merge to check. The scope's status line still reads DRAFT (O-7, accepted as is in round 1). |
| **Work reviewed** | WP6 commits 17dea12 (narrative, spec section 6, tests), bdf1c8b (unused import), 8f49253 (reword for round-1 G-3 and G-5, `docs/method.md` only). Also the WP6-relevant edits to `docs/limitations.md` made inside WP3 commits f635a04 and d0a2c0d. Reviewed at HEAD d0a2c0d. |
| **Supervisor (accepts)** | mzargham |
| **Acceptance record** | Verbal acceptance in chat, quoted in `work-packages/WP6-decisions.md`, after this report |

Reviewer: a fresh session that built none of WP6 and wrote neither the first review nor the fix. This is a COMPLETE rerun from step 1, as the round-1 disposition ("Fix G-3 and G-5 before acceptance") requires. Nothing was repaired. Mutation trials ran in a `git archive` copy of HEAD in the scratchpad, not in the working tree. Round-1 dispositions are in `WP6-decisions.md` (6b88cda).

## Deliverables

| ID | Verdict | Evidence |
|---|---|---|
| D-1 | met | `docs/method.md`, 588 lines. |
| D-2 | met | `docs/why-and-how.md`, 99 lines (unchanged since 17dea12). |
| D-3 | met | `docs/limitations.md`, 126 lines. |
| D-4 | met | `git diff 7f82d43 HEAD --stat -- docs/superpowers/specs` is the one 17dea12 hunk (23 insertions, 14 deletions) in section 6; no later spec change. |
| D-5 | met | `tests/test_narrative.py`, 9 tests. |
| D-6 | met | `work-packages/WP6-decisions.md` holds the approval and round-1 disposition records; acceptance entry pending, as expected. |

## Requirements

| ID | Verdict | Evidence |
|---|---|---|
| R-1 | met | Headings in `method.md` in order: pipeline stage table; Conditions of the theory; The model; The fit (J_tau, gradient and balance, convexity, temperature); What the stage learns (eight numbered statements, as spec 4); Tensions, not variance (with n-lemmas); Interpretation (elasticities, improvement factors, chart, pull-back, design variables); Novelty and white space; Prediction from configuration; Lineage; The posynomial and GGP extension; Research direction: kernel methods; Summary of lemma coverage. |
| R-2 | met | `uv run pytest tests/test_narrative.py`: 9 passed. Mutation trial: tag `L5` changed to `L88` fails `test_tags_resolve_and_all_lemmas_cited`. Limit: a tag swapped to another existing lemma is not caught (structure, not meaning); I checked the 22 tags by reading and found them correct. |
| R-3 | met | Checked again against code: `solvers.log_mean_exp` (LME), `solvers.support_weights` (p), `solvers.objective_and_grad` (U^T p), `coordinates.to_frontier_coordinates`/`helmert_basis`, `HyperbolicTradeSpace.improvement_factors`, `.project`, `.novelty_score`, `n_terms` guard in `.fit`. All agree with the formulas; `test_referenced_functions_exist` passes. Missing pointers for L4, L6 and the L3 balance equation were round-1 G-2, accepted as is. |
| R-4 | met | Conditions table ids {R1, A4, F5, F10} equal the ledger set; R1, F5, F10 role and failure mode equal `derivation/axioms.py` verbatim (`test_conditions_table_quotes_ledger_role_and_failure_mode`); A4 text marked "stated here" (round-1 G-1, accepted as is). Trial: renaming F5 to F55 in the ledger fails that test and `test_spec_matches_ledger`. |
| R-5 | met with new gaps N-1, N-2 | See "Substantive check" below. G-3 is fixed in the places it named, but the same overstatement as G-3(d) survives in one other sentence (N-1), and one support-function sentence goes beyond I3 (N-2). Posited axioms without failure-mode text: round-1 G-4, accepted as is. |
| R-6 | met | "Tensions, not variance" in `method.md` and `why-and-how.md` against spec 2: PCA spread; soft maximum of w.u over the simplex; smallest upper extent, binding constraint; w is the tension and ratios the exchange rates; w_j = 0 free at the balanced point; spread moves to the chart, principal directions are exercised trade-offs, co-moving metrics aligned not in tension. Unchanged by 8f49253. |
| R-7 | met | Same section and `limitations.md`: K = 1 finds one tension; several regional tensions are K > 1; deflation-style search a research question, not claimed; HoroPCA disambiguated with `[@chami2021horopca]`. |
| R-7a | met | n-lemma subsection against spec 2: facet whose normal has exactly n positive exponents; discovered as the support of w; exact at tau = infinity, smooth at working tau; `min_exponent` must be 0; K = 1 reveals contention at the balanced point; regional n-lemmas are K > 1; named dilemmas are heuristics; no case asserted to have a trilemma. `limitations.md` repeats the limits. |
| R-8 | met | `why-and-how.md` covers tensions, V = 1, the chart, the five-stage workflow, inputs and outputs in prose; links to method and limitations; case study by concept; `api.md` for tools. |
| R-9 | met | `limitations.md` lists every limit named by R-9, each with its reason, plus n-lemma limits, prediction, K > 1 and kernels as documented-not-built. |
| R-10 | met | `test_citation_keys_resolve` passes; trial with key `@nosuchkey2000` fails it. Prior-art statements re-read against `docs/literature.md` (Charnes, Andersen, Fare 1994, Aigner 1968/1977, Afriat, Battese, Hoburg, Boyd, Magnani, Schoelkopf, Chami, Rockafellar, Foellmer): consistent; the two round-1 gaps (DEA limit object; Magnani and Boyd link) are now worded as lit supports (see below). No priority or novelty claim; `grep -in 'priority'` shows only "claims nothing about priority". |
| R-11 | met | `test_spec_matches_ledger` passes. I parsed spec section 6 myself: L1 [A1,A2], L2 [A2,A3], L3 [A2,A3,R1], L4 [A1,A3], L5 [A3,I1,I2,I3,F5], L6 [A2,A5,I5], L7 [A1,A2], L8 [A7,I6], L9 [A1,A2,A4], L10 [A2,A6,I4,F10]; each equals `AXIOMS_USED` of its module. All 17 ledger ids (A0-A7, I1-I6, R1, F5, F10) occur in the axiom paragraph. Trials: spec L6 list changed fails; spec id F10 changed to F11 fails. |
| R-12 | met | beta is the log-mean-exp throughout (the rewritten L5 paragraph says so and cites the offset identity); `HyperbolicTradeSpace` used; the method is named "posynomial invariant form". |
| R-13 | met | `uv run pytest -q`: 844 passed, 8 skipped, 1 xfailed. `uv lock --check`: resolved, no change. `ruff check .`: all checks passed. `ruff format --check .`: 94 files formatted. WP6 diff 17dea12..HEAD touches only `docs/method.md` (8f49253) and `tests/test_narrative.py` (bdf1c8b) beyond the first commit's five files. `docs/limitations.md` was edited by WP3 commits (see Outside the scope). |
| R-14 | not met for one push (G-7), otherwise met | `git log --format=%B \| grep -ciE 'co-authored\|generated with'`: 0. All 117 commits authored by Michael Zargham. `gh run list`: 17dea12 success, bdf1c8b success, **8f49253 failure**, d0a2c0d success. Red runs in the WP6 range: 8f49253 (run 42446308761) failed `tests/test_narrative.py::test_no_wp3_signatures_quoted` with "limitations.md quotes select_temperature". Cause: the WP3 commit f635a04 (run 42446279178, also red, same failure) added `select_temperature` to `limitations.md`; WP6's commit inherited the red because it sat on top. Fixed by d0a2c0d (green). The earlier red runs in the repository (WP2, WP4 commits, 3864a8a to a60b57c) predate WP6. |

## Substantive check: the round-1 overstatement findings

Compared against each lemma's "What this proves / does NOT prove" docstring and `docs/literature.md`, in the current text.

| Finding | Now | Verdict |
|---|---|---|
| G-3 consistency (statement 5) | Reads "we expect w-hat and beta-hat to converge ... an expectation, not a proved result. L5 disclaims consistency, and neither pointwise-to-uniform convergence nor convergence of the minimizers is proved". SLLN pointwise convergence is attributed to I2. L5 docstring: "does NOT prove consistency (I2), uniform convergence". | worded to the lemma |
| G-3 K > 1 optimism | `method.md` (caveat 2 and the extension): "expected to tighten (a conjecture)" and "We conjecture ... neither proved by L10 nor tested". `limitations.md`: "expected to tighten the bound (a conjecture, not proved)". L10 docstring proves identities only. | worded to the lemma |
| G-3 "L10 carries novelty over" | Now "shift equivariance, the identity that the homogeneity, projection and invariant-form arguments rest on (whether novelty carries over unchanged is expected ..., not proved by L10)". `limitations.md` repeats the split. | worded to the lemma |
| G-3 "LSE overshoot diverges with N" | Now states the identity LSE = LME + (log N)/tau, "at least the maximum", offset grows with N, and "proves no more about the size of the excess over the maximum (only bounded above by (log N)/tau)". The "intended way" consequence is labelled "our reading, not a lemma". The page is now more careful than the L5 docstring's own phrase "diverges like (log n)/tau" (the docstring is outside WP6). | worded to the lemma |
| G-3 chart bijection | Chart paragraph now: L8 proves u <-> (Z, log-scale) bijection; the step to (Z, log V) is "ours, using A2 and the fitted w", affine not linear, with the algebra w.u = 1^T u/d + w.B^T Z checked by me; Needs now lists A2; prediction paragraph cites "L8 with A2 and A7". **But statement 6 (line 291) still says "The map (log V, Z) is a linear bijection of log space" with no qualifier.** | partly fixed: N-1 |
| G-5 "DEA is the limit object" | Now: DEA "computes hulls of the data; the log-convex hull of the data is the limit object ..., in the sense of the object that DEA-style hull methods compute (the project's reading)". `literature.md` says "the data's convex hull is the limit object in the spec's hierarchy". Marked as the project's reading; no longer attributed to DEA. Residual wording ambiguity (O-9). | worded to the source |
| G-5 Magnani-Boyd link | Now: "That the max of affine functions is the kappa -> infinity limit ... is the project's own statement (L10 proves the limit; Magnani and Boyd do not state this link)", matching `literature.md` lines 124-129. | worded to the source |

### Fresh scan for new overstatements of the same kind

Sampled 22 claims across the three pages and checked each against the lemma docstring or literature entry.

Faithful: (1) L1 homogeneity and invariant form, Needs A1, A2. (2) L2 shift, silent on per-metric rescaling. (3) L3 gradient and balance, "does not prove interior, existence, uniqueness, sign of lambda" matches the docstring. (4) L4 convexity, "not strict convexity" matches. (5) L5 limits under F5, with the pointer to the F5 table row. (6) L5 lim tau->0 LME = mean, and `limitations.md` "weights approach uniform, soft maximum approaches the mean (L5)" (the WP3-driven edit): consistent with L5 and L3, and the "not monotone below tau about 3" claim is supported by `docs/api.md` lines 56-61. (7) L6 Gaussian cumulant tau sigma^2 ||w||^2 / 2, "ridge" labelled an interpretation in `method.md`. (8) L7 elasticities, "L7 proves them for F itself and does not say they are those of the balanced point". (9) L8 existence of B not claimed. (10) L9 pull-back, "does not say a conditioning is appropriate". (11) L10 limit under F10, "proves identities ... no K > 1 solver". (12) Statement 3 depth 1/tau "a reading of the L3 weights, not a separate lemma". (13) Statement 1 entropic risk monotone in tau "a standard property, not a lemma here". (14) HoroPCA disambiguation, lit-consistent. (15) Kernel direction: "no source we know", support-vector analogy "a hypothesis". (16) Lineage statements for Cobb-Douglas, Shephard, Farrell, Aigner, Afriat, COLS. 

New findings:
- **N-1.** `method.md` statement 6 ("Invariances", line 291): "The map (log V, Z) is a linear bijection of log space with Z independent of w". L8 proves only the (Z, log-scale) bijection; the paragraph the fix edited now says the step to log V is ours, affine and needs A2. Statement 6 still carries the unqualified "linear" claim with no A2. This is the G-3(d) sentence pattern surviving in a second place.
- **N-2.** `method.md` statement 1 (line 238): "A closed convex set is determined by its support function (I3) ... so a softened support function over positive directions carries the log-convex hull of the admissibility set". I3 says the full support function determines the closed convex set. The fit uses only directions w in the simplex (positive), which determines only the monotone (downward-closed) hull, not the hull itself. The sentence reads stronger than I3. A hedge such as "the part of the hull visible from positive directions" would fit.
- Minor wording (O-9, observations): the tau -> 0 sentence in `method.md` ("degenerates to a vertex of the simplex") follows from L5's pointwise limit but convergence of the minimizer is not proved and the sentence is unqualified (L5 gives only the limit of the objective); `limitations.md` says "the ridge toward balanced exponents (L6)" while `method.md` correctly calls the ridge an interpretation; `why-and-how.md` says the fit "reports the metrics whose weights are positive", whereas at finite tau all weights are typically positive and the n-lemma reading is graded (as `method.md` and `limitations.md` say); "Far from the diagonal ... V-1 is conservative / reliable near the balanced region" is stated as fact in three places, from spec 4, with no lemma behind it (round-1 O-level, same as K > 1 spec claim, but here worded as established); statement 5 says I2 is "checked in the tests by replication", which tests invariance under replication, not convergence.
- WP3-driven edits to `limitations.md` (f635a04, d0a2c0d) are WP6-consistent: the small-tau sentence replaces an earlier unsupported "degenerates to a vertex" in that file with the L5 mean limit and defers to the API page; `frac_above_` is a WP2 estimator attribute (`estimator.py:65`), not a WP3 signature; the final form (d0a2c0d) removed `select_temperature` and passes `test_no_wp3_signatures_quoted`.

## Definition of good enough

| Item | Verdict | Evidence |
|---|---|---|
| D-1 to D-6 exist at the stated paths | met | See Deliverables. |
| R-1 to R-14 pass as checked, with evidence in the review | met with gaps | R-5 is qualified by N-1 and N-2; R-14 by G-7. |
| Non-goals untouched | met | See Outside the scope. |
| Every ledger condition stated with role and failure mode (R-4), and the PCA contrast with limits (R-6, R-7) | met | See R-4, R-6, R-7. |

## Outside the scope

- **Out-of-scope changes:** none by WP6 commits. `docs/limitations.md` (a WP6 deliverable) was edited inside WP3 commits f635a04 and d0a2c0d (a small-tau paragraph and a K > 1 hedge). The K > 1 hedge edits at `limitations.md` lines 40 and 106 are the WP6 fix from 8f49253's wording, landed in WP3's commit; they are WP6-consistent. `work-packages/README.md` lists the WP6 delivery range as 17dea12..bdf1c8b, omitting the fix commit 8f49253 (O-10).
- **Non-goals touched:** none. No code, `derivation/`, `references.bib`, `api.md`, site configuration or notebook changes by WP6. No priority claim; deflation is stated as a research question.

## Observations (not counted as failures)

- O-5, O-6, O-7, O-8 (round-1 G-6): test limits (structure not meaning), spec wording edits beyond lists, DRAFT status line, scratchpad note. Disposition recorded: accept as is.
- **O-9.** Wording points listed under the fresh scan (tau -> 0 vertex, L6 ridge in `limitations.md`, "weights positive" in `why-and-how.md`, optimism stated as fact, replication "check", and the DEA sentence's "log-convex hull ... DEA-style hull methods compute", since DEA computes hulls in metric space, not log space).
- **O-10.** The README delivery range for WP6 should read 17dea12..8f49253 (plus later review-driven fixes).
- The L5 docstring item 2 ("diverges like (log n)/tau") is looser than the identity it proves; the narrative is now stricter than the docstring. Outside WP6's scope.

## Open decisions (for the supervisor)

Round-1 items G-1, G-2, G-4, G-6 carry their recorded disposition (accept as is); G-3 and G-5 were "fix before acceptance" and the fix has been reviewed above. New items are pending.

- **N-1.** Statement 6 in `method.md` still says "linear bijection" for (log V, Z) with no A2 and no "ours". — options: accept as is / fix before acceptance / follow-up work package. Disposition: pending.
- **N-2.** Statement 1 says a softened support function over positive directions carries the log-convex hull; I3 supports only the full support function determining the closed convex set. — options: accept as is / fix before acceptance / follow-up work package. Disposition: pending.
- **G-7.** R-14 "CI green on every push": WP6 commit 8f49253 was red, because WP3's f635a04 broke WP6's `test_no_wp3_signatures_quoted`; green again at d0a2c0d. — options: accept as is / fix before acceptance / follow-up work package. Disposition: pending.
- **O-9, O-10 (one item).** The minor wording points and the stale README range. — options: accept these as is, or pick any to act on. Disposition: pending.

## Gap dispositions

| Gap | Disposition | Reason or follow-up |
|---|---|---|
| G-1 | accept as is (recorded 6b88cda) | A4 role and failure mode written in the narrative and marked "stated here". |
| G-2 | accept as is (recorded 6b88cda) | Missing pointers for L4, L6, L3 balance: not computed by the code. |
| G-3 | fix before acceptance (recorded); fix landed in 8f49253, verified above | Four of the five sub-claims now worded to the lemmas; the chart sub-claim survives in statement 6 (N-1). |
| G-4 | accept as is (recorded 6b88cda) | The ledger records no failure mode for those axioms. |
| G-5 | fix before acceptance (recorded); fix landed in 8f49253, verified above | Both claims now worded to `literature.md`. |
| G-6 | accept as is (recorded 6b88cda) | Observations O-5 to O-8. |
| N-1 | pending | |
| N-2 | pending | |
| G-7 | pending | |
| O-9, O-10 | pending | |

## Recommendation

**Do not recommend acceptance yet.** The round-1 fixes for G-3 and G-5 are in and, for six of seven sub-claims, worded to what the lemma docstrings and `literature.md` support. All 14 requirements pass as checked (844 tests, lock and lint clean, spec section 6 equals the ledger for all ten lemmas, attribution and authorship clean, mutation trials fail the tests). But the criterion of the fix, that no claim exceed its lemma, is not fully met: the "linear bijection" sentence in statement 6 (N-1) is the same overstatement as G-3(d) in a place the fix missed, and the I3 sentence (N-2) goes beyond its source. Both are one-sentence rewords. After they are fixed (or the supervisor accepts them as is), and G-7 and O-9/O-10 are dispositioned, I would recommend acceptance with the remaining accepted gaps noted.

Acceptance is the supervisor's act, recorded as named above. This report does not accept the work.

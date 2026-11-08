# WP6 — Review report (fourth pass)

| | |
|---|---|
| **Scope of work** | `work-packages/WP6-scope-of-work.md` |
| **Scope approval verified** | Verbal approval quoted in `work-packages/WP6-decisions.md`: supervisor mzargham, 2026-11-08, "okay proceed", defaults approved as one item, open decisions none. No PRs in this project, so no merge to check. The scope status line still reads DRAFT (O-7, accepted as is in round 1). |
| **Work reviewed** | WP6 commits 17dea12 (narrative, spec section 6, tests), bdf1c8b, 8f49253, e82594b, and now 94fbe72 (round-2 wording fixes in `docs/method.md`, `docs/limitations.md`, `docs/why-and-how.md`). Reviewed at HEAD 7704ab7 (later commits are WP4b and WP3 content, not WP6). |
| **Supervisor (accepts)** | mzargham |
| **Acceptance record** | Verbal acceptance in chat, quoted in `work-packages/WP6-decisions.md`, after this report |

Reviewer: a fresh session that built none of WP6 and wrote none of the earlier reviews or fixes. COMPLETE rerun from step 1, as round 2 requires ("Fix N-3, N-4 and the wording items, accept G-7"). Nothing was repaired. Mutation trials ran in `git archive` copies of HEAD in the scratchpad.

## Deliverables

| ID | Verdict | Evidence |
|---|---|---|
| D-1 | met | `docs/method.md`, 594 lines. |
| D-2 | met | `docs/why-and-how.md`, 99 lines. |
| D-3 | met | `docs/limitations.md`, 127 lines. |
| D-4 | met | Spec change is the single 17dea12 hunk in section 6; no later WP6 spec change (`git show --stat` of the five WP6 commits). |
| D-5 | met | `tests/test_narrative.py`, 9 tests. |
| D-6 | met | `WP6-decisions.md` holds approval, round-1 and round-2 dispositions; acceptance entry pending, as expected. |

## Requirements

| ID | Verdict | Evidence |
|---|---|---|
| R-1 | met | `method.md` headings cover stage table, conditions, model, fit, the eight statements, tensions-not-variance with n-lemmas, interpretation, novelty and white space, prediction, lineage, GGP extension, kernel direction. |
| R-2 | met | `pytest tests/test_narrative.py`: 9 passed. Mutation: first `<!-- lemma: L5 -->` changed to `L88` fails `test_tags_resolve_and_all_lemmas_cited`. Known limit (accepted, O-5): a tag swapped to another existing lemma is not caught. |
| R-3 | met | Pointers checked against `solvers.py`, `coordinates.py`, `estimator.py` (earlier pass, unchanged); `test_referenced_functions_exist` passes. 94fbe72 did not touch pointers. |
| R-4 | met | Conditions table ids {R1, A4, F5, F10}; verbatim ledger role and failure mode tested. Mutation: ledger id "F5" renamed "F55" (2 occurrences) fails `test_conditions_table_equals_ledger_set`, `..._quotes_ledger_role_and_failure_mode` and `test_spec_matches_ledger`. |
| R-5 | met | See "Substantive check": N-3 and N-4 are now worded to what the lemma docstrings and `literature.md` support. Two wording-level residues (N-5, N-6) below. |
| R-6 | met | "Tensions, not variance" in `method.md`, `why-and-how.md` matches spec section 2 point by point (unchanged in substance; 94fbe72 added only the graded-participation parenthesis). |
| R-7 | met | K = 1 one tension; K > 1 regional; deflation a research question; HoroPCA disambiguated (`limitations.md`, `method.md`). |
| R-7a | met | n-lemma subsection (`method.md` 340-356) and `limitations.md` 78-82 state: facet with exactly n positive exponents; support of w; exact at tau = infinity, graded at working tau; `min_exponent` must be 0; K = 1 balanced point only; regional n-lemmas are K > 1; no case asserted to have a trilemma. `why-and-how.md` now says "the contending set, the support of the weights at infinite temperature (at a finite temperature other metrics may carry small weight)". |
| R-8 | met | `why-and-how.md`: idea, V = 1, chart, workflow, inputs and outputs, links to method and limitations. |
| R-9 | met | `limitations.md` lists each R-9 limit with its reason, plus n-lemma limits, prediction, K > 1 and kernels as documented-not-built. |
| R-10 | met | `test_citation_keys_resolve` passes. Mutation: `[@nosuchkey2000; @...]` in `limitations.md` fails it. Prior-art statements re-read against `docs/literature.md` (Cobb-Douglas, Shephard/Fare, Farrell, Aigner-Chu, Afriat/Richmond/Greene, COLS via Battese, Aigner-Lovell-Schmidt, DEA, Foellmer vs EVaR, Aitchison, Egozcue, Hoburg, Boyd, Magnani, Schoelkopf, Chami): consistent. No priority claim ("claim nothing about priority"). |
| R-11 | met | I parsed spec section 6 myself and compared with `AXIOMS_USED` imported from each lemma module: L1 [A1,A2], L2 [A2,A3], L3 [A2,A3,R1], L4 [A1,A3], L5 [A3,I1,I2,I3,F5], L6 [A2,A5,I5], L7 [A1,A2], L8 [A7,I6], L9 [A1,A2,A4], L10 [A2,A6,I4,F10]: all ten equal. All 17 ledger ids (A0-A7, I1-I6, R1, F5, F10) occur in section 6. |
| R-12 | met | beta is the log-mean-exp throughout (LSE only as contrast); `HyperbolicTradeSpace` / `hyperbolic_trade_space`; "posynomial invariant form". |
| R-13 | met | `uv run pytest -q`: 839 passed, 8 skipped, 6 xfailed (xfails belong to WP4b). `uv lock --check`: resolved, no change. `ruff check .`: all checks passed. `ruff format --check .`: 95 files already formatted. WP6 commits touch only the three docs, the spec section 6, `tests/test_narrative.py`, `work-packages/`. |
| R-14 | met on the end state; G-7 (accepted) covers the earlier red pushes | `git log --format=%B \| grep -ciE 'co-authored\|generated with'`: 0. `git log --format=%an`: 129 commits, all Michael Zargham. `gh run list --limit 8`: all eight completed/success, including 94fbe72 (run 42448847023) and HEAD 7704ab7 (run 42448940138). |

## Substantive check

Read the lemma docstrings ("does NOT prove") and `docs/literature.md` directly, not the implementer's summary.

| Item | Current text (94fbe72) | Verdict |
|---|---|---|
| N-3 DEA lineage | "Data envelopment analysis [@charnes1978measuring] is a linear-programming measure of the relative efficiency of decision-making units. The hierarchy K=1 tangent, K-facet soft maximum, hull of the data (in log space, the data's log-convex hull) is the project's own framing from the design spec, not a statement taken from the DEA literature." `literature.md` lines 73-75 say exactly the LP efficiency measure and call the hull the limit object "in the spec's hierarchy"; spec line 215 has "data's log-convex hull (DEA)". | fixed, worded to the source |
| N-4 posynomial attribution | "By definition, the data-level log-mean-exp is already a posynomial in the data (a sum of exponentials of affine terms in the log data, normalized by 1/N)". The L5 attribution is gone, but see N-5. | fixed as to attribution |
| O-11a weights limit | `method.md` "the mean by L5; the weights by their definition in L3"; `limitations.md` "softmax weights approach uniform (by their definition, L3) and the soft maximum approaches the mean (L5)". | fixed |
| O-11b ridge | `limitations.md`: "the Gaussian cumulant tau sigma^2 ||w||^2/2 (L6), which we read as a ridge"; `method.md`: "L6 proves the cumulant ... the project's interpretation ... not part of L6". L6 docstring proves only the MGF identity. | fixed |
| O-11c L7 scope | `limitations.md`: "L7 proves the elasticities -w_k/w_j for the fitted hyperplane itself; identifying them with the fit at the balanced point needs L3 and R1"; `method.md` same, with the improvement-factor scope (V against that hyperplane, w_j != 0). Matches L7 docstring ("does NOT prove that the elasticities are the ones at the balanced point (needs the fit, L3 + R1)"). | fixed |
| O-11d "reports positive weights" | `why-and-how.md`, `method.md` statement 8 (participation "the contending set at tau = infinity; at finite tau graded"). | fixed |
| O-11e conservative / reliable | `limitations.md` "Our reading (from the spec, with no lemma behind it)"; `method.md` caveat 2 "reading (spec section 4, no lemma behind it)"; `why-and-how.md` "our reading is that it is conservative". | fixed (typo N-6 below) |
| O-10 README range | `work-packages/README.md` line 58 still reads `17dea12..e82594b` and omits 94fbe72. | not changed (status table, not a WP6 deliverable); noted as N-7 |

### Fresh scan: 31 claims sampled, all prior-art statements and each watch-word sentence

Watch words: "proved/prove" (every occurrence is a negation or an attribution to a named lemma or I-item); "converge" (statement 5, "an expectation, not a proved result"; L5 "disclaims consistency"); "carries" (e^{-tau delta} factor from L3 weights; "the maximum carried as the F10 symbol"; novelty "expected ... not proved by L10"); "removes" (none); "limit object" (none left in the three pages); "bijection" (L8 for (Z, log-scale); L9 requires alpha_j != 0 and conditioning invertible; the (Z, log V) step marked as ours using A2); "ridge" (only as interpretation, three places); "reports" (code reports n_eff, fraction above; fit reports the contending set, graded).

Also checked faithful: L1/L2/L3/L4 (convexity, not strict), L5 (identity, bounds, tau limits under F5, LSE excess "only bounded above"), L7 and L10 (posynomial identity exp(kappa Phi_K) verified symbolic, shift equivariance, "no K > 1 solver"), I3 support-function sentence, Magnani-Boyd link marked the project's own, entropic risk not EVaR, kernel direction "hypothesis ... not a result", K > 1 tightening "a conjecture".

New findings, all wording-level (one sentence each):

- **N-5 (wording-level).** `method.md` line 573: "By definition, the data-level log-mean-exp is already a posynomial in the data". Strictly it is exp(tau LME), a mean of monomials, that is a posynomial; LME is its scaled log. "By definition" also overstates a short derivation. Fix: "exp(tau LME) is a posynomial in the data (a mean of monomials); the log-mean-exp is its scaled logarithm".
- **N-6 (wording-level).** `method.md` line 452: sentence begins lowercase "our reading ..." after a full stop (typo from the 94fbe72 edit).
- **N-7 (wording-level, not WP6 content).** `work-packages/README.md` WP6 row range stale (see O-10).

No substantive finding. No claim contradicts a lemma's "does NOT prove" section; no prior-art statement exceeds `literature.md`.

## Definition of good enough

| Item | Verdict | Evidence |
|---|---|---|
| D-1 to D-6 exist at stated paths | met | Deliverables. |
| R-1 to R-14 pass as checked | met | Requirements table (R-14 earlier red pushes are G-7, accepted). |
| Non-goals untouched | met | Outside the scope. |
| Every ledger condition with role and failure mode (R-4); PCA contrast with limits (R-6, R-7) | met | R-4, R-6, R-7. |

## Outside the scope

- **Out-of-scope changes:** none by WP6 commits (`git show --stat` for 17dea12, bdf1c8b, 8f49253, e82594b, 94fbe72 lists only `docs/method.md`, `docs/why-and-how.md`, `docs/limitations.md`, the spec section 6, `tests/test_narrative.py`). `docs/limitations.md` also received WP3 edits (f635a04, d0a2c0d), consistent with WP6 wording. No change to `src/`, `derivation/` or `docs/references.bib` by WP6.
- **Non-goals touched:** none. No priority or novelty claim; deflation stated as research question; WP3 tools referred to by concept (`test_no_wp3_signatures_quoted` passes).

## Observations (not counted as failures)

- O-5 to O-8: test limits, spec wording edits beyond lists, DRAFT status line, scratchpad note. Recorded disposition: accept as is.
- The L5 docstring item 2 ("diverges like (log n)/tau") is looser than the identity it proves; the narrative is stricter than the docstring. Outside WP6.

## Open decisions (for the supervisor)

Previously dispositioned: G-1, G-2, G-4, G-6 accept as is (round 1); G-3, G-5 fixed and verified; N-1, N-2, O-9 verified fixed; **G-7 accept as is** (round 2, recorded in `WP6-decisions.md`); N-3, N-4, O-11 fixed per round 2 and verified above. New, pending, all wording-level:

- **N-5.** "log-mean-exp is already a posynomial" should say exp(tau LME) is. — options: accept as is / fix before acceptance / follow-up work package
- **N-6.** Lowercase "our" typo at `method.md` 452. — options: accept as is / fix before acceptance / follow-up work package
- **N-7.** README WP6 range stale (O-10 residue). — options: accept as is / fix before acceptance / follow-up work package

## Gap dispositions

| Gap | Disposition | Reason or follow-up |
|---|---|---|
| G-1, G-2, G-4, G-6 | accept as is (recorded round 1) | A4 text marked "stated here"; missing pointers not computed by code; ledger records no failure mode for posited axioms; observations O-5 to O-8. |
| G-3, G-5 | fix before acceptance (recorded); fixed, verified | 8f49253, e82594b, 94fbe72. |
| G-7 | accept as is (recorded round 2) | Cross-package parallel-push red runs; every later run green. |
| N-3, N-4, O-10/O-11 | fix (recorded round 2); verified fixed except N-5, N-7 residues | See Substantive check. |
| N-5, N-6, N-7 | pending | |

## Recommendation

**Recommend acceptance with the listed gaps noted**, once the supervisor gives N-5, N-6 and N-7 a disposition (they are wording-level; accepting them as is, or a one-line fix each, would not change the substance). All 14 requirements and R-7a pass as checked (839 passed, lock and lint clean, spec section 6 equals the ledger for all ten lemmas and all 17 ids, attribution and authorship clean, all eight latest CI runs green, three mutation trials fail the tests). N-3 and N-4 are fixed to what the lemma docstrings and `literature.md` support, and a fresh scan of the three pages found no substantive overstatement.

Acceptance is the supervisor's act, recorded as named above. This report does not accept the work.

# WP6 — Review report (third pass)

| | |
|---|---|
| **Scope of work** | `work-packages/WP6-scope-of-work.md` |
| **Scope approval verified** | The named record is verbal approval quoted in `work-packages/WP6-decisions.md`: supervisor mzargham, 2026-11-08, "okay proceed", defaults approved as one item, open decisions none. The project has no PRs, so there is no merge to check. The scope's status line still reads DRAFT (O-7, accepted as is in round 1). |
| **Work reviewed** | WP6 commits 17dea12 (narrative, spec section 6, tests), bdf1c8b (unused import), 8f49253 (reword for round-1 G-3 and G-5), e82594b (reword for second-pass N-1, N-2, O-9; `docs/method.md` only). Also the WP6-relevant edits to `docs/limitations.md` made inside WP3 commits f635a04 and d0a2c0d. Reviewed at HEAD e82594b (plus the review-report commits 3c6d312 and 70081fb above it, which are not WP6 content). |
| **Supervisor (accepts)** | mzargham |
| **Acceptance record** | Verbal acceptance in chat, quoted in `work-packages/WP6-decisions.md`, after this report |

Reviewer: a fresh session that built none of WP6 and wrote none of the earlier reviews or fixes. This is a COMPLETE rerun from step 1 (the round-1 disposition "Fix G-3 and G-5 before acceptance" requires a full rerun after the fixes). Nothing was repaired. Mutation trials ran in `git archive` copies of HEAD in the scratchpad, not in the working tree. Recorded dispositions are in `WP6-decisions.md` (6b88cda): G-3 and G-5 fix before acceptance; G-1, G-2, G-4, G-6 accept as is.

## Deliverables

| ID | Verdict | Evidence |
|---|---|---|
| D-1 | met | `docs/method.md`, 588 lines. |
| D-2 | met | `docs/why-and-how.md`, 99 lines, unchanged since 17dea12. |
| D-3 | met | `docs/limitations.md`, 126 lines. |
| D-4 | met | Spec change since 7f82d43 is the single 17dea12 hunk in section 6 (`git show --stat 17dea12` lists the spec: 37 lines changed); no later spec change. |
| D-5 | met | `tests/test_narrative.py`, 9 tests. |
| D-6 | met | `work-packages/WP6-decisions.md` holds the approval and round-1 disposition; acceptance entry pending, as expected. |

## Requirements

| ID | Verdict | Evidence |
|---|---|---|
| R-1 | met | `method.md` headings in order: pipeline stage table; Conditions of the theory; The model; The fit; What the stage learns (eight numbered statements as spec 4); Tensions, not variance (with n-lemmas); Interpretation (elasticities, improvement factors, chart, pull-back, design variables); Novelty and white space; Prediction from configuration; Lineage; The posynomial and GGP extension; Research direction: kernel methods; Summary of lemma coverage. |
| R-2 | met | `uv run pytest tests/test_narrative.py`: 9 passed. Mutation: tag `L5` changed to `L88` fails `test_tags_resolve_and_all_lemmas_cited`. Limit (accepted, O-5): a tag swapped to another existing lemma is not caught; I read the tags and found them correct. |
| R-3 | met | Checked formulas against code: `solvers.log_mean_exp`, `support_weights`, `objective_and_grad`, `solve_lp`, `solve_slsqp` all exist; `coordinates.helmert_basis`, `alr_basis`, `to_frontier_coordinates`, `from_frontier_coordinates` exist; estimator `n_terms` guard at `estimator.py:148-151` raises for `n_terms != 1`, matching the text; `test_referenced_functions_exist` passes. Missing pointers for L4, L6, L3 balance are G-2, accepted as is. |
| R-4 | met | Table ids {R1, A4, F5, F10} equal the ledger set; R1, F5, F10 role and failure mode verbatim (`test_conditions_table_quotes_ledger_role_and_failure_mode`); A4 text marked "stated here" (G-1, accepted). Trial: ledger id F5 renamed F55 fails that test and `test_spec_matches_ledger`. |
| R-5 | met, with minor wording gaps N-3, N-4 (below) | N-1, N-2 and O-9 (tau -> 0) are fixed; see "Substantive check". No claim found that contradicts a lemma's "does NOT prove" section; two small attributions still go beyond their cited source. |
| R-6 | met | "Tensions, not variance" in `method.md` and `why-and-how.md` against spec 2: PCA spread; soft maximum of w.u over the simplex; smallest upper extent, binding constraint; w is the tension, ratios the exchange rates; w_j = 0 free at the balanced point; spread moves to the chart; principal directions are exercised trade-offs; co-moving metrics aligned. |
| R-7 | met | Same section and `limitations.md`: K = 1 one tension; several regional tensions are K > 1; deflation a research question, not claimed; HoroPCA disambiguated `[@chami2021horopca]`. |
| R-7a | met | n-lemma subsection: facet whose normal has exactly n positive exponents; support of w; exact at tau = infinity, smooth at working tau; `min_exponent` must be 0; K = 1 balanced point only; regional n-lemmas are K > 1; named dilemmas are heuristics; no case asserted to have a trilemma. `limitations.md` repeats the limits. (`why-and-how.md` wording: O-11.) |
| R-8 | met | `why-and-how.md`: tensions, V = 1, chart, five-stage workflow, inputs and outputs, in prose; links to method and limitations; case by concept; `api.md` for tools. |
| R-9 | met | `limitations.md` lists each limit named by R-9 with its reason, plus n-lemma limits, prediction, K > 1 and kernels as documented-not-built. |
| R-10 | met | `test_citation_keys_resolve` passes; mutation with key `@nosuchkey2000` fails it. Prior-art statements re-read against `docs/literature.md`: Cobb-Douglas, Shephard, Farrell, Aigner-Chu (secondary record flagged), Afriat, Richmond, Greene, COLS definition (Battese), Aigner-Lovell-Schmidt (flagged as our reading), super-efficiency, Malmquist, Foellmer, Ahmadi-Javid (not used), Rockafellar, Aitchison, Egozcue (our reading), Hoburg (I4), Boyd 2007, Magnani (project's own limit statement), Schoelkopf, Chami: consistent, except the DEA sentence (N-3). No priority claim: `grep -in priority` finds only "claim nothing about priority" / "no claim of priority". |
| R-11 | met | I parsed spec section 6 myself and compared with `AXIOMS_USED` imported from each lemma module: L1 [A1,A2], L2 [A2,A3], L3 [A2,A3,R1], L4 [A1,A3], L5 [A3,I1,I2,I3,F5], L6 [A2,A5,I5], L7 [A1,A2], L8 [A7,I6], L9 [A1,A2,A4], L10 [A2,A6,I4,F10]: all ten equal. All 17 ledger ids (A0-A7, I1-I6, R1, F5, F10) occur in the section 6 axiom paragraph. Trials: F5 renamed F55 in the ledger fails `test_spec_matches_ledger`. |
| R-12 | met | beta is the log-mean-exp throughout, LSE appears only as the contrast with L5's identity; `HyperbolicTradeSpace` / `hyperbolic_trade_space` used; method named "posynomial invariant form". |
| R-13 | met | `uv run pytest -q`: 844 passed, 8 skipped, 1 xfailed. `uv lock --check`: resolved, no change. `ruff check .`: all checks passed. `ruff format --check .`: 95 files already formatted. WP6 commits touch only the five deliverable files plus `work-packages/`, `docs/method.md` (8f49253, e82594b) and `tests/test_narrative.py` (bdf1c8b). |
| R-14 | not met for two pushes (G-7); otherwise met | `git log --format=%B \| grep -ciE 'co-authored\|generated with'`: 0. `git log --format=%an`: 121 commits, all Michael Zargham. `gh run list --limit 12`: red runs in the WP6 range are **f635a04** (run 42446279178, a WP3 commit that edited `limitations.md`) and **8f49253** (run 42446308761, the WP6 reword on top). Both fail `tests/test_narrative.py::test_no_wp3_signatures_quoted` ("limitations.md quotes select_temperature"). Cause: WP3's f635a04 added `select_temperature` to WP6's `limitations.md`, tripping WP6's test; the two were pushed in parallel by separate sessions, so WP6's run was red because it sat on top. Fixed by d0a2c0d (run 42446615320, success). Every later run is green: d0a2c0d, 4fbc6ea, 3c6d312, 70081fb, **e82594b** (run 42447753392). Older red runs (WP2/WP4, before WP6) are outside the range. |

## Substantive check

Compared each reworded sentence with its lemma's "What this proves / does NOT prove" docstring and with `docs/literature.md`, at HEAD.

| Finding | Current text | Verdict |
|---|---|---|
| N-1 "linear bijection" (statement 6) | "L8 gives the bijection between u and (Z, log-scale); the passage to (Z, log V) is an invertible affine change of coordinates that uses A2 and the fitted w (our step, not part of L8)". Matches the chart paragraph, which derives w.u = 1^T u/d + w.B^T Z from A2 and lists A2 under Needs. L8 docstring proves only the (Z, log-scale) round trip. | fixed, worded to L8 and A2 |
| N-2 "softened support function carries the log-convex hull" (statement 1) | "the full support function (all directions) determines the log-convex hull ... That a softened support function over positive directions conveys that hull when read at finitely many directions is our reading, not I3; the method reads it at one direction". Matches I3 (a closed convex set is determined by its support function, `literature.md` appendix B) and the lemma remark in L5 ("the fit reads conv A through its support function", recorded, not proved). | fixed, worded to I3 |
| O-9 "degenerates to a vertex" (the fit, tau -> 0) | "As tau -> 0 the soft maximum tends to the mean and the softmax weights tend to uniform (L5). Our reading, not proved here, is that the fit then moves toward a vertex ... by the limit of the minimization". L5 item 4 proves lim LME = mean only; convergence of the minimizer is correctly labelled a reading. Small blemish: the weights limit is cited to L5 but is the definition in L3 (O-11). `limitations.md` already says "weights approach uniform ... mean (L5)" and defers to the API page, which says the same thing labelled as the project's reading. | fixed, worded to L5 |
| Round-1 G-3 (consistency; K > 1 optimism; L10 carry-over; LSE overshoot) | Statement 5 "an expectation, not a proved result ... L5 disclaims consistency"; K > 1 "expected to tighten (a conjecture)" in `method.md` and `limitations.md`; L10 "shift equivariance ... whether novelty carries over unchanged is expected ... not proved by L10"; LSE = LME + (log N)/tau stated as an identity, "intended way" labelled "our reading, not a lemma". | worded to the lemmas |
| Round-1 G-5 (Magnani-Boyd link; DEA limit object) | Magnani-Boyd: "the project's own statement (L10 proves the limit; Magnani and Boyd do not state this link)", matching `literature.md`. DEA: see N-3. | Magnani fixed; DEA partly fixed |

### Fresh scan: 28 claims sampled

Faithful (checked against lemma or literature entry): L1 homogeneity and invariant form (Needs A1, A2); L2 shift, "silent on per-metric rescaling"; L3 gradient and balance, "does not prove interior, existence, uniqueness, sign of lambda"; L4 convexity "not strict"; L5 identity and bounds mean <= LME <= max <= LSE, LSE >= max with the n >= 2 strictness unneeded for the stated inequality; L5 tau -> infinity limit under F5; L6 cumulant tau sigma^2 ||w||^2 / 2, ridge "an interpretation"; L7 "proves them for F itself and does not say they are those of the balanced point"; L8 "does not prove such a B exists for every d"; L9 pull-back and bijection (alpha_j != 0), "does not say a conditioning is appropriate"; L10 identities, "no K > 1 solver", "proves nothing about fitted parameters"; statement 3 depth 1/tau "a reading of the L3 weights, not a separate lemma"; statement 1 monotone in tau "standard property, not a lemma"; statement 2 LP duality "inherited (I1), checked numerically, not a SymPy lemma"; statement 7 identifiability "L4 does not prove it"; kernel direction "hypothesis to examine"; HoroPCA disambiguation; Cobb-Douglas / Shephard / Farrell / Aigner-Chu / Afriat / COLS lineage; Aigner-Lovell-Schmidt "our reading"; super-efficiency and Malmquist "prior art" with "not established by any source we cite"; Magnani-Boyd; Hoburg (I4); entropic risk, not EVaR; Aitchison "kin"; Egozcue "our reading".

Sentences containing the watch words: "proved" (all 11 occurrences in the three pages are negations or attributions to a named lemma); "converge" (statement 5, labelled expectation); "carries" (L10 sentence, hedged; I3 sentence, now corrected); "removes" (none); "limit object" (lineage, see N-3); "bijection" (L8, L9, prediction paragraph: each scoped correctly).

New findings (all small, wording only):

- **N-3.** `method.md` Lineage: "Data envelopment analysis [@charnes1978measuring] computes hulls of the data; the log-convex hull of the data is the limit object of the hierarchy ... in the sense of the object that DEA-style hull methods compute (the project's reading)". `literature.md` supports only that DEA is an LP measure of relative efficiency, and says "the data's convex hull is the limit object in the spec's hierarchy" (convex, not log-convex, and as the spec's statement). "DEA computes hulls" is not in the source, and "log-convex hull ... that DEA-style methods compute" mixes metric-space hulls with log-space hulls. The parenthesis marks the reading, so this is a residue of round-1 G-5 (and of second-pass O-9's last item), not a new claim of priority.
- **N-4.** `method.md` kernel section: "The data-level log-mean-exp is already a posynomial in the data (L5's normalization identity)". L5 proves LSE = LME + (log N)/tau and bounds; it does not prove a posynomial statement (that exp(tau LME) is a mean of monomials is elementary but is not L5). Mis-attribution to a lemma, in a section otherwise labelled hypothesis.

## Definition of good enough

| Item | Verdict | Evidence |
|---|---|---|
| D-1 to D-6 exist at the stated paths | met | Deliverables table. |
| R-1 to R-14 pass as checked, with evidence in the review | met except R-14's "every push" (G-7); R-5 carries N-3, N-4 | Requirements table. |
| Non-goals untouched | met | Outside the scope. |
| Every ledger condition stated with role and failure mode (R-4), and the PCA contrast with limits (R-6, R-7) | met | R-4, R-6, R-7. |

## Outside the scope

- **Out-of-scope changes:** none by WP6 commits. `git show --stat` of 17dea12, bdf1c8b, 8f49253, e82594b lists only `docs/limitations.md`, `docs/method.md`, `docs/why-and-how.md`, the spec (section 6), `tests/test_narrative.py`, `work-packages/` files. `docs/limitations.md` was also edited inside WP3 commits f635a04 and d0a2c0d (small-tau paragraph, K > 1 hedge, removal of the `select_temperature` mention); those edits are WP6-consistent (the K > 1 hedge is the 8f49253 wording, landed in WP3's commit). No change to `src/`, `derivation/` or `docs/references.bib` by WP6.
- **Non-goals touched:** none. No priority or novelty claim; deflation stated as a research question; WP3 tools referred to by concept (`test_no_wp3_signatures_quoted` passes).

## Observations (not counted as failures)

- O-5 to O-8 (round-1 G-6): test limits, spec wording edits beyond lists, DRAFT status line, scratchpad note. Recorded disposition: accept as is.
- **O-10.** `work-packages/README.md` line 58 still lists the WP6 delivery range as `17dea12..bdf1c8b`, omitting 8f49253 and e82594b (unchanged since the second pass).
- **O-11.** Remaining wording points of the same family, none contradicting a lemma: "the softmax weights tend to uniform (L5)" and `limitations.md` "weights approach uniform ... (L5)" cite L5 for what is the definition of the weights (L3); `limitations.md` "a ridge toward balanced exponents (L6)" where `method.md` correctly calls the ridge an interpretation; `limitations.md` line 34 "The elasticities of L7 are those at that point" where `method.md` says L7 does not say this and the identification needs L3 and R1; `why-and-how.md` "it reports the metrics whose weights are positive" where at finite tau all weights are typically positive (`method.md` and `limitations.md` state the graded reading); "conservative away from the balanced point / reliable near it" stated as fact in `method.md`, `limitations.md` and `why-and-how.md`, from spec 4, with no lemma behind it.
- The L5 docstring item 2 ("diverges like (log n)/tau") is looser than the identity it proves; the narrative is stricter than the docstring. Outside WP6.

## Judgment on the CI exception (R-14)

R-14 says "CI green on every push". Two pushes in the WP6 range were red (f635a04, which is WP3's, and 8f49253, WP6's). The cause is not content in either package alone: a WP3 edit to a WP6 file tripped a WP6 test while two sessions pushed in parallel, and the next commit (d0a2c0d) fixed it; all five subsequent runs, including the latest WP6 commit e82594b, are green. The literal requirement was missed for one WP6 push; the end state is green and attribution-free. I treat it as a gap for the supervisor, not as a failed deliverable, and I do not dispose of it.

## Open decisions (for the supervisor)

Round-1 items G-1, G-2, G-4, G-6 carry their recorded disposition (accept as is). G-3 and G-5 were "fix before acceptance"; the fixes have been reviewed above. Earlier second-pass items N-1, N-2 and O-9 (tau -> 0) are verified fixed and need no decision. New items, all pending:

- **G-7.** R-14 "CI green on every push": 8f49253 (and WP3's f635a04 beneath it) were red because of a cross-package test interaction in parallel pushes; green from d0a2c0d on. — options: accept as is / fix before acceptance / follow-up work package
- **N-3.** Lineage sentence on DEA ("computes hulls", "log-convex hull ... DEA-style methods compute") goes beyond `literature.md`, which supports only the LP efficiency measure and the spec's convex-hull hierarchy. — options: accept as is / fix before acceptance / follow-up work package
- **N-4.** Kernel section attributes "log-mean-exp is already a posynomial in the data" to L5, which does not prove it. — options: accept as is / fix before acceptance / follow-up work package
- **O-10, O-11 (one item).** The stale README delivery range and the remaining wording points. — options: accept these as is, or pick any to act on

## Gap dispositions

| Gap | Disposition | Reason or follow-up |
|---|---|---|
| G-1 | accept as is (recorded 6b88cda) | A4 role and failure mode written in the narrative and marked "stated here". |
| G-2 | accept as is (recorded 6b88cda) | Missing pointers for L4, L6, L3 balance: not computed by the code. |
| G-3 | fix before acceptance (recorded); fix landed in 8f49253 and e82594b, verified above | Statement 6 (N-1), statement 1 (N-2) and the tau -> 0 sentence (O-9) now worded to L8/A2, I3 and L5. |
| G-4 | accept as is (recorded 6b88cda) | The ledger records no failure mode for those axioms. |
| G-5 | fix before acceptance (recorded); fix landed in 8f49253, verified above | Magnani-Boyd worded to the source; DEA residue is N-3. |
| G-6 | accept as is (recorded 6b88cda) | Observations O-5 to O-8. |
| G-7 | pending | |
| N-3 | pending | |
| N-4 | pending | |
| O-10, O-11 | pending | |

## Recommendation

**Do not recommend acceptance yet, in the formal sense that the new gaps have no disposition.** Substantively the work is in good shape: all 14 requirements pass as checked (844 tests, lock and lint clean, spec section 6 equals the ledger for all ten lemmas and all 17 ledger ids, attribution and authorship clean, three mutation trials fail the tests), the three second-pass wording defects N-1, N-2 and O-9 are fixed to what L8/A2, I3 and L5 support, and the latest CI run is green. What remains are two small mis-attributions (N-3 on DEA, N-4 on L5), one process exception (G-7) and minor observations. If the supervisor accepts G-7, N-3, N-4 and O-10/O-11 as is, or has N-3 and N-4 reworded as one-sentence edits, I would recommend acceptance with the listed gaps noted.

Acceptance is the supervisor's act, recorded as named above. This report does not accept the work.

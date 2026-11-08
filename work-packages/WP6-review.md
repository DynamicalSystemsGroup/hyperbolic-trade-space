# WP6 — Review report (fifth pass)

| | |
|---|---|
| **Scope of work** | `work-packages/WP6-scope-of-work.md` |
| **Scope approval verified** | Verbal approval quoted in `work-packages/WP6-decisions.md`: supervisor mzargham, 2026-11-08, "okay proceed", defaults approved as one item, open decisions none. No PRs in this project, so no merge to check. The scope status line still reads DRAFT (O-7, accepted as is in round 1). |
| **Work reviewed** | WP6 commits 17dea12 (narrative, spec section 6, tests), bdf1c8b, 8f49253, e82594b, 94fbe72, and now f6d9b9a (round-3 one-line fixes in `docs/method.md`). Reviewed at HEAD 354bffd (the later commits are WP4b). |
| **Supervisor (accepts)** | mzargham |
| **Acceptance record** | Verbal acceptance in chat, quoted in `work-packages/WP6-decisions.md`, after this report |

Reviewer: a fresh session that built none of WP6 and wrote none of the earlier reviews or fixes. COMPLETE rerun from step 1, as round 3 ("One-line fixes, then accept") requires. Nothing was repaired. Mutation trials ran in a `git archive` copy of HEAD in the scratchpad.

## Deliverables

| ID | Verdict | Evidence |
|---|---|---|
| D-1 | met | `docs/method.md`, 594 lines. |
| D-2 | met | `docs/why-and-how.md`, 99 lines. |
| D-3 | met | `docs/limitations.md`, 127 lines. |
| D-4 | met | Spec change is the single 17dea12 hunk in section 6 (`git diff 17dea12~1 HEAD -- docs/superpowers` shows one hunk, `@@ -322,22 +322,31 @@`). |
| D-5 | met | `tests/test_narrative.py`, 9 tests. |
| D-6 | met | `WP6-decisions.md` holds approval and the round-1, round-2 and round-3 dispositions; acceptance entry pending, as expected. |

## Requirements

| ID | Verdict | Evidence |
|---|---|---|
| R-1 | met | `method.md` headings cover stage table, conditions, model, fit, the eight statements, tensions-not-variance with n-lemmas, interpretation, novelty and white space, prediction, lineage, GGP extension, kernel direction. |
| R-2 | met | `pytest tests/test_narrative.py`: 9 passed. Mutation: first `<!-- lemma: L5 -->` changed to `L88` fails `test_tags_resolve_and_all_lemmas_cited` (1 failed, 8 passed). Known limit (accepted, O-5): a tag swapped to another existing lemma is not caught. |
| R-3 | met | Pointer tables point at `solvers.log_mean_exp`, `solvers.objective_and_grad`, `solvers.solve_lp`, `coordinates.helmert_basis`, `to_frontier_coordinates`, `HyperbolicTradeSpace.*`; `test_referenced_functions_exist` passes. f6d9b9a touched no pointers. |
| R-4 | met | Conditions table ids {R1, A4, F5, F10}; verbatim ledger role and failure mode tested. Mutation: ledger id "F5" renamed "F55" (2 occurrences in `derivation/axioms.py`) fails `test_conditions_table_equals_ledger_set`, `..._quotes_ledger_role_and_failure_mode` and `test_spec_matches_ledger` (3 failed). |
| R-5 | met | See "Substantive check". No substantive finding; wording-level residues listed. |
| R-6 | met | "Tensions, not variance" in `method.md` and "The idea" in `why-and-how.md` match spec section 2 point by point (PCA maximizes spread; soft maximum minimized over the simplex; w is the tension, ratios exchange rates; w_j = 0 free; spread moves to the chart; aligned versus in tension). |
| R-7 | met | K = 1 one tension; K > 1 regional; deflation a research question; HoroPCA disambiguated (`limitations.md`, `method.md`). |
| R-7a | met | n-lemma subsection (`method.md`, "n-lemmas are discovered, not assumed") and `limitations.md` "What the n-lemma reading cannot say" state: facet with exactly n positive exponents; support of w; exact at tau = infinity, graded at working tau; floor on exponents zero; K = 1 balanced point only; regional n-lemmas are K > 1; no case asserted to have a trilemma. |
| R-8 | met | `why-and-how.md`: idea, V = 1, chart, workflow, inputs and outputs, links to method and limitations, case study by concept. |
| R-9 | met | `limitations.md` lists each R-9 limit with its reason, plus n-lemma limits, prediction, K > 1 and kernels as documented-not-built. |
| R-10 | met | `test_citation_keys_resolve` passes. Mutation: `[@nosuchkey2000; @...]` inserted in `limitations.md` fails it (1 failed). Prior-art statements re-read against `docs/literature.md`: consistent; no priority claim. |
| R-11 | met | I read spec section 6 (lines 340-351) myself and compared with `AXIOMS_USED` in each lemma module: L1 [A1,A2], L2 [A2,A3], L3 [A2,A3,R1], L4 [A1,A3], L5 [A3,I1,I2,I3,F5], L6 [A2,A5,I5], L7 [A1,A2], L8 [A7,I6], L9 [A1,A2,A4], L10 [A2,A6,I4,F10]: all ten equal. `test_spec_matches_ledger` passes and covers all ledger ids. |
| R-12 | met | beta is the log-mean-exp throughout (LSE only as the contrast); `HyperbolicTradeSpace` / `hyperbolic_trade_space`; "posynomial invariant form". `test_names_and_hygiene` passes. |
| R-13 | met | `uv run pytest -q`: 841 passed, 8 skipped, 5 xfailed (xfails are WP4b's). `uv lock --check`: Resolved 173 packages, no change. `ruff check .`: all checks passed. `ruff format --check .`: 95 files already formatted. WP6 commits touch only the three docs, spec section 6, `tests/test_narrative.py`, `work-packages/` (`git show --stat` of the six commits). |
| R-14 | met on the end state; G-7 (accepted) covers the earlier red pushes | `git log --format=%B \| grep -ciE 'co-authored\|generated with'`: 0. `git log --format=%an`: 136 commits, all Michael Zargham. `gh run list --limit 8`: all eight completed/success, including f6d9b9a (run 42450210046) and HEAD 354bffd (run 42450777946). |

## Substantive check

### N-5 and N-6 (round-3 items)

- **N-5 fixed and mathematically correct.** `method.md` (research-direction section) now reads: "From the definition, $\exp(\tau\cdot\text{log-mean-exp})$ is the mean of exponentials of affine terms in the log data, which is a posynomial in the data (a sum of monomials with positive coefficients $1/N$)". Check: here u = log m (A1), so exp(tau LME_tau(w·u)) = (1/N) sum_i exp(tau w·u_i) = (1/N) sum_i prod_j m_ij^(tau w_j): a sum of N monomials in the data with exponents tau w_j and coefficient exactly 1/N, for fixed w. The "By definition" overstatement and the claim that the log itself is a posynomial are gone. Correct.
- **N-6 fixed.** `method.md` caveat 2 now reads "...tangent only at one place. Our reading (spec section 4, no lemma behind it)...". A grep for lowercase words after a full stop in the three pages found no other instance.
- **N-7 resolved.** `work-packages/README.md` WP6 row now reads `17dea12..94fbe72`; it does not yet list f6d9b9a or this review (status table, supervisor-owned; see O-12).

### Fresh scan: 33 claims sampled

Read in full `why-and-how.md` and `limitations.md`, and `method.md` statements 1-8, tensions, n-lemma, chart, pull-back, novelty and caveats, the GGP and kernel sections, against lemma docstrings ("does NOT prove") and `literature.md`. Checked faithful: (1) support-function determines the log-convex hull (I3), finitely-many-directions reading marked "our reading"; (2) entropic risk versus EVaR; (3) LP duality as I1, inherited; (4) depth 1/tau as a reading of L3 weights; (5) L6 cumulant versus ridge reading marked interpretation; (6) consistency "an expectation, not a proved result", L5 disclaims; (7) invariances, single-metric rescaling outside L2; (8) bijection step to (Z, log V) marked ours using A2; (9) L8 any B satisfying A7, existence not proved; (10) isometric log-ratio "our reading"; (11) L9 requires A4, appropriateness not claimed; (12) V-1 as relative improvement via L1; (13) SFA parallel "our reading"; (14) DEA super-efficiency and Malmquist as nearest prior art, and "whether that matters ... not established"; (15) noise band order 1/tau; (16) optimism off the balanced point "reading ... no lemma behind it"; K > 1 tightening "a conjecture"; (17) R1 failure degrades to the invariant-form reading; (18) holes versus strata; (19) conditioning defines the question; (20) small-sample identifiability, L4 convexity not strict; (21) low-tau weights/mean (L3, L5); (22) n-lemma limits; (23) prediction conditional; (24) hyperbolic disambiguation; (25) PCA contrast limits; (26) K > 1 identities proved by L10, carry-over "expected"; (27) solver not built, `NotImplementedError`; (28) kernel direction "hypothesis"; (29) support-vector analogy "a hypothesis"; (30) "Not claimed anywhere" priority; (31) lemma coverage table matches AXIOMS_USED; (32) doubling every metric doubles V (L1); (33) machine verification versus human validation division.

New findings, all wording-level, one sentence each:

- **N-8 (wording-level).** `limitations.md` line 74-75: duplicated word, "outside the documented useful range) the / the softmax weights". Introduced in 94fbe72. Fix: delete one "the".
- **N-9 (wording-level, mild).** `why-and-how.md`: "After a one-time normalization the edge of the achievable region is exactly the surface $V=1$" reads as exact for the data's edge; it is exact for the learned surface (the next sentence says "the edge learned from the data", and the limitations page states that at finite tau some designs exceed V=1). Could say "the learned edge".
- **N-10 (wording-level, mild).** `why-and-how.md` and `limitations.md` say machine verification shows "the code agrees with" the formulas; it is checked by `test_matches_derivation.py` for the tagged groups, not for every function (the pull-back pointer is "the analysis toolkit"). Previously a recorded accept-as-is theme (G-2); stated here only so the supervisor sees it.

No substantive finding. No claim contradicts a lemma's "does NOT prove" section; no prior-art statement exceeds `literature.md`.

## Definition of good enough

| Item | Verdict | Evidence |
|---|---|---|
| D-1 to D-6 exist at stated paths | met | Deliverables. |
| R-1 to R-14 pass as checked | met | Requirements table (R-14 earlier red pushes are G-7, accepted). |
| Non-goals untouched | met | Outside the scope. |
| Every ledger condition with role and failure mode (R-4); PCA contrast with limits (R-6, R-7) | met | R-4, R-6, R-7. |

## Outside the scope

- **Out-of-scope changes:** none by WP6 commits (`git show --stat` for 17dea12, bdf1c8b, 8f49253, e82594b, 94fbe72, f6d9b9a lists only `docs/method.md`, `docs/why-and-how.md`, `docs/limitations.md`, the spec section 6, `tests/test_narrative.py`). `docs/limitations.md` also received WP3 edits, consistent with WP6 wording. No change to `src/`, `derivation/` or `docs/references.bib` by WP6.
- **Non-goals touched:** none. No priority or novelty claim; deflation stated as research question; WP3 tools referred to by concept (`test_no_wp3_signatures_quoted` passes).

## Observations (not counted as failures)

- O-5 to O-8: test limits, spec wording edits beyond lists, DRAFT status line, scratchpad note. Recorded disposition: accept as is.
- O-12: the README status table still cites review 71764d3 and range to 94fbe72; it will need the new review SHA and f6d9b9a at the supervisor's convenience (status table, not a WP6 deliverable).
- The L5 docstring item 2 ("diverges like (log n)/tau") is looser than the identity it proves; the narrative is stricter. Outside WP6.

## Open decisions (for the supervisor)

Previously dispositioned: G-1, G-2, G-4, G-6 accept as is (round 1); G-3, G-5 fixed and verified; N-1, N-2, O-9 verified fixed; G-7 accept as is (round 2); N-3, N-4, O-10, O-11 fixed and verified; N-5, N-6 fixed per round 3 and verified above; N-7 resolved. New, pending, all wording-level:

- **N-8.** Duplicated "the" in `limitations.md`. — options: accept as is / fix before acceptance / follow-up work package
- **N-9.** "is exactly the surface V=1" could say "the learned edge". — options: accept as is / fix before acceptance / follow-up work package
- **N-10.** "code agrees with" is tested for tagged groups only. — options: accept as is / fix before acceptance / follow-up work package
- **O-12.** README status table citation stale. — options: accept as is / fix before acceptance / follow-up work package

## Gap dispositions

| Gap | Disposition | Reason or follow-up |
|---|---|---|
| G-1, G-2, G-4, G-6 | accept as is (recorded round 1) | A4 text marked "stated here"; missing pointers not computed by code; ledger records no failure mode for posited axioms; observations O-5 to O-8. |
| G-3, G-5 | fix before acceptance (recorded); fixed, verified | 8f49253, e82594b, 94fbe72. |
| G-7 | accept as is (recorded round 2) | Cross-package parallel-push red runs; every later run green. |
| N-3, N-4, O-10, O-11 | fix (recorded round 2); fixed, verified | 94fbe72. |
| N-5, N-6 | fix (recorded round 3); fixed, verified | f6d9b9a. |
| N-7 | resolved | README range now ends at 94fbe72. |
| N-8, N-9, N-10, O-12 | pending | Wording-level; no disposition recorded yet. |

## Recommendation

**Recommend acceptance with the listed gaps noted**, once the supervisor gives N-8, N-9, N-10 and O-12 a disposition (all wording-level; accepting them as is would not change the substance, and N-8 is a one-word deletion). All 14 requirements and R-7a pass as checked (841 passed, lock and lint clean, spec section 6 equals the ledger for all ten lemmas, attribution and authorship clean, all eight latest CI runs green, three mutation trials fail the tests). N-5 is now mathematically correct and N-6 is fixed; a fresh scan of 33 claims found no substantive overstatement.

Acceptance is the supervisor's act, recorded as named above. This report does not accept the work.

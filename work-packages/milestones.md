# Milestones: v0.1 (the paper ships with it) and v0.2 (tooling, documentation, more worked examples)

Written 2026-11-14, 18:30, at the supervisor's request before the autonomous phase resumes. The path's steps are in
`release-candidate.md`; this board tracks every item in flight against both milestones, because much of the new work
is non-blocking but informing for v0.1 and required for v0.2. States: done, in flight, scoped, not started, his.

**v0.1, the goal state:** the paper, the docsite, the container of record, the case at K = 2 on the data of record,
one vocabulary, the reader loops closed, the release items, on `dev` for the supervisor's review; one PR from `dev`
to `main` that he alone merges. **v0.2, the secondary:** a tooling and documentation upgrade with more worked
examples, drawn from the research that lands in v0.1's record; the breadth those examples should show, in his words, is
`examples-coverage.md` (an intent record, not a requirement list).

## Current state (2026-11-14 22:56 EST; dev at 79d1c72; rewritten whole, the earlier table replaced)

One head, one remaining-work list, as the external review of 22:48 asked. Evidence for every row is a driver-log
entry of the same day; the reviewer's guide (`work-packages/reviewers-guide/`) names the candidate's head when the last
landing is in.

**Landed on dev and verified by the driver (accepted by him where marked):**

| Item | State |
|---|---|
| WP33 journeys, WP35 HoroPCA, WP37 history machinery, WP38 residual pass, WP39 the case's decision, WP40 thinning | accepted by him, 2026-11-14 ("all 6 are acceptable to me") |
| Third paper unit (requests 93 to 169); fourth unit fix4 (figure captions); the abstract with its three thrusts | landed; the Pareto sentence kept on his word |
| Final reader round: 46 core and 12 held-out reads, triage, requests 172 to 194 | landed; one wrong belief (his sentence, kept), the record defects to the fifth unit |
| Root page recast (his why, no headers) with the planted ternary; the history page as an essay; the docs home with quickstart and figure | landed on his word; the history "passable for now", carving pass later |
| WP45 three test records; WP42 build (tension matrix, elasticity vocabulary, contract 25); WP43 kernel-direction spike; WP47 release engineering with WP49's covenant; WP48 and WP50 readouts | landed, driver-verified |
| Cleanup instance 4, batch 1: bundle, 97 branches, three remote branches, owner map, manifest | done on his word |

**Landing tonight (verified on their branches; combined-tree checks at each landing):**

| Item | State |
|---|---|
| Fifth paper unit (record defects of waves 8 and 9) | notebooks re-executing on the merged tree, then tests, then lands |
| WP41 bridge page and Section 7's loop, with the D-5 read's small fixes | lands after the fifth unit |
| WP46 temperature page, lemma 22 (renumbered from 21) | lands after wp41, notebooks re-executed |
| Reviewer's guide refreshed (branch guide-refresh) | lands last with the head named |
| Final head: CI on both platforms, slow and docs-paper included; a local slow run | after the last landing |
| Cleanup batch 2: landed worktrees and branches removed, manifest extended | as each lands |

**Waiting on him (morning):**

| Item | Where |
|---|---|
| The root page figure, round 2 (three terms at the median, temperature 10), then the index page as a whole | port 8861; `WP51-decisions.md`; the loop runs on screenshots and his words |
| The reviewer's guide, four sittings; the close read of the entry surfaces and Appendix G.2 | `work-packages/reviewers-guide/` |
| The abstract phrases of request 172 | `WP11-final/triage/wave-8.md` |
| The merge-to-main workflow: version 0.1.0 and the dated changelog entry, the no-ff merge, the tag; the keyboard items (PyPI accounts, trusted publishers, environments, branch protection, Pages) | `supervisor-tasks.md`, `WP47-rounds/pypi-checklist.md` |
| A release rehearsal on GitHub: the Release workflow's dry run can only be dispatched once the workflow is on the default branch, so it follows the merge; the local dry run of its checks passed | `driver-log.md`, 2026-11-14 night |

**After 0.1:**

| Item | Where |
|---|---|
| The docs example that explicates the synthetic three-metric case (his ask tonight) | `WP51-decisions.md`, scoped after the figure passes his loop |
| WP50's dependency and first package; WP48's three questions; WP41 part 2 (`propose` and `check` in the package) | the readouts and `WP41-decisions.md` |
| The post-0.1 hygiene list (WP38 residue, pinned surfaces, history rows); the examples' breadth (`examples-coverage.md`); the futures without a package (the submartingale conjecture; Lean and Rust/WASM; partial and quantile frontiers) | the records named |

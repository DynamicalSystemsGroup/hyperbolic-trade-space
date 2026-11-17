# Milestones: v0.1 (the paper ships with it) and v0.2 (tooling, documentation, more worked examples)

Written 2026-11-14, 18:30, at the supervisor's request before the autonomous phase resumes. The path's steps are in
`release-candidate.md`; this board tracks every item in flight against both milestones, because much of the new work
is non-blocking but informing for v0.1 and required for v0.2. States: done, in flight, scoped, not started, his.

**v0.1, the goal state:** the paper, the docsite, the container of record, the case at K = 2 on the data of record,
one vocabulary, the reader loops closed, the release items, on `dev` for the supervisor's review; one PR from `dev`
to `main` that he alone merges. **v0.2, the secondary:** a tooling and documentation upgrade with more worked
examples, drawn from the research that lands in v0.1's record; the breadth those examples should show, in his words, is
`examples-coverage.md` (an intent record, not a requirement list).


## The 0.2 board, held until 0.1 ships (2026-11-17, 16:05 EST)

His release line (`WP64-decisions.md`, "His release line"): 0.1 merged on his bypass; then, each its own pull
request into `dev` reviewed by a code owner other than the author, and together the 0.2 release approved under
the review rule without the bypass:

- Governance items, each a pair (his word, 2026-11-17 21:30: "the v0.2 todo list needs to include changes in github or
  the ci will fail"); the `controls` job compares the declaration with the live settings and fails CI while they
  differ, so each pair is done together, declaration first:
  - the `main-review` bypass removed: `.github/governance.toml` (`bypass_actors = []`) in its own pull request, and
    he removes the bypass actor on the ruleset page; the field is local-only on the runner, so CI does not fail in
    between and the pair is checked by a code owner's local run; named in the 0.2 changelog;
  - default workflow permissions write to read: the declaration's `[actions]` section and Settings, Actions, General;
    local-only likewise;
  - a tighter control on the governed files (the gaps readout's question: a push ruleset, CODEOWNERS path lines, or a
    review-from-teams rule): a new ruleset is compared on the runner, so the declaration's pull request merges and
    he creates the ruleset within the same sitting, or the 0.2 scope gives the checker a transition state
    (a declared change that is accepted in either state until a date); decided at scoping;
  - `controls` added to the required checks on `main`: the `main-checks` ruleset's list and the declaration together,
    same rule.
- WP76, the iron-triangle example, from branch `claude/iron-triangle-example-12a7c6` (accepted in its session at
  9657a0f0; one rebase; his review of the interpretation).
- The docs' references to the paper cleaned up: 22 `paper:` links on nine docs pages and "the paper" in prose on
  five surfaces, the paper being a working paper whose abstract alone is published (his direction relayed from the
  WP76 session, `WP64-decisions.md`).
- Documentation improvements as 0.2's scope, scoped as their own package (his scoping card from the WP76 session).
- WP79 unit B if it does not land in 0.1: the paper's contribution route.
- Deferred from 0.1 by his word: Zenodo (after a first full draft is approved); the paper's first pinned mode.
- The directions backlog built and ordered with him (`notes/directions/README.md`), not 0.2 content by itself.
- Relayed from the WP76 session (2026-11-17, 16:40): a `v0.2` integration branch exists, cut at WP76's head over `dev`
  c0e210cc; it takes each 0.2 package as accepted and merges into `dev` after 0.1 is out. His documentation
  breakdown for 0.2, recorded in `WP81-decisions.md` on `v0.2`: 1 the paper as a working paper; 2 level sets on
  every log-plane figure; 3 Home as quickstart, Getting started as the explained walk; 4 the reader's path;
  5 vocabulary and disagreeing numbers; 6 more measured-data examples; 7 hygiene. WP81 (package 1) is at its scope
  gate there. Within package 1: the abstract page at `/paper/` says the paper is a working paper whose full text
  builds from `paper/` in the repository, since every docs `paper:` link lands there in abstract mode (not changed
  for 0.1, by his direction not to disrupt the release).

## Current state (2026-11-15 13:28 EST; dev at 022c4d2; the section of 2026-11-14 22:56 kept below as history)

The candidate he reviewed on the morning of 2026-11-15 (content head a63d390, fully green) is being reworked under his
rulings of that review (`paper-requirements.md` is the register; `driver-log.md` 12:20, autonomous mode with the
driver as his proxy). The stopping condition: one coherent rendered paper at one named head, the figure sequence
carrying the argument, his remaining edits small. Paper packages run one at a time on the notebook; docs packages run
beside them.

| Package | What it delivers | State |
|---|---|---|
| wp51 (root page) | the fan figure, the cards, dataset, the docs example | landed 01ad083 |
| WP53 | his review batch of the abstract and Sections 1 to 3; two figure generators; register and tests | in verification on its branch (rebased on dev) |
| WP54 | the skeleton: Section 7 into Future work; Future work from the spike records; AI acknowledgement and Reproducibility | approved; after WP53 |
| WP55 | Section 3's fitting problem in the lineage's template; Sections 4 to 6 rebuilt; open questions to the ledger | scoped from two spikes; after WP54 |
| WP56 | Sections 7 to 9 from the current model and records; the discussion to the value proposition; Figure 7 as one triangle; the decision-maker's ternary (a spike first) | directed; its lineage spike delivered |
| WP57 | the appendices: a planning package spawning one package per appendix; the assumptions, limitations and open questions section; re-lettering last | directed |
| WP59 | conditioning and feature engineering on the three public cases; the readout | landed a9cfb60, accepted |
| WP60 | the three example pages from the readout | scoped; runs beside the paper packages |
| WP58 | the docsite, root page and README swept; the reviewer's guide at the new head; full suite and CI; his sittings 2 to 4 | last |

## State at (2026-11-14 22:56 EST; dev at 79d1c72; rewritten whole, the earlier table replaced)

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

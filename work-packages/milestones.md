# Milestones: v0.1 (the paper ships with it) and v0.2 (tooling, documentation, more worked examples)

Written 2026-11-14, 18:30, at the supervisor's request before the autonomous phase resumes. The path's steps are in
`release-candidate.md`; this board tracks every item in flight against both milestones, because much of the new work
is non-blocking but informing for v0.1 and required for v0.2. States: done, in flight, scoped, not started, his.

**v0.1, the goal state:** the paper, the docsite, the container of record, the case at K = 2 on the data of record,
one vocabulary, the reader loops closed, the release items, on `dev` for the supervisor's review; one PR from `dev`
to `main` that he alone merges. **v0.2, the secondary:** a tooling and documentation upgrade with more worked
examples, drawn from the research that lands in v0.1's record.

| Item | Role for v0.1 | Role for v0.2 | State (2026-11-14 18:30) |
|---|---|---|---|
| Third paper unit (requests 93 to 169 of the final round) | blocking: the paper's statements as the mathematicians read them; the submartingale wording | none | in flight (worktree paperfix3, four commits, running) |
| The abstract (the supervisor's text, 497 words) | blocking: lands before the held-out reads | none | in flight (landing unit) |
| Held-out reader cells, waves 8 and 9 (12 reads) | blocking: the grid's stopping rule | none | not started; after the third unit, the abstract and the stage rebuild |
| Figure loop on Figures 3, 6, 7 (in the third unit); test 1 cold reads | blocking | none | in flight |
| WP33, WP35, WP37, WP38, WP39, WP40 acceptances | blocking: his acceptance at the gate | none | his (delivered and assistant-verified; `supervisor-review-list.md`) |
| The close read of the five entry surfaces and the reading pass G.2 | blocking: his | none | his; the entry-surfaces read against the abstract is `WP11-final/abstract/entry-surfaces-consistency.md` |
| Root page summary paragraph and "bespoke or opaque" | blocking only if he changes them | none | his |
| WP8b release items (version unit on `wp8b-version`; reviewer's guide and checklist on `wp8b-drafts`; CHANGELOG; register and grid refresh; final CI both platforms; the PR) | blocking: the last step | none | version held for the assistant's word; drafts not landed; refresh waits on the last prose unit |
| WP41 part 1: the bridge's well-posedness note, audit, docs page `docs/bridge.md`, Section 7's naming paragraph | required (his ruling 12:30): framing and docs page in 0.1 | part 2: the `propose` and `check` interface, the demonstration with a Monte Carlo check, the pull-back to configuration dimensions through the surrogate | in flight (worktree wp41, near delivery) |
| WP42 spike: tension defined, lemma step, prototype matrices, figure recipe, glossary entries (loss, objective, the three layers), Section 9 sentence drafted | informing: the readout gates; the vocabulary and the three layers (Section 3 in brief, glossary in full) and the four entry-surface edits are 0.1 on his readings of today; whether the tension definition, figure and decision-section number enter the 0.1 paper is his call at the readout | the tension method on the estimator; the docs' Tensions page reworked; the `tension_report` name settled | scoped and approved (16:55); PM15 to start |
| WP43 spike: beyond the posynomial (the class statement, the five-way held-out comparison, two planted kinds, the extension-point design) | informing: at most a word in the paper's three alternatives sentences (GGP against log-convex) | required: the extension point (feature map, convex parameter set, conic solver), the Examples section on more terms against a kernel | in flight (worktree wp43; protocol then an amendment labelled post hoc, to check at delivery) |
| WP44 hunt | done: the readout and the choice | the candidates list for further unrelated domains (leaf traits, battery ageing) | done (b332787, d4cd732) |
| WP45 test records: perovskite devices, amniote life histories, Broadbalk wheat (expected n-lemma before the fit; pass or fail; sensitivities; limits) | informing (his ruling 15:25): "to help us make sure we didn't miss something or get something wrong"; lands in 0.1's record | required: the three docs example pages drawn from the records, with their fresh-reader review | in flight (worktree wp45; wheat's manual fetch pending) |
| WP46: the fit temperature as a path (plotting helper, lemma step for the small-tau limit with its check, user-guide page) | required (his ruling 16:55): in the 0.1 candidate | none | scoped and approved; PM15 to start |
| The docs' acceptance test (three personas given the docs alone and a table, asked to fit and read it) | proposed by the assistant on his priority of 14:20; placement his call | if not 0.1, the first docs package | not scoped |
| The deliverables grid and the claims register refresh | blocking: after the last prose unit | none | not started |
| Post-0.1 list (78 flagged pinned surfaces, lemma-script rows, history rows, Appendix A rows, H1/H2, the paper page's late-loading outputs, code strings in the accessibility tree) | none | tooling and docs hygiene | recorded (driver-log, WP38-review) |
| Future directions, no package: the submartingale conjecture for the search; Lean and Rust/WASM; partial and quantile frontiers as prior art | the paper names them as future work | candidates for 0.3 and after | recorded (`WP36-decisions.md`, `WP43-decisions.md`, `WP44-rounds/hunt/readout.md`) |

What needs the supervisor for v0.1, in order: the acceptances on the review list; the close read of the entry
surfaces (two root-page sentences are his); the reading pass G.2; the WP42 readout's call on the tension's place in the
0.1 paper; the word on the version unit's timing; the merge of the PR. Everything else runs in the autonomous phase
under `release-candidate.md`'s standing orders and stop conditions, with the ticks' updates.

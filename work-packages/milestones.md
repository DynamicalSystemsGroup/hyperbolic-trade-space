# Milestones: v0.1 (the paper ships with it) and v0.2 (tooling, documentation, more worked examples)

Written 2026-11-14, 18:30, at the supervisor's request before the autonomous phase resumes. The path's steps are in
`release-candidate.md`; this board tracks every item in flight against both milestones, because much of the new work
is non-blocking but informing for v0.1 and required for v0.2. States: done, in flight, scoped, not started, his.

**v0.1, the goal state:** the paper, the docsite, the container of record, the case at K = 2 on the data of record,
one vocabulary, the reader loops closed, the release items, on `dev` for the supervisor's review; one PR from `dev`
to `main` that he alone merges. **v0.2, the secondary:** a tooling and documentation upgrade with more worked
examples, drawn from the research that lands in v0.1's record; the breadth those examples should show, in his words, is
`examples-coverage.md` (an intent record, not a requirement list).

| Item | Role for v0.1 | Role for v0.2 | State (2026-11-14 21:20) |
|---|---|---|---|
| Third paper unit (requests 93 to 169) | blocking | none | delivered at ca352f5; driver-verified (head checks, browser pass); accepted under the mandate once CI 43630979464's slow jobs are green |
| The abstract (his text, 497 words) | blocking | none | landed at 735fa51; head-verified; CI 43635411288 running; browser read of the front matter next |
| Held-out reader cells, waves 8 and 9 (12 reads) | blocking: the grid's stopping rule | none | stage rebuilding at the abstract head; PM15 then recaptures and runs the reads; triage after |
| Figure loop: Figures 3, 6, 7 cold reads; the 170/171 follow-up (Figure 6 z-order, L16 docstring, Figure 7 title wrap) | blocking | none | cold reads done (ca352f5); follow-up unit with PM15, not started |
| WP41 part 1: bridge well-posedness note, audit, `docs/bridge.md`, Section 7 paragraph | required (12:30 ruling) | part 2: `propose` and `check` interface, demonstration with a Monte Carlo check, pull-back to configuration dimensions | in flight (worktree wp41), near delivery |
| WP42 build, Scope A (his choice 20:30): lemma L21, the definition beside elasticity, package functions with tests, Figure 7 decision, glossary and checker with schema, the loss pass, entry-surface edits, Section 3 paragraph, docs page on routes back | required: the vocabulary, the three layers, tension's definition, the entry-surface edits; the Section 9 sentence his to accept | the routes back for kernels; seam values as reported pairs | his four answers in (23:05); build dispatched as Amendment 1 of the scope |
| WP43 spike: beyond the posynomial | informing: at most a word in the alternatives sentences | required: the extension point (feature map, convex parameter set, conic solver); Examples on more terms against a kernel | readout committed (worktree wp43); driver verification pending (the post hoc protocol amendment against R-1) |
| WP44 hunt | done | the candidates list for further unrelated domains | done |
| WP45 test records: perovskite, amniote, Broadbalk wheat | informing: lands in 0.1's record (15:25 ruling) | required: the three docs example pages with fresh-reader review; the coverage record's gaps | in flight (worktree wp45); wheat's manual fetch is his (below) |
| WP46 temperature path (helper, small-tau lemma step, user-guide page) | required (16:55 ruling) | none | in flight (worktree wp46; D-1 and D-4 landed there) |
| WP47 release engineering (0.1.0 metadata, trusted publishing workflow, CODEOWNERS, templates, CONTRIBUTING, SECURITY, maintainers page, his PyPI checklist) | blocking: the release path | the same path for 0.2 | approved 19:50; dispatched |
| WP48 governance-checks spike | readout only | required: the checks as automated release gates, as verification cases | approved 19:50; first pass committed; readout in progress |
| WP49 contributor covenant spike | readout before the PR; the covenant on his sign-off, placement his call at the readout | the same | approved 19:50; dispatched; his principle and tool stance recorded 20:50 and 21:10 |
| WP50 topological holes by persistent homology (research) | at most a future-work sentence, his to accept | none | approved 21:35; dispatched |
| WP8b: version unit, reviewer's guide and checklist, CHANGELOG, register and grid refresh, final CI both platforms, the PR | blocking: the last step | none | version held (rebases with WP47's metadata); drafts not landed; refresh after the last prose unit |
| Acceptances WP33, 35, 37, 38, 39, 40; the third unit; the abstract | blocking: his | none | his (`supervisor-tasks.md`) |
| Close read of the entry surfaces; reading pass G.2 | blocking: his | none | his |
| The docs' acceptance test (three personas, docs alone) | placement his call | if not 0.1, the first docs package | not scoped |
| Examples' breadth (`examples-coverage.md`) | an intent record | guides the choice of example pages | recorded 20:00 |
| Post-0.1 hygiene list (pinned surfaces, lemma-script rows, history rows, Appendix A rows, late-loading outputs, code strings in the accessibility tree) | none | tooling and docs hygiene | recorded |
| Future directions without a package: the submartingale conjecture; Lean and Rust/WASM; partial and quantile frontiers | named as future work | candidates for 0.3 and after | recorded |

What needs the supervisor is kept apart in `supervisor-tasks.md`: the things only he can do, and the things done together
at a keyboard. Everything else runs in the autonomous phase under `release-candidate.md`'s standing orders.

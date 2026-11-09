# PM handover note, 2026-11-09 (outgoing PM)

State of dev at 48df440. No agent of the outgoing PM is running; all worktrees it created are removed
(the worktrees listed under pm-worktrees/ belong to the incoming PM).

## What each stream did and where it stands

| Stream | Pushed | Result | Open |
|---|---|---|---|
| P1 paper text | 508b37f and earlier | Section 4 narrated, section 6 skim path, L16 and L17 blocks, WP17 wording in section 6, three-pane figure removed from the body, length ledger (paper/length_ledger.toml) with a row per addition, equation (2) broken to fit | Reader tests (P1r) on sections 4 and 6 not run; R-39 follow-ups from P3 and P5 not routed; Appendix F container paragraph needs the facts below |
| P2 vocabulary tool | 9a3156e | scripts/check_vocabulary.py, tests, baseline of 97 known violations (89 stem, 7 first use, 1 avoid: "exchange rate" in docs/index.md) in scripts/vocabulary_baseline.toml | Triage of the 97 into dispositions (P3); no `reserved` field in the schema |
| P3 vocabulary reading | not started | | One reader per paper section and docs page; three lists verbatim into work-packages/WP10-vocabulary-review.md |
| P4 claims register | 4cb61c0 | claims_register.toml, 23 rows (17 M, 6 S), tests | P5 rows to land through it |
| P5 claim extraction | not started | | One extractor and one backing-lookup agent per section |
| P6 docs text | d1053c3 (WP17 wording) | Fitting page, glossary entries term temperature and assignment | Examples page: drop example (ii) (cubesat triangle) and its test; add the values table from the helper below; the on-page shows / does not show / good for lines after the P8 table; `groups=` of plot_ternary goes with example (ii) |
| P7 ternary values helper | 0a18b5b | `ternary_marker_values(estimator, X, names=None)` returns a DataFrame (marker shape, number, shares per metric, V as a fraction of the highest marker); `df.attrs["levels"]` holds the line levels; contract version 8 | Used by P6 in the Examples key |
| P8 figure review | f8192ae, 76e2f31, fb8fbe1 | work-packages/WP8a-figure-review.md and candidates under docs/superpowers/notes/figure-candidates/ (fig7-a-depth.png recommended) | WITHDRAWN by the supervisor's reframe: reassess every docsite figure by intent with two cold readers on the image alone (Figure 6 heatmap: resize only; Figure 8 triangle: leave; Figure 9: dropped); deliver one table; nothing on a page changes until his answer |
| P9 release items | ce80b39 | LICENSE (MIT, Dynamical Systems Group), CHANGELOG.md (Unreleased, target 0.1.0), release punch list updated | The WP7 notebook archive is NOT done: the notebook is pinned by tests/test_notebook.py and the interface contract (needs an amendment or the driver's call); `__version__` still 0.0.1 (driver) |
| P10 container | bf80af4, e1f3267, 3c46237, 48df440 | Dockerfile builds linux/arm64; hts-paper and hts-alt (Ubuntu 24.04; Debian bookworm has no arm64 z3 wheel) built and run offline; record in paper/container/RECORD.md and README.md | See below |
| P11 verification tiers | 04a3471, 78f5e1c | slow markers (383 slow tests), scripts/check.py (`--changed`, `--fast`, `--list`), CI in three shards, fast suite 80 to 100 s with `-n auto --dist loadgroup` | The full suite rewrites the tracked examples/adcs/experiments/reports/v1-v2-comparison.md: revert it after runs or make the regeneration write elsewhere |

## Findings the incoming PM must route

1. Linux red (run 42684175900): tests/test_soft_fit.py::test_r2_default_planted_fits_equal_the_recording asserts bit-equality against Mac recordings for the tau = infinity cases. Fix: exact only under HTS_ENVIRONMENT_OF_RECORD=1 or on the recording platform; elsewhere stated tolerances, with labels allowed to differ on rows whose best two scores tie within EPS_FEAS; record the recording platform in the reference file. A branch wp17fix exists (worktree under pm-worktrees/).
2. P10, container of record (head 48df440): inside hts-paper (arm64, HTS_ENVIRONMENT_OF_RECORD=1, no network) 46 tests fail, 2011 pass: 45 in tests/test_soft_fit.py and 1 in tests/test_cubesat_oracle.py (settling time differs by up to 0.05 s). They are exact comparisons against recordings made on the Mac; the reference npz was regenerated in the image (max relative change 3.5e-15) and committed, but tests/data/soft_fit_default_reference.npz (the WP17 recording) is not P10's. The planted table digest in the container is b17d4f8f, against the committed c127dd4c (the committed notebooks therefore fail test_c_committed_output_is_current in the container until the outputs regenerated there, kept at scratchpad out-record, are committed). In hts-alt (not the environment of record) 4 fail: tests/test_soft_fit.py K = 3, tau = infinity, seeds 0 to 3: the same facets numbered differently (gap G-10), and seed 2's term_objective_change differs by 0.3 percent. No tolerance was changed.
3. P10 changed tests/test_container.py in three places (digest check reads the BASE_IMAGE default, platform expectation arm64, the record needle "103 passed"): confirm.
4. Facts for Appendix F (P1): image id changes with every commit because the history layer carries the commit; git history enters through a git bundle passed by paper/container/build.sh as a named build context; Node 24.22.2 for arm64 is verified by sha256 and signature; UV_NO_SYNC=1 keeps uv run from re-resolving offline.
5. The hard limits on Docker and Colima stand (images and containers named hts-* only; no change to Colima).

## Standing rules in force

Stage by path; no AI attribution; short checks before a push (lint and format on changed files, the tests of the changed files, Appendix B test with regeneration for any derivation change); the full suite is the driver's watcher; the Linux run is dispatched per batch by the driver; the figure review note governs figures; the paper's figures stay frozen until WP19's gates; the supervisor's tickets are recorded in work-packages/WP10-decisions.md and WP8a-decisions.md.

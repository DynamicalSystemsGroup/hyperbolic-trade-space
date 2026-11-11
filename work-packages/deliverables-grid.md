# Deliverables grid, 0.1 candidate

The grid the supervisor asked for on 2026-11-11 (11:40), as specified in `release-candidate.md` ("The deliverables
grid") and laid out by `status-report-template.md`. First fill, at dev `ef85f35`. Sparse: a cell is filled only where
the row serves the column; a blank cell is not applicable. State: `-` not started, `~` in progress, `d` delivered to
the assistant, `A` accepted. Evidence: the last reader round or user test and its verdict, or the check that ran, with
its commit or hash.

Personas by column: Explore P1, P8; Use P2, U1 to U4; Theory P5, P6, P9, P10; Model P3, P7; Evaluate P2, P8 and the
reviewer. P4 (the machine-learning practitioner) has no column in this mapping; the supervisor to say whether one
should be given.

| Deliverable | Explore | Use | Theory | Model | Evaluate |
|---|---|---|---|---|---|
| Root page | `d` ef85f35: two-panel and root-page screenshots at 1100 and 375 px, light and dark, read by the assistant; planted-figure fix fc9aa58; no reader round on the root page yet | | | | |
| README and repository layout | `-` WP33 signposting (D-2) not started; scope 5c70a4b approved | `-` U1 to U4 cells not run (WP32, scope 78608bc) | | | `~` X-3 cut 712a59f, diff read and budget lowered; the what-runs-where line waits on the Windows package |
| Docs user guide | | `~` R2 and R3 done, nothing broke, at af9ffea (`WP28-retest.md`, returns 334fb32); R1 install passed in round 2 (c6d0fff); WP31 task readers 3 of 3 on Choosing K (head 6745b88), accepted 1d26560; U1 to U4 not run | | | `~` docs and site tests green on Linux at 1814496; watcher 2285 at 4b7ca4a; WP33 wayfinding round not run |
| API reference and examples | | `~` Examples page: R2 and R3 done at af9ffea; two-panel figure fc9aa58 links its full-size PNG; the import surface (WP33 OD3) not yet read | | | `~` CI 1814496 green on Linux; watcher 4b7ca4a 2285 passed |
| Package (install, API, tests) | | `~` install and first fit passed, round 2 R1 (c6d0fff); U1 to U4 not run | | | `~` Linux three shards green at 1814496; watcher 4b7ca4a 2285 passed, 17 skipped, 2 xfailed; Windows not started (package opened 11:30, no spike recorded) |
| Paper body | `d` abstract, depth A: rounds 1b to 1d, W1 to W4 gone after CR-1 (60b1576); with the supervisor for his own review | | `~` WP11 round 3 at af9ffea (returns 334fb32, record 052e8ee): R-13 conditions 2 and 3 not met (S8's second item missing at depth B in five cells; no new why at depth C on the letter), `WP28-retest.md`; P9 and P10 re-read of the placed corollary pending (WP29, 1814496) | `~` P7 baseline (triage 0171ae7): classes 1 and 3 in progress; the cost answer sits in the model revision, which waits on the supervisor's values (gate checklist 450c65b) | |
| Paper appendices | | | `~` Appendix B: lemma chain and proof map green at a9e23b2 (all lemmas pass, 17 files, 371 steps); P9 and P10 dispositions approved 11:20 (`WP29-decisions.md`), re-read pending | `~` Appendices C and D.17 read by the P7 and P8 baselines (0171ae7, 45180fd); the cost-axis and list units wait on WP30 values | `~` Appendix F: container record accepted on regen (03189c5, d66c106, 25dba3c; 0 failed on both images); a cold reproduction from Appendix F alone not yet recorded |
| Derivations and proof map | | | `~` WP24 accepted (c3c1ce3); noise corollary derived and placed (WP29, 1814496), P9 and P10 re-read pending | | `d` lemma chain and proof map pass with the corollary: CI 1814496 green; watcher 4b7ca4a all checks green |
| Case model, views, stakeholders, data | | | | `~` P3 read of revision 7 (b0a9a92, 11 findings; revision 8 final); WP23 accepted (db59365, acceptance a5acf86); WP26 and WP27 accepted at 05f8a2a; WP30 data gate waits on the supervisor's values | `~` WP26 and WP27 acceptance reviews 2d2a81b and 3e22533, gaps closed at 05f8a2a; P8 baseline (0171ae7) F3, no candidate meets the requirements, is a supervisor question |
| Release items (container, CI x3, changelog, version, guide) | | `~` CHANGELOG.md carries its 0.1.0 line (b2c5dd9); LICENSE in place; version still 0.0.1 in `pyproject.toml` at ef85f35 (the version step is the driver's, D2) | | | `~` CI on two of three platforms: Linux 1814496 green, Mac watcher 4b7ca4a green; Windows not started; container accepted on regen (25dba3c); reviewer's guide not started |

**Reading the first fill.** No paper or package cell is `A` for the reader columns: the paper's stopping rule is not
met, and the candidate definition's reader pass is still owed. Accepted under the driver so far: WP10 structurally
(2026-11-09), WP23, WP24, WP25-4, WP26, WP27, WP28 (b1a806c), WP31 (1d26560). Nothing in the Use column has run the
user cells U1 to U4 or the wayfinding round WP33; those are the open reader evidence for the Use and Explore columns.

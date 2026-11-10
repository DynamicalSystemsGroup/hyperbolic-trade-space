# The parallel board: tight scopes the PM dispatches at the same time

Written 2026-11-09 by the driver on the supervisor's direction: "it seems like you are missing the
opportunity to use tight scopes of work to parallelize efforts using the PM as an orchestrator." And:
"i don't like the fact that you are not committing. we have dev so you can commit work".

## What the board is

The supervisor (2026-11-09): "to be clear the PM is managing agents scoped to the work packages." The
board is a view of the approved work packages, not a structure beside them. Every stream is a piece
of one package's approved scope (an amendment, a requirement, a ticket recorded in that package's
decisions file), and the agent that runs it is scoped to that package: its brief cites the package's
scope document and the requirement it serves, and its blast radius is inside that package's files.
A stream with no package behind it is not started until the package is scoped and approved.

| Stream | Package and the requirement it serves |
|---|---|
| P1, P1r | WP10 Amendment 4 R-38 and Amendment 5 R-39; the tickets of 2026-11-09 in `WP10-decisions.md` (section 4 narration, section 6 skim path); WP17 R-9 for the soft-fit wording |
| P2, P3 | WP10 Amendment 4 R-35 and R-36 (the vocabulary review) |
| P4, P5 | WP10 Amendment 5 R-43 (the claims review) |
| P6 | done: 3dbac94, 0fb09ab, 183397d, 8752903 (WP21 docs) |
| P7 | pushed 0a18b5b; tier 2 green |
| P8 | done: ce87711 table; applied abd6c11 (browser-checked at desktop width only) |
| P9, D2 | WP8b, release preparation: NOT YET SCOPED. Its items were started ahead of a scope; the PM drafts `WP8b-scope-of-work.md` now and the driver approves before anything further is done under it |
| P10 | accepted on regen: 03189c5, d66c106, 25dba3c (container record, 0 failed both images) |
| P11 | = WP20: 04a3471, 78f5e1c, fix-forward 5775220; R-3 closed; accepted pending tier 2 |
| D1 | WP11 (the reader grid), scoped and approved |
| B1 | WP19 (backlog); B2 | WP16 (held); B3 | WP22, the system model's two views (to be scoped by the PM; replaces the planned WP15 amendment) |

## Rules of the board

- **One stream, one tight scope, one set of files.** A stream owns the files listed for it and
  touches no others. Two streams never write the same file. A stream that needs a change in a file
  it does not own asks the PM, who routes it to the owner.
- **Each writing stream works in its own git worktree** (under the session scratchpad), on a local
  branch, so streams do not see each other's half-done files.
- **Commit and push to `dev` as soon as a unit of work is done**: rebase on `origin/dev`, run the
  stream's own short checks, `git push origin HEAD:dev`; if the push is refused, rebase and retry.
  Work does not sit uncommitted or unpushed. `dev` is the working branch: the full suite and the
  browser passes run on it afterwards, and a red head is fixed forward within the hour. Only `main`
  waits for verification.
- **Short checks before a push** (seconds to a few minutes, not the full suite): lint and format on
  the files changed; the tests of the files changed; and, for a change under `derivation/`, the
  Appendix B test with the appendix regenerated in the same push.
- **Readers fan out.** Any pass that only reads (cold reads, vocabulary lists, claim extraction,
  figure reads) runs as many agents at once as there are sections or pages.
- The PM keeps the status column current and reports each push's hash to the driver. The driver
  verifies on `dev` (full suite on both platforms, browser) and accepts or returns.

## Streams

| Id | Tight scope | Owns | Short check | Depends on | Status |
|---|---|---|---|---|---|
| P1 | Paper text, serial: narration before and between the definitions of section 4; the skim path through section 6; the soft-weight fit's wording in section 6; then routed fixes from P3, P5 | `paper/paper.ipynb` prose cells, `paper/length_ledger.toml`, the notebook re-execution | paper tests; length ledger | none | done: 508b37f..68f3a37, 792daa8, 36718d3, CR-1..3 60b1576/5518240, WP21 sentences 3d7d149; tier 2 pending |
| P1r | Reader tests of P1's sections (three personas for section 4; skim and close for section 6), fan-out, read only | `work-packages/WP10-reader-tests.md` | none | P1's first pass pushed | superseded by WP11 round 1 (driver); re-test after CR-1..3 is the driver's |
| P2 | The vocabulary tool as specified in `docs/superpowers/notes/vocabulary-review.md` | `scripts/check_vocabulary.py`, `tests/test_vocabulary.py`, the `assumed` and `stems` lists and `aliases`/`avoid` fields of `glossary.yaml` | its own tests | none | pushed 9a3156e; tier 2 green |
| P3 | The vocabulary reading: one fresh reader per section of the paper and per docs page, the three lists verbatim; triage to dispositions | `work-packages/WP10-vocabulary-review.md` | none (read only) | none | pushed b7df6be, 62a677e; re-triage into glossary calls pending |
| P4 | The claims register and its test as specified in `docs/superpowers/notes/claims-review.md` | `claims_register.toml`, `tests/test_claims_register.py` | its own tests | none | pushed 4cb61c0; tier 2 green |
| P5 | The claims pass: one extractor per section and page (read only), one backing-lookup agent per section; rows into the register through P4's owner; dispositions | `work-packages/WP10-claims-review.md` | none (read only) | none to start; P4 to land rows | pushed c3dfb6b; 328 rows landed 7bba8ed; 10 dropped for fragment mismatch (listed) |
| P6 | Docs text, serial: the soft-weight fit's wording (fitting, termination, API pages); the Examples page (cubesat triangle dropped, the table of values at the markers); later the on-page "shows / does not show / good for" lines | `docs/*.md`, `docs/user-guide/*.md` | docs and site tests | P7 for the values table | done: 3dbac94, 0fb09ab, 183397d, 8752903 (WP21 docs) |
| P7 | The ternary function's values helper, its doctest and tests; the contract amendment | `src/hyperbolic_trade_space/plotting.py`, `tests/test_plotting*.py`, `work-packages/interface-contract.*` | plotting and contract tests | none | pushed 0a18b5b; tier 2 green |
| P8 | The docsite figure review, the position-coordinates figure first; candidates as images, nothing on a page | `docs/superpowers/notes/figure-candidates/`, `work-packages/WP8a-figure-review.md` | none | none | done: ce87711 table; applied abd6c11 (browser-checked at desktop width only) |
| P9 | Release preparation, the independent items: `LICENSE` (MIT, Dynamical Systems Group), `CHANGELOG.md` for 0.1.0, the archive cleared, the release punch list brought up to date | `LICENSE`, `CHANGELOG.md`, `work-packages/release-punch-list.md`, the archive folders | the tests that read them | none | pushed; covered by WP8b (approved); version step is the driver's |
| P10 | The container of record (the supervisor, 2026-11-09: "go ahead. you can use colima. to be clear i made that available to you for reproducibility reasons"): the Dockerfile builds natively for linux/arm64 with Node pinned for that architecture; inside the container, offline at run time, the locked environment, the lemma chain, the full suite, the notebooks and the paper build; the run recorded (image digest, tool versions, results) and the environment values regenerated there; the exact comparisons pass inside it. Robustness (his word: it must not break "if you swap a different but generally comparable image"): the base image is a build argument, and a second image from a different comparable base, same lock, passes the whole suite within the stated tolerances with the same conclusions, every differing value listed in the record. Limits: images and containers named `hts-*` only; nothing under `~/.colima`; no stop, start, restart or reconfiguration of Colima; his other containers and images untouched; stop and report if memory or disk is short | `Dockerfile`, `.dockerignore`, `paper/container/`, `paper/environment_values.toml`, `tests/test_container.py` | the container tests | none | accepted on regen: 03189c5, d66c106, 25dba3c (container record, 0 failed both images) |
| P11 | Verification in tiers (`docs/superpowers/notes/verification-strategy.md`): `slow` markers on every test over about five seconds; `scripts/check.py` with the path-to-tests map and `--changed`; the tests that build the site or write shared files in one xdist group; the CI workflow in shards; the fast suite under three minutes | `scripts/check.py`, `tests/conftest.py`, marker lines in `tests/*.py`, `.github/workflows/test.yml` (the driver adds `pytest-xdist` to `pyproject.toml` and the lock) | the fast suite itself; the full suite once | the driver's dependency change | = WP20: 04a3471, 78f5e1c, fix-forward 5775220; R-3 closed; accepted pending tier 2 |
| D1 | Reader grid, round one, on the docsite and the root page (the driver runs it: the answer key stays with him) | `work-packages/WP11-round-1.md` | none (read only) | none | the driver, next |
| D2 | Version 0.1.0 and the reviewer's guide in sittings | `pyproject.toml`, `uv.lock`, the guide | lock check | P9 | the driver |
| B1 | WP19, the paper's figures: slots, figures, narration | `work-packages/WP19-slots.md`, `WP19-figure-review.md`, `paper/figures/*.py`, `scripts/build_figures.py`; placement through P1 | build_figures, paper figure tests | WP22 views | executing (see the packages table) |
| B2 | WP16, the data swap | (Amendment 2 drafted f7d180d) | | the driver's approval of Amendment 2; WP22d done | awaiting approval |

Shared files with a single owner: `glossary.yaml` (P2; other streams send entries to the PM),
`work-packages/interface-contract.*` (P7 until its amendment lands), `paper/paper.ipynb` (P1),
the docs pages (P6), `pyproject.toml` and `uv.lock` (the driver).

## Packages running or scoped (PM, latest; third PM, 2026-11-09, late night; the supervisor is back)

| Package | State |
|---|---|
| WP17 Linux soft-fit | closed: Linux 62085bb green in all three shards |
| WP10 (paper stream, P1) | abstract 85733c1, CR-1c + WP19 placements 8abb16a (218 words by ledger); CR-3/6/7/8, Corollary, Section 9 4f63628; R-36 9d5d3fd; running: unit 7 (energy differential glossed; PCA distinct, complementary, composable; WP10-decisions.md), unit 8 (WP19 P-4..P-10 except Figure 3) |
| WP10 R-36 vocabulary | re-triage 6b5d582, 8c9d0a2; derivation cce0ac5; docs 7be42ee; support bde5362; running: support unit 5 (glossary wording and six entries, reach in L14/L15), unit 6 (C152 with app-D-5; Corollary by name) |
| WP21 | rulings 2-4 landed (18dd8b6, 8a7e583, 3ff2e67, 73a8435); nothing open |
| WP22 | gate report 10cde31/264f1b8; decision swap 9c444e3; WP22d ff717ed, 6ed13ed, header d3018ba (model hash 0a0b4a4b64d1..., ledger @4, 0 drifts); WP22b/c folded into WP23 |
| WP19 | good enough reached 20496d7..da6662f (3 placed, Figures 4 and 7 dropped, captions); re-opened by the supervisor (WP19-decisions.md): Figure 3 redraw without facet colouring, Figure 4 sentence test, principle check over all figures (report first); all figures regenerate after WP23 |
| WP16 | Amendment 2 approved 7eaf468; unit 0 3d152c3; A/B reverted on the R-4 stop (K = 3 contending sets move with event-detected settling time; trial recorded in swap-evidence.md); now: settling time only, default-off switch; the regeneration and data gate move to WP23 |
| WP23 (model-realism loop) | scope drafted 7ffb719, awaits the driver's triage and the supervisor's OD1..OD8 |
| WP8b | approved; version step and reviewer's guide are the driver's |

File ownership rules added this PM: the stream that changes a registered sentence owns that row's `fragment` in
`claims_register.toml` and nothing else in it; `paper/supporting_material.ipynb`, its generators and `derivation/` have one
writer at a time (the support stream); Appendix B is regenerated in a stream-named `hts-<stream>` image, removed after.

## Packages running or scoped (fourth PM, 2026-11-10, early; the supervisor signed off for the night: "Proceed, I review after")

| Package | State |
|---|---|
| WP23 (model-realism loop) | scope folded 0769209; r2 model af37cb1; coverage eae754c, DSM 2620188, platform rule dd44575 (table produced in hts-paper; exact equality only under HTS_ENVIRONMENT_OF_RECORD); views rev 3 3fcc855, rev 4 abdb88f; round 1 pair 59c3407/29ce58e (zero exponents: power margin, eclipse reserve, peak slew power); round 2 battery (b) 5e436c6/e20db3f; round 3 interrogation a93ce10 (no model change; n-lemma readings written); round-3 cold reads next; then the gate unit. Case code (slew time out, settling time by events) is LOCAL on worktree `wp23case`, branch `wp23case`, head e7ee99b (5 commits): lands with the regeneration push. Contract amendment row 12 drafted in that branch |
| WP19 remaining redraws | done: 13d1026, 9eb46f7, f46a4ee (figures); 41c1872, 93d6ecc, cc409f8 (paper placements P-5/P-6/P-7, captions); docs re-read 0760265, 9e08ae3 |
| Package default (plot_log_plane, plot_ternary, plot_frontier_surface_3d one colour; color="facet" the option) | done: 3d6d48a, 0059264 (contract row 11) |
| Paper P-11 (MDAO prior art) | done 73c5bff; references verified (scratchpad/mdao-references.md, 11 DOIs) |
| Estimator iteration-cap warning | done 18d0064; register mend 7dff092, 656c3fe (C310) |
| Support: stderr test, D.14 regenerated in hts-paper 57a0f23716f4, Appendix B position paragraph | done 6d27662, 8849164; limitations link fixed 656c3fe |
| WP24 (the word facet) | scope 5a8bb5b approved; preparation 0be3449 (rename script, dry-run counts); lands after WP23's gate; worktree `wp24` holds the glossary patch |
| WP25 (tidiness, first instance) | done: db150fc inventory (346 rows), 09117d8 (169 files deleted), f9573fd review (drift list for WP24's docs push; 9 gaps) |

Worktrees alive: `wp23case` (unpushed case code), `wp24` (held glossary patch). All others removed.

## Packages running or scoped (fifth PM, 2026-11-10, morning; the swap final at 827f02a)

| Unit | State |
|---|---|
| 1. The paper onto the data of record (paper stream) | done ea46637, 628df90 (the case reads `data/v2/` directly; the frozen copies untouched; hts-paper f7b7585c7c58, 3c7cfc8a2e27 removed; the per-term K = 3 report by the case module's guard of ten; 48 cells, listed in swap-evidence part 5); reviewed 3f87eb5 (part 6: 13 findings, one blocking: `num-margin` moves under restart shift; plus 14, the soft-fit recording, from Linux) |
| 1c. Paper fix-forward (findings 1, 2, 4, 5, 6, 8, 9, 10, 12 of part 6; the MoE/MoP sentence in Section 8 with its ledger row; register rows for the new claims; one container run) | dispatched |
| 1s. The soft-fit recording on the data of record | done 126e1ea (58 passed on the Mac and in the image) |
| 1d. Contract row 13 (`case.data_dir` = data/v2; `frozen_data_dir` pins the frozen generation) | done a45b10f |
| 2. WP23 view-consistency (B, C, D, F; diagnostic_pair.py's title and shared vmax) | done 0fab294 (views revision 6; the paper's two byte copies; record in WP23-review.md) |
| 1b. docs/examples.md onto the new numbers | done 5dac142 (the figures regenerate from the page's blocks; nothing committed under docs/generated) |
| 1r. Reviewer of unit 1 | done 3f87eb5 (67 screenshots in scratchpad/paperreview-renders/) |
| 3. WP24 push 1 onward (worktree `wp24` holds the glossary patch); diagnostic_pair.py identifiers in a WP23 unit after push 1; glossary MoE/MoP/launch cost with the case section; WP25's drift rows in the docs push | after unit 1 |
| 4. WP23 acceptance review | done f5a63c2 (27 met, 12 not met in part or as stated, 1 not checkable; gaps G-1 to G-10 for the driver; recommends acceptance with the gaps noted) |
| 5. The WP7 notebook, tests/test_notebook.py and figures 01-09 deleted | done 4bd6bac; left dev red on the contract's R-4 pins until amendment 14 (WP24 push 1) retired them |
| WP23 gap units (the driver's acceptance conditions) | G-3 reads 8d49ab9 (three blocks on the behavioural view: type size, legend, totalMass label: revision 7 unit dispatched); G-5, G-7, G-17 acb20ce (Appendix E regenerated in 9c8a0c616386) |
| Glossary entries MoE, MoP, launch cost | done da2984e |
| WP23 `diagnostic_pair.py` identifiers (dev red on its test since 204e7c3) | dispatched |
| WP24 push 1 (src, contract row 14, tests, case code, generators; container run) | done 204e7c3, 5b01248 (image 9c8a0c616386); open: test_narrative's RENAMED map vs method.md identifiers (driver) |
| WP24 push 2 (derivation, proof map, Appendix B in the container) | dispatched |
| WP24 pushes 3 and 4, then the R-16 cold reads and WP24-review.md; WP25 instance 2 at WP23's final acceptance | next |
| 6. WP25 next instance | at the next gate |

Worktrees alive: `wp24` (held glossary patch) plus the running units' own. Docker: hts-paper 9c8a0c616386 (the environment of record until push 2 rebuilds it), hts-alt.

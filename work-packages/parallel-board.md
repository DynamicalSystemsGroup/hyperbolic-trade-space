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
| B1 | WP19, the paper's figures: slots, figures, narration | (scoped when it starts) | | the supervisor's two gates | backlog |
| B2 | WP16, the data swap | (scoped, held) | | the supervisor's choice on the step-read times | held |

Shared files with a single owner: `glossary.yaml` (P2; other streams send entries to the PM),
`work-packages/interface-contract.*` (P7 until its amendment lands), `paper/paper.ipynb` (P1),
the docs pages (P6), `pyproject.toml` and `uv.lock` (the driver).

## Packages running or scoped (PM, latest)

| Package | State |
|---|---|
| WP17 Linux soft-fit | informative message 14f7100, fix 6a8abd5 (shares allowance for tied rows); Linux run on 6a8abd5 or later to be dispatched |
| WP21 (assessment response) | approved; code D-1/D-2/D-3/D-5/D-8 pushed (5b55870..3a552c6); paper sentences 3d7d149; docs 8752903; open: Theorem 11 / support gloss, abstract tests pin R-38 wording (see report) |
| WP22 (system model views) | approved; rounds 1-3 pushed (bc71cfe, c5502ff, 9fc3952); stop recommended, round 4 optional (SlewBand link); the swap is a gate, not done |
| WP19 (figures) | scope drafted (7735343), awaits approval |
| WP8b | approved; version step and reviewer's guide are the driver's |
| Housekeeping | d7d9919, 811d260 (vocabulary baseline, register row C386) |


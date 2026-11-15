# What was verified, and how

Two kinds of checking, kept apart. A machine check says a statement holds on the committed inputs. A human validation
says a person reading the thing found it right, clear or useful. Neither stands in for the other
(`docs/superpowers/notes/presentation-framing.md`). Mathematics is checked by plain-SymPy scripts, which are a
pencil-and-paper substitute and not formal verification.

## Machine verification

| Check | What it covers | Where the result is recorded |
|---|---|---|
| Suite, lint, format, lock | the package, the derivations, the site builds | `work-packages/driver-log.md`: each landing on `dev` records its checks (the WP42 build's merged tree: 1,992 passed; the WP47 branch: 2,031 passed with one failure, the docs figure numbering, fixed on `dev` at d53e080 and confirmed gone after the rebase; the fan figure's branch: 2,035 passed). The run at `HEAD-TO-BE-NAMED` is yours to repeat (sitting 3) |
| CI on three platforms | Linux fast, slow and docs-paper; Windows fast and slow (the paper's build stays Linux and macOS); macOS by the maintainer's watcher | `work-packages/WP34-decisions.md`; run links in `work-packages/driver-log.md`. At the last record, fast jobs green on both platforms at d53e080 and 1cd23db, slow and docs-paper still running; the run at the head is named by the driver |
| Lemma chain and proof map | the derivation scripts and their tagged steps; Lemma 21 (tension) landed with the WP42 build, Lemma 22 (small temperature) lands with WP46 | `derivation/PROOF_MAP_FINDINGS.md`; `derivation/proof_map_record.json`; run `uv run python -m derivation.proofmap` |
| Claims register | each stated claim has a backing; ids were renumbered at landing so that none collides | `claims_register.toml`; `tests/test_claims_register.py` |
| Vocabulary check | terms follow `glossary.yaml`; "hole" is reserved and flagged | `scripts/check_vocabulary.py`; `work-packages/WP38-review.md` ("Gates") |
| Container regression | the paper's data regenerated in the container: `0 drifts` over 74 entries at the WP30 data gate (image `27add815d66c`, head `c64430e`). The notebooks changed by the WP42 build, WP46 and the fifth paper unit were re-executed on their merged trees; no container regression was run at the head | `paper/container/RECORD.md`; `work-packages/WP8b-release-checklist.md`, C1 to C5 |
| Residual pass checker | counts per prose surface of patterns that read as machine-written; no count has risen against the retaken baseline | `scripts/check_residuals.py`, `scripts/residuals_baseline.json`, `tests/test_residuals.py`; `work-packages/WP38-landed/final-compare-after-retake.txt` |
| WP43 spike rerun | after the lint pass the spike reran: every number in the data files identical; the three figures are the same data but not the same bytes (8 and 18 percent of pixels differ, text placement; the pre-lint scripts give the same new bytes, so the renderer differs) | `work-packages/WP43-rounds/spike/rerun-record.md` |
| WP50 instance | the instance script rerun by the driver: `results.json` byte-identical to the committed one; three of seventeen DOIs drawn and resolved | `work-packages/driver-log.md` ("WP50 readout verified"); `work-packages/WP50-rounds/spike/` |
| WP48 repository reads | three of the readout's reads of the repository repeated and confirmed (default token permission `write`, no ruleset on `main`, vulnerability alerts on) | `work-packages/WP48-decisions.md` |
| Release workflows | the eight verification cases run as scripts on payloads and as tests; the workflows have not run on GitHub | `work-packages/WP47-rounds/checks.md` |

### The residual pass's machinery (WP38)

- The reader's brief: `docs/superpowers/notes/residual-review.md` (ten kinds).
- The surface inventory: `scripts/prose_surfaces.py` (95 surfaces, 71,474 words at `c0fe11b`).
- The checker: `scripts/check_residuals.py`, with its committed baseline `scripts/residuals_baseline.json`. Re-run it
  with `--compare scripts/residuals_baseline.json` to see that no count rose; `--strict` exits 1 if one did.
- The test: `tests/test_residuals.py`.

## Human validation

| Evidence | What people did | Where |
|---|---|---|
| Final reader round, core | 46 reads of the paper and docs at stage head `c23cf60`, depths A to D, against answer key version 5 (hash committed first, key held outside the repository) | `work-packages/WP11-final/`; `work-packages/WP11-decisions.md` ("The final reader round") |
| Final reader round, held-out | 12 reads (waves 8 and 9, stage head `5ac44f7`): one wrong belief at depth A (the abstract's Pareto sentence read in reverse, which you kept as written), record defects found only at depth D and settled in the fifth paper unit; every wave-9 reader agrees with its wave-8 twin on the cell's job | `work-packages/WP11-final/triage/wave-8.md`, `wave-9.md` |
| Figure loop | fresh cold reads of Figures 3, 6 and 7, each image alone and then with its caption | `work-packages/WP11-final/figure-review-paperfix3.md`; `work-packages/WP42-rounds/build-record/cold-read/` |
| Earlier reader rounds and the reader grid | personas read the paper and docs at depths A to D | `work-packages/WP11-decisions.md`; `docs/superpowers/notes/reader-grid.md` |
| Package-user tests | four user tasks from the README, in three rounds, accepted | `work-packages/WP32-review.md`; `work-packages/WP32-decisions.md` |
| Wayfinding rounds | root page and docs routing | `work-packages/WP33-review.md` |
| Residual pass | 29 first-reader slots with 1,215 flag rows; 96 second-reader form rows (94 surfaces), 18 read clean and 78 still carry flags | `work-packages/WP38-flags/`; `work-packages/WP38-confirmations/`; `work-packages/WP38-review.md` |
| Expert and novice mathematics reads | read before the final round | `work-packages/WP29-review.md`; `work-packages/WP35-review.md` |
| Your reads in the browser | the docs home (landed on your word), the history page (taken as passable) and the root page | `work-packages/WP51-decisions.md`; `work-packages/WP52-decisions.md`; `work-packages/driver-log.md` |
| Fresh read of the bridge page | one fresh reader's page requests | `work-packages/WP41-review.md` |

What no reader could test in the residual pass (`work-packages/WP38-review.md`, "What no reader could test"): no
screenshots were saved; the case-model page is not on the docs site; the README was read as file text; the generated
lemma tables were not read separately; mathematics was read from page text, not typeset.

# What was verified, and how

Two kinds of checking, kept apart. A machine check says a statement holds on the committed inputs. A human validation
says a person reading the thing found it right, clear or useful. Neither stands in for the other
(`docs/superpowers/notes/presentation-framing.md`).

## Machine verification

| Check | What it covers | Where the result is recorded |
|---|---|---|
| Full suite, lint, format, lock | the package, the derivations, the site builds | `work-packages/driver-log.md` ("Verification snapshots by the driver"); latest CI row in this guide: run 43564973529 on `2a12f7f`, every job green on both platforms (`work-packages/driver-log.md`, "2a12f7f fully green") |
| CI on three platforms | Linux fast, slow and docs-paper; Windows fast and slow (the paper's build stays Linux and macOS) | `work-packages/WP34-decisions.md`; macOS through the maintainer's watcher, verdicts in `work-packages/driver-log.md` |
| Lemma chain and proof map | the derivation scripts, 20 lemma files, 505 tagged steps (`work-packages/deliverables-grid.md`) | `derivation/PROOF_MAP_FINDINGS.md`; run `uv run python -m derivation.proofmap` |
| Claims register | each stated claim has a backing | `claims_register.toml`; `tests/test_claims_register.py` |
| Vocabulary check | terms follow `glossary.yaml`; at `c0fe11b`: 0 new violations, 61 known | `work-packages/WP38-review.md` ("Gates") |
| Container regression | the paper's data regenerated in the container: `0 drifts` over 74 entries, 11 current | `paper/container/RECORD.md` ("Container regression at the WP30 data gate", image `27add815d66c`, head `c64430e`) |
| Residual pass checker | counts per prose surface of patterns that read as machine-written | below |

The container regression above ran at the WP30 data gate. A regression at the release head is not recorded
(`work-packages/WP8b-release-checklist.md`, C1 to C5).

### The residual pass's machinery (WP38)

- The reader's brief: `docs/superpowers/notes/residual-review.md` (ten kinds).
- The surface inventory: `scripts/prose_surfaces.py` (95 surfaces, 71,474 words at `c0fe11b`).
- The checker: `scripts/check_residuals.py`, with its committed baseline `scripts/residuals_baseline.json` (retaken at
  `c0fe11b`). Re-run it with `--compare scripts/residuals_baseline.json` to see that no count rose; adding `--strict` exits 1 if one did. At
  `c0fe11b` against the retaken baseline: 0 rose, `--strict` exit 0
  (`work-packages/WP38-landed/final-compare-after-retake.txt`). Against the old baseline 28 counts were above it, at
  pass start and at pass end (`work-packages/WP38-landed/final-compare-before-retake.txt`).
- The test: `tests/test_residuals.py` (9 passed at `c0fe11b`).

## Human validation

| Evidence | What people did | Where |
|---|---|---|
| Final reader round | not yet run (answer key version 5 fixed; the assistant's five settings recorded) | pending; `work-packages/WP11-decisions.md` ("The final reader round") |
| Earlier reader rounds and the reader grid | personas read the paper and docs at depths A to D | `work-packages/WP11-decisions.md`; `docs/superpowers/notes/reader-grid.md` |
| Package-user tests | four user tasks from the README, in three rounds, accepted | `work-packages/WP32-review.md`; `work-packages/WP32-decisions.md` |
| Wayfinding rounds | root page and docs routing, steps 47 to 30, none rose | `work-packages/WP33-review.md` |
| Residual pass, first readers | 29 reader slots, 1,215 flag rows | `work-packages/WP38-flags/` |
| Residual pass, second readers | 96 form rows (94 surfaces): 18 read clean, 78 still carry flags | `work-packages/WP38-confirmations/`; `work-packages/WP38-review.md` |
| Expert and novice mathematics reads | read before the final round | `work-packages/WP29-review.md`; `work-packages/WP35-review.md` |
| Browser passes | pages read as rendered; screenshots from commit `2a669de` | `work-packages/WP40-review.md`; `work-packages/README.md` |

What no reader could test in the residual pass (`work-packages/WP38-review.md`, "What no reader could test"): no
screenshots were saved; the case-model page is not on the docs site; the README was read as file text; the generated
lemma tables were not read separately; mathematics was read from page text, not typeset.

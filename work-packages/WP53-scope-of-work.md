# WP53 — Scope of work: integrate the review batch of 2026-11-15

| | |
|---|---|
| **Status** | Approved verbally, "approve 53 and 54" (2026-11-15, `WP53-decisions.md`) |
| **Supervisor (accountable)** | mzargham |
| **Repository** | `DynamicalSystemsGroup/hyperbolic-trade-space`, branch `dev` |
| **Approval record** | His words, quoted verbatim in `WP53-decisions.md` |
| **Acceptance record** | The driver's verification in `driver-log.md`; his word on the rendered result when he next reads |

## Purpose

His review of the abstract and Sections 1 to 3 was applied in place, in the working tree, with no tests or rebuilds
between edits. This package lands that batch on `dev` as one verified commit, so the packages that follow (WP54 to
WP58) build on a head that holds his text.

## Goals

- G1. The batch on `dev`: every edit recorded in `WP11-decisions.md` from "The abstract, his review of the candidate
  (2026-11-15 08:40 EST)" onward, as the working tree holds it, with nothing else changed.
- G2. The two drawings he approved (the three layers of prior art, the pipeline) produced by code, so Section 11's
  sentence "Every figure, table and reported number comes from a call into a tested module" stays true.
- G3. The records and tests that quoted the old text follow it: the claims register, the paper tests, the vocabulary
  baseline, the proof map if a definition label moved.

## Non-goals

- Any prose change beyond his edits (WP54 to WP57 own those). Re-lettering the appendices (WP57). Merging `wp51fig`.
- Changing the version.

## Deliverables

| ID | Deliverable | Serves |
|---|---|---|
| D-1 | One commit on `dev` holding the batch, the notebooks re-executed on it, pushed, CI dispatched | G1 |
| D-2 | `paper/figures/prior_art_layers.py` and `paper/figures/pipeline.py`, each writing its SVG beside it from text constants, registered where the paper's static figures are registered (`scripts/build_figures.PAPER_FIGURES`, `tests/test_paper_static_figures.py`), with a test that the committed SVG equals the generated one | G2 |
| D-3 | The claims register updated: rows whose fragment left the paper dropped or re-anchored (ids append-only, never reused), rows for his new sentences where they state a checkable fact (kind S) | G3 |
| D-4 | `work-packages/WP53-review.md`: the verification record (the checks run, their results, the register rows touched by id) | acceptance |

## Requirements and checks

| ID | Requirement | Check |
|---|---|---|
| R-1 | The abstract in `paper/paper.ipynb` equals `work-packages/review/abstract-draft.md` (whitespace aside) | a line in the review file comparing the two |
| R-2 | Nothing outside the batch changes | `git diff --stat` against `2875c11` lists only the files of the batch (the paper notebook, `paper/prior_art.yaml`, `paper/figures/`, `docs/references.bib`, the two notes under `docs/superpowers/notes/`, the register, tests, `work-packages/`) |
| R-3 | Lint, format, lock | `uv run ruff check .`, `uv run ruff format --check .`, `uv lock --check` |
| R-4 | The paper builds with no warning about a missing label, figure or citation | the MyST build log |
| R-5 | The suite | `uv run pytest -q -m "not slow"` green; the slow paper and docs tests green where a figure or page changed |
| R-6 | Residuals and vocabulary | `scripts/check_residuals.py` exit 0; `scripts/check_vocabulary.py` 0 new |
| R-7 | No AI attribution | `git log` of the commit free of Co-Authored-By and generated-by lines |
| R-8 | CI on the landing head | the dispatched run green on both platforms, recorded by run id |

## Definition of good

His text on `dev`, rendered as he reviewed it on 8797, with every check green and every record following.

## Definition of good enough

R-1 to R-7 met and recorded; R-8 dispatched and green at the fast jobs, the slow jobs recorded when they finish.

## Definition of done

Good enough met, no open item, and the driver's verification in `driver-log.md`.

## Open decisions

None.

## Agent's defaults

- The figure generators write SVG from Python string constants (no drawing library), matching the committed files
  byte for byte, with the glosses as module constants.
- Register rows that quoted cut sentences are dropped (their ids retired, never reused); rows whose fragment was
  reworded take the new fragment.
- The notebooks are re-executed with a warm `MPLCONFIGDIR` so no stderr enters an output.

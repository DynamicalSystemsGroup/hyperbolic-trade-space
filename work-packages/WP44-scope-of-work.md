# WP44 — Scope of work: a second case study from a public dataset (research spike)

| | |
|---|---|
| **Status** | DRAFT. The hunt is read-only and runs at once; the build of an example waits on the supervisor's choice from the readout. |
| **Supervisor (accountable)** | mzargham |
| **Repository** | `DynamicalSystemsGroup/hyperbolic-trade-space`; work on `dev`, in a spike folder |
| **Approval record** | The supervisor's direction of 2026-11-14 14:05, verbatim in `WP44-decisions.md` |
| **Acceptance record** | The supervisor's choice from the readout, quoted verbatim in `WP44-decisions.md` |

## Purpose

The supervisor's direction (`WP44-decisions.md`): a case study independent of the synthetic satellite, from a public
dataset with configurations and measured attributes whose phenomenon includes trade-offs, natural sciences welcome; for
the package and the documentation's examples, to support the paper's claims with a second table and to help people
using the tool; not for the paper.

## Goals

- G1. **A ranked list of candidates that meet the criteria:** an open licence that permits redistribution of a derived
  example (or a fetch-at-build route if not); a stable source, DOI or archival URL; configuration columns
  (controllable inputs, treatments or categorical design choices) and at least four measured attributes that condition
  to strictly positive, larger-is-better metrics; at least two hundred rows; a trade-off the field's literature names,
  with a citation; documentation of the columns and units.
- G2. **Each candidate mapped to the pipeline:** which columns are configuration, which attributes, the conditioning
  each attribute needs (orientation, shift, scale), what the n-lemma is expected to say if the literature's trade-off
  is real, and what a reader of the docs would learn from it that the cubesat does not teach.
- G3. **Plain options for the build:** one or two candidates to build as Examples pages, with the work each needs
  (fetch, conditioning rule, the fit at K = 1 and 2, the tension matrix once WP42 lands, the requirements-after-the-fit
  reading if the field has thresholds).

## Non-goals

- Building any example, fetching any dataset into the repository, or changing `docs/`, `src/`, `examples/` or the paper.
- Datasets without a licence or a stable source; datasets whose only attribute is one target (a regression benchmark).
- Synthetic or simulated tables (the satellite is one; the spike seeks measured data).

## Deliverables

| ID | Deliverable | Serves |
|---|---|---|
| D-1 | `work-packages/WP44-rounds/hunt/candidates.md`: at least eight candidates in a table (source with DOI or URL, licence, rows, configuration columns, attribute columns, the trade-off and its citation, the pipeline mapping, a fit of the criteria), natural sciences first, engineering and economics after | G1, G2 |
| D-2 | `work-packages/WP44-rounds/hunt/readout.md`: the ranking against the criteria, the two or three strongest with what a docs example would show, plain options for the build and its package | G3 |

## Requirements

| ID | Requirement | Checked by |
|---|---|---|
| R-1 | Every candidate's source resolves (DOI or URL fetched on the day, noted) and its licence is quoted from the source | the readout's source column; the reviewer resolves three at random |
| R-2 | Every trade-off claim carries a citation to a published source with a DOI | the candidates table |
| R-3 | No file outside `work-packages/WP44-rounds/` changes | `git diff --stat` |

## Definition of good

- The supervisor can pick a dataset from the readout and know what the example will show, what it costs to build and
  what it cannot show.

## Definition of good enough

- D-1 and D-2 delivered; R-1 to R-3 pass; at least three candidates meet every criterion of G1.

## Agent's defaults

- The hunt runs as one research agent on Sonnet with web search, then a second pass by the assistant on the top five
  for licence and source checks *(default)*.
- Natural sciences first (ecology and life history, plant and leaf economics, materials and alloys, agronomy trials,
  enzyme and protein data), then engineering experiments (building energy, concrete, vehicles, batteries), then
  economics (production and efficiency tables) *(default)*.

## Open decisions (for the supervisor)

None. The direction of 14:05 settles the aim; the choice of dataset is the readout's gate.

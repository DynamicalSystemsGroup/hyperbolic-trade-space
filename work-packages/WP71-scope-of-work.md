# WP71 — Scope of work: Broadbalk, the level V against biomass (a bounded update)

| | |
|---|---|
| **Status** | DRAFT, approved by the driver as his proxy on his direction of 2026-11-16 (`WP71-decisions.md`); runs after the level-set figure lands |
| **Supervisor (accountable)** | mzargham |
| **Repository** | `DynamicalSystemsGroup/hyperbolic-trade-space`; `docs/examples/wheat.md`, `examples/wheat/` (its variants or results generator), `claims_register.toml`; branch `wp71` |
| **Approval record** | The driver's approval under his mandate, quoted in `WP71-decisions.md` |
| **Acceptance record** | The driver's soft-confirm on the rendered page; his read |

## Purpose

His direction: "simply update the broadbalk wheat example so it calls out the observation that the V levels correlate
strongly with biomass which is cool and intuitive but bounded."

## Goals

- G1. **The observation, backed:** the correlation (or the regression slope, whichever the generator already
  produces more naturally) of log V with log biomass across the 3,753 plot-years, computed by the example's
  generator and written to its results file, so the page's number is a generated value with a register row.
- G2. **The sentence on the page,** in the arc's interpretation part: the fitted level is a biomass-like index
  (a weighted geometric mean of the two yields), it tracks biomass across the plot-years with the number of G1, and at
  a fixed level grain trades against straw at the rate the exponents give; the derived-metric sentence already on the
  page (biomass takes exponent 0.00) stays as the detection. No new figure: the level-set figure carries the picture.
- G3. **The register and tests follow:** a row for the number; the record test, the word budget and the residual
  checker green.

## Non-goals

No new plot (the reusable size-against-shape plot is the plotting step two's); no change to any other page, to the
package or to the paper; no claim about conservation (that is WP72's question).

## Deliverables

| ID | Deliverable | Serves |
|---|---|---|
| D-1 | The generator's new value and the results file regenerated | G1 |
| D-2 | The page's sentences; the register row; a capture of the rendered paragraph under `work-packages/WP71-rounds/` | G2, G3 |

## Requirements and checks

| ID | Requirement | Check |
|---|---|---|
| R-1 | The number is produced by the generator from the committed derived table and quoted exactly | `tests/test_wp45_examples.py` (the wheat record test) green |
| R-2 | The page stays within its word budget; no metanarration; vocabulary 0 new; residuals no new rise | `tests/test_site.py -k word_budgets`; `check_residuals.py --strict`; `check_vocabulary.py` |
| R-3 | The register test green; no attribution line; nothing outside the named files | `tests/test_claims_register.py`; `git diff --stat dev` |

## Definition of good

A reader of the wheat page sees, in two sentences backed by a number, that the level is size and the level set is
the trade.

## Definition of good enough

D-1 and D-2; R-1 to R-3; the driver's soft-confirm; landed for his read.

## Definition of done

Good enough met; his read recorded.

## Open decisions

None.

## Agent's defaults

- Correlation of log V with log biomass on the standardized-log fit of record (K = 1, the page's tau), reported to two
  decimals; the value lands in `examples/wheat/results.json` under a named key.

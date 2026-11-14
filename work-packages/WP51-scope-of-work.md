# WP51 — Scope of work: the root page recast (why, what, how) with the three-metric figure

| | |
|---|---|
| **Status** | DRAFT. Approved only by the recorded act below; the prose draft already exists on branch `rootpage` for his close read, nothing merges before his word. |
| **Supervisor (accountable)** | mzargham |
| **Repository** | `DynamicalSystemsGroup/hyperbolic-trade-space`, branch `rootpage` from `dev` |
| **Approval record** | The supervisor's verbal approval, quoted verbatim in `work-packages/WP51-decisions.md` |
| **Acceptance record** | His close read of the rendered page and his word to merge, quoted verbatim in `WP51-decisions.md` |

## Purpose

His direction of 2026-11-15 (`WP51-decisions.md`, `WP33-decisions.md` 00:20 to 00:45): the root page gets a why (the
line between what is possible and what is preferable), a what (the former why) and a how (the former what), without
headers; and the how's figure is drawn from the same three-metric planted table as the ternary, so the page is one
example throughout and shows a trade among more than two metrics.

## Goals

- G1. **The prose:** three sections in depth order, no headers; the summary paragraph and the two doors unchanged; the
  two vocabulary edits already ruled for this page ("explains trade-offs", "contend"). Drafted; his close read first.
- G2. **The figure:** from the planted three-metric table of `scripts/build_site_figures.py` (the ternary's fit, three
  terms), a three-by-three figure: rows the metric pairs (1 against 2, 2 against 3, 1 against 3); columns the metric
  space (the fitted reference surface's slices), the log space (the envelope's slices), and the chart's slice along the
  pair's axis (the direction of log m_i minus log m_j in the position plane, log V as height); in every pane the third
  metric is the fan parameter at three values, light to dark, so a reader sees the terms appear and leave as the third
  metric moves. One design marked in every pane as the current figure marks one. Light and dark renders.
- G3. **The ternary as the whole view:** kept beside the new figure, its caption saying it is the same table and the
  one view of the whole position space (every design by its shares, the regions where each term leads).
- G4. **The loop:** the figure-review recipe written before the draw (question, takeaway, sentence); cold reads of the
  rendered page, image alone then caption, by fresh readers; the five tests recorded; smallest change first.
- G5. **The record:** the claims register carries the why paragraph as framing; the site tests pin the new structure
  and the figure's placement; the figure's generator and a test that it is drawn from the ternary's fit.

## Non-goals

- The paper's Figure 1, its caption and the paper's text; the README; the docs home (their consistency rows stay
  with WP42's entry-surface list).
- Any governance wording on the page beyond the why paragraph as drafted.

## Deliverables

| ID | Deliverable | Serves |
|---|---|---|
| D-1 | `site/index.html` body (three sections, no headers) | G1 |
| D-2 | The figure's generator in `scripts/build_site_figures.py`, its light and dark images built at stage time, the caption | G2, G3 |
| D-3 | `work-packages/WP51-rounds/figure-review.md` with the recipe, the before and after images, the cold-read reports verbatim, the five tests | G4 |
| D-4 | Tests in `tests/test_site.py`; the claims row | G5 |

## Requirements

| ID | Requirement | Checked by |
|---|---|---|
| R-1 | The figure is drawn from `fit_why()`'s fit, not a second fit; a test asserts it | the test |
| R-2 | Every pane's fan uses the same three values of the third metric, stated in the caption | the figure-review record |
| R-3 | The page reads as its three sentences say to fresh readers, image alone then caption | the cold reads |
| R-4 | No word on the page claims what the paper does not back; the why paragraph is a framing row in the claims register | the register test |
| R-5 | Gates: full suite, ruff check and format, lock check, vocabulary and residual checks, the site tests; a browser pass at desktop and phone width, light and dark | the driver |

## Definition of good enough

- D-1 to D-4 delivered; R-1 to R-5 pass; his close read of the rendered page taken and his edits applied; his word to
  merge recorded.

## Agent's defaults

- Three fan values of the third metric at its 20th, 50th and 80th percentile over the planted table *(default)*.
- The pair's axis in the chart pane is `(e_i - e_j)/sqrt(2)` in the position plane; the slice holds the third
  coordinate at the fan value and shows the designs within a band of it *(default)*.
- The unit runs on Sonnet in the `rootpage` worktree after his close read of the prose; the cold readers are Haiku
  *(default)*.

## Open decisions (for the supervisor)

None in the problem; his close read of the prose is the next act.

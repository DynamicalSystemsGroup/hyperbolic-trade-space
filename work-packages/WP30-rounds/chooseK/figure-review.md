# Figure review: the case figures redrawn at K = 2 (unit chooseK, 2026-11-11)

Screenshots for this record: commit `c680853`, `git show c680853:<path>` with `<path>` under `work-packages/WP30-rounds/chooseK/screenshots/`.

Reviewer: the unit's author (no fresh-context cold readers were run; the figure-review note's cold read is the
PM's to schedule). The images were looked at as rendered files and, once the paper was built, in the page
(`screenshots/`). K = 2 is `case.CASE_K`, the K the package's own choosing-K checks pick (Appendix D.15).

## The K = 3 figures leave the body

The sentence test for keeping them as a labelled "one step too many" figure: the step is a number (the thinnest term
holds 0.06 of the near-frontier designs at K = 3 in both regimes), and the generated sentence `num-choosing-k` says it
with the table behind it in D.15. A picture of three panels would add the third term's line and heatmap, which the
rows of D.2 and D.3 carry. The K = 3 planes and association figures are dropped; the chart (a single image) is drawn
at K = 2 like the others.

## fig-planes-case (was fig-planes-k3)

- Intent: each term's trade-off as its own line in its own pair of metrics; the designs near the slice's median stop at
  the line.
- Sentence: "Term 1 trades pointing error against peak slew power along a line; term 2 trades available power against unit
  cost."
- Ink as data: two panels, the designs fill both frames (about nine tenths of each); legend in the empty lower-left of
  the bottom panel, over no design; the line is one stroke.
- Legible: the labels at the column width are the metric names and the "term 2" tag on the segment.
- Shows: each term's slope in the plane of its two heaviest metrics. Does not show: the surface bending where terms
  meet (the one pair both terms weigh shows term 2's line alone, tested), any grouping, the other eleven metrics.
- Disposition: redraw at K = 2 (committed code `paper/figures/planes.py`, `case.CASE_K`); caption rewritten to the
  panels now drawn (the torque-streak sentence went with the panel that no longer exists).

## fig-chart-level

- Intent: a design's level apart from its position along the surface. The chart coordinates do not depend on the
  number of terms except through the level, so the figure changes in the level only.
- Disposition: redrawn at K = 2 (`paper/figures/chart_level.py`), caption "K = 2".

## fig-tensions-case (was fig-tensions-k3)

- Intent: which metrics trade on each term, with its contending set and exponents.
- Sentence: "Term 1 (8 metrics) and term 2 (7 metrics) have different contending sets, and the association among the
  near-frontier designs of each term's cell shows what trades."
- Ink as data: two heatmaps of thirteen metrics each, fully used.
- Disposition: redrawn at K = 2 (two panels in the figure's existing layout); caption "each term of the K = 2 fit".

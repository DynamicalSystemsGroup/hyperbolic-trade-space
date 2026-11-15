# WP60: the perovskite page, figure record

Page: `docs/examples/perovskite.md`. Figure 8 in the docsite's sequence, drawn by the `{.runnable}` block above it
(`run.load`, the primary conditioning, `select_temperature`, a one-term fit, `plot_ternary(lines=True)`). Images:
`perovskite-figure-light.png` and `perovskite-figure-dark.png` beside this record, copied from the build.

## The sentence test

The one sentence a reader takes from the figure alone: the devices crowd one part of the triangle, away from the Voc
corner, and a single region, labelled "all three trade", covers it, so no metric is traded for free.

The caption completes it: it names the three metrics at the corners, the 40,045 devices, the star as the one-term
fit's exponent vector and the contours as equal V at a fixed total. The figure alone does not say what the star or
the contours are; the caption does.

## Choices and limits

- One term, not two. At K = 2 `plot_ternary` with the table raises "no room for the labels inside their regions":
  the second term holds 2.4 percent of the rows, so its region is too small to label. Markers alone at K = 2 (no
  table) draw the second exponent vector on the FF edge but show no devices and no regions, so the figure is the
  one-term fit; the K = 2 reading is in the prose.
- The figure shows no association signs or ranges; those are in the prose, from `variants.json`.

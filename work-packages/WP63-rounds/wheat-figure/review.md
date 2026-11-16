# Figure 10 (wheat): from one line to lines of equal V, the figure loop

His direction (verbatim in `work-packages/WP63-decisions.md`): "as drawn it reads like fit line and feels off. but if
instead we drew level sets with labeled values of V i think it would make its point much better, it also shows the the
tool is still useful even when the trade-off in question is only 2 dimensional". This unit covers the first step only:
`plot_log_plane(..., levels=None)` and the wheat page. The default drawing and its other uses come after his read.

## The recipe (written before the cold reads)

- **Question:** where do Broadbalk's plot-years sit relative to the fitted frontier, and what does the frontier say
  about grain against straw?
- **Intended takeaway:** the frontier V = 1 is one of a family of parallel straight lines of equal V. Every plot-year
  lies on one of those lines. V rises toward the upper right, and the dense cloud runs up to the frontier with a minority
  above it. Each line falls, so at equal V the model trades grain for straw.
- **Sentence (test 2):** "In the log plane the fit is a family of falling straight lines of equal V, the frontier
  V = 1 among them, and Broadbalk's plot-years spread across the levels up to the frontier."

## The drawing, round by round (images in the scratchpad, not kept)

1. Levels (0.2, 0.4, 0.6, 0.8, 1, 1.2), labelled by `clabel` at the point of each line farthest from the designs.
   Every label landed on the frame's top edge; 0.8 and 1 overlapped; the dense cloud hid the lines. Redrawn.
2. Levels (0.1, 0.25, 0.5, 1, 1.5): round values, roughly even in log V (gaps of 0.4 to 0.9), so the lines are evenly
   spaced and the labels have room. Each label sits at the line's end inside the frame, on whichever side (left or right)
   is farther from the designs, so the labels stack beside the cloud at the spacing of the lines. The labels separated,
   but the lines still disappeared inside the cloud.
3. With `levels`, the designs are drawn smaller and translucent (size 8, alpha 0.45) so the lines read through the cloud.
   The labels are 9 pt.
4. The label inset grew from 6 to 10 percent of the frame, which moved the labels off the top edge. This is the
   drawing the cold reads judged.

`clabel` was kept over hand-placed text for three reasons: it rotates each label along its line, breaks the line under
the label, and handles the K > 1 envelope the same way (a contour of the hard-max envelope over a grid). Only the
label positions are chosen here.

## The band

Dropped from this figure. `levels` draws the band only when `band` is passed. The band's job was to mark the
near-frontier plot-years, and the band here is 0.12 wide in log V, about 0.17 in the plane. That is narrower than the gap
between the frontier and its nearest level (log 1.5 = 0.41), so beside the levels it adds ink without adding a reading.
The temperature selection that sets it is stated in the prose ("a band of 0.12 in log V"). A level at V = exp(-0.12) =
0.89 would carry the band, but it would crowd the V = 1 label and was not needed for the intent.

## Test 1: the cold reads (verbatim, image first, caption second)

**Reader A** (light image, first caption):

> (1) The figure is a scatter of a few thousand points: standardized log grain on the x-axis against standardized log
> straw on the y-axis. Over it sit parallel straight lines of equal V (0.1, 0.25, 0.5, 1, 1.5), and V = 1 is drawn in
> bold black as the "frontier".
> (2) Most points sit in a dense cloud near (0, 0), with a long sparse tail toward low grain and low straw. The cloud
> runs along the frontier V = 1, and only a few points go past it toward V = 1.5. So V ranks the points by grain and
> straw together, and the frontier marks roughly the outer edge of the observed data.
> (3) The "V = 1" label is crowded by the dense cloud next to it. I could not tell what V stands for: it is not
> defined, and neither are its units. The frontier lies inside the cloud's upper edge rather than wrapping it, which
> makes it unclear whether points above V = 1 count as outliers or as a bad fit.

> Caption ("…with lines of equal V from 0.1 to 1.5; the heavy line, V = 1, is the fitted frontier. Every line falls: at
> equal V, more grain comes with less straw."): Yes, it changes my reading in two ways. First, it names the data as
> Broadbalk plot-years and says V = 1 is the fitted frontier, so I now take the points that pass V = 1 as residuals of
> the fit, not outliers. Second, its line "at equal V, more grain comes with less straw" is true of the drawn lines, but
> the cloud of points rises from lower left to upper right, so plot-years with more grain also have more straw. A reader
> could take that trade-off as something the data show, when it describes the model's lines. V is still not defined.

**Reader B** (dark image on the slate background, first caption):

> (1) The figure is a scatter of several thousand points: standardized log grain on the x-axis and standardized log
> straw on the y-axis. Over the points sit parallel straight contour lines labelled V = 0.1, 0.25, 0.5, 1 and 1.5. The
> V = 1 line is drawn in bold white and named "frontier V = 1".
> (2) The cloud runs from lower left to upper right, so grain and straw rise together. Its dense core sits just below
> the V = 1 frontier, and only a few points cross it. The low-V lines mark the sparse lower-left tail of poor performers.
> (3) The legend does not say what V is or whether higher V is better. The V = 1.5 label is crowded by the dense points
> near the top. Nothing explains why the contours slope downward while the data slopes upward.

> Caption: Yes, the caption explains the falling lines: they show the grain-for-straw trade at equal V, and the rising
> cloud just means plot-years spread across V. It also names the dataset (Broadbalk plot-years) and says what V = 1 is.
> It still does not say what V measures or whether higher is better, so the points sitting just below the frontier can
> only be read relative to it.

**Triage.** Both images conveyed the family of levels and the frontier among them, so the drawing was kept and the
fix went into the caption. Reader A caught the first caption stating the model's trade-off in words a reader could take
as a property of the data. Both readers wanted V defined. The caption was revised: V is glossed as a weighted geometric
mean of both yields, and the trade is attributed to the model ("Along each line the model trades grain for straw").
The register keeps the data's association (-0.87 near the frontier) in the prose.

**Reader C** (fresh, light image, final caption):

> (1) It's a scatter of a few thousand points: standardized log straw against standardized log grain. Parallel grey
> lines labelled V = 0.1, 0.25, 0.5 and 1.5 run down to the right, and a heavy black line marks V = 1. The legend reads
> "frontier V = 1" and "lines of equal V".
> (2) The two yields move together, and most points sit in one dense cloud near the origin with a sparse tail toward
> low yields. The fitted frontier V = 1 runs through the upper part of the cloud, so a fair number of points lie above
> it, between V = 1 and V = 1.5.
> (3) All labels were readable. Nothing in the figure says what V is, what the data are, or why some points lie above
> a line called the frontier.

> Caption: it gives the data (Broadbalk plot-years) and defines V as a weighted geometric mean, which explains why
> lines of equal V are straight with a negative slope. "Trades grain for straw" says how to read the slope. It does not
> explain the points above the frontier.

**Comparison with the intent.** The figure with its caption now matches the intended takeaway: a family of falling
lines of equal V, the frontier one of them, the plot-years spread across the levels, and the model's trade read from
the slope. Two gaps remain, both left on purpose:

- Why rows lie above the frontier. The sentence directly above the code block carries it (the temperature "puts a tenth
  of the rows above the frontier"), and the page is at its word budget (700 of 700).
- The rising cloud against the falling lines. That is the model and the data kept apart, as the page keeps them: the
  association near the frontier (-0.87) is the analysis and lives in the prose.

The "crowded" labels in rounds A and B were the 1 and 1.5 labels near the top of the cloud. Reader C, on the same
drawing, read every label.

## Test 2: the sentence

"In the log plane the fit is a family of falling straight lines of equal V, the frontier V = 1 among them, and
Broadbalk's plot-years spread across the levels up to the frontier." Deleting the figure loses where the 3,753
plot-years sit across the levels: the middle half between V = 0.31 and 0.77, a tenth below 0.13, a tenth above 1
(quantiles of `score_samples` on the page's fit). The sentence alone
cannot carry that. Kept.

## Test 3: ink is data

The frame is set by the designs and by their diagonal projections onto the outermost levels. Before, the frontier line
ran out to grain 4 above an empty upper right; now no line extends past the frame. The empty areas are the upper left, above
the sparse tail, which carries the labels, and the lower right lies beyond the data at equal V, between the lines, which carries the legend. The legend's two entries repeat what the inline labels say. They are kept as the key to the
two line weights.

## Test 4: legibility where it is read

Captured at 1,280 px in headless Chrome. The image is drawn 673 CSS px wide in the column. Light (`after-light.png`):
every label (V = 0.1, 0.25, 0.5, 1, 1.5) reads, grey 0.5 on white, and the frontier label is black. Dark
(`after-dark.png`): the levels and their labels are mid grey on slate and read; the frontier and its label are white;
the translucent cloud is dimmer than in light but its extent reads. No label covers a design that carries the reading.

## Test 5: shows, does not show, good for

- **Shows:** the one-term fit as lines of equal V in log grain against log straw, the frontier V = 1 among them, and
  where the 3,753 plot-years sit across those levels.
- **Does not show:** the association near the frontier (an analysis, in the prose), the second term of the two-term fit,
  the conditioning variants, or which plot-years are which cultivar.
- **Good for:** reading a plot-year's level against the frontier, and seeing that in two metrics the fit's level sets
  are straight lines whose slope is the trade.

## Captures (this directory)

- `before-light.png`, `before-dark.png`: the figure file as rendered from the base, dev at 06ea3580 (one frontier line
  and the band), at the build's size.
- `after-light.png`, `after-dark.png`: Figure 10 with its caption on the built page, at 1,280 px, light and dark
  (`capture.py`).

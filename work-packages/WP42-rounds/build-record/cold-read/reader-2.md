# Reader 2 (Haiku, image: images/fig-tension-matrix.png), verbatim

PART 1 (image alone)

The figure shows, for two terms of the trade-space fit, how strongly each metric that rises trades against each metric that gives way, with each cell's printed number as a signed exponent and its colour as the size of that tension on a log scale. I take from it that on term 1 the trades involving pointing error and peak slew power against depth of discharge are the steepest, and that depth of discharge sits at the bottom of most of the term 1 columns' trades in size, while on term 2 unit cost (as the rising metric) is the steepest row.

A coloured cell means a metric pair that carries an exponent on that term. The colour runs brown (about 0.1) through white (1) to dark green (10 and above), and the colour tracks the magnitude of the printed number, so brown is a small tension and green a large one. The white or near-white cells are the ones near 1 in magnitude, for example -1.1 for pointing error against unit cost on term 1.

Grey cells are empty, not zero. They sit on the diagonal (a metric against itself) and in pairs where the metric does not carry an exponent on that term, as the captions say (8 of 13 metrics on each term). No cell shows a literal zero. The smallest magnitude is -0.03 (total mass rising against unit cost on term 2).

On term 1 the steepest trade is pointing error rising while depth of discharge gives way, at -17. Peak slew power against depth of discharge is close behind at -16. Term 2 is steepest for unit cost rising while total mass gives way (-30), with unit cost against depth of discharge (-19) next.

I take the numbers as model output, not data. The figure shows no observations, only exponents and weights (w) from the fitted terms, so the values are only as good as the fit that produced them.

I take "unit" to be part of the metric name "unit cost", which appears in both panels. The figure does not define it. From context I read it as a cost per unit (per spacecraft built), not a unit of measure, but the figure does not say so and a reader could not tell from the figure alone.

Cold-read issues: the figure leans on the caption for what the rows and columns mean, the colour bar labels only three ticks (0.1, 1, 10), and "the metric that gives way" is not explained beyond the caption. A reader who has not seen the method would need the caption to read it correctly.

PART 2 (caption)

Report on fig-tension-matrix.png (cold read, image only; no other files read).

What it shows: for two terms of the trade-space fit, a heatmap of how strongly each metric that rises (rows) trades against each metric that gives way (columns). Each printed number is a derivative, and each colour is that derivative's size on a log scale. Revised after the caption came in: the caption says each cell is the change in the column metric per one unit of the row metric's conditioned value, at the term's balanced point, not a signed exponent or a logarithm step. Every drawn cell is negative.

Colour: brown is a small magnitude (about 0.1), white is about 1, dark green is 10 and above. Colour tracks the magnitude of the printed number.

Empty and zero cells: grey cells are not zeros. The diagonal is grey by design (a metric against itself). The caption says only metrics carrying an exponent on the term are drawn, and the line under each panel names the others, so a zero or blank cell is not shown. No cell shows a literal zero; the smallest magnitude is -0.03 (total mass rising against unit cost, term 2). The off-diagonal grey cells in the grid are not explained by the caption, which is still unclear to me.

Steepest trades: on term 1, pointing error rising against depth of discharge giving way (-17), with peak slew power against depth of discharge close behind (-16). On term 2, unit cost rising against total mass giving way (-30). Correction: these magnitudes depend on each metric's conditioned scale, so they are not like-for-like rankings. The caption names the elasticity as the scale-free companion, which is the right basis for comparing trades; this figure alone cannot rank them.

Data or model: model output. The numbers are derivatives of the fitted surface at the balanced point, not observations.

"Unit": the caption makes it one unit of the row metric's conditioned value, not a unit of measure. "Unit cost" stays a metric name (cost per unit built) and is not a unit of measure.

Cold-read issues: the figure depends on the caption for what rows, columns, colour and derivatives mean; the colour bar labels only three ticks (0.1, 1, 10); the off-diagonal grey cells in the grid are unexplained in the figure.

# Reader 2 (Haiku, image: images/after-compact.png), verbatim

PART 1 (image alone)

The figure shows, for each of the two terms of the K = 2 fit, an 8 by 8 grid of signed sensitivities between metrics. The figure's own title defines a cell as the change in the column metric per unit rise of the row metric, and the grid is labelled "size of the tension (log scale)" on its colour bar. I take from it that the two terms couple the metrics unevenly: most of the strong coupling runs into "depth of discharge" and "pointing error" or "peak slew power" in term 1, and into "unit cost" and "available power" in term 2.

- Empty (grey) cell: the grey cells sit on the diagonal, where the row and column are the same metric, and they are the only empty cells I can see.
- Cell with 0: there are no cells showing 0 in either panel.
- Coloured cell with a number: a value in conditioned units, colour set by its size on a log scale (white near 1, brown small around 0.1, dark green large, about 10 and up).

The steepest trade on term 1 is between pointing error (row) and depth of discharge (column), at -17. Peak slew power into depth of discharge (-16) is close behind. The reverse cell (depth of discharge into pointing error) is -0.06, so the trade is strongly one-directional in this reading.

PART 2 (caption)

The caption changed my reading in two ways.
- It says "empty" means the column metric carries no exponent on this term. That does not fit what I see: the grey cells are all on the diagonal, and every metric on the diagonal, such as unit cost or pointing error, does carry an exponent. So the grey cells are self-pairs, and the caption's definition of "empty" does not account for them. I should flag this to the authors rather than assume.
- It says "0" means the row metric carries no exponent. No cell in either panel shows 0, so I cannot check that rule against the figure. The bottom notes list the five metrics not shown per term, which is a separate exclusion the caption does not mention.

I take the numbers as the model, not as data. The caption says they are computed at each term's balanced point, in conditioned metrics, so they are derived from the fit and from the conditioning choice. They are not measurements.

I understand "unit" as a one-unit step in the conditioned metric's own scale. I am not sure whether that means a step in the value or a step in its logarithm, and the caption does not say. That matters: a value of -17 is only large if the step is in the value and the conditioned scales are comparable across metrics. Until the scale is stated, the ranking of trades depends on the conditioning choice, and it is local to the balanced point.

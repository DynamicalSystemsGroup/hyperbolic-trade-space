# Reader 1 (Haiku, image: images/after-replace.png), verbatim

Note first: the caption was already in the request when I opened the image, so I could not form Part 1 without seeing it. I have kept Part 1 to what is visible in the figure.

PART 1 (image alone)

The figure shows, for each of the two terms of the K = 2 fit, a grid of pairwise trade numbers among the 13 metrics. Rows are the metric that rises (i), columns are the metric that gives way (j). Each filled cell is a signed number with a colour on a log scale of its size, so it reads as how strongly the column metric moves against the row metric on that term. I take it that the fit's exponents, not raw measurements, drive these numbers.

- Empty (grey or blank) cell: the column metric carries no exponent on this term, so it is not read as giving way. The grey diagonal is the metric against itself.
- Cell showing 0: the row metric carries no exponent on this term, so raising it moves nothing along the term.
- Coloured cell with a number: the size of the trade. Brown is small (about 0.03), white is about 1, teal is large (about 17).

Steepest trade on term 1: pointing error rising against depth of discharge, at -17. The next steepest is peak slew power against depth of discharge, at -16. Depth of discharge is the metric that gives way in both of the largest cells.

PART 2 (caption)

The caption did change my reading in one respect. Before it, I had read the empty cells as "no trade", which is wrong: an empty column means the metric is not read as giving way, and a 0 row means the row metric does nothing on this term. The caption also tells me that the numbers are local, taken at each term's balanced point, and that the metrics are the conditioned ones, not physical units. It also says every drawn cell is negative, so the sign carries no information and only the magnitude is shown by the colour.

I take the numbers as model output, not data. They are properties of the fitted posynomial term at one point, so they are only as good as the fit. Keep the fit and the analysis apart when writing about them.

On "unit": I understand it only partly. I read "one unit rise of the row metric" as a rise of one unit in the log of the conditioned metric, so each number is a ratio of exponents with a sign, which is dimensionless. I am not certain of this. The caption does not say whether the unit is in log space or in the raw conditioned value, and the derivation should be checked before anyone quotes a number with a unit.

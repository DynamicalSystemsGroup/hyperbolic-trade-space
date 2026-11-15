# Reader 1 (Haiku, image: images/fig-tension-matrix.png), verbatim

PART 1 (image alone)

The figure shows, for two terms of the fitted model, how strongly each metric pulls against another: when the row metric rises, the column metric gives way by a size shown as a tension. What I take from it is that depth of discharge is the metric that gives way most often and most steeply in term 1, while pointing error and peak slew power are the two that push hardest.

A coloured cell is a tension, with its colour showing the size of that tension on a log scale. White is 1, green is above 1 (up to about 10 and beyond), and brown is below 1 (down to about 0.1). Each cell also carries a signed number labelled as an exponent. The figure has a conflict I could not resolve: every printed number is negative, yet the darkest green cells carry the most negative numbers (-16, -17) and the palest brown cells carry the least negative ones (-0.06). So the colour and the printed number do not run the same way, and the caption does not say which one to read as the magnitude.

No cell reads zero. The smallest printed magnitude is -0.03 (term 2, total mass row against unit cost column). The grey cells are not zeros: on term 1 they sit on the diagonal (each metric against itself), and the caption explains only the omitted columns (total mass, control effort, power margin, energy balance, battery peak power ratio), which are left out because they carry no exponent on this term. The diagonal grey is not explained anywhere on the page.

On term 1, the two metrics that trade most steeply are pointing error (row) against depth of discharge (column), at -17, followed closely by peak slew power against depth of discharge, at -16. The matrix is not symmetric, so the direction matters: the row metric is the one that rises and the column metric is the one that gives way.

I take the numbers as model output, not data. They are exponents, weights (w=) and tensions derived from a fit, and the figure draws no raw observations; the page gives no source for the fit, so I cannot check them from here.

I read "unit" only in the metric name "unit cost". The figure does not define it. My reading is cost per unit built (per spacecraft), not a unit of measure, but that is an inference from the name, not something the figure states.

PART 2 (caption)

Report on fig-tension-matrix.png (the two-panel tension matrix for term 1 and term 2 of the fit).

What it shows and what I take from it: for each term, the matrix gives how strongly the row metric's rise pulls the column metric, with depth of discharge the column that gives way most. Pointing error and peak slew power push hardest on term 1.

What a coloured cell means: colour is the size of the tension on a log scale, with white at 1, green above 1 and brown below 1. The printed number is the signed derivative of the column metric with respect to the row metric. Every drawn number is negative, so the colour, not the sign, carries the size. The caption, which arrived after my first report, confirms this, so the conflict I first flagged (negative numbers with both dark green and dark brown cells) is not a real conflict: -0.06 is a small magnitude (brown) and -16 is a large one (green).

Empty and zero cells: no cell reads zero; the smallest magnitude is -0.03 (term 2, total mass row against unit cost column). Grey cells are the diagonal (a metric against itself), and blank cells are metrics without an exponent on that term, which the line under each panel names. The caption confirms the diagonal reading.

Steepest trades on term 1: pointing error (row) against depth of discharge (column), -17, then peak slew power against depth of discharge, -16. The matrix is not symmetric, so the row is the metric that rises and the column is the one that gives way.

Data or model output: model output. The caption says these are derivatives of the fitted K = 2 surface at each term's balanced point, so they are not raw observations.

What unit means: the caption defines the unit as one unit of the row metric's conditioned value, a unit of measure, not cost per unit built. "Unit cost" remains a metric name the caption does not explain.

Still unclear: the magnitudes depend on each conditioned metric's scale at the balanced point, so -17 and -16 are not directly comparable across pairs with different scales. The elasticity, named as the scale-free companion, is not drawn, so I cannot use it from this figure.

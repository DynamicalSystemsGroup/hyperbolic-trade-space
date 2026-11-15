# WP42 build, cold read of Figure 7 (figure loop, test 1)

Two fresh Haiku readers, the image alone (`images/fig-tension-matrix.png`, drawn by `case.tension_matrix_figure` on the
K = 2 fit of the primary regime), then the final caption of `paper/paper.ipynb` (cell `fig-tension-matrix-caption`),
sent to the same reader. Reports verbatim apart from the heading lines.

Findings for the record. Both readers take the numbers as model output (the caption confirms it) and name the steepest
trade on term 1 as pointing error against depth of discharge (-17), then peak slew power against it (-16). Both read
"unit" only as part of "unit cost" from the image; after the caption it is one unit of the row metric's conditioned
value. Reader 1 first took the colour and the negative numbers for a conflict (dark green carries the most negative
numbers); the caption's "every drawn cell is negative" and the colour bar resolved it. Reader 2 reports unexplained
off-diagonal grey cells: the figure has none (grey is the diagonal only), a misreading. Both note that the magnitudes
are not like-for-like across pairs, which the caption says (the elasticity is the scale-free companion). No zero or
blank cell is drawn, as the caption states. Disposition: kept as built; the intent (how steeply one metric gives way
to another on each term, at the balanced point) is read.

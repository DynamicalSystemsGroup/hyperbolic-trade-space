# docsfig-first-fit

## Q5

(a) A scatter of a few hundred blue points in log-log axes, log m0 across and log m1 up. Most points sit in a cloud between about -3 and +2 on both axes, with a thin tail running down-left to one outlier near (-9, -9). A straight black line with negative slope, labelled "frontier V = 1", runs from about (-2.3, 3) to (3.3, -1.7) along the upper-right edge of the cloud. A grey strip labelled "band (log V >= -0.5)" lies just below and parallel to the line. A handful of points sit on or slightly above the line; most sit below the band. There is no title; the axes have no units; the line's slope is not stated.

(b) Mostly yes. The line is the frontier, the designs fall below it with a few just beyond it, and a grey band sits under the line. What it does not show:

- "the grey band holds those nearest to it": the band is drawn, but the designs inside it are not marked in any way, so the reader cannot tell which designs the band "holds" except by eye, and the band reads as a region, not as a set of designs.
- The band's width (0.5 in log V) is in the legend only as "log V >= -0.5"; how that maps to distance in this plane (it depends on the exponents) is not shown, so the strip's thinness cannot be checked against the 1/tau sentence on the page.
- "The first fit" is not quite what is drawn: the page's first fit is on three metrics (a trilemma), and the code under the figure refits on metrics 0 and 1 alone (`ts2`). The caption's "the first fit seen on two metrics" reads as a view of the three-metric fit; it is a second, two-metric fit.
- The fitted exponents (the line's slope, the elasticity between m0 and m1) are not shown or labelled.

(c) Sentence: "Fitted on two metrics, the frontier is a straight line in the log plane; the designs fall on or below it, a few just beyond, and the band of width 0.5 in log V under the line holds the designs nearest the frontier." The figure conveys a little more than that sentence: that the line sits on the upper-right edge of the cloud (it is a frontier, not a regression line through the middle), that only a handful of designs are beyond it, and how thin the band is relative to the spread of the data. It also shows, unremarked, a long tail toward the origin and one far outlier near (-9, -9) that stretches the axes and leaves the cloud in the upper-right third of the plot.

## Q1

On two metrics the fitted frontier is a straight line in the log plane along the outer edge of the designs, with a thin band of near-frontier designs just under it.

## Q2

Home page: "where each design sits relative to the fitted reference surface" (and, for the page, "Getting started: install from source and run a first fit").

## Q3

advances. The Home page promises that the package tells you where each design sits relative to the fitted reference surface, and this is the first and only place in the getting-started path where a user sees that picture for their first fit: a frontier on the edge of the data, not through it. Other figures (the root page's, and the log-plane figure in the user guide's Chart page, which I have not read) may carry a similar picture, but none of them sits on the page where a new user runs the first fit and needs to see what "frontier" means for that fit.

## Q4

Not "repeats". (If a later reviewer finds the Chart page's figure, unit docsfig-log-plane, draws the same two-metric log plane with band, this one would become a candidate for "repeats" of it; from what I was given I cannot say.)

## Q8

- Home page ("where each design sits relative to the fitted reference surface"): helps; the reader sees designs below, on and beyond the line. It does not say how far any one design is (no score is shown).
- Root page ("learn the shape of a trade space from evaluated designs"): helps modestly; on two metrics the "shape" is just a line, so it shows the frontier idea but not a trade space with several terms or tensions.
- Page opening ("install from source and run a first fit"): helps; it lets the reader check that their first fit produced a frontier on the edge of the data. It does not connect to the printed output (trilemma, exponents 0.3, 0.37, 0.33), since it is a separate two-metric fit.

## Q9

- Page text before the figure: "the designs lie on or just beyond a straight frontier". The figure shows most designs well below the line, and the caption says "fall below it or just beyond it"; the page sentence and the caption disagree, and the page sentence disagrees with the image.
- "the grey strip under the line is the region up to 0.5 below the frontier in log V" vs the legend "band (log V >= -0.5)" vs "the band of near-frontier designs has width 1/tau": with tau = 20, 1/tau is 0.05, not 0.5. I could not place whether the drawn band (0.5) is the same band the 1/tau sentence names, or a wider display band.
- "the first fit seen on two metrics" (caption) vs `ts2 = HyperbolicTradeSpace(temperature=20.0).fit(X2)` (code): is the figure a view of the three-metric fit or a new fit? The code says new fit; the caption reads as the same one.
- The outlier near (-9, -9) and the tail of designs toward it: nothing on the page says what they are.

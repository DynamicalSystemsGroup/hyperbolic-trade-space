# docsfig-three-terms

## Q5

(a) A scatter of a few hundred blue points on log m0 (x, about -8 to 0.5) against log m1 (y, about -7 to 1). A black line, labelled "frontier V = 1 (envelope)", runs as a gently falling straight piece from about (-8, 2) to about (0, 0), then bends sharply and drops steeply to about (0.4, -3.7). The points sit below and to the left of this line, packed densely along it near the corner and thinning out down and to the left. The legend also lists a grey "band (log V >= -0.02)", but I cannot see any grey band drawn on the plot; if it exists it is too thin to see under the points and line. I see two straight pieces in the black line, not more.

(b) Partly. The image shows designs in the log plane of two metrics, one colour, and a bent black frontier, as the caption and alt text say. It does not show three terms: I can see only two straight pieces in the black line, so if there are three, two of them are nearly collinear or one is too short to see. It does not draw the term lines themselves, only the envelope, so "each term is a straight line" is something I have to infer from the straight pieces of the envelope rather than see. The grey band named in the legend and in the alt text ("a grey band below it") is not visible at all. Nothing marks which designs belong to which term, or where one term hands over to the next.

(c) Sentence: "With several terms the frontier in the log plane of two metrics is a bent line made of straight pieces, one per term, with the designs lying below it." The figure conveys a little more than that sentence: that the pieces can have very different slopes (a shallow trade on one side, a steep one on the other), so the rate at which m1 is given up for m0 changes sharply at the corner; and that the designs crowd against the corner and along the frontier. It does not convey the count of three or the band.

## Q1

With several terms, the fitted frontier of two metrics is a bent line in log space, straight within each term's region, with the designs lying below it.

## Q2

The Home page: "a sum of monomial terms, where a monomial term ... is one trade-off." On its own page it serves the sentence "One term is flat in log space, with constant elasticities. When the rates vary by region, fit n_terms=K terms".

## Q3

advances. It is the only picture on the Fitting page, and the only one I was given in the docs, of what several terms do to the frontier: the bend, where the trade-off rate changes from region to region, which is the reason the page gives for choosing K > 1, and it is the output of the plot_log_plane call printed just above it. It advances weakly, because it does not show what its caption and alt text promise: I count two pieces, not three; the term lines are not drawn separately; and the band in the legend and alt text cannot be seen.

## Q4

Not "repeats". The nearest candidate is the root page's second figure (unit root-index-fig-figure1), whose caption speaks of "the three terms of the fitted reference surface" as coloured pieces, but that is on the root page and seen three ways, not the output of this page's plotting call; I did not read it, so I do not claim it carries this.

## Q8

- Home page ("fits a frontier model ... a sum of monomial terms, where a monomial term ... is one trade-off"): yes, partly; it shows terms as straight pieces of one frontier, but a reader cannot count the terms or tell which designs each covers.
- Root page ("learn the shape of a trade space from evaluated designs"): yes; it shows a learned frontier shape over evaluated designs, with a bend the one-term model could not draw.
- Page opening ("HyperbolicTradeSpace fits the frontier model to conditioned metrics"): yes; it shows what a fit with n_terms=3 looks like and what plot_log_plane returns, so a user can check their own plot against it, but the missing band and the two-versus-three count would confuse that check.

## Q9

- "band (log V >= -0.02)" in the legend, and "a grey band below it" in the alt text: no band is visible on the image.
- "Three terms" in the caption: I could find only two straight pieces in the frontier line.
- "frontier V = 1 (envelope)": whether this is the envelope of the three term lines or the fitted reference surface (the page distinguishes the supporting envelope at infinite tau from the fitted surface at finite tau, and this fit uses temperature=50.0).

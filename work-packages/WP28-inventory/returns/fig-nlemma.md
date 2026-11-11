# fig-nlemma

## Q5

### (a) What the image shows (written before the caption)

A triangle (a 2-simplex) whose corners are metric 1, metric 2 and metric 3; a corner is labelled "it binds alone", each edge is labelled a "dilemma" of the two metrics at its ends, and the interior is labelled "trilemma". Three coloured numbered dots are placed in it, one per "term", each with its exponent vector w listed at the right: term 1, w = (0.00, 0.35, 0.65), sits on the bottom edge (dilemma of 2 and 3); term 2, w = (0.44, 0.27, 0.28), sits in the interior (trilemma); term 3, w = (0.70, 0.30, 0.00), sits on the left edge (dilemma of 1 and 2). Open black circles mark "planted (the known answer)" positions; terms 1 and 3 sit inside their circles, while term 2's dot is a little below and to the right of its circle, so its recovered position differs slightly from the planted one. A note says the weight on these three metrics is 1.00 each ("all of it: d = 3"). So: each term's exponent vector, normalized to sum to one, is a point on the simplex, and where it lands (corner, edge, interior) names which metrics trade off in that term; the fitted vectors are compared against planted ones.

### (b) After the caption: does the image show what the caption says?

Yes, for the most part. The caption says each term's exponent vector at the fit temperature is a point of the triangle, drawn beside the planted one (open ring), and that the face holding the point names the n-lemma (corner, edge, interior). The image does that: two terms on edges (dilemmas), one in the interior (a trilemma), each beside its ring, and the faces are labelled on the drawing itself. The "weight the three carry is printed (here all of it)" is there too, though the image prints it as three numbers ("1.00, 1.00, 1.00") where the caption suggests one; I could not tell whether those are one value per term or per metric.

What it does not show: no corner case is populated, so "one metric binds alone" is labelled but never illustrated; it does not show the designs, their levels, the surface, or the term cells that Definition 6 fits; it does not show how far term 2's dot sits from its ring in any stated unit, nor whether that gap counts as recovery; and it does not show the elasticities, although the exponents printed at the right let a reader compute them (Definition 8). It also does not show the exact-maximum fit that Definition 6 says decides the contending set; the dots are the fit-temperature exponents, so the face is read from a different fit than the one the definition names (they agree here because the zeros are printed as 0.00).

### (c) The sentence test

Sentence: "Normalized to sum to one, a term's exponent vector is a point of the simplex over the metrics; the face it lies in (a corner, an edge, the interior) is the set of metrics with non-zero exponent, and its size names the n-lemma (one metric, a dilemma, a trilemma); in a synthetic three-metric table with three planted terms, the fit puts one term on each of two edges and one in the interior, at or next to the planted vectors."

The figure conveys a little more than that sentence: it gives a geometric picture of the n-lemma (support of w equals the face of the simplex) that a reader can take with them to the larger cases, and it shows at a glance how close the recovered vectors are to the planted ones (two on the ring, one slightly off). The exact numbers are printed beside it, so the sentence plus a three-row table would carry nearly all of it; the drawing's gain is the face-to-n-lemma reading by eye.

## Q1

The figure shows that a term's exponent vector is a point of the simplex whose face (corner, edge, interior) names the term's n-lemma, and that on a synthetic three-metric table the fit recovers three planted terms (two dilemmas and a trilemma) at or near their planted points.

## Q2

The abstract sentence "Each monomial term ... reports its contending metrics, an n-lemma (by analogy with dilemma and trilemma)", repeated in Section 1 ("Each monomial term ... names the metrics that contend on it ... an n-lemma"). Of the numbered main results it bears most on item 7 (the terms separate contending sets), though it shows a synthetic table and not the cubesat.

## Q3

advances. The abstract and Section 1 rest on the word n-lemma, coined by analogy, and Definition 6 defines it only as the support of an exact-maximum fit to a cell; this figure is the one place in the paper (by the units list) that makes the analogy concrete, showing dilemma and trilemma as the edge and interior of a simplex, with a recovery check against planted terms. No other unit in the paper is named as carrying that picture; its value is limited by the unpopulated corner and the unexplained gap of term 2 from its ring.

## Q4

Not applicable (verdict is not "repeats"). The units list has a docs figure, "Figure 8 on 'Examples'" (unit docsfig-ternary-planted), whose name suggests the same ternary-with-planted-terms picture; I have not read it, and it sits in the documentation, not the paper, so it does not change the verdict within the paper.

## Q9

- "Weight on these three metrics: 1.00, 1.00, 1.00 (all of it: d = 3)" against the caption's "the weight the three carry is printed": one weight is described, three are printed; I could not place what each 1.00 refers to.
- "drawn beside the planted one (open ring)" with term 2 sitting off its ring: neither the caption nor the text says whether that gap is a recovery error, an effect of the fit temperature, or within tolerance.
- "its exponent vector at the fit temperature is a point of the triangle" against Definition 6, where "the contending set ... is the support ... of the exact-maximum ($\tau=\infty$) fit to the term's cell": which fit's vector the dot is, and why the face read off it names the n-lemma, I could not reconcile on two readings.
- "(corner: it binds alone)": what a one-metric "n-lemma" means as a tension is not said, and the figure has no term there.

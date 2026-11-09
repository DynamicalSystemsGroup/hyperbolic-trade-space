# Reader P5-A (optimization reader), slice A

1. What this is about.
Trade-study analysis. A posynomial surface is fitted to attribute data (not to the Pareto boundary). It is meant as a PCA-like coordinate system that explains trade-offs, not variance.

2. The main result, as I understood it.
Fit a posynomial reference surface to the data. A reversible chart splits each design into a position along the surface and an "energy differential" (its level relative to the surface). Each facet gives an "n-lemma" of contending metrics with elasticities (percent given up per percent gained). A single n-lemma is a monomial, which is a convex program after a log transform. Several active trade-offs give a posynomial, which is GGP-compatible. A cubesat example identifies trade-offs among power, mass and attitude control.

3. Next steps.
Check the fit formulation and see what the "convex program" is. Look at how the elasticities come out of the exponents.

4. One sentence for a colleague.
It is a PCA-shaped, log-linear (monomial/posynomial) fit of trade-off surfaces that reports elasticities between metrics.

5. What the method does NOT do.
It does not find the Pareto boundary or optimize designs. It does not explain variance. As far as I can tell, it does not condition the data.

6. Confusion or stopping points, and claims to check.
"models the data underlying the table, not the Pareto boundary" - if the surface is fitted through the data, what loss and what constraint? A reference surface that is not a frontier is unclear.
"A reversible chart" - reversible in what sense?
"transforms into a convex program and is solved directly" - which convex program? Exact or approximate?
"the fit identifies the trade-offs" - no quantitative result is given.

7. Terms I had to guess.
"Energy differential" (I take it as a residual in log space). "Facet". "n-lemma". "Kernel that keeps that compatibility". "Mirrors the structure of PCA".

8. Read on?
Yes, because the monomial-to-convex claim and the GGP link are checkable. I would go straight to the formulation.

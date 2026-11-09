## 1. What this is about
A method for trade studies. It fits a smooth "reference surface" through a table of design outcomes, uses it as a coordinate system, and reports trade-offs as elasticities between metrics. It is pitched as a PCA-like tool, but for tensions rather than variance.

## 2. The main result, as I understood it
Fitting a posynomial (monomial for a single trade-off) to the data gives a reversible chart. One coordinate is position along the surface, the other is level relative to it ("energy differential"). Each facet names its contending metrics and gives percentage-for-percentage exchange rates. A cubesat example recovers the trade-offs among power, mass and attitude control.

## 3. What I would do next
Run it on a dataset where I already know the Pareto set, and check whether the surface and its elasticities match the known front's marginal rates of substitution.

## 4. One sentence for a colleague
It is a regression-fitted log-linear surface through the data, with tangent elasticities read off as trade-off rates, packaged like PCA.

## 5. What it does NOT do, and what it adds
It explicitly does not model the Pareto boundary, so it is not an efficient-frontier method. It does not say which designs are dominated or optimal. Against Pareto analysis, the possible additions are a continuous coordinate system, elasticities for any facet, and convexity via GGP. Against my toolkit that is plausible but unproven here.

## 6. Where I was confused
"models the data underlying the table, not the Pareto boundary". It is unclear how a central-tendency surface yields trade-offs rather than correlations. "energy differential" is undefined.

## 7. Terms guessed
"n-lemma", "facet", "energy differential", "kernel that keeps that compatibility".

## 8. Read on?
Yes, to see how a mean surface differs from a frontier and whether elasticities are causal trade-offs or just covariation.

## 1. What this is about
A way to analyse a trade study table of evaluated designs. It fits a smooth reference surface (a posynomial) to the data, not to the Pareto boundary. Designs then get coordinates: where they sit along the surface, and how far above or below it. It is offered as a replacement for PCA, because it explains trade-offs rather than variance.

## 2. The main result, as I understood it
Each facet of the surface reports an "n-lemma", a set of metrics in tension, with elasticities. Elasticity here means the percent of one metric given up per percent gained in another. A single trade-off fits a monomial, which is solved as a convex program. Several simultaneous trade-offs need a posynomial, which fits GGP. A cubesat example is said to identify the trade-offs.

## 3. What I would do next
Check whether my table of evaluated designs has strictly positive, larger-is-better columns. Then I would look for an implementation and try it on my power and mass data.

## 4. One sentence to a colleague
It is a PCA-like tool that fits a surface to your design table and reports the trade-off rates between metrics.

## 5. What it does NOT do
It does not find the Pareto front, and it does not pick a design. I could not tell whether it talks to my SysML model, or only to the table.

## 6. Confusion
"gives the data a coordinate system; the table and its reading are views". "energy differential, its level relative to the surface". "A reversible chart".

## 7. Guessed terms
Posynomial, kernel, facet, "energy differential", and GGP, which I took to mean generalized geometric programming.

## 8. Read on?
Yes, cautiously. Trade-off elasticities from my own data would be useful. But the abstract does not say what inputs are required, such as how many designs or whether the data must be positive. It also does not say how it handles my model's outputs.

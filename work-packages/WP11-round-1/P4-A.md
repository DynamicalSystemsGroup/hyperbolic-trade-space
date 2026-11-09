# Reader P4, slice A

1. What this is about
A scikit-learn-style unsupervised method for trade studies. Like PCA it gives a coordinate system for a table of design metrics, but it aims to expose trade-offs rather than variance.

2. The main result, as I understood it
Fit a posynomial surface to the data (not to the Pareto boundary). It splits each design into a position along the surface and a level relative to it. Each facet names the metrics in tension, with elasticities (percent of one metric lost per percent gained in another). A cubesat example identifies the trade-offs.

3. What I would do next
Look for the package and try it on one of my multi-objective tables, as a step in a pipeline next to PCA.

4. One sentence for a colleague
It is PCA-like feature engineering that tells you which metrics trade off, and at what exchange rate, instead of which directions vary most.

5. What it does NOT do
It does not find the Pareto front, pick a design, or predict anything. It seems to need strictly positive, larger-is-better metrics, though the abstract does not say so.

6. Confusion
"the data underlying the table, not the Pareto boundary" is unclear. "separates a design's position along the surface from its energy differential" is also unclear. "Modelling a single n-lemma fits a monomial, which transforms into a convex program" lost me.

7. Terms I guessed at
"Energy differential" (I guessed a residual from the surface). "Facet" (a face of the fitted surface). "Posynomial", "GGP" and "kernel" (I know the words only loosely). "Reversible chart" (an invertible transform?).

8. Read on?
Yes. The PCA analogy and the elasticity outputs fit my workflow. I would want to see the API, the input conditioning, and a comparison with PCA or ICA on the same data.

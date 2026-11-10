# Three passages from a paper on trade-off analysis (version B)

Read cold. Nothing else is available.

## Passage 1 (the end of the abstract)

Each monomial term, one trade-off, reports its contending metrics, an n-lemma (by analogy with dilemma and trilemma), with elasticities: the percentage of one metric given up per percentage gained in another. Modelling a single n-lemma fits a monomial, which transforms into a convex program and is solved directly; when several trade-offs are active at once the model is a posynomial, compatible with generalized geometric programming (GGP); any kernel that keeps that compatibility generalizes the method. Like PCA, our method is unsupervised feature engineering; the two answer different questions and compose, as when PCA is run on the chart. On a cubesat model coupling power, mass and attitude control, one monomial term blends the subsystems' trade-offs into a single tension; three terms separate the contending sets.

## Passage 2 (two definitions)

- Definition 6 (The n-lemma): The contending set of term k is the support (exponents above 10⁻⁹) of the exact-maximum (τ=∞) fit to the term's cell, the designs whose largest term it is; its size n_k names it. It is found, not assumed. Working-temperature exponents grade the members, and a member can carry a small one.
- Definition 7 (Reach and share): The reach β_k is the support value of the data in direction w_k: how far the data extend that way, their largest score along it. The term share is the fraction of near-frontier designs in the cell of term k; it shows which trade-offs carry most of the frontier and depends on the band.

## Passage 3 (the main results)

Main results (each has hypotheses, a sketch and a script).

1. The fitted reference surface is where the invariant value, a weighted geometric mean of the metrics that doubles when every metric doubles, equals one; it is not the Pareto boundary but the level from which every design's position and level, and each term's elasticities, are read (Theorem 1).
2. The one-term fit is a geometric program, convex in the logarithmic variables (Theorems 2, 3); its exponents are elasticities and its chart is reversible (Theorems 5, 6).
3. With one term the posynomial extension is the monomial, and a maximizer of V is Pareto-efficient (Theorems 8, 9).
4. The posynomial fit, not convex in the terms, has three levels of guarantee and a stopping declaration (Theorems 10, 11, Lemmas 1, 2, Proposition 3); a soft fit has a second-order certificate (Theorem 12).
5. PCA and the fit are chained: the principal directions of the near-frontier chart read the trade-offs the sampling exercised, a reading and not a result (Appendix D.16).
6. Numerical: the status a fit reaches. Open: Q1 to Q4 and the search's monotonicity.
7. On a cubesat model coupling power, mass and attitude control three monomial terms separate contending sets that one term blends (Section 9).

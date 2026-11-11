# sect-methods

## Q1
It states how the one-term fit is posed (an entropic soft maximum minimized over weights, with a target fraction of designs above the surface), what the analyst must do to the data first (log-affine conditioning), what the estimator's interface is, and which simplifying assumptions the method makes.

## Q2
Main-results items 2 and 3 (the one-term fit is a geometric program; the chart is reversible) and, in the abstract, "Modelling a single n-lemma fits a monomial, which transforms into a convex program", plus "fitted to the outer edge of the data, not through its middle: a soft support". It also serves the abstract's "Like PCA, our method is unsupervised feature engineering" only loosely, through the estimator paragraph.

## Q3
Verdict: advances. The story says the surface is fitted to the outer edge, not the middle, and that the fit is convex; the section is the only place that gives the actual objective (the log-mean-exp, the target fraction tau, the weights on a simplex) and the conditioning the theory requires. The estimator paragraph and the list of assumptions are the reader's only statement of what is being fitted and what is assumed, though several parts are compressed enough that a first reader must take them on trust.

## Q4
Not applicable. Parts overlap with the theorem statements in Section 6 and Appendix B (convexity, exactness of the pull-back), but the section only points to them and does not repeat them.

## Q6
none

## Q9
- "R1: the balanced point ... lies in the relative interior of a facet of the supporting envelope with positive normal": I could not place facet, supporting envelope or subgradient choice at this point; they are used before they are defined.
- "R2: the assignment margin gamma": I could not say where it is used in this section or why it is needed.
- "never the unnormalized log-sum-exp ... (Theorem 4)": the claim reads clearly, but the reader is sent to a theorem not seen here.
- "membership: Definition 6" and the thresholds "10^-3" and "10^-12": I could not say what participation is used for.
- "(Theorem 8)" cited for the kappa bound, while the story's item 3 cites Theorem 8 for the monomial extension: I could not tell whether these are the same statement.
- "$V_K$ is a generalized posynomial, the term maximum at the default kappa = infinity": kappa is not introduced in the section.

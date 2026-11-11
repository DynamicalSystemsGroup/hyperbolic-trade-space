# sect-prior-art

## Q1. What the section conveys

It places the method among eleven nearby families (Pareto methods, data envelopment analysis, production and distance functions, frontier estimation, PCA and its compositional and kernel variants, geometric programming, MDAO, tradespace exploration, decision analysis, MBSE). For each it says what is borrowed and what is different. Its claim is that the combination in one estimator, not any single piece, is new.

## Q2. Which story sentence it serves

Section 1, paragraph 2: "the computational alternatives are bespoke and opaque", and the abstract and Section 1 sentence "Like PCA, our method is unsupervised feature engineering; the two answer different questions". It also touches main-results item 3 (Theorem 9) through the Pareto paragraph. No numbered main result is about prior art.

## Q3. Verdict

advances.

Section 1 says the existing alternatives fall short and that the method differs from PCA. A first-time reader then needs to know, in the body of the paper, how the method differs from the obvious near neighbours: a nondominated set, DEA, frontier estimation and fitting with geometric programming. This section is the only place in the body that does that, and it ends on the novelty claim the contribution rests on. Appendix G is named as the larger register, so the section's job is the summary and it does not duplicate the register. Inside the section the prose largely repeats Table 1 row by row, especially the "Lineage" paragraph. The Pareto paragraph also repeats the dominance count from Section 1 and Theorem 9 from item 3. The table and the prose could be shortened to one or the other.

## Q4. If "repeats"

Not applicable. Partial overlap: Table 1 (unit tab-families) inside the section carries most of what the paragraphs carry, and Appendix G (unit appendix-g) is the full register.

## Q6. Boxed statements

none

## Q9. Read twice and still could not place

- "a band, not extreme units" (Table 1, DEA row) and "a band of near-frontier designs and an effective sample size": the band and the effective sample size are not defined in the story or before this point.
- "A smooth soft maximum over a simplex-constrained geometric mean": which simplex. The story does not say the exponents lie on a simplex.
- "We solve one convex program and K refits, and return coordinates with a pull-back to attribute units": what a refit and a "pull-back" are.
- "the soft maximum is an entropic risk functional Föllmer, n.d.": an undated citation, and the link to the soft maximum is asserted without explanation.
- The Pareto row's "Shares" cell, "A maximizer of a weighted geometric mean with positive exponents is Pareto-efficient": this is the paper's own Theorem 9, so it is unclear what Pareto methods share here.
- "Open. Which part of the Pareto boundary the terms reach is our reading": an "Open." label inside a prior-art paragraph. Is this one of Q1 to Q4 from item 6 or something else?
- "Attributes in place of inputs" (production-function row) against "Our metrics are larger-is-better ... in place of inputs, outputs": attributes or metrics?
- "the feature-engineering kin of the direction in Section 10": which direction (the kernel extension?).
- "the hyperbolic graph measure of efficiency of Färe, Grosskopf and Lovell": useful as a disambiguation, but the source is not in Table 1.

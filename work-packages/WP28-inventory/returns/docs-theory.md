# docs-theory

## Q1. What the page conveys

It states the model in definitions: a weighted geometric mean V of the metrics (one term, K terms as a posynomial), the surface V = 1 as the fitted reference surface (kept apart from the supporting envelope and the Pareto boundary), the chart coordinates (Z, log V), the constant elasticities and the n-lemma, and the model's assumptions.

## Q2. The story sentence it serves

Home page: "Theory in brief: the model on one page." Also the root page's Documentation card, "the model in brief", and the Home page's "it fits a frontier model in the posynomial invariant form ... which metrics contend, with what elasticity".

## Q3. Verdict

advances. The Home page promises one page that states the model, and this is that page: it defines V, the fitted reference surface, the chart, the elasticity formula and the n-lemma in one place, which the task pages of the user guide lean on. No other unit in the documentation is named as carrying the model on one page; the paper's Definitions section carries it for paper readers, but the docs story names this page for the package user.

## Q4. Repeats

Not applicable. (Overlap to note: the paper's Section 4 Definitions, unit sect-definitions, and Appendix A, unit appendix-a, likely carry the same definitions for the paper; the "What the model assumes" section overlaps with the docs page 'User guide: Limitations', unit docs-user-guide-limitations, which it points to.)

## Q8. Judged three ways

- Against the Home page: it delivers "the model on one page", and it gives meaning to the Home page's words "contend", "elasticity", "fitted reference surface" and "gaps" (as holes in the Z plane). One mismatch: the Home page leads with "a sum of monomial terms", while this page leads with a single weighted geometric mean and reaches the sum only in passing.
- Against the root page: it defines the n-lemma that the root page calls the method's unit, and the chart and "energy differential" that the root page's second figure caption uses. It does not mention PCA or tensions as the root page frames them, which is fine for a model page.
- Against its own opening sentence ("states the model so the user guide reads without gaps ... definitions and no proofs"): mostly yes. But the first section also describes how the fit is solved (geometric program, alternating assignment and convex refit, term_temperature=np.inf, labels driving the refit), which is fitting procedure rather than model definition, and several terms used are not defined here (the fit temperature tau, the participation threshold), so gaps remain.

Paragraphs or sections serving none of the three:

- "Fitting one term is a geometric program (GP), solved as a convex program ..." through "... not part of the fit." (the solver and default-parameter detail in the first section; it belongs to the fitting task page, not to a statement of the model).
- "The argument itself lives in the project repository, in the derivation scripts ..." (a pointer to where proofs live; it serves the "no proofs" promise only as a signpost, and a reader of the docs cannot act on "will be in the paper when it is published" when the Home page says the project page already links the paper).

## Q9. Read twice, still could not place

- "The model is a root of that sum, so the surface V = 1 is where the posynomial equals one." (a root in what sense: the K-th root, a root-finding root? Not defined.)
- "at the fit temperature tau" (tau appears without definition; its relation to term_temperature, introduced a paragraph earlier, is not stated.)
- "set by a participation threshold" (no parameter or value given.)
- "designs are chosen by an evaluator and not drawn from the attainable set" (what this assumption means for the user is deferred entirely to another page.)
- "Holes in the Z plane are candidates for white space." ("white space" is not the Home page's word "gaps" and is not defined here.)

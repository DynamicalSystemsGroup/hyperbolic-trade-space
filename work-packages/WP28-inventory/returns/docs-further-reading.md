# docs-further-reading

## Q1
It lists twelve sources the method builds on, grouped by what a reader may want from each (using the package, geometric programming, charts and neighbouring methods), each with a one-line note on its role.

## Q2
Home page: "Further reading: the sources the method builds on." It is the last item under "Where to start". The root page has no sentence that needs it.

## Q3
Verdict: advances. The Home page promises a page of sources the method builds on, and only this page delivers it. The paper's Works cited and Appendix G (register of prior art) may hold overlapping references, but I have not read them. This page is the documentation's own short, role-annotated pointer list, and it is the only place a package user gets the pointers (for example, which paper is the source of the multi-term fit, or where penalty="reweighted_l1" comes from).

## Q4
Not applicable. Possible overlap with sect-cited or appendix-g, unverified.

## Q8
- Against the Home page: matches. The Home page names it as "the sources the method builds on", and that is what the page is.
- Against the root page: the root page only points to the docs generally ("a guide per task... a glossary"). It does not mention further reading, so the page neither serves nor contradicts it.
- Against its own opening sentence ("The sources the method builds on, by what you may want from each. This is a short list and not a survey."): the page does this. It groups by reader want and is short. Two entries are not sources the method builds on: HoroPCA ("which this package is not") and Kernel PCA ("not built"). They are neighbours to avoid confusion, so they sit slightly outside the opening sentence. Data envelopment analysis is likewise a neighbour, not a source.
- Sections serving none of the three: none. The numbered reference list at the end (starting "1. Fabian Pedregosa") is the bibliography the bullets point to.

## Q9
- The bare numbers after titles ("scikit-learn and its API design 12", "Convex Optimization 3", "Kernel PCA 10") read like page numbers or a count until I saw the numbered list below. They are footnote markers, and the "12" after the first entry looks like twelve, not references 1 and 2.
- "Enhancing sparsity by reweighted $\\ell \_1$ minimization" in reference 7: the raw LaTeX in the rendered text. Also "Reweighted $\ell_1$ minimization 7" in the bullet.
- "the sparsity option, penalty="reweighted_l1"": a parameter name with no explanation on this page. It is fine for a user of the package but arrives without context.
- "the family the multi-term fit stays inside" and "the second source of the multi-term fit": the multi-term fit is not defined here. Home says only "a sum of monomial terms".

# Confirmation: glossary-appendix-a

| Surface | Reader | Rendered view and head | Reads clean | Remaining flags (kind, sentence in full) | Cuts that lost something |
|---|---|---|---|---|---|
| `appendix/appendix-a` (paper/supporting_material.ipynb, Appendix A. Notation and terms) | glossary-appendix-a | http://127.0.0.1:8791/paper/supporting-material/, Appendix A section as rendered; head 003f1d2 (own tab tab-178) | no | 13 flags, listed below | none seen (the earlier text was not opened, so a loss shows only as a gap in the landed text; none found) |

Remaining flags (generated table read as rendered; the table is compiled from glossary.yaml, so source-level fixes go there):

1. Kind 1 (metanarration, template block): "This appendix carries: one table: term, symbol, meaning in this paper, what it is not, and where it is defined, compiled from glossary.yaml and never typed."
2. Kind 4 (repository internals in reader-facing prose): "The repository keeps: the register’s reasoning and its phrase lists."
3. Kind 4 (file name and decision-record pointer in the "Defined in" cell, MoE row): "cubesat_r2.sysml (the mark in the doc of the metric's element); WP23-review.md"
4. Kind 4 (same, MoP row): "cubesat_r2.sysml (the mark in the doc of the metric's element); WP23-review.md"
5. Kind 4 (same, launch cost row): "cubesat_r2.sysml (calc def LaunchCost, LaunchBudgetRequirement); WP23-decisions.md OD1, OD2"
6. Kind 10(b) (acronyms never expanded in this document): "MoE" and "MoP" (rows "a metric a stakeholder states on the system in use, independent of the design" and "a metric of the system's performance under a stated scenario"; neither says measure of effectiveness / performance).
7. Kind 10(a) (term of art undefined at first use): "the Helmert log-ratio coordinates of the chart" (position along the frontier row).
8. Kind 10(a): "the softness of the weights softmax_k(kappa score) over the K terms" (term temperature row; softmax and kappa score not explained here).
9. Kind 10(a) (symbol used with no definition): "minus the mean over the rows of Phi_K; returned as mean_slack_" (mean slack row; Phi_K is not defined in the table, only Φ(u)).
10. Kind 9 (grammatical complexity, geometric program "Not" cell): "the several-term fit as one program, which is not convex in the terms (L16). With the weights given, the fit of all terms is a generalized geometric program"
11. Kind 9 (generalized geometric program "Not" cell, several ideas joined by semicolons): "a function class, or the unsupervised several-term fit as one program (not convex in the terms); the older use of the phrase for signomial programs; a design problem that uses the fitted model is one"
12. Kind 9 (ternary plot meaning): "the barycentric image of the shares of three metrics. A term's exponent vector sums to one, so it is a point of the triangle, where that term's V is largest at a fixed total"
13. Kind 10 (reference codes with no key in the appendix; reads as a dangling reference at first use): the "Defined in" and "Not" cells' codes "L9", "A4", "G-1", "I1", "R2", "F12" and so on, first met in "A4" (attributes row), with no statement here of what the letters index.

Not flagged: the Job/Main text keeps/This appendix carries block as a repeated house form beyond item 1 and 2; generated math symbols in the Symbol column.

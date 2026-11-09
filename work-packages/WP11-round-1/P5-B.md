1. What this is about.
A method for trade studies. Strictly positive, larger-is-better metrics are fitted with a monomial or posynomial reference surface (V = 1) in log space. Each fitted facet gives exponents that act as elasticities, and a reversible chart splits "position along the surface" from "level relative to it" (log V). It is pitched as a PCA-like tool that explains trade-offs rather than variance.

2. The main results.
The surface is the unit level set of a weighted geometric mean, and it is not the Pareto boundary (Thm 1, Def 1). The one-facet fit is convex in the exponents (Thm 3, the Hessian is tau times a variance), with simplex KKT conditions (Thm 2). Elasticities are -w_i/w_j (Thm 5). The chart is an orthogonal bijection (Thm 6). A maximizer of V is Pareto-efficient (Thm 9). The several-facet fit is non-convex, so it gets three levels of guarantee: descent, a numerical facet gap, and conditional local optimality (Thm 10-11, Lemmas 1-2, Prop 3). A soft fit has a second-order certificate (Thm 12).

3. Claims and non-claims.
The statements are careful about what they do not claim: "Convergence and stationarity are not claimed", "tightness is not claimed", "the converse is not claimed". Hypotheses are labelled (A1, R2, I14 and so on), but I cannot see what they say. Possibly loose points: the abstract's "explain tensions", and "n-lemma" as vocabulary. "Balanced hard-support geometry does not imply an interior minimizer" is stated without detail. Prop 2 is "a population identity, with no consistency claim", so statistical properties of the fit appear to be unaddressed. The case study has no ground truth.

4. Next steps.
Read the proofs of Thm 3 and Thm 10-11. Check how tau is chosen. Try it on my own data.

5. One sentence.
Fit a convex log-space geometric-mean surface to positive metrics and read the exponents as trade-off elasticities, with honest guarantees for one facet and weaker ones for several.

6. Figures.
Figure 5 helped most. The correlation heatmaps show negative-association blocks, such as slew time against control effort at -0.99, with the contending set outlined. Figure 2 was clear: a scatter in log-log space with a straight line. Figure 4 helped least, with coloured blobs and no visible structure I could read. Figure 7 was hard to judge, because the predicted and measured points are close but there are only three and no scale of error.

7. Confusion.
"energy differential" is physics language for log V, and the paper itself says it is not an energy. In Figure 3 the lines do not obviously track the data edge. Many points lie above the line in Figure 2, so this is clearly not a frontier.

8. Guessed terms.
"Facet" (meaning a term of the posynomial), "reach", "stock regime", and "support".

9. Read the whole paper?
Yes, for the theorem ledger and the honest hedging. The practical value for real trade studies is unclear.

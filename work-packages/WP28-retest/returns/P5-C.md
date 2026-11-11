# P5-C

## 1. What this is about

The paper starts from a table of N evaluated designs with d strictly positive, larger-is-better metrics. It fits a one-sided envelope to the data in log space. With one term (K = 1) the envelope is a single hyperplane w·u = β with w on the simplex. In metric space that is the level set V = 1 of a weighted geometric mean, which is where "hyperbolic" comes from. With K > 1 it is a max (or a log-sum-exp at finite κ) of such hyperplanes, so exp(κΦ_K) is a posynomial and the model is GGP-compatible.

The fit is not least squares. For each direction w the offset β is a normalised entropic soft maximum (log-mean-exp at temperature τ) of the scores w·u_i, and w minimises that soft maximum over the simplex. Read as an optimiser would read it, the K = 1 problem is the minimum over the simplex of a smoothed support function of the point cloud. At τ = ∞ it is the LP min_w max_i w·u_i. The stated purpose is decision analysis. Three outputs are read from the fit:

- each term's exponent vector, read as elasticities between metrics;
- the support of each term's exponents, the "contending set" or "n-lemma";
- a reversible change of coordinates, the "chart" (Z = Bu, log V), splitting each design into a position along the surface and a level relative to it.

The worked example is a cubesat with 706 feasible designs and 8 metrics.

## 2. The main results, as I now understand them

- **Homogeneity and shift (Th. 1, Prop. 1).** V is degree-1 homogeneous. A uniform shift of every log-metric by c moves β by c and leaves w* unchanged. Both are elementary and correct.
- **The one-term fit is convex (Th. 3).** The second directional derivative of the log-mean-exp is τ times a p-weighted variance. That is correct, and so is "every minimiser is global, uniqueness not claimed". Calling it a geometric program in x = e^w is right but roundabout: it is already a convex program in w. Its simplex KKT conditions (Th. 2) are the standard ones, g_j ≥ λ with complementary slackness, λ = w·g.
- **LME against LSE (Th. 4).** The bounds mean ≤ LME ≤ max and max − (log N)/τ ≤ LME are correct and standard. The 1/N normalisation makes β independent of N in the sense stated.
- **Geometry at τ = ∞, my own reading.** By LP duality, min_{w∈Δ} max_i w·u_i equals max over p in the data simplex of min_j (U^T p)_j. The "balanced point" U^T p is the point where the ray t·1 leaves the convex hull of the data extended downwards (free disposal). w is a normal of the supporting hyperplane there, and R1 asks that this normal be unique.
  - Equation (2)'s objective f_k(w) = J_τ(Uw) − ū_k·w equals J_τ((U − 1ū_k^T)w). Each term is therefore the support hyperplane where the diagonal ray from its cell's centroid leaves the hull of all the data.
  - At K = 1 this makes the slack objective invariant to per-metric shifts of the log-metrics, which equation (1) is not. This matches the remark in Section 8 that the two coincide on centred data.
- **Elasticities (Th. 5).** On the hyperplane, d log m_j / d log m_i = −w_i/w_j, holding the other metrics fixed. This is correct as a statement about the hyperplane.
- **Chart and pull-back (Th. 6, 7).** The chart is an orthogonal change of coordinates (a Helmert-type basis). Under log-affine conditioning V is a monomial in the shifted attributes.
- **Posynomial extension (Th. 8).** The log-sum-exp is squeezed within (log K)/κ of the max, and exp(κΦ_K) is a posynomial. Correct.
- **Pareto efficiency (Th. 9).** A maximiser of V (over some set, presumably the attainable set or the sample) is weakly efficient, and efficient when w > 0. This is the standard weighted-sum scalarisation fact in log coordinates, and the converse is correctly not claimed.
- **Several terms (Section 6.2).**
  - Th. 10: the objective is not convex, by the symmetry and averaging argument. With weights fixed, the soft objective majorises the soft slack, which is the usual Gibbs/Jensen majorisation, so the soft alternation is a majorise-minimise scheme.
  - Th. 11: the sharp alternation is a Lloyd-type scheme. Reassignment followed by an exact refit does not raise the mean slack, and it terminates in finitely many steps under unique minimisers and a tie rule.
  - Lemma 1: the term gap is the Frank-Wolfe duality gap, which bounds suboptimality. Correct.
  - Lemma 2: a positive assignment margin gives a radius within which labels do not change.
  - Prop. 3: inside that radius, with each w_k exactly optimal for its cell, the point is a local minimiser of the sharp objective. This is the k-means fixed-point argument and correct as stated.
  - Th. 12: a second-order sufficient condition for the soft fit. The Hessian D − κM is positive definite on a subspace containing the critical cone, and that suffices because the constraints are affine. The structure of the argument is correct.
- **Numerical results on the case.**
  - At K = 1 the contending set has 5 metrics.
  - At K = 3 the three sets differ (4, 5 and 5 metrics), and control effort and peak slew power each lead a term.
  - The K = 3 fit is declared certified: term gaps are below 1e-12 and the margin is 0.00121. The stable radius is 1.2e-4, about 70 times smaller than the band. The paper says plainly that this local certificate is tiny.
  - On 16 of 20 planted tables, all three planted terms are recovered "to within 0.05".
- **Open (stated as open).** Global convergence or optimality of the alternation, statistical consistency, identifiability, and when the surface recovers the Pareto boundary rather than the envelope of the sample.

## 3. What I would do next with it

- Read Appendix B's proofs of L15 (finite termination), L17 (the Hessian formula) and L3.9 (R1 at the fit temperature). These are the steps I could not check from the sketches.
- Treat the K = 1 problem as what it is, the minimum of a smoothed support function over the simplex, and work out its dual cleanly at finite τ. That should give the balanced point an entropy-regularised dual interpretation (p maximising min_j (U^T p)_j minus an entropy penalty). That interpretation would also say what τ is doing statistically.
- Run the sharp alternation from many random initialisations on the case and on the planted tables. I would report the spread of final objectives and of contending sets. Local-minimum multiplicity is the classic failure of Lloyd-type schemes, and the paper's stability evidence is jitter of the data, not of the starting point.
- Compare against the closest prior objects I can see in the bibliography but did not see discussed in the main text: Charnes et al. 1982/1983 (multiplicative DEA, "piecewise Cobb-Douglas envelopments") and Banker and Maindiratta 1986 (piecewise log-linear efficient surfaces). These look like the same geometric object, fitted by a different criterion.
- Study the bias that the Gaussian cumulant identity implies. Under noise the population soft maximum is inflated by τσ²‖w‖²/2, which favours spread-out weights, and more so at larger τ. I would want to know how this interacts with the fact that a smaller τ adds metrics to the support (Figure 4).

## 4. What I would tell a colleague

It is a frontier-fitting estimator: a soft-max support-function fit in log space, with a k-means-like alternation for several terms. It is packaged for engineering trade studies. The convex part (K = 1) is clean and the mathematics in the main text is mostly standard and stated carefully.

The guarantees for K > 1 are deliberately modest and honestly labelled. There is descent, finite termination under uniqueness, and a local-minimum certificate whose radius on the case is about 1e-4. The paper says this is far smaller than the scale at which it reads results. Global optimality is explicitly not claimed.

The interpretive content (contending sets, elasticities) rests on numerics and on choices: the conditioning, τ fixed by a 10%-above convention, and K chosen by the analyst. The paper says so. It is also clear about separating what is proved, what is observed and what is open, which I appreciated. The closest prior art seems to be multiplicative DEA (piecewise Cobb-Douglas envelopments), and I would want that comparison spelled out.

## 5. What the method does not do, and what the paper does not claim

- It does not compute the Pareto set, and it does not claim the surface is the Pareto boundary. At τ = ∞ it can at best describe the convex hull, in log space, of the sample's free-disposal set. Points on dents in log space (unsupported efficient points) are invisible to it, as with any weighted-sum scalarisation.
- It does not claim a global optimum, global convergence or uniqueness for K > 1. It does not claim uniqueness at K = 1.
- It does not claim statistical consistency, identifiability or sampling distributions for the exponents. The exponents describe the sample.
- It does not choose K. Mean slack decreases with K by construction.
- It does not claim causal trade-offs. Elasticities are properties of the fitted surface, in conditioned units.
- It does not impose requirements or constraints in the fit. They are read afterwards.
- The search loop (Section 7) is explicitly future work with no results.
- No kernel generalisation is built.
- The propose, predict, check exercise is an illustration on 3 proposals (2 distinct designs), not a rate.
- It does not claim that PCA on the chart is a result, only a reading.

## 6. Where I was confused or stopped, in order

1. "and 659 on 8, all of them (counts that hold over five regenerations...)". I read "all of them" as saying all 706 are nondominated, but the number is 659. I could not tell whether "all of them" refers to the designs or to the counts holding over all regenerations.

2. "Term aggregation: the formula is the sum; the package's mean subtracts the constant (log K)/κ from every level". I followed this, but it means the bounds of Theorem 8 are for the sum. With the mean, the squeeze is max − (log K)/κ ≤ Φ ≤ max. I had to work out which one the case uses; at κ = ∞ it does not matter.

3. Definition 6: "the support ... of the exact-maximum (τ = ∞) fit to the term's cell, centred on the cell's mean log-metric ... a member below the participation threshold ... contends in the limit". The contending set comes from one optimisation problem: τ = ∞, the cell's rows only, centred at the cell's mean. The exponents come from another: finite τ, f_k over all rows. So these are different data as well as different temperatures, and "contends in the limit" suggests only the temperature differs.
   - I also could not find a rule for the reverse case, a metric above the participation threshold that is not in the contending set. In Figure 8, term 3 has power margin at w = 0.02, settling time at 0.05 and depth of discharge at 0.02, and the title says 5-lemma. Six exponents are above 0.001 there. As far as I could make out the outlines at the image's resolution, I could see only four outlined cells in term 3's map, while its title says 5-lemma.
   - Section 5 says an exponent above threshold "participates". So participating and contending are two distinct notions, and I did not see how they relate.

4. "R1: ... lies in the relative interior of a facet of the supporting envelope with positive normal". At K = 1 the support is 5 of 8 metrics, so the normal w has zero components. I could not tell whether "positive normal" means positive on the support or strictly positive. Theorem 2's hypothesis "w_j > 0 for every j there" has the same ambiguity ("there" = on the support?).

5. Theorem 5's sketch: "Identifying these rates with the fit needs Theorem 2 and R1." R1 is explicitly a τ = ∞ statement and "does not imply that the finite-τ minimizer is interior", yet the elasticities are read at the fit temperature. I could not see which hypothesis licenses reading finite-τ exponents as identified elasticities.

6. Section 5: "rescaling one metric changes which term is tangent". I agree for the scale α_j. But f_1 (and every f_k) is invariant to per-metric shifts of the log-metrics, while equation (1) is not. I was not sure which objective "the model" refers to in that sentence, or whether shifts are meant to be included.

7. Theorem 10: (ii) states the majorisation, but I did not see the consequence stated, that the soft alternation does not increase the soft slack. Descent (L15) is stated only for the sharp alternation. I expected one or the other to be the stated algorithmic guarantee for the soft fit.

8. Theorem 11: "With unique term minimizers and a fixed tie rule the sharp alternation stops within K^N+1 iterations ... stationarity of the stop ... not claimed."
   - Theorem 3 explicitly does not give strict convexity, and Section 9 says the objective is flat along the swap of identical columns. The case has a pair with association 0.99. So I could not tell whether the uniqueness hypothesis is expected to hold on the case.
   - I also did not see why the stopping point is not stationary. With exact minimisers, a repeated assignment seems to be a fixed point satisfying Proposition 3's hypotheses except possibly R2.
   - K^N + 1 (3^706 here) is a finiteness statement, not a usable bound. That is fine, but I wanted it said.
   - A8 requires nonempty cells, and I did not see that reassignment preserves nonemptiness.

9. Corollary 1: "Hypotheses. As Proposition 3". Proposition 3 assumes every w_k minimises f_k exactly, so each G_k = 0 and the bound reads 0 ≤ F − F*_fixed ≤ 0. I expected the corollary to be for approximate minimisers, which is how the stopping declaration uses it ("term gaps within tolerance ... so Proposition 3 and Corollary 1 apply"). As written I could not reconcile the two.

10. Theorem 12's sketch: "computed through the sums ... and checked against finite differences on an exact instance". This is labelled Derived, which the paper defines as proved by a script. A finite-difference check on one instance is not a derivation of the Hessian formula in general, and I could not tell which of the two the script does. The same question applies to "Derived" generally, for statements in symbolic N, d and K.

11. The hypotheses F5, F10 and F12 ("the maximum is attained"). For finite N and a compact simplex these hold trivially, so I wondered what case they guard against. A8 also appears in Theorem 11 although Section 3 lists only A1 to A7.

12. "the exponents at the fit temperature rest on about 25 of the 706 designs". Two sentences earlier the effective sample size is 23.1. This is minor, but I paused over it.

13. "On the 20 planted tables the fit recovers all three terms to within 0.05 in 16". I could not tell within 0.05 of what: a norm of the exponent difference (which one?), the offsets, or both. I also could not tell how fitted terms are matched to planted ones.

14. "On term 2 the elasticity between total mass and energy balance is -1.7: ... one percent gained in energy balance is 1.7 percent given up in total mass".
   - From Figure 8 (w = 0.42 and 0.24) I reproduced −1.75 in conditioned log-metrics.
   - By Theorem 7, the elasticity in attribute units is −(w_i α_i)/(w_j α_j) and is with respect to (a_j + s_j), not a_j. The conditioning scales each metric to unit log-spread and shifts it.
   - So I could not tell whether "1.7 percent of total mass" means percent of kilograms or of the conditioned metric. The two coincide only if α_mass = α_EB and s = 0.

15. Figure 7 (as I read the image): the grey near-frontier band seems to lie just below the line log V = 0. Definition 4 defines the band as |log V| < 1/τ, which is symmetric. I could not tell at the image's resolution whether the band is drawn one-sided.

16. Section 6.3 / Section 12: "Q1: global convergence of the alternation, not pursued". Theorem 11 already gives finite termination, under its hypotheses. I could not tell whether Q1 means convergence to a stationary point from any start, or global optimality.

17. Section 7: "Outward monotonicity is stated for the exact maximum and not for the soft one; neither has a lemma here." Stated where, and as what? If it is stated without a lemma, I expected it among the Open items with a label.

18. Figure 8, term 3: the association between pointing error and peak slew power is −1.00 (−0.95 at K = 1, Figure 9). A perfect correlation among a cell's near-frontier designs suggests a functional coupling through the discrete swaps, which the text half-says. I wondered whether a "trade-off" at an elasticity of −0.38 between two metrics that are deterministic functions of the same two categorical choices means more than "these swaps move both".

## 7. Terms whose meaning I had to guess

- **n-lemma / contending set:** the support of a term's exponent vector in the τ = ∞ cell fit; n is its size.
- **Energy differential:** simply log V, the signed log-distance in "levels" to the surface.
- **Reach β_k:** the soft support function value h_τ(w_k) of the data.
- **Balanced point:** the dual point U^T p, the p-weighted centroid of the data, whose coordinates on the support are equal.
- **Cell:** the designs for which term k attains the max score (a Voronoi-like region of the max-affine model).
- **Term share:** the fraction of near-frontier designs in a cell.
- **Near-frontier band:** |log V| < 1/τ.
- **Participation threshold (10^-3):** the cutoff below which an exponent is treated as having no elasticity. It is distinct from membership in the contending set, and I did not fully understand the distinction.
- **Mean slack F:** the average over designs of the (sharp) distance below the K-term envelope in log units.
- **Term gap:** the Frank-Wolfe gap for f_k on the simplex.
- **Assignment margin / stable radius:** the smallest best-minus-second-best score gap, and the parameter radius that preserves labels.
- **Log-convex envelope:** I took it to mean convex in log coordinates (the region Φ_K ≤ 0 is convex in u), not log-convex in the usual sense of a function whose log is convex.
- **Hole (of the chart):** an empty region of the chart coordinates, used as a target for proposals.
- **F (fallback) / I (inherited):** an F is an attainment or regularity assumption added to make a step go through; an I is a standard result imported without proof.
- **"Sharp" / "soft" weights:** κ = ∞ hard assignment against finite-κ softmax responsibilities.
- **MoE / MoP:** measure of effectiveness / measure of performance, systems-engineering terms.
- **Certified (status):** the sharp-fit checks pass (assignment fixed, gaps and residuals within tolerance, cells nonempty, margin positive), or for a soft fit the second-order test passes.

## 8. Questions I am left with

- How is the alternation initialised, how many restarts are used, and how variable are the final objective and the contending sets across restarts?
- Is the Hessian formula of Theorem 12 derived symbolically in general, or checked numerically on an instance? More generally, what does "proved by a plain-SymPy script" establish for statements in symbolic N, d and K?
- What is the intended reading of Corollary 1 for approximate minimisers, and does the local-optimality conclusion survive approximation (it seems to, as ε-optimality on the stable neighbourhood)?
- Why is the tangency point the diagonal exit point from the data centroid (or the origin)? Is there a decision-theoretic reason to privilege the direction 1, given that the conditioning to unit log-spread is what makes 1 meaningful?
- Is uniqueness of the term minimisers expected on real tables with near-duplicate metrics, and if not, what does Theorem 11 give?
- How does the noise-induced penalty τσ²‖w‖²/2 bias the selected support, and does the 10% rule for τ make the support depend on the noise level?
- How does this relate precisely to multiplicative DEA and piecewise Cobb-Douglas envelopments, and to Magnani and Boyd's max-affine fitting, which minimises least squares rather than a one-sided slack?
- Are the K = 3 contending sets stable when K changes (K = 2, 4), or only under jitter at fixed K?
- In what units are the reported elasticities, conditioned or attribute?
- What exactly is "within 0.05" in the planted-recovery result?

## 9. Whether I would read the appendices

Yes, selectively. I would read Appendix B for L3.9, L15.17 to L15.22, L16 and L17. Those are the places where the main-text sketches did not let me check the step: R1 at the fit temperature, the uniqueness and termination argument, the soft-alternation descent, and whether the Hessian is derived or only checked. I would read Appendix E for what the gaps ledger concedes, D.14 for the meaning of the planted-recovery metric, and G for how the paper separates itself from multiplicative DEA. I would skip Appendix C (the cubesat model) and most of D, since judging the physics is not my field.

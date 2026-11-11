# P6-B

Reader background: efficiency measurement (DEA and its variants, Pareto dominance, stochastic and deterministic frontiers). I read the nine figures first, then the captions, the headings, and the main results and boxed statements. I had nothing else.

## 1. What this is about

The paper fits a frontier to a table of sampled designs. Each design is scored on d strictly positive, larger-is-better "metrics" (costs are inverted at a "conditioning" step the analyst does beforehand). With one term (K = 1) the frontier is a single monomial, a weighted geometric mean with exponents on the simplex, scaled so that V = 1 on a "fitted reference surface". In log coordinates that is a hyperplane w·u = β. With K > 1 terms the surface is a smoothed maximum (a log-sum-exp with "term temperature" κ) of several such hyperplanes, so it is the 1/κ power of a posynomial and stays compatible with geometric programming. The fit uses a soft maximum (a log-mean-exp at "fit temperature" τ) of the scores, and τ is chosen so that a target fraction of the designs (0.1 in the case study) lies beyond the surface. τ = ∞ gives the exact supporting envelope.

The model is then read in two ways. The exponents are taken as elasticities, that is, trade-off rates along the surface. The support of the exact-maximum fit within each term's "cell" (the designs that term scores highest) is called the "contending set", and its size n names the trade-off a "dilemma", "trilemma", or in general an "n-lemma". There is also a "chart": a design's level log V together with an orthonormal, scale-free position Z. The application is a cubesat attitude-control, power and mass model with eight metrics, two controller-gain regimes ("primary" and "stock"), and a K = 3 fit that the paper says separates contending sets which a single term blends.

In my field's terms, this is an output-only (benefit-of-the-doubt) frontier with one common set of weights, multiplicative (Cobb-Douglas) in the outputs. It is fitted as a soft or quantile-type boundary rather than as a full envelope, and it is extended to a piecewise log-linear (max-affine) surface by alternating assignment and refit.

## 2. The main results, as I understand them

- **Theorem 1.** V is homogeneous of degree 1 in the metrics, and log V = w·u − β. So 1/V is a radial (Farrell or Shephard-type, output-oriented) expansion factor with respect to the fitted surface (Theorem 5 states that improving every metric by 1/V reaches V = 1).
- **Proposition 1.** A common shift of all log-metrics moves β and leaves the exponents unchanged.
- **Theorems 2 to 4.** The one-term fit minimizes a log-mean-exp of the scores Uw over the simplex. This objective is convex, though not strictly (Theorem 3: the second derivative is τ times a variance), so every minimizer is global but it need not be unique. The KKT conditions are the usual simplex ones. Log-mean-exp sits between the mean and the maximum, and it differs from log-sum-exp by (log N)/τ.
- **Proposition 2.** Under Gaussian noise the soft maximum carries a bias term of τσ²‖w‖²/2. It is stated as a population identity, with no consistency claim.
- **Theorems 5 to 7.** Exponent ratios are elasticities on the surface. The chart (Z, log V) is an invertible reparametrization of the log-metrics. Under a stated affine-in-log conditioning, the model pulls back to the raw attributes, and a negative product w_j α_j marks a cost.
- **Theorem 8.** The K-term form is shift-equivariant. It reduces to the monomial at K = 1, sits within (log K)/κ of the hard maximum of the terms, and is a posynomial after exponentiation.
- **Theorem 9.** A maximizer of V is weakly Pareto-efficient, and efficient if every w_j > 0. The converse is explicitly not claimed.
- **Theorems 10 and 11, Lemmas 1 and 2, Proposition 3, Corollary 1.** The K-term fit is not convex in the terms, and it comes with three graded guarantees. Level 1: a Lloyd/k-means-style alternation does not increase the mean slack, and its sharp version terminates within K^N + 1 iterations. Level 2: a per-term duality gap G_k bounds suboptimality, and it equals the LP duality gap at τ = ∞. Level 3: given an assignment margin γ > 0 and a stable radius, the result is a local minimizer of the mean slack. Global optimality is not claimed.
- **Theorem 12.** A second-order sufficient-condition certificate for the soft (finite τ, κ) fit, with Hessian D − κM, where M measures the designs' ambiguity between terms.
- **Case study.** On the primary regime at K = 1, the fit temperature is τ ≈ 38 and the effective sample size is about 23. Five metrics carry weight: total mass 0.36, energy balance 0.18, pointing error 0.16, depth of discharge 0.16, settling time 0.14. Control effort, power margin and peak slew power get zero. At K = 3, the terms have different supports, for example term 3 is dominated by peak slew power (0.61) and pointing error (0.23). Under stock gains, the K = 1 weights move to control effort and settling time.
- **PCA (Appendix D.16).** Principal components on the near-frontier chart are offered as a reading of what the sampling exercised, not as a result.

## 3. What I would do next with it

- Line it up formally against (a) multiplicative DEA (Banker and Maindiratta; the Charnes-Cooper multiplicative model), (b) common-set-of-weights DEA and benefit-of-the-doubt composite indicators, (c) order-α and order-m partial frontiers (Cazals, Florens, Simar; Daouia), which are what a "fraction above V = 1 equals 0.1" convention most resembles, (d) max-affine and convex piecewise-linear regression (Magnani and Boyd) and Kuosmanen's CNLS/StoNED for the K > 1 alternation, and (e) GP-compatible softmax fitting of posynomials (Hoburg and coauthors). Table 1 apparently does this, but its body was not given to me, so I cannot tell whether these families are in it.
- Test units invariance: rescale one metric by a constant and see whether w* changes. Proposition 1 covers only a uniform shift c·1, not a per-metric shift. Radial DEA is units-invariant, and I would want the same property here or an explicit statement about how centring handles it.
- Test sensitivity to near-duplicate metrics. Power margin and energy balance correlate at 0.99 in Figures 8 and 9, and the weight lands on one or the other depending on the regime. That looks like the non-uniqueness Theorem 3 allows, not a change in the system.
- Resample the designs (bootstrap) and look at how stable the contending sets and exponents are. With n_eff ≈ 23 out of a few hundred designs, I would expect the support to move.

## 4. What I would tell a colleague

"It's a common-weights, output-only Cobb-Douglas frontier in log space, fitted as a soft quantile boundary (a log-mean-exp with temperature set so that 10% of the units lie beyond it), with a max-affine extension for several terms fitted by Lloyd-style alternation. The convexity, KKT, LSE/LME bounds and 'a maximizer of a strictly increasing scalarization is Pareto-efficient' are textbook, and the paper appears to label them as derived, not new. What I can see as its own is the reading: the support of the τ = ∞ weights, the outputs that get nonzero weight, is presented as the set of metrics in tension ('n-lemma'), per piece of the surface. In DEA we treat zero weights as a pathology and add weight restrictions. Here they are the finding. That is a substantive inversion of the interpretation, not just a renaming. Its validity depends on how stable and identifiable the support is, and the snippets give no evidence on that. The graded guarantees for the multi-term fit are carefully hedged and look honest. Much of the vocabulary (reach, energy differential, n-lemma, chart, cell) renames known objects."

Substantive versus terminological, as far as I can judge:
- Terminological: "reach" (the frontier intercept or offset), "energy differential" (the log distance-function value), "cell" (Voronoi or assignment region), "chart" (centred log-ratio coordinates plus a scale coordinate), "invariant form" (Cobb-Douglas aggregator, homogeneous of degree 1).
- Substantive or at least distinctive: tuning τ to a target exceedance fraction with the log-mean-exp; the explicit separation of the three objects (fitted reference surface, supporting envelope, Pareto boundary); using exact-maximum support as an interpretive device; the graded certificates for the non-convex K-term fit; keeping GP compatibility so the fitted surface can feed a downstream design optimization.

## 5. What the method does not do, and what the paper does not claim

- It is not an estimate of the Pareto boundary. Definition 1 says so, and the surface is deliberately exceeded by a fraction of the designs.
- No statistical inference: no consistency, rates, confidence regions or noise model. Proposition 2 is explicitly a population identity without a consistency claim.
- No uniqueness of the one-term minimizer, and no global optimality for K > 1. Termination of the sharp alternation is proved, but stationarity at the stop and convergence otherwise are not claimed. The stable radius is sufficient and not claimed tight. The approximate certificate covers the returned run only, not restarts.
- The converse of Theorem 9 is not claimed. So Pareto points that are not supported, in the log-convex sense, are not recovered at K = 1. This is the classic weighted-sum limitation, here in log space; K > 1 presumably mitigates it but is not claimed to remove it.
- No input/output distinction. Everything is an output after the analyst's conditioning, and the conditioning is left to the analyst.
- PCA on the chart, and the association (correlation) maps, are presented as analyses of the sampled designs, not properties of the model.
- Search of the design space is preliminary, and its monotonicity is open. Q1 to Q4 are listed as open but not given to me.
- I see no claim of noise robustness, no treatment of outliers or super-efficient units (beyond the 10% exceedance), and no comparison to a DEA or FDH frontier on the same data.

## 6. Where I was confused or stopped, in the order I met it

1. **Figure 1, before the caption.** The triangle shows three numbered points and open rings, with "planted (the known answer)". Term 2's point sits a little below its ring. I could not tell how close a recovery has to be to count as successful, or whether the off-diagonal placement of term 2 makes it still a trilemma by the support definition, since all three exponents are clearly positive. My questions were whether the support is read at τ = ∞ or at the fit temperature, and whether the edge points are exactly on the edge. The caption says "its exponent vector at the fit temperature is a point of the triangle", but Definition 6 says the n-lemma is named by the τ = ∞ support. At finite τ a point need not lie on an edge even when the exact-maximum support is two metrics. So which one does the figure show?
2. **Figure 2.** A parts tree with swap and tune labels. It is clear as a model, but it was not clear what it had to do with the frontier until the captions.
3. **Figure 3.** The SlewExperiment box reads "returns 7 of 8 metrics ... settling time (not returned)". The caption says "the measured slew supplies the settling time and the control effort, which the analysis passes on". I had to work out that settling time reaches the table directly from the measurement and not through the analysis. I also wondered why three requirements "read no traded metric", and whether constraints like these define the attainable set (feasibility) rather than entering the frontier at all.
4. **Figure 4.** "fraction of designs above V = 1" with "target 0.1" and the vertical line at τ = 38.1. The caption calls the choice "a convention, Section 5". I expected some justification of 0.1 in terms of what it buys, by analogy with choosing α in an order-α frontier. The bottom panel also shows that control effort carries weight at small τ and vanishes from about τ = 25. I could not tell whether the support is stable for τ above the fit temperature (it appears so) or whether this is an artefact of near-ties.
5. **Figure 5.** "they reach the line and stop there, a few beyond it". Looking at the image, the dark points spread widely below the line, down to about 2.5 log units, and only a band of them is near it. I read "reach and stop" as "the upper envelope of the dark points is near the line", not "they cluster on it". That is fine, but it was not what I first saw.
6. **Figure 6, top panel.** The black line cuts through the light cloud with many light points above it. The caption explains that light points "fall on either side of the line wherever their level is", but in the term 1 panel a good share of the dark points also seem to lie beyond the line near the top left. I could not judge whether that is within the 0.1 tolerance.
7. **Figure 6, bottom panel.** The line lies above almost all the points, and the discrete bands (tracker grade, wheel class) dominate the picture. For a discrete design space I wondered whether a smooth surface is the right object at all, or whether FDH-style thinking is more natural here.
8. **Figure 7.** The near-frontier band is very thin: |log V| < 1/τ ≈ 0.026. Only a small fraction of designs sit in it, and yet the PCA "position" direction is computed from those designs. The caption says "the K = 1 fit's band as at every K", which I did not fully parse: is the band always defined from the K = 1 τ even when the chart is for K = 3?
9. **Figure 8.** Outlined cells are the τ = ∞ support, and "an outlined metric can be grey". In term 3, energy balance is outlined with w = 0.00, while power margin has w = 0.02 and is not outlined. So a metric can be in the contending set with zero fit-temperature weight, and out of it with positive weight. Definition 6 does explain this, but it means the "n" in the n-lemma and the elasticities refer to different metric sets. I stopped to check that I had it right. Term 3 also shows pointing error against peak slew power at exactly −1.00, which suggests that within the cell these two are functionally tied (the discrete bands), so a correlation map tells me little there.
10. **Figure 9.** In the stock regime, total mass gets w = 0.00 and is not outlined, while in primary it is the heaviest metric. I expected a sentence on whether this is a real regime change or a consequence of the sampling. The captions present it neutrally.
11. **Definition 3**, "the package's mean subtracts the constant (log K)/κ". A software detail entered a definition. I had to work out that it changes only β.
12. **Definition 4**, "one inside the band weighs within a factor e of one on the surface". I took this to mean the softmax weight of a design in the band is within a factor e of the weight of a design exactly at V = 1. That needs the weight to be proportional to e^{τ log V}, which fits the log-mean-exp with temperature τ.
13. **Theorem 2**, "for the facet-normal reading, w_j > 0 for every j there (R1's relation at the fit temperature ...)". R1 is not defined in what I was given, and I could not reconstruct what the "facet-normal reading" asserts.
14. **Theorem 10 (i)**, "a convex program symmetric in the terms attains its minimum with all terms equal ... so it is not convex in them". I followed the logic (symmetry plus convexity forces a symmetric minimizer, and the fit does better asymmetrically), but it took a second reading.
15. **Main results**, "Numerical: the termination status a fit reaches, read from its record". I could not tell what result this is.
16. **Main results**, "the terms separate contending sets that one term blends". I expected some measure of separation, or a comparison of fit (slack, exceedance) between K = 1 and K = 3, and saw none in the snippets.

## 7. Terms whose meaning I had to guess

- **Hyperbolic trade space** (title): the level sets of a monomial, ∏ m_j^{w_j} = const, are hyperbola-like surfaces in the metric space, so trade-offs are multiplicative.
- **Conditioning**: a per-metric monotone transform (log m = α log(a + s) + b) that makes each attribute positive and larger-is-better.
- **Reach β**: the frontier offset, the (soft) maximum score along w.
- **Fit temperature τ / term temperature κ**: the inverse smoothing of the max over designs and of the max over terms respectively.
- **Slack / mean slack F**: the per-design gap between the design's score and the surface, averaged. I guess β minus the score, or the reverse, in log units.
- **Effective sample size**: probably (Σp)²/Σp² of the softmax weights, the number of designs that effectively determine the fit.
- **Participation threshold**: an exponent of at most 0.001 counts as non-participating at the fit temperature.
- **Contending set / n-lemma**: the metrics with nonzero exact-maximum weight in a term's cell, and their count.
- **Energy differential**: log V, a physics metaphor for the log distance to the surface.
- **Primary / stock regime**: the two settings of the controller gains, aggressive versus default.
- **A1 to A8, F5, F10, F12, I5 to I16, R1, R2, L1 to L17**: assumptions, facts, identities, regularity conditions and lemma-script labels. Not given to me. I guessed R2 is "assignment margin γ > 0".
- **Term share**: the fraction of near-frontier designs whose largest term is k.

## 8. Questions I am left with

1. Is the K = 1 fit invariant to rescaling a single metric (a per-metric shift in log)? If not, how is that handled: by centring, or by the conditioning?
2. Why minimize the soft maximum over a common w? Each DEA unit chooses its own most favourable weights; here one direction is chosen to make the data's extent smallest. What is the economic or engineering interpretation of the "tightest" common direction, and how does it compare to common-set-of-weights DEA?
3. How stable is the contending set under resampling of the designs, under the choice of target fraction, and under near-collinear metrics (power margin and energy balance)?
4. What does the K = 3 fit gain over K = 1 in fit terms, and how was K chosen?
5. How does the reference surface compare to the DEA/FDH frontier, or to an order-α frontier, on the same cubesat data?
6. With a discrete design space (wheel class, tracker grade), are the smooth terms partly fitting the discrete structure, and does that inflate n?
7. Is there any noise in the evaluations, simulated or real (the measured slew "field data when fielded")? If so, how does Proposition 2's bias enter the choice of τ?
8. What exactly are Q1 to Q4?

## 9. Would I read the whole paper?

Yes, selectively. I would go straight to Section 2 and Table 1, to see whether the authors place themselves against multiplicative and common-weights DEA, partial (order-α) frontiers and max-affine regression. Then I would read Section 5 for the τ convention and the conditioning, and Section 9 for the evidence that the K = 3 terms separate anything. The boxed mathematics is mostly standard convex analysis, so it would not by itself bring me back. What would bring me back is the interpretive claim that the zero pattern of a common-weights frontier identifies the metrics in tension. That is a reading my field has largely avoided, and I would want to see whether the paper shows it is stable enough to trust. If Table 1 omits the DEA literature, I would read the rest as a referee, expecting to ask for that comparison.

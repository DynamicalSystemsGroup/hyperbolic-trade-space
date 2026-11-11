# P5-B

## 1. What this is about

A method for reading a trade study. You have N candidate designs, each evaluated on d "metrics". A metric is a positive quantity where larger is better, and the paper works with its logarithm u. The method fits a "reference surface" to the outer edge of the cloud of log-metric points.

For one term the surface is a hyperplane w·u = β in log-metric space, with w on the probability simplex. Equivalently it is a weighted geometric mean of the metrics, ∏ m_j^{w_j}, set equal to a constant. That is a hyperbola-like surface, hence "hyperbolic trade space".

The fit is a soft-maximum (log-mean-exp) minimisation over w. It is convex, and I read it as a geometric program. The exponents w_j are then read as elasticities: percent change of metric j per percent change of metric i along the surface. Each design gets a "level" log V, which is 0 on the surface and negative inside it.

For several terms the model is a posynomial (a log-sum-exp of several such hyperplanes). The fit then alternates, k-means style, between assigning designs to the term that scores them highest and refitting each term on its cell. The paper offers three tiers of guarantee for that alternation and a soft-assignment variant with a second-order certificate.

A "term" is read through the set of metrics that contend in it: a dilemma if two, a trilemma if three, and in general an "n-lemma". The worked case is a cubesat model with 8 metrics: mass, energy balance, pointing error, settling time, control effort and so on. It is run in two regimes, "primary" (aggressive controller gains) and "stock".

## 2. The main results, as I now understand them

- **Homogeneity (Theorem 1).** V is homogeneous of degree 1 because w sums to 1. Doubling every metric doubles V.
- **Soft maximum (Theorem 4).** The log-mean-exp sits between the mean and the maximum, and within (log N)/τ of the maximum. That is correct.
- **KKT conditions (Theorem 2).** For minimising a convex function over the simplex, g_j ≥ λ = w·g with complementary slackness. I checked this and it is the standard result.
- **Convexity (Theorem 3).** J_τ(w) is convex in w, since its second derivative is τ·Var_p(v·u). Convexity is not claimed to be strict, and uniqueness is not claimed.
- **Elasticities (Theorem 5).** If the frontier is exactly the hyperplane, then d log m_j / d log m_i = −w_i/w_j. I checked it. Improving j alone by V^{-1/w_j}, or every metric by 1/V, reaches V = 1. Both follow.
- **Chart (Theorem 6).** (Z, log V) is a bijective rewriting of the log-metrics. Z is the d−1 coordinates orthogonal to the all-ones direction, and log V supplies the remaining coordinate. That works for K = 1.
- **Posynomial extension (Theorem 8).** The K-term level Φ_K is within (log K)/κ above the maximum of the term scores, and e^{κΦ} is a posynomial in m. Both are correct as written.
- **Efficiency (Theorem 9).** A maximiser of V is weakly Pareto-efficient, and efficient when every w_j > 0. The converse is explicitly not claimed. That is right, and it is the part that matters: a hyperplane in log space cannot represent a non-convex frontier.
- **Several terms.**
  - Theorem 10(i): the multi-term objective is symmetric in the terms but lower at distinct terms than at the all-equal point, so it is not convex in them.
  - Theorem 11 (Level 1): sharp alternation never increases the mean slack F. With unique minimisers and a fixed tie rule it stops in at most K^N + 1 iterations. Stationarity of the stop is not claimed.
  - Lemma 1 (Level 2): the term gap G_k bounds f_k(w) − f_k*. It is zero exactly at the simplex KKT point. I checked the inequality and it holds.
  - Lemma 2 and Proposition 3 (Level 3): if assignments have a positive margin and each term is a minimiser on its cell, then W is a local minimiser of F. The statement is local and conditional on the assignment staying stable.
  - Corollary 1: the gap is bounded relative to the optimum for the fixed partition, not the global optimum.
  - Theorem 12: a second-order sufficient condition for the soft-weight fit, holding at a point where KKT holds exactly.
- **Honesty about status.** The paper labels what is derived, what is "numerical" (the termination status a fit reaches), what is a reading (PCA, association maps), and what is open (Q1 to Q4, and the monotonicity of the search). I could not find a place in these boxes where an observation is dressed as a theorem.
- **Case study.** In the cubesat case the terms separate contending sets that a single term blends together. Figure 9 and Figure 8 support this at the level of which metrics are outlined.

## 3. What I would do next

- Read the proofs and the definitions of J_τ, f_k, the slack, F, and the soft-weight objective. The boxes use them without defining them.
- Read Section 5 for the τ convention, because the exponents I would quote depend on it.
- Reproduce the synthetic Figure 1 recovery on my own data. I would run it with several restarts and several random partitions to see whether the K > 1 alternation lands in different local minima.
- Take two near-collinear metrics (power margin and energy balance, r = 0.99) and perturb the data. I want to know how much weight moves between them.
- Read Section 6.3 (Q1 to Q4) and Section 7.

## 4. What I would tell a colleague

It is a careful, honestly labelled construction. For one term it is a convex fit of a supporting hyperplane to log data, with a soft-maximum smoothing. The KKT, convexity and elasticity statements all check out.

The several-term part is a k-means-like alternation with the usual guarantees and no more. These are monotone descent, finite termination, a gap bound, and local optimality conditional on a stable assignment. The paper says so itself.

The elasticity reading is conditional twice over. It holds along the fitted surface, not necessarily along the true frontier. It also depends on the fit temperature, which is set by a convention (10% of designs beyond V = 1). I would read the exponent table alongside Figure 4, which shows how much the weights move with τ.

## 5. What the method does not do, and what the paper does not claim

- **It is not the Pareto boundary.** Definition 1 says so. Theorem 9 gives only one direction, and the converse is declined.
- **K = 1 uniqueness.** Not claimed.
- **Global optimum for K > 1.** Not claimed. Level 3 is local and conditional on assignment stability. Corollary 1 is for the returned run, not across restarts.
- **Convergence of the sharp alternation to a stationary point.** Not claimed. The soft alternation has no stated convergence claim in the boxes I saw either.
- **Statistical consistency.** Proposition 2 says "no consistency claim". Figure 4 shows an effective sample size of 23 at the fit temperature, so I would expect the exponents to be noisy. The paper does not (in what I saw) offer an uncertainty statement.
- **Association maps and the PCA chart** are labelled readings of the sampled designs, not properties of the model.
- **Theorem 12** holds only where the first-order conditions are exact, not within a tolerance. I do not see how that applies to a numerical output.
- **Conditioning** of attributes into metrics is the analyst's job (Theorem 7 only says it is invertible).
- **The claim "the terms separate contending sets that one term blends"** rests on one case study with two regimes.

## 6. Where I was confused or stopped, in the order I met it

1. **Figure 1 legend:** "Weight on these three metrics: 1.00, 1.00, 1.00 (all of it: d = 3)". I expected one number and found three. I guessed one per term, each term having all its weight on the three metrics.
2. **Figure 1:** term 2's fitted point (orange) sits visibly below its planted ring, while terms 1 and 3 sit on theirs. I could not tell whether the offset is expected or a recovery error, and nothing says how the planted table was generated.
3. **Figure 2:** the swap/tune tags mark the configuration variables (wheel class, tracker grade; panel span, battery capacity, Kp, Kd). Kp and Kd are tuned variables here. Yet Figures 4 and 9 speak of regimes "aggressive controller gains" and "stock gains". I could not tell whether a regime fixes the gains or changes their range.
4. **Figure 3, SlewExperiment box:** "returns 7 of 8 metrics … From the measurement: control effort (passed on) and settling time (not returned)". The caption says the measured slew supplies settling time and control effort "which the analysis passes on", and that the analysis computes "the other six". The arrows from the analysis go to six metrics and none to control effort. I could not reconcile "7 of 8", "passed on" and "not returned".
5. **Figure 3:** "«MoP»", "«MoE»" and "traded metric". The pointing-error requirement is drawn as "not satisfied by cubesatBaseline", yet pointing error is a traded metric. I did not understand how requirements (thresholds) relate to a trade of larger-is-better metrics.
6. **Figure 4:** "n_eff = 23" with no definition. The y-axis starts near 560 at τ = 3, and I took N to be about 600. If the fit rests on about 23 effective designs I would want to know what that does to the exponents.
7. **Figure 4:** the fraction beyond V = 1 at the fit temperature reads about 0.09, not 0.10. The caption's "within 0.01" covers it, but the line is drawn at 38.1, a value that looks fitted to a target.
8. **Figure 4, heat map:** control effort has a nonzero exponent for τ up to 15 and is white from τ = 25 onward. Power margin and peak slew power are white at every τ. I could not tell whether the large exponents are stable under τ. The ordering of rows by the exponent at τ = 38.1 hides the τ-dependence.
9. **Figure 5 caption:** "they reach the line and stop there, a few beyond it (a tenth of all designs lie above V = 1 …)". In the figure the dark points are mostly far below the line. I read "reach the line and stop" as an upper envelope only. I checked that the line's slope is about −2, which matches 0.36/0.18 (the weights of total mass and energy balance in Figures 4 and 9), so that part is consistent.
10. **Figure 6, top panel:** I checked the streaks have slope +1 in the log plane, which matches control effort = torque × settling time. The term-1 line passes through few of the dark points. Term 1 later turns out to have only 3 near-frontier designs (Figure 8), and I do not know how much that term's line is determined by.
11. **Figure 7:** "(44% of it)" in the axis label. I guessed 44% of the spread among near-frontier designs. The surface is "the flat line log V = 0 whatever the position", true by construction in this chart. The figure then shows only how the designs' levels are distributed, and does not show whether the three-term surface fits.
12. **Figure 7:** the band is "the K = 1 fit's band as at every K". I could not tell why the band for K = 3 comes from the K = 1 temperature, or what fraction of designs lies above V = 1 for K = 3.
13. **Figure 8, top:** "term 1: 4-lemma … Too few near-frontier designs for an association reading: 3 of ten". A term can be named a 4-lemma while supported by 3 near-frontier designs. I could not work out whether a 4-lemma from so few designs is meaningful.
14. **Figures 8 and 9, correlation as "tension":** among near-frontier designs, which lie near the hyperplane, w·u is nearly constant. That forces Σ_j w_j Cov(u_i, u_j) ≈ 0 for each i, so negative correlations are partly a consequence of the selection, not independent evidence. I could not tell whether the paper treats this.
15. **Figure 9, regimes:** power margin and energy balance have r = 0.99. In primary, energy balance carries weight 0.18 and power margin 0. In stock the roles swap (power margin 0.18, energy balance 0.02). Settling time and control effort are at −0.95 in stock. So which of two near-duplicate metrics gets the weight can flip with the regime, and I do not see how an elasticity per metric survives that.
16. **Figure 9, stock:** energy balance has w = 0.02 and is not outlined. In Figure 8 term 3, energy balance is outlined with w = 0.00 and power margin has w = 0.02. So positive weight outside the contending set, and contending membership with zero weight, both occur. The caption covers the second case only.
17. **Headings:** "Scaling Decision Analysis with Hyperbolic Trade Space Identification". I could not tell what "Scaling" scales (the decision analysis? the number of metrics?).
18. **Definition 2 and Theorem 1:** Definition 2 writes V(m) = e^{−β}∏m_j^{w_j}, which already contains the offset. Theorem 1 then says V(m e^{−β}) = e^{−β}V(m), "so log V = w·u − β". If V already carries e^{−β}, the offset would be applied twice. I took Theorem 1's V to be the plain weighted geometric mean, but the two statements do not read the same way.
19. **Definition 3:** "the formula is the sum; the package's mean subtracts the constant (log K)/κ from every level and changes neither exponents nor offsets." If every level shifts by a constant, the set where the level equals 0 moves. I could not work out which convention the figures and the case study use.
20. **Boxes using undefined objects:** u, U, s_i, J_τ, f_k, F, "slack", ε in Proposition 2, and the hypothesis labels (A1 to A8, F5, F10, F12, I5 to I16, R1, R2). I could only reconstruct meanings. I took u to be log m, s_ik = w_k·u_i − β_k, J_τ(w) the log-mean-exp of Uw, and slack the reach minus the mean score. The fit appears to need the data centred (otherwise J is not shift-invariant per metric); Definition 6 mentions centring only for the cell refit.
21. **Theorem 4 hypothesis F5, "the maximum is attained":** for a finite sample this is automatic. I could not see why it is a hypothesis.
22. **Theorem 10(ii):** "the soft model's slack is bounded above by the fixed-weight objective, with equality at the weights' own model". That is the shape of a majorise-minimise surrogate, which would give monotone descent. I could not see a statement in the boxes that says the soft alternation descends or converges.
23. **Theorem 11 hypothesis "unique term minimisers":** Theorem 3 says convexity is not strict. I could not tell whether uniqueness holds in the case study, given the near-collinear metrics. And K^N + 1 is only a finiteness statement, astronomically large for N around 600.
24. **Theorem 12 "exactly at the point, not within a tolerance":** a computed point is never exact. I could not tell what the certificate certifies in practice.

## 7. Terms whose meaning I guessed

- **n-lemma:** the situation where n metrics contend, so that not all can be improved together. A corner is one metric binding alone, and an edge is a dilemma.
- **Contending set:** the metrics with nonzero exponent at the exact (τ = ∞) fit to a term's cell.
- **Participation threshold:** an exponent of 0.001 or less is treated as zero.
- **Term, cell:** a term is one hyperplane piece; its cell is the designs on which it scores highest.
- **Reach β:** the soft maximum of the scores along w, which fixes the offset.
- **Slack:** the reach minus the mean score. I read mean slack F as the objective of the multi-term fit.
- **Near-frontier band:** designs with |log V| < 1/τ.
- **Energy differential / level:** log V, borrowed from potentials.
- **Invariant value:** V, the weighted geometric mean.
- **Elasticity:** the log-log slope along the surface, as defined.
- **Fit temperature τ, term temperature κ:** the sharpness of the soft maximum over designs and over terms.
- **Term share:** the fraction of near-frontier designs in a term's cell.
- **MoP, MoE:** measure of performance and measure of effectiveness.
- **Planted:** a known generating term in synthetic data.
- **Regime:** a setting of the controller gains (primary or stock).
- **Tension:** negative correlation.
- **Weakly efficient:** no design strictly better in every metric.
- **Conditioned metric:** a positive, larger-is-better transform of an attribute.

## 8. Questions I am left with

- Is the fit objective J_τ alone, or the mean slack (reach minus mean score)? Is the data centred, and does the answer depend on how it is scaled or centred per metric?
- Where does the fit temperature convention (target 10% beyond V = 1) come from, and how stable are the exponents if the target changes?
- What does an effective sample size of 23 mean for the variability of the exponents? Is there any resampling?
- How should one read an exponent on a metric that is almost a duplicate (r = 0.99) of another?
- How does the multi-term fit behave across restarts, and how often does it reach a Level 3 point?
- Is Theorem 10(ii) used to claim anything about the soft alternation?
- What is the K = 3 fraction above V = 1, and why is the K = 1 band used at every K?
- Does the negative-correlation reading of Figures 8 and 9 account for the selection effect?
- What are Q1 to Q4, and what is not monotone in the search of Section 7?
- Is the Kp, Kd range the thing that differs between the regimes?
- Which of the sum or mean convention do the figures use?

## 9. Would I read the whole paper?

Yes. The one-term mathematics is correct and cleanly stated, the guarantees are narrower than the headline, and the paper says so. Several statements depend on definitions I was not given (F, f_k, slack, centring), and the proofs for Theorems 10 to 12 are where I would check the step that matters.

The case study makes claims about elasticities and separated contending sets that I would want to test against the τ-sensitivity, the near-collinear metrics, and the small-cell terms. I would read Sections 5 and 6 and Appendix B first, then the open questions.

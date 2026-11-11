# P2-B

## 1. What this is about

As far as I can tell, the paper replaces my weighted-criteria spreadsheet with something fitted. You take a table of evaluated designs: rows are configurations, columns are performance numbers ("metrics") that have been converted so that each is positive and larger is better. Instead of me choosing weights, the method fits weights to the data. It fits a surface along the outer edge of the cloud of designs. The surface is a weighted geometric mean of the metrics, set equal to one. The fitted weights (exponents) then tell you how much of one metric you give up per percent of another along that edge. The fit can also use more than one piece ("terms"), so that different parts of the edge can have different trade-offs. Each piece then names which metrics are actually fighting each other there: two metrics is a "dilemma", three a "trilemma", n an "n-lemma".

The worked example is a cubesat attitude-control and power model with eight traded metrics: settling time, control effort, pointing error, total mass, energy balance, power margin, depth of discharge and peak slew power. The configuration variables are a few swappable parts (wheel class, tracker grade) and a few tuned parameters (panel span, battery capacity, controller gains). It is run in two controller-gain regimes, "primary" (aggressive gains) and "stock".

## 2. The main results, as I now understand them

- **The score.** Each design gets a value V, a weighted geometric mean of its metrics, scaled so that V = 1 on the fitted surface. If every metric doubles, V doubles. log V is a weighted sum of log-metrics minus an offset (the "reach"). Designs with V > 1 lie beyond the fitted surface and V < 1 inside it. The paper insists that this surface is not the Pareto frontier. It is a reference level fitted near the outer edge. Only the τ = ∞ version (the "supporting envelope") has no design beyond it.
- **The one-term fit is well behaved.** With one term, fitting the weights is a convex problem (a geometric program in log variables). Any minimum you find is the global one, but the weights may not be unique. The fit uses a "soft maximum" controlled by a temperature τ. Low τ is close to averaging, high τ is close to taking the outermost design. In the example, τ is chosen by convention so that about 10% of designs end up above V = 1. Figure 4 makes this concrete: at the chosen τ ≈ 38, five of eight metrics get weight (total mass 0.36, energy balance 0.18, pointing error 0.16, depth of discharge 0.16, settling time 0.14), and three get essentially zero. The effective sample size there is about 23.
- **The weights are elasticities.** Along the surface, the percent change of metric j per percent change of metric i is minus the ratio of their weights. The paper also gives a "how far from the surface" reading: improving one metric by the factor V^(-1/w_j), or all metrics by 1/V, brings a design to V = 1. That is an auditable sentence I could say to a programme manager.
- **A reversible coordinate change ("the chart").** Log-metrics are split into an overall level (log V) and a position along the surface, with nothing lost. The metric-conditioning step (log, shift, scale per attribute) can also be pulled back, so the weights can be read in terms of the raw attributes. A negative exponent marks a cost attribute.
- **Maximising V gives a Pareto-efficient design.** It is efficient when all weights are positive, and weakly efficient otherwise. The converse is explicitly not claimed.
- **Several terms are harder.** The multi-term fit is not convex. What they offer instead is a ladder of weaker guarantees: (1) an alternating procedure (assign each design to its best term, refit each term on its own designs) never makes the objective worse and stops in a finite number of steps; (2) a computable gap per term that bounds how far each term's refit is from its own optimum; (3) if the assignments are stable under small perturbations, the result is a local minimum, with a bound for that run only. A soft variant gets a second-order local-minimum check. Global optimality is never claimed.
- **Case-study finding.** On the cubesat, the three-term fit separates groups of contending metrics that the one-term fit blends together. Examples are a settling time / control effort group, a mass / energy group, and a pointing error / peak slew power group. In the two regimes, the one-term fit puts weight on different metrics. Stock gains weight control effort and settling time heavily and give total mass zero weight. Primary gains weight total mass most and give control effort zero weight.
- **PCA on top.** PCA of the near-frontier designs' positions gives the main direction of spread. The paper frames this as a description of the sample, not a result about the system.

## 3. What I would do next with it

I would try it on the last trade study I did with a weighted spreadsheet, using the same evaluation table. I would compare the fitted exponents with the weights the team argued about. Then I would look at which metrics come out with zero weight, and check whether that matches the engineers' sense that those metrics "never really drove anything".

Then I would test its repeatability, which is the reason I would adopt it at all. I would refresh the evaluation data (new model version, more samples, a resample of the same set) and refit. Then I would see how much the exponents and the n-lemma membership move. I would do the same sweep over τ that Figure 4 shows. Figure 4 alone tells me that the choice of τ changes which metrics carry weight: control effort is in at low τ and out from τ ≈ 25 upward. I would want that sensitivity in front of the programme manager, not hidden.

Section 11 ("Reproducibility and your own case") suggests there is a package and a recipe for running it on my own table. That section is the first one I would read.

## 4. What I would tell a colleague

"It's a way of getting trade-off weights out of the evaluated designs instead of out of a meeting. It fits a geometric-mean surface along the outer edge of your design cloud. The weights it fits are directly 'percent of this for percent of that' along the edge, and metrics that don't matter on the edge get zero. The one-piece fit is a convex problem, so two people with the same data get the same answer up to ties, which is the audit story. You do have to pick a temperature that controls how tightly it hugs the outer edge, and the answer depends on it. The several-piece version tells you which metrics fight each other in which part of the trade space, but it only gives local guarantees. It doesn't search for designs, and it doesn't do your metric conditioning for you."

## 5. What the method does not do, and what the paper does not claim

- It does not find the Pareto frontier. The fitted surface is explicitly not the Pareto boundary, and some designs sit beyond it by construction (about 10% under their convention).
- It does not claim unique weights for the one-term fit. It claims a global minimum but not a unique minimiser.
- For several terms it claims no global optimum and no convergence beyond finite stopping of the sharp alternation. It does not claim that the stopping point is stationary. The certificate is for "the returned run, not across restarts".
- It does not claim that every Pareto-efficient design maximises V. Only the other direction is claimed.
- It does not condition the metrics. The analyst chooses how raw attributes become positive, larger-is-better metrics, and the result depends on that choice.
- The association maps (Figures 8 and 9) and the PCA direction are described as readings of the sampled designs, not properties of the model or the system.
- The Gaussian cumulant result is "a population identity, with no consistency claim". So there is no statistical consistency result for the fit as an estimator.
- Design-space search (Section 7) is marked preliminary, and its monotonicity is listed as open. So the method is identification and analysis, not an optimiser for new designs.
- The stable-radius bound is sufficient, and tightness is not claimed.
- Four open questions (Q1 to Q4) are flagged, though I was not told what they are.

## 6. Where I was confused or stopped, in order

1. **Figure 1, before the caption.** The triangle with "dilemma of 1 and 2" on the edges and "planted (the known answer)" was readable as a picture. But I could not tell what the open rings meant until the caption said "planted". Term 2's dot sits just below its ring, and I could not tell whether that is a miss or acceptable.
2. **Figure 2.** I understood it as a SysML-style block diagram, and "swap" vs "tune" was clear. I had no trouble here.
3. **Figure 3.** The box "SlewExperiment … returns 7 of 8 metrics, computed with no slew: pointing error, total mass. From the measurement: control effort (passed on) and settling time (not returned)." I could not work out which seven, or why settling time is "not returned" when it is plotted as a traded metric everywhere else. The caption says the measured slew supplies settling time and control effort "which the analysis passes on". That reads as if both are passed on, which contradicts "(not returned)" in the box. I also did not see why PointingErrorRequirement being "not satisfied by cubesatBaseline" matters for the trade.
4. **Figure 4.** I could read the curves. But "the fit temperature, the temperature at which the fraction is within 0.01 of the target (a convention, Section 5)" left me unsure why 10% is the right target. I also could not tell what I would choose for my own data. "Effective sample size … n_eff = 23" out of what looks like several hundred designs worried me. Does that mean the weights rest on about 23 designs?
5. **Figure 5.** "Dark: the designs whose other six metrics, weighed by their exponents, lie within 0.1 of that median … they reach the line and stop there, a few beyond it." In the plot, plenty of dark points lie well inside the line (down to about -2.5). I expected dark points to hug the line. I think the caption means only that they do not go far beyond it, but on first look it read as a claim the picture did not show.
6. **Figure 6, top panel.** The line passes above most of the cloud but well inside many light points near the top left. Two straight streaks run diagonally from the lower left. The caption explains the streaks as torque-limited slews, which helped. But I could not tell whether the fitted line is any good here.
7. **Figure 6, bottom panel.** The term's line sits above the six horizontal bands. A large group of designs sits near -1.2 to -1.4, far inside. I could not tell whether that lower cloud (large wheel) belongs to this term at all.
8. **Figure 7.** "each design's level log V, the energy differential". Why "energy"? Nothing here is an energy in my sense, and the model also has an actual energy balance metric. The axis label "(44% of it)" I took to be the share of spread on the first principal direction.
9. **Figure 8.** "term 1: 4-lemma … Too few near-frontier designs for an association reading: 3 of ten". "3 of ten" puzzled me: three designs out of a minimum of ten? I also stopped at "an outlined metric can be grey". In term 3, energy balance is outlined but has w = 0.00. So a metric is in the "contending set" but carries no weight. Definition 6 later explains this as contending at τ = ∞ but not at the fit temperature. On first reading it looked contradictory.
10. **Figure 8 vs Figure 6.** Figure 6 says term 1 is "settling time and control effort". But Figure 8 gives no map for term 1, and Figure 8's term 2 is dominated by energy balance (0.42) and total mass (0.24), as in Figure 6. That matches. In term 3, peak slew power (0.61) and pointing error (0.23) show a -1.00 association, which matches the bottom panel of Figure 6. But peak slew power has w = 0.00 in the one-term primary fit (Figure 9) and is in the -0.95 pair there. So a metric with zero weight in the one-term fit becomes the heaviest metric in a three-term piece. If that is the point of "the terms separate contending sets that one term blends", it is the most interesting thing in the paper. I am not sure I read it right.
11. **Main results, first bullet.** "fitted to the outer edge of the data, not through its middle, it is not the Pareto boundary but the level from which every design's position and level, and each term's elasticities, are read". It took several readings to see that this is a statement about what the surface is used for.
12. **Definition 3.** "the package's mean subtracts the constant (log K)/κ from every level and changes neither exponents nor offsets". I did not know what "the package" was, or why sum vs mean matters to me.
13. **Definition 4.** I followed the two temperatures, τ (fit) and κ (between terms). But I have no feel for how to set κ, and nothing I was given says how it was set in the case study.
14. **Definition 5.** "B u, with BB^T = I and B1 = 0". I can follow the linear algebra. But calling log V "the energy differential (level offset): the level of a potential" lost me again.
15. **Theorems 10 to 12 and Lemmas 1 and 2.** These are where I stopped following in detail. "Generalized posynomial in e^w", "LP duality gap", "critical cone", "positive definite on the tangent space of the active face" are outside my training. I took away only the gist: local guarantees, a computable gap, a local-minimum check.
16. **Theorem 11.** "the sharp alternation stops within K^N + 1 iterations". With N in the hundreds, that bound is astronomically large. I could not tell whether it is meant as a practical bound or only a proof of termination.

## 7. Terms whose meaning I had to guess

- **Metric / attribute / conditioning:** attribute is the raw output of the evaluation. Metric is that output transformed (log, shift, scale, sign flip) so it is positive and larger-is-better. Conditioning is that transformation.
- **Invariant value V:** the score of a design relative to the fitted surface. I could not see what it is "invariant" to, unless it means a uniform rescaling of all metrics only shifts the level.
- **Fit temperature τ:** how close the soft maximum is to a hard maximum. Low τ averages, high τ takes the outermost design.
- **Term temperature κ:** how sharply several terms hand over to each other.
- **Reach β:** the offset that puts the surface at the outer edge in a given weight direction.
- **Near-frontier band:** designs with |log V| < 1/τ, i.e. close to the surface.
- **Cell:** the designs assigned to a term (those it scores highest).
- **Contending set / n-lemma:** the metrics with nonzero weight when a term is refit as a hard maximum on its own cell. n is how many there are.
- **Participation threshold:** a weight below 0.001 is treated as zero for the elasticity reading.
- **Chart, position Z:** coordinates along the surface with the overall level removed.
- **Energy differential:** another name for log V. I do not know why "energy".
- **Planted:** the known true answer in the synthetic test case.
- **Elasticity:** percent change of one metric per percent change of another, along the surface.
- **Effective sample size:** roughly how many designs the soft maximum is really leaning on at that τ.
- **Regime (primary / stock):** two sets of controller gains under which the whole design sample was evaluated.
- **Slack, mean slack F:** the fit's objective, roughly how far designs sit from the surface, averaged.
- **A1 to A8, F5, F10, F12, I5 to I16, R1, R2:** hypothesis labels from an appendix I did not see. I took them to be assumptions (A), facts (F), identities (I) and regularity conditions (R).
- **Lemma script / "Derived":** each theorem seems to be checked by a script. I took "Derived" to mean derived in that script.

## 8. Questions I am left with

- If I refresh the evaluation data, how much do the exponents and the contending sets move? Is there any error bar on the weights (bootstrap or otherwise)? With n_eff ≈ 23, I would expect them to move noticeably.
- Why 10% above the surface? What happens to the conclusions at 5% or 20%? Is there guidance for choosing τ on a new problem?
- How were K = 3 and κ chosen for the case study? Is there a rule for how many terms to use?
- How sensitive are the results to the conditioning choices (shift, scale, log), which the analyst makes and the method does not check?
- How would I turn the output into a decision? The paper reads trade-offs, but my programme manager wants a recommended design or a short list. Is "maximise V" the intended selection rule, or only a property?
- What are Q1 to Q4?
- In Figure 3, which metric is not returned by the analysis, and does that matter?
- Why does peak slew power get zero weight at K = 1 but dominate term 3 at K = 3? Is that the headline finding or an artefact?
- How does it compare in practice with the prior-art families in Table 1, whose body I did not see?
- What would I need to install, and how long does a fit take on a few thousand designs and a dozen metrics?

## 9. Would I read the whole paper?

Yes, selectively. The one-term fit gives me what my spreadsheet lacks: weights fitted from data, with a convex fit I can rerun and defend, and direct elasticities. That is enough to try it. I would read Sections 1, 5, 8, 9 and 11 closely, and the Discussion for the limits. I would skip most of Section 6's multi-term theory and Appendix B, because I cannot check them and would take the guarantees on trust. What would stop me adopting it is if Section 11 does not let me run it on my own table without much effort. It would also stop me if the τ and K choices turn out to be judgement calls with no guidance, since then the answer could move for reasons I cannot explain to an auditor.

# P1-B

## 1. What this is about

A method for looking at a design trade study with many competing qualities. You start with a set of candidate designs, each scored on several "metrics" (mass, energy balance, pointing error, settling time and so on, all made positive and larger-is-better). The method fits a "reference surface" to the outer edge of that cloud of designs. The surface is the level at which one number, the "invariant value" V, equals 1. V is a weighted geometric mean of the metrics, so doubling every metric doubles V. The weights (the "exponents") say how hard each quality pulls against the others. They also give exchange rates: x percent more of one metric costs y percent of another along the surface (Definition 8, Theorem 5). Figure 1 sketches the idea for three metrics. One term fitted to the data is a point in a triangle. A corner means one metric binds alone, an edge means a dilemma between two metrics, and the interior means a trilemma.

The worked example is a cubesat (a small satellite) model with eight metrics: settling time, control effort, pointing error, energy balance, power margin, depth of discharge, peak slew power and total mass (Figures 2 and 3). The paper also claims the method can use several surface pieces ("terms") where one blends different trade-offs together. It then gives guarantees about when the several-term fit can be trusted, and how far.

## 2. The main results, stated as I understand them

- V is a scale-free score. A design with V = 1 sits on the fitted surface, and V above 1 means beyond it (Theorem 1).
- The fitted surface is deliberately not the Pareto boundary (the set of designs no other design beats on every metric). It is fitted to the outer edge of the data, and it is the reference level from which positions and levels are read (Definition 1). Roughly a tenth of designs are beyond it by convention.
- With one term the fitting problem is convex, so any answer the optimiser reaches is a global best. The paper does not claim the answer is unique (Theorems 2 and 3). The exponents are exchange rates, and the "chart" (position along the surface, plus level V) is a lossless rewrite of the metrics (Theorems 5 and 6).
- A design that maximises V is Pareto-efficient, at least weakly. The converse is not claimed (Theorem 9).
- With several terms the fit is no longer convex. The paper gives three levels of assurance: a descent guarantee, a numerical "gap" measure for how near a stopping point is to optimal, and local optimality under conditions. It also gives a stopping declaration and, for the soft version, a second-order certificate (Theorems 10 to 12, Lemmas 1 and 2, Proposition 3, Corollary 1). Global optimality is explicitly not claimed.
- Running principal component analysis (PCA) on the near-frontier designs reads off which trade-offs the sampling exercised. The paper calls this a reading, not a result.
- On the cubesat, several terms separate groups of contending metrics that one term blends together (Section 9).
- Four questions (Q1 to Q4) and the monotonicity of the search are stated as open.

## 3. What I would do next with it

Ask for the cubesat case (Section 9 and Appendix D) and look at how the one-term answer changes between the "primary" and "stock" controller regimes. In Figure 9 the heaviest metrics differ: total mass at 0.36 in one regime, control effort at 0.43 in the other. I would test whether the exchange rates agree with what my own engineers know about the real trade-offs. For one of our own systems I would ask an analyst to run it on a past decision where we already know the answer, as the paper does with its "planted" three-term example. I would not commit to a design on this until someone I trust has done that.

## 4. What I would tell a colleague

"It is a way to turn a big pile of simulated designs into a small set of exchange rates between qualities, for example how much mass you give up per unit of energy balance. It tells you which qualities are in a two-way or three-way tug of war. The one-term version is mathematically well behaved. The several-term version is not, and the paper says so and offers checks. The surface it draws is a reference level, not the true limit of what is achievable, so do not read it as 'the best possible design'."

## 5. What the method does not do, and what the paper does not claim

- It does not find the Pareto boundary. The paper says the surface is not that, and that the Pareto boundary is a property of the system.
- It does not decide which design to build. Maximising V gives an efficient design, but that is one among many, and the weights come from the data and not from my priorities.
- It does not prove the several-term fit is globally best (stated explicitly), and uniqueness is not claimed even for one term.
- The PCA reading and the association maps (Figures 7 to 9) are analyses of the sampled designs, not claims about the system or the model.
- The result depends on the sample. The paper says the position axis is "a reading of the sampled designs and not part of the model", and the fit temperature is "a convention".
- It does not handle the conditioning of attributes into metrics. Metrics must already be strictly positive and larger-is-better.
- The paper does not claim a search algorithm that provably improves (monotonicity is listed as open).
- I see nothing in what I was given that tests it against a case where the true trade-off is independently known, apart from the synthetic planted example in Figure 1. I cannot tell whether the full paper does more.

## 6. Where I was confused or stopped, in order

1. Figure 1, legend: "Weight on these three metrics: 1.00, 1.00, 1.00 (all of it: d = 3)". I expected one weight, or a weight per term. The three values look like one per term, but I could not tell what "weight on these three metrics" means or why it is printed three times.
2. Figure 1, labels: "term 1: dilemma of 2 and 3 ... w = (0.00, 0.35, 0.65)". I understood that w is a weighting, but "planted" ("the known answer") only became clear on reading the caption. Before the caption I did not know the figure was a test on synthetic data.
3. Figure 2: "swap" and "tune" markers and the notation "«part def»", "«abstract»". These are systems-engineering notation. I did not need them to see that some choices are discrete (wheel size, tracker grade) and some continuous (panel span, battery capacity, controller gains).
4. Figure 3: "requirements that read no traded metric", "MoP", "MoE", "ConfigurationVerification", "SlewVerification". I could not tell the difference between MoP and MoE (I guess measure of performance and measure of effectiveness). The legend colours are clear, but the diagram has too many unfamiliar labels for me to read quickly. I also could not tell what, if anything, I should conclude from it.
5. Figure 3, in the box: "SlewExperiment ... returns 7 of 8 metrics, computed with no slew: pointing error, total mass. From the measurement: control effort (passed on) and settling time (not returned)." This contradicts itself on a quick read. It says 7 of 8 returned, then lists two items "from the measurement", one passed on and one not returned. Where the eighth metric comes from I could not work out.
6. Figure 4, left panel: "fraction of designs above V = 1" against "fit temperature tau", with "target 0.1". I did not know what a fit temperature is, and I could not tell why a tenth of designs should be above a surface called a frontier. The caption says it is a convention. That helps, but it means the 38.1 chosen is set by a rule that the 10 percent rule creates.
7. Figure 4, bottom: "exponent w (white: at most 0.001)". Three of the eight metrics (control effort, power margin, peak slew power) drop to zero at the chosen temperature. I could not tell whether that means they do not matter or the method just does not see them. Figure 3 says they are read by requirements.
8. Figure 5, legend: "designs whose other six metrics are near the median (within 0.1 in log V)". I did not follow how a picture of eight metrics is flattened to two axes. The dark points are those that sit near a common slice. The light points scatter on both sides of the line. I took the line to be a fair summary only for the dark points.
9. Figure 6, top panel: two straight diagonal streaks. The caption explains them as torque-limited slews. I could not have interpreted them without the caption. Bottom panel: horizontal bands and columns of points, nothing like a cloud. The line looks like it cuts through the middle of those bands, with many points above it and none touching it in the upper-left. I could not tell by eye that the line is a good description.
10. Figure 7: the line is at log V = 0 "whatever the position", and many designs sit well below it (down to about -1.0). The horizontal axis is "the chart's direction of most spread among the near-frontier designs (44% of it)". I did not understand what the horizontal axis is in practical terms. The caption's parenthetical "to the right, better total mass and control effort, worse pointing error" is the only usable reading.
11. Figure 8: "Too few near-frontier designs for an association reading: 3 of ten". Term 1 has only three designs near the frontier, so one of three terms in the K = 3 fit cannot be examined. I could not tell what that means for the term's reliability.
12. Figure 8 and Figure 9: the heat maps show "association (negative = tension)". I understood a negative number as a conflict between qualities. The row label "w=0.00" in grey next to a black outline (the contending set), and the caption's "an outlined metric can be grey", I could not reconcile on first reading.
13. Figure 9: the primary and stock regimes have different heaviest metrics, with total mass at 0.00 in stock. I did not know whether this should be read as "the method is sensitive to the controller gains" or as "it discovers a real change in the trade-off".
14. Headings: "Scaling Decision Analysis with Hyperbolic Trade Space Identification". I did not know what "hyperbolic" refers to. The paper never uses the word in anything I was given. The section "7 Search of the design space (preliminary)" is also unclear to me, since I do not know what is being searched.
15. Main results, bullet 1: "a weighted geometric mean of the metrics that doubles when every metric doubles". Easy. The next clause, "fitted to the outer edge of the data, not through its middle, it is not the Pareto boundary but the level from which every design's position and level... are read", I had to read twice. I took it to mean the surface is a yardstick, not a limit.
16. Main results, bullet 2: "The one-term fit is a geometric program, convex in the logarithmic variables, so every minimizer is global, though uniqueness is not claimed". I understood the consequence (no local traps) but not what "geometric program" is or why uniqueness matters to me.
17. Definition 1: "The supporting envelope is the tau = infinity fit, which none exceeds". I expected the fitted surface to be the thing designs sit under. It is not: designs lie beyond it, and the envelope is a separate object. I could not see how I would use three different surfaces.
18. Definition 3: the formula for the posynomial. Unreadable for me. "kappa", "1/kappa power of a posynomial", "term aggregation: the formula is the sum; the package's mean subtracts the constant (log K)/kappa". I skipped it.
19. Definition 5: "Z = Bu, with BB^T = I and B1 = 0". I skipped it. "Energy differential (level offset): the level of a potential relative to the fitted reference surface". I could not tell why a physics term ("energy", "potential") is used for a score.
20. Definition 6, the n-lemma: "The contending set of term k is the support (exponents above 10^-9) of the exact-maximum fit to the term's cell, centred on the cell's mean log-metric". I could not follow this. The idea from Figure 1 is that a term involving two metrics is a dilemma and three metrics is a trilemma. The paper's word for this ("lemma") is not the usual meaning, and I did not see why the paper uses it.
21. Theorems 10 to 12: unreadable to me (Jensen, KKT, Hessian, positive definite on the tangent space of the active face). Taken at face value as a stack of guarantees. I did not see which of them I would ever need to rely on.
22. Theorem 4: "Log-mean-exp against log-sum-exp". I could not tell why this one is a main result rather than a technical remark.

## 7. Terms I had to guess

- Metric: a performance quantity made positive and larger-is-better. Guess: mass is flipped to "inverse kg" (Figure 5 axis label).
- Configuration, attribute: the choices and the raw outcomes, from the caption language. Guess: configuration is the design choices, attribute is the raw outcome, metric is the outcome after conditioning.
- Invariant value V: a score scaled so that V = 1 on the fitted surface. Guess: a ratio of how good a design is relative to the surface.
- Exponent, weight: a number per metric, summing to one. Guess: the importance, which is also the slope of an exchange rate.
- Elasticity: percent change of one metric per percent change of another along the surface. I took the paper's definition.
- Fit temperature tau: how strictly the fit follows the very best designs. Low means a smoothed average, infinite means the exact maximum. Guess from the plots: low tau uses many designs, high uses few (effective sample size falls from over 500 to about 23 at tau = 38.1).
- Term temperature kappa: how sharply the terms hand over from one to another. Guess.
- Near-frontier band: the designs within a factor of e of the surface, per Definition 4.
- Term, cell: a term is one piece of the surface, a cell is the designs that piece scores highest.
- Contending set: the metrics that actually bind in a term. Guess.
- Participation threshold: 0.001, below which a metric is treated as carrying no weight at the fit temperature.
- Posynomial, geometric program: I know only that the first is a sum of power-law terms and the second is the class of optimisation problems built from them, and that they are convex after a log transform.
- Pareto-efficient: no design beats it on every metric, which I know.
- Reach (beta): how far the data extend in a direction. Guess: it sets the offset so that V = 1 sits at the edge.
- Planted: a synthetic case where the answer is built in, so the method can be checked against it.
- Regime (primary, stock): two settings of the controller gains in the case study.
- Energy differential: log V, the level of a design relative to the surface.
- Chart: the pair (position along the surface, level).
- Association: Pearson correlation of log-metrics among near-frontier designs.
- Hyperbolic: no idea. I took it as a reference to the shape of an exchange-rate curve, since a product of metrics held constant is a hyperbola.

## 8. Questions I am left with

- How sensitive is the answer to the sample of designs I feed in? If I sample differently, do the exponents move?
- How is the 10 percent target chosen, and what happens to the exchange rates if I choose 5 or 20? The captions say it is "a convention". Figure 4 suggests exponents change a lot with tau (control effort vanishes by tau = 25).
- When a metric drops to zero weight, does that mean I can ignore it in the trade? Or only that it is not binding at the edge of the data?
- Figure 9: do the primary and stock regimes give different exchange rates because the physics differ or because the sample differs? How would I know?
- Figure 6: why do the fitted lines look poor against the banded data in the bottom panel? What is the cost of that?
- What is the check, apart from a synthetic case, that this method gives the right trade-offs on a system where the truth is known?
- How many designs and how many metrics can this handle, and how long does it take? The title says "scaling" and I saw no numbers on it.
- How do I choose the number of terms K? What happens if I choose it wrongly?
- What does "the terms separate contending sets that one term blends" amount to in a decision? Does it change which design I would pick?
- What is the competing method I would otherwise use (weighted sum, Pareto plot, utility function) and where does this beat it? Table 1 exists but I only saw its caption.
- What does an auditor see? Is there a record I can point to for how a number was produced?

## 9. Would I read the whole paper?

I would read selected parts, not the whole paper. I would read Section 1 (the decision problem), the cubesat case in Sections 8 and 9, and the discussion, because those would tell me whether the exchange rates mean something for a decision I would be asked to defend. I would skip the proofs and most of Sections 3 and 4. The figures show a method that works on one worked case, and the one-term guarantee is easy to state: the optimiser cannot get stuck. What stops me from putting my name to a choice on this is that I could not see from the figures whether the answer is stable against the sample, the temperature convention, or the number of terms, and Figures 4 and 9 suggest it moves. I would read on to see whether the paper addresses that.

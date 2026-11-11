# P3-B

## 1. What this is about

A method that takes a table of candidate configurations with eight computed outcomes each (conditioned to strictly positive, larger-is-better "metrics") and fits a smooth reference surface to the outer edge of the cloud. The surface is a weighted geometric mean of the metrics, scaled so it equals one on the surface. Each design then gets a level (how far inside or beyond the surface it sits) and a position along the surface. The weights act as elasticities: percent of metric j traded for percent of metric i. With several terms, the surface becomes a patchwork of pieces, and each piece names which metrics are in contention there (a "dilemma" of two, a "trilemma" of three, and so on). The worked case is a cubesat SysML model coupling power, mass and attitude control (Figures 2 and 3), with 8 metrics, some computed and some taken from a measured slew run (simulation here, field data when fielded).

## 2. The main results, stated as I understand them

- The fitted surface is where V = 1. V is a weighted geometric mean of the metrics with weights on the simplex, so it doubles when every metric doubles. The surface is fitted to the outer edge of the data, not through the middle. It is explicitly not the Pareto boundary. Some designs lie beyond it, by convention about 10 percent. A sharper "supporting envelope" (tau = infinity) is exceeded by none.
- With one term the fit is a convex problem (a geometric program), so any minimizer is global, though not necessarily unique. The weights read directly as elasticities. The (position, level) chart is an invertible rewriting of the metrics, so nothing is lost.
- With one term, a design that maximizes V is Pareto-efficient. The converse is not claimed.
- With several terms the fit is not convex. The paper gives three levels of guarantee (a descent step, a numerical stationarity gap, a conditional local-optimality statement), a stopping rule, and a second-order certificate for the soft version.
- PCA on the near-frontier points is described as a reading of the sampled designs. It is not a result about the model.
- On the cubesat, several terms separate groups of contending metrics that a single term blends together. Some questions (Q1 to Q4) are stated as open.

## 3. What I would do next with it

I would export my model's table (configurations by outcomes), invert or condition each outcome so that larger is better and strictly positive, and run the one-term fit. I would check the exponents first, since the paper says they are the elasticities, and compare them with the trade-offs I already know from the model. I would then look at the chart of levels. I would not try K greater than 1 until the one-term picture made sense.

## 4. What I would tell a colleague

"It's a way of summarizing a big trade table as a surface with elasticities, built on top of the table our model already exports. You condition the numbers to positive and larger-is-better, and the method does not touch the model. The headline output is a set of weights per region of the frontier. The cubesat example is a SysML model, so it is close to our world." I would add that I had not yet seen what the table-to-method step looks like in practice.

## 5. What the method does not do, and what the paper does not claim

- It does not compute the Pareto boundary, and it says so (Definition 1). It does not claim that every Pareto-efficient design is a maximizer of V (Theorem 9, "The converse is not claimed").
- It does not claim a unique minimizer, global optimality for several terms, or convergence of the several-term search. Stationarity of the stop is "not claimed" in Theorem 11.
- It does not claim causal or model-level trade-offs from the association maps. They are "an analysis of those designs and not of the model".
- It does not do the conditioning of your outputs. I infer this from "conditioned" appearing in the axis labels and the phrase "conditioning is invertible" in Theorem 7.
- It does not search the design space. Section 7 is marked "(preliminary)", and monotonicity of the search is listed as open.
- It does not tell you from what I have read how many samples you need, or what to do if you have only a handful of configurations.

## 6. Where I was confused or stopped, in order

1. Figure 1, the legend "Weight on these three metrics: 1.00, 1.00, 1.00 (all of it: d = 3)". I could not work out what "1.00, 1.00, 1.00" meant. I guessed that it was the weight each term puts on these three metrics. The caption says "the weight the three carry is printed", which agrees with that guess, but I do not know what the three numbers refer to.
2. Figure 1 caption: "planted (the known answer)" and "a synthetic table with three planted terms". I did not know how a planted answer is built, or that the fit recovers it. In the picture the fitted points sit on or near the open rings for terms 1 and 3, and term 2 sits slightly off, but I do not know how close counts as close.
3. Figure 1 and Definition 6, "n-lemma": the word "dilemma/trilemma" is used for a face of the simplex. I expected a trade-off among metrics, and that is what it appears to mean. But Definition 6 defines it through the support of an exact-maximum fit with exponents above 10^-9, while Figure 1 defines it by the face that holds the fitted point. I could not tell whether those two are the same thing. Figure 4 and Figure 8 later suggest they are not always: "an outlined metric can be grey".
4. Figure 2: the labels "swap" and "tune" are clear, but "Every name is read from the system model; so are the ranges, which the view does not draw (Appendix C.1)". I expected to see ranges, and I cannot tell what the design space is. Nor can I tell how many configurations were sampled, or how.
5. Figure 3, "SlewExperiment «analysis def» returns 7 of 8 metrics, computed with no slew: pointing error, total mass. From the measurement: control effort (passed on) and settling time (not returned)". I could not parse this. My reading is that the analysis returns seven metrics. Two are computed without any slew run. Control effort comes from the measurement and is passed through. Settling time comes from the measurement but is not returned by the analysis. But then who supplies settling time to the table? The arrows do show it going straight from SlewMeasurement to the settling-time box. Does that mean the analysis returns control effort only, so that the table I would export is assembled from two places?
6. Figure 3 caption: "Every traded metric is read by a requirement, the total mass through the launch cost (yellow: derived, not traded)". I had trouble with "traded" here. It seems to mean a metric included in the trade study.
7. Figure 3, the "MoP/MoE" stereotypes. Total mass is marked MoP, launch cost MoE, and pointing error MoE. I could not tell whether the method treats them differently. I think it does not.
8. Figure 4, the top panels: "the fit temperature, the temperature at which the fraction is within 0.01 of the target (a convention, Section 5)". In the picture the chosen tau of 38.1 sits where the curve crosses 0.1, but the sweep points near it (25 and 42) are both off the line. I do not know why 38.1 is not on the sweep grid, and what it means that n_eff is only 23. The effective sample size is 23, out of how many designs? The right panel starts above 500, so I infer about 600 or more.
9. Figure 4, bottom heat map: three of eight metrics (control effort, power margin, peak slew power) have a weight of essentially zero at the fit temperature. Are these metrics simply not part of the trade, or is the fit failing to see them? Figure 9 shows control effort at 0.00 in the primary regime and at 0.43, the biggest weight, in the stock regime. That left me unsure how much to trust a zero.
10. Figure 5, "slice": the line is described as the surface with the other six metrics held at the median. The cloud in the plane clearly sits on both sides of the line, with many points beyond it. I could not decide from the figure alone whether this is a good fit. The caption says dark points "reach the line and stop there, a few beyond it". By eye the dark points do cluster toward the line from below, but I could not tell it from the light points.
11. Figure 6, top panel: the two straight streaks. The caption explains them as torque-limited slews, which was helpful. But the caption also says "No drawn pair is weighed by a second term, so no panel shows two terms meeting". I expected to see the terms meeting, since that is what the method is for. Nowhere in these figures can I see a kink between terms.
12. Figure 6, bottom panel: the dots form horizontal bands and vertical columns, which are discrete configuration choices, not a continuum. The line passes above all of the dark points. I did not understand what it means to fit a smooth surface to discrete columns of points like these.
13. Figure 7: the vertical axis is "log V: level (0 on the surface, negative inside)". There are points above zero, up to about 0.05, which the caption explains as "beyond the surface". The horizontal axis is "position along the surface: the chart's direction of most spread among the near-frontier designs (44% of it)". The position is a PCA direction of the sample, "a reading of the sampled designs and not part of the model". That is, the picture's horizontal axis depends on which designs I happened to sample. I found that unsettling for something I would set beside my model.
14. Figure 7 caption: "the energy differential" and "level offset" for log V, and Definition 5, "a potential relative to the fitted reference surface". I did not follow why this is called energy or a potential.
15. Figure 8, first panel title: "Too few near-frontier designs for an association reading: 3 of ten". Term 1 of three gets no map. The caption says a term needs at least ten near-frontier designs. That means one of three terms in the primary K = 3 fit is supported by three designs. I could not tell whether that term is meaningful.
16. Figure 8: the diagonal is outlined for five metrics, called the "contending set", and the heading says "5-lemma". In term 3, "energy balance" has w = 0.00 but is outlined, while "depth of discharge" has w = 0.02 and is not. The caption says "an outlined metric can be grey", but I did not understand why. Also, in term 3 pointing error and peak slew power have an association of -1.00. I would want to know whether that is real, or a tell-tale of one metric being a function of the other through my own model's structure.
17. Figure 9: the contending set in the primary regime has settling time, pointing error, total mass, energy balance and depth of discharge. In the stock regime it has settling time, pointing error, control effort, power margin and depth of discharge. Both are "5-lemma". I could not tell whether the difference between regimes is an actual property of the cubesat, or noise of the fit. The paper says in Section 9 that terms "separate contending sets that one term blends", and Figure 9 is K = 1, so it is not directly that claim.
18. Definition 3 (the posynomial). I could follow the "weighted geometric mean" level, but the formula with two temperatures (tau, kappa), a "reach" beta and an offset c_k = e^{-kappa beta_k} was not step-by-step for me. I did not stop completely because the surrounding words ("how hard the maximum is", "how sharply terms meet") gave me the picture.
19. Theorem 2: "R1 is a statement about the exact-maximum (tau = infinity) geometry" and the hypotheses "A1 ... A8, F5, F10, F12, I5 ... I16, R1, R2, L1 ..." are named but not given in this slice. I cannot check any hypothesis against my model. That was true for every theorem, since all of them are listed as "Derived. Hypotheses. ..." with codes.
20. Theorems 10 to 12 and Lemmas 1 and 2: stopped. These deal with the several-term fit, and I could not follow them without the proofs. I took them as statements about how much you can trust a several-term fit.

## 7. Terms I had to guess

- "Metric": a conditioned outcome, positive, larger is better. I take it from the axis labels ("inverse kg; larger is better").
- "Conditioned": a transformation of the raw outcome (inverting a cost, shifting) so that it is positive and larger-is-better. I guess it is the analyst's job, and Figure 5's axes suggest that mass was inverted.
- "Fit temperature tau": how hard the soft maximum is. Large tau approaches the strict outer envelope. Small tau approaches the mean.
- "Term": one piece of a patchwork surface, with its own weights. Not a set of designs, but the designs where it scores highest are its "cell".
- "Near-frontier": designs with |log V| < 1/tau, that is, close to the surface.
- "Contending set": the metrics that actually bind for a given term at the strict limit.
- "Elasticity": percent change in one metric per percent change in another along the surface. This one is clear.
- "Participation threshold" (0.001): below it a weight is shown as white or grey.
- "Reach": how far the data extend along a term's direction. I take it to be the offset of the surface.
- "Regime" (primary/stock): two settings of the controller gains of the same model, giving two data tables.
- "Planted": a synthetic table generated from known terms, so the answer is known.
- "Effective sample size": the number of designs that effectively influence the soft maximum.
- "Cell": the designs assigned to a term.
- "Simplex": non-negative weights summing to one.
- "Energy differential": log V. I could not place the word "energy".

## 8. Questions I am left with

- What exactly is the table I hand over: rows are configurations, columns are the eight metrics after conditioning? Is there a minimum number of rows, and does the sampling of configurations (random? grid?) matter?
- The paper says conditioning is the analyst's job. What goes wrong if I condition badly, and are there any checks on that?
- What do I do with outcomes that are measurements instead of computed values (as for settling time here), when the measurement is noisy or only available for some configurations?
- What comes back that I can set beside my model? The weights per term look usable. Does the method give me anything at the configuration level, for example "this configuration is 0.04 below the surface, improve mass by 12 percent to reach it" (Theorem 5 seems to say something like this)?
- How sensitive are the weights to the choice of tau, and to the convention that 10 percent of designs lie beyond the surface? Figure 4 shows the weights moving a lot across tau for some metrics (control effort disappears above tau about 20).
- How do I choose K? The paper says K = 1 is built, and the several-term version has weaker guarantees. Is K = 3 in Figures 6 to 8 a choice or a result?
- Do the trade-offs read from the fit hold for configurations I did not sample?
- Is a zero weight a statement about the model, or only about this sample?
- What is the fit's answer when two metrics are nearly redundant (power margin and energy balance have an association of 0.96 to 0.99 in Figures 8 and 9)? The method seems to give weight to one and zero to the other.
- Does the method run on a table with a few hundred rows, and how long does it take?

## 9. Would I go on to read the whole paper?

Yes, but selectively. The reason is that the cubesat case is a SysML model with the same structure as mine (parts, swap and tune variables, requirements reading metrics), and Figures 2 and 3 show the method has been fitted onto a model like that without changing the model. I would go to Section 11 (reproducibility and your own case), Section 5 (the methods, including the conventions on tau) and Section 9 (the case analysis) first. I would likely skip the proofs and the several-term guarantees, because I cannot follow them and my first use would be K = 1. I would hold off on trusting any several-term result until I had seen what Section 6.3's open questions say.

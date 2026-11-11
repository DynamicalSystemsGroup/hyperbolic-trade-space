# P2-C

## 1. What this is about

A paper proposing a way to analyse a table of already-evaluated design alternatives (here, 706 feasible cubesat configurations, each scored on 8 attributes) so that a trade study can be justified rather than just reported. Instead of a weighted-criteria grid or a Pareto list, you condition the attributes into positive larger-is-better "metrics", take logs, and fit a surface to the upper outer edge of the cloud. The surface is a weighted geometric mean of the metrics (one "term") or a sum of several such terms. The fitted exponents say which metrics trade against which, and at what rate (elasticities). Each design also gets a level relative to the surface (log V, "energy differential") and a position along it. The authors pitch it as a PCA-like unsupervised summary, but one that explains trade-offs rather than variance. It is delivered as a scikit-learn-style transformer with fit, transform, inverse_transform and score_samples.

## 2. The main results, as I now understand them

- Pareto dominance stops shortlisting as metrics are added. On the cubesat data the nondominated set is 126 of 706 designs on 4 attributes and 659 on 8.
- The invariant value V is a weighted geometric mean of the metrics, with weights summing to one. Doubling every metric doubles V. The fitted surface is V = 1, offset so that roughly 10 percent of designs lie above it. It is a soft upper support of the data, not the true Pareto boundary and not a regression through the middle.
- With one term, the fit is a convex problem (a geometric program in log variables). Any minimizer is global, though the paper does not claim it is unique. The exponents are elasticities: percent of metric j given up per percent gained in metric i is w_i / w_j. The chart (position, log V) is an invertible rewrite of the log metrics. The map back to raw attribute units is exact if the conditioning is log-affine.
- A maximizer of V with positive exponents is Pareto-efficient. The converse is not claimed.
- With several terms, the fit is not convex. It alternates between assigning designs to terms and refitting. The paper gives three guarantees that are weaker than global optimality: the iteration does not make the objective worse, a numerical "term gap" shows how close to stationary it is, and local optimality holds if the assignment margin is positive. A soft version has a second-order certificate. Each returned fit states which of these levels it reached.
- Case study. At K=1 the "n-lemma" (the set of contending metrics) has 5 members: total mass, energy balance, pointing error, depth of discharge and settling time. At K=3 the terms have different contending sets of 4, 5 and 5 metrics. Control effort and peak slew power each lead a term, and they were absent from the K=1 set. Term shares are 0.03, 0.24 and 0.72. On term 2 the mass versus energy-balance elasticity is -1.7.
- On 20 synthetic tables with planted terms, the fit recovers all three terms to within 0.05 in 16 of 20.
- Aggressive controller gains and stock gains give different contending sets, so the controller gains change what trades.
- A "propose, predict, check" experiment did what it was aimed at for the energy differential (3 of 3 within the band) but not for position along the surface (1 of 3). The proposals reached the frontier by shrinking the battery and so violate the depth-of-discharge requirement.
- Search of the design space (Section 7) is explicitly future work. Four questions are open: global convergence, statistical consistency, identifiability and recovery of the Pareto boundary.

## 3. What I would do next with it

I would not install it yet. I would first reproduce the cubesat result from the code the paper says exists. Then I would take one of my own past trade tables (an attribute table with a known reasonable answer) and condition it. I would run K=1 and K=2 and check whether the exponents agree with what my subsystem leads say trades off. I would also try rescaling one metric to see how fragile the contending set is, since the paper itself says rescaling changes which term is tangent. I would keep my weighted-criteria sheet in parallel for one cycle. After that I would refresh the data with new evaluations, refit, and see whether the exponent story moves in a way I can explain to a programme manager.

## 4. What I would tell a colleague

"It fits a soft upper edge to your evaluated designs in log space and reports which metrics trade against which, with percent-for-percent rates. You can rerun it on refreshed data. It is a different thing from a weighted score, because the weights come from the data's edge, not from stakeholders. It is machine-checked on the maths, but a human still has to decide whether the conditioning and the number of terms make sense. The numbers describe how the sampled designs trade, not a causal law. Expect to do a lot of conditioning work yourself."

## 5. What the method does not do, and what the paper does not claim

- It does not rank or select a design. The paper stops short of that, and says selection falls to experts.
- The surface is not the Pareto boundary. Recovery of the Pareto boundary is an open question (Q4).
- The exponents do not claim causality. They describe the sampled, conditioned designs. They do not claim sampling error either, since designed samples such as grids are not independent observations.
- Rescaling or reconditioning a metric changes the answer, so a stable result is not "context-free discovery".
- It does not do the conditioning. That is the analyst's job.
- K is the analyst's choice. Mean slack falls as K rises by construction, so it cannot choose K.
- The multi-term fit has no global optimality claim, no convergence claim, and no claim that tensions are orthogonal or that a deflation-style search works.
- It has no claim that results hold outside the table or that they support a decision. The authors name that as a third claim that needs its own validation.
- It has no claim of statistical consistency under noise (Q2) or identifiability (Q3).
- The search or sampling loop (Section 7) has no results. The kernel extension is not built.
- Which individual designs fall to which term near a seam is "not a finding". The paper says 11 of the 706 designs sit within the band of a seam.
- The hardware values are illustrative, not datasheet values.
- The paper makes no priority claim, and says it did not find the combination in the sources it reviewed.

## 6. Where I was confused or stopped, in order

1. Abstract: "Principal component analysis (PCA) is trusted as reproducible and interpretable, and explains variance. We explain tensions." I expected a sentence saying what the problem is. I could not tell from the abstract whether the method makes a decision or just describes the data. "tensions" is not defined at that point.

2. Abstract: "a soft support that a few designs may exceed, not a regression." I could not picture what is being fitted to what. Only Section 4 and Section 5 made it a minimization of the maximum of a weighted sum of log metrics.

3. Abstract: "an n-lemma (by analogy with dilemma and trilemma), with elasticities". I expected a plain list of metrics that trade. "n-lemma" reads like jargon until Definition 6 and Figure 1.

4. Section 1, "Main results (Section 6; each has hypotheses, a sketch and a script)". The bullets use theorem numbers and phrases like "convex in the logarithmic variables". As someone outside convex analysis I took them on trust. I could not tell which bullet matters for my use. The one I would care about is the cubesat result, and it is last.

5. Section 1: "Appendix D.16 reads the principal directions of the near-frontier chart ... a reading and not a result." I did not understand why this is not a result when it is the headline composition with PCA. It later reappears as Figure 7's x-axis.

6. Section 1: "counts that hold over five regenerations of the data under rounding-level perturbation; a number that moves over them is printed as a range". I expected to see a range somewhere. I met none in the main text.

7. Section 1: "Numerical: the termination status a fit reaches, read from its record." I could not parse what this bullet claims.

8. Table 1 renders as a column of lines. Column headers (Family and sources, Produces, Shares, Differs) ran into each other and some rows seemed shifted, for example the Production and distance functions row, where "Differs" and "Shares" seemed to contain "the constant-returns Cobb-Douglas form" and "Attributes in place of inputs". I could follow the idea (DEA and frontier methods are the neighbours) but not the table reliably.

9. Section 2: "A smooth soft maximum over a simplex-constrained geometric mean". I had no handle on "simplex-constrained". I guessed it means weights that are non-negative and sum to one.

10. Definition 1 (Three objects): "The fitted reference surface is V=1 at finite τ ... The supporting envelope is the τ=∞ fit, which none exceeds." This was my first real point of strain. Three things are called a frontier, and I could not tell which one the results are about. The exact-maximum fit and the soft fit are used interchangeably later.

11. Section 4: "doubling every metric doubles it. It stays the same along a trade-off, hence invariant." I did not follow how it both doubles and is invariant. I guessed it is constant along a level curve and scales with the metrics.

12. Definition 2: "V(m)=e^{-β}∏ m_j^{w_j}" and "β the reach". I could not tell what β is until Definition 7 (the soft maximum of the scores). I read forward and back.

13. Definition 3 (Posynomial) and Definition 4: the symbols κ, c_k and "term aggregation: the formula is the sum; the package's mean subtracts the constant (log K)/κ". I could not tell whether the model that was fitted is the sum or the max. Later "Sharp weights by default" suggests max (κ=∞), but the paper never tells me plainly early on.

14. Definition 4: "The near-frontier band is |log V|<1/τ: the fit weighs every design in its soft maximum, and one inside the band weighs within a factor e of one on the surface." I expected a plain statement of how wide the band is in practical terms. I could not turn 1/τ = 0.0262 into "how close in percent".

15. Definition 5 (the chart): "Z=Bu, with BB^T=I and B1=0". I understood it as a rotation that removes overall scale. I did not understand why d minus 1 position coordinates are the right ones, or what reading to give them. Figure 7 later uses a PCA direction instead, so what the Z coordinates are for was unclear.

16. Definition 6 (n-lemma): "The contending set of term k is the support (exponents above 10^-9) of the exact-maximum (τ=∞) fit to the term's cell, centred on the cell's mean log-metric ... The reading uses both". I could not work out which of the two fits (soft at τ, or exact at τ=∞) names a metric as contending. I also could not tell whether the displayed exponents come from the same fit as the membership. Figure 8 confirms they differ ("an outlined metric can be grey").

17. Figure 1 caption: "(a synthetic table with three planted terms)". The picture itself was clear once I read the legend. But "Weight on these three metrics: 1.00, 1.00, 1.00 (all of it: d = 3)" was unclear until I read the explanation.

18. Section 5, R1: "the balanced point ... lies in the relative interior of a facet of the supporting envelope with positive normal; otherwise exponents are a subgradient choice, not an identified trade-off." I stopped here. I could not tell whether R1 holds for the cubesat case. I could not find a statement that it was checked.

19. Section 5, Equation (1): I could follow J_τ as a log-mean-exp. I could not tell what "the fit asks for the positive combination of log-metrics along which the data have the smallest upper extent" means geometrically, though I could read it as "the direction in which the data's soft maximum is smallest".

20. Section 5: "τ puts a target fraction of designs above V=1: 10 percent here, a convention". I could not tell whether this means you fit τ to hit 10 percent, or that 10 percent then follows from τ. Figure 4 clarifies that you sweep τ until the fraction is about 0.10. I would have liked that sentence in the text.

21. Section 5, Conditioning: "log m_j = α_j log(a_j + s_j) + b_j ... a scaler equalizes log-spread so one τ serves every metric." I took this to mean standardizing the logs. But "rescaling one metric changes which term is tangent" is, to me, a serious sensitivity. The paper says that "a stable fitted direction answers that question and is not a context-free discovery". I could not tell how much the cubesat answer depends on it.

22. Section 6 preamble: "Derived means proved from its hypotheses by a plain-SymPy script the tests run". Then "Whether the hypotheses suit a table is a human judgment (Section 10)". I did not know how to apply that judgment to my own table, and I did not find a checklist.

23. Theorem 1 through Theorem 12 as a block. Hypothesis codes like A1, F5, I10, R1 and "Appendix B, L3.9" refer to things I do not have. Items such as "I5 (moment generating functions multiply)" were opaque. I read them as sources of standard facts. I could not tell which theorems do work for a reader like me. I took only Theorem 1, Theorem 5 (elasticity) and the Pareto statement as consequential for use.

24. Proposition 2 (Gaussian cumulant): "(1/τ)log E e^{τ w·ε} = τσ²‖w‖²/2". I could not tell where this is used later. It is "a population identity, with no consistency claim". I expected a consequence for choosing τ under noise.

25. Theorem 5: "On it d log m_j / d log m_i = -w_i/w_j" versus Definition 8, "-w_{ki}/w_{kj}". The two are the same up to the term index. But in Section 9 "the elasticity between total mass and energy balance is -1.7: along the term, one percent gained in energy balance is 1.7 percent given up in total mass". For term 2 the figure weights are 0.24 (mass) and 0.42 (energy balance), so w_i/w_j is about 1.75. This matches. But the sentence direction took me a moment, and the sign convention "negative" is described as "given up".

26. Section 6.2, "Every term is fitted against every design ... β_k=J_τ(Uw_k) is the support over all rows". Then: "Refitting a term on its own rows alone, the plain one-term fit on its cell, is ill-posed (observed on planted data, Appendix D.13); the refit of record is f_k over all rows." Yet Definition 6 defines the contending set from a fit on the cell's rows alone. I could not tell whether those are the same thing. The text says they are not the "plain fit", and that f_k on the cell's rows is a different object. I could not resolve what exactly is computed.

27. Theorem 10 (i): "a convex program symmetric in the terms attains its minimum with all terms equal, and the fit's objective ... is lower at distinct terms than at that point, so it is not convex in them in general". I could follow the intent (permuting terms gives the same value, so a convex function would be minimized at the average), but the statement is compressed.

28. Theorem 11: "stops within K^N + 1 iterations". That bound is astronomically large for N = 706. I could not tell whether it was meant as reassurance or as a formal statement. Since "convergence otherwise, are not claimed", I read it as a finite-termination statement with no practical content.

29. Lemma 2 and the stopping declaration: "At K = 3 the margin is 0.00121 and the stable radius 0.0001209, against a band 1/tau of 0.0088 ... the local optimality certified covers changes about 70 times smaller than the band, so which term those 11 designs fall to is not a finding". I stopped here. The solver reports "certified", but the certificate covers only tiny perturbations, so I could not tell how much "certified" should reassure me. The paper says as much, and I found that honest. Still, for an auditor, "certified" next to "not a finding" is confusing.

30. Section 6.2: "certified at K = 2 and 3, with the largest term gap below 1e-12". I could not judge what 1e-12 means in the units of the objective.

31. Section 6.3 Open questions: "Q4: conditions under which the fitted reference surface recovers the Pareto boundary and not the supporting envelope of the sample." This undercuts the opening sentences. If we cannot say when the surface recovers the Pareto boundary, I could not tell what a decision-maker is entitled to conclude about the real trade space.

32. Section 7: "Because evaluation is noisy, the procedure resembles a diffusion with drift along the tangent spaces." This is a metaphor in a section declared to have no results. I could not tell what it commits to.

33. Section 8: "Each configuration is evaluated once into eight attributes". Then "The primary regime evaluates 1000 designs and keeps 706 as feasible". But earlier, "launch cost" is described as a metric and then as "derived, not traded". The text says "the launch cost and the pointing error are MoEs, the other seven traded metrics MoPs". That gives eight traded metrics including launch cost, but the figure says launch cost is "derived, not traded" and the eight are controls, power and total mass. Counting: traded metrics in Figure 3 are settling time, control effort, pointing error, energy balance, power margin, depth of discharge, peak slew power, total mass: eight. So "the other seven traded metrics" refers to eight minus pointing error, and launch cost is a ninth item that is not traded. I could count it, but the sentence reads as if launch cost is traded.

34. Figure 2 (the assembly view): I could read it, but the classes, wheel class, tracker grade, panel span, battery capacity, Kp and Kd were not connected to the eight attributes, so I could not tell which design variable drives which metric. The caption says it "does not show" this.

35. Figure 3 (behavioural view): the caption sentence "the measured slew supplies the settling time and the control effort, which the analysis passes on, and the analysis computes the other six, pointing error and total mass from the configuration alone" is garbled. "The other six" and then two named seems like a mismatch. The figure box says "returns 7 of 8 metrics, computed with no slew: pointing error, total mass. From the measurement: control effort (passed on) and settling time (not returned)." I could not reconcile "7 of 8" with the labels.

36. Section 8: "the baseline configuration fails the pointing-error requirement (0.0155 against 0.0085 degree), which 63.7 % of the baseline regime's feasible designs pass." Then "The fit ignores the four; Appendix D.17 reads them after it." I expected a statement of what that implies for using the fit to meet requirements. Section 10 later says pre-imposing requirements "changes the one-term contending set by at most one of its five metrics".

37. Section 8: "so at K=1 the fit's objective of equation (2), f_1(w) = J_τ(Uw) − ū_1·w, is that of equation (1); on uncentred log-metrics the two differ by the linear term". I followed this as a technical footnote. I did not know why a reader needs it here.

38. Figure 4: I could read both top panels and the heat map. The exponent column at τ = 38.1 gives total mass 0.36, energy balance 0.18, pointing error 0.16, depth of discharge 0.16, settling time 0.14. Those sum to 1.00. But at τ = infinity (last column) the exponents look similar and control effort has dropped out. The text says the "contending set" is five metrics. I stopped on "n_eff = 23" and "rest on about 25 of the 706 designs". The text says 23.1 and then "about 25". I could not tell whether 23 or 25 is meant.

39. Figure 4 caption: "the vertical line is the fit temperature, the temperature at which the fraction is within 0.01 of the target (a convention, Section 5)". Fraction 0.092 is within 0.01 of 0.10. But in the figure the curve crosses 0.1 a little to the left of the line. I would not have picked the same point by eye. I could not tell whether it is the first or the best τ within tolerance.

40. Section 8 text: "the exponents at the fit temperature rest on about 25 of the 706 designs; the contending set holds with the target fraction halved or doubled (Appendix D.5)". I took from this that the headline exponents rest on a very small effective sample. That seems important, and it sits in a sentence beside a figure.

41. Section 8: "The worked example of Appendix C.7 has 900 rows, 4 metrics and 3 planted terms ... the 20 tables of 400 rows". Here "Figure 1 drew a three-metric table; the case plants its own". I lost track of which synthetic table is which. There are three: Figure 1's three-metric table, the 900-row, 4-metric worked example and the 20 tables of 400 rows.

42. Section 9, "A known answer ... recovers all three terms to within 0.05 in 16, at the exact maximum and at temperature 50; the 4 failures have 5, 5, 6 and 11 frontier rows on their thinnest term". I read this as evidence that thin terms are not recoverable. I could not tell what the minimum number of frontier rows is that a user needs on a term. In the case, term 1 has 3 near-frontier designs, which is fewer than every failure. So the cubesat's term 1 is probably below the point where the method recovers planted terms. The paper does not draw that connection.

43. Figure 5: The picture is clear: a downward line and a cloud with dark points stopping at the line. But "log of the conditioned total mass (inverse kg; larger is better)" has values from -3 to 2, so the numbers are standardized logs, not physical. I could not read a physical trade rate off it. Many light-grey designs lie above and to the right of the line, and the caption says "a light design above the line can be inside the surface". I could not verify that by eye, and the dark points are only some 25 percent of the total. So the figure supports "the near-median slice stops at the line" but looks like a loose fit to a reader like me. I stopped here.

44. Section 9 text: "At K = 1 the exact-maximum fit has a 5-lemma across controls, power and energy, plus mass". The same sentence says "exponents at the fit temperature from 0.14 to 0.36". Figure 4's heat map shows the τ = ∞ column with the same five metrics but different shading. I could not tell if the 5-lemma at K=1 is from τ = ∞ or from τ = 38.1.

45. Figure 6, top panel: the settling time versus control effort plane shows streaks, two straight diagonal streaks at lower left plus a loose cloud, and a black line that goes through the cloud's upper edge only in the middle section. The caption explains the streaks as torque-limited slews. I could not tell how the line is "the edge" of the dark designs there. Some dark designs sit well above the line at the left (around -1 on the x-axis, 1.5 to 2 on y). I stopped on "with the designs near its slice's median stopping at its line". The picture does not obviously show that.

46. Figure 6, middle panel: the line is far above most points, and in the right half the points sit mostly below it. I could not tell it from a loose bound.

47. Figure 6, bottom panel: the line passes above all the points on the left and falls through the cluster on the right, and there are two groups of points far below it (y of about -1.2). The caption explains stepped bands. But "term 3's elasticity is read across the swapped parts' alternatives rather than along one continuous trade" means the slope is not a continuous trade rate. That undercuts using term 3's number as an elasticity. I could not tell what a project would do with a term-3 exponent of 0.61 on peak slew power.

48. Section 9: "Each K selects its own fit temperature ... τ = 38, 94 and 113 at K = 1, 2 and 3 ...; the figures of this section and the association reading use the K = 1 band at every K (gap G-9, Appendix E)". This was a surprise. The figures use a band that does not belong to the K=3 fit. I did not know how much that matters. Figure 7's grey band is "the K = 1 fit's band as at every K".

49. Figure 7: the plot is a cloud of grey points under a line at log V = 0, with a handful of points just above it and the bulk between 0 and -0.4. I could read it as intended. But the x-axis label "position along the surface: the chart's direction of most spread among the near-frontier designs (44% of it)" is a PCA direction, and the paper says it is "a reading of the sampled designs and not part of the model". The figure title in the caption says it is "the chart of the K = 3 fit". So a figure of a K=3 fit does not use K=3 terms at all. "Does not show: terms". I could not tell what a reader learns from it except that few designs reach the surface at any position. It was also unclear that one dimension of position is shown out of seven.

50. Figure 8: I could read the heat maps. For term 2, the outlined metrics are settling time, pointing error, total mass, energy balance and depth of discharge, with w = 0.18, 0.09, 0.24, 0.42, 0.07. For term 3 the outlined set includes energy balance (w = 0.00, grey) and excludes control effort, so "an outlined metric can be grey" is visible. Term 3's peak slew power and pointing error show association -1.00, which looks like a deterministic relation (the stepped bands). The text says the K=3 contending sets are "4, 5 and 5 metrics; control effort and peak slew power, absent from the K = 1 set, each lead a term of their own". But in the Figure 8 maps, control effort is not outlined in term 2 or term 3 and has w = 0.00 in both. Term 1 has no map, so its control-effort lead (0.40) cannot be seen in any figure. So "control effort leads a term" is not visible anywhere in the figures. Also, in term 3, the metric leading by exponent (peak slew power, 0.61) is correlated at exactly -1.00 with the second (pointing error, 0.23), so the pair is one dependent quantity. I could not tell if that is a trade-off or an artefact of the swaps.

51. Section 9: "The mean slack falls from 0.243 at K = 1 to 0.182 at K = 2 and 0.146 at K = 3 ... refitted at the K = 1 temperature it falls to 0.13 and 0.09". The slack units are not given. "Mean slack falls with K by construction and cannot choose it: three terms is the analyst's choice; the finding: their sets differ." I would have wanted a way to decide K. The paper says there is none, and a user must decide.

52. Section 9: "A clustering with per-cluster correlations would describe the same designs; the terms add a model". I could not tell how I would show a sceptic that the terms beat clustering. No comparison is made.

53. Section 9: "The term shares are 0.03, 0.24 and 0.72". Term 1 has 3 near-frontier designs out of what must be about 100 (3 is 0.03). I did not know what a term with three designs carries, or whether it is real or an artefact of the seams (11 designs sit within the band of a seam).

54. Section 9, Two regimes: "The regimes return a 5-lemma and a 5-lemma sharing 3 metrics ... counting them as one, the primary regime alone has total mass, the stock regime alone control effort". The sentence "energy balance and power margin, one in each regime's own part" is unclear. "Spearman +0.98 and +0.99" is not shown in Figure 9, which gives Pearson 0.99. The paper counts the two as one metric in comparisons, and I could not see what rule says when two metrics are "nearly coincident" and may be merged.

55. Figure 9: In the primary panel, the outlined set is settling time, pointing error, total mass, energy balance, depth of discharge. In the stock panel it is settling time, pointing error, control effort, power margin, depth of discharge. The pairs differ only by swapping energy balance for power margin (correlation 0.99). So "5-lemma sharing 3 metrics" is honest. Total mass has weight 0.36 in primary and 0.00 in stock, and control effort has weight 0.43 in stock and 0.00 in primary, and in the primary panel control effort and total mass are correlated at +0.62. I could not tell if swapping a heavy metric for a correlated one is a regime change or an artefact of which one the solver picked. The paper says identical columns make the objective flat, but a correlation of 0.62 is not identical. I stopped here: "the controller gains change what trades" looks like it rests on a swap between mass and control effort, which are positively associated.

56. Section 9, Candidates: "The 3 measured candidates have lowest energy differential -0.197 and highest -0.153, and 0 of them lie beyond the fitted reference surface." I could not tell what a reader should conclude. They are named by hand, and none is on the surface. Is that good or bad?

57. Section 9, Propose, predict, check: "Propose, predict, check is a check of the regressor on a few proposals, not an estimate of a rate". I could not follow what "a proposal is the pooled configuration predicted nearest a hole of the four-metric chart, within a radius that a stated rule sets from the data: the 2nd percentile of the pool's nearest predicted distances to the 300 most isolated holes" is doing. "Hole" is never defined. I guessed it means an empty region of the chart in which the surface suggests designs could exist. "Pool" is also undefined.

58. Section 9: "Of 3 proposals, the predicted energy differential lies within the regressor's own band 1/tau = 0.0935 ... position errors run from 0.5 to 1.1 bands." Section 10 says "Two of the three proposals are one configuration." So there are two distinct designs, and the results are rates over three. The paper says they "illustrate and do not estimate a rate". I stopped here because the section is a full section of the case analysis with no usable quantitative content.

59. Section 10: "A hole in the chart is an opportunity only where the trade space is log-convex around it, which the data cannot prove." This and the novelty sentence ("V−1 says how far beyond the fitted reference surface a design lies, not whether anyone wants it") sit uneasily with "Novelty and white space. ... V−1 is a relative improvement, meaningful relative to the band 1/τ". I could not tell whether V−1 is something I can quote to a programme manager.

60. Section 10, "Three claims": the paper separates optimizer certificate, description of this table, and out-of-table validity. I could follow it and found it useful. But I could not tell how a user does the second and third on a real project. The paper offers no procedure.

61. Section 10, "Requirements after the fit ... changes the one-term contending set by at most one of its five metrics, so on this case pre-imposing the requirements does not change what the frontier trades." "At most one of five" is a change of up to 20 percent of the set, which the paper states as no change. I could not tell what tolerance is intended.

62. Section 10: "Why a frontier. An answer far from the frontier is hard to justify, and the analysis must rerun on empirical data to support configuration management." I could not tell what argument this makes. It reads as a fragment.

63. Section 10, "PCA, what the contrast does and does not claim": "K = 1 finds one tension; several regional tensions need K > 1." and "Tensions the sampling never exercised cannot appear." I could follow it. But the abstract's "the two answer different questions and compose, as when PCA is run on the chart" and Figure 7's use of PCA make the composition one step of PCA on a chart coordinate, with no tested outcome in the main text. I could not tell what composing buys.

64. Section 11: "Every figure, table and reported number comes from a call into a tested module." I could not see any code, so I could not check, but I would want it. The docsite pages are named without addresses.

65. Section 12: "Beyond ..." repeated. I read it as a list of simplifications to relax. I did not find anything that told me which of these a practitioner will hit first.

66. Section 13: "AI coding assistance ... drafted code, derivation scripts and text ... The derivations are machine-checked. The author takes responsibility." And Section 10: "Appendix B gives one line of code to read each proof step against; it cannot say that a sentence means what its line computes." I could not tell what "machine-checked" is, given that the scripts are called plain SymPy that "the tests run". I read it as symbolic checks of algebra, not a proof assistant. I would not describe it to an auditor as formal verification.

67. Reference list: the Föllmer entry has "(n.d.)" and "Unpublished notes". I noticed that and did not follow it up. The Ahmadi-Javid, Charnes 1982 and 1983, Banker and Maindiratta 1986, Hirshorn 2017 and Parnell 2021 entries are in the list but I did not find where they are cited in the main text. They may be cited in the appendices.

## 7. Terms whose meaning I guessed

- **Metric (versus attribute)**: attribute is a raw evaluation outcome with units. Metric is the same quantity after conditioning: positive, larger is better, usually standardized in log space.
- **Conditioning**: a per-attribute transform (log, flip the sign if smaller is better, shift, scale), like preprocessing in a pipeline.
- **Posynomial / monomial / geometric program**: sum of products of powers of positive variables, a single product of powers, and an optimization over such things that becomes convex after taking logs. I took the convexity on trust.
- **Simplex** (exponents "on the simplex"): non-negative weights summing to one.
- **Term / cell**: a term is one product-of-powers piece of the surface. A cell is the set of designs for which that term scores highest.
- **n-lemma**: the set of n metrics with non-zero weight on a term, read as "these n things trade against each other".
- **Contending set**: the n-lemma's members, defined from the exact-maximum fit.
- **Elasticity**: percent change in one metric per percent change in another along the term. For me, the local trade rate.
- **Energy differential / level (log V)**: a design's signed log distance to the surface in V units. Zero means on it, negative means inside, positive means beyond. "Energy" is a metaphor only.
- **Reach (β)**: the soft maximum of the scores, the offset that places the surface.
- **Fit temperature τ**: sharpness of the soft maximum. Large τ behaves like a strict maximum. It is tuned here so about 10 percent of designs lie above the surface.
- **Term temperature κ**: sharpness with which terms are combined. At κ=∞ it is a max.
- **Band 1/τ**: the width in log V counted as "near the surface".
- **Effective sample size**: number of designs that effectively set the fit, from the softmax weights.
- **Chart (Z, log V)**: an invertible rewriting of the metrics into (a position in d-1 dimensions, a level).
- **Balanced point**: the weighted average of the data's log metrics at which the fit's active weights balance.
- **Facet of the supporting envelope**: a flat face of the upper boundary.
- **Slack**: the amount by which a design's score falls below its best term's value. Mean slack is the fit's objective.
- **Term gap / margin / stable radius**: term gap measures how far a term is from stationarity. Margin is the smallest score gap between a design's best and second-best term. Stable radius is how much the fit can move before assignments change.
- **Certified (versus stationary)**: the solver's own stopping labels. They do not mean the result is correct in any wider sense.
- **Hole**: an empty region of the chart. Not defined.
- **Pool**: the set of candidate configurations from which proposals are selected. Not defined.
- **Regressor**: a supervised model from configuration to chart coordinates.
- **Association**: Pearson correlation of log-metrics among a term's near-frontier designs.
- **MoE / MoP**: measure of effectiveness, read by the stakeholder; measure of performance, read off the subsystems.
- **Participation threshold**: the 0.001 exponent below which a metric is counted as not participating.
- **Planted**: synthetic tables with a known answer.
- **Pull-back**: mapping a result in metric space back to raw attribute units.

## 8. Questions I am left with

- What does a run on my data cost? How long does the K=3 fit take for N around 700 and d = 8, and is it sensitive to starting values or restarts?
- How should I choose K, and how should I choose which metrics to condition how? The paper says only that the analyst chooses.
- How does the answer move when I rescale a metric, or when I refresh the data with new designs? That is the use case I care about. The paper reports jitter at rounding level but not the effect of adding designs or changing the sample.
- How many near-frontier designs per term are needed for a term to be trusted? The planted-table failures have 5 to 11 frontier rows. The cubesat's term 1 has 3.
- With an effective sample of about 23 designs at K=1, how stable are the exponents under resampling the table? The paper says the exponents "are not estimates with a sampling error", so how would an auditor attach any error bar?
- Does the K=1 result depend on a few metrics being highly collinear (power margin and energy balance at 0.99)? What would I do with my own collinear metrics?
- How would I explain, in a sentence, why the fitted elasticity of -1.7 is something a design change would respect, when the paper says it is not causal?
- Why is the surface fitted to an upper edge with 10 percent of designs allowed above it, rather than a quantile regression or a standard efficient-frontier estimator? The paper lists the neighbours but I could not see a comparison on the same data.
- What would an auditor accept as evidence that the hypotheses (R1, R2, A4) hold for a given table? The paper calls it human validation but gives no checklist.
- Is there a plain-language or one-page protocol for the whole workflow (condition, choose τ, choose K, fit, read the contending sets, check the claims)?
- How is the PCA composition used in practice, and what decision does it inform?
- What was the outcome of "Numerical: the termination status a fit reaches"? I could not tell what that bullet reports.

## 9. Whether I would go on to the appendices

Yes, selectively. I would want the reproducibility appendix (F) first, to find the commands and see whether I can rerun the case, and the conditioning rule of the case (C.4), because everything depends on it. I would look at the gaps ledger (E) because the main text points to it for the limits I most care about (G-9, and the four open questions). I would read D.5, D.11, D.14 and D.17, which the text cites for the stability of the contending sets, the planted recovery and the requirements. I would skip the proofs (B) unless an auditor asked, since I cannot check them myself, and the paper says the scripts do. I would decide whether to adopt the method after those pieces, mainly to see whether the sensitivity evidence supports the main text's reading and whether there is a worked procedure I can repeat.

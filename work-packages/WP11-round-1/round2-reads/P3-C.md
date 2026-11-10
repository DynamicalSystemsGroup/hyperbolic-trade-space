Cell: P3-C (persona P3, depth C); model: sonnet; date: 2026-11-10
Slice commit: c6d0fff (staged build in the stage worktree, served at 127.0.0.1:8790); reader prompt: prompts/P3-C.txt

REPORT (reader P3-C: model-maintaining MBSE engineer; answered from the briefing and its nine figures only)

1. What this is about

The paper takes a table of evaluated designs and fits a "reference surface" to the outer edge of the data. Each row is one configuration. Each column is an evaluation outcome that has been conditioned into a strictly positive, larger-is-better "metric". The surface is a piece-wise log-linear envelope, a posynomial. Each piece (a "term") has an exponent vector on the simplex.

- The metrics with non-trivial exponents in a term are said to "contend". The paper calls that group an "n-lemma".
- The exponents are read as elasticities (percent of one metric traded per percent of another).
- Every design gets a level, log V. This is its distance from the surface, negative if it sits inside.
- Every design also gets a position along the surface, in a reversible "chart".
- The pitch is that this is a PCA-like, unsupervised way to explain trade-offs, where PCA explains variance. It is meant to replace the usual weighted-criteria trade grid with something reproducible.

The worked case is a cubesat model (power, mass, attitude control). It has 8 attributes and 706 feasible designs. A synthetic table with planted terms serves as a recovery test.

2. The main result

As I read it, the headline is structural, not a single number.

- For one term, the fit is a convex (geometric) program. Exponents are elasticities, the chart is invertible, and a maximizer of V is Pareto-efficient. These are marked "Derived", meaning a SymPy script checks them from stated hypotheses.
- For several terms the fit is not convex. The paper offers three weaker guarantees (descent, a numerical stationarity gap, local optimality where the assignment margin is positive) and a second-order certificate for the soft fit.
- On the cubesat:
  - One term gives a single 5-way tension: total mass, energy balance, pointing error, depth of discharge, settling time.
  - Three terms give contending sets of 4, 5 and 5 metrics. Control effort and peak slew power, absent from the one-term set, each lead a term.
  - Dominance stops shortlisting as metrics grow: 126 nondominated designs on 4 attributes, 659 of 706 on 8.
- On planted data the fit recovers all three terms in 16 of 20 tables.

The paper says plainly that the several-term claim is only "the finding: their sets differ". It does not claim a validated engineering conclusion.

3. What I would do next with it

I would export my own model's table of configurations and evaluated attributes, which I already can do. Then I would try to do the following.

- Decide, per attribute, the orientation (smaller-is-better becomes a negative exponent in the log-affine conditioning), the shift and the scaling.
- Run K = 1 and see whether its contending set matches what I already believe drives my product family.
- Run K = 2 or 3 and look at the contending sets.
- Check whether any term's elasticities agree with the sensitivities my own analyses give.
- Try the pre-imposed versus post-imposed requirements comparison (Appendix D.17 is the place the paper says it does this).

The paper does not tell me how to run any of it. It says "use the same calls" and "the package documentation is the user's guide", and that documentation is not in front of me. So I could not start from this text alone.

4. What I would tell a colleague

"It fits a soft upper envelope to your evaluated-designs table and tells you, region by region, which metrics are fighting each other and at what exchange rate. It also gives every design a single level score relative to that envelope. It is explicitly descriptive of the sample, not causal. The conditioning step is on you, and your choices change the answer. The theory is carefully hedged, and the several-term fit comes with only local guarantees. Worth a try on a table you already have, but the paper by itself does not show the calls."

5. What I think the method does not do

The paper itself says or implies the following.

- It does not find the Pareto boundary. It fits a soft envelope of the sample, and recovering the true boundary is open (Q4).
- It does not give causal exchange rates. Exponents describe how the sampled designs trade, not what changing a variable would do.
- It does not choose K. Mean slack falls with K by construction.
- It does not say which design to pick. Selection and interpretation are human validation.
- Statistical consistency, identifiability and global convergence are open (Q1 to Q3).
- The fit says nothing about designs outside the table. The paper calls that "a third claim the certificate does not make".
- It does not do the search of the design space (Section 7 is "future work with no results").
- It does not handle discrete variables, non-log-convex structure ("dents and holes"), or kernels. These are all future work.
- It does not tell me how this connects back to my model's parameters and constraints. Configurations enter only as table rows. The one attempt, "propose, predict, check", went wrong. The three proposals (two distinct designs) reached the four-metric frontier by shrinking the battery, and all failed the depth-of-discharge requirement.

6. Where I was confused or stopped

- "It is fitted to the outer edge of the data, not through its middle: a soft support that a few designs may exceed, not a regression." What this does when my table has outliers or measurement error is not clear to me. The fit temperature is set so that about 10 percent of designs lie above V = 1. I cannot tell how sensitive the answer is to that convention, apart from a one-line claim ("halving or doubling it leaves the contending sets unchanged, Appendix D.5").
- "Open and look at this image now" order versus my reading: I read past the first six figure references before opening them, so I read Figures 1 to 6 after the text. I have no complaint about the figures themselves apart from the points below.
- "The fit temperature is tau = 38.1: a fraction 0.092 of designs lies above V = 1 ... the band 1/tau is 0.0262 and the effective sample size is 23.1 designs." An effective sample size of 23 out of 706 is a very small set carrying the fit. The paper does not discuss what that means for how much I should trust the exponents. In Figure 4 the right-hand panel shows the same value (about 23).
- Several temperatures appear that I could not reconcile. Section 6.2 says "a band 1/tau of 0.0088" at K = 3. The mean slack line says K = 1, 2, 3 are fitted "at the temperatures 38, 94 and 113". Later, "the regressor's own band 1/tau = 0.0935" would correspond to a tau near 10.7. I could not tell which tau belongs to which result.
- "The 3 measured candidates have lowest energy differential -0.197 and highest -0.153, and 0 of them lie beyond the fitted reference surface." I do not know what these 3 candidates are or where they came from. The section says only "Candidates are scored against the K = 1 fit (Appendix D.7)".
- "Of 3 proposals, the predicted energy differential lies within the regressor's own band ... for 3, and the predicted position within that band for 1". Three proposals, two of them one configuration ("Two of the three proposals are one configuration"), is too few to read anything into. The paper says so itself ("illustrate and do not estimate a rate"). Then I do not see why it sits in the main text.
- Abstract: "three terms separate the contending sets." In Figure 8, terms 2 and 3 share settling time, pointing error and total mass, and term 1 has 4 metrics. The sets overlap heavily, so "separate" is a stretch to me. I was not sure whether "separate" means "different" or "disjoint". The paper says "the finding: their sets differ".
- Figure 8, term 3 panel. Energy balance is outlined as a member of the contending set but its exponent reads w=0.00 and is grey, while power margin, with w=0.02, is not outlined. The caption says "an outlined metric can be grey", and the text says "a member can carry a small one". I followed the rule, but I still could not tell which of the two metrics is meant to be the one that contends. Power margin and energy balance correlate at 0.99, so I assume the fit picks one arbitrarily.
- Figure 8, term 1: "Too few near-frontier designs for an association reading: 3 of ten". The first of three terms has no association map. So the claim for K = 3 is supported by two maps and one sentence.
- Figure 7: the sentence on the x-axis, "Z0: position along the surface (first of seven position coordinates, meaningless alone)". The chart is 8 metrics reduced to 7 position coordinates plus a level. Plotting one meaningless axis against level leaves me unable to read a design's position. I can see only that few designs reach log V = 0 and the rest sit well below it, down to about -1.0.
- Figure 6, top panel (settling time versus control effort). The plot shows strong visible structure that the paper's text does not explain: two straight diagonal streaks at lower left, and clusters. The caption mentions grouping only for the bottom panel. In all three panels many designs lie above the line, and the caption explains this ("a design can lie above the line here and still be inside the surface"). I accept that but cannot verify it from these two-metric slices.
- Figure 5: this is the K = 1 slice of mass versus energy balance. Many designs lie above and to the right of the drawn line, and the line is far from the visible upper-right edge of the cloud. So I cannot see the "outer edge" the abstract promises. The caption again says the other six metrics are held at the median.
- Figure 9, stock panel. Settling time and control effort are correlated at -0.95. Pointing error and settling time are +0.63. Primary: pointing error and peak slew power are -0.95. I cannot tell whether such near-perfect correlation means a real physical trade or a built-in dependency (the model says the measured slew supplies both settling time and control effort, Figure 3).
- Definition 1 and the three uses of "frontier". "Three objects carry the word frontier": the fitted reference surface (V = 1 at finite tau), the supporting envelope (tau = infinity), and the Pareto boundary. In the main text the word "frontier" is also used loosely ("near-frontier designs", "four-metric frontier"). I was unsure each time which of the three was meant.
- "Hyperbolic" in the title. The text says it refers to the level surfaces of V in metric space and is "unrelated to hyperbolic PCA". I could not see where hyperbolas come from. For two metrics a level set of a product of powers is a hyperbola-like curve in linear space, which I guessed. The paper never shows or states that explicitly.
- "Definition 5 ... Z = Bu, with BB^T = I and B1 = 0". I can follow the algebra but not why this basis (called Helmert in the proof script's name) is the right one to use. Section 6 only says it is reversible.
- Theorem 12's hypotheses: "the first-order conditions hold exactly at the point, not within a tolerance". The paper reports "certified" status with the largest gap below 1e-12. I do not see how the stated exactness and the numerical tolerance meet in practice.
- "At K = 3 the margin is 0.00121 and the stable radius 0.0001209, against a band 1/tau of 0.0088 ... here 11 of the 706." This says the term assignment for 11 designs is not stable to changes above 0.00012. For me this is the practical question (how fragile are the terms to a small change in my data?) and it gets one sentence.
- Table 1 (prior art): the column text is flattened in my copy ("Shares" cells read like fragments). Several cells read as odd English (for example "the weights act as a trade-off", "Attributes in place of inputs"). I could not use the table to see the real differences from DEA or stochastic frontiers.
- Section 5 on conditioning: "a scaler equalizes log-spread so one tau serves every metric. These choices define the question". For me this is the biggest input decision. The paper gives no guidance on choosing the shift or the scale beyond "scikit-learn tools", and it says rescaling one metric changes which term is tangent. In my own model's terms: the answer depends on my units and shifts, and I have no rule.
- Section 3 pipeline: "Stages 3 and 4, identification and analysis, are the method." I never learned what the minimum table size is. The paper says "small samples determine exponents weakly" and that planted recovery fails with 5 to 11 frontier rows on the thinnest term, but it gives no guide to how many rows I need.

7. Terms I had to guess

- "Energy differential" (log V): I took it as simply a signed log-distance from the fitted surface, "by analogy with a potential". I treated it as a score, not a physical energy (the paper says so).
- "Reach" (beta): the offset, how far out the data extend in a term's direction.
- "Cell" (of a term): the set of designs for which that term gives the highest score.
- "Contending set" and "n-lemma": the metrics whose exponent is nonzero in a term; n is how many.
- "Support" (of a fit): the set of nonzero exponents.
- "Simplex" (exponents on the simplex): non-negative weights summing to one.
- "Effective sample size": how many designs effectively carry the soft maximum. I guessed it is 1 over the sum of squared softmax weights.
- "Near-frontier band": the designs with |log V| below 1/tau, that is, within a factor of about e of the surface.
- "Participation threshold" (10^-3): below this an exponent is treated as not participating.
- "Term share": the fraction of near-frontier designs in a term's cell.
- "Slack" (mean slack F): the average gap between each design and the surface along its best term; lower means a tighter envelope.
- "Association" (Figures 8 and 9): Pearson correlation of the log-metrics among the near-frontier designs. The caption says this, but I first read it as a model output.
- "Pull-back": converting an exponent back from metric units to attribute units.
- "Balanced point" (R1): I guessed the point where all active constraints share equal weight; I did not work out the formal meaning.
- "Ridges" and "kinks": where two terms meet and the surface bends.
- "Kernel" (as an extension): I guessed it means richer feature maps in place of raw log-metrics, while keeping the programs geometric.
- "GGP / generalized geometric programming": a convex-after-transformation optimization class; I know the name from the Boyd tutorial but not the technical conditions.
- "MoE/MoP" (Figure 3): measure of effectiveness and measure of performance; I know these from systems engineering and the figure defines them.
- "Hole in the chart": a region of the position-level chart with no designs, flagged as a possible opportunity.
- "Planted table/term": a synthetic table generated from known exponents, used to test recovery.
- "Fit of record" and "environment of record": the specific configuration the reported numbers come from.

8. Would I go on to the appendices

Yes, selectively, for four things.

- Appendix C. I need the model description and the dataset names to see how the 8 attributes and the conditioning were set up, since that is the part I would copy for my own model.
- Appendix D.17. This is the reading of the model's four requirements after the fit. It is the closest the paper comes to connecting the fit to my requirements, which is what I would act on.
- Appendix D.11 and D.14. I want to see how stable the digits are, and what recovery looks like on small frontier counts.
- Appendix E, the gaps ledger. It states for each assumption what cannot be proved.

I would skip Appendix B's proofs, since I cannot judge them. I would read a line or two of the scripts only to check what a quantity is computed from. I would also look for an Appendix F entry or the package documentation that gives the actual calls and input format, because without that I cannot run the method.

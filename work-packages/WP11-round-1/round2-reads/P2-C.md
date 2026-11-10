Cell: P2-C (persona P2, depth C); model: sonnet; date: 2026-11-10
Slice commit: c6d0fff (staged build in the stage worktree, served at 127.0.0.1:8790); reader prompt: prompts/P2-C.txt

REPORT (reader P2-C: practising systems engineer, spreadsheet/Python/regression background, no convex analysis or GP)

I read the whole main text and opened all nine figures. Figure 1 through 6 I opened after reading their surrounding text rather than at the point of the instruction, because my first read of the briefing was truncated. This affects only when I saw them.

1. WHAT THIS IS ABOUT

It is a proposal to replace the weighted-criteria trade matrix with a fitted model of a table of evaluated designs. You start with configurations (design choices) that have been evaluated into attributes. You condition the attributes into "metrics" (positive, bigger is better, put on comparable log scales). The method then fits a "reference surface" to the outer edge of the data. It is not a regression through the middle. Each flat piece of that surface (a "term") has a set of exponents, one per metric. Those exponents are read as exchange rates: "percent of metric j given up per percent of metric i gained". The set of metrics that actually have non-zero exponents on a piece is called an "n-lemma" (dilemma, trilemma, 5-lemma). Each design also gets two numbers. One is a position along the surface. The other is a level relative to the surface, called "log V" or the "energy differential" (zero on the surface, negative inside, positive beyond). The authors position it against PCA: PCA says where the data vary, this says what trades against what. The worked example is a cubesat model with 8 metrics and 706 feasible designs. A planted synthetic table, where the answer is known, checks that the fit can recover it.

2. THE MAIN RESULT

As I understand it, the result has three layers.

(a) Mathematical. The one-term fit is a convex problem, so it has a single answer that does not depend on the starting point. The several-term fit is not convex. It comes with "three levels of guarantee": it descends, it can be checked for stationarity, and it is a local optimum if the assignment of designs to terms is stable. A "soft" version has a second-order certificate. All of these are marked "Derived" (proved by a script) and are conditional on stated assumptions.

(b) Cubesat. One term (K=1) gives a single 5-way tension: total mass, energy balance, pointing error, depth of discharge, settling time, with exponents 0.14 to 0.36. Three terms give three different contending sets of 4, 5 and 5 metrics. Control effort and peak slew power each lead a term, and neither appears in the one-term fit. So the one-term answer blends trade-offs that three terms separate. The baseline regime (stock controller gains) gives a different 5-way set from the aggressive-gain regime, sharing three metrics.

(c) The claim about Pareto sets. The nondominated set holds 126 of 706 designs on 4 attributes and 659 on 8, so dominance stops shortlisting. The fit instead gives structure. A maximizer of V is Pareto-efficient, but the converse is explicitly not claimed.

Recovery on planted data: 16 of 20 tables recover all three terms to within 0.05. The 4 failures had few frontier rows on the thinnest term.

3. WHAT I WOULD DO NEXT WITH IT

I would take one of my own existing trade tables, with a few dozen to a few hundred evaluated configurations and 4 to 8 criteria. I would write down, for each criterion, the conditioning rule (direction, shift, scale) and check what rescaling does. I would run K=1 and then K=2 or 3 and compare the contending sets with what my subject experts already believe. I would perturb the data (drop 10 percent of the rows, rerun, change the target fraction above the surface) to see whether the sets are stable. Then I would put the pipeline in a script and rerun it when the models change. Before anything else I would try the planted-data test on a case shaped like mine, to see whether the fit recovers something I know. I would not use the results to make a recommendation to a programme manager until I could explain the exponents without the maths.

4. WHAT I WOULD TELL A COLLEAGUE

"It's a reproducible, rerunnable alternative to hand-assigned weights. Instead of asking stakeholders for weights, it fits an upper-edge surface to the data and tells you which criteria actually trade against each other, and at what rate, in different regions of the design space. The cubesat case shows one blended tension splitting into three distinct ones. It's a fitted model, so it needs your judgment on conditioning and on how many terms to use, and the authors say plainly that the exponents describe how the sample trades, not what would happen if you changed a variable. It does not pick a design. The reproducibility story sounds strong (scripts, pinned environment, tests), though I haven't seen the appendices to check it."

5. WHAT I THINK THE METHOD DOES NOT DO

- It does not choose a design or rank candidates for a decision. The paper says selection "falls to experts".
- It does not give causal trade-offs. "They describe how the sampled designs trade, and not a causal exchange that changing a variable would reproduce."
- It does not choose K. "Mean slack falls with K by construction and cannot choose it."
- It is not the Pareto boundary, and the converse (every efficient design maximizes V for some weights) is not claimed.
- It gives no uncertainty on the exponents. Figure 8 "Does not show: ... the exponents' uncertainty". The paper lists statistical consistency under noise as open (Q2).
- It does not handle requirements before the fit. They are read after it.
- It does not handle non-log-convex structure (dents, holes), and gives no global guarantee for several terms.
- Search of the design space (Section 7) has no results.
- Rescaling a metric changes the answer, so the output depends on conditioning choices. The paper says so.
- Grid-style designed samples are described as not independent observations, so the exponents "describe the sample".

6. WHERE I WAS CONFUSED OR STOPPED

- "The fitted reference surface is where the invariant value, a weighted geometric mean of the metrics that doubles when every metric doubles, equals one". I understand the arithmetic but not why this is the right object to want. The motivation for a geometric mean (rather than a weighted sum) is never given in plain words.

- Abstract: "Modelling a single n-lemma fits a monomial, which transforms into a convex program and is solved directly; ... posynomial, compatible with generalized geometric programming (GGP)". I could not follow this and it never says what I would lose or gain by caring.

- "Definition 1 (Three objects)": "The fitted reference surface is V=1 at finite τ ... some designs lie beyond it. The supporting envelope is the τ=∞ fit, which none exceeds. The Pareto boundary is the nondominated set". I could tell the three apart. It was unclear which one the cubesat figures show, and the paper's own open question Q4 ("conditions under which the fitted reference surface recovers the Pareto boundary and not the supporting envelope of the sample") says it is not known which one you get.

- "τ puts a target fraction of designs above V=1: 10 percent here, a convention". Fit temperature τ was never explained in practitioner terms. I could not tell how I would pick it for my own data beyond "target 10 percent".

- "At K = 3 the margin is 0.00121 and the stable radius 0.0001209, against a band 1/tau of 0.0088 and a median best-minus-second-best score of 0.237: a margin below the band puts at least one design within the band of a seam, here 11 of the 706, and the certificate covers changes under the radius only." The numbers are given but I could not tell whether this is good or bad news. Reading it, the certified result is fragile to a change of about 0.0001, which sounds tiny. Yet the same paragraph elsewhere says the status is "certified". Also, 1/tau is 0.0088 here but 0.0262 at the K=1 temperature (38.1), and 0.0935 in the propose-predict-check paragraph; I could not tell these are different temperatures for different fits.

- "Mean slack falls with K by construction and cannot choose it: three terms is the analyst's choice". For a practitioner this is the most important unanswered practical question. How do I choose K? Section 12 says "selection rules" are future work.

- "A clustering with per-cluster correlations would describe the same designs; the terms add a model". Not argued beyond that sentence. A skeptical colleague would say "so why not just cluster and compute correlations?" I would want a concrete example of a decision that comes out differently.

- Figure 5 caption: "the other six metrics are held at the median of the near-frontier designs, so designs off that median fall on either side of it." In the plot most designs sit below or left of the line, but some sit above it (upper left, around log mass -0.5 to 0). I could not read how many designs are really above the surface from a slice. The caption itself says "a design above the line here can be inside the surface", so the figure cannot confirm or deny that the surface fits the data.

- Figure 6, top panel (settling time and control effort). Two distinct straight diagonal strips of designs run up to the right from the lower left, and many designs lie far from the term 1 line. The caption does not explain these strips. The bottom panel is explained (tracker grades, wheel classes), the top is not. Also the term 1 line in the top panel is shown as a single straight line with no visible kink, though the caption says "one straight segment per term" and "the kink where two meet". I do not see a kink in any of the three panels. Each slice shows only one term's segment, so the claim "Good for: seeing that the surface bends" is not what I saw.

- Figure 6, bottom panel. The term 3 line sits visibly above most of the designs; only the top row of points touches it. Pointing error and peak slew power form discrete bands. I do not see how a straight line is a meaningful frontier through points like these.

- Figure 7 caption: "Z0, the first of seven position coordinates, meaningless alone". A plot whose horizontal axis is stated to be meaningless alone is hard to use. What I can read: most designs have log V between 0 and -0.6, a few reach just above 0, and none exceeds about 0.05. I cannot tell from this figure what to do with any design.

- Figure 8, term 1: "Too few near-frontier designs for an association reading: 3 of ten". One of the three terms has no map, so the headline claim ("three terms separate the contending sets") rests on two association maps plus a number.

- Figure 8, term 2 and term 3. Outlined metrics and printed exponents disagree in ways that confused me. Term 3 outlines "energy balance" (w = 0.00, grey) but not "power margin" (w = 0.02), and term 2 has depth of discharge outlined with w = 0.07. The caption says an outlined metric can be grey, but I could not tell what to conclude: is energy balance in the n-lemma for term 3 or not? Also the text says the K=3 sets are "4, 5 and 5 metrics" and "control effort ... lead a term of their own", but control effort shows w = 0.00 in terms 2 and 3, so it must be term 1, and I cannot check that because term 1 has no map and no exponent table.

- Figure 8, term 3. Pointing error and peak slew power have an association of -1.00. A perfect negative correlation between two metrics is suspicious. It probably reflects the discrete bands seen in Figure 6, not a continuous trade-off, so reading it as an elasticity is questionable.

- Figure 9. Power margin and energy balance have an association of 0.99 in both regimes. Two nearly identical columns are both candidate members of a 5-lemma. In the stock regime power margin has w = 0.18 and energy balance 0.02; in primary the reverse (0.00 and 0.18). The text says the regimes "share 3 metrics" and that "the primary regime alone has energy balance". Given the 0.99 correlation I would call that a swap of one for the other, not a difference. This looks like the exponent being carried by whichever of two redundant metrics happens to win, which Figure 4's caption acknowledges ("carried by another metric").

- Section 8: "the launch cost and the pointing error are MoEs, the other seven traded metrics MoPs". Launch cost is described in Figure 3 as "derived, not traded", so "other seven traded metrics" next to launch cost is confusing. Of eight traded metrics, one (pointing error) is an MoE, so seven are MoPs; launch cost is not one of the eight.

- Section 8: "The planted table has 900 rows, 4 metrics and 3 planted terms" versus Section 9: "On 20 planted tables (400 rows, 4 metrics)". These are probably different tables but are not distinguished.

- Section 9: "The 3 measured candidates have lowest energy differential -0.197 and highest -0.153, and 0 of them lie beyond the fitted reference surface." I did not know what the candidates are or where they came from (a pointer to Appendix D.7 only). Also "Of 3 proposals ... within the regressor's own band 1/tau = 0.0935 of the measured one for 3, and the predicted position within that band for 1". With three proposals, two of which are the same design, there is nothing to conclude. The paper says as much ("illustrate and do not estimate a rate"), but a reader still has to decide why this paragraph is in the Results.

- Section 9: "they reached the four-metric frontier by spending the battery". A practitioner would read this as a failed demonstration. The proposals violate a requirement the fit ignores. The paper reports that honestly.

- Section 10: "Fitting first and reading the requirements after ... pre-imposing the requirements does not change what the frontier trades." Fine, but it applies to the one-term set only, and "at most one of its five metrics" could be a 20 percent change in the answer.

- Section 6.1 headings and boxes: "Derived. Hypotheses. A1 (metrics positive), A2 ..." with "I10: first-order conditions", "I14 (Jensen)" etc. These labels (A1, R1, F12, I8, L5.25) are never explained in the main text; the reader is sent to the appendices. As an engineer who cannot read the proofs, I got nothing from Section 6 beyond the statements in prose, and some of those (Theorem 2, Theorem 10, Lemma 2) I could not read at all.

- "Theorem 12 ... Hessian H = D - κM ... positive definite on the tangent space of the active face". This is where I would have wanted a sentence saying what the practitioner can conclude. The paper does say "the optimizer reached a local minimizer of the objective is the certificate", which I took as enough.

- "Three claims ... That the fit holds for designs outside the table, or supports a decision, is a third claim the certificate does not make". This is honest, but it means there is currently no validated claim that the method improves a decision. I was left wondering what evidence would count.

7. TERMS I HAD TO GUESS

- "Conditioning": preprocessing that turns an attribute into a positive larger-is-better metric (shift, scale, log). Guessed from "log-affine ... α_j log(a_j + s_j) + b_j".
- "Reach β": the level of the data's upper edge along a direction, so the offset that places the surface. Guessed from "soft maximum of their scores".
- "Soft maximum / log-mean-exp / entropic": a smooth version of "max" that weights designs near the top more heavily, with τ controlling how smooth it is. Guessed.
- "Temperature τ and κ": τ is how sharply the fit focuses on extreme designs; κ is how sharply terms meet. Guessed.
- "Energy differential": signed distance in "level" to the surface, effectively a log-ratio of a design's value to that of a surface design (log V). Guessed.
- "Chart": the two-part coordinates (position Z, level log V), reversible so no information is lost. Guessed.
- "Term" (a monomial term): one flat piece of the surface; its "cell" is the set of designs for which that term is the largest. Guessed.
- "n-lemma": the count of metrics with non-zero exponent on a term. The paper defines it ("support of the exact-maximum fit"), but I had to guess what "exact maximum" means: the τ=∞ limit, which the paper says is a linear program.
- "Support": the set of metrics with non-zero (above 1e-9) exponents. Guessed.
- "Simplex": exponents are non-negative and sum to one, i.e. weights. Guessed.
- "Posynomial / GGP / generalized posynomial": a particular sum-of-power-products class of function that optimization software can handle. I never needed more than this.
- "Slack" / "mean slack": the average gap between each design and the surface it is compared with; lower means a tighter fit. Guessed from F(W).
- "Effective sample size" (n_eff): number of designs that effectively carry the fit, 23.1 of 706 at τ = 38.1. Guessed.
- "Near-frontier band": designs within |log V| < 1/τ of the surface. Defined.
- "Margin / stable radius": how far the fit parameters can move before some design flips its assigned term. Guessed.
- "Certified / stationary": a label the solver attaches to a returned fit. Guessed as a convergence tag.
- "MoE / MoP": measure of effectiveness (stakeholder-facing) and measure of performance (subsystem-facing). Defined in the text.
- "Pull-back to attribute units": translating results from log-metrics back to the original units. Guessed.
- "Deflation-style search": successive extraction of components, as in PCA. Guessed.
- "Hole in the chart / white space": a region of the chart with no designs, a candidate for new designs. Guessed.
- "Planted": generating synthetic data from known exponents to test recovery. Defined by context.

8. WOULD I GO ON TO THE APPENDICES?

Yes, but selectively and for specific reasons. I would not read the proofs (Appendix B); I cannot check them and the paper already says each has a machine-checked script. I would read:
- Appendix D.5 (the effect of halving or doubling τ), D.11 (the "digits that hold" under perturbation), D.13 and D.14 (planted data, the four failures), and D.8 (the status declaration), because these tell me whether the answer is stable and how the method fails.
- Appendix D.15 (refit at the K=1 temperature) and D.17 (the requirements priced after the fit), since I would need these for a defensible narrative.
- Appendix C (the model, datasets and generator) and F (reproducibility: the commands, the pinned toolchain), since I would have to rerun this on my own data.
- Appendix E (the gaps ledger), because it records for each assumption what cannot be proved, which is what I would have to say to a programme manager.
- Appendix A (notation) for the terms I guessed at.
I would skip G (prior art) at first. I would stop reading if the appendices did not answer the question the main text leaves open: how to choose K, τ and the conditioning for a table that is not the cubesat, and how to show a reviewer, in plain language, why a recommendation changed when the data changed.

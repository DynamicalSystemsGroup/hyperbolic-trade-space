Cell: P4-B (persona P4, depth B); model: default (the session's default model); date: 2026-11-10
Slice commit: c6d0fff (staged build in the stage worktree, served at 127.0.0.1:8790); reader prompt: prompts/P4-B.txt

Report from the P4-B reader (machine-learning engineer; scikit-learn and PCA background; no systems-engineering or aerospace experience). Written from the briefing alone: nine figures with captions, the section headings, the main-results list and the boxed statements. Proof sketches, scripts, the body text and Table 1 were withheld.

---

## 1. What this is about

You have a table of candidate designs. Each row was scored on d metrics that have been massaged so that every one is strictly positive and larger is better (the paper calls this "conditioned"; the cubesat case has eight such metrics, from total mass to pointing error). Work in log-metrics u = log m. The paper fits a reference surface to the upper boundary of that cloud, not to its middle.

The one-term model is a weighted geometric mean V(m) = prod_j m_j^{w_j} with w on the probability simplex, so log V = w·u − β is a linear functional of the log-metrics minus an offset. The surface is V = 1. The fit chooses w to minimize a temperature-τ soft maximum (log-mean-exp, Theorem 4) of the scores w·u_i over the designs; at τ = ∞ this is "find the direction on the simplex in which the cloud extends least far," an LP whose solution is a sparse w (the "contending set"). Theorem 3 says the objective is convex in w; Theorems 2 and 3 together say it is a geometric program. The exponents w are then read as exchange rates between metrics along the surface (Definition 8, Theorem 5): d log m_j / d log m_i = −w_i/w_j.

The several-term extension (Definition 3) replaces the single linear functional by a second soft maximum, at temperature κ, over K such functionals: Φ_K(u) = (1/κ) log Σ_k exp(κ(w_k·u − β_k)). Each term owns a "cell" (the designs for which it is the largest term) and is fit on that cell; the algorithm alternates assignment and refit. That is Lloyd's algorithm with hyperplanes instead of centroids, and the guarantees are the ones you expect for Lloyd: monotone objective (Theorem 11), a KKT-gap stopping certificate per term (Lemma 1), local optimality on a neighbourhood where no assignment flips (Lemma 2, Proposition 3), and no global claim (Theorem 10 says the joint problem is not convex).

The "chart" (Definition 5, Theorem 6) is a fixed orthogonal change of coordinates on log-metrics: Z = Bu where B's rows are orthonormal and orthogonal to the all-ones vector, paired with log V. It separates "where along the surface" (Z) from "how far from the surface" (log V) and is exactly invertible. That is a centered-log-ratio-style projection, not a data-driven basis; the data-driven content is w and β.

Placement next to my tools: PCA on log-metrics finds the directions of greatest spread in the cloud. This finds the supporting hyperplane of the cloud's upper boundary, restricted to nonnegative normals that sum to one. PCA's loadings are about variance; these exponents are about what the best designs give up for each other. The nearest things in my kit are a one-class/support-vector boundary with a very specific (simplex-constrained, linear-in-log) hypothesis class, and for K > 1, k-planes or hinging-hyperplane fitting. The paper itself says PCA comes after the fit, applied to the chart of the near-frontier designs, as a reading rather than a result (main results list, Appendix D.16).

## 2. The main result

As I read it, the result is a package of three things, in decreasing order of strength:

(a) The one-term fit is convex (Theorem 3) and its outputs have clean interpretations: exponents are elasticities (Theorem 5), the chart is a bijection (Theorem 6), conditioning can be pulled back to the raw attributes (Theorem 7), and a maximizer of V is Pareto-efficient (Theorem 9, with the converse explicitly not claimed). Theorem 1 is the homogeneity property that gives the surface its name: scale every metric by k and V scales by k.

(b) The several-term fit is a well-behaved heuristic with graded certificates: descent, numerical stationarity with a bound on the suboptimality of each term (Lemma 1 and Corollary 1, "for the returned run, not across restarts"), and local optimality under assignment stability. A second-order certificate for the soft version (Theorem 12) splits the Hessian into within-term curvature minus κ times a between-term ambiguity matrix.

(c) Empirically, on the cubesat, one term blends everything (Figure 4: total mass 0.36, then energy balance, pointing error, depth of discharge, settling time at 0.14 to 0.18, three metrics at zero), while three terms separate distinct trade-offs (Figure 8: term 3 is dominated by peak slew power 0.61 against pointing error 0.23, with a correlation of −1.00 between them; term 2 is energy balance 0.42, total mass 0.24, settling time 0.18). The paper's own one-line version is "the terms separate contending sets that one term blends."

What I take away as the actual contribution is (a) plus the engineering decisions around it (the log-mean-exp rather than log-sum-exp so β is scale-free; the near-frontier band |log V| < 1/τ; the two thresholds that define "in the support" versus "participating"). (b) is competent but standard. (c) is a demonstration, not evidence of generality.

## 3. What I would do next with it

- Wrap it as a scikit-learn transformer and run it in a pipeline. fit(X) on log-metrics or metrics; transform returns the chart columns (Z, log V); inverse_transform exists by Theorem 6; score_samples is log V. The cubesat Figure 7 is essentially a residual plot of that transformer. I would want parameter names for τ, κ, K and the aggregation, and a check that negative inputs are rejected.
- Planted-truth recovery first (Figure 1 suggests the authors did this): synthesize data with known w, vary N, noise and τ, and measure recovery of the support and of the exponents. Then a sweep of K with restarts, because nothing in the slice tells me how K is chosen.
- Run the obvious comparison: PCA on log-metrics of the full cloud, PCA on the near-frontier chart as Appendix D.16 does, and the fitted w, on the same data, to see what each picks up. I expect the first principal component to track the biggest trade-off only when the sampling was dense along it, which is what the caption of the main-results bullet seems to warn about ("the trade-offs the sampling exercised").
- Try it on something I have: hyperparameter-search results with accuracy, latency, parameter count and training cost as the metrics. Those are positive, larger-is-better after inversion, and the question "what is the exchange rate between latency and accuracy among the good runs" is exactly what the exponents answer.
- Stress the collinearity case. In Figure 9 power margin and energy balance have correlation 0.99; in the primary regime energy balance takes w = 0.18 and power margin 0.00, while in the stock regime power margin takes 0.18 and energy balance 0.02. That looks like the weight bouncing between two nearly identical columns, the same instability you get from an L1-style sparse solution with correlated features. I would want to know whether the paper treats that as a feature (one of the pair is enough) or as something to regularize.

## 4. What I would tell a colleague

"It is a convex way to fit a Cobb-Douglas-looking surface to the top edge of a point cloud in log space. You get a weight vector on the simplex; the ratios of the weights are the exchange rates between metrics along that edge, and the fit is sparse at zero temperature so it also tells you which metrics are actually in tension. There is a change of coordinates that splits each point into position-along-the-edge and distance-from-the-edge, and it is exactly invertible. The multi-piece version is k-planes with Lloyd-style guarantees, nothing more. It is not PCA and it is not a Pareto-front estimator; it sits between them. The case study is a satellite with eight metrics and a lot of SysML, which you can skip if you only want the method."

## 5. What I think the method does not do

- It does not estimate the Pareto boundary. Definition 1 is explicit that the fitted surface, the τ = ∞ envelope and the Pareto boundary are three different objects, and Theorem 9 only goes one way.
- It does not model the map from configuration to metrics. There is no surrogate, no prediction of metrics for a new configuration, and the "Search of the design space" section is marked preliminary.
- It makes no statistical claim. Proposition 2 is "a population identity, with no consistency claim"; nothing in the slice gives sampling variability of w, confidence on the support, or a test for whether a metric belongs in the contending set. The association maps (Figures 8 and 9) are described repeatedly as "an analysis of those designs and not of the model."
- Its outputs depend on how the designs were sampled. The main-results bullet on PCA says so directly, and the near-frontier counts in Figure 8 (term 1 has three designs) show how thin the evidence for a term can get.
- τ selection is a rule of thumb: Figure 4 picks the first τ at which the fraction of designs above V = 1 reaches 0.1. I did not see where 0.1 comes from or what happens to w under a different target. The exponents in the heatmap are fairly stable from τ = 25 upward, which is reassuring but not a procedure.
- K selection is not in the slice at all.
- No global optimum at K > 1, and the certificates are per run.
- Conditioning is out of scope. Metrics have to arrive positive and larger-is-better; the paper pushes that to the analyst and gives a pull-back theorem for the affine-log case only (Theorem 7).

## 6. Where I was confused or stopped

- Main results: "PCA and the fit are chained: the principal directions of the near-frontier chart read the trade-offs the sampling exercised, a reading and not a result (Appendix D.16)." This is the sentence I most wanted, and it is one line pointing at an appendix. I could not tell from it whether PCA is applied to Z only, to (Z, log V), or to the raw log-metrics of the near-frontier designs, nor what "the sampling exercised" means operationally.

- Theorem 2: "Balanced hard-support geometry does not imply an interior minimizer at finite τ." I do not know what "balanced hard-support geometry" is. I stopped here.

- Theorem 10 (i): "a convex program symmetric in the terms attains its minimum with all terms equal, so the objective over all terms is not convex in them in general". I eventually read this as a symmetry argument (if the joint objective were convex and permutation-symmetric, averaging a solution over permutations could not hurt, so all terms would coincide; since distinct terms do better, it is not convex), but the sentence as boxed does not say that and I was not sure I had it right.

- Theorem 11: "step B, unpenalized, with support offsets β_k = J_τ(Uw_k) and each refit an exact minimizer of f_k." Step B of what? There is no step A in the slice, and "unpenalized" implies a penalized variant exists somewhere.

- Definition 3: "Term aggregation: sum by default, or mean; the formula is the sum." I could not tell what the mean variant would change or why it is mentioned if the formula is the sum.

- Figure 4 caption: "the vertical line is the fit temperature, where the fraction first meets the target." Target 0.1 of designs above V = 1 is presented as given. I stopped to ask why 0.1 and whether a different target would change the ranking of the exponents; the heatmap suggests not much above τ = 25, but the caption does not address it.

- Figure 8, term 1: "Too few near-frontier designs for an association reading: 3 of ten" against Figure 6, top panel, where "term 1" labels a line with a dense cloud of designs along it. The caption of Figure 6 warns that "a design can lie above the line here and still be inside the surface," which I think resolves it (the slice holds six other metrics at a median, so proximity in the picture is not proximity in eight dimensions), but it took two passes and I am still unsure how a term is fit on a cell that has only three near-frontier designs in it. I assume the cell is larger than its near-frontier subset.

- Figure 7 caption: "Z0, the first of seven position coordinates, meaningless alone". If the horizontal axis is meaningless alone I did not see what the figure shows beyond a histogram of log V turned sideways. I suspect the point is that the band is thin and most designs sit below it, but I would have taken the same from a one-dimensional plot.

- Definition 6: "the support (exponents above 10^-9) of the exact-maximum fit" alongside Figure 4's "a white cell is an exponent at most 0.001 (the glossary's participation threshold)" and Figure 8's "grey below the participation threshold, so an outlined metric can be grey". Two thresholds, two fits (τ = ∞ for the support, finite τ for participation). I followed it, but in Figure 8 term 2 energy balance is outlined with w = 0.42 while power margin, correlated 0.96 with it, is unoutlined at 0.00, and in term 3 the roles flip (energy balance outlined but grey at 0.00, power margin unoutlined at 0.02). I stopped to work out that "outlined" and "dark" are answering different questions and that near-duplicate metrics can land on either side of each.

- Figure 3 as a whole. The notation («MoP», «MoE», "SlewVerification", "ConfigurationVerification", «analysis def») is from a modelling language I do not know. I got the gist from the legend, but the sentence "the measured slew supplies the settling time and the control effort, which the analysis passes on" required the purple box to decode, and I still do not know what "slew" is beyond a manoeuvre.

- Figure 6, bottom panel, and its caption: "with the small or medium wheel peak slew power takes one value per wheel class and tracker grade (the six horizontal bands)". The metric is quantized by categorical choices, so the "surface" in that slice is a line passing through a few discrete rows. I was not sure what an elasticity means when one of the two metrics only takes six values.

- The hypothesis codes (A1 to A8, R1, R2, F5, F10, F12, I5, I6, I8, I9, I14 to I16) are cited throughout the statements and defined nowhere in the slice. I treated them as opaque labels.

## 7. Terms I had to guess

- "n-lemma", "dilemma", "trilemma": the number of metrics with nonzero weight in a term, named by analogy with dilemma. Guessed from Figure 1 and Definition 6; fairly confident.
- "contending set": the metrics in a term's support; the ones actually traded against each other. Guessed; confident.
- "reach β": the offset of the hyperplane; the soft maximum of the projected scores, i.e. how far the data go in direction w. Definition 7 says this, but the word "reach" alone would not have told me.
- "energy differential", "level", "potential" for log V: a physics metaphor for signed distance from the surface in log units. I guessed and would have preferred "log-offset" or "residual."
- "chart": used in the manifold sense, a coordinate system. Guessed from Definition 5.
- "cell": the set of designs for which a given term is the maximum, like a Voronoi cell. Guessed; confident.
- "conditioned": metrics after whatever transform made them positive and larger-is-better (the axis labels say "inverse kg" and "inverse deg," so inversion for cost-like quantities). Guessed from the axis labels.
- "regime", "primary", "stock": two versions of the dataset generated with different controller gains. Guessed from the Figure 9 caption.
- "effective sample size" (Figure 4): the inverse sum of squared softmax weights, counting how many designs the soft maximum actually listens to. Guessed from the shape of the curve and from Theorem 2's p = softmax(τUw).
- "trade study", "trade space": a comparison of candidate designs across competing metrics; the "space" is the metric space those designs occupy. Guessed.
- "hyperbolic" in the title: I assumed it refers to level sets of a product of powers being hyperbola-like in the metrics (x·y = const is a hyperbola), not to hyperbolic geometry. Guess.
- "«MoP»", "«MoE»": measure of performance, measure of effectiveness. Guessed from context in Figure 3.
- "slew": a rotation manoeuvre of the spacecraft. Guessed.
- "GGP-compatible" does not appear in the slice, but "generalized posynomial" (Theorem 10 (iii)) I took to mean a posynomial with monomial arguments allowed to be composed, as in the geometric-programming literature. Half-remembered, not read here.

## 8. Would I read the whole paper

Yes, selectively. I would read Sections 3 to 6.1 and Appendices D.16 and F in full, and skim the case sections. The reasons: the one-term fit is small, convex and immediately implementable; the placement relative to PCA is genuinely something I did not have a tool for (my habit for "which metrics trade against each other among the good points" has been PCA on a filtered subset, which the paper says is the wrong order); and the statements are unusually candid about what is not claimed, which makes me trust the parts that are. What would keep me from reading it end to end: the vocabulary load (n-lemma, reach, chart, cell, energy differential, contending set, participation, support, band, regime) is high enough that I was translating in my head throughout, and the case study is written for someone who already knows what a slew measurement and a tracker grade are. A notation-and-vocabulary table before Section 3, and the PCA comparison promoted from an appendix bullet to a figure in the results, would each have cut my reading time noticeably.

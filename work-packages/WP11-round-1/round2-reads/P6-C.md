Cell: P6-C (persona P6, depth C); model: sonnet; date: 2026-11-10
Slice commit: c6d0fff (staged build in the stage worktree, served at 127.0.0.1:8790); reader prompt: prompts/P6-C.txt

REPORT (efficiency and frontier-analysis reader, P6-C)

1. What this is about

The paper proposes a way to analyse a trade study. You have a table of N designs, each scored on d "metrics" (strictly positive, larger is better). The method fits a posynomial "reference surface" to the outer edge of that table, softly and not through its middle. Each design is then re-expressed as two numbers: where it sits along the surface (the "position"), and how far above or below the surface it is (the "level", log V, called the "energy differential"). Each monomial piece of the surface carries an exponent vector on the simplex. The metrics with nonzero exponent are the "contending set", an "n-lemma", and the ratios of exponents are elasticities, the trade rates between them. The paper contrasts this with PCA ("PCA explains variance, we explain tensions") and argues that Pareto dominance stops discriminating as metrics are added: 659 of 706 designs are nondominated on 8 attributes. It illustrates the method on a cubesat table (706 feasible designs, 8 attributes, 2 controller-gain regimes) and on planted synthetic tables where the answer is known.

In my own terms it is a one-sided, soft-maximum, log-linear frontier fit. V is a weighted geometric mean with weights on the simplex, so it is a constant-returns Cobb-Douglas / Shephard-type distance function. K pieces are combined by a log-sum-exp. The scores it reports are radial-style efficiency scores on the log scale.

2. The main result

I could not find a single headline theorem. The theorems are mostly algebraic facts about the construction, and the headline is empirical. The facts are:
- V is homogeneous of degree one.
- The one-term fit is a convex program.
- The exponents are elasticities.
- A maximizer of V is Pareto-efficient. The converse is explicitly not claimed.
- The multi-term alternation descends, has a stationarity gap, and is locally optimal where the assignment margin is positive. There is a second-order certificate for the soft fit.

The empirical claims are these:
- On the cubesat, one term gives a 5-lemma (total mass, energy balance, pointing error, depth of discharge, settling time) with exponents 0.14 to 0.36.
- Three terms give contending sets of 4, 5 and 5 metrics, and control effort and peak slew power each lead a term of their own.
- On 20 planted tables the fit recovers all three terms in 16 cases.
- Dominance saturates as metrics are added.

The framing claim is that the method gives a coordinate system, a level, and named trade-off exponents where a nondominated set gives only a list.

3. What I would do next

- Run it against a standard DEA benchmark. I would take a data set with known inputs and outputs, treat the larger-is-better metrics as outputs with a dummy constant input, and compare the K = 1 weights and the level (log V) with the CCR/BCC output-oriented efficiency scores and the multipliers. I would also compare against a stochastic frontier fit. I want to see where they agree and where they disagree.
- Test the identification claim directly. I would plant frontiers that are not log-convex (a dent or a concave section) and see what the fit reports. The paper admits this is Q4 and "holes".
- Perturb the conditioning, for example rescaling one metric, and see whether the contending sets move. The paper says they do ("rescaling one metric changes which term is tangent"), so I would measure how much.
- Read the appendices only to check the planted-recovery study and the dependence on tau.

4. What I would tell a colleague

"It is a smoothed, log-linear, one-sided envelope fit with a per-piece weight vector. In effect it is a soft Cobb-Douglas frontier with a max-affine extension, reported in terms of elasticities. The honest content is the reporting layer, not a new frontier estimator. The reporting layer is the position/level chart, the named contending sets, and the exact pull-back to attribute units. The paper is unusually frank that the surface is not the Pareto boundary, and it does not claim priority. Whether the contending sets mean anything in a real study depends on the conditioning and on K, both chosen by the analyst."

5. What I think the method does not do

- It does not estimate the Pareto boundary or a production possibility set. The paper says so (Definition 1, Q4). It fits a soft support that about 10 percent of designs exceed.
- It is not a consistent estimator under noise (Q2), and identifiability of the active metrics is open (Q3).
- It does not handle non-log-convex structure. The authors say no K represents it.
- Its answers depend on the conditioning. Rescaling a metric changes the tangent term. The exponents describe the sample and are not estimates with sampling error (Section 10).
- It does not choose K. Mean slack falls with K by construction.
- It does not give a global solution for K > 1 (Q1). The guarantees are descent, a stationarity gap, and local optimality under a positive margin.
- It does not give a causal exchange rate. The exponents are features of the conditioned empirical model.
- It does not do the search (Section 7 is future work with no results), and it does not select a design.
- On the evidence shown, it does not demonstrate that the terms recover a meaningful structure in real data beyond planted tables. The cubesat reading is interpretive.
- It does not handle returns to scale in the DEA sense. Constant returns follows from the simplex constraint. The paper says "homogeneity from the simplex, in place of ... a choice of returns to scale", so that choice is simply made for the user.

6. Where I was confused or stopped (quoted)

- Abstract and Section 1: "A fitted posynomial reference surface models the data underlying the table, not the Pareto boundary, and gives the data a coordinate system; the table and its reading are views of that model." I could not tell what "models the data underlying the table" means, or what "views of that model" means, until Definition 1. The sentence is vague and I had to guess.
- Section 2, DEA paragraph: "We differ in what the envelope is. We fit one exponent vector per term, a global named structure, where DEA obtains weights unit by unit". This is the key novelty claim against DEA, and I find it thin. Multiplier-form DEA with a fixed weight vector, and DEA with weight restrictions, also give one global weight vector. A max-affine fit is a piecewise-linear envelope, as DEA's free-disposal hull is. The real difference may be the smooth soft maximum and the log scale, but the paper does not say so directly.
- Table 1, Pareto row: "Shares: the weights act as a trade-off". It is unclear what is shared.
- Table 1, DEA row: "Differs: One exponent vector per term". The cell reads as a fragment and does not say how the method differs.
- Section 2 (Lineage): "Combining these pieces in one estimator is our design. We did not find the combination in the sources reviewed". This is an honest claim, but I could not judge it from the main text. The fitted-envelope literature (Hoburg et al. 2016, Magnani and Boyd) is close.
- Definition 2: "By analogy with a potential, designs of equal V stand at the same level, and log V, the energy differential, is a design's level relative to the fitted reference surface... A difference of levels is the same along every path between two designs. It is neither a physical energy nor a Euclidean distance." The analogy is not needed. log V = w·u − β is simply a linear score minus an offset, so path independence is trivial. I stopped at "energy differential" as a name that suggests more than it delivers.
- Definition 4: "the fit weighs every design in its soft maximum, and one inside the band weighs within a factor e of one on the surface". I could not parse it. The cited result is L5.25, which I cannot see.
- Definition 7: "The reach β_k is how far the data extend in direction w_k". The statement is hard to follow. The term share is "the fraction of near-frontier designs in the cell of term k ... depends on the band", so it is not an intrinsic property.
- Section 5: "τ puts a target fraction of designs above V=1: 10 percent here, a convention that keeps one extreme design from setting the surface". The surface is thus set partly by a free quantile parameter. The contending sets are said to be unchanged when it is halved or doubled, but the evidence is in Appendix D.5 only. Figure 4 shows the exponents do shift with tau: control effort drops out at about tau of 25 and the ranking changes.
- Section 6.1, Theorem 4: "LSE_τ = LME_τ + (log N)/τ". This is a trivial identity presented as a theorem, and the emphasis on "never the unnormalized log-sum-exp" read as more important than its content.
- Theorem 9: a maximizer of V is Pareto-efficient. This is the standard property of any strictly monotone scalarization with positive weights. It is correctly stated, but it is a thin connection to the Pareto world, and the converse (reaching the whole boundary) is not claimed. For non-convex boundaries the weighted-sum method cannot reach the concave parts, and the paper only says "our reading" in Section 7.
- Theorem 2 (the KKT conditions) has an odd sentence: "Balanced hard-support geometry does not imply an interior minimizer at finite τ." I could not see what it adds.
- Section 5: "Which term scores a design highest is analysis of the fitted model, not part of the fit". This contradicts the objective in Equation (2), where the label k(i) is an argmax inside F. I was confused about whether assignment is part of the fit.
- Section 6.2, Theorem 10 part (i): "a convex program symmetric in the terms attains its minimum with all terms equal, so the objective over all terms is not convex in them in general". The reasoning is compressed. I follow the idea (symmetry makes the all-equal point a minimizer of a convex symmetric problem, so a symmetric multi-term objective cannot also separate the terms), but it is hard to read as written.
- Section 6.2: "Refitting a term on its own rows is ill-posed (observed on planted data, Appendix D.13)". It is not clear what is ill-posed, since Theorem 11's descent depends on exactly this refit.
- Section 6.2, stopping declaration: "certified means that the second-order test holds... stationary that the term gaps hold and the curvature is not positive". The meaning of "certified" is a local minimizer only, but the word suggests more.
- Section 6.2: "At K = 3 the margin is 0.00121 and the stable radius 0.0001209, against a band 1/tau of 0.0088... here 11 of the 706, and the certificate covers changes under the radius only." The stable radius is smaller than the band by a factor of about 70, so the local-optimality guarantee covers perturbations far smaller than the noise. The text states this but does not draw the consequence. I also noticed that the band is 0.0262 at K = 1 (tau = 38.1) and 0.0088 at K = 3 (tau = 113), so the band is not comparable across K.
- Section 6.3: "Q1: global convergence of the alternation, not pursued." This is one of the four open questions, and the key ones for a frontier estimator (consistency, identifiability, recovery of the Pareto boundary) are all open.
- Section 8: "Of 706 feasible cubesat designs, the nondominated sets hold 126 on 4 and 659 on 8 attributes". The 4-attribute set is not specified. The saturation is partly a feature of the design sampling and the number of attributes, and is not a general finding.
- Section 8: "The planted table has 900 rows, 4 metrics and 3 planted terms." Section 9 then says "On 20 planted tables (400 rows, 4 metrics)". The row counts differ (900 vs 400), and I could not tell whether they are different tables.
- Section 9: "recovers all three terms to within 0.05 in 16, at the exact maximum and at temperature 50; the 4 failures have 5, 5, 6 and 11 frontier rows on their thinnest term". 16 of 20 is the main validation, and the tolerance and failure mode are plausible, but there is no comparison against another method. Sparse frontier support leads to failure, which is the known weakness of any boundary estimator.
- Figure 4: the heat map and exponent column are readable, but the exponents move with tau (control effort drops out above tau of about 25). The caption says the vertical line is where the fraction "first meets the target", while the text says the fraction is 0.092 against a target of 0.10, so the target is not met exactly. The right-hand top panel annotates "n_eff = 23" and the text says 23.1.
- Figure 5: with the other six metrics at the median, many designs lie above the drawn line. The caption warns that a design above the line "can be inside the surface", which means the slice shows little about the fit. The line also runs through the upper right of the cloud, with many points beyond it. At a 10 percent exceedance target this is expected, but the slice cannot show that.
- Figure 6: the straight lines do not touch the cloud's top edge in the top panel (settling time and control effort); a lot of points sit above the line. The caption says why (the median of the other six metrics). The bottom panel (pointing error and peak slew power) shows discrete bands, which look like the model's discrete design choices (tracker grade, wheel class), so a continuous log-linear surface is being fitted to a lattice. The caption also says "the large wheel's designs form the lower cloud".
- Figure 7: the chart shows log V from about −1 to +0.05, and most designs sit below the line with a large empty region at the bottom. Z0 has "no meaning alone". This figure shows almost nothing I can act on. The text promises it shows "each design's level read apart from its position along the surface" but I see no structure by position.
- Figure 8: for term 1 there is no map, "Too few near-frontier designs for an association reading: 3 of ten". So the 4-lemma of term 1 is supported by 3 near-frontier designs. The text claims "control effort and peak slew power ... each lead a term of their own", yet in the figure control effort is grey with w = 0.00 in terms 2 and 3, and term 1 (the one that would hold it) has no map. In term 3, "energy balance" is outlined (in the contending set) but its exponent is 0.00 (grey), and the caption explains "an outlined metric can be grey". I found this hard to read.
- Figure 8 and Figure 9: the maps are correlations among near-frontier designs. The text itself admits "A clustering with per-cluster correlations would describe the same designs; the terms add a model". The contending-set outlines come from the exact-maximum support while the exponents shown are at the fit temperature, so the two do not match in places (outlined, but w = 0.00). Also, in Figure 9 the strongly positive 0.99 association between power margin and energy balance looks like two measures of the same thing. That redundancy goes unremarked, and only one of the pair carries the exponent in the stock panel while the other carries 0.02.
- Figure 9, stock panel: "total mass" is grey (w = 0.00) and not outlined, but the text says "The stock set spans controls plus power and energy: mass enters only in the primary regime". This matches. But exponents such as depth of discharge 0.01 count as members. The membership threshold (10^-9 for the support, 10^-3 for participation) leads to a "5-lemma" that includes metrics with weight 0.01.
- Section 9: "The 3 measured candidates have lowest energy differential -0.197 and highest -0.153, and 0 of them lie beyond the fitted reference surface." The candidates are "scored against the K = 1 fit" but it is unclear what a candidate is here (they are introduced only by "Candidates are scored against the K = 1 fit (Appendix D.7)"). The sample of three is tiny.
- Section 9: "Of 3 proposals, the predicted energy differential lies within the regressor's own band 1/tau = 0.0935 ... for 3, and the predicted position within that band for 1". Section 10 then says "Two of the three proposals are one configuration" and "Three proposals of two designs illustrate and do not estimate a rate". This is honest, but it undermines the claim that the method can propose useful designs. The proposals "reached the four-metric frontier by spending the battery" and fail the depth-of-discharge requirement. That is a clear sign the surface is read as an opportunity where a requirement is violated.
- Section 10: "A hole in the chart is an opportunity only where the trade space is log-convex around it, which the data cannot prove."
- Section 10: "removing the infeasible designs or imposing the four requirements before the fit changes the one-term contending set by at most one of its five metrics". The numbers are in Appendix D.17.
- Section 10: "Novelty and white space. By Theorem 1, a design with V=v is a frontier design scaled by v, so V−1 is a relative improvement". This follows from homogeneity, but "a frontier design scaled by v" reads as a statement about physically realizable designs, which the surface does not claim to model.
- Section 10, "Why a frontier": "An answer far from the frontier is hard to justify, and the analysis must rerun on empirical data to support configuration management". The first sentence is an assertion and not an argument. The second is not connected to anything shown.
- Section 13: the AI-assistance statement ("The derivations are machine-checked") is a claim I cannot check from the main text. I also noticed that "verified" and "validated" are used in a specific, careful way (Section 10).
- Equation (2): F(W) = (1/N) Σ (β_k(i) − w_k(i)·u_i) = Σ (n_k/N) f_k(w_k), where f_k(w) = J_τ(Uw) − ū_k·w. The sharp-assignment objective is "mean slack to the assigned term's offset". Since β_k is defined over all rows (J_τ(Uw_k)) and the label is the argmax of s_ik, this is a one-sided mean-gap criterion. It reads like a minimum-gap fit to a max-affine function, in the spirit of Magnani and Boyd, and I could not see why it should select a frontier and not a regression through a shifted cloud, other than the soft-maximum offset.
- Appendix references (L5.25, I4, I6, etc.), "F5", "F10", "F12" and "A8" are cited without definitions in the main text.

7. Terms I had to guess

- "Posynomial reference surface" / "fitted reference surface": I took it as the level set V_K = 1 of a log-sum-exp (soft max-affine) function of the log-metrics. I guessed that "posynomial" is the exponentiated form and the surface is convex in log space.
- "Energy differential" / "level": I took it to be log V = w·u − β, a signed score relative to the surface. It is not an energy.
- "Position along the surface" / "chart": I took it as the projection Z = Bu onto the subspace orthogonal to the all-ones vector (a Helmert/isometric log-ratio basis), the log-ratios of the metrics. This is what makes it "free of overall scale".
- "n-lemma" / "contending set": the support of the exponent vector, the metrics with nonzero exponent in a term.
- "Reach" β: the soft maximum of the scores along the direction w, so the offset that puts the surface at the data's edge.
- "Cell" of a term: the set of designs for which that term is the largest, as in a Voronoi/max-affine partition. "Term share" is the fraction of near-frontier designs in the cell.
- "Near-frontier band" |log V| < 1/τ: designs within about 1/τ of the surface in log units.
- "Effective sample size": the reciprocal of the sum of squared softmax weights, I guessed, as the number of designs that effectively set the soft maximum. With n_eff = 23 of 706 designs, the surface is set by a small number of points.
- "Term gap": a duality-style gap on the simplex (g·w − min g) that bounds the suboptimality of a convex subproblem.
- "Assignment margin", "stable radius": the smallest score gap between the best and second-best term over designs, and the perturbation size below which assignments cannot change.
- "Conditioning": the analyst's preprocessing that makes each attribute positive, larger-is-better, and unit log-spread (log-affine transform).
- "Pull-back to attribute units": mapping exponents on metrics back to powers of the raw attributes through the log-affine conditioning.
- "MoE" / "MoP": measure of effectiveness vs measure of performance (the paper defines them in the text).
- "Compatible with generalized geometric programming (GGP)": the model can be used as a constraint or objective in a geometric program (log-sum-exp of affine functions in log space).
- "Hyperbolic": the paper says it is the shape of the level surfaces of V in metric space (products of powers equal to a constant), nothing to do with hyperbolic geometry in PCA.
- "Kernel direction": replacing the log-linear features by other GGP-compatible features. Nothing is built.
- "Weakly efficient" vs "efficient": the standard Pareto terms. I assumed "weakly" means no design improves all metrics strictly.

8. Would I read the appendices?

Yes, selectively, and for these reasons only:
- Appendix D.14 (the 20 planted tables) and D.5 (the effect of halving or doubling tau): these are the real empirical support for the identification claim, and the main text gives only counts.
- Appendix D.17 (requirements after the fit) and D.7 (candidates), because the main text gives conclusions without the numbers.
- Appendix G (the prior-art register), to see whether the "we did not find the combination" claim holds against DEA with weights restrictions and against Hoburg's softmax fitting.
- Appendix E (the gaps ledger), because it records exactly where the assumptions fail.

I would skip the proofs in Appendix B. The theorems are short algebra with sketches, and I can see they are standard facts about log-sum-exp, convexity and Pareto monotonicity. They are not where my doubt lies. My doubt is whether a soft one-sided log-linear envelope with an analyst-chosen tau, K and conditioning produces contending sets that mean anything outside planted data, and that is an empirical and methodological question, not a proof question. I would not go further unless the planted-data results held up and a comparison with a DEA multiplier solution agreed with the contending sets on a real data set.

Credit where it is due: the paper is frank about its limits (surface is not the boundary, no consistency claim, no priority claim), and it states the relation to DEA, distance functions and stochastic frontiers rather than hiding it. Its distinct contribution is the reporting layer (chart, named contending sets, elasticities, pull-back). I think the estimator underneath is old machinery (Cobb-Douglas distance function, corrected least-squares-style one-sided fit, max-affine extension), and the paper mostly says so itself.

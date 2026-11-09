# WP10 cold reads, round 1 (verbatim reports)

One fresh reader per depth (L-A to L-F), no persona. Each reader was given only its depth's slice of the rendered paper (L-A to L-D: slices built from the rendered site at commit abd06ac; L-E and L-F: a clean checkout at caff444, no container tooling) and the neutral task text of the brief; they never saw the scope, the records, the register, the story or this conversation. The reports below are verbatim, in the readers' own words; the PM's summary, if any, comes after them. Authors act only on change requests the driver writes.

---

## LA-1

# Reader report LA-1 (read cold: abstract, Figure 1 and caption, first screen only)

## 1. What this is about
A method for trade studies (comparing candidate designs against several competing metrics). You take a table of evaluated designs, fit a posynomial "frontier" surface to it, and use that fit to give each design coordinates: a position along the frontier (Z) and a distance from it ("energy differential", log V). The frontier is split into facets, and each facet reports which metrics are in tension there, with exchange rates between them. It is pitched as an unsupervised-learning tool that sits beside PCA, with a scikit-learn implementation. The case study is a cubesat attitude-control trade space.

## 2. Main result, as I understand it
Not a theorem. The claim is that the fitted frontier, drawn as a chart where the frontier is a straight line, gives an interpretable decomposition of a trade space. It tells you which metrics contend in each region, and with what exchange rates. In the cubesat example, one facet gives a single tension, whereas three facets give three regimes with different contending sets. The abstract also says the fit is convex for one facet and alternating convex for several, with guarantees stated at three levels (derived, numerical, open). I can't judge how strong any of this is from what I was given.

## 3. What I would do next
Find the methods section and check how the frontier is fit. In particular: how the data are conditioned into positive larger-is-better metrics, how the number of facets is chosen, and what the "n-lemma" is. Then try it on a small trade table of my own, if the package is easy to install.

## 4. What I would tell a colleague
"There is a paper proposing a PCA-like tool for trade studies. Instead of variance directions, it finds which objectives trade against each other, in regions of the Pareto-like frontier, with exchange rates. It is reproducible and has a scikit-learn API. I haven't seen the details or the evidence."

## 5. What the method does not do (from the little I saw)
- It doesn't explain variance, which is what PCA does. The abstract says so itself.
- It does not generate or evaluate designs. It takes a table of already-evaluated designs.
- Judging by the figure, it doesn't say which design to choose. It describes the structure of the space. The abstract's opening mentions "an answer", but I saw no sign of one.
- The abstract says "conditioning is the analyst's job" is not stated, but the phrase "table of evaluated designs" implies the metrics are already prepared. I'm guessing here.
- Guarantees for several facets are partly "numerical or open", so the multi-facet fit is probably a heuristic with no global-optimality guarantee.
- The abstract doesn't say how many facets are chosen or how sensitive the result is to that choice.

## 6. Where I was confused
- "We explain tensions." This is the one-line pitch, but I couldn't tell what "tension" means formally until I looked at the figure.
- "each facet reports the metrics that contend there, found rather than assumed, as an n-lemma with exchange rates". I don't know what an "n-lemma" is, and a lemma sounds like a proof object rather than a report.
- "A reversible chart separates where a design sits along the frontier from its energy differential to it". I'm unsure what "reversible" means here (invertible map, I guess) and why a physics word like "energy" appears.
- "Every claim points to a machine-checked derivation, a test or a regenerable table." I can't tell what is machine-checked (a proof assistant? symbolic algebra?).
- Figure 1, middle panel: the arrows w1, w2, w3 are called "each facet's normal" in the caption, but the paper has not yet said what they mean. Presumably the exchange-rate weights.
- Figure 1, left panel: the dotted curves are "other energy levels", and V = 1 is the frontier. I couldn't tell why the V > 1 side is called "beyond" or what V is in plain terms.
- The title says "Scaling Decision Analysis", but nothing in what I saw addresses scaling (more designs? more metrics?).

## 7. Terms I guessed
- Posynomial: a sum of positive-coefficient monomials, so convex after a log transform. I knew this from geometric programming.
- Facet: a linear piece of the log-space envelope.
- Energy differential (log V): signed log-distance from the frontier. Zero is on the frontier, negative is inside it, positive is beyond.
- Hyperbolic trade space: I guessed it refers to the hyperbola-like curves in metric space, such as a product of metrics being constant.
- Metric versus attribute versus configuration: the abstract uses "metrics" only, and I assume they are the positive, larger-is-better outputs.
- "Chain" with PCA: I read it as running PCA and then this method, or the reverse, in a pipeline.
- Unsupervised learning and feature engineering: I assumed they mean the fit gives a learned coordinate system with no labels.

## 8. Would I read further?
Yes, a bit. The figure is clear and does convey the idea: curved frontier, polyline in log space, flat line in the chart. The pitch (explaining what trades against what, rather than variance) is a real gap. I'd read the cubesat example and the facet-selection logic next. What worries me is that the abstract contains almost no numbers or comparison with other methods, such as Pareto-front analysis, so I can't judge the value. The vocabulary (n-lemma, energy differential) is heavy for a first pass. I could not tell from what I was given whether the method works on real, noisy data or how robust the facet count is.

---

## LB-1

# Cold skim report (LB-1)

I read README, headers, the list of main results and statements, the figure captions, and looked at figures 1, 2, 5 and 8. I did not see the body text, any numbers from the case study beyond what the figures show, or the proofs.

## 1. What this is about
A method for analysing multi-objective design decisions (the example is a cubesat attitude-control trade space). You have designs described by several "metrics" (positive, bigger is better). The paper fits a smooth "frontier" to the data in log space: a weighted geometric mean of the metrics, V, scaled so V = 1 sits at the frontier. One piece gives you exponents that act as exchange rates between metrics (percent of j per percent of i). A "chart" rewrites each design as (position along the frontier, log V), where log V is how far inside the frontier it sits. Several linear pieces ("facets", a posynomial with K terms) let the frontier bend, so different regimes of the trade space get different exchange rates. The point seems to be decision support: see which metrics are in tension, where designs are crowded, and where there are holes.

## 2. Main results, as I'd tell a colleague
- Mathematically: the one-facet fit is a convex problem on the simplex, with KKT conditions, so it is well behaved (Theorems 2, 3). The exponents have a clean reading as exchange rates, and the (position, log V) chart is an invertible rewrite of the metrics (Theorems 5, 6). A maximiser of V is Pareto-efficient (weakly, or fully when all weights are positive); the converse is explicitly not claimed (Theorem 9). The multi-facet algorithm gets a local-optimality statement with a computable gap, and it is stable to small perturbations of the facets (Lemmas 1, 2, Prop 3, Cor 4). Global optimality is explicitly not claimed.
- Empirically: on one cubesat case, three facets separate regimes that one facet blends together (Section 9). I can't judge how convincing that is. I saw only pictures.
- Not claimed: global optimality of the multi-facet fit, strict convexity, the converse of Pareto efficiency, consistency of the statistical estimator (Prop 2 is "a population identity, with no consistency claim"). The listed results are labelled "Derived", i.e. proved, not tested on many datasets. The "search of the design space" section is labelled preliminary. Figure 8 compares predicted with measured chart positions for three proposed designs, which looks like a small check.

## 3. What I'd do next
Find the case-study section and the reproducibility section, and try the method on a small dataset of my own with 3-5 metrics. I'd check that the exchange rates it reports match what I already believe about the trade-offs. I'd also try a different K to see whether the facets are stable.

## 4. What I'd tell a colleague
"It's a convex-fit way of getting an interpretable frontier and exchange rates out of design data. The theory looks careful about what it does and doesn't claim. The evidence is one cubesat example, so I'd wait to see whether it holds up elsewhere."

## 5. What the method does not do (as far as I can tell)
- It does not do the conditioning, i.e. turning raw attributes into positive larger-is-better metrics. I am inferring that from the pull-back theorem and the text "conditioning is invertible".
- It does not find the true Pareto boundary. The fitted surface is a smoothed reference, and "some designs lie beyond it" (Definition 9).
- It does not guarantee the global best facet partition.
- It does not discover unattained designs. The "holes" in Fig 5 are only candidates, "for human validation to judge".
- It does not tell you which metrics matter to the decision-maker, or what weights to use. The weights are fitted from data, not elicited.
- It needs strictly positive metrics (zeros and negatives are a problem, and I don't know how they are handled).
- It does not make claims about causal structure.

## 6. Where I was confused or stopped
- Definition 3: "the fit temperature tau>0 sets how hard the maximum is (tau=infinity is exact); the term temperature kappa>0 how sharply facets meet." I don't see how tau is chosen. Figure 2 shows a vertical bar marking "the temperature selected" at the point where the fraction above V = 1 reaches 0.1 (the "target fraction"), so it seems to be tuned to a target. Why 10% is not clear from what I have.
- Definition 6: "The reach beta_k is the support value of the data in direction w_k. The facet share is the fraction of near-frontier designs on facet k, our analogue of explained variance." I can't tell what "explained variance" would mean here, or how far the analogy goes.
- Theorem 2 note: "balanced hard-support geometry does not imply an interior minimizer at finite tau." I could not parse that.
- Definition 4: "log V is the energy differential (level offset)". Why "energy" is unexplained.
- Fig 2 right panel: several metrics (settling time, power margin, eclipse reserve, peak slew power) have exponent zero at every tau. I can't tell whether that means they don't matter or are dominated, and the paper-level conclusion isn't visible to me.
- Figures 5 and 6 are hard to read cold: dense overlap of facet colours, and I can't tell what the "holes" would be.
- Figure 8: the predicted and measured positions are close for three proposals, but three points aren't much and I don't know how they were chosen.
- Lemma/theorem labels like "A2", "R1", "F12", "I9" are hypotheses defined elsewhere; I could not check them.
- Section 2 is "Prior art, by family" and I could not see how this differs from standard Pareto/DEA/geometric programming methods; I only know the paper cites a posynomial structure.

## 7. Terms I had to guess
- Metric vs attribute: I guessed attributes are raw outcomes and metrics are the cleaned positive ones.
- "Simplex" Delta: the set of nonnegative weights summing to 1.
- "Facet": one linear piece of the log-frontier, i.e. one term of the posynomial.
- "Contending set" / "n-lemma": the metrics that actually have weight on a facet (dilemma = 2, trilemma = 3).
- "Posynomial": sum of positive monomials (geometric-programming term). Fine, but I'm guessing at how it's used.
- "Soft maximum" via log-mean-exp, and "effective sample size" in Fig 2: I guessed it is the number of designs effectively near the frontier under the softmax weights.
- "Reach": guessed it as the offset beta, the furthest extent of the data in that direction.
- "White space": unexplored regions of the design space.
- "Stable radius" and "assignment margin": the size of perturbation that does not change which facet a design belongs to.

## 8. Would I read further?
Yes, moderately. The framing is clear and the theory is honest about its limits, which I like, and the "exchange rate and chart" idea is appealing for decision support. What I couldn't tell is whether the empirical side is more than one example, how sensitive the results are to tau (chosen from a target fraction), K and the conditioning step, and how this beats a plain Pareto-front plus regression. I'd go to Sections 5, 8, 9 and 10 and look at the case construction and the limits discussion before deciding whether to try it. I would skip the proofs unless the results surprised me.

---

## LC-1

# Reader report LC-1

I read README.txt, main-text.txt (abstract through the works cited) and looked at figures 1, 6 and 8. The appendices (A to G) are referred to constantly but are not in the folder. I did not read figures 2 to 5 and 7 as images; I relied on their captions.

## 1. What this is about
It is a method for trade studies. You have a table of evaluated designs. Each design has several "metrics": positive numbers where larger is better, after an analyst has conditioned the raw attributes. The method fits a "posynomial frontier" to the upper edge of that cloud in log space. The frontier is a set of flat pieces ("facets"). Each facet has a vector of exponents that are non-negative and sum to one.

The metrics with non-zero exponent on a facet are said to "contend" there, and the paper calls that set an "n-lemma". Within a facet the exponents give exchange rates between metrics. The fit also gives each design a coordinate Z (position along the frontier) and log V (how far inside or beyond the frontier it sits). The pair (Z, log V) is a reversible chart.

The paper pitches this as a companion to PCA: PCA says where the data vary, this says what trades against what. It is demonstrated on a cubesat attitude-control example and a synthetic planted example.

## 2. Main results and how the argument gets there
The paper has two kinds of result.

**Mathematical properties of the construction**, each marked "Derived", with a SymPy script behind it. I could not see the proofs, only sketches:
- V is a degree-one weighted geometric mean, so scaling every metric by k scales V by k, and V can be read as an improvement factor.
- The one-facet fit is a convex program on the simplex, with KKT conditions stated. It uses log-mean-exp rather than log-sum-exp, so the offset does not depend on N.
- Exponent ratios are exchange rates, and the chart is an invertible rewriting.
- A maximizer of V is Pareto-efficient (the converse is not claimed).
- The multi-facet fit is non-convex. It alternates refitting each facet and reassigning designs, in the style of Magnani and Boyd. The guarantees come in three levels: descent; stationarity, via a facet-gap bound; and local optimality if the assignment margin is positive. The solver reports a status such as "certified".

**Empirical readings on the cubesat case**, which are not proved:
- With one facet, six of ten metrics contend.
- With three facets, shares are roughly 7%, 14% and 78%, and the contending sets have 6, 6 and 7 metrics. Their union has 9 metrics, so three metrics absent from the one-facet reading appear.
- Two regimes (aggressive and stock gains) give different contending sets that share 3 metrics.
- Three candidate designs were scored, and their positions were predicted by a regressor and then measured.

The argument runs: define the object, prove it behaves well, give an algorithm with graded guarantees, apply it, and say honestly what is open.

## 3. What I would do next
I would run it on a table I know well. I would first check how stable the contending sets are under a different conditioning (rescaling a metric changes which facet is tangent, as the paper itself says), a different tau and a different K. I would try to reproduce the three-versus-one-facet contrast on a case where I know the real trade-offs. I would also read the appendices on assumptions and gaps.

## 4. What I would tell a colleague
This is a careful, honest attempt to give trade studies a PCA-like, reproducible summary: which metrics fight each other on which part of the frontier, with exchange rates. The mathematics of the construction looks tidy and is machine-checked, but the claim that it finds real trade-offs rests on conditioning and modelling choices made by a human. The only evidence on real-ish data is one illustrative cubesat model with invented hardware values. Interesting, worth a look, not yet something I would trust a decision to.

## 5. What the method does not do
The paper says several of these itself:
- It does not condition the metrics. That is the analyst's job, and the result depends on it.
- It does not choose K. The objective falls with K by construction.
- It does not produce causal exchange rates. They describe how the sampled designs trade.
- It cannot represent non-log-convex structure, so it reaches only the log-convex part of the Pareto boundary.
- It offers no global optimality or convergence guarantee for K greater than 1, and no consistency under noise.
- It does not select designs. The search section (Section 7) is future work with no results.
- It does not find tensions the sampling never exercised.
- It gives no "successive tensions" deflation like PCA. The paper claims neither that this works nor that tensions are orthogonal.
- It does not tell you whether a hole in the chart is an opportunity.

## 6. Where I was confused or stopped
- "**the 'near-frontier band' is |log V|<1/τ**" and "**τ chosen so that a target fraction of designs lies above V=1**" (Section 5, Definition 3). Why a 10% target? Why is the band 1/τ wide? No reason is given. It is not obvious why the target fraction is a sensible statistical choice.
- "**the principal directions of the near-frontier chart coordinates are the exercised trade-offs**" (Section 1). This is stated without argument. The PCA chaining is claimed but never demonstrated in the main text.
- "**facet share ... our analogue of explained variance**". Why this is analogous is not argued. A share of near-frontier designs is a count, not a fraction of anything conserved.
- "**Each facet is fitted against all rows, as a supporting hyperplane of the whole cloud that is tightest on the facet; refitting on its own rows is ill-posed on the planted data**" (Section 6.2). The "why" for the ill-posedness is owed. I only see a bare assertion.
- Facet 1 of K=3 has a 6-lemma with six metrics contending out of ten. In Figure 6 the exponents are very uneven (for example 0.43, 0.37, 0.14, then 0.04 and 0.02). "Contending" is defined as w>0, and elsewhere "participation" has a threshold of 1e-12. So a metric with exponent 0.02 counts the same as one with 0.43, even though the paper says "one at or below 10^-12 is numerically zero". The pictures suggest a much smaller effective set than six. The "6-lemma" headline therefore looks sensitive to a threshold the text does not fix.
- "**the smallest assignment margin 0.00022 to 0.0016 and the smallest stable radius 1.8e-05 to 0.00013**", with the status "certified". These margins are tiny relative to a band of 0.026 to 0.065. A reader asks what "certified" is worth when the stable radius is 1e-5. The paper does not say.
- In Figure 8 the prediction test is reported as "predicted energy differential within the band for 3 of 3; predicted position within the band for 0; position errors 1.4 to 3.1 bands". The paper says "we report the result as it falls". But then Section 10 reads as if the method succeeded. With three proposals it is hard to say what was shown. The 3 of 3 on log V is also weak, because the three candidates all lie well inside the frontier, where the prediction is easy.
- The Table 2 caption refers to "(-0.072 to -0.071)" and "0.77 to 0.78", odd ranges with no explanation of what is varying. I guessed it is rounding jitter (a reference to D.11).
- The cubesat two-regime comparison says only that the contending sets differ. Whether the difference is physically right (for example, why mass and depth of discharge contend only under aggressive gains) is not argued. The paper leaves that to "human validation" and the reader is left with no check.
- "**Dominance ... stops discriminating as the number of metrics grows**" is backed only by the counts (671 of 706 nondominated on 10 attributes). That is suggestive, but it compares the fit with the nondominated set only on the count of survivors.
- The three-versus-one story depends on K = 3 being chosen. The text says the choice of K is the analyst's, and the objective alone cannot choose it. So "three facets report three regimes" is partly an artefact of asking for three.

## 7. Terms I had to guess
- "Energy differential" for log V. I inferred it from the figure label and the physics-flavoured naming. The text only says "level offset".
- "Reach" (β_k) as "support value of the data in direction w_k". I understood it as the extent of the cloud along w.
- "Balanced point", "ridge rows", "assignment margin", "stable radius". I took them to mean the point where the optimum is interior to a facet, rows lying between two facets, and a robustness measure for the hard assignment.
- "Hyperbolic" here means that the level sets of V are hyperbola-like in metric space. The paper says it is not about negative curvature.
- "Mean slack" is the average distance of designs below the envelope in the objective's units. I assumed this.
- "Effective sample size" (16 designs at τ=38.1) is how many designs the soft maximum is effectively leaning on. It is not defined in the main text.
- "Novelty V−1". This is clear enough once read, but "novelty" for a relative improvement is a surprising word.
- The labels I1 to I12, F5, F10, F12 and G-11 to G-14 are references into appendices I do not have, so I cannot tell what they assume.

## 8. Would I go to supporting material, and for what
Yes. The main text is a summary of an object whose proofs, conditions and failure modes live in the appendices, which are not in this folder. I would look for:
- Appendix E (assumptions and gaps), to see how stable the contending sets are under conditioning, tau and K.
- Appendix D (extended results, the planted-data recovery check). This is the one place I could see whether the method really recovers a known answer. The main text gives only "the planted table has 900 rows ... 3 planted facets" and says nothing about whether the exponents were recovered.
- Appendix C (the cubesat model, to judge how artificial it is).
- Appendix B (proof steps), to check one proof myself.
- The code or documentation, to run it on my own table.

## What I could not tell
- Whether the method recovers planted exponents at all. The main text never gives the result.
- How robust the contending sets are. This matters most for the headline results.
- How the temperature, K and the participation threshold were chosen beyond the stated rules.
- How well this works on real data. The one case uses illustrative values, and the paper says so.
- Whether the "derived" badges are right. I only saw sketches and trust the claim of machine-checking.

---

## LD-1

# Reader report LD-1

I read README.txt, main-text.txt (Sections 1-13; the works-cited list at the end I only skimmed), the headings of appendices.txt plus Appendix B (L4, L14, checker), D (D.1-D.4, D.9-D.11), E, F, parts of A and C.7, and figures 1 and 6. I did not read every appendix line (the proof tables are very long), and I did not look at figures 2-5, 7, 8 as images.

## 1. What this is about
A method for trade studies. You have a table of evaluated designs (configurations -> attributes -> "metrics": strictly positive, larger is better). The method fits a "frontier" to the upper edge of the data in log space: a weighted geometric mean V of the metrics, with weights (exponents) on the simplex, fitted by a soft maximum (log-mean-exp with temperature tau). With one facet (K=1) the fit is a convex program. With several facets (K>1) it alternates between assigning designs to facets and refitting. Each facet's nonzero exponents name the metrics that "contend" there (an "n-lemma"), and the ratios of exponents are exchange rates between metrics. A "chart" (Z, log V) re-expresses each design as a position along the frontier plus a distance from it. The authors pitch it as a PCA analogue that explains "tensions" (what trades against what) rather than variance. Demonstrated on a simulated cubesat attitude-control (ADCS) trade space under two controller-gain regimes, plus a synthetic "planted" example.

## 2. Main results and what supports each
- Algebraic/convexity facts (Theorems 1-9: homogeneity, convexity of the fit, KKT conditions, exchange rates, reversible chart, pull-back to attributes, posynomial extension, a maximizer of V is weakly Pareto-efficient). Support: short proof sketches in the text, each tied to a SymPy script and a step-by-step ledger in Appendix B. These look like fairly standard facts; the paper itself calls them "Derived".
- Multi-facet algorithm: three levels of guarantee (descent; stationarity via a "facet gap"; local optimality when the assignment margin is positive), and a status label ("certified" etc.). Support: Lemmas 1-2, Proposition 3, Corollary 4 (Appendix B), and printed solver records (Appendix D.2/D.8). Global optimality and statistical consistency are explicitly "Open" (Q1-Q4).
- Case study: at K=1 one 6-metric tension; at K=3 three facets (shares ~0.08 / 0.14 / 0.78) with contending sets of 6, 6, 7 metrics whose union has 9 metrics; the two regimes share 3 of 6 contending metrics. Support: Figures 3-7, Appendix D tables, and a jitter-stability table (D.11) showing the contending sets, signs, and certificate statuses unchanged under 1e-12 perturbation. This is a single case with no external ground truth (see 5 and 8).
- Propose-predict-check: of 3 proposed designs, predicted energy differential (log V) was within the band for 3/3, but predicted position along the frontier was within the band for 0/3 (errors 1.4 to 3.1 bands). The text reports this honestly, but it is a small, mixed result.

## 3. Three things the main text points to
1. Theorem 3 / L4 (convexity of the fit, "d^2/dt^2 J = tau Var_p(v.u)"). Easy to find: the text gives file name and "Appendix B, L4"; Appendix B has a 13-step table with the code line for each step and a GitHub link. I could follow it. The step "by declared axiom I11" is just the textbook fact that convex = nonnegative second derivative on every line. The proof content is the variance identity (L4.3-L4.5), which is a symbolic-algebra assertion; I could read the line being asserted but did not re-run it.
2. Corollary 4 / Proposition 3 (L14) and the "certified" status. Findable (Appendix B, L14, 16 plus 4 steps). A little confusing: Proposition 3 and Corollary 4 share one script and the step numbers are interleaved (L14.8 and L14.10 appear under the Corollary, L14.9 under the Proposition). The ledger for L14 depends on L12/L13 and on hypotheses (R2, exact facet optima) that I can only see hold numerically in D.2.
3. The numbers "mean slack falls 0.20 -> 0.138 -> 0.117", "tau = 38.1, effective sample size 16", "671 of 706 nondominated". All found in Appendix D (D.2, D.1/D.4, D.9) quickly, and they match. D.11 even shows which printed numbers move under 1e-12 jitter. Easy.

Also (not one of the three) the claim that every table is regenerable: Appendix F.4 gives one row per figure/table with the call, but the "Reads" column is just "examples/adcs/data/", and the code itself is not in what I was given.

## 4. What I would tell a colleague
It is a carefully hedged, well-documented proposal for finding which metrics trade against each other near the edge of a table of designs, using a smooth, convex fit with an interpretable exponent vector per region. The math for the single-facet case is simple and credible; the multi-facet part is a local heuristic with a useful self-diagnosis (status labels, stable radius). The evidence that it finds "real" tensions is one simulated cubesat case where the answer is not known independently, so treat the case study as a demonstration, not validation. The honesty about limits (Appendix E, 17 listed gaps) is unusual and useful. Worth trying on your own table, but check the conditioning and K choices yourself.

## 5. What the method does not do
- No predictive model (no `predict`); no causal claim (the paper says exponents describe how sampled designs trade, not what changing a variable would do).
- No guarantee of global optimum for K>1, no consistency under noise, no identifiability of the contending set under finite, biased samples, no proof that the fitted surface recovers the true Pareto boundary (Q1-Q4, open).
- Only sees the log-convex part of the frontier; non-log-convex dents appear only as "holes" for a human to judge.
- Does not choose K or the conditioning (the analyst does, and the paper admits rescaling a metric changes which facet is tangent); the objective falls with K by construction so cannot select K.
- Does not choose a design; search (Section 7) and kernels (Section 10) are future work with no results.
- Does not do deflation / successive orthogonal tensions like PCA; the PCA analogy is loose and the paper says so.
- Hard to see how it handles a metric that cannot be made strictly positive and larger-is-better by a log-affine map.

## 6. Where I was confused or stopped
- Section 3: "Three objects carry the word frontier (Definition Definition 9)." The doubled word is a typo; minor.
- Section 9: "The two regimes return a 6-lemma and a 6-lemma that share 3 metrics". Fine, but the text then says the K=1 set is "total mass, slew time, energy balance, control effort, pointing error and depth of discharge" while Appendix D.3 lists depth-of-discharge exponent 0.091, and Section 6 says "one at or below 10^-12 is numerically zero". OK, consistent. But in Figure 6 (K=3) the panel for facet 1 is titled "6-lemma (6 metrics contend)", while only 5 labels appear in black with a nonzero printed exponent (slew 0.37, pointing 0.04, control 0.43, energy balance 0.14, depth of discharge 0.02) and settling time and total mass both show w=0.00 in grey. Facet 2 likewise shows 5 nonzero labels (0.02, 0.22, 0.02, 0.31, 0.43) under a "6-lemma" title. I could not reconcile the count from the figure; perhaps rounding hides a small nonzero exponent, but the paper does not say. I did not find where this is resolved (maybe in D.3 for K=3, which I only partly read).
- Section 6.2: "Each facet is fitted against all rows, as a supporting hyperplane of the whole cloud that is tightest on the facet; refitting on its own rows is ill-posed on the planted data." I understood the idea but the supporting evidence (G-6 "sliver claim, observed not proved") is only in Appendix E.
- Section 9: "The temperature is re-selected at each K by the K = 1 criterion." tau goes 38.1 (K=1), 113.2 (K=2), 195.2 (K=3) in D.2. So the mean-slack comparison 0.20 -> 0.138 -> 0.117 is across different temperatures; I do not know how much of the drop is from K and how much from tau. The text says "The objective falls with K by construction", but not about the tau confound.
- Section 5: "tau chosen so that a target fraction of designs lies above V=1" (10%). Why 10% is the right operating point is stated as a convention (G-9), and the contending set could depend on it; D.1 shows 6 metrics with w>1e-3 across most tau for primary, which reassured me, but the stock regime moves between 6 and 7.
- Section 9 candidates: "0 of them lie beyond the fitted reference surface", so Table 2 does not show any novel design; I could not tell what the table is meant to demonstrate beyond ranks.
- Table 1 cells in the text are dense, with HTML anchors in the source; fine in print.

## 7. Terms I had to guess
- "Energy differential" (log V): guessed as signed log-distance from the frontier; Definition 4 says "level offset", which I used.
- "Reach" (beta_k) and "balanced point": Definition 6 says reach is the "support value of the data in direction w_k", and R1 uses "balanced point" without a main-text definition. I guessed it is where all active exponents have equal gradient.
- "Facet share" as the analogue of explained variance: fraction of near-frontier designs on the facet; I accept this but it is not variance-like in any computed sense.
- "Posynomial" / "GGP-compatible": I know geometric programming, so OK; the paper assumes it.
- "Hyperbolic": the paper says it means the level surfaces of V (m1^w1 m2^w2 = const), unrelated to hyperbolic geometry. Fine once I read Table 1.
- "Effective sample size" n_eff: guessed 1/sum p^2 of the softmax weights; D.1 numbers (e.g. 16 out of 706) are consistent.
- "Assignment margin", "stable radius": defined in R2 and Lemma 2; understood.
- "Nondominated", "white space", "holes in the chart": guessed that holes are empty regions of chart coordinates.
- "Planted" example: understood from C.7 (synthetic data with known facets).

## 8. What I could not check
- Any code, test, or script output: the proofs are reproduced as tables quoting script lines, but I had no scripts, no data files, no way to run `uv run python -m derivation.proofmap`. So "machine-checked" is something I take on trust; I only read the lines. The hash and "236 steps" in B.3 are unverifiable by me.
- The cubesat data and the attribute simulation (Appendix C describes it; I did not verify its physics, and the text says the hardware values are illustrative).
- Whether the K=3 facets and contending sets are physically meaningful: that needs an ADCS engineer, as the paper itself says.
- Whether the algorithm recovers the planted facets: the planted example is described (C.7) and mentioned in G-6/G-7/G-15, but I did not find a table in the main text stating the recovery rate; I did not read all of D.5/D.6/D.8.
- The figures were only partly inspected (1 and 6 as images). Figure 1 is a clear schematic; Figure 6 is readable but I could not confirm the n-lemma counts (see 6).
- The claim of comparison against PCA ("the two chain") is asserted; I saw no worked example of running PCA on the chart coordinates.
- The claimed absence of prior art for the combination, and the references' accuracy (DOIs): not checked.
- The statistical question of how stable the K=3 partition is across random restarts: G-14 mentions the objective being 0.09287 on four seeds and 0.11427 on one for stock K=3, i.e. local optima differ, and the paper reports the best restart; I could not tell from the main text how often that occurs for the primary regime.

---

## LE-1

# Reader report LE-1 (EF checkout, no Docker)

## 1. What I understood the paper to be about
The paper ("Scaling Decision Analysis with Hyperbolic Trade Space Identification") proposes a way to learn the shape of a design trade space from a table of designs. Each design has configuration variables and evaluated attributes. Attributes are conditioned into strictly positive, larger-is-better "metrics". A monomial (K=1) or posynomial (K>1 facets) frontier V(m) = product of m_j^{w_j} is fitted as a one-sided envelope of the data, using a log-mean-exp soft maximum with a temperature. Its unit level set is the Pareto-like frontier. The fit also gives coordinates (position along the frontier, and log V as distance to it) and exponents that read as trade-off rates. It is a scikit-learn-style unsupervised estimator. The results are backed by SymPy lemma scripts (L1 to L14) and illustrated on an ADCS (spacecraft attitude control) trade-study case with several data "regimes". Appendices A to G cover notation, proofs, the case model, extended results, assumptions and gaps, reproducibility, and prior art.

## 2. Commands run, in order
Setup: the appendix is Appendix F of `paper/supporting_material.ipynb` (read from cells 59-68). I copied the checkout (excluding `.git`) to a scratch dir, `.../scratchpad/readers/EF-work/repo`, and ran everything there. The copy included an untracked `.venv`, which I deleted before step 1.

1. `uv sync --locked`: installed the locked environment (about 176 packages, Python 3.12). It exited 0.
2. `uv lock --check`: printed "Resolved 176 packages", exit 0.
3. `uv run pytest -q`: `2 failed, 1836 passed, 13 skipped, 1 xfailed, 24 warnings in 640.11s`. The two failures are described in section 3.
4. `uv run python -m derivation.run`: printed the lemma chain, the assumptions with "buys / when it fails", and a final "ALL LEMMAS PASS."; exit 0.
5. `uv run python -m derivation.proofmap`: "PROOF MAP OK: 14 lemma files, 236 tagged steps"; exit 0.
6. `uv run python paper/execute_notebooks.py`: printed IPKernelApp warnings about unencrypted TCP, then "executed paper.ipynb" and "executed supporting_material.ipynb"; exit 0; 75 s.
7. `cd paper && uv run myst build --html`: "Built paper.ipynb", "Built supporting_material.ipynb", "Built 2 pages", then it printed "Server started on port 3000" and GET request lines. It exited 0, and `paper/_build/html` (32 MB) exists. No error was shown, but I only saw the last 25 lines of output.

## 3. Where things broke or were unclear
- Two pytest failures, in tests that call git on this checkout:
  - `tests/test_experiments.py::test_generating_commits_touched_the_files`: `assert '' == '3864a8a4...'` from `git log`.
  - `tests/test_v2_data.py::test_the_frozen_csvs_are_untouched_since_the_start`: "the history lacks the start commit fc2363e; fetch full history".
  - I believe both are caused by my having copied the tree without `.git`, not by the code. I did not re-run them in a git checkout. The appendix says the pass condition is "all tests pass" and does not mention that tests need git history.
- F.2 "The environment of record" is a placeholder in the notebook as I received it: "Shell. The container paragraph (the pinned image, how to build it and run the paper in it, and what differs outside it) is supplied by the container work package." So the appendix does not say how to build or run the container, or what differs outside it. I did not follow it up, since I was told to stay with what the appendix points to and to avoid containers.
- F.3 says `uv run python paper/execute_notebooks.py` has a pass condition "exits 0; the outputs are unchanged when the data and the seeds are". It does not say which outputs to compare, or how. I invented my own comparison (section 4).
- The `myst build --html` step starts a server and prints "Server started on port 3000". The appendix describes it as "build the paper as a static site, written to paper/_build/html". I did not check whether the process exits on its own in a terminal. Under my harness it returned. No process was left listening on port 3000.
- F.1 lists "Node.js" as unpinned ("MyST requires 22 or newer"). I used v23.7.0, the same as in the table.
- F.4's table lists, for the figure and table rows, which function is called, what it reads and which cell it writes. It never says how to re-run a single row separately from re-executing the whole notebook; I used only the whole-notebook command.

## 4. What I regenerated and whether it matched
Compared: before running step 6, I saved the shipped `paper.ipynb` and `supporting_material.ipynb`. After re-execution I compared every cell's source and every output's data payload (text/plain, text/html, text/markdown, and image/png as base64), cell by cell.
- `paper.ipynb`: 82 cells, 0 differing cells. This includes all 8 PNG figures: they are byte-identical as embedded base64.
- `supporting_material.ipynb`: 73 cells, 1 differing cell (cell 62, the F.1 toolchain table). The only differing row is "Commit": shipped `6764529ade25e3e835300817ad101ffc0c7ee893`, mine "fatal: not a git repository ...". That is the missing `.git` in my copy. Python 3.12.12, uv 0.9.18, Node v23.7.0 and platform macOS-26.5.2-arm64 were identical to the shipped table (same machine type), as were all locked package versions.
- The proof chain (L1 to L14 all pass, 236 proof-map steps) and the HTML build were regenerated and reported success. I did not open the built HTML in a browser beyond checking that `index.html` exists and its title is "Scaling Decision Analysis with Hyperbolic Trade Space Identification".
- I did not compare numbers in the text of the paper against my own output, other than via the cell-output identity above.

## 5. What I could not do and why
- The container route (F.2): I did not try it, because of the no-Docker instruction, and the appendix text for it is a placeholder anyway.
- Confirming the two git-dependent tests pass: I copied without `.git`. I did not run them against the original checkout, since I was told not to change anything outside the scratch area (running pytest in the original could write caches).
- Cross-platform reproduction (Linux, other macOS versions): not possible here. All results came from one Apple-silicon macOS machine, and the shipped outputs appear to have been produced on the same platform, so the byte-identical match may not carry over to other platforms.
- A visual check of the built site in a browser.

## 6. Terms or steps I had to guess
- "Clean kernel", "outputs unchanged": I took this to mean cell outputs in the executed notebooks, and compared them as described in section 4.
- I assumed the appendix commands are meant to be run from the repository root, in the order listed, and that `paper/execute_notebooks.py` overwrites the notebooks in place (which is why I ran it on the scratch copy).
- I read "uv sync --locked" as including the dependency group `paper` (needed by the notebook execution and myst). This worked without extra flags.
- I treated the F.4 table's "Writes: cell X of Y.ipynb" as meaning the output is the stored cell output, not a separate file.
- The `.venv` in the checkout: I deleted it in my copy and rebuilt, on the assumption that a reader would start without one.

---

## LF-1

# LF-1: reader run on make_frontier_data(300, 4, n_terms=2, random_state=777)

Scripts: /private/tmp/claude-501/-Users-z--claude-spares-spare-4Zb8mW/71474a52-35d3-48fa-82b0-c1328e96b5d6/scratchpad/readers/EF-work/F/s1.py to s6.py

## 1. Commands and output (abridged)

Setup, from Appendix F.3 (supporting_material.ipynb, cell "commands"; F.2 "environment of record" is an empty placeholder: "The container paragraph ... is supplied by the container work package"):
- `uv sync --locked` -> "Resolved 176 packages ... Audited 137 packages", exit 0.
- `uv lock --check` -> "Resolved 176 packages", exit 0.
- `uv run pytest -q -x` -> I started it, it ran past the 2-minute foreground limit and went to the background. I did not wait for the result, so I have no pass/fail for the suite.
I did not run the derivation, myst build or execute_notebooks steps (not needed to use the package).
The route to "my own table" is docs/getting-started.md and docs/user-guide/{fitting,termination,tensions,limitations}.md (the appendix itself only says use on one's own table "is on the docsite").

Data (s1.py): X shape (300,4); min per column 0.002, 0.010, 0.004, 0.010; max 8.5, 6.6, 16.5, 5.5; medians 0.61, 0.57, 0.46, 0.54. Log-std per column 1.29, 1.10, 1.32, 1.11. Log-correlations all positive, 0.13 to 0.36. So the columns are on a comparable log scale and I did no conditioning.

K=1 (s1.py): `HyperbolicTradeSpace(temperature=20.0).fit(X)` -> exponents [0.192 0.324 0.112 0.372], frac_above_ 0.177, n_eff_ 40.9, termination_.status `not_applicable`, conditioning_ 2.07. `select_temperature(X, target_frac_above=0.10, bounds=(3,1000))` -> 54.77; refit at that tau: exponents [0.19 0.33 0.11 0.37], frac_above 0.097, n_eff 17.0, conditioning 0.92. `tension_report` -> contending [0 1 2 3], "4-lemma".

K sweep, tau=50, 3 seeds each (s2.py): every fit for K=2, 3, 4 reported `certified`, max_gap about 1e-15, no warnings.
- K=2: exponents [0.14 0.29 0.05 0.51] and [0.26 0.36 0.18 0.20], shares [0.5 0.5], gamma 0.0028, radius 1.4e-4, n_eff 90.5, conditioning [16.7, 28.9], frac_above 0.337. Identical for seeds 0, 1, 2 (rows permuted).
- K=3: the same two facets plus a third [0.31 0.16 0.11 0.42] with share 0.12 (the other two shrink to 0.46/0.42). gamma 0.0018.
- K=4: the same two facets plus two small facets (shares 0.11 to 0.23), gamma 0.0009 down to 0.00016 depending on seed.

Per-K tau (s3.py): `select_temperature(..., target_frac_above=0.10, n_terms=K)` raised ValueError for K=2,3,4: "target frac_above 0.1 is not bracketed by bounds (3, 1000): frac_above_ is 0.543 at tau=3 and 0.300 at tau=1000". With target 0.33: K=2 tau 54.8, K=3 tau 113, K=4 tau 1000 (the upper bound). Same exponents for K=2.

Objective at fixed tau=50 (s4.py): K=1 -0.0695, K=2 0.5698, K=3 0.5583, K=4 0.5540, K=5 0.5506. K=2 over 10 seeds: 0.56984 every time. K=3 over 10 seeds: 0.5583 nine times and 0.5640 once.

Tension reports, K=2, tau=50, `tension_report(ts, X, band=0.15)` (s4.py): both facets "4-lemma", contending [0 1 2 3]. Facet 0 exponents [0.142 0.292 0.055 0.512], facet 1 [0.255 0.363 0.18 0.202]. Exchange-rate matrices: on facet 0 metric 3 dominates (e.g. rate[0,3] = -3.6, rate[2,3] = -9.4; rate[3,j] about -0.1 to -0.6); on facet 1 the rates are all within roughly -0.5 to -2. Default band (1/tau=0.02) gave `ValueError: facet 0: only 5 near-frontier rows (|log V| < 0.0182574) but min_near_frontier = 10; use a larger band ...` for the K=2 fit at tau=54.8.

Bootstrap (30 resamples, tau=50, s4.py): K=2: all 30 `certified`, exponents' sd across resamples 0.00 for both facets. K=3: the two big facets sd 0.00, the third facet's exponents sd 0.06 to 0.16.

tau sensitivity K=2 (tau = 20, 50, 100, 300): all `certified`, exponents move by at most 0.02 (e.g. 0.28 to 0.30 on metric 1 of facet 0).

## 2. Reading

The table has two regimes, two facets, split evenly (50/50 of rows). All four metrics contend on both (a 4-lemma each), so no metric is free in either regime. What differs is who gives way to whom:
- Facet A (exponents about 0.14, 0.29, 0.05, 0.51): metric 3 carries half the weight and metric 2 almost none (0.05). Along this facet a small give in metric 3 buys a lot in the others (rates -3.6 and -9.4 in the metric-3 column), and metric 2 is the cheapest to sacrifice in the rate-matrix sense but also barely binds.
- Facet B (about 0.26, 0.36, 0.18, 0.20): near-balanced; metric 1 is the heaviest, metric 3 has dropped from 0.51 to 0.20, and metric 2 rises to 0.18. Trades there are roughly one-for-one to two-for-one.
So the pull between metric 3 and metrics 0/1/2 is what changes between regimes. A single-facet fit (0.19, 0.32, 0.11, 0.37) averages the two and describes neither; it also has n_eff 17 vs about 90 for K=2.
I read K=2, not 3 or 4. Reasons in section 3.

## 3. Trustworthiness

- `termination_.status == certified` for every K>=2 fit, max_gap about 1e-15, no ConvergenceWarning, positive margin gamma (0.003) and radius (1.4e-4). Per the termination page that means the returned run is a local optimum of its fixed assignment (not global; says nothing about other restarts).
- K=1 shows `not_applicable`, which the page says is "Not a failure". It gives no convergence claim, so for K=1 I had only max_gap (1e-6) and frac_above.
- Restart stability: K=2 gave the same exponents and the same objective for all 10 seeds. Bootstrap resamples gave the same exponents (sd 0.00) in 30/30 `certified` fits. tau between 20 and 300 moves exponents by 0.02 at most.
- Choosing K: the docs say "where you choose K" and give no rule. My rule: at fixed tau the objective is highest at K=2 and falls for K=3,4,5 (reading "higher is better" is my guess, see section 6); K=3's extra facet is unstable (sd up to 0.16 under bootstrap, one seed in ten found a different optimum, 0.5640) while the two big facets are untouched; its share is 11 percent. The K=3 and K=4 extra facets look like splinters of the K=2 facets, not a new regime. The radius and gamma shrink as K grows (gamma 0.0028, 0.0024, 0.0007 at K=2,3,4), so "certified" is weaker evidence at larger K.
- Caveats I could not remove: gamma and radius are tiny in absolute terms (1e-4 to 1e-3), and I don't know what size counts as comfortable. The zero bootstrap sd could mean the facets are pinned by a few extreme rows (n_eff 90 of 300 suggests a modest set) and a bootstrap that keeps those rows reproduces them exactly; it does not show the fit is right, only stable. frac_above is 0.34 not 0.10 because multi-term fits cannot reach 0.10 on this table.

## 4. Where things broke or misled

- docs/user-guide/fitting.md: "Each training row's facet is `facet_`, and `coefficients_` and `facet_share_` hold the facets' posynomial coefficients and shares." There is no `facet_share_` attribute: `AttributeError: 'HyperbolicTradeSpace' object has no attribute 'facet_share_'`. The shares are in `termination_.shares`.
- fitting.md: "Re-select tau when you change the number of terms." I tried `select_temperature(X, target_frac_above=0.10, bounds=(3,1000), n_terms=K)`; for K>=2 it raises the "not bracketed" ValueError above. The page says the default 0.10 is "a common start" for real data and the 0.35 target is specific to the synthetic table; I could not tell what target to pass for a table I did not know, and used 0.33 after seeing the fraction at tau=1000. For K=4 the answer was the bracket end (1000).
- tensions.md: "A facet with fewer than `min_near_frontier` (default 10) near-frontier rows raises `ValueError`; widen `band`..." It does say so, but with the default band (1/tau) on the very first K=2 report call it just raised, so the first attempt to read a multi-term table fails; I had to pick band=0.15 with no guidance on its size.
- Appendix F.2 ("The environment of record") is a placeholder sentence, so the appendix gives no environment narrative; the commands in F.3 are enough to set up.
- termination.md says gamma is `inf` at one term; I got `nan` for gamma and radius at K=1 (status `not_applicable`).
- Nothing in the docs says how to choose K from the output (no K-selection function or comparison of `objective_`); the limitations page says only that a multi-term fit is a "local optimum chosen among seeded restarts" and that K is yours.
- The tau for K=2 and `frac_above_` are tied together: the docs example text says the synthetic table "puts 30 percent of its rows on the planted frontier", so frac_above floors near 0.3. That sentence is in the single-term tau paragraph; I had to infer it carries to K>1.

## 5. Reading versus planted truth (`info` opened only now)

Planted: 2 facets, 150 rows each, 90 frontier rows (30 percent), noise 0.0, interior_scale 1.0, exponents [0.137 0.299 0.053 0.511] and [0.251 0.364 0.181 0.204].
- Facet count: matched (2). K=3 and K=4 splinters were artefacts, as I judged.
- Exponents: facet A fit [0.142 0.292 0.055 0.512] vs planted, L1 distance 0.014; facet B [0.255 0.363 0.18 0.202] vs planted, 0.008. Matched to the second decimal.
- Row assignments: 297 of 300 rows in the same facet as planted (149/150 and 148/150 after allowing for label order); all 90 frontier rows assigned to the correct facet.
- Contending metrics: planted exponents are all positive in both facets, so the 4-lemma on both is right.
- My regime description (metric 3 weight 0.51 vs 0.20) matches.
- Nothing in my reading missed or overclaimed. The one thing I could not have known from outputs alone was whether the stability evidence (sd 0.00) was telling me the fit was right; the generator confirms it was.

## 6. Terms I guessed

- "objective_" direction: I assumed larger is better after seeing K=1 -0.07 and K=2 0.57. The docs describe "mean slack" and descent but do not say what objective_ means or which way is better, and K-comparison on it is my own device.
- "gamma" and "radius": I took them as the assignment margin and the perturbation radius per the termination page, but I do not know what magnitude is large enough.
- "n_eff_": taken as an effective number of designs carrying the fit (weights from the soft max); no formula read.
- "frac_above_" being near 0.3 as a floor for multi-term fits: inferred from the sentence about 30 percent of planted rows on the frontier; not stated for real tables.
- "band" in tension_report: assumed to be a width in log V; picked 0.15 by trial.
- "4-lemma": taken as "four metrics contend", per the tensions page.
- "conditioning_" values (0.9 to 500): I only know small means weakly identified; no threshold given.

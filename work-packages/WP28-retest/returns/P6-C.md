# P6-C

A note on procedure: I read each part of the text in one pass and opened the figure images after finishing the part that holds them, not at the line that names them. Figure 1 I saw before part 3. Figures 2 to 4 came after part 3, and Figures 5 to 9 after part 4. The figure-by-figure stumbles below are from the images and captions together.

## 1. What this is about

The paper proposes a way to analyse a trade study. The input is a table of N evaluated designs. Each design has d "metrics": strictly positive numbers, larger is better, produced by transforming raw attributes. The method takes logs and fits a one-sided piecewise-linear convex envelope to the cloud.

In its simplest form (K = 1) the envelope is a single hyperplane, w·log m = β, with w on the simplex. The weights w are the exponents of a weighted geometric mean (a Cobb-Douglas form with constant returns). The fit is a soft maximum, log-mean-exp, minimised over w. A temperature τ is chosen so that about 10% of designs lie beyond the surface.

With K > 1 there are K such hyperplanes. The envelope is their maximum, or a soft version of it. The authors call it a posynomial. The default fit is actually the sharp maximum.

The authors then read the fitted objects in a fixed vocabulary:
- The exponent vector of a term gives local exchange rates between metrics ("elasticities").
- The metrics with non-zero exponent form an "n-lemma".
- log V, a design's signed distance from the surface in log units, is the "energy differential".
- The remaining coordinates are a "chart" that is reversible.

The case is a simulated cubesat with 8 attributes. The paper shows that K = 1 gives one 5-metric tension and K = 3 gives three different contending sets. It compares two controller regimes. It also does a small "propose, predict, check" exercise. The paper sets itself against PCA ("explains variance") and against Pareto dominance, and says it makes no priority claim.

## 2. The main results, as I now understand them

**Model.** V(m) = exp(w·log m − β). It is a weighted geometric mean, homogeneous of degree one, so doubling every metric doubles V. V = 1 is the fitted surface. log V is negative inside and positive beyond.

**Three objects called "frontier".** These are the fitted surface at finite τ, which some designs exceed; the supporting envelope at τ = ∞, which none exceeds; and the true Pareto boundary. The paper says only the first is fitted, and it is not the third.

**Convexity.** For K = 1 the objective is convex in w (log-mean-exp is convex). Every minimiser is global. Uniqueness is not claimed. The log-mean-exp has a 1/N normalisation, so β describes the shape of the data and not its size.

**Reading.** Along a facet, dlog m_j / dlog m_i = −w_i / w_j. Scaling a design's metrics by 1/V puts it on the surface. The chart is an orthogonal rewriting that separates overall level from position.

**Pareto link.** A maximiser of V with positive exponents is Pareto-efficient. The converse is explicitly not claimed.

**Several terms.**
- The fit is not convex in the terms. The proof is a symmetry argument plus Jensen.
- It is an alternation in the style of Magnani and Boyd.
- Three levels of guarantee are given:
  - descent, with a trivial K^N bound on iterations;
  - a numerical stationarity measure called the term gap;
  - local optimality inside an assignment-stable neighbourhood, where the assignment margin is positive.
- A soft fit has a second-order certificate.

**Open questions.** Global convergence of the alternation (Q1), statistical consistency (Q2), identifiability of the active metrics (Q3), and whether the fitted surface recovers the Pareto boundary rather than the sample's envelope (Q4) are all stated as not established.

**Cubesat numbers.**
- 706 of 1000 designs are feasible.
- The nondominated set is 126 of 706 on 4 attributes and 659 on 8.
- At K = 1 the support is {total mass, energy balance, pointing error, depth of discharge, settling time}, with exponents 0.14 to 0.36.
- At K = 3 the contending sets have sizes 4, 5 and 5. Control effort leads term 1 and peak slew power leads term 3.
- Term shares are 0.03, 0.24 and 0.72.
- The elasticity of total mass against energy balance on term 2 is about −1.7.
- Mean slack drops from 0.243 to 0.182 to 0.146 as K goes 1, 2, 3. The authors say this cannot choose K.
- The K = 3 fit is "certified", but only for perturbations about 70 times smaller than the band, and 11 designs sit within the band of a seam.

**Planted-table recovery.** On 20 synthetic tables with three planted terms, all three terms are recovered to within 0.05 in 16 tables. The four failures are those whose thinnest term has 5, 5, 6 or 11 frontier rows.

**The "propose, predict, check" test.** It rests on three proposals that are really two designs. All three fail the depth-of-discharge requirement. The authors present it as illustration only.

## 3. What I would do next with it

I would test the claim that this is not just a known estimator, using a controlled experiment.

1. Take a DEA test bed with a known frontier. Use a multi-output technology with a constant dummy input, so that "all metrics larger is better" is the output-oriented case. Run three estimators on simulated samples: this method at K = 1, 2, 3 and a few τ; output-oriented multiplicative DEA / piecewise log-linear envelopment; and a quantile or order-α partial frontier. Compare four things: recovered facet normals, recovered scores V against the Farrell radial score, bias as sample size grows, and bootstrap variability of the exponents. This is Q2 to Q4 done by experiment.
2. Check whether the exceedance fraction (the 10% rule) is functionally a robustness parameter of the partial-frontier kind. I would vary it and see whether the facets move as an order-m or α-quantile frontier's would.
3. Test sensitivity to conditioning: rescale one metric and see how the exponents and the contending set move. The paper admits they move.
4. Run a leave-out or resampling stability study of the K = 3 sets on the cubesat, with fresh draws and not rounding-level jitter, and in particular for term 1, which has 3 near-frontier designs.
5. Try a standard DEA data set (hospitals, banks) and see whether the "n-lemma" reading adds anything to what facet weights already say.

## 4. What I would tell a colleague

It is a careful, very honest, unusually self-limiting paper, written for systems engineers and not for efficiency measurement. The estimator is, to my reading, a smooth, small-K, log-space output-oriented envelope. The envelope is convex in the logs and of Cobb-Douglas facets with exponents on the simplex, with the aim of reading tradeoffs and not scoring units.

The part that is substantively different from textbook DEA, as I see it:
- It fits a small number of global facets and does not give every unit its own weights. This is a form of regularisation. A full DEA frontier has many facets and could be coarse-grained to match.
- It uses a soft maximum with a tunable exceedance fraction, so it is a robustified or quantile-like envelope. Its effective sample size is reported, which is what one wants from a robust frontier.
- It reports solver status and certificates, and ships as a scikit-learn transformer.
- The reading rule (support set, exponents as elasticities, a chart of position against level) is a tidy presentation of what facet multipliers already give.

The part that I think is mostly terminological or standard:
- The "n-lemma" is the support of a facet's multiplier vector.
- The "invariant value" is the Farrell/Shephard radial distance in Cobb-Douglas form.
- "Maximiser of a positive-weight geometric mean is Pareto-efficient" is textbook scalarisation.
- "Energy differential" is a log efficiency score.
- Homogeneity, shift-equivariance, the convexity of log-mean-exp, and the orthogonal chart are routine.

The paper does not say what DEA does with the same data. There is no comparison run against DEA or against a partial frontier. The case shows the method working, not beating or matching anything.

## 5. What the method does not do, and what the paper does not claim

The method does not:
- estimate the Pareto boundary. The paper says the fitted surface is not that, and Q4 is open;
- give any uncertainty for exponents, any consistency result or bias analysis (Q2, Q3);
- choose K, or choose τ other than by the fixed 10% convention;
- find a global optimum for K > 1;
- handle non-log-convex boundaries (dents and holes);
- handle inputs, outputs or returns to scale, because there is one simplex-constrained constant-returns form;
- give causal or exchange-rate meaning to elasticities. The paper says they are descriptive of the sampled and conditioned table;
- give conditioning-free results. Rescaling a metric changes which term is tangent.

The paper does not claim:
- priority or novelty beyond "combining these pieces";
- that the converse of the Pareto theorem holds;
- that the three terms are orthogonal or that a PCA-style deflation works;
- that the contending sets are unique when columns nearly coincide (energy balance and power margin);
- that the propose-predict-check procedure has a measured success rate;
- that the search section has any result;
- that the formal derivations show the hypotheses suit a given table. That is left to "human validation".

## 6. Where I was confused or stopped, in the order I met it

1. Abstract: "PCA is trusted as reproducible and interpretable, and explains variance. We explain tensions." I read "explain tensions" as a slogan. I expected the abstract to say what quantity is estimated. It comes only later and is a facet's exponent vector.

2. Abstract: "A fitted posynomial reference surface models the data underlying the table, not the Pareto boundary." Then, in Section 5, the fits of record use "sharp weights ... κ = ∞". That is a maximum of monomials, a max-affine function in the logs. It is not a posynomial unless κ is finite. I could not tell whether "posynomial" in the abstract is the model class or the soft option.

3. Section 1: "the nondominated set holds 126 on 4 attributes ... and 659 on 8, all of them". There are 706 feasible designs, so 659 is not all of them. I expected either 706 or a different phrase.

4. Section 1, first main-results bullet: "The fitted reference surface is where the invariant value ... equals one (Theorem 1)". V is defined with β subtracted so that V = 1 on the surface, so this reads as a definition. Theorem 1, as stated later, is only homogeneity and a shift.

5. Table 1, DEA row: "global exponents per term, not per-unit weights; a band, not extreme units". In DEA, units on the same facet share a multiplier vector, so I expected the contrast to be "K facets against as many facets as the data give". The cell does not say that.

6. Section 2, DEA paragraph: "We differ in what the envelope is." The reference list includes Charnes, Cooper, Seiford and Stutz (1982, 1983) and Banker and Maindiratta (1986). Their titles are "A Multiplicative Model for Efficiency Analysis", "Invariant Multiplicative Efficiency and Piecewise Cobb-Douglas Envelopments" and "Piecewise Loglinear Estimation of Efficient Production Surfaces". These names are not cited in the main text I was given. I expected them to be the comparison, because they are the closest known estimators. I stopped here for a while.

7. Section 2: "Combining these pieces in one estimator is our design. We did not find the combination in the sources reviewed". I could not tell from the main text what the combination is, beyond soft maximum plus simplex plus small K plus certificate.

8. Section 3, Definition 1: "Three objects". Later text uses "frontier" without saying which. Definition 5 says "the position along the frontier". Theorem 5 says "the frontier is the hyperplane". I could not tell which of the three objects was meant.

9. Section 4: "doubling every metric doubles it. It stays the same along a trade-off, hence invariant." The first half says V scales with the metrics. The second half says V is constant along a trade-off. "Invariant" for the second is natural, but V is homogeneous of degree one, which is not what "invariant" usually means. I read it as invariant along the level set.

10. Definition 2 and Definition 7: V uses β, which is the "reach" of Definition 7, a later definition. At finite τ, β is a soft maximum, yet V = 1 is called the "surface" while about 10% of designs are above it.

11. Definition 4: "one inside the band weighs within a factor e of one on the surface". I could not parse "weighs" without the softmax weights. I guessed it means a softmax weight within a factor e.

12. Definition 6: "the support (exponents above 10^-9) of the exact-maximum (τ = ∞) fit to the term's cell, centred on the cell's mean log-metric". Then, in Section 6.2: "Refitting a term on its own rows alone ... is ill-posed ... the refit of record is f_k over all rows. The contending set's exact-maximum fit on the cell is f_k itself on the cell's rows (Definition 6), not that plain fit." I could not work out whether f_k uses all rows or only the cell's rows. The second sentence reads as a contradiction of the first.

13. Section 5, equation (1): minimise the soft maximum of w·u_i over the simplex. If u is not centred, minimising the largest score over the simplex tends toward the metric with the lowest log values. I expected an explicit normalisation in the objective. The centring is acknowledged only in Section 8 ("this conditioning centres each log-metric ... on uncentred log-metrics the two differ ... and need not share a minimiser"). Until then I was unsure what equation (1) meant.

14. Section 5, R1: "the balanced point, the support-weighted mean of the log-metrics U^T p (its components on the support of w equal, Theorem 2), lies in the relative interior of a facet of the supporting envelope with positive normal". I needed several reads. I guessed it says that the exponents are identified when the optimum sits in the middle of a facet and not on an edge.

15. Theorem 2: "for the facet-normal reading, w_j > 0 for every j there (R1's relation at the fit temperature, Appendix B, L3.9)". The statement bundles three conditions and a pointer into an appendix. I could not tell what the theorem concluded for a reader who stops at the box.

16. Theorem 9: "at K > 1, κ = ∞, through an active term". I could not tell what "through an active term" modifies.

17. Section 6.2, before Theorem 11: "Level 1 ... within K^N + 1 iterations". I expected a rate or a convergence statement. A bound of K^N is the number of partitions and says almost nothing, so I was unsure whether it was meant as a result.

18. "Numerical" paragraph: "the local optimality certified covers changes about 70 times smaller than the band". Margin 0.00121 against stable radius 0.0001209 against band 0.0088. I followed the numbers, but I could not tell what the certificate protects for a reader. The text itself says that which term 11 designs fall to is "not a finding".

19. Section 8, Figure 3 caption: "the measured slew supplies the settling time and the control effort, which the analysis passes on, and the analysis computes the other six, pointing error and total mass from the configuration alone." Six plus two does not parse. The figure's purple box says "returns 7 of 8 metrics, computed with no slew: pointing error, total mass". I could not reconcile the counts. This is the cubesat model and not central.

20. Figure 4 and its text: "the effective sample size is 23.1 designs" and then "the exponents at the fit temperature rest on about 25 of the 706 designs". I read 23 and 25 as two numbers for one quantity and could not tell which is meant.

21. Section 9, "A known answer": "recovers all three terms to within 0.05 in 16". I could not tell the norm for "within 0.05" (each exponent? the vector?). The failures have 5, 5, 6, 11 frontier rows on the thinnest term. Later, the cubesat's term 1 has 3 near-frontier designs of the ten the reading needs, and yet its contending set is reported (control effort at 0.40, etc.). Under the paper's own planted test, term 1 is below the point at which recovery failed. I could not square these.

22. Figure 6, bottom panel (term 3): the dark points sit on discrete horizontal bands, and a cluster is about 1.5 log-units below the line. The caption says the dark points are those whose other six metrics are near the median. I take that to mean dark does not mean "near the line". The text says "its elasticity is read across the swapped parts' alternatives rather than along one continuous trade". I expected a term's slope to be a trade-off, and here it is a line through a step-function catalogue. In Figure 8, term 3's two leading metrics have association −1.00. I read that as a deterministic relation created by the catalogue of parts and not a trade-off found in the data.

23. Figure 7: "the first principal direction of the near-frontier chart ... a reading of the sampled designs and not part of the model". The paper's pitch is "PCA explains variance, we explain tensions". Its main picture of the chart, though, uses PCA to choose the x-axis, and the x-axis carries 44% of the spread. I could not tell how this figure shows anything the method adds. It reads as a plot of log efficiency scores against a principal score.

24. Figure 8, term 3: "energy balance w = 0.00" is outlined as a member, and "power margin w = 0.02" is not. The association between them is 0.99. I understood from the caption that an outlined metric can be grey, but I could not see how the support is chosen when two metrics are near copies. Section 9's "identical columns" paragraph says as much about a pair.

25. Section 9, elasticity: "one percent gained in energy balance is 1.7 percent given up in total mass". This is −w_energy / w_mass, 0.42/0.24 = 1.75. I could check that. But the units are the conditioned metrics, which are log-affine functions of the raw attributes with a data-dependent scale and a shift. A percent of a conditioned metric is not a percent of kilograms or watt-hours unless the scale is one and the shift is zero. I expected the text to say which.

26. Section 9, candidates: "The 3 measured candidates have lowest energy differential −0.197 and highest −0.153, and 0 of them lie beyond the fitted reference surface." Hand-named designs scoring inside the surface is expected, so I could not tell what this shows.

27. Section 9, "Of 3 proposals ..." with Section 10: "Two of the three proposals are one configuration". So the effective count is two. The text says so honestly, but I stopped at "3 of 3" and "1 of 3" being reported as rates.

28. Section 10, "Requirements after the fit": "changes the one-term contending set by at most one of its five metrics, so on this case pre-imposing the requirements does not change what the frontier trades". One of five is 20% of the set. I could not tell why that counts as no change.

29. Section 10, "Why a frontier": "An answer far from the frontier is hard to justify, and the analysis must rerun on empirical data to support configuration management." I could not parse the second clause as a reason for a frontier.

30. Section 8: how the 1000 designs were drawn is not in the main text. Section 10 says "Designed samples, such as grids, are not independent observations". I could not tell whether the cubesat sample is random, a grid, or something else, and the answer matters for everything about exponents.

31. The title's "hyperbolic". Section 4 says it is the level curve m1^w1 m2^w2 = const in two metrics. For d metrics and unequal weights I do not see anything hyperbolic beyond that. I stayed puzzled about why it earns the title.

## 7. Terms whose meaning I had to guess

- **"Tension" (abstract, throughout).** My guess: a facet with a non-trivial set of metrics trading against each other, that is, negative local exchange rates.
- **"Energy differential" and "level".** log V, which is a log of the Farrell radial score.
- **"Reach" (β).** The soft maximum, over designs, of the score along w.
- **"Cell".** The set of designs that a term scores highest.
- **"Balanced point".** The softmax-weighted mean of the log-metrics.
- **"Contending set" and "n-lemma".** The support of the exponent vector. The "n" is its size.
- **"Participation threshold" (10^-3).** The cutoff below which an exponent is treated as zero when reading elasticities.
- **"Slack" (mean slack).** The average of β_{k(i)} − w_{k(i)}·u_i, the average distance below the surface. I took it to be the fit's objective.
- **"Certified", "stationary".** Solver statuses named by what is checked: certified is assignment fixed plus small gaps plus positive margin, and stationary is small gaps without the curvature check.
- **"Term gap".** A duality-gap-like number: the gradient dotted with w minus its smallest component.
- **"Margin" (γ) and "stable radius".** The smallest lead of a design's best term over its runner-up, and a perturbation size below which assignments cannot change.
- **"Near-frontier band".** The designs with |log V| < 1/τ.
- **"Conditioning".** Per-attribute log-affine preprocessing into metrics: orientation, shift, scale.
- **"Pull-back".** Writing V as a function of the raw attributes by substituting the conditioning.
- **"Position along the surface".** The chart coordinates Z, which are orthonormal log-ratio coordinates with the overall scale removed.
- **"Weakly efficient".** Cannot be improved in all metrics at once but might be improved in some without loss.

## 8. Questions I am left with

- Which of the case's findings survive a resample of the 1000 designs, not a rounding perturbation?
- Does a multiplicative DEA or piecewise log-linear envelope with K facets and the same data return the same exponents and the same term supports? The paper does not say.
- Is the 10% exceedance rule equivalent to a known partial frontier (quantile, order-m, expectile)?
- How does the choice of τ interact with the sample size? At τ = 38 the effective sample is about 23 designs. How stable is the K = 1 support at that size?
- Under what conditions does the fit approach the true boundary when the sample is dense near it? That is Q4. Is there even a heuristic?
- What is the sampling plan for the 1000 designs?
- How should I choose K when the paper says slack cannot?
- Why would an engineer prefer exponents of conditioned metrics, scaled to unit log-spread, to facet multipliers in physical units?
- What happens to the terms when two metrics are near copies, as energy balance and power margin are? Is the support then an artefact?
- What does the n-lemma reading add when a term's slope is a step function across catalogue choices, as for term 3?
- How would I run this with inputs as well as outputs?

## 9. Whether I would read the appendices

Yes, but selectively.

- **Appendix G**, the prior-art register. I want to see how the paper handles the multiplicative DEA and piecewise log-linear entries that appear in the reference list. That decides how I read the novelty claim.
- **D.11 and D.14.** These hold the digits that survive perturbation and the planted-table recovery. They are the only empirical support for the identification claim.
- **E**, the gaps ledger, for Q1 to Q4 and for the effect of conditioning.
- **B**, the proofs, only enough to see whether L15's iteration bound and L17's certificate say more than their one-line statements in the main text.
- **D.5 and D.15**, to see how the τ choice and the K comparison are handled.
- **C**, only to find how the cubesat sample was drawn, if it is there.

I would skip the SymPy scripts. They are checks of routine algebra.

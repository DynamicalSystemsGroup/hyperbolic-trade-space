# P4-B

## 1. What this is about

As far as I can tell, this is an unsupervised method for a table of designs (rows) by metrics (columns). Every metric is strictly positive and larger-is-better, which you get after "conditioning": the cost-like quantities are inverted, so mass becomes "inverse kg", for example. The method works in log space, u = log m. It fits a hyperplane w·u = β, with w on the probability simplex, against the *outer edge* of the cloud rather than through its middle. A soft maximum (log-mean-exp at a "fit temperature" τ) controls how hard it hugs the edge. Back in metric space that hyperplane is a weighted geometric mean V(m) = e^{-β} ∏ m_j^{w_j}, and the "fitted reference surface" is V = 1. With K > 1 terms you take a smooth maximum of several such hyperplanes (a log-sum-exp at a "term temperature" κ). In metric space that is a posynomial, so the surface becomes piecewise and convex in log space. Rows are assigned to whichever term scores them highest, much like k-means with hyperplanes instead of centroids.

The output reads like a transform. Each design gets a level, log V (0 on the surface, negative inside, positive beyond), and a position along the surface, Z = Bu. Here B is an orthonormal basis of the complement of the all-ones vector, which reminded me of the centred log-ratio coordinates from compositional data. The exponents w are read as elasticities: along the surface, a 1% gain in metric i costs w_i/w_j percent of metric j. The metrics that carry nonzero exponent in the exact-maximum fit are called the "contending set", and its size gives a name: dilemma, trilemma, "n-lemma".

The worked case is a small satellite (a "cubesat") with swappable parts and tunable parameters, 8 traded metrics, and two controller "regimes". So it is a dimensionality and structure reading of a trade-off frontier, aimed at engineering design studies.

How I would file it:
- **Family:** frontier or boundary estimation, a max-affine model in log space. It sits nearer to support-function and convex-hull estimation, or to one-class boundary methods, than to PCA. Its K > 1 version is a clustering-like alternation.
- **Assumptions:** strictly positive metrics, oriented so larger is better; scale-free (the fit is unchanged by a uniform shift of all log-metrics, Proposition 1); the exponents are nonnegative and sum to one.
- **Fitting:** a convex minimization over the simplex for K = 1 (a geometric program in the log variables; every minimizer is global, but the minimizer need not be unique). For K > 1 it alternates between assigning rows and refitting each term.
- **Transform:** (Z, log V), a reversible rewriting of the log-metrics.
- **When I'd pick it over PCA:** when I care about the edge of what is achievable and the exchange rates along it, not about the directions of greatest variance. The paper also runs PCA *on top of* the chart, among the near-frontier designs.

## 2. The main results, as I now understand them

- **The form (Theorem 1).** V is homogeneous of degree one: double every metric and V doubles. V = 1 defines the surface, and log V = w·u − β. The surface is *not* the Pareto boundary. Definition 1 separates three objects:
  - the fitted reference surface (finite τ, some designs lie beyond it);
  - the supporting envelope (τ = ∞, none lie beyond it);
  - the Pareto boundary (a property of the system, not of the fit).
- **The fit (Theorems 2 and 3).** The one-term fit is convex in w, with an explicit gradient Uᵀ softmax(τUw) and the usual simplex KKT conditions. Convexity is not strict, so uniqueness is not claimed.
- **The soft maximum (Theorem 4).** Log-mean-exp lies between the mean and the maximum and tends to each in the limits. It differs from log-sum-exp by log N / τ.
- **Noise (Proposition 2).** Under Gaussian noise, the soft maximum adds τσ²‖w‖²/2. This is a population identity, not a consistency result.
- **Reading the fit (Theorem 5).** The exponents give elasticities. Improving metric j alone by V^{-1/w_j}, or every metric by 1/V, brings a design onto the surface.
- **The chart (Theorem 6).** (Z, log V) is a bijection with u; the overall scale is factored out.
- **Pulling back (Theorem 7).** The fit can be pulled back through an invertible log-affine conditioning to the raw attributes. A negative product w_j·α_j marks a cost attribute.
- **Several terms (Theorem 8).** The K-term model is a posynomial and lies within log K / κ of the hard maximum of the terms.
- **Efficiency (Theorem 9).** A design that maximizes V is weakly Pareto-efficient, and efficient when every w_j > 0. The converse is not claimed.
- **Guarantees for K > 1 (Theorems 10 and 11, Lemmas 1 and 2, Proposition 3, Corollary 1, Theorem 12).** The fit is not convex in the terms. There are three levels of guarantee:
  1. Each accepted iteration does not increase the "mean slack", and the hard alternation stops in finitely many iterations (K^N + 1).
  2. A per-term duality-type gap certifies how close each term is to its own optimum.
  3. If no row's assignment would change under small moves (positive margin), the result is a local minimum.

  The soft version has a second-order certificate.
- **The case.** On the cubesat, one term blends trade-offs that three terms separate. In the primary regime the K = 1 fit is a 5-lemma: total mass carries the most weight (0.36), then energy balance (0.18), then pointing error, depth of discharge and settling time; control effort, power margin and peak slew power get zero. The K = 3 terms pick out different heavy pairs:
  - term 1: settling time and control effort;
  - term 2: total mass and energy balance;
  - term 3: pointing error and peak slew power.

  The stock regime gives a different 5-lemma, led by control effort and settling time.

## 3. What I would do next with it

- Look for the package's estimator. The main results mention "the package"; I would expect fit, transform → (Z, log V) and inverse_transform.
- Run it on a dataset where I know the frontier. Figure 1's synthetic planted-terms example is the obvious first check.
- Then put it in a pipeline after a conditioning step (a log, an inversion of cost columns) and compare what PCA on the raw logs gives me against what this gives me on the edge.
- Sweep τ myself, as Figure 4 does, to see how fragile the support is. I would also try K = 1, 2, 3 to see whether the extra terms are stable across restarts. The paper says its certificate covers only the returned run.

## 4. What I would tell a colleague

"It's a frontier-fitting cousin of PCA for positive, larger-is-better metrics. Take logs and fit a soft supporting hyperplane with simplex weights to the top edge of the cloud. The weights are elasticities, meaning exchange rates between metrics along the edge, and the number of nonzero weights tells you how many metrics are really in tension (dilemma, trilemma, ...). The transform gives every point a distance-to-edge (log V) and a position along the edge. With several terms it becomes a piecewise surface fitted by a k-means-like alternation, with honest, narrow guarantees. The edge it fits is a fitted level, not the Pareto set; there's a temperature knob, and they set it by a convention (10% of points above the surface)."

## 5. What the method does not do, and what the paper does not claim

- It does not estimate the Pareto boundary. The surface is a fitted level that some designs exceed by construction.
- Uniqueness of the one-term fit is not claimed: it is convex but not strictly.
- No global optimum for K > 1: only descent, finite stopping of the hard alternation, a gap bound and local optimality under a margin condition. Convergence when the alternation does not stop, and stationarity at the stop, are not claimed. The certificate is per run, not across restarts.
- The noise result has no consistency claim.
- The converse of Theorem 9 is not claimed: a Pareto-efficient design need not maximize V.
- The stable radius is sufficient, not tight.
- The association maps (Figures 8 and 9) and the PCA on the chart are readings of the sampled designs, not of the model, and say what the sampling exercised.
- It does not do the conditioning; that is left to the analyst.
- Section 7 (the search of the design space) is labelled preliminary, and its monotonicity is an open question. Q1 to Q4 are open too, though I do not know what they are.
- As far as I can tell it gives no uncertainty or confidence intervals for the exponents. τ is chosen by a convention, not estimated.

## 6. Where I was confused or stopped, in order

1. **Figure 1, before the caption.** "term 1: dilemma of 2 and 3", and the open ring as "planted (the known answer)". I could not tell what "dilemma" meant technically or what had been planted. The caption cleared this up: a synthetic table with known terms, and the face of the simplex that holds the exponent names how many metrics are in play. I also had to work out why each term is a single point on the triangle.

2. **Figure 2.** A parts diagram with filled diamonds and open arrows, "«part def»", "«abstract»", and "swap" and "tune" tags. I read it as UML-like, but it was not clear to me why a modelling diagram belongs in a paper about a fitting method. I took it to define the input space (the configurations), but nothing here tells me how the designs were sampled from it.

3. **Figure 3.** "«MoP»", "«MoE»", "SlewVerification", "ConfigurationVerification", and the purple box "returns 7 of 8 metrics, computed with no slew: pointing error, total mass. From the measurement: control effort (passed on) and settling time (not returned)." I struggled to reconcile "7 of 8" with the list that follows: two computed, one passed on, one not returned. The caption says the analysis computes the other six. I could not work out how this diagram matters for the method, beyond showing where the 8 columns come from. "the baseline configuration does not satisfy it" was also unclear: does this matter for the fit?

4. **Figure 4, top left.** "the fraction of designs above V = 1 ... target 0.1". I expected τ to be estimated or cross-validated; instead it is chosen so that a tenth of the designs sit beyond the surface, "a convention". I could not tell why 0.1. The effective sample size of 23 at that τ (out of what looks like ~600 designs) suggests the fit rests on very few points; that is fine for a frontier, but I wondered how stable it is.

5. **Figure 4, bottom.** Control effort has nonzero exponent at low τ, then drops to white; the support at the fit temperature and at ∞ looks the same (5 metrics). I wanted to know whether "5-lemma" is then robust to τ above ~25, which the figure seems to say, but the text I have does not.

6. **Figure 5 caption.** "they reach the line and stop there, a few beyond it". In the figure the dark points mostly scatter well below the line. Only a handful near the line are dark, many dark points sit 1 to 3 log units below it, and some are above it. I expected the dark points to pile up along the line. I could not work out whether "near the median within 0.1" is supposed to make them lie *on* the line or only *not beyond* it. The slope looks like about −2, which matches 0.36/0.18, so the elasticity reading checked out.

7. **Figure 6, top panel.** The two straight streaks are explained (torque-limited slews). But many light points and some dark ones lie above the term 1 line in the upper-left, and I could not tell whether that is expected for a term-level slice.

8. **Figure 6, bottom panel.** The lower cloud (large wheel) sits ~2.5 log units below the line. I wondered why those designs are assigned to term 3 at all, if they are.

9. **Figure 7.** "each design's level log V, the energy differential". "Energy differential" and "level of a potential" are physics words for what looks to me like a signed log-distance to the surface; I could not see what the energy metaphor adds. The grey band is very thin. I worked out that 1/τ ≈ 0.026, which fits, but "the K = 1 fit's band as at every K" took a second read. "(44% of it)" I took to be the explained-variance share of PC1.

10. **Figure 8, term 1 header.** "Too few near-frontier designs for an association reading: 3 of ten". I read this as 3 designs where at least 10 are required. At first I read it as "3 out of 10 designs".

11. **Figure 8, term 3 outlines.** Power margin has w = 0.02, above the participation threshold of 0.001, yet as far as I can see its cell is not outlined. Meanwhile energy balance is outlined with w = 0.00. Definition 6 explains the second case (contends in the limit, no elasticity at the fit temperature). It does not explain the first: a metric with a nonzero elasticity at the fit temperature that is not in the contending set. Stock regime in Figure 9: same thing, energy balance w = 0.02 not outlined, power margin w = 0.18 outlined. Power margin and energy balance correlate at 0.99, so the fit seems to pick one of a nearly redundant pair. I suspect this is the non-uniqueness (convex, not strictly) showing up, but I am not sure.

12. **Figure 8 and Definition 6 together.** The contending set is defined by refitting on the cell "centred on the cell's mean log-metric". I could not work out why centring matters, given the shift invariance of Proposition 1, unless it is for numerical reasons.

13. **Main results, first bullet.** "it is not the Pareto boundary but the level from which every design's position and level, and each term's elasticities, are read". Dense; I only understood it after Definition 1.

14. **Main results.** "Numerical: the termination status a fit reaches, read from its record." I could not tell what this result says.

15. **Definition 3.** "the package's mean subtracts the constant (log K)/κ from every level". I could not tell why the package uses a mean while the formula uses a sum, nor whether it affects V = 1.

16. **Theorems 2 to 12.** Hypothesis labels (A1 to A8, R1, R2, F5, F10, F12, I5 to I16) are not defined in what I have. A1, A2 and A8 I could infer from context; R1, R2 and the F labels I could not. Theorem 2: "R1's relation at the fit temperature ... does not imply that the finite-τ minimizer is interior". I could not work out what R1 is.

17. **Theorem 11.** "K^N + 1 iterations". Fine as a finiteness bound; I read it as the k-means-style argument.

18. **Theorem 12.** "H = D − κM ... κM the designs' ambiguity between terms". I followed the structure, but what M is was not something I could reconstruct.

## 7. Terms I had to guess

- **Hyperbolic (in the title, "hyperbolic trade space"):** probably that level sets of ∏ m_j^{w_j} are hyperbola-like curves in metric space, which are straight lines in log space.
- **Conditioned (metric):** a per-column monotone, invertible transform (log-affine, per Theorem 7) that makes the value positive and larger-is-better.
- **Trade study / traded metric:** the comparison of candidate designs across competing objectives; the metrics being compared.
- **MoP / MoE:** some kind of "measure of performance" and "measure of effectiveness", engineering labels.
- **Regime (primary / stock):** two settings of the controller gains, giving two separate datasets.
- **Reach β:** the soft-max score of the data along w, i.e. the offset of the hyperplane.
- **Cell:** the rows assigned to a term, like a cluster.
- **Term share:** the fraction of near-frontier designs in a term's cell.
- **Participation threshold:** an exponent of at most 0.001 is treated as zero for the elasticity reading.
- **Contending set / n-lemma:** the nonzero-exponent support of the τ = ∞ fit on a cell; n is its size.
- **Mean slack F:** the average of the soft-max objective over cells, weighted by cell size.
- **Effective sample size:** 1/Σp_i² of the softmax weights, I assume.
- **Glass-box / Tall's worlds:** not met here.
- **GGP:** not met here.
- **Energy differential / potential:** log V, by analogy with physics.
- **Supporting envelope:** the hard-maximum (τ = ∞) hyperplane that touches the data and has none beyond it.

## 8. Questions I am left with

- How are the ~600 designs sampled from the configuration space, and how much do the exponents depend on that sampling? The paper itself calls the PCA and association readings sampling-dependent; is the fit not?
- What does transform return exactly, and does inverse_transform recover raw attributes or conditioned metrics?
- How stable are the exponents and the contending set under bootstrap resampling? Is there any interval?
- How is K chosen? Is there a criterion beyond inspection?
- With near-collinear metrics (power margin and energy balance at 0.99), which one wins and why? Is the n-lemma count then meaningful?
- Why log-mean-exp with a 10% exceedance convention, rather than a quantile-regression-style fit (a pinball loss on w·u)?
- What are Q1 to Q4?
- What does the "search of the design space" do: does the fitted V guide sampling of new configurations?
- How does it compare against the prior art in Table 1, whose body I don't have? I assume production-frontier or data-envelopment methods are in there.

## 9. Would I go on to read the whole paper?

Yes, selectively. The core idea is clean and fills a gap in my toolbox: an edge-hugging, scale-free, interpretable linear fit in log space, with a reversible transform and a k-means-like extension with stated guarantees. I would read Sections 3 to 6 and the appendix with the package interface and reproducibility. I would skim the case construction (Section 8), since the satellite modelling is outside my world and the two diagrams did not help me. Before trusting the case analysis, I'd want the answer to the support-versus-threshold puzzle in Figures 8 and 9, and a statement on stability.

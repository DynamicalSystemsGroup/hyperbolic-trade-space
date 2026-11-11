# P3-C

## 1. What this is about

The paper proposes a way to read a trade study from a table of evaluated designs, not from weights a panel picks. You start with rows of designs and columns of outcomes. You turn each outcome into a positive, larger-is-better metric through a per-column log-affine map. The method then fits a surface to the outer edge of the cloud in log space. That surface is a weighted geometric mean of the metrics (one term), or a soft or hard maximum of several such means (several terms, a posynomial). The fitted exponents show which metrics trade against each other on each piece of the surface and at what rate (elasticities). Every design gets a coordinate pair: where it sits along the surface, and how far inside or beyond it it lies in log terms (the "energy differential", log V). The authors pitch it as an analogue of PCA that explains tensions rather than variance. It is packaged as a scikit-learn transformer.

For my purposes, the important line is that the evaluation stage is a black box. The method takes the table my system model already exports, plus a conditioning rule, and nothing else. It does not ask to see inside the model. The paper says measured attributes of a fielded system "would enter the same table and the same fit".

## 2. The main results, as I understand them

- **What the table must look like.** I need N rows (designs) by d columns (attributes). After conditioning, every metric must be strictly positive and larger-is-better. Conditioning has to be log-affine per column: log m_j = alpha_j log(a_j + s_j) + b_j. A negative alpha flips a smaller-is-better attribute, the shift s_j moves the origin, and a scaler equalises the spread. Zeros are tolerated (masked in the fit) and negative values are rejected. Because the conditioning is invertible, the fitted surface can be written back in my original attribute units exactly (Theorem 7). A negative product w_j alpha_j marks a cost attribute.
- **The one-term fit is a convex problem.** It minimises a log-mean-exp soft maximum of the scores w·u over exponent vectors on the simplex. Every minimiser is global, though there may be more than one. At infinite temperature it becomes a linear program. The temperature tau is chosen so that a target fraction of designs (10 percent here) lies beyond the surface. The surface is therefore a soft support, not a hard envelope and not a regression line.
- **What the outputs mean.** The exponents are elasticities along a term: d log m_j / d log m_i = -w_i/w_j. A design's V tells you by what common factor it would have to improve to reach the surface. Raising one metric j alone by the factor V^(-1/w_j) also reaches it. The chart (position Z = Bu with B orthonormal and orthogonal to the ones vector, plus log V) is a reversible rewriting of the log-metrics.
- **Pareto link, one direction only.** A maximiser of V with all exponents positive is Pareto-efficient. The converse, that every efficient design is picked by some w, is not claimed.
- **Several terms.** The model is a log-sum-exp (or, at the default, a maximum) of several monomial terms. It stays compatible with geometric programming, so later optimisation over it stays convex. The fit is not convex in the terms. It alternates two steps: assign designs to the term that scores them highest, then refit. It carries three graded guarantees: descent (with finite stopping under unique minimisers and a tie rule), a computable "term gap" bounding suboptimality per term, and local optimality when the assignment margin is positive. A soft-weight fit has a second-order certificate instead. Each returned fit carries a status: certified, stationary and so on.
- **Case (cubesat: power, mass, attitude control; 706 feasible designs, 8 attributes).** Dominance stops discriminating: with 8 attributes, 659 of 706 designs are nondominated. At K = 1 the fit names a 5-lemma: total mass, energy balance, pointing error, depth of discharge and settling time, with exponents 0.14 to 0.36. At K = 3 the tension splits into three terms with different contending sets. Control effort and peak slew power each lead a term, which they did not do at K = 1. On term 2, the mass/energy-balance elasticity is about -1.7. Changing controller gains changes what trades: mass drops out of the stock regime's set and control effort enters. On 20 planted tables the fit recovers the three planted terms in 16. The failures are the tables with very few frontier designs on one term.
- **The case's certificate is narrow.** At K = 3 the stable radius is about 70 times smaller than the band, so which term the 11 seam designs fall to is not a finding.

## 3. What I would do next with it

1. I would export one existing table from our product-line model: feasible configurations only, with the eight to twelve outcome columns we already trade on. I would write the conditioning rule myself, deciding orientation and shift per column. This is the step I would spend the most time on, because the paper is explicit that the conditioning defines the question.
2. I would fit K = 1 first and compare the contending set with what our engineers already believe trades. Then I would try K = 2 and 3 and check whether the sets differ the way the cubesat ones did.
3. I would pull the fitted surface back into attribute units (Theorem 7) and set it beside our model's own constraint relations. Where a term's elasticity disagrees with a sensitivity our model computes, I would treat that as a question about our sampling or our model, not a verdict either way.
4. I would mix in the rows where test data replaces computation, flag them, and see whether they sit consistently with the computed rows in the chart. The paper allows this in principle but does not test it.
5. I would score a few named candidate configurations against the fit, as Section 9 does, before trusting anything about proposals.

## 4. What I would tell a colleague

"It's a frontier fit on your exported trade table. You give it a positive, larger-is-better version of each outcome column, made through a per-column log transform you choose and can invert. It gives back three things: which outcomes contend on the edge of your design cloud, the exchange rates between them, and a score per design for how far inside the edge it sits. You don't have to touch the system model; the method only sees the table. The convex one-term version is solid and quick to read. The multi-term version is a local search with honest local certificates. It's descriptive of the sample you drew, not causal, and your choice of transforms and of how many terms changes the answer. Think of it as a second reading of the table next to Pareto filtering, not a replacement for requirements or for the model."

## 5. What the method does not do, and what the paper does not claim

- It does not claim to recover the Pareto boundary. The fitted surface is a soft support of the sample, and when it recovers the true boundary is an open question (Q4). Only "a maximiser of V is efficient" is proved, not the converse.
- It cannot represent non-log-convex structure (dents, holes in the frontier) at any K.
- Exponents are not causal exchange rates. They describe how the sampled designs trade, and are not what changing a variable would produce.
- No statistical consistency under noise (Q2), no identifiability under biased finite samples (Q3), and no global convergence of the multi-term alternation (Q1). For designed samples such as grids, the exponents carry no sampling-error interpretation.
- It does not choose K. Mean slack always falls with K. K is the analyst's choice, like the number of PCA components.
- It does not do conditioning for you, and it says the result depends on it.
- It does not handle requirements inside the fit. Requirements are read afterwards. On this case, imposing them first changes the one-term set by at most one metric, but that is reported for this case only.
- The design-space search (Section 7) has no results, and the proposal check is three proposals (two distinct designs), explicitly not a rate. Those proposals all failed a requirement that was not in the proposer's chart.
- A certificate says the optimiser reached a local minimum. It does not say the surface describes designs outside the table or supports a decision.
- The cubesat hardware values are illustrative, not datasheet values.
- Discrete variables are treated as continuous within a category, and only as a finite comparison across categories.

## 6. Where I was confused or stopped, in order

1. Abstract: "A fitted posynomial reference surface models the data underlying the table, not the Pareto boundary". I could not tell on first read what "the data underlying the table" is, as opposed to the table. Is it the sampled designs, or the space they come from? Definition 1 later helped, but this sentence stayed unclear.
2. Abstract: "its energy differential: its level relative to the surface, by analogy with a potential, not a physical energy". As someone who builds physical models, the word "energy" made me expect a physical quantity. I had to keep translating it to "log V". The disclaimer is there, but the term kept pulling me the wrong way.
3. Section 1: "the nondominated set holds 126 on 4 attributes ... and 659 on 8, all of them". 659 is not 706. I could not work out what "all of them" refers to: all 8 attributes, or all designs? Is the point that it is nearly all?
4. Definition 3: "the package's mean subtracts the constant (log K)/kappa from every level". A software implementation detail appears inside a definition. I was unsure whether the levels I would get from the package match the formula, and whether "V = 1" means the same thing in both.
5. Definition 6: "the support (exponents above 10^-9) of the exact-maximum (tau = infinity) fit to the term's cell, centred on the cell's mean log-metric: the term refit f_k ...". Three thresholds now (10^-9 here, 10^-3 "participation", 10^-12 "numerically zero") and two temperatures feed the reading of one term. I had to reread to see that the set of names comes from tau = infinity and the numbers from the fit temperature.
6. Section 5, R1: "the balanced point, the support-weighted mean of the log-metrics U^T p ... lies in the relative interior of a facet of the supporting envelope with positive normal". I could not picture this, and could not tell how I would check it on my own table. It seems to be the condition that makes the exponents meaningful as trade-offs, so it matters to me.
7. Section 5, Conditioning: "rescaling one metric changes which term is tangent". That seemed to sit uneasily with Proposition 1 (a uniform shift leaves w unchanged). I worked out that per-column rescaling differs from a shift of all columns together. I am still unsure how much my choice of scaler, not just orientation, moves the answer. The case uses a standard scaler. Is that a recommendation or just what was done?
8. Section 6.2: "Refitting a term on its own rows alone, the plain one-term fit on its cell, is ill-posed ... the refit of record is f_k over all rows". I followed that f_k has an extra linear term, but not why the plain cell fit fails or what "ill-posed" means here.
9. Section 6.2 numerical paragraph: margin 0.00121, stable radius 0.0001209, band 0.0088, "median best-minus-second-best score of 0.237". Four numbers on different scales. I understood the conclusion (seam designs are not a finding) only from the sentence after.
10. Section 8: "the effective sample size is 23.1 designs ... the exponents at the fit temperature rest on about 25 of the 706 designs". 23.1 rounded is 23, not 25. Minor, but I stopped on it.
11. Figure 4: the caption's first lines are dense. Reading the plot itself was easier: control effort carries weight at low tau and vanishes at the fit temperature.
12. Section 9, Figure 6 top panel: the "two straight streaks are torque-limited slews". This was a useful explanation, but it made me wonder how far term 1's line is set by a modelling artefact of our kind of simulation (a saturation) rather than by a trade. The paper does not say.
13. Figure 8, term 3: the title says 5 metrics in the exact-maximum support. On the plot I could clearly see outlines on pointing error, total mass, energy balance (which shows w = 0.00) and peak slew power. I was not sure which fifth cell is outlined. Settling time has w = 0.05 and depth of discharge w = 0.02, and I could not tell whether either is outlined. An outlined metric at w = 0.00 alongside non-outlined ones above zero is explained in the caption, but it is still counter-intuitive.
14. Section 9, Two regimes: "energy balance and power margin, one in each regime's own part, are the strongest-associated pair". I could not parse "one in each regime's own part". I took it to mean one appears in the primary set and the other in the stock set.
15. Section 9, propose-predict-check: "within the regressor's own band 1/tau = 0.0935". This tau differs from the fit's (band 0.0262 or 0.0088). I could not tell which fit this band belongs to (the "four-metric chart"?) or why proposals were aimed at a four-metric frontier when the case trades eight.
16. Section 11: "supply configurations, attributes and a conditioning rule". The fit itself uses only metrics, so I was unsure whether configurations are needed for the fit or only for the proposal step.

## 7. Terms whose meaning I had to guess

- **Energy differential**: log V, the signed log distance in "levels" of a design from the fitted surface (negative inside, positive beyond).
- **n-lemma / contending set**: the metrics with nonzero exponent in a term, which are the ones that trade against each other there. n is how many.
- **Reach (beta)**: the offset of a term, roughly how far the data extend in that weighted direction under the soft maximum.
- **Term share**: the fraction of near-frontier designs that a term scores highest.
- **Cell**: the designs a given term scores highest.
- **Mean slack**: the average amount by which designs fall short of the surface. It is the fit's objective.
- **Band (1/tau)**: the tolerance in log V within which a design counts as near the surface.
- **Effective sample size**: how many designs actually shape the soft-max fit (inverse sum of squared weights).
- **Balanced point**: the softmax-weighted average design in log space at the exact-maximum fit, a sort of contact point of the surface with the data.
- **Supporting envelope**: the hard (tau = infinity) version of the surface, which no design exceeds.
- **Assignment margin / stable radius**: how far the fitted terms can move before any design's term label changes.
- **Term gap**: a per-term computable bound on how far that term's fit is from its optimum.
- **Participation threshold**: an exponent above 10^-3 counts as carrying an elasticity.
- **Sharp vs soft (kappa)**: whether terms meet at a hard maximum (kinks) or a smoothed one.
- **MoE / MoP**: measure of effectiveness and measure of performance, the usual systems-engineering sense.
- **Codes such as A8, F12, I16, G-9**: assumption, fallback, inherited result and gap labels listed in appendices I did not have. I guessed only their category from Section 6's key.

## 8. Questions I am left with

- If some rows are measured and others computed, with different noise levels, should they be weighted differently, or does A5 (Gaussian in log space) assume one noise level for all? Does mixing sources bias which designs set the surface?
- How do I handle a nominal-is-best attribute (a target with tolerance either side)? A per-column log-affine map cannot fold it, so must it be split or left out?
- How sensitive are the contending sets to how my model's sampler covered the design space? The paper says tensions never exercised cannot appear. Is there any diagnostic for under-sampled regions other than the effective sample size and the planted-table failures?
- How do I check R1 on my own table, and what does the package report when it fails?
- What does the package return as a fit's status in practice, and how often should I expect "stationary" rather than "certified" at K > 1?
- How would I choose K beyond judgment? Are the contending sets at K and K+1 nested in any useful way?
- Can the fitted posynomial be fed back into my system model as a constraint or objective? The GP-compatibility suggests yes, but the paper does not show it.
- For the stepped term 3, where a swap drives the metrics, what does an elasticity across categorical alternatives mean in practice?
- With 8 metrics and 706 rows, the exponents rest on about 23 designs. How many rows would I need for 15 to 20 metrics?

## 9. Would I read the appendices?

Yes, selectively. I would read C.4 (the case's conditioning rule), because conditioning is the step I own and the one the paper says shapes the answer. I would read D.11 (which digits hold under regeneration) and D.8 (what a termination record looks like), because that is what I would get back and need to judge. I would read E (the gaps ledger), to see the assumptions written out against the failures I care about: noise, mixed data sources, sample design. I would read F (reproducibility), to see how to run my own table. I would skip the proofs in B unless I hit a failure of R1 or R2 in practice. The main text already tells me what each result needs, and proofs are not where my questions are.

[Process note: figures 1 to 4 were opened after parts 2 and 3 had both been loaded, not at the exact point in part 2 where Figure 1 is called for; all were looked at before part 4 was read.]

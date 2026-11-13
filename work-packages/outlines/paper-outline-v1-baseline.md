# Note: outline of the paper, v1 baseline (2026-11-08; superseded by paper-outline-v2-search.md, kept as the baseline)

Drafted 2026-11-08 from the story settled with the supervisor (`work-packages/WP10-decisions.md`,
"The paper's story"), the notation note (`notation.md`), the structure of his IEEE papers
(motivation, prior work, notation, definitions, proofs, case construction, case analysis,
discussion, future work, works cited) and the SciPy 2026 proceedings article as the build
reference. Word budget about 5,000, cap 6,000. "Backing" names what exists in the repository
today; "WP9" marks what the solver package adds before the paper is written.

## Abstract and Figure 1

Key points: trade studies are decided from documents; a model-based method must be trusted the
way PCA is; this method explains tensions, not variance; the unit is the n-lemma; the cubesat
case at K = 1 and K = 3, with the finding in one sentence; everything executable alongside.
Figure 1 is the hero: the cubesat trade space with its fitted facets and the contending metrics
named (chosen in WP10 for the abstract-and-figure reader).
Backing: the report outputs of the WP7 notebook (cells 28, 30), the K = 3 record (WP9 D-6).

## 1. Introduction: the decision problem

Key points: a trade study must produce an answer and a defensible justification; today the study
is a document, grids and tables, with the judgement hidden in weights; computational alternatives
are bespoke and their benefits unproven, so documents stick; the bar for a model-based method is
scale, complexity and noise handled consistently and interpretably; PCA has that standing but
explains variance; a decision-maker needs what trades against what; an answer far from the
frontier is hard to justify; the analysis must rerun on new data; the contribution; the paper's
organization.
Backing: NASA SE Handbook §6.8 (decision matrix as default, report required); Baker and Whalen
(traceability and repeatability; three methods, two answers); SEBoK (trade study the most common
method); Smith, Son, Piattelli-Palmarini and Bahill 2007 (mental mistakes in weights); Parnell et
al. 2021 (state of published practice); Madni and Sievers 2018, Henderson and Salado 2021 (MBSE
motivation and unproven benefits); Ross and Hastings 2005, Ross et al. 2010, Stump et al. 2009,
Spero et al. 2014 (tradespace exploration at scale, grounded in decision analysis); Howard 1988,
Keeney and Raiffa 1993 (what decision analysis demands); Jolliffe and Cadima 2016 (PCA). All
verified 2026-11-08, entered in `docs/references.bib` by WP10 under the WP5 rule.

## 2. Prior work

Key points: production frontiers and distance functions (Cobb-Douglas, Shephard, Farrell;
deterministic and stochastic frontiers; DEA and super-efficiency) are the lineage of a one-sided
fit; log-ratio and compositional PCA are the kin of the chart; geometric programming and
generalized posynomials (Boyd et al. 2007; Hoburg et al. 2016; Magnani and Boyd 2009) are the
form; kernel PCA is the feature-engineering kin and hyperbolic PCA the disambiguation; Pareto
fronts and multiobjective optimization are what the method is not; what the combination is and
what no source claims.
Backing: `docs/literature.md` (every section, with Appendix A of dropped candidates and B of
inherited axioms), `docs/references.bib` (38 verified entries today), the "Lineage" section of
`docs/method.md`.

## 3. Preliminaries and notation

Key points: the reader is assumed at multivariate calculus, linear algebra and convex
optimization; the pipeline c → a → m with its contracts (sampling, evaluation, conditioning,
identification, analysis) and who owns each stage; conditioning as the analyst's job with
scikit-learn tools; Assumptions A1 to A6 as numbered blocks with their interpretive role and
failure mode; the notation table (symbol, name, interpretation, PCA analogue, name in code),
anchored on Boyd and Vandenberghe and the scikit-learn glossary.
Backing: `docs/method.md` ("The pipeline", "Conditions of the theory"), `derivation/axioms.py`
(the ledger), `docs/preconditioning.md`, `notation.md`, `docs/superpowers/notes/sklearn-conformance.md`.

## 4. Definitions

Key points, each a numbered definition block: the monomial and the invariant value V; the
normalization that places V = 1 at the frontier (invariant form); the posynomial V_K and its
log Φ_K; the fit temperature τ and the band; the term temperature κ; the chart (Z, log V);
the contending set and the n-lemma; the reach β_k and the lead coefficient; the facet share; the
exchange rate; the tangent space and the ascent direction of a facet.
Backing: `docs/method.md` ("The model", "The fit", "Interpretation", "The posynomial and GGP
extension"), `notation.md`; estimator attributes in `src/hyperbolic_trade_space/estimator.py`
(`exponents_`, `log_offset_`, `basis_`, `support_weights_`, WP9: `coefficients_`, `facet_share_`,
`facet_`).

## 5. Results: the fit and what it proves

Key points: first, the intuition the method started from, as a lemma: a V-maximizer is Pareto-efficient (L11, WP9), with the non-converse stated (only the log-convex part of a front is reached by some w; Miettinen, Ehrgott); the one-sided fit as a convex program on the simplex, the log-mean-exp as the
entropic soft maximum and why not the unnormalized log-sum-exp (L5); homogeneity and the
invariant form (L1); shift equivariance (L2); gradient, support weights and the balanced KKT
condition (L3); convexity and identifiability (L4); Gaussian noise (L6); elasticities, exchange
rates and improvement factors (L7); the Helmert chart and its inverse (L8); the pull-back to
attribute units (L9); the K-term form, its K = 1 reduction and its κ → ∞ limit (L10). Then the
K > 1 algorithm in "given / repeat / until" form, what it inherits (Magnani and Boyd: convergence
to a local optimum; I5 in the ledger) and what is only observed; the sparsity option (reweighted
ℓ1 on the simplex, Candès, Wakin and Boyd 2008). Each lemma block has one interpretive paragraph
and a proof dropdown that runs the SymPy script.
Backing: `derivation/lemma_01` to `lemma_10` (`STATEMENT`, `derive`, `verify`, `AXIOMS_USED`),
`derivation/run.py` (the chain and the audit), `tests/test_derivation.py`,
`tests/test_matches_derivation.py` (code equals the lemmas at numeric instances),
`src/hyperbolic_trade_space/solvers.py` (`solve_lp`, `solve_slsqp`, `log_mean_exp`,
`support_weights`), `tuning.select_temperature`; WP9: `solve_terms`, the sparsity penalty, the
method page's algorithm statement, the I5 ledger entry.

## 6. Case construction

Key points: the cubesat attitude-control design space (wheel class, tracker grade, panel span,
battery, two gains) and its SysML v2 model; one thousand designs simulated once, two regimes
(aggressive gains primary, stock gains baseline); ten attributes; feasibility (settled, momentum,
depth of discharge); conditioning to metrics (orientation, shift, unit log-spread, invertible);
the temperature chosen for a tenth of designs above V = 1; a planted multi-facet frontier as the
controlled example where the answer is known. One figure of the raw table.
Backing: `examples/adcs/` (`cubesat_model.py`, `design_space.py`, `adcs_sim.py`,
`generate_dataset.py`, `cubesat_tradespace.sysml`, `extended_design_space.sysml`), the cached
CSVs in `examples/adcs/data/`, `tests/test_adcs_case.py`, `tests/test_adcs_enrichment.py`,
`tests/test_cubesat_model.py`, the WP4 and WP4b records; conditioning cells of the WP7 notebook
(sections 2 to 4) to become module functions (WP10 D-3); WP9 D-5 (planted K-facet data).

## 7. Case analysis

Key points, K = 1 first: the frontier in figures (surfaces, log planes, the chart with holes);
the tension report, a 6-lemma among ten attributes, the aligned pairs, the principal tension
directions, the closure caution; persistence under reconditioning (mass, an agility metric and
pointing error contend in every variant; the detail moves). Then K = 3: the three facets, their
contending sets and n-lemmas, their reach and share, where they meet in the chart; what K = 3 adds
to the K = 1 reading. Then the regime comparison: the same design problem with a different
shape under stock gains, mass leaving the contending set. Then candidate configurations: where
each sits (log V), what it trades (its facet), what one metric alone would have to do.
Figures carry the argument; every figure is numbered with a self-contained caption.
Backing: the WP7 notebook's report cells and figures 02 to 09 (`examples/adcs/figures/`), its
sensitivity table (section 8), per-category refits (section 10), candidates (section 11), regime
comparison (section 14); the plotting module's one-call figures; `tests/test_notebook.py` guards
(numbers, step-0 gate, nothing named before the report, wheel-class statement); WP9 D-6 (the K = 3
record and figures `k3_*.png`) and the facet-aware tension report.

## 8. Discussion

Key points: the author's interpretation, marked as human validation, of why the report looks the
way it does (gains, wheel class, tracker grade, panel span); what the decision-maker now has:
what trades against what, where a chosen configuration sits, which facet it lives on, how to
defend it; what the method cannot say (one facet per term, closure, small near-frontier samples,
stratified hardware, illustrative values, conditioning is a choice); verification by machine
versus validation by human, with the list of each; the tangent space and the ascent direction as
guidance for moving up the levels and for scoping the next experiments, with the chain back to
configurations stated and its estimation named as future work; rerunning on empirical data for
configuration management.
Backing: WP7 notebook sections 9, 15 and 16 (interpretation, limits, V&V); `docs/limitations.md`
("Limits of the method", "What the contrast with PCA does and does not claim"); L3, L7, L9 for the
tangent-space statements; `TradeSpaceRegressor` as the supervised map today; the ledger's failure
modes.

## 9. Reproducibility and your own case

Key points: the exact commands (`uv sync`, `uv run pytest`, `uv run python derivation/run.py`,
the notebook execution command, `myst start`) and what each produces; CI runs the same; the case
module separates the cubesat specifics from the generic steps, so another table runs through the
same functions; the five-line recipe for your own data and where to read about conditioning and
the API.
Backing: `pyproject.toml`, `uv.lock`, `.github/workflows/test.yml`, `CLAUDE.md`'s tooling rules,
`docs/api.md`, `docs/preconditioning.md`, WP10 D-3 (the case module) and its test on a second
table, the drill-down levels L-E and L-F (`WP10-decisions.md`).

## 10. Future work and a final remark

Key points: scalability and performance of the K > 1 solver; selection of K; kernel expansions
that remain generalized posynomials; estimating the configuration Jacobian for the ascent
direction; richer cases. Final remark, the hook: for new capabilities or technologies entering
the design space, a novelty or impact score from how far above V = 1 they are forecast to sit.
Backing: `docs/method.md` ("Research direction: kernel methods"), `docs/limitations.md`
("Extensions"), the WP9 non-goals, the supervisor's words on the final remark
(`WP10-decisions.md`).

## References

Backing: `docs/references.bib` (38 entries today, 15 to be added for section 1), each with a
resolved DOI or stable URL and a `verified` field; `tests/test_references.py`.

## Supporting material (`supporting_material.ipynb`), as lettered appendices the paper cites

A. Notation reference (the full table). B. The derivation ledger and each lemma's SymPy output.
C. The full case detail the paper summarizes: sensitivity variants, per-category refits, the
propose-predict-check with its mixed result, regime tables, the K = 1/2/3 diagnostic table.
D. Verification audit: tests by area, lemma PASS list, the scikit-learn checks and their one
documented expected failure, cross-checks. E. What remains for a human.
Backing: the WP7 notebook (retired as an artifact, mined for cells), `tests/`, `derivation/run.py`
audit, WP8's planned generated pages.

## Reading paths (the drill-down levels)

L-A abstract and Figure 1; L-B headers, the main-results list at the end of section 1, numbered
blocks and figure captions; L-C the whole paper; L-D the appendices; L-E section 9 and the repo;
L-F section 9's recipe, the case module and `docs/api.md`. Each checked by a cold-reader trial in
WP10 and by the supervisor's verdicts in WP11.

## Addendum (2026-11-08): the contrast with Pareto methods, for section 2 and section 8

Pareto dominance filters a table into a set; this method fits the table to a surface with
coordinates. Points to make, in order: (1) object: a nondominated set versus a parametric frontier
and a chart; (2) question: which designs survive versus what trade-offs explain the edge; (3) scale
with d: under dominance almost everything is nondominated once d is large, so the filter stops
discriminating, while the fit still returns d − 1 exponents per facet; (4) noise: dominance is a
hard comparison, one noisy design dominates many, while the fit is a soft maximum with a band and
an effective sample size; (5) what each returns: membership (and set indicators such as hypervolume
and spread) versus exchange rates, contending sets, distance from the frontier for every design
including interior ones, position along it, holes, pull-back to attribute units; (6) the
relation: with positive exponents a V-maximizer is Pareto-efficient; a single monomial touches the
log-convex part of the front (weighted-sum scalarization in log space); K facets approximate the
log-convex envelope of the front from outside; non-log-convex dents are the residual and show up
as holes; (7) multiobjective evolutionary methods (NSGA-II) generate designs, this identifies a
model from a given table and can guide generation through the ascent direction; (8) DEA is the
closer cousin (a piecewise-linear envelope fitted from data with an efficiency score per unit);
the K-facet envelope in log space is its log-linear relative, with a temperature and a chart.

Numbers from the cubesat primary dataset (706 feasible designs, orientations as in the notebook),
computed 2026-11-08 by the driver, to be reproduced by the case module in WP10:

| Columns | Nondominated designs | Share |
|---|---|---|
| ten attributes | 671 of 706 | 95.0 % |
| four-metric subset (slew time, pointing error, control effort, total mass) | 146 of 706 | 20.7 % |
| settling time and slew time only | 8 of 706 | 1.1 % |

The same table's K = 1 fit has 51 near-frontier designs at the chosen temperature in the ten-metric
fit and 71 in the four-metric view, with six and four contending metrics respectively.

## Addendum (2026-11-08): DEA, and the prior-art review as a requirement

Supervisor: "we also need to compare to DEA"; "prior art is an important part of lit review".

**DEA versus this method.** Shared: both envelop the data from one side; both score every unit by
its distance to the envelope (DEA's efficiency score, our log V); super-efficiency allows scores
beyond the frontier (our V > 1); the Malmquist index tracks a frontier that moves between data
sets (our rerun for configuration management); the convex hull is the limit object of our K-facet
envelope. Differs: (a) weights: DEA's multiplier form lets each unit choose the weights most
favourable to itself, so there is no single trade-off structure to report and each efficient unit
is justified by its own weights (the standing objection, answered in DEA by weight restrictions);
this method fits one exponent vector per facet with K small, a global named structure, and makes
sparsity a controlled metaparameter rather than an LP accident; (b) geometry: DEA's frontier is
piecewise linear in levels (convex combinations of observed units with free disposability), ours
piecewise log-linear, so exchange rates are constant elasticities within a facet; (c) inputs and
outputs and a returns-to-scale choice (CCR constant, BCC variable) versus larger-is-better metrics
after conditioning, with homogeneity by the simplex; (d) noise: DEA is deterministic and its
frontier is set by extreme units; ours is a soft maximum with a temperature, a band and an
effective sample size; (e) computation: N linear programs, one per unit, versus one convex program
and K refits; (f) coordinates: DEA returns a score and a peer set; this returns (Z, log V), holes,
the pull-back to attribute units and the facet; (g) for the decision-maker: DEA says "this unit is
efficient under some weights", this says "on this facet these metrics trade at these rates".
Citations: `charnes1978measuring`, `andersen1993procedure`, `fare1994productivity`,
`farrell1957measurement` (in the bibliography); Banker, Charnes and Cooper 1984; Allen et al.
1997; Dyson et al. 2001 (verified, to enter).

**Prior-art review, by family (section 2 of the paper; a requirement of WP10).** For each: what it
produces, what it shares, how this differs, citations. Nothing is claimed as novel; the
combination is described and the sources' limits stated (`docs/literature.md`, "What is the
supervisor's combination, and what the sources do not say").

| Family | Produces | Shares | Differs | Cites (bib keys; "+" to enter) |
|---|---|---|---|---|
| Pareto dominance and multiobjective optimization | a nondominated set; set indicators; generated designs | the front is where the frontier sits | fitted surface and coordinates versus a set; scales with d; soft versus hard; identification versus generation; log-convex envelope and holes | zitzler1999multiobjective, deb2002fast, +Miettinen 1998, +Ehrgott 2005 |
| Data envelopment analysis | per-unit efficiency, peers, super-efficiency, Malmquist | envelopment, distance scores, scores beyond one, frontier shift | one structure per facet versus per-unit weights; log-linear versus linear; soft; one program; chart | charnes1978measuring, andersen1993procedure, fare1994productivity, +Banker 1984, +Allen 1997, +Dyson 2001 |
| Production functions and distance functions | Cobb-Douglas form; Shephard distance | the weighted geometric mean with exponents summing to one; V as a distance | attributes in place of inputs; fitted one-sided to a frontier, not by regression | cobb1928theory, shephard1970theory, fare1995multi, farrell1957measurement |
| Deterministic and stochastic frontiers, COLS | a frontier by programming or by regression with one-sided error | one-sided criterion | soft maximum over a simplex-constrained geometric mean; no error distribution assumed | aigner1968estimating, afriat1972efficiency, aigner1977formulation, richmond1974estimating, greene1980maximum, battese1992frontier |
| PCA, sparse PCA | directions of variance; loadings | a learned coordinate chart with components | tensions not variance; one-sided; components on the simplex; sparsity as a metaparameter | jolliffe2016pca (+), pedregosa2011scikit |
| Log-ratio and compositional PCA | PCA on log-ratios; isometric log-ratio coordinates | the Helmert chart; scale invariance | the criterion (support function, not variance) | aitchison1983principal, aitchison1986statistical, egozcue2003isometric |
| Geometric programming, posynomial and max-affine fitting | GP-compatible fitted functions | the form Φ_K, softmax-affine; the partition-and-refit algorithm | fitting a frontier of a data cloud, not a function of inputs; the invariant form; the chart | boyd2007tutorial, hoburg2016data, hoburg2014geometric, magnani2009convex |
| Kernel PCA; hyperbolic PCA (disambiguation) | feature-space PCA; PCA in negative curvature | the kernel view of the terms as trade-offs; the name | GP-admissible kernels only; "hyperbolic" means the level surfaces, not the geometry | schoelkopf1998nonlinear, chami2021horopca |
| Entropic risk and the soft maximum | log-mean-exp as entropic value | β as the entropic soft maximum | one direction of the support function | ahmadijavid2012entropic, foellmer2026entropic, rockafellar1970convex |
| Tradespace exploration | many designs evaluated, utilities, visual steering | the setting and the scale | a fitted frontier and tensions, not utility aggregation | ross2004multi, +Ross 2005, +Ross 2010, +Stump 2009, +Spero 2014 |
| Decision analysis and MCDA (decision matrices, AHP, Pugh) | a ranked choice from weights and scores | the decision the output must support | weights are found from the data's edge, not elicited; reproducible | +NASA SE Handbook, +Baker and Whalen, +Smith 2007, +Parnell 2021, +Howard 1988, +Keeney and Raiffa 1993 |
| MBSE and digital engineering | models in place of documents | the move away from documents | a method whose trust rests on its own reproducibility and tests | +Madni and Sievers 2018, +Henderson and Salado 2021 |

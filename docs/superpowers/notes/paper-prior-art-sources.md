# Note: sources for the paper's prior-art section (WP10)

Source material for the author of the prior-art section and of the Pareto and DEA paragraphs. It
restates what the verified sources say, at the depth recorded in each `verified` field of
`docs/references.bib` and in `references-verified.md` ("Added for WP10"). Where a source was read
by abstract or title only, the row says so and claims nothing more. Nothing here is a claim of
novelty. Citations are keys, in the pandoc form. The table columns are the ones the supervisor
required (`WP10-decisions.md`, "DEA and prior art"): what the family produces, what it shares with
this method, how this method differs, and the keys. The "differs" cells are the project's own
statements (spec, outline addenda), not statements of the sources.

Terminology follows the register (`notation.md`): fitted reference surface, supporting envelope,
Pareto boundary, energy differential, level offset.

## 1. Families

| Family | Produces | Shares with this method | Differs | Cites |
|---|---|---|---|---|
| Pareto and multiobjective optimization | a nondominated set; scalarizations (weighted sums) that trace its supported part | a maximizer of a weighted geometric mean with positive exponents is Pareto-efficient (lemma L11); the weights act as a trade-off | returns no coordinate system and no exponents; see section 2 | [@miettinen1999nonlinear; @ehrgott2005multicriteria; @zitzler1999multiobjective; @deb2002fast] |
| Data envelopment analysis (DEA) | a relative efficiency score per decision-making unit from linear programs; scale and returns-to-scale variants; super-efficiency scores above one; Malmquist productivity indices | one-sided envelope of the data; a score per unit; scores beyond the boundary (V above 1); a boundary that moves between data sets | see section 3 | [@charnes1978measuring; @banker1984some; @andersen1993procedure; @fare1994productivity; @allen1997weights; @dyson2001pitfalls] |
| Production and distance functions | the Cobb-Douglas form; the Shephard distance function and its duality | the weighted geometric mean with exponents summing to one is the constant-returns Cobb-Douglas form; V read as a scaling factor to the boundary is a distance-function reading | attributes in place of inputs; the form is fitted from a table with a soft maximum | [@cobb1928theory; @shephard1970theory; @fare1995multi; @farrell1957measurement] |
| Deterministic and stochastic frontiers | frontier production functions estimated by programming, corrected OLS or maximum likelihood; stochastic frontiers with one-sided error | a one-sided criterion on log-linear residuals | smooth soft maximum over a simplex-constrained geometric mean in place of a shifted intercept; K facets | [@aigner1968estimating; @afriat1972efficiency; @richmond1974estimating; @greene1980maximum; @aigner1977formulation; @battese1992frontier] |
| PCA | uncorrelated components that successively maximize variance (the review's abstract) | "what explains this table": an unsupervised summary by a few directions | the criterion is a one-sided soft maximum, not variance; exponents live on the simplex | [@jolliffe2016principal] |
| Compositional and log-ratio PCA | PCA of compositional data; isometric logratio transformations | the chart Z = Bu is in the spirit of an isometric logratio chart | one-sided criterion; simplex weights | [@aitchison1983principal; @aitchison1986statistical; @egozcue2003isometric] |
| Geometric programming and max-affine fitting | GP tutorial with generalized posynomials; softmax-affine fits compatible with GP; convex piecewise-linear fits | the model class; the K > 1 refit scheme; the sparsity option | the sources fit regression surfaces, this method fits an envelope | [@boyd2007tutorial; @hoburg2014geometric; @hoburg2016data; @magnani2009convex; @candes2008enhancing] |
| Kernel and hyperbolic PCA | PCA in an implicit feature space; PCA in hyperbolic space with horospherical projections | kernel PCA is the feature-engineering kin of the GP-compatible kernel direction | "hyperbolic" here means level surfaces of V in metric space, unrelated to negative-curvature geometry | [@schoelkopf1998nonlinear; @chami2021horopca] |
| Entropic risk | the entropic risk measure and its limits (mean, essential supremum); entropic value-at-risk | the log-mean-exp soft maximum is the sample version of the entropic risk functional | none used from the risk-measure side; cited to avoid confusion | [@foellmer2026entropic; @ahmadijavid2012entropic] |
| Tradespace exploration | value-focused broad exploration of design alternatives (Ross and Hastings); a process framing of the exploration (Ross et al. 2010, title only); user-guided samplers and linked visualization with Pareto frontier display (Stump et al.); tradespace exploration for resilient systems (Spero et al., title only) | the setting: a table of evaluated designs | these explore and display; this method fits and reports a coordinate system and a score | [@ross2004multi; @ross2005tradespace; @ross2010revisiting; @stump2009visual; @spero2014tradespace] |
| Decision analysis and multiple-criteria methods | decision analysis with a normative versus descriptive distinction (Howard); multiple-objective preferences and value trade-offs (Keeney and Raiffa, title and record only); weighted-criteria comparison methods Pugh, AHP and Kepner-Tregoe (Baker and Whalen) | the weights are trade-off rates | the weights here are fitted from the data's edge, not elicited | [@howard1988decision; @keeney1993decisions; @baker2012survey; @parnell2016trade] |
| Model-based systems engineering | MBSE centred on the system model as the sole source of truth (Madni and Sievers); a review of the evidence for MBSE benefits, opening from document-based practice (Henderson and Salado) | the trade space as a model rather than a document | the method is a model-based trade analysis, not an MBSE methodology | [@madni2018model; @henderson2021value] |

The family-level statements that no source supports (the combination, priority, the value of the
difference) are listed in `docs/literature.md` ("What is the supervisor's combination"); the
paper keeps that list, in its own register.

## 2. The Pareto paragraph

What the sources and the project records support, in the order the paragraph needs.

- The Pareto methods the bibliography carries: the nondominated set and weighted-sum scalarization
  in the textbooks [@miettinen1999nonlinear; @ehrgott2005multicriteria] (records only; the
  non-converse for non-convex fronts is the textbooks' standard statement as recorded in
  `docs/literature.md`); evolutionary generation of nondominated sets [@deb2002fast] (read, with its
  spread metric) and the strength-Pareto comparison of evolutionary algorithms
  [@zitzler1999multiobjective] (record only).
- The contrast, from `paper-outline-v1-baseline.md` (addendum) and `WP10-decisions.md`, to be compressed
  to one paragraph: a nondominated set against a fitted reference surface with coordinates; "which
  designs survive" against "what trade-offs explain the edge"; dominance stops discriminating as d
  grows, while the fit returns d - 1 exponents per facet and a band of near-boundary designs;
  dominance is a hard comparison, the fit a soft maximum with a band and an effective sample size;
  generation (NSGA-II) against identification from a table; the relation (a V-maximizer with
  positive exponents is Pareto-efficient, one monomial touches the log-convex part of the Pareto
  boundary, K facets the log-convex envelope, dents are the residual and show as holes).
- Counts: 671 of 706 feasible designs nondominated on ten attributes, 146 on the four-metric
  subset, 8 on two. These are the driver's 2026-11-08 numbers; the paper quotes them from the case
  module's output (WP10 D-3), not from this note.

## 3. The DEA paragraph

- What the records say. Banker, Charnes and Cooper [@banker1984some]: the abstract says DEA uses
  mathematical programming for ex post evaluation of relative efficiency, that the CCR ratio form
  comprehends technical and scale inefficiencies, and the title names models for estimating technical and scale
  inefficiencies. Charnes,
  Cooper and Rhodes [@charnes1978measuring] introduced DEA as a linear-programming measure of
  relative efficiency. Andersen and Petersen [@andersen1993procedure]: ranking efficient units with
  scores above one. Fare et al. [@fare1994productivity]: Malmquist indices. Allen et al.
  [@allen1997weights] and Dyson et al. [@dyson2001pitfalls]: read by title only (weights
  restrictions and value judgements; pitfalls and protocols); the paragraph cites them for the
  topics in their titles and says no more.
- The points of comparison, from `paper-outline-v1-baseline.md` (addendum), restated as project
  statements. Shared: one-sided envelope; a score per unit (DEA's efficiency score, here the energy
  differential log V); super-efficiency and V above 1; Malmquist and the rerun for a moving
  boundary; the convex hull as the limit of the K-facet supporting envelope. Differs: (a) weights
  (DEA's multiplier form lets each unit choose favourable weights, answered in DEA by weights
  restrictions [@allen1997weights]; here one exponent vector per facet, a global named structure);
  (b) geometry (piecewise linear in levels against piecewise log-linear, constant elasticities
  within a facet); (c) inputs, outputs and a returns-to-scale choice against larger-is-better
  metrics with homogeneity by the simplex; (d) noise (a deterministic boundary set by extreme units
  against a soft maximum with a temperature, a band and an effective sample size); (e) computation
  (N linear programs against one convex program and K refits); (f) coordinates (a score and a peer
  set against (Z, log V), holes, the pull-back to attribute units and the facet); (g) the
  decision-maker's reading ("efficient under some weights" against "on this facet these metrics
  trade at these rates").

## 4. The state-of-practice sources (the "why")

What each is cited for, as far as the record read supports. The paper cites the subset its text
needs; all stay in the bibliography (supervisor: "keep all of them in our bibtex records").

| Key | What the record read says | Used for |
|---|---|---|
| `hirshorn2017nasa` [@hirshorn2017nasa] | NASA/SP-2016-6105 Rev 2: best practices and alternative approaches in six chapters (abstract); section 6.8 not read | trade studies in the agency's systems engineering practice (page and section to be confirmed by the author before the paper cites a claim) |
| `baker2012survey` [@baker2012survey] | defines trade studies as decision-making activities for the most acceptable technical solution; compares Pugh, AHP and Kepner-Tregoe on time, data and accuracy (page one read) | trade studies as a documented, repeatable decision activity; criteria weighed by elicited methods |
| `chilli2026decision` [@chilli2026decision] | SEBoK: structured analytical methods such as trade studies to weigh objectives and uncertainties; cognitive biases distort decisions | the practice and its known weakness |
| `smith2007ameliorating` [@smith2007ameliorating] | abstract: tradeoff studies are mandated, involve human numerical judgment, and are susceptible to human biases and errors | human judgment in trade studies |
| `parnell2021system` [@parnell2021system] | abstract: structured literature survey of trade-off analytics answering 14 research questions; trade-off analysis appears in almost every engineering domain | the published state of practice |
| `parnell2016trade` [@parnell2016trade] | publisher page: a decision management process based on decision theory and cost analysis | the reference text for trade-off analytics |
| `madni2018model` [@madni2018model] | abstract: MBSE centred on the system model as the sole source of truth | the model-based turn |
| `henderson2021value` [@henderson2021value] | abstract: practice is moving from document-based to model-based; the evidence for MBSE benefits is assessed by systematic review | documents as the incumbent medium |
| `ross2005tradespace`, `ross2010revisiting`, `stump2009visual`, `spero2014tradespace` | see the tradespace row of section 1 | tradespace exploration |
| `howard1988decision`, `keeney1993decisions` | decision analysis; multiple objectives (record only for the second) | what a decision-maker needs |
| `jolliffe2016principal` [@jolliffe2016principal] | abstract: PCA reduces dimensionality, increasing interpretability while minimizing information loss | PCA's standing as the interpretable summary |
| `zargham2026incose` [@zargham2026incose] | the supervisor's INCOSE IS 2026 paper (36(1), 1501-1514): typed simplicial complexes formalize document quality assurance with mandatory human accountability | the companion argument on documents and accountability; self-citation |

Not found (WP10-decisions, 2026-11-08): an empirical study of trade studies delivered as documents or
spreadsheets. The paper's sentence on documents rests on [@henderson2021value] (document-based
practice in transition) and [@baker2012survey], not on such a study.

## 5. A source of the derivation ledger

`nocedal2006numerical` [@nocedal2006numerical] is cited by the ledger entry I10 of the derivations
(first-order necessary conditions on the simplex, whose affine constraints satisfy the linear
independence constraint qualification; Theorem 12.1 and Definition 12.4). Its row in the preserved
snapshot `paper-sources/literature.md` is not in the snapshot (it was added to the snapshot after
it was taken, and has been removed again); this note carries the citation so that the bibliography
has no uncited key.

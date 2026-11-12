# WP35 stage 1 readout: the word "hyperbolic", HoroPCA run on the paper's tables, and Table 1's "differs" column

Spike head: see the commit that adds this file. Code, scripts and results: `docs/superpowers/notes/spike-horopca/`. Written for the assistant; the options at the end are the supervisor's, through the assistant.

## 1. The reading

### 1a. Every prose occurrence of "hyperbolic" (identifiers excluded)

Found by `docs/superpowers/notes/spike-horopca/grep_table.py` over the paper notebook, the supporting material,
`docs/`, `glossary.yaml`, `README.md`, `claims_register.toml`, `paper/prior_art.yaml`, `paper/reading_pass.yaml`,
`paper/myst.yml`, `mkdocs.yml`, and a plain grep of `src/` (the package name `hyperbolic_trade_space`,
`HyperbolicTradeSpace` and the repository URL are identifiers and are not counted).

| # | File and place | The sentence | Reads as |
|---|---|---|---|
| 1 | `paper/paper.ipynb` cell 0 (title); `paper/myst.yml` `title` | "Scaling Decision Analysis with Hyperbolic Trade Space Identification" | the name |
| 2 | `paper.ipynb` cell 13 (Section 2, `sec-prior-art-3`, closing the DEA paragraph) | 'The title's "hyperbolic" is the level curve of $V$ (Section Definitions), not the hyperbolic graph measure of efficiency of Färe, Grosskopf and Lovell, a measure on the graph of a technology with inputs and outputs both free [@fare1985measurement].' | caveat 1 (against Färe et al.) |
| 3 | `paper.ipynb` cell 13 (Section 2, Lineage paragraph) | 'Kernel PCA is the feature-engineering kin of the direction in Section Discussion [@schoelkopf1998nonlinear], and "hyperbolic" here is unrelated to hyperbolic PCA [@chami2021horopca].' | caveat 2 (against HoroPCA): the only sentence in the body that names HoroPCA, and it names it to disclaim a relation |
| 4 | `paper.ipynb` cell 15 (Definitions, first paragraph) | "In two metrics its level curves are $m_1^{w_1}m_2^{w_2}=\text{const}$, the rectangular hyperbola $m_1m_2=\text{const}$ when $w_1=w_2$: the title's word." | the one place the word is defined (positively) |
| 5 | `paper/prior_art.yaml` `hyperbolic-graph-measure` (renders in Appendix G) | row family "The hyperbolic graph measure of efficiency"; `differs`: "The title's word names the level curves of V, products of powers of larger-is-better metrics fitted to a table under a soft maximum, not this measure; nothing here scales inputs against outputs." | caveat 1, repeated |
| 6 | `prior_art.yaml` `kernel-hyperbolic-pca` (renders in Table 1 and Appendix G) | family "Kernel and hyperbolic PCA"; `does`: "PCA in an implicit feature space, and PCA in hyperbolic space with horospherical projections."; `differs`: '"Hyperbolic" here means the level surfaces of V in metric space, unrelated to negative-curvature geometry.' | caveat 2, repeated; the row that merges kernel PCA and HoroPCA |
| 7 | `paper/reading_pass.yaml` n=44 (three entries: sentence, table, why) | sentence '"hyperbolic" here is unrelated to hyperbolic PCA'; why: "Abstract: HoroPCA, PCA components generalized to hyperbolic space." | record of the audit of caveat 2 |
| 8 | `docs/user-guide/limitations.md` ("Name.") | '"Hyperbolic" describes the shape of the score, which tends to zero as any participating metric does. It is unrelated to PCA in hyperbolic space [@chami2021horopca].' | caveat 2, third copy, with a second (and different) definition: "the shape of the score which tends to zero" rather than the level curve |
| 9 | `docs/further-reading.md` | "HoroPCA [@chami2021horopca]: principal component analysis in hyperbolic space, which this package is not." | the docs' one-line acknowledgement |
| 10 | `claims_register.toml` (five rows) | fragments "\"hyperbolic\" here is unrelated to hyperbolic PCA", "HoroPCA [@chami2021horopca]: principal component analysis in hyperbolic space, which this package", "It is unrelated to PCA in hyperbolic space [@chami2021horopca].", the rectangular-hyperbola sentence, and the Färe et al. sentence | backing rows for rows 2, 3, 4, 8, 9 |

No occurrence in: `README.md`, `docs/index.md`, `docs/theory.md`, `docs/getting-started.md`, `docs/examples.md`,
the supporting material's own source cells (Appendix A prints the glossary, which has no entry; Appendix G prints
rows 5 and 6 from `prior_art.yaml`; Appendix G.1 and G.2 print the reading-pass entries), `glossary.yaml`, `src/`.

What the table says: the word has one positive definition (row 4, a rectangular hyperbola in two metrics, the
level curve of V) and **two different** informal ones in the docs (row 8, "the shape of the score"). It is
disclaimed in five places against two different referents (the Färe et al. measure, rows 2 and 5; negative-curvature
geometry, rows 3, 6, 8), and nowhere in the body does the reader meet HoroPCA except inside a disclaimer. The title
is the only occurrence a reader meets first, and the first caveat sits in Section 2, far from it.

### 1b. Table 1, row by row: whose method does "differs" describe?

Table 1 (Section 2) prints the `short` cells of the `section2` rows; Appendix G prints the full `differs`. A cell
is **ours** when this work (the method, the fit, the model, "we") is the grammatical or evident subject, **theirs**
when the family is, **mixed** when it opens with the family and turns to this work, **neither** when it is about
the word or the citation and not a difference between methods.

| Row | `short.differs` (Table 1) | Full `differs` (Appendix G) | Subject |
|---|---|---|---|
| Pareto and multiobjective optimization | "Returns no coordinate system and no exponents" | "Returns no coordinate system and no exponents: a nondominated set says which designs survive, the fit says what trades against what, ..." | **theirs** in both (the subject of "Returns" is the Pareto family: it reads as a deficiency of the family, and the "does" cell just above it begins "Returns a nondominated set"); the full cell turns to ours at "the fit says" |
| DEA | "global exponents per term, not per-unit weights; a band, not extreme units" | "One exponent vector per term, a global named structure, in place of weights obtained unit by unit; ..." | **ours**, but by elision (no verb, no subject) |
| Multiplicative DEA | (no short; Appendix G only) | "One exponent vector per term, fitted to every design at once under a soft maximum with a temperature and a band, ..." | **ours** |
| Hyperbolic graph measure | (no short) | "The title's word names the level curves of V, ... not this measure; nothing here scales inputs against outputs." | **neither**: about the word |
| Production and distance functions | "Attributes in place of inputs" | "Attributes in place of inputs, and the form is fitted from a table of designs with a soft maximum." | **ours**, by elision |
| Deterministic and stochastic frontiers | "A smooth soft maximum over a simplex-constrained geometric mean" | "A smooth soft maximum over a simplex-constrained geometric mean in place of a shifted intercept, and K terms." | **ours**, by elision |
| PCA | "The criterion is a one-sided soft maximum, not variance" | "The criterion is a one-sided soft maximum, not variance, and the exponents live on the simplex, so the components are trade-offs between metrics. The two chain: ..." | **ours** ("The criterion" is ours; "not variance" names theirs) |
| Compositional and log-ratio PCA | "The criterion is one-sided, and the weights lie on the simplex" | "The criterion is one-sided, and the weights lie on the simplex; the chart is paired with the level log V ..." | **ours** |
| Geometric programming and max-affine fitting | "this method fits an envelope, the one-sided boundary of the data" | "The sources fit regression surfaces; this method fits an envelope, ..." | short **ours** (explicit "this method"); full **mixed** (opens with the sources) |
| Kernel and hyperbolic PCA | '"Hyperbolic" here means the level surfaces of V in metric space' | '"Hyperbolic" here means the level surfaces of V in metric space, unrelated to negative-curvature geometry.' | **neither**: it defines our word and says nothing of how this method differs from kernel PCA or HoroPCA (the ambiguity the supervisor names) |
| Entropic risk | (no short) | "Nothing is used from the risk-measure side; the entries are cited to avoid confusion of the soft maximum with a risk measure." | **neither**: about citing |
| MDAO | "this method fits the table the evaluations leave behind" | "MDAO drives the evaluations toward an optimum; this method fits the table ..." | short **ours**; full **mixed**, opens with theirs |
| Tradespace exploration | "this method fits and reports a coordinate system and a score" | "These explore and display; this method fits and reports ..." | short **ours**; full **mixed** |
| Decision analysis and MCDM | "The weights are fitted from the data's edge, not elicited" | same | **ours** by elision ("the weights" are the fitted ones; "not elicited" names theirs) |
| Trade studies in practice | (no short) | "The weights are fitted from the table and the analysis reruns when the data change; ..." | **ours**, by elision |
| MBSE | "The method is a model-based trade analysis, not an MBSE methodology" | same | **ours** (explicit "The method") |

Count: of the sixteen rows, Table 1 prints twelve `short.differs` cells (four rows have no short and appear only in
Appendix G). Of the twelve, ten are ours (four of them by elision, a bare noun phrase the reader must attach to a
subject), one is theirs (Pareto) and one is neither (kernel and hyperbolic PCA). In Appendix G's full cells three
open with the family and turn to ours (geometric programming, MDAO, tradespace), Pareto opens with the family's
property, and three are about a word or a citation (hyperbolic graph measure, entropic risk, kernel and hyperbolic
PCA). The one cell a reader can take for the other method's property is Pareto's; the one that does not compare
methods at all while carrying the row the supervisor asks about is kernel and hyperbolic PCA.

### 1c. What the body borrows from PCA and from scikit-learn's unsupervised estimators

| Where | The sentence | What is borrowed |
|---|---|---|
| Abstract (cell 0) and Introduction (cell 5) | "Like PCA, our method is unsupervised feature engineering; the two answer different questions and compose, as when PCA is run on the chart." | the unsupervised, table-in, coordinates-out setting |
| Introduction (cell 5) | "We take PCA as inspiration and explain tensions where it explains variance." | the move from variance to a different explained quantity; PCA's role as the trusted, interpretable reference |
| Introduction (cell 4) | "PCA reduces dimensionality and increases interpretability while minimizing information loss [@jolliffe2016principal]." | the reader's reference point |
| Results summary (cell 7) | "The method and PCA compose: PCA run on the near-frontier chart reads the trade-offs the sampling exercised, a reading and not a result (Appendix D.16)." and "The method claims nothing as novel and does not replace PCA or Pareto analysis." | chaining; no claim of replacement |
| Notation (cell 14) | "estimator terms follow the scikit-learn documentation [@pedregosa2011scikit; @buitinck2013api]" and "Stage 2 is conditioning, the analyst's step, done with scikit-learn tools" | vocabulary; conditioning delegated to scikit-learn |
| Methods (cell 18) | "The fit is a scikit-learn transformer of the decomposition family: `fit` identifies exponents and offsets, `transform` returns the chart, `inverse_transform` reverses it, `score_samples` returns the energy differential." | the API shape of `PCA`/`NMF`-type estimators |
| Methods (cell 19) | "(iii) The analyst chooses K: a modelling choice, as the number of retained components is for PCA." | the hyperparameter analogy |
| Discussion (cell 101) | "A deflation-style search for successive tensions, as PCA extracts components, is a research question: we claim neither that it works nor that tensions are orthogonal." | successive components, explicitly not claimed |
| Section 2, Lineage (cell 13) | "Kernel PCA is the feature-engineering kin of the direction in Section Discussion [@schoelkopf1998nonlinear], and "hyperbolic" here is unrelated to hyperbolic PCA [@chami2021horopca]." | kernel PCA as kin of the (unbuilt) kernel extension |
| Appendix D.16 (supporting cells 71 to 73) | "The tension report runs a principal component analysis on the chart coordinates Z of the near-frontier designs in a term's cell. Its directions say along which combinations of metrics the near-frontier designs vary the most, ... the fit says which metrics bind, the analysis says where the sampled designs spread along the fitted surface." | the chain: PCA on our chart (`orient_by_pca`, `tension_report`) |
| `docs/superpowers/notes/sklearn-conformance.md` | "Semantics (glossary): `score_samples` is the sanctioned unsupervised per-sample score; ... `predict` is for labels/targets — not on the transformer"; "decomposition-family semantics" in `CLAUDE.md` | `fit`/`transform`/`inverse_transform`/`score_samples`, `parametrize_with_checks`, no `predict` |

Nothing in the body says the method is a kind of PCA. The borrowing is of intuition (an unsupervised summary a
reader can interpret), of the estimator interface, and of PCA as a downstream step on the chart.

## 2. The code spike: HoroPCA run on the paper's tables

### Setup (what was run)

- **Code.** `github.com/HazyResearch/HoroPCA`, the official PyTorch implementation of the ICML 2021 paper
  (`chami2021horopca`), cloned at commit `c9a99967a62688711f6b63dab3baee53fe2d8430` (17 June 2021, last push to the
  repository 2023). **Licence: none.** The repository has no LICENSE file and GitHub reports no licence, so by default
  all rights are reserved; the spike runs it locally from a clone outside the repository, vendors nothing, and nothing
  of it is in the package, `pyproject.toml` or `uv.lock`.
- **Environment.** A venv under the scratchpad: Python 3.12, torch 2.15.0, numpy 2.5.4, scipy 1.18.1, networkx 3.7.
  The repository targets Python 3.7 and PyTorch 1.8.1. It ran unmodified except for one call: `torch.solve`
  (removed from PyTorch; error text on torch 2.15 and on torch 1.12.1: "This function was deprecated since version
  1.9 and is now removed. `torch.solve` is deprecated in favor of `torch.linalg.solve`"). `compat.py` restores it
  from outside (`torch.solve(B, A) = (torch.linalg.solve(A, B), None)`); the clone is not edited. Check that the
  runs are the authors' code: their own CLI on their own `smalltree` dataset (`python main.py --dataset smalltree
  --model horopca --dim 10 --n-components 2`) printed distortion 0.20 and Fréchet variance 7.15 (README: 0.19 and
  7.15); the other models on the same data (`smalltree_run.txt`): PCA 0.84 / 0.34, tangent PCA 0.70 / 1.16,
  PGA 0.62 / 2.17.
- **Tables.** Planted: `make_frontier_data` with the seeds the soft-fit tests use: K = 1 (400 x 4, seed 0), K = 2
  (300 x 3, seed 7: `test_soft_fit.py` line 56), K = 3 (400 x 4, seeds 0 and 4: lines 353 and 301). Cubesat: the
  log-metrics of record, `case.load_study` in both regimes, 13 metrics; the 3,000 designs per regime reduce to
  2,134 (primary) and 2,355 (stock) feasible designs, the tables the paper fits. Our fits: `HyperbolicTradeSpace`
  at tau = 50 for the planted tables, `case.fit_study` (tau selected by the fraction-above criterion; 41.7 and 113.2
  for K = 1, 2 in primary) for the cubesat; K = 1 and K = 2.
- **Embedding (the choice, and what it does).** Log-metrics are Euclidean coordinates; HoroPCA needs points in the
  Poincaré ball. The spike centres the log-metrics on their mean, divides by one scalar so the farthest point has
  tangent norm R in {0.25, 1, 3} (hyperbolic distance 2R from the origin: 0.5, 2, 6), and applies the exponential
  map at the origin. R is a dial: small R puts the cloud in an almost flat patch around the origin, large R
  pushes the tail toward the boundary where the geometry is far from Euclidean. Because the tangent vectors are
  centred, the Fréchet mean is the origin (offsets measured by the repository's own `Frechet` class: below 5e-4 in
  every run), which is the method's standing assumption, so the repository's reflection is the identity up to that
  tolerance and the ideal points it returns read directly as directions in log-metric space. The logarithm map at
  the origin inverts the embedding exactly (round-trip error 7e-15), so the repository's tangent PCA is ordinary PCA
  of the table (a test in `test_spike_results.py`). Nothing about the data is hyperbolic by construction: the
  embedding is the spike's choice, not a property of the tables.
- **Methods compared.** (i) ordinary PCA (SVD of the centred log-metrics); (ii) HoroPCA with k = 1 (Busemann
  variance) and k = 2 (horospherical projection, mean squared pairwise distance), best of five random restarts by
  final loss, Adam, learning rate 0.05, 500 steps (the repository's defaults).
- **Comparison with the exponents.** For a target exponent vector w (planted term, or our fitted term), the number
  reported is |cos| of the best single component with w, and for two components the alignment ||P w|| of the unit
  w with the span of the components (1 means w lies in the span). Signs of components are arbitrary and ignored.
  "Explained" is the variance share (PCA) and the repository's mean squared pairwise distance of the projections over
  that of the data (HoroPCA); in the flat limit these coincide (R = 0.25: 0.316 against PCA's 0.328 on the cubesat
  primary subsample).

**Limits of the comparison, stated.** (1) The embedding and its scale are the spike's choices; the table gives three
scales and the conclusions below hold at all three. (2) HoroPCA was fitted on all rows of the planted tables but on a
seeded subsample of 500 rows for each cubesat table: its objective is O(n^2 d) per step with autograd, and a first
attempt at 2,134 rows had not finished one k = 2 run in ten minutes. PCA is quoted on all rows (the subsample's
explained variance differs by less than 0.015). (3) The hyperparameters are the repository's defaults, not tuned;
five restarts. (4) The targets are directions in log-metric space; HoroPCA's ideal points are boundary directions,
read as the same space because the Fréchet mean is the origin. (5) One run per seed of the planted generator; four
planted tables, two cubesat regimes: a spike, not a benchmark. (6) The paper's method is not run on the data of
HoroPCA's tasks (graphs embedded in hyperbolic space); that is not a comparison either way.

### Results

Cells are |cos| of the best single component with the target (k = 1) and the span alignment (k = 2), read at
R = 0.25 / 1 / 3 for HoroPCA. Full numbers: `analysis.txt`, `results.json`.

| Table | Target | PCA: best PC (|cos|), span of PC1+PC2 | HoroPCA k = 1 |cos| | HoroPCA k = 2 span |
|---|---|---|---|---|
| planted K = 1 (400 x 4, seed 0) | planted w | PC1 (0.98), 0.99 | 0.99 / 0.97 / 0.90 | 0.99 / 0.99 / 0.99 |
| planted K = 2 (300 x 3, seed 7) | term 1 | PC3 (0.81), 0.59 | 0.55 / 0.48 / 0.41 | 0.54 / 0.44 / 0.51 |
|  | term 2 | PC3 (0.70), 0.72 | 0.62 / 0.55 / 0.48 | 0.67 / 0.57 / 0.68 |
| planted K = 3 (400 x 4, seed 0) | term 1 | PC1 (0.99), 0.99 | 0.99 / 0.99 / 0.98 | 0.99 / 0.99 / 0.99 |
|  | term 2 | PC1 (0.83), 0.83 | 0.82 / 0.82 / 0.78 | 0.82 / 0.83 / 0.80 |
|  | term 3 | PC1 (0.78), 0.82 | 0.77 / 0.74 / 0.69 | 0.83 / 0.89 / 0.83 |
| planted K = 3 (400 x 4, seed 4) | term 1 | PC1 (0.79), 0.80 | 0.78 / 0.74 / 0.68 | 0.78 / 0.78 / 0.80 |
|  | term 2 | PC4 (0.82), 0.51 | 0.48 / 0.42 / 0.35 | 0.49 / 0.50 / 0.54 |
|  | term 3 | PC1 (0.64), 0.70 | 0.63 / 0.59 / 0.54 | 0.68 / 0.70 / 0.73 |
| cubesat primary (2,134 x 13) | our K = 1 term | PC10 (0.51), 0.02 | 0.03 / 0.02 / 0.04 | 0.03 / 0.03 / 0.06 |
|  | our K = 2 term 1 | PC8 (0.70), 0.39 | 0.26 / 0.24 / 0.27 | 0.38 / 0.34 / 0.33 |
|  | our K = 2 term 2 | PC10 (0.50), 0.09 | 0.09 / 0.08 / 0.01 | 0.09 / 0.09 / 0.08 |
| cubesat stock (2,355 x 13) | our K = 1 term | PC7 (0.75), 0.05 | 0.03 / 0.03 / 0.05 | 0.04 / 0.03 / 0.06 |
|  | our K = 2 term 1 | PC9 (0.50), 0.18 | 0.18 / 0.27 / 0.29 | 0.24 / 0.33 / 0.36 |
|  | our K = 2 term 2 | PC7 (0.80), 0.09 | 0.07 / 0.07 / 0.05 | 0.08 / 0.07 / 0.08 |

Variance explained. PCA, PC1 and PC1+PC2: planted K = 1 0.563 / 0.734; K = 2 0.651 / 0.842; K = 3 seed 0 0.554 /
0.717; seed 4 0.620 / 0.773; cubesat primary 0.325 / 0.523; stock 0.298 / 0.498. HoroPCA k = 1 / k = 2 at
R = 0.25, 1, 3: planted K = 1 0.562, 0.528, 0.410 / 0.735, 0.730, 0.711; cubesat primary 0.316, 0.216, 0.068 /
0.530, 0.492, 0.600. Our own fitted terms are not variance explanations and have no such number.
Run to run, HoroPCA's k = 1 optimum is not unique at the large scale: at R = 3 the five restarts end between 0.211
and 0.410 on planted K = 1 and between 0.293 and 0.538 on planted K = 2; at R = 0.25 the spread is 0.003 to 0.02.

**Reading.**

1. *Where a planted term and the leading direction coincide, both recover it; elsewhere neither does.* PCA's first
   component and HoroPCA's first direction match the planted K = 1 exponent at |cos| 0.98 and 0.99 (0.90 at R = 3);
   they match the K = 3 seed-0 terms at 0.99 / 0.83 / 0.78. That is a property of the generator: its interior
   designs sit at an exponentially distributed depth below the surface, so the largest spread of the cloud lies along
   the exponent vector. With K = 2 (d = 3) the best-matching PC is the third, the smallest-variance one, at 0.81 / 0.70;
   with seed 4 the term-2 match is PC4 of four. The exponent vector of a surface is not the direction of largest
   variance in general, and on the cubesat tables it is not close to it: our K = 1 exponent has span 0.02 (primary)
   and 0.05 (stock) with PC1+PC2, and its best match is PC10 and PC7 (|cos| 0.51 and 0.75). Between 0.03 and 0.06 is all
   either HoroPCA configuration captures of it.
2. *HoroPCA behaves like PCA at small scale and differently at large scale.* At R = 0.25 its explained fractions and
   directions agree with PCA's within 0.01 on the planted tables and within 0.012 on the cubesat. At
   R = 3 the Busemann (k = 1) objective picks directions that explain far less Euclidean variance (cubesat primary
   0.068 against PCA's 0.325) and the optimum depends on the restart; the k = 2 objective stays close to PCA's
   subspace on the planted tables (0.99 span on K = 1) and drifts on the cubesat.
3. *Neither names which metrics trade or at what rate.* PCA loadings and HoroPCA's ideal points are unit vectors
   with mixed signs and no sum-to-one scale. On the cubesat primary the first two PCs mix signs on the metrics (e.g. total mass
   -0.41 against available power +0.40 on PC1) and neither is sign-pure; the K = 1 fit names eight metrics with
   exponents summing to 1 (unit cost 0.257, available power 0.197, pointing error 0.156, fleet cost 0.151,
   momentum headroom 0.107, settling time 0.068, depth of discharge 0.042, total mass 0.021) and five at zero. A
   covariance pattern with opposite signs is a statement about how the sample spreads; it carries no elasticity (the
   rate at which one metric buys another along the surface) and no statement about the edge of the data.
   On planted K = 1 PC1 is sign-pure (all loadings positive) and its loadings (0.54, 0.43, 0.54, 0.48) sit near the
   exponents (0.23, 0.29, 0.25, 0.23) up to scale: an agreement of the generator, not a rate.
4. *The tables are not tree-like.* The Gromov four-point relative delta (400,000 sampled quadruples, 300 points) of
   the log-metric clouds is 0.46 (cubesat primary) and 0.45 (stock) against 0.42 and 0.39 for Gaussian clouds of
   the same dimension, and 0.26 to 0.33 for the planted tables; the repository's tree dataset has 0.00
   (`gromov.txt`). HoroPCA's published advantage is on tree-like and hierarchical data (on `smalltree` above, distortion 0.20 against
   0.84 for PCA); the paper's tables do not have that structure, so a hyperbolic embedding of log-metrics is available
   (any Euclidean cloud can be put in the ball) but nothing in the data asks for it.

**What each is good for, and when one would reach for it.**

- *HoroPCA.* Reducing the dimension of data that is already hyperbolic or tree-like (embeddings of graphs,
  taxonomies, phylogenies) while keeping distances, and as a whitening or visualization step for them; its authors
  report this (distance preservation, downstream classification, 2-D visualization). Reach for it when the points
  live on a hyperbolic manifold and Euclidean PCA distorts their distances. It does what this work does not: it has
  nothing to say about an edge, but it respects negative curvature, which this work never uses.
- *PCA.* Where a table spreads: the directions of largest variance, in closed form, with variance shares. It is
  the right first look at a table, and it chains with this work (Appendix D.16 runs it on the chart).
- *This work.* The one-sided edge of a table of evaluated designs: which metrics bind, with what elasticities, a level
  for every design, a reversible chart; convex, with a certificate. It has nothing to say about tree-like data or
  about where the sample spreads. The three answer different questions; the one the spike finds closest to ours in
  the setting (unsupervised, a table in, a coordinate system out) is the nearest in setting, and the farthest in
  what is estimated.

## 3. The solvers

HoroPCA (`learning/pca.py`, `geom/horo.py`, `geom/hyperboloid.py`) parameterizes the k components as k free vectors
in R^d, renormalized (k = 1) or Gram-Schmidt orthonormalized (k > 1) at every step into ideal points on the ball's
boundary. The horospherical projection is closed form and differentiable: for k = 1 the Busemann function
(`busemann`), for k > 1 a Minkowski-space Gram solve (`torch.solve`) for the orthogonal projection onto the spanned
geodesic submanifold followed by a move along the tangent toward the origin (`hyperboloid.horo_projection`). The
objective is the variance of the projections: for k = 1 `torch.var` of the Busemann values, for k > 1 the mean squared
pairwise hyperbolic distance of the projected points (an O(n^2) Fréchet-variance surrogate; options for a learned
mean and for summing the objective over nested subspaces exist). It is maximized with Adam, a fixed 500 steps at
learning rate 0.05, no convergence test, from random normal initial components, with restarts chosen by the caller
(`--n-runs`); components can be found jointly or one at a time with earlier ones frozen. The program is not convex and
the code gives no certificate: the spike saw different local optima across restarts at the large scale. The only
closed form in the file is for Euclidean and tangent PCA (SVD in `fit_spectral`); `HoroPCA` does not define it and the
base class raises `NotImplementedError`, and the paper's conclusion lists "deriving a closed-form solution" as future
work. The data must have its Fréchet mean at the origin, which the script obtains by a gradient iteration with a
fixed step schedule (falling back to the Euclidean mean if it does not converge). This work's programs are of a
different kind: the exponent vector lives on a simplex and the criterion is one-sided, so the K = 1 fit at tau =
infinity is a linear program (solved exactly), at finite tau a smooth convex program in the logarithmic variables
(the GP form, solved by SLSQP with an analytic Jacobian and a KKT-gap termination record), and K > 1 alternates
assigning designs to terms with a separate convex refit per term, which is a local method over assignments whose
every refit is globally solved. So the two optimizations differ in kind: HoroPCA maximizes a nonconvex variance over
orthonormal frames by stochastic-start gradient ascent; this work minimizes a convex criterion over a simplex with
a certificate, and is nonconvex only through the K-term assignment.

## 4. What they share in the scikit-learn sense, and the "kernel" question

**Shared.** Both are unsupervised: `fit` takes a table and no target. Both learn, in `fit`, a low-parameter object
(a frame of components; exponent vectors and offsets) and then give the data coordinates (HoroPCA `map_to_ball`,
this work `transform`). Both need a choice of the number of components (HoroPCA `n_components`, ours K). Both need
conditioning of the data first (HoroPCA: centring at the Fréchet mean; ours: strictly positive larger-is-better
metrics). Both can be followed by or chained with PCA. That is the decomposition-family idea this work borrows
(`fit`, `transform`, `inverse_transform`, `score_samples`; Section 1c).

**Differing in that sense.** The repository is not a scikit-learn estimator: it is a `torch.nn.Module` whose
`fit(x, iterative, optim)` takes a tensor, with no `get_params`/`set_params`, no `check_is_fitted`, no
`inverse_transform` (its projection is lossy: k coordinates from d) and no `score_samples`; the user supplies the
embedded, Fréchet-centred points and the result depends on the random initialization. Ours is a scikit-learn
transformer that passes `parametrize_with_checks`, with a reversible chart and a per-design score, deterministic
given the table.

**Is HoroPCA "PCA with a specific kernel"? No, on the evidence we have.** (1) The paper (arXiv 2106.03306, text
extracted and searched) does not contain the word "kernel". Its abstract and Section 3 say it generalizes the three
parts of PCA to hyperbolic space: the parameterization of subspaces (nested sequences of geodesic submanifolds
spanned by ideal points and a base point), the projection (horospherical, preserving Busemann coordinates), and an
objective (an intrinsic variance built from pairwise distances). (2) Kernel PCA is linear PCA on the
eigendecomposition of a Gram matrix of a positive semidefinite kernel; HoroPCA has no Gram matrix and no
eigendecomposition: its objective is a nonquadratic function of the points, optimized by gradient (Section 3 above).
(3) The nearest true statement of the supervisor's intuition is about the paper's *baseline*, tangent PCA: it is PCA
after a fixed explicit nonlinear map (the logarithm map at the Fréchet mean), which is "PCA with a feature map",
solved by SVD (`TangentPCA.fit_spectral`). HoroPCA is offered as the alternative to exactly that. What would be
accurate: HoroPCA is a generalization of PCA to a negative-curvature geometry (Riemannian PCA with horospherical
projections), not a kernel method. Not shown here: that no kernel can be found whose PCA reproduces it; the
claim made is that neither the paper nor the code presents it so.

## 5. Plain options for the paper's acknowledgement and distinction

The facts to build on: HoroPCA is a generalization of PCA to hyperbolic space for hyperbolic or tree-like data; this
work fits a one-sided posynomial edge to a table and is not a PCA of any kind; the setting and the interface are
shared; on the paper's tables neither HoroPCA nor PCA recovers our exponents except where the generator makes the
exponent direction the direction of largest spread; the two can chain (the spike embedded the log-metrics into the ball to do it,
and that embedding is not natural for them).

Question 1, how much of the spike enters the paper.
- (a) Section 2 holds one concise paragraph naming HoroPCA and what it generalizes, what this work borrows (the
  unsupervised setting, the estimator interface, PCA as a downstream step), and that the spike's runs found no
  recovery of the exponents beyond the generator's own variance; Appendix G carries the full version and the
  results table of section 2 here.
- (b) As (a), with the spike's table and code kept in `docs/superpowers/notes/spike-horopca/` and cited as a note,
  the appendix saying only what was run and what it showed in two or three sentences.
- (c) Section 2 and Appendix G carry the distinction from the literature alone (what HoroPCA is, what this work
  is), without the spike's numbers; the spike stays a record in the work package.

Question 2, Table 1's row.
- (a) Split "Kernel and hyperbolic PCA" into two rows, kernel PCA and HoroPCA, each `differs` cell with this work
  as the subject.
- (b) Keep one row and rewrite its `differs` cell with this work as the subject.
- (c) Drop the HoroPCA half from the table (Section 2's paragraph carries it) and keep a kernel PCA row.

Question 3, the word "hyperbolic".
- (a) One glossary entry (the level curves of V, products of powers of metrics; not negative-curvature geometry,
  not the Färe, Grosskopf and Lovell measure); Appendix A prints it; Section 2 and the docs point to it and the
  two body caveats go; the docs' second definition ("the shape of the score") is replaced by the pointer.
- (b) As (a), and the Section 2 caveat against Färe et al. stays in one sentence beside the title's first
  mention.
- (c) Change the title and the word where it names the surface (a different word for the level curves).

Question 4, how HoroPCA is described.
- (a) "The closest existing analog" as the supervisor put it, said in terms of setting only (unsupervised,
  table in, coordinates out).
- (b) "A generalization of PCA to negative curvature" without a closeness claim.

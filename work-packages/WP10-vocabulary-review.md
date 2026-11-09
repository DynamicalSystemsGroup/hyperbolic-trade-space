# WP10 Amendment 4, R-36: the vocabulary review (stream P3)

Run on the pinned commit `78f5e1cf984d4589a9232717023f408358c25803` (`git cat-file -t` gives commit). Record of the one full reading of everything a reader can reach,
under `docs/superpowers/notes/vocabulary-review.md` ("The reading", "Triage"). Nothing was edited: dispositions are recorded, not applied.

## How the reading was run

- Units: one per section of `paper/paper.ipynb` (the abstract, then each `##` section, with `Results` split at its `###` headings), one
  per appendix of `paper/supporting_material.ipynb` (Appendices B, D, E and G cut at their headings to at most about 28 kB each), one per
  page of `docs/*.md` and `docs/user-guide/*.md`, plus `site/index.html` and `README.md`. 54 units. Not read: the paper's
  empty front matter and its Works cited (37 characters; no prose). Order: density, densest first, the density being terms of art per
  100 words computed with the tool's own term matcher over each unit's text (the tool's per-section table is below).
- Text staged: the rendered reader-visible text of each unit as a plain file (notebook Markdown cells with generated tables; docs pages
  without front matter; the HTML text), plus the Glossary compiled from `glossary.yaml` as term and short, alphabetical. Files lived in the
  scratchpad, outside the repository.
- One fresh-context reader (a Sonnet subagent with no other context) per unit, handed only the unit file and the Glossary file. The
  hand-off text, recorded once (the first six readers had the same content in longer wording; the file names changed per unit):

> You are a fresh-context reader of one unit of technical documentation for a reader at the level of calculus, linear algebra and convex optimization (Boyd and Vandenberghe) and scikit-learn. Read exactly two files and nothing else (do not browse, search or open any other file or directory): 1. the Glossary (P3-units/GLOSSARY.txt); 2. the unit (P3-units/<unit file>). Read as a new reader with only this unit and the Glossary. Return three lists, each item with the whole sentence quoted verbatim, then the term(s) concerned and one short line of why: LIST 1 terms unresolved from the unit and the Glossary; LIST 2 places where a Glossary term would say it shorter or more exactly than the words used (name the term); LIST 3 terms of art that plain words would serve as well (name the plain words), and separately sentences where three or more terms of art arrive together. Selective, quoted, "none" if empty; no edits proposed beyond naming the term or plain words; no praise or summary. Write to P3-readings/<unit file>.md with headings LIST 1, LIST 2, LIST 3a, LIST 3b; reply "done".

- The readers' lists are quoted verbatim below. Their wording of the three lists varies slightly; the four headings are normalised.
- Triage: every item carries exactly one of the five dispositions (amend glossary entry; plain words; glossary term; add to `avoid`;
  no change, with the reason). **The dispositions were assigned by stated rules, not item by item by hand**: List 1 items are
  `amend glossary entry` unless the term is standard vocabulary at the assumed reader level (kernel, PCA, convex program, Pareto,
  Hessian, KKT, Lagrangian, softmax, gradient, eigen, transformer, scikit-learn terms: `no change`); List 2 items are `glossary term`;
  List 3a items are `plain words`; List 3b items are `plain words` on the introductory pages (abstract, section 1, README, root page,
  docs index, getting started, overview) and `no change` elsewhere; items on sentences that report a source (prior art, Appendix G,
  Further reading) are `no change`; items quoting a phrase withdrawn by Amendment 4 ("exchange rate", "model of the table", "generalized
  posynomial" outside a source report) are `add to avoid`. A reader asserting a clash over a term's meaning is marked `to the driver`.
  The glossary owner should treat each `amend glossary entry` as a candidate: the rule cannot tell a missing entry from a missing
  definition at first use, and either closes the item.
- Routing: items on paper sections 4 (Definitions) and 6 (Results, with its fit, algorithm and open-questions parts) and on any paper
  sentence on soft-fit wording are `routed to P1`; items on `docs/examples.md` and on soft-fit wording in docs pages are `routed to P6`.
  State of both at the pinned commit (PM-BRIEF, "Current state at the handover"): running under the outgoing PM, to be finished by it.

## The tool at the pinned commit

`uv run python scripts/check_vocabulary.py --density` exits **1** at the pinned commit: 97 new violations, 0 known (the Amendment 4
vocabulary pass that clears them is not part of this stream). Output, verbatim:

```
FAIL avoid: docs/index.md [hyperbolic-trade-space] 'exchange rates'  ...at what exchange rate
FAIL first-use: paper/paper.ipynb [The algorithm for several facets] 'assignment'  ...On the assignment-stable neighbourhood, with offsets  ,  , so   is a local minimizer of the mean slack. Global optimalit
FAIL first-use: paper/paper.ipynb [] 'fit temperature'  ...Temperatures and band
 
The fit temperature   sets how hard the maximum is (  is exact); the term temperature   how shar
FAIL first-use: paper/paper.ipynb [The fit and its geometry] 'improvement factor'  ...Two results say what the fitted numbers mean: the soft maximum of Gaussian noise has a closed form (L6), and along a fac
FAIL first-use: paper/paper.ipynb [] 'invariant value'  ...The invariant value   is a weighted geometric mean of the metrics; doubling every metric doubles it. It stays the same a
FAIL first-use: paper/paper.ipynb [] 'level offset'  ...The chart
 
 , with   and  , is the position along the frontier, free of overall scale.   is the chart, a reversible rew
FAIL first-use: paper/paper.ipynb [] 'position along the frontier'  ...The chart
 
 , with   and  , is the position along the frontier, free of overall scale.   is the chart, a reversible rew
FAIL first-use: paper/paper.ipynb [] 'term temperature'  ...Temperatures and band
 
The fit temperature   sets how hard the maximum is (  is exact); the term temperature   how shar
FAIL stem: docs/api.md [API] 'fitted surface'  ...the fitted surface as a
FAIL stem: docs/examples.md [A cubesat trade study across power, mass and attitude control] 'power margin'  ...power margin
FAIL stem: docs/getting-started.md [Reading the output] 'working temperature'  ...at the working temperature
FAIL stem: docs/index.md [hyperbolic-trade-space] 'exchange rate'  ...at what exchange rate
FAIL stem: docs/theory.md [Elasticities and the n-lemma] 'constant rate'  ...metric at constant rate
FAIL stem: docs/theory.md [Elasticities and the n-lemma] 'level surface'  ...the level surface is flat
FAIL stem: docs/theory.md [V = 1 is the fitted reference surface] 'working temperature'  ...at the working temperature tau
FAIL stem: docs/user-guide/chart.md [Reading log V] 'finite temperature'  ...at a finite temperature some training
FAIL stem: docs/user-guide/conditioning.md [Conditioning] 'error rate'  ...error rate
FAIL stem: docs/user-guide/conditioning.md [Conditioning] 'fitted surface'  ...report the fitted surface back in
FAIL stem: docs/user-guide/fitting.md [Several terms] 'finite temperature'  ...at finite temperature only
FAIL stem: docs/user-guide/fitting.md [One term] 'mean gap'  ...is the mean gap between facet
FAIL stem: docs/user-guide/fitting.md [Choosing the temperature] 'select temperature'  ...select temperature
FAIL stem: docs/user-guide/limitations.md [Limitations] 'finite temperature'  ...at a finite temperature some design
FAIL stem: docs/user-guide/limitations.md [Limitations] 'infinite temperature'  ...exact at infinite temperature with at
FAIL stem: docs/user-guide/limitations.md [Limitations] 'learned surface'  ...beyond the learned surface
FAIL stem: docs/user-guide/limitations.md [Limitations] 'varying rate'  ...for regionally varying rate fit several
FAIL stem: docs/user-guide/limitations.md [Limitations] 'working temperature'  ...at a working temperature
FAIL stem: docs/user-guide/tensions.md [The contending set and the n-lemma] 'fitted temperature'  ...of the fitted temperature
FAIL stem: docs/user-guide/tensions.md [The contending set and the n-lemma] 'infinity program'  ...infinity program itself
FAIL stem: docs/user-guide/tensions.md [Participation and elasticities] 'working temperature'  ...at the working temperature the exponent
FAIL stem: docs/user-guide/termination.md [Statuses] 'infinite temperature'  ...at infinite temperature this happen
FAIL stem: docs/user-guide/termination.md [Statuses] 'largest gap'  ...and the largest gap
FAIL stem: docs/user-guide/termination.md [Reading `termination_` and `conditioning_`] 'max gap'  ...max gap 0
FAIL stem: docs/user-guide/termination.md [How small is a small margin] 'median gap'  ...the median gap between a
FAIL stem: docs/user-guide/termination.md [How small is a small margin] 'median margin'  ...with the median margin
FAIL stem: docs/user-guide/termination.md [The three levels] 'smallest gap'  ...is the smallest gap by which
FAIL stem: docs/user-guide/termination.md [Statuses] 'weighted gap'  ...weighted gap within and
FAIL stem: paper/paper.ipynb [Open questions] 'across temperature'  ...1 fit across temperature on the
FAIL stem: paper/paper.ipynb [] 'convex envelope'  ...a log convex envelope
FAIL stem: paper/paper.ipynb [The algorithm for several facets] 'duality gap'  ...the lp duality gap
FAIL stem: paper/paper.ipynb [Open questions] 'fitted surface'  ...which the fitted surface recover the
FAIL stem: paper/paper.ipynb [] 'level surface'  ...mean the level surface of v
FAIL stem: paper/paper.ipynb [Open questions] 'power margin'  ...power margin
FAIL stem: paper/paper.ipynb [abstract] 'reference surface'  ...fitted posynomial reference surface model the
FAIL stem: paper/paper.ipynb [The algorithm for several facets] 'row gap'  ...sketch each row gap to every
FAIL stem: paper/paper.ipynb [Open questions] 'sample envelope'  ...not the sample envelope
FAIL stem: paper/paper.ipynb [Open questions] 'selected temperature'  ...the selected temperature is tau
FAIL stem: paper/paper.ipynb [] 'sided envelope'  ...a one sided envelope of the
FAIL stem: paper/paper.ipynb [] 'working temperature'  ...working temperature exponent grade
FAIL stem: paper/supporting_material.ipynb [L17. the soft-fit certificate: Hessian D - kappa M and the second-order test] 'abstraction gap'  ...assumption and abstraction gap
FAIL stem: paper/supporting_material.ipynb [L10. Extension Phi_K: shift equivariance, K = 1 reduction, kappa -> infinity = max] 'assert gap'  ...assert gap
FAIL stem: paper/supporting_material.ipynb [L17. the soft-fit certificate: Hessian D - kappa M and the second-order test] 'different temperature'  ...fit at different temperature
FAIL stem: paper/supporting_material.ipynb [L12. facet first-order gap: 0 <= f(w) - f* <= G, G = 0 iff the simplex KKT holds] 'duality gap'  ...the lp duality gap
FAIL stem: paper/supporting_material.ipynb [] 'explicit radius'  ...explicit radius
FAIL stem: paper/supporting_material.ipynb [L10. Extension Phi_K: shift equivariance, K = 1 reduction, kappa -> infinity = max] 'extension temperature'  ...the extension temperature is positive
FAIL stem: paper/supporting_material.ipynb [] 'finite temperature'  ...possible at finite temperature
FAIL stem: paper/supporting_material.ipynb [] 'fitted surface'  ...of the fitted surface in log
FAIL stem: paper/supporting_material.ipynb [] 'infinite temperature'  ...of the infinite temperature fit
FAIL stem: paper/supporting_material.ipynb [L13. assignment margin: score changes below gamma/2 keep the maximizing facets; explicit radius] 'instance margin'  ...instance margin or labels'
FAIL stem: paper/supporting_material.ipynb [Dimension reduction and model fitting] 'level surface'  ...mean the level surface of v
FAIL stem: paper/supporting_material.ipynb [L12. facet first-order gap: 0 <= f(w) - f* <= G, G = 0 iff the simplex KKT holds] 'lp gap'  ...the lp gap is the
FAIL stem: paper/supporting_material.ipynb [L17. the soft-fit certificate: Hessian D - kappa M and the second-order test] 'max gap'  ...max gap
FAIL stem: paper/supporting_material.ipynb [L17. the soft-fit certificate: Hessian D - kappa M and the second-order test] 'maximal gap'  ...hold the maximal gap
FAIL stem: paper/supporting_material.ipynb [L2. Uniform shift: J_tau(w; U + c 1^T) = J_tau(w; U) + c] 'maximum temperature'  ...the soft maximum temperature is positive
FAIL stem: paper/supporting_material.ipynb [] 'objective margin'  ...the objective margin
FAIL stem: paper/supporting_material.ipynb [] 'order gap'  ...the first order gap of the
FAIL stem: paper/supporting_material.ipynb [L13. assignment margin: score changes below gamma/2 keep the maximizing facets; explicit radius] 'perturbed margin'  ...perturbed margin below gamma
FAIL stem: paper/supporting_material.ipynb [L14. Proposition 3] 'positive margin'  ...r2 positive margin
FAIL stem: paper/supporting_material.ipynb [L17. the soft-fit certificate: Hessian D - kappa M and the second-order test] 'power margin'  ...power margin
FAIL stem: paper/supporting_material.ipynb [L17. the soft-fit certificate: Hessian D - kappa M and the second-order test] 'recovery rate'  ...a recovery rate is quoted
FAIL stem: paper/supporting_material.ipynb [Optimization and efficiency analysis] 'reference surface'  ...return a reference surface with coordinate
FAIL stem: paper/supporting_material.ipynb [Dimension reduction and model fitting] 'regression surface'  ...source fit regression surface
FAIL stem: paper/supporting_material.ipynb [L12. facet first-order gap: 0 <= f(w) - f* <= G, G = 0 iff the simplex KKT holds] 'row gap'  ...the row gap in l13
FAIL stem: paper/supporting_material.ipynb [L17. the soft-fit certificate: Hessian D - kappa M and the second-order test] 'selected temperature'  ...the selected temperature
FAIL stem: paper/supporting_material.ipynb [Optimization and efficiency analysis] 'sided envelope'  ...a one sided envelope of the
FAIL stem: paper/supporting_material.ipynb [Dimension reduction and model fitting] 'sided surface'  ...fitted one sided surface
FAIL stem: paper/supporting_material.ipynb [] 'signomial program'  ...phrase for signomial program
FAIL stem: paper/supporting_material.ipynb [L6. Gaussian cumulant of a weighted noise sum] 'summand gap'  ...assert summand gap
FAIL stem: paper/supporting_material.ipynb [L2. Uniform shift: J_tau(w; U + c 1^T) = J_tau(w; U) + c] 'unshifted gap'  ...equal the unshifted gap
FAIL stem: paper/supporting_material.ipynb [] 'working temperature'  ...at the working temperature
FAIL stem: paper/supporting_material.ipynb [L17. the soft-fit certificate: Hessian D - kappa M and the second-order test] 'zero margin'  ...with a zero margin or an
FAIL stem: src/hyperbolic_trade_space/estimator.py [HyperbolicTradeSpace] 'finite temperature'  ...act at finite temperature
FAIL stem: src/hyperbolic_trade_space/estimator.py [HyperbolicTradeSpace] 'parameter temperature'  ...parameter temperature
FAIL stem: src/hyperbolic_trade_space/estimator.py [HyperbolicTradeSpace] 'weighted gap'  ...mean the weighted gap are within
FAIL stem: src/hyperbolic_trade_space/gaps.py [module] 'knn gap'  ...knn gap score
FAIL stem: src/hyperbolic_trade_space/plotting.py [plot_frontier_surface_3d] 'wireframe surface'  ...the black wireframe surface v
FAIL stem: src/hyperbolic_trade_space/solvers.py [facet_gap] 'duality gap'  ...linear programming duality gap for the
FAIL stem: src/hyperbolic_trade_space/solvers.py [log_mean_exp] 'float temperature'  ...float temperature
FAIL stem: src/hyperbolic_trade_space/solvers.py [Termination] 'max gap'  ...max gap eps fea
FAIL stem: src/hyperbolic_trade_space/solvers.py [simplex_gap] 'order gap'  ...first order gap g
FAIL stem: src/hyperbolic_trade_space/solvers.py [solve_terms] 'recovery rate'  ...recovery rate on the
FAIL stem: src/hyperbolic_trade_space/solvers.py [soft_certificate] 'return gap'  ...return gap
FAIL stem: src/hyperbolic_trade_space/solvers.py [Termination] 'smallest gap'  ...is the smallest gap by which
FAIL stem: src/hyperbolic_trade_space/solvers.py [Termination] 'weighted gap'  ...every term weighted gap is at
FAIL stem: src/hyperbolic_trade_space/tensions.py [tension_report] 'fitted temperature'  ...of the fitted temperature and min
FAIL stem: src/hyperbolic_trade_space/tensions.py [tension_report] 'matching temperature'  ...and the matching temperature
FAIL stem: src/hyperbolic_trade_space/tensions.py [TensionReport] 'working temperature'  ...at the working temperature
FAIL stem: src/hyperbolic_trade_space/tuning.py [select_temperature] 'return temperature'  ...return temperature
once-used terms (1): termination status

terms of art per 100 words, by section
  37.5     3/8     src/hyperbolic_trade_space/datasets.py :: module
  25.0     3/12    src/hyperbolic_trade_space/estimator.py :: _conditioning
  20.0     3/15    src/hyperbolic_trade_space/plotting.py :: facet_labels
  20.0     3/15    src/hyperbolic_trade_space/plotting.py :: _ternary_colours
  18.7    17/91    src/hyperbolic_trade_space/gaps.py :: frontier_targets
  16.9    10/59    docs/user-guide/conditioning.md :: The pull-back to attributes
  14.3     3/21    docs/user-guide/fitting.md :: Synthetic data
  14.3     2/14    src/hyperbolic_trade_space/plotting.py :: _ternary_regions
  14.1    11/78    src/hyperbolic_trade_space/preconditioning.py :: module
  13.5    17/126   src/hyperbolic_trade_space/plotting.py :: _tension_panel
  13.3     2/15    src/hyperbolic_trade_space/tensions.py :: _report
  13.3     2/15    src/hyperbolic_trade_space/estimator.py :: _zero_limit_scores
  13.2     5/38    src/hyperbolic_trade_space/predictive.py :: fit
  13.2     5/38    docs/user-guide/tensions.md :: With several terms
  12.5    10/80    docs/user-guide/prediction.md :: Predicting from configuration
  12.5     2/16    src/hyperbolic_trade_space/plotting.py :: _ternary_says
  12.5     2/16    src/hyperbolic_trade_space/datasets.py :: _identifiable
  12.1     4/33    src/hyperbolic_trade_space/predictive.py :: predict_novelty
  12.0    22/183   docs/api.md :: API
  12.0     9/75    docs/user-guide/chart.md :: Plots
  12.0     6/50    src/hyperbolic_trade_space/estimator.py :: assign_facets
  11.8    13/110   docs/theory.md :: Elasticities and the n-lemma
  11.6     5/43    src/hyperbolic_trade_space/predictive.py :: predict_coordinates
  11.6    28/241   docs/examples.md :: Three metrics as shares of a total
  11.1     6/54    src/hyperbolic_trade_space/estimator.py :: module
  11.1     6/54    src/hyperbolic_trade_space/estimator.py :: inverse_transform
  11.1     4/36    src/hyperbolic_trade_space/estimator.py :: fit
  11.0    14/127   docs/examples.md :: The one-term fit, drawn
  11.0     9/82    docs/user-guide/tensions.md :: Participation and elasticities
  10.9    18/165   src/hyperbolic_trade_space/datasets.py :: make_configured_frontier_data
  10.8    12/111   docs/user-guide/overview.md :: What you supply, what you get back
  10.6    10/94    docs/user-guide/termination.md :: The three levels
  10.6     7/66    docs/user-guide/overview.md :: The pipeline
  10.5    28/266   src/hyperbolic_trade_space/predictive.py :: TradeSpaceRegressor
  10.4     5/48    docs/user-guide/termination.md :: `conditioning_`
  10.2     9/88    docs/user-guide/termination.md :: Reading `termination_` and `conditioning_`
  10.2    18/177   docs/further-reading.md :: Further reading
  10.1    17/169   docs/user-guide/fitting.md :: Several terms
  10.0    39/389   src/hyperbolic_trade_space/datasets.py :: make_frontier_data
  10.0    20/200   paper/paper.ipynb :: abstract

densest paragraphs
  25.0  docs/examples.md [Three metrics as shares of a total] Figure 8. Designs by shares of three metrics: regions, numbered exponent vectors, lines of equal V.
  23.5  paper/supporting_material.ipynb [L17. the soft-fit certificate: Hessian D - kappa M and the second-order test] | Planted facet | metric 1 | metric 2 | metric 3 | metric 4 | | facet 1 | 0.5 | 0.5 | 0 | 0 | | facet 2 | 0 | 0.5 | 0.5 | 0 | | facet 3 | 0 
  20.8  docs/user-guide/fitting.md [Several terms] One term is one flat facet in log space with constant elasticities. When the rates vary by region, fit facets, where you choose K:
  20.0  src/hyperbolic_trade_space/plotting.py [facet_labels] Facet of each row of X as "facet 1" .. "facet K" , for color= ( K > 1 ).
  20.0  src/hyperbolic_trade_space/plotting.py [plot_log_plane] Two metrics in the log plane: data, the frontier line and the near-frontier band.
  20.0  src/hyperbolic_trade_space/plotting.py [_ternary_colours] Facet colours: a facet that trades all three metrics is amber, the others blue, green, ...
  19.2  paper/paper.ipynb [] **Words.** A posynomial is a sum of monomials. A term, a monomial and a facet are one object: the term of the posynomial, the product of pow
  19.0  src/hyperbolic_trade_space/gaps.py [frontier_targets] Returns dict "metrics" : ndarray of shape (n_points, d), with V = 1 and chart coordinates Z_points ; "attributes" : preconditioner.inverse_t
  18.8  src/hyperbolic_trade_space/plotting.py [plot_ternary] Shares of a total among three metrics, as a triangle: where the facets dominate and peak.
  18.2  paper/paper.ipynb [The fit and its geometry] Sketch Simplex exponents turn the shift into in every term; the bounds are the squeeze of {prf:ref} ; each term is a monomial (I4: log-sum-e
  18.2  docs/user-guide/chart.md [Plots] - : two metrics, the data, the frontier and its band. - : three metrics, the frontier surface. - : the chart, with optional holes and target
  17.6  src/hyperbolic_trade_space/plotting.py [ternary_marker_values] Parameters estimator : HyperbolicTradeSpace A fitted estimator with three metrics. X : array-like of shape (n_samples, 3) The table of stric
  17.4  paper/paper.ipynb [Open questions] fig-chart-k3 The chart of the K = 3 fit: the first three position coordinates, coloured by facet, near-frontier designs outlined. enlarge
  17.4  docs/user-guide/fitting.md [Choosing K, the temperature and the band] Figure 2. Three facets fitted to two metrics: each facet is a straight line in log space, and the frontier is their envelope.
  17.2  docs/user-guide/prediction.md [Predicting from configuration] answers a question the unsupervised estimator cannot: where would a configuration without measurements fall? It composes two fits. `fit(X_co
97 new violation(s), 0 known
```

## Units, in density order

| # | Unit | Terms of art per 100 words |
|---|---|---|
| 1 | docs/api.md | 12.0 |
| 2 | paper/supporting_material.ipynb :: Appendix A. Notation and terms | 10.7 |
| 3 | docs/further-reading.md | 10.2 |
| 4 | paper/paper.ipynb :: Definitions | 9.9 |
| 5 | paper/paper.ipynb :: Title and abstract | 9.5 |
| 6 | docs/examples.md | 8.6 |
| 7 | paper/paper.ipynb :: Methods | 8.6 |
| 8 | docs/user-guide/prediction.md | 8.4 |
| 9 | docs/user-guide/tensions.md | 8.1 |
| 10 | docs/user-guide/chart.md | 7.9 |
| 11 | docs/theory.md | 7.5 |
| 12 | README.md | 7.4 |
| 13 | docs/user-guide/termination.md | 7.3 |
| 14 | docs/user-guide/fitting.md | 7.3 |
| 15 | paper/supporting_material.ipynb :: Appendix D. Extended results: what the method found in the table (part 2) | 7.3 |
| 16 | paper/paper.ipynb :: The fit and its geometry | 7.2 |
| 17 | paper/paper.ipynb :: Preliminaries and notation | 7.2 |
| 18 | docs/user-guide/overview.md | 7.1 |
| 19 | docs/user-guide/conditioning.md | 6.3 |
| 20 | site/index.html | 6.0 |
| 21 | docs/getting-started.md | 6.0 |
| 22 | paper/paper.ipynb :: Case analysis | 6.0 |
| 23 | docs/user-guide/limitations.md | 5.8 |
| 24 | paper/paper.ipynb :: The decision problem | 5.6 |
| 25 | paper/paper.ipynb :: Results | 5.5 |
| 26 | docs/index.md | 5.3 |
| 27 | paper/paper.ipynb :: Reproducibility and your own case | 5.0 |
| 28 | paper/paper.ipynb :: The algorithm for several facets | 5.0 |
| 29 | paper/paper.ipynb :: Discussion | 4.8 |
| 30 | paper/paper.ipynb :: Prior art, by family | 4.1 |
| 31 | paper/supporting_material.ipynb :: Appendix E. Assumptions and abstraction gaps | 3.9 |
| 32 | paper/paper.ipynb :: Search of the design space (preliminary) | 3.7 |
| 33 | paper/supporting_material.ipynb :: Appendix G. Register of prior art (part 1) | 3.5 |
| 34 | paper/supporting_material.ipynb :: Appendix B. Proofs, step for step with their scripts (part 9) | 3.2 |
| 35 | paper/supporting_material.ipynb :: Appendix D. Extended results: what the method found in the table (part 1) | 3.2 |
| 36 | paper/paper.ipynb :: Open questions | 3.1 |
| 37 | paper/supporting_material.ipynb :: Appendix C. The case's model: how the table of metrics came to be | 3.0 |
| 38 | paper/paper.ipynb :: Future work and final remark | 3.0 |
| 39 | paper/supporting_material.ipynb :: Appendix B. Proofs, step for step with their scripts (part 7) | 2.9 |
| 40 | paper/paper.ipynb :: Case construction | 2.7 |
| 41 | paper/supporting_material.ipynb :: Appendix B. Proofs, step for step with their scripts (part 5) | 2.7 |
| 42 | paper/supporting_material.ipynb :: Appendix B. Proofs, step for step with their scripts (part 10) | 2.2 |
| 43 | paper/supporting_material.ipynb :: Appendix B. Proofs, step for step with their scripts (part 8) | 2.2 |
| 44 | paper/supporting_material.ipynb :: Appendix B. Proofs, step for step with their scripts (part 4) | 2.0 |
| 45 | paper/supporting_material.ipynb :: Appendix B. Proofs, step for step with their scripts (part 3) | 1.8 |
| 46 | paper/supporting_material.ipynb :: Appendix B. Proofs, step for step with their scripts (part 1) | 1.6 |
| 47 | paper/supporting_material.ipynb :: Appendix B. Proofs, step for step with their scripts (part 6) | 1.1 |
| 48 | paper/supporting_material.ipynb :: Appendix F. Computational reproducibility | 1.0 |
| 49 | paper/supporting_material.ipynb :: Appendix B. Proofs, step for step with their scripts (part 2) | 1.0 |
| 50 | paper/supporting_material.ipynb :: Appendix G. Register of prior art (part 2) | 0.6 |
| 51 | paper/supporting_material.ipynb :: Appendix B. Proofs, step for step with their scripts (part 11) | 0.0 |
| 52 | paper/paper.ipynb :: Acknowledgments and process | 0.0 |
| 53 | docs/api-reference.md | 0.0 |
| 54 | paper/supporting_material.ipynb :: front matter | 0.0 |

## Item counts by disposition

| Disposition | Items |
|---|---|
| no change | 382 |
| amend glossary entry | 337 |
| glossary term | 304 |
| plain words | 297 |
| add to avoid | 17 |
| total | 1337 |

# The readings and dispositions

## Unit 1: docs/api.md

Density 12.0 terms of art per 100 words (22/183); staged text `docs_api.md.txt`.


### List 1. Terms unresolved from the unit and the Glossary

- "Fitted attributes for every number of terms include `exponents_`, `facet_`, `coefficients_`, `facet_share_`, `objective_` (what the solver minimized) and `mean_slack_` (the mean slack, to compare fits across numbers of terms)." Terms: facet_share_, mean_slack_. Slack of what is never said and the gloss repeats the name; no Glossary entry for either. Also "attributes" here (fitted attributes) clashes with the Glossary's "attributes" (evaluation outputs). **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it). **To the driver** (the reader reports a clash that touches a term's meaning).
- "`tension_report`, a function: contending set, elasticities and tension directions." Term: tension directions. Not in the Glossary or the unit. **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it).
- "`hyperbolic_trade_space.solvers`: the multi-term solver, the `Termination` record and the certificate functions, with `min_curvature` for a soft fit ([Reading termination](user-guide/termination.md))." Terms: certificate functions, min_curvature, soft fit. Certificate of what is undefined; "soft fit" is not a Glossary entry. **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it). **Routed to P6** (not edited here).
- "`hyperbolic_trade_space.gaps`: `knn_gap_scores`, `find_holes`, `frontier_targets`, `orient_by_pca` ([chart](user-guide/chart.md))." Terms: frontier_targets, orient_by_pca, "gap scores". What each does is not said. **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it).
- "`make_frontier_data`, a function: seeded synthetic data with a planted frontier." Term: planted frontier (which of the three frontier objects is planted). **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it).


### List 2. Where a Glossary term would say it shorter or more exactly

- "`HyperbolicTradeSpace`, a transformer: fits the surface and gives the chart of position and log V." Glossary: energy differential (log V; also level offset); position along the frontier; fitted reference surface (for "the surface"). **Disposition: glossary term** (use the Glossary term the reader names).
- "`frontier_in_original_units`, a function: the fitted surface as a monomial in raw attributes." Glossary: fitted reference surface or supporting envelope (which "surface" is meant); "raw attributes" is the Glossary's attributes. **Disposition: glossary term** (use the Glossary term the reader names).
- "`LogAffinePreconditioner`, a transformer: attributes to larger-is-better metrics, invertible." Glossary: conditioning; chart (reversible transformation). **Disposition: glossary term** (use the Glossary term the reader names).
- "`select_temperature`, a function: chooses the temperature by a target fraction above V = 1." Glossary: fit temperature; fitted reference surface (V = 1 is its level); invariant value (V). **Disposition: glossary term** (use the Glossary term the reader names).
- "`hyperbolic_trade_space.gaps`: `knn_gap_scores`, `find_holes`, `frontier_targets`, `orient_by_pca`" Glossary: white space (holes); novelty (gap scores). **Disposition: glossary term** (use the Glossary term the reader names).
- "the `Termination` record" in the solvers bullet. Glossary: termination status. **Disposition: glossary term** (use the Glossary term the reader names).
- "with `min_curvature` for a soft fit" Glossary: fit temperature (finite); conditioning of the exponents (curvature). **Disposition: glossary term** (use the Glossary term the reader names). **Routed to P6** (not edited here).
- "`TradeSpaceRegressor`, a regressor: metrics, coordinates and novelty from configuration." Glossary: log-metrics / position along the frontier for "coordinates". **Disposition: glossary term** (use the Glossary term the reader names).
- "`tension_report`, a function: contending set, elasticities and tension directions." Glossary: elasticity; participation threshold applies to what it reports. **Disposition: glossary term** (use the Glossary term the reader names).


### List 3a. Terms of art that plain words would serve

- "invertible" (in the LogAffinePreconditioner bullet): plain words "can be undone"; Glossary says chart is "reversible". **Disposition: plain words** (replace with the plain words the reader names).
- "parameters stored verbatim": plain words "stored exactly as given". **Disposition: plain words** (replace with the plain words the reader names).
- "a planted frontier": plain words "a known frontier built into the data". **Disposition: plain words** (replace with the plain words the reader names).
- "seeded synthetic data": plain words "simulated data with a fixed random seed". **Disposition: plain words** (replace with the plain words the reader names).


### List 3b. Sentences with three or more terms of art together

- "Fitted attributes for every number of terms include `exponents_`, `facet_`, `coefficients_`, `facet_share_`, `objective_` (what the solver minimized) and `mean_slack_` (the mean slack, to compare fits across numbers of terms)." Exponents, facet, coefficients, facet share, objective, slack, number of terms arrive together. **Disposition: no change** (a definition, statement or proof step where the terms are the content; the unresolved ones are items in List 1 and the shorter ones items in Lists 2 and 3a).
- "`hyperbolic_trade_space.solvers`: the multi-term solver, the `Termination` record and the certificate functions, with `min_curvature` for a soft fit ([Reading termination](user-guide/termination.md))." Multi-term solver, termination, certificate, curvature, soft fit. **Disposition: no change** (a definition, statement or proof step where the terms are the content; the unresolved ones are items in List 1 and the shorter ones items in Lists 2 and 3a). **Routed to P6** (not edited here).
- "`tension_report`, a function: contending set, elasticities and tension directions." Contending set, elasticity, tension. **Disposition: no change** (a definition, statement or proof step where the terms are the content; the unresolved ones are items in List 1 and the shorter ones items in Lists 2 and 3a).
- "`HyperbolicTradeSpace`, a transformer: fits the surface and gives the chart of position and log V." Surface, chart, position, log V. **Disposition: no change** (a definition, statement or proof step where the terms are the content; the unresolved ones are items in List 1 and the shorter ones items in Lists 2 and 3a).
- "`select_temperature`, a function: chooses the temperature by a target fraction above V = 1." Temperature, V = 1, fraction above. **Disposition: no change** (a definition, statement or proof step where the terms are the content; the unresolved ones are items in List 1 and the shorter ones items in Lists 2 and 3a).


## Unit 2: paper/supporting_material.ipynb :: Appendix A. Notation and terms

Density 10.7 terms of art per 100 words (147/1372); staged text `supp_appendix-a-notation-and-terms.txt`.


### List 1. Terms unresolved from the unit and the Glossary

- "the Helmert log-ratio coordinates of the chart" -- Helmert: neither the unit nor the Glossary defines it (Glossary "chart" says only reversible). **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it).
- "the potential evaluated at the design, a path-independent difference" -- potential: not defined; the Glossary gives the energy differential as the log of the invariant value, so which potential is unclear. **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it).
- "the weighted geometric mean of the metrics" with symbol "$V(m) = \prod_j m_j^{w_j}$" -- w_j (w without k) is not tied to the exponent vector w_k; which weights are meant is not stated. **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it).
- "the softness of the weights softmax_k(kappa score) over the K terms" -- score: the quantity being scored is never defined. **Disposition: no change** (standard vocabulary at the reader level the paper assumes (Boyd and Vandenberghe; scikit-learn)).
- "the participants at the working temperature; a statement about the whole system" -- working temperature, participating set: the Glossary mentions "working-temperature exponent" but defines neither. **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it).
- "the set of nondominated points of the attainable set" / "a sample drawn from the attainable set" -- attainable set: used throughout, defined nowhere in the unit or Glossary. **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it).
- "gamma divided by twice the largest row norm" -- row norm: of which matrix or which rows is not stated. **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it).
- "the label of the termination record" / "a statement about the choice among restarts" -- termination record, restarts: not defined. **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it).
- "the older use of the phrase for signomial programs" -- signomial programs: not defined, not standard at this level. **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it).
- "the minimum over rows of the best score minus the second-best" -- score (per row, per term): undefined. **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it).
- "an exponent below EPS_ZERO_EXPONENT" -- EPS_ZERO_EXPONENT: a code constant whose value is not given here (Glossary gives 1e-12 for "numerically zero", and says "at or below", not "below"). **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it).
- "zero is tolerated in data and masked in the fit" -- masked: not defined. **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it).
- "the entropic softness of the log-mean-exp" -- log-mean-exp: no Glossary entry; the reader must know it from elsewhere. **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it).
- Every "Defined in" cell (for example "A4", "L9", "G-1", "I6", "R2", "F12") -- these codes point to places the reader does not have; unresolvable from the unit. **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it).
- "compiled from `glossary.yaml` and never typed" -- glossary.yaml: the reader has the Glossary text but not this file's relation to it (minor). **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it).


### List 2. Where a Glossary term would say it shorter or more exactly

- "a product of powers of the metrics" (term) -- monomial: the Glossary says "One monomial of the posynomial". **Disposition: glossary term** (use the Glossary term the reader names).
- "the participants at the working temperature; a statement about the whole system" (contending set, Not) -- participation threshold / contending set: Glossary term would name the exponents above the threshold directly. **Disposition: glossary term** (use the Glossary term the reader names).
- "the Helmert log-ratio coordinates of the chart" (position along the frontier) -- chart / position along the frontier: Glossary defines this as "the other d - 1 chart coordinates". **Disposition: glossary term** (use the Glossary term the reader names).
- "the number of monomials of the posynomial frontier" (number of terms) -- fitted reference surface: "frontier" is here used undefined though the table says it is not a defined object. **Disposition: glossary term** (use the Glossary term the reader names).
- "a hole in the distribution of Z" (white space) -- Glossary says "a hole in the chart coordinates"; position along the frontier names Z. **Disposition: glossary term** (use the Glossary term the reader names).
- "the potential evaluated at the design, a path-independent difference" (energy differential) -- Glossary: "the log of the invariant value, relative to the fitted reference surface". **Disposition: glossary term** (use the Glossary term the reader names).
- "or a weight of a facet (that is a coefficient of the fit)" (share, Not) -- exponent vector: the Glossary term for a facet's weights. **Disposition: glossary term** (use the Glossary term the reader names).
- "the support of the exponent vector at infinite temperature" (contending set) -- supporting envelope: infinite temperature is the exact maximum fit the Glossary names. **Disposition: glossary term** (use the Glossary term the reader names).
- "the single-metric scaling that carries the design to V = 1" (improvement factor) -- Glossary says "the factor on one metric alone", shorter. **Disposition: glossary term** (use the Glossary term the reader names).
- "the set of share positions where one facet attains the maximum in log V" (region) -- assignment: the dominant term. **Disposition: glossary term** (use the Glossary term the reader names).


### List 3a. Terms of art that plain words would serve

- "the barycentric image of the shares of three metrics" -- plain words: triangle coordinates. **Disposition: plain words** (replace with the plain words the reader names).
- "a path-independent difference" -- plain words: a difference that depends only on the endpoints. **Disposition: plain words** (replace with the plain words the reader names).
- "the entropic softness of the log-mean-exp" -- plain words: how soft the maximum is. **Disposition: plain words** (replace with the plain words the reader names).
- "a point of the positive orthant" -- plain words: a list of positive numbers (orthant is standard at this level, so minor). **Disposition: plain words** (replace with the plain words the reader names).
- "the support of the exponent vector" -- plain words: its nonzero entries. **Disposition: plain words** (replace with the plain words the reader names).
- "the derivative of one log-metric with respect to another along the facet; a ratio of exponents" -- plain words: the trade rate between two metrics. **Disposition: plain words** (replace with the plain words the reader names).
- "the older use of the phrase for signomial programs" -- plain words: an older, different meaning of the phrase. **Disposition: plain words** (replace with the plain words the reader names). **To the driver** (the reader reports a clash that touches a term's meaning).


### List 3b. Sentences with three or more terms of art together

- "a function of the class closed under sums, products, positive powers and maxima that contains the posynomials; a class of functions" (generalized posynomial) **Disposition: add to avoid** (the phrase is withdrawn by WP10 Amendment 4 (R-33, R-34, R-37)).
- "minimize a generalized posynomial subject to generalized-posynomial constraints at most one and monomial constraints equal to one, over positive variables; the logarithmic change of variables makes it a convex program, and added variables turn it into a geometric program" (generalized geometric program) **Disposition: add to avoid** (the phrase is withdrawn by WP10 Amendment 4 (R-33, R-34, R-37)).
- "a function class, or the unsupervised several-facet fit as one program (not convex in the terms); the older use of the phrase for signomial programs; a design problem that uses the fitted model is one, and so is the fit with its weights given" (generalized geometric program, Not) **Disposition: no change** (a definition, statement or proof step where the terms are the content; the unresolved ones are items in List 1 and the shorter ones items in Lists 2 and 3a).
- "the barycentric image of the shares of three metrics (x = right + top / 2, y = sqrt(3) / 2 * top); a facet's exponent vector sums to one, so it is a point of the triangle, where that facet's V is largest at a fixed total" (ternary plot) **Disposition: no change** (a definition, statement or proof step where the terms are the content; the unresolved ones are items in List 1 and the shorter ones items in Lists 2 and 3a).
- "the smallest eigenvalue of the restricted Hessian of the objective on the simplex tangent space" (conditioning of the exponents) **Disposition: no change** (a definition, statement or proof step where the terms are the content; the unresolved ones are items in List 1 and the shorter ones items in Lists 2 and 3a).
- "the level set V = 1 of the fitted invariant, where the posynomial sum equals one; it models the data (the evaluated designs)" (fitted reference surface) **Disposition: no change** (a definition, statement or proof step where the terms are the content; the unresolved ones are items in List 1 and the shorter ones items in Lists 2 and 3a).
- "the Pareto boundary, or a bound that no design exceeds; the table and the reading drawn from it are views of the data, not what is modelled" (fitted reference surface, Not) **Disposition: no change** (a definition, statement or proof step where the terms are the content; the unresolved ones are items in List 1 and the shorter ones items in Lists 2 and 3a).
- "the several-facet fit as one program, which is not convex in the terms (L16); with the weights given, the fit of all terms is a generalized geometric program" (geometric program, Not) **Disposition: no change** (a definition, statement or proof step where the terms are the content; the unresolved ones are items in List 1 and the shorter ones items in Lists 2 and 3a).
- "the support of the exponent vector at infinite temperature" (contending set) **Disposition: no change** (a definition, statement or proof step where the terms are the content; the unresolved ones are items in List 1 and the shorter ones items in Lists 2 and 3a).
- "the softness of the weights softmax_k(kappa score) over the K terms" (term temperature) **Disposition: no change** (a definition, statement or proof step where the terms are the content; the unresolved ones are items in List 1 and the shorter ones items in Lists 2 and 3a).


## Unit 3: docs/further-reading.md

Density 10.2 terms of art per 100 words (18/177); staged text `docs_further-reading.md.txt`.


### List 1. Terms unresolved from the unit and the Glossary

- "Fitting softmax-affine functions to data so they remain compatible with geometric programming [@hoburg2016data] is the source of the multi-term fit." Term: softmax-affine. No definition in the unit; the Glossary has only "support weights" (softmax weights) and not this class. **Disposition: no change** (standard vocabulary at the reader level the paper assumes (Boyd and Vandenberghe; scikit-learn)).
- "Kernel PCA [@schoelkopf1998nonlinear]: the kin of the documented kernel direction, which is not built." Term: kernel direction. Not defined in the unit or the Glossary; "documented" points to a page the reader does not have. **Disposition: no change** (standard vocabulary at the reader level the paper assumes (Boyd and Vandenberghe; scikit-learn)).
- "Isometric log-ratio transformations for compositional data [@egozcue2003isometric] and principal component analysis of compositional data [@aitchison1983principal]: the neighbours of the chart." Terms: isometric log-ratio, compositional data. Neither is in the Glossary or explained here; only "chart" is defined. **Disposition: no change** (standard vocabulary at the reader level the paper assumes (Boyd and Vandenberghe; scikit-learn)).
- "HoroPCA [@chami2021horopca]: principal component analysis in hyperbolic space, which this package is not." Term: hyperbolic space. Not explained; reader cannot tell what is hyperbolic about the other work or in what sense this package is not. **Disposition: no change** (standard vocabulary at the reader level the paper assumes (Boyd and Vandenberghe; scikit-learn)).
- "Data envelopment analysis [@charnes1978measuring]: a frontier estimator from efficiency analysis, the nearest neighbour outside engineering design." Term: frontier. The Glossary says it names one of three objects and the pages name which; here it is not named. **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it).


### List 2. Where a Glossary term would say it shorter or more exactly

- "Fitting convex piecewise-linear functions by alternating partition and refit [@magnani2009convex]: the second source of the multi-term fit." Glossary: term / number of terms (the Glossary says "several-term fit"; "multi-term fit" is a variant name). **Disposition: no change** (the sentence reports a source in its own words (exempt by the note)).
- "A tutorial on geometric programming [@boyd2007tutorial]: posynomials and generalized posynomials, the family the multi-term fit stays inside." Glossary: generalized posynomial (the invariant V_K belongs to this class), generalized geometric program. **Disposition: no change** (the sentence reports a source in its own words (exempt by the note)).
- "Fitting softmax-affine functions to data so they remain compatible with geometric programming [@hoburg2016data] is the source of the multi-term fit." Glossary: generalized geometric program (the class the fit stays compatible with). **Disposition: no change** (the sentence reports a source in its own words (exempt by the note)).
- "Data envelopment analysis [@charnes1978measuring]: a frontier estimator from efficiency analysis, the nearest neighbour outside engineering design." Glossary: Pareto boundary / supporting envelope (whichever is meant). **Disposition: no change** (the sentence reports a source in its own words (exempt by the note)).


### List 3a. Terms of art that plain words would serve

- "the kin of the documented kernel direction" : "kin" -> relative / close relative. **Disposition: no change** (the sentence reports a source in its own words (exempt by the note)).
- "the neighbours of the chart" and "the nearest neighbour outside engineering design": "neighbours" -> related methods. **Disposition: no change** (the sentence reports a source in its own words (exempt by the note)).
- "the second source of the multi-term fit": "multi-term fit" -> fit with several terms (and be consistent with the Glossary). **Disposition: no change** (the sentence reports a source in its own words (exempt by the note)).


### List 3b. Sentences with three or more terms of art together

- "Fitting softmax-affine functions to data so they remain compatible with geometric programming [@hoburg2016data] is the source of the multi-term fit." Softmax-affine, geometric programming, multi-term fit. **Disposition: no change** (the sentence reports a source in its own words (exempt by the note)).
- "Isometric log-ratio transformations for compositional data [@egozcue2003isometric] and principal component analysis of compositional data [@aitchison1983principal]: the neighbours of the chart." Isometric log-ratio, compositional data, principal component analysis, chart. **Disposition: no change** (the sentence reports a source in its own words (exempt by the note)).
- "Kernel PCA [@schoelkopf1998nonlinear]: the kin of the documented kernel direction, which is not built." Kernel PCA, kernel direction, documented extension. **Disposition: no change** (the sentence reports a source in its own words (exempt by the note)).


## Unit 4: paper/paper.ipynb :: Definitions

Density 9.9 terms of art per 100 words (37/375); staged text `paper_definitions.txt`.


### List 1. Terms unresolved from the unit and the Glossary

- "The reach $\beta_k$ is the support value of the data in direction $w_k$." Terms: reach, support value. Neither is in the Glossary; "reach" is coined here and "support value" is only recoverable from convex analysis if the reader guesses support function. **Disposition: no change** (standard vocabulary at the reader level the paper assumes (Boyd and Vandenberghe; scikit-learn)). **Routed to P1** (not edited here).
- "The facet share is the fraction of near-frontier designs that facet $k$ dominates; it shows which facets carry most of the frontier and depends on the band." Terms: facet share. The Glossary "share" is a position in the triangle, a different meaning; "facet share" has no entry. **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it). **To the driver** (the reader reports a clash that touches a term's meaning). **Routed to P1** (not edited here).
- "Working-temperature exponents grade the members, and a member can carry a small one." Terms: working-temperature exponents, grade. "Working temperature" is never defined in the unit (only fit temperature and term temperature); the Glossary mentions it only inside "participation threshold". **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it). **Routed to P1** (not edited here).
- "The contending set of facet $k$ is the support (exponents above $10^{-9}$) of the exact-maximum ($\tau=\infty$) fit to the facet's rows; its size $n_k$ names it." Terms: support, exact-maximum fit. "Support" as a set of positive exponents is not defined here; the threshold 1e-9 also differs from the Glossary's "numerically zero" (1e-12) with no explanation. **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it). **Routed to P1** (not edited here).
- "The near-frontier band is $|\log V|<1/\tau$: in the soft maximum a design inside it weighs within a factor $e$ of one on the surface." Terms: near-frontier band, soft maximum. No Glossary entry for either; "weighs" is not tied to support weights. **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it). **Routed to P1** (not edited here).
- "designs of equal $V$ stand at the same level" Terms: level. Used as a noun throughout ("levels", "level relative to") with no Glossary entry beyond "level offset". **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it). **Routed to P1** (not edited here).


### List 2. Where a Glossary term would say it shorter or more exactly

- "and $\log V$, the energy differential, is a design's level relative to the reference surface $V=1$: negative inside, positive beyond." Glossary: "fitted reference surface" (and "level offset"). **Disposition: glossary term** (use the Glossary term the reader names). **Routed to P1** (not edited here).
- "The contending set of facet $k$ is the support (exponents above $10^{-9}$) of the exact-maximum ($\tau=\infty$) fit to the facet's rows; its size $n_k$ names it." Glossary: "supporting envelope" for the exact-maximum fit; "exponent vector" for the exponents; "numerically zero" for the threshold. **Disposition: glossary term** (use the Glossary term the reader names). **Routed to P1** (not edited here).
- "The reach $\beta_k$ is the support value of the data in direction $w_k$." Glossary: "supporting envelope" (a hyperplane supporting the rows from above) and "exponent vector" for the direction $w_k$. **Disposition: glossary term** (use the Glossary term the reader names). **Routed to P1** (not edited here).
- "Where several trade-offs are active at once, the model is a sum of such terms, one per facet." Glossary: "posynomial" (the sum of monomials) and "number of terms". **Disposition: glossary term** (use the Glossary term the reader names). **Routed to P1** (not edited here).
- "On facet $k$ the tangent space $\{v:w_k\cdot v=0\}$ trades contending metrics at constant $V$; the normal $w_k$ is the steepest ascent of $\log V$." Glossary: "exponent vector" for $w_k$ and "contending set" for the metrics. **Disposition: glossary term** (use the Glossary term the reader names). **Routed to P1** (not edited here).
- "$Z=Bu$, with $BB^\top=I$ and $B\mathbf 1=0$, is the position along the frontier, free of overall scale." Glossary: "frontier" is the everyday word with three referents; "position along the frontier" is right, but the unit never says which object (fitted reference surface). **Disposition: glossary term** (use the Glossary term the reader names). **Routed to P1** (not edited here).


### List 3a. Terms of art that plain words would serve

- "contending set" / "contending metrics": plain words "the metrics that matter on this facet". **Disposition: plain words** (replace with the plain words the reader names). **Routed to P1** (not edited here).
- "support (exponents above $10^{-9}$)": plain words "the metrics with positive weight". **Disposition: plain words** (replace with the plain words the reader names). **Routed to P1** (not edited here).
- "reach": plain words "how far the data extends in that direction". **Disposition: plain words** (replace with the plain words the reader names). **Routed to P1** (not edited here).
- "ascent direction" / "steepest ascent": plain words "uphill direction". **Disposition: plain words** (replace with the plain words the reader names). **Routed to P1** (not edited here).
- "near-frontier band": plain words "the designs close to the surface". **Disposition: plain words** (replace with the plain words the reader names). **Routed to P1** (not edited here).
- "grade the members": plain words "rank the members by weight". **Disposition: plain words** (replace with the plain words the reader names). **Routed to P1** (not edited here).


### List 3b. Sentences with three or more terms of art together

- "The contending set of facet $k$ is the support (exponents above $10^{-9}$) of the exact-maximum ($\tau=\infty$) fit to the facet's rows; its size $n_k$ names it." Terms together: contending set, facet, support, exponents, exact-maximum fit. **Disposition: no change** (a definition, statement or proof step where the terms are the content; the unresolved ones are items in List 1 and the shorter ones items in Lists 2 and 3a). **Routed to P1** (not edited here).
- "$V_K(m)=\big(\sum_{k=1}^{K}c_k\prod_j m_j^{\kappa w_{kj}}\big)^{1/\kappa}$ with $w_k\in\Delta$ and $c_k=e^{-\kappa\beta_k}$ is the $1/\kappa$ power of a posynomial, a sum of monomials ({prf:ref}`thm-extension`); $\Phi_K(u)=\frac1\kappa\log\sum_k e^{\kappa(w_k\cdot u-\beta_k)}$ is its logarithm." Terms together: posynomial, monomials, simplex weights, term temperature $\kappa$, offset $\beta_k$. **Disposition: no change** (a definition, statement or proof step where the terms are the content; the unresolved ones are items in List 1 and the shorter ones items in Lists 2 and 3a). **Routed to P1** (not edited here).
- "The facet share is the fraction of near-frontier designs that facet $k$ dominates; it shows which facets carry most of the frontier and depends on the band." Terms together: facet share, near-frontier designs, facet, dominates, frontier, band. **Disposition: no change** (a definition, statement or proof step where the terms are the content; the unresolved ones are items in List 1 and the shorter ones items in Lists 2 and 3a). **Routed to P1** (not edited here).
- "The near-frontier band is $|\log V|<1/\tau$: in the soft maximum a design inside it weighs within a factor $e$ of one on the surface." Terms together: near-frontier band, fit temperature, soft maximum, surface. **Disposition: no change** (a definition, statement or proof step where the terms are the content; the unresolved ones are items in List 1 and the shorter ones items in Lists 2 and 3a). **Routed to P1** (not edited here).
- "The chart separates where a design sits along the surface from its energy differential, how far it is from the surface in levels and not in Euclidean distance." Terms together: chart, surface, energy differential, levels. **Disposition: no change** (a definition, statement or proof step where the terms are the content; the unresolved ones are items in List 1 and the shorter ones items in Lists 2 and 3a). **Routed to P1** (not edited here).
- "On facet $k$ the tangent space $\{v:w_k\cdot v=0\}$ trades contending metrics at constant $V$; the normal $w_k$ is the steepest ascent of $\log V$." Terms together: facet, tangent space, contending metrics, normal, steepest ascent. **Disposition: no change** (a definition, statement or proof step where the terms are the content; the unresolved ones are items in List 1 and the shorter ones items in Lists 2 and 3a). **Routed to P1** (not edited here).


## Unit 5: paper/paper.ipynb :: Title and abstract

Density 9.5 terms of art per 100 words (20/210); staged text `paper_abstract.txt`.


### List 1. Terms unresolved from the unit and the Glossary

- "We explain tensions." Term: tensions. No definition in the unit; the Glossary uses "tension" only inside the participation threshold entry, with no entry of its own. **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it).
- "A fitted posynomial reference surface models the data underlying the table, not the Pareto boundary, and gives the data a coordinate system; the table and its reading are views." Term: the table, views. "The table" is never introduced (the Glossary mentions it only under number of designs), and "views" is not defined. **Disposition: no change** (standard vocabulary at the reader level the paper assumes (Boyd and Vandenberghe; scikit-learn)).
- "Modelling a single n-lemma fits a monomial, which transforms into a convex program and is solved directly; ..." Term: transforms into a convex program. The transformation (log chart, x = exp(y)) is not stated; the reader gets the Glossary only if they connect it to chart / geometric program. **Disposition: no change** (standard vocabulary at the reader level the paper assumes (Boyd and Vandenberghe; scikit-learn)).
- "...and the method may be generalized to any kernel that keeps that compatibility." Term: kernel. Not a Glossary entry; the sense (kernel methods for the posynomial terms) is not given. **Disposition: no change** (standard vocabulary at the reader level the paper assumes (Boyd and Vandenberghe; scikit-learn)).
- "On a cubesat model coupling power, mass and attitude control, the fit identifies the trade-offs among the metrics those subsystems set." Terms: cubesat, attitude control. Domain vocabulary, no definition or Glossary entry. **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it).


### List 2. Where a Glossary term would say it shorter or more exactly

- "A reversible chart separates a design's position along the surface from its energy differential, its level relative to the surface." Glossary: position along the frontier (and fitted reference surface); "its level relative to the surface" restates energy differential / level offset. **Disposition: glossary term** (use the Glossary term the reader names).
- "Each facet reports its contending metrics, an n-lemma (by analogy with dilemma and trilemma), with elasticities: the percentage of one metric given up per percentage gained in another." Glossary: contending set (for "contending metrics"); elasticity (the long gloss repeats the Glossary entry). **Disposition: glossary term** (use the Glossary term the reader names).
- "Modelling a single n-lemma fits a monomial, which transforms into a convex program and is solved directly; when several trade-offs are active at once the model is a posynomial, compatible with generalized geometric programming (GGP), and the method may be generalized to any kernel that keeps that compatibility." Glossary: geometric program / generalized geometric program (for "convex program ... compatible with"); number of terms (K) for "several trade-offs ... active at once". **Disposition: glossary term** (use the Glossary term the reader names).
- "On a cubesat model coupling power, mass and attitude control, the fit identifies the trade-offs among the metrics those subsystems set." Glossary: n-lemma / contending set for "trade-offs among the metrics". **Disposition: glossary term** (use the Glossary term the reader names).
- "A fitted posynomial reference surface models the data underlying the table, not the Pareto boundary, ..." Glossary: fitted reference surface (the posynomial qualifier is the Glossary's own entry wording). **Disposition: glossary term** (use the Glossary term the reader names).


### List 3a. Terms of art that plain words would serve

- "gives the data a coordinate system": plain words "a way to locate each design" (chart is the Glossary term). **Disposition: plain words** (replace with the plain words the reader names).
- "the table and its reading are views": plain words "the table and how we read it are two ways of seeing the same thing". **Disposition: plain words** (replace with the plain words the reader names).
- "energy differential": plain words "level relative to the surface" (already given in the same sentence; "level offset" is the Glossary alias). **Disposition: plain words** (replace with the plain words the reader names).
- "Our implementation mirrors the structure of PCA as an unsupervised learning method for feature engineering.": plain words "works the way PCA does, learning from the data alone to build new features". **Disposition: plain words** (replace with the plain words the reader names).
- "kernel": plain words "other function families". **Disposition: plain words** (replace with the plain words the reader names).
- "transforms into a convex program and is solved directly": plain words "becomes an easy-to-solve optimization problem". **Disposition: plain words** (replace with the plain words the reader names).


### List 3b. Sentences with three or more terms of art together

- "Modelling a single n-lemma fits a monomial, which transforms into a convex program and is solved directly; when several trade-offs are active at once the model is a posynomial, compatible with generalized geometric programming (GGP), and the method may be generalized to any kernel that keeps that compatibility." (n-lemma, monomial, convex program, posynomial, generalized geometric programming, kernel) **Disposition: plain words** (introductory page: spread the terms over more words).
- "A fitted posynomial reference surface models the data underlying the table, not the Pareto boundary, and gives the data a coordinate system; the table and its reading are views." (posynomial, reference surface, Pareto boundary, coordinate system) **Disposition: plain words** (introductory page: spread the terms over more words).
- "A reversible chart separates a design's position along the surface from its energy differential, its level relative to the surface." (chart, position along the surface, energy differential) **Disposition: plain words** (introductory page: spread the terms over more words).
- "Each facet reports its contending metrics, an n-lemma (by analogy with dilemma and trilemma), with elasticities: the percentage of one metric given up per percentage gained in another." (facet, contending metrics, n-lemma, elasticities) **Disposition: plain words** (introductory page: spread the terms over more words).
- "Our implementation mirrors the structure of PCA as an unsupervised learning method for feature engineering." (PCA, unsupervised learning, feature engineering) **Disposition: plain words** (introductory page: spread the terms over more words).


## Unit 6: docs/examples.md

Density 8.6 terms of art per 100 words (62/718); staged text `docs_examples.md.txt`.


### List 1. Terms unresolved from the unit and the Glossary

- "The tension report finds a contending set of six metrics (total mass, slew time, energy balance, control effort, pointing error, depth of discharge): a 6-lemma, found from the data with no prior choice of which metrics or how many." Term: tension report. Used as the main instrument, never defined here or in the Glossary (only a parameter name appears under participation threshold). **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it). **Routed to P6** (not edited here).
- "The mean slack falls from 0.204 at one term to 0.117 at three, and the status is `certified`." Term: mean slack. No definition and no Glossary entry; unclear what is slack in what. **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it). **Routed to P6** (not edited here).
- "The largest facet holds 78 percent of the near-frontier share and is the only one containing total mass and peak slew power; the other two are built on control effort, slew time and energy balance." Term: near-frontier share. Not defined; unclear whether it is share of designs, of support weight, or of something else (and "share" in the Glossary means a ternary position). **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it). **Routed to P6** (not edited here).
- "This block fits a planted table and draws it with lines of equal V:" Term: planted table. Not defined; make_frontier_data is not explained. **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it). **Routed to P6** (not edited here).
- "The same steps apply to any table of designs: condition, `select_temperature`, fit, then read the [tension report](user-guide/tensions.md) and the [termination record](user-guide/termination.md)." Term: select_temperature. Function never introduced; the only hint is the "tenth of the designs above V = 1" phrase earlier. **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it). **Routed to P6** (not edited here).


### List 2. Where a Glossary term would say it shorter or more exactly

- "With the temperature selected for a tenth of the designs above V = 1:" Glossary term: fit temperature. **Disposition: glossary term** (use the Glossary term the reader names). **Routed to P6** (not edited here).
- "V also depends on the total, so a marker is not where V = 1." Glossary terms: invariant value (for V) and fitted reference surface (for the level V = 1). **Disposition: glossary term** (use the Glossary term the reader names). **Routed to P6** (not edited here).
- "The same steps apply to any table of designs: condition, `select_temperature`, fit, then read the [tension report](user-guide/tensions.md) and the [termination record](user-guide/termination.md)." Glossary term: termination status (the record is not named as such). **Disposition: glossary term** (use the Glossary term the reader names). **Routed to P6** (not edited here).
- "Figure 7. The 706 feasible designs by their first two position coordinates; the ringed designs lie nearest the frontier." Glossary term: fitted reference surface (the Glossary says "frontier" must be named as one of three objects), and position along the frontier for "position coordinates". **Disposition: glossary term** (use the Glossary term the reader names). **Routed to P6** (not edited here).
- "The largest facet holds 78 percent of the near-frontier share and is the only one containing total mass and peak slew power; the other two are built on control effort, slew time and energy balance." Glossary term: fitted reference surface (for "near-frontier"); support weights if that is what the share is. **Disposition: glossary term** (use the Glossary term the reader names). **Routed to P6** (not edited here).
- "Exponents add over groups exactly: a facet's weight on a subsystem is a sum." Glossary term: exponent vector (the weights of term k on the simplex). **Disposition: glossary term** (use the Glossary term the reader names). **Routed to P6** (not edited here).


### List 3a. Terms of art that plain words would serve

- "The aggressive-gains table has 706 feasible designs. With the temperature selected..." / "Ten attributes are compared under two controller-gain regimes" : "regimes" would be served by "settings". **Disposition: plain words** (replace with the plain words the reader names). **Routed to P6** (not edited here).
- "This block fits a planted table and draws it with lines of equal V:" : "planted" would be served by "synthetic". **Disposition: plain words** (replace with the plain words the reader names). **Routed to P6** (not edited here).
- "...and can be cherry-picked; the triangle is for reading, not for measuring distance;" : "cherry-picked" would be served by "chosen to flatter the result". **Disposition: plain words** (replace with the plain words the reader names). **Routed to P6** (not edited here).
- "The tension report finds a contending set of six metrics" : "contending set" would be served by "the metrics that trade off" (Glossary term exists, but plain words suffice at first use). **Disposition: plain words** (replace with the plain words the reader names). **Routed to P6** (not edited here).


### List 3b. Sentences with three or more terms of art together

- "A numbered marker is a facet's exponent vector, where that facet's V is largest for a fixed total." (facet, exponent vector, V) **Disposition: no change** (a definition, statement or proof step where the terms are the content; the unresolved ones are items in List 1 and the shorter ones items in Lists 2 and 3a). **Routed to P6** (not edited here).
- "The mean slack falls from 0.204 at one term to 0.117 at three, and the status is `certified`." (slack, term, certified) **Disposition: no change** (a definition, statement or proof step where the terms are the content; the unresolved ones are items in List 1 and the shorter ones items in Lists 2 and 3a). **Routed to P6** (not edited here).
- "The largest facet holds 78 percent of the near-frontier share and is the only one containing total mass and peak slew power; the other two are built on control effort, slew time and energy balance." (facet, near-frontier share, plus the metric names) **Disposition: no change** (a definition, statement or proof step where the terms are the content; the unresolved ones are items in List 1 and the shorter ones items in Lists 2 and 3a). **Routed to P6** (not edited here).
- "The tension report finds a contending set of six metrics (total mass, slew time, energy balance, control effort, pointing error, depth of discharge): a 6-lemma, found from the data with no prior choice of which metrics or how many." (tension report, contending set, n-lemma) **Disposition: no change** (a definition, statement or proof step where the terms are the content; the unresolved ones are items in List 1 and the shorter ones items in Lists 2 and 3a). **Routed to P6** (not edited here).
- "A region is where one facet dominates, named by the metrics that trade there: an analysis of the fit, not a label on a design." (region, facet, analysis) **Disposition: no change** (a definition, statement or proof step where the terms are the content; the unresolved ones are items in List 1 and the shorter ones items in Lists 2 and 3a). **Routed to P6** (not edited here).


## Unit 7: paper/paper.ipynb :: Methods

Density 8.6 terms of art per 100 words (40/464); staged text `paper_methods.txt`.


### List 1. Terms unresolved from the unit and the Glossary

- "R1: the balanced point lies in the relative interior of a facet of the supporting envelope with positive normal; otherwise exponents are a subgradient choice, not an identified trade-off." Term: balanced point. Not defined in the unit or the Glossary. **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it).
- "$V_K$ is a generalized posynomial, the term maximum at the default $\kappa=\infty$ [@boyd2007tutorial]." Term: kappa. The symbol is never defined here; the Glossary has "term temperature" but does not tie it to kappa. **Disposition: add to avoid** (the phrase is withdrawn by WP10 Amendment 4 (R-33, R-34, R-37)).
- "With scores $s_i=w\cdot u_i$," Term: u (and w). u is never named as the log-metrics; the Glossary entry is not linked to the symbol. **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it).
- "A negative $\alpha_j$ marks smaller-is-better; the shift $s_j$ places the origin; a scaler equalizes log-spread so one $\tau$ serves every metric." Terms: s_j, log-spread. The symbol s is already the score s_i and the facet score s_ik, so s_j is a clash. "Log-spread" is not defined. **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it). **To the driver** (the reader reports a clash that touches a term's meaning).
- "(ii) *Sharp weights by default, soft on request:* facets are fitted at $\kappa=\infty$ with kinks on the ridges." Terms: ridges, kinks. Not defined; "ridges" is not a Glossary term. **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it).
- "(vi) *A log-convex envelope:* $\Phi_K$ is convex in $u$, which keeps later optimization convex; no $K$ represents non-log-convex structure." Term: Phi_K. Never defined in the unit or the Glossary. **Disposition: no change** (standard vocabulary at the reader level the paper assumes (Boyd and Vandenberghe; scikit-learn)).
- "(iv) *Small $K$:* the case needs three facets; a small $K$ keeps each contending set readable." Term: "the case". Which case is meant is not stated in the unit. **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it).
- "R2: the assignment margin $\gamma=\min_i[s_{i,k(i)}-\max_{k\neq k(i)}s_{ik}]$ is positive, with $s_{ik}=w_k\cdot u_i-\beta_k$ the energy differential of design $i$ against facet $k$." Term: k(i). The Glossary defines "assignment" but not this index notation. **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it).


### List 2. Where a Glossary term would say it shorter or more exactly

- "At $K=1$ the frontier is the unit level set of $V$." Term: fitted reference surface. "Frontier" is the Glossary's everyday word for three objects; this sentence means the level V = 1 of the fit. **Disposition: glossary term** (use the Glossary term the reader names).
- "$\tau$ puts a target fraction of designs above $V=1$: 10 percent here, a convention that keeps one extreme design from setting the surface" Terms: fit temperature (for tau), fitted reference surface (for "the surface"). Neither is named. **Disposition: glossary term** (use the Glossary term the reader names).
- "Several facets alternate weights with one program for all terms ({prf:ref}`thm-soft`)." Term: term temperature. "Weights" here could be exponent vectors, support weights or the soft weights over terms; the Glossary separates them. **Disposition: glossary term** (use the Glossary term the reader names).
- "The fit asks for the positive combination of log-metrics along which the data have the smallest upper extent, under an entropic soft maximum." Term: exponent vector (w on the simplex). Also "fit temperature" for the softness. **Disposition: glossary term** (use the Glossary term the reader names). **Routed to P1** (not edited here).
- "Zeros are tolerated in data and masked in the fit, negative values are rejected, and the pull-back to attribute units is exact ({prf:ref}`thm-pullback`)." Term: chart (reversible, "nothing is lost either way"). "Pull-back" is not used in the Glossary. **Disposition: glossary term** (use the Glossary term the reader names).
- "(ii) ... fitting at a finite $\kappa$ is the soft fit of {numref}`Section %s <sect-results>`, which does change them." Term: term temperature. "Soft fit" and "sharp weights" are the Glossary's finite and infinite term temperature. **Disposition: glossary term** (use the Glossary term the reader names). **Routed to P1** (not edited here).


### List 3a. Terms of art that plain words would serve

- "kinks on the ridges": "corners where facets meet". **Disposition: plain words** (replace with the plain words the reader names).
- "entropic soft maximum": "smooth maximum". The paper's own definition (log-mean-exp) follows at once. **Disposition: plain words** (replace with the plain words the reader names). **Routed to P1** (not edited here).
- "pull-back to attribute units": "mapping back to attribute units". **Disposition: plain words** (replace with the plain words the reader names).
- "equalizes log-spread": "gives every metric the same spread of logs". **Disposition: plain words** (replace with the plain words the reader names).
- "participates" (exponent above the participation threshold): "counts as active". **Disposition: plain words** (replace with the plain words the reader names).
- "Several facets alternate weights with one program for all terms": "several facets are fitted by alternating between the weights and one program". **Disposition: plain words** (replace with the plain words the reader names).
- "a subgradient choice": "an arbitrary pick among valid slopes". **Disposition: plain words** (replace with the plain words the reader names).


### List 3b. Sentences with three or more terms of art together

- "R1: the balanced point lies in the relative interior of a facet of the supporting envelope with positive normal; otherwise exponents are a subgradient choice, not an identified trade-off." Terms together: balanced point, relative interior, facet, supporting envelope, normal, exponents, subgradient, trade-off. **Disposition: no change** (a definition, statement or proof step where the terms are the content; the unresolved ones are items in List 1 and the shorter ones items in Lists 2 and 3a).
- "At finite $\tau$ one facet is a geometric program, convex after the change of variables $x=e^{w}$ ({ref}`Appendix B, L4.14 to L4.24 <appendix-b>`); $V_K$ is a generalized posynomial, the term maximum at the default $\kappa=\infty$ [@boyd2007tutorial]." Terms together: finite tau, facet, geometric program, change of variables, generalized posynomial, term maximum, kappa. **Disposition: add to avoid** (the phrase is withdrawn by WP10 Amendment 4 (R-33, R-34, R-37)).
- "(ii) *Sharp weights by default, soft on request:* facets are fitted at $\kappa=\infty$ with kinks on the ridges. For given facets a finite $\kappa$ moves the score by at most $(\log K)/\kappa$ ({prf:ref}`thm-extension`) and, by construction, leaves the facets unchanged;" Terms together: sharp weights, soft, facets, kappa, kinks, ridges, score. **Disposition: no change** (a definition, statement or proof step where the terms are the content; the unresolved ones are items in List 1 and the shorter ones items in Lists 2 and 3a).
- "R2: the assignment margin $\gamma=\min_i[s_{i,k(i)}-\max_{k\neq k(i)}s_{ik}]$ is positive, with $s_{ik}=w_k\cdot u_i-\beta_k$ the energy differential of design $i$ against facet $k$." Terms together: assignment margin, energy differential, facet, plus the symbols s, k(i), w, u, beta. **Disposition: no change** (a definition, statement or proof step where the terms are the content; the unresolved ones are items in List 1 and the shorter ones items in Lists 2 and 3a).
- "The theory asks conditioning to be log-affine per metric, $\log m_j=\alpha_j\log(a_j+s_j)+b_j$ with $\alpha_j\neq0$." Terms together: conditioning, log-affine, metric, alpha, a, s, b. **Disposition: no change** (a definition, statement or proof step where the terms are the content; the unresolved ones are items in List 1 and the shorter ones items in Lists 2 and 3a).


## Unit 8: docs/user-guide/prediction.md

Density 8.4 terms of art per 100 words (18/214); staged text `docs_user-guide_prediction.md.txt`.


### List 1. Terms unresolved from the unit and the Glossary

- "`predict_coordinates(X_config)`: the pair `(Z, log_v)`." Terms: Z, log_v. Neither symbol is defined here or in the Glossary; Z is presumably the position along the frontier and log_v the energy differential, but the unit never says. **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it).
- "`predict_novelty(X_config)`: V - 1, positive where the design is predicted beyond the surface." Terms: V, "the surface". V is never defined in the unit; the Glossary gives "invariant value" but no symbol V, and "the surface" is one of three frontier objects without being named. **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it).
- "A configuration predicted beyond V = 1 is a proposal for the next evaluation to run, to be checked, not a result." Term: V = 1. The level is unexplained in the unit; the Glossary reaches it only through "fitted reference surface" and "improvement factor". **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it).
- "The regressor declares `positive_only` targets and raises `ValueError` on negative `y`." Term: `positive_only`. Not a standard scikit-learn tag name and not in the Glossary. **Disposition: no change** (standard vocabulary at the reader level the paper assumes (Boyd and Vandenberghe; scikit-learn)).
- "`predict_std(X_config)`: the regressor's `return_std` propagated by the delta method; raises `AttributeError` if the regressor does not provide it." Term: `return_std`. It is a convention of some scikit-learn regressors, not of RandomForestRegressor, and the unit does not say which regressors provide it. **Disposition: no change** (standard vocabulary at the reader level the paper assumes (Boyd and Vandenberghe; scikit-learn)).


### List 2. Where a Glossary term would say it shorter or more exactly

- "`predict_novelty(X_config)`: V - 1, positive where the design is predicted beyond the surface." Term: novelty (and fitted reference surface). The sentence defines novelty in other words and leaves "the surface" unnamed. **Disposition: glossary term** (use the Glossary term the reader names).
- "`predict_coordinates(X_config)`: the pair `(Z, log_v)`." Terms: position along the frontier, energy differential. These would name the two parts exactly. **Disposition: glossary term** (use the Glossary term the reader names).
- "A configuration predicted beyond V = 1 is a proposal for the next evaluation to run, to be checked, not a result." Term: fitted reference surface (level V = 1); "beyond V = 1" is "beyond the fitted reference surface". **Disposition: glossary term** (use the Glossary term the reader names).
- "`trade_space` may be a `Pipeline` ending in a `HyperbolicTradeSpace`, such as a preconditioner followed by the estimator." Term: conditioning (LogAffinePreconditioner). "Preconditioner" names the analyst's conditioning step without the Glossary name. **Disposition: glossary term** (use the Glossary term the reader names).
- "where would a configuration without measurements fall?" Term: position along the frontier. This is the question the page answers. **Disposition: glossary term** (use the Glossary term the reader names).
- "`predict(X_config)`: metrics, through the inverse chart." Term: chart. Fine as written; no change needed beyond confirming "inverse chart" matches the Glossary. **Disposition: glossary term** (use the Glossary term the reader names).


### List 3a. Terms of art that plain words would serve

- "`predict_std(X_config)`: the regressor's `return_std` propagated by the delta method". Term: delta method. Plain words: "carried through the chart by a first-order approximation". **Disposition: plain words** (replace with the plain words the reader names).
- "so the surrogate's error carries into the novelty prediction." Term: surrogate. Plain words: "the regressor's error" (the page already calls it the regressor). **Disposition: plain words** (replace with the plain words the reader names).
- "A predicted position inherits the surrogate's error and extrapolation risk". Terms: surrogate, extrapolation risk. Plain words: "the regressor's error and the risk of predicting outside the training configurations". **Disposition: plain words** (replace with the plain words the reader names).
- "The regressor declares `positive_only` targets and raises `ValueError` on negative `y`." Term: declares `positive_only` targets. Plain words: "accepts only positive y". **Disposition: plain words** (replace with the plain words the reader names).
- "Coordinates, not metrics, are the regression target". Term: regression target. Plain words: "what the regressor is trained to predict". **Disposition: plain words** (replace with the plain words the reader names).


### List 3b. Sentences with three or more terms of art together

- "`fit(X_config, Y_metrics)` fits a clone of `trade_space` on the metrics, then fits a clone of `regressor` from configuration to the chart coordinates." Terms: clone, trade_space, metrics, configuration, chart coordinates. **Disposition: no change** (a definition, statement or proof step where the terms are the content; the unresolved ones are items in List 1 and the shorter ones items in Lists 2 and 3a).
- "`trade_space` may be a `Pipeline` ending in a `HyperbolicTradeSpace`, such as a preconditioner followed by the estimator." Terms: Pipeline, HyperbolicTradeSpace, preconditioner, estimator. **Disposition: no change** (a definition, statement or proof step where the terms are the content; the unresolved ones are items in List 1 and the shorter ones items in Lists 2 and 3a).
- "Coordinates, not metrics, are the regression target, so the surrogate's error carries into the novelty prediction." Terms: coordinates, metrics, surrogate, novelty. **Disposition: no change** (a definition, statement or proof step where the terms are the content; the unresolved ones are items in List 1 and the shorter ones items in Lists 2 and 3a).
- "A predicted position inherits the surrogate's error and extrapolation risk, and is conditional on the fitted trade space." Terms: predicted position, surrogate, extrapolation risk, fitted trade space. **Disposition: no change** (a definition, statement or proof step where the terms are the content; the unresolved ones are items in List 1 and the shorter ones items in Lists 2 and 3a).
- "`predict_std(X_config)`: the regressor's `return_std` propagated by the delta method; raises `AttributeError` if the regressor does not provide it." Terms: return_std, delta method, AttributeError. **Disposition: no change** (a definition, statement or proof step where the terms are the content; the unresolved ones are items in List 1 and the shorter ones items in Lists 2 and 3a).


## Unit 9: docs/user-guide/tensions.md

Density 8.1 terms of art per 100 words (42/520); staged text `docs_user-guide_tensions.md.txt`.


### List 1. Terms unresolved from the unit and the Glossary

- "`tension_report(estimator, X)` returns a frozen `TensionReport` that says which metrics contend and how they trade." Terms: frozen (TensionReport); "contend" is glossed only via the contending set, never in the unit. Why: "frozen" is unexplained (immutable dataclass?); contend is used before any definition. **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it).
- "`contending_set` holds the metrics with positive exponent in the exact-maximum fit (tau = infinity, exponents above 1e-9)." Terms: tau, exact-maximum fit. Why: the symbol tau appears with no definition in the unit; the Glossary has "fit temperature" but not the name tau. **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it).
- "`min_exponent` must be 0 for this reading, because a positive floor masks the sparsity; the report warns when the estimator was fitted with a floor." Terms: min_exponent, floor, sparsity. Why: no Glossary entry; the parameter is never introduced here. **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it).
- "`association` is the Pearson or Spearman correlation of the log-metrics: negative is traded, positive is aligned." Term: aligned (and "traded"). Why: used as technical labels without definition. **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it).
- "Near the surface the weighted sum of log-metrics is almost constant, so a binding constraint produces negative association even where no designer traded the metrics (`closure_note` says so)." Terms: binding constraint, closure_note. Why: the weights and the closure effect are not defined; closure_note is not introduced. **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it).
- "`tension_directions`: the principal directions of the near-frontier chart coordinates." Terms: near-frontier, band. Why: near-frontier is defined only by the band sentence earlier; "band" has no Glossary entry. **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it).
- "They equal `orient_by_pca` on the same rows." Term: orient_by_pca. Why: function never introduced, no Glossary entry. **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it).
- "At K > 1 the function returns a list of K reports, one per facet, each on the rows that facet dominates." Term: K. Why: K is not defined in the unit (Glossary has "number of terms" only). **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it).
- "A facet with fewer than `min_near_frontier` (default 10) near-frontier rows raises `ValueError`; widen `band` or lower `min_near_frontier`." Term: min_near_frontier. Why: parameter not defined elsewhere. **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it).
- Figure caption: "negative association (orange) marks metrics that are traded, and the outlined cells are the contending set." Term: association (heatmap sense). Why: used before its section defines it. **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it).


### List 2. Where a Glossary term would say it shorter or more exactly

- "`contending_set` holds the metrics with positive exponent in the exact-maximum fit (tau = infinity, exponents above 1e-9)." Glossary: supporting envelope (fit at infinite temperature); fit temperature. Says "exact-maximum fit (tau = infinity)" in longer words. **Disposition: glossary term** (use the Glossary term the reader names).
- "The report solves the tau = infinity program itself, independent of the fitted temperature." Glossary: supporting envelope / fit temperature. **Disposition: glossary term** (use the Glossary term the reader names).
- "a facet of the achievable region on which exactly n metrics contend." Glossary: n-lemma ("how many of the d metrics contend on a facet"). Also "achievable region" vs the Glossary's attainable set / Pareto boundary. **Disposition: glossary term** (use the Glossary term the reader names).
- "At the working temperature the exponents are smoothed, so a small one means weak participation, not membership." Glossary: participation threshold; exponent vector; fit temperature (working temperature is an unlisted synonym). **Disposition: glossary term** (use the Glossary term the reader names).
- "an exponent at or below 1e-12 is numerically zero." Already the Glossary term "numerically zero"; consistent, but the 1e-9 versus 1e-12 versus 1e-3 cutoffs sit across entries (contending, numerically zero, participation threshold). **Disposition: glossary term** (use the Glossary term the reader names).
- "`elasticities[j, k]` is the elasticity along the surface: the percentage change of metric j per percentage change of metric k". Glossary: elasticity. **Disposition: glossary term** (use the Glossary term the reader names).
- "For designs with absolute log V below `band` ... " Glossary: energy differential / level offset (log of the invariant value relative to V = 1); "absolute log V" would be "absolute energy differential". **Disposition: glossary term** (use the Glossary term the reader names).
- "Near the surface the weighted sum of log-metrics is almost constant" Glossary: invariant value (weighted geometric mean), so "log V near 0". **Disposition: glossary term** (use the Glossary term the reader names).
- "the principal directions of the near-frontier chart coordinates." Glossary: position along the frontier / chart. **Disposition: glossary term** (use the Glossary term the reader names).
- "depends on the band, and is a statement about the sampled table" Glossary: frontier (fitted reference surface vs Pareto boundary); "the surface" and "frontier" are used without naming which. **Disposition: glossary term** (use the Glossary term the reader names).


### List 3a. Terms of art that plain words would serve

- "frozen" -> "read-only" or "cannot be changed after creation". **Disposition: plain words** (replace with the plain words the reader names).
- "binding constraint" -> "the limit that stops all metrics improving at once". **Disposition: plain words** (replace with the plain words the reader names).
- "masks the sparsity" -> "hides which exponents are zero". **Disposition: plain words** (replace with the plain words the reader names).
- "smoothed" -> "blended by the finite temperature". **Disposition: plain words** (replace with the plain words the reader names).
- "closure" / "closure_note" -> "the sum-to-one effect". **Disposition: plain words** (replace with the plain words the reader names).
- "aligned" -> "rise together". **Disposition: plain words** (replace with the plain words the reader names).
- "traded" -> "one goes down when the other goes up". **Disposition: plain words** (replace with the plain words the reader names).
- "sampled table" -> "the data rows". **Disposition: plain words** (replace with the plain words the reader names).


### List 3b. Sentences with three or more terms of art together

- "`contending_set` holds the metrics with positive exponent in the exact-maximum fit (tau = infinity, exponents above 1e-9)." (metrics, exponent, exact-maximum fit, tau) **Disposition: no change** (a definition, statement or proof step where the terms are the content; the unresolved ones are items in List 1 and the shorter ones items in Lists 2 and 3a).
- "`elasticities[j, k]` is the elasticity along the surface: the percentage change of metric j per percentage change of metric k, constant on a facet and `nan` where metric j does not participate." (elasticity, surface, facet, participate) **Disposition: no change** (a definition, statement or proof step where the terms are the content; the unresolved ones are items in List 1 and the shorter ones items in Lists 2 and 3a).
- "Near the surface the weighted sum of log-metrics is almost constant, so a binding constraint produces negative association even where no designer traded the metrics (`closure_note` says so)." (surface, log-metrics, binding constraint, association) **Disposition: no change** (a definition, statement or proof step where the terms are the content; the unresolved ones are items in List 1 and the shorter ones items in Lists 2 and 3a).
- "Three fields describe the spread of the near-frontier designs along the surface:" with "`tension_loadings`: the same directions as loadings on the log-metrics." (loadings, log-metrics, directions) **Disposition: no change** (a definition, statement or proof step where the terms are the content; the unresolved ones are items in List 1 and the shorter ones items in Lists 2 and 3a).
- "At K > 1 the function returns a list of K reports, one per facet, each on the rows that facet dominates." (K, facet, dominates) **Disposition: no change** (a definition, statement or proof step where the terms are the content; the unresolved ones are items in List 1 and the shorter ones items in Lists 2 and 3a).
- "For designs with absolute log V below `band` (by default 1/tau, or 0.1 at infinite tau), `association` is the Pearson or Spearman correlation of the log-metrics" (log V, band, tau, association, log-metrics) **Disposition: no change** (a definition, statement or proof step where the terms are the content; the unresolved ones are items in List 1 and the shorter ones items in Lists 2 and 3a).


## Unit 10: docs/user-guide/chart.md

Density 7.9 terms of art per 100 words (49/624); staged text `docs_user-guide_chart.md.txt`.


### List 1. Terms unresolved from the unit and the Glossary

- "At a finite temperature some training designs lie beyond V = 1 by construction, so a score is meaningful relative to the band of width 1/tau." Terms: tau, "temperature=20.0" (code). The symbol tau is never tied to the fit temperature in the unit, and the Glossary entry "fit temperature" gives no symbol. **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it).
- "Compare `tau * log V` and the rank of log V among training scores, not V - 1 alone." Term: tau. Same gap; also no stated reason why tau * log V is the quantity to compare. **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it).
- "`plot_tensions`: the tension report as a heatmap." Terms: tension report, tension. The Glossary names only the `tension_report` parameter (participation threshold); "tension" itself is not defined in the unit or the Glossary. **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it).
- "For a multi-term fit, log V is the soft maximum over facets, and `improvement_factors` uses each row's active facet." Term: active facet. "Active" is undefined; the Glossary defines facet and assignment (the dominant term) but not "active". **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it). **Routed to P6** (not edited here).
- "An empty region can be an opportunity, a categorical stratum that cannot be occupied, or simply unsampled." Term: categorical stratum. Not defined in the unit or the Glossary, and not standard at the reader level. **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it).
- "The surface is also log-convex, so structure that is not log-convex is invisible to it." Terms: log-convex, structure. The reader may see this as convex in log-metrics, but the unit never says which space; "the surface" is also unresolved among the three frontier objects. **Disposition: no change** (standard vocabulary at the reader level the paper assumes (Boyd and Vandenberghe; scikit-learn)).
- "`orient_by_pca(Z, mask=None)`: rotates to the principal axes of the masked rows." Term: masked rows. The unit never says what the mask selects. **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it).
- "`frontier_targets(Z_points, estimator, preconditioner=None)`: sets log V = 0 at given positions and maps back to metrics and, with a preconditioner, to attributes." Term: preconditioner. The Glossary mentions LogAffinePreconditioner under conditioning, but the unit never introduces it. **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it).


### List 2. Where a Glossary term would say it shorter or more exactly

- "One is log V, the energy differential (level offset) to the fitted reference surface: negative inside, positive beyond." Terms: energy differential, level offset (both used, yet "log V" is introduced without being tied to "invariant value"). The Glossary says "the log of the invariant value". **Disposition: glossary term** (use the Glossary term the reader names).
- "The other `d - 1` say where along the surface the design sits, free of overall scale." Term: position along the frontier. The phrase "the other d - 1 chart coordinates, free of overall scale" is the Glossary definition. **Disposition: glossary term** (use the Glossary term the reader names).
- "Together they are a reversible rewriting of the metrics." Term: chart ("the reversible transformation between metric space and the fitting space"). **Disposition: glossary term** (use the Glossary term the reader names).
- "Plot the position coordinates and the designs spread over the trade space; gaps in that picture are candidates for white space (`hyperbolic_trade_space.gaps`):" Term: position along the frontier (for "position coordinates"). **Disposition: glossary term** (use the Glossary term the reader names).
- "`find_holes(Z, resolution=50, threshold=2.0)`: grid points inside the convex hull of Z that sit far from every design; supports `d - 1` of 1, 2 or 3." Term: white space (the unit calls the same thing "holes", "gaps" and "white space"). **Disposition: glossary term** (use the Glossary term the reader names).
- "V is a factor of improvement: doubling every metric doubles V." Term: invariant value (the Glossary gives "invariant value" for V, and the sentence never names it). **Disposition: glossary term** (use the Glossary term the reader names).
- "`project(X)` returns the design moved onto V = 1 by scaling all its metrics together." Term: fitted reference surface ("V = 1" is the level of the fitted reference surface). **Disposition: glossary term** (use the Glossary term the reader names).
- "Figure 4. One facet in the log plane: the line is V = 1, and the band below it has width 1/tau." Terms: fitted reference surface (for "the line"), fit temperature (for "1/tau"). **Disposition: glossary term** (use the Glossary term the reader names).
- "`plot_log_plane`: two metrics, the data, the frontier and its band." Term: frontier. The Glossary says the pages must name which of the three objects is meant (fitted reference surface, supporting envelope, Pareto boundary). The same applies to `plot_frontier_surface_3d`: "three metrics, the frontier surface." **Disposition: glossary term** (use the Glossary term the reader names).
- "A row with a zero metric has `nan` coordinates and no inverse." Terms: chart. Naming "chart coordinates" would be more exact than "coordinates". **Disposition: glossary term** (use the Glossary term the reader names).


### List 3a. Terms of art that plain words would serve

- "categorical stratum" -> "a kind of design that cannot be built" (or "a group the variables cannot reach"). **Disposition: plain words** (replace with the plain words the reader names).
- "simply unsampled" -> "no one has evaluated designs there". **Disposition: plain words** (replace with the plain words the reader names).
- "reversible rewriting of the metrics" -> "the same information in different coordinates" (if the Glossary term chart is not used). **Disposition: plain words** (replace with the plain words the reader names).
- "colour vocabulary" -> "set of colours" / "shared colour names". **Disposition: plain words** (replace with the plain words the reader names).
- "declared as module constants" -> "defined once in the plotting module". **Disposition: plain words** (replace with the plain words the reader names).
- "by construction" -> "because the fit allows it" (in context, an unexplained idiom). **Disposition: plain words** (replace with the plain words the reader names).
- "free of overall scale" -> "unchanged when all metrics are multiplied by the same factor". **Disposition: plain words** (replace with the plain words the reader names).
- "verdict" -> "decision" / "proof" (used twice, "not a verdict that", "a candidate and not a verdict"). **Disposition: plain words** (replace with the plain words the reader names).
- "a per-row label to pass as `color=`" -> "a label for each design, to colour the plot by". **Disposition: plain words** (replace with the plain words the reader names).


### List 3b. Sentences with three or more terms of art together

- "`transform` returns the chart, `inverse_transform` inverts it, and `score_samples` is log V alone." Four terms: chart, inverse transform, score_samples, log V. **Disposition: no change** (a definition, statement or proof step where the terms are the content; the unresolved ones are items in List 1 and the shorter ones items in Lists 2 and 3a).
- "For a multi-term fit, log V is the soft maximum over facets, and `improvement_factors` uses each row's active facet." Five terms: multi-term fit, log V, soft maximum, facets, active facet. **Disposition: no change** (a definition, statement or proof step where the terms are the content; the unresolved ones are items in List 1 and the shorter ones items in Lists 2 and 3a). **Routed to P6** (not edited here).
- "One is log V, the energy differential (level offset) to the fitted reference surface: negative inside, positive beyond." Four terms: log V, energy differential, level offset, fitted reference surface. **Disposition: no change** (a definition, statement or proof step where the terms are the content; the unresolved ones are items in List 1 and the shorter ones items in Lists 2 and 3a).
- "At a finite temperature some training designs lie beyond V = 1 by construction, so a score is meaningful relative to the band of width 1/tau." Four terms: finite temperature, V = 1, score, band of width 1/tau. **Disposition: no change** (a definition, statement or proof step where the terms are the content; the unresolved ones are items in List 1 and the shorter ones items in Lists 2 and 3a).
- "Compare `tau * log V` and the rank of log V among training scores, not V - 1 alone." Three terms: tau, log V, training scores. **Disposition: no change** (a definition, statement or proof step where the terms are the content; the unresolved ones are items in List 1 and the shorter ones items in Lists 2 and 3a).
- "`frontier_targets(Z_points, estimator, preconditioner=None)`: sets log V = 0 at given positions and maps back to metrics and, with a preconditioner, to attributes." Five terms: frontier targets, log V, positions, metrics, preconditioner and attributes. **Disposition: no change** (a definition, statement or proof step where the terms are the content; the unresolved ones are items in List 1 and the shorter ones items in Lists 2 and 3a).
- "`find_holes(Z, resolution=50, threshold=2.0)`: grid points inside the convex hull of Z that sit far from every design; supports `d - 1` of 1, 2 or 3." Three terms: grid points, convex hull, Z (position coordinates). **Disposition: no change** (a definition, statement or proof step where the terms are the content; the unresolved ones are items in List 1 and the shorter ones items in Lists 2 and 3a).
- "They share one colour vocabulary, declared as module constants (`FRONTIER_COLOR`, `BAND_COLOR`, `HOLE_COLOR`, `TENSION_CMAP`)." Four terms: frontier, band, hole, tension. **Disposition: no change** (a definition, statement or proof step where the terms are the content; the unresolved ones are items in List 1 and the shorter ones items in Lists 2 and 3a).
- "For a multi-term fit the plots draw every facet, and `facet_labels(estimator, X)` gives a per-row label to pass as `color=`." Three terms: multi-term fit, facet, facet_labels. **Disposition: no change** (a definition, statement or proof step where the terms are the content; the unresolved ones are items in List 1 and the shorter ones items in Lists 2 and 3a).
- "The surface is also log-convex, so structure that is not log-convex is invisible to it." Three terms: surface, log-convex, structure. **Disposition: no change** (a definition, statement or proof step where the terms are the content; the unresolved ones are items in List 1 and the shorter ones items in Lists 2 and 3a).


## Unit 11: docs/theory.md

Density 7.5 terms of art per 100 words (44/587); staged text `docs_theory.md.txt`.


### List 1. Terms unresolved from the unit and the Glossary

- "Let $B$ be a basis of the sum-zero subspace of $\mathbb{R}^d$ (a Helmert log-ratio basis by default)." Term: Helmert log-ratio basis. Not defined here, no Glossary entry; the reader cannot tell what B is or why it is the default. **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it).
- "the **fitted reference surface**, V = 1 at the working temperature tau; it is smooth, so a few designs lie beyond it;" Term: working temperature (tau). The Glossary has "fit temperature" (and mentions "working-temperature" only in passing); tau is never defined in the unit, and the name differs from the Glossary's. **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it).
- "the **Pareto boundary**, the nondominated set of the attainable designs, a property of the system and not of the fit." Term: attainable designs / attainable set. Used as the contrast object but defined neither here nor as a Glossary entry. **Disposition: no change** (standard vocabulary at the reader level the paper assumes (Boyd and Vandenberghe; scikit-learn)).
- "Metrics are positive and larger-is-better (conditioning is yours to choose); the surface is log-convex; at one term the elasticities are constant; designs are chosen by an evaluator and not drawn from the attainable set." Terms: log-convex surface; evaluator. Neither is defined; "evaluator" is not the Glossary's "evaluation". **Disposition: no change** (standard vocabulary at the reader level the paper assumes (Boyd and Vandenberghe; scikit-learn)).
- "fitting several facets alternates weights from the current model with one program for all terms." Term: "weights from the current model" (the soft weights over terms). The Glossary has "term temperature" and "support weights" but the unit never says which weights, what they depend on, or what is alternated. **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it).


### List 2. Where a Glossary term would say it shorter or more exactly

- "The package takes the sharp limit of the weights, one label per design; which facet dominates a design is analysis of the fitted model, not part of the fit." Terms: term temperature (infinity is the sharp limit of one label per design); assignment (the dominant term of a design). **Disposition: glossary term** (use the Glossary term the reader names).
- "where $Z$ is free of overall scale and says where along the surface the design sits, and $\log V$ says how far from it." Terms: position along the frontier (for Z); energy differential (for log V). **Disposition: glossary term** (use the Glossary term the reader names).
- "The fit chooses $w$ and an offset $\beta$ so that the data lie on or below the surface" Term: exponent vector (for w). **Disposition: glossary term** (use the Glossary term the reader names).
- "At a finite working temperature a small weight means weak participation, set by a participation threshold." Terms: exponent (the Glossary calls these weights exponents); fit temperature (for working temperature). **Disposition: glossary term** (use the Glossary term the reader names).
- "The metrics with positive weight at tau = infinity are the contending set, and its size n is the n-lemma (a dilemma is n = 2, a trilemma n = 3)." Terms: exponent vector ("positive entries name the metrics that contend"); supporting envelope (for "at tau = infinity"). **Disposition: glossary term** (use the Glossary term the reader names).
- "On the surface $w\cdot u=\beta$, the level surface is flat in log space, so moving along it trades the contending metrics at constant rates:" Terms: facet (flat piece in log space); elasticity (the rates). **Disposition: glossary term** (use the Glossary term the reader names).
- "Inside the surface V < 1; beyond it V > 1, and V - 1 says by how much." Term: novelty (how far beyond the fitted reference surface) is the Glossary's word for the beyond-the-surface reading. **Disposition: glossary term** (use the Glossary term the reader names).
- "the **supporting envelope**, the same fit at tau = infinity: the exact maximum, a linear program, with no design above it;" Term: fit temperature (infinite is the exact maximum). **Disposition: glossary term** (use the Glossary term the reader names).


### List 3a. Terms of art that plain words would serve

- "using the log-mean-exp (entropic) soft maximum of $w\cdot u$ over the designs." Term: soft maximum. Plain words: smooth maximum. **Disposition: plain words** (replace with the plain words the reader names). **Routed to P6** (not edited here).
- "the fit at tau = infinity is a linear program whose solution is generically sparse." Term: generically sparse. Plain words: has mostly zero entries for almost all data. **Disposition: plain words** (replace with the plain words the reader names).
- "Let $B$ be a basis of the sum-zero subspace of $\mathbb{R}^d$" Term: sum-zero subspace. Plain words: vectors whose entries add to zero. **Disposition: plain words** (replace with the plain words the reader names).
- "The package takes the sharp limit of the weights, one label per design;" Term: sharp limit. Plain words: the extreme case where each design gets exactly one term. **Disposition: plain words** (replace with the plain words the reader names).
- "fitting several facets alternates weights from the current model with one program for all terms." Term: alternates. Plain words: repeats two steps in turn (update the weights, then refit all terms). **Disposition: plain words** (replace with the plain words the reader names).
- "the **Pareto boundary**, the nondominated set of the attainable designs," Term: nondominated. Plain words: designs no other design beats on every metric. **Disposition: plain words** (replace with the plain words the reader names).


### List 3b. Sentences with three or more terms of art together

- "The fit chooses $w$ and an offset $\beta$ so that the data lie on or below the surface $\log V=w\cdot u-\beta=0$, using the log-mean-exp (entropic) soft maximum of $w\cdot u$ over the designs." Terms: offset, log-mean-exp, entropic, soft maximum, surface. **Disposition: no change** (a definition, statement or proof step where the terms are the content; the unresolved ones are items in List 1 and the shorter ones items in Lists 2 and 3a). **Routed to P6** (not edited here).
- "Fitting one facet is a geometric program (GP), solved as a convex program after the logarithmic change of variables; fitting several facets alternates weights from the current model with one program for all terms." Terms: facet, geometric program, convex program, change of variables, weights, terms. **Disposition: no change** (a definition, statement or proof step where the terms are the content; the unresolved ones are items in List 1 and the shorter ones items in Lists 2 and 3a).
- "A sum of such products, a posynomial, extends one term to K terms and keeps the programs inside geometric programming." Terms: posynomial, term, K terms, geometric programming. **Disposition: no change** (a definition, statement or proof step where the terms are the content; the unresolved ones are items in List 1 and the shorter ones items in Lists 2 and 3a).
- "It is found from the data and not assumed: the fit at tau = infinity is a linear program whose solution is generically sparse." Terms: fit, tau = infinity, linear program, generically sparse. **Disposition: no change** (a definition, statement or proof step where the terms are the content; the unresolved ones are items in List 1 and the shorter ones items in Lists 2 and 3a).
- "Metrics are positive and larger-is-better (conditioning is yours to choose); the surface is log-convex; at one term the elasticities are constant; designs are chosen by an evaluator and not drawn from the attainable set." Terms: metrics, conditioning, log-convex, term, elasticities, attainable set. **Disposition: no change** (a definition, statement or proof step where the terms are the content; the unresolved ones are items in List 1 and the shorter ones items in Lists 2 and 3a).
- "Let $B$ be a basis of the sum-zero subspace of $\mathbb{R}^d$ (a Helmert log-ratio basis by default)." Terms: basis, sum-zero subspace, Helmert, log-ratio. **Disposition: no change** (a definition, statement or proof step where the terms are the content; the unresolved ones are items in List 1 and the shorter ones items in Lists 2 and 3a).
- "At a finite working temperature a small weight means weak participation, set by a participation threshold." Terms: working temperature, weight, participation, participation threshold. **Disposition: no change** (a definition, statement or proof step where the terms are the content; the unresolved ones are items in List 1 and the shorter ones items in Lists 2 and 3a).


## Unit 12: README.md

Density 7.4 terms of art per 100 words (11/148); staged text `README.md.txt`.


### List 1. Terms unresolved from the unit and the Glossary

- "Python package `hyperbolic_trade_space` (import alias `hts`); the method is the *posynomial invariant form*." Terms: "hyperbolic", "invariant form". No Glossary entry for either; the Glossary has "invariant value" and "posynomial" but not the named form or why it is "hyperbolic". **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it).
- "From noisy, biased observations of a design problem (configuration variables and empirically assessed attributes), the method learns a hyperbolic "space": a monomial, later posynomial, frontier V(m) = Π m_j^{w_j} whose unit level set is the Pareto frontier, together with an invertible coordinate chart (position along the frontier, and log V, the energy differential to it)." Terms: "hyperbolic space" (in scare quotes, never explained); "V(m)" and "w_j" (the weights w are not defined here; the Glossary says "invariant value" but does not tie it to the symbol V); "frontier" (the Glossary says it names three objects, and the sentence does not say which). **Disposition: no change** (standard vocabulary at the reader level the paper assumes (Boyd and Vandenberghe; scikit-learn)).
- "Status: WP0 (setup) complete; the package code arrives in later work packages." Terms: "WP0", "work packages". Project jargon, not defined in the unit or the Glossary. **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it).
- "It is a scikit-learn-compatible unsupervised estimator, with SymPy-verified derivations and an ADCS trade-study case." Term: "ADCS". Unexpanded acronym; not in the Glossary. **Disposition: no change** (standard vocabulary at the reader level the paper assumes (Boyd and Vandenberghe; scikit-learn)).
- "- `examples/adcs/` — the ADCS trade-study case (WP4, WP7)" Terms: "WP4", "WP7", "ADCS". Same as above. **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it).


### List 2. Where a Glossary term would say it shorter or more exactly

- "From noisy, biased observations of a design problem (configuration variables and empirically assessed attributes), the method learns a hyperbolic "space": a monomial, later posynomial, frontier V(m) = Π m_j^{w_j} whose unit level set is the Pareto frontier, together with an invertible coordinate chart (position along the frontier, and log V, the energy differential to it)." Term: "fitted reference surface" for "a monomial ... frontier ... whose unit level set" (the level V = 1 of the fitted invariant). Also "Pareto boundary" is the Glossary name where "Pareto frontier" is used, and "configuration" and "attributes" for the parenthetical. "unit level set" is "the level V = 1". **Disposition: glossary term** (use the Glossary term the reader names).
- "Learn the shape of a design trade space." Term: "trade space" is used but the Glossary only defines it indirectly ("number of metrics ... the dimension of the trade space"); "white space" and "metrics" are the terms that say what shape is learned. Weak case. **Disposition: glossary term** (use the Glossary term the reader names).
- "- `examples/adcs/` — the ADCS trade-study case (WP4, WP7)" No Glossary term shorter; none. **Disposition: glossary term** (use the Glossary term the reader names).


### List 3a. Terms of art that plain words would serve

- "Learn the shape of a design trade space." Fine as is; none. **Disposition: plain words** (replace with the plain words the reader names).
- "From noisy, biased observations of a design problem (configuration variables and empirically assessed attributes), the method learns a hyperbolic "space": a monomial, later posynomial, frontier V(m) = Π m_j^{w_j} whose unit level set is the Pareto frontier, together with an invertible coordinate chart (position along the frontier, and log V, the energy differential to it)." - "unit level set": "the set where V = 1". - "invertible coordinate chart": "a reversible change of coordinates" (but "chart" is a Glossary term, so keep that one). - "hyperbolic "space"": "trade space" or "the geometry". - "empirically assessed": "measured or judged". **Disposition: plain words** (replace with the plain words the reader names).
- "It is a scikit-learn-compatible unsupervised estimator, with SymPy-verified derivations and an ADCS trade-study case." - "SymPy-verified derivations": "derivations checked by computer algebra" (SymPy is standard at this level; low priority). **Disposition: plain words** (replace with the plain words the reader names).
- "- `derivation/` — SymPy axiom and lemma scripts (WP1)" - "axiom and lemma scripts": "scripts that check each step of the derivation". **Disposition: plain words** (replace with the plain words the reader names).


### List 3b. Sentences with three or more terms of art together

- "From noisy, biased observations of a design problem (configuration variables and empirically assessed attributes), the method learns a hyperbolic "space": a monomial, later posynomial, frontier V(m) = Π m_j^{w_j} whose unit level set is the Pareto frontier, together with an invertible coordinate chart (position along the frontier, and log V, the energy differential to it)." Terms together: configuration, attributes, hyperbolic space, monomial, posynomial, frontier, level set, Pareto frontier, chart, position along the frontier, energy differential (eleven or more). **Disposition: plain words** (introductory page: spread the terms over more words).
- "It is a scikit-learn-compatible unsupervised estimator, with SymPy-verified derivations and an ADCS trade-study case." Terms together: estimator, SymPy, derivations, ADCS, trade study (borderline; ADCS is the unresolved one). **Disposition: plain words** (introductory page: spread the terms over more words).
- "Status: WP0 (setup) complete; the package code arrives in later work packages." Terms together: WP0, work packages (two project-internal terms; below three). **Disposition: plain words** (introductory page: spread the terms over more words).


## Unit 13: docs/user-guide/termination.md

Density 7.3 terms of art per 100 words (44/601); staged text `docs_user-guide_termination.md.txt`.


### List 1. Terms unresolved from the unit and the Glossary

- "Descent: no step made the mean slack worse (`mean_slack_`, defined at every number of terms)." Terms: mean slack. Not in the Glossary or defined in the unit. **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it).
- "`certified`: assignment fixed, residuals within `eps_feas`, `max_gap` within `eps_kkt`, no empty facet, margin positive." Terms: residuals, eps_feas, eps_kkt, empty facet. Residuals of what is never said; the tolerances are not defined here; "empty facet" has no entry. **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it).
- "`guard_stop`: an iteration raised the mean slack by more than `guard_tol`. Not converged." Terms: guard_tol, mean slack. The guard is not defined. **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it).
- "A small `conditioning_` or `n_eff_` says to widen the sample or read exponents loosely." Terms: n_eff_. Not defined anywhere. **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it).
- "`stationary`: the gaps hold, the curvature does not: a saddle or a flat direction." Terms: min_curvature, active face, strict local minimizer of the soft objective. The soft objective and the active face are undefined. **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it).
- "The smallest eigenvalue of the restricted Hessian at each facet's fit, over the participating exponents (above 1e-3), one per facet." Terms: restricted Hessian. The restriction is not stated (the Glossary entry for conditioning of the exponents does not say either). **Disposition: no change** (standard vocabulary at the reader level the paper assumes (Boyd and Vandenberghe; scikit-learn)).
- "Compare `gamma` with the median margin, the median gap between a design's best and second-best facet score: far below it, a few designs sit on a seam and most do not." Terms: facet score, seam. Neither is in the Glossary; "seam" is only glossed in passing. **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it).
- "`radius` is `gamma / (2R)`, with R the largest norm of a row (u, -1)." Terms: row (u, -1). u is never defined. **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it).
- "`bound`: the share-weighted sum of facet gaps, bounding the distance from the fixed-assignment optimum." Terms: bound, shares (the fields), fixed assignment. The Glossary "share" is the ternary-plot meaning, not these weights. **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it).
- "`not_applicable`: one term, `facet_step="tangent"`, a `penalty`, one metric, fewer designs than facets, or a soft fit at infinite temperature." Terms: facet_step="tangent", penalty. Not defined. **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it). **Routed to P6** (not edited here).
- "Every fit records how it stopped." Terms: none. Used only as a check that the opening is clear. **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it).
- "With several terms it alternates between weights from the current model and refitting each facet; the record says which of three levels it meets." Terms: alternates (the algorithm is not named); weights are undefined here (Glossary has support weights only). **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it).


### List 2. Where a Glossary term would say it shorter or more exactly

- "The assignment margin is the smallest gap by which a row's facet beats the runner-up; the stable radius is the perturbation provably leaving every facet unchanged." Term: assignment margin, stable radius, "row" for design. The stable radius is a size, not a perturbation; say "design" for "row". **Disposition: glossary term** (use the Glossary term the reader names).
- "2. Numerical stationarity: no first-order improvement is left. The facet gap G_k measures what remains." Term: facet gap. Glossary says "the first-order gap of a facet's refit; zero exactly when the optimality conditions hold". **Disposition: glossary term** (use the Glossary term the reader names).
- "`min_curvature`: soft fit only, the smallest curvature on the active face; `nan` otherwise." Term: conditioning of the exponents. The Glossary entry covers the same quantity for the hard fit. **Disposition: glossary term** (use the Glossary term the reader names). **Routed to P6** (not edited here).
- "At infinite temperature this happens when a frontier row lies on two facet planes or two facets coincide." Terms: supporting envelope, fit temperature. "Frontier row" reads as the supporting envelope; "infinite temperature" as the exact maximum. **Disposition: glossary term** (use the Glossary term the reader names).
- "`gamma`, `radius`: the margin and stable radius, `nan` at one term." Term: assignment margin. "the margin" is the assignment margin. **Disposition: glossary term** (use the Glossary term the reader names).
- "Compare `gamma` with the median margin, the median gap between a design's best and second-best facet score: far below it, a few designs sit on a seam and most do not." Term: assignment margin. The median is the typical assignment margin. **Disposition: glossary term** (use the Glossary term the reader names).
- "A soft fit (finite `term_temperature`) has no assignment, so no margin:" Term: term temperature. "Soft fit" is the one with finite term temperature. **Disposition: glossary term** (use the Glossary term the reader names). **Routed to P6** (not edited here).
- "The margin `gamma` is in score units (log metrics), the scale of the band 1/tau" Terms: log-metrics, fit temperature. "tau" is the fit temperature; the unit is log-metrics. **Disposition: glossary term** (use the Glossary term the reader names).


### List 3a. Terms of art that plain words would serve

- "Numerical stationarity" -> "no first-order improvement is left" (the unit says it itself). **Disposition: plain words** (replace with the plain words the reader names).
- "Conditional local optimality" -> "optimal for the current assignment of designs to facets". **Disposition: plain words** (replace with the plain words the reader names).
- "stationary_without_margin" -> "converged, but a design sits on a boundary". **Disposition: plain words** (replace with the plain words the reader names).
- "a seam between facets" -> "an edge where two facets meet". **Disposition: plain words** (replace with the plain words the reader names).
- "Residuals within eps_feas" -> "constraint violations below tolerance". **Disposition: plain words** (replace with the plain words the reader names).
- "a saddle or a flat direction" -> fine for this reader; none needed. **Disposition: plain words** (replace with the plain words the reader names).
- "Descent" (level 1) -> "the objective never got worse". **Disposition: plain words** (replace with the plain words the reader names).
- "weakly identified exponents" -> "exponents the data barely determine". **Disposition: plain words** (replace with the plain words the reader names).


### List 3b. Sentences with three or more terms of art together

- "`certified`: assignment fixed, residuals within `eps_feas`, `max_gap` within `eps_kkt`, no empty facet, margin positive." Terms: assignment, residuals, eps_feas, max_gap, eps_kkt, empty facet, margin. **Disposition: no change** (a definition, statement or proof step where the terms are the content; the unresolved ones are items in List 1 and the shorter ones items in Lists 2 and 3a).
- "`certified`: weighted gaps within `eps_kkt` and `min_curvature` above `eps_feas`, a strict local minimizer of the soft objective." Terms: gaps, eps_kkt, min_curvature, eps_feas, soft objective. **Disposition: no change** (a definition, statement or proof step where the terms are the content; the unresolved ones are items in List 1 and the shorter ones items in Lists 2 and 3a).
- "The smallest eigenvalue of the restricted Hessian at each facet's fit, over the participating exponents (above 1e-3), one per facet." Terms: restricted Hessian, facet, participating exponents. **Disposition: no change** (a definition, statement or proof step where the terms are the content; the unresolved ones are items in List 1 and the shorter ones items in Lists 2 and 3a).
- "`not_applicable`: one term, `facet_step="tangent"`, a `penalty`, one metric, fewer designs than facets, or a soft fit at infinite temperature." Terms: term, facet_step, penalty, metric, facet, soft fit, temperature. **Disposition: no change** (a definition, statement or proof step where the terms are the content; the unresolved ones are items in List 1 and the shorter ones items in Lists 2 and 3a). **Routed to P6** (not edited here).
- "`min_curvature`: soft fit only, the smallest curvature on the active face; `nan` otherwise." Terms: soft fit, curvature, active face. **Disposition: no change** (a definition, statement or proof step where the terms are the content; the unresolved ones are items in List 1 and the shorter ones items in Lists 2 and 3a). **Routed to P6** (not edited here).
- "The margin `gamma` is in score units (log metrics), the scale of the band 1/tau; `radius` is `gamma / (2R)`, with R the largest norm of a row (u, -1)." Terms: margin, score units, log-metrics, band, tau, radius, row. **Disposition: no change** (a definition, statement or proof step where the terms are the content; the unresolved ones are items in List 1 and the shorter ones items in Lists 2 and 3a).
- "Conditional local optimality: if no design sits exactly on a seam between facets, small changes to the facets cannot change which facet dominates which design, so the fixed assignment is optimal." Terms: seam, facets, dominates, assignment, optimal. **Disposition: no change** (a definition, statement or proof step where the terms are the content; the unresolved ones are items in List 1 and the shorter ones items in Lists 2 and 3a).


## Unit 14: docs/user-guide/fitting.md

Density 7.3 terms of art per 100 words (68/932); staged text `docs_user-guide_fitting.md.txt`.


### List 1. Terms unresolved from the unit and the Glossary

- "`exponents_`: shape `(n_terms, d)`, each row on the simplex." - Terms: exponents_, simplex (and d is undefined here). Glossary says "exponent vector ... on the simplex" but "simplex" itself is not defined; `n_terms` and `d` are not tied to the Glossary here. **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it).
- "`n_eff_`: how many designs carry the fit." - Term: n_eff_ ("carry the fit"). Close to "support weights" in the Glossary, but the effective count is never defined. **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it).
- "`objective_` and `mean_slack_`: `objective_` is what the solver minimized, the soft maximum at one term and the mean slack at several, so it is not comparable across numbers of terms." - Terms: soft maximum, slack, mean slack. The Glossary has no entry for slack or soft maximum; "facet and design" gap is only implied. **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it). **Routed to P6** (not edited here).
- "`termination_` and `conditioning_`: how the fit stopped and how well its exponents are identified ([termination page](termination.md))." - Term: identified (of the exponents). The Glossary has "conditioning of the exponents", but this sentence says "identified" without saying what that means. **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it).
- "The chart's basis, offsets and support weights are `basis_`, `log_offset_` and `support_weights_`." - Terms: basis, offset (of the chart). The Glossary defines chart but not its basis or log offset. **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it).
- "Keep `min_exponent` (a floor on every exponent) at 0 to read the contending set, and choose `coordinates` as `"ilr"` or `"alr"`." - Terms: ilr, alr. Neither is defined in the unit or the Glossary, and they are not standard at this reader level. **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it).
- "Tau is in units of inverse log-spread, so it depends on the conditioning." - Terms: log-spread, and the "conditioning" meant here (the Glossary's conditioning is the attributes-to-metrics step). Log-spread is undefined. **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it).
- "Fitting alternates weights from the current model with a refit, from several seeded starts (`n_restarts`, default 5) keeping the best." - Terms: refit, weights (which weights), seeded starts. The Glossary has "term temperature" for "soft weights" but not the alternating scheme. **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it).
- "`facet_step` is `"support"` (default) or `"tangent"`, which is not monotone and carries no local-optimality status." - Terms: facet_step, support, tangent, local-optimality status. None is defined. **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it).
- "`penalty="reweighted_l1"` with `alpha` pushes small exponents to exact zero, at finite temperature only." - Term: reweighted_l1. Not defined. A reader at this level knows l1, but not the reweighting. **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it).
- "Resample: a facet whose exponents change between bootstrap resamples or restarts is a splinter, a few designs fitted alone, and K is too large." - Term: splinter. It is glossed in the sentence itself, but it is not in the Glossary. **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it).
- "`tension_report` takes its band from the temperature, 1/tau. A facet with fewer than `min_near_frontier` designs in the band raises, and the message names the `band`, and the matching `temperature`, that holds enough." - Terms: tension_report, band. The Glossary has "participation threshold" mentioning "tension" but has no entry for tension or the band. "raises" is used loosely. **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it).
- "Kernel expansions that stay inside geometric programming are documented, not built." - Term: kernel expansions. Not defined here. "Geometric programming" is in the Glossary. **Disposition: no change** (standard vocabulary at the reader level the paper assumes (Boyd and Vandenberghe; scikit-learn)).
- "`select_temperature` needs a target the fit can reach." - Term: target (target_frac_above). Defined in practice, but "level-off" below is used without definition. **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it).
- "...so `frac_above_` levels off above zero as tau grows..." - Term: level-off (asymptote). Plain, but its cause ("facets are not supporting planes") is not explained. **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it).


### List 2. Where a Glossary term would say it shorter or more exactly

- "At one term it solves a convex problem and returns the minimizer." - Glossary: "geometric program" (convex after x = exp(y)). The sentence could name the problem. **Disposition: glossary term** (use the Glossary term the reader names).
- "`frac_above_`: the fraction of designs beyond V = 1." - Glossary: "novelty" and "fitted reference surface" (rows above it exist by construction). "Beyond V = 1" could say "above the fitted reference surface". **Disposition: glossary term** (use the Glossary term the reader names).
- "Infinity (`np.inf`) is the exact maximum, a linear program giving the supporting envelope: no design lies above it." - Glossary: "supporting envelope" is used correctly. "fit temperature" would say "tau" more exactly in the heading and the first sentence. **Disposition: glossary term** (use the Glossary term the reader names).
- "`temperature` is tau, how hard the maximum is." - Glossary: "fit temperature". **Disposition: glossary term** (use the Glossary term the reader names).
- "A finite tau gives the fitted reference surface with a band of near-frontier designs of width 1/tau, and a few designs beyond V = 1." - Glossary: "fit temperature" (finite gives a band of near-frontier designs); "fitted reference surface". **Disposition: glossary term** (use the Glossary term the reader names).
- "One term is one flat facet in log space with constant elasticities." - Glossary: "log-metrics" (log space), "monomial" or "term" (one term is one monomial). **Disposition: glossary term** (use the Glossary term the reader names).
- "`term_temperature` (kappa, default infinity) sets the temperature of the soft weights: finite, every design weighs every term; infinity, one label per design." - Glossary: "term temperature" and "assignment". **Disposition: glossary term** (use the Glossary term the reader names).
- "Reported facets are the dominant term." - Glossary: "assignment" (the dominant term of a design). **Disposition: glossary term** (use the Glossary term the reader names).
- "`facet_` gives each training row's dominant facet; `coefficients_` and `facet_share_` the facets' coefficients and shares." - Glossary: "assignment" for the dominant facet of a row. **Disposition: glossary term** (use the Glossary term the reader names).
- "`assign_facets(X)` reads which facet dominates new rows." - Glossary: "assignment". **Disposition: glossary term** (use the Glossary term the reader names).
- "Keep `min_exponent` ... at 0 to read the contending set..." - Glossary: "numerically zero" (the 1e-12 cutoff), and "participation threshold" would be exact about when an exponent counts. **Disposition: glossary term** (use the Glossary term the reader names).
- "Add a term while `mean_slack_` still falls by more than the variation between restarts." - Glossary: "number of terms" (the analyst's choice, never selected by the fit). **Disposition: glossary term** (use the Glossary term the reader names).
- "With two metrics the facets can be drawn in the log plane:" - Glossary: "log-metrics" for "log plane". **Disposition: glossary term** (use the Glossary term the reader names).
- "...Figure 2. Three facets fitted to two metrics: each facet is a straight line in log space, and the frontier is their envelope." - Glossary: "frontier" is an everyday word; this should say "fitted reference surface" or "supporting envelope". Same for the opening line "fits the frontier model" and "planted frontier". **Disposition: glossary term** (use the Glossary term the reader names).
- "With several terms the facets are not supporting planes, so `frac_above_` levels off..." - Glossary: "supporting envelope" applies only at infinite temperature; the sentence could name that. **Disposition: glossary term** (use the Glossary term the reader names).
- "Both are seeded and used throughout these pages." - No Glossary term. None. **Disposition: glossary term** (use the Glossary term the reader names).


### List 3a. Terms of art that plain words would serve

- "decomposition family" ("It follows the scikit-learn decomposition family: ..."): plain words, "the same methods as scikit-learn's PCA-style transformers". **Disposition: plain words** (replace with the plain words the reader names).
- "simplex" ("each row on the simplex"): plain words, "nonnegative and sums to 1". **Disposition: plain words** (replace with the plain words the reader names).
- "splinter": plain words, "a facet resting on a handful of designs". **Disposition: plain words** (replace with the plain words the reader names).
- "bootstrap resamples": plain words, "resamples of the rows drawn with replacement". **Disposition: plain words** (replace with the plain words the reader names).
- "level-off": plain words, "stops falling and flattens". **Disposition: plain words** (replace with the plain words the reader names).
- "not bracketed": plain words, "no value of tau in the bounds reaches the target". **Disposition: plain words** (replace with the plain words the reader names).
- "monotone" ("is not monotone in tau"): plain words, "does not always move the same way as tau". **Disposition: plain words** (replace with the plain words the reader names).
- "seeded starts": plain words, "random starting points fixed by a seed". **Disposition: plain words** (replace with the plain words the reader names).
- "carry the fit": plain words, "determine the fit". **Disposition: plain words** (replace with the plain words the reader names).
- "conditioned metrics" (first line): plain words, "metrics that are already positive and larger-is-better". **Disposition: plain words** (replace with the plain words the reader names).
- "log-spread": plain words, "the range of the data in log units". **Disposition: plain words** (replace with the plain words the reader names).
- "the minimizer": plain words, "the best fit". **Disposition: plain words** (replace with the plain words the reader names).


### List 3b. Sentences with three or more terms of art together

- "`objective_` and `mean_slack_`: `objective_` is what the solver minimized, the soft maximum at one term and the mean slack at several, so it is not comparable across numbers of terms." - Terms: objective, soft maximum, mean slack, numbers of terms. **Disposition: no change** (a definition, statement or proof step where the terms are the content; the unresolved ones are items in List 1 and the shorter ones items in Lists 2 and 3a). **Routed to P6** (not edited here).
- "Keep `min_exponent` (a floor on every exponent) at 0 to read the contending set, and choose `coordinates` as `"ilr"` or `"alr"`." - Terms: min_exponent, contending set, coordinates, ilr, alr. **Disposition: no change** (a definition, statement or proof step where the terms are the content; the unresolved ones are items in List 1 and the shorter ones items in Lists 2 and 3a).
- "A finite tau gives the fitted reference surface with a band of near-frontier designs of width 1/tau, and a few designs beyond V = 1." - Terms: tau, fitted reference surface, band, near-frontier, V = 1. **Disposition: no change** (a definition, statement or proof step where the terms are the content; the unresolved ones are items in List 1 and the shorter ones items in Lists 2 and 3a).
- "`penalty="reweighted_l1"` with `alpha` pushes small exponents to exact zero, at finite temperature only." - Terms: reweighted_l1, alpha, exponents, temperature. **Disposition: no change** (a definition, statement or proof step where the terms are the content; the unresolved ones are items in List 1 and the shorter ones items in Lists 2 and 3a).
- "`facet_step` is `"support"` (default) or `"tangent"`, which is not monotone and carries no local-optimality status." - Terms: facet_step, support, tangent, monotone, local-optimality status. **Disposition: no change** (a definition, statement or proof step where the terms are the content; the unresolved ones are items in List 1 and the shorter ones items in Lists 2 and 3a).
- "With several terms the facets are not supporting planes, so `frac_above_` levels off above zero as tau grows (about 0.30 on the table of `make_frontier_data(300, 4, n_terms=2, random_state=777)`) and the default target 0.10 raises "not bracketed"." - Terms: supporting planes, frac_above_, tau, target, bracketed. **Disposition: no change** (a definition, statement or proof step where the terms are the content; the unresolved ones are items in List 1 and the shorter ones items in Lists 2 and 3a).
- "A facet with fewer than `min_near_frontier` designs in the band raises, and the message names the `band`, and the matching `temperature`, that holds enough." - Terms: facet, min_near_frontier, band, temperature. **Disposition: no change** (a definition, statement or proof step where the terms are the content; the unresolved ones are items in List 1 and the shorter ones items in Lists 2 and 3a).
- "Fitting alternates weights from the current model with a refit, from several seeded starts (`n_restarts`, default 5) keeping the best." - Terms: weights, refit, seeded starts, restarts. **Disposition: no change** (a definition, statement or proof step where the terms are the content; the unresolved ones are items in List 1 and the shorter ones items in Lists 2 and 3a).
- "`term_temperature` (kappa, default infinity) sets the temperature of the soft weights: finite, every design weighs every term; infinity, one label per design." - Terms: term_temperature, kappa, soft weights, term, label. **Disposition: no change** (a definition, statement or proof step where the terms are the content; the unresolved ones are items in List 1 and the shorter ones items in Lists 2 and 3a).


## Unit 15: paper/supporting_material.ipynb :: Appendix D. Extended results: what the method found in the table (part 2)

Density 7.3 terms of art per 100 words (14/192); staged text `supp_appendix-d-extended-results-what-the-met_2.txt`.


### List 1. Terms unresolved from the unit and the Glossary

- "The tension report runs a principal component analysis on the chart coordinates Z of a facet's near-frontier designs." Terms: tension report, near-frontier, Z. The Glossary mentions tension_report only as a function carrying a threshold, never says what it reports. "Near-frontier" is undefined, and Glossary "frontier" names three different objects. Z is not tied to a symbol anywhere. **Disposition: no change** (standard vocabulary at the reader level the paper assumes (Boyd and Vandenberghe; scikit-learn)).
- "Its directions say along which combinations of metrics the near-frontier designs vary the most, with loadings on the metrics through the chart basis; the fit says which metrics bind, the analysis says where the sampled designs spread along the fitted surface." Term: chart basis. The Glossary defines chart but not its basis, and the reader cannot tell how loadings on chart coordinates are mapped back to metrics. **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it).
- "Dataset cubesat-primary, K = 1, designs with |log V| under the band 1/tau:" Terms: cubesat-primary, tau, band, V. The dataset is not described in this unit. The symbol tau is not defined here and the band is not defined as a term, though the Glossary's fit temperature hints at it. **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it).
- "| 2 | 0.21 | depth of discharge +0.51 to +0.52, total mass -0.46, slew time -0.39 |" Terms: depth of discharge, slew time. Metric names come from the case study and are not defined for this reader. The "+0.51 to +0.52" ranges are also unexplained (rounding? several facets?). **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it).


### List 2. Where a Glossary term would say it shorter or more exactly

- "the fit says which metrics bind" Glossary: contending set (metrics with positive exponent). "Bind" is looser and not defined. **Disposition: glossary term** (use the Glossary term the reader names).
- "the analysis says where the sampled designs spread along the fitted surface." Glossary: position along the frontier (the other d - 1 chart coordinates), and fitted reference surface. **Disposition: glossary term** (use the Glossary term the reader names).
- "Dataset cubesat-primary, K = 1, designs with |log V| under the band 1/tau:" Glossary: energy differential (log of the invariant value, so |energy differential| < 1/fit temperature); K = number of terms; tau = fit temperature. **Disposition: glossary term** (use the Glossary term the reader names).
- "The tension report runs a principal component analysis on the chart coordinates Z of a facet's near-frontier designs." Glossary: chart (names the transformation) and position along the frontier (names the free coordinates that PCA is run on). **Disposition: glossary term** (use the Glossary term the reader names).


### List 3a. Terms of art that plain words would serve

- "near-frontier designs" Plain words: designs close to the fitted surface. **Disposition: plain words** (replace with the plain words the reader names).
- "through the chart basis" Plain words: through the coordinate map back to the metrics. **Disposition: plain words** (replace with the plain words the reader names).
- "which metrics bind" Plain words: which metrics matter most / trade off against each other. **Disposition: plain words** (replace with the plain words the reader names).
- "Share of the spread of the chart coordinates" Plain words: fraction of the variance (explained variance ratio). **Disposition: plain words** (replace with the plain words the reader names).


### List 3b. Sentences with three or more terms of art together

- "The tension report runs a principal component analysis on the chart coordinates Z of a facet's near-frontier designs." Terms: tension report, principal component analysis, chart coordinates, facet, near-frontier. **Disposition: no change** (a definition, statement or proof step where the terms are the content; the unresolved ones are items in List 1 and the shorter ones items in Lists 2 and 3a).
- "Its directions say along which combinations of metrics the near-frontier designs vary the most, with loadings on the metrics through the chart basis; the fit says which metrics bind, the analysis says where the sampled designs spread along the fitted surface." Terms: near-frontier, loadings, chart basis, bind, fitted surface. **Disposition: no change** (a definition, statement or proof step where the terms are the content; the unresolved ones are items in List 1 and the shorter ones items in Lists 2 and 3a).
- "Dataset cubesat-primary, K = 1, designs with |log V| under the band 1/tau:" Terms: K, V, band, tau. **Disposition: no change** (a definition, statement or proof step where the terms are the content; the unresolved ones are items in List 1 and the shorter ones items in Lists 2 and 3a).


## Unit 16: paper/paper.ipynb :: The fit and its geometry

Density 7.2 terms of art per 100 words (45/623); staged text `paper_the-fit-and-its-geometry.txt`.


### List 1. Terms unresolved from the unit and the Glossary

- "The invariant value scales with the metrics (L1), and shifting every log-metric by a constant moves the offset by that constant and leaves the exponents unchanged (L2)." Term: "the offset". The Glossary's only offsets are "level offset" and "energy differential", which are not this one (it is beta, not yet introduced); and u, w, V are not defined in the unit. **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it). **Routed to P1** (not edited here).
- "**Derived.** *Hypotheses.* A1, A2, A3; $w\in\Delta$." Terms: A3, Delta. A3 is never stated (A1 and A2 are glossed once); the simplex symbol is not introduced. **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it). **Routed to P1** (not edited here).
- "**Derived.** *Hypotheses.* A2; R1 for the facet-normal reading; $w$ minimizes $J_\tau$ on $\Delta$." Terms: R1, "facet-normal reading", J_tau. None is defined here or in the Glossary. **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it). **Routed to P1** (not edited here).
- "Balanced hard-support geometry does not imply an interior minimizer at finite $\tau$." Terms: "balanced hard-support geometry", tau. Neither is defined; tau is never named (the Glossary has "fit temperature" but does not tie it to tau). **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it). **Routed to P1** (not edited here).
- "$\nabla J_\tau=U^\top p$, $p=\mathrm{softmax}(\tau Uw)$. With $g=\nabla J_\tau(w)$, $\lambda=w\cdot g$: $g_j\ge\lambda$ and $w_j(g_j-\lambda)=0$." Terms: U, p, J_tau. U (the log-metric matrix?) and J_tau (the fit objective) are never defined; "support weights" is in the Glossary but p is not tied to it. **Disposition: no change** (standard vocabulary at the reader level the paper assumes (Boyd and Vandenberghe; scikit-learn)). **Routed to P1** (not edited here).
- "**Derived.** *Hypotheses.* A3; F5 (the maximum is attained)." Terms: F5, N, s_i. The labels are not defined, and s_i and N appear without introduction in L5. **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it). **Routed to P1** (not edited here).
- "**Derived.** *Hypotheses.* A2, A3, A5, I5 (moment generating functions multiply); a population identity, with no consistency claim." Terms: A5, epsilon, sigma. The noise model behind A5 is not given, so the Gaussian setting is unstated. **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it). **Routed to P1** (not edited here).
- "**Derived.** *Hypotheses.* A7; I6 ($QQ^\top=I$ implies $Q^\top Q=I$)." Terms: A7, Z, B, Q. The Helmert-type matrix B and chart coordinates Z are not defined in the unit; the Glossary's "chart" does not give the construction. **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it). **Routed to P1** (not edited here).
- "**Derived.** *Hypotheses.* A2, A4: $\log m_j=\alpha_j\log(a_j+s_j)+b_j$, $\alpha_j\neq0$." Terms: s_j, alpha_j, b_j. The offsets and scales of the conditioning are not named; "log-affine conditioning" is not in the Glossary (only "conditioning"). **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it). **Routed to P1** (not edited here).
- "**Derived.** *Hypotheses.* A1, A6; F10 (the maximum is attained) for the limit." Terms: A6, F10. Undefined labels. **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it). **Routed to P1** (not edited here).
- "$\Phi_K(u+c\mathbf 1)=\Phi_K(u)+c$; $\Phi_1=w_1\cdot u-\beta_1$; $\max_kx_k\le\Phi_K\le\max_kx_k+(\log K)/\kappa$ with $x_k=w_k\cdot u-\beta_k$; $e^{\kappa\Phi_K}$ is a posynomial in $m$." Terms: Phi_K, kappa. kappa is not defined (it is presumably the "term temperature", but the unit does not say), and Phi_K is not introduced. **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it). **Routed to P1** (not edited here).
- "A maximizer of $V$ is weakly efficient in all $d$ metrics, and efficient when every $w_j>0$; at $K>1$, $\kappa=\infty$, through an active term." Terms: "weakly efficient", "active term". "Weakly efficient" is a multiobjective term not in the Glossary; "active term" is not either. **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it). **Routed to P1** (not edited here).
- "For $u'=u+\delta$, $\delta\ge0$, the gain $\sum_jw_j\delta_j$ is a sum of nonnegative terms; take the contrapositive. That only the log-convex part of a front is reached by some $w$ is our statement, not a cited one." Terms: "log-convex part of a front", "front". "Front" is not defined (the Glossary has "Pareto boundary"), and the claim is not explained. **Disposition: no change** (standard vocabulary at the reader level the paper assumes (Boyd and Vandenberghe; scikit-learn)). **Routed to P1** (not edited here).
- "Simplex exponents turn the shift into $c$ in every term; the bounds are the squeeze of {prf:ref}`thm-lme`; each term is a monomial (I4: log-sum-exp of affine functions is GP-compatible)." Terms: I4, "GP-compatible". The Glossary has "geometric program" but not "GP-compatible" or what I4 asserts beyond its gloss. **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it). **Routed to P1** (not edited here).


### List 2. Where a Glossary term would say it shorter or more exactly

- "**Derived.** *Hypotheses.* A1, A2; $w_j\neq0$; the frontier is the hyperplane $\{w\cdot u=\beta\}$." Term: facet. "The frontier" is, per the Glossary, ambiguous among three objects; here it is one flat piece, i.e. a facet. **Disposition: glossary term** (use the Glossary term the reader names). **Routed to P1** (not edited here).
- "Improving metric $j$ alone by $V^{-1/w_j}$, or every metric by $1/V$, reaches $V=1$." Term: improvement factor. The Glossary term names exactly the first factor. **Disposition: glossary term** (use the Glossary term the reader names). **Routed to P1** (not edited here).
- "$Z(u+c\mathbf 1)=Z(u)$ and $u=B^\top Z+\frac1d(\mathbf 1^\top u)\mathbf 1$: the map between $u$ and (position, log-scale) is a bijection, and $Q=[B;\mathbf 1^\top/\sqrt d]$ is orthogonal." Term: position along the frontier (and chart). "Position" is the Glossary's other d - 1 chart coordinates; the Glossary term would anchor it. **Disposition: glossary term** (use the Glossary term the reader names). **Routed to P1** (not edited here).
- "A maximizer of $V$ is weakly efficient in all $d$ metrics, and efficient when every $w_j>0$; at $K>1$, $\kappa=\infty$, through an active term." Terms: Pareto boundary (for "efficient"), term temperature (for "kappa=infinity"), assignment/dominant term (for "active term"). **Disposition: glossary term** (use the Glossary term the reader names). **Routed to P1** (not edited here).
- "With several terms, $V_K$ is the $1/\kappa$ power of a posynomial and its logarithm lies within $(\log K)/\kappa$ of its largest term (L10); a maximizer of $V$ is Pareto-efficient, and the converse is not claimed (L11)." Terms: term temperature (for kappa), assignment (for "largest term"), Pareto boundary (for "Pareto-efficient"); also "generalized posynomial", since V_K is in that class, not a posynomial itself. **Disposition: add to avoid** (the phrase is withdrawn by WP10 Amendment 4 (R-33, R-34, R-37)). **Routed to P1** (not edited here).
- "$\frac{d^2}{dt^2}J_\tau(w+tv)|_0=\tau\mathrm{Var}_p(v\cdot u)\ge0$: $J_\tau$ is convex, not claimed strictly." Term: support weights for p; fit temperature for tau. **Disposition: glossary term** (use the Glossary term the reader names). **Routed to P1** (not edited here).
- "Two results say what the fitted numbers mean: the soft maximum of Gaussian noise has a closed form (L6), and along a facet the exponents are elasticities and give the improvement factors to $V=1$ (L7)." Term: exponent vector for "the exponents" (used throughout the unit in the plural). **Disposition: glossary term** (use the Glossary term the reader names). **Routed to P1** (not edited here).


### List 3a. Terms of art that plain words would serve

- "$J_\tau(w;U+c\mathbf 1^\top)=J_\tau(w;U)+c$: $\beta$ moves by $c$ and $w^*$ is unchanged." together with "the log-mean-exp is shift-equivariant" (the sentence "Weights summing to one shift every score by $c$, and the log-mean-exp is shift-equivariant."): "shift-equivariant" -> "moves by the same shift". **Disposition: plain words** (replace with the plain words the reader names). **Routed to P1** (not edited here).
- "That only the log-convex part of a front is reached by some $w$ is our statement, not a cited one.": "log-convex part of a front" -> "the part of the trade-off curve that bulges outward the right way for a weighted sum to reach it". **Disposition: plain words** (replace with the plain words the reader names). **Routed to P1** (not edited here).
- "**Derived.** *Hypotheses.* A2, A3, A5, I5 (moment generating functions multiply); a population identity, with no consistency claim.": "population identity, with no consistency claim" -> "true for the underlying distribution; not claimed to hold for the fitted estimate". **Disposition: plain words** (replace with the plain words the reader names). **Routed to P1** (not edited here).
- "$Z(u+c\mathbf 1)=Z(u)$ and $u=B^\top Z+\frac1d(\mathbf 1^\top u)\mathbf 1$: the map between $u$ and (position, log-scale) is a bijection, and $Q=[B;\mathbf 1^\top/\sqrt d]$ is orthogonal.": "bijection" -> "one-to-one and reversible". **Disposition: plain words** (replace with the plain words the reader names). **Routed to P1** (not edited here).
- "The chart is a reversible rewriting of the log-metrics (L8), and under log-affine conditioning the pull-back to attributes is exact (L9).": "pull-back to attributes" -> "rewriting the result in terms of the original attributes"; "log-affine conditioning" -> "conditioning by a log-linear rescaling plus offset". **Disposition: plain words** (replace with the plain words the reader names). **Routed to P1** (not edited here).
- "Balanced hard-support geometry does not imply an interior minimizer at finite $\tau$.": "balanced hard-support geometry" -> say what is balanced (e.g. "several designs tying for the maximum with the weights split evenly"). **Disposition: plain words** (replace with the plain words the reader names). **Routed to P1** (not edited here).


### List 3b. Sentences with three or more terms of art together

- "The one-facet fit has simplex optimality conditions (L3), is convex (L4), and uses the log-mean-exp, which differs from the log-sum-exp by a constant (L5)." Terms: facet, simplex, optimality conditions, log-mean-exp, log-sum-exp. **Disposition: no change** (a definition, statement or proof step where the terms are the content; the unresolved ones are items in List 1 and the shorter ones items in Lists 2 and 3a). **Routed to P1** (not edited here).
- "Two results say what the fitted numbers mean: the soft maximum of Gaussian noise has a closed form (L6), and along a facet the exponents are elasticities and give the improvement factors to $V=1$ (L7)." Terms: soft maximum, facet, exponents, elasticities, improvement factors. **Disposition: no change** (a definition, statement or proof step where the terms are the content; the unresolved ones are items in List 1 and the shorter ones items in Lists 2 and 3a). **Routed to P1** (not edited here).
- "The chart is a reversible rewriting of the log-metrics (L8), and under log-affine conditioning the pull-back to attributes is exact (L9)." Terms: chart, log-metrics, log-affine conditioning, pull-back, attributes. **Disposition: no change** (a definition, statement or proof step where the terms are the content; the unresolved ones are items in List 1 and the shorter ones items in Lists 2 and 3a). **Routed to P1** (not edited here).
- "With several terms, $V_K$ is the $1/\kappa$ power of a posynomial and its logarithm lies within $(\log K)/\kappa$ of its largest term (L10); a maximizer of $V$ is Pareto-efficient, and the converse is not claimed (L11)." Terms: posynomial, kappa, term, Pareto-efficient, maximizer. **Disposition: no change** (a definition, statement or proof step where the terms are the content; the unresolved ones are items in List 1 and the shorter ones items in Lists 2 and 3a). **Routed to P1** (not edited here).
- "A maximizer of $V$ is weakly efficient in all $d$ metrics, and efficient when every $w_j>0$; at $K>1$, $\kappa=\infty$, through an active term." Terms: weakly efficient, efficient, kappa, active term, metrics. **Disposition: no change** (a definition, statement or proof step where the terms are the content; the unresolved ones are items in List 1 and the shorter ones items in Lists 2 and 3a). **Routed to P1** (not edited here).
- "Simplex exponents turn the shift into $c$ in every term; the bounds are the squeeze of {prf:ref}`thm-lme`; each term is a monomial (I4: log-sum-exp of affine functions is GP-compatible)." Terms: simplex, exponents, term, monomial, log-sum-exp, GP-compatible. **Disposition: no change** (a definition, statement or proof step where the terms are the content; the unresolved ones are items in List 1 and the shorter ones items in Lists 2 and 3a). **Routed to P1** (not edited here).


## Unit 17: paper/paper.ipynb :: Preliminaries and notation

Density 7.2 terms of art per 100 words (30/418); staged text `paper_preliminaries-and-notation.txt`.


### List 1. Terms unresolved from the unit and the Glossary

- "A3: $\tau>0$." Term: $\tau$. The symbol is never defined in the unit, and the Glossary has "fit temperature" and "term temperature" but does not say which one $\tau$ is. **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it).
- "A6: $\kappa>0$ and each term's exponents lie on the simplex." Term: $\kappa$. It appears in neither the unit nor the Glossary. **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it).
- "A4: conditioning is log-affine and invertible." Term: log-affine. The Glossary names LogAffinePreconditioner but does not define log-affine, so the assumption cannot be read. **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it).
- "A7: the chart's basis is orthonormal and sums to zero." Terms: chart's basis, sums to zero. The Glossary defines "chart" as a reversible transformation but not its basis. It is also unclear what sums to zero (the basis vectors, or the coordinates). **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it).
- "A5: noise, where used, is Gaussian in log space." Term: noise. The unit does not say noise in what (the attributes, the metrics, the fit residual). **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it).
- "{numref}`Section %s <sect-methods>` adds the regularity conditions R1 and R2." Terms: R1, R2. The conditions are not stated here or in the Glossary, so A1 to A7 and R1, R2 together cannot be assessed. **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it).
- "Results are read in light of the gaps ledger in {ref}`Appendix E <appendix-e>`, which records for each place where the map and the territory part the assumption that bridges it, what cannot be proved, the evidence on sensitivity and what that means for reading the result." Term: gaps ledger. It is not in the Glossary and is defined only by this long relative clause. **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it).
- "The fitted reference surface is $V=1$ at finite $\tau$, where the posynomial equals one; some designs lie beyond it." Terms: $V$, $K$-term posynomial. The unit never says what $V$ is (the Glossary has "invariant value" but does not tie the symbol $V$ to it) or what posynomial it is, since the exponents and coefficients have not been introduced. **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it).
- "A2: exponents lie on the simplex." Term: exponents. The unit gives no object that has exponents; the Glossary's "exponent vector" is per term, which has not been introduced. **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it).


### List 2. Where a Glossary term would say it shorter or more exactly

- "The supporting envelope is the $\tau=\infty$ fit, which none exceeds." Term: fit temperature (infinite temperature, the exact maximum). The Glossary phrase says what $\tau=\infty$ means. **Disposition: glossary term** (use the Glossary term the reader names).
- "The fitted reference surface is $V=1$ at finite $\tau$, where the posynomial equals one; some designs lie beyond it." Term: novelty (how far a design lies beyond the fitted reference surface), or energy differential (positive beyond). It names the "beyond" relation. **Disposition: glossary term** (use the Glossary term the reader names).
- "A term, a monomial and a facet are one object: the term of the posynomial, the product of powers, the flat piece in log space." Terms: monomial and log-metrics. The Glossary defines a monomial as a hyperplane in log-metrics, which is more exact than "product of powers". **Disposition: glossary term** (use the Glossary term the reader names).
- "A5: noise, where used, is Gaussian in log space." Term: log-metrics. It names the space where every fit happens. **Disposition: glossary term** (use the Glossary term the reader names).
- "With $N$ designs and $d$ metrics, $M\in\mathbb{R}^{N\times d}_{>0}$ is the table of metrics, $U=\log M$ has rows $u_i$, and $\Delta$ is the probability simplex in $\mathbb{R}^d$." Terms: number of designs, number of metrics, log-metrics. $N$, $d$ and $U$ are the Glossary's number of designs, number of metrics and log-metrics, and the Glossary does not link the symbols to the terms. **Disposition: glossary term** (use the Glossary term the reader names).
- "The Pareto boundary is the nondominated set of the attainable set, a property of the system." Term: Pareto boundary. The Glossary says "the nondominated points of the attainable set", which is the same wording, so there is no gain. **Disposition: glossary term** (use the Glossary term the reader names). **To the driver** (the reader reports a clash that touches a term's meaning).


### List 3a. Terms of art that plain words would serve

- "Stages 3 and 4, identification and analysis, are the method." Term: identification. Plain words: fitting (the Glossary and the conformance notes say fit). **Disposition: plain words** (replace with the plain words the reader names).
- "The Pareto boundary is the nondominated set of the attainable set, a property of the system." Terms: nondominated set, attainable set. Plain words: designs that no other achievable design beats on every metric. **Disposition: plain words** (replace with the plain words the reader names).
- "Stage 1 evaluates, and **the evaluation is a black box to the method: a simulator behind a system model, a physical test, or a human assessment.**" Term: black box. Plain words: the method sees only inputs and outputs. **Disposition: plain words** (replace with the plain words the reader names).
- "Results are read in light of the gaps ledger in {ref}`Appendix E <appendix-e>`, which records for each place where the map and the territory part the assumption that bridges it, what cannot be proved, the evidence on sensitivity and what that means for reading the result." Terms: map and territory, gaps ledger. Plain words: a list of where the model and the real system differ. **Disposition: plain words** (replace with the plain words the reader names).
- "The cubesat model of {numref}`Section %s <sect-case-construction>` is one instance behind that abstraction, not part of the method, so the method stays relevant as tools move or where scoring comes from physical systems or human judgment." Term: abstraction. Plain words: one example of the evaluation step. **Disposition: plain words** (replace with the plain words the reader names).


### List 3b. Sentences with three or more terms of art together

- "The fitted reference surface is $V=1$ at finite $\tau$, where the posynomial equals one; some designs lie beyond it." Terms: fitted reference surface, $V$, finite $\tau$, posynomial. **Disposition: no change** (a definition, statement or proof step where the terms are the content; the unresolved ones are items in List 1 and the shorter ones items in Lists 2 and 3a).
- "A term, a monomial and a facet are one object: the term of the posynomial, the product of powers, the flat piece in log space." Terms: term, monomial, facet, posynomial, log space. **Disposition: no change** (a definition, statement or proof step where the terms are the content; the unresolved ones are items in List 1 and the shorter ones items in Lists 2 and 3a).
- "With $N$ designs and $d$ metrics, $M\in\mathbb{R}^{N\times d}_{>0}$ is the table of metrics, $U=\log M$ has rows $u_i$, and $\Delta$ is the probability simplex in $\mathbb{R}^d$." Terms: designs, metrics, table of metrics, log-metrics, probability simplex. **Disposition: no change** (a definition, statement or proof step where the terms are the content; the unresolved ones are items in List 1 and the shorter ones items in Lists 2 and 3a).
- "The Pareto boundary is the nondominated set of the attainable set, a property of the system." Terms: Pareto boundary, nondominated set, attainable set. **Disposition: no change** (a definition, statement or proof step where the terms are the content; the unresolved ones are items in List 1 and the shorter ones items in Lists 2 and 3a).
- "A7: the chart's basis is orthonormal and sums to zero." Terms: chart, basis, orthonormal, sums to zero. **Disposition: no change** (a definition, statement or proof step where the terms are the content; the unresolved ones are items in List 1 and the shorter ones items in Lists 2 and 3a).
- "The supporting envelope is the $\tau=\infty$ fit, which none exceeds." Terms: supporting envelope, $\tau$, fit. **Disposition: no change** (a definition, statement or proof step where the terms are the content; the unresolved ones are items in List 1 and the shorter ones items in Lists 2 and 3a).
- "Results are read in light of the gaps ledger in {ref}`Appendix E <appendix-e>`, which records for each place where the map and the territory part the assumption that bridges it, what cannot be proved, the evidence on sensitivity and what that means for reading the result." Terms: gaps ledger, map and territory, assumption, sensitivity. **Disposition: no change** (a definition, statement or proof step where the terms are the content; the unresolved ones are items in List 1 and the shorter ones items in Lists 2 and 3a).


## Unit 18: docs/user-guide/overview.md

Density 7.1 terms of art per 100 words (27/381); staged text `docs_user-guide_overview.md.txt`.


### List 1. Terms unresolved from the unit and the Glossary

- "The package answers with tensions, not variance." Term: tension. Used as the central noun but defined nowhere (the Glossary only uses it inside "participation threshold" and "tension_report"); a reader cannot tell what a tension is as an object. **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it).
- "After a one-time normalization V = 1 is the fitted reference surface, V below 1 is inside it and V above 1 is beyond what the table reached." Term: one-time normalization. Normalization of what, by what rule, is not stated and is not in the Glossary. **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it).
- "Condition the attributes into metrics: positive, larger-is-better, comparable spread." Term: comparable spread. Spread is not defined (variance? range? scale?) and the Glossary entry for conditioning does not say. **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it).
- "a stopping record, [`termination_` and `conditioning_`](termination.md), saying how far to trust the fit." Term: conditioning_. The Glossary's "conditioning" is the analyst's step and "conditioning of the exponents" is a Hessian eigenvalue; the trailing-underscore attribute matches neither by name, so what it holds is unresolved. **Disposition: no change** (standard vocabulary at the reader level the paper assumes (Boyd and Vandenberghe; scikit-learn)).
- "The answer is one weight per metric, the weights sum to one, and the metrics with non-negligible weight are the ones that contend." Term: weight (versus exponent vector). The unit says "weights", the Glossary says "exponent vector" and "support weights" (a different thing: weights of designs); a reader cannot tell which the unit means. **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it).


### List 2. Where a Glossary term would say it shorter or more exactly

- "The answer is one weight per metric, the weights sum to one, and the metrics with non-negligible weight are the ones that contend." Terms: exponent vector, contending set. Replaces "one weight per metric, sum to one" and "metrics ... that contend" with the two defined names. **Disposition: glossary term** (use the Glossary term the reader names).
- "The weights define a score V, a weighted geometric mean of the metrics." Term: invariant value. The unit never names V; the Glossary does, with the doubling property. **Disposition: glossary term** (use the Glossary term the reader names).
- "They are found from the data, so you need not know in advance which dilemma or trilemma your problem holds." Term: n-lemma. Says "dilemma or trilemma" where the Glossary has the general term. **Disposition: glossary term** (use the Glossary term the reader names).
- "Because V scales with the metrics, it reads as a factor of improvement." Term: invariant value. The Glossary entry states exactly this property. **Disposition: glossary term** (use the Glossary term the reader names).
- "the weights and the metrics that participate;" Term: contending set (and participation threshold for what "participate" means). **Disposition: glossary term** (use the Glossary term the reader names).
- "how much one metric alone would need to improve to reach the surface;" Term: improvement factor. **Disposition: glossary term** (use the Glossary term the reader names).
- "a stopping record, [`termination_` and `conditioning_`](termination.md), saying how far to trust the fit." Term: termination status (the unit's "stopping record"). **Disposition: glossary term** (use the Glossary term the reader names).
- "a novelty score and candidate white space;" Terms: novelty, white space are used but the sentence "where the table is empty" earlier ("and where the table is empty") is the same idea in plain words. **Disposition: glossary term** (use the Glossary term the reader names).
- "which numbers pull against each other, at what elasticity, where the edge of the evaluated designs lies, and where the table is empty." Terms: Pareto boundary or supporting envelope (for "edge of the evaluated designs"), white space (for "where the table is empty"). The Glossary distinguishes the edge objects exactly; the unit's phrase does not. **Disposition: glossary term** (use the Glossary term the reader names).


### List 3a. Terms of art that plain words would serve

- "the metrics that participate" (also "the ones that contend"): plain words "the metrics that carry weight" or "the metrics that trade off". **Disposition: plain words** (replace with the plain words the reader names).
- "its energy differential (level offset) to the fitted reference surface": two names for one thing; plain words "how far inside or beyond the surface it sits". **Disposition: plain words** (replace with the plain words the reader names).
- "After a one-time normalization": plain words "after rescaling once". **Disposition: plain words** (replace with the plain words the reader names).
- "at what elasticity": plain words "at what exchange rate" (percent given up per percent gained). **Disposition: add to avoid** (the phrase is withdrawn by WP10 Amendment 4 (R-33, R-34, R-37)).
- "The package answers with tensions, not variance.": plain words "the package finds what pulls against what, not where the data spread". **Disposition: plain words** (replace with the plain words the reader names).


### List 3b. Sentences with three or more terms of art together

- "The weights define a score V, a weighted geometric mean of the metrics." Terms: weights, score V, weighted geometric mean, metrics. **Disposition: plain words** (introductory page: spread the terms over more words).
- "After a one-time normalization V = 1 is the fitted reference surface, V below 1 is inside it and V above 1 is beyond what the table reached." Terms: normalization, V, fitted reference surface. **Disposition: plain words** (introductory page: spread the terms over more words).
- "PCA finds the directions in which the data spread; this method finds the positive combination of the metrics along which the data stop, the binding constraint among metrics that are all better when larger." Terms: PCA, positive combination, binding constraint, metrics. **Disposition: plain words** (introductory page: spread the terms over more words).
- "for each design, its energy differential (level offset) to the fitted reference surface and its position along the surface;" Terms: energy differential, level offset, fitted reference surface, position along the surface. **Disposition: plain words** (introductory page: spread the terms over more words).
- "a stopping record, [`termination_` and `conditioning_`](termination.md), saying how far to trust the fit." Terms: stopping record, termination_, conditioning_, fit. **Disposition: plain words** (introductory page: spread the terms over more words).


## Unit 19: docs/user-guide/conditioning.md

Density 6.3 terms of art per 100 words (38/602); staged text `docs_user-guide_conditioning.md.txt`.


### List 1. Terms unresolved from the unit and the Glossary

- "The cheap diagnostic is the sign of the pulled-back exponent below." Term: pulled-back exponent. Not in the Glossary; "pull-back" is not defined where first used. **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it).
- "The pulled-back exponent on a raw attribute is `w_j * alpha_j`." Terms: w_j, alpha_j. Neither symbol is defined in the unit or Glossary (which is the weight, which is the exponent, of what). **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it).
- "The reason to scale is the temperature of the next page: it is quoted in inverse log-spread, so equal log-spread makes one temperature mean the same for every column." Terms: inverse log-spread, temperature, "next page". Log-spread is undefined; "temperature" is only resolved by guessing fit temperature, and "next page" points outside the unit. **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it).
- "For a fitted single-term estimator, `frontier_in_original_units(estimator, preconditioner)` returns `exponents_orig`, `log_const` and `shift`." Terms: log_const, exponents_orig. Not defined; log_const is not tied to the Glossary's fitted reference surface or invariant value. **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it).
- "It fixes what V = 1 means in practice." Term: V. The unit never defines V (the Glossary defines invariant value and the level V = 1 only indirectly); a first-time reader cannot tell what V is here. **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it).
- "The reference point is the attribute value that maps to metric 1; it is the centre removed by the scaler and stored as `log_offset_`." Term: reference point. Not in the Glossary, and easily confused with the Glossary's fitted reference surface. **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it).


### List 2. Where a Glossary term would say it shorter or more exactly

- "The package supplies `LogAffinePreconditioner`, which implements the family of maps the method allows, and `frontier_in_original_units`, which reports the fitted surface back in the units you started with." Term: fitted reference surface. "Fitted surface" is not a Glossary name, and the Glossary says "frontier" and its neighbours are ambiguous. **Disposition: glossary term** (use the Glossary term the reader names).
- "The map from attributes to metrics is yours to choose, because it is part of the question you ask." Term: conditioning. The Glossary defines exactly this step; the sentence circumlocutes it. **Disposition: glossary term** (use the Glossary term the reader names).
- "A wrong sign is not detected: the fit finds a surface for the wrongly oriented metric." Term: fitted reference surface (or supporting envelope, depending on temperature). "A surface" is unspecific. **Disposition: glossary term** (use the Glossary term the reader names).
- "Evaluate `log_const + exponents_orig @ np.log(X + shift)` to get log V for raw rows." Term: energy differential (log of the invariant value, relative to the fitted reference surface). "log V" names it less exactly. **Disposition: glossary term** (use the Glossary term the reader names).
- "so the fitted scale describes feasible designs only." Term: log-metrics / chart. "Fitted scale" is not a Glossary term. **Disposition: glossary term** (use the Glossary term the reader names).
- "The function needs a single-term fit; a multi-term fit is not a monomial in the attributes." Terms: number of terms, posynomial. "Single-term" and "multi-term" would be said exactly as number of terms equal to 1 or greater than 1. **Disposition: glossary term** (use the Glossary term the reader names).


### List 3a. Terms of art that plain words would serve

- "The cheap diagnostic is the sign of the pulled-back exponent below." Term: pulled-back exponent. Plain words: "the exponent restated on the raw attribute". **Disposition: plain words** (replace with the plain words the reader names).
- "it is quoted in inverse log-spread" Term: inverse log-spread. Plain words: "in units of one over the spread of the log values". **Disposition: plain words** (replace with the plain words the reader names).
- "so the fitted scale describes feasible designs only." Term: fitted scale. Plain words: "the scale learned from the data". **Disposition: plain words** (replace with the plain words the reader names).
- "A shift is a decision about where the scale begins" Term: shift / where the scale begins. Plain words: "the constant added before taking logs". **Disposition: plain words** (replace with the plain words the reader names).
- "The map from attributes to metrics is yours to choose" Term: map. Plain words: "the conversion". **Disposition: plain words** (replace with the plain words the reader names).


### List 3b. Sentences with three or more terms of art together

- "The reason to scale is the temperature of the next page: it is quoted in inverse log-spread, so equal log-spread makes one temperature mean the same for every column." Terms: temperature, inverse log-spread, log-spread, scaler. **Disposition: no change** (a definition, statement or proof step where the terms are the content; the unresolved ones are items in List 1 and the shorter ones items in Lists 2 and 3a).
- "The estimator tolerates zero metrics: such a row has V = 0 and no support weight, and its chart coordinates are `nan`." Terms: metrics, V, support weight, chart coordinates. **Disposition: no change** (a definition, statement or proof step where the terms are the content; the unresolved ones are items in List 1 and the shorter ones items in Lists 2 and 3a).
- "For a fitted single-term estimator, `frontier_in_original_units(estimator, preconditioner)` returns `exponents_orig`, `log_const` and `shift`." Terms: single-term, frontier_in_original_units, exponents_orig, log_const. **Disposition: no change** (a definition, statement or proof step where the terms are the content; the unresolved ones are items in List 1 and the shorter ones items in Lists 2 and 3a).
- "The reference point is the attribute value that maps to metric 1; it is the centre removed by the scaler and stored as `log_offset_`." Terms: reference point, metric, scaler, log_offset_. **Disposition: no change** (a definition, statement or proof step where the terms are the content; the unresolved ones are items in List 1 and the shorter ones items in Lists 2 and 3a).
- "The pulled-back exponent on a raw attribute is `w_j * alpha_j`." Terms: pulled-back exponent, attribute, w_j, alpha_j. **Disposition: no change** (a definition, statement or proof step where the terms are the content; the unresolved ones are items in List 1 and the shorter ones items in Lists 2 and 3a).


## Unit 20: site/index.html

Density 6.0 terms of art per 100 words (34/563); staged text `site_index.html.txt`.


### List 1. Terms unresolved from the unit and the Glossary

- "PCA explains variance; this explains tensions." Term: tensions. Used as the method's headline claim, but neither defined in the unit nor in the Glossary (only "participation threshold" mentions "the tension"). **Disposition: no change** (standard vocabulary at the reader level the paper assumes (Boyd and Vandenberghe; scikit-learn)).
- "The method belongs in unsupervised learning and feature engineering beside PCA: kin rather than a substitute, and the two chain (the tension report already runs PCA on the near-frontier chart coordinates)." Terms: tension report, near-frontier, chart coordinates. The report's contents are never stated, and "near-frontier" is not in the Glossary. **Disposition: no change** (standard vocabulary at the reader level the paper assumes (Boyd and Vandenberghe; scikit-learn)).
- "Four boxes use that fit: the chart (each design becomes a position along the frontier and a log V), the elasticities between the metrics that contend, the correction for noise, and the pull-back to your raw attributes." Terms: correction for noise, pull-back. Neither is defined here or in the Glossary, and the reader cannot tell what they compute. **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it).
- "The single-term core fits the weights and an offset to your designs as one convex problem." Terms: single-term core, offset. The Glossary has "level offset" (the energy differential), which is a different thing, and "single-term core" is not defined. **Disposition: no change** (standard vocabulary at the reader level the paper assumes (Boyd and Vandenberghe; scikit-learn)).
- "The lower boxes extend the model to several facets, relate it to the Pareto boundary, and give the multi-facet algorithm its guarantees." Terms: multi-facet algorithm, guarantees. The algorithm is not described, and the guarantees are not named in the unit (the Glossary's "termination status" is not linked to them). **Disposition: no change** (standard vocabulary at the reader level the paper assumes (Boyd and Vandenberghe; scikit-learn)).
- "What trades against what depends on where a design sits." Term: trade space (also used in "one part of the trade space"). Only appears in the Glossary as "the dimension of the trade space"; it is never itself defined. **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it).


### List 2. Where a Glossary term would say it shorter or more exactly

- "The foundation box is the invariant form: a weighted geometric mean V of the metrics, whose level V = 1 is the fitted reference surface and whose logarithm is the energy differential." Terms: invariant value (for "a weighted geometric mean V of the metrics"), energy differential (the Glossary's own wording for "whose logarithm"; the Glossary defines it as the log of the invariant value, relative to the fitted reference surface). "Invariant form" is also not the Glossary's name for V. **Disposition: glossary term** (use the Glossary term the reader names).
- "Its unit is the n-lemma, a power-weighted product of the metrics that names which of them compete on one part of the trade space." Terms: n-lemma, contending set. The Glossary gives the n-lemma as how many metrics contend on a facet, and the metrics that contend as the "contending set"; "power-weighted product" is unused and the sentence blurs the count with the set. **Disposition: glossary term** (use the Glossary term the reader names).
- "Each dot is an evaluated design, placed by which metric it favours; the coloured dots are at the frontier." Terms: frontier, Pareto boundary / supporting envelope. The Glossary says "frontier" is one of three objects; the sentence should name which. **Disposition: glossary term** (use the Glossary term the reader names).
- "...the chart (each design becomes a position along the frontier and a log V)..." Term: energy differential for "a log V". **Disposition: glossary term** (use the Glossary term the reader names).
- "The method told from evaluated designs to the frontier, its tensions and its gaps." Term: frontier (should say fitted reference surface, supporting envelope or Pareto boundary); also "tensions" could say contending set / n-lemma. **Disposition: glossary term** (use the Glossary term the reader names).
- "A scikit-learn-compatible estimator for the frontier, with an invertible log-ratio chart, tension reports and plotting helpers." Terms: chart ("invertible" is already in the Glossary's "reversible transformation"; "log-ratio chart" is not the Glossary's name), frontier (which object). **Disposition: glossary term** (use the Glossary term the reader names).


### List 3a. Terms of art that plain words would serve

- "Trade studies are usually decided from documents and tables, where the detail of the evaluated designs is lost, and the alternatives are bespoke or opaque." Term: bespoke. Plain words: custom-built, one-off. **Disposition: plain words** (replace with the plain words the reader names).
- "A model-based method has to clear a bar before a decision-maker can trust it: it has to show its reasoning, say where the data do not reach, and let the analysis be rerun." Term: clear a bar. Plain words: meet a standard. **Disposition: plain words** (replace with the plain words the reader names).
- "PCA explains variance; this explains tensions." Term: tensions. Plain words: which metrics compete. **Disposition: plain words** (replace with the plain words the reader names).
- "Each box carries a badge, derived, checked numerically or open; the red box lists the open questions." Term: badge. Plain words: label. **Disposition: plain words** (replace with the plain words the reader names).
- "The foundation box is the invariant form: ..." Term: invariant form. Plain words: the weighted geometric mean of the metrics, or the invariant value if that is the intended name. **Disposition: plain words** (replace with the plain words the reader names).
- "...the pull-back to your raw attributes." Term: pull-back. Plain words: mapping back to your original attributes. **Disposition: plain words** (replace with the plain words the reader names).


### List 3b. Sentences with three or more terms of art together

- "The method belongs in unsupervised learning and feature engineering beside PCA: kin rather than a substitute, and the two chain (the tension report already runs PCA on the near-frontier chart coordinates)." Terms: unsupervised learning, feature engineering, PCA, tension report, near-frontier, chart coordinates. **Disposition: plain words** (introductory page: spread the terms over more words).
- "The foundation box is the invariant form: a weighted geometric mean V of the metrics, whose level V = 1 is the fitted reference surface and whose logarithm is the energy differential." Terms: invariant form, weighted geometric mean, metrics, fitted reference surface, energy differential. **Disposition: plain words** (introductory page: spread the terms over more words).
- "Four boxes use that fit: the chart (each design becomes a position along the frontier and a log V), the elasticities between the metrics that contend, the correction for noise, and the pull-back to your raw attributes." Terms: chart, position along the frontier, log V, elasticities, metrics, contend, pull-back, attributes. **Disposition: plain words** (introductory page: spread the terms over more words).
- "Its unit is the n-lemma, a power-weighted product of the metrics that names which of them compete on one part of the trade space." Terms: n-lemma, power-weighted product, metrics, trade space. **Disposition: plain words** (introductory page: spread the terms over more words).
- "The single-term core fits the weights and an offset to your designs as one convex problem." Terms: single-term core, weights, offset, convex problem. **Disposition: plain words** (introductory page: spread the terms over more words).
- "The lower boxes extend the model to several facets, relate it to the Pareto boundary, and give the multi-facet algorithm its guarantees." Terms: facets, Pareto boundary, multi-facet algorithm, guarantees. **Disposition: plain words** (introductory page: spread the terms over more words).
- "A scikit-learn-compatible estimator for the frontier, with an invertible log-ratio chart, tension reports and plotting helpers." Terms: estimator, frontier, log-ratio chart, tension reports. **Disposition: plain words** (introductory page: spread the terms over more words).
- "The black arrow is the same step in each pane: a design's energy differential to the fitted reference surface." Terms: energy differential, fitted reference surface (plus "step"/"pane" figure references that the reader cannot see in the text); two terms, borderline. **Disposition: plain words** (introductory page: spread the terms over more words).


## Unit 21: docs/getting-started.md

Density 6.0 terms of art per 100 words (21/348); staged text `docs_getting-started.md.txt`.


### List 1. Terms unresolved from the unit and the Glossary

- "The table below is synthetic: 300 designs scored on 3 metrics, all positive and larger-is-better, with a planted frontier." Terms: planted frontier. Why: "planted" is undefined, and the Glossary says frontier names one of three objects without saying which is planted. **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it).
- "`report.exponents` are the fitted weights at the working temperature; their ratios are the elasticities between the contending metrics (`report.elasticities`)." Terms: working temperature. Why: the Glossary has fit temperature, not working temperature, and the unit sets only `temperature=20.0`; the link between the two is not stated. **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it).
- "`report.contending_set` lists the metrics that contend at the edge of the table: here all three, an n-lemma with n = 3, which the report names a trilemma." Terms: edge of the table. Why: no table edge is defined (a table has rows, not an edge); the reader cannot tell what "at the edge" means. **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it).
- "From there the guide follows the order of a study: [fit](user-guide/fitting.md), [read the tensions](user-guide/tensions.md), [use the chart](user-guide/chart.md)." Terms: tensions. Why: "tension" is never defined in the unit; the Glossary mentions it only inside "participation threshold" and "tension_report". **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it).


### List 2. Where a Glossary term would say it shorter or more exactly

- "In the log plane of metrics 0 and 1 the designs lie on or just beyond a straight frontier, and the grey band marks those within 0.5 of it in log V:" Terms: log-metrics; fitted reference surface; energy differential (level offset). Why: "log plane", "straight frontier" and "within 0.5 in log V" are each a Glossary term stated more exactly (log-metrics; fitted reference surface; offset of 0.5 in energy differential). **Disposition: glossary term** (use the Glossary term the reader names).
- "`ts.transform(X)` is the chart, `d - 1` position coordinates plus that log V, and `ts.inverse_transform` undoes it." Terms: position along the frontier; energy differential. Why: "`d - 1` position coordinates" is the Glossary's "position along the frontier", and "that log V" is the energy differential already named in the previous sentence. **Disposition: glossary term** (use the Glossary term the reader names).
- "The idea is easiest to see with two of the metrics, where the model is a line." Terms: monomial; hyperplane in log-metrics. Why: "the model is a line" is the Glossary's monomial, a hyperplane in log-metrics, which becomes a line when d = 2. **Disposition: glossary term** (use the Glossary term the reader names).
- "Real attributes are rarely positive, larger-is-better and comparably scaled." Terms: metrics; conditioning. Why: "positive, larger-is-better" is the Glossary's definition of metrics, and the next sentence's "Turning them into metrics" is conditioning. **Disposition: glossary term** (use the Glossary term the reader names).
- "`fit` learned one exponent per metric, summing to one." Terms: exponent vector. Why: the Glossary's exponent vector (weights on the simplex over the metrics) says this in one term. **Disposition: glossary term** (use the Glossary term the reader names).


### List 3a. Terms of art that plain words would serve

- "`report.contending_set` lists the metrics that contend at the edge of the table: here all three, an n-lemma with n = 3, which the report names a trilemma." Terms: contend, n-lemma, trilemma. Plain words: "compete" or "trade off against each other"; "three-way trade-off". **Disposition: plain words** (replace with the plain words the reader names).
- "`report.exponents` are the fitted weights at the working temperature; their ratios are the elasticities between the contending metrics (`report.elasticities`)." Terms: elasticities. Plain words: "the rate at which one metric is given up for another". **Disposition: plain words** (replace with the plain words the reader names).
- "`ts.score_samples(X)` is the log of V for each design, the energy differential to the fitted reference surface: negative inside, positive beyond." Terms: energy differential, fitted reference surface. Plain words: "signed log distance from the fitted frontier curve". **Disposition: plain words** (replace with the plain words the reader names).
- "`ts.transform(X)` is the chart, `d - 1` position coordinates plus that log V, and `ts.inverse_transform` undoes it." Terms: chart. Plain words: "a re-coordinatized copy of the table". **Disposition: plain words** (replace with the plain words the reader names).
- "In the log plane of metrics 0 and 1 the designs lie on or just beyond a straight frontier, and the grey band marks those within 0.5 of it in log V:" Terms: log plane. Plain words: "the plot of the logs of metrics 0 and 1". **Disposition: plain words** (replace with the plain words the reader names).


### List 3b. Sentences with three or more terms of art together

- "`ts.score_samples(X)` is the log of V for each design, the energy differential to the fitted reference surface: negative inside, positive beyond." Terms: score_samples, log V, energy differential, fitted reference surface, inside/beyond. **Disposition: plain words** (introductory page: spread the terms over more words).
- "`ts.transform(X)` is the chart, `d - 1` position coordinates plus that log V, and `ts.inverse_transform` undoes it." Terms: transform, chart, position coordinates, log V, inverse_transform. **Disposition: plain words** (introductory page: spread the terms over more words).
- "`report.contending_set` lists the metrics that contend at the edge of the table: here all three, an n-lemma with n = 3, which the report names a trilemma." Terms: contending_set, contend, n-lemma, trilemma. **Disposition: plain words** (introductory page: spread the terms over more words).
- "`report.exponents` are the fitted weights at the working temperature; their ratios are the elasticities between the contending metrics (`report.elasticities`)." Terms: exponents, working temperature, elasticities, contending metrics. **Disposition: plain words** (introductory page: spread the terms over more words).
- "In the log plane of metrics 0 and 1 the designs lie on or just beyond a straight frontier, and the grey band marks those within 0.5 of it in log V:" Terms: log plane, frontier, beyond, band, log V. **Disposition: plain words** (introductory page: spread the terms over more words).


## Unit 22: paper/paper.ipynb :: Case analysis

Density 6.0 terms of art per 100 words (35/586); staged text `paper_case-analysis.txt`.


### List 1. Terms unresolved from the unit and the Glossary

- "At K = 1 the fit reports one tension at the balanced point ({numref}`Figure %s <fig-plane-1>`)." Terms: tension, balanced point. Neither is defined in the unit; the Glossary only mentions "tension" inside other entries (participation threshold), and "balanced point" appears nowhere. **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it).
- "The mean slack falls from 0.20 at K = 1 to 0.138 at K = 2 and 0.117 at K = 3, at the temperatures 38, 113 and 195; refitted at the K = 1 temperature it falls to 0.09 and 0.05 (<a href=\"supporting-material/#sub-d-15\" target=\"_self\" style=\"color:inherit;text-decoration:underline\">Appendix D.15</a>)." Term: mean slack. Not in the Glossary; the reader cannot tell what is being averaged or whether lower is better. **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it).
- "Mean slack falls with K by construction and cannot choose it: three facets is the analyst's choice; the finding: their sets differ." Term: mean slack (again), and "sets" (which sets, the contending sets). Slack is undefined, so "by construction" cannot be checked. **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it).
- "Log-metric planes of the K = 1 fit (primary regime), one per pair of the facet's largest exponents, with the near-frontier band." Terms: primary regime, near-frontier band. Neither is in the Glossary; "regime" is never defined in this unit, and the band's width is not given. **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it).
- "The same pipeline on the baseline regime separates the problem's contribution from the gains' ({numref}`Figure %s <fig-regimes-1>`)." Terms: baseline regime, the gains' contribution, pipeline. The text later calls the same regime "stock"; the unit never says what differs between the regimes. **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it).
- "The regimes return a 6-lemma and a 6-lemma sharing 3 metrics (control effort, pointing error and slew time); the primary regime alone has depth of discharge, energy balance and total mass, the stock regime alone eclipse reserve, power margin and settling time." Terms: primary regime, stock regime (also "baseline"). Regimes undefined; "baseline" and "stock" appear to be the same thing but this is not stated. **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it).
- "On 20 planted tables (400 rows, 4 metrics) the fit recovers all three facets to within 0.05 in 16, at the exact maximum and at temperature 50; the 4 failures have 5, 5, 6 and 11 frontier rows on their thinnest facet (<a href=\"supporting-material/#sub-d-14\" target=\"_self\" style=\"color:inherit;text-decoration:underline\">Appendix D.14</a>)." Terms: planted tables, "within 0.05" (distance in what?), frontier rows, thinnest facet. Planting is not explained and the error measure is unnamed. **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it).
- "Of 3 proposals, the predicted energy differential lies within the regressor's own band 1/tau = 0.0651 of the measured one for 3, and the predicted position within that band for 0; position errors run from 1.4 to 3.1 bands." Terms: tau, the regressor's own band, proposals. tau is not defined (the Glossary has fit temperature, but no symbol); "band" is used here with a different meaning than in "near-frontier band". **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it). **To the driver** (the reader reports a clash that touches a term's meaning).
- "Association among the near-frontier designs of each K = 3 facet (negative: tension)." Terms: association, tension. The statistic (correlation? rank?) is not named. **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it).
- "At K = 1 the exact-maximum fit has a 6-lemma across controls, power and energy, plus mass: total mass, slew time, energy balance, control effort, pointing error and depth of discharge contend, with working-temperature exponents from 0.09 to 0.24." Terms: working-temperature exponents. The Glossary has fit temperature and participation threshold but no "working temperature"; it is not said which temperature is the working one. **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it).
- "The 3 measured candidates have lowest energy differential -0.144 and highest -0.072 to -0.071, and 0 of them lie beyond the fitted reference surface." Terms: measured candidates. Unclear how candidates differ from the proposals in the next paragraph, and from the table rows. **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it).


### List 2. Where a Glossary term would say it shorter or more exactly

- "The K = 3 facets have contending sets (exact-maximum supports) of 6, 6 and 7 metrics; peak slew power, power margin and settling time are absent from the K = 1 set." Glossary term: n-lemma. "A 6-, 6- and 7-lemma" is shorter, and "exact-maximum supports" is a loose use of support (support weights / supporting envelope are the Glossary's terms). **Disposition: glossary term** (use the Glossary term the reader names).
- "Outlined: the contending set, the support of the exact-maximum fit; w is the fitted exponent, small for some members." Glossary terms: contending set, exponent vector. "Support of the exact-maximum fit" restates the Glossary definition of contending set; "fitted exponent" is the exponent vector's entry. **Disposition: glossary term** (use the Glossary term the reader names).
- "At K = 3 the tension separates into three facets with different contending sets: {numref}`Figure %s <fig-plane-3>` shows their envelope, {numref}`Figure %s <fig-chart-3>` places each design and {numref}`Figure %s <fig-tensions-3>` shows what trades off." Glossary term: supporting envelope. "Their envelope" is ambiguous among the Glossary's three frontier objects; name which one. **Disposition: glossary term** (use the Glossary term the reader names).
- "Mean slack falls with K by construction and cannot choose it: three facets is the analyst's choice; the finding: their sets differ." Glossary term: number of terms ("never selected by the fit"). Say "the number of terms is the analyst's choice". **Disposition: glossary term** (use the Glossary term the reader names).
- "Log-metric planes of the K = 3 fit with the near-frontier band; designs coloured by facet, lines the facets." Glossary terms: fit temperature, fitted reference surface. "Near-frontier band" is the finite-temperature band of the fitted reference surface; name it. **Disposition: glossary term** (use the Glossary term the reader names).
- "A regressor from configuration to chart coordinates predicts where proposals fall ({numref}`Figure %s <fig-predict-check-1>`); we then measure them." Glossary term: position along the frontier. "Where proposals fall" is the position along the frontier (or the chart coordinates); the sentence should use one. **Disposition: glossary term** (use the Glossary term the reader names).
- "Of 3 proposals, the predicted energy differential lies within the regressor's own band 1/tau = 0.0651 of the measured one for 3, and the predicted position within that band for 0; position errors run from 1.4 to 3.1 bands." Glossary terms: energy differential (used correctly), position along the frontier (for "predicted position"), fit temperature (for tau, if that is what tau is). **Disposition: glossary term** (use the Glossary term the reader names).
- "The 3 measured candidates have lowest energy differential -0.144 and highest -0.072 to -0.071, and 0 of them lie beyond the fitted reference surface." Glossary term: novelty ("how far a design lies beyond the fitted reference surface"). "0 lie beyond" is "none has novelty". **Disposition: glossary term** (use the Glossary term the reader names).
- "We read the case as the method asks: what contends, how, and where designs sit (tables: {ref}`Appendix D <appendix-d>`; digits that hold: {ref}`D.11 <sub-d-11>`)." Glossary terms: contending set (what contends), position along the frontier (where designs sit). **Disposition: glossary term** (use the Glossary term the reader names).


### List 3a. Terms of art that plain words would serve

- "On 20 planted tables (400 rows, 4 metrics) the fit recovers all three facets to within 0.05 in 16, at the exact maximum and at temperature 50; the 4 failures have 5, 5, 6 and 11 frontier rows on their thinnest facet (<a href=\"supporting-material/#sub-d-14\" target=\"_self\" style=\"color:inherit;text-decoration:underline\">Appendix D.14</a>)." Term: planted. Plain words: "synthetic tables built with a known answer". **Disposition: plain words** (replace with the plain words the reader names).
- "A regressor from configuration to chart coordinates predicts where proposals fall ({numref}`Figure %s <fig-predict-check-1>`); we then measure them." Term: regressor. Plain words: "a fitted model" or "a model that predicts". **Disposition: plain words** (replace with the plain words the reader names).
- "Association among the near-frontier designs of each K = 3 facet (negative: tension)." Term: association. Plain word: "correlation" (if that is what is computed). **Disposition: plain words** (replace with the plain words the reader names).
- "The mean slack falls from 0.20 at K = 1 to 0.138 at K = 2 and 0.117 at K = 3, at the temperatures 38, 113 and 195; refitted at the K = 1 temperature it falls to 0.09 and 0.05 (<a href=\"supporting-material/#sub-d-15\" target=\"_self\" style=\"color:inherit;text-decoration:underline\">Appendix D.15</a>)." Term: slack. Plain words: "average distance of the designs from the fitted surface" (or whatever it measures). **Disposition: plain words** (replace with the plain words the reader names).
- "The same pipeline on the baseline regime separates the problem's contribution from the gains' ({numref}`Figure %s <fig-regimes-1>`)." Terms: pipeline, regime. Plain words: "the same steps on the untuned (stock-gains) case"; "case" or "setting" for regime. **Disposition: plain words** (replace with the plain words the reader names).
- "Mean slack falls with K by construction and cannot choose it: three facets is the analyst's choice; the finding: their sets differ." Term: by construction. Plain words: "necessarily, since more facets always fit at least as well". **Disposition: plain words** (replace with the plain words the reader names).


### List 3b. Sentences with three or more terms of art together

- "At K = 1 the exact-maximum fit has a 6-lemma across controls, power and energy, plus mass: total mass, slew time, energy balance, control effort, pointing error and depth of discharge contend, with working-temperature exponents from 0.09 to 0.24." Terms: exact-maximum fit, 6-lemma, contend, working-temperature exponents. **Disposition: no change** (a definition, statement or proof step where the terms are the content; the unresolved ones are items in List 1 and the shorter ones items in Lists 2 and 3a).
- "The K = 3 facets have contending sets (exact-maximum supports) of 6, 6 and 7 metrics; peak slew power, power margin and settling time are absent from the K = 1 set." Terms: K = 3 facets, contending sets, exact-maximum supports, K = 1 set. **Disposition: no change** (a definition, statement or proof step where the terms are the content; the unresolved ones are items in List 1 and the shorter ones items in Lists 2 and 3a).
- "Association among the near-frontier designs of each K = 3 facet (negative: tension)." Terms: association, near-frontier, facet, tension. **Disposition: no change** (a definition, statement or proof step where the terms are the content; the unresolved ones are items in List 1 and the shorter ones items in Lists 2 and 3a).
- "Outlined: the contending set, the support of the exact-maximum fit; w is the fitted exponent, small for some members." Terms: contending set, support, exact-maximum fit, fitted exponent. **Disposition: no change** (a definition, statement or proof step where the terms are the content; the unresolved ones are items in List 1 and the shorter ones items in Lists 2 and 3a).
- "The regimes return a 6-lemma and a 6-lemma sharing 3 metrics (control effort, pointing error and slew time); the primary regime alone has depth of discharge, energy balance and total mass, the stock regime alone eclipse reserve, power margin and settling time." Terms: regimes, 6-lemma, primary regime, stock regime. **Disposition: no change** (a definition, statement or proof step where the terms are the content; the unresolved ones are items in List 1 and the shorter ones items in Lists 2 and 3a).
- "Of 3 proposals, the predicted energy differential lies within the regressor's own band 1/tau = 0.0651 of the measured one for 3, and the predicted position within that band for 0; position errors run from 1.4 to 3.1 bands." Terms: energy differential, regressor, band, tau, predicted position. **Disposition: no change** (a definition, statement or proof step where the terms are the content; the unresolved ones are items in List 1 and the shorter ones items in Lists 2 and 3a).
- "The 3 measured candidates have lowest energy differential -0.144 and highest -0.072 to -0.071, and 0 of them lie beyond the fitted reference surface." Terms: measured candidates, energy differential, fitted reference surface. **Disposition: no change** (a definition, statement or proof step where the terms are the content; the unresolved ones are items in List 1 and the shorter ones items in Lists 2 and 3a).
- "At K = 3 the tension separates into three facets with different contending sets: {numref}`Figure %s <fig-plane-3>` shows their envelope, {numref}`Figure %s <fig-chart-3>` places each design and {numref}`Figure %s <fig-tensions-3>` shows what trades off." Terms: tension, facets, contending sets, envelope. **Disposition: no change** (a definition, statement or proof step where the terms are the content; the unresolved ones are items in List 1 and the shorter ones items in Lists 2 and 3a).
- "Log-metric planes of the K = 1 fit (primary regime), one per pair of the facet's largest exponents, with the near-frontier band." Terms: log-metric planes, primary regime, facet's largest exponents, near-frontier band. **Disposition: no change** (a definition, statement or proof step where the terms are the content; the unresolved ones are items in List 1 and the shorter ones items in Lists 2 and 3a).


## Unit 23: docs/user-guide/limitations.md

Density 5.8 terms of art per 100 words (28/479); staged text `docs_user-guide_limitations.md.txt`.


### List 1. Terms unresolved from the unit and the Glossary

- "Moving the reference or the scale of one metric changes which facet is tangent." Term: reference (of a metric). Not in the Glossary; the reader cannot tell what is being moved, nor which surface the facet is tangent to. **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it).
- "A hole is an opportunity only if the trade space is log-convex around it." Term: trade space. The Glossary uses it only inside other entries (number of metrics, white space) and never defines it. **Disposition: no change** (standard vocabulary at the reader level the paper assumes (Boyd and Vandenberghe; scikit-learn)).
- "A single term has constant elasticities and finds one tension, at its balanced point." Terms: tension, balanced point. Neither is defined in the unit or the Glossary (tension appears only in passing under participation threshold); the sentence rests on both. **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it).
- "Away from that point a design can score below 1 while locally on the frontier." Terms: score, V (used unglossed throughout). "Score" is not defined, and "V" is never introduced in the unit; the Glossary has "invariant value" but does not link it to "score" or "V". **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it).
- "Read `n_eff_` and `conditioning_` ([Reading termination](termination.md))." Term: n_eff_. Not in the Glossary; the reader cannot tell what it measures. **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it).
- "The set is exact at infinite temperature with `min_exponent` at 0, and graded participation at a working temperature." Terms: min_exponent, working temperature. The parameter and the term are not in the Glossary (the Glossary has fit temperature and participation threshold, not working temperature). **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it).
- "A tension is a binding constraint, not a correlation, and negative association near the surface is partly a closure effect." Term: closure effect. Not defined and not standard; the reader must guess it means shares summing to a fixed total. **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it).
- "On 20 planted seeds ($K = 3$, $d = 4$, $N = 400$) it recovers the planted facets in 16 or 17; failures are facets with five or six frontier rows." Terms: planted seeds, planted facets, frontier rows. Not in the Glossary; "frontier rows" is also an unmatched use of the ambiguous "frontier". **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it).
- "More restarts do not cure this; a larger sample or `facet_step=\"tangent\"` can help." Term: facet_step="tangent". The option is named but never explained. **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it).
- "A prediction inherits the surrogate's error and the fitted trade space ([Predicting](prediction.md))." Term: surrogate. Not defined; the reader cannot tell what stands in for the evaluation. **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it).


### List 2. Where a Glossary term would say it shorter or more exactly

- "The surface is log-convex." Term: fitted reference surface (or supporting envelope). "The surface" is bare and could be any of the three frontier objects. **Disposition: glossary term** (use the Glossary term the reader names).
- "For regionally varying rates fit [several terms](fitting.md)." Term: elasticity. "Rates" is the Glossary's elasticity (percentage given up per percentage gained). **Disposition: glossary term** (use the Glossary term the reader names).
- "A maximizer of V is efficient in the contending metrics, and the converse is not claimed." Term: contending set, invariant value. "V" is the invariant value; "contending metrics" are the contending set. **Disposition: glossary term** (use the Glossary term the reader names).
- "Judge a score against the band 1/tau." Terms: fit temperature, invariant value. "Tau" is the fit temperature and "score" the invariant value; the Glossary's phrase "band of near-frontier designs" says what the band is. **Disposition: glossary term** (use the Glossary term the reader names).
- "Read `n_eff_` and `conditioning_` ([Reading termination](termination.md))." Term: conditioning of the exponents (and support weights for n_eff_ if that is what it counts). `conditioning_` seems to be the Glossary's conditioning of the exponents. **Disposition: glossary term** (use the Glossary term the reader names).
- "V - 1 says how far a design lies beyond the learned surface, not that it is wanted, feasible or safe." Terms: novelty, fitted reference surface. "V - 1" is the novelty score; "learned surface" is the fitted reference surface. **Disposition: glossary term** (use the Glossary term the reader names).
- "Hyperbolic\" describes the shape of the score, which tends to zero as any participating metric does." Term: invariant value, participation threshold. "Score" is the invariant value; "participating metric" is the Glossary's participation. (Quoted with its opening quotation mark restored: "\"Hyperbolic\" describes the shape of the score, which tends to zero as any participating metric does.") **Disposition: glossary term** (use the Glossary term the reader names).
- "A multi-term fit is a local optimum chosen among seeded restarts." Term: number of terms. "Multi-term" is "number of terms greater than 1". **Disposition: glossary term** (use the Glossary term the reader names).


### List 3a. Terms of art that plain words would serve

- "A tension is a binding constraint, not a correlation, and negative association near the surface is partly a closure effect." Term: closure effect. Plain words: "shares that must add to a fixed total pull against each other". **Disposition: plain words** (replace with the plain words the reader names).
- "The set is exact at infinite temperature with `min_exponent` at 0, and graded participation at a working temperature." Term: graded participation. Plain words: "partial membership". **Disposition: plain words** (replace with the plain words the reader names).
- "A prediction inherits the surrogate's error and the fitted trade space ([Predicting](prediction.md))." Term: surrogate. Plain words: "the stand-in model". **Disposition: plain words** (replace with the plain words the reader names).
- "On 20 planted seeds ($K = 3$, $d = 4$, $N = 400$) it recovers the planted facets in 16 or 17; failures are facets with five or six frontier rows." Term: planted seeds. Plain words: "20 synthetic datasets with known facets". **Disposition: plain words** (replace with the plain words the reader names).
- "If the balanced point sits on a vertex or edge of the weights' simplex, exponents are not unique and some elasticities are undefined." Term: weights' simplex vertex or edge. Plain words: "if one or more weights is zero". **Disposition: plain words** (replace with the plain words the reader names).


### List 3b. Sentences with three or more terms of art together

- "If the balanced point sits on a vertex or edge of the weights' simplex, exponents are not unique and some elasticities are undefined." Terms: balanced point, vertex or edge, simplex, exponents, elasticities. **Disposition: no change** (a definition, statement or proof step where the terms are the content; the unresolved ones are items in List 1 and the shorter ones items in Lists 2 and 3a).
- "A single term has constant elasticities and finds one tension, at its balanced point." Terms: term, elasticities, tension, balanced point. **Disposition: no change** (a definition, statement or proof step where the terms are the content; the unresolved ones are items in List 1 and the shorter ones items in Lists 2 and 3a).
- "The set is exact at infinite temperature with `min_exponent` at 0, and graded participation at a working temperature." Terms: infinite temperature, min_exponent, graded participation, working temperature. **Disposition: no change** (a definition, statement or proof step where the terms are the content; the unresolved ones are items in List 1 and the shorter ones items in Lists 2 and 3a).
- "On 20 planted seeds ($K = 3$, $d = 4$, $N = 400$) it recovers the planted facets in 16 or 17; failures are facets with five or six frontier rows." Terms: planted seeds, K, d, N, facets, frontier rows. **Disposition: no change** (a definition, statement or proof step where the terms are the content; the unresolved ones are items in List 1 and the shorter ones items in Lists 2 and 3a).
- "The fitted reference surface and the supporting envelope are determined by the sample you give; the Pareto boundary is a property of the system." Terms: fitted reference surface, supporting envelope, Pareto boundary. **Disposition: no change** (a definition, statement or proof step where the terms are the content; the unresolved ones are items in List 1 and the shorter ones items in Lists 2 and 3a).
- "A very high tau rests the fit on a few extreme designs; below tau of about 3 the soft maximum approaches the mean." Terms: tau, fit, soft maximum. **Disposition: no change** (a definition, statement or proof step where the terms are the content; the unresolved ones are items in List 1 and the shorter ones items in Lists 2 and 3a). **Routed to P6** (not edited here).
- "A hole is an opportunity only if the trade space is log-convex around it." Terms: hole (white space), trade space, log-convex. **Disposition: no change** (a definition, statement or proof step where the terms are the content; the unresolved ones are items in List 1 and the shorter ones items in Lists 2 and 3a).


## Unit 24: paper/paper.ipynb :: The decision problem

Density 5.6 terms of art per 100 words (30/536); staged text `paper_the-decision-problem.txt`.


### List 1. Terms unresolved from the unit and the Glossary

- "A posynomial surface fitted to the data underlying the table gives them a coordinate system: the chart, a reversible rewriting of the metrics as a position along the surface and a level relative to it." Term: "the table". No table has been introduced in the unit; the reader cannot tell what data it holds or where the rows come from. **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it).
- "The surface is not the Pareto boundary, and the table and its reading are views ({prf:ref}`def-objects`)." Term: "views". The sense of "views" (of what, with what status) is undefined here and resolved only by an unseen cross-reference. **Disposition: no change** (standard vocabulary at the reader level the paper assumes (Boyd and Vandenberghe; scikit-learn)).
- "Open: Q1 to Q4 and the search's monotonicity." Terms: "Q1 to Q4", "the search". The questions are never stated, and "the search" (which procedure, over what) is not defined in the unit or Glossary. **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it).
- "The several-facet fit, not convex in the terms, has three levels of guarantee and a stopping declaration ({prf:ref}`thm-soft`, {prf:ref}`thm-descent`, {prf:ref}`lem-gap`, {prf:ref}`lem-margin`, {prf:ref}`prop-local`); a soft fit has a second-order certificate ({prf:ref}`thm-certificate`)." Terms: "three levels of guarantee", "stopping declaration", "second-order certificate". The Glossary gives termination status only as a list of names; what is certified, and how a second-order certificate differs from the others, is not stated. **Disposition: no change** (standard vocabulary at the reader level the paper assumes (Boyd and Vandenberghe; scikit-learn)). **Routed to P1** (not edited here).
- "Our implementation mirrors the structure of PCA as an unsupervised learning method for feature engineering, and the two chain: {ref}`Appendix D.16 <sub-d-16>` reads the principal directions of the near-frontier chart as the trade-offs the sampling exercised, a reading and not a result." Terms: "near-frontier chart", "the sampling exercised". "Near-frontier" is not defined (the Glossary calls "frontier" three different objects), and what sampling exercises a trade-off is unexplained. **Disposition: no change** (standard vocabulary at the reader level the paper assumes (Boyd and Vandenberghe; scikit-learn)).
- "With one term the posynomial extension is the monomial, and a maximizer of V is Pareto-efficient ({prf:ref}`thm-extension`, {prf:ref}`thm-pareto`)." Terms: "V", "posynomial extension". The symbol V appears with no definition in the unit (the Glossary has "invariant value" but does not tie it to V here), and "extension" of what is not said. **Disposition: no change** (standard vocabulary at the reader level the paper assumes (Boyd and Vandenberghe; scikit-learn)).
- "On this case, with the number of designs and of metrics, dominance stops shortlisting: its nondominated set nears the whole table." Term: "dominance ... shortlisting". "Nondominated" is not defined in the unit and the Glossary has only Pareto boundary (attainable set, not sample); the sample-based set is never named. **Disposition: no change** (standard vocabulary at the reader level the paper assumes (Boyd and Vandenberghe; scikit-learn)).
- "Objectives may align in one region and oppose in another." Term: "region". The Glossary gives "region" a narrow meaning (a facet's dominance set in the ternary plot); the unit uses it in the plain sense without saying so. **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it).
- "On a cubesat model coupling power, mass and attitude control the facets separate contending sets that one facet blends ({numref}`Section %s <sect-case-analysis>`)." Term: "attitude control". Domain term unexplained for a reader at the stated level (cubesat is guessable, this is not). **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it).


### List 2. Where a Glossary term would say it shorter or more exactly

- "A posynomial surface fitted to the data underlying the table gives them a coordinate system: the chart, a reversible rewriting of the metrics as a position along the surface and a level relative to it." Terms: fitted reference surface, position along the frontier, energy differential (level offset). The Glossary names all three objects exactly; "posynomial surface", "position along the surface" and "a level relative to it" are looser. **Disposition: glossary term** (use the Glossary term the reader names).
- "The surface is not the Pareto boundary, and the table and its reading are views ({prf:ref}`def-objects`)." Term: fitted reference surface. "The surface" is ambiguous given the Glossary's three "frontier" objects. **Disposition: glossary term** (use the Glossary term the reader names).
- "The fitted reference surface is the unit level set of a degree-one weighted geometric mean, not the Pareto boundary ({prf:ref}`thm-invariant`)." Term: invariant value. The weighted geometric mean whose doubling doubles it already has this name, and the level V = 1 is its definition. **Disposition: glossary term** (use the Glossary term the reader names).
- "The one-facet fit is a geometric program, convex in the logarithmic variables ({prf:ref}`thm-kkt`, {prf:ref}`thm-convex`); its exponents are elasticities and its chart is reversible ({prf:ref}`thm-elasticity`, {prf:ref}`thm-chart`)." Term: log-metrics. "Logarithmic variables" is the Glossary's log-metrics. **Disposition: glossary term** (use the Glossary term the reader names).
- "The several-facet fit, not convex in the terms, has three levels of guarantee and a stopping declaration ({prf:ref}`thm-soft`, {prf:ref}`thm-descent`, {prf:ref}`lem-gap`, {prf:ref}`lem-margin`, {prf:ref}`prop-local`); a soft fit has a second-order certificate ({prf:ref}`thm-certificate`)." Terms: termination status, fit temperature. "Levels of guarantee and a stopping declaration" is termination status; "a soft fit" is a finite fit temperature. **Disposition: glossary term** (use the Glossary term the reader names). **Routed to P1** (not edited here).
- "Our implementation mirrors the structure of PCA as an unsupervised learning method for feature engineering, and the two chain: {ref}`Appendix D.16 <sub-d-16>` reads the principal directions of the near-frontier chart as the trade-offs the sampling exercised, a reading and not a result." Term: fit temperature. "Near-frontier" is the finite-temperature band of near-frontier designs. **Disposition: glossary term** (use the Glossary term the reader names).
- "Of 706 feasible cubesat designs, the nondominated sets hold 7 to 8 on 2, 145 to 146 on 4 and 671 on 10 attributes (a range is the spread over five regenerations of the data under rounding-level perturbation, <a href="supporting-material/#sub-d-11" target="_self" style="color:inherit;text-decoration:underline">Appendix D.11</a>)." Terms: number of designs, number of metrics. "706 feasible designs" and "2, 4, 10 attributes" are these counts; also dominance is computed on metrics, so "attributes" is the wrong Glossary word. **Disposition: glossary term** (use the Glossary term the reader names).
- "Each facet names the metrics that contend on it with elasticities: an n-lemma (by analogy with dilemma and trilemma)." Term: contending set. "The metrics that contend on it" is the contending set. **Disposition: glossary term** (use the Glossary term the reader names).


### List 3a. Terms of art that plain words would serve

- "Of 706 feasible cubesat designs, the nondominated sets hold 7 to 8 on 2, 145 to 146 on 4 and 671 on 10 attributes (a range is the spread over five regenerations of the data under rounding-level perturbation, <a href="supporting-material/#sub-d-11" target="_self" style="color:inherit;text-decoration:underline">Appendix D.11</a>)." Term: "regenerations ... under rounding-level perturbation". Plain: "five reruns of the data, each rounded slightly differently". **Disposition: plain words** (replace with the plain words the reader names).
- "Our implementation mirrors the structure of PCA as an unsupervised learning method for feature engineering, and the two chain: {ref}`Appendix D.16 <sub-d-16>` reads the principal directions of the near-frontier chart as the trade-offs the sampling exercised, a reading and not a result." Terms: "unsupervised learning method for feature engineering", "the sampling exercised", "chain". Plain: "a method that finds structure without labels", "the trade-offs the sampled designs actually show", "can be run one after the other". **Disposition: plain words** (replace with the plain words the reader names).
- "The several-facet fit, not convex in the terms, has three levels of guarantee and a stopping declaration ({prf:ref}`thm-soft`, {prf:ref}`thm-descent`, {prf:ref}`lem-gap`, {prf:ref}`lem-margin`, {prf:ref}`prop-local`); a soft fit has a second-order certificate ({prf:ref}`thm-certificate`)." Terms: "stopping declaration", "second-order certificate". Plain: "a stated reason for stopping", "a check that the stopping point is a true local optimum". **Disposition: plain words** (replace with the plain words the reader names). **Routed to P1** (not edited here).
- "Open: Q1 to Q4 and the search's monotonicity." Term: "monotonicity". Plain: "whether the search always improves the fit". **Disposition: plain words** (replace with the plain words the reader names).
- "On this case, with the number of designs and of metrics, dominance stops shortlisting: its nondominated set nears the whole table." Terms: "dominance", "nondominated set", "shortlisting". Plain: "designs not beaten on every metric by another design"; "narrowing the list". **Disposition: plain words** (replace with the plain words the reader names).
- "The fitted reference surface is the unit level set of a degree-one weighted geometric mean, not the Pareto boundary ({prf:ref}`thm-invariant`)." Term: "degree-one". Plain: "a weighted geometric mean that doubles when every metric doubles". **Disposition: plain words** (replace with the plain words the reader names).


### List 3b. Sentences with three or more terms of art together

- "A posynomial surface fitted to the data underlying the table gives them a coordinate system: the chart, a reversible rewriting of the metrics as a position along the surface and a level relative to it." Terms: posynomial, chart, metrics, position along the surface, level. **Disposition: plain words** (introductory page: spread the terms over more words).
- "The several-facet fit, not convex in the terms, has three levels of guarantee and a stopping declaration ({prf:ref}`thm-soft`, {prf:ref}`thm-descent`, {prf:ref}`lem-gap`, {prf:ref}`lem-margin`, {prf:ref}`prop-local`); a soft fit has a second-order certificate ({prf:ref}`thm-certificate`)." Terms: facet, convex, terms, levels of guarantee, stopping declaration, soft fit, second-order certificate. **Disposition: plain words** (introductory page: spread the terms over more words). **Routed to P1** (not edited here).
- "The one-facet fit is a geometric program, convex in the logarithmic variables ({prf:ref}`thm-kkt`, {prf:ref}`thm-convex`); its exponents are elasticities and its chart is reversible ({prf:ref}`thm-elasticity`, {prf:ref}`thm-chart`)." Terms: facet, geometric program, logarithmic variables, exponents, elasticities, chart. **Disposition: plain words** (introductory page: spread the terms over more words).
- "The fitted reference surface is the unit level set of a degree-one weighted geometric mean, not the Pareto boundary ({prf:ref}`thm-invariant`)." Terms: fitted reference surface, unit level set, degree-one weighted geometric mean, Pareto boundary. **Disposition: plain words** (introductory page: spread the terms over more words).
- "With one term the posynomial extension is the monomial, and a maximizer of V is Pareto-efficient ({prf:ref}`thm-extension`, {prf:ref}`thm-pareto`)." Terms: term, posynomial extension, monomial, V, Pareto-efficient. **Disposition: plain words** (introductory page: spread the terms over more words).
- "Our implementation mirrors the structure of PCA as an unsupervised learning method for feature engineering, and the two chain: {ref}`Appendix D.16 <sub-d-16>` reads the principal directions of the near-frontier chart as the trade-offs the sampling exercised, a reading and not a result." Terms: PCA, unsupervised learning, feature engineering, principal directions, near-frontier chart. **Disposition: plain words** (introductory page: spread the terms over more words).
- "On a cubesat model coupling power, mass and attitude control the facets separate contending sets that one facet blends ({numref}`Section %s <sect-case-analysis>`)." Terms: facets, contending sets, attitude control. **Disposition: plain words** (introductory page: spread the terms over more words).
- "Each facet names the metrics that contend on it with elasticities: an n-lemma (by analogy with dilemma and trilemma)." Terms: facet, metrics, contend, elasticities, n-lemma. **Disposition: plain words** (introductory page: spread the terms over more words).


## Unit 25: paper/paper.ipynb :: Results

Density 5.5 terms of art per 100 words (6/110); staged text `paper_results.txt`.


### List 1. Terms unresolved from the unit and the Glossary

- "The one-facet fit comes first: the invariant value and its shift (L1, L2), the fit as a convex program (L3 to L5), what its numbers mean (L6, L7), the chart (L8, L9) and several terms (L10, L11)." Terms: "L1" to "L17" (and "L12 to L14" etc.), "shift". The L-labels are never said to be lemmas; "shift" is not a Glossary entry (level offset / energy differential is the nearest). **Disposition: no change** (standard vocabulary at the reader level the paper assumes (Boyd and Vandenberghe; scikit-learn)). **Routed to P1** (not edited here).
- "The several-facet fit is not convex; it has three levels of guarantee (L16, L15, L12 to L14) and, for a soft fit, a certificate (L17)." Terms: "certificate", "soft fit", "L16/L15/L12 to L14/L17". "Certificate" is neither defined nor in the Glossary (only "certified" inside termination status); "soft fit" is not an entry; the L-labels are unexplained. **Disposition: no change** (standard vocabulary at the reader level the paper assumes (Boyd and Vandenberghe; scikit-learn)). **Routed to P1** (not edited here).
- "The sentences between the boxes say what the next result is for." Term: "boxes". Nothing in the unit says what the boxes are (presumably the result statements). **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it). **Routed to P1** (not edited here).
- "Whether the hypotheses suit a table is a human judgment ({numref}`Section %s <sect-discussion>`)." Terms: "hypotheses", "table". The hypotheses are never named, and the table is not introduced in the unit (the Glossary only says a row is a configuration). **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it). **Routed to P1** (not edited here).


### List 2. Where a Glossary term would say it shorter or more exactly

- "The one-facet fit comes first: the invariant value and its shift (L1, L2), the fit as a convex program (L3 to L5), what its numbers mean (L6, L7), the chart (L8, L9) and several terms (L10, L11)." Term: "level offset" (or "energy differential") for "shift"; "geometric program" for "convex program" if that is what is meant (convex after x = exp(y)). **Disposition: glossary term** (use the Glossary term the reader names). **Routed to P1** (not edited here).
- "The several-facet fit is not convex; it has three levels of guarantee (L16, L15, L12 to L14) and, for a soft fit, a certificate (L17)." Term: "termination status" for "levels of guarantee" (but the Glossary lists six, not three); "fit temperature" (finite) for "soft fit". **Disposition: glossary term** (use the Glossary term the reader names). **Routed to P1** (not edited here).


### List 3a. Terms of art that plain words would serve

- "Whether the hypotheses suit a table is a human judgment ({numref}`Section %s <sect-discussion>`)." Term: "hypotheses"; plain words: "assumptions". **Disposition: plain words** (replace with the plain words the reader names). **Routed to P1** (not edited here).


### List 3b. Sentences with three or more terms of art together

- "The one-facet fit comes first: the invariant value and its shift (L1, L2), the fit as a convex program (L3 to L5), what its numbers mean (L6, L7), the chart (L8, L9) and several terms (L10, L11)." Terms: one-facet fit, invariant value, shift, convex program, chart, several terms; six items in one list, with only lemma numbers to point at. **Disposition: no change** (a definition, statement or proof step where the terms are the content; the unresolved ones are items in List 1 and the shorter ones items in Lists 2 and 3a). **Routed to P1** (not edited here).
- "The several-facet fit is not convex; it has three levels of guarantee (L16, L15, L12 to L14) and, for a soft fit, a certificate (L17)." Terms: several-facet fit, convex, levels of guarantee, soft fit, certificate. **Disposition: no change** (a definition, statement or proof step where the terms are the content; the unresolved ones are items in List 1 and the shorter ones items in Lists 2 and 3a). **Routed to P1** (not edited here).


## Unit 26: docs/index.md

Density 5.3 terms of art per 100 words (10/190); staged text `docs_index.md.txt`.


### List 1. Terms unresolved from the unit and the Glossary

- "`hyperbolic_trade_space` learns the shape of a design trade space from evaluated designs." Terms: hyperbolic (in the package name), trade space. Why: neither is defined in the unit; the Glossary uses "trade space" without defining it, and nothing says what is hyperbolic. **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it).
- "Give it a table of designs, each scored on several metrics where larger is better, and it fits a frontier model in the posynomial invariant form." Terms: frontier model, invariant form. Why: the Glossary says "frontier" names one of three objects, so "frontier model" is ambiguous here, and "invariant form" is not defined (only "invariant value" is). **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it).
- "[Examples](examples.md): a cubesat trade study across power, mass and attitude control." Term: attitude control. Why: aerospace jargon, not defined here or in the Glossary, and not standard at the reader's level. **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it).
- "It is a scikit-learn estimator (`fit`, `transform`, `inverse_transform`, `score_samples`) in the unsupervised and feature-engineering family, beside PCA: PCA finds where the data spread, this finds where they stop, and the two chain." Term: "the two chain". Why: it is unclear what chaining means here (output of one fed to the other?) and in what order. **Disposition: no change** (standard vocabulary at the reader level the paper assumes (Boyd and Vandenberghe; scikit-learn)).


### List 2. Where a Glossary term would say it shorter or more exactly

- "It then tells you which metrics contend, at what exchange rate, where each design sits relative to the fitted reference surface, and where the table has gaps." Terms: contending set (metrics contend), elasticity (exchange rate), energy differential (where each design sits relative to the surface), white space (gaps in the table). Why: each clause restates a Glossary term loosely; the terms are exact and shorter. **Disposition: add to avoid** (the phrase is withdrawn by WP10 Amendment 4 (R-33, R-34, R-37)).
- "Give it a table of designs, each scored on several metrics where larger is better, and it fits a frontier model in the posynomial invariant form." Terms: metrics, posynomial, fitted reference surface. Why: "frontier model" is the ambiguous everyday word; the Glossary names the fitted object exactly (a posynomial whose level V = 1 is the fitted reference surface). **Disposition: glossary term** (use the Glossary term the reader names).
- "[User guide](user-guide/overview.md): one page per task, from conditioning your attributes to reading what the fit reports." Term: termination status. Why: "what the fit reports" is vague against the Glossary's exact name for part of the report. **Disposition: glossary term** (use the Glossary term the reader names).


### List 3a. Terms of art that plain words would serve

- "It is a scikit-learn estimator (`fit`, `transform`, `inverse_transform`, `score_samples`) in the unsupervised and feature-engineering family, beside PCA: PCA finds where the data spread, this finds where they stop, and the two chain." Term: "unsupervised and feature-engineering family". Plain words: "a data-transformer, like PCA". **Disposition: plain words** (replace with the plain words the reader names).
- "[User guide](user-guide/overview.md): one page per task, from conditioning your attributes to reading what the fit reports." Term: conditioning your attributes. Plain words: "preparing your raw measurements". **Disposition: plain words** (replace with the plain words the reader names).
- "Give it a table of designs, each scored on several metrics where larger is better, and it fits a frontier model in the posynomial invariant form." Term: posynomial invariant form. Plain words: "a sum-of-power-terms model" (or defer the name to a link). **Disposition: plain words** (replace with the plain words the reader names).


### List 3b. Sentences with three or more terms of art together

- "Give it a table of designs, each scored on several metrics where larger is better, and it fits a frontier model in the posynomial invariant form." Terms: metrics, frontier model, posynomial invariant form. **Disposition: plain words** (introductory page: spread the terms over more words).
- "It then tells you which metrics contend, at what exchange rate, where each design sits relative to the fitted reference surface, and where the table has gaps." Terms: metrics contend, exchange rate, fitted reference surface. **Disposition: add to avoid** (the phrase is withdrawn by WP10 Amendment 4 (R-33, R-34, R-37)).
- "It is a scikit-learn estimator (`fit`, `transform`, `inverse_transform`, `score_samples`) in the unsupervised and feature-engineering family, beside PCA: PCA finds where the data spread, this finds where they stop, and the two chain." Terms: estimator, the four method names, unsupervised, feature-engineering, PCA. **Disposition: plain words** (introductory page: spread the terms over more words).
- "[User guide](user-guide/overview.md): one page per task, from conditioning your attributes to reading what the fit reports." Terms: conditioning, attributes, fit. **Disposition: plain words** (introductory page: spread the terms over more words).


## Unit 27: paper/paper.ipynb :: Reproducibility and your own case

Density 5.0 terms of art per 100 words (3/60); staged text `paper_reproducibility-and-your-own-case.txt`.


### List 1. Terms unresolved from the unit and the Glossary

- "Every figure, table and reported number comes from a call into a tested module; {ref}`Appendix F <appendix-f>` gives the pinned toolchain, the environment of record, the commands and one row per item." Term: "environment of record". Not in the Glossary and not standard; unclear whether it differs from the pinned toolchain. **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it).
- "To run your own table, supply configurations, attributes and a conditioning rule, and use the same calls; the package documentation is the user's guide." Term: "table". The Glossary uses it ("rows of the table") but never defines it; it is unclear whether it means the configurations-to-attributes data or the metrics. **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it).


### List 2. Where a Glossary term would say it shorter or more exactly

- "To run your own table, supply configurations, attributes and a conditioning rule, and use the same calls; the package documentation is the user's guide." Term: "table" could be the Glossary's "number of designs" row sense (each row an evaluated configuration); "conditioning rule" is exactly the Glossary's "conditioning" (attributes into metrics), and the unit does not say the result is the metrics. **Disposition: glossary term** (use the Glossary term the reader names).


### List 3a. Terms of art that plain words would serve

- "Every figure, table and reported number comes from a call into a tested module; {ref}`Appendix F <appendix-f>` gives the pinned toolchain, the environment of record, the commands and one row per item." Terms: "pinned toolchain", "environment of record". Plain words: "the exact software versions" and "the setup the results were produced in". **Disposition: plain words** (replace with the plain words the reader names).


### List 3b. Sentences with three or more terms of art together

- "Every figure, table and reported number comes from a call into a tested module; {ref}`Appendix F <appendix-f>` gives the pinned toolchain, the environment of record, the commands and one row per item." Terms: pinned toolchain, environment of record, tested module; three engineering terms in one list. **Disposition: no change** (a definition, statement or proof step where the terms are the content; the unresolved ones are items in List 1 and the shorter ones items in Lists 2 and 3a).
- "To run your own table, supply configurations, attributes and a conditioning rule, and use the same calls; the package documentation is the user's guide." Terms: configurations, attributes, conditioning rule; all Glossary terms, but three undefined-in-place terms in one clause. **Disposition: no change** (a definition, statement or proof step where the terms are the content; the unresolved ones are items in List 1 and the shorter ones items in Lists 2 and 3a).


## Unit 28: paper/paper.ipynb :: The algorithm for several facets

Density 5.0 terms of art per 100 words (45/908); staged text `paper_the-algorithm-for-several-facets.txt`.


### List 1. Terms unresolved from the unit and the Glossary

- "Every facet is fitted against every design: the model is $\Phi_K$ ({prf:ref}`thm-extension`), each offset $\beta_k=J_\tau(Uw_k)$ is the support over all rows, and the fit minimizes the mean slack $F(W)=-\frac1N\sum_i\Phi_K(u_i)$." Terms: J_tau, U, "offset", "slack", "mean slack". None is defined here or in the Glossary; the reader cannot tell what J_tau computes or what slack measures. **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it). **Routed to P1** (not edited here).
- "With weights $\alpha_{ik}=\mathrm{softmax}_k(\kappa\,s_{ik})$ from the current model: (i) a convex program symmetric in the terms attains its minimum with all terms equal, so the objective over all terms is not convex in them in general; (ii) the soft model's slack is bounded above by the fixed-weight objective, with equality at the weights' own model; (iii) the fixed-weight objective is a generalized posynomial in $e^{w}$." Terms: kappa, "fixed-weight objective", "soft model". The Glossary has term temperature but never says how kappa relates to it, and "fixed-weight objective" is never defined. **Disposition: add to avoid** (the phrase is withdrawn by WP10 Amendment 4 (R-33, R-34, R-37)). **Routed to P1** (not edited here).
- "**Derived.** *Hypotheses.* A1, A2, A3, A6; I14 (Jensen); I15 (generalized posynomial)." Terms: A1-A8, F12, R2, I-numbers, "Derived". The code labels are not defined in the unit or the Glossary, so the hypotheses cannot be read. **Disposition: add to avoid** (the phrase is withdrawn by WP10 Amendment 4 (R-33, R-34, R-37)). **Routed to P1** (not edited here).
- "Refitting a facet on its own rows is ill-posed (observed on planted data, {ref}`Appendix D.13 <sub-d-13>`)." Terms: "planted data", "ill-posed". The reader does not know what was planted or in what sense the problem is ill-posed (no minimizer, or not unique). **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it). **Routed to P1** (not edited here).
- "**Derived.** *Hypotheses.* A8 (a partition into nonempty cells); F12 (the minimum is attained); step B, unpenalized, with support offsets $\beta_k=J_\tau(Uw_k)$ and each refit an exact minimizer of $f_k$." Terms: "cells", "step B", "unpenalized". Cells are not the same word as facets or rows, and step B and the penalty it omits are not introduced. **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it). **To the driver** (the reader reports a clash that touches a term's meaning). **Routed to P1** (not edited here).
- "**Derived.** *Hypotheses.* R2 ($\gamma>0$); F12; I9 (Cauchy-Schwarz)." Term: gamma. The Glossary defines the assignment margin but never says that gamma is its symbol. **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it). **Routed to P1** (not edited here).
- "On the assignment-stable neighbourhood, with offsets $\beta'_k=J_\tau(Uw'_k)$, $F(W')-F(W)=\sum_k\frac{n_k}{N}\big(f_k(w'_k)-f_k(w_k)\big)\ge0$, so $W$ is a local minimizer of the mean slack." Term: "assignment-stable neighbourhood". Not defined; the Glossary has stable radius but not this neighbourhood. **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it). **Routed to P1** (not edited here).
- "Soft-fit certificate: at a feasible point of the soft-weight fit where the first-order (KKT) conditions hold, if the Hessian $H=D-\kappa M$ of the soft objective is positive definite on the tangent space of the active face, the point is a strict local minimizer; $D$ and $M$ are both positive semidefinite, $D$ the weighted within-term curvature and $\kappa M$ the designs' ambiguity between terms." Term: "active face". It is not defined, and it is unclear whether it is a facet or a face of the simplex. **Disposition: no change** (standard vocabulary at the reader level the paper assumes (Boyd and Vandenberghe; scikit-learn)). **Routed to P1** (not edited here).
- "At K = 3 the margin is 0.00022 to 0.0019 and the stable radius 1.8e-05 to 0.00016, against a band 1/tau of 0.0051 and a median best-minus-second-best score of 0.18: a margin below the band puts a few designs on a seam, and the certificate covers changes under the radius only." Terms: "seam", "band 1/tau". The Glossary gives a band of near-frontier designs, not a band of width 1/tau in score, and "seam" is not defined. **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it). **Routed to P1** (not edited here).
- "On the primary regime the solver declares the status certified at K = 2 and 3, with the largest facet gap below 1e-12." Term: "primary regime". The test setting is not defined. **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it). **Routed to P1** (not edited here).


### List 2. Where a Glossary term would say it shorter or more exactly

- "The sharp weights give one label per design, $k(i)=\arg\max_ks_{ik}$, $s_{ik}=w_k\cdot u_i-\beta_k$; with $n_k$ the designs labelled $k$ and $\bar u_k$ their mean log-metric," Terms: assignment, number of designs. "One label per design" is the assignment, and n_k is the number of designs assigned to term k. **Disposition: glossary term** (use the Glossary term the reader names). **Routed to P1** (not edited here).
- "Which facet dominates a design is analysis of the fitted model, not part of the fit (steps: {ref}`Appendix B.2 <sub-b-2>`)." Term: assignment. The Glossary defines the assignment as the dominant term of a design and as an analysis; "A design's assignment is analysis, not part of the fit" says the same in fewer words. **Disposition: glossary term** (use the Glossary term the reader names). **Routed to P1** (not edited here).
- "The package fits with sharp weights at the default term temperature (infinity) and with soft weights at a finite one; a soft fit is certified by the second-order test ({prf:ref}`thm-certificate`)." Term: term temperature. "Sharp weights" and "soft weights" are the infinite and finite cases of the term temperature and can be named that way throughout. **Disposition: glossary term** (use the Glossary term the reader names). **Routed to P1** (not edited here).
- "The sharp-weight fit meets three levels of guarantee, none global: descent (L15), numerical stationarity by the facet gap (L12) and local optimality where the margin is positive (L13, L14)." Terms: termination status, assignment margin. The "levels of guarantee" are what the Glossary calls the termination status, and "the margin" is the assignment margin. **Disposition: glossary term** (use the Glossary term the reader names). **Routed to P1** (not edited here).
- "**The stopping declaration.** Each returned fit carries the levels it meets ({ref}`Appendix D.8 <sub-d-8>`)." Term: termination status. "Stopping declaration" and "levels it meets" are the Glossary's termination status. **Disposition: glossary term** (use the Glossary term the reader names). **Routed to P1** (not edited here).
- "On the primary regime the solver declares the status certified at K = 2 and 3, with the largest facet gap below 1e-12." Terms: termination status, number of terms, numerically zero. K is the number of terms, and "below 1e-12" is the Glossary's numerically-zero threshold. **Disposition: glossary term** (use the Glossary term the reader names). **Routed to P1** (not edited here).
- "Reassignment gives each row the least of its slacks; the refit minimizes a convex $f_k$ of which the previous $w_k$ is a feasible point." Term: assignment. "Reassignment" is reassigning each design to its dominant term. **Disposition: glossary term** (use the Glossary term the reader names). **Routed to P1** (not edited here).
- "At K = 3 the margin is 0.00022 to 0.0019 and the stable radius 1.8e-05 to 0.00016, against a band 1/tau of 0.0051 and a median best-minus-second-best score of 0.18: a margin below the band puts a few designs on a seam, and the certificate covers changes under the radius only." Terms: assignment margin, fit temperature. "Margin" is the assignment margin, and the "median best-minus-second-best score" is the typical gap that the assignment margin takes the minimum of. **Disposition: glossary term** (use the Glossary term the reader names). **Routed to P1** (not edited here).
- "each offset $\beta_k=J_\tau(Uw_k)$ is the support over all rows" Term: supporting envelope. "Support over all rows" is what the Glossary calls the supporting envelope (the exact-maximum fit). **Disposition: glossary term** (use the Glossary term the reader names). **Routed to P1** (not edited here).


### List 3a. Terms of art that plain words would serve

- "Refitting a facet on its own rows is ill-posed (observed on planted data, {ref}`Appendix D.13 <sub-d-13>`)." Plain words: "has no stable answer" for "ill-posed"; "synthetic data with a known answer" for "planted data". **Disposition: plain words** (replace with the plain words the reader names). **Routed to P1** (not edited here).
- "Cyclic shifts of the terms and Jensen's inequality give (i) and (ii); (iii) is a product of powers of posynomials." Plain words: "relabelling the terms in a cycle" for "cyclic shifts of the terms". **Disposition: plain words** (replace with the plain words the reader names). **Routed to P1** (not edited here).
- "On the primary regime the solver declares the status certified at K = 2 and 3, with the largest facet gap below 1e-12." Plain words: "main test setting" for "primary regime". **Disposition: plain words** (replace with the plain words the reader names). **Routed to P1** (not edited here).
- "At K = 3 the margin is 0.00022 to 0.0019 and the stable radius 1.8e-05 to 0.00016, against a band 1/tau of 0.0051 and a median best-minus-second-best score of 0.18: a margin below the band puts a few designs on a seam, and the certificate covers changes under the radius only." Plain words: "sit near a tie between two facets" for "on a seam". **Disposition: plain words** (replace with the plain words the reader names). **Routed to P1** (not edited here).
- "One accepted iteration does not raise the mean slack $F$: reassigning each row to its maximizing facet lowers or keeps $F$, and refitting each facet on the new cells does likewise. Convergence and stationarity are not claimed." Plain words: "each pass never makes F larger" for "descent"; "groups" for "cells". **Disposition: plain words** (replace with the plain words the reader names). **Routed to P1** (not edited here).
- "Soft-fit certificate: at a feasible point of the soft-weight fit where the first-order (KKT) conditions hold, if the Hessian $H=D-\kappa M$ of the soft objective is positive definite on the tangent space of the active face, the point is a strict local minimizer; $D$ and $M$ are both positive semidefinite, $D$ the weighted within-term curvature and $\kappa M$ the designs' ambiguity between terms." Plain words: "how unsure designs are which term they belong to" for "ambiguity between terms". **Disposition: plain words** (replace with the plain words the reader names). **Routed to P1** (not edited here).


### List 3b. Sentences with three or more terms of art together

- "The package fits with sharp weights at the default term temperature (infinity) and with soft weights at a finite one; a soft fit is certified by the second-order test ({prf:ref}`thm-certificate`)." Terms: sharp weights, term temperature, soft weights, certified, second-order test. **Disposition: no change** (a definition, statement or proof step where the terms are the content; the unresolved ones are items in List 1 and the shorter ones items in Lists 2 and 3a). **Routed to P1** (not edited here).
- "The sharp-weight fit meets three levels of guarantee, none global: descent (L15), numerical stationarity by the facet gap (L12) and local optimality where the margin is positive (L13, L14)." Terms: sharp-weight fit, descent, numerical stationarity, facet gap, local optimality, margin. **Disposition: no change** (a definition, statement or proof step where the terms are the content; the unresolved ones are items in List 1 and the shorter ones items in Lists 2 and 3a). **Routed to P1** (not edited here).
- "At K = 3 the margin is 0.00022 to 0.0019 and the stable radius 1.8e-05 to 0.00016, against a band 1/tau of 0.0051 and a median best-minus-second-best score of 0.18: a margin below the band puts a few designs on a seam, and the certificate covers changes under the radius only." Terms: margin, stable radius, band, score, seam, certificate. **Disposition: no change** (a definition, statement or proof step where the terms are the content; the unresolved ones are items in List 1 and the shorter ones items in Lists 2 and 3a). **Routed to P1** (not edited here).
- "Soft-fit certificate: at a feasible point of the soft-weight fit where the first-order (KKT) conditions hold, if the Hessian $H=D-\kappa M$ of the soft objective is positive definite on the tangent space of the active face, the point is a strict local minimizer; $D$ and $M$ are both positive semidefinite, $D$ the weighted within-term curvature and $\kappa M$ the designs' ambiguity between terms." Terms: soft-weight fit, KKT conditions, tangent space of the active face, strict local minimizer, within-term curvature, ambiguity between terms. **Disposition: no change** (a definition, statement or proof step where the terms are the content; the unresolved ones are items in List 1 and the shorter ones items in Lists 2 and 3a). **Routed to P1** (not edited here).
- "If every facet score changes by at most $\delta$ with $2\delta<\gamma$, each row's maximizing facet is unchanged and unique. This holds whenever every $(w_k,\beta_k)$ moves by less than the stable radius $r=\gamma/(2\max_i\lVert(u_i,-1)\rVert_2)$, sufficient and not tight." Terms: facet score, maximizing facet, stable radius, gamma (assignment margin). **Disposition: no change** (a definition, statement or proof step where the terms are the content; the unresolved ones are items in List 1 and the shorter ones items in Lists 2 and 3a). **Routed to P1** (not edited here).
- "With $g=\nabla f_k(w)$, the facet gap is $G_k(w)=g\cdot w-\min_jg_j=\sum_jw_j(g_j-\min_lg_l)\ge0$, and $0\le f_k(w)-f_k^*\le G_k(w)$. $G_k=0$ exactly when the simplex KKT conditions of {prf:ref}`thm-kkt` hold. At $\tau=\infty$, with the LP duals, $G_k$ is the LP duality gap." Terms: facet gap, simplex KKT conditions, tau = infinity, LP duals, LP duality gap. **Disposition: no change** (a definition, statement or proof step where the terms are the content; the unresolved ones are items in List 1 and the shorter ones items in Lists 2 and 3a). **Routed to P1** (not edited here).
- "For a soft fit, certified means that the second-order test holds ({prf:ref}`thm-certificate`), and stationary that the facet gaps hold and the curvature is not positive." Terms: soft fit, certified, second-order test, stationary, facet gaps. **Disposition: no change** (a definition, statement or proof step where the terms are the content; the unresolved ones are items in List 1 and the shorter ones items in Lists 2 and 3a). **Routed to P1** (not edited here).
- "**Derived.** *Hypotheses.* A8 (a partition into nonempty cells); F12 (the minimum is attained); step B, unpenalized, with support offsets $\beta_k=J_\tau(Uw_k)$ and each refit an exact minimizer of $f_k$." Terms: A8, F12, cells, step B, unpenalized, support offsets. **Disposition: no change** (a definition, statement or proof step where the terms are the content; the unresolved ones are items in List 1 and the shorter ones items in Lists 2 and 3a). **Routed to P1** (not edited here).


## Unit 29: paper/paper.ipynb :: Discussion

Density 4.8 terms of art per 100 words (21/439); staged text `paper_discussion.txt`.


### List 1. Terms unresolved from the unit and the Glossary

- "It showed that the regressor places the energy differential of a proposal within its band (3 of 3), the easy part." Terms: regressor, proposal, band. Which regressor, what a proposal is and which band are not stated in the unit or the Glossary (the Glossary's "band" is the near-frontier band, not an interval on the energy differential). **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it).
- "**What propose, predict, check showed.**" Term: propose, predict, check. A named procedure never defined here or in the Glossary. **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it).
- "K = 1 finds one tension; several regional tensions need K > 1." Term: tension. Used throughout and only mentioned inside the Glossary entry for participation threshold; never defined. **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it).
- "A deflation-style search for successive tensions, as PCA extracts components, is a research question: we claim neither that it works nor that tensions are orthogonal." Terms: deflation-style search, tensions (orthogonal). Orthogonal in what space is not said. **Disposition: no change** (standard vocabulary at the reader level the paper assumes (Boyd and Vandenberghe; scikit-learn)).
- "By {prf:ref}`thm-invariant`, a design with $V=v$ is a frontier design scaled by $v$, so $V-1$ is a relative improvement, meaningful relative to the band $1/\tau$." Terms: tau, frontier design, band. The symbol tau is not tied to fit temperature, and "frontier design" is not a Glossary object. **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it).
- "An answer far from the frontier is hard to justify, and the analysis must rerun on empirical data to support configuration management." Terms: configuration management, frontier. The sentence's claim is not followable; configuration management is not the Glossary's configuration. **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it).
- "One facet is tangent at one place and is conservative off it." Term: conservative. Conservative in which direction (over or under the data) is not stated. **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it).
- "{ref}`Appendix E <appendix-e>` gives the ledger." Term: ledger. Not defined; only the title of a list of limits can be guessed. **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it).
- "The research question is which kernel expansions keep the programs geometric programs, so that the guarantees and reading rules carry over." Terms: kernel expansions, guarantees, reading rules. Which guarantees and which reading rules is not said. **Disposition: no change** (standard vocabulary at the reader level the paper assumes (Boyd and Vandenberghe; scikit-learn)).
- "The exponents depend on the conditioning." Term: the symbol K and "conditioning" are fine, but "exponents" is ambiguous between the exponent vector and the working-temperature exponents. **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it).


### List 2. Where a Glossary term would say it shorter or more exactly

- "A hole in the chart is an opportunity only where the trade space is log-convex around it, which the data cannot prove." Term: white space (Glossary: a hole in the chart coordinates). **Disposition: glossary term** (use the Glossary term the reader names).
- "The fitted surface is a log-convex envelope." Term: supporting envelope or fitted reference surface; the Glossary separates these and the sentence picks neither. **Disposition: glossary term** (use the Glossary term the reader names).
- "An answer far from the frontier is hard to justify, and the analysis must rerun on empirical data to support configuration management." Term: frontier; the Glossary says to name one of fitted reference surface, supporting envelope or Pareto boundary. **Disposition: glossary term** (use the Glossary term the reader names).
- "**Why a frontier.**" Term: frontier, same reason. **Disposition: glossary term** (use the Glossary term the reader names).
- "By {prf:ref}`thm-invariant`, a design with $V=v$ is a frontier design scaled by $v$, so $V-1$ is a relative improvement, meaningful relative to the band $1/\tau$." Terms: invariant value (V), improvement factor, fit temperature (for $1/\tau$). **Disposition: glossary term** (use the Glossary term the reader names).
- "It did not show that it places the position along the frontier (0 of 3), and 3 proposals illustrate and do not estimate a rate." Term: number of designs (3 proposals) is not the point; "position along the frontier" is used correctly, but "frontier" here should be the fitted reference surface. **Disposition: glossary term** (use the Glossary term the reader names).
- "The exponents and elasticities are features of the conditioned empirical model: they describe how the sampled designs trade, and not a causal exchange that changing a variable would reproduce." Term: conditioned empirical model; Glossary's conditioning and fitted reference surface say what is modelled. **Disposition: glossary term** (use the Glossary term the reader names).


### List 3a. Terms of art that plain words would serve

- "Tensions the sampling never exercised cannot appear." Term: exercised. Plain: "covered" or "sampled". **Disposition: plain words** (replace with the plain words the reader names).
- "A deflation-style search for successive tensions, as PCA extracts components, is a research question" Term: deflation-style search. Plain: "removing one tension and searching again". **Disposition: plain words** (replace with the plain words the reader names).
- "One facet is tangent at one place and is conservative off it." Term: conservative. Plain: "falls short of the data away from it" (or whichever direction is meant). **Disposition: plain words** (replace with the plain words the reader names).
- "{ref}`Appendix E <appendix-e>` gives the ledger." Term: ledger. Plain: "list of limits". **Disposition: plain words** (replace with the plain words the reader names).
- "**Cross-application.**" Term: cross-application. Plain: "Other uses". **Disposition: plain words** (replace with the plain words the reader names).
- "How the attributes were produced is a black box to the method" Term: black box. Plain: "the method does not use how the attributes were produced". **Disposition: plain words** (replace with the plain words the reader names).
- "It showed that the regressor places the energy differential of a proposal within its band (3 of 3), the easy part." Term: energy differential. Plain: "how far a design sits from the fitted surface" (Glossary: log of the invariant value). **Disposition: plain words** (replace with the plain words the reader names).


### List 3b. Sentences with three or more terms of art together

- "By {prf:ref}`thm-invariant`, a design with $V=v$ is a frontier design scaled by $v$, so $V-1$ is a relative improvement, meaningful relative to the band $1/\tau$." **Disposition: no change** (a definition, statement or proof step where the terms are the content; the unresolved ones are items in List 1 and the shorter ones items in Lists 2 and 3a).
- "It showed that the regressor places the energy differential of a proposal within its band (3 of 3), the easy part." **Disposition: no change** (a definition, statement or proof step where the terms are the content; the unresolved ones are items in List 1 and the shorter ones items in Lists 2 and 3a).
- "It did not show that it places the position along the frontier (0 of 3), and 3 proposals illustrate and do not estimate a rate." **Disposition: no change** (a definition, statement or proof step where the terms are the content; the unresolved ones are items in List 1 and the shorter ones items in Lists 2 and 3a).
- "The exponents and elasticities are features of the conditioned empirical model: they describe how the sampled designs trade, and not a causal exchange that changing a variable would reproduce." **Disposition: no change** (a definition, statement or proof step where the terms are the content; the unresolved ones are items in List 1 and the shorter ones items in Lists 2 and 3a).
- "A hole in the chart is an opportunity only where the trade space is log-convex around it, which the data cannot prove." **Disposition: no change** (a definition, statement or proof step where the terms are the content; the unresolved ones are items in List 1 and the shorter ones items in Lists 2 and 3a).
- "A deflation-style search for successive tensions, as PCA extracts components, is a research question: we claim neither that it works nor that tensions are orthogonal." **Disposition: no change** (a definition, statement or proof step where the terms are the content; the unresolved ones are items in List 1 and the shorter ones items in Lists 2 and 3a).
- "The research question is which kernel expansions keep the programs geometric programs, so that the guarantees and reading rules carry over." **Disposition: no change** (a definition, statement or proof step where the terms are the content; the unresolved ones are items in List 1 and the shorter ones items in Lists 2 and 3a).
- "Machine verification shows that a formula follows from its hypotheses and that the code agrees; it does not show that the hypotheses suit a table." **Disposition: no change** (a definition, statement or proof step where the terms are the content; the unresolved ones are items in List 1 and the shorter ones items in Lists 2 and 3a).


## Unit 30: paper/paper.ipynb :: Prior art, by family

Density 4.1 terms of art per 100 words (40/972); staged text `paper_prior-art-by-family.txt`.


### List 1. Terms unresolved from the unit and the Glossary

- "It scores each unit against the data by mathematical programming, with weights obtained from the data rather than set in advance [@banker1984some]; a super-efficiency variant ranks efficient units against a reference technology spanned by all other units [@andersen1993procedure], and Malmquist indices run across data sets [@fare1994productivity]." Terms: super-efficiency, reference technology, Malmquist indices. Three DEA terms of art, none defined here or in the Glossary, none standard for this reader. **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it).
- "Our metrics are larger-is-better with homogeneity from the simplex, in place of inputs, outputs and a choice of returns to scale." Terms: homogeneity from the simplex, returns to scale. Economics usage of "returns to scale" is not explained, and "homogeneity from the simplex" is not in the Glossary. **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it).
- "We solve one convex program and K refits, and return coordinates with a pull-back to attribute units." Term: pull-back. Differential-geometry word, not defined; the reader cannot tell what map is meant. **Disposition: no change** (standard vocabulary at the reader level the paper assumes (Boyd and Vandenberghe; scikit-learn)).
- "Frontier estimation by programming, corrected least squares and one-sided error is the family of one-sided fits, reviewed in [@battese1992frontier] after [@aigner1968estimating; @afriat1972efficiency; @aigner1977formulation]." Terms: corrected least squares, one-sided error. Econometric estimators that are neither defined nor in the Glossary. **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it).
- "The chart is in the spirit of log-ratio coordinates for compositional data [@aitchison1983principal; @egozcue2003isometric]." Terms: log-ratio coordinates, compositional data. Not defined; the Glossary "chart" does not say how it relates to them. **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it).
- "Pareto methods return a nondominated set and find its members by scalarization, for example the weighting method [@miettinen1999nonlinear; @ehrgott2005multicriteria]; evolutionary algorithms generate such sets [@zitzler1999multiobjective; @deb2002fast]." Term: weighting method. Named without a definition, and the Glossary has no entry for it. **Disposition: no change** (standard vocabulary at the reader level the paper assumes (Boyd and Vandenberghe; scikit-learn)).
- "Dominance is a hard comparison that stops discriminating, on this case, as metrics are added ({numref}`Section %s <sect-problem>` counts it), while the fit returns an exponent vector per facet, a band of near-frontier designs and an effective sample size." Term: effective sample size. Not in the Glossary and not defined in the unit; the reader cannot tell what it measures. **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it).
- "Combining these pieces in one estimator is our design." and the table row "Tradespace exploration" ("Value-focused broad exploration of design alternatives"). Term: value-focused. Unexplained qualifier of a method family. **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it).
- "Kernel PCA is the feature-engineering kin of the direction in {numref}`Section %s <sect-discussion>` [@schoelkopf1998nonlinear], and "hyperbolic" here is unrelated to hyperbolic PCA [@chami2021horopca]." Term: hyperbolic PCA. Named only to be excluded; the reader is never told what it is, and "direction" points to a section not given. **Disposition: no change** (standard vocabulary at the reader level the paper assumes (Boyd and Vandenberghe; scikit-learn)).
- "{ref}`Appendix G <appendix-g>` is the larger register; it is not exhaustive and says for every entry what this work does differently, extends or adds." Term: register. Used as a noun for a table of entries; not defined. **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it).


### List 2. Where a Glossary term would say it shorter or more exactly

- "The weighted geometric mean with exponents summing to one has the constant-returns Cobb-Douglas form [@cobb1928theory], and reading V as the factor that scales a design to the boundary is our distance-function reading, after Shephard's characterization of a technology by its distance function [@shephard1970theory; @fare1995multi; @farrell1957measurement]." Terms: invariant value ("weighted geometric mean with exponents summing to one", and bare "V"), improvement factor ("the factor that scales a design to the boundary"). **Disposition: no change** (the sentence reports a source in its own words (exempt by the note)).
- "Our boundary is a soft maximum with a temperature, a band and an effective sample size, not a boundary set by extreme units." Terms: fit temperature ("a temperature"), supporting envelope or fitted reference surface (Glossary says "frontier" is ambiguous; "boundary" here is unnamed). **Disposition: no change** (the sentence reports a source in its own words (exempt by the note)). **Routed to P1** (not edited here).
- "We solve one convex program and K refits, and return coordinates with a pull-back to attribute units." Terms: chart ("coordinates with a pull-back" is the reversible transformation), number of terms (K). **Disposition: no change** (the sentence reports a source in its own words (exempt by the note)).
- "The two meet in one result: a maximizer of V with positive exponents is Pareto-efficient ({prf:ref}`thm-pareto`)." Terms: invariant value (V), contending set ("positive exponents" are the metrics that contend). **Disposition: no change** (the sentence reports a source in its own words (exempt by the note)).
- Table cell "Returns no coordinate system and no exponents". Terms: chart (coordinate system), exponent vector (exponents). **Disposition: no change** (the sentence reports a source in its own words (exempt by the note)).
- Table cell "this method fits and reports a coordinate system and a score". Terms: chart, energy differential or novelty (the score). **Disposition: no change** (the sentence reports a source in its own words (exempt by the note)).
- "Our facets are piecewise log-linear with constant elasticities within a facet." Terms: log-metrics ("log-linear"), monomial or term (each facet is a hyperplane in log-metrics). **Disposition: no change** (the sentence reports a source in its own words (exempt by the note)).
- "Which part of the Pareto boundary the facets reach is our reading: the theorem gives efficiency of a maximizer, not the converse." Term: Pareto boundary is used correctly; "the facets reach" could be "the supporting envelope touches". Supporting envelope. **Disposition: no change** (the sentence reports a source in its own words (exempt by the note)).


### List 3a. Terms of art that plain words would serve

- "Kernel PCA is the feature-engineering kin of the direction in {numref}`Section %s <sect-discussion>` [@schoelkopf1998nonlinear], and "hyperbolic" here is unrelated to hyperbolic PCA [@chami2021horopca]." Term: feature-engineering kin. Plain words: "a close relative that builds new input features". **Disposition: no change** (the sentence reports a source in its own words (exempt by the note)).
- "Dominance is a hard comparison that stops discriminating, on this case, as metrics are added ({numref}`Section %s <sect-problem>` counts it), while the fit returns an exponent vector per facet, a band of near-frontier designs and an effective sample size." Term: stops discriminating. Plain words: "stops telling designs apart". **Disposition: no change** (the sentence reports a source in its own words (exempt by the note)).
- Table cell "The weights are fitted from the data's edge, not elicited". Term: elicited. Plain words: "asked of the decision maker". **Disposition: no change** (the sentence reports a source in its own words (exempt by the note)).
- "We fit one exponent vector per facet, a global named structure, where DEA obtains weights unit by unit, and practice has added weights restrictions [@allen1997weights] and protocols for applying it [@dyson2001pitfalls]." Term: global named structure. Plain words: "one set of weights for the whole surface, each with a name". **Disposition: no change** (the sentence reports a source in its own words (exempt by the note)).
- "Our boundary is a soft maximum with a temperature, a band and an effective sample size, not a boundary set by extreme units." Term: extreme units. Plain words: "the best individual designs". **Disposition: no change** (the sentence reports a source in its own words (exempt by the note)). **Routed to P1** (not edited here).


### List 3b. Sentences with three or more terms of art together

- "The weighted geometric mean with exponents summing to one has the constant-returns Cobb-Douglas form [@cobb1928theory], and reading V as the factor that scales a design to the boundary is our distance-function reading, after Shephard's characterization of a technology by its distance function [@shephard1970theory; @fare1995multi; @farrell1957measurement]." Terms: weighted geometric mean, constant-returns Cobb-Douglas, V, distance function. **Disposition: no change** (the sentence reports a source in its own words (exempt by the note)).
- "Our metrics are larger-is-better with homogeneity from the simplex, in place of inputs, outputs and a choice of returns to scale." Terms: larger-is-better, homogeneity, simplex, returns to scale. **Disposition: no change** (the sentence reports a source in its own words (exempt by the note)).
- "Our boundary is a soft maximum with a temperature, a band and an effective sample size, not a boundary set by extreme units." Terms: soft maximum, temperature, band, effective sample size. **Disposition: no change** (the sentence reports a source in its own words (exempt by the note)). **Routed to P1** (not edited here).
- "Dominance is a hard comparison that stops discriminating, on this case, as metrics are added ({numref}`Section %s <sect-problem>` counts it), while the fit returns an exponent vector per facet, a band of near-frontier designs and an effective sample size." Terms: dominance, exponent vector, facet, near-frontier, effective sample size. **Disposition: no change** (the sentence reports a source in its own words (exempt by the note)).
- "Frontier estimation by programming, corrected least squares and one-sided error is the family of one-sided fits, reviewed in [@battese1992frontier] after [@aigner1968estimating; @afriat1972efficiency; @aigner1977formulation]." Terms: frontier estimation, corrected least squares, one-sided error, one-sided fits. **Disposition: no change** (the sentence reports a source in its own words (exempt by the note)).
- "It scores each unit against the data by mathematical programming, with weights obtained from the data rather than set in advance [@banker1984some]; a super-efficiency variant ranks efficient units against a reference technology spanned by all other units [@andersen1993procedure], and Malmquist indices run across data sets [@fare1994productivity]." Terms: super-efficiency, reference technology, Malmquist indices, mathematical programming. **Disposition: no change** (the sentence reports a source in its own words (exempt by the note)).
- "The model class and refit scheme come from geometric programming and max-affine fitting [@boyd2007tutorial; @hoburg2016data; @magnani2009convex]; the soft maximum is an entropic risk functional [@foellmer2026entropic]." Terms: model class, geometric programming, max-affine fitting, soft maximum, entropic risk functional. **Disposition: no change** (the sentence reports a source in its own words (exempt by the note)). **Routed to P1** (not edited here).
- "Our facets are piecewise log-linear with constant elasticities within a facet." Terms: facet, piecewise log-linear, elasticities. **Disposition: no change** (the sentence reports a source in its own words (exempt by the note)).
- Table cell "A smooth soft maximum over a simplex-constrained geometric mean". Terms: soft maximum, simplex, geometric mean. **Disposition: no change** (the sentence reports a source in its own words (exempt by the note)). **Routed to P1** (not edited here).
- "Pareto methods return a nondominated set and find its members by scalarization, for example the weighting method [@miettinen1999nonlinear; @ehrgott2005multicriteria]; evolutionary algorithms generate such sets [@zitzler1999multiobjective; @deb2002fast]." Terms: nondominated set, scalarization, weighting method, evolutionary algorithms. **Disposition: no change** (the sentence reports a source in its own words (exempt by the note)).


## Unit 31: paper/supporting_material.ipynb :: Appendix E. Assumptions and abstraction gaps

Density 3.9 terms of art per 100 words (130/3297); staged text `supp_appendix-e-assumptions-and-abstraction-g.txt`.


### List 1. Terms unresolved from the unit and the Glossary

- "(a) The fitted reference surface: $\Phi(u)=w\cdot u-\beta=0$ at finite $\tau$ with $\beta=J_\tau(Uw)$ (L3, L5); $V>1$ is possible." Terms: $J_\tau$, $\beta$ as offset, L3, L5. Why: neither the soft-maximum functional nor the lemma labels are defined here or in the Glossary. **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it).
- "L11: a $V$-maximizer is weakly efficient; the converse is not claimed." Terms: L11, weakly efficient. Why: lemma label is opaque, and weak efficiency is not given for this setting. **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it).
- "L6: under A5 ($\varepsilon_j$ i.i.d. $N(0,\sigma^2)$, $\sigma>0$) and I5, $\tfrac1\tau\log E\,e^{\tau w\cdot\varepsilon}=\tau\sigma^2\lVert w\rVert^2/2$, an identity for the population expectation." Terms: L6, A5, I5. Why: assumption and invariant labels are unresolved without the ledger. **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it).
- "Proposition 3 (L14) is for step B, unpenalized, with support offsets $\beta_k=J_\tau(Uw_k)$; level 1 (descent) is for B only (I7); I8 requires a convex facet objective." Terms: step B, level 1, support offsets, I7, I8. Why: "step B" and the numbered levels are never defined in the unit or Glossary. **Disposition: no change** (standard vocabulary at the reader level the paper assumes (Boyd and Vandenberghe; scikit-learn)).
- "D: the near-frontier rows of a facet lie on one hyperplane in log space." Terms: D (the tangent step), near-frontier. Why: "D" is a bare letter; the tangent step it names is not defined. **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it).
- "The plain fit on a facet's own rows has its support function minimized at a vertex of the simplex when those rows lie in a cone of the chart that does not contain the origin." Terms: plain fit, own-rows, support function, sliver. Why: "sliver" and "plain fit" are not defined; "support function" is not the Glossary's "support weights". **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it).
- "R2 and L13: the margin $\gamma=\min_i[s_{i,k(i)}-\max_{k\ne k(i)}s_{ik}]$ is zero when a row lies on two facet planes; at $\tau=\infty$ a frontier row on a ridge has slack 0 for both facets; two identical facets tie on every row." Terms: R2, L13, $s_{ik}$, slack, ridge. Why: scores $s_{ik}$ and slack are not defined. **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it).
- "Corollary 4 bounds $F(W)-F^*_{\text{fixed}}$, where $F^*_{\text{fixed}}$ is the optimum for the fixed assignment of the returned run (L14)." Terms: Corollary 4, $F$, $W$. Why: the objective and parameter set are not introduced. **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it).
- "Mean slack ranks the restarts usefully." Terms: mean slack, restarts. Why: slack is not defined. **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it).
- "Level 3 conditions on R2 (positive margin), nonempty facets, exact facet optima ($G_k=0$) and offsets $\beta_k=J_\tau(Uw_k)$, with I8 (first-order convexity) and I9 (Cauchy-Schwarz) for the radius $\gamma/(2\max_i\lVert(u_i,-1)\rVert_2)$ and F12 for the minimum representation." Terms: Level 3, $G_k$, I9, F12, minimum representation. Why: $G_k$ (apparently the facet gap) and F12 are unresolved. **Disposition: no change** (standard vocabulary at the reader level the paper assumes (Boyd and Vandenberghe; scikit-learn)).
- "No theorem for the multi-facet alternation beyond I7 (the partition-and-refit pattern of Magnani and Boyd) and the three levels (L12 to L14), all local." Terms: alternation, the three levels. Why: the alternation (fit) algorithm is not described here. **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it).
- "The Linux CI run 42540318424 resolved one tied row differently from macOS, so `assignment_changes` counts a row only when its label trails the maximum score by more than `EPS_FEAS`; run 42541322671 on Linux stopped a tied seed at the iteration cap where macOS reports stationary without margin (`tests/test_solvers.py::test_r1_planted_certificates` accepts both for a zero margin)." Terms: `assignment_changes`, `EPS_FEAS`. Why: code identifiers, not in the Glossary. **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it).
- "Planted fits: maximum facet gap $\le10^{-12}$ after the polish (SLSQP alone left $4.7\times10^{-5}$ at $\tau=50$, none of 60 facets certified at $10^{-8}$); $\gamma\in(10^{-4},10^{-2})$ and radius in $(10^{-6},10^{-3})$ at $\tau=50$." Terms: polish, planted fits. Why: the polish step is never described. **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it).
- "Cubesat `conditioning_` (M3): $K=1$ 1.12 (primary), 0.522 (stock); $K=3$ primary 15.33, 4.01, 0.0949; stock 0.873, 0.154, 0.927." Terms: M3, primary, stock. Why: the two sampling regimes and the M-labelled measurements are not defined in this unit. **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it).
- "That the fraction above $V=1$ is monotone in $\tau$ at $K>1$ (it was bracketed at every $K$ observed); that $1/\tau$ corresponds to a noise level; that the selected $\tau$ is stable across seeds." Terms: bracketed, selected $\tau$. Why: the selection rule for $\tau$ is not stated. **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it).


### List 2. Where a Glossary term would say it shorter or more exactly

- "An exponent above the participation threshold at the working temperature participates; an exponent at or below $10^{-12}$ is mathematically zero; the restricted Hessian at the fit is positive definite." Term: numerically zero. Why: the Glossary says 1e-12 is numerically zero and not the same as mathematically zero; the sentence calls it mathematically zero. **Disposition: glossary term** (use the Glossary term the reader names).
- "Stability: the smallest eigenvalue of that matrix." Term: conditioning of the exponents. Why: that is the Glossary's exact definition. **Disposition: glossary term** (use the Glossary term the reader names).
- "An exponent at or below $10^{-12}$ is zero; a row with a zero metric carries no information about the other exponents." Term: numerically zero. Why: the Glossary name marks the code convention against true zero. **Disposition: glossary term** (use the Glossary term the reader names).
- "R2 and L13: the margin $\gamma=\min_i[s_{i,k(i)}-\max_{k\ne k(i)}s_{ik}]$ is zero when a row lies on two facet planes; at $\tau=\infty$ a frontier row on a ridge has slack 0 for both facets; two identical facets tie on every row." Term: assignment margin. Why: "the margin" is the Glossary's smallest gap by which a facet beats the runner-up. **Disposition: glossary term** (use the Glossary term the reader names).
- "The contending set is the support of $w$; identified only where the restricted Hessian is positive definite (G-2) and the facet's frontier rows determine the plane (G-7)." Terms: contending set, exponent vector. Why: "support of $w$" is the positive entries of the exponent vector. **Disposition: glossary term** (use the Glossary term the reader names).
- "$V=1$ reads as the reference level of a fitted object; $V>1$ is beyond the fitted reference surface, a candidate to test, not a point proved attainable or unattainable; Pareto statements are made only for maximizers, through L11." Terms: novelty, level offset. Why: "beyond the fitted reference surface" is the Glossary's novelty, and the level V = 1 is its level offset. **Disposition: glossary term** (use the Glossary term the reader names).
- "Under D or the penalty the fit is an option with first-order diagnostics; the certificate columns are read as diagnostics and no local-optimality statement is made." Terms: termination status, facet gap. Why: "certificate columns" are these two reported quantities. **Disposition: glossary term** (use the Glossary term the reader names).
- "The sampled designs reach the boundary of the attainable set (the data are near-frontier somewhere); $\tau$ is chosen so a stated fraction of rows lies above $V=1$; only the log-convex part of a Pareto front is reached by some $w$ (L11)." Terms: fit temperature, Pareto boundary. Why: "$\tau$" is the fit temperature, and "Pareto front" should be "Pareto boundary". **Disposition: glossary term** (use the Glossary term the reader names).
- "A fit with $\gamma=0$ is first-order stationary per facet (levels 1 and 2) with no local-optimality claim; facet numbers are labels, never identities." Terms: termination status ("stationary without margin"), assignment margin. Why: that is exactly the Glossary status. **Disposition: glossary term** (use the Glossary term the reader names).


### List 3a. Terms of art that plain words would serve

- "Step B is a choice supported by measurement on the planted family; it is not a theorem about every geometry." Term: planted family. Plain: synthetic data built with a known frontier. **Disposition: plain words** (replace with the plain words the reader names).
- "G-6. The sliver claim (observed, not proved)." Term: sliver. Plain: narrow wedge of rows. **Disposition: plain words** (replace with the plain words the reader names).
- "Beyond it: event detection on the error norm for the sub-step part of the resolution, and a different definition of the time for the grazing case (for instance the last exit from the band, or the time at which the error stays inside for a hold)." Terms: grazing case, sub-step. Plain: the case where the error only touches the band edge; finer than one time step. **Disposition: plain words** (replace with the plain words the reader names).
- "That the step-quantized time converges to the first crossing time as the step shrinks; that the map from design to time is continuous where the trajectory touches the band; that the printed digits of any quantity computed from the two times are reproducible." Term: step-quantized. Plain: time read off the simulation step grid. **Disposition: plain words** (replace with the plain words the reader names).
- "A facet with few frontier rows is reported with its exponents and counted near-frontier rows; its exponents are read as a family member, not a point." Term: family member. Plain: one of several equally good exponent sets. **Disposition: plain words** (replace with the plain words the reader names).


### List 3b. Sentences with three or more terms of art together

- "Uniqueness: strict convexity on the simplex tangent space, the restricted Hessian $\tau(U^\top\mathrm{diag}(p)U-(U^\top p)(U^\top p)^\top)$ positive definite on the participating coordinates (L3, L4, R1)." Terms: strict convexity, simplex tangent space, restricted Hessian, positive definite, participating coordinates, lemma labels. **Disposition: no change** (a definition, statement or proof step where the terms are the content; the unresolved ones are items in List 1 and the shorter ones items in Lists 2 and 3a).
- "The plain fit on a facet's own rows has its support function minimized at a vertex of the simplex when those rows lie in a cone of the chart that does not contain the origin." Terms: plain fit, support function, vertex of the simplex, cone, chart. **Disposition: no change** (a definition, statement or proof step where the terms are the content; the unresolved ones are items in List 1 and the shorter ones items in Lists 2 and 3a).
- "Proposition 3 (L14) is for step B, unpenalized, with support offsets $\beta_k=J_\tau(Uw_k)$; level 1 (descent) is for B only (I7); I8 requires a convex facet objective." Terms: Proposition 3, step B, support offsets, level 1, I7, I8, facet objective. **Disposition: no change** (a definition, statement or proof step where the terms are the content; the unresolved ones are items in List 1 and the shorter ones items in Lists 2 and 3a).
- "Level 3 conditions on R2 (positive margin), nonempty facets, exact facet optima ($G_k=0$) and offsets $\beta_k=J_\tau(Uw_k)$, with I8 (first-order convexity) and I9 (Cauchy-Schwarz) for the radius $\gamma/(2\max_i\lVert(u_i,-1)\rVert_2)$ and F12 for the minimum representation." Terms: level 3, R2, margin, facet optima, offsets, I8, I9, F12, radius. **Disposition: no change** (a definition, statement or proof step where the terms are the content; the unresolved ones are items in List 1 and the shorter ones items in Lists 2 and 3a).
- "L6: under A5 ($\varepsilon_j$ i.i.d. $N(0,\sigma^2)$, $\sigma>0$) and I5, $\tfrac1\tau\log E\,e^{\tau w\cdot\varepsilon}=\tau\sigma^2\lVert w\rVert^2/2$, an identity for the population expectation." Terms: L6, A5, I5, cumulant form, population expectation. **Disposition: no change** (a definition, statement or proof step where the terms are the content; the unresolved ones are items in List 1 and the shorter ones items in Lists 2 and 3a).
- "No theorem for the multi-facet alternation beyond I7 (the partition-and-refit pattern of Magnani and Boyd) and the three levels (L12 to L14), all local." Terms: multi-facet alternation, I7, partition-and-refit, three levels, L12 to L14. **Disposition: no change** (a definition, statement or proof step where the terms are the content; the unresolved ones are items in List 1 and the shorter ones items in Lists 2 and 3a).
- "The contending set is the support of $w$; identified only where the restricted Hessian is positive definite (G-2) and the facet's frontier rows determine the plane (G-7)." Terms: contending set, support of $w$, restricted Hessian, positive definite, frontier rows. **Disposition: no change** (a definition, statement or proof step where the terms are the content; the unresolved ones are items in List 1 and the shorter ones items in Lists 2 and 3a).
- "The fit minimizes $J_\tau(Uw)$ on the simplex; for one row it is $\min_w w\cdot u_1$, attained at the vertex on the row's smallest log-metric, a single-metric degenerate case and not a trade-off, so the fitted object is not defined for the input." Terms: $J_\tau$, simplex, vertex, log-metric, degenerate case, trade-off. **Disposition: no change** (a definition, statement or proof step where the terms are the content; the unresolved ones are items in List 1 and the shorter ones items in Lists 2 and 3a).


## Unit 32: paper/paper.ipynb :: Search of the design space (preliminary)

Density 3.7 terms of art per 100 words (8/217); staged text `paper_search-of-the-design-space-preliminary-.txt`.


### List 1. Terms unresolved from the unit and the Glossary

- "The outer loop evaluates the proposals, appends them to the table, refits, and repeats until the supporting envelope stops moving beyond the noise band." Term: noise band. Not in the Glossary (the Glossary's "band" is the fit-temperature band of near-frontier designs, a different thing); no size or estimate of the noise is given, so the stopping rule cannot be applied. **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it).
- "Ascent may reach only the log-convex part of the Pareto boundary (our reading)." Term: log-convex part. Not defined; it is unclear whether this means convex in log-metrics, or the portion of the boundary a facet can touch. **Disposition: no change** (standard vocabulary at the reader level the paper assumes (Boyd and Vandenberghe; scikit-learn)).
- "Outward monotonicity is stated for the exact maximum and not for the soft one; neither has a lemma here." Term: outward monotonicity. Not defined or in the Glossary; the reader cannot tell what is monotone, outward from what, or in which variable. **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it).
- "Because evaluation is noisy, the procedure resembles a diffusion with drift along the tangent spaces." Terms: diffusion with drift, tangent spaces. A stochastic-process image with no model given; "tangent spaces" of which object (the facets, the boundary) is not said. **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it).
- "A convergence theorem for the nested scheme is a goal, and the scheme motivates the kernel direction of {numref}`Section %s <sect-discussion>`." Term: kernel direction. Not in the Glossary; with only these files the reader has no way to say which kernel (fitting, regression, or the kernel of a map) is meant. The unrendered {numref} markup also leaves the cross-reference empty. **Disposition: no change** (standard vocabulary at the reader level the paper assumes (Boyd and Vandenberghe; scikit-learn)).
- "...estimated by finite differences or a supervised regressor; a categorical variable is a finite comparison." Term: finite comparison. Not defined; it is unclear what is compared and what direction results for a categorical variable. **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it).


### List 2. Where a Glossary term would say it shorter or more exactly

- "The middle loop proposes: on each facet the normal is an ascent direction in log space, chained back through the conditioning and the evaluation to a direction in configuration space, estimated by finite differences or a supervised regressor; a categorical variable is a finite comparison." Terms: exponent vector (for "the normal"), log-metrics (for "log space"), configuration (for "configuration space"). Each is the Glossary's exact name for the object. **Disposition: glossary term** (use the Glossary term the reader names).
- "Outward monotonicity is stated for the exact maximum and not for the soft one; neither has a lemma here." Terms: supporting envelope (for "the exact maximum") and fit temperature (for "the soft one", i.e. finite temperature). The Glossary names the infinite-temperature fit and the finite-temperature fit exactly. **Disposition: glossary term** (use the Glossary term the reader names).
- "Ascent may reach only the log-convex part of the Pareto boundary (our reading)." Term: fitted reference surface or supporting envelope, whichever the ascent actually climbs; "Pareto boundary" here is correct but the ascent is on the fit, so the sentence does not say which object reaches which. **Disposition: glossary term** (use the Glossary term the reader names).
- "The inner loop identifies, fitting the facets to the current table." Term: number of designs / configuration (the table is "the rows of the table, each row one evaluated configuration"); "the current table" could say the evaluated designs. **Disposition: glossary term** (use the Glossary term the reader names).


### List 3a. Terms of art that plain words would serve

- "...estimated by finite differences or a supervised regressor..." Term: supervised regressor. Plain words: "a model fitted to the evaluated designs". **Disposition: plain words** (replace with the plain words the reader names).
- "Because evaluation is noisy, the procedure resembles a diffusion with drift along the tangent spaces." Term: diffusion with drift. Plain words: "a random walk that is pushed steadily along the facets". **Disposition: plain words** (replace with the plain words the reader names).
- "The theory treats variables as continuous within a category." Term: continuous within a category. Plain words: "treats numeric choices as smooth, within each fixed choice of category". **Disposition: plain words** (replace with the plain words the reader names).
- "A convergence theorem for the nested scheme is a goal..." Term: nested scheme. Plain words: "the three loops together". **Disposition: plain words** (replace with the plain words the reader names).


### List 3b. Sentences with three or more terms of art together

- "The middle loop proposes: on each facet the normal is an ascent direction in log space, chained back through the conditioning and the evaluation to a direction in configuration space, estimated by finite differences or a supervised regressor; a categorical variable is a finite comparison." Terms: facet, normal, ascent direction, log space, conditioning, evaluation, configuration space, finite differences, supervised regressor, categorical variable. **Disposition: no change** (a definition, statement or proof step where the terms are the content; the unresolved ones are items in List 1 and the shorter ones items in Lists 2 and 3a).
- "Because evaluation is noisy, the procedure resembles a diffusion with drift along the tangent spaces." Terms: evaluation, diffusion with drift, tangent spaces. **Disposition: no change** (a definition, statement or proof step where the terms are the content; the unresolved ones are items in List 1 and the shorter ones items in Lists 2 and 3a).
- "The outer loop evaluates the proposals, appends them to the table, refits, and repeats until the supporting envelope stops moving beyond the noise band." Terms: refit, supporting envelope, noise band. **Disposition: no change** (a definition, statement or proof step where the terms are the content; the unresolved ones are items in List 1 and the shorter ones items in Lists 2 and 3a).
- "A convergence theorem for the nested scheme is a goal, and the scheme motivates the kernel direction of {numref}`Section %s <sect-discussion>`." Terms: convergence theorem, nested scheme, kernel direction. **Disposition: no change** (a definition, statement or proof step where the terms are the content; the unresolved ones are items in List 1 and the shorter ones items in Lists 2 and 3a).
- "Outward monotonicity is stated for the exact maximum and not for the soft one; neither has a lemma here." Terms: outward monotonicity, exact maximum, soft maximum, lemma. **Disposition: no change** (a definition, statement or proof step where the terms are the content; the unresolved ones are items in List 1 and the shorter ones items in Lists 2 and 3a). **Routed to P1** (not edited here).


## Unit 33: paper/supporting_material.ipynb :: Appendix G. Register of prior art (part 1)

Density 3.5 terms of art per 100 words (69/1953); staged text `supp_appendix-g-register-of-prior-art_1.txt`.


### List 1. Terms unresolved from the unit and the Glossary

- "A maximizer of a weighted geometric mean with positive exponents is Pareto-efficient (lemma L11), and the weights act as a trade-off." Terms: lemma L11; "the weights act as a trade-off". L11 is not stated or linked here, and "weights" is not tied to the Glossary's exponent vector or elasticity. **Disposition: no change** (standard vocabulary at the reader level the paper assumes (Boyd and Vandenberghe; scikit-learn)).
- "Returns no coordinate system and no exponents: a nondominated set says which designs survive, the fit says what trades against what, with one exponent vector per facet, a band of near-boundary designs and an effective sample size." Terms: effective sample size. Used here and in the DEA entry; neither defined nor in the Glossary (support weights is the nearest). **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it).
- "One exponent vector per facet, a global named structure, in place of weights obtained unit by unit; piecewise log-linear facets with constant elasticities within a facet; larger-is-better metrics with homogeneity by the simplex in place of inputs, outputs and a returns-to-scale choice; a soft maximum with a temperature, a band and an effective sample size in place of a deterministic boundary set by extreme units; one convex program and K refits; coordinates and a pull-back to attribute units in place of a score and a peer set." Terms: homogeneity by the simplex; returns-to-scale choice; pull-back; peer set; K refits; "global named structure". None defined in the unit or Glossary. **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it).
- "Evaluates the relative efficiency of each decision-making unit by mathematical programming on the observed data, with weights obtained from the data, with variants for scale and returns to scale, a super-efficiency variant that ranks efficient units against a reference technology spanned by all other units, and Malmquist productivity indices across data sets." Terms: decision-making unit; super-efficiency; reference technology; Malmquist index. DEA/economics vocabulary outside the stated reader level and undefined. **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it).
- "The chart Z = Bu is in the spirit of an isometric logratio chart." Terms: Z, B, u; isometric logratio chart. The Glossary defines "chart" but not these symbols or the logratio chart. **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it).
- "The criterion is one-sided, and the weights lie on the simplex; the chart is paired with the level log V and is reversible to the metrics and to attribute units." Terms: criterion; "level log V". The Glossary has level offset (the energy differential) but not "level log V" as written. **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it).
- "The model class, the K > 1 refit scheme and the sparsity option." Terms: refit scheme; sparsity option. Neither is explained here or in the Glossary (facet gap mentions a refit only in passing). **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it).
- "PCA in an implicit feature space, and PCA in hyperbolic space with horospherical projections." Terms: horospherical projections. Undefined and not standard at the reader level. **Disposition: no change** (standard vocabulary at the reader level the paper assumes (Boyd and Vandenberghe; scikit-learn)).
- "Decision analysis with a normative versus descriptive distinction; multiple-objective preferences and value trade-offs; weighted-criteria comparison methods (Pugh, AHP, Kepner-Tregoe); a decision-management framework based on decision theory and cost analysis." Terms: Pugh, AHP, Kepner-Tregoe. Method names given with no gloss. **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it).
- "The Cobb-Douglas production form, and the Shephard distance function with its duality." Terms: Shephard distance function; its duality. Economics terms, undefined. **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it).


### List 2. Where a Glossary term would say it shorter or more exactly

- "Returns no coordinate system and no exponents: a nondominated set says which designs survive, the fit says what trades against what, with one exponent vector per facet, a band of near-boundary designs and an effective sample size." Term: fit temperature ("a band of near-frontier designs"); "near-boundary" is also loose against Pareto boundary. **Disposition: no change** (the sentence reports a source in its own words (exempt by the note)).
- "This is not just a Pareto front: a front is the set of designs that no other design dominates, while the fit returns a reference surface with coordinates, and for each facet the exponents that give the elasticities between metrics." Terms: Pareto boundary (for "Pareto front" and "front"), fitted reference surface (for "a reference surface"). **Disposition: no change** (the sentence reports a source in its own words (exempt by the note)).
- "A one-sided envelope of the data, a score per unit, scores beyond the boundary (V above 1) and a boundary that moves between data sets." Terms: supporting envelope; novelty / energy differential ("scores beyond the boundary (V above 1)"). **Disposition: no change** (the sentence reports a source in its own words (exempt by the note)).
- "This is not just log-ratio analysis: the log-ratio chart is one half of the coordinate system, and the other half is the level log V relative to a fitted one-sided surface, which log-ratio analysis does not fit." Terms: energy differential (or level offset) for "the level log V relative to a fitted one-sided surface"; fitted reference surface. **Disposition: no change** (the sentence reports a source in its own words (exempt by the note)).
- "The criterion is one-sided, and the weights lie on the simplex; the chart is paired with the level log V and is reversible to the metrics and to attribute units." Terms: exponent vector ("the weights lie on the simplex"); energy differential ("the level log V"). **Disposition: no change** (the sentence reports a source in its own words (exempt by the note)).
- "The sources fit regression surfaces; this method fits an envelope, the one-sided boundary of the data, and reads its exponents as elasticities." Term: supporting envelope ("an envelope, the one-sided boundary of the data"). **Disposition: no change** (the sentence reports a source in its own words (exempt by the note)).
- "This is not just geometric-programming or max-affine fitting: those fit a surface through the middle of the data by regression, while this fits the edge of the data and reports the terms as trade-offs." Terms: fitted reference surface / supporting envelope ("the edge of the data"); elasticity ("trade-offs"). **Disposition: no change** (the sentence reports a source in its own words (exempt by the note)).
- "The weights are fitted from the data's edge, not elicited." Terms: exponent vector; supporting envelope. **Disposition: no change** (the sentence reports a source in its own words (exempt by the note)).
- "A smooth soft maximum over a simplex-constrained geometric mean in place of a shifted intercept, and K facets." Terms: invariant value ("a simplex-constrained geometric mean"); number of terms ("K facets"). **Disposition: no change** (the sentence reports a source in its own words (exempt by the note)).
- "The weighted geometric mean with exponents summing to one is the constant-returns Cobb-Douglas form; V read as a scaling factor to the boundary is a distance-function reading." Terms: invariant value; improvement factor ("a scaling factor to the boundary"). **Disposition: no change** (the sentence reports a source in its own words (exempt by the note)).


### List 3a. Terms of art that plain words would serve

- "Identification from a table, not generation of designs." Term: identification. Plain words: fitting a model to a table of designs. **Disposition: no change** (the sentence reports a source in its own words (exempt by the note)).
- "larger-is-better metrics with homogeneity by the simplex in place of inputs, outputs and a returns-to-scale choice" (in the DEA differently-sentence quoted in full under List 1). Term: homogeneity by the simplex. Plain words: exponents that sum to one, so doubling every metric doubles the score. **Disposition: no change** (the sentence reports a source in its own words (exempt by the note)).
- "coordinates and a pull-back to attribute units in place of a score and a peer set" (same sentence). Term: pull-back. Plain words: mapping back to attribute units. **Disposition: no change** (the sentence reports a source in its own words (exempt by the note)).
- "Decision analysis with a normative versus descriptive distinction; multiple-objective preferences and value trade-offs; weighted-criteria comparison methods (Pugh, AHP, Kepner-Tregoe); a decision-management framework based on decision theory and cost analysis." Term: normative versus descriptive. Plain words: how decisions should be made versus how people make them. **Disposition: no change** (the sentence reports a source in its own words (exempt by the note)).
- "Kernel PCA is the feature-engineering kin of the kernel direction that stays compatible with geometric programming." Term: feature-engineering kin. Plain words: a close relative among feature-building methods. **Disposition: no change** (the sentence reports a source in its own words (exempt by the note)).
- "A one-sided envelope of the data, a score per unit, scores beyond the boundary (V above 1) and a boundary that moves between data sets." Term: scores beyond the boundary. Plain words: scores above 1. **Disposition: no change** (the sentence reports a source in its own words (exempt by the note)).


### List 3b. Sentences with three or more terms of art together

- "Geometric programming with generalized posynomials, aircraft design as geometric programs with fits compatible with them, softmax-affine fits compatible with geometric programming, convex piecewise-linear fits, and reweighted l1 sparsity." Terms: geometric programming; generalized posynomials; softmax-affine fits; convex piecewise-linear fits; reweighted l1 sparsity. **Disposition: no change** (the sentence reports a source in its own words (exempt by the note)).
- "One exponent vector per facet, a global named structure, in place of weights obtained unit by unit; piecewise log-linear facets with constant elasticities within a facet; larger-is-better metrics with homogeneity by the simplex in place of inputs, outputs and a returns-to-scale choice; a soft maximum with a temperature, a band and an effective sample size in place of a deterministic boundary set by extreme units; one convex program and K refits; coordinates and a pull-back to attribute units in place of a score and a peer set." Terms: exponent vector, facet, elasticities, simplex, returns to scale, soft maximum, temperature, effective sample size, pull-back, peer set. **Disposition: no change** (the sentence reports a source in its own words (exempt by the note)).
- "Evaluates the relative efficiency of each decision-making unit by mathematical programming on the observed data, with weights obtained from the data, with variants for scale and returns to scale, a super-efficiency variant that ranks efficient units against a reference technology spanned by all other units, and Malmquist productivity indices across data sets." Terms: decision-making unit; returns to scale; super-efficiency; reference technology; Malmquist index. **Disposition: no change** (the sentence reports a source in its own words (exempt by the note)).
- "Estimates frontier production functions by programming, corrected ordinary least squares or maximum likelihood, and stochastic frontiers with one-sided error, as reviewed by Battese (1992)." Terms: frontier production functions; corrected ordinary least squares; maximum likelihood; stochastic frontiers; one-sided error. **Disposition: no change** (the sentence reports a source in its own words (exempt by the note)).
- "A smooth soft maximum over a simplex-constrained geometric mean in place of a shifted intercept, and K facets." Terms: soft maximum; simplex; geometric mean; facets. **Disposition: no change** (the sentence reports a source in its own words (exempt by the note)).
- "The weighted geometric mean with exponents summing to one is the constant-returns Cobb-Douglas form; V read as a scaling factor to the boundary is a distance-function reading." Terms: weighted geometric mean; constant-returns; Cobb-Douglas form; distance function. **Disposition: no change** (the sentence reports a source in its own words (exempt by the note)).
- "The criterion is one-sided, and the weights lie on the simplex; the chart is paired with the level log V and is reversible to the metrics and to attribute units." Terms: one-sided criterion; simplex; chart; level log V; attribute units. **Disposition: no change** (the sentence reports a source in its own words (exempt by the note)).
- "The log-mean-exp soft maximum is the sample version of the entropic risk functional." Terms: log-mean-exp; soft maximum; entropic risk functional. **Disposition: no change** (the sentence reports a source in its own words (exempt by the note)).
- "The entropic risk measure and its limits (the mean and the essential supremum), and entropic value-at-risk." Terms: entropic risk measure; essential supremum; entropic value-at-risk. **Disposition: no change** (the sentence reports a source in its own words (exempt by the note)).


## Unit 34: paper/supporting_material.ipynb :: Appendix B. Proofs, step for step with their scripts (part 9)

Density 3.2 terms of art per 100 words (78/2423); staged text `supp_appendix-b-proofs-step-for-step-with-the_9.txt`.


### List 1. Terms unresolved from the unit and the Glossary

- "Soft-weight alternation: with weights alpha\_ik = softmax\_k(kappa score\_ik) from the current model, (i) a convex program symmetric in the terms attains its minimum with all terms equal, so the objective over all terms is not convex in them in general; (ii) the soft model's slack is bounded above by the fixed-weight objective, with equality at the weights' own model; (iii) the fixed-weight objective is a generalized posynomial in exp(w)." Terms: soft-weight alternation, fixed-weight objective, score, slack, soft model, "the weights' own model". None is defined here or in the Glossary; the reader cannot tell what is being alternated or what "slack" measures. **Disposition: add to avoid** (the phrase is withdrawn by WP10 Amendment 4 (R-33, R-34, R-37)).
- "the shifted sum over the terms equals the unshifted sum, so row i's soft slack is" Term: soft slack. Used with no definition of slack (a gap between what and what), and the sentence is cut off. **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it).
- "by declared axiom **A6** (posited): the extension temperature is positive, kappa \> 0, and each of the K terms has exponents theta\_k on the simplex" Term: extension temperature. Not in the Glossary; it is unclear whether it is the term temperature or the fit temperature. **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it).
- "Gibbs: log sum\_k exp(kappa x) - sum\_k alpha (kappa x - log alpha) = Jensen slack" Term: Gibbs (inequality/variational identity). Not defined in the unit, not in the Glossary, and not a standard name at the convex-optimization level. **Disposition: no change** (standard vocabulary at the reader level the paper assumes (Boyd and Vandenberghe; scikit-learn)).
- "the mean over rows of the alpha-weighted slack is sum\_k (n\_k/N)(beta\_k - ubar\_k.w\_k)" Terms: n\_k, N, beta\_k, ubar\_k. These symbols are never defined in the unit or the Glossary. **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it).
- "the mean of the nonnegative Jensen slacks is nonnegative: F \<= G\_alpha - E" Terms: G\_alpha, E. Neither symbol is defined, so the bound cannot be read. **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it).
- "the licensed logarithm of y\_k = exp(kappa x\_k)/alpha\_k: the sum alpha f(y)" Term: licensed logarithm. Ledger jargon with no definition; the sentence is also cut off. **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it).
- "the product over the terms is a generalized posynomial (I15's premise held at L16.31)" Term: premise held. It is unclear what "premise" refers to without the lemma script. **Disposition: add to avoid** (the phrase is withdrawn by WP10 Amendment 4 (R-33, R-34, R-37)).


### List 2. Where a Glossary term would say it shorter or more exactly

- "by declared axiom **A6** (posited): the extension temperature is positive, kappa \> 0, and each of the K terms has exponents theta\_k on the simplex" Terms: term temperature, exponent vector, number of terms. "Term temperature" and "exponent vector" name these exactly. **Disposition: glossary term** (use the Glossary term the reader names).
- "by declared axiom **A3** (posited): the soft-maximum temperature is positive: tau \> 0" Term: fit temperature. The Glossary names the soft-maximum hardness this way. **Disposition: glossary term** (use the Glossary term the reader names).
- "by declared axiom **A2** (posited): the exponents w lie on the simplex: w\_j \>= 0 and sum\_j w\_j = 1" Term: exponent vector. **Disposition: glossary term** (use the Glossary term the reader names).
- "by declared axiom **A1** (posited): metrics are strictly positive, larger-is-better: m\_i\[j\] \> 0, so u = log m is defined" Terms: metrics, log-metrics. The Glossary says "log-metrics" for u. **Disposition: glossary term** (use the Glossary term the reader names).
- "A1: the log-metrics are real, so the scores x\_ik, x0\_ik (current model) are real" Term: log-metrics (already used), with "scores" possibly meaning the facet or term scores. The Glossary has no "score" entry, so "score" is unresolved. **Disposition: glossary term** (use the Glossary term the reader names).
- "shifting the K terms by s in 0..K-1 sends position k to term k+s, wrapped: the head" Term: number of terms (K). **Disposition: glossary term** (use the Glossary term the reader names).
- "Soft-weight alternation: with weights alpha\_ik = softmax\_k(kappa score\_ik) from the current model" Term: term temperature. The Glossary entry "the temperature of the soft weights over the terms in the several-term fit" describes exactly these weights. **Disposition: glossary term** (use the Glossary term the reader names).
- "A2: the exponents w\_kj are real (on the simplex), so x\_kj = exp(w\_kj) \> 0" Terms: exponent vector, chart. The exp(w) change of variables is the Glossary's chart or the convex change x = exp(y). **Disposition: glossary term** (use the Glossary term the reader names).


### List 3a. Terms of art that plain words would serve

- "A2 licenses the logarithms: log prod\_k P\_k^(n\_k/(N tau)) \* Mono\_k = G\_alpha(W)" Term: licenses. Plain words: "guarantees the arguments are positive, so the logarithms exist". **Disposition: plain words** (replace with the plain words the reader names).
- "by declared axiom **A1** (posited): ... " and "by declared axiom **I14** (inherited): ..." Terms: posited, inherited. Plain words: "assumed" and "taken from an earlier lemma". **Disposition: plain words** (replace with the plain words the reader names).
- "tightness: at x = x0 the same slack is 0 (log alpha = kappa x0 - log Z0)" Term: tightness. Plain words: "the bound holds with equality". **Disposition: plain words** (replace with the plain words the reader names).
- "the alpha-weighted mean slack regroups by terms" Term: regroups. Plain words: "can be rewritten as a sum over terms". **Disposition: plain words** (replace with the plain words the reader names).
- "shifting the K terms by s in 0..K-1 sends position k to term k+s, wrapped: the head" Term: cyclic shift (wrapped). Plain words: "rotating the order of the terms". **Disposition: plain words** (replace with the plain words the reader names).


### List 3b. Sentences with three or more terms of art together

- "Soft-weight alternation: with weights alpha\_ik = softmax\_k(kappa score\_ik) from the current model, (i) a convex program symmetric in the terms attains its minimum with all terms equal, so the objective over all terms is not convex in them in general; (ii) the soft model's slack is bounded above by the fixed-weight objective, with equality at the weights' own model; (iii) the fixed-weight objective is a generalized posynomial in exp(w)." Terms: softmax, temperature kappa, score, slack, fixed-weight objective, generalized posynomial. **Disposition: add to avoid** (the phrase is withdrawn by WP10 Amendment 4 (R-33, R-34, R-37)).
- "by declared axiom **A6** (posited): the extension temperature is positive, kappa \> 0, and each of the K terms has exponents theta\_k on the simplex" Terms: extension temperature, terms, exponents, simplex. **Disposition: no change** (a definition, statement or proof step where the terms are the content; the unresolved ones are items in List 1 and the shorter ones items in Lists 2 and 3a).
- "by declared axiom **I15** (inherited): a function of positive variables formed from posynomials using addition, multiplication, positive (fractional) power and maximum is a generalized posynomial (the definition)" Terms: posynomial, positive power, maximum, generalized posynomial. **Disposition: add to avoid** (the phrase is withdrawn by WP10 Amendment 4 (R-33, R-34, R-37)).
- "I14 with f = -log: the row's Jensen slack sum\_k alpha (-log y\_k) + LSE" Terms: Jensen slack, row, LSE (log-sum-exp, not expanded here), weights alpha. **Disposition: no change** (a definition, statement or proof step where the terms are the content; the unresolved ones are items in List 1 and the shorter ones items in Lists 2 and 3a).
- "the mean over rows of the alpha-weighted slack is sum\_k (n\_k/N)(beta\_k - ubar\_k.w\_k)" Terms: alpha-weighted slack, mean over rows, beta\_k, ubar\_k, with n\_k and N all undefined. **Disposition: no change** (a definition, statement or proof step where the terms are the content; the unresolved ones are items in List 1 and the shorter ones items in Lists 2 and 3a).
- "the mean of the nonnegative Jensen slacks is nonnegative: F \<= G\_alpha - E" Terms: Jensen slack, F, G\_alpha, E. **Disposition: no change** (a definition, statement or proof step where the terms are the content; the unresolved ones are items in List 1 and the shorter ones items in Lists 2 and 3a).
- "A3: the power n\_k/(N tau) of the posynomial is positive (alpha \> 0, tau \> 0)" Terms: posynomial, power, alpha, tau (fit temperature). **Disposition: no change** (a definition, statement or proof step where the terms are the content; the unresolved ones are items in List 1 and the shorter ones items in Lists 2 and 3a).


## Unit 35: paper/supporting_material.ipynb :: Appendix D. Extended results: what the method found in the table (part 1)

Density 3.2 terms of art per 100 words (148/4667); staged text `supp_appendix-d-extended-results-what-the-met_1.txt`.


### List 1. Terms unresolved from the unit and the Glossary

- "The settling time and the slew time are read off the accepted steps of an adaptive integration, so a relative change of 1e-12 in a design variable can move them by up to half a second, and by much more where the error trajectory grazes the settling band (gap G-17)." Term: "gap G-17" (also "gap G-10" in D.14). A numbered gap with no definition or pointer in the unit or Glossary. **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it).
- "The record also holds the maximal gap, the Corollary bound, the margin, the stable radius and the shares." Term: "Corollary bound". No corollary is stated or cited, and "bound" is not in the Glossary; the table column "bound" is unexplained. **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it).
- "`certified`: the assignment is fixed, residuals and gaps are within tolerance, no facet is empty and the margin is positive; levels 1 to 3 hold." Term: "levels 1 to 3". The Glossary says only that termination status is a "level of guarantee"; what the levels are is never given. "Residuals" is also unspecified. **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it).
- "The diagnostic `conditioning_` of the estimator is the smallest eigenvalue of the restricted Hessian at each facet's fit; a small value flags a nearly flat direction, so weakly identified exponents." Term: "restricted Hessian". Restricted to what is not stated, here or in the Glossary. **Disposition: no change** (standard vocabulary at the reader level the paper assumes (Boyd and Vandenberghe; scikit-learn)).
- "`mean_slack_` is defined for every K and is comparable across K at one temperature; `objective_` is the soft maximum at one term and the mean slack at several, and is not." Terms: "mean slack", "objective_". Neither is defined; slack relative to what is not said. **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it).
- "Here the two refits are compared with the true labels given, so the alternation plays no part." Term: "alternation". The alternating procedure is not described in the unit or Glossary; "own-rows refit" versus "support refit" is likewise unexplained here. **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it).
- "The settling time and the slew time are read off the accepted steps of an adaptive integration, so a relative change of 1e-12 in a design variable can move them by up to half a second, and by much more where the error trajectory grazes the settling band (gap G-17)." Term: "settling band" (and `Kp`, `Kd` in the next sentence). Domain terms from the case study, not defined in this unit. **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it).
- "Datasets cubesat-primary and cubesat-stock and the six check designs were regenerated 5 times with `Kp`, `Kd`, the panel span and the battery capacity of every design multiplied by 1 + e, e uniform in [-1e-12, 1e-12], and every quantity this paper reports was recomputed (755 quantities, of which 330 numbers move at all)." Terms: "Kp", "Kd", "check designs". Gains and check designs are not defined here. **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it).
- "Compare it with the median over the designs of the gap between best and second-best facet score: far below it, a few designs sit on a seam and most do not." Term: "facet score". The Glossary defines facet and assignment margin but not the per-facet score. **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it).
- "This appendix carries: tables that cite their dataset by the label Appendix C defines: the temperature selection, the diagnostics at K = 1, 2, 3, ..." Terms: "frac_above", "n_eff" (effective sample size), "reach beta_k", "share" (as a facet share, not the ternary share), "tau*log V", "rank among training", "dZ", "Z within band" appear as column headers with no definition; the Glossary has none of them as such. **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it).


### List 2. Where a Glossary term would say it shorter or more exactly

- "The temperature is selected afresh at each K, so the mean slack of D.2 and of section sect-case-analysis compares fits at different temperatures." Term: "fit temperature". The bare "temperature" is ambiguous against "term temperature". **Disposition: glossary term** (use the Glossary term the reader names).
- "Here each K is refitted at the K = 1 temperature." Term: "fit temperature". **Disposition: glossary term** (use the Glossary term the reader names).
- "At the exact maximum the fit of each of these tables stops without a margin (`stationary_without_margin`) or at the iteration cap, depending on the platform, and its errors move with it, so neither is printed: a frontier row on two facet planes ties at the exact maximum and the platform's argmax and linear-program vertex choice resolve the tie (gap G-10)." Term: "supporting envelope" for "the exact maximum", and "termination status" for the two named stops. **Disposition: glossary term** (use the Glossary term the reader names).
- "The margin gamma is in score units, the scale of the band 1/tau; below the band, a change as small as the band can move a design to another facet." Term: "assignment margin" (gamma is never tied to it); "fit temperature" for tau. **Disposition: glossary term** (use the Glossary term the reader names).
- "Compare it with the median over the designs of the gap between best and second-best facet score: far below it, a few designs sit on a seam and most do not." Term: "assignment margin" is exactly this gap (smallest, over designs); "seam" is not a Glossary term. **Disposition: glossary term** (use the Glossary term the reader names).
- "The tables not recovered, with the frontier rows of their thinnest planted facet (a facet needs at least 5 frontier rows, one more than there are metrics, to be determined by them), ..." Term: "support weights" or "supporting envelope". The Glossary says "frontier" is an everyday word that pages should replace by one of three named objects; here it is used bare. **Disposition: glossary term** (use the Glossary term the reader names).
- "Here the two refits are compared with the true labels given, so the alternation plays no part." Term: "assignment" for "true labels" (the dominant term of each design). **Disposition: glossary term** (use the Glossary term the reader names).
- "The diagnostic `conditioning_` of the estimator is the smallest eigenvalue of the restricted Hessian at each facet's fit; a small value flags a nearly flat direction, so weakly identified exponents." Term: "conditioning of the exponents" (the Glossary entry is the same definition; the section title already uses it, so the sentence can cite it). **Disposition: glossary term** (use the Glossary term the reader names).
- "**Main text keeps:** section sect-case-analysis in about 500 words: K = 1, K = 3, the regime comparison, the candidates, propose-predict-check in one paragraph and the nondominated counts." Term: "number of terms" for "K"; "Pareto boundary" for what the nondominated counts measure. **Disposition: glossary term** (use the Glossary term the reader names).


### List 3a. Terms of art that plain words would serve

- "A quantity that moves is printed in this paper to the digits that held in all 6 datasets (the committed one and the 5 regenerated), as a range where not even two digits did, and as a bound where it is a numerical residue." Terms: "numerical residue" (rounding error), "committed" (the saved one). Plain: "rounding error". **Disposition: plain words** (replace with the plain words the reader names).
- "**Stability of the conclusions under rounding-level jitter**" and the sentence "Datasets ... were regenerated 5 times with ... e uniform in [-1e-12, 1e-12]". Term: "rounding-level jitter". Plain: "tiny random changes to the inputs". **Disposition: plain words** (replace with the plain words the reader names).
- "Compare it with the median over the designs of the gap between best and second-best facet score: far below it, a few designs sit on a seam and most do not." Term: "seam". Plain: "sit near the boundary between two facets". **Disposition: plain words** (replace with the plain words the reader names).
- "Here the two refits are compared with the true labels given, so the alternation plays no part." Term: "alternation". Plain: "the back-and-forth between assigning and refitting". **Disposition: plain words** (replace with the plain words the reader names).
- "The stable radius is gamma divided by twice the largest norm of a row of the log-metrics with a final entry of minus one, so it is smaller than the margin and is sufficient, not tight." Terms: "sufficient, not tight". Plain: "a safe distance, but not the largest safe distance". **Disposition: plain words** (replace with the plain words the reader names).
- "a frontier row on two facet planes ties at the exact maximum and the platform's argmax and linear-program vertex choice resolve the tie" Terms: "ties", "linear-program vertex choice". Plain: "the row is equally good on two facets, and the platform's arbitrary pick decides which". **Disposition: plain words** (replace with the plain words the reader names).


### List 3b. Sentences with three or more terms of art together

- "**This appendix carries:** tables that cite their dataset by the label Appendix C defines: the temperature selection, the diagnostics at K = 1, 2, 3, the exponents and facets, the regime comparison, the sensitivity variants, the refits by category, the candidate designs (the table of the candidates, which the main text leaves here), the solver's termination records with what each status asserts, the nondominated counts, propose-predict-check the stability of the conclusions under rounding-level jitter in the times, the conditioning of the exponents, the refit on a facet's own rows, the recovery of planted facets over twenty tables, the mean slack at a fixed temperature and a principal component analysis of the near-frontier chart." (Also garbled: "propose-predict-check the stability".) **Disposition: no change** (a definition, statement or proof step where the terms are the content; the unresolved ones are items in List 1 and the shorter ones items in Lists 2 and 3a).
- "`certified`: the assignment is fixed, residuals and gaps are within tolerance, no facet is empty and the margin is positive; levels 1 to 3 hold." Terms: assignment, residuals, gaps, facet, margin, levels. **Disposition: no change** (a definition, statement or proof step where the terms are the content; the unresolved ones are items in List 1 and the shorter ones items in Lists 2 and 3a).
- "The stable radius is gamma divided by twice the largest norm of a row of the log-metrics with a final entry of minus one, so it is smaller than the margin and is sufficient, not tight." Terms: stable radius, gamma, log-metrics, margin. **Disposition: no change** (a definition, statement or proof step where the terms are the content; the unresolved ones are items in List 1 and the shorter ones items in Lists 2 and 3a).
- "The margin gamma is in score units, the scale of the band 1/tau; below the band, a change as small as the band can move a design to another facet." Terms: margin, score units, band, tau, facet. **Disposition: no change** (a definition, statement or proof step where the terms are the content; the unresolved ones are items in List 1 and the shorter ones items in Lists 2 and 3a).
- "The record also holds the maximal gap, the Corollary bound, the margin, the stable radius and the shares." Terms: maximal gap, Corollary bound, margin, stable radius, shares. **Disposition: no change** (a definition, statement or proof step where the terms are the content; the unresolved ones are items in List 1 and the shorter ones items in Lists 2 and 3a).
- "`mean_slack_` is defined for every K and is comparable across K at one temperature; `objective_` is the soft maximum at one term and the mean slack at several, and is not." Terms: mean slack, objective_, soft maximum, temperature, term. **Disposition: no change** (a definition, statement or proof step where the terms are the content; the unresolved ones are items in List 1 and the shorter ones items in Lists 2 and 3a).
- "At the exact maximum the fit of each of these tables stops without a margin (`stationary_without_margin`) or at the iteration cap, depending on the platform, and its errors move with it, so neither is printed: a frontier row on two facet planes ties at the exact maximum and the platform's argmax and linear-program vertex choice resolve the tie (gap G-10)." Terms: exact maximum, margin, iteration cap, frontier row, facet planes, argmax, linear-program vertex. **Disposition: no change** (a definition, statement or proof step where the terms are the content; the unresolved ones are items in List 1 and the shorter ones items in Lists 2 and 3a).
- "A table is recovered when the largest error of the exponents, after matching fitted to planted facets, is under 0.05 and at least 90% of its frontier rows lie on the right facet." Terms: exponents, planted facets, frontier rows, facet. **Disposition: no change** (a definition, statement or proof step where the terms are the content; the unresolved ones are items in List 1 and the shorter ones items in Lists 2 and 3a).


## Unit 36: paper/paper.ipynb :: Open questions

Density 3.1 terms of art per 100 words (2/64); staged text `paper_open-questions.txt`.


### List 1. Terms unresolved from the unit and the Glossary

- "Q3: identifiability of the active metrics under finite, biased observations." Terms: active metrics, identifiability. "Active metrics" is not in the Glossary (closest is contending set), and the unit does not say which metrics are active or what is to be identified. **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it). **Routed to P1** (not edited here).
- "Four questions are not established ({ref}`Appendix E <appendix-e>` records them as gaps G-14, G-11, G-12 and G-13)." Terms: gaps G-14, G-11, G-12, G-13. The labels are defined only in Appendix E, which a reader of this unit does not have, and the numbering is out of order. **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it). **Routed to P1** (not edited here).
- "Q1: global convergence of the alternation, not pursued." Terms: the alternation. The Glossary does not define it, and the unit does not say which alternation (which steps alternate) is meant. **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it). **Routed to P1** (not edited here).
- "Q2: statistical consistency under noise and refitting." Terms: refitting. The Glossary has no entry for it. It could mean the facet refit (see facet gap) or refitting on new samples. **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it). **Routed to P1** (not edited here).


### List 2. Where a Glossary term would say it shorter or more exactly

- "Q4: conditions under which the fitted surface recovers the Pareto boundary and not the sample's envelope." Terms: fitted reference surface, supporting envelope. "Fitted surface" is the Glossary's fitted reference surface, and "the sample's envelope" is its supporting envelope. Using the exact names would show which of the three frontier objects is meant. **Disposition: glossary term** (use the Glossary term the reader names). **Routed to P1** (not edited here).
- "Q3: identifiability of the active metrics under finite, biased observations." Term: contending set. "Active metrics" is the contending set (the metrics with positive exponent in the exact-maximum fit). **Disposition: glossary term** (use the Glossary term the reader names). **Routed to P1** (not edited here).
- "Q3: identifiability of the active metrics under finite, biased observations." Terms: number of designs, fit temperature. "Finite, biased observations" could be said with the Glossary's design and temperature terms, since the sample's bias is what the finite-temperature band relies on. **Disposition: glossary term** (use the Glossary term the reader names). **Routed to P1** (not edited here).


### List 3a. Terms of art that plain words would serve

- "Q1: global convergence of the alternation, not pursued." Plain words: "whether the back-and-forth fitting steps always reach the best answer from any starting point". **Disposition: plain words** (replace with the plain words the reader names). **Routed to P1** (not edited here).
- "Q2: statistical consistency under noise and refitting." Plain words: "whether the estimates settle on the true values as data grows, despite noise". **Disposition: plain words** (replace with the plain words the reader names). **Routed to P1** (not edited here).
- "Q3: identifiability of the active metrics under finite, biased observations." Plain words: "whether the data are enough to tell which metrics really trade off". **Disposition: plain words** (replace with the plain words the reader names). **Routed to P1** (not edited here).


### List 3b. Sentences with three or more terms of art together

- "Q4: conditions under which the fitted surface recovers the Pareto boundary and not the sample's envelope." Terms: fitted surface, Pareto boundary, envelope (also "recovers" in the statistical sense). **Disposition: no change** (a definition, statement or proof step where the terms are the content; the unresolved ones are items in List 1 and the shorter ones items in Lists 2 and 3a). **Routed to P1** (not edited here).
- "Q3: identifiability of the active metrics under finite, biased observations." Terms: identifiability, active metrics, biased observations. **Disposition: no change** (a definition, statement or proof step where the terms are the content; the unresolved ones are items in List 1 and the shorter ones items in Lists 2 and 3a). **Routed to P1** (not edited here).
- "Q2: statistical consistency under noise and refitting." Terms: statistical consistency, noise, refitting. **Disposition: no change** (a definition, statement or proof step where the terms are the content; the unresolved ones are items in List 1 and the shorter ones items in Lists 2 and 3a). **Routed to P1** (not edited here).


## Unit 37: paper/supporting_material.ipynb :: Appendix C. The case's model: how the table of metrics came to be

Density 3.0 terms of art per 100 words (39/1301); staged text `supp_appendix-c-the-case-s-model-how-the-tabl.txt`.


### List 1. Terms unresolved from the unit and the Glossary

- "**Main text keeps:** {numref}`section %s <sect-case-construction>` in about 300 words: the cubesat model, the two regimes, the ten attributes, feasibility and conditioning." Term: regimes (primary, stock). Never defined here or in the Glossary; the reader cannot tell what differs between cubesat-primary and cubesat-stock beyond the Kp range and gain-box flag. **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it).
- "The repository keeps: the SysML model file, the evaluation code, the experiment ledger and the data." Terms: SysML, experiment ledger. SysML is not standard at the reader level; "ledger" is not defined (the C.6 columns "Ledger entry" and "Ledger hash" depend on it). **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it).
- "Each metric is `m_j = exp((o_j log(a_j + s_j) - c_j) / k_j)` for attribute `a_j`, with orientation `o_j` (+1 larger is better, -1 smaller is better), shift `s_j = 0`, and the offset `c_j` and log scale `k_j` of the conditioning above." Terms: offset c_j, shift s_j. The C.4 table shows k but no c_j, and nothing says how c_j is chosen (the "std of log m = 1" column hints at standardising, unstated). **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it).
- "| settled | 24 | 24 | 976 |" (C.3 table rows: settled, power_ok, momentum_ok, all attributes positive). Terms: settled, power_ok, momentum_ok. The feasibility conditions are named but never defined or given thresholds; "fails alone" versus "removed in this order" is also unexplained. **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it).
- "| control effort | control_effort | torque.s, proxy | no |" Terms: proxy, torque.s. What control effort is a proxy for is not said. **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it).
- "| pointing error | `cubesat_model.py` | `pointing_error_deg` | computed: pointing budget |" Term: pointing budget (and "computed: accounting" versus "measured: on the integrated slew"). Domain terms (slew, settling, eclipse reserve, depth of discharge, momentum) are not defined for a reader outside spacecraft engineering. **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it).
- "| cubesat-primary | primary | examples/adcs/data/adcs_designs_cubesat_gains.csv | adopted-adcs_designs_cubesat_gains | uv run python examples/adcs/generate_dataset.py --model cubesat --gain-box aggressive --n 1000 --seed 0 --slew-deg 30 --t-end 600 --force | 1000 | 706 | ..." Terms: gain-box aggressive, adopted (ledger entry). Not defined. **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it).
- "| reciprocal | 7.322 | 505.9 | 0.8282 | 1 | 0.05526 | 9.194 |" (C.4 rows). Terms: reciprocal, direct (orientation values). Table uses them; the C.5 text gives only +1/-1, so the mapping is left to the reader. **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it).
- "Dataset planted-3-facet:" with "| facet 1 | 0.5 | 0.5 | 0 | 0 |". Terms: planted, make_frontier_data. "Planted example" is never explained as a synthetic case with known exponents; the Glossary defines facet and exponent vector but not planted. **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it).


### List 2. Where a Glossary term would say it shorter or more exactly

- "The table of metrics, one row per kept design and one column per metric, is where the model ends and the method begins." Terms: number of designs, number of metrics, metrics. The Glossary entries say rows are evaluated configurations and columns the dimension of the trade space; "n designs by d metrics" says it exactly. **Disposition: glossary term** (use the Glossary term the reader names).
- "Dataset cubesat-primary: 706 designs by 10 metrics; the first 5 rows:" Terms: number of designs, number of metrics. Matches the Glossary's two counts; could use their names. **Disposition: glossary term** (use the Glossary term the reader names).
- "| Design variable | Declared min | Declared max | cubesat-primary min | cubesat-primary max | cubesat-stock min | cubesat-stock max |" Term: configuration. The table is the configuration space; the Glossary distinguishes design variables (fitted? no, carried as covariates) which the heading does not note for wheel_class and st_grade. **Disposition: glossary term** (use the Glossary term the reader names).
- "To let a reader judge whether the case, a cubesat model coupling power, mass and attitude control, is a fair test, and build a comparable one, by following the model from configurations to the table of metrics; what the method found in that table is {ref}`Appendix D <appendix-d>`." Terms: configuration, attributes, conditioning. "From configurations through attributes and conditioning to metrics" uses the Glossary chain exactly. **Disposition: glossary term** (use the Glossary term the reader names).


### List 3a. Terms of art that plain words would serve

- "**This appendix carries:** tables generated from the model and never typed: the configuration space, the evaluation with the part of the model that produces each attribute, feasibility, conditioning, the table of metrics, the datasets with their provenance, and the planted example." Term: provenance. Plain words: where each dataset came from (source and how it was made). **Disposition: plain words** (replace with the plain words the reader names).
- "| Attribute | File | Name in the file | How it is obtained |" / "measured: on the integrated slew". Term: integrated slew. Plain words: simulated turn. **Disposition: plain words** (replace with the plain words the reader names).
- "| Larger is better |" with "reciprocal" / "direct". Terms: reciprocal, direct. Plain words: smaller is better, larger is better. **Disposition: plain words** (replace with the plain words the reader names).
- "with orientation `o_j` (+1 larger is better, -1 smaller is better)". Term: orientation. Plain word: direction. **Disposition: plain words** (replace with the plain words the reader names).
- "| Label | Regime | File | Ledger entry | Command | Designs sampled | Designs kept | SHA-256 | Ledger hash |" Term: ledger hash. Plain words: fingerprint recorded in the log. **Disposition: plain words** (replace with the plain words the reader names).


### List 3b. Sentences with three or more terms of art together

- "**This appendix carries:** tables generated from the model and never typed: the configuration space, the evaluation with the part of the model that produces each attribute, feasibility, conditioning, the table of metrics, the datasets with their provenance, and the planted example." Terms: configuration space, evaluation, attribute, feasibility, conditioning, table of metrics, provenance, planted example. **Disposition: no change** (a definition, statement or proof step where the terms are the content; the unresolved ones are items in List 1 and the shorter ones items in Lists 2 and 3a).
- "**Main text keeps:** {numref}`section %s <sect-case-construction>` in about 300 words: the cubesat model, the two regimes, the ten attributes, feasibility and conditioning." Terms: regimes, attributes, feasibility, conditioning. **Disposition: no change** (a definition, statement or proof step where the terms are the content; the unresolved ones are items in List 1 and the shorter ones items in Lists 2 and 3a).
- "Each metric is `m_j = exp((o_j log(a_j + s_j) - c_j) / k_j)` for attribute `a_j`, with orientation `o_j` (+1 larger is better, -1 smaller is better), shift `s_j = 0`, and the offset `c_j` and log scale `k_j` of the conditioning above." Terms: metric, attribute, orientation, shift, offset, log scale, conditioning. **Disposition: no change** (a definition, statement or proof step where the terms are the content; the unresolved ones are items in List 1 and the shorter ones items in Lists 2 and 3a).
- "To let a reader judge whether the case, a cubesat model coupling power, mass and attitude control, is a fair test, and build a comparable one, by following the model from configurations to the table of metrics; what the method found in that table is {ref}`Appendix D <appendix-d>`." Terms: configurations, table of metrics, attitude control, method. **Disposition: no change** (a definition, statement or proof step where the terms are the content; the unresolved ones are items in List 1 and the shorter ones items in Lists 2 and 3a).


## Unit 38: paper/paper.ipynb :: Future work and final remark

Density 3.0 terms of art per 100 words (5/169); staged text `paper_future-work-and-final-remark.txt`.


### List 1. Terms unresolved from the unit and the Glossary

- "Beyond small K, scalability and speed, and a global search or certificate for the alternation (Q1)." Terms: "the alternation", "Q1". Neither is defined in the unit or the Glossary; the reader cannot tell which alternating procedure or which open question is meant. **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it).
- "The search of {numref}`Section %s <sect-search>` needs a convergence theorem, and Q2 to Q4 need their own conditions." Terms: "The search", "Q2 to Q4". The search is not in the Glossary and the cross-reference is not visible; Q2 to Q4 are undefined. **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it).
- "Beyond one facet, K > 1 is built; beyond sharp weights with smoothing on request, a nonsmooth search on the tangent cones of the ridges, whose generalized gradient is the convex hull of the active normals, should tolerate the kinks." Terms: "sharp weights", "ridges", "kinks", "active normals", "the nonsmooth search". The Glossary has term temperature and facet but none of these; the reader must guess that ridges and kinks are the facet boundaries and that sharp means infinite term temperature. **Disposition: no change** (standard vocabulary at the reader level the paper assumes (Boyd and Vandenberghe; scikit-learn)).
- "Beyond log-affine conditioning, GGP-compatible kernels, the generalization the search motivates." Terms: "GGP", "kernels", "the generalization the search motivates". The Glossary spells out generalized geometric program but never gives the abbreviation; "kernels" is not defined here; the motivation is not stated. **Disposition: no change** (standard vocabulary at the reader level the paper assumes (Boyd and Vandenberghe; scikit-learn)).
- "Beyond continuous variables within a category, discrete design variables." Term: "category". Not in the Glossary; unclear whether it means a categorical configuration value or a class of design. **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it).
- "Beyond a log-convex envelope, the detection of dents and holes." Terms: "dents", "log-convex envelope". Holes relate to white space, but dents are not defined; the envelope is not tied to the supporting envelope. **Disposition: no change** (standard vocabulary at the reader level the paper assumes (Boyd and Vandenberghe; scikit-learn)).


### List 2. Where a Glossary term would say it shorter or more exactly

- "Beyond one facet, K > 1 is built; beyond sharp weights with smoothing on request, ..." Terms: number of terms (for K > 1, and the unexplained K); term temperature (for sharp weights with smoothing, i.e. infinite versus finite). Both are exact in the Glossary. **Disposition: glossary term** (use the Glossary term the reader names).
- "Beyond the analyst's K, selection rules." Term: number of terms. The Glossary says it is the analyst's choice, never selected by the fit; K alone is bare. **Disposition: glossary term** (use the Glossary term the reader names).
- "Beyond log-affine conditioning, GGP-compatible kernels, the generalization the search motivates." Terms: conditioning; generalized geometric program (GGP). The Glossary names the full class and says it is convex after x = exp(y). **Disposition: glossary term** (use the Glossary term the reader names).
- "Beyond a log-convex envelope, the detection of dents and holes." Terms: supporting envelope; white space. Holes in the chart coordinates are white space. **Disposition: glossary term** (use the Glossary term the reader names).
- "Beyond continuous variables within a category, discrete design variables." Term: configuration. The Glossary term for design variables is configuration. **Disposition: glossary term** (use the Glossary term the reader names).
- "A new capability or technology entering the design space could be given a novelty or impact score from how far above $V=1$ it is forecast to sit." Terms: novelty (defined as distance beyond the fitted reference surface, a score for white space and new capabilities); fitted reference surface (the level V = 1); trade space (not "design space"); improvement factor for the impact reading. **Disposition: glossary term** (use the Glossary term the reader names).


### List 3a. Terms of art that plain words would serve

- "a nonsmooth search on the tangent cones of the ridges, whose generalized gradient is the convex hull of the active normals, should tolerate the kinks." Plain: a search that copes with sharp corners where facets meet. **Disposition: plain words** (replace with the plain words the reader names).
- "Beyond sharp weights with smoothing on request" Plain: hard assignment of each design to one term, with optional blending. **Disposition: plain words** (replace with the plain words the reader names).
- "a global search or certificate for the alternation (Q1)" Plain: a method that finds, or proves, the best answer of the back-and-forth fitting step. **Disposition: plain words** (replace with the plain words the reader names).
- "Beyond a log-convex envelope, the detection of dents and holes." Plain: finding places where the data bulge inward or leave gaps. **Disposition: plain words** (replace with the plain words the reader names).
- "Beyond continuous variables within a category, discrete design variables." Plain: choices that are counted rather than measured. **Disposition: plain words** (replace with the plain words the reader names).
- "GGP-compatible kernels, the generalization the search motivates." Plain: richer curve shapes that stay solvable as convex programs. **Disposition: plain words** (replace with the plain words the reader names).


### List 3b. Sentences with three or more terms of art together

- "Beyond one facet, K > 1 is built; beyond sharp weights with smoothing on request, a nonsmooth search on the tangent cones of the ridges, whose generalized gradient is the convex hull of the active normals, should tolerate the kinks." Terms: facet, K, sharp weights, nonsmooth search, tangent cones, ridges, generalized gradient, convex hull, active normals, kinks. **Disposition: no change** (a definition, statement or proof step where the terms are the content; the unresolved ones are items in List 1 and the shorter ones items in Lists 2 and 3a).
- "Beyond log-affine conditioning, GGP-compatible kernels, the generalization the search motivates." Terms: log-affine conditioning, GGP, kernels, the search. **Disposition: no change** (a definition, statement or proof step where the terms are the content; the unresolved ones are items in List 1 and the shorter ones items in Lists 2 and 3a).
- "Beyond small K, scalability and speed, and a global search or certificate for the alternation (Q1)." Terms: K, global search, certificate, alternation, Q1. **Disposition: no change** (a definition, statement or proof step where the terms are the content; the unresolved ones are items in List 1 and the shorter ones items in Lists 2 and 3a).
- "A new capability or technology entering the design space could be given a novelty or impact score from how far above $V=1$ it is forecast to sit." Terms: design space, novelty score, V=1. **Disposition: no change** (a definition, statement or proof step where the terms are the content; the unresolved ones are items in List 1 and the shorter ones items in Lists 2 and 3a).


## Unit 39: paper/supporting_material.ipynb :: Appendix B. Proofs, step for step with their scripts (part 7)

Density 2.9 terms of art per 100 words (67/2306); staged text `supp_appendix-b-proofs-step-for-step-with-the_7.txt`.


### List 1. Terms unresolved from the unit and the Glossary

- "Level 3 is for step B, unpenalized, with support offsets beta\_k = J\_tau(U w\_k) only." Terms: Level 3, step B, unpenalized, support offsets, J_tau, U. None is defined here or in the Glossary (which has "support weights", not "support offsets"); the objective they belong to is never stated. **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it).
- "**Ledger.** axioms imported and applied: F12, I9, R2; proved results imported: none; exported: L13_RESULT; 17 steps." Terms: Ledger, imported/exported, axiom labels F12, I9, R2. The ledger vocabulary and what the labels stand for are not defined; only the cell text under each label hints. **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it).
- "**L13.1** | by declared axiom **F12** (posited): min representation for L12 and L13: ..." Terms: declared axiom, posited, inherited, regularity (the kind tags beside F12, I9, R2). The three kinds are never distinguished or defined, so the reader cannot tell what is assumed versus proved. **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it).
- "**Hypotheses** (quoted from the statement): every facet score changes by at most delta (carried by the symbols delta (nonnegative), a1 (nonnegative), a2 (nonnegative)); ..." Terms: carried by the symbols, a1, a2, nth, a_, r_, b_, UU, U_. The symbol-carrying convention and these auxiliary symbols are unexplained. **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it).
- "Facet scores s\_ik = w\_k.u\_i - beta\_k = theta\_k.(u\_i, -1), the energy differential (log V) of design i against facet k; ..." Terms: facet score, w_k, beta_k, theta_k, u_i, (u_i, -1). The score is not in the Glossary; u versus u~ (used later as ||u~||) and ubar_k are never defined. **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it).
- "Per facet, sum\_{i in C\_k} (beta\_k - w\_k.u\_i) = n\_k (beta\_k - w\_k.ubar\_k) = n\_k f\_k(w\_k), n\_k = |C\_k|, so the mean slack is F(W) = sum\_k (n\_k/N) f\_k(w\_k)." Terms: C_k (cell), f_k, F(W), mean slack. The objective f_k and the slack are not defined in the unit or Glossary. **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it).
- "A8: F(W) = (1/N) sum\_k n\_k f\_k(w\_k) = sum\_k share\_k f\_k(w\_k) with share\_k = n\_k / N" Term: share. The Glossary defines share as a ternary-plot position; here it is a cell fraction n_k/N, a clash. **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it). **To the driver** (the reader reports a clash that touches a term's meaning).
- "then on the assignment-stable neighborhood of the fitted reference surface (finite tau, Phi = 0, V \> 1 possible; or the tau = inf supporting envelope) F(W') - F(W) = ..." Terms: Phi, tau, W'. Phi is undefined; tau is the fit temperature only by inference. **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it).
- "Corollary 4: F(W) - F\*\_fixed \<= sum\_k (n\_k/N) G\_k with G\_k the facet gaps of L12 (nonnegative sums)" Terms: F*_fixed, "nonnegative sums". F*_fixed is undefined. **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it).
- "**L14.9** | by proved result **L13**: assignment margin: score changes below gamma/2 keep the maximizing facets; explicit radius ..." Term: maximizing facet versus "assignment" and "term". The Glossary calls the dominant term the assignment; "maximizing facet" is not mapped to it. **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it).
- "assignment-stable neighborhood" (L13 statement and L14 statement). Term: neighborhood in what space (facet parameters theta). Not stated. **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it).
- "L12: 0 \<= f(w) - f\* \<= G, G = 0 iff the simplex KKT holds" Term: simplex KKT, f*. The constraint set (w on the simplex) is not restated; the Glossary says facet gap is zero when optimality conditions hold, but f* is undefined. **Disposition: no change** (standard vocabulary at the reader level the paper assumes (Boyd and Vandenberghe; scikit-learn)).


### List 2. Where a Glossary term would say it shorter or more exactly

- "If every facet score changes by at most delta, every row's new gap to every other facet is \>= gamma - 2 delta, positive when 2 delta \< gamma, so each maximizing facet is unchanged and unique." Term: assignment (and assignment margin): "so every design's assignment is unchanged". **Disposition: glossary term** (use the Glossary term the reader names).
- "R2 (regularity): positive assignment margin: gamma = min\_i \[s\_i,k(i) - max\_{k != k(i)} s\_ik\] \> 0, where s\_ik = w\_k.u\_i - beta\_k, so every row has a unique maximizing facet" Terms: assignment margin, assignment: "so every design has one assignment". **Disposition: glossary term** (use the Glossary term the reader names).
- "**L13.7** | computed | the new gap is positive when 2 delta \< gamma: each maximizing facet is unchanged" Term: assignment ("each assignment is unchanged"). **Disposition: glossary term** (use the Glossary term the reader names).
- "an assignment-stable neighborhood of the fitted reference surface's facets" Term: stable radius ("perturbations of the facets inside the stable radius"). **Disposition: glossary term** (use the Glossary term the reader names).
- "**L13.12** | computed | R2: gamma \> 0, so the radius gamma / (2 U) is positive: the neighborhood is nonempty" Term: stable radius. **Disposition: glossary term** (use the Glossary term the reader names).
- "every row" / "row i" in L13 and L14 statements. Term: design (each Glossary "number of designs" row is one design). **Disposition: glossary term** (use the Glossary term the reader names).
- "the cells C\_1..C\_K partition the N rows: every row lies in exactly one cell" Terms: assignment, term, number of designs: "each of the N designs is assigned to one of K terms". **Disposition: glossary term** (use the Glossary term the reader names).
- "Level 3 is for step B, unpenalized, with support offsets beta\_k = J\_tau(U w\_k) only." Term: support weights / fit temperature, if offsets are what the Glossary's support weights and temperature produce. **Disposition: glossary term** (use the Glossary term the reader names).


### List 3a. Terms of art that plain words would serve

- "**L13.2** | by declared axiom **I9** (inherited): Cauchy-Schwarz inequality: ..." Terms: declared axiom, posited, inherited. Plain words: "assumed" and "assumed from an earlier proof". **Disposition: plain words** (replace with the plain words the reader names).
- "**L14.11** | computed | per facet, sum\_i (beta\_k - w\_k.u\_i) = n\_k (beta\_k - w\_k.ubar\_k) by a Fubini swap" Term: Fubini swap. Plain words: "exchanging the order of the two sums" (standard, but plain serves). **Disposition: plain words** (replace with the plain words the reader names).
- "**L13.9** | computed | the Cauchy-Schwarz chain slack a U + \|\|Delta\|\| b is nonnegative" Term: chain slack. Plain words: "the leftover in the chain of inequalities". **Disposition: plain words** (replace with the plain words the reader names).
- "**L14.14** | computed | A8: with n\_k = sum\_i chi\_ki the cell sum is n\_k (beta\_k - w\_k.ubar\_k) = n\_k f\_k(w\_k)" Terms: cell, chi_ki. Plain words: "the group of designs on facet k", "membership indicator". **Disposition: plain words** (replace with the plain words the reader names).
- "the slack rest is \>= 0" (L13.1). Term: slack. Plain words: "the nonnegative leftover". **Disposition: plain words** (replace with the plain words the reader names).
- "Fixed-assignment expression" ("on the neighborhood the full objective equals the fixed-assignment expression"). Plain words: "the objective with each design's facet held fixed". **Disposition: plain words** (replace with the plain words the reader names).
- "**L13.4** | computed | a parameter change moves the score by Delta theta\_k . (u\_i, -1)". Term: computed (versus axiom). Plain words: "checked by symbolic algebra". **Disposition: plain words** (replace with the plain words the reader names).


### List 3b. Sentences with three or more terms of art together

- "Facet scores s\_ik = w\_k.u\_i - beta\_k = theta\_k.(u\_i, -1), the energy differential (log V) of design i against facet k; margin gamma = min\_i \[s\_i,k(i) - max\_{k != k(i)} s\_ik\] \> 0 (R2)." Terms: facet score, energy differential, margin, R2. **Disposition: no change** (a definition, statement or proof step where the terms are the content; the unresolved ones are items in List 1 and the shorter ones items in Lists 2 and 3a).
- "With Cauchy-Schwarz (I9), |Delta theta\_k.(u\_i, -1)| \<= ||Delta theta\_k||\_2 ||(u\_i, -1)||\_2, so 2 delta \< gamma holds whenever max\_k ||Delta theta\_k||\_2 \< gamma / (2 max\_i ||(u\_i, -1)||\_2): an assignment-stable neighborhood of the fitted reference surface's facets" Terms: Cauchy-Schwarz, I9, assignment-stable neighborhood, fitted reference surface, facet. **Disposition: no change** (a definition, statement or proof step where the terms are the content; the unresolved ones are items in List 1 and the shorter ones items in Lists 2 and 3a).
- "Proposition 3: if the margin is positive (R2), every facet is nonempty and every w\_k minimizes f\_k, then on the assignment-stable neighborhood of the fitted reference surface (finite tau, Phi = 0, V \> 1 possible; or the tau = inf supporting envelope) F(W') - F(W) = sum\_k (n\_k/N) (f\_k(w'\_k) - f\_k(w\_k)) \>= 0, a local minimizer." Terms: margin, R2, facet, assignment-stable neighborhood, fitted reference surface, tau, Phi, supporting envelope. **Disposition: no change** (a definition, statement or proof step where the terms are the content; the unresolved ones are items in List 1 and the shorter ones items in Lists 2 and 3a).
- "Level 3 is for step B, unpenalized, with support offsets beta\_k = J\_tau(U w\_k) only." Terms: Level 3, step B, unpenalized, support offsets, J_tau. **Disposition: no change** (a definition, statement or proof step where the terms are the content; the unresolved ones are items in List 1 and the shorter ones items in Lists 2 and 3a).
- "**Ledger.** axioms imported and applied: A8, R2; proved results imported: L12_RESULT (from lemma_12_facet_gap), L13_RESULT (from lemma_13_margin); exported: L14_RESULT; 16 steps, in the file's one sequence of 20." Terms: axioms, A8, R2, imported, exported, L12_RESULT, L13_RESULT. **Disposition: no change** (a definition, statement or proof step where the terms are the content; the unresolved ones are items in List 1 and the shorter ones items in Lists 2 and 3a).
- "**L14.1** | by declared axiom **A8** (posited): the cells C\_1..C\_K partition the N rows: every row lies in exactly one cell (chi\_ki = 1 when row i is in cell k, sum\_k chi\_ki = 1, chi\_ki \>= 0), and the cell counts n\_k = sum\_i chi\_ki are at least 1 (every facet is nonempty)" Terms: declared axiom, posited, cell, partition, chi_ki, cell counts, facet. **Disposition: no change** (a definition, statement or proof step where the terms are the content; the unresolved ones are items in List 1 and the shorter ones items in Lists 2 and 3a).
- "**L14.10** | by proved result **L12**: facet first-order gap: 0 \<= f(w) - f\* \<= G, G = 0 iff the simplex KKT holds" Terms: proved result, facet gap, simplex KKT, f*. **Disposition: no change** (a definition, statement or proof step where the terms are the content; the unresolved ones are items in List 1 and the shorter ones items in Lists 2 and 3a).


## Unit 40: paper/paper.ipynb :: Case construction

Density 2.7 terms of art per 100 words (9/329); staged text `paper_case-construction.txt`.


### List 1. Terms unresolved from the unit and the Glossary

- "Conditioning orients each attribute, shifts and scales it to unit log-spread and keeps the map invertible." Term: unit log-spread. Not in the Glossary and not defined here; it is unclear whether it means unit standard deviation of the log or unit range. **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it).
- "Feasibility removes designs that do not settle, saturate the momentum budget or discharge the battery too deeply." Terms: saturate the momentum budget; settle. Spacecraft-control jargon, not in the Glossary, and the reader cannot tell what the thresholds are. **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it).
- "Top left: the fraction of designs above V = 1 against the temperature tau, with the target fraction as a horizontal line." Terms: target fraction. Not in the Glossary; who sets the target and why 0.10 is not said. **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it).
- "Top right: the effective sample size." Term: effective sample size. Not in the Glossary; "support weights" is related but the link is not made. **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it).
- "The selected temperature is tau = 38.1: a fraction 0.096 of designs lies above V = 1 (the target is 0.10), the band 1/tau is 0.0262 and the effective sample size is 16 designs." Terms: band 1/tau; selected temperature. The Glossary mentions a band only inside "fit temperature"; the unit never says how the temperature is selected or why 1/tau is a width, or in what units. **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it).
- "We use two regimes of the same design problem: aggressive controller gains (the primary regime) and stock gains (the baseline)." Term: regime. Not in the Glossary; the sense (a parameter setting of the same model) is only inferred. **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it).
- "Where the answer must be known, we plant it: a synthetic table with three facets of known exponents ({ref}`Appendix C <appendix-c>` gives its generator), from which {numref}`Section %s <sect-case-analysis>` asks whether the fit recovers them." Terms: plant / planted table; recovers. Not in the Glossary; "recover" has no stated criterion. **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it).


### List 2. Where a Glossary term would say it shorter or more exactly

- "Conditioning orients each attribute, shifts and scales it to unit log-spread and keeps the map invertible." Term: chart. "keeps the map invertible" is the Glossary's "reversible transformation ... nothing is lost either way". **Disposition: glossary term** (use the Glossary term the reader names).
- "The selected temperature is tau = 38.1: a fraction 0.096 of designs lies above V = 1 (the target is 0.10), the band 1/tau is 0.0262 and the effective sample size is 16 designs." Terms: fit temperature; support weights. "Selected temperature" is the fit temperature, and the band of near-frontier designs is defined there; "effective sample size" is what the support weights give. **Disposition: glossary term** (use the Glossary term the reader names).
- "The planted table has 900 rows, 4 metrics and 3 planted facets." Terms: number of designs; number of metrics; number of terms. The Glossary's names for rows, metric count and facet count would tie the numbers to the symbols used elsewhere. **Disposition: glossary term** (use the Glossary term the reader names).
- "Bottom: the exponent of each metric." Term: exponent vector. The Glossary names this object. **Disposition: glossary term** (use the Glossary term the reader names).
- "Top left: the fraction of designs above V = 1 against the temperature tau, with the target fraction as a horizontal line." Term: fitted reference surface. "Above V = 1" is "beyond the fitted reference surface" (novelty/energy differential positive); the unit never says V = 1 is that surface. **Disposition: glossary term** (use the Glossary term the reader names).
- "Each configuration is evaluated once into ten attributes: controls (settling time, slew time, pointing error and control effort), power and energy (power margin, energy balance, eclipse reserve, peak slew power and depth of discharge) and mass (total mass)." Term: attributes. Fine as used; the Glossary adds that they are raw, in mixed units and directions, which the unit does not say before "Conditioning orients". **Disposition: glossary term** (use the Glossary term the reader names).


### List 3a. Terms of art that plain words would serve

- "Feasibility removes designs that do not settle, saturate the momentum budget or discharge the battery too deeply." Terms: saturate the momentum budget. Plain words: "use up the wheels' stored-momentum capacity". **Disposition: plain words** (replace with the plain words the reader names).
- "We use two regimes of the same design problem". Term: regimes. Plain words: "two settings" or "two cases". **Disposition: plain words** (replace with the plain words the reader names).
- "Where the answer must be known, we plant it". Term: plant. Plain words: "build it in" or "construct it". **Disposition: plain words** (replace with the plain words the reader names).
- "Conditioning orients each attribute, shifts and scales it". Term: orients. Plain words: "makes larger better" (flips where needed). **Disposition: plain words** (replace with the plain words the reader names).
- "a black box to the method". Term: black box. Plain words: "which the method does not see inside". **Disposition: plain words** (replace with the plain words the reader names).


### List 3b. Sentences with three or more terms of art together

- "Conditioning orients each attribute, shifts and scales it to unit log-spread and keeps the map invertible." Terms: conditioning, attribute, unit log-spread, invertible map. **Disposition: no change** (a definition, statement or proof step where the terms are the content; the unresolved ones are items in List 1 and the shorter ones items in Lists 2 and 3a).
- "The selected temperature is tau = 38.1: a fraction 0.096 of designs lies above V = 1 (the target is 0.10), the band 1/tau is 0.0262 and the effective sample size is 16 designs." Terms: temperature, V = 1, target, band, effective sample size. **Disposition: no change** (a definition, statement or proof step where the terms are the content; the unresolved ones are items in List 1 and the shorter ones items in Lists 2 and 3a).
- "Top left: the fraction of designs above V = 1 against the temperature tau, with the target fraction as a horizontal line." Terms: V = 1, temperature, target fraction. **Disposition: no change** (a definition, statement or proof step where the terms are the content; the unresolved ones are items in List 1 and the shorter ones items in Lists 2 and 3a).
- "Where the answer must be known, we plant it: a synthetic table with three facets of known exponents ({ref}`Appendix C <appendix-c>` gives its generator), from which {numref}`Section %s <sect-case-analysis>` asks whether the fit recovers them." Terms: plant, facets, exponents, generator, fit, recovers. **Disposition: no change** (a definition, statement or proof step where the terms are the content; the unresolved ones are items in List 1 and the shorter ones items in Lists 2 and 3a).
- "Feasibility removes designs that do not settle, saturate the momentum budget or discharge the battery too deeply." Terms: feasibility, settle, momentum budget, depth of discharge. **Disposition: no change** (a definition, statement or proof step where the terms are the content; the unresolved ones are items in List 1 and the shorter ones items in Lists 2 and 3a).


## Unit 41: paper/supporting_material.ipynb :: Appendix B. Proofs, step for step with their scripts (part 5)

Density 2.7 terms of art per 100 words (61/2287); staged text `supp_appendix-b-proofs-step-for-step-with-the_5.txt`.


### List 1. Terms unresolved from the unit and the Glossary

- "The package uses the sharp limit of the weights, one label per design, $k(i)=\arg\max_ks_{ik}$ with $s_{ik}=w_k\cdot u_i-\beta_k$; the program then separates into one convex program per term, $f_k(w)=J_\tau(Uw)-\bar u_k\cdot w$, with $n_k$ the designs labelled $k$ and $\bar u_k$ their mean log-metric." Terms: J_tau, U, "mean slack", "label". J_tau is never defined here and is not in the Glossary (a support/log-mean-exp function is only guessable); "label" is not in the Glossary (assignment is close but not named). **Disposition: no change** (standard vocabulary at the reader level the paper assumes (Boyd and Vandenberghe; scikit-learn)).
- "The model is $\Phi_K$ (L10); every facet is fitted against every design, each offset $\beta_k=J_\tau(Uw_k)$ being the support over all rows; the fit minimizes the mean slack." Terms: offset beta_k, "support over all rows", "mean slack". "Mean slack" is not defined in the unit or Glossary, nor is the "support" here (Glossary has "support weights" and "supporting envelope" only). **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it).
- "L17 treats the soft fit at finite $\tau$ and $\kappa$: the gradient and the Hessian $D-\kappa M$ of its objective, and the second-order test that certifies a strict local minimizer." Terms: D, M, "soft fit". D and M are not defined in the unit; the L17 construction is not shown. **Disposition: no change** (standard vocabulary at the reader level the paper assumes (Boyd and Vandenberghe; scikit-learn)).
- "the extension temperature is positive, kappa \> 0, and each of the K terms has exponents theta\_k on the simplex" (L10.1 and L10.2, axiom A6). Term: "extension temperature". The Glossary has "fit temperature" and "term temperature" but not "extension", and Phi_K itself is never defined in this unit. **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it).
- "Phi\_K(u + c 1) = Phi\_K(u) + c" and "shift equivariance: Phi\_K(u + c 1) - (Phi\_K(u) + c) is 0 (logs licensed: A1, A6)". Terms: "shift equivariance", "logs licensed". Not in the Glossary; the sense of "licensed" (positivity makes the log splitting valid) is not stated. **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it).
- "by declared axiom **F10** (posited): max representation for L10: the maximum over the K terms of x\_k = theta\_k.u - beta\_k is a symbol M with x\_k \<= M for all k in 1..K and x\_{k0} = M for some k0 in 1..K". Term: "max representation", "F10". Axiom family F is not explained here. **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it).
- "L16 does not prove that the alternation converges." Terms: "alternation", L16. The alternation is described only by the unit's own steps (1) to (3); L16 is not in the unit. **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it).
- "where w\_j \> 0): weakly efficient in all d metrics, efficient when every w\_j \> 0." Terms: "weakly efficient", "efficient". Pareto-standard, but the Glossary entry for Pareto boundary does not define them and the unit gives only the definitions via L11.18 and L11.19. **Disposition: no change** (standard vocabulary at the reader level the paper assumes (Boyd and Vandenberghe; scikit-learn)).
- "The label belongs to the package and not to the model; which facet dominates a design is analysis of the fitted model." Term: "label". The Glossary covers "assignment" and "region" but "label" is the unit's own word. **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it).


### List 2. Where a Glossary term would say it shorter or more exactly

- "The package uses the sharp limit of the weights, one label per design, $k(i)=\arg\max_ks_{ik}$ ..." Terms: "term temperature" (infinity is the sharp limit of one label per design) and "assignment". **Disposition: glossary term** (use the Glossary term the reader names).
- "The label belongs to the package and not to the model; which facet dominates a design is analysis of the fitted model." Term: "assignment" (the dominant term of a design, an analysis). **Disposition: glossary term** (use the Glossary term the reader names).
- "L16 states the program for weights $\alpha_{ik}=\mathrm{softmax}_k(\kappa s_{ik})$" Term: "term temperature" for kappa (and "support weights" for the softmax weights if they are the designs' weights). **Disposition: glossary term** (use the Glossary term the reader names).
- "L17 treats the soft fit at finite $\tau$ and $\kappa$" Terms: "fit temperature" (tau) and "term temperature" (kappa). **Disposition: glossary term** (use the Glossary term the reader names).
- "the extension temperature is positive, kappa \> 0, and each of the K terms has exponents theta\_k on the simplex" Terms: "exponent vector", "term temperature". **Disposition: glossary term** (use the Glossary term the reader names).
- "metrics are strictly positive, larger-is-better: m\_i\[j\] \> 0, so u = log m is defined" Terms: "metrics", "log-metrics". **Disposition: glossary term** (use the Glossary term the reader names).
- "a maximizer of V = exp(w.u - beta) over a set S is not dominated by any member of S in the contending metrics (w\_j \> 0)" Terms: "invariant value" (V), "contending set" (the metrics with positive exponent). **Disposition: glossary term** (use the Glossary term the reader names).
- "so it is weakly efficient in all d metrics" and "The converse is not claimed: only the log-convex part of a front is reached by some w" Term: "Pareto boundary" for "front". **Disposition: glossary term** (use the Glossary term the reader names).
- "it is a generalized posynomial in $e^{w}$, so its minimization is a generalized geometric program in the sense of Boyd et al." Terms: "generalized posynomial" and "generalized geometric program" are used correctly; no change needed beyond noting "in the sense of Boyd et al." duplicates the Glossary citation. **Disposition: add to avoid** (the phrase is withdrawn by WP10 Amendment 4 (R-33, R-34, R-37)).
- "the fit minimizes the mean slack" and "k(i)" Term: "facet gap" is nearby but not the same; none for slack. **Disposition: glossary term** (use the Glossary term the reader names).
- "exp(kappa Phi\_K) is a posynomial" Term: "posynomial" used correctly; none. **Disposition: glossary term** (use the Glossary term the reader names).


### List 3a. Terms of art that plain words would serve

- "by declared axiom **A6** (posited)" : "posited" -> "assumed". **Disposition: plain words** (replace with the plain words the reader names).
- "**Ledger.** axioms imported and applied: A1, A6, F10; proved results imported: none; exported: none; 19 steps." : "Ledger" -> "list of what the proof uses and gives". **Disposition: plain words** (replace with the plain words the reader names).
- "L11.20 ... negative control inside the chain: without step 3 (V strictly larger) nothing follows" : "negative control" -> "check that the claim fails without this step"; "the chain is vacuous" -> "the argument would be empty". **Disposition: plain words** (replace with the plain words the reader names).
- "L10. Extension Phi_K: shift equivariance" : "shift equivariance" -> "adding c to every u adds c to the result". **Disposition: plain words** (replace with the plain words the reader names).
- "weighted-sum scalarization" : "scalarization" -> "turning the metrics into one number by weighting". **Disposition: plain words** (replace with the plain words the reader names).
- "The package uses the sharp limit of the weights" : "sharp limit" -> "hard assignment (each design gets exactly one term)". **Disposition: plain words** (replace with the plain words the reader names).
- "The alternation takes weights from the current model and then solves one program for all terms (L16)." : "alternation" -> "back-and-forth (alternating) steps". **Disposition: plain words** (replace with the plain words the reader names).
- "the upper squeeze bound M + (log K)/kappa tends to M as kappa -\> inf" : "squeeze" -> "sandwich". **Disposition: plain words** (replace with the plain words the reader names).


### List 3b. Sentences with three or more terms of art together

- "The package uses the sharp limit of the weights, one label per design, $k(i)=\arg\max_ks_{ik}$ with $s_{ik}=w_k\cdot u_i-\beta_k$; the program then separates into one convex program per term, $f_k(w)=J_\tau(Uw)-\bar u_k\cdot w$, with $n_k$ the designs labelled $k$ and $\bar u_k$ their mean log-metric." **Disposition: no change** (a definition, statement or proof step where the terms are the content; the unresolved ones are items in List 1 and the shorter ones items in Lists 2 and 3a).
- "L16 states the program for weights $\alpha_{ik}=\mathrm{softmax}_k(\kappa s_{ik})$: the fixed-weight objective bounds the soft model's mean slack from above and equals it at the model the weights came from, and it is a generalized posynomial in $e^{w}$, so its minimization is a generalized geometric program in the sense of Boyd et al. [@boyd2007tutorial]." **Disposition: add to avoid** (the phrase is withdrawn by WP10 Amendment 4 (R-33, R-34, R-37)).
- "L17 treats the soft fit at finite $\tau$ and $\kappa$: the gradient and the Hessian $D-\kappa M$ of its objective, and the second-order test that certifies a strict local minimizer." **Disposition: no change** (a definition, statement or proof step where the terms are the content; the unresolved ones are items in List 1 and the shorter ones items in Lists 2 and 3a).
- "The model is $\Phi_K$ (L10); every facet is fitted against every design, each offset $\beta_k=J_\tau(Uw_k)$ being the support over all rows; the fit minimizes the mean slack." **Disposition: no change** (a definition, statement or proof step where the terms are the content; the unresolved ones are items in List 1 and the shorter ones items in Lists 2 and 3a).
- "For w in the simplex and u' = u + delta, delta \>= 0: w.u' - w.u = sum\_j w\_j delta\_j \>= 0, strictly \> 0 whenever some j has w\_j \> 0 and delta\_j \> 0; hence V(u') \>= V(u) with strict inequality under the same condition, and a maximizer of V = exp(w.u - beta) over a set S is not dominated by any member of S in the contending metrics (w\_j \> 0): weakly efficient in all d metrics, efficient when every w\_j \> 0." **Disposition: no change** (a definition, statement or proof step where the terms are the content; the unresolved ones are items in List 1 and the shorter ones items in Lists 2 and 3a).
- "At K \> 1, kappa = infinity, a maximizer of Phi = max\_k (theta\_k.u - beta\_k) is not dominated through any term active at it (theta\_k0.delta = 0), so it is weakly efficient in all d metrics." **Disposition: no change** (a definition, statement or proof step where the terms are the content; the unresolved ones are items in List 1 and the shorter ones items in Lists 2 and 3a).


## Unit 42: paper/supporting_material.ipynb :: Appendix B. Proofs, step for step with their scripts (part 10)

Density 2.2 terms of art per 100 words (56/2519); staged text `supp_appendix-b-proofs-step-for-step-with-the_10.txt`.


### List 1. Terms unresolved from the unit and the Glossary

- "every direction of the critical cone is a direction of the tangent space of the face" (L17.19). Term: "face" / "active face". Not in the Glossary (which has "facet", a different object); the unit never says which polyhedron the face belongs to. **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it).
- "dF along V is sum_k V_k.g_k, g_k = (n_k/N)(utilde_k - ubar_k^alpha) (refit gradient)" (L17.12). Terms: "refit gradient", F, n_k, N, utilde, ubar. "facet gap" mentions a refit, but nothing defines the refit gradient or these symbols. **Disposition: no change** (standard vocabulary at the reader level the paper assumes (Boyd and Vandenberghe; scikit-learn)).
- "the first derivative of the offset along V is sum_l p_lk c_lk (the L3 gradient)" (L17.4). Terms: "offset" (beta_k), "the L3 gradient", c. Depends on another lemma and on symbols not defined here; "level offset" in the Glossary is a different object. **Disposition: no change** (standard vocabulary at the reader level the paper assumes (Boyd and Vandenberghe; scikit-learn)).
- "the second derivative of F is V'DV - kappa V'MV" (L17.35); also "the second derivative of F along V is V'DV - kappa V'MV, the moment forms of D and M" (L17.13). Terms: "moment form" (and "squares form" in L17.36-38). Neither is defined, and which one is "the" variance is unclear. **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it).
- "the first derivative of -Phi_i at t = 0 is -sum_k alpha_ik y_ik" (L17.8). Terms: Phi_i, "soft model of a design" (L17.30), y_ik. Phi_i is never introduced here. **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it).
- "A1: the log-metrics u and the direction V (real vectors) are real families" (L17.1). Term: "real families" (the code's real_base). Not standard; the unit does not say what a family is. **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it).
- "exact instance: the point with both terms equal is stationary on the simplex" (L17.49). Terms: "exact instance", "both terms equal" (the all-equal point). The instance's data and K are not given. **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it).


### List 2. Where a Glossary term would say it shorter or more exactly

- "A2: the exponents W_kj of every term are nonnegative (on the simplex)" (L17.2). Glossary term: "exponent vector" (the weights of term k on the simplex over the metrics). **Disposition: glossary term** (use the Glossary term the reader names).
- "A3, A6: tau > 0 and kappa > 0; the squares forms are sums of nonnegative terms" (L17.17), with A6 "the extension temperature is positive, kappa > 0". Glossary terms: "term temperature" for kappa (softmax weights over terms) and "fit temperature" for tau; "extension temperature" is a third name for what looks like one of these. **Disposition: glossary term** (use the Glossary term the reader names).
- "D the weighted within-term curvature and kappa M the designs' ambiguity between terms" (statement). Glossary terms: "assignment" and "assignment margin" (a design's dominant term and the gap to the runner-up) say what the ambiguity is. **Disposition: glossary term** (use the Glossary term the reader names).
- "the support weights p_lk of a term sum to one" (L17.11). Glossary term: "support weights" is used correctly here, but L17.10 "the weights alpha_ik = softmax_k(kappa x_ik) of a design sum to one" has no Glossary name; "term temperature" ("soft weights over the terms") would name it. **Disposition: glossary term** (use the Glossary term the reader names).
- "A1: the scores x0 of the model at W are real" (L17.3). Glossary term: "energy differential" / "log-metrics" would say what x0 is if it is the log-invariant relative to the surface; the unit never ties "score" to a Glossary object. **Disposition: glossary term** (use the Glossary term the reader names).


### List 3a. Terms of art that plain words would serve

- "the squares form of a weighted variance is the moment form plus vbar^2 (Q - 1)" (L17.36). Terms: "squares form", "moment form". Plain words: "the sum-of-squared-deviations expression" and "the mean-of-squares-minus-square-of-mean expression". **Disposition: plain words** (replace with the plain words the reader names).
- "A1: the log-metrics u and the direction V (real vectors) are real families" (L17.1). Term: "real families". Plain words: "are real-valued arrays". **Disposition: plain words** (replace with the plain words the reader names).
- "the soft model of a design: first derivative of -Phi_i is -sum alpha y" (L17.30). Term: "soft model of a design". Plain words: "the design's soft-maximum score". **Disposition: plain words** (replace with the plain words the reader names).
- "A positive definite form on the face is positive on the cone (a restriction)" (L17.20). Term: "restriction". Plain words: "a form positive on a set is positive on any subset of it". **Disposition: plain words** (replace with the plain words the reader names).


### List 3b. Sentences with three or more terms of art together

- "Soft-fit certificate: at a feasible point of the soft-weight fit where the first-order (KKT) conditions hold, if the Hessian H = D - kappa M of the soft objective is positive definite on the tangent space of the active face, the point is a strict local minimizer; D and M are both positive semidefinite, D the weighted within-term curvature and kappa M the designs' ambiguity between terms." Terms: soft-weight fit, KKT, tangent space of the active face, strict local minimizer, within-term curvature. **Disposition: no change** (a definition, statement or proof step where the terms are the content; the unresolved ones are items in List 1 and the shorter ones items in Lists 2 and 3a).
- "every direction of the critical cone is a direction of the tangent space of the face" (L17.19). Terms: critical cone, tangent space, face. **Disposition: no change** (a definition, statement or proof step where the terms are the content; the unresolved ones are items in List 1 and the shorter ones items in Lists 2 and 3a).
- "A3, A6: tau > 0 and kappa > 0; the squares forms are sums of nonnegative terms" (L17.17). Terms: tau, kappa, squares forms (plus the A6 "extension temperature"). **Disposition: no change** (a definition, statement or proof step where the terms are the content; the unresolved ones are items in List 1 and the shorter ones items in Lists 2 and 3a).
- "the gradient of F is the weighted refit gradient of each term" (L17.34). Terms: gradient of F, weighted refit gradient, term. **Disposition: no change** (a definition, statement or proof step where the terms are the content; the unresolved ones are items in List 1 and the shorter ones items in Lists 2 and 3a).
- "the second derivative of -Phi_i at t = 0 is -kappa Var_alpha(y) - sum_k alpha_ik z_k" (L17.9). Terms: Phi_i, Var_alpha, y, z_k (all undefined in the unit). **Disposition: no change** (a definition, statement or proof step where the terms are the content; the unresolved ones are items in List 1 and the shorter ones items in Lists 2 and 3a).


## Unit 43: paper/supporting_material.ipynb :: Appendix B. Proofs, step for step with their scripts (part 8)

Density 2.2 terms of art per 100 words (22/1012); staged text `supp_appendix-b-proofs-step-for-step-with-the_8.txt`.


### List 1. Terms unresolved from the unit and the Glossary

- "Level 1 (descent), step B unpenalized: reassigning every row to its maximizing facet does not increase the mean slack F, and refitting each facet to a minimizer of its convex facet objective does not increase F; so F is non-increasing along accepted iterations." Terms: Level 1, step B, unpenalized, mean slack F, convex facet objective, accepted iterations. Why: the unit never says what the levels, steps, penalty, slack, per-facet objective or the iteration are; none is in the Glossary. **Disposition: no change** (standard vocabulary at the reader level the paper assumes (Boyd and Vandenberghe; scikit-learn)).
- "A8: the membership family chi\_ki, the cell counts n\_k and the number N of rows" (and the A8 axiom text: "the cells C\_1..C\_K partition the N rows"). Terms: cell, membership family. Why: "cell" is not in the Glossary (nearest is region/assignment); its link to facets is left implicit. **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it).
- "F12: r\_ki = s\_ki - m\_i \>= 0 for every row i and facet k, with equality at k\*(i)". Terms: s\_ki, m\_i, k\*(i), r\_ki. Why: s\_ki is never defined as the slack of row i on facet k, and the Glossary has no entry for slack. **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it).
- "by L12: a minimizing refit has e\_k = f'\_k(w\_k) - f'\_k\* \>= 0". Terms: f'\_k, w\_k, f'\_k\*, refit. Why: the primed objective and its variable w_k are undefined here; "refit" is used for a per-facet minimization, not as in the Glossary's "facet gap" sense. **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it).
- "by L14: on any partition of the rows, F = sum\_k share\_k f\_k(w\_k)". Terms: share\_k (a different "share" than the Glossary's ternary-plot share), F, f\_k. Why: the Glossary "share" is a position in a triangle; here it is a cell's fraction n_k/N. **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it).
- "axioms imported and applied: A8, F12; proved results imported: L12\_RESULT (from lemma\_12\_facet\_gap), L14\_RESULT (from lemma\_14\_assignment\_stable); exported: none; 16 steps." Terms: ledger, axioms imported, exported. Why: the proof-ledger conventions are not explained in the unit. **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it).


### List 2. Where a Glossary term would say it shorter or more exactly

- "reassigning every row to its maximizing facet does not increase the mean slack F" (Statement). Term: assignment. Why: "assigning a design to its maximizing facet" is the Glossary's assignment. **Disposition: glossary term** (use the Glossary term the reader names).
- "A8: the membership family chi\_ki, the cell counts n\_k and the number N of rows" Term: number of designs (N rows = number of designs). Why: the Glossary names the table rows' count. **Disposition: glossary term** (use the Glossary term the reader names).
- "by proved result **L12**: facet first-order gap: 0 \<= f(w) - f\* \<= G, G = 0 iff the simplex KKT holds" Term: facet gap. Why: "first-order gap of a facet's refit, zero exactly when the optimality conditions hold" is already the Glossary's definition. **Disposition: glossary term** (use the Glossary term the reader names).
- "A8: sum\_k chi\_ki = 1, so row i's slack on its own cell is m\_i + sum\_k chi\_ki r\_ki" Term: assignment (cell = the facet a design is assigned to). Why: "its own cell" is "its assigned facet". **Disposition: glossary term** (use the Glossary term the reader names).
- "F12: ... the slack of row i on its maximizing facet k\*(i) is m\_i, the least over facets" Term: assignment margin is nearby (smallest gap to runner-up); "assignment" for "maximizing facet". Why: the Glossary pins down "dominant term of a design". **Disposition: glossary term** (use the Glossary term the reader names).


### List 3a. Terms of art that plain words would serve

- "unpenalized" (Statement): "with no added penalty term". **Disposition: plain words** (replace with the plain words the reader names).
- "posited" / "by declared axiom ... (posited)": "assumed". **Disposition: plain words** (replace with the plain words the reader names).
- "partition" / "chi\_ki = 1 when row i is in cell k": "every row belongs to exactly one group". **Disposition: plain words** (replace with the plain words the reader names).
- "non-increasing" (Statement, L15.16): "never goes up". **Disposition: plain words** (replace with the plain words the reader names).
- "nonempty" (A8: "every facet is nonempty"): "has at least one row". **Disposition: plain words** (replace with the plain words the reader names).
- "membership family chi\_ki" (L15.1, L15.5): "indicator of which group a row is in". **Disposition: plain words** (replace with the plain words the reader names).
- "accepted iterations": "the steps the algorithm keeps". **Disposition: plain words** (replace with the plain words the reader names).


### List 3b. Sentences with three or more terms of art together

- "Level 1 (descent), step B unpenalized: reassigning every row to its maximizing facet does not increase the mean slack F, and refitting each facet to a minimizer of its convex facet objective does not increase F; so F is non-increasing along accepted iterations." **Disposition: no change** (a definition, statement or proof step where the terms are the content; the unresolved ones are items in List 1 and the shorter ones items in Lists 2 and 3a).
- "by declared axiom **A8** (posited): the cells C\_1..C\_K partition the N rows: every row lies in exactly one cell (chi\_ki = 1 when row i is in cell k, sum\_k chi\_ki = 1, chi\_ki \>= 0), and the cell counts n\_k = sum\_i chi\_ki are at least 1 (every facet is nonempty); declared at [line 31]" **Disposition: no change** (a definition, statement or proof step where the terms are the content; the unresolved ones are items in List 1 and the shorter ones items in Lists 2 and 3a).
- "by declared axiom **F12** (posited): min representation for L12 and L13: the minimum m of a finite family x\_j (the gradient components g\_j in L12, the row gaps in L13) is a symbol with x\_j \>= m for all j and x\_{j0} = m for some j0; declared at [line 31]" **Disposition: no change** (a definition, statement or proof step where the terms are the content; the unresolved ones are items in List 1 and the shorter ones items in Lists 2 and 3a).
- "by proved result **L12**: facet first-order gap: 0 \<= f(w) - f\* \<= G, G = 0 iff the simplex KKT holds" **Disposition: no change** (a definition, statement or proof step where the terms are the content; the unresolved ones are items in List 1 and the shorter ones items in Lists 2 and 3a).


## Unit 44: paper/supporting_material.ipynb :: Appendix B. Proofs, step for step with their scripts (part 4)

Density 2.0 terms of art per 100 words (44/2221); staged text `supp_appendix-b-proofs-step-for-step-with-the_4.txt`.


### List 1. Terms unresolved from the unit and the Glossary

- "d log m\_j / d log m\_k = -w\_k / w\_j on F; improving metric j alone by f = V^(-1/w\_j) reaches V = 1" — term: F. Never defined here or in the Glossary (the Glossary names the fitted reference surface, supporting envelope, Pareto boundary, not F). **Disposition: no change** (standard vocabulary at the reader level the paper assumes (Boyd and Vandenberghe; scikit-learn)).
- "the tangent direction e\_k0 + x e\_j0 has dG(v) = w\_k0 + x w\_j0" — terms: G, dG, v. No definition of G or of what it is differentiated against. **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it).
- "V = e^{w.b - beta} Prod\_j (a\_j + s\_j)^{w\_j alpha\_j}; conditioning invertible" — terms: s\_j, a\_j, b, beta. The statement uses s\_j while the steps use r\_j (the "raw attribute"); a\_j, b and beta are never introduced. **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it).
- "Pull-back: V = e^{w.b - beta} prod_j (a_j + s_j)^{w_j alpha_j}" (the L9 heading, as "#### L9. Pull-back: V = e^{w.b - beta} prod_j (a_j + s_j)^{w_j alpha_j}") — term: pull-back. Not in the Glossary; the direction of the pull is unstated. **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it).
- "the sum-zero chart: Z = B u with B a (d-1) x d matrix satisfying B B^T = I and B 1 = 0 (orthonormal rows spanning the sum-zero subspace; the Helmert basis is one realization)" — terms: Helmert basis, sum-zero chart. The Glossary "chart" is a reversible map, but Z = B u drops the common shift and is not reversible alone. **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it).
- "the cumulant (1/tau) log E exp(tau w.eps) equals tau sigma^2 ||w||^2 / 2" — term: cumulant. Short for cumulant generating function scaled by 1/tau; not defined, and not standard at calculus/convex level. **Disposition: no change** (standard vocabulary at the reader level the paper assumes (Boyd and Vandenberghe; scikit-learn)).
- "by declared axiom **A5** (posited): noise: eps\_j are i.i.d. N(0, sigma^2), independent across j, with sigma \> 0" — terms: posited, and "inherited" on the I5/I6 rows. The two axiom kinds are not defined in the unit or Glossary. **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it).


### List 2. Where a Glossary term would say it shorter or more exactly

- "A2: the exponents w lie on the simplex: w\_j \>= 0 and sum\_j w\_j = 1" (axiom text "the exponents w lie on the simplex: w\_j \>= 0 and sum\_j w\_j = 1") — exponent vector. Glossary: weights of a term on the simplex over the metrics. **Disposition: glossary term** (use the Glossary term the reader names).
- "the soft-maximum temperature is positive: tau \> 0" — fit temperature (or term temperature). Says which temperature, and notes infinity is the exact maximum. **Disposition: glossary term** (use the Glossary term the reader names).
- "at f = V^(-1/w\_j0) the new log V is 0: the point reaches the frontier V = 1" — fitted reference surface. "Frontier" is an everyday word for three objects; V = 1 is the fitted reference surface. **Disposition: glossary term** (use the Glossary term the reader names).
- "d log m\_j / d log m\_k = -w\_k / w\_j on F; improving metric j alone by f = V^(-1/w\_j) reaches V = 1" — improvement factor (f is the improvement factor on metric j) and fitted reference surface (for V = 1 / F). **Disposition: glossary term** (use the Glossary term the reader names).
- "uniform improvement: scaling every metric by 1/V gives V = 1" — invariant value (V doubles when every metric doubles, which is why 1/V works) and improvement factor. **Disposition: glossary term** (use the Glossary term the reader names).
- "L8. Sum-zero (Helmert-type) chart and scale/shape bijection" (heading as "#### L8. Sum-zero (Helmert-type) chart and scale/shape bijection") — position along the frontier. Glossary: the other d - 1 chart coordinates, free of overall scale. **Disposition: glossary term** (use the Glossary term the reader names).
- "A1: a point of F is a point of log-metrics u = log m, a real family" — log-metrics is used correctly here; F is the only unresolved piece (see List 1). **Disposition: glossary term** (use the Glossary term the reader names).


### List 3a. Terms of art that plain words would serve

- "A4: a\_j + r\_j \> 0 licenses the log of the power (a\_j + r\_j)^(w\_j alpha\_j)" — "licenses": plain word "allows". **Disposition: plain words** (replace with the plain words the reader names).
- "A7: B 1 = 0 kills the term c (B 1) of B (u + c 1)" — "kills": plain words "sets to zero". **Disposition: plain words** (replace with the plain words the reader names).
- "by declared axiom **A5** (posited): noise: eps\_j are i.i.d. N(0, sigma^2), independent across j, with sigma \> 0" — "posited": plain word "assumed". **Disposition: plain words** (replace with the plain words the reader names).
- "the chart is blind to the common shift: Z(u + c 1) = Z(u)" — "blind to": plain words "unchanged by". **Disposition: plain words** (replace with the plain words the reader names).
- "the conditioning is invertible: the round trip returns u\_j" — "round trip": plain words "going there and back". **Disposition: plain words** (replace with the plain words the reader names).


### List 3b. Sentences with three or more terms of art together

- "the sum-zero chart: Z = B u with B a (d-1) x d matrix satisfying B B^T = I and B 1 = 0 (orthonormal rows spanning the sum-zero subspace; the Helmert basis is one realization)" — sum-zero chart, orthonormal rows, sum-zero subspace, Helmert basis. **Disposition: no change** (a definition, statement or proof step where the terms are the content; the unresolved ones are items in List 1 and the shorter ones items in Lists 2 and 3a).
- "conditioning is log-affine and invertible: log m\_j = alpha\_j log(a\_j + s\_j) + b\_j with alpha\_j != 0 (negative alpha\_j marks a cost attribute)" — conditioning, log-affine, invertible, cost attribute. **Disposition: no change** (a definition, statement or proof step where the terms are the content; the unresolved ones are items in List 1 and the shorter ones items in Lists 2 and 3a).
- "Population identity under the log-space Gaussian model (A5: eps\_j iid N(0, sigma^2), independent across j, sigma \> 0): (1/tau) log E exp(tau w.eps) = tau sigma^2 ||w||^2 / 2, with E the population expectation; not a finite-sample estimator, and no consistency claim" — population identity, log-space Gaussian model, finite-sample estimator, consistency claim. **Disposition: no change** (a definition, statement or proof step where the terms are the content; the unresolved ones are items in List 1 and the shorter ones items in Lists 2 and 3a).
- "the moment generating function of a sum of independent random variables is the product of their moment generating functions (ledger addition to spec section 6)" — moment generating function, ledger addition, spec section 6. **Disposition: no change** (a definition, statement or proof step where the terms are the content; the unresolved ones are items in List 1 and the shorter ones items in Lists 2 and 3a).


## Unit 45: paper/supporting_material.ipynb :: Appendix B. Proofs, step for step with their scripts (part 3)

Density 1.8 terms of art per 100 words (40/2222); staged text `supp_appendix-b-proofs-step-for-step-with-the_3.txt`.


### List 1. Terms unresolved from the unit and the Glossary

- "**Statement.** LSE = LME + (log n)/tau; LSE - max \>= 0 (strict for n \>= 2); lim\_{tau-\>inf} LME = max; lim\_{tau-\>0} LME = mean; mean \<= LME \<= max" -- LSE, LME: abbreviations never expanded in the unit or Glossary, and the reader cannot tell which is the unnormalized one. **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it).
- "**Statement.** d^2/dt^2 J\_tau(w + t v)|\_0 = tau Var\_p(v.u) = (tau/2) sum\_i sum\_k p\_i p\_k (s\_i - s\_k)^2 \>= 0 with p = softmax(tau U w), s\_i = v.u\_i, so J\_tau is convex" -- J\_tau, U, u, v: the objective and its symbols are never defined here (L3 is only referenced); tau is not tied to a Glossary term. **Disposition: no change** (standard vocabulary at the reader level the paper assumes (Boyd and Vandenberghe; scikit-learn)).
- "the normalizer Z, a net sum of positive terms, is positive" -- "net sum": no meaning given; Z is not defined in the unit. **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it).
- "negative control: without sum\_i p\_i = 1 the identity fails, so it is used" -- "negative control": not standard at this level; "it is used" has no clear referent. **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it).
- "mean \<= LME: the tangent-line floor of the LME equals the mean" -- "tangent-line floor": undefined phrase, and LME is undefined. **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it).
- "the sum of n ones is n, so the shifted sum T is at most n" -- "shifted sum T": T is not defined in the unit (only implied by L5.7). **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it).
- "by declared axiom **A2** (posited): the exponents w lie on the simplex: w\_j \>= 0 and sum\_j w\_j = 1" -- "declared axiom ... (posited)" versus "(inherited)": the distinction and the labels A1, A2, A3, F5, I11, I13 are not explained in the unit. **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it).


### List 2. Where a Glossary term would say it shorter or more exactly

- "by declared axiom **A2** (posited): the exponents w lie on the simplex: w\_j \>= 0 and sum\_j w\_j = 1" -- exponent vector: names w as the weights of a term on the simplex. **Disposition: glossary term** (use the Glossary term the reader names).
- "A1: u = log m is real, so the scores w.u\_i and v.u\_i are real families" -- log-metrics: u = log m is the log-metrics. **Disposition: glossary term** (use the Glossary term the reader names).
- "by declared axiom **A1** (posited): metrics are strictly positive, larger-is-better: m\_i\[j\] \> 0, so u = log m is defined" -- metrics, log-metrics: the Glossary states both, and the unit repeats the metrics definition. **Disposition: glossary term** (use the Glossary term the reader names).
- "by declared axiom **A3** (posited): the soft-maximum temperature is positive: tau \> 0" -- fit temperature: the Glossary's term for how hard the maximum is, which tau appears to be; the unit uses a different name. **Disposition: glossary term** (use the Glossary term the reader names).
- "by L3: the scores w.u\_i and v.u\_i and the softmax weights p, as L3 defined and proved" -- support weights: the softmax weights of the designs. **Disposition: glossary term** (use the Glossary term the reader names).


### List 3a. Terms of art that plain words would serve

- "by declared axiom **A3** (posited): the soft-maximum temperature is positive: tau \> 0" -- "posited": plain word "assumed". **Disposition: plain words** (replace with the plain words the reader names).
- "negative control: without sum\_i p\_i = 1 the identity fails, so it is used" -- "negative control": "a check that the identity fails without the normalization". **Disposition: plain words** (replace with the plain words the reader names).
- "mean \<= LME: the tangent-line floor of the LME equals the mean" -- "tangent-line floor": "lower bound from the tangent line". **Disposition: plain words** (replace with the plain words the reader names).
- "the normalizer Z, a net sum of positive terms, is positive" -- "net sum": just "sum". **Disposition: plain words** (replace with the plain words the reader names).
- "A2 licenses the logarithm of the positive x\_j: prod\_j x\_j^(tau u\_ij) = exp(tau w.u\_i)" -- "licenses": "allows taking". **Disposition: plain words** (replace with the plain words the reader names).


### List 3b. Sentences with three or more terms of art together

- "I13: a posynomial objective, monomial equality and monomial inequalities make the" -- posynomial, monomial equality, monomial inequalities; also a truncated sentence. **Disposition: no change** (a definition, statement or proof step where the terms are the content; the unresolved ones are items in List 1 and the shorter ones items in Lists 2 and 3a).
- "**Statement.** d^2/dt^2 J\_tau(w + t v)|\_0 = tau Var\_p(v.u) = (tau/2) sum\_i sum\_k p\_i p\_k (s\_i - s\_k)^2 \>= 0 with p = softmax(tau U w), s\_i = v.u\_i, so J\_tau is convex" -- softmax, soft-maximum objective, directional derivative, weighted variance, convex. **Disposition: no change** (a definition, statement or proof step where the terms are the content; the unresolved ones are items in List 1 and the shorter ones items in Lists 2 and 3a).
- "A3, F5: T\_raw \> 0 (exponentials of the real scores, tau \> 0), so log splits: LSE - LME" -- scores, tau, T\_raw, LSE, LME. **Disposition: no change** (a definition, statement or proof step where the terms are the content; the unresolved ones are items in List 1 and the shorter ones items in Lists 2 and 3a).
- "T \>= 1 + (second term) \> 1, so LSE - max = (1/tau) log T \> 0 for n \>= 2 (tau \> 0)" -- shifted sum T, LSE, tau, strictness at n >= 2. **Disposition: no change** (a definition, statement or proof step where the terms are the content; the unresolved ones are items in List 1 and the shorter ones items in Lists 2 and 3a).
- "the problem in w (minimize log f0(exp w) = tau J\_tau(w)) is convex, by L4.13" -- J\_tau, log-transformed posynomial f0, convex form, L4.13 reference. **Disposition: no change** (a definition, statement or proof step where the terms are the content; the unresolved ones are items in List 1 and the shorter ones items in Lists 2 and 3a).


## Unit 46: paper/supporting_material.ipynb :: Appendix B. Proofs, step for step with their scripts (part 1)

Density 1.6 terms of art per 100 words (29/1779); staged text `supp_appendix-b-proofs-step-for-step-with-the_1.txt`.


### List 1. Terms unresolved from the unit and the Glossary

- "**The repository keeps:** the scripts, the axiom ledger, the runner, the checker and the committed record." Terms: runner, checker, committed record. Never defined; the reader cannot tell what each does (the ledger is only explained later). **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it).
- "L4. convexity of the soft-maximum objective (second directional derivative = tau Var_p)". Terms: Var_p, tau, soft-maximum objective. The distribution p is never introduced; tau is not in the Glossary under that name. **Disposition: no change** (standard vocabulary at the reader level the paper assumes (Boyd and Vandenberghe; scikit-learn)).
- "L5. LSE = LME + log(n)/tau; mean <= LME <= max; tau limits". Terms: LSE, LME. Abbreviations not expanded here or in the Glossary. **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it).
- "L6. Gaussian cumulant of a weighted noise sum". Terms: Gaussian cumulant, noise. No noise model appears in the Glossary or the unit. **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it).
- "L8. Sum-zero (Helmert-type) chart and scale/shape bijection". Terms: Helmert-type, scale/shape. The Glossary "chart" does not mention Helmert or the scale/shape split. **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it).
- "L9. Pull-back: V = e^{w.b - beta} prod_j (a_j + s_j)^{w_j alpha_j}". Terms: pull-back, a_j, s_j, alpha_j, b, beta. None of the symbols is defined. **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it).
- "L10. Extension Phi_K: shift equivariance, K = 1 reduction, kappa -> infinity = max". Terms: Phi_K, kappa, shift equivariance. Kappa and Phi_K are not defined. **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it).
- "L11. A V-maximizer is Pareto-efficient (weighted-sum scalarization; converse not claimed)". Terms: V-maximizer, Pareto-efficient, scalarization. The Glossary gives only the Pareto boundary. **Disposition: no change** (standard vocabulary at the reader level the paper assumes (Boyd and Vandenberghe; scikit-learn)).
- "L15. descent (Level 1): reassignment and facet refit do not increase the mean slack". Terms: Level 1, reassignment, refit, mean slack. "Slack" is undefined, and "Level 1" is not matched to the Glossary's termination status. **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it).
- "L17. the soft-fit certificate: Hessian D - kappa M and the second-order test". Terms: soft-fit certificate, D, M, kappa. The matrices are not defined. **Disposition: no change** (standard vocabulary at the reader level the paper assumes (Boyd and Vandenberghe; scikit-learn)).
- "A2: the simplex sum\_j w\_j is replaced by 1 wherever it appears". Terms: A2, rewrite. The reader has to infer that A1 to A3 are labels for assumptions listed elsewhere (A3 is named only in the step list). **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it).


### List 2. Where a Glossary term would say it shorter or more exactly

- "invariant form: V(m / V(m)) = 1, the point lies on the frontier". Term: fitted reference surface. "Frontier" is the Glossary's ambiguous everyday word; V = 1 is the fitted reference surface. **Disposition: glossary term** (use the Glossary term the reader names).
- "metrics are strictly positive, larger-is-better: m\_i\[j\] \> 0, so u = log m is defined". Term: log-metrics (and metrics). u is the log-metrics. **Disposition: glossary term** (use the Glossary term the reader names).
- "the exponents w lie on the simplex: w\_j \>= 0 and sum\_j w\_j = 1". Term: exponent vector. w is the exponent vector on the simplex. **Disposition: glossary term** (use the Glossary term the reader names).
- "the soft-maximum temperature is positive: tau \> 0". Term: fit temperature. The Glossary names this quantity; "soft-maximum temperature" is a second name. **Disposition: glossary term** (use the Glossary term the reader names).
- "**The solver for K > 1 and its three levels of guarantee (L12 to L17)**" as written: "The solver for K > 1 and its three levels of guarantee (L12 to L17)". Terms: number of terms, termination status. K is the number of terms, and the levels are the termination status. **Disposition: glossary term** (use the Glossary term the reader names).
- "L13. assignment margin: score changes below gamma/2 keep the maximizing facets; explicit radius". Term: stable radius. "Explicit radius" is the stable radius. **Disposition: glossary term** (use the Glossary term the reader names).
- "L7. Elasticities -w_k/w_j on the frontier; improvement factor V^(-1/w_j)". Term: fitted reference surface (or facet). The elasticities hold along a facet. **Disposition: glossary term** (use the Glossary term the reader names).
- "offset: V(m e^-beta) = e^-beta V(m), so log V = w.u - beta". Term: energy differential. log V is the energy differential, so the line can say so. **Disposition: glossary term** (use the Glossary term the reader names).


### List 3a. Terms of art that plain words would serve

- "**Hypotheses** (quoted from the statement): none beyond the declared axioms below." Plain words: assumptions (hypotheses), assumed (declared axioms). **Disposition: plain words** (replace with the plain words the reader names).
- "by declared axiom **A2** (posited)". Plain words: "assumed" for posited. **Disposition: plain words** (replace with the plain words the reader names).
- "**Ledger.** axioms imported and applied: A1, A2; proved results imported: none; exported: L1_RESULT; 8 steps." Plain words: ledger = list of assumptions used; imported/exported = used from / handed on to other proofs. **Disposition: plain words** (replace with the plain words the reader names).
- "The address of a step is its file and its tag (`L2.1`, `L2.2`, ...), and the tag is unique within the file." Plain words: address = location; tag = label. **Disposition: plain words** (replace with the plain words the reader names).
- "**Main text keeps:** each statement as a theorem-style block with hypotheses, a narrative proof sketch and a one-line pointer to its file." Plain words: theorem-style block = boxed statement; narrative proof sketch = short outline of the proof. **Disposition: plain words** (replace with the plain words the reader names).
- "A step that SymPy cannot derive is an explicit hypothesis or an entry of the ledger." Plain words: hypothesis = stated assumption. **Disposition: plain words** (replace with the plain words the reader names).


### List 3b. Sentences with three or more terms of art together

- "per proof, in the paper's numbering: the statement with its hypotheses, its file, the proof as numbered steps (a sentence of prose, the step's formal claim, its kind and a link to its line), and the ledger status; compiled from `derivation/proof_map_record.json`, the lemma scripts and the axiom ledger, with the checker's table at the end." Terms: hypotheses, ledger, lemma scripts, axiom ledger, checker. **Disposition: no change** (a definition, statement or proof step where the terms are the content; the unresolved ones are items in List 1 and the shorter ones items in Lists 2 and 3a).
- "the line applies an entry of the axiom ledger that the script imported by name; the entry's wording and citation are shown beside the step, and the link gives the import line, the declaration's address in the proof's own file." Terms: axiom ledger, imported, import line, declaration, address. **Disposition: no change** (a definition, statement or proof step where the terms are the content; the unresolved ones are items in List 1 and the shorter ones items in Lists 2 and 3a).
- "What the correspondence establishes: every step of the prose has exactly one line of code, the lines are in the order of the prose, every computed line passes, and neither a line nor a sentence can change without the checker reporting the step." Terms: correspondence, computed line, checker, step. **Disposition: no change** (a definition, statement or proof step where the terms are the content; the unresolved ones are items in List 1 and the shorter ones items in Lists 2 and 3a).
- "L12. facet first-order gap: 0 <= f(w) - f* <= G, G = 0 iff the simplex KKT holds". Terms: facet first-order gap, simplex, KKT. **Disposition: no change** (a definition, statement or proof step where the terms are the content; the unresolved ones are items in List 1 and the shorter ones items in Lists 2 and 3a).
- "L16. soft-weight alternation: symmetry, the fixed-weight bound and the generalized posynomial". Terms: soft-weight alternation, fixed-weight bound, generalized posynomial. **Disposition: add to avoid** (the phrase is withdrawn by WP10 Amendment 4 (R-33, R-34, R-37)).
- "L10. Extension Phi_K: shift equivariance, K = 1 reduction, kappa -> infinity = max". Terms: Phi_K, shift equivariance, kappa. **Disposition: no change** (a definition, statement or proof step where the terms are the content; the unresolved ones are items in List 1 and the shorter ones items in Lists 2 and 3a).
- "L3. gradient of the soft-maximum objective and the full simplex KKT conditions". Terms: soft-maximum objective, simplex, KKT. **Disposition: no change** (a definition, statement or proof step where the terms are the content; the unresolved ones are items in List 1 and the shorter ones items in Lists 2 and 3a).


## Unit 47: paper/supporting_material.ipynb :: Appendix B. Proofs, step for step with their scripts (part 6)

Density 1.1 terms of art per 100 words (20/1799); staged text `supp_appendix-b-proofs-step-for-step-with-the_6.txt`.


### List 1. Terms unresolved from the unit and the Glossary

- "For the facet refit f(w) = J\_tau(U w) - ubar\_k.w on the simplex (convex by L4), g = grad f(w) and G = g.w - min\_j g\_j = sum\_j w\_j (g\_j - min g) \>= 0, with G = 0 iff w\_j (g\_j - min g) = 0 for every j (L3's simplex KKT: g\_j \>= lambda, w\_j (g\_j - lambda) = 0, lambda = w.g); and 0 \<= f(w) - f\* \<= G." - Terms: J\_tau, U, ubar\_k, "facet refit". None is defined in the unit or the Glossary (the Glossary has "fit temperature" and "facet gap" but not J\_tau, U or the refit's objective); the reader cannot tell what f is. **Disposition: no change** (standard vocabulary at the reader level the paper assumes (Boyd and Vandenberghe; scikit-learn)).
- "For the fitted reference surface (finite tau, Phi = 0, V \> 1 possible) this is the stopping certificate of a facet; for the tau = inf supporting envelope, with the LP duals p, G is the LP duality gap (I1)" - Terms: Phi, "stopping certificate", "LP duals p". Phi is never defined; "stopping certificate" is not in the Glossary; the LP that p solves is not stated. **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it).
- "**Ledger.** axioms imported and applied: A2, F12, I1, I12, I8; proved results imported: L4_RESULT (from lemma_04_convexity); exported: L12_RESULT; 33 steps." - Terms: "ledger", "axioms imported", "proved results imported", L12_RESULT. The bookkeeping vocabulary is not explained at this level. **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it).
- "by declared axiom **A2** (posited): the exponents w lie on the simplex: w\_j \>= 0 and sum\_j w\_j = 1; declared at [line 40](https://github.com/DynamicalSystemsGroup/hyperbolic-trade-space/blob/main/derivation/lemma_12_facet_gap.py#L40)" - Terms: "posited" versus "inherited" (used on I8, I12, I1). The difference between the two kinds of declared axiom is not stated. **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it).
- "**Hypotheses** (quoted from the statement): f(w) - f\* \>= 0 because f\* is the minimum (carried by the symbols c_nn (nonnegative))" - Terms: "carried by the symbols", c_nn. How a symbol carries a hypothesis is unexplained. **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it).
- "F12: the slacks gm\_j = g\_j - m are nonnegative" - Terms: gm, m. m (the minimum of g) is defined only inside the F12 text of another row; gm is a code name. **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it).
- "by L4: J\_tau is convex along every line, so f = J\_tau - linear is convex" - Terms: J\_tau again, and "soft-maximum objective" (row L12.10). The soft maximum is not defined in the unit; the Glossary defines "fit temperature" but not this objective. **Disposition: no change** (standard vocabulary at the reader level the paper assumes (Boyd and Vandenberghe; scikit-learn)).
- "I12: complementary slackness p\_i (M - s\_i) = 0 applied to each summand: the sum is 0" - Terms: M, s\_i, u\_i, "active rows". M and s\_i = w.u\_i are given in the I12 text of another row; "active rows" and u\_i are never defined. **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it).


### List 2. Where a Glossary term would say it shorter or more exactly

- "For the fitted reference surface (finite tau, Phi = 0, V \> 1 possible) this is the stopping certificate of a facet; for the tau = inf supporting envelope, with the LP duals p, G is the LP duality gap (I1)" - Terms: "facet gap", "fit temperature". G is the facet gap; "finite tau" and "tau = inf" are the fit temperature finite and infinite. **Disposition: glossary term** (use the Glossary term the reader names).
- "For the facet refit f(w) = J\_tau(U w) - ubar\_k.w on the simplex (convex by L4), g = grad f(w) and G = g.w - min\_j g\_j = sum\_j w\_j (g\_j - min g) \>= 0, with G = 0 iff w\_j (g\_j - min g) = 0 for every j (L3's simplex KKT: g\_j \>= lambda, w\_j (g\_j - lambda) = 0, lambda = w.g); and 0 \<= f(w) - f\* \<= G." - Terms: "facet gap", "exponent vector". G is the facet gap; w is the exponent vector of term k (the Glossary says "the weights of term k on the simplex"). **Disposition: glossary term** (use the Glossary term the reader names).
- "A2: the weight families v and w on the simplex are nonnegative" - Term: "exponent vector". "weight families v and w on the simplex" are exponent vectors. **Disposition: glossary term** (use the Glossary term the reader names).
- "File. [lemma\_12\_facet\_gap.py](https://github.com/DynamicalSystemsGroup/hyperbolic-trade-space/blob/main/derivation/lemma_12_facet_gap.py)." - Term: "facet gap". The title is the Glossary term; the unit's heading "facet first-order gap" should use it. **Disposition: glossary term** (use the Glossary term the reader names).
- "#### L12. facet first-order gap: 0 <= f(w) - f\* <= G, G = 0 iff the simplex KKT holds" - Term: "facet gap". The Glossary defines it exactly as "the first-order gap of a facet's refit; zero exactly when the optimality conditions hold". **Disposition: glossary term** (use the Glossary term the reader names).


### List 3a. Terms of art that plain words would serve

- "computed" - Plain words: "checked by SymPy". As a Kind label it is vague. **Disposition: plain words** (replace with the plain words the reader names).
- "by declared axiom **A2** (posited)" - Plain words: "assumed". "declared axiom (posited)" is heavier than needed. **Disposition: plain words** (replace with the plain words the reader names).
- "L12.9 ... exact two-metric LP: primal and dual values and gaps at an optimal pair and off it" - Plain words: "a worked two-metric example: objective values of the problem and its dual, and their difference, at and away from the optimum". **Disposition: plain words** (replace with the plain words the reader names).
- "L12.30 ... g.w splits into sum\_j w\_j (U^T p)\_j minus the centring term ubar.w" - Plain words: "centring term" is "the mean subtracted from each column". **Disposition: plain words** (replace with the plain words the reader names).
- "L12.25 ... swapping the finite sums: sum\_j w\_j (U^T p)\_j = sum\_i p\_i (w.u\_i)" - Plain words: "exchanging the order of the two sums". **Disposition: plain words** (replace with the plain words the reader names).
- "L12.21 ... a \>= 0 and a \<= 0 force a = 0: G = 0 only if every term w\_j (g\_j - m) is 0" - Plain words: "a is squeezed to zero". The squeeze step is stated clearly; no change needed except the label "termwise vanishing" in the code. **Disposition: plain words** (replace with the plain words the reader names).


### List 3b. Sentences with three or more terms of art together

- "For the fitted reference surface (finite tau, Phi = 0, V \> 1 possible) this is the stopping certificate of a facet; for the tau = inf supporting envelope, with the LP duals p, G is the LP duality gap (I1)" - Terms: fitted reference surface, stopping certificate, facet, supporting envelope, LP duals, LP duality gap. **Disposition: no change** (a definition, statement or proof step where the terms are the content; the unresolved ones are items in List 1 and the shorter ones items in Lists 2 and 3a).
- "For the facet refit f(w) = J\_tau(U w) - ubar\_k.w on the simplex (convex by L4), g = grad f(w) and G = g.w - min\_j g\_j = sum\_j w\_j (g\_j - min g) \>= 0, with G = 0 iff w\_j (g\_j - min g) = 0 for every j (L3's simplex KKT: g\_j \>= lambda, w\_j (g\_j - lambda) = 0, lambda = w.g); and 0 \<= f(w) - f\* \<= G." - Terms: facet refit, J\_tau, simplex, convexity by L4, gradient, simplex KKT, multiplier lambda. **Disposition: no change** (a definition, statement or proof step where the terms are the content; the unresolved ones are items in List 1 and the shorter ones items in Lists 2 and 3a).
- "by declared axiom **I12** (inherited): complementary slackness of the LP pair at tau = infinity: the dual weights p are supported on the rows whose score attains the maximum M, p\_i (M - s\_i) = 0 for every row i, with s\_i = w.u\_i [Boyd & Vandenberghe, Convex Optimization, section 5.5.2 (complementary slackness)]" - Terms: declared axiom, complementary slackness, LP pair, dual weights, score, row. **Disposition: no change** (a definition, statement or proof step where the terms are the content; the unresolved ones are items in List 1 and the shorter ones items in Lists 2 and 3a).
- "by declared axiom **I1** (inherited): LP strong duality: min\_{w in simplex} max\_i w.u\_i equals the dual max over lambda in the simplex of min\_j (U^T lambda)\_j (checked numerically in pytest) [Boyd & Vandenberghe, Convex Optimization, section 5.2]" - Terms: declared axiom, LP strong duality, simplex, dual max, min-max. **Disposition: no change** (a definition, statement or proof step where the terms are the content; the unresolved ones are items in List 1 and the shorter ones items in Lists 2 and 3a).
- "by declared axiom **F12** (posited): min representation for L12 and L13: the minimum m of a finite family x\_j (the gradient components g\_j in L12, the row gaps in L13) is a symbol with x\_j \>= m for all j and x\_{j0} = m for some j0" - Terms: declared axiom, min representation, symbol, gradient components, row gaps. **Disposition: no change** (a definition, statement or proof step where the terms are the content; the unresolved ones are items in List 1 and the shorter ones items in Lists 2 and 3a).
- "by declared axiom **I8** (inherited): first-order convexity inequality: a differentiable convex f satisfies f(v) \>= f(w) + grad f(w).(v - w) for all feasible v, w [Boyd & Vandenberghe, Convex Optimization, section 3.1.3]" - Terms: declared axiom, inherited, first-order convexity inequality, gradient, feasible. **Disposition: no change** (a definition, statement or proof step where the terms are the content; the unresolved ones are items in List 1 and the shorter ones items in Lists 2 and 3a).
- "by proved result **L4**: convexity of the soft-maximum objective (second directional derivative = tau Var\_p)" - Terms: proved result, soft-maximum objective, second directional derivative, tau, Var\_p. **Disposition: no change** (a definition, statement or proof step where the terms are the content; the unresolved ones are items in List 1 and the shorter ones items in Lists 2 and 3a).


## Unit 48: paper/supporting_material.ipynb :: Appendix F. Computational reproducibility

Density 1.0 terms of art per 100 words (15/1516); staged text `supp_appendix-f-computational-reproducibility.txt`.


### List 1. Terms unresolved from the unit and the Glossary

- "- **The repository keeps:** the code, the tests, the lock file, the Dockerfile and the ledger." Term: the ledger. Never defined here or in the Glossary; the reader cannot tell what it records. **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it).
- "| uv run python -m derivation.run | run the chain L1 to L17 | every lemma reports PASS |" Terms: the chain L1 to L17, lemma. Neither the lemmas nor the chain is defined here or in the Glossary; the reader cannot tell what they establish or what PASS means. **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it).
- "| uv run python -m derivation.proofmap | check the proof map against the scripts | exits 0 |" Terms: proof map, the scripts. Undefined here and in the Glossary; which scripts, and what is mapped to what, is unstated. **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it).
- "Shell. The container paragraph (the pinned image, how to build it and run the paper in it, and what differs outside it) is supplied by the container work package." Terms: container work package, pinned image. Project-internal process term in reader-facing text; section F.2 is empty for the reader. **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it).
- "- **This appendix carries:** the pinned toolchain generated from the lock, the environment of record, the commands and what a pass looks like, and one row per figure and table with its call, its input and its output." Term: the environment of record. Used as a name, never defined; F.2 is a placeholder. **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it).
- "- **Main text keeps:** {numref}`section %s <sect-reproducibility>` in a few sentences: everything is regenerable, the environment and the commands are in this appendix, use of the package on one's own table is on the docsite." Terms: {numref}`...` (unrendered markup), docsite. Raw cross-reference syntax is visible and the docsite is not located. **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it).


### List 2. Where a Glossary term would say it shorter or more exactly

none


### List 3a. Terms of art that plain words would serve

- "- **This appendix carries:** the pinned toolchain generated from the lock, the environment of record, the commands and what a pass looks like, and one row per figure and table with its call, its input and its output." Terms: pinned toolchain, the lock, environment of record. Plain words: the exact tool versions recorded in the lock file; the environment the authors ran in. **Disposition: plain words** (replace with the plain words the reader names).
- "| uv run python paper/execute_notebooks.py | execute both notebooks from a clean kernel and write the outputs | ..." (the What-it-does cell, quoted: "execute both notebooks from a clean kernel and write the outputs") Term: clean kernel. Plain words: a fresh Python session with nothing carried over. **Disposition: plain words** (replace with the plain words the reader names).
- "- **The repository keeps:** the code, the tests, the lock file, the Dockerfile and the ledger." Term: Dockerfile. Plain words: the recipe for the container image. **Disposition: plain words** (replace with the plain words the reader names).


### List 3b. Sentences with three or more terms of art together

- "- **This appendix carries:** the pinned toolchain generated from the lock, the environment of record, the commands and what a pass looks like, and one row per figure and table with its call, its input and its output." Terms: pinned toolchain, lock, environment of record, pass. **Disposition: no change** (a definition, statement or proof step where the terms are the content; the unresolved ones are items in List 1 and the shorter ones items in Lists 2 and 3a).
- "- **The repository keeps:** the code, the tests, the lock file, the Dockerfile and the ledger." Terms: lock file, Dockerfile, ledger. **Disposition: no change** (a definition, statement or proof step where the terms are the content; the unresolved ones are items in List 1 and the shorter ones items in Lists 2 and 3a).
- "Shell. The container paragraph (the pinned image, how to build it and run the paper in it, and what differs outside it) is supplied by the container work package." Terms: container, pinned image, work package. **Disposition: no change** (a definition, statement or proof step where the terms are the content; the unresolved ones are items in List 1 and the shorter ones items in Lists 2 and 3a).
- "exits 0; the outputs are unchanged when the data and the seeds are: `git diff --stat -- paper/paper.ipynb paper/supporting_material.ipynb` then shows only the commit and platform lines of the toolchain table, and `PAPER_EXECUTE=1 uv run pytest tests/test_paper.py -k clean_kernel` compares every other text output of a fresh run with the committed one" Terms: git diff --stat, toolchain table, PAPER_EXECUTE, pytest -k clean_kernel, seeds, committed output. **Disposition: no change** (a definition, statement or proof step where the terms are the content; the unresolved ones are items in List 1 and the shorter ones items in Lists 2 and 3a).
- "exits 0, with no error reported; it prints a line that a server started on a local port, because the builder renders the pages through a temporary server that stops when the build ends" Terms: builder, local port, temporary server, static site build. **Disposition: no change** (a definition, statement or proof step where the terms are the content; the unresolved ones are items in List 1 and the shorter ones items in Lists 2 and 3a).


## Unit 49: paper/supporting_material.ipynb :: Appendix B. Proofs, step for step with their scripts (part 2)

Density 1.0 terms of art per 100 words (23/2374); staged text `supp_appendix-b-proofs-step-for-step-with-the_2.txt`.


### List 1. Terms unresolved from the unit and the Glossary

- "d/dt J\_tau(w + t v)|\_0 = sum\_i p\_i (v . u\_i) = sum\_j v\_j (sum\_i p\_i u\_ij), p = softmax(tau U w), so grad J\_tau = g = U^T p." Terms: J_tau, U, u_i, p. Why: the objective J_tau and the matrix U with rows u_i are never defined in the unit, and the Glossary has no entry for them; n and d appear without being introduced. **Disposition: no change** (standard vocabulary at the reader level the paper assumes (Boyd and Vandenberghe; scikit-learn)).
- "A2: if Z were all d coordinates the simplex sum would be 0, but A2 makes it 1" Term: Z. Why: Z (the set of zero coordinates, apparently) is used here first and never defined. **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it).
- "R1: the balanced point has w\_j \> 0, so w\_j is a positive coordinate" Terms: balanced point, balanced. Why: "balanced" is not in the Glossary; the unit only shows it by example (L3.29), never defines it. **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it).
- "the hard-support geometry is balanced: U^T p = (1, 1)" Terms: balanced, hard-support. Why: neither is in the Glossary; "balanced" is given only as an instance of U^T p having equal entries, which is not stated as the definition. **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it).
- "constructed instance: at tau = inf primal and dual values are equal (both 1)" Terms: primal, dual values. Why: the primal and dual of which program is never said, and the unit has no dual problem. **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it).
- "at tau = 1, J is strictly convex in s on the simplex segment" Terms: s, simplex segment. Why: the parameter s is never introduced (nor how it parametrizes w in the two-coordinate example). **Disposition: no change** (standard vocabulary at the reader level the paper assumes (Boyd and Vandenberghe; scikit-learn)).
- "the combination alpha 1 + sum\_j gamma\_j e\_j has component alpha + gamma\_m at m" Terms: alpha, gamma_j, e_j, m, the vector 1. Why: the coefficients and the index m are not introduced; the step is readable only after L3.17. **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it).
- "negative control: with Z all coordinates only the inside equation remains, alpha free" Term: inside equation. Why: which equation is "inside" (a coordinate in Z) versus "outside" is never stated. **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it).
- "hence the gradient is G\_j = sum\_i p\_i u\_ij, as v is arbitrary" Terms: G versus g. Why: the statement writes the gradient as g and U^T p; the capital G first appears here with no stated relation. **Disposition: no change** (standard vocabulary at the reader level the paper assumes (Boyd and Vandenberghe; scikit-learn)).
- "**Ledger.** axioms imported and applied: A2, I10, R1; proved results imported: none; exported: L3_RESULT; 35 steps." Terms: ledger, imported, exported, L3_RESULT. Why: ledger vocabulary is not in the Glossary, and the Kind column values (computed, declared axiom, posited, inherited) are not explained in the unit. **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it).
- "R1: ... the balanced point lies in the relative interior of a facet of the frontier with positive normal" (R1 text in L3.9: "the balanced point lies in the relative interior of a facet of the frontier with positive normal; this is a statement about the hard-support (tau = infinity) geometry and does not imply that the finite-tau minimizer of J\_tau is interior") Term: positive normal. Why: normal to which object and what its positivity gives is not stated. **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it).


### List 2. Where a Glossary term would say it shorter or more exactly

- "Balanced hard-support geometry (tau = infinity) does not imply an interior finite-tau minimizer: a constructed instance has a balanced hard optimum and a finite-tau minimizer on the boundary with g\_j \> lambda at the inactive j" Terms: supporting envelope, fit temperature. Why: "hard-support (tau = infinity)" is the supporting envelope, and tau is the fit temperature (infinite = exact maximum). **Disposition: glossary term** (use the Glossary term the reader names).
- "this is a statement about the hard-support (tau = infinity) geometry and does not imply that the finite-tau minimizer of J\_tau is interior" Terms: supporting envelope, fit temperature. Why: same; "finite-tau" is a finite fit temperature. **Disposition: glossary term** (use the Glossary term the reader names).
- "the balanced point lies in the relative interior of a facet of the frontier with positive normal" Terms: facet, frontier. Why: Glossary says "frontier" names three objects; here it is the supporting envelope, and the sentence should say so. **Disposition: glossary term** (use the Glossary term the reader names).
- "d/dt J\_tau(w + t v) at 0 equals sum\_i p\_i (v.u\_i), p the softmax of tau U w" Term: support weights. Why: the softmax weights of the designs are the Glossary's support weights. **Disposition: glossary term** (use the Glossary term the reader names).
- "the swap identity holds at the softmax weights p = softmax(tau U w)" Term: support weights. Why: same. **Disposition: glossary term** (use the Glossary term the reader names).
- "the exponents w lie on the simplex: w\_j \>= 0 and sum\_j w\_j = 1" Term: exponent vector. Why: the Glossary gives w as the exponent vector of term k on the simplex over the metrics. **Disposition: glossary term** (use the Glossary term the reader names).
- "the finite-tau minimizer of the instance is the boundary point w = (1, 0)" Terms: fit temperature, contending set. Why: w = (1, 0) means one metric contends (a contending set of size 1), and "finite-tau" is a finite fit temperature. **Disposition: glossary term** (use the Glossary term the reader names).


### List 3a. Terms of art that plain words would serve

- "by declared axiom A2 (posited): the exponents w lie on the simplex: w\_j \>= 0 and sum\_j w\_j = 1" Term: posited. Plain words: assumed. **Disposition: plain words** (replace with the plain words the reader names).
- "negative control: with Z all coordinates they are dependent (1 - sum\_j e\_j = 0)" Term: negative control. Plain words: counter-check, or "the same check on a case where it should fail". **Disposition: plain words** (replace with the plain words the reader names).
- "I10: g\_j = lambda + mu\_j and w\_j mu\_j = 0 termwise, so sum\_j w\_j (g\_j - lambda) = 0" Term: termwise. Plain words: term by term. **Disposition: plain words** (replace with the plain words the reader names).
- "constructed instance: at tau = inf primal and dual values are equal (both 1)" Term: constructed instance. Plain words: worked example. **Disposition: plain words** (replace with the plain words the reader names).
- "a constructed instance has a balanced hard optimum and a finite-tau minimizer on the boundary with g\_j \> lambda at the inactive j" Terms: hard optimum, inactive j. Plain words: exact-maximum optimum; a coordinate whose weight is zero. **Disposition: plain words** (replace with the plain words the reader names).
- "hence the gradient is G\_j = sum\_i p\_i u\_ij, as v is arbitrary" Term: arbitrary v. Plain words: for every direction v (fine as is; listed only because "as v is arbitrary" is the whole reason the gradient can be read off). **Disposition: plain words** (replace with the plain words the reader names).


### List 3b. Sentences with three or more terms of art together

- "At a minimizer w of J\_tau on the simplex, with lambda = w.g: g\_j \>= lambda for all j and w\_j (g\_j - lambda) = 0 (complementary slackness); the equal-gradient condition (U^T p)\_j = lambda is the case w\_j \> 0, so all components are equal at an interior minimizer." Terms: minimizer, simplex, complementary slackness, equal-gradient condition, interior minimizer. **Disposition: no change** (a definition, statement or proof step where the terms are the content; the unresolved ones are items in List 1 and the shorter ones items in Lists 2 and 3a).
- "Balanced hard-support geometry (tau = infinity) does not imply an interior finite-tau minimizer: a constructed instance has a balanced hard optimum and a finite-tau minimizer on the boundary with g\_j \> lambda at the inactive j" Terms: balanced, hard-support, tau, interior, finite-tau minimizer, hard optimum, inactive. **Disposition: no change** (a definition, statement or proof step where the terms are the content; the unresolved ones are items in List 1 and the shorter ones items in Lists 2 and 3a).
- "first-order (KKT) necessary conditions at a local minimizer w of a continuously differentiable f on the simplex {w \>= 0, sum\_j w\_j = 1}: there are lambda and mu\_j \>= 0 with g\_j - lambda - mu\_j = 0 (g = grad f(w)) and w\_j mu\_j = 0." Terms: first-order, KKT, local minimizer, simplex, multipliers, complementarity. **Disposition: no change** (a definition, statement or proof step where the terms are the content; the unresolved ones are items in List 1 and the shorter ones items in Lists 2 and 3a).
- "The constraints are affine and their active gradients (the all-ones vector, and e\_j for each w\_j = 0) are linearly independent at every point of the simplex, so the linear independence constraint qualification holds and no convexity of f is used [Nocedal & Wright, Numerical Optimization, 2nd ed., Theorem 12.1 (first-order necessary conditions) with Definition 12.4 (LICQ); for a convex f the same conditions are also Boyd & Vandenberghe, Convex Optimization, section 5.5.3, a remark and not the basis]" Terms: affine constraints, active gradients, linear independence constraint qualification, convexity. **Disposition: no change** (a definition, statement or proof step where the terms are the content; the unresolved ones are items in List 1 and the shorter ones items in Lists 2 and 3a).
- "the balanced point lies in the relative interior of a facet of the frontier with positive normal; this is a statement about the hard-support (tau = infinity) geometry and does not imply that the finite-tau minimizer of J\_tau is interior" Terms: balanced point, relative interior, facet, frontier, positive normal, hard-support, finite-tau minimizer. **Disposition: no change** (a definition, statement or proof step where the terms are the content; the unresolved ones are items in List 1 and the shorter ones items in Lists 2 and 3a).
- "I10: stationarity of J - lambda (sum\_j w\_j - 1) - sum\_j mu\_j w\_j along e\_{j0}" Terms: stationarity, Lagrangian terms (multipliers lambda, mu), e_{j0} direction. **Disposition: no change** (a definition, statement or proof step where the terms are the content; the unresolved ones are items in List 1 and the shorter ones items in Lists 2 and 3a).
- "d/dt J\_tau(w + t v)|\_0 = sum\_i p\_i (v . u\_i) = sum\_j v\_j (sum\_i p\_i u\_ij), p = softmax(tau U w), so grad J\_tau = g = U^T p." Terms: directional derivative, softmax, tau, gradient. **Disposition: no change** (a definition, statement or proof step where the terms are the content; the unresolved ones are items in List 1 and the shorter ones items in Lists 2 and 3a).


## Unit 50: paper/supporting_material.ipynb :: Appendix G. Register of prior art (part 2)

Density 0.6 terms of art per 100 words (14/2191); staged text `supp_appendix-g-register-of-prior-art_2.txt`.


### List 1. Terms unresolved from the unit and the Glossary

- "A fresh reader read what is accessible of each cited work (abstracts, open full texts, publisher descriptions; not the paywalled books and articles) and checked each sentence of {numref}`section %s <sect-problem>` and {numref}`section %s <sect-prior-art>`, the sketch of the Pareto theorem (L11) and the process paragraph that says what a cited work says." Terms: L11, the Pareto theorem. Neither is defined here or in the Glossary, so the reader cannot tell which result is sketched. **Disposition: no change** (standard vocabulary at the reader level the paper assumes (Boyd and Vandenberghe; scikit-learn)).
- "L11 proof sketch: 'Only the log-convex part of a front is reached by some w'" Terms: log-convex part of a front, w. The Glossary has no front and no w; what w weights is not said. **Disposition: no change** (standard vocabulary at the reader level the paper assumes (Boyd and Vandenberghe; scikit-learn)).
- "Table row Pareto: 'Returns a nondominated set of designs, and traces its supported part with scalarizations such as weighted sums' (and Pareto paragraph: 'Pareto methods return a nondominated set and trace its supported part by scalarization')" Term: supported part. It is not in the Glossary and is not standard at the stated level, though the unit says the words were removed. **Disposition: no change** (standard vocabulary at the reader level the paper assumes (Boyd and Vandenberghe; scikit-learn)).
- "DEA: 'It builds a one-sided envelope of the data and scores each unit against it'" Terms: DEA, unit. DEA is never expanded or defined, and a unit is not a Glossary term. **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it).
- "'scores above one in the super-efficiency variant'" Term: super-efficiency. It is undefined, and the reader cannot see what a score above one means. **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it).
- "'Malmquist indices across data sets'" Term: Malmquist index. It is undefined and not standard at the reader level. **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it).
- "'each unit in DEA may choose favourable weights, a problem answered there by weights restrictions'" Terms: favourable weights, weights restrictions. Neither is defined; the reader cannot tell what the problem is. **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it).
- "Table row DEA: 'variants for scale and returns to scale'" Term: returns to scale. It is an economics term and is not defined. **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it).
- "Lineage: 'The weighted geometric mean with exponents summing to one is the constant-returns Cobb-Douglas form'" Terms: constant-returns, Cobb-Douglas form. These are economics terms that the reader at this level does not necessarily have. **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it).
- "Lineage: 'reading V as the factor that scales a design to the boundary is a distance-function reading'; table: 'the Shephard distance function with its duality'" Terms: distance function, its duality. The unit never says which duality. **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it).
- "Lineage: 'Frontier estimation by programming, corrected least squares and one-sided error is the family of one-sided fits'; table: 'programming, corrected OLS or maximum likelihood, and stochastic frontiers with one-sided error'" Terms: corrected least squares (COLS), stochastic frontiers. They are undefined, and the Glossary does not cover them. **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it).
- "Lineage: 'The chart is in the spirit of log-ratio coordinates for compositional data'; table: 'PCA of compositional data, and isometric logratio transformations to coordinates free of the constant-sum constraint'" Terms: compositional data, isometric logratio, constant-sum constraint. They are statistics terms not defined here; the Glossary chart does not cover them. **Disposition: no change** (standard vocabulary at the reader level the paper assumes (Boyd and Vandenberghe; scikit-learn)).
- "Lineage: 'The model class and refit scheme come from geometric programming and max-affine fitting'; table: 'Geometric programming with generalized posynomials'" Terms: max-affine fitting, refit scheme. Max-affine is not in the Glossary, and the Glossary mentions a refit only under facet gap. **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it).
- "Lineage: 'the soft maximum is an entropic risk functional'" Term: entropic risk functional. It is undefined, and the Glossary has no entry for it. **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it).
- "'"hyperbolic" here is unrelated to hyperbolic PCA'; table: 'PCA in hyperbolic space with horospherical projections'" Terms: hyperbolic PCA, horospherical projections. Neither is defined, and the sentence says only what the word does not mean. **Disposition: no change** (standard vocabulary at the reader level the paper assumes (Boyd and Vandenberghe; scikit-learn)).
- "Table row MBSE: 'MBSE centred on the system model as the sole source of truth'" Term: MBSE. It is never expanded; the reader at this level does not necessarily know it. **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it).
- "'weighted-criteria comparison methods (Pugh, AHP, Kepner-Tregoe)'" Terms: Pugh, AHP, Kepner-Tregoe. They are named methods that are not defined and not standard at the reader level. **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it).


### List 2. Where a Glossary term would say it shorter or more exactly

- "DEA: 'It builds a one-sided envelope of the data and scores each unit against it'" Glossary term: supporting envelope. It is a hyperplane that supports the observed rows from above, which is more exact than one-sided envelope. **Disposition: no change** (the sentence reports a source in its own words (exempt by the note)).
- "Lineage: 'Frontier estimation by programming, corrected least squares and one-sided error is the family of one-sided fits'; table: 'programming, corrected OLS or maximum likelihood, and stochastic frontiers with one-sided error'" Glossary term: fit temperature. The Glossary defines the one-sided fit through it, with infinite temperature the exact maximum. **Disposition: no change** (the sentence reports a source in its own words (exempt by the note)).
- "Table row Pareto: 'Returns a nondominated set of designs, and traces its supported part with scalarizations such as weighted sums' (and Pareto paragraph: 'Pareto methods return a nondominated set and trace its supported part by scalarization')" Glossary term: Pareto boundary. It is the nondominated points of the attainable set. **Disposition: no change** (the sentence reports a source in its own words (exempt by the note)).
- "Lineage: 'reading V as the factor that scales a design to the boundary is a distance-function reading'; table: 'the Shephard distance function with its duality'" Glossary terms: improvement factor, invariant value. V as the factor on a metric that brings a design to V = 1 is exactly the improvement factor. **Disposition: no change** (the sentence reports a source in its own words (exempt by the note)).
- "Lineage: 'The weighted geometric mean with exponents summing to one is the constant-returns Cobb-Douglas form'" Glossary terms: invariant value, exponent vector. The first is a weighted geometric mean of the metrics, and the second carries weights on the simplex, so exponents summing to one is already the exponent vector. **Disposition: no change** (the sentence reports a source in its own words (exempt by the note)).
- "L11 proof sketch: 'Only the log-convex part of a front is reached by some w'" Glossary terms: Pareto boundary, supporting envelope. Together they say what is reached and by what. **Disposition: no change** (the sentence reports a source in its own words (exempt by the note)).
- "Lineage: 'The model class and refit scheme come from geometric programming and max-affine fitting'; table: 'Geometric programming with generalized posynomials'" Glossary terms: geometric program, generalized geometric program. These use the name the Glossary defines. **Disposition: no change** (the sentence reports a source in its own words (exempt by the note)).


### List 3a. Terms of art that plain words would serve

- "'each unit in DEA may choose favourable weights, a problem answered there by weights restrictions'" Term: weights restrictions. Plain words: limits on how large or small each weight may be. **Disposition: no change** (the sentence reports a source in its own words (exempt by the note)).
- "Table row Pareto: 'Returns a nondominated set of designs, and traces its supported part with scalarizations such as weighted sums' (and Pareto paragraph: 'Pareto methods return a nondominated set and trace its supported part by scalarization')" Term: scalarization. Plain words: combining the objectives into one weighted score. **Disposition: no change** (the sentence reports a source in its own words (exempt by the note)).
- "Lineage: 'Frontier estimation by programming, corrected least squares and one-sided error is the family of one-sided fits'; table: 'programming, corrected OLS or maximum likelihood, and stochastic frontiers with one-sided error'" Term: corrected OLS. Plain words: ordinary least squares shifted up until it lies on the best points. **Disposition: no change** (the sentence reports a source in its own words (exempt by the note)).
- "'scores above one in the super-efficiency variant'" Term: super-efficiency. Plain words: ranking the best units against all the others. **Disposition: no change** (the sentence reports a source in its own words (exempt by the note)).


### List 3b. Sentences with three or more terms of art together

- "Lineage: 'Frontier estimation by programming, corrected least squares and one-sided error is the family of one-sided fits'; table: 'programming, corrected OLS or maximum likelihood, and stochastic frontiers with one-sided error'" Terms: programming, corrected least squares, one-sided error, maximum likelihood, stochastic frontiers. Five terms stacked. **Disposition: no change** (the sentence reports a source in its own words (exempt by the note)).
- "Lineage: 'The chart is in the spirit of log-ratio coordinates for compositional data'; table: 'PCA of compositional data, and isometric logratio transformations to coordinates free of the constant-sum constraint'" Terms: log-ratio coordinates, compositional data, isometric logratio, constant-sum constraint. **Disposition: no change** (the sentence reports a source in its own words (exempt by the note)).
- "Lineage: 'The model class and refit scheme come from geometric programming and max-affine fitting'; table: 'Geometric programming with generalized posynomials'" Terms: model class, refit scheme, geometric programming, max-affine fitting. **Disposition: no change** (the sentence reports a source in its own words (exempt by the note)).
- "Table row Pareto: 'Returns a nondominated set of designs, and traces its supported part with scalarizations such as weighted sums' (and Pareto paragraph: 'Pareto methods return a nondominated set and trace its supported part by scalarization')" Terms: nondominated set, supported part, scalarization, weighted sums. **Disposition: no change** (the sentence reports a source in its own words (exempt by the note)).
- "'each unit in DEA may choose favourable weights, a problem answered there by weights restrictions'" Terms: DEA, favourable weights, weights restrictions. **Disposition: no change** (the sentence reports a source in its own words (exempt by the note)).
- "Lineage: 'Tradespace exploration displays a table of designs'; table: 'Value-focused broad exploration of design alternatives, user-guided samplers and linked visualization with the Pareto frontier displayed'" Terms: tradespace exploration, value-focused exploration, user-guided samplers, linked visualization, Pareto frontier. **Disposition: no change** (the sentence reports a source in its own words (exempt by the note)).
- "Lineage: 'reading V as the factor that scales a design to the boundary is a distance-function reading'; table: 'the Shephard distance function with its duality'" Terms: V, boundary, distance function, duality. **Disposition: no change** (the sentence reports a source in its own words (exempt by the note)).
- "reworded to what was read. Cited now for weights restrictions arising in practice; 'favourable weights chosen by each unit' is no longer attributed." Terms: weights restrictions, favourable weights, unit. **Disposition: no change** (the sentence reports a source in its own words (exempt by the note)).
- "reworded to what was read. 'Scores above one' is no longer attributed; the sentence says a super-efficiency variant ranks efficient units against a reference technology spanned by all other units." Terms: super-efficiency, efficient units, reference technology. **Disposition: no change** (the sentence reports a source in its own words (exempt by the note)).


## Unit 51: paper/supporting_material.ipynb :: Appendix B. Proofs, step for step with their scripts (part 11)

Density 0.0 terms of art per 100 words (0/291); staged text `supp_appendix-b-proofs-step-for-step-with-the_11.txt`.


### List 1. Terms unresolved from the unit and the Glossary

- "The checker passes only when: every proof names one file; every step of every file belongs to exactly one proof; the prose steps and the script steps correspond one to one and in order; every step by a declared axiom applies an entry that exists in the ledger and that the file imports; the entries a file imports, applies and lists as used are the same set; a proved result is imported from an earlier proof and applied by a step; no premise hides in a signed symbol; and the fingerprint of each step (its tag, prose and line of code) and of each ledger entry equals the record's." Terms: ledger, ledger entry, signed symbol, "premise hides in a signed symbol", fingerprint, tag, record, proved result. Why: none is in the Glossary or standard at this level; the opening sentence leans on all of them and the section starts with no setup. **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it).
- "| `lemma_01_homogeneity.py` | A1, A2 | none | L1_RESULT | 8 | 0 |" (and every table row with codes A1..A8, F5, F10, F12, I1..I16, R1, R2). Terms: A1, I10, R1, F5 etc., L1_RESULT. Why: the entry codes and result names are never decoded here (axiom, identity, ... family unknown), so the "Ledger entries imported" column cannot be read. **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it).
- "| Signed symbols declared as hypotheses |" with counts 0, 1, 5, 10. Terms: signed symbol, hypothesis. Why: not defined; why lemmas 11 and 13 need 5 and 10 is opaque. **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it).
- "| Check the scripts against the record | `uv run python -m derivation.proofmap` |" and "| Refresh the record (deliberate; prints what moved) | `uv run python -m derivation.proofmap --update` |". Terms: proofmap, --execute, --update. Why: no statement of what "computed step" versus other steps means, or what moving means. **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it).
- "| Lemma files, steps | 17, 364 |". Terms: lemma file, step. Why: a lemma file and a step are used as units without definition; the Glossary has n-lemma only, a different thing. **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it).


### List 2. Where a Glossary term would say it shorter or more exactly

none


### List 3a. Terms of art that plain words would serve

- "every step by a declared axiom applies an entry that exists in the ledger". Terms: ledger. Plain words: the list of assumed facts. **Disposition: plain words** (replace with the plain words the reader names).
- "the fingerprint of each step ... equals the record's". Terms: fingerprint, record. Plain words: hash (checksum) of each step matches the saved copy. **Disposition: plain words** (replace with the plain words the reader names).
- "| Exported |" and "Proved results imported". Terms: exported, imported. Plain words: provides, uses from an earlier proof. **Disposition: plain words** (replace with the plain words the reader names).
- "| Ledger entries fingerprinted | 30 |". Terms: fingerprinted. Plain words: given a checksum. **Disposition: plain words** (replace with the plain words the reader names).


### List 3b. Sentences with three or more terms of art together

- "The checker passes only when: every proof names one file; every step of every file belongs to exactly one proof; the prose steps and the script steps correspond one to one and in order; every step by a declared axiom applies an entry that exists in the ledger and that the file imports; the entries a file imports, applies and lists as used are the same set; a proved result is imported from an earlier proof and applied by a step; no premise hides in a signed symbol; and the fingerprint of each step (its tag, prose and line of code) and of each ledger entry equals the record's." Why: checker, axiom, ledger, proved result, signed symbol, fingerprint, tag and record in one sentence, eight clauses. **Disposition: no change** (a definition, statement or proof step where the terms are the content; the unresolved ones are items in List 1 and the shorter ones items in Lists 2 and 3a).


## Unit 52: paper/paper.ipynb :: Acknowledgments and process

Density 0.0 terms of art per 100 words (0/70); staged text `paper_acknowledgments-and-process.txt`.


### List 1. Terms unresolved from the unit and the Glossary

- "AI coding assistance (Claude Code, Anthropic) drafted code, derivation scripts and text inside those packages, in a process modelled on the harness described in [@zargham2026incose], whose deterministic checks and named human approver are the verification mechanism this paper inherits." Terms: "harness", "deterministic checks". Why: "harness" is never defined here and is not in the Glossary; the reader must follow a citation to learn what it is or what the checks test. **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it).
- Same sentence. Term: "derivation scripts". Why: not in the Glossary; the reader cannot tell which derivations (which results) these produce. **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it).
- "The derivations are machine-checked." Terms: "derivations", "machine-checked". Why: unsaid what is checked, by what tool, and what "checked" guarantees (symbolic identity? proof?); the Glossary has no entry. **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it).
- "Work was done in supervisor-gated work packages: a written scope the author approved before execution, and a review afterwards." Term: "supervisor-gated work packages". Why: only half-explained by the colon; "supervisor" versus "author" is unclear (same person or not), and "work package" is not in the Glossary. **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it).


### List 2. Where a Glossary term would say it shorter or more exactly

none


### List 3a. Terms of art that plain words would serve

- "Work was done in supervisor-gated work packages: a written scope the author approved before execution, and a review afterwards." Term: "supervisor-gated work packages". Plain words: "stages of work, each approved in writing before it began and reviewed after". **Disposition: plain words** (replace with the plain words the reader names).
- "AI coding assistance (Claude Code, Anthropic) drafted code, derivation scripts and text inside those packages, in a process modelled on the harness described in [@zargham2026incose], whose deterministic checks and named human approver are the verification mechanism this paper inherits." Terms: "harness", "verification mechanism ... inherits". Plain words: "the workflow", "the way correctness is checked, which this paper takes over". **Disposition: plain words** (replace with the plain words the reader names).
- "The derivations are machine-checked." Term: "machine-checked". Plain words: "checked by a program" (and say which). **Disposition: plain words** (replace with the plain words the reader names).


### List 3b. Sentences with three or more terms of art together

- "AI coding assistance (Claude Code, Anthropic) drafted code, derivation scripts and text inside those packages, in a process modelled on the harness described in [@zargham2026incose], whose deterministic checks and named human approver are the verification mechanism this paper inherits." Terms: harness, deterministic checks, named human approver, verification mechanism, derivation scripts. **Disposition: no change** (a definition, statement or proof step where the terms are the content; the unresolved ones are items in List 1 and the shorter ones items in Lists 2 and 3a).


## Unit 53: docs/api-reference.md

Density 0.0 terms of art per 100 words (0/63); staged text `docs_api-reference.md.txt`.


### List 1. Terms unresolved from the unit and the Glossary

- "## `TradeSpaceRegressor`" — TradeSpaceRegressor: a class name with no gloss in the unit and not in the Glossary; a reader cannot tell how it differs from HyperbolicTradeSpace. **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it).
- "## `HyperbolicTradeSpace`" — HyperbolicTradeSpace: the main class is named but not described here and not in the Glossary; "hyperbolic" is not explained. **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it).
- "## `frontier_in_original_units`" — frontier, original units: the Glossary says "frontier" names one of three objects and the heading does not say which; "original units" is not defined (attributes versus metrics?). **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it).
- "## `make_configured_frontier_data`" — configured frontier data: unit gives no hint what "configured" adds over make_frontier_data; Glossary has "configuration" but not this use. **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it).
- "## `select_temperature`" — temperature: the Glossary has fit temperature and term temperature, and the name does not say which is selected or by what criterion. **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it).
- "## `__version__`" — none beyond standard; skip. **Disposition: amend glossary entry** (add an entry, or define the term at its first use, so the page resolves it).


### List 2. Where a Glossary term would say it shorter or more exactly

- "## `LogAffinePreconditioner`" — conditioning: the Glossary says LogAffinePreconditioner does the conditioning (attributes to metrics); the unit gives no such pointer. **Disposition: glossary term** (use the Glossary term the reader names).
- "## `tension_report`" — participation threshold: the Glossary says the threshold is a parameter of tension_report; the unit does not link the name to it. **Disposition: glossary term** (use the Glossary term the reader names).
- "## `frontier_in_original_units`" — fitted reference surface / supporting envelope / Pareto boundary: Glossary term would name exactly which frontier is returned. **Disposition: glossary term** (use the Glossary term the reader names).
- "## `make_configured_frontier_data`" — configuration: the Glossary term would say what "configured" means (design variables carried as covariates). **Disposition: glossary term** (use the Glossary term the reader names).


### List 3a. Terms of art that plain words would serve

- "Generated from the numpydoc docstrings of the public names." — "public names": plain words "the functions and classes you are meant to call". **Disposition: plain words** (replace with the plain words the reader names).


### List 3b. Sentences with three or more terms of art together

none


## Unit 54: paper/supporting_material.ipynb :: front matter

Density 0.0 terms of art per 100 words (0/26); staged text `supp_front.txt`.


### List 1. Terms unresolved from the unit and the Glossary

none


### List 2. Where a Glossary term would say it shorter or more exactly

none


### List 3a. Terms of art that plain words would serve

none


### List 3b. Sentences with three or more terms of art together

none


## Routing table

| Routed to | Unit | Item (opening words) | Disposition recorded |
|---|---|---|---|
| P6 | 1. docs/api.md | "`hyperbolic_trade_space.solvers`: the multi-term solver, the `Termination` record and the certificate functio... | amend glossary entry |
| P6 | 1. docs/api.md | "with `min_curvature` for a soft fit" Glossary: fit temperature (finite); conditioning of the exponents (curva... | glossary term |
| P6 | 1. docs/api.md | "`hyperbolic_trade_space.solvers`: the multi-term solver, the `Termination` record and the certificate functio... | no change |
| P1 | 4. paper/paper.ipynb :: Definitions | "The reach $\beta_k$ is the support value of the data in direction $w_k$." Terms: reach, support value. Neithe... | no change |
| P1 | 4. paper/paper.ipynb :: Definitions | "The facet share is the fraction of near-frontier designs that facet $k$ dominates; it shows which facets carr... | amend glossary entry |
| P1 | 4. paper/paper.ipynb :: Definitions | "Working-temperature exponents grade the members, and a member can carry a small one." Terms: working-temperat... | amend glossary entry |
| P1 | 4. paper/paper.ipynb :: Definitions | "The contending set of facet $k$ is the support (exponents above $10^{-9}$) of the exact-maximum ($\tau=\infty... | amend glossary entry |
| P1 | 4. paper/paper.ipynb :: Definitions | "The near-frontier band is $/\log V/<1/\tau$: in the soft maximum a design inside it weighs within a factor $e... | amend glossary entry |
| P1 | 4. paper/paper.ipynb :: Definitions | "designs of equal $V$ stand at the same level" Terms: level. Used as a noun throughout ("levels", "level relat... | amend glossary entry |
| P1 | 4. paper/paper.ipynb :: Definitions | "and $\log V$, the energy differential, is a design's level relative to the reference surface $V=1$: negative ... | glossary term |
| P1 | 4. paper/paper.ipynb :: Definitions | "The contending set of facet $k$ is the support (exponents above $10^{-9}$) of the exact-maximum ($\tau=\infty... | glossary term |
| P1 | 4. paper/paper.ipynb :: Definitions | "The reach $\beta_k$ is the support value of the data in direction $w_k$." Glossary: "supporting envelope" (a ... | glossary term |
| P1 | 4. paper/paper.ipynb :: Definitions | "Where several trade-offs are active at once, the model is a sum of such terms, one per facet." Glossary: "pos... | glossary term |
| P1 | 4. paper/paper.ipynb :: Definitions | "On facet $k$ the tangent space $\{v:w_k\cdot v=0\}$ trades contending metrics at constant $V$; the normal $w_... | glossary term |
| P1 | 4. paper/paper.ipynb :: Definitions | "$Z=Bu$, with $BB^\top=I$ and $B\mathbf 1=0$, is the position along the frontier, free of overall scale." Glos... | glossary term |
| P1 | 4. paper/paper.ipynb :: Definitions | "contending set" / "contending metrics": plain words "the metrics that matter on this facet".... | plain words |
| P1 | 4. paper/paper.ipynb :: Definitions | "support (exponents above $10^{-9}$)": plain words "the metrics with positive weight".... | plain words |
| P1 | 4. paper/paper.ipynb :: Definitions | "reach": plain words "how far the data extends in that direction".... | plain words |
| P1 | 4. paper/paper.ipynb :: Definitions | "ascent direction" / "steepest ascent": plain words "uphill direction".... | plain words |
| P1 | 4. paper/paper.ipynb :: Definitions | "near-frontier band": plain words "the designs close to the surface".... | plain words |
| P1 | 4. paper/paper.ipynb :: Definitions | "grade the members": plain words "rank the members by weight".... | plain words |
| P1 | 4. paper/paper.ipynb :: Definitions | "The contending set of facet $k$ is the support (exponents above $10^{-9}$) of the exact-maximum ($\tau=\infty... | no change |
| P1 | 4. paper/paper.ipynb :: Definitions | "$V_K(m)=\big(\sum_{k=1}^{K}c_k\prod_j m_j^{\kappa w_{kj}}\big)^{1/\kappa}$ with $w_k\in\Delta$ and $c_k=e^{-\... | no change |
| P1 | 4. paper/paper.ipynb :: Definitions | "The facet share is the fraction of near-frontier designs that facet $k$ dominates; it shows which facets carr... | no change |
| P1 | 4. paper/paper.ipynb :: Definitions | "The near-frontier band is $/\log V/<1/\tau$: in the soft maximum a design inside it weighs within a factor $e... | no change |
| P1 | 4. paper/paper.ipynb :: Definitions | "The chart separates where a design sits along the surface from its energy differential, how far it is from th... | no change |
| P1 | 4. paper/paper.ipynb :: Definitions | "On facet $k$ the tangent space $\{v:w_k\cdot v=0\}$ trades contending metrics at constant $V$; the normal $w_... | no change |
| P6 | 6. docs/examples.md | "The tension report finds a contending set of six metrics (total mass, slew time, energy balance, control effo... | amend glossary entry |
| P6 | 6. docs/examples.md | "The mean slack falls from 0.204 at one term to 0.117 at three, and the status is `certified`." Term: mean sla... | amend glossary entry |
| P6 | 6. docs/examples.md | "The largest facet holds 78 percent of the near-frontier share and is the only one containing total mass and p... | amend glossary entry |
| P6 | 6. docs/examples.md | "This block fits a planted table and draws it with lines of equal V:" Term: planted table. Not defined; make_f... | amend glossary entry |
| P6 | 6. docs/examples.md | "The same steps apply to any table of designs: condition, `select_temperature`, fit, then read the [tension re... | amend glossary entry |
| P6 | 6. docs/examples.md | "With the temperature selected for a tenth of the designs above V = 1:" Glossary term: fit temperature.... | glossary term |
| P6 | 6. docs/examples.md | "V also depends on the total, so a marker is not where V = 1." Glossary terms: invariant value (for V) and fit... | glossary term |
| P6 | 6. docs/examples.md | "The same steps apply to any table of designs: condition, `select_temperature`, fit, then read the [tension re... | glossary term |
| P6 | 6. docs/examples.md | "Figure 7. The 706 feasible designs by their first two position coordinates; the ringed designs lie nearest th... | glossary term |
| P6 | 6. docs/examples.md | "The largest facet holds 78 percent of the near-frontier share and is the only one containing total mass and p... | glossary term |
| P6 | 6. docs/examples.md | "Exponents add over groups exactly: a facet's weight on a subsystem is a sum." Glossary term: exponent vector ... | glossary term |
| P6 | 6. docs/examples.md | "The aggressive-gains table has 706 feasible designs. With the temperature selected..." / "Ten attributes are ... | plain words |
| P6 | 6. docs/examples.md | "This block fits a planted table and draws it with lines of equal V:" : "planted" would be served by "syntheti... | plain words |
| P6 | 6. docs/examples.md | "...and can be cherry-picked; the triangle is for reading, not for measuring distance;" : "cherry-picked" woul... | plain words |
| P6 | 6. docs/examples.md | "The tension report finds a contending set of six metrics" : "contending set" would be served by "the metrics ... | plain words |
| P6 | 6. docs/examples.md | "A numbered marker is a facet's exponent vector, where that facet's V is largest for a fixed total." (facet, e... | no change |
| P6 | 6. docs/examples.md | "The mean slack falls from 0.204 at one term to 0.117 at three, and the status is `certified`." (slack, term, ... | no change |
| P6 | 6. docs/examples.md | "The largest facet holds 78 percent of the near-frontier share and is the only one containing total mass and p... | no change |
| P6 | 6. docs/examples.md | "The tension report finds a contending set of six metrics (total mass, slew time, energy balance, control effo... | no change |
| P6 | 6. docs/examples.md | "A region is where one facet dominates, named by the metrics that trade there: an analysis of the fit, not a l... | no change |
| P1 | 7. paper/paper.ipynb :: Methods | "The fit asks for the positive combination of log-metrics along which the data have the smallest upper extent,... | glossary term |
| P1 | 7. paper/paper.ipynb :: Methods | "(ii) ... fitting at a finite $\kappa$ is the soft fit of {numref}`Section %s <sect-results>`, which does chan... | glossary term |
| P1 | 7. paper/paper.ipynb :: Methods | "entropic soft maximum": "smooth maximum". The paper's own definition (log-mean-exp) follows at once.... | plain words |
| P6 | 10. docs/user-guide/chart.md | "For a multi-term fit, log V is the soft maximum over facets, and `improvement_factors` uses each row's active... | amend glossary entry |
| P6 | 10. docs/user-guide/chart.md | "For a multi-term fit, log V is the soft maximum over facets, and `improvement_factors` uses each row's active... | no change |
| P6 | 11. docs/theory.md | "using the log-mean-exp (entropic) soft maximum of $w\cdot u$ over the designs." Term: soft maximum. Plain wor... | plain words |
| P6 | 11. docs/theory.md | "The fit chooses $w$ and an offset $\beta$ so that the data lie on or below the surface $\log V=w\cdot u-\beta... | no change |
| P6 | 13. docs/user-guide/termination.md | "`not_applicable`: one term, `facet_step="tangent"`, a `penalty`, one metric, fewer designs than facets, or a ... | amend glossary entry |
| P6 | 13. docs/user-guide/termination.md | "`min_curvature`: soft fit only, the smallest curvature on the active face; `nan` otherwise." Term: conditioni... | glossary term |
| P6 | 13. docs/user-guide/termination.md | "A soft fit (finite `term_temperature`) has no assignment, so no margin:" Term: term temperature. "Soft fit" i... | glossary term |
| P6 | 13. docs/user-guide/termination.md | "`not_applicable`: one term, `facet_step="tangent"`, a `penalty`, one metric, fewer designs than facets, or a ... | no change |
| P6 | 13. docs/user-guide/termination.md | "`min_curvature`: soft fit only, the smallest curvature on the active face; `nan` otherwise." Terms: soft fit,... | no change |
| P6 | 14. docs/user-guide/fitting.md | "`objective_` and `mean_slack_`: `objective_` is what the solver minimized, the soft maximum at one term and t... | amend glossary entry |
| P6 | 14. docs/user-guide/fitting.md | "`objective_` and `mean_slack_`: `objective_` is what the solver minimized, the soft maximum at one term and t... | no change |
| P1 | 16. paper/paper.ipynb :: The fit and its geometry | "The invariant value scales with the metrics (L1), and shifting every log-metric by a constant moves the offse... | amend glossary entry |
| P1 | 16. paper/paper.ipynb :: The fit and its geometry | "**Derived.** *Hypotheses.* A1, A2, A3; $w\in\Delta$." Terms: A3, Delta. A3 is never stated (A1 and A2 are glo... | amend glossary entry |
| P1 | 16. paper/paper.ipynb :: The fit and its geometry | "**Derived.** *Hypotheses.* A2; R1 for the facet-normal reading; $w$ minimizes $J_\tau$ on $\Delta$." Terms: R... | amend glossary entry |
| P1 | 16. paper/paper.ipynb :: The fit and its geometry | "Balanced hard-support geometry does not imply an interior minimizer at finite $\tau$." Terms: "balanced hard-... | amend glossary entry |
| P1 | 16. paper/paper.ipynb :: The fit and its geometry | "$\nabla J_\tau=U^\top p$, $p=\mathrm{softmax}(\tau Uw)$. With $g=\nabla J_\tau(w)$, $\lambda=w\cdot g$: $g_j\... | no change |
| P1 | 16. paper/paper.ipynb :: The fit and its geometry | "**Derived.** *Hypotheses.* A3; F5 (the maximum is attained)." Terms: F5, N, s_i. The labels are not defined, ... | amend glossary entry |
| P1 | 16. paper/paper.ipynb :: The fit and its geometry | "**Derived.** *Hypotheses.* A2, A3, A5, I5 (moment generating functions multiply); a population identity, with... | amend glossary entry |
| P1 | 16. paper/paper.ipynb :: The fit and its geometry | "**Derived.** *Hypotheses.* A7; I6 ($QQ^\top=I$ implies $Q^\top Q=I$)." Terms: A7, Z, B, Q. The Helmert-type m... | amend glossary entry |
| P1 | 16. paper/paper.ipynb :: The fit and its geometry | "**Derived.** *Hypotheses.* A2, A4: $\log m_j=\alpha_j\log(a_j+s_j)+b_j$, $\alpha_j\neq0$." Terms: s_j, alpha_... | amend glossary entry |
| P1 | 16. paper/paper.ipynb :: The fit and its geometry | "**Derived.** *Hypotheses.* A1, A6; F10 (the maximum is attained) for the limit." Terms: A6, F10. Undefined la... | amend glossary entry |
| P1 | 16. paper/paper.ipynb :: The fit and its geometry | "$\Phi_K(u+c\mathbf 1)=\Phi_K(u)+c$; $\Phi_1=w_1\cdot u-\beta_1$; $\max_kx_k\le\Phi_K\le\max_kx_k+(\log K)/\ka... | amend glossary entry |
| P1 | 16. paper/paper.ipynb :: The fit and its geometry | "A maximizer of $V$ is weakly efficient in all $d$ metrics, and efficient when every $w_j>0$; at $K>1$, $\kapp... | amend glossary entry |
| P1 | 16. paper/paper.ipynb :: The fit and its geometry | "For $u'=u+\delta$, $\delta\ge0$, the gain $\sum_jw_j\delta_j$ is a sum of nonnegative terms; take the contrap... | no change |
| P1 | 16. paper/paper.ipynb :: The fit and its geometry | "Simplex exponents turn the shift into $c$ in every term; the bounds are the squeeze of {prf:ref}`thm-lme`; ea... | amend glossary entry |
| P1 | 16. paper/paper.ipynb :: The fit and its geometry | "**Derived.** *Hypotheses.* A1, A2; $w_j\neq0$; the frontier is the hyperplane $\{w\cdot u=\beta\}$." Term: fa... | glossary term |
| P1 | 16. paper/paper.ipynb :: The fit and its geometry | "Improving metric $j$ alone by $V^{-1/w_j}$, or every metric by $1/V$, reaches $V=1$." Term: improvement facto... | glossary term |
| P1 | 16. paper/paper.ipynb :: The fit and its geometry | "$Z(u+c\mathbf 1)=Z(u)$ and $u=B^\top Z+\frac1d(\mathbf 1^\top u)\mathbf 1$: the map between $u$ and (position... | glossary term |
| P1 | 16. paper/paper.ipynb :: The fit and its geometry | "A maximizer of $V$ is weakly efficient in all $d$ metrics, and efficient when every $w_j>0$; at $K>1$, $\kapp... | glossary term |
| P1 | 16. paper/paper.ipynb :: The fit and its geometry | "With several terms, $V_K$ is the $1/\kappa$ power of a posynomial and its logarithm lies within $(\log K)/\ka... | add to avoid |
| P1 | 16. paper/paper.ipynb :: The fit and its geometry | "$\frac{d^2}{dt^2}J_\tau(w+tv)/_0=\tau\mathrm{Var}_p(v\cdot u)\ge0$: $J_\tau$ is convex, not claimed strictly.... | glossary term |
| P1 | 16. paper/paper.ipynb :: The fit and its geometry | "Two results say what the fitted numbers mean: the soft maximum of Gaussian noise has a closed form (L6), and ... | glossary term |
| P1 | 16. paper/paper.ipynb :: The fit and its geometry | "$J_\tau(w;U+c\mathbf 1^\top)=J_\tau(w;U)+c$: $\beta$ moves by $c$ and $w^*$ is unchanged." together with "the... | plain words |
| P1 | 16. paper/paper.ipynb :: The fit and its geometry | "That only the log-convex part of a front is reached by some $w$ is our statement, not a cited one.": "log-con... | plain words |
| P1 | 16. paper/paper.ipynb :: The fit and its geometry | "**Derived.** *Hypotheses.* A2, A3, A5, I5 (moment generating functions multiply); a population identity, with... | plain words |
| P1 | 16. paper/paper.ipynb :: The fit and its geometry | "$Z(u+c\mathbf 1)=Z(u)$ and $u=B^\top Z+\frac1d(\mathbf 1^\top u)\mathbf 1$: the map between $u$ and (position... | plain words |
| P1 | 16. paper/paper.ipynb :: The fit and its geometry | "The chart is a reversible rewriting of the log-metrics (L8), and under log-affine conditioning the pull-back ... | plain words |
| P1 | 16. paper/paper.ipynb :: The fit and its geometry | "Balanced hard-support geometry does not imply an interior minimizer at finite $\tau$.": "balanced hard-suppor... | plain words |
| P1 | 16. paper/paper.ipynb :: The fit and its geometry | "The one-facet fit has simplex optimality conditions (L3), is convex (L4), and uses the log-mean-exp, which di... | no change |
| P1 | 16. paper/paper.ipynb :: The fit and its geometry | "Two results say what the fitted numbers mean: the soft maximum of Gaussian noise has a closed form (L6), and ... | no change |
| P1 | 16. paper/paper.ipynb :: The fit and its geometry | "The chart is a reversible rewriting of the log-metrics (L8), and under log-affine conditioning the pull-back ... | no change |
| P1 | 16. paper/paper.ipynb :: The fit and its geometry | "With several terms, $V_K$ is the $1/\kappa$ power of a posynomial and its logarithm lies within $(\log K)/\ka... | no change |
| P1 | 16. paper/paper.ipynb :: The fit and its geometry | "A maximizer of $V$ is weakly efficient in all $d$ metrics, and efficient when every $w_j>0$; at $K>1$, $\kapp... | no change |
| P1 | 16. paper/paper.ipynb :: The fit and its geometry | "Simplex exponents turn the shift into $c$ in every term; the bounds are the squeeze of {prf:ref}`thm-lme`; ea... | no change |
| P6 | 23. docs/user-guide/limitations.md | "A very high tau rests the fit on a few extreme designs; below tau of about 3 the soft maximum approaches the ... | no change |
| P1 | 24. paper/paper.ipynb :: The decision problem | "The several-facet fit, not convex in the terms, has three levels of guarantee and a stopping declaration ({pr... | no change |
| P1 | 24. paper/paper.ipynb :: The decision problem | "The several-facet fit, not convex in the terms, has three levels of guarantee and a stopping declaration ({pr... | glossary term |
| P1 | 24. paper/paper.ipynb :: The decision problem | "The several-facet fit, not convex in the terms, has three levels of guarantee and a stopping declaration ({pr... | plain words |
| P1 | 24. paper/paper.ipynb :: The decision problem | "The several-facet fit, not convex in the terms, has three levels of guarantee and a stopping declaration ({pr... | plain words |
| P1 | 25. paper/paper.ipynb :: Results | "The one-facet fit comes first: the invariant value and its shift (L1, L2), the fit as a convex program (L3 to... | no change |
| P1 | 25. paper/paper.ipynb :: Results | "The several-facet fit is not convex; it has three levels of guarantee (L16, L15, L12 to L14) and, for a soft ... | no change |
| P1 | 25. paper/paper.ipynb :: Results | "The sentences between the boxes say what the next result is for." Term: "boxes". Nothing in the unit says wha... | amend glossary entry |
| P1 | 25. paper/paper.ipynb :: Results | "Whether the hypotheses suit a table is a human judgment ({numref}`Section %s <sect-discussion>`)." Terms: "hy... | amend glossary entry |
| P1 | 25. paper/paper.ipynb :: Results | "The one-facet fit comes first: the invariant value and its shift (L1, L2), the fit as a convex program (L3 to... | glossary term |
| P1 | 25. paper/paper.ipynb :: Results | "The several-facet fit is not convex; it has three levels of guarantee (L16, L15, L12 to L14) and, for a soft ... | glossary term |
| P1 | 25. paper/paper.ipynb :: Results | "Whether the hypotheses suit a table is a human judgment ({numref}`Section %s <sect-discussion>`)." Term: "hyp... | plain words |
| P1 | 25. paper/paper.ipynb :: Results | "The one-facet fit comes first: the invariant value and its shift (L1, L2), the fit as a convex program (L3 to... | no change |
| P1 | 25. paper/paper.ipynb :: Results | "The several-facet fit is not convex; it has three levels of guarantee (L16, L15, L12 to L14) and, for a soft ... | no change |
| P1 | 28. paper/paper.ipynb :: The algorithm for several facets | "Every facet is fitted against every design: the model is $\Phi_K$ ({prf:ref}`thm-extension`), each offset $\b... | amend glossary entry |
| P1 | 28. paper/paper.ipynb :: The algorithm for several facets | "With weights $\alpha_{ik}=\mathrm{softmax}_k(\kappa\,s_{ik})$ from the current model: (i) a convex program sy... | add to avoid |
| P1 | 28. paper/paper.ipynb :: The algorithm for several facets | "**Derived.** *Hypotheses.* A1, A2, A3, A6; I14 (Jensen); I15 (generalized posynomial)." Terms: A1-A8, F12, R2... | add to avoid |
| P1 | 28. paper/paper.ipynb :: The algorithm for several facets | "Refitting a facet on its own rows is ill-posed (observed on planted data, {ref}`Appendix D.13 <sub-d-13>`)." ... | amend glossary entry |
| P1 | 28. paper/paper.ipynb :: The algorithm for several facets | "**Derived.** *Hypotheses.* A8 (a partition into nonempty cells); F12 (the minimum is attained); step B, unpen... | amend glossary entry |
| P1 | 28. paper/paper.ipynb :: The algorithm for several facets | "**Derived.** *Hypotheses.* R2 ($\gamma>0$); F12; I9 (Cauchy-Schwarz)." Term: gamma. The Glossary defines the ... | amend glossary entry |
| P1 | 28. paper/paper.ipynb :: The algorithm for several facets | "On the assignment-stable neighbourhood, with offsets $\beta'_k=J_\tau(Uw'_k)$, $F(W')-F(W)=\sum_k\frac{n_k}{N... | amend glossary entry |
| P1 | 28. paper/paper.ipynb :: The algorithm for several facets | "Soft-fit certificate: at a feasible point of the soft-weight fit where the first-order (KKT) conditions hold,... | no change |
| P1 | 28. paper/paper.ipynb :: The algorithm for several facets | "At K = 3 the margin is 0.00022 to 0.0019 and the stable radius 1.8e-05 to 0.00016, against a band 1/tau of 0.... | amend glossary entry |
| P1 | 28. paper/paper.ipynb :: The algorithm for several facets | "On the primary regime the solver declares the status certified at K = 2 and 3, with the largest facet gap bel... | amend glossary entry |
| P1 | 28. paper/paper.ipynb :: The algorithm for several facets | "The sharp weights give one label per design, $k(i)=\arg\max_ks_{ik}$, $s_{ik}=w_k\cdot u_i-\beta_k$; with $n_... | glossary term |
| P1 | 28. paper/paper.ipynb :: The algorithm for several facets | "Which facet dominates a design is analysis of the fitted model, not part of the fit (steps: {ref}`Appendix B.... | glossary term |
| P1 | 28. paper/paper.ipynb :: The algorithm for several facets | "The package fits with sharp weights at the default term temperature (infinity) and with soft weights at a fin... | glossary term |
| P1 | 28. paper/paper.ipynb :: The algorithm for several facets | "The sharp-weight fit meets three levels of guarantee, none global: descent (L15), numerical stationarity by t... | glossary term |
| P1 | 28. paper/paper.ipynb :: The algorithm for several facets | "**The stopping declaration.** Each returned fit carries the levels it meets ({ref}`Appendix D.8 <sub-d-8>`)."... | glossary term |
| P1 | 28. paper/paper.ipynb :: The algorithm for several facets | "On the primary regime the solver declares the status certified at K = 2 and 3, with the largest facet gap bel... | glossary term |
| P1 | 28. paper/paper.ipynb :: The algorithm for several facets | "Reassignment gives each row the least of its slacks; the refit minimizes a convex $f_k$ of which the previous... | glossary term |
| P1 | 28. paper/paper.ipynb :: The algorithm for several facets | "At K = 3 the margin is 0.00022 to 0.0019 and the stable radius 1.8e-05 to 0.00016, against a band 1/tau of 0.... | glossary term |
| P1 | 28. paper/paper.ipynb :: The algorithm for several facets | "each offset $\beta_k=J_\tau(Uw_k)$ is the support over all rows" Term: supporting envelope. "Support over all... | glossary term |
| P1 | 28. paper/paper.ipynb :: The algorithm for several facets | "Refitting a facet on its own rows is ill-posed (observed on planted data, {ref}`Appendix D.13 <sub-d-13>`)." ... | plain words |
| P1 | 28. paper/paper.ipynb :: The algorithm for several facets | "Cyclic shifts of the terms and Jensen's inequality give (i) and (ii); (iii) is a product of powers of posynom... | plain words |
| P1 | 28. paper/paper.ipynb :: The algorithm for several facets | "On the primary regime the solver declares the status certified at K = 2 and 3, with the largest facet gap bel... | plain words |
| P1 | 28. paper/paper.ipynb :: The algorithm for several facets | "At K = 3 the margin is 0.00022 to 0.0019 and the stable radius 1.8e-05 to 0.00016, against a band 1/tau of 0.... | plain words |
| P1 | 28. paper/paper.ipynb :: The algorithm for several facets | "One accepted iteration does not raise the mean slack $F$: reassigning each row to its maximizing facet lowers... | plain words |
| P1 | 28. paper/paper.ipynb :: The algorithm for several facets | "Soft-fit certificate: at a feasible point of the soft-weight fit where the first-order (KKT) conditions hold,... | plain words |
| P1 | 28. paper/paper.ipynb :: The algorithm for several facets | "The package fits with sharp weights at the default term temperature (infinity) and with soft weights at a fin... | no change |
| P1 | 28. paper/paper.ipynb :: The algorithm for several facets | "The sharp-weight fit meets three levels of guarantee, none global: descent (L15), numerical stationarity by t... | no change |
| P1 | 28. paper/paper.ipynb :: The algorithm for several facets | "At K = 3 the margin is 0.00022 to 0.0019 and the stable radius 1.8e-05 to 0.00016, against a band 1/tau of 0.... | no change |
| P1 | 28. paper/paper.ipynb :: The algorithm for several facets | "Soft-fit certificate: at a feasible point of the soft-weight fit where the first-order (KKT) conditions hold,... | no change |
| P1 | 28. paper/paper.ipynb :: The algorithm for several facets | "If every facet score changes by at most $\delta$ with $2\delta<\gamma$, each row's maximizing facet is unchan... | no change |
| P1 | 28. paper/paper.ipynb :: The algorithm for several facets | "With $g=\nabla f_k(w)$, the facet gap is $G_k(w)=g\cdot w-\min_jg_j=\sum_jw_j(g_j-\min_lg_l)\ge0$, and $0\le ... | no change |
| P1 | 28. paper/paper.ipynb :: The algorithm for several facets | "For a soft fit, certified means that the second-order test holds ({prf:ref}`thm-certificate`), and stationary... | no change |
| P1 | 28. paper/paper.ipynb :: The algorithm for several facets | "**Derived.** *Hypotheses.* A8 (a partition into nonempty cells); F12 (the minimum is attained); step B, unpen... | no change |
| P1 | 30. paper/paper.ipynb :: Prior art, by family | "Our boundary is a soft maximum with a temperature, a band and an effective sample size, not a boundary set by... | no change |
| P1 | 30. paper/paper.ipynb :: Prior art, by family | "Our boundary is a soft maximum with a temperature, a band and an effective sample size, not a boundary set by... | no change |
| P1 | 30. paper/paper.ipynb :: Prior art, by family | "Our boundary is a soft maximum with a temperature, a band and an effective sample size, not a boundary set by... | no change |
| P1 | 30. paper/paper.ipynb :: Prior art, by family | "The model class and refit scheme come from geometric programming and max-affine fitting [@boyd2007tutorial; @... | no change |
| P1 | 30. paper/paper.ipynb :: Prior art, by family | Table cell "A smooth soft maximum over a simplex-constrained geometric mean". Terms: soft maximum, simplex, ge... | no change |
| P1 | 32. paper/paper.ipynb :: Search of the design space (preliminary) | "Outward monotonicity is stated for the exact maximum and not for the soft one; neither has a lemma here." Ter... | no change |
| P1 | 36. paper/paper.ipynb :: Open questions | "Q3: identifiability of the active metrics under finite, biased observations." Terms: active metrics, identifi... | amend glossary entry |
| P1 | 36. paper/paper.ipynb :: Open questions | "Four questions are not established ({ref}`Appendix E <appendix-e>` records them as gaps G-14, G-11, G-12 and ... | amend glossary entry |
| P1 | 36. paper/paper.ipynb :: Open questions | "Q1: global convergence of the alternation, not pursued." Terms: the alternation. The Glossary does not define... | amend glossary entry |
| P1 | 36. paper/paper.ipynb :: Open questions | "Q2: statistical consistency under noise and refitting." Terms: refitting. The Glossary has no entry for it. I... | amend glossary entry |
| P1 | 36. paper/paper.ipynb :: Open questions | "Q4: conditions under which the fitted surface recovers the Pareto boundary and not the sample's envelope." Te... | glossary term |
| P1 | 36. paper/paper.ipynb :: Open questions | "Q3: identifiability of the active metrics under finite, biased observations." Term: contending set. "Active m... | glossary term |
| P1 | 36. paper/paper.ipynb :: Open questions | "Q3: identifiability of the active metrics under finite, biased observations." Terms: number of designs, fit t... | glossary term |
| P1 | 36. paper/paper.ipynb :: Open questions | "Q1: global convergence of the alternation, not pursued." Plain words: "whether the back-and-forth fitting ste... | plain words |
| P1 | 36. paper/paper.ipynb :: Open questions | "Q2: statistical consistency under noise and refitting." Plain words: "whether the estimates settle on the tru... | plain words |
| P1 | 36. paper/paper.ipynb :: Open questions | "Q3: identifiability of the active metrics under finite, biased observations." Plain words: "whether the data ... | plain words |
| P1 | 36. paper/paper.ipynb :: Open questions | "Q4: conditions under which the fitted surface recovers the Pareto boundary and not the sample's envelope." Te... | no change |
| P1 | 36. paper/paper.ipynb :: Open questions | "Q3: identifiability of the active metrics under finite, biased observations." Terms: identifiability, active ... | no change |
| P1 | 36. paper/paper.ipynb :: Open questions | "Q2: statistical consistency under noise and refitting." Terms: statistical consistency, noise, refitting.... | no change |

## To the driver (readers' reports of a clash touching a term's meaning)

- Unit 1, docs/api.md: "Fitted attributes for every number of terms include `exponents_`, `facet_`, `coefficients_`, `facet_share_`, `objective...
- Unit 2, paper/supporting_material.ipynb :: Appendix A. Notation and terms: "the older use of the phrase for signomial programs" -- plain words: an older, different meaning of the phrase....
- Unit 4, paper/paper.ipynb :: Definitions: "The facet share is the fraction of near-frontier designs that facet $k$ dominates; it shows which facets carry most of ...
- Unit 7, paper/paper.ipynb :: Methods: "A negative $\alpha_j$ marks smaller-is-better; the shift $s_j$ places the origin; a scaler equalizes log-spread so one ...
- Unit 17, paper/paper.ipynb :: Preliminaries and notation: "The Pareto boundary is the nondominated set of the attainable set, a property of the system." Term: Pareto boundary. Th...
- Unit 22, paper/paper.ipynb :: Case analysis: "Of 3 proposals, the predicted energy differential lies within the regressor's own band 1/tau = 0.0651 of the measured o...
- Unit 28, paper/paper.ipynb :: The algorithm for several facets: "**Derived.** *Hypotheses.* A8 (a partition into nonempty cells); F12 (the minimum is attained); step B, unpenalized, wi...
- Unit 39, paper/supporting_material.ipynb :: Appendix B. Proofs, step for step with their scripts (part 7): "A8: F(W) = (1/N) sum\_k n\_k f\_k(w\_k) = sum\_k share\_k f\_k(w\_k) with share\_k = n\_k / N" Term: share. The Glossar...

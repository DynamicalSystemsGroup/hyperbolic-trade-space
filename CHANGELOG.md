# Changelog

All notable changes to this project are recorded here, in the format of
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/). The project follows
[Semantic Versioning](https://semver.org/). Entries are drawn from the work-package records in
`work-packages/` and the git history; the package that made each change is named in parentheses.

## [Unreleased] - target 0.1.0

Not yet released: no tag, no publication. The version in `pyproject.toml` is set by the release
package.

### Added

- The package `hyperbolic_trade_space` (alias `hts`): the posynomial invariant form for a trade
  space, with the scikit-learn estimator `HyperbolicTradeSpace` (fit, `transform`,
  `inverse_transform`, `score_samples`), the frontier chart (Helmert and additive-log-ratio
  coordinates) and the entropic (log-mean-exp) soft maximum (WP2).
- The K = 1 (monomial) fit with its solvers, and tests under scikit-learn's estimator checks (WP2).
- The several-term (K > 1) posynomial fit with sharp term assignment, a mean-slack objective and
  a sparsity option (WP9), and the fit with soft weights (WP17).
- Certificates and a stopping declaration printed by a fit (WP13).
- Conditioning and analysis tools: `LogAffinePreconditioner`, `frontier_in_original_units`,
  `select_temperature`, `TradeSpaceRegressor`, hole and target finding (`find_holes`,
  `frontier_targets`, `knn_gap_scores`) (WP3).
- `tension_report`: the tensions that define the trade-offs, with elasticities (WP3, WP13).
- Plotting: the log plane, the 3-D frontier surface, frontier coordinates, tensions, and ternary
  plots documented in the examples (WP3, WP18).
- The derivation ledger: plain-SymPy lemma scripts L1 to L17 in `derivation/`, an axioms ledger, a
  proof-map checker and its committed record (WP1, WP9, WP13, WP17).
- The documentation site (MkDocs): getting started, user guide, theory, API reference generated
  from docstrings, generated glossary and derivation pages, further reading and a bibliography
  with resolved references (WP5, WP6, WP8a).
- A root page and one-command local staging of the site (WP8a, WP14).
- Stable reference keys from the docsite into the paper: `[text](paper:key)` names a label the paper
  defines, the docs build turns it into a link to the paper page and anchor and fails on an undefined
  key; the paper's article theme is pinned so a clean checkout builds the paper (WP8b).
- A user-guide page, "Choosing K": the checks that bear on the number of terms, what each can and cannot say,
  a temperature recipe with `select_temperature`, and worked examples on planted tables and the cubesat (WP31).
- The interface contract between the technical and presentation sides, with its manifest
  (WP14).
- The case study (a SysML-modelled illustrative cubesat attitude-control design space): the
  simulation port, design space, seeded dataset, the SysML v2 model with an experiment ledger,
  and the experiments module (WP4, WP4b, WP15).
- The paper as an executed notebook (mystmd), with a supporting-material notebook of
  computationally verifiable appendices and a container definition (`Dockerfile`) for the
  environment of record (WP10).
- The estimator keyword `term_aggregation` (`"sum"` default, `"mean"`), the count `n_distinct_terms`
  on the termination record, and the bound stated for both aggregations (WP21).
- The case model in two views, configuration and assessment, in one SysML v2 model: requirements,
  verification cases and a trace from configuration variables to assessed attributes to the traded
  metrics (WP22); the model-realism loop that added total mass with launch cost as its measure of
  effectiveness, so every design choice reaches at least one metric (WP23).
- The case model read in the OpenMBEE view editor, with a harness note for loading and reading it
  there (WP26), and a stakeholder layer: two stakeholders, one tied to price and one to
  performance in the operational life, their concerns traced to the requirements and the
  metrics (WP27).
- Figures chosen by section, each with the purpose it serves and what it does not show (WP19).
- Developer tooling for verification in tiers: a fast test suite, a path-to-tests map
  (`scripts/check.py`), parallel workers and a sharded Linux run (WP20).
- `LICENSE` (MIT, copyright 2026 Dynamical Systems Group) and this changelog.

### Changed

- The case study moves onto the model of record: the nine-attribute datasets, the settling time by
  event detection, and the K = 1, 2, 3 record and the paper's numbers regenerated on them inside
  the container of record; every moved number is listed with its cause in
  `work-packages/swap-evidence.md`, and the earlier data stays as the cited comparison (WP16,
  WP23).
- The word "facet" is gone from every surface, including the package's public names: the model's
  objects are monomial terms (term assignment, distinct terms, per-term shares), the paper, the
  docs, the glossary, the derivations and the interface contract follow (WP24).
- Improvement by subtraction: one pass over the paper and the docs removed figures, arguments and
  paragraphs that did not advance the narrative, each deletion recorded with what it no longer
  did (WP28); repository tidiness passes removed unused files and closed drift between the docs,
  the glossary and the code (WP25).
- The response to the independent assessment: the paper and docs keep three claims apart
  (certificate, observed geometry, usefulness outside the observations) (WP21).
- The fit's formal statements made exact in the derivations and the ledger, following the
  response to the external review (WP13).

### Notes

- Not part of 0.1.0: the trade-off-aware search (WP12, after 0.1); publishing to PyPI or an
  image registry; the PDF export.

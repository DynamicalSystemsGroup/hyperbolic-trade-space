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
- The several-term (K > 1) posynomial fit with sharp facet assignment, a mean-slack objective and
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
- The interface contract between the technical and presentation sides, with its manifest
  (WP14).
- The case study (a SysML-modelled illustrative cubesat attitude-control design space): the
  simulation port, design space, seeded dataset, the SysML v2 model with an experiment ledger,
  and the experiments module (WP4, WP4b, WP15, WP16).
- The paper as an executed notebook (mystmd), with a supporting-material notebook of
  computationally verifiable appendices and a container definition (`Dockerfile`) for the
  environment of record (WP10).
- `LICENSE` (MIT, copyright 2026 Dynamical Systems Group) and this changelog.

### Changed

- The case and its records moved to the new data generation, with the frozen data kept as the
  cited comparison (WP16).
- The fit's formal statements made exact in the derivations and the ledger, following the
  response to the external review (WP13).

### Notes

- Not part of 0.1.0: the trade-off-aware search (WP12, after 0.1); publishing to PyPI or an
  image registry; the PDF export.

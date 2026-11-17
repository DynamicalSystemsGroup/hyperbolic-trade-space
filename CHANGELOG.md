# Changelog

All notable changes to this project are recorded here, in the format of
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/). The project follows
[Semantic Versioning](https://semver.org/). Entries are drawn from the work-package index
(`work-packages/INDEX.md`) and the git history; the package that made each change is named in parentheses.

## [Unreleased]

### Removed

- The `main-review` bypass carried for the 0.1 release (one user, `mzargham`, on pull requests): removed from the
  governance declaration (`.github/governance.toml`) by this change and from the ruleset by a code owner after its
  merge, attested by a code owner's local run of `scripts/check_repo_settings.py`; the 0.2 release is the first
  merged under the review rule without it (`GOVERNANCE.md`).

### Changed

- The default workflow permissions are read and a workflow may not approve a pull request (the design's value; live
  was write through 0.1), and `controls`, the settings check, is a required status check on `main` beside the three
  shards and `admissibility`; both declared in `.github/governance.toml` and set on GitHub after the merge (WP82).
- The governed files (the secondary rules of `GOVERNANCE.md`) are under a declared control: a `CODEOWNERS` line per
  file naming the three code owners as the approvers of a change to it, and the `governance-files` push ruleset,
  which refuses a push touching one of them by anyone but a Repository admin (WP82).
- The admissibility documents: rows for a bug report and a question, the `controls` job in the pull request's
  conformance row, and each judged row naming its guideline (WP82).

## [0.1.0] - 2026-11-17

### Added

- Two release lifecycles. The software (the package, the docs and the root page) is released by the merge of a
  pull request from `dev` into `main`: the release workflow checks admissibility, runs the suite, builds, creates
  the tag `v<version>`, publishes to PyPI by trusted publishing, deploys the site and publishes the GitHub release;
  a failure is named in the run, cleaned up by `scripts/release_cleanup.py` and reported in an issue; a merge
  without a new version redeploys the site only. The paper has its own branch (`paper`), tags (`paper-*`, published
  as GitHub releases on a code owner's approval) and change record (`paper/CHANGES.md`); its tests run in its own
  workflow and leave the software's suite. `/paper/` serves the mode named in `paper/mode.toml`, which is
  `abstract` (the title, the author and the abstract) (WP65, WP66).
- Release engineering and governance: the release workflow with trusted publishing, a software bill of materials
  and the version and changelog gates; five enforcement workflows; `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`,
  `SECURITY.md`, code owners, and issue and pull-request templates with their admissibility conditions (WP47).
- Lint and the Linux fast shard run on every push to `dev`; the full matrix runs on the release pull request and
  when the release workflow calls it (WP67).
- Governance as executable: the repository's settings (rulesets, environments, Pages, the code owners' access, the
  workflow permissions) declared in `.github/governance.toml`, checked against the live repository by
  `scripts/check_repo_settings.py` in a `controls` job that runs first in the Tests and Release workflows, and
  attested in each release's notes; `GOVERNANCE.md` states the release rules, the two reviews and the repository's
  secondary rules (WP78).
- The paper's own contribution route: a `/paper/` line in `.github/CODEOWNERS` names the paper's approvers apart from
  the code owners, a pull request into `paper` is merged by an approver who is not its author, the pull request
  template has a paper section, and "Contributing to the paper" in `CONTRIBUTING.md` and "The paper's route" in
  `GOVERNANCE.md` say how the paper is edited, approved, published and reaches the site (WP79).
- Public-link metadata on every page of the site: a description, a canonical address, Open Graph and Twitter card
  fields with a preview image, structured data for the software and the site, `robots.txt` and a sitemap, from
  one source of values (WP80).
- Windows as a third platform for the fast and slow test shards, run on dispatch and at gates; the paper's tests
  run in the paper's workflow (WP34).
- The package `tradespace` (alias `hts`): the posynomial invariant form for a trade
  space, with the scikit-learn estimator `HyperbolicTradeSpace` (fit, `transform`,
  `inverse_transform`, `score_samples`), the frontier chart (Helmert and additive-log-ratio
  coordinates) and the entropic (log-mean-exp) soft maximum (WP2).
- The K = 1 (monomial) fit with its solvers, and tests under scikit-learn's estimator checks (WP2).
- The several-term (K > 1) posynomial fit with sharp term assignment, a mean-slack objective and
  a sparsity option (WP9), and the fit with soft weights (WP17).
- Certificates and a stopping declaration printed by a fit (WP13).
- Conditioning and analysis tools: `LogAffinePreconditioner`, `frontier_in_original_units`,
  `select_temperature`, `TradeSpaceRegressor`, holes and frontier targets (`find_holes`,
  `frontier_targets`, `knn_gap_scores`) (WP3).
- `trade_off_report`: the tensions that define the trade-offs, with elasticities (WP3, WP13; named
  `tension_report` until WP42).
- The fit temperature as a path: `temperature_path` and `plot_temperature_path`, the user-guide page "The fit
  temperature", and the small-temperature lemma L22 (WP46).
- Plotting: the log plane, the 3-D frontier surface, frontier coordinates, tensions, and ternary
  plots documented in the examples (WP3, WP18).
- The derivation ledger: plain-SymPy lemma scripts L1 to L22 in `derivation/`, an axioms ledger, a
  proof-map checker and its committed record (WP1, WP9, WP13, WP17, WP29, WP42, WP46).
- The noise result: lemma scripts L18 to L20 (the noise covariance under the conditioning map, the shift bound,
  noise as a ridge on the exponents) with planted-data tests (WP29).
- The documentation site (MkDocs): getting started, user guide, theory, API reference generated
  from docstrings, generated glossary and derivation pages, further reading and a bibliography
  with resolved references (WP5, WP6, WP8a).
- A root page and one-command local staging of the site (WP8a, WP14); the root page recast as why, what and
  how, with the three-metric triangle shaded by the trade-off that binds there and the pairwise slices, both
  generated at build time from a planted table (WP51).
- A history and acknowledgements page on the root site, its dated reference list rendered from `history.yaml`
  at build time (WP37), with the governance lineage on it (WP52).
- Journeys and signposting: the docs home leads with the five need links, the user guide has a router page, the
  README carries the package-only install line and the paper link, and the package docstring names the docs
  site (WP33).
- User-guide pages checked by package-user tests: four tasks run from the docs as written, with their fixtures
  (a plain CSV, a pump SysML v2 model, an export script and its exported table) under `tests/fixtures/user-tests/`
  (WP32).
- The bridge page, from the chart back to a design (WP41); a user-guide page on the routes back from a
  tension (WP42).
- Two sentences on the limitations page: a proof in a theorem prover would fix each lemma's statement over the
  reals and would not bound the double-precision error, which the certificates check (WP36).
- Three public case studies, perovskite solar cells, amniote life histories and Broadbalk wheat, each fetched
  with a hash check, conditioned, fitted and read (WP45), with their conditioning ladders and chains (WP59);
  their example pages (WP60), redrafted to one template with an arc (WP63); the wheat page's level V against
  biomass (WP71).
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

- The package is named `tradespace` (import name `tradespace`, distribution name `tradespace`); it was
  `hyperbolic-trade-space` during development and was never released under that name (WP77).
- The case study moves onto the model of record: the nine-attribute datasets, the settling time by
  event detection, and the K = 1, 2, 3 record and the paper's numbers regenerated on them inside
  the container of record; every moved number is listed with its cause in
  [`work-packages/swap-evidence.md`](https://github.com/DynamicalSystemsGroup/tradespace/blob/4f81a4ea3649ff844cff2acdf9d447285cbb0fc5/work-packages/swap-evidence.md), and the earlier data stays as the cited comparison (WP16,
  WP23).
- The word "facet" is gone from every surface, including the package's public names: the model's
  objects are monomial terms (term assignment, distinct terms, per-term shares), the paper, the
  docs, the glossary, the derivations and the interface contract follow (WP24).
- The tension matrix and the elasticity vocabulary across the package and the docs: `tension_report` becomes
  `trade_off_report`, with `tension_matrix` and `design_tensions` beside it (WP42).
- The case study revised: momentum headroom as the ninth traded metric, the fleet-size variable and the cost
  model; the datasets regenerated at 3,000 designs per regime and the cost ladders written from them (WP30).
- The residual pass: patterns that read as machine-written removed from the docs, the glossary and the example
  pages, with a checker and its baseline (`scripts/check_residuals.py`) (WP38).
- Improvement by subtraction: one pass over the paper and the docs removed figures, arguments and
  paragraphs that did not advance the narrative, each deletion recorded with what it no longer
  did (WP28); repository tidiness passes removed unused files and closed drift between the docs,
  the glossary and the code (WP25); release thinning and the repository's organization (WP40); live guidance
  moved to `notes/` and `docs/superpowers` retired (WP62); the process record left the tree before 0.1, each
  document indexed with the hash it is read at (WP73).
- The response to the independent assessment: the paper and docs keep three claims apart
  (certificate, observed geometry, usefulness outside the observations) (WP21).
- The fit's formal statements made exact in the derivations and the ledger, following the
  response to the external review (WP13).

### Fixed

- The case model's views generator accepts a requirement usage under either type name,
  `SatisfyRequirementUsage` or `VerifyRequirementUsage` (the external review's finding 7) (WP74).

### Notes

- Not part of 0.1.0: the trade-off-aware search (WP12, after 0.1); an image on a registry; the
  PDF export.

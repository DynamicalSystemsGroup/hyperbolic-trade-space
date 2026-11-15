# Sitting 3: the code, the derivations and the release engineering

Entry point: files, no page. Package `src/hyperbolic_trade_space/`; derivations `derivation/` (start at
`derivation/PROOF_MAP_FINDINGS.md`); case study `examples/adcs/` (start at `examples/adcs/case-model.md`); release
engineering `.github/`, `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, `SECURITY.md`, `docs/code-owners.md`. Commands are
`uv run ...`.

- [ ] Run `uv run pytest -q` (doctests included), `uv run ruff check .`, `uv run ruff format --check .` and
  `uv lock --check` on your machine at `415d889`. Compare with the counts recorded by branch in
  `work-packages/driver-log.md` (the WP42 build's merged tree: 1,992 passed; the fan figure's branch: 2,038 passed;
  wp46's merged tree before its last rebase: 2,063 passed fast; the full run at 415d889 under "Final head") and
  with release checklist row B1 (`work-packages/WP8b-release-checklist.md`).
- [ ] Run `uv run python -m derivation.proofmap`. It reports the lemma chain and its tagged steps; the chain now holds
  Lemma 21 (tension) and Lemma 22 (the small-temperature step, WP46): 22 lemmas. Count against
  `derivation/proof_map_record.json`.
- [ ] Pick one lemma script (for example `derivation/lemma_01_homogeneity.py`, then `derivation/lemma_21_tension.py`)
  and read it as pencil-and-paper work. These scripts are business-casual checks, not a formal proof
  (`docs/superpowers/notes/proof-conventions.md`).
- [ ] Read the public estimator's docstring and the first call in `README.md`; does it run as shown? Then the renamed
  names of your ruling (`trade_off_report`, `spread_directions`, `spread_loadings`, `plot_association`, and the new
  `tension_matrix` and `design_tensions`) against `work-packages/WP42-decisions.md`, "Naming item 2".
- [ ] Skim the scikit-learn conformance note (`docs/superpowers/notes/sklearn-conformance.md`) against the estimator:
  `fit`, `transform`, `inverse_transform`, `score_samples`; no `predict` on the transformer.
- [ ] The claims register `claims_register.toml`: run `uv run pytest -q tests/test_claims_register.py`; every claim a
  reader can rely on has a backing (`docs/superpowers/notes/claims-review.md`).
- [ ] `uv run python scripts/check_vocabulary.py` against `glossary.yaml` (the glossary now has layers and the
  avoided words "hole" and "gap" for the chart's unoccupied region), and
  `uv run python scripts/check_residuals.py --compare scripts/residuals_baseline.json --strict`, which should exit 0.
- [ ] The release workflows in `.github/workflows/` (release, test, pages and the five admissibility checks), each
  action pinned to a commit. They are written and tested on payloads but have not run on GitHub; the cases are in
  `work-packages/WP47-rounds/checks.md` (eight verification cases). Review against your amendments in
  `work-packages/WP47-decisions.md` (the cheap checks in 0.1; the software bill of materials in 0.1).
- [ ] `CONTRIBUTING.md`, the three admissibility files in `.github/`, `CODE_OF_CONDUCT.md` (the Contributor Covenant
  3.0, unaltered) and `docs/code-owners.md`. Review against the texts you signed off in
  `work-packages/WP49-decisions.md` ("Sign-off"); only the link to the code owners' page differs, as you ruled.
- [ ] The case study's model file `examples/adcs/cubesat_tradespace.sysml` and the data in `examples/adcs/data`; the
  three test records of WP45 in `examples/perovskite`, `examples/amniote` and `examples/wheat`, each with its expected
  n-lemma written before its fit (`work-packages/WP45-rounds/*/test-record.md`). The cubesat model is a numerical
  demonstrator, not the project's subject; the three records are documentation inputs for the next release, not docs
  pages yet.

Evidence: `work-packages/WP24-review.md`, `work-packages/WP29-review.md`, `work-packages/WP32-review.md`,
`work-packages/WP42-rounds/build-record/`, `work-packages/WP47-rounds/checks.md`, `paper/container/RECORD.md`.

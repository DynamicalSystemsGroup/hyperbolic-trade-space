# Sitting 3: the code and the derivations

Entry point: files, no page. Package `src/hyperbolic_trade_space/`; derivations `derivation/` (start at
`derivation/PROOF_MAP_FINDINGS.md`); case study `examples/adcs/` (start at `examples/adcs/case-model.md`). The
generated lemma pages are also in the paper's Appendix B (sitting 1). Commands are `uv run ...`; this draft ran none
of the full-suite commands.

- [ ] Run `uv run pytest -q` (doctests included) on your machine; the record of the last Mac fast suite is in
  `work-packages/driver-log.md` ("Verification snapshots by the driver"); a re-run at the release head is open
  (`work-packages/WP8b-release-checklist.md`, B1).
- [ ] Run `uv run ruff check .` and `uv run ruff format --check .`; `uv lock --check`.
- [ ] Run `uv run python -m derivation.proofmap`; it reports the lemma chain and the tagged proof steps (the grid
  records 20 lemma files and 505 tagged steps).
- [ ] Read the public estimator's docstring and the first call in `README.md`; does the first call run as shown?
- [ ] Skim the scikit-learn conformance note (`docs/superpowers/notes/sklearn-conformance.md`) against the estimator:
  `fit`, `transform`, `inverse_transform`, `score_samples`; no `predict` on the transformer.
- [ ] Pick one lemma script (for example `derivation/lemma_01_homogeneity.py`) and read it as pencil-and-paper work.
  These scripts are business-casual checks, not a formal proof (`docs/superpowers/notes/proof-conventions.md`).
- [ ] Open the claims register `claims_register.toml`; run `uv run pytest -q tests/test_claims_register.py`.
- [ ] Run `uv run python scripts/check_vocabulary.py`; the vocabulary source is `glossary.yaml`.
- [ ] Run the residual checker `uv run python scripts/check_residuals.py --compare scripts/residuals_baseline.json --strict`
  (the committed baseline; see `verified.md`); it should exit 0.
- [ ] Look at the case study's model file `examples/adcs/cubesat_tradespace.sysml` and the data in
  `examples/adcs/data`. The cubesat model is a numerical demonstrator, not the project's subject.

Evidence: `work-packages/WP24-review.md`, `work-packages/WP29-review.md`, `work-packages/WP32-review.md`,
`paper/container/RECORD.md`.

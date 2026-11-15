# WP62 inventory (D-1)

The classification of what the repository holds, by the supervisor's rule of 2026-11-15 (`WP61-decisions.md`): the tree holds the delivered content and what builds and checks it, the live guidance, the boundary content on the future directions, and the live packages; everything else is historical and leaves at one commit, read back by hash from `INDEX.md`. Class is by the rule, not by age. Readers come from `git grep` of each path over the whole tree (code, tests, workflows, the docsite, `CLAUDE.md`, the register's backing fields, the notebooks, and the live packages' documents); a reader inside another landed package's document does not hold a path in place, and a citation in a note that moves or leaves is re-pointed to the new path or to the hash. The two notebooks are never edited, so a path a notebook names stays until that notebook's package re-executes it.

Nothing has moved. This file is committed alone; the moves wait for the driver's approval line in `WP62-decisions.md`.

## Decisions this inventory makes that go beyond the scope's lists

1. `notation.md` and `abstraction-gaps.md` are on the scope's move list but the supporting-material notebook links both; by the scope's own rule they stay under `docs/superpowers/notes/` until that notebook's package re-executes it. `scripts/build_generated.py` and `paper/generate_repro.py` read `abstraction-gaps.md` and need no edit then.
2. `paper-sources/` (the six snapshots of pages that left the docsite) is guarded by `tests/test_paper_sources.py` and `tests/test_narrative.py`, and the notebook links `literature.md`; leaving the tree would change those tests' logic, which the scope forbids. It stays whole and retires with those two tests in the notebook's package.
3. `references-verified.md` and `paper-prior-art-sources.md` are ledgers read by the register, `PROOF_MAP_FINDINGS.md`, `paper/prior_art.yaml` and `tests/test_references.py`; they move to `notes/` rather than leave.
4. `figure-candidates/` (the triple search and its record) is read by the register (`gen:` and `file:` backings) and `tests/test_paper.py`; it moves to `paper/figures/`.
5. `bench_oracle.py` is read by the notebook, not by a test (no test imports it); it stays with `methods.py` (which it imports) and the spike's README. `project.py` and `render.sh` are read by three tests and `scripts/check.py`; they move to `scripts/` (`sysml_project.py`, `sysml_render.sh`), the tests' paths updated, no logic changed.
6. `kernel-direction.md` is listed to leave; the WP43 readout, which keeps the content, is boundary content and is copied to `notes/directions/`.
7. The ternary spike's readout is not on `dev` (it is `work-packages/WP56-rounds/ternary/readout.md` at `cf4faca` on branch `wp56-ternary`); the directions folder takes it when WP56 lands, and the index lists it as pending. The WP52 readout is `WP52-rounds/spike/proposal.md` (no file of that package is named readout). Not on the scope's list and so not brought back: the WP35, WP36 wave notes beyond the readout, WP39, WP40, WP44 and WP49 readouts; the driver may add any.
8. Landed-package files that code, tests, the register, the paper's ledgers or a workflow read stay where they are (the column says which reader holds each); files whose only readers are notes, the log or other historical documents leave.


## Top-level paths

| path | class | readers | disposition |
|---|---|---|---|
| `.dockerignore` | builds or checks it | Dockerfile; tests/test_container.py | stays |
| `.gitattributes` | builds or checks it | README.md; tests/test_line_endings.py | stays |
| `.github/` | builds or checks it | the workflows (CI); CLAUDE.md | stays |
| `.gitignore` | builds or checks it | README.md; tests/test_interface_contract.py; tests/test_paper.py; work-packages/WP25-3-scope-of-work.md; work-packages/WP25-4-scope-of-work.md; work-packages/WP25-review.md; work-packages/WP59-review.md; work-packages/driver-log.md; work-packages/interface-contract.md; work-packages/interface-contract.toml | stays |
| `.python-version` | builds or checks it | .github/workflows/test.yml; CLAUDE.md; CONTRIBUTING.md; README.md; docs/superpowers/specs/2026-11-07-posynomial-invariant-form-design.md; paper/generate_repro.py; supporting_material.ipynb (notebook); tests/test_contributing_links.py; tests/test_interface_contract.py; tests/test_paper.py; work-packages/WP25-2-scope-of-work.m ... | stays |
| `CHANGELOG.md` | delivered content | README.md; docs/code-owners.md; pyproject.toml; scripts/release_checks.py; tests/test_release_checks.py; work-packages/WP25-2-scope-of-work.md; work-packages/WP25-3-scope-of-work.md; work-packages/WP8b-decisions.md; work-packages/WP8b-release-checklist.md; work-packages/WP8b-review.md; work-packages/WP8b-reviewers-guide-skel ... | stays |
| `CLAUDE.md` | live guidance | README.md; docs/superpowers/specs/2026-11-07-posynomial-invariant-form-design.md; scripts/check_residuals.py; tests/test_vocabulary.py; work-packages/PM-BRIEF.md; work-packages/README.md; work-packages/WP25-3-scope-of-work.md; work-packages/WP25-4-scope-of-work.md; work-packages/WP25-decisions.md; work-packages/WP25-review.m ... | stays |
| `CODE_OF_CONDUCT.md` | delivered content | CONTRIBUTING.md; tests/test_contributing_links.py | stays |
| `CONTRIBUTING.md` | delivered content | .github/PR_ADMISSIBILITY.md; SECURITY.md; docs/code-owners.md; tests/test_contributing_links.py; work-packages/driver-log.md | stays |
| `Dockerfile` | builds or checks it | CHANGELOG.md; README.md; paper/container/README.md; paper/container/build.sh; supporting_material.ipynb (notebook); scripts/check.py; tests/test_check_script.py; tests/test_container.py; work-packages/WP25-2-scope-of-work.md; work-packages/WP25-3-scope-of-work.md; work-packages/driver-log.md | stays |
| `LICENSE` | delivered content | .github/workflows/release.yml; CHANGELOG.md; README.md; examples/adcs/adcs_sim.py; pyproject.toml; work-packages/WP25-2-scope-of-work.md; work-packages/WP25-3-scope-of-work.md; work-packages/WP8b-decisions.md; work-packages/WP8b-release-checklist.md; work-packages/WP8b-review.md; work-packages/WP8b-scope-of-work.md; work-pac ... | stays |
| `README.md` | delivered content | CLAUDE.md; Dockerfile; register backing; docs/superpowers/notes/abstraction-gaps.md; docs/superpowers/notes/residual-review.md; docs/superpowers/notes/spike-horopca/grep_table.py; docs/superpowers/notes/spike-horopca/test_spike_results.py; docs/superpowers/notes/user-journeys.md; docs/superpowers/notes/vocabulary-review.md;  ... | stays |
| `SECURITY.md` | delivered content | CONTRIBUTING.md; tests/test_contributing_links.py | stays |
| `claims_register.toml` | delivered content | README.md; docs/code-owners.md; docs/superpowers/notes/claims-review.md; docs/superpowers/notes/spike-horopca/grep_table.py; paper/container/RECORD.md; tests/test_claims_register.py; tests/test_site.py; work-packages/PM-BRIEF.md; work-packages/WP25-2-scope-of-work.md; work-packages/WP25-3-scope-of-work.md; work-packages/WP25 ... | stays (backing fields re-pointed) |
| `derivation/` | delivered content | tests/test_derivation.py; the register; the paper | stays |
| `docs/` | delivered content | mkdocs.yml; tests/test_docs.py; tests/test_site.py | stays, minus docs/superpowers/ |
| `examples/` | delivered content | tests; the paper (notebooks); the docsite | stays |
| `glossary.yaml` | delivered content | CLAUDE.md; README.md; register backing; docs/superpowers/notes/residual-review.md; docs/superpowers/notes/spike-horopca/grep_table.py; docs/superpowers/notes/vocabulary-review.md; mkdocs.yml; paper/container/RECORD.md; paper/generate_register.py; paper/generate_repro.py; supporting_material.ipynb (notebook); scripts/build_ge ... | stays |
| `history.yaml` | delivered content | README.md; register backing; docs/code-owners.md; scripts/assemble_site.py; scripts/check_history_links.py; scripts/history_record.py; tests/test_site.py; work-packages/PM-BRIEF.md; work-packages/driver-log.md | stays |
| `mkdocs.yml` | builds or checks it | README.md; docs/superpowers/notes/spike-horopca/grep_table.py; docs/superpowers/notes/user-journeys.md; scripts/assemble_site.py; scripts/check.py; scripts/paper_keys.py; tests/test_site.py; work-packages/WP25-2-scope-of-work.md; work-packages/WP25-3-scope-of-work.md; work-packages/WP25-decisions.md; work-packages/WP25-scope ... | stays (superpowers exclude replaced) |
| `paper/` | delivered content | scripts/assemble_site.py; tests/test_paper.py; the notebooks (own) | stays |
| `pyproject.toml` | builds or checks it | .github/RELEASE_ADMISSIBILITY.md; CHANGELOG.md; CONTRIBUTING.md; README.md; docs/code-owners.md; docs/ruff.toml; docs/superpowers/notes/spike-horopca/README.md; docs/superpowers/notes/verification-strategy.md; examples/adcs/experiments/__main__.py; paper/generate_repro.py; supporting_material.ipynb (notebook); scripts/check. ... | stays (ruff extend-exclude updated) |
| `scripts/` | builds or checks it | CI; tests/test_check_script.py | stays |
| `site/` | delivered content | scripts/assemble_site.py; tests/test_site.py | stays |
| `src/` | delivered content | every test; the docsite; the paper | stays |
| `tests/` | builds or checks it | CI (.github/workflows/test.yml) | stays |
| `uv.lock` | builds or checks it | .github/RELEASE_ADMISSIBILITY.md; .github/workflows/pages.yml; .github/workflows/release.yml; .github/workflows/test.yml; CLAUDE.md; CONTRIBUTING.md; Dockerfile; README.md; docs/code-owners.md; docs/superpowers/notes/spike-horopca/README.md; docs/superpowers/specs/2026-11-07-posynomial-invariant-form-design.md; paper/contain ... | stays |
| `work-packages/` | live package | CLAUDE.md; tests/test_interface_contract.py; the register; paper generators; INDEX.md | stays, thinned (second table) |
| `notes/ (new)` | live guidance | CLAUDE.md; tests; scripts; the register (after WP62) | created by WP62 (notes/, notes/directions/) |

## docs/superpowers/ (every entry)

| path | class | readers | disposition |
|---|---|---|---|
| `docs/superpowers/notes/claims-review.md` | live guidance | CLAUDE.md; register backing; tests/test_claims_register.py; work-packages/WP25-3-scope-of-work.md | moves to notes/ |
| `docs/superpowers/notes/figure-review.md` | live guidance | CLAUDE.md; work-packages/PM-BRIEF.md; work-packages/WP11-final/figure-review-paperfix2.md; work-packages/WP11-final/figure-review-paperfix3.md; work-packages/driver-log.md | moves to notes/ |
| `docs/superpowers/notes/proof-conventions.md` | live guidance | CLAUDE.md; register backing; docs/superpowers/notes/notation.md; docs/superpowers/specs/2026-11-07-posynomial-invariant-form-design.md; work-packages/WP54-scope-of-work.md | moves to notes/ |
| `docs/superpowers/notes/sklearn-conformance.md` | live guidance | CLAUDE.md; register backing; docs/superpowers/specs/2026-11-07-posynomial-invariant-form-design.md; tests/test_sklearn_compat.py; work-packages/README.md | moves to notes/ |
| `docs/superpowers/notes/vocabulary-review.md` | live guidance | CLAUDE.md; glossary.yaml; scripts/check_vocabulary.py; work-packages/WP25-4-scope-of-work.md; work-packages/interface-contract.md | moves to notes/ |
| `docs/superpowers/notes/presentation-framing.md` | live guidance | CLAUDE.md; docs/superpowers/specs/2026-11-07-posynomial-invariant-form-design.md; work-packages/WP8b-reviewers-guide-skeleton.md | moves to notes/ |
| `docs/superpowers/notes/user-journeys.md` | live guidance | paper/length_ledger.toml; work-packages/PM-BRIEF.md; work-packages/WP54-decisions.md; work-packages/WP54-review.md | moves to notes/ |
| `docs/superpowers/notes/residual-review.md` | live guidance | scripts/check_residuals.py; scripts/prose_surfaces.py; work-packages/PM-BRIEF.md; work-packages/WP8b-reviewers-guide-skeleton.md | moves to notes/ |
| `docs/superpowers/notes/reader-grid.md` | live guidance | work-packages/PM-BRIEF.md; work-packages/README.md; work-packages/WP11-scope-of-work.md; work-packages/WP8b-reviewers-guide-skeleton.md; work-packages/driver-log.md | moves to notes/ |
| `docs/superpowers/notes/verification-strategy.md` | live guidance | scripts/check.py; tests/conftest.py; work-packages/PM-BRIEF.md; work-packages/driver-log.md | moves to notes/ |
| `docs/superpowers/specs/2026-11-07-posynomial-invariant-form-design.md` | live guidance | CLAUDE.md; tests/test_narrative.py; work-packages/PM-BRIEF.md; work-packages/README.md | moves to notes/ |
| `docs/superpowers/notes/references-verified.md` | live guidance (the verified-sources ledger behind the bibliography) | register backing; derivation/PROOF_MAP_FINDINGS.md | moves to notes/ (added to the scope list: the register and PROOF_MAP_FINDINGS cite it) |
| `docs/superpowers/notes/paper-prior-art-sources.md` | live guidance (sources of the prior-art table) | paper/prior_art.yaml | moves to notes/ (added: tests/test_references.py reads it) |
| `docs/superpowers/notes/notation.md` | live guidance | docs/superpowers/notes/abstraction-gaps.md; docs/superpowers/notes/paper-sources/method.md; glossary.yaml; paper/container/RECORD.md; supporting_material.ipynb (notebook); tests/test_docs.py | stays until supporting_material.ipynb's package re-executes it, then moves to notes/ (the notebook links it) |
| `docs/superpowers/notes/abstraction-gaps.md` | live guidance | register backing; docs/superpowers/notes/notation.md; docs/superpowers/notes/paper-sources/README.md; docs/superpowers/notes/paper-sources/limitations.md; docs/superpowers/notes/paper-sources/method.md; docs/superpowers/notes/proof-conventions.md; docs/superpowers/notes/residual-review.md; paper/container/RECORD.md; paper/ge ... | stays until supporting_material.ipynb's package re-executes it, then moves to notes/ (the notebook links it; scripts/build_generated.py and paper/generate_repro.py read it) |
| `docs/superpowers/notes/adcs-tensions-probe.md` | historical | docs/superpowers/notes/abstraction-gaps.md; examples/adcs/cubesat_model.py; examples/adcs/cubesat_tradespace.sysml; supporting_material.ipynb (notebook); tests/test_adcs_enrichment.py | stays until supporting_material.ipynb's package re-executes it, then leaves the tree |
| `docs/superpowers/notes/kernel-direction.md` | historical (content carried by the WP43 readout) | none | leaves the tree, read by hash |
| `docs/superpowers/notes/figure-candidates/` | delivered content (the generator and record the register and the ternary-caption test read) | register backing | moves to paper/figures/ (register, test_paper.py re-pointed) |
| `docs/superpowers/notes/paper-sources/ (7 files)` | historical (snapshots of pages that left the docsite) | register backing; supporting_material.ipynb (notebook); tests/test_narrative.py; tests/test_paper_sources.py; work-packages/WP25-2-scope-of-work.md; work-packages/interface-contract.md; work-packages/interface-contract.toml | stays until supporting_material.ipynb's package re-executes it (literature.md is linked; tests/test_paper_sources.py and test_narrative.py guard the six snapshots, WP10 left them to repoint), then retires with those tests |
| `docs/superpowers/notes/spike-facet-refit/README.md, bench_oracle.py, methods.py` | historical (spike), notebook-linked | docs/superpowers/notes/abstraction-gaps.md; paper/generate_results.py; supporting_material.ipynb (notebook) | stays until supporting_material.ipynb's package re-executes it (README and bench_oracle.py are linked; bench_oracle imports methods.py) |
| `docs/superpowers/notes/spike-facet-refit/ (bench_cubesat.py, bench_planted.py, bench_restarts.py)` | historical (spike) | none | leaves the tree, read by hash |
| `docs/superpowers/notes/spike-figure1/ (2 files)` | historical (design spike of Figure 1) | paper/figures/figure1.py | leaves the tree, read by hash (paper/figures/figure1.py docstring cites the hash) |
| `docs/superpowers/notes/spike-horopca/ (16 files)` | historical (the first HoroPCA spike; WP35-rounds/spike-h holds the rerun the paper reads) | register backing; docs/superpowers/notes/spike-horopca/README.md; docs/superpowers/notes/spike-horopca/make_tables.py; docs/superpowers/notes/spike-horopca/test_spike_results.py; paper/prior_art.yaml | leaves the tree, read by hash (register backings of C536 and the gromov claim, prior_art.yaml comments re-pointed to WP35 readouts) |
| `docs/superpowers/notes/spike-sysml-diagrams/project.py` | builds or checks it (generator of the case model's views; three tests and scripts/check.py read it) | tests/test_model_coverage.py; tests/test_system_model_v2_r1.py; work-packages/WP25-scope-of-work.md | moves to scripts/sysml_project.py (tests and check.py re-pointed) |
| `docs/superpowers/notes/spike-sysml-diagrams/render.sh` | builds or checks it (renders the views) | none | moves with project.py to scripts/sysml_render.sh |

## paper/ (beyond the notebooks, their generators, figures, myst.yml and the container folder)

| path | class | readers | disposition |
|---|---|---|---|
| `paper/BROWSER_NOTES.md` | historical (browser-review notes) | work-packages/WP54-review.md | leaves the tree, read by hash |
| `paper/.gitignore` | builds or checks it | none | stays |
| `paper/environment_reference.npz` | builds or checks it | paper/container/README.md; paper/container/RECORD.md | stays |
| `paper/environment_values.toml` | builds or checks it | paper/container/README.md; paper/container/RECORD.md; paper/generate_findings.py; tests/_env.py; tests/test_cubesat_oracle.py; tests/test_paper.py; work-packages/WP25-scope-of-work.md | stays |
| `paper/execute_notebooks.py` | builds or checks it | paper/container/README.md; paper/container/RECORD.md; paper/generate_repro.py; supporting_material.ipynb (notebook); tests/test_paper.py; work-packages/WP11-final/figure-review-paperfix3.md; work-packages/WP25-4-scope-of-work.md; work-packages/WP54-review.md; work-packages/driver-log.md | stays |
| `paper/length_ledger.toml` | live guidance (the ledger) | docs/superpowers/notes/residual-review.md; paper/container/RECORD.md; work-packages/WP11-decisions.md; work-packages/WP25-2-scope-of-work.md; work-packages/WP25-3-scope-of-work.md; work-packages/WP53-review.md | stays |
| `paper/prior_art.yaml` | delivered content | register backing; docs/superpowers/notes/spike-horopca/grep_table.py; paper/container/RECORD.md; paper/generate_repro.py; supporting_material.ipynb (notebook); work-packages/WP11-decisions.md; work-packages/WP25-decisions.md; work-packages/WP25-review.md; work-packages/WP53-scope-of-work.md | stays (comment cites re-pointed) |
| `paper/reading_pass.yaml` | delivered content | register backing; docs/superpowers/notes/spike-horopca/grep_table.py; paper/generate_repro.py; supporting_material.ipynb (notebook); work-packages/WP8b-review.md | stays |
| `paper/style.css` | delivered content | paper/BROWSER_NOTES.md | stays |
| `paper/stability_extra.json` | delivered content | register backing; paper/container/RECORD.md | stays |
| `paper/stability_extra.py` | builds or checks it | paper/container/RECORD.md | stays |
| `paper/regenerate_row.py` | builds or checks it | paper/generate_repro.py; supporting_material.ipynb (notebook); tests/test_paper.py | stays |
| `paper/paper_common.py` | builds or checks it | paper/container/README.md; paper/container/RECORD.md; paper/environment_values.toml | stays |
| `paper/paper_paths.py` | builds or checks it | none | stays |
| `paper/paper_perturb.py` | builds or checks it | paper/environment_values.toml | stays |
| `paper/paper_stability.py` | builds or checks it | none | stays |

## examples/ (beyond each case's code, manifests, derived data and results.json)

| path | class | readers | disposition |
|---|---|---|---|
| `examples/adcs/case-model.md` | delivered content (the case model's how-to) | docs/superpowers/notes/user-journeys.md; scripts/check_vocabulary.py; scripts/prose_surfaces.py; scripts/residuals_baseline.json; tests/test_case_model_howto.py; work-packages/WP25-3-scope-of-work.md; work-packages/WP25-scope-of-work.md; work-packages/interface-contract.toml | stays |
| `examples/adcs/cubesat_tradespace.sysml` | delivered content | examples/adcs/experiments/ledger/ledger.jsonl; examples/adcs/experiments/probes/probe-record.md; work-packages/interface-contract.toml | stays |
| `examples/adcs/extended_design_space.sysml` | delivered content | work-packages/interface-contract.toml | stays |
| `examples/adcs/model_v2/ (3 .sysml, views/ 11 files)` | delivered content | register backing; docs/superpowers/notes/spike-sysml-diagrams/project.py; examples/adcs/experiments/ledger/ledger.jsonl; examples/adcs/model_v2/coverage.py; examples/adcs/model_v2/diagnostic_pair.py; examples/adcs/model_v2/ledger_gate.py; examples/adcs/model_v2/views/coverage.md; paper/container/README.md; paper/container/RE ... | stays |
| `examples/adcs/experiments/probes/probe-record.md` | delivered content (a record the case read by tests) | none | stays |
| `examples/adcs/experiments/reports/ (change-register.md, sensitivity.json)` | delivered content (data of record) | register backing; docs/superpowers/notes/abstraction-gaps.md; paper/container/RECORD.md; supporting_material.ipynb (notebook); tests/test_paper.py; work-packages/WP25-2-scope-of-work.md; work-packages/WP25-3-scope-of-work.md; work-packages/WP25-scope-of-work.md; work-packages/driver-log.md | stays |
| `examples/adcs/experiments/ledger/ledger.jsonl` | delivered content (the experiment ledger) | examples/adcs/model_v2/stakeholders.sysml; paper/container/README.md; paper/container/RECORD.md; work-packages/interface-contract.md; work-packages/interface-contract.toml | stays |
| `examples/adcs/experiments/toolkit-pin.toml` | builds or checks it | .github/workflows/test.yml; Dockerfile | stays |
| `examples/*/LICENCE-DATA.txt (3)` | delivered content | examples/wheat/derive.py; work-packages/driver-log.md | stays |
| `examples/*/variants.json (3)` | delivered content | register backing; docs/examples/perovskite.md; examples/amniote/variants.py; examples/perovskite/variants.py; examples/wheat/variants.py; work-packages/WP59-review.md; work-packages/WP59-rounds/amniote.md; work-packages/WP59-rounds/perovskite.md; work-packages/WP59-rounds/readout.md; work-packages/WP59-rounds/wheat.md; work- ... | stays |

## scripts/

| path | class | readers | disposition |
|---|---|---|---|
| `scripts/admissibility.py` | builds or checks it | .github/workflows/draft-label-gate.yml; .github/workflows/issue-admissibility.yml; .github/workflows/merge-by-code-owner.yml; .github/workflows/pr-fields.yml; .github/workflows/pr-linked-issue.yml; docs/code-owners.md | stays |
| `scripts/assemble_site.py` | builds or checks it | .github/workflows/pages.yml; paper/.gitignore; tests/test_check_script.py; tests/test_site.py; work-packages/WP25-2-scope-of-work.md; work-packages/WP25-4-scope-of-work.md; work-packages/WP25-scope-of-work.md; work-packages/WP8b-decisions.md; work-packages/WP8b-scope-of-work.md | stays |
| `scripts/build_figures.py` | builds or checks it | paper/container/RECORD.md; work-packages/WP25-4-scope-of-work.md; work-packages/WP25-review.md; work-packages/WP60-rounds/amniote.md; work-packages/WP60-rounds/wheat.md; work-packages/WP60-scope-of-work.md; work-packages/driver-log.md | stays |
| `scripts/build_generated.py` | builds or checks it | docs/superpowers/notes/paper-sources/README.md; docs/superpowers/notes/presentation-framing.md; docs/superpowers/specs/2026-11-07-posynomial-invariant-form-design.md; glossary.yaml; mkdocs.yml; work-packages/WP8b-scope-of-work.md; work-packages/interface-contract.md; work-packages/interface-contract.toml | stays (paths updated) |
| `scripts/build_site_figures.py` | builds or checks it | register backing; docs/examples.md; work-packages/WP51-decisions.md; work-packages/WP51-rounds/synthetic-case.md; work-packages/WP51-scope-of-work.md | stays |
| `scripts/check.py` | builds or checks it | CHANGELOG.md; docs/superpowers/notes/verification-strategy.md; tests/test_check_script.py; work-packages/WP25-2-scope-of-work.md; work-packages/WP25-3-scope-of-work.md; work-packages/WP25-4-scope-of-work.md; work-packages/WP25-review.md; work-packages/WP25-scope-of-work.md; work-packages/WP8b-decisions.md; work-packages/driv ... | stays (paths updated) |
| `scripts/check_history_links.py` | builds or checks it | history.yaml; tests/test_site.py | stays |
| `scripts/check_release_version.py` | builds or checks it | .github/workflows/release.yml | stays |
| `scripts/check_residuals.py` | builds or checks it | CLAUDE.md; docs/superpowers/notes/residual-review.md; tests/test_residuals.py; work-packages/WP53-scope-of-work.md; work-packages/WP54-review.md; work-packages/WP54-scope-of-work.md; work-packages/WP57-scope-of-work.md; work-packages/WP59-review.md; work-packages/WP59-scope-of-work.md; work-packages/WP60-scope-of-work.md; wo ... | stays (paths updated) |
| `scripts/check_vocabulary.py` | builds or checks it | CLAUDE.md; docs/superpowers/notes/residual-review.md; docs/superpowers/notes/vocabulary-review.md; scripts/check_residuals.py; tests/test_vocabulary.py; work-packages/WP25-2-scope-of-work.md; work-packages/WP25-3-scope-of-work.md; work-packages/WP25-4-scope-of-work.md; work-packages/WP25-review.md; work-packages/WP25-scope-o ... | stays (paths updated) |
| `scripts/history_record.py` | builds or checks it | tests/test_site.py | stays |
| `scripts/paper_keys.py` | builds or checks it | mkdocs.yml; work-packages/WP8b-decisions.md; work-packages/WP8b-review.md; work-packages/interface-contract.md; work-packages/interface-contract.toml | stays |
| `scripts/prose_surfaces.py` | builds or checks it | docs/superpowers/notes/residual-review.md; scripts/check_residuals.py; tests/test_residuals.py; work-packages/WP8b-reviewers-guide-skeleton.md | stays (paths updated) |
| `scripts/release_checks.py` | builds or checks it | .github/workflows/release.yml | stays |
| `scripts/residuals_baseline.json` | builds or checks it | docs/superpowers/notes/residual-review.md; scripts/check_residuals.py; work-packages/WP8b-reviewers-guide-skeleton.md | stays (paths updated) |
| `scripts/stage_site.py` | builds or checks it | tests/test_site.py; work-packages/WP11-final/README.md; work-packages/WP25-3-scope-of-work.md; work-packages/WP25-4-scope-of-work.md; work-packages/WP25-review.md; work-packages/WP8b-decisions.md; work-packages/WP8b-release-checklist.md; work-packages/WP8b-review.md; work-packages/WP8b-reviewers-guide-skeleton.md; work-packa ... | stays |
| `scripts/vocabulary_baseline.toml` | builds or checks it | scripts/check_vocabulary.py; work-packages/WP25-2-scope-of-work.md; work-packages/WP25-4-scope-of-work.md; work-packages/WP25-review.md; work-packages/WP25-scope-of-work.md; work-packages/WP53-review.md; work-packages/WP8b-release-checklist.md; work-packages/driver-log.md | stays (paths updated) |
| `scripts/wp30_cost_ladders.py` | builds or checks it (WP30 cost ladders; two tests run it) | tests/test_cost_model.py; tests/test_wp30_cost_ladders.py | stays |

## site/

| path | class | readers | disposition |
|---|---|---|---|
| `site/index.html` | delivered content | register backing; docs/superpowers/notes/presentation-framing.md; docs/superpowers/notes/residual-review.md; docs/superpowers/notes/user-journeys.md; docs/superpowers/notes/vocabulary-review.md; scripts/assemble_site.py; scripts/check_vocabulary.py; scripts/prose_surfaces.py; scripts/residuals_baseline.json; tests/test_check ... | stays |
| `site/history.html` | delivered content | register backing; docs/superpowers/notes/residual-review.md; history.yaml; scripts/history_record.py; scripts/prose_surfaces.py; scripts/residuals_baseline.json; tests/test_residuals.py; tests/test_site.py; work-packages/WP8b-reviewers-guide-skeleton.md; work-packages/driver-log.md | stays |
| `site/paper/index.html` | delivered content | work-packages/WP25-3-scope-of-work.md | stays |

## work-packages/ (what WP61 left, and the boundary readouts)

| path | class | readers | disposition |
|---|---|---|---|
| `work-packages/INDEX.md` | live package (the index) | CLAUDE.md; work-packages/WP61-scope-of-work.md | stays |
| `work-packages/PM-BRIEF.md` | live guidance | CLAUDE.md; paper/container/RECORD.md; work-packages/WP25-4-scope-of-work.md | stays |
| `work-packages/README.md` | live package (the protocol) | CLAUDE.md; register backing; docs/superpowers/specs/2026-11-07-posynomial-invariant-form-design.md; tests/test_interface_contract.py; work-packages/PM-BRIEF.md; work-packages/WP25-3-scope-of-work.md; work-packages/WP61-scope-of-work.md; work-packages/driver-log.md; work-packages/interface-contract.md | stays |
| `work-packages/WP10-decisions.md` | historical | derivation/PROOF_MAP_FINDINGS.md; docs/superpowers/notes/claims-review.md; docs/superpowers/notes/notation.md; docs/superpowers/notes/vocabulary-review.md; paper/container/README.md; paper/myst.yml | stays (held by derivation/PROOF_MAP_FINDINGS.md, paper) |
| `work-packages/WP10-reading-pass.md` | historical | paper/generate_reading_pass.py; paper/reading_pass.yaml | stays (held by paper) |
| `work-packages/WP10-scope-of-work.md` | historical | docs/superpowers/notes/paper-sources/README.md | leaves the tree, read by hash (INDEX.md names it) |
| `work-packages/WP10-vocabulary-review.md` | historical | scripts/vocabulary_baseline.toml | stays (held by scripts) |
| `work-packages/WP11-decisions.md` | live package | (the package) | stays |
| `work-packages/WP11-final/` | live package | (the package) | stays |
| `work-packages/WP11-round-1` | live package | (the package) | stays |
| `work-packages/WP11-scope-of-work.md` | live package | (the package) | stays |
| `work-packages/WP12-decisions.md` | live package | (the package) | stays |
| `work-packages/WP16-decisions.md` | historical | paper/container/RECORD.md | stays (held by paper) |
| `work-packages/WP17-decisions.md` | historical | register backing; docs/superpowers/notes/claims-review.md | stays (held by claims_register.toml) |
| `work-packages/WP17-scope-of-work.md` | historical | register backing; docs/superpowers/notes/claims-review.md | stays (held by claims_register.toml) |
| `work-packages/WP18-decisions.md` | historical | docs/superpowers/notes/figure-review.md | leaves the tree, read by hash (INDEX.md names it) |
| `work-packages/WP19-decisions.md` | historical | docs/superpowers/notes/figure-review.md; paper/figures/chart_level.py; paper/figures/figure1.py; paper/figures/planes.py; paper/figures/ternary_pair.py | stays (held by paper) |
| `work-packages/WP19-figure-review.md` | historical | register backing; paper/length_ledger.toml | stays (held by claims_register.toml, paper) |
| `work-packages/WP20-review.md` | historical | tests/test_check_script.py | stays (held by tests) |
| `work-packages/WP21-scope-of-work.md` | live package | (the package) | stays |
| `work-packages/WP23-decisions.md` | historical | register backing; examples/adcs/model_v2/ledger_gate.py | stays (held by claims_register.toml, examples) |
| `work-packages/WP23-review.md` | historical | examples/adcs/model_v2/coverage.py | stays (held by examples) |
| `work-packages/WP23-rounds/` | historical | examples/adcs/experiments/reports/change-register.md; examples/adcs/model_v2/diagnostic_pair.py; paper/container/RECORD.md; supporting_material.ipynb (notebook); scripts/wp30_cost_ladders.py; tests/test_noise_ridge.py; tests/test_wp30_cost_ladders.py; work-packages/WP25-2-scope-of-work.md; work-packages/WP25-3-scope-of-work. ... | stays until supporting_material.ipynb's package re-executes it (the notebook reads it) |
| `work-packages/WP25-2-scope-of-work.md` | live package | (the package) | stays |
| `work-packages/WP25-3-scope-of-work.md` | live package | (the package) | stays |
| `work-packages/WP25-4-scope-of-work.md` | live package | (the package) | stays |
| `work-packages/WP25-decisions.md` | live package | (the package) | stays |
| `work-packages/WP25-review.md` | live package | (the package) | stays |
| `work-packages/WP25-rounds/` | live package | (the package) | stays |
| `work-packages/WP25-scope-of-work.md` | live package | (the package) | stays |
| `work-packages/WP29-review/` | historical | paper/length_ledger.toml | stays (held by paper) |
| `work-packages/WP30-build-notes.md` | historical | examples/adcs/experiments/definitions.py | stays (held by examples) |
| `work-packages/WP30-rounds/` | historical | paper/container/RECORD.md; scripts/wp30_cost_ladders.py | stays (held by paper, scripts) |
| `work-packages/WP31-readout.md` | historical | register backing | stays (held by claims_register.toml) |
| `work-packages/WP33-scope-of-work.md` | historical | paper/length_ledger.toml | stays (held by paper) |
| `work-packages/WP35-amendment-1-scope.md` | historical | paper/length_ledger.toml | stays (held by paper) |
| `work-packages/WP35-decisions.md` | historical | register backing; paper/length_ledger.toml | stays (held by claims_register.toml, paper) |
| `work-packages/WP35-review.md` | historical | paper/length_ledger.toml | stays (held by paper) |
| `work-packages/WP35-rounds/` | historical | register backing; docs/superpowers/notes/spike-horopca/README.md; paper/generate_repro.py; paper/prior_art.yaml; supporting_material.ipynb (notebook); tests/test_paper.py | stays until supporting_material.ipynb's package re-executes it (the notebook reads it) |
| `work-packages/WP36-decisions.md` | boundary content | register backing | readout copied to notes/directions/ (one file); the rest stays, held by readers |
| `work-packages/WP36-rounds/` | boundary content (readout.md and the three wave notes); the rest historical | register backing; work-packages/PM-BRIEF.md | readout copied to notes/directions/ (one file); the rest stays, held by readers |
| `work-packages/WP37-rounds/` | historical | register backing; scripts/history_record.py; tests/test_site.py | stays (held by claims_register.toml, scripts, tests) |
| `work-packages/WP38-confirmations/` | historical | docs/superpowers/notes/residual-review.md | leaves the tree, read by hash (INDEX.md names it) |
| `work-packages/WP38-flags/` | historical | docs/superpowers/notes/residual-review.md | leaves the tree, read by hash (INDEX.md names it) |
| `work-packages/WP38-scope-of-work.md` | historical | docs/superpowers/notes/residual-review.md | leaves the tree, read by hash (INDEX.md names it) |
| `work-packages/WP39-scope-of-work.md` | historical | paper/length_ledger.toml | stays (held by paper) |
| `work-packages/WP41-rounds/` | boundary content (spike/readout.md); the rest historical | register backing | readout copied to notes/directions/ (one file); the rest stays, held by readers |
| `work-packages/WP43-rounds/` | boundary content (spike/readout.md); the rest historical | docs/superpowers/notes/kernel-direction.md | readout copied to notes/directions/ (one file); the rest leaves the tree |
| `work-packages/WP45-rounds/` | historical | register backing; docs/superpowers/notes/paper-prior-art-sources.md; examples/amniote/run.py; examples/perovskite/run.py | stays (held by claims_register.toml, examples) |
| `work-packages/WP46-decisions.md` | historical | register backing | stays (held by claims_register.toml) |
| `work-packages/WP46-rounds/` | historical | register backing | stays (held by claims_register.toml) |
| `work-packages/WP47-rounds/` | historical | .github/workflows/issue-admissibility.yml; tests/test_admissibility.py; tests/test_release_checks.py | stays (held by .github/workflows/issue-admissibility.yml, tests) |
| `work-packages/WP4b-decisions.md` | historical | docs/superpowers/notes/adcs-tensions-probe.md; tests/test_adcs_enrichment.py | stays (held by tests) |
| `work-packages/WP51-decisions.md` | live package | (the package) | stays |
| `work-packages/WP51-rounds/` | live package | (the package) | stays |
| `work-packages/WP51-scope-of-work.md` | live package | (the package) | stays |
| `work-packages/WP53-decisions.md` | live package | (the package) | stays |
| `work-packages/WP53-review.md` | live package | (the package) | stays |
| `work-packages/WP53-scope-of-work.md` | live package | (the package) | stays |
| `work-packages/WP54-decisions.md` | live package | (the package) | stays |
| `work-packages/WP54-review.md` | live package | (the package) | stays |
| `work-packages/WP54-scope-of-work.md` | live package | (the package) | stays |
| `work-packages/WP55-decisions.md` | live package | (the package) | stays |
| `work-packages/WP55-scope-of-work.md` | live package | (the package) | stays |
| `work-packages/WP56-decisions.md` | live package | (the package) | stays |
| `work-packages/WP57-decisions.md` | live package | (the package) | stays |
| `work-packages/WP57-scope-of-work.md` | live package | (the package) | stays |
| `work-packages/WP59-decisions.md` | live package | (the package) | stays |
| `work-packages/WP59-review.md` | live package | (the package) | stays |
| `work-packages/WP59-rounds/` | live package | (the package) | stays |
| `work-packages/WP59-scope-of-work.md` | live package | (the package) | stays |
| `work-packages/WP60-decisions.md` | live package | (the package) | stays |
| `work-packages/WP60-rounds/` | live package | (the package) | stays |
| `work-packages/WP60-scope-of-work.md` | live package | (the package) | stays |
| `work-packages/WP61-decisions.md` | live package | (the package) | stays |
| `work-packages/WP61-scope-of-work.md` | live package | (the package) | stays |
| `work-packages/WP62-decisions.md` | live package | (the package) | stays |
| `work-packages/WP62-scope-of-work.md` | live package | (the package) | stays |
| `work-packages/WP8b-decisions.md` | live package | (the package) | stays |
| `work-packages/WP8b-release-checklist.md` | live package | (the package) | stays |
| `work-packages/WP8b-review.md` | live package | (the package) | stays |
| `work-packages/WP8b-reviewers-guide-skeleton.md` | live package | (the package) | stays |
| `work-packages/WP8b-rounds` | live package | (the package) | stays |
| `work-packages/WP8b-scope-of-work.md` | live package | (the package) | stays |
| `work-packages/WP9-decisions.md` | historical | docs/superpowers/notes/notation.md; docs/superpowers/notes/spike-facet-refit/README.md | leaves the tree, read by hash (INDEX.md names it) |
| `work-packages/WP9-review.md` | historical | docs/superpowers/notes/abstraction-gaps.md; supporting_material.ipynb (notebook) | stays until supporting_material.ipynb's package re-executes it (the notebook reads it) |
| `work-packages/build-notes/` | historical | docs/superpowers/specs/2026-11-07-posynomial-invariant-form-design.md; examples/adcs/experiments/probes/probe-record.md; work-packages/PM-BRIEF.md; work-packages/README.md | leaves the tree, read by hash |
| `work-packages/deliverables-grid.md` | historical | none | leaves the tree, read by hash |
| `work-packages/driver-log.md` | live package (the log) | docs/superpowers/notes/verification-strategy.md; work-packages/PM-BRIEF.md | stays |
| `work-packages/examples-coverage.md` | historical | work-packages/PM-BRIEF.md; work-packages/driver-log.md | leaves the tree, read by hash |
| `work-packages/external-assessment-2026-11-09/` | historical | docs/superpowers/notes/abstraction-gaps.md; supporting_material.ipynb (notebook); work-packages/WP21-scope-of-work.md; work-packages/WP25-scope-of-work.md | stays until supporting_material.ipynb's package re-executes it, then leaves |
| `work-packages/external-review-2026-11.md` | historical | docs/superpowers/notes/abstraction-gaps.md; docs/superpowers/notes/notation.md | leaves the tree, read by hash |
| `work-packages/interface-contract.md` | delivered content (the contract) | CLAUDE.md; register backing; tests/test_interface_contract.py; work-packages/PM-BRIEF.md; work-packages/WP25-2-scope-of-work.md; work-packages/WP25-3-scope-of-work.md; work-packages/WP25-4-scope-of-work.md; work-packages/interface-contract.toml | stays |
| `work-packages/interface-contract.toml` | delivered content (the contract) | CLAUDE.md; register backing; tests/test_check_script.py; tests/test_interface_contract.py; work-packages/WP25-2-scope-of-work.md; work-packages/WP25-3-scope-of-work.md; work-packages/WP25-4-scope-of-work.md; work-packages/WP8b-scope-of-work.md; work-packages/interface-contract.md | stays |
| `work-packages/milestones.md` | live package (the release board) | none | stays |
| `work-packages/outlines/` | historical | docs/superpowers/notes/paper-prior-art-sources.md; work-packages/PM-BRIEF.md; work-packages/README.md | leaves the tree, read by hash |
| `work-packages/paper-requirements.md` | historical | work-packages/driver-log.md | leaves the tree, read by hash |
| `work-packages/parallel-board.md` | live package (PM state) | work-packages/PM-BRIEF.md; work-packages/driver-log.md | stays |
| `work-packages/release-candidate.md` | live package (WP8b) | work-packages/WP8b-scope-of-work.md | stays |
| `work-packages/release-punch-list.md` | live package (WP8b) | work-packages/WP8b-scope-of-work.md | stays |
| `work-packages/review/` | live package (WP53, WP54, WP57 state: deferred, open questions) | paper/length_ledger.toml; work-packages/WP11-decisions.md; work-packages/WP53-review.md; work-packages/WP53-scope-of-work.md; work-packages/WP54-decisions.md; work-packages/WP54-review.md; work-packages/WP54-scope-of-work.md; work-packages/WP55-scope-of-work.md; work-packages/WP57-scope-of-work.md; work-packages/WP8b-scope-o ... | stays |
| `work-packages/reviewers-guide/` | live package (WP8b, WP58) | work-packages/WP8b-scope-of-work.md | stays |
| `work-packages/spikes/` | historical (three spikes) | docs/superpowers/notes/abstraction-gaps.md; docs/superpowers/notes/paper-sources/limitations.md; docs/superpowers/notes/paper-sources/method.md; paper/container/README.md; paper/container/RECORD.md; supporting_material.ipynb (notebook); pyproject.toml | spike-objective and spike-certificates stay until supporting_material.ipynb's package re-executes them; spike-container-platform leaves (cited by the container README and RECORD, re-pointed to the hash) |
| `work-packages/status-report-template.md` | historical | none | leaves the tree, read by hash |
| `work-packages/supervisor-review-list.md` | historical | docs/superpowers/notes/residual-review.md; work-packages/driver-log.md | leaves the tree, read by hash |
| `work-packages/supervisor-tasks.md` | historical | none | leaves the tree, read by hash |
| `work-packages/supervisor-walkthrough.md` | historical | work-packages/driver-log.md | leaves the tree, read by hash |
| `work-packages/swap-evidence.md` | historical | CHANGELOG.md; examples/adcs/experiments/reports/change-register.md; examples/adcs/experiments/sensitivity.py; paper/container/RECORD.md; tests/test_cubesat_model.py; tests/test_v2_data.py; work-packages/driver-log.md | stays: read by tests/test_cubesat_model.py, tests/test_v2_data.py, CHANGELOG.md, the case change register |
| `(out of the tree) WP48-rounds/spike/readout.md (WP48, governance control checks)` | boundary content | none (to be cited from WP54-review.md's Future work record) | restored from commit ba62c15 as one file under notes/directions/ |
| `(out of the tree) WP50-rounds/spike/readout.md (WP50, persistent homology)` | boundary content | none (to be cited from WP54-review.md's Future work record) | restored from commit 5233126 as one file under notes/directions/ |
| `(out of the tree) WP52-rounds/spike/proposal.md (WP52, governance lineage proposal)` | boundary content | none (to be cited from WP54-review.md's Future work record) | restored from commit 03790a0 as one file under notes/directions/ |
| `(out of the tree) WP56-rounds/ternary/readout.md (WP56 ternary spike; on branch wp56-ternary, not yet on dev)` | boundary content | none (to be cited from WP54-review.md's Future work record) | taken from commit cf4faca on branch wp56-ternary when the driver says so; until then the index lists it as pending |

## Counts

Rows: 213 (a row is a path, a folder or a named group of files).

By class: boundary content 8; builds or checks it 42; delivered content 34; historical 56; live guidance 19; live package 54.

By disposition: boundary readout to notes/directions/ 8; created 1; leaves 21; moves 16; stays 157; stays until the notebook package 10.

Class by disposition:

| class | disposition | rows |
|---|---|---|
| boundary content | boundary readout to notes/directions/ | 8 |
| builds or checks it | moves | 2 |
| builds or checks it | stays | 40 |
| delivered content | moves | 1 |
| delivered content | stays | 33 |
| historical | leaves | 21 |
| historical | stays | 27 |
| historical | stays until the notebook package | 8 |
| live guidance | created | 1 |
| live guidance | moves | 13 |
| live guidance | stays | 3 |
| live guidance | stays until the notebook package | 2 |
| live package | stays | 54 |

Top-level paths classified historical: none, so R-2 is met on the top level; the only top-level historical material sits inside `work-packages/` and `docs/superpowers/`.

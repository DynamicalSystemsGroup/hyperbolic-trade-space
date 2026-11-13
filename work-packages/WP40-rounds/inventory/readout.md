# WP40 stage 1: inventory of what a release reader meets

Head inventoried: `dev` 1d741d2 (2026-11-12). Counts are of tracked files (`git ls-files`, 1126 files, 65.2 MB real bytes);
sizes are bytes on disk, not blocks. "Readers" are the other tracked files that name the item by path (code, tests, config,
prose). Nothing was moved, deleted or edited to make this readout. The per-entry table for `work-packages/` (184 entries,
size, file count, readers) is `work-packages-entries.txt` beside this file.

Option vocabulary, one per row, no ranking: **stays** (where it is), **moves** (to a named place), **goes** (git keeps the
history), **pointer** (summarized in one file that points at the history, the content leaves the tree). Where a row names two,
they are alternatives for the decision stage, not a sequence.

## 1. What dominates

Checkout (tracked, 65.2 MB) and the archive a GitHub reader downloads ("Download ZIP" or a release's source tarball is
`git archive HEAD`: 49.4 MB gzipped, of which `work-packages/` is 44.1 MB and `docs/superpowers/` 0.7 MB).

| Rank | Item | Size | Files | Share of checkout |
|---|---|---|---|---|
| 1 | `work-packages/` screenshots (png/jpg) | 44.7 MB | 324 | 69 % |
| 2 | `work-packages/` everything else (md 7.9 MB across 419 md files, plus 15 py, 10 txt, small data) | 7.6 MB | 456 | 12 % |
| 3 | `examples/adcs/` (data 2.8 MB, `case.py` 92 KB, experiments 0.8 MB, model_v2 0.5 MB) | 4.3 MB | 60 | 7 % |
| 4 | `paper/` (the two notebooks 2.3 MB, figures 1.3 MB) | 4.0 MB | 47 | 6 % |
| 5 | `tests/` (166 KB of data and fixtures beyond the 60 test files) | 1.7 MB | 72 | 3 % |
| 6 | `docs/` (`superpowers/` 1.5 MB, the docs site 0.15 MB) | 1.7 MB | 90 | 3 % |
| 7 | the rest: `derivation/` 0.7, `scripts/` 0.3, `claims_register.toml` 0.3, `uv.lock`, `src/` and the root files | about 1.5 MB | | 2 % |

Eight directories hold about 43 MB of the 44.7 MB of screenshots: WP28-review 9.3 MB, WP30-review 8.8, WP32-review 8.1,
WP35-review 4.5, WP33-review 4.0, WP30-rounds 3.8, WP29-review 3.6, WP26-view-editor-feedback 1.1 (all sizes bytes, one WP each).
No code, test, script or config reads any file in the eight review directories except `WP30-rounds/cost-ladders.md`
(written by `scripts/wp30_cost_ladders.py`) and `WP35-rounds/` (read by `tests/test_paper.py`, see section 3).

Git pack (`git count-objects -vH`): 12 974 objects in pack, 100.6 MiB, 2 packs, 2724 loose objects (76.7 MiB, to be
repacked by a `git gc` and not content). 1696 commits, 115 refs. The pack is history: removing a file from the tree does not
shrink it. By path, summing every blob ever stored: `examples/adcs/` 18.0 MB (of which the deleted
`adcs_trade_study.ipynb` two versions 3.6 MB, the deleted `examples/adcs/figures/` PNGs about 3 MB), the 98 revisions of
`paper/paper.ipynb` 11.4 MB, `docs/superpowers/` 9.0 MB (418 blobs, spike data and the deleted spike folders), `paper/figures/`
8.3 MB, and the work-package screenshots about 45 MB compressed-in-pack. The largest single stored blobs are the notebook
revisions (2.7 MB each) then the 0.9 MB history-page screenshots in `WP37-review/` and `WP37-rounds/`. Only a history rewrite
shrinks the pack; no option below proposes one (an option for the supervisor if he wants the clone itself thin: a rewrite
changes every commit hash the records quote).

What a GitHub reader sees first: the root listing (25 entries: dirs `derivation docs examples paper scripts site src tests
work-packages`, files `CHANGELOG.md CLAUDE.md Dockerfile LICENSE README.md claims_register.toml glossary.yaml history.yaml
mkdocs.yml pyproject.toml uv.lock` and dotfiles), then the README: a one-line purpose, a clone block, a 12-line example, and a
Layout list of seven entries. The Layout list omits `CHANGELOG.md`, `CLAUDE.md`, `claims_register.toml`, `glossary.yaml`,
`history.yaml`, `mkdocs.yml`, `Dockerfile` and `docs/superpowers/`, and describes `work-packages/` as "scopes and decisions"
although it is 80 % of the tree. A tarball reader unpacks 65 MB, of which `work-packages/` (184 entries) is four fifths; it sorts last in the listing.

## 2. Protected (not thinned by this package)

| Item | Where | Why protected |
|---|---|---|
| The paper | `paper/paper.ipynb`, `paper/supporting_material.ipynb`, `paper/figures/`, `paper/generate_*.py`, `paper/myst.yml`, `paper/length_ledger.toml`, `paper/*.yaml`, `paper/container/` | the paper and what builds it |
| Data of record | `examples/adcs/data/v2/` (4 CSV), `paper/environment_reference.npz`, `paper/environment_values.toml`, `tests/data/v2_first_designs_of_record.csv`, `examples/adcs/experiments/ledger/ledger.jsonl` | read by tests and hashed by the ledger (`.gitattributes` fixes LF endings for this reason) |
| Decision records | the 42 `work-packages/WP*-decisions.md` (546 KB), and `driver-log.md` (204 KB) | the supervisor's words verbatim; the record of the gates |
| Held-out material | something in `work-packages/WP11-*` is protected; it was not opened and is not described here | not this package's |
| Claims and vocabulary | `claims_register.toml`, `glossary.yaml`, `history.yaml`, `scripts/vocabulary_baseline.toml`, `scripts/residuals_baseline.json` | tests read them |
| Contract | `work-packages/interface-contract.md`, `interface-contract.toml` | pinned by `tests/test_interface_contract.py` (deletions check the contract first, PM-BRIEF) |
| Kept by decision | any file a decision record names as a deliverable (PM-BRIEF, 2026-11-11) | the record is its reader; this inventory does not decide those, the next stage greps the 42 records |

## 3. Top-level directories and files

| Entry | What it does for the release reader / the record | Size, files | Readers | Options |
|---|---|---|---|---|
| `src/hyperbolic_trade_space/` | the package | 0.2 MB, 12 | everything | stays |
| `docs/` (site pages, `user-guide/`, `references.bib`) | the docs site, built by mkdocs (`docs/superpowers/` excluded from the site by `exclude_docs`) | 0.15 MB, 19 | `mkdocs.yml`, tests | stays |
| `docs/superpowers/notes/` | 31 working notes and 9 spike folders; a mix of live references and build residue (section 4) | 1.5 MB, 70 | see section 4 | per row |
| `docs/superpowers/specs/` | the design spec CLAUDE.md names; read by `tests/test_narrative.py` | 44 KB, 1 | CLAUDE.md, test | stays |
| `paper/`, `site/` | the paper and the root page | 4.0 MB, 47; 24 KB, 3 | protected | stays |
| `derivation/` | SymPy lemma scripts, proof-map record and findings | 0.7 MB, 30 | tests, paper | stays |
| `examples/adcs/` | the case study: model, simulator, data, experiments, SysML model v2 | 4.3 MB, 60 | tests, paper, docs | stays; subrows in section 6 |
| `scripts/` | 14 build and check tools, 2 baselines | 0.3 MB, 15 | CI, tests | stays; `wp30_cost_ladders.py` row in section 6 |
| `tests/` | 60 test files, fixtures, data | 1.7 MB, 72 | CI | stays |
| `work-packages/` | the build's record: scopes, reviews, decisions, round outputs, screenshots | 52.3 MB, 780 | 3 tests, 4 scripts, paper generators, the claims register | per row, sections 3 and 5 |
| `.github/workflows/` | CI (`test.yml` on `main`, `pages.yml` on tags) | 2 files | | stays |
| `README.md` | the front door; Layout list incomplete | 4 KB | | stays, Layout list redrafted (section 7) |
| `CHANGELOG.md` | what changed per package; points at `work-packages/` and git history | 8 KB | | stays |
| `CLAUDE.md` | conventions for agents; names `work-packages/` and `docs/superpowers/` paths | 8 KB | agents | stays, or moves into `work-packages/` with README pointer |
| `claims_register.toml` | every claim a reader can rely on and its backing; 0.3 MB; cites 90+ repository paths | 0.3 MB | `tests/test_claims_register.py` | stays |
| `glossary.yaml`, `history.yaml` | the one source of terms; the release history record | 40 KB each | tests, scripts | stays |
| `mkdocs.yml`, `Dockerfile`, `pyproject.toml`, `uv.lock`, `.python-version`, `LICENSE`, `.gitattributes`, `.dockerignore`, `.gitignore` | tooling | small | | stays |
| `pyproject.toml` ruff exclusion | excludes `docs/superpowers/notes/spike-*` and `work-packages/WP32-cells/round-*` | | | moves with whatever moves of those two paths |

## 4. `docs/superpowers/notes/` (31 entries; bytes, readers outside the entry)

Readers column: C = code/tests/config, D = other docs, W = mentions in `work-packages/`.

| Entry | Size | Readers | What it does | Options |
|---|---|---|---|---|
| `abstraction-gaps.md` | 34 KB | C3 D7 W19 | source of Appendix E; generator reads it | stays |
| `notation.md` | 22 KB | C2 D4 W12 | notation reference; `tests/test_docs.py` reads it; glossary cites | stays |
| `paper-sources/` (7 files) | 159 KB | C3 W16 | sources the paper's prose is built from; `tests/test_paper_sources.py`, `test_narrative.py` read it | stays |
| `claims-review.md`, `vocabulary-review.md`, `residual-review.md`, `proof-conventions.md`, `sklearn-conformance.md`, `figure-review.md`, `verification-strategy.md`, `references-verified.md` | 12, 6, 10, 12, 5, 4, 4, 15 KB | C1-2 each (not figure-review) | the standing conventions the repository's checks apply | stays; or all move to `docs/conventions/` (one folder, eight files, so the README names one place) |
| `presentation-framing.md`, `user-journeys.md` | 3, 9 KB | `user-journeys` C2 | site framing; wayfinding input | stays |
| `reader-grid.md` | 17 KB | W19 | reader personas (the grid; not the answer key) | stays; or moves with the review records |
| `adcs-tensions-probe.md` | 85 KB | C2 D3 W6 | probe record cited by `cubesat_model.py`, its test and a SysML file | stays; or pointer (the 85 KB cited by two code comments) |
| `adcs-port.md`, `opensysml-usage.md`, `system-model-tidy.md`, `view-editor-harness.md` | 3, 3, 12, 7 KB | no code reader (W4-12; `adcs-port` and `opensysml-usage` D1) | build notes on the model and tool | goes; or moves to `work-packages/` |
| `paper-outline-v1-baseline.md`, `paper-outline-v2-search.md`, `search-prior-art.md` | 20, 9, 7 KB | no code reader | outline history and a search record the paper superseded | goes; or moves to `work-packages/` |
| `paper-prior-art-sources.md` | 15 KB | C1 (`paper/prior_art.yaml`) | source list behind the prior-art generator | stays |
| `figure-candidates/` (1 file) | 5 KB | C1 (register cites it) | the triple-search script | stays; or goes (register row narrowed) |
| `spike-horopca/` (14 files) | 621 KB | C2 (register, `prior_art.yaml`) | the HoroPCA spike: results the register cites; includes a 512 KB `tables.npz` | stays; or moves its data out and keeps `README.md` |
| `spike-sysml-diagrams/` (2) | 60 KB | C3 | `project.py` is live (tests, `scripts/check.py`); the 108 other files were deleted by WP25 | stays |
| `spike-facet-refit/` (6), `spike-figure1/` (2) | 42, 27 KB | C2 each (`generate_results.py`, `figure1.py`) | live imports | stays |
| `spike-objective/` (7), `spike-certificates/` (8) | 46, 50 KB | D4 / D2 only | throwaway benchmark scripts; excluded from ruff; results recorded in WP records and the register | goes; or pointer (one summary file naming results and commits) |
| `spike-container-platform/` (1) | 3 KB | D2 | report | goes; or stays |

Three code comments point at notes that do not exist in the tree (`superpowers/notes/k3-cubesat.md` in `tests/test_case.py`;
`spike-soft-fit/` and `spike-ggp-fit/report.md` in `derivation/PROOF_MAP_FINDINGS.md`): drift to close in the build stage.

## 5. `work-packages/` classes (52.3 MB, 780 files; per-entry sizes in `work-packages-entries.txt`)

| Class | Entries | Size, files | Readers | Options |
|---|---|---|---|---|
| Decision records | 42 `WP*-decisions.md` | 546 KB, 42 | `paper/myst.yml`, notes, tests cite `WP10-decisions.md` | protected, stays |
| Driver log | `driver-log.md` | 204 KB | | protected, stays |
| Process documents | `README.md`, `PM-BRIEF.md` (78 KB), `release-candidate.md`, `release-punch-list.md` (read by `tests/test_site.py`), `deliverables-grid.md`, `parallel-board.md`, `supervisor-review-list.md`, `status-report-template.md` | about 300 KB, 8 | CLAUDE.md, tests | stays |
| Contract | `interface-contract.md`, `.toml` | 45 KB, 2 | test, scripts | protected, stays |
| Scopes of work | 44 `*scope-of-work.md` / `*-scope.md` | 904 KB, 44 | W only | stays; or pointer (one index file) |
| Reviews (text) | 35 `WP*-review.md`, `WP10-claims-review.md` (564 KB) and `WP10-vocabulary-review.md` (536 KB) among them | 2.1 MB, 35 | `WP10-vocabulary-review.md` read by `vocabulary_baseline.toml`; `WP23-review.md` by `model_v2/coverage.py` | stays |
| Inventories and cut lists | `WP25-inventory.md`, `WP25-5-inventory.md`, `WP28-inventory.md`, `WP28-cut-list.md` | 520 KB | W only | stays; or goes (the deleted rows are in git; the current tidiness record is WP40) |
| Review screenshots | `WP26-review`, `WP27-review`, `WP28-review`, `WP29-review`, `WP30-review`, `WP32-review`, `WP33-review`, `WP35-review`, `WP37-review`: 262 images and `review.md`, `readings.md`, `measure_install.py` files | about 40 MB | only the review md that cite them; one claims-register row cites `WP33-review`; `paper/length_ledger.toml` cites `WP29-review` | each directory: stays; moves out of the tree (a release asset or a branch/tag, named by pointer); goes (the review md keeps the finding); pointer |
| Round outputs read by code | `WP23-rounds/spikes/spike-D-*`, `spike-D2-*` (economics scripts), `WP30-rounds/cost-ladders.md` and `appendix-c-leaves-out.md`, `WP35-rounds/spike-h/` (results.json, hypothesis.md), `WP37-rounds/trace.md`, `WP10-reading-pass.md` | about 200 KB | tests and generators read these paths | stays |
| Other round outputs | rest of `WP23-rounds` (467 KB), `WP30-rounds` (3.8 MB, 35 images), `WP35-rounds` (1.0 MB), `WP36-rounds`, `WP37-rounds` (191 KB, 8 files incl. 0.9 MB draft shot), `WP39-rounds` | about 6 MB | W; some register rows | stays; or goes; screenshots within are the same choice as the review screenshots |
| Reader runs and triage | `WP28-inventory/` (122 md: briefs and 151 reader runs), `WP28-retest/` (29), `WP31-readout/` and `WP31-task-readers/`, `WP19-cold-reads-*`, `WP26-view-editor-feedback/` (31 images, 1.1 MB), `WP33-wayfinding/`, `external-assessment-2026-11-09/`, `WP10-cold-reads-triage.md` | about 2.6 MB | W only | stays (they are the record of the user tests); or goes, keeping the triage and readout md; or pointer |
| Verbatim cell returns | `WP32-cells/` (18 files, excluded from ruff) | 124 KB | `pyproject.toml`, register | stays |
| Held-out | `WP11-*` | | | protected, not described |
| Misc evidence | `swap-evidence.md` (195 KB, read by 3 code files and `tests/test_cubesat_model.py`), `external-review-2026-11.md`, `WP26-model-changes.md`, `WP29-placement-proposal.md`, `WP34-readout.md`, `WP30-build-notes.md` (read by `definitions.py`) | about 400 KB | per file | stays |

If screenshots leave the tree, the review markdown that embeds them by relative path gets a one-line pointer so no link
dangles; `tests/test_site.py` and the register tests do not read images in `work-packages/` (checked above).

## 6. Other file classes

| Class | Size, files | What it does | Options |
|---|---|---|---|
| `examples/adcs/data/*.csv` (legacy v1 and cubesat v1) | 0.81 MB, 5 + 2 sensitivity | v1 data cited by the experiment ledger and legacy oracle; the ledger hashes bytes | stays (hashed); or pointer after the ledger decision |
| `examples/adcs/data/v2/` | 2.1 MB, 4 | the data of record | protected |
| `examples/adcs/experiments/` | 0.8 MB, 22 (ledger, oracle, probes, reports) | the experiment ledger and its runner | stays |
| `examples/adcs/model_v2/` | 0.5 MB, 16 (SysML v2, views PNG/SVG/PUML) | the system model the paper draws from | stays |
| `examples/adcs/*.py` (`case.py` 92 KB, `adcs_sim.py`, `generate_dataset.py`, `k_terms.py`, `noise_injection.py`, `design_space.py`, `make_check_designs.py`) | small | case study code; `design_space.py` read only by `definitions.py` and the ledger; `extended_design_space.sysml` by `case-model.md` and a test | stays |
| `paper/BROWSER_NOTES.md`, `paper/container/`, `paper/stability_extra.*`, `paper/reading_pass.yaml` | small | paper build and reproducibility record (tests read them) | protected |
| `scripts/wp30_cost_ladders.py` | 12 KB | regenerates `WP30-rounds/cost-ladders.md`; named by two tests | stays |
| `tests/data`, `tests/fixtures/user-tests/` | 0.5 MB (3 files), 44 KB (7) | reference arrays; the user-test fixtures with `ANSWERS.md` for the pump-table tests (not WP11's key) | stays |
| Tracked scratch | none found: no `scratch`, `tmp`, `HANDOVER`, `.bak` file is tracked; untracked ignored dirs exist locally (`.claude/`, `_stage/`, `build/`, caches) | | nothing to do; `.gitignore` covers them |
| Git pack | 100.6 MiB | history | stays; (history rewrite is a separate decision, not proposed) |

## 7. Draft Layout list (README), one line per entry, for a stranger

```
## Layout

- `src/hyperbolic_trade_space/`: the Python package (fit a frontier, read its tensions).
- `docs/`: the user guide and API reference; built into the docs site. `docs/superpowers/` holds the working notes the
  checks apply (conventions, notation, source lists).
- `paper/`: the paper as two notebooks and what rebuilds them; `site/` is the root page that links docs and paper.
- `examples/adcs/`: the cubesat attitude-control case study the paper uses: model, data, experiments, system model.
- `derivation/`: the proofs of the method's results as SymPy scripts, one per lemma.
- `tests/`: the test suite; `scripts/`: build and check tools.
- `claims_register.toml`: each claim the paper and docs make and what backs it.
- `glossary.yaml`: the terms, one name per object; `history.yaml`: the release history.
- `CHANGELOG.md`: what changed, by work package.
- `work-packages/`: the build's record (scopes, reviews, decisions, screenshots of the reviews); not needed to use the method.
- `CLAUDE.md`: conventions for contributors working with Claude Code.
- `mkdocs.yml`, `Dockerfile`, `pyproject.toml`, `uv.lock`: build and environment files.
```

A top-level reader meets 12 lines instead of 7; with the screenshots moved or pointed, `work-packages/` becomes a 7 MB
folder of text and the line "not needed to use the method" is true of the checkout's size as well as its purpose.

## 8. Shape of the options (for the decision stage)

1. Screenshots: 324 images, 44.7 MB, 69 % of the checkout, read by no test: stays / moves out of the tree (named
   location) / goes / pointer. Largest single decision.
2. Review and round directories (nine review dirs, six round dirs): the code-read files stay in every variant; the
   rest is the same four options per directory.
3. Reader runs (WP28 inventory and retest, WP31, WP19 cold reads): record of the user tests; four options, 2.6 MB.
4. Notes: 8 convention notes plus 6 live ones stay; 5 build notes, 3 outline/search notes and 2 spike folders have no
   code reader (goes / moves into `work-packages/`).
5. Superseded inventories (WP25, WP25-5, WP28; 520 KB): stays / goes.
6. Pack (100.6 MiB): stays; a rewrite is separate and changes hashes the records quote.
7. README Layout list and a short `work-packages/README.md` header saying what is in the folder: redraft per section 7.
8. Drift to close in the build stage: three dangling note paths in code comments; the Layout list omissions.

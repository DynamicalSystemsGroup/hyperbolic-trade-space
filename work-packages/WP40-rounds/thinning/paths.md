# WP40 path list (D-4), made at the build's start head H0 = `94cb6a1`

Made by `git grep` over every tracked file except `WP11-*` (never opened). Old paths and names searched: the moved
items and removed files of `moves.md`, `spike-*` (the ruff glob), the three drift names (`k3-cubesat`, `spike-soft-fit`,
`spike-ggp-fit`), and every png/jpg under `work-packages/`.

## 1. Images

- No code, test, script, config, claims-register row, docs page or notebook reads a png/jpg under `work-packages/`
  (greps of `tests/`, `scripts/`, `paper/*.py`, `claims_register.toml`, `docs/`, `mkdocs.yml`, `paper/*.yaml`, `paper/*.toml`). R-1 holds with no
  image kept; 333 images (the readout counted 324 at 1d741d2; WP39 and later added nine), none under `WP11-*`.
- `claims_register.toml` and `paper/length_ledger.toml` cite review directories (`WP33-review`, `WP29-review`) as
  evidence paths; the directories stay (text remains), only their images go.
- Files that embed or list a removed image and so take the pointer line at D-1 (decision records, scopes of work and the
  four removed inventories excluded):

  - `work-packages/WP19-cold-reads-fig1/cold-read-2-riders.md`
  - `work-packages/WP23-review.md`
  - `work-packages/WP23-rounds/gate/README.md`
  - `work-packages/WP23-rounds/round-1/README.md`
  - `work-packages/WP23-rounds/round-1/cold-reads.md`
  - `work-packages/WP23-rounds/round-3/INTENT.md`
  - `work-packages/WP23-rounds/round-3/cold-reads.md`
  - `work-packages/WP23-rounds/round-4/INTENT.md`
  - `work-packages/WP23-rounds/round-4/README.md`
  - `work-packages/WP26-review.md`
  - `work-packages/WP26-view-editor-feedback.md`
  - `work-packages/WP27-acceptance-review.md`
  - `work-packages/WP27-review.md`
  - `work-packages/WP28-review/two-panel/readings.md`
  - `work-packages/WP29-review.md`
  - `work-packages/WP29-review/reads2/README.md`
  - `work-packages/WP30-review/review.md`
  - `work-packages/WP30-rounds/chooseK/cold-reads/cold-read-figs-6-7-8.md`
  - `work-packages/WP30-rounds/paperwp30/figure-loop.md`
  - `work-packages/WP33-review.md`
  - `work-packages/WP35-review.md`
  - `work-packages/WP35-review/reads/read-P9.md`
  - `work-packages/WP35-review/reads/read-R13.md`
  - `work-packages/WP37-review.md`
  - `work-packages/supervisor-review-list.md`
  - `work-packages/swap-evidence.md`

  Directories whose images no file names, so a governing file takes the directory form of the line: `WP26-review/`,
  `WP27-review/`, `WP32-review/`, `WP37-review/` (each by its `WPn-review.md`), `WP28-review/` and `WP33-review/` (by
  `WP28-review.md`, `WP33-review.md`), `WP30-rounds/{d2order,reqcost,s6fix,viewsp,chooseK/screenshots}` (by
  `WP30-review/review.md` and `WP30-rounds/chooseK/figure-review.md`), `WP35-rounds/build-shots/` (by
  `WP35-review.md`), `WP36-rounds/` (by `WP36-rounds/spike/readout.md`).

## 2. Moved or removed text paths

### 2a. Editable hits (count: 25 lines in 18 files, outside the notebook and the exempt classes)

| File:line | Names | Action |
|---|---|---|
| `docs/superpowers/notes/paper-prior-art-sources.md:47,79` | `paper-outline-v1-baseline.md` | path to `work-packages/outlines/` |
| `docs/superpowers/notes/paper-outline-v1-baseline.md:1`, `paper-outline-v2-search.md:3` | each other, bare sibling names | none: both move to `outlines/` and the bare names still resolve |
| `docs/superpowers/notes/paper-sources/limitations.md:143,160` | `spike-objective/` | path to `work-packages/spikes/` |
| `docs/superpowers/notes/paper-sources/method.md:915` | `spike-objective/` | path to `work-packages/spikes/` |
| `docs/superpowers/notes/spike-certificates/README.md:4`, `spike-objective/README.md:3` | their own folder | path to the new folder |
| `docs/superpowers/specs/2026-11-07-posynomial-invariant-form-design.md:379` | `adcs-port.md` | path to `work-packages/build-notes/` |
| `examples/adcs/experiments/probes/probe-record.md:7` | `opensysml-usage.md` | path to `work-packages/build-notes/` |
| `paper/container/README.md:6`, `RECORD.md:6` | `spike-container-platform/report.md` | path to `work-packages/spikes/` |
| `pyproject.toml:51` | the glob `docs/superpowers/notes/spike-*` | one line: exact entries for the spike folders that remain under `docs/superpowers/notes/` (`spike-horopca`, `spike-sysml-diagrams`, `spike-facet-refit`, `spike-figure1`) and `work-packages/spikes/` |
| `work-packages/PM-BRIEF.md:121,516,534,669,670` and 454 (`k3-cubesat.md`, history) | `adcs-port`, `WP28-inventory.md`, `paper-outline-v1-baseline.md`, `search-prior-art.md` | moved names get the new path; mentions of the removed `WP28-inventory.md` are history rows (see 2c) |
| `work-packages/README.md:119,120` | `system-model-tidy.md`, `paper-outline-v2-search.md` | path to the new folder |
| `work-packages/parallel-board.md:139`, `supervisor-review-list.md:98` | `view-editor-harness.md` | path to `work-packages/build-notes/` |
| `work-packages/WP8b-release-checklist.md:77` | `WP25-5-inventory.md` (removed) | history row, see 2c |

### 2b. Notebook and generated text (D-8, not in this build; see `notebook-cells.md`)

`paper/supporting_material.ipynb`: nine hits (lines 12547, 12555, 12571, 12611, 12650, 12651, 12653, 12658, 12664 at
H0), all in the Appendix E table generated from `docs/superpowers/notes/abstraction-gaps.md` (lines 33, 34, 36, 41 of
the note). The note and the cells change together in D-8; this build leaves both.

### 2c. Exempt classes and history rows (counted, not edited)

Exempt by R-3 (decision records, scopes of work, reviews, `driver-log.md`, the WP40 records, the two named borderline
files `WP27-acceptance-review.md` and `external-review-2026-11.md`, and the four inventories removed in D-2): 513 hit
lines in 39 files at H0 (361 of them in the two inventories `WP25-inventory.md` and `WP25-5-inventory.md`, which go).
Keyed by `moves.md`. History rows in process documents that name a removed file (`WP28-inventory.md`,
`WP25-5-inventory.md`) as something that existed: left as written and counted as residue by the R-3 report.

## 3. Drift comments (D-7)

`tests/test_case.py:5` (`k3-cubesat.md`), `derivation/PROOF_MAP_FINDINGS.md:226` and `:281` (`spike-ggp-fit/report.md`,
`spike-soft-fit/`), `derivation/lemma_16_soft_fit_alternation.py:47` (`spike-ggp-fit`). Other `k3-cubesat` mentions name
a history commit (`method.md:884,965`, `spike-certificates/README.md:106`, `run_cubesat.py:20`) or sit in
`swap-evidence.md`, `external-review-2026-11.md`, `PM-BRIEF.md:454`; each says "deleted; last version at" or is a
quoted record; left as written.

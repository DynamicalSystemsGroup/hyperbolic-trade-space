# WP73 D-3: every reference from outside the record into a removed path, and what was done with it

The archive commit is `4f81a4ea`; the removed set is what `work-packages/` held there and the tree no longer does (521
files; eight more moved with `git mv`). The scan is `tests/test_index.py::test_nothing_outside_the_record_names_a_removed_path`:
every tracked text file outside `work-packages/`, every bare `work-packages/<path>` and every `blob/main/` or
`tree/main/` URL into the record, against the files held by any commit the index names. Three dispositions:

- **moved**: a test or a generator reads the file, so the file moved to a place of the current state and the reader
  names the new path (29 references in 15 places; the files are listed in `INDEX.md`, "Moved by WP73");
- **repointed**: a citation, in prose, a comment, a docstring or a TOML string, carries the commit the file is read at
  (118 references in 43 places): in Markdown the path keeps its name and gains
  `(git show 4f81a4ea:<path>)`, the form the records already use; in code, tests, TOML, YAML and the workflow comment
  the path becomes `4f81a4ea:<path>`; a URL becomes a blob URL at the archive commit;
- **dropped**: the mention did no work (1).

`notes/` is outside this package; its seven citations were repointed in the same form and nothing else in a note
changed. Inside the record, the two release checklists' citation of `WP65-design/specification.md` and the G8
section of `WP67-rounds/record.md` (the eighty captures) gained the same form.

## Moved

| File | Reference | What was done | Count |
|---|---|---|---|
| `tests/test_wp45_examples.py` | work-packages/WP45-rounds/<case>/test-record.md (read) | repointed to tests/data/wp45/<case>/test-record.md (moved with git mv) | 1 |
| `examples/amniote/run.py` | work-packages/WP45-rounds/amniote/test-record.md | names the new path | 1 |
| `examples/perovskite/run.py` | work-packages/WP45-rounds/perovskite/test-record.md | names the new path | 1 |
| `notes/paper-prior-art-sources.md` | work-packages/WP45-rounds/ | names tests/data/wp45/ | 1 |
| `tests/test_paper.py` | work-packages/WP57-rounds/assumptions-queue.md (read) | repointed to tests/data/wp57/assumptions-queue.md (moved); the docstring names it | 2 |
| `scripts/wp30_cost_ladders.py` | work-packages/WP23-rounds/spikes/spike-D-cubesat-economics/economics.py (read), work-packages/WP30-rounds/cost-ladder... | repointed to examples/adcs/spikes/economics.py and examples/adcs/spikes/cost-ladders.md (both moved); the docstring names the new path | 3 |
| `tests/test_wp30_cost_ladders.py` | work-packages/WP23-rounds/spikes/spike-D2-prices-2026/economics2026.py (read) | repointed to examples/adcs/spikes/economics2026.py (moved) | 1 |
| `examples/adcs/spikes/economics.py` | its own data root, four levels up from the old place | the root is three levels up from the new place; its usage line names the new path | 2 |
| `paper/generate_reading_pass.py` | work-packages/WP10-reading-pass.md (read) | repointed to paper/data/WP10-reading-pass.md (moved); the docstring and the generated header name it | 3 |
| `paper/reading_pass.yaml` | work-packages/WP10-reading-pass.md (the header comment) | names paper/data/WP10-reading-pass.md, as the generator now writes | 1 |
| `claims_register.toml` | file = "work-packages/WP45-rounds/perovskite/test-record.md" | file = "tests/data/wp45/perovskite/test-record.md" | 4 |
| `claims_register.toml` | file = "work-packages/WP45-rounds/amniote/test-record.md" | file = "tests/data/wp45/amniote/test-record.md" | 4 |
| `claims_register.toml` | file = "work-packages/WP45-rounds/wheat/test-record.md" | file = "tests/data/wp45/wheat/test-record.md" | 3 |
| `paper/length_ledger.toml` | (work-packages/WP57-rounds/assumptions-queue.md, WP57d) | (tests/data/wp57/assumptions-queue.md, WP57d) | 1 |
| `examples/adcs/spikes/economics.py` | uv run python work-packages/WP23-rounds/spikes/spike-D-cubesat-economics/economics.py | uv run python examples/adcs/spikes/economics.py | 1 |

## Repointed

| File | Reference | What was done | Count |
|---|---|---|---|
| `.github/workflows/issue-admissibility.yml` | work-packages/WP47-rounds/checks.md | `4f81a4ea:<path>`, the form `git show` takes | 1 |
| `tests/test_admissibility.py` | work-packages/WP47-rounds/checks.md | `4f81a4ea:<path>`, the form `git show` takes | 1 |
| `tests/test_release_checks.py` | work-packages/WP47-rounds/checks.md | `4f81a4ea:<path>`, the form `git show` takes | 1 |
| `examples/adcs/experiments/definitions.py` | work-packages/WP30-build-notes.md | `4f81a4ea:<path>`, the form `git show` takes | 1 |
| `examples/adcs/experiments/sensitivity.py` | work-packages/swap-evidence.md | `4f81a4ea:<path>`, the form `git show` takes | 1 |
| `tests/test_v2_data.py` | work-packages/swap-evidence.md | `4f81a4ea:<path>`, the form `git show` takes | 1 |
| `examples/adcs/model_v2/coverage.py` | work-packages/WP23-review.md | `4f81a4ea:<path>`, the form `git show` takes | 1 |
| `examples/amniote/variants.py` | work-packages/WP59-rounds/amniote.md | `4f81a4ea:<path>`, the form `git show` takes | 1 |
| `scripts/vocabulary_baseline.toml` | work-packages/WP10-vocabulary-review.md | `4f81a4ea:<path>`, the form `git show` takes | 1 |
| `tests/test_noise_ridge.py` | work-packages/WP23-rounds/spikes/spike-E-noise/check2_noise_is_ridge.py | `4f81a4ea:<path>`, the form `git show` takes | 1 |
| `tests/test_paper.py` | work-packages/WP56-rounds/moved-to-appendix.md | `4f81a4ea:<path>`, the form `git show` takes | 1 |
| `paper/length_ledger.toml` | work-packages/WP19-figure-review.md | `4f81a4ea:<path>`, the form `git show` takes | 1 |
| `paper/length_ledger.toml` | work-packages/WP29-review/P9-P10-triage.md | `4f81a4ea:<path>`, the form `git show` takes | 1 |
| `paper/length_ledger.toml` | work-packages/WP33-scope-of-work.md | `4f81a4ea:<path>`, the form `git show` takes | 1 |
| `paper/length_ledger.toml` | work-packages/WP35-amendment-1-scope.md | `4f81a4ea:<path>`, the form `git show` takes | 1 |
| `paper/length_ledger.toml` | work-packages/WP35-review.md | `4f81a4ea:<path>`, the form `git show` takes | 1 |
| `paper/length_ledger.toml` | work-packages/WP39-scope-of-work.md | `4f81a4ea:<path>`, the form `git show` takes | 1 |
| `paper/length_ledger.toml` | work-packages/WP57-rounds/map.md | `4f81a4ea:<path>`, the form `git show` takes | 1 |
| `tests/test_cubesat_model.py` | work-packages/swap-evidence.md | `4f81a4ea:<path>`, the form `git show` takes | 2 |
| `claims_register.toml` | work-packages/WP51-rounds/synthetic-case.md | `4f81a4ea:<path>`, the form `git show` takes | 7 |
| `claims_register.toml` | work-packages/WP54-review.md | `4f81a4ea:<path>`, the form `git show` takes | 13 |
| `claims_register.toml` | work-packages/WP55-review.md | `4f81a4ea:<path>`, the form `git show` takes | 40 |
| `claims_register.toml` | work-packages/WP56-review.md | `4f81a4ea:<path>`, the form `git show` takes | 1 |
| `claims_register.toml` | work-packages/WP56-rounds/figures/record.md | `4f81a4ea:<path>`, the form `git show` takes | 5 |
| `claims_register.toml` | work-packages/WP60-rounds/amniote.md | `4f81a4ea:<path>`, the form `git show` takes | 14 |
| `CHANGELOG.md` | `work-packages/swap-evidence.md`, | a blob URL at the archive commit | 1 |
| `examples/adcs/experiments/reports/change-register.md` | `work-packages/WP23-rounds/gate/README.md`) | the path keeps its name and gains `git show 4f81a4ea:<path>` | 1 |
| `examples/adcs/experiments/reports/change-register.md` | `work-packages/swap-evidence.md`, "WP23 close-out") | the path keeps its name and gains `git show 4f81a4ea:<path>` | 1 |
| `examples/adcs/experiments/reports/change-register.md` | \| CR-2 \| `torque_saturated_frac` differs from the frozen file beyond its saturation tolerance in 3 primary rows (la... | the path keeps its name and gains `git show 4f81a4ea:<path>` | 1 |
| `paper/container/RECORD.md` | five ledger entries, is `work-packages/WP23-rounds/gate/README.md`; | the path keeps its name and gains `git show 4f81a4ea:<path>` | 1 |
| `paper/container/RECORD.md` | is the gate section of `work-packages/swap-evidence.md`. | the path keeps its name and gains `git show 4f81a4ea:<path>` | 1 |
| `paper/container/RECORD.md` | --out work-packages/WP23-rounds/gate` \| 26 s \| | `4f81a4ea:<path>`, the form `git show` takes | 1 |
| `paper/container/RECORD.md` | new (D-9, `work-packages/swap-evidence.md`, the gate section) | the path keeps its name and gains `git show 4f81a4ea:<path>` | 1 |
| `paper/container/RECORD.md` | (`work-packages/swap-evidence.md` part 6, dispositions in part 7) | the path keeps its name and gains `git show 4f81a4ea:<path>` | 1 |
| `paper/container/RECORD.md` | \| `work-packages/WP30-rounds/data-gate/k-record.txt` \| | the path keeps its name and gains `git show 4f81a4ea:<path>` | 1 |
| `paper/supporting_material.ipynb` | blob/main/work-packages/WP57c-review.md | a blob URL at the archive commit | 1 |
| `notes/directions/README.md` | `work-packages/WP72-rounds/readout.md` (moves to this folder at landing) | the path keeps its name and gains `git show 4f81a4ea:<path>` | 1 |
| `notes/directions/candidates.md` | spike (`work-packages/WP72-rounds/readout.md`) | the path keeps its name and gains `git show 4f81a4ea:<path>` | 1 |
| `notes/directions/wp43-kernel-direction.md` | (the scripts are in history at d0a97cd) | the path gains the `git show <commit>:<path>` of the commit the index names | 1 |
| `notes/directions/wp50-persistent-homology.md` | changes no file outside `work-packages/WP50-rounds/`. | the path gains the `git show <commit>:<path>` of the commit the index names | 1 |
| `notes/directions/wp52-governance-lineage.md` | Nothing was written outside `work-packages/WP52-rounds/spike/`; | the path gains the `git show <commit>:<path>` of the commit the index names | 1 |
| `notes/residual-review.md` | One table per reader slot, `work-packages/WP38-flags/<slot>.md`. | the path gains the `git show <commit>:<path>` of the commit the index names | 1 |
| `notes/residual-review.md` | one form per surface, `work-packages/WP38-confirmations/<slot>.md`: | the path gains the `git show <commit>:<path>` of the commit the index names | 1 |

## Dropped

| File | Reference | What was done | Count |
|---|---|---|---|
| `tests/test_check_script.py` | "work-packages/WP20-review.md" | the sample of an unmapped path is now `work-packages/INDEX.md`; the mention did no work | 1 |

## Kept in place because something outside the record reads it

Named in the package's row of `INDEX.md` with its reader: `WP9-review.md`, `external-assessment-2026-11-09/`,
`spikes/spike-certificates/`, `spikes/spike-objective/` (the paper's gaps table links them through
`docs/superpowers/notes/abstraction-gaps.md` and `paper_common.link_paths`); `WP17-scope-of-work.md`,
`WP31-readout.md`, `WP35-rounds/spike/readout.md`, `WP36-rounds/spike/readout.md`, `WP41-rounds/spike/`,
`WP46-rounds/`, `WP56-rounds/figures/tension-values.txt` and `ternary-values.txt`, `WP59-rounds/wheat.md`
(`file:` backings of the claims register); `WP35-rounds/spike-h/` (`paper/generate_repro.py`, `tests/test_paper.py`,
the register); `WP37-rounds/trace.md` (`scripts/history_record.py`, `tests/test_site.py`, the register);
`WP56-rounds/ternary/` (`examples/adcs/spikes/fleet_performance.py` and `.json`, `examples/adcs/model_v2/stakeholders.sysml`,
the supporting material's link). Kept by a decision rather than a reader: `build-notes/view-editor-harness.md` (his
word at WP25-4), `supervisor-tasks.md`, `supervisor-walkthrough.md` and `reviewers-guide/` (WP62's decision: until
WP58 refreshes the guide), `deliverables-grid.md`, `status-report-template.md` and `parallel-board.md` (read by
`release-candidate.md`, the software checklist's D5 and `PM-BRIEF.md`), `review/deferred.md` (his rulings held until
the prose review completes). In flight, untouched: WP8b, WP11, WP12, WP21, WP25 (by the index's state), WP58, WP73.

# WP25 — Review report (second instance, unit A in progress)

| | |
|---|---|
| **Scope of work** | `work-packages/WP25-2-scope-of-work.md` (approved 2026-11-10, 07:00, by the driver under the mandate; `WP25-decisions.md`, "Instance 2") |
| **Work reviewed** | `dev` a9e23b2 and the instance's commits: the inventory (D-1), the deletion commit "WP25: 31 files deleted (second instance, unit A)" (D-2), the drift fixes (D-4), this report |
| **Written by** | unit A, 2026-11-10; the checks below ran in its worktree at the head of the unit. Unit B (after WP24's last push and the paper unit) completes "Drift", "Gaps" and "Checks", and the reviewer reruns R-1 to R-10 |

Rewritten per instance (A3). The first instance's report is at `f9573fd`; the deleted files' last versions are at `a9e23b2`
(`git show a9e23b2:<path>`).

## Checks (D-5, G4), unit A

| Check | Command | Result |
|---|---|---|
| Docs build, the repo's | `uv run python scripts/assemble_site.py --out <tmp> --paper placeholder` | `assembled site in <tmp>`, exit 0 |
| Fast suite | `uv run pytest -q -m "not slow" -n auto` | `1744 passed, 16 skipped, 1 xfailed`; no failure at the head of the unit |
| Docs and register tests | `uv run pytest -q tests/test_claims_register.py tests/test_docs.py tests/test_site.py` | `111 passed` (a first reword of `getting-started.md` broke register row C173, which pins "their ratios are the elasticities between the contending"; reworded to keep the fragment and add "with a minus sign") |
| Vocabulary guard | `uv run python scripts/check_vocabulary.py` | `70 new violation(s), 0 known`; 70 at a9e23b2 before the unit (diffed); a first wording of the overview fix added one stem hit, reworded |
| Lock | `uv lock --check` | `Resolved 178 packages`, exit 0 |
| Deletion commit (R-4) | `git show --stat <hash> \| tail -1`; `git show --format=%B -s <hash> \| grep -c '^work-packages/'` | `31 files changed, 1157 deletions(-)`; 31 |
| Nothing live names a deleted path (R-3) | `for f in $(git diff --name-only --diff-filter=D a9e23b2..HEAD); do git grep -l -F "$f" -- . ':!work-packages/WP25-*'; done \| wc -l` | 0. Basename hits outside the records are same-named files in other places, listed per row in the inventory (`examples/adcs/model_v2/views/`, the diagnostic pair's temporary output) |
| Contract and tests (R-2) | `git grep -n -F <path or basename> -- work-packages/interface-contract.md work-packages/interface-contract.toml tests/test_interface_contract.py`, per delete row | 0 for all 31 rows, both forms (the inventory's first section) |
| Inventory (R-1) | the A2 command diffed against the inventory's rows; `grep -ciE "undecided\|tbd\|\?\?" work-packages/WP25-inventory.md` | 198 rows, no difference; 0 |
| Untouched (R-7) | `git diff --stat a9e23b2..HEAD -- paper src`; `--diff-filter=R` | empty; empty. `derivation/` has one text edit (below), no script |
| Attribution (R-10) | `git log --format=%B a9e23b2..HEAD \| grep -ciE "co-authored-by\|generated"` | 0 |

## Drift (D-3, G2): the first instance's 19 rows, and five found since

| # | Row | State | Where |
|---|---|---|---|
| 1 | `getting-started.md` L39-40, the grey band marks points within 0.5 | fixed | "the grey strip under the line is the region up to 0.5 below the frontier in log V" (`plot_log_plane` shades the strip and does not grey the points) |
| 2 | `getting-started.md` L61-62, ratios are the elasticities | fixed | "with a minus sign" (`elasticities[j, k] = -w_k / w_j`); register row C173's fragment kept |
| 3 | `overview.md` L13-14, non-negligible weight contends | fixed | positive weight in the exact-maximum fit (tau = inf); a small weight at the fit temperature is weaker participation (glossary: contending set) |
| 4-6 | `fitting.md` L39-41 (band width), L59 (re-select tau), L99-100 (mean slack picks K) | routed: unit B | the page is on WP24's D-11 list and carries the word being renamed (17 occurrences); edited after WP24's last push |
| 7-9 | `chart.md` L102 (five plots), L60 (soft maximum over terms), L41 and L55-56 (band width) | routed: unit B | same: WP24 D-11 page (4 occurrences) |
| 10 | `chart.md` L112, the plots draw every facet | routed: WP24 docs push | WP24 rewrites the sentence |
| 11 | `termination.md` L47, `iteration_cap` warns | closed | 4e39097: the page says `fit` warns for `uncertified` and `guard_stop`, and `iteration_cap` has its own rule |
| 12 | `termination.md` L49-53, a soft fit can end `uncertified` | routed: unit B | WP24 D-11 page (18 occurrences) |
| 13-14 | `theory.md` L21-23, two sentences | routed: WP24 docs push | WP24 rewrites the sentences |
| 15-17 | `glossary.yaml` mean slack, termination statuses, assignment | routed: WP24 docs push | `glossary.yaml` is WP24's |
| 18 | `README.md` status line | closed | ef281d1 |
| 19 | `derivation/PROOF_MAP_FINDINGS.md` L226, L281, citations of deleted spikes | fixed | "(deleted; last version at 73c5bff)"; text only, no script, no recorded value |
| N-a | `examples/adcs/model_v2/views/coverage.csv` names the decision-element column by the enum type (`WheelClass`) | routed: PM | WP23 is accepted (db59365); the generator is `examples/adcs/model_v2/`; options: leave the caption's bridge as the intended reading, or rename the column in the generator |
| N-b | `paper/length_ledger.toml` row at L557, "the earlier radius was a typed constant" | routed: the paper stream | its file |
| N-c | `tests/test_narrative.py` `RENAMED` map | closed | 9b1152e (WP24 push 2 dropped the map; `grep -n RENAMED tests/test_narrative.py` is empty) |
| N-d | the six `abstraction-gaps.md` rows read against the data | routed: unit B | needs the measurement recipes M3 to M5 rerun on `data/v2/` (they name the v1 data paths and the old "stock" regime); the note carries 13 occurrences of the word WP24 renames |
| N-e | the vocabulary count after A5 | closed | 70 at a9e23b2 and 70 at the head of the unit |

## Gaps (D-4, G3): the nine rows re-checked

The contract's 124 pinned names grepped over `docs/*.md docs/user-guide/*.md`: 37 absent now (33 at the first instance); the renames of WP24 push 1 account for the difference (`assign_cells`, `cell_`,
`cell_labels`, `term_gap`, `term_objective`, `term_share_`, `single_term_termination` are new names no page uses yet). `plot_ternary` and
`ternary_marker_values`: 0 hits in `docs/api.md` and `chart.md` (4 in `examples.md`). No fill in unit A (every page is on
WP24's list).

| Row | State |
|---|---|
| `coordinates` submodule and its four functions | open; unit B (api page or Chart page, after WP24) |
| `solvers` names (19) | open; unit B (a directive on the API reference page) |
| `tensions` report fields `association_kind`, `contending_exponents`, `novelty_score`; residuals | open; unit B (Tensions and Termination pages) |
| `training_log_v_` | open; unit B (Fitting page) |
| submodule names `tuning`, `predictive`, `preconditioning` | dropped (stands): the objects are documented through the top-level names |
| `plot_ternary`, `ternary_marker_values` in `docs/api.md` and `chart.md` | open; unit B |
| `spike-ternary/report.md` | scheduled: WP24 points `claims_register.toml` L32 and `glossary.yaml` L515, L535 at `plot_ternary`'s Notes; unit B deletes the report |
| the three spikes (46 files) | decided 2026-11-10 07:00: the paper unit re-points the citations; unit B then deletes the 26 `.txt` and `.csv` outputs (rows held in the inventory); the 20 READMEs and scripts stay |
| `streams/P10-review.md` | held: WP10's acceptance (WP10 is a working draft) |

## Left for unit B

The 26 spike outputs; `spike-ternary/report.md`; `scripts/rename_facet.py`, `tests/test_rename_facet.py` and their line in
`scripts/check.py`; drift rows 4 to 9, 12 and the routed ones after WP24 (10, 13 to 17); row N-d; gap rows 1 to 4, 6; the
final R-1 to R-10 rerun.

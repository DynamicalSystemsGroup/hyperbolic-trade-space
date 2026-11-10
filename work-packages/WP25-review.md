# WP25 — Review report (second instance, units A and B)

| | |
|---|---|
| **Scope of work** | `work-packages/WP25-2-scope-of-work.md` (approved 2026-11-10, 07:00, by the driver under the mandate; `WP25-decisions.md`, "Instance 2") |
| **Work reviewed** | `dev` a9e23b2 and the instance's commits: the inventory (D-1), the deletion commit "WP25: 31 files deleted (second instance, unit A)" (D-2), the drift fixes (D-4), this report |
| **Written by** | unit A, 2026-11-10; the checks below ran in its worktree at the head of the unit. Unit B (2026-11-10, after WP24's last push and the paper unit) completed "Drift", "Gaps" and "Checks" (section "Unit B" below); the reviewer reruns R-1 to R-10 |

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
| 4-6 | `fitting.md` L39-41 (band width), L59 (re-select tau), L99-100 (mean slack picks K) | fixed | unit B, 2132d36: "the designs with |log V| below 1/tau"; "Hold tau fixed across numbers of terms, selected at K = 1"; "`mean_slack_` falls with K by construction, so it cannot choose K alone: add a term only while the resampled exponents stay stable" (register row C402) |
| 7-9 | `chart.md` L102 (five plots), L60 (soft maximum over terms), L41 and L55-56 (band width) | fixed / closed | 7 fixed in 2132d36 ("six plots", a bullet for `plot_ternary` and `ternary_marker_values`, register row C400); 8 closed by WP24 ("the maximum over terms at the default `term_temperature=inf`", row C295); 9: the caption (L41) already says "log V from -1/tau to 0"; L55-56 fixed in 2132d36 ("the near-frontier band, |log V| below 1/tau") |
| 10 | `chart.md` L112, the plots draw every facet | closed | WP24: the page says the designs are one colour by default and `color="cell"` colours them by cell, any other string raising `ValueError` |
| 11 | `termination.md` L47, `iteration_cap` warns | closed | 4e39097: the page says `fit` warns for `uncertified` and `guard_stop`, and `iteration_cap` has its own rule |
| 12 | `termination.md` L49-53, a soft fit can end `uncertified` | fixed | unit B, 2132d36: "`uncertified`: as above" in the soft-fit list (solvers.py:658-659); `not_applicable` at tau = inf was already in the status list |
| 13-14 | `theory.md` L21-23, two sentences | closed | WP24: "alternates assigning the designs to terms with a separate convex refit of each term"; "By default (`term_temperature=np.inf`) the package takes the sharp limit ... and the labels drive the refit" |
| 15-17 | `glossary.yaml` mean slack, termination statuses, assignment | closed | WP24: mean slack "falls with K by construction and cannot choose K"; termination status lists "stationary (soft fit only)"; assignment "Only the soft fit (finite term temperature) weighs every term against every design" (glossary.yaml L425, L468, L484) |
| 18 | `README.md` status line | closed | ef281d1 |
| 19 | `derivation/PROOF_MAP_FINDINGS.md` L226, L281, citations of deleted spikes | fixed | "(deleted; last version at 73c5bff)"; text only, no script, no recorded value |
| N-a | `examples/adcs/model_v2/views/coverage.csv` names the decision-element column by the enum type (`WheelClass`) | routed: PM | WP23 is accepted (db59365); the generator is `examples/adcs/model_v2/`; options: leave the caption's bridge as the intended reading, or rename the column in the generator |
| N-b | `paper/length_ledger.toml` row at L557, "the earlier radius was a typed constant" | routed: the paper stream | its file |
| N-c | `tests/test_narrative.py` `RENAMED` map | closed | 9b1152e (WP24 push 2 dropped the map; `grep -n RENAMED tests/test_narrative.py` is empty) |
| N-d | the six `abstraction-gaps.md` rows read against the data | fixed (e1341e0) | M3 and M5 rerun on `data/v2/`: their numbers held (conditioning 7.09 and 0.0170, 9.03 / 9.26 / 0.273 and 9.28 / 0.214 / 10.1, the M5 changes 0.008 / 0.001 and 0.004 / 0.001); the recipes now name `examples/adcs/data/v2/` and the primary and baseline regimes (key `stock`), and M5 states what it measures. The figures taken from `k3-cubesat.md` (G-1, G-7, G-9, G-11 to G-13, G-16) did not match the data of record and were replaced by `k_terms.py`'s output on `data/v2/` (the same as `tests/test_case.py` `RECORD`); see "Unit B" |
| N-e | the vocabulary count after A5 | closed | 70 at a9e23b2 and 70 at the head of the unit |

## Gaps (D-4, G3): the nine rows re-checked

The contract's 124 pinned names grepped over `docs/*.md docs/user-guide/*.md`: 37 absent now (33 at the first instance); the renames of WP24 push 1 account for the difference (`assign_cells`, `cell_`,
`cell_labels`, `term_gap`, `term_objective`, `term_share_`, `single_term_termination` are new names no page uses yet). `plot_ternary` and
`ternary_marker_values`: 0 hits in `docs/api.md` and `chart.md` (4 in `examples.md`). No fill in unit A (every page is on
WP24's list).

| Row | State |
|---|---|
| `coordinates` submodule and its four functions | filled: listed in `docs/api.md` beside the other submodules (2132d36) |
| `solvers` names (19) | dropped with a reason: `docs/api.md` already lists the module and what it holds, and no submodule has a directive on the API reference page (that page renders the nine top-level names); the Theory page and Appendix B describe what the functions compute |
| `tensions` report fields `association_kind`, `contending_exponents`, `novelty_score`; residuals | filled for the fields: `association_kind` and `contending_exponents` on the Tensions page, `sum_residual`, `floor_residual`, `offset_residual` on the Termination page (2132d36). `novelty_score` is a method of the estimator, not a report field; the Prediction page is its reader, unchanged |
| `training_log_v_` | filled: one sentence on the Fitting page beside the chart's attributes (2132d36, register row C401) |
| submodule names `tuning`, `predictive`, `preconditioning` | dropped (stands): the objects are documented through the top-level names |
| `plot_ternary`, `ternary_marker_values` in `docs/api.md` and `chart.md` | filled (2132d36): the plotting list of `api.md`, and a bullet on the Chart page linking the Examples page's figure (no new figure) |
| `spike-ternary/report.md` | held: `glossary.yaml` no longer cites it, but `claims_register.toml` C001 (note) and `docs/superpowers/notes/claims-review.md` line 74 cite its Correction for "the largest log V of any design is 0.071", which stands in no other file; delete when both are re-pointed (register: WP24's file; the review note was outside unit B's blast radius) |
| the three spikes (46 files) | done: the 26 `.txt` and `.csv` outputs deleted in 14a41a4 after G-6 was re-pointed (e1341e0); the 20 READMEs and scripts stay (their "writes" tables name what each script writes) |
| `streams/P10-review.md` | held: WP10's acceptance (WP10 is a working draft) |

## Unit B (2026-11-10): commits, checks, what remains

Commits on `dev` (rebased on bb51b7e): `e1341e0` (the ledger read against `data/v2/`, G-6 re-pointed, Appendix E rewritten on the host), `14a41a4` (the deletion commit), `2132d36` (the drift rows and the gap fills), and the commit of this report and the inventory's closing section.

### Deletions (D-2, R-2, R-3, R-4)

"WP25: 28 files deleted (second instance, unit B)": the 26 spike outputs (`spike-certificates/` 7, `spike-facet-refit/` 10, `spike-objective/` 9), `scripts/rename_facet.py` and `tests/test_rename_facet.py`; the commit also edits `scripts/check.py` (its map line for the script). The message lists each path and what it no longer did. Held: `spike-ternary/report.md` (reason in the gap table). The citations re-pointed first: G-6 (`oracle.txt` to the README section 3a and `bench_oracle.py`), the only citation of a deleted output by path outside the spike folders; `paper/supporting_material.ipynb` carried it only through the compiled Appendix E table, now rewritten. The READMEs cite the other outputs as what each script writes. `fail_seeds.py` reads `recovery_restarts.csv`, which `bench_c.py` writes first (the README's order).

Appendix E: `tab-E-gaps` rewritten on the host by running that cell with `setup-appendices` in a fresh kernel (`nbclient`, outputs written in place, the way push 4 did; `paper/execute_notebooks.py` runs whole notebooks and was not used). `git diff` of the notebook, cell by cell: cell 73 (`tab-E-gaps`) changed, the other cells byte-equal. No container run (the rule of 2026-11-10 09:05).

### The ledger read against the data of record (N-d)

Rerun on `data/v2/` with `examples/adcs/k_terms.py` (both regimes, seeds 0 to 4, the K = 1, 2, 3 table and the fixed-tau diagnostic) and the M3 and M5 calls. The rows quoted `k3-cubesat.md`, which is the earlier record: tau by K was 38.10, 113.22, 195.18 (primary) and 41.72, 78.75, 162.78 (stock); the data of record gives 38.10, 94.42, 113.22 and 45.68, 71.92, 113.22 (`tests/test_case.py` `RECORD` pins them). Replaced in G-1 (fractions above V = 1), G-7 (smallest near-frontier count of a K = 3 term: 3 and 20), G-9 (tau, band, fractions, rows in a term's own band, mean slack, objective spread), G-10 and G-14 (the baseline K = 3 runs at tau = infinity: gamma 1.1e-16 and objective 0.13579 on all five seeds; at tau = 113.22 objective 0.09269 on all five), G-11 (primary objective 0.14579), G-12 (the K = 1 contending sets: primary total mass, energy balance, pointing error, depth of discharge, settling time; baseline control effort, settling time, power margin, pointing error, energy balance, depth of discharge; "slew time" is not a v2 metric), G-13 (mean slack 0.243 to 0.146 and 0.179 to 0.093) and G-16 (the K = 3 certificates, now equal to `test_k_terms_case.py`'s MARGIN). The rows citing `k3-cubesat.md` for these now cite `k_terms.py` on `data/v2/`. Not changed: G-2's M3 and M5 numbers (they held), G-5, G-17 (just narrowed), and the spike-sourced numbers of G-6, G-7, G-8, G-10 (planted spike tables), G-15, which describe the planted family and the spike runs.

### Checks (D-5, G4), unit B, at the head 2132d36 plus this report

| Check | Command | Result |
|---|---|---|
| Deleted paths named outside records (R-3) | `for f in $(git diff --name-only --diff-filter=D origin/dev..HEAD); do git grep -l -F "$f" -- . ':!work-packages/WP25-*'; done \| wc -l` | 1, `work-packages/WP24-review.md` (a record: the line naming `rename_facet.py` and `check.py` L60); 0 elsewhere. 28 paths |
| Contract and tests (R-2) | `git grep -n -F -e <path> -e <basename> -- work-packages/interface-contract.md work-packages/interface-contract.toml tests/test_interface_contract.py`, per path | 0 for the plain substring; 0 with a filename boundary (`cubesat.csv` as a substring of `adcs_designs_cubesat.csv` is the contract's other file, not a hit) |
| Inventory (R-1) | the A2 command at the head against the table's first column; `grep -ciE "undecided\|tbd\|\?\?"` | 144 rows at the head; 58 rows of the table are gone (all deleted), 4 new paths now have rows (inventory, closing section); 0 |
| Fast suite | `uv run pytest -q -m "not slow" -n auto` | `1731 passed, 16 skipped, 1 xfailed` (13 fewer than unit A's 1744: the deleted `test_rename_facet.py`) |
| Docs, register, site, vocabulary tests | `uv run pytest -q tests/test_claims_register.py tests/test_docs.py tests/test_site.py tests/test_vocabulary.py tests/test_narrative.py` | `112 passed` |
| Doctests | `uv run pytest -q --doctest-modules src` | `57 passed` |
| Site | `uv run python scripts/stage_site.py --paper placeholder` | `Documentation built in 1.30 seconds`, exit 0 |
| Word budgets | `tests/test_site.py::test_word_budgets_hold` (held by tightening) | fitting 800/800, chart 597/600, termination 596/600, tensions 613/700, api 258/300; total 6656/7600 |
| Vocabulary guard | `uv run python scripts/check_vocabulary.py` | `69 new violation(s), 0 known` (70 at unit A; not higher) |
| Lock, lint | `uv lock --check`; `uv run ruff check .`; `uv run ruff format --check .` | `Resolved 178 packages`; `All checks passed!`; `323 files already formatted` |
| Untouched (R-7) | `git diff --stat origin/dev..HEAD -- paper src derivation`; `--diff-filter=R` | `paper/supporting_material.ipynb` only (cell `tab-E-gaps`, the routed regeneration, e1341e0); empty for `src`, `derivation`; no rename |
| Attribution (R-10) | `git log --format=%B origin/dev..HEAD \| grep -ciE "co-authored-by\|generated"` | 0 for unit B's commits. Over `a9e23b2..HEAD` the unit-A pattern finds 6 lines in others' messages ("regenerated", "docs/generated", "the generated tables"); `grep -ciE "co-authored-by\|generated (with\|by)"` finds 1, "generated by scripts/build_figures.py" in a WP24 message |
| Watcher verdict per push (R-10) | the CI run of the push | not in hand at the time of writing; the PM or the reviewer reads it |

### What remains, and why

- `spike-ternary/report.md`: held until `claims_register.toml` C001 and `claims-review.md` line 74 stop citing it for the 0.071 figure (a register edit that must keep the claim backed, the figure stands in no other file).
- Routed from unit A, still open: N-a (`coverage.csv` names the column by the enum type; PM) and N-b (`paper/length_ledger.toml` row at L557; the paper stream).
- `tests/test_case.py` L278 and `docs/superpowers/notes/k3-cubesat.md` (cited by `paper/supporting_material.ipynb`, `tests/test_case.py` and the paper-sources notes for the earlier K = 3 record) still describe the earlier record as "the record of k3-cubesat.md, as printed", though its numbers differ from `RECORD`'s; the note was outside unit B's blast radius. Options: refresh the note from `k_terms.py` output, or delete it and re-point the two citations to `k_terms.py`.
- Not read against the data: G-8, G-15 and the spike-sourced figures of G-6, G-7 and G-10 (planted spikes, outside the cubesat data).
- `docs/examples.md` was not touched (the close-out package's); the paper notebooks' prose and `glossary.yaml` not touched.
- `streams/P10-review.md`: held for WP10's acceptance.

### Recommendation for the driver

Accept D-1 to D-6 of the second instance as met on the evidence above, with the four open items listed (one held file, N-a, N-b, the `k3-cubesat.md` note) carried to the next instance or named owners. The acceptance record is the driver's, quoted verbatim in `WP25-decisions.md`.

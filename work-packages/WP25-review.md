# WP25 — Review report (third instance)

| | |
|---|---|
| **Scope of work** | `work-packages/WP25-3-scope-of-work.md` (approved 2026-11-10, 15:50, by the driver under the mandate; `WP25-decisions.md`, "Instance 3": OD1 (b), OD2 (b), OD3 (b)) |
| **Work reviewed** | `dev` from ca6ce94 (the instance's start; d5d0c3d the head it rebased on before its first push): 6e34f2b (OD1's register and note edits), de3ce61 (the deletion commit), 43a0936, dfc4729, b6c426c, cc30725, 2f1c2d9 (the drift fixes, one per file), the inventory (D-1) and this report |
| **Written by** | the instance's agent, 2026-11-10; every check below ran in its worktree at the head named in the row; the reviewer reruns R-1 to R-11 |

Rewritten per instance (A3). The second instance's report is at `ca6ce94` and the first's at `f9573fd`; the deleted
file's last version is at `b555be7` (`git show b555be7:docs/superpowers/notes/spike-ternary/report.md`).

## Deletions (D-2, R-2, R-3, R-4)

One commit, de3ce61, "WP25: 1 file deleted (third instance)": `docs/superpowers/notes/spike-ternary/report.md` (OD1
(b)). The commit body lists the path with what it no longer did, the R-2 grep (0 by path, 0 by basename over the
contract, the manifest and `tests/test_interface_contract.py`) and the live surfaces that named it. Before it, in the
same push, 6e34f2b dropped the 0.071 sentence from `claims_register.toml` C001's note and from `claims-review.md`'s
row for "a marker is not where V = 1", so no citation dangled; C001 rests on its listed backing (the two
`tests/test_plotting.py` ternary tests and `plot_ternary`'s Notes).

**OD2 (b), applied in a second deletion commit after the PM's ruling.** The scope's sizing said
`examples/adcs/experiments/reports/v1-v2-comparison.md` is "read by no test or page". With the file deleted, the fast
suite gave `1 failed, 1740 passed`: `tests/test_v2_data.py::test_the_committed_report_exists_and_includes_the_register`
read the committed file through `cmp.REPORT` (the generator's constant, so neither grep saw the reference). The executor
held the file and put two options to the PM; the PM ruled that the driver's recorded decision (the report is deleted and
regenerated on demand) changed the requirement that test pinned, so the test joined the radius for this one change: it is
now `test_the_regenerated_report_includes_the_register`, which runs `experiments compare --out <tmp>` (as the slow test
above it does) and checks the same content (the register included verbatim, the solver-exclusion section); the unused
`REPORT` constant went with it; nothing else in the file changed (fdd6d25). Then the deletion commit "WP25: 1 file
deleted (third instance, OD2)" (5a3ee03) listed the file with what it no longer did; the hash rows in
`paper/container/RECORD.md` and `WP23-rounds/gate/README.md` stay as history (A9); last version f517875. R-2 grep 0, 0
(the inventory's first section).

## Drift (D-3, G2)

Vocabulary tool: `69 new violation(s), 0 known` at ca6ce94 and at the head (not higher). Register, docs, site,
vocabulary and narrative tests, and the doctests: the lines are under "Checks".

| Row | State | Where, or what the read found |
|---|---|---|
| S-1 (C001's note and `claims-review.md` line 74 cite the 0.071 figure) | fixed, 6e34f2b | the sentence dropped from both; C001's `backing` unchanged (two tests, `plot_ternary`); the report deleted in de3ce61 |
| S-2 (`spike-certificates/README.md` line 106, `run_cubesat.py` line 20 cite `k3-cubesat.md`) | fixed, 43a0936 and dfc4729 | "(deleted; last version at 4409920)" (`git rev-parse --short f1101ce^`); the spike's taus 195.18 and 162.78 stay as its own run's record (A6) |
| S-3 ("facet" as the model object in the notes `CLAUDE.md` names) | fixed, b6c426c and cc30725 | `proof-conventions.md`: the seven lines (term objective, term-score change, maximizing term(s), identical terms, the several-term fit, each term's gap, nonempty cells and exact term optima). `claims-review.md`: the reviewer's own words on row 74 and in the pointer column of rows 76 and 85; the quoted paper fragments and line 10's quotation keep the word. `figure-review.md`: unchanged (line 7 quotes a caption; lines 70 to 72 discuss the word), per A5 |
| S-4 (`case-model.md` line 363 cites `docs/clients/python/verification.md`) | fixed, 2f1c2d9 | "the runtime's own `docs/clients/python/verification.md`, not a path in this repository" (A6); `tests/test_case_model_howto.py` passes |
| S-5 (`CHANGELOG.md` names no package after WP18) | routed: WP8b (the changelog is its deliverable), one unit | the packages to enter: WP19 (figures), WP22, WP23 and its close-out (the model, eight metrics, the data of record at @7), WP24 (the rename), WP25 (the deletions: 169, 31, 28, 1) |
| S-6 (the nine pages' numbers, read by command, A8) | closed: no number moved | every runnable block of `getting-started.md`, `fitting.md`, `tensions.md`, `termination.md`, `chart.md`, `prediction.md`, `conditioning.md` and `examples.md` run in one namespace per page (as `tests/test_docs.py::test_runnable_blocks_execute` does) and its printed values matched the prose: `getting-started.md` L36 (`trilemma [0 1 2]`, `[0.3 0.37 0.33]`); `fitting.md` L126-128 (0.855, 0.692, 0.664, 0.658; smallest exponent 0.07 to 0.08 at K = 3, 0.00 to 0.07 at K = 4); `tensions.md` L103 (0.351, 0.043); `termination.md` L92 (gamma 0.0020, band 0.02, median margin 0.21). Numbers no block prints, each by a command: `fitting.md` L56 (30 percent on the planted frontier: `info["frontier_mask"].mean()` on `make_frontier_data(300, 3, random_state=0)` is 0.3), L85 (at tau = 50, kappa = 5000 within 0.001 of the infinite-kappa exponents: the page's table `make_frontier_data(400, 4, n_terms=3, random_state=0)`, terms matched by permutation, max difference 0.000000), L131 (`frac_above_` levels off about 0.30: 0.337, 0.31, 0.30, 0.30 at tau 50, 200, 1000, 5000 with `n_terms=2` on the named table); `tensions.md` L55 (band 1/tau, 0.1 at infinite tau: `tensions.py` line 209); `chart.md` L67 (`find_holes` defaults `resolution=50, threshold=2.0`: `gaps.py` line 62); `examples.md` L13 (706 feasible), L16 (0.243 to 0.146, `certified`), L17-20 (72 and 3 percent, peak slew power and control effort, 3 near-frontier designs), the contending sets and `examples/adcs/k_terms.py` on `data/v2/` (44 s; the K = 3 terms' sets are 4, 5 and 5 metrics, the page's "5, 4 and 5" as a list of sizes), the two text blocks against `case.requirements_summary()` and `case.design_sets_summary()` (byte-equal), Figure 7's 193 ringed designs (`plot_frontier_coordinates` rings log V above the default band 0.1: 193 of 706); `README.md` L12 and L19 (the status line, Python 3.12). `prediction.md`, `conditioning.md`: parameters only |
| S-7 (metric names and counts) | closed, recorded | `grep -n -iE "nine metrics|ten metrics|nine traded|slew time|eclipse reserve|launch cost"` over the docs pages, `README.md`, `glossary.yaml` and `claims_register.toml`: no docs page or the README; the glossary's `launch cost` entry (the term's own entry, WP23 OD2's record) and its MoE `short`; one register note (C-row "rewritten at the WP23 close-out", a record of the change). The eight metric names appear on `examples.md` (46 lines) and `overview.md` (1); no other page names a metric |
| N-a (`coverage.csv` names the column by the enum type) | routed: WP26's modeller, one unit through the generator (OD3 (b)) | the model tests' pins re-read; after WP27's current round (`WP25-decisions.md`, "Instance 3"); landed at 6c8481a |
| N-b (`paper/length_ledger.toml`, "typed constant") | closed | `grep -n "typed constant" paper/length_ledger.toml` finds line 612 only, WP24 push 3's comment ("typed constant, cut since") |
| Added by the read: API names on the pages | closed: none stale | every backticked identifier on the docs pages and the README that looks like a package name (an underscore or a trailing underscore) checked against the package's names, the three estimators' parameters and fitted attributes, `Termination`'s and `TensionReport`'s fields and the plotting and gaps signatures: the only unknowns are the `frontier_in_original_units` dict keys (`exponents_orig`, `log_const`), scikit-learn's `return_std` and the tag `positive_only`, and the four termination status strings, all current in `src/` |
| Added by the read: `tests/test_v2_data.py` read OD2's file | closed: the PM's ruling, the test regenerates the report (above) | the scope's "read by no test or page" was wrong for this file |

## Gaps (D-3, G3)

| Row | State | Reason, or owner |
|---|---|---|
| P-1 (`estimator.EPS_ZERO_EXPONENT`, `estimator.PARTICIPATION_THRESHOLD`, `plotting.CATEGORY_COLORS`, `plotting.DATA_COLOR` on no page) | dropped here, scheduled: the PM (a contract question) | the four are in their modules' `__all__` but not in the manifest's `package.submodule_names` (`estimator = ["HyperbolicTradeSpace"]`; `plotting` lists the eight plot names), so the contract does not pin them and the API page, which lists the pinned surface, should not document them before the floor rule is applied. The PM decides: add them to the manifest in one commit (the floor rule) and then one sentence on the API page (258 of 300 words free; the Fitting page is at 800 of 800), or leave them internal |
| P-2 (the contract's backticked names on no docs page) | classed: 125 absent of 198 backticked names (the scope's 145 counted plain identifiers; this count includes dotted and file names) | by the section the name first appears in: 40 in the change-control log only (old names, retired pins: `facet_*`, `assign_facets`, `figs`, `panels`, `slew_time_*`, `eclipse_reserve_wh`, `launch_cost`, `exchange_rates`, the figure pins); 20 in section 14 and one other section (names the log retired or renamed: `soft_*`, `term_gap`, `term_record`, `run_regime`, the v2 data keys); 27 in section 7 (the case module and data: `generate_dataset`, `simulate_adcs`, `sample_designs`, the five csv files, `case.v2.*`; the case's page is `examples/adcs/case-model.md` and `examples.md`'s "Run it", and the case module is not the package's public surface); 11 in section 9 (the derivation ledger's interface `derivation.run`, `derivation.axioms` and their names, documented by `derivation/run.py`'s own text and the generated derivations page; not a docsite page); 11 in section 10 (the glossary schema's field names and the config files, documented in `glossary.yaml`'s header); 6 in section 4 (`__all__`, `package.submodule_names`, the certificate functions `simplex_gap`, `assignment_margin`, `fixed_assignment_bound` and `solvers.distinct_terms`: the second instance's dropped `solvers` rows, A7); 2 in section 3 (`__call__`, `design_id`: the evaluation boundary, `case-model.md`); the rest file names (`pyproject.toml`, `pages.yml`, `CHANGELOG.md`, `MAJOR.MINOR.PATCH`). No public package name with no page is left: every pinned top-level and submodule name is on `docs/api.md` (`tests/test_docs.py::test_every_exported_name_appears_in_api`, `::test_submodule_functions_appear_in_api`) |
| P-3 (the close-out's case functions on `examples.md`) | dropped: the page already says what they add | `examples.md` carries "Requirements read after the fit" (`case.requirements_summary()`, byte-equal to the page) and the three design sets (`case.design_sets_summary()`), and names the association reading's rule ("fewer than the ten an association reading needs, so none is given"); the function names `requirements_table`, `design_sets_table`, `association_all_pairs` are the case's, on `case-model.md` (lines 194, 258); the page is the user's |
| P-4 (the gate rule and the "host-recorded, re-pin at the gate" marking live in `PM-BRIEF.md` only) | routed: the driver (`paper/container/README.md` and `RECORD.md` are his) | one paragraph in the container README: the container is a gate check, not a unit step; a host unit that re-records a reference marks the file "host-recorded, re-pin at the gate" |
| P-5 (WP26's `views.sysml`, WP27's `stakeholders.sysml` on no page) | scheduled: WP26 and WP27 at their acceptance | their packages' records name them; a sentence on `case-model.md` is theirs to add |

## Checks (D-5, G4), at the head of this report

| Check | Command | Result |
|---|---|---|
| Site | `uv run python scripts/stage_site.py --paper placeholder` | `Documentation built in 0.97 seconds`, `staged site in <worktree>/_stage`, exit 0 |
| Fast suite (R-5) | `uv run pytest -q -m "not slow" -n auto` | `1742 passed, 16 skipped, 1 xfailed`, exit 0 (the same count: one test replaced one) at the head after OD2's deletion; `1742 passed, 16 skipped, 1 xfailed` before it (1731 at the second instance; WP27's and WP11's tests since). With the file deleted and the test unchanged it was `1 failed, 1740 passed` |
| Mapped tests (R-5) | `uv run python scripts/check.py --changed` (at the OD1 push) | `1 failed, 1740 passed, 16 skipped, 1 xfailed` with `v1-v2-comparison.md` deleted (the failure above), before the deletion commit was remade; the head's suite is the row above |
| Register, docs, site, vocabulary, narrative tests (R-6) | `uv run pytest -q tests/test_claims_register.py tests/test_docs.py tests/test_site.py tests/test_vocabulary.py tests/test_narrative.py` | `136 passed` (136 at the scope's sizing) |
| Doctests (R-6) | `uv run pytest -q --doctest-modules src` | `57 passed` |
| Vocabulary guard (R-6) | `uv run python scripts/check_vocabulary.py` | `69 new violation(s), 0 known` (69 at ca6ce94; `case-model.md`, which it scans, was edited); 69 again after OD2's deletion |
| Lock, lint (R-6) | `uv lock --check`; `uv run ruff check .`; `uv run ruff format --check .` | `Resolved 178 packages`; `All checks passed!`; `348 files already formatted` |
| Inventory (R-1) | the A2 command at the head, first column diffed against the Rows table; `grep -ciE "undecided\|tbd\|\?\?" work-packages/WP25-inventory.md` | 209 rows, 0 difference; 0 |
| Contract and tests (R-2) | `git grep -n -F -e <path> -e <basename> -- work-packages/interface-contract.md work-packages/interface-contract.toml tests/test_interface_contract.py` | 0 and 0 for `spike-ternary/report.md`; 0 and 0 for `v1-v2-comparison.md` (the inventory's first section) |
| Nothing live names the deleted path (R-3) | `for f in $(git diff --name-only --diff-filter=D d5d0c3d..HEAD); do git grep -l -F "$f" -- . ':!work-packages/WP25-*'; done` | `spike-ternary/report.md`: `work-packages/WP18-scope-of-work.md`, `work-packages/WP8a-decisions.md`; `v1-v2-comparison.md`: `paper/container/RECORD.md`, `work-packages/WP23-rounds/gate/README.md` (the hash rows), `WP10-decisions.md`, `WP15-scope-of-work.md`, `WP23-review.md`, `driver-log.md`, `swap-evidence.md`, `streams/P10-review.md` (all records); 0 in every other live file |
| Deletion commit (R-4) | `git show --stat de3ce61 \| tail -1`; `git show --format=%B -s de3ce61 \| grep -c '^docs/superpowers/notes/spike-ternary/report.md'` | `1 file changed, 155 deletions(-)`; 1. The second deletion commit, 5a3ee03: `1 file changed, 498 deletions(-)`; 1 |
| Untouched (R-7) | `git diff --stat d5d0c3d..HEAD -- paper derivation src examples/adcs/data examples/adcs/model_v2 examples/adcs/experiments/ledger`; `--diff-filter=R` | empty; empty |
| Non-goals surfaces (R-8) | `git diff --stat d5d0c3d..HEAD -- glossary.yaml work-packages/interface-contract.md work-packages/interface-contract.toml tests/test_interface_contract.py CHANGELOG.md paper/container 'work-packages/WP26*' 'work-packages/WP27*' 'work-packages/WP11*' 'work-packages/WP10*' work-packages/streams mkdocs.yml pyproject.toml uv.lock` | empty. The instance's whole diff: `claims_register.toml` (one line), the three notes, the two spike files, `case-model.md` (two lines), the deleted report, and the four WP25 records |
| Attribution (R-10) | `git log --format=%B d5d0c3d..HEAD \| grep -ciE "co-authored-by\|generated (with\|by)"` | 0 |
| Watcher verdict per push (R-10) | the CI run of each push | not in hand at the time of writing; the PM or the reviewer reads it |
| Numbers written (R-11) | the D-4 commit messages | no number was written on a page: no S-6 number moved; the hash written (4409920) comes from `git rev-parse --short f1101ce^` |

## What remains, and why

- The routed rows: S-5 (WP8b), N-a (WP26's modeller, OD3 (b)), P-1 (the PM, the manifest), P-4 (the driver), P-5
  (WP26 and WP27 at acceptance).
- Held files, unchanged: `search-prior-art.md` (WP12, unscoped), `streams/P10-review.md` (WP10's acceptance), WP11's
  round-2 reads (16), WP26's (33) and WP27's (10) files, each the next instance's or its package's.

## Recommendation for the driver

Accept D-1 to D-6 of the third instance as met on the evidence above, with the
five routed rows named with their owners. The acceptance record is the driver's, quoted verbatim in
`WP25-decisions.md`.

# WP25 — Review report (first instance)

| | |
|---|---|
| **Scope of work** | `work-packages/WP25-scope-of-work.md` (approved 2026-11-09, 23:20, by the driver under the mandate; "Gate outcomes") |
| **Work reviewed** | `dev` 73c5bff → db150fc (the inventory, D-1) → 09117d8 (the deletion commit, D-2); this report and the records (D-3 to D-6) |
| **Supervisor (accepts)** | mzargham |
| **Acceptance record** | verbal, quoted in `WP25-decisions.md` |
| **Written by** | the executing stream, 2026-11-10; every check below was run after the deletions, at 09117d8, in the stream's worktree; the reviewer reruns R-1 to R-8 |

Rewritten per instance (A3). The deleted files' last versions are at `73c5bff` (`git show 73c5bff:<path>`).

## Checks (D-5, G4)

| Check | Command | Result |
|---|---|---|
| Docs build, the repo's | `uv run python scripts/assemble_site.py --out <tmp> --paper placeholder` | `assembled site in <tmp>`, exit 0; `INFO - Documentation built in 0.99 seconds` |
| Docs build, bare strict | `uv run mkdocs build --strict -f mkdocs.yml -d <tmp>` | `Aborted with 18 warnings in strict mode!`: all 18 name `docs/generated/*` (the glossary page and the figures the assemble step writes); the same 18 warnings at 73c5bff before the deletions (diffed, identical); none names a deleted path |
| Fast suite | `uv run pytest -q -m "not slow"` | `2 failed, 1816 passed, 16 skipped, 453 deselected, 1 xfailed in 244.70s`; the two failures fail identically at the pre-deletion head (Observations) |
| Path-mapped tests | `uv run python scripts/check.py --changed` | `2 failed, 1816 passed, 16 skipped, 1 xfailed in 57.66s` (the same two) |
| Doctests (R-7) | `uv run pytest -q --doctest-modules src` | `57 passed in 9.31s` |
| Vocabulary guard (R-4) | `uv run python scripts/check_vocabulary.py` | exit 1: `71 new violation(s), 0 known`; byte-identical output at the pre-deletion head (`diff -q`): the known red, no new violation |
| Register and vocabulary tests (R-4) | `uv run pytest -q tests/test_claims_register.py tests/test_vocabulary.py` | `1 failed, 35 passed`: `test_the_register_holds`, `C310: test_surface_k3_and_coordinates_facet_colouring is not defined in tests/test_plotting.py` (a register row of another stream; `tests/` and `claims_register.toml` untouched here) |
| Lock | `uv lock --check` | `Resolved 178 packages`, exit 0 |
| Deletion commit | `git show --stat 09117d8 \| tail -1` | `169 files changed, 12875 deletions(-)`; `git show --format=%B -s 09117d8 \| grep -c '^docs/\|^work-packages/'` = 169 |
| Attribution (R-9) | `git log --format=%B 73c5bff..09117d8 \| grep -ciE "co-authored-by\|generated"` | 0 |
| Untouched surfaces (R-5, R-6) | `git diff --stat 73c5bff..09117d8 -- paper derivation src`; `--diff-filter=R`; `--diff-filter=A --name-only`; the R-6 pathspec with `':(glob)docs/*.md'` | empty; empty; `work-packages/WP25-inventory.md` only; empty (the bare `docs/*.md` pathspec matches `docs/superpowers/notes/**.md` in git, so the reviewer uses `:(glob)`) |

## Requirements

| ID | Verdict | Evidence |
|---|---|---|
| R-1 | met | the inventory command rerun at 09117d8: 0 paths in the tree outside the live set without a row; 169 rows without a file, the deleted set; `grep -ciE "undecided\|tbd\|\?\?" WP25-inventory.md` = 0 |
| R-2 | met | 169 paths in `git show --stat 09117d8` = the inventory's 169 delete rows (generated from the same list); the message has one "path: what it no longer did" line per path |
| R-3 | met | the docs build and the suite above; each deleted basename and path grepped over the remaining tree is on its inventory row: hits only in records (`WP8a-decisions.md`, `WP10-decisions.md`, `WP17-*.md`, `WP18-scope-of-work.md`, `WP19-*.md`, `WP22-scope-of-work.md`, `WP24-scope-of-work.md`, `external-review-2026-11.md`, the kept `spike-ternary/report.md`), two source citations in `derivation/PROOF_MAP_FINDINGS.md` (lines 226 and 281, Drift below), the by-name mention in `derivation/lemma_16_soft_fit_alternation.py:47`, and basename coincidences (`cubesat.sysml`, `assembly_view.png`, `index.html`, `paper-map.webp`, `README.md`) |
| R-4 | met as the head stands | both guards' output lines above; the one red (`C310`) and the 71 vocabulary violations are the head's before this package and belong to other streams' surfaces |
| R-5 | met | the three diffs above |
| R-6 | met | the pathspec diff above, empty |
| R-7 | met | 18 drift rows below (15 navigation pages, the compiled glossary read through `glossary.yaml`, `README.md`, `site/index.html`); every finding has a fix and a landing push; the three output lines are in Checks |
| R-8 | met | the gaps command below: 124 pinned names, 33 absent from `docs/*.md docs/user-guide/*.md`, each with a disposition; the features the read named are rows |
| R-9 | met | the attribution grep = 0; pushes `db150fc`, `09117d8` (the watcher's tier-2 verdict is the driver's to append) |
| R-10 | met | the instance line in the scope's header note; `WP25-decisions.md` "Instance 1" |

## Drift (D-3, G2): the pages against the code at 09117d8

Read against: `HyperbolicTradeSpace.__init__` defaults (`term_aggregation="sum"`, values `"sum"`/`"mean"`), the `color`
option (`None` by default: the designs one colour, band points grey; an array of categories or `"facet"`; other strings
raise), the six glossary entries, the adopted model's views (`examples/adcs/model_v2/views/`). The word "facet" by
itself is WP24's and is not a row. "Lands in": WP24's docs push where the sentence is one WP24 rewrites; otherwise the
next WP25 instance (A6). No page was edited (all are WP24's surface).

| Page | Line and statement | What the code says | Fix drafted | Lands in |
|---|---|---|---|---|
| `docs/index.md` | none | | | |
| `docs/getting-started.md` | L39-40 "the grey band marks those within 0.5 of it in log V" | `plot_log_plane` shades only `-band <= log V <= 0` and does not grey the points (plotting.py:205-219) | "the grey strip marks the region up to 0.5 below the frontier in log V" | next WP25 instance |
| `docs/getting-started.md` | L61-62 "their ratios are the elasticities" | `elasticities[j, k] = -w_k / w_j` (tensions.py:69, :252) | "minus their ratios are the elasticities (`report.elasticities`)" | next WP25 instance |
| `docs/user-guide/overview.md` | L13-14 "the metrics with non-negligible weight are the ones that contend" | `contending_set` is the support of the separate tau = inf program (tensions.py:243-245); weight above `threshold` at the fit temperature is `participating` (:249) | "the metrics with positive weight in the exact-maximum (tau = inf) fit contend; a small weight at the fit temperature is weak participation" | next WP25 instance |
| `docs/user-guide/conditioning.md` | none | | | |
| `docs/user-guide/fitting.md` | L39-41 "a band of near-frontier designs of width 1/tau" | the band is `abs(log V) < 1/tau` (estimator.py:383; glossary "near-frontier band"): 1/tau is the half-width | "a near-frontier band, abs(log V) below 1/tau" | next WP25 instance |
| `docs/user-guide/fitting.md` | L59 "Re-select tau when you change the number of terms." | `mean_slack_` is comparable across `n_terms` "at a fixed temperature" (estimator.py:133-134); L99-100 and L133 of the page say to hold tau | "Hold tau fixed when you change the number of terms; select it at K = 1." | next WP25 instance |
| `docs/user-guide/fitting.md` | L99-100 "Add a term while `mean_slack_` still falls by more than the variation between restarts" | the glossary's mean slack "falls with K by construction and cannot choose K" (glossary.yaml:469) | "`mean_slack_` falls with K by construction, so it cannot choose K alone; add a term only while the resampled exponents stay stable" | next WP25 instance |
| `docs/user-guide/tensions.md` | none | | | |
| `docs/user-guide/chart.md` | L102 "provides five plots" (no `plot_ternary`) | six plot functions and `ternary_marker_values` (plotting.py:50-65, :879) | "six plots", a bullet for `plot_ternary` linked to Examples | next WP25 instance |
| `docs/user-guide/chart.md` | L60 "For a multi-term fit, log V is the soft maximum over facets" | at the default `term_temperature=np.inf` it is the exact maximum; log-sum-exp shifted by `term_aggregation` only for finite kappa (estimator.py:471-476) | "the maximum of the term scores at the default `term_temperature=inf`, a log-sum-exp aggregated by `term_aggregation` (default `"sum"`) when it is finite" | next WP25 instance |
| `docs/user-guide/chart.md` | L41 caption and L55-56 "the band below it has width 1/tau" | the plot shades `-band <= log V <= 0` (plotting.py:81-85); the glossary band is two-sided, width 2/tau | call the grey strip the lower half of the near-frontier band (log V from -1/tau to 0) | next WP25 instance |
| `docs/user-guide/chart.md` | L112-113 "the plots draw every facet, and `facet_labels(estimator, X)` gives a per-row label to pass as `color=`" | `plot_log_plane` draws a term only where it has weight on both plotted metrics (plotting.py:162-164); the designs are one colour by default; `color="facet"` labels by itself; other strings raise (plotting.py:15-18, :123-132) | "the designs are one colour by default; `color="facet"` (or an array of categories) colours them by cell; any other string raises ValueError" | WP24 docs push |
| `docs/user-guide/prediction.md` | none | | | |
| `docs/user-guide/termination.md` | L47 "`fit` warns for `uncertified`, `guard_stop` and `iteration_cap`" | `iteration_cap` warns only when `max_gap > tol` or `objective_change > tol` (estimator.py:391-401) | "warns for `uncertified` and `guard_stop`, and for `iteration_cap` only when the gap or the last objective change exceeds `tol`" | next WP25 instance |
| `docs/user-guide/termination.md` | L49-53, a soft fit lists only `certified` and `stationary` | a soft fit can also end `uncertified`; `stationary_without_margin` never occurs for one (solvers.py:653-659) | add `uncertified` for the soft fit, and `not_applicable` at tau = inf | next WP25 instance |
| `docs/user-guide/limitations.md` | none (the `../../../paper/` link is `test_site.py`'s red, Observations) | | | |
| `docs/api.md` | none (the plotting bullet at L34-35 leaves out `plot_ternary` and `ternary_marker_values`; a gap row) | | | |
| `docs/api-reference.md` | none; it renders the nine top-level names only (gap rows) | | | |
| `docs/examples.md` | none: every API name, path, figure and user-guide link checks out; the fit results it quotes (0.204 to 0.117, `certified`, 6/6/7, 78 percent, 212) were not rerun here | | | |
| `docs/theory.md` | L21-22 "fitting several facets alternates weights from the current model with one program for all terms" | `solve_terms` alternates partition and an entropic refit per term, no joint program (solvers.py:1290-1301) | "alternates assigning the designs to terms with a separate convex refit of each term" | WP24 docs push |
| `docs/theory.md` | L22-23 "The package takes the sharp limit of the weights, one label per design; which facet dominates ... is analysis" | the sharp limit is the default only (`term_temperature=np.inf`); a finite value is the soft fit; in the label fit the labels drive the refit (estimator.py:62-74) | "by default (`term_temperature=np.inf`) the package takes the sharp limit, and the labels drive the refit; reading off the dominant term afterwards is the analysis" | WP24 docs push |
| `docs/further-reading.md` | none (`penalty="reweighted_l1"` matches estimator.py:93, :299) | | | |
| `docs/generated/glossary.md` (from `glossary.yaml`) | L469 mean slack, "The objective the fit minimizes" | at `n_terms=1` the fit minimizes J_tau (`objective_`), "different quantities" from `mean_slack_` (estimator.py:115-127); the formula is `mean_slack_`'s | "The mean shortfall of the designs below the fitted surface, F(W) = -(1/N) sum_i Phi_K(u_i), returned as `mean_slack_`; the several-term fit minimizes it" | WP24 docs push (glossary.yaml is WP24's) |
| `docs/generated/glossary.md` | L485 termination status lists six statuses | the soft fit has a seventh, `"stationary"` (solvers.py:654-659, :1146) | add "stationary (soft fit only)" | WP24 docs push |
| `docs/generated/glossary.md` | L426 assignment, "since the fit weighs every term against every design" | true of the soft fit only; at the default the labels partition and refit (estimator.py:72-73; solvers.py:1290) | "only the soft fit (finite term temperature) weighs every term against every design" | WP24 docs push |
| `README.md` | L12 "Status: WP0 (setup) complete; the package code arrives in later work packages" | the package is built and exported (`__init__.py:6-24`) | replace with the release state or drop it and point at the site | next WP25 instance (README is WP24's surface until its acceptance) |
| `site/index.html` | none (methods, conformance claim, the PCA on near-frontier coordinates check out) | | | |
| `derivation/PROOF_MAP_FINDINGS.md` (not a page; from R-3) | L226 "Source: `docs/superpowers/notes/spike-ggp-fit/report.md`"; L281 "its addendum (`docs/superpowers/notes/spike-soft-fit/`)" | both paths deleted here; last version at 73c5bff | append "(at 73c5bff)" to each citation | WP24 (owner of `derivation/`), or stays as a record |

The system model's views: no navigation page, `README.md` or `site/index.html` names a view path; `examples/adcs/case-model.md` (WP23's) names `project.py` and `render.sh`, both held.

## Gaps (D-4, G3)

The command: every name of `interface-contract.toml` `[package]` (`public_names`, `submodules`, `submodule_names.*`,
`estimator.fitted_attributes`, `methods`, `termination_fields`, `termination_statuses`, `report_fields`,
`term_aggregation_values`) grepped with `grep -l -F` over `docs/*.md docs/user-guide/*.md`: 124 names, 33 absent.
`docs/api-reference.md` renders only the nine top-level names (`::: hyperbolic_trade_space.<name>`), so a submodule name
is on the site only if a page writes it.

| Gap (name or feature; where it lives) | Disposition |
|---|---|
| `coordinates` submodule and its four functions `alr_basis`, `helmert_basis`, `to_frontier_coordinates`, `from_frontier_coordinates` (src/coordinates.py): no page, no directive | scheduled: next WP25 instance adds a `::: hyperbolic_trade_space.coordinates` directive or a paragraph on the Chart page (the page is WP24's surface now) |
| `solvers` names `simplex_gap`, `facet_gap`, `assignment_margin`, `fixed_assignment_bound`, `solve_lp`, `solve_slsqp`, `solve_terms`, `soft_objective`, `soft_weights`, `soft_hessian`, `soft_certificate`, `facet_objective`, `objective_and_grad`, `log_mean_exp`, `level_set`, `single_facet_termination`, `SolveResult`, `TermsResult`, `DISTINCT_TERMS_DISTANCE` (src/solvers.py; the contract pins their signatures) | scheduled: next WP25 instance, one directive `::: hyperbolic_trade_space.solvers` on the API reference page; the Theory page and Appendix B of the paper describe what they compute |
| `tensions` report fields `association_kind`, `contending_exponents`, `novelty_score`; residuals `floor_residual`, `offset_residual`, `sum_residual` (src/tensions.py, src/estimator.py) | scheduled: next WP25 instance, the Tensions and Termination pages name them where they explain the report and the record |
| fitted attribute `training_log_v_` (estimator.py) | scheduled: next WP25 instance, one line on the Fitting page beside `transform` |
| submodule names `tuning`, `predictive`, `preconditioning` (their public classes are rendered through the top-level re-exports) | drop: the objects are documented; the module path adds nothing a user needs |
| `plot_ternary`, `ternary_marker_values` absent from the plotting lists of `docs/api.md` L34-35 and `docs/user-guide/chart.md` L102 (the Examples page shows the plot) | the chart.md row above; `docs/api.md` gets the two names in the same push (next WP25 instance) |
| `spike-ternary/report.md` is a `file:` backing of a register row and the `defined_in` of two glossary entries | scheduled: WP24 (owner of `claims_register.toml` and `glossary.yaml`) points both at `plot_ternary`'s Notes; the next instance deletes the report |
| `spike-certificates/`, `spike-objective/`, `spike-facet-refit/` (46 files) are cited by README path from `paper/supporting_material.ipynb` and by `paper/generate_results.py` | scheduled: at WP10's acceptance instance, fold each README's result into the supporting material and delete the folders, or keep the README and its generator and delete the outputs; one decision for the driver then |
| `work-packages/streams/P10-review.md`: the P10 gate's review, named by no file | scheduled: WP10's acceptance folds it into `WP10-review.md` or deletes it |

## Observations (not counted as failures)

- Two reds are the head's before this package and fail identically at 73c5bff: `tests/test_claims_register.py::test_the_register_holds`
  (`C310` names a test not in `tests/test_plotting.py`) and `tests/test_site.py::test_docsite_pages_do_not_cite_into_the_paper`
  (`limitations.md` links `../../../paper/`, from 8849164). The vocabulary tool's 71 violations are the known red. All three
  belong to the streams that own `claims_register.toml`, `tests/test_plotting.py` and `docs/user-guide/limitations.md`.
- Held for the next instance (WP23's data gate): `spike-sysml-diagrams/project.py` and `render.sh`, the 31 files of
  `work-packages/WP23-rounds/`; `examples/adcs/figures/*.png` (in the live set and WP23's radius, A7).
- The bare `mkdocs build --strict` is not the repo's docs build; `scripts/assemble_site.py` is (it writes the generated
  glossary and figures first). The scope's R-3 names both; the reviewer uses the assemble step.

## Open decisions (for the supervisor)

None.

## Recommendation

Good enough met (R-1 to R-10). Present for acceptance; the drift rows are WP24's and the next instance's to land.

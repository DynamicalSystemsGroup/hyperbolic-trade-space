# Interface contract: technical side and presentation side

Contract version 13. Manifest: `work-packages/interface-contract.toml` (single source of every pinned
fact below). Asserted by `tests/test_interface_contract.py` in the default `uv run pytest`.

## 1. Purpose

The technical work (package, derivations, case, data) and the presentation work (docsite, paper,
release machinery) proceed in parallel. This document pins the surface they meet at, so that content
and machinery iterate without breaking each other. It writes no content and no machinery.

The supervisor, 2026-11-08, verbatim: "the docsite, the paper publishing, and eventually the pypi
release machinery need to stay stable even as the content evolves. so we should be able to pin that
interface so i can iterate on content and the release machinery and publication flow in parallel".

The supervisor's design rule (`WP10-decisions.md`, verbatim): "those repos and the supporting tools for
that ecosystem are developing quickly. we're keeping an abstraction of config variables and measured
attributes so our method is relevant even as tools move, or in cases where scoring comes from
physical systems or human assessments". The stable surface is therefore the configuration to
attributes boundary (section 3), not any tool. The contract and the package's public names mention no
modeling tool, tool version or tool construct.

## 2. Quoted from the manifest

The block below is valid TOML. Each line is a manifest fact stated here by dotted key; the test parses
the block and fails if any line differs from the manifest. A fact changes in both places in one commit
(section 14).

```toml
contract_version = 13
package.import_name = "hyperbolic_trade_space"
package.distribution_name = "hyperbolic-trade-space"
package.version = "0.0.1"
package.version_changed_by = "WP8b"
package.public_names = ["HyperbolicTradeSpace", "LogAffinePreconditioner", "TradeSpaceRegressor", "__version__", "frontier_in_original_units", "make_configured_frontier_data", "make_frontier_data", "select_temperature", "tension_report"]
package.submodules = ["plotting", "gaps", "solvers", "coordinates", "datasets", "preconditioning", "predictive", "tensions", "tuning", "estimator"]
package.estimator.fitted_attributes = ["exponents_", "log_offset_", "training_log_v_", "termination_", "conditioning_", "mean_slack_", "facet_", "coefficients_", "facet_share_"]
package.estimator.term_aggregation_default = "sum"
package.estimator.term_aggregation_values = ["sum", "mean"]
boundary.oracle.status = "pinned_at_WP15_acceptance"
boundary.oracle.call = "__call__(configuration: Mapping[str, float | str]) -> dict[str, float | bool]"
boundary.oracle.evaluate = "evaluate(designs: pandas.DataFrame) -> pandas.DataFrame"
boundary.cubesat_instance.signatures.measure = ["configuration", "model", "kw"]
boundary.cubesat_instance.signatures.sample_designs = ["n", "seed", "model"]
case.dir = "examples/adcs/"
case.regimes = ["primary", "stock"]
case.regime_files.primary = "adcs_designs_cubesat_gains.csv"
case.regime_files.stock = "adcs_designs_cubesat.csv"
case.producing_command = "uv run python examples/adcs/k_terms.py"
case.figures.dir = "examples/adcs/figures/"
derivation.entry_cmd = "uv run python derivation/run.py"
derivation.chain_length = 14
derivation.generated_dir = "build/generated/"
derivation.generated_pages = ["derivations.md", "verification.md"]
derivation.generated_by = "scripts/build_generated.py"
docs.pages = ["index.md", "getting-started.md", "user-guide/overview.md", "user-guide/conditioning.md", "user-guide/fitting.md", "user-guide/tensions.md", "user-guide/chart.md", "user-guide/prediction.md", "user-guide/termination.md", "user-guide/limitations.md", "api.md", "examples.md", "theory.md", "further-reading.md"]
docs.generated_dir = "docs/generated/"
docs.generated_pages = ["glossary.md"]
docs.glossary_source = "glossary.yaml"
docs.glossary_entry_field_names = ["id", "term", "short", "register", "formal", "not", "symbol", "defined_in", "aliases", "avoid"]
docs.glossary_entry_required_field_names = ["id", "term", "short", "register", "formal", "not"]
docs.glossary_list_field_names = ["aliases", "avoid"]
docs.glossary_file_key_names = ["entries", "assumed", "stems"]
docs.paper_sources_dir = "docs/superpowers/notes/paper-sources/"
docs.bibliography = "docs/references.bib"
docs.citation_syntax = "[@key]"
docs.math_inline = "$...$"
docs.math_display = "$$...$$"
build.tests_cmd = "uv run pytest"
build.docs_cmd = "uv run --group docs mkdocs build --strict"
build.docs_out = "_site/docs/"
build.paper_cmd = "uv run myst build --html"
build.paper_out = "_site/paper/"
build.root_index_out = "_site/index.html"
build.workflow = ".github/workflows/pages.yml"
build.workflow_deploys_on = "release tag v* and manual dispatch only; never on a push to main or dev"
build.default_groups = ["dev", "case", "docs"]
build.stage.script = "scripts/stage_site.py"
build.stage.command = "uv run python scripts/stage_site.py --serve"
build.stage.build_dir = "_stage/"
build.stage.url = "http://127.0.0.1:8000"
```

## 3. The stable surface: configuration to attributes

**The table.** One row per evaluated configuration. Columns are of four kinds:

- configuration columns: the design variables (numeric or categorical), not fitted, carried as covariates;
- attribute columns: measured outcomes, raw, in mixed units and directions; conditioning them into
  strictly positive, larger-is-better metrics is the analyst's job (the package starts at the fit);
- flag columns: booleans such as feasibility;
- identifier columns: `design_id`, `seed`.

The table is what `fit`, the analysis and the search consume.

**The oracle signature.** A deterministic function from one configuration to an attribute row:

```python
class Oracle(Protocol):
    config_names: tuple[str, ...]
    attribute_names: tuple[str, ...]
    flag_names: tuple[str, ...]

    def __call__(self, configuration: Mapping[str, float | str]) -> dict[str, float | bool]: ...
    def evaluate(
        self, designs: pandas.DataFrame
    ) -> pandas.DataFrame: ...  # batch, rows in design_id order
```

`__call__` returns a mapping whose keys are the attributes, flags and auxiliary columns. It is
deterministic; noise is added by a wrapper (the search's), not by the oracle. The scenario is fixed
when the oracle is constructed, not per call. A configuration out of range, or an unknown category,
raises `ValueError` naming the variable. `evaluate` is the batch form and returns rows in `design_id`
order.

**Black box.** The source of the attributes is a black box to the method: a simulator, a physical
test or a human assessment satisfy the same contract. The method, the paper and the search depend on
the table and on this signature only.

**Status of the protocol.** The protocol is stated here and is pinned by an additive amendment when
WP15 is accepted. Until then the frozen cubesat pair is the pinned oracle.

**The cubesat instance.** `cubesat_model.measure(configuration, model=None, **kw)` and
`cubesat_model.sample_designs(n, seed=0, model=None)` are pinned as the cubesat instance only (their
parameter names are in the manifest). Whatever machinery the instance uses lies behind the boundary
and is not part of this contract.

## 4. R-1 Package surface

Pinned: import name `hyperbolic_trade_space`; distribution name `hyperbolic-trade-space`; the
public names of `__all__` (floor, section 2); the importable submodules (section 2); per submodule
the importable names (manifest `package.submodule_names`), including the certificate functions
`simplex_gap`, `facet_gap`, `assignment_margin`, `fixed_assignment_bound`, the `Termination` record
and the tolerances `EPS_FEAS`, `EPS_KKT`, `GUARD_TOL`, `POLISH_STEPS`; the parameter names of the four
certificate functions; the fitted attributes `termination_` and `conditioning_` (and
`exponents_`, `log_offset_`, `training_log_v_`; from version 3 also `mean_slack_`, `facet_`, `coefficients_`,
`facet_share_`, which exist for every number of terms: at one term `facet_` is all zeros and
`facet_share_` is `[1.0]`; `mean_slack_` is the mean slack, the quantity to compare across numbers of
terms, while `objective_` is what the solver minimized); the `Termination` field names and status strings;
the per-facet report fields of `TensionReport`. From version 6 the record also carries
`min_curvature` and the status `"stationary"`, and `solvers` also offers `soft_weights`,
`soft_objective`, `soft_hessian` and `soft_certificate` (see below).

*The soft fit (version 6, WP17).* A finite `term_temperature` kappa, with `n_terms > 1` and
`facet_step="support"`, selects the soft fit: every design carries the weights
`softmax_k(kappa (w_k . u - beta_k))` on every term and the fit minimizes the mean slack of the
model it reports; at the default `np.inf` the fit is the label fit, unchanged. The word
`"certified"` then has two meanings, by the kind of fit. Label fit: the assignment is fixed, the
gaps are within `EPS_KKT` and the margin is positive (conditional local optimality of the fixed
assignment). Soft fit: every term's weighted gap is within `EPS_KKT` and the Hessian of the soft
objective is positive definite on the tangent space of the active face (a strict local minimizer of
the soft objective, the second-order sufficient condition); `"stationary"` is the same gaps with
curvature not positive (a saddle or a flat direction); `min_curvature` is the smallest curvature
(`nan` for a label fit); `gamma`, `radius` and `bound` are `nan` for a soft fit. A soft fit at
`temperature = inf`, with a penalty, or under `facet_step="tangent"` (which ignores kappa) reports
`"not_applicable"` (the last: the fit is the label fit). `facet_`, the facet shares, the
contending sets and the elasticities stay the analysis by the dominant term; `mean_slack_` is the
mean slack of the reported model.

*The term aggregation (version 9, WP21 D-1).* The constructor keyword `term_aggregation` of
`HyperbolicTradeSpace` takes `"sum"` (the default) or `"mean"` (manifest
`package.estimator.term_aggregation_default`, `term_aggregation_values`); it is stored verbatim and
validated in `fit`. `"sum"` is the log-sum-exp over the K terms (today's behaviour, every committed
number), with `max <= Phi_K <= max + log K / kappa`; `"mean"` is the log-mean-exp, `Phi_K - log K /
kappa`, with `max - log K / kappa <= Phi_K <= max`. The two differ by the constant `log K / kappa`,
so the soft weights, the Hessian, the certificate and the fitted terms are the same; `score_samples`
and the mean slack shift by exactly that constant. No effect at `term_temperature = inf` or one term.

*Distinct terms (version 10, WP21 D-5).* The `Termination` record also carries `n_distinct_terms`,
the number of distinct terms of the returned model: exponent vectors within
`solvers.DISTINCT_TERMS_DISTANCE` (Euclidean, single linkage; `solvers.distinct_terms`) count as one.
It equals K on a fit whose terms are all different and falls below K where terms repeat; it is `1` at
one term and in the degenerate shortcuts, and `-1` on a record built without the exponents. It is read
only: no other field, status or number changes.

Consumers: the docsite generates its API reference from the numpydoc docstrings of the public names,
and the paper reads the attributes above; neither imports a name outside this list without an
amendment.

## 5. R-2 Version string

One authority: `pyproject.toml` `[project].version`, mirrored by `hyperbolic_trade_space.__version__`.
Format: PEP 440, `MAJOR.MINOR.PATCH`. Current value: `0.0.1` (section 2). Only WP8b (the release
machinery) changes it, and it changes both places together; a bump therefore edits the manifest value
in the same commit. The presentation layer reads the version and never writes it.

## 6. R-3a The boundary

Stated in section 3. Checked by a toy oracle built in the test from a pure-Python function; the
protocol members are asserted by name; the frozen pair exists with the pinned parameter names; the
contract text and the package's top-level names contain no modeling-tool word or tool-version string.

## 7. R-3 Case module and data

The case code lives under `examples/adcs/` and is importable through the `pythonpath` of
`pyproject.toml` (`.`, `src`, `examples/adcs`). Pinned modules and functions, with parameter names
(manifest `case.signatures`): `k_terms` (`load_metrics`, `make_conditioner`, `fit_k`, `select_tau`,
`reports`, `facet_record`, `certificate`, `run_regime`, `main`; attribute `REGIMES`), `generate_dataset`
(`generate`, `generate_cubesat`, `main`), `design_space` (`sample_designs`, `evaluate_design`),
`cubesat_model` (`measure`, `sample_designs`), `adcs_sim` (`simulate_adcs`, `run_step_response`,
`make_config`), `make_check_designs` (`feasible_primary`, `predict`, `simulate`, `main`).

Regimes: `primary` is `adcs_designs_cubesat_gains.csv`, `stock` is `adcs_designs_cubesat.csv`.

Data files in `examples/adcs/data/` (the frozen generation, manifest `case.frozen_data_dir`, the cited
comparison; the case module reads the data of record under `case.data_dir = "examples/adcs/data/v2/"`
since version 13), each with its exact header and dtype classes (int, float, bool,
str) in the manifest (`case.data`): `adcs_designs_cubesat_gains.csv` (primary), `adcs_designs_cubesat.csv`
(baseline), `adcs_designs.csv`, `check_designs_cubesat.csv`, `check_predictions_cubesat.csv`. The
files are committed and seeded; only a package whose scope says so regenerates them, and it updates
the manifest in the same commit.

The v2 datasets live in `examples/adcs/data/v2/` with the frozen file names (manifest `case.v2`):
the frozen columns less the slew-time columns `slew_time_s` and `slew_time_05deg_s`, in the frozen
order. The traded metrics of the v2 data are nine (`case.v2.traded_metrics`); the one time metric
is the settling time, read by event detection (`case.v2.settling_time_method`), the hold time: the
first time after which the pointing error stays inside the band of the model's settling fraction.
The check-design predictions carry `pred_std_settling_time_s`. The v2 files are ledgered
(`examples/adcs/experiments/ledger/ledger.jsonl`) and regenerate once, in the container of record,
by a package whose scope says so, which updates this manifest in the same commit.

## 8. R-4 Figures

Figures the presentation layer embeds are PNG files in `examples/adcs/figures/`, named `NN_name.png`
(from the case notebook) or `k3_<kind>_<regime>.png` (from `uv run python examples/adcs/k_terms.py`).
The fifteen files existing today are listed in the manifest (`case.figures.files`). The presentation
layer treats figures as read-only inputs and never writes there. Figures are committed; the paper is
committed executed (supervisor, `WP14-decisions.md`, OD1).

## 9. R-5 Derivation ledger and generated pages

`uv run python derivation/run.py` runs the chain L1 to L14 (`CHAIN_NAMES`; 14 modules), prints the
assumption audit, exits 0 on success and non-zero on a failed lemma. Lemma modules are
`derivation/lemma_NN_<name>.py`; numbers are contiguous from 1, never reused or renumbered, and a
new lemma takes the next number. The interface of `derivation.run` (`CHAIN`, `CHAIN_NAMES`,
`run_chain`, `load_chain`, `lemma_number`, `print_audit`, `main`) and of `derivation.axioms`
(`AXIOMS`, `by_tag`, `fallbacks`) is pinned. Two pages are generated for the paper's appendices and
are not on the docsite: `derivations.md` and `verification.md`, written by
`scripts/build_generated.py` into `build/generated/` (git-ignored, never committed, outside
`docs/`). The same script compiles the docsite's Glossary page (section 10). The contract pins names
and locations, not prose.

## 10. R-6 Documentation sources

The docsite is the documentation of the package for a user: Markdown in `docs/` (the pages of
`docs.pages`: Home, Getting started, the User guide pages under `docs/user-guide/`, API, Examples,
Theory in brief, Further reading), the generated API reference (`docs/api-reference.md`) and the
generated Glossary, plus `references.bib`. The Glossary is compiled from `glossary.yaml` by
`scripts/build_generated.py` into `docs/generated/glossary.md` (git-ignored) and carries term and a
one-line definition only; `glossary.yaml` is the single source of the register's phrases and is
offered to the paper as the source of its register table. Its schema is pinned (a floor, section 14):
an entry has the required fields `id`, `term`, `short`, `register`, `formal`, `not` and the optional
`symbol`, `defined_in`, `aliases` (a list of accepted variants) and `avoid` (a list of `phrase` and
`reason`, variants that must not appear); the file has `entries` and the optional lists `assumed`
(terms the reader is assumed to know, each with a reason) and `stems` (the stems that mark a term of
art). The Glossary page renders term and short only; the new fields are for the paper's register and
the vocabulary review (`docs/superpowers/notes/vocabulary-review.md`). Notes under `docs/superpowers/notes/` are
excluded from navigation. `docs/superpowers/notes/paper-sources/` holds verbatim snapshots of the
pages that left the docsite (read-only; the paper's author reads them). Citations: `[@key]` (several
as `[@key1; @key2]`) against `docs/references.bib`. Math: LaTeX in `$...$` and `$$...$$`. The
presentation side owns the pages; the technical side edits none, and a pinned page is renamed or
removed only by an amendment. `docs/api.md` stays the hand-written overview; `docs/api-reference.md`
is generated from the numpydoc docstrings (supervisor, OD2: "Generated from docstrings").
Presentation-owned: `mkdocs.yml`, `glossary.yaml`, the pages above, `docs/generated/`, `site/`,
`paper/`, the workflows named below, release files.

## 11. R-7 Build and publish interface

- tests: `uv run pytest`
- docsite: `uv run --group docs mkdocs build --strict` into `_site/docs/`
- paper: `uv run myst build --html`, run in `paper/`, delivered to `_site/paper/`
- root index: `site/index.html` copied to `_site/index.html`
- Pages: `.github/workflows/pages.yml` deploys on a release tag `v*` and on manual dispatch only, never on a push to `main` or `dev`; the existing
  `.github/workflows/test.yml` stays the technical side's CI
- public paths: `/`, `/docs/`, `/paper/` (under `https://dynamicalsystemsgroup.github.io/hyperbolic-trade-space/`), stable
- dependency groups: `docs` and `paper` belong to the presentation side, `dev`, `case`, `notebooks` to
  the technical side; `default-groups` is `["dev", "case", "docs"]`; `pyproject.toml` itself is edited by the
  driver on request
- the branching rule of `work-packages/README.md` applies

## 12. R-8 Change control

See section 14.

## 13. R-12 Local staging: release control

One command builds the whole site (root index, docsite under `/docs/`, paper under `/paper/`) into
`_stage/` and serves it on `http://127.0.0.1:8000`, with no network and no kernel, by default:

```
uv run python scripts/stage_site.py --serve
```

WP8a delivers `scripts/stage_site.py` and the first such review; the clause is skipped until the file
exists. Release control (supervisor, OD1, verbatim): "the review of the staged local host version of
the site should be done before a merge that would generate a deployment. this needs to be part of
release control". A merge to `main` that would deploy is therefore preceded by a review of the staged
site, recorded in the merging package's decisions file. The review loop needs no publish.

## 14. Change control (R-8)

An amendment is a commit that edits this document and the manifest together, says what changed, why,
and which side it affects, and is approved verbally by the supervisor with the quote recorded in
`work-packages/WP14-decisions.md`. Removing or renaming a pinned item needs an amendment; so does
moving case code, a figure, a data file or a build output. Additions (a module, a public name, a
page, a figure) need no approval but are added to the manifest in the same commit (floor rule); the
test enforces this. A deprecation names the replacement, keeps the old name for one amendment cycle
and states when it goes. `contract_version` is an integer; it increases by one per amendment and equals
the last row of the change log.

| Version | Date | Change | Side affected | Approval |
|---|---|---|---|---|
| 1 | 2026-11-08 | Initial version: package surface, boundary, case, figures, derivation, docs, build, staging, ownership | both | `WP14-decisions.md`, scope approval ("Approved") |
| 2 | 2026-11-08 | Docsite for a package user (WP8a Amendment 2): `docs.pages` becomes Home, Getting started, User guide, API, Examples, Theory in brief, Further reading; `method.md`, `why-and-how.md`, `preconditioning.md`, `limitations.md`, `literature.md`, `case.md` leave `docs/`; pinned path `docs/superpowers/notes/paper-sources/`; the docs pages move to the presentation side (carve-out for the paper sources); `glossary.yaml` is a presentation file and the Glossary is compiled from it into `docs/generated/glossary.md`; `derivations.md` and `verification.md` move to `build/generated/` for the paper's build; the world-line labelling (C-9) is withdrawn and `overrides/` is removed; delivered clauses leave the skip list; the known-gaps row on the bibliography and literature page is rewritten | both | `WP14-decisions.md`, "Contract version 2" ("Approved") |
| 3 | 2026-11-09 | Fitted attributes for every number of terms (WP10, cold-reader findings 19 and 20): `facet_`, `coefficients_` and `facet_share_` exist at one term as well (all zeros, `exp(-kappa beta)`, `[1.0]`); `mean_slack_` is added, the mean slack defined for every number of terms, and `objective_` is documented as what the solver minimized. Additive: the pinned fitted attributes grow (floor rule); no existing fitted number changes | both | `WP10-cold-reads-triage.md`, items 19 and 20 (the driver's triage) |
| 4 | 2026-11-09 | The glossary's schema (WP10 Amendment 4, R-35): the entry fields `aliases` and `avoid` (lists) and the file-level lists `assumed` and `stems` are pinned beside the existing fields (`docs.glossary_entry_field_names`, `docs.glossary_entry_required_field_names`, `docs.glossary_list_field_names`, `docs.glossary_file_key_names`); the Glossary page still renders term and short only. Additive: the pinned lists grow (floor rule) | presentation (the paper reads the same file) | `WP10-decisions.md`, "The supervisor's reading of the abstract, second pass" ("make sure its reflected in our glossary and that we have a documented review technique for jargon checking") |
| 5 | 2026-11-09 | The tension report's field `exchange_rates` is renamed `elasticities` (WP10 Amendment 4, R-37), with no alias since nothing is released: `package.tensions.report_fields` carries the new name; the code takes the glossary's word. No number changes | both | `WP10-decisions.md`, "The supervisor's reading of the abstract, second pass" ("i believe we define these as elasticities"), and the driver's call on the field |
| 6 | 2026-11-09 | The soft several-term fit (WP17, R-1, R-7): a finite `term_temperature` selects the fit with a weight on every term for every design; the `Termination` record gains `min_curvature` and the status `"stationary"`; `"certified"` has two meanings (label fit: the fixed assignment; soft fit: the second-order test of the soft objective); `solvers` offers `soft_weights`, `soft_objective`, `soft_hessian`, `soft_certificate`. Additive: the pinned field, status and name lists grow (floor rule); the default (`np.inf`) fit is unchanged, attribute for attribute | technical (the docsite and the paper words follow) | `WP17-scope-of-work.md`, approved by the driver under the mandate on the supervisor's conditional direction and amended on his question ("can we get another certification method for the soft fit") |
| 7 | 2026-11-09 | The ternary plot (WP18, R-5): `plotting` also offers `plot_ternary(estimator, X=None, names=None, groups=None, lines=False, near=0.2, ax=None, scheme="auto") -> Axes`; it draws a triangle of the shares of a total among three metrics, tinted by region (where each facet dominates, named by words read from the fit) with the designs as points and each facet's exponent vector as a numbered marker (where that facet's V peaks at a fixed total, not where V = 1); `lines=True` adds lines of equal V; `groups` sums each facet's exponents within three groups of metrics. Additive: the pinned `plotting` list grows (floor rule); no other pinned fact changes | technical (the docsite and the paper words follow) | `WP18-scope-of-work.md`, approved by the driver under the mandate |
| 8 | 2026-11-09 | The values at the ternary plot's markers (WP18, supervisor's request): `plotting` also offers `ternary_marker_values(estimator, X, names=None) -> pandas.DataFrame`, one row per numbered marker of `plot_ternary(..., lines=True)` (marker shape, number, the facet's exponent vector as shares, and V attained there as a fraction of the highest marker's V; `attrs["levels"]` holds the equal-V levels), computed by the code that draws the lines and markers. Additive: the pinned `plotting` list grows (floor rule); `plot_ternary`'s signature is unchanged and its figure is unchanged | technical (the docsite and the paper words follow) | `WP18-decisions.md`, supervisor, "this one is great but make sure the prose is clear about the values attained at the square, star and triangle points marked" |
| 9 | 2026-11-09 | The term aggregation keyword (WP21 D-1, D-2): `HyperbolicTradeSpace` gains `term_aggregation` (`"sum"` default, `"mean"`), stored verbatim and validated in `fit`; manifest `package.estimator.term_aggregation_default` and `term_aggregation_values`. Additive; the default is today's behaviour, so no committed number changes | technical (the docsite and the paper words follow) | `external-assessment-2026-11-09/triage.md`, the supervisor on A4: "really the package should support both setups ... in practice these should be keyword based." |
| 10 | 2026-11-09 | The distinct-terms count (WP21 D-5): the `Termination` record gains `n_distinct_terms` (exponent vectors within `solvers.DISTINCT_TERMS_DISTANCE` count as one); `solvers` offers `distinct_terms` and `DISTINCT_TERMS_DISTANCE`. Additive: the pinned field and name lists grow (floor rule); no other field and no committed number changes | technical (the docs K-sweep example and the paper's D.15 show it beside the slack) | `external-assessment-2026-11-09/triage.md`, finding A3, accepted by the driver under the mandate; `WP21-scope-of-work.md` D-5 |
| 11 | 2026-11-09 | The designs' colour in the plots (`WP19-decisions.md`, the principle check's package item; the supervisor's "Recolour" for docs Figure 8): colouring designs by the term that scores them highest is the cluster idiom and is no plot's default. `plot_ternary` gains a trailing keyword, `plot_ternary(estimator, X=None, names=None, groups=None, lines=False, near=0.2, ax=None, scheme="auto", color=None) -> Axes`: by default the designs are one neutral colour (the near-frontier ones larger); `color="facet"` colours the near-frontier designs by the term that scores each highest (its cell), an analysis of the fit; the region tints, the numbered exponent-vector markers and the lines of equal V are unchanged, so `ternary_marker_values` (row 8) is unchanged. `plot_log_plane` and `plot_frontier_surface_3d` (pinned by name only; signatures unchanged) likewise draw the designs in one colour for any number of terms, with the term lines or the envelope surface as the model, and take `color="facet"` for the cell. Every existing call runs unchanged; the rendered figures change as stated | technical (the docsite and the paper words follow) | the driver under the mandate (`WP19-decisions.md`, the principle check's package item; the supervisor's "Recolour") |
| 12 | 2026-11-10 | One time metric (WP23 G5, D-4; the supervisor, `WP16-decisions.md`: "One: settling time"): the v2 datasets lose `slew_time_s` and `slew_time_05deg_s`, their headers are pinned (`case.v2.data`, the frozen columns less those two, in the frozen order), the traded metrics of the v2 data are the nine of `case.v2.traded_metrics`, the settling time is read by event detection (`case.v2.settling_time_method = "events"`, WP16 Amendment 2 D-7), and the check-design predictions carry `pred_std_settling_time_s`. No `launch_cost` column (`WP23-decisions.md`, OD2). The frozen files and their `case.data` manifests are unchanged | technical (the paper's figures and numbers that used slew time regenerate in their own stream after the data gate; the docs follow) | the driver under the mandate, recorded in `WP23-decisions.md` at the data gate |
| 13 | 2026-11-10 | The case reads the data of record (WP23's swap, ea46637): `case.data_dir` changes from `examples/adcs/data/` to `examples/adcs/data/v2/`, where the paper's case module (`CUBESAT.data_dir`, `k_terms.DATA`) now reads; the frozen generation under `examples/adcs/data/` stays the cited comparison and is untouched, so its directory is pinned as the new `case.frozen_data_dir = "examples/adcs/data/"` and the `case.data` file manifests are asserted there. Not additive: one pinned field changes its value (a pinned path moves, which needs an amendment, section 14), with one key added to keep the frozen files pinned. No file moves and no committed number changes | technical (the paper and docs already read the v2 data) | the driver under the mandate, 2026-11-10; WP23's swap, `WP23-decisions.md` |

## 15. Consumers: may assume, must not touch

**Docsite (WP8a).** May assume: the public names, version rule, citation and math syntax, the
bibliography path, the derivation entry points, the generated-page names and locations, and the
docstring style; that `uv run pytest` is green on `main`; that the build commands of section 11 and
the staging command of section 13 are its to implement. Must not touch: `src/`, `derivation/`,
`examples/`, `docs/superpowers/` other than `docs/superpowers/notes/paper-sources/`,
`docs/references.bib`, `pyproject.toml` and `uv.lock` except through the driver.

**Paper (WP10, with the outputs of WP12).** May assume: the case modules, functions, parameter names,
regimes, data headers and figure names of sections 7 and 8, the estimator attributes of section 4, the
boundary of section 3; that figures and data are committed and stable; the contents of
`docs/superpowers/notes/paper-sources/` (read-only), `glossary.yaml` (the register's phrases) and the
generated `derivations.md` and `verification.md` in `build/generated/`. Must not touch: data files,
figures and case modules other than `examples/adcs/case.py`; the docsite files; the derivation chain.
Its build is the paper command of section 11, delivered to `_site/paper/`; the paper is committed executed.

**Release machinery (WP8b).** May assume: one version source (section 5), the `pages.yml` and
`test.yml` workflow names, the branch rule. Must not touch: the package code or content, the docsite
and the paper beyond reading their outputs; it edits the version in the two places together, with the
manifest value.

**Technical side (WP13 onward).** May assume: the presentation side reads only what the manifest lists.
Must not touch: the presentation-owned paths of section 16; it keeps every pinned name, path, header
and command, adds items freely with a manifest edit in the same commit, and announces any other change
by amendment.

## 16. File ownership by side (R-9, R-10)

Sides are pairwise disjoint; the manifest carries the explicit paths and the test asserts it.

| Side | Paths (prefixes end in `/`) |
|---|---|
| technical | `src/`, `derivation/`, `tests/` (except carve-outs), `docs/superpowers/` (except the carve-out below), the case modules, notebook, `data/`, `figures/`, `model_v2/`, `experiments/` and `case-model.md` under `examples/adcs/`, `.github/workflows/test.yml`, `README.md`, `.python-version` |
| process | `work-packages/` (except carve-outs), `CLAUDE.md` |
| WP14 | `work-packages/interface-contract.md`, `work-packages/interface-contract.toml`, `tests/test_interface_contract.py` |
| WP8a | `mkdocs.yml`, `glossary.yaml`, `site/`, `scripts/`, `.github/workflows/pages.yml`, `tests/test_site.py`, `docs/index.md`, `docs/getting-started.md`, `docs/user-guide/`, `docs/api.md`, `docs/api-reference.md`, `docs/examples.md`, `docs/theory.md`, `docs/further-reading.md`, `docs/generated/`, `docs/superpowers/notes/paper-sources/` (carve-out inside the technical `docs/superpowers/`) |
| WP10 | `paper/`, `examples/adcs/case.py`, `tests/test_paper.py`, `tests/test_case.py`, `docs/references.bib` |
| WP12 | none yet; declared by an additive amendment when its scope is approved |
| WP8b | `CHANGELOG.md`, `LICENSE`, `.github/workflows/release.yml` |
| driver | `pyproject.toml`, `uv.lock`, `.gitignore` |

Links from one side's file to another side's are allowed; no file is shared beyond links.

## 17. Known gaps (R-11)

Open conformance gaps, recorded and not fixed here; each names the closing package.

| Gap | Closed by |
|---|---|
| The docstring of `src/hyperbolic_trade_space/__init__.py` says package code arrives in later work packages | WP8b |
| `paper/myst.yml` does not exist | WP10 |
| `pyproject.toml` has no `paper` group | WP10 (edit by the driver) |
| `docs/references.bib` is assigned to WP10; `docs/literature.md` is a preserved source under `docs/superpowers/notes/paper-sources/`; later technical edits go through an amendment | WP10 |
| The Oracle protocol is stated but not yet pinned | WP15 |

## 18. Skip list

The test skips each clause below, with its reason, until the file exists, then enforces it. The
clauses WP8a delivered (the generated-pages script, the docsite configuration, the API reference
page, the Pages workflow, the staging command, the root index) are enforced and left this list in
version 2.

| Clause | File | Reason | Closed by |
|---|---|---|---|
| R-7 paper configuration | `paper/myst.yml` | WP10 delivers the paper configuration | WP10 |
| R-3a Oracle protocol | `examples/adcs/experiments/oracle.py` | WP15 delivers the protocol; pinned by additive amendment | WP15 |

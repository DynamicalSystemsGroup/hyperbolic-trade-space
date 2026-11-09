# Interface contract: technical side and presentation side

Contract version 1. Manifest: `work-packages/interface-contract.toml` (single source of every pinned
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
contract_version = 1
package.import_name = "hyperbolic_trade_space"
package.distribution_name = "hyperbolic-trade-space"
package.version = "0.0.1"
package.version_changed_by = "WP8b"
package.public_names = ["HyperbolicTradeSpace", "LogAffinePreconditioner", "TradeSpaceRegressor", "__version__", "frontier_in_original_units", "make_configured_frontier_data", "make_frontier_data", "select_temperature", "tension_report"]
package.submodules = ["plotting", "gaps", "solvers", "coordinates", "datasets", "preconditioning", "predictive", "tensions", "tuning", "estimator"]
package.estimator.fitted_attributes = ["exponents_", "log_offset_", "training_log_v_", "termination_", "conditioning_"]
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
derivation.generated_dir = "docs/generated/"
derivation.generated_pages = ["derivations.md", "verification.md"]
derivation.generated_by = "scripts/build_generated.py"
docs.pages = ["method.md", "why-and-how.md", "preconditioning.md", "api.md", "limitations.md", "literature.md"]
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
build.workflow = ".github/workflows/publish.yml"
build.workflow_deploys_from = "main"
build.default_groups = ["dev", "case"]
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
    def evaluate(self, designs: pandas.DataFrame) -> pandas.DataFrame: ...  # batch, rows in design_id order
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
`exponents_`, `log_offset_`, `training_log_v_`); the `Termination` field names and status strings;
the per-facet report fields of `TensionReport`.

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

Data files in `examples/adcs/data/`, each with its exact header and dtype classes (int, float, bool,
str) in the manifest (`case.data`): `adcs_designs_cubesat_gains.csv` (primary), `adcs_designs_cubesat.csv`
(baseline), `adcs_designs.csv`, `check_designs_cubesat.csv`, `check_predictions_cubesat.csv`. The
files are committed and seeded; only a package whose scope says so regenerates them, and it updates
the manifest in the same commit.

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
(`AXIOMS`, `by_tag`, `fallbacks`) is pinned. Generated pages go to `docs/generated/` (git-ignored,
never committed), built by `scripts/build_generated.py`, with page names `derivations.md` and
`verification.md`; the contract pins names and location, not prose.

## 10. R-6 Documentation sources

The docsite reads Markdown in `docs/`: `method.md`, `why-and-how.md`, `preconditioning.md`, `api.md`,
`limitations.md`, `literature.md`, and `references.bib`. Notes under `docs/superpowers/notes/` are
excluded from navigation. Citations: `[@key]` (several as `[@key1; @key2]`) against
`docs/references.bib`. Math: LaTeX in `$...$` and `$$...$$`. The technical side adds pages and
renames none without an amendment. `docs/api.md` stays the hand-written overview;
`docs/api-reference.md` is a presentation-owned page generated from the numpydoc docstrings
(supervisor, OD2: "Generated from docstrings"). Presentation-owned: `mkdocs.yml`, `docs/index.md`,
`docs/case.md`, `docs/api-reference.md`, `docs/generated/`, `site/`, `paper/`, the workflows named
below, release files.

## 11. R-7 Build and publish interface

- tests: `uv run pytest`
- docsite: `uv run --group docs mkdocs build --strict` into `_site/docs/`
- paper: `uv run myst build --html`, run in `paper/`, delivered to `_site/paper/`
- root index: `site/index.html` copied to `_site/index.html`
- Pages: `.github/workflows/publish.yml` deploys from `main` only; `dev` never deploys; the existing
  `.github/workflows/test.yml` stays the technical side's CI
- public paths: `/`, `/docs/`, `/paper/` (under `https://dynamicalsystemsgroup.github.io/hyperbolic-trade-space/`), stable
- dependency groups: `docs` and `paper` belong to the presentation side, `dev`, `case`, `notebooks` to
  the technical side; `default-groups` is `["dev", "case"]`; `pyproject.toml` itself is edited by the
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

## 15. Consumers: may assume, must not touch

**Docsite (WP8a).** May assume: the public names, version rule, docs page names, citation and math
syntax, the bibliography path, the derivation entry points and the generated-page names and location,
and the docstring style; that `uv run pytest` is green on `main`; that the build commands of section 11
and the staging command of section 13 are its to implement. Must not touch: `src/`, `derivation/`,
`examples/`, the technical docs pages (a front-matter block or link fix needs the owning package's
agreement), `pyproject.toml` and `uv.lock` except through the driver.

**Paper (WP10, with the outputs of WP12).** May assume: the case modules, functions, parameter names,
regimes, data headers and figure names of sections 7 and 8, the estimator attributes of section 4, the
boundary of section 3; that figures and data are committed and stable. Must not touch: data files,
figures and case modules other than `examples/adcs/case.py`; the docsite files; the derivation chain.
Its build is the paper command of section 11, delivered to `_site/paper/`; the paper is committed executed.

**Release machinery (WP8b).** May assume: one version source (section 5), the `publish.yml` and
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
| technical | `src/`, `derivation/`, `tests/` (except carve-outs), the technical docs pages (`method.md`, `why-and-how.md`, `preconditioning.md`, `api.md`, `limitations.md`), `docs/superpowers/`, the case modules, notebook, `data/`, `figures/`, `model_v2/`, `experiments/` and `case-model.md` under `examples/adcs/`, `.github/workflows/test.yml`, `README.md`, `.python-version` |
| process | `work-packages/` (except carve-outs), `CLAUDE.md` |
| WP14 | `work-packages/interface-contract.md`, `work-packages/interface-contract.toml`, `tests/test_interface_contract.py` |
| WP8a | `mkdocs.yml`, `overrides/`, `site/`, `scripts/`, `.github/workflows/publish.yml`, `tests/test_site.py`, `docs/index.md`, `docs/case.md`, `docs/api-reference.md`, `docs/generated/` |
| WP10 | `paper/`, `examples/adcs/case.py`, `tests/test_paper.py`, `tests/test_case.py`, `docs/references.bib`, `docs/literature.md` |
| WP12 | none yet; declared by an additive amendment when its scope is approved |
| WP8b | `CHANGELOG.md`, `LICENSE`, `.github/workflows/release.yml` |
| driver | `pyproject.toml`, `uv.lock`, `.gitignore` |

Links from one side's file to another side's are allowed; no file is shared beyond links.

## 17. Known gaps (R-11)

Open conformance gaps, recorded and not fixed here; each names the closing package.

| Gap | Closed by |
|---|---|
| The docstring of `src/hyperbolic_trade_space/__init__.py` says package code arrives in later work packages | WP8b |
| `scripts/` does not exist | WP8a |
| `docs/generated/` does not exist (built by `scripts/build_generated.py`) | WP8a |
| `mkdocs.yml`, `site/index.html`, `paper/myst.yml`, `.github/workflows/publish.yml`, `scripts/stage_site.py` do not exist | WP8a (`paper/myst.yml`: WP10) |
| `docs/api-reference.md` does not exist | WP8a |
| `.gitignore` ignores `site/` (the root index source) and lacks `_stage/` | WP8a (edit by the driver) |
| `pyproject.toml` has no `paper` group; `docs` is not in `default-groups` | WP10 and WP8a (edit by the driver) |
| The WP8a draft names the workflow `pages.yml` and a script `assemble_site.py`; the contract names `publish.yml` and `stage_site.py` | WP8a follows the contract |
| `docs/references.bib` and `docs/literature.md` are assigned to WP10; later technical edits go through an amendment | WP10 |
| The Oracle protocol is stated but not yet pinned | WP15 |

## 18. Skip list

The test skips each clause below, with its reason, until the file exists, then enforces it.

| Clause | File | Reason | Closed by |
|---|---|---|---|
| R-5 generated pages script | `scripts/build_generated.py` | WP8a delivers the generated-pages script | WP8a |
| R-7 docsite configuration | `mkdocs.yml` | WP8a delivers the docsite configuration | WP8a |
| R-6 API reference stub | `docs/api-reference.md` | WP8a delivers the presentation-owned stub | WP8a |
| R-7 Pages workflow | `.github/workflows/publish.yml` | WP8a delivers the Pages workflow | WP8a |
| R-12 local staging command | `scripts/stage_site.py` | WP8a delivers the staging command | WP8a |
| R-7 root index source | `site/index.html` | WP8a delivers the root index | WP8a |
| R-7 paper configuration | `paper/myst.yml` | WP10 delivers the paper configuration | WP10 |
| R-3a Oracle protocol | `examples/adcs/experiments/oracle.py` | WP15 delivers the protocol; pinned by additive amendment | WP15 |

# WP14 — Scope of work: Interface contract (technical ↔ presentation)

| | |
|---|---|
| **Status** | DRAFT. Approved only by the recorded act below. Nothing in this package is executed before then. |
| **Supervisor (accountable)** | mzargham |
| **Repository** | `DynamicalSystemsGroup/hyperbolic-trade-space` (local: `/Users/z/Documents/GitHub/posynomial-invariant-form`); work on `dev`, merged to `main` at acceptance |
| **Approval record** | Verbal approval in chat, quoted verbatim in `work-packages/WP14-decisions.md` |
| **Acceptance record** | Verbal acceptance in chat, quoted verbatim in `work-packages/WP14-decisions.md`, after `work-packages/WP14-review.md` |

## Purpose

The supervisor, 2026-11-08, verbatim: "yes but let's assert an interface contract between the
technical work and the presentation layer work so they can proceed in parallel. the docsite, the
paper publishing, and eventually the pypi release machinery need to stay stable even as the content
evolves. so we should be able to pin that interface so i can iterate on content and the release
machinery and publication flow in parallel".

Today the presentation packages (WP8a the site skeleton, WP10 the paper, WP12 the search, WP8b the
release) would each discover the technical side's paths, entry points and commands by reading code,
and the technical side (WP13 now, WP12 later) could rename any of them without knowing. This package
writes down the surface the two sides meet at, pins it in a contract document, and adds a test that
fails when the repository drifts from it. It writes no content and no presentation machinery.

## Goals

- G1. A contract document names, for each thing the presentation layer consumes, its path, entry
  point or command, format, and what the presentation layer may assume; and, for each thing the
  technical side owns, what it promises not to break.
- G2. The contract says how it is changed (an amendment), who may change what (file ownership by
  side), and how the two sides stay disjoint (no shared files beyond links).
- G3. A test asserts the contract against the repository, runs in the default `uv run pytest`
  with no network, and fails with a message that names the contract clause broken.
- G4. The contract is stated so that the three presentation outputs of the roadmap (docsite, paper,
  release machinery) can each be built against it in parallel with the technical work, and so the
  supervisor can iterate on content and on the release and publication flow independently.

## Non-goals

- No docsite, no `mkdocs.yml`, no root `index.html`, no `paper/`, no `myst.yml`, no workflow, no
  release, no changelog: those are WP8a, WP10, WP8b. WP14 only pins what they will meet.
- No change to package code, derivations, narrative pages or data (WP13 and later packages own them);
  the contract describes and asserts what exists, and records mismatches it finds as follow-ups
  rather than fixing them.
- No decision on the paper's content, the docsite's navigation, or the PyPI timing (deferred by the
  supervisor).
- No new tooling dependency: the contract test uses the standard library and what is already locked.
- No freeze of content: prose, numbers in prose, figures' appearance and the data may evolve; the
  contract pins where they live, how they are produced and what shape they have.

## Deliverables

| ID | Deliverable | Serves |
|---|---|---|
| D-1 | `work-packages/interface-contract.md` *(default)*: the contract document (sections in R-1 to R-8) | G1, G2, G4 |
| D-2 | `work-packages/interface-contract.toml` *(default)*: the machine-readable manifest of the pinned items (paths, commands, public names, formats, version rule), which the test reads and the document quotes | G1, G3 |
| D-3 | `tests/test_interface_contract.py`: asserts the manifest against the repository and the document against the manifest | G3 |
| D-4 | A link to the contract from `work-packages/README.md` (breakdown row and Status table) and from `CLAUDE.md` *(default; links only)* | G2 |
| D-5 | `work-packages/WP14-decisions.md` (approval record) and, at the gate, `WP14-review.md` | all |

## Requirements

The contract document has the sections below; the stated paths are the defaults and are quoted
from the repository as of this draft (re-read at execution, because WP13 is concurrently adding
to `src/` and `docs/`).

| ID | Requirement | Checked by |
|---|---|---|
| R-1 | **Package surface.** The contract pins the import name `hyperbolic_trade_space`, the distribution name `hyperbolic-trade-space`, and the public names exported in `__all__` of `src/hyperbolic_trade_space/__init__.py` *(default: the list is a floor, additive growth allowed; today `HyperbolicTradeSpace`, `LogAffinePreconditioner`, `TradeSpaceRegressor`, `frontier_in_original_units`, `make_configured_frontier_data`, `make_frontier_data`, `select_temperature`, `tension_report`, `__version__`; the names WP13 adds, such as the certificate functions, enter the manifest when WP13 is accepted, by the amendment rule R-8)*. Submodules the presentation layer may import: `plotting`, `gaps`, `solvers`, `coordinates`, `datasets`, `preconditioning`, `predictive`, `tensions`, `tuning`. The fitted-attribute and method names the paper reads (`termination_`, `conditioning_` and the per-facet report fields) are pinned by name once they exist. | Test: every pinned name imports; every listed name is in `__all__`; a removed or renamed name fails the test |
| R-2 | **Version string.** One authoritative version: `pyproject.toml` `[project].version`, mirrored by `hyperbolic_trade_space.__version__` *(default)*; the contract states the format (PEP 440, `MAJOR.MINOR.PATCH`), the current value (`0.0.1`), that the release machinery (WP8b) is the only thing that changes it, and that the presentation layer reads it, never writes it. | Test: the two values are equal and PEP 440 valid; the manifest value equals both (so a bump without an amendment fails) |
| R-3 | **Case module and data.** The case code lives under `examples/adcs/` and is importable with `pythonpath` as configured in `pyproject.toml` (`.`, `src`, `examples/adcs`) *(default)*; the contract pins the modules and functions the paper and notebooks call (`k_terms`: `load_metrics`, `make_conditioner`, `fit_k`, `select_tau`, `reports`, `facet_record`, `certificate`, `run_regime`, `main`; `generate_dataset`: `generate`, `generate_cubesat`, `main`; `design_space`: `sample_designs`, `evaluate_design`; `cubesat_model`, `adcs_sim`, `make_check_designs`; the two SysML files), the regime names (`primary`, `stock`) and the committed data files in `examples/adcs/data/` (`adcs_designs_cubesat_gains.csv` the primary, `adcs_designs_cubesat.csv` the baseline, `adcs_designs.csv`, `check_designs_cubesat.csv`, `check_predictions_cubesat.csv`) with their column schema (header line and dtypes of the attribute and configuration columns the case reads) and the rule that the files are committed, seeded and regenerated only by a package whose scope says so. | Test: functions exist with the pinned signatures (parameter names); each CSV exists, parses, and carries the pinned columns; `k_terms.run_regime` runs on a small `n_max` sample |
| R-4 | **Figures.** Figures the presentation layer embeds are produced by named functions or scripts into `examples/adcs/figures/` *(default)*; the contract pins the directory, the file naming (`NN_name.png`, `k3_<kind>_<regime>.png`), the format (PNG), and the producing command (`uv run python examples/adcs/k_terms.py`; the notebook for `01_` to `09_`); the presentation layer treats figures as read-only inputs and never writes there. Whether figures are consumed as committed files or regenerated at build is OD2's neighbour and is fixed by OD1. | Test: the pinned figure names exist and are valid PNGs; the producing script's CLI entry exists |
| R-5 | **Derivation ledger and generated pages.** `uv run python derivation/run.py` is the entry point: it runs the chain L1 to L14 (`CHAIN_NAMES` in `derivation/run.py`), prints the assumption audit and exits 0 on success, non-zero on a failed lemma; lemma modules are `derivation/lemma_NN_<name>.py`, each exposing the interface `derivation/run.py` already uses *(default: pinned to the current one)*; lemma numbers are never reused or renumbered (new lemmas take the next number); the contract pins the location the generated pages are written to (`docs/generated/`, git-ignored, built by `scripts/build_generated.py`, which WP8a writes) and the page names (`derivations.md`, `verification.md`) as the names the docsite will link, but not their prose. | Test: `derivation.run` imports and its `CHAIN` is non-empty and ordered; module names match the pattern with no gaps or duplicates in the numbering; the `scripts/build_generated.py` clause is checked once WP8a has delivered it (the test skips that clause until the file exists, and the skip is listed in the document) |
| R-6 | **Documentation sources.** The docsite reads Markdown in `docs/` (`method.md`, `why-and-how.md`, `preconditioning.md`, `api.md`, `limitations.md`, `literature.md`, `references.bib`) and the notes under `docs/superpowers/notes/` (excluded from navigation); the contract pins file names the navigation may link, the citation syntax (`[@key]` against `docs/references.bib`), the math syntax (LaTeX in `$...$` and `$$...$$`), and the rule that the technical side adds pages but renames none without an amendment. Presentation files (`mkdocs.yml`, `docs/index.md` and other site-only pages, `docs/generated/`, `index.html` at the site root, `paper/`, `myst.yml`, `.github/workflows/publish.yml`, release files) belong to the presentation side. | Test: each pinned page exists, ends in `.md`, every `[@key]` in them resolves in the bib (already covered by `tests/test_references.py`; this test calls its helper rather than duplicate it); no presentation-owned path is touched by the technical side's files list in the manifest |
| R-7 | **Build and publish interface.** The contract fixes the commands and outputs the machinery shares: tests `uv run pytest`; docsite `uv run --group docs mkdocs build --strict` into `_site/docs/` *(default)*; paper `uv run myst build --html` into `_site/paper/` *(default)*; root `index.html` copied to `_site/index.html`; Pages deployed by `.github/workflows/publish.yml` from `main` only (`dev` never deploys); the `docs` dependency group in `pyproject.toml` is owned by the presentation side and the `dev` and `case` groups by the technical side; paths inside `_site/` are the public URLs (`/`, `/docs/`, `/paper/`) and are stable. The branching rule of `work-packages/README.md` applies. | Test: `pyproject.toml` dependency groups and `[tool.uv]` default groups match the manifest; `uv lock --check` is already a CI step; the build commands are asserted as strings in the manifest, and executed only in WP8a's and WP10's own tests |
| R-8 | **Change control.** A change to the contract is an amendment: a PR-or-commit that edits `interface-contract.md` and the manifest together, says what changed, why, and which side it affects, and is approved by the supervisor verbally with the quote in `work-packages/WP14-decisions.md` *(default)*. The technical side promises no pinned item is removed or renamed without one; additions (new modules, new `__all__` names, new pages, new figures) do not need an amendment but must be added to the manifest in the same commit, which the test enforces as a floor. A deprecation (a pinned item replaced) names the replacement, keeps the old name for one amendment cycle and states when it goes. | Test: the manifest records `contract_version` *(default: an integer starting at 1)*; the document carries the same number; each amendment appends a row to the document's change log; the test fails when they disagree |
| R-9 | **File ownership.** WP14 may create: D-1 to D-5 above and nothing else. WP14 may edit only to add links: `work-packages/README.md`, `CLAUDE.md`. WP14 must not edit any file that WP13 owns: `docs/method.md`, `docs/api.md`, `docs/limitations.md`, `docs/why-and-how.md`, `derivation/`, `src/`, `docs/superpowers/notes/notation.md`, `docs/superpowers/notes/abstraction-gaps.md`, `docs/superpowers/notes/k3-cubesat.md`; nor `pyproject.toml`, `uv.lock`, `examples/`, `.github/`. The document states the ownership table by side (technical, presentation, shared-by-link-only). | Inspect `git diff --stat` for the delivery range: only the D-1 to D-5 paths and the two link edits appear; a test or a grep in the review confirms no WP13-owned path changed |
| R-10 | **Disjointness is checkable.** The contract lists, per presentation package (WP8a, WP10, WP12 where it touches presentation, WP8b), the files it may create or edit, and the test asserts these sets are pairwise disjoint and disjoint from the technical side's set. | Test on the manifest sets |
| R-11 | **Mismatches are recorded, not fixed.** Where the repository today differs from what the contract needs (for example the version string in `__init__.py` versus the docstring's "arrive in later work packages", no `scripts/` directory yet, no `docs/generated/`), the document lists the item as an open conformance gap with the package that closes it. | Inspect the document's "Known gaps" section; each gap has a closing package |

Delivery is on `dev` with commits prefixed "WP14: " *(default)*; every push passes the local checks
(`uv run pytest`, `uv run ruff check .`, `uv run ruff format --check .`, `uv lock --check`, the
attribution grep); no AI attribution lines.

## Definition of good

- The two sides can be worked on by different agents, or by the supervisor and an agent, on the same
  day, with each reading only the contract and its own side; a presentation author never needs to
  open `src/` to know what to call, and a technical author never needs to open the site config to
  know what must not move.
- The contract is short enough to be read in ten minutes and exact enough that the test is the
  review.
- The test failure messages say which clause and which side broke it and what the amendment path is.
- The manifest is the single source for the facts the document quotes, so the two cannot drift.

## Definition of good enough

- D-1 to D-5 exist at the stated paths; R-1 to R-11 are each met with their stated check.
- `uv run pytest` passes with `tests/test_interface_contract.py` included, and the test fails when
  a pinned item is removed or renamed (shown once in the review by a deliberate temporary break, not
  committed).
- The document covers the four consumers: docsite (WP8a), paper (WP10, WP12 outputs it reads),
  release machinery (WP8b), and the technical side (WP13 onward), each with a one-paragraph "what
  you may assume" and "what you must not touch".
- The two open decisions below are recorded as decided in the contract, with the supervisor's quote.
- The supervisor can say in chat which WP8a and WP10 files are his to iterate on without asking the
  technical side, by reading R-9 and R-10.

## Definition of done

Good enough is met, **no open item remains unresolved**, and the supervisor has accepted the work by the acceptance record above.

## Agent's defaults

- Contract location and format *(default)*: `work-packages/interface-contract.md` with the manifest
  `work-packages/interface-contract.toml` (TOML parsed with `tomllib` from the standard library); not
  under `docs/`, so the docsite navigation is not affected and the contract is not published as
  content. Appears in D-1, D-2.
- Test location *(default)*: `tests/test_interface_contract.py`, in the default test run, no network,
  no kernel, no build of the site or paper. Appears in D-3.
- Public surface as a floor *(default)*: pinned names may grow, never shrink or rename without an
  amendment. Appears in R-1, R-8.
- Single version source *(default)*: `pyproject.toml`, mirrored by `__version__`; WP14 asserts equality
  and does not change either. Appears in R-2.
- Case code stays under `examples/adcs/` *(default)*: the paper's "case code as a tested module"
  (WP10) imports from there; moving it is a WP10 amendment to this contract. Appears in R-3.
- Figures and data are inputs to the presentation layer, read-only; changes to them are made by a
  technical package and announced in the manifest. Appears in R-3, R-4.
- Generated pages live in `docs/generated/`, git-ignored, produced by `scripts/build_generated.py`
  (the WP8 approved design); the contract pins the names, WP8a writes the script. Appears in R-5.
- Site layout as approved in `WP8-decisions.md` ("Amendment 1 revised"): root `index.html`, MkDocs
  under `/docs/`, mystmd under `/paper/`, one Pages site, deployed from `main` only. Appears in R-7.
- Amendment approval is verbal with the quote recorded in `WP14-decisions.md`, in line with the
  repository's approval convention; additive changes need no approval but must update the manifest.
  Appears in R-8.
- Contract version is an integer, starting at 1; the change log is a table in the document. Appears in R-8.
- Link edits to `work-packages/README.md` and `CLAUDE.md` are the only edits outside new files. Appears in R-9.
- Conformance gaps are listed, not fixed; the closing package is named by the agent from the
  breakdown (WP8a, WP10, WP8b, WP13). Appears in R-11.
- Test skip rule *(default)*: a clause about a file a later package delivers (`scripts/build_generated.py`,
  `mkdocs.yml`, `myst.yml`, `publish.yml`) is skipped with a stated reason until the file exists, and
  becomes enforced once present; the skip list is printed in the document. Appears in R-5, R-7.
- Commit prefix, local checks and attribution rule as the other packages. Appears in the delivery paragraph.

## Open decisions (for the supervisor)

- **OD1.** Is the paper executed at build time or committed already executed? This fixes what the
  publishing machinery may assume about the paper and who owns the figures and numbers it shows.
  Options: (a) committed executed: `paper/paper.ipynb` and `supporting_material.ipynb` are stored
  with their outputs, the build (`myst build --html`) never starts a kernel, the author re-executes
  and commits when content changes, CI and Pages need no case dependencies for the paper; (b) executed at
  build: the build runs the notebooks (`myst build --execute`) from the lock with the `case` group,
  outputs are not committed, a changed technical API breaks the paper build until the paper is
  updated, and the build is slower and needs the `case` dependencies and the data in CI; (c) executed
  at release only: committed unexecuted on `dev`, executed and committed by the release step before
  the merge to `main`.
- **OD2.** Is the docsite's API reference generated from the docstrings or hand-written? This fixes
  whether a signature change on the technical side flows to the site by itself or needs a presentation
  edit, and whether numpydoc docstrings are part of the pinned contract. Options: (a) generated
  (`mkdocstrings` as WP8 D-3 approved; docstrings are pinned as the source, the page
  `docs/api-reference.md` is a presentation-owned stub, and `docs/api.md` stays WP13's hand-written
  overview); (b) hand-written (`docs/api.md` is the only API page, the technical side updates it with
  each signature change, and no `mkdocstrings` dependency); (c) generated into the paper's
  supporting material as well (the same extraction feeds both, which couples the paper's build to
  the docstring format).

Unresolved before the gate: OD1, OD2, and the Agent's defaults list as one item.

## Oracle signature (added by the PM for consistency with the WP15 draft)

The callable interface between the cubesat model and the analysis (`Oracle` protocol: `config_names`,
`attribute_names`, `flag_names`, `__call__(configuration) -> dict`, `evaluate(designs) -> DataFrame`) is
stated in `work-packages/WP15-scope-of-work.md`, section "The oracle signature". The contract pins the
frozen pair `cubesat_model.measure` and `sample_designs` today (R-3) and adopts the `Oracle` protocol
by an additive amendment (R-8) when WP15 is accepted.

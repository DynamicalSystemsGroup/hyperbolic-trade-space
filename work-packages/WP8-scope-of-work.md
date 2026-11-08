# WP8 — Scope of work: Site and first release

| | |
|---|---|
| **Status** | DRAFT. Approved only by the recorded act below. Nothing in this package is executed before then. |
| **Supervisor (accountable)** | mzargham |
| **Repository** | `DynamicalSystemsGroup/hyperbolic-trade-space` (local directory: `/Users/z/Documents/GitHub/posynomial-invariant-form`; renamed by the supervisor to `hyperbolic-trade-space` before WP8 executes, see Preconditions) |
| **Approval record** | Verbal approval in chat, quoted verbatim in `work-packages/WP8-decisions.md` |
| **Acceptance record** | Verbal acceptance in chat, quoted verbatim in `work-packages/WP8-decisions.md`, after the review report `work-packages/WP8-review.md` |

## Purpose

All the content exists as repository files: the method (WP1 derivations, WP2 to WP3 code, WP6 narrative, WP5 literature) and, after WP7, the case notebook. WP8 turns it into a published, reproducible GitHub Pages site paired with the executable specification, following spec §9 and the framing note (`docs/superpowers/notes/presentation-framing.md`: Tall's three worlds, glass-box seams, machine verification versus human validation), and cuts the first release. It is the last package of the breakdown; release controls (branch protection and PR-based gating) come after the first release.

## Goals

- G1. A MkDocs Material site configured from the existing Markdown, with pages: Home (a landing page with one card per artifact, mapped to the three worlds), Why and how to use it, Mathematics, Derivations (generated ledger), Preconditioning, Case: ADCS trade study (the rendered notebook), Verification and validation (generated), API and API reference, Extensions and limitations, Literature (from the bibliography).
- G2. Generated pages: `scripts/build_generated.py` writes the derivation ledger and lemma status page and the verification and validation summary page into `docs/generated/` at build time.
- G3. A publishing workflow modelled on the ADCS and hc-marimo workflows: test and derivation run, strict site build, deploy to GitHub Pages on `main` only, build without deploy on pull requests.
- G4. The first release: version `0.1.0`, tag, release notes, a GitHub release, and a TestPyPI dry run (not PyPI) to rehearse packaging; the license file.
- G5. The site is verified: a strict build succeeds, every formula and citation resolves, every internal link resolves.

## Non-goals

- No change to the content of the accepted packages (code, derivations, narrative, bibliography, notebook) except what the site build strictly requires (front matter, link fixes, a docs index), each recorded; substantive content defects are reported as follow-up work.
- No re-execution of the notebook in CI: it is rendered as committed.
- No release controls (branch protection, required reviews, PR-merge acceptance records): they follow the first release, by the supervisor's earlier decision.
- No publication to PyPI: only a TestPyPI dry run is made (supervisor's decision OD1).
- No custom domain, analytics or theme development beyond configuration.

## Deliverables

| ID | Deliverable | Serves |
|---|---|---|
| D-1 | `mkdocs.yml`: site configuration (Material theme, `pymdownx.arithmatex` with MathJax, `mkdocs-jupyter`, `mkdocstrings[python]`, `mkdocs-bibtex`), navigation, repository link | G1 |
| D-2 | `docs/index.md`: landing page with cards per artifact (method, derivations, toolkit, case, literature, verification) mapped to the three worlds, and a "start wherever suits you" paragraph | G1 |
| D-3 | `docs/case.md` (or a navigation entry) rendering `examples/adcs/adcs_trade_study.ipynb` through `mkdocs-jupyter`, and `docs/api-reference.md` using `mkdocstrings` | G1 |
| D-4 | `scripts/build_generated.py` and its tests | G2 |
| D-5 | `.github/workflows/publish.yml` | G3 |
| D-6 | Release artifacts: version bump, `CHANGELOG.md`, `LICENSE` (MIT, 2026 Dynamical Systems Group), annotated tag, GitHub release with notes, TestPyPI upload of the built wheel and sdist | G4 |
| D-7 | `tests/test_site.py` (configuration, link and citation resolution, generated-page content) | G5 |
| D-8 | `work-packages/WP8-decisions.md` (approval record) | G1–G5 |

## Requirements

| ID | Requirement | Checked by |
|---|---|---|
| R-1 | `uv run --group docs mkdocs build --strict` succeeds from a clean clone, with the `docs` group installed from the lock, producing the full site with no warnings (broken links, missing pages and unresolved citations are errors) | reviewer runs the command in a fresh clone |
| R-2 | The navigation contains all pages of G1, in the order of spec §9, each page naming the world it serves (embodied, symbolic or formal) in a short line | inspect `mkdocs.yml` and the pages |
| R-3 | Math renders: display and inline formulas from `docs/method.md` and `docs/preconditioning.md` appear in the built HTML through MathJax; a smoke check finds the arithmatex markers for the displayed formulas of a sample page | `tests/test_site.py` (built HTML contains the math markers) |
| R-4 | Citations render: every `[@key]` in the docs resolves through `mkdocs-bibtex` to an entry of `docs/references.bib`, and the Literature page lists the bibliography | strict build; `tests/test_site.py` |
| R-5 | `scripts/build_generated.py` writes `docs/generated/derivations.md` (the L1–L10 results with titles, statements, axioms used; the axiom ledger with the DERIVED, POSITED, INHERITED, REGULARITY and FALLBACKS sections including each condition's interpretive role and failure mode, produced by running the derivation chain) and `docs/generated/verification.md` (test counts by area from a pytest collection, the sklearn compatibility check counts and the documented expected failure, the lemma PASS list, the cross-check tests, and a "validated by a human" section stating what is not machine-verified); the generated files are gitignored and recreated at build time | `uv run python scripts/build_generated.py` then inspect; `tests/test_site.py` checks the content against `derivation/axioms.py` and the lemma modules |
| R-6 | The Derivations page ledger equals the axiom ledger printed by `derivation/run.py` (same ids, tags, statements, roles and failure modes) | `tests/test_site.py` |
| R-7 | The API reference is generated by `mkdocstrings` from the package docstrings for every exported name, and `docs/api.md` is the narrative companion; no docstring renders with errors | strict build |
| R-8 | The Case page renders the committed executed notebook with its outputs and figures, without executing it | built HTML contains the notebook outputs; the build does not call a kernel |
| R-9 | The landing page has one card per artifact with working links, and the framing (Tall's three worlds, glass-box seams, verify with the machine and validate as a human) follows `presentation-framing.md` | inspection; link check |
| R-10 | `.github/workflows/publish.yml`: checkout, `astral-sh/setup-uv`, `uv sync --locked` (with the `docs` group), `uv run pytest`, the derivation run, `scripts/build_generated.py`, `uv run mkdocs build --strict`, `actions/upload-pages-artifact`, `actions/deploy-pages` with the permissions and environment `github-pages`; deploy only on pushes to `main`; pull requests build without deploying; actions pinned to current versions as in the existing workflows | inspect; a workflow run on a pull request builds and does not deploy; a run on `main` deploys |
| R-11 | The deployed site is reachable at the Pages URL (https://dynamicalsystemsgroup.github.io/hyperbolic-trade-space/) and the main pages load (home, mathematics, derivations, case, API, literature, V&V) | reviewer fetches the pages after deployment |
| R-12 | The first release exists: the version in `pyproject.toml` and `__version__` agree (0.1.0); `LICENSE` is present with the MIT text and the copyright line "Copyright (c) 2026 Dynamical Systems Group"; `CHANGELOG.md` summarizes the packages WP0 to WP7; an annotated tag `v0.1.0` exists; a GitHub release carries the notes and links the site; the tag points at a commit whose CI is green; `uv build` produces a wheel and an sdist that pass `twine check`, and they are uploaded to TestPyPI (a dry run; the PyPI upload is not made) and install from TestPyPI into a clean environment with `import hyperbolic_trade_space` working | `git tag -l`, `gh release view`, `uv build`, `twine check`, a clean-environment install from TestPyPI |
| R-13 | `tests/test_site.py` runs in the default `uv run pytest`: configuration parses, every nav page exists, every relative link in `docs/*.md` resolves, generated pages contain the required sections; no network access is needed | run it |
| R-14 | Suite, linters and lock pass and nothing outside scope changed: `uv run pytest`, `uv run ruff check .`, `uv run ruff format --check .`, `uv lock --check`; `git diff --stat` shows only the deliverable paths, `.gitignore`, `pyproject.toml` and `uv.lock` (only for the version and docs-group pins), recorded front-matter or link fixes in `docs/` and `work-packages/` | run the commands; inspect the diff |
| R-15 | No AI attribution lines; commits authored as Michael Zargham; CI green on every push; the release commit's CI is green | `git log` grep returns 0; `gh run list` |

## Definition of good

- A visitor can land on the site, choose any of the three worlds as an entry point and find the others one click away; the derivations, the code and the case visibly agree, and the site says where the machine verified and where a human must validate.
- The site is reproducible: every command is `uv run`, the build uses the lock, and the generated pages come from running the code, not from copies.
- Honest about status: conditions and limitations are visible, the extensions are marked documented-not-built, and the V&V page lists the one documented expected failure with its reason.
- The release is small and clear: version, notes and links, with nothing published that the supervisor did not decide.

## Definition of good enough

- Deliverables D-1 to D-8 exist at the stated paths.
- R-1 to R-15 pass as checked, with evidence in the review report.
- Non-goals untouched (no content changes beyond recorded front-matter and link fixes, no release controls, no kernel execution in CI).

## Definition of done

Good enough is met, **no open item remains unresolved**, and the supervisor has accepted the work by the acceptance record above.

## Preconditions

- The supervisor has renamed the GitHub repository to `hyperbolic-trade-space` (OD2, "Rename first, then WP8"); the driver has updated `origin` and the repository paths and URLs in the documents; WP8 builds the site and the Pages URL under the final name. If this has not happened when WP8 is to start, WP8 does not start.
- GitHub Pages is enabled for the repository with source "GitHub Actions" (the supervisor's setting).
- TestPyPI credentials are the supervisor's to provide: a TestPyPI API token stored as a repository secret (`TEST_PYPI_API_TOKEN`) or a trusted-publisher registration for the project name on TestPyPI. Without it, the TestPyPI part of R-12 cannot be done and WP8 stops at that step and tells the driver (a precondition, not a defect).

## Agent's defaults

All marked *(default)* where they appear; the supervisor approves or changes the list as one item. Execution waits for the acceptance of WP7 (the Case page) and for the preconditions below.

- Site tooling *(default)*: MkDocs Material, `pymdownx.arithmatex` (generic, MathJax loaded from the CDN version pinned in `mkdocs.yml`), `mkdocs-jupyter` (`execute: false`, `include_source: false`), `mkdocstrings[python]` with the numpydoc docstring style, `mkdocs-bibtex` reading `docs/references.bib`; versions pinned in the `docs` dependency group and the lock (the group exists; extra pins are added if the build requires them).
- Site layout *(default)*: `docs_dir: docs`; navigation Home, Why and how to use it (`why-and-how.md`), Mathematics (`method.md`), Derivations (`generated/derivations.md`), Preconditioning (`preconditioning.md`), Case: ADCS trade study (the notebook), Verification & validation (`generated/verification.md`), API (`api.md`), API reference (`api-reference.md`), Extensions and limitations (`limitations.md`), Literature (`literature.md`); `docs/superpowers/` and `docs/references.bib` are excluded from the navigation (`exclude_docs`).
- Landing page *(default)*: hand-written `docs/index.md` using Material grid cards, in the tone of the ADCS and hc-marimo landing pages: a sentence on the idea, "start wherever suits you", and cards for the method (formal world), the derivations and verification (formal and operational), the toolkit and API (operational), the case notebook (embodied), the literature and limitations.
- Notebook page *(default)*: the notebook is included by `mkdocs-jupyter` from `examples/adcs/adcs_trade_study.ipynb` via a symlink-free copy step in the build (`scripts/build_generated.py` copies it into `docs/generated/`), so the committed notebook stays the single source.
- `scripts/build_generated.py` *(default)*: pure standard library plus the project's modules and `subprocess` for `pytest --collect-only -q`; writes Markdown; derivation ledger from `derivation.run.run_chain` and `derivation.axioms`; fails (non-zero exit) if the chain fails; `docs/generated/` is gitignored (already in `.gitignore` from WP0).
- Workflow *(default)*: triggers `push` to `main`, `pull_request` to `main` and `workflow_dispatch`; `concurrency: pages`; build job on `ubuntu-24.04` with the `opensysml` runtime cache step copied from `test.yml` if the test step needs it (`REQUIRE_OPENSYSML=1`); deploy job needs the build job, `permissions: pages: write, id-token: write`, environment `github-pages`, `if: github.ref == 'refs/heads/main'`; pinned `actions/checkout@v5`, `astral-sh/setup-uv@v7`, `actions/upload-pages-artifact@v4`, `actions/deploy-pages@v4`.
- Strictness *(default)*: `mkdocs build --strict`; known benign warnings (if any) are silenced explicitly in `mkdocs.yml` with a comment, never by dropping `--strict`.
- Release *(default)*: version `0.1.0` in `pyproject.toml` and `__version__` (currently 0.0.1); `CHANGELOG.md` in "Keep a Changelog" style listing WP0 to WP7 outcomes; annotated tag `v0.1.0` created on the commit that passes CI after the version bump; GitHub release created with `gh release create v0.1.0 --notes-file` linking the site and the notebook; the tag, the GitHub release and the TestPyPI upload are created only after the supervisor's approval of this scope (approval of the scope is the authorization for the release it names: tag, GitHub release and TestPyPI dry run; no PyPI upload).
- Link fixes *(default)*: relative links between pages are normalized to the MkDocs form (`page.md#anchor`); the `[@key]` citation syntax is unchanged; front matter is added only where Material needs a title.
- Tests *(default)*: `tests/test_site.py` uses `yaml.safe_load` (PyYAML is pulled in by mkdocs; imported lazily and skipped with a clear failure message, not silently, if the `docs` group is absent), regular expressions and the built site directory when present; the full-build test runs `mkdocs build --strict` into a temporary directory and is marked to run in the default suite only when the `docs` group is installed in CI (CI installs it through the default groups: the `docs` group is added to `default-groups` in this package, a recorded `pyproject.toml` and `uv.lock` change).
- TestPyPI *(default)*: built with `uv build`; uploaded in the publish workflow job `testpypi` (manual `workflow_dispatch` input or on the release tag only, never on pull requests) with `pypa/gh-action-pypi-publish@release/v1` pointed at `https://test.pypi.org/legacy/`, using the secret above or trusted publishing; the dry run is verified by installing from `https://test.pypi.org/simple/` with `--extra-index-url https://pypi.org/simple/` into a clean environment; a failed upload because the version exists is not retried by bumping the version without the driver.
- License *(default)*: standard MIT text, `Copyright (c) 2026 Dynamical Systems Group`; `pyproject.toml` already declares MIT and keeps `authors = [{ name = "Michael Zargham" }]`.
- Commits prefixed "WP8: "; configuration and pages, then generated-page script and tests, then the workflow, then the version bump and release notes, then the status table and decisions file; every push green and attribution-free *(default)*.

## Open decisions (for the supervisor)

None. Every item was resolved through the decision loop, recorded verbatim in `work-packages/WP8-decisions.md`: OD1 "TestPyPI dry run only", OD2 "Rename first, then WP8", OD3 "MIT, copyright DynamicalSystemsGroup". Decided: 3, deferred: 0, raised: 0. The Agent's defaults list above is the one remaining item for the supervisor to approve or change at the scope gate.

## Amendment 1 (2026-11-08, pending re-approval; REVISED the same day, see the note at the end of this section): MkDocs → mystmd

What changes and why, per scope-of-work section 6. On 2026-11-08 the supervisor redirected the
case notebook into a paper built with mystmd, the SciPy 2026 proceedings article as the reference
case (verbatim in `WP10-decisions.md`: "mystmd is fine but https://proceedings.scipy.org/articles/wdyr6752
as your reference case ... we still need it to read like a paper even with the supporting
materials available in the repo or in other pages in the myst cite"). MkDocs Material cannot
render the MyST directives the paper uses, so the site tooling changes; the purpose, the release
and the preconditions do not. Items below replace their originals; everything not named is as
approved.

- G1: "A mystmd site configured from the repository's `myst.yml` (delivered by WP10), whose index
  is the paper, with the supporting-material notebook, the docs pages (why and how, mathematics,
  preconditioning, API, extensions and limitations, literature), the generated derivation ledger
  and verification pages, and a landing section of cards mapped to the three worlds."
- G2: `scripts/build_generated.py` writes MyST Markdown into `docs/generated/`.
- D-1: `myst.yml` (from WP10) plus the site and deployment settings; the `docs` dependency group
  drops `mkdocs-material`, `mkdocs-jupyter`, `mkdocstrings[python]`, `mkdocs-bibtex` and gains
  `mystmd` (the PyPI wrapper, pinned; Node is provided by the wrapper or by `actions/setup-node`
  in CI, recorded as a default to approve at re-approval).
- D-3: the API reference page is produced by a small script that renders the package's numpydoc
  docstrings to MyST Markdown (mystmd has no Python autodoc), or is dropped in favour of
  `docs/api.md` alone — a default for the supervisor to approve at re-approval.
- D-5 and R-10: the workflow runs `uv run myst build --html` (strict: warnings fail the build) and
  deploys `_build/html`.
- R-1, R-3, R-4, R-7, R-8: restated for mystmd (clean strict build from a clean clone; math and
  citations render through mystmd's own MathJax and bibliography handling; the paper and the
  supporting notebook render from committed outputs without a kernel).
- R-2: navigation per `myst.yml`'s table of contents, in the order paper, supporting material,
  docs pages, generated pages, literature.
- Agent's defaults "Site tooling", "Site layout", "Landing page", "Notebook page", "Strictness",
  "Link fixes": restated for mystmd at re-approval; "Workflow", "Release", "TestPyPI", "License",
  "Tests" unchanged in substance.
- Dependency: WP8 now waits for WP11 (readability loops on the paper), per the breakdown of
  2026-11-08.

Re-approval: verbal, quoted in `work-packages/WP8-decisions.md`, after WP10's scope exists (the
`myst.yml` WP8 deploys is WP10's deliverable, so the restated defaults are written then).

**Revision of Amendment 1 (2026-11-08, late; `WP8-decisions.md`, "Amendment 1 revised").** The
supervisor's decision, verbatim: "MkDocs docsite + MyST paper, one Pages site". The items above that
replaced MkDocs are withdrawn: the docsite is built with MkDocs Material as approved (G1, D-1 to
D-4, R-1 to R-9 unchanged, with the Case page now linking the paper rather than rendering the
retired WP7 notebook), and the paper is a separate mystmd build from `paper/` (WP10) deployed under
`/paper/` of the same GitHub Pages site by the same workflow; D-5 and R-10 run both builds; D-7's
tests cover both; the landing page carries a card for the paper. The dependency on WP11 stands.

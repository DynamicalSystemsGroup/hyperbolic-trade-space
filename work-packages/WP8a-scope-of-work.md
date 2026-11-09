# WP8a — Scope of work: Site skeleton up

| | |
|---|---|
| **Status** | DRAFT. Approved only by the recorded act below. Nothing in this package is executed before then. |
| **Supervisor (accountable)** | mzargham |
| **Repository** | `DynamicalSystemsGroup/hyperbolic-trade-space` (local directory: `/Users/z/Documents/GitHub/posynomial-invariant-form`) |
| **Approval record** | Verbal approval in chat, quoted verbatim in `work-packages/WP8a-decisions.md` |
| **Acceptance record** | Verbal acceptance in chat, quoted verbatim in `work-packages/WP8a-decisions.md`, after the review report `work-packages/WP8a-review.md` |

## Purpose

The breakdown of 2026-11-08 splits WP8: the supervisor wants a working draft of the documentation
visible early, and the presentation machinery (the site, the paper's deployment target, later the
release) stable while content evolves ("the docsite, the paper publishing, and eventually the pypi
release machinery need to stay stable even as the content evolves", `README.md`). WP8a puts the site
skeleton up on GitHub Pages: a thin hand-written root index that splits to the MkDocs docsite under
`/docs/` and to a `/paper/` slot, with the generated derivation-ledger and verification pages, deployed
from `main` on merge. It is built against the WP14 contract so that content (WP13 now, WP10 and WP12
later) and machinery iterate in parallel. It is not the release (WP8b) and it does not edit the
content of `docs/*.md`.

Inherited from WP8 (approved, `WP8-decisions.md`): G1 to G3 and G5, D-1 to D-5 and D-7, R-1 to R-11,
R-13 to R-15, as restated by "Amendment 1 revised" (MkDocs docsite + MyST paper, one Pages site; root
index "pretty thin html like in the hc-marimo repo"; "a hook for talks and other items later"). The
release goal G4, D-6 and R-12 stay with WP8b. This document replaces WP8's text for the parts it
carries; WP8's own scope gets a short amendment recording the split when this one is approved
(a record edit, not new scope).

## The WP14 contract items this package consumes

WP14 is being drafted in parallel. WP8a is written against "the WP14 contract" and needs these items
from it, pinned. Where the contract names them differently, WP8a follows the contract's names and
records the mapping.

| # | Item needed from the WP14 contract | Used for |
|---|---|---|
| C-1 | The package's import name, version source (`pyproject.toml` and `__version__`) and its exported names (`__all__`) | API reference, the package card, the check that every exported name appears in `docs/api.md` |
| C-2 | The derivation entry points: `derivation.run.run_chain`, `derivation.run.CHAIN`, the axiom ledger in `derivation.axioms` (`AXIOMS`, tags, `by_tag`, `fallbacks`), and the result shape (lemma number, title, statement, axioms used) | `scripts/build_generated.py` (derivation ledger) |
| C-3 | The verification inputs: the pytest collection command and its area grouping (file to area map), the sklearn-conformance test files and their `*_EXPECTED_FAILURES` dictionaries, the lemma PASS list | `scripts/build_generated.py` (V&V page) |
| C-4 | The docs page set and file names (`why-and-how.md`, `method.md`, `preconditioning.md`, `api.md`, `limitations.md`, `literature.md`, `references.bib`), the stable heading anchors other pages link to, and the rule that pages may be edited in content but not renamed or deleted without a contract change | `mkdocs.yml` navigation, link tests |
| C-5 | The generated-page contract: output directory `docs/generated/` (gitignored), file names `derivations.md` and `verification.md`, required section headings of each | `scripts/build_generated.py`, `tests/test_site.py` |
| C-6 | The build commands and their order (generated pages, docsite build, paper build) and the site layout: Pages root, `/docs/`, `/paper/`, and the public URL `https://dynamicalsystemsgroup.github.io/hyperbolic-trade-space/` | the workflow, `scripts/assemble_site.py`, `mkdocs.yml` `site_url` |
| C-7 | The paper slot: the directory (`paper/`), the build entry point WP10 will provide, the output directory and the base URL it must build for (`/hyperbolic-trade-space/paper/`), and the rule that WP10 replaces only the paper step | the `/paper/` slot, the single `paper` step in `scripts/assemble_site.py` |
| C-8 | The data, figure and notebook paths the docs may link to (e.g. `examples/adcs/`), and which are committed versus built | `docs/case.md` link targets, link tests |
| C-9 | The "world" labelling convention: how a page declares which of Tall's three worlds it serves (front-matter key and values) | R-2 of WP8 |
| C-10 | The test-marker and group convention for tests that need the `docs` group (and that the contract's own test is part of the default `uv run pytest`) | `tests/test_site.py` |

If WP14's contract changes any of C-1 to C-10 after WP8a is approved, the contract test (WP14's) fails
first; WP8a follows by a recorded fix, not by an amendment, as long as the change is a rename or
relocation rather than a new capability.

## Goals

- G1. A MkDocs Material docsite under `/docs/` of the Pages site, with the pages: Home, Why and how to
  use it, Mathematics, Derivations (generated), Preconditioning, Case (a short page pointing to the paper
  slot and the case code), Verification and validation (generated), API, API reference, Extensions and
  limitations, Literature; each page names the world it serves.
- G2. `scripts/build_generated.py` writes the derivation ledger and lemma status page and the
  verification and validation page into `docs/generated/` at build time, from running the code.
- G3. A root `index.html` (thin hand-written HTML after hc-marimo's `site/index.html`): one card each for
  the paper, the docs and the package, a "start wherever suits you" paragraph, a source link; built to
  grow, so talks and later artifacts are added as cards.
- G4. A `/paper/` slot: a placeholder page, deployed at the paper's final URL, which WP10 replaces by
  publishing the paper there without touching the rest of the site.
- G5. One Pages workflow that tests, builds everything into `_site/` and deploys it on a merge to
  `main`.
- G6. The skeleton is verified: strict build, every internal link resolving, the workflow and layout
  asserted by tests, and the deployed site reachable after the merge.

## Non-goals

- Not the release: no version bump, `CHANGELOG.md`, `LICENSE`, tag, GitHub release or TestPyPI/PyPI upload
  (WP8b).
- No content edits to `docs/*.md` (WP13 owns those files while it executes). WP8a may only add a
  front-matter block at the top of an existing page and fix a link, each listed in the decisions file;
  anything else it finds is reported as a defect for the owning package.
- No paper: no `myst.yml`, no notebook-to-paper work, no Node/mystmd installation (WP10, WP11).
- No rendering of the retired WP7 notebook in the docsite.
- No custom domain, analytics, theme development beyond configuration and one small template override
  for the world line.
- No release controls (branch protection, required reviews), by the supervisor's earlier decision.
- No change to the package, derivation or test code of other packages.
- No kernel execution in CI.

## Deliverables

| ID | Deliverable | Serves |
|---|---|---|
| D-1 | `mkdocs.yml`: Material theme, `pymdownx.arithmatex` (MathJax), `mkdocstrings[python]`, `mkdocs-bibtex`, `site_url` under `/docs/`, navigation, repository link, `exclude_docs` for `superpowers/` and `references.bib` | G1 |
| D-2 | `docs/index.md` (docs home: a map of the pages to the three worlds, link back to the root) and `docs/case.md` (points to the paper slot and the case code), `docs/api-reference.md` (mkdocstrings), `overrides/` (one partial rendering the world line from front matter) | G1 |
| D-3 | `scripts/build_generated.py` and its tests | G2 |
| D-4 | `site/index.html` (the root landing page) and `site/paper/index.html` (the placeholder) | G3, G4 |
| D-5 | `scripts/assemble_site.py`: builds `_site/` (root index, `_site/docs/` from MkDocs, `_site/paper/`); the paper step is one function WP10 replaces | G3, G4, G5 |
| D-6 | `.github/workflows/pages.yml` | G5 |
| D-7 | `tests/test_site.py` | G6 |
| D-8 | `pyproject.toml` and `uv.lock` (the `docs` group pins; `docs` added to `default-groups`); `.gitignore` entry for `_site/` | G1, G6 |
| D-9 | Front-matter blocks and link fixes in `docs/*.md`, listed individually | G1 |
| D-10 | `work-packages/WP8a-decisions.md` (records) and a row in the status table of `work-packages/README.md` | all |

## File ownership

| Path | Owner during WP8a | Rule |
|---|---|---|
| `mkdocs.yml`, `overrides/`, `site/`, `scripts/`, `.github/workflows/pages.yml`, `tests/test_site.py`, `docs/index.md`, `docs/case.md`, `docs/api-reference.md` | WP8a (creates) | after acceptance, WP10 owns only the paper function in `scripts/assemble_site.py`; WP8b owns nothing here |
| `docs/generated/` | WP8a's script (gitignored, never committed) | |
| `docs/method.md`, `why-and-how.md`, `preconditioning.md`, `api.md`, `limitations.md`, `literature.md`, `references.bib` | WP13 (content) | WP8a: front matter at the top and listed link fixes only, applied last and rebased onto WP13's state, so a content change never conflicts with a block of lines at the file head |
| `pyproject.toml`, `uv.lock` | shared | WP8a changes only the `docs` group, `default-groups` and the lock entries they cause; WP8b later changes the version |
| `.github/workflows/test.yml` | WP0 (accepted) | untouched |
| `derivation/`, `src/`, `tests/` other than `test_site.py`, `examples/`, `docs/superpowers/` | other packages | read-only for WP8a |
| `work-packages/WP8a-*`, the WP8a row of `README.md` | WP8a | |

## Requirements

| ID | Requirement | Checked by |
|---|---|---|
| R-1 | `uv run python scripts/assemble_site.py` succeeds from a clean clone with the lock installed (`uv sync --locked`), running `mkdocs build --strict`, producing `_site/index.html`, `_site/docs/index.html`, `_site/paper/index.html`; broken links, missing pages and unresolved citations are errors | reviewer runs it in a fresh clone |
| R-2 | The docs navigation contains all pages of G1 in the order of spec section 9; each page shows a one-line world label (embodied, symbolic or formal) from its front matter (C-9) | inspect `mkdocs.yml` and the built pages; `tests/test_site.py` |
| R-3 | Math renders: displayed formulas of `method.md` and `preconditioning.md` appear in the built HTML as arithmatex markers | `tests/test_site.py` on the built output |
| R-4 | Citations resolve: every `[@key]` in the docs resolves to an entry of `docs/references.bib` and the Literature page lists the bibliography | strict build; `tests/test_site.py` |
| R-5 | `scripts/build_generated.py` writes `docs/generated/derivations.md` (every lemma of the chain with number, title, statement and axioms used; the axiom ledger by tag, with each condition's role and failure mode, produced by running the chain through C-2) and `docs/generated/verification.md` (test counts by area from a pytest collection, the sklearn-conformance check counts with each documented expected failure and its reason, the lemma PASS list, and a "validated by a human" section stating what is not machine-verified); it exits non-zero if the chain fails | run it; `tests/test_site.py` compares the content with `derivation.axioms` and the expected-failure dictionaries |
| R-6 | The ledger on the Derivations page equals the one `derivation/run.py` prints (same ids, tags, statements, roles, failure modes) | `tests/test_site.py` |
| R-7 | The API reference is generated by `mkdocstrings` from the numpydoc docstrings for every exported name (C-1); no docstring renders with errors | strict build; `tests/test_site.py` |
| R-8 | The root `index.html` is thin hand-written HTML (no framework, no build step, no external scripts, light and dark colour schemes as in hc-marimo), has one card each for the paper, the docs and the package with working relative links (`paper/`, `docs/`, the API page and the repository), a "start wherever suits you" paragraph, and a source link; a comment marks where a new card goes | inspection; `tests/test_site.py` resolves each card href against the assembled `_site/` |
| R-9 | `_site/paper/index.html` is a placeholder that says the paper is in preparation, links back to the root and to the docs, and is the only thing WP10 must replace (C-7) | inspection; `tests/test_site.py` |
| R-10 | `.github/workflows/pages.yml`: checkout, `astral-sh/setup-uv`, `uv sync --locked`, `uv run pytest`, `uv run python scripts/assemble_site.py`, `actions/upload-pages-artifact` of `_site`, `actions/deploy-pages` with `pages: write`, `id-token: write` and environment `github-pages`; the deploy job runs only on `main`; triggers push to `main` and `workflow_dispatch` | inspect; `tests/test_site.py` parses the YAML and asserts these; a dispatch run on `dev` builds and does not deploy |
| R-11 | After the merge of the delivery into `main`, the workflow run on `main` is green and the pages load at the public URL: root, `docs/`, `docs/method/`, `docs/generated/derivations/`, `docs/generated/verification/`, `docs/api-reference/`, `docs/literature/`, `paper/` | reviewer fetches them after deployment |
| R-12 | `tests/test_site.py` runs in the default `uv run pytest` with no network access: configuration parses, every nav page exists, every relative link in `docs/*.md`, `site/index.html` and `site/paper/index.html` resolves, generated pages contain the sections of C-5, the workflow asserts as in R-10; the full-build test runs `mkdocs build --strict` into a temporary directory | run it |
| R-13 | Suite, linters and lock pass and nothing outside scope changed: `uv run pytest`, `uv run ruff check .`, `uv run ruff format --check .`, `uv lock --check`; `git diff --stat` against the start commit shows only paths in the ownership table, and in `docs/*.md` only the listed front-matter blocks and link fixes | run the commands; inspect the diff |
| R-14 | No AI attribution lines; commits authored as Michael Zargham; local checks green on every push to `dev`; CI green on the merge to `main` | `git log` grep returns 0; `gh run list` |

## Definition of good

- A visitor lands on a page that is quick to read, in the supervisor's style of the hc-marimo and ADCS
  pages, and chooses the paper, the docs or the package; every choice leads somewhere real, and the paper
  slot is honest about being in preparation.
- The docs are readable as a working draft today and keep working as WP13, WP10 and WP12 change the
  content, because everything the site depends on is named in the WP14 contract.
- The generated pages come from running the code, and the V&V page says plainly what the machine verified
  and what a human must validate.
- Adding a card (a talk, a deck) is one block in `site/index.html`; swapping the paper in is one function
  in `scripts/assemble_site.py`.

## Definition of good enough

- Deliverables D-1 to D-10 exist at the stated paths.
- R-1 to R-14 pass as checked, with evidence in the review report.
- The non-goals are untouched: no release artifacts, no `docs/*.md` content change beyond the listed
  front matter and link fixes, no paper build.

## Definition of done

Good enough is met, **no open item remains unresolved**, and the supervisor has accepted the work by the acceptance record above.

## Preconditions

- The WP14 contract is accepted (C-1 to C-10 pinned and its test in the default suite). WP8a does not
  start before that.
- GitHub Pages is enabled for the repository with source "GitHub Actions" (the supervisor's setting).
- The repository is renamed to `hyperbolic-trade-space` (done, `WP8-decisions.md`).
- The live check (R-11) needs a merge of `dev` into `main` (`git merge --no-ff dev`), which carries the
  package's delivery; see OD1.

## Agent's defaults

All marked *(default)* where they appear; the supervisor approves or changes the list as one item.

- Source of the root page *(default)*: `site/index.html` (as in hc-marimo), copied to `_site/index.html`; the repository root keeps no `index.html`.
- Docsite output *(default)*: `mkdocs build --strict -d _site/docs`, `docs_dir: docs`, `site_url` set to the public `/docs/` URL; `docs/superpowers/` and `references.bib` excluded from the site.
- Assembly *(default)*: `scripts/assemble_site.py` (standard library plus `subprocess`) runs the generated-pages script, the MkDocs build and copies the root index and the paper slot, so the workflow and local reproduction run the same single command and the logic is testable.
- Docs tooling *(default)*: `mkdocs-material`, `pymdownx.arithmatex` (generic, MathJax from a CDN version pinned in `mkdocs.yml`), `mkdocstrings[python]` (numpydoc style), `mkdocs-bibtex`; `mkdocs-jupyter` is dropped from the `docs` group because the notebook is retired from the docsite; `docs` is added to `default-groups` so the full-build test runs in the default suite (a recorded `pyproject.toml` and `uv.lock` change).
- World label *(default)*: front-matter key per C-9 (provisionally `world: embodied | symbolic | formal`), rendered as one line under the page title by a small Material template override in `overrides/`; if the contract names no key, `world` is used.
- Docs home and Case page *(default)*: `docs/index.md` is a short map of the pages to the three worlds and a link back to the root; `docs/case.md` is a short page that links the paper slot and the case code (`examples/adcs/`) and says the case is told in the paper.
- Package card *(default)*: links to the API page of the docs and the GitHub repository and shows an install-from-source line; no PyPI link, since PyPI is deferred ("pypi deferred for pending feedback from friends and collaborators").
- Placeholder wording *(default)*: "The paper is in preparation" with links to the root and the docs, same styling as the root page.
- Workflow *(default)*: `.github/workflows/pages.yml`; triggers push to `main` and `workflow_dispatch` only, in keeping with the dev-branch rule that Actions run when content merits it (this drops WP8's "pull requests build without deploying", recorded as a departure); `concurrency: pages`; `ubuntu-24.04`; the `opensysml` runtime cache step copied from `test.yml` if the test step needs it; `actions/checkout@v5`, `astral-sh/setup-uv@v7`, `actions/upload-pages-artifact@v4`, `actions/deploy-pages@v4`; the deploy job needs the build job and runs `if: github.ref == 'refs/heads/main'`.
- Strictness *(default)*: `--strict` always; a benign warning, if any, is silenced explicitly in `mkdocs.yml` with a comment.
- Generated script *(default)*: standard library plus the project's modules and `subprocess` for `pytest --collect-only -q`; Markdown output; sklearn counts from the same collection, expected failures read from the `*_EXPECTED_FAILURES` dictionaries named in C-3.
- Front matter and link fixes *(default)*: front matter only where C-9 requires the world key or Material needs a title; link fixes only where `--strict` or the link test finds a broken relative link, each listed with file, line, before and after in `WP8a-decisions.md`; applied last and rebased onto the current `dev`.
- Tests *(default)*: `yaml.safe_load` for the config and workflow; regular expressions and the built directory; no network; the full-build test builds into a temporary directory.
- Evidence before the merge *(default)*: a local assembly served with `python -m http.server`, a browser look at the root, the docs and the placeholder (per the supervisor's browser-in-the-loop practice), and a `workflow_dispatch` build run on `dev` showing the build job green and the deploy job skipped.
- Commits prefixed "WP8a: ", on `dev`; order: contract-bound script and tests, docs config and pages, root index and slot, workflow, front matter and link fixes, status and decisions; attribution-free *(default)*.

## Open decisions (for the supervisor)

- **OD1.** Where does the live-site check sit in acceptance? The workflow can deploy only from `main`, so the live URL can be checked only after a merge. Options: (a) acceptance waits for the merge of `dev` into `main` and judges the live site (R-11 inside good enough); (b) acceptance is judged on the local assembly plus the green `dev` build run, then the merge to `main` follows and R-11 is checked as a post-merge confirmation that does not reopen acceptance.
- **OD2.** Does the public site say it is a working draft? The deployment makes an unfinished site public at the Pages URL. Options: (a) a visible "working draft" line on the root page, the docs home and the paper placeholder; (b) no label, the paper placeholder alone says "in preparation".
- **OD3.** What does the paper card on the root page do until WP10 publishes? Options: (a) it is shown and links to the placeholder page; (b) it is shown as "coming" without a link; (c) it is omitted from the root page until the paper exists.

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

## Gate outcomes (2026-11-08, `WP8a-decisions.md`)

- OD1: "Accept on the staged site; live check after the merge". OD2: "no label we don't deploy to
  main and thus github pages until we have an actual first release. in the mean time its local host
  review loops". Consequences, replacing the corresponding items above: the Pages workflow
  (`.github/workflows/pages.yml`) triggers on the release tag (`v*`) and `workflow_dispatch` only,
  never on pushes to `main`; no deployment happens in WP8a; R-11 (the live URL) moves to WP8b and is
  checked at the first release; WP8a's acceptance evidence is the staged localhost assembly (one
  command, WP14 R-12) reviewed by the supervisor plus a green `workflow_dispatch` build run on
  `dev` that builds without deploying. OD3 becomes a default: the paper card is shown on the root
  page and links to the placeholder. `pyproject.toml` and `uv.lock` changes (the `docs` group pins,
  `default-groups`) are requested from the driver, who owns those files (WP14), not made by WP8a.
Link policy (supervisor, at the defaults): placeholder links that will be live at the first release
are allowed; `tests/test_site.py` lists them as expected-at-release, not broken; every such link goes
on `work-packages/release-punch-list.md` for the live check at WP8b; broken links found live are
fixed in a patch; no caveat text on the pages.


# WP8a, Amendment 2 (draft): the docsite for a user of the package

| | |
|---|---|
| **Status** | DRAFT amendment to `work-packages/WP8a-scope-of-work.md`. Approved only by the recorded act below. Nothing here is executed before then. WP8a stays HELD at its acceptance gate meanwhile. |
| **Supervisor (accountable)** | mzargham |
| **Approval record** | Verbal approval in chat, quoted verbatim in `work-packages/WP8a-decisions.md`; the same quote is copied into `work-packages/WP14-decisions.md` as the approval of interface contract version 2 (section "WP14 contract amendments") |
| **Acceptance record** | Verbal acceptance in chat after a second staged review of the localhost site and a green `workflow_dispatch` build on `dev`, quoted in `WP8a-decisions.md` |
| **Replaces** | WP8a goal G1, deliverables D-2 and D-9, requirements R-2, R-3, R-4, R-12 (as rewritten below), the "no content edits to `docs/*.md`" non-goal, and the `docs/*.md` rows of the ownership table. Everything else in WP8a, including "Gate outcomes", stands. |

## Purpose

At the staged-site review (2026-11-08) the supervisor held WP8a, verbatim: "hold until the doc site is
restructured. i think it can be thinned out. should be more scikit learn doc site like. don't force
things into the doc site that belong in the paper"; and "i need a seperation of concerns between the
paper and the doc site the doc site is for a user of the package. the paper is for someone who wants
to understand the how and why underneath"; and about the root page: "the top level page can include
the figure for how but it also needs text to summarize it".

The skeleton WP8a built carries the paper's material in the docsite: `docs/method.md` alone is about
11,900 words of lemma narrative, and the six hand-written pages total about 24,200 words. Amendment 2
turns the docsite into the documentation of a package (what scikit-learn's site is: Getting started,
User guide, API reference, Examples, Glossary, What's new), moves every how-and-why page out to the
paper's sources, and puts the summarizing paragraph under the root page's How figure. The staged review
is repeated afterwards.

The rule used throughout: **a package user needs it to run, read or trust a result: it stays (rewritten
short, for use); someone who wants to understand how and why underneath needs it: it moves.** Nothing a
user needs is left only in the paper; nothing that belongs in the paper is forced into the docsite.

## Goals (added to or replacing WP8a's)

- **G1' (replaces G1).** A MkDocs Material docsite under `/docs/` for a user of the package, shaped like
  the scikit-learn documentation: Home, Getting started, User guide, API reference, Examples, Theory in
  brief (one page), Further reading, Changelog, plus the generated Derivations and Verification pages
  (placement per OD1).
- **G7.** The how-and-why material leaves the docsite and is preserved as sources for the paper (WP10),
  with a table that says what each moved section is the source for.
- **G8.** The root page's How figure has a summarizing paragraph in the register's words.
- **G9.** Every deeper claim on the docsite links to a named paper section; the docsite never argues a
  result.

## Non-goals (added)

- No paper text: WP8a moves sources and writes the user's docsite. It writes no paper section and does
  not edit `paper/`. WP10 reads the preserved sources and must not edit `docs/*.md`.
- No new mathematics, lemma, derivation or package code; no docstring edits (the API reference renders
  the docstrings as they are; a docstring defect is reported to the technical side).
- No deletion of moved text from git history; no rewording of moved text (a verbatim snapshot).
- No deployment, no release (WP8b), no PyPI link.
- Not a rewrite of the docs' voice by invention: user pages restate only what the moved pages and the
  docstrings already say, shortened; any claim not already in them is not added.
- No embedded figures copied from `examples/adcs/figures/` (links only; contract section 8 treats them
  as read-only inputs).

## The docsite after the restructure

Navigation, in this order (the scikit-learn pattern: a short path to a first result, a guide per task,
a generated reference):

| Nav section | File | Budget (words) | What it carries (source) |
|---|---|---|---|
| Home | `docs/index.md` | 250 | What the package does in a paragraph, entry points to the sections below, links to the root and the paper (replaces the three-worlds table; see OD4) |
| Getting started | `docs/getting-started.md` | 400 | Install from source, the five-line example that runs, how to read its output, where to go next (`README.md`, `why-and-how.md` opening) |
| User guide | `docs/user-guide/overview.md` | 500 | The idea in use: tensions, not variance; the pipeline condition, fit, read; what you supply and get back (`why-and-how.md`) |
| | `docs/user-guide/conditioning.md` | 700 | `LogAffinePreconditioner`: orientation, shift, scaling, zeros, diagnostics, the pull-back to attributes (`preconditioning.md`, derivation parts dropped) |
| | `docs/user-guide/fitting.md` | 800 | `HyperbolicTradeSpace` at K = 1 and K > 1; parameters; choosing tau with `select_temperature`; what a fit returns (`api.md` stage 3 and K > 1) |
| | `docs/user-guide/tensions.md` | 700 | The tension report: contending set, exchange rates, the n-lemma, the participation threshold (`api.md`, `why-and-how.md`) |
| | `docs/user-guide/chart.md` | 600 | The chart, `score_samples` (log V), holes and white space, the plots (`api.md`, `why-and-how.md`) |
| | `docs/user-guide/prediction.md` | 350 | `TradeSpaceRegressor`: predicting metrics, coordinates and novelty from configuration (`api.md`) |
| | `docs/user-guide/termination.md` | 600 | Reading `termination_` and `conditioning_`: statuses, tolerances, what each means for a decision (`api.md` stopping record) |
| | `docs/user-guide/limitations.md` | 500 | Limitations as they bear on use: when a result misleads and what to check (`limitations.md` short part; long part moves) |
| API reference | `docs/api.md` | 300 | Short overview table of the public names, then `docs/api-reference.md` (mkdocstrings, generated, unchanged) |
| Examples | `docs/examples.md` (replaces `case.md`) | 400 | The cubesat case in brief: what was evaluated, what the tension report found, links to `examples/adcs/` and the paper's case section |
| Theory in brief | `docs/theory.md` | 700 | One page: the invariant form, V = 1, the chart, the n-lemma; each deeper claim is a link to a named paper section |
| Verification | `docs/generated/derivations.md`, `docs/generated/verification.md` | generated | Placement per OD1 |
| Further reading | `docs/further-reading.md` (replaces `literature.md`) | 300 | A short annotated pointer list; the survey is the paper's related-work section |
| Changelog | `docs/changelog.md` | 150 | What's new; starts per OD3 |
| (optional) Glossary | `docs/glossary.md` | 300 | The register's phrases in one line each (OD5) |

Hand-written total cap: **7,600 words** (today: about 9,200 in the user-facing pages plus about 15,000
in `method.md` and `literature.md`, which leave). Each page carries no displayed lemma, proof or
review text. `docs/superpowers/` is excluded from the site as now. Table-of-contents depth, page
titles and anchors are the Agent's defaults.

**Theory in brief** is a single page with five short sections: the invariant form (a weighted geometric
mean, V = 1 as the fitted reference surface), what V = 1 means in use (an improvement factor), the
chart (Z and log V, reversible), the n-lemma (which metrics contend, found and not assumed), and a
"Where each claim is argued" table: one row per deeper claim, the claim in one sentence, and a link to
the named paper section (provisional slugs in the table below). At most six displayed formulas, none
tagged as a lemma.

**Root page.** `site/index.html` keeps the figure and gains a paragraph under it *(default text, for the
supervisor's eye in the staged review)*:

> Read the map from the top. The foundation box is the invariant form: a weighted geometric mean V of
> the metrics, whose level V = 1 is the fitted reference surface and whose logarithm is the energy
> differential. The single-term core fits the weights and an offset to your designs as one convex
> problem. Four boxes use that fit: the chart (each design becomes a position along the frontier and a
> log V), the exchange rates between the metrics that contend, the correction for noise, and the
> pull-back to your raw attributes. The lower boxes extend the model to several facets, relate it to
> the Pareto boundary, and give the multi-facet algorithm its guarantees. Each box carries a badge,
> derived, checked numerically or open; the red box lists the open questions.

The paragraph replaces the one-line "The boxes are the reading order" sentence; thin HTML, no scripts,
light and dark, checked at desktop and 375 px.

## What moves out: the table for WP10

Everything below is preserved verbatim as a snapshot of the WP13-accepted text (commit `d7673c6`) in
`docs/superpowers/notes/paper-sources/` under the same file name (`method.md`, `literature.md`,
`limitations.md`, `preconditioning.md`, `api.md`, `why-and-how.md`), plus a `README.md` there holding
this table. Moved text is not deleted from git history. The paper homes are provisional (WP10 owns
the paper's structure and may rename them; the amendment's slug file, below, is how the docsite
follows). Word counts are for the section's own text.

**Provisional paper structure used below:** Preliminaries; Methods; Results; Discussion; Related work
(prior art); Appendix A (the register); Appendix B (conditions of the theory and lemma coverage);
Appendix E (abstraction gaps); Appendix D (the K > 1 solver and the three levels).

### `docs/method.md` (about 11,900 words; leaves the docsite entirely)

| Section (line) | Words | Stays on the docsite (rewritten for use) | Moves; source for paper section |
|---|---|---|---|
| Preamble and "Map and territory" (5) | ~316 | Nothing restated (a link only) | Policy paragraph in the body (Methods opening) |
| The pipeline and where the mathematics sits (32) | 265 | The pipeline in two sentences in User guide overview | Preliminaries |
| Conditions of the theory (54) | 1258 | One line per condition that bears on use, inside user-guide limitations | Methods (the conditions) and Appendix B (the table) |
| The model (95) | 445 | Theory in brief: the invariant form, V = 1 | Methods |
| The fit (151) | 796 | Fitting page says what is fitted, not why it converges | Results, theorem-style statements with proof sketches pointing to `derivation/` |
| What the stage learns, and why it is shape (258) | 1038 | none | Results (theorem-style) |
| Tensions, not variance (368) | 355 | Tensions page: the idea in use, two paragraphs | Results (theorem-style) |
| n-lemmas are discovered, not assumed (397) | 246 | Theory in brief and Tensions page: the n-lemma defined in two sentences | Results |
| Interpretation (417) | 830 | Tensions and Chart pages: how to read exchange rates and log V | Discussion |
| Novelty and white space (514) | 406 | Chart page: holes in use | Discussion |
| Prediction from configuration (550) | 139 | Prediction page | Methods (the model with covariates) |
| Lineage (562) | 232 | Further reading: one pointer | Related work |
| The posynomial and GGP extension (584) | 347 | Fitting page: K > 1 in use | Results (algorithm subsection) and Appendix D |
| The solver for small K (636) | 1214 | none | Results (algorithm) and Appendix D |
| Three levels of guarantee (736) | 2031 | Termination page: the statuses in use | Appendix D (body keeps the statement of each level) |
| What is proved, what is inherited, what is only observed (939) | 616 | none; one line in user-guide limitations | Abstraction-gaps appendix; policy paragraph in the body |
| Simplifying assumptions (973) | 903 | none | Abstraction-gaps appendix (Appendix E) |
| Research direction: kernel methods under the GGP constraint (1047) | 210 | Fitting page: one sentence "documented, not built" | Discussion (future work) |
| Summary of lemma coverage (1070) | 218 | none | Appendix B |

### The other pages

| Page (words) | Stays (rewritten for use) | Moves; source for |
|---|---|---|
| `index.md` (191) | Rewritten as Home | three-worlds table: paper (framing section) |
| `why-and-how.md` (1419) | Getting started (opening) and User guide overview, about 900 words together | "The frontier as V = 1", "What the fit certifies": Methods; the PCA contrast: Discussion; the idea text: paper introduction |
| `case.md` (113) | `examples.md` | none (a pointer page) |
| `preconditioning.md` (2093) | `user-guide/conditioning.md` (700): orientation, shift, scaling, zeros, diagnostics, pull-back | "What the theory asks of stage 2", "Invertibility" derivation, "Conditions under which these tools mislead" derivation parts: Methods and Appendix B; "A worked case in general terms" (307): paper's case section |
| `api.md` (3353) | `api.md` overview table (300); Stage 2, 3, 4 and K > 1 usage into the user-guide pages | Lemma and ledger-id citations: Appendix B; "Kernel methods (documented, not built)": Discussion; the K > 1 mathematics (about 500 of 814 words): Results and Appendix D |
| `api-reference.md` (108) | unchanged (generated) | none |
| `limitations.md` (2002) | `user-guide/limitations.md` (500): the limits that change what a user does | "Limits of the method" long text (966): Discussion and Appendix E; "What the contrast with PCA does and does not claim" (97): Discussion; "Extensions" (756): Discussion (future work) |
| `literature.md` (3066) | `further-reading.md` (300), a few annotated links | Entire survey, Appendix A (candidates dropped) and Appendix B (sources for the axioms): Related work and the references appendix |
| `generated/derivations.md`, `generated/verification.md` | per OD1 | per OD1 |
| the abstraction-gaps ledger (`docs/superpowers/notes/abstraction-gaps.md`, not under `docs/*.md`, unchanged) | docsite page only per OD2 | Appendix E (the ledger), with the policy paragraph in the paper body |

## File ownership (replaces the `docs/*.md` rows of WP8a)

| Path | Owner during Amendment 2 | Rule |
|---|---|---|
| `docs/*.md`, `docs/user-guide/`, `mkdocs.yml`, `overrides/`, `site/`, `scripts/`, `tests/test_site.py` | WP8a | WP13 is accepted, so the technical side no longer owns the six pages; WP10 does not edit them |
| `docs/superpowers/notes/paper-sources/` | WP8a creates once; read-only after | WP10 reads it (copies out what it needs); nothing else writes there; excluded from the site by the existing `superpowers/` rule |
| `docs/references.bib` | WP10 (unchanged) | keys not cited by the docsite remain valid; the docsite cites only keys that exist |
| `tests/test_docs.py`, `tests/test_narrative.py`, `tests/test_references.py`, `tests/test_notebook.py` | technical side, edited by WP8a for the repointing listed below only | each edit a repoint or a split, no assertion weakened, listed in `WP8a-decisions.md` |
| `docs/superpowers/` otherwise, `src/`, `derivation/`, `examples/` | other packages | untouched |

## WP14 contract amendments (contract version 2)

Per contract section 14 an amendment edits `interface-contract.md` and `interface-contract.toml` in one
commit, says what changed, why and which side it affects, and is approved verbally with the quote in
`WP14-decisions.md`. The amendments Amendment 2 needs:

1. **Pinned docs pages (section 2 `docs.pages`, section 10, section 15).** `docs.pages` becomes the new
   page list (every file in the navigation table above, hand-written ones only);
   `docs.presentation_pages` equals it plus `docs/api-reference.md`; `method.md` and `literature.md` are
   removed from the pinned set (removal needs this amendment); `why-and-how.md`, `preconditioning.md`
   and `case.md` are renamed or replaced as in the table. `docs/api.md` stays the hand-written overview
   and `docs/api-reference.md` stays generated, unchanged in name and role.
2. **Ownership (section 16, manifest `[ownership]`).** The five technical docs pages leave the technical
   side's set; the WP8a row gains `docs/*.md`, `docs/user-guide/`; the WP10 row loses `docs/literature.md`
   (the file leaves `docs/`) and keeps `docs/references.bib`.
3. **New pinned path.** `docs.paper_sources_dir = "docs/superpowers/notes/paper-sources/"`, created by
   WP8a, read-only afterwards; WP10 may assume its contents (section 15, Paper "may assume").
4. **Paper anchors (section 15, Paper "may assume" and "must provide").** New manifest key
   `docs.paper_section_slugs`: the named paper sections the docsite links to, as anchors under
   `/paper/` (provisional list in `scripts/paper_sections.toml`: preliminaries, methods, results,
   algorithm, discussion, related-work, appendix-a-register, appendix-b-conditions,
   appendix-c-gaps, appendix-d-solver, case). WP10 either builds these anchors or amends the list; the
   docsite's link test reads the list. Links to these anchors are expected-at-release (the release
   punch list), per the link policy of the gate.
5. **Section 17 known gaps.** The row "`docs/references.bib` and `docs/literature.md` are assigned to
   WP10" is rewritten: `literature.md` becomes a preserved source; the bibliography stays.
6. **Section 9 generated pages.** Unchanged if OD1 keeps them in the docsite; if they move, the page
   location in `derivation.generated_dir` and `derivation.generated_pages` changes in the same amendment.
7. **Change log row.** Version 2, today's date, the above, "both", approval quote.
8. **Route lists outside the contract.** `scripts/stage_site.py` and `tests/test_site.py` list
   `docs/method/` and `docs/literature/`; both change to the new routes; `release-punch-list.md` gains the
   paper-section links.

## Tests that follow the pages

| Test | Today | After |
|---|---|---|
| `tests/test_site.py` nav list, `test_world_lines_render`, math-marker test, punch-list routes | assert the eleven old pages, math in `method` and `preconditioning`, route `docs/method/` | assert the new nav set (see R-2' below); math-marker test targets `theory` (and `conditioning` if it carries inline math); world-line test per OD4; routes updated; new tests R-3' to R-8' below |
| `tests/test_docs.py` user-page assertions (`PAGES = preconditioning.md, api.md`: citations resolve, lemma ids in range, ledger ids exist, names in `api.md`, submodule names, statuses and tolerances documented) | on `preconditioning.md`, `api.md` | `PAGES` become the user-guide pages and `api.md`; "cites some lemma or ledger id" is asserted only on `theory.md` (user pages may name an id inline as a link, never state a lemma); exported names and submodule functions asserted over `api.md` plus user guide; statuses and tolerances over `termination.md` |
| `tests/test_docs.py` method assertions (Map and territory exactly once, three levels headings, new lemmas cited, statuses in method) | on `method.md` | move to a new `tests/test_paper_sources.py` pointing at `paper-sources/method.md`, so the assertions keep guarding the moved text; WP10 repoints it to the paper's sources; "not restated" (no page restates the policy) stays on the docsite pages |
| `tests/test_docs.py` register phrases and forbidden phrases | scan `docs/*.md` | register-phrase test scans the surviving docsite pages (glob now recursive, excluding `generated/` and `superpowers/`) and still requires all ten phrases, carried as: fitted reference surface, supporting envelope, Pareto boundary in `theory.md`; energy differential, level offset in `chart.md`; participation threshold, numerically zero in `tensions.md`; facet gap, assignment margin, stable radius in `termination.md`. Forbidden-phrase test scans the docsite and `paper-sources/` |
| `tests/test_narrative.py` (formula tags, lemma tags resolve, conditions table equals the ledger, referenced functions exist, spec matches the ledger, names and hygiene) | on `method.md`, `why-and-how.md`, `limitations.md` | repointed to the `paper-sources/` snapshots (constants only) and renamed in WP10 when the paper exists; `why-and-how` and `limitations` assertions that concern user text (hygiene: no emoji, no attribution) also run over the new docsite pages |
| `tests/test_references.py` (bib hygiene; every bib key cited in `literature.md`) | `docs/literature.md` | `LIT` points at `paper-sources/literature.md`; bib parsing tests unchanged; citation-resolve test also runs over docsite pages; WP10 repoints "every key cited" to the paper |
| `tests/test_notebook.py` line 248 (`"docs/method.md"` in the retired notebook's closing cell) | the notebook links `docs/method.md` on GitHub | assertion repointed to the preserved path or the clause dropped with the retired notebook; the notebook itself is not edited; the punch list notes its links |
| `tests/test_interface_contract.py` | parametrised over `docs.pages` | follows the manifest; needs no edit beyond the contract commit |

## Deliverables

| ID | Deliverable | Serves |
|---|---|---|
| D-11 | The docsite pages of the navigation table, at the stated paths, within budget; `mkdocs.yml` navigation; `docs/index.md` rewritten | G1', G9 |
| D-12 | `docs/superpowers/notes/paper-sources/` (six verbatim snapshots and `README.md` with the move table above) | G7 |
| D-13 | Root page paragraph in `site/index.html` | G8 |
| D-14 | `scripts/paper_sections.toml` and the docsite link checks; `scripts/stage_site.py` routes | G9 |
| D-15 | Contract version 2: edits to `interface-contract.md` and `.toml`, quote in `WP14-decisions.md` | G1', G7 |
| D-16 | Tests rewritten, split or repointed as in the table above; new `tests/test_paper_sources.py` | all |
| D-17 | `docs/changelog.md` per OD3; `docs/glossary.md` if OD5 says so | G1' |
| D-18 | The moved pages removed from `docs/`; `release-punch-list.md` updated; `WP8a-decisions.md` records; README status row | all |

## Requirements

| ID | Requirement | Checked by |
|---|---|---|
| R-2' (replaces R-2) | The navigation page set equals the table above (hand-written pages in that order, plus the generated pages per OD1); every nav page exists; no `method.md` or `literature.md` under `docs/` | `tests/test_site.py` compares `flatten_nav` with the list |
| R-3' (replaces R-3) | Math renders where used: displayed formulas appear as arithmatex markers on `theory.md`; inline math on user pages renders; MathJax pinned | `tests/test_site.py` on the built output |
| R-4' (replaces R-4) | Citations on docsite pages resolve (`[@key]` against `docs/references.bib`); Further reading renders its references | strict build; `tests/test_docs.py`; `tests/test_site.py` |
| R-15 | Word budgets hold: each page within its budget (code blocks and tables excluded), total at most 7,600 | `tests/test_site.py` counts words of the source pages |
| R-16 | No docsite page carries a lemma block, proof, "Proposition", "Corollary", `$$` tag comments or review prose: no match for `^\*\*(Lemma|Proposition|Corollary)`, `\bWP\d+\b`, `supervisor`, `reviewer`, `abstraction-gaps`, `\bG-\d+\b`; displayed formulas only on `theory.md`, at most six | `tests/test_site.py` regexes over `docs/**/*.md` (excluding `superpowers/` and `generated/`) |
| R-17 | Every deeper claim on `theory.md` links a named paper section: the "Where each claim is argued" table has no row without a link, and every link target (`../../paper/#slug`) is a slug of `scripts/paper_sections.toml`; the other pages link the paper only through those slugs | `tests/test_site.py`; the links are on the release punch list |
| R-18 | Getting started and user-guide code blocks run: each block marked as runnable executes on seeded synthetic data (`make_frontier_data`) and the five-line example prints without error | `tests/test_docs.py` extracts and executes the marked blocks, offline |
| R-19 | The staged site builds strict, with every internal link resolving; placeholder links to the paper and to release items are listed expected-at-release | `uv run python scripts/stage_site.py`; `uv run mkdocs build --strict`; `tests/test_site.py` |
| R-20 | The register-phrase test passes over the surviving pages with all ten phrases and no phrase list shortened; forbidden phrases absent from the docsite and from `paper-sources/` | `uv run pytest tests/test_docs.py` |
| R-21 | The preserved sources are verbatim snapshots of the six pages at `d7673c6` and the moved assertions pass against them | `git diff --no-index` of each snapshot against `git show d7673c6:docs/<page>`; `tests/test_paper_sources.py` |
| R-22 | The root page carries the paragraph under the figure; the page stays thin HTML with no scripts, light and dark; the card links resolve | `tests/test_site.py`; inspection at desktop and 375 px in the browser pane |
| R-23 | Contract version 2: the manifest and document agree; the contract test passes; the quote is in `WP14-decisions.md` | `uv run pytest tests/test_interface_contract.py` |
| R-24 | Suite, linters and lock pass; nothing outside the ownership table changed (`src/`, `derivation/`, `examples/`, `pyproject.toml`, `uv.lock` untouched); no AI attribution lines | `uv run pytest`, `uv run ruff check .`, `uv run ruff format --check .`, `uv lock --check`, `git diff --stat`, `git log` grep |
| R-25 | Separation of concerns holds on a cold read of the docsite: a package user can install, fit, read a tension report and the termination record from the docsite alone; nothing a reader of the paper needs to follow an argument is only on the docsite | the supervisor's second staged review (acceptance evidence) |

## Definition of good

- A user lands on a page that reads like scikit-learn's documentation: a first result in minutes, a
  guide per task, a generated reference, and one short page of theory that says plainly "the argument is
  in the paper" and links the exact section.
- The docsite is thin: no page makes the reader work through mathematics to run the package, and the
  paper's author finds, in `paper-sources/`, every section of text the docsite gave up, with a stated
  home.
- Adding a user-guide page, or changing a paper section name, is one edit and one test, because the paper
  links go through one slug file.

## Definition of good enough

- D-11 to D-18 exist at the stated paths; R-2' to R-4' and R-15 to R-25 pass with evidence in the review
  report.
- The staged site (`uv run python scripts/stage_site.py --serve`) has been reviewed by the supervisor a
  second time and a green `workflow_dispatch` build on `dev` is recorded.
- Non-goals untouched: no paper text, no package, derivation or docstring change, no deployment.

## Definition of done

Good enough is met, **no open item remains unresolved**, and the supervisor has accepted WP8a by the
acceptance record above (this closes the hold).

## Order of work

1. Snapshot the six pages to `paper-sources/` with the move-table `README.md`; commit (a revertible
   point; nothing removed yet).
2. Contract version 2 and `scripts/paper_sections.toml` (once the supervisor's approval is recorded).
3. Rewrite the tests first: nav set, budgets, forbidden-content, link checks, repointed and split
   assertions (red against the old site).
4. Write the pages in this order: Getting started, conditioning, fitting, tensions, chart, termination,
   prediction, Theory in brief, user-guide limitations, Examples, API overview, Further reading,
   Changelog (Glossary if chosen), Home; each page against its budget and the register phrases.
5. Remove the moved pages from `docs/`; update `mkdocs.yml`, `stage_site.py`, punch list.
6. Root page paragraph.
7. Strict build, staging, browser look at desktop and 375 px (browser pane), ruff and the suite.
8. Review report for acceptance; second staged review with the supervisor; dispatch build on `dev`.

## Estimate

About 16 to 22 hours of agent work in four sessions: snapshot, contract and tests (4 h); page writing
(8 to 10 h, about 0.6 h per page for 13 pages); root paragraph, build, staging and fixes (2 h); review
report and dispatch run (2 h). One review loop with the supervisor is expected, and a second pass on
wording after it.

## Agent's defaults

All marked *(default)* where they appear; the supervisor approves or changes the list as one item.

- Page names, directory (`user-guide/`), nav order and budgets in the navigation table *(default)*.
- The `d7673c6` snapshots with the same file names, plus a `README.md` carrying the move table, in
  `docs/superpowers/notes/paper-sources/` *(default)*; moved pages are removed from `docs/` in the same
  commit that adds the replacements, and git history keeps them.
- The root paragraph text above *(default)*, subject to the supervisor's edits in the staged review.
- Hand-written total cap 7,600 words, page budgets, the forbidden-content regexes and the six-formula
  limit on `theory.md` *(default)*.
- Paper links by slugs in `scripts/paper_sections.toml`, treated as expected-at-release links on the
  punch list *(default)*; the provisional slugs and the provisional paper structure above *(default)*.
- Examples page links only, no figures copied *(default)*.
- Runnable code blocks marked with a fence attribute and executed by a test *(default)*; the
  five-line example uses `make_frontier_data(300, 3, random_state=0)`, `HyperbolicTradeSpace(temperature=20.0)`,
  `fit`, and `tension_report` (verified to run while drafting this amendment).
- Test edits are repoints and splits only; no assertion is weakened or dropped *(default)*.
- MathJax from the pinned CDN stays; the world-line override is kept in `overrides/` whatever OD4 says.
- Commits prefixed "WP8a: ", on `dev`, attribution-free *(default)*.

## Open decisions (for the supervisor)

- **OD1.** Where do the generated Derivations and Verification-and-validation pages live? Options:
  (a) both stay in the docsite as a "Verification" section, as in the pages the staged review saw;
  (b) both move to the paper's supporting material (built into `/paper/`, generator and contract paths
  move with them) and the docsite carries one sentence and a link; (c) the docsite keeps only the
  Verification page (what the tests and checks cover, and what a person must validate) and the
  derivation ledger moves to the paper.
- **OD2.** Does the abstraction-gaps ledger get a docsite page? Options: (a) no, it is the paper's
  appendix only, and the user-guide limitations page links it; (b) yes, a short docsite page of the
  ledger as a table of "what the model assumes and where it can mislead", linked from the User guide.
- **OD3.** How does the Changelog start? Options: (a) empty, an "Unreleased" heading only, until WP8b
  writes the first release entry; (b) a first entry for 0.0.1 written now from the commit history;
  (c) no Changelog page until WP8b.
- **OD4.** Do the docsite pages keep the three-worlds "world line" (and the home page's worlds table)?
  Options: (a) keep a world line on every docsite page; (b) drop it from the docsite and keep the three
  worlds as the paper's framing only; (c) keep it only on Theory in brief and Verification.
- **OD5.** Does the docsite carry a Glossary page, as scikit-learn's does? Options: (a) yes, one line per
  register phrase and symbol a user meets (about 300 words); (b) no, the register stays the paper's
  Appendix A and the user guide defines terms where it uses them.

## Amendment 2: gate outcomes (2026-11-08, `WP8a-decisions.md`)

The draft above reads with these outcomes: OD1 "move both to the paper. and even there they are
likely going to be appendices" (no generated Derivations or Verification page on the docsite; the
script keeps producing them for the paper's build); OD2 "No docsite page; paper appendix only" (the
gaps ledger); OD3 "No page until WP8b" (changelog); OD4 "Drop it from the docsite" (world lines; the
`overrides/` partial for them is removed; contract item C-9 withdrawn in contract version 2); OD5
"yes to glossary but let's generate it programmatically rather than hand write it. you can make
glossary.yaml so that the source is skimmable but the glossary should be compiled from that not free
text" (`glossary.yaml` as the single source, compiled into the Glossary page by
`scripts/build_generated.py`, offered to WP10 as the register's source). Defaults approved as one
item: "Approve the defaults as listed". Decided 5, deferred 0, raised 0.

Further gate outcome (supervisor, at the approval question; verbatim in `WP8a-decisions.md`): G9 is
withdrawn: the docsite carries no citations into the paper for now; `scripts/paper_sections.toml`,
the paper-section slugs and the expected-at-release paper links in docs pages are removed from this
amendment, and contract version 2 drops its paper-anchors item. New requirement R-26: no leftover
reference to removed content anywhere in the docsite, its navigation, the site scripts or the
tests' route lists (checked by a test that scans the built docsite and the sources for the moved
file names, their old anchors, lemma tags, the generated-page names and the world key, and by the
strict build). Deferred, on the punch list: references from the docsite to the paper by stable
reference keys (a registry resolved at build time, like LaTeX labels), added after the paper and
its appendices are stable.

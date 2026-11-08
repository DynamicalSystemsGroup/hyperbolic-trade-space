# WP8 — Decision records

Records typed by the agent (driver session). Decisions are the supervisor's.

## Pre-approval decisions (2026-11-08)

- **OD1 (first release), verbatim choice:** "TestPyPI dry run only". Disposition: tag v0.1.0 and a
  GitHub release, plus a TestPyPI upload to rehearse packaging; PyPI later.
- **OD2 (timing vs repository rename), verbatim choice:** "Rename first, then WP8". Disposition: the
  supervisor renames the GitHub repository to `hyperbolic-trade-space` before WP8 executes; the driver
  then updates `origin` and the repository paths/URLs in the docs; WP8 builds the site and the Pages
  URL under the final name.
- **OD3 (license), verbatim choice:** "MIT, copyright DynamicalSystemsGroup". Disposition: add
  `LICENSE` (MIT, 2026 Dynamical Systems Group); `pyproject.toml` already declares MIT.

## Scope approval (approval gate)

- **Document:** `work-packages/WP8-scope-of-work.md` (OD1–OD3 applied; preconditions: renamed repo
  (done), Pages enabled with source "GitHub Actions", `TEST_PYPI_API_TOKEN` secret).
- **Date:** 2026-11-08
- **Supervisor (mzargham), verbatim:** "accept 4b and approve 7 and 8. given how long its been remember to send the notebook author to look at the acds-lifecycle-demo and hc-marimo repos and pages sites to get a sense of my style"
- **Disposition:** approved; defaults list approved as one item; open decisions: none. Executes after
  WP7's acceptance and once the preconditions hold. The same style instruction applies to the site.

## Acceptance (acceptance gate)

- pending `work-packages/WP8-review.md`

## Amendment 1 revised: MkDocs docsite plus a MyST paper, one Pages site (2026-11-08, late)

- Context: Amendment 1 (written at the paper's redirection) moved the whole site to mystmd. The
  supervisor's roadmap of the three outputs, verbatim: "update to a docsite (we can stick to make
  docs unless you think we need sphynx) * update to the paper (myst modeled after scipy
  proceedings)". Driver's question: MkDocs docsite plus MyST paper on one Pages site / keep mystmd
  for everything / separate deployments. **Supervisor (mzargham), verbatim:** "MkDocs docsite + MyST
  paper, one Pages site".
- Disposition: Amendment 1 is revised: the docsite stays MkDocs Material as originally approved
  (D-1, D-2, D-3, D-4, R-1 to R-9 as approved); the paper is a separate mystmd build from
  `paper/` (WP10's `myst.yml`) deployed under `/paper/` of the same Pages site by the same
  workflow (`mkdocs build --strict` into `_site/`, `myst build --html` into `_site/paper/`); the
  landing page and the docsite navigation link the paper; `tests/test_site.py` covers both builds.
  Sphinx is not needed. Re-approval of the revised amendment at WP10's scope gate, when the
  `myst.yml` it deploys exists.
- Layout, **supervisor (mzargham), verbatim:** "you can use an index page at the top level on github
  pages then spit to the paper and to the docs." Disposition: the Pages site has a hand-written
  index at its root (the landing page of D-2, in the tone of the ADCS and hc-marimo landing pages:
  one card for the paper, one for the docs, one for the package, "start wherever suits you"), the
  MkDocs docsite under `/docs/` and the mystmd paper under `/paper/`; the workflow builds both into
  `_site/docs/` and `_site/paper/` beside the root `index.html`.
- **Supervisor (mzargham), verbatim:** "that index page will serve as a hook for talks and other items
  later". Disposition: the root index is designed as a growing landing page (one card per artifact,
  as the ADCS and hc-marimo sites do), so talks, decks and later artifacts are added as cards without
  restructuring; WP8's D-2 says so.
- **Supervisor (mzargham), verbatim:** "the index can be pretty thin html like in the hc-marimo repo".
  Disposition: the root index is a thin hand-written `index.html` modelled on
  `/Users/z/Documents/GitHub/hc-marimo/site/index.html` (no framework, no build step; cards, a stack
  line, an audience note, a call to action per artifact, a source link at the foot); D-2 names it as
  the template.

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

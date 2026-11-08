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

- pending

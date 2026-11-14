# WP47 — Scope of work: release engineering and repository governance for v0.1

| | |
|---|---|
| **Status** | DRAFT. Approved only by the recorded act below; nothing is built before then. |
| **Supervisor (accountable)** | mzargham |
| **Repository** | `DynamicalSystemsGroup/hyperbolic-trade-space`; work on `dev` |
| **Approval record** | The supervisor's verbal approval, quoted verbatim in `work-packages/WP47-decisions.md` |
| **Acceptance record** | The supervisor's acceptance after `WP47-review.md`, and the TestPyPI dry run he runs with the assistant |

## Purpose

The supervisor's direction (`WP47-decisions.md`, verbatim): he publishes the package on PyPI with the assistant's help;
code owners, issue and pull-request templates and the other repository items are to be set up; he alone merges to
`main` for now and onboarding further maintainers must be straightforward; candidate releases go through `dev`;
semantic versioning. This package builds what the repository needs for that and hands him a checklist for the steps
only he can take (accounts, trusted publishers, branch protection).

## Goals

- G1. **The package builds and publishes by a workflow he triggers, with no secret in the repository:** `uv build`
  produces the wheel and sdist from `pyproject.toml` (version 0.1.0, semantic versioning, the metadata complete: urls,
  classifiers, keywords, the licence file); a `release.yml` workflow publishes to TestPyPI on manual dispatch from
  `dev` and to PyPI on a `v*` tag on `main`, through trusted publishing (OpenID Connect) with a GitHub environment per
  index; the workflow runs the full suite first and refuses a tag whose version does not match `pyproject.toml`.
- G2. **The flow is written down and enforced where the repository can enforce it:** `CONTRIBUTING.md` states
  candidates on `dev`, releases from `main` by the maintainer, semantic versioning with what bumps each part, the
  `CHANGELOG.md` convention, the checks a pull request must pass; the branch protections he sets on GitHub (main:
  require pull request, require the test workflow, restrict merges to maintainers; dev: require the test workflow) are a
  checklist in `docs/maintainers.md` with screenshots' worth of exact setting names.
- G3. **Ownership and templates:** `.github/CODEOWNERS` naming him for everything (one line to add a maintainer);
  issue templates (bug, question, a case study proposal) and a pull-request template that asks for the claim-and-backing
  habit (what changed, what backs it, which tests); `SECURITY.md` with how to report. No code of conduct here: the
  contributor covenant is WP49's spike (OD1, closed 2026-11-14), and `CONTRIBUTING.md` carries one line pointing to it
  once it lands.
- G4. **Onboarding a maintainer is one page:** `docs/maintainers.md`: how a maintainer is added (CODEOWNERS, the
  GitHub team, the PyPI collaborator), how a release is cut (version bump, changelog, tag, the workflow), how a
  candidate is reviewed, where the records live.
- G5. **The supervisor's PyPI steps are a short checklist with the exact names:** create the PyPI and TestPyPI
  projects or pending publishers for `hyperbolic-trade-space` pointing at this repository, the workflow file
  `release.yml` and the environments `testpypi` and `pypi`; then the dry run.

## Non-goals

- Publishing anything before his acceptance and merge; the TestPyPI dry run is the only publish before the tag.
- Governance control checks as automated release gates (WP48's spike decides their shape; their build is after v0.1).
- Changing the test workflow beyond what the release workflow needs from it.
- Any change to the paper or the docsite's content pages (the maintainers page is new).

## Deliverables

| ID | Deliverable | Serves |
|---|---|---|
| D-1 | `pyproject.toml` metadata and version 0.1.0 (landing with the version unit of WP8b, rebased), `uv build` clean, the wheel's contents checked | G1 |
| D-2 | `.github/workflows/release.yml` (trusted publishing; TestPyPI on dispatch from `dev`, PyPI on `v*` tags on `main`; the suite first; the version check) | G1 |
| D-3 | `CONTRIBUTING.md`, `SECURITY.md`, `.github/CODEOWNERS`, `.github/ISSUE_TEMPLATE/` (three), `.github/pull_request_template.md` | G2, G3 |
| D-4 | `docs/maintainers.md` (the flow, the branch-protection checklist, onboarding, cutting a release), in the docs navigation under a "Project" heading | G2, G4 |
| D-5 | `work-packages/WP47-rounds/pypi-checklist.md`: the supervisor's steps with exact names, and the record of the TestPyPI dry run when it is done | G5 |
| D-6 | `work-packages/WP47-review.md`: the build and the workflow tried on a fork or a dry run (`workflow_dispatch` against TestPyPI needs his publisher first; until then the workflow is validated by `act` or by a dry-run job that builds and checks the version) | all |

## Requirements

| ID | Requirement | Checked by |
|---|---|---|
| R-1 | `uv build` succeeds and `uv run python -m twine check dist/*` passes; the wheel contains the package and the licence and nothing from `examples/` or `work-packages/` | the review runs them |
| R-2 | No token or secret is added to the repository; publishing is by OpenID Connect | the workflow's text |
| R-3 | The workflow refuses a tag whose version differs from `pyproject.toml` | a dry-run job with a mismatched tag |
| R-4 | Every new file passes the vocabulary check and the attribution grep | `uv run python scripts/check_vocabulary.py`; the grep |
| R-5 | `CODEOWNERS` names the supervisor for `*` and the docs page says how a second maintainer is added in one line | the files |
| R-6 | No change to `paper/` | `git diff --stat` |

## Definition of good

- A new maintainer reads one page and can cut a release; the supervisor's own steps fit on one screen; nothing
  publishes without his tag.

## Definition of good enough

- D-1 to D-6 delivered; R-1 to R-6 pass; the TestPyPI dry run done with him, or ready to run the moment his pending
  publisher exists.

## Definition of done

Good enough is met, no open item remains unresolved, and the supervisor has accepted the work.

## Agent's defaults

- Trusted publishing via `pypa/gh-action-pypi-publish` with environments `testpypi` and `pypi`; the version check reads
  `pyproject.toml` with Python's `tomllib` *(default)*.
- Semantic versioning as in semver 2.0.0; pre-release candidates as `0.1.0rc1` on TestPyPI only *(default)*.
- Issue templates as YAML forms; the pull-request template asks for the claim, the backing and the tests *(default)*.
- The unit runs on Sonnet in a worktree; the reviewer tries the build and the dry-run job *(default)*.

## Open decisions (for the supervisor)

- **OD1 (closed 2026-11-14, `WP47-decisions.md`).** A code of conduct: he wants a contributor covenant tied to how AI is
  used and supervised, as its own spike (WP49). None is written in WP47.

No open decision remains.

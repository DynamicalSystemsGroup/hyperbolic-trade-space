# WP0 — Scope of work: Setup and persisted working agreements

| | |
|---|---|
| **Status** | DRAFT. Approved only by the recorded act below. Nothing in this package is executed before then. |
| **Supervisor (accountable)** | mzargham |
| **Repository** | `DynamicalSystemsGroup/posynomial-invariant-form` (local: `/Users/z/Documents/GitHub/posynomial-invariant-form`) |
| **Approval record** | Verbal approval in chat, quoted verbatim in `work-packages/WP0-decisions.md` (supervisor's decision: "we can do verbal approvals for now"; release controls after the first release) |
| **Acceptance record** | Verbal acceptance in chat, quoted verbatim in `work-packages/WP0-decisions.md`, after the review report `work-packages/WP0-review.md` |

## Purpose

Nothing in the approved plan is visible to the agents that will execute later packages. WP0 persists
the plan into the repository as a design spec, reference notes, work-package procedure and project
conventions; scaffolds a reproducible uv project with CI; and pushes the first commit, so that a
Sonnet project-manager session can run WP1 onward from repository files alone.

## Goals

- G1. The approved plan's content is persisted in the repository where executing agents will read it.
- G2. The repository is a reproducible uv project (lockfile, pinned Python, test CI) that any clone can install.
- G3. The supervisor's gated-work process is operable here: skills installed, procedure and breakdown recorded, PM brief written.

## Non-goals

- No package code beyond an importable empty package with a version; no estimator, solver, derivation, docs content or notebook (WP1–WP8).
- No site build, no Pages workflow (WP8).
- No release controls, branch protection or PR-based gating (supervisor: after the first release).
- No literature review or BibTeX (WP5).

## Deliverables

| ID | Deliverable | Serves |
|---|---|---|
| D-1 | `docs/superpowers/specs/2026-11-07-posynomial-invariant-form-design.md`: design spec (plan §1, §3–§8) | G1 |
| D-2 | `docs/superpowers/notes/{adcs-port,proof-conventions,sklearn-conformance,presentation-framing,references-verified}.md` | G1 |
| D-3 | `work-packages/README.md` (operating procedure, roles, records, breakdown WP0–WP8) and `work-packages/PM-BRIEF.md` | G1, G3 |
| D-4 | Repo `CLAUDE.md` (uv-only commands, nomenclature, conformance pointer, derivation/docs conventions, no-attribution rule, work-package procedure and file locations) | G1, G3 |
| D-5 | uv project: `pyproject.toml` (hatchling, src layout, `requires-python >=3.12,<3.13`, runtime deps numpy/scipy/sympy/scikit-learn>=1.8/pandas/matplotlib, groups `dev`, `docs`, `notebooks`), `.python-version`, `uv.lock`, `.gitignore`, pytest and ruff config, `src/posynomial_invariant_form/__init__.py` with `__version__`, `tests/conftest.py` (MPLBACKEND=Agg), a placeholder import test | G2 |
| D-6 | `.github/workflows/test.yml`: setup-uv, `uv sync --locked`, `uv lock --check`, `uv run pytest` | G2 |
| D-7 | `README.md` stub: one-paragraph description, quickstart (`uv sync`, `uv run pytest`), pointer to `work-packages/` and the spec | G1, G2 |
| D-8 | Gated-work skills installed: `~/.claude/skills/{work-breakdown,scope-of-work,work-execution,work-acceptance,CLAUDE.md,README.md}` symlinked from a clone at `~/.claude/skills-src/claude-skills` (outside the repo) | G3 |
| D-9 | `work-packages/WP0-decisions.md` with the approval record; first commit on `main` pushed to `origin` | G1, G3 |

## Requirements

| ID | Requirement | Checked by |
|---|---|---|
| R-1 | `uv sync --locked` succeeds from a clean clone with Python 3.12 | run it in a fresh temporary clone |
| R-2 | `uv run pytest` passes (placeholder test, doctest-modules enabled) | run it |
| R-3 | `uv lock --check` passes | run it |
| R-4 | `uv run python -c "import posynomial_invariant_form as p; print(p.__version__)"` prints a version | run it |
| R-5 | The spec contains every decision in plan §1 and the mathematics, API, conformance, demo, derivation and site sections (§3–§8) | inspect headings against the plan file |
| R-6 | Each note in D-2 states its sources (file paths or DOIs) | inspect |
| R-7 | `work-packages/README.md` lists WP0–WP8 with one line each and the procedure; `PM-BRIEF.md` names the files a PM must read and the first skill to invoke | inspect |
| R-8 | `CLAUDE.md` states the no-attribution rule and the uv-only rule | inspect |
| R-9 | `ls -la ~/.claude/skills` shows the six symlinks resolving to the clone | run it |
| R-10 | `git log origin/main` shows the first commit with no AI attribution lines | run it |

## Definition of good

- A Sonnet PM session started cold in the repo can read `CLAUDE.md`, `work-packages/PM-BRIEF.md`, the spec and notes and scope WP1 without asking what the project is.
- The repo looks like the supervisor's other repos: uv, flat conventions, one obvious entry point.

## Definition of good enough

- All deliverables D-1 to D-9 exist at the stated paths.
- R-1 to R-10 pass as checked.
- No code beyond the empty package (non-goals untouched).

## Definition of done

Good enough is met, **no open item remains unresolved**, and the supervisor has accepted the work by the acceptance record above.

## Agent's defaults

- Skills installed by symlink from a clone at `~/.claude/skills-src/claude-skills` *(default)*, so `git pull` updates them.
- Spec and notes under `docs/superpowers/specs/` and `docs/superpowers/notes/` *(default)*; work-package documents under `work-packages/` *(default)*.
- Build backend hatchling with src layout; ruff with line length 100; pytest `addopts = "--doctest-modules"`; `testpaths = ["tests"]` *(default)*.
- Dependency groups named `dev`, `docs`, `notebooks` *(default)*; `docs` and `notebooks` groups declared now but their packages installed only when WP8/WP7 need them (kept out of the default sync via `default-groups = ["dev"]`) *(default)*.
- `.gitignore` from the standard Python template plus `.venv/`, `_site/`, `site/`, `docs/generated/` *(default)*.
- Version `0.0.1` in `__init__.py` *(default)*.
- CI workflow runs on push and pull request to `main` on ubuntu-latest, Python from `.python-version` *(default)*.
- First commit message: "WP0: setup, persisted plan and working agreements" *(default)*.

## Open decisions (for the supervisor)

None. Every item was resolved through the decision loop (in the approved plan). Decided: 13 (plan
decisions), deferred: 0, raised: 0.

# WP61 — Scope of work: archive the completed packages and index them by delivery commit

| | |
|---|---|
| **Status** | Approved by the driver as his proxy under his direction of 2026-11-15 (`WP61-decisions.md`) |
| **Supervisor (accountable)** | mzargham |
| **Repository** | `DynamicalSystemsGroup/hyperbolic-trade-space`, `work-packages/` |
| **Approval record** | His words, quoted verbatim in `WP61-decisions.md` |
| **Acceptance record** | The driver's check that every test and generator that reads a work-packages path still passes; his read of `INDEX.md` |

## Goals

- G1. `work-packages/INDEX.md`: every package WP1 onward, one row: number, title, state (landed, accepted by him,
  in flight, scoped, retired, superseded), the dev commit where it landed (from `git log` on its files and the driver
  log), where its documents now live. The one place the status lives.
- G2. `work-packages/archive/WPnn/` holds the documents (scope, decisions, review, amendments, rounds) of every
  package that landed and has no work in flight, moved with `git mv`; a path that any file outside `work-packages/`
  reads (code, tests, notebooks, docs, the register's `backing` fields, `mkdocs.yml`) is not moved and is listed in
  the index as "in place, read by <file>".
- G3. The protocol in `work-packages/README.md`: the index is the status; scope files carry no live status line (the
  header's Status cell says "see INDEX.md"); `milestones.md` is the board of the release; a package is archived at
  its landing with its hash, by the driver, as part of landing.

## Non-goals

- Editing the content of any package document beyond the status cell. Touching the packages in flight (WP25, WP8b,
  WP11, WP51, WP53 to WP61), `driver-log.md`, `milestones.md`, `paper-requirements.md`, `release-candidate.md`,
  `PM-BRIEF.md`, `interface-contract.*`, `supervisor-*.md`, `reviewers-guide/`, `review/`, `examples-coverage.md`.

## Deliverables and checks

| ID | Deliverable | Check |
|---|---|---|
| D-1 | `INDEX.md` | every `WPnn-scope-of-work.md` in the tree has a row; every row's commit exists on dev and touches that package's files or is named in the driver log |
| D-2 | `archive/` with the moves | `git log --follow` works for a sampled moved file; the grep of work-packages paths outside the folder resolves every path |
| D-3 | the README protocol and the status cells | `grep -L "see INDEX.md" work-packages/archive/*/WP*-scope-of-work.md` empty |
| R-1 | nothing that reads a work-packages path breaks | `uv run pytest -q -m "not slow" tests/test_paper.py tests/test_site.py tests/test_claims_register.py tests/test_history_structure.py`, `uv run python -m derivation.proofmap`, `uv run mkdocs build -q`; lint and format |

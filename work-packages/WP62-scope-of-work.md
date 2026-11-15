# WP62 — Scope of work: the tree holds the current state (the superpowers notes retired; the historical material indexed)

| | |
|---|---|
| **Status** | see INDEX.md (approved by the driver as his proxy under his directions of 2026-11-15, `WP61-decisions.md`) |
| **Supervisor (accountable)** | mzargham |
| **Repository** | `DynamicalSystemsGroup/hyperbolic-trade-space`; a branch `wp62` in its own worktree |
| **Approval record** | His words in `WP61-decisions.md` (the superpowers notes as prompt residue; the repository-wide rule; the heuristic now in CLAUDE.md) |
| **Acceptance record** | The driver's check that every test, generator and page that read a moved or removed path still passes; the inventory read by him when he next reads |

## Purpose

His heuristic (CLAUDE.md, Process): the repository's job is the current state; git history's job is the trajectory;
indexes and ledgers in the tree make the historical material discoverable and dereferenceable. His rule for what
stays: the delivered content and what builds and checks it; the live guidance; the boundary content on future
directions from the research spikes; the live packages with the index, the board and the log. `docs/superpowers/` is
"essentially prompt residue by most interpretations" and is retired as a location.

## Goals

- G1. **An inventory first:** every top-level path and every entry under `docs/superpowers/`, `paper/` (notes and
  records, not the notebooks, generators and figures), `examples/` (beyond the case code and data of record),
  `scripts/`, `site/`, `work-packages/` (what WP61 left) classified as: delivered content; builds or checks it; live
  guidance; boundary content; live package; historical. With the reader of each path (code, test, notebook, docsite,
  CLAUDE.md, the register's backing) or "none". The inventory is approved by the driver as proxy before a file moves.
- G2. **`docs/superpowers/` retired:** the live guidance notes (claims-review, figure-review, proof-conventions,
  sklearn-conformance, vocabulary-review, presentation-framing, user-journeys, notation, residual-review, reader-grid,
  verification-strategy, abstraction-gaps, the design spec) move to `notes/` at the repository root with `git mv`,
  every reference updated (CLAUDE.md, tests, scripts, docs pages, `work-packages/`); user-journeys' section numbers
  corrected to the paper's eleven sections. The spike folders and the rest leave the tree at one commit. A path a
  notebook reads stays in place until that notebook is next re-executed by its package (WP55 to WP57), listed in
  the index with the reader.
- G3. **The boundary content gathered:** the readouts that define the future directions (WP36's decisions, WP41's,
  WP43's, WP48's, WP50's and WP52's spike readouts, the ternary spike's readout) copied or moved to
  `notes/directions/`, one file each, cited from the paper's Future work record (WP54-review.md) and listed in the
  index; the originals removed where they were under a landed package.
- G4. **The index's second table:** every historical path removed in G2 and G3, with the commit that holds it, its
  purpose in one clause and the dereferencing command; the README's protocol extended to notes and spike outputs.

## Non-goals

- Any edit to `paper/paper.ipynb` or `paper/supporting_material.ipynb` (WP55 holds the notebook; a notebook's
  references move with its package). Any change to the package, the tests' logic, the docsite's pages beyond a path.
  The live packages' documents (WP11, WP25, WP8b, WP51, WP53 to WP62).

## Deliverables and checks

| ID | Deliverable | Check |
|---|---|---|
| D-1 | `work-packages/WP62-rounds/inventory.md`, the classification with readers, approved as proxy before any move | the driver's approval line in `WP62-decisions.md` |
| D-2 | `notes/` with the live guidance and `notes/directions/` with the boundary readouts; `docs/superpowers/` gone except notebook-read paths, which the index lists | `ls docs/superpowers` shows only the listed paths; `grep -rn "docs/superpowers" CLAUDE.md tests scripts docs mkdocs.yml work-packages/README.md work-packages/PM-BRIEF.md` returns only the listed paths |
| D-3 | The index's second table and the README's protocol | every removed path has a row with a commit on dev that holds it; `git show <commit>:<path>` works for a sample of five |
| R-1 | Nothing that reads a path breaks | `uv run pytest -q -m "not slow"`, `uv run python -m derivation.proofmap`, `uv run mkdocs build -q`, `scripts/check_residuals.py`, `scripts/check_vocabulary.py`, lint and format; the site assembled (`scripts/stage_site.py`) |
| R-2 | The tree after: no top-level path classified historical remains | the inventory's disposition column against `git ls-files` |

## Definition of good

A reader checking out the repository meets the delivered content, the guidance for working on it, the directions the
spikes opened, and the live packages, and finds everything else by its index row.

## Definition of good enough

D-1 approved; D-2 and D-3 landed with R-1 green; R-2 met except notebook-read paths, each listed.

## Definition of done

Good enough met; the driver's acceptance; his read of the inventory when he next reads.

## Agent's defaults

- `notes/` is a plain folder at the root, not under `docs/` (the docsite's source) and not built by MkDocs; the
  docsite's `exclude` or `not_in_nav` is updated if MkDocs warns.
- The two Python files tests import from spike folders (`spike-facet-refit/bench_oracle.py`,
  `spike-sysml-diagrams/project.py`) move with their readers updated, to `tests/fixtures/` or `scripts/`, whichever the
  tests' conventions use.
- One unit; the inventory in its first commit, the moves in a second after the driver's approval line.

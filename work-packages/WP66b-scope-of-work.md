# WP66b — Scope of work: the paper model (stage 3, build)

| | |
|---|---|
| **Status** | DRAFT, approved by the driver as his proxy under his approval of the plan (2026-11-16, `WP64-decisions.md`) |
| **Supervisor (accountable)** | mzargham |
| **Repository** | `DynamicalSystemsGroup/hyperbolic-trade-space`; branch `wp66b`; the file set of `work-packages/WP65-design/build-plan.md`, section "WP66b, the paper model" (19 files) |
| **Approval record** | The driver's approval under his mandate, quoted in `WP64-decisions.md` |
| **Acceptance record** | The driver's independent run and read; landed first of the three units |

## Purpose

Build the paper's release control model as `work-packages/WP65-design/specification.md` specifies it (sections 2,
3.1, 5.2 and 6.3): the paper's workflow on the `paper` branch, event-driven; the mode file and its validation; the key
manifest and its builder; the pin tooling and the link pinning; the paper marker that takes every paper test out of
the software gate; the register, vocabulary and residual checks split by surface; the paper's release checklist.

## Goals

- G1. `.github/workflows/paper.yml` per specification 2.2 (push to `paper` and `qc/paper/**` builds and tests; a
  `paper-*` tag publishes the two assets as a GitHub release, drafts published last; the clean-up on failure; the
  `paper-release` environment on the release job present as the specification writes it, with a comment that his
  third question keeps or removes it).
- G2. `paper/mode.toml` (mode `abstract` for 0.1) and `scripts/paper_mode.py` per 3.1; `paper/build_keys.py` and
  `paper/paper-keys.json` per 2.6; `scripts/paper_pin.py` per 2.4; `paper/pin_links.py` per 2.7; `paper/CHANGES.md`
  per 2.8.
- G3. The `paper` marker (`tests/conftest.py`, the three test modules), the splits by surface in the register,
  vocabulary and residual tests and their scripts' `--surface` and `--views`, per 5.2.
- G4. `tests/test_paper_model.py` with every test the build plan's section 2 lists for WP66b.
- G5. `work-packages/release-checklist-paper.md` per 6.3 (the paper's rows of the old checklist with their ids and
  states; the old file is removed by WP66a, which owns it).

## Non-goals

No file outside the unit's file set (the build plan's table is the contract; a file another unit owns is never
touched; a need for one is reported, not met); no deploy, tag, publish or push; no change to the paper's content or
the package's public surface; no change to his keyboard settings.

## Requirements and checks

| ID | Requirement | Check |
|---|---|---|
| R-1 | Every element of the specification's sections for this unit is implemented or reported as impossible with the reason | a table in the hand-back mapping section to file |
| R-2 | Every test the build plan lists for this unit exists, is named as listed, and passes | `uv run pytest -q <the unit's test files>` |
| R-3 | The software suite passes with the paper tests deselected; lint, format, lock | the build plan's section 3 commands, exit codes captured |
| R-4 | No attribution line; no metanarration in any page or record text; `git diff --stat dev` names only the unit's files | the grep; a read; the diff |

## Definition of good

The unit's part of the design works end to end on a local checkout exactly as the specification states, and its tests
would catch the regressions the specification names.

## Definition of good enough

R-1 to R-4 met; the driver's independent run green; landed on `dev` in the build plan's order.

## Definition of done

Good enough met; WP67's quality-control runs green on the unit's part.

## Open decisions

None; the design is approved and the questions that remain his do not change this unit's files beyond a one-line
switch named in the scope.

## Agent's defaults

- One unit, worktree prepared by the driver; the specification's section numbers are cited in commit messages.

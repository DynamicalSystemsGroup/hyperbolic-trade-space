# WP66a — Scope of work: the software model (stage 3, build)

| | |
|---|---|
| **Status** | DRAFT, approved by the driver as his proxy under his approval of the plan and his three answers (2026-11-16, `WP64-decisions.md`) |
| **Supervisor (accountable)** | mzargham |
| **Repository** | `DynamicalSystemsGroup/hyperbolic-trade-space`; branch `wp66a`; the file set of `work-packages/WP65-design/build-plan.md`, section "WP66a, the software model" (20 files) |
| **Approval record** | The driver's approval under his mandate, quoted in `WP64-decisions.md` |
| **Acceptance record** | The driver's independent run and read; landed last of the three units |

## Purpose

Build the software's release control model as `work-packages/WP65-design/specification.md` specifies it (sections
1, 5.1, 6.1, 6.2 and 7, with his three answers of 2026-11-16: the review rule with him as bypass; a merge without a
new version redeploys the site only; the paper's publication approved by a code owner): the merge of the `dev` pull
request into `main` as the release, the tag created by the workflow, PyPI by trusted publishing inside `release.yml`,
the site composed and deployed as called jobs, failure detection at every step and the clean-up script, the software
gate without the paper's tests, and the records the unit owns.

## Goals

- G1. `.github/workflows/release.yml` per specification 1.2 to 1.4 with the site-only path of his second answer
  (admissibility reports `site-only` when the tag exists on an earlier commit and the package files are unchanged
  since it: the run composes and deploys the site and skips the tag, PyPI and the release; a change to package files
  with an unchanged version fails); the `qc/**` push trigger and the dry-run dispatch on `dev`; `on-failure` running
  `scripts/release_cleanup.py` and opening the labelled issue; PyPI as the last irreversible step.
- G2. `scripts/release_cleanup.py` and `scripts/release_checks.py` per 1.4 and 1.3, with their tests
  (`tests/test_release_cleanup.py`, `tests/test_release_checks.py`) as the build plan's section 2 lists them.
- G3. `.github/workflows/test.yml` per 5.1 (the three software shards with `not paper`, pull requests to `main`, the
  dispatch and the call; Windows never on a pull request); `pages.yml` removed; `tests/test_release_workflows.py` and
  `tests/test_ci_shards.py` as listed.
- G4. The records: `.github/RELEASE_ADMISSIBILITY.md`; `docs/code-owners.md` (the four drifts corrected; the `pypi`
  environment without a reviewer; the `main` rulesets per his first answer; the `paper-release` environment per his
  third); `CHANGELOG.md` (the unreleased entry naming the two lifecycles and the paper's mode); `CITATION.cff`; the
  interface contract `.md` and `.toml` amendment 29 and `tests/test_interface_contract.py`; `work-packages/README.md`
  (the branching and CI lines as they now are); `WP8b-release-checklist.md` removed with `INDEX.md`'s protocol
  followed for a file that leaves the tree (the driver fills the commit hash at landing);
  `work-packages/release-checklist-software.md`; `release-candidate.md`'s dated section on the two lifecycles.

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

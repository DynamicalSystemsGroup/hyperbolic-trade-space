# WP82 — Scope of work: the 0.2 governance update

**Status:** DRAFT until approved. **Supervisor:** Michael Zargham (`mzargham`). **Approval:** verbal, quoted
verbatim in `WP82-decisions.md` (the repository's convention). **Acceptance:** his word, quoted there; then the pull
request from `governance-bypass-removal` into `dev`, opened after `dev` is merged into `main` for 0.1 (his word),
reviewed and merged by a code owner who is not its author (`danlessa`). The pull request closes the issue that carries
this scope in the scope-of-work template; the issue is posted on his word.

## Purpose

His release line of 2026-11-17 (`WP64-decisions.md`): 0.1 merged on the `main-review` bypass; then the bypass removed
by a change to the declaration first and the ruleset second, in a pull request of its own, named in the 0.2 changelog.
His decision of this evening (`WP82-decisions.md`): that pull request also carries the gap items of WP78's readout he
picked, so that the 0.2 release, the first through the review rule without a bypass, is also the first under the
declared control on the governed files.

## Goals

- **G1** The `main-review` bypass is gone from the declaration; after the merge he removes it from the ruleset, and a
  code owner's local run of the checker attests the live settings conforming.
- **G2** The gap items he picked are declared: the default workflow permissions `read` with approving reviews off
  (gap 1); `controls` among the required status checks of `main-checks` (gap 3); the control on the governed files as
  CODEOWNERS path lines naming all three code owners plus a push ruleset on the governed paths with the Repository
  admin role as its bypass (amendment 2); the admissibility rows (gaps 4, 6, 7).
- **G3** The pull request clears the repository's own admissibility: `closes #n`, the template's sections, the field
  checks green, a non-author code owner's merge, and the suite green on the push after the merge except for the one
  documented window (R-5).

## Non-goals

- Changing any setting on GitHub: every setting changes after the merge, by him, declaration first (`GOVERNANCE.md`).
- Gap 2 (the local-only fields stay local-only: no token, no field leaves the declaration); gap 5 (WP79's paper
  template); gap 8 (the publishers, Zenodo, the labels); the `main-review` rule's other parameters.
- The documentation pull request (`v0.2` into `dev`) and the 0.2 release itself (version, changelog heading, tag).
- New workflows: the bug and question templates get rows a code owner judges, not a check.

## Deliverables

- **D-1** `.github/governance.toml`: `rulesets.main-review.bypass_actors = []`; `actions.default_workflow_permissions
  = "read"` and `can_approve_pull_request_reviews = false`; `controls` in `main-checks`' required status checks; a
  fifth ruleset `governance-files` (target `push`, rule `file_path_restriction` over the governed paths, bypass
  `RepositoryRole` 5 `always`); every `governed_files` entry's `control` field names the path line and the ruleset.
- **D-2** `.github/CODEOWNERS`: one line per governed path naming `@mzargham @danlessa @rororowyourboat`;
  `scripts/admissibility.py` reads the governed lines (`owners_of`) and `tests/test_admissibility.py` holds this
  repository's file to them.
- **D-3** `scripts/check_repo_settings.py` compares a push ruleset (target, the file-path rule's paths, the bypass)
  if it does not already; `tests/data/wp78/` carries the declared state (the recorded payloads edited for the changed
  fields, a payload for the new ruleset in the API's shape, marked as such in the fixture's note), and
  `tests/test_repo_settings.py` names each new kind of drift.
- **D-4** The documents: `GOVERNANCE.md` (the review paragraph after 0.1; the secondary rules' control; the window of
  R-5), `.github/ISSUE_ADMISSIBILITY.md` (rows for a bug report and a question), `.github/PR_ADMISSIBILITY.md` (the
  `controls` job in the conformance row; each judged row naming its guideline page and section), `docs/code-owners.md`
  (step 4 of a release; the settings to change after this merge, in order), `CHANGELOG.md` (`## [Unreleased]`, the
  entries).
- **D-5** Every workflow job declares the permissions it writes with, so `read` as the default changes nothing that
  runs; checked by reading each workflow and by a test if one does not already hold it.
- **D-6** The issue (the scope-of-work template, `draft`, posted on his word) and the pull request description (the
  template's sections, the Tests section quoting the suite at the head, the Defaults section listing the hand-made
  fixture and the window).

## Requirements

- **R-1** `uv run python scripts/check_repo_settings.py --fixture tests/data/wp78` is conforming, and `--runner` is
  conforming with the local-only fields listed. Checked by running both.
- **R-2** A live run on the branch before the merge reports exactly the differences the settings he will change
  account for (the bypass, the workflow permissions, the required check, the missing ruleset), nothing else. Checked
  by running it and reading the lines.
- **R-3** `uv run pytest -m "not slow and not paper"`, `uv run ruff check .`, `uv run ruff format --check .`,
  `uv lock --check` pass at the head. Checked by running them.
- **R-4** No setting is changed before the merge, by anyone but him, or without the declaration first. Checked by the
  live run (R-2) and his word.
- **R-5** The window is written down: after the merge, the `controls` job on the push to `dev` fails on the required
  check and the missing ruleset (runner-checked fields) until he changes those two settings; the order of his changes
  and the local run that closes the window are in `docs/code-owners.md` and the pull request. Checked by reading.
- **R-6** No AI attribution in commits, the pull request or the documents. Checked by `git log` and reading.
- **R-7** Every claim in the documents is backed by a setting, a test or his recorded word; the vocabulary and
  residual checks pass. Checked by `uv run python scripts/check_vocabulary.py` and the residual checker.

## Definition of good

The 0.2 release is merged under the review rule with no bypass, under declared and attested settings, and a change to
a governed file is approved by a code owner and pushed by an admin, with the declaration, the fixture, the tests, the
documents and the live repository saying the same thing.

## Definition of good enough

- R-1 and R-3 pass at the head (conformance).
- R-2's live differences are exactly the four he will set, listed in the pull request (conformance).
- `tests/test_admissibility.py` holds this repository's CODEOWNERS to the `*` line, the paper line and the governed
  lines (conformance).
- The window (R-5) and the order of his settings changes are in `docs/code-owners.md` and the pull request (fitness).
- The admissibility rows read as rows: a condition, a kind, who enforces or records it (fitness).
- The pull request carries the bypass removal and the four picked items, nothing else (fitness).

## Definition of done

Good enough met, no open item, his acceptance quoted in `WP82-decisions.md`; the pull request opens after 0.1 and is
merged by `danlessa`; his settings changes follow, and his local run reads conforming.

## Open decisions

None. His answers of 2026-11-17 are quoted in `WP82-decisions.md`.

## Agent's defaults

- Branch `governance-bypass-removal`, cut from `dev` 7973fbd1, rebased onto `dev` when 0.1 is out; one commit per
  deliverable.
- The push ruleset is named `governance-files`; its paths are the `governed_files` table's paths; its bypass actor is
  `RepositoryRole` 5 (Repository admin), mode `always`; enforcement `active`.
- The declaration keeps `actions` local-only (gap 2 untouched); `can_approve_pull_request_reviews = false` goes with
  `read`, as the design (WP65, section 6) said.
- The required check is named `controls`, the job's name in both workflows.
- The fixture is hand-edited to the declared state and the new ruleset's payload is hand-made in the API's shape
  (recorded again by `--record` after his settings change, in a follow-up commit); the fixture directory's note says
  which files are recordings and which are not.
- The bug and question rows are fitness rows judged by a code owner at triage (the labels `bug` and `question`
  record it); no new workflow.
- Each judged row of `PR_ADMISSIBILITY.md` names its guideline as "page, section" in the row.
- The changelog entries go under `## [Unreleased]`, `### Removed` and `### Changed`; the 0.2 release renames the
  heading.
- The `Tools used` section of the pull request names uv, ruff, pytest and the GitHub CLI; his line on AI tools is his
  to write.

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

## Amendments

### Amendment 1 (2026-11-17, evening): the versioning rule and its check

His words, verbatim (`WP82-decisions.md`, "Amendment 1"): "i recommend we also indicate that the governance update is
the reason why this qualifies as an 0.2.0 rather than an 0.1.1 since documentation updates since didn't touch the
optimizer just the documentation and the governance machinery"; "i think we probably need to ensure we have explicit
guidance and checks for semantic versioning. this also probably amounts to changes in the governance"; asked where the
rule lands, "Amend WP82". The amendment joins the governance pull request before it opens.

**Goal added.** **G4** The version number's meaning is a stated rule with an executable side and a judged side, and
0.2.0 is named a minor release for the governance update, the package's code unchanged.

**Deliverables added.**

- **D-7** `GOVERNANCE.md`, a `## Versions` section: while the major is 0, a patch release changes neither the public
  surface nor a governed file; a minor release adds capability, changes the surface or changes a secondary rule; the
  major stays 0 until a release whose surface is a commitment; what is executable and what is judged; the sentence on
  0.2.0.
- **D-8** The public surface as a record: `scripts/api_surface.py` (by import and `inspect`; sorted JSON; `--write`,
  `--check` naming each differing entry), `tests/data/api_surface.json` committed, `tests/test_api_surface.py` holding
  the record equal to the package with the rewrite command in its failure message.
- **D-9** `scripts/release_checks.py version-kind`: the version against the highest `v*` tag below it; the bump named;
  a patch release refused for a changed record (or, for a previous tag without a record, a surface that differs from
  the one computed from the tag's `src`), a changed governed file (the declaration's `governed_files` paths) or an
  `Added` or `Removed` section in the entry; the first release and an already-tagged version pass with a notice; a
  step in `release.yml`'s admissibility job; tests on temporary repositories with tags.
- **D-10** The rows: a machine row in `.github/RELEASE_ADMISSIBILITY.md` and the judged part (the entry names what
  moved the number) in its fitness row; the test named in `.github/PR_ADMISSIBILITY.md`'s conformance row; the rule in
  `docs/code-owners.md` ("Cutting a release"); the changelog entry under `### Added`; this amendment and the decision
  record; the index row.

**Requirements added.**

- **R-8** `uv run python scripts/api_surface.py --check` exits 0 at the head, and `tests/test_api_surface.py` fails
  when the record is stale. Checked by running both (the test's own stale-record case).
- **R-9** `uv run python scripts/release_checks.py version-kind` classifies patch, minor and major, and refuses each
  of the three patch conditions with one line per difference. Checked by `tests/test_release_checks.py`.
- **R-10** `tests/test_release_workflows.py` and `tests/test_release_checks.py` name the step among the gates; the
  dry-run and TestPyPI paths of `release.yml` are unchanged. Checked by those tests and by reading the job's `if`.

**Agent's defaults (Amendment 1).**

- The record leaves out `__version__` (the version is what the rule classifies) and a class's inherited methods (the
  base's surface); properties are not recorded; module constants are recorded with their value; a module without
  `__all__` contributes the public names it defines.
- The previous release is the highest `v*` tag strictly below the version by version order (a final release above its
  pre-releases); a tag equal to the version is the redeploy case and passes with a notice, the `tag` check deciding.
- The bump is the first of the three numbers that moved; a pre-release of a higher number is classified by its number.
- The patch check reads the committed record at the head (held equal to the package by the test), not a fresh import,
  so the admissibility job needs no import of the package unless the previous tag lacks a record; that fallback runs
  `scripts/api_surface.py` in a fresh interpreter over `git archive <tag> src`, so the workflow step runs under
  `uv run --locked` (the project environment) rather than `--no-project`.
- The step is skipped on a site-only merge, as the changelog step is; a patch release whose entry is still under
  `## [Unreleased]` (a dry run) has its sections not read, with a notice.
- The judged part is folded into the existing fitness row rather than a second fitness row, so the secondary-rules list
  and the declaration's `by` field ("the fitness row", singular) stay true.
- Nothing is added to the secondary-rules list: the record is a record, not a rule; the interface contract is not
  amended, since no package surface changes.

### Amendment 2 (2026-11-17, evening): the Dependabot route

His words, verbatim (`WP82-decisions.md`, "Amendment 2"), with a screenshot of the eight open Dependabot pull requests
#4 to #11, each "Review required", 15 of 18 checks failing: "we're going to need to handle this stuff. in v0.2 if
possible"; asked where the route lands, "Amend WP82"; then: "i also think we should extend our governance PR content to
provide instructions for how dependabot PRs should be handled since it seems like they will be a common occurance
(some of our dependencies are advancing rather quickly)". The amendment joins the governance pull request before it
opens.

**Goal added.** **G5** A dependency update has a declared route: Dependabot's pull request targets `dev`, the
admissibility checks read it as one, the test workflow runs on it before the merge, and a code owner has the steps.

**Deliverables added.**

- **D-11** `.github/dependabot.yml`: `target-branch: dev` and `labels: ["dependencies"]` for both ecosystems; minor and
  patch bumps grouped into one weekly pull request per ecosystem, a major on its own; the weekly schedule kept.
- **D-12** The route in the rules: a machine row for a dependency update in `.github/PR_ADMISSIBILITY.md` (opened by
  `dependabot[bot]` against `dev` with the `dependencies` label; its own description stands in for the template; no
  issue; the test workflow before the merge; a code owner merges, an admin where it touches a workflow);
  `scripts/admissibility.py` `linked-issue` and `pr-fields` pass such a pull request with a notice quoting the row,
  `merge` unchanged (the author is the bot); `pr-fields.yml` fires on `labeled` too; the cases in
  `tests/test_admissibility.py`, among them one holding `dependabot.yml` to the target, the label and the groups.
- **D-13** `.github/workflows/test.yml`: the `pull_request` event for base `dev`, gated at job level to
  `github.actor == 'dependabot[bot]'` on `controls` and `test`; lint, `controls` and the fast shard, as the push to
  `dev`; the workflow tests (`tests/test_ci_shards.py`) holding the trigger, the gate and the matrix.
- **D-14** The documents: `GOVERNANCE.md`'s pull-request paragraph (the route and the steps in brief);
  `docs/code-owners.md`, a sentence under "Reviewing a candidate" and the section "Dependency updates" (the steps a
  code owner takes, the red-run case, a major bump of a runtime dependency); the Tests paragraph of that page;
  `CHANGELOG.md` under `### Changed`; this amendment, the decision record, the index row.

**Requirements added.**

- **R-11** The linked-issue and fields checks pass a dependency update with the notice and fail a pull request missing
  any one of the three conditions (the bot, the label, the base `dev`); the merge check passes a code owner's merge of
  one. Checked by `tests/test_admissibility.py`.
- **R-12** `test.yml` runs on a pull request into `dev` for Dependabot alone, the fast shard, with `controls`; a
  pull request into `dev` by anyone else runs no job; `main`'s pull requests, the push to `dev`, the call and the
  dispatch are unchanged. Checked by `tests/test_ci_shards.py`, `tests/test_release_workflows.py`,
  `tests/test_workflow_permissions.py` and `uv run python scripts/release_checks.py pins`.
- **R-13** The docs page carries no package number, "supervisor" or "reviewer"; the vocabulary check adds no term.
  Checked by `tests/test_site.py::test_hand_written_pages_carry_no_review_or_proof_content` and
  `scripts/check_vocabulary.py`.

**Agent's defaults (Amendment 2).**

- `.github/dependabot.yml` is not added to the secondary rules. It is configuration downstream of the route, which is
  stated in two governed files (`GOVERNANCE.md`, `.github/PR_ADMISSIBILITY.md`) and enforced by the admissibility
  script and the test workflow's trigger; a drift in it (a target other than `dev`, the label gone) is caught on the
  bot's next pull request, which then fails the linked-issue and fields checks as any other would, and a test holds
  the file to its target, label and groups. Keeping it out leaves the `governance-files` ruleset's path list, the
  CODEOWNERS lines, the declaration, the fixture and the count of nine unchanged, so his post-merge settings list does
  not grow.
- The `controls` job runs on the bot's pull request: its endpoints need Metadata (always granted), Actions (read) and
  Pages (read), which the job declares, and a Dependabot-triggered run's token keeps the read permissions and loses
  the writes and the secrets, none of which the job uses. The first Dependabot pull request after the merge is the
  live check; should the job read red for a permission reason, the fallback is to extend the job's `if` to skip it on
  that event, with the `test` job's `needs` already accepting `skipped`.
- The gate is `github.actor == 'dependabot[bot]'` on a `pull_request` into `dev`, on `controls` and on `test` (with
  `controls` skipped the shard would otherwise run, since the release's call runs `controls` itself). A hand push to
  the bot's branch makes the pusher the actor and skips the run; `@dependabot rebase` restores it. Windows was
  already off on every pull request.
- The fast shard alone on the bot's pull request, as on the push to `dev` (the full matrix stays the release pull
  request's); the matrix expression reads `github.base_ref == 'dev'` beside the push case.
- The row's three conditions are all required: a person's pull request carrying the `dependencies` label is read as
  any other, and so is a bot pull request into `main`. `pr-fields.yml` gains the `labeled` type because Dependabot
  applies the label after the open, so an `opened` payload may not carry it yet; the later `labeled` event re-runs
  the check (the linked-issue workflow already fires on `labeled`).
- The groups are named `actions-minor-and-patch` and `python-minor-and-patch`, `patterns: ["*"]`, `update-types:
  ["minor", "patch"]`; a major bump is outside every group and arrives alone.
- The notice reads `a dependency update; the row says: <the row>`, the shape of the merge check's notice.
- `CONTRIBUTING.md`'s sentence ("Dependency updates arrive as pull requests from the update bot and go through the
  same review as any change") stays true and is not touched.

**After the merge (the eight open pull requests #4 to #11 against `main`).** A code owner, in this order: on the
repository's Insights, Dependency graph, Dependabot page, "Check for updates" for `github-actions` and for `uv`, which
runs the bot with the new configuration; the bot's new pull requests arrive against `dev`, grouped, with the label.
Each pull request still open against `main` afterwards is closed with a one-line comment naming the route ("dependency
updates target `dev`; superseded by #n"). Whether the bot closes the `main` pull requests itself as superseded when the
target changes is observed at that first run; a bump the bot does not recreate against `dev` within that run is
brought by the next weekly run or by "Check for updates" again. Each new pull request is then merged on its own by a
code owner after the Tests workflow passes on it, an admin where it moves an action pin, following "Dependency
updates" on the code owners' page.

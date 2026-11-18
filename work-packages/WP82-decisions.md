# WP82 — Decisions: the 0.2 governance update (the bypass removal and WP78's gap items)

Supervisor: Michael Zargham (`mzargham`). Every answer below is his, quoted verbatim from the popup he answered; the
question is paraphrased. Branch `governance-bypass-removal`, cut from `dev` 7973fbd1 on 2026-11-17; the pull request
into `dev` opens after `dev` is merged into `main` for 0.1 (his word, below), for `danlessa` to review and merge.

## His ask (2026-11-17, evening, in the v0.2 session), verbatim

> if you wrap up the doc site work. i need you to go back and interrogate the governance change part of 0.2. i made
> some changes on dev as i am working on getting 0.1 out. you may need to make sure our governance changes in 0.2 have
> a PR that will actually clear. once dev goes into main for the 0.1 release i need PRs for the governance update and
> the documentation update for dev. to share with danilo and team

**Applied as.** The live settings read back conforming to `dev`'s declaration (61 fields, a local run). The bypass
removal was prepared first as one commit (2044e6ff: the declaration, the recorded fixture hand-edited to the declared
state, the local-only test turned around, `GOVERNANCE.md`, the code owners' page, the 0.2 changelog entry) and checked
(66 governance tests; the checker conforming on the fixture and in runner mode, one difference live until the ruleset
page changes; ruff clean). What a pull request into `dev` must clear, read from `dev`: `closes #n` or `small-fix`;
the template's five sections; a merge by a code owner who is not the author (the row binds with three code owners);
no test runs on a pull request into `dev`, the suite and the `controls` job run on the push after the merge. The
readiness note is in the sessions' shared notes folder (`0.2-pull-requests-readiness.md`).

## What the governance pull request carries (2026-11-17)

Asked whether the pull request carries the bypass removal only (his release line), the bypass plus gap items he names,
or waits for 0.1. His answer, verbatim:

> Bypass plus gap items

Asked which of WP78's gap items (`work-packages/WP78-rounds/gaps.md`) go in, any number of: the default workflow
permissions to read (gap 1, local-only); `controls` as a required status check on `main` (gap 3, runner-checked, so the
push to `dev` after the merge is red until the setting follows); a control on the governed files (amendment 2, the
mechanism a second question); the admissibility rows (gaps 4, 6, 7, documents only). His answer, verbatim:

> Workflow permissions to read,controls required on main,A control on the governed files,The admissibility rows

**Applied as.** All four, in this one pull request with the bypass removal. Gap 2 (the local-only fields: keep them,
a token with Administration (read), or the fields out of the declaration) was not offered and is not changed: the
default workflow permissions and the rulesets' bypass actors stay local-only. Gap 5 is WP79's; gap 8 names non-goals;
gap 9 is done.

## The mechanism for the governed files (2026-11-17)

Asked which of GitHub's mechanisms the declaration adopts for the governed files (a push ruleset restricting the
governed paths; CODEOWNERS path lines; a review rule with file patterns; CODEOWNERS lines plus a push ruleset), with
each one's reach, bypass and cost to direct commits on `dev` as the gaps readout lays them out. His answer, verbatim:

> CODEOWNERS lines plus a push ruleset

**Applied as.** `.github/CODEOWNERS` gains a line per governed path naming who approves a change to it (his principle
of 2026-11-17, 13:40: CODEOWNERS is the source of truth for authority); a push ruleset restricts pushes that touch the
governed paths, with a bypass list that keeps a code owner's direct commits to `dev` possible; the declaration gains the
fifth ruleset and the `control` field of each `governed_files` entry names both; `scripts/admissibility.py` reads the
path lines. Who the lines name and who the push ruleset's bypass is are the next two questions.

## The push ruleset's bypass list (2026-11-17)

Asked who is on the bypass list of the push ruleset on the governed files (always on; a pull request's merge is a push,
so with no bypass nobody could change a governed file): the Repository admin role (today him and Danilo; direct
commits to `dev` by an admin continue, anyone else changes governed files through a pull request an admin merges);
Maintain and above; an organisation team he names. His answer, verbatim:

> Repository admins

## Whom the CODEOWNERS path lines name (2026-11-17)

Asked whom the path lines name as the approvers of each governed file: him alone; him and Danilo (the admins,
matching the push ruleset's bypass); all three code owners written out per path. His answer, verbatim:

> All three code owners

**Applied as.** One line per governed path, each `@mzargham @danlessa @rororowyourboat`; the push ruleset
`governance-files` restricts pushes touching those paths with `RepositoryRole` 5 (Repository admin), mode `always`,
as its one bypass actor; the declaration's `control` field of every governed file names both. Who may approve is
the lines; who may push is the ruleset.

## Approval of the scope (2026-11-17)

Asked whether he approves `WP82-scope-of-work.md` at 19f64d5b for execution (the bypass removal; the four gap items;
the checker, fixture and tests following; the window written down; no setting changed by anyone but him, after the
merge; the Agent's defaults as one item). His answer, verbatim:

> Approved

Execution runs on `governance-bypass-removal`; the pull request waits for `dev` to be in `main` for 0.1.

## Execution (2026-11-17, evening)

Branch `governance-bypass-removal`, rebased onto `dev` 7b0d7cdf (the paper's route, WP79, landed there while the
package was scoped); content head 9fa94658. The live check on the branch, `uv run python scripts/check_repo_settings.py`,
reports five differences (six with Amendment 3's `general.delete_branch_on_merge`), which are the settings he
changes on GitHub after Danilo merges the pull request, in this order (a runner-checked field first, so the window is
short):

1. Settings, Rules, Rulesets: the `main-checks` ruleset's required status checks gain `controls` (runner-checked:
   the `controls` job on the push to `dev` is red until this and item 2 are done).
2. Settings, Rules, New push ruleset `governance-files`, enforcement active, "Restrict file paths" with the nine
   governed paths of the declaration, bypass list: Repository admin, always (runner-checked).
3. Settings, Rules, Rulesets, `main-review`: remove the bypass actor (local-only).
4. Settings, Actions, General, Workflow permissions: read, and untick "Allow GitHub Actions to create and approve
   pull requests" (local-only).
5. Settings, General, Pull Requests: "Automatically delete head branches" on (runner-checked; Amendment 3).
6. A local run reads `conforming (70 fields)`; `--runner` reads `conforming (63 fields on the runner; 7
   local-only)`; a `--record tests/data/wp78` run replaces the hand-edited fixture with recordings (a follow-up
   commit). Re-run the red `controls` job.

The live lines on the branch before any of that, verbatim: `rulesets: expected ["dev", "governance-files",
"main-checks", "main-review", "paper"], found ["dev", "main-checks", "main-review", "paper"]`;
`rulesets.main-review.bypass_actors: expected [], found ["User:10465438:pull_request"]`;
`rulesets.main-checks.rules.required_status_checks.required_status_checks: expected ["admissibility", "controls",
"test (docs)", "test (fast)", "test (slow)"], found ["admissibility", "test (docs)", "test (fast)", "test (slow)"]`;
`actions.default_workflow_permissions: expected "read", found "write"`;
`actions.can_approve_pull_request_reviews: expected false, found true`; and, from Amendment 3,
`general.delete_branch_on_merge: expected true, found false`.

Decided during execution (the Agent's defaults, noted here): the bug and question rows name the form's required
fields as their machine side and the triaging code owner as their judged side; the judged rows cite the paragraph of
`CONTRIBUTING.md` or the section of `docs/code-owners.md` by name; the permissions test accepts a workflow whose own
line reads contents and writes issues or pull requests for its one job.

## The push ruleset on a public repository (2026-11-17, from the independent read)

GitHub's documentation offers push rulesets for "a private or internal repository"; this repository is public, and
the session could not tell from the API without creating one. Asked whether Settings, Rules, Rulesets, New ruleset
offers "New push ruleset" here (else CODEOWNERS lines alone, or a review rule on `dev`). His answer, verbatim:

> Yes, it is offered

The branch stands as built. The reviewer's other findings (the ordered settings list on the code owners' page as the
scope asks; three `GOVERNANCE.md` sentences; the index row's columns; the checker's branch test by target) are fixed in
the review's second pass, `WP82-review.md`.

## Acceptance (2026-11-17)

Asked whether he accepts WP82, delivered on `governance-bypass-removal` at a99e2ca2 with `WP82-review.md` recommending
acceptance (the declaration with the bypass removal and his four items; the fixture and the runner mode conforming; the
live run's five lines his post-merge settings account for; the fast suite 2,036 passed; the independent read's findings
fixed or dispositioned; the code owners' page captured). His answer, verbatim:

> Accepted

The pull request into `dev` opens after `dev` is in `main` for 0.1, for `danlessa` to review and merge; then his five
settings changes in the order under "Execution".

## Amendment 1: the versioning rule (2026-11-17, evening)

His words, in this order, verbatim:

> i recommend we also indicate that the governance update is the reason why this qualifies as an 0.2.0 rather than an
> 0.1.1 since documentation updates since didn't touch the optimizer just the documentation and the governance
> machinery

> i think we probably need to ensure we have explicit guidance and checks for semantic versioning. this also probably
> amounts to changes in the governance

Asked where the versioning rule lands (amend WP82: the rule, the surface record and the check join the 0.2 governance
pull request before it opens; its own package in 0.2; its own package after 0.2). His answer, verbatim:

> Amend WP82

**Applied as.** Amendment 1 of `WP82-scope-of-work.md` (goal G4, deliverables D-7 to D-10, requirements R-8 to R-10,
the Agent's defaults listed there), delivered on the governance branch before the pull request opens: a `## Versions`
section in `GOVERNANCE.md` (the patch, minor and major rule while the major is 0; the executable and the judged side;
the sentence that 0.2.0 is minor for the governance update with the package's code unchanged since 0.1.0); the public
surface as the record `tests/data/api_surface.json`, written by `scripts/api_surface.py` and held equal to the package
by `tests/test_api_surface.py`; the release check `scripts/release_checks.py version-kind` in `release.yml`'s
admissibility job, with its tests; the machine row and the judged part in `.github/RELEASE_ADMISSIBILITY.md`, the test
named in `.github/PR_ADMISSIBILITY.md`, the rule on the code owners' page, the changelog entry under `### Added`. The
secondary-rules list and the declaration are unchanged: the record is a record, not a rule.

## Amendment 2: the Dependabot route (2026-11-17, evening)

His sentence at about 20:50 EST, with a screenshot of the eight open Dependabot pull requests #4 to #11 (each "Review
required", 15 of 18 checks failing), verbatim:

> we're going to need to handle this stuff. in v0.2 if possible

The driver's finding: `.github/dependabot.yml` named no `target-branch`, so Dependabot's pull requests targeted
`main`, the default branch, and were judged as releases: the release `admissibility` job, the template-fields check and
the linked-issue check failed on each, while `controls` and the three test shards passed on every bump. Asked where
the Dependabot route lands (target branch `dev`, the labels, the bot's admissibility row, tests on its pull requests),
with the options "Amend WP82", "Own package in 0.2" and "After 0.2", his answer, verbatim:

> Amend WP82

At about 21:15 EST, verbatim:

> i also think we should extend our governance PR content to provide instructions for how dependabot PRs should be
> handled since it seems like they will be a common occurance (some of our dependencies are advancing rather quickly)

**Applied as.** Amendment 2 of `WP82-scope-of-work.md` (goal G5, deliverables D-11 to D-14, requirements R-11 to
R-13, the Agent's defaults and the "After the merge" steps listed there), delivered on the governance branch before
the pull request opens: `.github/dependabot.yml` targets `dev` with the `dependencies` label, minor and patch bumps
grouped weekly per ecosystem and a major on its own; a dependency row in `.github/PR_ADMISSIBILITY.md`, which the
linked-issue and fields checks of `scripts/admissibility.py` pass with a notice quoting it (the three conditions: the
bot, the label, the base `dev`), `pr-fields.yml` firing on `labeled` too; `test.yml` running lint, `controls` and the
fast shard on the bot's pull requests into `dev` and nothing on anyone else's; the route in `GOVERNANCE.md`'s
pull-request paragraph and the code owner's steps in `docs/code-owners.md`, "Dependency updates"; the changelog entry
under `### Changed`. `.github/dependabot.yml` is not added to the secondary rules (the reason is in the amendment's
defaults); the declaration, the fixture and the governed set are unchanged. The eight pull requests against `main` are
handled after the merge as the amendment says: "Check for updates" on the Dependabot page, the stale ones closed with a
one-line comment naming the route, each new one merged on its own by a code owner after the Tests workflow passes.

## Amendment 3: the gates prepared by command (2026-11-17, evening)

Two failures earlier in the evening. A release dry run of a content branch at version 0.1.0, pushed to `qc/release`, was
refused by the `tag` check: `v0.1.0` is on `main`'s merge commit and the package files had changed since it, so the
head was `taken`, the rule's answer to a released version with changed package files. The throwaway version bump
then made by hand set five of the six places the version is written and missed the contract document's quoted value;
`tests/test_interface_contract.py::test_r8_document_quotes_the_manifest` caught it.

His sentence at about 21:10 EST, verbatim:

> do we need to update how we do dry runs or how we prepare our code before dry runs so we don't have these kinds of
> errors in the future. in general i'd prefer to set up our processes to not fail the gate, than relax the gate

Asked where the release-preparation tooling lands (the one-command version bump, the gates runnable locally, the page
naming them), with the options "Own package in 0.2", "Amend WP82" and "After 0.2", his answer within minutes, verbatim:

> Amend WP82

At about 21:20 EST, verbatim:

> i am also seeing branch sprawl on github remote. another SOP we may need integrated into our governance work is
> making sure we're cleaning up after ourselves

**Applied as.** Amendment 3 of `WP82-scope-of-work.md` (goal G6, deliverables D-15 to D-18, requirements R-14 to
R-17, the Agent's defaults listed there), delivered on the governance branch. No gate is relaxed.
`scripts/release_checks.py bump <version> --changelog final|stub|none [--date]` writes the version in its six places
(`pyproject.toml`, `__version__`, `CITATION.cff`, the contract manifest and the two values its document quotes),
refreshes the lock and edits the changelog for a release or a dry run; `scripts/release_checks.py gates [--release]`
runs the Tests workflow's checks, the vocabulary, surface, settings and branch checks and, with `--release`, the
admissibility checks locally, one line each with a verdict, the step before a report, a push, a pull request or a dry
run; `scripts/release_checks.py branches` names a remote branch the rules do not account for. The branch rule is
`GOVERNANCE.md`, "Branches", with `delete_branch_on_merge = true` declared in `.github/governance.toml` (`[general]`,
since the key `repository` is the repository's name) and compared by the settings check from
`GET repos/{owner}/{repo}` on the runner; live it is `false` today, the sixth difference, item 5 of the post-merge list
under "Execution" above; the fixture's `repository.json` is recorded and edited to the declared value, 70 fields. The
dry-run step is "A dry run" on the code owners' page: a throwaway `bump <next version> --changelog stub` commit on
top of the head, `gates --release` green, pushed to `qc/release`, never merged, deleted after the run; the checklist's
row R2 says the same.

The runs. At the content head 312a16c2, `gates --release` reads 12 of 15 green and three refusals, each the correct
answer: `repository settings` (the six live differences, his post-merge list), `branches` (`origin/deps-2026-11`,
stray, with `qc/release` noticed as a dry-run branch left behind; both a code owner's to delete) and `tag`
(`v0.1.0 is taken: v0.1.0 is on 74e62fdaf256, which is not an ancestor of 312a16c2cc5a`, a content branch at a
released version). On a throwaway commit over it, `bump 0.2.0 --changelog stub` (seven files, `uv.lock` among them),
the same command reads `version: 0.2.0`, `tag: v0.2.0 is new`, `changelog --final` ok, `version-kind: 0.2.0 after
v0.1.0 is a minor release`, `pins` ok, the paper's mode ok: every release gate green; the commit was dropped. That
run also caught a test of this amendment that pinned the stub version instead of reading the current one; fixed in
the records commit.

## Records ride with the work they record (2026-11-17, about 21:45 EST)

Seeing five record-only commits on `dev` tonight (the driver log, the decisions files, the checklists, the board,
pushed under his identity as events happened), his question at about 21:43 EST, verbatim:

> so you are committing the notes from our conversation direct to dev?

Asked where the process records (the driver log, the decisions files, the checklists, the board) go from here, with
the options "Direct to dev, as now", "Batched pull request" and "With the work they record" (records ride in the
package's own pull request and nowhere else; between pull requests they live only in the working tree or outside the
repository), his answer at about 21:45 EST, verbatim:

> With the work they record

**Applied as.** No record-only commit to `dev` from here. Each package's records (its decisions file with his words,
its review, its rows in the index, the checklists it ticks, the board, the driver log's entries about it) land in
that package's pull request; between pull requests they are in the working tree or in the driver's notes outside the
repository. The five record commits of 2026-11-17 evening stay as history. The rule is one sentence in
`work-packages/README.md` ("Branching"); `GOVERNANCE.md`'s sentence on how a governed file is edited is about governed
files and is left as it is; `CLAUDE.md` is not edited. The times written in the driver's entries on `dev` for the
evening of 2026-11-17 after 20:45 EST run ahead of the clock by up to two hours (the entries' sequence is right; the
commit timestamps of 1f154885, eeab5201, faee0f9c, 068e79d9 and 924e253c are the record).


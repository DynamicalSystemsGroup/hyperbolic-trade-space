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

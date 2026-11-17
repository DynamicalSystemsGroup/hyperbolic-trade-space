# Governance

How this repository's rules are made, enforced and changed: the two release lifecycles, the two reviews, who holds
authority, the files that carry the rules, and the check that runs first in every workflow.

## The two lifecycles

The software (the package `tradespace`, the docs and the root page) is released by the merge of a pull request from
`dev` into `main`. Candidates are pull requests into `dev`; `main` holds releases only. The merge starts the Release
workflow (`.github/workflows/release.yml`): it checks the settings against their declaration, checks admissibility,
runs the suite, builds the wheel and the sdist with a software bill of materials, composes the site, creates the tag
`v<version>` and a draft release, publishes to PyPI by trusted publishing, deploys the site and publishes the release.
A merge whose version is already released and whose package files are unchanged since its tag redeploys the site only.
The conditions are `.github/RELEASE_ADMISSIBILITY.md`.

The paper is edited on the `paper` branch and published by a `paper-*` tag there, which `paper.yml` builds, tests and
publishes as a GitHub release once one of the paper's approvers (`jshorish`, `mzargham`) approves the `paper-release`
environment; the one who pushed the tag does not approve it. The paper reaches the site when `paper` is merged into
`dev` and `dev` into `main`. Its change record is `paper/CHANGES.md`, its tests run in its own workflow, and its
contribution route is kept apart from the software's.

## The two reviews

Two decisions, by two people, with two questions.

Into `dev`, a review of the work. A code owner who is not the pull request's author asks: does this do what its
issue says, and is each good-enough item met (conformance by running the check, fitness by looking)? The conditions
are `.github/PR_ADMISSIBILITY.md`; the review is recorded in the pull request, the merge under the merger's name.

Into `main`, a review of the release. A code owner who is not the pull request's author asks: is this candidate the
release? They read the changelog entry, the release issue the pull request closes and the staged site, and merge.
The merge is the decision; the `pypi` environment waits for nobody else. A pull request's author cannot approve it,
so for the 0.1 release the `main-review` ruleset carried a bypass for one named user (`mzargham`) on pull requests
(decided 2026-11-17; set by name that afternoon), and 0.1 was merged on it. The bypass is removed after 0.1 by a
change to the declaration first, then to the ruleset, in a pull request of its own, named in the 0.2 changelog; the
0.2 release is the first through the review rule without it, attested by a code owner's local run of the checker.

## The paper's route

A change to the paper is a pull request into `paper`, reviewed and merged by a paper approver (the `paper/` line of
`.github/CODEOWNERS`) who is not its author: the merge check records it, as it records a merge into `dev`. The
approver reads for the argument (each claim backed, the glossary's words); the paper workflow checks the build, the
tests, the residual counts and the key manifest on the push that the merge makes. The pull request template's
`Paper` section names the section or figure changed, the residual check's result and the build, and the pull request
check reads it on that base. A pin is a `paper-*` tag pushed by an approver, approved at the `paper-release`
environment by the other, and recorded in the mode file; it reaches the site by the merge of `paper` into `dev` and
of `dev` into `main`. The `paper` ruleset forbids deletion and force pushes, as `dev`'s does; files under `tests/`
and `scripts/` change on `dev`. The route in full is "Contributing to the paper" in `CONTRIBUTING.md`.

## Authority

`.github/CODEOWNERS` is the source of truth for authority in the repository: the logins on its `*` line are the
code owners, the people who approve drafts, review and merge candidates, and release; the logins on its `paper/`
line are the paper's approvers, who review and merge pull requests into `paper` and approve a paper tag's
publication, and who are not thereby code owners. Every check that asks who may do something reads that file; no
other list exists. Each code owner, and each paper approver, is a collaborator with at least the access the
declaration names for their line, which the settings check verifies. The `paper-release` environment's required
reviewers are the paper's approvers, declared with it.

## The secondary rules

The files that say how the repository's rules are made, changed and enforced are its secondary rules (rules about
rules). The set is small and enumerated; adding a file to it is itself a governed change. Each is executable (a
script or a test checks it) or a guideline (a named role judges it):

- `.github/CODEOWNERS` — executable: `scripts/check_repo_settings.py` checks each code owner's and each paper approver's access; the merge check (`scripts/admissibility.py`) reads both lines.
- `.github/governance.toml` — executable: the declaration of the settings; `scripts/check_repo_settings.py` in the `controls` job, `tests/test_repo_settings.py`.
- `.github/workflows/*.yml` — executable: `scripts/release_checks.py pins` and the workflow tests (`tests/test_release_workflows.py`, `tests/test_ci_shards.py`, `tests/test_release_checks.py`, `tests/test_paper_model.py`).
- `GOVERNANCE.md` — guideline: a code owner judges a change to it at review; its list of secondary rules is tested against the declaration.
- `.github/ISSUE_ADMISSIBILITY.md` — guideline: the code owner who removes the `draft` label judges the fitness rows; the machine rows run in the issue workflows.
- `.github/PR_ADMISSIBILITY.md` — guideline: the code owner who reviews and merges judges the fitness rows; the machine rows run in the pull request workflows and the test workflow.
- `.github/RELEASE_ADMISSIBILITY.md` — guideline: the code owner who merges the release judges the fitness row; the machine rows run in the release workflow.
- `.github/ISSUE_TEMPLATE/*.yml` — executable: `tests/test_admissibility.py` checks that the scope-of-work template carries the fields the checks read.
- `.github/pull_request_template.md` — executable: `tests/test_admissibility.py` checks that it carries the sections the pull request check reads.

Each is changed by a pull request into `dev` or a direct commit to `dev`, approved by the owners on its own
`.github/CODEOWNERS` line (the three code owners) and pushed by a Repository admin: the `governance-files` push
ruleset refuses a push that touches one of these paths by anyone else, a pull request's merge included, so a
candidate that changes a governed file is merged by an admin (decided 2026-11-17). The declaration's `codeowners`
and `control` fields record both.

## The declaration and the check

`.github/governance.toml` declares the settings that enforce the release rules: the five rulesets (`main-review`,
`main-checks`, `dev`, `paper`, and `governance-files`, the push ruleset on the governed files) with their rules,
parameters and bypass actors; the four environments
(`github-pages`, `pypi`, `testpypi`, `paper-release`) with their reviewers and branch or tag policies; the Pages
build; the code owners' and the paper approvers' minimum access; the default workflow permissions. `scripts/check_repo_settings.py` reads
the live settings through the GitHub API, compares them with the declaration field by field, prints each
difference and exits non-zero on any; an endpoint it cannot read fails the check by name, never silently. A
field the declaration marks `checked_on = "local"` is not read on the runner: today the default workflow
permissions (their endpoint needs a permission the workflow token never has) and the rulesets' bypass actors (the
API returns them to administrators only; the token sees an empty list). The job's report lists those fields as not
checked there, with the reason, and a code owner's local run checks them; the removal of the `main-review` bypass
after 0.1 is therefore attested by that local run and the ruleset page, not by the runner, and until the settings
a declaration change names are changed that local run reports each of them as a difference.

The `controls` job runs it first in the Tests and Release workflows; every other job needs it, so no test, build or
publish runs while a setting differs from its declaration. Its report is the job summary. A change to a setting
starts with the declaration: the declaration changes, then the setting, and the next run checks them. For a field
the runner checks (a ruleset, a required check) the `controls` job is red on the first push to `dev` after the
merge until the setting follows, so the merger changes the setting in the same sitting and re-runs the job; a
local-only field is attested by a code owner's local run.

Attestation: a release's run summary and its GitHub release notes carry the line
`Controls: .github/governance.toml@<hash> checked at <merge commit>: conforming (N fields on the runner; M
local-only)`, so the release states which rules were declared, at which commit, that they were in effect when it was
made, and which fields a code owner checks by hand.

## How the repository is organised

- `src/tradespace/`: the package; `tests/`: its suite, the docs and site checks, and the checks of the rules on this page.
- `derivation/`: the method's results as SymPy lemma scripts; `examples/adcs/`: the cubesat case study.
- `docs/`: the user guide and API reference; `site/`: the root page; `paper/`: the paper's notebooks and build.
- `scripts/`: build, check and release tools, among them `admissibility.py`, `release_checks.py` and `check_repo_settings.py`.
- `work-packages/`: each package's scope, decisions and review; `notes/`: the live guidance.
- `.github/`: the secondary rules, the workflows and the dependency bot.

Issues are templated: a scope of work (`.github/ISSUE_TEMPLATE/scope-of-work.yml`, labelled `draft` until a code
owner approves it), a bug report and a question; blank issues are off, and security reports go to the private
advisory form. Pull requests have one template (`.github/pull_request_template.md`), target `dev` (`paper` for a
change to the paper, with the template's `Paper` section filled), and name the issue they resolve or carry the
`small-fix` label.

Criteria are of two kinds. Executable: the rows marked machine in the three admissibility documents, run by the
issue and pull request workflows, the test workflow (lint, format, lock, the three test shards, the attribution
check) and the release workflow (version, tag, changelog, pins, bill of materials, merge, the PyPI hash check), and
the `controls` job. Judged: the rows marked fitness, decided by the code owner each row names, with the guideline
in `CONTRIBUTING.md` ("Review is against the scope") and the code owners' page (`docs/code-owners.md`, "Reviewing a
candidate" and "Cutting a release"); each judged row names its guideline. A check with no row, or a judged criterion
with no guideline, is a gap, listed for decision in `work-packages/WP78-rounds/gaps.md` (the items he decided on
2026-11-17 are WP82's; the local-only fields' item stays open there).

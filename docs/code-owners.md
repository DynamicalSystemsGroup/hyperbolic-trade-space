# Code owners

For a code owner: who the code owners are, the repository settings that enforce the contributing page,
how a candidate is reviewed, how a release is cut, and how a code owner is added. Contributors read
`CONTRIBUTING.md` in the repository instead.

## Who the code owners are

The code owners are the logins on the `*` line of `.github/CODEOWNERS`. That file is the record of who may approve,
merge and release; the checks below read it. Name users, not teams: the checks do not expand a team.

## The flow

The software (the package and the docs) and the paper have separate release lifecycles. Candidates are pull
requests against `dev`. `main` holds releases only: the merge of a pull request from `dev` into `main` is the
software's release, and nothing else reaches `main`. The paper is edited on the `paper` branch and published by
pushing a `paper-*` tag there; the merge of `paper` into `dev`, then the next merge of `dev` into `main`, carries a
published paper to the site. Nothing publishes except that merge, a `paper-*` tag the paper's approvers approve, or a
dispatch of the Release workflow on `dev` with the target `testpypi`. How a change to the paper is proposed, approved
and published is the section "Contributing to the paper" of `CONTRIBUTING.md`. The rules in full, the two reviews and
the repository's secondary rules are in `GOVERNANCE.md` at the repository root.

## Repository settings

The rulesets, the environments, the Pages source, the code owners' access and the workflow permissions are declared
in `.github/governance.toml` and checked against the live repository by `uv run python
scripts/check_repo_settings.py`, which runs first in every CI run as the `controls` job (`GOVERNANCE.md`). Set each
on GitHub to match the declaration, then run the checker; to change one, change the declaration first, then the
setting. A field the runner checks (a ruleset, a required check) turns the `controls` job red on the first push to
`dev` after the merge until the setting follows: change it in the same sitting and re-run the job. A local-only
field (the workflow permissions, a ruleset's bypass actors) is attested by your local run. The settings below are
the ones the declaration does not hold.

The governed files (`GOVERNANCE.md`, the secondary rules) each have their own `CODEOWNERS` line naming the three
code owners as the approvers of a change to them, and the `governance-files` push ruleset refuses a push that
touches one of them by anyone but a Repository admin; a pull request that changes a governed file is merged by an
admin.

After the merge of the 0.2 governance change, in this order: 1. `main-checks` gains the required check
`controls`; 2. the push ruleset `governance-files` is created (active; the nine governed paths; bypass Repository
admin, always); the `controls` job on the push to `dev` is red until these two are done, then re-run it; 3.
`main-review` loses its bypass actor; 4. the workflow permissions become read, approving reviews off; 5. your local run
reads `conforming (69 fields)`, and `uv run python scripts/check_repo_settings.py --record tests/data/wp78` re-records
the fixture in a follow-up commit.

Settings, Labels: create `draft` and `small-fix`. The scope-of-work template applies `draft`; a code owner removes it
to turn a draft into an issue. `small-fix` stands in for an issue on a pull request that fixes a typo or a broken link.
The label `release-failure` is created by the Release workflow.

The Tests workflow runs on every pull request into `main` (the required checks), when the Release workflow calls it,
and on dispatch (Actions, Tests, Run workflow), which also runs Windows. A push to `dev` runs lint and the Linux
fast shard only. It never runs Windows on a pull request or a push. Its first job, `controls`, is the settings check;
the shards need it.

PyPI and TestPyPI: a pending trusted publisher for `tradespace`, owner `DynamicalSystemsGroup`, workflow
`release.yml`, environment `pypi` (TestPyPI: `testpypi`). No token is stored anywhere.

Zenodo: off until the paper's first full draft is approved (decided 2026-11-17). Once the repository is
switched on in Zenodo's GitHub settings, every GitHub release published from then on, the software's and the
paper's, is archived with a DOI. `CITATION.cff` is the metadata it reads.

## What the workflows check

Five workflows read the machine rows of the admissibility conditions (`.github/ISSUE_ADMISSIBILITY.md` and
`.github/PR_ADMISSIBILITY.md`). Workflows triggered by issue events run from the default branch, so they act once the
files are there. Each is a script in `scripts/admissibility.py`; none runs code from an issue or a pull request.

- A draft issue is checked when opened or edited: every field of the scope-of-work template is present, and each
  good-enough item is marked conformance or fitness. On a gap it comments and keeps the `draft` label.
- Removing `draft` by anyone but a code owner is reverted, with a comment.
- A pull request must say `closes #n` or carry `small-fix`, and fill every section of its template.
- A merge into `dev` is recorded: by a code owner who is not the author. While the code owners are one person the
  check passes with a notice that quotes the condition; the notice stops the day a second code owner is added.

## Pinned actions

Every third-party action in `.github/workflows/` is pinned to its full commit SHA, with the release tag in a
trailing comment. A tag can be moved to different code after the fact; a SHA cannot, so a compromised action
release cannot reach the publishing job unseen. Dependabot (`.github/dependabot.yml`, weekly, for `github-actions`
and `uv`) opens a pull request that moves a pin and its comment together; read the action's release notes, then
merge into `dev`. To move one by hand, resolve the new tag with
`gh api repos/<owner>/<repo>/git/ref/tags/<tag>` (follow an annotated tag to its commit) and replace both the SHA
and the comment. The Release workflow refuses a release while any action is unpinned.

## Reviewing a candidate

Read the pull request template's answers (what changed, what backs it, which tests, defaults, tools used). Run the
tests and the code yourself, and look at any rendered result (a docs page, a plot, the paper) rather than reading the
source alone. A claim with no backing is narrowed or dropped. Take the issue's good-enough items one by one:
conformance by running the check, fitness by looking and signing the judgement. Merge into `dev`.

## Cutting a release

1. On `dev`: set `version` in `pyproject.toml` (and `uv lock` to refresh `uv.lock`), move the Unreleased entries
   in `CHANGELOG.md` under the new version with the date, and commit.
2. Optionally dispatch the Release workflow on `dev` with target `testpypi` (a candidate version such as
   `0.1.0rc1` can be published only once per version). The suite runs first. Install from TestPyPI and try it.
3. Open the pull request from `dev` into `main`, closing a release issue ("Release 0.1.0"). Its checks are the
   three test shards and `admissibility`. `admissibility` refuses the pull request unless the version is new (or
   the merge is site-only, below), the changelog has the entry, the lock is current and every action is pinned; it
   also refuses while a Release run on `main` is queued or in progress. Stage the site, review it, and record the
   review in the release issue.
4. Merge it (merge commit). One release pull request at a
   time, merged after the previous Release run has ended.
5. Watch the run. On the merge commit it checks the settings against their declaration, checks admissibility again,
   runs the suite, and builds and checks the
   wheel, the sdist and the software bill of materials (CycloneDX, from the lock). It composes the site, creates
   the tag `v<version>` and a draft release whose notes end with the settings check's attestation, and publishes
   to PyPI, the one step that cannot be undone. Last, it deploys the site and publishes the release (archived by
   Zenodo once the repository is switched on there).
6. On failure, read the issue the run opens (label `release-failure`). It names the failed job and step, what the
   clean-up removed or kept, and the retry. Before PyPI holds the version, the clean-up removes the tag and the
   draft: a re-run of the whole run, or a new pull request after a fix, starts clean. After PyPI holds it, the
   clean-up keeps them: the retry is a re-run of the failed jobs, or a new version when the cause needs a code
   change. By hand: `uv run --no-project python scripts/release_cleanup.py --tag v0.1.0 --dry-run`.

A merge whose version is already released, with `src/`, `pyproject.toml` and `uv.lock` unchanged since its tag (a
docs fix, a new paper pin), redeploys the site only: no tag, no PyPI, no release. A change to those files with the
version unchanged is refused.

The Release workflow's dispatch on `dev` (target `dry-run`, the default) and a push to a `qc/` branch build, check
the wheel, the metadata and the bill of materials, compose the site, and publish nothing. Giving the dispatch a
`tag` input that differs from the package version shows the refusal.

## Adding a code owner

Add their login to the `*` line and to each governed file's line of `.github/CODEOWNERS`, the source of truth for
authority (`GOVERNANCE.md`); add
them as a collaborator with the access the declaration requires (`.github/governance.toml`, `code_owners`), which
the settings check verifies on the next run; add them as an Owner or Maintainer of the project on PyPI and TestPyPI
(Manage, Collaborators). The paper's approvers are the logins on the `paper/` line of the same `CODEOWNERS` file
and the `paper-release` environment's required approvers, declared in the same declaration and kept apart from the
code owners, who approve, merge and release the code and the documentation. Publishing needs no secret, so there is
no token to hand over.

## Where the records live

`CHANGELOG.md` (user-visible changes), `work-packages/` (each package's scope, decisions and review),
`history.yaml` (the project's history), `claims_register.toml` (claims and their backing), and the first release's
steps (`pypi-checklist.md`, in the release package's record; `work-packages/INDEX.md` names the commit it is read at).

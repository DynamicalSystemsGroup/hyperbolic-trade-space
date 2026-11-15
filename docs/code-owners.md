# Code owners

For a code owner: who the code owners are, the repository settings that enforce the contributing page,
how a candidate is reviewed, how a release is cut, and how a code owner is added. Contributors read
`CONTRIBUTING.md` in the repository instead.

## Who the code owners are

The code owners are the logins on the `*` line of `.github/CODEOWNERS`. That file is the record of who may approve,
merge and release; the checks below read it. Name users, not teams: the checks do not expand a team.

## The flow

Candidates are pull requests against `dev`. `main` holds releases only. A code owner merges `dev` into `main`
(`git merge --no-ff dev`) when the content merits it, and tags a release on `main`. Nothing publishes except a tag
a code owner pushes, or a dispatch of the Release workflow a code owner starts.

## Repository settings

Set once, on GitHub.

Settings, Labels: create `draft` and `small-fix`. The scope-of-work template applies `draft`; a code owner removes it
to turn a draft into an issue. `small-fix` stands in for an issue on a pull request that fixes a typo or a broken link.

Settings, Branches, Add branch ruleset (or Add classic branch protection rule):

- `main`: require a pull request before merging; require status checks to pass (add `test (fast)`,
  `test (slow)`, `test (docs-paper)`); restrict who can push to matching branches (the code owners only); block
  force pushes; restrict deletions.
- `dev`: require a pull request before merging and approval from code owners; require status checks to pass (the
  same three); block force pushes. Turn on "Do not allow approval by the author" (no self-approval) on the day a
  second code owner is added; with one code owner it would block every merge.

The Tests workflow runs on dispatch (Actions, Tests, Run workflow), so a pull request's check appears after a
code owner dispatches it on the pull request's branch.

Settings, Environments: create `testpypi` and `pypi`. On `pypi`, add a required approval by a code owner and
restrict deployment branches and tags to `v*`. On `testpypi`, restrict deployment to the `dev` branch.

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
and the comment. The Release workflow refuses a tag while any action is unpinned.

## Reviewing a candidate

Read the pull request template's answers (what changed, what backs it, which tests, defaults, tools used). Run the
tests and the code yourself, and look at any rendered result (a docs page, a plot, the paper) rather than reading the
source alone. A claim with no backing is narrowed or dropped. Take the issue's good-enough items one by one:
conformance by running the check, fitness by looking and signing the judgement. Merge into `dev`.

## Cutting a release

1. On `dev`: set `version` in `pyproject.toml` (and `uv lock` to refresh `uv.lock`), move the Unreleased entries
   in `CHANGELOG.md` under the new version with the date, and commit.
2. Dispatch the Release workflow on `dev` with target `testpypi` (a candidate version such as `0.1.0rc1` can be
   published only once per version). The suite runs first. Install from TestPyPI and try it.
3. Merge `dev` into `main`: `git checkout main && git merge --no-ff dev && git push`.
4. Tag and push: `git tag v0.1.0 && git push origin v0.1.0`. The Release workflow refuses the tag unless the version
   equals the tag, the changelog has the entry, the lock is current, every action is pinned and the suite passes. It
   builds, checks, writes the software bill of materials (CycloneDX, from the lock, checked to name every locked
   package), and waits for a code owner's approval of the `pypi` environment before it publishes.
5. The workflow creates the GitHub release from the tag with the wheel, the sdist, the bill of materials and the
   changelog entry. Check the PyPI page.

The Release workflow's default dispatch target is `dry-run`: it builds, checks the wheel, the metadata and the bill
of materials, and publishes nothing; its artifacts hold the wheel, the sdist and the bill. Giving it a `tag` input
that differs from the package version shows the refusal.

## Adding a code owner

Add their login to the `*` line of `.github/CODEOWNERS`; add them as a collaborator with write access and to the
`main` ruleset's allowed pushers; add them as an Owner or Maintainer of the project on PyPI and TestPyPI (Manage,
Collaborators); add them as an approver of the `pypi` environment; turn on no self-approval on `dev`. Publishing
needs no secret, so there is no token to hand over.

## Where the records live

`CHANGELOG.md` (user-visible changes), `work-packages/` (each package's scope, decisions and review),
`history.yaml` (the project's history), `claims_register.toml` (claims and their backing), and the first release's
steps (`pypi-checklist.md` in the release package's folder under `work-packages/`).

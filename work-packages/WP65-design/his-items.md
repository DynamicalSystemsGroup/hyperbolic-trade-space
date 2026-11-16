# WP65 D-3: his keyboard items and the details that remain his

Settings no agent can make: none exists today (WP64 readout, live state of 2026-11-16). Do them before the first
pull request from `dev` into `main` (build plan, section 6); the driver reads each back with `gh api` afterwards.
Where a setting depends on one of his three questions (the last section), the step names the question.

## 1. Pages

Repository, Settings, Pages, Build and deployment, Source: **GitHub Actions**. Nothing else on the page.

## 2. Environments

Settings, Environments.

- **`github-pages`** (created by GitHub when Pages uses Actions; otherwise New environment, name `github-pages`):
  Deployment branches and tags, **Selected branches and tags**, Add deployment branch or tag rule, type Branch,
  name pattern `main`. No required reviewers. No secrets.
- **`pypi`**: New environment, name `pypi`. Deployment branches and tags, **Selected branches and tags**, rule type
  Branch, pattern `main`. Required reviewers: **none** (the merge is the release decision; `specification.md`, 6.2).
  No secrets.
- **`testpypi`**: New environment, name `testpypi`. Deployment branches and tags, Selected branches and tags, rule
  type Branch, pattern `dev`. No reviewers, no secrets.
- **`paper-release`** (only if question 3 is answered with an approval): New environment, name `paper-release`.
  Deployment branches and tags, Selected branches and tags, rule type Tag, pattern `paper-*`. Required reviewers:
  `mzargham`; **Prevent self-review off** (you push the tag, so with it on you could not approve). No secrets.

## 3. Rulesets

Settings, Rules, Rulesets, New ruleset, New branch ruleset. For each: Enforcement status **Active**.

**`main`** (target: Add target, Include default branch). Bypass list and the review rule per question 1.
- Restrict deletions: on.
- Require a pull request before merging: on. Required approvals and "Require review from Code Owners" per
  question 1. Allowed merge methods: **Merge** only.
- Require status checks to pass: on. "Require branches to be up to date before merging": on. Add checks, typed
  exactly, source **GitHub Actions**: `test (fast)`, `test (slow)`, `test (docs)`, `admissibility`.
- Block force pushes: on.
- Everything else off (no linear history: the release is a merge commit).

**`dev`** (target: Include by pattern, `dev`). Bypass list empty.
- Restrict deletions: on. Block force pushes: on. Nothing else (the driver commits to `dev` directly).

**`paper`** (target: Include by pattern, `paper`; create the branch first or let the ruleset wait for it). Same as
`dev`.

No tag rulesets: the clean-up deletes a failed release's tag with the workflow's token, and a tag rule would block it
unless GitHub Actions is a bypass actor, which GitHub's pages do not state.

## 4. Trusted publishers

**PyPI**: pypi.org, signed in, Your account, Publishing, Add a new pending publisher, GitHub tab:
PyPI Project Name `hyperbolic-trade-space`; Owner `DynamicalSystemsGroup`; Repository name
`hyperbolic-trade-space`; Workflow name `release.yml`; Environment name `pypi`; Add. (If the project already exists
there: the project, Manage, Publishing, the same fields.) The project is created by the first publish.

**TestPyPI**: test.pypi.org, the same form with Environment name `testpypi`.

No token is stored anywhere.

## 5. Zenodo

zenodo.org, Log in with GitHub (authorise the Zenodo application; if the organisation `DynamicalSystemsGroup`
restricts third-party applications, grant Zenodo under the organisation's Settings, Third-party access), your
profile menu, GitHub, **Sync now**, then switch **On** for `DynamicalSystemsGroup/hyperbolic-trade-space`. Before the
first release: the first archive is of `v0.1.0`.

## 6. Nothing else

Actions' default workflow permissions stay read-only (Settings, Actions, General, Workflow permissions: Read
repository contents); each job declares what it needs. The label `release-failure` is created by the workflow.

## The details that remain his

### Question 1. You are the only code owner and the author of the release pull request. GitHub does not let a pull request's author approve it, so a required code-owner review would block every release. What stands for the review on `main`?

- **(a) The review rule with you as bypass.** Two rulesets on `main`: one with "Require a pull request" plus one
  required approval and "Require review from Code Owners", bypass list Repository admin ("For pull requests only");
  the other with the status checks, merge method, deletions and force pushes, bypass list empty. You merge by ticking
  the bypass box; the checks still bind, since rules of every ruleset aggregate and the bypass is per ruleset (the
  QC stage confirms that a bypass of the first leaves the second binding). The day a second code owner exists, the
  bypass goes.
- **(b) No required approval; merging restricted to you.** One ruleset: pull request required with 0 approvals, the
  checks, merge only, and "Restrict updates" with bypass Repository admin, so only you can merge into `main`. The
  record of your review is the release issue the pull request closes.
- **(c) Pull requests opened by the driver's own account.** A second GitHub account (a machine user) opens the
  release pull request and you approve it as the code owner; one ruleset with one required approval and code-owner
  review, no bypass. Costs an account, its access and its credentials.

### Question 2. Every merge into `main` is a release. When `dev` carries a new paper pin or a docs correction but no new package version, what does the merge do?

- **(a) Every merge is a version.** The pull request's `admissibility` fails while `v<version>` exists; a paper pin
  or a docs fix reaches the site with the next version (a patch release if nothing else changed).
- **(b) A merge without a new version redeploys the site only.** `admissibility` reports `site-only` when the tag
  exists on an earlier commit and the package files (`src/`, `pyproject.toml`, `uv.lock`) are unchanged since it;
  the run composes and deploys the site and skips the tag, PyPI and the release; the changelog check is skipped. A
  change to the package files with an unchanged version still fails.
- **(c) A separate site dispatch.** Merges stay releases as in (a); a `workflow_dispatch` of `site.yml` with a
  `deploy` input, allowed from `main` only, redeploys the site between releases.

### Question 3. A paper tag publishes a GitHub release, which Zenodo archives with a permanent DOI. Does that publication wait for your approval?

- **(a) No.** The pushed tag is the decision; `paper.yml` publishes when the build and the tests pass. A tag pushed
  in error still mints a DOI.
- **(b) Yes, through the `paper-release` environment.** The `release` job waits for your approval in the run;
  nothing is published or archived until you approve; a tag pushed by an agent waits for you.

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
setting. The declaration is approved first, in the review. A field the runner checks (a ruleset, a required check,
a repository setting) is then changed in one sitting before the merge, so the push run of `controls` after the merge
compares the new declaration with settings already changed and is green. A local-only field (the workflow
permissions, a ruleset's bypass actors) is attested by your local run after the merge. The settings below are the
ones the declaration does not hold.

The governed files (`GOVERNANCE.md`, the secondary rules) each have their own `CODEOWNERS` line naming the three
code owners as the approvers of a change to them, and the `governance-files` push ruleset refuses a push that
touches one of them by anyone but a Repository admin; a pull request that changes a governed file is merged by an
admin.

For the 0.2 governance change, once the declaration is approved, a Repository admin applies the three
runner-checked settings in one sitting before the merge: 1. `main-checks` gains the required check `controls`; 2. the
push ruleset `governance-files` is created (active; the nine governed paths; bypass Repository admin, always); 3.
Settings, General, Pull Requests: "Automatically delete head branches" on. Then the governance pull request is
merged, and no other push to `dev` happens between the settings and the merge. After the merge, the two local-only
settings: 4. `main-review` loses its bypass actor; 5. the workflow permissions become read, approving reviews off.
Then your local run reads `conforming (70 fields)`, and a `--record` run of `scripts/check_repo_settings.py` into the
recorded fixture under `tests/data/` replaces the hand-edited files in a follow-up commit.

Settings, Labels: create `draft` and `small-fix`. The scope-of-work template applies `draft`; a code owner removes it
to turn a draft into an issue. `small-fix` stands in for an issue on a pull request that fixes a typo or a broken link.
The label `release-failure` is created by the Release workflow.

The Tests workflow runs on every pull request into `main` (the required checks), when the Release workflow calls it,
and on dispatch (Actions, Tests, Run workflow), which also runs Windows. A push to `dev` runs lint and the Linux
fast shard only, and so does every pull request into `dev`, a person's or Dependabot's; the full set (fast, slow,
docs) stays on pull requests into `main`. It never runs Windows on a pull request or a push. Its first job,
`controls`, is the settings check; the shards need it. It does not run on a pull request into `dev` (a pull request
may carry a declaration ahead of the live settings); it runs on a push to `dev`, a pull request into `main`, the
release's call and a dispatch.

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
conformance by running the check, fitness by looking and signing the judgement. Before approving, run `uv run python
scripts/release_checks.py gates` on the branch: the Tests workflow's checks, the vocabulary, surface, settings and
branch checks, one line each with a verdict. Merge into `dev`; the repository setting deletes the merged branch, and a
`qc/*` branch or a stale branch the `branches` check names is deleted by a code owner. A dependency
update, Dependabot's pull request into `dev`, has no template and no issue: its steps are the next section.

## Dependency updates

Dependabot (`.github/dependabot.yml`) opens its pull requests against `dev` with the `dependencies` label, weekly:
one pull request per ecosystem (`github-actions`, `uv`) for that week's minor and patch bumps, and a pull request of
its own for each major bump. Its description, the release notes, the commits and the compatibility score, stands in
for the template, and it names no issue; the pull request checks pass it with a notice that quotes its row in
`.github/PR_ADMISSIBILITY.md`. The Tests workflow runs on it as on any pull request into `dev`: lint and the Linux
fast shard. When one arrives:

1. Read the bump: what moved, from which version to which, whether a major moved, and the release notes Dependabot
   quotes (a breaking change named there is read before anything runs).
2. Confirm the Tests workflow ran on the pull request and is green. The workflow runs lint and the fast shard on
   every pull request into `dev`, so a missing run means something else (a conflict with `dev`, a closed or
   retargeted pull request): comment <code>&#64;dependabot rebase</code> and it runs on the bot's push.
3. For a workflow-action bump: the pin is a full commit SHA with the new version in its trailing comment (`uv run
   python scripts/release_checks.py pins` on the branch), and an admin merges it, since the push ruleset
   `governance-files` covers `.github/workflows/*.yml`.
4. For a `uv` bump: `uv.lock` is the only file touched beyond `pyproject.toml`, and `uv lock --check` passes on the
   branch (the fast shard runs it).
5. Merge with a merge commit. The merge check records that a code owner merged it.

When the run is red, the pull request stays open: file the failure as an issue (the test that failed, the bump that
caused it), and either fix it on `dev` and comment <code>&#64;dependabot rebase</code>, or close the pull request with a comment that
names the issue (a closed bump is skipped until the dependency's next release;
<code>&#64;dependabot ignore this major version</code> skips the whole line). A major bump of a runtime dependency (`numpy`, `scipy`, `scikit-learn`) is a
candidate like any other: when it changes behaviour, open a scope-of-work issue for it and deliver the change as a
pull request that closes the issue, with the record `tests/data/api_surface.json` and the changelog following.

## Cutting a release

1. On `dev`: `uv run python scripts/release_checks.py bump 0.2.0 --date <merge day> --changelog final`. It writes
   the version in every place it is written (`pyproject.toml`, `__version__`, `CITATION.cff` with the date, the
   interface contract's manifest and document), refreshes `uv.lock`, and moves the Unreleased entries in
   `CHANGELOG.md` under the new version with the date; commit the files it prints. The bump follows the rule in
   `GOVERNANCE.md` ("Versions"): a patch release leaves the package's public names and signatures (the record
   `tests/data/api_surface.json`) and the governed files untouched; a minor release adds capability, changes those
   names or signatures, or changes a governed file; the changelog entry names what moved the number.
2. Optionally dispatch the Release workflow on `dev` with target `testpypi` (a candidate version such as
   `0.1.0rc1` can be published only once per version). The suite runs first. Install from TestPyPI and try it.
3. Run `uv run python scripts/release_checks.py gates --release` at the head: the Tests workflow's checks, the
   repository's own, and the release admissibility checks (`version`, `tag`, `changelog --final`, `version-kind`,
   `pins`, the paper's mode file) as the pull request will see them, one line each; every line green before the pull
   request opens.
4. Open the pull request from `dev` into `main`, closing a release issue ("Release 0.1.0"). Its checks are the
   three test shards and `admissibility`. `admissibility` refuses the pull request unless the version is new (or
   the merge is site-only, below), the changelog has the entry, the bump matches what changed since the previous
   tag (`scripts/release_checks.py version-kind`), the lock is current and every action is pinned; it also refuses
   while a Release run on `main` is queued or in progress. Stage the site, review it, and record the
   review in the release issue.
5. Merge it (merge commit). One release pull request at a
   time, merged after the previous Release run has ended.
6. Watch the run. On the merge commit it checks the settings against their declaration, checks admissibility again,
   runs the suite, and builds and checks the
   wheel, the sdist and the software bill of materials (CycloneDX, from the lock). It composes the site, creates
   the tag `v<version>` and a draft release whose notes end with the settings check's attestation, and publishes
   to PyPI, the one step that cannot be undone. Last, it deploys the site and publishes the release (archived by
   Zenodo once the repository is switched on there).
7. On failure, read the issue the run opens (label `release-failure`). It names the failed job and step, what the
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

### A dry run

A rehearsal of content on a `qc/` branch is prepared by a throwaway commit on top of the head: `uv run python
scripts/release_checks.py bump <next version> --changelog stub`, committed, `gates --release` green, pushed with
`git push origin HEAD:qc/release`, never merged, and the branch deleted after the run (`git push origin --delete
qc/release`). The next version is the one the rule allows: a patch where neither the package's public names and signatures
nor a governed file changed since the last tag, otherwise the next minor; `version-kind` in `gates --release` says which before the
push. The bump is needed because the `tag` check refuses a head whose version is already tagged once the package files
changed since that tag, and a content branch at a released version is exactly that: the rule doing its job, not a
reason to relax it. The `branches` check names a `qc/*` branch left behind.

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

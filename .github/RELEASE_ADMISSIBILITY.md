# Release admissibility conditions

The merge of a pull request from `dev` into `main` becomes a release only when every condition below holds. Each row
says whether the condition is verified by machine (conformance) or judged by a person (fitness), and what enforces
or records it. The release workflow (`.github/workflows/release.yml`) checks the conformance rows on the pull request
(the required check `admissibility`) and again on the merge commit, and stops before anything is published when one
fails; the fitness condition is a code owner's decision, recorded by name, and no check stands in for it.

| Condition | Kind | Enforced or recorded by |
|---|---|---|
| The repository's settings match their declaration at the merge commit | conformance, machine | the `controls` job, first in the release workflow and in the test workflow, running `scripts/check_repo_settings.py` against [`governance.toml`](governance.toml); no other job runs until it passes; its report is the run summary (the fields marked local-only in the declaration are listed there as not checked on the runner), and the release notes end with `Controls: .github/governance.toml@<hash> checked at <merge commit>: conforming (N fields on the runner; M local-only)` ([`GOVERNANCE.md`](../GOVERNANCE.md)) |
| The release is the merge of a pull request from `dev` into `main`, by a code owner, as a merge commit | conformance, machine | the `main` rulesets declared in [`governance.toml`](governance.toml) (a pull request with a code owner's review, merge commits only, the required checks; the bypass for 0.1 as [`GOVERNANCE.md`](../GOVERNANCE.md) says); the release workflow's merge check (two parents, the second on `dev`) |
| The version in `pyproject.toml` is a release version, its tag `v<version>` is new, and the changelog has an entry for it | conformance, machine | the release workflow's version, tag and changelog checks; the workflow creates the tag on the merge commit, and no workflow starts on a tag |
| A merge with the version already released and `src/`, `pyproject.toml` and `uv.lock` unchanged since its tag redeploys the site only; a change to those files with the version unchanged is refused | conformance, machine | the release workflow's tag check (`site-only` or `taken`) |
| The test suite is green at the merge commit | conformance, machine | the three test shards required on the pull request; the release workflow runs the suite again and stops on failure |
| The lock matches the declaration and the build installs from the lock only | conformance, machine | `uv lock --check`; `uv sync --locked` in the workflow |
| Every workflow action is pinned to a commit, not a tag | conformance, machine | the pin check in the workflow; the update bot moves pins by pull request |
| The release carries a software bill of materials that matches the lock | conformance, machine | generated in the release workflow from the locked resolution and attached to the release; checked against `uv.lock` |
| The paper's mode file is valid for serving | conformance, machine | `scripts/paper_mode.py check --stage served` in the release workflow |
| No pull request in the release has an open admissibility failure | conformance, machine | the pull request checks on `dev` (see [the pull request admissibility conditions](PR_ADMISSIBILITY.md)) |
| Publishing runs only from the merge commit through the release workflow, by trusted publishing, and the files PyPI holds for the version are the files built in that run | conformance, machine | trusted publishing (no tokens; the publisher names `release.yml` and the `pypi` environment, which admits `main` only); the hash check after the upload |
| A failed release is detected, named and cleaned up | conformance, machine | the release workflow's `on-failure` job: the failed job and step in the run summary, `scripts/release_cleanup.py` (removes the tag and the draft before PyPI holds the version, keeps them after), an issue labelled `release-failure`, closed by the next successful run of the version |
| This candidate is the release: it does what its changelog says and is fit to ship | fitness, a code owner | the merge of the pull request, which records who merged and when, and the release issue it closes, which records the review of the staged site; the merger has read the changelog and the review records of the pull requests inside. The `pypi` environment has no required reviewer: the merge is the decision |

How a release is cut, step by step, is in [the code owners' page](../docs/code-owners.md).

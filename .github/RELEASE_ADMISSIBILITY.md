# Release admissibility conditions

A tag on `main` becomes a release only when every condition below holds. Each row says whether the condition is
verified by machine (conformance) or judged by a person (fitness), and what enforces or records it. The release
workflow refuses a tag that fails a conformance condition; the fitness condition is a code owner's decision, recorded
by name, and no check stands in for it.

| Condition | Kind | Enforced or recorded by |
|---|---|---|
| The merge into `main` comes from `dev` only, by a code owner, with `--no-ff`, and carries a version tag `vX.Y.Z` | conformance, machine | branch protection on `main` (pull request required, review from code owners, restricted merge); the release workflow runs only on `v*` tags on `main` |
| The version in `pyproject.toml` equals the tag, follows semantic versioning, and the changelog has an entry for it | conformance, machine | the release workflow's version check; the changelog check |
| The test workflow is green on both platforms at the tagged commit | conformance, machine | the release workflow runs the suite first and stops on failure |
| The lock matches the declaration and the build installs from the lock only | conformance, machine | `uv lock --check`; `uv sync --locked` in the workflow |
| Every workflow action is pinned to a commit, not a tag | conformance, machine | the pin check in the workflow; the update bot moves pins by pull request |
| The release carries a software bill of materials that matches the lock | conformance, machine | generated in the release workflow from the locked resolution and attached to the release; checked against `uv.lock` |
| No pull request in the release has an open admissibility failure | conformance, machine | the pull request checks on `dev` (see [the pull request admissibility conditions](PR_ADMISSIBILITY.md)) |
| Publishing runs only from the tag through the release workflow, after a code owner approves its environment | conformance, machine | trusted publishing (no tokens); the `pypi` environment's required reviewers are the code owners |
| This candidate is the release: it does what its changelog says and is fit to ship | fitness, a code owner | the environment approval, which records who approved and when; the approver has read the changelog and the review records of the pull requests inside |

How a release is cut, step by step, is in [the code owners' page](../docs/code-owners.md).

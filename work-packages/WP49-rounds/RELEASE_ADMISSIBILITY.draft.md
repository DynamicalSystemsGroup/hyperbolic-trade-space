# Release admissibility conditions

A tag on `main` becomes a release only when every condition below holds. Each names the check that enforces it; the
release workflow refuses a tag that fails one, and the last condition is a code owner's decision, recorded by name.

| Condition | Enforced by |
|---|---|
| The merge into `main` comes from `dev` only, by a code owner, with `--no-ff`, and carries a version tag `vX.Y.Z` | branch protection on `main` (pull request required, review from code owners, restricted merge); the release workflow runs only on `v*` tags on `main` |
| The version in `pyproject.toml` equals the tag, follows semantic versioning, and the changelog has an entry for it | the release workflow's version check; the changelog check |
| The test workflow is green on both platforms at the tagged commit | the release workflow runs the suite first and stops on failure |
| The lock matches the declaration and the build installs from the lock only | `uv lock --check`; `uv sync --locked` in the workflow |
| Every workflow action is pinned to a commit, not a tag | the pin check in the workflow; the update bot moves pins by pull request |
| The release carries a software bill of materials that matches the lock | generated in the release workflow from the locked resolution and attached to the release; checked against `uv.lock` |
| No pull request in the release has an open admissibility failure | the pull request checks on `dev` (see [the pull request admissibility conditions](PR_ADMISSIBILITY.md)) |
| Publishing runs only from the tag through the release workflow, after a code owner approves its environment | trusted publishing (no tokens); the `pypi` environment's required reviewers are the code owners |
| A code owner has decided that this candidate is the release | the environment approval, which records who approved and when |

The first eight are conformance and are verified by machine. The last is fitness and is a person's judgement; no
check stands in for it. How a release is cut, step by step, is in [the code owners' page](../docs/code-owners.md).

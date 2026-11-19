# Pull request admissibility conditions

A pull request is reviewed only when every machine row below holds, and merges into `dev` only when every row holds.
Each row says whether the condition is verified by machine (conformance) or judged by a named reviewer who is a code
owner (fitness), and what enforces or records it. The pull request workflow checks the machine rows when a pull
request is opened or edited and on each push; the reviewer's rows are recorded in the review, by name.

| Condition | Kind | Enforced or recorded by |
|---|---|---|
| It names the issue it resolves (`closes #n`), or carries the small-fix label | conformance, machine | the linked-issue check |
| Its description states what changed, what backs it, which tests cover it, and the tools used | conformance, machine | the template's fields present and non-empty |
| Its defaults, the details the scope did not settle, are listed for the reviewer | conformance, machine | the template's defaults field present (it may say none) |
| It does one thing its title says | fitness, a code owner | the reviewer's judgement, recorded in the review (guideline: `CONTRIBUTING.md`, "A pull request delivers against its issue") |
| Its history is readable: each commit builds and passes; no merge of `main` into the branch; no force-push to a shared branch | conformance, machine | the workflow runs the suite on the head; the branch rules refuse force-pushes; a merge-commit check |
| The conformance checks pass: lint, format, lock, tests (among them `tests/test_api_surface.py`: a change to the public surface rewrites `tests/data/api_surface.json`, which the version rule of `GOVERNANCE.md` reads), the vocabulary and residual checks, both platforms | conformance, machine | the test workflow: on a pull request into `dev`, lint and the Linux fast shard; on the push to `dev` that the merge makes, its `controls` job (the settings against their declaration), lint and the Linux fast shard; on the release pull request, the full matrix |
| No commit message names a tool as author or generator | conformance, machine | the attribution check in the test workflow |
| Every conformance item of its issue's good-enough list passes | conformance, machine | the checks the items name, quoted in the review |
| Every fitness item of its issue's good-enough list is validated: it does what the issue intends, reads as intended, renders right | fitness, a code owner | the reviewer looks at the thing and signs the judgement in the review (guideline: `CONTRIBUTING.md`, "Review is against the scope"; `docs/code-owners.md`, "Reviewing a candidate") |
| No gap is left open: each is accepted with a reason, fixed before the merge, or made its own issue | fitness, a code owner | the review's gap list with a disposition per gap (guideline: `CONTRIBUTING.md`, "Review is against the scope") |
| The scope was not widened: a change the issue does not cover went back to the issue as an amendment | fitness, a code owner | the reviewer compares the diff with the issue's blast radius (guideline: `CONTRIBUTING.md`, "A pull request delivers against its issue") |
| It is merged by a code owner who is not its author | conformance, machine | branch protection (review from code owners, no self-approval) and the merge check. While the code owners are one person this row cannot hold and the check passes with a notice; the bypass ends the moment a second code owner is added, by design, and no setting restores it |
| A dependency update, a pull request opened by `dependabot[bot]` against `dev` with the `dependencies` label (`.github/dependabot.yml`), stands in for the first three rows: its description is Dependabot's own (the release notes, the commits, the compatibility score), it names no issue, the test workflow runs on it before the merge, and a code owner merges it (a Repository admin where it touches `.github/workflows/*.yml`, the `governance-files` push ruleset) | conformance, machine | the linked-issue and fields checks, which pass with a notice quoting this row; the test workflow's `pull_request` run into `dev` (lint, the fast shard); the merge check |

A pull request into `paper` (a change to the paper; the route is "Contributing to the paper" on the contributing
page) is read by the same checks with two rows in their `paper` form:

| Condition | Kind | Enforced or recorded by |
|---|---|---|
| Its description's `Paper` section names the section or figure changed, the residual check's result and the build | conformance, machine | the template's `Paper` section present and non-empty, read on a pull request into `paper` only |
| It is merged by a paper approver, a login on the `paper/` line of `CODEOWNERS`, who is not its author | conformance, machine | the merge check on a pull request closed into `paper`; the approvers are two, so the row holds and there is no notice. A code owner who is not on that line does not merge it |

The paper's approvers read the pull request for the argument; the paper workflow runs the build, the tests, the
residual comparison and the key manifest once the merge lands on `paper`.

The template that asks for the fields is [`pull_request_template.md`](pull_request_template.md). What the review
records, and how a reviewer separates the two kinds of items, is on the [contributing page](../CONTRIBUTING.md).

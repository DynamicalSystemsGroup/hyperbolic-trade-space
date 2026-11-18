# WP78 D-8: the inventory's gaps, and the governance-ruleset question

The inventory (amendment 1) is the section "How the repository is organised" of `GOVERNANCE.md`; the split of the
secondary rules into executable and guideline (amendment 4) is its section "The secondary rules" and the
`governed_files` table of `.github/governance.toml`. Below: what the inventory found missing, for his decision,
nothing fixed beyond pointers; then the question of amendment 2. Plain options, no recommendation.

## The split of the secondary rules (amendment 4)

Executable (a script or a test checks it): `.github/CODEOWNERS` (`check_repo_settings.py`, `admissibility.py`),
`.github/governance.toml` (`check_repo_settings.py`, `tests/test_repo_settings.py`), `.github/workflows/*.yml`
(`release_checks.py pins`, the workflow tests), `.github/ISSUE_TEMPLATE/*.yml` and
`.github/pull_request_template.md` (`tests/test_admissibility.py`). Guideline (a named role judges it):
`GOVERNANCE.md` (a code owner at review; its list tested), `.github/ISSUE_ADMISSIBILITY.md` (the code owner who
removes `draft`), `.github/PR_ADMISSIBILITY.md` (the code owner who reviews and merges),
`.github/RELEASE_ADMISSIBILITY.md` (the code owner who merges the release); the machine rows of the three run in
the workflows each names. Five executable, four guideline; `tests/test_repo_settings.py` holds the declaration and
`GOVERNANCE.md` to the same list.

## Gaps found

1. **The default workflow permissions read back `write`, not `read`.** `WP65-design/his-items.md` (section 6) and
   the code owners' page said read; the live value on 2026-11-17 is `default_workflow_permissions = "write"` with
   `can_approve_pull_request_reviews = true` (a workflow could approve a pull request). The declaration encodes the
   live value, as the scope requires. His decision: keep `write`, or set `read` (and `false`) on GitHub after the
   declaration is changed to say so, in that order.
2. **The workflow token cannot read that setting, so it is local-only.** `GET actions/permissions/workflow` needs
   the Administration permission (read), which GitHub never grants to the workflow token; the other endpoints need
   Metadata (always granted), Actions and Pages (declared on the job). The declaration marks the `actions` section
   `checked_on = "local"` with the reason; the `controls` job (`--runner`) lists its two fields as not checked on
   the runner, they leave the exit code alone, and the attestation counts them (`conforming (59 fields on the
   runner; 2 local-only)`); a code owner's local run (`uv run python scripts/check_repo_settings.py`) checks every
   field. Any endpoint that should be readable and is not still exits 2. His decisions: on the setting itself
   (item 1: `write` live, `read` in the design), and whether he wants a local-only field at all, or instead (a) a
   fine-grained token or GitHub App with Administration (read) as a repository secret for that one read, or (b) the
   field out of the declaration, read back by hand like the publishers and Zenodo. The first live `controls` run on
   `dev` (run 44148913732 at 78feb3c1) read every endpoint and found one more field of this kind: GitHub returns a
   ruleset's bypass actors to administrators only, so the workflow token saw `[]` for `main-review` and the field
   is unverifiable on the runner in both directions. Every ruleset's `bypass_actors` now carries a field-level
   `checked_on = "local"`; the runner's verdict is `conforming (55 fields on the runner; 6 local-only)`. The 0.2
   removal of the `main-review` bypass is therefore attested by a code owner's local run of the checker and by the
   ruleset page, not by the runner; the same options (a) and (b) apply to it.
3. **`controls` is not a required status check on `main`.** The `main-checks` ruleset requires the three shards and
   `admissibility`; `controls` gates them in practice (every shard needs it) but is not named. Adding it is a
   ruleset change (a non-goal of WP78) and, by the rule of this package, a change to the declaration first.
4. **Two issue templates have no row and no check.** `bug.yml` and `question.yml` are not read by any check and no
   admissibility document names a condition for a bug report or a question. The scope-of-work template is read by
   `scripts/admissibility.py` and tested.
5. **No pull request template for the paper.** Pull requests into `paper` use the software's template, whose
   sections (`closes #n`, tests) fit code. WP79 scopes the paper's template and its `CODEOWNERS` line.
6. **No row for the settings check on a pull request into `dev`.** `.github/PR_ADMISSIBILITY.md` lists the test
   workflow's checks (row "The conformance checks pass") without the `controls` job, which now runs on every push
   to `dev`; `RELEASE_ADMISSIBILITY.md` has the row.
7. **Judged criteria whose guideline is a page, not a row.** The fitness rows ("It does one thing its title says";
   "This candidate is the release") point at a code owner's judgement; the guideline for the judgement is the prose
   of `CONTRIBUTING.md` ("Review is against the scope") and `docs/code-owners.md` ("Reviewing a candidate",
   "Cutting a release"); the staged-site review of a release has a route map in `WP68-rounds/his-site-review.md`
   that is not a standing guideline. Whether each judged row names its guideline in the row itself is his call.
8. **Settings the checker cannot read** (non-goals, named): the PyPI and TestPyPI pending publishers (no API; the
   TestPyPI rehearsal is their check), Zenodo (off until the first full draft of the paper), the labels `draft`
   and `small-fix` (the code owners' page is their record).
9. **The admissibility documents are three, not two.** `.github/ISSUE_ADMISSIBILITY.md` joins the pull request
   and release documents in the governed set, since its rows are of the same kind.

## The governance-ruleset question (amendment 2)

His words (2026-11-17, 13:35): "its possible we need a branch ruleset specifically for governance". The governed
paths: `.github/CODEOWNERS`, `.github/governance.toml`, `.github/workflows/**`, `GOVERNANCE.md` (and, by amendment
4, the three admissibility documents and the templates). GitHub offers three mechanisms. Today each governed file is
edited like any other: a pull request into `dev`, or a direct commit to `dev` by a code owner (the driver's
day-to-day commits are direct). Whatever he chooses fills the `control` field of each `governed_files` entry.

**(a) A push ruleset restricting file paths.** Settings, Rules, New push ruleset, "Restrict file paths" with the
governed paths. *Binds:* every push to every branch of the repository (and its forks) that touches a listed path;
there is no branch condition on a push ruleset, so a pull request branch is bound too. *Bypass:* the ruleset's
bypass list (a repository role, a team, an app); a push-ruleset bypass is always on, there is no "pull requests
only" mode. Without a bypass actor nobody can change the files from git at all; with Repository admin as bypass, an
admin's pushes go through and nobody else's do. *Cost to direct commits on `dev`:* the driver commits under an
admin login, so with the admin bypass nothing changes in practice and the control is the bypass list; without it,
every change to a governed file is blocked until an admin pushes it. *Checker:* readable; the rulesets endpoint
returns a push ruleset (`target = "push"`, rule `file_path_restriction`, `restricted_file_paths`), and the
declaration gains a fifth ruleset.

**(b) CODEOWNERS path lines.** Lines such as `/.github/governance.toml @mzargham` in `.github/CODEOWNERS`.
*Binds:* only where "Require review from Code Owners" is in force, which today is pull requests into `main`
(`main-review`); a pull request touching a governed path then needs an approval from an owner of that path. On
`dev` nothing changes, since `dev` requires no pull request. *Bypass:* `main-review`'s bypass list (one user,
`mzargham`, on pull requests, for 0.1). *Cost to direct commits on `dev`:* none. *Checker:* the file is in the tree; the
checker reads its `*` line today and the parser (`scripts/admissibility.py`) would be extended to path lines,
which then also name who may approve a change to each governed file (his principle of 13:40, with CODEOWNERS
itself as the record).

**(c) A review rule with file patterns.** In a branch ruleset's "Require a pull request before merging", the
"Required reviewers" setting: a team, a minimum number of approvals and file patterns (the API's
`required_reviewers` parameter, which the declaration already carries as empty on `main-review`). It needs an
organisation team (DynamicalSystemsGroup is an organisation). *Binds:* pull requests into the branch the ruleset
targets whose changes match the patterns. On `dev` it would come with a pull request requirement for every change
to `dev`, since the rule lives inside "Require a pull request". *Bypass:* that ruleset's bypass list; with Repository
admin as bypass, the driver's direct commits continue and the rule binds everyone else. *Cost to direct commits on
`dev`:* without a bypass, they end; with the admin bypass, none for the driver. *Checker:* readable; the parameter
is in the ruleset's detail, and the declaration pins the team, the count and the patterns.

The mechanisms combine: (b) with (a) or (c) makes CODEOWNERS name the approvers and the ruleset enforce the route.
He decides; nothing is set before his word, and the declaration changes first.

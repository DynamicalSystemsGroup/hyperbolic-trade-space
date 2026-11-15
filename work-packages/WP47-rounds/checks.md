# WP47 verification cases (D-7, R-12, R-13)

Each case is a requirement, a method, the evidence and a verdict, so that WP48's readout can cite it. The machine rows
of `.github/ISSUE_ADMISSIBILITY.md`, `.github/PR_ADMISSIBILITY.md` and `.github/RELEASE_ADMISSIBILITY.md` are the
requirements; fitness rows have no workflow (a code owner judges them and the record names who). The workflows read
the event payload as data and run no code from an issue or a pull request. Issue-event workflows run from the default
branch, so a live trial needs the files there; until then the evidence is the script run on payloads and the tests.

Evidence on `wp47`: `uv run pytest tests/test_admissibility.py tests/test_release_checks.py
tests/test_contributing_links.py` and the script runs quoted below; the review record holds their output.

| Case | Requirement (row) | Workflow and trigger | Method | Evidence | Verdict |
|---|---|---|---|---|---|
| VC-1 | A draft's scope, non-goals, blast radius, good, good-enough items (each marked) and open decisions are present and non-empty | `issue-admissibility.yml`; issues opened, edited | `scripts/admissibility.py issue` on a payload; tests per field | a payload without the blast radius and with an unmarked item exits 1 and names both; a full payload exits 0; `test_issue_*` | passes in test; live trial pending the default branch |
| VC-2 | Only a code owner removes `draft`; any other removal is reverted | `draft-label-gate.yml`; issues unlabeled | `label-gate` on a payload, owners read from `.github/CODEOWNERS` | removal by a non-owner exits 1 with the comment text; by an owner exits 0; `test_draft_label_*` | passes in test; live trial pending |
| VC-3 | A pull request names its issue (`closes #n`) or carries `small-fix` | `pr-linked-issue.yml`; pull request opened, edited, labeled, unlabeled | `linked-issue` | `see #3` exits 1; `closes #3`, `Fixes #3`, `resolved org/repo#9` and the label exit 0; `test_pull_request_naming_*` | passes in test; live trial pending |
| VC-4 | A pull request's what changed, what backs it, tests, defaults and tools used are present and non-empty (none is a valid answer) | `pr-fields.yml`; pull request opened, edited, synchronize | `pr-fields` | a body with one section exits 1 naming the other four; the template's own empty comments count as empty; `test_pull_request_with_an_empty_field_*` | passes in test; live trial pending |
| VC-5 | Merged into `dev` by a code owner who is not the author; with one code owner the check passes with a notice quoting the row | `merge-by-code-owner.yml`; pull request closed into `dev`, merged | `merge` | one owner: exit 0 and the notice; two owners, merger is the author or a stranger: exit 1; unmerged or other base: ignored; `test_merge_*` | passes in test; the setting itself (no self-approval) is on the checklist |
| VC-6 | The tag equals the package version; the changelog has the entry; the lock is current | `release.yml`, job `check`; tag push, or dispatch with a `tag` input | `check_release_version.py`, `release_checks.py changelog`, `uv lock --check` | tag `v0.1.0` against version 0.0.1 exits 1 with the message; `changelog --final` exits 1 until the entry exists; `test_release_version.py`, `test_a_final_release_*` | passes in test; the dry-run dispatch shows it in the log once on GitHub |
| VC-7 | Every action is pinned to a commit | `release.yml`, job `check` (and `tests/test_release_checks.py` on every run of the suite) | `release_checks.py pins` | exit 0 on the repository; a tag-pinned action exits 1 | passes |
| VC-8 | The release carries a software bill of materials that names every package `uv.lock` names (R-13) | `release.yml`, job `build`; attached to the GitHub release and to the dry run's artifacts | `uv export --locked --format cyclonedx1.5 --all-groups` then `release_checks.py sbom` | 194 locked packages: 193 components plus the root component, all named at their locked versions; a bill missing a package or a version exits 1 | passes locally; the artifact appears on the first dry-run dispatch |

Not covered by a workflow: the suite on both platforms and the attribution grep (the test workflow), the merge
form `--no-ff` from `dev` and the fitness rows (a code owner's decision), the environment approval for publishing
(the `pypi` environment's required approval, a setting on the checklist).

The default branch point: `issues` and `pull_request_target` workflows take their definition from the default branch.
If the default branch is `main`, the five admissibility workflows begin to act when the release merge lands on `main`.

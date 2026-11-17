# WP78 — Scope of work: governance as executable (the release rules declared, checked first, attested)

| | |
|---|---|
| **Status** | DRAFT, approved by the driver as his proxy under the mandate; his words of 2026-11-17 in `WP64-decisions.md` ("Governance as executable") are the content |
| **Supervisor (accountable)** | mzargham |
| **Repository** | `DynamicalSystemsGroup/tradespace`; `dev` after WP77 lands; part of the 0.1 release |
| **Approval record** | The driver's approval under his mandate, quoted in `WP64-decisions.md` |
| **Acceptance record** | The driver's verification; the first run of the `controls` job green on `dev`; the 0.1 release notes carrying the attestation; his read |

## Purpose

The repository's release rules exist today as settings on GitHub and as prose (`WP65-design/his-items.md`,
`docs/code-owners.md`); their read-back is the driver running API calls by hand. His words: "the code governance rules
specified as executables and the repo configuration conformance checked"; "a GOVERNANCE.md file and a pointer to the
executable specifications and the conformance checks"; "a first step that checks the controls are in place as
specified before proceeding with the rest of the checks"; the metacheck shows "that the repo contents includes a
specification of its own release rules and that those release rules were in effect as of the release".

## Goals

- G1. The expected configuration declared in one file in the tree (the declaration): the four rulesets (`main-review`,
  `main-checks`, `dev`, `paper`) with their targets, rules, parameters and bypass actors; the four environments
  (`github-pages`, `pypi`, `testpypi`, `paper-release`) with reviewers, self-review, admin bypass and branch or tag
  policies; Pages built by the workflow; the code owners of `.github/CODEOWNERS` and their minimum access (write);
  the default workflow permissions (read). The values are the ones read back on 2026-11-17 (`WP68-rounds/record.md`, G7).
- G2. A checker, `scripts/check_repo_settings.py`, that reads the live configuration through the GitHub API, compares
  it with the declaration field by field, prints every difference and exits non-zero on any; a `--report` option
  writes the comparison as Markdown for a job summary.
- G3. The checker tested on recorded API responses (fixtures), without network: a conforming set passes; each kind of
  drift (a missing check, an extra bypass actor, a changed reviewer, a policy on the wrong branch, a code owner
  without write access) is reported by name.
- G4. `GOVERNANCE.md` at the repository root: what the release rules are in one page, where they are declared (G1),
  how they are checked (G2) and where the admissibility rows are; the code-owners page, `CONTRIBUTING.md`,
  `README.md` and `.github/RELEASE_ADMISSIBILITY.md` point at it instead of describing settings in prose.
- G5. A first job `controls` in `test.yml` and `release.yml` that runs the checker; every other job `needs` it, so no
  test, build or publish runs while the configuration differs from its declaration. Its summary carries the report.
- G6. Attestation: the release run's summary and the GitHub release notes name the merge commit, the declaration's
  path and hash at that commit, and the `controls` result, so a release states that its own rules were in effect
  when it was made.
- G7. The WP68 record's G7 read-back becomes the checker's output at the head, and `his-items.md` says the settings
  are checked by the checker.

## Non-goals

No code changes a setting (the checker reads only); no check of the PyPI and TestPyPI pending publishers (no API
exists; the TestPyPI rehearsal is their check) or of Zenodo; no new dependency (the standard library and the `gh`
CLI, present locally and on the runners); no change to the rulesets themselves (the bypass on `main-review` is
removed after 0.1 by a change to the declaration first, then to the setting).

## Deliverables

| ID | Deliverable | Serves |
|---|---|---|
| D-1 | The declaration file | G1 |
| D-2 | `scripts/check_repo_settings.py` | G2 |
| D-3 | `tests/test_repo_settings.py` and its fixtures | G3 |
| D-4 | `GOVERNANCE.md` and the pointers in the four documents | G4 |
| D-5 | The `controls` job in both workflows, with `needs` on every other job | G5 |
| D-6 | The attestation lines in the release run's summary and `scripts/release_checks.py`'s notes | G6 |
| D-7 | The record and `his-items.md` updated | G7 |

## Requirements and checks

| ID | Requirement | Check |
|---|---|---|
| R-1 | The checker passes against the live repository on 2026-11-17's settings | `uv run python scripts/check_repo_settings.py` exits 0 locally |
| R-2 | Every declared field is compared; a field the workflow token cannot read is reported as unreadable and fails the job, never skipped silently | the fixture tests; the first `controls` run on a push to `dev` |
| R-3 | The job is first: no other job in either workflow starts without it | `needs:` on every other job; the run's graph |
| R-4 | The declaration is the one source: no document states a setting value the declaration does not hold | `grep` of the four documents for ruleset and environment names finds pointers, not values |
| R-5 | No attribution line; lint, format, the fast suite and the docs build green | the usual checks |

## Definition of good

A reader of `GOVERNANCE.md` finds the rules, the file that declares them and the job that enforced them on the
release they are reading, and a drift in any setting stops CI with the field named.

## Definition of good enough

G1 to G5 and G7 done and green on `dev`; G6 present in the workflow and seen in the `qc/release` dry run's summary.

## Definition of done

Good enough met; the 0.1 release notes carry the attestation; his read of `GOVERNANCE.md`.

## Open decisions

None: his words fix the scope. The workflow token's visibility of each endpoint is a fact the first run establishes,
not a decision.

## Agent's defaults

- The declaration lives at `.github/governance.toml` (beside `CODEOWNERS` and the admissibility rows) (default).
- The checker calls `gh api` by subprocess, so authentication is the user's locally and the workflow token on the
  runners; the job's permissions are `contents: read` plus what the endpoints need, declared on the job (default).
- The job is named `controls` and its report is the step summary (default).
- The attestation line's form: `Controls: <path>@<short hash> checked at <merge sha>: conforming` (default).
- The unit starts after WP77 lands and rebases onto its head (default).

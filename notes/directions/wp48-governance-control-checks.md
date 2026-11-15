# WP48 D-3: readout. Governance checks as verification cases, drafted against this repository

Written 2026-11-14 against dev `070cc54` (the worktree base) and the repository's GitHub settings read the same day at
about 15:15 EST with `gh api` (read-only GET requests on `DynamicalSystemsGroup/hyperbolic-trade-space`). Sources are
in `wiki-notes.md` (D-1) and `governance-checks-notes.md` (D-2); their commits and read dates apply here. Nothing in
this readout was run through the SysML engine: the model text below is drafted, not parsed. The repository state below
was read, not assumed. The release workflow of WP47 (`.github/workflows/release.yml`, with `CODEOWNERS`, templates,
`CONTRIBUTING.md`, `SECURITY.md`) is on branch `wp47` at `34c7847`, not on dev, so "today" below means dev plus
GitHub's live settings, and a line says where WP47 changes it.

## 1. What "verification case" means here

The supervisor's phrase has a ready meaning in this repository: SysML v2 `verification def`, as section 5 of
`examples/adcs/model_v2/cubesat.sysml` already uses (lines 1033 to 1066: `subject`, `objective { verify requirement
... }`), run through the `opensysml` client that `pyproject.toml` already pins in the `case` group. A governance check is
a verification case when it has four named parts:

| Part | In SysML v2 | In the governance-checks repository |
|---|---|---|
| Requirement | `requirement def` with `subject`, `assume constraint`, `require constraint` | the same, 35 of them (D-2) |
| Method | the `verification def`'s `objective` (`verify requirement`), and the sensor that reads each fact | `sense.py`, one sensor per check; no `verification def` |
| Evidence | facts bound into the model, stored with the run | `results.json`, `summary.md` as a job artifact |
| Verdict | `verify_satisfaction()`: holds, violated, undecided | the same, mapped to pass, fail, unreadable |

Two shapes, shown for each drafted check:

- **Shape S (SysML v2 first).** Requirement and `verification def` in a model file beside the case model; a small sensor
  script writes the facts as JSON; the engine returns the verdict; the workflow keeps the JSON and the table.
- **Shape R (claims register fallback).** A row in `claims_register.toml` whose fragment is the sentence the docs say
  and whose backing is the check's script. The register's backing types today are `lemma`, `test`, `gen`, `func`,
  `file`, `bib`, `glossary`, `reading` (header of `claims_register.toml`); a run of a workflow is none of them, so
  Shape R needs one new backing type (for example `check:`), an amendment to `claims-review.md`, and its verdict is
  pass or fail of a test, with no "unreadable".

## 2. Three checks, drafted

The three differ on purpose: one reads GitHub settings, one reads a release, one reads repository files.

### Check 1. The default branch keeps its history (wiki SOP-history-protection)

- **Requirement.** `main` blocks force pushes and deletion.
- **Method.** `gh api repos/{repo}/rules/branches/main` includes `non_fast_forward` and `deletion` (or classic
  protection allows neither). Needs Metadata: read, which the workflow's own token has.
- **Evidence.** Two booleans, `forcePushBlocked` and `deletionBlocked`, with the response's timestamp and the commit.
- **Verdict.** Pass if both; fail if read and either is false; unreadable if the call fails.
- **This repository today: fails.** `rules/branches/main` returned `[]` and `branches/main/protection` returned 404, read
  2026-11-14. No WP47 file changes it: it is a GitHub setting the supervisor makes (WP47's checklist).

Shape S:

```sysml
package RepoGovernance {
    part def Repository {
        attribute forcePushBlocked : ScalarValues::Boolean;
        attribute deletionBlocked : ScalarValues::Boolean;
    }
    requirement def NoForcePush {
        subject repo : Repository;
        require constraint { repo.forcePushBlocked }
    }
    requirement def NoDeletion {
        subject repo : Repository;
        require constraint { repo.deletionBlocked }
    }
    verification def ReleaseGate {
        subject repo : Repository;
        objective {
            verify requirement noForcePush : NoForcePush;
            verify requirement noDeletion : NoDeletion;
        }
    }
}
```

Shape R: a claim whose fragment is a sentence in `SECURITY.md` or the maintainers' page, such as "the default branch
cannot be force-pushed or deleted", with `backing = ["check:scripts/governance/history.py"]` (the new type) and the
verdict a test of the script against a recorded response.

### Check 2. The release carries an SBOM and cannot be changed (wiki SOP-release-integrity, automated half)

- **Requirement.** Each release has an asset matching `*.spdx.json`, `*.spdx`, `*.cdx.json` or `*bom*.json`, and is
  immutable.
- **Method.** Two forms. After publishing: `gh api repos/{repo}/releases/latest` assets and `immutable` (the wiki's
  form). Before publishing: the workflow checks the build output it is about to upload for the same name pattern, so
  the gate can stop a release; the wiki's form cannot, it can only report.
- **Evidence.** Asset names, the `immutable` flag, the tag.
- **Verdict.** Pass if both hold; fail if read and not; unreadable if the call fails; not applicable before a release.
- **This repository today: not applicable, and would fail at the first release as built.** `releases/latest` returned
  404 and there are no tags (read 2026-11-14); no workflow step on dev or on `wp47` generates an SBOM (searched
  `cyclonedx`, `spdx`, `sbom` outside docs and work-packages: one hit, `paper/paper.ipynb`, not a workflow). Adding the
  step is a change to WP47's release workflow, which WP48's scope excludes; the readout only reports it.

Shape S differs from Check 1 in one place: the requirement carries an `assume constraint { repo.hasRelease }` so a
repository without a release is "not applicable" rather than failing, as governance-checks does for `stableRelease`.

### Check 3. Workflows start read-only and name their dependencies exactly (wiki SOP-workflow-least-privilege, plus one check the wiki lacks)

- **Requirement.** (a) The Actions default token is read-only; (b) each workflow declares `permissions:` and each
  `uses:` names a commit SHA. (a) is the wiki's automated check; (b) is the wiki's attested "workflows-hardened" made
  checkable, and the SHA rule is governance-checks's own practice (its `check.yml` pins every action to a SHA, D-2).
- **Method.** (a) `gh api repos/{repo}/actions/permissions/workflow`, `default_workflow_permissions == read`, needs
  Administration: read, so the supervisor's token, not the workflow's. (b) A script parses `.github/workflows/*.yml` and
  counts workflows without a top-level `permissions:` and `uses:` lines not at a 40-character SHA; needs no token and can
  run on every pull request.
- **Evidence.** The setting's value; the counts and the file names.
- **Verdict.** Pass if the setting is `read` and both counts are zero.
- **This repository today: fails both.** `default_workflow_permissions` is `write` and
  `can_approve_pull_request_reviews` is true (read 2026-11-14). `test.yml` has no `permissions:` block; `pages.yml` has
  job-level blocks only; all 12 `uses:` lines across the two files are version tags (`@v4`, `@v5`), none a SHA
  (`grep` on dev `070cc54`). WP47's `release.yml` is on `wp47` and was not read for this check.

Shape R suits (b) well: the claim "every workflow pins its actions to a SHA" is a statement about files, backed by the
script's own test, exactly like the register's `func:` and `test:` backings; (a) is not a statement about files and
fits only as evidence from a run.

## 3. The repository against the rest of the wiki

Read 2026-11-14. "WP47" means a file present on branch `wp47`, not on dev.

| Wiki check | Today | Note |
|---|---|---|
| Dependabot alerts on | passes | `vulnerability-alerts` returned 204 |
| Push protection | fails | `secret_scanning_push_protection` is `disabled` |
| Code scanning | not configured | not read through the code-scanning endpoints; no workflow runs one |
| Private vulnerability reporting | fails | `{"enabled": false}` |
| Security policy | WP47 | `SECURITY.md` is on `wp47` only |
| CODEOWNERS present and valid | WP47 | `.github/CODEOWNERS` on `wp47` only; `codeowners/errors` returned 404 today |
| Contribution guide | passes (GitHub) | `community/profile` lists `contributing`; WP47 rewrites the file |
| README | passes | `community/profile` lists `readme` |
| Licence | MIT in the file | `license` is null in the repository metadata, which the wiki's check reads: it would fail until GitHub detects the file (the `LICENSE` on dev reads "MIT License"; `main` lacks it or it is not recognised) |
| Semantic-version tags | not applicable | no releases; `pyproject.toml` version is 0.0.1 |
| Review required, status checks required | fails | the ruleset list is empty (Check 1) |
| Lock file | passes in files | `uv.lock` is committed, holds 739 `sha256` hashes over 178 locked packages, and the test workflow runs `uv lock --check` and `uv sync --locked`; the wiki does not ask for this (D-1) |
| Signed commits | not checked | 1868 commits on dev, every one reports signature status `N` (none); the wiki does not ask for this |
| Organisation checks (owners, 2FA, base permission, 5 rows) | not applicable | this repository is in an organisation the wiki's checks do not govern |

## 4. Proposal

Costs are sizes of work, not hours, and are my estimates from the files read, not measurements.

| Item | Cost | Where it runs |
|---|---|---|
| Check 1, history protection | small: two facts, one `gh api` call | release workflow, before publishing |
| Check 3(b), workflow files | small: parse YAML, no token | every pull request and the release workflow |
| Check 3(a), default token read-only | small to read; the setting is the supervisor's to change | scheduled run with the supervisor's token, or the release workflow if the token is stored as a secret |
| Check 2, SBOM and immutable release | medium: the workflow must first generate an SBOM and the supervisor must enable immutable releases; the check is small | release workflow, before publishing (build output) and after (release) |
| The engine and model for all of the above | medium once, small per check after: one `repo_governance.sysml`, one sensor script, the existing `opensysml` pin | the same job |
| Baseline-regression exit | small: governance-checks's logic, 14 lines | so known failures stay visible without turning the release red |

The wiki's own unreadable verdict matters most here: Checks 1 and 3(a) need a token the release workflow does not
normally carry, and the three-way verdict lets the gate run without it and say what it could not read.

### Open decisions, plain options (one at a time)

**Q1. In what form is a governance check written?**

- A. SysML v2: requirement and verification def in a model file, run by the engine already installed.
- B. Claims register: a row per check with a new `check:` backing, a script as the test.
- C. Both: the requirement in SysML v2, and a register row for each that quotes the sentence the docs say.

**Q2. Which checks does the first release control carry?**

- A. Checks 1 and 3(b) only: they need no token and no new release step.
- B. Checks 1, 3(a), 3(b): adds the default-token setting, run with the supervisor's token on a schedule.
- C. All three drafted: adds the SBOM and immutable release, which first needs a change to the release workflow.

**Q3. When does it run?**

- A. In the release workflow, before publishing; a failure stops the release.
- B. On a schedule, reporting only; a failure opens nothing and stops nothing.
- C. In the release workflow as a report, with a recorded baseline, stopping a release only when a passing check
  starts to fail.

## 5. What the paper may say now, may not, and what the next release builds

- **May say now (backed by this readout's read):** the project's release process is intended to carry governance checks
  taken from a public registry of policies, expressed as SysML v2 requirements and verification definitions, the form
  the case model already uses. The wiki and the checking repository exist and were read at the commits named.
- **May not say:** that any governance check runs, that the repository meets the wiki's policies, or that releases are
  attested or signed. Today at least five of the wiki's checks fail (history, review, default token, push protection,
  private reporting) and nothing runs any of them.
- **The next release builds:** whichever of Q1 to Q3 the supervisor picks: the model file, the sensor scripts, the
  workflow step, a recorded baseline, and the settings changes only he can make (branch ruleset, push protection,
  private reporting, default token, immutable releases).

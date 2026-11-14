# WP48 spike, first pass (research agent, Sonnet, 2026-11-14; as returned, paraphrase of pages read through a summarising fetch; thresholds to spot-check)

Research spike report, read 2026-11-14. Fetches went through WebFetch, which summarises pages with a small model, so wording is paraphrase and thresholds should be spot-checked before they are relied on. Raw file URLs (raw.githubusercontent.com ... /main/) returned 404; github.com/.../blob/HEAD/... worked. I did not read the individual SOP pages for archive-notice, contributing, governance-roles-named, maintainers-match, org-base-permission, org-few-owners, org-two-factor or project-files. Those rows come from the Policies page only. I did not fetch the 8 Source-* pages (c_scrm, cisa, dodcio, iso12207, nist, ofac, openssf, ssdf), only their names.

## 1. Wiki: https://github.com/Open-MBEE/repo-registry/wiki

**Home** states that it is a PROVISIONAL review pack for OpenMBEE maintainers, rendered from the repo-registry model at commit 858cf1f. It covers 182 repositories and 22 policies, and says nothing is in effect and no repository is checked. Change proposals go by pull request to the model file, not the wiki.

Pages: Home, Taxonomy, Repositories, Policies, Sources, 22 SOP-* pages, and 8 Source-* pages. The Policies page lists the policy-to-SOP mapping (below).

Where a page defines a pass condition, I give it. Pages are at `https://github.com/Open-MBEE/repo-registry/wiki/<name>`. Check types are "automated" (read from the GitHub API) or "attested" (a human-maintained `ATTESTATIONS.yaml` entry).

- **SOP-release-integrity** (graduated tools): each release carries an SBOM, signed artifacts with build provenance, and no built executables in source. Automated: the latest release has an SBOM asset matching `*.spdx.json`, `*.spdx`, `*.cdx.json` or `*bom*.json`, and `immutable` is true. Attested: SLSA Build Level 3 provenance (GitHub Actions, hosted runners, reusable workflow, artifact attestations), plus an `ATTESTATIONS.yaml` entry for the current release last changed by a code owner. Cites CISA, NIST 800-53 SR-4 and SA-10, OpenSSF, NIST 800-218 PS.2 and PS.3.
- **SOP-dependency-management**: turn on Dependabot alerts, publish a dependency policy, and pin direct dependencies of provided services to exact versions. Automated: the `vulnerability-alerts` endpoint returns 204, which needs Administration: read. Attested: the policy is published and followed, and service pins are exact.
- **SOP-history-protection**: block force pushes and deletion on the default branch. Passes if `allow_force_pushes.enabled == false` (or a ruleset has `non_fast_forward`) and `allow_deletions.enabled == false` (or a ruleset has `deletion`).
- **SOP-change-review** (high tier): at least one code-owner approval and passing status checks before merge. Passes if `required_approving_review_count >= 1`, `require_code_owner_reviews` is on, and required status checks are set.
- **SOP-codeowners**: a CODEOWNERS file at `.github/CODEOWNERS`, `CODEOWNERS` or `docs/CODEOWNERS`. "present" needs HTTP 200 and Contents: read. "valid" needs an empty `errors` list from the GitHub codeowners errors endpoint.
- **SOP-verified-code-owners** (high tier): each code owner verified out of band by an org owner within 12 months. Each CODEOWNERS entry must appear in `data/maintainers.yaml` with a verification date less than 12 months old.
- **SOP-license-by-type**: a single root LICENSE from an accepted list per content type (Apache-2.0 or MIT for tools, CC-BY-4.0 for media, Apache-2.0 for governance, and so on). The check reads the SPDX ID that GitHub detects. It fails if the ID is missing, NOASSERTION or not allowed, unless an exception is recorded in `data/deviations.yaml`.
- **SOP-secret-protection**: push protection on. The check reads `secret_scanning_push_protection` and needs Administration: read.
- **SOP-static-analysis**: code scanning on pull requests and the default branch, with critical findings fixed in 14 days. Automated: code scanning is configured (default setup or analyses exist) and no open critical alert is older than 14 days.
- **SOP-workflow-least-privilege**: the Actions default token is read-only, and each job requests minimal `permissions:`. Automated: default workflow permission is read. Attested: no untrusted text run as commands, and minimal job permissions.
- **SOP-vulnerability-remediation**: critical in 14 days, medium and high in 60 days. Automated: no open critical Dependabot alert older than 14 days, no open high or medium alert older than 60 days, and no open code-scanning alert of medium or higher older than 60 days. Attested: coordinated releases.
- **SOP-security-policy**: SECURITY.md plus private vulnerability reporting. Automated: the policy is present and private reporting is on. Attested: disclosure followed.
- **SOP-semantic-versioning** (from 1.0): tags are vMAJOR.MINOR.PATCH. Automated: every non-draft release tag from the last 12 months matches. Attested: a stable-release policy for graduated tools.
- **SOP-security-design** (high tier): a short, current security-controls document. Attestation only.
- **From the Policies page only** (https://github.com/Open-MBEE/repo-registry/wiki/Policies):
  - archive-notice: README carries an end-of-support notice and fork pointers.
  - contributing: a guide exists and requires tests with code.
  - org-few-owners: 2 or 3 org owners.
  - governance-roles-named: governance holders' org membership is public.
  - org-base-permission: default member permission is read.
  - org-two-factor: 2FA required org-wide.
  - maintainers-match: `data/maintainers.yaml` agrees with CODEOWNERS.
  - project-files: README exists.

**Not on the wiki.** I found no page asking for signed commits or tags, branch protection beyond the history and review pages above, a lock-file check, or an OpenSSF Scorecard run. "Signed" appears only for release artifacts with provenance, under release-integrity. Lock files appear only indirectly, as the "exact pins for service projects" attestation.

## 2. https://github.com/Open-MBEE/governance-checks

**Purpose** (README): measures Open-MBEE repositories against the repo-registry policies, as a stopgap until the registry reports compliance itself.

**Pipeline** (README):
1. `model/governance.sysml` is hand-written. It has 34 `requirement def`s in 17 policy packages, each with a `subject repo : Repository`, an `assume constraint` giving when it applies, and a `require constraint` giving the test. The README says it also holds the name patterns the sensors use.
2. `model.py` generates `model/repositories.sysml` from `repos.yaml`. CI fails if the committed file is stale (`model.py --check`).
3. `sense.py` reads facts via `gh api` and GraphQL, returning counts, flags, strings and ages in days, never verdicts. It uses endpoints such as `repos/{full}/rules/branches/{branch}`, `branches/{branch}/protection`, `releases/latest`, `code-scanning/alerts` and `dependabot/alerts`. Unreadable facts are omitted and reported as unreadable.
4. `check.py` uses the `opensysml` client to start a sysml-grpc service at a pinned release, import the facts, and call `verify_satisfaction()`. Verdicts `holds`, `violated` and `undecided` map to pass, fail and unreadable. The final statuses are pass, fail, exception, unreadable, attested/unattested, n/a and unimplemented.
5. Outputs: `results.json`, `summary.md` and a table in the job summary. `baseline.json` holds the accepted state. The exit code is 1 only on a regression against the baseline or a construction error.

**Inputs:**
- `repos.yaml`: repositories with type and stage, evidence links (`attest`), and the OpenSysML pin.
- `registry.ref`: the pinned repo-registry commit.
- A checkout of repo-registry, passed as `--registry`.
- `GH_TOKEN` from the `GOVERNANCE_TOKEN` secret, with read on Administration, Code scanning, Dependabot, Metadata and Contents.
- CLI options: `--only`, `--json`, `--summary`, `--baseline`, `--update-baseline`.

**Run form** (`.github/workflows/check.yml`, workflow "governance"):
- Triggers: Mondays 06:17 UTC, manual dispatch, any pull request, and pushes to `develop` and `main`.
- Jobs: `unit` (pytest), then `measure`.
- Permissions: top-level none, `contents: read` per job.
- Actions are pinned to SHAs, and checkout uses `persist-credentials: false`.
- Pull requests fall back to the default `github.token`.
- The workflow is not reusable: there is no `workflow_call` and no composite action. Reuse would mean copying or forking it.

**Layout:**
- `.github/workflows/check.yml`
- `model/` (`governance.sysml`, `repositories.sysml`)
- `tests/` (with `fixtures/registry/`)
- `check.py`, `sense.py`, `model.py`, `common.py`
- `repos.yaml`, `baseline.json`, `requirements.txt`
- `CONTRIBUTING.md`, `SECURITY.md`, `LICENSE`, `README.md`

**Licence:** Apache-2.0 (https://github.com/Open-MBEE/governance-checks/blob/HEAD/LICENSE). The copyright line is an unfilled template. Apache-2.0 allows reuse, modification and redistribution of the scripts, model and workflow, provided the licence text, a notice of changes and the NOTICE contents (if any) are kept. I did not check for a NOTICE file.

**Reusable as code:**
- The pattern of one sensor per fact.
- The `sense.py` endpoint recipes.
- The requirement-per-check model.
- The baseline-regression exit logic.

All of these are tied to Open-MBEE's repo-registry data layout and to `opensysml` (a pinned external gRPC service), so they are not drop-in for a single-repo release gate.

**"Verification cases":** the phrase "verification case" does not appear in what I read (README, governance.sysml, check.py). The SysML v2 `verification def` / `verify` constructs were not seen either. I could not read `sense.py`'s full text, `model.py` or `common.py`. The SysML v2 idea of "does the model satisfy the requirement" shows up as OpenSysML's `verify_satisfaction()`, applied to `requirement def`s with `assume constraint` and `require constraint`. The README calls its unit tests (requirement-to-policy matching, tier match, licence-list match), the staleness check and the baseline regression "verification" in the plain English sense only.

## 3. A governance check as a verification case

A SysML v2 verification case has four parts: the requirement it verifies, the method, the evidence collected, and a verdict. governance-checks already has the requirement and verdict halves. It has a `require constraint`, and `holds`/`violated`/`undecided` verdicts from `verify_satisfaction`. Its sensors are the evidence step. Taking the wiki's release-integrity and history-protection pages as the source, a concrete case for the maintainer's release process is as follows.

- **Requirement:** every release of the package ships an SBOM and is built with provenance (SOP-release-integrity: SBOM asset matching `*.cdx.json` or `*bom*.json`, `immutable == true`).
- **Method:** inspection by script, run by the release workflow after the release is drafted. The script runs `gh api repos/DynamicalSystemsGroup/hyperbolic-trade-space/releases/latest` and `gh api .../rules/branches/main` (a pattern taken from `sense.py`).
- **Evidence:** a JSON file attached to the workflow run, recording the observed facts: asset names, the `immutable` flag, and whether the default branch blocks force pushes and deletion (`non_fast_forward` and `deletion` in the rules), each with a timestamp and the release tag.
- **Verdict:** pass if an asset name matches the SBOM glob and `immutable` is true and both branch rules are present. Fail if a fact was read and does not match. Unreadable if the token cannot read the endpoint.

A workflow could produce this today with `gh api` and `jq`, with no SysML tooling. If the maintainer later wants the SysML form, `verification def` bound to the same requirement could take the JSON as its evidence. That route would need `opensysml`, which governance-checks pins, and I have not checked its availability or licence.

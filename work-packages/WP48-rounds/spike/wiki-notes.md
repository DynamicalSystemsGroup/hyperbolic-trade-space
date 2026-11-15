# WP48 D-1: the Open-MBEE repo-registry wiki, read page by page

Read 2026-11-14 from a full clone of the wiki's git repository, not through a summarising fetch:
`https://github.com/Open-MBEE/repo-registry.wiki.git` at commit `cde230c5a56b011a437c22f6befa0e62d5d9d0e9`
(2026-10-18). Every page is at `https://github.com/Open-MBEE/repo-registry/wiki/<name>`. The pages quoted here were
read in full; the eight `Source-*` pages (c_scrm, cisa, dodcio, iso12207, nist, ofac, openssf, ssdf) were read only for
the clause identifiers each SOP cites, not for their content, and `Repositories` and `Taxonomy` were read for
structure only. This supersedes the first pass (`first-pass.md`), whose figures were paraphrase.

## What the wiki is

`Home` (https://github.com/Open-MBEE/repo-registry/wiki/Home): a PROVISIONAL review pack for the OpenMBEE maintainers,
rendered by `scripts/wiki.py` from repo-registry commit `858cf1f` (the sidebar names it). It says nothing in it is in
effect yet and no repository is checked. It covers 182 repositories (`Repositories`) and 22 policies (`Policies`). A
repository has a type (tool, media, research, governance), a stage (sandbox, incubating, graduated, archived) and from
those a tier (high, medium, low, none); a policy is in effect for the kinds its rule selects (`Taxonomy`, `Policies`).
Change proposals are pull requests to the model files in the registry, never wiki edits.

Each policy has an SOP page with the same four parts: set-up steps; **automated checks** (one line each, the GitHub
API call and the pass condition, the token permission it needs; "a check it can't read shows as yellow, never as off");
**attested checks** (a human claim recorded in `ATTESTATIONS.yaml`, valid only for the named release and only if the
last change to the file was committed by a code owner); and "Why", the cited clauses (CISA, NIST SP 800-53, OpenSSF
baseline, DoD CIO OSS memo, NIST SP 800-218, ISO 12207, NIST SP 800-161).

A transferable idea, independent of Open-MBEE's organisation: every check is stated as a pass condition over an API
fact, with a third answer, unreadable, beside pass and fail, and every judgement that no API can read is an attestation
tied to one release.

## The 22 policies, with what each requires

Applicability below is for a graduated tool (the high tier), the bar a released package would be held to. "A" is
automated, "T" attested.

| SOP page (policy) | What it requires | Pass condition as the page states it |
|---|---|---|
| `SOP-release-integrity` (Trustworthy releases) | Each release carries an SBOM, signed artifacts with build provenance, immutable releases, no built executables in source | A: latest release has an asset like `*.spdx.json`, `*.spdx`, `*.cdx.json` or `*bom*.json`; A: `releases/latest` has `immutable == true`. T: signed with SLSA Build Level 3 provenance (GitHub-hosted runners, reusable workflow, artifact attestations); T: no built executables |
| `SOP-history-protection` (Keep the history) | Default branch blocks force pushes and deletion | A: `branches/{b}/protection` has `allow_force_pushes.enabled == false` or `rules/branches/{b}` includes `non_fast_forward`; A: `allow_deletions.enabled == false` or the rules include `deletion`. Squash merging is stated fine |
| `SOP-change-review` (Reviewed changes) | High tier: a pull request, at least one approval, code-owner review, passing status checks | A: `required_approving_review_count >= 1` and `require_code_owner_reviews`, or the same in a `pull_request` rule; A: `required_status_checks` set or a `required_status_checks` rule |
| `SOP-codeowners` (Named owners) | A CODEOWNERS file at `.github/`, root or `docs/` | A: one of the three paths returns 200; A: `codeowners/errors` is empty |
| `SOP-verified-code-owners` | High tier: each code owner appears in `data/maintainers.yaml` with a verification dated within 12 months | A: every CODEOWNERS entry is in that file with a date under 12 months |
| `SOP-dependency-management` (Know and watch your dependencies) | Dependabot alerts on; a published dependency policy; services pin direct dependencies exactly | A: `vulnerability-alerts` returns 204 (404 is off only with admin read, else yellow). T: dependency policy; T: service pins |
| `SOP-vulnerability-remediation` | High tier: critical in 14 days, medium and high in 60 | A: no open critical Dependabot alert older than 14 days and no high or medium older than 60; A: no open code-scanning alert of medium or higher older than 60. T: coordinated releases |
| `SOP-static-analysis` (Code scanning) | Code scanning on changes; critical findings fixed promptly | A: `code-scanning/default-setup` state `configured` or analyses non-empty; A: no open critical alert older than 14 days |
| `SOP-secret-protection` | Push protection on | A: `security_and_analysis.secret_scanning_push_protection.status == enabled` (needs Administration: read) |
| `SOP-workflow-least-privilege` | Actions default token read-only; hardened workflows | A: `actions/permissions/workflow` has `default_workflow_permissions == read`. T: no outside-controlled text run as a command, no outside pull-request code with write access or secrets, minimal job permissions |
| `SOP-security-policy` (Vulnerability reporting) | A security policy and private vulnerability reporting | A: GraphQL `isSecurityPolicyEnabled`; A: `private-vulnerability-reporting` `enabled == true`. T: disclosure followed |
| `SOP-license-by-type` | A single accepted licence per content type | A: `license.spdx_id` in the type's list (tool: Apache-2.0 or MIT; media: CC-BY-4.0, Apache-2.0 or MIT; research adds CDLA; governance: Apache-2.0); missing or NOASSERTION fails unless `data/deviations.yaml` records an exception |
| `SOP-semantic-versioning` | From 1.0, tags are `vMAJOR.MINOR.PATCH` | A: every non-draft release tag in the last 12 months matches. T: a stable-release policy (graduated tools) |
| `SOP-contributing` (Contribution guide) | A guide that keeps demands small and asks for tests | A: `community/profile` `files.contributing` not null. T: content |
| `SOP-project-files` (README) | A README | A: `community/profile` `files.readme` not null |
| `SOP-security-design` | High tier: a current short security-controls document | T only |
| `SOP-archive-notice` | Archived repository's README says support ended | A: `archived == true`. T: the note |
| `SOP-maintainers-match` | Named maintainers equal the code owners; owners are a subset | A: compares org owners, public members, `data/maintainers.yaml` and CODEOWNERS. T: other powers declared |
| `SOP-governance-roles-named` | Owners and maintainers have public org membership | A: owners' membership not concealed; maintainers are public members |
| `SOP-org-few-owners` | Two or three organisation owners | A: `orgs/{org}/members?role=admin` returns 2 to 3 |
| `SOP-org-base-permission` | Default member permission read | A: `default_repository_permission` in (read, none) |
| `SOP-org-two-factor` | Two-factor required org-wide | A: `two_factor_requirement_enabled == true` |

The last five rows and `SOP-verified-code-owners` govern an organisation or a maintainers file this repository does not
have; the rest apply to a single repository.

## What the wiki does not ask for

Searched across all 22 SOP pages and `Policies`, 2026-11-14: no signed commits or signed tags, no lock-file or
exact-pin check for a library (pins are asked only of "services the project provides"), no OpenSSF Scorecard run, no
SHA-pinning of third-party actions, no required reviewers beyond code owners. "Signed" appears only for release
artifacts with provenance. These are gaps relative to the supervisor's prompt list, not misreadings; the proposal
(`readout.md`) says what to do about each.

## Facts to carry forward

- The wiki states every check's API route and permission, so each is reproducible with `gh api` and a token with the
  named read permission.
- Several checks need Administration: read (push protection, Dependabot alerts on, the default token, code-scanning
  default setup); the supervisor's own token has it, the workflow's `github.token` does not.
- Attestations are per release and valid only if a code owner last changed the file; this is the wiki's own answer to
  "a human claim that no API can read", and it is the same job this repository's claims register does for prose.

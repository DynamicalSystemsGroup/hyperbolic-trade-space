# WP48 — Scope of work: governance control checks for the release process (research spike; after v0.1)

| | |
|---|---|
| **Status** | DRAFT, a research spike. Approved only by the recorded act below. |
| **Supervisor (accountable)** | mzargham |
| **Repository** | `DynamicalSystemsGroup/hyperbolic-trade-space`; the readout under `work-packages/WP48-rounds/` |
| **Approval record** | The supervisor's verbal approval, quoted verbatim in `work-packages/WP47-decisions.md` |
| **Acceptance record** | The supervisor's acceptance of the readout, quoted verbatim |

## Purpose

The supervisor's direction (`WP47-decisions.md`): his research into open-source software security best practices is in
the Open-MBEE repo-registry wiki (https://github.com/Open-MBEE/repo-registry/wiki), and governance checks exist at
https://github.com/Open-MBEE/governance-checks; out of scope for v0.1, but he wants governance control checks in the
repository as part of the automated release control process, borrowing ideas or code, and expressed as verification
cases where possible. The spike reads both, maps them to this repository, and proposes the shape.

## Goals

- G1. **His research, read:** the wiki's pages summarised with what each check requires (branch protection, signed
  commits or tags, dependency pinning and lock checks, SBOM, licence files, CODEOWNERS, review rules, release
  provenance), each with its source page cited.
- G2. **The governance-checks repository, read:** what it checks, how (actions, scripts, a schema), its licence, and
  which parts could be reused as code in this repository.
- G3. **Verification cases:** how the supervisor's phrase is meant here (the SysML v2 verification case, as the case
  model already uses for its requirements, or the repository's claim-and-backing register) and how a governance check
  would be stated as one: the requirement, the verification method, the evidence the release workflow produces, the
  verdict; two or three checks drafted that way against this repository's state.
- G4. **A proposal:** which checks to adopt first, what each costs, where they run (the release workflow of WP47), and
  what the repository fails today; plain options.

## Non-goals

- Building any check in v0.1; changing the release workflow beyond WP47's.
- Any security assessment of dependencies beyond what the checks themselves report.

## Deliverables

| ID | Deliverable | Serves |
|---|---|---|
| D-1 | `work-packages/WP48-rounds/spike/wiki-notes.md`: the wiki read page by page with citations | G1 |
| D-2 | `work-packages/WP48-rounds/spike/governance-checks-notes.md`: the repository read, with its licence and reusable parts | G2 |
| D-3 | `work-packages/WP48-rounds/spike/readout.md`: the verification-case shape with two or three drafted checks, the repository's state against them, the proposal with plain options | G3, G4 |

## Requirements

| ID | Requirement | Checked by |
|---|---|---|
| R-1 | Every statement about the wiki or the repository cites the page or file read, with the date | the notes |
| R-2 | No file outside `work-packages/WP48-rounds/` changes | `git diff --stat` |

## Definition of good enough

- D-1 to D-3 delivered; R-1 and R-2 pass; the supervisor can pick the first checks from the readout.

## Agent's defaults

- The spike runs as one research agent on Sonnet with web access; the assistant checks three citations at random
  *(default)*.
- "Verification case" is read first as the SysML v2 construct the case model already uses, with the claims register as
  the fallback shape; the readout shows both *(default)*.

## Open decisions (for the supervisor)

None. The direction of 19:25 settles the aim and the timing (after v0.1).

# WP47 — Decisions: release engineering and repository governance (PyPI, branches, semantic versioning, templates)

## The direction (2026-11-14, 19:25)

**Supervisor, verbatim:** "the release is going to involve me setting the package up on pypi, i will need that to be
facilitated by you, let me know when is a good time to do that. i also will need to set up code owners, issue
templates, PR templates, and other items for this repo. for the time being i am the only person who can merge into main
but we should make it straightforward to onboard other maintainers in the future. we want candidate releases to go
through a dev branch. we also want semantic versioning. i recommend you spiking on my repo here
https://github.com/Open-MBEE/repo-registry/wiki to see my research into open source software security best practices.
while its out of scope for the first release v0.1, i like the idea of getting governance control checks into the repo
so they become part of our automated release control process. we can borrow ideas (or even code) from here
https://github.com/Open-MBEE/governance-checks though if possible i'd like to make use of verification cases."

**Applied as:** two packages. WP47 (this file; `WP47-scope-of-work.md`): the release engineering and governance items
v0.1 needs, built so that he does the PyPI steps with exact names in hand: packaging metadata and semantic versioning
(0.1.0 from the held version unit), a release workflow with trusted publishing (OpenID Connect, no tokens) that
publishes on a version tag on `main` after his merge, a TestPyPI dry run from `dev` first, `CODEOWNERS` naming him,
issue and pull-request templates, `CONTRIBUTING.md` stating the flow (candidates on `dev`, releases from `main` by the
maintainer, semantic versioning), `SECURITY.md`, and a maintainers' onboarding page; the branch protections he sets on
GitHub are written down for him as a checklist. WP48 (`WP48-scope-of-work.md`): the research spike on his
repo-registry wiki and the governance-checks repository, out of scope for v0.1, with a readout on which checks become
part of the automated release control and how they are expressed as verification cases.

**The good time for PyPI, as the assistant reads it:** the accounts and the pending trusted publishers (PyPI and
TestPyPI) can be created as soon as WP47 gives him the exact workflow file name and environment name, so before the
release PR; the TestPyPI publish runs from `dev` at the candidate head as a dry run; the real publish runs on the
`v0.1.0` tag on `main` after his merge, so nothing is published before his acceptance.

**Supervisor, verbatim (19:30):** "basically i am talking about the devsecops aspects of this work which come into
focus now that the project is nearing a release"

**Applied as:** WP47 and WP48 together are the DevSecOps line: WP47 the release path v0.1 needs (packaging, trusted
publishing with no secrets, the branch flow, ownership, templates, the maintainers' page); WP48 the controls that become
automated release gates after v0.1, read from his research and expressed as verification cases.

## OD1, the code of conduct (2026-11-14, 19:40)

**Supervisor, verbatim:** "i think it would be good to have a contributor covenant and given the nature of this work to
date it may need to be explicitly tied to how AI is used and supervised. i want this to be an AI native open source
package but i also need it be trusted and trustworthy. so i think the contributor covenant is its own spike."

**Applied as:** OD1 closed. WP47 ships no `CODE_OF_CONDUCT.md`; `CONTRIBUTING.md` leaves a line for the covenant once
it lands. The covenant is its own research spike, WP49 (`WP49-scope-of-work.md`, decisions in `WP49-decisions.md`):
the Contributor Covenant read, the published AI-contribution policies of other open-source projects read, this
repository's own practice written down as it is, and a readout with plain options for a covenant that says how AI is
used and supervised here. Nothing is adopted before his word on the readout.

## Approval

**Supervisor, verbatim (2026-11-14, 19:50; popup, multi-select over WP47, WP48, WP49):** "WP47,WP48,WP49"

**Applied as:** WP47 approved as scoped (OD1 closed above); WP48 approved as scoped (its approval record is this file). The WP47 unit starts in a worktree; the WP48 spike continues from its committed first pass to the readout.

## Amendment 1: the cheap enforcement checks in v0.1 (2026-11-14, 19:20 EST)

**Supervisor, verbatim (popup: cheap checks with WP47 in v0.1, or all after v0.1 under WP48):** "Cheap ones in v0.1"

**Applied as:** WP47 gains the checks that are a small GitHub Action with the gh CLI or a repository setting, from the
list in `WP49-decisions.md` (19:10): (1) issue admissibility on opened or edited (the template's fields present and
non-empty, else a comment naming the gap and the `draft` label kept); (2) the `draft` label removable only by a code
owner, any other removal reverted; (3) a pull request names the issue it resolves or carries the small-fix label; (4)
the pull request description's fields filled; (5) the merge into `dev` by a code owner who is not the author, as the
branch-protection settings on his checklist plus a check on the merge event. Each is a workflow under
`.github/workflows/` pinned by SHA, with a test or a dry run in the review record, and each is written as a
verification case (requirement, method, evidence, verdict) so WP48's readout can cite it. The review-record check
(8) waits for WP48's definition of the record. Fitness items get no script.

## Amendment 2: the software bill of materials in v0.1 (2026-11-14, 19:50 EST)

**Supervisor, verbatim:** "sbom in v0.1"

**Applied as:** WP47's release workflow produces a software bill of materials for each release and attaches it to the
GitHub release beside the wheel and sdist: generated from the locked resolution in a standard format (CycloneDX or
SPDX, the agent's default is CycloneDX via a SHA-pinned action or `uv export` fed to the generator), for the package
as built, so what a version contains can be audited afterwards. It is written as a verification case (the release
carries an SBOM that matches the lock; evidence: the release asset and the workflow log) and is WP48's check 2 made
real in v0.1. The TestPyPI dry run from `dev` produces it too, so the step is exercised before the first real release.


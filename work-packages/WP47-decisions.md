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

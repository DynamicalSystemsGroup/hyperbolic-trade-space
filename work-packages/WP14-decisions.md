# WP14 — Decision records (interface contract, technical ↔ presentation)

Records typed by the agent (driver session). Decisions are the supervisor's.

## Origin (2026-11-08)

- The supervisor's condition on the breakdown, verbatim: "let's assert an interface contract between
  the technical work and the presentation layer work so they can proceed in parallel. the docsite,
  the paper publishing, and eventually the pypi release machinery need to stay stable even as the
  content evolves. so we should be able to pin that interface so i can iterate on content and the
  release machinery and publication flow in parallel". Draft scope by the PM's bounded subagent
  (`WP14-scope-of-work.md`, committed f341690 on dev, merged to main at WP13's acceptance).

## Decision loop (2026-11-08)

- **OD1, the paper executed at build or committed executed.** Options: committed executed /
  executed at build / executed at release only. **Supervisor (mzargham), verbatim:** "committed
  executed but also i want you to ensure we can build and deploy to local host to support review
  loops that don't require a publish to github pages. the review of the staged local host version
  of the site should be done before a merge that would generate a deployment. this needs to be part
  of release control"
- Disposition: decided, committed executed; and a new requirement *(raised by OD1)* for WP14 and
  WP8a: the whole site (root index, `/docs/`, `/paper/`) builds and serves on localhost with one
  command and no network, as a staged review target; the branching convention gains a release-control
  step: a merge to `main` that would deploy is preceded by a review of the staged localhost site,
  recorded; the contract pins the local build-and-serve command as part of the presentation
  interface.

- **OD2, the API reference.** Options: generated from docstrings / hand-written only / generated
  into the supporting material too. **Supervisor (mzargham), verbatim:** "Generated from docstrings".
  Disposition: decided; `mkdocstrings` as WP8 first approved; the numpydoc docstrings are pinned as
  the source in the contract; `docs/api-reference.md` is a presentation-owned stub; `docs/api.md`
  stays the hand-written overview.

- **Agent's defaults, as one item** (with the localhost build-and-serve command added from OD1).
  **Supervisor (mzargham), verbatim:** "Approve the defaults as listed". Disposition: approved. Loop
  closed: decided 2 (OD1, OD2), deferred 0, raised 1 (the staging review, folded into the scope as a
  requirement), defaults approved as one item.

## Scope approval (approval gate)

- pending

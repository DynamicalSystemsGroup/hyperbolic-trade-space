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

- **Document:** `work-packages/WP14-scope-of-work.md` at commit 0ece73e (no open items; R-12 added).
- **Date:** 2026-11-08.
- **Driver's question:** "WP14, the interface contract between the technical work and the presentation
  layer: a pinned contract document with a TOML manifest and a test, the configuration-to-attributes
  table and oracle signature as the stable surface with no tool names, the paper committed executed,
  the API reference generated from docstrings, the one-command localhost staging as release control;
  no open items. Do you approve the scope for execution?" (options: Approved / Not yet).
- **Supervisor (mzargham), verbatim:** "Approved"
- **Disposition:** approved; the PM executes WP14 first on `dev` (WP8a, WP10 and WP15 build against
  it); acceptance merge to `main` by the driver after a review.

## Acceptance gate (2026-11-08)

- Delivery on `dev`: df475b8, 02b9731 (contract and manifest, version 1), 9f8e5f7 (test), 328371a
  (contract follows the delivered site machinery); review `WP14-review.md` (b7f81e0): G0–G4, D-1 to
  D-5, R-1 to R-12 met; 101 manifest-versus-repository fact checks with 0 failures; five deliberate
  breaks each failed with a clause-named message. Manual Tests run on `dev` at 32bb156 green
  (42546036830). Driver's own checks at 32bb156: 1303 passed, 13 skipped, 1 xfailed; ruff, format,
  lock clean; attribution grep 0; the contract, manifest, test, scripts and site files present.
- Gaps (reviewer and PM suggest accept as is unless noted): G-1 commit 328371a edits the
  WP8a-owned `pages.yml`; G-2 the deploy rule and `default-groups` moved while contract_version
  stayed 1 (v1 not yet accepted); G-3 the manifest entered in a WP8a-titled commit; G-4 the test's
  skip list is stale (six of eight entries now enforced; housekeeping follow-up); G-5 open-by-design
  gaps (the Oracle protocol awaiting WP15, `paper/myst.yml` and the `paper` group awaiting WP10, a
  package `__init__` docstring, WP12 ownership); G-6 `--serve` not exercised by the reviewer
  (covered by the supervisor's staged review in WP8a).
- **Bundle (G-1 to G-6).** **Supervisor (mzargham), verbatim:** "Accept the bundle as is".
  Disposition: accepted with the reviewers' reasons; G-4's skip-list housekeeping goes to the PM's
  follow-up list; no open item before the acceptance question.

## Acceptance (acceptance gate)

- **Review of record:** `work-packages/WP14-review.md` (b7f81e0). **Delivery:** `dev` df475b8..328371a
  (with 32bb156 the PM's status commit), merged to `main` together with WP8a after its staged
  review (the merge deploys nothing: the Pages workflow triggers on a release tag or manual
  dispatch only).
- **Date:** 2026-11-08.
- **Driver's question:** "WP14, the interface contract: contract document and manifest at version 1,
  the configuration-to-attributes table and oracle signature pinned with no tool names, the paper
  committed executed, the API reference from docstrings, the localhost staging command pinned, a
  test that checked 101 clauses against the repository; every gap dispositioned, CI green. Do you
  accept the work?" (options: Accepted / Not yet).
- **Supervisor (mzargham), verbatim:** "Accepted"
- **Disposition:** accepted; contract version 1 is in force; changes to it are amendments; WP15 may
  start once its scope is approved; the PM's follow-up list carries the skip-list housekeeping.

## Contract version 2 (amendment; approved with WP8a's Amendment 2, 2026-11-08)

- Items (from `WP8a-scope-of-work.md`, "WP14 contract amendments (contract version 2)", as changed at
  the gate): the pinned docs pages become the user-facing set; ownership of the docs pages moves to
  the presentation side; a pinned path `docs/superpowers/notes/paper-sources/`; the known-gaps row on
  the bibliography and literature page; generated Derivations and Verification pages leave the
  docsite and the world key (C-9) is withdrawn; a change-log row; the route lists in
  `scripts/stage_site.py` and `tests/test_site.py`. The paper-anchors item is dropped (docsite
  citations into the paper are deferred to stable reference keys).
- **Supervisor (mzargham), verbatim** (the same quote as in `WP8a-decisions.md`): "Approved"
- Disposition: contract version 2 approved; executed with WP8a's Amendment 2.

## Contract versions 13, 15 and 16 (pointer entries, 2026-11-10)

Section 14 of the contract says amendments are quoted here; these three were recorded where they arose and are
pointed to from here. Version 13: the case reads the data of record (`case.data_dir` = `examples/adcs/data/v2/`;
WP23's swap, `WP23-decisions.md`). Version 15: eight traded metrics (the WP23 close-out, `WP23-decisions.md`, "The
two metric redundancies"). Version 16: the estimator's two module constants pinned, the palette names out of
`plotting.__all__` (WP25-3 gap P-1, the driver's call in `driver-log.md`, "PM6's batch 2").

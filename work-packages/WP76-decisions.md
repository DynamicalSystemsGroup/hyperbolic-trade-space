# WP76 — Decisions: the iron-triangle example (Kitchenham-CSC software projects)

## His memo (2026-11-17, verbatim; the task's starting document)

"Memo: Iron-triangle example for the next release

Recommendation

Place the iron-triangle example in the next release scope and begin it in parallel with the 0.1 handoff, on a separate
branch. It should not become a dependency for the first release.

The example offers a familiar entry point for project-management readers and demonstrates an important distinction:
metrics can jointly constrain a frontier while some move together and others trade against one another. The existing
probe provides enough material to develop the example, but its sensitivity to conditioning and portfolio composition
deserves a dedicated review.

Developing it against the 0.1 candidate—and then the released package—will also test how readily a contributor can
produce a defensible new case.

Proposed scope of work

Purpose. Produce one reproducible public example answering: Among comparable projects, did greater delivered scope
accompany less schedule and budget slack, and did those two slacks move together?

Starting evidence. Build from the WP70 research packet
(https://github.com/DynamicalSystemsGroup/hyperbolic-trade-space/tree/4f81a4ea3649ff844cff2acdf9d447285cbb0fc5/work-packages/WP70-rounds),
delivered at `4bf40d31` and preserved at `4f81a4ea3649ff844cff2acdf9d447285cbb0fc5`.

The probe used 141 usable Kitchenham–CSC software projects. Near the fitted frontier, scope opposed schedule and budget
slack, while the two slacks moved together. That direction persisted across several scoring definitions, but fitted
exponents and subset readings varied. These are findings to reproduce and assess, not predetermined acceptance
outcomes.

Work

1. Establish reproducibility. Verify the source, licence, checksum, exclusions and existing scripts against the
   current package. Preserve a permitted data artifact or reliable retrieval procedure. Record the exact package
   version and Git SHA used.
2. Define the case in SysML v2. Record attributes, units, effort as the budget proxy, metric orientations, positivity
   transformations, conditioning alternatives and the frontier-band rule in the system model. The example page should
   explain their decision relevance and link to the definitions.
3. Reproduce and challenge the result. Reproduce the one-term baseline and assess the previously investigated two-term
   alternative. Check sensitivity to plausible conditioning choices, frontier-band choices and influential
   observations. Retain the project-type and client subset contrasts.
4. Present both kinds of relationship. Use signed near-frontier associations and scatter plots to distinguish shared
   movement from substitution. Present fitted frontier participation separately. Use a ternary only if it adds a clear,
   defensible reading.
5. Publish one example page. Follow the repository's established example structure: management question, data,
   analysis, findings, practical interpretation and limitations. Keep detailed checks in analysis records and
   assumptions in the SysML v2 system model.

Deliverables

* One public example page with generated figures.
* A SysML v2 system model defining the case.
* Reproducible analysis code and data provenance.
* A compact verification record covering sensitivity and reproduction.
* A short research note identifying what this case could test in a future conic-expression generalization.

Acceptance criteria

* A clean run reproduces the published tables and figures.
* The narrative distinguishes frontier participation, positive association and negative association.
* The headline survives the stated sensitivity checks, or is narrowed to match their results.
* Subset differences and influential observations are reported openly.
* A project-management reader can identify what was measured, what was found and what decisions the evidence cannot
  support.
* Claims remain observational and portfolio-specific. Because the dataset has no quality measurements, it does not
  empirically establish the proposed 3 + m extension.

Boundaries and integration

This package requires no new estimator, conic-expression implementation, additional dataset or broader research
programme. Record package defects separately and resolve any blocking dependency explicitly.

Integrate after the first release, following technical verification and author review of the interpretation. The
conic-expression research may proceed independently; completing it is not an acceptance condition for this example."

## The driver's framing of the package (2026-11-17, from the session that started this one)

The example is a supervisor-gated work package for the release after 0.1, on this branch only: nothing touches `dev`
or `main`, no pull request, nothing outward without his word; the branch is merged into `dev` after 0.1 is out and
after his review. Standing rules restated: no AI attribution; uv only; no new dependency; claims backed or narrowed,
never caveated; model, fit and analysis apart in prose; glossary terms; arbitrary dimension d in symbols; no
metanarration; figures earn their place; no crypto-economic material on public surfaces; package defects recorded here,
not fixed on this branch.

## The branch moved onto the 0.1 candidate (the agent, 2026-11-17)

The branch `claude/iron-triangle-example-12a7c6` was created at the old `main` (e7fd1165, the WP13 merge), which has
none of the examples template, the claims register or the three example pages. It had no commits of its own, so it was
reset onto `dev` 814853ad, the 0.1 candidate the memo names as the development target. Neither `dev` nor `main` was
touched.

## Scope gate

The scope `WP76-scope-of-work.md` is drafted with two open items: OD1 (whether the 3 + m idea appears on the public page)
and OD2 (the Agent's defaults as one item). His answers are recorded below as they come.

## Package defects met on the way (recorded, not fixed here)

Carried from WP70 (`WP70-decisions.md`, "WP70 delivered and landed"), to be re-checked against the 0.1 candidate during
execution:

1. `plot_ternary`'s region label names the two largest exponents as trading even where their near-frontier association
   is positive (+0.43 on the WP70 primary fit).
2. `trade_off_report` raises when fewer than ten rows fall inside the default band `1 / tau` (at about 141 rows a tenth
   above the frontier can leave fewer); every portfolio study needs its band rule stated.
3. The `tau = inf` contending set includes a planted non-participant at a fit-temperature exponent of 0.00 to 0.07 in
   every synthetic run of WP70.

### OD1 (2026-11-17, his answer in the popup, as typed by the agent)

Asked: "Your memo bounds the claim (the data do not establish the 3 + m extension). Does the 3 + m idea appear on the
public example page at all?" Options: not on the page; one sentence in the limitations. His answer, verbatim: "Not on
the page". Decided: the page's limitations say only that the table carries no quality measure; the 3 + m framing stays
in the research note and the WP70 record.

### OD2 (2026-11-17, his answer in the popup, as typed by the agent)

Asked: the Agent's defaults list, as one item: approve, or change items. His answer, verbatim: "Approve the list".
Decided: every default stands as written.

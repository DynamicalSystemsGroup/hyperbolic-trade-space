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

## The base moved with the rename (2026-11-17, during execution)

The driver's session (the one that started this package) sent, verbatim: "The matplotlib font-cache failures in a
fresh worktree are an environment matter known in this repository: set MPLCONFIGDIR to a writable directory of your
own (for example a folder under your scratchpad) before every pytest and figure build, and they go away without any
rebuild. Also for your information: the package was renamed today; dev now carries import name `tradespace` and
repository `DynamicalSystemsGroup/tradespace` (the old address redirects), so rebase your branch onto origin/dev before
you touch src imports or URLs, and the SysML toolkit cache moved to ~/.cache/tradespace."

Verified before acting: local `dev` at c0e210cc (WP77) has `name = "tradespace"` and `src/tradespace`; `origin/dev`
(efb74de6) is its ancestor; the remote URL is `DynamicalSystemsGroup/tradespace.git`; six commits since 814853ad.
The branch was rebased onto `dev` c0e210cc (one conflict, the contract document: `dev` took amendment 30 for the
rename, so this package's page amendment is 31, contract version 31). The import name in this package's scripts and
tests and the repository URL on the page follow the rename; the results regenerated byte for byte apart from the
provenance. The scope's deliverables, requirements and defaults are unchanged; the header names the new base. The
matplotlib font cache: `MPLCONFIGDIR` set to a scratch folder for every figure build and test run in this worktree,
nothing under the home directory touched.

## Scope gate

The scope `WP76-scope-of-work.md` is drafted with two open items: OD1 (whether the 3 + m idea appears on the public page)
and OD2 (the Agent's defaults as one item). His answers are recorded below as they come.

## Package defects met on the way (recorded, not fixed here)

Carried from WP70 (`WP70-decisions.md`, "WP70 delivered and landed") and re-checked against the 0.1 candidate
(814853ad, version 0.1.0) on 2026-11-17:

1. **The ternary's region label reads the two largest exponents as trading.** Re-checked: on the primary fit
   `plotting._ternary_says(fit.exponents_[0], names)` returns "schedule slack trades against budget slack", where the
   near-frontier association of those two is +0.43. Not blocking: the page draws no ternary (R-10; the verification
   record, section 5). A fix belongs to the plotting step's region-label rule (`notes/directions/README.md`, "Plotting
   step two").
2. **`trade_off_report` refuses an association from fewer than ten rows inside `1 / tau`.** Re-checked: at K = 1 the
   primary fit's `1 / tau` holds 12 rows, so the report does not raise there; the case's band rule (15 rows) is
   stated in the model and applied by `run.band_for`. At K = 2 at the same band the per-term report raises on the
   first term (9 rows): recorded in the results as the message, not worked around. Not blocking; the band rule is the
   analyst's and the example states it.
3. **The `tau = inf` contending set and a non-participant.** Not re-checked here: the case has no planted
   non-participant (all three metrics contend on every scaled rung). Carried as WP70 left it.
4. **New: the two-term fit on the type-D subset reports both term shares as 0.00** (`variants.json`,
   `subsets.type_D.k2.term_share`), with status certified: no near-frontier row is assigned to either term at the
   K = 2 fit's own band, so the shares sum to zero rather than to one. Reported as returned (the verification record,
   section 4); whether `term_share_` should carry a guard or a warning when no row is near the frontier is a question
   for the estimator's owner. Not blocking: the page reads the subsets at K = 1.

### OD1 (2026-11-17, his answer in the popup, as typed by the agent)

Asked: "Your memo bounds the claim (the data do not establish the 3 + m extension). Does the 3 + m idea appear on the
public example page at all?" Options: not on the page; one sentence in the limitations. His answer, verbatim: "Not on
the page". Decided: the page's limitations say only that the table carries no quality measure; the 3 + m framing stays
in the research note and the WP70 record.

### OD2 (2026-11-17, his answer in the popup, as typed by the agent)

Asked: the Agent's defaults list, as one item: approve, or change items. His answer, verbatim: "Approve the list".
Decided: every default stands as written.

## WP76 approved (2026-11-17, his answer in the popup, as typed by the agent)

Asked whether he approves `WP76-scope-of-work.md` at cf5c66f8 for execution on this branch. His answer, verbatim:
"Approved". Execution begins under `work-execution`; nothing on `dev` or `main`.

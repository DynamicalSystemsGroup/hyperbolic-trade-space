# Driver's log (the autonomous phase)

Kept by the driver (the supervisor's assistant session). Two lists: what is waiting for the
supervisor, and what the driver decided for the PM, with its basis, so the supervisor can audit
those calls at any time. The supervisor's own decisions are quoted in the `WPn-decisions.md` files,
not here. Rules for who answers what: `PM-BRIEF.md`, "The autonomous phase".

## Waiting for the supervisor

Nothing. By the mandate of 2026-11-08 (`release-candidate.md`) the next thing that reaches him is
the PR from `dev` to `main` with the reviewer's guide, unless a stop condition is met first: a
contradiction of his recorded words, a finding about the mathematics that changes a statement or a
conclusion, a trade-off his words do not settle, or an outward-facing act other than the PR.

## Scopes and acceptances by the driver (for the supervisor's review at the PR)

| Date | Call | Evidence | Record |
|---|---|---|---|
| 2026-11-08 | Accepted the proof-step tagging as a first increment of the paper's D-12 | checker: 14 files, 191 steps; chain passes; 148 derivation and proof-map tests pass with the two guarded test files unedited; no statement, title or axiom list changed; lint clean | `WP10-decisions.md`, "The driver's calls under the mandate" |
| 2026-11-08 | Defined and approved WP10 Amendment 2: close the tagging's findings truthfully (seven prose-only steps, premises hidden in symbol assumptions, listed axioms nothing depends on, unlicensed forced expansions); withdrew my own instruction not to change the axiom lists | `derivation/PROOF_MAP_FINDINGS.md`; the supervisor's rules on steps and cited results | `WP10-scope-of-work.md`, "Amendment 2" |
| 2026-11-08 | Committed the CI step that provisions the pinned SysML toolkit | the fetch verifies size and sha256 before extraction and the library's pinned commit; run locally: 7 toolkit tests pass | `.github/workflows/test.yml`, 7653e75 |
| 2026-11-08 | Defined and approved WP16, the data swap: mutation check, a clean generation in the container of record, a three-way comparison, then swap unless a conclusion changes | the four new datasets have the frozen files' sha256 (checked by the driver); ledger entries marked dirty; identity on one machine is not yet evidence about the model or the container | `WP16-scope-of-work.md`, `WP16-decisions.md` |
| 2026-11-08 | Docstrings shown in the API reference carry no lemma, axiom or specification tags; plain words now, stable keys into the paper at release preparation | the docsite review's gap G-1; "make sure we don't have left over references to content we removed" | to be recorded in `WP8a-decisions.md` at acceptance |
| 2026-11-08 | The first-order condition in L3 (new entry I10) is re-based on the constraint qualification for affine constraints, with LICQ on the simplex as a computed step, instead of on strong duality | as delivered, I10 cited Boyd and Vandenberghe 5.5.3 with 5.2.3, which needs convexity, proved in L4, which imports L3's result; the implementer flagged it; no statement changes | `WP10-decisions.md`, "The driver's calls under the mandate" |
| 2026-11-08 | The Linux difference in a check design's saturation fraction is not loosened away: it is measured between this Mac and the container and the tolerance is set from that evidence, inside WP16 | CI run 42560520228: 0.0179 on Linux against 0.0215 committed, beyond the stated relative tolerance of 0.1 | `WP16-scope-of-work.md` (G2), to be recorded in `WP16-decisions.md` |
| 2026-11-08 | The paper's committed outputs must be produced in the container before CI is asked to match them; values that depend on the platform are named in one list with reasons, not skipped | the same run: a generated table's hash differs between macOS and Linux | `WP10-scope-of-work.md`, Amendment 1, R-31 |
| 2026-11-08 | The docsite gains figures (at most seven, generated at build time from the package's plotting functions on the synthetic data of the code shown above each); this reverses the approved default of a docsite without figures | the driver's browser pass: sixteen pages, no figure, a page about plots that shows none; "like with other unsupervised method we need lots of plots to make the space intuitive" | `WP8a-driver-browser-pass.md` |
| 2026-11-08 | Root page map links to its full size and may use a wide screen; a redraw is left to the reader loops. Phone-width tables become lists; API reference parameters render as lists | the same pass: the map is 694 px wide from a 1536 px image and unreadable; tables cut off at 375 px | `WP8a-driver-browser-pass.md` |

## Decided by the driver for the PM

| Date | Question | Decision | Basis |
|---|---|---|---|
| 2026-11-08 | WP15 needs a Z3 executable for the model checks | `z3-solver` added to the `case` group; lock at 5.3.3.0 | the supervisor's recorded role for Z3 in WP15; inside the approved scope; recorded in `WP15-decisions.md` |
| 2026-11-08 | Docsite home page linked the glossary at the wrong path (strict build failed) | routed to the PM to fix | a defect against WP8a Amendment 2's own requirement |
| 2026-11-08 | Docsite limitations page 17 words over its budget | trim the page; do not raise the budget | the budgets were approved with Amendment 2; "i think it can be thinned out" |
| 2026-11-08 | Platform of record for the container | linux/amd64, to match CI | shown to the supervisor in the approval question for WP10 Amendment 1; approved with it |
| 2026-11-08 | Site tests collide when several agents run the suite in one checkout | the site fixture builds into a temporary directory; a failure in files an implementer does not own is re-run alone before it is reported | a defect in the tests' robustness, inside WP8a's own requirement that the suite passes |
| 2026-11-08 | The pinned toolkit is not provisioned in CI, so five model-checking tests would fail there | no Tests dispatch on `dev` until the workflow provisions it; the PM sends the step, the driver commits it | the supervisor's "Pinned" for the toolkit in WP15; fixtures fail by name by design |

## Verification snapshots by the driver

| Date | Tree | Result | Reading |
|---|---|---|---|
| 2026-11-08 | `dev` near 2e808f9 plus uncommitted work of four implementers | 1508 passed, 11 skipped, 1 xfailed, 13 errors; lock clean; attribution 0; lemma chain passes on re-run | not a verdict: 8 errors were a collision between concurrent site builds (pass alone); 5 need the pinned toolkit, absent from the driver's environment and from CI; lint errors only in an uncommitted file |
| 2026-11-08 | `dev` near 33f63b1, shared checkout, the PM regenerating the experiments meanwhile | 1710 passed, 16 skipped, 1 xfailed, 7 failed; lock clean; attribution 0 | not a verdict: the 7 failures are the experiment and data tests, which pass alone (57 passed) and failed while the ledger was being rewritten; lint errors only in uncommitted files |
| 2026-11-08 | commit 66f997c, the driver's clean checkout, this Mac | 1727 passed, 16 skipped, 1 xfailed, 1 failed; lint, format, lock clean; lemma chain passes; proof map OK, 229 steps | a verdict: one real defect, a site test that asserts files only an earlier manual build creates |
| 2026-11-08 | commit 33f63b1, CI run 42560520228, ubuntu | 1711 passed, 5 failed | a verdict: the same site test; a spec check already fixed later; a tolerance of 1e-9 on an integrated value across platforms; the paper's committed Appendix C output carrying a platform-dependent hash; one check design's saturation fraction 17 percent from the committed value on Linux |

**Method from here on.** The driver verifies a named commit in its own clean checkout (a git
worktree in the session scratchpad with its own locked environment), not the shared tree, so a
result is a verdict on a commit and cannot be disturbed by agents at work. First used at 66f997c.

## Overruled or corrected (kept so the pattern is visible)

| Date | The driver's call | The supervisor's correction |
|---|---|---|
| 2026-11-08 | Described approved Appendix F as the source map | it was the verification audit; corrected in chat and in `WP10-decisions.md` |
| 2026-11-08 | Three kinds of proof step including one argued only in prose | "proof steps that cite an inherited result are still steps ... which still needs to happen in the code" |
| 2026-11-08 | Leave the helper functions in L3's script; move them later | "its a best bet to factor helper tools into their own file" |
| 2026-11-08 | Nine details in one defaults item | "you lumped a lot here" |

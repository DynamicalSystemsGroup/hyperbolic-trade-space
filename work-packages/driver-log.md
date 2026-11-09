# Driver's log (the autonomous phase)

Kept by the driver (the supervisor's assistant session). Two lists: what is waiting for the
supervisor, and what the driver decided for the PM, with its basis, so the supervisor can audit
those calls at any time. The supervisor's own decisions are quoted in the `WPn-decisions.md` files,
not here. Rules for who answers what: `PM-BRIEF.md`, "The autonomous phase".

## Waiting for the supervisor

**Needs him (2026-11-09, 01:14):** his Colima configuration is changed from his original and the
driver could not restore it. A second container implementer, dispatched by the PM with a brief that
allowed restarting Colima, set `rosetta: false` in `~/.colima/default/colima.yaml` at 00:46 and
restarted the VM. The driver stopped the agent; the attempt to restore the file and restart the VM
a second time was refused by the session's permission check, rightly, as interference with his
running workloads. State left: Colima running with `rosetta: false`; one container the agent
started, `hts-exec`, still running. To restore: set line 126 back to `rosetta: true` and restart
Colima when convenient. No agent uses Docker or Colima until he says so.

**Needs his decision (2026-11-09, 02:35; work continues meanwhile):** two fitted attributes,
settling time and slew time, are read off integration steps. Under perturbations of one part in
10^12 the paper's conclusions do not move (contending sets, leading metrics, signs of tensions,
temperatures, certificates, check outcomes, feasibility), but several printed numbers do (146
becomes 145; 8 becomes 7; the K = 3 shares move in the second decimal) and one design's slew time
jumps from 33.4 s to 12.5 s where its trajectory grazes the settling band
(`work-packages/swap-evidence.md`, "Sensitivity of the conclusions"). Keep the data and report at
reproducible precision with the effect named as a gap, or measure the times by event detection and
regenerate everything.

**For his eye at the PR, from the cold reads:** three readers did not accept "facet share, our
analogue of explained variance" as stated (the register's entry); the title's "scaling" is not
carried by the first screen; how his own review of the mathematics and the tools disclosure are
worded; the sentence about his INCOSE paper.

**For his eye, not blocking:** the platform of record for the container is provisionally
linux/arm64 instead of linux/amd64, which he was told would come back to him
(`docs/superpowers/notes/spike-container-platform/report.md`).

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
| 2026-11-09 | **Provisional, promised back to the supervisor:** the container of record is linux/arm64, not linux/amd64; exact equality only inside it, stated tolerances elsewhere | spike: amd64 under Rosetta cannot start the notebook kernel; arm64 runs both notebooks and 67 of 68 paper tests in two minutes; hashes of float data differ by architecture and by operating system | `docs/superpowers/notes/spike-container-platform/report.md`; `WP10-decisions.md` |
| 2026-11-09 | WP15 returned after its fresh review: the two oracles through one interface, exclusions written to the ledger and consumed by the sampler are fixed before acceptance; the momentum condition outside the solver is accepted with its reason | `WP15-review.md`: the clean model is what is evaluated (trace with equal hashes; the reviewer's own mutations move the attributes and flip the flags); gaps A to F | `WP15-decisions.md`, "The driver's calls under the mandate" |
| 2026-11-09 | The saturation fraction is compared with an absolute tolerance of 0.01 and no relative term | `swap-evidence.md`: a step count over about 1340 steps, diagnostic only; moves by whole steps under 1e-15 perturbations; largest deviation 0.0080 over 60 re-runs; flags never change | `WP16-decisions.md` |
| 2026-11-09 | Before the swap is decided: measure whether the paper's conclusions move when the two step-quantized fitted times jitter (five perturbed regenerations per dataset, refit each) | the same evidence: settling and slew time move up to 1.3 percent, 0.48 s, under rounding-level perturbation | `WP16-scope-of-work.md`, Amendment 1 |
| 2026-11-09 | Under either answer on the times: a new abstraction gap for step-read times and band grazing; the paper prints fragile quantities with their measured range and residues as bounds; the swap is held and the simulator untouched | `swap-evidence.md`, sensitivity section: 740 quantities compared over five perturbed regenerations; conclusions identical, some printed numbers not | `WP16-decisions.md` |
| 2026-11-09 | **Accepted WP15** (the system model tidy-up) | its fresh review with the reviewer's own mutations; the returned gaps closed with tests; commit 2d2a751 green in the driver's clean checkout (1804 passed, 0 failed; ledger verifies with no drift). A complete Linux run on this commit is still owed (GitHub download timeouts) | `WP15-decisions.md` |
| 2026-11-09 | **Accepted WP8a with Amendment 2** (the docsite for a package user, the root page) | three browser passes by the driver at two widths and both schemes; commit 2d2a751 green; the docsite's own 78 tests. The PM's separate reviewer did not repeat the browser pass | `WP8a-decisions.md`; `WP8a-driver-browser-pass.md` |
| 2026-11-09 | WP10 (the paper) returned after its fresh review. Fix before acceptance: the word cap counted on what renders; figures referenced; the execution test; Levels 2 and 3 named; the claims beyond their basis; a reading pass on what cited sources say | `WP10-review.md`: one requirement not met, one partly; rendered prose about 6,390 words against the cap of 6,000 because the counter omitted generated sentences | `WP10-decisions.md` |
| 2026-11-09 | **Removed a false sentence from the paper:** "an external reviewer audited the mathematics" | the review was the supervisor's own, with an AI-made chart (his words, `external-review-2026-11.md`); how to describe it is his wording | `WP10-decisions.md` |
| 2026-11-09 | The novelty sentence is reworded to say what was looked at and not that the literature lacks it | "we claim nothing as novel"; "clarify what our work does differently, extends, adds" | `WP10-decisions.md` |
| 2026-11-09 | Triage of the first cold reads (one fresh reader per depth): 22 findings; change requests to the paper, Appendix F, the docsite and the package | every reader stated the story correctly; reproduction matched cell for cell; an unseen planted table was read correctly from the docs alone; replicated gaps: n-lemma membership against the figure, the planted recovery result absent from the main text, the unexplained 10 percent target, the unargued analogy for the facet share | `WP10-cold-reads.md` (verbatim); `WP10-cold-reads-triage.md` |
| 2026-11-09 | Package: fitted attributes exist for every K; a quantity comparable across K (`mean_slack_`); the contract's manifest amended with them | the adapt-depth reader hit an AttributeError at one term and compared `objective_` across K, which is two different quantities; reproduced by the driver | `WP10-cold-reads-triage.md`, items 19 to 22 |
| 2026-11-09 | Defined and approved WP11, the reader-grid loops: answer key fixed first with its hash committed, six cells held out, three roles apart, at most four rounds | the supervisor's words on the grid; the first cold reads | `WP11-scope-of-work.md`, `WP11-decisions.md` |

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
| 2026-11-09 | commit 7656157, the driver's clean checkout, this Mac | 1753 passed, 16 skipped, 1 xfailed, 3 failed; ruff check clean; ruff format fails on 4 files; lock clean; lemma chain passes; proof map OK, 236 steps; attribution 0 | a verdict, not green: Appendix B was not regenerated after the first-order axiom was re-based (the checker and the paper's tests caught it, as designed; one test pinned the step count as a literal); docsite code blocks are not in ruff's format. Docsite fixes confirmed separately in the browser |
| 2026-11-09 | commit a7eebde, the driver's clean checkout, this Mac | 1758 passed, 16 skipped, 1 xfailed, 0 failed; ruff check and format clean; lock clean; lemma chain passes; proof map OK, 236 steps; attribution 0 | **the first green verdict on a named commit** |
| 2026-11-09 | commit a7eebde, CI run 42572757374, ubuntu | 1755 passed, 3 failed | the three values that are exact only where they were produced: the planted table's hash, Figure 1's data hash, one check design's saturation fraction. The pinned toolkit and the Z3 wheel both work on Linux. |
| 2026-11-09 | commit 67de186, the driver's clean checkout, this Mac (includes the paper's main text and the environment-of-record tolerance design) | 1795 passed, 13 skipped, 1 xfailed, 0 failed; ruff check and format clean; lock clean; lemma chain passes; proof map OK, 236 steps; attribution 0 | green |
| 2026-11-09 | commit 2d2a751, the driver's clean checkout, this Mac | 1804 passed, 13 skipped, 1 xfailed, 0 failed; ruff check and format clean; lock clean; lemma chain passes; proof map OK, 236 steps; ledger 15 entries, 0 drifts; attribution 0 | green; the commit on which WP15 and WP8a Amendment 2 are accepted |
| 2026-11-09 | commit 5636ca7, the driver's clean checkout, this Mac (the paper with the new gap, reproducible-precision reporting and the rendering fixes; the hardened toolkit helper) | 1838 passed, 13 skipped, 1 xfailed, 0 failed; ruff check and format clean; lock clean; lemma chain passes; proof map OK, 236 steps; ledger 15 entries, 0 drifts; attribution 0 | green |
| 2026-11-09 | commit 5636ca7, CI run 42588028427, ubuntu (amd64) | 1838 passed, 13 skipped, 1 xfailed, 0 failed | **green on Linux**, the first since the environment-of-record tolerance design; the same counts as the Mac. Settles the Linux run owed on WP15 and WP8a Amendment 2 (5636ca7 contains 2d2a751) |

**Method from here on.** The driver verifies a named commit in its own clean checkout (a git
worktree in the session scratchpad with its own locked environment), not the shared tree, so a
result is a verdict on a commit and cannot be disturbed by agents at work. First used at 66f997c.
| 2026-11-09 | CI stays blocked by a GitHub timeout on one toolkit download: the helper gains an idempotent fetch, an install from a local archive and an API fallback, all with the same checksum verification; the pin is not changed | the direct URL returns 504 from CI and from this Mac for over an hour; the same asset fetched through the release API has the pinned sha256 | to the PM; the workflow step follows the helper's commit |

## Overruled or corrected (kept so the pattern is visible)

| Date | The driver's call | The supervisor's correction |
|---|---|---|
| 2026-11-08 | Described approved Appendix F as the source map | it was the verification audit; corrected in chat and in `WP10-decisions.md` |
| 2026-11-08 | Three kinds of proof step including one argued only in prose | "proof steps that cite an inherited result are still steps ... which still needs to happen in the code" |
| 2026-11-08 | Leave the helper functions in L3's script; move them later | "its a best bet to factor helper tools into their own file" |
| 2026-11-08 | Nine details in one defaults item | "you lumped a lot here" |

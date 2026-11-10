# Driver's log (the autonomous phase)

Kept by the driver (the supervisor's assistant session). Two lists: what is waiting for the
supervisor, and what the driver decided for the PM, with its basis, so the supervisor can audit
those calls at any time. The supervisor's own decisions are quoted in the `WPn-decisions.md` files,
not here. Rules for who answers what: `PM-BRIEF.md`, "The autonomous phase".

## Waiting for the supervisor

- (2026-11-10, 02:25) **Do proposals that fail a model requirement count as check designs?** Under the stated
  reach rule the proposer returns three proposals on the settling-time view; two are one configuration; all three
  sit at the small end of the battery range (22 to 25 Wh) and fail the depth-of-discharge requirement, because the
  proposer trains on the settled, momentum-safe, power-positive rows (as WP7 did) and the chart has no
  depth-of-discharge axis. The log V claim holds for 3 of 3 and the position claim now for 1 of 3 (was 0 of 3).
  Options: keep them as check designs and let the section say the proposer does not see the feasibility flag; or
  train the proposer on the fully feasible rows (a method change to the check, scoped); or drop the proposals and
  keep the three hand-written candidates. The driver's recommendation: the first for 0.1, said plainly, with the
  second recorded as future work. Non-blocking; the paper's sentences follow whatever you choose.
- (2026-11-10, 00:35) **Two findings of WP23 round 3 for your decision at the gate (the gate proceeds; these
  come with the threshold popup).** (1) The metric set carries two redundancies the data make plain: eclipse reserve
  and depth of discharge are one quantity (Spearman -0.9994; the reserve 0.3C - D and the ratio D/C are the same
  inequality), and power margin and energy balance are both affine in the generated power (log correlation 0.96:
  one carries the exponent, which one switches between regimes). Options when you are back: keep both of each pair
  as the model's MoPs and let the fit show it; or drop one of each (seven traded metrics); or keep the pairs and
  state the redundancy in the case prose as a reading. (2) The proposed peak-slew-power limit of 2.4 W (20 % above
  the baseline) fails 56.4 % of the feasible primary designs, because peak slew power is a step function of the
  wheel class and tracker grade (41 distinct values); a percentage margin on a step is not a threshold. The driver
  has asked the loop to propose the limit on the step's own terms (the value that admits the baseline's wheel
  class, with the pass fraction of each candidate shown) so the popup shows you what each choice admits.
- (2026-11-09, 23:20) **WP23, coming to you at the data gate (proceeds overnight on my verification per
  "Proceed, I review after"):** the four illustrative thresholds proposed by the loop, each 20 % above the baseline
  configuration: pointing error 0.0186 deg; control effort 0.0114 N·m·s; peak slew power 2.4 W; launch budget
  95,698 USD (15.95 kg at an illustrative 6,000 USD/kg); plus a battery discharge-rate requirement of 1 C from
  round 2 (the battery swap was assessed and not taken: its couplings were already present). Round 1 facts: with
  the new model, events and nine metrics, the metrics with zero exponent at every temperature went from four to
  three in the primary regime (settling time now carries weight) and from two to one in the baseline regime; the
  three that never bind (power margin, eclipse reserve, peak slew power) share one cause found by the coverage
  table: the reaction wheels saturate at the three named configurations, so gains, battery and panel do not move
  peak slew power or power margin. Round 3 interrogates that (ranges, saturation, metric definitions) and changes
  the model only where the system's purpose justifies it. One changed conclusion for your decision at the gate: on
  the round-1 primary regime the K = 3 per-term report refuses (one term's cell has 3 to 7 near-frontier rows
  against the report's minimum of 10); the fit is reported from exponents and shares, nothing loosened.
- (2026-11-09, 18:10; answered 20:40) **The word "energy differential".** Resolved: "Keep it, gloss it" (`WP10-decisions.md`).
- (2026-11-09, 19:30; answered 20:45) **The abstract's PCA sentence.** Resolved: reword as distinct, complementary and composable (`WP10-decisions.md`).
- (2026-11-09, 20:20; answered 20:55) **Slew time under event detection.** Resolved: one time metric, the settling time (hold time); slew time leaves the traded metrics (`WP16-decisions.md`).

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
| 2026-11-09 | **Accepted WP10 structurally** (the paper with Amendments 1 to 3); container deliverables, the data swap and the supervisor's list left open and stated | two fresh reviews (the second: accept with gaps noted; no mathematical error; 28 numbers recomputed); six cold reads triaged and answered; commit 4ede5bd green on the Mac and on Linux (1882 passed, 0 failed on both); the driver's rendered read | `WP10-decisions.md` |

## Decided by the driver for the PM

| Date | Question | Decision | Basis |
|---|---|---|---|
| 2026-11-08 | WP15 needs a Z3 executable for the model checks | `z3-solver` added to the `case` group; lock at 5.3.3.0 | the supervisor's recorded role for Z3 in WP15; inside the approved scope; recorded in `WP15-decisions.md` |
| 2026-11-08 | Docsite home page linked the glossary at the wrong path (strict build failed) | routed to the PM to fix | a defect against WP8a Amendment 2's own requirement |
| 2026-11-08 | Docsite limitations page 17 words over its budget | trim the page; do not raise the budget | the budgets were approved with Amendment 2; "i think it can be thinned out" |
| 2026-11-08 | Platform of record for the container | linux/amd64, to match CI | shown to the supervisor in the approval question for WP10 Amendment 1; approved with it |
| 2026-11-08 | Site tests collide when several agents run the suite in one checkout | the site fixture builds into a temporary directory; a failure in files an implementer does not own is re-run alone before it is reported | a defect in the tests' robustness, inside WP8a's own requirement that the suite passes |
| 2026-11-08 | The pinned toolkit is not provisioned in CI, so five model-checking tests would fail there | no Tests dispatch on `dev` until the workflow provisions it; the PM sends the step, the driver commits it | the supervisor's "Pinned" for the toolkit in WP15; fixtures fail by name by design |

- 2026-11-09: WP8b (release preparation) and WP20 (verification in tiers) scoped by the fresh PM's
  bounded scope subagents in the template, no open decisions; approved by the driver under the
  mandate. WP8b brings the items done ahead of its scope (LICENSE, changelog, punch list, archive)
  under it and sequences the reference keys and the reviewer's guide after WP11's stopping rule and
  the version last. WP20 covers the slow markers, `scripts/check.py`, the xdist group and the CI
  shards; its first two commits are already on `dev` (04a3471, 78f5e1c) and are accepted against it.

- 2026-11-09: the container of record (P10, 48df440) and the driver's call that the committed exact
  values are produced inside it, approved by the supervisor: "the reproducibility results make sense
  to me. byte exact with identical image but small differences due to minor variations in
  mathematical libriaries when switching between linux and mac. document and approve". The
  regeneration inside the container runs under WP10 Appendix F; Appendix F's text states the
  two-sided result.

- 2026-11-09: WP21 (the response to the independent assessment; the term-aggregation toggle with the
  sum as default) and WP22 (the system model's two views) scoped by the PM and approved by the
  driver under the mandate. WP22's two open decisions settled by the driver for the supervisor's
  review: metrics without a bound in the configuration stay uncovered and are shown as traded without
  a requirement (their values are his, WP22b); the slew-time requirement is completion within the
  horizon. The Linux run on the head with the WP17 fix still fails the same three exact-recording
  tests at tau = inf (run 42705219840; the three shards work); returned to the PM with the container
  of record as the place to reproduce it.

- 2026-11-09, 17:20: the supervisor steps away for an extended period and leaves the driver in charge.
  **Verbatim:** "i want to remind you to remind our team to look at images/screenshots not just code
  and text because we're building this for humans. we have a grid of human stakeholder proxies and
  depths of reading you can use for assessments. remember you report to me the pm agent reports to
  you and all the subagents report to the PM. we're orchestrating a complex engineering project and
  what i want is to get this project into a state i can approve for a first release. you are left
  in charge while i am away from my computer." Standing while he is away: every rendered thing is
  judged from its image in the browser, never from code or text alone; the reader grid (six personas
  by six depths, `docs/superpowers/notes/reader-grid.md`) is the instrument for assessments; the
  chain of report is subagents to the PM, the PM to the driver, the driver to him; decisions that are
  his accumulate under "Waiting for the supervisor" below with the driver's recommendation and the
  work routes around them; the progress updates continue in the chat.

- 2026-11-09, 18:10: WP11 round 1, the L-A and L-B cells (12 fresh readers on the staged paper at
  20fa550): no reader believed the method picks a design or that a certificate is a global optimum;
  three wrong beliefs replicated (the surface as a regression through the cloud; PCA replaced rather
  than joined; a facet as a cluster of designs); "energy differential" guessed by 12 of 12; the case
  sentence of the abstract carries no finding for any reader; Figure 2 the anchor, Figures 4 and 7
  fail the cold read. Record and change requests CR-1 to CR-5 in `WP11-round-1/triage.md`; CR-5 is
  a term decision for the supervisor (under "Waiting for the supervisor", with the driver's
  recommendation).

- 2026-11-09, 18:25, calls on the PM's table. (1) The regeneration inside the container of record
  (03189c5, d66c106, 25dba3c): accepted on the record's evidence (0 failed in both images with the
  flag; no conclusion-level change; the CSVs untouched; the changed values listed), subject to tier 2
  and the Linux run dispatched on it (42717834248). (2) The WP17 fix for the Linux failure
  (d66c106): the cause is a degenerate LP at tau = inf (gap G-10); off-platform the test now matches
  facets by exponent vector and compares exponents and labels, and skips the path-dependent
  quantities (status, iteration counts, support weights, the objective change) for tau = inf only,
  with the exact comparison still run in the environment of record. Accepted as justified by the
  tie analysis; the docstring must say so. (3) WP20's question on the workflow trigger: CI runs on
  pushes to main, pull requests to main and manual dispatch, not on pushes to dev; the shards keep
  all three triggers. (4) The docsite figures' reassessment by intent (ce87711): three caption
  fixes, one resize (the tension heatmap) and one drop (the cubesat triangle, his word) approved;
  applied to the pages. (5) The two model views from the visualization engineer (7afffce: the
  assembly view, vertical, with the two kinds of configuration variable marked; the behavioural view
  of requirements, subsystems and the ten traded metrics, with the gaps shown honestly) are
  candidates for WP19 with their recipes; the gap list is WP22's first input.

- 2026-11-09, 19:15: WP19 (figures by section) scoped by the PM in the template, no open decisions,
  approved by the driver under the mandate; candidates are placed when they pass the figure review,
  each with purpose and hypothesis, for the supervisor's review-and-revise on his return. The
  watcher's verdict on abd6c11 (2 failed: the claims-register and vocabulary guards tripping on
  moved fragments and new words) shows the new mechanical checks working; the commits that followed
  (811d260, d7d9919) are the fix-forward, to be confirmed by the next verdict.

## The driver's calls of 2026-11-09, evening (for the supervisor's review)

- **PM handovers.** The fourth PM handed over at c622c6e (after the data gate) and the fifth started at 02:30 on the paper's move onto the data of record. The third PM handed over at 01e2d64 (PM-BRIEF.md, "third PM to fourth") after two batches; the fourth PM started from the files at 21:35 on WP23 and the remaining WP19, paper and package units.

- **Glossary wording (the supervisor's vocabulary).** Wording-only fixes approved where three entries use
  synonyms of their own terms (`facet`, `support-weights`: "fitted surface" becomes the entry's own term;
  `contending-set`: "working temperature" becomes the glossary's term); no meaning changes. Two entries added
  because the paper's statements already use them as fixed terms and one object needs one name: `cell` (the set of
  rows assigned to one facet; A8, L15) and `reach` (β_k, how far the data extend in a facet's direction, the soft
  maximum of their scores; L5), and the derivation text's "support offsets" for β (L14, L15) becomes the same name.
  Added likewise, with definitions taken from the paper's own definition boxes and no new meaning: `near-frontier
  band` (Definition 4), `effective sample size` (Figure 1), `certificate` (Theorem 12), `mean slack` (Theorem 11).
  Deferred to the supervisor: "tension" (kept as a plain word), "soft fit", "pull-back", "abstraction gap".
- **WP19 candidates, the driver's own image reads (cold, image before caption).** The n-lemma ternary: a triangle
  whose corners are the three metrics, edges labelled as dilemmas of their endpoints, the interior a trilemma, the
  three facets' exponent vectors as numbered markers on the planted answers: one look says what an n-lemma is and
  where a facet's exponents put it; earns its place beside Definition 6. The assembly view: a cubesat of eight parts,
  two swapped among three alternatives, four tuned in ranges, levels and ranges read from the model: the "part
  swapping and param tuning" framing in one picture; earns its place in Section 8. The behavioural view:
  requirements on the left pointing at the metric each reads, metrics grouped by subsystem, the four traded metrics
  with no requirement dashed, sources on the right: the logical train from requirement to metric to source, and the
  WP22b gap visible; earns its place in Section 8; the "same statement as SlewBandRequirement" note is cryptic (two
  readers and the driver agree) and is his to word. All three placed as candidates for his review and revise loop.

- **Disk use (2026-11-09, 21:50; the supervisor: "one thing i noticed is that we're eating up a lot of space. are
  we cleaning up environments/images or are they proliferating").** Found: 45 git worktrees under the scratchpad
  (27 GB, most from finished streams), 17 untagged ~2 GB Docker images left by our rebuilds of hts-paper, hts-alt
  and earlier hts images, 26.7 GB of Docker build cache, an 18 GB uv cache. Done by the driver: 34 worktrees
  removed (older than 40 minutes, clean, fully merged into origin/dev); the six live ones kept (27 GB to 4.2 GB).
  Rule given to the PM for PM-BRIEF: a worktree is removed as soon as its unit is pushed; one image per stream,
  the previous image id removed when hts-paper or hts-alt is rebuilt; no venv in a worktree that runs no tests.
  Docker image removal and the two cache prunes: the supervisor approved "Both" (build cache and uv cache); the
  driver's Docker removals were blocked by its permission classifier as irreversible deletions, so the exact
  commands were handed to him to run.

- **A warning leaks into the rendered paper (2026-11-09, 22:55; the supervisor saw it in Section 9 of the staged
  build and asked whether it is handled).** The committed output of the recovery cell (Appendix D.14, 20 planted
  tables across `RECOVERY_TAUS`) carries one stderr line from `paper/generate_results.py:505`: "ConvergenceWarning:
  solver did not converge: max_iter reached; termination status 'iteration_cap', max facet gap 6.66e-16". Reading:
  the several-term alternation hit `max_iter` (500) while the facet gap was at machine precision, so the fit is
  numerically stationary (the level 2 certificate, Lemma 1) and the words "did not converge" overstate it; the
  alternation's assignment step cycled, the per-term fits had converged. Two defects, neither a result: (1) the
  estimator warns on the iteration cap alone; it should warn only when the facet gap is above `tol`, and otherwise
  record the status ("iteration_cap", gap certified) without a warning; (2) the paper's executed cells must carry no
  stderr; a test asserts it over the committed outputs, and the recovery table's `status` column (already there)
  carries the fact; the sentence in Section 9 or D.14 reports the status counts. The claim "16 of 20 within 0.05"
  stands. Routed to the PM as two units (estimator with a test; paper cell regenerated in the container with the
  guard test). Nothing needed from the supervisor.

- **Standing order (2026-11-09, 23:00), the supervisor verbatim:** "add a standing order to review with
  screenshots/browser and to make sure your PM reviewers are not just reading code and prose but actually running
  code, analyzing data and looking at render plots, and web pages". Recorded in `CLAUDE.md` (Reviews run the
  thing), `PM-BRIEF.md` (same title) and the driver's memory; the PM told. The warning leak of Section 9 is the case
  that taught it: three reviews read the cell and none looked at the page.

- **Standing order (2026-11-09, 23:05), the supervisor verbatim:** "another standing order is that negative edits
  are welcome even preferred. the marginal value of content covers prose and figures and really any content. it is
  not just for whether something should be added that still leads to unbounde growth but should also be applied
  regarding whether to delete something". Recorded in `CLAUDE.md`, `PM-BRIEF.md` and the driver's memory; the PM
  told; the length ledger records removals.

- **Clarification (2026-11-09, 23:10), the supervisor verbatim:** "i will eventually have to rewrite the abstract by
  hand so don't stress about that specifically. i mean more like making sure we're not jamming in plots or
  arguments for their ownsake that don't advance the narrative of the paper. we got a bit bloated early n and i want
  a disciplined improvement by subtraction pass once we have have complete content. or if something is stuck in a
  loop or cannot be made clear rather than agonize assess removal". Disposition: no cut pass on the abstract (his to
  rewrite by hand; it rests as is); a whole-paper improvement-by-subtraction pass is a step of the path (5a), run
  once the content is complete (after WP23's regeneration and the rename), judging every figure, argument and
  section by whether it advances the paper's narrative; and a rule for every stream now: when a passage or figure is
  stuck in a loop or cannot be made clear, the next move is to assess removal, not another round.

- **WP23 data gate, the driver's verification in progress (2026-11-10, 02:30; unit pushed at 8507bd9).** Looked
  at, cold: the gate's primary-regime heatmap (nine rows; settling time carries weight at low temperature and
  fades; total mass saturates the colourbar cap, the redraw in progress; energy balance, depth of discharge and
  pointing error carry; control effort white at every temperature), the behavioural view at revision 5 (every
  traded metric with its requirement, MoE and MoP marks legible, launch cost a derived MoE, the stub to total mass
  short but visible) and the assembly view (unchanged but for the legend). Read in the K record: primary regime
  K = 1 at tau 38.1 is a 5-lemma (total mass 0.358, energy balance 0.184, pointing error 0.164, depth of discharge
  0.158, settling time 0.136; control effort 1e-17); K = 3 at tau 113 separates term 1 (energy balance 0.42, total
  mass 0.24, settling time 0.18), term 2 (control effort 0.40, settling time 0.37, energy balance 0.19; share
  0.034) and term 3 (peak slew power 0.61, pointing error 0.23); the baseline regime's K = 1 leads with control
  effort 0.43. Reading: with slew time gone, one term in the primary regime no longer sees the control trade-off
  at all; three terms find it in a small term; the case sentence "one facet blends the subsystems' trade-offs into
  a single tension; three facets separate the contending sets" holds, with a different and arguably sharper
  content. D-9 quantifies old against new before the swap call; the checks on the head are the watcher's and the
  Linux run's (dispatched on 8507bd9); the agent's own runs are recorded in the gate README.

- **Calls of 2026-11-10, 03:05 (the fifth PM's first table).** (1) The per-term mechanism for the K = 3 report: the
  PM's call stands (the paper's generators call `tension_report` with the guard off and the case module applies the
  same guard of ten per term in one helper; the number and the band unchanged; the thin term's panel is its
  one-sentence reason with the estimator's count). A package item for after 0.1 or WP24's docs push: the public
  report should return per-term availability itself rather than refuse at the first thin term; recorded as a
  backlog row, not done now. (2) The WP7 case-study notebook `examples/adcs/adcs_trade_study.ipynb` with its nine
  figures: it reads the frozen copies, names slew time 22 times, carries the old data's outputs and no docs page
  links it. Deleted now as a small unit with its test (`tests/test_notebook.py`) and figures, under the negative-edit
  order and WP25's rule; the frozen generation files stay, since the paper cites them; history keeps the notebook.
  (3) The check section's new sentence for `num-predict-reading` is honest and stays; its phrase "the easy part"
  is a judgement the subtraction pass reads again.

- **The paper on the data of record (2026-11-10, 04:40; 628df90), the driver's image reads before the reviewer's
  pass.** The temperature-sweep figure after redraw 2: titled by regime, nine rows ranked by exponent, the fit
  temperature an outlined column with the exponents printed in it (total mass 0.36, energy balance 0.18, pointing
  error 0.16, depth of discharge 0.16, settling time 0.14), control effort faint at low temperature and white from
  25 on, the colourbar named with its white floor; a cold reader sees which metrics the one term trades and that
  three never enter. Passes. The one-term plane, now total mass against energy balance: a grey cloud with the
  surface as a line at its outer edge and a few designs beyond; reads as a soft support, not a regression; the
  trade is less tight to the eye than the old slew-time pair, which is the data's truth. Passes. The three-term
  tension figure: term 1 (5-lemma: energy balance, total mass, settling time leading) and term 3 (5-lemma: peak
  slew power 0.61 against pointing error at -1.00) as heatmaps with their contending sets outlined; term 2's panel
  is the one sentence "Too few near-frontier designs for an association reading: 3 of ten", which says exactly what
  the decision asked; the blank panel is large and the subtraction pass may shrink it. Titles already say "term".
  Passes as a candidate. The staged site is rebuilding at 628df90 for the driver's browser pass; Linux dispatched;
  the watcher's run follows.

- **Browser pass of the staged paper at 628df90 (2026-11-10, 04:50; the driver, localhost:8000/paper/).** The page
  renders; no "Warning", "Traceback" or stderr text anywhere on it (counts 0, 0); ten captions (Table 1 and
  Figures 1 to 9) in the new numbering, Figure 5 the one-term plane in total mass and energy balance with its
  caption stating that the other seven metrics are held at the near-frontier median; Section 9 opens with the
  5-lemma sentence on the data of record (total mass, energy balance, pointing error, depth of discharge and
  settling time, exponents 0.14 to 0.36); the abstract is the rested one. One defect found by Linux, not by the
  page: the WP17 R-2 cubesat recording is the old data's (routed). The desktop width is the one that matters; not
  checked at phone width by design.

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
| 2026-11-09 | commit 74f76c0, the driver's clean checkout, this Mac (the paper after the review's and the cold reads' change requests; the package fixes; L15) | 1880 passed, 13 skipped, 1 xfailed, 0 failed; ruff check and format clean; lock clean; lemma chain passes; proof map OK, 15 files, 252 steps; ledger 0 drifts; attribution 0 | green |
| 2026-11-09 | commit 91ef11b, the driver's clean checkout (Mac) and CI run 42619390841 (ubuntu) | both: 1881 passed, 14 skipped, 1 xfailed, 0 failed; on the Mac also ruff, format, lock, lemma chain, proof map (15 files, 252 steps), ledger, attribution clean | green on both platforms: the paper as delivered with its second review |
| 2026-11-09 | commit 4ede5bd, the driver's clean checkout (Mac) and CI run 42623588724 (ubuntu) | both: 1882 passed, 15 skipped, 1 xfailed, 0 failed; Mac: ruff, format, lock, lemma chain, proof map (15 files, 252 steps), ledger 0 drifts, attribution 0 | green on both platforms; the commit on which WP10 is accepted structurally |

**Method from here on.** The driver verifies a named commit in its own clean checkout (a git
worktree in the session scratchpad with its own locked environment), not the shared tree, so a
result is a verdict on a commit and cannot be disturbed by agents at work. First used at 66f997c.
| 2026-11-09 | CI stays blocked by a GitHub timeout on one toolkit download: the helper gains an idempotent fetch, an install from a local archive and an API fallback, all with the same checksum verification; the pin is not changed | the direct URL returns 504 from CI and from this Mac for over an hour; the same asset fetched through the release API has the pinned sha256 | to the PM; the workflow step follows the helper's commit |
| 2026-11-09 | commit b8dcd3b, the driver's clean checkout, this Mac | 1894 passed, 15 skipped, 1 xfailed, 1 failed; ruff check and format clean; lock clean; lemma chain passes; proof map OK, 15 files, 263 steps; attribution 0 | a verdict, not green: the geometric-program steps (L4.14 to L4.24, 23b1d66) landed before Appendix B was regenerated, so its committed output still says 252 steps. The guard caught it as designed. The regeneration is in the PM's hands (uncommitted in the shared checkout at the time). Rule sent to the PM: a lemma change and the regenerated appendix land in one push |
| 2026-11-09 | commit b8dcd3b, CI run 42629688853, ubuntu | 1894 passed, 15 skipped, 1 xfailed, 1 failed | the same single failure as on the Mac (Appendix B's committed output not regenerated); nothing platform-specific |
| 2026-11-09 | commit 4c24f6b, the driver's clean checkout, this Mac | 1901 passed, 15 skipped, 1 xfailed, 0 failed; ruff check and format clean; lock clean; lemma chain passes; proof map OK, 15 files, 263 steps; ledger 15 entries, 0 drifts; attribution 0 | green: the geometric-program wording and steps, the case as a cubesat model coupling power, mass and attitude control, keywords without tool names, the arrow in pane 1 of Figure 1, Appendix B regenerated |
| 2026-11-09 | commit 4c24f6b, CI run 42637501930, ubuntu | success | green on Linux |
| 2026-11-09 | commit 3c9a68d, the staged site built in the driver's clean checkout, in the browser | index page at desktop and 375 px, light and dark, scrolled: the Why triangle (a light and a dark image), the three-pane figure with the arrow beside What, the map beside How; each opens at full size; no horizontal overflow at 375 px. Paper: abstract, keywords, Figure 1 and its caption read as rendered | one finding returned to the PM: two region labels of the Why image sit across the triangle's edge, where the image the supervisor approved has them inside. Test suite on 3c9a68d not finished at the time of this row |
| 2026-11-09 | commit 3c9a68d, the driver's clean checkout, this Mac | 1909 passed, 15 skipped, 1 xfailed, 0 failed; ruff check and format clean; lock clean; lemma chain passes; proof map OK, 15 files, 263 steps; ledger 15 entries, 0 drifts; attribution 0 | green: the index page with an image for each of why, what and how. Linux run 42639977088 in progress at the time of this row |
| 2026-11-09 | commit 3c9a68d, CI run 42639977088, ubuntu | success | green on Linux: the index page commit |
| 2026-11-09 | commit a17ecf6, the staged site built in the driver's clean checkout, in the browser | index page at desktop light and at 375 px dark: the three region labels of the Why image sit inside their own regions, clear of the edge and of the dense part of the cloud, legible at phone width; no horizontal overflow | the driver's finding on label placement is closed. Test suite on a17ecf6 running on both platforms at the time of this row |
| 2026-11-09 | commit a17ecf6, the driver's clean checkout, this Mac | 1912 passed, 15 skipped, 1 xfailed, 0 failed; ruff check and format clean; lock clean; lemma chain passes; proof map OK, 15 files, 263 steps; ledger 15 entries, 0 drifts; attribution 0 | green: the Why image's labels inside their regions. Linux run 42642725921 in progress at the time of this row. The subtitle commit 4ee3a10 after it changed one line of `site/index.html`; the site tests (44) pass on it |
| 2026-11-09 | commit a17ecf6, CI run 42642725921, ubuntu | success | green on Linux: the index page with its three images and the label placement. With the Mac verdict and the browser pass above, the index page change is accepted by the driver |
| 2026-11-09 | commit e63ed70, the driver's clean checkout, this Mac, and the staged site in the browser | 1917 passed, 15 skipped, 1 xfailed, 0 failed; ruff check and format clean; lock clean; lemma chain passes; proof map OK, 15 files, 263 steps; ledger 15 entries, 0 drifts; attribution 0. Browser: the abstract as rendered (194 words), section 1, the Definition, the theory page, the Glossary, the root page | green: WP10 Amendment 4, first push (the surface is posynomial; the data is what is modelled; elasticity for exchange rate with the report's field renamed; the abstract in the supervisor's words; the glossary's class entries). Two leftovers returned to the PM for Amendment 5 (membership wording on the theory page; section 1's PCA sentence). Linux run 42659494793 in progress at the time of this row |
| 2026-11-09 | commit e63ed70, CI run 42659494793, ubuntu | success | green on Linux: WP10 Amendment 4, first push, verified on both platforms and accepted by the driver |
| 2026-11-09 | commit 92d65c3 (includes 1a50ee4, L16), the driver's clean checkout, this Mac | proof map OK, 16 files, 312 steps; two tests of Appendix B fail (committed output not regenerated) | a verdict, not green, and the second time for this reason: the lemma commit was pushed without the regenerated appendix, against the rule given to the PM twice. Returned to the PM with the fix and a mechanical form of the rule for `PM-BRIEF.md`. Full suite running to see whether anything else is red |
| 2026-11-09 | commit f9b8217, the driver's clean checkout, this Mac, and the staged site in the browser | 1927 passed, 15 skipped, 1 xfailed, 0 failed; ruff check and format clean; lock clean; lemma chain passes; proof map OK, 16 files, 312 steps; ledger 15 entries, 0 drifts; attribution 0. Browser: section 6.2 and Theorem 10 (L16), the theory page, the Fitting page, at desktop and 375 px | green: WP10 Amendment 5, R-39 to R-42 (the fit stated without membership; the glossary's GGP; L16; the over-broad claim narrowed), and the head of dev is green again after the Appendix B regeneration. One display finding returned (equation (2) wider than its column). Linux run 42669238762 in progress at the time of this row |
| 2026-11-09 | commit f9b8217, CI run 42669238762, ubuntu | success | green on Linux: WP10 Amendment 5, R-39 to R-42, verified on both platforms and accepted by the driver |
| 2026-11-09 | commit 2985a8c (includes 480937e, WP17), the driver's own acceptance script against the built estimator, clean checkout, this Mac | the default fit is unchanged (planted table: the same exponents and mean slack 0.63084; cubesat mean slacks 0.13842, 0.11733, 0.10593, 0.09287, all as before the change); with `term_temperature = tau`: status certified on the planted table (min curvature 2.196, gap 1e-15, margin and radius not asserted), certified 20 of 20 on the benchmark with 16 within 0.05 of the planted exponents, certified on all four cubesat fits (min curvature 0.0271, 0.0310, 0.1239, 0.0223) with the same contending sets and leading metrics as the default; a soft fit at tau = inf reports not_applicable | WP17's good-enough check by the driver passes, and the numbers equal the spike's to the digits printed. Full suite on this head and the Linux run not finished at the time of this row |
| 2026-11-09 | commit 2985a8c, the driver's clean checkout, this Mac | 2044 passed, 16 skipped, 1 xfailed, 0 failed; format, lock, lemma chain, proof map (312), ledger clean; ruff check: 1 error (a line of 137 characters in `tests/test_site.py`) | not green on lint only; returned to the PM and fixed in the next commits |
| 2026-11-09 | commit 1072dce, the driver's clean checkout, this Mac | 2059 passed, 16 skipped, 1 xfailed, 0 failed; ruff check and format clean; lock clean; lemma chain passes; proof map OK, 17 files, 364 steps; ledger 15 entries, 0 drifts | green: WP17 (the soft-weight fit, its certificate, L17 with I16, Appendix B regenerated), the length ledger, the ternary function with its contract and glossary entries. The driver's own acceptance script for WP17 is the row above. Linux run 42684175900, on the later head f7e5055, in progress at the time of this row |
| 2026-11-09 | commit f7e5055, the driver's clean checkout, this Mac | 2057 passed, 16 skipped, 1 xfailed, 0 failed; ruff check and format clean; lock clean; lemma chain passes; proof map OK, 17 files, 364 steps; ledger 15 entries, 0 drifts | green: the three-pane figure out of the paper's body, the two equations broken across lines, the length ledger's baseline lowered, the container files committed as work in progress. From here, tier 2 verdicts come from the watcher's log (`scratchpad/verdicts.log`), one line per head of `dev`; Linux runs per batch |
| 2026-11-09 | commit 25dba3c (the regeneration inside the container of record), the watcher, this Mac | 2121 passed, 16 skipped, 1 xfailed, 0 failed; lint, format, lock, lemma chain, proof map (17 files, 364 steps), ledger, attribution all clean | green on the Mac: the committed exact values now come from the container; with the record's 0 failures inside both images, the regeneration is accepted by the driver |
| 2026-11-09 | commit 25dba3c, CI run 42717834248, ubuntu, three shards | fast and docs-paper shards green; the slow shard: 1 failed, 383 passed: test_soft_fit.py::test_r2_default_planted_fits_equal_the_recording[planted3_K3_tauinf_support] | down from three cases to one; the same degenerate LP at tau = inf for seed 3; returned to the PM to interrogate seed 3 on amd64 (the assertion carries no values, so the test's message is to be made informative first) |
| 2026-11-09 | commit 7f162c6, tier 2 watcher, clean worktree, this Mac | 2164 passed, 16 skipped, 1 xfailed, 0 failed; ruff check and format clean; lock clean; lemma chain passes; proof map OK, 370 steps; ledger 0 drifts; attribution 0 | a verdict: the two guard failures of abd6c11 (claims register, vocabulary) are fixed forward; dev green on the Mac at the WP19 approval head |
| 2026-11-09 | commit 62085bb, CI run 42727700605, ubuntu, three shards | fast, slow and docs-paper all green | a verdict: the soft-fit planted3 seed-3 case passes on Linux after 6a8abd5 (termination shares carry the tie allowance); both platforms green at the handover head |
| 2026-11-09 | commit 1b496d3, CI run on ubuntu, three shards (includes the WP22d swap ff717ed and 6ed13ed, the paper CR push 4f63628, WP19 19a/19b) | fast, slow and docs-paper all green | a verdict: the swap and the depth-B change requests pass on Linux; the Mac tier 2 verdict on the swap commits is pending (watcher green on 9d5d3fd, 2166 passed, the head before the swap) |
| 2026-11-09 | commit bde5362, tier 2 watcher, clean worktree, this Mac (after the WP22d swap ff717ed, 6ed13ed, d3018ba) | 2166 passed, 16 skipped, 1 xfailed, 0 failed; all checks; lock; lemmas; proof map; 0 drifts; attribution 0 | a verdict: the swap is green on both platforms (Linux 1b496d3 above); WP22d accepted as the adopted model; Linux dispatched on 7ffb719 for the paper placements and the docs vocabulary |
| 2026-11-09 | commit 7ffb719, CI run on ubuntu, three shards (the paper placements 8abb16a, docs vocabulary, WP23 scope draft) | fast, slow and docs-paper all green | a verdict: the figure placements and the vocabulary units pass on Linux |
| 2026-11-09 | commit 77844c5, tier 2 watcher, this Mac | 2166 passed, 16 skipped, 1 xfailed; all checks | a verdict: green through the WP16 trial commits; later heads (redraws, glossary entries, unit 8) pending; Linux dispatched on the handover head 01e2d64 |
| 2026-11-09 | commit 01e2d64, CI run on ubuntu, three shards (the handover head: redraws, glossary entries, unit 8, WP16 switch) | fast, slow and docs-paper all green | a verdict: everything through the third PM's last landing passes on Linux |
| 2026-11-09 | commit 9eb46f7, tier 2 watcher, this Mac | 2166 passed, 16 skipped, 1 xfailed; all checks | a verdict: green through the fourth PM's first WP23 units; the staged site rebuilt at 3fcc855 for the supervisor's browser |
| 2026-11-09 | commit c0f43f2, tier 2 watcher, this Mac (WP23 round 1 units, the plotting default, the glossary entries) | 2166 passed, 16 skipped, 1 xfailed; all checks | a verdict: green through WP23 round 1; Linux dispatched on the round 2 head (2620188 and after) as the batch gate |
| 2026-11-09 | commit 1501c53, CI run on ubuntu, three shards (WP23 rounds 1 and 2 unit 1, the plotting default) | fast FAILED (test_vocabulary: "fitted surface" in plotting.py's module docstring, the known red, fixed at 0059264), slow FAILED (test_model_coverage: the committed coverage table differs from a Linux regeneration), docs-paper green | a verdict with one new finding: the coverage table's empirical part is not platform-stable as committed; routed to the WP23 stream (the environment-of-record rule: exact equality only under HTS_ENVIRONMENT_OF_RECORD=1, structural equality elsewhere, or the table regenerated in hts-paper and pinned from there); re-dispatch after the fix |
| 2026-11-09 | commit 6d27662, tier 2 watcher, this Mac (the estimator warning condition, the recovery cell regenerated in hts-paper, the no-stderr guard, the Appendix B position, WP25 scope) | 2166 passed, 16 skipped, 1 xfailed; all checks | a verdict: green; the committed notebooks carry no ConvergenceWarning line (grep 0); Linux re-dispatched on dd44575 (the coverage table under the environment-of-record rule) |
| 2026-11-10 | commit dd44575, CI run on ubuntu, three shards | slow green (the coverage table under the environment-of-record rule passes on Linux); fast FAILED (test_claims_register: C150 points at a test, fixed after at 7dff092 to be confirmed; test_site: limitations.md carries a relative link "../../../paper/" from the Appendix B pointer, new); docs-paper FAILED (test_cr2: "fig-plane-k1" not in list after the Figure 2 rename, fixed after at f969e23 to be confirmed) | a verdict: the coverage-table finding is closed; three later-landed units tripped guards; the limitations link is routed; re-dispatch on the next head |
| 2026-11-10 | commit 9130208, CI run on ubuntu, three shards (the three guard fixes, WP25's deletions, P-11, the Appendix B position) | fast, slow and docs-paper all green | a verdict: both platforms green at the head before the gate unit; the coverage table, the register, the Figure 2 rename and the limitations page all pass on Linux |
| 2026-11-10 | commit a27191e, tier 2 watcher, this Mac (WP23 D-7 case prose) | 2166 passed, 16 skipped, 1 xfailed; all checks | a verdict: green; the gate unit (regeneration with the reach rule) is the next head to verify on both platforms |
| 2026-11-10 | commit 8507bd9, CI run on ubuntu, three shards (the WP23 gate unit: swap, contract 12, reach rule, regeneration of record) | fast, slow and docs-paper all green | a verdict: the gate head is green on Linux; the Mac watcher's run on it is next; the swap call waits on D-9 |
| 2026-11-10 | commit 241c63d, tier 2 watcher, this Mac (contains the WP23 gate unit 8507bd9 and the heatmap redraw 2) | 2166 passed, 16 skipped, 1 xfailed; all checks; lock; lemmas; proof map; 0 drifts; attribution 0 | a verdict: the gate head is green on both platforms; the WP23 swap is final (WP23-decisions.md) |
| 2026-11-10 | commit c622c6e, tier 2 watcher, this Mac (the fifth-PM handover head; the suite now 2223 tests after WP23's additions) | 2223 passed, 16 skipped, 1 xfailed; all checks; 29 min | a verdict: green; the paper's regeneration unit is the next head of consequence |
| 2026-11-10 | commit 628df90, CI run on ubuntu, three shards (the paper on the data of record) | fast and docs-paper green; slow FAILED: test_soft_fit R-2 default cubesat fits against the recording (primary, stock) | a verdict with one finding: the WP17 R-2 recording of the cubesat fits is the old data's and was not in the unit's slot list; routed as a fix-forward unit (regenerate in hts-paper); re-dispatch after |

## Overruled or corrected (kept so the pattern is visible)

| Date | The driver's call | The supervisor's correction |
|---|---|---|
| 2026-11-08 | Described approved Appendix F as the source map | it was the verification audit; corrected in chat and in `WP10-decisions.md` |
| 2026-11-08 | Three kinds of proof step including one argued only in prose | "proof steps that cite an inherited result are still steps ... which still needs to happen in the code" |
| 2026-11-08 | Leave the helper functions in L3's script; move them later | "its a best bet to factor helper tools into their own file" |
| 2026-11-08 | Nine details in one defaults item | "you lumped a lot here" |
- 2026-11-09, lines of equal V on the triangle (spike). The driver drew them at a fixed geometric
  mean and labelled them with relative values of log V. The supervisor: "why is max V running off
  the page. shouldn't it be interior?", "the points well above V=1 imply an error". Corrected: the
  total is held fixed, each facet's V peaks at its exponent vector, no design is above log V 0.071.
  Lesson for figures: a label on a level line must be a quantity a reader can check against the
  designs drawn beside it.
- 2026-11-09, the GGP clause of the abstract. The driver held the supervisor's sentence and offered
  him wordings, on the ground that section 6 says the several-facet fit is not convex. He answered
  that the driver was confusing the fit with the analysis and asked for a research sprint. The
  sprint (`docs/superpowers/notes/spike-ggp-fit/`) found him right: no design needs a unique facet
  in the fit, and with the weights given the fit is one GGP. Lesson: when his statement about the
  method looks false, do the spike from his side first and bring the finding, not a menu.
- 2026-11-09, the three-pane figure. The driver's call was that it goes on the index page and also
  stays the paper's Figure 1. The supervisor, reviewing the staged paper: "i am worried they may be
  out of place and distracting in the paper body. it may be best to keep this in the index as a high
  level story arc / gloss." Overruled: the figure leaves the paper's body (ticket with the PM).
- 2026-11-09, the cubesat triangle in the docs' examples. The driver's browser pass called it clean
  and informative. The supervisor: "this is pretty vacuous. doesn't seem to earn its place on the
  page, even in the documentation. make sure we also do visual loops for figures". Overruled: the
  figure is dropped. Lesson: tidy is not informative; a figure whose caption says all it shows fails.
  The figure review (`docs/superpowers/notes/figure-review.md`) now applies to every figure, and the
  driver's own look is one reading in it, not the verdict.
- 2026-11-09, how the run was being driven. The supervisor: "it seems like you are missing the
  opportunity to use tight scopes of work to parallelize efforts using the PM as an orchestrator."
  and "i don't like the fact that you are not committing. we have dev so you can commit work".
  Corrected: `work-packages/parallel-board.md` (one tight scope and one set of files per stream,
  each in its own worktree, readers fanned out); the rule that held pushes until a full check is
  replaced by commit-and-push to `dev` as each unit is done, with verification after, on `dev`.
  Fourteen held commits were pushed, and the container files left uncommitted since the Colima
  incident were committed.
- 2026-11-09, waiting on checks. The supervisor: "are you regularly blocked waiting on ci (which
  takes a long time); i think you should design a strategy to be employed by our PM that helps keep
  us unblocked while also not completely forgoing the checks". The driver had spent 12 to 25
  minutes waiting on each full run. Now: `docs/superpowers/notes/verification-strategy.md` (tiers;
  the full suite runs on each new head in a watcher nobody waits for; Linux per batch; both
  platforms only at acceptances and merges), stream P11 for the tooling, and a separate worktree
  for the browser staging.


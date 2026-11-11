# WP29 — Scope of work: Track A, the noise result (a new result from Proposition 2)

| | |
|---|---|
| **Status** | DRAFT. Approved only by the recorded act below. Nothing in this package is executed before then. |
| **Supervisor (accountable)** | mzargham |
| **Repository** | `DynamicalSystemsGroup/hyperbolic-trade-space` (local: `/Users/z/Documents/GitHub/posynomial-invariant-form`); work on `dev` |
| **Approval record** | The driver's approval under the mandate (`release-candidate.md`), quoted verbatim in `work-packages/WP29-decisions.md` |
| **Acceptance record** | The driver's acceptance under the mandate, quoted verbatim in `work-packages/WP29-decisions.md`, after `work-packages/WP29-review.md`; the placement in the paper (stage 5) additionally needs the supervisor's word, recorded there |

**Header note.** Track A of the lifecycle that `PM-BRIEF.md` ("Bigger candidate edits run the full lifecycle") sets for
any candidate edit that is more than a narrowing or a placement. The origin is the supervisor's S-9 (`WP28-decisions.md`),
verbatim: "consider whether we need another result that addresses our models relationship to measurement noise and/or noise
in the process being measured. this may result in more work so first spike for relevant results and if we can add a
result that builds on this proposition to character our relation to the noise. similiar to the modeling updates deploy
research spike agents before deciding whether/what to build, then build, then quality control, then integrate, then
review again." Stages (1) and (2) are done and recorded; this package is stages (3) to (6). Drafted 2026-11-11 from
`origin/dev` a2d25f9.

## The six stages

| Stage | State | Record |
|---|---|---|
| (1) Research spike | Done; readout at 9002bbe (now `work-packages/WP23-rounds/spikes/spike-E-noise/README.md`, with `check1` to `check4` scripts and outputs). No change to the product | the readout |
| (2) Decision | Done: the driver, 2026-11-11 00:05, `driver-log.md` (entry 98dae07, "Track A stage (2)"), decided below | `driver-log.md` |
| (3) Build | This package, D-1 to D-4 | the lemma scripts, tests, Appendix B |
| (4) Quality control | This package, R-5 to R-9 | `WP29-review.md`, section "Quality control" |
| (5) Integrate | **Prepared as a proposal and not landed** until the supervisor's morning glance at the two statements (new results in his paper are his to see before they are placed) | D-5, then D-6 on his word |
| (6) Cascade review, then acceptance review | This package, R-12 to R-14 | `WP29-review.md` |

**Stage (2), the decision (the driver's, `driver-log.md`):** build **A3** and **A1**; **A2** (the ridge reading) held
as a tested-by-spike statement in the gaps ledger with its check script kept; **A4** dropped as a result (it duplicates
M2); **A5** (risk-averse certainty equivalent) recorded only, no Discussion paragraph (a risk attitude the method does
not have); the entropic-risk source is opened in full before the paper cites it, as every reference is.

- **A3.** L6 with a noise covariance: for eps ~ N(0, Sigma), (1/tau) log E exp(tau w.eps) = tau w'Sigma w / 2 (the same
  moment-generating-function route; L6 is Sigma = sigma^2 I); a diagonal Sigma gives the shift tau sum_j w_j^2 sigma_j^2 / 2.
  The conditioning as the map from a relative measurement error on an attribute to the noise the fit sees,
  sigma_j = delta_j / s_j under log-affine conditioning (the spike's A4 convention, not the dropped candidate A4: see
  A2 of the defaults). The cubesat injection table, both regimes: it states that the data of record carry no noise of
  their own, that noise is injected as a design choice, and that the finding belongs to the fit-plus-conditioning pair,
  not to the model.
- **A1.** The two-regime upper bound on the noise shift of the soft maximum: for clean scores s_i and noise z_i i.i.d.
  N(0, v^2), v = sigma ||w||, `mean(s) - LME(s) <= E LME_tau(s+z) - LME_tau(s) <= min(tau v^2 / 2, E max_i z_i)`, with
  E max z_i <= v sqrt(2 log N) (Jensen with L6 below; the maximum of the draws above). Stated as an upper bound that is
  **not tight** (the spike found it loose by a factor of 2 to 6 at tau = 50 to 200), with the crossover
  tau* = 2 sqrt(2 log N) / v as a rule of thumb, not a sharp one.

## Purpose

The paper has one place that ties the temperature to a noise level, L6 (Proposition 2), and it assumes equal noise in
every conditioned metric (A5), which the standard conditioning cannot deliver: each log-attribute is divided by its log
spread, so a one percent error on total mass (spread 0.066) is as large in the metric as 12 percent on settling time
(readout, A3). A reader from stochastic frontier or stochastic DEA will ask what noise level their temperature assumes
and how far the exponents move with it. The outcome of this package: two statements the paper can state, each a lemma
script with tagged steps, a test on planted data and a regenerated Appendix B, plus a cubesat injection experiment that
shows what noise does to the contending set; and, after the supervisor's glance, their placement with every number,
sentence, register row and key the change moves found and resolved. Kept apart in the prose (`CLAUDE.md`): the
**model** (the noise-free soft maximum), the **fit** (the estimator on a finite noisy table) and the **analysis** (what
a reader concludes); the injected noise is a property of the experiment, not of the system.

## Goals

- G1. **Two results proved at the repository's standard.** A3 and A1 each a lemma script in `derivation/` in the
  ledger pattern (`docs/superpowers/notes/proof-conventions.md`), a test on planted data, Appendix B regenerated in the
  same push, the proof map updated.
- G2. **A case demonstration that says what it is.** The cubesat injection table for both sampling regimes, with the
  statement that the data carry no noise and the noise is injected.
- G3. **Held and dropped candidates recorded.** A2 in the gaps ledger as a tested-by-spike statement with its check
  script kept; A4 and A5 recorded in the readout's disposition and nowhere else.
- G4. **The placement prepared, not landed.** A proposal the supervisor can read in the morning: the corollary after
  L6, the covariance form, the case table in Appendix D, the G-3 and G-12 readings; landed only on his word.
- G5. **The cascade found and resolved** after the placement: every number, sentence, figure, ledger row, register
  row and key the change moves.

## Non-goals

- A2 (the ridge reading and a noise-sensitivity reading of `conditioning_`) built; A4 as a result; A5 as a definition
  or a Discussion paragraph; a risk-averse (-tau) variant; any statement of consistency (G-11 stays open with M2).
- A change to `src/`, the estimator, the data of record, the model files or the cubesat's evaluation. The noise is
  injected in the experiment script; the data stay unchanged.
- Any placement in the paper, the docs or the register before the supervisor's word (stage 5).
- Process-noise frontiers beyond the entropic reading L6 already carries; a stochastic-frontier or stochastic-DEA
  estimator; kernel or K > 1 versions of the noise results.

## Deliverables

| ID | Deliverable | Serves |
|---|---|---|
| D-1 | `derivation/lemma_18_noise_covariance.py` (name *(default)*): A3's lemma, plain SymPy, tagged steps: the multivariate-normal moment-generating function, the quadratic form, the diagonal case, the conditioning map sigma_j = delta_j / s_j | G1 |
| D-2 | `derivation/lemma_19_noise_shift_bound.py` (name *(default)*): A1's lemma: the lower bound (LME >= mean, Jensen on exp), the Jensen-with-L6 upper bound (concavity of log), the maximum-of-draws upper bound (the inequality of exponentials, as L5 does), and E max z_i <= v sqrt(2 log N) with its source or derivation tagged | G1 |
| D-3 | Tests on planted data: one file per lemma or one shared (`tests/test_derivation.py` additions are the derivation stream's; new test files preferred *(default)*): the identity and the sandwich on planted draws, a negative control for each (a deliberately wrong covariance form; a bound with the shift reversed) | G1 |
| D-4 | `derivation/proof_map_record.json` (and `PROOF_MAP_FINDINGS.md` if it lists lemmas) updated; Appendix B (`tab-B-*` cells of `paper/supporting_material.ipynb`) regenerated in the same push, on the host | G1 |
| D-5 | The cubesat injection experiment as a script under `examples/adcs/` (or kept under the spike folder until placement *(default)*) writing the table for both regimes: relative error delta 0.5, 2, 5, 10 percent, 8 repetitions, contending-set Jaccard, largest exponent change, offset shift against L6 with the diagonal Sigma and against the isotropic A5 reading; the table header states the three facts of G2 | G2 |
| D-6 | Gaps ledger rows (`docs/superpowers/notes/abstraction-gaps.md`): A2 as a tested-by-spike statement citing `check2_noise_is_ridge.py` (kept); the G-3 and G-12 readings **as a proposal** (see D-7) | G3, G4 |
| D-7 | `work-packages/WP29-placement-proposal.md`: the proposal for stage 5 as text and diffs the supervisor can read: the corollary after L6 (statement, sketch and script box as the paper's other results have them), the covariance form, the case table placed in Appendix D, the revised G-3 and G-12 readings, register rows, the entropic-risk citation if any (source opened in full, DOI or stable URL resolved, before it enters `docs/references.bib`) | G4 |
| D-8 | After the supervisor's word only: the placement landed; the cascade pass | G4, G5 |
| D-9 | `work-packages/WP29-review.md` (quality control, cascade, acceptance review) and `WP29-decisions.md` | all |

## Requirements

| ID | Requirement | Checked by |
|---|---|---|
| R-1 | A3's statement is proved: for Sigma positive semi-definite, (1/tau) log E exp(tau w.eps) = tau w'Sigma w / 2; for diagonal Sigma, tau sum_j w_j^2 sigma_j^2 / 2; L6 is Sigma = sigma^2 I. The conditioning map holds under log-affine conditioning and the lemma states that hypothesis | `uv run python derivation/run.py` (or the repository's lemma runner) passes the new script, every tag resolving; the reviewer reads the step list against the statement |
| R-2 | A1's statement is proved in its three parts and is stated as an upper bound that is not tight; the crossover is stated as a rule of thumb | the lemma script passes; the statement text in the script contains "not tight" and no sentence claims equality of the shift with either bound; reviewer reads |
| R-3 | A planted-data test per lemma: the identity (A3) and the sandwich (A1) hold within Monte Carlo tolerance on at least the spike's cell family (N = 100 to 10000, v = 0.05 and 0.2, tau = 1 to 200), seeds fixed | `uv run pytest -q <the new test files>`; the reviewer reruns with two other seeds |
| R-4 | **Negative controls fail as they should**: a wrong covariance form (the isotropic A5 form applied to unequal sigma_j) fails the A3 test by a margin the test states (the spike found the isotropic reading off by 10 to 20 times on the case); a reversed or tau-shifted bound fails the A1 test | the control tests run and pass as expected-fail checks (`xfail(strict=True)` or an explicit assertion that the wrong form is rejected), listed in `WP29-review.md` |
| R-5 | Every existing lemma script still passes and the proof map's check passes with the two lemmas present | `uv run python derivation/run.py` all green; the repository's proof-map check (`uv run python scripts/check.py --changed` lists it); `uv run pytest -q tests/test_derivation.py` |
| R-6 | **Appendix B is regenerated in the same push as each lemma** (the lemma stream's rule), on the host with the suite's tolerance branches; the container is not a step here (`PM-BRIEF.md`, "The container is a gate check"). A re-recorded reference that the exact-equality branches read re-records only the arrays this change affects, leaves the rest, and marks the file "host-recorded, re-pin at the gate" | the Appendix B test; `git diff --stat` of the push shows the notebook outputs and the lemma in one commit; `git grep -n "host-recorded, re-pin at the gate"` lists every file so marked, each named in `WP29-review.md` for the driver's regression |
| R-7 | The cubesat table's claims are the ones the readout measured, regenerated by the script: Jaccard and largest exponent change per delta and regime; the offset shift against L6 with diagonal Sigma and against the isotropic reading. A number in the table not reproduced by the script on a fresh run does not appear | the script run twice from the repository root, outputs diffed; the reviewer compares the spike's `check3-output.txt` with the new output and records every difference |
| R-8 | The table states, in its header and in the proposal's prose: the data of record carry no noise of their own; the noise is injected as a design choice; the finding belongs to the fit-plus-conditioning pair, not to the model. No sentence says the cubesat is noisy | grep of the table text and D-7 for the three statements; a cold reader (Sonnet, no repository context beyond the table and its caption) is asked what the table shows and what it does not show, and the answer is recorded verbatim |
| R-9 | Vocabulary and claims: new text uses the glossary's terms (`uv run python scripts/check_vocabulary.py`, with the flag the repository's current state requires); every sentence a reader can rely on is backed by a lemma step, a generated value or a test, or is narrowed or dropped; the model, the fit and the analysis are kept apart | `check_vocabulary.py` count not above its baseline; a claims pass over D-7 listed row by row in `WP29-review.md` |
| R-10 | **Exact-equality references.** The new lemmas and tests add no exact-equality reference of their own; any existing test whose reference the Appendix B regeneration moves is named, re-recorded only for the affected arrays, and marked per R-6 | `uv run pytest -q -m "not slow"` green on the host apart from failures already at the start, each named; the list of files marked per R-6 |
| R-11 | The stage-5 proposal is complete and **nothing in it has landed**: after D-7 and until the supervisor's word, `git diff <start>..HEAD -- paper docs/method.md docs/references.bib claims_register.toml docs/superpowers/notes/abstraction-gaps.md` shows only D-6's A2 row and nothing of the G-3 or G-12 readings, the corollary, the Appendix D table, the register rows or the citation | the diff above; `grep -n` for the new lemma's number in `paper/*.ipynb` returns the Appendix B table only |
| R-12 | **The cascade** (after the supervisor's word): every number, sentence, figure, ledger row, register row, lemma count, proof-map entry, cross-reference and key the placement moves is found and resolved: the lemma count in the paper and docs, the length ledger (`paper/length_ledger.toml`: a raise row, or cuts, for the added words), the register (a row per new claim, the ones G-3 and G-12 touch re-read), `references.bib` (the entropic-risk source opened in full before it is cited), `notation.md` (sigma_j, delta_j, s_j if introduced), the glossary and Appendix A (a new entry regenerates Appendix A in the same push), the interface contract's keys if a table or cell id is pinned | the cascade list in `WP29-review.md`, one line per item with its state and hash; a search for every changed number (`git grep -n` of the old values) shows no stale hit |
| R-13 | The paper and docs build and the rendered result is looked at: the placed corollary, the Appendix D table and the revised G-3 row as rendered, in a browser, with screenshots in the record | `uv run python scripts/stage_site.py --paper placeholder` (after the stage note: a fresh worktree copies the main checkout's `paper/_build/templates`); the reviewer opens the pages in a browser tab of their own (`tabs_create`), records screenshots and the console and stderr state |
| R-14 | **Acceptance review runs the thing:** a reviewer other than the executor reruns R-1 to R-13 at the head, runs the lemma scripts, the tests, the experiment and the build, and records commands, output lines and screenshots; the PM reads it before the driver's acceptance | `WP29-review.md`, section "Checks" |
| R-15 | Untouched: `src/`, the data of record, the model files, `pyproject.toml`, `uv.lock`; no file renamed; no attribution line | `git diff --stat <start>..HEAD -- src examples/adcs/data examples/adcs/model_v2 pyproject.toml uv.lock` empty; `git log --format=%B <start>..HEAD \| grep -ciE "co-authored-by\|generated (with\|by)"` returns 0 |

## Files owned

| Stream | Owns |
|---|---|
| Derivation-side agent (stage 3, Sonnet, its own worktree) | `derivation/` (the two new lemma scripts, `proof_map_record.json`, `PROOF_MAP_FINDINGS.md`), the new tests for them, Appendix B regeneration only (the `tab-B-*` outputs of `paper/supporting_material.ipynb` and what that regeneration rewrites); the experiment script D-5. Touches no prose of the paper, docs, register or glossary |
| Proposal writer (stage 5 preparation, Sonnet) | `work-packages/WP29-placement-proposal.md`, D-6's ledger rows |
| Paper stream (stage 5, 6, on the supervisor's word) | the paper cells, `docs/` pages, `claims_register.toml`, `paper/length_ledger.toml`, `docs/references.bib`, `notation.md`, `glossary.yaml` and Appendix A as the cascade requires |
| Reviewers (stages 4, 6) | `work-packages/WP29-review.md`; no product file |

While a gate's container regression runs, no stream pushes anything that regenerates paper outputs or the v2 data (the
PM says when it has landed); the lemma push waits for that word, prose and records may land.

## Sequence

1. D-1 and D-2 with D-3 and D-4 in the derivation-side agent's worktree: one lemma, its test, its Appendix B
   regeneration and proof-map entry per push (tier 1, host).
2. D-5 (the experiment), then D-6's A2 row.
3. Stage 4: R-1 to R-10 checked; a cold math read of both lemma statements and proofs by a reader who has not seen the readout (Sonnet), recorded verbatim with dispositions.
4. D-7, the proposal, and the notice to the driver that the two statements are ready for the supervisor's glance. **Stop.**
5. On the supervisor's word: D-8 (the placement), the cascade (R-12), the build and the rendered look (R-13), the acceptance review (R-14), the driver's acceptance.

## Risks

- **The exact-equality references.** Appendix B regeneration on the host rewrites tables that environment-of-record
  tests read with exact-equality branches. Mitigation: R-6 and R-10 (re-record only affected arrays, mark the file,
  leave the pin to the driver's container regression); the push waits if a regression is running.
- **The held placement.** Stage 5 waits for the supervisor; the build can finish while the paper is unchanged, and a
  late reply leaves the lemmas in Appendix B with no prose citing them. Mitigation: R-11 keeps the placement out of
  every file until his word; the proposal is self-contained; if he declines a statement, the lemma, its test and its
  Appendix B table are deleted as one unit (the marginal-value test, applied to what is already there).
- **A bound mistaken for a result.** A1 is true and loose. Mitigation: R-2 and the proposal's wording; the cold read
  asks what the bound lets a reader conclude.
- **A conditioning claim that belongs to the analyst.** sigma_j = delta_j / s_j holds under log-affine conditioning
  only; other scalers need their own map. Mitigation: the lemma states the hypothesis (R-1); the table says the finding
  belongs to the fit-plus-conditioning pair (R-8).
- **The citation.** The readout opened the Foellmer-Knispel chapter's abstract page only, and no page that states the
  entropic formula. Mitigation: the source is opened in full before any citation (stage 2), or the sentence stays a
  derivation from L6 with no citation.
- **Lemma-number and count drift.** New lemmas move counts the paper, docs and register state. Mitigation: R-12.

## Definition of good

- Two statements the supervisor reads once and sees the point of: noise enters through a covariance and the
  conditioning is the map from a measurement error to the noise the fit sees; the shift of the soft maximum is bounded
  and the bound says when L6 can be read. Each proved at the repository's standard, tested with controls, placed with
  its cascade resolved, and a case table a reader trusts because it says what is injected.

## Definition of good enough

- The two lemma scripts pass with tagged steps; planted-data tests and negative controls pass; the proof map and
  Appendix B are current; the existing suite is as at the start or better; the files marked "re-pin at the gate" are
  listed (R-1 to R-6, R-10).
- The injection table reproduces from its script and carries the three statements (R-7, R-8).
- The proposal is complete and nothing of it has landed before the supervisor's word (R-11); if he declines a
  statement, its unit is removed whole.
- After his word: the placement landed, the cascade list closed, the rendered pages looked at, the reviewer's run
  recorded (R-12 to R-14); the untouched surfaces untouched (R-15). Stop there and present.

## Definition of done

Good enough is met, **no open item remains unresolved**, and the supervisor has accepted the work by the acceptance record above.

## Agent's defaults

Approved or changed as one item at the scope gate. Each is marked *(default)* where it appears.

- **A1. Decisions inherited.** Stage (2) as the driver recorded it (build A3 and A1; hold A2; drop A4; record A5) and
  the lifecycle of `PM-BRIEF.md` hold unchanged *(default)*.
- **A2. Naming.** The spike's candidate labels A1 to A5 are the readout's; "the conditioning convention" in A3 is the
  readout's "log-affine conditioning (A4)", a different A4 from the dropped candidate. Lemma files take the next two
  numbers after `lemma_17`, named as in D-1 and D-2 *(default)*.
- **A3. Models by role.** Sonnet for the derivation-side agent, the proposal writer, the cold readers and the
  reviewers; Haiku for mechanical units (greps, counts, screenshot runs); Opus only on the driver's word *(default)*.
- **A4. One worktree per stream**, from `origin/dev`; one unit, one push; the derivation-side push only with its
  regenerated Appendix B (`PM-BRIEF.md`) *(default)*.
- **A5. The experiment's parameters** are the spike's (delta 0.5, 2, 5, 10 percent; 8 repetitions; the clean tau);
  the script stays under the spike folder until placement, then moves with the table *(default)*.
- **A6. Test files** new, not additions to `tests/test_derivation.py`, to keep the derivation-side agent's blast
  radius to new files *(default)*.
- **A7. Where the review files live**: `WP29-review.md` and `WP29-decisions.md` beside this scope, following WP25-4
  *(default)*.
- **A8. The cold reader** of R-8 and the cold math read of stage 4 are Sonnet agents given only the artifact, recorded
  verbatim with the disposition of each remark *(default)*.

## Open decisions (for the driver)

- **OD1.** The supervisor's glance at the two statements is the gate for stage 5. How does the driver want the
  statements put to him? — options: (a) the proposal file `WP29-placement-proposal.md` with the two statements, their
  proof sketches and one cubesat table, as one short read / (b) the two lemma scripts' rendered Appendix B tables
  only, with the driver's own summary / (c) a short rendered page of the proposal staged in the site build for a look
  in the browser.
- **OD2.** If the supervisor does not reply before the lemmas pass stage 4, what does the package do? — options:
  (a) wait, with the lemmas, tests and Appendix B tables landed on `dev` and no prose citing them / (b) hold the
  lemma pushes too, so `dev` carries nothing of Track A until his word, the work staying in a branch.
- **OD3.** The entropic-risk citation. — options: (a) find and open in full a source that states the entropic formula
  (the readout names Foellmer-Knispel 2011, DOI 10.1142/S0219493711003334; its page returned 403 and the formula was not seen, so not yet opened in full) and cite it in the proposal /
  (b) no citation; the sentence is a derivation from L6 and says so.
- **OD4.** The cubesat injection script and table. — options: (a) the script moves to `examples/adcs/` and its table
  goes to Appendix D at placement / (b) the table is a docs-page figure of the fit-plus-conditioning pair and not an
  appendix table / (c) the script and table stay in the spike folder and the paper cites the lemmas only.

The driver decides OD1 to OD4 under the mandate; the rest is the Agent's defaults as one item.

## Gate outcomes

- None yet.

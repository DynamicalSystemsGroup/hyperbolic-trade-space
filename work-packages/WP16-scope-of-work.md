# WP16 — Scope of work: the data swap (the paper's case on the generation of record)

| | |
|---|---|
| **Status** | Defined and approved by the driver under the mandate of 2026-11-08 (`release-candidate.md`); for the supervisor's review at the PR. Executes after WP15 is verified and accepted by the driver. |
| **Supervisor (accountable)** | mzargham |
| **Records** | `work-packages/WP16-decisions.md`; the driver's calls in `driver-log.md` |

## Purpose

The supervisor: "do it in parallel to start but eventually i'd like to be able to swap over onto the
new data", and for 0.1: "Swap for 0.1 if the evidence supports it" (the option put to him: move the
paper's case and its records onto the new generation, list every number that changes and why, keep
the frozen data as the cited comparison; if the new data changes a conclusion, stop and bring it
to him).

## What is known (verified by the driver, 2026-11-08, `dev` at 093dc7a)

- The four cubesat datasets generated through the clean model (`examples/adcs/data/v2/`) have the
  same sha256 as the frozen files on this machine. The change register lists no number that moves.
- The new oracle loads `model_v2/cubesat.sysml`, runs its analysis through the runtime, checks
  feasibility through the model, and integrates the slew with the unchanged Python simulation.
- Not yet known: that a change to the model changes the output (so that identity is a result and
  not a reused path); what the generation looks like when produced in the container of record
  (linux/amd64); the ledger entries were written from a tree with other agents' uncommitted files
  and are marked dirty.

## Goals

- G1. **A generation of record.** The datasets the paper uses are produced through the clean model,
  from a clean checkout at a named commit, with ledger entries that are not dirty.
- G2. **The evidence for the swap, as three comparisons:** frozen against new on this machine
  (done: identical); new on this machine against new in the container of record; and every number,
  table and figure of the paper computed on each. Each difference is listed with its size and its
  cause; each paper number is marked unchanged or changed, with both values.
- G3. **The swap.** `examples/adcs/case.py` and the paper read the generation of record; Appendix C
  describes the model that produced it; Appendix F gives its provenance (ledger entry, hash,
  commit, platform) and the command that regenerates it with the tolerance to expect elsewhere.
- G4. **The frozen generation stays as the cited comparison**, where it is, read by the accepted
  packages' record scripts and tests, and tied to the generation of record by a test.

## Non-goals

- Changing the model's physics, the sampling, the seeds or the scenario constants.
- Re-running or editing the accepted records of WP7, WP9 and WP13 (they stay on the frozen files;
  the tie in G4 is what carries them over).
- The legacy geostationary dataset and its oracle (kept for the study of model scope).

## Deliverables

| ID | Deliverable |
|---|---|
| D-1 | A mutation check in the tests: a scratch copy of the model with one accounting constant changed yields different attributes through the oracle (the model is what is evaluated). |
| D-2 | The generation of record: datasets and ledger entries from a clean checkout (a separate git worktree at a named commit), produced in the container of record; the same produced natively on this machine for comparison. |
| D-3 | `examples/adcs/experiments/reports/swap-evidence.md`, generated: the three comparisons of G2; the list of paper numbers with old and new values; a one-paragraph reading. |
| D-4 | `case.py` and the paper's generators on the generation of record; the provenance exposed for Appendices C and F; the tie test of G4. |
| D-5 | `WP16-decisions.md`: the driver's call to swap or not, with the evidence, and the stop condition's outcome. |

## Requirements

| ID | Requirement | Checked by |
|---|---|---|
| R-1 | The mutation check fails if the oracle ignores the model. | the test, shown failing against a stub |
| R-2 | No ledger entry of the generation of record is dirty; each names its commit, platform and container image id. | a test on the ledger |
| R-3 | `swap-evidence.md` lists every difference between the three generations with size and cause, and every number, table and figure of the paper as unchanged or changed. | generated; inspection by the driver |
| R-4 | **Stop condition.** If any conclusion stated in the paper, or any facet's leading metrics, sign of a tension, selected K or certificate status, differs between generations, execution stops and the driver takes it to the supervisor. | the driver, from D-3 |
| R-5 | The frozen files are unmodified (their sha256 as at `main`), and a test ties them to the generation of record (equal, or within the stated tolerance with the differing columns named). | tests |
| R-6 | The suite, lint, format, lock and the lemma chain pass; no AI attribution. | local checks; the container; CI |

## Definition of good enough

D-1 to D-5 delivered; R-1 to R-6 pass; the swap is made if R-4's stop condition is not met and is
not made, with the reason recorded, if it is.

## Agent's defaults

- If the container's generation differs from this machine's only within the reproducibility
  tolerance and no paper number changes at its printed precision, the container's generation is the
  generation of record (the container is the environment of record) and the difference is stated
  in Appendix F.
- If generating in the emulated container is too slow to be workable, the generation of record is
  produced natively from the clean checkout, the container reproduces a stated sample of it, and
  that is said in Appendix F.
- The generation of record lives in `examples/adcs/data/v2/`.

## Amendment 1 (2026-11-09, the driver, under the mandate): the times read off the step sequence

Why: `work-packages/swap-evidence.md` found that `settling_time_s` and `slew_time_s`, two of the ten
fitted attributes, are read off the accepted steps of the adaptive integration and move by up to
1.3 percent (0.48 s) under perturbations of one unit in the last place.

- **G5 (new).** The sensitivity of the paper's conclusions to that quantization is measured, not
  assumed.
- **D-6 (new).** Each of the two cubesat datasets regenerated five times through the clean oracle
  with the four continuous design variables perturbed by a relative 1e-12 (seeded); for each
  regeneration the case module's one-term fit (temperature re-selected), the K = 2 and K = 3 fits,
  the regime comparison, the nondominated counts and propose-predict-check; a generated section of
  `swap-evidence.md` with, per quantity the paper reports, the committed value, the range over the
  regenerations, and whether it changes at the paper's printed precision. No Docker.
- **R-7 (new).** The section lists the per-column deviation of every fitted attribute between
  regenerations; states for the contending set, the leading metrics of each facet, the signs of the
  tensions, the selected temperatures, the certificate statuses, the regime comparison and the
  check designs' outcomes whether each is identical across regenerations; and the stop condition of
  R-4 applies to it. Checked by the driver from the generated section.
- **For the supervisor, with that evidence:** whether the two times stay as read off the steps
  (data unchanged; the quantization named as a gap with its measured effect) or are measured by the
  integrator's event detection (reproducible to rounding; the data and every number change).
- **Tolerances.** `torque_saturated_frac`: absolute 0.01, no relative term, in every test that
  compares it. The two time columns keep their absolute allowance until D-6 gives the evidence to
  set it.

## Amendment 2 (2026-11-09, drafted by the PM for the driver's approval)

Status: DRAFT; approved only by the driver's recorded approval in `WP16-decisions.md`. Nothing below is executed before then.

**Why.** Amendment 1's spike (`work-packages/swap-evidence.md`, "Sensitivity of the conclusions to the
step-quantized times") found `settling_time_s` and `slew_time_s` read off the accepted steps of the RK45
integration (`adcs_sim.simulate_adcs`; `_last_outside` and `_first_inside` in
`experiments/cubesat_oracle.py`): under a relative 1e-12 jitter they move by up to 0.49 s, and design 763's
slew time jumps from 33.44 s to 12.53 s where its error trajectory grazes the band. The supervisor, verbatim:
"event detection and regenerate. i also want to note that i do expect changes of this order of complexity due
to the sysmlv2 model refactor. there may be others. focus on ensuring the integrity of the process so we can
justify or bound our claims relative to the methods and data we have." The driver's disposition (same record)
fixes the order and the item-by-item check below.

**New goals.**

- G6. The simulator reads the two crossing times by event detection (scipy `solve_ivp` events on the
  attitude error minus the threshold, located on the dense interpolant: slew time the first entry into the
  band, settling time the last exit above the settling fraction) *(mechanism: default)*, reproducible to rounding.
- G7. The datasets, the K = 1, 2, 3 record, the check designs and the paper's numbers regenerated on the new
  model (WP22's model, adopted as `model_v2/cubesat.sysml`) inside the container of record (`hts-paper`), after the WP22 gate records
  the model swap.
- G8. The comparison report at the data gate lists every change with size and cause, and checks the
  conclusions item by item (contending sets, leading metrics, signs of tensions, selected temperatures,
  certificates, check outcomes, counts, feasibility flags); R-4's stop condition applies. G4 is unchanged:
  the frozen generation stays the cited comparison.

**Order** (the driver's disposition: "WP22's model with the event-detection change in the simulator, the
ledger's new version; then the v2 regeneration; then the gate and the swap; then the paper's regeneration in
the container"): (1) event detection in the simulator and a new ledger version on the WP22 model; (2) the v2
regeneration; (3) the data gate and the swap; (4) the paper's regeneration in the container.

| ID | Deliverable | Serves |
|---|---|---|
| D-7 | Event-detected times in `adcs_sim.py` and the oracle's read-off, with their tests | G6 |
| D-8 | New ledger entries (`@n+1`, not dirty, naming commit, platform, image id) and `examples/adcs/data/v2/*` regenerated in `hts-paper`; the K = 1, 2, 3 record (`k_terms.py`), check designs and container record (`paper/container/RECORD.md`, `tests/data/v2_first_designs_of_record.csv`) | G7 |
| D-9 | The comparison report, generated into `swap-evidence.md` (new section), and the gate decision in `WP16-decisions.md` | G8 |

| ID | Requirement | Checked by |
|---|---|---|
| R-8 | Event-detected times are continuous where the step-read ones jumped: design 763 under the five seeds of D-6 moves by rounding only | a test on design 763 |
| R-9 | Under the 1e-12 perturbation of D-6, both times move by at most rounding (relative 1e-9 *(default)*) on the six check designs | a perturbation test |
| R-10 | The ledger carries the new version; the container record names the image id; no entry dirty | the ledger test; `RECORD.md` |
| R-11 | The report lists every change with size and cause and each conclusion of G8 as identical or changed | generated; the driver's inspection |
| R-12 | The mutation check (D-1, `tests/test_mutation_v2.py`) passes on the new model | the test |

**Non-goals.** No change to the physics other than how the crossing time is read (the saturation fraction
stays step-based with its 0.01 tolerance); no change to sampling, seeds or scenario constants; no edit to the
accepted records of WP7, WP9, WP13; nothing moves before the WP22 gate decision is recorded.

**Dependencies.** The WP22 gate (model swap recorded); the container of record `hts-paper`
(`paper/container/README.md`); Docker limits: `hts-*` names only, nothing under `~/.colima` or `~/.docker`, no
`--platform linux/amd64`.

**Good enough.** D-7 to D-9 delivered; R-8 to R-12 and R-6 pass; the swap made if R-4 is not met, held and
taken to the supervisor with the record if it is.

**Blast radius.** `examples/adcs/adcs_sim.py`, `examples/adcs/experiments/cubesat_oracle.py`, their tests
(`tests/test_cubesat_oracle.py`, `tests/test_cubesat_model.py`, a new event-detection test), the ledger module
and `ledger.jsonl`, `examples/adcs/data/v2/*`, `k_terms.py` and the check-design generators, the paper's
generators (`paper/generate_results.py` and the ones that read the data), `RECORD.md`, the record test data,
`swap-evidence.md`; Appendix C and F text only through the paper stream.

**Agent's defaults.** The event mechanism above; the rounding bound of R-9; the report as a new section of
`swap-evidence.md`; the new ledger ids follow `ledger.rerun` (`<id>@<n>`).

**Open decisions (for the driver).**

- **OD-A.** Event detection removes the sub-step part but not the grazing (a trajectory touching the band
  within rounding still flips the first entry). Is the grazing discontinuity reported as the remaining part of
  gap G-17 in the abstraction-gaps ledger, as the driver began — options: yes, G-17 narrowed to the grazing
  case with the new measurement / no, the definition of slew time changes (for instance a hold time) and
  that is taken to the supervisor.
- **OD-B.** The frozen datasets' tie test (R-5) can no longer hold within 0.5 s in the two time columns
  (design 763 alone differs by about 20 s) — options: a tolerance set from the regenerated evidence / the tie
  states "differs in the two time columns, listed" and asserts equality elsewhere.

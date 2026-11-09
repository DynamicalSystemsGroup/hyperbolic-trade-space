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

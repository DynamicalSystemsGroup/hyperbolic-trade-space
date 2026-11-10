# WP16 — Decision records (the data swap)

Records typed by the driver. This package is defined and approved by the driver under the
supervisor's mandate (`release-candidate.md`: "you can define and accept scopes to get to something
you believe i will expect"); the calls below are the driver's, for his review at the PR.

## Origin

- **Supervisor (mzargham), verbatim (WP15):** "do it in parallel to start but eventually i'd like to
  be able to swap over onto the new data".
- **Supervisor (mzargham), verbatim (2026-11-08, the 0.1 candidate):** "Swap for 0.1 if the evidence
  supports it".

## The driver's calls

- **2026-11-08. Scope defined and approved** (`WP16-scope-of-work.md`). Basis: the PM reported the
  four new datasets byte-identical to the frozen ones; the driver confirmed the sha256 values
  itself. Because identity on one machine does not show that the clean model is what is evaluated,
  nor what the container of record produces, and because the ledger entries were written from a
  tree with uncommitted work, the scope asks for a mutation check, a generation from a clean
  checkout in the container, and a three-way comparison before the swap is made.
- **2026-11-09. Tolerance for the saturation fraction, set from evidence.**
  `work-packages/swap-evidence.md` (d177964) shows `torque_saturated_frac` is a count of
  integration steps divided by their number (24 of 1343 for one design), a diagnostic column and
  not one of the ten fitted attributes; a relative perturbation of 1e-15 in the inputs moves it by
  whole steps; over 60 perturbed re-runs it deviates by at most 0.0080 and the two CI runs lie
  inside that range; the four feasibility flags never change. Call: the column is compared with an
  **absolute tolerance of 0.01 and no relative term**, in every test that compares it (the check
  designs and the first-twenty tests), with the reason stated in the test. This replaces a relative
  tolerance that was wrong in kind, and loosens nothing that is fitted.
- **2026-11-09. A finding in the same evidence, and a spike before the swap is decided.** Two of the
  ten fitted attributes, `settling_time_s` and `slew_time_s`, are also read off the step sequence
  (the first or last accepted step at which the error crosses a threshold). Under the same
  rounding-level perturbations they move by up to 1.3 percent, 0.48 s, against a test allowance of
  0.5 s. The paper's numbers are unaffected in themselves, because the paper reads committed files;
  but a generation produced on another platform differs in two fitted columns at the percent level,
  so "the evidence supports the swap" now needs a further piece. Scope amended (below, G5 and R-7):
  regenerate each dataset several times under rounding-level perturbation, refit each, and report
  whether any conclusion moves. Stop condition unchanged: if one does, it goes to the supervisor.
  Whatever the outcome, the quantization of the two times is named as a gap, with its measured size.
  Replacing the read-off by the integrator's event detection would remove the effect and change the
  data; that is a choice between keeping the accepted records' numbers and a cleaner measurement,
  and it is taken to the supervisor with the spike's evidence, not decided here.
- **2026-11-09. The sensitivity spike's result (2d40fa2), and what goes to the supervisor.** Five
  regenerations of each dataset with the four continuous inputs perturbed by at most 1e-12, each
  refit; an unperturbed control reproduced the committed files exactly. **Identical in all five and
  in the committed data:** the contending sets at K = 1 and on each facet at K = 3, in both regimes;
  each facet's leading metrics; the signs of the six reported tensions; the selected temperatures at
  one decimal; the certificate statuses; every check design's pass or miss; all four feasibility
  flags of all 2000 designs; the count of 671 of 706 nondominated on ten attributes. **Not
  identical at the printed precision:** the nondominated counts on reduced views (146 becomes 145;
  8 becomes 7; 157 becomes 158); the K = 3 facet shares (0.089, 0.133, 0.778 range over 0.065 to
  0.087, 0.136 to 0.152, 0.761 to 0.795, order unchanged); the effective sample size, one
  near-frontier count and five association values in the second decimal; the solver's numerical
  residues. **In the data:** settling and slew time move by up to 0.49 s, and one design's slew
  time jumps from 33.44 s to 12.53 s because its error trajectory grazes the settling band.
  Reading: R-4's stop condition as written (a conclusion, a facet's leading metrics, a sign, a
  selected K, a certificate status) is not met; but numbers the paper prints are not reproducible
  to the precision printed, and one fitted attribute is discontinuous in the design. The driver
  had said this choice would be the supervisor's and puts it to him: keep the data and the
  measurement and report at the precision that is reproducible, with the effect named as a gap; or
  measure the two times by the integrator's event detection and regenerate everything (which
  removes the sub-step part and not the grazing).
- **2026-11-09. Done meanwhile, because it is needed under either answer.** (1) A new entry in the
  abstraction-gaps ledger for the times read off the step sequence and the band-grazing
  discontinuity, with this evidence. (2) The paper prints no number to a precision at which it is
  not reproducible: the fragile quantities carry their range over the perturbed regenerations, and
  numerical residues are printed as bounds. (3) The saturation fraction's absolute tolerance is
  applied in the older first-twenty test as well. The swap itself is held: no file moves and
  `adcs_sim` is untouched until he answers.

## The step-read times, decided (2026-11-09, before the supervisor stepped away)

- Driver's question: keep the data and report ranges / event detection and regenerate / decide later.
- **Supervisor (mzargham), verbatim:** "event detection and regenerate. i also want to note that i do
  expect changes of this order of complexity due to the sysmlv2 model refactor. there may be others.
  focus on ensuring the integrity of the process so we can justify or bound our claims relative to
  the methods and data we have. all models are wrong and some are useful. our focus is being
  demonstrably useful for a trade study that supports decision analysis/design optimization over
  part swapping and param tuning against a handful of metrics."
- **Disposition:** WP16 is unblocked. The simulator reads the crossing times (settling, slew) by event
  detection instead of the integrator's accepted steps; the datasets, the K = 1, 2, 3 record, the
  check designs and the paper's numbers are regenerated on the new model (WP22) inside the
  container of record; every change is listed in the comparison report at the data gate; the
  conclusions are checked item by item (contending sets, leading metrics, signs, certificates,
  check outcomes, counts) and any that changes is interrogated and resolved, or brought to him with
  the record. Order: WP22's model with the event-detection change in the simulator, the ledger's
  new version; then the v2 regeneration; then the gate and the swap; then the paper's regeneration
  in the container. His framing of what the work is for is the test of every claim: demonstrably
  useful for a trade study over part swapping and parameter tuning against a handful of metrics,
  with claims justified or bounded by the methods and data.


## Amendment 2 approved (2026-11-09, 20:20; the driver under the mandate, for the supervisor's review)

Draft at f7d180d (`WP16-scope-of-work.md`, "Amendment 2"), on the adopted model `cubesat.sysml` (the WP22 swap,
`WP22-decisions.md`). The supervisor's direction it executes: "event detection and regenerate" (above); he expects
changes of this order from the model refactor.

- **OD-A** (event detection removes the sub-step part of the slew-time defect but not the grazing case; design 763
  goes from 33.4 s to 12.5 s): report it as gap G-17 narrowed to the grazing case. No redefinition of slew time (a
  hold time) now: that changes a measured quantity's meaning and is his call; it goes under "Waiting for the
  supervisor" in the driver log with the design-763 evidence.
- **OD-B** (the frozen tie test R-5 cannot hold within 0.5 s in the two time columns): state what is true: "differs
  in the two time columns, listed" with equality elsewhere. No tolerance read off the regenerated evidence: a bound
  chosen from the data it has to pass is tuning to the test.
- **Agent's defaults** accepted as one item: `solve_ivp` events on error minus threshold (slew time the first entry
  into the band, settling time the last exit), rounding bound rel 1e-9, a new section of `swap-evidence.md`, ledger
  ids `<id>@<n>`. The draft's `cubesat_r1.sysml` references become `cubesat.sysml` on execution.
- Good enough as drafted; the regenerated datasets, the K = 1, 2, 3 record and the paper's numbers regenerate in the
  `hts-paper` container with their tests passing in the same push; a Linux dispatch at the gate; the data-gate
  comparison (old against new numbers, every moved number listed with its cause) is the delivery I verify.

## Slew time under event detection (2026-11-09, 20:50; OD-A of Amendment 2, put to the supervisor)

**Driver's question (popup):** event detection removes the sub-step part of the defect but not the grazing case
(design 763: 33.4 s to 12.5 s). Options: First entry (as approved) / Hold time / Decide in WP23. **Supervisor
(mzargham), verbatim:** "we want the hold time one but its really the "settling time" in control laguage"

**Disposition (pending one clarification):** the quantity wanted is the hold time, which in control language is the
settling time: the first time after which the pointing error stays inside the band. The case model already names a
settling time (event detection computes it as the last exit from the band, the same quantity) and a slew time (first
entry into the band, the grazing-prone one). Whether the case keeps two time metrics or one is a dataset-column
question and goes to the supervisor next, then into WP23's scope.

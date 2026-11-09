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

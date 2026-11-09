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

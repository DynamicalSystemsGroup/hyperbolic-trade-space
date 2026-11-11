# WP31 — Decisions (choosing K in the documentation)

The supervisor's words are quoted verbatim where they bind; the driver's calls are listed for his review at the PR.

## Origin

The supervisor, 2026-11-10, verbatim in `driver-log.md` ("Choosing K in the documentation").

## Stage (2), the driver (2026-11-10, 23:30; readout `WP31-readout.md` at 8386f44, 18c258c)

- **Placement A: a new user-guide page "Choosing K"**, between Fitting and Tensions, by a contract amendment adding it
  to `docs.pages`; the fitting page's "Choosing K, the temperature and the band" section shrinks to a pointer (net
  negative there). The question is one a user asks on its own, and the supervisor asked for methods and examples both.
- **The page's content, from the readout:** methods first, each with what it can and cannot do: the mean slack at one
  fixed temperature (falls with K by construction, so it never chooses alone; an elbow where there is one, as the
  stock regime at K = 3, and none where there is not, as the primary regime); the planted-recovery check as the
  method's own test (terms found at K0, extra terms spurious); the resampling splinter check with its noise stated
  (it jumps past K0 on planted tables and is noisy on the cubesat); the certificate and the term share as readings
  of a fit, not selectors; what large K does on our data (from the sweep: the per-term cells thin, the stable radius
  shrinks, the n-lemmas fragment), stated from the sweep and the lemmas, not by analogy. Then two worked examples:
  a planted table (K0 = 2 and 3) and the cubesat, both regimes. The PCA elbow heuristic named once as kin, with the
  sentence that our large-K limit differs and how. No held-out criterion is claimed, since none exists in the package.
- **The 0.31 sentence** on the fitting page does not reproduce (0.55 with fresh draws): the first unit replaces it
  with what the check shows across seeds (the spread stated, or the number dropped), a narrowing that lands before
  the page; the page then carries the re-measured statement with its seeds.
- Stage (4): three task readers ("choose K for this table and say why") on the staged page; stages (5) and (6) as
  usual; the glossary, the register and the ledger follow.

**Driver, verbatim:** "WP31 stage 2: placement A, the fitting section to a pointer, the 0.31 sentence corrected first,
the page built from the readout's methods with their limits stated and two worked examples; the elbow named once."

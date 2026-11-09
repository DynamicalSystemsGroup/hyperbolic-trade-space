# WP11 — Decision records (readability and correctness loops)

Records typed by the driver. This package is defined and approved by the driver under the
supervisor's mandate (`release-candidate.md`); the calls below are the driver's, for his review at
the PR. The supervisor's words on the grid and the personas ("Use these six") are in
`WP10-decisions.md`, "The reader grid".

## The driver's calls

- **2026-11-09. Scope defined and approved** (`WP11-scope-of-work.md`). Basis: the grid and protocol
  note; the first cold reads (`WP10-cold-reads.md`), which showed that fresh readers given only a
  slice produce specific, checkable findings, and that one reader per cell is enough to start if
  replication is read across cells. Added to the note's protocol: the answer key is kept out of the
  repository while the loops run and its hash is committed first; six core cells are held out by a
  seeded draw; at most four rounds before reporting non-convergence.

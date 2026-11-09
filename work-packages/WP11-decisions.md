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
- **2026-11-09. The answer key is fixed; its hash and the held-out draw, committed before any persona
  read.** Answer key version 1, written by the driver from the recorded story, the outline, the
  register and the accepted results, and kept outside the repository: sha256
  `4fdbaefd37ab13e8e490380c40685b2b8c26088cd1f69299773db823a51b90bf`. If the supervisor's pending
  choice on the two step-read times changes a fact in it, a new version is made before the next
  round and its hash recorded here beside this one. Held-out cells, one core cell per persona, by
  Python's `random.Random(20261109).choice` over each persona's core depths in the grid's order:
  P1 at L-A, P2 at L-A, P3 at L-D, P4 at L-C, P5 at L-D, P6 at L-B.
- **Correction.** The grid has 24 core cells and 6 edge cells; the note, the scope and the driver's
  report to the supervisor said 23. Round 1 therefore reads 18 core cells and three edge cells.

## Answer key, version 2 (2026-11-09, 17:50)

- The triager (the driver) updated the key for the supervisor's decisions of the day (elasticity for
  exchange rate; the fit stated without membership; depth A is the title and abstract since the
  three-pane figure left the paper's body; posynomial as the model class; the data as what is
  modelled; the two named uses). Held outside the repository as before. SHA-256 of version 2:
  `e72f3eeac76089d8657add60ac1b7553ac8fcfd022cc6cb0b69fb050931ad638`. Round 1 begins with the L-A and L-B cells of all six personas on the staged paper at
  20fa550, the stable part of the paper while the narration and figure passes run.


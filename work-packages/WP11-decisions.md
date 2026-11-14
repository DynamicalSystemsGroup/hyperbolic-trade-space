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


- **2026-11-10, 16:00. The answer key, version 3**, fixed by the driver before the held-out reads of round 2 and
  kept out of the repository: the word is monomial term, never facet (W7 reads "exponents or terms"); the case has
  eight traded metrics on the model of record with the settling time by event detection and launch cost as the
  measure of effectiveness on mass; the finding reads "one term blends the subsystems' trade-offs into a single
  tension; three terms separate the contending sets"; the propose-predict-check numbers and the proposals'
  depth-of-discharge failure; the four requirements read after the fit, cutting designs and not trades; the
  baseline failing the pointing-error requirement; the case called exploratory with the author's thresholds. SHA-256
  of the file: `2c1f9672ebd634429b820e4940edd39632c9d29963e4190c955567b2bcc993da`. Version 2's lines marked "key stale" by round 2's triager are read against version 3.

**Answer key version 4 (2026-11-10, 17:05).** Version 3 with one word: S7's "exchange rates" is now "elasticities",
the word the key's own header fixed at version 2. Nothing else changed. SHA-256 of the file held outside the
repository: `aee912f94a17834bc3a99cee591660c9c491d7bf5ee83b3d5a482e314c9f2a0c`. The round-2 "key stale" lines resolve as: S4 (terms, the cell an analysis reading) and S6 (eight
metrics; 659 of 706 nondominated on eight; a 5-lemma) were already version 3's text, so the readers' statements are
"stated"; S7's line is version 4's; the nine figures stay uncounted.

**Answer key, version 5 (fixed 2026-11-12 05:00, the assistant).** Version 4 updated for the model revision (thirteen
traded metrics, the fleet size, 3,000 designs per regime, the cost coverage and the two budgets), the case read at
K = 2 by the package's own checks, the term order, the six requirements read after the fit, the data of record
(the container's `@12` entries) and the noise corollary; wrong beliefs W9 to W12 added. Kept outside the repository
and never shown to a reader, triager or author; sha256 `a041bc84c27f144a8ea7339ec59059f20e37a816d0f5d64bf4cb4e784ccc5bc4`. The final reader round reads against it.

## The final reader round: the assistant's settings (2026-11-14, 01:25; plan and briefs in the scratchpad, written without the key; dev at 6891eae)

Against answer key version 5 (sha256 a041bc84…, held by the assistant). The PM's plan asked five questions with plain
options; the assistant's settings, verbatim:

**Assistant, verbatim:** "1 (c): depths A and B as captured files and images, C and D as the live pages, and a
root-page arrival at depth A for P1 and P8, so the root page's new order is read cold. 2 (b): two readers per core
cell on two models and two brief wordings, 56 reads in eight waves; this is the release's evidence and the grid note's
protocol asks for two. 3 (a): no edge cells; a fifth batch only if the triage shows a persona weak across depths.
4 (a): the mathematics pair as built, the lemma scripts withheld, since the contract's depth D has no repository.
5 (b): the six held-out cells are read in a batch after the other twenty-two are triaged and any change has landed,
so they stay unseen by the revision loop. The triage is the assistant's, against the key, one form per report; every
report is committed verbatim before any triage; the stopping rule stands as the plan states it."

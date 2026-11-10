# WP11 round 1, the L-A and L-B cells: triage (the driver, 2026-11-09, 18:10)

Read: the staged paper at 20fa550. Twelve fresh readers, six personas at depth A (title and abstract)
and six at depth B (headings, the main-results list, the boxed statements with proofs withheld, the
figures and their captions). Reports verbatim in this folder; slices beside them. Marked against the
answer key, version 2 (hash in `WP11-decisions.md`), which stays outside the repository.

## Recall (what the depths owe)

| Owed | Depth A, of 6 | Depth B, of 6 |
|---|---|---|
| The problem and the idea (tensions, not variance; a fitted surface gives the data a coordinate system) | 6 stated | 6 stated |
| Elasticities as what a facet reports | 6 stated | 6 stated |
| The surface is not the Pareto boundary; the method does not pick a design | 6 stated | 6 stated |
| Kin to PCA and chained with it, not a replacement | 4 stated; 2 read it as an alternative or replacement | 5 stated; 1 asked for a comparison on the same data |
| The finding of the case in one sentence | 0 of 6: every reader said the case sentence gives no result | 6 stated it from the main-results list ("facets separate contending sets that one facet blends") |
| The three levels of guarantee (depth B) | not owed | 6 stated, with "not claimed" phrases quoted |
| Two or more things the method does not claim (depth B) | not owed | 6 stated |

## Wrong beliefs (the worst outcome of a read)

- **The surface read as a regression through the middle of the cloud** (depth A: the optimization
  reader and the sceptical neighbour; depth B: the sceptical neighbour, "a statistical fit through the
  cloud"). The abstract says the surface "models the data" and never says it sits at the data's
  outer edge as a soft supporting surface. One reader at depth B then noticed "many points lie above
  the line, so this is clearly not a frontier", which is the right observation without the words to
  place it.
- **PCA replaced rather than joined** (two readers at depth A). The abstract's sentence on PCA
  ("mirrors the structure of PCA as an unsupervised learning method") no longer says kin and chained.
- **A facet read as a cluster of designs** (three readers at depth B guessed "facet" as a cluster or
  segment of designs). The boxed statements still carry membership language ("reassigning each row
  to its maximizing facet", "rows assigned") and nothing at depth B says a facet is a piece of the
  surface, not a set of designs.

No reader believed that the method picks the design, that a certificate proves a global optimum,
or that the case validates the method on hardware.

## Friction (replicated across readers)

- "Energy differential": guessed by 12 of 12. The abstract's gloss ("its level relative to the
  surface") and Definition 2's analogy did not land; one reader objected that the paper itself says it
  is not an energy. The glossary holds a second name for the same object, "level offset".
- "The table and its reading are views": stopped 3 of 6 at depth A.
- "Modelling a single n-lemma fits a monomial, which transforms into a convex program": lost the
  two non-mathematical personas at depth A; the GGP and kernel clause was opaque to 5 of 6,
  including the optimization reader ("a kernel that keeps that compatibility").
- "The unit level set of a degree-one weighted geometric mean" (the main-results list): stopped
  2 of 6 at depth B; the glossary's words for the same object are plainer.
- Terms guessed at depth B by three or more readers: reach, share, support, "stock" and "primary"
  regimes, tau; and "6-lemma" read as odd for a "lemma" by two.
- One reader at depth A could not tell what inputs the method needs (positive, larger-is-better);
  one at depth B could not tell what the model supplies and what the analyst does.

## Figures (cold reads of the images, depth B)

- Helped most, 6 of 6: Figure 2, the log-metric planes of the one-term fit ("a scatter sloping down
  with one line through it: a visible trade-off"). Figure 5, the association heatmaps, helped the
  optimization reader most and was called dense by three others.
- Helped least: Figure 4, the chart of the three-term fit ("coloured dots on unexplained Z
  coordinates", 4 of 6); Figure 7, predicted against measured positions ("could not tell good from
  bad", 4 of 6). Figures 5 and 6 carry an unexplained "w = ..." for two readers.

## Change requests (to the paper stream unless noted; structural, not polish)

- CR-1 (abstract, with the supervisor's wording kept where it is his): one clause saying the surface
  is fitted as a soft supporting surface at the data's outer edge, not a regression through it; the
  PCA sentence says kin and chained; the case sentence carries the finding (one facet reports one
  tension; three facets separate three contending sets across the subsystems); "the table and its
  reading are views" said more plainly or dropped; the kernel clause shortened or dropped.
- CR-2 (the main-results list): the glossary's words in place of "the unit level set of a degree-one
  weighted geometric mean"; one item that PCA is chained (D.16).
- CR-3 (statements and captions at depth B): a facet is a piece of the surface, said once where
  "facet" first appears in the statements; "reach", "share", "support" and the two regimes glossed at
  first use in a caption or statement; the sharp-limit sentence of Theorem 11 kept but "label"
  wording so that a facet is not read as a set of rows.
- CR-4 (figures; to WP19's slot list, as evidence): Figure 2 is the anchor and earns its place;
  Figures 4 and 7 fail the cold read as drawn; the "w = ..." annotations of Figures 5 and 6 need a
  caption clause.
- CR-5 (a term decision for the supervisor, recorded under "Waiting for the supervisor"): "energy
  differential" was guessed by every reader; the glossary's alternative name is "level offset".
  Options when he is back: keep the term and gloss it at first use in the abstract; or make "level
  offset" the term and "energy differential" the analogy named once. The driver's recommendation:
  the first, since the term carries his reading of V as a potential and the gloss can be one clause.

## Round 1b (re-test of the abstract, depth A, after CR-1 landed at 60b1576; staged build 7f162c6)

Four readers (P1 decision maker, P3 systems engineer, P5 ML practitioner, P6 sceptical neighbour),
abstract only, cold, reports in the driver's scratchpad (`readers/round1b/P{1,3,5,6}-A.md`).

- Gone: the surface read as a regression (0 of 4; all four now state it is not a regression and
  not the Pareto boundary). The elasticity reading is correct in all four and every reader
  would read on. No reader believes the method picks a design.
- Still wrong (W4 of the key): 4 of 4 read the method as an alternative to PCA ("a cleaner
  alternative to PCA", "replacing PCA-style summaries", "as an alternative to PCA" twice). The
  key says kin and chained, not a substitute. The current wording that produces it is the
  opening contrast ("explains variance, not trade-offs. We explain tensions.") followed by
  "mirrors the structure of PCA", which says kin but not chained; CR-1's "kin and chained" clause
  did not land.
- Not stated: the finding. The closing clause "a single facet gives one tension, several separate
  sets" was named as confusing by 3 of 4 ("the ending told me little"). CR-1 asked for the finding
  in the case sentence; it landed too compressed to be read.
- Confusing in 4 of 4: "the table and its reading are views" (the supervisor's reading; needs its
  object, a model, named) and "energy differential" (CR-5, with the supervisor).
- Asked for by P5 and P6: what "soft supporting envelope" is mathematically. No change: the
  abstract carries the words and Definition 1 the mathematics; a depth-C re-test will say
  whether the definition answers it.

Change request CR-1b (paper stream; the supervisor's sentences kept, the smallest edit to each):

- The PCA sentence says chained as well as kin: "Our implementation mirrors the structure of
  PCA as an unsupervised learning method for feature engineering, and the two chain." (his earlier
  wording "the two chain", which the main-results list already carries as item 5).
- "the table and its reading are views" names its object: "the table and its reading are views
  of that model."
- The case sentence carries the finding in the main-results list's own words, which Section 9
  backs: "On a cubesat model coupling power, mass and attitude control, one facet blends the
  subsystems' trade-offs into a single tension; three facets separate the contending sets."
- Re-test at depth A (the same four personas) once it lands; the depth-B re-test runs now on the
  current build, since CR-2 has landed (main results in the glossary's words; item 5, PCA chained).

## Next

Re-test the L-A and L-B cells after CR-1 to CR-3 land; then the L-C and L-D cells (main text; with
appendices) once the section 4 and 6 narration is in; the docsite's task readers alongside.

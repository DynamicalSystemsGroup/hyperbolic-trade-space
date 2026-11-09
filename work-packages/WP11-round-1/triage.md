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

## Next

Re-test the L-A and L-B cells after CR-1 to CR-3 land; then the L-C and L-D cells (main text; with
appendices) once the section 4 and 6 narration is in; the docsite's task readers alongside.

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

Four readers (P1 the accountable decision maker, P3 the modeller, P5 the optimization reader, P6 the sceptical neighbour),
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

### Round 1b, depth B (six readers, skim of the current build 7f162c6: headings, main results, statements, captions, figure images)

Reports in the driver's scratchpad (`readers/round1b/P{1..6}-B.md`); slice `readers/round1b/slice-B.md`.

- Held: no reader believes the surface is the Pareto boundary or that the method picks a design;
  elasticities read correctly by 6 of 6 (three in their own words, "exchange rate"); the hedged
  statements raise trust in 4 of 6 ("makes me trust it more than the usual method paper"); 6 of 6
  would read on, selectively (P1 and P2 to Sections 8 to 11, P4 and P5 to Sections 5 and 6, P6 to
  Section 2, Appendix G and Section 9). The "w = ..." boxes of Figures 5 and 6 are now read from the
  caption (CR-4's clause landed). Figure 1 is read as the temperature selection by 4 of 6; Figure 2
  remains the anchor for the practitioners; Figure 3's kink is where two readers first believed the
  facets mean more than a colouring.
- Not landed (CR-3 stays open): a facet is still read as a set of designs by P1 ("a sub-group of
  designs"), half so by P2 and P4 ("one plane, i.e. one family of designs"; "one hyperplane or cluster");
  P3 and P6 read it as a piece of the surface from Figure 3's bent line. The statements still carry no
  sentence saying what a facet is where the word first appears.
- New, CR-6 (statements, Definition 1 or the main-results lead): 3 of 6 (P1, P4, P6) understood that
  the reference surface is not the Pareto boundary and then did not know what it is for ("I understood
  the negative but not what I am supposed to do with a surface that is not the frontier"; "made it sound
  like a quantile"). One positive clause is owed where the negative stands: the reference surface is
  the level from which every design's position and level, and each facet's elasticities, are read.
- New, CR-7 (Definition 4): the band sentence "in the soft maximum a design inside it weighs within a
  factor e of one on the surface" lost 3 of 6 (P1, P2, P3: "I do not know what a soft maximum is or why
  a design 'weighs' anything"). Say it in the fit's own words (the fit counts a design inside the band
  almost as much as one on the surface) or move the weight clause to the remark that the new lemma
  step (U05-C009) backs.
- New, CR-8 (Definitions 2 and 7; glossary): β is "a fitted offset" in Definition 2 and "the reach, the
  support value of the data in direction w_k" in Definition 7; P3 and P5 could not tell whether these
  are one quantity. One object, one name: the glossary's term for β at both places, and "support value"
  glossed or dropped. P5 also asks in what sense a facet "dominates" a design (Definition 7): use the
  cell wording of ruling 2 (the facet whose term is largest for that design).
- To WP19 as evidence (CR-4 holds): Figure 4 least helpful for 2 of 6 ("I saw clusters by colour but
  took nothing from it I could repeat"); Figure 7 least helpful for 2 of 6 and read by all as
  "predictions matched measurements for three proposed designs" with no sense of what was proposed,
  why there are two panels, or what a bad position would look like. Figure 3's bottom panel shows a
  metric quantised into horizontal bands; P3 and P6 inferred a discrete design variable and noted that
  nothing they read says so: a caption clause naming the discrete alternative behind the bands.
- Observation for the paper stream's judgement, not a forced edit: P6 (the sceptic) will decide at
  Section 9 whether "facets separate contending sets that one facet blends" is a finding or a
  restatement of "clusters have different correlation structure", which Figures 5 and 6 (association
  heatmaps) make them suspect. Section 9 should say what the facets give that a clustering with
  per-cluster correlations does not: the fitted exponents and elasticities per facet are the model's
  reading; the heatmaps are the analysis. Keep the two apart in that section's prose.

### Round 1c (abstract, depth A, after CR-1b landed at 85733c1; four readers P1, P3, P5, P6)

Reports in the driver's scratchpad (`readers/round1c/P{1,3,5,6}-A.md`).

- Landed: the finding is read (P1: "a single-facet fit smears three subsystems' trade-offs into one,
  while a three-facet fit pulls them apart"; P3 and P6 restate it); "facet" is now guessed right by 4 of 4
  (one term of the posynomial, a face of the surface), where round 1b had it as a cluster; the regression
  reading stays gone; elasticities right in 4 of 4; 4 of 4 read on.
- Held for the supervisor (unchanged): PCA read as an alternative or replacement by 3 of 4; "energy
  differential" questioned by 4 of 4 ("the physics word made me wonder").
- New, CR-1c (the driver's own clause from CR-1, not the supervisor's wording, so free to change): "It is a
  soft supporting envelope of the data, not a regression" confused 4 of 4 next to "models the data ...
  not the Pareto boundary": an envelope sounds like a boundary (P3), the two sentences read as
  contradictory (P5: "if it models the data rather than the boundary, I do not see why the elasticities
  should be trade-off rates"), "soft" is unexplained (P1, P6), which side it sits on is unsaid (P6). Replace
  with the plain picture: "It is fitted to the outer edge of the data, not through its middle: a soft
  support, not a regression." The body defines "soft" (the temperature); the abstract need not.
- Stop rule for the abstract: after CR-1c lands, one more depth-A pass; if the only remaining confusions
  are the two items held for the supervisor, the abstract rests until he is back.

Note (2026-11-09, 21:00): figure numbers in the records above are those of the build before 8abb16a; the three WP19 placements renumber every earlier figure by +3 (old Figure 1 is Figure 4, old Figure 2 is Figure 5, and so on).

### Round 1d (abstract, depth A, after unit 7 at 35b3df6: the energy gloss and the PCA rewording; P1, P3, P5, P6)

Reports in the driver's scratchpad (`readers/round1d/P{1,3,5,6}-A.md`).

- Resolved: PCA is no longer read as replaced (P1: "It does not replace PCA; the authors say the two answer
  different questions and can be used together"; P6 names the composition as a testable claim); "energy
  differential" is read through its gloss by 3 of 4 (P3 "a slack from the surface", P5 "a potential-like scalar",
  P6 "the residual"); the finding, "facet", the elasticities and "not a regression" hold from round 1c. All four
  read on.
- Remaining, not held for anyone: "a soft support" (3 of 4: "I do not know what soft buys me", "the phrase is doing
  a lot of work without a definition"); P1 cannot tell the outer edge of the data from the Pareto boundary;
  "reversible chart" unclear to P3 and P5 (a coordinate map, invertible, but of what dimension).
- CR-1d (one clause, the driver's own sentence): "a soft support, not a regression" becomes "a soft support that a
  few designs may exceed, not a regression". It says what soft buys in the reader's terms (P3 guessed exactly this)
  and separates the edge from the boundary for P1. "Reversible chart" is left to Definition 5; the L-C test says
  whether the body answers it.
- Stop: after CR-1d the abstract rests for the supervisor's own review. Every wrong reading of the key (W1 to W4)
  is gone at depth A; what remains are concept words whose definitions belong in the body.

## Next

Re-test the L-A and L-B cells after CR-1 to CR-3 land; then the L-C and L-D cells (main text; with
appendices) once the section 4 and 6 narration is in; the docsite's task readers alongside.

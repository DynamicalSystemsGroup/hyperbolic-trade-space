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

## Round 2 (depths B and C on the settled paper at c6d0fff; six personas at B, five at C, P4-C held out)

Triage of 2026-11-10. Eleven fresh readers on the staged paper at c6d0fff (nine figures; "term"
for the earlier "facet"; the eight-metric data of record): six personas at depth B (headings, the
main-results list, the boxed statements with proofs withheld, the figures and their captions) and
five at depth C (the whole main text, appendices withheld). Reports verbatim in `round2-reads/`
(committed first, 1c67568); the slices and prompts are described in its README. Marked against
answer key version 2, held outside the repository; the triager confirmed its SHA-256 before
reading: `e72f3eeac76089d8657add60ac1b7553ac8fcfd022cc6cb0b69fb050931ad638`. Where the key's
facts predate WP23 and WP24, the statement is marked "key stale" rather than the reader wrong; the
stale lines are listed at the end for the driver. P6-B is one of the held-out cells of the draw
and was read in round 1 and again here; recorded for the driver (the confirmation read needs a
fresh reader on an unused brief wording).

### Per cell, against the key

The depth-B job is to state the main results and what is and is not claimed; the depth-C job is
to follow the argument with no "why" left that the main text owes. "Stated", "missing" and
"wrong" are the key's three marks; "key stale" is this round's fourth.

| Cell | Problem and idea (S1, S2) | PCA kin and chained | Surface not the Pareto boundary; a piece of surface per term (S3, S4) | Three levels, global not claimed (S5) | The case's finding (S6) | Two of S8 | Wrong belief on the key's list |
|---|---|---|---|---|---|---|---|
| P1-B | stated ("deciding between competing designs when you are trading many measures") | missing (PCA not mentioned) | stated; term "one flat piece of a piecewise surface" | stated in part (descent, local; stationarity not named) | stated | stated (not Pareto; "does not choose a design for you") | none |
| P2-B | stated ("the inputs are what I already produce") | half (chained read as a word not understood) | stated; term and cell told apart after a re-read | stated, all three | stated, with Figure 8 and 9 numbers | stated | none |
| P3-B | stated | missing | stated as a level some designs exceed; but the colleague sentence says the surface is fitted "through" the table (see wrong beliefs off the key) | stated | stated | one item (not Pareto) | none on the list |
| P4-B | stated | stated ("PCA comes after the fit, applied to the chart... a reading rather than a result"; "It is not PCA and it is not a Pareto-front estimator; it sits between them") | stated; the several-term fit read as Lloyd's algorithm with hyperplanes, which Theorem 11 as boxed says | stated, all three, with Corollary 1's "returned run" | stated | stated | none |
| P5-B | stated (thin on S1: "a way to describe a trade study") | missing (the item noted only as unintelligible) | stated, with the log-convex limit drawn correctly | stated, all three, checked by hand | stated | one item (not Pareto) | none |
| P6-B | stated ("the paper is written for people who do not speak DEA") | half (the item read as "listed under main results and described as not a result in the same sentence") | stated (Definition 1's three objects named as "the distinction my field spends effort teaching") | stated, all three | stated | stated (not Pareto; "does not tell the decision-maker what to choose") | none |
| P1-C | stated (the decision problem in the reader's words: "not the ranking, but the reason for the ranking") | stated ("PCA tells you where your data spreads out; this tells you where your data fights with itself") | stated ("a smooth reference surface that a few designs may poke through"; "each piece of the surface") | stated, with the limits (S7) in the authors' words | stated, both results (dominance saturates; one five-way tension becomes three) | stated, nine items | none |
| P2-C | stated | stated ("PCA says where the data vary, this says what trades against what") | stated ("It is not a regression through the middle") | stated | stated, three layers | stated | none |
| P3-C | stated | stated ("a PCA-like, unsupervised way to explain trade-offs, where PCA explains variance") | stated | stated | stated ("the finding: their sets differ") | stated | none |
| P5-C | stated, in optimization terms | stated | stated; the log-convex envelope and the K>1 nonconvexity read exactly | stated, with the certificate's radius read ("covers perturbations smaller than 1.2e-4") | stated | stated | none |
| P6-C | stated, in frontier terms (a Shephard-type distance to a soft Cobb-Douglas envelope) | stated | stated ("The paper is unusually frank that the surface is not the Pareto boundary") | stated | stated | stated ("does not claim priority") | none |

Depth B's job is done in 6 of 6 cells: every skim reader states the main results and quotes what
is not claimed. Depth C's job is not done in any cell: every main-text reader left with two or
more of the same "whys" open (what the effective sample size means; what "certified" means for
the fit of record; what the Section 6.2 numbers mean for the three-term split; what a candidate
is; what term 1 rests on; which of two near-duplicate metrics contends). Those are the change
requests below.

### Wrong beliefs

None of W1 to W8 in any of the eleven cells. No reader believes the method picks the design, that
certified means a global optimum (all five main-text readers and four skim readers say "local",
"for the returned run"), that the surface is the Pareto boundary, that the method replaces PCA or
Pareto analysis or claims to be new in kind, that the elasticities are causal (P1-C: "it tells you
about the designs you happened to evaluate, not about physics"), that the case validates on
hardware (P1-C: "illustrate the method; they are not satellite engineering"), that the exponents are
free of the conditioning (every cell names it), or that everything is machine-proved.

Beliefs the paper does not back, off the key's list (counted at once):

- **Convex read as "one answer"** (three cells, two depths): "it has one answer and does not depend
  on where you start" (P2-B); "a well-behaved (convex) problem with a unique answer" (P1-C); "a
  single answer that does not depend on the starting point" (P2-C). Theorem 3 says "convex, not
  claimed strictly", and the near-duplicate pair of metrics the readers found (below) is exactly
  where a minimizer need not be unique. CR-17.
- **The surface fitted "through" the table** (one cell, depth B): P3-B's colleague sentence, "this
  method fits a smooth reference surface through it and reads off trade-off rates", beside "I
  could not tell whether that is good or bad fit quality" at Figure 5. Round 1's regression reading
  is gone at depth A (rounds 1b to 1d) and at depth C; at depth B the slice carries no sentence that
  places the surface at the data's outer edge (the abstract's clause is depth A's), and P1-B says
  the consequence: "I cannot yet say in plain language what the fitted surface promises me". CR-9.
- **The several-term fit read as cell refits** (three skim cells, two main-text stops): "Each term
  owns a 'cell' ... and is fit on that cell; the algorithm alternates assignment and refit. That is
  Lloyd's algorithm with hyperplanes" (P4-B); "reassign each row to its maximising term, refit each
  term on its cell" (P6-B). This is what Theorem 11 and equation (2) say as boxed, against the
  recorded intent (every term fitted against every design; weights from the current model, then
  one program for all terms; one label per design is the package's sharp limit) and against
  Section 5's own sentence; two main-text readers found the contradiction (P5-C, P6-C, quoted under
  CR-15). Not a reader's error: a contradiction in the paper's sentences. CR-15, and a question for
  the supervisor below.

### Defects (counted at once)

- Definition 2's two halves disagree: "V(m)=∏_j m_j^{w_j}" has no normalization and "log V = w·u − β"
  has one; P5-B: "Is V 'the product' or 'the product times e^{-beta}'?" (CR-19).
- k indexes a metric in Theorem 5 and a term in Definition 8 (P5-B) (CR-19).
- Section 5's geometric-program sentence runs the change of variables the wrong way against the
  lemma it cites: L4.14 to L4.24 show the program in x = e^w is a geometric program in standard
  form and that "the problem in w is the convex form of this program (L4.23)"; the sentence says
  "convex after the change of variables x=e^{w}" (P5-C) (CR-18).
- Three descriptions of planted data that do not match (900 rows in Section 8; twenty tables of
  400 rows in Section 9; three metrics in Figure 1), and the Section 8 sentence stands where it has
  no referent (P2-C, P5-C, P6-C) (CR-24).
- Figure 4's caption says the fit temperature is "where the fraction first meets the target" while
  the text reports 0.092 against a target of 0.10; the package's rule (`select_temperature`) is a
  bisection to within 0.01 of the target (P6-C) (CR-31).
- Table 1 carries cells that are fragments: "Shares: the weights act as a trade-off"; "Differs: One
  exponent vector per term" (P3-C, P6-C) (CR-26).
- "Certified" is defined in the text for a soft fit only, while the default fit is sharp and the
  Discussion cites Theorem 12 (finite κ) for the fit of record; the package's termination record
  defines certified for a sharp fit separately (assignment fixed, residuals and term gaps within
  tolerance) (P5-C) (CR-14).
- Main-results item 1 cites Theorem 1 for a scope the box does not carry: the box is homogeneity
  and the log form; the item's "not the Pareto boundary but the level from which ... are read" is
  Definition 1's (P6-B) (CR-9).

### Friction replicated in two or more cells

- **Effective sample size 23** (ten cells; every cell but P4-B). "I also do not know what 'effective
  sample size' of 23 means for my trust. It starts around 560 and falls to 23, which sounds
  alarming" (P1-B); "For me this is the most important number in the paper and it is left as an
  annotation" (P6-B); "The paper does not discuss what that means for how much I should trust the
  exponents" (P3-C). CR-10.
- **Term 1 of the K = 3 fit rests, for the reader, on "3 of ten"** (eleven cells). "One of the three
  headline tensions is carried by three designs ... the one piece of evidence I could inspect for
  that term is a sentence saying there is not enough evidence to draw" (P1-C); "the claim for K = 3
  is supported by two maps and one sentence" (P3-C); "control effort shows w = 0.00 in terms 2 and
  3, so it must be term 1, and I cannot check that because term 1 has no map and no exponent table"
  (P2-C). CR-11.
- **Outlined but grey, unoutlined but 0.02** (nine cells). "I could not tell which set I am supposed
  to report as 'the trade'" (P2-B); "I could not tell which of the two I should act on" (P3-B);
  "It makes the relation between the tau-finite exponents and the tau-infinity support unclear"
  (P5-B). CR-12.
- **Energy balance and power margin at 0.96 to 0.99, the exponent on one in one regime and the
  other in the other** (seven cells: P2-B, P4-B, P5-B, P6-B, P2-C, P3-C, P6-C). "That looks like a
  collinearity artefact to me, not a trade" (P2-B); "the familiar zero-multiplier problem with
  near-collinear outputs: which of the two is 'contending' is not identified by the data, and I would
  want the paper to say so rather than let the n-lemma vocabulary suggest a finding" (P6-B); "I
  would call that a swap of one for the other, not a difference" (P2-C). CR-12.
- **Figure 7's horizontal axis "meaningless alone"** (eight cells). "why a coordinate that is
  meaningless alone is the x-axis of a figure" (P2-B); "I did not see what the figure shows beyond a
  histogram of log V turned sideways" (P4-B); "I cannot tell from this figure what to do with any
  design" (P2-C). CR-30.
- **Why 0.1, and who sets it** (ten cells; at depth B the caption gives no reason, at depth C the
  Section 5 sentence is found and one more is wanted). "Why target 0.1, and who sets it?" (P1-B);
  "τ selection is a rule of thumb ... I did not see where 0.1 comes from" (P4-B); "I would have liked
  one more sentence on why 10 percent rather than 5 or 20" (P1-C). Resolved by the depth contract
  at C (Section 5 says it is a convention and D.5 holds the evidence); at B, a caption clause: CR-31.
- **Theorem 10 (i)'s "so"** (six cells). "I read it three times" (P2-B); "the step from 'a convex
  symmetric program would have a symmetric minimizer' to 'so the actual objective is not convex' is
  not closed by what is stated" (P5-B); "I could not follow the 'so'" (P1-C). CR-16.
- **The Section 6.2 numbers at K = 3** (five cells, all of depth C). "I stopped completely ... I could
  not tell whether that is good news, bad news, or routine" (P1-C); "the certified result is fragile
  to a change of about 0.0001, which sounds tiny. Yet the same paragraph elsewhere says the status is
  'certified'" (P2-C); "it makes Level 3 close to vacuous for the fit of record" (P5-C); "The stable
  radius is smaller than the band by a factor of about 70 ... The text states this but does not draw
  the consequence" (P6-C). CR-13.
- **"Certified": sharp or soft, and what it means** (four cells at C). "I could not determine whether
  the K = 2, 3 fits of record are sharp or soft, and hence what 'certified' means for them" (P5-C);
  "The meaning of 'certified' is a local minimizer only, but the word suggests more" (P6-C); "I do
  not see how the stated exactness and the numerical tolerance meet in practice" (P3-C). CR-14.
- **Several temperatures, several bands** (five cells). "1/tau is 0.0088 here but 0.0262 at the K=1
  temperature (38.1), and 0.0935 in the propose-predict-check paragraph; I could not tell these are
  different temperatures for different fits" (P2-C); "The caption does not say which tau and kappa
  produced the K = 3 fit shown" (P5-B); "the band is not comparable across K" (P6-C). CR-23.
- **"Balanced hard-support geometry"; "the balanced point"; "step B, unpenalized"** (seven cells in
  all). "I do not know what hard-support geometry is and could not reconstruct the sentence" (P2-B);
  "I do not know what 'the balanced point' is; it is not defined in the main text" (P5-C); "Step B
  of what? There is no step A in the slice, and 'unpenalized' implies a penalized variant exists
  somewhere" (P4-B). CR-21.
- **"Term aggregation: sum by default, or mean"** (three skim cells). "I do not know why there are two
  options or when I would pick the mean" (P2-B); "I could not see what the mean alternative changes
  ... and the sentence does not say" (P6-B). CR-22.
- **Main-results items 5 and 6** (three cells each). "I did not understand what 'chained' means here,
  nor what distinguishes a reading from a result" (P2-B); "This is the sentence I most wanted, and it
  is one line pointing at an appendix" (P4-B); "Unintelligible without the section it points to"
  (P6-B, on "Numerical: the status a fit reaches"). CR-20.
- **Candidates and the three proposals** (four cells at C). "I did not know what the candidates were,
  who proposed them, or why three" (P1-C); "Three proposals, two of them one configuration ... is too
  few to read anything into. The paper says so itself ... Then I do not see why it sits in the main
  text" (P3-C). CR-24 (the candidate sentence); the proposals paragraph stays by the recorded intent
  (the key lists propose-predict-check among the results, mixed), its first sentence saying its job.
- **Figure 6's top panel: two diagonal streaks the caption does not name; no kink seen** (five cells).
  "two diagonal streaks of designs rising from lower left to upper right ... the caption says nothing
  about them" (P2-B); "I do not see a kink in any of the three panels. Each slice shows only one
  term's segment, so the claim 'Good for: seeing that the surface bends' is not what I saw" (P2-C).
  CR-32.
- **Term 3's elasticity read across a lattice** (seven cells). "I was not sure what an elasticity
  means when one of the two metrics only takes six values" (P4-B); "A facet spanned by categorical
  alternatives has elasticities that are artefacts of the catalogue, not of a trade-off" (P6-B); "It
  probably reflects the discrete bands seen in Figure 6, not a continuous trade-off, so reading it as
  an elasticity is questionable" (P2-C). CR-27.
- **Figure 5 cannot show the edge** (four cells). "the line is far from the visible upper-right edge
  of the cloud. So I cannot see the 'outer edge' the abstract promises" (P3-C); "the figure cannot
  confirm or deny that the surface fits the data" (P2-C). CR-33.
- **Figure 1's marker against its printed n-lemma** (two skim cells). "'The n-lemma printed is the
  support of the exact-maximum fit, not read off the marker' lost me completely" (P1-B); "I could not
  tell why the marker and the printed n-lemma can differ" (P3-B). CR-34.
- **"Regime" met before it is defined** (two skim cells). "I did not know what a regime is until this
  caption. ... The term appears in Figures 4, 5 and 6 before it is explained in Figure 9" (P2-B);
  "The caption does not say what I should conclude. This is probably the most decision-relevant
  picture in the set, and it is left unexplained" (P1-B, Figure 9). CR-31 (the gloss); the
  conclusion is the "Good for" line, page text given at depth C (a slice question for the driver,
  below).
- **"126 on 4 and 659 on 8"** (two cells). "had to read it three times ... the strongest motivating
  number in the paper and it is written in shorthand" (P1-C); "The 4-attribute set is not specified"
  (P6-C). CR-25.
- **Hypothesis codes** (five cells). "These labels (A1, R1, F12, I8, L5.25) are never explained in the
  main text" (P2-C); "I treated them as opaque labels" (P4-B). At B the A-codes are Section 3's
  (depth C) and the I- and F-codes Appendix B's and E's (depth D): the depth contract; one pointer
  sentence at Section 6's lead: CR-21.
- **Where to go to run it; a rule for conditioning** (three cells at C). "The paper does not tell me
  how to run any of it ... So I could not start from this text alone" (P3-C); "I need a house rule for
  conditioning before I would allow this to appear in a decision package" (P1-C). The depth
  contract: pointers to the next depth, named: CR-28.
- **"Hyperbolic"** (two cells). "The paper never shows or states that explicitly" (P3-C); "'Hyperbolic'
  also collides with the hyperbolic graph efficiency measure in my literature" (P6-B). CR-29.
- **"A clustering with per-cluster correlations would describe the same designs"** (two cells at C).
  "Not argued beyond that sentence. A skeptical colleague would say 'so why not just cluster and
  compute correlations?'" (P2-C); "The text itself admits" it (P6-C). CR-27.
- **"Energy differential"** (five cells comment; every cell reads it correctly through the gloss).
  "'Energy differential' put me on the wrong foot — in a power-and-mass problem, I assumed for a
  moment it was a real energy quantity. The parenthetical rescues it, but the term fights the domain"
  (P1-C); "a name that suggests more than it delivers" (P6-C); "I would have preferred 'log-offset' or
  'residual'" (P4-B). CR-5, with the supervisor; the evidence is added, no new request.

### Figure reads (image first, then the readers)

- Figure 1 (the simplex): a triangle, three numbered markers, a ring beside each, a legend of
  exponent vectors. Read by all as "which metrics a term trades, by the face its point sits in";
  two skim readers stopped at the marker-against-printed-support clause and at "the weight the three
  carry" (P3-B: "I could not tell what a weight on a metric triple means beyond the trivial case").
- Figures 2 and 3 (the model's views): read as the case's parts and requirements by every cell;
  the pictures the executive would show a board (P1-B: "Those two I can follow as an engineer");
  the modelling-language notation («MoP», «analysis def») is opaque to the ML reader (P4-B) and the
  caption's "computes the other six, pointing error and total mass from the configuration alone"
  took one reader three passes (P6-B).
- Figure 4 (the temperature sweep): two curves and an exponent heat map; the outlined column at
  38.1; "n_eff = 23" annotated. The most reusable figure for the practitioners ("the first thing I
  would show a reviewer, because it makes the one judgement call visible", P2-B; the exponents
  "fairly stable from τ = 25 upward", P4-B) and the figure that raised the effective-sample-size
  question in ten cells. One reader read the caption's selection rule against the text's 0.092
  (P6-C).
- Figure 5 (the one-term plane): a cloud with a line down its upper-right flank; many designs to
  the right of it. Round 1's anchor at four metrics; at eight, four readers say the slice shows a
  slope and not the fit.
- Figure 6 (the three planes): top, a dense cloud with two straight streaks at the lower left and
  a line through the cloud's upper part; middle, a cloud with the line above its top edge, few
  designs touching; bottom, horizontal bands and columns, a lattice, with the line above all but
  the top row. The bottom panel's bands are explained and read as the swaps (every cell); the top
  panel's streaks are not explained and were noticed first (five cells); the kink the "Good for"
  promises is not drawn in any panel (two cells). The lattice is where seven readers decided term
  3's elasticity is read across alternatives.
- Figure 7 (the chart): a sideways distribution of levels with a thin grey band at zero and a
  horizontal axis the caption disowns. Eight readers took the vertical story only. The figure's job
  (a level read apart from a position) does not survive the cold read; round 1 found the same on
  this figure under its old number.
- Figure 8 (associations per term): a placeholder sentence for term 1, two maps with outlined
  cells and a w column, one map with an outlined grey cell and an unoutlined 0.02. Every cell met
  the placeholder; nine met the outline-against-exponent puzzle; seven read the 0.96 to 0.99 pair.
  Read correctly by all as an analysis of the near-frontier designs, not the model.
- Figure 9 (the two regimes): two maps; the executive calls it "probably the most decision-relevant
  picture in the set" (P1-B) and the practitioner "precisely the 'why did the answer change' story"
  (P2-B); seven readers then read the energy-balance-to-power-margin swap and called it a swap.

### Preferences logged, not acted on (one cell each unless said)

A notation-and-vocabulary table before Section 3 and the PCA comparison promoted to a figure
(P4-B); Theorem 4 "a trivial identity presented as a theorem" (P6-C); "Why a frontier" is "an
assertion and not an argument" (P6-C); "Scaling" in the title ambiguous (P6-B); why a geometric mean
rather than a weighted sum "is never given in plain words" (P2-C); how to choose K (P2-C, P3-C:
the paper says it is future work; the depth contract holds); the minimum table size (P3-C: a new
result, non-goal); "thinnest term" undefined and "whether 11 rows is a worrying threshold" (P1-C);
"a frontier design scaled by v reads as a statement about physically realizable designs" (P6-C);
Definition 9's name against its content (P5-B); J_τ undefined in the skim (P5-B: equation (1) is
page text, a slice effect); the Section 13 statement "a claim I cannot check from the main text"
(P6-C); the Section 8 MoE sentence beside launch cost (P2-C); "at most one of its five metrics
could be a 20 percent change" (P2-C); "separate" against "differ" for the finding (P3-C: "the sets
overlap heavily, so 'separate' is a stretch"); "frontier" used loosely after Definition 1's three
objects ("near-frontier", "four-metric frontier"; P3-C); Figure 3's "returns 7 of 8 metrics" box
against its caption (P6-B); the band "a hair-thin sliver" (P1-B, P3-B: a reading of the picture;
Definition 4 defines it); Definition 4's weight sentence after CR-7 (P6-C: "I could not parse it";
P5-B verified it).

### Contradictions, resolved in the grid note's order

- *Depth contract (a).* Skim readers wanted the reason for 0.1, what a regime is, what Figure 9
  means, what Figure 7 shows and what the hypothesis codes are. Section 5, Section 8 and the "Shows
  / Does not show / Good for" blocks answer the first four at depth C and the appendices the fifth;
  no material moves up. Caption clauses carry the pointers (CR-31, CR-21). One question for the
  driver: the "Shows / Does not show / Good for" blocks are page text under each figure and were
  given at depth C only; a skimmer who reads figures and captions would see them. Whether they
  belong in the depth-B slice decides whether three of this round's skim frictions (Figure 9's
  conclusion, Figure 7's point, Figure 5's limit) are slice artefacts.
- *Depth contract (a).* The practitioners and the modeller want the calls, a conditioning rule and
  a rule for K. The calls and the conditioning guide are the docsite's (D-6); K is future work by
  the paper's own words. Resolved by naming the pointers (CR-28); nothing moves up.
- *Recorded intents (b).* The sceptic at both depths: "the estimator underneath is old machinery
  (Cobb-Douglas distance function, corrected least-squares-style one-sided fit, max-affine
  extension), and the paper mostly says so itself" (P6-C); against the ML reader: "the placement
  relative to PCA is genuinely something I did not have a tool for" (P4-B) and the optimization
  reader: "nothing claimed as Derived appears false, but the guarantees are the guarantees of
  coordinate descent on a nonconvex problem, dressed accurately rather than up" (P5-C). The intent
  claims nothing as novel and Section 2 says "We claim no priority"; the readers' verdicts are
  compatible with it. No change. What remains is the register question below.
- *Recorded intents (b).* P2-C and P3-C: the three proposals "do not estimate a rate", so why in the
  Results. The key lists propose-predict-check among the results (mixed: the energy differential
  predicted, the position not); it stays; its first sentence says its job (folded into CR-24's
  constraint on Section 9's closing paragraphs).
- *Recorded intents (b), the fit stated without membership.* The sentences of Section 5, Section
  6.2, Definition 6 and Theorem 11 contradict one another as read by two main-text readers and as
  the skim readers reconstructed the algorithm. CR-15 constrains the author by the intent; whether
  the intent's sentence ("every term is fitted against every design") describes the sharp fit of
  record or the soft fit only is the supervisor's question below.
- *Reader model (c).* P2-C's "why a geometric mean rather than a weighted sum"; P1-C's "thinnest
  term"; P3-C's minimum table size. The assumed mathematics holds from depth C; these are logged.
- *Remaining, for the supervisor (d):* below.

### What remains for the supervisor, with both readers' words

1. **"Energy differential" (CR-5, open since round 1).** All eleven read it correctly through the
   gloss; five comment on the name. P1-C: "in a power-and-mass problem, I assumed for a moment it
   was a real energy quantity. The parenthetical rescues it, but the term fights the domain. 'Level
   above or below the surface' would have done." P6-C: "The analogy is not needed ... path
   independence is trivial. I stopped at 'energy differential' as a name that suggests more than it
   delivers." The options of CR-5 stand (keep the term with its gloss; or make "level offset" the
   term and the analogy named once).
2. **Two sentences of his in the abstract, at depth C.** P6-C: "I could not tell what 'models the
   data underlying the table' means, or what 'views of that model' means, until Definition 1. The
   sentence is vague and I had to guess." P2-C, on the GGP and kernel sentence: "I could not follow
   this and it never says what I would lose or gain by caring"; P1-C: "'GGP-compatible kernel': no
   useful guess". Rounds 1b to 1d left both as his; nothing new is asked, the evidence is recorded.
3. **The fit stated without membership against the sharp fit of record.** P6-C: "'Which term scores
   a design highest is analysis of the fitted model, not part of the fit'. This contradicts the
   objective in Equation (2), where the label k(i) is an argmax inside F. I was confused about whether
   assignment is part of the fit." P5-C: "Is the contending set computed from an LP on the cell's
   rows alone (said to be ill-posed), or from f_k at τ = ∞ (soft max over all rows minus the cell
   mean)? The two can have different supports." The package's default is the sharp fit (labels),
   with soft weights on request. Options: (i) the paper says the fit of record is the sharp
   alternation, in which labels enter the objective, and keeps "every term is fitted against every
   design" for the offsets (each β_k is the soft maximum over all rows) and the soft fit; or (ii) the
   fit of record becomes the soft-weight fit the intent describes, which is a change of record
   (regeneration, not this package); or (iii) the intent's sentence is amended to say the sharp
   limit's labels are part of its objective and "which term dominates a design" is the reading after
   the fit. CR-15 is written for (i) and stops if (i) cannot be said truthfully.
4. **The sceptic's register question.** P6-B: "I want to see whether the prior-art table knows
   multiplicative DEA, the hyperbolic measure, Aigner-Chu and partial frontiers; if it does and says
   plainly how this differs, the paper earns its claim of a method." P6-C: "Multiplier-form DEA with a
   fixed weight vector, and DEA with weight restrictions, also give one global weight vector. A
   max-affine fit is a piecewise-linear envelope, as DEA's free-disposal hull is. The real difference
   may be the smooth soft maximum and the log scale, but the paper does not say so directly." Aigner
   and Chu and weights restrictions are in Table 1; multiplicative DEA (Charnes, Cooper, Seiford and
   Stutz; Banker and Maindiratta) and the hyperbolic graph measure (Färe, Grosskopf and Lovell) are
   not, and the title's word collides with the second. Options: add the two families to Appendix G
   and one clause to Section 2's DEA paragraph (each reference with a resolved DOI); or leave the
   register as reviewed and let the claim "we did not find the combination in the sources reviewed"
   carry it. Section 2's DEA paragraph already names the soft maximum, the band and the log scale as
   the difference; P6-C read it and still found it thin.

Mathematics questions one reader raised, for the driver (new mathematics is a non-goal; check,
do not overrule): (a) P5-C, equations (1) and (2) at K = 1 coincide only if the log-metrics are
centred; the conditioning of record does centre them (`preconditioning.py` uses a standard scaler
per log-metric) and the paper does not say so; (b) P5-B and P5-C, Theorem 12's second-order test on
"the tangent space of the active face" needs strict complementarity, which the hypotheses do not
list; (c) P5-C, Theorem 12's sketch offers a finite-difference agreement "on an exact instance" under
a Derived label; (d) P5-C, R1 is stated for the τ = ∞ envelope and invoked in Theorem 2 at finite τ;
(e) P5-C, finite termination of the sharp alternation "is elementary and distinct from the hopeless
Q1"; (f) P5-B and P5-C, the support of a non-unique LP optimum is solver-dependent, so R1 should be
checked numerically on the case before "5-lemma" is printed; (g) P6-C, why equation (2) selects a
frontier "and not a regression through a shifted cloud, other than the soft-maximum offset".

### Earlier change requests: which hold

- CR-1, CR-1b, CR-1c, CR-1d (abstract): landed; the two sentences held for the supervisor are item
  2 above.
- CR-2 (main results in the glossary's words; PCA chained): landed; item 5's "chained" is now the
  word three readers cannot read (CR-20).
- CR-3 (a facet is a piece of the surface; reach, share, support glossed): **holds after the rename.**
  Eleven of eleven read "term" as a piece of the surface and "cell" as the set of designs (P2-B:
  "I had to re-read to separate 'term' (a piece of the surface) from 'cell' (a set of rows)"; P1-B:
  "one flat piece ... of a piecewise surface"). The cluster reading of round 1 is gone. "Reach" is
  guessed right wherever it is guessed; "support" and "binds" are still unglossed for the executive
  (CR-34).
- CR-4 (figures): the "w = ..." boxes read from the caption (holds); the chart (old Figure 4, now
  Figure 7) still fails the cold read (CR-30); old Figure 7 (predicted against measured) has left the
  body; old Figure 2 (now Figure 5) is no longer the anchor at eight metrics (CR-33).
- CR-5 (energy differential): open, with the supervisor (item 1).
- CR-6 (a positive clause for the reference surface): landed in main-results item 1 for depth C;
  not for the executive at depth B ("I cannot yet say in plain language what the fitted surface
  promises me"): CR-9 carries the edge clause there.
- CR-7 (Definition 4's band sentence): reworded; one reader verifies it, one cannot parse it;
  logged.
- CR-8 (β one name; "dominates"): landed; Definition 2's new inconsistency is CR-19.

### Change requests (continuing the file's numbering; each names a passage, a problem and a constraint)

Structural, to the paper stream:

- **CR-9** (the main-results list, item 1, and Definition 1). Passage: "it is not the Pareto boundary
  but the level from which every design's position and level, and each term's elasticities, are read
  (Theorem 1)". Problem: nothing a skim reader sees places the surface at the data's outer edge
  (the abstract's clause is not in the skim), so one reader's summary has it fitted "through" the
  table and another cannot say what the surface promises; and the citation points at homogeneity
  for a statement that is Definition 1's. Constraint: the abstract's own words in one clause ("fitted
  to the outer edge of the data, not through its middle"), in the item or in Definition 1; the item
  cites Theorem 1 for the invariant value and Definition 1 for the three objects; no new claim.
- **CR-10** (Section 8, the fit-temperature sentence; Section 10, "Limits, in brief"). Passage: "the
  band 1/tau is 0.0262 and the effective sample size is 23.1 designs." Problem: the quantity is never
  said and its value is never read; ten readers stopped on it and two would not defend the exponents
  without knowing what it means. Constraint: one or two sentences saying what it counts (the designs
  the soft maximum weighs, the glossary's definition) and what the value means for the reading (the
  exponents at the fit temperature rest on about two dozen designs; the contending set holds under a
  halved or doubled temperature, D.5; the digits that hold, D.11); no uncertainty claim, since the
  paper says the exponents are not estimates with a sampling error.
- **CR-11** (Section 9, the three-terms paragraph; Figure 8's term-1 placeholder, to the figure's
  owner for its part). Passage: "control effort and peak slew power, absent from the K = 1 set, each
  lead a term of their own." Problem: every reader met "Too few near-frontier designs for an
  association reading: 3 of ten" and could not check the sentence, because term 1's exponents are
  printed nowhere the main text's reader sees; one of the three headline terms rests, for the reader,
  on a sentence that says there is not enough to draw. Constraint: the main text prints what it
  relies on: term 1's contending set with its leading exponent, its near-frontier count and the term
  shares (D.3 holds them), as generated values; the placeholder in Figure 8 prints term 1's exponent
  column even without a map; the finding stays "their sets differ"; no new result.
- **CR-12** (Section 9, the regimes paragraph and the three-terms paragraph; Definition 6's prose).
  Passages: "the primary regime alone has energy balance and total mass, the stock regime alone
  control effort and power margin"; "Exponents at the fit temperature grade the members, and a member
  can carry a small one." Problem: nine readers could not say which set to report as the trade when
  an outlined metric is grey and an unoutlined one carries 0.02; seven read the 0.96 to 0.99 pair
  (energy balance, power margin) and called the regimes' difference a swap of names. Constraint:
  the text names the pair once and says what the fit can and cannot tell apart between two
  near-duplicate columns (the fit is convex, not strictly, Theorem 3; the exponent's split between
  them is not identified by the data, so one carries it), backed by Theorem 3 and the association
  shown; one rule sentence says which set the reading uses (the contending set names the n-lemma;
  the exponents at the fit temperature give the elasticities; a member below participation contends
  in the limit and carries no elasticity at the fit temperature); the regimes sentence then counts
  the pair as one; no new result.
- **CR-13** (Section 6.2, the numerical paragraph). Passage: "At K = 3 the margin is 0.00121 and the
  stable radius 0.0001209, against a band 1/tau of 0.0088 and a median best-minus-second-best score of
  0.237: a margin below the band puts at least one design within the band of a seam, here 11 of the
  706, and the certificate covers changes under the radius only." Problem: all five main-text readers
  stopped and could not tell whether it is good, bad or routine; two drew the consequence the
  paragraph leaves undrawn. Constraint: the paragraph ends with the reading in the paper's register
  (what a margin below the band means for the three-term split; that the local-optimality
  certificate covers changes about seventy times smaller than the band; where the evidence of the
  contending sets' stability is, D.5); the claim narrowed by the paper itself, no caveat added to
  prove one.
- **CR-14** (Section 6.2, the stopping declaration and the status sentence; Section 10, "Three
  claims"). Passages: "For a soft fit, certified means that the second-order test holds (Theorem 12),
  and stationary that the term gaps hold and the curvature is not positive."; "On the primary regime
  the solver declares the status certified at K = 2 and 3"; "That the optimizer reached a local
  minimizer of the objective is the certificate (Theorem 12)." Problem: the fit of record's kind
  (sharp by default, soft on request) is not said where its status is reported, certified is defined
  for the soft kind only, and the Discussion cites the soft theorem for the fit of record. The
  termination record defines certified for a sharp fit (assignment fixed, residuals and term gaps
  within tolerance) and separately for a soft fit (second-order). Constraint: say which the fits of
  record are; define certified for each kind in one sentence, from the termination record (D.8); the
  Discussion cites the result that applies (Proposition 3 and Corollary 1 for a sharp fit, Theorem 12
  for a soft one); no new claim.
- **CR-15** (Section 5, "The estimator" and the sentence before Theorem 10; Section 6.2's lead;
  Definition 6; the sentence after Theorem 10). Passages: "Which term scores a design highest is
  analysis of the fitted model, not part of the fit (steps: Appendix B.2)." against equation (2) and
  Theorem 11's "reassigning each row to the cell of its maximizing term"; Definition 6's "the
  exact-maximum (τ=∞) fit to the term's cell" against "Refitting a term on its own rows is ill-posed
  (observed on planted data, Appendix D.13)". Problem: two main-text readers found these contradict
  and three skim readers reconstructed the algorithm as cell refits from the boxes. Constraint: the
  recorded intent (every term fitted against every design; weights from the current model, then one
  program for all terms; one label per design is the package's sharp limit; which term dominates is
  analysis): one paragraph in 6.2 says, for the sharp fit of record, where the labels enter (the
  objective's argmax) and that each offset is the soft maximum over all rows, and that reading which
  term dominates a design after the fit is analysis; Definition 6 says which program yields the
  contending set and in what sense a refit on a cell's own rows is ill-posed; from Appendix B.2 and
  the package, not by guess; if the sentences cannot be reconciled without changing the intent, stop
  and report (the supervisor's item 3).
- **CR-16** (Theorem 10 (i) and the sentence that introduces it). Passage: "a convex program symmetric
  in the terms attains its minimum with all terms equal, so the objective over all terms is not
  convex in them in general". Problem: six readers stopped at the "so"; four supplied the missing
  step themselves and said the box does not say it. Constraint: the step said once, in the box or in
  the sentence before it, in L16's words (a symmetric convex objective would be minimized with all
  terms equal, which a useful several-term fit is not); no new mathematics.

Local, to the paper stream:

- **CR-17** (Section 5, the sentence on the one-term program; the sentence before Theorem 3).
  Passages: "The one-term fit is a geometric program, convex in the logarithmic variables"; "J_τ is
  convex, not claimed strictly." Problem: three readers read convex as one answer independent of the
  start; the paper claims convexity, not strict convexity, and CR-12's pair is where a minimizer need
  not be unique. Constraint: one clause where convexity is first glossed in prose saying what it gives
  (every minimizer is global) and does not (uniqueness is not claimed); no new claim.
- **CR-18** (Section 5, "The model"). Passage: "At finite τ one term is a geometric program, convex
  after the change of variables x=e^{w} (Appendix B, L4.14 to L4.24)". Problem: the direction is
  reversed against the lemma cited: the program in x = e^w is the geometric program in standard form
  and the problem in w is its convex form (L4.23); Section 1 says it right. Constraint: "a geometric
  program in x = e^w, whose convex form is the problem in w (L4.14 to L4.24)", or words to that
  effect; nothing else changes.
- **CR-19** (Definition 2; Theorem 5). Passages: "V(m)=∏_j m_j^{w_j} and, with the reach β (Definition
  7), log V = w·u − β"; Theorem 5's "d log m_j / d log m_k = −w_k/w_j" against Definition 8's "along
  term k ... −w_{ki}/w_{kj}". Problem: the two halves of Definition 2 disagree by the normalization,
  and k is a metric in one box and a term in the next. Constraint: Definition 2 writes V with its
  normalization, consistent with Theorem 1's V(me^{−β}) = e^{−β}V(m); Theorem 5 uses a metric index
  other than k; the glossary's names.
- **CR-20** (the main-results list, items 5 and 6). Passages: "PCA and the fit are chained: the
  principal directions of the near-frontier chart read the trade-offs the sampling exercised, a
  reading and not a result (Appendix D.16)."; "Numerical: the status a fit reaches. Open: Q1 to Q4 and
  the search's monotonicity." Problem: three readers cannot read "chained" or why a main result is
  "not a result"; three find the sixth item unintelligible without its sections. Constraint: item 5
  says what composes with what and where ("PCA run on the near-frontier chart reads the trade-offs
  the sampling exercised: a reading, Appendix D.16"); item 6 names its objects in a clause each (the
  status is the termination record's, Section 6.2; Q1 to Q4 are Section 6.3's); the glossary's words.
- **CR-21** (Theorem 2's last sentence; R1 in Section 5; Theorem 11's hypotheses; Section 6's lead).
  Passages: "Balanced hard-support geometry does not imply an interior minimizer at finite τ."; "the
  balanced point lies in the relative interior of a facet of the supporting envelope with positive
  normal"; "step B, unpenalized, with support offsets". Problem: four readers stopped at the Theorem
  2 sentence, two could not find "the balanced point" defined, four did not know what step B or
  "unpenalized" is, five treated the hypothesis codes as opaque. Constraint: "balanced point"
  defined in one clause where R1 is stated; the Theorem 2 sentence glossed in R1's words or moved to
  the remark; "step B, unpenalized" said in the alternation's words (the refit step with support
  offsets, without the penalty the package offers) or cut from the box; one sentence at Section 6's
  lead saying where each code family is defined (A: Section 3; R: Section 5; F and I: Appendices B
  and E). "Facet" in R1 is a face of the supporting envelope, a polyhedron, not the earlier word for
  a term; the vocabulary check decides whether it stays.
- **CR-22** (Definition 3). Passage: "Term aggregation: sum by default, or mean; the formula is the
  sum." Problem: three readers could not tell what the mean changes or why the box carries it.
  Constraint: the clause says what the mean changes (if the package offers it, in one phrase) or the
  box drops it and the package documentation keeps it.
- **CR-23** (Section 9, where the K = 3 fit is introduced; the mean-slack sentence; Figure 7's caption,
  to the figure's owner for its clause). Passages: "at the temperatures 38, 94 and 113"; "a band 1/tau
  of 0.0088"; "the regressor's own band 1/tau = 0.0935". Problem: five readers could not reconcile
  the bands or tell which temperature produced Figure 7. Constraint: one sentence where the K = 3 fit
  is introduced says each fit of record's temperature and band and that each K has its own
  temperature by the same rule; Figure 7's caption names its temperature and band.
- **CR-24** (Section 8's planted-table sentence; Section 9, "A known answer" and "Candidates"; the
  proposals paragraph). Passages: "The planted table has 900 rows, 4 metrics and 3 planted terms.";
  "On 20 planted tables (400 rows, 4 metrics)"; "Candidates are scored against the K = 1 fit (Appendix
  D.7). The 3 measured candidates have lowest energy differential -0.197 ...". Problem: three readers
  found three planted-data descriptions that do not match and one sentence with no referent; four
  did not know what a candidate is; three asked why three proposals of two designs sit in the
  Results. Constraint: each planted table named once with its job (Figure 1's three-metric table,
  the 900-row table of D.13, the twenty 400-row tables of D.14) and the orphan sentence moved next to
  "Where the answer must be known, we plant it"; "candidate" said in one clause (what they are, where
  from) or the paragraph goes to D.7 behind a pointer; the proposals paragraph's first sentence says
  its job (a check of the regressor, not an estimate of a rate); generated values stay generated.
- **CR-25** (Section 1, the dominance counts). Passage: "Of 706 feasible cubesat designs, the
  nondominated sets hold 126 on 4 and 659 on 8 attributes". Problem: two readers read it three times;
  the four attributes are not named. Constraint: the sentence in words, the four attributes named
  (from D.11), the counts as generated.
- **CR-26** (Table 1). Passages: Pareto row, "Shares: the weights act as a trade-off"; DEA row,
  "Differs: One exponent vector per term". Problem: two readers found cells that are fragments and
  could not use the table against DEA. Constraint: each cell a clause answering its column; the DEA
  "Differs" cell carries the paragraph's own difference (one exponent vector per term, a global named
  structure, where DEA weights unit by unit; a soft maximum with a band, not a boundary set by extreme
  units). The slice flattened the table's layout; the cell text is as rendered.
- **CR-27** (Section 9, the sentence after the mean-slack paragraph). Passage: "A clustering with
  per-cluster correlations would describe the same designs; the terms add a model: each term's fitted
  exponents give the elasticities at which its contending metrics trade (Theorem 5)". Problem: two
  readers found it unargued ("so why not just cluster and compute correlations?"); seven read term
  3's two leading metrics as set by the tracker and wheel swaps and asked what an elasticity means
  across a lattice. Constraint: one term's elasticity read as a number from its exponents (a generated
  value, not typed), the thing an association cannot give; for term 3, the clause that its two
  leading metrics are set by the swaps (Figure 6's bottom panel), so its elasticity is read across
  the catalogue's alternatives and not along a continuous trade (Section 12 names discrete variables
  as future work); no new result.
- **CR-28** (Section 11; Section 5, "Conditioning (stage 2)"). Passages: "the package documentation
  is the user's guide"; "done with scikit-learn tools (Section 5)". Problem: three main-text readers
  could not start from the text and asked for a house rule for conditioning; the paper rightly leaves
  both to the next depth and points at nothing named. Constraint: Section 11 names the docsite page
  (install and first fit) and Section 5's conditioning paragraph names where the case's rule is
  (Appendix C) and where the guide is; nothing moves up.
- **CR-29** (Section 4, the sentence before Definition 2). Passage: "The invariant value V is a
  weighted geometric mean of the metrics; doubling every metric doubles it." Problem: two readers
  guessed where the title's word comes from and said the paper never says it where V is defined
  (Section 2's clause is in the lineage paragraph). Constraint: one clause: the level surfaces of V
  are hyperbola-like in the metrics (two metrics: m_1^{w_1} m_2^{w_2} = const), hence the title's word;
  no new claim.

To the figures' owners (figure-review's cold read decides; the paper stream is told):

- **CR-30** (Figure 7, structural). Passage: "Z0, the first of seven position coordinates,
  meaningless alone". Problem: eight readers took nothing from the horizontal axis and the figure's
  job (a level read apart from a position) did not survive the cold read; round 1 found the same on
  this figure under its old number. Constraint: either the horizontal axis earns its place (a
  position coordinate with a stated reading; for instance the first principal direction of the
  near-frontier chart that D.16 reads as the trade-off the sampling exercised) or the figure becomes
  the level distribution alone; the caption then says what the axis is; ink as data.
- **CR-31** (Figure 4, local). Passages: "the vertical line is the fit temperature, where the fraction
  first meets the target"; "with the target 0.1 (dashed)"; "primary regime". Problem: the caption's
  rule disagrees with the text's 0.092 against 0.10 (the package bisects to within 0.01 of the
  target); ten readers asked why 0.1; two skim readers met "regime" four figures before Figure 9
  defines it. Constraint: the caption states the rule as applied (the temperature at which the
  fraction is within 0.01 of the target 0.1, a convention: Section 5) and glosses "primary regime"
  at this first caption (aggressive controller gains; the stock regime is Figure 9's second panel).
- **CR-32** (Figure 6, local). Passage: "one straight segment per term (named on it)"; "Good for:
  seeing that the surface bends and that each term is a piece of it." Problem: five readers saw two
  straight streaks in the top panel that the caption does not name while it names the bottom panel's
  bands; two saw no kink in any panel. Constraint: the caption says what the streaks are if the model
  backs it (Appendix C), or the panel is not the one to show; "Good for" says what the panels show as
  drawn (each term's slope in its own plane) unless the kink is drawn; ink as data.
- **CR-33** (Figure 5, local). Passage: "The line is the surface in this slice: the other six metrics
  are held at the median of the near-frontier designs, so designs off that median fall on either side
  of it." Problem: four readers could not see the outer edge the abstract promises and concluded the
  slice cannot confirm or deny the fit; the anchor status of round 1 rested on a four-metric picture.
  Constraint: the figure shows what it can (the one-term slope) with the designs near the median of
  the other six distinguished, or only those, so the line is their edge; or the caption's first
  sentence says the picture shows the slope and not the fit; the sentence test.
- **CR-34** (Figure 1, local). Passage: "The n-lemma printed is the support of the exact-maximum fit,
  not read off the marker." Problem: two skim readers could not tell why the marker and the printed
  n-lemma can differ; "binds" and "support" are unglossed for the executive. Constraint: the caption
  says in plain words that the marker is the exponent at the fit temperature and the printed n-lemma
  the support of the exact-maximum fit (a member can carry a small exponent), or drops the clause;
  "binds alone" stays.

### The worst cells, and what model readers could not establish

Worst cells, by the key: no cell carries a wrong belief from the list. At depth B the worst are
P3-B (the surface "through" the table in the colleague sentence; PCA not recalled; one item of
S8) and P1-B (PCA not recalled; "I cannot yet say in plain language what the fitted surface
promises me"; "binds", "support", "simplex" stopped the read at Figure 1). At depth C the worst are
P2-C (the most stops, and the practitioner's three questions left by design: K, the temperature,
the conditioning) and P5-C (the two statement problems, CR-14 and CR-15, and seven mathematics
questions for the driver). P6-C's list is the longest and its reading the most exact.

What model readers could not establish: whether the supervisor's two abstract sentences read to
his collaborators (model readers parse them and still call them vague); whether an effective
sample of 23 is comfortable (a judgement the paper must make from D.5 and D.11, not a reading);
whether the energy-balance-to-power-margin swap is a finding or a near-duplicate artefact (the
figures show the pair; only the author can say what the fit identifies); whether the three
proposals belong in the Results (the key says yes; three of five main-text readers say no); the
mathematics questions (a) to (g), which need the driver and the lemmas; whether a forty-minute
executive would reach Section 9 at all (a model does not tire; P1-B's "I would read Sections 1, 9
and 10 and skip the theory" is a model's forecast); and the docsite's part of the read (D-6's
loop).

### Key stale, for the driver (the statement marked "key stale", the reader not marked wrong)

- S4: "With K terms the frontier has K facets" (the word is "term" after WP24; every reader uses
  "term" and the triage follows).
- S6: "ten attributes" (twice) and "Nearly all designs (671 of 706) are nondominated on ten
  attributes" (the data of record after WP23 have eight attributes; the paper's counts are 126
  nondominated on 4 and 659 on 8 of 706; the readers' recall of 8 and 659 is correct).
- S6: "One term gives one tension among six metrics" (the paper's K = 1 fit is a 5-lemma: total mass,
  energy balance, pointing error, depth of discharge, settling time; the readers' "five" is correct).
- S7: "Exchange rates describe sampled designs, not causes" (the key's own header says the word is
  elasticity; the line keeps the old word).
- The header's "the three-pane figure has left the paper's body" holds; the paper now has nine
  figures, which the key does not count and need not.
- Unchanged and still right: S1 to S3, S5, S8, S9, the depths' jobs, W1 to W8.

## Docs loop, round 2 (three task readers on the staged site at c6d0fff)

Triage of 2026-11-10 (D-6). Three fresh readers, one task each, on the staged site at c6d0fff
(the root page, the docsite, the paper) with a clean worktree of the repository at the same
commit: install and run a first fit (R1); read a tension report and choose K (R2); read a
termination record and say whether the fit converged (R3). Reports verbatim in
`round2-docs-reads/` (committed first, fdab633), with the tasks and models in its README. The
docs pages are unchanged between c6d0fff and the head of `dev` at the triage (ca6ce94). Every
passage a reader quoted was checked against the page, and every command a reader ran was re-run
in a worktree of `dev`: the first fit, the Termination page's example and its margin check,
`examples/adcs/k_terms.py`, `case.fit_study` at K = 1 and K = 3, and the Fitting page's K recipe
on the cubesat table. Every number the three readers report replicates to the digits they give.

The docs loop has no answer key of its own; the four things a package user must leave with are
the brief's: the method does not pick a design; what a sharp fit's certificate says; what K
means; what the termination record's fields say.

### Per reader: the task, and what the reader believed at the end

| Reader | Task done | What the reader believed at the end | Against the docs and the package |
|---|---|---|---|
| R1 (install, first fit) | Yes. `uv sync`; the Getting started snippet in a file; output `trilemma [0 1 2]`, `[0.3 0.37 0.33]`; the two-metric plot saved. Read the fit as: all three metrics contend, exponents nearly equal, elasticities near -1 pairwise, most designs inside the surface (mean log V -0.67, 108 of 300 beyond). | "It does not choose a design for you"; conditioning is a separate step; "it describes the data you give it"; "makes no claims on the page about uncertainty"; "not a prediction or optimization engine for new designs". | All correct. The last holds for the estimator (no `predict`); the user guide's prediction page composes a regressor for that question, on a page the reader did not open. The one thing the reader left unchecked (whether 108 of 300 beyond V = 1 is expected) is expected: the synthetic table puts 30 percent of its rows on the planted frontier (Fitting page); `frac_above_` = 0.360 replicates. No wrong belief. |
| R2 (tension report, choose K) | Yes. K = 3 for the primary table, with reasons (mean slack at fixed tau 0.243, 0.132, 0.088, 0.070; ten resamples at K = 3 return the same three families of terms, at K = 4 two terms share one participating set in 6 of 10; every K = 3 cell at fixed tau has 27, 17 and 118 near-frontier designs); K = 2 named as the cautious alternative; held loosely, with the reasons. | K is "the analyst's choice, never selected by the fit"; the certificate "is about a local optimum of the solver, not about the data being right"; tensions are "observations of the fit, not explanations"; association near the surface is partly closure; the fit "assigns each design to a term (cell)". | All correct. "Assigns each design to a term" is what the package's default sharp fit does (`cell_`); the glossary's entry "assignment: an analysis, since the fit weighs every term against every design" is the paper triage's open item 3 (the fit stated without membership), not a reader's error. No wrong belief. |
| R3 (termination record) | Yes. "The fit converged, by the package's own criteria, to a local optimum", from the K = 3 cubesat record: `certified`, `assignment_changes = 0`, `n_empty = 0`, `max_gap` 4.1e-15 against `eps_kkt` 1e-8, residuals 0, `gamma` 0.0012 > 0, `n_distinct_terms = 3`, five seeds agreeing. | Certified means the three levels, "a local optimum of the objective, not of other restarts"; `bound` bounds the distance from the fixed-assignment optimum; the one-term record "does not certify anything" and the convex program is what to rely on; a soft fit "means designs are weighted across terms instead of hard-assigned"; whether it holds outside the table "is not something the certificate says". | All correct, field by field against the `Termination` docstring. One step is the page's, not the reader's: to judge the margin the reader compared `gamma` with the band 1/tau (0.0012 against 0.0088) because the page puts `gamma` "on the scale of the band" first, and says it did not compute the median margin the page's rule names (0.237 on this fit; replicated). No wrong belief. |

No reader believes the method picks a design, that certified means a global optimum, that the
fit chooses K, or anything about a record field that the docstring does not say. All three
tasks were done from the pages alone.

### Defects (counted at once)

1. **The Examples page's K comparison is the one the Fitting page forbids.** Examples, "Three
   terms": "The mean slack falls from 0.243 at one term to 0.146 at three, and the status is
   `certified`." Fitting, "Choosing K": "Compare numbers of terms at one fixed temperature, by
   `mean_slack_`, never by `objective_` and never at a temperature re-selected for each K."
   Replicated: 0.243 is at tau 38.10 and 0.146 at tau 113.22, each re-selected for its K
   (`k_terms.py`, `case.fit_study`); at the K = 1 temperature the mean slack is 0.243, 0.132,
   0.088 (the script's own "DIAGNOSTIC, fixed tau" block). The same bullet's "72 percent", "3
   percent" and "3 near-frontier designs, fewer than the ten an association reading needs" are
   also the re-selected fit's; at fixed tau the three cells hold 27, 17 and 118 near-frontier
   designs and every term has a reading. R2: "I expected the Examples page's headline comparison
   to be the fixed-temperature one (0.243 → 0.088), or to say why it is not." DCR-1.
2. **The Fitting page's K recipe gives no signal on the case's own table.** Fitting, "Choosing K":
   "add a term only while the resampled exponents stay stable", measured in the page's block as
   `exponents_.min()` over resamples. On the cubesat table the smallest exponent is 0.000 at K =
   1, 2, 3 and 4 in every resample (replicated: four resamples each), because some metric is
   always excluded; the Tensions page says sparsity is the normal case. One reader found it; it
   counts because the run shows it. R2: "The recipe as written gave me no signal; I had to invent
   a substitute." DCR-2.
3. **`shares`: one word, three quantities.** The record's `shares` is the row share |C_k|/N
   (`Termination` docstring); the Termination page lists it under "The fields" with no
   definition. `term_share_`, the Examples page's "near-frontier share" and `k_terms.py`'s "term
   shares" are the share of the near-frontier rows. The glossary's "share" is a metric's share of
   a total in the ternary plot. On the K = 3 cubesat fit the record's `shares` are [0.256, 0.229,
   0.514] and `term_share_` is [0.034, 0.241, 0.724]. R3: "Same name, two quantities." DCR-3; the
   glossary's part to the PM.
4. **The Termination page's margin rule points two ways.** "How small is a small margin":
   "Compare `gamma` with the median margin ... far below it, a few designs sit on a seam", then
   the page's example, "`gamma` is 0.0020 against the band 0.02 and the median margin 0.21: level
   3 holds", where `gamma` is a hundredfold below the median. On the cubesat K = 3 fit `gamma` is
   0.0012 against a median margin of 0.237 (replicated). The rule and its example cannot both be
   read as written; R3 read the band instead. DCR-4.
5. **The script prints "mean slack" under a column headed `objective_`.** Examples, "Run it":
   `k_terms.py` "reproduces the one-, two- and three-term fits", and the page's "mean slack ...
   0.243 ... 0.146" are the script's `objective_` column. For the sharp fit at K > 1 `objective_`
   equals `mean_slack_`; at K = 1 it is the soft maximum, which on this table equals the mean
   slack only because the conditioning's standard scaler centres the log-metrics (mean of u . w
   is 3e-15; replicated). R2: "my K=1 fit had objective_ 0.243374 and mean_slack_ 0.2434,
   identical to four digits, which left me unsure which number I was looking at." DCR-5.

### Friction replicated in two of three readers

- **V, and log V, met before any definition** (three of three). Getting started, "Reading the
  output": "`ts.score_samples(X)` is the log of V for each design, the energy differential to the
  fitted reference surface": V is not said on the page. R1: "I read score_samples as a signed
  distance, in log terms"; R2: "met before any definition; guessed"; R3: "V seems to be a design's
  score relative to the fitted surface (1 on the surface, above 1 beyond it)". All three guessed
  it right; the glossary has it (invariant value). DCR-6.
- **The temperature, where first met** (two of three). Getting started passes `temperature=20.0`
  and says only "at the fit temperature". R1: "never explained on this page"; R3, from the Fitting
  page's sentence: "I took it on faith". DCR-7.
- **What `k_terms.py` prints, and where the record is** (two of three). Examples, "Run it": run
  the script, "then read the tension report and the termination record". The script prints
  summary tables with its own column heads. R2 guessed "reach beta_k", "gap G_k", "gamma",
  "radius", "bound", "certified" and still "only half" understands two; R3: "the script prints
  summary tables ... rather than the record object itself. To see the actual record I had to work
  out ... that `fit.estimator.termination_` would give it." DCR-8.
- **"Posynomial" where first met** (two of three). The root page: "applies a posynomial invariant
  form to learn the shape of a trade space"; R3: "not defined where I met it on the landing page";
  R1, on the docs home's "a sum of monomial terms": "partly explains it". DCR-9.
- **n-lemma, trilemma** (three of three guessed it, three of three guessed right: "n metrics are
  in mutual tension"). Logged, no request: the Getting started sentence does its job.

### Friction reported once (logged, not acted on)

- R1: two install routes (the root page's `pip install git+...`; Getting started's clone and
  `uv sync`), "and I had to pick one"; the page says `uv run python first_fit.py` and never says
  to make the file; "the package's own example data" against a synthetic generator (the task's
  wording; the case is on the Examples page, which R1 did not open).
- R2: a 404 at `docs/glossary/`, the reader's own guess (the link is `docs/generated/glossary/`
  and no page links the guessed path); what "ilr" and "alr" change (the Chart page, not opened);
  at fixed tau with several terms `frac_above_` rises to 0.26 against the 0.10 target, "which the
  Fitting page warns is normal with several terms but which I cannot judge".
- R3: Getting started never mentions `termination_`, and the one-term record shows `max_gap`
  8.7e-6 against `eps_kkt` 1e-8 with `status` `not_applicable`; the docstring says the gaps are
  then diagnostics, the page's `not_applicable` bullet does not (replicated; one reader).
  `conditioning_` "small" with no scale (0.27 beside 9.26 and 9.03 on the K = 3 fit). KKT, term
  gap, restricted Hessian and seam are "optimization vocabulary I don't have"; the reader
  reconstructed each from the page.

### Preferences logged

- R1 would start from a real table rather than a generator (the case is one page away).
- R2 asks for "a stability check in the Fitting page that works for sparse exponents (set
  recurrence or term duplication across resamples)": folded into DCR-2's constraint, since the
  page's own criterion (a term that changes between resamples is a splinter) is kept and only its
  measure changes.
- R3 would have the Examples page "print `termination_` directly after 'Run it'": DCR-8.

### Contradictions

None between the three readers; their tasks do not overlap. One for the harness, not the docs:
"the package's example" named two things to two readers (the synthetic first fit; the cubesat).
R1 took the first, R2 and R3 the second and said so. The next round's task wording names the
page.

### Change requests (DCR-1 onward; each names a page and a passage, a problem and a constraint; local or structural; target)

- **DCR-1** (Examples, "Three terms" bullet). Structural; the docs stream. Passage: "The mean
  slack falls from 0.243 at one term to 0.146 at three, and the status is `certified`. ... The
  largest holds 72 percent of the near-frontier share ... the smallest term holds 3 percent ...
  Its cell holds 3 near-frontier designs, fewer than the ten an association reading needs, so none
  is given." Problem: the comparison is between fits at temperatures re-selected per K, which the
  Fitting page's rule forbids, and the "fewer than ten" sentence is a consequence of that
  re-selection (at the K = 1 temperature the cells hold 27, 17 and 118 near-frontier designs).
  Constraint: the bullet reports the K comparison the Fitting page asks for (mean slack at the K
  = 1 temperature: 0.243, 0.132, 0.088, from `case.mean_slack_fixed_tau`, which exists and is
  unused by the page), and the three terms' sets and shares at that temperature; if the
  re-selected fit stays on the page, one sentence says what it is for and that its numbers are not
  the comparison; the paper's Section 9 numbers are the paper stream's (CR-23 holds them) and
  nothing here changes the paper.
- **DCR-2** (Fitting, "Choosing K, the temperature and the band", the resample block and the two
  sentences after it). Structural; the docs stream. Passage: "add a term only while the resampled
  exponents stay stable" and the block's `exponents_.min()`, with "the smallest exponent stays
  within 0.07 to 0.08 at K = 3 and ranges from 0.00 to 0.07 at K = 4". Problem: the measure is
  identically zero whenever a metric is excluded, which the Tensions page calls the normal case,
  so the recipe gives no signal on the Examples page's own table (0.000 at every K in every
  resample). Constraint: the page's criterion stays (a term whose exponents change between
  resamples is a splinter); its measure is one that is not zero under sparsity, read per term
  (each term's participating set across resamples, or the change of each term's exponent vector;
  `n_distinct_terms` already counts terms that coincide), shown on a table where sparsity occurs;
  the synthetic numbers may stay as the dense case; no new result or rule for K.
- **DCR-3** (Termination, "The fields", the `shares` bullet; the glossary's "share"). Local for
  the page, to the docs stream; the glossary entry to the PM. Passage: "`status`, `reason`,
  `n_iter`; `max_gap`, `gaps` (`nan` for an empty cell) and `shares`." Problem: `shares` is the
  only field on the page without a definition, and the same word names the near-frontier share on
  the Examples page (`term_share_`) and a metric's share of a total in the glossary. Constraint:
  the page says what the record's `shares` is (the share of all designs in each term's cell, the
  docstring's |C_k|/N) and that `term_share_` is the share of the near-frontier designs; the
  glossary's question (one name per quantity: the record's row share, the estimator's
  near-frontier share, the ternary share of a total) is the PM's, and a glossary entry
  regenerates Appendix A in the same push.
- **DCR-4** (Termination, "How small is a small margin"). Local; the docs stream. Passage:
  "Compare `gamma` with the median margin, the median gap between best and second-best term score:
  far below it, a few designs sit on a seam." and "On this table at tau = 50, `gamma` is 0.0020
  against the band 0.02 and the median margin 0.21: level 3 holds." Problem: the rule says far
  below the median is a warning and the example, a hundredfold below the median, is read as
  holding; a reader took the band as the comparison instead. Constraint: one reading that the
  example satisfies, stated so that a user can apply it to their own record (level 3 holds
  whenever `gamma` is positive, as the status says; the median says how typical the tightest
  design is; what a user does with a `gamma` far below the median, in one sentence); the
  cubesat K = 3 record (`gamma` 0.0012, median 0.237) must read the same way as the page's
  example; no new claim about the certificate.
- **DCR-5** (Examples, "Run it"; `examples/adcs/k_terms.py`, the `summary` table's `objective_`
  column). Local; the page to the docs stream, the script to its owner by the PM (not a docs
  file). Passage: the page's "mean slack ... 0.243 ... 0.146" against the script's column head
  `objective_`. Problem: the page's number is printed under the name the Fitting page says never
  to compare by; the two coincide here for reasons the pages do not give. Constraint: the table
  the page points to prints `mean_slack_` under that name; the Fitting page's `objective_`
  bullet, or the estimator's docstring, may say in one clause that the two coincide at K = 1 when
  the log-metrics are centred, which the case's conditioning does.
- **DCR-6** (Getting started, "Reading the output", the `score_samples` sentence). Local; the docs
  stream. Passage: "`ts.score_samples(X)` is the log of V for each design, the energy differential
  to the fitted reference surface: negative inside, positive beyond." Problem: V is not defined
  on the page and three of three readers guessed it. Constraint: one clause in the glossary's
  words (V, the invariant value, a weighted geometric mean of the metrics, 1 on the fitted
  reference surface), before "log of V"; no new term.
- **DCR-7** (Getting started, "A first fit", `temperature=20.0`). Local; the docs stream.
  Passage: `HyperbolicTradeSpace(temperature=20.0).fit(X)` and, later, "the fitted weights at the
  fit temperature". Problem: the one parameter the snippet sets is not said on the page; two
  readers guessed it. Constraint: one clause where the parameter first appears (tau, how hard the
  maximum is; a band of near-frontier designs of width 1/tau), with the pointer to the Fitting
  page's "Choosing the temperature"; nothing about how to choose it moves up.
- **DCR-8** (Examples, "Run it"). Local; the docs stream. Passage: "`k_terms.py`, which
  reproduces the one-, two- and three-term fits ... then read the tension report and the
  termination record". Problem: the script prints summary tables with its own column heads
  ("reach beta_k", "gap G_k", "bound", "term shares") and not the record; two readers guessed the
  heads and one had to find `fit.estimator.termination_` from an earlier block. Constraint: the
  paragraph says what the script prints (the per-K summary and its columns, the per-term record,
  the fixed-temperature diagnostic, the seed check) and gives the one line that returns the
  record of a fit from the page's own objects (`fit.estimator.termination_`), with the
  Termination page as the place its fields are read; no new output.
- **DCR-9** (the root page, the subtitle). Local; the docs stream (`site/index.html`). Passage:
  "An unsupervised learning method which applies a posynomial invariant form to learn the shape
  of a trade space from evaluated designs." Problem: the method's name is the only term on the
  page not said in plain words; the docs home says it one click later. Constraint: one clause
  of the docs home's words (a sum of terms, each a product of powers of the metrics) in the
  subtitle or the paragraph below it; nothing else on the root page changes.

### For the PM

- The glossary's "share" (DCR-3): three quantities under one word; the entry is the PM's.
- DCR-1 and the paper's CR-23 describe the same fits (the Examples page's three-term paragraph
  mirrors the paper's Section 9 numbers at re-selected temperatures); the docs follow the Fitting
  page's rule whatever the paper decides, and the two streams should land their sentences knowing
  of each other.
- `k_terms.py` (DCR-5) is under `examples/adcs/`, not a docs-stream file.
- The next round's task wording names the page ("the first fit on the Getting started page";
  "the cubesat study on the Examples page").

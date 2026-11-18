# Final reader round, wave 3: the assistant's triage against answer key version 5

Head read: c23cf60. Reports: `../reports/{G20,G04,F09,F02,F26,F13,G24}.md`, committed verbatim at ea0132d before this
triage. Forms as in `wave-1.md`; counting rules the same. Models: m1 Sonnet (G20, F02, F13, G24), m2 Haiku (G04, F09,
F26). Change requests continue wave 2's numbering at 48.

## G20 (P7-C, wording 2, Sonnet)

- Key marks: S3 to S9 stated correctly, with the case's numbers (seven-metric K = 1 set, 8 and 7 at K = 2, shares 0.74
  and 0.26, the -0.9 elasticity, 28 designs, 0.56 M USD, 16 of 20 planted tables, three proposals of two designs);
  S7 stated (toy; cost model's exclusions; not causal; hypotheses are human validation); S8 stated (no novelty, no
  global optimum, search is future work, no rate from three proposals). The reader marks as his own the words
  "replacement for the weighted-criteria grid".
- Wrong beliefs: none. W1, W2, W3, W6 avoided in so many words.
- Depth job: done, with whys owed (below).
- Findings that count: fleet size "a count that is no part and is not drawn" (6.20; F09 (62), G24 (30): three cells);
  "frontier" for which of Definition 1's three objects (6.7; F09 (36), G24 (9): three cells); F- and I-codes and
  "restrict nothing" (6.14; F09 (48, 107): three cells); the Final remark's novelty score against Section 10 (6.43;
  F09 (93), G24 (46): three cells); Section 7's "resembles a diffusion with drift" (6.19; F09 (61), G24 (29): three
  cells); Table 2's level column read as a ranking of rows that differ by less than the band (6.35, 6.36; F09 (88),
  G24 (44): three cells); the selection-rule sentence "gives up the least ... among the 5 of the 28" (6.34; F09 (87):
  two cells); thresholds "read from the data's pass fractions" (6.23; F09 (66): two cells); the elasticity's units
  (6.12; G24 (17, 38): two cells); Figure 4's saturated colour scale (6.27; F13 (8), G24 (33): three cells);
  n_eff = 74 with no word on the exponents' stability (6.26; F02 (7), F13 (7), G24 (32): four cells). Counted
  already: "three terms" (6.13), 63.7 % (6.24), "five metrics" (6.40), "certified" (6.18), machine-checked (6.42),
  near-collinear metrics (6.21), Figure 8's selection (6.33), 0.56 M (6.34), the regressor's band (6.38), 3 of 3
  (6.37). Logged: tau printed 42 and 41.7 (6.26); "the terms add a model" unverified (6.32; G24 (37): two cells, for
  the supervisor); Theorem 9 as a headline (6.4; G24 (21): for the supervisor); theorem references ahead of their
  statements (6.5); the scaling-all-metrics reading of V - 1 (6.39); "Loading" placeholders and garbled math in the
  text extraction (slice artefacts, the README's incidents).

## G04 (P4-A, wording 2, Haiku)

- Key marks: S1 stated; S2 stated (surface as a model of the data, not the Pareto boundary; the chart; n-lemma with
  elasticities; composes with PCA); supports a trade study; the finding stated; wants to read on, for the PCA
  composition as a testable pipeline claim.
- Wrong beliefs: none; W4 avoided ("meant to sit beside PCA rather than replace it").
- Depth job: done.
- Findings: the abstract's phrases (the same set, with "solved directly" read as closed form and "kernel" in the ML
  sense); for the supervisor, six cells now (G26, F19, F04, F03, G04, F26).

## F09 (P2-C, wording 1, Haiku)

- Key marks: S3 to S9 stated correctly (the three objects of Definition 1; convex one-term fit, uniqueness not claimed;
  weak efficiency over the set S, converse not claimed; three levels and the soft certificate; the K = 2 margin
  against the band; Q1 to Q4; no novelty; the search has no results).
- Wrong beliefs: none.
- Depth job: done, with four whys owed that the reader names (the soft certificate's status, fleet size, the triples'
  selection, the derivation claims); each has a request below or in waves 1 and 2.
- Findings that count: "the package" before anything says what it is (6.39, 6.53, 6.76; F02 (22), F13 (15), G24
  (12): four cells); "reach" and "offset" for one object (6.43; the glossary's "level offset" names another); A1's
  strictly positive metrics against the package's dropped zero rows (6.38; G24 (18): two cells); Section 10's heading
  "what the contrast does" with no contrast introduced (6.90); Theorem 12's exact first-order hypothesis against a
  numerical "certified" (6.56, 6.57: sharpens request 21); Section 7's monotonicity "stated but without a lemma"
  (6.60; with 6.61 the diffusion sentence); the fleet size (6.62); Figure 3's settling time (6.64; six cells now);
  thresholds from pass fractions (6.66); Figure 8's selection (6.81: counted); 0.56 M (6.86: counted); the rule
  sentence (6.87); the level column (6.88); the Final remark (6.93); the abstract's "unsupervised feature engineering"
  beside Section 2's "not a PCA of any kind" and the kernel sentence beside Section 12's "Nothing here is built"
  (6.32, 6.33: for the supervisor). Counted already: thresholds (6.41), participation (6.69), R1 "one point" (6.73),
  Theorem 11 (6.55), band 0.0935 (6.83), 3 of 3 (6.84, 6.85), "five metrics" (6.89), machine-checked (6.94, 6.95).
  Logged: the pseudoinverse's superscript plus (6.51); Proposition 2 as a Proposition (6.52); "claims nothing as novel"
  beside "our design" (6.34).

## F02 (P2-B, wording 1, Sonnet)

- Key marks: S4 stated (pieces, dilemma and trilemma); S5's three levels and the soft certificate stated with the
  paper's hedges; S6's main results stated (V doubles; the three objects; convexity; elasticities; weak efficiency;
  log-mean-exp; the noise ridge; two terms separate; PCA on the chart as a reading); S8 stated (does not rank; no
  novelty; not PCA or Pareto). One mis-stated detail outside the W list: "thirteen requirements read from a system
  model" (the model states six); the skim slice's Figure 3 caption is the likely source. Not a wrong belief of the key.
- Wrong beliefs: none. W5 and W7 avoided (6.1: "a property of a fitted exponent vector"); W9 avoided.
- Depth job: done.
- Findings that count: n_eff = 74 (6.7); Figure 5 (6.10: seven cells now with F12, G08, G21, F13, G24); "the package"
  (6.22); the score undefined where Definition 7 uses it (6.25; F09's guessed terms: two cells); terms possibly
  "labelled arbitrarily" (6.15: the share order is stated nowhere in the main text or the supporting material; a
  W11 guard); Figure 8's "typical size" and "at a fixed total" (6.16; F13 (14): two cells) and the single-metric
  corner (6.16; F13 (13): two cells); "binds alone" (6.16; F13 (2): two cells); "blends" undefined beside the
  "Numerical" tag (6.20: joins request 32); Figure 1's face rule and "planted" (6.1, 6.2: join request 37). Counted
  already: Figure 3 (6.4), near-collinear metrics (6.8, 6.14), Figure 6 (6.11, 6.12), Definition 3 (6.22),
  thresholds (6.24), Theorem 10 (6.29), Theorem 11 (6.30). Logged: the n-lemma name at eight metrics (6.13: for the
  supervisor, eight cells now); results before the case in the section order (6.34: for the supervisor, one cell);
  hypotheses labelled and not stated in the B slice (6.31: the slice); Table 1's body, Section 11 and equation (2)
  absent from the slice (6.24, 6.35, 6.36: the slice).

## F26 (P8-A, wording 1, Haiku)

- Key marks: S1 stated and welcomed; S2 stated; supports a trade study; the finding stated; wants to read on, to the
  cubesat section and the chart's definition.
- Wrong beliefs: none ("does not claim a performance comparison, a validated decision outcome, or an improvement over
  an existing trade-study practice").
- Depth job: done.
- Findings: the abstract's phrases (the same set); the abstract gives the executive no number from the case (one
  cell; for the supervisor beside the abstract).

## F13 (P7-B, wording 1, Sonnet)

- Key marks: S4 stated; S5's three levels, the soft certificate and the stopping declaration stated; S6's main results
  stated, including Figure 8's two regions by name; S8 stated. "A trilemma of three or more" is a loose reading of the
  n-lemma's count, not a wrong belief.
- Wrong beliefs: none. W6 avoided ("a demonstrator, not a design").
- Depth job: done.
- Findings that count: the main results' pointer after "every design's position and level, and each term's
  elasticities, are read from it" resolves to Definition 1, the three objects, which defines none of them (6.21: a
  dangling pointer); "binds alone" (6.2); fleet cost against unit cost, association -0.44 and -0.56 (6.6; G24 (30,
  Q): joins the fleet-size request); n_eff (6.7); Figure 4's scale (6.8); Figure 5 (6.9, 6.10: the slope is the
  exponent ratio, to be said); the single-metric corner and "typical size" (6.13, 6.14); "the package" (6.15).
  Counted already: Figure 3 (6.4), Figure 6 (6.11), Figure 7 (6.12), Theorem 10 (6.18), Theorem 11 (6.19). Logged:
  one slew as the control experiment (6.4: S7); the baseline failing two boxes (6.5: the key's S6, consistent);
  total mass at 0.02 (6.8); how the designs were sampled, absent from the B slice (6.23).

## G24 (P6-C, wording 2, Sonnet)

- Key marks: S3 to S9 stated correctly and in the frontier economist's own terms (a soft one-sided log-linear envelope
  by a convex program; the exact invertible chart; the nondominated counts 236 and 2,134; the K = 2 reading; 28
  designs; the priced question). The judgement "partly real, partly relabelling" is the reader's and allowed.
- Wrong beliefs: none. W2 avoided (6.28); W11 avoided (the share order read from the text's "term 1 carries most").
- Depth job: done, with whys owed (below).
- Findings that count: the fleet size and the fleet cost's relation to unit cost (6.30, Q7); "frontier" (6.9); "the
  package" (6.12); zero rows (6.18); the fit as a geometric program in the exponents against the GGP compatibility of
  Sections 10 and 12 with the metrics as variables (6.20: one cell, a real ambiguity); the elasticity's units and
  Theorem 7's pull-back unapplied (6.17, 6.38); Figure 4 (6.32, 6.33); Figure 5 ("a regression trend through the
  cloud's upper-middle, not an edge", 6.34); Figure 8's 286 triples (6.40: joins request 28); the level column (6.44);
  3 of 3 against "within 0.164 against the band 0.094" (6.45: two different quantities read as one; joins request
  43); the Final remark and V - 1 against log V (6.46); the diffusion sentence and Section 9's use of a "preliminary"
  loop (6.29). Counted already: R1's check (6.15), the K = 1 band at every K (6.13: the paper's own gap G-9), the
  machine-checked wording (6.22, 6.50), Theorem 11 (6.27), "certified" (6.28), the ill-posed refit (6.24), "five
  metrics" (6.48), "three terms" (6.42). For the supervisor: the "Contribution" sentence and the title's "Scaling"
  (6.3; F04: two cells); "hyperbolic" (6.8; five cells now); "invariant" in two senses (6.11; G20 (9), H01, H02: four
  cells); Theorem 9 as a standard scalarization property (6.21; G20 (4): two cells); what the fit adds to Table 2
  beyond a two-measure nondominated filter (6.43) and "the terms add a model" (6.37); D.5's "unchanged" as supports
  not exponents (6.16: his D.5 item); the Föllmer entry's "n.d." (6.51); order-m and quantile frontiers absent from
  Table 1 (6.6: a post-0.1 prior-art candidate). Logged: the estimand (6.1: Q4, stated as open); the LP vertex's
  support against a 7-lemma (6.14); Figure 6's sagging upper edge (6.35); no restarts study (6.26: the paper says so);
  the planted recovery as by construction (6.41).

## Roll-up, wave 3

| Cell | Report | Model | Key marks | Wrong beliefs | Depth job | Counting findings |
|---|---|---|---|---|---|---|
| P7-C | G20 | Sonnet | correct | none | done, whys owed | 11 replicated frictions |
| P4-A | G04 | Haiku | correct | none | done | 0 (abstract, to the supervisor) |
| P2-C | F09 | Haiku | correct | none | done, whys owed | 2 defects (pointerless contrast, offset), 9 frictions |
| P2-B | F02 | Sonnet | correct, 1 mis-stated detail | none | done | 7 frictions |
| P8-A | F26 | Haiku | correct | none | done | 0 (abstract, to the supervisor) |
| P7-B | F13 | Sonnet | correct | none | done | 1 defect (dangling pointer), 6 frictions |
| P6-C | G24 | Sonnet | correct | none | done, whys owed | 1 defect-grade ambiguity (GP in which variables), 10 frictions |

No wrong belief in twenty-one reports. Every depth's job done. Twelve new places, each stopping two to four readers
of different personas, join the list; the abstract, the title's two words, the n-lemma name and "invariant" keep
accumulating cells for the supervisor's close read.

## Change requests added at wave 3 (numbered after wave 2's 47; the same unit if it has not landed, else the next)

48. Section 12, Final remark: "could be given a novelty or impact score from how far above V = 1 it is forecast to
    sit" contradicts Section 10 ("not whether anyone wants it") and is unbacked; drop it, or narrow it to the
    forecast distance above the surface and say whether that is V - 1 or log V (the two appear in Section 10).
49. Section 7: "the procedure resembles a diffusion with drift along the tangent spaces" has no definition or result
    behind it; drop it or mark it a conjecture. "Outward monotonicity is stated for the exact maximum ... Neither
    maximum has a lemma here": say where it is stated (Section 6.3's open list) or write "conjectured".
50. Table 2's caption: say that the rows stand in the order of the rules, not of the level, and that the picks'
    levels differ by less than the K = 2 band 1/tau = 0.0088, so the level column does not order them.
51. Section 9, the executive paragraph: restate the rule in steps (the 28 that pass the six requirements and lie in
    both bands; of those, the 5 that no other beats on both executives' measures; of those, the one that gives up
    the least of either measure), so a reader can state it without D.19.
52. Section 8: "whose limits are read from the data's pass fractions, not a mission's" is read as circular; say the
    thresholds are illustrative, chosen from a ladder of pass fractions for an exploratory case (as Section 10 says),
    and point to D.17 for the values.
53. Section 9's -0.9 elasticity: say its units (conditioned log-metrics after the standard scaler) and whether the
    pull-back of Theorem 7 changes it (by the ratio of the two metrics' scales); extends request 29.
54. Audit "frontier" in the main text (Section 1, Theorem 9, "Why a frontier", "the four-metric frontier"): each use
    names one of Definition 1's three objects or is the defined "near-frontier band".
55. Section 6's preamble: say what the F and I codes are (the register's hypothesis families) and what "F5 and F10
    ... restrict nothing" means (hypotheses that hold throughout), or drop the sentence.
56. Figure 4's lower panel: the colour scale saturates (the top rows near-black from tau 3 to 25), so the sweep's
    change cannot be read; run the figure-review loop on the panel with the three readers' words (G20 (27), F13 (8),
    G24 (33)).
57. Section 5: "A row with a zero metric is left out of the fit" against A1's strictly positive metrics: say that A1
    is the model's hypothesis and the drop the package's handling, and whether the package warns.
58. "The package" (Definition 3, Theorem 8, Section 9): name it at first use (the scikit-learn estimator of Section 11
    and Appendix F) or write "the implementation".
59. "Offset" names beta in Section 6.2 ("each offset beta_k"), the estimator paragraph ("exponents and offsets") and
    the sentence before Theorem 1 ("moves the offset"), while the glossary's word is reach and its "level offset" is
    log V. Write reach for beta everywhere; keep or retire "level offset" as the glossary rules.
60. Section 10's heading "PCA, what the contrast does and does not claim": introduce the contrast (Section 2's
    comparison with PCA) in the paragraph's first sentence, or rename the heading.
61. Section 8, beside n_eff = 73.6: say what the record says about the K = 1 exponents' stability (D.15's movement
    under three resamples at K = 1, if the record holds it; else that it is not assessed), since four readers ask
    whether 74 effective designs suffice.
62. State where terms are first numbered (Definition 7 or Figure 7's caption) that terms are numbered by share,
    largest first (ties by cell size, then the first exponent); the rule is in the key and the code and nowhere in
    the paper.
63. Figure 8's legend and caption: gloss "typical size" (the metric's geometric mean over the table) and "at a fixed
    total" (the sum of the three scaled metrics), and one clause on a single-metric corner (that metric alone raises
    V there; nothing trades).
64. Definition 7 uses "scores" before Section 5 defines s_i = w . u_i; define the score where it is first used.
65. Figure 1's caption: "one metric binds alone" uses a constraint word; the glossary's verb is contends.
66. Main results, item 1: the pointer after "are read from it" resolves to Definition 1 (the three objects); point to
    the definitions of the chart, the level and the elasticity.
67. Theorem 3 and Sections 10 and 12: one clause that the fit is a geometric program in the exponents (x = e^w), and
    that the GGP compatibility of Sections 10 and 12 concerns the model as a constraint with the metrics as
    variables; say which at each mention.
68. Section 8: "the fleet size, a count that is no part and is not drawn" reads as "not sampled"; say it is not drawn
    in Figure 2's assembly view, being no part, and is a configuration variable drawn from 1 to 30; and say how the
    fleet cost is formed from the unit cost and the fleet size, so a reader sees why the two metrics are not
    collinear (associations -0.44 and -0.56 in Figure 7).

Earlier requests gaining cells or precision at wave 3: 21 (F09 (56): the stopping declaration should say the
numerical certificate checks Theorem 12's second-order test at a point meeting the first-order conditions within
tolerance, which the theorem's exact hypothesis does not cover); 26 (six cells); 28 (G24: say how many of the 286
triples met the criterion); 32 (gloss "blends"); 36 (seven cells; two readers see a trend line through the cloud, not
an edge: the figure-review loop, shows and does not show, with the slope named as the exponent ratio); 37 (F02's
"planted" question); 43 (G24: the predicted-against-measured difference and the measured log V against zero are two
quantities; say both); 46, 47 (cells).

For the supervisor (entry surfaces and his own text; not applied here):
- The abstract: six cells now (G26, F19, F04, F03, G04, F26); the same phrases. Two claims matters among them: "any
  kernel that keeps that compatibility generalizes the method" while Section 12 says nothing is built (F09, G24,
  F26); "unsupervised feature engineering" beside Section 2's "not a PCA of any kind" (F09). F26: the abstract gives
  the executive no number from the case.
- The title: "Scaling" (F04, G24: read as computational scale; G24 adds that the "Contribution" sentence reads as a
  purpose and that near-all-nondominated in 13 dimensions is generic for random draws); "hyperbolic" (five cells).
- "Invariant" in two senses (scale-covariant V; constant along a trade-off): G20, G24, H01, H02.
- The n-lemma name beside "Lemma 1", "2-lemma" and "8-lemma": eight cells.
- Section 9's elasticity across stepped metrics: F12, G20, G24, F09 (four cells).
- Theorem 9 in the main results: two mathematically literate readers (G20, G24) call weak efficiency of a monotone
  aggregate's maximizer standard and ask why it is a headline. A marginal-value question for his call.
- The decision section: G24 asks what the fit adds to Table 2 beyond a two-measure nondominated filter (the answer
  is the near-frontier band, which is the fit's); G20 and G24 ask what "the terms add a model" adds beyond a
  clustering (the sentence says: elasticities and a level). Whether one sentence each should say so is his call.
- D.5's "unchanged" (supports, not exponents): G24, joining his D.5 item.
- Works cited: the Föllmer entry is "n.d." with a documented reason (G24); Föllmer and Schied's book states the
  entropic risk measure with a DOI, if he prefers a dated source.
- Post-0.1 prior-art candidate: partial and robust frontiers (order-m, quantile frontiers), raised by the frontier
  economist as the family a 10 percent convention belongs beside (G24).
- Structure: results before the case in the section order (F02, one cell).

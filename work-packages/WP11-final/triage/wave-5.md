# Final reader round, wave 5: the assistant's triage against answer key version 5

Head read: c23cf60. Reports: `../reports/{F22,G25,G05,F16,F14,G06,F28}.md`, committed verbatim at bc5e724 before this
triage (finished 13:49 to 13:55 UTC; committed by the assistant, PM15 being silent since 13:55). Forms as in
`wave-1.md`; counting rules the same. Models: m1 Sonnet (F16, F14), m2 Haiku (F22, G25, G05, G06, F28). Change
requests continue at 93. Findings the wave-1 unit (c42d860) has already landed are marked "landed" and not counted.

## F22 (P3-B, wording 1, Haiku)

- Key marks: S4, S5's three levels and the soft certificate, S6's main results and S8 stated correctly; Figure 5's
  slope checked against Figure 4's exponents.
- Wrong beliefs: none.
- Depth job: done.
- Findings that count: Figure 3's caption rule ("an orange line from each to the traded metric it reads") against
  its own exception (total mass through the launch cost) (6.10; G05 (3): joins 26, twelve cells); Figure 5's caption
  "within 0.1 of that median" against the legend's "within 0.1 in log V" (6.12; joins 36); the main results'
  "conditional local optimality" without "the cells held fixed" (6.34); the stopping declaration unnamed in the main
  results (6.36; joins 80); n_k as a function of the 1e-9 tolerance (6.24; G06 (10): joins 19). Landed: Figure 1's
  rounding (6.1), the stray "enlarge" (6.11). Counted already: Figure 3 (6.2), Figure 4's legibility (6.3), Figure
  6's "energy" (6.13), Figure 7's thresholds (6.14), Figure 8's legend (6.7), "binds" (6.8), Definition 1's table
  (6.20), "the package" (6.22), f_k's scope (6.23), the facet-normal reading (6.27), Theorem 12 (6.33), "the rates"
  (6.35), the hypothesis codes (6.37). Logged: Figure 6's principal direction's sign (6.5); u undefined in the B
  slice (6.21: Section 3 defines it).

## G25 (P7-D, wording 2, Haiku)

- Key marks: S3 to S9 stated correctly with the appendices' numbers (D.11's 345 of 817 moving quantities; D.14's four
  failures by seed; C.8's exclusions; H's hypotheses); S7 and S8 stated.
- Wrong beliefs: none. W2 avoided ("certified is the highest level" as a status); W6 avoided.
- Depth job: seven pointers followed, six found; D.15's body did not render when opened (a rendering incident for the
  README); no proof followed to its script lines (no shell by the brief).
- Findings that count: "nearly one axis (Spearman at least 0.97)" against C.5's one-axis rule at 0.99, the two metrics
  at 0.98 and 0.97 (6.18; G06 (2): two cells); the fourth threshold named three ways (6.20; G06 (28): two cells);
  Figure 3's thirteen requirement boxes against six (6.19; joins 69, five cells); the shortlist's band (6.30; joins
  70); total mass at the fit temperature (6.25; joins 73, five cells); Z and the principal direction both "position
  along the surface" (6.26; joins 41); Figure 7's term-2 panel: eight black labels counted against "7-lemma" (6.24;
  joins 87's loop); Theorem 12's sketch checked by finite differences on an instance yet labelled Derived (6.16; F14
  (20): two cells); "the package's checks pick K = 2" against D.15's "no check decides K alone" (Q; G06 (33): two
  cells); Section 8's planted sentence reading as near-complete recovery (6.22); C.8's uncosted launch slot for fleets
  below four (6.33); Section 2's HoroPCA sentence without H's limits (6.34); Figure 8's "favours" (6.27; G05 (8),
  H01, H02: four cells); the alt text "<Figure size 800x700 with 4 Axes>" on the inline figures (6.1; G06 (51): two
  cells, verified on the rebuilt page: Figures 4, 5 and 7). Landed: "three terms" (6.9). Counted already: the three
  objects (6.1), hyperbolic (6.3), Definition 3 (6.4), the GP's variables (6.5), thresholds (6.6), the ill-posed refit
  (6.7), Figure 1's rule (6.8), zero rows (6.11), the F-codes (6.12), L14 (6.13), machine-checked (6.14), the kernel
  sentence (6.15), "two enter no contending set" (6.17), Figure 3's box (6.21), Figure 5 (6.23: the axis units "W"
  and "inverse USD" cannot be literal after conditioning), 0.56 M (6.28), "five metrics" (6.29), the band 0.0935
  (6.31), R1 (6.32). Logged: the Contribution count (6.2); "scaler" read as a typo (6.11; F28 (m): a gloss); "Loading"
  on first load (6.1: incidents).

## G05 (P5-B, wording 2, Haiku)

- Key marks: S4, S5, S6's main results and S8 stated correctly; Theorems 2, 3, 5, 6, 7, 8, 9, Lemmas 1 and 2,
  Corollary 2 and Proposition 2 checked by hand from their statements and found right.
- Wrong beliefs: none.
- Depth job: done.
- Findings that count: Theorem 10 (i)'s argument needs the minimum over all symmetric points, not one symmetric point
  (6.24; F14 (22): two cells); Theorem 11's finite stop: non-increase over finitely many partitions does not rule out
  cycling at equal F (6.25); Corollary 1's expectation inside the logarithm (6.27; F14 (14), F05 (21): three cells);
  Theorem 12's H in which variables, the soft weights' derivatives (6.26; joins 115); the main results' first sentence
  true at K = 1 only (6.11); "over S" dropped from the main results' Theorem 9 line (6.23); which kappa the K = 2
  figures use, and Definition 3's shift changing levels (6.16, 3.3; F14 (5)); Figure 8's panel B diamond possibly
  inside the edge (6.8; joins 132: a region's label names the leading pair); Proposition 3's conditioning given Lemma
  2 (6.30; joins 111). Counted already: Figure 1's rule (6.1), Figure 3 (6.3), the 10 percent convention and n_eff
  (6.4), Figure 6's two positions (6.6), near-collinear metrics and selection-induced association (6.7: for the
  supervisor, two cells now), "executives' measures" (6.9), the GP's variables (6.12), "certificate" (6.13), Definition
  1's table (6.15), f_k's scope (6.19), the facet-normal reading (6.22). Logged: Figure 7's ten-design drawing
  threshold against a 13 by 13 correlation of rank at most nine (6.7: for the supervisor, the figure's rule); Definition
  9's tangent space (6.21); "13 Acknowledgments and process" as a heading (6.10).

## F16 (P3-A, wording 1, Sonnet)

- Key marks: S1 stated; S2 stated (surface as a model of the data, not the Pareto boundary; the chart reversible;
  terms with elasticities; composes with PCA); supports a trade study; the finding stated; wants to read on, for the
  input contract.
- Wrong beliefs: none; W1 avoided ("It does not choose a design").
- Depth job: done.
- Findings: the abstract's phrases (eight cells now); "Scaling" read as computational scale (F04, G24, F16: three
  cells); the input contract absent from the abstract (positivity, orientation, how many designs), the evaluator's
  own question. For the supervisor.

## F14 (P9-C, wording 1, Sonnet)

- Key marks: Sections 3 to 6 stated correctly and in full (every theorem's content, the case's margin numbers, the
  open questions); S7's conditioning dependence stated; S8 stated.
- Wrong beliefs: none.
- Depth job: done, with whys owed, most of them precision defects in the statements (below). The most exacting read of
  Sections 3 to 6 in the round.
- Findings that count: "flat in log space piece by piece" only at kappa = infinity (6.1); R2's "energy differential of
  design i against term k" for s_ik (6.4); R1 to R3's pronoun, quantifier, use and "clean fit" (6.7; F28 (u)); three
  notations for J_tau (6.8); Lemma 1's KKT against Theorem 2's (6.11); the notation collisions k, c, s, alpha, m, x,
  Delta, N, p (6.23; F21 (13), F28 (j, s)); Theorem 5's hyperplane hypothesis, quantifier and sketch (6.15); Theorem
  6's K > 1 clause and B's non-uniqueness (6.16; F21 (19), F28 (y), G06 (16): four cells); Theorem 7's sketch (6.17);
  Theorem 8's x_k and the kappa = infinity case (6.18); "active term" (6.19; F28 (z)); label, cell and A8's partition;
  Corollary 2 and Proposition 3 on W's argmax cells (6.21, 6.27; G05 (30), F28 (gg)); Theorem 10 (ii)'s fixed-weight
  objective and Jensen (6.22; F05 (17), F28 (cc)); Lemma 1's f_k* and A3 (6.25; F28 (ee)); the case sentence mixing
  score-space and parameter-space quantities (6.26); Theorem 12's D, M and objective (6.28); Corollary 1's A9 and P on
  a face (6.14). Landed: A3's range (6.3), Theorem 1's sketch (6.10), Theorem 11's hypotheses (6.24), "three terms"
  (6.30). Counted already: Definition 3 (6.5), Definition 6 (6.6), zero rows (6.9), the facet-normal reading (6.11),
  Theorem 4's mean (6.13), Theorem 8's "so" (6.18), Theorem 9's F-codes (6.19), Derived and Theorem 12's instance
  (6.20), Theorem 11's non-accepted iteration (6.24), Theorem 12 against the declaration (6.28, 6.29). Logged: A7 and
  A8 restate definitions (6.2: for the supervisor, his hypotheses list); "Rescaling one metric" against Proposition 1
  (6.9: a per-metric rescaling, correctly read); code lines before generated sentences in the DOM (6.30: hidden by
  CSS on the rendered page, verified; not on screen); Figure 1's 0.00 as rounding (6.32).

## G06 (P6-D, wording 2, Haiku)

- Key marks: S3 to S9 stated correctly with the appendices' numbers; Table 2's fleet-cost arithmetic checked (fleet
  times unit cost; the 0.56 M difference reproduced); the 47-times ratio checked; Corollary 1's tau/2 checked in the
  MathML.
- Wrong beliefs: none. W4 handled as the reader's own judgement ("a combination of known pieces").
- Depth job: seventeen pointers followed and found; no proof followed to its script lines.
- Findings that count: Corollary 1's hypotheses omit A10, which L18 uses (6.18; verified: A10 is in the axioms and
  L18, L20 import it; the main text lists A1 to A9); the Spearman rule (6.2; with G25); the fourth threshold's names
  (6.28; with G25); "pick K" (6.33; with G25); "log-convex" against "convex in u" (6.12; F28 (p): two cells); "the
  curvature is not positive" (6.21); "slack" negative beyond the surface (6.20); Figure 6's 36 percent computed for
  K = 1 (6.35; joins 41) and the fraction above zero not countable by eye (6.36: a check for 41); D.10's numbers
  behind "within 0.164" (6.42: proposals 1 and 3 at 0.00615, proposal 2 at 0.1641; joins 43 with the record);
  "novelty" against Appendix A's "not a measure of attainability" (6.47; joins 48); D.14's failed fits certified
  (8.11; joins 21: certified is local, which is what the word means); the alt text (6.51; with G25); "certificate" for
  the theorem and the status (6.22; joins 21); multiplicative DEA absent from the main text (6.4; joins 75, three
  cells); the DEA "hyperbolic graph measure" as a second sense of the title word (6.5; for the supervisor). Landed:
  Appendix E's G-1 (8.15), "five metrics" (6.45), the stray "enlarge" (6.30), Theorem 12's sign (6.21 partly).
  Counted already: the three objects (6.1, 6.6), the Contribution count (6.2, 6.3), Definition 3 (6.7), Definition 4
  (6.8), Definition 6 (6.9), "binds" (6.10), the F-codes (6.13), the facet-normal reading (6.14), "the rates" (6.15),
  Theorem 6 (6.16), L14 (6.19), the diffusion sentence (6.24), the fleet size (6.25), "two enter no contending set"
  (6.26), Figure 3's boxes (6.27), total mass (6.29), R1 (6.31), Figure 5 (6.32), the bands (6.34), Figure 7's label
  (6.37: for the supervisor), Figure 8 (6.38), the regressor's band (6.41), the rule sentence (6.43), 3 of 3 (6.46),
  the Final remark (6.48), machine-checked (6.49), uncited entries (6.50: joins 44). Logged: "identical columns"
  (6.39); the hole's rule (6.40: in the repository); the AI disclosure (6.52).

## F28 (P10-C, wording 1, Haiku)

- Key marks: Sections 3 to 6 stated correctly; the bands and the 47-times ratio checked; Proposition 2 checked;
  Theorem 5's factor checked.
- Wrong beliefs: none.
- Depth job: done, with whys owed (below).
- Findings that count: C used in R3 before Corollary 1 defines it (k); "kinks on the ridges" where the paper's word is
  seam and "ridge" is the noise term's (o); Theorem 4's "mean" (v; F14 (13)); "support" in three senses (aa; F21
  (24), F14 (23), G27, G21: five cells); "37 of the 2,134" and "the primary regime" before Section 8 (jj; F14 (30));
  "tangent" and "scaler" unexplained (m); "active term" (z); Corollary 2's minimum over weights with the cells fixed
  (gg); Theorem 6's K > 1 (y); "frontier" in Section 5 and Definition 7 (b, i: joins 54); Q1 "not pursued" against
  Open and the gap order (kk). Landed: A5 and A9 (a), the thresholds (g), "three terms" (n). Counted already: zero rows
  (c), the reach's three definitions (d), "invariant" (e), "the package" (f), Figure 1 (h), R1 (j, t, u), the GP's
  variables (l), the F-codes (q), L-numbers out of order (r), Theorem 1's k (s), "the rates" (w), "by" (x), Theorem 10
  (ii) (cc), Theorem 11's terms (dd), f_k* (ee), Proposition 3 (ff), Theorem 12's sign and the declaration (hh, ii).
  Logged: the proof and script boxes' length and the colour coding (layout: for the supervisor); F's minimization
  bringing the surface down (bb).

## Roll-up, wave 5

| Cell | Report | Model | Key marks | Wrong beliefs | Depth job | Counting findings |
|---|---|---|---|---|---|---|
| P3-B | F22 | Haiku | correct | none | done | 5 frictions, all joining earlier requests |
| P7-D | G25 | Haiku | correct | none | pointers found (6 of 7; D.15 did not render); no proof followed | 3 defects (Spearman rule; threshold's three names; alt text), 10 frictions |
| P5-B | G05 | Haiku | correct | none | done | 3 precision defects (Theorem 10 (i); Theorem 11's stop; Corollary 1's expectation), 6 frictions |
| P3-A | F16 | Sonnet | correct | none | done | 0 (abstract, to the supervisor) |
| P9-C | F14 | Sonnet | correct | none | done, whys owed | 14 precision defects in Sections 3 to 6, 6 frictions |
| P6-D | G06 | Haiku | correct | none | pointers found (17); no proof followed | 2 defects (A10 missing; Spearman rule), 9 frictions |
| P10-C | F28 | Haiku | correct | none | done, whys owed | 2 vocabulary defects ("ridges"; "support"), 9 frictions |

No wrong belief in thirty-five reports. The three mathematicians on Sections 3 to 6 (F14, G05, F28) return the
statements' precision defects the earlier waves only brushed: these are the second unit's record checks.

## Change requests added at wave 5 (numbered after wave 4's 92)

93. Theorem 12's sketch: separate what the script derives symbolically from the finite-difference check on an exact
    instance; "Derived" covers the former.
94. The inline figures' alt text (Figures 4, 5 and 7) is the matplotlib repr "<Figure size 800x700 with 4 Axes>";
    set the alt to the caption's first sentence.
95. Section 9: "the package's checks pick K = 2" becomes "point to K = 2" with D.15's own words (the largest drop in
    the mean slack, read against the other two checks; no check decides alone).
96. Main results, first sentence: "with one term" (V_K at K > 1 is the 1/kappa power of a sum).
97. Theorem 10 (i): the instance's value at distinct terms must be lower than the minimum over all symmetric points for
    the argument to show non-convexity; verify what L16 shows and state that.
98. Theorem 11's finite stop: say why non-increase over finitely many partitions stops (strict decrease on any
    reassignment unless the partition is fixed, with the tie rule), from L15.17 to L15.22.
99. Corollary 1: the expected noisy objective is log E exp (Proposition 2's cumulant), not the expectation of the
    objective; state A9 fully (independent across rows, one Sigma); write P for a face; Delta w against the simplex's
    Delta.
100. "Words" and Definition 1: "flat in log space piece by piece" holds at kappa = infinity; say so.
101. R2: "the energy differential of design i against term k" names s_ik; the glossary's energy differential is log V;
     call s_ik the score.
102. Section 5's R1 to R3: the pronoun "Its"; "an optimal dual weight vector" (some or every); where R1 is used
     (Theorem 2's remark; Section 9's check); "clean fit" defined (noise-free).
103. One notation for the objective: J_tau(w), J_tau(Uw) and J_tau(w; U + c) are three.
104. Lemma 1: say the KKT conditions are Theorem 2's applied to f_k (gradient U^T p minus the cell mean).
105. Notation audit (Appendix A and the main text): k (scalar in Theorem 1, term index), c (configuration,
     coefficient, shift), s (score, shift), alpha (conditioning exponent, soft weight), m (metric, eigenvalue), x (e^w,
     x_k), Delta (simplex, Delta w), N (designs, normal), p (dual vector, softmax weights): distinct letters where two
     meanings meet in one statement. The supervisor's notation convention (scikit-learn docs, Boyd and Vandenberghe)
     governs the choices.
106. Theorem 5: the hyperplane hypothesis is Definition 2 at K = 1 (drop it or say why it is listed); the quantifier
     on j; the sketch names the step that needs Theorem 2.
107. Theorem 6: hypotheses for the K > 1 clause (A6; Theorem 8's shift equivariance) and B as any orthonormal basis of
     the sum-zero space (Helmert in the code).
108. Theorem 7's sketch: where e^{w . b} comes from; verify against L9.
109. Theorem 8: rename x_k (it collides with x = e^w) and state the kappa = infinity case as the maximum, a generalized
     posynomial (I15), with its step.
110. Theorem 9 at K > 1: define "active term" (a term attaining the maximum at the maximizer).
111. Section 6.2: label, cell and A8's partition coincide for the sharp fit (argmax cells, ties by the rule); Corollary
     2 and Proposition 3 take A8's partition to be W's argmax cells.
112. Theorem 10 (ii): write the fixed-weight objective (with the entropy term if equality at the softmax needs it) and
     name the function Jensen is applied to; verify against L16.
113. Lemma 1: define f_k* (the minimum over the simplex) and list A3.
114. Section 6.2's case sentence: name which quantity the certificate bounds (score changes under half the margin;
     parameter changes under the radius) without mixing the two, and give the radius its own sentence.
115. Theorem 12: display the soft objective, define D and M or point to the step, and say in which variables H is
     taken; joins 40.
116. Section 8: "nearly one axis (Spearman at least 0.97)" against C.5's one-axis rule at 0.99, the two metrics at
     0.98 and 0.97: one rule, stated the same in both places.
117. One phrase for "log-convex", "convex in u" and "log-convex envelope", defined at first use.
118. Corollary 1's hypotheses: A10 (the attribute-noise axiom L18 and L20 use) is absent from Section 3's list and
     from the statement; add it or say why L20 does not need it.
119. The stopping declaration: "the curvature is not positive" becomes the test's condition (not positive definite on
     the tangent space of the active face).
120. R3 uses C before Corollary 1 defines it: define it there or point forward.
121. Section 5's conditioning sentence: gloss "tangent" (which term touches the data's edge there) and "scaler" (the
     per-metric scaling, scikit-learn's word).
122. Simplifying assumption (ii) "kinks on the ridges": the paper's word for where terms meet is seam; "ridge" is the
     noise term's word.
123. Theorem 4: "mean" is the arithmetic mean of the scores.
124. "Support" in three senses (the nonzero set; the 1e-9 set; the soft maximum over rows in Theorem 11 and Section
     6.2): the third becomes "reach" or "soft maximum".
125. Section 6.2's numerical paragraph: name the case at first mention ("the cubesat case of Section 8, primary regime,
     2,134 feasible designs").
126. The fourth threshold's name across Section 8 ("launch cost"), D.17 ("total mass 15.11 kg") and Figure 3
     ("LaunchBudgetRequirement"): one name, the launch budget read on total mass at 7,000 USD per kilogram.
127. Section 8's cost sentence: the launch slot is not costed for fleets below four (C.8), which understates launch cost
     for those fleets by 1.4 to 4.2 times; the decision table's fleets are four and more. The supervisor's eye (his
     cost model).
128. Section 2's HoroPCA sentence carries the reviewer's boundaries in one clause (a mechanism demonstration on clean
     tables; the embedding ours; the authors' code at its defaults, one direction). The supervisor's eye.
129. Section 8's planted-recovery sentence says "16 of 20 (Section 9)" rather than reading as near-complete recovery.
130. Main results: "conditional local optimality" gains "with the cells held fixed"; "a maximizer of V" gains "over the
     table".
131. Definition 3 or Section 9: say the fits of record are sharp (kappa = infinity) where a reader asks which kappa the
     K = 2 figures use.
132. Figure 8's caption: gloss "favours X" at a vertex (where that metric's share is largest) and say a region's label
     names its leading pair where a third exponent is small; the root page's figure shares the word.

Earlier requests gaining cells or precision at wave 5: 19 (n_k as a function of the 1e-9 tolerance); 21 (D.14's
failed fits are certified local minima, which is what the word means; "certificate" for the theorem and the status;
eleven cells); 26 (the caption's rule against the launch-cost exception; twelve cells); 36 (the caption's "within 0.1
of that median" against the legend's "within 0.1 in log V"; the axis units; ten cells); 40 (five cells); 41 (Z against
the principal direction need separate names; D.16's 36 percent is for K = 1; verify Figure 6's fraction above zero is
the convention's); 43 (from D.10: proposals 1 and 3 at log V 0.00615, proposal 2 at 0.1641: say two within the band
and one outside); 44 (G06 confirms); 46 (the LP minimiser's uniqueness); 48 (Appendix A's "not a measure of
attainability" belongs in the Discussion's V - 1 paragraph); 54, 57, 58, 63, 67 (five cells), 69 (five cells), 70, 73
(five cells), 75 (three cells), 78, 79, 80, 82, 84, 85, 86, 87 (G25's count of term 2's labels), 88.

For the supervisor (entry surfaces, his own text and vocabulary; not applied here):
- The abstract at eight cells; "Scaling" at three (F16 adds the input contract the evaluator looks for); "hyperbolic"
  at eight, with the DEA literature's "hyperbolic graph measure" as a second sense in the field (F06, G06);
  "invariant" at six; the n-lemma name at thirteen.
- Theorem 9: "over S" dropped in the main results (G05), with the four earlier cells.
- Figure 7's "association (negative: tension)": the label does the interpreting (G06), and selection near a surface
  induces negative association (F05, G05): two cells each. A claims matter for his reading.
- The DEA question in the frontier economists' words: "a combination of known pieces, and the main text does not make
  that comparison as sharply as the appendix does" (G06; F06, G24): request 75 is his to approve.
- Requests 127 (the launch slot below four satellites) and 128 (the HoroPCA sentence's boundaries) touch his cost model
  and the reviewer's judgement he pasted.
- Structure: the L-numbers out of reading order (four cells); the proof and script boxes' length (F28); A7 and A8
  restating definitions in the hypotheses list (F14); Figure 7's ten-design drawing threshold against a 13 by 13
  correlation (G05).
- Incidents for the README: D.15's body did not render for G25; "Loading" on first load for five readers now; the
  code cells are hidden by CSS on the rendered page (verified), so the "code as text" reports come from DOM
  extraction, not the screen.

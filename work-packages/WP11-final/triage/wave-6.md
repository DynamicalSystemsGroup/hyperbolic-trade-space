# Final reader round, wave 6: the assistant's triage against answer key version 5

Head read: c23cf60. Reports: `../reports/{G16,F07,G11,G12,G28,F24,F27}.md`, committed verbatim as each finished (6d32d81,
c9976cc, fec9662, 79de4a8, e2af6ae) before this triage. The wave was spawned by the assistant from the committed briefs
(PM15 held in a foreground call); models per `slots.tsv`: m1 Sonnet (G12, G28, G11, F07), m2 Haiku (F27, F24, G16).
Forms as in `wave-1.md`; counting rules the same. Requests continue at 133. Findings the wave-1 unit (c42d860) has
landed are marked "landed".

## G16 (P3-A, wording 2, Haiku)

- Key marks: S1, S2 (the surface as a model of the data; the chart; n-lemma with elasticities; composes with PCA),
  supports a trade study, the finding, wants to read on (for the input contract: positivity, direction, sampling
  near the edge).
- Wrong beliefs: none.
- Depth job: done.
- Findings: the abstract's phrases (ten cells now); the captured first screen's "IN THIS ARTICLE" chevron with no list
  (the slice's capture of a collapsed contents panel; the README's incidents).

## F07 (P8-B, wording 1, Sonnet)

- Key marks: S4, S5's three levels, S6's main results, S8 stated correctly ("the 10 percent is an input, not a
  finding").
- Wrong beliefs: none. W1 avoided; W6 avoided (the slew is simulated).
- Depth job: done. The executive would not read the whole paper: "it does not show me a decision that changed, a cost
  of adoption, or a number I can put in a budget line" (section 9): a reader-need finding on the decision section,
  for the supervisor.
- Findings that count: Figure 3's caption "the total mass is read through the launch cost" reads reversed against the
  figure's dashed arrow (6.3; G11 (3), G13: three cells; joins 26); Figure 7's panel title "exact-maximum support"
  against the caption's "contending set" (6.11); Figure 8's callouts read as physical findings (6.12; G11 (9): joins
  63); "if level is not a ranking and not a requirement margin, what would I do with it?" (6.13; joins 50 and the
  supervisor's "executive" item); the three levels out of order (6.15; joins 80); what a zero exponent means for a
  requirement (Q; joins 72). Counted already: Figure 3's count (6.2), Figure 4's scale and the 10 percent convention
  (6.4, 6.5), "regime" (6.6), Figure 5 (6.7, 6.8), Figure 6's "energy" and "36 % of it" (6.9, 6.10), Theorem 12
  (6.14), the hypothesis codes (6.16), Definition 1's three places (6.17), Definition 4's factor e (6.18), the share's
  dependence on the band (6.19), the "Numerical" tag (6.20), Section 7 (6.21).

## G11 (P4-B, wording 2, Sonnet)

- Key marks: S4, S5's three levels, S6's main results and S8 stated correctly; the k-means analogy drawn and bounded.
- Wrong beliefs: none.
- Depth job: done.
- Findings that count: Theorem 7's "negative w_j alpha_j marks a cost attribute" for a reader who knows the metrics are
  larger-is-better (6.24; F27 (6.7): two cells); Theorem 5's hyperplane hypothesis K = 1 only (6.23: landed); the five
  white rows as feature selection or incident (6.5; joins 72); Figure 3's launch-cost direction (6.3; joins 26);
  Figure 8's "where its V peaks" against the edge (6.9; joins 63 and 132); the two positions (6.19; joins 41).
  Counted already: "binds" (6.1), Figure 4 (6.4), Figure 5 (6.6), Figure 6 (6.7), Figure 7 (6.8), "executives'
  measures" (6.10), the pointer after "read from it" (6.12), the GP's variables (6.13), Definition 3 (6.15), the
  thresholds (6.17), "scores" (6.18), Theorem 1's k (6.20), the hypothesis codes (6.21), Theorem 9's zeros (6.25),
  Theorem 10 (6.26), Theorem 11 (6.27), Theorem 12 (6.28), L14 and the levels' order (6.29), "the rates" (6.30), the
  "Numerical" tag (6.31). Logged: Theorem 4 as a theorem on a par with the others (6.22: marginal value, for the
  supervisor); the estimator's interface absent from the B slice (Q1: Section 5's estimator paragraph is prose).

## G12 (P5-C, wording 2, Sonnet)

- Key marks: Sections 1 to 10 stated correctly, Derived, Numerical and Open kept apart; S7 and S8 stated.
- Wrong beliefs: none.
- Depth job: done, with whys owed, several of them precision defects (below).
- Findings that count: the main results' "(Theorem 1)" for the surface being V = 1 lands on homogeneity (6.3; F06
  (3), F27 (6.1): three cells); "ill-posed" for a convex problem that has minimizers (6.37; joins 135); Theorem 10
  (ii)'s descent not stated (6.35; joins 136); Section 10's "Three claims" stronger than Corollary 2 (6.58); the
  requirements-after-the-fit sentence untagged (6.57); Table 2's "distance" against Definition 2 (6.56); the 1/N
  sentence (6.26); the term gap as the Frank-Wolfe gap (6.40); slack negative beyond the surface (6.33; G06 (20): two
  cells); the simplex constraint in x = e^w (6.18; joins 67); V - 1 against log V for large v (6.61; joins 48);
  Theorem 5's dependency in the sketch (6.29; joins 106); Theorem 6's K > 1 clause unreadable (6.30; joins 107);
  Theorem 8's "posynomial" for a generalized one (6.31; joins 109); Theorem 11 (6.38; joins 98); the cell-centred
  objective against all-rows offsets (6.34; joins 20); the fraction above V = 1 monotone in tau (6.19: logged, D.1
  shows it). Counted already: the abstract (6.1, 6.2), Theorem 9's reading (6.4, 6.6, 6.32), the Contribution count
  (6.5), DEA (6.7), Definition 1 (6.8), "invariant" (6.9), Definition 3 (6.11), Definition 6 (6.13), the reach (6.14),
  R1 and the balanced point (6.15), zero rows (6.20), conditioning (6.21), the F-codes (6.23), "certified" (6.44,
  6.45), Section 7 (6.47, 6.48), the regressor's band (6.55), machine-checked (6.63). Logged: "Loading" figures (the
  incidents, six readers now).

## G28 (P10-C, wording 2, Sonnet)

- Key marks: Sections 3 to 6 stated correctly in a non-specialist's words; the equation (2) grouping checked; Lemma
  2's Cauchy-Schwarz checked; the 47-times ratio checked.
- Wrong beliefs: none.
- Depth job: done, with whys owed.
- Findings that count: "support" in three senses (6.48; joins 124); which kappa and level convention the K = 2 figures
  use (6.11; G13, G05: joins 131, three cells); Theorem 6's K > 1 clause (6.43; joins 107); "37 of the 2,134" and
  "primary regime" before Section 8 (6.63; joins 125); the three levels against the lemma numbers (6.55; joins 80);
  the reach's forward pointer and "their scores" without an antecedent (6.8, 6.19; joins 85 and 64); lambda in
  Theorem 2 as the average or the minimum (6.35, 6.57: one clause owed; joins 104); Definition 8 reads as a claim,
  not a definition, with the derivation in Theorem 5 (6.20: logged, for the supervisor's structure); Theorem 7's
  product sign (6.44; joins 146). Counted already: Definition 1 (6.5, 6.6), "invariant" (6.7), "energy differential"
  (6.9, 6.14), Definition 3 (6.11), Definition 6 (6.15 to 6.17), Figure 1 (6.18), R1 to R3 (6.22 to 6.24), the F-codes
  (6.24b), the GP (6.25), the 10 percent convention (6.26), zero rows (6.27), the thresholds (6.28), "three terms"
  (6.30: landed), L-numbers (6.31), Theorem 1's k (6.32), Corollary 1 (6.41), Theorem 12 (6.61), the stopping
  declaration (6.62). Logged: Section 3's assumptions as one run-on paragraph (6.2), the three families of conditions
  split across sections (6.3), proofs numbered apart from statements (6.33), Figure 1's legend colours against the
  numbering (6.18): structure, for the supervisor.

## F24 (P6-C, wording 1, Haiku)

- Key marks: S3 to S9 stated correctly; the 47-times arithmetic checked.
- Wrong beliefs: none. W4 handled as the reader's own question.
- Depth job: done, with whys owed.
- Findings that count: "nears the whole table" for 2,134 of 2,134 (6.2; G03 (1), G25 (2): three cells); the
  nondominated counts on attributes or conditioned metrics (6.19); "leads a term of its own" without the term's number
  (6.22); no designs visible above zero in Figure 6 (6.24; G06 (36): joins 141); "log-convex envelope" against
  "piecewise log-linear" (6.6; joins 117); the abstract's "a few" against Section 5's tenth (6.1; F20 (1): two cells);
  Theorem 12 Derived against measured (6.12, 6.14; joins 93). Counted already: hyperbolic (6.3), HoroPCA (6.4),
  Candès (6.5), Definition 3 (6.7), the thresholds (6.8), zero rows (6.9), R1 (6.10), "ridges" (6.11), Theorem 11
  (6.13), the declaration (6.15), Section 7 (6.17), the fleet size (6.18), the requirements against feasibility
  (6.20), "enlarge" (6.21: landed), the regressor's band (6.23), Figure 8 (6.25), "five metrics" (6.26: landed), 3 of
  3 (6.27), the Final remark (6.28), Föllmer (6.30: for the supervisor, three cells).

## F27 (P9-D, wording 1, Haiku)

- Key marks: S3 to S9 stated correctly with the appendices' numbers; every theorem's content; the case's D.19 choices
  recomputed and found to agree; the -0.9 elasticity checked as -0.216/0.250.
- Wrong beliefs: none. W2 named and avoided ("certified ... not a mathematical certificate in the sense of a proof").
- Depth job: twenty-nine pointers followed, nearly all found; ledger lines read for twelve lemmas (L1 to L5, L12 to
  L14, L16, L17, L19, L20); no script run (no shell). The best depth-D read of the round and the one that crosses the
  appendices against each other.
- Findings that count (verified where marked): Theorem 10 (ii)'s L16.43 proves F <= G_alpha - E with E the entropy
  term, which the main text drops (6.9; verified in `derivation/lemma_16_soft_alternation.py` line 312); no record
  checks R1 (6.11); the own-rows refit "ill-posed" against the contending set's estimator (6.5); Appendix E against
  D.1, D.2, D.11, D.13 and D.14 (6.36 to 6.39: the unit regenerated most of E at c42d860; G-17 was not in its list);
  D.19's nondominated counts (6.28); the SLSQP polish absent from the described algorithm (6.12); the finite stop as
  a pigeonhole (6.13); Figure 4's outlined column at the sweep point 42.06 against the fit's 41.72 (6.24; G20 (26):
  two cells); Figure 6's level at K = 2 (6.25); the launch understatement's convention (6.20); the regimes' Kp ranges
  (6.18); Theorem 7's sign (6.7); B.3's "no premise hides" against the signed-symbol column (6.42); L19 unused (6.45);
  D.18's factor (section 5); D.14's certified failures (section 5; joins 21); Appendix A's V row and "balanced point"
  missing (6.2, 6.34); the regressor's band as the four-metric view's tau (6.27; joins 47); "3 of 3" counting one
  configuration twice (6.27; joins 43); the zero-row count (6.44; joins 57); the fleet size against C.1's range (6.15;
  joins 68); the fourth threshold (6.17; joins 126); the K choice as a judgement (6.21; joins 95); contending against
  participating (6.22; joins 73); Corollary 1's object and "noise small" (6.6; joins 99); Theorem 9's S (6.8; joins
  130); the names (6.34; joins 59, 54, 124). Landed: 63.7 (6.16), Theorem 2's R1 clause (6.4), "three terms" (6.10),
  Figure 8's count (6.26). For the supervisor: "machine-checked" against Appendix B's "not formal verification" and
  160 of 505 steps applying posited axioms (6.30); the weaker novelty claim (6.31; three cells); "hyperbolic" (6.33);
  the HoroPCA sentence's spike (6.32; joins 128).

## Roll-up, wave 6

| Cell | Report | Model | Key marks | Wrong beliefs | Depth job | Counting findings |
|---|---|---|---|---|---|---|
| P3-A | G16 | Haiku | correct | none | done | 0 (abstract, to the supervisor) |
| P8-B | F07 | Sonnet | correct | none | done | 6 frictions; a reader-need verdict for the supervisor |
| P4-B | G11 | Sonnet | correct | none | done | 1 defect (Theorem 7's sign), 5 frictions |
| P5-C | G12 | Sonnet | correct | none | done, whys owed | 4 defects, 10 frictions |
| P10-C | G28 | Sonnet | correct | none | done, whys owed | 9 frictions, all joining earlier requests |
| P6-C | F24 | Haiku | correct | none | done, whys owed | 2 defects ("nears"; the term's number), 5 frictions |
| P9-D | F27 | Haiku | correct | none | pointers found; ledger lines read; no script run | 9 defects across the appendices, 12 frictions |

No wrong belief in forty-two reports. One loose statement (G13's "designs above the surface are beyond what the
sample reached", in wave 7) is noted there.

## Change requests added at wave 6 (numbered after wave 5's 132)

133. Main results, item 1: the pointer after "The fitted reference surface is where the invariant value ... equals
     one" lands on Theorem 1 (homogeneity); point to Definition 2, and to Section 5 for the fit.
134. Section 1: "its nondominated set nears the whole table" where the count is the whole table (2,134 of 2,134):
     "is the whole table"; and say the counts are on the conditioned metrics, larger is better.
135. Definition 6 against Section 6.2 and D.13: say how the contending set's estimator (the cell's rows centred on
     their own mean, tau = infinity: D.13's support refit) differs from the own-rows refit D.13 found not to recover
     planted terms, with D.13's two counts; and replace "ill-posed" by what D.13 observed, since the problem is convex
     and has minimizers (extends 20; four cells).
136. Theorem 10 (ii): state the bound as L16.43 proves it, F <= G_alpha - E, and define E (the mean entropy of the
     weights over kappa); the main text drops E (extends 112; verified in the script).
137. Section 9's "R1 of Section 5 holds on both regimes": no record checks R1; produce the check (the balanced point
     and the facet normal at tau = infinity, per regime) as a D-table and cite it, or narrow the sentence to what is
     checked (extends 46 to a claims defect; four cells).
138. Appendix B.2 and Section 6.2: say that the implementation polishes the alternation's stop (G-16 names SLSQP) if
     that is the code of record, so the algorithm described is the one whose status is reported.
139. Theorem 11's finite stop: say the finiteness is combinatorial (a pigeonhole over the K^N partitions, L15.22), not a
     practical stopping guarantee; D.14's iteration-cap runs, if the record has them (extends 98).
140. Figure 4's caption: the outlined column is the sweep point nearest the fit temperature (42.06; unit cost 0.26),
     not the fit of record (41.72; 0.2571); say so.
141. Figure 6's caption: name the level plotted (the K = 2 fit's log V, so its surface is the line by construction)
     and verify the fraction of designs above zero against the convention; two readers see none (extends 41).
142. D.19 against Section 9's counts: "548 designs that pass the six requirements, 11 nondominated on pointing error
     and fleet cost, 1 within the band of both fits" against the shortlist's eight nondominated among the 28: say the
     two sets differ (the 548 and the 28), or reconcile the counts.
143. Appendix E against D.1, D.2, D.11, D.13 and D.14 (tau by K and regime; G-7's recovery counts against D.13's
     largest error and D.14's 16 of 20; G-17's 346 against D.11's 345): the unit regenerated E's cubesat rows at
     c42d860; verify on the rebuilt page that every row F27 names now matches D, G-17 included (extends 11).
144. Section 8's launch understatement: state the convention ("understated by X times" as the slot over the reported
     launch cost), or give true over reported. The supervisor's cost model.
145. Sections 8 and 9: the regimes differ in the sampled gain range (C.1: Kp 0.2 to 2 primary, 0.03 to 1 stock); "two
     regimes of the same design problem" and "separates the problem's contribution from the gains'" say so. The
     supervisor's case model.
146. Theorem 7: "negative w_j alpha_j marks a cost attribute" fails at w_j = 0; the sign that marks a cost is alpha_j's.
147. Appendix B.3: "No premise hides in a signed symbol" against the per-file column of signed symbols declared as
     hypotheses: say they are declared premises, listed per file, and that L14's minimality enters as the sign of dfk.
148. L19 (the crossover tau*): say where it is used, or list it as unused.
149. D.18's text: give the factor by which the ridge prediction exceeds the measurement where it does, not "exceeds".
150. Appendix A: add "balanced point"; the "invariant value" row carries V without e^{-beta} while Definition 2 has
     it (the register row of wave 1's item 3).
151. Section 9: "peak slew power ... leads a term of its own" names the term (term 1).
152. Figure 3's caption: the direction of the launch-cost link (launch cost computed from total mass; the launch
     budget requirement reads launch cost), since "the total mass is read through the launch cost" reads reversed
     against the dashed arrow (extends 26; three cells).
153. Figure 7's panel titles: "exact-maximum support" and the caption's "contending set" name one object; one name.
154. Section 5's convention sentence: "a tenth" is where the abstract's "a few" is redeemed; say "about a tenth, by
     convention" there (the abstract's phrase is the supervisor's).
155. Section 10, "Three claims": "That the optimizer reached a local minimizer of the objective is the certificate" is
     stronger than Corollary 2's bound with the cells fixed and Proposition 3 at the exact minimizers; say what the
     certificate covers (extends 21).
156. Section 10's requirements-after-the-fit sentence carries no Derived, Numerical or Open tag where the others do.
157. Table 2's caption: "the distance above or below" for log V against Definition 2's "not a Euclidean distance":
     "the level".
158. Section 5: "making it a property of the shape of the data, not the number of designs" attributes more to the
     1/N than it does (the minimizer is unchanged; the offset moves by (log N)/tau).
159. Lemma 1: name the gap as the Frank-Wolfe gap in one clause.
160. Section 6.2: "slack" is negative for a design beyond the surface; say so where it is defined (two cells).
161. Definition 6: the 1e-9 threshold is a convention and the exact-maximum support can be non-unique; one clause that
     the support is checked under jitter (D.11) and how ties are read (extends 19; three cells).

Earlier requests gaining cells or precision at wave 6: 19, 20, 21 (D.14's certified failures; "Three claims"), 26
(twelve cells, the arrow's direction), 36 (F07, G11, G13: the 0.1 in log V is 0.4 on the axis), 41 (which level;
the fraction above zero), 42, 43 (one configuration counted twice), 46 (now 137), 47 (the four-metric view's tau from
D.5), 48, 49, 54, 56 (the sweep's columns evenly spaced on a log scale: G13), 57 (the dropped-row count), 58, 59, 63,
67, 68 (C.1's range 1 to 30), 72, 73, 80, 85, 86, 93, 95, 98, 99, 104 (lambda as the average or the minimum), 105,
106, 107 (four cells), 109, 112 (now 136), 116, 117, 124, 125, 126, 128 (the spike), 130, 131 (three cells).

For the supervisor (entry surfaces, his own text, vocabulary and the case's design; not applied here):
- The abstract at ten cells; "a few" against a tenth (two cells); G19 and F16 read "unsupervised feature engineering"
  as frontier estimation; "Scaling" at four; "hyperbolic" at eleven, with the DEA sense; "invariant" at nine; the
  n-lemma name at seventeen.
- The decision section as the executive reads it (F07): "it does not show me a decision that changed, a cost of
  adoption, or a number I can put in a budget line"; with G24 and F06's "what the fit adds to Table 2". A reader-need
  finding on WP39's section, his to weigh.
- "Machine-checked" (Section 13) against Appendix B's "not formal verification" and 160 of 505 steps applying posited
  axioms (F27); the repository's own rule says the scripts are a pencil-and-paper substitute. His wording.
- The weaker novelty claim ("We did not find the combination in the sources reviewed"): three cells.
- The case's design: the regimes' Kp ranges (145) and the launch slot's convention (144) touch his model; the launch
  price as a step function of mass class (G13) is a limits item.
- Theorem 9's S and the case's zero exponents (six cells); Theorem 4 as a theorem on a par (G11).
- Structure: Section 3's assumptions as one paragraph, the condition families split across sections, proofs numbered
  apart from statements, L-numbers out of order (five cells), Figure 1's legend colours against its numbering,
  Definition 8 as a claim before its theorem (G28).
- Incidents for the README: "Loading" figures and tables on first extraction for six readers; the captured first
  screen's collapsed contents chevron (G16).

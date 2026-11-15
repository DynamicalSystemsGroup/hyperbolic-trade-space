# Final reader round, wave 9: the assistant's triage of the second-wording held-out reads

Head read: 5ac44f7 (the dev abstract head the stage was rebuilt from). Reports: `../reports/{G01,G15,G10,G17,G18,G23}.md`,
committed verbatim. Models per `slots.tsv`: m1 Sonnet (G10), m2 Haiku (G01, G15, G17, G18, G23). These are the
second-wording twins of wave 8's held-out cells (F01, F10, F15, F17, F18, F23). Wave 8's triage was not yet written
when this was drafted, so replication with the twins is marked from the F reports' own text, not from their triage.
Forms as in `wave-1.md`; counting rules as in `wave-7.md` (wrong belief and defect count at once; friction and
missing at two cells; preference logged). The answer key is not used here: no key marks are cited, and "wrong
belief" below means a reading that contradicts a sentence of the paper, each checked by grep against
`raw/paper.txt` (and `raw/supporting-material.txt`). Quotes of figure text were read from the figure images.
Requests are labelled 182 and on; the driver renumbers them globally.

## G01 (P1-A, wording 2, Haiku)

- Depth A (abstract only). Main results as stated: a way to describe trade-offs among designs as a frontier; the
  family defined by level sets of a posynomial; monomial case convex, posynomial case GGP-compatible; unsupervised
  like PCA but with a curved surface, "losing nothing"; the n-lemma; Pareto improvements raise energy; white space as
  possible under-explored region; SymPy-scripted proofs and a scikit-learn estimator. Held as claims, "not results I
  have checked".
- Said the method does not do: give a single optimal design; say how many designs are needed or what sparse data do;
  say how categorical attributes become positive metrics; claim formal verification now (listed as future work);
  claim the cubesat results generalise; claim measured speed or scale.
- Contradictions with the paper: 0. One loose line: "The abstract gives no numbers at all", in a report whose own
  section 1 and the abstract carry "thirteen metrics" (the reader means no size, fit quality or rates; not a reading of
  a sentence).
- Depth job: done. The reader read the abstract as a promise, went to the worked example and the fit error as the next
  step, and would not sign off on "losing nothing" before seeing the numbers.
- Findings, all on the abstract (for the supervisor, no requests): "losing nothing" against a fitted surface that
  "normally leaves residuals" (6.9; G15 (10), G10 (6.1), G18 (6.1): four cells in this wave); "energy" in quotation marks
  never defined (6.10; G15 (11), G10 (6.3)); "log-convex" applied to a frontier (6.6; G15 (7), G10 (6.2)); "posynomial",
  "level sets of" (6.7; G15 (8)); what conditioning does to a value (6.4, 6.5; G15 (6, 7)); the n-lemma's meaning and the
  link from maximum energy to weak efficiency (6.11, 6.12; G15 (12, 13)); "white space" without a test (6.13; G15
  (14)); what "scripted with SymPy" covers (6.14; G15 (16)); "pulls back", "a rule" (6.16, 6.17; G15 (19)); "measurements"
  against "a simulation study" (6.18; G15 (17)); verification and speed joined in one future-work item (6.19; G15 (20));
  the title's "scaling" with no size (6.1; G15 (1)); the machine-learning and PCA opener (6.2; G15 (3)); "hyperbolic"
  with no picture (6.3; G15 (4, 5)); "unsupervised" beside a fitted surface (6.20); "detected", "losing the thread"
  (6.15; G15 (18)). With G01 and G15 the abstract's phrases stand at thirteen cells to this wave (eleven to wave 7).

## G15 (P2-A, wording 2, Haiku)

- Depth A. Main results as stated: conditioning into positive larger-is-better metrics; no strong sampling assumption,
  only a log-convex frontier; the posynomial family, monomial case convex, GGP-compatible; energy level sets; Pareto
  improvements raise energy, a maximizer is weakly efficient; n-lemmas detected in the worked example; white space;
  traceability ("a point with no data is a conjecture"); SymPy proofs, scikit-learn estimator.
- Said the method does not do: assume a well-behaved design space or a sampling distribution (it assumes log-convexity
  and needs conditioning); claim formal verification; claim a fitted surface is a validated model (a point without data
  is a conjecture); say how the example decision was validated; claim white-space search works (future thrust).
- Contradictions with the paper: 0.
- Depth job: done. The reader would read the method section next, write the procedure as ordered steps, and run the
  estimator on a small table of its own; it "would not rely on the abstract alone for anything I could defend on
  Monday".
- Findings: the abstract's phrases, as under G01 (all twenty-one confusions are phrase-level: "scaling", "hyperbolic",
  "piecewise", "conditioning" in two senses, "log-convex", "posynomial", "losing nothing", "energy", "n-lemma", "weakly",
  "white space", "scripted", "pulls back", "a rule", "detected"); one not on G01's list: the keyword "open source
  software" has no sentence of its own (6.21; one cell, logged). For the supervisor.

## G10 (P3-D, wording 2, Sonnet)

- Depth D. Main results as stated: the fit as a log-mean-exp soft maximum over the simplex, convex in w, any minimizer
  global, uniqueness not claimed, a linear program at infinite temperature; V homogeneous of degree one, exponents as
  elasticities, the factor V^(-1/w_j); the chart a bijective rewriting, exact pull-back under log-affine conditioning;
  a maximizer weakly Pareto-efficient, the converse not claimed; K > 1 not convex, three levels of guarantee and a
  soft-fit certificate, none global; noise as a ridge, a population statement; on the case, 236 nondominated of 2,134
  on four attributes and all 2,134 on thirteen, a 7-metric K = 1 contending set, K = 2 with 8 and 7, 16 of 20 planted
  tables recovered, three proposals that landed as predicted while violating depth of discharge. Three kinds of claim
  held apart (scripted algebra, numbers observed on this table, validation outside it).
- Said the method does not do: run or model the evaluation; do the conditioning; choose K; say a design is attainable;
  give causal exchange rates; replace PCA or Pareto analysis; guarantee the Pareto boundary rather than the supporting
  envelope; predict; handle dents, holes or categorical variables inside the theory; search the design space; assess
  stability of exponents at K = 1; make the cubesat numbers real; answer the decision. "Formally verified" it places
  only on the requirement checks in the system model; confirmed in Appendix B ("formal verification is said only of
  those checks").
- Contradictions with the paper: 0.
- Pointers followed (D): Appendix C.4, for the rule the evaluation side must meet: asked for, found as a per-attribute
  table (orientation, raw range, log-spread k), with no statement of the rule in words. Appendix E, the gap ledger:
  asked for, found (G-1 to G-12 read; the dump cut at G-13). Appendix A: found in part. Appendix B's statement and B.2:
  found; the B.1 and B.3 step tables: not found, showing "Loading...". C.8, the cost model and omissions: found. Appendix
  D (Section 9's numbers): not found, tables lazy-loaded, only the prose lead-ins seen. H: text found, H.3's table not.
  F and G: headings and prose only. The docs' Getting started and Conditioning pages: boundary (not among the pages).
  One process slip, reported by the reader: three JavaScript calls were sent without its tab id and ran in another tab
  (tab-113); two errored and one returned empty, all read-only; redone on its own tab.
- Depth job: done, with whys owed. The reader named what its side delivers (a table of positive, oriented,
  conditioned outcomes), what it must settle first (orientation, shift, scaler, "these choices define the question"),
  and what stays its own (conditioning, zero and negative outputs, the evaluation's behaviour at the edges). It could
  not find the conditioning rule in words, a rule of thumb for rows against d and K, how a human or ordinal assessment
  is conditioned, or the noise size at which the contending set changes (D.18's table did not render): see 192.
- Findings that count: Table 2's caption "the levels, all inside the near-frontier band" against the baseline row's
  -0.330 and the reader's expectation that a larger level is better (6.45; G18 (14); F10 (19) states the same for the K =
  2 band: three cells; new: 182); "900 rows" against "twenty tables of 400 rows" (6.35; F10, F18 (both ask to reconcile
  it): three cells; new: 183); Definition 4's "the open one, as the code counts it" (6.13; G17, G18 (5), G23 (15); F10,
  F17: six cells; joins 17: 186); Definition 3's "the formula is the sum" against "the package's mean" (6.12; G17,
  G18 (4), G23 (14); F17, F23: six cells; joins 5, 131: 187); R1 as "a tau = infinity condition and does not give it" (6.21;
  G17, G18 (9), G23 (19): four cells; joins 24, 102: 188); the zero metric left out "without a warning" against A1
  and "negative values are rejected" (6.18; G17, G18 (6); F10, F17, F18: six cells; joins 57: 193); Figure 5's
  vertical axis (6.37; G17, G23 (4): joins 36: 189); Figure 4's "evenly spaced on a log scale, not to scale" (6.34;
  G17, G23 (3); joins 56, 140: 194); Figure 8's selection ("which eight of the thirteen", the picking rule) (6.42; G23
  (8); joins 28, 63, 132: 190); the conditioning rule only as a table in C.4 (6.8, section 8 item 1; the wave-7 G09
  read ends the same way: two cells: 192).
- Counted already: "invariant" in two senses (6.10), Definition 2's potential line (6.11, logged as preference),
  Definition 7's "how far" (6.16; joins 59), Section 3's A, R, F, I codes (6.9, 6.24; joins 55), the three thresholds
  (6.14; 19), "certified" and the 37 designs near a seam (6.28, 6.29; 21, 114), Theorem 10 (i) (6.25; 22, 97), Theorem 11's
  K^N bound (6.27; 139), the one-term fit named in three ways (6.26: the refit of record, the own-rows fit, the contending
  set; 135), the two bands at K = 2 (6.39; 70), the limits chosen from pass fractions (6.33, 6.46; 52, 51), the -0.9 in
  conditioned units (6.40; 53), Figure 8's picking (6.42), the proposal rule and its three proposals (6.43, 6.44; 43, 69),
  "novelty V - 1" against log V (6.48; the wave-3 V - 1 item), the prefilter's effect on the baseline set (6.49: a reader-
  need item for the supervisor with 6.8), the platform tie (6.50, logged: the paper states it).
- Logged: lazy-loaded tables read as "Loading..." through the page text for most of Appendices B, C and D (the README's
  incidents; the second depth-D reader after G09 to meet it); no way to open the scripts (boundary); the whole-
  text assumptions (multivariate calculus, linear algebra, convex optimization) against a reader at linear algebra
  and basic statistics, who followed statements and not proof sketches (6.51: expected, not a finding).
- Reader-need verdict, for the supervisor: Section 11 says "supply configurations, attributes and a conditioning
  rule" and sends to the docs; no page of the paper lists what the table must satisfy. Both D readers who came for the
  evaluation side's duties (G09, G10) assemble it from Sections 3, 5, 8 and Appendix E.

## G17 (P4-C, wording 2, Haiku)

- Depth C. Main results as stated: with K = 1 a geometric program in the exponents, convex in the weights, exponents
  as elasticities, a reversible chart (Theorems 2, 3, 5, 6); a maximizer weakly efficient, the converse not proved;
  K > 1 not convex, three levels of guarantee plus a soft-fit certificate, none global; on the cubesat table a seven-
  metric K = 1 set, K = 2 with shares 0.74 and 0.26, 28 of 2,134 designs through the requirements and the band, the
  decision left to the executives ("prices the question"). The K choice read as a modelling choice, as the number of
  retained components is for PCA.
- Said the method does not do: a global optimum of the several-term fit; consistency, identifiability or a sampling error
  on exponents; recover the Pareto boundary; say whether the hypotheses suit a table; causal statements; replace PCA or
  Pareto analysis; handle discrete variables within a category; a convergence theorem for the outer search loop. "The
  paper explicitly does not claim that its proposals reliably cross V = 1".
- Contradictions with the paper: 0. The first reading of n as the metric count was corrected by the reader from
  Definition 6 ("So n is the size of the contending set, not the metric count").
- Depth job: done. The reader placed it against PCA (setting and the estimator interface borrowed, "not a PCA of any
  kind" as the paper says of HoroPCA; PCA used downstream on the near-frontier chart), named input (conditioned
  table), outputs (chart, levels, exponents, reaches) and the pipeline calls (fit, transform, inverse_transform,
  score_samples; no predict). Owed: the conditioning default, what the estimator does with a zero row and what
  score_samples returns in sign.
- Findings that count: score_samples "returns the energy differential" with negative inside and positive beyond, against
  a score_samples that reads higher as more typical (F17 asks whether it fits the sklearn contract; logged once at
  wave 4: second cell: 191); Definition 4's open band (joins 186); Definition 3's sum and mean (187); R1 (188); the zero
  row dropped without a warning (193); Figure 5's vertical axis (189); Figure 4's axis words (194); "none of 60
  planted terms" and "the 20 planted tables" with no word that 60 is twenty tables of three terms (with G10
  (35): 183); Figure 6's axis as a model quantity (the caption already says it is a reading; joins 41).
- Counted already: the abstract's "n-lemma" with n as the metric count (the n-lemma name), "like PCA" against
  "not a PCA of any kind" (the PCA item), Theorem 3 "not claimed strictly", the three objects (54), the
  hyperbola as a special case, the three thresholds (19), Figure 1, A1 to A10 (55), Section 8's
  0.97 and 0.99 (116), the K = 2 choice resting on D.15 (95), the facet-normal reading (24), the
  chart and "energy differential" naming, "machine-checked" (the supervisor's item), Table 2 and the
  executives' paragraph (51, 71), the regressor's band (47). Logged: Figure 2 and Figure 3 as dense for a
  reader who does not know SysML v2 (preference); the reference list's two unpublished or non-peer-reviewed items
  (Föllmer, n.d.; the SEBoK entry; the wave-7 Föllmer note); the process disclosure (Claude Code named), read as not
  changing how the claims read.

## G18 (P5-D, wording 2, Haiku)

- Depth D. Main results as stated, with algebra checked by the reader: K = 1 convex in the exponents, every minimizer
  global, uniqueness not claimed (Theorems 2, 3); elasticities, the chart a bijection (Theorems 5, 6), exact inversion
  under log-affine conditioning (Theorem 7); a maximizer weakly efficient, the converse not claimed (Theorem 9); K > 1 not
  convex (Theorem 10), three levels of guarantee (Theorem 11, Lemma 1, Lemma 2 with Proposition 3 and Corollary 2) and a
  soft-fit certificate (Theorem 12); noise as a ridge and a first-order shift (Corollary 1; the reader checked the
  cumulant algebra); on the case, observations and not proofs. Checked in passing: 0.9^(-50) is about 194 for Theorem
  5's "about 190".
- Said the method does not do: claim priority; replace PCA or Pareto analysis; global convergence (Q1), consistency
  (Q2), identifiability under finite biased samples (Q3), recovery of the Pareto boundary rather than the supporting
  envelope (Q4); formal verification; fit designs outside the table; pick K beyond the package's checks; causal
  exponents.
- Contradictions with the paper: 0. One muddle: "The band at K = 2 is 0.0240 (stated, 1/tau at K = 1)"; the paper has
  0.0240 and 0.0088 at K = 1 and 2 and uses the K = 1 band for the figures and shortlist (G-9). The reader's own
  parenthesis says so; not counted.
- Pointers followed (D): Appendix A (terms): asked for, found ("frontier" listed as "not a defined object"). Appendix B,
  intro and B.1 to L3.10 (for Theorem 2's KKT conditions and L3.9): asked for, found; L4, L16, L17, L20: not reached
  (the reader stopped for the page's length). Appendix E G-1 to G-5 (what cannot be proved of the frontier and the
  uniqueness of the exponents): asked for, found; G-6 on not read. Pointed to by the main text and not opened: Appendix
  C, D (D.8, D.11, D.14, D.15, D.19), F, G, H. Boundary: the Download Notebook link.
- Depth job: partly done. The reader's job was whether the guarantees are the ones established and whether anything
  observed is passed off as proved; it did that for the main statements (and checked what it reached), but it opened
  no figure (it says so: "I did not take screenshots") and did not reach the proofs behind Theorems 3, 10 and 12. The
  convexity and noise statements were checked from the main text's own sketches.
- Findings that count: Table 2's caption "all inside the near-frontier band" against the baseline row at -0.330 (6.14:
  182, with G10 and F10); the zero metric against A1 and G-5 (6.6: 193); Definition 4's closed and open band (6.5:
  186); Definition 3's sum and mean (6.4: 187); R1 against "the balanced point ... in the relative interior of a facet"
  (6.9: 188); "frontier" in three objects (6.3; joins 54: four cells in this wave with G10 (7), G23 (17), G17); "proved" for steps
  that are posited axioms, 160 of 505 steps "by a declared axiom" in Appendix B (6.7; the "Derived" and "machine-
  checked" items, 31); Theorem 11's finite stop resting on unique term minimizers that G-2 says cannot be shown for a
  data set (6.11; joins 23, 139: the text states the hypothesis, the reader asks what the cubesat fits then rest on).
- Counted already: "losing nothing" (6.1), the n-lemma's size depending on a threshold and the fit used (6.2; 135, 161),
  the F codes (6.8; 55), Proposition 3's conditional form (6.12, clear), Theorem 12's sign convention (6.13: unchecked;
  joins 115, 40), total mass at 0.02 (6.15; 73), the 28-design rule (6.16; 51), Figure 1's inside-the-face point (6.17;
  37), the 37 designs at a seam (6.18), "prospectively specified" (6.19; 128).
- Logged: the reader's section 10 states what it could not check (the figures as images, L4, L16, L17, L20, D.8, D.11,
  D.14, D.15, D.19, H, G, F, G-6 on, any computation); not a finding about the paper.

## G23 (P6-B, wording 2, Haiku)

- Depth B (headings, results and statements, figures and captions). Main results as stated: V a weighted geometric mean
  with reach beta, V = 1 the fitted reference surface; the chart; the one-term fit convex, every minimizer global,
  uniqueness not claimed, the fit minimizing the reach; exponents as elasticities; a maximizer weakly efficient; K > 1 with
  three levels of guarantee and a soft-fit certificate; noise as a ridge; on the cubesat two terms with different
  contending sets (8 and 7 metrics), "observed and not proved"; "claims nothing as novel". Its own derivation, not in
  its material: at tau = infinity and one term the fit is a linear program (the paper states it in Section 5, which this
  depth does not reach).
- Said the method does not do: give the Pareto boundary; a consistency result (Proposition 2 "a population identity,
  with no consistency claim"); uniqueness; stationarity of the stop; say whether the elasticities are right; the
  schedule, risk or a larger fleet's worth; say the K = 2 split is true of the real system; resolve Q1 to Q4.
- Contradictions with the paper: 2.
  1. The reader on Figure 7's term 2: "Definition 6 says the two thresholds 'nest in size', which I read as
     'participating is a subset of contending'", and then finds eight non-grey labels under a title "7-lemma (7 metrics in
     the contending set)". Paper, Definition 6: "They nest in size, and the last two read different fits."; Section 9: "At
     the fit temperature total mass also carries 0.02 and is not in the contending set"; Figure 7's caption: "so an
     outlined metric can be grey and a black one not outlined". Term 2 has total mass at 0.01 black and not outlined:
     the figure and the paper agree; the reading does not (184).
  2. The reader: "The soft-weight alternation descends the mean slack (Theorem 11), and finishes after at most K^N + 1
     iterations". Paper, Theorem 11: "The sharp alternation then stops after finitely many iterations"; the soft-weight
     alternation is Theorem 10 (ii), its certificate Theorem 12 (185).
- Pointers (B): the reader wanted Section 2 and Table 1 (the prior-art families) to judge novelty; at this depth it had
  Table 1's caption and the heading "Prior art, by family" only: boundary. Appendices D.3, D.15, D.19: named by captions,
  not in this depth's material: boundary.
- Depth job: done to the slice's limit. It states what the paper does and claims, finds the paper's own claim to no
  novelty, and names the part it would test (the n-lemma and contending sets under resampling and under the 10 percent
  convention); the question it came with (whether the gap to the established frontier methods is real or terminology)
  is answered only in Section 2 and Table 1, outside depth B. For the supervisor: at this depth the novelty statement
  is the one sentence of Main results.
- Findings that count: Figure 7's count (184, above; F23 (7) reads the same legend as two systems that "disagree by
  design": two cells; joins 73, 153, 87, 42); Figure 5's axis label (6.4; 189); Figure 4's markers and axis (6.3;
  194, joins 140); Figure 8's "where its V peaks", "fixed total" and the picking (6.8; 190, joins 63, 132, 28);
  Definition 4's open band (6.15; 186); Definition 3 (6.14; 187); R1 (6.19; 188); the main results' sentence "two
  terms hold different contending sets where one term merges them into one" with no way to tell which merge (6.24;
  joins 87 and 151, whose caption and Section 9 sentence name peak slew power).
- Counted already: Figure 1 (6.1; 37), Figure 3's caption against its box (6.2; 26, 88: the box lists four of ten, the
  caption's "nine it computes" resolves to ten once control effort is added; verified against the image), "regime" (6.3;
  27), Figure 6's four names for log V and two fits in one plot (6.5; 27, 41, 141), the near-collinear pair (6.7; 42),
  "executives" (6.10; 38), "invariant" for a quantity that doubles with its inputs (6.12; the supervisor's "invariant"
  item), the fit stated without the reach it minimizes (6.13; 67), two infinities (6.16; 131), Definition 1's two surfaces
  (6.17; 54), Theorem 10 (i) (6.20; 22), Theorem 11's K^N (6.21: the reader agrees with the paper's "not a practical
  stopping guarantee"), Theorem 12 (6.22; 115), labels without a key (6.25; 55). Logged (depth artifacts): equation (2)
  and R3, A9, A10, R2 undefined in the material (6.18, 6.23).

## Roll-up, wave 9

| Cell | Report | Model | Depth | Contradictions | Depth job | Counting findings |
|---|---|---|---|---|---|---|
| P1-A | G01 | Haiku | A | 0 | done | 0 (abstract phrases, to the supervisor) |
| P2-A | G15 | Haiku | A | 0 | done | 0 (abstract phrases, to the supervisor) |
| P3-D | G10 | Sonnet | D | 0 | done, whys owed | 2 defects (Table 2's "all", 900 against 400), 8 frictions, 1 missing |
| P4-C | G17 | Haiku | C | 0 | done | 1 friction (score_samples), 6 joining |
| P5-D | G18 | Haiku | D | 0 | partly (figures unseen, proofs not reached) | 1 defect (Table 2), 5 joining |
| P6-B | G23 | Haiku | B | 2 | done to the slice's limit | 1 wrong belief (nest in size), 1 wrong belief (Theorem 11's alternation), 5 joining |

- Contradictions with the paper: 2 in 6 reads, both in the depth-B reader (G23), both low stakes and both traceable to a
  sentence that invites them. None in the two abstract readers or the C and D readers.
- The new record defects came from the depth-D readers: Table 2's caption says "all inside the near-frontier band" and
  its baseline row is -0.330 (G10, G18; F10 reads the band by K), and Section 8 describes a 900-row planted example and
  then "16 of 20 such tables" that D.14 says have 400 rows (G10; F10 and F18 ask the same). Neither is in the triage of waves 1 to 7; the caption sentence is what request 50 asked for, and C.7 and D.14 were
  never set side by side there.
- Definition 3, Definition 4 and the R1 remark each stop four of the six readers although earlier requests (5, 17, 24,
  131) put a sentence there: the fixes are present and still read as two aggregators, a definition adjusted to the code,
  and a negative statement. 186, 187 and 188 say the same facts positively.
- Held fixed from wave 7's roll-up: no reader's main results contradict the record's mathematics; G10 and G17 state
  "formal verification" only of the requirement checks and the lemma scripts as pencil-and-paper checks; G18 re-derived
  the noise identity and found the paper's cumulant statement right.

## Twin agreement: wave 9 reader against its wave-8 twin (same cell, other wording and model)

Read from the F reports at the same head (5ac44f7); wave 8's own triage may add detail.

- P1-A, G01 (Haiku, wording 2) with F01 (Sonnet, wording 1): agree on the job. Both read the abstract as a method for a
  curved trade-off surface that describes, and does not choose, a design; both treat "losing nothing", "energy", "white
  space" and "a rule" as unexplained, would look first at the cubesat example, and would read on. They differ in posture
  only: F01 would try a re-run on a past programme and says "worth an hour"; G01 would "not sign it off yet".
- P2-A, G15 (Haiku, wording 2) with F15 (Sonnet, wording 1): agree. Both take the method as the trade-study analogue of
  PCA with a conditioning step first, both would run the estimator on a finished study, and both list the same
  abstract phrases. G15 asks for the method section's ordered steps; F15 asks first for the code and the example.
- P3-D, G10 (Sonnet, wording 2) with F10 (Haiku, wording 1): agree on the job and on the findings: the same record
  defects (the 400 and 900 rows; the "all inside the near-frontier band" caption), the silent drop of a zero row, the
  conditioning and K as the analyst's, no stability assessment at K = 1, the case's thresholds chosen from pass
  fractions. They differ in reach: F10 lists D.19's table and Appendix E beyond its first rows as unread; G10's page text lost most
  tables to "Loading..." and G10 also sent three calls to another tab by mistake.
- P4-C, G17 (Haiku, wording 2) with F17 (Sonnet, wording 1): agree. Both place it as a fit and a chart that compose with
  PCA downstream, state the same results (the K = 1 geometric program, the K = 2 case, the 28-design shortlist, the
  decision priced and not answered) and the same limits, and both ask about score_samples and the three thresholds. F17
  finds Definition 6's three thresholds hard to hold ("nest in size"); G17 first reads n as the metric count and
  corrects itself from Definition 6.
- P5-D, G18 (Haiku, wording 2) with F18 (Sonnet, wording 1): agree on what is established (the convex core correct, the
  noise identity re-derived, the several-term guarantees local, the converse not claimed) and on the open items (the
  zero-row masking, "machine-checked" against the lemma scripts, the closed and open band). Neither opened the figures
  (F18's tab closed first; G18 took no screenshots), and both left Appendices D, F, G and H.3 mostly unread; F18 also asks
  to reconcile 900 and 400 rows, which G18 did not reach.
- P6-B, G23 (Haiku, wording 2) with F23 (Sonnet, wording 1): agree on the job. Both state the main results with the paper's
  own limits (not the Pareto boundary, no consistency claim, local guarantees, the 10 percent convention), both say the
  paper's one novelty statement is "claims nothing as novel" and that Table 1 and Section 2 decide it, and both read Figure
  7's two highlight systems (outline from the exact fit, grey from the fit-temperature exponent) with effort. G23 goes
  further and misreads "nest in size"; F23 reads the legend correctly and asks what the count of metrics means when a
  pair is one axis.

## Change requests added at wave 9 (labelled H9-n; the driver renumbers after 165)

Defects and wrong beliefs (count at once):

182. Table 2's caption: "the levels, all inside the near-frontier band, do not rank them" while the baseline row's level
      is -0.330 and the sponsor-alone row's +0.016 lies inside the K = 1 band (0.0240) and outside the K = 2 band (0.0088).
      Name the band the sentence means (the K = 1 band, as the shortlist uses, G-9) and say the sentence holds for the
      picks, the baseline row being context with the last two rows. Constraint: the order-of-the-rules sentence (50) and
      the table's numbers stay.
183. Section 8's closing sentence and Section 6.2: "The worked example of Appendix C.7 has 900 rows ... 16 of 20 such
      tables" while D.14's twenty tables have 400 rows, and "none of 60 planted terms" carries no word that 60 is twenty
      tables of three. Say once: twenty tables of 400 rows, 4 metrics and three terms (60 planted terms), distinct from
      C.7's single 900-row example. Constraint: the counts are the record's, unchanged.
184. Definition 6's "They nest in size, and the last two read different fits": read as "participating is a subset of
      contending" and then Figure 7's term 2 (seven outlined, eight black labels) looks inconsistent. Give the thresholds
      by their order as numbers (10^-12, 10^-9, 10^-3), say that the contending set and the participating set read
      different fits so that neither contains the other in general, and in Figure 7's caption name term 2 as the case
      (total mass, 0.01, participates and is not contending). Constraint: the thresholds stay conventions; joins 73, 153.
185. Main results, "three levels of guarantee, descent (Theorem 11) ...": say these are the sharp alternation's, as
      Theorem 11 and Theorem 10 (ii) say, so that Theorem 11 is not read as the soft-weight alternation's descent.
      Constraint: the stopping declaration stays a paragraph, not a numbered result (80).

Frictions and missing (two cells or more):

186. Definition 4: "the band here is the open one, as the code counts it" reads as a definition adjusted to the code
      (G10, G17, G18, G23; F10, F17). Say the band is open, |log V| < 1/tau, and that L5.25's bound on the closed band
      contains it; drop "as the code counts it". Constraint: the lemma script is not edited (17).
187. Definition 3's "Term aggregation": "the formula is the sum. The package's mean (kappa = infinity: the maximum)
      subtracts the constant" reads as two aggregators (G10, G17, G18, G23; F17, F23). One order: the model's formula is
      the sum; the reported level subtracts (log K)/kappa; at the fits of record, kappa = infinity, the aggregate is the
      maximum and the offset is zero. Constraint: Theorem 8's statement unchanged (5, 131).
188. Theorem 2's remark on R1: "R1 is a tau = infinity condition and does not give it" stops readers (G10, G17, G18, G23).
      State the positive fact: at the fit temperature each exponent read as an elasticity must be positive in that fit,
      and R1 secures the facet at tau = infinity only. Constraint: the L3.9 pointer stays (24, 102).
189. Figure 5's vertical-axis label ("log of the conditioned unit cost (inverse USD; larger is better)") does not show
      the shift the title and caption give ("adjusted for the other eleven metrics"); two readers read the plain metric
      (G17, G23; G10's first read of the caption). Make the label say it is shifted. Constraint: the figure-review loop;
      the line's slope stays the elasticity (36).
190. Figure 8's caption: "the 56 triples of eight of the thirteen metrics": name the eight (or the appendix row) and
      say how the two displayed were picked (the stable two-term pattern, 105 of 291 fits); the legend's "where its V
      peaks" read as a physical optimum. Constraint: no new result; the caption stays shows and does not show (28, 63, 132).
191. Section 3's estimator paragraph: "score_samples returns the energy differential": give the sign and direction
      there (log V, positive beyond the surface and so higher is further out), since the method's name for a score
      reads higher as more typical (G17; F17 asks; logged at wave 4). Constraint: the interface unchanged.
192. Appendix C.4 and Section 11: C.4 is a table with no sentence of the rule; Section 11's "supply configurations,
      attributes and a conditioning rule" sends to the docs. State the case's rule in words above the table
      (orientation by reciprocal for a smaller-is-better attribute; log-spread scaling to a standard deviation of one
      in the log-metric) and, in Section 11, list what the table must meet before the fit (strictly positive, larger-is-
      better; a zero row left out without a warning; negatives rejected; feasible designs). Constraint: record only, no
      new method content; the docs' Conditioning page stays the guide (G09, G10).
193. Section 5's "the package tolerates a zero metric by leaving that row out of the fit, without a warning" against
      A1 and "negative values are rejected": say why there is no warning (or that there is one), and in G-5 mark which
      sentence is the bridging assumption ("carries no information about the other exponents") and which the unproved
      part ("the row still constrains the other metrics"). Constraint: package behaviour is the supervisor's; the
      statement must match the code (extends 57; G10, G17, G18; F10, F17, F18).
194. Figure 4's caption: "evenly spaced on a log scale, not to scale" reads as saying both (G10; G17 parses it; G23 on
      the two markers): say the columns are the sweep's values at equal spacing and not a linear temperature axis.
      Constraint: the ring-and-line explanation of 140 stays.

## Earlier requests gaining cells at wave 9

5 and 131 (Definition 3: four more cells, six with the F twins); 17 (Definition 4: four); 24 and 102 (R1: four); 26 and 88
(Figure 3's box: G23); 27 (regime, the four names of log V: G23); 36 (Figure 5: three); 37 (Figure 1: G18, G23); 38 (the
executives' measures: G23); 41 and 141 (Figure 6: G17, G23); 42 (near-collinear pairs: G23); 47 (the regressor's band:
G17); 51 and 52 (the shortlist's rule and limits: G10, G17, G18); 53 (-0.9: G10, G17); 54 ("frontier": G10, G17, G18, G23);
55 (hypothesis codes: G10, G17, G18, G23); 57 (the zero row: G10, G17, G18); 63 and 132 (Figure 8: G10, G23); 70 (the bands:
G10, G18); 73 (total mass at 0.02: G18, G23); 87 and 151 (peak slew power: G23); 95 (K = 2 from the checks: G10, G17, G18, G23);
116 (0.97 and 0.99: G17); 135 and 161 (the n-lemma's estimator and threshold: G10, G18); 139 (Theorem 11's finite stop: G10, G17,
G18, G23); 22 and 97 (Theorem 10 (i): G10, G23); 115 (Theorem 12: G18, G23).

## Incidents for the README

- G10's text capture of the supporting page lost most step and results tables to "Loading..." (Appendices B, C, D, parts
  of H); the supporting-material capture the briefs were drawn from has them, so the reading was limited by the load, as
  for earlier readers (waves 3 to 7).
- G10 issued three JavaScript calls without its tab id; they ran in another tab, read-only (two errors, one empty).
- G18 opened no figure and stopped reading Appendix B at L3.10 for the page's length; its report lists what it did not
  check.

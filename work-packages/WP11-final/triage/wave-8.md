# Final reader round, wave 8: the assistant's triage of the six held-out F cells

Head read: 5ac44f7 (the dev abstract head). Reports: `../reports/{F01,F10,F15,F17,F18,F23}.md`, committed verbatim
(729f120) before this triage. These six are the held-out cells of the 2026-11-09 draw (P1-A, P3-D, P2-A, P4-C, P5-D,
P6-B), read after the second unit landed, on the rebuilt stage and the recaptured slices. Models per `slots.tsv`: m1
Sonnet (F01, F15, F17, F18, F23), m2 Haiku (F10); all wording 1. Their G twins are wave 9. The answer key is held by
the driver and was not consulted: this triage records what each reader stated, quotes every reading that contradicts
a sentence of the paper (reader's words from the report, the paper's from `raw/paper.txt` or `raw/supporting-material.txt`,
both checked by search), classifies findings, and applies the wave-7 rule (wrong belief or defect counts at once;
friction or missing at two cells; preference logged). Request ids are H8-1 to H8-10; the driver renumbers globally.
Earlier requests are cited by their wave-7 numbers (1 to 165). Report items are cited as (6.n).

The depths, from the final-round plan: A abstract only (F01, F15); B headings, results, figures and captions (F23);
C whole main text (F17); D main text plus supporting material (F10, F18).

## F01 (P1-A, Sonnet)

- Main results stated: a table of designs fitted with a curved frontier; designs placed by position and level; the
  highest-energy design is weakly Pareto-efficient; white space on an occupied frontier is a conjecture until built
  and measured; "n-lemma" for a monomial term in n metrics; a scikit-learn package with SymPy-scripted proofs;
  convexity for the simplest version.
- Does not do: choose the design; do the conditioning; claim the design space is well behaved; claim formal
  verification or that the search is done; say how well the fit works, how much data it needs, or the cubesat answer.
- Contradictions with the paper: 1 (weak).
  - Reader: "Moving to a higher-energy level means an improvement". Paper (abstract): "Pareto improvements increase
    energy, and a design that maximizes energy is weakly Pareto-efficient." The paper's implication runs from
    improvement to energy; the reader drops the direction.
- Findings (all on the abstract, the supervisor's hand; friction unless noted):
  - Title: "Scaling" read as a size claim the abstract never makes (6.1; F15 (6.1): two cells).
  - "Energy" has no stated link to the problem (6.8; F15 (6.10), F17 (6.2, 6.9), F23 (6.6): four cells).
  - "Piecewise hyperbolic" cannot be pictured (6.3; F15 (6.4): two cells); "white space" and "occupied level set"
    undefined (6.11; F15 (6.13)); "log-convex" and what it excludes (6.5; F15 (6.6); F18 (6.1)); "proposed by a rule"
    (6.14; F15 (6.17)); "a monomial term in n metrics" (6.9; F15 (6.11), F10 (6.1)); "losing nothing" (6.7; F15 (6.9)).
  - The abstract opens on "an answer and a justification" and never states the cubesat answer (6.16; F15 (6.2, 8)).
  - Thirteen metrics, a decision on two (6.13; F15 (6.15)).
  - "scripted with SymPy" read as not formally verified, correctly, but only by inference (6.12).
- Depth job: done for the problem, the idea and wanting to read on (to the cubesat result and the plain statement of
  what the frontier assumption excludes). The finding is not stated, and the reader says so: the abstract states
  none.
- Change requests: H8-1 (abstract, for the supervisor). The abstract phrases above join the supervisor's list.

## F15 (P2-A, Sonnet)

- Main results stated: a fitted trade-off surface among positive larger-is-better metrics, each design placed by
  position and "energy", invertible; one term convex, several terms inside generalized geometric programming; the
  n-lemma; maximal energy is weakly Pareto-efficient; white space and points without data are conjectures; SymPy
  proofs and a scikit-learn estimator.
- Does not do: the conditioning; the choice among competing fits or of the number of terms; generate designs; formal
  verification; weights or the final choice; uncertainty of the measurements or the fit.
- Contradictions with the paper: 1.
  - Reader: "Raising energy is a Pareto improvement". Paper (abstract): "Pareto improvements increase energy, and a
    design that maximizes energy is weakly Pareto-efficient." The reader reverses the implication; a design with a
    higher level can be worse on a metric. Classified wrong belief.
- Findings (all on the abstract; friction): the phrases listed under F01 (title, energy, piecewise, white space,
  losing nothing, n-lemma, rule, thirteen to two, the missing answer); "we do not assume ..." beside "we apply
  conditioning to ensure the solvers behave" read as slightly at odds (6.6); the sentence "The paper provides a
  literature review, formal results and a worked example" describes the paper and not the result (6.14); Rust and
  theorem provers read as unrelated to a user's Monday (6.18: preference).
- Depth job: done for the problem, the idea and wanting to read on (to the worked example and the conditioning
  description). The finding is not stated (6.2, 8: "what is the cubesat result in plain terms"), for the same
  reason as F01. The reader's next step is a rerun on a finished study of its own, "from the abstract alone I cannot
  yet tell if I could do it on Monday".
- Change requests: H8-1 (the same abstract sentence).

## F23 (P6-B, Sonnet)

- Main results stated: V a weighted geometric mean, homogeneous of degree one (Theorem 1); K = 1 convex in the
  exponents, minimizers global, uniqueness not claimed (Theorems 2, 3); log-mean-exp with the exact maximum at
  tau = infinity (Theorem 4); exponents as elasticities, the chart reversible, the exact pull-back (Theorems 5 to 7);
  a maximizer weakly Pareto-efficient (Theorems 8, 9); K > 1 not convex (Theorem 10) with three weak guarantees
  and a soft-fit certificate (Theorems 11, 12, Lemma 1, 2); noise acts as a ridge (Corollary 1); K = 2 on the cubesat
  gives two terms where K = 1 merges them, observed and not proved; no novelty claimed, PCA and Pareto not replaced.
- Does not do: estimate the Pareto boundary (about a tenth of designs lie beyond the surface by construction);
  consistency or a sampling distribution for the exponents; global optimum, stationarity or convergence for K > 1;
  choose K from theory; rank designs on the surface; the conditioning.
- Contradictions with the paper: 0. One statement is not in the slice and exists in the paper: the reader "did not
  see" that non-log-convex frontiers cannot be represented; Section 5 (vi) says "no $K$ represents non-log-convex
  structure" (a depth contract, not a misreading).
- Findings:
  - defect: Figure 6 draws the grey near-frontier band below zero only (about -0.02 to 0; image checked), while
    Definition 4 gives "The near-frontier band is $|\log V|<1/\tau$" (6.6; F17 read the same figure and found it
    clear). One cell, counts at once: H8-4.
  - friction: Figure 8's two triples came from a search (105 of 291 fits); no chance baseline (6.8, 8, 22; F17 (6.36)):
    two cells, H8-9. What K = 2 adds over K = 1 (6.22, 8; F17 (6.33, 8), F18 (9)): three cells, H8-8.
  - friction, joining earlier requests: Figure 1's face against the point drawn (6.1; joins 37, F17 (6.13): two more
    cells); Figure 3's count "ten of the thirteen" (6.3; joins 26); Figure 4's evenly spaced axis and the 74
    effective designs (6.4; joins 56 and 61); Figure 5's cloud well below the line at high power (6.5; joins 36);
    Figure 7's outline and grey rules (6.7; joins 87, 153); the main results' "It is not the Pareto boundary: every
    design's position and level are read from it through the chart" read as a reason (6.11; joins 66); "design table"
    (6.12; joins 35); Definition 2's beta before Definition 7 (6.13; joins 85); Definition 3's "mean" for a maximum
    (6.14; joins 5); the three thresholds and equation (2) (6.15; joins 19, 161); the hypothesis codes (6.16; joins
    55); Theorem 11 (6.19; joins 98, 139); Theorem 12's exact-point hypothesis (6.20; joins 21); Corollary 1 (6.21;
    joins 84).
  - preference: "energy differential" as a name (6.6); Theorem 9 "adds no content specific to this fit" (6.18).
- Depth job: done. B-slice limits seen: the heading "Abstract" with no text, and Table 1's caption without its body
  (6.9, 6.10).
- Change requests: H8-4, H8-8, H8-9.

## F17 (P4-C, Sonnet)

- Reading note: the whole main text as rendered; one figure (Figure 6) by screenshot, the others by caption; the
  supporting material not opened.
- Main results stated: the table M of N designs by d metrics; the K = 1 fit (log-mean-exp soft maximum, convex in
  w, any minimizer global, a linear program at tau = infinity); elasticities, the reversible chart, the exact pull-back,
  weak efficiency (converse not claimed); the K > 1 alternation with three levels of guarantee and a soft-fit
  certificate; Q1 to Q4 open; cubesat: 236 of 2,134 nondominated on 4 attributes and all 2,134 on 13, a 7-lemma at K =
  1 and an 8 and a 7 at K = 2 (shares 0.74 and 0.26), 28 shortlisted designs ending in a question the method prices
  and does not answer; planted recovery 16 of 20; composes with PCA as a reading.
- Does not do: replace PCA or Pareto analysis or claim novelty; global optimum, consistency or identifiability;
  causal exchange rates or sampling error; predict, choose K or choose a design; represent non-log-convex structure;
  the search of Section 7 (no results); show the fit holds outside the table.
- Contradictions with the paper: 1 (minor).
  - Reader: "only the Discussion says the proposals reached the surface 'by spending the battery'". Paper (Section 9):
    "The proposals fail the depth-of-discharge feasibility condition: they reached the four-metric fitted reference
    surface by spending the battery (the Discussion's reading of the check, Section 10)." The sentence stands in
    Section 9 and again in the Discussion.
- Findings (the whole main text; forty-three items, most joining earlier requests):
  - friction, new at two cells: "baseline" for the Table 2 configuration and for the stock regime (6.28; F10 (6.14)):
    H8-7. What K = 2 adds (6.33; see F23): H8-8. The Figure 8 selection (6.36): H8-9. The estimator's call and its
    defaults not in the main text; Section 11 is three sentences and defers (6.42, 8; G09 in wave 7: two cells): H8-10.
  - friction, silent drop of a zero row (6.16; F10 (6.5): two cells): a reaction to the package's behaviour that
    request 57 asked the text to state, and it now does ("without a warning"); a package decision, for the supervisor.
  - friction, joining earlier requests: Section 1's pointers to Theorems, Lemmas and Q1 to Q4 before they are defined
    (6.4; joins 80, 66); the three objects called frontier (6.6; joins 54); "invariant" for a degree-one function
    (6.8; the paper says "It stays the same along a trade-off, hence invariant"); "reach" in Definition 2 before
    Definition 7 (6.8; joins 85); "energy differential" (6.9); Definition 3's "mean" and "sum" (6.10; joins 5); the
    closed and the open band (6.11; joins 17; F10 (6.3)); the three thresholds (6.12; joins 19, 161); Figure 1 (6.13;
    joins 37); R1 to R3 and Theorem 2's hypothesis (6.14, 6.20; joins 24, 102, 137); the 10 percent convention as a
    hyperparameter (6.15; joins 154); the zero-row clause (6.16); the answer's dependence on the scaler (6.17; joins
    74, 121); K = 2 and the checks (6.18, 6.31; joins 90, 95); the hypothesis codes (6.19; joins 55); Corollary 1's use
    (6.21; joins 84); the own-rows refit (6.22; joins 20, 135); Theorem 10 (i) as an instance (6.23; wave 5's
    Theorem 10 item); Theorem 11 and the iteration cap (6.24; joins 98, 139); "certified" against 37 designs on seams
    (6.25; joins 21); Section 7 in the contents (6.26; joins 49); "contending", "carry an exponent", "participates"
    (6.27; joins 19, 72); the K = 1 band at K = 2 (6.29; joins 70); 16 of 20 and thin terms in real tables (6.30; joins
    76); the elasticity's units (6.34; joins 29, 53); the method's output against the requirements after the fit
    (6.38; joins 51); Table 2's three decimals against the seam (6.39; joins 50); "Why a surface" unparseable (6.40;
    wave 7's "Why a frontier"); the PCA analogy and successive tensions (6.41; wave 7's item).
  - friction, one cell, logged: "claims nothing as novel" beside "Contribution" (6.3); the nondominated count as a
    general fact (6.5); a clustering against the terms (6.33); term 1's elasticity read across swapped parts (6.35).
- Depth job: done, whys owed (the reader names the whys that the text leaves to appendices: 6.7, 6.12, 6.14, 6.17,
  6.18, 6.25, 6.42 and 6.43). The reader would go on to C.4, the register of terms, D.15, D.14, Appendix E and
  Appendix F.
- Change requests: H8-7, H8-8, H8-9, H8-10.

## F10 (P3-D, Haiku)

- Main results stated: the K = 1 fit convex, a maximizer weakly Pareto-efficient; K > 1 not convex with three levels
  and the soft certificate; cubesat K = 1 with a seven-metric contending set and total mass at 0.02 outside it; K =
  2 with 8 and 7 metrics (shares 0.74 and 0.26, elasticity about -0.9 on term 2); planted recovery 16 of 20 with
  one certified failure; Table 2's 28 shortlisted designs, five rules, five picks, the question priced and not
  answered; the HoroPCA comparison on controlled tables.
- Does not do: a global optimum for K > 1; a sampling error for exponents; show the surface is the Pareto boundary;
  say how to choose the conditioning, K or the 10 percent; claim priority; show the fit holds outside the table; give
  established cubesat numbers.
- Contradictions with the paper: 1.
  - Reader: "The one-per-metric count does not hold as written." Paper (Section 8): "The model states thirteen
    requirements, one for each traded metric." The count holds on the text's own account (four feasibility
    conditions, six read after the fit, three more: thirteen), the launch budget standing as the limit on total
    mass; the Figure 3 caption says the launch budget requirement "reads the launch cost (yellow: derived, not
    traded)", which is what misled the reader. Classified friction, joins 126.
- Findings:
  - defect, two cells (with F18 (6.13)): Section 8's "The worked example of Appendix C.7 has 900 rows, 4 metrics and
    3 planted terms. The fit recovers all three terms on 16 of 20 such tables" against D.14's "twenty tables of 400
    rows and 4 metrics" (6.10): H8-2.
  - defect, one cell: D.3's per-term table prints near-frontier counts 318 and 119 beside shares 0.7384 and 0.2616;
    318 over 437 is 0.728; the band each column uses is not named (6.22): H8-5.
  - friction, two cells with F17: "baseline" (6.14): H8-7. The zero-row clause (6.5, see F17).
  - friction, joining earlier requests: the "package's mean" in Definition 3 (6.2; joins 5); the closed and the open
    band (6.3; joins 17); the boundary soft over designs and sharp over terms (6.4); Theorem 2's hypotheses (6.7;
    joins 24, 137); "machine-checked" against "not formal verification" (6.6; counted since wave 2); the own-rows
    refit and D.14 (6.9; joins 135); the three thresholds (6.11; joins 19, 161); the one-per-metric count (6.12;
    joins 126); "a count that is no part" (6.13; joins 68); the fraction above V = 1 depends on K and the convention
    (6.15; joins 11, 154); the elasticity's orientation and units (6.16; joins 29, 53); "3 of 3" with two proposals
    one configuration (6.17; joins 43); "cheapest fleet" against the baseline row's lower fleet cost, read as "among the
    shortlist" (6.18; joins 92); "all inside the near-frontier band" against the K = 2 band (6.19; joins 50, 70);
    the launch understatement "by 3.1 to 4.2 times" (6.20; joins 144); "certified" against the failure that is
    certified and wrong (6.25; joins 21); K = 2 against K = 3 under the resampling check (6.26; joins 95); the
    Foellmer entry as an unpublished page (6.30; wave 6's supervisor item, now four cells).
  - friction, one cell, logged: "conservative" undefined in "One term is tangent at one place and is conservative
    off it" (6.21); "conditioning_" and the analyst's conditioning share a word (6.23); D.14's second recovery
    condition (90 percent of frontier rows on the right term) absent from the main text's "to within 0.05" (6.24);
    1e-12 called "rounding-level" (6.27); internal labels and a stray "test" in Appendix E entries (6.28); H1 to H4
    used in the table before H.1 defines them (6.29).
- Pointers followed (the depth's job):
  - Asked for and found: Section 3 and Definition 6 to Appendix A, B, E (read the job statements and the first rows of
    E, G-1, G-2); C.8; C.4 (matches the main text); D.11 (matches); D.13 (matches); D.8 (matches); C.7 (conflicts
    with D.14); D.5; D.3; D.14; D.15; D.16; D.10; D.17; Appendix H (H.1, Table 1, H.4, limits); Appendix F's text; the
    works cited in full.
  - Asked for and not read, by the reader's choice and said so: Appendix A's table, B.1's steps, C.1 to C.3, D.1, D.19's
    table, G.1, G.2, F's tables, E beyond its first rows.
  - Boundary: the lemma scripts, the model file, any cited source, the pre-registration record (in the repository
    or outside the two pages); the reader says it could check no proof step.
- Depth job: done. Every pointer it followed was found, and four of them surfaced a disagreement (C.7 against D.14;
  D.3's shares; D.14's second condition; Appendix E's labels).
- Change requests: H8-2, H8-5, H8-7.

## F18 (P5-D, Sonnet)

- Reading note: the whole main text and the supporting material as extracted text; no rendered figure was seen (the
  tab closed near the end); table bodies of the D, F, G and H appendices loaded late and were not read; Appendix E
  was read to about G-16.
- Main results stated: homogeneity and the uniform shift; the K = 1 fit convex (Hessian tau times a variance), the
  log-mean-exp bounds, the noise ridge with its first-order shift; elasticities and the improvement factor; the chart
  bijection and the exact pull-back; the K-term extension and weak efficiency; the non-convexity of K > 1 by a
  symmetry argument; the soft alternation as a majorize-minimize step; the three sharp-alternation levels; the soft
  certificate D - kappa M; Q1 to Q4 open; the cubesat numbers and the planted recovery. The reader checked
  several statements by hand and found them as written.
- Does not do: the Pareto boundary; causal rates; uniqueness; a global optimum or consistency; non-log-convex
  structure; a second-order certificate at a sharp fit; choose K. The paper does not claim novelty, uniqueness of
  minimizers, that ascent in Section 7 converges, that a decision follows from the fit, or that the scripts are formal
  verification.
- Contradictions with the paper: 0.
- Findings:
  - defect, one cell: Section 3 lists A1 to A10, and L19 declares an axiom "A11" (independent N(0, v^2) row noise)
    that no list in the main text carries (6.17; joins 118): H8-3.
  - defect (precision), one cell: Proof 7 says "Its Hessian is $\tau C$ (Theorem 3)" of the ridge objective; that is
    J_tau's Hessian; the ridge objective's is tau (C + Sigma), the Sigma term being set aside to first order (6.8):
    H8-6.
  - defect (capture), one cell: table bodies loaded late and Appendix E was cut off after about G-16; F10 read these
    tables in full. The same class as the "Loading" incidents of earlier waves (the README's incidents).
  - friction, joining earlier requests: "log-convex" against "convex in u" (6.1; joins 117); "in the exponents"
    and "x = e^w" (6.2); Proposition 3 against Corollary 2 in "the cells held fixed" (6.3; joins 80); Theorem 1's V
    with and without e^(-beta) (6.4; joins 150); the band as a convention (6.5; joins 17); Definition 6's three
    fits and equation (2) (6.6; joins 20, 161; wave 7's equation (2) item); Theorem 2 and R1 (6.7; joins 24, 137);
    Theorem 10 (i)'s instance (6.9); Theorem 11 and the unique minimizers (6.10; joins 98, 139); "certified" and the
    polished point (6.11; joins 21); the elasticity's shifted units (6.14; joins 29, 53; C.4 was not opened); the K
    pick as a modelling choice with no penalised criterion (6.15; joins 95); the decision's use of the fit as a
    band filter (6.16; joins 51, 70); the abstract's "may be" against Section 10's hedge (6.18; abstract).
  - friction, one cell, logged: K = 1's "not_applicable" status against Lemma 1 (6.12; D.8's legend says "a single
    term", without the reason).
- Pointers followed (the depth's job):
  - Asked for and found: L3.9 (carries the R1 caveat in the same words); B's L1 to L3 steps and the statements of L4
    to L20; E's G-2, G-6, G-7, G-8, G-10, G-14, G-15; D.8 (matches); D.9, D.10, D.11 (found); D.14 (found, with the
    400 against 900 rows); C.8; H.1, H.2, H.4, H.5.
  - Asked for and not found or not readable: H.3's table (empty in the extraction); E beyond about G-16 (cut off);
    L16's instance (the statement was read, the instance not).
  - Not read: C.4, C.7, D.1 to D.7, D.13, D.15 to D.19, A, F, G.
  - Boundary: the lemma scripts and the repository test of uniqueness; the rendered figures.
- Depth job: done for what it read, with two pointers that came back empty on a late-loading page (a capture
  defect, not the paper's).
- Change requests: H8-3, H8-6, H8-8.

## Roll-up, wave 8

| Slot | Cell | Model | Stated the main results | Contradictions | Depth job | New findings that count |
|---|---|---|---|---|---|---|
| F01 | P1-A | Sonnet | yes, except the finding (the abstract has none) | 1 (weak) | done, the finding not stated | 1 wrong belief shared with F15 |
| F15 | P2-A | Sonnet | yes, except the finding | 1 | done, the finding not stated | 1 wrong belief |
| F23 | P6-B | Sonnet | yes | 0 | done | 1 defect, 2 frictions |
| F17 | P4-C | Sonnet | yes | 1 (minor) | done, whys owed | 3 frictions, 1 reader-need |
| F10 | P3-D | Haiku | yes | 1 | done, 4 disagreements found | 2 defects, 1 friction |
| F18 | P5-D | Sonnet | yes | 0 | done, 2 pointers empty | 2 defects |

- Wrong beliefs: one, the reversed implication of the abstract's "Pareto improvements increase energy" (F15; F01's
  wording is a weaker form of it). Both readers are at depth A; the sentence is the supervisor's.
- The cluster that recurs in every depth is unchanged: the abstract's phrases (energy, piecewise, white space,
  losing nothing, n-lemma, "log-convex", the title's "Scaling"), the thresholds, "certified", Theorem 11, R1, Definition
  3, the elasticity's units, the K choice. They join earlier requests; none is new.
- Held-out cells against the others: no wrong belief that depth B, C or D produced; the depth A reading carries the
  one wrong belief and the missing finding. F10 and F18, at depth D, found three record inconsistencies between the
  main text and the appendices (900 against 400 rows, D.3's shares, the A11 axiom) that no reader at an earlier depth
  could see; this is what depth D is for.
- For the supervisor, not requests: the abstract's phrases and the missing finding (F01, F15); the Foellmer entry
  (F10; four cells); the silent drop of a zero row as package behaviour (F10, F17).

## Change requests added at wave 8 (H8-n; the driver renumbers)

H8-1. Abstract (the supervisor's hand): "Pareto improvements increase energy, and a design that maximizes energy is
      weakly Pareto-efficient." is read as "raising energy is a Pareto improvement" (F15; F01 in weaker form: wrong
      belief). Constraint: say only what Theorem 9 and its converse note support; no new claim.
H8-2. Section 8: "The worked example of Appendix C.7 has 900 rows, 4 metrics and 3 planted terms. The fit recovers all
      three terms on 16 of 20 such tables" against D.14's twenty tables of 400 rows (F10, F18: defect). Constraint:
      the record says C.7 is one table of 900 rows with no noise and the twenty tables have 400 rows each; say which is
      which.
H8-3. Section 3's list A1 to A10 and L19's A11 (independent Gaussian row noise): add A11 to the list or say the script
      declares it (F18: defect; extends 118). Constraint: the codes in the scripts and in Section 3 agree.
H8-4. Figure 6: the grey near-frontier band is drawn below zero only, while Definition 4 gives a band of |log V| <
      1/tau, and the caption names neither side nor width (F23: defect). Constraint: draw the band on both sides, or
      say it is one-sided; name its width (the K = 1 band 0.024 used at every K, per the Section 8 sentence); figure
      review loop with 41, 141.
H8-5. D.3's per-term table: near-frontier counts 318 and 119 against shares 0.7384 and 0.2616 (318 of 437 is 0.728): say
      the band each column uses (F10: defect). Constraint: the shares in Section 9 (0.74 and 0.26) are the record's.
H8-6. Proof 7 (Corollary 1): "Its Hessian is $\tau C$ (Theorem 3)" of the ridge objective: the ridge objective's
      Hessian is tau (C + Sigma); say that it holds to first order in the noise, or attribute tau C to J_tau (F18: precision defect).
      Constraint: the closed form and L20's statement are unchanged.
H8-7. "Baseline" names Table 2's baseline configuration and, in "the stock (baseline) regime" and "the baseline
      regime's feasible designs", the stock regime (F10, F17: friction). Constraint: one name for each object; the
      glossary's term.
H8-8. Section 9 and the Discussion: what the two-term reading gives over the one-term fit, and what the record holds
      for K = 2 against K = 1 (the checks of D.15), with no held-out comparison implied (F23, F18, F17; wave 7's G09
      asked the same of the terms' meaning: friction). Constraint: say what D.15 holds; add no claim; one clause.
H8-9. Figure 8's caption or Section 9: the triples are picked from a search (105 of 291 fits showed two stable terms);
      say whether a search of the same size on data without planted contention was run and what it gave, or that none
      was (F23, F17: friction). Constraint: extends 28; no number not in the record.
H8-10. Section 11: name the estimator class and the call's shape in a sentence (the parameters and their defaults are in
      Appendix F) and say where the conditioning rule sits (Appendix C.4, the Conditioning page) (F17; wave 7's
      G09: reader-need, two cells). Constraint: the marginal-value test, the supervisor decides; no how-to.

Earlier requests gaining cells at wave 8: 5 (three), 17 (three), 19 and 161 (four), 21 (four), 24 and 137 (three),
26, 29 and 53 (three), 35, 36, 37 (two), 49, 50 and 70 (two), 51 (two), 54 (two), 55 (two), 56, 57 (two), 61 (three),
66, 68, 80, 84 (two), 85 (two), 87, 92, 95 (four), 98 and 139 (three), 117, 118, 126, 135, 144, 150, 154 (two).

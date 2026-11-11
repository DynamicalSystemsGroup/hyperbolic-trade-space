# WP28 D-5: the re-test (WP11 round 3), against answer key version 4

Triage of 2026-11-10 by a triager who was neither a reader nor an author; the key itself was never seen, the driver
marked the triager's sentence list (stated / missing / wrong per sentence) against answer key version 4 (OD7).

## What was read

- **Head:** the staged paper and site at af9ffea, served at 127.0.0.1:8791. Returns and briefs verbatim in
  `WP28-retest/` (334fb32, committed before this triage).
- **Paper cells:** depth B P1-B to P6-B; depth C P1-C, P2-C, P3-C, P5-C, P6-C; P4-C held out as in round 2; P6-B2,
  the confirmation read of the held-out P6-B on a fresh brief wording (P6-B itself was read again).
- **Models, by label:** model A read P1-B, P3-B, P5-B, P2-C, P6-C, P6-B2 and R3; model B the rest.
- **Docs:** the task reads R2 (choose K) and R3 (the termination record) on the two pages the cut list changed
  (Examples, Chart), each with a clean checkout at af9ffea in which the reader ran the task's code, as in round 2;
  other docs pages were not given. R1 (install, first fit) was not re-read: its round-2 path passed through no
  changed page. The staging note (scratch `docs-tasks.md`) first said "reading only, no checkout"; it was corrected
  to the briefs as sent, which this record follows.
- **What changed since round 2 (c6d0fff):** the round-2 CR units 1 to 5 and the maths unit (captions of Figures
  1, 4 to 7; main-results items 1, 2, 5, 6; eight boxed statements), and on this head the three sentences of the
  maths check: Theorem 11's K^N + 1 sentence (res-L15), the Methods R1 sentence (sec-methods), the Section 8
  centring sentence (sec-case-construction-1b). WP28's executed cuts are docs only (X-1 the Chart page's holes
  figure, X-2 the Examples page's coordinates figure; X-3 the README); the paper carries no cut at this head.
- **Tags below:** [T11], [R1], [C8] for a stop that names one of the three sentences.

## Per cell, against the key, beside round 2

"Sentences" counts the cell's sentences put to the key (part 2 of the return and the beliefs of parts 1, 4, 5);
"missing" counts the key's items owed at the depth that no sentence of the cell states. Stops are the return's
section 6 entries.

| Cell | Round 3: stated / wrong / missing | Missing (round 3) | Round 2 against the key | Stops r3 (r2) | New since round 2 (main) | Gone since round 2 |
|---|---|---|---|---|---|---|
| P1-B | 11 / 0 / 2 | S4's n-lemma as such; S8's second item | PCA missing; S5 in part; two of S8 | 22 (11) | Fig 1 legend; Fig 3 box; Fig 5; Def 3; Def 6 centring; main-results items 1, 2 | Fig 1 marker against the printed n-lemma; "temperature" unexplained; "binds", "support"; the band a sliver |
| P2-B | 10 / 1 / 2 | S4's n-lemma; S8's second item | half on PCA ("chained" not understood); off-key "convex, one answer" | 16 (12) | Fig 1 term 2's point; Fig 3 box; Fig 5; kappa unset; [T11] | "balanced hard-support geometry"; Theorem 10 (i); Fig 6 streaks unnamed; "regime"; "chained" |
| P3-B | 9 / 0 / 1 | S8's second item | PCA missing; one item of S8; off-key "fitted through the table" | 20 (10) | Fig 3 box and labels; Fig 6 no meeting terms; Fig 9; [R1] (Thm 2) | the surface "through" the table; Fig 1 marker (now a point-against-support stop) |
| P4-B | 14 / 0 / 3 | S8 entire (both items); S4's name | all stated; off-key cell refit (Lloyd with hyperplanes) | 18 (12) | Fig 5; positive weight not outlined; Def 6 centring; "Numerical" item; [R1]; [T11] read as intended | "chained"; "balanced hard-support geometry"; "step B"; Theorem 10 (i); Fig 7 "meaningless alone" |
| P5-B | 13 / 1 / 2 | S8's two items | PCA missing; one item of S8; defects Def 2, k | 24 (18) | Figs 1 to 3; n_eff; selection effect in the maps; Thm 10 (ii); Thm 12 tolerance; centring inferred; [T11] | Def 2 without beta; k for metric and term; Theorem 10 (i); Def 9's name; "step B"; Theorem 12's complementarity |
| P6-B | 14 / 0 / 0 | none | half on PCA; off-key cell refit | 16 (14) | Fig 1 point against support; Fig 4 by order-alpha; Fig 5; Fig 9; a measure of separation; [R1] | "chained"; "balanced hard-support geometry"; "step B"; the title's "Scaling"; thresholds 1e-9 against 0.001 |
| P6-B2 | 8 / 2 / 1 | S8's first item (does not pick the design) | (confirmation read; no round-2 cell) | 19 | n_eff; energy differential; Fig 7's hidden curvature; [T11]; Thm 12 tolerance | (compare P6-B: replicates it on 8 passages) |
| P1-C | 14 / 0 / 0 | none | all stated; off-key "convex, one answer" | 17 (10) | "all of them"; 23.1 against 25; Def 3; Def 6 two fits; [R1]; K = 1 band | Theorem 10; Fig 7 "meaningless alone"; Fig 6 bottom; "126 on 4" read three times (now "all of them") |
| P2-C | 13 / 0 / 0 | none | all stated; off-key "convex, one answer" | 67 (23) | abstract sentences; Table 1 rendering; Def 3; [R1]; [T11]; [C8]; 23.1 against 25; regime swap; uncited references | 900 against 400 planted rows; Fig 6 streaks; Fig 7 "meaningless"; Theorem 12's Hessian |
| P3-C | 11 / 0 / 0 | none | all stated | 16 (21) | "all of them"; Def 3; Def 6 thresholds; [R1]; 6.2 ill-posed refit; 23.1 against 25 | "open and look" order; Table 1 fragments; "hyperbolic"; Def 5's basis; Theorem 12 tolerance; candidates |
| P5-C | 14 / 0 / 0 | none | all stated; two statement problems (CR-14, CR-15) | 18 (12) | "all of them"; Def 3 bounds; Thm 10 (ii); [R1] at Thm 5; [T11]; Corollary 1; within 0.05; -1.7 units | the geometric program's change of variables; sharp/soft "certified"; Theorem 12's complementarity; R1's "balanced point" undefined; eq (1) against (2) on centring (closed by [C8]) |
| P6-C | 13 / 0 / 0 | none | all stated | 31 (37) | "posynomial" against the sharp default; [C8]; [R1] twice; [T11]; Fig 3 caption; 23.1 against 25; within 0.05; -1.7 units | Table 1 fragments; Theorem 4 trivial; Section 5 "analysis, not part of the fit"; Fig 4 caption against 0.092; 900 against 400 rows; Section 13 |

Depth B states the main results in every cell except S8's second item (five of six cells) and S8 entire (P4-B, P5-B);
PCA, missing or half in five B cells in round 2, is stated in all six (main-results item 5 now says "compose").
Depth C states the whole argument in every cell, S7 included. Stop counts are the readers' habits more than the
paper's (P2-C's 67 is one reader's thoroughness; P3-C and P6-C fell); the comparison that counts is the replicated
list.

### Friction replicated in two or more cells (round 3; the round-2 count beside it)

- Figure 3's box "returns 7 of 8 metrics ... settling time (not returned)" against the caption's count: 9 cells (1).
- Definition 3 "the package's mean subtracts the constant (log K)/kappa": 10 cells (3, as CR-22's "sum by default, or
  mean").
- Outlined but grey, and the reverse (positive weight, not outlined; participating against contending): 12 (9).
- Figure 8 "3 of ten": 8 (11). Figure 5's "they reach the line and stop there" against the image: 8 (4, as "cannot
  show the edge"). Energy differential: 7 (5). Figure 6 bottom lattice and term 3 across alternatives: 10 (7).
  The 0.99 pair: 7 (7). Figure 7, what it adds: 6 (8). "The K = 1 fit's band as at every K": 5 (5). Why 0.1: 6 (10).
  n_eff at depth B: 5 (10). Hypothesis codes: 7 (5). Main results "Numerical: the termination status": 3 (3).
- Figure 1: the legend's "1.00, 1.00, 1.00", 5 (1); the point at the fit temperature against the tau = infinity
  support, 3 (2, as the marker); term 2's point off its ring, 4 (new).
- Depth C only: "23.1 designs" then "about 25 of the 706", 5 of 5 (new, CR-10's sentence); "659 on 8, all of them"
  read as all 706, 4 of 5 (new, CR-25's sentence); Definition 6's cell fit against Section 6.2's "f_k over all
  rows", 4 (2, CR-15); Section 6.2's numbers against "certified", 4 (5, every reader now states the conclusion);
  rescaling one metric against Proposition 1, 3 (1); propose-predict-check, 4 (4); the abstract's "data underlying
  the table", 3 (1); "within 0.05", the -1.7's units, "We explain tensions", Section 4's "invariant", "Why a
  frontier", the requirements' "at most one of five", the uncited multiplicative-DEA references: 2 each.
- [T11] 7 cells; [R1] 8 cells; [C8] 3 cells (next section).

Gone since round 2, named by no cell: "balanced hard-support geometry"; "step B, unpenalized" as an undefined step;
"chained"; "regime" before its gloss; Figure 6's unnamed streaks (four cells say the caption helped); Figure 7's
"meaningless alone"; the 900-row against 400-row planted tables; Figure 4's caption against 0.092; Table 1's
fragments; Definition 2 without beta; k for a metric and a term; the geometric program's change of variables;
Theorem 12's strict complementarity; Theorem 10 (i)'s "so" as a stop (three cells followed it); the convex fit read
as "one answer" (P2-B's "the same answer up to ties" is marked stated, loosely).

## R-13, condition by condition

1. **No wrong belief from the key's list in any cell: met.** The driver: "no W1-W8 belief in any of the twelve
   cells". One statement is wrong against the key (S5) in four sentences of three cells, P2-B.6, P5-B.2, P6-B2.7 and
   P6-B2.8: "the several-term fit read as a per-cell one-term refit" ("Each term is therefore fitted against its own
   cell ... not against the whole data set", P6-B2). In the driver's words its source is "Theorem 11's box wording
   'refitting each term on its new cell' read without 6.2's first sentence": a statement wrong against the key, not
   a W1-W8 belief, and a defect of the box's wording (CR-35). Round 2 logged the same reading off the key in P4-B
   and P6-B; this round P4-B and P6-B state the alternation without it, and three other skim cells carry it.
2. **Every main result of the key stated at depth B in every cell: not met on S8.** S8's second item (the method
   claims no novelty; it does not replace PCA or Pareto analysis) is missing in P1-B, P2-B, P3-B, P4-B and P5-B; S8's
   first item (does not pick the design) is missing in P4-B, P5-B and P6-B2. (The driver's summary names P4-B alone
   as missing all of S8; the driver's per-cell mark for P5-B, "S8's two items", says P5-B does too; this record
   follows the per-cell marks.) S4's n-lemma name is missing in
   three B cells. Every other main result is stated in every B cell, and PCA (missing or half in five B cells in
   round 2) is now stated in all six. Round 2 marked two items of S8 stated in P1-B, P2-B, P4-B and P6-B: on S8,
   depth B is worse than round 2. No cut touches what depth B reads (the paper has no cut at this head); the
   main-results list does not carry S8's second item (below), so the misses trace to the slice, not to WP28.
3. **At depth C no "why" that round 2 did not already carry: not met on the letter.** New "why"s, with their
   source; none traces to a cut:
   - from the three sentences of this head: what K^N + 1 is for and whether it is a result (P2-C, P5-C, P6-C
     [T11]); its uniqueness hypothesis against Theorem 3, why the stop is not stationary, whether reassignment
     keeps cells nonempty, Q1 against it (P5-C [T11]); why a reader needs the centring sentence in Section 8 (P2-C
     [C8]); which objective "rescaling one metric changes which term is tangent" refers to, f_k being shift-invariant
     (P5-C, next to [C8]);
   - from round-2 CR sentences: "23.1" against "about 25" (all five C cells; CR-10); "all of them" (four; CR-25);
     the mean's bounds under Theorem 8 (P5-C; CR-22's sentence);
   - from passages unchanged since round 2, read by new readers: the -1.7's units, conditioned or physical (P5-C,
     P6-C); "within 0.05" of what (P5-C, P6-C); Corollary 1 for approximate minimizers and the soft alternation's
     descent (P5-C); "posynomial" against the sharp default (P6-C); Theorem 9's "through an active term" (P6-C);
     the sampling plan (P6-C); Section 4's "invariant" (P2-C, P6-C); the regime finding as a swap of correlated
     metrics (P2-C); "one in each regime's own part" (P3-C).
   Carried by round 2 and still open: R1 at finite tau (round 2's (d): P5-C, now naming the R1 sentence); whether R1
   holds on the case (round 2's (f): P1-C, P2-C, P3-C; tested since 4c9416c, not said in the text); Definition 6
   against Section 6.2 (CR-15); the K = 1 band at every K (CR-23); term 1 on 3 designs and the planted failures
   (CR-11); multiplicative DEA (the supervisor's item 4); the centring at equation (1) (round 2's (a), now answered in
   Section 8, which P6-C wants earlier).
4. **No replicated friction that names a cut or a pointer: met.** No paper cell can name one (no paper cut at this
   head). R2 and R3 name neither removed figure nor anything near them; the one pointer both stop on, "read on the
   termination page", is DCR-8's (923857d), not a cut's, and they stop because the re-read gave them two pages only.

## The three sentences of this head, as read

- [T11] Theorem 11's "stops within K^N + 1 iterations": seven cells (P2-B, P4-B, P5-B, P6-B2, P2-C, P5-C, P6-C).
  P4-B reads it as intended ("Fine as a finiteness bound"); six find it empty ("astronomically large", P2-B; "a
  trivial bound (number of partitions plus one)", P6-B2; "says almost nothing", P6-C); P5-B and P5-C set its
  hypothesis "unique term minimizers" against Theorem 3's non-strict convexity and the 0.99 pair. CR-36.
- [R1] the Methods R1 sentence: five of five C cells and three B cells (through Theorem 2's box). Hard to picture
  (P1-C, P3-C, P6-C); whether it holds on the cubesat, "I could not find a statement that it was checked" (P2-C;
  P1-C, P3-C); P5-C: Theorem 5's sketch uses R1, a tau = infinity statement, to identify the finite-tau elasticities.
  CR-37.
- [C8] the centring sentence: P5-C uses it as intended (round 2's (a) closed: "the two coincide on centred data");
  P6-C needed it earlier ("acknowledged only in Section 8 ... until then I was unsure what equation (1) meant"); P2-C
  "did not know why a reader needs it here". At depth B, where Section 8 is not given, P5-B infers it ("the fit
  appears to need the data centred"). CR-38.

## Docs: R2 and R3

- **R2 (read a tension report, choose K): done; nothing broke.** Chose K = 1 as the report to act on, with K = 3 as
  a check; ran `k_terms.py` and the page's blocks; every number matches the page (17, 10 and 73 percent and 0.243 to
  0.132 to 0.088 at the one-term temperature). Round 2's R2 chose K = 3 on the same facts (no criterion for K; term 1
  thin at the re-selected temperature): the reader's judgement, not a page defect. Round 2's DCR-1 is gone (the page
  compares at the fixed temperature and R2 confirmed it). Remains: shares under two names (DCR-3; "took a
  recomputation"). New stops: "No pair ... reaches a rank correlation of 0.99" against Figure 5's 0.99 (two measures
  and two row sets, read first as a contradiction); the share above V = 1 rising with K at fixed tau (0.092, 0.190,
  0.258) beside the slack comparison; "5-lemma" and "exact-maximum support" as further names of the contending set;
  pairs inside the set near zero association under "negative = tension"; a price of 7.92 bands. None names a cut.
- **R3 (the termination record): done; nothing broke.** Answered on the K = 1 fit (converged by the solver's message
  and zero residuals; no certification applies at K = 1) and reported K = 2 and 3 certified; round 2's R3 answered
  on K = 3. Both are right for the record read; "for the example" named two fits again, as round 2's harness note
  warned. With the Termination page not given, R3 answered from the docstrings ("Without the checkout I could not
  have answered"). Remains: the record's shares (26, 23, 51) against the page's (17, 10, 73) (DCR-3); K = 1's
  max_gap 8.7e-6 against eps_kkt 1e-8 (round 2, once). None names a cut.

## P6-B2, the confirmation read: its four answers

- **The surface against the nondominated set:** stated. Not the Pareto boundary and not the nondominated set; about
  a tenth lies beyond it; an upper hull of the sample only at tau = infinity; the Pareto boundary a property of the
  system, not of the sample.
- **How a several-term fit is computed:** wrong against S5 (P6-B2.7, P6-B2.8): "refit each term's exponent vector and
  offset on the designs of its cell alone ... not against the whole data set". The Theorem 11 box's wording (CR-35).
- **PCA:** stated. "They are different tools that compose"; PCA gives Figure 7's axis only, a reading of the sample;
  the exponents are not principal directions.
- **Another name:** stated (no novelty held). Aigner-Chu's Cobb-Douglas LP frontier at K = 1 and tau = infinity, a
  smoothed LP at finite tau, max-affine or CNLS-like at K > 1; what it adds: one vocabulary across frontier and Pareto
  analysis, the reversible chart, one-term convexity, the several-term certificates.

## Change requests (CR-35 onward)

Each names the passage (notebook cell id in `paper/paper.ipynb`, or the generator), the problem in the readers'
words with the cells, and the constraint. WP28 adds no content: each is a narrowing or a placement, the shorter
wording preferred; a sentence with a claims-register row is re-pointed in the same commit.

- **CR-35 (Theorem 11's box, `res-L15`; local).** Passages: the hypothesis "step B, the refit of each term on its
  cell, unpenalized ... each refit an exact minimizer of f_k" and the statement "refitting each term on its new cell
  does likewise". Problem: three skim cells and the confirmation read state the several-term fit as a one-term fit on
  the cell's rows ("refit each term on its own designs", P2-B; "refitting each term on its cell", P5-B; "fitted
  against its own cell ... not against the whole data set", P6-B2), the one statement this round marked wrong; two
  main-text readers meet the contradiction with Section 6.2 (P2-C, P6-C). The box is what depth B reads; Section
  6.2's first sentence ("Every term is fitted against every design ... the support over all rows", `sec-results-
  algorithm`) is not in it. Constraint: the box says what the refit is in 6.2's words, replacing and not adding:
  "step B, the refit of each term by $f_k$ (its support over all rows less its cell's mean), unpenalized ...";
  "refitting each term by $f_k$ does likewise". Not this CR: the sentence of cell 853a940d ("The contending set's
  exact-maximum fit on the cell is $f_k$ itself on the cell's rows") and Definition 6, read against 6.2 by P2-C,
  P5-C, P6-C, are round 2's supervisor item 3 and stay there.
- **CR-36 (Theorem 11's K^N + 1 sentence, `res-L15`; local).** Passage: "With unique term minimizers and a fixed tie
  rule the sharp alternation stops within $K^N+1$ iterations (Appendix B, L15.17 to L15.22)". Problem: seven cells;
  six read the count as empty ("astronomically large ... a practical bound or only a proof of termination", P2-B;
  "a trivial bound", P6-B2; "unsure whether it was meant as a result", P6-C); P5-B and P5-C set "unique term
  minimizers" against Theorem 3 ("I could not tell whether the uniqueness hypothesis is expected to hold on the
  case", P5-C). Constraint, one wording: "With unique term minimizers, which Theorem 3 does not supply, and a fixed
  tie rule the sharp alternation stops after finitely many iterations (Appendix B, L15.17 to L15.22); stationarity
  of the stop, and convergence otherwise, are not claimed." The count stays in L15.
- **CR-37 (R1: Theorem 5's sketch, `res-L7`, and the case's K = 1 sentence, `num-k1` from
  `generate_findings.k1_sentence`; local).** Passages: "Identifying these rates with the fit needs Theorem 2 and R1"
  (`res-L7`); the Methods R1 sentence (`sec-methods`). Problem: R1 is now stated at tau = infinity, and P5-C: "R1 is
  explicitly a tau = infinity statement ... yet the elasticities are read at the fit temperature. I could not see
  which hypothesis licenses reading finite-tau exponents as identified elasticities"; three C readers ask whether R1
  holds on the case ("I could not find a statement that it was checked", P2-C; P1-C, P3-C), while
  `tests/test_paper.py::test_the_regimes_contending_set_is_the_unique_lp_optimum_not_a_solver_choice` (4c9416c)
  checks it on both regimes. Constraint: the sketch names what it uses, "needs Theorem 2's hypothesis (R1's relation
  at the fit temperature)" (a narrowing, no longer than now); and `k1_sentence` adds one clause backed by that test,
  "R1 holds on both regimes: the exact-maximum optimum is one point, so the support is not a solver's choice", with
  a claims-register row citing the test (the one addition here; the alternative is to leave the check to Appendix
  D and say so in the sketch).
- **CR-38 (the centring sentence, `sec-case-construction-1b`; placement).** Passage: "This conditioning centres each
  log-metric (the standard scaler), so at K=1 the fit's objective of equation (2) ... is that of equation (1); on
  uncentred log-metrics the two differ by the linear term ... and need not share a minimizer." Problem: the sentence
  compares two equations, and Section 8 is where neither is: P2-C "did not know why a reader needs it here"; P6-C
  needed it at equation (1) ("until then I was unsure what equation (1) meant"); P5-C read it as the link between
  the two objectives. Constraint: the comparison moves to `sec-results-algorithm`, after "with $f_k$ convex by
  Theorem 3", the first place both equations stand ("On centred log-metrics, as the case's conditioning makes them,
  $f_1=J_\tau$ and equation (2) at $K=1$ is equation (1); otherwise they differ by $\bar u_1\cdot w$."); Section 8
  keeps "This conditioning centres each log-metric (the standard scaler)." Net words not above the present
  sentence; claims-register C421 re-pointed; the ledger rows of both sections.
- **CR-39 (the effective sample sentence, `num-temperature` from `generate_findings.temperature_sentence`; local).**
  Passage: "the effective sample size is 23.1 designs ... so the exponents at the fit temperature rest on about 25
  of the 706 designs". Problem: five of five C cells ("Why 23.1 in one place and 'about 25' in the next?", P1-C;
  "23.1 rounded is 23, not 25", P3-C; "two numbers for one quantity", P6-C); `_about` rounds to the nearest five.
  Constraint: one number: "rest on about that many of the 706 designs", and `_about` goes if nothing else calls it.
- **CR-40 (the nondominated sentence, `num-nondominated` from `generate_findings.nondominated_sentence`, line
  "on {columns}, all of them"; local).** Passage: "the nondominated set holds 126 on 4 attributes (...) and 659 on
  8, all of them". Problem: four of five C cells read "all of them" as all 706 designs ("659 is not all of 706",
  P1-C; P3-C, P5-C, P6-C); it means all 8 attributes. Constraint: "659 on all 8" (shorter).
- **CR-41 (Figure 3's caption, `fig-behavioural-caption`; local).** Passages: the box, read from the model by the
  views generator (`examples/adcs/model_v2/views`, out of this package's reach): "SlewExperiment returns 7 of 8
  metrics, computed with no slew: pointing error, total mass. From the measurement: control effort (passed on) and
  settling time (not returned)"; the caption: "the measured slew supplies the settling time and the control
  effort, which the analysis passes on, and the analysis computes the other six, pointing error and total mass from
  the configuration alone". Problem: nine cells cannot reconcile the counts ("It says 7 of 8 returned, then lists
  two items", P1-B; "which contradicts '(not returned)'", P2-B; "Six plus two does not parse", P6-C). The box is
  right (the analysis returns seven: control effort passed through and six computed, two of them with no slew;
  settling time goes from the measurement straight to the table); the caption's "which the analysis passes on"
  covers the settling time, which it does not pass on. Constraint, one wording: "the measured slew supplies the
  settling time directly and the control effort through the analysis, which computes the other six (the pointing
  error and the total mass from the configuration alone) and so returns seven of the eight."

**Not a CR: depth B's S8 (a placement question for the driver).** The main-results list (`sec-decision-3`) carries
"not the Pareto boundary" (item 1) and "The method and PCA compose ... a reading and not a result" (item 5); no
item says that the method claims no novelty or does not replace PCA or Pareto analysis, nor that it does not pick
the design. "We claim no priority" opens Section 2 (`sec-prior-art`), which depth B does not read. Five B cells
miss S8's second item and P4-B and P5-B all of S8 because the B slice does not carry it; whether item 5 or item 1 should
(a clause, not a new item) is the driver's call under the depth contract.

## Recommendation on R-13

**Not met as written; nothing lost to a cut.** Conditions 1 and 4 are met: no W1-W8 belief in any of the twelve
cells, and no friction names a cut or a pointer. Conditions 2 and 3 are not met on their letter: depth B misses S8's
second item in five of six cells (all of S8 in P4-B and P5-B) and depth C carries new "why"s in every cell. None of these
traces to a WP28 cut: the paper carries none at this head, S8's second item is not in the slice depth B reads, and
the new "why"s come from the three sentences of the maths check, two round-2 CR sentences and unchanged passages
read by fresh readers. The one statement wrong against the key (four sentences, three cells) is the Theorem 11
box's wording. CR-35 to CR-41 close the paper's part; the S8 placement is the driver's.

Counts: 12 paper cells, 148 sentences marked (stated 144, wrong 4); W1-W8 beliefs
0; missing at depth B 11 key items over 6 cells (S8's second item 5, S8's first item 3, S4's n-lemma name 3); missing at depth C 0; stops 284 (round 2: 180 over 11 cells); replicated passages
43; friction naming a cut or a pointer 0; docs tasks 2 of 2 done, 0 broken.

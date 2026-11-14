# Final reader round, wave 1: the assistant's triage against answer key version 5

Head read: c23cf60 (the stage built from it). Reports: `../reports/{F03,G14,G26,G08,F25,G27,F11}.md`, committed
verbatim at 165917a before this triage. The key (sha256 a041bc84…) is held outside the repository; its marks are
S1 to S9 (what the paper says) and W1 to W12 (wrong beliefs); the depth jobs are A, B, C, D as the grid names them.
One form per report, then the roll-up and the change requests. Classification: wrong belief, missing, friction,
defect (broken link, wrong number, raw markup, stale sentence, stderr line), preference. Counts at once: wrong
belief, defect. Counts at two cells: friction, missing. Logged only: preference.

## G26 (P8-A, wording 2, Sonnet, wave 1)

- Key marks: S1 stated correctly ("an answer plus a justification a responsible executive can follow"); S2 stated
  correctly (a surface fitted to the outer edge as a model of the data, not the Pareto boundary; position and
  distance; terms naming contending metrics with elasticities; complements PCA); "supports a trade study" stated;
  the finding in one sentence stated (one term blends, two separate). The two uses are not in the abstract and were
  not stated (allowed at A).
- Wrong beliefs: none. W1 avoided ("an analyst's tool, not a decision"); W3 avoided; W4 avoided.
- Depth job: done (knows the problem, the idea, the finding; wants to read on, to the example).
- Findings: twelve points of friction on the abstract's wording ("We explain tensions" before the term is defined;
  "the data underlying the table"; "its reading", "views of that model"; "soft support"; "reversible chart" with no
  chart introduced; "GGP" and "kernel"; "run on the chart"; no number anywhere). All on the abstract, which is the
  supervisor's hand: reported to him, changed by no one here. Classification: friction (abstract), logged for his
  close read.
- Pointers at D: not applicable.

## G08 (P1-B, wording 2, Sonnet, wave 1)

- Key marks: S4 stated correctly (terms, n-lemma, elasticities, cells as regions); S5's three levels stated
  correctly ("three grades of assurance", no global promise); S6 stated correctly (thirteen metrics, K = 2 separates
  what one term blends, the shortlist against a baseline that fails the pointing-error and unit-cost requirements,
  about a tenth of designs beyond the surface by convention); S8 at least two items stated (does not replace PCA or
  Pareto analysis; claims no novelty; does not find the best design).
- Wrong beliefs: none.
- Depth job: done.
- Findings:
  - defect: the Figure 4 and Figure 7 captions end with the stray word "enlarge" (the full-size link renders as its
    link text at the caption's end). Also seen by F11 (d). Counts at once.
  - friction: Figure 7's outline-versus-grey rule not followable; the takeaway not in the caption.
  - friction: Figure 8's "term 2" against Figure 7's "term 2" (different fits; the caption says "two triples, each
    fitted with two terms", not enough for the reader). Related: F25 (16), the triples are a selected best case
    and the caption does not say so. Two cells.
  - friction: "certified" and Theorem 12's exactness against a computed tolerance (item 23). Replicated by F03 (25),
    G14 (46, 47), G27 (48), F25 (15). Two or more cells: counts.
  - friction: Table 2's level column "not a ranking" yet used to compare (16); F03 (39), F25 (5) likewise. Counts.
  - friction: Q1 to Q4 named in the main results without their content (18); a depth-B artefact (6.3 is not in the
    B slice); logged.
  - preference: Theorem 10's negative result "in a box" (22); also F03 (24), G14, G27: see the replicated defect on
    Theorem 10 (i) below.
- Pointers at D: not applicable.

## F11 (P4-B, wording 1, Haiku, wave 1)

- Key marks: S4, S5 (three levels), S6 (thirteen metrics; K = 2 separates), S8 (no novelty; not PCA or Pareto; no
  global guarantee) all stated correctly; checked Theorem 1, Theorem 5, Theorem 9 and Lemma 1 by hand and found them
  right; the chart as a change of basis, not a reduction, stated correctly.
- Wrong beliefs: none.
- Depth job: done.
- Findings:
  - defect: Figure 1's legend prints term 2 as (0.44, 0.27, 0.28), which sums to 0.99 while the other terms print to
    1.00 (a rounding display). Counts at once (small).
  - friction: Figure 3's "returns ten of the thirteen" against the arrows counted; the settling-time wording in the
    box against the caption. Also G08 (4) and F03 (29): three cells. Counts.
  - friction: "regime" undefined at its first use in the B slice (d); "energy differential" in a caption before its
    definition (f); also G08 (11). Counts (captions).
  - friction: near-collinear metrics and how the fit separates them (g); the "fewer than ten near-frontier designs"
    threshold undefined (g); F25 (12) on the effective sample size. Logged as friction, one cell each.
  - preference: "lemma" for a count (g); also G14 (9), G27 (50): a vocabulary point for the supervisor, not changed.
- Pointers at D: not applicable.

## F03 (P3-C, wording 1, Sonnet, wave 1)

- Key marks: the whole argument stated correctly, S7 included (one illustrative case; conditioning, K and the
  temperature are the analyst's; elasticities describe the sample, not causes; Q1 to Q4 open; thresholds chosen from
  the data's pass fractions); S8 stated; S9 understood as symbolic checks, not formal proof (correct).
- Wrong beliefs: none. W5 avoided explicitly; W1 avoided; W6 avoided.
- Depth job: done with whys left that the main text owes (see the change requests): the three thresholds; the
  contending set's cell-rows fit against "ill-posed"; which feasibility step precedes the fit.
- Findings (45 items; the ones that count):
  - defect: "they reached the four-metric frontier by spending the battery (Section 10)" points at the Discussion,
    which does not mention the depth of discharge (38). Counts at once.
  - defect: "63.7 % of the baseline regime's feasible designs pass" against D.17's 65.6 % for the same regime (30);
    also F25 (8). A hand-typed number in prose against a generated table: resolve from the data of record and make
    the sentence generated. Counts at once.
  - friction, replicated: the three thresholds (10^-3, 10^-9, 10^-12) and their relation (14); G14 (8), G27 (12e),
    F25 (11). Counts.
  - friction, replicated: Definition 6's fit "on the cell's rows alone" against Section 6.2's "refitting a term on
    its own rows alone is ill-posed" (13); G14 (35), G27 (12c, 41). Counts.
  - friction, replicated: "certified" against tolerance (19, 25); see G08.
  - friction, replicated: the Theorem 10 (i) argument (24); G14 (38), G27 (40). Counts.
  - friction: Section 7's "stated for the exact maximum" with no statement to point at (26): the round-2 restoration
    left "stated by whom" open; one cell plus the second readers' note. Counts (two sources).
  - friction: what the system model must supply is never in one place (6, 42); one cell; logged, with a note that
    this is P3's own want and the docs' Getting started carries it.
  - missing: the conditioning rule's defensible scalings (16); D.5 holds the scaler variant; one cell; logged.
  - preference: "hyperbolic" as a light justification of the title (10); F25 (3). Two cells of preference: logged
    for the supervisor's close read of the title, not a change.
- Pointers at D: not applicable.

## G14 (P9-C, wording 2, Haiku, wave 1)

- Key marks: the argument of Sections 3 to 6 stated correctly and checked (Theorems 4, 8, 9 and Lemma 2 by hand);
  S5's three levels and their conditional character stated; S7's open questions stated; the symbolic scripts read as
  checks, not proofs (correct).
- Wrong beliefs: none.
- Depth job: partly done: thirteen whys remain, most of them defects of the text (below), which is what C is for.
- Findings (51 items; the ones that count):
  - defect: Theorem 6's Q is written with 1^T/d where orthogonality needs 1^T/sqrt(d) (30); G27 (10) found the same
    against L8. Counts at once.
  - defect: two objects named V, with and without e^{-beta} (Definition 2 against Appendix A and L1; Proof 1's
    sketch drops beta) (27); G27 (6, 28, 51). Counts at once.
  - defect: Definition 3's "c_k = e^{-kappa beta_k} is the 1/kappa power of a posynomial" is garbled (4); the
    posynomial is the bracketed sum (G27 8). Counts at once.
  - defect: Figure 1's caption names "the case's association maps", defined nowhere (10). Counts at once.
  - defect: Corollary 1's hypotheses cite A5 (isotropic noise) and A9 (general covariance) together (33); one is the
    operative model. Counts at once (small). The ridge's power of tau (32) is tau/2 in the source: no defect.
  - defect: the main text's "the case needs three terms" against the case read at K = 2 (24); F25 (7), G27 (26). A
    stale sentence and a W11 risk. Counts at once.
  - friction, replicated: the thresholds (8); the "band of a seam" and the 37 designs' criterion (49), F25 (15);
    "certified" for a tolerance status (46, 47, 48, 50); Corollary 2 bounds the fixed-cell improvement only (44),
    G27 (46); Theorem 10 (i) needs "every symmetric point" (38), G27 (40); Theorem 11's finite stop needs the
    strict decrease stated in the theorem (40), G27 (42). Counts.
  - friction: "Derived" must say whether the script proves the general statement or checks instances (26); G27
    (47). Counts.
  - friction: R1 used in Theorem 2's hypothesis as a statement about the finite-tau minimiser (14, 28); G27 (17, 30).
    Counts.
  - friction: Theorem 5's hypotheses do not say K = 1 (29); G27 (34). Counts.
  - preference: Definition 2's "same along every path" adds nothing (3). Logged.
- Pointers at D: not applicable.

## F25 (P7-D, wording 1, Sonnet, wave 1)

- Key marks: S6 stated correctly in full (thirteen metrics; 2,134 and 2,355 feasible; the K = 1 and K = 2 fits and
  their leaders; the six requirements read after the fit; 548 and 28; the priced question; the baseline fails the
  pointing-error requirement); S7 stated with the cost coverage and what the case leaves out (W10 avoided: "a lower
  bound ... excludes payload ..."); W6 avoided ("a demonstration and says so"); S9 stated (the symbolic scripts,
  "business casual").
- Wrong beliefs: none.
- Depth job: done: eighteen pointers followed and found (C.1 to C.8, D.1 to D.7, D.9 to D.11, D.15 to D.17, D.19,
  E to G-11); not followed: B, F, G, H.
- Findings (23 items; the ones that count):
  - defect: the Discussion's "changes the one-term contending set by at most one of its five metrics" against the
    seven-metric set (21). A stale number in prose. Counts at once.
  - defect: Appendix E's gap rows quote tau and bands for the unfiltered 3,000-design table while Section 9 and D.2
    give the 2,134-design fit of record, and the page does not say which (22). Resolve: the ledger states its
    dataset or is regenerated from the data of record. Counts at once.
  - defect: "63.7 %" (8); see F03.
  - defect: "the case needs three terms" (7); see G14.
  - missing: the elasticities are percentages of the conditioned metrics, not of the raw attributes, and the raw-unit
    pull-back (Theorem 7) is never printed for the case; a hardware reader reads "0.9 percent" as physical (4). One
    cell; a real reader trap for P7's persona. Counts as a change request on the strength of the persona (one
    sentence at the elasticity's first case use saying the percentages are of the conditioned metrics, with the
    pointer to Theorem 7).
  - missing: the closing question's 0.56 M USD is the difference of two fleets that differ in wheel class, tracker
    grade and fleet size, not the price of the tracker alone (17). One cell; the sentence says "whether a fine star
    tracker ... is worth about 0.56 M USD", which a careful reader can take as the tracker's price. A one-clause fix
    ("the two fleets differ in wheel, tracker and size"). Counts on the strength of the finding.
  - friction: D.19 lists design 190 as nondominated against 999 at the printed precision (18); the printed digits
    should decide it or the text say they tie. One cell; small; include with the defects.
  - friction: the regressor's band 0.0935 in propose-predict-check is not explained where used (20). One cell.
  - friction: Figure 6's position axis is the K = 1 band's first principal direction used with a K = 2 level, said
    in Section 9 but not in the caption (14). One cell.
  - friction: total mass at 0.02 participates but is not in the 7-lemma; Definition 6 names the reverse case only
    (11). One cell.
  - friction: Section 5 states the favourable variant of D.5 (the target fraction) and not the scaler variant that
    changes the contending set (6). One cell; a claims matter: the sentence is backed as written, the omission is
    the reader's point. Logged for the supervisor.
  - friction: the title word names the two-metric case (3); see F03.
- Pointers at D: asked for 18, found 18 (the boundary: the model files and code are out of reach by design).

## G27 (P9-D, wording 2, Sonnet, wave 1)

- Key marks: Sections 3 to 6 and Appendices A and B stated correctly in detail; the scripts read as bookkeeping,
  not a proof assistant (correct); S5 and S7 stated; the K > 1 limits stated.
- Wrong beliefs: none.
- Depth job: done: eighteen moves into the supporting material, every pointer found, one proof followed to its
  script lines (L3.9, L5.25, L8, L9, L10, L11, L14 to L17, L20).
- Findings (59 items; the ones that count beyond those shared above):
  - defect: A3 is tau in (0, infinity] in Section 3 and tau > 0 in L2 and L4; the same for A6 and kappa (1).
    Counts at once.
  - defect: n_k means the size of the contending set in Definition 6 and the number of designs labelled k in 6.2
    and L14, both in Appendix A's table (12d). Counts at once.
  - defect: Theorem 9's main-text statement claims efficiency for an all-positive active term at K > 1 while L11's
    statement claims weak efficiency only (37). Counts at once.
  - defect: the conditioning formula's letters swap roles between Section 5 (a_j the attribute, s_j the shift) and
    L9 and L18 (a_j the shift, r_j the attribute, s_j a log-spread) (23). Counts at once.
  - defect: Definition 4's band is strict while L5's is closed (9). Small; counts.
  - friction, replicated: the thresholds, the two Vs, Q's normalisation, Theorem 10 (i) and (ii), Theorem 11's
    hypotheses stated mid-text, Corollary 2's reach, "certified", R1 in Theorem 2, Theorem 5's K = 1: see G14.
  - friction: "support" in two senses in neighbouring paragraphs (38); "offset" for beta, b_j and log V (35);
    "frontier" for three objects (51); c, k, p, v, s each with two meanings (29, 59). One cell each, from the one
    reader whose job this is; counts as the notation scrub the two experts both ask for.
  - friction: Appendix A rows missing for alpha_j, s_j, b_j, p, B, P, C, Sigma, alpha_ik, x_k, theta_k, W, label,
    slack, offset, support (52). One cell; part of the scrub.
  - friction: H1, H2 and "step B" in L15 and L14 undefined (42, 45); the lemma pages are generated from derivation/,
    off limits in this release; logged for the post-0.1 list.
- Pointers at D: asked for 18, found 17; "a list of the hypothesis codes" named in Section 6 was found only inline
  (not found).

## Roll-up, wave 1

| Cell | Report | Model | Key marks | Wrong beliefs | Depth job | Counting findings |
|---|---|---|---|---|---|---|
| P8-A | G26 | Sonnet | correct | none | done | 0 (abstract friction, reported to the supervisor) |
| P1-B | G08 | Sonnet | correct | none | done | 1 defect (enlarge), 3 replicated frictions |
| P4-B | F11 | Haiku | correct | none | done | 1 defect (0.99), 2 replicated frictions |
| P3-C | F03 | Sonnet | correct | none | done, whys owed | 2 defects, 5 replicated frictions |
| P9-C | G14 | Haiku | correct | none | partly (defects) | 6 defects, 9 replicated frictions |
| P7-D | F25 | Sonnet | correct | none | done | 4 defects, 2 missing, 5 frictions |
| P9-D | G27 | Sonnet | correct | none | done | 5 defects, the notation scrub |

No wrong belief in seven reports. Model readers establish recall and the location of stumbles; what they cannot
establish (ease of a human reader, fatigue) is not claimed. Silence is weak evidence. Stopping rule: not yet
assessable (one wave of eight; a replicated friction is open until the fix lands and a later wave does not raise it).

## Change requests from wave 1 (each names the passage, the problem and the constraint; no persona, no depth)

Defects (count at once), one paper-queue unit:
1. Figure 4 and Figure 7 captions: the "[enlarge](...)" link renders as the bare word "enlarge" at the caption's
   end. Make the link text a phrase ("full-size figure") or move it out of the caption. Constraint: the figure-review
   rule's shows/does-not-show lines stay.
2. Theorem 6: Q = [B; 1^T/d] in the main text; L8 has 1^T/sqrt(d). Correct the main text; the proof sketch's "the
   blocks of QQ^T" then holds.
3. V with and without e^{-beta}: Definition 2 (with), Appendix A's register row and L1's statement (without), Proof
   1's sketch ("A1 gives V = exp(w.u)"). One object, one formula: the register row and the sketch say the scaled V,
   or the unscaled one gets its own symbol. Constraint: the lemma scripts are not edited; the statement text that the
   appendix prints from them is theirs, so Appendix A's row and the main-text sketch move toward L1 or the discrepancy
   is named in one sentence.
4. Section 3, A3 and A6: "tau in (0, infinity]" and "kappa in (0, infinity]" against the scripts' tau > 0 and kappa
   > 0 (L2, L4, L10, L16). State the convention once: the axioms are for finite values, infinity is the exact limit
   named where used.
5. Definition 3: "c_k = e^{-kappa beta_k} is the 1/kappa power of a posynomial" is garbled; say that V_K is the
   1/kappa power of the bracketed posynomial, and that e^{kappa Phi_K} is the posynomial.
6. Definition 6 and Appendix A: n_k is used for the size of the contending set and for the number of designs
   labelled k. Two names.
7. Section 5's simplifying assumption (iv), "the case needs three terms": the case is read at K = 2 (D.15). Correct
   the sentence to what the case shows (K = 2 chosen; K = 3 certified, with a thin term).
8. Section 8: "63.7 % of the baseline regime's feasible designs pass" against D.17's 65.6 % for the baseline regime.
   Resolve from the data of record; the sentence becomes a generated value with its register row.
9. Discussion: "changes the one-term contending set by at most one of its five metrics": the K = 1 contending set
   has seven metrics. Correct from the record (D.5 or D.17).
10. Section 9: "they reached the four-metric frontier by spending the battery (Section 10)": the Discussion does not
    discuss it. Point at the passage that does (D.10 or the Discussion's requirements paragraph) or drop the pointer.
11. Appendix E: the gap rows quoting tau and bands (G-2, G-9 and any other) describe the unfiltered 3,000-design
    table while Section 9 and D.2 give the 2,134-design fit of record. Either each row names its dataset or the
    ledger regenerates from the data of record.
12. Theorem 9: the main text claims efficiency at K > 1 for an all-positive active term; L11's statement claims weak
    efficiency only, with the stronger step inside the script. The main text states what L11 states, or L11's
    statement is extended by the lemma-script owner (post-0.1); for 0.1 the main text yields.
13. Corollary 1: hypotheses A5 and A9 together; keep the operative noise model (A9 with Sigma; A5 as its isotropic
    case) and say so.
14. Figure 1 caption: "the case's association maps" names nothing; drop or define.
15. Figure 1 legend: term 2 prints (0.44, 0.27, 0.28); print the rounding so the three sum to 1.00 as the others do.
16. Section 5 and L9/L18: the conditioning letters (a_j, s_j, r_j) swap roles between the main text and the
    scripts; align the main text's letters to the scripts' or name the correspondence once in Appendix A.
17. Definition 4's band strict, L5's closed: one convention, stated.
18. D.19: design 190 prints as nondominated against 999 at the printed precision (equal pointing error, higher
    cost); print the deciding digit or say the two tie.

Replicated friction (counts at two cells), the same unit, wording only:
19. The three thresholds (participation 10^-3, the contending set's 10^-9, numerically zero 10^-12): one sentence,
    where the first is introduced, saying what each is for and how they nest.
20. Definition 6's "on the cell's rows alone" against 6.2's "refitting a term on its own rows alone is ill-posed":
    say in 6.2 that the ill-posed refit is the finite-temperature one inside the alternation and the contending set's
    exact-maximum fit is well-posed, or whichever is true.
21. The stopping declaration and "certified": say once that certified is a tolerance-based status at the returned
    point, that Theorem 12 and Proposition 3 hold at the exact point the fit approximates, and that Corollary 2 bounds
    the improvement with the cells held fixed.
22. Theorem 10 (i): state the argument as the instance shows it (the objective is lower at a distinct-term point than
    at the symmetric point, so it is not convex), without the "symmetric minimizer" clause, or state "every symmetric
    point".
23. Theorem 11: move the uniqueness and tie-rule hypotheses into the Hypotheses line.
24. Theorem 2 and R1: say that R1 is a tau = infinity condition and that the hypothesis "w_j > 0 for every j" is
    taken at the fit temperature on its own, with L3.9 as the pointer.
25. Theorem 5's hypotheses: add K = 1.
26. Figure 3's caption against its boxes: the count "ten of the thirteen" and the settling time's route; one
    consistent statement.
27. "Energy differential" at its first appearance in a caption (Figure 6) gets "(log V, the level)"; "regime" at its
    first caption use gets its gloss.
28. Figure 8's caption: say that the triples are their own two-term fits, chosen from a search of every triple, and
    how many triples showed two stable terms.
29. Section 9, first case use of an elasticity ("one percent gained in available power is 0.9 percent given up in
    unit cost"): say the percentages are of the conditioned metrics and point at Theorem 7 for the raw-unit rates.
30. Section 9's closing paragraph: one clause that the two fleets compared differ in wheel class, tracker grade and
    fleet size, so the 0.56 M USD is the fleets' difference, not the tracker's price.
31. "Derived": say in Section 6's preamble whether a script proves the statement for arbitrary d or checks it on
    instances (the proof-conventions note knows; the sentence must).

To the supervisor (not changed here): the abstract's phrases the executive stumbled on ("We explain tensions"
before the term; "the data underlying the table"; "soft support"; "reversible chart"; "GGP" and "kernel"); the title
word naming the two-metric case (two cells); Section 5 stating D.5's favourable variant only; the vocabulary
"n-lemma" as a count (three cells, preference).

Post-0.1 (recorded): H1, H2 and "step B" in the lemma scripts' generated text; Appendix A's missing rows for the
scripts' symbols; L11's statement weaker than the main text's claim (if the main text does not yield).

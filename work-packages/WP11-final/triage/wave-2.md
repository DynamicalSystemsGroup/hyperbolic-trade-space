# Final reader round, wave 2: the assistant's triage against answer key version 5

Head read: c23cf60. Reports: `../reports/{G02,F19,H01,F12,H02,F04,G21}.md`, committed verbatim at ac01241 before this
triage. Forms as in `wave-1.md`; counting rules the same.

## G02 (P2-B, wording 2, Haiku)

- Key marks: S4, S5's three levels, S6 (thirteen metrics; the K = 1 exponents read off Figure 4; K = 2 splits the
  frontier into two contending regions), S8 (no novelty; not PCA or Pareto; the level is not a ranking) all stated
  correctly; Theorems 4, 5, 9, Lemma 1 and Proposition 2 checked by hand and found to follow; Figure 5's slope checked
  against Figure 4's exponents.
- Wrong beliefs: none.
- Depth job: done.
- Findings that count: the "(Section 9; Numerical)" tag that names no heading (6.16; F11 (j), G21: three cells);
  the main results' "second-order certificate" where Theorem 12 says a strict local minimiser (6.19); Definition 1's
  "none of the table's designs exceeds" read as Table 2 (6.20; G21: two cells); Definition 3's sum, mean and maximum
  in one paragraph (6.21; four cells with G14, G27, G21); n_k with two meanings (6.23; counted at wave 1); f_k's two
  scopes (6.24; three cells); Figure 6's position axis being a principal direction and not Z (6.25; F25 (14): two
  cells); Table 2's "the executives' measures" undefined to the skimmer (6.15; F11, G21: three cells); the duplicate
  "(L14)" label (6.31; G27, G21: three cells); near-duplicate metrics in Figure 7 with no word on what that does to
  the fit (6.7; F11 (g): two cells); the stray "enlarge" (counted at wave 1). Logged: J_tau used before its equation in
  the B slice (a slice artefact), the "Abstract" heading with no text under it (the B capture's headers file).

## F19 (P6-A, wording 1, Haiku)

- Key marks: S1 stated; S2 stated (the surface as a model of the data, not the Pareto boundary; the chart; terms and
  elasticities); supports a trade study stated; the finding stated; wants to read on, with the specific question a
  frontier economist asks (how the soft fit differs from DEA, stochastic frontiers and a log-linear envelope).
- Wrong beliefs: none; W4 avoided ("I would not yet call the difference substance or vocabulary").
- Depth job: done.
- Findings: the abstract's phrases ("explain tensions"; "coordinate system"; "a few" unquantified; "reversible";
  "active"; "kernel" and "compatibility"; "feature engineering" without the concrete claim). All on the abstract: for
  the supervisor, four cells now (G26, F19, F04, F03).

## H01 (P1-ROOT, wording 1, Sonnet) and H02 (P8-ROOT, wording 1, Haiku)

- Key marks at depth A on the root page's first screen: the problem stated (trade studies lose the designs' detail;
  alternatives bespoke or opaque); the idea stated (a surface fitted to evaluated designs, read for which trade-offs
  lead where); supports a trade study stated; no finding is on the first screen and none was invented; both would
  read on, briefly, to a worked example.
- Wrong beliefs: none in either (W1 avoided by both: "It does not choose a design for you"; W6 avoided: "the example
  is constructed").
- Depth job: done for the slice given.
- Findings, both cells, for the supervisor's close read of the root page (changed by no one here):
  - the plain-language summary paragraph stops both executives at "posynomial invariant form", "invariant" (invariant
    to what) and "unsupervised" (what is predicted); the gloss "a sum of terms each a product of powers of the metrics"
    is read as algebra. Two cells.
  - "The alternatives are bespoke or opaque" names no alternative. Two cells.
  - the three conditions read as a promise the first screen does not redeem (the figure follows). Two cells.
  - the figure's caption terms "exponent vector", "frontier", "reference surface", and the label "favours metric 1"
    are opaque to both; the dots' size difference is not visible; the first screen cuts the triangle's lower corners
    at 1280 by 800. Two cells.
  Classification: friction on an entry surface, replicated; routed to the supervisor with the proposed wordings in
  the change list, not applied.

## F12 (P5-C, wording 1, Haiku)

- Key marks: the argument of Sections 3 to 6 stated correctly and checked (Theorems 3, 4, 5, 6, 9, Lemma 1, Lemma 2,
  Proposition 3 by hand; the K = 2 numbers' internal consistency); S7 stated (Q1 to Q4; not causal; the fit does not
  hold outside the table; designed grids are not independent observations); S8 stated.
- Wrong beliefs: none.
- Depth job: done, with whys owed that are defects (below).
- Findings that count:
  - defect: the main results cite "(Theorem 8, Theorem 9)" for weak Pareto efficiency; Theorem 8 is the posynomial
    extension (1). Check and cite the statements that state it.
  - defect: Table 1's geometric-programming row lists Candès et al. 2008 (reweighted l1) among its sources (2); verify
    the row against prior_art.yaml's intent and move or drop the citation.
  - defect: the Discussion's "It did not show that it places the position along the frontier (3 of 3)" against
    Section 9's position within the band for 3 of 3 with errors of 0.2 to 0.8 bands (27). The two sentences are
    generated from the same study; make them say one thing from the record.
  - defect: Works cited holds Ahmadi-Javid 2012, Hirshorn et al. 2017 and Parnell et al. 2021 with no citation in the
    main text (29); if they are cited only in the supporting material the shared bibliography is right and the paper
    says nothing; if not, they are stale. Check.
  - counted already: the thresholds (4), "the case needs three terms" (5), Definition 3 (6), "five metrics" (26),
    "certified" (13), "Derived" and "machine-checked" (11, 28), Theorem 11's strictness (12), Theorem 12's sign (15).
  - friction, two cells: the regressor's band 0.0935 never introduced (22; F25 (20)). Counts.
  - friction, three cells: Figure 5's dark points scatter about a log unit around the line while the caption says
    "within 0.1 in log V" (20; G08 (9), G21). Counts: the caption must say that 0.1 is the selection of the dark
    designs by their other metrics, and that the vertical axis is the conditioned metric's log, not log V.
  - friction, one cell: elasticity read across stepped metrics (23), a real conceptual point; logged for the supervisor
    with the Section 9 sentence quoted.
  - friction, one cell: "R1 holds on both regimes: the exact-maximum optimum is one point" asserted (19); the
    sentence can say "checked (D.n)". Logged; one word if the unit passes.
  - the ridge's tau-squared (8): the source has tau/2; the page text extraction loses the fraction bar. Not a defect;
    noted in the README's incidents.

## F04 (P4-A, wording 1, Sonnet)

- Key marks: S1 stated (an organizational framing noticed as such); S2 stated (surface as a model of the data, the
  chart as an invertible transform, terms with elasticities, composes with PCA); supports a trade study stated; the
  finding stated; wants to read on, for the API.
- Wrong beliefs: none; W4 avoided.
- Depth job: done.
- Findings: the abstract's phrases (the same set; four cells); "Scaling" in the title read as computational scale
  (one cell; logged for the supervisor beside the title word); no package named in the abstract (one cell; the
  keywords say open source; logged).

## G21 (P10-B, wording 2, Haiku)

- Key marks: S4, S5's three levels, S6 (Figure 8's examples), S8 all stated correctly; the chart as reversible stated.
- Wrong beliefs: none.
- Depth job: done.
- Findings that count: Figure 1's rule for a term's face against Definition 6's support (G27 (13): two cells); Figure
  3's settling time (four cells now); Figure 5 (three cells); the "Numerical" tag (three cells); Definition 1's table
  (two cells); Definition 3 (four cells); f_k's scope (three cells); Theorem 12's sign (four cells with G14, G27, F12);
  the duplicate (L14) label (three cells); "support" in three senses (G27: two cells); Table 2's "executives'
  measures" (three cells). Logged: Lemma 2 without a level label (one cell); Figure 6's "inside" and the direction
  for cost metrics (one cell; the caption says "better"); "Lemma 2" and "2-lemma" in one paragraph (vocabulary, for the
  supervisor; four cells of preference now).

## Roll-up, wave 2

| Cell | Report | Model | Key marks | Wrong beliefs | Depth job | Counting findings |
|---|---|---|---|---|---|---|
| P2-B | G02 | Haiku | correct | none | done | 6 replicated frictions, 2 defects (tag, "local") |
| P6-A | F19 | Haiku | correct | none | done | 0 (abstract, to the supervisor) |
| P1-ROOT | H01 | Sonnet | correct | none | done | 0 applied (root page, to the supervisor, 4 items replicated) |
| P5-C | F12 | Haiku | correct | none | done, whys owed | 4 defects, 2 replicated frictions |
| P8-ROOT | H02 | Haiku | correct | none | done | as H01 |
| P4-A | F04 | Sonnet | correct | none | done | 0 (abstract, to the supervisor) |
| P10-B | G21 | Haiku | correct | none | done | 7 replicated frictions |

No wrong belief in fourteen reports so far. Every depth's job done. The replication across cells is now the signal:
the same ten or so places in the paper's statements and captions stop readers of every persona.

## Change requests added at wave 2 (numbered after wave 1's 31; the same unit if it has not landed, else a second)

32. Main results: the "(Section 9; Numerical)" tag names no heading; cite the section and, if the taxonomy word is
    wanted, say "a numerical result".
33. Main results: "a soft fit has a second-order certificate" becomes "a second-order certificate of a strict local
    minimizer", as Theorem 12 states.
34. Main results: the weak-Pareto-efficiency line cites Theorem 8 and Theorem 9; cite the statements that state it
    (Theorem 9, and Theorem 8 only if its text carries the K > 1 efficiency clause).
35. Definition 1: "which none of the table's designs exceeds" names the design table, not Table 1 or Table 2; say
    "none of the design table's rows".
36. Figure 5's caption: say that the dark designs are selected by their other eleven metrics lying within 0.1 (in log
    V) of the median, that the vertical axis is the log of the conditioned metric, and that the scatter around the
    line is therefore not the band; if the sentence "reach the line and stop there" cannot be read off the figure,
    the figure-review rule applies (shows and does not show).
37. Figure 1's caption: state the rule that places a term's point on a face (the exact-maximum support with its
    threshold) and reconcile it with Definition 6, so the figure and the definition read the n-lemma the same way.
38. Table 2's caption: gloss "the executives' measures" as the operator's pointing error and the sponsor's unit cost
    and fleet cost.
39. Proposition 3 and Corollary 2 both carry "(L14)"; distinguish the labels (the shared script's step ranges) in the
    main text as the appendix does.
40. Theorem 12: one clause on why kappa M enters with a minus sign (the designs' ambiguity between terms lowers the
    curvature), or a pointer to the step that shows it.
41. Figure 6's caption: say that the position axis is the first principal direction of the K = 1 near-frontier chart
    (D.16) under the K = 2 level, and that "inside" is V < 1.
42. Figure 7's caption or the text beside it: one clause on near-collinear metrics (the one-axis pairs are read
    summed, D.3), since a reader of the correlation panels asks what the fit does with them.
43. The Discussion's propose-predict-check sentence against Section 9's: make them say one thing from the record (the
    position within the band for 3 of 3 with errors of 0.2 to 0.8 bands, or whatever the study says).
44. Works cited against citations: Ahmadi-Javid 2012, Hirshorn et al. 2017, Parnell et al. 2021; verify each is cited
    somewhere in the paper or the supporting material, else retire.
45. Table 1's geometric-programming row: verify the Candès et al. 2008 citation's place against prior_art.yaml and
    move or drop it.
46. Section 9: "the exact-maximum optimum is one point" gains "(checked, D.n)" with the record that checks it.
47. The regressor's band (1/tau = 0.0935) in propose-predict-check: say whose tau it is where it is first used.

For the supervisor (entry surfaces and his own text; not applied here):
- The root page's summary paragraph stops both executives at "posynomial invariant form", "invariant" and
  "unsupervised" (H01, H02). A plainer sentence is possible: "A method that learns, from a table of evaluated designs,
  which of their qualities trade against which, and at what rate." His call.
- "The alternatives are bespoke or opaque" (root page Why): both ask which alternatives.
- The root figure's caption: "exponent vector", "frontier", "reference surface" and "favours metric 1" are opaque to
  both executives; the dots' sizes are not visible at that scale; the first screen cuts the triangle.
- The abstract's phrases, now four cells (G26, F19, F04, F03): "We explain tensions" before the term; "the data
  underlying the table"; "soft support"; "reversible chart"; "GGP" and "kernel"; "a few" unquantified.
- The title: "Scaling" read as computational scale (F04); "hyperbolic" names the two-metric case (F03, F25, F12).
- The n-lemma name beside "Lemma 1" and "2-lemma" (F11, G14, G27, F12, G21): a vocabulary ruling.
- Section 9's elasticity read across stepped metrics (F12 (23)): whether the sentence should say the rate is read
  across the swapped parts' alternatives and is not a derivative.

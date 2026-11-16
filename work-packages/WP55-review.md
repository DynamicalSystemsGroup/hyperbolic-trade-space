# WP55 review: the mathematics builds up (Section 3's fitting problem, Sections 4 to 6)

Head before: `c98044d` (dev, WP54 landed). Branch `wp55`. Written by the executing unit; the driver's soft-confirm
is on screenshots of the rendered page (the anchors are at the end).

## Words before (WP54 head), measured by `tests/test_paper.py::words_by_section`

| Section | Before | Ceiling before |
|---|---|---|
| 3 Preliminaries and notation | 364 | 642 |
| 4 Definitions | 1256 | 1256 |
| 5 Methods | 892 | 892 |
| 6 Results | 3789 | 3789 |
| Sections 3 to 6 | 6301 | 6579 |

## Words after

| Section | After | Ceiling after |
|---|---|---|
| 3 Preliminaries and notation | 511 | 642 |
| 4 Definitions | 1061 | 1061 |
| 5 Methods | 1174 | 1414 |
| 6 Results | 2936 | 2936 |
| Sections 3 to 6 | 5682 | 6053 |

R-4 met: 5922 against 6301 (379 fewer). Methods grew by 522, the algorithm and the thresholds having moved in;
Results shrank by 853 and Definitions by 195.

## The argument, before and after

Each row: the object, its hypotheses, its conclusion in one line, the proof pointer. The after column is filled
in when the edit is done ("unchanged", or the change and its justification).

### Definitions (Section 4 before; Section 3 where noted)

| Label | Before: statement | After |
|---|---|---|
| (S3) V | V(m;w,β)=e^{-β}∏ m_j^{w_j}, log V = w·u−β; no type | changed: V gains its type V : R^d_{>0} -> R_{>0} and the power-law shorthand m^w = prod m_j^{w_j}; the formula is the same (power-law notation, Hoburg and Abbeel II; BV 1.6) |
| (S3) fit | θ* ∈ argmin J(θ;U) over Θ; no template, β not named as an optimal value | changed: problem (1) displayed and numbered, minimize J_tau(w) = lme_tau(Uw) subject to w >= 0, 1^T w = 1, variable w in R^d; beta named its optimal value J_tau(w*) (BV 4.1.1); the general argmin sentence, loss and objective sentences kept; A1 to A3 stated as plain sentences; the sentence pointing to Methods for J and Theta dropped (a forward reference, R-2). The feasible set and the loss are what they were |
| def-objects | the fitted reference surface: level set V=1 at the fit temperature τ | unchanged (verbatim) |
| def-envelope | the supporting envelope: surface of the exact-maximum fit (τ=∞) | unchanged (verbatim) |
| def-pareto-boundary | the Pareto boundary: nondominated set of the attainable set | unchanged (verbatim) |
| def-invariant | V(m)=e^{-β}∏ m_j^{w_j}, w∈Δ, reach β | unchanged in meaning; the reach is now the optimal value of (1) of Section 3, so the definition no longer refers forward to the reach definition; V(m) = e^{-beta} m^w in the shorthand |
| def-posynomial | V_K=(Σ_k e^{-κβ_k}∏ m_j^{κ w_kj})^{1/κ}; Φ_K=log V_K; cell of a term; package mean subtracts (log K)/κ; fits of record sharp | unchanged in meaning; bridge sentence to the GP tutorial added (c_k = e^{-kappa beta_k}, a_k = kappa w_k, Section 2.1); the definition points to Appendix B, L10 instead of thm-extension (R-2); the package's mean aggregation and the sharp fits of record moved to Methods (convention, not definition) |
| def-temperature | τ>0 fit temperature, κ>0 term temperature, band \|log V\|<1/τ; within-factor-e weight bound (L5.25) | unchanged; the within-factor-e bound on the band (L5.25) and the strict-band note moved to Methods, the temperature rule where the reason for the band lives |
| def-chart | Z=Bu, B (d−1)×d, BB^T=I, B1=0; chart (Z, log V) | unchanged (one prose sentence before it) |
| def-nlemma | contending set of term k: support (>1e-9) of the τ=∞ fit to its cell, centred; size ν_k; jitter check; tie; three thresholds; reading | split: Definition (the contending set, its size names the n-lemma, found not assumed) and one reading sentence after the figure; the 1e-9, 1e-12 and 1e-3 thresholds, the jitter check, G-10 and the solver's tie-breaking moved to Methods (Thresholds and ties); no meaning changes: the same set read at the same fits |
| def-reach | reach β_k: soft maximum of scores along w_k; term share; terms numbered by share | unchanged in meaning (reach soft maximum of scores along w_k; term share the fraction of near-frontier designs in the cell, depends on the band); placed after the band so it refers back only; the numbering of terms by share moved to Methods (Thresholds and ties) |
| def-exchange | elasticity d log m_j / d log m_i = −w_ki/w_kj | unchanged (verbatim) |
| def-tension | T_ij = dm_j/dm_i = −(w_ki/w_kj)(m_j/m_i), cases, T_ij T_ji=1, matrix per term, balanced point, attribute units | unchanged in meaning; split into shorter sentences; the attribute-unit formula and the forward references to L21, L9, L1 and to Methods removed (the formula stays in L21); the limit that a tension is a rate along the surface kept once here |
| def-ascent | tangent space {v: w_k·v=0}; normal w_k the ascent direction = gradient of log V in u | unchanged (verbatim) |

### Assumptions and conditions (Section 5 list before)

| Code | Before: statement | After |
|---|---|---|
| A1 | metrics strictly positive | unchanged; plain sentence in Section 3 (assumed throughout) |
| A2 | exponents on the simplex | unchanged; plain sentence in Section 3 |
| A3 | τ>0 (finite; τ=∞ the exact limit) | unchanged; plain sentence in Section 3; tau = infinity the limit named where used |
| A4 | conditioning log-affine and invertible | unchanged; displayed block "A4, log-affine conditioning" in Methods, Conditioning (stage 2) |
| A5 | noise, where used, independent N(0,σ²) in log space | unchanged; displayed block "A5, independent noise" in Results, before L6 |
| A6 | κ>0 and each term's exponents on the simplex | unchanged; displayed block "A6, terms on the simplex" in Methods, Several terms; the finite/limit remark carried in the block |
| A7 | chart basis orthonormal, sums to zero | unchanged; displayed block "A7, orthonormal chart basis" in Results, before L8; the chart definition keeps B's two conditions |
| A8 | rows split into nonempty cells, one per term | unchanged; displayed block "A8, cells" in Methods, Several terms; the argmax-cell identification for a sharp fit stays a sentence there and in L14's statement |
| A9 | each row's noise Gaussian, mean zero, one covariance Σ | unchanged; displayed block "A9, row noise" in Results, before L20 |
| A10 | attribute measurement error multiplicative, log-normal, independent; L18 maps it to A9's noise | unchanged; displayed block "A10" in Results, before L20 (no result of the paper uses it; it maps an attribute's error to A9's noise, Appendix B L18) |
| A11 | noise a row's weighted metrics carry independent across rows, N(0,v²), v>0; L19 uses it | unchanged; displayed block "A11" in Results, before L20 (used by Appendix B L19 only) |
| R1 | at the τ=∞ fit, the balanced point lies in the relative interior of a facet of the hull with positive normal; components of U^T p on the support of w equal | unchanged; displayed condition "R1, a positive facet normal" in Results, before L3; the positive-exponent reading of L7 cites it there |
| R2 | (K≥2) assignment margin γ>0 | unchanged; displayed condition "R2, a positive assignment margin" in Results, before L13 |
| R3 | at the clean fit zero exponents have gradient strictly above the common value; C positive definite on the sum-zero vectors vanishing where w does | unchanged; displayed condition "R3, a positive definite covariance" in Results, before L20 |

### Results (Section 6 before)

| Label | Lemma | Hypotheses | Conclusion (one line) | Proof pointer | After |
|---|---|---|---|---|---|
| thm-invariant | L1 | A1, A2 | V(λm)=λV(m); V(m/V(m))=1; V(m e^{-β})=e^{-β}V(m) | lemma_01_homogeneity.py | unchanged in content; "Let ... Assume ... Then" with one display; sketch and script box out; "Proof: Appendix B, L1"; one interpretation sentence |
| prop-shift | L2 | A1, A2, A3 | J_τ(w;U+c)=J_τ(w;U)+c; β moves by c, minimizers unchanged | lemma_02_shift.py | unchanged in content; the interpretation says the shift is a change of units (multiplying every metric by e^c), which the statement implies |
| thm-kkt | L3 | A2, A3; w minimizes J_τ on Δ; for the facet-normal reading w_j>0 at the fit temperature | ∇J_τ=U^T p; g_j≥λ, w_j(g_j−λ)=0; equal components of U^T p on the support | lemma_03_gradient_kkt.py | unchanged in content; hypotheses in one Assume sentence (the facet-normal clause now inside it); BV 4.2.3 (minimization over the probability simplex) cited; R1 does not imply an interior minimizer, said once |
| thm-convex | L4 | A1, A3 | d²/dt² J_τ(w+tv)=τ Var_p(v·u)≥0; J_τ convex, not strictly | lemma_04_convexity.py | unchanged in content; BV 3.1.5 and 3.2.2 cited (log-sum-exp convex, preserved by affine maps) |
| thm-lme | L5 | A3 | LSE=LME+(log N)/τ; mean ≤ LME ≤ max; LME ≥ max−(log N)/τ; limits | lemma_05_lse_lme.py | unchanged in content; chain of bounds as one display (the lower bound LME >= max - (log N)/tau written as max <= LME + (log N)/tau); BV 3.1.5 cited |
| prop-cumulant | L6 | A2, A3, A5, I5 | (1/τ) log E e^{τ w·ε} = τσ²‖w‖²/2 | lemma_06_gaussian_cumulant.py | unchanged in content; A5 displayed before it |
| cor-noise-ridge | L20 | A1, A3, R3, A9 (A5 a case), noise small | J^R=J_τ+(τ/2) w^TΣw; exponent shift δ=−(PCP)^+PΣw | lemma_20_noise_ridge.py | unchanged in content; the definitions of C and P move into the Let; the sketch leaves (Appendix B keeps it); A9 and R3 displayed before it |
| thm-elasticity | L7 | A1, A2; K=1; w_j>0 | d log m_j/d log m_i=−w_i/w_j; improvement factors V^{-1/w_j}, 1/V | lemma_07_elasticities.py | unchanged in content; BV 4.5.3 cited; the small-exponent limit (about 190) and the R1 and L3 conditions stated once in the interpretation |
| thm-tension | L21 | A1, A4; term hyperplane; sign hypotheses | dm_j/dm_i=−(w_ki/w_kj)(m_j/m_i); attribute-unit form; same at a design's own ratios | lemma_21_tension.py | unchanged in content; the attribute-unit formula now displayed beside the metrics formula; the sign and the seam limits kept once |
| thm-chart | L8 | A2, A7, I6; K>1: A6 | Z(u+c1)=Z(u); u=B^T Z+ℓ1; (Z, log V) a bijection | lemma_08_helmert_chart.py | unchanged in content; the L10 reference becomes a pointer to Appendix B, L10 (R-2: L10 follows); A7 displayed before it |
| thm-pullback | L9 | A2, A4 | V=e^{w·b−β}∏(a_j+s_j)^{w_j α_j}; conditioning invertible | lemma_09_pullback.py | unchanged in content; GP tutorial 2.1 cited |
| thm-extension | L10 | A1, A6, I15 | Φ_K shift-equivariant; max s_k ≤ Φ_K ≤ max s_k+(log K)/κ; posynomial; κ=∞ the maximum | lemma_10_extension.py | unchanged in content; the pointer to Methods for the class name dropped; BV 3.1.5 and 4.5.3 cited |
| thm-pareto | L11 | A2 | a maximizer of V is weakly efficient; efficient when all w_j>0; same for Φ_K at κ=∞ | lemma_11_pareto.py | unchanged in content; the converse stated as not claimed once, here; BV 4.7.4 cited |
| thm-soft | L16 | A1, A2, A3, A6, I14, I15 | F symmetric not convex; F ≤ G_α−E, equality at own weights; e^{G_α} a generalized posynomial | lemma_16_soft_fit_alternation.py | unchanged in content; the display F(W) <= G_alpha(W) - E; BV 3.1.8 cited; its algorithm text moved to Methods |
| thm-descent | L15 | A8; exact refits; unique minimizers, fixed tie rule | one accepted iteration does not raise F; finite stop (≤K^N+1) | lemma_15_descent.py | unchanged in content; the pigeonhole bound and the cap-reaching fits, and the empty-cell rule, in the interpretation |
| lem-gap | L12 | A2, A3, I8, f_k convex | 0≤f_k−f_k*≤G_k (Frank-Wolfe gap); G_k=0 iff KKT | lemma_12_term_gap.py | unchanged in content; BV 3.1.3 cited |
| lem-margin | L13 | R2, I9 | score changes ≤δ with 2δ<γ keep the maximizing term; stable radius r=γ/(2 max‖(u_i,−1)‖) | lemma_13_margin.py | unchanged in content; R2 displayed before it |
| prop-local | L14 | A8 (argmax cells), R2, w_k minimize f_k | within r with cells fixed, F(W')−F(W)≥0: local minimizer | lemma_14_assignment_stable.py | unchanged in content |
| cor-bound | L14 | A8, w_k∈Δ, cells fixed, G_k | 0≤F(W)−F*_fixed≤Σ(n_k/N)G_k | lemma_14_assignment_stable.py | unchanged in content |
| thm-certificate | L17 | A1, A2, A3, A6, I16; finite τ, κ; exact KKT | Hessian D−κM PD on the active face's tangent space implies a strict local minimizer | lemma_17_soft_fit_certificate.py | unchanged in content; Nocedal and Wright, Theorem 12.6 cited; the sketch's finite-difference remark left to Appendix B |
| Open questions | none | Q1 global convergence, Q2 consistency under noise, Q3 identifiability, Q4 recovery of the Pareto boundary | open (gaps G-14, G-11, G-12, G-13) | none | moved to work-packages/review/open-questions.md, OQ-5 to OQ-8; Results keeps one pointer to Appendix E |

## What left (negative edits, each with what it no longer did)

| Content | What it no longer did |
|---|---|
| The Derived label, the Hypotheses label, the sketch and the Script box of every result (20 blocks) | Stated each result twice and pointed at the script a second time; the proof, its steps and the script are Appendix B's ("Proof: Appendix B, Ln" now ends each statement) |
| The five one-sentence previews before result groups (L3 to L5, L8 and L9, L10 and L11, the levels, L17) | Said in a sentence what the next blocks state |
| The Results preamble (Derived, Numerical, Open and the hypothesis-code legend) | Explained badges the section no longer carries; "Hypotheses marked I" is the one key kept |
| "Whether the hypotheses suit a table is a human judgment (Section 9)" | A forward reference to Discussion, which states it |
| The subsection "Open questions" (Q1 to Q4) | Held what is not established; now OQ-5 to OQ-8 of `work-packages/review/open-questions.md`; Results ends with one pointer to Appendix E |
| The assumptions paragraph and the conditions paragraph of Methods | Listed A1 to A11 and R1 to R3 before any result used them; each is now displayed where used (A1 to A3 in Section 3) |
| The forward references of Sections 3 to 5 (numref to Methods and Results, prf:ref to results, "(gap G-10)" kept) | Pointed to material not yet given; they point back or to Appendix B |
| The n-lemma definition's thresholds, jitter check, tie-breaking | Convention and solver behaviour inside a definition; now Methods, "Thresholds and ties" |
| The attribute-unit tension formula in the Tension definition | Repeated L21's display |

## The three sections' claim, evidence and hand-off (for the soft-confirm)

- **Section 3 (the fitting problem).** Claim: the one-term fit is the displayed problem (4), minimize the soft maximum of the
  scores over the simplex, with the reach its optimal value; the log change of variables makes the scores linear in the
  exponents. Evidence: the problem's convexity (Appendix B, L4). Hand-off: Section 4 names the objects of the fit.
- **Section 4 (Definitions).** Claim: every object (surface, envelope, boundary, invariant value, posynomial, temperatures,
  reach and share, chart, n-lemma, elasticity, tension, ascent direction) is one term per sentence, prose first, from
  Section 3's symbols, with the tutorial's c_k and a_k as the bridge. Evidence: the definitions are statements, backed by
  the lemmas they point to in Appendix B. Hand-off: Section 5 says how the objects are found.
- **Section 5 (Methods).** Claim: the one-term fit is a convex program (a geometric program at finite temperature), the
  several-term fit is a heuristic with three levels of guarantee. Evidence: Appendix B, L4.14 to L4.24, L15, L12 to L14,
  L17, and the planted-term refit comparison (Appendix D.13). Hand-off: Section 6 states what is proved.
- **Section 6 (Results).** Claim: twenty results, each in "Let, Assume, Then" with its lemma and its assumptions. Evidence:
  Appendix B (the proofs and scripts); the register rows. Hand-off: Section 7 builds the case the results are applied to.

## The symbol table

Drafted (N and d: `n_samples`, `n_features`; M and U: the table and its logarithm; w, beta: exponents, reach; V: the
invariant value; tau, kappa, K: `temperature`, `term_temperature`, `n_terms`; J: `loss_`; Delta), twelve rows, and not
kept. In the rendered Section 3 each symbol is defined in the paragraph where it enters, five short paragraphs on one
screen; a table after them restates those paragraphs and reads as a small Appendix A, and the one column that is new,
the code names, is carried by one sentence ending the estimator paragraph of Methods. This is a negative edit: the
table did not earn its place.

## Where the lineage's form and his differed, and the choice

- Results: the textbook's "Suppose ... Then" against his "Let ... Assume ... Then": his (the scope's default).
- The assumption blocks carry MyST's `prf:assumption`; the builder numbers them in order of appearance, which would print
  "Assumption 1" for A4. They are `:enumerated: false` and carry their code in the title, "Assumption (A4, log-affine
  conditioning)", so the lemma scripts' A and R codes stay the names.
- The heuristic is a `prf:algorithm` (numbered "Algorithm 1"), the builder's kind for a procedure; Magnani and Boyd number
  the alternation and call it a heuristic.
- The builder numbers every display equation, so the template of Section 3 prints as (4), not (1); references are by
  label ({eq}), so they follow.
- BV's note that notation is explained in prose (1.6) and his "Notation" paragraph agree; Section 3 is his text plus the
  template; the one sentence that pointed forward to Methods for J and Theta is gone (R-2).

## Follow-through

- **Register** (`claims_register.toml`): 44 rows retired (C004 C007 C012 C014 C015 C017 C018 C019 C020 C021 C023 C038 C092
  C099 C386 C416 C417 C418 C421 C460 C464 C465 C466 C467 C473 C640 C641 C642 C643 C648 C649 C650 C651 C652 C653 C654 C655
  C657 C658 C660 C664 C802 C803 C851), 39 added (C922 to C960; each names its retired id and keeps its backing); six rows
  keep their id and change anchor (C022, C419, C420, C639, C665, C795), because the sentence moved to Methods or Results
  unchanged. Retired without a successor, the claim being a sketch sentence that is Appendix B's: C015, C017, C460, C651,
  C657, C803.
- **Paper tests** (`tests/test_paper.py`): the lemma-block test now reads "Let, Assume, Then" with the proof pointer; the
  badge test became the assumptions-and-conditions test, the open-questions test and a forward-reference test (R-2); the
  count of words does not count a labelled display; the citation locators are not read as versions or typed references;
  pins that moved with the sentence (thresholds, band bound, numbering rule, own-rows refit, sharp fits of record, A9's
  independence clause, R1) follow it; the F labels and I4 left the cr12 test with the sketches.
- **Appendix B generator** (`paper/generate_proofs.py`): the hypotheses line of a lemma with no declared hypotheses was
  read from the paper's "Derived. Hypotheses." line; it now reads the "Assume ..." sentence. The Appendix B text for those
  lemmas changed in wording only (the supporting notebook re-executed). The supporting notebook's cells were not edited.
- **Length ledger**: Results cut 853, Definitions cut 195, Methods raised 522 (the algorithm and the thresholds moved in);
  Section 3 is below its ceiling without a row.
- **Vocabulary baseline**: one stale row removed (the "row gap" of the deleted L13 sketch); no row added.

## Checks (head of the branch)

| Check | Result |
|---|---|
| `uv run --frozen python paper/execute_notebooks.py` | both notebooks re-executed (the supporting notebook's Appendix B hypotheses lines follow the generator change); no cell of the supporting notebook edited |
| `uv run --frozen python derivation/run.py` | ALL LEMMAS PASS |
| `uv run --frozen python -m derivation.proofmap` | PROOF MAP OK: 22 lemma files, 549 tagged steps (unchanged); nothing under `derivation/` changed |
| `myst build --html` in `paper/` | no missing label, figure or cross-reference warning; the one remaining warning, a duplicate identifier `fig-tension-matrix` (a code cell and a figure label of Section 8), is at the previous head |
| `mkdocs build -q` | exit 0 |
| `scripts/check_residuals.py` | exit 0 |
| `scripts/check_vocabulary.py` | 0 new violations, 66 known; one stale baseline row removed |
| `ruff check .`, `ruff format .`, `uv lock --check` | clean |
| fast suite, `pytest -q -m "not slow"` | 2086 passed, 17 skipped, 2 xfailed; the one failure of the run (a ledger ceiling, Results 2936 against 2930) was fixed by the ledger row and re-run green |
| slow paper tests, `pytest -q -m slow tests/test_paper.py` | 27 passed |
| R-2, references in Sections 3 to 6 against the order of labels | all point back (`test_no_section_3_to_6_reference_points_forward`); the one exception is his sentence in Section 3, "{numref} fig-pipeline", whose figure is the next cell |
| R-3, `open`, `not established`, `conjecture` in Sections 3 to 6 | one hit, the pointer "Appendix E records what the results leave open" |
| R-5 | as the two rows above |

## Anchors for the driver's screenshots (G6)

The built paper is served at `http://127.0.0.1:8815/paper/index.html` (port 8795 is held by a server started on
2026-11-14 for `pm-worktrees/wp41/_stage`, left alone; port 8796 by another session's). Desktop width, the first three
depths:

- `#sect-notation` (Section 3: the fitting problem is the last paragraph; the template is the fourth numbered display),
- `#sect-definitions` (Section 4), and `#fig-nlemma` (Figure 3, the n-lemma: the figure, then with its caption, then with
  the reading sentence and Definition 11 below it),
- `#sect-methods` (Section 5: the assumption block A4, the thresholds, the assumption block A6, Algorithm 1),
- `#sect-results` (Section 6: R1, Theorem 2 with its interpretation paragraph, then down to the levels of guarantee).

## Section 5 revision pass (coordinator's review of the rendered page)

Methods 1414 words before the pass, 1174 after (the ceiling stays at 1414; Sections 3 to 6 together 5682 against 6301
at the WP54 head). Cut or moved, against "results restated, caveats about what is not proved, one point per place":

- the pointer "Appendix B, supporting material, L4.14 to L4.24" is "Appendix B, L4"; "(10 percent here)" and the
  closed-versus-strict band clause are gone;
- the Conditioning paragraph lost the note on the scripts' letters, the zero-metric sentences, the case-has-none sentence
  and the pointer to the documentation; "not a context-free discovery" is a plain statement;
- "(gap G-10)" left the text (OQ-9 of `work-packages/review/open-questions.md` carries the tie rule); the tie is
  resolved "by the fixed tie rule";
- the planted-term recovery numbers left Methods (a result, in Appendix D.13); one sentence says the refit of record is
  f_k over all rows centred at the cell's mean and that refitting on a cell's rows alone does not recover planted terms;
- "none global" is said once, in the heuristic's sentence "carries no global guarantee";
- "Simplifying assumptions" and its heading are gone: (i) and (v) restated A4 and the one-term fit; (ii) is one clause
  and the L10 bound in the paragraph after Algorithm 1; (iii) is one sentence beside "Several terms"; (vi) is OQ-10;
  (iv) is the case's and is cut.

**For WP56:** the case's K = 2, the package's checks pointing to it (Appendix D.15), that K = 3 is certified too and adds a
thin term, and that a small K keeps each contending set readable, were in item (iv) of Section 5; Section 8 may carry
them. The "fits of record, every K = 2 figure included, are sharp" sentence is also cut; Section 8 says which fit it reads.
Figure 3's caption still has the Shows, Does not show and Good for lines (WP56's figure unit).

Register: retired C042, C098, C105, C106, C419, C622, C924, C928, C929, C934, C958; added C961 to C966.

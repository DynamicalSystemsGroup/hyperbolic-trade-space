# WP29 review: acceptance package for the supervisor

Screenshots for this record: commit `2a669de`, `git show 2a669de:<path>` with `<path>` under `work-packages/WP29-review/`, `work-packages/WP29-review/reads2/shots/`.

Stage 6 of `WP29-scope-of-work.md`. Head read: dev at d7ac579. Nothing here is accepted; the acceptance is the supervisor's.

## 1. What landed

| Hash | What |
|---|---|
| 8b5c4f4 | Corollary 1 (noise moves the exponents by a ridge, L20) placed between L6 and L7 in Section 6; D.18 injected-noise table; gaps G-3, G-11, G-12; glossary entries ridge and active face; register C459 to C463 |
| 3f8c49b | The narrowings of the P9 and P10 triage applied to Sections 3 to 6: Corollary 1 to interior fits and the expected noisy objective, weak efficiency, Corollary 2 hypotheses, R1 and R3, symbols defined, margin sentence in score units, Appendix B quotes the boxes' hypotheses; ledger rows; register C464 to C467 |
| d7ac579 | L20 face step: the shift on the support under strict complementarity (steps L20.52 to L20.63); R3 and Corollary 1 state P as the projector onto the sum-zero vectors that vanish where w does; D.18 text and outputs; G-12; register C465 and C473 |
| this unit | the second reads, `WP29-review/reads2/` (briefs, returns, shots) |

## 2. Claims and backing (Corollary 1 as it now stands)

| Claim in the box | Backing |
|---|---|
| noise of covariance Sigma adds the ridge (tau/2) w'Sigma w to J_tau | L20.2, L20.18 to L20.20 (with L18); exact for the log of the expected noisy sum, every real w |
| the exponents move to first order by -(PCP)^+ P Sigma w; equal case -sigma^2 (PCP)^+ P w | L20.35 to L20.43 (interior), L20.55 to L20.60 (face), L20.50, L20.51 |
| P projects onto the sum-zero vectors that vanish where w does; zero exponents stay zero | L20.55 to L20.58; L20.62, L20.63 |
| the shift is at most ||P Sigma w||/m, m the smallest eigenvalue of C on that space; lowers w'Sigma w | L20.44 to L20.49, L20.61 |
| it is the shift of the minimizer of the expected noisy objective, not of one noisy fit; not whether the rates are right | docstring limits; D.18 is the measured demonstration |

Checks run at the head in this worktree: `derivation/run.py` ALL LEMMAS PASS; `derivation.proofmap` OK, 20 lemma files, 505 tagged steps; `tests/test_noise_ridge.py` and `tests/test_paper.py` 186 passed, 4 skipped (95 s); the paper and supporting material build and stage (`scripts/stage_site.py`); the box rendered and looked at (`reads2/shots/cor-box-light.png`: box, sketch and script are separate, links to Proposition 2, Theorem 2 and Theorem 3 show, the hypotheses line carries A1, A3, A9, I9, I18, R3).

## 3. The reads (verbatim in `WP29-review/reads2/`; one reader per cell, no replicates)

- **d2, the check of the box against the script (the supervisor-approved narrowing).** Stated precisely and no hypothesis lost in the three named points:
  - Support/active face: exact. The script's P is the mean-subtracting map when every exponent is positive and P_T (sum-zero, zero off the support T) on the face, with R3's strict complementarity (gap off T positive, L20.62) and C positive definite on the tangent space. The box says "vanish where w does", "P = I - 11'/d when every exponent is positive".
  - Bound ||P Sigma w||/m: exact for the first-order shift (Euclidean norm; m a positive Rayleigh constant, the smallest eigenvalue being the sharpest). The face case rests on L20.61 referring back to L20.44 to L20.49 (not re-run for P_T).
  - Expected-noisy-objective minimiser: the object is J^R, the log of the expected noisy sum; the script computes the stationary point of the first-order model on the face and does not state that J^R is convex or that a minimiser exists.
  Residual mismatches, each a wording item: (i) "on the conditioned metrics" is noise on the log-metrics, the same Sigma in every row; (ii) "the fit" is the clean fit w*; (iii) "lowers" is first order (the shift's change of w'Sigma w is at most -2m||delta||^2, the exact change has a second-order term); (iv) "zero exponents stay zero" rests on a positive margin (L20.62, L20.63) taken as given, never computed from Sigma, C, w*; (v) A5 (sigma > 0) is used in the equal case and is not in the hypotheses line; (vi) "when the shift is not zero" (L20.48) is not printed; (vii) the sketch's "its gradient on the face vanishes" is the clean J_tau's, the noisy objective's is tau P Sigma w*; (viii) the Taylor step is not a numbered assertion; (ix) "noise small" is used by no step.
- **b2 (precision read of Sections 3 to 6 and Appendices, 49 requests).** On Corollary 1 (its request 27) it finds (a) to (g): the same points as d2 (log-metrics, clean minimizer, J^R is a log of an expectation, first order in Sigma, "lowers" first order, A5 missing, sketch gradient). Request 48: Appendix B's "Hypotheses (quoted from the statement)" lines for L11 to L13, L19, L20 carry step premises (for L20, "when the shift is not zero"), not the statement's hypotheses. Other requests are outside Corollary 1 and are logged, not decided here (A3 and A6 finite versus the infinity default, beta, V and the Definition 2 identity, kappa, Definition 6 and the n-lemma, R1, Theorem 4 notation, F convexity clause, L-numbers against page numbers, among others); the file is read as a list for the triage.
- **a2 (cold read of the box, P5 type).** Stated all nine claims correctly (ridge, shift, equal case, C and P, zero exponents, bound, lowers, expected noisy objective, no claim on the rates). It stopped at: the codes A1, A3, A9, I9, I18, R3 (only the glossed ones resolved); "conditioned metrics" (noise on m or log m); J_tau and tau not in the excerpt; whether the expectation is inside or outside the logarithm; whether C is positive definite on the range of P (R3 not visible); "the fit" clean or noisy; where Cauchy-Schwarz enters; what "verify" checks; Corollary 1 citing Theorems 2 and 3 and L18 while Proposition 2 is "the equal case". The image helped (box, sketch and script separated, Theorem and Proposition links visible).
- **c2 (novice, P10).** Corollary 1: "I followed the projection and the shape of the formula. I could not check the formula itself. Proof 7 helped." It did not name the box among its three first stops: R1 in Section 5, Definition 6 with the paragraph after Theorem 10, Theorem 12. Other stops: the letter codes (I-codes explained only where they occur), s and alpha with several meanings, result numbers per type against L-numbers, "verify", "the package's mean". Pictures cut boxes at page edges (a property of the tiles).

Against round one (`reads/`): in a1 the stops on "active face", the unexplained codes and the `conditioning_` in a bound are gone from the box's own stops (the box states P and m); the codes, the clean-fit and the expectation-inside-the-log questions remain, now as wording items (i) to (iii) above. Verdict: the box is now exact in its three narrowed points; nine wording items remain for the box, none needs a new hypothesis beyond A5 and the margin.

## 4. Word deltas

Body +201 words; Results net +129; the step in this unit +30 (as given by the supervisor's brief; the rendered pages carry them). This unit changed no paper text.

## 5. Items not done

R6, R18, T3, T4, S8, S16 and S17 (logged in `P9-P10-triage.md`), the S6 renaming, A0 (the glossary), and D.18's margin sentence, which uses the exponent and not the gradient gap (the reads' item (iv) is the same gap). Also open from this round: the nine wording items of section 3 and b2's other 48 requests, none of them triaged here.

## 6. Host re-execution status

Only the patched cells have been re-executed; the whole notebook is not re-executed. Full re-execution of the paper and supporting notebooks is at the WP30 gate.

## 7. Screenshots

- Box and neighbours: `work-packages/WP29-review/reads2/shots/cor-box-light.png`; dark and light of the box from the placement: `work-packages/WP29-review/cor-noise-ridge-light.png` and `cor-noise-ridge-dark.png` (at 8b5c4f4).
- Sections 3 to 6, 13 tiles: `work-packages/WP29-review/reads2/shots/p10-page-01.png` to `p10-page-13.png`.

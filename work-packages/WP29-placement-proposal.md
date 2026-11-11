# WP29 placement proposal (stage 5, prepared and not landed)

For the supervisor's glance. Nothing below is in the paper, the docs, the register, the ledger or `references.bib`; the
lemmas, tests and Appendix B tables are on branch `wp29` and not on `dev`. If he declines a statement, its lemma, test and
Appendix B table are deleted as one unit. Kept apart throughout: the **model** (the noise-free soft maximum), the **fit**
(the estimator on a finite noisy table), the **analysis** (what a reader concludes).

## The two statements, in words

1. **Noise enters through a covariance, and the conditioning is the map from a measurement error to the noise the fit
   sees (L18).** For Gaussian noise with covariance Sigma on the conditioned metrics, (1/tau) log E exp(tau w.eps) =
   tau w'Sigma w / 2; L6 is Sigma = sigma^2 I; for a diagonal Sigma the shift is tau Sum_j w_j^2 sigma_j^2 / 2. Under the
   log, orient, standardise conditioning, a multiplicative measurement error of log-size delta_j on attribute j is noise
   sigma_j = delta_j / s_j in the metric, s_j the log spread the conditioning divides by. One percent on total mass (spread
   0.066) is as large in the metric as twelve percent on settling time (spread 0.83).
2. **The shift of the soft maximum under noise is bounded, and the bound says when L6 can be read (L19).** For clean scores
   s_i and independent N(0, v^2) draws z_i (v^2 = sigma^2 ||w||^2, or w'Sigma w by L18),
   0 <= E LME_tau(s+z) - LME_tau(s) <= min(tau v^2 / 2, E max z), E max z <= v sqrt(2 log n); tau v^2 / 2 and
   v sqrt(2 log n) cross at tau* = 2 sqrt(2 log n) / v. **An upper bound that is not tight**: near equality with tau v^2 / 2
   in the small-tau regime, a factor of up to about 2.6 above the shift at tau = 200 in the planted cells (the L6 value alone,
   up to about 12). tau* is a rule of thumb. The lower bound is Delta >= 0 (the convexity of LME;
   the PM replaced the weaker mean(s) - LME(s), which is at most 0).

Proof sketches (each step is a tagged line of the script, Appendix B):

- L18: w.eps is a centred normal of variance q = w'Sigma w (the definition of a Gaussian vector, A9); the moment generating
  function at tau is exp(tau^2 q / 2) (sympy.stats); the diagonal case collapses the double sum by the Kronecker delta; the
  equal-level case is L6; the conditioning map applies A4 with a_j = 0 and the error model log rt_j = log r_j + zeta_j (A10)
  to get eps_j = alpha_j zeta_j exactly, variance alpha_j^2 delta_j^2, with s_j := 1/|alpha_j|.
- L19: lower: the tangent line with the softmax weights of the clean scores gives LME(s+z) - LME(s) >= Sum p_i z_i, and E z_i = 0; first upper: Jensen for the concave logarithm with the L6 moment
  generating function; second upper: exp(tau(s_i+z_i)) <= exp(tau s_i) exp(tau max z); the maximum: Jensen for exp and a
  sum bound give E max z <= log n / lam + lam v^2 / 2, minimised at lam = sqrt(2 log n) / v.

## Proposed placements (as text; the paper stream lands them on his word)

**P1. Corollary after L6 (paper, Results).** Statement: "With noise covariance Sigma in place of sigma^2 I, the cumulant
is tau w'Sigma w / 2 (L18); with a diagonal Sigma, tau Sum_j w_j^2 sigma_j^2 / 2. For a measurement error of log-size
delta_j on attribute j, the conditioned metric carries sigma_j = delta_j / s_j (log, orient, standardise conditioning).
The shift of the soft maximum under that noise lies between 0 and min(tau v^2 / 2, v sqrt(2 log n)) (L19); the
second bound is not tight, and tau* = 2 sqrt(2 log n) / v marks where L6 stops being the smaller." Script box: `L18`,
`L19`, Appendix B. Sentence on the sign: the soft maximum is the entropic risk with the risk-seeking sign (+tau); noise
raises the reference surface; a risk-averse reading is the (-tau) version, a different object, the analyst's choice (no
citation: it is a derivation from L6; see OD3 below).

**P2. The covariance form (notation, `docs/method.md`).** One paragraph and the symbols sigma_j, delta_j, s_j in
`notation.md`.

**P3. The case table (Appendix D, from `examples/adcs/noise_injection.py`).** Header text, verbatim: "The data of record
carry no noise of their own; they are deterministic simulator output. The noise is injected as a design choice of this
experiment: each raw attribute is multiplied by exp(delta z), z ~ N(0,1). What the table shows belongs to the fit and the
conditioning together, not to the model, and not to the system." Columns: delta (percent), sigma_j range, largest exponent
change, contending-set Jaccard, offset shift, L6 with sigma_j, L6 with one sigma. The script output (primary regime):

| delta (%) | largest exponent change | Jaccard | offset shift | L6, sigma_j | L6, one sigma |
|---|---|---|---|---|---|
| 0.5 | 0.013 | 0.94 | 0.013 | 0.014 | 0.001 |
| 2.0 | 0.085 | 0.82 | 0.101 | 0.227 | 0.018 |
| 5.0 | 0.293 | 0.71 | 0.174 | 1.416 | 0.111 |
| 10.0 | 0.307 | 0.68 | 0.199 | 5.665 | 0.444 |

Stock regime: Jaccard 0.98, 0.98, 0.93, 0.89 and largest exponent change 0.043, 0.103, 0.136, 0.150 at the same four levels.
Claims the table licenses (and no more): the contending set is stable under measurement error of half a percent and
degrades as the error grows, faster in the primary regime where total mass (exponent 0.358, spread 0.066) drives the
change; L6 with the per-metric sigma_j tracks the offset shift where tau w'Sigma w / 2 is below the max bound (primary
0.5 percent) and overshoots beyond it, as L19 says it may. The spike's sentence that the one-sigma reading is "off by 10 to
20 times everywhere" is **dropped**: at the larger levels the one-sigma value is nearer the shift than the diagonal one
(primary 10 percent: shift 0.199, diagonal 5.665, one sigma 0.444).

**P4. Gap rows.** G-3 (offset shift against L6): add that the equal-noise reading is replaced by Sigma (L18), that M1's
single tau is read against L19's crossover (to be computed for M1's tau and sigma before the sentence is written), and keep "population quantity approached with N". G-12
(identifiability): add the injected-noise reading, in the words of P3, under "what it does not show": a metric's presence
in the contending set is a property of the sample, the conditioning and the noise together. Also proposed, the held A2 row
(new): "Noise on the metrics is a ridge on the exponents; tested by spike (`check2_noise_is_ridge.py`: first-order formula
within 3e-4 of the ridge minimiser; the noisy fit tracks it at small tau); no lemma; the effect is small where the problem
is well conditioned (largest bias 0.006)".

**P5. Register rows (one per new claim).** C-a: the covariance cumulant (backed: L18.11 to L18.14, test
`test_L18_cumulant_is_tau_wSw_over_2_on_planted_noise`); C-b: sigma_j = delta_j / s_j under log-affine conditioning
(L18.18 to L18.20, `test_L18_conditioning_maps_log_error_to_sigma_j_equal_delta_over_spread`); C-c: the shift sandwich and
E max z bound (L19, `test_L19_sandwich_and_the_max_bound_hold_on_planted_cells`); C-d: not tight
(`test_L19_the_bound_is_not_tight`); C-e: the injection table (script, `noise_injection.py`). The rows G-3 and G-12 touch
are re-read.

**P6. Citation (OD3).** The entropic-risk source (Foellmer and Knispel) was not opened in full: its publisher page returned
403 and two other routes found nothing. Fallback (b): no citation; the sentence is a derivation from L6 and says so.
Nothing enters `references.bib`.

## What a reader may conclude, and may not

May: the offset shift under Gaussian noise is at most min(tau v^2 / 2, v sqrt(2 log n)); the L6 value is the right size when
tau is well below tau*; the per-attribute error that the fit sees is delta_j / s_j. May not: that the shift equals the
bound; that the cubesat is noisy; that the fitted exponents move by the shift (the offset does not determine them); that the
result holds for other scalers, a_j != 0, non-Gaussian or non-independent noise, or weights fitted on the noisy table
(L18 and L19 say so in their "does not prove" lists).

## Cascade (for the paper stream after his word; not done)

Lemma count (17 to 19) in paper, docs, `tests/test_build_generated.py` (already 19 on the branch); Appendix B part heading
for L18 and L19 (`PARTS` in `paper/generate_proofs.py`); length ledger raise; register rows P5; `notation.md`; Appendix D
cell and the contract key if the table id is pinned; ledger entries A9, A10, A11, I17, F19 in the docs' ledger count.

## Decisions recorded (PM, for the placement)

1. The lower bound is Delta >= 0 (convexity of LME); the weaker mean(s) - LME(s) is dropped from the lemma, its test and
   this proposal.
2. Appendix B: L18 and L19 stay in the second part and "B.2 ... (L12 to L19)" is kept (the `test_paper` heading test requires
   it); at placement the part heading is reworded so that it does not say "the several-term fit" of a noise result.
   `PARTS` and the paper are not touched before the supervisor's word.

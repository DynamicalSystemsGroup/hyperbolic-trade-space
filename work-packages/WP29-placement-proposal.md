# WP29 placement proposal (stage 5; landed on dev with the placement, 2026-11-11)

For the supervisor's glance. Nothing below is in the paper, the docs, the register, the ledger or `references.bib`; the
lemmas, tests and Appendix B tables are on branch `wp29` and not on `dev`. If he declines a statement, its lemma, test and
Appendix B table are deleted as one unit. Kept apart throughout: the **model** (the noise-free soft maximum), the **fit**
(the estimator on a finite noisy table), the **analysis** (what a reader concludes).

## Revision after the supervisor's glance (2026-11-11; prepared by the derivation agent, not applied)

His disposition (WP29-decisions.md, the glance): not two lemma boxes but **one corollary**, after Proposition 2 and
Theorem 3, that accounts for noise where the paper reads. This section supersedes P1 below (the two boxes) and the
"May" and "May not" lists where they differ; P2 to P6 stand except as noted. Built on the branch: `derivation/
lemma_20_noise_ridge.py` (L20, 51 tagged steps; imports L3, L4 and L18 by their proved results), the ledger entries R3
(the clean fit interior to its face, well conditioned there) and I18 (the pseudoinverse), A9 given its symmetry relation,
`tests/test_noise_ridge.py` (28 tests). L18 stays as the supporting lemma (it now exports `L18_RESULT`); L19 stays in
Appendix B only, no box.

### Where the box goes

Proposition 2 of the rendered paper is the Gaussian cumulant (L6, `prop-cumulant`: the second `prf:proposition` after L2);
Theorem 3 is the convexity of the fit (L4, `thm-convex`: the third `prf:theorem` after L1 and L3). Both stand before
`res-L7` in `paper/paper.ipynb`, so the corollary is a new markdown cell **`res-L20` between `res-L6` and `res-L7`**,
label `cor-noise-ridge`, and its sketch cites `prop-cumulant`, `thm-convex` and `thm-kkt`. Text proposed (the shift is
written Delta w in the paper, because L18 already uses delta_j for a relative measurement error; the script's `dl` is
the same object):

> **Corollary (Noise moves the exponents by a ridge, L20).** *Derived. Hypotheses.* A1, A3, A5 (Sigma = sigma^2 I) or A9
> (a covariance Sigma), I9, I18; R3 (the clean fit is interior to its face and C is positive definite on the face's
> tangent space); the noise small and the result first order.
> Gaussian noise with covariance Sigma on the conditioned metrics adds a ridge to the objective, J_tau(w) + (tau/2)
> w'Sigma w, and to first order moves the exponents by Delta w = - (P C P)^+ P Sigma w, in the equal case
> Delta w = - sigma^2 (P C P)^+ P w. Here C is the softmax-weighted covariance of the log-metrics at the fit, P projects
> onto the tangent space of the active face, and an attribute with relative measurement error delta_j enters as
> sigma_j = delta_j / s_j, s_j its log spread (L18). The shift is at most tau ||P Sigma w|| / `conditioning_`, and it
> lowers ||w||^2. It says how far noise of a given size moves the exponents, not whether the rates are right.
> *Sketch.* The expected noisy objective is J_tau plus the ridge ({prf:ref}`prop-cumulant`, row by row); the Hessian of
> J_tau is tau C ({prf:ref}`thm-convex`) and its gradient on the face vanishes ({prf:ref}`thm-kkt`); setting the ridge
> gradient against tau C Delta w on the tangent space gives the closed form.
> *Script:* `derivation/lemma_20_noise_ridge.py`; Appendix B, L20.

Notes on the box. (1) "Toward uniform" is in norm: ||w||^2 falls at first order (L20.49: `delta'Sigma w <= -m
||delta||^2 <= 0`); the lemma does not say each exponent moves toward 1/d, and for a C that is not a multiple of the
identity some do not. (2) The size is stated in `conditioning_` terms: that diagnostic is tau times the smallest
eigenvalue m of C on the tangent space, so the bound is tau ||P Sigma w|| / `conditioning_`. (3) The box never says
"unbiased", "consistent" or "correct rates"; G-11 stays open.

### The demonstration (Appendix D), as injected noise on noise-free data of record

Header text (replaces the P3 header, same two sentences): the data of record carry no noise of their own; the noise is
injected as a design choice of this experiment, each raw attribute multiplied by exp(delta z); what the table shows
belongs to the fit and the conditioning together. Columns, per regime and delta: `conditioning_` (one value per regime),
the first-order shift predicted by L20 (largest component, on the active face, Sigma = diag((delta / s_j)^2), L18), the
shift measured (largest component of the mean over the script's eight draws), and the draw-to-draw spread; the
contending-set Jaccard column stays; the L6 columns and the offset-shift column of P3 are **dropped** (they served the
L19 reading, which is now in Appendix B only; their numbers stay in `tests/test_noise_lemmas.py`). A scratch computation
on the branch's code (`examples/adcs/noise_injection.py`'s draws and case; **not yet a generated value of the repository**,
the Appendix D cell must generate it):

| regime, `conditioning_` | delta (%) | predicted largest shift | measured, mean of 8 draws | spread of the draws |
|---|---|---|---|---|
| primary, 7.09 | 0.5 | 0.003 | 0.005 | 0.012 |
| | 2 | 0.047 | 0.071 | 0.043 |
| | 5 | 0.292 | 0.275 | 0.098 |
| | 10 | 1.168 | 0.304 | 0.067 |
| stock, 0.017 | 0.5 | 0.022 | 0.032 | 0.047 |
| | 2 | 0.348 | 0.102 | 0.068 |
| | 5 | 2.174 | 0.136 | 0.035 |
| | 10 | 8.694 | 0.147 | 0.043 |

What the table licenses, and no more: at 0.5 and 2 percent (primary) and 0.5 percent (stock) the predicted and measured
shifts agree within the spread of the draws; the stock regime, whose `conditioning_` is 400 times smaller, moves about
seven times as far at 0.5 percent, so the direction "larger where `conditioning_` is smaller" is borne out, the ratio of
the movements is not the inverse ratio of the diagnostic (the bound is an upper bound). Where the predicted shift exceeds
the smallest active exponent (primary from 5 percent: 0.29 against 0.136; stock from 2 percent: 0.35 against 0.012 to
0.04) the formula is outside its range and the measured shift saturates because the contending set changes (a new exponent
enters; the table's Jaccard column says so); the primary 5 percent agreement (0.292 against 0.275) is not read as a
confirmation. Two further limits the Appendix D text states: the conditioning is refitted on the noisy table, which L18 does
not cover (it assumes a fixed scaler: at 10 percent on total mass, spread 0.066, the noise itself inflates the spread), and
eight draws is a small sample. A second row of evidence for the surrogate itself is in the tests: on planted frontier data
(d = 4, N = 20000) the first-order formula is within 3e-4 of the minimiser of J + ridge in all nine cells of sigma in
{0.05, 0.10, 0.20} and tau in {5, 20, 50} (largest 2.94e-4), and the package's fit of the noisy table lies nearer that
minimiser than the clean fit does at tau = 5 (0.0006 against 0.0020 at sigma 0.10; 0.0013 against 0.0065 at 0.20), but
**not at tau = 50 and sigma = 0.20** (0.0078 against 0.0067), where the surrogate (a logarithm of an expectation) no
longer describes the noisy table; the cause is not established.

### The gaps rows (revised)

- **G-3** (L6 against a finite sample). Keep the row. Add to "what is claimed": the equal-noise reading is generalised to
  a covariance (L18), and the effect of that noise on the exponents is the corollary (L20), to first order. "What cannot
  be proved" gains: the noisy fit of a finite table landing at the minimiser of the expected objective (L20 proves the
  ridge identity for the expected exponential, a logarithm of an expectation; the gap to the expectation of the logarithm
  is a Jensen gap, measured, not proved). Evidence: `tests/test_noise_ridge.py::test_the_noisy_fit_tracks_the_ridge_at_small_tau`
  and `..._no_longer_follows_the_ridge_at_large_tau_and_noise`. Reading: unchanged ("a population quantity approached
  with N"), plus one clause: the offset's own bound is L19, Appendix B.
- **G-11** (Q2, consistency). Stays open and says so. Add one sentence to "what is claimed": L20 gives the first-order
  size of the movement of the exponents under Gaussian noise of known covariance, a bias at a stated noise level, not a
  consistency or unbiasedness statement. Evidence: the nine-cell test (`test_first_order_formula_is_within_3e_4_of_the_ridge_minimiser`)
  and M2's table. Reading: "a movement of the stated size under the stated noise; the rates are not certified."
- **G-12** (Q3, identifiability). Add under "what it does not show": a metric's presence in the contending set is a
  property of the sample, the conditioning and the noise together, and the L20 shift is large where `conditioning_` is
  small, which is where presence is least identified; and the formula does not hold at an exponent on the boundary of the
  simplex (`test_at_a_boundary_exponent_...`: the full-simplex projector sends a zero exponent to 0.014 where the
  constrained fit keeps it at zero; the formula on the face agrees to 2e-5) nor once the noise lifts a boundary exponent
  off zero (`test_when_the_noise_overcomes_the_complementarity_margin_...`). Reading: the contending set, `conditioning_`
  and the injected-noise table are read together.
- The **held A2 row** proposed in P4 is **withdrawn**: A2 is now the corollary, with a lemma; no separate row.

### Does a main-results clause earn its place?

The list has seven items; item 2 says the one-term fit's exponents are elasticities. The corollary answers the question a
reader of that item asks next, how far noise moves them, and is the one result that touches the paper's reading of the
exponents. The marginal-value test, applied also to what is there: a clause costs about twenty words and replaces
nothing; omitting it leaves the corollary visible only in the Results section and Appendix B. Candidate wording, appended
to item 2 and left to the paper stream to adopt or drop: "; to first order, noise on the metrics shifts the exponents by a
ridge the conditioning bounds ({prf:ref}`cor-noise-ridge`)". The paper stream decides from the rendered list and the
length ledger.

### What the revised corollary does not claim, and a check of the formula

The statement of the corollary is the lemma's STATEMENT: first order (the product of noise and shift is set aside and
named; no bound on the remainder), an interior solution on the active face with strict complementarity, small noise,
Gaussian noise, a fixed scaler; no statement that the noisy fit of a finite table lands at the minimiser of the ridge
objective; no statement that the fitted rates are right.

The supervisor's formula, checked against my own derivation (L20) and the numbers: **delta = -sigma^2 (P C P)^+ P w is
correct** as stated for Sigma = sigma^2 I (sign, the factor sigma^2, tau cancelled: the Hessian of J_tau is tau C and the
ridge gradient tau Sigma w), the sign confirmed by the nine-cell test; the general form is -(P C P)^+ P Sigma w. Four
refinements the corollary carries, none changing his formula: (1) "toward uniform" is true of ||w||^2 (the shift lowers
the ridge), not coordinate by coordinate; (2) "large exactly where `conditioning_` is small" is an upper bound,
||delta|| <= tau ||P Sigma w|| / `conditioning_` (the diagnostic is tau times the smallest eigenvalue of C on the tangent
space, so the tau reappears here), and the shift is large only when the ridge force has a component along the weak
direction; (3) P is the projector of the active face, as he wrote, not of the full simplex: at a boundary exponent the
full-simplex projector gives a spurious exponent (tested); (4) the quantity minimised is the logarithm of an expected
exponential, which the noisy fit approaches at small tau and not at tau = 50 with sigma = 0.20 (tested, cause not
established).

### Cascade (additions to the list below)

Lemma count 19 to 20 in the paper and docs (`tests/test_build_generated.py` already reads 20 on the branch; two
chain-membership expectations in `tests/test_proof_map.py` gained L18's and L20's proved-result imports and exports);
ledger entries R3, I18
and A9's new relation in the docs' ledger count and `docs/superpowers/notes` copies; `PARTS` in `paper/generate_proofs.py`:
L18 to L20 are about noise and belong in a third part ("Noise on the metrics", 18 to 20), not under the several-term fit
(the heading "(L12 to L20)" is kept until then, as the test requires); register rows C-a to C-d of P5 are re-cut as: the
ridge identity (L20.20), the first-order shift (L20.43 and the nine-cell test), the norm bound and the descent of the
ridge (L20.48, L20.49), the stated limits (the boundary test), and the table of Appendix D (generated). The vocabulary
check (`uv run python scripts/check_vocabulary.py`) has not been run on the proposed box text: "ridge", "active face" and
"tangent space" need the glossary's terms.

## The two statements, in words (L18 and L19; superseded as two boxes by the revision above)

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

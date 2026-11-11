# Track A spike: a result that characterises the model's relation to noise (WP28, S-9)

Question (the supervisor, S-9, verbatim in `work-packages/WP28-decisions.md`): whether the paper needs another result on
the model's relationship to measurement noise and/or noise in the process being measured, building on Proposition 2
(L6). Spike only: no change to the product, no derivation written. Scripts and outputs are in this folder; run from the
repository root with `uv run python work-packages/WP23-rounds/spikes/spike-E-noise/<script>`.

## Where the paper stands

L6 (`derivation/lemma_06_gaussian_cumulant.py`): under A5 (eps_j i.i.d. N(0, sigma^2)) and I5,
(1/tau) log E exp(tau w.eps) = tau sigma^2 ||w||^2 / 2, a population identity. Gap G-3 reads the fitted offset shift
against it (M1: ratio 1.07, 1.02, 0.99 at N = 400, 4000, 40000); G-11 (Q2, consistency) is open with M2 (planted
exponent error, noise 0.05). A5 is stated in log space on the conditioned metrics. A fact the paper does not use: the
cubesat data of record are deterministic simulator output, so the case has no noise of its own; noise on it can only be
injected.

Three things to keep apart (CLAUDE.md): the **model** (the posynomial frontier and its soft maximum, noise-free),
the **fit** (the estimator on a finite noisy table), the **analysis** (what a reader concludes about the system). And two
kinds of noise that look the same in the formula and differ in meaning:

- **Measurement noise in attributes**: the same configuration measured again gives a different reading; the
  system's response is fixed. The frontier of interest is the noise-free one; noise is an obstacle to recover it.
- **Noise in the process**: the system itself responds randomly (tolerances, environment). Rows are draws; the
  "frontier" is a choice (frontier of the mean, of a risk-adjusted value, or of the best realised draw).
  L6's sign is the point: the soft maximum is the entropic risk with the risk-seeking sign (+tau). Noise raises the level
  of the reference surface (lucky draws count as upside); a risk-averse reading is the -tau version, a different
  object, and is the analyst's choice, not a theorem.

## Sources (each opened; what was and was not verified)

| source | URL | opened | what it gives |
|---|---|---|---|
| Aigner, Lovell, Schmidt (1977), Formulation and estimation of stochastic frontier production function models, J. Econometrics 6(1):21-37 | https://doi.org/10.1016/0304-4076(77)90052-5 (resolver 302 to Elsevier); bibliographic page https://ideas.repec.org/a/eee/econom/v6y1977i1p21-37.html | the IDEAS page (no abstract, full text restricted); the composed-error form y = f(x) + v - u is from my knowledge, not from the page | the stochastic frontier: noise v symmetric, one-sided inefficiency u >= 0; observations can lie beyond the deterministic frontier |
| Land, Lovell, Thore (1993), Chance-constrained data envelopment analysis, Managerial and Decision Economics 14(6):541-554 | https://doi.org/10.1002/mde.4090140607 (resolver 302 to Wiley; Wiley page 403, abstract not opened) | the DOI resolves; the description (stochastic inputs/outputs, frontier envelops observations "most of the time") is from a search snippet | chance-constrained DEA |
| Land, Lovell, Thore (1994), Productive efficiency under capitalism and state socialism, Technol. Forecast. Soc. Change 46(2):139-152 | https://doi.org/10.1016/0040-1625(94)90022-1 via https://scholars.duke.edu/publication/638947 | yes (abstract page) | an application of chance-constrained DEA |
| Bolos, Benitez, Coll-Serrano (2024), Chance constrained directional models in stochastic DEA, Oper. Res. Perspectives 12:100307 | https://arxiv.org/abs/2410.14295 | yes (abstract) | the current chance-constrained family: radial and directional, a probability level in place of a temperature |
| Foellmer, Knispel (2013), Convex risk measures: basic facts, law-invariance and beyond, asymptotics for large portfolios, Handbook of the Fundamentals of Financial Decision Making, ch. 30 | https://econpapers.repec.org/RePEc:wsi:wschap:9789814417358_0030 (DOI 10.1142/9789814417358_0030 taken from the page's links) | yes (abstract page) | convex risk measures; the entropic risk (1/gamma) log E exp(gamma X) belongs to this family but the page does not name it. I did not open a page that states the entropic formula; the Gaussian value mu + gamma sigma^2 / 2 is L6 itself (verified in the lemma script), not a citation |

No source yet opened that proves anything about the soft maximum with noise; the citations are positioning (what a
reader from stochastic frontier or stochastic DEA will ask), not support for a claim. Any claim adopted later needs
its own lemma or test. A source for the entropic risk with a stated formula still has to be found and opened
(Foellmer-Knispel 2011, Stochastics and Dynamics, DOI 10.1142/S0219493711003334, resolves by 302 to World Scientific, page 403).

## Relation to the stochastic-frontier and chance-constrained literatures (positioning, not a claim)

Stochastic frontier analysis separates the deviation from the frontier into noise v and inefficiency u by distributional
assumptions (v Gaussian, u half-normal). Stochastic DEA keeps the envelope but asks it to hold with a given
probability. The paper's finite-tau fit is neither: tau softens the envelope, "some designs lie beyond it" is the
stochastic-frontier picture (v pushes a row over a deterministic frontier), and tau is chosen by the fraction above.
L6 is the one place the paper ties tau to a noise level. A reader from either literature will ask: what noise level does
my tau assume, and how far do the exponents move with it? The candidates below answer that.

## Candidates

### A1. Two-regime bound on the noise shift of the soft maximum (model, a lemma)

- Hypothesis: L6 is exact only when the soft-maximum weights spread over many rows; as tau grows it overshoots, since
  the fitted offset cannot rise faster than the largest noise draw.
- Claim: for fixed clean scores s_i and noise z_i = w.eps_i i.i.d. N(0, v^2), v = sigma ||w||, with LME the log-mean-exp:
  `mean(s) - LME(s) <= E LME_tau(s+z) - LME_tau(s) <= min( tau v^2 / 2 , E max_i z_i )`, and E max z_i <= v sqrt(2 log N).
  First bound: Jensen (log concave) with L6. Second: exp(tau(s_i+z_i)) <= exp(tau s_i) exp(tau max z). Lower: LME >= mean.
- Check: lemma script (SymPy: Jensen step is concavity of log; the max step is an inequality of exponentials, as L5 does);
  a test on planted data. Cheap.
- Numerical sanity (check1): 60 cells (on-surface and interior scores, N = 100 to 10000, v = 0.05 and 0.2, tau = 1 to 200,
  Monte Carlo): 0 violations. The L6 branch is active up to tau v^2 / 2 about 0.1 to 0.3 and the bound is already
  loose by a factor 2 to 6 at tau = 50 to 200; the actual shift sits below E max z (e.g. 0.72 against 0.77). So the
  bound is true; the crossover tau* = 2 sqrt(2 log N) / v is a usable rule, not a sharp one.
- Cost: low (one lemma, one test, a sentence and a G-3 row update). Risk: low; the claim is an upper bound and
  the paper must say it is not tight.
- Adds: tells the reader when the offset shift can be read as L6 (tau v^2 small against log N) and when not, which
  G-3 and M1 only show at one tau. Where: a corollary after L6 and a revised G-3 reading.

### A2. Noise on the metrics is a ridge on the exponents (model/fit, a lemma plus a diagnostic)

- Hypothesis: with L6 applied row by row, the population objective under noise is J_tau(w) + tau sigma^2 ||w||^2 / 2
  (a ridge, on the simplex, towards uniform exponents), so the noisy fit is the noise-free fit with a ridge, and to first
  order the exponent bias is delta = -sigma^2 (P C P)^+ P w, C = the p-weighted covariance of the log-metrics at the fit
  (tau cancels, since the Hessian is tau C). This ties noise to `conditioning_` (the restricted eigenvalue): the
  exponents are fragile to noise exactly where that eigenvalue is small.
- Check: lemma (L3/L4 Hessian plus L6); a test on planted data; a diagnostic (a noise-sensitivity reading of
  `conditioning_`).
- Numerical sanity (check2, planted d = 4, N = 20000, sigma 0.05, 0.1, 0.2, tau 5, 20, 50): the first-order formula
  matches the ridge-objective minimiser to 3e-4 or better. The noisy package fit tracks the ridge minimiser at small
  tau (sigma 0.2, tau 5: 0.0013 apart against 0.0065 from the clean fit) and less well at tau 50 (0.0078 apart), where the
  weights concentrate and the identity needs A1's condition. The bias itself is small on this well-conditioned data
  (largest 0.006), comparable to the sampling error of the noisy fit. So the identity holds and the effect is small
  where the problem is well conditioned.
- Cost: medium (lemma needs the Hessian-in-the-tangent-space step and an interior-solution hypothesis; the estimator
  may not need to change). Risk: medium; it is a first-order statement and boundary exponents (zero) are excluded; the
  effect may be negligible on the case.
- Adds: a mechanism for "what noise does to the exponents" with a computable reading from the fitted object; answers
  part of Q2 as a bias statement, not consistency. Where: Section on assumptions/gaps, G-11.

### A3. L6 with a noise covariance Sigma, and the conditioning as the map from measurement error to Sigma (model plus analysis, a lemma plus a case experiment)

- Hypothesis: A5 (equal sigma in every conditioned metric) cannot hold after the standard conditioning, because the
  scaler divides each log-attribute by its log spread s_j, so a relative measurement error delta on attribute j becomes
  sigma_j = delta / s_j. The cubesat has s_j = 0.066 for total mass and 0.5 to 0.9 for the others: one percent error on
  mass is as large in the metric as 12 percent on settling time.
- Claim: for eps ~ N(0, Sigma), (1/tau) log E exp(tau w.eps) = tau w'Sigma w / 2 (L6 is Sigma = sigma^2 I); with a
  diagonal Sigma the shift is tau sum_j w_j^2 sigma_j^2 / 2 and sigma_j = delta_j / s_j under log-affine conditioning (A4).
- Check: lemma (the same MGF route as L6 with a multivariate normal; the conditioning step is algebra); case
  experiment on the cubesat (check3).
- Numerical sanity (check3, cubesat of record, noise injected as a relative error delta on every raw attribute, then
  conditioned and refitted at the clean tau, 8 reps): in the primary regime the contending set (Jaccard 1 = same) falls to
  0.94 at delta 0.5 percent, 0.82 at 2 percent and 0.71 at 5 percent, with the largest exponent change 0.013, 0.085 and
  0.29; total mass (exponent 0.358, spread 0.066) drives it. The baseline regime (mass exponent 0) is steadier: Jaccard
  0.98 at 2 percent, 0.89 at 10 percent. The offset shift follows L6 with the diagonal Sigma at small noise (primary,
  delta 0.5 percent: 0.013 against 0.014; baseline: 0.000 against 0.000) and saturates beyond (A1's regime); the isotropic
  A5 reading is off by 10 to 20 times everywhere. This candidate survives and is the strongest in showing the case.
- Cost: lemma low; the case experiment medium (a script and a table; the data stay unchanged since the noise is injected). Risk: low for the
  lemma; the injected noise is a design choice and the table must say so (the data have none). The statement "which
  metrics fail first" is about conditioning, which is the analyst's step, so the prose must say the finding belongs to the
  fit-plus-conditioning pair, not to the model.
- Adds: a quantity a reader can use: "your measurement error divided by the attribute's log spread is the noise the fit
  sees", and a case demonstration of how the contending set degrades with it. Answers part of Q3 (identifiability under
  finite observation). Where: after L6 (the covariance form), a short case table in the results or an appendix, G-3/G-12.

### A4. The temperature under noise: the exact-maximum fit has a noise floor, a finite temperature does not (fit; an experiment, no lemma)

- Hypothesis: error in the exponents is U-shaped in tau under noise: the exact maximum (tau = infinity) follows the
  largest noisy scores and keeps an error proportional to sigma however large N; a moderate tau averages it.
- Check: a planted-data experiment only.
- Numerical sanity (check4, 15 seeds, sigma 0.05 and 0.15, N = 200, 2000, 20000, tau 1 to 300 and infinity): at tau =
  infinity the median error is 0.011, 0.010, 0.007 (sigma 0.05) and 0.032, 0.031, 0.023 (sigma 0.15): it barely falls with N and
  scales with sigma. At tau = 10 to 30 it is 0.016 to 0.007 at N = 200 and 0.001 to 0.003 at N = 20000. At tau = 1 the
  error is larger at small N (0.087) and falls with N, so the small-tau side is bias that N removes on this planted family,
  and the U is mostly the tau-large arm. The minimum sits near tau 10 to 30 for all N and does not move with N in these cells.
- Verdict: the claim "no decay at tau = infinity" is already in G-11 (M2); this adds a sigma-dependence and a wider tau grid but no new
  statement. Weak as a result. Better as a table row than as a result; the "minimum moves up with N" version did not appear.
- Cost: low. Risk: it duplicates M2. Adds: little. Candidate to drop.

### A5. Risk-averse certainty equivalent as a named variant (analysis; a definition plus a worked example)

- Hypothesis: for process noise, a reader wants the risk-averse reading. Replacing tau by -tau in the aggregate score gives
  w.mu - gamma w'Sigma w / 2 (entropic risk with a stated sign); the per-metric adjustment mu_j - gamma sigma_j^2 / 2 is
  linear in w and is more conservative, since w_j^2 <= w_j on the simplex.
- Check: lemma (L6's route plus the simplex inequality); no case experiment, since the data carry no replicates.
- Cost: low for the lemma, but the use (replicate runs to estimate Sigma) is not in the case, so there is nothing to show.
  Risk: high of overreach: it introduces a risk attitude the method does not otherwise have. Adds: positions the method
  against the entropic-risk literature. Where: Discussion only.
- Sanity: none run (algebra). Not recommended as a result at this stage; recorded for the Discussion.

## What was run

| script | what | output |
|---|---|---|
| `check1_shift_bounds.py` | Monte Carlo of the soft maximum's shift against L6 and the max bound, 60 cells | `check1-output.txt` (0 violations) |
| `check2_noise_is_ridge.py` | planted data: noisy fit vs ridge objective vs first-order bias | `check2-output.txt` |
| `check3_cubesat_noise_injection.py` | cubesat, both regimes, relative noise 0.5 to 10 percent injected, refit | `check3-output.txt` |
| `check4_tau_under_noise.py` | planted data: exponent error against tau, sigma, N | `check4-output.txt` |

None of these touches `derivation/`, `src/` or the data. Seeds are fixed. Nothing was killed outright; A4 is weak and
A5 untested.

## Plain options for the driver

1. Build A3 only (L6 with a covariance, the conditioning as the map from measurement error to noise, one case table).
2. Build A3 and A1 (the covariance form and the two-regime bound on the shift), one lemma each.
3. Build A3, A1 and A2 (adds the ridge reading and a noise-sensitivity reading of `conditioning_`).
4. Build nothing; record A1 to A3 in the gaps ledger as tested-by-spike statements and cite them in G-3, G-11 and G-12.
5. Take A5 into the Discussion as a short paragraph, with any of the above.

Open points that the driver may want answered before a build: the injected-noise table needs a statement that the data
have no noise of their own; whether the entropic-risk source (Foellmer-Knispel) has to be opened in full before
the paper cites it.

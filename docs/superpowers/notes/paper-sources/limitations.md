---
world: formal
---

# Extensions and limitations

Posynomial invariant form is a model of a trade space, and this page lists where it is wrong in
ways we know about, so that its usefulness can be judged by the reader and not assumed. The policy
for reading the formal results is the Map and territory paragraph of [Mathematics](method.md), and
the gaps between the formal objects and the implementation are recorded in
`docs/superpowers/notes/abstraction-gaps.md`. The conditions of the theory are the terms on which
the interpretation is offered; the table is in
[Mathematics](method.md#conditions-of-the-theory), and each limitation below points back to the
condition it comes from.

There is a division of labour in what the checks do. Machine verification (the lemmas in
`derivation/`, run by the test suite) shows that a formula follows from stated hypotheses and that
the code agrees with the formula. Human validation decides whether the hypotheses are reasonable
for the problem at hand, and whether a finding is an engineering fact or an artefact of how the
metrics were conditioned. The first is in the repository; the second is the analyst's.

## Limits of the method

**Log-convexity only (condition: the one-term and K-term model form).** The fitted surface is
a log-convex envelope: in log space, the boundary of a convex set, or its softened version. Any
structure that is not log-convex, such as dents, holes and disconnected regions, is invisible to
the surface and is left to the near-frontier analysis in the chart. No number of terms $K$
represents it (the extension is a log-convex envelope plus a non-convex residual). A hole is
therefore an opportunity only if the trade space is log-convex around it, which the data cannot
prove.

**One term at $K=1$ (conditions: R1, A2).** A single monomial has constant exchange rates: it is
tangent to the admissibility set at one place, the balanced point, and finds one tension there.
L7 proves the elasticities $-w_k/w_j$ for the fitted hyperplane itself; identifying them with the
fit at the balanced point needs L3 and R1, and they are not proved for the data away from it. Trade spaces whose exchange rates vary by region need the $K>1$ extension.

**Optimism off the balanced point (condition: R1).** Far from the diagonal a design can have
$V\ll1$ while being locally on the frontier, because the one hyperplane is not tangent there. Our
reading (from the spec, with no lemma behind it) is that the score $V-1$ is then conservative and
that near the balanced region it is more reliable. Points whose chart
coordinates lie outside the training hull are flagged; the $K>1$ extension is expected to tighten the bound (a conjecture, not proved).
When R1 fails outright (the balanced point at a vertex, an edge, or a facet with a zero normal
component) the exponents are not unique, some elasticities are undefined, and the frontier reading
degrades to the weaker invariant-form reading.

**Noise band and calibrated novelty (conditions: A3, A5).** At a finite temperature some training
designs lie above $V=1$ by construction. A novelty score is meaningful only relative to a band of
order $1/\tau$, so the calibrated score (the rank of $\log V$ among training scores, and
$\tau\log V$) belongs next to $V-1$. Under the log-space Gaussian model the population objective gains the cumulant
$\tau\sigma^2\|w\|^2/2$ (L6), a population identity that we read as a ridge toward balanced
exponents; noise that is not Gaussian, independent or homoscedastic is outside that statement, and
no finite-sample or consistency statement is made.

**Holes versus structural strata (condition: human validation).** A region of the chart with no
near-frontier points can be an opportunity, a categorical stratum that cannot be occupied, or a
region that is simply unsampled. The distance-to-nearest-point score cannot tell these apart;
human validation decides.

**Novelty is not preference.** $V-1$ measures how far beyond the learned surface a design lies. It
does not say that the design is wanted, feasible or safe, and the elasticities are shape, not
preference: they say how metrics trade on the surface, not how they should be traded.

**Dependence on conditioning (condition: A4).** The metrics are conditioned by the analyst:
oriented so that larger is better, shifted to be positive and scaled to a comparable log-spread
about a chosen reference point. The fitted exponents describe the conditioned metrics, and moving
the reference or the scale of a single metric changes which term is tangent. The pull-back of L9
is exact only if the conditioning is log-affine and invertible. Conditioning is not a nuisance
step to be tuned until the answer looks right; it defines the question.

**Small-sample identifiability (conditions: R1, rank of the weighted covariance).** With few
designs, or designs that barely differ near the envelope, the fit may be weakly determined. L4
proves convexity of the objective, not strict convexity; uniqueness at a finite temperature needs
a rank condition on the weighted covariance that is not proved, and the fit reports its effective
sample size and `conditioning_` (the smallest eigenvalue of the restricted Hessian) so the analyst
can see how many designs carry it and how flat the least-determined direction is. At very high temperature the fit
rests on a few extreme designs and is noise-sensitive; at very low temperature (below $\tau\approx3$, outside the documented useful range) the
the softmax weights approach uniform (by their definition, L3) and the soft maximum approaches the mean of the scores (L5), so
`frac_above_` is not monotone there (see the API page).

**Local optimality is conditional (condition: R2).** For the several-term fit, level 3 of the
[three levels](method.md#three-levels-of-guarantee) holds for step B, unpenalized, where the
assignment margin is positive. At $\tau=\infty$ the margin is zero when a frontier row lies on two
term planes or two terms coincide (4 of 20 chosen runs on the planted data, none at $\tau=50$);
the status is then `stationary_without_margin`, with first-order stationarity per term and no
local-optimality claim. Step D and the penalty carry no level 3 (`not_applicable`), and
`termination_` of an iteration cap or a guard stop is never `certified`.

**What the n-lemma reading cannot say.** The contending set is read from the support of the
exponents. That reading requires the floor on exponents to be zero, is exact only at infinite
temperature, and at a working temperature gives a graded participation, not a sharp set. At $K=1$
it describes the balanced point and no other region. The fit reports what contends; whether that
is a recognizable dilemma, trilemma or n-lemma is for the engineer to decide.

**Prediction from configuration is conditional.** Predicted position inherits the surrogate's
error and extrapolation risk, and is conditional on the fitted trade space. The unsupervised
estimator does not make it.

**Disambiguation: hyperbolic.** In this project "hyperbolic" describes the shape of the score: it
tends to zero as any participating metric tends to zero. It is not principal component analysis in
negative-curvature geometry, which is a distinct line of work [@chami2021horopca], and the two
should not be confused.

## What the contrast with PCA does and does not claim

The method is described as finding tensions, where PCA finds variance; see the contrast in
[Mathematics](method.md#tensions-not-variance). Its limits belong here too. $K=1$ finds one tension.
Several regional tensions are the $K>1$ extension. A deflation-style search for successive
tensions, in the way PCA extracts successive components, is a research question; we make no claim
that it works or that successive tensions are orthogonal in any sense. And a tension is a
statement about the conditioned metrics and the sampled space: tensions the sampling never
exercised cannot appear.

## Extensions: the posynomial fit (small K) and kernels (not built)

**The posynomial extension, $K>1$: built for small $K$.** The monomial is replaced by the
generalized posynomial $V_K$, whose logarithm is a softmax-affine function [@hoburg2016data] and
which is compatible with geometric programming [@boyd2007tutorial]. The identities underlying the
shift equivariance, and the soft-maximum limit, are proved (L10, conditions A6 and F10); that a
maximizer of $V$ is Pareto-efficient is proved (L11), without its converse; that homogeneity,
projection and novelty carry over is expected from the construction, not proved. The estimator's
`n_terms` fits $K$ terms by partition and refit; it is built, tested and demonstrated for small $K$
(the case study uses $K=3$). What it returns is a local optimum (I7), and nothing is claimed about
global optimality. The assumptions behind it are named, defended and extended in
[Mathematics](method.md#simplifying-assumptions). Future work, none of it built:

- *Scalability and performance.* Many terms, many designs, and faster solves.
- *Selection of $K$.* The analyst chooses $K$, reading a table of the objective and the fraction
  above the frontier by $K$, with the temperature re-selected at each $K$; a selection rule is open.
- *Temperature across $K$.* $\tau$ is re-selected at each $K$ by the $K = 1$ criterion; whether the
  target fraction should differ by $K$ is open.
- *Nonsmooth search.* The fit is a hard maximum with kinks on the ridges, smoothed on request by
  `term_temperature`. We expect, and have not shown, that searches along the frontier tolerate the
  kinks, since a maximum of smooth functions has a tangent cone at a ridge and its generalized
  gradient is the convex hull of the active normals; searching on those tangent cones is the way
  to drop the smoothing.
- *The local optimum.* A global search or a certificate, and a joint rather than term-by-term
  refit. The alternation can be trapped: on 20 planted seeds ($K=3$, $d=4$, $N=400$) it recovers
  the planted terms in 16 or 17, for either per-term step, and the failures are terms with only
  five or six frontier rows (the generator guarantees at least $d+1$, which is necessary for
  identifiability and not sufficient for recovery) and one seed with a well-populated term.
  The analyst's options are more restarts (`n_restarts`), a better start, and the tangent step
  (`refit_step="tangent"`), and their limits are measured. The spikes
  (`docs/superpowers/notes/spike-objective/`) found, at $\tau=\infty$, that on seeds 3 and 8 two or
  three of the five restarts pass, so a restart that recovers the terms exists there; on seeds 1
  and 16 none does, because the sparse term is barely determined by its frontier rows. But the
  restart is chosen by the mean slack, and that selection does not pick the passing restarts:
  rerunning the built solver (step B, $\tau=\infty$) with 5, 20 and 50 restarts recovered none of
  seeds 1, 3, 8 and 16. At $\tau=50$
  the default step has no passing restart on seeds 3 and 8; the tangent step does (3 and 5). So
  `n_restarts` is a cost-for-robustness knob, not a remedy; the selection rule and the start are
  the limit, and a different selection rule or start is future work.
- *Thin terms.* A term with fewer frontier rows than dimensions is not determined by them; only
  the interior rows locate it, and the mean-slack objective prefers to split a large term rather
  than keep a sparse one. More restarts do not cure this (no restart passes on seeds 1 and 16, and extra restarts did not help elsewhere: see above);
  the options are a larger sample, a better start or the tangent step, which uses the near-frontier
  rows directly.
- *A non-monotone step.* `refit_step="tangent"` (step D) uses the near-frontier rows directly and
  recovers about as often as the default, but the mean slack is not monotone under it; the
  default `"support"` step is monotone and is the one the paper presents. A frontier-weighted
  objective was measured and parked (`docs/superpowers/notes/spike-objective/`).
- *Kernels,* below.

**Kernel methods.** The research direction is kernel expansions that remain generalized
posynomials, so that the programs stay geometric programs. Kernel PCA [@schoelkopf1998nonlinear]
is the kin to cite for the feature-engineering idea; no source we know addresses kernels restricted
to GP-compatible forms, and the support-vector analogy is a hypothesis. Open questions are
selecting support designs, the local normals, the roles of the two temperatures, overfitting toward
the data's convex hull and whether novelty and white-space semantics survive. See
[Mathematics](method.md#research-direction-kernel-methods-under-the-ggp-constraint).

**Not claimed anywhere.** The documentation makes no claim of priority or novelty for the
method. Close neighbours that do part of the same job are reviewed in `literature.md`.

# Extensions and limitations

All models are wrong and some are useful. Posynomial invariant form is a model of a trade space,
and this page says where it is wrong in ways we know about, so that its usefulness can be judged
by the reader and not assumed. The theory behind the method does not have to match the
implementation exactly: its job is to ground the work and to explain how to understand and
interpret results, including the method's limitations. Theorems may carry hypotheses that we cannot
certify for the spaces we sample, such as well-conditioned metrics, a balanced point in the
relative interior of a facet, or log-convexity where white space is read. We therefore state every
such hypothesis explicitly, in the ledger `derivation/axioms.py`, with its interpretive role and its
failure mode. The conditions of the theory are the method's limitations. They are not defects to be
minimized; they are the terms on which the interpretation is offered. The table of conditions is in
[Mathematics](method.md#conditions-of-the-theory), and each limitation below points back to the
condition it comes from.

There is a division of labour in what the checks do. Machine verification (the lemmas in
`derivation/`, run by the test suite) shows that a formula follows from stated hypotheses and that
the code agrees with the formula. Human validation decides whether the hypotheses are reasonable
for the problem at hand, and whether a finding is an engineering fact or an artefact of how the
metrics were conditioned. The first is in the repository; the second is the analyst's.

## Limits of the method

**Log-convexity only (condition: the one-facet and K-facet model form).** The fitted surface is
a log-convex envelope: in log space, the boundary of a convex set, or its softened version. Any
structure that is not log-convex, such as dents, holes and disconnected regions, is invisible to
the surface and is left to the near-frontier analysis in the chart. No number of terms $K$
represents it (the extension is a log-convex envelope plus a non-convex residual). A hole is
therefore an opportunity only if the trade space is log-convex around it, which the data cannot
prove.

**One facet at $K=1$ (conditions: R1, A2).** A single monomial has constant exchange rates: it is
tangent to the admissibility set at one place, the balanced point, and finds one tension there.
The elasticities of L7 are those at that point and are proved for the surface, not for the data
away from it. Trade spaces whose exchange rates vary by region need the $K>1$ extension.

**Optimism off the balanced point (condition: R1).** Far from the diagonal a design can have
$V\ll1$ while being locally on the frontier, because the one hyperplane is not tangent there. The
score $V-1$ is then conservative. Near the balanced region it is more reliable. Points whose chart
coordinates lie outside the training hull are flagged; the $K>1$ extension tightens the bound.
When R1 fails outright (the balanced point at a vertex, an edge, or a facet with a zero normal
component) the exponents are not unique, some elasticities are undefined, and the frontier reading
degrades to the weaker invariant-form reading.

**Noise band and calibrated novelty (conditions: A3, A5).** At a finite temperature some training
designs lie above $V=1$ by construction. A novelty score is meaningful only relative to a band of
order $1/\tau$, so the calibrated score (the rank of $\log V$ among training scores, and
$\tau\log V$) belongs next to $V-1$. Gaussian noise adds a known offset to $\beta$ and a ridge
toward balanced exponents (L6); noise that is not Gaussian, independent or homoscedastic is
outside that statement.

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
the reference or the scale of a single metric changes which facet is tangent. The pull-back of L9
is exact only if the conditioning is log-affine and invertible. Conditioning is not a nuisance
step to be tuned until the answer looks right; it defines the question.

**Small-sample identifiability (conditions: R1, rank of the weighted covariance).** With few
designs, or designs that barely differ near the envelope, the fit may be weakly determined. L4
proves convexity of the objective, not strict convexity; uniqueness at a finite temperature needs
a rank condition on the weighted covariance that is not proved, and the fit reports its effective
sample size so the analyst can see how many designs carry it. At very high temperature the fit
rests on a few extreme designs and is noise-sensitive; at very low temperature it degenerates to a
vertex.

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

## Extensions, documented and not built

**The posynomial extension, $K>1$.** Replace the monomial by the generalized posynomial
$V_K$, whose logarithm is a softmax-affine function [@hoburg2016data] and which is compatible with
geometric programming [@boyd2007tutorial]. The identities that carry homogeneity, projection and
novelty over are proved (L10, conditions A6 and F10). What is not built is a solver: the fit of an
envelope with $K$ facets is a non-convex problem with per-facet support and a choice of the
number of terms and the temperature, and we leave it to a later package. The estimator's
`n_terms` parameter exists so the interface need not change; a value other than one raises
`NotImplementedError`. A solver-free substitute is to refit the single-term model at several
reference points. A planted two-facet frontier is the demonstration to build when the solver
exists: $K=1$ should under-score one region and $K=2$ should recover both. See
[Mathematics](method.md#the-posynomial-and-ggp-extension).

**Kernel methods.** The research direction is kernel expansions that remain generalized
posynomials, so that the programs stay geometric programs. Kernel PCA [@schoelkopf1998nonlinear]
is the kin to cite for the feature-engineering idea; no source we know addresses kernels restricted
to GP-compatible forms, and the support-vector analogy is a hypothesis. Open questions are
selecting support designs, the local normals, the roles of the two temperatures, overfitting toward
the data's convex hull and whether novelty and white-space semantics survive. See
[Mathematics](method.md#research-direction-kernel-methods-under-the-ggp-constraint).

**Not claimed anywhere.** The documentation makes no claim of priority or novelty for the
method. Close neighbours that do part of the same job are reviewed in `literature.md`.

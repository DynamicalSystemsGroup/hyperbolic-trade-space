# Limitations

The model is a map of a trade space and not the territory. These are the limits that change what you
do with a result.

**Conditioning defines the question.** The exponents describe the conditioned metrics. Moving the
reference or the scale of one metric changes which facet is tangent. Refit under a second reasonable
conditioning and report what moves ([Conditioning](conditioning.md)).

**The surface is log-convex.** Dents, holes and disconnected regions are invisible to it, and no
number of terms represents them. A hole is an opportunity only if the trade space is log-convex around it.

**One term has one tension.** A single term has constant elasticities and finds one tension, at
its balanced point. Away from that point a design can score below 1 while locally on the frontier. If the balanced point sits on a vertex or
edge of the weights' simplex, exponents are not unique and some elasticities are undefined. For
regionally varying rates fit [several terms](fitting.md).

**The surface is not the Pareto boundary.** The fitted reference surface and the supporting envelope
are determined by the sample you give; the Pareto boundary is a property of the system. A maximizer
of V is efficient in the contending metrics, and the converse is not claimed.

**Noise and temperature.** At a finite temperature some designs lie beyond V = 1 by construction.
Judge a score against the band 1/tau. A very high tau rests the fit on a few extreme designs; below
tau of about 3 the soft maximum approaches the mean.

**Small samples.** With few designs, or designs that barely differ near the edge, exponents are
weakly determined. Read `n_eff_` and `conditioning_` ([Reading termination](termination.md)).

**Contending sets are a reading.** The set is exact at infinite temperature with `min_exponent` at
0, and graded participation at a working temperature. The fit reports what contends; whether that is
a recognizable dilemma is for you. A tension is a binding constraint, not a correlation, and
negative association near the surface is partly a closure effect.

**Local fits.** A multi-term fit is a local optimum chosen among seeded restarts. On 20 planted seeds
($K = 3$, $d = 4$, $N = 400$) it recovers the planted facets in 16 or 17; failures are facets with
five or six frontier rows. More restarts do not cure this; a larger sample or `facet_step="tangent"`
can help.

**Novelty is not preference.** V - 1 says how far a design lies beyond the learned surface, not that
it is wanted, feasible or safe. Elasticities are shape, not preference, and not causal.

**Prediction is conditional.** A prediction inherits the surrogate's error and the fitted trade
space ([Predicting](prediction.md)).

**Name.** "Hyperbolic" describes the shape of the score, which tends to zero as any participating
metric does. It is unrelated to PCA in hyperbolic space [@chami2021horopca].

Machine checks confirm that formulas follow from stated conditions and that the code agrees with
them. Whether the conditions suit your problem is for you to judge.

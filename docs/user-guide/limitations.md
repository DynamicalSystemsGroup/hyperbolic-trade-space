# Limitations

The model is a map, not the territory. These limits change what you do with a result.

**Conditioning defines the question.** Moving the
reference or the scale of one metric changes which term is tangent. Refit under a second reasonable
conditioning and report what moves ([Conditioning](conditioning.md)).

**The surface is log-convex.** Dents, holes and disconnected regions are invisible to it, and no
number of terms represents them. A hole is an opportunity only if the trade space is log-convex around it.

**One term has one tension.** A single term has constant elasticities and finds one tension, at
its balanced point. Away from that point a design can score below 1 while locally on the frontier. If the balanced point sits on a vertex or
edge of the weights' simplex, exponents are not unique and some elasticities are undefined. For
regionally varying elasticities fit [several terms](fitting.md).

**The surface is not the Pareto boundary.** The fitted reference surface and the supporting envelope
are determined by the sample you give; the Pareto boundary is a property of the system. A maximizer
of V is efficient in the contending metrics, and the converse is not claimed.

**Noise and temperature.** At a finite temperature some designs lie beyond V = 1 by construction.
Judge a score against the band 1/tau. A very high tau rests the fit on a few extreme designs; below
tau of about 3 the soft maximum approaches the mean.

**Small samples.** With few designs, or designs that barely differ near the edge, exponents are
weakly determined. Read `n_eff_` and `conditioning_` ([Reading termination](termination.md)). Designed
samples, such as grids, are not independent observations: the exponents describe the sample and carry
no sampling error.

**Contending sets are a reading.** The set is exact at infinite temperature with `min_exponent` at
0, and graded participation at a fit temperature. A tension is a binding constraint, not a correlation, and
negative association near the surface is partly a closure effect.

**Local fits.** A multi-term fit is a local optimum chosen among seeded restarts. A trade-off with few
frontier rows can be missed; more restarts do not cure this, a larger sample can help.

**Novelty is not preference.** V - 1 says how far a design lies beyond the fitted reference surface, not that
it is wanted, feasible or safe.

**Prediction is conditional.** A prediction inherits the surrogate's error and the fitted trade
space, and inverting a level into a bounded outcome is yours ([Predicting](prediction.md)).

**Name.** The [glossary](../generated/glossary.md) and the [paper](paper:sect-definitions) define "hyperbolic".

Machine checks confirm that formulas follow from stated conditions and that the code agrees with
them. Whether the conditions suit your problem is for you to judge. The lemma scripts replace
pencil-and-paper derivation, not formal verification; [Appendix B](paper:appendix-b) of the paper states
what they do and do not establish. A proof in a theorem prover would fix each lemma's statement over the real numbers.
It would not bound the double-precision error, which the certificates check.

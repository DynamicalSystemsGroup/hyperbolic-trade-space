# Why and how to use it

Suppose you have run many designs through an evaluation, a simulator or a test, and each design
comes back with a handful of numbers: mass, power, settling time, pointing error. Some designs are
better in one number and worse in another. What you want to know is not a single best design but
the shape of the trade: which numbers pull against each other, at what exchange rate, where the
edge of what is achievable lies, where the unexplored gaps are, and how far past the edge a new
idea would be. This page explains how posynomial invariant form answers those questions and what
you do to use it. The mathematics is in [Mathematics](method.md) and what can go wrong is in
[Extensions and limitations](limitations.md).

## The idea: tensions, not variance

If you have used principal component analysis, the first picture is a good one. PCA looks at your
data and finds the directions in which it spreads most; it asks where the data are free. This
method asks a different question: along which positive combination of the metrics do the data stop?
It looks for the binding constraint among metrics that are all better when larger. The answer is a
set of weights, one per metric, that sum to one. Metrics in the support of the weights (at infinite temperature; at finite temperature, those with non-negligible weight) are the ones that
contend at the edge; their ratios are the exchange rates between them; a metric with zero weight is
not constrained by the edge at that point.

We call this the tension. It is what defines the trade-off. The spread is not thrown away: along
the edge, the designs that sit near it differ only in how they trade the contending metrics, and
the principal directions of that spread are the trade-offs the designs actually exercised. Two
metrics that rise and fall together there are aligned, not in tension.

The set of contending metrics is found, not chosen. Engineering is full of named dilemmas and
trilemmas, which are often rules of thumb. We use the term n-lemma for a facet of the achievable
region on which exactly $n$ metrics contend (dilemma and trilemma are $n=2$ and $n=3$). The fit does not need to know in advance which metrics
contend, or how many: it reports the contending set, the support of the weights at infinite temperature (at a finite temperature other metrics may carry small weight, a graded participation), and that may be two,
three or more. What the fit reports is a finding to be explained, not a label to be confirmed.

## The frontier as $V=1$

The weights define a single score, the weighted geometric mean of the metrics,
$V=\prod_j m_j^{w_j}$. Because the weights sum to one, doubling every metric doubles $V$, so $V$ is
read as a factor of improvement. After a one-time normalization the edge of the achievable region is
exactly the surface $V=1$. A design with $V<1$ is inside; a design with $V>1$ is beyond the edge
learned from the data, and $V-1$ says by how much. We call this normalized representation the
invariant form, and the method posynomial invariant form because the same idea extends from one
product of powers to sums of such products (posynomials).

Three surfaces answer to the word edge, and the register names them. The *fitted reference
surface* is the smooth $V=1$ surface that the fit places at its working temperature; because it is
smooth, a few designs sit just beyond it. The *$\tau=\infty$ supporting envelope* is the hard
version of the same surface, which no design exceeds. The *Pareto boundary* is the boundary of the
attainable set, a property of the designs that can exist and not of the fit. The text says edge or
frontier where the context makes the choice plain.

## The chart

A fitted model gives each design two kinds of coordinate. One number, the log of $V$, is its
energy differential (level offset) to the edge: how far above or below the edge it sits, in log
terms. The remaining $d-1$ numbers, for $d$ metrics, say where along the edge it
is, free of overall scale. Together they are a reversible rewriting of the metrics. Plot the
along-the-edge coordinates and you see the designs spread over the trade space; holes in that
picture are candidates for white space.

## The workflow

The method follows the stages of a trade study, and the package covers the last two.

1. **Sample** configurations. Any scheme will do; it may be sparse or biased.
2. **Evaluate** each configuration into attributes, with whatever model or test you have.
3. **Condition** the attributes into metrics. This is your job, done with ordinary scikit-learn
   tools: orient each so larger is better, make it positive, and scale it to a comparable spread
   about a chosen reference. Conditioning is part of the question you are asking; see the
   limitations.
4. **Identify**: fit `HyperbolicTradeSpace` to the metrics. It returns the weights, the offset, a
   reversible chart and diagnostics: how many designs carry the fit, and what fraction lie above
   the edge.
5. **Analyse**: read the tension, score designs for novelty, look for white space, predict where a
   proposed configuration would land, and plot. These tools are the analysis toolkit, described by
   concept here; their interface is documented in `api.md`.

## What the fit certifies

With one term the fit is a convex program and its answer is the minimizer. With several terms
($K>1$) the fit alternates between assigning designs to terms and refitting each term, and it
reports how far it got in three levels. The first is descent: no step made the objective worse.
The second is stationarity: each term sits where no further first-order improvement is available,
and the report gives the remaining gap for each term. The third is local optimality: if no design
sits exactly on the seam between two terms (the margin is positive), small changes to the terms
cannot change which term owns which design, and the fit is a local optimum; the report gives the
margin and the size of change that is safe. A status line says which levels you have: certified,
stationary without margin, or a stop at the iteration cap or on the guard, which the report names
and does not call converged. The statements and their conditions are in
[Mathematics](method.md#three-levels-of-guarantee).

## What you supply, and what you get back

You supply a table of designs and a rule for turning attributes into positive, larger-is-better,
comparably scaled metrics. You get back:

- the weights (the tension) and the metrics that participate;
- the exchange rates between contending metrics, as local trade-offs on the edge;
- for any design, its energy differential (level offset) to the edge and its position along it;
- for any design, how much a single metric alone would have to improve to reach the edge, and its
  projection onto the edge;
- a novelty score with a calibrated companion that respects the noise band;
- candidate white space, with the warning that holes may be structural, not opportunities;
- optionally, the edge written back in the original attribute units;
- predictions of where a configuration without measurements would fall, from a regressor fitted to
  the chart coordinates.

## What to keep in mind

The method reads the edge of the achievable region as a single flat surface in log space, tangent
at one balanced place. Away from that place our reading is that it is conservative; where the trade
space is not log-convex it cannot see the structure; where there are too few designs the weights
are weakly determined. The conditions behind each result are listed in
[Mathematics](method.md#conditions-of-the-theory), each with what it buys and what is lost without
it, and the Map and territory paragraph there says how to read results in light of them. Machine
verification confirms that the formulas follow from the stated conditions and that the code agrees
with them; whether the conditions are reasonable for your problem is a human judgement, and so is
whether a hole is an opportunity or a novel design is wanted.

For a worked case, see the case study page on a small-satellite attitude-control trade space,
where the fit is asked what contends and the answer is then explained in physical terms. For the
formulas, go to [Mathematics](method.md); for the limits, to
[Extensions and limitations](limitations.md); for the sources the method descends from, to
`literature.md`.

---
world: symbolic
---

# Preconditioning: from attributes to metrics

The identification stage of the method consumes a strictly positive matrix of larger-is-better
metrics and presumes nothing else (A1). Real evaluations produce attributes: masses in kilograms,
costs in dollars, error rates, margins, counts, quantities some of which are better when small. This
page is about the map between the two, stage 2 of the pipeline in [Mathematics](method.md). The
package does not decide that map for you; it supplies one tool, `LogAffinePreconditioner`, that
implements the family of maps the theory allows, and one function, `frontier_in_original_units`,
that reports the fitted frontier back in the units you started with. Everything below is therefore
about choices the analyst makes and what each choice costs, and it is organised around what the
theory asks of the conditioning and no more.

## What the theory asks of stage 2

Two properties are used, and they are the only ones. The conditioning must be log-affine per metric,

$$
\log m_j=\alpha_j\log(a_j+s_j)+b_j,\qquad \alpha_j\neq0,
$$
<!-- A4 -->

and it must give strictly positive larger-is-better metrics (A1, A4). Log-affine is what lets the
fitted frontier survive the change of units as a monomial (L9), and a nonzero $\alpha_j$ is what
makes the map invertible. The sign of $\alpha_j$ is the orientation: a negative $\alpha_j$ marks a
cost attribute, one where smaller is better (A4, L9). That the chosen $(\alpha,b,s)$ is *appropriate*
is posited, not derived; neither the lemma nor the package can tell you whether kilograms or the
logarithm of kilograms is the quantity a designer trades. The sections below are the choices.

## Orientation

Each column is either larger-is-better, orientation $+1$, or smaller-is-better, orientation $-1$.
The preconditioner computes $z_j=o_j\log(a_j+s_j)$ with $o_j\in\{+1,-1\}$, so a smaller-is-better
attribute is inverted in log space and comes out as a larger-is-better metric (A4, L9). The
orientation is a judgement about the problem, not about the data, and a wrong sign is not detected:
the fit will happily find a frontier of the wrongly oriented metric. The cheap diagnostic is the sign
of the exponent after the pull-back (below): a fitted exponent on a raw attribute that disagrees in
sign with what you believe about that attribute is a prompt to revisit the orientation.

## Shift and the reference point

Logarithms need positive arguments, and many attributes are nonnegative with a meaningful zero. The
shift $s_j$ moves the argument to $a_j+s_j$; it must be such that $a_j+s_j\ge0$, which the
preconditioner checks, raising `ValueError` with "Negative values in data" otherwise. A shift is an
analyst's decision about where the metric's scale begins, and it is not neutral: the same data
shifted differently give different log-spreads, different spread of the conditioned metrics and a
different frontier (A4 posits the map; it does not rank the choices). Use a shift when an attribute
legitimately reaches zero and a small positive offset is the natural unit of resolution, and leave it
at zero otherwise.

The *reference point* is the value of an attribute that maps to metric $1$. In the preconditioner it
is the centre removed by the scaler, stored as `log_offset_`. Why it matters: the metric vector
$m$ is positive and its frontier is a weighted geometric mean, and a common multiplicative rescaling
of all metrics shifts the log-score by a constant (L1, A2); but rescaling *one* metric changes the
geometry. Putting each metric on the scale where "1" means a typical, comparable level makes the
exponents comparable and makes the temperature, which is expressed in units of the log-spread of the
metrics, mean the same thing for every column. The reference point therefore also fixes what a
fitted $V=1$ means in practice: designs sit at $V\le1$ relative to a frontier measured against that
chosen scale (L1, A3).

## Scaling

After the logarithm, the preconditioner fits a scaler on the finite $z$ values of each column and
returns $m=\exp(\text{scaled }z)$. With `scaler="standard"` each metric has unit log-standard-deviation
over its finite entries; with `"robust"` the log interquartile range is normalized instead, which is
the better choice when a few extreme designs would dominate a standard deviation; with `None` the
metric is the pure power-law $m=e^{z}$ and the scale is whatever the attribute's units were. A
scikit-learn scaler instance is accepted if it is affine per column. The reason to scale at all is
the temperature: the soft maximum has temperature $\tau>0$ (A3) whose useful values are quoted in
units of the inverse log-spread (L5), so metrics with very different log-spreads make a single
$\tau$ soft for one column and hard for another. Equalizing the log-spread removes that. Scaling is
affine in log space, so it is within the family A4 allows and is inverted exactly.

The fitted pieces are `log_offset_` ($c_j$, the log value that maps to metric $1$) and `log_scale_`
($k_j$, log units per scaled unit); in the notation above $\alpha_j=o_j/k_j$ and $b_j=-c_j/k_j$
(A4, L9).

## Invertibility

Because $\alpha_j\ne0$ the conditioning is a bijection between raw attributes and log-metrics, with
inverse $a_j=\exp((u_j-b_j)/\alpha_j)-s_j$ (L9, A4). `inverse_transform` is exact up to floating
point, which the tests hold to $10^{-10}$ with mixed orientation and a nonzero shift. Invertibility
is what lets the analysis results be read in attribute units: a frontier target found in metric
space, a hole in the chart, a prediction, can be mapped back to something a designer can build or
measure (A4, L9). The chart of the identification stage is itself invertible (L8, A7), so the
composition from attributes to chart coordinates and back is lossless on the positive rows.

## Zeros and infeasible rows

A raw attribute exactly at $-s_j$ makes $a_j+s_j=0$ and its log is $-\infty$. The preconditioner
sends such an entry to the metric $0$, whatever the orientation, and ignores it when fitting the
scaler. That is the right convention for a larger-is-better attribute at its floor, and it matches
the estimator, which tolerates zero metrics: a row with a zero metric has $V=0$, no support weight and
no chart coordinates, and it is excluded from the objective (A1 is then relaxed from strictly
positive to nonnegative at the data level, with the zero rows carried as infinitely dominated). For
a smaller-is-better attribute, however, a raw value of zero is the *best* possible, not the worst, so
mapping it to metric $0$ is a defensible bookkeeping choice and not a statement about quality; if
that matters, shift the column so that zeros are not reached.

Infeasible rows are a different matter and are not the preconditioner's job. A design that violates
a constraint, fails to evaluate, or produces a nonphysical value should be removed before
conditioning, because the frontier is a statement about the admissible region (A1) and an infeasible
design is outside it by construction. Dropping rows on the basis of the attribute values themselves
is a selection and changes what the identification stage can say; a common case is to filter on
feasibility first, then condition the survivors, so that the fitted scale and the log-spread
describe feasible designs only. If a column is entirely at its floor there is nothing to learn from
it and the preconditioner falls back to the identity scaling for that column.

## Diagnostics

A conditioning is judged by what it does to the metrics and by whether the story it tells is
sensible. Four checks, none of which proves the conditioning is right (A4 is posited):

- *Unit log-spread.* After `"standard"` scaling, `np.log(M).std(axis=0)` is one in every finite
  column. If it is not, a column has zeros or a degenerate range.
- *Round trip.* `inverse_transform(transform(X))` should return `X`; this is the invertibility
  statement (L9).
- *Sign of the pulled-back exponents.* The raw-attribute exponent is $w_j\alpha_j$ (L9). With
  $w_j\ge0$ on the simplex (A2), its sign is the orientation; a surprising sign is a prompt to
  revisit the orientation or the shift.
- *Sensitivity of the answer to the choice.* Because the choices are not derived, the honest check is
  to refit under a second reasonable conditioning (for instance the other scaler, or a modest change
  of shift) and see whether the participating metrics, the contending set and the tension directions
  of the tension report move. Where they move, the finding depends on the conditioning and should be
  reported that way. The temperature is the other setting that is expressed in conditioned units;
  `select_temperature` chooses it by the fraction of designs above the frontier (L5) and so the
  answer is conditional on the conditioning too.

## The pull-back to attributes

Once the estimator is fitted on the conditioned metrics, the frontier can be written in attribute
units. Starting from $\log V=w\cdot\log m-\beta$ (L1) and substituting $\log m_j=\alpha_j\log(a_j+s_j)+b_j$
(A4), the simplex constraint $\sum_jw_j=1$ (A2) lets the offset $\beta$ be absorbed through the
invariant form, and the result is

$$
V=e^{\,w\cdot b-\beta}\prod_{j=1}^{d}(a_j+s_j)^{\,w_j\alpha_j}.
$$
<!-- lemma: L9 -->

Said in words: the frontier remains a monomial, now in the raw attributes, with exponents $w_j\alpha_j$
and a log constant $w\cdot b-\beta$ (L9). A negative exponent marks a cost attribute. The function
`frontier_in_original_units(estimator, preconditioner)` returns exactly this as a dictionary:
`exponents_orig` ($w_j\alpha_j$), `log_const` ($w\cdot b-\beta$) and `shift` ($s_j$); evaluate
`log_const + exponents_orig @ log(X + shift)` to get $\log V$ for raw attributes, which equals the
`score_samples` of the preconditioner-then-estimator chain on the same rows. The test suite checks this
agreement numerically. It needs a single-term fit: for $K>1$ the extension replaces the monomial by a
softmax-affine function (L10), which is not a monomial in the attributes, so the closed form does not
apply. Note also that the reading of the exponents as exchange rates (L7, R1) is a reading in
*metrics*; in attribute units the elasticities along the frontier are rescaled by the $\alpha_j$.

## A worked case in general terms: the nine-attribute cubesat

The cubesat tradespace in the case studies has nine attributes of mixed orientation: some are
larger-is-better (capability measures, margins), some are smaller-is-better (mass, power draw, cost
and similar), and they span very different units and orders of magnitude. The route through this page
is the following, and it is the general route for any such case.

1. *Filter on feasibility.* Designs that violate a requirement or fail to evaluate are removed first,
   so that every survivor has strictly positive attributes (the admissible region of A1 is what is
   left) and no floor-valued entries need the zero convention above.
2. *Orient.* Give the smaller-is-better columns orientation $-1$ and the rest $+1$ (A4). With nine
   columns the orientation is a vector of nine signs, one per attribute, not a scalar.
3. *Shift and scale.* A zero shift suffices when every attribute is strictly positive; use `"robust"`
   scaling if a handful of extreme designs dominate the spread. The scaler gives each of the nine metrics
   the same log-spread, which is what makes one temperature meaningful across them (A3, L5).
4. *Fit and tune.* Fit the estimator on the nine conditioned metrics, choose $\tau$ by
   `select_temperature`, and read the tension report: which metrics participate, which are free, the
   contending set (an $n$-lemma of whatever size $n$ the data support, at $\tau=\infty$ with
   `min_exponent = 0`, L3), the exchange rates (L7) and the principal tension directions.
5. *Pull back.* Convert the participating exponents to raw attributes with
   `frontier_in_original_units` (L9); a smaller-is-better attribute will carry a negative exponent
   and the others positive.

Nothing about the nine-attribute case is special to the package: it is the same two choices (orientation,
scale) applied nine times. What it exercises is the discipline of doing them explicitly and then
checking that the findings survive a reasonable alternative.

## Conditions under which these tools mislead

- The conditioning is posited (A4). Different defensible orientations, shifts or scalers give
  different frontiers; the tools make the choice explicit, they do not make it correct.
- The interpretation of the exponents as a facet normal and exchange rates rests on the balanced
  point lying in the relative interior of a facet with a positive normal (R1). Where it does not, the
  exponents are not unique and some exchange rates are undefined (L3, L7, R1).
- Sub-populations with different frontiers (strata) mixed in one fit produce a single frontier that
  fits none of them; condition and fit within a stratum, or compare strata, rather than mixing them.
  This is a limitation of the method, discussed in [Extensions and limitations](limitations.md).
- A tension is a binding constraint, not a correlation; the closure effect makes some negative
  association among participating metrics unavoidable near the frontier, so read it alongside the
  exponents (see the tension report in [API](api.md)).
- The pull-back is of a single-term fit only (L9); the posynomial extension does not admit the same
  closed form (L10).

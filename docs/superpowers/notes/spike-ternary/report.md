# Spike: ternary plots for reading tensions (2026-11-09, the driver)

Asked by the supervisor while reading section 9: "i want you to do a pass to explore the use of
ternary plots ... i think we could use something more intuitive to help with under standing
tensions. do a research spike then give me a readout on whether this will help us and how". Tool he
pointed to: mpltern (https://mpltern.readthedocs.io). Throwaway script: `make_ternary.py` beside
this file (run with `uv run --with mpltern`; mpltern 1.0.5 works with the locked matplotlib and is
not a project dependency). Figures A to D beside it. Nothing in the package or the paper changed.

## Why a ternary plot is native to the method, not decoration

1. **Exponents live on a simplex** (axiom A2). For three metrics the ternary diagram *is* that
   simplex. The n-lemma is the face of the simplex that carries the exponent vector: a corner is one
   binding metric, an edge is a dilemma, the interior is a trilemma. A zero exponent sits on the
   boundary, where no logarithm is needed.
2. **Exchange rates are read off position.** The rate between metrics i and j is w_i / w_j, the ratio
   of two barycentric coordinates. Taking any three metrics and renormalizing (a sub-composition)
   keeps every such ratio, so a three-metric ternary shows true exchange rates among those three.
   It must say what share of the facet's weight those three carry.
3. **Grouping is exact for exponents.** With metrics in groups g, V = prod_g M_g^{W_g}, where
   W_g is the sum of the group's exponents and M_g the group's weighted geometric mean. So a
   three-group ternary of ten metrics is exact for where the weight lies. It hides tensions inside
   a group, and M_g differs from facet to facet.
4. **Designs.** The chart's position Z = B log m is the log-ratio coordinate of the closed
   composition of the metrics. For three metrics a ternary of the (centred) metric compositions is
   the chart's position plane with labelled corners. The energy differential is the direction the
   ternary removes: it has to be colour, or left out.

## What the figures show

- **A, planted table, three metrics, three facets.** Left: the three fitted exponent vectors land on
  the planted ones; one facet is on an edge (a dilemma), one near an edge, one in the interior (a
  trilemma). Right: the near-frontier designs fall into three regions by facet. This is the idea of
  the method in one picture, with axes a reader can name.
- **C left, cubesat, the three metrics both regimes share.** Two of the three facets and the stock
  regime sit on the slew-time and control-effort edge; the third facet sits on the slew-time and
  pointing-error edge; the one-facet fit of the primary regime is in the interior between them.
  "One facet blends what three separate" is visible at a glance. The legend prints the weight these
  three metrics carry on each facet (0.83, 0.54, 0.27): the third facet is mostly about other
  metrics, and the picture has to say so.
- **B left, cubesat, ten metrics in three groups** (performance, energy, mass; the grouping is the
  analyst's). The stock regime and two facets lie on the performance and energy edge: mass does not
  contend there. The dominant facet and the primary one-facet fit are pulled toward mass.
- **D, 40 resamples of the three-facet fit.** Two facets are tight; the dominant facet smears along
  a line (its mass share is not firm). Stability shown in the same picture as the reading.
- **Not useful:** B right (the temperature path collapses under grouping); C right (cubesat designs
  in a three-metric sub-composition do not separate by facet: ten-dimensional positions do not
  survive the projection, and only 4, 6 and 35 designs are near the frontier).

## Limits

Three parts only: ten metrics need a sub-composition or a grouping, and both are choices that can be
cherry-picked (120 triples). The level is not shown. The triangle is not the log-ratio geometry:
it is for reading, not for measuring distance. Clouds need centring and scaling to fill it. Some
readers have never read a ternary diagram and need a one-line key.

## Readout

It helps, in three places, and should not be used in two.

1. **The picture of an n-lemma** (figure A): for the paper's concept figure or section 4, and for
   the docsite's Tensions page. It gives "dilemma" and "trilemma" a literal place.
2. **Section 9, in place of or beside the three heatmaps of Figure 6** (which a reviewer measured as
   illegible): the exponent ternary on the shared metrics (C left) and the grouped one (B left).
3. **Appendix D, stability** (figure D).
4. Not for cubesat designs, and not for the temperature path in grouped form.

Cost: one plotting helper for exponent vectors on a ternary (three named metrics, or three named
groups; prints the weight carried), mpltern as an optional plotting dependency, a contract amendment
for the new public name, and three short algebraic facts (the face reading, ratios kept by
sub-compositions, exponents adding over groups) that could each be one scripted step.

## Addendum (2026-11-09): lines of equal V on the triangle

The supervisor's question: can lines of equal V (or equal log V) be drawn on the triangle, to show
how the triangle maps to the method. Script: `make_why4.py`. Figures: `why4-A-lines-on-regions.png`,
`why4-B-lines-only.png`, `why4-C-designs-by-logV.png`, `why4-E-log-ratio-plane.png`; side by side at
`mock/lines.html`.

**The identity.** Every exponent vector sums to one, so with t the mean of the log metrics (the
overall level) and p = u - t the position,

    log V(m) = t + h(p),    h(p) = max_k (w_k . p - beta_k).

Checked on the planted table against `score_samples`: largest difference 4.4e-16. The triangle shows
p and drops t. So V is not a function of the position (figure C: designs at one position carry
different V), but its level lines are: h = const is the line of equal V among designs at one overall
level, the same family at every level. Read the other way, the frontier V = 1 sits at the level
t = -h(p) over each position, so the same lines are a contour map of the frontier.

**What the lines show.**

- They bend exactly at the borders of the regions (A, B): a region is where one facet attains the
  maximum, and the lines are that facet's.
- In log-ratio coordinates (E) the method is straight: each region is a polygon, and its lines are
  parallel and evenly spaced, normal to w_k - 1/d. The spacing for a step of 0.25 in log V is
  0.25 / |w_k - 1/d|: 0.47 and 0.42 in the two-metric regions, 1.09 where all three trade. Uneven
  exponents give tight lines; a facet with equal exponents would give none (V would depend on the
  level alone).
- On the triangle itself the lines curve and crowd toward the edges. That is the closure, not the
  method (the Limits above: the triangle is for reading, not for measuring).
- No interior peak on this table: 1/d is outside the hull of the three exponent vectors, so V at
  one level rises all the way toward metric 3 (its exponent is the largest in two facets).
- A drawing as a solid (the triangle as floor, the level as height, the frontier as a roof of three
  flat faces, log V as the gap under it) was tried and dropped: the roof hides the designs.

**Use.** For the index page the lines crowd the image the supervisor chose (mock:
`mock/index-lines.html`); the driver's view is that they belong one level down, in the paper's
section on the chart or the docsite's theory page, as B or E, where "position and level" is the
point being made. Three scripted steps would back them: exponents sum to one, the split of log V,
and the normal of a facet's lines.

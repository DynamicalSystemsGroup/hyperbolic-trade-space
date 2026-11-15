# WP50 D-1: the objects, and what near means in the chart

Read 2026-11-14 at `dev` a1879e6. Serves G1. Numbers marked (instance) are in `instance/out/results.json`, produced by
`instance/instance.py` and read in `instance.md`. The word *white space* is 0.1's; *hole* is the reserved word and is used
here only for the object this spike defines.

## The two aims, as the frame

The search has two aims, in the supervisor's words (`WP50-decisions.md`, 22:25): "find and where possible characterize and
potentially 'fill in' holes within the envelope, and push the envelope". He calls them "fundamentally complementary" (22:27).
Everything below serves the first aim; the second (pushing the envelope, the level `log V`) enters only where the two share a
coordinate.

## What a point is

A point is a design as the chart of Section 4 places it: its position `Z` in `R^(d-1)` (the sum-zero log-ratio coordinates,
free of overall scale) and its level `log V`. L8 (`derivation/lemma_08_helmert_chart.py`) gives the map between log metrics `u`
and `(Z, log V)` as a bijection. Three facts of the code matter for what follows (all read in `estimator.py` and
`coordinates.py`, and checked in the instance):

1. `Z = u B^T` with `B` the Helmert basis, fixed by the data's dimension `d` and not by the fit. A refit leaves every `Z`
   unchanged (instance: maximum change 0.0 between the K = 2 fit on all rows and the K = 2 fit on a random half). Only the
   level moves with the fit (instance: largest change 0.066 on the case, `log V` in `[-2.42, 0.39]`).
2. `log V` is `ell + g(Z)`, with `ell` the mean of `u` and `g` fixed by the exponents: at K = 1 an affine function of `u`; at K = 2 the soft maximum of two affine scores, so
   piecewise-affine, with a seam where the two terms trade places.
3. A unit change in one metric (`m_j -> c m_j`) translates `u`, hence translates the chart. Distances between designs in
   the chart do not change (instance: 2.7e-15 over 300 designs). Distances between the raw metrics change by a factor from
   0.018 to 40 for the same unit change, so which designs are nearest in the raw metrics depends on how someone chose the
   units. That is the first reason the chart, and the logarithm under it, is the place to ask what is near what.

## Candidate distances

Let `a = (Z_a, l_a)` and `b = (Z_b, l_b)`, with `l` the level `log V`.

| Candidate | Formula | What a hole is under it | What it does and does not see |
|---|---|---|---|
| Position | `norm(Z_a - Z_b)` | A region of positions with no design at any level | Level-blind. Invariant under refits (fact 1), so a hole of the position distance does not move when the fit changes. It cannot see a gap in level at a position that is occupied |
| Chart | `sqrt(norm(Z_a-Z_b)^2 + s^2 (l_a-l_b)^2)` | A region of the `(d)`-dimensional chart with no design, a tunnel in `Z` through all levels or a pocket within them | One free number `s` (the level weight). The diagram depends on it (instance: at s = 0, 0.5, 1, sqrt(3), 2 sqrt(3) the planted table has 2, 2, 3, 0, 0 classes above the null; `instance.md`) |
| Log metrics | `norm(u_a - u_b)` | Same as the chart distance at the one `s` that makes the chart an isometry | At K = 1, `(Z, sqrt(d)(l - w.B^T Z))` is an isometric copy of the log metrics (instance: error 3.6e-15). The unsheared chart distance is between 0.57 and 1.01 of the log-metric distance (instance), so `s = 1` is not the isometry |
| Across the seam (K >= 2) | Euclidean in the chart, or the shortest path along the surface | Same as the chart distance, with the kink of the surface counted or not | `log V` is a Lipschitz function of `Z` (slope `norm(B w_k)` per term); on the case the slopes are 0.54 and 0.35, so a chord of the chart between two points is at least 0.88 of the path along the surface, and the path is at most 14 percent longer (instance, `chord_over_path_bound`) |

Two points follow. First, a metric across a seam needs no special construction here: the chart is one coordinate system on
both sides, `Z` is smooth across the seam, and only the level is kinked, by a bounded amount. Second, the choice that
matters is `s`, the weight of the level against the position, and it is a modelling choice with a reason either way: the
level is where the second aim lives (pushing), the position is where filling in lives.

## Against doing it in the raw metrics

Three reasons, each checked or derived:

- **Units** (above): the raw nearest-neighbour structure depends on the units of each metric; the chart's does not.
- **Shape of the frontier**: in the raw metrics the K = 1 frontier is the hyperbolic surface `prod m_j^{w_j} = e^beta`,
  curved; in the chart it is the plane `l = 0` and, at K = 2, a piecewise-flat sheet. A ball of the raw metric sitting on
  the frontier mixes a distance along the surface with a distance off it, so a "hole near the frontier" has no clean
  meaning; in the chart the distance along the surface is `norm(Z)` and the off-surface distance is `l`.
- **Scale and position are separated**: a design twice as good on every metric moves only in the level, not in position
  (L8, `Z(u + c1) = Z(u)`). Holes of position are therefore holes in which trade-off ratios have been tried, and holes of
  level are holes in how good the design at a ratio was; the two are different statements about the search.

What the chart does not do: it does not make the sample dense. A chart is a coordinate system; whether a region is
unsampled is read from the data.

## What each choice does to a hole

A hole under a distance is a class of the persistence diagram of the complex built on that distance (`construction-and-tools.md`),
located by the circumcentre of the simplex that kills it. Two consequences:

- **The position distance finds holes of trade-off ratios.** A loop around an unsampled disk of `Z` at every level. In the planted
  instance the diagram and the circumcentres find both planted disks, to within 0.04 of their centres (instance).
- **Adding the level (the chart distance) can lose them.** At `s = sqrt(3)` the same planted disks are no longer above the hole-free null,
  because stretching the level axis thins the sample in the stretched dimension and raises the null's longest loop. This
  is a statement about the null as much as the hole: the null threshold is recomputed at each `s` (instance).
- **The frontier is the boundary of the sample, and persistent homology does not see a gap that opens to the outside.** A
  region of the near-frontier surface cut into the sample from the frontier side (a bay) is homologically a disk, not a
  loop, so it is not a class (by construction; not measured in the instance). A hole of the persistence diagram is a gap enclosed by designs. White space that is a bay
  (open towards the edge of the sample) is invisible to degree 1 of the plain construction; the fence in the sensor-coverage
  work (de Silva and Ghrist 2006, 2007) is the remedy for it, and is the first thing a build would have to decide
  (`readout.md`).

## Why the piecewise-affine chart is the natural place

The chart is the one coordinate system in which (i) distance does not depend on units, (ii) the frontier is flat so that
along and across are separate axes, (iii) position is fit-independent, so a hole of position survives refits by
construction, and (iv) the same construction works at any K, because K only changes the level. Doing the same in the raw
metrics loses all four.

## References

All resolved; see `construction-and-tools.md` for the list with dates read.

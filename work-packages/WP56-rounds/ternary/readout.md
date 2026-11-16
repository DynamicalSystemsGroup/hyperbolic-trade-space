# WP56 spike: the fleet-performance aggregate and the decision-maker's ternary

Script `examples/adcs/spikes/fleet_performance.py`; numbers in `fleet_performance.json` beside it. Data: the
primary regime (the table Section 9 reads; 2,134 feasible designs, fleet size 1 to 30, pointing error up to 0.0086
degree). Corners: fleet cost (sponsor), unit cost (manufacturer), fleet performance (operator). Costs conditioned
as the case conditions them. Fit at K = 1 and K = 2, the case's temperature rule, band 1/tau of the K = 1 fit.

Fleet cost is exactly fleet size times unit cost and each aggregate is a function of fleet size and pointing
error, so it is partly recoverable from the two costs: the unit-cost exponent at K = 1 is 0.006, 0.053 and 0.000 in
(a), (b), (c), and the frontier lies on the fleet-cost to performance edge.

## The three definitions

n fleet size, e pointing error (degree), e_req = 0.008495 degree, the case's pointing requirement.

| | formula | units | constants (reading) | assumes | place in the SysML v2 model |
|---|---|---|---|---|---|
| (a) coverage | 1 - (1 - p(e))^n, p(e) = p0 exp(-e/e0) | probability | p0 = 0.2 (one satellite's chance of covering the target set in the period at zero error); e0 = e_req (error at which that chance falls to 1/e) | independent satellites, one target set | derived attribute of the fleet, from `fleetSize` and the pointing error |
| (b) capacity | n/(1 + n/n0) * e0/(e0 + e) | satellite-equivalents | n0 = 10 (fleet size at half the ceiling); e0 = e_req | a ceiling on useful satellites; pointing a separate factor | derived attribute of the fleet |
| (c) refresh rate | 1/(t0 + T1/(n w(e))), w = exp(-(e/ew)^2) | refreshes per day | n0 = T1/t0 = 10 (single-satellite revisit time over latency, t0 = 1 day); ew = e_req | a latency floor; pointing erodes the footprint | derived attribute from revisit time, latency and pointing |

Each increases in n with diminishing returns and falls with e. The footprint geometry behind (c)'s pointing term:
Wertz, "Space Mission Geometry", https://doi.org/10.1007/978-94-011-3794-2_5 (DOI resolved; chapter not read in full).
The latency form is the analyst's composition. Constants that only scale an aggregate (t0, a unit) are absorbed by
the conditioning.

## The fits

Exponents (fleet cost, unit cost, performance); elasticity of the fleet-cost metric with respect to the performance
metric, conditioned units; association among near-frontier designs (fleet cost / performance, unit cost /
performance).

| | band, near-frontier | K = 1 exponents | elasticity | contending | association | K = 2 term 1 (share) | K = 2 term 2 (share) |
|---|---|---|---|---|---|---|---|
| (a) | 0.029, 176 | 0.386, 0.006, 0.608 | -1.58 | performance, fleet cost, unit cost | -0.995, +0.358 | 0.140, 0.000, 0.860 (0.93); elasticity -6.13 | 0.537, 0.000, 0.463 (0.07); -0.86 |
| (b) | 0.038, 190 | 0.452, 0.053, 0.495 | -1.10 | performance, fleet cost, unit cost | -0.990, +0.311 | 0.368, 0.094, 0.539 (0.73); -1.47 | 0.544, 0.000, 0.456 (0.28); -0.84 |
| (c) | 0.026, 195 | 0.418, 0.000, 0.582 | -1.39 | performance, fleet cost | -0.997, +0.681 | 0.317, 0.000, 0.683 (0.87); -2.15 | 0.495, 0.000, 0.505 (0.13); -1.02 |

Every fit has one dominant region and a thin second; fleet cost and performance trade in every term (association below
-0.93); the unit-cost association with performance is positive at K = 1 (0.31 to 0.68), near zero in the dominant K = 2 term
and positive (0.44 to 0.60) in the thin one.

## Figures

- `coverage.png`: (a) at K = 2; designs spread along the fleet-cost to performance edge, term 1's star near the performance corner, term 2's diamond halfway up that edge.
- `capacity.png`: (b) at K = 2; term 1 reaches into the interior (unit-cost exponent 0.09), the boundary bends.
- `revisit.png`: (c) at K = 2; both markers on the fleet-cost to performance edge, the boundary running straight from the unit-cost corner to term 2's marker.

## The decision's stability

Section 9's rules on each three-metric fit: the shortlist is the six-requirement designs (548) inside the band of both fits.

| rule | (a) design, fleet size | (b) | (c) |
|---|---|---|---|
| shortlist size | 41 | 53 | 61 |
| sponsor (least fleet cost) | 766, 6 | 913, 4 | 190, 5 |
| manufacturer (least unit cost) | 702, 20 | 2697, 24 | 982, 23 |
| operator (best performance) | 299, 21 | 1274, 20 | 982, 23 |
| between (smallest larger shortfall) | 1590, 16 | 1225, 13 | 1001, 15 |
| balanced between the terms | 1590, 16 | 2477, 12 | 1001, 15 |

No rule picks the same design under all three. The aggregates rank the 2,134 designs alike (Spearman 0.98 to 0.99)
but the shortlists, a thin band of 41 to 61 designs, overlap by 16 to 22 designs (unions 72 to 98) and the top five
by level share none. Varying each constant by a factor of two each way (four variations per aggregate) changes the pick
in 15 of 20 rule-variations for (a), 15 for (b) and 18 for (c): the constants move the pick as much as the definition.
At the coarse reading the rules keep their character over the 15 fits: sponsor 3 to 11 satellites, manufacturer 19 to 28,
operator 18 to 28, between 9 to 16.

With Section 9's shortlist held fixed (its 13-metric fits), only the aggregate moves: the operator's pick is one of two
designs over the 15 evaluations (2356: 25 satellites, medium wheel and tracker, 11 times; 2826: 16 satellites, fine tracker, 4 times) and
the in-between pick one of four (fleet size 6 to 12). Section 9's own picks with pointing error as the operator's
measure are 2950 (6 satellites, fine tracker) and 1858 (5, fine tracker). The aggregate rewards fleet size, so the
operator's pick moves to larger fleets.
The stock-gain regime agrees in kind: sponsor 3 to 4 satellites, operator 20 to 28, between 11 to 14.

## Recommendation

Carry (a), coverage probability, into the SysML v2 model. The argument is modelling: it is the quantity an operator
holds for a coverage problem (the chance a target is covered in the period); it needs the fewest constants, each with an
operational reading (a satellite's chance at perfect pointing; the pointing error that cuts that chance by 1/e), and the
second is anchored on the requirement already in the model; it is bounded, so it cannot be mistaken for a count. (b) has
no operator reading for its ceiling n0. (c) asks the SysML v2 model for revisit time, latency and a footprint law, more
detail than was asked for. Stability does not separate them: the pick moves about as much for each. The cost of (a) is saturation:
it reaches 0.998 at the largest fleets.

## What the data cannot settle

The constants and the target set are mission assumptions the data of record do not carry; the design-level pick moves
with them as much as with the definition, so the stable content is each rule's character, not one design, until the
operator supplies them.

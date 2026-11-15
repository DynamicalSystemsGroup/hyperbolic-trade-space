# Note: the kernel direction, its class and its boundary (WP43)

For the glossary's "kernel direction" entry to cite. One page; the evidence is in
`work-packages/WP43-rounds/spike/readout.md`. A definition with two convexity facts, not a new result.

## The class

Write `u = log m`. A **log-convex invariant form** is a score `log V(u) = f_theta(u)` with parameters `theta` in a
convex set `Theta` such that

1. `f_theta(u)` is affine in `theta` for each `u` (the parameters enter linearly);
2. for each `theta` in `Theta`, `f_theta` is convex in `u`;
3. `f_theta(u + s 1) = f_theta(u) + s` (degree-one homogeneity: the shift along the diagonal moves the level by `s`,
   so the chart `[Z | log V]` and its closed-form inverse carry over unchanged).

Members: the monomial `w.u - beta` (`w` on the simplex); the log-quadratic term
`w.u + (1/2) u'Qu - beta` with `Q` positive semidefinite and `Q 1 = 0` (the translog form of Christensen, Jorgenson and
Lau 1973, 10.2307/1927992, with its curvature and homogeneity restrictions); a nonnegative combination of convex
features with the weights in a convex set. The finite maximum of members, and the soft maximum `(1/kappa) log mean exp`
of members, are convex in `u` and homogeneous, so they score as members, but their parameters no longer enter
linearly: the fit of a maximum of several members is the partition-and-refit scheme (a local optimum), as for `K > 1`.

## The two facts

- **The fit is convex in the parameters.** For a member, the entropic soft maximum of `f_theta(u_i)` over the rows is a
  log-sum-exp of functions affine in `theta` (convex: Boyd and Vandenberghe 2004, 3.1.5 and 3.2.2), and the mean of
  `f_theta(u_i)` is affine in `theta`; so minimising their difference over `Theta` (the mean-slack fit; at `tau = inf`
  the maximum over rows, a pointwise maximum of affine functions, 3.2.3) is a convex program. For the monomial this is
  L4 (convexity of `J_tau`) and, with the simplex constraint, the geometric program of Boyd, Kim, Vandenberghe and
  Hassibi 2007; for the log-quadratic term it is a semidefinite program.
- **The designer's problem is convex in the log-metrics.** `{u : f_theta(u) <= 0}` is convex, so a constraint
  `V <= 1`, and any objective convex in `u` over it, is a convex program in `u`: the form of a geometric program
  without the posynomial (Boyd et al. 2007; Agrawal, Diamond and Boyd 2019, 10.1007/s11590-019-01422-z, call such
  functions log-log convex in the metrics).

## Which word

A generalized posynomial in `m` has `log f(e^u)` growing at most linearly in `u` (a posynomial's does; sums, products,
positive powers and maxima keep it linear), and `w.u + (1/2) u'Qu` with `Q != 0` grows quadratically. So the
log-quadratic term is in the class and **not** a generalized geometric program in the metrics: "GGP" names a proper
subclass, "log-convex" (in the log-metrics, as assumption (vi) of the paper already says) names the class.

## The boundary

No member represents an edge whose region is not convex in `u` (a dent or notch in the edge): `{f_theta <= 0}` is
convex for every member and for every maximum of members, so such a surface passes over the notch, and the rows under
it are slack (WP43 readout, boundary section).

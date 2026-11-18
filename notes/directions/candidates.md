# Candidate directions (not yet spiked)

Ideas the supervisor has raised that are research directions, each with his words verbatim and the date, kept here
until one becomes a spike with a readout in this folder. Not commitments; not for the 0.1 release.

## Learning the invariant rather than the trade (the supervisor, 2026-11-16 16:06 EST, verbatim)

"i also think it would be a good idea to figure out how to use our approach to find patterns like this. they showed up
in the automated market maker work we did as well. constant product market makers have exactly this shape in their
data. in order to learn this we'd need a form factor that could find variables in the data that could be the invariant
rather than the trade"

Context: the grain, straw and biomass case of the wheat example (both yields rise with biomass; at a fixed biomass they
trade), where the fit put exponent 0 on the derived metric and the level V played the size. The driver's reading of
the direction: the same posynomial form with a second estimator. The frontier fit finds the exponent vector by a
one-sided objective (the entropic soft maximum: the data lie below the level set). A conserved quantity is found by a
two-sided objective: within a group of rows that share the invariant (one pool between liquidity events; one
plot-year's management regime), the monomial m^v with the least variance of log V is the invariant, and the directions
of large variance are the trades along its level set. For a constant-product market maker the data lie on the level
set x y = k, so v = (1, 1) has zero within-pool variance and (1, -1) carries the trading. Candidates for a spike: the
estimator (least within-group variance in log space, with the group structure as an input or found by clustering of
levels); how it relates to the fit (the frontier is the invariant of the best rows; a conserved quantity is the
invariant of every row); K > 1 (a sum of monomials as the invariant, as in stable-swap market makers, which the
posynomial form carries); the tests (planted invariants recovered; the wheat and a market-maker table); what the
package would expose. Related: the dependence screen among metrics at conditioning and the size-against-shape plot
(`work-packages/WP70-decisions.md`, 2026-11-16), both the driver's suggestions from the same conversation.

## The separability formulation and the roadmap (the supervisor, 2026-11-16 17:19 EST, verbatim)

"as for the estimator that finds invariants. the thing i was thinking could work is something like a separability
approach where V (x) = posynomial(x)  AND V (x) = Ax

this would mean the the level set was explained twice, in our case with different variables. one affine and one
hyperbolic. the low dimensional case being `biomass = wheat * straw`, which is a contant product invariant, but with
the invariant level sets being a different variable. the generalization being affine on one side and posynomial on
the other.

like with our earlier work this should start with the monomial case, and a scalar. but we should explore
generalizations. this should be viewed as a research roadmap and the any new features in the estimator should come in
0.2 or later"

Reading: the level explained twice, posynomial in one block of variables and affine in another, agreeing row by row;
first the monomial with a scalar affine side (w . log x = log(a y + b); at b = 0 the statistic is the correlation of
log V with log y, 0.99 for wheat with y = biomass, `WP71`); then a vector y, several terms, several outputs. WP72's
spike (`work-packages/WP72-rounds/readout.md`, `git show 4f81a4ea:work-packages/WP72-rounds/readout.md`) is stage 1 of this roadmap; the estimator's features enter the package
at 0.2 or later, never 0.1.

**His addition (17:20 EST, verbatim):** "it could end up being a different approach but between the market makers and
the biology examples (and likely others in real life to be found)"

The driver's reading: the separability formulation is a hypothesis, not a design; the spike that follows WP72 keeps
the approach open (the two-sided within-group estimator, the two-view formulation, or something else) and is judged
on the cases: the market makers as internal test cases, the biology examples (wheat; the amniote life histories are a
candidate, with body mass as the size), and other real-life tables the spike looks for.

**His note on the formulation (17:27 EST, verbatim):** "since we're working with nonnegative values (the posynomials)
you may also want to explore semidemifinite cone programs or precisely striclty positive definite cone programs.
otherwise i think you just end up with Linear programs (equality constraint formulation) on the affine side. seems like
a lot of potential for weird fits. but a lot of it should be on the analysis or modeler since this is essentially
choosing kernels"

The driver's reading: the affine side over nonnegative data is a conic problem, not a plain linear program with
equality constraints (the positive orthant at least; a positive-definite cone where the affine side is a quadratic
form), and the spike should write it that way and look at what each cone admits and refuses; degenerate fits are
expected and must be reported, not hidden; which variables sit on which side, and in what form, is the analyst's
choice, as a kernel is: the package supplies the estimator and the diagnostics, the modeller the blocks. Consistent
with the package's line that conditioning is the analyst's job and that kernel methods are documented extensions
compatible with generalized geometric programming.

## Solvers: cvxpy demonstrates feasibility, never a dependency (the supervisor, 2026-11-16 ~22:30 EST, verbatim)

"they are slow because you are using cvx rather than a custom solver. cvx is good to demonstrate feasibility but not as
a dependency"

Applied as: the WP43 timings (40 to 80 s a log-quadratic fit, 200 to 260 s with the tau bisection) are the spike's
cvxpy formulation, not the model's cost, and are not quoted as such. The pattern is the monomial's: a spike proves the
program convex and feasible with cvxpy; the package then solves it with its own routine on numpy and scipy, as the
monomial fit does with `solve_lp` and `solve_slsqp`. The log-quadratic fit is a smooth convex objective over a cone of
small dimension (Q is d by d, 13 by 13 on the case), so a projected first-order or Newton method with the eigenvalue
projection onto the semidefinite cone keeps Fact 1 and the core install (numpy, scipy, scikit-learn). The conic
dependency list in the WP43 readout (cvxpy, clarabel, scs, osqp, qdldl, highspy) is the spike's environment, not a
lock need; the readout's section 5 is read with this ruling. The same rule governs the separability estimator's affine
side: the cone is written in cvxpy to find out what it admits and refuses, and the package gets its own solver.

## From the external review of 2026-11-16 (0.2 or later)

Packaging: widen the Python range with a CI matrix; `plotting` as an extra behind a lazy import; sympy out of the runtime dependency set once `derivation/` has its own environment. Model: the standard library's MoE and MoP metadata in place of the `doc` first-word mark; `variation`/`variant` and the library's `TradeStudy` for the alternatives; both belong to the model-focused project (ADCS-lifecycle-demo) as much as to this one. Record: `work-packages/review/external-review-2026-11-16.md`.

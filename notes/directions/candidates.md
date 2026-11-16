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

# WP72 — Decisions: learning the invariant rather than the trade (a research spike)

## His direction (16:09 EST, 2026-11-16, verbatim)

"we have two different scopes now. one is to simply update the broadbalk wheat example so it calls out the
observation that the V levels correlate strongly with biomass which is cool and intuitive but bounded. the other is a
research spike on a variant of our method that can find this pattern which we can test out on the wheat example but
also on public uniswap data (which i am pretty sure i have access to from a github model i made many years ago)"

Earlier the same day (`notes/directions/candidates.md`): "i also think it would be a good idea to figure out how to
use our approach to find patterns like this. they showed up in the automated market maker work we did as well.
constant product market makers have exactly this shape in their data. in order to learn this we'd need a form factor
that could find variables in the data that could be the invariant rather than the trade"

## WP72 approved as proxy (16:09 EST)

`WP72-scope-of-work.md` (stage 1, a research spike: the estimator for a conserved monomial or posynomial, planted
tests, the wheat table, a public constant-product market-maker table, a readout that says what the method variant is,
what it found and what the package would expose) is approved by the driver under his mandate on the direction above.
One unit on branch `wp72`, nothing in `src/` or the docs. The Uniswap data: the unit looks for an open public table
first; his own GitHub model from years ago is a source he may point the unit to when he is back (an open question
held, not blocking).

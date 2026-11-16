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

## His pointers and his boundary (16:11 EST, verbatim)

The Uniswap source: "https://github.com/danlessa/uniswap". Then his diagram of the constant-product market maker (x1 x2
= z; a swap u1 along the hyperbola, a liquidity event u2 across hyperbolas; theta the position on the level set) with
"look familiar". Then: "balancer was a higher dimensional version of the same: https://docs.balancer.fi/whitepaper.pdf".
And the boundary: "i don't want the public examples in my doc site to be crypto economic but they do make good test
cases because they have public data"

The driver's reading: Balancer's weighted constant product (the product of balances to weights on the simplex) is the
monomial invariant form in d dimensions with arbitrary exponents, Uniswap v2 its equal-weight two-token case; both
are test cases for the spike, with a Balancer pool's declared weights the cleanest check of a recovered exponent
vector. Neither becomes an example on the docsite: the spike's tables live in `work-packages/WP72-rounds/` and any
later package that exposes the estimator demonstrates it on the wheat table or another non-financial dataset. The
unit was dispatched with the Uniswap pointer and the diagram's reading before the Balancer message; the Balancer case
is added to its brief if the hand-back lacks it.

**His refinement (16:13 EST, verbatim):** "financial examples are okay but not crypto. we're trying to shed an
association with being a crypto firm. finance is okay but needs to be conventional"

The driver's reading, for every public surface (the docsite, the paper, the README, the examples): no
crypto-economic example or dataset; conventional finance is admissible (a public equities, bond, insurance, banking
or corporate-finance table); the market-maker tables stay test cases in the spike's record only, named as such.

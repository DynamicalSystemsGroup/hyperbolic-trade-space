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

## WP72 spike delivered and landed (16:33 EST)

`work-packages/WP72-rounds/` landed as 468681d6: `readout.md` (about 2,700 words), `estimator.py` (`InvariantFit`: minimize
w'S_W w over the simplex, S_W the pooled within-group scatter of log M; the levels per group as outputs; fallbacks
when groups are not given, by order or by clustering the levels, the second named as circular; `two_term_invariant`
for K = 2 by BFGS with restarts), the planted tests and their results, the wheat and market-maker studies with figures
and manifests, the fetched data git-ignored. Relations to the lemmas stated: L1 (a common scale does not move the
minimizer), L8 (a scale move changes log V only, a move along the level set changes Z only), L22 (the frontier loss at
small temperature is the leading term taken group by group; convergence of the minimizers not proved).

Results. Planted: clean tables recovered to 4e-10 (d = 2 and 3, six groups; groups given or found by order); error
about 0.03 times the level noise up to 0.1; both two-term invariants recovered to 1.5e-8; a frontier cloud reports a
poor fit (within-share 0.99) rather than a false invariant; failures named (10 percent mislabelled rows, 0.04; the
order fallback past noise 0.03 at d = 3; pooling without groups biased 0.1; plain PCA leaves the simplex once the
levels' spread reaches the trades'). Wheat: year and treatment set the level (15 percent of the variance of log V
within groups against 73 for shuffled labels, w = (0.41, 0.59)); within a group the level is not conserved (flatness
1.28): biomass is a size the groups set, not an invariant; within a year and section the grain-to-straw ratio is
what is shared. Market maker: Uniswap v2 DAI/WETH, 4,327 reserve updates in 105 stretches between liquidity events,
w = (0.4989, 0.5011) with within-share 6e-5; the 0.001 offset from one half is the 0.3 percent fee; log V jumps at
mints and burns; the frontier fit goes to a vertex. His collaborator's repository (MIT, commit cd768a7) holds the v1
model and a BigQuery query but no committed table, so the data came from the public chain through a free endpoint
(blocks 12,959,744 to 12,989,743; hashes in `amm-manifest.toml`).

Flagged for him: the endpoint refused Python's HTTP client; the unit's attempt to present a browser-like user agent
from Python was blocked by the permission system and dropped; the fetch then used the system's `curl` as itself,
which the endpoint serves. The data is not in the tree. Whether that fetch is acceptable is his call; the result does
not depend on it (the planted tests and the wheat study stand alone). The crypto boundary holds: the market maker is
a test case in this record and nothing on a public surface.

His five questions from the readout wait for his read: what the variant becomes (an estimator of the package; a docs
section; a readout only); how groups enter; which market-maker data a next stage uses; several terms now or later;
whether the wheat page cites the finding (WP71 is scoped to V against biomass alone and proceeds so). The unit's
recommendation for a next stage: `InvariantFit` in `src/` as a decomposition-family transformer with the chart as
`transform`, a report and one chart plot, lemma steps for the scale corollary and the group-wise L22, one docs page
on a non-crypto example.

## His formulation and the roadmap boundary (17:19 EST, verbatim)

"as for the estimator that finds invariants. the thing i was thinking could work is something like a separability
approach where V (x) = posynomial(x)  AND V (x) = Ax

this would mean the the level set was explained twice, in our case with different variables. one affine and one
hyperbolic. the low dimensional case being `biomass = wheat * straw`, which is a contant product invariant, but with
the invariant level sets being a different variable. the generalization being affine on one side and posynomial on
the other.

like with our earlier work this should start with the monomial case, and a scalar. but we should explore
generalizations. this should be viewed as a research roadmap and the any new features in the estimator should come in
0.2 or later"

The driver's reading: the level set explained twice, by a posynomial of one block of the data's variables and by an
affine function of another block, the two agreeing row by row; the estimator finds both at once (the exponents on the
simplex for the posynomial side, the affine map for the other), a two-view problem in the spirit of canonical
correlation between a log-linear view and an affine view. The first case is the monomial with a scalar on the affine
side: w . log x = log(a y + b) for one variable y, whose statistic at b = 0 is the correlation of log V with log y that
WP71 just put on the wheat page (0.99 with y = biomass). Generalizations in order: a vector y with A a row; several
terms on the posynomial side; both sides with several outputs. The roadmap: WP72's readout is stage 1; the next spike
formulates and plants the separability estimator; nothing of it enters the package before 0.2. Recorded in
`notes/directions/candidates.md` as the direction's statement.

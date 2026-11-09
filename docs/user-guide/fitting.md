# Fitting

`HyperbolicTradeSpace` fits the frontier model to conditioned metrics. At one term it solves a convex
problem and returns the minimizer. It follows the scikit-learn decomposition family: `fit`,
`transform`, `inverse_transform`, `score_samples`, and no `predict`. Parameters are stored as given
and validated in `fit`.

## One term

```python {.runnable}
from hyperbolic_trade_space import HyperbolicTradeSpace, make_frontier_data

X, info = make_frontier_data(300, 3, random_state=0)
ts = HyperbolicTradeSpace(temperature=20.0).fit(X)
print(ts.exponents_.round(2), round(ts.frac_above_, 2))
```

The fitted attributes are `exponents_` (shape `(n_terms, d)`, each row on the simplex),
`log_offset_`, `frac_above_` (the fraction of designs beyond V = 1), `n_eff_` (how many designs carry
the fit), `support_weights_`, `basis_`, `objective_`, `termination_` and `conditioning_`. Further
parameters: `min_exponent` (a floor on every exponent; keep it at 0 to read the contending set),
`coordinates` (`"ilr"` or `"alr"`), `tol`, `max_iter` and `random_state`.

## Choosing the temperature

`temperature` is tau, how hard the maximum is. Infinity (`np.inf`) is the exact maximum, a linear
program that gives the supporting envelope: no design lies above it. A finite tau gives the fitted
reference surface with a band of near-frontier designs of width 1/tau, and a few designs beyond
V = 1. Tau is in units of inverse log-spread, so it depends on the conditioning.

`select_temperature` picks tau so that a target fraction of designs lies above V = 1:

```python {.runnable}
from hyperbolic_trade_space import make_frontier_data, select_temperature

X, info = make_frontier_data(300, 3, random_state=0)
tau = select_temperature(X, target_frac_above=0.35, bounds=(3, 1000))
print(round(tau, 1))
```

This synthetic table puts 30 percent of its rows on the planted frontier, hence the target 0.35;
for real data the default 0.10 is a common start. Use values of tau of about 3 and above: below that
`frac_above_` is not monotone in tau, and a `ValueError` says when the bracket `bounds` does not
contain the target. Re-select tau when you change the number of terms.

## Several terms

One term is one flat facet in log space with constant exchange rates. When the rates vary by region,
fit `n_terms=K` facets, where you choose K:

```python {.runnable}
from hyperbolic_trade_space import HyperbolicTradeSpace, make_frontier_data

X, info = make_frontier_data(400, 4, n_terms=3, random_state=0)
ts = HyperbolicTradeSpace(n_terms=3, temperature=50.0, random_state=0).fit(X)
print(ts.exponents_.shape, ts.termination_.status)
```

Fitting partitions the designs among facets and refits each, from several seeded starts (`n_restarts`,
default 5) keeping the best. More restarts cost time and are not a cure for a poor local optimum.
Extra fitted attributes are `facet_` (each training row's active facet), `coefficients_` and
`facet_share_`; `assign_facets(X)` labels new rows. `term_temperature` (kappa, default infinity)
rounds the corners where facets meet; finite kappa leaves the facets unchanged. `penalty="reweighted_l1"`
with `alpha` pushes small exponents to exact zero, at finite temperature only. `facet_step` is
`"support"` (default) or `"tangent"`, which is not monotone and carries no local-optimality status.
What the fit reports about itself is on the [termination page](termination.md).

Kernel expansions that stay inside geometric programming are documented, not built.

## Synthetic data

`make_frontier_data` plants a frontier, with `n_terms=K` for K facets; `make_configured_frontier_data`
also returns configuration variables. Both are seeded and used throughout these pages.

# Fitting

`HyperbolicTradeSpace` fits the frontier model to conditioned metrics. At one term it solves a convex
problem and returns the minimizer. It follows the scikit-learn decomposition family: `fit`,
`transform`, `inverse_transform`, `score_samples`, and no `predict`. Parameters are stored as given
and validated in `fit`.

## One term

```python {.runnable}
from hyperbolic_trade_space import (
    HyperbolicTradeSpace,
    make_frontier_data,
)

X, info = make_frontier_data(300, 3, random_state=0)
ts = HyperbolicTradeSpace(temperature=20.0).fit(X)
print(ts.exponents_.round(2), round(ts.frac_above_, 2))
```

The attributes to read first:

- `exponents_`: shape `(n_terms, d)`, each row on the simplex.
- `frac_above_`: the fraction of designs beyond V = 1.
- `n_eff_`: how many designs carry the fit.
- `objective_` and `mean_slack_`: `objective_` is what the solver minimized, the soft maximum at one
  term and the mean slack at several, so it is not comparable across numbers of terms.
  `mean_slack_` is the mean gap between facet and design, defined at every number of terms; compare
  fits with it, at a fixed temperature.
- `termination_` and `conditioning_`: how the fit stopped and how well its exponents are identified
  ([termination page](termination.md)).

The chart's basis, offsets and support weights are `basis_`, `log_offset_` and `support_weights_`.
Keep `min_exponent` (a floor on every exponent) at 0 to
read the contending set, and choose `coordinates` as `"ilr"` or `"alr"`.

## Choosing the temperature

`temperature` is tau, how hard the maximum is. Infinity (`np.inf`) is the exact maximum, a linear
program giving the supporting envelope: no design lies above it. A finite tau gives the fitted
reference surface with a band of near-frontier designs of width 1/tau, and a few designs beyond
V = 1. Tau is in units of inverse log-spread, so it depends on the conditioning.

`select_temperature` picks tau so that a target fraction of designs lies above V = 1:

```python {.runnable}
from hyperbolic_trade_space import (
    make_frontier_data,
    select_temperature,
)

X, info = make_frontier_data(300, 3, random_state=0)
tau = select_temperature(X, target_frac_above=0.35, bounds=(3, 1000))
print(round(tau, 1))
```

This synthetic table puts 30 percent of its rows on the planted frontier, hence the target 0.35;
for real data the default 0.10 is a common start. Use tau of about 3 and above: below that
`frac_above_` is not monotone in tau. A `ValueError` says when `bounds` misses the target.
Re-select tau when you change the number of terms.

## Several terms

One term is one flat facet in log space with constant elasticities. When the rates vary by region,
fit `n_terms=K` facets, where you choose K:

```python {.runnable}
from hyperbolic_trade_space import (
    HyperbolicTradeSpace,
    make_frontier_data,
)

X, info = make_frontier_data(400, 4, n_terms=3, random_state=0)
ts = HyperbolicTradeSpace(
    n_terms=3, temperature=50.0, random_state=0
).fit(X)
print(ts.exponents_.shape, ts.termination_.status)
```

Fitting alternates weights from the current model with a refit, from several seeded starts
(`n_restarts`, default 5) keeping the best. `assign_facets(X)` reads which facet
dominates new rows. Options:

- `term_temperature` (kappa, default infinity) sets the temperature of the soft weights: finite,
  every design weighs every term; infinity, one label per design. Reported facets are the dominant
  term.
- `penalty="reweighted_l1"` with `alpha` pushes small exponents to exact zero, at finite temperature
  only.
- `facet_step` is `"support"` (default) or `"tangent"`, which is not monotone and carries no
  local-optimality status.

`facet_` gives each training row's dominant facet; `coefficients_` and `facet_share_` the facets'
coefficients and shares. At one term `facet_` is all zeros and `facet_share_` is `[1.0]`. What the fit
reports about itself is on the [termination page](termination.md).

## Choosing K, the temperature and the band

Compare numbers of terms at one fixed temperature, by `mean_slack_`, never by `objective_` and never
at a temperature re-selected for each K. Add a term while `mean_slack_` still falls by more than the
variation between restarts. Resample: a facet whose exponents change between bootstrap resamples
or restarts is a splinter, a few designs fitted alone, and K is too large.

```python {.runnable}
import numpy as np
from hyperbolic_trade_space import (
    HyperbolicTradeSpace,
    make_frontier_data,
)

X, info = make_frontier_data(400, 4, n_terms=3, random_state=0)
rng = np.random.default_rng(0)
for K in (1, 2, 3, 4):
    fit = lambda A, s: HyperbolicTradeSpace(
        n_terms=K, temperature=50.0, random_state=s
    ).fit(A)
    ms = fit(X, 0).mean_slack_
    W = [
        fit(X[rng.choice(400, 400)], s).exponents_.min()
        for s in range(4)
    ]
    print(K, round(ms, 3), np.round(W, 2))
```

The mean slack falls from 0.855 at K = 1 to 0.692, 0.664 and 0.658: the third term is the last that
pays. Over the four resamples the smallest exponent stays within 0.07 to 0.08 at K = 3 and ranges from
0.00 to 0.07 at K = 4: the fourth facet changes with the sample.

`select_temperature` needs a target the fit can reach. With several terms the facets are not
supporting planes, so `frac_above_` levels off above zero as tau grows (about 0.30 on the table of
`make_frontier_data(300, 4, n_terms=2, random_state=777)`) and the default target 0.10 raises "not
bracketed". The message names a target, a fixed `temperature`, and wider `bounds`. Select
tau at K = 1 and hold it fixed, or choose a target above the level-off.

`tension_report` takes its band from the temperature, 1/tau. A facet with fewer than
`min_near_frontier` designs in the band raises, and the message names the `band`, and the matching
`temperature`, that holds enough. On that table at tau = 50 the band 0.02 holds five designs of
facet 0 and 0.025 holds ten.

With two metrics the facets can be drawn in the log plane:

```python {.runnable}
from hyperbolic_trade_space.plotting import plot_log_plane

X2, _ = make_frontier_data(300, 2, n_terms=3, random_state=0)
ts2 = HyperbolicTradeSpace(
    n_terms=3, temperature=50.0, random_state=0
).fit(X2)
plot_log_plane(ts2, X2)
```

<figure markdown>
![Designs in the log plane of two metrics with the frontier drawn as a bent line made of three facets, each coloured differently, and a grey band below it.](../generated/figures/three-facets-light.png#only-light)
![Designs in the log plane of two metrics with the frontier drawn as a bent line made of three facets, each coloured differently, and a grey band below it.](../generated/figures/three-facets-dark.png#only-dark)
<figcaption>Figure 2. Three facets fitted to two metrics: each facet is a straight line in log space, and the frontier is their envelope.</figcaption>
</figure>

Kernel expansions that stay inside geometric programming are documented, not built.

## Synthetic data

`make_frontier_data` plants a frontier, with `n_terms=K` for K facets; `make_configured_frontier_data`
also returns configuration variables. Both are seeded and used throughout these pages.

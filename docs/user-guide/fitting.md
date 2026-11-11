# Fitting

`HyperbolicTradeSpace` fits the frontier model to conditioned metrics. At one term it solves a convex
problem and returns the minimizer. It follows the scikit-learn decomposition family: `fit`,
`transform`, `inverse_transform`, `score_samples`, and no `predict`.

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
  term and the mean slack at several, so it is not comparable across numbers of terms (at one
  term they coincide when the log-metrics are centred, as the cubesat's are).
  `mean_slack_` is the mean shortfall below the fitted reference surface, defined at
  every number of terms; compare fits with it, at a fixed temperature.
- `termination_` and `conditioning_`: how the fit stopped and how well its exponents are identified
  ([termination page](termination.md)).

The chart's basis, offsets and support weights are `basis_`, `log_offset_` and `support_weights_`. `training_log_v_` is log V of the training rows.
Keep `min_exponent` (a floor on every exponent) at 0 to
read the contending set, and choose `coordinates` as `"ilr"` or `"alr"`.

## Choosing the temperature

`temperature` is tau, how hard the maximum is. Infinity (`np.inf`) is the exact maximum, a linear
program giving the supporting envelope: no design lies above it. A finite tau gives the fitted
reference surface with a near-frontier band, the designs with |log V| below 1/tau, and a few designs
beyond V = 1. Tau is in units of inverse log-spread, so it depends on the conditioning.

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
for real data start at the default 0.10. Use tau of 3 and above: below that
`frac_above_` is not monotone in tau.
Hold tau fixed across numbers of terms, selected at K = 1.

## Several terms

One term is flat in log space, with constant elasticities. When the rates vary by region, fit
`n_terms=K` terms, where you choose K:

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

Fitting alternates weights from the current model with a refit, from `n_restarts` seeded
starts (default 5), keeping the best. `assign_cells(X)` reads the cell of new
rows. Options:

- `term_temperature` (kappa, term temperature, default infinity): infinity, one label per design;
  finite, every design weighs every term. Read kappa on the scale of tau: far below it, terms
  merge. At tau = 50, kappa = 5000 is within 0.001 of the infinite-kappa exponents.
- `term_aggregation`: `"sum"` (default) or `"mean"`, which subtracts log K / kappa; with the sum, a
  repeated term shifts the soft maximum by log 2 / kappa.
- `penalty="reweighted_l1"` with `alpha` pushes small exponents to exact zero, at finite temperature
  only.
- `refit_step` is `"support"` (default) or `"tangent"`, which is not monotone and carries no
  local-optimality status.

`cell_` gives each training row's cell; `coefficients_` and `term_share_` the terms' coefficients
and term shares. At one term `cell_` is all zeros and `term_share_` is
`[1.0]`.

## Choosing K, the temperature and the band

Compare numbers of terms at one fixed temperature, by `mean_slack_`, never by `objective_` and never
at a temperature re-selected for each K. `mean_slack_` falls with K by construction, so it cannot choose
K alone: a term whose exponents change between bootstrap resamples or restarts is a splinter, a
few designs fitted alone, and K is too large.

```python {.runnable}
import sys

import numpy as np
from hyperbolic_trade_space import HyperbolicTradeSpace

sys.path.insert(0, "examples/adcs")
import case

study = case.load_study("primary")
M, tau = study.M, case.fit_study(study, K=1).tau
rng = np.random.default_rng(0)
for K in (1, 2, 3, 4):
    fit = lambda A, s: HyperbolicTradeSpace(
        n_terms=K, temperature=tau, random_state=s
    ).fit(A)
    ref = fit(M, 0)
    moved = np.zeros(K)
    for s in range(3):
        W = fit(M[rng.choice(len(M), len(M))], s).exponents_
        d = np.abs(W[:, None] - ref.exponents_).sum(axis=2)
        moved = np.maximum(moved, d.min(axis=0))
    print(K, round(ref.mean_slack_, 3), np.round(moved, 2))
```

On the cubesat table of the [examples](../examples.md), where terms leave metrics out, the
mean slack falls from 0.243 at K = 1 to 0.132, 0.088 and 0.07. The last column, per term: its
exponent vector's distance to the nearest resampled term, the largest over three resamples (summed
absolute differences, at most 2). The values belong to this draw of resamples, so none of them is a
threshold for K.

`select_temperature` needs a target the fit can reach. With several terms the term planes are not
supporting planes, so `frac_above_` levels off above zero as tau grows (about 0.30 on the table of
`make_frontier_data(300, 4, n_terms=2, random_state=777)`) and the default target 0.10 raises "not
bracketed". Choose a target above the level-off.

`tension_report` takes its band from the temperature, 1/tau. A term whose cell has fewer than
`min_near_frontier` designs in the band raises, and the message names the `band`, and the matching
`temperature`, that holds enough.

Two metrics, drawn in the log plane:

```python {.runnable}
from hyperbolic_trade_space.plotting import plot_log_plane

X2, _ = make_frontier_data(300, 2, n_terms=3, random_state=0)
ts2 = HyperbolicTradeSpace(
    n_terms=3, temperature=50.0, random_state=0
).fit(X2)
plot_log_plane(ts2, X2)
```

<figure markdown>
![Designs in the log plane of two metrics, all in one colour, with the frontier drawn as one black bent line, the envelope of three straight term lines, and a grey band below it.](../generated/figures/three-terms-light.png#only-light)
![Designs in the log plane of two metrics, all in one colour, with the frontier drawn as one black bent line, the envelope of three straight term lines, and a grey band below it.](../generated/figures/three-terms-dark.png#only-dark)
<figcaption>Figure 2. Three terms fitted to two metrics: each term is a straight line in log space, and the frontier is their envelope.</figcaption>
</figure>

## Synthetic data

`make_frontier_data` plants a frontier, with `n_terms=K` for K terms; `make_configured_frontier_data`
also returns configuration variables. Both are seeded and used throughout these pages.

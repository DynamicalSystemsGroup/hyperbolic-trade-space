# Choosing K

The fit never selects the number of terms K; you do. Every check below reads fits at one
temperature, selected at K = 1 on your table ([the recipe](#the-temperature)): `mean_slack_` is
comparable across K at one temperature, and `objective_` is not. No check decides K alone, so each
is given with what it cannot say. The package has no held-out criterion for K.

## Methods

- **Mean slack against K.** Fit `n_terms` = 1, 2, ... and read the drop in `mean_slack_`, the mean
  shortfall of the designs below the fitted reference surface, per added term. A break, one large drop then small ones, shows where
  added terms stop paying. The mean slack falls with every added term by construction, so it cannot choose K, and a table may show no break.
- **Thinnest term.** `term_share_.min()` is the share of the near-frontier designs in the thinnest
  term's cell. The band is the designs within 1/tau of the surface in log V; a cell is the designs
  for which the term is largest. Read the share against 1/K, what each term holds if the cells are equal.
  It says a term is thin, not which K is right.
- **Movement under resampling.** Refit on resamples of the rows and measure how far each term's
  exponent vector sits from the nearest term of the refit (summed absolute differences; exponents sum to one, so at most
  2). It is noisy: draws of one procedure differ by several tenths on the cubesat below, so it offers no
  threshold.
- **Planted check.** Fit `make_frontier_data(n_terms=K0)` at your table's shape to see how recovery
  looks. The planted K0 is known there; your table's is not.
- **The certificate.** `termination_.status` says the optimizer reached a local minimizer;
  `termination_.radius` is the stable radius, the size of a change of the terms that leaves every
  design's cell unchanged. Every fit below at K = 2 and above is certified, so it does not say K is
  right.

## The temperature

For your table `M` of conditioned metrics, the fit temperature is selected at K = 1 and held for
every K ([Fitting](fitting.md#choosing-the-temperature)):

<!-- vocab-exempt: select temperature -->
```python {.runnable}
from hyperbolic_trade_space import (
    make_frontier_data,
    select_temperature,
)

M, _ = make_frontier_data(400, 4, n_terms=2, random_state=0)
tau = select_temperature(M, 0.10, bounds=(3, 1000))
print(round(tau, 1))
```
<!-- vocab-exempt: select temperature -->

0.10 is the share of designs allowed above V = 1. The planted table returns 50.0, used
below for all three (26.5 and 38.1 on the others); real data may need `bounds=(3, 1e4)`.

## Helpers

The planted blocks need only the installed package; the case study's cubesat blocks run from the repository root.

```python {.runnable}
import numpy as np
from hyperbolic_trade_space import HyperbolicTradeSpace


def fit_k(M, K, tau, seed=0):
    return HyperbolicTradeSpace(
        n_terms=K, temperature=tau, random_state=seed
    ).fit(M)


def sweep(M, tau, Ks, planted=None):
    """One line per K at one temperature; returns the mean slacks."""
    slack = []
    for K in Ks:
        fit = fit_k(M, K, tau)
        t = fit.termination_
        line = (
            f"K={K} slack={fit.mean_slack_:.3f}"
            f" thinnest={fit.term_share_.min():.2f}"
            f" {t.status} radius={t.radius:.0e}"
        )
        if planted is not None:
            d = np.abs(fit.exponents_[:, None] - planted[None]).max(
                axis=2
            )
            line += (
                f" found={(d.min(axis=0) < 0.05).sum()}"
                f" unmatched={(d.min(axis=1) >= 0.05).sum()}"
            )
        print(line)
        slack.append(fit.mean_slack_)
    drops = -np.diff(slack)
    print("drops", drops.round(3))
    return np.array(slack)


def movement(M, K, tau, draws=2, seed=0):
    """Largest distance to the nearest term of a refit on a resample."""
    ref = fit_k(M, K, tau)
    rng = np.random.default_rng(seed)
    moved = np.zeros(K)
    for s in range(draws):
        W = fit_k(M[rng.choice(len(M), len(M))], K, tau, s).exponents_
        d = np.abs(W[:, None] - ref.exponents_).sum(axis=2)
        moved = np.maximum(moved, d.min(axis=0))
    return moved.max()
```

## A planted table

`found` counts planted terms matched by a fitted term (largest exponent
difference under 0.05); `unmatched` counts fitted terms matching none.

```python {.runnable}
for K0, seed in ((2, 0), (3, 0), (3, 1)):
    X, info = make_frontier_data(400, 4, n_terms=K0, random_state=seed)
    print(f"planted K0 = {K0}, table {seed}")
    sweep(X, 50.0, range(1, 6), np.asarray(info["exponents"]))
```

With two planted terms the mean slack drops by 0.108 at K = 2 and by 0.005 or less after; both
terms are found at K = 2. With three, table 0 drops by 0.163 and 0.029, then 0.005 or less, and all
three are found at K = 3. Table 1 drops by 0.181, then 0.006 or less, and finds two of the three at
every K from 2: the break reads the terms the fit recovers, not the number planted.

```python {.runnable}
X, _ = make_frontier_data(400, 4, n_terms=3, random_state=0)
for K in (3, 5):
    print(
        K, np.round([movement(X, K, 50.0, seed=s) for s in range(2)], 2)
    )
```

On table 0 the movement is 0.04 and 0.02 at K = 3, and 0.23 and 0.24 at K = 5.

## The cubesat

The two regimes of the [examples](../examples.md), each at its K = 1 temperature, selected as in the
recipe.

```python {.runnable}
import sys

sys.path.insert(0, "examples/adcs")  # repository root
import case

studies = {r: case.load_study(r) for r in ("primary", "stock")}
taus = {r: case.fit_study(s, K=1).tau for r, s in studies.items()}
for r, s in studies.items():
    print(r)
    sweep(s.M, taus[r], range(1, 6))
```

The primary regime drops by 0.078, then 0.023, 0.012 and 0.005: a break at K = 2, where the
thinnest term holds 0.28 (0.21 at K = 3). The stock regime drops by 0.055, 0.031, 0.012 and 0.010,
bending with no break, so the mean slack cannot choose K; its thinnest term holds 0.35 at K = 2 and
0.13 at K = 3.

```python {.runnable}
for K in (2, 3, 4):
    M, tau = studies["primary"].M, taus["primary"]
    print(
        K, np.round([movement(M, K, tau, seed=s) for s in range(3)], 2)
    )
```

Over three draws the primary regime's movement is 0.18 to 0.20 at K = 2, 0.15 to 0.29 at K = 3 and
0.14 to 0.95 at K = 4. The ranges overlap, so this check excludes none.

## Large K and the elbow in PCA

The elbow heuristic for the number of principal components reads a break the same way. The limit
differs: variance explained ends at d components, while
here K has no ceiling and the mean slack no floor.

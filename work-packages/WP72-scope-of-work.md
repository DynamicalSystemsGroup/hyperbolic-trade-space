# WP72 — Scope of work: learning the invariant rather than the trade (stage 1, a research spike)

| | |
|---|---|
| **Status** | DRAFT, approved by the driver as his proxy on his direction of 2026-11-16 (`WP72-decisions.md`); a spike, not for the 0.1 release |
| **Supervisor (accountable)** | mzargham |
| **Repository** | `DynamicalSystemsGroup/hyperbolic-trade-space`; writes only under `work-packages/WP72-rounds/`; branch `wp72` |
| **Approval record** | The driver's approval under his mandate, quoted in `WP72-decisions.md` |
| **Acceptance record** | The driver's acceptance of the readout; his read; a readout under `notes/directions/` if he adopts the direction |

## Purpose

His direction (`WP72-decisions.md`): a variant of the method that finds the pattern where several quantities rise
together along a level and trade at a fixed level, as a constant-product market maker's reserves do (x y = k) and as
grain and straw do against biomass; tested on the wheat example and on public Uniswap data.

## Goals

- G1. **The variant stated:** the same posynomial invariant form with a second estimator. The frontier fit is
  one-sided (the entropic soft maximum, the data below the level set); the invariant fit is two-sided: within a group
  of rows that share the invariant, the monomial m^v (exponents on the simplex) with the least variance of log V is
  the invariant, and the chart's large-variance directions are the trades along its level set. State it in the
  paper's notation (Boyd and Vandenberghe for the problem, scikit-learn for the estimator); say how the groups enter
  (given, or found by clustering the levels); say what K > 1 means here (a sum of monomials as the invariant, as in a
  stable-swap pool) and whether the several-term machinery of the package carries it; relate it to the homogeneity
  lemma and the chart (`derivation/`, `paper/`, read-only).
- G2. **Planted tests:** tables generated with a known invariant (one monomial; a posynomial of two terms; noise on
  the level; several groups with different levels) and the estimator's recovery of the exponent vector, against the
  frontier fit on the same tables (which finds the boundary, not the level) and against plain PCA in log space.
- G3. **The wheat table:** grain and straw (and biomass) over the plot-years; what the variant finds with and without
  groups (year, treatment, cultivar); whether biomass is a level or a size that varies, in the variant's own terms.
- G4. **A constant-product market maker:** a public table of a Uniswap v2 pool's reserves over time (swaps between
  liquidity events as the groups); the invariant recovered as (1, 1) within groups and the level jumps at liquidity
  events; the source open, cited and hashed by a manifest; if no open table is fetched today, say so and name what is
  needed from his own model (he said he has access from a GitHub model of his; held as an open question for him).
- G5. **The readout:** the variant, the results, what it tells the method's users (a dependence screen; the
  size-against-shape reading), what the package would expose (an estimator class, a report, a plot) and at what cost,
  and the decisions that are his, as plain options.

## Non-goals

No change to `src/`, the docs, the paper, the derivation or the examples; no claim beyond the tables run; no deploy.

## Deliverables

| ID | Deliverable | Serves |
|---|---|---|
| D-1 | `work-packages/WP72-rounds/readout.md` | G1, G5 |
| D-2 | `work-packages/WP72-rounds/estimator.py` (the variant, with the package as a dependency) and `tests_planted.py` with its results table | G2 |
| D-3 | `work-packages/WP72-rounds/wheat.md` and its script and figures | G3 |
| D-4 | `work-packages/WP72-rounds/amm.md`, its manifest, script and figures, or the statement of what is missing | G4 |

## Requirements and checks

| ID | Requirement | Check |
|---|---|---|
| R-1 | The planted exponent vectors are recovered within a stated tolerance on the clean tables, and the readout states where recovery fails as noise or group confusion grows | the results table |
| R-2 | Every data source is cited, licensed and hashed; nothing is committed but small result tables | the manifests; `git diff --stat dev` |
| R-3 | The readout's statement of the variant uses the paper's notation and names its relation to the lemmas | a read |
| R-4 | Lint and format; no attribution line; no metanarration; nothing outside `work-packages/WP72-rounds/` | `uv run ruff check .`; `ruff format --check .`; the grep; the diff |

## Definition of good

He can decide from the readout whether the variant is a second estimator of the package, a note in the docs, or
nothing, and what the next stage would build.

## Definition of good enough

D-1 to D-4 (D-4 possibly as the statement of what is missing); R-1 to R-4; the driver's acceptance; his read.

## Definition of done

Good enough met; his decision recorded.

## Open decisions

1. **The Uniswap source:** an open public table the unit finds, or his GitHub model's data (held for him; the spike
   proceeds on what it can fetch).

## Agent's defaults

- One unit on branch `wp72`; the estimator a small scikit-learn-style class in the package's folder of the spike; the
  frontier fit and PCA as the two baselines; figures with the package's plotting where they fit, matplotlib otherwise.

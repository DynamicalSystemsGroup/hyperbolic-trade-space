# WP41 spike readout: the bridge from the chart back to a design

Spike for `WP41-scope-of-work.md` D-1. Run records: `selection_rules.py` and its output
`run-record.txt` (one run each, from the data of record, reproducible with
`MPLCONFIGDIR=$(mktemp -d) uv run python work-packages/WP41-rounds/spike/selection_rules.py`; it ran
locally with the committed v2 oracle, about 30 seconds).

## 1. The note: the approach, stated once

**The forward map.** A configuration c (design variables) is evaluated to attributes a, conditioned to
metrics m, and read through the chart to a point (Z, log V). The conditioning and the chart are reversible
(the chart is a bijection, L8, `thm-chart`; the conditioning is invertible, L9, `thm-pullback`, which is the route back to attribute units; the scope's "Theorem 7" is L9, as L7 is the elasticities). Invertibility is lost at one place only,
the evaluation c to a, where it fails three ways: many configurations give one outcome (many-to-one), not
every chart point is the outcome of any configuration (not onto: the attainable set is a subset), and the
evaluation can differ from one run to the next (noisy; the case's data of record are deterministic, so on
the case the noise is injected, `examples/adcs/noise_injection.py`).

**The preimage of a chart point.** For a chart point p, its preimage is the set of configurations whose
evaluation lands at p: empty when p is not attainable, and not a single point when it is attainable.

**Two routes back.**

- *Sampled route.* A point with a datum is a row of the table, so its configuration is the row's. This is
  a lookup, no conjecture. With a noisy evaluation, re-evaluating the configuration may land elsewhere.
- *Conjecture route.* A point without a datum has no known configuration. A **proposal** is a configuration
  chosen for it, together with the chart point the regressor predicts for it and a **tolerance**. It is a
  conjecture until **checked**: the design is built or evaluated, and its measured chart point is compared
  with the predicted one.

**The selection rule.** The preimage is not unique, so a proposal needs a **selection rule**: how one
configuration is picked from those predicted near the target. Three are prototyped below; the default is
for the supervisor (section 4).

**The check and its three outcomes.** The tolerance is the fit's band 1/tau (default). The check evaluates
the proposal once (a Monte Carlo evaluation would average several runs) and reports one of:

- *confirmed*: the design is feasible and the measured point is within the tolerance of the predicted one;
- *refuted*: the design is feasible but the measured point is farther; the measured row is a row the table
  lacked, so the fit is rerun (the regressor and, if the table grew, the chart are refit);
- *infeasible*: the design fails a feasibility condition, so it is not a design at all; the row is kept
  with its flags, the regressor is refit with it as a datum of the infeasible region.

**The outer loop is the refit.** Propose, evaluate, append the row, refit, repeat (Section 7's loop).

**What stays open.** Not expected to move outward at every step: it could move inward on a step. The
conjecture is a submartingale property: outward in expectation, with a convergence result when the expected
progress ceases. Future work; no conditions are derived (`WP36-decisions.md`, change request 169).

## 2. Audit of the existing pieces

| Piece | Where | Place in the note | State |
|---|---|---|---|
| The regressor: configuration to chart coordinates, `predict_coordinates`, `predict_std` | `src/tradespace/predictive.py` (`TradeSpaceRegressor`) | The prediction half of a proposal: the predicted chart point and a spread | Built; tested; carries the regression error in coordinates |
| The sampled route | none (the table row) | A datum's configuration is its row; the chart is `transform` of the row's metrics | Implicit: no function, no page says it |
| The pooled-configuration proposal and its radius | `examples/adcs/make_check_designs.py` (frozen WP7 script, the constant `REACH = 0.35`); `examples/adcs/experiments/check_designs.py` (`Proposer`, the data of record's flow: `REACH_QUANTILE = 0.02` of the nearest pool distances over the 300 most isolated holes) | The selection rule "nearest configuration in the pool", with a radius that decides whether a target counts as reachable | Built for the case, not in the package; the rule is hard-coded; the two files differ (constant against quantile) and the `Proposer` prints the rule it uses; neither separates proposals: on the data of record proposals 1 and 3 are the same configuration, since two holes had one pooled configuration nearest |
| A tolerance | `case.predict_check` and the paper's D.10 table: the band 1/tau on log V and on ||dZ|| | The tolerance of the check | Built for the case; not a package parameter |
| The check designs, measured | `examples/adcs/make_check_designs.py simulate`, `experiments/check_designs.py` (`Checks`, `CheckOracle`), `data/v2/check_designs_cubesat.csv`; the table in `case.predict_check` | The check: evaluate the proposal, compare with the prediction | Built for the case: one run per proposal, comparison in `predict_check`; there is no function that returns an outcome |
| The three outcomes | the paper's D.10 and the Discussion's reading: the three proposals on the data of record are within the band of their predictions but fail the depth-of-discharge condition | Confirmed, refuted, infeasible | Only the comparison exists; the outcome label does not; "infeasible" is read by a person from the flags |
| The feasibility conditions | the flags `settled`, `power_ok`, `momentum_ok`, `dod_ok` of the oracle; the regressor is trained on feasible rows only | Decides infeasible | The surrogate carries no feasibility: a proposal is predicted at a feasible-trained surface and may be infeasible (eight of nine prototyped proposals below) |
| Noise | `examples/adcs/noise_injection.py` (noise-ridge corollary, Appendix B L20) | The evaluation's noisiness; sets how much of a refuted outcome is noise | Built as an experiment on the fit's exponents; it does not feed a tolerance; no repeated-evaluation check exists |
| The refit loop (outer loop) | Section 7 prose only; the ledger of `examples/adcs/experiments/` re-runs a table but not a loop | The outer loop | Missing: no code, no run; future work for the convergence statement, 0.2 for a demonstration |
| The submartingale conjecture | `WP36-decisions.md`; Section 7's Open sentence (request 169, in `paperfix3`) | What stays open | Documented, nothing derived, as ruled |
| Section 7's prose | `paper/paper.ipynb`, "Search of the design space (preliminary)" | The procedure at a high level: inner loop identifies, middle loop proposes, outer loop evaluates and refits | Uses "the middle loop proposes" and "evaluates the proposals" without the names proposal, selection rule, check; the unit's edit adds them |
| Appendix D.10, "Propose, predict, check" | `paper/paper.ipynb` (the check), `paper/supporting_material.ipynb` | One run of the conjecture route | Built; reports the three proposals as a check of the regressor, not a rate |

## 3. The selection rules, prototyped (one run each)

Data of record: the v2 primary table (2,134 feasible designs), the four-metric view, tau = 10.69 so the
band 1/tau = 0.0935, the seeded pool of 100,000 configurations of the proposer. The existing rule,
recomputed, reproduces the three committed proposals (printed: `[True, True, True]`). Targets: the three
committed holes and the next seven isolated, separated holes, ten in all. The distance of a predicted
point to a target is sqrt(|dZ|^2 + (2 log V)^2) as in the existing rule. The proposer's reach, from the
data, is 0.6947.

| Rule | What it does | Targets within the proposer's reach (of 10) | Within the band 1/tau (of 10) | Median distance to target | Median change from the reference datum (L1, features in [0,1]) |
|---|---|---|---|---|---|
| Nearest in pool | the pooled configuration predicted nearest the target (the existing rule) | 3 | 0 | 1.125 | 1.30 |
| Smallest change | among pooled configurations predicted within the reach, the one nearest the datum nearest the target | 3 | 0 | 1.125 | 1.30 |
| Surrogate search | L-BFGS-B over the four continuous variables from several starts, the nine categorical combinations enumerated, minimising the predicted distance | 3 | 0 | 1.095 | 1.41 |

The three rules tie on reach: the same three targets are reachable by each, none is within the band, and
the other seven lie farther than 1.0 from every predicted point the pool or the search finds. The search
gets slightly nearer on every target (for example 0.632 against 0.678 on target 2) but no rule reaches a
target within the band. Under the default's wording (the rule that reaches its target within the band most
often) the answer is a three-way tie at zero, so the default is not settled by the run and goes to the
supervisor as a plain choice (section 4).

**Each rule's proposal for the first three targets, built and checked once** (the v2 oracle, run locally;
the check is the band on |dlogV| and on ||dZ||, and the four feasibility flags):

| Target | Rule | Predicted distance to target | dZ | dlogV | Failed flag | Outcome |
|---|---|---|---|---|---|---|
| 1 | nearest in pool | 0.674 | 0.017 | 0.042 | dod_ok | infeasible |
| 1 | smallest change | 0.690 | 0.016 | 0.024 | dod_ok | infeasible |
| 1 | surrogate search | 0.664 | 0.022 | 0.042 | dod_ok | infeasible |
| 2 | nearest in pool | 0.678 | 0.077 | 0.061 | dod_ok | infeasible |
| 2 | smallest change | 0.678 | 0.077 | 0.061 | dod_ok | infeasible |
| 2 | surrogate search | 0.632 | 0.101 | 0.081 | dod_ok | infeasible |
| 3 | nearest in pool | 0.626 | 0.017 | 0.042 | dod_ok | infeasible |
| 3 | smallest change | 0.670 | 0.045 | 0.018 | none | confirmed |
| 3 | surrogate search | 0.622 | 0.022 | 0.035 | dod_ok | infeasible |

Read: the regressor's prediction agrees with the measurement within the band in all nine builds except one
(the search's proposal for target 2, ||dZ|| 0.101 against the band 0.0935); eight of nine fail
depth of discharge, which the surrogate does not model. One proposal is confirmed (the smallest-change
rule on target 3); one run each, on three targets, is a record and not an estimate of a rate. The
smallest-change rule moved the proposal off the pooled configuration that sits on the depth-of-discharge
edge; whether that is the rule or luck is not known from one run. The local oracle reproduces the committed
rows (settling time 42.98409 against the committed 42.9840907 for proposal 1; control effort differs in the
fifth significant figure, 0.0840092 against 0.0840100).

## 4. Plain options for the supervisor

**The default selection rule for 0.2** (the three rules tie on reach, so the default is a choice):

1. Nearest in the pool, the existing rule: simplest, the rule the paper's D.10 already used; it cannot
   return a configuration outside the pool and does not separate proposals (two holes gave one design).
2. Smallest change from a named reference design: needs a reference (the nearest datum, or a design the
   analyst names); keeps a proposal close to a design known to evaluate, which is the only rule here whose
   proposal was feasible; adds a parameter, the reach it searches inside.
3. A search over the surrogate: finds the nearest predicted point the box allows and is not limited by the
   pool; cost is a search per target and no feasibility awareness, so it can sit at the box edge (all three
   of its proposals sit at a bound of the box).

**The shape of the 0.2 interface** (to be scoped from the note):

1. Two functions on the regressor: a `propose` that takes a target chart point and a rule and returns a
   proposal (configuration, predicted point, tolerance), and a `check` that takes a proposal and a measured
   metrics row and returns an outcome among confirmed, refuted, infeasible.
2. A small proposal object (configuration, predicted point, tolerance) with a method `check(measured, feasible)`,
   and the rule passed to the regressor's method that makes it.
3. A recipe in the docs and the case's code only, no package function, until the case demonstration shows
   what the interface should be.

The feasibility condition (what the check calls infeasible) enters 0.2 either as a flag the analyst passes
to `check`, or as a constraint the search respects; the run above supports only the first as built.

## 5. Not established by the spike

The rule that reaches farthest on the case's holes, the rate at which proposals are confirmed, whether the
smallest-change result is the rule or the draw, and anything about the outer loop's behaviour: one run each.
Section 7's open item stays as ruled.

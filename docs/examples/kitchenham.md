# Kitchenham-CSC software projects: scope against slack

## Where the projects come from

<!-- register: examples/kitchenham/results.json describe; manifest.toml -->

Kitchenham, Pfleeger, McColl and Eagan compiled 145 software projects that Computer Sciences Corporation finished between 1994 and 1999, to study its estimation accuracy [@kitchenham2002empirical]. The table is on Zenodo as doi:10.5281/zenodo.268457 under CC BY 4.0. A row is one project: a plan and an actual for effort (hours) and duration (days), and the delivered size in function points. To reproduce:

```bash
uv run python examples/kitchenham/run.py --fetch
uv run python examples/kitchenham/variants.py
```

## The attributes

```text
schedule slack (+1)  1 - actual duration / planned duration, a share
                     of the plan; the plan is the estimated completion
                     date minus the actual start; negative when late
budget slack (+1)    1 - actual effort / first estimate, a share of
                     the plan; effort in hours stands for the budget
scope (+1)           adjusted function points delivered
also kept            project type (D development, P perfective
                     maintenance; ten projects carry none), client
```

141 of the 145 projects are kept: three have no estimated completion date and one's precedes its start. Each rule is a named element of the [case model](https://github.com/DynamicalSystemsGroup/hyperbolic-trade-space/blob/main/examples/kitchenham/kitchenham.sysml).

## What the fit is asked

Project managers speak of an iron triangle: time, cost and scope constrain one another, so a team protects two at the third's expense. Near this portfolio's frontier, did more delivered scope go with less schedule and budget slack, and did the two slacks move together or against each other?

## The fit

<!-- register: examples/kitchenham/results.json describe (worst overruns), runs.primary -->

Both slack shares take the shift 10, the round number above the worst overrun (8.9 times the planned duration), so every metric is positive; scope is unshifted; each log gets a standard scaler ([conditioning](../user-guide/conditioning.md)). The [temperature](../generated/glossary.md) that puts a tenth of the projects above the frontier is 22.8. At one term the exponents are 0.71 for schedule slack, 0.18 for budget slack and 0.11 for scope; all three are in the [contending set](../generated/glossary.md). The band widens from 1/τ to hold fifteen projects, 0.047 in log V. Among them the association of the two slacks is +0.43, of schedule slack with scope −0.71 and of budget slack with scope −0.92.

```python {.runnable}
import sys

sys.path.insert(0, "examples/kitchenham")
import run

x = run.load_derived()
fit, tau = run.fit_k1(run.condition(x))
run.pairs_figure(x, fit, tau)
print(round(tau, 1), fit.exponents_.round(2))
```

<figure markdown>
![Three scatter panels of the 141 projects in standardized log-metrics, each with the fifteen near-frontier projects marked in orange: schedule slack against budget slack, where the marked points rise together, association +0.43; schedule slack against scope, association −0.71; budget slack against scope, association −0.92, where the marked points fall as scope rises.](../generated/figures/kitchenham-pairs-light.png#only-light)
![Three scatter panels of the 141 projects in standardized log-metrics, each with the fifteen near-frontier projects marked in orange: schedule slack against budget slack, where the marked points rise together, association +0.43; schedule slack against scope, association −0.71; budget slack against scope, association −0.92, where the marked points fall as scope rises.](../generated/figures/kitchenham-pairs-dark.png#only-dark)
<figcaption>Figure 11. Each pair of log-metrics with the fifteen projects nearest the frontier marked; the number is their association, a correlation. Shared movement left, substitution centre and right.</figcaption>
</figure>

<!-- register: examples/kitchenham/results.json runs.primary.k2 -->

At two terms the second term holds none of the near-frontier projects (shares 1.00 and 0.00) and the mean level below the frontier falls from 0.345 to 0.271 from the far rows: one term describes the portfolio.

<!-- register: examples/kitchenham/variants.json conditioning -->

**The ladder.** Under the six scaled rules (Figure 12) scope's association is negative with both slacks, −0.48 to −0.92, and the slacks' is positive, +0.13 to +0.52. With no scaler scope's exponent is 0.00 and the fit reads the scale, not the projects. Schedule slack's exponent runs from 0.35 to 0.71, scope's from 0.11 to 0.46.

```python {.runnable}
run.participation_figure()
```

<figure markdown>
![Dot chart of seven conditioning rules against exponent from 0 to 1, three colours for schedule slack, budget slack and scope; schedule slack's dots lie between 0.35 and 0.71, budget slack's between 0.18 and 0.48, scope's between 0.11 and 0.46 except a hollow dot at zero for the no-scaler rule.](../generated/figures/kitchenham-participation-light.png#only-light)
![Dot chart of seven conditioning rules against exponent from 0 to 1, three colours for schedule slack, budget slack and scope; schedule slack's dots lie between 0.35 and 0.71, budget slack's between 0.18 and 0.48, scope's between 0.11 and 0.46 except a hollow dot at zero for the no-scaler rule.](../generated/figures/kitchenham-participation-dark.png#only-dark)
<figcaption>Figure 12. Each metric's exponent at one term under the seven rules; hollow, outside the contending set. Which metrics bound the frontier is read here, how they move together from Figure 11.</figcaption>
</figure>

<!-- register: examples/kitchenham/variants.json bands, influence -->

**Band and influential projects.** At bands holding ten to twenty-five projects the slacks' association runs from +0.67 to +0.17 and scope's from −0.53 to −0.95. Leaving each project out in turn, 140 of 141 refits keep every sign; without project 16 the slacks' association is −0.20. Without the largest project (18,137 function points) it is +0.10; without the worst schedule overrun schedule slack's exponent falls to 0.37.

<!-- register: examples/kitchenham/variants.json subsets -->

**The subsets.** In the 50 development projects the pattern holds (+0.27, −0.65, −0.70). In the 73 perfective-maintenance projects and the largest client's 113 the two slacks run against each other (−0.74 and −0.10) while scope stays against schedule slack.

**On your own portfolio.** Refit with one change at a time; read the contending set, each sign, each exponent's range.

## What the fit says

Near this portfolio's frontier, the projects that delivered more scope had less schedule and budget slack, under every scaled rule, every band and every project removed. The two slacks moved together in most readings, weakly or not in some: the association thins as the band widens, turns negative without one project, and reverses in two subsets. All three sides bound the frontier; the trades are read from the associations, not the exponents, which the conditioning moves.

## What the example cannot show

One company's projects of one decade, with effort standing for money. A quarter of the projects end exactly on the estimated date, so some dates may have been recorded as the actual. The table carries no quality measure, so the case says nothing about quality. Nothing here says why a project landed where it did.

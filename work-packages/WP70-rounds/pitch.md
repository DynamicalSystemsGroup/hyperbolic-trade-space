# WP70 D-1 — The iron triangle in project data: a pitch

## Part one: for the project-management reader

### The question

Time, cost and scope, with quality in the middle: a team can protect two sides at the expense of the third. The
claim to test is that the triangle has more than three sides. Each quality measure a project answers to (escaped
defects, rework, acceptance) is a further side, so a project with m quality measures faces 3 + m goals that compete.
Across many finished projects, which goals did the best projects trade against one another, which moved together,
and which did not constrain them at all?

### How the data are read

Each finished project is scored on each side so that more is better:

- **schedule slack**: the share of the planned duration left over; an on-time project scores zero and a late one
  less than zero, before the shift;
- **budget slack**: the same for money, or for effort where effort is the budget recorded;
- **scope**: what was delivered, in story points or function points;
- **quality**: each measure turned so that more is better (days between escaped defects, not defect count).

A late or over-budget project has negative slack, and the analysis needs every score above zero, so a fixed
amount is added to both slack scores: the same amount for every project, chosen to clear the worst overrun and
reported with the result.

Then the analysis looks at the edge of the portfolio: the projects that no other project beats on every side at
once. Along that edge, if more scope comes with less slack, the best projects paid for scope with time or money; if
two sides rise together, those two were not traded. The edge is fitted as a smooth surface with one weight per side.
A weight says how strongly that side bounds the edge; a side with no weight
did not constrain the best projects. Whether two sides trade is read from how they move among the projects at the
edge, not from the weights.

### The proof of concept: 141 software projects

The data are 145 software projects of one IT services company, Computer Sciences Corporation, run between 1994 and
1999 and published by Kitchenham and colleagues (2002). Each project has a first estimate of effort and the actual
effort in hours (the budget the table records), an estimated completion date and the actual duration, and the
delivered size in function points. 141 have a usable plan. The typical project delivered 275 function points, on
its planned date (24 percent exactly on it) and 3 percent under its effort estimate; the worst ran 8.9 times its
planned duration and 5.9 times its estimate. The table holds no quality measure.

What the analysis found:

1. **All three sides constrain the best projects.** Each gets weight in the fitted edge.
2. **Near the edge, scope was paid for with time and money together.** Among the 15 projects nearest the edge,
   budget slack and scope run against each other (correlation -0.92), as do schedule slack and scope (-0.71), while
   schedule slack and budget slack rise together (+0.43). In this portfolio the triangle behaved as two sides: time
   and money together on one side, scope on the other.
3. **The best projects were large and came in early and under.** Those 15 delivered a median of 552 function points,
   in 86 percent of the planned time and on 76 percent of the estimate.
4. **One edge describes the portfolio.** A second, separate edge was tried and held no projects near it in most
   of the scorings below.
5. **The direction is stable; the exchange rate is not.** The analysis was repeated under seven scorings of the whole
   portfolio, each a different reasonable way of turning plans and actuals into scores (the amount added to the
   slack, a cap on overruns, the plan-to-actual ratio instead of the share). In six, scope runs against both
   slacks and the two slacks rise together; a seventh scoring, with the sides left on their raw scales, is dominated
   by scope's far larger spread and reads differently. The weights move: schedule's runs from 0.35 to 0.71 and
   scope's from 0.11 to 0.46, so how much time and money buys a function point is not settled by these data. In two
   subsets the pattern changed: within one project type (73 projects) time and money traded against each other, and
   within the largest client (113 projects) they did not move together. Whether those are different portfolios or
   too few projects to read, these data do not say.

![The figure is a three-by-three grid of correlations among schedule slack, budget slack and scope for the 15
projects nearest the edge: budget slack against scope -0.92 and schedule slack against scope -0.71 in orange,
schedule slack with budget slack +0.43 in light purple; the fitted weights under each name are 0.71, 0.18 and
0.11.](case/figures/kitchenham-association.png)

*Figure 1. Kitchenham-CSC, the 15 projects nearest the fitted edge: how each pair of sides moves together (purple,
positive) or against each other (orange, negative); w is each side's weight in the edge. The title's "trilemma (3
metrics contend)" is the package's name for finding 1, all three sides constraining the edge; the outlined diagonal
cells mark those sides.*

### What a programme would tell a PE and PMP that they do not already know

- **Which sides bind in a given portfolio, measured.** Here time and money moved together and scope was the side
  traded; a fixed-price portfolio, or an agile one with fixed sprints, may bind differently.
- **The exchange rate at the edge.** How much slack the best projects gave up per unit of scope, with an uncertainty
  that says whether a portfolio can quote it.
- **Where each quality measure sits.** On the edge (traded for scope or time), off it (free), or merely moving with
  another side.
- **One triangle or several.** Whether project types or clients face different edges, which a portfolio average
  hides.
- **Which projects had room.** A project well inside the edge could have gained on every side at once; one on it
  could not.

It does not tell why a project landed where it did, what caused an overrun, or how to plan the next project.

### What a first study costs

Each option is one or two of the repository's work packages: the data are free and open, and the cost is the
work of assembling a table and one review by the accountable lead. The smallest, an example page on the Kitchenham-CSC projects, is one
package; a study on agile sprint data with quality measures, or on the UK's major-projects data, is two.

## Part two: in the method's terms

### The mapping (G1)

| Side | Attribute (raw) | Metric (larger is better, strictly positive) | Conditioning, reported | Needs from a dataset |
|---|---|---|---|---|
| time | `1 - actual duration / planned duration` (share of plan) | the share plus a shift `s` | `LogAffinePreconditioner(orientation=+1, shift=s)`, `s` a round number above the worst overrun ratio minus one (10 for Kitchenham-CSC, whose worst ratio is 8.9); the alternative, plan over actual with shift 0, is a rung of the ladder | a planned and an actual duration (or start, planned end, actual end) per unit |
| money | `1 - actual cost / planned cost` (effort where effort is the budget) | likewise | likewise, the same `s` | a planned and an actual cost or effort per unit |
| scope | story points delivered (agile), else the dataset's own measure (function points here) | as recorded | orientation +1, shift 0; the unit floats between teams, which the standard scaler of the log absorbs within one portfolio | delivered size per unit |
| quality j = 1..m | each measure, oriented: a count of defects becomes days between them, or is inverted (orientation -1) | as recorded or inverted | orientation per measure; a shift only where a measure reaches zero (a release with no escaped defect) | the measure at the same grain |

Every metric is strictly positive after its shift and larger-is-better by its orientation (R-2, against
`docs/user-guide/conditioning.md`): the shift is the documented "decision about where the scale begins", and the
ladder reports how the reading moves with it. The units a dataset allows are the project (Kitchenham-CSC, public
portfolios), the release, and the sprint (agile archives, where time and cost are fixed by the time box and scope
floats). The fit is asked: which sides are in the contending set (the n of the n-lemma, here
n ≤ 3 + m); whether the near-frontier association between two sides is negative (traded) or positive
(aligned); whether one term or two describes the portfolio (do project types face different frontiers); and where
each quality metric's exponent sits.

### The fit on Kitchenham-CSC (D-4)

Script `case/kitchenham.py`, results `case/results_kitchenham.json`, source record `case/manifest.toml`
(doi:10.5281/zenodo.268457, CC BY 4.0, 7,877 bytes, sha256 `0832342b…2ac0`; downloaded to the git-ignored
`case/data/`, nothing committed). Rows: 141 of 145 (three with no estimated completion date, one whose estimated
completion precedes its start).

- **Conditioning:** time and money as share of plan with shift 10 (the worst shifted value 2.1), scope as delivered
  function points, standard scaler of the logs.
- **Fit temperature:** `select_temperature` at a tenth of rows above the frontier: tau = 22.8; 9.2 percent above.
- **K = 1:** exponents 0.71 (time), 0.18 (money), 0.11 (scope). Contending set at tau = inf: all three, a trilemma.
- **Near-frontier band:** 1 / tau = 0.044 holds fewer than 15 projects; widened to 0.047, the smallest band that
  holds 15 (`case/casekit.py` records every widening). Association: time and money +0.43, time and scope -0.71,
  money and scope -0.92. The closure effect makes negative association likely among contending metrics; the positive
  one between time and money is the stronger evidence, of alignment.
- **K = 2:** the second term owns no near-frontier project (term shares 1.0 and 0.0); the mean level below the
  frontier (`mean_slack_`, a fit quantity, not a project's slack) falls from 0.345 to 0.271, from the far rows.
  One term.

**The ladder** (one change each; exponents and association in the order time, money, scope; the last column is the
smaller K = 2 term's share of the near-frontier projects):

| Rung | n | tau | Exponents | Contending | Assoc. T·B, T·S, B·S | Near | 2nd term |
|---|---|---|---|---|---|---|---|
| primary: shift 10, standard | 141 | 22.8 | 0.71, 0.18, 0.11 | T B S | +0.43, -0.71, -0.92 | 15 | 0.00 |
| robust scaler | 141 | 8.3 | 0.35, 0.19, 0.46 | T B S | +0.52, -0.74, -0.88 | 17 | 0.17 |
| no scaler | 141 | 196.6 | 0.52, 0.48, 0.00 | T B | -0.85, +0.19, +0.05 | 15 | 0.00 |
| shift 20 | 141 | 17.7 | 0.62, 0.23, 0.15 | T B S | +0.41, -0.68, -0.92 | 15 | 0.00 |
| shift 40 | 141 | 17.7 | 0.59, 0.24, 0.17 | T B S | +0.28, -0.66, -0.86 | 15 | 0.00 |
| cap overrun at 3, shift 3 | 141 | 13.7 | 0.51, 0.28, 0.21 | T B S | +0.13, -0.48, -0.88 | 15 | 0.00 |
| plan over actual, no shift | 141 | 5.0 | 0.39, 0.21, 0.40 | T B S | +0.50, -0.68, -0.90 | 19 | 0.15 |
| development projects only | 50 | 22.8 | 0.59, 0.15, 0.26 | T B S | +0.27, -0.65, -0.70 | 15 | 0.00 |
| type P projects only | 73 | 62.8 | 0.93, 0.05, 0.02 | T B S | -0.74, -0.64, +0.09 | 15 | 0.00 |
| client 2 only | 113 | 37.8 | 0.83, 0.12, 0.05 | T B S | -0.10, -0.82, -0.41 | 15 | 0.25 |

Held: the trilemma in 9 of 10 rungs; in the six rungs on the whole portfolio with a scaler, scope negative against
both slacks (-0.48 to -0.92) and the two slacks positive (+0.13 to +0.52). Moved: every exponent (time 0.35 to 0.93).
Without a scaler the shifted slacks' log-spreads (0.14, 0.07) are a tenth of scope's (1.07) and the fit becomes a
time-against-money dilemma: a reading of the scale, not of the projects. The subsets of one project type and one
client read time against money; whether that is a different portfolio or 73 and 113 rows being too few is open.

**Data caveats.** 24 percent of the projects end exactly on their estimated completion date, which suggests the date
was sometimes recorded as, or revised to, the actual; one company, one decade, effort standing for money.

### The synthetic case (D-3, summary)

`synthetic.md` and `case/synthetic.py`: 300 projects, m = 2, a planted two-term frontier (the triangle; defects
against scope and time) and a planted non-participant (acceptance). Conditioned as plan over actual, K = 2 recovers
both terms within 0.07 in L1 at noise 0.05 (0.18 at 0.15); K = 1 averages them into a compromise. Conditioned as share
of plan with the shift, the triangle term's budget exponent rises from the planted 0.33 to 0.42 to 0.57: the shift
bends a planted monomial, so it belongs in any study's ladder. A study needs on the order of hundreds of units before
a second term is readable; Kitchenham-CSC's 141 did not carry one.

### The n = 3 + m reading

On Kitchenham-CSC, m = 0 and n = 3 by the contending set, while the association reads two blocks: time and money
aligned, scope against them. A contending set of three does not mean three independent sides. The reading the
programme would bring to a PMP is the pair: which sides contend, and which of the contenders move together.

### Two findings about the package

- `plot_ternary` labels the one-term triangle "schedule slack trades against budget slack" from the two largest
  exponents (`case/figures/kitchenham-ternary.png`), where the near-frontier association of those two is +0.43: the
  words read the model's weights, not the trade among projects, and the ternary does not show this result.
- At about 141 rows a tenth above the frontier leaves fewer than ten rows inside 1 / tau in some rungs, and
  `trade_off_report` raises; every portfolio study needs the band rule stated (here: widen to 15 rows, recorded).
  The contending set at tau = inf, on the synthetic rows, includes the planted non-participant at a fit-temperature
  exponent of 0.00 to 0.07 in every run.

## The options

| | A. The three sides on real projects | B. Scope and quality in agile sprints | C. A public major-projects portfolio |
|---|---|---|---|
| **Data or generator** | Kitchenham-CSC (doi:10.5281/zenodo.268457, CC BY 4.0), fetched and hashed; the synthetic generator for the ladder's calibration | TAWOS (doi:10.5522/04/21308124, Apache 2.0), a 637 MB MySQL dump | UK GMPP annual data (OGL v3.0), the March 2024 file and earlier years, joined by project ID |
| **Metrics** | schedule slack, budget slack (effort), scope (function points); m = 0 | schedule slack per sprint (planned against completed end), delivered story points, m = 2 to 3: days between bugs raised, share not reopened, estimate stability | budget slack (in-year baseline against forecast), schedule slip (end date across years), scope as baseline benefits; quality the IPA delivery confidence (three levels) |
| **Unit** | project (141) | sprint (thousands across 44 projects) | project-year (227 projects in 2024) |
| **Questions in PM terms** | Do time and money move together and against scope at the edge? Is the exchange rate quotable? Do project types face different edges? | Where does quality sit when time and cost are fixed by the sprint: traded for scope, or free? Do projects share one edge? | Do major government projects that hold budget lose schedule or benefits? Does a Red rating mark projects far inside the edge? |
| **Analysis plan** | the arc of `notes/examples-template.md`: rows, attributes, the question, the fit with the ladder, the reading | the same arc; a parser for the dump; per-project and pooled fits; the generator's sample-size ladder first | the same arc; the year-to-year join; the rating as a colour, not a metric, if three levels are too coarse |
| **Deliverable** | an example page in this repository (`docs/examples/`, with a derived table the licence allows) | a study of its own (a work package, its notebook and a derived sprint table) | a study of its own |
| **Cost** | one package | two packages (the sprint table; the fit and its page) | two packages (the panel; the fit and its page) |
| **What would make it fail** | the reading depends on the scoring beyond the direction (the exponents already do); the exact-on-date pile-up drives the edge | sprints closed on their planned date leave time with no variation; bugs cannot be tied to sprints | slips cannot be joined across renamed projects; too few rated projects (115 of 227 in 2024) |
| **What it tells a PE and PMP** | a measured answer, on real projects, to which sides the best projects traded | whether quality is the side agile teams spend when the time box holds | whether the public portfolio's best projects buy schedule with money or with benefits |

## The assessment

The materials are too sparse for a research programme now. No open dataset found carries all three sides and a
quality measure at one grain; the best real table, Kitchenham-CSC, is 141 projects of one company in the 1990s, has no
quality measure, and fixes the direction of the trade but not its rate; the agile archives carry scope and quality
but no money; the public portfolios carry money, time and a coarse rating, and need years joined before they carry a
plan. The recommendation is smaller cases integrated into the examples: option A first, as an example page whose
reading is the direction and whose ladder is shown. Option B is the one case that could grow into a programme: if
sprint data give a stable reading of where quality sits, a programme across agile archives, public portfolios and a
partner's own project records (the many-examples programme his direction sketches) would have its first result to
build on, and its scope would be written then.

## The cold read (R-4)

A context-gapped reader in persona P1 (the accountable decision maker), briefed as a COO who is a PE and PMP, was
given part one and Figure 1 only, on 2026-11-16. The three sentences, verbatim:

1. "The data covers 145 software projects that Computer Sciences Corporation ran between 1994 and 1999. For each one
   it gives planned and actual effort and duration, plus delivered function points. 141 of them are usable, and none
   has a quality measure."
2. "The study tested whether the best projects trade time, cost and scope against each other, and whether quality
   measures act as extra sides of the triangle."
3. "Among the projects nearest the best edge, extra scope cost time and money together, and time and money moved
   together. So the triangle behaved like two sides, but the rate of exchange between them is not settled."

**Match.** The data and the finding match. The reason half-matches: the question of quality as further sides is the
programme's, and this data has no quality measure, which the reader states in sentence 1 and folds into sentence 2.
The reader would fund the smallest step ("one work package on free, open data").

**What the reader stopped at, and what changed.** "slack, time and money as one, against scope" (reworded: time and
money together on one side, scope on the other); "one weight per side" with no meaning in management terms (a
sentence now says what a weight is and that trades are read from co-movement, not weights); "scorings" undefined until
item 5 (defined at its first use); the subset sentence, "exactly the sentence that decides whether I trust the
method", left unexplained (now gives each subset's size, what changed, and that the data cannot say why); "the
supervisor's read" (now "one review by the accountable lead"); the figure's "trilemma (3 metrics contend)" title and
outlined diagonal unexplained (the caption now names both). Not changed: the diagonal 1.00 cells, which the package's
figure draws. The quoted sentences are of the text before these edits; a second cold read was not run.

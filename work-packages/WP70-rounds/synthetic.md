# WP70 D-3 — The synthetic portfolio: a generator built to the n = 3 + m story

The generator writes a portfolio as a project office would hold it, with a planted answer the fit can be scored
against. What D-4 needed is implemented in `case/synthetic.py`; the rest is design.

## What one row is

One project: a planned duration and its actual, a planned budget and its actual, the story points delivered, and m
quality metrics. The implemented case has m = 2:

| Column | Meaning | Unit | Larger is better |
|---|---|---|---|
| `plan_days`, `actual_days` | planned and actual duration | days | the ratio plan / actual |
| `plan_cost`, `actual_cost` | planned and actual cost | thousands | the ratio plan / actual |
| `story_points` | scope delivered | story points | yes |
| `defect_interval_days` | mean days between escaped defects after release | days | yes |
| `acceptance` | user-acceptance score | score, about 7 at the centre | yes |

## How it is drawn

1. **The planted frontier.** The larger-is-better quantities (plan over actual for time and money, story points, the
   two quality metrics) are drawn by the package's `make_frontier_data` around a planted two-term frontier: 300
   projects, 30 percent on the frontier with log-noise `noise`, the rest inside it at a mean depth of 0.5 in log V.

   | Term | schedule | budget | scope | defect interval | acceptance | Story |
   |---|---|---|---|---|---|---|
   | 1 | 0.30 | 0.30 | 0.40 | 0 | 0 | the iron triangle: time, money and scope trade; quality free |
   | 2 | 0.25 | 0 | 0.25 | 0.50 | 0 | defects against scope and time: a project that ships more, sooner, ships more defects |

   The acceptance score is in neither term: a planted non-participant, which a fit should leave out.
2. **Raw units.** Each log quantity is standardized and given a typical spread and centre (log-spread 0.25 for time,
   0.30 for money, 0.8 for story points, 0.6 for the defect interval, 0.15 for acceptance; centres 1, 1, 120 points,
   30 days, 7). The planted exponents, as a standard scaler of the raw logs sees them, are the planted ones times each
   column's log-spread before the rescaling, renormalized: term 1 (0.31, 0.33, 0.36, 0, 0) and term 2 (0.26, 0, 0.23,
   0.51, 0) at noise 0.05.
3. **Plans and actuals.** Planned durations are log-normal around 90 days (log-sd 0.4); planned cost is about 4
   thousand per story point (log-sd 0.2). The actuals are the plans divided by the drawn plan-over-actual ratios, so
   an overrun is a ratio below one.
4. **Slack as the project office reports it.** Slack is `1 - actual / plan`, a share of the plan, negative for an
   overrun. The worst overrun in the drawn portfolio is 3.28 times plan (noise 0.05) and 3.26 (noise 0.15).

## The conditioning, a choice reported

Two conditionings of the same rows, both with orientation +1 and a standard scaler of the logs:

- **Plan over actual** (no shift): the log of the ratio is the log overrun with its sign turned. This is the form in
  which the planted frontier is a monomial, so it is the form that can recover it.
- **Share of plan with the package's shift**: `1 - actual / plan + s`, with `s` the smallest whole number above the
  worst overrun (4) and four times that (16). The shift keeps every overrun strictly positive, as he asked; it is not
  a power of the ratio, so the planted monomial is bent.

## What it shows (the runs of `case/results_synthetic.json`)

| Noise | Conditioning | K = 2 term matching the iron triangle | K = 2 term matching defects | L1 distance to planted (triangle, defects) |
|---|---|---|---|---|
| 0.05 | plan over actual | 0.31, 0.31, 0.35, 0.01, 0.02 | 0.24, 0.01, 0.24, 0.50, 0.00 | 0.05, 0.07 |
| 0.05 | share, shift 4 | 0.26, 0.47, 0.24, 0.02, 0.01 | 0.29, 0.03, 0.23, 0.45, 0.00 | 0.33, 0.11 |
| 0.05 | share, shift 16 | 0.28, 0.42, 0.27, 0.02, 0.01 | 0.28, 0.02, 0.23, 0.46, 0.00 | 0.25, 0.10 |
| 0.15 | plan over actual | 0.32, 0.29, 0.32, 0.00, 0.07 | 0.24, 0.03, 0.25, 0.48, 0.01 | 0.11, 0.18 |
| 0.15 | share, shift 4 | 0.19, 0.57, 0.20, 0.00, 0.04 | 0.33, 0.07, 0.24, 0.36, 0.01 | 0.56, 0.29 |
| 0.15 | share, shift 16 | 0.30, 0.42, 0.22, 0.00, 0.05 | 0.23, 0.08, 0.27, 0.42, 0.00 | 0.29, 0.23 |

(Exponents in the order schedule, budget, scope, defect interval, acceptance.)

- **A planted answer recovered.** Under plan over actual, K = 2 finds both terms within 0.07 in L1 at noise 0.05 and
  within 0.18 at noise 0.15; the acceptance score's exponent is at most 0.07. The two terms each hold about half the
  near-frontier projects, and the mean level below the frontier falls from 0.458 (K = 1) to 0.315 (K = 2).
- **One term cannot say it.** At K = 1 the weights are spread over four metrics (0.26, 0.15, 0.29, 0.29, 0.02 at
  noise 0.05): the triangle and the defect trade averaged into one compromise that no planted project obeys.
- **The conditioning's effect.** The shifted share keeps every project positive and bends the triangle term: budget
  slack's exponent rises from the planted 0.33 to 0.42 to 0.57, more so at the smaller shift and the higher noise.
  The defect term, which has no budget in it, moves less. The shift is therefore read as part of the question.
- **A finding about the report.** The contending set at the exact maximum (tau = inf) is the support of a linear
  program on each term's rows; on these rows it includes the planted non-participant in every run, at exponents of
  0.00 to 0.07 at the fit temperature. On finite noisy rows the fit-temperature exponents, not the tau = inf
  support, separate the planted non-participant.

## What it cannot show

Anything about real projects: the trade-offs, their exponents, the number of terms and the noise are the generator's
inputs, so the fit returns them. It tests the method and the conditioning against a known answer, and calibrates
how many projects and how much noise a study needs; it does not test the iron triangle.

## Not implemented (design only)

- **More quality metrics** (m = 3 to 5: escaped defects per point, rework share, availability after release) with a
  planted non-participant among them.
- **Agile time boxes:** a sprint generator whose duration and cost are fixed and whose scope floats, to show what the
  fit says when two sides carry no variation (the case of the sprint archives in `datasets.md`).
- **The project office's rounding:** a share of projects reported exactly on plan (24 percent of Kitchenham-CSC's
  schedules are), to measure what that pile-up does to the frontier.
- **A sample-size ladder:** n = 50, 100, 300, 1000, to say how many projects a real study needs before K = 2 is
  readable (Kitchenham-CSC's 141 did not carry a second term).

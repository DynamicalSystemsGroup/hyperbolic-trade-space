# WP76 verification record: Kitchenham-CSC software projects, scope against slack

Written to verify the example against its scope (`work-packages/WP76-scope-of-work.md`, R-1 to R-12), reported whether
it passes or not. Every number is read from `examples/kitchenham/results.json` and `examples/kitchenham/variants.json`,
which `tests/test_wp76_kitchenham.py` holds equal to the page and to this record.

## 0. This case's row of the coverage matrix (`work-packages/examples-coverage.md`, second table)

| Counts | K, fit | Origin | Stage | Method |
|---|---|---|---|---|
| 10 recorded columns; 3 metrics (schedule slack, budget slack, scope); project type and client the covariates; objectives: none posed | K = 1 of record; K = 2 tested, its second term holds no near-frontier project; soft (band 0.047 at tau 22.8, widened from 1/tau = 0.044 to hold 15 of 141) | measured | project management, finished projects | actual, the company's own records of plans and actuals |

## 1. What was expected before the run (from the WP70 probe, `git show 4f81a4ea:work-packages/WP70-rounds/pitch.md`)

The memo's findings to reproduce and assess, not acceptance outcomes: on 141 projects, at the primary conditioning,
all three sides in the contending set; near the frontier scope against both slacks and the two slacks together; one
term; the direction held across the scaled scorings and the exponents moved; two subsets read differently. The
headline the page may state is decided by section 4, not by this expectation.

## 2. Source and reproduction (G1, R-1, R-7)

- **Source.** Zenodo record 268457, `kitchenham.arff`, 7,877 bytes, md5 `8945f95d3bbfc40df4687089767aae16`, sha256
  `0832342b248418cca324cebe77d86d2f90ae223c1119af9360783bdbad0b2ac0`, CC BY 4.0, uploaded by Masateru Tsunoda
  2017-02-03 (the Zenodo API, read 2026-11-17). The file fetched on 2026-11-17 matched the WP70 manifest of 2026-11-16 in
  size and both hashes. The paper is Kitchenham, Pfleeger, McColl and Eagan, JSS 64(1), 2002,
  doi:10.1016/S0164-1212(02)00021-3 (Crossref, 2026-11-17; `docs/references.bib`, `kitchenham2002empirical`).
- **Exclusions.** 145 rows; three have no estimated completion date and one's estimated completion precedes its
  start, so their planned duration is missing or negative; 141 kept. The rule is `KeptProject` in
  `examples/kitchenham/kitchenham.sysml` (planned duration above `plannedDurationBound` = 0), applied by `run.derive`.
  Ten of the 141 carry no project-type code (they are in the whole-portfolio fits and in no type subset).
- **Artefact.** The derived table `examples/kitchenham/derived/projects.csv` (141 rows: project, client, type, the
  plans, the actuals, the overrun ratios, the three attributes) is committed with `LICENCE-DATA.txt` beside it, as the
  licence allows; the source file itself is fetched into the git-ignored `examples/kitchenham/data/` and verified.
- **Package and commit.** `results.json` records `package_version` 0.1.0 (`hyperbolic_trade_space.__version__`) and
  the Git SHA of the run (`provenance.git_sha`, with `git_dirty`); the SHA is of the tree the run was made on, which
  precedes the commit that carries the file.
- **Reproduction.** `uv run python examples/kitchenham/run.py --check` refits from the committed derived table and
  compares every key of `results.json` but the provenance with a fresh run: reproduced. The same run on the file of
  record (`--fetch`) rewrote the derived table and the results without a diff. The WP70 numbers of 2026-11-16
  (package at 4bf40d31) and the 0.1.0 numbers agree to every digit quoted: tau 22.80, exponents 0.706, 0.184, 0.110,
  band 0.0468, 15 near, association +0.43, -0.71, -0.92, K = 2 shares 1.0 and 0.0, mean slack 0.345 to 0.271.

## 3. Counts and the conditioning rule

141 projects: 50 of type D (development), 73 of type P (perfective maintenance), 4 A, 2 C, 1 Pr, 1 U, 10 with no
code; client 2 has 113, client 1 has 16, the other four clients 12 together. Medians: 275 function points, on the
planned date (24.1 percent exactly on it; 63 percent on or under), 97 percent of the effort estimate (67 percent on or
under). Worst overruns: 8.89 times the planned duration, 5.93 times the first estimate. Over all rows the log overrun
ratios and log function points correlate weakly (0.16 to 0.22).

Rule (the model's `primary`): schedule slack and budget slack as shares of plan with shift 10 (the smallest shifted
value is 2.1), scope as adjusted function points unshifted, orientation +1 for all three, standard scaler of the logs;
the fit temperature at a tenth of projects above V = 1 (bounds 3 to 10^4); the near-frontier band the larger of
1/tau and the smallest band holding 15 projects.

## 4. The fit, the sensitivity checks and the verdict (G3, R-3, R-4, R-9)

**Baseline (K = 1).** tau = 22.8 (9.2 percent above). Exponents 0.71 (schedule slack), 0.18 (budget slack), 0.11
(scope); contending set all three (n = 3). 1/tau = 0.044 holds 12 projects; the band is widened to 0.047, holding 15.
Association among the 15: schedule slack with budget slack +0.43; schedule slack with scope -0.71; budget slack with
scope -0.92.

**The two-term alternative (K = 2 at tau = 22.8, five restarts, seed 0).** Terms (0.75, 0.15, 0.10) and (0.00, 0.64,
0.36); shares 1.00 and 0.00 (the second term holds no near-frontier project); mean slack 0.271 against 0.345 at
K = 1, the fall coming from rows far below the frontier; status certified. The per-term report at the band 0.047
refuses on the first term (9 rows inside the band at K = 2, guard 10): recorded, not worked around. One term describes
the portfolio.

**The conditioning ladder** (exponents and associations in the order schedule slack, budget slack, scope; T·B the
two slacks, T·S and B·S scope against each):

| Rule | tau | Exponents | Set | T·B | T·S | B·S | Near (band) | K = 2 shares | Pattern |
|---|---|---|---|---|---|---|---|---|---|
| primary (shift 10, standard) | 22.8 | 0.71, 0.18, 0.11 | 3 | +0.43 | -0.71 | -0.92 | 15 (0.047, widened) | 1.00, 0.00 | holds |
| robust scaler | 8.3 | 0.35, 0.19, 0.46 | 3 | +0.52 | -0.74 | -0.88 | 17 (0.121) | 0.83, 0.17 | holds |
| no scaler | 196.6 | 0.52, 0.48, 0.00 | 2 | -0.85 | +0.19 | +0.05 | 15 (0.006, widened) | 1.00, 0.00 | fails |
| shift 20 | 17.7 | 0.62, 0.23, 0.15 | 3 | +0.41 | -0.68 | -0.92 | 15 (0.070, widened) | 1.00, 0.00 | holds |
| shift 40 | 17.7 | 0.59, 0.24, 0.17 | 3 | +0.28 | -0.66 | -0.86 | 15 (0.086, widened) | 1.00, 0.00 | holds |
| cap at 3, shift 3 | 13.7 | 0.51, 0.28, 0.21 | 3 | +0.13 | -0.48 | -0.88 | 15 (0.078, widened) | 1.00, 0.00 | holds |
| plan over actual | 5.0 | 0.39, 0.21, 0.40 | 3 | +0.50 | -0.68 | -0.90 | 19 (0.201) | 0.85, 0.15 | holds |

Held on the six scaled rules: scope against both slacks (-0.48 to -0.92), the slacks together (+0.13 to +0.52), all
three contending. Without a scaler the shifted slacks' log-spreads are a tenth of scope's and scope's exponent is
0.00: a reading of the scale. Moved: every exponent (schedule 0.35 to 0.71, budget 0.18 to 0.28, scope 0.11 to 0.46
across the scaled rules).

**The band ladder** (the primary fit; the association recomputed at each band):

| Band | log V | Near | T·B | T·S | B·S | Pattern |
|---|---|---|---|---|---|---|
| 1/tau | 0.044 | 12 | +0.66 | -0.82 | -0.95 | holds |
| 10 rows | 0.040 | 10 | +0.67 | -0.85 | -0.95 | holds |
| 15 rows (the rule) | 0.047 | 15 | +0.43 | -0.71 | -0.92 | holds |
| 20 rows | 0.066 | 20 | +0.31 | -0.65 | -0.85 | holds |
| 25 rows | 0.086 | 25 | +0.17 | -0.53 | -0.82 | holds |

The pattern holds at every band; the slacks' association thins from +0.67 to +0.17 as the band widens, scope's
negative associations weaken but keep their sign.

**Influential observations.** Leave-one-out over the 141 projects at tau = 22.8 (the temperature held so the change
is the row's; the band rule reapplied): 140 of 141 refits hold the pattern. Project 16 is the exception: without it the
15-row band takes in a different set and the slacks' association is -0.20 (scope's -0.42 and -0.66); its removal also
moves schedule slack's exponent by 0.05. Project 138 moves an exponent by 0.051; no other row reaches 0.05. Across the
141 refits the slacks' association ranges -0.20 to +0.66, schedule slack with scope -0.82 to -0.42, budget slack with
scope -0.94 to -0.66. The named extremes, removed with the temperature reselected:

| Removed | tau | Exponents | T·B | T·S | B·S | Near | Pattern |
|---|---|---|---|---|---|---|---|
| project 102, the largest (18,137 function points) | 17.7 | 0.73, 0.18, 0.09 | +0.10 | -0.52 | -0.77 | 21 | holds |
| project 32, the worst schedule overrun (8.9x) | 12.1 | 0.37, 0.43, 0.20 | +0.38 | -0.66 | -0.91 | 18 | holds |
| project 69, the worst budget overrun (5.9x) | 17.7 | 0.82, 0.07, 0.11 | +0.26 | -0.75 | -0.68 | 17 | holds |

The worst schedule overrun sets the primary shift (10 is the round number above 8.9) and its removal moves the
exponents most (schedule slack 0.71 to 0.37, budget slack 0.18 to 0.43); the signs do not move.

**The subsets** (the primary rule refitted):

| Subset | n | tau | Exponents | T·B | T·S | B·S | K = 2 shares | Pattern |
|---|---|---|---|---|---|---|---|---|
| type D, development | 50 | 22.8 | 0.59, 0.15, 0.26 | +0.27 | -0.65 | -0.70 | 0.00, 0.00 | holds |
| type P, perfective maintenance | 73 | 62.8 | 0.93, 0.05, 0.02 | -0.74 | -0.64 | +0.09 | 1.00, 0.00 | fails |
| client 2, the largest | 113 | 37.8 | 0.83, 0.12, 0.05 | -0.10 | -0.82 | -0.41 | 0.75, 0.25 | fails |

In the two larger subsets the two slacks run against each other and schedule slack carries almost the whole exponent
vector; scope stays against schedule slack in all three. Whether these are different portfolios or too few rows to
read, the data do not say. The type-D K = 2 fit reports both term shares as 0.00 (no near-frontier project under
either term's band at K = 2): recorded as returned.

**Verdict on the headline (R-3).** The negative half (more scope with less schedule slack and less budget slack
near the frontier) holds on every scaled rule, every band, every leave-one-out refit and every extreme. The positive
half (the two slacks together) holds on the six scaled rules, every band and 140 of 141 refits, thins to +0.17 at
the widest band and +0.10 without the largest project, turns negative without project 16, and reverses in the
type-P and client-2 subsets. The page states exactly that: the first half without qualification over those checks,
the second as "most readings, weakly or not in some", naming the band, the one project and the two subsets.
`test_page_states_the_headline_only_where_the_checks_hold` pins the scope of the statement to the rows of the
tables above.

## 5. The two figures through the figure loop (G4, R-10)

Figure 11 (`kitchenham-pairs`): the three pairs of conditioned log-metrics with the 15 near-frontier projects
marked and each pair's association in the panel title; the frame holds the projects from the 2nd percentile up and
says how many lie beyond it (6, the worst overruns). Intent written first: shared movement in the slack pair,
substitution in the two scope pairs, read from the marked points. Figure 12 (`kitchenham-participation`): each
metric's one-term exponent under the seven rules, hollow where the metric is outside the contending set. Intent:
participation shown apart from association, and the exponents' movement with the rule. No ternary: its region label
reads the two largest exponents as trading (schedule slack against budget slack) where their association is +0.43
(the WP70 defect, re-checked on this fit: `_ternary_says` returns "schedule slack trades against budget slack"), so
the ternary would show the opposite of the reading. Cold reads and captures: section 7.

## 6. Limits

One company, one decade, effort for money; 24 percent of the projects end exactly on their estimated date; ten
projects without a type code; no quality measure, so nothing about quality as a further side (OD1). The band rule
is a choice (15 rows) and the band ladder shows what it does. Not asserted: a cause for any project's position, a
rate of exchange between scope and slack, or anything beyond this portfolio.

## 7. The reads and the captures (R-5, R-10, R-11)

**The figure loop (2026-11-17).** Two fresh-context readers per figure, given the image alone, then the caption;
one reader of each pair in the persona of a project manager. Intent written before the reads: Figure 11, shared
movement in the slack pair and substitution in the two scope pairs, read from the marked points; Figure 12,
participation shown apart from association, with the exponents' movement across the rules.

- Figure 11, reader 1 (light image): "I take it that the highlighted points move together in the first pair and trade
  off against each other in the other two, most strongly in budget vs scope." Ink as data "roughly 60 to 70 percent";
  labels readable, "tick labels and legend text are small"; confused by "near the frontier", "association" and "6
  beyond the frame"; the far point in the scope panels "unclear whether it is an outlier or meaningful". Caption:
  "partly changed my reading ... positive means shared movement, negative means substitution."
- Figure 11, reader 2 (dark image, PMP persona): "the pairs move together a bit in the first plot (+0.43) but trade
  off against each other in the second and third (-0.71, -0.92)." Ink "most of it"; the pale text of the dark image
  hard to read outside a dark page; "the legend text is cut off ('near the frontier (' ends abruptly)"; confused by
  "standardized", "association", "6 beyond the frame", "frontier". Caption: "helped ... I now read the left plot as
  'shared movement' and the other two as 'substitution'."
- Figure 12, reader 1 (light): "the exponents change with the rule, and that scope drops to exactly 0 under 'no
  scaler', where its marker is hollow." Ink "about 75 to 80 percent"; labels legible; the legend title "only a
  fragment"; "participation apart from association is cryptic". Caption: confirmed the hollow marker, did not change
  the substance.
- Figure 12, reader 2 (dark, PMP persona): "the three project levers get different weights depending on the rule,
  with schedule slack usually the largest and scope the smallest." Ink "about 75-80%"; the dark image's pale text
  hard to read outside a dark page; "exponent at one term means nothing to me"; the legend title unexplained.
  Caption: "mostly labels the chart rather than explaining it."

Both figures passed the sentence test (the intent was read from the image by all four before the caption) and the
ink test; the disposition for each is the smallest change: Figure 11, the legend moved to the lower left of the first
panel, where it no longer runs into the marked points, and the per-panel "6 beyond the frame" replaced by one line
under the panels, "6 projects, the worst overruns, lie beyond the frames"; the caption says the association is a
correlation. Figure 12, the legend title completed ("filled: in the contending set; hollow: outside it") and the
caption rewritten to say what is read here and what from Figure 11. The terms the readers stopped at ("frontier",
"contending set", "standardized", "exponent at one term") are the page's, defined or linked to the glossary in the
paragraph above each figure, not the figure's to define. The pale text of the dark images is the site's dark scheme
(light text on the dark page; the images are transparent), judged on the rendered page below. No redraw.

**Shows, does not show, good for.** Figure 11 shows how each pair of metrics moves among the fifteen projects
nearest the frontier; it does not show the frontier itself, the exponents, or a cause; it is good for telling shared
movement from substitution at a glance. Figure 12 shows each metric's exponent under each rule and whether it is in
the contending set; it does not show which way metrics move together or how far a project is from the frontier; it
is good for seeing that participation holds while the exponents move with the conditioning.

**The project-management cold read (R-5)** and **the captures (R-11)**: below, filled at the browser pass.

## 8. What this changes for the method

A portfolio of a hundred-odd rows needs its band rule stated: 1/tau held 12 projects here and fewer on other rungs.
The association of two metrics among fifteen rows can turn on one project outside the band, so the leave-one-out
table belongs beside any association read from a small near-frontier set. The ternary's region label is not a
reading of co-movement (package defect, `WP76-decisions.md`).

# WP56 figure loop, depths one and two: Figure 7 (the tension matrix) and the decision-maker's ternary

The loop of `notes/figure-review.md` at its first two depths (the figure alone; the figure with its caption), first
unit of WP56. Every PNG here is the light theme at 100 dpi, as the paper shows it. The numbers below are read from
`tension-values.txt` and `ternary-values.txt`, written by `tension_rounds.py` and `ternary_rounds.py` beside this
file on the data of record (`examples/adcs/data/v2/`, unchanged). Cold readers were fresh-context agents given the
image path alone, then the caption file; their findings are quoted or summarised per round.

## Figure 7, the tension matrix

**Recipe.** Question: on each term of the case's K = 2 fit, how many units of one metric does a unit of another cost
at the term's balanced point? Takeaway: the costs are ordered and one-sided; a metric whose unit is worth much on the
term costs several units of the light ones (depth of discharge, total mass). Sentence: every drawn value is -1 or
less, from -1.1 to -17 on term 1 and from -1.0 to -30 on term 2.

**The values, computed first** (`tension-values.txt`; `|T|` is the size of a cell, `T[i, j] = dm_j/dm_i`):

| term | row order | upper half: min, max of \|T\|; cells below one | lower half: min, max; cells above one |
|---|---|---|---|
| 1 | exponent | 0.683, 17.283; 4 of 28 | 0.058, 1.464; 4 of 28 |
| 1 | tension | 1.081, 17.283; 0 of 28 | 0.058, 0.925; 0 of 28 |
| 2 | exponent | 0.529, 30.131; 1 of 28 | 0.033, 1.891; 1 of 28 |
| 2 | tension | 1.013, 30.131; 0 of 28 | 0.033, 0.987; 0 of 28 |

So the withdrawn claim (rows by exponent, every upper value at least one) is false on this fit: five upper cells are
below one (term 1: peak slew power against pointing error 0.925, unit cost against available power 0.734
and against momentum headroom 0.816, fleet cost against momentum headroom 0.683; term 2: momentum headroom against
pointing error 0.529). The order that makes every upper cell at least one exists and is exact: `|T[i, j]| = s_i / s_j` with
`s_i = w_i / m_i` at the balanced point (the formula of `tension_matrix`, L21), so sorting by `s`, largest first,
puts every cell right of the diagonal at `s_i/s_j >= 1`. `case.tension_order(..., "tension")` sorts by the mean of
`log|T[i, j]|` over the row, which is `log s_i` less a constant.

**Choice: the upper triangle, rows and columns in the "tension" order** (`triangle="upper", order="tension"`). It is
the one arrangement whose values the caption states in one sentence without exceptions (all -1 or less; the range per
term); in exponent order a sentence about the range needs a list of the five exceptions. The values then grow
monotonically to the right along each row and upward along each column, which the cold reader of round 4 read off
unprompted ("the cost grows toward low-weight metrics"). The exponent stays on each row label (`w`), so the
exponent order is not lost, only not the sort key. Both options stay in the routine for interactive use (`"both"`,
`"exponent"` the defaults).

**Rounds.**

| round | PNG | what changed | cold read, image alone (finding) |
|---|---|---|---|
| r0 | `tension-r0-both-exponent.png` | the paper's Figure 7 before WP56 (both halves, exponent order) | his read (WP56-decisions.md, 12:30): the reciprocal halves make the reader reverse-engineer 1/x |
| r1 | `tension-r1-upper-exponent.png`, `tension-r1-lower-exponent.png` | one half, exponent order | not read cold; by the values above, a mix of cells above and below one in each half, so no one-sentence range |
| r2 | `tension-r2-upper-tension.png` | upper half, tension order; staircase without the diagonal | not read cold; the colour bar keeps its brown half, which no drawn cell uses |
| r3 | `tension-r3-upper-tension-bar.png` | the colour bar cut to the drawn side (1 upward) | reader 1: "the diagonal also looks shifted, because the first row has no empty cell while the first column label is 'peak slew power' rather than 'pointing error'"; `w=` unexplained; tension undefined; signed cells against an unsigned bar |
| r4 | `tension-r4-upper-tension-diagonal.png` | the grey diagonal kept, so a row and its column meet; the row axis says what `w` is | reader 2: "Every cell is negative (-1.0 to -30), and the shading darkens toward the top-right ... raising the row metric costs the column metric, and the cost grows toward low-weight metrics" |

**Depth two (r4 with the caption draft, reader 2).** The caption resolved the direction (per unit rise of the row
metric), the order and the empty half; the reader checked its numbers against the cells (-1.1 to -17, -1.0 to -30)
and found them matching. Still open for that reader: what `w` is (now on the axis label and in the caption below),
the unsigned colour bar against signed cells (the caption now says the colour is the size), the empty last row (the
diagonal cell of the lightest metric; kept so the diagonal reads), and "balanced point" (defined in the paper's
Definition of tension, depth three). The bar ends at 10^1.3 (about 20): the cells above it (-30 on term 2's top row)
take the end colour; their numbers are printed.

**Tests.** Cold read matches the sentence at r4 (reader 2 above). Sentence test: the figure carries 56 values per
fit in an order a reader can scan, which a sentence cannot. Ink as data: about 45 to 50 per cent of the frame (reader
2); the white lower half is the reciprocal and is not drawn by choice. Legibility at the column: the cell numbers
(9 pt at 100 dpi, the case's floor) and rotated column labels are the smallest type; readable at the full-size link,
small in the column (both readers). Not redrawn for that.

**Shows:** each term's tensions among the metrics with an exponent on it, at its balanced point, as the cost in units
of each lighter metric of a unit of a heavier one. **Does not show:** a design's own tensions, the association among
designs, the reciprocal half (implied), an effect of changing a design variable. **Good for:** reading how many units
of one metric a unit of another costs on each term.

**Caption draft.**

> The tension matrix of each term of the K = 2 fit at the term's balanced point, for the metrics that carry an
> exponent w on the term (the line under each panel names the others). A cell is the change in the column metric per
> unit rise of the row metric's conditioned value along the term, and its colour is the size of that change on a log
> scale. Rows and columns run from the metric a unit of which is worth most on the term to the one worth least. Every
> drawn value is therefore -1 or less: from -1.1 to -17 on term 1 and from -1.0 to -30 on term 2. Each cell left of
> the diagonal is the reciprocal of its mirror image right of it.

## The decision-maker's ternary: fleet cost, unit cost, coverage probability

**Recipe.** Question: do the three stakeholders' objectives (sponsor: fleet cost; manufacturer: unit cost; operator:
coverage probability) pull three ways on this case? Takeaway and sentence (his): the three objectives were not
guaranteed to collapse to one trade-off; on this model they do, because fleet cost is unit cost times fleet size,
with unit cost nearly flat. The figure's part of that sentence: the fit's one term lies on the edge between fleet
cost and coverage probability, with unit cost's exponent near zero. The reason (the identity) is the prose's.

**The values** (`ternary-values.txt`): 2,134 feasible designs of the primary regime, fleet size 1 to 30; fleet cost
over unit cost times fleet size between 0.999999994 and 1.000000005 on every row; coverage probability from 0.0725
to 0.9979. K = 1 (tau 34.791): exponents fleet cost 0.386, unit cost 0.006, coverage probability 0.608. K = 2
(tau 113.219): term 1 0.140, 0.000, 0.860 (share 0.93); term 2 0.537, 0.000, 0.463 (share 0.07). These equal the
spike's coverage row (`WP56-rounds/ternary/readout.md`).

**Choice: one term** (`case.FLEET_TERNARY_K = 1`). At K = 2 both terms sit on the same edge and the cold reader took
the two markers as stakeholders pulling "in different directions"; at K = 1 the cold readers read the one trade-off
between sponsor and operator with the manufacturer's corner idle, which is the sentence. The K = 2 fit says the same
more strongly (unit cost's exponent 0.000 in both terms) and is printed in the values file; the prose may cite it.

**Rounds.**

| round | PNG | what changed | cold read, image alone (finding) |
|---|---|---|---|
| spike | `../ternary/coverage.png` | the spike's figure: formula in the title, no stakeholders | (the spike's own read) |
| r1 | `ternary-r1-k2.png` | the measure named in the title, no formula; each corner names its stakeholder; K = 2 | "The star (term 1) sits near the operator corner and the diamond (term 2) near the sponsor/operator edge, so the stakeholders pull in different directions" |
| r1 | `ternary-r1-k1.png` | the same at K = 1 | "the single star (term 1) sits on the fleet-cost/coverage edge, so the fitted optimum favours sponsor and operator over the manufacturer"; the badge "1" beside the star redundant |
| r2 | `ternary-r2-k1.png` | K = 1, the badge "1" hidden (one term) | reader 2: "the sponsor and operator are in tension and ... the manufacturer's corner is barely involved, since the optimum sits on the sponsor-operator edge" |

**Depth two (r2 with the caption draft, reader 2).** "The caption answers most of what was open ... It also adds
the numbers (0.39, 0.006, 0.61), so unit cost carries almost no weight, and that changes my reading from a hunch into
something stated." Asked whether image and caption say the objectives reduce to one trade-off: "yes ... a single
trade-off between fleet cost (sponsor) and coverage probability (operator), with unit cost (manufacturer) nearly
irrelevant." Still open: that the star is not a design (now in the caption), and V, "conditioned" and "term"
(defined in the paper before Section 8, depth three). Both readers would take the star for "the best design"
without the caption; the legend says "exponent vector of term 1" and the caption now says "not a design".

**Tests.** Cold read matches the figure's part of the sentence at r2. Sentence test: the figure shows where 2,134
designs sit against the fit's one direction and that the manufacturer's corner carries nothing; the sentence alone
would not show the designs' spread toward the unit-cost corner that the fit gives no weight. Ink as data: about 60 to
65 per cent (reader 2), the legend about 15 per cent of the height. Legibility at 500 to 700 px: the legend (9.5 pt) and
the corners' second lines are the smallest type, readable; the dots overprint in the dense band. No equation in
the figure: the title is the three objectives' names.

**Shows:** the three objectives of the fleet, one per stakeholder, the designs placed by their shares, and the one
fitted term's exponent vector on the fleet-cost to coverage-probability edge with its lines of equal V. **Does not
show:** why the trade-off collapses (fleet cost is unit cost times fleet size; the prose and the SysML v2 model),
the coverage probability's definition (the SysML v2 model, `CoverageProbability`), the requirements, a pick.
**Good for:** seeing that the three stakeholders' objectives reduce to one trade-off on this case and which two
stakeholders it sets against each other.

**Caption draft.**

> The fleet's three objectives, one per stakeholder: fleet cost (sponsor), unit cost (manufacturer) and coverage
> probability (operator), fitted with one term over the primary regime's 2,134 feasible designs. A design sits at its
> shares of the three conditioned objectives, a corner being all of the total in one. The star is the term's exponent
> vector, not a design: 0.39 on fleet cost, 0.61 on coverage probability and 0.006 on unit cost, on the edge between
> fleet cost and coverage probability. The thin lines are equal invariant value V at a fixed total, rising toward the
> star.

## Build notes for the review

- The coverage probability is section 5 of `examples/adcs/model_v2/stakeholders.sysml` (`CoverageAssumptions`,
  `coverageAssumptions`, `CoverageProbability`), the file applied after `cubesat.sysml` as one model. Not in
  `cubesat.sysml`: the data of record's ledger entries carry that file's hash (`tests/test_mutation_v2.py` holds the
  current entry to it) and the file is at its line cap (1,200), so an edit there would move the record's link to the
  data with no data change. No other model element changed.
- The case module computes it (`case.coverage_probability`, `case.with_coverage`); the test
  `test_coverage_probability_in_the_model_is_the_pipelines` evaluates the model's calc on the three named
  configurations and a fleet of twelve and holds it to the Python value (relative 1e-12), and the constants equal.
- The spike script `examples/adcs/spikes/fleet_performance.py` and its JSON stay as the record of the comparison
  across the three definitions (the readout cites them); the build does not import them.
- The paper cells (the figure call `case.fleet_ternary_figure()`, Figure 7's
  `case.tension_matrix_figure(study, fit_case, triangle="upper", order="tension")`) and the captions enter the
  notebook in the second phase, after WP55 lands.

## Phase two (after WP55 landed; dev b5b3a86)

### Rounds after the paper call was fixed

| figure | round | PNG | what changed | cold read |
|---|---|---|---|---|
| Figure 7 | r5 | `tension-r5-upper-strict.png` | the driver's call: `triangle="upper"` is strict, no diagonal, the empty last row and first column dropped; the exponent stays on each row label | (the r4 reads stand; the misread of r3, "the diagonal also looks shifted", is answered by the caption's ordering sentence) |
| ternary | r3 | `ternary-r3-k1.png` | corners by what a design there has: "low fleet cost (sponsor)", "low unit cost (manufacturer)", "high coverage probability (operator)", replacing "favours fleet cost", which reads as favouring a high cost | reader 3: "A design near the top is relatively cheap for the fleet, near the lower left cheap per unit, near the lower right high in coverage"; "the sponsor and operator pull against each other"; noted that mixed low/low/high wording could make a reader pause, not that it reverses |
| ternary | r4 | `ternary-r4-k1.png` | after the depth-three read: the legend says "the exponent vector of the one term, not a design" (it said "term 1" beside a Figure 9 with two terms, and readers took the star for the best design) | (depth three below) |

### The captions as in `paper/paper.ipynb` (these replace the drafts above)

- `fig-tension` (three sentences): "The tension matrix of each term of the K = 2 fit at its balanced point, for the metrics
  with an exponent w on the term, the others named below each panel. A cell is the change in the column metric per
  unit rise of the row metric's conditioned value; the metrics run from the one whose unit is worth most on the term to
  the least. Every drawn value is therefore -1 or less, from -1.1 to -17 on term 1 and from -1.0 to -30 on term 2;
  each undrawn cell is the reciprocal of its mirror image." The paper writes negative numbers with the hyphen-minus,
  as the cells print them. The label changed from `fig-tension-matrix` to `fig-tension`: the code cell and the figure
  shared the identifier (the duplicate-identifier warning of WP55's build); the cell keeps its id, which names the
  full-size PNG `figures/fig-tension-matrix.png`, and the two `numref`s of Section 8 point at the new label.
- `fig-fleet` (55 words): "The decision's three objectives, one per stakeholder, fitted with one term over the primary regime's
  2,134 feasible designs, each at its shares of the three conditioned objectives. The star is the term's exponent
  vector, not a design; it lies on the edge from fleet cost (0.39) to coverage probability (0.61), with 0.006 on unit
  cost." Placed in Section 8 before the decision cells (after the propose, predict, check sentence), cell
  `fig-fleet-ternary`, `case.fleet_ternary_figure()` at K = 1.

The sign and reciprocal convention: cells and caption carry the definition's sign (a tension is negative where both
metrics carry an exponent); the caption states the reciprocal once. No sentence of Section 8's prose states the
convention otherwise (the two sentences that cite the figure name it only), so no prose sentence changed.

### `fig-ternary-pair` leaves the paper

What it no longer did: it showed, on two triples picked from a search over 56 triples, that two terms of one fit can
lead in different regions of a triangle. The case's K = 2 reading carries that point with the case's own fit (the
chart, Figure 7's two panels and their contending sets); the pair's fits were not the case's fit, and its caption
spent two sentences on the search that picked it. The decision-maker's ternary is the paper's one triangle, on the
decision's objectives. Removed with it: the paragraph "Three metrics at a time" that introduced it (its reading of a
triangle, shares and the marker, is in the new caption), `paper/figures/ternary_pair.py`, `fig-ternary-pair.png`,
`paper/figures/triple_search.py` and `triple_search_record.json` (in history at the WP56 base, b5b3a86), the entry of
`scripts/build_figures.py`, and the four tests that read them. The docs page keeps its own two-panel drawing
(`case.ternary_pair_figure`, `docs/examples.md`). Figures in `paper/paper.ipynb`: ten before, ten after (the pair
out, the ternary in).

### Register

Retired: C468, C469 (the pair's region sentences), C470 (the "Three metrics at a time" paragraph), C471 (the search
counts), C472 (the pair's Shows line), C800 (Figure 7's "sorted by exponent", no longer true; its claim is C969).
Added: C967 (the value ranges, R), C968 (the order, S), C969 (the metrics drawn, S, as C800), C970 (the reciprocal,
M, L21.12), C971 (the ternary's design count and exponents, R). No other row was anchored in a Shows,
Does-not-show or Good-for line.

### The Shows, Does-not-show and Good-for lines, moved from the paper

### `fig-nlemma`

*Shows:* each term's exponent vector as a point of the simplex, in the face that names its n-lemma. *Does not show:* designs, their levels or the surface; with more than three metrics, anything beyond the three drawn. *Good for:* reading by eye how many and which metrics contend in a term.

### `fig-assembly`

*Shows:* every part of the cubesat and how it assembles, the two kinds of configuration variable and the swapped parts' levels, read from the model. *Does not show:* the physics, the attributes and metrics a configuration is evaluated into, or which configurations were sampled or are feasible. *Good for:* mapping the case's design variables onto one's own system model.

### `fig-behavioural`

*Shows:* which traded metric each requirement reads, grouped by functional subsystem, and what supplies each metric. *Does not show:* requirement thresholds or which designs pass them, the conditioning or the fit; the subsystem of a requirement is the analyst's reading. *Good for:* tracing each traded metric back to the requirement that reads it.

### `fig-tau`

*Shows:* which metrics carry the K = 1 exponent at each fit temperature of the sweep and how each exponent moves with it; where the fit temperature sits on the fraction-above curve and what effective sample it leaves. *Does not show:* fit quality, the fitted reference surface or the designs near it, any K > 1 fit, the exponents' values at the fit temperature ({ref}`Appendix D.3 <sub-d-3>`), the metrics at most 0.001 throughout, or why a metric has no exponent (carried by another metric, or a step function of the swaps: the n-lemma reading is the text's). *Good for:* reading the n-lemma at the fit temperature and how far it depends on the temperature; seeing what the fit temperature costs in effective sample.

### `fig-plane-1`

*Shows:* every design in the plane of the term's two heaviest metrics, adjusted for its other eleven, the term's line there, and each design's level as its distance from the line. *Does not show:* the other eleven metrics themselves, which the adjustment folds into the height, or the Pareto boundary. *Good for:* seeing the one-term trade-off as a line with a slope, and the line as the upper edge of the designs.

### `fig-chart-case`

*Shows:* each design's level against its position along the direction of most spread, the surface as the flat line log V = 0; where along that direction the designs reach the surface and where they fall deepest inside. *Does not show:* terms, any grouping, or the other directions of position. *Good for:* reading a design's level apart from where it sits along the main trade-off.

### `fig-tension` (was `fig-tension-matrix`)

*Shows:* each term's tensions among the metrics that carry an exponent on it, at its balanced point, and each metric's exponent. *Does not show:* a design's own tensions, the association among designs, a seam, or an effect of changing a design variable. *Good for:* reading how steeply one metric gives way to another on each term.

### `fig-ternary-pair` (left the paper, WP56)

*Shows:* where each term leads and where its V peaks. *Does not show:* groups of designs, the values of V on the lines, the other ten metrics or a cause.


## Depth three: figure, caption and the prose around it, as rendered

Built with `cd paper && BASE_URL=/paper uv run --frozen myst build --html` (no warning in the log; the
duplicate-identifier warning is gone), served at `http://localhost:8821/paper/`, captured in the light theme at 1280
px over the Chrome DevTools protocol (`depth3-fig-tension.png`, `depth3-fig-fleet.png`; the fleet capture was redone
after r4). A fresh-context reader was given the two screenshots alone.

**Figure 9 (`fig-tension`).** Reader: "a cell is how much of the column metric gives way per unit rise of the row
metric. All drawn values are negative and at least 1 in size, up to -17 on term 1 and -30 on term 2." The caption
and the figure agree. Findings at this depth, all in the prose the next unit rewrites, none a sign or reciprocal
contradiction (the prose states no convention for the matrix):
- the elasticity sentence after the figure ("On term 2 the elasticity between unit cost and available power is
  -0.9") is a log-log rate, the matrix a rate in conditioned units; a reader checks -0.9 against the cell (-2.8) and
  it fails. The prose should say the two are different quantities or not invite the comparison.
- the terms sentence ("contending sets ... of 8 and 7 metrics"; "peak slew power ... leads term 1") against the
  panels' "8 of 13 metrics carry an exponent" and the first row (pointing error): the contending set and the
  exponent-carrying set differ, and "leads" means the largest exponent while the rows run in the tension order.
- the elasticity sentence prints "alpha_i/alpha_j" as plain text.
- "worth most on the term" is undefined for the reader at this depth; the prose may say it is the exponent over the
  metric's conditioned value at the balanced point.

**Figure 10 (`fig-fleet`).** Reader: "Each design is placed by its shares of three objectives, one per stakeholder
... The star, the term's exponent vector, sits on the fleet-cost to coverage edge at 0.39 and 0.61. The figure agrees
with that caption." Findings, for the prose unit: the decision paragraph after the figure opens "The case's two
stakeholders: the operator cares about the pointing error, the sponsor about the unit cost and the fleet cost",
against the figure's three stakeholders with the operator on coverage probability; the decision's mapping must follow
his ruling (one stakeholder per objective). The paragraph before the figure (propose, predict, check) does not lead
to it; the figure needs its sentence where the decision subsection reads it. Fixed here: the legend's "term 1" (r4).
Left: the star sits outside the cloud of designs, which a reader can take for extrapolation; the caption's "not a
design" and the legend now say what it is.

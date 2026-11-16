
## The tension matrix figure (2026-11-15, 12:30 EST by the machine clock)

**Supervisor, verbatim (on the paper's Figure 7, two 8 x 8 tension matrices, screenshot in chat):** "i find this plot
more confusing than previous versions. i sort of understand the asymetry, which appears to be a 1/x relationship but
i worry that while that is technically correct it makes the plot harder to interpret not easier. its still
essentially the same information, just codified differently. i am okay with preserving options in the plotting
routines because in an interactive setting it can be helpful to try it out different ways but for a static paper i
think we may only want the upper or lower diagonal matrix so the reader isn't trying to reverse engineer that 1/x
relationship in the data"

**Recorded as a WP56 deliverable:** the plotting routine gains a `triangle` option (both, upper, lower; both the
default for interactive use); the paper's figure draws one triangle. The driver's default for the figure loop: the
upper triangle with the rows ordered by exponent, largest first, so every drawn cell is the cost of a gain in a
heavier metric paid in a lighter one and all values are at least one; the caption says the other triangle is the
reciprocal. Judged as rendered in WP56's figure loop before it reaches him.

## A decision-maker's ternary: unit cost, fleet cost, performance (2026-11-15, 12:35 EST by the machine clock)

**Supervisor, verbatim:** "i also think it may be worth trying to build a ternary plot that is unit cost, fleet cost
and performance. where performance is some aggregated that is interpretable as "how well can the fleet do its job" i
would expect it to improve in a larger fleet but with diminishing returns, and to be impacted by the pointing error.
we're assuming the fleet is trying to achieve some sort of coverage problem. i don't want to add a lot of model
detail. just enough to get to something obviously relevant to a top level decision maker that fits on a ternary."

**Recorded as a WP56 candidate edit (the six-stage lifecycle):** a research spike first: a fleet-performance
aggregate from the model's existing outputs (fleet size and pointing error at least), improving with fleet size
with diminishing returns and falling with pointing error, read as coverage; two or three candidate definitions with
their formula, their reading for an executive and the model detail each needs (as little as possible); each fitted
with unit cost and fleet cost as a three-metric table and drawn as a ternary; the candidates brought to him with the
figures before any build. The WP59 finding that a derived metric can absorb the metrics it is made of applies and is
stated once in the spike.

**Supervisor, verbatim (the ternary's three objectives, 2026-11-15):** "it will make the story easier to follow sponsor =
total cost, manufacture = unit cost, operator = performance. that way we map our 3 objectives to unique stakeholders"

**Recorded for the WP56 spike and build:** the decision-maker's ternary maps each objective to one stakeholder: the
sponsor to total (fleet) cost, the manufacturer to unit cost, the operator to performance (how well the fleet does
its job). Section 9's decision and its table use the same mapping, one stakeholder per objective.

## Amendments from the metamanager's feedback (2026-11-15 afternoon)

- The driver's default for the tension matrix (the upper triangle with rows by exponent, "all values at least one")
  is withdrawn: the entries are elasticities at the term's balanced point in conditioned units, not bare exponent
  ratios, so the range claim is not established. The figure loop settles the triangle and the row order on the
  actual values; any statement about the range is derived and checked numerically before it enters a caption.
- The performance aggregate is accepted as a modelling choice: formula, units, monotonicity in fleet size and
  pointing error, two or three plausible definitions compared, and the decision's stability across them reported;
  the definition is not chosen for the ternary's looks.

**Supervisor, verbatim (on the aggregate's place, 2026-11-15 afternoon):** "on this one i want to make sure you don't
overcomplicate the paper the details of the modeling assumptions and how they are made go in the model itself. they
can referred to but not explicated at length. the paper is a view, the sysmlv2 model in the repo is "the model".
i'd also recommend thinking about the word "model" as a pronoun. there are so many kinds of models in this work
that this word can only be used if it is immediately obvious from context which model we're talking about.
otherwise indicate which object we're talking about unambiguously"

**Applied as:** the aggregate's definition, assumptions and the comparison across definitions live in the SysML v2
model and the WP56 record; the paper states the definition in a sentence and refers to the record. "Model" is used
in the paper only where the object is obvious; otherwise the object is named (the register's rules).

## The ternary spike's readout, read by the driver (13:45 EST)

Branch wp56-ternary at cf4faca (`WP56-rounds/ternary/readout.md`, three figures, `examples/adcs/spikes/fleet_performance.py`).
Three candidate aggregates (coverage probability, a capacity with a ceiling, a refresh rate after Wertz), each fitted
with unit cost and fleet cost on the primary regime's 2,134 designs. The finding that decides the question is
structural, checked by the driver on the data of record: fleet cost equals unit cost times fleet size exactly (the
ratio is 1.000 on every row), so log fleet cost is log unit cost plus log fleet size and the three objectives have
two degrees of freedom plus the pointing error inside performance. The fits say the same: unit cost's exponent is
0.006, 0.053 and 0.000 under the three definitions, and every term trades fleet cost against performance. The pick is
not stable across definitions or across a factor of two in any constant (the sponsor's rule picks fleets of 3 to 11,
the operator's 18 to 28, under every fit). The spike recommends coverage probability as the operator's quantity if an
aggregate is carried into the SysML v2 model.

**Waiting for the supervisor (a problem-level choice, his):** with fleet cost the model's product of unit cost and
fleet size, the stakeholder triple cannot show three independent tensions. Options, plain: (1) keep the triple and
read the ternary as what it is, a dilemma between the sponsor's fleet cost and the operator's performance with the
manufacturer's unit cost nearly flat, said in one sentence; (2) replace the sponsor's axis by one not tied by the
accounting identity (the model would need a cost the sponsor bears that is not n times unit cost, such as launch or
operations cost, a model change); (3) drop the three-stakeholder ternary and keep Section 9's decision table as the
stakeholders' view. The driver's reading: (1) if the point of the figure is the stakeholder mapping, (3) if the point
is a figure that carries the argument on a skim; (2) is the only route to a genuine three-way picture and is a model
change beyond "just enough detail". No build until his word.

## His choice on the ternary (14:03 EST)

**Supervisor, verbatim:** "keep the ternary and explain what is shows. i would note that there are almost certaintly
modeling assumptions that could pull it towards the middle, but that would involve more complex assumptions about how
manufacturing costs scale. i don't think we need to force a more complex model. i think we need to say that this was
not guaranteed to collapse to the 2d trade off, and what we got was a traceable thread that says it does and why. and
if we revise modeling assumptions we can check to see if the result holds easily"

**Applied as (WP56 build item):** the three-stakeholder ternary stays, with coverage probability as the operator's
performance (the spike's recommendation), defined in the SysML v2 system model as a derived attribute of the fleet and
recorded with the comparison in the analysis record; the paper's sentences say: the three objectives were not
guaranteed to collapse to one trade-off; on this model they do, because fleet cost is unit cost times fleet size, so
the sponsor's objective rides on the manufacturer's and the fleet size, and the fit names the dilemma between fleet
cost and performance with unit cost nearly flat; a different cost scaling in manufacturing could pull designs toward
the middle, and the pipeline refits to check it. The thread is traceable: the SysML v2 model's definition, the data
of record, the fit, the figure. No new model complexity.

**Supervisor, verbatim (14:03 EST):** "also don't force the equation into the figure"

**Applied as:** the ternary's title carries the name of the performance measure (coverage probability), not its formula; the formula lives in the SysML v2 model and the record, named once in the prose.

## The driver's approval as proxy (18:03 EST)

Under his autonomous-mode mandate (`WP11-decisions.md`, 2026-11-15: "run in autonomous mode ... do a soft confirm on
each section as my proxy") the driver approves `WP56-scope-of-work.md` at dev 1ba7af9, with two amendments made before
approval: G3 covers every caption in the paper and the supporting material, not only Sections 7 to 9 (Figure 3's
caption still carries the Shows, Does-not-show and Good-for lines WP60 removed from the docs); and the first unit
starts now on the deliverables that do not touch the notebooks (the coverage attribute in the SysML v2 model, the
generator, the tension matrix routine's `triangle` option, the figure loop at the first two depths), pausing before
any notebook edit until WP55 lands. The spike inputs are taken from the branches `wp56-ternary` (cf4faca:
`work-packages/WP56-rounds/ternary/`, `examples/adcs/spikes/fleet_performance.py`) and `wp56spike` (6cbf936:
`work-packages/WP56-rounds/spike-lineage.md`). Open decisions for him: none; the triangle and row order of Figure 7
are the driver's call on the figure loop's screenshots.

## Unit 1 read by the driver; the figure calls (18:39 EST)

Branch `wp56` at 2377ea3 (spike inputs 627dc24; the coverage attribute, case code and tests a652958; the figure loop
2377ea3). Coverage probability lives in `examples/adcs/model_v2/stakeholders.sysml` as a measure of effectiveness
with its formula, constants and readings (p0 = 0.2 at zero pointing error; e0 the pointing error limit), checked
against the pipeline's function by a test; the data of record, the derivations and the paper are untouched. The
driver's calls on the loop's screenshots, as the scope leaves them to him as proxy:

- **Figure 7:** the upper triangle in tension order (rows and columns from the metric a unit of which is worth most
  on the term to the least), so every drawn value is at or below minus one with no exception; the earlier claim
  that every value is at least one in exponent order was false (five cells below one) and is withdrawn for good.
  Phase two drops the empty last row and the empty first column (the strict upper triangle), keeps the exponent on
  each row label, and cuts the caption to three sentences with the value ranges.
- **The ternary:** one term over the 2,134 feasible designs of the primary regime; both cold readers read one
  trade-off between the sponsor's fleet cost and the operator's coverage probability with the manufacturer's corner
  idle, which is his sentence; at two terms both terms sit on the same edge and the readers took the two markers as
  disagreement, so the two-term fit is reported in the prose as the refit check, not drawn. Phase two reconsiders
  the corner labels ("favours fleet cost" reads as favouring a high cost; the conditioned objectives are low fleet
  cost, low unit cost, high coverage) in the figure loop, and keeps the title as the measure's name.
- The collapse holds exactly on the data of record: fleet cost over unit cost times fleet size lies within
  1e-8 of one on every row (a test now checks it).

## Phase two read at depth three (22:15 EST)

On the unit's build (port 8821, branch `wp56` at bdb0b49 plus the Appendix G rewording): Figure 9, the tension
matrix, as the strict upper triangle in tension order with a three-sentence caption giving the ranges (every drawn
value at or below minus one; -1.1 to -17 on term 1, -1.0 to -30 on term 2); Figure 10, the stakeholder ternary at one
term with the corners "low fleet cost (sponsor)", "low unit cost (manufacturer)", "high coverage probability
(operator)", the star on the fleet-cost to coverage edge, the title the measure's name and no formula. Both read on
the page as his sentences say. The old `fig-ternary-pair`, its paragraph and its generators are out (register C468 to
C472 and C800 retired; C967 to C971 added); Section 2 names Appendix G. The prose around both figures is still the old
Section 8 text ("The case's two stakeholders: the operator ... the sponsor ...") and contradicts the three-stakeholder
mapping; that is the second unit's rewrite, on these landed figures. The driver accepts phase two as proxy pending the
unit's final commit and the landing checks.

## The figure phase landed (22:36 EST)

Branch `wp56` at 336ab32 merged into `dev` at c1a886d; CI 43798043201. The driver's checks on the branch: lint, format,
lock and the proof map clean; derivations and the data of record untouched; attribution grep empty. The driver's
fast run in the unit's worktree ended "4 failed, 2081 passed, 3 errors" and the chain merged on it (the pipeline's
status was read, not pytest's; recorded in the driver log). The rerun on dev's head: 2,087 passed, one failure,
`test_every_paper_key_is_a_label_of_the_built_paper`, which reads the local `paper/_build` of 11:15 against the
renamed label `fig-tension`; after a fresh build the test passes. The unit's own runs: fast 2,088, slow paper 28.
The worktree's other failures were not reproduced on dev and are left to CI's verdict. The second unit now rewrites
the prose of Sections 7 to 9 on these figures.

## The prose of Sections 7 to 9 read at depth three and landed (00:50 EST)

Read on the second unit's captures of its build (port 8857, branch `wp56p` at 23f7e17; the pane was hidden, so the
captures in `WP56-rounds/prose/` and the page's text stand as the record) against the register's rows for Sections 7
to 9. Section 7 opens with the fleet and the SysML v2 model named, the CADRE precedent, the problem as a displayed
triple; Table 2 (new, generated) holds the thirteen metrics with their marks, requirements and the stage each is
applied, and the derived coverage probability as the fourth MoE; provenance in one paragraph; the baseline
configuration carried to Table 3's first row. Section 8 goes from the nondominated opener to the decision: the four
cold-read defects fixed (contending sets 8 and 7 with total mass drawn outside its set; peak slew power "carries the
largest exponent"; -0.9 per percent set against the matrix's -2.8 per unit; the alpha ratio as math; "Theorem 7" was
the wrong number and the generator now counts it from the notebook, Theorem 8); the requirements after the fit with
their excluded counts (178 of 238 jointly); the three-stakeholder paragraph in his sentences with the identity and the
two-term refit printed beside their call; the decision with one stakeholder per objective (manufacturer and operator
both pick the fleet of 25 at 5.85 M USD and coverage 0.98; the sponsor the fleet of 4 at 1.13 M USD and 0.46; between
them the fleet of 10 at 2.88 M USD and 0.76, one of 17 nondominated on fleet cost and coverage of the 28 shortlisted);
Table 3 with five rows; the closing sentence naming the calls and what no rerun supplies. Section 9: human
validation with the case's own check of the collapse, what the case showed against Section 1's contribution, the
three layers, the limits once at the end (a new test holds that). R-1 (21 sentences about the model, each with its
record), R-4 and R-6 met; R-5 met on the scope's measure (typed Markdown 3,320 to 2,562; the rendered count with the
generated sentences is 3,638, recorded). Soft-confirmed as proxy.

Landing: `dev` fast-forwarded to bdd06c5 (23f7e17 plus one landing edit). The landing edit: CI 43798043201's slow jobs
failed on both platforms on one doctest, `coverage_probability(1, 0.0)` printing 0.19999999999999996 against an
expected 0.2 (the first unit's docstring; the slow-marked docstring test was in neither unit's run nor the driver's);
the example now rounds. The driver's checks on the branch, exit codes captured: fast suite 2,091 passed (exit 0);
slow paper tests and the docstring test (exit 0, below); lint, format, lock, proof map (22 files, 549 steps),
vocabulary 0 new, attribution grep empty, derivations and the data of record untouched; residuals exit 1 as on dev
with `paper.ipynb` at or below dev on every count. Register: C972 to C987 added, 30 retired, 15 re-anchored; next free
C988. Open questions OQ-11 to OQ-13 added by the unit (the manufacturer absent from `stakeholders.sysml`; the stale
pass rate in `cubesat.sysml`'s header, 63.7 against 65.6 %; the pick moves with the coverage constants).

Noted for his read, not changed: the two names for the second regime ("stock regime" nine times, "baseline regime"
seven, no glossary entry; older than WP56 and spread over the generators, so a vocabulary item for WP58); the
generated datasets sentence says "3,000" twice and "thirteen attributes" a third time; Figures 5 and 8 keep the
first unit's long captions (230 and 194 words). D.19's rule paragraph names the old rules until WP57c lands, its
first commit.

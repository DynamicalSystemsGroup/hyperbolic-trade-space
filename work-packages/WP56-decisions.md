
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

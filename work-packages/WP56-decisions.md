
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

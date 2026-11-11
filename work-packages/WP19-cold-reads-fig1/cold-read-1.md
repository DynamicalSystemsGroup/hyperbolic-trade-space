# Cold read of the redrawn Figure 1 (planted rings and their legend entry removed)

Reader: one fresh Sonnet agent, image only (`fig-nlemma.png`), neutral brief: say what it shows, what each element
means, what looks missing, odd or ambiguous, and what a caption should answer; at most 300 words.

Reader's report, verbatim:

**What it shows.** A triangle (a 2-simplex) with corners labelled metric 1 (top, "corner: it binds alone"), metric 2 (bottom left) and metric 3 (bottom right). The edges are labelled "dilemma of 1 and 2", "1 and 3" and "2 and 3". The interior is labelled "trilemma". Three numbered dots (blue 1, orange 2, green 3) are placed in it. A right-hand panel, "Each term's exponent vector", lists:
- term 1: dilemma of 2 and 3, w = (0.00, 0.35, 0.65). It sits on the bottom edge.
- term 2: trilemma of all three, w = (0.44, 0.27, 0.28). It sits in the interior.
- term 3: dilemma of 1 and 2, w = (0.70, 0.30, 0.00). It sits on the left edge.

A footer says "Weight on these three metrics: 1.00, 1.00, 1.00 (all of it: d = 3)".

**Reading.** Each term of the posynomial has exponents that sum to 1. Its position is barycentric: a corner means it depends on one metric alone, an edge on two, the interior on all three. "Binds" and "dilemma/trilemma" mean the term couples that many metrics.

**Odd or ambiguous.**
- The footer is cryptic. 1.00, 1.00, 1.00 appears to be each term's weights summing to 1, but it reads as per-metric totals. Summing the columns instead gives 1.14, 0.92, 0.93, so the footer is not that.
- Only the metric 1 corner is annotated. Corners 2 and 3 are not, and the "binds alone" label is jargon.
- Dot 3 sits on the left edge and dot 1 on the bottom edge. Dot 3 is slightly off the exact edge position for 0.70/0.30.
- The right edge, "1 and 3", has no dot.
- The legend gives no direction convention (which corner means weight 1).
- "Weight" (footer) and "exponent" (title) name the same quantity.
- Nothing says where the metrics come from, or whether this is one model with three terms (K = 3) or three separate models.
- The figure does not say which dilemma is "hard".
- The bottom third of the canvas is empty.

**What a caption should answer.**
- What the triangle is (the space of exponent vectors, summing to 1), and what position means.
- That the three terms are the terms of one fitted posynomial.
- What "binds" means: the metric whose term sets the frontier.
- Why edges are dilemmas and the interior is a trilemma.
- What the reader should take away: more terms, richer trade-off structure.
- Whether the values are illustrative or fitted.

Reading (the assistant): the rings are not missed; no question concerns a second marker. The footer's three equal
numbers (each term's weights on the three metrics) read as per-metric totals: raised to the supervisor, not edited here.

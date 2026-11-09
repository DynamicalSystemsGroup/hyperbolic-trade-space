# WP18 — Decision records (ternary plots in the documentation's examples)

Records typed by the agent (driver session). The supervisor's review is at the PR.

## Origin (2026-11-09)

- **Supervisor (mzargham), verbatim:** "one more thing i'd like you to put in your work backlog and
  have the PM scope and provision agents to work on is adding examples using the ternary plots to
  the documentation. keep it simple like with the other plots in the examples; we just want that
  visualization pattern to be documented, accessible and interpretable for users."
- The PM's bounded scope subagent drafted `work-packages/WP18-scope-of-work.md` (09f12ea).

## Open decisions, settled by the driver under the mandate (for the supervisor's review)

- **OD1, where the new prose goes.** Options: a new page with its own budget / the Examples page's
  budget raised from 400 to 650 words with the key and limits there / the key and limits on the
  chart page with two budgets raised. **Driver's call:** the Examples page, budget 650. Reason: he
  asked for examples "like with the other plots in the examples", and a user should find the plot,
  the code and how to read it in one place; the site's total stays well inside 7,600 words. The
  page budgets were approved by him in WP8a Amendment 2, so this raise is listed for his review.
- **OD2, the figure cap.** Options: raise the docsite's cap from seven to nine / keep seven with one
  two-panel figure and no equal-V overlay / retire an existing figure. **Driver's call:** raise the
  cap to nine, one figure per example. Reason: he asked for added examples; a two-panel figure is
  harder to read at phone width, and no existing figure was named for retirement.

## Agent's defaults

- Approved as listed in the scope, as one item. One default is flagged for the supervisor to strike:
  the lines of equal V are ON in example (i) and off by default in the function. He has said of that
  picture "this is great. i think it really captures the essence" and has not said where the lines
  are to be used.

## Scope approval (the driver, under the mandate)

- **Document:** `work-packages/WP18-scope-of-work.md` at 09f12ea, with OD1 and OD2 as settled above.
- **Date:** 2026-11-09.
- **Disposition:** approved for execution. Execution starts when an implementer is free on files
  that do not collide: WP17 is amending the interface contract and the glossary now, so WP18's
  contract amendment takes the next version number after WP17's lands.

## The supervisor on the cubesat triangle (2026-11-09)

- **Supervisor (mzargham), verbatim,** on the second example's figure (the three-term cubesat fit by
  exponents summed over subsystems: three markers in an empty triangle; caption "only facet 3
  carries mass (0.18)"): "just a heads up. this is pretty vacuous. doesn't seem to earn its place on
  the page, even in the documentation. make sure we also do visual loops for figures".
- **Disposition:** example (ii) is dropped from the documentation (figure, code block and caption);
  its one finding stays as a sentence if the page wants it. The figure cap goes to eight. The
  remaining example and the root page's Why image go through the figure review
  (`docs/superpowers/notes/figure-review.md`: a cold read of the image alone, the sentence test, ink
  as data, legibility where it is read, what it shows and does not show) before WP18 is delivered.
  The driver had passed this figure as "clean" in his browser pass; recorded under "Overruled or
  corrected" in the driver's log. The same review is stage 2 of WP19 for the paper's figures and is
  run over the docsite's existing figures as a ticket.

## The supervisor on the planted triangle (2026-11-09)

- **Supervisor (mzargham), verbatim,** on the first example's figure (three metrics on the planted
  table: regions with their boxed labels, designs, the lines of equal V, and the numbered square,
  star and diamond markers): "this one is great but make sure the prose is clear about the values
  attained at the square, star and triangle points marked. that doesn't need to be in the figure
  itself, it can be in a table or prose related to how to read this plot".
- **Disposition:** the figure is confirmed by him and stays exactly as drawn. The driver's two change
  requests on it (leave the boxed region labels off when the lines are on; enlarge the marker
  numbers) are withdrawn: he judged the picture with them and called it great. The equal-V lines
  stay ON in this example, which settles the default that had been flagged for him to strike. Added
  to the page, in the "how to read this plot" key as a small table or a sentence each: for every
  marked point, its marker and number, the facet's exponent vector (the shares at which it sits),
  and the value of V attained there at one total, stated in the same units as the lines (a fraction
  of the highest marker's value), with the levels of the lines named. The values are generated from
  the fit by the code that draws the lines, never typed. His confirmation stands as this figure's
  verdict in the figure review; its record needs only the recipe and what the figure shows and does
  not show.


## Delivery note: the values at the marked points (P7, 2026-11-09)

- Public helper `ternary_marker_values(estimator, X, names=None)` in `hyperbolic_trade_space.plotting`
  returns a table, one row per numbered marker of `plot_ternary(..., lines=True)`: marker shape and
  number, the facet's exponent vector (its shares) and V there as a fraction of the highest
  marker's V (that row reads 1.00), with the levels of the equal-V lines in `attrs["levels"]`. It
  shares the level constant, the marker shapes and the log-V evaluation with the drawing code; no
  second implementation. Contract version 8.
- The figure is unchanged: the docs example (900 designs) renders to an identical pixel array
  before and after.
- "Total" is the sum of the three metrics each in units of its typical size; the lines plot applies
  no power (only the lines-off view spreads the designs by one), and the fraction does not depend on
  the total chosen.
- `groups=` is kept: its generic test and docstring stand, and `docs/examples.md` still calls it
  until the example (ii) removal lands (P6). It can go with that removal.

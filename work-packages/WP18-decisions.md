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

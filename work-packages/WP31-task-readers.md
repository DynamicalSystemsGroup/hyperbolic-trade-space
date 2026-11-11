# WP31 — Task readers on the rebuilt "Choosing K" page (head 6745b88)

Three fresh readers (Sonnet), page only, task "choose K for this table and say why". Tables: P = `make_frontier_data(400, 4, n_terms=2, random_state=7)`,
Q = the same with `n_terms=3, random_state=5` (truth held by the PM), C = the cubesat primary regime. Returns below are the readers' choices and
evidence; their stuck points are quoted in full in the PM's report to the driver.

| Reader | Table | Chose | Truth | Evidence (tau=50 unless stated) |
|---|---|---|---|---|
| P | planted | K = 2 | K0 = 2 | slack drops 0.271, 0.005, 0.004, 0.003; K >= 2 certified; same break at tau 20 and 100 |
| Q | planted | K = 3 (K = 2 nearest) | K0 = 3 | drops 0.146, 0.060, 0.004, 0.004; movement small at K = 3, large at K >= 4; same at tau 20, 100 |
| C | cubesat primary | K = 2, low confidence, "the data do not pick K" | the page states no break | drops 0.112, 0.044, 0.017, 0.010; thinnest 0.07 at K = 2; page numbers reproduce exactly |

## Triage (PM)

- The page's numbers reproduce (planted 0.108/0.005 and 0.163/0.029; cubesat drops, thinnest, radii, movement ranges). Helper blocks ran.
- Defects against the task (all three readers): (1) the temperature: "selected at K = 1 (Fitting)" gives a reader with their own table no recipe, and
  the cubesat block's `case.fit_study(s, K=1).tau` is not available to a user of the installed package; two readers guessed tau and bracketed it.
  (2) Terms used without a gloss on the page: slack, near-frontier band, cell, certificate radius, "at most 2" for movement; no scale for "thin".
  (3) The `sweep` helper asserts `drops[-1] > 0.002`, which two readers hit or removed (tau = 100 gives 0.002). (4) `sys.path.insert(0, "examples/adcs")`
  runs only from the repository root; the page does not say so.
- Not defects: the page has no combined decision rule and no held-out criterion by the driver's stage-2 decision; the readers reached the planted truth
  on both planted tables and a hedged, correctly "no break" reading on the cubesat.
- Record gap: the pane could not save screenshots to files for these readers; the page's rendered review with saved screenshots is e5d7c7b's
  (`scratchpad/wp31review/choosing-k-*.png`); the rebuilt head has not been re-photographed.

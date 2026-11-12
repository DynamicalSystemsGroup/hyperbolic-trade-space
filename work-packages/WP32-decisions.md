# WP32 — Decisions

The supervisor's words are quoted verbatim where they bind; the assistant's calls are listed for his review.

## Scope gate (2026-11-11, 10:10; scope at 78608bc; the assistant)

Origin: the supervisor's words in `docs/superpowers/notes/reader-grid.md`, "Axis 3". OD1: the plain CSV is a synthetic
table from `make_frontier_data` with generic column names, written once as a fixture; no public dataset is hunted.
OD2: the model-exported table comes from a small SysML v2 model that is not a satellite (three or four metrics; a
pump, a bicycle or a heat exchanger trade), built for the test and kept small. OD3: the fixtures live under
`tests/fixtures/user-tests/`, the cells' code and returns under `work-packages/WP32-cells/` as records. The defaults
approved as one item. **Assistant, verbatim:** "WP32 approved with OD1 synthetic CSV, OD2 a small non-satellite model,
OD3 fixtures under tests and records under work-packages."

## Approval (2026-11-12; the assistant, scope at 03d95fd), open questions decided

**Assistant, verbatim:** "WP32 Q1: after two re-runs, an open stop the docs owe goes to the chief engineer's list with the cell's words; Q2: a code defect a cell finds is fixed in this package as its own unit with a test, since the package is the deliverable and a user-found defect blocks the release." Both scopes approved as written at 03d95fd.

## Round 3 (2026-11-12; the assistant, head 60f92d9)

Acceptance record: pending (the supervisor's acceptance of WP32 has not been given; this file records none).
**Assistant, verbatim:** "Round 3 is accepted: both pump-table cells reached the fit and the trilemma with the new block, no stop persists, nothing goes to the chief engineer's list from the cells. The K = 1 tension_report error on an exact-relation table right after select_temperature: no change; the message names the fix and all three cells that met it recovered in one step; the review names it as a residual, not a caveat in the docs. U2's HTTP-text reach is noted and acceptable for the docs text (the rendered pass is the reviewer's)."
Rows: `triage.md`, "Round 3" (R3-1 to R3-4).

## Review closure (2026-11-12; the assistant's dispositions of `WP32-review.md` at d09af78)

Acceptance record: pending (quoted later by the supervisor's assistant; this file records none).
- R-10 gap (review finding 6): one fresh U1 cell runs on the next staged head, beside WP33's repeat round, with its return and a one-row triage closing the gap. U1 met R2-3 in round 2 before that fix landed; U3 met nothing in round 2 and is complete, so no U3 re-run.
- Review finding 7: `scripts/build_figures.py` rewriting two tracked paper figures (`paper/figures/fig-chart-level.png`, `fig-ternary-pair.png`) byte-differently on each run is a machinery defect outside WP32. It is routed to a separate unit (not WP32); WP32 changes nothing there.

## Acceptance (2026-11-12, 19:25; the assistant, under the supervisor's mandate; review at d09af78, closure at c33b108)

**Assistant, verbatim:** "WP32 is accepted. The four package-user cells completed in three rounds from the README,
the site and the installed package alone; the six docs fixes and the register repair landed; the review ran the
cells' code at the head and checked every triage row against the diff; its findings are closed except R-10 for U1,
which one fresh U1 cell on the next staged head closes, recorded here; the figure-build defect is a machinery unit
outside this package. The residuals stand as written."

# WP32 review (D-7)

Reviewer: Sonnet, in worktree `pm-worktrees/wp32rev` at `origin/dev` head 58cc8a7. The stage (http://127.0.0.1:8791/) is frozen at
60f92d9; `git diff 60f92d9 HEAD` over `docs/`, `README.md` and `src/` holds only `docs/superpowers/notes/user-journeys.md`
(WP33), so the stage pages equal the head's. Screenshots: `WP32-review/` (images only; `PAGE-WIDTH-SCHEME.jpg`, five pages
by 375 and 1280 px by light and dark).

## What was run

- The ten cell scripts (round 1: U1 `run.py`, U2 `run.py`, U3 `fit.py`, U4 `run.py`; round 2: U1 `analysis.py`, U2
  `analysis.py`, U3 `analyze.py`, U4 `analysis.py`; round 3: U2 `run.py`, U4 `run.py`), each copied to the reviewer's
  scratchpad with the committed fixture as `table.csv` (the cells' own `table.csv` equals the fixture byte for byte in all
  ten), run with `uv run --project <worktree> python <script>`: ten exit 0, each prints the fit, the K sweep and the tension
  report and writes the heatmap `tensions.png` (R-9). Planted facts reproduce: plain table tau 178.2, contending set
  `[0 1 3]`, exponents `[0.49 0.506 0.004]`; pump table tau 695.5 (target 0.25, bounds to 1000) or 6023.1 (target 0.10,
  bounds to 1e4), trilemma `[0 1 2]`, exponents `[0.28 0.234 0.487]`, mass 0. Stderr: only the matplotlib first-run
  font-cache line.
- The README first call runs and prints `[0.29 0.39 0.32]`.
- Triage numbers re-measured on the pump table: default target 0.10 with bounds (3, 1000) raises; tau 4869.7, 6023.1, 7400.8,
  8490.2 for bounds (0.1, 1e4), (3, 1e4), (3, 1e5), (3, 1e6); `frac_above_` 0.215, 0.155, 0.10, 0.09, 0.05, 0.025 at tau 1e3,
  3e3, 6023, 1e4, 3e4, 1e6. All as the triage says (R2-1, R2-2).
- Checks: `check_vocabulary.py` 0 new violations; whole-repo `ruff check .` clean; `ruff format --check .` 601 files formatted;
  `pytest -m "not slow"` on `test_user_test_fixtures`, `test_interface_contract`, `test_claims_register`, `test_docs`,
  `test_site`, `test_text_encoding`: all pass (one skip); `git log 03d95fd..HEAD -- src` is empty;
  `uv run --group docs mkdocs build --strict` passes after `build_generated.py` and `build_figures.py` (the bare build
  fails on the missing git-ignored generated figures, as designed).
- Rendering, own tab `tab-93` (closed at the end): fitting, choosing-k, tensions, chart, overview at 913 px, and at 375 px
  with dark scheme emulated; no horizontal overflow at 375 px on any page, zero broken internal links or anchors (all
  nav and article links fetched), all images loaded, no "Loading", placeholder, traceback or `NaN` in text (the word
  `ValueError` appears in prose only), the heatmap caption reads "w under a name is its exponent" and the dark 375 px view
  shows it. Saved screenshots by headless Chrome of the stage pages inside a 375 px or 1280 px frame.

## Findings

severity | where | evidence | what it breaks

- medium | `WP32-cells/triage.md`, `WP32-decisions.md` | triage has two sections (round 1, round 2); `round-3/` holds two returns and the commit 58cc8a7 says "round 3 accepted" but no triage section and no decision record of the acceptance exists. Round-3 stops without rows: both cells' `tension_report` K = 1 band error after `select_temperature` (U2 error 2, U4 error 2), U2's cwd `FileNotFoundError`, U2's guessed `/docs/overview/` 404 and the tab cap, U2's "README does not say which columns are attributes; the overview says so, found late" | R-7 (every stop has a row) and R-14 for round 3; the stopping rule's record (Q1) is silent
- low | `triage.md` column 6, rows 5, 6, 7, 9 | the diffs delete, with the column saying "none" or something else: `fitting.md` "It follows the scikit-learn decomposition family: `fit`, `transform`, `inverse_transform`, `score_samples`, and no `predict`" and the quantified clause "(about 0.30 on the table of `make_frontier_data(300, 4, n_terms=2, random_state=777)`)" (9449733, row 6, column says "the cap of 1000"); `chart.md` "They share one colour vocabulary, declared as module constants (`FRONTIER_COLOR`, ...)" (f0242ad, row 7, "none"); `tensions.md` "This is how the method chains with PCA: the spread along the surface is the set of trade-offs the designs exercised" (0d7a0c3, rows 5 and 9, which list only "The set is found, not assumed") | R-14: the record does not show every removal; deletions are welcome but each must say what the content no longer did
- low | `triage.md` row 1 | says the README "Status" paragraph and CI sentence "go to `work-packages/`"; `work-packages/README.md` holds a status table and the release-candidate paragraph but neither the "0.1 release candidate in preparation" sentence nor "shards run on Linux and Windows; paper build on Linux and macOS" (grep finds the latter nowhere in the repository's markdown) | the row claims a move the diff does not show; those two README sentences were deleted
- low | `triage.md` row 10 | says the overview lost "two sentences of the opening paragraph and 'reads as a factor of improvement'"; the diff removes one opening sentence ("Some designs win on one number and lose on another.") and the factor sentence | the count is one too high
- low | `round-1/U4-return.md` | the return has no header block; model, persona and head are not named in it (the other nine have them). The round-1 README says "Sonnet cells" and describes the copied files, rounds 2 and 3 say "same setup"; no worktree listing is recorded for any round | R-4 asks the model named in the return header and the worktree listing recorded
- low | R-10, U1 and U3 | the last fresh U1 and U3 are round 2 (head a3a61af), run before the round-2 fixes (R2-1, R2-3, R2-8); round 3 re-ran U2 and U4 only. U1 hit R2-3 (batches B and C) and said "could not check it there", so a stop the docs owed was not re-tested for the persona it hit; U3 hit none | the definition of good enough asks one fresh cell of each kind in the final round
- low | `scripts/build_figures.py` | running it rewrites two tracked files, `paper/figures/fig-chart-level.png` and `fig-ternary-pair.png`, byte-different on every run; reverted here, nothing committed | a docs-only figure build dirties the paper's tracked images (a note for the machinery's owner, not WP32)

## Residuals (recorded, not defects)

- At K = 1 on an exact-relation table, `tension_report` right after `select_temperature` raises "only 5-6 near-frontier rows ...
  min_near_frontier = 10; use band=..." (tau 6023 gives a band of 1.7e-4 with 6 rows). Met by U1 (plain-table batches), U2 and U4
  in round 2 and by U2 and U4 again in round 3; every one recovered in one step from the message (refit at tau 4760, or
  band 0.00021). The message is right; the fitting page's block now steers an exact-relation table to tau near 6000.
- The matplotlib `findfont ... Lucida Grande` stderr line on plots: a font-cache effect reproducible without the package.
- U2's round-3 reach was HTTP text: the pane was at its tab cap, so U2 did not see the pages rendered (the task's pages
  are rendered here, above).

## Good enough (scope, "Definition of good enough")

| Item | Verdict | Evidence |
|---|---|---|
| G1 to G7 delivered | met | task text, fixtures, three rounds, triage (rounds 1 and 2), fixes, this review; round-3 record gap is the medium finding |
| R-1 to R-14 met | not met, see the table | R-4, R-7, R-14 have findings; R-10 partly |
| One fresh cell each of U1 to U4 completes in the final round (R-10) | partly met | U2 and U4 in round 3; U1 and U3 in round 2 only (finding above) |
| Every triage row has a disposition; every named request landed or is deferred with a reason | met for rows 1 to 20 and R2-1 to R2-11 | all landed requests match the diffs (rows 1 to 7, 9, 10; R2-1, R2-3, R2-8); deferrals: row 16 to WP33, R2-4 and R2-7 as features; round 3 has no rows |

## Requirements

| ID | Verdict | Evidence |
|---|---|---|
| R-1 | met | `grep` of `tasks.md` for work-packages, derivation, notes, paper, glossary, tests, scripts, contract, WP numbers: no hits; the three rounds' `tasks.md` are byte-identical to the committed one |
| R-2 | met | `plain_table.csv` 250 x 6, `pandas.read_csv` loads, no satellite vocabulary in the CSV or generator, minima 0.42, 4.9, 0.059, 28 with maxima to 5e5 (needs conditioning); `test_user_test_fixtures.py` passes |
| R-3 | met | `pump_trade.sysml` shares no element with `examples/adcs/` (fixtures README says so; the model has its own `calc def`s); `export_pump_table.py` reproduced by `test_user_test_fixtures.py` |
| R-4 | not met (low) | pages-opened lists hold the README, stage URL, table, model source and package tracebacks or `dir()` only (U2 round 2 fetched eight more site pages by script and searched them; U4 guessed `/docs/guide/`, U2 `/docs/overview/`, both 404); round-1 U4 return names no model; no worktree listing recorded |
| R-5 | met | all ten returns carry the six fields (code, pages, errors, questions, steps, standing answer) and the plain-sentence answers; U2 round 3 headings differ in wording only |
| R-6 | met | `ec3709e`, `bd90bf9`, `0fc6b29` each add only returns and a README line and precede the triage commits `d6fefa8` and `2942ff5`; `diff` of each of the ten committed returns against the cell's own `return.md` is empty |
| R-7 | not met for round 3; met for rounds 1 and 2 | rounds 1 and 2: every error row traced to a triage row (row 6, R2-1, R2-3, rows 7, 8, 9, 20, R2-9); round 3: no rows (medium finding) |
| R-8 | met | `git log 03d95fd..HEAD -- src` empty (no code change; Q2 not exercised); `test_interface_contract.py` passes |
| R-9 | met | ten of ten scripts run to exit 0 on the fixtures at head and yield fit, K sweep, tension report and chart |
| R-10 | partly met | round 3 U2 and U4 completed; both met only the residual K = 1 band error and recovered; U1 and U3 rest on round 2 |
| R-11 | met | all ten returns answer no; U2 and U4 round 2 and 3 quote the overview clause "any table works, and a SysML v2 model's exported table is one source" as optional |
| R-12 | met | five changed pages, desktop and 375 px, light and dark: no stderr line, broken link, placeholder or "Loading"; the README is GitHub-side and was not rendered |
| R-13 | met | vocabulary, whole-repo ruff check and format check, mkdocs strict build, and the named tests all pass (above) |
| R-14 | not met (low) | the D-4 column exists for every row, but four deletions in the diffs are not in it (findings 2 to 4) |

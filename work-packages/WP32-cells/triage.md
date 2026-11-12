# WP32 triage, round 1

Inputs: the four returns in `round-1/` (unedited), the planted answers in
`tests/fixtures/user-tests/ANSWERS.md`, and the package and docs at head ec3709e. A row per stop, error,
wrong guess or snag. Dispositions: **docs** (a docs edit, net neutral or negative in words), **defect**
(its own code unit with a test), **no change** (reason), **not owed** (reason a second reader accepts).
The last column is what a cell skipped or what could go.

| # | Stop or snag | Who | Page or function | Disposition | Content that did not earn its place |
|---|---|---|---|---|---|
| 1 | README has no first call; the first fit is two clicks away on the site | U1, U3 | `README.md` | docs: first screen = one install line, one first-call example (import, condition, fit) | README "Status" paragraph and the CI sentence under Quickstart (repo-process, for the maintainer) go to `work-packages/` |
| 2 | README points to docs by a repo path (`docs/index.md`), not the site | U1, U3 | `README.md` | docs: link the site | the repo-path link |
| 3 | README never says to `cd` into the checkout (`uv sync` in the wrong directory); one cell ran bare `python3` because only `uv run pytest` is shown | U4, U3 | `README.md` | docs: `cd` in the install line; "run everything with `uv run`" | none |
| 4 | "Choosing K" helper block imports `case` from `examples/adcs`; all four cells hit or avoided it and rewrote a five-line loop | U1, U2, U3, U4 | `user-guide/choosing-k.md`, "Helpers" | docs: the import moves into the cubesat block that uses it, so the helpers need only the installed package | the cubesat half of the page (4 of 9 sections) was skipped by every cell: it stays for the case-study reader, now marked as such in one clause |
| 5 | Report does not give the band's design count | U1 | `TensionReport.n_near_frontier` | no change in code: the field exists and prints with the report; docs: name it on the tensions page | none |
| 6 | Default target 0.10 raises `ValueError` "not bracketed" on both tables (bounds (3, 1000)); target 0.25 worked | U2, U4 | `select_temperature`; `fitting.md`, "Choosing the temperature" | **docs, not a code defect.** The message names the fractions at both ends, the cause and the three remedies, and both cells recovered from it in one step. I ran the pump table: bounds (3, 1000) raise; bounds (3, 1e4) give tau 6023 at target 0.10 and (3, 1e5) give 7401; the plain table gives 178.2 and 173.2 at (3, 1e4) and (3, 1e5). So the failure is the docs' example bounds and the unqualified "start at the default 0.10" for a table bound by an exact relation (a model sweep), which stays above the target at tau 1000 | the cap of 1000 in the page's advice |
| 7 | `plot_frontier_coordinates(ts, M)` raises `TypeError`; it takes `Z, log_v` | U2 | `user-guide/chart.md` "Plots" | docs: the bullet names the signature and where `Z`, `log_v` come from | none |
| 8 | stderr `findfont: Failed to find font weight normal for Lucida Grande` on every plot | U1, U2, U3, U4 | matplotlib | no change: it reproduces with a bare `imshow` and `colorbar` and no package import, so it is the matplotlib font cache on this machine, not the package | none |
| 9 | Report names a trilemma `[0 1 3]` on the plain table, the third member's exponent 0.004 to 0.01 | U1, U3 | `tensions.md`, "The contending set" | docs: one clause (the name counts every exponent above 1e-9; read the exponents before the name). Planted-fact check below: both cells read the pair right | the sentence "The set is found, not assumed" restates the next sentence |
| 10 | No page connects a SysML v2 model to the tool; which model elements become attribute columns, and which columns are not attributes (design variables, a `batch` label, ids), is guessed | U2, U4 (design variables also U1, U3, U2, U4: `batch`, `sample`) | `user-guide/overview.md`, pipeline step 2 | docs: **owed.** One optional clause on the existing page: any table works, a SysML v2 model's exported table is one source, design variables and labels are configuration, not attributes. Not a new page, not the first screen; the tool still needs no SysML v2 | two sentences of the overview's opening paragraph and "reads as a factor of improvement" (deleted to pay for the clause) |
| 11 | "Is fitting per batch the intended use?" (categorical column) | U1, U3 | none | covered by row 10's clause (labels are not attributes); per-group fitting is not owed | none |
| 12 | Which target fraction is meaningful for real data; is tau near 700 trustworthy | U2 | `fitting.md` | not owed beyond row 6: the docs already say the band is 1/tau and tau is a judgement; a second sentence would be caveat | none |
| 13 | Heatmap label "power_kw" is the inverted metric (sign reads opposite to raw correlation) | U2 | `tensions.md`, `plot_tensions(names=)` | not owed: U2 resolved it itself and the conditioning page says metrics are inverted | none |
| 14 | `plot_frontier_coordinates` shows no ringed near-frontier points at tau 695 and "looked like a blob" | U2 | `chart.md` | not owed: the band defaults to 1/tau and `band=` is a parameter; a reading of the chart for four metrics is the figure's job (WP33 wayfinding) | none |
| 15 | Four-metric table: "no plot for four metrics other than the heatmap" | U1, U4 | `chart.md` | not owed: `plot_frontier_coordinates` and `plot_ternary` exist; the page lists them. Wayfinding datum for WP33 | none |
| 16 | Overview read last; "I would have wanted it first" | U2 | Home, Getting started | deferred to WP33 (journeys and first screens) | none |
| 17 | `batch` column and `sample` handled by guess; "what is the lemma name for"; "does stiffness exponent 0 mean redundant"; K has no held-out criterion; 1/tau band at unit log-std | U1, U3 | tensions, choosing-k | not owed: the docs state the K limit in the page's first paragraph; the others are readings the cells answered correctly | none |
| 18 | "Install" on the Getting-started page says `git clone`; two cells did not need it | U2, U4 | `getting-started.md` | not owed: a package user without a checkout needs it; there is no PyPI release (non-goal) | none |
| 19 | Efficiency not exported by the pump model; "illustrative constants" | U4 | `tests/fixtures/` model | not owed: a question about the test model, not the docs | none |
| 20 | Own slips: wrong working directory for `table.csv`; `sed -i` on stdin; `df.corr(numeric_only=)` on system python | U1, U4, U3 | none | not owed: not documentation gaps (third is row 3) | none |

## Standing question

U1, U2, U3, U4 each answered **no**: nothing made them think they need SysML v2 or satellites. The only
satellite material a cell met was the "cubesat" line on the Home page, set aside by all, and the
cubesat blocks in "Choosing K" (rows 4 and 10 reduce both: the helpers run from the installed package and
the clause says the model side is optional). Two cells (U2, U4) said the model helped as a reader's aid
only and no page connects it to the table (row 10).

## Planted-fact check

- Plain table (U1, U3): planted pair strength and weight, exponents about `[0.48, 0.50, 0.01, 0.01]`, a
  third member in the contending set allowed. Both cells read the pair right (exponents 0.49 and 0.50;
  the contending set `[0 1 3]` seen as a dilemma with a marginal cost, stiffness absent) and flagged cost
  as marginal. U1 and U3 thought the "trilemma" label overstated it. The docs do not mislead (they say a
  small exponent is weak participation, threshold 1e-3), but they never say the name counts every exponent
  above 1e-9, so the clause in row 9 is owed. My rerun: contending set `[0 1 3]`, exponents
  `[0.49, 0.506, 0.004]`.
- Pump table (U2, U4): planted trilemma `[0 1 2]`, exponents about `[0.28, 0.23, 0.49, 0.00]`, mass
  outside the frontier but strongly associated. Both cells read it right (tau 695.5; mass exponent 0, mass
  association with flow -0.93 explained by pump size). U2 also pulled the surface back to raw units and
  found flow times head over power, the model's own law.

## Defect requests for a code unit

None. Row 6 is a docs defect; the error message already says what to do. An optional polish, not owed: at
`n_terms=1` the message could name a numeric target as the `n_terms>1` branch does ("raise the target to
about 0.24"); both cells succeeded without it, so no unit is opened for it.

# WP32 triage, round 1

Inputs: the four returns in `round-1/` (unedited), the planted answers in
`tests/fixtures/user-tests/ANSWERS.md`, and the package and docs at head ec3709e. A row per stop, error,
wrong guess or snag. Dispositions: **docs** (a docs edit, net neutral or negative in words), **defect**
(its own code unit with a test), **no change** (reason), **not owed** (reason a second reader accepts).
The last column is what a cell skipped or what could go.

| # | Stop or snag | Who | Page or function | Disposition | Content that did not earn its place |
|---|---|---|---|---|---|
| 1 | README has no first call; the first fit is two clicks away on the site | U1, U3 | `README.md` | docs: first screen = one install line, one first-call example (import, condition, fit) | README "Status" paragraph ("0.1 release candidate in preparation") and the CI sentence under Quickstart ("shards run on Linux and Windows; paper build on Linux and macOS"): deleted, not moved (`work-packages/README.md` holds a status table and does not carry either sentence). They described repo process for the maintainer and told a package user nothing to do |
| 2 | README points to docs by a repo path (`docs/index.md`), not the site | U1, U3 | `README.md` | docs: link the site | the repo-path link |
| 3 | README never says to `cd` into the checkout (`uv sync` in the wrong directory); one cell ran bare `python3` because only `uv run pytest` is shown | U4, U3 | `README.md` | docs: `cd` in the install line; "run everything with `uv run`" | none |
| 4 | "Choosing K" helper block imports `case` from `examples/adcs`; all four cells hit or avoided it and rewrote a five-line loop | U1, U2, U3, U4 | `user-guide/choosing-k.md`, "Helpers" | docs: the import moves into the cubesat block that uses it, so the helpers need only the installed package | the cubesat section was skipped by every cell: it stays for the case-study reader, now marked as such in one clause |
| 5 | Report does not give the band's design count | U1 | `TensionReport.n_near_frontier` | no change in code: the field exists and prints with the report; docs: name it on the tensions page | none |
| 6 | Default target 0.10 raises `ValueError` "not bracketed" on both tables (bounds (3, 1000)); target 0.25 worked | U2, U4 | `select_temperature`; `fitting.md`, "Choosing the temperature" | **docs, not a code defect.** The message names the fractions at both ends, the cause and the three remedies, and both cells recovered from it in one step. I ran the pump table: bounds (3, 1000) raise; bounds (3, 1e4) give tau 6023 at target 0.10 and (3, 1e5) give 7401; the plain table gives 178.2 and 173.2 at (3, 1e4) and (3, 1e5). So the failure is the docs' example bounds and the unqualified "start at the default 0.10" for a table bound by an exact relation (a model sweep), which stays above the target at tau 1000 | the cap of 1000 in the page's advice; `fitting.md`: the sentence "It follows the scikit-learn decomposition family: `fit`, `transform`, `inverse_transform`, `score_samples`, and no `predict`" (named the API's lineage; the next block shows the calls) and the clause "(about 0.30 on the table of `make_frontier_data(300, 4, n_terms=2, random_state=777)`)" (a quantified example on a table the reader does not have) |
| 7 | `plot_frontier_coordinates(ts, M)` raises `TypeError`; it takes `Z, log_v` | U2 | `user-guide/chart.md` "Plots" | docs: the bullet names the signature and where `Z`, `log_v` come from | `chart.md`: the sentence "They share one colour vocabulary, declared as module constants (`FRONTIER_COLOR`, ...)" (an implementation detail; the reader sees the colours in the plots and does not set them) |
| 8 | stderr `findfont: Failed to find font weight normal for Lucida Grande` on every plot | U1, U2, U3, U4 | matplotlib | no change: it reproduces with a bare `imshow` and `colorbar` and no package import, so it is the matplotlib font cache on this machine, not the package | none |
| 9 | Report names a trilemma `[0 1 3]` on the plain table, the third member's exponent 0.004 to 0.01 | U1, U3 | `tensions.md`, "The contending set" | docs: one clause (the name counts every exponent above 1e-9; read the exponents before the name). Planted-fact check below: both cells read the pair right | the sentence "The set is found, not assumed" restates the next sentence; `tensions.md`: the sentence "This is how the method chains with PCA: the spread along the surface is the set of trade-offs the designs exercised" (a claim about another method with no lemma or test behind it) |
| 10 | No page connects a SysML v2 model to the tool; which model elements become attribute columns, and which columns are not attributes (design variables, a `batch` label, ids), is guessed | U2, U4 (design variables also U1, U3, U2, U4: `batch`, `sample`) | `user-guide/overview.md`, pipeline step 2 | docs: **owed.** One optional clause on the existing page: any table works, a SysML v2 model's exported table is one source, design variables and labels are configuration, not attributes. Not a new page, not the first screen; the tool still needs no SysML v2 | one sentence of the overview's opening paragraph ("Some designs win on one number and lose on another.") and the factor sentence ("reads as a factor of improvement"), deleted to pay for the clause |
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

# WP32 triage, round 2

Inputs: the four returns in `round-2/` (unedited), head a3a61af and the stage as served. Round 2 is the first
re-run; the stopping rule (two re-runs, then a persisting docs stop goes to the chief engineer's list with the
cell's words) has not yet fired. Reach: no cell opened a page outside the README, the site and the package
(U2 fetched eight further site pages by script and searched them for "SysML" and "export" only; U1, U3, U4 read
the README and five to seven pages; the package source appeared in tracebacks and in U2's grep). U4 guessed
`/docs/guide/` (404). No cell was blocked: all four reached an answer.

## Round-1 rows: recurred?

| Round-1 row | Recurred? |
|---|---|
| 1 README first call | no: U3 read the README example, U1/U2/U4 ran `uv sync` and imported at once |
| 2 README repo-path link | no |
| 3 `cd` / `uv run` | the README gap did not recur; U4 again ran from the wrong directory and U3 again ran a stray command on system python (own slips, row R2-9) |
| 4 helper imports `case` | no stop. U2 still describes the helpers as "partly" importing `case`; the Helpers block does not, the cubesat block does, and U2 skipped it. U3's new snag is R2-4 |
| 5 band count | no (U2 printed `n_near_frontier`) |
| 6 not bracketed at 0.10, bounds (3, 1000) | **recurred, U2 and U4**; see R2-1 |
| 7 `plot_frontier_coordinates` signature | no (nobody used it) |
| 8 font warning | recurred, all four; matplotlib, no change |
| 9 trilemma `[0 1 3]` | recurred, U1 and U3; read right both times (R2-5) |
| 10 SysML v2 connection | the clause was found and used by U2 and U4; the remaining wish is R2-7 |
| 11 `batch`/`sample` | recurred as inference, U1 and U3 (neither opened the overview where the clause is); no stop |
| 12, 17 which target / K limits | recurred as questions, answered correctly by the cells |
| 13, 14, 15, 16, 18, 19 | no |
| 20 own slips | recurred (U3 system python, U4 working directory) |

## Round-2 rows

| # | Stop, error, snag or guess | Who | Page or function | Disposition | Content that did not earn its place |
|---|---|---|---|---|---|
| R2-1 | `select_temperature(M, 0.10, bounds=(3, 1000))` raises "not bracketed" on the exact-relation pump table; both cells recovered in one step from the message and the page's sentence | U2, U4 | `choosing-k.md` "The temperature" and `fitting.md` code blocks | **docs, again; round 1's sentence was not enough because cells copy the code block, not the prose.** Both blocks carried `bounds=(3, 1000)`. The fitting block now uses `(3, 1e4)` (its output is not quoted anywhere); the choosing-k block stays at `(3, 1000)` because its 50.0, 26.5 and 38.1 are quoted and used below, and the line after it now says real data may need `bounds=(3, 1e4)`; the fitting page says to start at the default 0.10 with `bounds=(3, 1e4)`. Not a code defect: the default bounds `(0.1, 1e4)` return 4870 on the pump table. The package default is unchanged | "a model sweep needed", "above the fractions the message gives" (the message says it), "Hold tau fixed across numbers of terms, selected at K = 1" (choosing-k says it), "and none has been studied", "the tau used" |
| R2-2 | Same target gives 8490 with bounds to 1e6 and 6023 with 1e4, "unexplained" | U4 (U2 asked the same) | `select_temperature` | **not a defect; explained, one clause added to the fitting page.** Measured on the pump table: frac_above_ is 0.215 at tau 1e3, 0.155 at 3e3, 0.10 at 6023, 0.09 at 1e4, 0.05 at 3e4, 0.025 at 1e6, so it falls slowly and many tau lie within `tol` = 0.01 of 0.10. Bisection returns the first one it meets, which depends on the bracket: 4870 (bounds 0.1 to 1e4), 6023 (3 to 1e4), 7401 (3 to 1e5), 8490 (3 to 1e6). The docstring already says "returns a tau with abs error at most tol". Tightening `tol` would change tau elsewhere (the paper's numbers); not touched | none |
| R2-3 | `tension_report` raises "only 5-6 near-frontier rows ... min_near_frontier = 10; use band=..." at K = 1, on the pump table and on plain-table batches B and C; message clear, every cell recovered in one step (band 2.1e-4, 0.00021) | U1, U2, U4 | `tensions.md` "With several terms" | docs: the sentence on `min_near_frontier` sat under "With several terms" and read as K > 1 only; it now says "(at K = 1, all rows)". Code message is right and unchanged | "Treat association as evidence only together with the exponents and the directions" (the closure sentence before it already says so) |
| R2-4 | The K-sweep helper is shown in the page and not importable from the package | U3 | `choosing-k.md` "Helpers" | no change: a package function is a feature, outside this package's scope; the page gives the code and U3 wrote a shorter loop in one step | none |
| R2-5 | "Trilemma" `[0 1 3]` with third exponent 0.004; what exponent makes a metric a real member | U1, U3 | `tensions.md` | not owed: both cells quoted the page's 1e-9 reading and read the exponents before the name (U3: "effectively a dilemma"). The threshold (1e-3) is on the page | none |
| R2-6 | `scaler=None` gives a monolemma on mass; standard and robust give a trilemma without mass; which to trust | U2 | `conditioning.md` | not owed: the page says `None` keeps the pure power law, to refit under a second conditioning and that the scaler is a choice. A rule for which scaler to trust would be advice the method does not have | none |
| R2-7 | No programmatic route from a SysML v2 model to orientation (a smaller-is-better flag in the export); "does the package read the .sysml file" | U2, U4 | none | not owed: the overview clause says the package reads tables, and both cells found it; an exporter or flag is a feature, the tool still needs no SysML v2. Both answered the standing question no | none |
| R2-8 | Heatmap tick labels "w=0.00" versus "w=0.01" unexplained | U1 | `tensions.md` Figure 3 caption | docs: caption says "w under a name is its exponent" (label is `report.exponents`) | none |
| R2-9 | Own slips: `FileNotFoundError` (script in `hts/`), system-python `numeric_only` (U3); `np.round` on the dict that `frontier_in_original_units` returns (U2) | U4, U3, U2 | none | not owed: not documentation gaps (README says `uv run`); the dict is a return type the signature shows | none |
| R2-10 | How small an `n_eff_` or near-frontier count is too small; what `conditioning_` = 52.6 means; Termination page not opened | U1, U2, U3, U4 | `termination.md`, `limitations.md` | not owed beyond R2-3: the pages exist and name both fields; no page gives a threshold because the method has none to give. Wayfinding datum for WP33 | none |
| R2-11 | Does a noise-free table suit the tool; is a band of 2e-4 meaningful | U2, U4 | `limitations.md` | not owed: the page says designed samples carry no sampling error; U2 read it | none |

## Standing question

All four answered **no**. Satellite words met: the "cubesat" line on the Home page and the cubesat section of
"Choosing K", set aside as optional by all four. Both model-side cells used the overview clause (configuration is
not attributes; the table is the route) and said the model helped as a reader's aid and for a hand check of
the answer (U2 recovered the efficiency ceiling by hand).

## Planted-fact check

- Plain table (U1, U3): pair strength and weight, exponents 0.49 and 0.50-0.51, cost 0.004, stiffness about 0;
  both cells read the pair right and flagged cost as weak (U3 "effectively a dilemma"; U1 "weak third member").
  tau 178.2 on both. Right.
- Pump table (U2, U4): trilemma `[0 1 2]` (flow, head, power), exponents 0.28, 0.23, 0.49, mass 0; both read it
  right, pulled it back to flow x head / power capped (exponents 0.198), robust scaler agreeing, and mass read
  as correlated and not binding. Right. Both reached it only after the bounds step (R2-1) and the band step (R2-3).

## Docs stop that persists

None blocking. R2-1 recurred, so the next round tests the new code blocks; if a cell hits "not bracketed" a
third time on a copied block, it goes to the chief engineer's list with that cell's words.

## Defect requests for a code unit

None. R2-1 and R2-2 are the page's example bounds and the tolerance semantics the docstring states; the
package default is not the defect and is not changed.

# WP32 triage, round 3

Inputs: the two returns in `round-3/` (unedited), head 60f92d9 and the stage as served. Round 3 re-ran U2 and U4
only, by the assistant's decision (see `WP32-decisions.md`). Neither cell raised "not bracketed". Both reached the fit
and the trilemma `[0 1 2]` (exponents 0.28, 0.23, 0.49, mass 0, pump table). No stop persists, so nothing goes to the
chief engineer's list from the cells.

## Round-2 rows: recurred?

| Round-2 row | Recurred? |
|---|---|
| R2-1 "not bracketed" at 0.10, bounds (3, 1000) | no: both cells copied the pattern, `select_temperature(M, 0.10, bounds=(3, 1e4))`, tau 6023.1, no error |
| R2-2 tau moves with the bounds | no as a question; U2 and U4 both note the fitting page's warning and read it as given |
| R2-3 K = 1 band error | recurred in a new place, R3-1 |
| R2-5 trilemma reading | read right by both (U4 tested tau 50, 200, 1000, 4760: the set is stable) |
| R2-6, R2-10, R2-11 questions | recurred as questions (which tau to report, identity of physics versus trade, mass exponent 0); answered by the cells, no stop |
| R2-7 no route from the model to orientation | recurred as the step 6 wish, both cells; the same disposition (the overview clause says the package reads tables) |
| R2-9 own slips | U2 only, R3-2 |
| font warning (row 8) | U4 reports it three times; matplotlib, no change |

## Round-3 rows

| # | Stop, error, snag or guess | Who | Page or function | Disposition | Content that did not earn its place |
|---|---|---|---|---|---|
| R3-1 | `tension_report(ts, M)` at K = 1 right after `select_temperature` (tau 6023.1) raises "only 6 near-frontier rows (|log V| < 0.000166) but min_near_frontier = 10; use a larger band, band=0.00021 ..., or fit at temperature=4.76e+03 ..." on the exact-relation pump table; both cells refit at tau 4760 (U2, U4) in one step from the message and got 10 rows | U2, U4 | `tension_report`; `fitting.md` | **no change; residual.** The assistant ruled: the message names the fix and all three cells that met it (U1 batches, U2, U4, over rounds 2 and 3) recovered in one step. The review lists it as a residual, not a defect and not a caveat for the docs. The package is unchanged | none |
| R3-2 | `FileNotFoundError: 'table.csv'` running `run.py` from inside the checkout | U2 | none | not owed: an own slip (R2-9 again); the README says `uv run` and the cell recovered by running from its own directory with `--project` | none |
| R3-3 | Guessed `/docs/overview/` (HTTP 404; the page is `/docs/user-guide/overview/`); the browser pane refused a new tab (tab cap), so U2 read the pages over HTTP as converted text and did not see them rendered | U2 | stage | no change: the guess is a reader's wayfinding datum (cf. R2's `/docs/guide/`), found in two steps. HTTP-text reach is accepted for the docs text by the assistant; the rendered pass is the reviewer's, and the review rendered the pages | none |
| R3-4 | "README does not say which columns are attributes; the overview page says it, found late" | U2 | `README.md`; `user-guide/overview.md` | not owed beyond row 10: the overview clause (design variables and labels are configuration, not attributes) is there and U4 found it fifth and used it; U2 reached it twelfth because it read the conditioning page first. The README's first screen is one install line and one first call by decision (row 1), and a column rule there would regrow it. Reading order is the wayfinding datum of row 16, with WP33 | none |

## Standing question

Both answered **no**. The closest quotation both give is the overview clause ("any table works, and a SysML v2 model's
exported table is one source"), read as optional. The cubesat example on the Examples page was set aside.

## Planted-fact check

Pump table: trilemma `[0 1 2]` (flow, head, power), exponents 0.28, 0.234, 0.487, mass 0; both read it right, both
noted that power is defined by the model from flow and head so the trade is partly an identity (U4: "partly a
definition"), and mass associated with flow (-0.93) but not binding. Right, and matching the answers file.

## Defect requests for a code unit

None.

## Content that did not earn its place

None this round: no docs edit followed it.

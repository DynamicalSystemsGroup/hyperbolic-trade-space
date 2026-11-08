# WP7 — Review report

| | |
|---|---|
| **Scope of work** | `work-packages/WP7-scope-of-work.md` (draft 3, two regimes of the SysML-modelled cubesat) |
| **Scope approval verified** | The project has no PRs (`gh pr list` empty); the recorded act is `work-packages/WP7-decisions.md`, "Scope approval (approval gate)", supervisor mzargham, verbatim "accept 4b and approve 7 and 8. given how long its been remember to send the notebook author to look at the acds-lifecycle-demo and hc-marimo repos and pages sites to get a sense of my style", document `de2f758`, recorded in `44e8d59`. |
| **Work reviewed** | `main` at `db4aa0a`: `94f5fdf` (step 0 probe note), `e5cbc1a` (style study), `67eea92` (predictions), `32f513d` (check simulations, script, column tests), `71af906` (notebook, figures, tests), `db4aa0a` (author notes); predecessor `44e8d59`. Diff base `44e8d59`. |
| **Supervisor (accepts)** | mzargham |
| **Acceptance record** | Verbal acceptance in chat, quoted verbatim in `work-packages/WP7-decisions.md`, after this report |

A fresh reviewer who built none of WP7. Every command below was run in this session (`unset VIRTUAL_ENV`). Review only: two trial edits to the notebook were made and undone with `git checkout`; no repair was made.

## Deliverables

| ID | Verdict | Evidence |
|---|---|---|
| D-1 | met | `examples/adcs/adcs_trade_study.ipynb`, 62 cells, 16 numbered sections; every code cell has outputs; my own re-execution reproduced all text outputs identically (below). |
| D-2 | met | Nine PNGs `examples/adcs/figures/01_…` to `09_…`; re-execution rewrote them byte-identical (`git status` clean afterwards). Figures 01, 03, 05 inspected (see G-2). |
| D-3 | met | `data/check_designs_cubesat.csv`: 6 rows, `role` candidate 3 / proposal 3. |
| D-4 | met | Probe note section "WP7 step 0" (`94f5fdf`, +76 lines): both regimes, gate statement. |
| D-5 | met | `tests/test_notebook.py` (12 tests) passes; trial below. |
| D-6 | met | `WP7-decisions.md`: approval verbatim, standing style instruction, style study, author notes; acceptance "pending". |

## Requirements

| ID | Verdict | Evidence |
|---|---|---|
| R-1 | met, one deviation (G-3) | `OPENSYSML_BINARY=/nonexistent/bad uv run --group notebooks jupyter nbconvert --execute --to notebook --output-dir <fresh tmp> --output run.ipynb examples/adcs/adcs_trade_study.ipynb`: completes, 11.5 s. Text outputs of all cells diff-identical to the committed notebook (118144 characters each; numbers equal exactly on this platform). Run from the working tree with a temp output directory, not a fresh clone. The notebook reads four files, not the three named (it adds `check_predictions_cubesat.csv`); `test_inputs_are_the_cached_files` asserts exactly those four and no import of opensysml, `cubesat_model`, `generate_dataset`, `make_check_designs`, `adcs_sim`. |
| R-2 | met | `tests/test_notebook.py::test_executed_without_errors_and_with_figures` and `test_png_copies_exist` pass; no error or stderr outputs. |
| R-3 | met (see section order, G-8) | Sections 1 to 16 in the order of the scope; `test_sections_in_order` passes. Sensitivity (8) and interpretation (9) follow the report (7), which they need. R-3 lists stages, not their placement relative to interpretation; acceptable. |
| R-4 | met | Orientations as probe (cell 4); `std of log m` = 1 for every metric and the log-spread column printed; rows removed per condition printed (settled 24, power 0, momentum 165 in order, positivity 105; 706). Five sensitivity variants (baseline, robust, uniform shift, alternating shift, eight metrics); persistence reported. The persistence claim is overstated for one clause (G-1). |
| R-5 | met | τ = 38.10, `frac_above_` 0.096 against 0.10; table of exponents, `n_eff_`, objective, τ printed; sweep on 12 values in (3, 1e3) plus ∞; non-monotone region below 3 described. No test parses the table; inspected. |
| R-6 | met with defects (G-2) | Two subset surfaces, four-metric hole chart, log planes, titles present. Axis labels read "(m)" for the conditioned metric and are not in original-attribute units. |
| R-7 | met | Report cell prints `n_lemma = 6`, contending set, working exponents, associations, directions, counts 20/25/6. I scanned markdown cells 0 to 27 myself for tension, trade, against, contend, lemma, heavier, bottleneck: no tension, dilemma or n-lemma is named before cell 28; cell 1 says explicitly that none is named; cells 16 and 23 show fitted exponents and a remark that large wheels sit at the fast end, with no named tension. Trial 1 and 2 below. |
| R-8 | met with gaps (G-5) | Section 9 gives mechanism, design variable and what would change it for the effort, mass, pointing and energy tensions; the three near-redundant pairs are reported as accounting identities; thin margins disclosed; "What the report does not expose" present. Principal directions 3 and 4 and the peak-slew-power associations are not explained (the last are disclosed as unexplained). |
| R-9 | met | Section 2 per-class feasibility; wheel-class statement verbatim "both a feasibility boundary and a frontier tension when the wheel is the bottleneck", "a feasibility boundary only in the baseline regime", "depends on the operating regime" (`test_wheel_class_statement_and_disclosures`); mass in primary contending set, absent in baseline; counts 20/25/6 and 79/23/1; "6 of the 51 near-frontier designs have large wheels". |
| R-10 | met | Section 10 (wheel, tracker, panel, battery, Kp, Kd table and figure 07; per-class refits with contending sets); section 11 (3 candidates: log V, novelty V−1, calibrated novelty, improvement factors); section 12 pull-back agrees with `score_samples` to 2.6e-15 (I got 1.1e-16 by my own formula). |
| R-11 | met | Regressor GP; predictions printed before comparison (`test_predictions_precede_the_check`); git order `94f5fdf` (02:31:48) < `e5cbc1a` < `67eea92` predictions (02:34:27) < `32f513d` results (02:36:25) < `71af906` notebook (02:58:13). Comparison reported: log V inside band for all three (0.32, 0.34, 0.71 of band), Z outside (1.35, 2.21, 3.09 bands), proposals 1 and 2 fail `dod_ok`. I reproduced these from the CSVs with a fresh four-metric fit (dZ 0.0880/0.1439/0.2007; dlogV −0.021/−0.0221/−0.0459; eclipse reserves −2.12/−2.03/51.3). |
| R-12 | met | Section 15: stratified, censored, illustrative, stiff-loop (third underdamped, 4.7 %, quoted from the WP4b record and labelled not recomputed; the values match probe note line 762), 37.2 % momentum, power never limits a slew (3.2 % capped, all large; 3.5 % of feasible), near-frontier sizes (51, 71, 16.2, 12 to 19). |
| R-13 | met | Section 16: machine-verified list with pointers, L1 to L9 with sections, R1/A4/F5/F10 and the regime with failure modes, seven-item "What remains for a human". |
| R-14 | met | Step 0 note precedes everything; gate statement present; contending sets 6 and 6 as expected. |
| R-15 | met, out-of-scope files (G-3) | `uv run pytest`: **897 passed, 8 skipped, 1 xfailed** (93 s). `ruff check .`: All checks passed. `ruff format --check .`: 101 files already formatted. `uv lock --check`: Resolved 173 packages. `git diff --stat 44e8d59..HEAD` shows no change to `src`, `pyproject.toml`, `uv.lock`, `docs/` pages, datasets or model. |
| R-16 | met | Message grep (co-authored, generated with, claude, case-insensitive) over `94f5fdf~1..HEAD`: 0. All 181 commits author Michael Zargham (committer likewise). `gh run list --limit 10`: all ten success, latest `db4aa0a` in 3m58s. Red runs in the last 40: three, all WP4b (`7a175a4`, `4897434`, `be9ea7d`, the aggressive-box reproducibility tolerance, fixed by `620cfc8`, as recorded in the WP4b review). No WP7 run is red. Notebook raw JSON: no `/Users/`, `/private/`, `/var/` (`test_no_machine_specific_paths`; my grep of the output text). |

## Definition of good enough

| Item | Verdict | Evidence |
|---|---|---|
| D-1 to D-6 exist | met | above |
| R-1 to R-16 pass with evidence | met, with the gaps below | above |
| Contending set at least 2, not asserted; tensions and alignments explained; WP4b finding reported (R-7 to R-9) | met | above; gaps G-1, G-5 qualify "every" |
| Non-goals untouched | met | no toolkit, dataset, model or docs page change |

## Outside the scope

- **Out-of-scope changes:** `examples/adcs/make_check_designs.py` (251 lines) and `tests/test_check_designs.py` (the scope's default was a script kept out of the repository unless the reviewer asks); `examples/adcs/data/check_predictions_cubesat.csv` (not in D-3 or R-1's list, but needed to show predictions recorded before the check). `e5cbc1a` adds the style study to the decisions file, which the supervisor's instruction invites. See G-3.
- **Non-goals touched:** none found. No trilemma named early, no preference among designs; the baseline regime is not claimed to have an agility-against-mass tension.

## Independent recomputation

Own scripts (not committed; in the session scratchpad). Feasible set, LP and soft fit rebuilt with `scipy.optimize.linprog` and L-BFGS from the CSV alone (per-column log, centred, unit standard deviation).

| Quantity | Notebook | Mine |
|---|---|---|
| feasible n (s/m/l) | 706 = 191/248/267 | identical; baseline 780 = 239/279/262 |
| contending set τ = ∞ | mass .223, slew .201, energy bal. .169, effort .143, pointing .135, DoD .129 | identical to three decimals |
| near-frontier at τ 38.1 (s/m/l) | 20 / 25 / 6 (51) | 20 / 25 / 6 (51) |
| settling–mass, slew–mass Pearson (Spearman) | −0.54 (−0.34), −0.48 (−0.33) | same |
| pointing–effort, settling–pointing | −0.36 (−0.48), +0.18 (+0.20) | same |
| slew–effort, pointing–mass | −0.87 (−0.83), −0.64 (−0.68) | same |
| median slew/settling | 0.60 (baseline 0.74) | 0.601 (0.745) |
| baseline contending set | effort .434, slew .253, power margin .179, settling .081, pointing .040, eclipse reserve .013 | identical (baseline near-frontier counts from my approximate soft fit differ by one or two; the package counts agree with the WP4b review) |
| pull-back vs `score_samples` | 2.55e-15 | 1.1e-16 (manual formula) |
| check designs | table of section 13 | reproduced (above) |
| candidates log V | −0.115, −0.0717, −0.1436 | −0.1150, −0.0717, −0.1436 |

Finding from the recomputation: in the eight-metric sensitivity refit the first principal direction loads settling time at +0.04 (total mass −0.58, control effort −0.46, depth of discharge +0.43, eclipse reserve +0.33, pointing +0.31), so no agility metric loads against effort in it (G-1).

## Trial

Inserted "This is a trilemma." into markdown cell 7 (before the report) of the committed notebook: `tests/test_notebook.py::test_nothing_named_before_the_report` FAILED (11 others pass). Restored with `git checkout`. A second trial inserting "mass is traded against slew" failed the same test. Limit: the guard is a phrase list; a paraphrase such as "speed costs weight" would pass it. My own scan found no such sentence (G-8). `git status` clean.

## Substantive reading as a reader

(a) Cell by cell. The notebook opens with a card (title, byline, stack line, one paragraph, pointers), states "Cached data, no simulation", then section 1 asks the designer's questions in physical terms (what does a faster slew cost, what does sharper pointing cost, what does a bigger wheel do) and says that no tension is named until section 7. Steps are small: sixteen numbered sections, a short markdown cell, one code cell, then a "What the output shows" cell and a "Next" line. Interpretation follows outputs: section 7's reading is labelled "a reading of the output, not yet an explanation", section 9 is headed as the author's interpretation for human validation and "can be wrong", and section 14 adds an "Author's interpretation" paragraph. The closure caution is quoted before the interpretation and the interpretation says the association is not the evidence, the exponents are. The wheel-class statement is present in the scope's words. The regime comparison is a table plus figure 09. Disclosures are all present, with numbers: stiff-loop regime, 37.2 % small-wheel momentum failures, large wheels few (6 of 51; 2.2 % of large-wheel designs near the frontier), thin margins including the Spearman −0.34/−0.33 against Pearson −0.54/−0.48 on the mass associations, power never limiting a slew. Near-redundant pairs are called accounting identities. Propose-predict-check is honest: log V inside the band, Z outside for all three, two of three proposals fail `dod_ok`, measured designs still in white space, and "a mixed one". The V&V section ends with the machine list and a seven-item "What remains for a human". It reads as a notebook a supervisor would recognise as honest. Weaknesses are in G-1, G-2, G-5, G-7, G-9.

(b) Style instruction (supervisor's references read: `jaxa_notebook.ipynb`, `homicidal_chauffeur.py` section structure, `TALK_NOTES.md`, both Pages sites). The notebook honours the style in 11 of 15 points and falls short in four.

1. Embodied question first: partly. The question is the cubesat engineer's and comes first, but the "figure" after it is ten histograms of raw columns (figure 01), not the system, a slew or a puzzle with an answer that intuition does not predict (hc-marimo's star puzzle, the ADCS site's REQ-001 at 105 s against the simulation). Falls short.
2. Small visible steps: met in structure; but several cells are long (cell 31 and the section 9 interpretation, about seven dense paragraphs in one cell). The references use two to six sentence cells. Partly.
3. Prose after output, marked: met.
4. V&V as a distinction and a section: met (section 16).
5. "What remains" list: met, concrete (figures 03 to 05, explanations, conditioning).
6. Limits plain and early: met in voice and numbers; they sit in section 15, late, though the key ones (feasibility boundary, thin margins, n=51) recur in 2, 7, 9.
7. One visual vocabulary: met (constants printed in the first cell, one added colour declared); minor: hole colour is `#D55E00` (vermillion) but is called "red" in text and titles.
8. Notation at first use plus table: met.
9. Assumed/derived/inherited: met (R1, A4, F5, F10, regime by ledger tag).
10. Credit, no priority claims: met (source paragraph, "novelty" only as V−1).
11. Show the unwelcome result: met (Z misses, `dod_ok` failures, the candidate that failed momentum and was changed).
12. Landing-page tone and card: partly. The opening cell is card-like; there is no call-to-action link and no source link at the foot beyond doc pointers.
13. Narrative arc: partly. "Next" lines end each section and it ends on the human step; but the sections 8 to 9 detour (sensitivity then interpretation) sits between report and tools.
14. Honest mode flags: met ("read from … (cached …)").
15. No emojis, no hype: met.

Falls short: points 1, 2, 12 (and 13 mildly). Recorded as G-7, a style judgement for the supervisor, not a scope failure.

(c) Numbers: confirmed (table above).

(d) Claims against docstrings and `docs/limitations.md`. The L2 remark is correct: `lemma_02_shift.py` proves only a uniform shift (same constant on every metric) leaves the exponents unchanged and says per-metric shifts change the facet; the notebook includes the uniform shift as a code check and the alternating shift as the probe, as the docstring prescribes. The notebook's "multiplies every score by the same factor" is loose (it adds a constant to log V). The Spearman −0.34 / Pearson −0.54 is disclosed as numbers and as "only just beyond −0.30", which is right against R-9's threshold; the gap itself (rank against linear association on 51 points with six large-wheel designs) is not discussed (G-6). The τ < 3 caution matches `docs/limitations.md`. R1 not certified: stated. Overstatement found: G-1 and G-9.

(e) The `pred_std_*` columns of `check_predictions_cubesat.csv` hold the delta-method standard deviation of the four predicted metrics (shape (3, 4)), not of Z and log V. The notebook discloses this twice (cell 50 code output and the cell 51 note, with a check that the recorded values equal a fresh call, difference 5.8e-09), reads them under their true meaning and leaves the file as recorded (it is the authority for predictions committed before the simulations). The disclosure is adequate for the notebook; the misnomer remains in the CSV header, in the docstring of `make_check_designs.py` ("``predict_std``" of log V and Z) and in `tests/test_check_designs.py` (`pred_std_log_v` required). Listed as G-4; no result depends on it, the Z and log V comparison does not use these columns.

(f) Damping numbers: quoted from the WP4b record (probe note: 33 % underdamped, 4.7 % below 0.5), labelled "computed there from the linearised loop, not recomputed in this notebook". I did not recompute them either (the dataset has no damping or inertia column and recomputing needs the model's inertia). Labelled, traceable, adequate for a disclosure; note that the note's design-time figures were 5.3 % (box) and 33 %, and the 4.7 % is the post-hoc figure on the 1000 designs.

(g) Section order: sensitivity and interpretation after the report is right, because the sensitivity runs the report under changes and the interpretation must follow its output (R-7, R-8 require "after the report output"). R-3 lists stages, not where interpretation goes, so the order conforms. A reader meets interpretation in section 9 after two intervening sections; accepted.

## Observations (not counted as failures)

- Scope text expected "7 near-frontier large-wheel designs"; the notebook's own final-τ report gives 6, quoted from its own output (the step 0 note says to do so).
- Time-axis tension: the style study commit `e5cbc1a` landed after step 0 and before notebook authoring; the instruction was observed in effect.
- The notebook was authored by a script kept outside the repository (as the scope's default says); no regeneration path for the notebook exists in the repo.

## Open decisions (for the supervisor)

Substantive (affect a good-enough item or a non-goal) are asked one at a time; wording-level items go as one item. All pending.

- **G-1 (substantive, affects R-4 persistence).** Cell 34 says "effort loads against agility in the first direction persists in all five" variants. In the eight-metric refit the first direction has settling time at +0.04 and no agility metric among its top loadings (cell 33 shows only the top four). Correct the sentence to four of five, or show the loadings — options: accept as is / fix before acceptance / follow-up work package — **pending**.
- **G-2 (wording-level with a requirement attached, R-6).** Figure axes read "(m)" for conditioned metrics, which can be read as metres, and are not in original-attribute terms; figure 03 left panel does not obviously show the surface hugging the upper envelope (inspect it); holes are vermillion but called "red" — options: accept as is / fix before acceptance / follow-up work package — **pending**.
- **G-3 (out of scope).** `make_check_designs.py`, `tests/test_check_designs.py`, `check_predictions_cubesat.csv` are outside D-3 and R-15's file list; the notebook reads four files, not three (R-1) — options: accept as is / fix before acceptance / follow-up work package — **pending**.
- **G-4 (follow-up candidate).** Mislabelled `pred_std_*` columns in `check_predictions_cubesat.csv`, in the script docstring and in `tests/test_check_designs.py`; notebook discloses it. A correction should be an erratum note or a new column, not an edit of the committed predictions — options: accept as is / fix before acceptance / follow-up work package — **pending**.
- **G-5 (R-8).** Principal directions 3 and 4 and the peak-slew-power associations are not explained in section 9 (the latter disclosed as unexplained and as a hypothesis); R-8 says every exposed tension and alignment — options: accept as is / fix before acceptance / follow-up work package — **pending**.
- **G-7 (style, judgment for the supervisor).** Points 1, 2, 12 of the style study fall short (histogram instead of an embodied figure, long interpretation cells, no call-to-action or source link) — options: accept as is / fix before acceptance / follow-up work package — **pending**.
- **G-6, G-8, G-9, G-10 (wording-level, one item).** G-6: the Spearman/Pearson gap on the mass associations is stated, not discussed. G-8: the "nothing named before the report" test is a phrase list and a paraphrase would pass it (my reading found none); cell 23 carries an unmarked remark on wheel classes and mass before the report. G-9: section 9's "the sensitivity check confirms it" for which member of a pair enters is partly circular (the eight-metric refit removes slew time and energy balance, so they cannot enter), the robust and alternating variants support it. G-10: "multiplies every score by the same factor" in section 8 should read "adds a constant to log V"; damping numbers are quoted not recomputed (labelled; acceptable) — options: accept as is / fix before acceptance / follow-up work package — **pending**.

## Gap dispositions

| Gap | Disposition | Reason or follow-up |
|---|---|---|
| G-1 | pending | |
| G-2 | pending | |
| G-3 | pending | |
| G-4 | pending | |
| G-5 | pending | |
| G-7 | pending | |
| G-6, G-8, G-9, G-10 | pending | |

## Recommendation

Do not recommend acceptance yet: the gaps have no disposition, and the supervisor should decide at least G-1 (an overstated persistence claim) before accepting. On the evidence the package meets D-1 to D-6 and R-1 to R-16 with gaps. The notebook re-executes without opensysml and reproduces every committed output, the numbers recompute independently, the propose-predict-check order is in the git history, the tension and regime statements follow the fit and are honest about thin margins, and the suite, linters, lock, attribution and CI are clean. Once each gap has a disposition and any "fix" is done, this becomes a recommendation to accept with the listed gaps noted.

Acceptance is the supervisor's act, recorded as named above. This report does not accept the work.

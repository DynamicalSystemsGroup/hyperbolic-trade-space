# WP7 — Review report (second pass)

| | |
|---|---|
| **Scope of work** | `work-packages/WP7-scope-of-work.md` (draft 3, two regimes of the SysML-modelled cubesat) |
| **Scope approval verified** | The project has no PRs; the recorded act is `work-packages/WP7-decisions.md`, "Scope approval (approval gate)", supervisor mzargham, verbatim "accept 4b and approve 7 and 8. given how long its been remember to send the notebook author to look at the acds-lifecycle-demo and hc-marimo repos and pages sites to get a sense of my style", recorded in `44e8d59`. |
| **Work reviewed** | `main` at `755bf5e`. First-pass review `2c28bd0`; dispositions `4e2e2a3`; G-4 rename `145a5e4`; editing pass `755bf5e`. Delivery commits `94f5fdf`, `e5cbc1a`, `67eea92`, `32f513d`, `71af906`, `db4aa0a`. Diff base `44e8d59`. |
| **Supervisor (accepts)** | mzargham |
| **Acceptance record** | Verbal acceptance in chat, quoted verbatim in `work-packages/WP7-decisions.md`, after this report |

A fresh reviewer who built none of WP7 and wrote none of the earlier reviews. Complete review from step 1, every command run in this session (`unset VIRTUAL_ENV`). Review only: one trial edit was made and undone with `git checkout`; no repair, `git status` clean afterwards. This report overwrites the first-pass report.

## Deliverables

| ID | Verdict | Evidence |
|---|---|---|
| D-1 | met | `examples/adcs/adcs_trade_study.ipynb`, 89 cells, 16 numbered sections plus a closing "Where to go from here"; 27 code cells, none without outputs, 9 embedded PNGs. |
| D-2 | met | Nine PNGs `01_two_designs` to `09_regime_comparison`; re-execution left `git status` clean and every PNG byte-identical (`cmp`). `01_attributes.png` was deleted in `145a5e4` and replaced by `01_two_designs.png` in `755bf5e`. |
| D-3 | met | `data/check_designs_cubesat.csv`, 6 rows (candidate 3, proposal 3). |
| D-4 | met | Probe note section "WP7 step 0" (`94f5fdf`), both regimes, gate statement. |
| D-5 | met | `tests/test_notebook.py`: 17 tests (12 before the editing pass), all pass; trial below. |
| D-6 | met | `WP7-decisions.md`: approval, style instruction, style study, author notes, round-1 dispositions, editing-pass note; acceptance "pending". |

## Requirements

| ID | Verdict | Evidence |
|---|---|---|
| R-1 | met, one deviation (G-3, accepted) | `OPENSYSML_BINARY=/nonexistent/bad uv run --group notebooks jupyter nbconvert --execute --to notebook --output-dir <scratch> --output run.ipynb examples/adcs/adcs_trade_study.ipynb`: completes. All 27 code cells: text outputs identical to the committed notebook (29692 characters), all 9 embedded PNGs identical (base64 equal), all cell sources equal. Run from the working tree, not a fresh clone. `read_csv` calls: `adcs_designs_cubesat.csv`, `adcs_designs_cubesat_gains.csv`, `check_designs_cubesat.csv`, `check_predictions_cubesat.csv` (four files, not the three named). Mentions of opensysml, `generate_dataset`, `cubesat_model` are prose or print strings only; no import, no regeneration. |
| R-2 | met | `test_executed_without_errors_and_with_figures`, `test_png_copies_exist` pass; no error outputs. |
| R-3 | met | Sections in the scope's order (`test_sections_in_order`); sensitivity (8) and interpretation (9) after the report (7), as in round 1 (G-8 family, accepted). The hook figure sits in section 1, before section 2 (`test_hook_figure_is_early_and_names_no_tension`). |
| R-4 | met | Orientations as probe; `std of log m` = 1 for every metric; removals 24 / 0 / 165 / 105 to 706; five variants. The G-1 sentence is now correct (see G-1 below). |
| R-5 | met | tau 38.10, `frac_above_` 0.096 against 0.10; exponent table, `n_eff_` 16.2, objective, sweep over 12 values plus infinity. |
| R-6 | met, one qualification (G-12) | Figures 03 to 05 inspected as PNGs. Axis labels now read "conditioned X (inverse unit; larger is better)" or "(unit; larger is better)"; grep for "(m)" and for a bare "red" in the notebook: no hits (the only "(m)" is the formula `V(m)`). Figure 03, first subset: the edge-on view shows the V = 1 line cutting along the upper edge of the cloud, ringed near-frontier designs on the line from lower to upper end; the 3-D wireframe is readable but cluttered. Second subset: line hugs the cloud over the lower and middle range and runs well above every design at the upper end (G-12). |
| R-7 | met (G-11 wording) | Report cell prints `n_lemma = 6`, set, exponents, associations, directions, counts 20/25/6. I scanned markdown cells 0 to 26 for tension, trade, against, contend, lemma, bottleneck, cost, binds: no tension, dilemma or n-lemma is named; cell 1 says none is named until section 7. Cell 23 (figure reading, before the report) states subset-fit exponents and that "pointing error hardly binds in that three-metric view" (G-11). Trial below. |
| R-8 | met with accepted gaps (G-5) | Section 9 is now 19 short cells, each tension split into mechanism, design variable, what would change it; accounting identities; thin margins; "What the report does not expose"; unexplained associations disclosed. Directions 3 and 4 still unexplained (G-5, accepted). |
| R-9 | met | Per-class feasibility (small 191/344, medium 248/345, large 267/311), wheel-class statement in the scope's words (cell 56 and cell 80), baseline table, 20/25/6 and 79/23/1, "6 of the 51" large. |
| R-10 | met | Sections 10 to 12; pull-back vs `score_samples` 2.55e-15. |
| R-11 | met | GP regressor; predictions printed before the comparison; git order below; comparison reported as mixed (log V inside the band 0.32/0.34/0.71, Z outside 1.35/2.21/3.09, proposals 1 and 2 fail `dod_ok`). |
| R-12 | met | Section 15 intact, numbers unchanged. |
| R-13 | met | Section 16 intact; the human list item 1 now asks the reader to judge the edge-on views too. |
| R-14 | met | Step 0 note precedes the notebook (`94f5fdf` before `71af906`). |
| R-15 | met, out-of-scope files (G-3, accepted) | `uv run pytest`: **902 passed, 8 skipped, 1 xfailed** (96 s). `uv run ruff check .`: All checks passed. `uv run ruff format --check .`: 102 files already formatted. `ruff check` and `ruff format --check` on the `.ipynb` alone: passed. `uv lock --check`: Resolved 173 packages. `git diff --stat 44e8d59..HEAD`: no change to `src/`, `pyproject.toml`, `uv.lock`, docs pages, datasets or model. |
| R-16 | met | Message grep (co-authored, generated with, claude, case-insensitive) over `94f5fdf~1..HEAD`: 0. All 186 commits author and committer Michael Zargham. `gh run list --limit 10`: all ten completed success, latest `755bf5e` (4m7s). Notebook raw JSON: no `/Users/`, `/private/`, `/var/`. `145a5e4` was pushed together with `755bf5e`, so it has no run of its own (G-14). |

## Definition of good enough

| Item | Verdict | Evidence |
|---|---|---|
| D-1 to D-6 exist | met | above |
| R-1 to R-16 pass with evidence | met, with the gaps below | above |
| Contending set at least 2, not asserted; tensions and alignments explained; WP4b finding reported | met | above; G-5 accepted, G-11 wording |
| Non-goals untouched | met | no toolkit, dataset, model or docs-page change; no trilemma named early; baseline not claimed to have an agility-against-mass tension |

## Outside the scope

- **Out-of-scope changes:** unchanged from round 1, G-3 (accepted): `make_check_designs.py`, `tests/test_check_designs.py`, `check_predictions_cubesat.csv`. New in this round: `145a5e4` and `755bf5e` edit `WP7-decisions.md` (inside `work-packages/`, allowed by R-15) and delete `01_attributes.png` (replaced; same figure slot).
- **Non-goals touched:** none.

## Verification of each fix

**G-1 (persistence sentence): fixed.** Cell 36 now says control effort loads against an agility metric in the first principal direction in four of five variants, names the exception (eight-metric refit), and cell 35 prints per-variant loadings. From the notebook's own printed table: baseline effort -0.40 vs slew +0.40; robust -0.62 vs slew +0.35; all-metric shift identical to baseline; alternating -0.48 vs slew +0.51 / settling +0.55; eight-metric effort -0.46 with settling +0.04 and total mass -0.58. Four of five holds; the parenthesis "three independent variants" (the all-metric shift is the baseline again by L2) is also correct. Supporting sentences in cell 36 (slew time in three variants, settling in two; effort in the set in three, absent under robust and eight-metric; set size 6, 6, 6, 6, 5) all check against the printed table. My own rough PCA of the eight-metric near-frontier set also gives a small settling loading (+0.09).

**G-2 (axes, figure 03, colour): fixed, with a qualification (G-12).** No bare "(m)" labels; "conditioned ... larger is better" wording throughout; the "red" word is gone (a test forbids it); holes are named vermillion and are `#D55E00`. I looked at the PNGs: figure 03 is now 2 x 2. In the first subset the V = 1 surface visibly hugs the upper envelope in the edge-on view (ringed designs along the line from end to end). In the second subset it does not at the upper end, and the text says so in the words "towards the upper end the line runs well above every design, so the surface extends beyond the sampled designs there and the 3-D wireframe overstates what the data support". The statement is honest and matches the picture.

**G-7 (style): fixed in part, see style section.** Hook figure `01_two_designs.png` is early (cell 6, before section 2): left panel, 706 designs by slew time and mass coloured by wheel class with A (fastest slew) and B (lightest bus) marked; right panel, their ten attributes as factors of the table median. It poses a question ("what else came with it?", "Neither is the better design") and names no tension; the markdown beside it states that the notebook asks this of all ten attributes. Section 9 and the report, regime and verification cells are split into one-idea cells (section 9: cells 39 to 57). The closing cell has "Where to go from here", "Start wherever suits you", links to the repository, `docs/method.md`, the spec, `docs/api.md`, `docs/limitations.md`, the SysML files, and a five-line recipe. The repository URL equals `git remote` and `gh repo view`; the linked paths exist in the repository. Cosmetic: the hook figure legend overlaps the lowest pair of bars (G-13).

**G-4 (column rename): fixed.** `git diff` of data rows between `145a5e4~1` and `145a5e4`: `diff` and `cmp` report the rows identical, only the header differs (`pred_std_z1, z2, z3, log_v` to `pred_std_slew_time_s, pred_std_pointing_error_deg, pred_std_control_effort, pred_std_total_mass_kg`). `make_check_designs.py` writes the new names and its docstring and `_std` docstring say what they hold; `tests/test_check_designs.py` and the new test in `tests/test_notebook.py` check them; the notebook's `predict_std` cell recomputes them (difference 5.8e-09) and says the header was corrected after the check with values byte-identical. Commit order evidence still holds: `94f5fdf` (02:31:48) < `67eea92` predictions (02:34:27) < `32f513d` results (02:36:25) < `71af906` notebook; `test_predictions_precede_the_check` passes. Judgement on renaming a committed prediction record: acceptable, because the numbers are unchanged, git keeps the original header at `67eea92`, and the notebook discloses the change in the place where the columns are read. The prediction values were fixed before the check; only labels changed after.

**G-10 (wording): fixed; the first-pass suggestion was less accurate than the author's text.** Cell 34 says the uniform shift "adds that constant to every score w.u and to the fitted offset beta and, by L2, leaves the exponents unchanged (it does not multiply the scores)". `derivation/lemma_02_shift.py`: J(w; U + c 1^T) = J(w; U) + c, and beta = J(w*), so beta shifts by c, w* is unchanged, and log V = score minus beta is unchanged. The author's wording is correct. The first-pass remark that it should read "adds a constant to log V" was wrong (log V does not change). The old wording survives only in the first author note of `WP7-decisions.md`, which the editing-pass note marks as the earlier draft.

## Independent recomputation

Own script (scratchpad, not committed), from the CSVs alone: per-column log, orientation, centring, unit standard deviation; `scipy.optimize.linprog` for the tau = infinity support; L-BFGS soft fit on the simplex at the notebook's tau = 38.10.

| Quantity | Notebook | Mine |
|---|---|---|
| feasible n (s/m/l) | 706 = 191/248/267 | identical; baseline 780 = 239/279/262 |
| contending set tau = inf, primary | mass .223, slew .201, energy bal. .169, effort .143, pointing .135, DoD .129 | identical to three decimals |
| contending set, baseline | effort .434, slew .253, power margin .179, settling .081, pointing .040, eclipse .013 | identical |
| near-frontier at tau 38.10 | 51 = 20 / 25 / 6; baseline 103 = 79 / 23 / 1 | 51 = 20 / 25 / 6; baseline 105 = 79 / 25 / 1 at my own approximate tau 41.2 (approximate solver, tau chosen by grid) |
| settling-mass, slew-mass (Pearson, Spearman) | -0.54 (-0.34), -0.48 (-0.33) | same |
| pointing-effort, settling-pointing, slew-effort, pointing-mass | -0.36 (-0.48), +0.18 (+0.20), -0.87 (-0.83), -0.64 (-0.68) | same |
| pull-back vs `score_samples` | 2.55e-15 | log-spreads k = 0.8282, 0.6455, 0.8604, 0.0658 match the notebook table; pull-back identity holds to rounding |
| candidates, proposals | section 11, 13 tables | unchanged since round 1, not re-derived this pass; the notebook's outputs re-executed identically |

## Trial

Appended "This is a trilemma." to markdown cell 7 (before the report cell) of the committed notebook: `uv run pytest tests/test_notebook.py` gave 1 failed (`test_nothing_named_before_the_report`), 16 passed. Restored with `git checkout examples/adcs/adcs_trade_study.ipynb`; rerun: 17 passed; `git status` clean. Limit unchanged: the guard is a phrase list (G-8, accepted).

## Substantive reading as a reader

Read all 89 cells in order against the outputs. The notebook opens with a card (title, byline, source link, stack, one paragraph, "Start wherever suits you"), says "Cached data, no simulation", then section 1 poses the designer's questions in physical terms, a notation table, one setup cell, the load, and the hook figure with two designs. Steps are mostly small; section 9 is now readable one idea at a time. Interpretation follows outputs and is marked as the author's. Honest reporting is intact: sensitivity exceptions, Spearman against Pearson, the large-wheel thinness, the propose-predict-check miss, "a mixed one", seven human items. Numbers in the prose that I checked against printed outputs agree (cells 10, 13, 16, 19, 23, 31 to 36, 62, 65, 68, 74, 79).

**Style instruction, point by point** (after reading `jaxa_notebook.ipynb` (31 cells, markdown cells median 295 characters, largest 1072), `homicidal_chauffeur.py` (twelve sections with section signs, §11 V&V, §12 further reading), `TALK_NOTES.md` (beat 2 puzzle, beat 9 V&V, beat 10 end on the human step), and both Pages sites (hc-marimo: four cards with arrow CTAs, "Start wherever suits you", source link; ADCS site: take-away, tables, event cards with arrow links, footer source link)).

1. Embodied question first: **partly honoured**, improved. A figure now appears before section 2 and it poses a question about two real designs, but it is a scatter and a bar chart of table values, not the system, a slew or a puzzle whose answer intuition does not predict (the references' star, REQ-001 at 105 s against the simulation). Residual: judgment call for the supervisor.
2. Small visible steps: **partly honoured**. Section 9 and the report, regime and V&V cells are split. Overall the 62 markdown cells have median 703 characters (reference 295); the largest are 3097, 2816, 2469 and 1862 characters (setup, section intros, the limits list). Honoured where it was worst, not everywhere.
3. Prose after output, marked: honoured.
4. V&V as distinction and section: honoured.
5. "What remains" list: honoured.
6. Limits plain and early: honoured in voice and numbers; the full list is in section 15, key items recur earlier.
7. One visual vocabulary: honoured; vermillion is named consistently. Minor: the medium-wheel orange and the vermillion holes are close in figure 05 (G-13).
8. Notation at first use plus table: honoured.
9. Assumed, derived, inherited: honoured.
10. Credit, no priority claims: honoured.
11. Show the unwelcome result: honoured.
12. Landing-page tone and card: **now honoured** in substance: card opening with source link and stack line, "Start wherever suits you" twice, a closing section with links to repo, spec, method, API, limitations, model and a five-line recipe. Differences from the sites: bulleted links rather than cards, no arrow-style call to action. I judge this a pass.
13. Narrative arc: honoured; "Next" lines, ends on the human step, then credit and the call to action (as in the references, which end on a link).
14. Honest mode flags: honoured.
15. No emojis, no hype: honoured.

Of points 1, 2, 12: **12 is honoured; 1 and 2 are improved and partly honoured.** I would not call point 1 failed, because a figure of real designs precedes the method; I would not call it met either.

## Observations (not counted as failures)

- Scope text expected 7 large-wheel near-frontier designs; the notebook reports 6 from its own output.
- The notebook was authored by a script kept outside the repository (scope default).
- First-pass items G-3, G-5, G-6, G-8, G-9 were not touched in this pass (checked: the corresponding text and tests are unchanged apart from the section 9 split).

## Open decisions (for the supervisor)

All wording-level or style-residual; none changes a good-enough item except G-12, which qualifies R-6.

- **G-12 (R-6, substantive qualification).** R-6 asks each three-metric surface to hug the upper envelope. Figure 03's second subset does so only over the lower and middle range; the text says the surface overstates the data at the upper end. Honestly reported, but the literal requirement is met for one subset and partly for the other — options: accept as is / fix before acceptance / follow-up work package — **pending**.
- **G-7r (style residual).** Point 1 (hook is data, not the embodied system or a puzzle) and point 2 (markdown median 703 against 295 characters in the reference; several cells over 1800) remain partly honoured — options: accept as is / fix before acceptance / follow-up work package — **pending**.
- **G-11, G-13, G-14 (wording-level, one item).** G-11: cell 23, before the report, states subset-fit exponents (slew time 0.45, control effort 0.51) and that "pointing error hardly binds"; these are fit outputs, not named tensions, but they sit before the report (related to G-8, accepted). G-13: hook-figure legend overlaps the last bars; figure 04 y-labels crowd at the left edge; medium-wheel orange and vermillion holes are close in figure 05. G-14: `145a5e4` deletes `01_attributes.png` while the notebook and `test_png_copies_exist` still named it until `755bf5e`, so that commit alone would fail the test (by inspection, not run); the two were pushed together and CI on `755bf5e` is green — options: accept as is / fix before acceptance / follow-up work package — **pending**.

## Gap dispositions

Previously dispositioned (supervisor, verbatim "Fix G-1, G-2, G-7, G-4, G-10; accept the rest", `WP7-decisions.md`, round 1):

| Gap | Disposition | Reason or follow-up |
|---|---|---|
| G-1 | fix before acceptance, done | verified in this pass (above) |
| G-2 | fix before acceptance, done | verified; qualification G-12 raised |
| G-7 | fix before acceptance, done in part | points 12 honoured; 1 and 2 improved; residual G-7r pending |
| G-4 | fix before acceptance, done | verified (above) |
| G-10 | fix before acceptance, done | verified; author's wording correct |
| G-3 | accept as is | out-of-scope script, test and predictions file; untouched |
| G-5 | accept as is | directions 3 and 4 unexplained; untouched |
| G-6 | accept as is | untouched |
| G-8 | accept as is | phrase-list guard; untouched |
| G-9 | accept as is | untouched |

New this pass:

| Gap | Disposition | Reason or follow-up |
|---|---|---|
| G-12 | pending | |
| G-7r | pending | |
| G-11, G-13, G-14 | pending | |

## Recommendation

Recommend acceptance with the listed gaps noted, once the supervisor gives G-12, G-7r and the wording item a disposition (none of them is a failed requirement; accepting all as is leaves the work good enough). Reasons: all five "fix" items are verified fixed independently; the notebook re-executes with a bad `OPENSYSML_BINARY`, reads only the four cached CSVs and reproduces every text output and all nine PNGs; the numbers recompute from the CSVs alone; the prediction record is unchanged in its values and its order in git is preserved; the suite (902 passed), ruff, lock, attribution, authorship and CI are clean; the trial shows the early-naming guard works. The remaining weaknesses are the second subset in figure 03 (disclosed), the residual style points 1 and 2 (judgment), and cosmetic items.

Acceptance is the supervisor's act, recorded as named above. This report does not accept the work.

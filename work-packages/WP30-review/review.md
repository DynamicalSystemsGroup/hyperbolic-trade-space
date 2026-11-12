# WP30 stage 6 review: the reviewer who ran the thing

Head 8806b0e, worktree `scratchpad/pm-worktrees/s6review` (branch `s6review`), 2026-11-12. Nothing was fixed. Site read at
http://127.0.0.1:8791/ (paper, supporting material, docs, Examples, choosing-K), light and dark, 1280 px and 375 px, in
headless Chrome through Playwright and in the browser pane (own tab, tab-80). Screenshots are the `.jpg` files beside this
file; names are `<page>-<figure or section>-<light|dark>-<desktop|mobile>.jpg`.

## Commands run

| Command | Result |
|---|---|
| `uv run pytest -q -m "slow or not slow"` | 2356 passed, 16 skipped, 2 xfailed, 0 failed, 27 warnings (sklearn ConvergenceWarning in `test_sklearn_compat`), 4129 s |
| `uv run ruff check .` | All checks passed |
| `uv run ruff format --check .` | 584 files already formatted |
| `uv lock --check` | Resolved 178 packages, no change |
| `uv run python paper/execute_notebooks.py` | both notebooks executed, 25 min, stderr empty (only my `time` line); `git status`: paper figures and `paper.ipynb` unchanged; `supporting_material.ipynb` differs in three lines, the Appendix F.2 "Commit" value (605d2603 committed, 8806b0e observed when the cell ran): the expected record of the checkout, reverted, not committed |
| `PYTHONPATH=examples/adcs uv run python -m experiments verify` | 74 entries (11 current); 0 drifts; current are `@12` (shared-subspace `@11`) |
| `uv run python scripts/check_vocabulary.py` | 0 new violations, 65 known |
| browser console, all four modes, paper | no errors or warnings; no horizontal scroll on paper, supporting material, docs home, Examples, choosing-K |
| rendered-text greps (paper, supporting material, docs) | see findings: no `eight metrics`, `K = 3` as a choice, `@10`/`@11`, `1,000 designs`, `CostToBuild`, `6,000 USD`, `90,643`, `no traded metric`, `Loading`; pointers read `@12` |

## Findings

severity | where | evidence | what it breaks

changes a view | paper, Figure 8 "Does not show" line (also `claims_register.toml:5753`, `paper/paper.ipynb:1737`) | rendered text and `paper-fig8-ternary-light-desktop.jpg`: "the other five metrics"; each triple leaves ten of the thirteen out | a stale count from eight metrics (eight minus three); a reader is told five metrics are left out, the figure leaves out ten
changes a view | supporting material, Appendix E rows G-2 and G-17 (source `docs/superpowers/notes/abstraction-gaps.md`, rendered into the paper) | `get_page_text`/DOM text: "Cubesat conditioning_ on the eight-metric data (M3): ... primary K = 3 ... terms led by energy balance, control effort and peak slew power ... five participants" and "nondominated counts (659 of 706 on eight attributes, 126 on the four-metric view) ... 74 of 685 quantities" | numbers of the eight-metric, 1,000-design data stand in the paper beside the thirteen-metric, 3,000-design record (2,134 feasible primary); the sensitivity record was re-run at 3,000 designs (95f6f5d, 684b5b7), the prose was not
cosmetic | docs Examples page, Figure 5 (`case.tension_figure`) | `docs-examples-fig5-crop-light-desktop.jpg`: thirteen metrics in a figure sized for fewer: x tick labels overprint each other, cells cramped, title "term 1: 7-lemma (7 metrics in the exact-maximum support" cut by the colour bar | the figure fails legibility on the page that teaches the method; the paper's Figure 7 (larger) reads
cosmetic | paper Figure 7 and docs Figure 5 | `paper-fig7-tensions-light-desktop.jpg`: term 2 row "total mass w=0.01" is black but not outlined; the caption says only that an outlined metric can be grey | a reader meets the converse case (above threshold, outside the contending set) unexplained; it is the exact-maximum support versus the fit temperature
cosmetic | paper Figure 7 at 375 px | `paper-fig7-tensions-dark-mobile.jpg`: heat map scaled to the screen, labels and values unreadable; the "enlarge" link is the reading route | none beyond the phone view
cosmetic | all paper matplotlib figures, dark mode | `paper-fig5-plane-dark-desktop.jpg`: white image panel on the dark page | known to the figure loop; not a WP30 change
cosmetic | paper Figure 3 | `paper-fig3-behavioural-light-desktop.jpg`: the label "totalMass" sits on the dashed arrow between total mass and launch cost | overprint of one edge label
cosmetic | paper Section 8 | rendered text: "Of the 13 traded metrics" beside "thirteen attributes", "thirteen metrics are traded" | digit and word for the same count in one section
cosmetic | `work-packages/WP30-gate-checklist.md`, brief | checklist says 1,250 designs per regime; `definitions.py` `SAMPLE_PER_REGIME = 3000`, paper says 3,000 (2,134 and 2,355 feasible) | a record disagrees with the model; the paper and the data agree
cosmetic | docs Examples page | no sentence of the 6,000,000 inside 8,000,000 USD relation; it is on the linked case page (`examples/adcs/case-model.md:221`, GitHub) and in the paper and Appendix C.8 | the decision (`WP30-decisions.md`) says the docs case page carries it, and it does; the Examples page itself does not
cosmetic | supporting material C.5 at 375 px | `sm-C5-dark-mobile.jpg`: the two data tables show six of thirteen columns, the rest by horizontal scroll inside the table | none (no page-level horizontal scroll)

No finding blocks.

## Verdicts, WP30 "Definition of good enough"

| Item | Verdict | Evidence |
|---|---|---|
| (3a) R-1, R-2, R-3: model, oracle, case, tests; one metric count; computed reasons | met | full suite green incl. slow; thirteen everywhere read (Figure 3 shows thirteen metrics, ten of them from the slew experiment; paper, Appendix C.5 "2,134 designs by 13 metrics"; docs Examples "Thirteen metrics") |
| (3b) R-4, R-5, R-7: cost model, supervisor's values, no placeholder | met | suite green; D.17 and C.8 print 350,000 USD per satellite and 6,000,000 USD per fleet, launch 7,000 USD/kg, 105,770 USD |
| Data gate R-6, R-8 to R-11 | met as far as run | ledger verify 0 drifts at `@12`; contract and data tests green; I did not recompute D-8 or the first-1,000-row equality (container branches); feasible counts now 2,134 and 2,355 of 3,000, not 706 and 780, because the sample is 3,000 |
| Cascade R-12 to R-15 | not met | R-13: two stale hits (findings 1 and 2); R-14: figures and pages looked at here, light and dark, two widths, screenshots in this folder, the two cold readers are not in this review; R-15: ruff, format, lock, pytest pass here; no Linux dispatch run by me; no attribution trailer or "generated by" in `git log` since 2026-11-09 (only the file name CLAUDE.md matches) |
| Coverage statement (6,000,000 inside 8,000,000 USD) | met | paper Section 8, Appendix C.8, D.17; `case-model.md`; not on the docs Examples page |
| K = 2 (Section 9, D.15) | met | paper "pick K = 2 on the primary regime and the stock regime"; docs Examples "read at K = 2"; choosing-K page: break at K = 2, stock bends with no break |
| Term order | met | K = 2 term 1 is the 8-lemma with share 0.74 (stock 0.75) in Section 9, Figure 7, D.3, docs Examples; metric order in Figure 7 and D.3 agree |
| Six requirements, four performance thresholds, D.17 wording | met | Section 8 and D.17: four thresholds (peak slew power, pointing error, control effort, launch cost / total mass 15.11 kg) and two limits |
| Thirteen metrics, two that do not participate | met | Section 8: power margin and battery peak power ratio, Spearman at least 0.97; Figure 4 white rows; Figure 7 contending sets of 8 and 7 |
| Pointers at `@12` | met | Appendix F rows `v2-primary@12`, `v2-baseline@12`; ledger verify |
| Figure numbering 1 to 8, cross-references | met | rendered paper holds Figures 1 to 8 once each, no gap; docs figures 1 to 6 run across pages |
| Stderr guard | met | no stderr on execute_notebooks; no console errors; no Traceback/Warning text on any rendered page |
| Plots say what captions say | met with the cosmetic notes | Figures 3 to 8 read against captions; the "five metrics" line of Figure 8 is the exception (finding 1) |
| Tables with consistent spelling | met | D.2, D.3, D.17 use the glossary names |
| No leftover count or stale conclusion in rendered text | not met | findings 1 and 2 (`eight-metric data`, `eight attributes`, `706`, `other five metrics`); every other pattern clean |

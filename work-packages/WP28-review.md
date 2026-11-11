# WP28 — Review report (D-6)

| | |
|---|---|
| **Package** | WP28, improvement by subtraction (step 5a) |
| **Scope of work** | `work-packages/WP28-scope-of-work.md` |
| **Scope approval verified** | `work-packages/WP28-decisions.md`, "Scope gate" (the driver, verbatim, under the mandate; commit d7a3fe3); the cut list's gate under OD6 (a): "Cut list" (1bd0ecc) |
| **Start** | `<start>` = 1277210 |
| **Head reviewed** | 9216154 (`origin/dev` at the staging step and at the full suite: "WP28: the two orphan figure files deleted") |
| **Date** | 2026-11-10 |
| **Reviewer** | fresh: neither an inventory reader, the triager nor a stream author; worktree `pm-worktrees/wp28review` (kept for R-13), with a detached `pm-worktrees/wp28review-start` at 1277210 for the word counts |
| **Supervisor (accepts)** | mzargham; the acceptance is the driver's under the mandate, recorded in `WP28-decisions.md` after this report |

The review's own scripts (not committed): `r1_enumerate.py` (R-1), `words.py` (R-5), `cdp_shot.py` (R-15
screenshots, headless Chrome with `prefers-color-scheme` emulated) in the session scratchpad's `wp28rev/`.

## Deliverables

| ID | Verdict | Evidence |
|---|---|---|
| D-1 | met | `WP28-inventory.md` (2461344, model labels d803daf): 122 unit rows plus the root page's two images; returns, briefs, templates, `units.tsv` committed in `WP28-inventory/` before the cut list (2461344 precedes 68d240f). R-1, R-2, R-3 below. |
| D-2 | met | `WP28-cut-list.md` (68d240f): X-1 to X-4 with form, "no longer did", "narrative loses", six checks each; "Kept, with reason" (15 rows); "For the supervisor" S-1 to S-10; "Stuck"; counts. Every one of the 29 units not "advances" is in exactly one of cut (4), kept (15), for the supervisor (10). |
| D-3 | met | No paper cut was approved (X-4 kept by the driver's decision 2; S-1 to S-10 held), so no notebook cut, no `[[cut]]` row and no regeneration was due. The cruft: `paper/figures/fig-chart-k3.png` and `fig-predict-check.png` deleted at 9216154 with the "nothing reads them" line. |
| D-4 | met | X-1 at 87b0f37, X-2 at af9ffea (docs stream), X-3 at 712a59f (the driver, decision 1); each net negative (R-5); C303 and C369 to C371 removed in the same commits (R-6); `scripts/build_site_figures.py` needed no change (it builds from the pages; `git grep chart-holes adcs-coordinates` outside `work-packages/`: no hit); the vocabulary tool exits 0 (R-9). |
| D-5 | pending | `WP28-retest.md` does not exist at 9216154; the returns are committed (334fb32, `WP28-retest/returns/`, 13 files) and the driver's key marks are in `driver-log.md` (bd9e191). The retest's key marks are with the driver; R-13 is filled when the PM resumes this review. |
| D-6 | met | This file and `WP28-review/` (16 screenshots). |
| D-7 | met (to this point) | `WP28-decisions.md`: "Scope gate" and "Cut list", verbatim; "Acceptance" follows this report. |

## Requirements

| ID | Verdict | Evidence |
|---|---|---|
| R-1 | met | The review's script enumerates from the sources (the paper's `## ` section cells, `prf:` blocks other than proofs, `{figure}`/`{table}` floats; the supporting material's `## Appendix X.` headings and `tab-` code cells; `mkdocs.yml`'s nav without `generated/` and `api-reference.md`; each page's `![` figures; the root page and its `<img>`s; the README) and diffs against the inventory's first column. At fbeede5 (the commit the readers read): "enumerated 124 {'section': 14, 'float': 10, 'statement': 27, 'appendix': 7, 'appendix-table': 40, 'docs-page': 14, 'docs-figure': 8, 'root': 1, 'root-image': 2, 'readme': 1} ... inventory first column rows: 124 unique: 124; in sources, not in inventory: []; in inventory, not in sources: []". At 9216154 the only difference is the two cut figures: "in inventory, not in sources: ['docsfig-adcs-coordinates', 'docsfig-chart-holes']". |
| R-2 | met | All 56 briefs grepped case-insensitive for `work-packages|review|triage|change request|round|wp[0-9]|persona|decision|supervisor|driver|PM|inventory|cut list|claims.register|answer key`: no file. Read in full: `sect-results.md`, `docsfig-chart-holes.md`, `appendix-d.md`: each names the unit, points to the story slice (abstract and Section 1; Home and root page for docs) and the questions, and forbids opening anything else. The story slices (still in the scratchpad) have no record word; the appendix D and E slices and the README slice carry `work-packages/` paths because the rendered pages print them (the process pointers the cut list keeps by design). The briefs carry the scratchpad's `claude-501` paths (R-16). |
| R-3 | met | The 20 figure and table returns (9 paper figures, `tab-families`, 8 docs figures, 2 root images) all open with Q5 (a) "what the image shows", then (b) after the caption, then (c) the sentence test, then Q1 onward; each brief's step 1 has the reader write (a) to the file before opening the caption. |
| R-4 | met | X-1 and X-2: the commit bodies carry the cut list's "What the content no longer did" line word for word (87b0f37: "It drew the hole finder's squares on a seeded sample that has no interior hole, so the squares trace the rim of the cloud; it showed no hole."; af9ffea: "It drew the 706 feasible designs on the first two of seven position coordinates, which its own caption calls meaningless alone, ..."). X-3 (712a59f) carries it in its subject ("it no longer described the method a second time nor called the unit level set the Pareto frontier"). Each row has six checks with outcomes; X-4, the one failing check (6), was not executed and was kept by the driver's decision 2. |
| R-5 | met | The executed units, `prose_words()` at 1277210 and at 9216154: `user-guide/chart.md` 597 → 561 (−36), `examples.md` 716 → 676 (−40), `README.md` 162 → 98 (−64, the 14-word pointer counted); no other docs page changed; docs total 6,954 → 6,814 with the README. No WP28 unit touched the paper; `words_by_section()` grew by 129 from units outside WP28's cuts (Out of scope). `git diff --stat 1277210..HEAD`: 168 files, +9197 −152 (the WP28 records, mostly). |
| R-6 | met, one exception named (G-2) | `uv run pytest tests/test_claims_register.py`: 21 passed. `git diff 1277210..HEAD -- claims_register.toml`: removed C303 (87b0f37), C369, C370, C371 (712a59f); none re-pointed; one row added, C421 (fbeede5, WP28 unit 0, the centring clause in Case construction, WP11's item (a), a narrowing the driver allowed before the inventory); no row added by a cut. |
| R-7 | met | `uv run pytest tests/test_interface_contract.py tests/test_site.py`: 136 passed. `contract_version = 16` at both ends; `git diff --stat 1277210..HEAD -- work-packages/interface-contract.*`: empty. |
| R-8 | not met (one part, G-1) | `uv run pytest tests/test_paper.py -k ledger`: 5 passed. No paper cut executed, so no `[[cut]]` row is due and the ledger part reads as not applicable. The ceilings under OD5 (a): `BUDGETS` lowered for the two pages cut (`chart.md` 600 → 561, `examples.md` 720 → 676), but `TOTAL_BUDGET` is still 7600 against the cut list's own "Budgets after" row ("`TOTAL_BUDGET` lowered to the pass's total", 6,716). |
| R-9 | met | `uv run python scripts/check_vocabulary.py --baseline scripts/vocabulary_baseline.toml`: exit 0, "0 new violation(s), 69 known", "once-used terms (0)". `uv run pytest tests/test_paper.py -k register`: 9 passed. No glossary entry removed (`git diff 1277210..HEAD -- glossary.yaml`: empty), as the cut list's check (5) predicted. |
| R-10 | met | `git diff 1277210..HEAD -- tests/`: `tests/test_site.py` three lines, each in a commit naming its row and the approval: the `chart.md` budget (87b0f37, X-1), the `"chart-holes"` member of `test_figures_are_few_captioned_and_in_both_colour_schemes` (87b0f37, "under R-10, the cut list approved ... row X-1"), the `examples.md` budget (af9ffea, X-2). No weakening beyond the cut: `MAX_FIGURES`, the four other required names and the `adcs-` requirement stand. `tests/test_paper.py` changed only in 4c9416c (WP11's maths check: a new test of R1 on the case, and `test_cr15_...` counting shared scripts from the proof record), not a WP28 cut (Out of scope). |
| R-11 | not applicable (re-execution); met (tests) | `paper/execute_notebooks.py` was not run (the brief's instruction): no paper unit of WP28 executed, and the paper edits in the range (fbeede5, dbb18e3) are Markdown cells; the supporting material's change came with WP11's 4c9416c. `uv run pytest tests/test_paper.py tests/test_paper_static_figures.py`: "149 passed, 4 skipped". |
| R-12 | met (for WP28's units) | Front matter cell 0, its metadata and the notebook metadata identical at 1277210 and at the head; the cells changed are `sec-methods`, `res-L3`, `res-L15`, `res-L17`, `sec-case-construction-1b` (WP11 and unit 0); C406's and C407's fragments sit in `sec-discussion`, unchanged; the proposals' sentence (`sec-search`) unchanged; `sect-future` unchanged. `git diff --stat 1277210..HEAD -- src derivation examples/adcs mkdocs.yml`: `derivation/lemma_15_descent.py` +73, `derivation/proof_map_record.json` +73, both from 4c9416c (WP11's maths-check unit, which OD1 (b) placed before the stage); `src/`, `examples/adcs/`, `mkdocs.yml`: no change. |
| R-13 | pending | Filled when the PM resumes this review with `WP28-retest.md`. |
| R-14 | met | `uv run pytest -q` on 9216154 in this worktree: "2203 passed, 16 skipped, 1 xfailed, 23 warnings in 1508.75s (0:25:08)", exit 0. Linux: CI run 42941495293 ("Tests", workflow_dispatch) on af9ffea, success; `driver-log.md` row "commit af9ffea, CI run on ubuntu, three shards ... fast, slow and docs-paper all green", the watcher green on dbb18e3 (2203 passed). The commits after af9ffea are records and the two PNG deletions. |
| R-15 | met | `uv run python scripts/stage_site.py` in the clean worktree at 9216154 (theme templates copied from the main checkout): exit 0; served on 127.0.0.1:8828. Every changed page looked at in the browser pane at 1440 px and captured light and dark (16 screenshots, readings below). |
| R-16 | met | `git log 1277210..HEAD --format=%B | grep -iwE "co-authored-by|generated (with|by)|claude|anthropic|sonnet|opus"`: 0 lines; the CI's own pattern (`\bco-authored-by\b|\bgenerated with\b|🤖`) on the range: 0. In the files: the only matches are `claude-501` scratchpad paths in the 56 inventory briefs and 14 retest briefs (`WP28-inventory/briefs/`, `WP28-retest/briefs/`) and the name "CLAUDE.md" (the repository's own file) on added lines of the cut list, `PM-BRIEF.md` and `driver-log.md`; no attribution. Vocabulary: R-9. |

## Definition of good enough

| Item | Verdict | Evidence |
|---|---|---|
| D-1: every unit has its row; returns verbatim and committed before the triage; briefs free of records; figures image first | met | R-1, R-2, R-3; 2461344 before 68d240f |
| D-2: every non-"advances" unit is a cut or kept; six checks per cut; "for the supervisor" lists what may not be cut | met | 29 = 4 + 15 + 10; R-4 |
| D-3 and D-4: every cut not for the supervisor executed or listed with its failing check; net negative; notebooks, register, contract, ledger, glossary, pinned tests; suite green | met except the total budget (G-1) | X-1, X-2, X-3 executed; X-4 listed with check (6) and kept by decision; R-5 to R-11, R-14 |
| D-5: the re-test | pending | R-13 |
| D-6: every changed page in the browser; R-12 and R-16 | met | R-15, R-12, R-16 |
| The counts | met | below |

## The counts

| | |
|---|---|
| Units inventoried | 122 (14 sections, 27 statements, 10 floats, 7 appendices, 40 appendix tables, 14 docs pages, 8 docs figures, the root page, the README), plus the root page's 2 images read inside `root-index`; 56 readers, two models |
| Verdicts by kind | advances 93, repeats 7, does not advance 21, split 1 (Definition 7), stuck 0 (readers); stuck by the record: 1 term, "energy differential", the supervisor's decision |
| Cuts by form | executed: goes 2 (X-1, X-2), pointer 1 (X-3), merged 0; not executed: X-4 (goes, check (6) failing, kept by the driver); for the supervisor: S-1 to S-10 (goes 7, pointer 3), none executed |
| Words removed, per section and page | paper sections: 0 (no paper cut); docs: `user-guide/chart.md` −36, `examples.md` −40; `README.md` −64; appendices 0 |
| Register rows | removed 4 (C303, C369, C370, C371); re-pointed 0; added 1 outside the cuts (C421, unit 0) |
| Glossary entries removed | 0 |
| Tests changed under R-10 | `tests/test_site.py` `BUDGETS["user-guide/chart.md"]` 600 → 561 (X-1, OD5 (a)); the `"chart-holes"` member of the required set (X-1, the cut list approved, 1bd0ecc); `BUDGETS["examples.md"]` 720 → 676 (X-2, OD5 (a)) |

## Outside the scope

- **Out-of-scope changes** (`git diff --stat 1277210..HEAD` lines no WP28 deliverable accounts for):
  - 4c9416c, WP11 round 2's maths-check unit (OD1 (b) put it before the stage): `derivation/lemma_15_descent.py`,
    `derivation/proof_map_record.json`, `paper/paper.ipynb` (`res-L3`, `res-L17`), `paper/supporting_material.ipynb`
    (Appendix B), `tests/test_paper.py` (one new test, one test reading the proof record), `paper/length_ledger.toml`
    (a Results raise of 42).
  - fbeede5, WP28 unit 0 (WP11's item (a), the centring clause in Case construction): `paper/paper.ipynb`
    (`sec-case-construction-1b`), a ledger raise of 47, register row C421. The driver allowed it before the inventory.
  - dbb18e3, the paper's held unit under WP11 round 2 (d), (e) by the driver's order: `sec-methods` (+15) and
    `res-L15` (+25), two ledger raises.
  - Records outside WP28's own files: `work-packages/PM-BRIEF.md` (da051a4, 1cee3cf), `work-packages/WP14-decisions.md`
    (393ad74), `work-packages/driver-log.md` (the driver's rows).
  - The three paper units raise the body by 129 words (9,805 → 9,934: Methods +15, Results +67, Case construction
    +47), each with its ledger row.
- **Non-goals touched:** none by a WP28 unit. `derivation/` changed in the range by WP11's unit (above), not by this
  package.

## Browser pass (R-15)

Staged at 9216154, served at 127.0.0.1:8828, read in the browser pane at 1440 px (light and dark by emulation);
the screenshots were captured headless at 1440 × 900 with the colour scheme emulated, scrolled to each changed place.

| Screenshot (light / dark) | Reading |
|---|---|
| `01-chart-figure4-{light,dark}.png` | Chart page: Figure 4 (the log plane) is the page's only figure now and is numbered 4 after Tensions' Figure 3; the grey band the caption names is thin and hard to see in both schemes (not changed by WP28). |
| `02-chart-holes-{light,dark}.png` | "Holes and white space": the block ends at `find_holes(...)`; no figure, no stray import, the "A hole is a candidate" paragraph follows directly; the "Plots" list still names `plot_frontier_coordinates`. The section's lead ("Plot the position coordinates ... gaps in that picture are candidates") now introduces a block that computes holes and shows nothing. |
| `03-examples-figure5-{light,dark}.png` | Examples, "The one-term fit, drawn": the lead reads "this block draws the one-term fit's tension report:", one block, then the heatmap (Figure 5); no trace of the coordinates figure. |
| `04-examples-figure6-{light,dark}.png` | The planted ternary captioned "Figure 6", drawing unchanged; docs figures run 1 to 6 across the site with no gap, and no prose cites a docs figure by number. |
| `05-docs-home-{light,dark}.png` | The docs Home, the README's pointer target (`docs/index.md`): the page says what the method does and "Where to start", as the pointer sentence promises. |
| `06-paper-s5-methods-{light,dark}.png` | Section 5: R1 stated "at the exact-maximum (τ = ∞) fit", then "R1's relation at the fit temperature is the hypothesis Theorem 2 states", Theorem 2 a live link; maths rendered (no KaTeX error on the page). |
| `07-paper-s62-theorem11-{light,dark}.png` | Section 6.2, Theorem 11: "stops within K^N + 1 iterations (Appendix B, L15.17 to L15.22); stationarity of the stop, and convergence otherwise, are not claimed", the reference a live link; sketch and script boxes follow. |
| `08-paper-s8-centring-{light,dark}.png` | Section 8: the centring sentence with f₁(w) = J_τ(Uw) − ū₁·w rendered inline, "equation (2)" and "equation (1)" named; "Section 12" a live link. |

No unresolved reference (`??`, raw `{ref}`/`{numref}`/`{prf:ref}`), no error or warning text and no maths error on
the paper page (checked in the pane over the whole page text).

## Observations (not counted as failures)

- **O-1.** The scope's sizing says "123 units"; its own list sums to 122 (14 + 27 + 10 + 7 + 40 + 14 + 8 + 1 + 1), which
  is what the inventory holds.
- **O-2.** The definition of good asks that "the ledger shows the paper shorter than it started"; no paper cut
  executed (X-4 kept; S-1 to S-10 with the supervisor) and the body is 129 words longer from the WP11 units, so the
  paper is not shorter at this head. Good enough does not require it.
- **O-3.** Chart page, "Holes and white space": after X-1 the block computes `holes, scores` and neither prints nor
  draws them; a reader following "Plot the position coordinates" meets no picture and no output. Not a dangling
  reference, a stumble.
- **O-4.** Chart page Figure 4: the near-frontier band is barely visible at the size shown (pre-existing).
- **O-5.** The browser pass covered desktop width only, as R-15 asks; `PM-BRIEF.md` "Reviews that pass through the
  browser are done in the browser" also asks 375 px, not run here.
- **O-6.** OD5 (a) read strictly lowers every docs budget to its count after the pass; the units lowered the two
  pages they cut (the cut list's reading), and the other twelve pages keep budgets above their counts.

## Open decisions (for the driver)

- **G-1.** `TOTAL_BUDGET` in `tests/test_site.py` is 7600; the cut list's "Budgets after" and OD5 (a) lower it to the
  pass's total (6,716) — options: accept as is / fix before acceptance / follow-up work package
- **G-2.** C421 added in the range (unit 0) against R-6's "no new row" — options: accept as is / fix before acceptance /
  follow-up work package
- **G-3.** The out-of-scope units (4c9416c, fbeede5, dbb18e3) and the records — options: accept as is / fix before
  acceptance / follow-up work package
- **G-4.** Observations O-1 to O-6, as one item — options: accept these as is / pick any to act on

## Gap dispositions

| Gap | Disposition | Reason or follow-up |
|---|---|---|
| G-1 to G-4 | pending (the driver's) | |

## Recommendation

Pending R-13: the recommendation is written when the re-test's record (`WP28-retest.md`) is read.

Acceptance is the driver's act under the mandate, recorded in `WP28-decisions.md`. This report does not accept the work.

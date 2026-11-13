# WP28 — Review report (D-6)

Screenshots for this record: commit `c680853`, `git show c680853:<path>` with `<path>` under `work-packages/WP28-review/`.

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

See "Second pass at 18c258c" below: the recommendation is written there, after R-13.

Acceptance is the driver's act under the mandate, recorded in `WP28-decisions.md`. This report does not accept the work.

## Second pass at 18c258c (2026-11-11)

**Head:** 18c258c (`origin/dev` when this pass ran). The last commit that touches anything outside `work-packages/`
is a2d25f9; the five after it (35668e5 to 18c258c) are WP29, WP30 and WP31 records only. **Landed since the first
pass (9216154):**
- WP28's own units: db8d8bd (G-1), afdb222 (O-3), the CR units CR-35 to CR-41 (b0d14a4, 4dee363, c12e5bc, 91369c2,
  e70585f, 6b858fc, 95d77b4), the supervisor's rulings (ac22112), S-3 (a74579c), S-10 (a2a0f14 Appendix D.12,
  5260d7f the docs termination page), the CR-37 loose ends (d6e0f1b) and the re-test record (052e8ee).
- Other packages' records (Track A, Track B and the figure loop) and the lint commit a2d25f9.

The fresh staged site was built in a new worktree, `pm-worktrees/wp28stage2`, detached at 18c258c, with the theme
templates copied from the main checkout; it was served on 127.0.0.1:8829 and read in a browser tab of the reviewer's
own (closed afterwards). The tests and the code ran in `pm-worktrees/wp28review`, fast-forwarded to 18c258c.

### Requirements, second pass

| ID | Verdict | Evidence |
|---|---|---|
| R-5 | not met on the letter (G-5) | **The cuts are net negative.** S-3 takes Case analysis 1,825 to 1,722 (−103) and Case construction 1,156 to 1,146 (−10); O-3 takes `chart.md` 561 to 557 (−4).<br>**The supervisor's S-10 adds words** at his word "keep and clarify": Appendix D's Markdown 1,130 to 1,283 (+153) and `user-guide/termination.md` 581 to 714 (+133).<br>**The CR units change Results and Case construction.** Results 2,429 to 2,467 (+38): CR-35 +6, CR-36 +7, CR-37 −1, CR-38 +26. Case construction 1,187 to 1,156 before S-3: CR-38 −38 (the comparison moved to 6.2), CR-39 +1, CR-41 +6. CR-40 takes The decision problem 714 to 712.<br>**Totals.** Paper body 9,805 at the start, 9,934 at af9ffea, 9,846 at the head. Docs total, README aside, 6,792 to 6,845. Measured per commit with `words_by_section()` and `prose_words()` over 15 commits (the review's `words_seq.py`). |
| R-6 | met, exceptions named (G-2) | `tests/test_claims_register.py`: 21 passed. **Rows removed since the start:** C303, C369, C370, C371. **Rows added**, each backing a sentence a recorded unit added, none for cut prose: C421 (unit 0), C422 (c12e5bc, CR-37), C423 to C425 (a2a0f14, S-10), C426 (d6e0f1b). No row names the cut Figure 9 (the implementer's grep; `git grep fig-regimes claims_register.toml` finds nothing). |
| R-7 | met | `tests/test_interface_contract.py tests/test_site.py`: 136 passed; `contract_version = 16`. |
| R-8 | met | **The two `[[cut]]` rows are S-3's:** Case analysis 103 and Case construction 10, each with date, section, `words_removed`, `no_longer_did` and `authority` ("the supervisor, S-3: 'Cut to a pointer'"). They equal R-5's deltas exactly.<br>**The ledger reader.** `ledger_ceilings()` subtracts cut rows: run, it gives the Case analysis ceiling 1,732 (count 1,722), Case construction 1,190 (count 1,146) and a total of 10,342 (count 9,846). `pytest -k "ledger or ceiling"`: 5 passed.<br>**The docs budgets.** `TOTAL_BUDGET` is 6845, the count after the pass (db8d8bd; G-1 closed). `chart.md` is 557 and `termination.md` 714, at S-10's count. |
| R-9 | met | `check_vocabulary.py --baseline`: "0 new violation(s), 69 known", exit 0; `pytest -k register`: 9 passed; `glossary.yaml` unchanged. |
| R-10 | met | **The five tests a74579c changed** each cite "Cut to a pointer (S-3, R-10, WP28-decisions.md)" in a comment beside the change, and the commit subject names S-3 and "the supervisor's word":<br>- `test_cells_whose_output_is_embedded_...`, from at least 4 to at least 3<br>- `test_every_figure_and_table_is_referenced_from_the_text`, 10 to 9<br>- `test_every_figure_shows_its_smallest_text_...`, 3 to 2<br>- `test_cr1_...`, which loses `fig-regimes-caption` from the tuple<br>- `test_regime_names_...`, which loses its `fig-regimes` exemption<br>Each count drops by exactly the one figure, and removing the exemption makes that check stricter.<br>**`test_each_ledger_row_...`** gains the cut-row field checks.<br>**Other changes since the first pass are additions or tightenings:** 6b858fc ("659 on all 8"), a2a0f14 (the D.12 test), d6e0f1b (the Section 8 centring test), and in `test_site.py` the three budgets (db8d8bd, afdb222, 5260d7f). |
| R-11 | met | **The host run.** `paper/execute_notebooks.py` ran on the host after S-3, the one unit that removed code cells. It re-recorded only Appendix F.4: the `fig-regimes` row left (`WP28-decisions.md`, "Close units", U1). The later paper units (a2a0f14, d6e0f1b) are Markdown cells.<br>**The tests.** `pytest tests/test_paper.py tests/test_paper_static_figures.py`: "151 passed, 4 skipped". The D.12 test alone (`-k d12`): 1 passed. |
| R-12 | met (for WP28's units) | **Unchanged:** the front matter (cell 0), `sec-discussion` (C406, C407), `sec-search` (the proposals' sentence) and `sec-future`.<br>**Under the protected paths** (`src`, `derivation`, `examples/adcs`, `mkdocs.yml`), the only change is still 4c9416c's `derivation/` (WP11).<br>**Cells removed:** `fig-regimes`, `fig-regimes-caption` and `fig-regimes-lines` (S-3, the supervisor's word). |
| R-13 | not met as written (G-6) | `WP28-retest.md` (052e8ee), "R-13, condition by condition":<br>**(1) No wrong belief: met.** "no W1-W8 belief in any of the twelve cells". The one statement wrong against the key (S5, four sentences in three cells) traces to Theorem 11's box wording, now changed by CR-35.<br>**(2) Every main result at depth B: not met.** S8's second item is missing in five of six B cells, and all of S8 in P4-B and P5-B. The record traces this to S8's absence from the main-results list, not to a cut.<br>**(3) No new "why" at depth C: not met on the letter.** The new "why"s come from the maths check's three sentences, two round-2 CR sentences and unchanged passages; the record names none from a cut.<br>**(4) No friction naming a cut or a pointer: met.**<br>**The re-test predates S-3.** It read af9ffea, before S-3 (the paper's one cut) and before CR-35 to CR-41. No fresh reader has read Section 9 since Figure 9 went to its pointer. |
| R-14 | met | **Fast suite at 18c258c:** `uv run pytest -q -m "not slow"` gave "1750 passed, 16 skipped, 455 deselected, 1 xfailed, 6 warnings in 230.15s", exit 0.<br>**Full suite:** 2203 passed at 9216154 (first pass).<br>**Linux CI:** run 42954612918 at a2a0f14 succeeded; run 42957819945 at 18c258c was in progress when this pass ran. |
| R-15 | met | `scripts/stage_site.py` at 18c258c exited 0 in the fresh worktree. 16 screenshots (8 places, light and dark at 1440 px), listed below. |
| R-16 | met | **The whole-word pattern** over `1277210..18c258c` matches one subject only: 2a65d6e, "... (PM-BRIEF, CLAUDE.md)", the repository's file name, not attribution.<br>**The CI's pattern:** 0.<br>**Vocabulary:** R-9. |

### Running the code

- **The docs `conditioning_` block** (`docs/user-guide/termination.md`, 5260d7f), run as written, prints
  `[19.52364466]` for the planted table and `[2.27276623e-06]` for the copy whose second metric nearly repeats the
  first, at temperature 20. Both numbers hold.
  - The second number depends on `min_exponent=0.1`, which the block passes and the prose does not explain.
  - With the default `min_exponent`, the near-duplicate table gives 12.40, not 2.27e-06: the fit drops the duplicate
    and the value stays near the first.
  - The implementer's record for D.12 says the same ("a near-duplicate metric does not lower `conditioning_` ... the
    fit gives the duplicate a zero exponent"). The page's sentence "two metrics that move together in log space cause
    it" is true only when both take part in the fit (O-7).
- **The D.12 snippet** `HyperbolicTradeSpace(temperature=50.0).fit(M).conditioning_` on a strictly positive planted
  table (`make_frontier_data(300, 4, random_state=1)`) returns `[36.44227204]`, one positive value as the test checks.
- **The Chart page's holes block** (afdb222) prints `168 [8.63 8.36 7.89]`, and the scores come out in descending
  order, as the new lead sentence ("most isolated first") says. O-3 is closed.
- **The cut-ledger reader:** R-8 above.

### Does Appendix D.4 carry what Figure 9 carried?

The S-3 implementer's account is confirmed on the rendered page.
- **What D.4 holds** (`tab-D-regime_comparison`): per regime, tau, `frac_above_` and `n_eff_`; the band and the
  near-frontier count; `n_lemma`; both contending sets by name; three pair associations (settling time with total
  mass, pointing error with control effort, settling time with pointing error); and the strongest-pair sentence.
- **What it lacks:** the two 8 × 8 association matrices and each metric's K = 1 exponent that Figure 9 drew. The
  feasible-design associations are in C.5's table; the exponents are in D.3's.
- **What Section 9 relies on is in D.4 or D.3.** The prose and its generated sentence use the two sets, the three
  shared metrics, the one-axis pair and the "mass enters only in the primary regime" reading. The all-pairs picture
  is what the pointer gives up, as the cut list said.
- **A stumble a reader would meet:** Section 9's generated sentence gives the strongest pair as "Spearman +0.98 and
  +0.99 ... Appendix D.3". D.4 prints +0.982 and +0.988 and says no pair reaches 0.99, the one-axis threshold, so the
  rounded "+0.99" reads as crossing it. This is not new: the retest lists "The 0.99 pair" as friction in 7 cells,
  as in round 2 (O-8).

### Browser pass, second (R-15)

| Screenshot (light / dark), under `work-packages/WP28-review/` | Reading |
|---|---|
| `r2-09-paper-s9-two-regimes-{light,dark}.png` | **Section 9, "Two regimes."** The paragraph points to Appendix D.4 (a live link), and the generated sentence follows with the 5-lemma comparison. No "Figure 9" anywhere on the page: the page text has 0 matches. Figures run 1 to 8 with Table 1, and no `??`, raw role or KaTeX error appears on the page. |
| `r2-10-sm-d4-{light,dark}.png` | **D.4 "The regimes side by side."** The table renders with both contending sets and the three pairs (values with bracketed second figures), followed by the strongest-pair sentence. |
| `r2-11-sm-d12-{light,dark}.png` | **D.12** renders as an opening paragraph and the three labelled paragraphs *Why it matters*, *How it is computed* and *Inspecting your own problem*. The Theorem 3 link resolves across the pages and the code font is right. The K = 1 rows printed below match the text (7.1 primary, 0.017 stock). |
| `r2-12-docs-termination-conditioning-{light,dark}.png` | **Termination page, `conditioning_`.** The new paragraph and the runnable block render, and the conditioning link works. `min_exponent=0.1` shows in the code with no word on it in the prose (O-7). |
| `r2-13-docs-chart-holes-{light,dark}.png` | **Chart page, holes.** The new lead sentence reads "Holes of a three-metric fit, most isolated first:" and the block ends with the `print`. |
| `r2-14-paper-s62-theorem11-{light,dark}.png` | **Theorem 11 after CR-35 and CR-36.** The hypotheses say the refit is by f_k ("its support over all rows less its cell's mean"); the statement says "unique term minimizers, which Theorem 3 does not supply". The K^N + 1 count left the box (it is in L15). |
| `r2-15-paper-s62-equations-{light,dark}.png` | **Section 6.2, after equation (2) (CR-38).** "On centred log-metrics, as the case's conditioning makes them, f₁ = J_τ and equation (2) at K = 1 is equation (1); otherwise they differ by ū₁·w." The maths renders. |
| `r2-16-paper-s8-centring-fig4-{light,dark}.png` | **Section 8.** The centring sentence is now one sentence, "This conditioning centres each log-metric (the standard scaler)."; Figure 4 follows. The caption no longer names a second panel of Figure 9 (the test passes, and the source contains no "Figure 9"). |

### Definition of good enough, second pass

| Item | Verdict | Evidence |
|---|---|---|
| D-3 and D-4: every cut executed or listed; net negative; ledger, register and tests; suite green | met except R-5's letter (G-5) | The approved cuts and the supervisor's cut (S-3) are executed. Nothing on the cut list is left unexecuted without a decision: X-4 was kept by the driver; S-1, S-2 and S-4 to S-10 were ruled keep. R-6 to R-11 and R-14 above. |
| D-5: re-test at a named commit after the last unit | not met (G-6) | The re-test read af9ffea; S-3 and CR-35 to CR-41 landed after it. |
| The counts | met | below |

**Counts, updated:**
- **Cuts executed:** goes 2 (X-1, X-2); pointer 2 (X-3, S-3); merged 0.
- **Cut rows in the ledger:** 2, both S-3's (113 words).
- **Words removed by cuts:** Case analysis −103, Case construction −10, `chart.md` −36 then −4, `examples.md` −40,
  README −64.
- **Words added by the supervisor's S-10:** Appendix D +153, `termination.md` +133.
- **Register rows:** 4 removed (C303, C369 to C371), 0 re-pointed, 6 added (C421 to C426; C421 by unit 0, the rest
  by the CR and S-10 units).
- **Glossary entries removed:** 0.
- **Tests changed under R-10:** the five of a74579c, the ledger row test, and the four `test_site.py` budget lines.

### Gaps, updated

- **G-1** closed by db8d8bd: `TOTAL_BUDGET` 6845, the measured count.
- **G-2** C421 to C426: rows added for sentences that recorded units added; none for cut prose. Options: accept as
  is / fix before acceptance / follow-up work package.
- **G-5** R-5's "every executed unit is net negative; no section, page or appendix grows" does not hold on its
  letter. Appendix D grows +153 and `termination.md` +133, at the supervisor's word on S-10 ("keep and clarify why
  it matters"). Results grows +38 from the WP28 CR units of the re-test. Each has a ledger raise row or a budget
  line. Options: accept as is / fix before acceptance / follow-up work package.
- **G-6** R-13 and D-5. The re-test's own record finds conditions 2 and 3 not met on their letter, and traces neither
  to a cut. The re-test also predates S-3, the only paper cut, so no fresh reader has read Section 9 with its
  pointer in place of Figure 9. Options: accept as is (the record traces nothing to a cut, and D.4 holds what
  Section 9 relies on) / fix before acceptance (a narrow confirm read of Section 9 and D.4 at the head) / follow-up
  work package (S8's placement in the main-results list, which the record leaves to the driver).
- **G-3** (the out-of-scope units) and **G-4** (the observations, now O-1, O-2, O-4 to O-8, as one item) stand.
  - O-3 closed by afdb222.
  - O-6: the twelve other page budgets stay above their counts.
  - **O-7.** The docs `conditioning_` block's near-duplicate demonstration relies on `min_exponent=0.1`, unexplained
    on the page; at the default the duplicate is dropped and the value is 12.40.
  - **O-8.** Section 9's "+0.99" against D.4's 0.99 threshold (pre-existing friction).

### Recommendation

**Recommend acceptance with the listed gaps noted**, because:
- every cut the cut list and the supervisor approved has executed, each net negative with its "no longer did" line,
  its register rows and its ledger or budget row;
- the contract, register, ledger, vocabulary and pinned tests hold, and the fast suite is green at 18c258c (full
  suite green at 9216154; Linux green at a2a0f14);
- the changed pages render correctly in both schemes;
- the re-test found no wrong belief and no friction that names a cut or a pointer.

The deciding open item is G-6. The paper's one cut (S-3) has not been read by a fresh reader. D.4 carries the sets
and pair tensions Section 9 relies on, but not the full matrices Figure 9 drew. If the driver wants R-13's letter
met for that cut, a narrow confirm read of Section 9 and D.4 at the head is the fix before acceptance. G-5's growth
is the supervisor's own S-10 addition and the re-test's CR units, each recorded.

Acceptance is the driver's act under the mandate, recorded in `WP28-decisions.md`. This report does not accept the
work.

# WP28 D-2 — The cut list

| | |
|---|---|
| **Date** | 2026-11-10 |
| **Inputs** | the inventory `WP28-inventory.md` (commit 2461344; 122 units read at fbeede5) with the returns in `WP28-inventory/returns/`; the records named in the scope (WP11 round 2 and its docs loop, WP19's round 2 and "The band in the planes", `WP19-slots.md` "Fixed by the supervisor", `WP23-review.md` "Pending with the supervisor", the `WPn-decisions.md` files) |
| **Checked against** | `dev` at d803daf; nothing under `paper/`, `docs/`, `site/`, `README.md`, `claims_register.toml`, `glossary.yaml`, `tests/` or `scripts/` changed between fbeede5 and d803daf |
| **Gate** | OD6 (a): the driver approves this list before any cut lands; a test named in check (6) changes under R-10 citing that approval |

**How the checks were run.** Words: `words_by_section()` and `rendered_words()` of `tests/test_paper.py` for the
paper and the supporting material (the appendices have no ledger row, so their words are `rendered_words()` of the
cells that go), `prose_words()` of `tests/test_site.py` for the docs pages and the README, each on a scratch copy
with the cut applied. Register: every `[[claim]]` fragment matched against the text that goes. Glossary: every cut
applied to a scratch copy of the corpus and `scripts/check_vocabulary.py --root <copy> --baseline
scripts/vocabulary_baseline.toml` run on it (dead entries, new violations, stale baseline rows). Tests and pins:
`git grep` of each cell id, label, file name and distinctive phrase over `tests/`, `scripts/`, `paper/*.py`,
`paper/*.toml`, `work-packages/interface-contract.toml` and `claims_register.toml`. Decisions: `git grep` of the
`WPn-decisions.md` files for each unit's subject.

**The process pointers.** The published pages name process records (`work-packages/` paths in Appendices A, D, E
and G, Section 13 and the README). The process is part of the paper by the supervisor's design; no row below cuts
one. The README row keeps its status line and its layout, which carry them.

## The cuts

Three rows execute on approval; one is a cut with a failing check, not executed until the check is resolved.

### X-1. `docsfig-chart-holes` (User guide: The chart, Figure 5): goes

- **Form.** Goes: the `<figure>` element (both images and the caption) and the two plotting lines of the block above
  it (the import of `plot_frontier_coordinates` and its call), so the block shows `find_holes` and draws nothing
  unseen. The lead "Holes of a three-metric fit:", the block's fit and `find_holes` call, and the prose on holes
  after the figure stay.
- **What the content no longer did.** It drew the hole finder's squares on a seeded sample that has no interior
  hole, so the squares trace the rim of the cloud; it showed no hole.
- **What the narrative loses.** A picture of `find_holes`' output on a sample where it finds nothing inside. The
  Home page's "where the table has gaps" is carried by the page's prose on holes and the `find_holes` call, as now.
- **Record.** The reader's verdict (does not advance; "the one sentence in Q5 (c) carries all of it") and the
  record agree: `WP8a-figure-review.md` row 5, "Partly", the rim reading; its rework was withdrawn with the other
  verdicts (`WP8a-decisions.md`, 2026-11-09), not decided. Not a figure the supervisor fixed. The page's reader
  (`docs-user-guide-chart`, advances) credits the page's holes section, not the figure.
- **Checks.**
  1. Register: C303 (its caption) is removed with it. No row re-pointed.
  2. Contract: no pin. `chart.md` is a pinned page and stays; no figure is pinned (`case.figures` holds none).
  3. Sentence test: fails, which is why it goes. The reader's sentence: "find_holes marks grid positions far from
     every design as orange squares; on this seeded sample none fall inside the cloud, so they only trace its rim."
  4. Ceiling: `chart.md` 597 to 561 words (−36) against its budget of 600; OD5 (a) lowers the budget to the count
     after the pass. No paper ledger row.
  5. Glossary: no entry made dead ("hole", "white space" and the chart's terms stay in use on the page).
  6. Tests: `tests/test_site.py::test_figures_are_few_captioned_and_in_both_colour_schemes` pins `"chart-holes"` in
     its required set (WP8a D1, commit 069e9cc); the name leaves the set under R-10 citing this list's approval. The
     same test's `MAX_FIGURES` bound and "an example from the case" (an `adcs-` figure) still hold.
     `tests/test_docs.py` requires `plot_frontier_coordinates` to be named in the guide: `chart.md`'s "Plots" list
     still names it.
- **Knock-on.** The docs figures after it renumber in their captions: Examples' Figures 6, 7 and 8 become 5, 6
  and 7 (with X-2: Figure 6 becomes 5 and Figure 8 becomes 6). No prose cites a docs figure by number. The generated images are git-ignored and
  `scripts/build_figures.py` builds from the pages, so no script entry goes.

### X-2. `docsfig-adcs-coordinates` (Examples, Figure 7): goes

- **Form.** Goes: the runnable block that draws it and the `<figure>` element. The lead sentence's clause naming it
  goes with it; the lead becomes "`examples/adcs/case.py` runs the study from the committed table; this block draws
  the one-term fit's tension report:" (the existing words, the clause removed).
- **What the content no longer did.** It drew the 706 feasible designs on the first two of seven position
  coordinates, which its own caption calls meaningless alone, with the nearest designs ringed; its caption says it
  shows coverage, not the frontier.
- **What the narrative loses.** That `plot_frontier_coordinates` runs on the case's chart. Where a design sits
  relative to the surface is carried by the Chart page and its log-plane figure; where the table has gaps by the
  Chart page's holes section.
- **Record.** The reader's verdict (does not advance) and the record agree: the supervisor on this figure
  (`WP8a-decisions.md`, 2026-11-09): "this one feels a bit hard to read. it doesn't really seem to reveal the
  frontier clearly, but maybe that's not the point"; the driver's reading given to him: "As drawn it probably does
  not earn its place"; the proposed replacement was withdrawn with the other verdicts, not decided. Not a figure he
  fixed. **Readers disagree:** the page's reader (`docs-examples`, advances) credits Figure 7 with
  "position of designs relative to the surface"; the caption says it does not show the frontier, and the figure's
  reader could not place what it shows. Decided for the figure's reader: a figure whose caption disowns the reading
  the page reader gives it does not carry that reading.
- **Checks.**
  1. Register: no row names its caption or the clause. None re-pointed.
  2. Contract: no pin (`examples.md` stays; `plot_frontier_coordinates` stays in the API list).
  3. Sentence test: fails. What remains after the caption's disclaimers is "the plotting call runs", which the
     code block says.
  4. Ceiling: `examples.md` 716 to 676 words (−40) against its budget of 720; OD5 (a) lowers it.
  5. Glossary: no entry made dead.
  6. Tests: no pin on the name. `test_figures_are_few_captioned_and_in_both_colour_schemes` requires an `adcs-`
     figure: `adcs-tensions` remains (see S-4: the two cannot both go without that test's requirement changing).
- **Knock-on.** Figure 8 (the planted ternary) becomes Figure 7 in its caption (6 with X-1). Its drawing is
  unchanged (OD4 b holds: the supervisor's "stays as drawn" is about the drawing).

### X-3. `readme` (the repository's README): its description shortened to a pointer to the docs Home page

- **Form.** Shortened to a pointer. The paragraph "Learn the shape of a design trade space. ... and an ADCS
  trade-study case." is replaced by the pointer sentence, in full:

  > The docsite's [Home page](docs/index.md) says what the method does and where to start.

  The title line, the status line, the quickstart and the layout stay (the status line and the layout carry the
  process pointers).
- **What the content no longer did.** It described the method a second time, in older words than the Home page:
  "a monomial, later posynomial, frontier ... whose unit level set is the Pareto frontier", which Definition 1,
  main result 1 and the abstract deny (the surface "is not the Pareto boundary"); "later posynomial" when K > 1 is
  built; "noisy, biased observations" with nothing on what the method does about either (the reader's Q9).
- **What the narrative loses.** Nothing the Home page does not carry (the reader: "Home's first paragraph and the
  root page's opening sentence already say" it). A visitor on the repository's page loses a one-paragraph summary
  and gets a link to it.
- **Record.** Written in WP0 (4281350); no decision record names it. The reader's verdict (repeats) and the record
  (its sentence contradicts the paper's main claim) agree.
- **Checks.**
  1. Register: C369, C370 and C371 (the three fragments of that paragraph) are removed with it. None re-pointed.
  2. Contract: no pin on the text. `README.md` sits under `[ownership.technical]` in `interface-contract.toml`;
     the scope's blast radius gives it to the docs stream for this package. Flagged, not failing: the PM confirms
     the stream may edit it.
  3. Sentence test: not a figure.
  4. Ceiling: no budget (the README is not in `BUDGETS`); `prose_words` 162 to 98 (−64, the pointer's 14 counted
     against it).
  5. Glossary: no entry made dead (the README is in the vocabulary corpus; checked on the copy).
  6. Tests: none pins the paragraph (`tests/test_paper_sources.py` reads the paper-sources README, not this one).

### X-4. `tab-D-refits_by_category` (Appendix D.6, Refits by category): goes — **check (6) fails; not executed until resolved**

- **Form.** Goes: the heading cell `app-D-refit` and the table cell; the phrase "the refits by category," leaves
  Appendix D's job list (the reader named the table). The generator `refits_by_category` stays: `paper/paper_perturb.py`
  reads it by name and is not the paper stream's file.
- **What the content no longer did.** It refitted the one-term fit within each wheel class, per regime: a table no
  sentence of the main text points to and that the depth-D reader would not look for ("nothing in the story or the
  pointers asks what the fit returns per wheel class").
- **What the narrative loses.** Nothing a pointer names. The per-class contending sets (six metrics each) are not
  cited anywhere else.
- **Record.** Added by WP10 (a62708a) among the Appendix D extensions; no decision names it. OD2 (b): not pointed
  to, and the reader says no depth-D reader would look for it: both conditions met.
- **Checks.**
  1. Register: no row. 2. Contract: no pin. 3. Not a figure. 4. Appendix D has no ledger ceiling; `rendered_words`
     −8 (heading 4, job phrase 4); a `[[cut]]` row with section "Appendix D". 5. Glossary: no entry made dead.
  6. **Fails.** `tests/test_paper.py::test_c_has_the_metric_table_and_the_sources_and_d_has_the_extended_tables`
     pins `tab-D-refits_by_category` and requires D's headings numbered 1, 2, ... without a gap, so D.7 to D.17
     renumber to D.6 to D.16. That touches about thirty visible link texts in the body and its generated sentences,
     the four link constants `_D8`, `_D11`, `_D14`, `_D15` of `paper/generate_findings.py` (outside the paper
     stream's blast radius: `paper/generate_*.py` only to remove a generator), the pin
     "{ref}\`Appendix D.7 <sub-d-7>\`" at `tests/test_paper.py:1541`, the register fragment at
     `claims_register.toml:869` ("Appendix D.16"), and every record and review that cites a D number.
     `test_the_c_and_d_additions_are_current_and_cite_the_labels` also names the cell. Appendix F.4 regenerates.
- **What would resolve it.** One of: the driver amends the paper stream's blast radius to the four link constants of
  `generate_findings.py` and accepts the renumbering (records keep their old numbers as history); or the table
  stays and this row moves to "kept".

## Kept, with reason

Every unit whose verdict was not "advances" and that is neither a cut nor for the supervisor.

| Unit | Verdict | Kept because |
|---|---|---|
| `tab-families` (Table 1) | repeats | It carries three families no paragraph of Section 2 carries (MDAO, decision analysis, MBSE); the MDAO row is how the supervisor's request ("the MDAO literature ... needs to be included", `WP10-decisions.md`, 2026-11-09, 22:05) reached the body; the depth-C sceptic of round 2 went to it (P6-B: "I want to see whether the prior-art table knows multiplicative DEA ..."). The reader's "repeats" holds for eight rows, not the table. |
| `def-reach` (the term share) | split: share does not advance | The term share is printed in the body: Section 9's generated sentence "The term shares are 0.03, 0.24 and 0.72" (`num-terms-k3`) and the D.2 and D.8 tables. **Readers disagree:** Section 4's reader judged it against the story alone; Section 9 uses it. The definition stays. |
| `def-ascent` | does not advance | Section 7 (the search, story item 6) runs on it: "on each term the normal is an ascent direction in log space" and "drift along the tangent spaces"; the supervisor's own direction ("computing ascent directions in the configuration space", `WP10-decisions.md`, 2026-11-08). |
| `thm-lme` (L5) | does not advance | Cited by `{prf:ref}` from Section 5 ("the log-mean-exp, never the unnormalized log-sum-exp", the convention CLAUDE.md fixes) and from Theorem 8's sketch (`thm-extension`, story item 3). Removing it breaks two references the story's units make. |
| `thm-pullback` (L9) | does not advance | Cited by `{prf:ref}` twice in Section 5 ("the pull-back to attribute units is exact"; "(v) Log-affine conditioning ... exactly invertible"), and Section 2 names the pull-back as a difference from DEA. |
| `sect-reproducibility` | repeats | It is itself the pointer (75 words): round 2's CR-28 put it there because three depth-C readers "could not start from the text" and the paper "points at nothing named"; register rows C124, C125. Cutting it reopens that friction. |
| `tab-C-metric_table` | does not advance | OD2 (b) needs both "not pointed to" and "no depth-D reader would look": the reader would look "partly" (the formula and the shape of the table). |
| `tab-C-metric_associations` | repeats (conditional, "from the pointer") | The reader would look for it (the strongest pair, the 0.99 test); the reader had not read D.3 and says the 28-pair listing "may be its only full home". It is: D.4 prints only the strongest pair per regime and D.3 prints exponents, not associations. |
| `tab-D-temperature_selection` (D.1) | repeats (conditional on Figure 4) | The reader would look for it. **Readers disagree:** the D reader's "repeats, if Figure 4 draws the same sweep"; Figure 4's reader says advances. Figure 4 draws the curves, D.1 prints the values the rule selects on (round 2: "why 0.1" in ten cells, resolved at depth C by the appendix's evidence). Decided: kept. |
| `tab-D-regime_comparison` (D.4) | repeats | The reader would look for it; it is the only full home of the two regimes' pair tensions, and the fallback home of the regime comparison if S-3 lands. |
| `tab-D-candidate_designs` (D.7) | does not advance | Pointed to by Section 9 ("Appendix D.7"): OD2 (b) keeps a table the main text points to. |
| `tab-D-propose_predict_check` (D.10) | does not advance | Pointed to by Section 9 ("Appendix D.10"). |
| `tab-D-requirements_at_the_frontier` (D.17) | does not advance | Pointed to by Sections 8 and 10; it backs C406, which waits for the supervisor (non-goal). |
| `tab-D-design_sets_comparison` (D.17) | does not advance | Pointed to by Sections 8 and 10; it backs C407, which waits for the supervisor (non-goal). |
| `tab-G-reading_pass_table` (G.2) | does not advance | A depth-D reader who doubts a citation looks for it (the reader's own words), so OD2 (b)'s second condition fails; it is the outcome WP10's C-3 recorded ("The outcome is a table in Appendix G"), and it lists the sentence on the author's INCOSE paper for him. It is a verification record, part of the paper's process by design. |

## For the supervisor

Cuts this package may not make. Each row gives the reader's verdict, why it is his, and the checks as they would
run, so that his yes or no can be executed without another triage.

| Row | Unit | Verdict | Why it is his | Form if he cuts it | Words | Checks that would bite |
|---|---|---|---|---|---|---|
| S-1 | `fig-assembly-view` (Figure 2) | does not advance ("the six design variables are already named in Section 8's first paragraph") | OD4 (b): one of the two model views he directed (`WP22-decisions.md`) | goes: cell `fig-assembly-caption`, `paper/figures/fig-assembly-view.png`, its `MODEL_VIEWS` entry in `scripts/build_figures.py`, the clause "(Figure 2)" in `sec-case-construction` | Case construction −145 | register: none; contract: none; tests: `tests/test_paper_static_figures.py::test_model_views_in_the_paper_equal_the_models_views`, Appendix F.4 regenerates; glossary: none dead |
| S-2 | `fig-behavioural-view` (Figure 3) | does not advance ("the text of Section 8 already gives both in one sentence") | OD4 (b): the second model view; his directions on it (`WP22-decisions.md`, 2026-11-09) | goes: cell `fig-behavioural-caption`, the image, its `MODEL_VIEWS` entry, and the two sentences of `sec-case-construction-1` that describe the view ("Figure 3 traces ... MoPs.") | Case construction −240 | as S-1; glossary: none dead |
| S-3 | `fig-regimes` (Figure 9) | does not advance ("No sentence of the abstract or Section 1 needs the comparison") | OD4 (b): one of "Paper Figures 5 and 6 (tension heatmaps, the drawing he liked)" (`WP19-decisions.md`, principle check, 2026-11-09, 21:20; Figure 6 then was the two regimes) | shortened to a pointer: the code cell, caption and lines go; in `sec-case-analysis-3b` "(Figure 9)" is re-pointed to "({ref}\`Appendix D.4 <sub-d-4>\`)"; the gloss "; the stock regime is the second panel of Figure 9" leaves Figure 4's caption | Case analysis −103, Case construction −11 | register: none; tests: `tests/test_paper.py` lines 2227 and 2302 name the caption cell; F.4 regenerates; glossary: none dead. **Readers disagree:** round 2 called it "probably the most decision-relevant picture in the set" (P1-B) and "precisely the 'why did the answer change' story" (P2-B); the inventory's figure reader and Section 9's reader ("no story sentence asks for a regime comparison") say it does not advance |
| S-4 | `docsfig-adcs-tensions` (Examples, Figure 6) | repeats `docsfig-tension-report` | OD4 (b): "i like the tension heatmap. you can resize it but don't rework it" (`WP8a-decisions.md`; it is docs Figure 6) | goes with its block | `examples.md` −31 | `test_figures_are_few_captioned_and_in_both_colour_schemes` requires an `adcs-` figure: with X-2 executed, this cut fails that requirement ("an example from the case, on the frozen data") unless the test's requirement is changed by his decision |
| S-5 | `docsfig-ternary-planted` (Examples, Figure 8) | does not advance (a synthetic table the story never mentions) | OD4 (b): "this one is great"; "Docs Figure 8 ... stays as drawn" (`WP19-slots.md`; `WP8a-decisions.md`) | goes: the figure alone leaves the "Reading it" list and the marker table with no picture, so the coherent unit is the subsection "Three metrics as shares of a total" | `examples.md` −19 (figure), −194 (subsection) | register: C001 (in the subsection) removed with the subsection; glossary: none dead (figure alone checked; `plot_ternary` and `ternary_marker_values` stay in the API list) |
| S-6 | `sect-future` (Section 12) | does not advance | His rule (`WP10-decisions.md`, "Simplifying assumptions: name, defend, go beyond"); the final remark is his ("reserved for a final remark in the paper"); "future work can include other cases spanning the engineering lifecycle" | goes | Future work −188 (whole section) | register C126, C127, C128 removed; two `{numref}` references to it (Sections 5 and 8) break; tests: `tests/test_paper.py` lines 75 and 1870; ledger row "Future work and final remark"; glossary: none dead |
| S-7 | `sect-process` (Section 13) | does not advance | His disclosure (`WP10-decisions.md`, OD5: "the paper's disclosure is the supervisor's own statement, in his voice"); a process pointer (the driver's call on process records) | goes | Acknowledgments −73 | register C129, C130 removed; tests: `tests/test_paper.py` lines 78, 1671–1672, 2123, and the reading pass's `zargham2026incose` row (line 2265) loses its sentence |
| S-8 | `prop-shift` (L2) | does not advance | WP10's R-17, approved by him ("Approved", `WP10-decisions.md`, scope approval): "Every lemma ... appears in paper.ipynb as a numbered block" | shortened to a pointer: the box `res-L2` goes; in `sec-results` "(L2)." becomes "({ref}\`Appendix B, L2 <appendix-b>\`)." | Results −44 (box 46, pointer +2) | **(6) fails:** `tests/test_paper.py::test_every_lemma_has_a_theorem_style_block_with_hypotheses_sketch_and_script` pins the tag list L1 to L17 in the body (R-17, R-18); register: none names the box (C014's fragment stays); glossary: none dead |
| S-9 | `prop-cumulant` (L6) | does not advance | as S-8 | shortened to a pointer: the box `res-L6` goes; in `run-L6` "(L6)," becomes "({ref}\`Appendix B, L6 <appendix-b>\`),"; A5 stays in Section 3's list (Appendix B uses it) | Results −48 | **(6) fails** as S-8; register C016's fragment contains "(L6)" and is re-pointed to the new wording; vocabulary: one baseline row goes stale (`first-use`, `paper/paper.ipynb`, "improvement factor") |
| S-10 | `tab-D-conditioning_diagnostic` (D.12) | does not advance (not pointed to; no reader would look) | the diagnostic is part of WP13's response to the external review, which he accepted ("Accepted", `WP13-decisions.md`: "the conditioning diagnostic and stated tolerances"); its printing in D was the driver's fix-before-acceptance G-4 of WP10 | goes: heading and paragraph `app-D-cond`, the table, the phrase in D's job list; Appendix E's G-row already prints the K = 1 and K = 3 values | Appendix D −52 | **fails twice:** `paper/environment_values.toml` names "D conditioning_diagnostic" (the scope's "Never" list); D.13 to D.17 renumber (X-4's ripple); tests: `test_appendix_d_prints_the_conditioning_diagnostic`, `_TERM_NUMBERED`; the generator stays (`paper_perturb.py`); glossary: "conditioning of the exponents" becomes once-used, not dead |

Not listed because no reader's verdict was against them: the abstract (non-goal), C406, C407 and the proposals'
sentence (non-goals; their tables are kept above), Appendix F (out by OD2 (b); its reader: advances), the root
page and its two images, the process pointers of Appendices A, D, E and G.

## Stuck

- **The readers' (the inventory's definition):** none. No reader returned "stuck" for any of the 122 units. The
  readers' Q9 lists (`WP28-inventory.md`, "Q9: read twice, still unplaced") are phrases a reader could not place,
  not verdicts on units; none is a cut here.
- **The record's (named in two or more review rounds with change requests and still drawing friction in the
  last):**
  - "Energy differential" (a term, not a unit): CR-5 in round 1, held through rounds 1b to 1d, five cells of round
    2 comment on it, both readers of WP19's round 2 still ask what it means, and the inventory's Q9 lists it five
    times (Figure 7, Appendix A, the Prediction page, the root page's Figure 1, the root page). Stuck by the record. His decision (CR-5: keep the
    term, gloss it): for him, not a cut.
  - The chart (now Figure 7, `fig-chart-level`): round 1 (CR-4), round 1b, round 2 (CR-30). Not stuck now: WP19's
    round 2 redraw passed its hypothesis and the inventory's reader says it advances.
  - The one-term plane (now Figure 5, `fig-planes-k1`): round 1 (CR-4), round 2 (CR-33). Not stuck now: the redraw
    passed (narrowly on the image alone) and the inventory's reader says it advances.
  - The near-frontier band in the planes: named in round 1b (CR-7, Definition 4's sentence) and round 2 (logged, no
    request); the band left the planes after WP19's round 2. Not stuck by the definition (no request in the last
    round).

## Counts

| | |
|---|---|
| Units | 122: advances 93, repeats 7, does not advance 21, split 1, stuck 0 (readers); the 29 not "advances": cut 3, cut with a failing check 1, for the supervisor 10, kept 15 |
| Stuck by the record | 1 term ("energy differential"), his; 0 units |
| Cuts by form | goes 3 (X-1, X-2, X-4), merged 0, pointer 1 (X-3); for the supervisor: goes 7, pointer 3 |
| Words that would leave (X-1 to X-3) | `docs/user-guide/chart.md` 597 → 561 (−36); `docs/examples.md` 716 → 676 (−40); docs total 6,792 → 6,716; `README.md` 162 → 98 (−64, not budgeted); paper body 0 |
| Words with X-4 | Appendix D −8 (no ledger ceiling) |
| Words if the supervisor took every S row | Results −92, Case construction −396, Case analysis −103, Future work −188, Acknowledgments −73 (paper body 9,894 → 9,042); Appendix D −52; `examples.md` a further −50 (S-4 and S-5's figure) or −225 (with S-5's subsection) |
| Register rows | removed: C303, C369, C370, C371 (4); re-pointed 0; with the S rows: removed C126 to C130, re-pointed C016 (C001 to judge with S-5) |
| Glossary entries made dead | 0 (every cut and every S row checked on a copy) |
| Pinned tests that would change | X-1: `tests/test_site.py::test_figures_are_few_captioned_and_in_both_colour_schemes` (the "chart-holes" member); X-4 if resolved: `tests/test_paper.py::test_c_has_the_metric_table_and_the_sources_and_d_has_the_extended_tables`, `::test_the_c_and_d_additions_are_current_and_cite_the_labels`, the pin at line 1541; X-2, X-3: none |
| Budgets after (OD5 (a)) | `chart.md` 561, `examples.md` 676, `TOTAL_BUDGET` lowered to the pass's total |

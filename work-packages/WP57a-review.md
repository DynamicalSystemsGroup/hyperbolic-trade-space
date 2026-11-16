# WP57a review: the front matter and Appendices A, F and G

Branch `wp57ab`, one commit after dev `b5b3a86`. Every count below is read from a named generated output:
`work-packages/WP57-rounds/a/counts-before.txt` and `counts-after.txt` (`uv run python
work-packages/WP57-rounds/map_counts.py --paper paper/paper.ipynb --supp paper/supporting_material.ipynb`, before
the edit and after re-execution), `tests/test_paper.py`, `scripts/check_vocabulary.py`, `scripts/check_residuals.py`,
`python -m derivation.proofmap`, the MyST build log. Screenshots: `work-packages/WP57-rounds/a/*.png`.

## What changed

| Place | Before | After | No longer does |
|---|---|---|---|
| Front matter (cell `frontmatter-supporting`) | title block and a companion paragraph (38 words; the counter's 44 include the 6 words of the YAML block) | title block (6) | tells the reader which appendix is for whom |
| Appendix A, cell `app-A-job` | Job block, 83 words | cut | says what the main text, the appendix and the repository each keep |
| Appendix A, `register_table` | 72 rows, 2,946 generated words, Layer column | 65 rows, 2,510 generated words, no Layer column | lists glossary entries no sentence of the paper or the appendices uses; prints a column blank in 62 rows |
| Appendix F, cell `app-F-job` | Job block, 116 words | cut; F.1 to F.4 as they were (141 prose words, 1,340 generated, 72 rows) | says what Section 11 and the repository keep |
| Appendix G, cells `app-G-job`, `app-G-scope` | Job block and scope sentence, 186 words | cut; the scope sentence queued (`WP57-rounds/assumptions-queue.md`) | argues with an objection, counts Section 2's words, lists its own contents |
| Appendix G, cell `app-G-horopca-pointer` | 12 words | cut (the HoroPCA entry's own text cites Appendix H) | narrates the page |
| Appendix G.2, cells `app-G-2`, `tab-G-reading_pass_table` | 54 prose words, 1,732 generated, 53 rows | moved to `paper/supplement/reading-pass.md` (written by `paper/generate_supplement.py` from `reading_pass_table(plain=True)`); one line of 29 words at the end of G.1 cites it | prints a table about the paper's text inside the paper |

Totals (typed prose of the four places): 44 + 83 + 257 + 252 = 636 before, 6 + 0 + 141 + 29 = 176 after; the
supporting material's typed prose 4,440 to 3,980 (`all` row of the two counts files). Generated words of the
supporting material: 57,839 to 55,659; table rows 1,298 to 1,237.

## The register filter (G2)

`generate_register.used_entry_ids` applies `scripts/check_vocabulary.py`'s matching (`load_glossary`, `segments`,
`match_spans`: an entry's term or alias, normalized tokens) to the paragraphs and generated Markdown outputs of
`paper/paper.ipynb` and `paper/supporting_material.ipynb`, with Appendix A's cells taken out by position. Result: 65
of 72 entries listed; off the page: `binding-term`, `characteristic-point`, `number-of-designs`,
`position-along-the-frontier`, `row-share`, `termination-status`, `ternary-plot`. The map estimated 62: its three
others, `number-of-terms`, `number-of-metrics` and `conditioning-of-the-exponents`, match in the generated step
prose of Appendix B (L11, L22) and in G.1's register text, so by the rule they stay.

Found while building it, outside this scope: `check_vocabulary.read_notebook` marks Appendix A's paragraphs by the
heading they sit under and misses a heading whose cell opens with an anchor line (`(appendix-a)=`), so the checker's
dead-entry rule today counts the register table as a use; a fix would report the seven entries above as dead.
Reported, not fixed.

## The glossary (G2, the driver's call 6)

Five `defined_in` fields repointed: `binding-term` to `plotting._ternary_region_of (docstring)`;
`characteristic-point` to `plot_ternary (docstring, Notes)`; `objective` and `loss` to `Preliminaries and notation`
(Section 3's sentence "Loss is scikit-learn's word for the function a solver minimizes; objective is kept for what the
decision-maker maximizes"); `launch-cost` to `model_v2/cubesat.sysml (calc def LaunchCost,
LaunchBudgetRequirement); case-model.md, The requirements and what each reads` (the field named `cubesat_r2.sysml`,
a file no longer in the tree). Found, outside this scope: five more fields name repository records (`WP41 note` on
`prediction`-family entries, three; `cubesat_r2.sysml ...; WP23-review.md`, two).

## Register rows

Retired: C131 (A's Job block, "compiled from `glossary.yaml` and never typed"), C161 (G's Job block, "with its
dropped candidates and the bibliography of all adopted sources"). Added: C1101 (the citing line in G.1), C1102 (the
supplement's sentence naming its generator and command). Ids C967 to C1100 left for WP56's unit.

## Tests

- `test_each_appendix_opens_with_its_job_and_three_tiers` becomes `test_job_blocks_remain_only_in_the_appendices_not_yet_tightened` (`JOB_BLOCKS = {C, D, E, H}`; A, B, F, G carry no Job block or tier phrase; B's goes in WP57b).
- `test_register_table_equals_the_glossary` becomes `test_register_table_equals_the_glossary_entries_in_use`.
- `test_register_opens_by_saying_it_is_not_exhaustive` becomes `test_appendix_g_is_the_register_and_one_line_citing_the_reading_pass` (the four cells of G by id).
- `test_reading_pass_table_is_in_appendix_g_and_current` and `_g2_cells` become `test_reading_pass_supplement_equals_its_generator_and_g1_cites_it` (the staleness test of R-3) and `test_generate_supplement_writes_what_its_generators_return`.

## Requirements

| ID | Check | Result |
|---|---|---|
| R-1 | kept anchors cited: `appendix-a` (Section 3), `appendix-f` (Section 11), `appendix-g` (Section 12); F.1 to F.4 and G.1 are their step deeper | `counts-after.txt`, "cited by" column: A [3], F [11], G [12] |
| R-2 | no sentence about the paper's text; residuals | `check_residuals.py --json` on dev's tree (b5b3a86) and on this branch: the surfaces of A, F, G and the title lose 7 metanarration counts (totals 16 to 9), 1 restatement-free, long sentences 263 to 259, compound 188 to 185, parens 823 to 818; no count of any surface rises except by re-keying (G.1's register now counts under `appendix/appendix-g`, the surface `appendix/g-1` having no paragraph of its own between the two headings). `--compare --strict` against the WP38 baseline (c0fe11b): 129 counts above it on dev, 130 here, the one difference that re-keying; the rises are in `docs/`, `site/` and the glossary long-forms surface, on dev before this branch |
| R-3 | supplement equals its generator; G.1 cites it; the cut text at `git show c89843a:paper/supporting_material.ipynb` (the nine cells unchanged between c89843a and dev b5b3a86, checked by id) | the two supplement tests pass |
| R-4 | proof map and derivation unchanged | `PROOF MAP OK: 22 lemma files, 549 tagged steps`; `git diff dev -- derivation/` empty |
| R-5 | suites, lint, format, lock, vocabulary, build | `uv run pytest -q -m "not slow"`: 2,086 passed, 17 skipped, 2 xfailed, then one more fix (`test_reader_depth_anchors_are_all_present` asserted the companion paragraph; it now asserts the title block alone) and the two touched tests rerun green; the slow paper suite runs once after WP57b; `ruff check`, `ruff format --check`, `uv lock --check` clean; `check_vocabulary.py` 0 new, 67 known (one row added: `termination-status` became a dead entry once the register table stopped counting as prose, see above); `python -m derivation.proofmap` 22 files, 549 steps; MyST build log without a warning or error |

## Screenshots

`work-packages/WP57-rounds/a/`: `top.png` (the title block, no companion paragraph), `front-and-A.png` and `A-table.png` (Appendix A, five columns, 65 rows), `F.png` (F opens on F.1), `G.png` (G opens on G.1), `G1-end.png` (the citing line, then Appendix H). Page checks by the screenshot script: no "Companion to the paper", "not exhaustive", "G.2 What the paper took" or "tested by experiment in Appendix H" on the page; "Job." occurs five times (B, C, D, E, H; B's goes in WP57b); the A table has 65 body rows and the header Term, Symbol, Meaning in this paper, Not, Defined in; the G.1 link resolves to `blob/main/paper/supplement/reading-pass.md`; no horizontal overflow at 1,280 px.

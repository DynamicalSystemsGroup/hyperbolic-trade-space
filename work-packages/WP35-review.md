# WP35 review (stage 6): HoroPCA acknowledged and distinguished, "hyperbolic" defined once, Table 1's "differs" column made uniform

Screenshots for this record: commit `2a669de`, `git show 2a669de:<path>` with `<path>` under `work-packages/WP35-review/`, `work-packages/WP35-review/reads/shots/`, `work-packages/WP35-rounds/build-shots/`.

Reviewer: a fresh reviewer who did not build it. Scope: `work-packages/WP35-scope-of-work.md`; decisions: `WP35-decisions.md`.
Build under review: `b1b43cf` (with the three earlier WP35 commits `4928795`, `6916871`, `dda1fe7`), on the staged site
http://127.0.0.1:8791/ (read only). **Commands run at head `cec9d70adce0a6de4fe3b1e124922775ceacfcd7`** (`origin/dev` when this
worktree `wp35rev` was cut; `b1b43cf` is its ancestor, and between them `paper/paper.ipynb` changed by two non-WP35 lines,
the WP33 abstract and Organization sentence, ledgered). Start head for the word counts: `7b47261` (the parent of the first
WP35 commit `4928795`; for the two notebooks it equals `b1b43cf^`). Nothing was edited in content; findings are recorded only.
Scripts are in the scratchpad, not here.

## Verdicts

| R | Verdict | Evidence |
|---|---|---|
| R-1 | met | `paper.ipynb` cell `sec-prior-art-3` has exactly one paragraph starting "**HoroPCA.**" (script: `[p for p in cell.split("\n\n") if "HoroPCA" in p]` gives 1). It says "the closest existing analog in setting, unsupervised with a table in and coordinates out, and the farthest in what is estimated", the borrowings ("that setting, the estimator interface of scikit-learn and PCA as a downstream step (Appendix D.16)"), "recovered the planted exponents only where the generator made them the direction of largest spread", and "is not a PCA of any kind". `grep "with a kernel"` over the cell: no match; "kernel PCA" appears only in the untouched Lineage sentence about the feature-engineering kin, not of HoroPCA. Rendered at 1280 (screenshot `section2-horopca-light-1280x800.jpg`): reads as written. `uv run pytest tests/test_paper.py -k "horopca or differs or section2_distinguishes or prior_art"`: 8 passed. A register row per sentence: R-8. |
| R-2 | met | `uv run pytest -q tests/test_paper.py -k "horopca or differs or section2_distinguishes or prior_art"`: 8 passed, including `test_the_horopca_table_equals_the_spike_record` (reads `results.json` and `analysis.txt` independently of the generator, 15 rows) and `test_the_horopca_passage_numbers_are_in_the_record`. The table is generated (`tab-G-horopca` code cell calls `horopca_table()`, listed in Appendix F's reproduction table). Spot checks of passage numbers against the record: 0.068 = `results.json` cubesat_primary R=3 k1 explained 0.06836; delta_rel 0.46/0.45 vs 0.42/0.39 = `gromov.txt` 0.457/0.446 vs 0.420/0.393; tree 0.00; distortion 0.20 vs 0.84 = `smalltree_run.txt` horopca vs pca. One mismatch of comparison basis: finding F-3. |
| R-3 | met | Appendix G cells `app-G-horopca`, `app-G-horopca-reading`: "the embedding was ours, not natural for the data ... Nothing in the data asks for it"; limits: "The embedding and its scale are ours", "seeded subsample of 500 rows of each cubesat table", "hyperparameters are the repository's defaults, with five restarts", "a spike and not a benchmark", "not run on the data of HoroPCA's own tasks"; cites `docs/superpowers/notes/spike-horopca/` (`grep -c` in the cell: 1; also asserted by the test). Rendered pages seen (`appendix-G-horopca-light-1280x800.jpg`). |
| R-4 | met | Direct check over `paper/prior_art.yaml` (17 entries): 0 `differs` cells and 0 `short.differs` cells not beginning "This work", 0 `does` cells beginning "This work". `uv run pytest tests/test_paper.py -k prior_art`: 4 passed; `test_every_differs_cell_has_this_work_as_its_subject` and the id assertion (`{"kernel-pca","horopca"} <= ids`, `kernel-hyperbolic-pca` absent) pass. Table 1 rendered shows both rows (`table1-light-1280x800.jpg`). |
| R-5 | met | `git diff 7b47261 HEAD -- paper/prior_art.yaml`: mixed rows' family half is in `does` (gp-maxaffine `does` ends "The sources fit regression surfaces."; mdao and tradespace `does` carry the family's scope); Pareto `differs` now reads "This work returns a coordinate system and exponents: the fit says what trades against what..." and `does` ends "A nondominated set says which designs survive, by a hard comparison." (rendered Appendix G, `appendix-G-register-light-1280x800.jpg`): no longer reads as a deficiency of the family. |
| R-6 | met | `uv run pytest -q tests/test_vocabulary.py`: 16 passed; `uv run python scripts/check_vocabulary.py`: "0 new violation(s), 63 known". `glossary.yaml` has `id: 'hyperbolic'` (58 entries, was 57); Appendix A prints it (`appendix-A-light-1280x800.jpg`, row "hyperbolic ... Definitions"); the glossary page prints it (`glossary-light-1280x800.jpg`, `glossary-dark-390x844.jpg`). `test_register_table_equals_the_glossary` passes in the not-slow `tests/test_paper.py` run (R-16). "Same push" is not checkable at commit granularity: the glossary (`6916871`) and the regenerated `tab-A-register` (`b1b43cf`) are separate commits; they agree at head. |
| R-7 | met | `uv run python docs/superpowers/notes/spike-horopca/grep_table.py .` at head, compared with `readout.md` 1a (10 rows): row 2 (Färe caveat in the DEA paragraph) is now the pointer 'The title's "hyperbolic" is defined in Section 4 and Appendix A'; row 3 (the HoroPCA disclaimer) is gone, replaced by the paragraph; row 4 (Definitions) unchanged; row 5 (Färe, `hyperbolic-graph-measure`) is "Its word ... is defined in Appendix A, and is not this measure"; row 6 split into `kernel-pca` (no "hyperbolic") and `horopca` (describing HoroPCA, "hyperbolic space"); row 8 (limitations second definition) is "The glossary and the paper define "hyperbolic""; row 9 (further reading) is "the nearest analog in setting; how this work differs". New mentions are descriptions of HoroPCA (paragraph, Appendix G) and the glossary entry itself, not caveats. `git diff 7b47261 HEAD -- paper/myst.yml README.md | wc -l`: 0 (title and README unchanged). |
| R-8 | met | `uv run pytest -q tests/test_claims_register.py`: 21 passed (and 127 passed, 1 skipped in `-m "not slow" tests/test_site.py tests/test_docs.py tests/test_claims_register.py tests/test_vocabulary.py`). |
| R-9 | met, with notes | Counts below. Section 2 nets 0 (565 to 565, test method); the docs fall (limitations 493 to 475, further reading 195 to 193, total of the budgeted pages 7254 to 7223, under `TOTAL_BUDGET` 7241 which itself moved 7254 to 7241, down only); the Appendix G rise (+659 words) has its ledger row with job and reader; `uv run pytest -q tests/test_site.py::test_word_budgets_hold`: 1 passed; `tests/test_paper.py` word-ceiling tests: in the not-slow run, passed (R-16). Notes: F-4 (limitations budget not lowered), and Table 1's short cells and the glossary grow (the new row, the new entry) without a ledger row of their own (tables count as data under the ledger's rule). |
| R-10 | met | Notebook cell comparison `7b47261` to head (script in scratchpad): paper.ipynb cells changed: `frontmatter`, `sec-decision-3`, `sec-prior-art-2`, `sec-prior-art-3` (source only; the first two are the WP33 abstract move, ledgered) and `tab-families` (Table 1 output); supporting_material.ipynb: `tab-A-register`, `tab-G-register`, `tab-G-reading_pass_table` outputs, `tab-F-reproduction` (one new row for `horopca_table()`), `tab-F-toolchain` (the observed commit hash only), and 3 new cells (`app-G-horopca`, `tab-G-horopca`, `app-G-horopca-reading`). No other cell's source or output differs. `git diff --stat 7b47261 HEAD -- examples paper/figures docs/figures`: empty. No figure file in `b1b43cf` (`git show --stat b1b43cf`: 0 figure paths). |
| R-11 | met | `git diff origin/dev -- pyproject.toml uv.lock src/ | wc -l`: 0 (at head); `git diff 7b47261 HEAD --stat -- pyproject.toml uv.lock src derivation`: empty; `uv lock --check`: "Resolved 178 packages". |
| R-12 | met on the record; the re-execution was not re-run | `git show --stat b1b43cf`: `paper/paper.ipynb` and `paper/supporting_material.ipynb` (and `claims_register.toml`, `length_ledger.toml`) in one commit, no figure file changed so none is owed. I did not run `paper/execute_notebooks.py` (it rewrites both notebooks in place, and "one writer at a time" forbids it from a review); the guard is the paper tests that compare each generated cell with its generator (`test_prior_art_committed_outputs_are_current`, `test_register_table_equals_the_glossary`, `test_the_horopca_table_equals_the_spike_record`, run in R-16: not-slow, 158 passed). |
| R-13 | met on the reading; wording fixes listed | three fresh reads against the intended reading in "R-13 and R-14" below: none implies a PCA, a hyperbolic-geometry method or a kernel method |
| R-14 | holds; six reader pairs triaged with one-line resolutions | "R-14 balance verdict" below; 20 consolidated fix-wording items and word-budget cuts proposed |
| R-15 | met, with findings F-1, F-2, F-5 to F-7 | Screenshots below; no raw markup, unrendered math or console error on any of the five surfaces; every link of the five pages fetched. |
| R-16 | see "Checks" | `uv run ruff check .`: All checks passed; `uv run ruff format --check .`: 623 files already formatted; `uv lock --check`: ok; `tests/test_text_encoding.py`: 2 passed; attribution: `git log 7b47261..HEAD` bodies for "co-authored", "generated with", "claude": 0; added lines in the diff outside `work-packages/` matching those words: 2, both unrelated (a history-page record about a person "co-authored the 2020 paper" and a script docstring "Generated by `scripts/history_record.py`", not attribution of a model). |

## Word counts per touched surface (start head `7b47261` against head `cec9d70`)

Method: the paper's own `rendered_words` and `words_by_section` (tests/test_paper.py), `prose_words` (tests/test_site.py) for the docs, whitespace words of the YAML fields for the register and the glossary. Script: scratchpad `wp35rev_count.py`.

| Surface | Before | After | Change |
|---|---|---|---|
| Paper body, all sections (test method; tables and abstract excluded) | 10186 | 10195 | +9 (the WP33 sentence moved from the abstract into Organization, ledgered, not WP35) |
| Section 2 "Prior art, by family" | 565 | 565 | 0 (119 added, 119 cut, per the ledger rows) |
| Appendices, supporting material markdown (all) | 3905 | 4564 | +659 |
| Appendix G markdown cells (`app-G*`) | 370 | 1029 | +659 (ledger `[[raise]]` 659 with job and reader) |
| `prior_art.yaml` entries | 16 | 17 | +1 row (the split) |
| `prior_art.yaml` `differs` (full), words | 541 | 620 | +79 |
| `prior_art.yaml` `does` (full), words | 494 | 580 | +86 |
| `prior_art.yaml` `short.differs` (Table 1), words | 116 | 130 | +14 |
| `glossary.yaml` entries / words (all string fields) | 57 / 3043 | 58 / 3131 | +1 / +88 |
| `docs/user-guide/limitations.md` | 493 | 475 | -18 |
| `docs/further-reading.md` | 195 | 193 | -2 |
| Docs, sum over the budgeted pages | 7254 | 7223 | -31 (`TOTAL_BUDGET` 7254 to 7241) |

## R-15: screenshots (`work-packages/WP35-review/`), one reading each

All taken at the staged site with system Chrome through Playwright (headless, `networkidle` then 5 s). `scrollWidth` equals the viewport on every page (no page-level horizontal scroll). Console and network on the docs pages show one line each: `404 https://api.github.com/repos/DynamicalSystemsGroup/hyperbolic-trade-space/releases/latest` (finding F-1); none on the paper pages.

| Surface (URL) | Size | File | Reading |
|---|---|---|---|
| Limitations, the "Name." line (`/docs/user-guide/limitations/`) | 1280x800 | `limitations-light-1280x800.jpg` | Reads: "Name. The glossary and the paper define "hyperbolic"." with two live links, set in the page's one-line style; nothing clipped. |
| | 390x844 | `limitations-light-390x844.jpg` | Same line at the foot of the page; wraps cleanly, links visible. |
| Further reading (`/docs/further-reading/`) | 1280x800 | `further-reading-light-1280x800.jpg` | The Charts and neighbouring methods list reads "Kernel PCA ... which is not built." then "HoroPCA ...: the nearest analog in setting; how this work differs." with a link; list intact. |
| | 390x844 | `further-reading-light-390x844.jpg` | Same two lines, link wraps to its own line; superscript references intact. |
| Glossary page (`/docs/generated/glossary/`; `/docs/glossary/` is a 404, the page is served under `generated/`) | 1280x800 light | `glossary-light-1280x800.jpg` | Entry H, "hyperbolic: The title's word: the level curves of V ... Not negative-curvature geometry, and not the graph measure of Färe, Grosskopf and Lovell." one entry in the alphabetical list. |
| | 390x844 light | `glossary-light-390x844.jpg` | Taken at the top of the page (A to C); the H entry is shown in the dark 390 shot and the 1280 shots. |
| | 1280x800 dark | `glossary-dark-1280x800.jpg` | Top of the page in dark theme, legible; the H entry is not in frame (the entry is shown in the light 1280 shot). |
| | 390x844 dark | `glossary-dark-390x844.jpg` | The H entry in dark theme at phone width, legible, wraps cleanly. |
| Appendix A, register table (`/paper/supporting-material/` at `#tab-A-register`) | 1280x800 | `appendix-A-light-1280x800.jpg` | The row "hyperbolic" sits between "invariant value" and "exponent vector" with meaning, "Not" and "Defined in: Definitions"; math rendered, all five columns visible. |
| | 390x844 | `appendix-A-light-390x844.jpg` | Table inside a horizontal scroll container (scrollWidth 654 in 346): Term, Symbol and the start of Meaning visible, "Not" and "Defined in" are off-screen until scrolled (F-2). |
| Appendix G register, Pareto row (`#tab-G-register`) | 1280x800 | `appendix-G-register-light-1280x800.jpg` | "What this work does differently" opens "This work returns a coordinate system and exponents ..." as a sentence; the Pareto "does" ends with the hard-comparison sentence. |
| | 390x844 | `appendix-G-register-light-390x844.jpg` | Same list at phone width, wraps. |
| Appendix G HoroPCA table (`#tab-G-horopca`) | 1280x800 | `appendix-G-horopca-light-1280x800.jpg` | Fifteen-row generated table, six columns, numbers readable; heading "HoroPCA's" shows the dotted abbreviation underline across "PCA" inside the word (F-5). |
| | 390x844 | `appendix-G-horopca-light-390x844.jpg` | Last column ("HoroPCA: two directions, alignment") is cut at the right edge of its scroll container (412 in 346) (F-2). |
| Table 1 (`/paper/` at `#tab-families-1`) | 1280x800 | `table1-light-1280x800.jpg` | Four columns; every "Differs" cell opens "This work ..."; Kernel PCA and HoroPCA are two rows (the second partly below the fold). |
| | 390x844 | `table1-light-390x844.jpg` | The Differs column is cut at the container edge ("This wor"; scrollWidth 379 in 346) (F-2). |
| Section 2 (`#sec-prior-art-3`), not asked for, taken because it is the main deliverable | 1280x800 | `section2-horopca-light-1280x800.jpg` | The HoroPCA paragraph reads as the scope requires; "HoroPCA" is set with a dotted abbreviation underline across "PCA" in the bold lead-in and in the first sentence (F-5). |
| | 390x844 | `section2-horopca-light-390x844.jpg` | Paragraph wraps cleanly. |
| Incidental, Appendix E (`#tab-E-gaps`) | 1280x800 | `incidental-appendixE-raw-math-light-1280x800.jpg` | Raw `$...$` TeX shown as literal text in the gaps table (F-6); present at the start head too. |

Links fetched from the five pages (distinct URLs, fragment stripped, GET): limitations 22 links, 0 non-200; glossary 35, 0 non-200; further reading 57, 2 non-200 (two doi.org redirects answered 403, publisher bot walls: `10.1093/biomet/70.1.57`, `10.1162/089976698300017467`); the paper's Table 1 page 209 links, 25 non-200, all doi.org (21 answered 403, 3 answered 202, and `10.1007/978-94-009-4109-0` answered 404); supporting material 682 links, 7 non-200 (GitHub 404s, F-7). In-page targets checked: `#sect-definitions`, `#sect-prior-art`, `#appendix-g`, `#tab-families-1`, `#sec-prior-art-3` exist.

## Findings (record only; nothing fixed)

| # | Severity | Finding |
|---|---|---|
| F-1 | low | Every docs page logs `404 https://api.github.com/repos/.../releases/latest` (the theme's repository widget; the repository has no release or is private). One console error per page load on the three docs pages in R-15. Not WP35's; the paper pages are clean. |
| F-2 | medium | At 390 px the tables of Table 1, Appendix A and Appendix G (HoroPCA) sit in a horizontal scroll container, and the column this package is about, "Differs" (Table 1), "Not"/"Defined in" (Appendix A) and the last column of the HoroPCA table, is off-screen in the first view, with no visible cue other than a clipped word. The theme does this to every table; WP35's new column set (a longer "Differs" cell) and new HoroPCA table inherit it. |
| F-3 | low | Appendix G passage says R = 3 HoroPCA keeps 0.068 "against PCA's 0.325 on the cubesat primary". 0.325 is PCA on all rows (`analysis.txt` line 3); HoroPCA ran on the 500-row subsample, where PCA's first component is 0.328 (`analysis.txt` line 21, `results.json` 0.32789). The test pins the string "0.068 against PCA's 0.325" rather than the like-for-like value. The conclusion is unaffected (0.003 difference); the basis differs and the passage names the subsample elsewhere, not here. |
| F-4 | low | `tests/test_site.py` `BUDGETS` for `limitations.md` still reads 493 while the page is now 475 (the `TOTAL_BUDGET` was lowered 7254 to 7241, the per-page cap was not), leaving 18 words of unledgered room. |
| F-5 | low | The paper's abbreviation markup puts the dotted "PCA" tooltip inside the word "HoroPCA" (two instances in Section 2, one in the bold lead-in, and in Appendix G); it reads as a typesetting accident and suggests "Horo" is a separate word. |
| F-6 | low, incidental, not WP35 | Appendix E's gaps table (`tab-E-gaps`) renders its TeX as literal `$\Phi(u)=w\cdot u-\beta=0$` in the cells (visible at 1280 and 390); identical at the start head `7b47261`.  Not raised by this package. |
| F-7 | info, not WP35 | Seven GitHub links in the supporting material (`derivation/lemma_12`, `15` to `20`) return 404 on `blob/main`; `origin/main` holds `lemma_12_facet_gap.py` to `lemma_14` only (the links name `lemma_12_term_gap.py` and `lemma_15` to `lemma_20`, which exist on `dev` and not yet on `main`), and `lemma_01_weighted_geometric_mean.py`, which is on `main`, also returns 404 to an unauthenticated fetch (the repository is private). Publisher DOIs 403 to `curl`/`urllib` (bot walls), and `doi.org/10.1007/978-94-009-4109-0` returns 404 although the bibliography records it verified by Crossref. None are touched by WP35. |
| F-8 | info | The Appendix G passage states "HoroPCA respects negative curvature and is built for data that has it" and credits it with a distortion of 0.20 against 0.84 for PCA on the authors' small tree. Both are backed by the record; recorded as the fair-to-HoroPCA content the scope's definition of good asks for, with no finding. |

## Checks run at `cec9d70`

| Command | Result |
|---|---|
| `uv run ruff check .` | All checks passed |
| `uv run ruff format --check .` | 623 files already formatted |
| `uv lock --check` | Resolved 178 packages |
| `uv run pytest -q tests/test_text_encoding.py` | 2 passed |
| `uv run pytest -q tests/test_paper.py -k "horopca or differs or section2_distinguishes or prior_art"` | 8 passed |
| `uv run pytest -q tests/test_paper.py -k prior_art` | 4 passed |
| `uv run pytest -q tests/test_claims_register.py` | 21 passed |
| `uv run pytest -q tests/test_vocabulary.py` | 16 passed |
| `uv run pytest -q tests/test_site.py::test_word_budgets_hold` | 1 passed |
| `uv run pytest -q -m "not slow" tests/test_site.py tests/test_docs.py tests/test_claims_register.py tests/test_vocabulary.py` | 127 passed, 1 skipped |
| `uv run python scripts/check_vocabulary.py` | 0 new violation(s), 63 known |
| `uv run pytest -q -m "not slow" tests/test_paper.py` | 158 passed, 3 skipped, 15 deselected in 139 s (includes `test_register_table_equals_the_glossary`, `test_prior_art_committed_outputs_are_current`, the HoroPCA table and passage tests, the ledger ceiling tests). The unfiltered file run was stopped after 14 minutes on the slow-marked tests; the 15 slow tests were not run (the scope asks for not-slow on touched tests, the full suite at the gate) |
| `git diff origin/dev -- pyproject.toml uv.lock src/` | empty |

## R-13 and R-14: the fresh readers on the finished Appendix H and Section 2

Amendment 1 (RA-10, RA-11): three fresh readers, each given only Section 2 and Appendix H (with the Appendix G
pointer) as rendered at `3d5a53e` on the staged site (127.0.0.1:8791), judged in a browser pane. Their returns are kept
verbatim in `WP35-review/reads/` (`read-P9.md`, an expert mathematical-presentation reader; `read-P10.md`, a novice
reader; `read-R13.md`, a cold reader with no persona). Nothing was edited in a notebook or elsewhere: this section
records and triages.

**Conditions of the reads, stated plainly.** The readers' browser panes were about 800 px (R-13) to 840 px (P10) wide,
not 1280 px. P9's file is named `P9-h3-results-1280.jpg` and its header says 1280 by 800, but the image is 800 by 506, so
the 1280 label is not met either. The 390 by 844 reads were done (P9 and R-13 saved a 390 shot of the table; P10 looked
at 390 and saved nothing, "seen at 390 (not saved)"). The browser tool returns images inline and writes no files: the
images in `reads/shots/` were saved afterwards by copying (P9: `P9-h3-results-1280.jpg`, `P9-h3-table-390.jpg`; R-13:
`R13-appendixH-top-desktop.jpg`, `R13-table1-390.jpg`). **The screenshots in `reads/shots/` are what exist.** The build's
own 1280 by 800 and 390 by 844 screenshots of the finished appendix (not the readers') are the `appH-*` files in
`WP35-review/` (commit `3d5a53e`). So no reader saw Appendix H at 1280 px width: a gap, listed again in the acceptance
note. Console: P9 and P10 saw no errors; R-13 saw only thebe debug lines, and its four error lines were CORS blocks
from its own fetch tests.

**Disposition key.** *fix-wording*: a plain-word or one-line change, with the owning place. *fix-link*: repository
links 404 on `blob/main` until the merge to `main`; not a defect, resolves after the merge, to be re-checked in the
WP8b checklist row G2. *leave*: no change, with the reason. *out-of-scope*: not this package's surface (none arose).
Severities are the readers' own. Finding numbers are each reader's own; "FW-n" refers to the consolidated fix-list
below. Owning units are notebook cell ids in `paper/supporting_material.ipynb` (`app-H-job`, `app-H-1`, `app-H-2`,
`tab-H-hypothesis-caption`, `app-H-4`, `app-H-4b`, `app-H-5`) and `paper/paper.ipynb` (`sec-prior-art-3`); the
generated sentences are owned by functions in `paper/generate_prior_art.py`.

### P9 (expert): 22 findings

| # | Severity | Verbatim quote | Disposition |
|---|---|---|---|
| 1 | slows a reading | "The hypothesis, committed with its refutation conditions before any table existed (record)" | fix-wording (FW-2): "before any table of this experiment existed"; `app-H-1` |
| 2 | slows a reading | Section 2: "In a pre-registered test"; H.1: "prospectively specified follow-up" | fix-wording (FW-1): "a prospectively specified test" in `sec-prior-art-3`; one term for one thing |
| 3 | slows a reading | "the spread ratio ρ, the spread along the edge's vector over that along the next largest direction" | fix-wording (FW-3): standard deviation, and "largest direction orthogonal to it" (the record's own definition, `hypothesis.md` lines 16 to 18); `app-H-1` |
| 4 | slows a reading | "Kind B moves the vector, by t, off the generator's depth direction" | fix-wording (FW-4): t and depth direction in one clause; `app-H-1` |
| 5 | blocks a reading | "kind C removes the edge" and "In C, ρ is 2 or 0.5 and the rows are symmetric" | fix-wording (FW-5): what C still scores and what symmetric means; `app-H-1`, `app-H-2` |
| 6 | slows a reading | "this work recovers the vector in at least 0.9 of the tables"; "at most 0.1 at ρ ≤ 0.5"; "PCA at most 0.2" | fix-wording (FW-6): counts, since there are six tables per cell; `horopca_conditions()` |
| 7 | polish | "refuted by any cell below" | fix-wording (FW-6): "under 6 of 6"; `horopca_conditions()` |
| 8 | slows a reading | "PCA and HoroPCA, in at least 0.9 at ρ ≥ 2 and at most 0.1 at ρ ≤ 0.5" | fix-wording (FW-7): "HoroPCA at R = 0.25 and at R = 1"; `horopca_conditions()` |
| 9 | polish | "All 26 checks over the 11 cells hold" | fix-wording (FW-11): H3's stated clause names PCA only, so 26 does not follow from the printed clauses; `horopca_verdict_sentence()` |
| 10 | slows a reading | "the leading directions of PCA and HoroPCA track the variation in the sampled designs" | fix-wording (FW-14): narrow to what the table prints; `app-H-4` |
| 11 | slows a reading | "the authors' code recovered planted exponents only where they were the direction of largest spread" | fix-wording (FW-4: the depth direction is where the generator puts its spread, so B at t = 0 is named). The "planted" against "vector" pair is leave: Section 2 is plain-word and the appendix defines the vector |
| 12 | slows a reading | "on the paper's tables its exponents are recovered by neither HoroPCA nor PCA except where the generator made them the direction of largest spread (Appendix H, and the earlier spike's record)" | fix-wording (FW-15): "on the synthetic tables of Appendix H, the first components of PCA and HoroPCA ..."; `paper/prior_art.yaml` HoroPCA entry (lines 297 to 299), printed in Appendix G |
| 13 | slows a reading | "returns a gap bounding the result's distance from the best" | fix-wording (FW-16): the shortfall is in objective value, not distance; `app-H-5` |
| 14 | slows a reading | "which for one term is convex, by a linear program or sequential quadratic programming" | fix-wording (FW-17): drop "by a linear program or sequential quadratic programming" (also P10's jargon); `app-H-5` |
| 15 | slows a reading | "That objective is not convex: the authors' code runs Adam from random starts" | fix-wording (FW-18): split the sources by claim (objective: the paper; Adam and restarts: the repository); whether the claims register backs the non-convexity is for the owner to check, not decided here; `app-H-5` |
| 16 | slows a reading | "optimizes a frame, k orthonormal directions, so that points projected along horospheres ... keep the most variance" | leave: the reader calls it a defensible gloss; the Busemann function and base point would cost words and lose the novice, and estimands-before-H.2 would break the section order of RA-1 (hypothesis, design, results, interpretation, formalism). This work's estimand is already in H.1 ("a vector of exponents defining a surface that bounds the rows from above") |
| 17 | slows a reading | "the log-metrics are centred and scaled until the farthest lies at distance R from the centre" | fix-wording (FW-10): name the map in limit (a), "the exponential map at the origin" (`hypothesis.md` line 74); `app-H-4b` |
| 18 | polish | "though an analyst with other domain information might choose it" | fix-wording (FW-20, a cut): padding, not backed by the experiment; `horopca_slab_sentences()` |
| 19 | slows a reading | "PCA's component of least variance recovers the vector in 5 of 6 tables at ρ = 0.25 and at t = 0.9, and in none of the other nine cells" | fix-link for the source links the count rests on; the count itself is leave: it is generated from `pca_last_rec` in the record, and the generator raises if the record no longer fits the sentence |
| 20 | slows a reading | "Source: results.json, readout.md." (both 404 on `blob/main`) | fix-link: the files are on `dev` and not yet on `main`; the hypothesis link is pinned to a commit and opens. Optional, the supervisor's call: pin the two links to a commit as the record link is |
| 21 | polish | two tables called "Table 1" on different pages | leave: the build numbers each document's tables itself; the two are on different pages and neither cross-reference is ambiguous |
| 22 | polish | "five restarts" and "HoroPCA ran one direction at its default settings" | leave: `hypothesis.md` lines 74 to 76 list the restarts among "the repository's defaults"; if the owner finds five is ours and not the default, the limit reads "default settings, five restarts" (+2 words) |

### P10 (novice): 11 findings

| # | Severity | Verbatim quote | Disposition |
|---|---|---|---|
| 1 | slows a reading | "H1 (A, B): this work recovers the vector in at least 0.9 of the tables; refuted by any cell below." | fix-wording (FW-8, FW-6): give the threshold's number at first use, "reaches 0.9" in `app-H-1`; the counts of FW-6 remove the second 0.9 |
| 2 | slows a reading | "Tables of kind A keep the edge and vary the spread ratio ρ, the spread along the edge's vector over that along the next largest direction." | fix-wording (FW-3): "the edge's vector (the planted exponents)"; `app-H-1` |
| 3 | slows a reading | "Kind B moves the vector, by t, off the generator's depth direction" | fix-wording (FW-4); `app-H-1` |
| 4 | slows a reading | "HoroPCA needs a ball, so the log-metrics are centred and scaled until the farthest lies at distance R from the centre: nearly flat at R = 0.25, moderately curved at R = 1." | fix-wording (FW-9): "a ball (the disk that models hyperbolic space)"; `app-H-2` |
| 5 | slows a reading | "survives (H1, H2)" ... "survives" / "All parts" | fix-wording (FW-12): one caption line, "H1 to H4 are the predictions listed in H.1"; `tab-H-hypothesis-caption`. The "All parts" row with empty cells is leave: it is the verdict over every cell, and the caption line says so |
| 6 | polish | "HoroPCA, R = 0.25 and 1" with cells "0/6, 0/6" | fix-wording (FW-12): "(R = 0.25, R = 1)" in the same caption line |
| 7 | slows a reading | "All 26 checks over the 11 cells hold" | fix-wording (FW-11) |
| 8 | slows a reading | "Source: results.json, readout.md." | fix-link (as P9 20) |
| 9 | polish | "PCA's component of least variance recovers the vector in 5 of 6 tables ..." | fix-wording (FW-13): "(its fourth)" after "component of least variance"; `horopca_slab_sentences()` |
| 10 | polish | "recovered planted exponents only where they were the direction of largest spread" (Section 2) | leave: the reader accepts it ("Acceptable"); "planted" is defined where the appendix is entered |
| 11 | polish | "with horospherical projections" (Section 2) | leave: the reader finds it fine for a paragraph that names the method; the gloss is in H.5, and Section 2 has no spare words |

### R-13 (cold reader): 10 findings

| # | Severity | Verbatim quote | Disposition |
|---|---|---|---|
| 1 | slows a reading | "In a pre-registered test, on an embedding of ours, the authors' code recovered planted exponents only where they were the direction of largest spread (Appendix H)." | fix-wording (FW-1) |
| 2 | slows a reading | "Kind B moves the vector, by t, off the generator's depth direction, and kind C removes the edge." | fix-wording (FW-4, FW-5) |
| 3 | slows a reading | "H1 (A, B): this work recovers the vector in at least 0.9 of the tables; refuted by any cell below." | fix-wording (FW-6): "6 of 6" |
| 4 | slows a reading | "H2 (A): PCA and HoroPCA, in at least 0.9 at ρ ≥ 2 and at most 0.1 at ρ ≤ 0.5" | fix-wording (FW-6, FW-7): the missing noun, "recover the vector in" |
| 5 | slows a reading | "HoroPCA needs a ball, so the log-metrics are centred and scaled until the farthest lies at distance R from the centre" | fix-wording (FW-9): one plain line for the ball and R |
| 6 | slows a reading | "HoroPCA optimizes a frame, k orthonormal directions, so that points projected along horospheres (the curved counterparts of hyperplanes in flat space) keep the most variance." | leave: the reader's own expected change is "None needed" (both words are defined where first used) |
| 7 | polish | "Source: results.json, readout.md." | fix-link (the links). The regenerating command beside the source is leave: the Job block names the folder, RA-10(4) asks for a source or a command, and a source is given |
| 8 | polish | "Appendix D.16 chains them, running PCA on the chart of the near-frontier designs." | leave: the reader says "Pointer is present; fine" |
| 9 | polish | "returns a gap bounding the result's distance from the best" | fix-wording (FW-16): "gap" and "distance" |
| 10 | polish | "All 26 checks over the 11 cells hold" | fix-wording (FW-11) |

### The checks C1 to C7 against the intended reading

The intended reading is RA-10 and RA-6 as the amendment states them. The readers' words are verbatim from their returns.

| Check | Intended reading | P9 | P10 | R-13 |
|---|---|---|---|---|
| C1 threshold and chance rates before the table | "recovered" has the threshold 0.9 on \|cos\| and the chance rates beside it, before the table | holds: "The threshold is \|cos\| ≥ 0.9, fixed before the run. Chance reaches it with probability 0.037 for a random direction and 0.152 for a random point of the simplex"; both rates reproduced by simulation at d = 4. Caveat: the 0.9 appears in H1 before it is stated in words | holds with a late first number: H.1 defines \|cos\| and says "the threshold below" (finding 1); "simplex" has no line | holds: "It precedes Table 1" |
| C2 causal arm and failure condition | arm A varies the spread with the edge fixed; refutation stated | holds: "At ρ = 2, removing the edge takes this work from 6 of 6 tables to 0 of 6 and leaves PCA at 6 of 6" | holds | holds |
| C3 one plain line at first use (R, PC, \|cos\|, span alignment, distortion, frame, horosphere) | one plain line each of those that are used | partly: R plain; frame and horosphere late (H.5); "t, depth direction, generator, spread, tree-like, temperature, one term, symmetric" missing | R, \|cos\|, frame, "recovers" hold; "does not hold for 'depth direction', 'ball' and 'simplex'" | R "could not tell / partly"; \|cos\| holds; frame and horosphere only in H.5, defined there; PC, span alignment, distortion not used |
| C4 sources, caption, link that opens | every kept number has a source; the table has a caption and a source link | does not hold: "both links return 404" (fix-link) | does not hold fully: "two of the links 404 at blob/main" (fix-link) | could not tell: the in-page fetch was blocked by CORS; the Chami URL returned 200 |
| C5 390 px, no clipped column | all columns visible | holds: five columns visible, document 390, table 346 (`P9-h3-table-390.jpg`) | holds: wrapper scrollWidth 346 = clientWidth 346 (not saved) | holds: table 346 of 366, scrollWidth 390 (`R13-table1-390.jpg`) |
| C6 register | no sentence says HoroPCA is worse; none calls this work a PCA, a hyperbolic-geometry method or a kernel method | holds: "is not a PCA of any kind"; "the methods answer different questions" | holds; "this work tracks the planted upper boundary" could be read as a win, but a qualifier on orientation follows | holds: nothing implies a PCA, a hyperbolic-geometry method or a kernel method ("This work builds no kernel") |
| C7 reading limits | the embedding ours, clean small data not tree-like, six tables per cell, defaults, R = 3 reported not tested | holds with one gap: "30 percent" is in H.2 and not in limit (b); "in the record" does not say where | holds | holds, with the same one item: "30 percent of the rows on the edge" is in H.2 and not in the limits |

The three own-words summaries match the intended reading. R-13: "This work differs in what it estimates: the one-sided
edge of a table (a vector of exponents for a boundary surface), not a variance. It 'is not a PCA of any kind'", and the
solver contrast (non-convex Adam from random starts against a convex program with a gap). P10: "Appendix H asks whether
HoroPCA ... estimates the same thing as this work ... Every prediction held. The authors say the two methods answer
different questions and can be chained". P9: "PCA and HoroPCA follow the spread of a table, this work follows its upper
edge ... the hypothesis survives". P9's recomputation of the four printed verdict rows (A at ρ = 0.5 and 2, B at
t = 0.9, C at ρ = 2) agrees with the printed cells. The one shared mismatch with the intended reading is
"pre-registered" in Section 2 against "prospectively specified" in H.1 (P9 2, R-13 1).

**R-13 verdict: met on the reading, with wording fixes listed.** Each reader says in its own words what HoroPCA is, how
this work differs and what is shared; none found a sentence that implies a PCA, a hyperbolic-geometry method or a
kernel method.

### R-14 balance verdict

**The pair holds as a pair.** The novice follows the thread (P10 summarised the appendix correctly and lost it only
briefly, at "depth direction" and in the Adam sentence of H.5); the expert finds the printed numbers right and two
sentences that say more than the experiment shows (FW-14, FW-15). Where the two readers' asks conflict, each pair has a
one-line resolution that serves both:

| Pair | P9 asks (precision) | P10 asks (plainness) | One-line resolution serving both |
|---|---|---|---|
| ρ, t, depth direction | ratio of standard deviations; which direction is the denominator at ρ < 1; t defined | the sentence is dense: "spread", "the vector" and "next largest direction" arrive together | two plain sentences in `app-H-1`, one per kind: "Kind A keeps the edge and varies ρ, the standard deviation along the edge's vector over that along the largest direction orthogonal to it." "Kind B moves the vector by t from the generator's depth direction (equal exponents) toward one metric." |
| Fractions against counts | "at least 0.9 of the tables" can only mean 6 of 6 | two different 0.9s (a share of tables, a \|cos\|); the number arrives late | state H1 to H4 as counts ("in 6 of 6 tables"), so the only 0.9 left is the \|cos\| threshold, and give it at first use ("reaches 0.9") |
| Jargon in the solver paragraph | do not say "linear program" of a log-mean-exp | Adam, convex, LP, SQP are jargon | drop "by a linear program or sequential quadratic programming"; keep "Adam" with its source and "convex" (one word, a property the lemma proves) |
| Ball and map | name the map into the ball | "ball" and "curved" are not linked to anything known | the plain gloss "(the disk that models hyperbolic space)" in the design paragraph; the exact map, "the exponential map at the origin", in reading limit (a), where the expert reads it |
| Estimand placement | state the three estimands together before H.2 | keep the thread in order | leave: this work's and PCA's estimands are in H.1 in words; the criterion for HoroPCA stays in H.5, as RA-1 fixes the section order |
| Section 2 terms | "planted exponents" against "vector" (two words, one object) | "planted" and "horospherical" unexplained | leave both: Section 2 is one budgeted paragraph with a link to the appendix, and both readers say it suffices to decide to open the appendix |

The expert's remaining asks go where the novice does not read them (the design paragraph, the reading limits, the
caption) or are cuts or narrowings, which cost the novice nothing.

### Consolidated fix-list of wording changes (duplicates merged across readers)

Estimated words are mine and not measured; the ledger test and the word test measure.

| FW | Change | Owning place | Raised by | Words |
|---|---|---|---|---|
| FW-1 | "pre-registered" becomes "prospectively specified" (one term for one thing) | `sec-prior-art-3` (Section 2) | P9 2, R-13 1 | 0 |
| FW-2 | "before any table existed" becomes "before any table of this experiment existed" | `app-H-1` | P9 1 | +4 |
| FW-3 | ρ: "the standard deviation along the edge's vector (the planted exponents) over that along the largest direction orthogonal to it" | `app-H-1` | P9 3, P10 2 | +6 |
| FW-4 | B: "moves the vector by t from the generator's depth direction (equal exponents, where the generator puts its spread) toward one metric": generator, t and depth direction in one clause | `app-H-1` | P9 4, 11; P10 3; R-13 2 | +8 |
| FW-5 | C: "removes the edge and still scores the same vector"; "the rows spread symmetrically along the vector" | `app-H-1`, `app-H-2` | P9 5; R-13 2 | +8 |
| FW-6 | H1 to H4 as counts ("in 6 of 6 tables", "in 0 of 6", "in at most 1 of 6"); "refuted by any cell under ..."; the missing noun ("recover the vector in") | `horopca_conditions()` | P9 6, 7; P10 1; R-13 3, 4 | +2 |
| FW-7 | H2 names "HoroPCA at R = 0.25 and at R = 1" | `horopca_conditions()` | P9 8 | +4 |
| FW-8 | the threshold's number at first use: "reaches 0.9" | `app-H-1` | P10 1 | +3 |
| FW-9 | "a ball (the disk that models hyperbolic space)" | `app-H-2` | P10 4, R-13 5 | +6 |
| FW-10 | limit (a): "the exponential map at the origin into the ball" for "the map into the ball" | `app-H-4b` | P9 17 | +5 |
| FW-11 | "All 26 checks over the 11 cells hold" becomes "Every check in the 11 cells holds" (the alternative, a one-line count rule, costs about 12 words); any test or claims row that pins "26" moves with it | `horopca_verdict_sentence()` | P9 9, P10 7, R-13 10 | 0 |
| FW-12 | caption: "H1 to H4 are the predictions listed in H.1; HoroPCA cells read R = 0.25, R = 1" | `tab-H-hypothesis-caption` | P10 5, 6 | +12 |
| FW-13 | "PCA's component of least variance (its fourth)" | `horopca_slab_sentences()` | P10 9 | +3 |
| FW-14 | H.4 narrowed: "PCA and HoroPCA recover the vector only where it is the direction of largest spread, in these cells, and the methods answer different questions" for "the leading directions ... track the variation in the sampled designs, so their agreement depends on how the boundary's orientation relates to the sample's spread" | `app-H-4` | P9 10 | -12 |
| FW-15 | Appendix G's HoroPCA entry: "on the synthetic tables of Appendix H, the first components of PCA and HoroPCA recover the exponents only where ..." for "on the paper's tables its exponents are recovered by neither HoroPCA nor PCA except ..." | `paper/prior_art.yaml` (lines 297 to 299), printed in Appendix G | P9 12 | +6 (Appendix G's own row) |
| FW-16 | "returns a gap bounding the result's shortfall from the best value" and "nothing bounds how far its objective is from the best" for "distance from the best" | `app-H-5` | P9 13, R-13 9 | +3 |
| FW-17 | drop "by a linear program or sequential quadratic programming" | `app-H-5` | P9 14 (P10 jargon) | -8 |
| FW-18 | sources by claim: the objective's non-convexity from the paper, Adam and restarts from the repository at c9a9996 | `app-H-5` | P9 15 | +4 |
| FW-19 | "30 percent of the rows on the edge" added to reading limit (b) | `app-H-4b` | R-13 C7, P9 C7 | +8 |
| FW-20 | cut "though an analyst with other domain information might choose it" | `horopca_slab_sentences()` | P9 18 | -10 |

**Count: 20 consolidated fix-wording items** (FW-1 to FW-20), from 32 reader findings marked fix-wording: P9 17
(findings 1 to 15, 17, 18; finding 11 counted once), P10 8 (1 to 7, 9), R-13 7 (1 to 5, 9, 10). No finding is
out-of-scope. The fix-link findings are P9 19 and 20, P10 8, R-13 7, and C4 of every reader; they resolve after the merge
to `main` and are to be re-checked in WP8b checklist row G2. Finding F-7 of this review recorded that a file already on
`main` also returned 404 to an unauthenticated fetch (the repository is private): row G2 should fetch with and without
sign-in before calling the links resolved.

### Word budget note

Appendix H is at 899 of 900 words (headroom 1), so every net addition needs a compensating cut. The positive entries
above total about +79 words gross if all are taken (FW-2 to FW-10, FW-12, FW-13, FW-16, FW-18, FW-19; FW-15 sits in
Appendix G's own ledger row); the in-place cuts FW-14, FW-17 and FW-20 take back -30, leaving about +49 net. Proposed
further cuts, each with what the content no longer did:

1. `app-H-job`: "**This appendix carries:** the hypothesis, experiment, results, reading and solver differences." (-12). It lists the
   headings that follow.
2. `app-H-4`: after FW-14, "and the methods answer different questions" (-6). The next sentence, "The methods are
   complementary", carries the register; the clause repeats it.
3. `app-H-4b`, limit (b): "robustness under realistic sampling is separate" (-6). The limit already says "a mechanism
   demonstration".
4. `app-H-2`: "no noise," (-2). Limit (b) says noise-free.

These four give about -26. The first tier, FW-1 to FW-9, FW-11, FW-12, FW-14, FW-16, FW-17 and FW-20 (about +56 gross,
-30 in place), then nets about 0 against the cuts. The second tier (FW-10, FW-13, FW-18, FW-19, about +20) has no cut I
can propose that is clearly a negative edit: either the ledger takes a raise row of about 20 words with job and reader
(the supervisor's call) or those four are left, each at its reader's severity (all slows a reading or polish, none
blocking). FW-5 is the only finding rated "blocks a reading" (P9 5) and is in the first tier. The word counts are my
estimates.

### Acceptance note

R-13 and R-14 are met on the reads, with the 20 wording items to apply by the owning units and the supervisor's call on
the second-tier budget. Not yet seen by a reader: Appendix H rendered at 1280 by 800 (the readers' panes were 800 to
840 px; the build's own 1280 shots are the `appH-*` files in `WP35-review/`), and the links to `results.json` and
`readout.md` opening (they open after the merge to `main`).

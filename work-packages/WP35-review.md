# WP35 review (stage 6): HoroPCA acknowledged and distinguished, "hyperbolic" defined once, Table 1's "differs" column made uniform

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
| R-13 | to be filled by the PM | see section below |
| R-14 | to be filled by the PM | see section below |
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

## R-13 and R-14, the readers

to be filled by the PM from the readers' returns

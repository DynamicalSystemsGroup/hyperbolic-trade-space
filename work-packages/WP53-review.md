# WP53 review: the verification record

Branch `wp53`, built on `e91fc35` (his review batch as applied in place).

## Requirements

| ID | Check | Result |
|---|---|---|
| R-1 | The abstract in cell 0 of `paper/paper.ipynb` equals `work-packages/review/abstract-draft.md`, whitespace aside | Equal. Three hyphen breaks at line wraps ("Trade-offs", "trade-off", "under-explored") are joined in the notebook to match the draft. |
| R-2 | `git diff --stat 2875c11` | The batch's files, the two generators, the ledger, the vocabulary baseline and the tests. `paper/length_ledger.toml` and `scripts/vocabulary_baseline.toml` are records the scope did not list; both follow his text. |
| R-3 | `ruff check .`, `ruff format .`, `uv lock --check` | "All checks passed!", "1007 files left unchanged", "Resolved 194 packages". |
| R-4 | `cd paper && BASE_URL=/paper myst build --html`, grep the log | No warning about a missing label, figure or citation. Remaining: `Duplicate identifier in file "fig-tension-matrix"` (a cell id that equals a figure label; present before this package, not touched). |
| R-5 | `pytest -q -m "not slow"` | 3 failed, 2065 passed, 17 skipped (below). Slow paper tests: see the end of this file. |
| R-6 | `check_residuals.py`; `check_vocabulary.py` | Exit 0; "0 new violation(s), 67 known" (10 rows added to the baseline, all his wording). |
| R-7 | `git log 2875c11..HEAD` for Co-Authored-By or generated-by | None. |
| R-8 | CI | Not in this package's reach (no push). |

## D-2 generators

`paper/figures/prior_art_layers.py` and `paper/figures/pipeline.py` write `fig-prior-art-layers.svg` and `fig-pipeline.svg` from string constants; the committed SVGs equal `svg()` byte for byte. Both are in `build_figures.PAPER_FIGURES`; `tests/test_paper_static_figures.py::test_each_drawn_svg_equals_its_generators_output` pins them.

## D-3 claims register

- Retired (sentence cut, ids never reused): C011, C036, C037, C059, C060, C061, C067, C085, C088, C089, C090, C440, C533, C562, C644.
- Reworded (same id, new fragment): C052, C057, C066, C072, C073, C075, C091, C532, C677, C683, C685, C686, C692, C799.
- Re-anchored ("Prior art, by family" to "Prior art"): C083, C529, C530, C531, C532. C802 re-anchored to "Methods" (the assumptions moved there).
- Added (C849 to C855, renumbered at the coordinator's word; C842 to C848 left to the figure branch): C849 Fulcoly citation (L, bib); C850 the soft maximum (M, L5); C851 V as function and value (M, L1); C852 the fitting problem and loss (S); C853 the Pareto boundary definition (M, L11); C854 the fitted reference surface definition (M, L5); C855 the black-box evaluation (S, interface contract).
- Not registered: the contribution sentence and the roadmap paragraph.

## Pinned test phrases changed (tests/test_paper.py)

- SECTIONS and every `_section(...)`: "Prior art, by family" to "Prior art".
- Abstract: "weakly Pareto-efficient" to "Pareto-efficient".
- Surface definition: "where the posynomial equals one" to "is the level set $V=1$ of the fit".
- Case description: the Section 1 occurrence ("cubesat model coupling power, mass and attitude control") dropped; Section 3 and Appendix C keep theirs.
- HoroPCA paragraph: "recovered the planted trade-offs ..."; the count of "hyperbolic" in Section 2 is 1; the "Appendix A" pointer assertion dropped (the sentence was cut).
- `test_the_main_results_list_ends...` and `test_the_combination_sentence...` replaced by `test_the_paper_claims_nothing_as_novel` (neither Section 1 nor 2 says the combination was absent; Section 2 has none of novel/first/new).
- `test_policy_paragraph_appears_once...` and `test_the_main_results_cite...` removed (the paragraph and the list are cut; the docsite versions of the policy tests are unchanged and pass).
- Reader depths: the main-results and organization assertions replaced by the roadmap naming every section label.
- Roadmap sentence "from its SysML v2 model" exempted in the no-tooling-names test, as the abstract is.
- c1 claims: two Section 1 assertions dropped (Main results text cut). cr7_16: the nondominated sentence now follows `sec-case-analysis`; the three-objects check reads the Definitions. "The package is the scikit-learn estimator of" replaced by the decomposition-family sentence. Figure count 10 to 12.
- Records: length ledger rows for Prior art (111), Definitions (81), Methods (147), Case analysis (60); the hand-synced `nocite-prior-art` cell rewritten from `generate_prior_art.nocite()`; the two figure directives split from their paragraphs into cells `fig-prior-art-drawing` and `fig-pipeline-drawing` (the figure test strips figure cells before looking for the reference).

## Left red (a test can pass only by changing his text, or fails without this batch)

1. `test_no_hedging_phrases_in_the_body`: "However" in Section 1 ("However, identifying how linearly independent vectors explain variance ...").
2. `test_every_figure_and_table_is_referenced_from_the_text`: `tab-families-1` has no `numref` since his rewrite removed "Table 1 lists the families ..." from Section 2.
3. `test_cr13_the_first_generated_range_says_what_varies`: the `num-participation` output reads "K = 1 to 3"; the same output is committed at `2875c11`, so the failure is not from this batch.

## Slow paper tests

`pytest -q -m slow tests/test_paper.py tests/test_paper_static_figures.py`: 1 failed, 27 passed (39 minutes). The failure, `test_cr11_chaining_with_pca_is_worked_on_the_case_in_d16`, pinned the cut Section 1 pointer to Appendix D.16; it now pins Section 2's pointer and passes alone.

The non-slow suite after the last edits: 3 failed (the three above), 2065 passed, 17 skipped, 2 xfailed.

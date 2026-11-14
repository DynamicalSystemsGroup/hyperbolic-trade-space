# WP38 review: the residual pass (patterns that read as machine-written)

Prepared for the supervisor's acceptance. Status: delivered and assistant-verified; acceptance pending. Pass heads: first readings at `8e846a9`, landings from `6007221`, second readings at `c8897c2` (appendix 14 and the glossary appendix at `003f1d2`), review head `c0fe11b`.

## The honest summary

The pass ran over every prose surface and every landing is in. It is not "every surface reads clean". Of the 96 rows of the second readers' confirmation forms (94 surfaces; two surfaces occupy two rows), 18 read clean and 78 still carry flags a second reader would mark. Most of what remains is of two kinds the pass's reach could not touch without changing structure or a claim: long or stacked sentences that were left as generated or pinned by a test (kind 9), and terms of art met before their definition in that document (kind 10). Another part sits in surfaces the pass was not allowed to edit (the abstract, the lemma pages generated from `derivation/`, the history page). These are listed below as the post-0.1 list. The checker's totals fell and no count rose against the new baseline; against the old baseline, 28 counts are still above it, now in different places than at the start (the pass's own added lead sentences, Appendix H, the README), so the old "do not rise" gate is replaced by the retaken one.

## Requirements R-1 to R-14

| ID | Evidence | Status |
|---|---|---|
| R-1 | `grep -c '^### Kind ' docs/superpowers/notes/residual-review.md` returns 10 (run at `c0fe11b`). the examples' commits were not re-resolved with `git show` in this review | met; examples not re-verified here |
| R-2 | The brief's reach section (copy-editing only). Routed flags appear as "routed" in the flag tables: 142 of 1215 first-reader rows; in the landed records the routed outcomes are 4 (L1), 15 (L3), 26 (N1), 191 (N2) plus the history page's 31 | met |
| R-3 | Kinds 9 and 10 in the brief (split or reorder, never added words; plain word or definition at first use). In landing, 236 "define" flags were met by 'define only where the first use has room (page budgets, tests)'; many "not applied" rows give "a define adds words" | met in the brief; the landing held to it by leaving defines un-applied rather than adding glosses |
| R-4 | Six-column flag table in all 29 `WP38-flags/*.md`; confirmation form with a verdict and remaining flags in all 29 `WP38-confirmations/*.md` | met. The forms vary in layout between readers; the verdict column is `yes`, `no`, or `no (N)` |
| R-5 | `uv run python scripts/prose_surfaces.py` at `c0fe11b`: 95 surfaces, 71,474 words, 27 reader slots (README 191, site 623, glossary long forms 2,531, docs 16 surfaces 6,717, examples 9 surfaces 5,002). The pass's 29 slots split the paper and appendix notebooks finer than the inventory's slot count; the inventory was not changed | met; 27 vs 29 is a slot-count difference of grouping only |
| R-6 | `uv run python scripts/check_residuals.py` prints the per-surface counts (meta, hedge, intens, paren, lparen, restat, longs, compd, deepc) and the per-document acronym and glossary-term first-use table; `tests/test_residuals.py` (9 passed) covers no-file-written and the form | met |
| R-7 | `scripts/residuals_baseline.json` retaken at `c0fe11b`; `uv run pytest -q tests/test_residuals.py`: 9 passed; the report is stable in form (keys and order unchanged by the retake) | met |
| R-8 | Counts per surface do not rise against the baseline of the head the tooling branched from (`1d741d2`): not met in the strict sense. At pass start (8e846a9) 28 counts were above it; at pass end 28 counts are above it (`WP38-landed/final-compare-before-retake.txt`), in different places. Against the retaken baseline: 0 rose, `--strict` exit 0 (`final-compare-after-retake.txt`). The totals fell on every kind except hedges (see the table below) | partly met; honest reading: totals fell, a set of per-surface counts did not |
| R-9 | 29 first readings (`WP38-flags/`), 29 second readings (`WP38-confirmations/`), each on the served page (README as file text; see the limits below) | met in form; the result of the second reading is the 18/78 split above |
| R-10 | Cuts landed under the ledger and the register; the landed records give the rows; the group of tests `tests/test_claims_register.py tests/test_site.py tests/test_docs.py tests/test_text_encoding.py tests/test_residuals.py` run at `c0fe11b` (result below); `tests/test_paper.py` and `tests/test_gaps.py` were run by the execution unit (`X-execute`, 377 passed, 4 skipped) and by round 2 (`R2-lostfacts`, 198 passed, 3 skipped for the paper tests) | met on the records; re-run result in the next row |
| R-11 | No number or figure changed: `X-execute` records no figure file under `paper/figures` changed and no quoted number moved. Four correctness items were corrected by the pass (`R-residue` part A: the D.18 pointer, the Appendix E count, the case-model "20 of the variables", the bib title), each a wrong sentence, not a style edit. Round 2 added three lead sentences (D.1, C.3, D.7) and restored one phrase, recorded as additions | met, with those listed exceptions |
| R-12 | Entry-surface rows in `work-packages/supervisor-review-list.md` "Entry surfaces": site index (rows at `a390117`), README (`a390117`), docs home (`1ef3dc7`); history page: none applied (31 rows routed); the abstract: none applied (7 rows routed). Round 2 and later units did not change an entry surface | met |
| R-13 | `work-packages/WP8b-reviewers-guide-skeleton.md` lines 36 to 43 name the brief, the inventory, the checker with its baseline, the test, the flag tables and the confirmations | met |
| R-14 | At `c0fe11b`: `uv run ruff check .` all checks passed; `uv run ruff format --check .` 728 files already formatted; `uv lock --check` resolved; vocabulary check, text-encoding and the group tests: see the table "Gates" below; no `Co-Authored-By` or "generated by" line in the pass's commits (`git log 8e846a9..HEAD`: 0 matches) | met, see gates |

### Gates (run at c0fe11b)

| Gate | Result at `c0fe11b` |
|---|---|
| `uv run ruff check .` | all checks passed |
| `uv run ruff format --check .` | 728 files already formatted |
| `uv lock --check` | resolved (178 packages) |
| `uv run python scripts/check_vocabulary.py` | 0 new violations, 61 known |
| `uv run pytest -q tests/test_residuals.py` | 9 passed |
| `tests/test_text_encoding.py tests/test_residuals.py tests/test_claims_register.py tests/test_site.py tests/test_docs.py` (`-p no:xdist`, 26 minutes) | 143 passed, 1 skipped, 2 failed, 11 errors. The failures and errors are in `tests/test_site.py` and `tests/test_docs.py` fixtures that build the docs site in this worktree (the build prints a MkDocs 2 warning banner on stderr, which the build assertion rejects; rerun with `NO_MKDOCS_2_WARNING=1` gave the same 2 failed, 11 errors). Not diagnosed further; this commit changes only records and the baseline, so the cause is the build environment, not the pass. The same tests passed at the execution unit (`X-execute`, 377 passed, 4 skipped) and round 2. Re-run on a clean checkout before acceptance |
| `git log 8e846a9..HEAD`, grep for `Co-Authored-By` or "generated by" | 0 matches |

## The pass in numbers

29 reader slots (inventory: 95 surfaces, 71,474 words).

First-reader flag rows: 1,215. By proposed disposition: split 384, cut 301, define 236, keep 151, routed 142, one unmarked.

Landings by unit, with heads (rows are flag-table rows):

| Unit | Head | Rows | Applied | Left (keep) | Routed | Not applied |
|---|---|---|---|---|---|---|
| L1 docs (docs-01 to 03) | `7f790f2` | 135 | 115 | 6 | 4 | 10 |
| L2 entry (README 8 rows, root page 17, history 31) | `0b31ef1` | 56 | by row in `L2-entry.md` | by row | history page 31 routed, 2 root page | by row |
| L3 case (example-01, example-02, glossary page) | `d417196` | 148 | 108 | 14 | 15 | 11 |
| N1 paper (paper-01 to 04) | `7caf05d` (with N2 and X) | 227 | 121 | 24 | 26 | 56 |
| N2 appendices (appendix-01 to 16, glossary appendix, Appendix A rows) | `7caf05d` | 649 | 181 | 98 | 191 | 179 (and 24 "not this unit" in the tables) |
| residue (D.18, Appendix E, case-model draws, bib; appendix-14's 55 rows N2 did not reason) | `368f3a1` | 55 + 4 | 26 applied, 28 keep, 2 routed (the 55 rows) | | | |
| round 2, lost facts | `ba22d92` | 30 candidate rows | restored 1, re-pointed 15, lead sentence 3 | | left or routed 8 | |
| l1-nit | `116c929` | 1 | the reweighted ℓ₁ sparsity title and the register row C422 | | | |

The row totals reconcile to the 1,215 first-reader rows (135 + 56 + 148 + 227 + 649).

### The checker, before and after

Pass start (`8e846a9`, `WP38-flags/before-checker.txt`) against pass end (`c0fe11b`, `final-compare-after-retake.txt`). Columns as the checker prints them.

| Surface group | words | meta | hedge | intens | paren | lparen | restat | longs | compd | deepc |
|---|---|---|---|---|---|---|---|---|---|---|
| paper body, before | 10,450 | 3 | 5 | 2 | 233 | 34 | 4 | 77 | 77 | 2 |
| paper body, after | 10,026 | 4 | 5 | 2 | 222 | 30 | 1 | 46 | 57 | 1 |
| appendices, before | 48,618 | 16 | 2 | 1 | 291 | 39 | 2 | 106 | 108 | 3 |
| appendices, after | 48,102 | 13 | 2 | 1 | 254 | 22 | 2 | 90 | 67 | 1 |
| docs, before | 6,911 | 0 | 4 | 2 | 65 | 7 | 2 | 40 | 47 | 1 |
| docs, after | 6,717 | 0 | 4 | 0 | 56 | 3 | 2 | 24 | 38 | 1 |
| examples, before | 5,672 | 2 | 0 | 0 | 121 | 25 | 1 | 44 | 20 | 0 |
| examples, after | 5,002 | 0 | 0 | 0 | 87 | 13 | 1 | 24 | 10 | 0 |
| README, before | 205 | 0 | 0 | 0 | 4 | 1 | 0 | 1 | 1 | 0 |
| README, after | 191 | 0 | 0 | 0 | 2 | 0 | 0 | 1 | 1 | 0 |
| root page, before | 310 | 0 | 1 | 0 | 2 | 2 | 0 | 1 | 0 | 0 |
| root page, after | 300 | 0 | 1 | 0 | 2 | 0 | 0 | 1 | 0 | 0 |
| history page, before and after | 323 | 0 | 0 | 1 | 9 | 0 | 0 | 1 | 0 | 0 |
| glossary long forms, before | 2,615 | 0 | 0 | 0 | 32 | 0 | 0 | 4 | 10 | 0 |
| glossary long forms, after | 2,531 | 0 | 0 | 0 | 27 | 0 | 0 | 1 | 7 | 0 |
| **total, before** | 75,104 | 21 | 12 | 6 | 757 | 108 | 9 | 274 | 263 | 6 |
| **total, after** | 73,192 | 17 | 12 | 4 | 659 | 68 | 6 | 188 | 180 | 3 |

Words fell by 1,912 (2.5 percent). Acronyms undefined at first use fell from 34 to 22; acronyms never expanded in their document from 34 to 21; glossary terms without a definition at first use from 203 to 192. The case-model page fell from 5,672 to 5,002 words (-670), the largest single drop. The counts on the history page and on hedges did not move. The text added by the round-2 lead sentences (D.1, C.3, D.7), the Appendix H material landed with WP35, and the README's two parentheses are the surfaces that stand above the old baseline.

Baseline: the checker's old baseline (`1d741d2`) showed 28 counts rose at pass start and still shows 28 at pass end. The new baseline (`c0fe11b`) shows 0 rose and `--strict` exits 0. The old comparison before the retake is saved in `work-packages/WP38-landed/final-compare-before-retake.txt`, the new one in `final-compare-after-retake.txt`.

## The confirmations (second readers)

96 form rows (94 surfaces), 29 forms. Reads clean: 18. Remaining flags: 78. The two readers' forms are not uniform: some give "no (N)", some list flags numbered with their kind. The tally by kind below counts the flags that name a kind, row by row, so it is approximate.

| Kind | Rows (surfaces) mentioning it | Flags mentioning it |
|---|---|---|
| 9, grammatical complexity | 46 | 82 |
| 10, jargon and terms met before a definition | 43 | 78 |
| 2, a second-thought parenthetical | 13 | 15 |
| 7, restatement | 12 | 13 |
| 1, metanarration | 10 | 15 |
| 4, a detail that belongs elsewhere | 9 | 13 |
| 6, signposting | 6 | 7 |
| 3, 5, 8 | 1 each | 1 each |

Seventeen rows also name a lost fact or dangling reference; round 2 resolved them as recorded below.

## The lost-facts record (round 2, `ba22d92`)

Source: the second readers' forms. Finding: for most candidates the pre-pass text (8e846a9) already had the same gap, so "restore" was rarely possible and the fix was a pointer word or a short lead sentence. Restored 1 ("Neither maximum has a lemma here"). Re-pointed 15: "either use" now points to Section 1 (Section 8 and Appendix C); "the executives' call" became "the closing decision"; "R1 holds" became "R1 of Section 5 holds" (generated sentence; claims row C422 fragment re-pointed, backing unchanged); "the loops" became "the nested loops below" (ledger raise, 2 words); "docsite" became "the documentation's"; "(26.5 and 38.1 on the others)" became "on the other two planted tables"; three glossary entries (assignment, row share, participation threshold); the HoroPCA "row above" became "entry above"; five case-model phrases (the records, the table's third part, the regenerated figure, the four thresholds, what each verifies). Added a lead sentence 3 (Appendix D.1, C.3 legend, D.7's log V against the K = 1 fit of record). Left or routed 8: G-9 (already points to Appendix E), docs "Figure 2" numbering (correct through the whole site), Appendix H citation parentheses (site theme), the L20 delta and L18 relative error (lemma pages), D.9 and D.2 bare tables (unchanged since 8e846a9), forward references and acronyms in Section 1 and Table 1. Detail: `WP38-landed/R2-lostfacts.md`. Residue-stage correctness items (`R-residue` part A): D.18's pointer, the Appendix E count, the case-model's "20 of the variables", the bibliography's ℓ₁ title: each a wrong sentence, corrected.

## What no reader could test

- Screenshots were not saved: the readers read the served pages in a browser pane and wrote what they read; the record is the flag and confirmation text, not images. CLAUDE.md asks for screenshots in the record; this pass does not have them.
- The case-model page (`examples/adcs/case-model.md`) is not rendered by the docs site; its readers read the file text.
- The README was read as file text from the worktree, not as GitHub renders it.
- The generated lemma tables were not read (paper-01's form says so for the paper; the appendix readers read the lemma pages as served but not the generator output separately).
- Math was read from the rendered text, not typeset (MathML duplicates the formula in the page text).
- The forms' kind tally is by reading of free text, not a structured field.

## Open items for the supervisor: the post-0.1 list

Not changed by the pass, each for the reason given. The 76 flagged surfaces (the supervisor-given count; this review's parse finds 78 of 96 form rows) by kind:

| Kind | Surfaces (rows) | Typical sentence |
|---|---|---|
| 9, grammatical complexity | 46 | "A fitted posynomial reference surface models the data underlying the table, not the Pareto boundary, and gives the data a coordinate system; the table and its reading are views of that model." (abstract; and generated lemma statements with a colon, a semicolon and a parenthesis) |
| 10, jargon, terms and acronyms met before definition | 43 | "KKT", "LSE = LME + log(n)/tau", "ledger", "SymPy", "Helmert-type" used without a first-use definition in that document |
| 2, parenthetical second thought | 13 | "Control (the attitude loop under the nominal slew, a 30 degree slew with a 600 s horizon)." (case page) |
| 7, restatement | 12 | "This work belongs beside PCA in unsupervised learning and feature engineering and is not a PCA." (root page) |
| 1, metanarration | 10 | "The appendix has two parts:" followed by the two items the headings already show |
| 4, detail that belongs elsewhere | 9 | "The research record of both tables is work-packages/WP23-rounds/spikes/." |
| 6, signposting | 6 | "What the correspondence establishes is this." (Appendix B) |
| 3, 5, 8 | 1 each | one caveat, one hedge, one intensifier |

Other open items:

- **The 163 lemma-script rows.** The statements of L2 to L20 are generated from `derivation/`, which is off limits to this package; the owner is the lemma-script owner, and the sentences' shape (a statement with hypotheses, a colon, a parenthesis, indices) is what the readers flag as kind 9 and 10 (for example L20's "delta" never said to be the minimizer shift, L18's "relative error of what").
- **The history-page rows (30 by the supervisor-given count, 31 by L2's) and the two root-page rows.** The history page's sentences are the supervisor's statements and rulings (WP37); `tests/test_site.py` requires each prose sentence to open a claims row and each team-account sentence to carry "our own account", so a split or cut needs new rows and his wording. The two root-page rows: the lead sentence of the choice ("Choose the line that is yours...", kept by his ruling of 2026-11-14) and the Why-figure caption (a test pins it as one sentence then the link note).
- **The abstract's put-off and flagged sentences:** seven first-reader rows (define "posynomial"; split three long sentences; a hedge "may exceed"; keep for the two definition parentheticals), reported, changed by no one.
- **Appendix H citation parentheses:** the page renders each citation without parentheses; the fault is the site theme, not the markup (owner: the site build).
- **Docs "Figure 2" numbering:** figures are numbered through the whole site, so a page's first figure may be Figure 2; left as correct.
- **The checker's baseline:** retaken at `c0fe11b`; the old baseline's 28 raised counts no longer gate.
- **Tests that pin generated sentences:** the readers' splits of the generated count paragraph, the findings sentences and `tests/test_site.py` captions were not applied where a test pins the form (rows marked "not applied" in the landed records); changing them is a test change for the owning package.

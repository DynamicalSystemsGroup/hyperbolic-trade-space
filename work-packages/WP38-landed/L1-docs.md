# WP38 landed record, unit L1-docs

Slots docs-01, docs-02, docs-03 (135 flag rows). File set: `docs/*.md`, `docs/user-guide/*.md`. Branch `wp38docs`, from dev at 6007221.

## Counts by disposition

| Slot | Rows | Applied | Left (keep) | Routed | Not applied |
|---|---|---|---|---|---|
| docs-01 | 54 | 43 | 2 | 2 | 7 |
| docs-02 | 58 | 52 | 2 | 2 | 2 |
| docs-03 | 23 | 20 | 2 | 0 | 1 |
| Total | 135 | 115 | 6 | 4 | 10 |

Prose words in the file set: 8,949 to     8753 (by `wc`; getting-started is at its budget of 348 by the site test's count).

## Not applied, left, routed

| Surface | Flag | Outcome | Why |
|---|---|---|---|
| docs/index.md | split "which metrics contend, with what elasticity, ..." | not applied | the split lost the checker's definition cue for elasticity and metrics (terms undefined at first use 4 to 6; R-8) |
| docs/index.md | define "posynomial ... a term (a product of powers of the metrics)" | not applied | removing the parenthetical lost the cue for term and metrics (same count, R-8); the gloss is the page's only definition of a term |
| docs/theory.md | cut opening "For a reader who wants the model stated in one place" | not applied | page-purpose line each page opens with; with the closing line cut it is the only pointer to the paper's proofs |
| docs/theory.md | define "sum-zero subspace", "Helmert log-ratio basis" | left | the stated reader level (calculus, linear algebra, convex); a glossary link adds no content |
| docs/getting-started.md | define "uv" ("a Python package manager") | not applied | `tests/test_site.py::test_word_budgets_hold`: the page's budget is 348 words and the gloss put it 11 over; the three other glosses and splits were trimmed to fit, the uv gloss went |
| docs/theory.md | define "energy differential (level offset)" to one name | not applied | `tests/test_docs.py::test_register_phrases_present` requires the phrase "energy differential" in the prose (notation register); chart and overview took the shorter "level offset" |
| docs/further-reading.md | cut "how this work differs" | not applied | it is the link text naming the paper section it opens |
| docs/user-guide/conditioning.md | cut "they show whether the story is sensible" | not applied | claims row C248 (kind P, "None proves a conditioning right.") would fall under the six-word fragment minimum; the clause carries the row |
| docs/user-guide/tensions.md | cut "(`closure_note` says so)" | not applied | the one place the page names the field |
| docs/user-guide/termination.md | cut "level 3 holds" in the worked example | not applied | the earlier restatement ("Level 3 holds whenever gamma is positive") was cut instead; one statement stays |
| docs/examples.md | keep "The triples show how to read the figure; they are not findings." | left (keep) | |
| docs/user-guide/choosing-k.md | keep colon sentence on PCA limits | left (keep) | |
| docs/user-guide/fitting.md | keep term ordering rule | left (keep) | specification |
| docs/user-guide/overview.md | keep "Where the method misleads ..." | left (keep) | |
| docs/user-guide/termination.md | keep "Hessian, covariance, eigenvalue" | left (keep) | reader level |
| docs/user-guide/termination.md | keep "Keep three claims apart." | left (keep) | |
| docs/api-reference.md | docstring `term_temperature` split | routed | generated from `src/` docstring; owner of the estimator docstrings |
| docs/api-reference.md | docstring `temperature` "LP" | routed | same |
| docs/user-guide/limitations.md | "A proof in a theorem prover ... certificates" | routed | claims register (owner: claims review); a hypothetical about a tool the page does not use, backed by `abstraction-gaps.md` |
| docs/user-guide/tensions.md | `1e-12` numerical-zero constant (participating) | routed | a number; owner: whoever holds the constants record |

Partial applications: "level offset" alone for "energy differential (level offset)" on chart and overview (the glossary lists both); fitting "tol" glossed as "the accepted error in `frac_above_`" (the "exact-relation table" clause is left as written, backed by the page's test); termination "The second" kept in its sentence order because claims row C376 and the checker's cue for "certificate" read it; `log-convex` swapped for "convex in log space" on the chart page; chart "wanted, feasible or safe" cut to "good".

Test pin updated: `tests/test_docs.py::test_examples_page_case_numbers_are_the_computed_record` named three phrases of the examples page by their old wording; the list now carries the new wording ("contending set of seven metrics that trade off", "The larger adds peak slew power ..."), the numbers unchanged.

Entry surface: `docs/index.md` changed (PCA expanded in the first bullet; the closing navigation line cut: the menu shows those pages). Listed in `work-packages/supervisor-review-list.md`, "Entry surfaces".

Beyond the table (noted by docs-01): bibliography entry 7 of `docs/further-reading.md` renders "Enhancing sparsity by reweighted \ell_1 minimization" with a markup fault in the reference source; passed to the owner of `docs/references.bib`, not edited.

## Claims register

Re-pointed (fragment moved to the surviving text, backing unchanged): C165 (restored to its original text), C174, C177, C184, C195 (restored), C196, C198, C204, C215, C218, C219, C220, C225, C227, C235, C239, C242, C257, C264, C270, C273, C275, C276, C278, C279, C288, C315, C325, C331, C347, C349, C350, C375, C376, C377, C379, C381, C383, C385, C427, C444, C490.

Retired (the sentence is cut; each row's backing is a test, lemma or note that stays): C030 (fielded-system caveat), C176 (closing pointer line), C266 ("Both are seeded and used throughout these pages"), C319 (predicted position inherits the error), C345 (maximizer efficient, converse not claimed; L11 stands in the derivation), C353 (the glossary and paper define "hyperbolic"), C380 (a cap on a table that never reaches the slope).

No ledger row changed (no paper text in this unit).

## Checker, per surface, baseline (head 1d741d2) to now

`uv run python scripts/check_residuals.py --compare scripts/residuals_baseline.json`: no count of any docs surface rose; the 28 counts above baseline are the other units' text (WP39, WP35, WP40). Changed counts only:

| Surface | Counts | Terms undefined at first use | Acronyms undefined |
|---|---|---|---|
| `docs/api-reference.md` | words 296->288 ; parens 7->6 ; long_parens 1->0 | 15 -> 14 | 1 -> 1 |
| `docs/examples.md` | words 651->600 ; parens 5->2 ; long_parens 1->0 ; dense_paras 1->0 ; long_sentences 4->2 | 9 -> 8 | 0 -> 0 |
| `docs/further-reading.md` | words 188->182 | 1 -> 1 | 1 -> 0 |
| `docs/getting-started.md` | no change | 10 -> 9 | 0 -> 0 |
| `docs/index.md` | words 205->193 | 4 -> 3 | 1 -> 1 |
| `docs/theory.md` | words 595->575 ; parens 7->5 ; long_parens 1->0 ; long_sentences 4->1 | 12 -> 12 | 0 -> 0 |
| `docs/user-guide/chart.md` | words 513->508 ; intensifiers 1->0 ; parens 5->3 | 15 -> 15 | 0 -> 0 |
| `docs/user-guide/choosing-k.md` | words 556->542 ; long_sentences 3->2 | 3 -> 3 | 1 -> 1 |
| `docs/user-guide/conditioning.md` | words 579->576 ; long_sentences 1->0 ; compound 2->1 | 8 -> 8 | 0 -> 0 |
| `docs/user-guide/fitting.md` | words 617->614 ; parens 9->8 ; long_parens 2->1 | 18 -> 16 | 0 -> 0 |
| `docs/user-guide/index.md` | no change | 0 -> 0 | 0 -> 0 |
| `docs/user-guide/limitations.md` | words 487->443 ; intensifiers 1->0 | 1 -> 1 | 0 -> 0 |
| `docs/user-guide/overview.md` | words 393->388 ; parens 3->2 ; long_sentences 3->2 | 9 -> 9 | 1 -> 0 |
| `docs/user-guide/prediction.md` | words 226->212 ; long_sentences 2->1 | 5 -> 4 | 0 -> 0 |
| `docs/user-guide/tensions.md` | words 571->560 ; parens 8->7 ; long_parens 1->0 ; long_sentences 4->1 ; compound 5->1 | 12 -> 11 | 1 -> 0 |
| `docs/user-guide/termination.md` | words 710->703 ; long_sentences 5->1 ; compound 8->4 | 10 -> 10 | 0 -> 0 |
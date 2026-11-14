# WP38 landed: L2-entry (readme-01, site-01)

Branch wp38entry. Copy edits only. Dispositions per flag row; counts at the end.

## readme-01 (8 rows)

| Row | Disposition |
|---|---|
| line 3 first sentence | applied (split into two sentences, "See the docs, the paper and ... for a case study") |
| line 11 package-only comment | left (keep) |
| line 25 `select_temperature` comment | left (keep) |
| line 32 `docs/superpowers/` clause | applied (cut) |
| line 41 `work-packages/` list | applied (cut; the clause "not needed to use the method" kept) |
| line 44 build-files bullet | applied (split into two bullets) |
| line 44 housekeeping names | not applied: WP40 D-6 requires every top-level entry named in the Layout; the names stay, the bullet is shorter and split |
| line 43 CLAUDE.md | left (keep) |

## site-01 (index.html, 17 rows; history.html, 31 rows)

index.html
- line 117 summary: left (keep). line 137 PCA: applied (define, "Principal component analysis (PCA)"). n-lemma sentence: left (keep).
- line 139 split: applied. line 140 parenthetical: applied (own sentence). "kin": applied (define, plain words). line 141 parenthesis: applied (split); "so it drops into the same workflows": applied (cut).
- figcaption 1 (line 130): not applied: tests/test_site.py pins the caption as one sentence then the link note (`cap.count(". ") == 1`); a split needs the test and the supervisor's word. Routed to the supervisor. Instruction on figure 1: left (keep); on figure 2: applied (cut). Figure 2 caption: left (keep).
- line 151 lead sentence ("Choose the line that is yours ..."): not applied: the supervisor's ruling of 2026-11-14 keeps the lead sentence and the two doors; routed to the supervisor (cut or split on his word).
- line 123 split: applied. "usually": routed (claims owner; C357 untouched). line 124: applied (idiom swapped, "must meet three conditions").

history.html (all 31 rows): none applied; routed to the supervisor, for these reasons. The page's prose is the supervisor's own statement of purpose and rulings (WP37-decisions.md: the Penland and Clark clauses, "our own account" marks, "people and the human lineage"); `tests/test_site.py` requires each prose sentence to open a claims-register row and each team-account sentence to carry "our own account" or "the same account", so a split, a cut of the mark, or a define that adds link text needs new rows and the supervisor's decision on the wording. A split of the cadCAD sentence was tried and reverted (test_history_every_prose_sentence_has_a_row_in_the_claims_register failed on the new sentence). The generated "Dated references" list was not touched. Routed rows by kind: splits 16, cuts 15 (the five "in our own account" marks, "human lineage", "synthesis effort", "special cases ...", the ICMS acronym, others), defines 11 (MAIDs, GDS, MSML, RAI, ICMS, NumFOCUS, OpenMBEE, cadCAD, geometric programs, "firm post", "formal methods"), keeps 1 (Shorish/Paruch line).

## Counts (by row, the two slots)

Applied 12 (readme 4, index 8). Left (keep) 8 (readme 3, index 4, history 1). Routed 33 (history 30, index 3: the lead sentence and the figure caption to the supervisor, "usually" to the claims owner). Not applied 1 (readme housekeeping names, WP40 D-6). The flag tables' own totals are 8 rows (readme) and 48 (site); a table row that groups two edits is one row here.

## Checker (scripts/check_residuals.py --compare scripts/residuals_baseline.json)

Columns: words, meta, hedge, intens, paren, lparen, restat, longs, compd, deepc.
Before (dev 6007221): README.md 205 0 0 0 4 1 0 1 1 0; site/index.html 310 0 1 0 2 2 0 1 0 0; site/history.html 323 0 0 1 9 0 0 1 0 0.
After: README.md 191 0 0 0 2 0 0 1 1 0; site/index.html 299 0 1 0 2 0 0 0 1 0; site/history.html 323 (unchanged: the trial edit was reverted) 0 0 1 9 0 0 1 0 0.
The README's and the index's above-baseline lines (parens, compound) are gone or reduced; history.html is unchanged.

## Claims rows re-pointed (fragment text only; backing and kind unchanged)

C355, C356, C360, C361 (site/index.html). C357, C358 and C359 unchanged. No ledger row (no paper text).

## Tests

tests/test_claims_register.py, tests/test_docs.py, tests/test_text_encoding.py, tests/test_site.py, vocabulary check, ruff: see the report.

# WP38 landed record: R2-lostfacts (sentences the pass's cuts lost, and dangling references)

Branch wp38r2, from origin/dev at 2a12f7f. Source: the second readers' confirmation forms in `work-packages/WP38-confirmations/` (27 files). Scope: lost facts and dangling antecedents only; style flags (kinds 1 to 9) are not touched. Comparison text: the pre-pass commit 8e846a9.

One finding that changes the brief: for most candidates the pre-pass text had the same gap ("either use", "the executives' call", "R1 holds", "gap G-9", the 26.5 and 38.1 numbers, the D.1 and C.3 tables with no lead sentence, D.7's log V). Nothing was cut that carried the antecedent; the gap was always there. So "restore" is rarely possible and the fix is a pointer word or a short lead sentence.

## Decisions

| Row (source form) | Decision | What and why |
|---|---|---|
| Section 8 "either use" (paper-03) | re-point | The antecedent is Section 1's "two uses: design optimization ... and configuration management". Added the pointer "(Section 1)" after "either use" (numref to sect-problem), also in Appendix C's Job line (appendix-11). 8e846a9 had the same phrase. |
| Section 9 "the executives' call" (paper-03) | re-point | The two executives are introduced only in the closing paragraph; the opening now says "the closing decision" (same word count). |
| Section 9 "R1 holds on both regimes" (paper-03) | re-point | R1 is a Section 5 condition; the generated sentence (generate_findings.k1_sentence) now reads "R1 of Section 5 holds ...". Claims row C422's fragment re-pointed; backing unchanged. |
| Section 9 "gap G-9" (paper-03) | left | The sentence already points to Appendix E, the gaps ledger named in Section 3, where G-9 is a row; the pre-pass text was the same. |
| Search section "the loops" (paper-02) | re-point | The sentence that introduced the loops was never before it; "enters the loops" now reads "the nested loops below" (ledger raise, 2 words). 8e846a9 opened the next paragraph with "There are nested loops"; that sentence stays cut (it said what the three sentences after it say). |
| Search section "Neither case has a lemma here" (paper-02) | restore | 8e846a9: "neither has a lemma here", after the exact and the soft maximum; now "Neither maximum has a lemma here" (same word count as "Neither case"). |
| Methods "the docsite's Conditioning page" (paper-02) | re-point | "docsite" is the documentation; swapped to "the documentation's" (word-neutral). |
| docs choosing-k "(26.5 and 38.1 on the others)" | re-point | The others are the two other planted tables of the planted-table block (the text has no more detail; 8e846a9 identical): "on the other two planted tables". |
| docs fitting "Figure 2" with no Figure 1 (docs-02) | left | The docs number their figures through the whole site (Figure 1 on getting-started, 3 on tensions, 4 on chart); Figure 2 is correct there. |
| glossary "assignment" (glossary-01) | re-point | "the labels" had no antecedent; now "At the default (infinite), the assignments drive the refit." |
| glossary "row share" | re-point | "the record's bound" now "the termination record's bound" (the parenthetical naming it was cut by the pass). |
| glossary "participation threshold" | re-point | "participates in the tension" (the glossary has no entry "tension") now "counts as participating", the formal field's own words. |
| Appendix D.1 bare tables (appendix-11) | add lead (not a restoration) | 8e846a9 had no lead sentence either (no commit ever did); the generator now opens with one sentence naming the columns and how the fit temperature is chosen (target fraction 0.10, from the case spec; Section 8 states the selected values). Words counted in the Appendix D raise row. |
| Appendix C.3 legend (appendix-11) | add lead (not a restoration) | Same: no earlier text. One sentence names the four flags and the two count columns (from `cubesat_model.py`'s flag definitions and `feasibility_table`'s docstring). |
| Appendix D.7 log V values vs table (appendix-12) | add lead | The prose quotes log V against the fit to the designs that meet the four thresholds; the table scores against the K = 1 fit of record (`candidate_designs` docstring). One sentence says so; no number changes; 8e846a9 had the clash. |
| Appendix G "The HoroPCA row above" (appendix-16) | re-point | The register (G.1) has the HoroPCA entry; the reader saw one subsection; "row above" now "entry above". |
| Appendix H "HoroPCA Chami et al., 2021 carries" (appendix-16) | left (routed, site theme) | The citation is `[@chami2021horopca]`, a parenthetical cite; the served page renders every cite in the book without parentheses (class "cite-group parenthetical"), so the fault is the site theme, not the markup. Owner: the site build. |
| L20 "delta" never said to be the minimizer shift (appendix-10) | left (routed) | Lemma page statement generated from `derivation/`; owner the lemma-script owner. L18 "relative error of what" likewise. |
| Appendix D.18 "The last column shows where noise lifts one" (appendix-13) | already fixed | The pass's generator text now reads "the overlap of the contending set with the clean fit's, shows where noise changes it"; the form read the earlier output; this execution refreshes it. |
| Appendix D.9, D.2 bare tables (appendix-12) | left | Unchanged by the pass (the cells are identical in 8e846a9); not provably lost. |
| examples case-model "the records" (example-01) | re-point | "what the paper and the records cite": "the records" names nothing; now "what the paper cites". |
| case-model "Verification definitions name what each verifies" | re-point | now "name the requirement each verifies". |
| case-model "The table's third part" | re-point | "The coverage table's third part" (the coverage table has three sections). |
| case-model "The regenerated figure checks it" | re-point | "The paper's regenerated temperature figure". |
| case-model "The four thresholds" | re-point | "The four performance thresholds", the paper's term. The two cost limits and the battery sentence are left (no earlier text; adding shares would be new content). |
| paper-01 "Numerical" and "Q1 to Q4" in Main results | left | Forward references to Section 6, which names them; not cut. "tau", "kappa" in the assumptions, "MBSE" in Table 1 (spelled out in the same row), "scalarization", "seam": definitions that would add words; out of scope. |
| README, site, docs-01 (other pages), examples-02 | left | Forms report no lost fact. |

## Files and ledger

Ledger: one raise row, Search of the design space (preliminary), +2 words ("the nested loops below"); the other edits are word-neutral or inside their ceilings; the appendix lead sentences (D.1, C.3, D.7) are outside the counted body sections.

Changed: `paper/paper.ipynb`, `paper/supporting_material.ipynb` (sources, then both executed once), `paper/generate_findings.py`, `paper/generate_results.py`, `paper/generate_model.py`, `paper/figures`, `glossary.yaml`, `docs/user-guide/choosing-k.md`, `examples/adcs/case-model.md`, `claims_register.toml` (C422 fragment), `paper/length_ledger.toml` (raise rows below).

## Counts

Restored 1 (Neither maximum has a lemma here), re-pointed 15 (either use twice counted as one row, closing decision, R1, nested loops, documentation, 26.5 and 38.1, three glossary entries, HoroPCA entry, and five case-model phrases), added a lead sentence 3 (D.1, C.3, D.7), left or routed 8 (G-9, Figure 2, Appendix H citation parentheses, L20 delta and L18, D.9 and D.2, forward references and acronyms in Section 1 and Table 1, remaining pages with no lost fact).

## Checks

Both notebooks executed with the paper group (the first run used an unwarmed MPLCONFIGDIR and left a font-cache stderr line in paper.ipynb; paper.ipynb alone was executed again with a warmed directory; supporting_material.ipynb is from the first run). Group tests/test_paper.py tests/test_claims_register.py tests/test_site.py tests/test_docs.py tests/test_text_encoding.py tests/test_residuals.py tests/test_gaps.py with `-p no:xdist`: 377 passed, 4 skipped, 1 failed (the font-cache stderr line); after the second execution tests/test_paper.py: 198 passed, 3 skipped. ruff check and format clean, `uv lock --check` clean, `scripts/check_vocabulary.py`: 0 new violations. The residual checker's comparison against the pre-pass baseline is unchanged in kind by this unit: the added lead sentences raise the paren and compound counts of D.1, C.3 and D.7 by one or two each; the comparison text is in the unit's scratch record.

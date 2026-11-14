# WP38 R-residue: correctness items and the second pass on Appendix E
## Part A: correctness

1. Appendix D.18 pointer: WRONG (overclaim). The last column is the contending-set Jaccard; it moves when noise changes the set (a lift or a drop), so 'shows where noise lifts one' named neither the column nor what it shows. Reads now 'The last column, the overlap of the contending set with the clean fit's, shows where noise changes it.' (paper/generate_results.py; output regenerated).
2. Appendix E count: WRONG ('G-1 to G-17', table runs to G-18). The typed range is cut from the job block; tests/test_paper.py::test_appendix_e_job_block_types_no_gap_range pins that no range is typed and that the table's ids are G-1 to G-n in order. The docstring of paper/generate_gaps.py no longer types a range.
3. examples/adcs/case-model.md '20 of the variables': WRONG. SHARED_COUNT = 20 in examples/adcs/experiments/definitions.py is the number of designs drawn; the shared variables are three (wheel class, tracker grade, Kp). Reads 'There are 20 draws, over the variables the two variants share.'
4. docs/references.bib candes2008enhancing: WRONG on the docs page (mkdocs-bibtex rendered the title's math as a doubled-backslash MathJax string, which does not typeset). The title now uses the Unicode glyphs for ell-one; the built docs/further-reading page shows 'reweighted ℓ₁ minimization'. No reference, DOI or URL changed. The paper's references take the same BibTeX title and read it as plain text (not separately rendered here; the myst build is not part of this unit).

## Part B: the 55 rows of appendix-14 that N2 did not reason (disposition per row)

Row numbers are those of work-packages/WP38-flags/appendix-14.md. Rows N2 settled are listed with 'N2'.

| Row | Flag | Disposition | Note |
|---|---|---|---|
| 1 | cut | routed | the Job / three-tier frame is shared by every appendix and test_each_appendix_opens_with_its_job_and_three_tiers pins the three tiers |
| 2 | routed | applied | Part A2: the typed range cut (the block names no count; a test pins that no range is typed and that the table's ids run G-1 to G-n) |
| 3 | cut | routed | same as row 1 |
| 4 | split | keep | the trailing 'test' is the link label link_paths makes of the test path; the sentence is complete without it |
| 5 | split | applied | N2 |
| 6 | keep | keep | N2 |
| 7 | split | applied | N2 |
| 8 | define | keep | 'simplex' is a glossary term; a define adds words |
| 9 | define | applied | N2 |
| 10 | split | applied | N2 |
| 11 | keep | keep | N2 |
| 12 | split | keep | a split needs a new subject for the counts of participants; adds words |
| 13 | split | keep | parentheses hang on generated link labels; the two findings are the evidence of two tests |
| 14 | keep | keep | N2 |
| 15 | split | applied | N2 |
| 16 | split | applied | G-3: split at the semicolon |
| 17 | define | keep | the codes are the lemma codes of Appendix B and the ledger; a gloss adds words |
| 18 | define | applied | N2 |
| 19 | split | keep | the parenthesis is one item of a list of things that cannot be proved; promoting it would break the list |
| 20 | keep | keep | N2 |
| 21 | cut | applied | N2 |
| 22 | split | applied | N2 |
| 23 | split | applied | N2 |
| 24 | cut | applied | N2 |
| 25 | keep | keep | N2 |
| 26 | keep | keep | N2 |
| 27 | define | applied | G-5 title: 'masking in the fit' swapped for 'rows left out of the fit' (plain word) |
| 28 | split | applied | N2 |
| 29 | keep | keep | N2 |
| 30 | split | applied | N2 |
| 31 | keep | keep | N2 |
| 32 | define | keep | 'support function' and 'chart' are glossary terms |
| 33 | split | applied | N2 |
| 34 | cut | applied | G-6: the ungrammatical provenance aside reads 'with bench_oracle.py in that folder'; the source stays |
| 35 | keep | keep | N2 |
| 36 | split | keep | the history aside is the reason seeds with fewer than d+1 rows appear next to a generator that guarantees d+1 |
| 37 | cut | applied | N2 |
| 38 | split | applied | G-7: reordered, the qualifier first |
| 39 | split | applied | G-8: three sentences |
| 40 | define | keep | 'half-step', 'step B', 'step D' are the method's words, defined in the main text; a gloss adds words |
| 41 | cut | keep | bare 'test' labels are generated link labels; each carries a path |
| 42 | cut | applied | G-8: 'with first-order diagnostics' cut (the second clause says it) |
| 43 | split | applied | G-9: split at the semicolon |
| 44 | define | keep | 'near-frontier' is a glossary term |
| 45 | split | applied | G-9: three sentences |
| 46 | split | applied | G-9: the data list is four short sentences, no word added |
| 47 | split | keep | 'RECORD' is a generated link label for the test's record constant |
| 48 | define | keep | 'objective_' is the attribute name of the API, the object's name |
| 49 | split | applied | G-10: three sentences |
| 50 | define | applied | G-10: 'measure-zero' swapped for 'probability zero'; split at the semicolon |
| 51 | cut | applied | N2 |
| 52 | cut | applied | N2 |
| 53 | keep | keep | N2 |
| 54 | define | keep | 'spike' is the repository's word for the exploratory runs and the link names the record; a gloss adds words |
| 55 | split | applied | G-10: split |
| 56 | define | applied | G-11 title: the 'Q2:' label cut (the open questions are listed in the ledger's header, not in this appendix) |
| 57 | split | applied | G-11: three sentences |
| 58 | split | keep | the setup parenthesis names the data the numbers come from; a split adds words |
| 59 | keep | keep | N2 |
| 60 | cut | applied | N2 |
| 61 | split | applied | N2 |
| 62 | define | applied | G-12 title: 'active metrics' swapped for 'the contending set' (the glossary's term); 'Q3:' label cut |
| 63 | split | applied | G-12: the last clause is its own sentence at the semicolon |
| 64 | define | keep | 'working' is an exponent the probe note defines; a gloss needs content from it, not a copy edit; owner: a content pass on G-12 |
| 65 | keep | keep | N2 |
| 66 | keep | keep | N2 |
| 67 | cut | applied | N2 |
| 68 | cut | applied | N2 |
| 69 | cut | keep | not a restatement: the sentence adds the reading ('the part of the cloud a single hyperplane does not follow') and the limitations link; G-9 holds the same slack numbers as evidence for tau, this row for the boundary |
| 70 | split | applied | G-13: split at the semicolon |
| 71 | keep | keep | N2 |
| 72 | split | keep | 'all local' qualifies both I7 and the levels; any reordering changes the scope |
| 73 | keep | keep | N2 |
| 74 | cut | applied | N2 |
| 75 | cut | applied | N2 |
| 76 | cut | applied | G-15: the second '(L14)' cut |
| 77 | cut | applied | N2 |
| 78 | split | applied | N2 |
| 79 | split | applied | G-15: split |
| 80 | define | applied | G-16 title: 'as ledger conditions' cut |
| 81 | split | keep | a list of conditions; a split adds words |
| 82 | split | applied | G-16: split |
| 83 | keep | keep | N2 |
| 84 | define | keep | SLSQP is named at G-2 and is the solver's name; 'the polish' is the finite-tau polish of the row's own mechanism cell |
| 85 | cut | keep | raw test names are generated link labels; each carries a path |
| 86 | keep | keep | N2 |
| 87 | keep | keep | N2 |
| 88 | define | keep | the row's mechanism cell defines it (event detection on the dense solution); a gloss adds words |
| 89 | split | applied | G-17: the second clause is its own sentence |
| 90 | split | keep | a verbless list sentence; a verb adds words |
| 91 | split | applied | G-17: the clause that restates the mechanism cell cut; the subject named |
| 92 | split | keep | a list inside one sentence; a split adds words |
| 93 | keep | keep | N2 |
| 94 | cut | applied | N2 |
| 95 | cut | keep | it is the row's consequence: the parenthesis is its scope; cutting it widens the claim |
| 96 | define | keep | 'identify' is the word of the ledger header and of G-12's 'identifiability'; test_gaps names it; one object, one name |
| 97 | split | applied | G-18: the conditions follow the claim; no word added |
| 98 | cut | applied | N2 |
| 99 | cut | applied | N2 |
| 100 | split | applied | G-18: three sentences |
| 101 | cut | applied | N2 |
| 102 | cut | keep | not a restatement: the fixture's K = 3 plane is constructed, this is the package's own K = 3 fit on the fixture |
| 103 | keep | keep | N2 |
| 104 | cut | keep | the first clause is the reading rule of the consequence cell, the second the action; the bridging cell says another thing |
| 105 | cut | applied | N2 |

Counts over the 55 rows N2 did not reason: {'routed': 2, 'applied': 26, 'keep': 28}. Rows 1 and 3 are routed to the owner of the appendix frame.

(The 56 non-N2 rows are the 55 N2 left unapplied plus row 2, which N2 routed and Part A2 settles.)

## Execution and checks
Both notebooks executed once (paper/execute_notebooks.py, warmed MPLCONFIGDIR, no stderr). paper.ipynb unchanged; supporting_material.ipynb: D.18 text, Appendix E job block and table; no file under paper/figures changed.

## Checker (scripts/check_residuals.py --compare scripts/residuals_baseline.json), words / meta / long sentences / compound
- appendix/appendix-e: before 3741 / 1 / 1 / 1, after 3720 / 1 / 1 / 1 (21 words fewer; the flagged meta, long and compound sentences are the job block's frame, routed, and the G-18 sensitivity cell).
- appendix/d-18: before 268, after 278 words (the pointer names the column and what it shows: ten words more, a correction, not copy-editing).
- TOTAL words 73047 before, 73036 after.

## Claims rows and ledger rows
None re-pointed. See paper/length_ledger.toml note below if the checks name a row.

# WP38 landed record: appendices unit N2 (slots appendix-01 to appendix-16, glossary-appendix-a, and the Appendix A rows of glossary-01)

Branch wp38nb, after N1-paper, rebased on origin/dev. Sources edited, nothing executed: the notebook outputs of the supporting material are stale until the execution unit runs both notebooks once. Row numbers are the row's order in its flag table.

## Counts by disposition

| Slot | Rows | Applied | Left (keep) | Routed | Not applied |
|---|---|---|---|---|---|
| appendix-01 | 38 | 13 | 7 | 15 | 3 |
| appendix-02 | 28 | 2 | 2 | 24 | 0 |
| appendix-03 | 40 | 9 | 2 | 29 | 0 |
| appendix-04 | 19 | 4 | 3 | 7 | 5 |
| appendix-05 | 19 | 0 | 0 | 17 | 2 |
| appendix-06 | 39 | 8 | 4 | 24 | 3 |
| appendix-07 | 17 | 2 | 1 | 14 | 0 |
| appendix-08 | 25 | 2 | 7 | 6 | 10 |
| appendix-09 | 18 | 1 | 3 | 14 | 0 |
| appendix-10 | 29 | 0 | 7 | 22 | 0 |
| appendix-11 | 28 | 12 | 2 | 4 | 10 |
| appendix-12 | 33 | 16 | 1 | 4 | 12 |
| appendix-13 | 54 | 32 | 9 | 3 | 10 |
| appendix-14 | 105 | 29 | 20 | 1 | 55 |
| appendix-15 | 47 | 12 | 4 | 7 | 24 |
| appendix-16 | 65 | 15 | 20 | 0 | 30 |
| glossary-appendix-a | 32 | 16 | 4 | 0 | 12 |
| glossary-01 (Appendix A rows only; 24 long-form rows belong to unit L3-case) | 13 | 8 | 2 | 0 | 3 |

## Files changed

`paper/supporting_material.ipynb` (markdown cells 0, 6, 11, 16, 28, 34, 36, 53, 61, 63, 66, 69, 72, 74, 76, 78, 80, 83, 94, 99, 100, 104, 117; outputs untouched), `paper/generate_proofs.py`, `paper/generate_results.py`, `paper/generate_repro.py`, `paper/prior_art.yaml`, `glossary.yaml` (Appendix A fields `formal`, `not`, `defined_in`), `docs/superpowers/notes/abstraction-gaps.md` (Appendix E), `claims_register.toml` (fragments only).

## Routed, with owner

- 163 rows on the lemma pages (L1 to L20, B.1, the L2 block): the statement, the step prose and the axiom text are generated from the lemma scripts and the axiom ledger in `derivation/`; owner: the lemma-script owner. The recurring items: the full axiom text and the "declared at line N" tag printed at every step that uses it (a ledger-renderer structure, owner of `derivation/proofmap.py`), statements and steps with undefined symbols (L3 Z, L5 T_raw, L7 G and v, L8 Z B u Q, L9 s_j against r_j, L12 and L13 symbols), step prose cut off mid-clause (L15.19 to L15.22, L16.1, L16.2), the L8 Hypotheses and Ledger lists out of step (A2), and the repeated step and check pair (L14.2 to L14.5, L19.5 and L19.25).
- The appendix frame (job, main text keeps, this appendix carries, the repository keeps) and the intro line that lists the appendices: structure, owner the paper package; Appendix C and E frame rows included.
- Axiom text and source notes of the ledger (I10, I16, I14, I15, I17, A9, A10): owner the axiom-register owner; the provenance note of I16 ("to be confirmed by the author") belongs in the references record.
- Table and column wording flagged but not copy edits: the D.1 and D.8 column names, the D.4 pair rows, "contending set" and "zero set" heads, the D.18 pointer to a last column (the column is the Jaccard); owner the results-table owner.

## Applied, in groups

- The page template of Appendix B (`generate_proofs.py`): the closing parenthesis "(the paper's box; the script declares the axioms below)" and the label "quoted from the statement" are gone from every Hypotheses line (22 results); the Ledger line is four short sentences; the second result's statement no longer says "above" in its pointer to the first (the Shared script sentence stays as it was: a test pins it); the checker's eight conditions are eight sentences; how-to-read: the three-kinds sentence is split, "no kind for an argument made only in prose" is cut (the two-parts list stays: a test pins it), the establish / cannot-establish pair is one claim per sentence.
- Appendix B prose (cells 6, 11): sources of the compilation and the file path cut, "so rigor is bought at that friction" cut, the algorithm paragraph split in five.
- Appendix C and D prose (cells 16 to 83 and the `generate_results.py` stability and injected-noise lead-ins): splits at semicolons and colons, announcements cut ("This section reads", "Section 9 closes with", "This section sets"), repository paths cut (D.13, D.14, D.17, D.19), "seam" replaced by "cell boundary".
- Appendix E (`abstraction-gaps.md`): 29 edits to the ledger note: splits at semicolons in G-1 to G-6, the CI run numbers and "WP9 review" aside cut from G-10, "no sentence of the prose claims" clauses cut from G-11 and G-14, the sentence that restates G-1 cut from G-13, "triage finding A5" cut from G-18, "usefully" cut from G-15.
- Appendix F (`generate_repro.py`): the lock's format revision cut from the pin, the two command cells split into sentences.
- Appendix G (`prior_art.yaml`, cells 99, 100, 104): splits and cuts in the DEA, multiplicative DEA, frontier, PCA, HoroPCA, MDAO, tradespace, decision-analysis and trade-study entries; "XDSM" and "AHP" no longer appear unexpanded; G.2's intro cut to two sentences and the record path made a link. Table 1 and the section-2 extracts (`short`) are untouched.
- Appendix H: one cut (cell 117, "The methods are complementary, and"); nothing else.
- Appendix A (`glossary.yaml`): 12 fields cut or split (attributes, conditioning, hyperbolic, monomial term, monomial, generalized posynomial, geometric program, generalized geometric program, fitted reference surface, frontier, certificate, ridge, ternary plot, numerically zero).

## Claims rows re-pointed (backing kept)

C032, C136, C139, C140, C154, C158, C388, C395, C396, C499, C534, C620: each fragment now names the surviving text (a capital letter or a full stop where a semicolon stood, a line wrap of a string in the generator). Two cuts were reverted because a row quotes the sentence and nothing surviving says it: C152 (the termination record's fields, D.8) and C159 (the second analysis is computed from the first's coordinates, D.16). Two more were reverted because a test pins them: the Shared script sentence (`test_cr15`), the two-parts list (`test_appendix_b_shows_every_result_of_the_record_with_derived_counts`), and the C.8 sentence "The model is a demonstration and its numbers are illustrative", which a test compares with the mirrored paragraph in `work-packages/WP30-rounds/appendix-c-leaves-out.md`. `tests/test_claims_register.py`: 21 passed.

## Ledger

Appendix H visible prose (the test's count: Markdown, caption, generated sentences from the stale outputs): 916 before, 911 after, ceiling 920 unchanged. Markdown words of the supporting material's sources: 4,780 before, 4,563 after (the supporting material, other than H, has no ceiling row; the ledger is not changed). The count of the generated sentences moves at the execution.

## Generated-output coupling

Every edit to a generator or to `glossary.yaml`, `prior_art.yaml`, `abstraction-gaps.md` changes a notebook output that is committed (Appendix A's table, B, D.11, D.18, E, F.1, F.3, G): those outputs are stale until the execution unit runs both notebooks once. The tests that compare an output with its generator (for example `test_register_committed_output_is_current`, the Appendix B committed-output test, the Appendix E table) fail until then; the checker's counts for the appendix surfaces read the committed outputs and are unchanged until then.

## appendix-01

| Row | Flag | Surface and location | Result | Note |
|---|---|---|---|---|
| 1 | routed | appendix/title, cell 0, intro paragraph | routed | lists the appendices the contents list already shows; a cut is a structure change, owned by the paper package |
| 2 | cut | appendix/title, cell 0, intro paragraph | applied | cell 0 sentence cut |
| 3 | routed | appendix/appendix-b, cell 5, "Main text keeps" | routed | job/keeps/carries/repository-keeps frame is the appendices' template (structure), applied to every appendix |
| 4 | split | appendix/appendix-b, cell 5, "This appendix carries" | applied | cell 6: split; path and list of sources cut |
| 5 | cut | appendix/appendix-b, cell 5, same sentence | applied | cell 6: split; path and list of sources cut |
| 6 | routed | appendix/appendix-b, cell 5, "The repository keeps" | routed | repeats the list of sources just given in "carries"; part of the template, so routed with the frame |
| 7 | keep | appendix/appendix-b, cell 5, What the scripts establish | left | keep |
| 8 | split | appendix/appendix-b, cell 5, What the scripts establish | applied | cell 6: split after "readers"; "so rigor is bought at that friction" cut (claim C388 re-pointed) |
| 9 | keep | appendix/appendix-b, cell 5, What the scripts establish | left | keep |
| 10 | define | appendix/appendix-b, cell 5, What the scripts establish | not applied | sentence quoted by claims row C389 and a test; "Z3" and "requirement checks" are the sentence's own terms |
| 11 | cut | appendix/appendix-b, cell 5, What the scripts establish | not applied | sentence quoted by claims row C389 and a test; "Z3" and "requirement checks" are the sentence's own terms |
| 12 | keep | appendix/appendix-b, cell 5, after the how_to_read cell | left | keep |
| 13 | split | appendix/appendix-b, cell 5, after the how_to_read cell | applied | generate_proofs.how_to_read: split |
| 14 | cut | appendix/appendix-b, cell 5, kinds list | applied | generate_proofs.how_to_read: cut |
| 15 | split | appendix/appendix-b, cell 5, kinds list | applied | generate_proofs.how_to_read: parenthesis promoted to its own sentence |
| 16 | cut | appendix/appendix-b, cell 5 | not applied | tests/test_paper.py::test_appendix_b_shows_every_result_of_the_record pins "(L12 to L20)" in the list; left |
| 17 | split | appendix/appendix-b, cell 5 | applied | generate_proofs.how_to_read: one sentence per claim |
| 18 | cut | appendix/appendix-b, cell 5 | applied | generate_proofs.how_to_read: last clause cut |
| 19 | keep | appendix/appendix-b, cell 5 | left | keep |
| 20 | routed | appendix/b-1, cell 9, L1 hypotheses | applied | generate_proofs.py: the closing parenthesis of the Hypotheses line and the label "quoted from the statement" dropped |
| 21 | routed | appendix/b-1, cell 9, L1 hypotheses | applied | generate_proofs.py: the closing parenthesis of the Hypotheses line and the label "quoted from the statement" dropped |
| 22 | define | appendix/b-1, cell 9, L1 ledger line | routed | lemma-script owner (derivation/): the statement, step prose and axiom text on this page are generated from the lemma scripts and the axiom ledger |
| 23 | routed | appendix/b-1, cell 9, L1.2 and L1.3 and L1.8 | routed | lemma-script owner (derivation/): the statement, step prose and axiom text on this page are generated from the lemma scripts and the axiom ledger |
| 24 | cut | appendix/b-1, cell 9, L1.3 | routed | lemma-script owner (derivation/): the statement, step prose and axiom text on this page are generated from the lemma scripts and the axiom ledger |
| 25 | keep | appendix/b-1, cell 9, L1.8 | left | keep |
| 26 | define | appendix/b-1, cell 9, heading of L3 (short part following) | routed | lemma-script owner (derivation/): the statement, step prose and axiom text on this page are generated from the lemma scripts and the axiom ledger |
| 27 | define | appendix/b-1, cell 9, heading of L5 (short part following) | routed | lemma-script owner (derivation/): the statement, step prose and axiom text on this page are generated from the lemma scripts and the axiom ledger |
| 28 | split | appendix/b-1, cell 9, L3 statement | routed | lemma-script owner (derivation/): the statement, step prose and axiom text on this page are generated from the lemma scripts and the axiom ledger |
| 29 | split | appendix/b-1, cell 9, L11 statement | routed | lemma-script owner (derivation/): the statement, step prose and axiom text on this page are generated from the lemma scripts and the axiom ledger |
| 30 | keep | appendix/b-1, cell 9, L11 statement | left | keep |
| 31 | routed | appendix/l2, cell 10 output, hypotheses | applied | generate_proofs.py: the closing parenthesis of the Hypotheses line and the label "quoted from the statement" dropped |
| 32 | cut | appendix/l2, cell 10 output, hypotheses | applied | generate_proofs.py: the closing parenthesis of the Hypotheses line and the label "quoted from the statement" dropped |
| 33 | define | appendix/l2, cell 10 output, L2.1 | routed | lemma-script owner (derivation/): the statement, step prose and axiom text on this page are generated from the lemma scripts and the axiom ledger |
| 34 | define | appendix/l2, cell 10 output, L2.2 | routed | lemma-script owner (derivation/): the statement, step prose and axiom text on this page are generated from the lemma scripts and the axiom ledger |
| 35 | routed | appendix/l2, cell 10 output, L2.2, L2.3, L2.5 | routed | lemma-script owner (derivation/): the statement, step prose and axiom text on this page are generated from the lemma scripts and the axiom ledger |
| 36 | define | appendix/l2, cell 10 output, L2.6 | routed | lemma-script owner (derivation/): the statement, step prose and axiom text on this page are generated from the lemma scripts and the axiom ledger |
| 37 | split | appendix/l2, cell 10 output, L2.8 | routed | lemma-script owner (derivation/): the statement, step prose and axiom text on this page are generated from the lemma scripts and the axiom ledger |
| 38 | keep | appendix/l2, cell 10 output, L2.4 | left | keep |

## appendix-02

| Row | Flag | Surface and location | Result | Note |
|---|---|---|---|---|
| 1 | define | appendix/l3, cell 10, L3 title and Statement | routed | lemma-script owner (derivation/): the statement, step prose and axiom text on this page are generated from the lemma scripts and the axiom ledger |
| 2 | routed | appendix/l3, cell 10, L3 Statement | routed | lemma-script owner (derivation/): the statement, step prose and axiom text on this page are generated from the lemma scripts and the axiom ledger |
| 3 | split | appendix/l3, cell 10, L3 Statement | routed | lemma-script owner (derivation/): the statement, step prose and axiom text on this page are generated from the lemma scripts and the axiom ledger |
| 4 | cut | appendix/l3, cell 10, L3 Hypotheses | applied | generate_proofs.py: the closing parenthesis of the Hypotheses line and the label "quoted from the statement" dropped |
| 5 | cut | appendix/l3, cell 10, L3 Hypotheses | routed | lemma-script owner (derivation/): the statement, step prose and axiom text on this page are generated from the lemma scripts and the axiom ledger |
| 6 | define | appendix/l3, cell 10, L3 ledger line | routed | lemma-script owner (derivation/): the statement, step prose and axiom text on this page are generated from the lemma scripts and the axiom ledger |
| 7 | routed | appendix/l3, cell 10, step table, every row | routed | lemma-script owner (derivation/): the statement, step prose and axiom text on this page are generated from the lemma scripts and the axiom ledger |
| 8 | define | appendix/l3, cell 10, L3.1 | routed | lemma-script owner (derivation/): the statement, step prose and axiom text on this page are generated from the lemma scripts and the axiom ledger |
| 9 | define | appendix/l3, cell 10, L3.4 | routed | lemma-script owner (derivation/): the statement, step prose and axiom text on this page are generated from the lemma scripts and the axiom ledger |
| 10 | split | appendix/l3, cell 10, L3.5 | routed | lemma-script owner (derivation/): the statement, step prose and axiom text on this page are generated from the lemma scripts and the axiom ledger |
| 11 | split | appendix/l3, cell 10, L3.5 | routed | lemma-script owner (derivation/): the statement, step prose and axiom text on this page are generated from the lemma scripts and the axiom ledger |
| 12 | cut | appendix/l3, cell 10, L3.5 | routed | lemma-script owner (derivation/): the statement, step prose and axiom text on this page are generated from the lemma scripts and the axiom ledger |
| 13 | routed | appendix/l3, cell 10, L3.6, L3.7, L3.10, L3.11, L3.20 | routed | lemma-script owner (derivation/): the statement, step prose and axiom text on this page are generated from the lemma scripts and the axiom ledger |
| 14 | cut | appendix/l3, cell 10, L3.9 | routed | lemma-script owner (derivation/): the statement, step prose and axiom text on this page are generated from the lemma scripts and the axiom ledger |
| 15 | cut | appendix/l3, cell 10, L3.11 | routed | lemma-script owner (derivation/): the statement, step prose and axiom text on this page are generated from the lemma scripts and the axiom ledger |
| 16 | define | appendix/l3, cell 10, L3.15 | routed | lemma-script owner (derivation/): the statement, step prose and axiom text on this page are generated from the lemma scripts and the axiom ledger |
| 17 | define | appendix/l3, cell 10, L3.30 | routed | lemma-script owner (derivation/): the statement, step prose and axiom text on this page are generated from the lemma scripts and the axiom ledger |
| 18 | keep | appendix/l3, cell 10, L3.22 | left | keep |
| 19 | cut | appendix/l4, cell 10, L4 Hypotheses | applied | generate_proofs.py: the closing parenthesis of the Hypotheses line and the label "quoted from the statement" dropped |
| 20 | cut | appendix/l4, cell 10, L4.1 | routed | lemma-script owner (derivation/): the statement, step prose and axiom text on this page are generated from the lemma scripts and the axiom ledger |
| 21 | cut | appendix/l4, cell 10, L4.1 | routed | lemma-script owner (derivation/): the statement, step prose and axiom text on this page are generated from the lemma scripts and the axiom ledger |
| 22 | define | appendix/l4, cell 10, L4.2 | routed | lemma-script owner (derivation/): the statement, step prose and axiom text on this page are generated from the lemma scripts and the axiom ledger |
| 23 | define | appendix/l4, cell 10, L4.6 | routed | lemma-script owner (derivation/): the statement, step prose and axiom text on this page are generated from the lemma scripts and the axiom ledger |
| 24 | cut | appendix/l4, cell 10, L4.8 | routed | lemma-script owner (derivation/): the statement, step prose and axiom text on this page are generated from the lemma scripts and the axiom ledger |
| 25 | keep | appendix/l4, cell 10, L4.11 | left | keep |
| 26 | cut | appendix/l4, cell 10, L4.13 | routed | lemma-script owner (derivation/): the statement, step prose and axiom text on this page are generated from the lemma scripts and the axiom ledger |
| 27 | define | appendix/l4, cell 10, L4.14 | routed | lemma-script owner (derivation/): the statement, step prose and axiom text on this page are generated from the lemma scripts and the axiom ledger |
| 28 | split | appendix/l4, cell 10, L4.12 | routed | lemma-script owner (derivation/): the statement, step prose and axiom text on this page are generated from the lemma scripts and the axiom ledger |

## appendix-03

| Row | Flag | Surface and location | Result | Note |
|---|---|---|---|---|
| 1 | routed | appendix/l5, cell 10 output, L5 Statement | routed | lemma-script owner (derivation/): the statement, step prose and axiom text on this page are generated from the lemma scripts and the axiom ledger |
| 2 | define | appendix/l5, cell 10 output, L5 heading and Statement ("LSE", "LME") | routed | lemma-script owner (derivation/): the statement, step prose and axiom text on this page are generated from the lemma scripts and the axiom ledger |
| 3 | keep | appendix/l5, cell 10 output, L5 File line | left | keep |
| 4 | cut | appendix/l5, cell 10 output, L5 Hypotheses | applied | generate_proofs.py: the closing parenthesis of the Hypotheses line and the label "quoted from the statement" dropped |
| 5 | routed | appendix/l5, cell 10 output, L5 Ledger | applied | generate_proofs.py: the ledger line is now separate sentences (capital A) |
| 6 | define | appendix/l5, cell 10 output, L5.1 | routed | lemma-script owner (derivation/): the statement, step prose and axiom text on this page are generated from the lemma scripts and the axiom ledger |
| 7 | split | appendix/l5, cell 10 output, L5.2 | routed | lemma-script owner (derivation/): the statement, step prose and axiom text on this page are generated from the lemma scripts and the axiom ledger |
| 8 | routed | appendix/l5, cell 10 output, L5.1 to L5.5 (axiom F5 text) | routed | lemma-script owner (derivation/): the statement, step prose and axiom text on this page are generated from the lemma scripts and the axiom ledger |
| 9 | routed | appendix/l5, cell 10 output, L5.1, L5.2, L5.10, L5.20, L5.25 (axiom A3 text) | routed | lemma-script owner (derivation/): the statement, step prose and axiom text on this page are generated from the lemma scripts and the axiom ledger |
| 10 | keep | appendix/l5, cell 10 output, L5.9 | left | keep |
| 11 | cut | appendix/l5, cell 10 output, L5.20 | routed | lemma-script owner (derivation/): the statement, step prose and axiom text on this page are generated from the lemma scripts and the axiom ledger |
| 12 | split | appendix/l5, cell 10 output, L5.25 | routed | lemma-script owner (derivation/): the statement, step prose and axiom text on this page are generated from the lemma scripts and the axiom ledger |
| 13 | split | appendix/l6, cell 10 output, L6 Statement | routed | lemma-script owner (derivation/): the statement, step prose and axiom text on this page are generated from the lemma scripts and the axiom ledger |
| 14 | define | appendix/l6, cell 10 output, L6 Statement ("iid") | routed | lemma-script owner (derivation/): the statement, step prose and axiom text on this page are generated from the lemma scripts and the axiom ledger |
| 15 | cut | appendix/l6, cell 10 output, L6 Statement ("not a finite-sample estimator, and no c | routed | lemma-script owner (derivation/): the statement, step prose and axiom text on this page are generated from the lemma scripts and the axiom ledger |
| 16 | cut | appendix/l6, cell 10 output, L6 Hypotheses | applied | generate_proofs.py: the closing parenthesis of the Hypotheses line and the label "quoted from the statement" dropped |
| 17 | routed | appendix/l6, cell 10 output, L6 Ledger | applied | generate_proofs.py: the ledger line is now separate sentences (capital A) |
| 18 | routed | appendix/l6, cell 10 output, L6.1 | routed | lemma-script owner (derivation/): the statement, step prose and axiom text on this page are generated from the lemma scripts and the axiom ledger |
| 19 | define | appendix/l6, cell 10 output, L6.9 | routed | lemma-script owner (derivation/): the statement, step prose and axiom text on this page are generated from the lemma scripts and the axiom ledger |
| 20 | define | appendix/l7, cell 10 output, L7 Statement | routed | lemma-script owner (derivation/): the statement, step prose and axiom text on this page are generated from the lemma scripts and the axiom ledger |
| 21 | cut | appendix/l7, cell 10 output, L7 Hypotheses | applied | generate_proofs.py: the closing parenthesis of the Hypotheses line and the label "quoted from the statement" dropped |
| 22 | define | appendix/l7, cell 10 output, L7 Ledger | routed | lemma-script owner (derivation/): the statement, step prose and axiom text on this page are generated from the lemma scripts and the axiom ledger |
| 23 | define | appendix/l7, cell 10 output, L7.1 | routed | lemma-script owner (derivation/): the statement, step prose and axiom text on this page are generated from the lemma scripts and the axiom ledger |
| 24 | split | appendix/l7, cell 10 output, L7.3 | routed | lemma-script owner (derivation/): the statement, step prose and axiom text on this page are generated from the lemma scripts and the axiom ledger |
| 25 | cut | appendix/l7, cell 10 output, L7.3 (axiom text) | routed | lemma-script owner (derivation/): the statement, step prose and axiom text on this page are generated from the lemma scripts and the axiom ledger |
| 26 | define | appendix/l7, cell 10 output, L7.4 | routed | lemma-script owner (derivation/): the statement, step prose and axiom text on this page are generated from the lemma scripts and the axiom ledger |
| 27 | routed | appendix/l8, cell 10 output, L8 heading | routed | lemma-script owner (derivation/): the statement, step prose and axiom text on this page are generated from the lemma scripts and the axiom ledger |
| 28 | define | appendix/l8, cell 10 output, L8 Statement | routed | lemma-script owner (derivation/): the statement, step prose and axiom text on this page are generated from the lemma scripts and the axiom ledger |
| 29 | cut | appendix/l8, cell 10 output, L8 Hypotheses | applied | generate_proofs.py: the closing parenthesis of the Hypotheses line and the label "quoted from the statement" dropped |
| 30 | routed | appendix/l8, cell 10 output, L8 Hypotheses ("A2") and Ledger | applied | generate_proofs.py: the ledger line is now separate sentences (capital A) |
| 31 | routed | appendix/l8, cell 10 output, L8.1, L8.2, L8.4, L8.5 (axiom A7 text) | routed | lemma-script owner (derivation/): the statement, step prose and axiom text on this page are generated from the lemma scripts and the axiom ledger |
| 32 | cut | appendix/l8, cell 10 output, L8.3 (axiom I6 text) | routed | lemma-script owner (derivation/): the statement, step prose and axiom text on this page are generated from the lemma scripts and the axiom ledger |
| 33 | define | appendix/l9, cell 10 output, L9 heading | routed | lemma-script owner (derivation/): the statement, step prose and axiom text on this page are generated from the lemma scripts and the axiom ledger |
| 34 | split | appendix/l9, cell 10 output, L9 Statement | routed | lemma-script owner (derivation/): the statement, step prose and axiom text on this page are generated from the lemma scripts and the axiom ledger |
| 35 | cut | appendix/l9, cell 10 output, L9 Hypotheses | applied | generate_proofs.py: the closing parenthesis of the Hypotheses line and the label "quoted from the statement" dropped |
| 36 | routed | appendix/l9, cell 10 output, L9 Ledger | applied | generate_proofs.py: the ledger line is now separate sentences (capital A) |
| 37 | define | appendix/l9, cell 10 output, L9.1, L9.3, L9.4 (axiom A4 text) | routed | lemma-script owner (derivation/): the statement, step prose and axiom text on this page are generated from the lemma scripts and the axiom ledger |
| 38 | routed | appendix/l9, cell 10 output, L9.1, L9.3, L9.4, L9.5 | routed | lemma-script owner (derivation/): the statement, step prose and axiom text on this page are generated from the lemma scripts and the axiom ledger |
| 39 | define | appendix/l9, cell 10 output, L9.3 | routed | lemma-script owner (derivation/): the statement, step prose and axiom text on this page are generated from the lemma scripts and the axiom ledger |
| 40 | cut | appendix/l9, cell 10 output, L9.1 | routed | lemma-script owner (derivation/): the statement, step prose and axiom text on this page are generated from the lemma scripts and the axiom ledger |

## appendix-04

| Row | Flag | Surface and location | Result | Note |
|---|---|---|---|---|
| 1 | define | appendix/l10, cell 10, L10.25 | routed | lemma-script owner (derivation/): the statement, step prose and axiom text on this page are generated from the lemma scripts and the axiom ledger |
| 2 | keep | appendix/l10, cell 10, L10.15 | left | keep |
| 3 | keep | appendix/l10, cell 10, L10.11 | left | keep |
| 4 | define | appendix/l11, cell 10, heading | routed | lemma-script owner (derivation/): the statement, step prose and axiom text on this page are generated from the lemma scripts and the axiom ledger |
| 5 | cut | appendix/l11, cell 10, statement | routed | lemma-script owner (derivation/): the statement, step prose and axiom text on this page are generated from the lemma scripts and the axiom ledger |
| 6 | split | appendix/l11, cell 10, statement | routed | lemma-script owner (derivation/): the statement, step prose and axiom text on this page are generated from the lemma scripts and the axiom ledger |
| 7 | split | appendix/l11, cell 10, statement | routed | lemma-script owner (derivation/): the statement, step prose and axiom text on this page are generated from the lemma scripts and the axiom ledger |
| 8 | define | appendix/l11, cell 10, statement | routed | lemma-script owner (derivation/): the statement, step prose and axiom text on this page are generated from the lemma scripts and the axiom ledger |
| 9 | define | appendix/l11, cell 10, L11.20 | routed | lemma-script owner (derivation/): the statement, step prose and axiom text on this page are generated from the lemma scripts and the axiom ledger |
| 10 | split | appendix/b-2, cell 11 | applied | cell 11: split at the semicolon (claims C136 re-pointed) |
| 11 | define | appendix/b-2, cell 11 | not applied | a define adds words (a gloss or expansion) and the term is the one the glossary, ledger or main text uses; left |
| 12 | split | appendix/b-2, cell 11 | applied | cell 11: the loop and its stopping rule are now two sentences |
| 13 | split | appendix/b-2, cell 11 | applied | cell 11: split into the bound, the posynomial fact and the consequence (claims C139, C140 re-pointed) |
| 14 | cut | appendix/b-2, cell 11 | applied | cell 11: split into the bound, the posynomial fact and the consequence (claims C139, C140 re-pointed) |
| 15 | cut | appendix/b-2, cell 11 | not applied | citation rendering is the bibliography filter, not the cell text |
| 16 | define | appendix/b-2, cell 11 | not applied | a define adds words (a gloss or expansion) and the term is the one the glossary, ledger or main text uses; left |
| 17 | cut | appendix/b-2, cell 11 | not applied | claims row C144 quotes "the second-order test that certifies a strict local minimizer" |
| 18 | keep | appendix/b-2, cell 11 | left | keep |
| 19 | split | appendix/b-2, cell 11 | not applied | claims rows C145 and C146 quote it as written (a split would change the fragment) |

## appendix-05

| Row | Flag | Surface and location | Result | Note |
|---|---|---|---|---|
| 1 | define | appendix/l12, cell 12, L12 heading | routed | lemma-script owner (derivation/): the statement, step prose and axiom text on this page are generated from the lemma scripts and the axiom ledger |
| 2 | split | appendix/l12, cell 12, Statement | routed | lemma-script owner (derivation/): the statement, step prose and axiom text on this page are generated from the lemma scripts and the axiom ledger |
| 3 | cut | appendix/l12, cell 12, Statement | routed | lemma-script owner (derivation/): the statement, step prose and axiom text on this page are generated from the lemma scripts and the axiom ledger |
| 4 | define | appendix/l12, cell 12, Statement | routed | lemma-script owner (derivation/): the statement, step prose and axiom text on this page are generated from the lemma scripts and the axiom ledger |
| 5 | routed | appendix/l12, cell 12, Hypotheses | routed | lemma-script owner (derivation/): the statement, step prose and axiom text on this page are generated from the lemma scripts and the axiom ledger |
| 6 | routed | appendix/l12, cell 12, step table L12.1 to L12.8, L12.16, L12.27, L12.32 | routed | lemma-script owner (derivation/): the statement, step prose and axiom text on this page are generated from the lemma scripts and the axiom ledger |
| 7 | split | appendix/l13, cell 12, Statement | routed | lemma-script owner (derivation/): the statement, step prose and axiom text on this page are generated from the lemma scripts and the axiom ledger |
| 8 | split | appendix/l13, cell 12, Statement | routed | lemma-script owner (derivation/): the statement, step prose and axiom text on this page are generated from the lemma scripts and the axiom ledger |
| 9 | routed | appendix/l13, cell 12, Hypotheses | routed | lemma-script owner (derivation/): the statement, step prose and axiom text on this page are generated from the lemma scripts and the axiom ledger |
| 10 | cut | appendix/l13, cell 12, step L13.8 | routed | lemma-script owner (derivation/): the statement, step prose and axiom text on this page are generated from the lemma scripts and the axiom ledger |
| 11 | split | appendix/l14, cell 12, Shared script | not applied | tests/test_paper.py::test_cr15 pins "each proof lists its own steps in the file's order" as one sentence with the numbering; left |
| 12 | define | appendix/l14, cell 12, Statement | routed | lemma-script owner (derivation/): the statement, step prose and axiom text on this page are generated from the lemma scripts and the axiom ledger |
| 13 | cut | appendix/l14, cell 12, Statement | routed | lemma-script owner (derivation/): the statement, step prose and axiom text on this page are generated from the lemma scripts and the axiom ledger |
| 14 | split | appendix/l14, cell 12, Statement | routed | lemma-script owner (derivation/): the statement, step prose and axiom text on this page are generated from the lemma scripts and the axiom ledger |
| 15 | cut | appendix/l14, cell 12, Statement | routed | lemma-script owner (derivation/): the statement, step prose and axiom text on this page are generated from the lemma scripts and the axiom ledger |
| 16 | routed | appendix/l14, cell 12, step table L14.2 to L14.5 and L14.12 to L14.15 | routed | lemma-script owner (derivation/): the statement, step prose and axiom text on this page are generated from the lemma scripts and the axiom ledger |
| 17 | define | appendix/l14, cell 12, step L14.10 | routed | lemma-script owner (derivation/): the statement, step prose and axiom text on this page are generated from the lemma scripts and the axiom ledger |
| 18 | cut | appendix/l14-2, cell 12, corollary Statement | routed | lemma-script owner (derivation/): the statement, step prose and axiom text on this page are generated from the lemma scripts and the axiom ledger |
| 19 | cut | appendix/l14-2, cell 12, corollary Shared script | not applied | tests/test_paper.py::test_cr15 pins "each proof lists its own steps in the file's order" as one sentence with the numbering; left |

## appendix-06

| Row | Flag | Surface and location | Result | Note |
|---|---|---|---|---|
| 1 | split | appendix/l14-2, cell 12 output, "Shared script" | not applied | tests/test_paper.py::test_cr15 pins "each proof lists its own steps in the file's order" as one sentence with the numbering; left |
| 2 | cut | appendix/l14-2, cell 12 output, "File." | applied | generate_proofs.py: "above" dropped from the pointer |
| 3 | cut | appendix/l14-2, cell 12 output, "Hypotheses" | routed | lemma-script owner (derivation/): the statement, step prose and axiom text on this page are generated from the lemma scripts and the axiom ledger |
| 4 | split | appendix/l14-2, cell 12 output, "Ledger" | applied | generate_proofs.py: the ledger line is now separate sentences (capital A) |
| 5 | define | appendix/l14-2, cell 12 output, "Ledger" | routed | lemma-script owner (derivation/): the statement, step prose and axiom text on this page are generated from the lemma scripts and the axiom ledger |
| 6 | define | appendix/l14-2, cell 12 output, step L14.8 prose | routed | lemma-script owner (derivation/): the statement, step prose and axiom text on this page are generated from the lemma scripts and the axiom ledger |
| 7 | keep | appendix/l14-2, cell 12 output, step L14.8 and L14.10 | left | keep |
| 8 | split | appendix/l15, cell 12 output, "Shared script" | not applied | tests/test_paper.py::test_cr15 pins "each proof lists its own steps in the file's order" as one sentence with the numbering; left |
| 9 | split | appendix/l15, cell 12 output, "File." | routed | lemma-script owner (derivation/): the statement, step prose and axiom text on this page are generated from the lemma scripts and the axiom ledger |
| 10 | define | appendix/l15, cell 12 output, "File." | routed | lemma-script owner (derivation/): the statement, step prose and axiom text on this page are generated from the lemma scripts and the axiom ledger |
| 11 | split | appendix/l15, cell 12 output, "Hypotheses" | applied | generate_proofs.py: the closing parenthesis of the Hypotheses line and the label "quoted from the statement" dropped |
| 12 | cut | appendix/l15, cell 12 output, "Hypotheses" | applied | generate_proofs.py: the closing parenthesis of the Hypotheses line and the label "quoted from the statement" dropped |
| 13 | split | appendix/l15, cell 12 output, "Hypotheses" | routed | lemma-script owner (derivation/): the statement, step prose and axiom text on this page are generated from the lemma scripts and the axiom ledger |
| 14 | define | appendix/l15, cell 12 output, "Hypotheses" | routed | lemma-script owner (derivation/): the statement, step prose and axiom text on this page are generated from the lemma scripts and the axiom ledger |
| 15 | split | appendix/l15, cell 12 output, "Ledger" | applied | generate_proofs.py: the ledger line is now separate sentences (capital A) |
| 16 | split | appendix/l15, cell 12 output, step L15.1 prose | routed | lemma-script owner (derivation/): the statement, step prose and axiom text on this page are generated from the lemma scripts and the axiom ledger |
| 17 | cut | appendix/l15, cell 12 output, step L15.1 | routed | lemma-script owner (derivation/): the statement, step prose and axiom text on this page are generated from the lemma scripts and the axiom ledger |
| 18 | routed | appendix/l15, cell 12 output, steps L15.3, L15.5, L15.6 | routed | lemma-script owner (derivation/): the statement, step prose and axiom text on this page are generated from the lemma scripts and the axiom ledger |
| 19 | split | appendix/l15, cell 12 output, step L15.2 | routed | lemma-script owner (derivation/): the statement, step prose and axiom text on this page are generated from the lemma scripts and the axiom ledger |
| 20 | keep | appendix/l15, cell 12 output, step L15.2 | left | keep |
| 21 | define | appendix/l15, cell 12 output, steps L15.2, L15.4 | routed | lemma-script owner (derivation/): the statement, step prose and axiom text on this page are generated from the lemma scripts and the axiom ledger |
| 22 | keep | appendix/l15, cell 12 output, step L15.7 | left | keep |
| 23 | define | appendix/l15, cell 12 output, step L15.8 | routed | lemma-script owner (derivation/): the statement, step prose and axiom text on this page are generated from the lemma scripts and the axiom ledger |
| 24 | keep | appendix/l15, cell 12 output, step L15.16 | left | keep |
| 25 | routed | appendix/l15, cell 12 output, steps L15.9 to L15.16 | routed | lemma-script owner (derivation/): the statement, step prose and axiom text on this page are generated from the lemma scripts and the axiom ledger |
| 26 | split | appendix/l15-2, cell 12 output, section heading | routed | lemma-script owner (derivation/): the statement, step prose and axiom text on this page are generated from the lemma scripts and the axiom ledger |
| 27 | define | appendix/l15-2, cell 12 output, section heading | routed | lemma-script owner (derivation/): the statement, step prose and axiom text on this page are generated from the lemma scripts and the axiom ledger |
| 28 | cut | appendix/l15-2, cell 12 output, "Shared script" | not applied | tests/test_paper.py::test_cr15 pins "each proof lists its own steps in the file's order" as one sentence with the numbering; left |
| 29 | split | appendix/l15-2, cell 12 output, "File." | applied | generate_proofs.py: "above" dropped from the pointer |
| 30 | cut | appendix/l15-2, cell 12 output, "File." | routed | lemma-script owner (derivation/): the statement, step prose and axiom text on this page are generated from the lemma scripts and the axiom ledger |
| 31 | cut | appendix/l15-2, cell 12 output, "Hypotheses" | applied | generate_proofs.py: the closing parenthesis of the Hypotheses line and the label "quoted from the statement" dropped |
| 32 | split | appendix/l15-2, cell 12 output, "Ledger" | applied | generate_proofs.py: the ledger line is now separate sentences (capital A) |
| 33 | define | appendix/l15-2, cell 12 output, step L15.17 | routed | lemma-script owner (derivation/): the statement, step prose and axiom text on this page are generated from the lemma scripts and the axiom ledger |
| 34 | split | appendix/l15-2, cell 12 output, step L15.18 | routed | lemma-script owner (derivation/): the statement, step prose and axiom text on this page are generated from the lemma scripts and the axiom ledger |
| 35 | routed | appendix/l15-2, cell 12 output, step L15.19 | routed | lemma-script owner (derivation/): the statement, step prose and axiom text on this page are generated from the lemma scripts and the axiom ledger |
| 36 | define | appendix/l15-2, cell 12 output, step L15.19 | routed | lemma-script owner (derivation/): the statement, step prose and axiom text on this page are generated from the lemma scripts and the axiom ledger |
| 37 | routed | appendix/l15-2, cell 12 output, step L15.20 | routed | lemma-script owner (derivation/): the statement, step prose and axiom text on this page are generated from the lemma scripts and the axiom ledger |
| 38 | routed | appendix/l15-2, cell 12 output, step L15.21 | routed | lemma-script owner (derivation/): the statement, step prose and axiom text on this page are generated from the lemma scripts and the axiom ledger |
| 39 | routed | appendix/l15-2, cell 12 output, step L15.22 | routed | lemma-script owner (derivation/): the statement, step prose and axiom text on this page are generated from the lemma scripts and the axiom ledger |

## appendix-07

| Row | Flag | Surface and location | Result | Note |
|---|---|---|---|---|
| 1 | split | appendix/l16, cell 12 output, Statement | routed | lemma-script owner (derivation/): the statement, step prose and axiom text on this page are generated from the lemma scripts and the axiom ledger |
| 2 | routed | appendix/l16, cell 12 output, Statement (i) | routed | lemma-script owner (derivation/): the statement, step prose and axiom text on this page are generated from the lemma scripts and the axiom ledger |
| 3 | routed | appendix/l16, cell 12 output, Hypotheses | applied | generate_proofs.py: the closing parenthesis of the Hypotheses line and the label "quoted from the statement" dropped |
| 4 | define | appendix/l16, cell 12 output, Hypotheses | routed | lemma-script owner (derivation/): the statement, step prose and axiom text on this page are generated from the lemma scripts and the axiom ledger |
| 5 | routed | appendix/l16, cell 12 output, Ledger | applied | generate_proofs.py: the ledger line is now separate sentences (capital A) |
| 6 | routed | appendix/l16, L16.1 | routed | lemma-script owner (derivation/): the statement, step prose and axiom text on this page are generated from the lemma scripts and the axiom ledger |
| 7 | routed | appendix/l16, L16.2 | routed | lemma-script owner (derivation/): the statement, step prose and axiom text on this page are generated from the lemma scripts and the axiom ledger |
| 8 | routed | appendix/l16, L16.6 | routed | lemma-script owner (derivation/): the statement, step prose and axiom text on this page are generated from the lemma scripts and the axiom ledger |
| 9 | routed | appendix/l16, L16.8, L16.14, L16.21 | routed | lemma-script owner (derivation/): the statement, step prose and axiom text on this page are generated from the lemma scripts and the axiom ledger |
| 10 | routed | appendix/l16, L16.31 | routed | lemma-script owner (derivation/): the statement, step prose and axiom text on this page are generated from the lemma scripts and the axiom ledger |
| 11 | define | appendix/l16, L16.13 | routed | lemma-script owner (derivation/): the statement, step prose and axiom text on this page are generated from the lemma scripts and the axiom ledger |
| 12 | define | appendix/l16, L16.30 | routed | lemma-script owner (derivation/): the statement, step prose and axiom text on this page are generated from the lemma scripts and the axiom ledger |
| 13 | define | appendix/l16, L16.14 | routed | lemma-script owner (derivation/): the statement, step prose and axiom text on this page are generated from the lemma scripts and the axiom ledger |
| 14 | define | appendix/l16, L16.17 | routed | lemma-script owner (derivation/): the statement, step prose and axiom text on this page are generated from the lemma scripts and the axiom ledger |
| 15 | define | appendix/l16, L16.43 | routed | lemma-script owner (derivation/): the statement, step prose and axiom text on this page are generated from the lemma scripts and the axiom ledger |
| 16 | cut | appendix/l16, L16.49 | routed | lemma-script owner (derivation/): the statement, step prose and axiom text on this page are generated from the lemma scripts and the axiom ledger |
| 17 | keep | appendix/l16, L16.48 | left | keep |

## appendix-08

| Row | Flag | Surface and location | Result | Note |
|---|---|---|---|---|
| 1 | split | `appendix/l17`, L17 Statement | not applied | not applied in this pass: left; no edit made |
| 2 | define | `appendix/l17`, L17 Statement, "first-order (KKT) conditions" | not applied | a define adds words (a gloss or expansion) and the term is the one the glossary, ledger or main text uses; left |
| 3 | cut | `appendix/l17`, L17 Hypotheses | applied | generate_proofs.py: the closing parenthesis of the Hypotheses line and the label "quoted from the statement" dropped |
| 4 | cut | `appendix/l17`, L17 Hypotheses | applied | generate_proofs.py: the closing parenthesis of the Hypotheses line and the label "quoted from the statement" dropped |
| 5 | routed | `appendix/l17`, L17.21 (I16 text) | routed | Long parenthetical definition inside a conditional; axiom text is owned by the axiom register, so the rewrite is not made here. |
| 6 | routed | `appendix/l17`, L17.21 (I16 text) | routed | Provenance of the reading (course copy, page, "to be confirmed") belongs in the references record, not in a reader-facing ledger row; a source claim, so owned e |
| 7 | routed | `appendix/l17`, L17.22 and L17.23 (I16 text) | routed | The identical axiom text, long source note included, is printed three times (L17.21 to 23); once at first use would do. Placement change, so routed. |
| 8 | keep | `appendix/l17`, L17.24 | left | keep |
| 9 | keep | `appendix/l17`, L17.14 | left | keep |
| 10 | define | `appendix/l17`, L17.36 | not applied | a define adds words (a gloss or expansion) and the term is the one the glossary, ledger or main text uses; left |
| 11 | define | `appendix/l17`, L17.13 | not applied | a define adds words (a gloss or expansion) and the term is the one the glossary, ledger or main text uses; left |
| 12 | keep | `appendix/l17`, L17.19 | left | keep |
| 13 | routed | `appendix/l17`, L17.19 | routed | Term used (L17.19) before its definition (L17.21); reordering is a structure change. |
| 14 | split | `appendix/l18`, L18 Statement | not applied | not applied in this pass: left; no edit made |
| 15 | split | `appendix/l18`, L18 Statement | not applied | not applied in this pass: left; no edit made |
| 16 | cut | `appendix/l18`, L18 Statement | not applied | not applied in this pass: left; no edit made |
| 17 | routed | `appendix/l18`, L18.8 to L18.10 (A10 text) | routed | Parenthesis carries a second thought and repeats the statement; axiom text, owned by the axiom register. |
| 18 | keep | `appendix/l18`, L18.8 to L18.10 (A10 text) | left | keep |
| 19 | routed | `appendix/l18`, L18.2 to L18.4 (A9 text) | routed | The parenthesis adds a justification and the clause after the semicolon adds a different case; axiom text, repeated three times (L18.2 to 4) for the same reason |
| 20 | cut | `appendix/l18`, L18.5 | not applied | not applied in this pass: left; no edit made |
| 21 | keep | `appendix/l18`, L18.6 (A4 text) | left | keep |
| 22 | define | `appendix/l18`, L18.11 | not applied | a define adds words (a gloss or expansion) and the term is the one the glossary, ledger or main text uses; left |
| 23 | cut | `appendix/l18`, L18.5 (A5 text) | not applied | not applied in this pass: left; no edit made |
| 24 | keep | `appendix/l18`, L18.13 | left | keep |
| 25 | keep | `appendix/l18`, L18.14 | left | keep |

## appendix-09

| Row | Flag | Surface and location | Result | Note |
|---|---|---|---|---|
| 1 | keep | appendix/l19, Statement | left | keep |
| 2 | routed | appendix/l19, Statement, "(A11)" | routed | lemma-script owner (derivation/): the statement, step prose and axiom text on this page are generated from the lemma scripts and the axiom ledger |
| 3 | split | appendix/l19, Statement, "(from E max z <= ...)" | routed | lemma-script owner (derivation/): the statement, step prose and axiom text on this page are generated from the lemma scripts and the axiom ledger |
| 4 | routed | appendix/l19, Hypotheses line | routed | lemma-script owner (derivation/): the statement, step prose and axiom text on this page are generated from the lemma scripts and the axiom ledger |
| 5 | routed | appendix/l19, Ledger line | applied | generate_proofs.py: the ledger line is now separate sentences (capital A) |
| 6 | routed | appendix/l19, L19.2 | routed | lemma-script owner (derivation/): the statement, step prose and axiom text on this page are generated from the lemma scripts and the axiom ledger |
| 7 | routed | appendix/l19, L19.2 | routed | lemma-script owner (derivation/): the statement, step prose and axiom text on this page are generated from the lemma scripts and the axiom ledger |
| 8 | routed | appendix/l19, L19.1 | routed | lemma-script owner (derivation/): the statement, step prose and axiom text on this page are generated from the lemma scripts and the axiom ledger |
| 9 | routed | appendix/l19, L19.6 | routed | lemma-script owner (derivation/): the statement, step prose and axiom text on this page are generated from the lemma scripts and the axiom ledger |
| 10 | routed | appendix/l19, L19.10 | routed | lemma-script owner (derivation/): the statement, step prose and axiom text on this page are generated from the lemma scripts and the axiom ledger |
| 11 | routed | appendix/l19, L19.10 | routed | lemma-script owner (derivation/): the statement, step prose and axiom text on this page are generated from the lemma scripts and the axiom ledger |
| 12 | routed | appendix/l19, L19.10 | routed | lemma-script owner (derivation/): the statement, step prose and axiom text on this page are generated from the lemma scripts and the axiom ledger |
| 13 | define | appendix/l19, L19.11 | routed | lemma-script owner (derivation/): the statement, step prose and axiom text on this page are generated from the lemma scripts and the axiom ledger |
| 14 | keep | appendix/l19, L19.12 | left | keep |
| 15 | cut | appendix/l19, L19.30 | routed | lemma-script owner (derivation/): the statement, step prose and axiom text on this page are generated from the lemma scripts and the axiom ledger |
| 16 | define | appendix/l19, L19.41 | routed | lemma-script owner (derivation/): the statement, step prose and axiom text on this page are generated from the lemma scripts and the axiom ledger |
| 17 | keep | appendix/l19, L19.13 | left | keep |
| 18 | routed | appendix/l19, L19.5 and L19.25 | routed | lemma-script owner (derivation/): the statement, step prose and axiom text on this page are generated from the lemma scripts and the axiom ledger |

## appendix-10

| Row | Flag | Surface and location | Result | Note |
|---|---|---|---|---|
| 1 | split | appendix/l20, cell 12, Statement | routed | lemma-script owner (derivation/): the statement, step prose and axiom text on this page are generated from the lemma scripts and the axiom ledger |
| 2 | split | appendix/l20, cell 12, Statement | routed | lemma-script owner (derivation/): the statement, step prose and axiom text on this page are generated from the lemma scripts and the axiom ledger |
| 3 | keep | appendix/l20, cell 12, Statement | left | keep |
| 4 | define | appendix/l20, cell 12, Statement | routed | lemma-script owner (derivation/): the statement, step prose and axiom text on this page are generated from the lemma scripts and the axiom ledger |
| 5 | split | appendix/l20, cell 12, Statement | routed | lemma-script owner (derivation/): the statement, step prose and axiom text on this page are generated from the lemma scripts and the axiom ledger |
| 6 | keep | appendix/l20, cell 12, Statement | left | keep |
| 7 | keep | appendix/l20, cell 12, Statement | left | keep |
| 8 | routed | appendix/l20, cell 12, Hypotheses | routed | lemma-script owner (derivation/): the statement, step prose and axiom text on this page are generated from the lemma scripts and the axiom ledger |
| 9 | cut | appendix/l20, cell 12, Hypotheses | routed | lemma-script owner (derivation/): the statement, step prose and axiom text on this page are generated from the lemma scripts and the axiom ledger |
| 10 | cut | appendix/l20, cell 12, step L20.2 | routed | lemma-script owner (derivation/): the statement, step prose and axiom text on this page are generated from the lemma scripts and the axiom ledger |
| 11 | cut | appendix/l20, cell 12, step L20.9 | routed | lemma-script owner (derivation/): the statement, step prose and axiom text on this page are generated from the lemma scripts and the axiom ledger |
| 12 | cut | appendix/l20, cell 12, step L20.10 | routed | lemma-script owner (derivation/): the statement, step prose and axiom text on this page are generated from the lemma scripts and the axiom ledger |
| 13 | routed | appendix/l20, cell 12, steps L20.1 to L20.62 (every axiom step) | routed | lemma-script owner (derivation/): the statement, step prose and axiom text on this page are generated from the lemma scripts and the axiom ledger |
| 14 | routed | appendix/l20, cell 12, steps L20.4, L20.5, L20.6, L20.7 | routed | lemma-script owner (derivation/): the statement, step prose and axiom text on this page are generated from the lemma scripts and the axiom ledger |
| 15 | routed | appendix/l20, cell 12, steps L20.11, L20.12, L20.14, L20.62 | routed | lemma-script owner (derivation/): the statement, step prose and axiom text on this page are generated from the lemma scripts and the axiom ledger |
| 16 | routed | appendix/l20, cell 12, step L20.11 (R3 text) | routed | lemma-script owner (derivation/): the statement, step prose and axiom text on this page are generated from the lemma scripts and the axiom ledger |
| 17 | routed | appendix/l20, cell 12, steps L20.13, L20.15 | routed | lemma-script owner (derivation/): the statement, step prose and axiom text on this page are generated from the lemma scripts and the axiom ledger |
| 18 | routed | appendix/l20, cell 12, steps L20.16, L20.43, L20.60 | routed | lemma-script owner (derivation/): the statement, step prose and axiom text on this page are generated from the lemma scripts and the axiom ledger |
| 19 | keep | appendix/l20, cell 12, step L20.16 (I18 text) | left | keep |
| 20 | routed | appendix/l20, cell 12, step L20.20 | routed | lemma-script owner (derivation/): the statement, step prose and axiom text on this page are generated from the lemma scripts and the axiom ledger |
| 21 | routed | appendix/l20, cell 12, step L20.60 | routed | lemma-script owner (derivation/): the statement, step prose and axiom text on this page are generated from the lemma scripts and the axiom ledger |
| 22 | routed | appendix/l20, cell 12, step L20.61 | routed | lemma-script owner (derivation/): the statement, step prose and axiom text on this page are generated from the lemma scripts and the axiom ledger |
| 23 | routed | appendix/l20, cell 12, step L20.62 | routed | lemma-script owner (derivation/): the statement, step prose and axiom text on this page are generated from the lemma scripts and the axiom ledger |
| 24 | routed | appendix/l20, cell 12, step L20.35 | routed | lemma-script owner (derivation/): the statement, step prose and axiom text on this page are generated from the lemma scripts and the axiom ledger |
| 25 | routed | appendix/l20, cell 12, step L20.30 | routed | lemma-script owner (derivation/): the statement, step prose and axiom text on this page are generated from the lemma scripts and the axiom ledger |
| 26 | routed | appendix/l20, cell 12, step L20.4 | routed | lemma-script owner (derivation/): the statement, step prose and axiom text on this page are generated from the lemma scripts and the axiom ledger |
| 27 | keep | appendix/l20, cell 12, step L20.34 | left | keep |
| 28 | keep | appendix/l20, cell 12, Statement | left | keep |
| 29 | keep | appendix/l20, cell 12, Statement | left | keep |

## appendix-11

| Row | Flag | Surface and location | Result | Note |
|---|---|---|---|---|
| 1 | split | appendix/b-3, cell 13, "The checker passes only when" | applied | generate_proofs.checker: eight sentences |
| 2 | split | appendix/appendix-c, cell 15, "Job." | applied | cell 16: split at the semicolon |
| 3 | split | appendix/appendix-c, cell 15, "The cubesat case is a worked example" | applied | cell 16: first split; "either use" left (it is the supervisor's sentence, claims row C032 re-pointed) |
| 4 | routed | appendix/appendix-c, cell 15, "Main text keeps" | routed | Announces what is elsewhere; the template of the "Job / keeps / carries" frame is structure, owned by the appendix-frame package. |
| 5 | routed | appendix/appendix-c, cell 15, "This appendix carries" | routed | The headings already list the parts; part of the same frame, structure, so routed. |
| 6 | define | appendix/appendix-c, cell 15, "The repository keeps" | not applied | a define adds words (a gloss or expansion) and the term is the one the glossary, ledger or main text uses; left |
| 7 | - | appendix/c-1, cell 17 | not applied | not applied in this pass: left; no edit made |
| 8 | define | appendix/c-3, cell 22, table headings | not applied | a define adds words (a gloss or expansion) and the term is the one the glossary, ledger or main text uses; left |
| 9 | cut | appendix/c-5, cell 26, first paragraph | not applied | not applied in this pass: left; no edit made |
| 10 | cut | appendix/c-5, cell 26, "The association of every pair" | applied | cell 28: split; the code path dropped |
| 11 | split | appendix/c-5, cell 26, same sentence | applied | cell 28: split; the code path dropped |
| 12 | keep | appendix/c-6, cell 30, ledger table | left | keep |
| 13 | split | appendix/c-8, cell 30 (C.8), cost paragraph | applied | cell 34: split in three (claim C496 still quotes the first clause) |
| 14 | define | appendix/c-8, cell 30 (C.8), cost paragraph | not applied | a define adds words (a gloss or expansion) and the term is the one the glossary, ledger or main text uses; left |
| 15 | routed | appendix/c-8, cell 30 (C.8), cost paragraph | routed | A comparison figure with no source stated here; it is a number, so owner decides whether it stays. |
| 16 | cut | appendix/c-8, cell 30 (C.8), "What the case leaves out." | not applied | the paragraph is mirrored in work-packages/WP30-rounds/appendix-c-leaves-out.md and a test requires the two to be equal; left |
| 17 | keep | appendix/c-8, cell 30 (C.8), "Four requirement limits" | left | keep |
| 18 | split | appendix/c-8, cell 30 (C.8), Pointing error | applied | cell 34: split at "so" and the colon (claim C504 still quotes) |
| 19 | split | appendix/c-8, cell 30 (C.8), Momentum | applied | cell 34: subject moved next to its verb |
| 20 | split | appendix/c-8, cell 30 (C.8), Launch | applied | cell 34: three sentences (claim C502 still quotes) |
| 21 | define | appendix/c-8, cell 30 (C.8), Scenario | not applied | a define adds words (a gloss or expansion) and the term is the one the glossary, ledger or main text uses; left |
| 22 | split | appendix/appendix-d, cell 35, "Job." | applied | cell 36: split at the semicolon |
| 23 | routed | appendix/appendix-d, cell 35, "Main text keeps" | routed | Metanarration of the appendix frame; structure, owned by the frame package. |
| 24 | define | appendix/appendix-d, cell 35, "Main text keeps" | applied | cell 28: split; the code path dropped |
| 25 | split | appendix/appendix-d, cell 35, "This appendix carries" | not applied | not applied in this pass: left; no edit made |
| 26 | routed | appendix/appendix-d, cell 35, same sentence | applied | cell 28: split; the code path dropped |
| 27 | define | appendix/d-1, cell 37, table headings | not applied | a define adds words (a gloss or expansion) and the term is the one the glossary, ledger or main text uses; left |
| 28 | define | appendix/d-1, cell 37, table | not applied | a define adds words (a gloss or expansion) and the term is the one the glossary, ledger or main text uses; left |

## appendix-12

| Row | Flag | Surface and location | Result | Note |
|---|---|---|---|---|
| 1 | routed | appendix/d-2, cell 40, table header | routed | Column names (frac_above_, gamma, radius, bound) are used before any definition in the appendix (D.8 explains some later); a pointer is a placement, owner of th |
| 2 | routed | appendix/d-4, cell 44, row "settling time, total mass" | routed | The bracketed second value is not said to be anything in the rendered text; a gloss needs new content |
| 3 | define | appendix/d-4, cell 44, row "tau, frac_above_, n_eff_" | not applied | a define adds words (a gloss or expansion) and the term is the one the glossary, ledger or main text uses; left |
| 4 | split | appendix/d-4, cell 44, closing line | not applied | not applied in this pass: left; no edit made |
| 5 | split | appendix/d-7, D.7 cell 49 | not applied | claims row C506 quotes the sentence as written |
| 6 | cut | appendix/d-7, D.8 cell 51 | not applied | claims row C152 quotes it |
| 7 | routed | appendix/d-7, D.8 cell 51 | routed | "levels 1 to 3" is used with no statement of what the levels are in this appendix; naming them is new content, owner of the certificate section |
| 8 | split | appendix/d-7, D.8 cell 53 | applied | cell 53: split; "seam" replaced by "cell boundary" |
| 9 | split | appendix/d-7, D.8 cell 53 | applied | cell 53: split; "seam" replaced by "cell boundary" |
| 10 | split | appendix/d-7, D.8 cell 53 | applied | cell 53: split; "seam" replaced by "cell boundary" |
| 11 | split | appendix/d-9, D.11 cell 60 | applied | generate_results.stability: split; "in this paper" and the repeat of the column title cut |
| 12 | split | appendix/d-9, D.11 cell 60 | applied | generate_results.stability: split after the jitter range; the count is its own sentence |
| 13 | split | appendix/d-9, D.11 cell 60 | applied | generate_results.stability: split; "in this paper" and the repeat of the column title cut |
| 14 | define | appendix/d-9, D.11 cell 60 | not applied | a define adds words (a gloss or expansion) and the term is the one the glossary, ledger or main text uses; left |
| 15 | split | appendix/d-9, D.11 cell 60 | applied | generate_results.stability: split; "in this paper" and the repeat of the column title cut |
| 16 | cut | appendix/d-9, D.11 cell 60 | applied | generate_results.stability: split; "in this paper" and the repeat of the column title cut |
| 17 | routed | appendix/d-12, D.12 para 1 | routed | "Restricted Hessian" is used before it is defined (the third paragraph says what is restricted); a reorder is a placement |
| 18 | split | appendix/d-12, D.12 para 2 | applied | cell 61: the restated clause and the pointer to the table rows cut (claims C423, C424 re-pointed or still quote) |
| 19 | cut | appendix/d-12, D.12 para 2 | applied | cell 61: the restated clause and the pointer to the table rows cut (claims C423, C424 re-pointed or still quote) |
| 20 | cut | appendix/d-12, D.12 para 2 | applied | cell 61: the restated clause and the pointer to the table rows cut (claims C423, C424 re-pointed or still quote) |
| 21 | cut | appendix/d-12, D.12 para 3 | applied | cell 61: the function and file name cut |
| 22 | keep | appendix/d-12, D.12 para 4 | left | keep |
| 23 | define | appendix/d-13, D.13 | not applied | a define adds words (a gloss or expansion) and the term is the one the glossary, ledger or main text uses; left |
| 24 | cut | appendix/d-13, D.13 | applied | cell 63: the repository paths cut |
| 25 | cut | appendix/d-13, D.14 | applied | cell 66: cut; the pointer to Section 9 stays with D.14's heading and the main text |
| 26 | split | appendix/d-13, D.14 | applied | cell 66: three sentences; the repository paths cut |
| 27 | cut | appendix/d-13, D.14 | applied | cell 66: three sentences; the repository paths cut |
| 28 | split | appendix/d-13, D.15 | not applied | not applied in this pass: left; no edit made |
| 29 | split | appendix/d-13, D.15 | not applied | not applied in this pass: left; no edit made |
| 30 | split | appendix/d-13, D.15 | not applied | not applied in this pass: left; no edit made |
| 31 | define | appendix/d-13, D.16 | not applied | a define adds words (a gloss or expansion) and the term is the one the glossary, ledger or main text uses; left |
| 32 | split | appendix/d-13, D.16 | not applied | not applied in this pass: left; no edit made |
| 33 | cut | appendix/d-13, D.16 | not applied | not applied in this pass: left; no edit made |

## appendix-13

| Row | Flag | Surface and location | Result | Note |
|---|---|---|---|---|
| 1 | split | appendix/d-15, cell 68, para 1 | applied | cell 69: definition of the movement promoted to its own sentence; "the temperature of the fits the case analysis shows" cut; colon sentence split (claim C154 re-pointed) |
| 2 | keep | appendix/d-15, cell 68, para 1 | left | keep |
| 3 | split | appendix/d-15, cell 68, para 1 | applied | cell 69: definition of the movement promoted to its own sentence; "the temperature of the fits the case analysis shows" cut; colon sentence split (claim C154 re-pointed) |
| 4 | split | appendix/d-15, cell 68, para 1 | applied | cell 69: definition of the movement promoted to its own sentence; "the temperature of the fits the case analysis shows" cut; colon sentence split (claim C154 re-pointed) |
| 5 | cut | appendix/d-15, cell 68, para 1 | applied | cell 69: definition of the movement promoted to its own sentence; "the temperature of the fits the case analysis shows" cut; colon sentence split (claim C154 re-pointed) |
| 6 | define | appendix/d-15, cell 68, para 1 | not applied | a define adds words (a gloss or expansion) and the term is the one the glossary, ledger or main text uses; left |
| 7 | split | appendix/d-15, cell 68, para 1 | applied | cell 69: definition of the movement promoted to its own sentence; "the temperature of the fits the case analysis shows" cut; colon sentence split (claim C154 re-pointed) |
| 8 | define | appendix/d-15, cell 68, para 1 | applied | cell 69: definition of the movement promoted to its own sentence; "the temperature of the fits the case analysis shows" cut; colon sentence split (claim C154 re-pointed) |
| 9 | define | appendix/d-16, cell 71, para 1 | applied | cell 72: split at the semicolon |
| 10 | split | appendix/d-16, cell 71, para 1 | applied | cell 72: split at the semicolon |
| 11 | cut | appendix/d-16, cell 71, para 1 | not applied | claims row C159 quotes "the second is computed from the first's coordinates"; the sentence stays |
| 12 | keep | appendix/d-16, cell 71, para 1 | left | keep |
| 13 | split | appendix/d-17, cell 74, para 1 | applied | cell 74: announcement, derived launch figure, code path and the unit variants cut; the first table's columns follow "Its columns are" |
| 14 | cut | appendix/d-17, cell 74, para 1 | applied | cell 74: announcement, derived launch figure, code path and the unit variants cut; the first table's columns follow "Its columns are" |
| 15 | define | appendix/d-17, cell 74, para 1 | applied | cell 74: announcement, derived launch figure, code path and the unit variants cut; the first table's columns follow "Its columns are" |
| 16 | cut | appendix/d-17, cell 74, para 1 | applied | cell 74: announcement, derived launch figure, code path and the unit variants cut; the first table's columns follow "Its columns are" |
| 17 | split | appendix/d-17, cell 74, para 2 | not applied | the column list kept (the table's own columns); the definition in parentheses stays (claim C505 quotes the excess-column sentence) |
| 18 | cut | appendix/d-17, cell 74, para 2 | applied | cell 74: announcement, derived launch figure, code path and the unit variants cut; the first table's columns follow "Its columns are" |
| 19 | split | appendix/d-17, cell 74, para 2 | not applied | the column list kept (the table's own columns); the definition in parentheses stays (claim C505 quotes the excess-column sentence) |
| 20 | keep | appendix/d-17, cell 74, para 2 | left | keep |
| 21 | keep | appendix/d-17, cell 74, para 2 | left | keep |
| 22 | cut | appendix/d-17, cell 74, para 2 | applied | cell 74: announcement, derived launch figure, code path and the unit variants cut; the first table's columns follow "Its columns are" |
| 23 | cut | appendix/d-17, cell 74, para 2 | applied | cell 74: announcement, derived launch figure, code path and the unit variants cut; the first table's columns follow "Its columns are" |
| 24 | keep | appendix/d-17, cell 74, para 2 | left | keep |
| 25 | split | appendix/d-17, cell 74, para 3 | applied | cell 76: code paths cut; two splits (claim C499 re-pointed) |
| 26 | cut | appendix/d-17, cell 74, para 3 | applied | cell 76: code paths cut; two splits (claim C499 re-pointed) |
| 27 | split | appendix/d-17, cell 74, para 3 | applied | cell 76: code paths cut; two splits (claim C499 re-pointed) |
| 28 | split | appendix/d-17, cell 74, para 3 | applied | cell 76: code paths cut; two splits (claim C499 re-pointed) |
| 29 | define | appendix/d-17, cell 74, para 3 | not applied | a define adds words (a gloss or expansion) and the term is the one the glossary, ledger or main text uses; left |
| 30 | routed | appendix/d-17, cell 74, para 3 | routed | A repository path in reader-facing prose; a link with words or a cut, but placement is the owning package's (WP23 record); supervisor list. |
| 31 | split | appendix/d-17, cell 74, table 3 caption | not applied | not applied in this pass: left; no edit made |
| 32 | routed | appendix/d-17, cell 74, para 1 | routed | Column heads use "contending set" and "zero set" with no definition in the appendix; a table change, not copy-editing. |
| 33 | define | appendix/d-18, cell 78, para 1 | applied | cell 78 and generate_results.injected_noise (claim C463 still quotes the sentence it has) |
| 34 | cut | appendix/d-18, cell 78, para 1 | applied | cell 78 and generate_results.injected_noise (claim C463 still quotes the sentence it has) |
| 35 | split | appendix/d-18, cell 78, para 1 | applied | cell 78 and generate_results.injected_noise (claim C463 still quotes the sentence it has) |
| 36 | cut | appendix/d-18, cell 78, para 1 | applied | cell 78 and generate_results.injected_noise (claim C463 still quotes the sentence it has) |
| 37 | keep | appendix/d-18, cell 78, para 1 | left | keep |
| 38 | split | appendix/d-18, cell 78, table lead | applied | generate_results.injected_noise: split; "as a design choice of this experiment" cut |
| 39 | cut | appendix/d-18, cell 78, table lead | applied | generate_results.injected_noise: split; "as a design choice of this experiment" cut |
| 40 | split | appendix/d-18, cell 78, table lead | applied | generate_results.injected_noise: split; "as a design choice of this experiment" cut |
| 41 | routed | appendix/d-18, cell 78, table lead | routed | Points at a column that does not exist in the rendered table (the last column is the Jaccard); a table or sentence mismatch, not copy-editing. |
| 42 | keep | appendix/d-18, cell 78, table lead | left | keep |
| 43 | cut | appendix/d-19, cell 80, para 1 | applied | cell 80/83: announcement, repeated "cheapest unit cost", the script path and "exact" cut |
| 44 | split | appendix/d-19, cell 80, para 1 | not applied | not applied in this pass: left; no edit made |
| 45 | split | appendix/d-19, cell 80, para 1 | applied | cell 80: colon sentence split (claims C620, C621 re-pointed) |
| 46 | define | appendix/d-19, cell 80, para 1 | not applied | a define adds words (a gloss or expansion) and the term is the one the glossary, ledger or main text uses; left |
| 47 | cut | appendix/d-19, cell 80, para 1 | applied | cell 80/83: announcement, repeated "cheapest unit cost", the script path and "exact" cut |
| 48 | keep | appendix/d-19, cell 80, para 1 | left | keep |
| 49 | cut | appendix/d-19, cell 80, para 1 | applied | cell 80/83: announcement, repeated "cheapest unit cost", the script path and "exact" cut |
| 50 | split | appendix/d-19, cell 80, cubesat-primary text | not applied | not applied in this pass: left; no edit made |
| 51 | keep | appendix/d-19, cell 80, cubesat-stock text | left | keep |
| 52 | split | appendix/d-19, cell 80, table lead | applied | cell 80/83: announcement, repeated "cheapest unit cost", the script path and "exact" cut |
| 53 | cut | appendix/d-19, cell 80, table lead | applied | cell 80/83: announcement, repeated "cheapest unit cost", the script path and "exact" cut |
| 54 | define | appendix/d-19, cell 80, table lead | not applied | a define adds words (a gloss or expansion) and the term is the one the glossary, ledger or main text uses; left |

## appendix-14

| Row | Flag | Surface and location | Result | Note |
|---|---|---|---|---|
| 1 | cut | appendix/appendix-e, cell 85, job block | not applied | not applied in this pass: the sentence is generated from a table or the abstraction-gaps ledger and was not hand-edited |
| 2 | routed | appendix/appendix-e, cell 85, job block | routed | restates the table header and says G-17 while the table runs to G-18 (a number; owner: the paper's appendix package) |
| 3 | cut | appendix/appendix-e, cell 85, job block | not applied | not applied in this pass: the sentence is generated from a table or the abstraction-gaps ledger and was not hand-edited |
| 4 | split | appendix/appendix-e, G-1 sensitivity | not applied | not applied in this pass: the sentence is generated from a table or the abstraction-gaps ledger and was not hand-edited |
| 5 | split | appendix/appendix-e, G-1 sensitivity | applied | abstraction-gaps.md G-1: the clause after the semicolon is its own sentence |
| 6 | keep | appendix/appendix-e, G-1 formal object | left | keep |
| 7 | split | appendix/appendix-e, G-1 consequence | applied | abstraction-gaps.md G-1: three sentences |
| 8 | define | appendix/appendix-e, G-2 formal object | not applied | a define adds words (a gloss or expansion) and the term is the one the glossary, ledger or main text uses; left |
| 9 | define | appendix/appendix-e, G-2 formal object | applied | abstraction-gaps.md G-2: "that matrix" named the restricted Hessian |
| 10 | split | appendix/appendix-e, G-2 bridging | applied | abstraction-gaps.md G-2: three sentences |
| 11 | keep | appendix/appendix-e, G-2 sensitivity | left | keep |
| 12 | split | appendix/appendix-e, G-2 sensitivity | not applied | not applied in this pass: the sentence is generated from a table or the abstraction-gaps ledger and was not hand-edited |
| 13 | split | appendix/appendix-e, G-2 sensitivity | not applied | not applied in this pass: the sentence is generated from a table or the abstraction-gaps ledger and was not hand-edited |
| 14 | keep | appendix/appendix-e, G-2 sensitivity | left | keep |
| 15 | split | appendix/appendix-e, G-2 consequence | applied | abstraction-gaps.md G-2: split |
| 16 | split | appendix/appendix-e, G-3 formal object | not applied | not applied in this pass: the sentence is generated from a table or the abstraction-gaps ledger and was not hand-edited |
| 17 | define | appendix/appendix-e, G-3 formal object | not applied | a define adds words (a gloss or expansion) and the term is the one the glossary, ledger or main text uses; left |
| 18 | define | appendix/appendix-e, G-3 bridging | applied | abstraction-gaps.md G-3: split (i.i.d. left as it is) |
| 19 | split | appendix/appendix-e, G-3 cannot-prove | not applied | not applied in this pass: the sentence is generated from a table or the abstraction-gaps ledger and was not hand-edited |
| 20 | keep | appendix/appendix-e, G-3 sensitivity | left | keep |
| 21 | cut | appendix/appendix-e, G-3 sensitivity | applied | abstraction-gaps.md G-3: the truncated test name cut |
| 22 | split | appendix/appendix-e, G-3 consequence | applied | abstraction-gaps.md G-3: split |
| 23 | split | appendix/appendix-e, G-4 formal object | applied | abstraction-gaps.md G-4: split |
| 24 | cut | appendix/appendix-e, G-4 cannot-prove | applied | abstraction-gaps.md G-4: cut |
| 25 | keep | appendix/appendix-e, G-4 sensitivity | left | keep |
| 26 | keep | appendix/appendix-e, G-4 consequence | left | keep |
| 27 | define | appendix/appendix-e, G-5 title | not applied | a define adds words (a gloss or expansion) and the term is the one the glossary, ledger or main text uses; left |
| 28 | split | appendix/appendix-e, G-5 cannot-prove | applied | abstraction-gaps.md G-5: split |
| 29 | keep | appendix/appendix-e, G-5 sensitivity | left | keep |
| 30 | split | appendix/appendix-e, G-5 consequence | applied | abstraction-gaps.md G-5: split |
| 31 | keep | appendix/appendix-e, G-6 title | left | keep |
| 32 | define | appendix/appendix-e, G-6 formal object | not applied | a define adds words (a gloss or expansion) and the term is the one the glossary, ledger or main text uses; left |
| 33 | split | appendix/appendix-e, G-6 sensitivity | applied | abstraction-gaps.md G-6: the three results are separate sentences |
| 34 | cut | appendix/appendix-e, G-6 sensitivity | not applied | not applied in this pass: the sentence is generated from a table or the abstraction-gaps ledger and was not hand-edited |
| 35 | keep | appendix/appendix-e, G-6 consequence | left | keep |
| 36 | split | appendix/appendix-e, G-7 sensitivity | not applied | not applied in this pass: the sentence is generated from a table or the abstraction-gaps ledger and was not hand-edited |
| 37 | cut | appendix/appendix-e, G-7 sensitivity | applied | abstraction-gaps.md G-10: internal run numbers cut |
| 38 | split | appendix/appendix-e, G-7 sensitivity | not applied | not applied in this pass: the sentence is generated from a table or the abstraction-gaps ledger and was not hand-edited |
| 39 | split | appendix/appendix-e, G-8 formal object | not applied | not applied in this pass: the sentence is generated from a table or the abstraction-gaps ledger and was not hand-edited |
| 40 | define | appendix/appendix-e, G-8 sensitivity | not applied | a define adds words (a gloss or expansion) and the term is the one the glossary, ledger or main text uses; left |
| 41 | cut | appendix/appendix-e, G-8 sensitivity | not applied | not applied in this pass: the sentence is generated from a table or the abstraction-gaps ledger and was not hand-edited |
| 42 | cut | appendix/appendix-e, G-8 consequence | not applied | not applied in this pass: the sentence is generated from a table or the abstraction-gaps ledger and was not hand-edited |
| 43 | split | appendix/appendix-e, G-9 formal object | not applied | not applied in this pass: the sentence is generated from a table or the abstraction-gaps ledger and was not hand-edited |
| 44 | define | appendix/appendix-e, G-9 formal object | not applied | a define adds words (a gloss or expansion) and the term is the one the glossary, ledger or main text uses; left |
| 45 | split | appendix/appendix-e, G-9 bridging | not applied | not applied in this pass: the sentence is generated from a table or the abstraction-gaps ledger and was not hand-edited |
| 46 | split | appendix/appendix-e, G-9 sensitivity | not applied | not applied in this pass: the sentence is generated from a table or the abstraction-gaps ledger and was not hand-edited |
| 47 | split | appendix/appendix-e, G-9 sensitivity | not applied | not applied in this pass: the sentence is generated from a table or the abstraction-gaps ledger and was not hand-edited |
| 48 | define | appendix/appendix-e, G-9 consequence | not applied | a define adds words (a gloss or expansion) and the term is the one the glossary, ledger or main text uses; left |
| 49 | split | appendix/appendix-e, G-10 formal object | not applied | not applied in this pass: the sentence is generated from a table or the abstraction-gaps ledger and was not hand-edited |
| 50 | define | appendix/appendix-e, G-10 bridging | not applied | a define adds words (a gloss or expansion) and the term is the one the glossary, ledger or main text uses; left |
| 51 | cut | appendix/appendix-e, G-10 sensitivity | applied | abstraction-gaps.md G-10: the CI run numbers cut; the facts stay |
| 52 | cut | appendix/appendix-e, G-10 sensitivity | applied | abstraction-gaps.md G-10: the CI run numbers cut; the facts stay |
| 53 | keep | appendix/appendix-e, G-10 sensitivity | left | keep |
| 54 | define | appendix/appendix-e, G-10 sensitivity | not applied | a define adds words (a gloss or expansion) and the term is the one the glossary, ledger or main text uses; left |
| 55 | split | appendix/appendix-e, G-10 consequence | not applied | not applied in this pass: the sentence is generated from a table or the abstraction-gaps ledger and was not hand-edited |
| 56 | define | appendix/appendix-e, G-11 title | not applied | a define adds words (a gloss or expansion) and the term is the one the glossary, ledger or main text uses; left |
| 57 | split | appendix/appendix-e, G-11 formal object | not applied | not applied in this pass: the sentence is generated from a table or the abstraction-gaps ledger and was not hand-edited |
| 58 | split | appendix/appendix-e, G-11 sensitivity | not applied | not applied in this pass: the sentence is generated from a table or the abstraction-gaps ledger and was not hand-edited |
| 59 | keep | appendix/appendix-e, G-11 sensitivity | left | keep |
| 60 | cut | appendix/appendix-e, G-11 consequence | applied | abstraction-gaps.md G-11: the sentence about the paper's prose cut |
| 61 | split | appendix/appendix-e, G-11 consequence | applied | abstraction-gaps.md G-11: the sentence about the paper's prose cut |
| 62 | define | appendix/appendix-e, G-12 title | not applied | a define adds words (a gloss or expansion) and the term is the one the glossary, ledger or main text uses; left |
| 63 | split | appendix/appendix-e, G-12 cannot-prove | not applied | not applied in this pass: the sentence is generated from a table or the abstraction-gaps ledger and was not hand-edited |
| 64 | define | appendix/appendix-e, G-12 sensitivity | not applied | a define adds words (a gloss or expansion) and the term is the one the glossary, ledger or main text uses; left |
| 65 | keep | appendix/appendix-e, G-12 consequence | left | keep |
| 66 | keep | appendix/appendix-e, G-13 title | left | keep |
| 67 | cut | appendix/appendix-e, G-13 formal object | applied | abstraction-gaps.md G-13: the sentence that restates G-1 cut |
| 68 | cut | appendix/appendix-e, G-13 sensitivity | applied | abstraction-gaps.md G-10: internal run numbers cut |
| 69 | cut | appendix/appendix-e, G-13 sensitivity | not applied | not applied in this pass: the sentence is generated from a table or the abstraction-gaps ledger and was not hand-edited |
| 70 | split | appendix/appendix-e, G-13 consequence | not applied | not applied in this pass: the sentence is generated from a table or the abstraction-gaps ledger and was not hand-edited |
| 71 | keep | appendix/appendix-e, G-14 title | left | keep |
| 72 | split | appendix/appendix-e, G-14 formal object | not applied | not applied in this pass: the sentence is generated from a table or the abstraction-gaps ledger and was not hand-edited |
| 73 | keep | appendix/appendix-e, G-14 bridging | left | keep |
| 74 | cut | appendix/appendix-e, G-14 sensitivity | applied | abstraction-gaps.md G-10: internal run numbers cut |
| 75 | cut | appendix/appendix-e, G-14 consequence | applied | abstraction-gaps.md G-14: "no sentence claims" clause cut |
| 76 | cut | appendix/appendix-e, G-15 formal object | not applied | not applied in this pass: the sentence is generated from a table or the abstraction-gaps ledger and was not hand-edited |
| 77 | cut | appendix/appendix-e, G-15 bridging | applied | abstraction-gaps.md G-15: "usefully" and the history aside cut |
| 78 | split | appendix/appendix-e, G-15 sensitivity | applied | abstraction-gaps.md G-15: "usefully" and the history aside cut |
| 79 | split | appendix/appendix-e, G-15 consequence | not applied | not applied in this pass: the sentence is generated from a table or the abstraction-gaps ledger and was not hand-edited |
| 80 | define | appendix/appendix-e, G-16 title | not applied | a define adds words (a gloss or expansion) and the term is the one the glossary, ledger or main text uses; left |
| 81 | split | appendix/appendix-e, G-16 formal object | not applied | not applied in this pass: the sentence is generated from a table or the abstraction-gaps ledger and was not hand-edited |
| 82 | split | appendix/appendix-e, G-16 bridging | not applied | not applied in this pass: the sentence is generated from a table or the abstraction-gaps ledger and was not hand-edited |
| 83 | keep | appendix/appendix-e, G-16 cannot-prove | left | keep |
| 84 | define | appendix/appendix-e, G-16 sensitivity | not applied | a define adds words (a gloss or expansion) and the term is the one the glossary, ledger or main text uses; left |
| 85 | cut | appendix/appendix-e, G-16 sensitivity | not applied | not applied in this pass: the sentence is generated from a table or the abstraction-gaps ledger and was not hand-edited |
| 86 | keep | appendix/appendix-e, G-16 consequence | left | keep |
| 87 | keep | appendix/appendix-e, G-16 consequence | left | keep |
| 88 | define | appendix/appendix-e, G-17 title | not applied | a define adds words (a gloss or expansion) and the term is the one the glossary, ledger or main text uses; left |
| 89 | split | appendix/appendix-e, G-17 bridging | not applied | not applied in this pass: the sentence is generated from a table or the abstraction-gaps ledger and was not hand-edited |
| 90 | split | appendix/appendix-e, G-17 sensitivity | not applied | not applied in this pass: the sentence is generated from a table or the abstraction-gaps ledger and was not hand-edited |
| 91 | split | appendix/appendix-e, G-17 sensitivity | not applied | not applied in this pass: the sentence is generated from a table or the abstraction-gaps ledger and was not hand-edited |
| 92 | split | appendix/appendix-e, G-17 sensitivity | not applied | not applied in this pass: the sentence is generated from a table or the abstraction-gaps ledger and was not hand-edited |
| 93 | keep | appendix/appendix-e, G-17 sensitivity | left | keep |
| 94 | cut | appendix/appendix-e, G-17 consequence | applied | abstraction-gaps.md G-17: the second clause cut |
| 95 | cut | appendix/appendix-e, G-17 consequence | not applied | not applied in this pass: the sentence is generated from a table or the abstraction-gaps ledger and was not hand-edited |
| 96 | define | appendix/appendix-e, G-18 title | not applied | a define adds words (a gloss or expansion) and the term is the one the glossary, ledger or main text uses; left |
| 97 | split | appendix/appendix-e, G-18 formal object | not applied | not applied in this pass: the sentence is generated from a table or the abstraction-gaps ledger and was not hand-edited |
| 98 | cut | appendix/appendix-e, G-18 bridging | applied | abstraction-gaps.md G-18: the restating clause cut |
| 99 | cut | appendix/appendix-e, G-18 cannot-prove | applied | abstraction-gaps.md G-18: the restating clause cut |
| 100 | split | appendix/appendix-e, G-18 sensitivity | not applied | not applied in this pass: the sentence is generated from a table or the abstraction-gaps ledger and was not hand-edited |
| 101 | cut | appendix/appendix-e, G-18 sensitivity | applied | abstraction-gaps.md G-18: "triage finding A5" cut |
| 102 | cut | appendix/appendix-e, G-18 sensitivity | not applied | not applied in this pass: the sentence is generated from a table or the abstraction-gaps ledger and was not hand-edited |
| 103 | keep | appendix/appendix-e, G-18 consequence | left | keep |
| 104 | cut | appendix/appendix-e, G-18 consequence | not applied | not applied in this pass: the sentence is generated from a table or the abstraction-gaps ledger and was not hand-edited |
| 105 | cut | appendix/appendix-e, G-18 consequence | applied | abstraction-gaps.md G-18: the restating clause cut |

## appendix-15

| Row | Flag | Surface and location | Result | Note |
|---|---|---|---|---|
| 1 | routed | appendix/appendix-f, cell 88, opening | routed | The Job / Main text keeps / carries / repository keeps frame is a structure shared by every appendix; routed to the owner of the appendix frame, not a per-appen |
| 2 | routed | appendix/appendix-f, cell 88, opening | routed | Lists the headings F.1 to F.4 that follow; the shared frame, so routed |
| 3 | routed | appendix/appendix-f, cell 88, opening | routed | Says what is not here; part of the shared frame |
| 4 | define | appendix/appendix-f, F.1 | not applied | a define adds words (a gloss or expansion) and the term is the one the glossary, ledger or main text uses; left |
| 5 | cut | appendix/appendix-f, F.1 | applied | generate_repro.py: "(format revision 3)" dropped from the pin |
| 6 | define | appendix/appendix-f, F.2 | not applied | F.2 sentences are backed by claims rows C-F.2 (RECORD.md) that quote them |
| 7 | cut | appendix/appendix-f, F.2 | not applied | F.2 sentences are backed by claims rows C-F.2 (RECORD.md) that quote them |
| 8 | cut | appendix/appendix-f, F.2 | not applied | F.2 sentences are backed by claims rows C-F.2 (RECORD.md) that quote them |
| 9 | cut | appendix/appendix-f, F.2 | not applied | F.2 sentences are backed by claims rows C-F.2 (RECORD.md) that quote them |
| 10 | split | appendix/appendix-f, F.3 intro | applied | cell 94: the tail clause is now a participle |
| 11 | split | appendix/appendix-f, F.3 table, notebooks row | applied | generate_repro.py: the first check is its own sentence |
| 12 | split | appendix/appendix-f, F.3 table, regenerate_row row | not applied | not applied in this pass: left; no edit made |
| 13 | split | appendix/appendix-f, F.3 table, build row | applied | generate_repro.py: split |
| 14 | routed | appendix/appendix-f, F.4 | routed | The same parenthetical repeats in about thirty rows of a generated table; one fix at the generator, not thirty cuts here |
| 15 | define | appendix/appendix-g, cell 98, Job | applied | cells 99, 100 |
| 16 | routed | appendix/appendix-g, cell 98, frame | routed | Shared appendix frame; routed with the other appendices |
| 17 | routed | appendix/appendix-g, cell 98, frame | routed | 70-plus words, nested parentheses and colons, two repository paths; frame sentence, routed with the shared frame |
| 18 | keep | appendix/appendix-g, cell 98 | left | keep |
| 19 | cut | appendix/appendix-g, cell 98 | applied | cells 99, 100 |
| 20 | split | appendix/appendix-g, cell 98 | applied | cells 99, 100 |
| 21 | routed | appendix/g-1, Pareto, Why this is not just | routed | The "Why this is not just the neighbour" field restates the "does differently" field in most entries (Pareto, DEA, production, frontiers, PCA, log-ratio, GP, tr |
| 22 | define | appendix/g-1, DEA, What this shares | not applied | a define adds words (a gloss or expansion) and the term is the one the glossary, ledger or main text uses; left |
| 23 | split | appendix/g-1, DEA, What it does | applied | prior_art.yaml |
| 24 | define | appendix/g-1, DEA, differently | not applied | a define adds words (a gloss or expansion) and the term is the one the glossary, ledger or main text uses; left |
| 25 | define | appendix/g-1, DEA, differently | not applied | a define adds words (a gloss or expansion) and the term is the one the glossary, ledger or main text uses; left |
| 26 | split | appendix/g-1, Multiplicative DEA, What it does | applied | prior_art.yaml |
| 27 | keep | appendix/g-1, Multiplicative DEA, What it does | left | keep |
| 28 | split | appendix/g-1, Hyperbolic graph, What it does | not applied | not applied in this pass: left; no edit made |
| 29 | cut | appendix/g-1, Deterministic and stochastic frontiers | applied | prior_art.yaml |
| 30 | split | appendix/g-1, PCA, differently | applied | prior_art.yaml |
| 31 | split | appendix/g-1, PCA, Why this is not just | not applied | not applied in this pass: left; no edit made |
| 32 | define | appendix/g-1, Compositional and log-ratio PCA | not applied | a define adds words (a gloss or expansion) and the term is the one the glossary, ledger or main text uses; left |
| 33 | split | appendix/g-1, Compositional and log-ratio PCA | not applied | not applied in this pass: left; no edit made |
| 34 | define | appendix/g-1, GP and max-affine, What it does | not applied | a define adds words (a gloss or expansion) and the term is the one the glossary, ledger or main text uses; left |
| 35 | define | appendix/g-1, GP and max-affine, shares | not applied | a define adds words (a gloss or expansion) and the term is the one the glossary, ledger or main text uses; left |
| 36 | split | appendix/g-1, HoroPCA, What it does | not applied | not applied in this pass: left; no edit made |
| 37 | split | appendix/g-1, HoroPCA, differently | not applied | not applied in this pass: left; no edit made |
| 38 | cut | appendix/g-1, HoroPCA, differently | applied | prior_art.yaml |
| 39 | keep | appendix/g-1, Entropic risk, differently | left | keep |
| 40 | define | appendix/g-1, Entropic risk, What it does | not applied | a define adds words (a gloss or expansion) and the term is the one the glossary, ledger or main text uses; left |
| 41 | split | appendix/g-1, MDAO, What it does | not applied | not applied in this pass: left; no edit made |
| 42 | define | appendix/g-1, MDAO, What it does | not applied | a define adds words (a gloss or expansion) and the term is the one the glossary, ledger or main text uses; left |
| 43 | keep | appendix/g-1, MDAO, differently | left | keep |
| 44 | split | appendix/g-1, Tradespace, What it does | not applied | not applied in this pass: left; no edit made |
| 45 | define | appendix/g-1, Decision analysis, What it does | not applied | a define adds words (a gloss or expansion) and the term is the one the glossary, ledger or main text uses; left |
| 46 | split | appendix/g-1, MBSE, What it does | not applied | not applied in this pass: left; no edit made |
| 47 | cut | appendix/g-1, G.1 closing | not applied | pinned by tests/test_paper.py (the pointer to Appendix H sits beside the row it tests) |

## appendix-16

| Row | Flag | Surface and location | Result | Note |
|---|---|---|---|---|
| 1 | split | appendix/systems-engineering-practice-and-decision-analys, cell 102, MDAO "What it does" | applied | prior_art.yaml: MDAO entry |
| 2 | define | appendix/systems-engineering-practice-and-decision-analys, cell 102, MDAO "What it does" | applied | prior_art.yaml: MDAO entry |
| 3 | cut | appendix/systems-engineering-practice-and-decision-analys, cell 102, MDAO "What it does" | applied | prior_art.yaml: MDAO entry |
| 4 | keep | appendix/systems-engineering-practice-and-decision-analys, cell 102, MDAO title paragraph | left | keep |
| 5 | split | appendix/systems-engineering-practice-and-decision-analys, cell 102, MDAO "shares" | applied | prior_art.yaml: MDAO entry |
| 6 | split | appendix/systems-engineering-practice-and-decision-analys, cell 102, MDAO "differently" | applied | prior_art.yaml: MDAO entry |
| 7 | keep | appendix/systems-engineering-practice-and-decision-analys, cell 102, MDAO "differently" | left | keep |
| 8 | split | appendix/systems-engineering-practice-and-decision-analys, cell 102, TSE "does" | applied | prior_art.yaml: tradespace entry |
| 9 | cut | appendix/systems-engineering-practice-and-decision-analys, cell 102, TSE "does" | applied | prior_art.yaml: tradespace entry |
| 10 | cut | appendix/systems-engineering-practice-and-decision-analys, cell 102, TSE "Why this is not just the neighbour" | not applied | not applied in this pass: left; no edit made |
| 11 | split | appendix/systems-engineering-practice-and-decision-analys, cell 102, TSE heading | not applied | not applied in this pass: left; no edit made |
| 12 | split | appendix/systems-engineering-practice-and-decision-analys, cell 102, decision analysis "does" | applied | prior_art.yaml: decision analysis entry |
| 13 | define | appendix/systems-engineering-practice-and-decision-analys, cell 102, decision analysis "does" | applied | prior_art.yaml: decision analysis entry |
| 14 | split | appendix/systems-engineering-practice-and-decision-analys, cell 102, trade studies "differently" | applied | prior_art.yaml: trade studies entry |
| 15 | split | appendix/systems-engineering-practice-and-decision-analys, cell 102, trade studies "does" | applied | prior_art.yaml: trade studies entry |
| 16 | define | appendix/systems-engineering-practice-and-decision-analys, cell 102, MBSE "does" | not applied | a define adds words (a gloss or expansion) and the term is the one the glossary, ledger or main text uses; left |
| 17 | split | appendix/systems-engineering-practice-and-decision-analys, cell 102, MBSE "does" | not applied | not applied in this pass: left; no edit made |
| 18 | keep | appendix/systems-engineering-practice-and-decision-analys, cell 102, closing | left | keep |
| 19 | split | appendix/g-2, cell 104, intro | applied | cell 104 |
| 20 | cut | appendix/g-2, cell 104, intro | applied | cell 104 |
| 21 | define | appendix/g-2, cell 104, intro | applied | cell 104 |
| 22 | keep | appendix/g-2, cell 104, table, Where in it | left | keep |
| 23 | keep | appendix/g-2, cell 104, table, Where in it | left | keep |
| 24 | keep | appendix/g-2, cell 104, table, row Cobb and Douglas | left | keep |
| 25 | keep | appendix/g-2, cell 104, table, rows Allen 1997 and Dyson 2001 | left | keep |
| 26 | define | appendix/g-2, cell 104, table, row Charnes et al. 1978 | not applied | a define adds words (a gloss or expansion) and the term is the one the glossary, ledger or main text uses; left |
| 27 | cut | appendix/g-2, cell 104, table, row Battese 1992 | not applied | not applied in this pass: left; no edit made |
| 28 | keep | appendix/g-2, cell 104, table, rows Aigner and Chu to Aigner et al. 1977 | left | keep |
| 29 | define | appendix/g-2, cell 104, table, row Battese 1992 | not applied | a define adds words (a gloss or expansion) and the term is the one the glossary, ledger or main text uses; left |
| 30 | cut | appendix/g-2, cell 104, table, row Hoburg et al. 2016 | not applied | not applied in this pass: left; no edit made |
| 31 | split | appendix/g-2, cell 104, table, row Zargham 2026 | not applied | not applied in this pass: left; no edit made |
| 32 | keep | appendix/appendix-h-horopca-beside-this-work-a-tested-hyp, cell 106, Job block | left | keep |
| 33 | define | appendix/appendix-h-horopca-beside-this-work-a-tested-hyp, cell 106, Job block | not applied | Appendix H: every number, claim, threshold and reading limit is pinned by claims rows C570 to C594 and tests; edits go down only and none was safe beyond the one listed |
| 34 | split | appendix/appendix-h-horopca-beside-this-work-a-tested-hyp, cell 106, H.1 | not applied | Appendix H: every number, claim, threshold and reading limit is pinned by claims rows C570 to C594 and tests; edits go down only and none was safe beyond the one listed |
| 35 | cut | appendix/appendix-h-horopca-beside-this-work-a-tested-hyp, cell 106, H.1 | not applied | Appendix H: every number, claim, threshold and reading limit is pinned by claims rows C570 to C594 and tests; edits go down only and none was safe beyond the one listed |
| 36 | split | appendix/appendix-h-horopca-beside-this-work-a-tested-hyp, cell 106, H.1 | not applied | Appendix H: every number, claim, threshold and reading limit is pinned by claims rows C570 to C594 and tests; edits go down only and none was safe beyond the one listed |
| 37 | split | appendix/appendix-h-horopca-beside-this-work-a-tested-hyp, cell 106, H.1 | not applied | Appendix H: every number, claim, threshold and reading limit is pinned by claims rows C570 to C594 and tests; edits go down only and none was safe beyond the one listed |
| 38 | split | appendix/appendix-h-horopca-beside-this-work-a-tested-hyp, cell 106, H.1 | not applied | Appendix H: every number, claim, threshold and reading limit is pinned by claims rows C570 to C594 and tests; edits go down only and none was safe beyond the one listed |
| 39 | split | appendix/appendix-h-horopca-beside-this-work-a-tested-hyp, cell 106, H.1 | not applied | Appendix H: every number, claim, threshold and reading limit is pinned by claims rows C570 to C594 and tests; edits go down only and none was safe beyond the one listed |
| 40 | keep | appendix/appendix-h-horopca-beside-this-work-a-tested-hyp, cell 106, H.1 | left | keep |
| 41 | define | appendix/appendix-h-horopca-beside-this-work-a-tested-hyp, cell 106, H.1 | not applied | Appendix H: every number, claim, threshold and reading limit is pinned by claims rows C570 to C594 and tests; edits go down only and none was safe beyond the one listed |
| 42 | split | appendix/appendix-h-horopca-beside-this-work-a-tested-hyp, cell 106, H.1 | not applied | Appendix H: every number, claim, threshold and reading limit is pinned by claims rows C570 to C594 and tests; edits go down only and none was safe beyond the one listed |
| 43 | keep | appendix/appendix-h-horopca-beside-this-work-a-tested-hyp, cell 106, H.1 | left | keep |
| 44 | cut | appendix/appendix-h-horopca-beside-this-work-a-tested-hyp, cell 106, H.2 | not applied | Appendix H: every number, claim, threshold and reading limit is pinned by claims rows C570 to C594 and tests; edits go down only and none was safe beyond the one listed |
| 45 | split | appendix/appendix-h-horopca-beside-this-work-a-tested-hyp, cell 106, H.2 | not applied | Appendix H: every number, claim, threshold and reading limit is pinned by claims rows C570 to C594 and tests; edits go down only and none was safe beyond the one listed |
| 46 | keep | appendix/appendix-h-horopca-beside-this-work-a-tested-hyp, cell 106, H.2 | left | keep |
| 47 | keep | appendix/appendix-h-horopca-beside-this-work-a-tested-hyp, cell 106, H.3 | left | keep |
| 48 | cut | appendix/appendix-h-horopca-beside-this-work-a-tested-hyp, cell 106, H.3 | not applied | Appendix H: every number, claim, threshold and reading limit is pinned by claims rows C570 to C594 and tests; edits go down only and none was safe beyond the one listed |
| 49 | keep | appendix/appendix-h-horopca-beside-this-work-a-tested-hyp, cell 106, H.3 | left | keep |
| 50 | routed | appendix/appendix-h-horopca-beside-this-work-a-tested-hyp, cell 106, H.3 | not applied | Appendix H: every number, claim, threshold and reading limit is pinned by claims rows C570 to C594 and tests; edits go down only and none was safe beyond the one listed |
| 51 | keep | appendix/appendix-h-horopca-beside-this-work-a-tested-hyp, cell 106, H.3 | left | keep |
| 52 | split | appendix/appendix-h-horopca-beside-this-work-a-tested-hyp, cell 106, H.4 | not applied | Appendix H: every number, claim, threshold and reading limit is pinned by claims rows C570 to C594 and tests; edits go down only and none was safe beyond the one listed |
| 53 | cut | appendix/appendix-h-horopca-beside-this-work-a-tested-hyp, cell 106, H.4 | applied | cell 117: "The methods are complementary, and" cut (claim C580 still quotes the rest) |
| 54 | keep | appendix/appendix-h-horopca-beside-this-work-a-tested-hyp, cell 106, H.4 | left | keep |
| 55 | keep | appendix/appendix-h-horopca-beside-this-work-a-tested-hyp, cell 106, H.4 | left | keep |
| 56 | split | appendix/appendix-h-horopca-beside-this-work-a-tested-hyp, cell 106, H.4 reading limits (a) | not applied | Appendix H: every number, claim, threshold and reading limit is pinned by claims rows C570 to C594 and tests; edits go down only and none was safe beyond the one listed |
| 57 | cut | appendix/appendix-h-horopca-beside-this-work-a-tested-hyp, cell 106, H.4 reading limits (a) | not applied | Appendix H: every number, claim, threshold and reading limit is pinned by claims rows C570 to C594 and tests; edits go down only and none was safe beyond the one listed |
| 58 | split | appendix/appendix-h-horopca-beside-this-work-a-tested-hyp, cell 106, H.4 reading limits (b) | not applied | Appendix H: every number, claim, threshold and reading limit is pinned by claims rows C570 to C594 and tests; edits go down only and none was safe beyond the one listed |
| 59 | cut | appendix/appendix-h-horopca-beside-this-work-a-tested-hyp, cell 106, H.4 reading limits (c) | not applied | Appendix H: every number, claim, threshold and reading limit is pinned by claims rows C570 to C594 and tests; edits go down only and none was safe beyond the one listed |
| 60 | keep | appendix/appendix-h-horopca-beside-this-work-a-tested-hyp, cell 106, H.4 reading limits | left | keep |
| 61 | keep | appendix/appendix-h-horopca-beside-this-work-a-tested-hyp, cell 106, H.5 | left | keep |
| 62 | define | appendix/appendix-h-horopca-beside-this-work-a-tested-hyp, cell 106, H.5 | not applied | Appendix H: every number, claim, threshold and reading limit is pinned by claims rows C570 to C594 and tests; edits go down only and none was safe beyond the one listed |
| 63 | split | appendix/appendix-h-horopca-beside-this-work-a-tested-hyp, cell 106, H.5 | not applied | Appendix H: every number, claim, threshold and reading limit is pinned by claims rows C570 to C594 and tests; edits go down only and none was safe beyond the one listed |
| 64 | define | appendix/appendix-h-horopca-beside-this-work-a-tested-hyp, cell 106, H.5 | not applied | Appendix H: every number, claim, threshold and reading limit is pinned by claims rows C570 to C594 and tests; edits go down only and none was safe beyond the one listed |
| 65 | keep | appendix/appendix-h-horopca-beside-this-work-a-tested-hyp, cell 106, H.5 | left | keep |

## glossary-appendix-a

| Row | Flag | Surface and location | Result | Note |
|---|---|---|---|---|
| 1 | routed | `appendix/appendix-a`, cell 2, scaffold line 1 | not applied | left; no edit made |
| 2 | routed | `appendix/appendix-a`, cell 2, scaffold line 2 | not applied | left; no edit made |
| 3 | routed | `appendix/appendix-a`, cell 2, scaffold line 3 | not applied | left; no edit made |
| 4 | routed | `appendix/appendix-a`, cell 2, scaffold line 4 | not applied | left; no edit made |
| 5 | routed | `appendix/appendix-a`, cell 2, code echo | not applied | left; no edit made |
| 6 | keep | `appendix/appendix-a`, cell 2, row "attributes", Meaning | left | keep |
| 7 | cut | `appendix/appendix-a`, cell 2, row "attributes", Not | applied | glossary.yaml: the clause after "metrics" cut |
| 8 | cut | `appendix/appendix-a`, cell 2, row "conditioning", Not | applied | glossary.yaml: "the fit consumes metrics" cut |
| 9 | split | `appendix/appendix-a`, cell 2, row "hyperbolic", Meaning | applied | glossary.yaml: split into two sentences (claim C534 re-pointed) |
| 10 | define | `appendix/appendix-a`, cell 2, row "hyperbolic", Not | applied | glossary.yaml: "principal component analysis" written out |
| 11 | cut | `appendix/appendix-a`, cell 2, row "monomial term", Not | applied | glossary.yaml: the parenthesis cut |
| 12 | split | `appendix/appendix-a`, cell 2, row "generalized posynomial", Not | applied | glossary.yaml: the parenthesis cut |
| 13 | cut | `appendix/appendix-a`, cell 2, row "generalized posynomial", Defined in | applied | glossary.yaml: "the one cited sentence of the Methods" cut |
| 14 | split | `appendix/appendix-a`, cell 2, row "geometric program", Not | applied | glossary.yaml: split so the exception stands apart |
| 15 | split | `appendix/appendix-a`, cell 2, row "generalized geometric program", Meaning | applied | glossary.yaml: split |
| 16 | split | `appendix/appendix-a`, cell 2, row "generalized geometric program", Not | applied | glossary.yaml: "and so is the fit with its weights given" cut; the rest left (the design-problem clause is a claim) |
| 17 | cut | `appendix/appendix-a`, cell 2, row "fitted reference surface", Not | applied | glossary.yaml: second half of the Not cell cut |
| 18 | define | `appendix/appendix-a`, cell 2, row "frontier", Meaning | applied | glossary.yaml: "of the three" replaced by "object" |
| 19 | keep | `appendix/appendix-a`, cell 2, row "energy differential", Meaning | left | keep |
| 20 | define | `appendix/appendix-a`, cell 2, row "reach", Meaning | not applied | J_tau(U w_k) is the notation the register is there to define |
| 21 | keep | `appendix/appendix-a`, cell 2, row "numerically zero", Meaning | left | keep |
| 22 | split | `appendix/appendix-a`, cell 2, row "certificate", Meaning | applied | glossary.yaml: split into two sentences |
| 23 | define | `appendix/appendix-a`, cell 2, row "conditioning of the exponents", Meaning | not applied | a define adds words; the terms are the ones Boyd and Vandenberghe use |
| 24 | split | `appendix/appendix-a`, cell 2, row "ridge", Not | applied | glossary.yaml: split |
| 25 | keep | `appendix/appendix-a`, cell 2, row "novelty", Meaning | left | keep |
| 26 | split | `appendix/appendix-a`, cell 2, row "ternary plot", Meaning | applied | glossary.yaml: coordinate formulas cut; split |
| 27 | routed | `appendix/appendix-a`, cell 2, row "ternary plot", Defined in | applied | glossary.yaml: coordinate formulas cut; split |
| 28 | define | `appendix/appendix-a`, cell 2, row "MoE", Meaning | not applied | a define adds words; MoE and MoP are the system model's own marks |
| 29 | define | `appendix/appendix-a`, cell 2, row "MoP", Meaning | not applied | a define adds words; MoE and MoP are the system model's own marks |
| 30 | routed | `appendix/appendix-a`, cell 2, rows "MoE" and "MoP", Defined in | not applied | left; no edit made |
| 31 | routed | `appendix/appendix-a`, cell 2, row "launch cost", Defined in | not applied | left; no edit made |
| 32 | routed | `appendix/appendix-a`, cell 2, "Defined in" column throughout | not applied | left; no edit made |

## glossary-01

| Row | Flag | Surface and location | Result | Note |
|---|---|---|---|---|
| 1 | split | glossary/long-forms, assignment.short | not this unit | docs glossary page short form (unit L3-case) |
| 2 | split | glossary/long-forms, certificate.short | not this unit | docs glossary page short form (unit L3-case) |
| 3 | define | glossary/long-forms, conditioning.short | not this unit | docs glossary page short form (unit L3-case) |
| 4 | define | glossary/long-forms, contending set.short | not this unit | docs glossary page short form (unit L3-case) |
| 5 | split | glossary/long-forms, energy differential.short | not this unit | docs glossary page short form (unit L3-case) |
| 6 | keep | glossary/long-forms, fitted reference surface.short | not this unit | docs glossary page short form (unit L3-case) |
| 7 | keep | glossary/long-forms, frontier.short | not this unit | docs glossary page short form (unit L3-case) |
| 8 | define | glossary/long-forms, generalized geometric program.short | not this unit | docs glossary page short form (unit L3-case) |
| 9 | define | glossary/long-forms, geometric program.short | not this unit | docs glossary page short form (unit L3-case) |
| 10 | cut | glossary/long-forms, hyperbolic.short | not this unit | docs glossary page short form (unit L3-case) |
| 11 | split | glossary/long-forms, launch cost.short | not this unit | docs glossary page short form (unit L3-case) |
| 12 | split | glossary/long-forms, mean slack.short | not this unit | docs glossary page short form (unit L3-case) |
| 13 | cut | glossary/long-forms, monomial term.short | not this unit | docs glossary page short form (unit L3-case) |
| 14 | routed | glossary/long-forms, MoP.short | not this unit | docs glossary page short form (unit L3-case) |
| 15 | keep | glossary/long-forms, MoE.short | not this unit | docs glossary page short form (unit L3-case) |
| 16 | split | glossary/long-forms, near-frontier band.short | not this unit | docs glossary page short form (unit L3-case) |
| 17 | keep | glossary/long-forms, numerically zero.short | not this unit | docs glossary page short form (unit L3-case) |
| 18 | define | glossary/long-forms, participation threshold.short | not this unit | docs glossary page short form (unit L3-case) |
| 19 | define | glossary/long-forms, conditioning of the exponents.short | not this unit | docs glossary page short form (unit L3-case) |
| 20 | split | glossary/long-forms, ridge.short | not this unit | docs glossary page short form (unit L3-case) |
| 21 | cut | glossary/long-forms, row share.short | not this unit | docs glossary page short form (unit L3-case) |
| 22 | split | glossary/long-forms, term share.short | not this unit | docs glossary page short form (unit L3-case) |
| 23 | keep | glossary/long-forms, termination status.short | not this unit | docs glossary page short form (unit L3-case) |
| 24 | keep | glossary/long-forms, effective sample size.short | not this unit | docs glossary page short form (unit L3-case) |
| 25 | routed | paper/supporting-material, Appendix A, opening block | not applied | left; no edit made |
| 26 | split | paper/supporting-material, Appendix A, row `geometric program`, Not | applied | glossary.yaml: split so the exception stands apart |
| 27 | split | paper/supporting-material, Appendix A, row `generalized geometric program`, Not | applied | glossary.yaml: "and so is the fit with its weights given" cut; the rest left (the design-problem clause is a claim) |
| 28 | cut | paper/supporting-material, Appendix A, row `generalized posynomial`, Not | applied | glossary.yaml: the parenthesis cut |
| 29 | cut | paper/supporting-material, Appendix A, row `monomial`, Not | applied | glossary.yaml: the parenthesis cut |
| 30 | define | paper/supporting-material, Appendix A, row `hyperbolic`, Not | applied | glossary.yaml: "principal component analysis" written out |
| 31 | define | paper/supporting-material, Appendix A, row `numerically zero`, Meaning | applied | glossary.yaml: the code constant replaced by its value |
| 32 | split | paper/supporting-material, Appendix A, row `ridge`, Not | applied | glossary.yaml: split |
| 33 | keep | paper/supporting-material, Appendix A, row `certificate`, Meaning | left | keep |
| 34 | split | paper/supporting-material, Appendix A, row `ternary plot`, Meaning | applied | glossary.yaml: coordinate formulas cut; split |
| 35 | routed | paper/supporting-material, Appendix A, rows `MoE`, `MoP`, Defined in | not applied | left; no edit made |
| 36 | routed | paper/supporting-material, Appendix A, row `launch cost`, Defined in | not applied | left; no edit made |
| 37 | keep | paper/supporting-material, Appendix A, row `launch cost`, Meaning | left | keep |

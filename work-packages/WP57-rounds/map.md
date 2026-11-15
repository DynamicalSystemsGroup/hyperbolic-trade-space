# WP57 map: the appendices against the paper (G1)

Read against `paper/supporting_material.ipynb` at dev `c89843a` and `paper/paper.ipynb` as WP55 leaves it (branch
`wp55`). Counts come from `work-packages/WP57-rounds/map_counts.py` (`uv run python work-packages/WP57-rounds/map_counts.py
--paper <wp55 copy>`): prose words are the typed markdown of a subsection (headings, anchor lines and directive fences
excluded); generated words are the stored outputs of its code cells; rows are the body rows of the rendered tables;
cells count markdown and code cells from a heading to the next. Register rows are the ids in `claims_register.toml`
whose `file` is the supporting material or a generator; rows filed with an empty anchor are placed by their fragment.
Citing sentences are the paper's sentences holding a `{ref}` to the anchor, by section number; a generated sentence
that links the anchor through `appendix_link` in `paper/generate_findings.py` is marked "(generated)".

A disposition is one of: **keep** (the step deeper its citing sentence needs); **shorten** (to what is named);
**move** (to the named path, cited from the appendix in one line); **cut**. "Pending WP56" marks a row whose citing
sentences all sit in Sections 7 to 9; the call given is provisional and is re-read when WP56 lands.

Moved generated tables land as files under `paper/supplement/` written by the same generator functions through a
small script (`paper/generate_supplement.py`), so nothing is typed; moved typed prose lands in the repository page
named. The totals are in section 5.

## 1. The appendices, subsection by subsection

### Front matter (cell 0)

| Anchor, title | Cited by | Prose / generated / cells | Opines or narrates | Register | Disposition | No longer does |
|---|---|---|---|---|---|---|
| (title cell) Companion paragraph | none | 44 / 0 / 2 (with the import cell) | narrates the document: "Companion to the paper, for readers who check the proofs (Appendix B), reproduce the results ..." | none | cut the paragraph; the title and the import cell stay | tells the reader which appendix is for whom; the headings carry it |

### Appendix A. Notation and terms (3 cells; 83 prose, 2,946 generated, 72 rows)

| Anchor, title | Cited by | Prose / generated / cells | Opines or narrates | Register | Disposition | No longer does |
|---|---|---|---|---|---|---|
| `appendix-a`, Job block | S3 "Appendix A is the full register of symbols and terms"; S5 "the lemma scripts write the shift and the attribute with other letters" | 83 / 0 / 2 | yes, three sentences whose subject is the appendix: "This appendix carries: one table ... compiled from `glossary.yaml` and never typed" | C131 | cut the Job block | says what the main text, the appendix and the repository each keep; the heading and the table say it |
| `appendix-a`, the register table (`register_table`) | the same two sentences | 0 / 2,946 / 1 | no | none (the glossary's own rows C415, C534, C817 to C819 back glossary text) | shorten: the generator takes the entries the paper or the appendices use (62 of 72 today; the 10 unused are `binding-term`, `characteristic-point`, `position-along-the-frontier`, `row-share`, `termination-status`, `conditioning-of-the-exponents`, `ternary-plot` and the three `number-of-*` symbol entries, which stay as symbols); the Layer column goes (empty in 62 rows) | lists glossary entries no sentence of the paper uses, and a layer column almost always blank |

Also found: four `defined_in` cells read "WP51-decisions.md (the supervisor, 2026-11-14 night)" and "WP11-decisions.md
(the supervisor, ...)", a repository record named inside the paper's table. The field lives in `glossary.yaml`; the
child names the defining place in the paper or the package instead (a glossary edit, not a notebook edit).

### Appendix B. Proofs, step for step with their scripts (10 cells; 635 prose, 33,606 generated, 603 rows)

| Anchor, title | Cited by | Prose / generated / cells | Opines or narrates | Register | Disposition | No longer does |
|---|---|---|---|---|---|---|
| `appendix-b`, Job block | S3 "convex in w (Appendix B, L4)"; S4 "a sum of monomials (Appendix B, L10)"; S5 eight pointers (L5, L4.14 to L4.24, L16, L5.25, L9, L10); S6 "Proof: Appendix B, Ln" on every result, L3.9, L17.13, L17.19; S9 "gives one line of code to read each proof step against" | 112 of 237 / 0 / 2 (shared with the next row) | yes: "This appendix carries: per proof, in the paper's numbering ..." | none | cut the Job block | says what the main text keeps and what the repository keeps |
| `appendix-b`, "What the scripts establish" | S9 "Verify and validate" and S11 "scripted checks in place of pencil and paper"; `docs/user-guide/limitations.md` "Appendix B of the paper states what they do and do not establish" | 125 of 237 / 0 / (same cell) | no (its subject is the scripts) | C387, C388, C389 | keep | |
| `appendix-b`, `how_to_read` | the same | 0 / ~250 / 1 | yes, two places: "The appendix has two parts"; the closing paragraph repeats S9's sentence ("What it cannot establish is that a sentence means what its line computes; that reading is the human validation") | none | shorten in `generate_proofs.how_to_read`: keep the rule (one file per proof, one line per step, the tag) and the three kinds with their counts; drop the two-parts list and the closing paragraph | repeats Section 9's verify-and-validate sentence and narrates the page's structure |
| `appendix-b`, `proof_map` | every "Proof: Appendix B, Ln" | 0 / ~640 / 1 (24 rows) | no | none | keep | |
| `sub-b-1`, B.1 The fit and its geometry (L1 to L11), `proofs_fit` | the S6 proof pointers for L1 to L11 | 0 / 10,805 / 2 (184 rows) | no (generated from the record) | none | keep | |
| `sub-b-2`, B.2 "The algorithm" paragraph | S5 "is read after the fit (steps: Appendix B.2)"; S6 "Newton steps that close the gap the solver leaves (Appendix B.2)" | 398 / 0 / 1 | yes: "L19 bounds the noise shift of the offset, and no result or table of this paper uses it"; the lemma-by-lemma commentary ("L16 does not prove ...", "L17 treats ...", "L21 is the tension of ...") narrates the proof tables that follow; the alternation, the labels and eq-slack restate Section 5 | C132 to C146, C666, C667 (17 rows) | shorten to about 120 words: what the two citing sentences need and Section 5 does not say, the restart rule (random centres in the chart, the restart with the smallest mean slack returned), the stop rule, the polish (five reduced Newton steps after each SLSQP refit, the joint polish, G-16) and that the status refers to the polished point; "L16 does not prove that the alternation converges" goes to the assumptions section (C142); the rest of the commentary goes | restates Section 5's alternation, labels and program; comments on each lemma before its table; says which results the paper does not use |
| `sub-b-2`, `proofs_solver` (L12 to L22) | the S6 proof pointers for L12 to L17, L20, L21; A10 and A11 for L18, L19 | 0 / 21,317 / 1 (365 rows) | no | none | keep; L22 (small-temperature expansion) is the one result no paper sentence cites (`docs/user-guide/temperature.md` cites it); the appendix presents the record whole and the record is R-4's | |
| `sub-b-3`, B.3 The checker and the record, `checker` | S11 "a proof map from each result to its steps" (the step deeper) | 0 / 596 / 2 (30 rows) | no | none | keep | |

### Appendix C. The case's model (20 cells; 789 prose, 3,322 generated, 175 rows)

| Anchor, title | Cited by | Prose / generated / cells | Opines or narrates | Register | Disposition | No longer does |
|---|---|---|---|---|---|---|
| `appendix-c`, Job block and opening | S7 "Appendix C describes the model behind the evaluation and names each dataset" | 172 / 0 / 2 | yes: "To let a reader judge whether the case ... is a fair test"; and two sentences that are in Section 7 word for word ("The cubesat case is a worked example of design optimization, not a study of either use"; "In this design loop the simulation is how the attributes are measured ...") | C032 (the duplicated sentence), C147 | pending WP56; provisional: cut the opening cell; C032 re-anchors to Section 7, where the sentence stays; C147 retires with the Job block | repeats two Section 7 sentences and judges the case |
| `sub-c-1`, C.1 The configuration space | S7 Figure 1 caption "so are the ranges, which the view does not draw (Appendix C.1)"; S7 "0.03 to 1 in the stock (baseline) regime (Appendix C.1)"; S8 "whose gains were sampled over a lower range (Appendix C.1)" | 0 / 157 / 2 (7 rows) | no | none | pending WP56; keep | |
| `sub-c-2`, C.2 The evaluation (`evaluation`, `attribute_sources`) | S7's sentence above (the thread from attribute to file and function) | 0 / 342 / 3 (31 rows) | no | none | pending WP56; keep | |
| `sub-c-3`, C.3 Feasibility | S7 "Four are the feasibility conditions, which remove designs ..." (the counts removed) | 0 / 189 / 2 (10 rows) | no | none | pending WP56; keep | |
| `sub-c-4`, C.4 Conditioning | S5 "The case's conditioning rule is Appendix C.4's" | 0 / 532 / 2 (26 rows) | no | none | keep | |
| `sub-c-5`, C.5 The table of metrics (`metric_table`, `metric_associations`) | S7 (generated) `participation_sentence` links C.5 | 51 / 1,901 / 4 (90 rows) | no | none | shorten: one five-row preview (the primary regime) and the pairs at \|Spearman\| at least 0.5 (11 of 78) with the one-axis sentence; the stock preview and the full 78-pair table move to `paper/supplement/metric-associations.md`, cited in one line | prints two previews of the same columns and 67 pairs below 0.5 that no reading uses |
| `sub-c-6`, C.6 The datasets | S7 "names each dataset"; every D table cites the labels | 0 / 113 / 2 (3 rows) | no | none | pending WP56; keep | |
| `sub-c-7`, C.7 The planted example | S7 "we plant it, with the generator of Appendix C.7" | 0 / 88 / 2 (8 rows) | no | none | pending WP56; keep | |
| `sub-c-8`, C.8 The cost model and what the case leaves out | S7 "the slot is up to 4.2 times the reported launch cost ... (Appendix C.8)"; S8 (generated) `decision_sentence` "the numbers are nominal (Appendix C.8)" | 566 / 0 / 1 | no (its subject is the model); the omission list explicates modelling assumptions at length, which the requirements place in the model and its record | C496, C497, C502, C503, C504 | pending WP56; provisional: shorten to the cost-model paragraph (about 160 words) plus the launch-slot item S7 cites (about 60); the "What the case leaves out" paragraph and the other four items move to `examples/adcs/case-model.md`, "What the case leaves out" (which carries four of the five in its own words and ends "The full list is Appendix C.8"), cited in one line; the mirror `work-packages/WP30-rounds/appendix-c-leaves-out.md` and the test clause that reads it follow (the paragraph is then the case page's); C497, C503, C504 re-anchor to the case page; WP56's "pricing detail ... moved to Appendix C" lands in the kept paragraph | explicates what the cubesat model omits, which the case page and the SysML v2 model record |

### Appendix D. Extended results (50 cells; 1,624 prose, 7,870 generated, 293 rows)

| Anchor, title | Cited by | Prose / generated / cells | Opines or narrates | Register | Disposition | No longer does |
|---|---|---|---|---|---|---|
| `appendix-d`, Job block | S8 "tables: Appendix D" | 220 / 0 / 2 | yes: "To let a reader check that the main text's summary of the analysis is fair, including the results that are mixed"; "Main text keeps: Section 8 in about 500 words ..." | none | pending WP56; provisional: cut the Job block (the test `test_c_and_d_each_point_to_the_other_in_their_opening` retires with it) | judges the main text's summary and lists the appendix's own contents |
| `sub-d-1`, D.1 Selection of the temperature | none (Figure 4 draws the sweep for the primary regime; the generated `temperature_sentence` in S7 states the fit temperature); the table's lead sentence points at "Section 7", stale (the rule is Section 5's) | 0 / 466 / 2 (26 rows) | no | none | move to `paper/supplement/temperature-sweep.md`; D keeps no row | tabulates both regimes' sweeps that the figure draws for one |
| `sub-d-2`, D.2 Diagnostics at K = 1, 2, 3 | none; S8 (generated) `k_temperatures_sentence` reads tau per K | 0 / 234 / 2 (6 rows) | no | none | merge into D.8: one table per regime with K, tau, band, loss, fraction above, term rows and shares, status, gamma, radius, bound; D.8's first table (its columns are a subset) goes | duplicates D.8's gap, status, margin, radius and bound and D.3's rows and shares |
| `sub-d-3`, D.3 Exponents and terms | S7 Figure 4's Does-not-show line (leaves with WP56's caption cleanup); S8 "its exponents are still read apart, Appendix D.3"; S8 (generated) `terms_sentence` "Appendix D.3 has the rows" | 0 / 1,752 / 2 (100 rows) | no | C805 (generated band sentence) | pending WP56; keep (K = 3 stays as the step deeper for S5 (iv) "K = 3 is certified too and adds a thin term") | |
| `sub-d-4`, D.4 The regimes side by side | S8 "separates the problem's contribution from the gains' (Appendix D.4)" | 0 / 148 / 2 (7 rows) | no | none | pending WP56; keep | |
| `sub-d-5`, D.5 Sensitivity variants | S5 "Halving or doubling that fraction leaves the contending sets unchanged, and a different scaler does not" | 0 / 418 / 2 (10 rows) | no | none (C628 backs the paper's generated scaler sentence) | keep | |
| `sub-d-6`, D.6 Refits by category | none | 0 / 260 / 2 (6 rows) | no | none | move to `paper/supplement/refits-by-category.md`; D keeps no row | reports six one-term fits by wheel class that no sentence reads |
| `sub-d-7`, D.7 Candidate designs | none (the test `test_the_candidates_paragraph_is_cut_and_the_table_stays_in_appendix_d` keeps it; the three designs also appear in D.17's second table with their levels) | 54 / 85 / 2 (3 rows) | no | C506 | merge into D.17: the sentence reading the two candidates beyond the thresholds-met surface sits under D.17's second table, which lists them; the three-row table goes; the test's clause changes | prints the candidates' levels twice |
| `sub-d-8`, D.8 The solver's termination records ("What each status asserts", `termination_records`, "How small is a small margin", `margin_reading`) | S6 "reported as stationary without margin, never certified (Appendix D.8)"; S6 "Each returned fit carries the levels it meets (Appendix D.8)"; S8 "the margin, gap and status of this fit are in ... Appendix D.8"; S6 (generated) `margin_sentence` | 192 / 286 / 4 (12 rows) | no | C148 to C152, C342 | keep; receives D.2's table and D.12's table | |
| `sub-d-9`, D.9 Comparison with nondominated sorting | S8 (generated) `nondominated_sentence` states the counts; S2 "Dominance ... stops discriminating, on this case, as metrics are added" | 0 / 76 / 2 (4 rows) | no | none | pending WP56 (G2: the generated sentence stays or goes to D); keep | |
| `sub-d-10`, D.10 Propose, predict, check | S8 "we then measure them (Appendix D.10)"; `docs/bridge.md` links it | 0 / 94 / 2 (3 rows) | no | none | pending WP56; keep | |
| `sub-d-11`, D.11 Stability under rounding-level jitter | S5 "checked under rounding-level jitter (Appendix D.11)"; S8 "digits that hold: D.11" | 0 / 445 / 2 (15 rows) | no | C395, C396 (generated) | keep | |
| `sub-d-12`, D.12 The conditioning of the exponents | none | 162 / 108 / 2 (12 rows) | no; the three italic paragraphs ("Why it matters", "How it is computed", "Inspecting your own problem") are user-guide prose: "Fit the conditioned metrics at a finite temperature and read the attribute" | C423, C424, C425, C441 | merge the table into D.8 with its one defining sentence (the smallest eigenvalue of the restricted Hessian at each term's fit); the three paragraphs move to `docs/user-guide/termination.md`, section `conditioning_`, which already holds the diagnostic's reading; C423, C425, C441 re-anchor there, C424 to the table's cell | instructs the reader in the package from inside the paper |
| `sub-d-13`, D.13 The refit on a term's own rows | S5 "recovered none of the 60 planted terms ... (at tau = infinity, Appendix D.13)" | 40 / 78 / 2 (2 rows) | yes: "Section 6 says what refitting a term on its own rows alone does ... Here the two refits are compared" (and the section named is now Section 5) | C153 | shorten to the one sentence the table needs ("the two refits are compared with the true labels given, so the alternation plays no part"); C153 retires or re-anchors to Section 5 | narrates the main text and names the wrong section |
| `sub-d-14`, D.14 Does the fit recover a planted answer | S6 "Appendix D.14 records fits that reach the iteration cap first"; S7 "the recovery of planted terms is read in Appendix D.14" | 47 / 449 / 3 (6 rows) | no | none (C631, C672, C801 back the paper's generated planted sentence) | keep | |
| `sub-d-15`, D.15 Choosing K for the case | S5 (iv) "the value the package's checks point to (Appendix D.15)"; S8 Figure 6 caption "the K the package's checks point to (Appendix D.15)" | 146 / 194 / 3 (8 rows) | the opener narrates: "Section 8 takes K from three checks of the package's choosing-K guide" | C154, C155 | keep; reword the opener to state the three checks directly | |
| `sub-d-16`, D.16 Chaining with PCA | S2 "use PCA as a downstream step (Appendix D.16)"; S8 Figure 6 caption "Appendix D.16 gives its share of the spread and its loadings"; H.4 | 90 / 84 / 3 (3 rows) | no | C156 to C160 | keep | |
| `sub-d-17`, D.17 The requirements read after the fit (two tables) | S7 "Appendix D.17 gives the values"; S7 "Appendix D.17 reads them after it"; S9 "Numerical. Appendix D.17 prices each of the six requirements" | 400 / 1,286 / 4 (34 rows) | no; the first paragraph spells out every column of the first table | C499, C505 | pending WP56 (G5 cuts or moves "Numerical"; G2 brings the requirements as constraints into S8); provisional: keep both tables; shorten the prose to the thresholds' values, the price's definition and the design sets' rule (about 250 words); receives D.7's sentence | glosses each column the table's header names |
| `sub-d-18`, D.18 The noise-ridge corollary against injected noise | none in the paper (Corollary 1's commentary ends "it does not say whether the elasticities are right" without a pointer) | 86 / 299 / 2 (8 rows) | the opener narrates: "Section 6 states that noise on the metrics shifts the exponents by a ridge (L20)" | C463, C662 (generated) | keep as the step deeper for Corollary 1 (the one measurement of the ridge against noisy fits); cut the opener; the missing pointer at Corollary 1 is a main-text edit outside WP57's non-goals, listed in section 6 for the driver | |
| `sub-d-19`, D.19 The decision: the shortlist and the rules | S8 Table 2 caption "the picks' other design variables ... are in Appendix D.19"; "The shortlist and the rules are in Appendix D.19" | 187 / 1,108 / 5 (28 rows) | the opener narrates: "The shortlist of Section 8 is ..."; "The rules the main text names pick from it" | C619 to C621; C609 to C614, C616, C626, C661 (generated in D.19's cells) | pending WP56 (G2 rewrites the decision with one stakeholder per objective); provisional: keep the shortlist table and the rules; state the rules directly; the stock-regime funnel sentence stays as the regime comparison | |

### Appendix E. Assumptions and abstraction gaps (3 cells; 92 prose, 3,951 generated, 18 rows)

| Anchor, title | Cited by | Prose / generated / cells | Opines or narrates | Register | Disposition | No longer does |
|---|---|---|---|---|---|---|
| `appendix-e`, Job block | S6 "Appendix E records what the results leave open"; S9 "Appendix E gives the ledger" | 92 / 0 / 2 | yes, and stale: "Main text keeps: the paragraph 'Map and territory' in Section 3" (Section 3 no longer holds it) | none | cut; E becomes "Assumptions, limitations and open questions" (section 2) | points at a paragraph the paper no longer has |
| `appendix-e`, `gaps_table` | the same two sentences | 0 / 3,951 / 1 (18 rows, six columns) | no | C507 backs the ledger itself | shorten in `generate_gaps.gaps_table`: four columns (gap, bridging assumption, what cannot be proved, interpretive consequence) with one link per row to the ledger row; the "Formal object" and "Sensitivity evidence" columns (the lemma statements in LaTeX and the M1 to M5 numbers) stay in `docs/superpowers/notes/abstraction-gaps.md` | reprints the ledger's formal statements and measurement numbers that its linked row holds |

### Appendix F. Computational reproducibility (10 cells; 257 prose, 1,340 generated, 72 rows)

| Anchor, title | Cited by | Prose / generated / cells | Opines or narrates | Register | Disposition | No longer does |
|---|---|---|---|---|---|---|
| `appendix-f`, Job block | S11 "The pinned toolchain, the environment of record and the commands are in Appendix F" | 116 / 0 / 2 | yes, three sentences: "Main text keeps: Section 11 in a few sentences ..." | none | cut | says what Section 11 and the repository keep |
| `sub-f-1`, F.1 The pinned toolchain | the same | 0 / 185 / 2 (17 rows) | no | none | keep | |
| `sub-f-2`, F.2 The environment of record | the same | 99 / 0 / 2 | no | C024 to C029 | keep | |
| `sub-f-3`, F.3 Commands | the same | 42 / 276 / 2 (8 rows) | no | none | keep | |
| `sub-f-4`, F.4 One row per figure and table | the same; `paper/regenerate_row.py` reads it | 0 / 879 / 2 (47 rows) | no | none | keep | |

### Appendix G. Register of prior art (8 cells; 252 prose, 4,523 generated, 53 rows)

| Anchor, title | Cited by | Prose / generated / cells | Opines or narrates | Register | Disposition | No longer does |
|---|---|---|---|---|---|---|
| `appendix-g`, Job block and scope sentence | S12 "the sources of the main text and of the register of Appendix G"; Section 2 names Table 1 and not Appendix G (the requirements say it names both) | 186 / 0 / 3 | yes: "To show that the prior art was surveyed, and answer in advance the objection that this work is just some existing method"; "Main text keeps: Section 2 in about 600 words" | C161 | cut the Job block; the scope sentence ("what each work says was read only in part") moves to the assumptions section as a limitation of the register | argues with an objection and counts Section 2's words |
| `sub-g-1`, G.1 The register (`register`) | S12 | 0 / 2,791 / 2 | no | C065, C069, C070, C074, C076, C084, C535 to C537 (in `prior_art.yaml`) | keep; the three layers' order is already its order | |
| `sub-g-1`, pointer cell "The HoroPCA entry above is tested by experiment in Appendix H" | none | 12 / 0 / 1 | yes, page narration | none | cut (the entry's own text cites Appendix H) | |
| `sub-g-2`, G.2 What the paper took from where (`reading_pass_table`) | S11 "No claim enters without ... a verified source" (the record of the verified sources) | 54 / 1,732 / 2 (53 rows) | its rows quote the paper's own sentences ("What we say") beside the source and the place read: a verification record of the text, not a step deeper into a result | none (the test `test_reading_pass_rows_carry_what_the_paper_does_and_resolve_in_the_bibliography` checks the YAML) | move to `paper/supplement/reading-pass.md` (written from `paper/reading_pass.yaml` by the same function), cited in one line at the end of G.1; the alternative, keep as S11's step deeper, is the driver's call (section 6) | prints a table about the paper's text inside the paper |

### Appendix H. HoroPCA beside this work (15 cells; 664 prose, 417 generated, 12 rows)

| Anchor, title | Cited by | Prose / generated / cells | Opines or narrates | Register | Disposition | No longer does |
|---|---|---|---|---|---|---|
| `appendix-h`, Job block | S2 "recovered the planted trade-offs only where they were the direction of largest spread" (one sentence, with the three boundaries in brief: an embedding of ours; defaults and one direction; clean tables, so a mechanism and not a rate) | 46 / 0 / 2 | yes: "This appendix carries: the experiment and its reading" | none | cut | |
| `sub-h-1`, H.1 The hypothesis and what would refute it (`horopca_conditions`) | the same | 190 / 98 / 2 | one sentence about the appendix: "This appendix is a prospectively specified follow-up to an exploratory spike that informed its design, a bounded synthetic experiment supporting the positioning, not a performance benchmark" | C570 to C573, C591 to C594, C595 (generated) | keep; cut that sentence (C591 retires); the rest states the hypothesis, the table kinds and the recovery threshold, which S2's sentence needs | describes itself |
| `sub-h-2`, H.2 The experiment | the same | 105 / 0 / 1 | no | C574 to C576 | keep | |
| `sub-h-3`, H.3 Results (threshold sentence, table, verdict, contrast) | the same | 45 / 271 / 6 (12 rows) | no | none typed (the generated sentences are tested) | keep | |
| `sub-h-4`, H.4 What the table shows and "Reading limits" | the same; the three boundaries (a), (b), (c) are the one step deeper | 180 / 48 / 3 | no | C577, C578, C580, C582, C583, C584, C590 | keep; the limits (a) to (c) are also listed in the assumptions section by reference, not repeated | |
| `sub-h-5`, H.5 How the formalism and the solvers differ | none; G.1's HoroPCA entry carries the same contrast ("it maximizes a nonconvex variance over frames by gradient ascent with restarts", C536; "by convex programs on a simplex with a certificate", C537) | 108 / 0 / 1 | no | C585 to C588 | cut; C585 to C588 retire against C536, C537 | repeats the register's "differs" field |

The whole-appendix alternative in `paper-requirements.md` ("else moved to the repository with one line in G") would
move 664 prose words and 15 cells, re-file 22 register rows (C570 to C594) and leave S2's kind-R sentence backed by
the generator and the record in `work-packages/WP35-rounds/spike-h/` alone. S2 states the three boundaries in brief,
so the map reads H as their step deeper and keeps it shortened; the choice is the driver's (section 6).

## 2. Assumptions, limitations and open questions

### 2.1 Inventory

Every assumption, caveat, limitation and open question stated in the main text (wp55) or the appendices, with where it
sits, what it assumes or leaves open, and its record. "Lemma" means the lemma scripts import the entry from
`derivation/axioms.py` (37 entries: A0 to A11, R1 to R3, I1 to I18, F5, F10, F12, F19). "Gap" is a row of
`docs/superpowers/notes/abstraction-gaps.md` (G-1 to G-18). "OQ" is a row of `work-packages/review/open-questions.md`.

**Section 2, Prior art**

| Where | Assumes or leaves open | Record |
|---|---|---|
| Pareto methods paragraph | dominance stops discriminating on this case as metrics are added (a reading of D.9's counts) | D.9; gap G-13 |
| HoroPCA paragraph | the comparison is on an embedding of ours, at the authors' defaults, one direction; clean tables, so a mechanism and not a rate | H.4 limits (a) to (c); `WP35-rounds/spike-h/readout.md` |

**Section 3, Preliminaries**

| Where | Assumes or leaves open | Record |
|---|---|---|
| "Three assumptions hold throughout" | A1 metrics strictly positive; A2 exponents on the simplex; A3 fit temperature positive, tau = infinity named where used | lemma A1, A2, A3 |

**Section 4, Definitions**

| Where | Assumes or leaves open | Record |
|---|---|---|
| Energy differential | log V is neither a physical energy nor a Euclidean distance (the analogy marked) | glossary `energy-differential`; C006 |
| The n-lemma | the contending set is found, not assumed; read at the exact maximum | glossary; G-12 |
| Tension | a rate along the fitted reference surface, not the effect of changing a design variable | L21; `def-tension` |

**Section 5, Methods**

| Where | Assumes or leaves open | Record |
|---|---|---|
| Conditioning | A4 log-affine, invertible conditioning; the choices define the question, so a stable fitted direction is not a context-free discovery; zero metrics mask their row without a warning; negatives rejected | lemma A4; L9; G-5; `docs/user-guide/conditioning.md` |
| Thresholds and ties | three thresholds are conventions (10^-12, 10^-9, 10^-3); a tie at the exact maximum is resolved by the platform | G-2, G-10 |
| Several terms | A6 kappa positive, terms on the simplex; F is not convex, the alternation is a heuristic with no global guarantee; A8 nonempty cells; the labels are an implementation choice, not an assumption | lemma A6, A8; L16 (i); G-14 |
| The certificate | three levels, none global; stationarity measured, not proved | L12 to L15; G-15, G-16 |
| Simplifying assumptions (i) to (vi) | one term at K = 1 has constant elasticities; sharp weights by default; the analyst chooses K; small K; log-affine conditioning; a log-convex surface, no K represents non-log-convex structure | L10, L16; G-1, G-9; `docs/user-guide/limitations.md` |

**Section 6, Results**

| Where | Assumes or leaves open | Record |
|---|---|---|
| R1 | at the exact maximum the balanced point lies in the relative interior of a facet with positive normal; it does not imply the finite-tau minimizer is interior | lemma R1; L3.9; G-2 |
| Convexity (L4) | convex, not claimed strictly; two identical columns leave the loss flat along their swap (S8) | L4; G-2 |
| A5, A9, A10, A11 | Gaussian noise assumptions, independent or with one covariance; multiplicative measurement error | lemma A5, A9, A10, A11; L6, L18, L19 |
| Gaussian cumulant (L6) | a population identity with no consistency claim | G-3, G-11 |
| R3 and Corollary 1 (L20) | strict complementarity and a positive definite covariance on the support; the shift is of the minimizer of the expected loss, not of one noisy fit; it does not say whether the elasticities are right; measured against injected noise in D.18, where the prediction exceeds the measurement in seven of eight rows | lemma R3; L20; D.18; G-3, G-11 |
| Elasticities (L7) | the reading is for metrics with sizeable exponents; the rates are the fit's own only where w_j > 0 at the fit temperature | L7; G-2 |
| Tension (L21) | does not say the surface is the right one, or give the tension at a seam | L21 |
| Pareto (L11) | weak efficiency; the converse is not claimed; only the log-convex part of the boundary is reached | L11; G-1; OQ-3 |
| Descent (L15) | the K^N + 1 bound is a pigeonhole count, not a practical stopping guarantee; stationarity of the stop and convergence otherwise are not claimed; fits that reach the cap are in D.14 | L15; G-14; D.14 |
| R2, the margin (L13) | a positive assignment margin; the radius is sufficient, not tight | lemma R2; L13; G-10, G-16 |
| Approximate certificate (L14) | for the returned run, not across restarts | L14; G-15 |
| Soft-fit certificate (L17) | holds at the exact point the polished fit approximates | L17; G-16 |
| The stopping declaration | certified is a status at the returned point, set by tolerances; measured, not proved | D.8; G-16 |

**Section 7, Case construction** (pending WP56)

| Where | Assumes or leaves open | Record |
|---|---|---|
| Requirements | the four threshold limits are illustrative values chosen by the share of designs each admits, not a mission's | D.17; the SysML v2 model |
| Costs | each cost is a lower bound on a full costing; the launch slot is not costed, so fleets of one to three are underpriced; hardware values are illustrative; no schedule, no payload, a flat launch price | C.8; `examples/adcs/case-model.md`; the model's `COVERAGE` text |

**Section 8, Case analysis** (pending WP56)

| Where | Assumes or leaves open | Record |
|---|---|---|
| Two regimes | which of a nearly coincident pair carries the exponent is not read as a finding | L4; D.3, D.4 |
| Three metrics at a time | the triples' fits are not the case's K = 2 fit | Figure 5's caption |
| Propose, predict, check | a check on a few proposals, not an estimate of a rate; turning a level into a bounded outcome can fail while the fit is certified | D.10; OQ-3; `docs/bridge.md` |
| The decision table | the method does not tell the schedule or the risk, what to buy beyond the modelled parts, or what a larger fleet is worth; the numbers are nominal | D.19; C.8 |

**Section 9, Discussion** (pending WP56; G5 moves "Three claims", "Why a surface" and "Numerical" out or to this section)

| Where | Assumes or leaves open | Record |
|---|---|---|
| Interpretation is human validation | exponents and elasticities describe how the sampled designs trade, not a causal exchange; white space is an opportunity only where the trade space is log-convex, which the data cannot prove; novelty is not preference | G-1, G-3; `docs/user-guide/limitations.md` |
| Verify and validate | machine verification does not show the hypotheses suit a table; the correspondence cannot say a sentence means what its line computes | B, "What the scripts establish"; `how_to_read` |
| Three claims | the certificate covers a local minimizer; that the surface describes the table is read from figures; that it holds outside the table or supports a decision needs its own validation | G-1, G-15; `docs/user-guide/termination.md` |
| Limits, in brief | a log-convex surface; one term tangent at one place, conservative off it; exponents depend on the conditioning; small samples determine exponents weakly; designed samples carry no sampling error | G-1, G-2, G-11, G-12 |
| Trade-offs beyond the first, and PCA | successive trade-offs after removing the last is a research question; trade-offs the sampling never exercised cannot appear | G-12, G-13; `docs/user-guide/choosing-k.md` |
| The kernel direction | which kernel expansions keep the fit a geometric program is open; nothing is built | `notes/directions/wp43-kernel-direction.md` |

**Section 10, Future work**: the three directions carry their boundaries in the readouts (`notes/directions/`); none
is stated as a caveat in the text.

**The appendices**

| Where | Assumes or leaves open | Record |
|---|---|---|
| B, "What the scripts establish" | a step checks the algebra under the ledger's assumptions, not that they hold for a table | B; `notes/proof-conventions.md` |
| B.2 | L16 does not prove that the alternation converges; L19 is used by no result or table | L16, L19; G-14 |
| C.8 | the omission list (pointing error a loop-and-tracker figure; momentum a one-slew reading; the launch slot; the scenario's choices; the rigid wings) | the SysML v2 model; `examples/adcs/case-model.md` |
| D.8 | the stable radius is sufficient, not tight | L13 |
| D.14 | at the exact maximum the failing tables' status depends on the platform (G-10); the count does not | G-10 |
| D.16 | the principal directions are a reading of the sampled designs, not part of the model | D.16 |
| D.17 | the price is a feature of the fitted model on this table, not a causal exchange; the two cost limits are budget limits, so a set constrained by them would be a fleet-size choice | D.17; `WP23-rounds/spikes/` |
| D.18 | the conditioning is refitted on each noisy table, which L18 does not cover; eight draws are few | D.18; `examples/adcs/noise_injection.py` |
| E | the eighteen gaps, each with what cannot be proved (G-14 global convergence not pursued; G-11 no consistency theorem; G-13 recovery measurable only where the boundary is planted; G-18 equal mean slack does not identify the boundary) | `docs/superpowers/notes/abstraction-gaps.md` |
| F.2 | byte-for-byte reproduction only in the image of record; elsewhere within tolerances | F.2; C024 to C029 |
| G | the register is not exhaustive; what each work says was read only in part | G.2; `paper/reading_pass.yaml` |
| H.4 | the embedding is part of the treatment; clean, non-tree-like tables; six tables per cell establish separation, not rates | H.4; C582, C583, C590 |

**The ledger** (`work-packages/review/open-questions.md`; all four left the old Section 7 with WP54)

| Id | Open | Record |
|---|---|---|
| OQ-1 | the search's outer loop is conjectured outward in expectation (a submartingale); no conditions derived | `WP36-decisions.md`; `notes/directions/wp41-bridge-to-the-search.md` sections 1 and 5; `docs/bridge.md` |
| OQ-2 | a convergence result for the nested scheme once expected progress ceases; variables treated as continuous within a category | `WP36-decisions.md`; the gaps ledger row that names it |
| OQ-3 | whether ascent reaches beyond the log-convex part of the boundary; a design built to a predicted improvement need not follow it | `notes/directions/wp41-bridge-to-the-search.md` sections 3 and 5 |
| OQ-4 | how a sampling strategy enters the nested loops; the method assumes nothing about how designs were drawn | `paper/length_ledger.toml`, the raise row of 2026-11-11 |

Repeats found across surfaces (one point per place): the S9 verify-and-validate sentence and `how_to_read`'s
closing paragraph; S7's launch-slot sentence and C.8's launch item (the main text keeps the brief form, C.8 the
numbers); S9 "Limits, in brief" and `docs/user-guide/limitations.md` (two surfaces, allowed); the HoroPCA contrast in
G.1 and H.5. No caveat is repeated inside the main text itself at wp55; WP56 owns Sections 7 to 9.

### 2.2 The proposed shape of the section

Appendix E becomes **"Assumptions, limitations and open questions"**, in three parts, each one list or table and no
prose about the page:

1. **Assumptions.** One table: id, statement in one line, where the main text states it, the results that use it
   (from the proof map's "Ledger entries imported" column). Rows A0 to A11 and R1 to R3 (15), in the order of the ledger;
   the I-entries (results of the literature) and F-entries (formal devices) listed by id with their citation in one
   line each, since the main text names them only by id ("I10 (the first-order conditions)"). Generated from
   `derivation/axioms.py` by a small addition to `generate_gaps.py`, never typed.
2. **Limitations.** The inventory of 2.1 grouped by the section each item left (Sections 2 to 9, then the
   appendices), one line per item: what is not established, and its record (a gap id, a lemma, a subsection). The
   gaps table follows, in its four-column form, as the record the lines point at. Items pending WP56 are written when
   WP56 lands.
3. **Open questions.** OQ-1 to OQ-4 from the ledger, one line each with the record, and the research questions
   Section 9 names (successive trade-offs; the kernel direction) by one line each pointing at `notes/directions/`.

Each item appears once; a caveat that Section 6 states at its result is listed here with a pointer, not restated. The
section's generated parts (the assumptions table, the gaps table) carry no register rows of their own; the typed lines
do, one per item that makes a claim.

## 3. The children

Grouping from the map: G joins WP57a (no pending-WP56 row, no dependency on the assumptions section; cut-and-move
work like A and F); H stays with E in WP57d (both read the paper's limits). Order: a, b before WP56 lands if the driver
wishes (no row of theirs is pending); c after WP56; d after c (it lists what C and D still state and receives what
WP56's Discussion moves out); e last.

| Child | Appendices | What it does | Words removed (prose / generated) and moved | Files it touches | Order |
|---|---|---|---|---|---|
| WP57a | front matter, A, F, G | cuts the four Job blocks, the companion paragraph and G's pointer cell; filters A's register to the entries the paper uses and drops the Layer column; fixes the four `defined_in` fields that name decision files; moves G.2's reading-pass table to `paper/supplement/reading-pass.md` with one line in G; moves G's scope sentence to the assumptions section's queue | prose −480 (front 44, A 83, F 116, G 237: the Job block and scope 186, the pointer 12, G.2's introduction 54, less the one citing line); generated −~2,180 (A ~450 filtered, G.2 1,732 moved) | `paper/supporting_material.ipynb` (cells 0, 3, 89, 99, 100, 103, 104, 105); `paper/generate_register.py`; `paper/generate_supplement.py` (new) and `paper/supplement/reading-pass.md`; `glossary.yaml` (`defined_in`); `claims_register.toml` (C131, C161); `tests/test_paper.py` (`test_reading_pass_table_is_in_appendix_g_and_current`, the G.2 cell test); `paper/length_ledger.toml` (cut rows under "Appendix G"); `scripts/residuals_baseline.json`, `scripts/vocabulary_baseline.toml` | 1 |
| WP57b | B | cuts B's Job block; shortens `how_to_read` (the rule and the kinds; no two-parts list, no verify-and-validate repeat); shortens B.2 to the restart, stop and polish rules the two citing sentences need; queues "L16 does not prove convergence" for the assumptions section; keeps the proof map, the step tables and the checker | prose −~390 (Job 112, B.2 278); generated −~60 | `paper/supporting_material.ipynb` (cells 6, 11); `paper/generate_proofs.py` (`how_to_read`); `claims_register.toml` (C132 to C146, C666, C667: retire or re-anchor); `tests/test_paper.py` (`test_the_claims_of_c1_have_their_true_basis`, `test_appendix_b_shows_every_result_of_the_record_with_derived_counts`); `paper/length_ledger.toml` ("Appendix B" cut rows); residuals baseline | 2 |
| WP57c | C, D | re-reads every pending row at WP56's landing; cuts C's opening and D's Job block; shortens C.5 (one preview, pairs at or above 0.5) and C.8 (the cost paragraph and the slot item), moving the rest to the supplement and the case page; moves D.1 and D.6 to the supplement; merges D.2 and D.12's table into D.8 and D.7 into D.17; moves D.12's paragraphs to the termination page; cuts the narrating openers of D.13, D.15, D.18, D.19; shortens D.17's prose; receives what WP56 moves into C and D | prose −~1,140 (C 518: 172 cut, 346 moved; D 619: 220 cut, 130 moved, the rest merged or shortened); generated −~2,340 (C 1,400 moved; D 466 + 260 moved, 215 merged); rows −~115 | `paper/supporting_material.ipynb` (C and D cells); `paper/generate_model.py` (`metric_table`, `metric_associations`); `paper/generate_results.py` (`termination_records` absorbs `k_diagnostics` and `conditioning_diagnostic`; `design_sets_comparison` absorbs the candidates' sentence); `paper/generate_supplement.py` and `paper/supplement/{metric-associations,temperature-sweep,refits-by-category}.md`; `examples/adcs/case-model.md`; `docs/user-guide/termination.md`; `work-packages/WP30-rounds/appendix-c-leaves-out.md`; `claims_register.toml` (C032, C147 to C153, C342, C423 to C425, C441, C496, C497, C503, C504, C506); `tests/test_paper.py` (about 12 tests, among them `test_c_and_d_each_point_to_the_other_in_their_opening`, `test_the_candidates_paragraph_is_cut_and_the_table_stays_in_appendix_d`, `test_appendix_c8_states_what_the_model_file_says_about_cost_and_what_is_left_out`, `test_appendix_d_prints_the_conditioning_diagnostic`, `test_no_table_or_figure_appears_in_both_c_and_d`); `paper/length_ledger.toml` ("Appendix C", "Appendix D" cut rows); both baselines | 3 (after WP56) |
| WP57d | E, H | builds "Assumptions, limitations and open questions" in the shape of 2.2 (the assumptions table generated from the axiom ledger; the limitations list from 2.1 with the WP56 rows filled; the open questions from the ledger); shortens the gaps table to four columns; cuts H's Job block, its self-description sentence and H.5; checks that no caveat listed is repeated in the main text and reports any repeat to the driver (a main-text edit is outside the scope) | prose: E −92, +~450 (the new lists); H −179 (Job 46, the self-description sentence 25, H.5 108); generated: E −~2,350 (the two columns) | `paper/supporting_material.ipynb` (E and H cells); `paper/generate_gaps.py` (columns; the assumptions table from `derivation/axioms.py`); `work-packages/review/open-questions.md` (read; each row marked "in the appendix"); `claims_register.toml` (C585 to C588, C591 retired; new rows for the typed limitation lines); `tests/test_paper.py` (`test_appendix_e_job_block_types_no_gap_range`, `test_appendix_e_rows_agree_with_appendix_d`, `test_appendix_h_is_within_its_ledger_ceiling` (920 lowered by a cut row), `test_appendix_h_says_where_each_term_is_first_defined_and_points_at_d16`); `paper/length_ledger.toml` ("Appendix H" cut row); residuals baseline | 4 |
| WP57e | all | re-letters in the order of first mention (section 4), once; every reference, anchor, cell id, proof-map part, register anchor, test, ledger key, baseline key and docs link follows; `python -m derivation.proofmap` unchanged | none | the inventory of section 4 | 5, last before WP58 |

Definitions of good enough, one sentence each:

- **WP57a:** A's table lists only terms the paper uses, F is its four subsections with no preamble, G is the register
  in the three layers with one line citing the reading pass, and every cut Job block is gone from the rendered page.
- **WP57b:** every "Proof: Appendix B, Ln" in Section 6 still lands on its step table, B.2 says only what Sections 5
  and 6 point at, and `how_to_read` states no sentence Section 9 states.
- **WP57c:** every C and D subsection kept is cited by a sentence of Sections 2 to 9 as WP56 leaves them, the moved
  tables are in `paper/supplement/` and the case page with one citing line each, and no D subsection repeats another's
  columns.
- **WP57d:** every item of the inventory appears once in the new section with its record, the gaps table is four
  columns, H reads as the step deeper for Section 2's one sentence, and the driver holds a list of any caveat the main
  text repeats.
- **WP57e:** the appendices are lettered in the order of first mention, `uv run pytest`, the residual and vocabulary
  checks, `uv lock --check` and the proof map pass, and no reference to an old letter remains outside dated records.

## 4. Re-lettering

First mention in the paper (wp55), by paper cell and offset (`map_counts.py`, "first mention"):

| Order | Current | First mention | Proposed |
|---|---|---|---|
| 1 | D | Section 2, cell 13, "use PCA as a downstream step (Appendix D.16)" | A |
| 2 | H | Section 2, cell 13, "(Appendix H)" | B |
| 3 | A | Section 3, cell 14, "Appendix A is the full register" | C |
| 4 | B | Section 3, cell 16, "convex in w (Appendix B, L4)" | D |
| 5 | C | Section 5, cell 20, "Appendix C.4's" | E |
| 6 | E | Section 6, cell 54, "Appendix E records what the results leave open" | F |
| 7 | F | Section 11, cell 111 | G |
| 8 | G | Works cited, cell 112 | H |

All eight letters change under this rule. Counted at the appendix level instead (the first `appendix-x` reference,
subsection pointers not counted), the order is H (S2), A (S3), B (S3), E (S6), C (S7), D (S8), F (S11), G (S12),
and all eight letters change again. Section 2's pointer to D.16 is what places the case tables first; WP56 may change
the pointers of Sections 7 to 9, so the order is fixed at WP57e from the paper as it then stands.

Inventory of what follows a change of letter (counts from `grep -E 'appendix-[a-h]|sub-[a-h]-[0-9]+|Appendix [A-H]\b'`
over the tree, `site/`, `.venv` and the dated records excluded, plus the notebook's metadata):

| Surface | Count | What changes |
|---|---|---|
| `paper/paper.ipynb` (wp55) | 84 references (`{ref}` roles and "Appendix X" text) in 48 markdown cells | the role text and target of each |
| `paper/supporting_material.ipynb` | 8 appendix headings, 41 subsection headings, 49 `(anchor)=` lines, 101 letter references in text and captions; 119 of 121 cell ids carry a letter (`app-X`, `app-X-n`, `tab-X-*`, `sent-X-*`), 44 `tab-X-*` labels read by F.4 and `regenerate_row.py` | headings, anchors, cross-references, cell ids and labels |
| `paper/generate_findings.py` | 11 `appendix_link` constants (`_D3`, `_D5`, `_D8`, `_D11`, `_D14`, `_C5`, `_E`, `_D15`, `_D17`, `_C8`, `_D19`) and 17 docstring mentions | the anchor and the link text |
| other generators (`generate_proofs`, `generate_model`, `generate_results`, `generate_prior_art`, `generate_reading_pass`, `generate_register`, `generate_gaps`, `generate_repro`) | 20 docstring and comment lines; `generate_results` prints "the generator of Appendix C" in two table captions | text |
| `derivation/` | `python -m derivation.proofmap` carries no letter; `generate_proofs.PARTS` names B.1 and B.2 without the letter; the headings "B.1", "B.2", "B.3" are the notebook's | the three headings only |
| `claims_register.toml` | 82 rows filed under the supporting material, 49 with an anchor that is a subsection heading ("D.8 The solver's termination records"); 34 lines name a letter | the `anchor` fields; ids stay (append-only) |
| `tests/test_paper.py` | 64 lines with a cell id or label, 49 with an anchor or "Appendix X"; 68 test functions touch a letter | literals in the tests |
| `tests/test_site.py`, `tests/test_vocabulary.py` | 3 and 1 lines (`appendix-b`; "## Appendix A." in a fixture) | literals |
| `paper/length_ledger.toml` | 5 ceiling keys ("Appendix B", "C", "D", "G", "H"; the H ceiling is asserted at 920) and 75 dated rows | the keys; the dated rows stay as written |
| `scripts/residuals_baseline.json`, `scripts/vocabulary_baseline.toml` | 48 and 2 surface keys (`appendix/appendix-a`, ...) | regenerated with `--write-baseline` |
| `scripts/check_vocabulary.py`, `scripts/prose_surfaces.py` | 2 and 3 lines (the "Appendix A" special case for the register table) | the pattern |
| docs | `docs/bridge.md` 1 (`paper:sub-d-10`), `docs/user-guide/limitations.md` 1, `docs/user-guide/temperature.md` 2 (`paper:appendix-b`) | link targets and text |
| `examples/adcs/` | `case-model.md` 3 ("Appendix D.17", "C.8", "Appendix D"), `case.py` 1, `experiments/sensitivity.py` 3, `noise_injection.py` 1, `experiments/reports/change-register.md` 1 | text |
| `glossary.yaml` | 2 `defined_in` fields ("Appendix D.17", "Appendix D.10") | the fields |
| `paper/prior_art.yaml`, `paper/reading_pass.yaml` | 18 (16 comments, 2 text fields naming Appendix H and A) and 2 | text |
| `paper/myst.yml`, `paper/paper_common.py`, `paper/regenerate_row.py`, `paper/container/build-paper.sh` | 1, 1, 3, 1 | comments and the F.4 docstring |
| dated records left as written | `paper/container/RECORD.md` 7, `derivation/PROOF_MAP_FINDINGS.md` 2, `work-packages/*` (the decisions, reviews and rounds) | none |

## 5. Totals

Before (dev `c89843a`) and after the dispositions of section 1 (estimates for the shortened rows; the moved and cut rows
exact):

| Appendix | Cells before → after | Prose words before → after | Generated words before → after | Table rows before → after |
|---|---|---|---|---|
| front matter | 2 → 2 | 44 → 0 | 0 → 0 | 0 → 0 |
| A | 3 → 2 | 83 → 0 | 2,946 → ~2,500 | 72 → ~62 |
| B | 10 → 10 | 635 → ~245 | 33,606 → ~33,540 | 603 → 603 |
| C | 20 → 19 | 789 → ~270 | 3,322 → ~1,920 | 175 → ~100 |
| D | 50 → 40 | 1,624 → ~1,005 | 7,870 → ~6,930 | 293 → ~252 |
| E | 3 → ~5 | 92 → ~450 (the new lists) | 3,951 → ~1,600 | 18 → 18 (plus the assumptions table, 15 rows) |
| F | 10 → 9 | 257 → 141 | 1,340 → 1,340 | 72 → 72 |
| G | 8 → 4 | 252 → ~15 | 4,523 → 2,791 | 53 → 0 |
| H | 15 → 13 | 664 → ~485 | 417 → 417 | 12 → 12 |
| **all** | **121 → ~104** | **4,440 → ~2,610** | **57,975 → ~51,040** | **1,298 → ~1,120** |

The typed prose loses about 2,280 words and the new section adds about 450. Of the 2,280, about 1,280 are cut (the
eight Job blocks, 1,027 words together; the companion paragraph; the two Section 7 sentences repeated in C; H.5 and
H.1's self-description; G's pointer cell; the narrating openers of D.13, D.15, D.18 and D.19; D.7's sentence, merged),
about 580 move (C.8's omission paragraph and list to the case page; D.12's three paragraphs to the termination page;
G.2's introduction with its table; G's scope sentence and B.2's L16 clause to the assumptions section), and about 420
are shortening (B.2, D.17). Of the 6,900 generated words removed, about 3,860 move to `paper/supplement/` (G.2 1,732;
C.5 ~1,400; D.1 466; D.6 260) and about 3,000 go by compression or merge (E's two columns ~2,350; A's filter ~450; D.2
and D.7's merges ~215; `how_to_read` ~60).

The three largest removals: E's gaps table from six columns to four (~2,350 generated words); G.2's reading-pass
table to the repository (1,732 generated words, 53 rows); C.5's association table and second preview to the repository
(~1,400 generated words, 74 rows). The largest typed-prose removals: C.8 (−346), B.2 (−278), D's Job block (−220).

## 6. For the driver

Calls the map does not make:

1. D.18 has no citing sentence. Corollary 1's commentary is where a pointer belongs; adding one is a main-text edit
   outside WP57's non-goals.
2. G.2: move to the repository (the map's call) or keep as the step deeper for Section 11's "verified source".
3. H: keep shortened (the map's call) or move whole to the repository with one line in G, re-filing 22 register rows.
4. The re-lettering rule: first mention of any subsection (D, H, A, B, C, E, F, G) or of the appendix as a whole
   (H, A, B, E, C, D, F, G); each changes all eight letters.
5. Section 2 does not name Appendix G, though `paper-requirements.md` says it holds "Table 1 and Appendix G's
   register"; a main-text pointer or a change to the requirements.
6. The four glossary `defined_in` fields that name decision files render in the paper's table; a glossary edit in
   WP57a, or left.

# WP57c review: Appendices C and D

Branch `wp57c` (worktree off `dev` at d84cc74), two commits: the first unit (G2, D.19 and the moved material) and the
second (G1, G3, G4, G5). Counts by `work-packages/WP57-rounds/map_counts.py --paper paper/paper.ipynb --supp
paper/supporting_material.ipynb`: `WP57-rounds/c/counts-before.txt` (d84cc74) and `counts-after.txt`. Captures and the
unit's cold read: `WP57-rounds/c/*.png`, `WP57-rounds/c/cold-read.md`.

## G1: the citation table, refreshed at WP56's landing (before any edit)

Read from `paper/paper.ipynb` at d84cc74: typed pointers by `map_counts.py` (`WP57-rounds/c/counts-before.txt`, the
citing-sentence list), generated pointers from the committed outputs of the paper's code cells (links built by
`appendix_link`). "S7" is Section 7, "(gen)" a generated sentence.

| Subsection | Cited by (WP56's landing) | Map's disposition | Now | Why |
|---|---|---|---|---|
| C (opening, Job block) | S7 "described by a SysML v2 system model in the repository (Appendix C)" | cut the opening; C032 to S7; C147 retires | confirmed: cut; C032 retired (not re-anchored), C147 retired | C032's sentence ("this design loop the simulation is how the attributes are measured ...") left Section 7 with WP56; Section 9's "because the evaluation is a black box to the method" says its end and has its own row (C031); no Section 1 sentence holds it |
| C.1 configuration space | S7 Figure 4 caption "so are the ranges ... (Appendix C.1)" | keep | confirmed | typed pointer |
| C.2 evaluation | no pointer; step deeper for S7 "the slew is integrated in Python, and every other attribute and the four feasibility verdicts are computed by the SysML v2 model's calcs and requirements" | keep | confirmed | the attribute-to-file-and-function table is the one step under that sentence |
| C.3 feasibility | no pointer; step deeper for S7 "Four feasibility conditions remove the designs that do not settle, saturate the momentum budget, run short of power or discharge the battery too deeply" | keep | confirmed | the counts each condition removes |
| C.4 conditioning | S5 "The case's conditioning rule is Appendix C.4's" | keep | confirmed | typed pointer |
| C.5 table of metrics | no typed pointer; the generated participation sentence that linked it left the paper with WP56 and now prints in D.3, which links C.5 | shorten, move the rest | confirmed | step deeper for D.3's one-axis reading and S7's "thirteen attributes make thirteen metrics"; one primary preview, the 11 pairs at 0.5 or above, the one-axis sentence |
| C.6 datasets | S7 "Appendix C.6 names each table with the command that wrote it" | keep | confirmed | typed pointer |
| C.7 planted example | S8 "planted, with the generator of Appendix C.7" | keep | confirmed | typed pointer |
| C.8 cost model and what is left out | no pointer (S7's slot sentence and S8's "nominal (Appendix C.8)" left with WP56); step deeper for Table 2's cost limits (350,000 USD, 6,000,000 USD) and S9 "its costs a lower bound on a full costing" | shorten to the cost paragraph plus the slot item | changed: the cost paragraph plus its lower-bound sentence; the slot item moves too | no paper sentence names the launch slot after WP56; the lower-bound sentence is what S9's clause needs |
| D (Job block) | S8 "Appendix D holds the tables" | cut | confirmed | |
| D.1 temperature selection | none (S7's `temperature_sentence` and Figure 6 draw the primary sweep) | move to `paper/supplement/temperature-sweep.md` | confirmed | |
| D.2 diagnostics at K = 1, 2, 3 | none | merge into D.8 | confirmed; the term rows and shares left out (D.3's term tables carry them) | no D subsection repeats another's columns |
| D.3 exponents and terms | S8 (gen) `terms_sentence` "(Appendix D.3)" | keep | confirmed; receives the participation sentence | |
| D.4 regimes side by side | S8 "separates the problem's contribution from the gains' (Appendix D.4)" | keep | confirmed; receives the pair-counted-as-one rule | |
| D.5 sensitivity variants | S5 "a different scaler does not (Appendix D.5)"; S7 (gen) `temperature_sentence` "(Appendix D.5)" | keep | confirmed; receives the scaler sentence | |
| D.6 refits by category | none | move to `paper/supplement/refits-by-category.md` | confirmed | |
| D.7 candidate designs | none | merge into D.17 | confirmed: the sentence is generated under D.17's second table, which lists the candidates | |
| D.8 termination records | S6 "never certified (Appendix D.8)", "the levels it meets (Appendix D.8)"; S8 "margin, gap and status ... Appendix D.8" | keep, receive D.2 and D.12's tables | confirmed; the margin reading's table keeps only the median (its other columns are D.8's first table's) | |
| D.9 nondominated sorting | no pointer; S8 (gen) `nondominated_sentence` states its counts | keep (pending) | confirmed with the Agent's second default: the sentence names D.9 for the counts | the parenthetical is one link; merging the four-row table into D.11 would mix a result with the stability record |
| D.10 propose, predict, check | S8 "then measured (Appendix D.10)" | keep | confirmed; receives the proposer's rule, the never-clipped rule and the reading of the proposals | |
| D.11 stability | S5 and S6 (gen) `margin_sentence`, S8 (gen) `nondominated_sentence`, S8 "D.11 the digits that hold" | keep | confirmed | |
| D.12 conditioning of the exponents | none | table to D.8, paragraphs to `docs/user-guide/termination.md` | confirmed | the page already held "why" and "how"; it gains the convex-loss sentence and the one-line call |
| D.13 refit on own rows | S5 "(at tau = infinity, Appendix D.13)" | shorten the opener | confirmed | |
| D.14 recovery of a planted answer | S6 "Appendix D.14 records fits that reach the iteration cap first"; S8 (gen) `planted_sentence` "(Appendix D.14)" | keep | confirmed | |
| D.15 choosing K | S8 Figure 8 caption "(Appendix D.15)"; S8 (gen) `choosing_k_sentence` | keep, opener stated directly | confirmed; receives the K temperatures | |
| D.16 chaining with PCA | S2 "(Appendix D.16)"; S8 Figure 8 caption | keep | confirmed | |
| D.17 requirements read after the fit | S8 (gen) `requirements_sentence` and `design_sets_sentence` "(Appendix D.17)" | keep both tables; shorten prose; receive D.7 | confirmed; receives the ladder sentence | |
| D.18 noise-ridge against injected noise | none until now; Corollary 1's commentary gains its pointer (driver's call 1) | keep, cut the opener | confirmed | |
| D.19 the decision | S8 (gen) `decision_sentence` "(Appendix D.19)"; S8 Table 3 caption | keep, rules stated directly | changed: rules rewritten to Section 8's four (first commit); `decision_detail` retired (it read nondominance on pointing error and fleet cost, a pair no rule now uses) | |

The Agent's default for D.9 taken: `nondominated_sentence` names Appendix D.9 in its parenthetical (two words in Section
8, a `[[raise]]` row), and D.9 keeps its four-row table. C.5's "pairs at |Spearman| at least 0.5" are 17 of 78 when a
pair counts if it reaches 0.5 in either regime (the map's 11 counted one regime); the generator prints the count.

## Words per subsection (typed prose / generated words), before and after

| Subsection | before | after | | Subsection | before | after |
|---|---|---|---|---|---|---|
| C (opening) | 172 / 0 | 0 / 0 | | D (Job block; now the supplement line) | 220 / 0 | 27 / 0 |
| C.1 | 0 / 157 | 0 / 157 | | D.1 | 0 / 466 | moved |
| C.2 | 0 / 342 | 0 / 342 | | D.2 | 0 / 234 | merged into D.8 |
| C.3 | 0 / 189 | 0 / 189 | | D.3 | 0 / 1,752 | 0 / 1,875 |
| C.4 | 0 / 532 | 0 / 532 | | D.4 | 0 / 148 | 50 / 148 |
| C.5 | 51 / 1,901 | 62 / 633 | | D.5 | 0 / 418 | 0 / 475 |
| C.6 | 0 / 113 | 0 / 113 | | D.6 | 0 / 260 | moved |
| C.7 | 0 / 88 | 0 / 88 | | D.7 | 54 / 85 | merged into D.17 |
| C.8 | 566 / 0 | 267 / 0 | | D.8 | 192 / 286 | 255 / 332 |
| **C** | **789 / 3,322** | **329 / 2,054** | | D.9 | 0 / 76 | 0 / 76 |
| | | | | D.10 | 0 / 94 | 81 / 265 |
| | | | | D.11 | 0 / 445 | 0 / 445 |
| | | | | D.12 | 162 / 108 | to D.8 and the termination page |
| | | | | D.13 | 40 / 78 | 16 / 78 |
| | | | | D.14 | 47 / 449 | 47 / 449 |
| | | | | D.15 | 146 / 194 | 144 / 245 |
| | | | | D.16 | 90 / 84 | 90 / 84 |
| | | | | D.17 | 400 / 1,286 | 344 / 1,337 |
| | | | | D.18 | 86 / 299 | 82 / 299 |
| | | | | D.19 | 187 / 1,108 | 178 / 965 |
| | | | | **D** | **1,624 / 7,870** | **1,314 / 7,073** |

Rows 175 to 107 (C) and 293 to 240 (D); cells 20 to 19 and 50 to 43. D grew where WP56's material landed (D.3, D.4, D.5,
D.10, D.15, D.17: about 170 typed and 400 generated words); the map's estimate for D (about 1,005 typed) is not met
by about 300 words, most of it that landing and D.8's merged sentence. The supporting material in all: typed 3,589 to
2,819, generated 55,587 to 53,394 (A and F's generated tables move with the cells they list).

## What moved, with paths (R-3)

| From | To | Cited from |
|---|---|---|
| C.5's stock preview and all 78 pairs | `paper/supplement/metric-associations.md` (`generate_supplement.py`, staleness test) | C.5, one line |
| C.8's "What the case leaves out" paragraph and five items | `examples/adcs/case-model.md`, "What the case leaves out" (the page's own list, gaining the paragraph's sentences, the launch slot's figures at two and three satellites and the structure item; its line "The full list is Appendix C.8" gone) | C.8, one line |
| `work-packages/WP30-rounds/appendix-c-leaves-out.md` (the mirror) | deleted with its test clause; `git show d84cc74:work-packages/WP30-rounds/appendix-c-leaves-out.md` | |
| D.1's sweep | `paper/supplement/temperature-sweep.md` | D's opening line |
| D.6's refits | `paper/supplement/refits-by-category.md` | D's opening line |
| D.2's table, D.12's table | D.8's table, one per regime (`termination_records`; `k_diagnostics` and `conditioning_diagnostic` retired); D.2's term rows and shares left to D.3 | |
| D.12's paragraphs | `docs/user-guide/termination.md`, `conditioning_` (the convex-loss sentence and the one-line call; the page already said why and how) | D.8, one link |
| D.7's sentence and table | generated under D.17's second table (`_candidates_sentence`, from the placement table); `candidate_designs` retired | |
| `margin_reading` | keeps the median column only (the margin, radius and band are D.8's first table) | |

Every cut typed text is at `git show d84cc74:paper/supporting_material.ipynb` (cells `app-C-job`, `app-C-8`, `app-D-job`,
`app-D-cand`, `app-D-cond`, `app-D-own`, `app-D-fixed-text`, `app-D-req`, `app-D-req-sets`, `app-D-noise`,
`app-D-decision`, `app-D-decision-table`).

## moved-to-appendix.md

Every line of `WP56-rounds/moved-to-appendix.md` carries a "WP57c" column: eleven typed lines (five landed: C.8's
lower-bound sentence, D.17's ladder, D.4's pair rule, D.10's proposer rule and never-clipped rule; six not landed with
the reason) and six generated lines (four landed by one call each: D.3 `participation_sentence`, D.5
`temperature_variants`, D.10 `proposals_reading`, D.15 `k_temperatures`; `recovery_sentence` not landed, D.14's tables
state every failure; `tension_sentence` retired), and the D.19 note marked landed.

## Register

| | Ids |
|---|---|
| Retired, first unit | C609, C610, C611, C661 (`decision_detail`, nondominance on pointing error and fleet cost, which no rule reads now); C620, C621 (the two-stakeholder rules, replaced by C992); C797, C798 (`tension_sentence`) |
| Retired, second unit | C032 (the Job block's duplicate of a Section 7 sentence that WP56 cut; Section 9's C031 holds the black-box clause); C147 (the Job block); C153 (D.13's narrating opener); C424 (D.12's typed case values, now printed in D.8's table) |
| Re-anchored or re-worded | C616 (the shortlist table's row), C628 (the scaler sentence, now "The `RobustScaler` variant changes the K = 1 contending set"), C423 and C425 (to `docs/user-guide/termination.md`), C441 (to D.8), C497, C502, C503, C504 (to the case page), C506 (to `_candidates_sentence`), C670 (backing `termination_records`) |
| Added | C988 (D.4, the pair counted as one), C989 (D.10, the proposer's radius), C990 (D.10, never clipped), C991 (D.17, the ladder), C992 (D.19, the four rules), C993 (D.19, the coverage probability's source), C994 (C.8, the lower bound), C995 (Corollary 1's pointer to D.18), C996 (D.8, the merged table with `conditioning_`) |

Ids used: C988 to C996. `review/open-questions.md` gains OQ-14 (the decision's unused picks).

## Tests

Changed: `_moved` reads the D cells (`MOVED_TO_D`); `JOB_BLOCKS` = E, H; `_TERM_NUMBERED` loses D.2 and D.12; the C and
D table-set test (D numbered in order, gaps allowed until WP57e); the stability-heading test; the dataset-label test
skips the moved sentences (the table above each cites it); the proposer's-radius test reads D.10; the scaler regex; the
participation phrase; the decision format and notebook tests (coverage column, 17 marks, no `sent-D-decision`); the
C.8 tests (cost items and order in C.8, the load and limits' kinds and the list's numbers on the case page, the mirror
gone); the D.7 test reads D.17's output; the conditioning tests read D.8's column and the termination page; the
K = 2 fraction test reads D.8; the supplement writer's file list; `tests/test_site.py`, the termination page's budget
743 to 767 (D.12's 24 words). Added: `test_the_moved_sentences_in_appendix_d_are_their_generators_output`,
`test_d19_states_section_8s_four_rules_and_no_other` (R-4), `test_appendix_d8_prints_the_conditioning_of_the_exponents`,
`test_the_c_and_d_supplement_files_equal_their_generators_and_are_cited`. Retired: the tension finite-difference test,
`test_c_and_d_each_point_to_the_other_in_their_opening`, `test_d19_says_the_nondominated_sets_of_the_548_and_the_shortlist_differ`.

## Checks

| Check | Command | Output | Exit |
|---|---|---|---|
| Notebooks | `cd paper && MPLCONFIGDIR=<warm cache> uv run python execute_notebooks.py` (both after the generators changed; the supporting notebook again after each output change) | executed paper.ipynb, executed supporting_material.ipynb | 0 |
| Supplement | `uv run python paper/generate_supplement.py --check` | (no stale file) | 0 |
| Fast suite | `uv run pytest -q -m "not slow" -n auto` | 2,091 passed, 17 skipped, 2 xfailed (on the final tree) | 0 |
| Slow paper tests | `uv run pytest -q -m slow -n auto tests/test_paper.py tests/test_case.py::test_docstrings_run_and_are_numpydoc` | 31 passed in 14 min 21 s (before the last markdown-only edits: C.8's "covered cost", the funnel cell moved, a generator line re-wrapped) | 0 |
| Register | `uv run pytest -q tests/test_claims_register.py` | 21 passed | 0 |
| Lint, format, lock | `uv run ruff check .`; `uv run ruff format --check .`; `uv lock --check` | All checks passed; 624 files already formatted; resolved | 0, 0, 0 |
| Proof map | `uv run python -m derivation.proofmap` | PROOF MAP OK: 22 lemma files, 549 tagged steps (as dev) | 0 |
| Vocabulary | `uv run python scripts/check_vocabulary.py` | 0 new violation(s), 67 known | 0 |
| Residuals | `uv run python scripts/check_residuals.py --compare scripts/residuals_baseline.json --strict` | exits 1 as on dev; the supporting notebook at or below dev on every count (metanarration 5 to 3, parens 283 to 279, long sentences 93 to 89, compound 59 to 56, dense paragraphs 34 to 33, terms undefined at first use 17 to 16, the rest equal); the baseline lowered where C and D's counts fell (C and D metanarration 1 to 0, D compound 1 to 0, D.19 long sentences 3 to 2) | 1 |
| Data and derivations | `git diff --stat dev -- derivation examples/adcs/data` | empty | 0 |
| Docs | `uv run mkdocs build -q` | built (the MkDocs 2 notice only) | 0 |
| Paper build | `cd paper && BASE_URL=/paper uv run --frozen myst build --html` | no warning or error in the log | 0 |

The site is served on port 8871 (`scratchpad/serve-wp57c`, a link to `paper/_build/html`).

## Amendments proposed (the problem, not the scope)

- `test_c_has_the_metric_table_and_the_sources_and_d_has_the_extended_tables` pinned D's subsections as 1 to n; moving
  D.1, D.2, D.6, D.7 and D.12 leaves gaps that WP57e's re-lettering closes. The test now asserts order only; WP57e
  restores the consecutive check.
- The termination page's word budget rises by the 24 words D.12 moved into it.

## Left for the driver

- `generate_findings.recovery_sentence` prints in no cell (D.14's tables say it all); its tests read the generator. Retire
  it with its rows, or keep.
- `generate_findings.decision` still computes the retired rules' picks and marks (OQ-14).
- WP57e: re-letter (D now runs D.3 to D.19 with gaps; C.1's heading is "Configurations (the design variables and their ranges)").
- Soft-confirm C and D on the captures; the landing (both commits) and CI on both platforms.

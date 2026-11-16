# WP57 D-3: the supporting material read at five depths

The parent's D-3 (`WP57-scope-of-work.md`): the whole supporting material, Appendices A to H as WP57e re-lettered them,
read with the paper once the children landed. Read on dev at c2b80421, branch `wp57-review`; nothing outside this file
and `work-packages/WP57-rounds/review/` changes.

## Method

The site at dev's head, served read-only at `http://localhost:8797/paper/` (paper) and `/paper/supporting-material/`,
captured by headless Chrome at 1,280 by 900 with `WP57-rounds/review/capture.py` (`text` writes both pages' inner text
and every paper link to the supporting material with its paragraph, `pointers.json`; `shots` writes the 70 PNGs).
Pass 1 was done before any child record was opened: the paper end to end, the supporting material end to end, each of
the paper's 85 links followed and its landing captured (`landing-<anchor>.png`), each appendix at depth 4 and each
boundary between appendices at depth 5 (`boundary-ab.png` to `boundary-gh.png`: the end of one appendix above the
start of the next), and a probe of the page's own links (relative links resolved and clicked). Pass 2 then read
`WP57-rounds/map.md`, `WP57a-review.md` to `WP57e-review.md`, the cold reads and `WP57-decisions.md`, ran the checks of
R-1 to R-5 and filled the "already recorded in" column without changing a pass-1 row.

Reading details decided here: a pointer "finds the step in the first screen" when the 900 px viewport the link opens
shows the value, row or sentence the citing sentence relies on; a caveat is a sentence that says what a result does
not establish; a forward reference is a reference from an appendix to a later appendix of the same page.

## The pointers

85 links from the paper to the supporting material: 84 in the text and the sidebar's "Supporting material" entry, to
29 distinct targets. Every anchor resolves. The paper-side generated links (`supporting-material/#sub-b-7` and the like)
resolve correctly from `/paper/`, including after "Back to Article".

| Target | Paper sentences (count) | What the sentence promises | First screen | More than the step |
|---|---|---|---|---|
| `#appendix-a` | S2 Table 1's register; S12 Works cited (2) | the full register behind Table 1 | yes: A.1, the first family | the "Why this is not just the neighbour" bullets repeat "differs" (F-29) |
| `#sub-b-11` | S2 "PCA as a downstream step"; Fig. 8 caption (2) | the share of spread and the loadings | yes: 0.361 and the loadings | no |
| `#appendix-c` | S2 HoroPCA sentence (1) | the test and its three boundaries | the hypothesis (C.1); the boundaries are C.4, three screens down | the least-variance component paragraph |
| `#appendix-d` | S3 "the full register of symbols and terms" (1) | the register | yes | rows for words the paper never uses (novelty, design tensions); "Defined in" names unreachable places (F-11) |
| `#appendix-e` | "Appendix E, Ln" and "Proof: Appendix E, Ln" in S3 to S6, four step pointers (L3.9, L5.25, L17.13, L17.19), and two bare "Appendix E" (49) | the proof of Ln, or its step | no: E's preamble and proof map; Ln is 2 to 51 screens down (F-1) | not applicable |
| `#sub-b-3` | S5 target fraction halved or doubled, the scaler; S7 (2) | the variants' contending sets | yes | the four-metric view row; "baseline" names two things (F-9) |
| `#sub-f-4` | S5 "The case's conditioning rule is Appendix F.4's" (1) | the rule | no: two tables of numbers; the rule opens F.5 (F-6) | a constant column |
| `#sub-b-7` | S5, S6, S8 (4) | the digits that hold under jitter | yes | four rows that show no movement (F-18) |
| `#sub-e-2` | S5 "steps: Appendix E.2"; S6 Newton steps (2) | restarts, stopping, the polish | yes, the first paragraph | no |
| `#sub-b-8` | S5 own-rows refit (1) | the 0 of 60 against 60 of 60 | yes | no |
| `#sub-b-13` | S6 Corollary 1 (1) | the ridge against injected noise | yes | it holds a result the paper does not state (F-15) |
| `#sub-b-9` | S6 iteration cap; S8 16 of 20 (2) | the record of the cap; the recovery count | the count, yes; the cap record is the paragraph after the second table | no |
| `#sub-b-4` | S6 twice; S8 (3) | statuses, margin, gap | yes | no |
| `#appendix-g` | S6 last line; S9 Limits (2) | what the results leave open; the case's limits | G.1's table; the case's limits are a G.2 row about six screens down | G.2 restates main-text caveats (F-7) |
| `#appendix-f` | S7 the system model (1) | the model behind the table | F.1's table; no sentence | no |
| `#sub-f-1` | Fig. 4 caption, the ranges (1) | declared ranges | yes | no |
| `#sub-f-6` | S7 "names each table with the command" (1) | label, file, command | yes | a hash column printed twice (F-32) |
| `#sub-b-5` | S8 nondominated counts (1) | 236 and 2,134 | yes | no |
| `#appendix-b` | S8 "Appendix B holds the tables" (1) | the tables | a sentence about two moved files, then B.1 (F-17) | no |
| `#sub-b-10` | S8 twice; Fig. 8 caption (3) | the three checks for K | yes | no |
| `#sub-f-7` | S8 "the generator of Appendix F.7" (1) | the generator | yes | no |
| `#sub-b-1` | S8 term shares (1) | 0.74 and 0.26 | the per-term table is the second screen | K = 3 and the baseline regime's tables (F-20, leave) |
| `#sub-b-2` | S8 regimes (1) | the two contending sets | yes | three unlabelled association rows (F-10) |
| `#sub-b-6` | S8 propose, predict, check (1) | the three proposals | yes | it shows two proposals are one configuration (F-14) |
| `#sub-b-12` | S8 twice (2) | exclusions; the design sets | the first, yes; the second two screens down | the check-design table (F-19) |
| `#sub-b-14` | S8 twice (2) | shortlist, rules, picks' variables | yes | no |
| `#sub-h-3` | S8 commands (1) | the commands | yes | no |
| `#sub-h-2` | S8 "last digits" (1) | the environment of record | yes | no |
| `#appendix-h` | S11 (1) | toolchain, environment, commands | yes | H.4 lists 3 of 10 figures (F-16) |

## Findings

Severity: B blocks the read; C costs the reader; K cosmetic. Depth 1 to 5 as in `paper-requirements.md`.

| # | Location | D | What the reader meets | Finding | Sev | Disposition | Already recorded in |
|---|---|---|---|---|---|---|---|
| F-1 | Paper S3 to S6 → `#appendix-e` | 3, 5 | "Proof: Appendix E, L17" | All 49 links to E land on E's top; the result is 2 (L1) to 51 (L17) screens below, though `proof-l1` to `proof-l22` exist on the page. Step pointers (L17.19) land 50 screens from their row | B | main-text wording: each role targets `proof-ln` | new; `WP57b-review.md` R-1 "25 of 25 land" checked that each anchor exists, not where the link goes |
| F-2 | B.1, B.3, B.10 | 2 | "named a pair one axis (Appendix F.5)" | The supporting page's three generated links (`supporting-material/#sub-f-5`, `#sub-b-10`, `#appendix-g`) resolve to `/paper/supporting-material/supporting-material/...`: a 404 | B | appendix wording: `appendix_link` writes a page-relative path only the paper page resolves | new; the cold reads checked `#` links only |
| F-3 | every repository link on the page | 3 | `paper/supplement/temperature-sweep.md` | The links to moved material, the scripts' lines, the gaps ledger and the guides point at `blob/main`; `main` is e7fd1165 (WP13), 2,010 commits behind dev, and holds none of them | B | the supervisor's call: merge to main, or pin the links to a commit; WP58 | new |
| F-4 | C.3, G.1, G.2 | 5 | "Table 1: Appendix C's hypothesis table" | The supporting page numbers its tables 1 to 4, so "Table 1" to "Table 3" each name two objects across the paper and its supporting material | C | appendix wording (prefix the page's numbering, or no numbers); WP58 | `WP57-decisions.md` (WP57e landing) records page-order numbering for his read; the collision is not named |
| F-5 | F.3 against S7 Table 2 | 5 | "removed in this order" | F.3 removes settled, power, momentum, depth of discharge; S7 says the case applies them in the order of Table 2 (settling, depth of discharge, momentum, power). The counts depend on the order | C | main-text or appendix wording, one order; WP58 | new |
| F-6 | F.4, S5 | 3 | "The case's conditioning rule is Appendix F.4's" | F.4 is two tables; the rule is F.5's first sentence | C | appendix wording: F.5's formula moves to F.4's head | new |
| F-7 | G.2 against S6 and S9 | 5 | "One term is tangent at one place and conservative off it" | G.2's rows restate main-text caveats nearly word for word, so each is said twice in the one document | C | the supervisor's call: G.2 points (section, record) or the main text points; WP58 | the map's 2.2 shape ("listed with a pointer, not restated"); the repeat not flagged in `WP57d-review.md` |
| F-8 | B.2, B.3, B.6, B.12, B.13, C.4, E preamble, F.8, A | 4, 5 | "eight draws are few" | Caveats outside G; those of B.12 and B.13 are also G.2 rows, so said twice | C | cut where G.2 holds the row; C.4's limits are the supervisor's call | C.4: map row `sub-h-4` (kept, listed in G by reference); the rest new |
| F-9 | B.3, B.12, B.14, F.6 | 4 | variant "baseline", column "shared with baseline" | "baseline" names the baseline regime, B.3's default variant and its column; the regime also appears as `cubesat-stock`, "stock" and `v2-baseline@12` | C | appendix wording: the variant "default"; one name for the regime in labels | the regime rename (OQ-11) and D's "baseline regime" row; the variant collision new |
| F-10 | B.2 | 1, 2 | "settling time, total mass -0.46 (-0.46)" | Three rows give no word for what the number or the bracket is | C | appendix wording (row label) | new |
| F-11 | D, column "Defined in" | 2 | "Prediction from configuration; WP41 note" | Plain text naming headings that no longer exist, work-package records and docstrings | C | appendix wording: paper anchors, or drop the column; WP58 | WP58 list in `WP57-decisions.md` (WP57a: five `defined_in` fields); the column as a whole new |
| F-12 | D, row conditioning | 1 | "the main text the attribute a_j and the shift s_j" | A sentence about the paper's text (R-2) carrying a notation clash: a_j is the shift in the scripts and the attribute in the main text | C | appendix wording; the clash is WP58's | the map's row for old A (the clash); R-2 reading new |
| F-13 | E preamble, B.7, A (entropic risk, closing line), C.3 caption, D (frontier), G.1 | 4 | "on the stack the paper already uses" | Sentences and headers about the paper's text that the residual checker does not flag | K | appendix wording | C.3's caption: WP57e for WP58; the rest new |
| F-14 | B.6 against S8 | 5 | "Two of the three proposals are one configuration." | S8 counts "3 of 3" | C | main-text wording; WP58 | new |
| F-15 | B.13 against S6 | 5 | "by a factor of 1.6 to 179" | The prediction exceeds the measured shift in 7 of 8 rows; S6 points to B.13 without saying what it shows | C | the supervisor's call (main-text wording) | map D.18 row and decision 1 (the pointer added); the content new |
| F-16 | H.4 against S11 | 4, 5 | "One row per figure and table" | 3 of the paper's 10 figures have a row (6, 9, 10); 1 to 5, 7 and 8 none; the "Writes" column is clipped at 1,280 px | C | appendix wording or the heading narrowed; WP58 | new |
| F-17 | B, opening | 4 | "The K = 1 fit at each temperature ... are paper/supplement/..." | B's first sentence names what is not in B | K | appendix wording: move it to B's end | the moves: WP57c; the placement new |
| F-18 | B.7, second table | 1 | "largest term gap ... below 1e-12" | 4 of the 8 "quantities that move" read "below 1e-12" in every column | K | cut those rows | new |
| F-19 | B.12, check-design table | 4 | "fast_effort_hungry ... +0.315" | No paper sentence reads the check designs; the proposals repeat B.6 | C | move to the repository (`paper/supplement/`) | map D.7 row (merged into D.17), accepted in WP57c |
| F-20 | B.1, K = 3 and the baseline regime's K = 2, 3 tables | 4 | six tables before B.2 | Bulk ahead of what S8 reads | K | leave: S6 reads K = 3's certificate, B.10 its share | map D.3 row (keep K = 3) |
| F-21 | B, F, G.2's gaps | 1 | "`objective_` is compared across K" | Code names in place of the paper's words (`frac_above_`, `n_eff_`, `n_lemma`, `panel_span_m`, `st_grade`); `objective_` is not an attribute of the package and "objective" is reserved for the decision-maker | C | appendix wording; the gaps ledger's `objective_` to `loss_` | new |
| F-22 | A → C, D; B.7 → G-17; B.8, B.9 → F; B.10 → G; E → F, G | 5 | "the six check designs" (B.7) | Forward references; B.7 uses "check designs" before B.12 introduces them | K | leave the letter references (a reference set read by lookup); B.7's word is appendix wording | new |
| F-23 | G.2, column "Section" | 2 | "Section 9 ... Novelty V − 1" | Rows assign to Section 9 sentences Section 9 does not carry (novelty; configuration management) | K | appendix wording | `WP57-decisions.md` (WP57d): "the paper governs"; these two rows new |
| F-24 | G.2 gaps table | 1 | "D: the near-frontier rows ... lie on one hyperplane" | "D" and "Step B" name hypotheses with appendix letters; gap ids G-1 to G-18 beside subsections G.1 to G.3 | K | appendix wording (gaps ledger) | new |
| F-25 | E, every step table | 1, 4 | the A1 wording three times in L2.2 | Each of 169 axiom steps repeats the axiom's full wording; the step's prose is the narrowest column | C | appendix wording: the id linked, the wording once in the Ledger line; WP58 | new |
| F-26 | E, proof map | 2 | "L1. Homogeneity and invariant form" | The map's rows do not link to their proofs | K | appendix wording | new |
| F-27 | page top | 5 | "Supporting material", then Appendix A | No front matter; the entry is the paper's sidebar and its pointers | K | leave: the companion paragraph was cut as narration and the headings say what each part holds | map, front matter row |
| F-28 | the outline | 5 | "In this article" | A fixed box showing A to C; below C the reader's place is not shown | K | WP58 (theme) | new |
| F-29 | A, nine families | 4, 5 | "Why this is not just the neighbour." | Repeats the "differs" bullet; "shares" and "differs" repeat Table 1 | K | cut the "Why" bullets | new |
| F-30 | F.2, D | 4 | `cubesat_tradespace.sysml`, `model_v2/cubesat.sysml`, `cubesat_r2.sysml` | Four files for what the paper calls one SysML v2 system model | C | appendix wording: name the model once; WP58 | new |
| F-31 | F.3 against S7 | 5 | "Each condition is a flag the simulation returns" | S7: the verdicts "are computed by the SysML v2 model's calcs and requirements" | C | one statement; WP58 | new |
| F-32 | F.4, F.6 | 1 | "std of log m: 1" | A constant column; F.6 prints the same hash twice | K | cut the columns | new |
| F-33 | B.2, F.5 | 5 | "Pairs at \|Spearman\| 0.99 or above ..." | The same sentence ends B.2 and F.5 | K | keep it in F.5 | new |
| F-34 | H.1 | 1 | "Commit 6d86038d" | The execution commit, not the page's head | K | leave: the row says "observed when the cell ran" | WP57e cold read |

Counts: 34 findings; 3 B, 17 C, 14 K; 20 new, 14 with an earlier record (4 fully, 10 partly).

## Depth 4, per appendix

**A.** Reads in order through its three layers. Each family carries four or five bullets, and in nine the fifth ("Why
this is not just the neighbour") says the fourth again; the shares and differs fields are Table 1's text. Two entries
carry reading notes ("read by title"), provenance the reading pass holds.

**B.** Fourteen subsections in the order of Section 8 with the solver records between. B opens on a sentence about two
moved files. B.1's six tables come before anything S8 reads beyond K = 1 and 2. B.2's association rows are unlabelled.
B.3 makes "baseline" a variant. B.6 is the one place a reader learns two proposals are one design. B.7's movement table
carries rows that do not move. B.12 runs four tables, the last on check designs no sentence uses. Three generated links
(B.1, B.3, B.10) 404. Caveats sit in B.2, B.3, B.6, B.12 and B.13.

**C.** Reads as a prospectively specified test: hypothesis, experiment, table, reading. The table is "Table 1" on a page
that follows a paper whose Table 1 is the families. C.4 ends in three reading limits and a paragraph outside the
hypothesis.

**D.** One table, no prose. The "Meaning" and "Not" columns are the step deeper Section 3 wants. "Defined in" sends a
reader to places outside the paper or no longer in it, and the conditioning row speaks about the main text.

**E.** The preamble, the counts and the proof map, then twenty-two proofs and the checker. Read in order it holds;
reached from a paper pointer it fails, since every pointer lands on the preamble (F-1). The step tables print each
axiom's wording at every use, which multiplies the page's height; the proof map does not link to the proofs.

**F.** Configurations, evaluation, feasibility, conditioning, the table of metrics, datasets, the planted example, the
cost model: the order of the pipeline. F.3's order and its "simulation returns" disagree with Section 7. F.4 carries no
rule. F.2 names four files as the model. F.8 ends in caveats and a pointer to what the case leaves out.

**G.** Assumptions (generated), limitations (typed rows, then the gaps table), open questions. G.2's typed rows restate
the main text; its gaps table uses appendix letters as hypothesis names and a stale attribute; G.3's records include
work-package files.

**H.** Toolchain, environment, commands, one row per figure and table. H.4 omits seven of the paper's figures and its
"Writes" column is clipped.

## Depth 5, the whole

The order A to H is the order of first mention in the paper, and the boundaries read clean
(`boundary-ab.png` to `boundary-gh.png`): no appendix opens by referring back to the previous one. Read front to back
the page is not one document with the paper in three ways. Its lookups break: 49 of 85 pointers land a long scroll from
their target, three in-page links 404, and every repository link 404s until main catches up. Its names fork: Tables 1
to 3, "baseline", the case's model files, code names in place of the paper's words. Its caveats double: G.2 restates
the main text, and B, C, E and F keep their own. The three lineages stay apart in placement (A is prior art, E the
proofs, B, C and F the case and its comparison), with one crossing: E's preamble names the case's SysML v2 model as the
place formal verification is said. The register of the main text holds in A, C and the prose of B; the generated
tables of B, D, E and G drift into the code's register (ASCII mathematics in E's statements, attribute names in B and
G).

## Acceptance against the parent scope

| Req | Evidence | Verdict |
|---|---|---|
| R-1 Every kept subsection cited or the step deeper | The map's citation column and the decisions: every kept subsection has a citing sentence except two the driver kept on record (L22, cited by no paper sentence, `grep -c L22` 0 on the paper's text, kept as the record whole; the check-design table merged into B.12, F-19). The landings are in the pointer table | met, with the two recorded exceptions; F-1 is a pointer defect, not a citation gap |
| R-2 No sentence in an appendix about the paper's text | `check_residuals.py --json`: metanarration 0 on every supporting-material surface. The read finds sentences about the paper's text the checker does not flag (F-12, F-13) | met by the checker; not met by the read (F-12, F-13; cosmetic to costs) |
| R-3 Nothing cut is lost | `git log` shows each moved file at its path: `paper/supplement/reading-pass.md` (d4f6fc58), `temperature-sweep.md` and `refits-by-category.md` (772e343a), `metric-associations.md` (772e343a, 64f01a1d), `examples/adcs/case-model.md`, `docs/user-guide/termination.md`, `notes/directions/wp35-horopca-formalism-and-solvers.md` (c8f8407b); each cited from its appendix in one line | met in the tree; on the rendered page every such link 404s (F-3) |
| R-4 Derivation and proof map unchanged by WP57a to d | `uv run python -m derivation.proofmap`: PROOF MAP OK, 22 files, 549 steps; `git log --oneline -1 -- derivation`: db5a6f4c (WP62, 2026-11-15 16:39), before the map's approval at 18:04; the record last changed at 415d8899 (WP46); no WP57 commit touches `derivation/` | met |
| R-5 Register follows; tests, lint, residuals | `uv run pytest -q tests/test_claims_register.py`: 21 passed; `check_residuals.py --compare scripts/residuals_baseline.json --strict`: exit 1 with 125 rises, dev's 126 less the one WP57e recorded; `uv run ruff check .` and `ruff format --check .` clean on this branch | met as on dev |

## For the supervisor's read

1. F-1: the 49 proof pointers to land on their proof (`proof-ln`), a main-text change of 49 role targets.
2. F-3: the repository links point at `main`, which is 2,010 commits behind dev; merge, or pin the links to a commit.
3. F-7 and F-8: one home for each caveat. G.2 as pointers to the main text's sentences, or the main text pointing to
   G.2; and whether C.4's reading limits stay in C.
4. F-15: whether Section 6 says what B.13 shows (the prediction overshoots in 7 of 8 rows).
5. F-5 and F-31: which order and which source of the feasibility verdicts is the case's, the paper's or F.3's.
6. F-4: the supporting page's table numbering against the paper's.
7. F-14: "3 of 3" proposals against two distinct configurations.

## Proposed WP58 items

- The 49 "Appendix E, Ln" roles retargeted to `proof-ln` (F-1).
- `appendix_link` writing links that resolve from both pages (F-2).
- Repository links that resolve on the published page (F-3).
- The supporting page's table numbers distinct from the paper's (F-4).
- One feasibility order and one source of the verdicts (F-5, F-31).
- F.5's rule at F.4's head (F-6).
- One home per caveat: G.2's restatements to pointers, B's, E's and F's caveats to G (F-7, F-8).
- "baseline" for the regime only, one label for it in tables (F-9).
- B.2's association rows labelled (F-10).
- D's "Defined in" to paper anchors or dropped; its conditioning row without "the main text" (F-11, F-12).
- The sentences of F-13 rewritten.
- Section 8's proposal count and Section 6's B.13 sentence (F-14, F-15).
- H.4 complete or its heading narrowed, its last column unclipped (F-16).
- Step tables citing axioms by linked id; the proof map linked (F-25, F-26).
- The SysML v2 model named once in F.2 and D (F-30).
- The check-design table of B.12 to `paper/supplement/` (F-19).
- The smaller cuts and renames F-17, F-18, F-21, F-24, F-29, F-32, F-33.

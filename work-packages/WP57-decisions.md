
## The planning scope drafted (13:31 EST)

`WP57-scope-of-work.md`: a map of every appendix subsection against the sentence that cites it, then children WP57a to WP57e (A and F; B; C and D; E, G and H with the assumptions, limitations and open questions section; re-lettering last). Executes after WP56 lands. The driver approves as his proxy then.

## The planning map approved as proxy (18:04 EST)

Under his autonomous-mode mandate the driver approves G1 of `WP57-scope-of-work.md` now, ahead of WP56's landing:
one unit writes `work-packages/WP57-rounds/map.md` from the supporting material as it is on dev and the paper as
WP55 leaves it (branch `wp55`), reading only, no edit to either notebook. The map marks every subsection whose
citing sentence sits in Sections 7 to 9 as "pending WP56", to be re-read at WP56's landing before the children's
scopes are cut. The children WP57a to WP57e are approved one at a time after WP56 lands, as the scope says.

## The map read and accepted by the driver as proxy (18:28 EST)

`work-packages/WP57-rounds/map.md` (branch `wp57map`, 92f3434; counts by `map_counts.py`, rerun by the driver):
121 cells and 4,440 words of typed prose in the supporting material, about 2,280 words of prose and 3,860 generated
words leaving under the dispositions; every Job block is metanarration by the standing rule and three are stale;
seven subsections uncited. The driver's calls on the six items the map left open:

1. D.18 (the one measurement of Corollary 1) gets a one-line pointer at Corollary 1; the non-goal on main-text edits is
   amended to allow the pointers the map lists (this one, and Section 2's pointer to Appendix G), nothing else.
2. G.2 (the reading pass) moves to the repository as the map proposes, its YAML kept for our own checking; his words
   of WP38 govern ("my intuition is we keep it in its yaml form for our own checking but we may want to drop it from
   the supporting materials ... i want to keep traceability records and assessments without giving the feeling that
   no human validated the citations"). The reviewer's guide's sitting 1 item on G.2 is rewritten by WP58.
3. Appendix H kept, shortened to the three boundaries Section 2's HoroPCA paragraph needs (the map's call).
4. Re-lettering by first mention of any subsection in reading order, computed by WP57e on the text as it then stands
   (after WP56 and WP57a to d), since those packages move citing sentences; his rule is the order of first mention.
5. Section 2 names Appendix G in one sentence beside Table 1 (WP57a); the register entry stands.
6. The four glossary `defined_in` fields that name decision files are repointed in WP57a.

Children: WP57a (front matter, A, F, G) and WP57b (B) are scoped now and run in sequence by one unit after WP55 lands;
WP57c (C, D) after WP56; WP57d (E, H) after c; WP57e last.

## WP57a and WP57b approved as proxy (18:42 EST)

`WP57a-scope-of-work.md` (front matter, Appendices A, F, G; Section 2's one sentence naming Appendix G; G.2 to
`paper/supplement/reading-pass.md` on his WP38 words; the glossary's `defined_in` fields repointed, five not four) and
`WP57b-scope-of-work.md` (Appendix B: the Job block cut, `how_to_read` and B.2 shortened to what the citing sentences
need, every proof reachable by its lemma label, the derivation chain and proof map unchanged), both at d7d3403, are
approved by the driver under his mandate. One unit runs a then b on branch `wp57ab` after WP55 lands; the driver
soft-confirms each appendix on screenshots before the next child.

## WP57a and WP57b accepted as proxy and landed (20:52 EST)

Read on the unit's screenshots of the rendered appendices (A's table, F, G and G.1's end; B's opening, B.2 and the
L16 table). WP57a d4f6fc5: the companion paragraph and the Job blocks of A, F and G gone; A's register 72 to 65 rows
without the Layer column, five `defined_in` fields repointed; G.2 to `paper/supplement/reading-pass.md` (55 rows,
generated, with a staleness test), cited in one line at the end of G.1. WP57b 88ce016: B's Job block gone, "What the
scripts establish" kept; `how_to_read` shortened; B.2 is one paragraph of 121 words on restarts, stopping and the
polish; all 25 "Appendix B, Ln" pointers of Sections 3 to 6 land on their result; the derivation chain and proof map
unchanged (22 files, 549 steps). The driver's one landing edit (04a1e3a): B.2 named "its step (3)", a step the
algorithm no longer has, and now names the descent rule (L15). Supporting material after both: 115 cells, typed prose
4,440 to 3,591 words, metanarration count 16 to 8. Register: C131, C161, C132 to C136, C139 to C146 and C667
retired; C1101 and C1102 added (C967 to C1100 left to WP56). Checks: fast suite 2,086, slow paper 27, paper tests
rerun after the edit 206 passed; lint, format, lock, vocabulary clean. Landed on `dev` at 07842b7; CI 43788752177.
Queued for WP57d: `WP57-rounds/assumptions-queue.md`. For WP58: the dead glossary entry termination-status; five
`defined_in` fields naming repository records; the live lists that still say "Appendix G.2"; the stale myst.yml
comment "(Appendices A to G)".

## WP57c approved as proxy (00:50 EST)

`WP57c-scope-of-work.md` (Appendices C and D) is approved by the driver under his mandate, after WP56's landing at
bdd06c5. Its first commit lands what WP56 moved (`WP56-rounds/moved-to-appendix.md`) and rewrites D.19's rule
paragraph to Section 8's four rules, which D.19 contradicts until then; the rest follows the map's dispositions with
every "pending WP56" row re-read against the pointers as WP56 leaves them (C.5, C.8 and D.17's typed pointers and the
old C.8 slot sentence left Sections 7 to 9; D.9 is reached by a default; D.18 gets Corollary 1's pointer by call 1).
Ids from C988. One unit on branch `wp57c`; the driver soft-confirms C and D on its captures before landing.

## WP57c accepted as proxy and landed (03:45 EST)

Read on the unit's captures of the rendered appendices (`WP57-rounds/c/`: C's opening, C.5, C.8, D's opening, D.8,
D.17, D.19 and Corollary 1) and its cold read. Branch `wp57c` rebased onto `dev` at 78a40d1 (the OQ-11 commits) and
fast-forwarded: ba4e188 (D.19 states Section 8's four rules as a list; the shortlist table carries the coverage
probability and the mark for the 17 of 28 designs nondominated on fleet cost and coverage probability; WP56's moved
material landed in D.3, D.4, D.5, D.10, D.15 and D.17; `tension_sentence` and `decision_detail` retired) and 772e343
(the G1 table re-read at WP56's landing; C's opening and D's Job block gone; C.5 to one primary preview and the 17
pairs at |Spearman| 0.5 or above in either regime, the rest in `paper/supplement/metric-associations.md`; C.8 the cost
paragraph with its lower-bound sentence, the rest on `examples/adcs/case-model.md`; D.1 and D.6 to
`paper/supplement/`; D.2 and D.12's tables into D.8 and D.12's paragraphs onto `docs/user-guide/termination.md`; D.7
generated under D.17; Corollary 1 points to D.18). Typed prose C 789 to 329 words and D 1,624 to 1,314 (the map's
estimate for D missed by about 300 words, most of it WP56's material landing there); the supporting material 3,589
to 2,819 typed words. Register: C988 to C996 added; C032, C147, C153, C424, C609 to C611, C620, C621, C661, C797 and
C798 retired; eleven re-anchored. Every line of `WP56-rounds/moved-to-appendix.md` marked.

The driver's calls: the two amendments accepted (the D-numbering test asserts order only until WP57e re-letters; the
termination page's budget 743 to 767 for D.12's 24 words); `recovery_sentence`, printed nowhere now, stays in the
generator and joins OQ-14 with the decision's unused picks, since it feeds the stability record through
`paper_perturb.py` and leaves with that record's regeneration; the D.9 default taken (the nondominated sentence names
D.9 for its counts). R-1 to R-6 met: the G1 table and the `references_resolve` test; the residual checker with the
supporting notebook at or below dev on every count; the paths in the review; the D.19 rules test; proof map 22 files,
549 steps and the data diff empty; lint, format, lock and vocabulary clean. The driver's independent run on the
rebased tree, exit codes captured: fast suite 2,091 passed; slow paper tests with the docstring test 31 passed;
register 21; R-1 and R-4's named tests 4 passed; mkdocs built; the supplement check clean. No attribution line on
either commit. CI 43833554284. For WP57e: D runs D.3 to D.19 with gaps. For WP58: `decision()`'s retired picks and
`recovery_sentence` (OQ-14).

## WP57d approved as proxy (05:03 EST)

`WP57d-scope-of-work.md` (Appendix E as "Assumptions, limitations and open questions" in the map's three parts, the
assumptions table generated from `derivation/axioms.py`, the nine queue lines placed, every open OQ listed once;
Appendix H by the map: the Job block and H.1's self-description cut, H.5 to the repository unless a sentence needs it)
is approved by the driver under his mandate, after WP57c's landing at 772e343. Ids from C997. One unit on branch
`wp57d`, dispatched when the regime rename lands and releases the supporting notebook; the driver soft-confirms E and H
on its captures before landing.

## WP57d accepted as proxy and landed (07:27 EST)

Read on the unit's captures of the rendered appendices (`WP57-rounds/d/`: E's opening and E.1's two tables, E.2's
table and the gaps table, E.3, H.1 and H.4) and its cold read. Branch `wp57d`, based on `dev` at 2db089d5 (no rebase
needed), fast-forwarded: c8f8407b, one commit for E and H, since both live in the supporting notebook and each commit
is to pass the suite (the scope allowed one or two). E is "Assumptions, limitations and open questions" in three
parts. E.1: two tables generated from `derivation/axioms.py` and the proof map (A0 to A11 and R1 to R3, each with the
section that states it and the lemmas that import it, each lemma a link to its proof; I1 to I18 and F5 to F19 with
their citations), nothing typed but the captions. E.2: a typed table of 39 limitations, one per row with the section
it left and its record, then the gaps table in four columns, each gap linking its row of the ledger. E.3: OQ-1 to
OQ-10 and OQ-12 to OQ-14 in the ledger's order and words, then Section 9's two research questions; OQ-11 (closed)
absent. All nine lines of `WP57-rounds/assumptions-queue.md` placed and marked. H: the Job block and H.1's sentence
about the appendix cut; H.2 to H.4 kept; H.5 moved verbatim to `notes/directions/wp35-horopca-formalism-and-solvers.md`
and cited in one line at the end of H.4, after the check that no sentence of Sections 2 to 9 needs it. No main-text
edit; the anchors `appendix-e` and `appendix-h` resolve. Typed prose E 92 to 1,637 words (a list of items with their
records; link targets counted), H 664 to 513 (rendered 916 to 751, the ceiling lowered to 751); the supporting
material's generated words 53,460 to 52,619. Register: C997 to C1050 added; C585 to C588 and C591 retired; none
re-anchored.

The driver's calls: the one-commit delivery accepted; the unit's reading of the research questions' records accepted
(successive trade-offs has no readout in `notes/directions/`, so its row names the design specification and the
choosing-K guide); where the map's section 2.1 and the paper differ, the paper governs (six items no longer in the
paper are not listed); E.3 lists the repository-internal questions OQ-12 and OQ-14 beside the method's, as the scope
asked for every open entry, and his read decides whether they stay. R-1 to R-6 met per the review's tables. The
driver's independent run on the merged tree, exit codes captured: lint, format, lock, proof map (22 files, 549 steps),
vocabulary (0 new), supplement check, register 21, fast suite 2,095 passed, slow paper tests with the docstring test
31 passed, mkdocs built, data and derivation diff empty; residuals exit 1 as on dev with the same rises, the
supporting notebook at or below dev on every count. No attribution line. CI 43866677782. For WP57e: E keeps its
letter here; the supporting page's table numbers after E moved by three. For WP58: E.3 links `WP57c-review.md`,
`WP56-rounds/ternary/readout.md` and `WP36-decisions.md`, which need the archived hash when those documents leave
the tree.

## WP57e approved as proxy (07:50 EST)

`WP57e-scope-of-work.md` (re-lettering once, last, by his rule of first mention as the map's call 4 records it; the
order recomputed on the paper as it stands; subsections renumbered consecutively; every anchor, id, label, pointer,
register anchor, ledger key, baseline key, test literal and docs link following; dated records left as written; no
other change) is approved by the driver under his mandate, after WP57d's landing at c8f8407b. On the paper at
c8f8407b the rule gives G, D, H, A, B, C, E, F: the register of prior art becomes A (Section 2 names it beside Table
1), the case tables B, the HoroPCA comparison C, notation D, the proofs E, the case model F, the assumptions section G,
reproduction H. Every letter changes; the result goes to him with his read, where the rule is his to revise, and the
package is rerunnable. One unit on branch `wp57e`; the driver soft-confirms on its captures before landing. After it
lands: the parent's D-3, a read of the whole supporting material, then WP58.

## WP57e accepted as proxy and landed (09:23 EST)

Delivered on branch `wp57e`, one commit, 64f01a1d, off the head 6d86038d (no rebase). The order recomputed on the paper
at the base by `map_counts.py`: G, D, H, A, B, C, E, F, so the register of prior art is A, the case tables B, the
HoroPCA comparison C, notation D, the proofs E, the case model F, the assumptions section G and reproduction H; old
D.3 to D.19 are B.1 to B.14 and every other appendix keeps its numbers under its new letter. One detail against the
scope's purpose line: H's (old F's) first mention is Section 8's closing paragraph, not Section 11; the order is the
same. 43 tracked files follow (the paper's 74 roles as the only main-text edit; the supporting notebook's headings,
anchors, cell ids, labels and cell order, re-executed; generators' link constants renamed after their targets; 96
register anchors and two fragments; the ledger's ceiling keys and each row's `section` key; the residual baseline's
keys renamed, not regenerated; the checkers' patterns; tests; docs, the case, the glossary's two `defined_in`; the gaps
ledger that G.2's table prints). Dated records left as written, each named in `WP57e-review.md` with its reason.
Numbering test restored and a first-mention test added, so the rule is checked on every run. Register: no id added
or retired.

The driver's calls: the unit's four readings accepted (a ledger row's `section` follows because it is the key the
ceiling sums by, its text as written; the baseline renamed so no rise of dev is absorbed; the gaps ledger follows as
the source of a printed table; the surface-id pattern widened to H). Test function names keep their dated letters
(56 register backings and `scripts/check.py` cite them); a rename is WP58's if wanted. The one register `note` that
carries a role to an old anchor (OQ-14's, `sub-d-19`) is provenance text that nothing renders, left for WP58 with the
other dated fields. R-1 to R-6 met per the review (85 pointers, 0 land elsewhere; word diff 0 changes beyond letters
and numbers; outputs letters only but H.1's commit row and H.4's row order; the build log clean). Soft-confirmed on
the captures: the outline A to H with consecutive numbers, the eight openings, Section 2's pointer landing on B.11 and
Section 6's on G. The driver's independent run on the branch, exit codes captured: lint, format, lock, proof map (22
files, 549 steps), vocabulary (0 new), supplement check, register 21, data and derivation diff empty, word diff,
pointers, R-3 grep, mkdocs, fast suite 2,097 passed, slow paper tests with the docstring test 31 passed; residuals
exit 1 as on dev with dev's 126 rises less one (the supporting material's terms undefined at first use, now under its
baseline). No attribution line. Fast-forwarded and pushed; CI 43885046691. For his read: every letter changed, the
rule his to revise, the package rerunnable from `WP57-rounds/e/reletter.py`; the supporting page's table numbers
follow page order (HoroPCA Table 1, the assumptions Table 2, cited Table 3, gaps Table 4); C's table caption names its
own appendix in plain text, a wording edit for WP58. Next: the parent's D-3, a read of the whole supporting material,
then WP58.

## WP57 D-3 delivered and landed (10:46 EST): the whole supporting material read at five depths

On his go-ahead ("Yes, start D-3"), one unit read the paper and the supporting material as served at c2b80421, cold
first and against the children's records second; `WP57-review.md` and 70 captures under `WP57-rounds/review/` landed
at 2dbd8dd8 (the branch rebased onto the records head; lint and format clean; no attribution line; nothing outside the
review and its folder). 85 pointers followed; 34 findings: 3 that block the read, 17 that cost the reader, 14 cosmetic;
20 new, 14 with an earlier record. R-1, R-3, R-4 and R-5 met; R-2 met by the checker and not by the read (two
sentences about the paper's text the checker misses).

The driver's calls. The three blocking findings are verified on the served page: F-1, every one of the paper's 49
"Appendix E, Ln" pointers lands on E's preamble, the proof up to fifty screens below (the proof headings are output
cells, so they carry no site anchor a role can target; the fix is a design step of WP58, not a retarget alone); F-2,
the three generated links on the supporting page itself (B.1, B.3, B.10) are written page-relative for the paper's
page by `paper_common.appendix_link` and 404 from the supporting page (a one-line generator fix, WP58); F-3, the 178
repository links point at `blob/main`, 2,011 commits behind dev, so each 404s on the staged site until main catches up
or the links pin a commit (his call). Of the seven items the review lists for his read, F-3 is his now; the other six
(one home per caveat, F-7 and F-8; Section 6 and B.13's overshoot, F-15; the feasibility order and the source of the
verdicts, F-5 and F-31; the table numbering, F-4; the proposal count, F-14; the proof pointers, F-1) go to him with the
parent's record and are worked in WP58 after his word where they touch the main text. The review's seventeen WP58 items
are adopted into WP58's scope as proposed. The parent WP57's good enough is met (map accepted, five children landed and
soft-confirmed, re-lettered once, R-1 to R-5 per the review); its done waits on his read.

## His answer on the repository links (12:22 EST, verbatim)

Asked (popup, three plain options: pin to the build's commit; keep `blob/main`; point at dev): "point at dev but
consider repointing to main upon release". The driver's reading: every repository link the supporting material and the
docs write (`blob/main`, 178 on the supporting page) points at `blob/dev` from WP58 on, and the release checklist
carries the step "repoint the repository links to main" for his decision at release. Worked in WP58.

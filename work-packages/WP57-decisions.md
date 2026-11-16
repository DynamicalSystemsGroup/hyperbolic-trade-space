
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

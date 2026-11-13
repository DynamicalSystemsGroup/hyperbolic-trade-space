# WP39 review: the case ends in a decision

For the supervisor's acceptance. Scope: `WP39-scope-of-work.md` (approved at fe2335e); decisions: `WP39-decisions.md`.
Reviewed head: `7b81e26` on `dev` (the subsection's text is as of `f89c663`, accepted as rendered at 10:35 on 2026-11-14).
Each line below names its backing (a command, a commit, a test or a read file). Where a line cannot be backed, it says so.

## Summary

The package is built and read. Section 9 closes with "What the executives decide": one paragraph and a six-row table, with
the 28-design table and the rules in Appendix D.19. Both cold readers followed the reduction to the two-way choice and both
said easier. The first read found one blocker ("Table ??"), fixed in `50d8427`. The re-read after the second fix unit finds
no blocker and no "Table ??"; it leaves four "slows" and four "polish" items, listed below, none of them in the closing
paragraph's meaning. The skim test put seven sentences off; four were changed, three are left or reported. Three items
need the supervisor (below). Acceptance is the supervisor's.

## Requirements R-1 to R-13

| ID | Status | Evidence |
|---|---|---|
| R-1 numbers generated and registered; table and sentences from one function | Met | `paper/generate_findings.py` (`decision`, `decision_sentence`, `decision_table`) built in `52208db`; stability entries in `82ab799`; register rows moved with the wording in `50d8427` and `f89c663`. Command: `uv run pytest -q tests/test_claims_register.py tests/test_paper.py` (result in the gates line below). The perturbation clause (a changed input moves the sentence and the register fails) is covered by the tests of `52208db` and `82ab799`; I did not re-perturb the input by hand in this review. |
| R-2 priced in program currency | Met | Paragraph, sentence 3, quoted by P8 (read-P8.md Q2): "One question remains, and it is theirs: whether a fine star tracker, which brings the pointing error from about 0.003 to 0.0008 degree, is worth about 0.56 M USD of a 6 M USD fleet cost limit." The fleet-size range is the 4 and 5 fleets at 1.13 M and 1.69 M USD. P7's arithmetic: 1,686,142 minus 1,127,465 = 558,677 (read-P7.md, numbers table). |
| R-3 readable without subsystem detail | Met, with one caption note | Paragraph, rendered, searched here for `exponent`, `term`, `id`, `log V`, `lemma`, `D.n`: no match (a script over the rendered output of cell 97 of `paper/paper.ipynb`). The table caption does say "log V at K = 2", glossed in words in the same clause; the P8 re-read item 6 asks for it dropped (polish). The ids and the full configuration are in D.19, not in the table. |
| R-4 nominal clause and C.8; the model prices and does not choose | Met | "The method prices the question and does not answer it; the numbers are nominal (Appendix C.8)." P7 quotes it for Q2 (read-P7.md); P8 says it raised trust (read-P8.md). P8's re-read could not tell what "nominal" means for the dollar figures (estimates or placeholders): open question for the supervisor, not a fault of the pointer, which P7 followed and found works. |
| R-5 what the method does not tell | Met | Table caption: "The method does not tell the schedule or the risk, what to buy beyond the modelled parts, or what a larger fleet is worth." P8 and P7 both noticed it. P7 notes it sits in the caption and not the paragraph; left as decided (Q1 (c) shape, Draft 2). |
| R-6 the shortlist is the 28 within both bands; each named design is in it and passes the six requirements | Met | The generator's assertion and test (`52208db`); P7 checked every design named in the table against the D.19 shortlist: the five table designs 999, 2950, 1858, 766, 2356 match to rounding, and all 28 have pointing error, unit cost and fleet cost inside the D.17 limits (read-P7.md). The slew power, control effort and mass requirements were not checkable by P7 (columns absent); the generator asserts that every named design passes all six requirements (`generate_findings.py`, the check at line 732 of the generator), which I read and did not re-run apart from the test suite. |
| R-7 the P8 and P7 cold reads | Met on the reading; polish items open | See "The cold reads" below. |
| R-8 skim test | Run; remedies applied for four of seven put-off sentences | See "The skim test" below. |
| R-9 entry-surface changes listed | Met | See "Entry-surface changes" below. |
| R-10 ceilings hold; each added sentence has a job; cuts state what the text no longer did | Met | Run here: the paper's own counter gives Section 9 at 1,734 of a ceiling of 1,736, the paper's counted words 10,354 against a total ceiling of 11,725 (the function `words_by_section` and `ledger_ceilings` of `tests/test_paper.py`). The ledger rows are at `paper/length_ledger.toml` (WP39 block from about line 1423): the raise rows with their jobs, the Candidates cut (48 words, "no_longer_did" stated), the K-choice shortening (35 words). The second fix unit added no raise (decisions entry at 10:35). |
| R-11 cascade resolved; Figure 9 and its paragraph unchanged | Met | `grep -c "Table ??" paper/paper.ipynb` gives 0; the label `tab-decision-case` resolves (P8 re-read: 0 occurrences of "Table ??" on the page, "Table 2" resolves). The Candidates cascade (D.7, generator sentence, perturbation entry, pointer) was done in `20bff6e` and the sensitivity tests in `50d8427`; CI on `74b470f` was red on the two sensitivity tests and fixed there (driver log, `54c4032`, `384e7ae`). I did not diff Figure 9's cells in this review; the second fix unit's diff (`f89c663`) touches the notebook only in the decision cells. |
| R-12 vocabulary | Met | `uv run python scripts/check_vocabulary.py` (result in the gates line). "defensible" is not in the paragraph or the table. |
| R-13 gates | See the gates line | Commands run here, below. No AI attribution in the commits of this package (grep below). |

Gates, run at `631d7a7` in this worktree: `uv run pytest -q tests/test_claims_register.py tests/test_paper.py`: 218 passed, 3 skipped (17 min on a loaded machine); `tests/test_text_encoding.py`: 2 passed; `uv run ruff check .`: all checks passed; `uv run ruff format --check .`: 660 files already formatted; `uv lock --check`: resolved; `uv run python scripts/check_vocabulary.py`: 0 new violations, 63 known; `git log 9b284fa..HEAD` message bodies contain no co-author or generated-by line (0 matches). Not run here: `tests/test_site.py` and `tests/test_docs.py` (they build the site and did not finish in the time available, and I stopped them); the driver's record is the fast suite passing on `f89c663` (decisions entry at 10:35) and 0ccc0a3's site tests, so R-11's site and docs half rests on that record and not on a run of this review.

## The cold reads (R-7)

Files: `work-packages/WP39-rounds/reads/read-P8.md`, `read-P7.md` (first reads, head `a538fc4`), `read-P8-reread.md` (head
`8699324`, after the two fix units). Screenshots were not saved: the readers' browser tabs were not fronted, and the pane
refuses to composite frames for a tab that is not in front, so each read is from the rendered page text (read-P7.md says
so; read-P8.md says its screenshot was returned to the reader and not written to disk). The rendered page was therefore read,
and not seen by these readers, and no image is in the record.

**First reads (a538fc4).**

- P8 Q1: "Partly ... I stopped following at 'lie within the band of both fits'". Q2: easier, quoting "One question remains, and it is theirs: whether a fine star tracker, which brings the pointing error from about 0.003 to 0.0008 degree, is worth about 0.56 M USD of a 6 M USD fleet budget." 9 findings: 1 blocks, 5 slow, 3 polish.
- P7 Q1: "Yes for the arithmetic and the logic of 2,134 to 28 to a two-way choice. I stopped at 'lie within the band of both fits'". Q2: easier, quoting "The method prices the question and does not answer it; the numbers are nominal (Appendix C.8)." 5 findings: 1 slows, 4 polish. Every number cross-checked against D.19 and D.17 and found in agreement.
- The test of R-7 (both follow, both say easier) is met on the reading.

**The blocker and its fix.** P8 finding 1, verbatim: "(the executives' call: Table ??; tables: Appendix D; digits that
hold: D.11)", an unresolved reference. P7 found the same (finding 1). Fixed in `50d8427` (the table takes the label
`tab-decision-case`, cited with `numref`). Backed: `grep -c "Table ??" paper/paper.ipynb` gives 0, and the re-read finds
"Table 2" resolving and 0 occurrences of "Table ??" in the page text.

**The other findings and their dispositions.** Fixed in `50d8427` and `f89c663`, per the ruling at 09:05 (48f823c): the
band glossed at the point of use ("the near-frontier band of both fits, the simpler and the richer"); "regrets least"
became "gives up the least of either measure among the 5 of the 28 that no other beats on both"; "6 M USD fleet budget"
became "6 M USD fleet cost limit" (C.8 puts the full budget at 8 M USD: P7 finding 2, a correctness fix); the table's
configuration column cut to wheel class, tracker grade and fleet size; the caption names what the level is and why the last
two rows are there; D.19 shows the two term levels (P7 finding 5); the roles "operator" and "sponsor" are introduced as the
case's two stakeholders at first mention (P8 finding 9). Not changed: P8 finding 7 (rounding 0.0008 against 0.00074,
polish, fine as is by the reader's own words) and P8 finding 8 (the baseline sentence stays in the caption; the caption now
also names the unit cost it misses, finding 4 of P7).

**The re-read (P8, head 8699324).** Q1: "Yes for the last paragraph taken alone; the route to it through the section I did
not follow. I stopped following at 'At K = 1 the exact-maximum fit has a 7-lemma across controls, power and energy, plus
cost'". Q2: "Easier at the end, harder in the middle", quoting "One question remains, and it is theirs: whether a fine star
tracker, which brings the pointing error from about 0.003 to 0.0008 degree, is worth about 0.56 M USD of a 6 M USD fleet
cost limit." Counts: blocks 0, slows 4, polish 4. The scope's test for R-7 is the reader's answers about the section that
was built, the closing subsection. The "harder in the middle" is outside it: it names the paragraphs before the
subsection, Section 9's third paragraph ("7-lemma", "exact-maximum fit") and the "Two terms" paragraph ("the mean slack, read
at the K = 1 temperature, drops most at K = 2 (0.08 and 0.05)"), which this package did not write and was told not to
rewrite (non-goals: no rewrite beyond the put-off sentences of the skim test). The reader names no sentence of the
subsection as making the call harder. Those sentences are listed below as findings for the supervisor and the final reader
round, not as WP39 faults.

Re-read findings by place:

| # | Where | Sentence quoted by the reader | Status |
|---|---|---|---|
| 1 | Section 9 opening line (outside the subsection, but the pointer to it) | "what contends, how, and where designs sit (the executives' call: Table 2; tables: Appendix D; digits that hold: D.11)" | open polish: names three places in one breath; the reader would say "the decision is in Table 2 at the end of this section" |
| 2 | Section 9, "One term" (outside) | "the exact-maximum fit has a 7-lemma across controls, power and energy, plus cost" | open, outside WP39: method words, where the reader stopped following |
| 3 | Section 9, "Two terms" (outside) | "the mean slack, read at the K = 1 temperature, drops most at K = 2 (0.08 and 0.05)" | open, outside WP39: reader asks that method-detail stretches be marked as skippable |
| 4 | Subsection, sentence 4 | "gives up the least of either measure among the 5 of the 28 that no other beats on both" | open polish: plain after one re-read, the densest phrase of the paragraph; the reader would name the compromise and its cost against each end. Not changed, as it is the wording the ruling fixed at 09:05 |
| 5 | Subsection, sentence 2 | "lie in the near-frontier band of both fits, the simpler and the richer" | open polish: **"band" is not plain** (reader: "'band': not plain ... I read it as 'close to the best', acceptable by guess"); a short gloss or drop "of both fits" |
| 6 | Table caption | "level of each (log V at K = 2: the distance above or below the fitted reference surface, not a ranking)" | open polish: drop "log V at K = 2" from the caption |
| 7 | Table, level column | "+0.010" beside "-0.012" | open polish: a higher level can be taken as better; the reader would put "not a ranking" in the column header |
| 8 | Figure captions | "Figure 5:Log-metric plane of the K = 1 fit..." and the "enlarge" control | open polish: no space after the colon in captions (the table caption shows the same, "Table 2:The baseline ..."), and the page chrome in the text flow; a rendering matter, not seen by me (no image) |

The reader's three wordings: "band" not plain (item 5 above, reported as an open polish item); "gives up the least of either
measure" plain after one re-read; "level" plain only through the caption's gloss. Reader's "what I could not tell" also
lists: whether 0.56 M USD is the tracker alone or the fleet difference (the text gives 1.69 M less 1.13 M and the reader
infers the second), why the operator-alone fleet of six is not the answer, what "nominal" means for the dollars, how
uncertain the 28-design shortlist is. None is a sentence that makes the call harder; the first and third are candidates for
one clause each, for the supervisor to say whether they earn a place.

No sentence in either read, first or second, says that the method decides or ranks. The nearest is the caption's "the designs the
rules pick" (re-read) and the row label "balanced between the terms" (P7, first read); both are defined as rules in D.19.

## The skim test (R-8)

File: `work-packages/WP39-rounds/reads/skim-P8.md` (head `a538fc4`, text read, no screenshots). What the reader took away in
two minutes: "A new way to read a trade study ... I could not tell what it costs me, how long it takes my team, or what
decision I would defend differently to a board." Verdicts by surface, and what was done:

| Surface | Verdict | Put-off sentence, as the reader quoted it | Disposition |
|---|---|---|---|
| Site root, adoption line | neutral, leaning put off | "few designs determine the exponents only weakly" (in "from package-only install to a first fit took 31 s, ...") | Changed, `50d8427`: "with few designs, how strongly each metric counts (the exponents) is only weakly determined". The reader asked for "trade-off strengths"; the ruling kept the term in a gloss so the claim keeps its word. Listed. |
| Site root, What | put off mildly | "Its unit is the n-lemma, a power-weighted product of the metrics that names which of them compete on one part of the trade space." | Changed, `50d8427`: "a combination of the metrics". Listed. |
| Paper abstract | neutral, mixed | "gives the data a coordinate system"; "Modelling a single n-lemma fits a monomial, which transforms into a convex program and is solved directly". Encouraging: "A trade study must produce an answer and a justification an accountable executive can follow." | Reported, not touched (supervisor's text). Listed for the supervisor. |
| Section 1, opening | encouraged | "Decision analysis has two products: an answer, and a justification an accountable executive can follow and defend." | None needed. |
| Section 1, contribution line | encouraged | "Of 2,134 feasible cubesat designs, the nondominated set holds 236 on 4 attributes ... and 2,134 on all 13" (the regeneration parenthesis is "noise") | None; the parenthesis serves the checker. |
| Discussion, first lines | neutral | "Interpretation is human validation. The fit reports what contends; whether that is an explicable trade-off is for an engineer to decide." | None. |
| Conclusion ("Future work and final remark") | put off | "Beyond Python, a Rust core compiled to WebAssembly, whose verification tools address panics and overflow, not numerical accuracy." and "Beyond log-affine conditioning, kernels that keep the fit a generalized geometric program (GGP)." | Left, with the reason: each is a backed claim (C566 and the GGP sentence) whose substance is the jargon; the ruling at 09:05 says they serve the method reader. Listed for the supervisor. |
| Docs root | neutral | "a sum of monomial terms, where a monomial term (a product of powers of the metrics) is one trade-off" | Changed, `50d8427`: "a sum of terms, where a term (...)". Listed. |
| Docs Examples | put off | "At the one-term temperature (case.mean_slack_fixed_tau) the mean slack falls from 0.122 to 0.043." | Changed, `50d8427`: "the mean slack (the designs' average distance from the fitted frontier)"; "so that mean level cannot choose K". The numbers 0.122 and 0.043 are as they were. Listed. |

Seven sentences were named; four are changed (the two root-page sentences, the docs-root sentence, the Examples sentence), the
two conclusion fragments are left, the abstract's two are reported. The decisions file's ruling lists the same split
(48f823c). `git show --stat 50d8427` shows the changes in `site/index.html`, `docs/index.md` and `docs/examples.md` only,
with no other entry-surface file (README, the history page) in it. Beyond the put-off sentences, the diff of those files
in `50d8427` holds only the two sentences and the Examples pair named; I read `git show 50d8427 -- site/index.html
docs/index.md` and saw nothing else in them (the Examples diff is four lines).

Not an item of the skim test but an entry-surface change in the same package's window: `0ccc0a3` moved the root page's needs
block to the end as the supervisor's ruling on WP33 (b8c4e2d). It is listed in the review list under that ruling.

What the skimmer could not tell, in the reader's words: "What adopting it costs a program in money or calendar time beyond a
31 s install"; "the word 'conditioning' is never explained on the root page"; "What decision on the cubesat case would differ
because of this method, and what I would tell a board" (the last is what the package's subsection answers, one click down).

## Entry-surface changes (R-9)

Rows in `work-packages/supervisor-review-list.md`, "Entry surfaces", checked against `git log`:

| Surface | Row's commit | `git log` check |
|---|---|---|
| Root page, adoption line | 50d8427 | `git show --stat 50d8427` includes `site/index.html` |
| Root page, What | 50d8427 | same |
| Docs home | 50d8427 | `git show --stat 50d8427` includes `docs/index.md` |
| Docs Examples (not one of the five, its first screen) | 50d8427 | includes `docs/examples.md` |
| Root page, needs block moved last | 0ccc0a3 | `git show --stat 0ccc0a3` includes `site/index.html` (WP33's ruling, not the skim test) |
| Paper conclusion, not changed | n/a | no commit; row states why |
| Abstract, not changed | n/a | no commit; the row names the two sentences |

The row for the notebook unit's own change (the decision subsection) cites "notebook unit 20bff6e; clean execution
a538fc4" and was written at `c9bc069`. One thing to correct: that row still reads "a 6 M USD fleet budget", which the second
fix unit changed in the paper to "fleet cost limit" (`f89c663` changed only the Examples row of the entry-surface table in the review list,
not this row). The row is stale by that one phrase; it is not changed in this commit.

## Lifecycle stage 6: the cascade

What is consistent, and how I know: the ledger and Section 9's ceiling (1,734 of 1,736, counted here); the register and the
generator (the register and paper tests, gates line); Section 9's pointer to the table resolves (Table 2); Appendix D.19 is
the detail the caption and the paragraph point to and the reads checked it against C.8 and D.17; the review list rows and the
decisions file name the same dispositions; the docs pages and site tests (`tests/test_site.py`, `tests/test_docs.py`) are in
the gates line. What is not claimed: that Figure 9 is unchanged (not diffed in this review, see R-11); that CI on `main` is
green for this head (I did not run a merge; the driver log records CI runs for earlier heads); that the rendered page was
seen as an image by any reader (it was not).

**Word counts.** Section 9: 1,734 words against its ceiling of 1,736 (the counter of `tests/test_paper.py`, run here). The paragraph
was recorded at 141 words at the notebook unit's acceptance (the ledger's raise row said 145 for the paragraph as first
planned). The paper's counted words: 10,354 against the total ceiling of 11,725.

**Stability.** The decision text's quantities take the stability treatment (decision of 2026-11-14 00:05; commit `82ab799`):
the counts, pointing errors, prices and the tracker difference were measured on the five regenerations and none moved. Per the
decisions file, the generator prints the counts, the baseline row, the level cells and the 28-design table exactly
(`generate_findings.py`: "exact on the data of record", "the baseline is not a pick: no stability entry, exact"); stability
covers the numbers quoted in the prose (the "about" figures and the rounded prices). I did not re-measure the five
regenerations in this review.

## For the supervisor

1. **The abstract.** Reported, not touched. The skimmer was put off by "gives the data a coordinate system" and "Modelling a
   single n-lemma fits a monomial, which transforms into a convex program and is solved directly", after being encouraged by
   its first sentence, "A trade study must produce an answer and a justification an accountable executive can follow." The
   rewrite is yours.
2. **"Conditioning" on the root page.** The skimmer says the word is never explained there (the adoption line links it but
   does not say what it is). Listed with the entry surfaces; no change made.
3. **The balanced-row clause.** The skimmer asked, and the re-read asks, why two rows are in the table (the balanced pick and
   the cheapest unit). The caption now says they are context. Whether the balanced-between-the-terms row earns its place for an
   executive at all, or whether a clause saying what it shows to a buyer is wanted (decision on the unfilled clause), is the
   supervisor's call; the build left it as the caption has it.
4. The conclusion's two "Beyond" fragments: left with the reason above; yours to judge.
5. Open polish items from the re-read (rows 1, 4 to 8 above, including "band" not plain) and the two method paragraphs the
   reader could not follow (rows 2 and 3, outside this package): yours to take into the final reader round or drop.

## What no reader could test

- The rendered table and page as an image: no screenshot was saved by any reader (the tabs were not fronted, so the pane
  would not composite). P8's first read took one that was not written to disk. No reader looked at the layout of the
  closing table at phone width, or at the first screen's break (skim-P8.md says so).
- Whether an actual executive, not a persona, would find the call easier: the personas are the scope's test, and the answer
  key's sentence is the assistant's and was not read by any agent of this package.
- Whether the five regenerations hold on another platform for the decision text (the generator's platform-perturbation run
  covers it per `82ab799`; not re-run here).

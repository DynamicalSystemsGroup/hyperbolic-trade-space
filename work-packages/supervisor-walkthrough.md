# Supervisor walk-through: what you accept and review, and against what

Written 2026-11-14, late, from the scopes, review files, decisions files and `driver-log.md`. Ten items, one section each. Acceptance is yours and nobody else's. Your answer is one line in chat, which the driver quotes verbatim in the package's `WPn-decisions.md` as the acceptance record; where nothing is written there yet, the record does not say you accepted. The driver walks each item with you in chat, one at a time. "Driver verified" means the driver's checks as logged, never an acceptance. Staged site: http://localhost:8791/ (docs root `/docs/`, paper `/paper/`, supporting material `/paper/supporting-material/`). Screenshots cited by the older reviews are in git at `2a669de` (`git show 2a669de:<path>`).

## 1. WP33: journeys and signposting

**What.** Every surface routes each kind of reader to their door in a click or two, with nothing aimed at another reader, and the repository smaller than before.

**Against** (`WP33-scope-of-work.md`, good enough): the twelve-row journeys map and a signposting unit on every surface; every cut and placement recorded with its reason; no surface adds net words (R-2) and no persona takes more steps on the repeat (R-10), both rounds recorded; every first screen screenshotted with a reading; gates pass. Amendments (`WP33-decisions.md`): contract amendments 21 to 23 (API pages merged, router page, package docstring); and your rulings of 2026-11-14, 09:15 to 09:30: the needs block moves last as a call to action, the summary becomes a body paragraph before Why, and the block thins to two doors, "Read the paper" and "Use the tool". Those supersede the scope's five-doors test.

**Where.** Root `/`; `/docs/` (five need links first); `/docs/user-guide/` (one-line router); `/docs/api-reference/`; `/docs/examples/`; `/paper/` Section 1 and its Organization paragraph; `README.md` Layout list (not served; read on GitHub). Records: `WP33-decisions.md`, `WP33-wayfinding.md`, `WP33-review.md` with addendum. Tests: `tests/test_site.py::test_word_budgets_hold`, `tests/test_interface_contract.py`.

**Driver verified.** Fresh review at `d801a43`; its findings F-1 to F-8 closed in the addendum. Repeat round: steps 47 to 30. Fast suite 1934 at `722ce86`; CI 43339340106 on that head green on both platforms.

**Open.** U2 and U4 not repeated; no door for a systems engineer (the root doors are yours); "Loading..." placeholders and wide tables to WP8b.

**You answer.** Do you accept WP33? One line.

## 2. WP35: HoroPCA distinguished, "hyperbolic" defined (with Appendix H)

**What.** The paper says concisely and testably how this work differs from HoroPCA and from PCA, and uses "hyperbolic" in one defined sense.

**Against** (`WP35-scope-of-work.md`, `WP35-amendment-1-scope.md`): D-1 to D-8 and R-1 to R-16 hold, and the amendment's A-1 to A-7 and RA-1 to RA-13. In short: one HoroPCA paragraph in Section 2; prior-art rows in one "This work ..." convention; glossary entry `hyperbolic`; every number generated from the spike record; no sentence calling HoroPCA worse or this a PCA; the three fresh readers match the intended reading; clean cascade. Amendment: your 2026-11-13 request that the comparison become Appendix H (falsifiable hypothesis, experiment, results, interpretation, how formalism and solvers differ), the reviewer's judgment you relayed (a bounded synthetic experiment, not a benchmark), and the wording unit (FW-1 to FW-20 except FW-14; ceiling 900 to 920).

**Where.** `/paper/` Section 2 ("HoroPCA." paragraph) and Table 1; `/paper/supporting-material/` Appendix H (verdict-first table, reading limits, H.4), Appendix G pointer, Appendix A "hyperbolic"; `/docs/user-guide/limitations/`. Tests: `tests/test_paper.py -k "horopca or prior_art"`. Records: `WP35-review.md`, `WP35-decisions.md` (reviewer's judgment, 2026-11-13 19:20).

**Driver verified.** Review at `cec9d70`: R-1 to R-16 met, some with notes. Appendix H accepted at `3d5a53e` (CI 43373481676 green); wording unit at `1235f7f` (CI 43394683441 green; fast suite 1943).

**Open.** FW-14 left as written; C4's two links 404 until the merge to `main`; the review notes the second-tier word budget as your call.

**You answer.** Do you accept WP35, Appendix H included? One line.

## 3. WP37: the history page

**What.** A thin page at `/history.html` acknowledging people and lineage over ten years, so the work is not read as AI-generated out of the blue.

**Against** (`WP37-scope-of-work.md`): D-1 to D-8 delivered and R-1 to R-14 hold; your 2026-11-12 rulings on purpose, size ("as thin as we can") and sourcing; every open decision answered or recorded as a default you approve. Amendment D-9 and D-10 (approved 2026-11-12): `history.yaml` is the record, the page its view, tests tie every link, name and year to it. Your 2026-11-13 rulings (Penland, Clark, client projects, slimming, Medley, cadCAD, Boyd) are applied.

**Where.** `/history.html` (linked once from the root footer; back link on top); `history.yaml`; `work-packages/WP37-rounds/open-items.md`, `trace.md`, `w3-check.md`. Tests: `uv run pytest tests/test_site.py -k history`; `scripts/check_history_links.py`.

**Driver verified.** Review `d801a43` plus two addenda: R-2, R-4, R-8, R-12 met at final head. 397 words (aim 350 missed), 69 record entries, 68 links ok, one blocked (Wiley DOI, confirmed in a browser 2026-11-13). Fast suite 1937 at `13ed54c`; page read in the browser.

**Open** (`open-items.md`; none blocks): name spellings, Medium links, firm's name-change date, team's-account marks, Medley write-up, "Nash to Lyapunov" authorship, the nine defaults. WP38 routed 31 flagged sentences on this page to you.

**You answer.** Do you accept the history page, with those open items yours? One line.

## 4. WP38: the residual pass (patterns that read as machine-written)

**What.** A review machinery and one pass over every prose surface that removes unneeded metanarration, parentheticals, caveats and complex sentences, copy-editing only.

**Against** (`WP38-scope-of-work.md`): D-1 to D-4 exist and pass R-1 to R-7; every inventory row read and confirmed (R-9); counts not rising (R-8); no claim lost (R-10, R-11); entry-surface changes listed (R-12); guide names the machinery (R-13); gates (R-14). Your direction of 2026-11-13 and the assistant's calls of 2026-11-14 (`WP38-decisions.md`).

**Where.** `WP38-review.md` (the honest summary first); `WP38-flags/`, `WP38-confirmations/`, `WP38-landed/`; `docs/superpowers/notes/residual-review.md`; `scripts/check_residuals.py`, `scripts/residuals_baseline.json`, `tests/test_residuals.py`. The entry-surface rows are in `supervisor-review-list.md` "Entry surfaces".

**Driver verified.** 1,211 flags, 537 edits landed; words 75,104 to 73,192; parentheticals 757 to 659; long sentences 274 to 188. Review head `c0fe11b`; `116c929` CI 43581901051 green, fast suite 1947.

**Open.** Not "every surface reads clean": 18 of 96 confirmation rows clean, 78 still flagged. R-8 holds only against the retaken baseline. Post-0.1: lemma-script text (163 rows), history-page and abstract rows (yours), Appendix H parentheses.

**You answer.** Do you accept WP38 as delivered, with the post-0.1 list? One line.

## 5. WP39: the case ends in a decision

**What.** Section 9 closes with what the two executives decide: a feasible, near-frontier choice, priced, narrated for people who are not experts.

**Against** (`WP39-scope-of-work.md`; your words in `WP39-decisions.md`): D-1 to D-6 landed; R-1 to R-6 and R-10 to R-13 pass; both cold reads follow the reduction and say easier (R-7); skim test run, put-off sentences fixed, entry-surface changes listed (R-8, R-9); clean cascade. Decided: shape of Draft 2, 28 designs within both bands, no term mapped to an executive.

**Where.** `/paper/` Section 9, "What the executives decide" and Table 2; `/paper/supporting-material/` D.19 and C.8. Reads: `WP39-rounds/reads/` (`read-P8.md`, `read-P7.md`, `read-P8-reread.md`, `skim-P8.md`). Generator `paper/generate_findings.py`.

**Driver verified.** R-1 to R-13 met (`WP39-review.md`, 218 paper and register tests). Fast suite 1946 at `94cb6a1`; CI 43494523985 green. Both readers: easier.

**Open** (your calls, `WP39-review.md` "For the supervisor"): the abstract's two put-off phrases; "conditioning" on the root page; the balanced-row clause; two "Beyond" conclusion fragments; "nominal" and "band" wording. No reader saved a screenshot of the table.

**You answer.** Do you accept WP39? One line.

## 6. WP40: release thinning and repository organization

**What.** The repository a release reader meets is smaller and its README says where things are.

**Against** (`WP40-scope-of-work.md`): D-1 to D-9 landed and R-1 to R-11 pass; a cold look at the README, rendered and as markdown, finds the Layout list accurate and links alive; clean cascade. Decided: the assistant's calls 1 to 8 (`WP40-decisions.md`).

**Where.** `README.md` Layout list; `work-packages/README.md` (retrieval commands); `WP40-rounds/thinning/moves.md`, `before-after.md`; `WP40-review.md`. The README is not on the staged site.

**Driver verified.** Fresh review: R-1 to R-9, R-11 met, ten images retrieved and viewed. Files 1,153 to 820; tracked 69.99 to 21.46 MB; archive 70.94 to 22.16 MB. CI 43514777340 on `996ed15` green.

**Open.** Reviewer's R-10 (checker counts raised by the Layout list) is covered by the WP38 pass; the dangling hash was the assistant's and is corrected to `2a669de`.

**You answer.** Do you accept WP40? One line.

## 7. The third paper unit (requests 93 to 169)

**What.** The final reader round's change requests 93 to 169 landed at `ca352f5`: record defects, figure loop, wording.

**Against.** No scope file. Standards: `CLAUDE.md` (every claim backed, or narrowed or dropped, no caveats added), `docs/superpowers/notes/figure-review.md`, and the triage dispositions in `WP11-final/triage/wave-5.md` to `wave-7.md`. Your own text was not touched; the 20 items routed to you are in `supervisor-review-list.md` (final reader round).

**Where.** `/paper/` and `/paper/supporting-material/`: Theorem 10 (ii), Theorem 11, Corollary 1, Definition 6, D.13, D.19, Appendix E rows G-7, G-13, G-14, G-17, B.2; Figures 3, 6, 7. Records: `paperfix3-record-defects.md`, `figure-review-paperfix3.md`; screenshots `figure-loop/verify-ca352f5-fig6.jpg`, `-fig7.jpg`. Commits `4694ed2` to `ee7fa7b`.

**Driver verified.** Head checks (fast suite 1973); browser pass against the defects file; cold reads of Figures 3, 6, 7. CI 43630979464 green on every job, both platforms. Driver log 19:05 to 23:30: accepted under the mandate.

**Open.** Requests 170 and 171 (Figure 6 line over points, Figure 7 title wrap); L16 docstring wording; held-out reads (waves 8, 9) pending.

**You answer.** Do you accept requests 93 to 169 as landed? One line.

## 8. The abstract landing (`735fa51`)

**What.** Your edited abstract is the paper's front matter, word for word.

**Against.** Your rulings in `WP11-decisions.md`, "The abstract pass": your sentences and order; 500-word target, slight over or under fine; metric, attribute, objective and loss as in the glossary; "piecewise hyperbolic frontiers"; the scikit-learn sentence; the PCA and pull-back sentences; one sentence dropped; "you can land the abstract now". The changes table is in `WP11-final/abstract/draft-2026-11-14.md`.

**Where.** `/paper/`, top; the draft file; `735fa51` and the commits before it.

**Driver verified.** Text diffed word for word against the draft, no difference. Rendered page read: 497 words. Fast suite 1973 at `0070e6d`. CI 43635411288: fast and Windows slow green; Linux slow and docs-paper still running at the last log entry.

**Open.** The abstract stays yours to rewrite. Seven flagged sentences routed to you by WP38. Three old-abstract phrases outside `paper/` are noted for WP42.

**You answer.** Do you accept the abstract as landed? One line.

## 9. Close read of the five entry surfaces

**What.** Root page, README, abstract, history page and docs home, read closely, as you set on 2026-11-12.

**Against.** Your 2026-11-12 rule and the day's rulings; the nine-row table in `WP11-final/abstract/entry-surfaces-consistency.md` (nothing applied). Rows moved since the data gate are in `supervisor-review-list.md` "Entry surfaces".

**Where.** `/` , `/docs/`, `/history.html`, `/paper/` abstract; `README.md` (not served).

**Driver verified.** Root page read in the browser after your rulings; no later commit applies the table.

**Open.** Your two root sentences (the summary paragraph, "bespoke or opaque"); four small edits (trade-offs, contend, "unsupervised learning, beside PCA", README) await your word; gap, hole and white space, and the tension report's name, go to WP42.

**You answer.** Per surface: accept, or the edit you want. One line each.

## 10. Reading pass G.2

**What.** Appendix G.2 says what the paper took from where, so a reader can check it themselves.

**Against** (`WP38-decisions.md`, your G.2 words): three columns (what we say, the source, where in it); no machine verdict; and the claim that the authors validated the record enters the paper only after you have done it.

**Where.** `/paper/supporting-material/` G.2 (anchor `sub-g-2`); `paper/reading_pass.yaml`: 56 rows over 46 sources; open each source at the place named.

**Driver verified.** Three-column header renders (driver log, 2026-11-13).

**Open.** Nine rows are marked "confirm" and one "supervisor" (n 56, your INCOSE article).

**You answer.** Is the paper's reflection of its sources right? One line.

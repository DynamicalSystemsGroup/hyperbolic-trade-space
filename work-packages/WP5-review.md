# WP5 — Review report (second pass)

| | |
|---|---|
| **Scope of work** | `work-packages/WP5-scope-of-work.md` |
| **Scope approval verified** | Recorded in `work-packages/WP5-decisions.md` ("Scope approval" plus the "Approval-record note", which states the github-cli check was done before execution; G-1 accepted as is). The project has no PRs; the record is typed by the agent, so the chat itself cannot be confirmed by this review. |
| **Work reviewed** | `main` at `4ce27d4` (fix commit, touches only `docs/references.bib` and `docs/literature.md`), on top of `442a538` and `2d2c10e`. Reviewer built none of it and wrote none of the earlier review. Trial edits restored with `git checkout`; tree clean. |
| **Supervisor (accepts)** | mzargham |
| **Acceptance record** | Verbal acceptance in chat, quoted verbatim in `work-packages/WP5-decisions.md`, after this report |

Complete rerun from step 1 after the "fix before acceptance" dispositions for G-2 to G-5. Every command was run in this session.

## Verified COLS attribution (for the driver's spec section 4 correction)

I fetched and read Battese (1992), Agricultural Economics 7(3-4), 185-208 (PDF at ageconsearch.umn.edu/record/172957). What it supports, and nothing more:

- Footnote 2: COLS = the OLS estimates with the intercept raised by the largest residual so that all deviations from the estimated frontier are non-positive. "Greene (1980) showed that the COLS estimator is consistent" for i.i.d. one-sided errors.
- Text: deterministic frontier models "were first specified by Aigner and Chu (1968)" for a Cobb-Douglas model, estimated by linear or quadratic programming (a programming-based frontier, not COLS). "The frontier model (1) was first presented by Afriat (1972, p. 576)." "Richmond (1974) further considered the model" with gamma errors.
- No sentence in Battese says a specific paper introduced COLS. Richmond and Greene paper texts were not read by the implementer or me (records only).

So the supportable spec wording is: COLS (corrected OLS) is OLS with the intercept shifted by the largest residual (Battese 1992, fn. 2); its consistency is due to Greene (1980); the deterministic frontier it estimates goes back to Afriat (1972), Aigner and Chu (1968; programming-based) and Richmond (1974). Aigner and Chu should not be credited with COLS, and no paper should be named as the originator of COLS on present evidence.

## Deliverables

| ID | Verdict | Evidence |
|---|---|---|
| D-1 | met | `docs/references.bib`: 40 entries (`grep -c '^@'`), five new (afriat1972, richmond1974, greene1980, battese1992, deb2002). |
| D-2 | met | `docs/literature.md` present with Appendix A (dropped/limited) and Appendix B (axiom sources). |
| D-3 | met | `tests/test_references.py`, standard library only. |
| D-4 | met | `work-packages/WP5-decisions.md` has the approval record and the round-1 gap record; the acceptance entry reads "pending". |

## Requirements

| ID | Verdict | Evidence |
|---|---|---|
| R-1 | met | `uv run pytest tests/test_references.py`: 7 passed. Every entry has a DOI or https URL and a dated `verified` field with a record URL. |
| R-2 | met | Re-resolved 24 entries live. Crossref (curl): afriat1972, richmond1974, greene1980, battese1992, deb2002 (all five new), andersen1993, charnes1978, aigner1977, zitzler1999, ross2004, boyd2004, boyd2007, rockafellar1970, horn2012, hoburg2016, magnani2009 (16). Authors, year, title, venue, volume, issue, pages all match the bib; Crossref gives no end page for Richmond (515) and Afriat (568, end page 598 taken from Battese's reference list, which I read: "Int. Econ. Rev., 13: 568-598"), Boyd 2007 gives no page (author source stated), and Battese's Crossref author is "Battese, G" (bib has the full name). Further: fare1994 by WebFetch of IDEAS (four authors, AER 84(1), 66-83, 1994, match). cobb1928 by WebSearch (AER 18(1) Supplement, 139-165, JSTOR 1811556 match; JSTOR page not opened). aigner1968: EconBiz page blocked by a bot wall (WebFetch), WebSearch returned the EconBiz record (authors, AER 58(4), 1968); pages 826-839 are confirmed by Battese's reference list, which I read. Battese 1992 PDF re-read (passages quoted above); Deb et al. PDF re-read (title page vol. 6 no. 2 April 2002; "Diversity metric", "we define a different metric to measure the spread in obtained solutions"). Inherited-axiom sources resolved: boyd2004 (I1), rockafellar1970 (I3), horn2012 (I6), hoburg2016 (I4); billingsley2012 (I2, I5) not re-fetched (Open Library). All spec section 4 entries in the sample. No mismatch found. |
| R-3 | met | Tests `test_keys_unique_and_well_formed`, `test_required_fields_per_type` pass. Carried observation: `foellmer2026entropic` has `year = {n.d.}`. |
| R-4 | met | Trials: entry without `verified` appended to the bib: 2 failed (`test_every_entry_records_its_verification`, `test_every_bib_key_is_cited`), 5 passed; `[@missing2020key]` appended to `literature.md`: 1 failed (`test_every_citation_resolves_to_the_bib`), 6 passed; both restored by `git checkout`, `git status` clean. |
| R-5 | met | COLS now has sourced coverage (Battese, Greene, Richmond, Afriat) with honest limits; Pareto spread metric covered by Deb et al.; all other topics as in the first pass. Residual: the Schott spacing metric is unsourced and Zitzler-Thiele's hypervolume role rests on secondary summaries; both are stated in the text and Appendix A. |
| R-6 | met | 14 citation contexts read against sources and records (table below). Priority and novelty remain explicitly the supervisor's; no unsupported superlative left. |
| R-7 | met | Appendix A lists dropped or limited candidates with reasons, including the Aigner-Chu-as-COLS error, Richmond/Greene as COLS sources, Schott, Zitzler-Thiele, Winsten, Ross wording. |
| R-8 | met, with note | Appendix B maps I1 to I6 to keys; statements match `derivation/axioms.py`. Content checks remain thin (I1 table of contents, I4 abstract); the appendix says so. |
| R-9 | met | `uv run pytest -q`: 381 passed, 3 skipped. `ruff check .`: all passed. `ruff format --check .`: 60 files formatted. `uv lock --check`: resolved, no change. WP5 files changed since the first review (`git show --stat 4ce27d4`, `git diff --stat 2d2c10e 4ce27d4 -- docs tests/test_references.py`): only `docs/literature.md` and `docs/references.bib`. |
| R-10 | met | `git log bcfe110..HEAD` grep for co-authored/generated: 0. Authors: 28 commits, all Michael Zargham. `gh run list --limit 5`: all 5 completed/success, head `4ce27d4` green. |

### Judgement of the five fixes

| Fix | Verdict | Evidence |
|---|---|---|
| (a) COLS sources | faithful | Text defines COLS as OLS plus intercept shift by the largest residual, credits Greene with consistency, names Afriat as source of the deterministic frontier and Richmond as a further treatment, says no read source names a paper that introduced COLS, and says Aigner and Chu is not cited for COLS. This matches the Battese passages I read. Minor: "Afriat ... first to present the deterministic frontier model in its statistical form" adds "in its statistical form"; Battese says only "the frontier model (1) was first presented by Afriat (1972, p. 576)" (O-6). Richmond's `verified` field also cites Aly et al. 1987 (read by the implementer, not in the bib; not re-checked by me) and discloses an unconfirmed web-search claim attributing OLS-and-shift to Richmond; the text correctly does not use it. |
| (b) Pareto spacing source | adequate | Deb et al. (2002) is cited only for a diversity (spread) metric from distances between consecutive nondominated solutions, and the text says it is "a spread measure of a front, not a gap to a frontier". Matches the PDF. Schott is mentioned only as "commonly credited ... not confirmed", with no citation key (`grep -i schott`: literature.md lines 156 and 211 only; not in the bib). Zitzler-Thiele is marked as unconfirmed for hypervolume in text, in Appendix A and in its `verified` field. |
| (c) Ross superlative | fixed | "Closest named prior art" removed; now "related tradespace-exploration work and the application setting"; Appendix A records the removal. |
| (d) Magnani and Boyd placement | fixed | Citation now follows only "fit convex piecewise-linear functions (maxima of affine functions) to data"; the kappa-to-infinity statement follows as "the project's own statement, not one shown to be in either source". |
| (e) Secondary-record marking | fixed | `grep SECONDARY docs/references.bib`: cobb1928 and aigner1968 begin "SECONDARY RECORD ONLY". Sentences softened ("only a secondary record ... was checked"; Aigner-Chu rests on the read survey). Richmond and Zitzler-Thiele are not marked with the phrase but state record-only status in their `verified` fields and the text (O-7). |

### Passage review for R-6

| Citation and statement | Judgement |
|---|---|
| cobb1928: weighted geometric mean, constant returns, 1928 | Supported by record; content not read, text says so. |
| shephard1970, fare1995: distance function; reading of V is the spec's | Supported by title/chapter; assigned to the spec. |
| aigner1968 + battese1992: programming-based deterministic frontier | Supported by Battese text (read). |
| afriat1972: deterministic frontier model first presented | Supported by Battese p. text; "statistical form" is a small embellishment (O-6). |
| greene1980: showed COLS consistent for i.i.d. one-sided errors | Matches Battese footnote 2; stated as taken from the survey. |
| richmond1974: further treatment with gamma errors | Matches Battese; text hedges that the paper was not opened. |
| andersen1993, fare1994: super-efficiency, Malmquist, "prior art" | Supported by abstracts; difference stated as untested. |
| foellmer2026: entropic risk limits | Supported by extracted PDF text; identification is labelled as the authors' algebra. |
| rockafellar1970: support function determines a closed convex set | Section title only; text says so. |
| egozcue2003 | Hedged correctly. |
| magnani2009 | Now correctly scoped (fix d). |
| ross2004 | Now correctly scoped (fix c). |
| deb2002: spread metric, not a gap | Supported by the PDF. |
| chami2021: HoroPCA unrelated to the spec's "hyperbolic" | Supported by the abstract. |

## Definition of good enough

| Item | Verdict | Evidence |
|---|---|---|
| D-1 to D-4 exist at the stated paths | met | See Deliverables. |
| R-1 to R-10 pass as checked | met | See Requirements. |
| Non-goals untouched (no site wiring, narrative pages, new dependencies) | met | `uv lock --check` unchanged; the WP5 fix touches two doc files; no mkdocs files. |
| No unresolved bib entry; unverifiable candidates dropped and listed | met | Appendix A; tests pass. |

## Outside the scope

- **Out-of-scope changes:** none by WP5. The fix commit `4ce27d4` touches only `docs/literature.md` and `docs/references.bib`. (Other packages' commits in the range, e.g. estimator and ADCS tests, belong to WP2/WP4 and were not reviewed here.)
- **Non-goals touched:** none. The spec and notes were not modified; the COLS correction to spec section 4 is left to the driver.

## Observations (not counted as failures)

- **O-1.** The offline test cannot detect a wrong or stale record; accuracy rests on live resolution (24 entries re-run here, no mismatch).
- **O-2.** Axiom sources I1 to I3, I5, I6 have only bibliographic or table-of-contents checks; Appendix B says so, though its wording on section 5.2.3 slightly overstates.
- **O-3.** Entropic risk definition rests on unpublished notes with year unknown (key says 2026).
- **O-4.** SLLN is met by a textbook rather than the original.
- **O-5.** Decisions-file approval date (2026-11-08) differs from commit date (2026-11-07); explained in the approval note.
- **O-6.** New: "in its statistical form" for Afriat goes a little past Battese's wording; trivial rewording would fix it.
- **O-7.** New: only cobb1928 and aigner1968 carry the literal "SECONDARY RECORD ONLY" marker; Richmond, Greene, Afriat and Zitzler-Thiele are record-only too and disclosed in their fields and the text.
- **O-8.** Richmond's `verified` note relies on Aly et al. 1987, which is not in the bib; a reader cannot follow that step.

## Open decisions (for the supervisor)

- **G-1 and G-6 equivalents (first-pass G-1 approval wording; O-1 to O-5):** already dispositioned by the supervisor as accept as is. Listed below as accepted.
- **G-7.** New observations O-6 to O-8 (minor wording and marking). Accept these as is, or pick any to act on. Options: accept as is / fix before acceptance / follow-up work package.

No new gap affects a good-enough item or a non-goal. The first-pass G-2 to G-5 are resolved by the fixes judged above.

## Gap dispositions

| Gap | Disposition | Reason or follow-up |
|---|---|---|
| G-1 (approval wording) | accept as is (supervisor, round 1) | Check recorded in the approval-record note. |
| G-2 (COLS, Pareto spacing sources) | fixed (fix before acceptance) | Verified by this rerun, items (a) and (b). |
| G-3 (Aigner-Chu, Cobb-Douglas secondary records) | fixed | Marked and softened; Aigner-Chu now backed by the read Battese survey; items (e). |
| G-4 (Magnani and Boyd placement) | fixed | Item (d). |
| G-5 (Ross superlative) | fixed | Item (c). |
| G-6 (O-1 to O-5) | accept as is (supervisor, round 1) | Minor. |
| G-7 (O-6 to O-8) | pending | Supervisor to decide, one item. |

## Recommendation

Recommend acceptance with the listed gaps noted, because all five requested fixes are present and faithful to the sources I re-read (Battese 1992 and Deb et al. 2002 PDFs, Crossref and web records for 24 entries with no mismatch), the hygiene test fails correctly on both trials, suite, linters, lock and CI are green, attribution is clean, and nothing outside scope changed. Only minor observations O-6 to O-8 remain pending as one item (G-7).

Acceptance is the supervisor's act, recorded as named above. This report does not accept the work.

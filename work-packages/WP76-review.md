# WP76 — Review report: the iron-triangle example (Kitchenham-CSC software projects)

| | |
|---|---|
| **Scope of work** | `work-packages/WP76-scope-of-work.md` |
| **Scope approval verified** | His answer "Approved" in the popup of 2026-11-17, quoted verbatim in `work-packages/WP76-decisions.md` ("WP76 approved"), after OD1 ("Not on the page") and OD2 ("Approve the list") were decided; the project's convention is verbal approval quoted in the decisions file |
| **Work reviewed** | Branch `claude/iron-triangle-example-12a7c6`, merge base `dev` c0e210cc (the renamed 0.1 candidate), through the head that carries this report; nothing on `dev` or `main` (`git branch --contains HEAD` lists only this branch) |
| **Supervisor (accepts)** | mzargham |
| **Acceptance record** | His word in chat after the technical verification and his author review of the interpretation, quoted verbatim in `WP76-decisions.md` |

Two fresh-context reviewers (subagents that did not build the work) ran the checks: a first pass at ec8704fa found
four fixable gaps (a stale count in the record, nine model elements without their own rationale, the named verify
test missing, an unlisted file); after the fixes a second pass at 70708ec7 reran every check from the start. The
evidence below is the second pass's, with the author's own runs where named. Every command was run with
`MPLCONFIGDIR` set to a scratch folder (the worktree's matplotlib font cache, an environment matter recorded in
`WP76-decisions.md`).

## Deliverables

| ID | Verdict | Evidence |
|---|---|---|
| D-1 | met | `docs/examples/kitchenham.md` (the five-part arc, 699 prose words of 700); `mkdocs.yml` lists it after the wheat page; `interface-contract.toml` `docs.pages` and `presentation_pages` carry it, `contract_version = 31` (amendment 31 in the document; `dev` took 30 for the rename); `docs/examples.md` "Four public datasets" with one route sentence; `tests/test_site.py` budget 700 and `TOTAL_BUDGET = 12045`; figures `kitchenham-pairs` and `kitchenham-participation` built from the page's blocks |
| D-2 | met | `examples/kitchenham/kitchenham.sysml`: one package, nine numbered sections, 52 `doc` blocks; strict load passes in `tests/test_wp76_kitchenham.py` |
| D-3 | met | `manifest.toml` (DOI, licence, size 7,877, md5, sha256, exclusions 4 of 145, retrieval URL), `run.py`, `variants.py`, `derived/projects.csv` (141 rows) with `LICENCE-DATA.txt`, `results.json` (package 0.1.0, SHA 76a63fd1, clean tree), `variants.json`; `docs/references.bib` `kitchenham2002empirical` with its `verified` field, cited in `notes/paper-prior-art-sources.md` |
| D-4 | met | `tests/data/wp76/kitchenham/verification-record.md` sections 0 to 8; `tests/test_wp76_kitchenham.py` (17 tests); register rows C1104 to C1120, all backed; the coverage row in `examples-coverage.md` |
| D-5 | met | `notes/directions/wp76-iron-triangle-conic.md` (one page, defines nothing); row 76 and two items in `notes/directions/README.md` |
| D-6 | met | `WP76-decisions.md` (the memo, the approval, the base move, four package defects); `WP76-rounds/capture.mjs`, eight captures and `captures.json`; the INDEX row (the first pass found it naming this report before the report existed; this report closes that) |

## Requirements

| ID | Verdict | Evidence |
|---|---|---|
| R-1 | met | `run.py --check`: "results.json reproduced from derived/projects.csv (provenance keys excluded)"; `variants.py` leaves `git diff --stat -- examples/kitchenham/` empty; the author's end-to-end run on a clean tree at 76a63fd1 with the cache deleted (`run.py --fetch`: fetch, verify, derive, fit) moved only the provenance; `tests/test_wp76_kitchenham.py` 17 passed; the slow figure test and the runnable-block test: 38 slow site and docs tests passed at ec8704fa (29 minutes), and the two reruns at the final head are recorded in the decisions file when they finish |
| R-2 | met | Participation: "all three are in the contending set" (C1109) and "All three sides bound the frontier; the trades are read from the associations, not the exponents" (C1118); the positive pair "+0.43" and the negative pairs "−0.71 ... −0.92" (C1110); the project-management reader named the three apart |
| R-3 | met | `variants.json` `headline`: six scaled rungs hold, no scaler fails, all five bands hold, 140 of 141 leave-one-out refits hold, all three extremes hold, type D alone of the subsets; the page states the negative half over "every scaled rule, every band and every project removed" and the positive half as "most readings, weakly or not in some", naming the band, project 16 and the two subsets; `test_page_states_the_headline_only_where_the_checks_hold` pins exactly those rows |
| R-4 | met | The page names the subsets with 50, 73 and 113 rows and their signs; project 16 (the one sign flip) and the largest project and worst overrun by what they do; the record's influence table lists 16 and 138 (the exponent move of 0.05); `test_page_reports_the_subsets_openly` |
| R-5 | met | Record section 7: the PMP reader's three answers verbatim (145 to 141 and the three quantities; the narrowed headline; cause, quality, generalisation, the dates and the exponents refused); a match on all three; the first attempt, which received the figures only through an extraction defect, is discarded and said so |
| R-6 | met | `tests/test_claims_register.py` 22 passed; no causal or general wording on the page; "3 + m" absent; the limitations say only "The table carries no quality measure, so the case says nothing about quality" |
| R-7 | met | The manifest's fields; `package_version` 0.1.0 equals `tradespace.__version__`; `git_sha` 40 characters, `git_dirty` false; `test_verify_fails_loudly` and `test_manifest_names_source_doi_licence_and_exclusions` pass; `test_cached_file_of_record_matches_manifest` passed on the fetched file |
| R-8 | met | Seven model tests pass, among them `test_every_constant_and_alternative_in_the_model_has_a_doc_rationale` (every valued attribute and named part opens with a `doc`) and the three that hold `run.py` and `variants.py` to the model's values; the page links the model |
| R-9 | met | `runs.primary.k2`: shares 1.00 and 0.00, mean slack 0.271 against 0.345, certified, the per-term report's refusal recorded; the page's two-term sentence; pinned by test |
| R-10 | met | Both figures through the loop (record sections 5 and 7: intent first, four cold reads, dispositions, shows and does not show); looked at by the reviewers and the author; the line under the panels says nine projects lie beyond the frames, which the reviewer recounted; `MAX_FIGURES = 12` in both places; no ternary, with the reason |
| R-11 | met, with G-1 noted | 699 of 700 words; vocabulary 0 new; `mkdocs build --strict` clean; eight captures, no sideways scroll, the scheme applied per capture, the one console error the GitHub release lookup; the residual check's strict exit is pre-existing repository drift (G-1), and the branch's one changed surface, the Examples index, holds the base's counts after the route sentence was reworded at the review; the checker's patterns run over the page directly find no metanarration (record section 7a) |
| R-12 | met | `ruff check .` clean; `ruff format --check .` clean; `uv lock --check` resolved; the fast suite 2,011 passed, 12 skipped, 2 xfailed (the reviewer's run, 5 min 18 s; the author's run at the previous head 2,009 passed); no attribution line in the files or the commit messages (the grep's only hit is the scope's own row quoting the command); every path in `git diff --name-only c0e210cc..HEAD` maps to a deliverable or a default |

## Definition of good enough

| Item | Verdict | Evidence |
|---|---|---|
| R-1 to R-12 on one commit, evidence per requirement in the record | met | the table above; the record's sections 2 to 7a |
| The project-management cold read's three answers match the page | met | record section 7 |
| The page looked at as rendered, captures in `WP76-rounds/` | met | eight captures, `captures.json`, the author's crops of the dark figures before and after the colour fix |
| Every package defect met on the way recorded with its evidence | met | `WP76-decisions.md`, four defects (the ternary's label re-checked; the report's guard; the `tau = inf` set carried; the type-D two-term shares of 0.00) |
| A message to him naming the branch, the page, the record and what waits on 0.1 | met at the hand-off | the chat message that follows this report |

## Outside the scope

- **Out-of-scope changes:** none. `.gitignore` (the data cache), `scripts/build_figures.py` and `tests/test_site.py` (the figure cap and budgets), `notes/paper-prior-art-sources.md` (the key's citation) are the scope's defaults.
- **Non-goals touched:** none. Nothing under `src/`; `pyproject.toml` and `uv.lock` unchanged; the three example pages, the paper and the user guide untouched; `dev` and `main` untouched; no pull request.

## Observations (not counted as failures)

- `scripts/prose_surfaces.py` scans `docs/*.md` and `docs/user-guide/*.md`, so no page under `docs/examples/` is a residual surface; the metanarration check over the example pages is by hand (a tool gap, a candidate for the next tidiness package).
- The page's link to the case model resolves on `main` only after the merge; the other example pages carry no comparable link.
- At 375 px the figures shrink below legibility, as the figure rule allows; the attributes block scrolls inside its box as on the other pages.
- The page omits project 138 (an exponent move of 0.05, in the record only); R-4's "what they do" is met for the sign flip and the extremes.
- `dev` moved on during execution (the rename, then f305f548); the merge base stays c0e210cc and the branch will need one more rebase at integration.
- The scope's R-12 grep matches its own text in the scope file; harmless.

## Open decisions (for the supervisor)

- **G-1.** `check_residuals.py --compare --strict` exits 1 on this branch as on `dev` (131 counts rose repository-wide against a baseline that predates the paper's and the history page's later edits); the branch adds no rise on any surface it changes. Options: accept as is (pre-existing drift, outside this package) / fix before acceptance (rebaseline the residuals on this branch) / follow-up work package (the rebaseline with the next tidiness package).
- **G-2.** The observations above, as one item: accept as is, or pick any to act on.

## Gap dispositions

Filled from his answers, quoted in `WP76-decisions.md`.

| Gap | Disposition | Reason or follow-up |
|---|---|---|
| G-1 | (his answer) | |
| G-2 | (his answer) | |

## Recommendation

Recommend acceptance with G-1 noted: every deliverable is in place and every requirement's check passed on the
reviewed head by a fresh-context reviewer, the headline is narrowed to exactly the rows the sensitivity checks
support, the project-management reader identified what was measured, what was found and what the evidence cannot
support, and the one open check (the residual baseline) fails for the repository as a whole, not for this branch.

Acceptance is the supervisor's act, recorded as named above. This report does not accept the work.

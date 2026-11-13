# WP37 review: the history page

Reviewer: a Sonnet agent that did not build the page. Run at head **d801a43** (`origin/dev`, worktree `wp37rev`),
2026-11-12. Staged page read only at http://127.0.0.1:8791/history.html; its text is byte-identical to
`history_record.build_page_file(site/history.html)` of this head (diff empty apart from a trailing newline). Nothing on
the page or the record was changed by this review.

## Requirements

| R-id | Verdict | Evidence |
|---|---|---|
| R-1 links resolve | met | `uv run python scripts/check_history_links.py` (no credentials): 87 URLs, 86 ok, 1 blocked (403, doi.org/10.1002/iis2.70203, Wiley bot challenge), 0 FAIL. The one blocked link is not on the page prose; the browser confirmation by a person is not done (not checkable by an agent) and stays listed |
| R-2 link matches claim (W3 re-run at final head) | not met | `w3-check.md` is dated at draft b0386e3 (26 URLs); the page has since been rewritten and the record holds 87. No W3 table for this head exists. The reader's walk lists link-to-claim doubts for the supervisor or the record (below) |
| R-3 sentence kinds, team's account marked | met | `trace.md` has 15 rows for 15 sentences; `pytest tests/test_site.py -k history` 21 passed, incl. `trace_table_is_current`, `team_account_sentences_are_marked`. Row 3 ("We perform ...") is team-account by firm first person, Marked "no" in the table; the sentence is not prefixed "in our own account" (it follows the marked sentence 2). Judgement for the supervisor |
| R-4 every work dated; every person has a work, link or marked account | met | 13 person entries in `history.yaml`, all 13 names on the page (Koch, Bernardineli, Mehta, Jodesty, Shorish, Paruch, Penland, Hackel, Lima, Clark, McOwen, Riascos-Álvarez, Barlin); Hackel and Riascos-Álvarez rest on the marked team-account sentence only, as the scope allows. Person table not written out here (see `history.yaml`, kind person) |
| R-5 vocabulary | met | `pytest tests/test_site.py -k history` 21 passed (`uses_no_cryptocurrency_or_web3_vocabulary`, `list_holds_no_banned_word_outside_link_titles`); `uv run python scripts/check_vocabulary.py`: 0 new violations, 63 known |
| R-6 word ceiling | met against the ceiling, aim missed | visible prose 418 words (own count, matches the test); test bound 250 to 420 (`one_screen`) passes; the scope's aim of 350 or fewer is not reached (418) |
| R-7 special-case rule | met | `trace.md` row 12 flag yes; sentence reads "Special cases where the work was highly public: a review ... Filecoin ... and the RAI controller"; no focus implied. Generated list marks 7 entries with the phrase beside them (rendered page) |
| R-8 structure and arc | not met in part | six parts in order present as paragraphs (purpose, arc, people, firm today, special cases, closing). Parts 2 and 3 are merged with the people into the same paragraphs, and part 5 (special cases) precedes part 4 (the firm today: NumFOCUS, OpenMBEE) in the page: the page order is purpose, 2014, cadCAD, GDS/people, team account, special cases, firm today. Arc runs 2007/2013 in the list and 2014 in the prose to 2026. The method itself is never named (reader's walk). Supervisor to rule whether the order and the missing bridge are accepted |
| R-9 no private material | met | `check_history_links.py` run with no token: every github.com link 200 (26 repository entries incl. the 13 profile pages), 0 FAIL |
| R-10 paper, docs, src, derivation, pyproject, uv.lock untouched | met | files touched by every commit that touches the page, record, scripts or WP37 rounds: `claims_register.toml`, `history.yaml`, `scripts/{assemble_site,check_history_links,history_record}.py`, `site/{history,index}.html`, `tests/test_site.py`, `work-packages/WP37*` only; none under paper/, docs/, src/, derivation/; `git status` clean at start |
| R-11 fresh reader | see section below | verdict PARTLY (reads as long-running lineage of the firm, not of the method) |
| R-12 rendered check | not met in part | `work-packages/WP37-review/` at 1280x800 and 390x844, light and dark: no console messages, no page error, no horizontal scroll (scrollWidth equals clientWidth in all four). The prose ends at y=736 so it fits one 1280x800 screen, but the page is 2732 px tall (390 wide: 5099) with the 87-entry list and the footer link "The method" at y=2687, so the footer link is not on the first screen as the requirement states. `WP37-rounds/draft-shots/` still holds the old draft's images, not replaced (kept; supervisor or PM to say delete). Touch targets: 89 of 91 links under 24 px tall at 1280 and 50 of 91 at 390 (inline text links; reader's finding confirmed) |
| R-13 root link once; assembler copies; assembled site serves it | met | `grep -c history.html site/index.html` = 1 (footer, line 168); `scripts/assemble_site.py` lines 173-175 write `history.html` via `history_record.build_page_file`; `uv run pytest -q tests/test_site.py` (full, incl. `test_assembled_site_carries_the_history_page`): 72 passed, 1 skipped (the local built-paper test skips without a build), 28 min |
| R-14 whole-repo lint, lock, encoding, no attribution | met | `uv run ruff check .` all passed; `ruff format --check .` 639 files formatted; `uv lock --check` resolved 178 packages; `tests/test_text_encoding.py` passed (23 passed with the claims register); CI's attribution regex over `git log` = 0 hits. Two files say "Generated by `history_record.py`" (a script provenance line in `scripts/history_record.py` and `trace.md`), not an AI attribution; left |
| R-15 record fields and schema at the top | met | `pytest -k history_record` passed (in the 21); `history.yaml` lines 1 to 33 give the schema; 87 entries: paper 17, repository 17, post 14, person 13, role 11, talk 9, video 6 |
| R-16 every link, name, year on the page ties to the record | met | `pytest -k history` passed: `every_link_on_the_page_is_a_record_entry`, `every_name_...`, `every_year_...`; all 29 prose links matched to an entry by my own join (none without an entry) |
| R-17 generated list chronological, year, link, people, special-case mark | met | `list_is_generated_from_the_record_oldest_first` passed; rendered list read: 70-odd entries oldest first from 2007 to 2026 with people and the italic phrase on 7 entries |
| R-18 trace current; claims register rows | met | `trace_table_is_current` and `every_prose_sentence_has_a_row_in_the_claims_register` passed; `tests/test_claims_register.py` passed |
| D-1 to D-10 | met except D-8 (this review, the supervisor's acceptance and `WP37-decisions.md` updating remain) | files present: `site/history.html`, `history.yaml`, scripts, tests, `WP37-rounds/` (w1 to w5, trace.md, open-items.md) |

## Checks (head d801a43)

| Check | Result |
|---|---|
| `uv run pytest -q tests/test_site.py -k "history and not assembled"` | 21 passed |
| `uv run pytest -q tests/test_text_encoding.py tests/test_claims_register.py` | 23 passed |
| `uv run python scripts/check_history_links.py` | 86 ok, 1 blocked (403), 0 FAIL |
| `uv run ruff check .`, `ruff format --check .`, `uv lock --check` | clean, 639 formatted, resolved |
| `uv run python scripts/check_vocabulary.py` | 0 new violations (63 known) |
| full `uv run pytest -q tests/test_site.py` (includes the docs-site assembly; slow) | 72 passed, 1 skipped |

## Rendered page: one-line readings (screenshots in `work-packages/WP37-review/`)

- `history-1280x800-light.png`: the whole prose, title to the italic tagline, fits the screen on a cream ground and the "Dated references" heading starts at the bottom edge; no footer link visible.
- `history-1280x800-dark.png`: the same layout on near-black, links pale blue, body text and the muted tagline legible.
- `history-390x844-light.png`: one column, the first screen holds the purpose and three paragraphs, text wraps cleanly, no sideways scroll.
- `history-390x844-dark.png`: the same on dark; contrast fine, links underlined and recognisable.
- `history-1280x800-light-full.png`: after the prose a 70-row dated list from 2007 to 2026, each with year, linked title and people, seven rows carrying the italic special-case phrase; "The method" footer link is the last line.
- `history-1280x800-dark-full.png`: the same on dark; the list reads equally well and the footer link is visible.
- `history-390x844-light-full.png`: a 5,100 px column; the list wraps to two or three lines per entry, no horizontal overflow.
- `history-390x844-dark-full.png`: the same on dark; no clipping.

## R-11, the fresh reader

The fresh reader (Sonnet, rendered page only), verbatim as returned to the PM; verdict PARTLY.

> the page says the firm is a contract research and engineering firm founded 2017 as BlockScience now the Dynamical Systems Group; the history it gives is pre-firm convex optimization and geometric programs for network protection (Preciado), cadCAD, GDS, the parameter-selection article, workshops, gds-core and gds-axelrod, a community-currency model, public cases (Filecoin review, RAI controller), NumFOCUS and OpenMBEE ties; the method itself (posynomial, hyperbolic trade space) is never described or placed in a lineage; a stranger learns the firm's history but not how it led to the method; the only bridge is "this project is part of a synthesis effort to make our learnings accessible". Lost the thread: the opening promises "the human lineage of this work" but the next paragraphs are about cadCAD, GDS, gds-core with no step to a posynomial frontier method; jump from "Before the firm" (2014) to cadCAD (2018) without a connecting idea; the "Special cases... highly public" sentence arrives without setup; the tagline "With computers, fast but with confidence." is unexplained; "The method" link at the bottom is the first place the method is named. Promotion or unsupported (quoted short): "long-running endeavour with many contributors"; "came not from an academic group but from a contract research" (flagged "In our own account"); "studying the spaces of feasible designs of their systems"; the tagline; "highly automated system" (RAI controller); "Special cases where the work was highly public" (the label appears seven times in the dated list including a YouTube walkthrough and a Zenodo calculator); "relevant work was done at the firm by people we thank but cannot describe here"; "in our own account of the team, its backgrounds are..."; "this project is part of a synthesis effort to make our learnings accessible" (claims lineage with no link). Links: "founded in 2017" links to michael.zargham.org (a personal homepage); "talk at a workshop in Edinburgh (ICMS), October 2024" links to the CV pdf (a self-report, not an event record), same for the RAI case-study workshop entry; "OpenMBEE" links to dynamicalsystemsgroup.com/partners (the firm's own page); "maintainer across" links to michael.zargham.org/research; "SciPy 2026" goes to a pretalx talk listing; "design record" (RAI) goes to Zenodo 10474385 titled "Summoning the Money God" in the list; "Generalized Dynamical Systems" goes to a page titled "Part I Foundations"; bare-year links "2014" and "2020 journal version" and generic "a post of the firm", "a video series" do not say where they land; two list entries share destinations with prose links under different names. List against prose: prose "Zargham's convex optimization (2014)" has no matching convex-optimization entry (the 2014 link goes to Accelerated Dual Descent); the community-currency model appears as a 2022 blog and a 2023 DOI paper (looks duplicate); GDS appears three times in 2022 with different author orderings; the dated list's AUTHORS.txt entry credits more people than the prose (Mace, Bernardineli, Lima, Clark); Hackel and Riascos-Alvarez "worked on client projects we cannot name" has no list entry; the "special case" label sits on entries that are not Filecoin or RAI. Layout: 1280 px fine; 390 px no horizontal scroll but 50 of 91 links render under 24 px tall; dark contrast fine; no theme toggle and no site navigation, the only exit is "The method" link.

**Intended reading** (scope, purpose, 2f26713): the work is the synthesis and publication of a long-running endeavour, not AI-generated out of the blue. **Match:** partly. The reader reads the lineage of the firm and its people, long-running and many-authored, which answers the "out of the blue" risk for the firm; the reader does not read the lineage of the method, because the method is not named or placed. The reviewer's own reading of the rendered page agrees with all quoted facts; the 50/91 and 89/91 touch-target counts are re-measured above.

### The PM's triage of the reader's findings

**Needs the supervisor's ruling** (content of the page; nothing changes on an agent's judgement):

1. The page never names the method nor bridges from the firm's history to it ("The method" is the first mention; the only bridge is the synthesis clause with no link). Options: leave (the purpose is people, not method); one clause naming the method and the lineage step; or cut the synthesis clause.
2. The tagline, default 6 (a): the walk says it is unexplained and it earns no place in the arc. Default 6 says to cut it if the walk says so; this is that case, the ruling is his.
3. "long-running endeavour with many contributors" and "synthesis effort to make our learnings accessible" as unlinked claims (the second is marked "in our own account").
4. The special-case label on 7 list entries (incl. a walkthrough video and a calculator, a Zenodo record titled with "Cryptocurrency") beyond the Filecoin review and RAI that the prose names; and the title "Summoning the Money God" visible in the list (a linked source's title, permitted by the scope).
5. The Edinburgh talk and the "founded in 2017" claim resting on self-published pages (CV, homepage): defaults 8 (a) and the owner's own account.
6. The gap in the prose arc between 2014 and cadCAD 2018 (one connecting idea or none).
7. Whether the page's order (special cases before the firm today) and the merged parts match the six-part structure (R-8), and whether the footer link belongs above the list (R-12: the footer link is at the end of an 87-entry page, not on the first screen).
8. Touch targets: 50 of 91 links under 24 px at 390 wide; whether the page meets a target-size rule or the site's register is accepted.
9. Hackel and Riascos-Álvarez have no list entry (the list shows only entries marked listed; people default to not listed).

**Record defects** (an agent may fix in a later unit; none touches the page's wording):

1. `w3-check.md` is not re-run at this head (R-2).
2. Duplicate or near-duplicate list rows: community-currency model as a 2022 blog and a 2023 paper; three GDS rows in 2022 with different author orderings; list entries sharing a destination under a different name from the prose link. The record's `note` fields should say they are distinct works, or entries merge.
3. The 2014 prose link "convex optimization" lands on "Accelerated Dual Descent for Network Flow Optimization" with no word in the page saying it is the convex-optimization work; the entry's `shows` should state it (the title is the source's).
4. The AUTHORS.txt list row credits more names than the prose; the row is the file's own listing (`shows` should say so).
5. `draft-shots/` still holds the old draft's images (R-12 says replace).
6. `blocked` link doi.org/10.1002/iis2.70203: person confirmation in a browser outstanding.
7. Bare-year and generic link labels ("2014", "a post of the firm", "a video series"): a page change, but the record can carry the landing title (it does, in the list).

## Supervisor review list

`work-packages/supervisor-review-list.md` carries the history page rows (prose, generator and tests, the entry surfaces `site/history.html` and the root footer link) with commits 10fb343, 45877ec, a5089b6, df0cad9; this review changes none of them. The nine defaults of `WP37-decisions.md` (1 Barlin role only; 2 "Bernardineli"; 3 "Penland"; 4 blog.block.science posts; 5 CarolinaRiascos; 6 keep the closing phrase unless the walk says otherwise; 7 Clark paper without the setting; 8 Edinburgh via the CV; 9 D-9) all stand as written on the page; the reader's walk bears on 6 (above), 7 and 8.

## Addendum: the closing unit (2026-11-13), R-2, R-8 and R-12 re-checked

The closing unit applied the assistant's calls under the supervisor's standing rulings (`WP37-decisions.md`, the triage
ruling of 11:50 and the Penland and Clark rulings of 13:20 and 13:30; the list is in `WP37-rounds/open-items.md`
section 8). Prose is 406 visible words (418 before; the test ceiling goes 420 to 406; the aim of 350 is not reached).

| R-id | Verdict | Evidence |
|---|---|---|
| R-2 link matches claim (W3 re-run at the final head) | met | `WP37-rounds/w3-check.md` is regenerated for this head: 29 links of the page's prose, 26 match, 3 partial with reasons (OpenMBEE and OpenSysML, one link each shows only part of the clause and the role is on the research page the clause links; Riascos-Álvarez, the handle is hers and the work is the marked team account), 0 `no`. Statuses from `uv run python scripts/check_history_links.py --page`: 27 external links, 27 ok. The new bridge clause was read against the geometric-programming tutorial's section 2 (a geometric program has posynomial objective and constraint functions). The record's 87 URLs: 86 ok, 1 blocked (doi.org/10.1002/iis2.70203), 0 FAIL; the blocked link was confirmed by the assistant in a browser to be the supervisor's INCOSE International Symposium 2026 article on Wiley Online Library. The record defects are fixed: `note` fields on the community-currency post and paper and on the three 2022 GDS rows, the AUTHORS.txt row's `shows`, the 2014 convex-optimization row's `shows`. |
| R-8 structure and arc | met, with two readings stated | The paragraphs run in the scope's order: purpose and the firm, the arc (before the firm, cadCAD, Generalized Dynamical Systems and the parameter selection article), the people's paragraph, the firm today (NumFOCUS, SciPy, PyData, OpenMBEE, OpenSysML), the special cases. Part 6 (the closing phrase) is cut by default 6 (a). The arc runs 2014 to 2026 as dated links (2013 is the 2014 paper's journal year), and the purpose is one sentence. Parts 2 and 3 stay interleaved: the people are named inside the arc paragraphs with their works, by the pointer register. `tests/test_site.py::test_history_page_follows_the_scope_order_and_the_closing_unit_rulings` pins the order. |
| R-12 rendered check | met | Screenshots at `work-packages/WP37-review/history-{1280x800,390x844}-{light,dark}.png`, built from this head's `history_record.build_page_file()` and opened in system Chrome (Playwright): no console message and no page error in any of the four, `scrollWidth` equals `clientWidth` in all four (1280 and 390). At 1280 by 800 the prose ends at y=754 and the back link "The method" is at y=18 to 34, on the first screen; at 390 by 844 the back link is at y=18 to 34 and the prose ends at y=1576. The footer link sits at y=2705 (1280) and y=5000 (390), the end of the 87-entry list; the top back link is what the first screen now carries. Readings: 1280 light, the bridge clause and the Penland and Clark sentences read as ruled, the last prose paragraph is the special cases and the dated list begins below the fold; 1280 dark, same text with the dark palette, links legible; 390 light and dark, the prose wraps in one column, the back link first, no overflow. The four `-full` images of the old head are deleted (git keeps them) as were `WP37-rounds/draft-shots/`. |

Checks run on the closing head: `uv run pytest -q tests/test_site.py -k "history and not network and not assembled"` 21 passed;
`tests/test_claims_register.py` and `tests/test_text_encoding.py` 23 passed; `scripts/check_history_links.py` as above;
`scripts/history_record.py --check` (trace current); `scripts/check_vocabulary.py` 0 new violations (63 known);
whole-repo `ruff check .` and `ruff format --check .` clean; `uv lock --check` resolved.

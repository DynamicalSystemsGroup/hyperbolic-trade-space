# WP33 review (journeys and signposting)

Screenshots for this record: commit `c680853`, `git show c680853:<path>` with `<path>` under `work-packages/WP33-review/`, `work-packages/WP33-review/docs/`.

Reviewer: not the builder. Review head: `d801a43` (worktree `wp33rev`, from origin/dev). Start head of the package: `60f92d9`.
Commands were run in that worktree; no content was changed. Screenshots are in `work-packages/WP33-review/`.

Which head each screenshot shows. The staged site at http://127.0.0.1:8791/ is built from the stage worktree at `ff9c410`, which
contains all four WP33 entry-surface units (`fbbaf2b`, `540843a`, `2114aad`, `7ef86dc`). Check: the staged root page is byte-identical
to `site/index.html` at `d801a43` (empty diff); `/docs/api/` is 404 and `/docs/user-guide/` is the one-line router; the staged paper
carries the Section 1 audience sentence. `ff9c410..d801a43` touches no page the first screens show (it changes the supporting
material's Appendix G.2, the reading-pass scripts, the ledger and a residual-review note), so the screenshots stand for `d801a43`.
The README is not served by the site and GitHub's rendering is not available: it was rendered locally from `README.md` with the
Python `markdown` package and a plain stylesheet (`scratchpad/wp33rev/readme.html`); fonts and chrome differ from GitHub's.

## Verdict table

| R | Verdict | Evidence |
|---|---|---|
| R-1 | met | `grep -c '^| [PU][1-8] ' docs/superpowers/notes/user-journeys.md` returns 12; each row has persona plus four fields (arrives, first need, path, content aimed at another user) and cites file and heading. |
| R-2 | met in substance; the letter ("no `words_added`") not met | `uv run pytest -q -m "not slow" tests/test_site.py tests/test_paper.py tests/test_claims_register.py tests/test_interface_contract.py tests/test_docs.py tests/test_text_encoding.py`: 365 passed, 4 skipped (built-paper and `PAPER_EXECUTE`/`PAPER_BUILD` tests, as expected). Counts, start `60f92d9` to `d801a43`, below. No touched surface is higher except the new one-line router (0 to 3 words) and the API page that received the merged `api.md`; every sum is negative. `TOTAL_BUDGET` 7472 to 7241; page budgets only fall (new: router 3, `api-reference.md` 287 in place of `api.md` 300). Paper ledger ceiling 11490 to 11100 overall; the WP33 rows alone: 5 cuts (11, 60, 9, 3, 39 = 122 words) and 2 `[[raise]]` rows (9, 37 = 46 words): the letter says paper cuts are `[[cut]]` rows with no `words_added`, and these two rows are `words_added` (a sentence moved between sections and the new audience sentence). Counted body words 10,269 to 10,193 (-76). |
| R-3 | partly met | Screenshots and first lines; see "First screens". Root: met (one whom sentence, five links, no directory listing, section or banner above the needs). Docs home: met at 1280, not at 390 (three of five need links fall below the fold). README: one whom sentence, but one link only ("docs"; "the paper" is plain text), and the layout list starts inside the first screen. Paper: first screen is the abstract (1280) or the contents list (390); the audience sentence is the top of Section 1, not on the first screen (the abstract is the supervisor's hand). API page: no whom-it-is-for sentence. Atop each hand-written docs page (15 files, router excluded): a sentence naming the reader on 4 (`index`, `getting-started`, `conditioning`, `examples`); not on `chart`, `choosing-k`, `fitting`, `limitations`, `overview`, `prediction`, `tensions`, `termination`, `api-reference`; `theory` and `further-reading` state purpose, not reader. |
| R-4 | met for coverage and job; audience per directory not stated | `ls -d */` in the worktree: `derivation docs examples paper scripts site src tests work-packages` (9); `git ls-files \| cut -d/ -f1 \| sort -u` adds only files and `.github`. All nine are in the README Layout list (src; docs; paper and site; scripts and tests; derivation; examples/adcs; work-packages); no stale entry ("docs/ — the docs site"). The list gives each directory's job; the audience is only the one first sentence ("analysts"), not per entry. |
| R-5 | not met | The Organization paragraph (rendered on the staged `/paper/`) reads "Appendices: A notation, ... G prior art. We assume multivariate calculus, linear algebra and convex optimization." It lists appendices; it does not route by depth (abstract and figure; headers and results; whole text; appendices; repository and container), and it is 9 words longer than at `60f92d9` (one sentence added). Routing by reader now sits in the new first sentence of Section 1 (37 words in, 39 cut, net -2), which is a different instrument. No L-A to L-F reader record exists in `WP33-wayfinding/`. |
| R-6 | met | The same pytest run (claims register, site, paper, contract, docs): green. `uv run python scripts/check_vocabulary.py`: "0 new violation(s), 63 known". `uv run ruff check .`: all checks passed; `uv run ruff format --check .`: 639 files formatted; `uv lock --check`: resolved. Links: every first-screen link of the root page resolves on the staged site (200), including `docs/examples/#requirements-read-after-the-fit` and `paper/supporting-material/#appendix-b` (both ids present). Docs and paper build: not rebuilt by me (rule: no stage run); the built paper tests were skipped; the staged site shows the built result. One backing weakness in the register: see finding F-4. |
| R-7 | met; the cited authority is missing | `uv run pytest tests/test_interface_contract.py` green; `git diff 60f92d9 HEAD -- work-packages/interface-contract.*`: `contract_version` 20 to 22, change-log rows 21 (one API page) and 22 (router page `docs/user-guide/index.md`), `docs.pages`, `presentation_pages`, `ownership` and `api_overview_page` follow the removals in the same commits (`7ef86dc`, `2114aad`). Both rows cite "`WP33-decisions.md`, D-2 items 5 and 6"; that file has no such section (see F-2). |
| R-8 | met | Root screenshots (all four): the "Decide what adopting it would change" door (now `docs/examples/#requirements-read-after-the-fit`, anchor present on the staged page) and the muted line with three lines of adoption cost: who writes the conditioning (link to the conditioning page), "31 s package-only install to a first fit, about 100 s counting reading and writing", few designs determine the exponents only weakly (link to limitations). Register rows C508 (100 s, backed by a cell return), C509, C510, C563 (31 s). C563's backing is weaker than the others: F-4. |
| R-9 | partly met | Baseline (`60f92d9`) and repeat (`df0cad9`) each have fresh Sonnet readers for P1 to P8 with steps, lost, skipped, skim, found, whom-told (`WP33-wayfinding/baseline/`, `repeat/`). U1 to U4: baseline from WP32 rounds; repeat only U1 (round 4, `WP32-cells/round-4/`); U2 to U4 are WP32's earlier returns, "unchanged". The twelve-row table per round in `WP33-wayfinding.md` does not exist (D-4). Baseline readers did two persona passes each and the repeat one persona per reader, so the step counts are indicative. |
| R-10 | met for P1 to P8 and U1; not checkable for U3 | `repeat/comparison.md`: steps 47 to 30; P1 5 to 4, P2 7 to 3, P3 6 to 4, P4 4 to 4, P5 7 to 4, P6 5 to 3, P7 6 to 4, P8 7 to 4; none rose. Bounce points closed or listed in the comparison. U1 (round 4, `df0cad9`) reached the planted answer with no stop the docs owe. U3 was not re-run after the fixes, so "U1 and U3 reach the own-table path without a page presuming SysML v2 or satellites" is checked for U1 only. The triage is not in `WP33-decisions.md` (the decisions of the repeat are in `driver-log.md` at `4bb1732`; F-2). |
| R-11 | partly met | Screenshots of the root page, the README (local render), docs Home, paper first screen, API, Examples and the history page, 28 images, both widths, light and dark; readings below. Console and network were recorded for each: no error on the root, README (local), paper or history pages; every docs page logs one 404 (identified as F-3). The installed package was not screenshotted: its first line is read from `help` text (F-5). No broken link on any first screen. |
| R-12 | met | The tier-1 commands above: all green (ruff check, ruff format --check, `uv lock --check`, 365 passed). `git log 60f92d9..HEAD --format=%B \| grep -ci -E 'co-authored\|generated by\|claude\|anthropic'` returns 0 (140 commits). Not run by me: the full suite (the gate's). |

### Word counts per surface (start `60f92d9` to `d801a43`)

Counter: the test's `prose_words` rule for docs pages (code blocks, tables, image alt text, HTML comments and mkdocstrings directives
excluded), the test's `_VisibleText` parser for the root page, `wc -w` for the README, the test's `words_by_section` for the paper.

| Surface | Before | After | Change |
|---|---|---|---|
| `site/index.html` (visible words; the review list's own figure for the first unit is 433 to 372) | 411 | 383 | -28 |
| `README.md` (`wc -w`) | 137 | 137 | 0 |
| `docs/index.md` | 236 | 206 | -30 |
| `docs/getting-started.md` | 358 | 348 | -10 |
| `docs/user-guide/overview.md` | 407 | 399 | -8 |
| `docs/user-guide/conditioning.md` | 611 | 610 | -1 |
| `docs/user-guide/choosing-k.md` | 702 | 573 | -129 |
| `docs/user-guide/limitations.md` | 499 | 475 | -24 |
| `docs/examples.md` (received the cubesat block) | 673 | 671 | -2 |
| `docs/further-reading.md` | 195 | 193 | -2 |
| `docs/api.md` + `docs/api-reference.md` (merged into the latter) | 298 + 37 | 287 | -48 |
| `docs/user-guide/index.md` (router, new) | 0 | 3 | +3 |
| Docs, all hand-written pages | 7,474 | 7,223 | -251 |
| Paper, counted body words (Section 1: 727 to 723; Prior art 625 to 565, which includes WP35's zero-net paragraph; Preliminaries 452 to 443; Results 2,814 to 2,811) | 10,269 | 10,193 | -76 |

Source changes (R-2 does not cover them): two docstring top-lines (`preconditioning.py`, `tensions.py`), no other file under `src/`;
`pyproject.toml`, `uv.lock`, `derivation/` unchanged since `60f92d9`.

## First screens

Images are PNG in `work-packages/WP33-review/<surface>/`, named `<surface>-<width>x<height>-<scheme>.png` (docs pages keep the earlier
names `home-1280-light.png` and so on; these were replaced by the new capture at the same names). The script is
`scratchpad/wp33rev/shots.py` (Playwright, system Chrome). Need-phrases are links that name a thing the reader wants to do.

| Surface | Image(s) | Reading (one line) | Need-phrases | Whom-it-is-for sentence |
|---|---|---|---|---|
| Root page | `root/root-1280x800-{light,dark}.png`, `root-390x844-{light,dark}.png` | Title, one subtitle, one sentence naming the paper and the documentation, five links, a muted adoption paragraph, then "Why"; all of it fits in 390 by 844 at the fold; light and dark identical in layout. | 5, each a link (docs getting started, docs overview, paper, appendix B, examples requirements block) | 1: "Choose the line that is yours: the documentation serves those who run the tool, the paper those who read it, check it or decide on it." |
| README (local render) | `readme/readme-1280x800-{light,dark}.png`, `readme-390x844-{light,dark}.png` | One sentence, two code blocks (install, first fit), then "Layout" whose list starts inside the first screen; "the paper" is not a link. | 0 as such; 1 link ("docs") | 1: "For analysts with a table of evaluated designs, to learn which metrics trade: the docs, the paper, `examples/adcs/` for a case study." |
| Docs Home | `docs/home-1280-{light,dark}.png`, `home-390-{light,dark}.png` | A whom sentence with two links, two explanatory paragraphs, then five need links and a pointer to the menu; at 1280 everything is above the fold, at 390 only the first need link and the start of the second are. | 5, each a link; all above the fold at 1280, two of five at 390 | 1: "For an analyst with a table of evaluated designs. The paper makes the argument for the method; the project page links it, these docs and the package." |
| Paper first screen | `paper/first-screen-1280x800-{light,dark}.png`, `first-screen-390x844-{light,dark}.png` | Title and abstract (1280); at 390 the title and an open contents list with the abstract below the fold; the dark theme works. | 0 | 0 on the screen; the sentence is the first of Section 1 ("This paper is for readers deciding whether to rely on a trade study, checking the mathematics, or placing the method among prior methods", with where each goes) |
| API | `api/api-reference-1280x800-{light,dark}.png`, `api-reference-390x844-{light,dark}.png` | A description of the page, then eight linked names with their jobs; reads as a reference, not a router. | 0 (names, not needs) | 0 |
| Examples | `docs/examples-1280-{light,dark}.png`, `examples-390-{light,dark}.png` | A reader line, then the case's numbers and three bullets; the contents list names the blocks; dense but one reader's. | 0 | 1: "For the reader who wants a worked case: ..." (does not say where the others go) |
| History (root page footer link, "History and acknowledgements") | `history/history-1280x800-{light,dark}.png`, `history-390x844-{light,dark}.png` | A wall of prose with many links about people and lineage; one screen of text, no routing; a link back to `./` exists in the page. | 0 | 0 in the reader sense; the opening sentence says what the page is |

Console and network per page (Chrome, light and dark): root, paper and history: none. Every docs page (home, API, Examples, and by the
same theme the Fitting page): one `404` on `https://api.github.com/repos/DynamicalSystemsGroup/hyperbolic-trade-space/releases/latest`
(see F-3). Installed package, read as `help` text (`uv run python`): the module docstring says "Package code arrives in later work
packages (see ``work-packages/README.md``)."; class and function top-lines are one line of purpose each and none points to the docs.

## Deliverables

| D | Delivered? | Where |
|---|---|---|
| D-1 | delivered | `docs/superpowers/notes/user-journeys.md` (12 rows, placements and cuts table, P8 requirements). |
| D-2 | delivered for the root page, `docs/index.md`, Section 1 of the paper (and the first-screen/abstract rule), `docs/examples.md`, the README layout, `docs/api-reference.md` (merged); partly for the rest: the tops of the API page and the `examples/adcs/` entry carry no reader sentence (R-3); the package surface carries only two docstring top-lines (Q2's "where the docs are" sentence is absent, the package docstring is stale: F-5) | commits `ebacd28`, `2b07609`, `a80a403`, `38b7f0e`, `50f2227`, `eae2d24`, `7ef86dc`, `2114aad`, `540843a`, `fbbaf2b`, `2298720`. |
| D-3 | not delivered as specified | `work-packages/WP33-decisions.md` holds only the scope gate and the approval (18 lines). The placements and cuts and their one-line reasons are in the journeys note ("candidates"), the ledger's `no_longer_did` rows, the commit messages and `driver-log.md` (`4bb1732`); no record states what was placed or cut and why, per unit (F-2). Ledger and budgets landed with their pushes. |
| D-4 | partly | There is no `WP33-wayfinding.md`; the folder `WP33-wayfinding/` holds `baseline/` (four reader files and a README), `repeat/` (`P1-P8.md`, README) and `comparison.md` (eight rows plus a U1 line). The twelve-row table per round is missing. |
| D-5 | this file, with 28 new screenshots (and the earlier images kept) | `WP33-review.md`, `WP33-review/`. `WP33-decisions.md` does not hold the acceptance, as expected before acceptance. |

## Findings

| # | Severity | Finding | Where | Owner |
|---|---|---|---|---|
| F-1 | high | The paper's first screen names no reader. The abstract is left untouched by decision, so the whom-it-is-for sentence sits at the top of Section 1; at 390 by 844 the first screen is the contents list and the abstract is below it. R-3 and R-5 ask for it on the first screen and for an Organization paragraph that routes by depth; neither holds, and the Organization paragraph grew by 9 words. | `paper/paper.ipynb` Section 1; `paper/length_ledger.toml` rows of 2026-11-12 | the supervisor (abstract is his hand); the assistant for the Organization paragraph |
| F-2 | high | D-3 and D-4 are not in their named files. `WP33-decisions.md` has no placement and cut record and no triage of the repeat; `WP33-wayfinding.md` does not exist; contract rows 21 and 22 cite "`WP33-decisions.md`, D-2 items 5 and 6", which is not there (the decision is in `driver-log.md` `4bb1732`, which also says the router needs "no amendment" while commit `2114aad` made it amendment 22). | `work-packages/WP33-decisions.md`, `work-packages/interface-contract.md` rows 21, 22 | PM (record) |
| F-3 | medium | The docs pages' console 404 is identified: Material for MkDocs's repository widget asks `api.github.com/.../releases/latest`, and the repository has no published release; the widget shows "0 0" for stars and forks. The root page's "Release notes" link goes to the same empty releases page. | every docs page; `site/index.html` footer; `mkdocs.yml` | assistant (release); it disappears with a first release or with the widget off |
| F-4 | medium | Register row C563 (the root page's "31 s") is backed by `pyproject.toml` and `README.md`, which do not contain the measurement; the figure lives in the row's note, with no script or log committed. C508 (about 100 s) is one cell's reading at an older head, kept narrowed. The two figures sit side by side ("took 31 s, or about 100 s counting the reading and writing") with different bases. | `claims_register.toml` C563, C508; `site/index.html` | PM (a committed measurement record, or the figure narrowed) |
| F-5 | medium | The package docstring is stale and routes nowhere: "Package code arrives in later work packages (see `work-packages/README.md`)". It is the first thing `help(hyperbolic_trade_space)` prints; Q2 was "one sentence where the docs are". `interface-contract.toml` lists it as a known gap closed by WP8b. | `src/hyperbolic_trade_space/__init__.py` | WP8b |
| F-6 | medium | Docs Home at 390 by 844: three of the five need links are below the fold, after two explanatory paragraphs; the README's layout list begins within the first screen and "the paper" is unlinked; the API page and nine of fifteen docs pages have no reader sentence on top. | `docs/index.md`, `README.md`, `docs/api-reference.md`, user-guide pages | PM (a cut or a reorder, net negative) |
| F-7 | low | R-2's letter: two `[[raise]]` rows (9 and 37 words) for WP33; each is paid in the same section by cuts (11, 39), the sums are negative. | `paper/length_ledger.toml` | PM (record, or the requirement worded to allow a moved sentence) |
| F-8 | low | The repeat readers took no screenshots (text extraction only), so layout findings from the repeat rest on text; and baseline and repeat readers were arranged differently (two passes each against one persona each). | `WP33-wayfinding/repeat/README.md` | none needed; noted for the acceptance |

## Open items (what remains open, and who owns it)

From the repeat comparison's open list and the units landed after the round. "Landed" means the commit is on the head; no fresh
reader has read the result, so "closed" below means a change is in, not that a reader found the path shorter.

| Item | State | Owner |
|---|---|---|
| The "Decide" door's target (P1, P8: landed mid-appendix D.17) | changed in `540843a` to the Examples "Requirements read after the fit" block, anchor present; no reader has followed the new route | PM (a reader at the next round); the adoption cost "not sized in effort" (P8) is unchanged |
| Thin PCA comparison on the Overview (P4) | `2114aad` points the sentence at the paper (Section and Appendix D.16); not re-read | PM |
| Getting started does not say evaluation stays outside the package (P3) | `2114aad` states the package never calls the model; not re-read | PM |
| Audience line on `/paper/` and on the supporting material (six of eight readers) | `fbbaf2b` put one sentence at the top of Section 1; the first screen of the paper and the supporting material's first screen still carry none (F-1) | the supervisor (abstract); PM (supporting material) |
| Link text "Appendix B, L4.14 to L4.24" does not say it leaves the article (P5) | not changed | PM |
| No door named for a systems engineer; the toy statement sits in C.8 and Appendix E (P7) | not changed | PM |
| "Loading..." placeholders and the wide Appendix E table | already on the review list and WP8b; the staged supporting material still shows "Loading" in 42 lines of its HTML | WP8b |
| The 404 console line on the Fitting page | identified (F-3) | assistant |
| `uv sync` installs every group (round-4 triage 2) | `540843a` adds the package-only line and the flag note to the README; the root page's 31 s is measured on it (F-4 on its backing) | PM |
| `select_temperature` pointer in the README snippet (round-4 triage 1) | landed in `540843a` | none |
| API page merge, contract versions 21 and 22 (`7ef86dc`, `2114aad`) | landed with change-log rows; cited authority missing (F-2); the typed `/docs/user-guide/` address answers with the one-line router (200 on the staged site) | PM (record) |
| Section 1 audience sentence (`fbbaf2b`) | in; paper counted -4 in Section 1; first-screen visibility is F-1 | the supervisor |
| U2 to U4 not repeated; U3 not checked against the fixed pages | open (R-10) | PM |
| The package surface (docstring, F-5) | open | WP8b |
| Definition of done: "no open item remains unresolved" | not met while F-1, F-2 and the rows above stand; acceptance is the supervisor's | the supervisor |

Everything else not named above is closed at this head.

## Addendum: the closing round (PM, after the assistant's return of the package)

Evidence for each finding of the review, at the dev head named in the commit that carries this addendum.

| Finding | Closed by | Evidence |
|---|---|---|
| F-1 / R-5: the paper's first screen names no reader; the Organization paragraph does not route by depth | eb08f27 (paragraph routes by depth: abstract and figure; headers and results; whole text; appendices; repository and container; net 17 words with the cut of the repeated PCA sentence), fbbaf2b (audience sentence atop Section 1), 79015eb (link text says it opens the supporting material); the abstract (the supervisor's hand) is unchanged and the finding is written into the review list's Entry surfaces section with F-1's words | assistant's render at 69362b5; ledger rows; tests/test_paper.py |
| F-2: D-3 and D-4 records missing; router contract authority | 36e0e9f: WP33-decisions.md holds the 12 placements and cuts, the repeat triage, the router decision (amendment 22 by the contract's pages rule) and the assistant's rulings verbatim; WP33-wayfinding.md holds the 12-row tables per round; contract rows 21 and 22 cite the record | files; tests/test_interface_contract.py |
| F-3: 404 on every docs page | not a project resource: the theme's repository widget asks api.github.com for releases of a private repository; WP8b checklist row (assistant's call) | WP35-review F-1 |
| F-4: C563 backing | 2dcfbd1: measure_install.py and measure.out committed under WP33-review/, C563 points at them | claims register test |
| F-5: package docstring | b943eba (one sentence on what the package is, one naming the docs site; contract known-gap row closed by amendment 23) | doctests 7 passed |
| F-6: docs Home at 390 px, README, API page | 15d00af: docs Home puts the five need links first (all above 506 px of 844); README links the paper; reader sentence on api-reference and theory; the router has its own title | docs build strict; tests/test_site.py |
| R-9 / R-10: U3 not re-run | WP32-cells/round-5: one fresh U3 cell at ff9c410 reached the planted answer with no stop the docs owe, install to first fit 30 s of first import after a 0.7 s sync; U2 and U4 stand as WP32's unchanged returns | round-5/triage.md |
| R-10 for P1, P8 (Decide door) and P3, P4 (PCA pointer, evaluation outside the package) | fixed (540843a, 2114aad), not yet re-read by a fresh reader: folded into the final reader round by the assistant's call | |
| P5 link text | 79015eb | |
| P7: no door for a systems engineer | not changed: the root page's doors are an entry surface for the supervisor's close read; listed in the Entry surfaces section | |

Still open and owned elsewhere: the "Loading..." placeholders and the wide tables at 390 px (WP8b), the package docstring is closed here, the repository widget 404 and the blob/main link check (WP8b checklist rows), the supervisor's reading of the five entry surfaces. Definition of done: no open item of WP33's own remains unresolved; the supervisor's acceptance is pending through the review list.

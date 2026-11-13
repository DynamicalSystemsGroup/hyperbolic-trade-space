# WP33 — Decisions

The supervisor's words are quoted verbatim where they bind; the assistant's calls are listed for his review.

## Scope gate (2026-11-11, 10:10; scope at 5c70a4b; the assistant)

Origin: the supervisor's words in `PM-BRIEF.md`, "One size fits none", with the no-bloat clause. OD1: routing may change
a pinned name only by a contract amendment, never by drift. OD2: no surface adds net words; every signposting unit is
net neutral or negative on the surface it touches. OD3: "the package itself" is the installed package's import
surface: the `hts` namespace, the public API's docstrings and the package docstring, the first thing a coder sees in a
REPL or an editor, which routes to the docs in one line. OD4: two wayfinding rounds at most, the second on the fixed
surfaces. OD5: WP32's U1 to U4 cells double as the wayfinding readers for those personas. The defaults approved as
one item. **Assistant, verbatim:** "WP33 approved with OD1 amendment only, OD2 no net words, OD3 the import surface,
OD4 two rounds, OD5 yes."

## Approval (2026-11-12; the assistant, scope at 03d95fd), open questions decided

**Assistant, verbatim:** "WP33 Q1: the three adoption-cost lines are backed by what the docs already ask of the user (who writes the conditioning: the analyst, pointing at the conditioning page) and by the time to a first fit measured by the U1 and U3 cells as a register row; 'designs needed' states only what the limits page says (small samples determine exponents weakly) with no invented number. Q2: docstring top-lines only, one sentence each where the docs are, the contract's docstring pins checked; pyproject untouched. Q3: removal or merge where the map shows a page serves no path, each as an amendment when it touches a pinned name, with the deletion stating what the page no longer did. Q4: the executive arrives at the root page; the paper's first screen stays the paper's."

## D-2 rulings, items 5 and 6 (2026-11-12; the assistant, as recorded in `driver-log.md` at 4bb1732)

The repeat round's two open items, ruled on after the round-2 comparison. **Assistant, verbatim:** "the api.md and
api-reference.md merge proceeds by interface-contract amendment (one page, the pinned names kept as anchors or the
contract's rows updated, contract_version bumped, the deletion stating what the page no longer did); the User guide nav
heading is fixed in mkdocs.yml's nav titles without renaming overview.md unless a title alone cannot do it" (item 5 and
item 6 respectively, landed in `7ef86dc`; contract version 21). Closing call on the typed address `/docs/user-guide/`,
**assistant, verbatim:** "add docs/user-guide/index.md as a one-line router ('Start here: Overview', the need-phrase
form) so the typed URL lands on a line instead of a listing, nav unchanged. no rename and no amendment".

The router and the contract. The driver-log entry says "no amendment". The unit (`2114aad`) applied the contract's own
rule instead: `docs.pages` and `presentation_pages` list every hand-written docs page, and a page added there is a
change to pinned names, so the unit recorded contract change-log row 22 and `contract_version` 22. Both stand on the
record: the call as given said no amendment; the contract's pages rule requires one, so version 22 is right and the
ruling's intent (no rename, nav unchanged, one line) is kept. Change-log rows 21 and 22 cite this section.

## D-3: placements and cuts landed, each with its one-line reason

Every unit is net neutral or negative in words on its surface; ledger rows and budgets landed with their pushes.

| Unit | Commit | Placed or cut | Reason (what the content no longer did) |
|---|---|---|---|
| Root page | `ebacd28` | Three artefact cards, the paragraph describing them, the install command and a template comment cut; five need-phrases and one whom-it-is-for sentence, one adoption line, a demonstrator clause added; 433 to 372 words | The cards routed by artefact, so a reader guessed which was theirs; the install command is on the page the first need links to |
| Docs Home | `2b07609` | Seven page-named bullets become five need links; the workflow paragraph cut; 236 to 206 | The paragraph restated the first one and no path opened it |
| Choosing K | `38b7f0e` | The cubesat block moves to Examples ("Choosing K on the case"); Examples cuts a Run-it paragraph, a ternary bullet, a limits explanation, two class names and a caption clause to pay; choosing-k 702 to 573, Examples 673 to 671 | All four package-user readers skipped the block in both rounds; it is the case reader's |
| Overview | `50f2227` | The configuration-not-attributes clause leaves the overview pipeline list; stated once in Getting started, Your own data; overview 407 to 399 | The cell readers never opened the overview and guessed the batch and sample columns |
| Getting started and tops | `eae2d24` | "What must hold" in three bullets on Your own data; whom-it-is-for lines atop Getting started and Conditioning; four Getting-started sentences and one Limitations sentence cut; 358 to 351 | The modeller assembled it from three pages; the cut sentences were usage tips or restated a caption |
| README | `a80a403` | Layout lists every top-level directory with its job and where each reader goes; two docstring top-lines say what the object is for | The list omitted four directories and routed no one |
| Paper rows | `d8d650e`, corrected by `2298720` | Section 2 -60 (DEA clauses Table 1 and Appendix G carry, a Lineage sentence), Section 3 -9, Section 6 -3, a stochastic-frontier line in Appendix G; the abstract restored word for word; the reader sentence ends Section 1's Organization paragraph | Placements 6 and 7 were already done (WP28 CR-36, CR-37); the Section 6 item repeated the certificate; the abstract is the supervisor's hand |
| API | `7ef86dc` | `docs/api.md` removed, its overview opens `docs/api-reference.md` (nav title API); contract 21 | It was a second navigation entry that only linked to the reference page |
| User guide heading | `7ef86dc` | Nav titles only: "User guide, page by page" and "User guide: start here"; `overview.md` not renamed | The heading read as a link to a page, and led to a listing |
| PCA and evaluation | `2114aad` | Overview points to the paper for the PCA comparison; Getting started says the package never calls the model; the router page added; contract 22; getting-started 351 to 348 | P3 and P4 bounced where the docs did not say evaluation stays outside or where PCA is compared |
| Paper first screen | `fbbaf2b` | One sentence at the top of Section 1 names three readers and their doors; a sentence restating the abstract and Main results item 5 cut (37 in, 39 out) | Six of eight repeat readers found no reader sentence on `/paper/` |
| Root page, second | `540843a` | The adoption door opens the Examples requirements block; the install figure is the measured package-only 31 s; the README gains the package-only install line and a `select_temperature` pointer, net 0 words | The "Decide" door landed mid-appendix (P1, P8); `uv sync` installs every group (U1) |

Not placed: placements 6 and 7 of the journeys note (already done at the stage head); the root second-figure caption
sentence was reworded in `ebacd28` rather than moved.

## D-3: triage of the repeat round (stage head df0cad9; `WP33-wayfinding/repeat/comparison.md`)

No persona's steps rose; total 47 to 30 (P1 to P8). Each baseline bounce point:

| Bounce point | Disposition |
|---|---|
| The guessed `/docs/user-guide/` URL (P2, P4) | Closed: nav reached; the typed address now lands on the router (`2114aad`) |
| No audience sentence on the root, docs Home, Getting started | Closed (`ebacd28`, `2b07609`, `eae2d24`) |
| "The case page" for what the case leaves out (P7) | Closed: P7 reached C.8 from the contents list; the cubesat block and clause on the Home page place the demonstrator |
| The "Decide" door lands on D.17 (P1, P8) | Fixed since: it opens the Examples requirements block (`540843a`) |
| Thin PCA comparison on Overview (P4) | Fixed since: the Overview points to the paper (`2114aad`) |
| Getting started silent on evaluation staying outside (P3) | Fixed since (`2114aad`) |
| No reader sentence on `/paper/` | Fixed since in Section 1 (`fbbaf2b`); the first screen and the supporting material remain listed (supervisor: abstract; PM: supporting material) |
| "Appendix B, L4.14 to L4.24" link text (P5) | Listed |
| No door for a systems engineer (P7) | Listed: the toy statement is in C.8 and Appendix E |
| "Loading..." placeholders, wide Appendix E table | Listed (supervisor review list; WP8b) |
| The 404 console line on the Fitting page | Identified in the review as the repository widget's call to `releases/latest` (no published release); listed |

U1 (round 4) completed to the planted answer with no stop the docs owe (`WP32-cells/round-4/triage.md`); U3 was not
re-run. The two tables are in `WP33-wayfinding.md` (D-4).

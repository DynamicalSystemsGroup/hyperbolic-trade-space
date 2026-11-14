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

## The supervisor on the root page's needs block (2026-11-14, 09:15; his close read of the entry surfaces)

**Supervisor, verbatim** (with a screenshot of the block "Choose the line that is yours ..." with its five doors and the
adoption line): "this essentially call to action. goes last in the index not first"

**Applied as:** the needs block (the "Choose the line that is yours" sentence, the five doors and the adoption line)
moves to the end of the root page, after the Why, What and How sections; the whom sentence stays at the top. The test
that pins the order (`tests/test_site.py`, whom before needs before why before what) changes to the new order; the
journeys note's placement row says the block closes the page as the call to action. Listed under Entry surfaces with
its commit for his close read.

## The supervisor on the root page's one-sentence summary (2026-11-14, 09:25)

**Supervisor, verbatim:** "'An unsupervised learning method which applies a posynomial invariant form, a sum of terms
each a product of powers of the metrics, to learn the shape of a trade space from evaluated designs.' this is not a
subtitle, its plain laguage summary. it goes before the 'why'"

**Applied as:** the sentence leaves the header's subtitle slot and becomes a plain paragraph placed immediately before
the Why section (after the whom sentence), styled as body text; the header keeps the title and the byline. Folded
into the root-page unit with the needs block's move; listed under Entry surfaces.

## The supervisor on thinning the call to action (2026-11-14, 09:30)

**Supervisor, verbatim:** "i also think you can thin out the call to action down to reader the paper or use the tool."

**Applied as:** the closing block keeps its lead sentence (the documentation serves those who run the tool, the paper
those who read it, check it or decide on it) and two doors, "Read the paper" and "Use the tool"; the other three doors
and the adoption line go, each removal stating what the block no longer did (the Check-the-mathematics door: Appendix
B is one click inside the paper; the Decide door: the decision is now narrated in the paper's Section 9 and the
Examples page's requirements block stays reachable from the docs; the Bring-your-own-model door: the docs' Getting
started carries it; the adoption line: its measured figure stays on the README and in register row C563, re-pointed).
The journeys note's placements for P1, P7 and P8 are updated to the two doors. Folded into the root-page unit; listed
under Entry surfaces.

## The root page's Why: the descriptive and the normative kept apart (2026-11-15, 00:20)

**Supervisor, verbatim:** "one thing i want to get into the \"why\" is that we're trying to make a scientific assessment of what is possible and what
trades against what while deferring on the normative judgement of what is preferable. this aims to strike a cleaner or at
least reproducible and auditable distinction between what options are on the table and which options are preferable. this
is critical for any system with multiple stakeholders, and this makes the nature of how competing objects actually compete
explicit, it offers a concrete approach to deciding both whether to search for new options, and to deliberate in a
scientific grounded way about the options currently available. i don't want you to add a lot of prose to the index but we
wrote this before we introduced the 2 stakeholders with partially competing top level directions in the paper. my personal
motivation intersects with questions of governance, politics and accountability, with a desire to improve epistemics while
preserving the real contentions that arise naturally. an extra bit of context for me is that i plan to use this research
project for my ostrom workshop visiting researcher application / nomination so we need to hit a note where the
applicability to collective governance is is easy to see but without reframing the project around it. we already know
infrastructure is political, its part of the reason we have decision analysis and engineering requirements mapped back to
stakeholder needs in the first place."

**Applied as:** a light-touch addition to the root page's Why, his surface, drafted for his red pen and not applied
before his word: the method makes a scientific assessment of what is possible and what trades against what, and defers
the normative judgement of what is preferable; the distinction between the options on the table and the options
preferred is reproducible and auditable; with several stakeholders this makes explicit how competing objectives
compete, and gives a concrete footing for two decisions, whether to search for new options and how to deliberate over
the ones in hand. Two or three sentences, no reframing; the paper's two stakeholders are the instance. The context he
gives (governance, politics, accountability; epistemics with the real contentions preserved; the Ostrom Workshop
application) is recorded as his intent and not written onto the page.

**Supervisor, verbatim (00:30), on the same:** "so the why comes in to levels. there is a deeper motivation why, then the more
technical why is about getting computers to help us solve these problems in scalable, reproducible and interpretable ways"

**Applied as:** the Why section is drafted as two short paragraphs for his red pen: the deeper motivation first (what is
possible and what trades against what, assessed; what is preferable, deferred to the accountable people; the line
between options on the table and options preferred made reproducible and auditable; competing objectives made
explicit; the footing for searching and for deliberating), then the technical why (trade studies decided from documents
and tables, alternatives bespoke or opaque; computers that help in scalable, reproducible and interpretable ways, the
abstract's three words; the three conditions a decision-maker needs before trusting a model-based method). Not applied
before his word.

**Supervisor, verbatim (00:40), on the same:** "we can remove the why and what headers. i think we get three sections after
this revision. we could recast our previous why as a what, and our previous what as a how. with our recently conversation
about motivation becoming a why. noting that why, what, how is a heuristic for making a depth of detail walk natural for a
human reader. we could include the headers if it helps or drop them. whichever allows the page to do its job effectively"

**Applied as (discussion, not yet a build):** the root page's body becomes three sections in depth order: Why (the
motivation of 00:20, the line between what is possible and what is preferable), What (the former Why: trade studies
from documents and tables, alternatives bespoke or opaque, computers helping in scalable, reproducible and
interpretable ways, the three conditions for trust), How (the former What: PCA explains variance, this explains
tensions; the n-lemma; the figure). Headers kept or dropped by what lets the page do its job, to be settled by a cold
read of both renderings rather than by argument. Nothing applied before his word.

**Supervisor, verbatim (00:45):** "i am good with dropping the headers. i want you to draft the updated index page based on
this discussion and then show it to me for a close read and feedback before we merge it into dev"

**Applied as:** the root page redrafted on a branch (`rootpage`) by the driver: three sections without headers (why,
what, how), the summary and the two doors kept, the figure under the how; built and shown rendered in the browser pane
for his close read; merged into `dev` only on his word, with the page's structure test and the claims row updated in
the same commit.


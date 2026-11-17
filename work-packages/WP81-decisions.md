# WP81 — Decisions: the 0.2 documentation improvement, package 1 (the paper as a working paper)

## The programme and its record (2026-11-17)

This session is the v0.2 content session; the other open session releases v0.1 (his words, verbatim: "basically i have
2 sessions open. one focused on releasing v0.1 and one working on v0.2 content"). His direction for 0.2, verbatim:
"i also want to clean up the references to the paper which is currently a working paper. only the abstract is
published as a webpage but the full content can be built from the repo. per our recent changes the paper gets its own
development path. my overall take is that the documentation site needs work but our goal is not to disrupt the 0.1
release, instead to extend the scope of the 0.2 release to be documentation improvements". On the docs home's
first-fit figure: "here is another place: we upgraded these plots to have several level sets marked so it doesn't
look like a fit line". On WP76: "the iron triangle addition is part of the documentation improvement". On the home
and Getting started: "home and getting started have a lot of redundancy. that might be fine but i need you to assess
whether its distracting or productive. my intuition is that even if the same example is used. home as quickstart
which is direct and to the point, and getting started has a bit more explanation. also do not forget my injunction
against metanarration."

## The breakdown (`work-breakdown`; his OK 2026-11-17, verbatim: "OK the list")

Grounded in his words above and a fresh read of every page of the built site (the reader's ranked findings are in
`WP81-rounds/site-read-2026-11-17.md`). In order, each the largest step he can still judge quickly:

0. WP76, done: the iron-triangle example page, model, record and note.
1. The paper as a working paper: every pointer into the paper on the docs, README and root page reworded for a paper
   whose abstract alone is published and whose full text builds from the repository; the rule for `paper:` links in
   abstract mode decided once. Fixes how every later page may cite the paper. (This package, WP81.)
2. Level sets on every log-plane figure: the plotting default and the four single-line figures (the home and Getting
   started's shared first-fit figure, chart, fitting) through the figure loop; the paper's uses listed for the paper
   branch. Fixes the figure idiom before any page is redrawn.
3. Home as the quickstart, Getting started as the explained walk: the same example; Home keeps the pitch line, the
   router, the block and the figure with a one-clause caption; Getting started keeps the explanation and its figure
   carries the level sets and the band; no metanarration; the PCA contrast up front. Fixes the entry.
4. The reader's path: the Examples hub and the home lead with the measured-data pages and link all four; the cubesat
   case on its own page; maintainer content (code owners, the site-figure build block) off the reader path; the
   journeys note's placements. Fixes the navigation later pages land in.
5. Vocabulary at first use and the numbers that disagree: glossary links at first use on the guide pages, one worked
   reading of a report's output, the reader's five suspect numbers checked and fixed, the conditioning dependence
   said early. Fixes the guide's wording before new content cites it.
6. More measured-data examples, one package per case on the template: the synthetic three-metric explication page,
   battery ageing, TAWOS sprints; the size-against-shape plot and the dependence screen as reusable tools.
7. Hygiene: the residual baseline re-set, the example pages made residual surfaces, the post-0.1 list.

The list is a plan, revisited at each acceptance; only package 1 is firm.

## The 0.2 line (his answer 2026-11-17, verbatim: "A v0.2 integration branch")

Asked where the 0.2 work lives while 0.1 waits on `dev` (one branch per package, or an integration branch). Decided:
branch `v0.2`, cut from the head of WP76's branch (`claude/iron-triangle-example-12a7c6`, so it carries WP76), takes
each later package as it is accepted and is tested together; merged into `dev` after 0.1 is out, after one rebase and
his review. This worktree works on `v0.2` from here. Nothing on `dev` or `main`; no pull request. The v0.1 session is
told.

## Scope gate

`WP81-scope-of-work.md` is drafted; his answers are recorded below as they come.

### OD1 (2026-11-17, his answer in the popup, as typed by the agent)

Asked for the rule for `paper:` links while the paper is in abstract mode (every link lands on the abstract page with
no anchor). Options: keep every link in a sentence naming the working paper and its target; remove the links until a
pin is served, each pointer becoming the docs' own statement, with one naming sentence on the home and one in
Further reading; keep a link only where a named result is cited. His answer, verbatim: "Remove until a pin". Folded
into the scope (G2, D-1, D-2, R-1, R-2, the defaults).

### The review method (2026-11-17, his answer to OD2, verbatim; a standing direction for every 0.2 documentation package)

"since you are reviewing docs i would like to remind you that we need to do visual reviews so make sure you are doing
screenshots and tracing user journeys with different personas. and organize your findings and explore potentially
competing preferences before instituting changes"

Folded into the scope as R-8 (the journeys of `notes/user-journeys.md` traced per persona through every page that
points at the paper, screenshots per step, findings per persona and pointer, competing preferences written out with
the choice before any edit, the journeys re-traced after) and as the order of work in the defaults; it binds packages
2 to 7 of the breakdown the same way. OD2 itself went back to him with this folded in.

### OD2 (2026-11-17, his answer in the popup, as typed by the agent)

Asked again with R-8 folded in: approve the defaults list, or change items. His answer, verbatim: "Approve the list".

## WP81 approved (2026-11-17, his answer in the popup, as typed by the agent)

Asked whether he approves `WP81-scope-of-work.md` at d1aeba17 for execution on `v0.2`. His answer, verbatim:
"Approved". Execution begins under `work-execution` in the scope's order of work: the inventory, the persona journeys
traced with screenshots, the findings and competing preferences recorded, the dispositions, then the edits.

## His direction on the two jobs (2026-11-17, verbatim; a standing direction for every 0.2 documentation package)

"i also want you to remember to use the working paper as a context source for the documentation site work. the
documentation site and the paper do different jobs. so there may be things we want to pull from the paper so they can
be explained in brief or used to clarify a concept or mechanism for a user. however we may also need to remove
materials from the documentation site if they are actually drifting into the papers role. this will help us keep the
doc site tight and easily navigated: supporting a user not a researcher"

Folded into WP81: a replaced pointer's statement is drawn from the working paper's text, in brief, for a user; a
pointer whose content is the paper's job (a proof, an appendix, the prior-art argument, the search programme) is
removed rather than restated; the journey readers are asked, per page, what is the paper's job and not the docs'.
The dispositions of `notes/paper-references.md` take three values: brief from the paper; removed as the paper's role;
names the working paper.

## A default departed from, for his acceptance (2026-11-17)

The Agent's defaults say "the docsite total stays". The two naming sentences his rule requires (the home, Further
reading) cost 34 words net after every paper pointer's removal and the trims on the same pages (the home's caption
clause "Getting started walks through the output", a sentence about another page; the bridge bullet's "the
conjecture it is"); paying the rest would cut content that is not this package's (the bibliography's entries, the
theory page's definitions). `TOTAL_BUDGET` in `tests/test_site.py` rises by 34 with the reason; put to him as a gap at
the acceptance gate.

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

## His direction on lemma scripts (2026-11-17, verbatim)

"we don't need to address lemma scripts at all in documentation. that's something reserved for the paper"

Context: the re-trace had the optimization reader (P5) and the modeller (P3) asking the theory page to say where the
lemma scripts are, and the temperature and limitations pages named them; the second cold read found "lemma scripts"
undefined on the theory page. His word decides the competing preference: the docs do not address the lemma scripts;
the theory page's lead reads "definitions only, no proofs"; the temperature page states its two limits in words with
no lemma named ("the derivation does not bound the remainder"); the limitations page loses the three sentences on
the lemma scripts and theorem provers (the register rows C390, C567 and C568 retired, their ids never reused); the
Further reading sentence and the root page's body sentence no longer name `derivation/`. The README's repository map
keeps its `derivation/` line (a map of folders, not documentation of the method).

## The page's name (2026-11-17, verbatim)

On the iron-triangle page's navigation title "Software projects (Kitchenham-CSC)": "iron triangle example name with
a parenthetical in the docs is awkward pick a name that is accurate like you did with others and just stick with it".
Done in WP81's first unit as "Kitchenham software projects" (the navigation title and the page's heading), named like
"Broadbalk wheat"; outside WP81's scope, on his word, recorded here.

## The word budget (2026-11-17)

The Agent's defaults say the docsite total stays. After the removals of this package and the two naming sentences, the
touched pages net 19 words fewer than before WP81 (the home 289 of 350, Further reading 228 of 300; the total 12030
against the cap of 12055), so the default holds and `TOTAL_BUDGET` is unchanged at 12055. An earlier state of this
section recorded a rise; it is superseded.

## Acceptance (2026-11-17)

Asked whether he accepts WP81, delivered on `v0.2` at 774ff89b with `WP81-review.md` recommending acceptance (every
paper link out of the docs, each pointer the docs' own statement or gone, the working paper named on the home, in
Further reading, on the root page and in the README, the lemma scripts named nowhere in the docs, the fast suite
2,012 passed at the content head 2703c0f9, the twelve journeys re-traced with captures). His answer, verbatim:

> Accepted

The package merges into `dev` with the rest of `v0.2` after 0.1 is out, in the documentation pull request.

## The documentation pull request's shape (2026-11-17, evening)

Asked how the documentation pull request into `dev` opens after 0.1 (one pull request for the whole `v0.2` branch; one
per accepted package; decide when 0.1 is out). His answer, verbatim:

> One pull request for v0.2

The branch merges into `dev` as one change, "the 0.2 documentation improvement", closing one issue in the scope-of-work
template; the governance update (WP82, branch `governance-bypass-removal`) is its own pull request, apart from it, per
his release line. Both open once `dev` is in `main` for 0.1; a code owner who is not the author merges each. The
readiness note with the issue and pull request drafts is in the sessions' shared notes folder
(`0.2-pull-requests-readiness.md`); the trial merge into `dev` 7973fbd1 found two conflicts (index rows; WP76's register
ids `C1104` to `C1120` against `dev`'s `C1104`, to be renumbered at the rebase) and a green fast suite once resolved.

## The rebase onto `dev` after 0.1 (2026-11-17, evening)

0.1 was merged into `main` by him (74e62fda, 19:25 EST). `v0.2` was rebased onto `dev` 0dc2f4d2 (33 commits of
`dev` since the base c0e210cc, the branch's 31 replayed; the backup ref `v0.2-pre-rebase` at e49a8cd4 local only).
The two conflict kinds the trial merge found: `work-packages/INDEX.md` rows (resolved by row order, six times) and
WP76's register rows against `dev`'s `C1104`, the root page's closing sentence. `dev`'s `C1104` row stands whole;
WP76's seventeen rows are `C1105` to `C1121` (one id up each), and `WP76-review.md` names the new ids; no other file
on either side referred to them. `README.md`, `mkdocs.yml`, `site/index.html` and `tests/test_site.py` merged without
conflict and were read against `dev`'s versions: the `User guide` section title, the public-link hook and the
closing sentence from `dev` stand with the Kitchenham page, the budgets and the working-paper sentence from this branch.
The fast suite at the rebased tree: 2,045 passed, 12 skipped, 2 xfailed. The scope issue for the documentation pull
request is DynamicalSystemsGroup/tradespace#13 (opened by him with the `draft` label; it names WP76, WP81 and the
README update); the pull request says `closes #13`.

## The README and the install text (2026-11-17, late evening): unit 4, after acceptance, on his word

His words tonight, relayed verbatim by the driver session:

> one thing i noticed is the readme appears to be badly out of date. we need to get a readme update into the 0.2
> merge candidate. since i was able to merge v0.1, i do need to get to the 0.2 PR so danilo can review that.

> PR into dev for the documentation and readme updates

> its also worth noting that the documentation update can now account for this package being live on pip which can
> verify once the release lands

**Applied as** unit 4 of this package, on `v0.2` after the rebase. `README.md` reflects the released state: the
one-line description of `pyproject.toml`, the install from PyPI first (`pip install tradespace`, `uv add tradespace`)
with the clone-and-sync form for work on the package, the first fit of the getting-started page (the same code, the
same output, reproduced on the branch), the links a reader needs (the docs, the project page, the working paper as
this package names it, `CONTRIBUTING.md`, `GOVERNANCE.md`, the code owners' page, the code of conduct, the security
policy, the changelog, `CITATION.cff`), the four public datasets and the cubesat case, and the layout read line by
line against the tree. The layout keeps the folders a user opens and drops the rest: the register, the glossary and
history files, `CLAUDE.md`, the build and environment files, the license and the dot-files, which a user does not open
and the earlier list described one by one; the changelog and the governance file moved into the Contributing
paragraph. On the docs, the one install block (`docs/getting-started.md`) leads with PyPI and keeps the clone for work
on the package, within the page's budget of 348 words. His acceptance is given in the driver session when it shows him
the rendered README; the review is in `WP81-review.md` ("Unit 4"); the captures are `WP81-rounds/readme/`.


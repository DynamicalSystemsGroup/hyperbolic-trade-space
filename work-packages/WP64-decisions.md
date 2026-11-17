# WP64 — Decisions: the paper's lifecycle, apart from the software's

## His direction (12:30 EST, 2026-11-16, verbatim)

First, thinking it through: "i am considering a move where we break the paper release from the software and
documentation release. that would mean listing the paper as forthcoming on the index. i am considering this split
because i feel like the code and documentation is already useful and holding its release for a potentially long and
iterative refinement process on a large paper feels like bad form."

Then the decision: "let's give the paper a simple life cycle mode. its forthcoming and we only provide the abstract.
then its a working paper, while i am iterating on it. if/when a rachet it down for a publication we'll pin it to align
with a submission, and pin it again to deal with peer-review type revisions. the point is the paper should get a paper
lifecycle and the package should get an open source software lifecycle. at release of the software i think the
abstract is sufficient and the abstract is approved"

The driver's reading: the paper's lifecycle has four modes, forthcoming (the abstract only), working paper (the whole
paper, iterated), submitted (pinned to a submission) and revision (pinned again); the software and the docs follow an
open-source release lifecycle of their own; 0.1 of the software ships with the paper in forthcoming mode. The abstract
approved is the one in `paper/paper.ipynb`'s front matter at cdd597f5.

## His clarification (12:32 EST, verbatim)

"keep in mind the repo is open source so if someone pulls the repo they can still build the paper. we don't need to its
forthcoming we can just say we're iterating towards a paper release"

## WP64 approved as proxy (12:32 EST)

`WP64-scope-of-work.md` (one declared mode read by the site assembly; the abstract page at `/paper/` in `abstract`
mode with the approved abstract read from the notebook, the iteration line and the build command; the root card per
mode; the docs' `paper:` citations landing on the abstract page; the release checklist split into the software's and
the paper's; the mode set to `abstract` for 0.1) is approved by the driver under his mandate on the direction above.
One unit on branch `wp64`; the driver soft-confirms on captures and lands it on `dev` for his read.

## His direction, widened (12:34 EST, verbatim)

"i want you to build to seperate release control models. one for the paper which is triggered event driven and
probably builds from its own branch. and the flow for the documentation and pypi release which we gate around merging
to main. i expect this to be a significant reconfiguration so i propose you spiking to research the refactor, then
design, then implement, the test, integrate, test again. you get the idea"

The driver's calls: the unit dispatched on the first WP64 scope (a mode file, the abstract page, the checklist split)
is stopped before any delivery, since those are design choices the spike makes; its worktree is reset. WP64 becomes
stage 1 of the six-stage lifecycle, the research spike, with its own readout; the design (stage 2) is scoped from the
readout and goes to him with the decisions that are his; build, quality control, integrate and the cascade review
follow as their own packages. The abstract's approval and the four modes stand as recorded above and are inputs to
the spike.

## WP64 re-scoped and approved as proxy (12:34 EST)

`WP64-scope-of-work.md` is now the research spike: a map of today's release machinery, the constraints that couple the
paper to the software, the two candidate control models with the events, branches, gates and artefacts of each, the
decisions that are his, and the package sequence for the stages after it. No change to the repository's machinery in
this package. Approved by the driver under his mandate on the direction above.

## WP64 spike delivered and accepted as proxy (12:44 EST)

`WP64-rounds/readout.md` and `machinery.toml` landed at 86a3841e. The driver verified the live claims with `gh api`:
the repository is public; `main` is e7fd1165, 2,018 commits behind `dev`, holding only `test.yml`, so `pages.yml` and
`release.yml` have never run; no rulesets, no branch protection, no environments, Pages unconfigured, no releases or
tags. 23 couplings, five of which must be cut or bridged for either side to release alone (the docs' keys resolved
from the notebooks; the paper's tests in the software gate; the strict paper build before the Pages deploy; one Pages
artefact; one version and tag space). Three paper designs (pointer branch; the paper owns its branch; tags only), two
site compositions, three software designs. R-1 to R-5 met. His six questions go to him one at a time from here; the
design stage WP65 is scoped from his answers.

## His answers to the spike's questions (popups, one at a time; verbatim)

**Q1, where the paper's sources live (15:14 EST):** "i think that once i have a stable release the paper can cite
whichever release was active when that paper version was shipped. for now i don't have a stable release. i think going
forward we may want paper and dev to be two different branches. that said, you can reference dev for now since my goal
is to get dev merged into main for an 0.1 release as soon is as reasonable"

The driver's reading: now, the paper builds from `dev` (its sources stay there) and nothing waits on a paper branch;
the design keeps the step to a separate `paper` branch open for after a stable release, where each paper version pins
the software release that was current when it shipped. The priority is `dev` merged into `main` for 0.1 as soon as
reasonable.

**Q2, where the paper is read (15:21 EST):** "one site, with /paper/ and in order to make this work now i want the
/paper on dev to be just title author and abstract, with the full paper build on the paper branch. then i can merge
paper into dev, then into main to trigger a rebuild. we have some risks of merge conflicts if they are moving in
parallel but it should only be in link correctness since the paper is itself a website and its code components are all
pinned with reproducibility machinery"

The driver's reading, Q1 and Q2 together: one site; a `paper` branch where the paper is iterated and its full build
runs; on `dev` the `/paper/` slot is the title, the author and the abstract; the paper's release event is the merge of
`paper` into `dev` and then of `dev` into `main`, which rebuilds the site; conflicts between the branches are expected
only in links.

**Q3, a DOI per pinned version (15:22 EST):** "Zenodo via GitHub integration" (the popup's option: every GitHub release
archived with a DOI, the software's as well as the paper's; one switch in Zenodo, no token in the repository).

**Q4, earlier pins on the site (15:23 EST):** "Only the current one" (the popup's option: `/paper/` serves the current
pin; earlier pins remain as tags, GitHub releases and their Zenodo DOIs, not as pages).

**Q5, the paper's tests and the software's gate (15:24 EST):** "All leave" (the popup's option: the paper's tests run
only in the paper branch's workflow; the software gate runs the package, docs and site tests; a software change that
breaks the paper shows on the paper branch when it merges `dev` in).

**Q6, what publishes the software (15:27 EST):** "can you do merge itself releases plus failure detection instrument
with a clean up script?"

The driver's reading of the six answers, the design the next stage specifies: the software's release is the merge of
the `dev` pull request into `main` (the gate: required checks, code-owner review, a merge commit); the push to `main`
runs the release workflow, which creates the `v<version>` tag, publishes to PyPI and composes and deploys the site as
called jobs; every step reports, a failure anywhere is detected and named in the run, and a clean-up script (run by the
workflow on failure and runnable by hand) removes the tag and the draft release so the merge can be retried. The
paper iterates on a `paper` branch, whose workflow is event-driven: a push builds and tests the whole paper, a
`paper-*` tag publishes its built HTML and its key manifest as a GitHub release, which Zenodo archives with a DOI
(the software's releases likewise, through the GitHub integration); the paper's tests run only there. On `dev` and
`main` the `/paper/` slot is the title, the author and the approved abstract until the paper's mode names a published
pin; the site composer takes the paper slot from that release's artefact and never builds the paper itself, so a
paper that does not build cannot block the software. Only the current pin is served. The paper's release event
towards the public site is the merge of `paper` into `dev`, then of `dev` into `main`.

## WP65 approved as proxy (15:27 EST)

`WP65-scope-of-work.md` (stage 2, the design: the software's release workflow with failure detection and the clean-up
script; the paper's event-driven workflow on its branch; the mode and the slot; the docs' key manifest; the test gate;
the records; the build plan for three units) is approved by the driver under his mandate on his six answers. One unit
on branch `wp65`; the specification goes to his read with the items that are his.

## His approval of the plan (15:31 EST, verbatim)

"i approve this plan. do you have what you need from me on that?"

The plan approved: the design the six answers fix (the driver's reading above) and the stages after it (WP65 design,
WP66a to c build, WP67 quality control, WP68 integrate with the first merge to `main`, WP69 the cascade review).

## His expectation for 0.1 (15:41 EST, verbatim)

"this split should leave my package in a clean state for an 0.1 release with the paper link only holding the abstract
so i am expecting to need to do that configuration and release work soon."

The driver's reading: the build (WP66a to c) and integration (WP68) stages are the priority after the design lands;
the target state is `dev` merged into `main` as 0.1 with `/paper/` the abstract page.

## WP65 design delivered and accepted as proxy (15:47 EST)

`work-packages/WP65-design/specification.md`, `build-plan.md` and `his-items.md` landed as 44c22443 (rebased onto the
records head; nothing outside the folder; no attribution line). The specification cites eleven GitHub, PyPI and
Zenodo rules it relies on, maps every element of his answers to its section, and places all 23 couplings (10
bridged, 7 cut, 6 left). Three build units with disjoint file sets: WP66b the paper model (19 files), WP66c the
composer, the abstract page and the docs' keys (11), WP66a the software model (20); landing order b, c, a.

The driver's calls on the twelve adjustments the decided design forced: all accepted as the design's (quality control
by pushes to `qc/**` branches since no dispatch exists before the first merge to `main`; PyPI as the last
irreversible step with the clean-up refusing after it and the retry a re-run; the PyPI jobs inside `release.yml`
since trusted publishing refuses a reusable workflow; the mode file's extra fields; the author from `myst.yml`; the
root card's line per mode, its wording for his read; staging from a local artefact; the execution test's platform
question settled at the first paper run; the `pypi` environment without a reviewer since the merge is the decision).
A fourth drift (`docs/code-owners.md` asking `dev` for a pull request) is corrected in WP66a. Three questions remain
his and wait for his return (posed one at a time): the review rule on `main` for a sole code owner; what a merge
without a new version does; whether a paper tag's publication waits for his approval. WP66c and WP66b can start
before those answers (WP66b with the paper-release environment as a one-line switch); WP66a waits on the second.

## WP66b and WP66c approved as proxy (15:48 EST)

`WP66b-scope-of-work.md` (the paper model) and `WP66c-scope-of-work.md` (the composer, the abstract page and the
docs' keys) are approved by the driver under his approval of the plan; each unit's contract is its section of the
specification and the build plan's file set, disjoint from the other's. Both dispatched in parallel on `wp66b` and
`wp66c`; landing order b then c. WP66a (the software model) waits on his second question (what a merge without a new
version does).

## His answers to the design's three questions (popups, one at a time; verbatim)

**Q1, the review rule on `main` (15:53 EST):** "Review rule, you as bypass" (the popup's option: two rulesets on
`main`, one requiring a pull request with one approval and code-owner review with repository admins able to bypass it
for pull requests only, the other holding the required checks, merge-only, no deletions or force pushes, no bypass;
he merges by ticking the bypass; the checks still bind; the bypass goes the day a second code owner exists).

**Q2, a merge without a new version (15:54 EST):** "Site-only redeploy" (the popup's option: when the tag exists on an
earlier commit and the package files are unchanged since it, the run composes and deploys the site and skips the tag,
PyPI and the release; a change to package files with an unchanged version still fails).

**Q3, approval of a paper tag's publication (15:56 EST):** "a code owner must approve it but it does not need to be me"

The driver's reading of the three: Q1 the review rule with him as bypass (two rulesets on `main`); Q2 a merge
without a new version redeploys the site only; Q3 the `paper-release` environment on the paper workflow's publish
job with the code owners as its required reviewers (today that is him alone, so self-review stays allowed; any code
owner added later can approve). All three questions closed; WP66a is scoped from them.

## WP66a approved as proxy (15:56 EST)

`WP66a-scope-of-work.md` (the software model: `release.yml` rewritten with the merge as the release, the site-only
path of Q2, failure detection and the clean-up script; `test.yml` without the paper tests; `pages.yml` removed; the
release checks and tests; the records of G6 the unit owns) is approved by the driver under his approval of the plan
and his three answers. Dispatched on `wp66a`; lands last of the three.

## WP66b landed (16:18 EST)

The paper's release control model landed as ea82a15e (the unit's commit rebased onto dev, plus the driver's one-line
register fix: C919 names the split test). `paper.yml` (push to `paper` and `qc/paper/**` builds and runs every paper
test; a `paper-*` tag publishes the HTML tarball and the key manifest as a GitHub release, drafts published last, the
`paper-release` environment on the publish job per his third answer; the clean-up on failure); `paper/mode.toml` in
`abstract`; `paper/paper-keys.json` (121 keys, canonical) and `paper/build_keys.py`; `scripts/paper_mode.py` and
`scripts/paper_pin.py`; `paper/pin_links.py`; `paper/CHANGES.md`; the `paper` marker deselecting 748 paper tests from
the software gate unless `HTS_PAPER_TESTS=1`; the register, vocabulary and residual tests split by surface with
`--surface` and `--views`; `tests/test_paper_model.py` (51 tests); `work-packages/release-checklist-paper.md`. Eleven
choices where the specification was silent in `WP66b-rounds/notes.md`, accepted.

The driver's independent run on the rebased branch, exit codes captured: lint, format, lock, the YAML parse, vocabulary
on the software surface (0 new), the mode check, the key check, `test_paper_model` 51, the register test, the fast
suite 1,924 passed with no paper test collected, mkdocs; the paper tests under the switch 230 passed and one failed,
`test_paper_residual_counts_do_not_rise`, because `scripts/residuals_baseline.json` was taken at c0fe11b and 52 paper
and appendix counts have risen since: a paper-gate item, not a software-gate one, left for the paper branch (retake
the baseline with his read, or accept the rises row by row). CI dispatched on dev.

The unit's requests, applied by the driver at the other units' landings since messages to running units were declined:
WP66c removes `test_every_paper_key_is_a_label_of_the_built_paper` and `test_paper_theme_is_pinned_to_a_commit` from
`tests/test_site.py` (now in `test_paper_model.py`) and may import `scripts.paper_mode` and read the manifest; WP66a
keeps `test.yml`'s attribution block byte-identical to `paper.yml`'s, makes `release_cleanup.py` accept paper tags, and
adds `scripts/paper_mode.py` and `scripts/paper_pin.py` to amendment 29's ownership. His first answer's `blob/dev`
links are a paper change (the two generator constants and a re-execution of both notebooks) for the paper branch.

## WP66c landed (2026-11-16, 18:20), accepted as proxy

Landed at bf823f22 (the unit's aff808b3 rebased on dev). The composer (`scripts/assemble_site.py`) resolves the slot
from the mode file, serves the abstract page (`scripts/paper_abstract.py`, `site/paper/abstract.html`) in abstract
mode or a fetched, hashed and key-checked pin otherwise, with the fallback said on the page and in the run;
`site.yml` composes and `pages-deploy.yml` deploys, call-only; `scripts/paper_keys.py` resolves the docs' 23
citations from the manifest in both slots. The driver's checks on the rebased head: register, lint, format, lock,
vocabulary, WP66b's mode check against the composer's call, the offline stage, the slot tests and the fast suite
(1,870 passed, the site, build and slot modules deselected after the unit's own 125-test run of 57 minutes), all exit 0.
Captures in `work-packages/WP66c-rounds/captures/` looked at: the abstract page at 1,280 and 375 px in both schemes,
the pinned banner, the root card. The unit's two uncommitted copies of WP66b's files were dropped; WP66b's committed
copies serve. For his read: the root lead sentence "The paper makes the argument and gives the proofs" says more than
`/paper/` holds in abstract mode (the card already says "its abstract; the paper is iterated towards release"); the
abstract page's `tree/paper` link 404s until WP68 creates the branch; a missing or invalid mode file gives the
fallback page rather than a failed build (the unit's literal reading of spec 3.4, `work-packages/WP66c-rounds/notes.md`).

## WP66a landed (2026-11-16, 18:50), accepted as proxy; WP67 scoped and approved as proxy

Landed at 708ef565 (the unit's 68f40db1 rebased on dev, the conflict in `release-candidate.md` resolved by keeping his
"Autonomous until the evening" section before "The two lifecycles"; plus 708ef565, amendment 29's ownership of
`scripts/paper_mode.py` and `scripts/paper_pin.py` by WP10, WP66b's request). WP66b's other two requests were already
met in the delivery: the attribution step in `test.yml` is byte-identical to `paper.yml`'s, and `release_cleanup.py`
knows the three paper tag shapes. The driver's checks on the rebased branch: lint, format, lock, vocabulary, the YAML
parse of every workflow, `release_checks.py pins`, the unit's five test modules, the register test, the fast suite and
the attribution grep, all exit 0. `pages.yml` is gone; `release.yml` runs on pull requests to `main`, pushes to `main`
and `qc/**` (not `qc/paper/**`) and dispatch; `test.yml` on pull requests to `main`, by call and by dispatch.
Follow-ups carried: `CONTRIBUTING.md` wording (WP58); `CITATION.cff` and `pyproject.toml` to 0.1.0 (WP68).

WP67 (`WP67-scope-of-work.md`) is approved as proxy under his approval of the plan: the build plan's section 4 runs
as pushes to `qc/**` and `qc/paper/**`, the browser pass per mode, the machinery diff, the clean-up script by hand,
and one addition from the external review of 2026-11-16: lint and the fast shard on every push to `dev`, landed
before the dry run. The paper build's known residual-baseline failure is recorded, not repaired (the paper branch's
first item).

## His answer on the process record (2026-11-16, 20:58 EST), verbatim

Asked, with the disposition of the external review of 2026-11-16, whether the process record leaves the tree before
the 0.1 merge or after: **"Before 0.1"**.

**Disposition.** WP73 (`WP73-scope-of-work.md`), approved as proxy: the landed packages' documents leave the tree
after WP67 lands and before WP68's pull request, the index naming the hash each is read at; the references from
the tests, the docs and the paper resolved; the material pending his read listed with its blob URLs in
`supervisor-review-list.md`.

## WP67 landed (2026-11-17, 01:40 EST), accepted as proxy

The driver's acceptance under his mandate; his read of `work-packages/WP67-rounds/record.md` pending (the release
issue of WP68 cites it). Record 0d5a4df4; the D-4 fixes cb0ad18f and b8197b52; the trigger f05ad97c and 57a0dc25.

**Met:** G1 (release dry run, all three shards after D-4 item 1), G2 (the failing dry run stops at admissibility,
nothing after it, no issue), G3 (the artefact's `/paper/` is the abstract page), G6 (clean-up dry runs exit 0), G7
(the machinery diff, 104 rows explained), G8 (the browser pass, five modes, eighty captures), G9 (lint and the fast
shard on every push to `dev`); R-2 (no release, tag or issue; the `qc/**` branches deleted); R-4 and R-5.

**Not met on the hosted runner, recorded as the paper branch's first items (G4, G5):** three paper tests fail on
Ubuntu runners and not locally: the residual-count baseline (52 counts above the c0fe11b baseline; known since
WP66b), the clean-kernel notebook check (the tab-F-datasets sha256 drifts on the runner), the myst HTML build's
full-size figure links (0 of 3 on the runner, 3 of 3 locally). The paper branch takes them before its first tag.
The planted test of G5 was appended to a module the paper marker does not cover and was never collected, so G5's
run showed the same three failures as G4; the failure path (`build` fails, the summary names the step, no release,
no issue) was seen on those, and the planted case is recorded honestly as not exercised.

**What the browser pass found and fixed (D-4 item 3):** the pinned slot's banner, written as a static element after
`<body>`, failed the article theme's React hydration (error 418) and was dropped from every pinned page once the
page's scripts ran; the composer now installs it by a script before `</body>` and names its colours for both
schemes (unstyled it read black on the dark background) with padding clear of the theme's scheme button.
Specification 3.2 amended; `tests/test_paper_slot.py` amended; the fast suite, the register test, lint, format and
the lock check green on both commits.

**Two things for him, not fixed:** (1) a paper archive packed by hand on a Mac carries AppleDouble members and the
composer refuses the first one (`._index.html is not UTF-8 text`), so it falls back with that reason; options (a)
skip `._*` and `__MACOSX/` members, (b) keep the refusal, (c) refuse with a reason naming the cause and
`COPYFILE_DISABLE=1`. The hosted build packs with GNU tar and writes no forks. (2) `stage_site.py --serve` serves the
site at the root while a hosted `paper-release` artefact's assets point at `/hyperbolic-trade-space/paper/`, so a
local review of a hosted artefact renders unstyled; the staging script could serve under the Pages prefix (an item
for WP58 or WP68's staging, not the release path).

**Process:** the browser-pass unit's loop hung on a server that ignored its interrupt and the unit ended without a
hand-back; the driver stopped it, finished the loop and ran the four later attempts. The captures in the tree are
the top 1,200 px of any page taller than 2,000 px (the full set weighed 364 MB); the table's measurements are of
the full pages.

**Next:** WP73 (the process record leaves the tree), then the correction package for `VerifyRequirementUsage`,
then WP68 up to the pull request, which waits for his word.

## WP68 scoped and approved as proxy (2026-11-17, 02:05 EST)

`WP68-scope-of-work.md` (the first merge into `main`: version 0.1.0, the changelog, the punch list, the local and
hosted checks at the head, the staged site looked at, the release issue drafted, his settings read back, the pull
request on his word, the steps after his merge) is approved by the driver under his approval of the plan
(`WP65-design/build-plan.md`, section 6). The pull request, the merge and his keyboard items are his; nothing
outward happens before his word, quoted here when given. Runs after WP73 and WP74 land; its index row is added
when WP73's rewrite of the index lands.

## WP74 landed (2026-11-17, 02:55 EST), accepted as proxy

The external review's finding 7 (the repository matched only `SatisfyRequirementUsage`, the name opensysml 0.12.1
gives a `verify requirement` statement in `query`): `WP74-scope-of-work.md`, approved as proxy under the review's
disposition; landed at 20a4d624 (the unit's ada60258 and the driver's correction). One constant,
`REQUIREMENT_USAGE_KINDS`, in `examples/adcs/experiments/probes.py` (not `cubesat_model.py`, which the experiment
ledger hashes), used at every match of what `query` returns: the probes' counts, `_verified` and
`_requirement_usages` in `tests/test_system_model_v2_r1.py`, the model-checking test. Two planted tests read a
requirement usage under either name. The driver's correction at acceptance: the satisfy loop of
`scripts/sysml_project.py` `behavioural` stays on `SatisfyRequirementUsage`, since the API JSON it reads keeps
satisfy statements and verify statements apart and the widening would have counted verify statements as satisfy
statements on a corrected engine. Fast suite 1,984, register, lint, format, lock green on the landed head; the
touched and ledger tests 160 passed with the engine present. Index row when WP73's index lands.

## WP73 landed (2026-11-17, 03:50 EST), accepted as proxy

The driver's acceptance under his answer "Before 0.1". Landed at 276728a3 (nine unit commits rebased on `dev`).
The documents of every package landed, accepted, delivered or superseded by 2026-11-17 left the tree: 521 tracked
files, `work-packages/` from 70 MB to 7.4 MB (815 to 289 tracked files); each index row reads
`git show 4f81a4ea:work-packages/<file>`, 4f81a4ea being the `dev` head the archive started from. References from
outside the record: 29 moved with their files (`tests/data/wp45/`, `tests/data/wp57/`, `examples/adcs/spikes/`,
`paper/data/`), 118 repointed to the hash (code, tests, TOML, YAML, Markdown; seven in `notes/`, citation strings
only), one dropped; the table in `WP73-rounds/references.md`. Fourteen items pending his read are listed with
their questions and blob URLs at 4f81a4ea in `supervisor-review-list.md`. `tests/test_index.py` dereferences every
hash and path and refuses a bare removed path outside the record; it skips on a shallow clone. The driver's
checks on the rebased head: index test 5 passed; register; fast suite 1,989 passed; lint, format, lock;
vocabulary; the strict docs build in the abstract slot (after `build_generated`, `build_figures`,
`build_site_figures`); no attribution line. Left for WP58: WP25's eight files, WP21's scope and WP12's decisions
(kept by index state), the README's stale WP28 sentence, and the retained-by-decision files the index names.

## WP68, G1 to G6 done (2026-11-17, 06:20 EST); G7 to G9 wait on him

Landed on `dev`: 6b487929 (the changelog's `[0.1.0] - 2026-11-17`, the punch list, `WP68-rounds/checks.md`) and
ab8fc0f9 (version 0.1.0 in `pyproject.toml`, `__version__`, `CITATION.cff` with `date-released`, `uv.lock` by
`uv lock` with the project's own line the only change, and the interface contract's manifest value, which R-2 of
the contract has the bump edit in the same commit; contract version 29 unchanged). The unit's full software suite
found that fifth copy of the version (one failure, then fixed); the driver's checks on the landed head: the
contract, release, index and site tests 200 passed; register; fast suite 1,991; lint, format, lock; the changelog
check exit 0; `__version__` reads 0.1.0. The staged site at 7e6839a0 looked at (G5, `WP68-rounds/record.md`); the
release issue's text drafted (G6, `WP68-rounds/release-issue.md`), to be opened with the pull request on his word.
The changelog's date is provisional: the merge's day is written when he says the word. The `qc/release` dry run
at ab8fc0f9 is the last run before the pull request (R-2); its result goes in `driver-log.md`.

**What waits on him:** the keyboard items of `WP65-design/his-items.md` (G7), his word for the pull request from
`dev` into `main` (G8), his merge, then the after-merge steps (G9). Nothing outward has been done: no pull request,
no issue, no tag, no release.

## Zenodo stays off; his site review comes before the pull request (2026-11-17, 09:05 EST)

To the driver's release walkthrough (the status, the pros and cons, what he reviews to get there), his two
decisions, verbatim:

> i want to keep the zenodo publication step turned off until we have a first full draft approved.

> i need to do a full review of the documentation and top level static site for me to click through.

**Applied as.** Zenodo is a switch in Zenodo's own GitHub settings and nothing in the workflows, so no workflow
changes: his keyboard list (`WP65-design/his-items.md`, section 5) now says the switch stays off; the release
issue's text, `docs/code-owners.md`, the software checklist's R1 and WP68's G7 and G9 (amendment 1 in the scope)
no longer count a Zenodo archive among 0.1's outputs. The 0.1 GitHub release is therefore not archived and mints
no DOI; `CITATION.cff` carries no DOI. A consequence for the paper line: a pinned paper mode needs a DOI in
`paper/mode.toml` (`scripts/paper_mode.py`), so no working-paper pin is published before Zenodo is on, which by his
word is when a first full draft is approved; `/paper/` holds the abstract until then. The pull request from `dev`
into `main` waits on his click-through of the documentation and the top-level site: the site at the head
(814853ad) is served on 127.0.0.1:8797 and the route map is `WP68-rounds/his-site-review.md`, where his findings
are collected. Nothing outward has been done.

## Two more code owners; no solo owner on PyPI (2026-11-17, 09:40 EST)

Verbatim, mid-morning:

> for the release i would like you include danilo and rohan as codeowners and at least danilo ( danlessa) has a pypi
> account so we don't end up with a solo owner package. by the way i am logged in to pypi as mzargham in my browser ow

**Applied as.** `@danlessa` added to the `*` line of `.github/CODEOWNERS` (he is already a repository admin, so
the write access CODEOWNERS needs exists); Rohan's GitHub login is asked for and added when given. The procedure
is the one `docs/code-owners.md` states under "Adding a code owner": collaborator with write access; Owner or
Maintainer on PyPI and TestPyPI; required approver of `paper-release` with "Prevent self-review" on; the bypass
removed from the first `main` ruleset. The PyPI project does not exist yet (the first publish creates it under the
account that registered the pending publisher), so the PyPI step is an after-merge item in the release issue, done
by him in his signed-in session. Open for him: whether the 0.1 pull request is approved by a second code owner
under the review rule, or merged by his bypass as Q1 of the release models decided while he was the only one.

## The package is named `tradespace` (2026-11-17, 10:20 EST)

Before the pending publisher was created, verbatim:

> so this is our last chance to reconsider the name. one question. is just `trade-space` available?

The driver's answer: nothing named `trade-space` or `tradespace` exists on PyPI or TestPyPI (the simple index 404s
for both; PyPI treats the two as one name since 2024), and no repository of that name exists under the
organisation; a rename touches 334 files, the import path, the repository name and the Pages address, and needs a
new full verification. His decision:

> i want the shorter name. tradespace, let's rename the package in github and take the tradespace name in pypi

**Applied as.** The repository is renamed `DynamicalSystemsGroup/tradespace` on GitHub (the old address redirects);
the distribution and the import are both `tradespace` (`src/tradespace/`); the Pages address becomes
`https://dynamicalsystemsgroup.github.io/tradespace/`; the pending publishers name project `tradespace`, repository
`tradespace`. The tree rename is one unit (WP77; WP76 is left to the iron-triangle example, in flight in its own
session) with the full verification repeated: suite, lock, strict docs in both slots, the site looked at, a new
`qc/release` dry run. Version 0.1.0 is unchanged, since nothing was released under the old name; the changelog's
0.1.0 entry names the rename. Verbatim quotations and dated records (`*-decisions.md`, `driver-log.md`) keep the
old name as history; live documents and every current-state file take the new one.

## The paper's reviewer is Jamsheed Shorish; the code owners are for code and documentation (2026-11-17, 11:05 EST)

While setting the `paper-release` environment, verbatim:

> i want jamsheed shorish as a reviewer on the paper. rohan and danilo are for the code and documentation

**Applied as.** The `paper-release` environment's required reviewers are `jshorish` (an organisation member with
read access to the repository, so eligible) and `mzargham`, with "Prevent self-review" on: a paper tag he pushes is
approved by Jamsheed; one pushed by anyone else, by either. This replaces the coupling in WP65's design that made
the code owners the paper's approvers (his Q3 of 2026-11-16 said "a code owner must approve it but it does not
need to be me"); the code owners (`mzargham`, `danlessa`, Rohan when his login is given) approve, merge and
release the software. `WP65-design/his-items.md` and `docs/code-owners.md` ("Adding a code owner") are brought
to this after WP77 lands, since the rename unit holds those files.

## The `main` review rule for 0.1: his bypass (2026-11-17, 11:25 EST)

Asked, now that a second code owner exists, who approves the 0.1 pull request (the popup's two options: Danilo
approves under the review rule with no bypass; or his bypass for 0.1, removed afterwards). His answer, the popup's
option as worded:

> Your bypass, for 0.1

**Applied as.** The first `main` ruleset (pull request required, one approval, review from code owners) carries
Repository admin as bypass for pull requests; the second (the four required checks, merge commits only, no deletion,
no force push) has no bypass. He merges 0.1 by ticking the bypass; the checks bind. After 0.1 the bypass is removed,
as `docs/code-owners.md` ("Adding a code owner") says. His settings read back so far: Pages on the workflow;
`github-pages` on `main`, `pypi` on `main`, `testpypi` on `dev`, `paper-release` on `paper-*` with reviewers
`mzargham` and `jshorish`, self-review prevented, no admin bypass; the two pending publishers by his screenshots.

## Rohan's login; a release needs two of three (2026-11-17, 11:35 EST)

Verbatim:

> do you have rohan in code owners? i want a release to only require 2 of 3. so it doesn't bind up if i am busy with
> business stuff

> rohan is "rororowyourboat"

**Applied as.** `@rororowyourboat` (Rohan Mehta; an organisation member with write access) added to the `*` line of
`.github/CODEOWNERS`: the code owners are `mzargham`, `danlessa`, `rororowyourboat`. "Two of three" is the
`main-review` ruleset as designed (one required approval, review from code owners; GitHub never counts the author),
so any code owner's pull request approved by any other releases; the same holds for merges into `dev` under the
admissibility check. His bypass stays for 0.1 and is removed after it.

## Governance as executable: GOVERNANCE.md, the specification, the conformance check first in CI (2026-11-17, 12:05 EST)

Verbatim, after his settings were read back:

> are you able to use api access to verify my project configuration? per some of our earlier discussion i want the
> code governance rules specified as executables and the repo configuration conformance checked

> i think we may need a GOVERNANCE.md file and a pointer to the executable specifications and the conformance checks.
> i also want my ci to include a first step that checks the controls are in place as specified before proceeding
> with the rest of the checks. these metachecks make it clear that the repo contents includes a specification of its
> own release rules and that those release rules were in effect as of the release

**Applied as.** WP78 (`WP78-scope-of-work.md`), scoped from these words and approved by the driver as his proxy under
the mandate: the expected repository configuration declared in one file in the tree; a checker that reads the
live configuration through the GitHub API and fails on any difference; `GOVERNANCE.md` at the root pointing at
the declaration, the checker and the admissibility rows; a first job `controls` in the Tests and Release workflows
that every other job needs; the release run's summary and the release notes carrying the check's result at the
merge commit, so a release attests that its own rules were in effect. It starts when WP77 (the rename) lands,
since both touch the workflows and the code-owners page; it is part of 0.1 (the 0.1 release is the first to carry
the attestation).

Added, verbatim, on the scope:

> this will make the removal of the bypass rule explicit in the repo in release 0.2

So the bypass on `main-review` is removed by a commit to the declaration after 0.1, named in the 0.2 changelog, and
the 0.2 release's attestation shows the rule without the bypass in effect at that merge.

## No read-through before the release; the repository's organisation checked; the `paper` branch cut now (2026-11-17, 12:50 EST)

Verbatim:

> i don't need to do a read through before the release. i want to focus on getting the release out but i am making
> sure our repo organization both in the repo and in github are all configured. that includes how code is organized,
> how issues and PRs should templated, conformance and admissibility checks that can be executed but also guidelines
> that are provided to handle criteria that cannot be reduced to prescripted checks. the flow for the software and
> documentation has been cleaned up but i want to make sure we maintained a clean seperation for the paper work.
> ultimately they merge into the same main but we went to some pains to keep the work separable. i think the best
> move would be to create the paper branch, and do some exploration and testing to make sure we have what we need in
> place to support parallel work.

**The driver's reading and application.** (1) His click-through of the site (his word of 09:05) is no longer a
gate on the pull request; the route map `WP68-rounds/his-site-review.md` stays for his reading after the release.
The gates left are WP78 landing and his word for the pull request. (2) WP78 gains, by amendment 1 in its scope, an
inventory of the repository's organisation (the code layout, the issue and pull request templates, the executable
checks, and the guidelines for the criteria that are judged rather than checked, which `GOVERNANCE.md` names and
points at) with a readout of gaps. (3) The `paper` branch is cut from `dev` now (c0e210cc, after the rename) and
pushed, so the `paper` ruleset binds from its first push; the after-merge step of WP68 G9 that created it is done
early. (4) A rehearsal of parallel work on the two branches (the paper built and tested from `paper` by `paper.yml`,
a paper edit merged into `dev` to see where the branches touch, the pin flow from a `paper-*` tag through the
composer, the three hosted-runner paper tests) is scoped as WP79, its own piece, not a gate on 0.1.

## Contributing to the paper takes its own route (2026-11-17, 13:00 EST)

Verbatim:

> contributing to the paper should take a different route from contributing to code and documentation. we need to
> make that clear and enable it in practice.

**Applied as.** WP79 (`WP79-scope-of-work.md`): the paper's contribution route made clear (its own section of
`GOVERNANCE.md` and `CONTRIBUTING.md`, a pull request template for the paper) and enabled (a `paper/` ownership line
in `CODEOWNERS` naming the paper's approvers; the admissibility merge row extended to pull requests into `paper`;
the `paper` branch's ruleset; the rehearsal of parallel work: the paper built and tested from `paper` by its
workflow, an edit merged back into `dev`, the pin flow from a `paper-*` tag through the composer). Who approves a
paper pull request is his open decision, asked 13:00.

Answered, verbatim (13:05 EST):

> paper PRs are approved by mzargham or jshorish

WP79's OD-1 is option (a): the `paper/` line of `.github/CODEOWNERS` names `@mzargham @jshorish`; a pull request
into `paper` is merged by one of them who is not its author. WP79 is approved by the driver as his proxy with
this answer.

## His release line: 0.1 on the bypass, then 0.2 through the preferred flow (2026-11-17, 13:20 EST)

Verbatim:

> so my plan to really make sure everything is working is to get the 0.1 release through on my bypass. then remove
> the bypass and add the iron trangle example. then make a pull request for danilo to review. assuming he accepts
> that work we get an 0.2 release and a test of our preferred release flow

**Applied as.** The line after 0.1: the bypass removed by a change to WP78's declaration and then to the ruleset,
named in the 0.2 changelog; the iron-triangle example (its session, branch `iron-triangle-example`) merged into
`dev`; version 0.2.0 and its changelog entry; the pull request from `dev` into `main` approved by `danlessa` under
the review rule (two of three, the author never counting) and merged; the 0.2 release's attestation shows the rule
without the bypass. That release is the first live run of the preferred flow.

Added, verbatim (13:30 EST), on the two reviews (into `dev`, of the work; into `main`, of the release):

> i like it. as long as it is well documented. the 0.2 will test both parts. i might note that we may want to avoid
> mixing the governance change PR with the content addition.

**Applied as.** `GOVERNANCE.md` (WP78 G4) states the two reviews as two decisions with two questions, who makes each
and what each reads. After 0.1 the bypass removal is its own pull request into `dev`, reviewed and merged apart
from the iron-triangle pull request; both ride in 0.2.

Added, verbatim (13:35 EST):

> its possible we need a branch ruleset specifically for governance

**Applied as.** A question for WP78's gaps readout, with GitHub's three mechanisms laid out for his choice: a push
ruleset restricting pushes that touch the governance paths (`.github/CODEOWNERS`, the declaration,
`.github/workflows/**`, `GOVERNANCE.md`) so they arrive by pull request even on `dev`; CODEOWNERS path lines for
those files; a "review from specific teams" rule with file patterns, which needs an organisation team. The readout
states what each binds and what it costs, and he decides; nothing is set before his word.

Added, verbatim (13:40 EST), the principle:

> i plan to use codeowners as the source of truth for authority in the repo, though that file itself will fall under
> the list of governed files. editing governed files will have tighter controls.

**Applied as (WP78).** `.github/CODEOWNERS` is the one record of who holds authority; the declaration names the
governed files (CODEOWNERS itself, the declaration, the workflows, `GOVERNANCE.md`, the admissibility rows, the
templates) and the controls on editing them; `GOVERNANCE.md` says so in those words. The exact tighter control is
the question of amendment 2's readout (a push ruleset so governed files change only by pull request, CODEOWNERS
path lines for them, or both), decided by him; the checker verifies that the live settings match whatever the
declaration says about the governed files.

Added, verbatim (13:45 EST), the vocabulary:

> in econ and law we might call these "secondary rules" or "rules about rules". we need to keep rules about rules to
> a small set files and specify them executably where possible so we can do conformance checks.

**Applied as (WP78).** `GOVERNANCE.md` uses the term: the governed files are the repository's secondary rules (the
rules about how its rules are made, changed and enforced; H. L. A. Hart's term), kept to a small enumerated set,
each specified executably where it can be (the declaration and the checker) and as a guideline where it cannot,
with the readout saying which is which. The set is enumerated in the declaration and in `GOVERNANCE.md`, and
adding a file to it is itself a governed change.

## The root page carries the repository's and the package's name (2026-11-17, 14:30 EST)

Looking at the staged site (the copy on screen was the head before the rename), verbatim:

> honestly i think the top level index needs to have the same name as the repo and the package
> "hyperbolic-trade-space". we can keep the statement about the posynomial invariant form in the short description
> since it remains the formal basis for the approach and

Asked which name, since he wrote the old one (the popup's options: `tradespace`, the morning's decision; or
`hyperbolic-trade-space`, reverting the rename). His answer: "tradespace". So the morning's decision stands and
the head already satisfies the ask: the root heading and `site_name` read `tradespace`, the title
"tradespace: posynomial invariant form", the short description keeps the posynomial invariant form as the formal
basis. Nothing to change.

The sentence's end, verbatim (14:32 EST):

> and worry about changes if when the package ships more features that expand what shaped trade spaces it supports

So the short description names the posynomial invariant form as today's formal basis, and changes when the model
family broadens (the question WP75's readout opens); the name `tradespace` is the stable one.

## The root page's closing sentence (2026-11-17, 15:05 EST)

His paragraph for the root page, verbatim:

> "Trade studies are usually decided from documents and tables, where the detail of the evaluated designs is lost,
> and the alternatives are bespoke or opaque. Computers can help in ways that are scalable, reproducible and
> interpretable, but a model-based method must meet three conditions before a decision-maker can trust it: it has
> to show its reasoning, say where the data do not reach, and let the analysis be rerun. Once these criteria are
> met, design space exploration and design optimization can be accelerated by automated loops without loss of human
> interpretability."

> i know the extra sentence is a bit sales-pitchy but it is true and i think it will impact interest levels in the
> package and encourage it to be used how we intend it to be used

**Applied as.** The sentence is appended to the root page's third paragraph as he wrote it, with one word: "these
conditions" for "these criteria", since the paragraph's earlier sentence says "three conditions" and the glossary
rule is one object, one name. Registered as C1104, kind P (the author's judgement, stated as a possibility).

## Public-link metadata on the root page and the docs (2026-11-17, 15:15 EST)

Verbatim, three messages:

> one other thing that comes to mind is that the top level index cite needs basic SEO and preview machinery

> the doc site probably does too

> formal metadata that other systems expect to see when handling public links

**Applied as.** WP80 (`WP80-scope-of-work.md`), part of 0.1: on the root page, the history page, the abstract page
and every docs page, the metadata that link handlers and search engines read: a description, a canonical address,
Open Graph and Twitter card fields with an image, structured data (JSON-LD) for the software and the site, and a
robots file and sitemap for the whole site; the composer and the docs theme emit them from one source of values;
a test reads them off the staged site. Approved by the driver as his proxy under the mandate.

## His direction for 0.2, relayed from the WP76 session (2026-11-17, ~16:00 EST)

Given by him while reading the site in the iron-triangle session; the verbatim record is that session's
`WP76-decisions.md` on branch `claude/iron-triangle-example-12a7c6`, and the session relayed it here as:

> i also want to clean up the references to the paper which is currently a working paper. only the abstract is
> published as a webpage but the full content can be built from the repo. per our recent changes the paper gets
> its own development path. my overall take is that the documentation site needs work but our goal is not to
> disrupt the 0.1 release, instead to extend the scope of the 0.2 release to be documentation improvements

**Applied as.** Nothing changes for 0.1. The 0.2 board (opened at 0.1's release; held here until then) carries: the
bypass removal (its own pull request); WP76, the iron-triangle example (its pull request into `dev`); the docs'
references to the paper cleaned up (that session's inventory: 22 `paper:` links on nine docs pages, "the paper" in
prose on five surfaces; the paper a working paper whose abstract alone is published and whose full build comes
from the repository on its own branch); documentation improvements as 0.2's scope, scoped as their own package
(he has a scoping card for it from that session). Also on the WP76 branch at his word and outside its package: the
docs home's and the README's first lines gained "or of observed cases: reported devices, species, plot-years,
finished projects" (267b7866), with the site's word budget raised by ten; that lands with the branch.

## macOS is not a CI platform; an issue for later (2026-11-17, 16:20 EST)

Verbatim:

> i realized that since i am developing on a mac we may have done linux and windows ci tests but not mac ones? if
> this is the case i think we continue for now but actually write an issue for addressing in the future

The fact: `test.yml` runs the three shards on `ubuntu-24.04` and the fast and slow shards on `windows-latest` by
dispatch; `release.yml` and `paper.yml` run on Ubuntu only; no job runs on macOS. His Mac is the platform of every
local check in the records (the full software suite, the lemma chain, the docs builds, the browser passes), so
macOS is covered by hand at every gate and never by a hosted runner. **Applied as:** 0.1 continues; a draft issue
in the repository's scope-of-work template is opened for a macOS shard (its cost, the toolkit cache on macOS
runners, which shards) to be scoped after 0.1.

The issue: https://github.com/DynamicalSystemsGroup/tradespace/issues/1 (the scope-of-work template, label `draft`). Two findings on the way: the labels `draft` and
`small-fix` that `docs/code-owners.md` lists as set once by hand did not exist (created by the driver with
`gh label create`, since the template needs them); and the issue, pull-request and label-gate workflows run from
the default branch, which is still e7fd1165, so no admissibility check ran on this issue and none runs on any issue
or pull request until `dev` is merged into `main`. Both go to WP78's gaps readout.

## The `main-review` bypass is him by name, for pull requests only (2026-11-17, 18:50 EST)

Verbatim:

> i removed the role based bypass and changed it to me. we are still going to remove the bypass allowance in 0.2

> okay i changed it and submitted it. check now

Read back: `main-review` active on the default branch, one rule (`pull_request`), bypass `User:10465438` (mzargham),
mode `pull_request` (his first save read "Always allow"; the driver asked for "For pull requests only" and he
changed it before submitting). The declaration follows this once (the check was not yet in force when he changed
the setting); from here on the declaration changes first. The 0.2 removal stands.

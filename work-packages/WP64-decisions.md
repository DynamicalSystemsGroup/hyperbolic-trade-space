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

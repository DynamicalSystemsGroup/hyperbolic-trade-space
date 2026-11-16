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

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

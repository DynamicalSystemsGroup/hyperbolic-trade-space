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

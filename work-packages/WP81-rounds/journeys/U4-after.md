# U4 after the edits (home, bridge)

**Home.** (a) The first line now reads "The project page links these docs, the package and the paper." It no longer
says the paper makes the argument. A closing line was added: "The argument and the proofs are the working paper's;
its abstract is on the project page, and the full text builds from the repository." The bullet is now "Pick a point
on the chart and get a design: the route back and how to check it", which is the wording I asked for. (b) Resolved. I
now know that only the abstract is online and that the full text builds from the repo. The "conjecture" bullet is
gone. (c) Still unresolved from before: "posynomial invariant form" is used before the page defines it. The page also
doesn't say whether `trade_off_report` or `transform` is the main entry point. The closing line gives no build command
or link, so "builds from the repository" is a dead end for me.

**Bridge.** (a) The intro now says "It is the bridge to a search loop that is planned and not shipped." That was my
suggested recast. The chart-theorem and Appendix B.6 pointers are gone. The invertibility section now states its
reasons inline. The cubesat reading is inline too. The outer-loop sentence is "Propose, evaluate, append the row,
refit, and repeat", with no paper mention. (b) All four pointers are resolved as I wanted. (c) One part still falls
short. "The conjecture is that it is a submartingale… convergence result… This is future work, and no conditions… are
derived." is research framing in the docs. I'd still want a plain line: "no convergence guarantee; treat each proposal
as a check". "Serves both aims of the search" is also still there.

**New or remaining blockers.** `Z_target` is still `.mean(axis=0)` of the first row's coordinates. The check is prose
only, with no function and no import path for the case code. "Preimage", "datum" and "selection rule" are not
glossed.

**My take.** The paper links are cleanly gone and the docs now stand alone. What stops me is the missing code for the
check step and for turning a picked point into a target, not the paper.

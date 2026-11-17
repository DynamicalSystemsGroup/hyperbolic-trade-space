# P5 after the edits (theory, temperature, termination, limitations; further reading and home)

**1. Theory.** (a) Every "the paper has them" link is gone. The top line now says "definitions only, no proofs".
"Figure 1 of the paper" is gone. The n-lemma is stated as a definition. The sparse-LP claim is now in plain words: "a
linear program whose solution is generically sparse". (b) Homogeneity: resolved, since it is a one-line statement and
now has no dead link. GP-to-convex: partly. "solved as a convex program after the logarithmic change of variables"
reads as a fact, but no lemma or script is named. Reversibility and constant elasticities: both are statements with
no route to a proof. (c) New stop: the page says "no proofs" and gives no pointer to where they are. The lemma scripts
are named only on Limitations and Further reading.

**2. Temperature.** (a) The lemma links are gone. The new wording is "the supporting envelope (lemma 5 of the lemma
scripts)" and "tau over two times the variance of the score (lemma 22 of the lemma scripts)". The "definition" link is
also gone. (b) The statements in words stay. The route is still weak. "Lemma 5 of the lemma scripts" is an unlinked
number with no file path. I would have to go to `derivation/` and find lemma 5 myself. It no longer dead-ends, but it
is not a route either. The log-mean-exp definition is still not written as an equation here. (c) Nothing new.

**3. Termination.** (a) Unchanged: no paper links before or after. (b) Not resolved. "the perturbation provably
leaving every design's assignment unchanged" still has no lemma, script or pointer. (c) Nothing new.

**4. Limitations.** (a) The Appendix E link is replaced by "The lemma scripts replace pencil-and-paper derivation, not
formal verification; the scripts are under derivation/ in the repository." (b) Resolved. This is what I asked for.
(c) "Closure effect" and the two senses of "conditioning" are still unexplained.

**5. Further reading and home.** (a) Further reading names the working paper, the build folder and `derivation/`
together; Home says the argument and the proofs are the working paper's, its abstract on the project page, the full
text built from the repository. (b) Partly. Home still says the proofs are "the working paper's", but the paper is not
fully available, and `derivation/` is not named there. (c) Neither page gives a build command or a lemma index.

**My take.** Yes, I can now find the route: Limitations and Further reading both lead to `derivation/` without a dead
end. The route is weakest at the point of need. The lemma numbers on the Temperature page have no file name, and
Theory says "no proofs" without pointing to the scripts. What I would still change: add one line on Theory pointing
to `derivation/`; give each lemma number a script name or a lemma index; add a pointer for the termination "provably"
claim; write the convex program once, with objective and constraints.

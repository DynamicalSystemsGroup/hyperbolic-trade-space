# P2 after the edits (examples, fitting, further reading)

Caveat from the reader: P2.md was not yet on disk, so "against my earlier report" is taken from the P2 rows in
journeys.md. [P2.md has since been filed.]

**Examples.** (a) The paper link on the SysML model is gone. The text now reads "described by a SysML v2 system
model... The model and the data are in examples/adcs/: uv run python examples/adcs/k_terms.py". I get a path and a
command I can rerun, which is what I wanted. The text has no "paper" or "Appendix" pointers left. (b) The former
pointer is resolved for the run-and-rerun need. It still falls short on one point: the model is only a path, not
shown. (c) New: "a 7-lemma" and "Figure 6" / "Figure 7" are numbered like a paper's figures, which could read as
hidden paper figures. "The triples are not findings" reads abruptly.

**Fitting.** (a) The thm-extension link is gone. The text now reads "fit n_terms=K terms, where you choose K (Choosing
K)". "Terms" links to the glossary. (b) Resolved. I did not want the paper there. (c) Nothing stops me. The page
claims "solves a convex problem and returns the minimizer" with no statement or pointer for the reviewer. Fitting does
not say where its guarantees are proved.

**Further reading.** (a) New: "The working paper (its abstract on the project page; the full text builds from paper/
in the repository; the lemma scripts under derivation/) carries the literature review, the formal results and the
worked example." (b) This answers my reviewer need only in part. It names a folder, derivation/, and says the paper
builds from paper/. It does not say which lemma backs which claim, and it does not say how to build the paper. (c)
"Formal results" overstates what pencil-and-paper SymPy scripts are. I would say "derivations". The sentence is one
long parenthesis stacked with clauses. The page sits last in the nav, so a reviewer-hander only reaches it by chance.

**My take.** Yes, I can now say where a derivation to hand a reviewer is: derivation/ in the repository, named once on
Further reading. I would still add one line on Fitting and Theory in brief, "each result here has a lemma script in
derivation/", plus a claim-to-script index, a build command for paper/, and "derivations" in place of "formal
results".

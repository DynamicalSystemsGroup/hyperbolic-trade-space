# Spike: the supervisor's own style in his control papers (WP55 prework)

## Papers

Full text read: **A** Zargham, Ribeiro, Ozdaglar, Jadbabaie, "Accelerated dual descent for network optimization," arXiv:1104.1157 (2011), the six-page precursor of **B**; **C** Preciado, Zargham, Enyioha, Jadbabaie, Pappas, "Optimal vaccine allocation to control epidemic outbreaks in arbitrary networks," arXiv:1303.3984, same title as CDC 2013, DOI 10.1109/CDC.2013.6761078; **D** Zargham, Ribeiro, Jadbabaie, "A distributed line search for network optimization," arXiv:1203.2808, ACC 2012, DOI 10.1109/ACC.2012.6314986.

Partly read: **E** Zargham, Ribeiro, Jadbabaie, "Accelerated backpressure algorithm," arXiv:1302.1475 (Sections I, II, VI; publication not resolved).

Resolved, abstract only (journal text closed, no open copy found): **B** "Accelerated dual descent for network flow optimization," IEEE TAC 59(4):905-920, 2014, DOI 10.1109/TAC.2013.2293221; **F** Preciado et al., "Optimal resource allocation for network protection against spreading processes," IEEE TCNS 1(1):99-108, 2014, DOI 10.1109/TCNS.2014.2310911; **G** Jadbabaie, Ozdaglar, Zargham, "A distributed Newton method for network optimization," CDC 2009, DOI 10.1109/CDC.2009.5400289; **H** Wei, Zargham, Ozdaglar, Jadbabaie, CDC 2011, DOI 10.1109/CDC.2011.6161134. Resolved, nothing read: CDC 2012 "Network optimization under uncertainty," 10.1109/CDC.2012.6426324; CDC 2014 "On convergence rate of Accelerated Dual Descent Algorithm," 10.1109/CDC.2014.7039378.

## Conventions observed

**Introduction.** Problem, limit of the literature, insight, contribution, in about a page and a half. A: "Conventional approaches to network optimization are based on subgradient descent". Literature carries a sentence on what each work misses (D). The insight is stated as one sentence ("Our insight is to consider a Taylor's expansion of the inverse Hessian"); the roadmap is parenthetical section pointers inside the contribution sentences (A, D), or one "The paper is organized as follows" (C). Abstracts: one paragraph ending on a quantified claim ("one to two orders of magnitude").

**Notation.** No notation section in A and D; Section II fixes it inline in plain sentences: "The notation x ≥ 0 means that all components x_i ≥ 0", transpose, inner product, norm with :=. C has "Notation & Preliminaries" with graph theory first. Calligraphic sets, lower-case vectors, upper-case matrices, [A]_ij entries, iteration index as subscript k.

**Problem statement.** A displayed template, "maximize ... subject to: Ax = b", numbered (1), after the model's assumptions are said in prose ("We assume that the cost functions are strictly convex"). C states "Problem 1: Given ..., find ..." in words, then "mathematically stated as" min/s.t. with the optimal value named T*, then a change of variables (γ_i = β_i^{-1}) making it convex.

**Assumptions.** "Assumption 1", displayed, named in parentheses (Lipschitz dual Hessian), stated in the section whose result needs them, introduced as "standard assumptions"; C follows with what the assumption implies and an example attaining it with equality.

**Results and proofs.** A sentence says what is coming ("stated and proved in the next proposition"): "Proposition. Let ... Assume ... Then", then "Proof:" at once. A long proof is announced ("we need two preliminary results") with the lemma stated first. An interpretation paragraph follows, tied to a textbook result ("same structure of local convergence results for Newton's method [4, Section 9.5]"). Citations carry theorem numbers ([7, Theorem 7.2.10]). Terms are defined inline with :=. C: Lemma 3.1, Theorem 4.1, Remark 4.1. A heuristic is labelled heuristic and given a certificate (C: dual bound, "within 10%").

**Figures and simulations.** Protocol stated: graph generator, sizes (25 nodes, 75 edges), stopping tolerance 10^-10, trials (35, 50), min/mean/max. Limits stated flat: "minimal when increasing N from 2 to 3", "not a strict decrease".

**Sentences.** "We", "Our goal is"; "Observe that", "Notice that"; present tense for the method, past for what was shown. Limits are said once, unhedged: "This is not a drawback of ADD, but a characteristic of all second order descent algorithms."

**Conclusion.** One paragraph of 120 to 150 words on the contribution, the theorem and the numerical finding, one sentence of extensions with citations (A, E, D).

## Recommendations for the paper

1. Open with problem, limit of existing methods, insight, contribution; drop the audience sentence (A, D).
2. Fix notation in plain sentences where each symbol first appears, with := and [A]_ij-style entries (A Section II).
3. Display the fit as a numbered template naming the optimal value, then the log change of variables (C Section III).
4. State each assumption, displayed and named, in the section whose result uses it (A Section IV).
5. Put "Proposition. Let ... Assume ... Then" first, "Proof:" next, then one interpretation paragraph against a textbook result (A).
6. Cite textbook results by theorem or section number (A).
7. Call the K > 1 alternation a heuristic and give it a certificate, as C does for greedy (C Section IV-B).
8. Fix one simulation protocol (generator, sizes, trials, tolerance, min/mean/max) and put the finding in each caption (A Figs. 1-4).
9. Say each limit once, where it arises (A, after Proposition 1).
10. End with one paragraph and one sentence of extensions (A, D).

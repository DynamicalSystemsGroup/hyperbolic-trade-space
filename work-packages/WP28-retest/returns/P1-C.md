# P1-C

## 1. What this is about

The paper offers a way to turn a large table of evaluated designs into a statement of which qualities pull against which, and by how much. The usual trade study is a weighted-criteria table where someone picks the weights. Here the "weights" are fitted from the best edge of the data instead of argued in a meeting. The authors fit a surface along the outer edge of the designs. They say it is not the true best-possible boundary, but a smooth reference level that about 10 percent of designs are allowed to exceed. Each design then gets two kinds of number: where it sits along that edge (which trade it is making) and how far short of the edge, or beyond it, it is (its "level", which they call the energy differential).

Each piece of the surface (a "term") names the qualities that are in tension on it. They call this an "n-lemma": a dilemma for two, a trilemma for three, and so on. It also gives exchange rates between them, as percent of one given up per percent gained in another. The pitch is "PCA for trade-offs": PCA tells you where the data vary, this tells you what trades against what. The worked example is a cubesat with power, mass and attitude-control qualities: 1000 simulated designs, 706 feasible, 8 measured qualities.

## 2. The main results, as I understand them

- **The problem it fixes is real on this case.** With 8 qualities, 659 of 706 feasible designs are "nondominated", meaning no other design beats them on everything. The usual Pareto shortlist therefore shortlists almost nothing. With 4 qualities it is 126. That is the business case for something other than dominance.
- **The one-term fit is well behaved.** With one term the fitting problem is convex: any answer the solver finds is as good as any other. The paper says this plainly, and also says the answer need not be unique. The fitted weights read directly as exchange rates. The rewriting into "position plus level" can be reversed exactly, back to the original units.
- **A design that scores best on the fitted value is not dominated by any other design.** The paper explicitly does not claim the reverse: some good designs may never come out on top.
- **With several terms the guarantees get weaker, and the paper says so.** Each step of the fitting procedure does not make things worse. The run stops after a bounded number of steps under stated conditions. The solver can certify a local optimum, but not a global one. On the cubesat with three terms the certificate covers only very small changes: the "stable radius" is about 70 times smaller than the near-frontier band. So which term claims 11 borderline designs is not a finding. The paper says this itself.
- **Cubesat, one term.** Five qualities contend: total mass, energy balance, pointing error, depth of discharge, settling time. Their weights run from 0.14 to 0.36, with mass heaviest. These weights rest on an effective sample of about 23 designs out of 706.
- **Cubesat, three terms.** The single tension splits into three, with 4, 5 and 5 contending qualities:
  - Term 1, led by control effort (0.40), covers only 3 percent of near-frontier designs, too few for the association map.
  - Term 2 covers 24 percent. Mass trades against energy balance at -1.7: one percent more energy balance costs 1.7 percent of mass.
  - Term 3 covers 72 percent. It is led by peak slew power and pointing error. Those two move in steps with the wheel and tracker choices, so its exchange rate is across hardware options, not along a smooth trade.
- **Checking against known answers.** On 20 synthetic tables with planted answers, all three terms were recovered in 16. The 4 failures had very few designs (5 to 11) near the edge on their thinnest term.
- **Controller gains change what trades.** With aggressive gains mass enters the tension. With stock gains control effort does instead.
- **Hand-picked candidates.** Three named candidates all sit inside the surface, 15 to 18 percent short in level terms.
- **The three proposed designs failed.** These were designs proposed to fill gaps in the chart. They landed near the edge in level, but only 1 of 3 landed where predicted along it. All 3 failed the depth-of-discharge requirement, because the chart used to propose them had no depth-of-discharge axis.
- **Requirements after the fit.** Applying the four requirements before fitting, instead of after, changes the one-term contending set by at most one quality.

## 3. What I would do next with it

I would run it on a trade we have already closed, where we know the answer and know why we chose it. I would see whether the terms and exchange rates match what my senior engineers would have said. If they match, the tool is a faster and more defensible way to state what we already know. If they don't match, I want to know whether the tool or my engineers are wrong.

I would also run it twice with different, reasonable conditioning choices: which qualities are smaller-is-better, how they are scaled. The paper says these choices "define the question" and change which term comes out. I want to see how much the answer moves before I let a team rely on it. I would not use the "propose new designs" part yet. The paper calls it preliminary, and in the one test it walked straight into a requirement failure.

## 4. What I would tell a colleague

It is a principled way to say "these five things are fighting each other, and here is the rate". That is the sentence I most often cannot get out of an analyst with a pile of simulation runs. It is honest about its limits to a degree I rarely see: it repeatedly states what is not claimed.

The cautions:
- The numbers describe the designs you sampled, not the physics. A tension you never sampled will not show up.
- The one-term weights on the cubesat rest on about two dozen designs.
- How many terms to use is the analyst's call, not the data's.
- The weights depend on how the analyst prepared the qualities.

Treat it as a structured, reproducible reading of the trade space, not as a decision. The paper says the same: whether a finding is a real engineering trade-off is for an engineer to judge.

## 5. What the method does not do, and what the paper does not claim

- It does not pick a design. Selection stays with experts.
- It does not find the true Pareto boundary. When the fitted surface coincides with the true boundary is an open question (Q4).
- It does not claim that changing a design variable would reproduce an exchange rate. The rates describe how sampled designs trade; they are not causal.
- It does not account for requirements in the fit. They are read afterward.
- It does not claim a global best fit for more than one term, nor that the fitting procedure converges in general (Q1).
- It makes no statistical-consistency claim under noise (Q2), and does not claim the right qualities are identified from limited or biased samples (Q3).
- It cannot represent a trade space with dents. The surface is always bowed one way (log-convex), and gaps in the chart are opportunities only if the space really is that shape there, which the data cannot prove.
- It does not choose the number of terms. Mean slack always falls as terms are added.
- The design-search loop has no results and no convergence theorem.
- The kernel extension is not built.
- The hardware values in the cubesat are illustrative, not datasheet values.
- The three proposals illustrate the idea; they do not estimate a success rate.

## 6. Where I was confused or stopped, in order

1. Abstract and Section 1: "the nondominated set holds 126 on 4 attributes ... and 659 on 8, all of them". 659 is not all of 706. I could not tell whether "all of them" meant all 8 attributes, or all designs in some other count I was missing.
2. Abstract: "A fitted posynomial reference surface models the data underlying the table, not the Pareto boundary, and gives the data a coordinate system; the table and its reading are views of that model." I had to read this three times. I did not know what it meant for a table to be a "view" of a model fitted to that same table.
3. Abstract: "its energy differential: its level relative to the surface, by analogy with a potential, not a physical energy." The name kept pulling me toward physics. I ended up treating it as "log of how far short of the edge, as a ratio".
4. Table 1 (prior art). The Differs column assumes I know DEA, Shephard distance functions and max-affine fitting. Phrases like "global exponents per term, not per-unit weights; a band, not extreme units" meant little to me. I skipped most of Section 2.
5. Section 3, "Map and territory". Fine in spirit. But it hands the real caveats to an appendix ledger I don't have, so I could not judge how big the gaps are.
6. Definition 3: "the package's mean subtracts the constant (log K)/κ from every level and changes neither exponents nor offsets." I could not tell whether this matters to me as a reader of results, or only to someone using the software.
7. Definition 6 (the n-lemma). It says the contending set comes from the exact-maximum fit, while the exchange rates come from the fit at the chosen temperature. I followed that there are two fits, but not why one names the set and the other gives the numbers.
8. Section 5, "Conditions of the theory", R1. "The balanced point ... lies in the relative interior of a facet of the supporting envelope with positive normal" was beyond me. I took away only that if this fails, the weights are an arbitrary choice rather than a real trade-off. That sounds important, and I could not tell whether it holds on the cubesat.
9. Section 6. The run of theorem boxes, each with hypothesis codes (A1, F5, I10, ...), is not written for me. I read only the plain sentences between the boxes, which the paper says are there for that purpose, and they helped.
10. Section 6.2, the K = 3 numbers: "the margin is 0.00121 and the stable radius 0.0001209, against a band 1/tau of 0.0088". I understood the conclusion: the certificate covers only tiny changes, so 11 borderline designs could go either way. I could not judge whether a certificate that small is worth having for a decision.
11. Section 8, after Figure 4: "the effective sample size is 23.1 designs ... so the exponents at the fit temperature rest on about 25 of the 706 designs". Why 23.1 in one place and "about 25" in the next? Small, but it made me wonder which to quote.
12. Figure 4 caption: "the band 1/tau is 0.0262". Later the K = 3 fit has its own band of 0.0088, yet "the figures of this section ... use the K = 1 band at every K". I did not follow why the figures would use a different band from the fit they show, or what that changes in what I see.
13. Figure 8, term 3. Power margin and depth of discharge carry weights of 0.02 but are not outlined as contending. Energy balance has weight 0.00 but is outlined. Definition 6 explains the second case (contends in the limit). I found nothing explaining the first: a quality with a nonzero exchange rate that is not in the contending set.
14. Section 9: "Term 3's two leading metrics ... are stepped by the swaps ... so its elasticity is read across the swapped parts' alternatives". This is the term covering 72 percent of near-frontier designs. If its exchange rate is really a comparison between hardware options rather than a smooth trade, what does the -rate mean to a manager? I expected the largest term to be the most usable, and it reads as the least.
15. Section 9, propose-predict-check: "a hole of the four-metric chart, within a radius that a stated rule sets from the data: the 2nd percentile of the pool's nearest predicted distances to the 300 most isolated holes." I could not follow this.
16. Section 9: "Of 3 proposals ..." and then Section 10: "Two of the three proposals are one configuration". So there were really two designs. That should have been said up front.
17. Section 10: "Novelty V - 1 says how far beyond the fitted reference surface a design lies". I followed this. But the final remark about scoring new technologies by how far above V = 1 they are forecast to sit made me ask: forecast how, given the method only describes the sampled table?

## 7. Terms whose meaning I had to guess

- **Energy differential / level (log V):** how far a design is inside (negative) or beyond (positive) the reference edge, on a log-ratio scale. Roughly, -0.15 means about 15 percent short on all qualities at once.
- **Fit temperature (τ):** a knob for how strictly the edge hugs the very best designs. Higher means stricter, so fewer designs set the edge.
- **Band (1/τ):** the tolerance zone around the edge within which a design counts as "near-frontier".
- **Effective sample size:** how many designs actually set the edge.
- **Reach (β):** how far out the data go in a given weighted direction, i.e. where the edge sits.
- **Contending set / n-lemma:** the qualities with real weight on a term, i.e. the ones in tension there.
- **Cell:** the designs a given term "owns" (scores highest).
- **Term share:** the fraction of near-frontier designs in each term's cell.
- **Mean slack:** an average of how far designs sit below the surface. The fit minimizes it.
- **Simplex:** the weights are positive and add up to one.
- **Posynomial / monomial:** a monomial is one product of qualities raised to powers (one trade-off). A posynomial is a sum of those (several trade-offs).
- **Log-convex:** the surface bows outward only, with no dents.
- **Conditioning:** the analyst's preparation of raw attributes: flip smaller-is-better ones, shift and scale them.
- **KKT conditions, Hessian, critical cone:** technical tests that the solver sits at a proper optimum. I took them on trust.
- **Supporting envelope:** the strict version of the edge, with no design allowed past it.
- **MoE / MoP:** measure of effectiveness (what the customer cares about) versus measure of performance (what the subsystem delivers). These I knew.

## 8. Questions I am left with

- How sensitive are the contending sets and exchange rates to the analyst's conditioning choices? The paper says the choices define the question, but shows no example of the answer moving.
- With the one-term answer resting on about 23 designs, how much would the weights shift if a different 1000 designs were sampled? The paper says designed samples carry no sampling error in the usual sense. Then what do I use to judge stability?
- How should a team choose the number of terms? Three is "the analyst's choice". What would a second analyst choose, and would it change the story told to the board?
- Is there a case where the method's answer changed a decision a weighted-criteria study would have made, and was then shown right?
- For a term whose leading qualities step with discrete hardware choices (term 3 here), is the exchange rate usable for anything?
- Can the requirements be brought into the fit, so that proposals do not run into a requirement the chart cannot see?
- When the edge it fits is not the true best-possible boundary (Q4), how wrong can the exchange rates be?

## 9. Would I read the appendices?

Selectively, yes. I would not read the proofs (B); I would leave them to a technical reviewer, and the paper says they are machine-checked against code. I would read the assumptions-and-gaps ledger (E), because that is where I learn how far I can lean on these results. That decides whether I put my name to a choice resting on them. I would read the stability results (D.5, D.11) to see what survives perturbation. I would read the requirements reading (D.17), because requirements are what I answer for. The rest I would delegate.

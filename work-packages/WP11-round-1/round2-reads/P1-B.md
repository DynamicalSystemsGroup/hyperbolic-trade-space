Cell: P1-B (persona P1, depth B); model: sonnet; date: 2026-11-10
Slice commit: c6d0fff (staged build in the stage worktree, served at 127.0.0.1:8790); reader prompt: prompts/P1-B.txt

REPORT (reader P1-B: executive, undergraduate engineering economics, no optimization theory)

1. WHAT THIS IS ABOUT
This is a paper, and a method, for deciding between competing designs when you are trading many measures of goodness against each other. The case study is a cubesat. It has eight measures: pointing error, settling time, control effort, total mass, energy balance, power margin, depth of discharge and peak slew power. Each design is a choice of reaction wheel class, star tracker grade, solar panel span, battery capacity and controller gains. The authors fit a smooth "reference surface" to a large sample of simulated designs. The surface summarises the best the sample suggests is achievable. The weights on its terms tell you which metrics are in tension with which. Figure 2 (the parts and their swap/tune variables) and Figure 3 (requirements mapped to the eight metrics) show the case clearly. Those two I can follow as an engineer.

2. THE MAIN RESULT
I can only state it loosely. The method produces a surface that is not the Pareto boundary, a "weighted geometric mean of the metrics that doubles when every metric doubles". Its weights ("exponents") read as elasticities: percent change of one metric per percent change of another along the surface. On the cubesat, one surface term blends contending sets of metrics that three terms separate. In the single-term fit, total mass carries the largest weight (0.36), then energy balance (0.18), pointing error, depth of discharge, settling time (0.16, 0.16, 0.14), and three metrics carry nothing (Figure 4). The paper's stated claims are about the fit being well behaved (convex for one term), the surface being tied to Pareto-efficiency for a maximiser, and guarantees for the several-term fit being weaker, with some questions explicitly open. That several-term fit is not guaranteed to find the best answer; the paper says so.

3. WHAT I WOULD DO NEXT WITH IT
- Ask my staff for the one-page version: for this cubesat, which two or three trades matter and which design changes move them. Figure 6 suggests the answer (settling time against control effort, mass against energy, pointing error against peak slew power), but I would not take it from a caption.
- Ask for the tradeoff in my own units: what does one percent more mass cost in energy balance, in dollars or kilograms of launch budget?
- Ask whether the pointing-error requirement, which the baseline does not satisfy (Figure 3), is moved by anything the surface suggests.
- Not commit to a design on the strength of this alone. I would treat it as a map of where the tension is, to be checked against a simpler analysis my team already trusts.

4. WHAT I WOULD TELL A COLLEAGUE
"It's a way of finding which of your many requirements actually fight each other, from a big batch of simulated designs. It draws a fitted boundary and tells you the weights. On a cubesat it says mass and energy dominate, and that a single boundary hides three different sub-trades. The theory looks careful about what it claims. I couldn't judge whether the fitted surface is the right thing to trust, and I would want someone I know to confirm the trade-offs against engineering judgement."

5. WHAT THE METHOD DOES NOT DO (as I read it)
- It does not find the Pareto boundary. The paper says it is "not the Pareto boundary".
- It does not give a global optimum for several terms. It guarantees descent and local optimality at best, and says "Global optimality is not claimed."
- The association maps (Figures 8 and 9) are described as "an analysis of those designs and not of the model". They describe the sample, not the system.
- It does not choose a design for you. There is no cost, risk or schedule weighting that I could see.
- It depends on how the analyst conditions the metrics into positive larger-is-better numbers, and the placement of requirements in subsystems is "the analyst's reading". Those are judgement calls outside the method.
- A search of the design space is marked "preliminary", and four questions are listed as open.

6. WHERE I WAS CONFUSED OR STOPPED
- "Figure 1: The n-lemma on the simplex ... a corner, one metric binds alone; an edge, a dilemma of the two metrics at its ends; the interior, a trilemma." I understood the picture (which metrics a term trades). I did not understand "binds", "support" or "simplex". "The n-lemma printed is the support of the exact-maximum fit, not read off the marker" lost me completely.
- "the fraction of designs above V = 1 (V is the invariant value; above 1 is beyond the fitted reference surface)". I could not tell whether a design above the surface is good, impossible or an error. Figure 5 shows many designs far below the line and few above, and "larger is better", so I assumed beyond the surface means better than the fit expects, but I am not certain.
- Figure 4 caption: "the vertical line is the fit temperature, where the fraction first meets the target". Why target 0.1, and who sets it? I also do not know what "effective sample size" of 23 means for my trust. It starts around 560 and falls to 23, which sounds alarming.
- "temperature" generally, as in "fit temperature tau" and "term temperature kappa". It is plainly not physical, and I never learned what turning it up or down does in plain terms.
- Figure 7: "each design's position along the surface (Z0, the first of seven position coordinates, meaningless alone) against its level log V, the energy differential". The plot is mostly designs below zero with a few near it. "Energy differential" is a term from physics used here for something else. I could not read an engineering message from it.
- Figure 8: "Too few near-frontier designs for an association reading: 3 of ten" for term 1, while the title says "4-lemma". Term 1 is therefore described but not analysed. Term 2 shows "5-lemma" while the three terms' contending sets are described as separating sets. I do not see how they separate, as both terms 2 and 3 are 5-lemmas.
- Figure 8/9: "so an outlined metric can be grey". The outlined cells and the weights disagree in places (for example energy balance, outlined, w=0.00 in term 3). I could not tell whether that is a flaw or normal.
- Figure 9: the primary and stock regimes differ greatly (stock: control effort 0.43, total mass 0.00; primary: total mass 0.36). The caption does not say what I should conclude. This is probably the most decision-relevant picture in the set, and it is left unexplained. That the aggressive-gain assumption flips which metric matters worries me.
- Figure 6, bottom: "the tracker grade places the pointing error in three groups ... the large wheel's designs form the lower cloud". This is a clear engineering insight (discrete parts make clusters), but the line fits the data poorly and I could not tell whether that is a problem.
- Definition 4: "the near-frontier band is |log V|<1/tau". In Figure 7 and elsewhere the grey band is a hair-thin sliver, so I do not know what is "near" in practical terms.
- Theorem statements generally ("the Hessian ... positive definite on the tangent space of the active face"). Stopped reading. I took these as machinery for staff to check.

7. TERMS I HAD TO GUESS
- "metric": a measure of goodness, positive, bigger is better after conditioning (guessed from the figure axes: "larger is better").
- "term": one flat piece (a straight line in the log-log plots) of a piecewise surface.
- "contending set" / "n-lemma": the set of metrics that are actually in tension in a piece of the surface. n is the count. A 2-lemma is a classic trade-off of two things.
- "exponent w" / "elasticity": a weight; the percent change of one metric traded per percent of another.
- "near-frontier designs": the designs closest to the fitted surface.
- "above V=1" / "beyond the surface": better than the fit says is typical for the best. This is a guess.
- "association": correlation among the near-frontier designs; negative means one metric is traded for another.
- "conditioned": converted to a positive scale where larger is better (inverse of kg and so on).
- "fit temperature": a knob for how strictly the fit follows the very best designs versus all of them. Low means soft and averaged, infinity means only the best.
- "reach", "share", "cell", "ascent direction", "simplex", "posynomial", "chart", "KKT": not understood and not guessed beyond "cell = the group of designs that go with a term".

8. WHETHER I WOULD GO ON TO READ THE WHOLE PAPER
I would read Sections 1, 9 and 10 (the decision problem, the case analysis and the discussion), and skip the theory. I would go on because the case study is believable. The figures from the system model are what I would show a board, and the finding that one blended surface hides three separate sub-trades, and that the regime (aggressive versus stock gains) changes which metric dominates, is exactly the kind of thing I would want to know. I would not read Sections 3 to 6 and the proofs myself. I would ask someone I trust to say whether the method is sound and whether the statements about convexity and local optimality hold up. I stop short of staking my name on it, because I cannot yet say in plain language what the fitted surface promises me, and the paper says outright that it is not the Pareto boundary, which is what I would normally want.

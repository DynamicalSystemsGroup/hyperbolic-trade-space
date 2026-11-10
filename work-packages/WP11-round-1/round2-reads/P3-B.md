Cell: P3-B (persona P3, depth B); model: sonnet; date: 2026-11-10
Slice commit: c6d0fff (staged build in the stage worktree, served at 127.0.0.1:8790); reader prompt: prompts/P3-B.txt

REPORT (reader P3-B: systems-model engineer; answered from the briefing and the nine figures only)

1. What this is about
The paper takes a table of evaluation outcomes for many candidate configurations, which is what my model already exports. It turns each column into a "metric": strictly positive, larger-is-better, and "conditioned" by some transform. It then fits a "reference surface" to the table. The surface is a weighted geometric mean of the metrics, set equal to one. Each design gets a position along the surface and a level (log V) relative to it. The weights are read as elasticities, meaning percent of metric j traded per percent of metric i. The case study is a cubesat model with eight metrics: settling time, control effort, pointing error, energy balance, power margin, depth of discharge, peak slew power and total mass. The cubesat model is built in a model-based engineering tool (Figures 2 and 3 are its assembly and requirements views). The paper also covers a fit with several terms (K = 3), which splits the surface into pieces, each with its own set of "contending" metrics.

2. The main result
As I read it, the one-term fit is a convex problem, specifically a geometric program. Its exponents are elasticities, and the (position, level) chart is a reversible rewriting of the metrics. The fit is not the Pareto boundary. It is a reference level that some designs exceed. Figure 4 shows a design fraction above V = 1 of about 0.1 at fit temperature 38.1, with effective sample size 23. The exponents there are total mass 0.36, energy balance 0.18, pointing error 0.16, depth of discharge 0.16 and settling time 0.14. Control effort, power margin and peak slew power drop to zero. With several terms there is no global-optimum claim, only descent, a numerical stationarity gap and local optimality. On the cubesat, three terms separate contending sets that one term blends. Figures 6, 8 and 9 show this.

3. What I would do next
- I would take my cubesat table of configurations and eight evaluated outputs and condition each into a positive, larger-is-better number. For example, invert the mass, settling time and pointing error, as the Figure 5 and 6 axis labels do.
- I would run the single-term fit and read the exponent table as a ranking of which outputs bind.
- I would put the exponents next to my model's requirements from Figure 3, to see which requirement-linked metrics bind and which never do. Control effort, power margin and peak slew power get exponent zero in Figure 4, and I would want to know why before acting on it.
- I would then try K = 3 and compare the cells with my parameter swaps (wheel class, tracker grade). Figure 6's bottom panel suggests tracker grade and wheel class show up as visible clusters.

4. What I would tell a colleague
"If you already have a table of candidate designs and their evaluated outputs, this method fits a smooth reference surface through it and reads off trade-off rates between outputs. The rates are the weights on a geometric mean, and the method has nothing to say about what a design is made of. It reports which outputs bind together, and it distinguishes a single 'binding' output, a pair, and larger groups. You supply the conditioning (positive, larger-is-better), and you must choose a fit temperature. The cubesat example is one worked case. Treat the surface as a reference level, not the true Pareto frontier."

5. What I think the method does not do
- It is not the Pareto boundary. Definition 1 and Theorem 9 say a maximizer of V is efficient, but the converse is not claimed.
- It does not condition the data for me. That is my job, and the briefing says nothing about how to do it well.
- It gives no global optimality for K > 1. Theorem 11 and Proposition 3 claim descent and local optimality only.
- The correlation maps (Figures 8 and 9) are "an analysis of those designs and not of the model", so they describe my sampling, not my system.
- It says nothing about how a configuration variable (a swap or a tune) produces an attribute. That stays in my model.
- It does not say how much data is enough, or how to choose the fit temperature beyond "where the fraction first meets the target" of 0.1.
- It does not tell me when negative or zero outputs can be used. Strictly positive metrics are required (A1).

6. Where I was confused or stopped
- "The n-lemma printed is the support of the exact-maximum fit, not read off the marker." (Figure 1 caption) I could not tell why the marker and the printed n-lemma can differ. In the figure, term 1 sits on the edge, but for term 2 the open ring and the filled marker are visibly apart.
- "n_eff = 23" and "the fraction first meets the target" (Figure 4). I do not know what effective sample size means here, or why 23 is acceptable. The caption says the fit temperature is where the fraction first meets the target, but I do not know why 0.1 is the right target.
- "the weight the three carry is printed (here all of it)" (Figure 1 caption). The legend shows "1.00, 1.00, 1.00 (all of it: d = 3)". I could not tell what a weight on a metric triple means beyond the trivial case.
- "an outlined metric can be grey" (Figure 8 caption). In Figure 8 term 3, energy balance is outlined with w = 0.00, so the contending set includes a metric with zero fitted exponent. I could not tell which of the two I should act on.
- Figure 8, term 1 header: "term 1: 4-lemma (4 metrics in the exact-maximum support)" followed by "Too few near-frontier designs for an association reading: 3 of ten". I did not understand why term 1 has only three near-frontier designs when it carries the settling-time and control-effort cluster in Figure 6.
- "Z0, the first of seven position coordinates, meaningless alone" (Figure 7). I did not understand what I should read from Figure 7 if the horizontal axis is meaningless. The vertical level seems to be the content, with most designs inside (log V < 0). The near-frontier band is visually very thin, so I could not judge how many designs count as on the surface.
- Theorem 12's statement "the Hessian H = D − κM ... positive definite on the tangent space of the active face". I could follow it only as a statement and not as a derivation.
- "with the other six metrics held at the median of the near-frontier designs in that term's cell, so a design can lie above the line here and still be inside the surface." (Figure 6 caption) I could not tell how I would judge a fit from these slices, since every plane misleads in a different way.
- The slice in Figure 5 shows many designs above the line (to the upper right of it) and many far below. I could not tell whether that is good or bad fit quality, and the caption does not say.
- "Appendix C.1" is cited for the ranges; nothing in this slice states what range each tune parameter takes.

7. Terms I had to guess
- "Metric": a conditioned, positive, larger-is-better version of one of my outputs. I guessed this from "metrics (conditioned attributes)" in the Figure 5 and 6 axis labels, such as "log of the conditioned total mass (inverse kg; larger is better)".
- "Conditioning": a transform of my raw outputs, such as an inverse, plus an offset. I guessed from Theorem 7, with the form log m = α log(a + s) + b.
- "Contending set" and "n-lemma": the group of metrics that actually bind together on a term. A corner is one metric, an edge is two (a "dilemma"), and the interior is three or more.
- "Fit temperature (tau)": a sharpness knob for the soft maximum. Large tau approaches the exact maximum, which would be the supporting envelope. I guessed.
- "Reach (beta)": an offset that places the surface where the data extend. I guessed from Definition 7.
- "Near-frontier band": the designs within |log V| < 1/tau of the surface.
- "Energy differential (log V)": the signed distance of a design from the surface in log terms, negative inside.
- "Cell": the subset of designs assigned to one term.
- "Term share" and "participation threshold" (0.001): the share of near-frontier designs per term; an exponent below this counts as not participating.
- "Primary" and "stock" regimes: two controller-gain settings (aggressive versus stock). I assumed these are two datasets from the same model.
- "Posynomial" and "geometric program": I know GP from convex optimisation. I guessed the paper uses a sum of monomials in the metrics, fitted in log space.
- "Association": the Pearson correlation of log-metrics among near-frontier designs, with negative meaning tension.

8. Would I read the whole paper
Yes, selectively. The question that matters to me is what to feed in and what comes back, and the figures show a concrete answer: a table of positive metrics in, and an exponent table and cell structure out, which I can compare to my requirements. I would go first to Section 11 (Reproducibility and your own case) and Section 8 (Case construction), because those say how to prepare my own table, how to condition it, and how to choose tau. I would skim the proofs in Section 6 and the appendices, since I do not do proofs. I would want Section 9 (Case analysis) to show how the exponents in Figure 4 turn into a decision. I would stop reading if Section 11 turned out to require rebuilding my model around the paper's conditioning conventions.

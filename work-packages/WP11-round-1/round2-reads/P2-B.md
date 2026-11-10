Cell: P2-B (persona P2, depth B); model: default (the session's default model); date: 2026-11-10
Slice commit: c6d0fff (staged build in the stage worktree, served at 127.0.0.1:8790); reader prompt: prompts/P2-B.txt

REPORT (reader P2-B: working systems engineer, trade studies as documents, practitioner statistics, no convex analysis)

1. What this is about

As far as I can tell from the slice, this is a method for turning a table of evaluated design candidates into a fitted "reference surface" in the space of the metrics being traded, and then reading off that surface which metrics are actually in tension at the frontier and at what exchange rate. The inputs are what I already produce: a list of configurations (in the cubesat case, two part swaps and four tuned parameters, Figure 2), each evaluated to eight metrics that requirements read (Figure 3), with the metrics first made positive and larger-is-better (so mass becomes inverse kg, pointing error becomes inverse degrees). The output of the one-term fit is a set of exponents, one per metric, summing to one, that define a weighted geometric mean V; the surface is where V = 1. The exponents are presented as the weights the data imply rather than weights a stakeholder assigns, and the ratio of two exponents is the exchange rate between those two metrics along the frontier. A several-term version lets the frontier have different pieces with different sets of metrics in tension. The whole thing is set up to be rerun: there is a fit temperature chosen by a stated rule (Figure 4), a glossary threshold for what counts as participating, and scripts behind every statement.

2. The main result

The result I take away is in three parts.

First, the frontier model: a weighted geometric mean of the metrics with exponents on the simplex is scale-free (double every metric and V doubles, Theorem 1), and its exponents are elasticities, i.e. the percent change in one metric you pay per percent gain in another along the surface (Theorem 5, Definition 8). That is a statement I can explain to a programme manager: "at the frontier, one percent less mass costs you about two percent of energy balance" is exactly the sentence a trade study is supposed to deliver.

Second, the one-term fit is convex in log variables (Theorem 3), which I read as: it has one answer and does not depend on where you start. The several-term fit is not convex (Theorem 10) and the paper is explicit that what it offers there is a descent guarantee, a numerical stationarity check and a conditional local optimality, with global optimality not claimed. I appreciated that the limits are written into the statements.

Third, on the cubesat case, the three-term fit separates sets of contending metrics that the one-term fit blends. Figure 9 shows the one-term fit puts 0.36 on total mass and spreads the rest over energy balance, pointing error, depth of discharge and settling time; Figure 8 shows the three-term fit has one piece dominated by energy balance and mass (term 2) and another dominated by peak slew power and pointing error (term 3), with a third piece that has too few near-frontier designs to say anything about. Also from Figure 9: with stock controller gains the frontier is a control-effort against settling-time story and mass drops out entirely; with aggressive gains it is a mass against energy story. That is the kind of "why did the recommendation change" explanation I currently cannot produce from a weighted-score matrix.

3. What I would do next with it

- Take an existing trade study of mine where the option matrix is already in a spreadsheet, convert the criteria to positive larger-is-better metrics (the inverse trick in the figures is straightforward), and run the one-term fit. Compare the fitted exponents with the weights the stakeholders assigned at the time. If they differ substantially, that is immediately a finding worth a review slide: the data say the frontier trades A against B, but we were scoring on C.
- Reproduce a Figure 4 for my own data before trusting anything. The tau sweep is the first thing I would show a reviewer, because it makes the one judgement call (where to set the temperature) visible, and the exponent table across the sweep shows which metrics are robust to that call (in Figure 4, control effort only participates at very low tau, everything else is stable from 25 onwards).
- Rerun the fit every time the evaluation models change and diff the exponent table and the contending set. That is the operational use I care about: a change in a requirement or a model should produce a change in exponents I can point at, not a re-done PDF.
- Bootstrap or jackknife the design table to get a spread on the exponents. The paper shows an effective sample size (n_eff = 23 at the fit temperature in Figure 4) but I did not see interval estimates on w in this slice, and I would not defend 0.36 versus 0.18 to a reviewer without knowing how much they move under resampling.
- Deal with near-duplicate metrics before fitting. Power margin and energy balance have correlation 0.96 to 0.99 in every map (Figures 8 and 9), and the fit puts weight on one and zero on the other, with the choice flipping between regimes (energy balance 0.18 and power margin 0.00 in primary; power margin 0.18 and energy balance 0.02 in stock). That looks like a collinearity artefact to me, not a trade, and I would merge or drop one before running.
- Read Section 11 and Appendix F first, because whether I can set this up on my own project depends entirely on what the pipeline requires of me.

4. What I would tell a colleague about it

"It is a regression for trade studies, but the thing it regresses is the frontier, not the average. You feed it the same option table you already have; it hands back a weight per criterion that the data imply, the weights are exchange rates, and a sweep plot shows how sensitive those weights are to the one tuning knob. The one-term version is well behaved; the multi-term version is a clustering-like iteration with partial guarantees, so run it a few times. The cubesat example is close enough to our problems that you can read the case study without the theory. Watch for criteria that are really the same quantity under two names; the method will pick one arbitrarily. And it does not pick a design for you: it tells you the shape of the frontier, and the choice is still yours."

5. What I think the method does not do

- It does not choose a design or rank options. The surface is a reference level; Theorem 9 says a maximizer of V is Pareto-efficient, but nothing in the slice says the maximizer is the design you want, and the requirements in Figure 3 (including the pointing-error requirement that the baseline fails) do not enter the fit at all.
- It does not describe the system; it describes the sample. Definition 1 is careful that the Pareto boundary is a property of the system while the fitted surface is fitted at finite tau and some designs lie beyond it. So the exponents depend on how the design space was sampled, and the paper's own PCA remark ("the trade-offs the sampling exercised, a reading and not a result") says as much. If my sampling of configurations is lopsided, so is the frontier.
- It does not give uncertainty on the exponents, as far as this slice shows. There is an effective sample size and a sweep, not intervals.
- It does not resolve collinear metrics (see power margin against energy balance above).
- It does not, by itself, handle the discrete structure in the data. Figure 6 bottom shows pointing error in three columns and peak slew power in horizontal bands set by tracker grade and wheel class, with a straight-line segment drawn through them, and the term 3 map in Figure 8 has a correlation of exactly -1.00 between pointing error and peak slew power. To me that reads as two metrics determined by the same categorical choice, not a continuous trade, and the method draws a slope through it anyway.
- It does not choose K (the number of terms) for you, and for K > 1 it does not guarantee a global optimum ("Global optimality is not claimed"; "The bound is for the returned run, not across restarts").
- It does not do the conditioning from raw attributes to positive metrics; that is left to the analyst (Theorem 7 gives the form, not the choice).
- It does not search the design space; Section 7 is marked preliminary and no figure shows it.

6. Where I was confused or stopped

- "The fit temperature τ > 0 sets how hard the maximum is (τ = ∞ is exact)" (Definition 4) and "the temperature of the soft maximum in the fit" (Figure 4 caption). I stopped here for a while. I have no intuition for a temperature in a fit. Theorem 4 helped a little ("the mean and the maximum are the limits"), so I read tau as a dial between fitting the average of the cloud and fitting its outer edge, but I would not be able to explain the mechanism to a reviewer.

- "the effective sample size with its value at the fit temperature" (Figure 4 caption) together with "n_eff = 23" in the figure. There look to be several hundred designs in Figure 5. If 23 of them effectively determine eight exponents, I would want to know how stable those exponents are, and I could not find that in the slice.

- "Balanced hard-support geometry does not imply an interior minimizer at finite τ." (Theorem 2). I do not know what hard-support geometry is and could not reconstruct the sentence.

- "(i) a convex program symmetric in the terms attains its minimum with all terms equal, so the objective over all terms is not convex in them in general" (Theorem 10). I read it three times. I think it means "if the problem were convex, all terms would come out identical, which is useless, so it cannot be convex", but the logic of "attains ... so ... not convex" was not something I could follow.

- "Z = Bu, with BB^⊤ = I and B1 = 0, is the position along the frontier, free of overall scale" (Definition 5) and "log V is the energy differential (level offset)". The matrix conditions I can parse mechanically but the figure that uses it (Figure 7) is captioned "Z0, the first of seven position coordinates, meaningless alone", which left me asking why a coordinate that is meaningless alone is the x-axis of a figure. I took from Figure 7 only that most designs sit below the surface and a handful above, which Figure 4 already told me.

- Figure 8, term 3: "Outlined: the contending set, the support of the exact-maximum fit; w is the exponent at the fit temperature, grey below the participation threshold, so an outlined metric can be grey." The caption explains the case of an outlined grey metric (energy balance, w = 0.00). It does not explain the reverse case I see in the same panel: power margin (w = 0.02) and depth of discharge (w = 0.02) are black, nonzero, and not outlined. So the printed "5-lemma" counts five metrics while six or seven carry weight. I could not tell which set I am supposed to report as "the trade".

- Figure 6, top panel: "one straight segment per term (named on it)". Not in the caption, and the thing I noticed first: two diagonal streaks of designs rising from lower left to upper right, roughly parallel, cutting across the cloud. Those are the most structured feature in the panel and the caption says nothing about them. I assume they come from the controller gains, but I am guessing.

- "primary regime (aggressive controller gains) above, stock (stock gains) below" (Figure 9 caption). I did not know what a regime is until this caption. Are these two separate design tables, or one table split? The term appears in Figures 4, 5 and 6 before it is explained in Figure 9.

- "The fitted reference surface is V = 1 at finite τ, where the posynomial equals one; some designs lie beyond it." (Definition 1). Coming from Pareto-front thinking, a frontier that designs lie beyond is a contradiction until you accept it is a reference level and not a boundary. The sentence does say this, but it took the figures (Figure 7's "a design above the line lies beyond the surface") to make it stick.

- "PCA and the fit are chained: the principal directions of the near-frontier chart read the trade-offs the sampling exercised, a reading and not a result (Appendix D.16)." (Main results). I did not understand what "chained" means here, nor what distinguishes a reading from a result.

- "Numerical: the status a fit reaches. Open: Q1 to Q4 and the search's monotonicity." (Main results). I could not tell what the numerical result is from this line.

- "Term aggregation: sum by default, or mean; the formula is the sum." (Definition 3). I do not know why there are two options or when I would pick the mean.

7. Terms I had to guess

- n-lemma, dilemma, trilemma: guessed from Figure 1 that an n-lemma is the number of metrics that carry weight in a term, i.e. how many things are genuinely in tension. The triangle figure made this clear; the word alone did not.
- Contending set: the metrics with nonzero exponent in the exact-maximum fit; the ones competing at the frontier. Guessed from Definition 6 and the outlines in Figures 8 and 9.
- Cell: the set of designs for which a given term is the largest; a cluster assignment, in effect. Definition 3 says so, but I had to re-read to separate "term" (a piece of the surface) from "cell" (a set of rows).
- Reach (beta): the intercept of the surface in log space; how far out the data go in the direction of the exponents. Guessed from Definition 7 and log V = w·u − β.
- Soft maximum / log-mean-exp: a smoothed maximum that becomes the plain average at low tau and the plain maximum at high tau. Guessed from Theorem 4.
- Near-frontier band: the designs within a tolerance of the surface, the tolerance being 1/tau. Guessed from Definition 4 and the grey strip in Figures 5 to 7.
- Slack, mean slack F: I guessed this is the per-design residual from its own term's surface, averaged; the loss the alternation minimizes. Not defined in the slice.
- Conditioning / conditioned metric: the transformation from a raw attribute (mass in kg) to a positive larger-is-better metric (inverse kg), with the form in Theorem 7. Guessed from the axis labels in Figures 5 and 6.
- Regime: a separate design table generated under a different fixed setting of the controller (aggressive versus stock gains). Guessed from Figure 9 only.
- Posynomial: a sum of products of powers with positive coefficients. Taken from Definition 3; I had not met the word.
- Weakly efficient (Theorem 9): guessed it means no other design beats it on every metric at once, as opposed to beating it on some and tying on the rest.
- Stopping declaration (main results): guessed it is a rule stating at which of the three guarantee levels the several-term iteration stopped and why.
- Elasticity: percent change per percent change, as in economics. Definition 8 states it; I include it because it is the one term I am confident I understood and would reuse.
- Chart: a change of coordinates of the log metrics into (position along the surface, height above it). Guessed from Definition 5 and Figure 7.
- MoP / MoE in Figure 3: measure of performance and measure of effectiveness, the usual SE usage. Not defined in the slice but familiar.

8. Would I read the whole paper

Yes, selectively, and I would start from the back. Sections 8, 9, 10 and 11 and Appendix F first, because the cubesat case is close to problems I actually have, and because whether this is usable depends on what the reproducibility section asks of me and on how the exponents behave under resampling and under changes to the evaluation models. Then Section 5 to understand the fit temperature rule and the several-term iteration well enough to describe them to a reviewer. I would skip Appendix B and most of Sections 3, 4 and 6 on a first pass; the statements as boxed are written for someone who reads KKT conditions comfortably, and I do not.

What pulls me in: the method is rerunnable, the one judgement call is made visible in a single sweep plot, the exponents translate into sentences a programme manager can act on, and the two-regime comparison in Figure 9 is precisely the "why did the answer change" story I am currently unable to produce. What holds me back: the density of the formal part, the open questions about collinear and categorically determined metrics that the cubesat figures themselves expose, and the absence, in this slice at least, of any spread on the exponents. If Section 11 lets me run this on my own table in an afternoon, the rest of the paper earns its reading.

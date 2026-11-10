Cell: P1-C (persona P1, depth C); model: default (the session's default model); date: 2026-11-10
Slice commit: c6d0fff (staged build in the stage worktree, served at 127.0.0.1:8790); reader prompt: prompts/P1-C.txt

READER REPORT — P1-C (senior executive, programme sign-off)

I read the main text and the nine figures once through, as I would a staff paper the night before a review. I did not have the appendices. What follows is my reading, not a verdict on the mathematics, which I am not equipped to audit.

---

1. WHAT THIS IS ABOUT

This is about the part of a trade study I actually have to defend: not the ranking, but the reason for the ranking. Today my staff give me a table of candidate designs scored on several criteria, with weights somebody chose, and a winner. When a board member or a customer asks "why did you give up mass for power?" the honest answer is usually "because of the weights," and the weights are a judgment call.

The authors propose instead to fit a curved surface to the outer edge of the whole table of evaluated designs — the surface that the best designs are pressing up against — and then read off that surface what is being traded against what, and at what rate. They stress it is fitted to the edge, not through the middle, and that it is not the Pareto front (the set of designs nothing beats); it is a smooth reference surface that a few designs may poke through. Every design then gets two numbers: where it sits along that surface, and how far inside or outside it is. Each "piece" of the surface names a cluster of metrics that are in tension with each other (they call it an n-lemma — a dilemma, a trilemma, and so on) and gives the exchange rate between them as elasticities: percent of this per percent of that. That is a language I use already in engineering economics.

They compare themselves to PCA throughout. The pitch is that PCA tells you where your data spreads out; this tells you where your data fights with itself.

The worked case is a small satellite (cubesat) model coupling power, mass and attitude control: 1000 designs evaluated, 706 feasible, 8 attributes each.

2. THE MAIN RESULT

As I read it, there are two results, one about the problem and one about the method.

About the problem: with 706 designs and 8 attributes, the classic "keep only designs nothing beats" filter stops filtering. They report 659 of 706 survive on 8 attributes. That matches my experience — past a handful of criteria, dominance keeps almost everything and the shortlist is made by weights, i.e. by people. That is the motivation and I found it convincing.

About the method: on the cubesat, one fitted term blends everything into a single five-way tension (total mass, energy balance, pointing error, depth of discharge, settling time). Three terms pull that apart into three distinct tensions with different member sets, and two metrics that were invisible with one term — control effort and peak slew power — each come to lead a term of their own. Figure 8 is the payoff: on term 3, peak slew power and pointing error sit at association −1.00, which reads as "you buy pointing accuracy with slew power, almost one for one," and that is exactly the sentence I would want to say in a review. The two-regime comparison (Figure 9) shows that changing the controller gains changes what trades: mass only enters the tension under aggressive gains. That is also a useful, defensible kind of statement.

They also claim the one-term fit is a well-behaved (convex) problem with a unique answer, and that the several-term fit is not, but comes with a certificate saying how good a local answer it reached. I take their word on the mathematics; the structure of the claims — "this is proved, this is observed, this is open" — is unusually clear and I appreciated it.

3. WHAT I WOULD DO NEXT WITH IT

- Ask my systems engineering lead to run it on one completed programme where we already know the answer and the arguments we had. If the fitted tensions match the fights we actually had in the design reviews, that is validation I can stand behind. If they do not, I want to know why before I use it on a live decision.
- Ask one specific question of the authors or my staff: how sensitive are the elasticities to the conditioning step (the units, shifts and scaling of each metric)? The paper says plainly that "rescaling one metric changes which term is tangent." That means two analysts could condition the same table differently and get different named tensions. I need a house rule for conditioning before I would allow this to appear in a decision package.
- Insist that the requirements be applied in the reading. The paper's own proposals section is instructive: the proposed designs reached the frontier "by spending the battery" and all failed the depth-of-discharge requirement. That is precisely the kind of outcome an optimizer produces and an executive gets blamed for. The method did not do anything wrong, but the workflow around it must.
- Use it, for now, as a diagnostic that sits beside the trade study, not as the thing that chooses. The authors say the same thing themselves.

4. WHAT I WOULD TELL A COLLEAGUE

"There is a method that takes the full table of evaluated designs, fits a surface to the outer edge, and then tells you — in percent-per-percent terms — which metrics are in tension with which, and whether it is one big tangle or several separate ones. On a satellite case it pulled one five-way tangle apart into three readable trade-offs and surfaced two metrics the single-tension view missed. It does not pick a design, it does not replace the requirements check, and the named tensions depend on how you scale the metrics first. The authors are candid about all of that, which raises my trust. Worth a pilot on a finished programme before we let it near a live one."

5. WHAT I THINK THE METHOD DOES NOT DO

Mostly in the authors' own admission, which I credit them for:

- It does not choose a design. It gives coordinates and a tension map; the choice "falls to experts."
- It does not find the true Pareto front. The surface is "not the Pareto boundary"; whether it recovers it is their open question Q4.
- It does not tell you how many terms to use. "Mean slack falls with K by construction and cannot choose it: three terms is the analyst's choice." So the headline "three tensions" is partly a decision someone made.
- It does not give causal exchange rates. The elasticities "describe how the sampled designs trade, and not a causal exchange that changing a variable would reproduce." In plain language: it tells you about the designs you happened to evaluate, not about physics.
- It does not give error bars. "Designed samples, such as grids, are not independent observations: the exponents describe the sample and are not estimates with a sampling error." That means I cannot ask "how confident are you in 0.36?" and get an answer in the usual form.
- It does not enforce requirements. The fit "ignores the four" threshold requirements; they are read afterwards.
- It cannot find trade-offs the sampling never exercised, and it cannot represent dents or holes in the trade space (non-log-convex structure).
- The several-term fit has no guarantee of finding the best answer, only a certificate about the answer it reached, and only for "the returned run, not across restarts."
- The design-space search (Section 7) and the kernel generalisation are explicitly unbuilt, with "no results."
- The hardware values in the case are "illustrative and not datasheet values," so the cubesat findings illustrate the method; they are not satellite engineering.

6. WHERE I WAS CONFUSED OR STOPPED

(a) Abstract: "A reversible chart separates a design's position along the surface from its energy differential: its level relative to the surface, by analogy with a potential, not a physical energy." I stopped here. "Energy differential" put me on the wrong foot — in a power-and-mass problem, I assumed for a moment it was a real energy quantity. The parenthetical rescues it, but the term fights the domain. "Level above or below the surface" would have done.

(b) Section 1: "Of 706 feasible cubesat designs, the nondominated sets hold 126 on 4 and 659 on 8 attributes." I understood the point but had to read it three times to parse "126 on 4 and 659 on 8" as counts of surviving designs when 4 or 8 attributes are compared. This is the strongest motivating number in the paper and it is written in shorthand.

(c) Section 5: "$\tau$ puts a target fraction of designs above $V=1$: 10 percent here, a convention that keeps one extreme design from setting the surface." This is the one tuning knob I understood the purpose of, and I would have liked one more sentence on why 10 percent rather than 5 or 20. The sentence says halving or doubling it leaves the contending sets unchanged, which helps, but the appendix reference is where that evidence lives.

(d) Section 6.2, Numerical paragraph: "At K = 3 the margin is 0.00121 and the stable radius 0.0001209, against a band 1/tau of 0.0088 and a median best-minus-second-best score of 0.237: a margin below the band puts at least one design within the band of a seam, here 11 of the 706, and the certificate covers changes under the radius only." I stopped completely. I understand this is a health report on the fit, and that 11 designs sit close to a boundary between two tensions, but I could not tell whether that is good news, bad news, or routine. I would need my analyst to translate it into "the three-term split is stable / fragile."

(e) Theorem 10 statement: "a convex program symmetric in the terms attains its minimum with all terms equal, so the objective over all terms is not convex in them in general." I could not follow the "so." I accept the conclusion (the several-term fit is harder), but the sentence reads as if the reasoning is obvious and it was not to me.

(f) Figure 7 caption and axis: "Z0, the first of seven position coordinates, meaningless alone." A figure that announces its horizontal axis has no meaning on its own left me unsure what I was supposed to take from the horizontal spread. I took away only the vertical story — most designs are inside, a few touch the surface — which the caption confirms is the intent, but I wondered why the axis was drawn at all.

(g) Figure 6, bottom panel. The caption explains the horizontal bands by wheel class and tracker grade, which I followed. But the fitted "term 3" line passes above almost every design, with a whole lower cloud far below. I could not reconcile that picture with the Figure 8 statement that term 3 is where pointing error and peak slew power trade at −1.00. The caption warns that "a design can lie above the line here and still be inside the surface" (and presumably below it and still near it), so I accept this is a slicing artefact, but the figure and the association map pull in different directions for a reader like me.

(h) Figure 8 top: "term 1: 4-lemma (4 metrics in the exact-maximum support). Too few near-frontier designs for an association reading: 3 of ten." I stopped. One of the three headline tensions is carried by three designs. The text says control effort "leads a term of its own," and the one piece of evidence I could inspect for that term is a sentence saying there is not enough evidence to draw. I would want this said in the main text, not only in a caption.

(i) Section 9: "the 4 failures have 5, 5, 6 and 11 frontier rows on their thinnest term." I understood the gist (the method fails when a tension is supported by few designs) but not what "thinnest term" means precisely, nor whether 11 rows is a worrying threshold for a real table with 706 designs and three terms.

(j) Section 9, Candidates: "The 3 measured candidates have lowest energy differential -0.197 and highest -0.153, and 0 of them lie beyond the fitted reference surface." I did not know what the candidates were, who proposed them, or why three. The paragraph assumes context I did not have from the main text.

7. TERMS I HAD TO GUESS

- "Posynomial": guessed a sum of products of powers; the paper defines it, but I had to carry a guess for several pages before the definition landed.
- "Monomial term": guessed one product of powers; one "piece" of the surface.
- "n-lemma": guessed from dilemma/trilemma — a tension among n metrics. Confirmed.
- "Contending set": guessed the metrics that participate in a tension. Confirmed by Figure 8's outlines.
- "Elasticity": I know this from economics — percent change in one thing per percent change in another. The paper uses it the same way.
- "Energy differential" / "level": guessed "how far above or below the reference surface, on a log scale." Confirmed, but see 6(a).
- "Fit temperature tau" and "soft maximum": guessed that a soft maximum is a maximum that lets several top designs share the influence rather than one winner taking all, and that temperature sets how sharply it picks. Figure 4 supports this: the higher the temperature, the fewer designs count (effective sample size falls to 23 at the chosen setting).
- "Effective sample size": guessed "how many designs are really setting the surface." Twenty-three out of 706 struck me as a small number to hang a surface on; the paper does not discuss whether that is comfortable.
- "Near-frontier band": guessed the designs within a tolerance of the surface. Confirmed.
- "Term share" and "cell": guessed that each design is assigned to whichever term scores it highest, and the share is the fraction of near-frontier designs so assigned.
- "Margin," "stable radius," "term gap," "certified," "stationary": guessed collectively as "diagnostics saying the solver stopped at a genuine local answer and how much wiggle room there is." I could not go further.
- "Log-convex envelope": guessed "a smooth outer hull that cannot show dents." The paper's later sentence about dents and holes confirmed the guess.
- "Mean slack": guessed "average distance of designs from the surface," which falls as you add terms because more pieces fit better. Confirmed by the text's own caveat.
- "MoE / MoP": I know these from acquisition practice — measures of effectiveness (what the stakeholder cares about) versus measures of performance (what the subsystem delivers).
- "GGP-compatible kernel": no useful guess; I took it as "a future generalisation that preserves the solvability," and moved on.

8. WOULD I READ THE APPENDICES?

Selectively, and only through my staff. I would not read the proofs (Appendix B) — not my job and not my competence. I would ask someone to read and brief me on three:

- Appendix E, the gaps ledger, because the paper keeps pointing to it as the place where it says what cannot be certified for a real table. For a method I might stand behind publicly, that list is the document I most need.
- Appendix D.5 and D.11, the sensitivity to the temperature and which digits hold under perturbation, because the numbers I would quote need to be the stable ones.
- Appendix D.17, requirements after the fit, because the battery episode shows that the requirements reading is where this method meets reality.

I would also want someone to open Appendix C far enough to confirm what "illustrative hardware values" means in practice, so that nobody in my organisation mistakes the cubesat findings for satellite engineering.

Overall impression, in one line for the record: the method answers a question I genuinely have — "what is really being traded here?" — in a vocabulary I can defend, and the authors are disciplined about what they have not shown. The two things that would stop me using it on a live decision today are the dependence of the named tensions on the conditioning choices, and the fact that one of the three headline tensions in the case rests on three designs.

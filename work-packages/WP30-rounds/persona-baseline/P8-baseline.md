# P8 baseline read (new-space program/business-line executive), origin/dev 45180fd

Read: paper case sections and appendices C, D.17 (notebook text and outputs), paper figures (assembly, behavioural, planes K=3, tensions K=3), docs Examples page rendered at 127.0.0.1:8796. Not read: work-packages, notes, tests, model sources. The paper page itself was not built (read from notebook). I did not find a "stakeholder layer" or "verdicts" section as such: the closest are the MoE/MoP marking in the behavioural view, the four threshold requirements read after the fit (D.17, Examples page), the three hand-named candidates and the three proposals. I treat those as the verdicts.

## 1. What held my interest / what lost it

Held:
- The opening claim that dominance stops shortlisting (126 of 706 nondominated on 4 attributes, 659 on all 8). That is my everyday pain: the trade table where everything is "Pareto".
- Requirements read after the fit (D.17): pass shares, near-frontier designs excluded, and the finding that pre-imposing the four requirements barely changes what trades. If true on a real case this is useful: I could stop arguing about constraint order.
- The honest "propose, predict, check" result: proposals reached the frontier by shrinking the battery to 22-25 Wh and all failed depth of discharge. This is exactly how optimisers behave in my programs, and the paper says so.
- Elasticity sentence for term 2: 1% energy balance costs 1.7% mass. A number I can put in front of a chief engineer.
- Model-derived behavioural view with MoE/MoP and "baseline fails pointing requirement": looks like something I could audit.

Lost:
- Within two screens everything is in log-conditioned, unit-less coordinates (log V, "bands", tau, K, n-lemma). The only money number in the entire case is buried in D.17: launch budget 90,643 USD at 6,000 USD/kg. No unit cost, no schedule, no quantity.
- The verdict never lands on a design or a buy. The paper says it "stops short of selecting a design, which falls to experts." Fine as scope, but nothing shows the method changing a decision.
- Prices of requirements are in "bands" (0.07, 0.56, 7.92). I cannot convert to dollars, kilograms or weeks.
- The case never says what the three terms/contending sets mean for a program (e.g. "buy the fine tracker" or "relax the effort requirement").

## 2. Findings

F1. Case has no cost or schedule axis; only launch cost, derived from mass at a flat 6,000 USD/kg.
- Says: mass is the stakeholder-facing MoE via launch cost (behavioural view, D.17).
- Real business: satellite cost is dominated by bus and payload, not launch for this class; the trade I run is recurring unit cost vs NRE vs lead time vs reliability vs launch. A fine-grade star tracker, large wheel and bigger battery differ in unit price and lead time by multiples; none appears. Rideshare pricing is roughly of the order of 6-7k USD/kg for small payloads as I know it (unsure of the exact current tariff), so 6,000 is sane, but it is a flat linear price with no minimum, no integration fee, no dispenser/mass-class steps.
- Severity: changes the decision (a trade study without cost reads as an engineering study, not a business decision).
- Says toy? Partly: "hardware values are illustrative and not datasheet values" appears once in the case construction text and once in future work. It does not say "no cost or schedule model". Examples page and docs index do not say it at all.

F2. Equal log-spread conditioning makes total mass, the heaviest exponent (0.358), a metric that varies only 11.9 to 16.06 kg (log-spread 0.066, about 35% range), against settling time spanning 7 s to 506 s.
- Says: total mass is the leading contender in the K=1 5-lemma.
- Business reading: a 35% mass spread is about 71k to 96k USD of launch in this model, immaterial next to the program. The scaler gives it the same weight as a 70x-ranging attribute, so the "exponent" is not importance. The paper says conditioning "defines the question" but a reader like me takes "total mass leads" as a finding about the program.
- Severity: changes the decision (misread of what matters).
- Toy flag: partially (the conditioning caveat is in methods prose, not next to the result).

F3. No candidate meets the requirements.
- Says: baseline, all three hand-named candidates and all three proposals have "meets the requirements: False" in both regimes (D.17 table); jointly only 40.8 % (primary) and 38.7 % (stock) of feasible designs meet the four requirements.
- Business reading: the shown designs are all non-compliant, and the model's own baseline fails pointing (0.0155 vs 0.0085 deg). A program would not carry a baseline that fails its own requirement, and "which designs to name by hand" would be the compliant ones. Hand candidates are all interior (log V -0.15 to -0.20), so the method scores them as unremarkable, with no sentence about what a program does with that.
- Severity: changes the decision / cosmetic depending on how it is used; the story reads as unfinished.
- Toy flag: no.

F4. Requirement margins priced in "bands" and log V, not in program currency.
- Says: control-effort requirement in stock regime costs 7.92 bands, 0.17 log V; pointing 0.56 bands.
- Business: I need "this requirement costs N kg, N USD or N weeks". Cost of a requirement is the thing I negotiate with the customer.
- Severity: changes the decision (can't use it); unit-less price is defensible mathematically.
- Toy flag: says "a feature of the fitted model, not a causal exchange", which is honest but does not say how to convert.

F5. Sampling is 1000 random designs over 6 variables (3 wheel classes, 3 tracker grades, panel span 0.3-1 m, battery 20-200 Wh, two gains), roughly uniform (design counts per level near equal; 344/345/311).
- Business: real configuration space is a few vendor parts with discrete availability, integration constraints (volume, deployables, thermal) and legacy heritage; uniform sampling of battery capacity between 20 and 200 Wh is not how a bus is built. Reasonable for a demonstrator; the paper does say it is a worked example.
- Severity: cosmetic for the method claim, changes the decision for any "here is what trades" claim.
- Toy flag: yes, "worked example of design optimization, not a study".

F6. Single scenario: one 30-degree slew, 600 s window, no radiation, thermal, jitter, eclipse variation, degradation or reliability (rg. wheel life). Pointing is a budget formula (computed), not measured.
- Severity: cosmetic for a method paper; changes the decision for any claim about actual designs.
- Toy flag: only implicitly.

F7. Docs Examples page asserts "the finding depends on the regime" and that the contending set "barely moves" with requirements, in the same breath, with no hint of which of the two to rely on. Also the page shows 5/4/5 contending sets and shares 17/10/73 percent at the one-term temperature, the paper shows 4/5/5 and 3/24/72 percent at each K's own temperature; both are labelled but a skimming reader sees two sets of numbers for "three terms".
- Severity: cosmetic.
- Toy flag: n/a.

F8. Fleet, quantity and multi-satellite effects absent entirely (no per-fleet budget, no production learning, no shared-launch packing).
- Severity: changes the decision for my standing question (I budget per fleet); fair scope for a method paper, but the paper never says "single satellite, no fleet".
- Toy flag: no.

F9. Where the paper is honest and I credit it: "A hole in the chart is an opportunity only where the trade space is log-convex around it, which the data cannot prove"; "that the fit supports a decision is a third claim the certificate does not make". Good. But the first claim, "an accountable executive can follow and defend", is not delivered by the case: an executive cannot follow log V, tau, n-lemma without translation.

## 3. Numbers off by more than 2x (or implausible)
- Mass range: total mass 11.9 to 16.06 kg; as a design-driver the exponent 0.36 is out of proportion to its 1.35x range (see F2). Not a wrong number, a mis-weighted one.
- Launch budget 90,643 USD for a ~15 kg cubesat: within about 1x-2x of rideshare tariffs as I recall them (I am not certain of the current rate); but with the mass range, launch ranges roughly 71k to 96k USD, and there is no unit cost to compare. Cost per satellite and per fleet: none given, so nothing to check, which is itself the gap.
- Peak slew power 1.3 to 7.4 W and power margin 6.9 to 66 W for 0.3-1 m panel span: plausible for a 12U-class bus; I would not call these off.
- Battery 20-200 Wh: 10x range; a 200 Wh pack on a 12U is a stretch but not impossible; uncertain.
- Pointing requirement 0.0085 deg (about 30 arcsec) and baseline 0.0155 deg: plausible; fine-grade star tracker with wheels in this class is typically better than that; unsure.
- Settling time 7 s to 506 s for a 30 deg slew: the 70x spread is plausible for gain choices; the long end (8 min) is not a design anyone would fly; the sample includes these without comment.
- No schedule numbers anywhere to test.

## 4. What I would change first, in order
1. Add one sentence up front in the case (and on Examples) stating what the case lacks: no unit cost, no schedule, no reliability, no fleet; hardware values illustrative; single satellite; one slew scenario. The "illustrative" statement is currently in one sentence mid-paragraph in Case construction and absent from the docs.
2. Express the priced requirements (D.17) in program currency: kg and launch USD for mass, and where possible wheel/tracker grade swaps; or state plainly why the method returns bands only and give one worked conversion.
3. Show one decision the method changes: e.g. "with control effort and peak slew power split off into their own terms, the requirement on X can be relaxed at no cost to V; the one-term view would have missed this". Right now the K=1 vs K=3 result is "sets differ", which reads as description.
4. Put a named design that meets the four requirements in the candidates, and say whether the method ranks it above the baseline. At the moment every named design fails.
5. State next to the exponents that mass leads partly because of equal log-spread scaling, in terms of kg and USD (a 4 kg spread equals about 25k USD in launch).
6. Reconcile the Examples page figures (5/4/5, 17/10/73) with the paper (4/5/5, 3/24/72) with one line saying they are at different temperatures.

## 5. Standing question and decision question

Realistic enough to keep me interested? Partly. The structure (requirements, MoE/MoP, mass to launch cost, a baseline that fails a requirement, optimisers cheating on the battery) is recognisably real, and the propose/predict/check result is credible because it admits failure. What loses me is that cost, schedule and fleet are missing, and the case never says in one place that it is a mechanical-and-attitude-control toy. It says "illustrative hardware values" once; it does not say what else is not modelled. So: interested as a method demo; not as a business case, and it does not claim to be one, but it does not flag the gap where I would look.

Would the method change a decision I make? Not on this case as presented. It would change how I run the pre-decision analysis if (a) I could feed it cost, schedule and risk as metrics (the black-box abstraction suggests I can, but the case does not show it), and (b) requirement prices came out in my currency. The plausible uses for me: tell the customer which requirement is expensive (D.17); stop arguing about whether to constrain before or after (the contending set barely moves); catch optimisers/regressors that win by exploiting a bound (battery at 22-25 Wh).

Cost of adoption, as best I can infer: an analyst who writes the conditioning (orientation, shifts, scale) per metric, 1000-ish evaluated designs (here simulations; for me, vendor quotes or test data are far fewer than 706 designs, and the paper says small samples determine exponents weakly), a Python/uv toolchain, and a person who can read log V and n-lemma. I did not see an estimate of the analyst time or of the minimum number of designs; I would ask for it. Per effective sample, the fit rests on about 23 designs of 706.

Do the case's economics and verdicts read sanely? The little economics there is (6,000 USD/kg launch, 15.1 kg limit, 90,643 USD) is sane at the rideshare level; the verdicts are mostly absent or unflattering (all named designs fail requirements; proposals fail DoD), which is honest but leaves no recommendation.

What the method does not tell me (not said in one place): cost and schedule, risk, what to buy, how many to fly, whether the sampled trade space resembles what vendors sell, how the answer moves if a requirement changes by a stated amount in dollars.

Unsure: current rideshare tariffs; whether the fine tracker/large wheel prices were meant to be modelled (I found no cost attribute in the eight attributes); whether a stakeholder-layer section exists elsewhere that I was not directed to read (paper page not built here).

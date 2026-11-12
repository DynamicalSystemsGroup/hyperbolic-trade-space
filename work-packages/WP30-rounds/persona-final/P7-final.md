# P7 final read (systems engineer, flight hardware), origin/dev 8806b0e, staged site 127.0.0.1:8791

Read, rendered in a browser (own tab): the paper body at /paper/ (Section 8 to 10, 12), Appendix C at /paper/supporting-material (C.1 to C.8, all tables), Figure 3 as drawn, examples/adcs/case-model.md, and model_v2/cubesat.sysml (headers, cost model, launch note, requirements). Not run: the code and the experiments.

Order of reading, stated plainly: the baseline file was opened by mistake in the same step as the sysml grep, before this first pass was written. The first-pass findings below were formed from the rendered pages and the model; the second pass (section 6) is the item-by-item comparison the brief asked for. Treat the first pass as lightly anchored.

## 1. What held my interest, what lost it

Held:
- Cost is now a traded axis and is built from parts. Unit cost and fleet cost are two of the thirteen metrics; each part has a 2026 listing behind it (panels 340,000 USD/m2, battery 70 USD/Wh, wheels 4,000 USD plus a torque term, tracker 150,000 USD.arcsec over accuracy), the assembly line is marked as having no source, and the shares and slopes of the learning curves are called choices. A unit cost of 207,000 to 663,000 USD for a 12U with launch inside it is the right order against the 275,000 USD platform listing the model cites. I could audit it without help.
- The cost is called a lower bound in the body and in C.8, with the list of what it leaves out (payload, communications, flight software, environmental test, licensing, ground, operations, broker fees). The sponsor's 8,000,000 USD against a covered 6,000,000 USD makes the lower bound a number, not a caveat.
- The baseline fails its own pointing requirement (0.0155 against 0.0085 degree) and the model says so with a negated satisfy. Lifelike.
- C.8 is a real list of what is missing, in a hardware engineer's words: schedule, qualification, fault tolerance, thermal, communications, growth allowance, constant 12 W load, momentum not accumulated or dumped, gains as trade variables, limits not flowed down from a mission. I found most of my objections already written.
- Figure 3 (rendered) is a SysML reading I can use: requirement to metric, with the slew measurement box saying "simulation here; field data when fielded". That line says what the abstraction is for.

Lost me:
- The toy statement sits in Appendix C.8 and in case-model.md. The paper body says the hardware values are "illustrative and not datasheet values" and that the cost is a lower bound; it does not say, where the findings are read, that feasibility has no margins, that momentum is one slew, or that the pointing error is controller plus tracker only. A reader who stops at Section 9 reads "pointing error" as a leading contending metric and "momentum headroom" as a contender with no warning.
- The pointing error is still controller steady state plus tracker accuracy. Its smallest value is 0.0006 degree (about 2 arcsec) and it is a leading metric of the K = 1 and K = 2 terms (Section 9). A flight team does not quote that number: alignment, roll-axis tracker error and wheel jitter dominate. C.8 does not list it.
- Momentum: the statement is there, but not what it voids. A constant disturbance accumulated over one orbit is about the small wheel's whole capacity, so "small wheel is feasible" is the first reading a flight engineer distrusts, and the momentum flag removes 540 designs.
- Launch: 7,000 USD/kg linear, with the 50 kg minimum slot noted in the model as "not modelled". For a fleet of one to three of these (12 to 16 kg each) the launch term is understated by up to 3.5x at a fleet of one, and fleet size is a design variable from 1 to 30. C.8 lists "the launch slot minimum" among exclusions, but not that it distorts the low end of the fleet-size axis.
- The wings go to 1.0 m per side, rigid, with no hinge mass and no flexible mode. Not listed.

## 2. Findings

Format: model says / real program / severity / does the case say toy?

N-F1. Pointing error is the loop plus the tracker only.
- Model: root-sum-square of the steady error (torque over Kp) and the tracker accuracy; range 0.0006 to 0.0173 degree; limit 0.0085 degree.
- Real: boresight alignment, thermal distortion, tracker roll-axis error and jitter dominate; 0.01 to 0.1 degree is typical for a good cubesat. A 2 arcsec total is not credible for a flight claim.
- Severity: would change before trusting a pointing reading. The metric leads the K = 1 and K = 2 terms.
- Toy: no. C.8 does not name it; the body says only "illustrative".

N-F2. Momentum is one slew, and the case does not say which reading that voids.
- Model: peak momentum in one 30 degree slew against the wheel capacity; no accumulation, no dump.
- Real: disturbance accumulation over an orbit is the dominant wheel-sizing driver; magnetorquers or thrusters dump it.
- Severity: would change before trusting any wheel-class reading (small wheel feasible; momentum headroom as a contender).
- Toy: yes in C.8 and case-model.md ("not accumulated or dumped"); not in the body.

N-F3. Launch cost has no slot minimum; the low end of the fleet-size axis is mispriced.
- Model: 7,000 USD/kg times total mass per satellite; a note in the model that a 50 kg minimum slot (350,000 USD) is not modelled.
- Real: one to three satellites of this class pay the slot; fleet of one is about 3.5x higher on launch.
- Severity: cosmetic for the method; would change before trusting a fleet-size or unit-cost reading at small fleets.
- Toy: partly. "launch slot minimum" is in the C.8 exclusion list; its effect on the fleet-size variable is not said.

N-F4. No margins; the feasibility boundary is nominal.
- Model: mass and power are nominal sums; no growth allowance, no battery fade or round-trip loss; depth of discharge 0.3 hard line.
- Real: concept budgets carry 15 to 30 percent growth and end-of-life battery derating; feasible sets shrink.
- Severity: would change before trusting the feasible-set size (2,134 of 3,000).
- Toy: yes (C.8: "no mass or power growth allowance"; case-model.md: "no battery fade or charge loss").

N-F5. Requirement limits read off the data, and the settled requirement is the horizon.
- Model: four limits from pass fractions, two cost budgets; settled means below 600 s.
- Real: limits flow down from a mission; 600 s for a 30 degree slew would not survive an agility review.
- Severity: breaks credibility if the reader asks where a requirement came from; the body's feasibility paragraph reads as if the six requirements were mission requirements.
- Toy: yes for the limits (C.8: "none is flowed down from a mission"); not for the 600 s horizon.

N-F6. Gains are trade variables and the slew law is a saturating PD.
- Model: Kp and Kd are two of seven variables; the "primary" regime is the aggressive gain box.
- Real: gains are tuned in software and cost nothing; slews are shaped profiles.
- Severity: would change before trusting; two of seven variables are a controls-design step.
- Toy: partly. C.8: "though a flight project would tune them in software". The slew law is not named as a choice.

N-F7. Rigid wings to 1.0 m, no hinge mass, no flexible mode.
- Real: first bending of a 1 m deployable wing sits near the high-gain loop bandwidth; hinges add mass.
- Severity: would change before trusting the large-panel, high-gain corner; cosmetic elsewhere.
- Toy: no.

N-F8. Constant 12 W load, no communications, thermal or payload duty cycle.
- Severity: would change before trusting the battery and power results; cosmetic for attitude.
- Toy: yes (C.8).

N-F9. Battery: continuous capacity, pack-level 140 Wh/kg, 1 C.
- Real: discrete cells; pack-level specific energy lower; peak-power rating matters.
- Severity: cosmetic.
- Toy: generic "illustrative" only.

N-F10. No fault tolerance, three wheels, no schedule or qualification.
- Severity: would change before trusting "cheapest feasible".
- Toy: yes (C.8).

N-F11. Total mass spans 11.9 to 16.3 kg with about 10.6 kg fixed.
- Honest reading of a bus-dominated spacecraft and visible in C.4 (log-spread 0.065); the body does not say the mass axis is a trim on a fixed bus.
- Severity: cosmetic.
- Toy: not stated.

N-F12. One orbit, one fixed 0.6 h eclipse, no altitude.
- Severity: cosmetic.
- Toy: yes in case-model.md ("One scenario"); not in the paper.

## 3. Would I trust the trade reading on my own program

No, and the paper does not ask me to. I would trust the form of the reading: a contending set with elasticities, read from a table I can regenerate, with a cost axis that is not a constant times mass. I would not use any ranking from this model; the three things that decide a flight bus here are pointing budget, momentum management and margins, and each is missing or nominal. What I would change, in order:
1. Replace the pointing error by an error budget (alignment, roll axis, jitter) or say in C.8 that it is the loop plus the tracker.
2. Add momentum accumulation over an orbit and a dump element, or state what its absence voids (small-wheel feasibility).
3. Price the launch slot minimum, or state that fleet sizes of one to three are mispriced.
4. Add a growth allowance and end-of-life battery derating, and re-run feasibility.
5. Move two sentences of C.8 into the body at the point the findings are read (see 4).
6. Mark the settled horizon and the slew law as choices.

## 4. Does the paper body carry more of the case than the demonstration needs

Somewhat. The body (Sections 8 and 9) carries: the six-requirement paragraph with the baseline failure (0.0155 against 0.0085, 63.7 percent of the stock regime passing), the 6,000,000 and 8,000,000 USD budgets, the MoE/MoP rule with the three MoEs named, the fitting temperature figures and Figure 3. For me the MoE/MoP sentence and the pass fraction do not earn their place in the body: the method's demonstration reads the requirements only in D.17 and in the "Requirements after the fit" paragraph. Figure 2 and Figure 3 are the SysML reading I value, and the paper is better with them, but they are the model, not the method; a reader who is not a systems engineer meets two case figures before the first result. The imbalance I would fix is the other direction: the body carries the case's realism claims (cost, requirements) and not its toy statements (margins, momentum, pointing); those are only in C.8. The body should carry one sentence naming what is nominal and where C.8 is.

## 5. Verdict on the hard requirement

Is the case realistic enough to keep a space-industry collaborator interested, and honest where it is a toy: Yes on interest, and mostly yes on honesty, with three residuals. Interest: the cost axis is now real and sourced, the baseline fails a requirement, and the model reads cleanly. Honesty: C.8 and case-model.md name most structural gaps in a hardware engineer's terms; what is missing is (a) the pointing error's optimism (N-F1, not listed), (b) what the momentum and launch-slot statements void (N-F2, N-F3), and (c) placement: the body does not carry the toy statements next to the findings that rest on them. Items a, b are a sentence each in C.8; c is a sentence in Section 8.

## 6. Second pass: each baseline finding

Evidence is a page and a sentence of the rendered paper or the case page.

| baseline | status | evidence |
|---|---|---|
| F1 cost axis is mass times a constant | resolved (cost); narrowed (launch structure) | Section 8: unit cost and fleet cost are two of the thirteen metrics, "the unit cost and the fleet cost from an analysis each" (Figure 3 caption). C.8: "launch is 7,000 USD per kilogram of the total mass"; the slot minimum is in the exclusion list ("the launch slot minimum and broker fees"). The linear structure remains; see N-F3. |
| F2 build cost outside the trade, low | resolved | C.8: "The part prices are 2026 vendor and marketplace listings; the assembly line ... has no source"; unit cost 207,000 to 663,000 USD (C.4). "each is a lower bound on a full costing" (Section 8). |
| F3 limits from the model's own output | narrowed to a toy statement | C.8: "Four requirement limits are read from the data's pass fractions and two are cost budgets; none is flowed down from a mission." The 600 s settled horizon is not named as a choice. |
| F4 no margins or growth | narrowed to a toy statement | C.8: "no mass or power growth allowance"; case-model.md: "Mass and power are nominal sums ... no battery fade or charge loss". Not in the body. |
| F5 momentum is one slew | narrowed to a toy statement | C.8: "Momentum is checked over one slew, not accumulated or dumped"; case-model.md: "no desaturation device exists". Still open: what it voids (N-F2). |
| F6 pointing error loop plus tracker only | still open | No sentence in the body, C.8 or case-model.md names alignment, roll axis or jitter. The metric still leads a term (Section 9). |
| F7 gains as trade variables; saturating PD | narrowed (gains); still open (slew law) | C.8: "the controller gains are trade variables though a flight project would tune them in software". The saturating PD is not named. |
| F8 rigid wings | still open | No mention of flexibility or hinge mass on any page read; wings still to 1.0 m (C.1). |
| F9 subsystems missing, constant 12 W | narrowed to a toy statement | C.8: "no thermal or communications model ... and a constant 12 W load"; the payload, communications and operations are named as outside the cost. |
| F10 battery model | still open (cosmetic) | No sentence on discrete cells, pack-level specific energy or cycle life in the paper; the cycle-life roll-up does not appear in the paper. Generic "illustrative". |
| F11 star tracker figures | narrowed to a toy statement | Section 8: "The hardware values of the case are illustrative and not datasheet values"; the tracker price is now tied to a listed unit. |
| F12 mass trade narrow | still open (cosmetic) | C.4 shows the log-spread of total mass at 0.065; no sentence says the mass axis is a trim on a fixed bus. |
| F13 wheel electrical model | narrowed to a toy statement | Same generic sentence as F11; no specific statement. |
| F14 no redundancy, no failure case | narrowed to a toy statement | C.8: "no fault tolerance", "no schedule or qualification". |
| F15 stakeholder layer thin | still open (cosmetic) | The sponsor appears with a budget (6,000,000 against 8,000,000 USD); launch provider, regulator and integration team are not named. |
| F16 no altitude, one fixed eclipse | narrowed to a toy statement (case page only) | case-model.md: "One scenario. One 30 degree slew in a 600 s horizon, one fixed 0.6 h eclipse of a LEO of about 95 minutes, no altitude." Not in the paper. |
| Baseline change 7: one paragraph on what the case leaves out | resolved, in the appendix | C.8 "What the case leaves out" is that paragraph; the body points to it only through "Section 12 says how to go beyond that". |
| Baseline change 8: what "verification" means | resolved on the case page; not in the paper | case-model.md: "'Verification' on this page is a solver checking a requirement on a configuration, not a hardware test." The paper's own "machine verification" (Section 10) is a different sense, explained there, and Figure 3 names "SlewVerification" without the gloss. |

Count: resolved 3 (F1 cost, F2, change 7) plus 1 on the case page only (change 8); narrowed to a toy statement 9 (F3, F4, F5, F9, F11, F13, F14, F16, and F7 gains); still open 5 (F6, F8, F10, F12, F15), of which F6 is the one that would change a reading.

# P7 baseline read (systems engineer, flight hardware), origin/dev 45180fd

Read: examples/adcs/case-model.md, model_v2/cubesat.sysml, model_v2/stakeholders.sysml, data/v2/*.csv (summary stats),
paper case section (Case construction, D.17) and Appendix C/D.17 prose. I did not run the code or open the rendered views; Appendix C tables are generated and I read only their prose. Figures and numbers below are from my own experience or from the files; where I am unsure I say so.

## 1. What held my interest, what lost it

Held:
- The header of cubesat.sysml says plainly "documentation of a demonstration, not an engineering model. Every number is illustrative ... never calibrated to hardware". I respect that; it is the right opening and it is repeated on the cost roll-ups and the launch rate.
- Every constant has a rationale beside it, units are carried (arcsec, N.m.s, Wh/kg), and the accounting is traceable: mass sum, power from flux x efficiency x packing x degradation x incidence, eclipse energy, DoD. This is how a first-pass budget sheet reads. I could audit it without help.
- A baseline that FAILS one of its own requirements (pointing 0.0155 vs 0.0085 deg) is lifelike; baselines fail requirements all the time and the model says so with a `not satisfy`.
- The battery C-rate requirement tying the pack to the slew's eclipse peak load is a real coupling (battery sized by peak power, not only energy). Good instinct.
- Part tables (wheel torque/momentum/mass, tracker accuracy/mass/power) are in the right class of numbers for COTS cubesat parts. I would not throw them out.

Lost me:
- Cost. The only cost in the trade is launch cost = 6,000 USD/kg x mass, which is the total-mass metric multiplied by a constant. Build cost exists in stakeholders.sysml but is "not a traded metric and no requirement reads it". So the trade has no cost axis; the thing that actually separates a 2-arcsec tracker from a 30-arcsec one (about 10x in price, per the case's own roll-up: 155k vs 15k USD) is excluded.
- Requirements are set from "the loop's ladder of pass fractions": limits chosen so that 90 to 95 percent of sampled designs pass. In a program the limit comes from the mission and the budget before the designs exist. Here the numbers (2.6 W, 0.008495 deg, 0.05922 N.m.s, 90,643 USD) are read off a distribution of the model's own output. Four-significant-figure limits tell a flight engineer the number came from the data, not the mission.
- No schedule, no lead time, no heritage/TRL, no vendor, no qualification. The model never asks "can I get it by the launch date".
- "Verification" here means a solver/engine checking a SysML constraint on a model. Hardware people hear verification as test/analysis/inspection/demonstration of built hardware. The case does not say which sense it means in the verification-case text I read.

## 2. Findings

Format: model says / real program / severity / does the case say toy?

F1. Cost axis is mass x constant.
- Model: launchCost = 6000 x totalMass; launch budget 90,643 USD = 15.107 kg. Range across data: about 71k to 96k USD.
- Real: a 12U is sold as a slot on a rideshare/dispenser (a fixed price by form factor, with a mass cap, e.g. 24 kg-class), so cost within the slot does not move with 0.5 kg of panel or battery; marginal mass has near-zero launch cost until you hit the cap, then a cliff. List rideshare price near 6k USD/kg is plausible for the order of magnitude (I am fairly, not fully, sure of current figures). The model states "increasing in mass" as a design choice.
- Severity: would change before trusting a trade reading. The total-mass vs launch-cost "MoE" pair is one axis dressed as two, and the cost trade is the one I would care about most.
- Toy flag: yes for the rate ("illustrative, not a cited price"). No for the linear-in-mass structure.

F2. Build cost is outside the trade and low in absolute terms.
- Model: bus 60k, panels 150k/m2, battery 50/Wh, antenna 15k, IMU 5k, wheel 8k + 2e6 x torque, tracker 5k + 300k/arcsec-accuracy. Baseline rolls to about 215k USD by my sum (rough; I did not run it).
- Real: flight-grade 12U bus hardware (structure, OBC, EPS, radio, ADCS) is typically several times that, and hardware is a minority of program cost; NRE, integration and test, ground segment, operations and labour dominate. Off by 3 to 5x on hardware and 10x or more on program cost. Not a stated target of the case.
- Severity: cosmetic if it stays a roll-up nobody reads; would change before trusting if cost is ever added to the trade.
- Toy flag: yes ("illustrative, never cited or calibrated").

F3. Requirement limits derived from the model's own output distribution.
- Model: four limits chosen from a pass-fraction ladder; settling requirement is "settling time < horizon (600 s)", so a design that takes 599 s to hold in a 0.3 deg band "passes".
- Real: limits flow down from a mission need (e.g. "slew 30 deg and hold within X s so that Y images per pass"). A settled requirement of 10 minutes for a 30 deg slew would not survive a review on an imaging or comms-pointing mission. The 2.6 W peak-slew-power limit is about 20 percent of the 12 W housekeeping load and is not a thing anyone budgets separately; it would sit inside the EPS peak-load line.
- Severity: breaks credibility for a reader who asks "where did this requirement come from"; the case is candid that it is the supervisor's choice from a ladder, which softens but does not fix.
- Toy flag: partly. It says "the supervisor's choice" and "illustrative"; it does not say "not mission-derived".

F4. No margins or growth allowance anywhere.
- Model: mass is a plain sum; power and energy are nominal; DoD limit 0.3 is a hard line.
- Real: concept-stage budgets carry mass and power growth allowances (commonly 15 to 30 percent at this maturity; I am citing practice, not a specific standard) and CBE vs maximum-expected values; battery sized for end-of-life capacity fade, charge/discharge efficiency (the energy balance has no round-trip loss) and heater load.
- Severity: would change before trusting. Feasibility boundaries (dod_ok, energy balance >= 0) move materially once a margin is applied; the data show energy balance min 1.0 Wh and dod up to 0.43, so many "feasible" designs would be rejected.
- Toy flag: no.

F5. Momentum is checked for one slew only; no accumulation or dumping.
- Model: momentum_ok = peak momentum in the slew <= wheel capacity. Disturbance torque 2e-6 N.m constant.
- Real: a constant 2e-6 N.m over one orbit (about 5,560 s from the orbital rate given) accumulates about 0.011 N.m.s, which is more than the small wheel's 0.010 N.m.s capacity. Cubesats carry magnetorquers (or thrusters) to dump momentum; there are none in the model, and no momentum-management requirement. The mission-length question (can the wheels survive the disturbance environment) is the dominant wheel-sizing driver in practice.
- Severity: would change before trusting a wheel-class reading; I would not trust "small wheel is feasible" without it. (Caveat: I am not certain 2e-6 is the right order for a 12U with wings at the unstated altitude; the altitude is not stated.)
- Toy flag: no. The gap is not named in the files I read.

F6. Pointing error is controller steady-state plus star tracker accuracy only.
- Model: RSS of 4(tau_gg + tau_dist)/Kp and the tracker 1-sigma. Range in data 0.0006 to 0.017 deg; limit 0.0085 deg (about 31 arcsec).
- Real: payload pointing budgets are dominated by alignment (tracker-to-payload boresight, thermal distortion, deployable settling), tracker cross-axis vs roll-axis accuracy (roll is several times worse), jitter from wheels, and sample-rate/latency effects. A claimed 2-arcsec-tracker design landing at 0.0006 deg total (about 2 arcsec) is not something a flight team would quote; 0.01 to 0.1 deg is typical for good cubesat systems (from memory, not verified here).
- Severity: would change before trusting the pointing metric (it spans 20x in the data, which is mostly Kp and tracker grade by construction).
- Toy flag: partly ("MoE: how well the payload points" is presented as the stakeholder's need but computed as a controller-plus-sensor quantity).

F7. Controller gains as trade variables, and a saturated PD for a 30 deg slew.
- Model: Kp, Kd are two of six configuration variables, sampled log-uniform; the loop is a PD law clipped at wheel torque; settling time 7 to 600 s; "stiff loop that asks for more torque than a wheel gives".
- Real: gains are software, tuned late and cheaply; they are not hardware trade variables, and they cost no mass, power or dollars (the case itself notes gains do not reach total mass). Slews are commanded with shaped (bang-bang/eigenaxis) profiles, not a saturating PD on a 30 deg error. Wheel-class differences in the results (large wheel median settle 22 s vs small 144 s in the aggressive-gain data) are partly an artifact of the saturated-PD choice.
- Severity: would change before trusting. Six variables, two of which are free tunes, give the fit a controller-tuning story rather than a hardware-trade story.
- Toy flag: no.

F8. Rigid-body only, with 1 m deployable wings.
- Model: panel span up to 1.0 m per wing x 0.34 m chord, thin-plate inertia, no flexibility. Natural frequency of the loop at the high-gain corner: with Kp 2 and X-inertia of order 1 kg.m2 (my estimate from the geometry, not run), wn is about 0.1 Hz.
- Real: wing first-bending modes of a 1 m deployable on a cubesat are typically a few tenths of a hertz to a hertz (my estimate, uncertain); a loop near that will excite them; deployment hinges also add mass and settling time that no entry reflects. Panel mass 2.5 kg/m2 has no hinge/mechanism mass.
- Severity: would change before trusting the agile and large-panel region; cosmetic elsewhere.
- Toy flag: no.

F9. Subsystems missing from a "12U cubesat" bus.
- Model: bus 10 kg lumps structure, avionics, harness; antenna 0.5 kg; 12 W "housekeeping and payload" constant. No comms/radio mass and power as a variable, no thermal, no propulsion, no deployer interface, no separate payload.
- Real: payload and comms power are duty-cycled and often dominate peak loads (a transmit burst of 20 to 40 W is typical for a 12U downlink; my recollection, not a spec). A constant 12 W erases the load profile that sizes the battery.
- Severity: would change before trusting the power/battery results; cosmetic for the attitude results.
- Toy flag: partly ("housekeeping and payload 12 W" is labelled illustrative).

F10. Battery model.
- Model: continuous capacity 20 to 200 Wh at 140 Wh/kg, 1 C discharge, DoD limit 0.3, cycle life 10,000 x (0.3/DoD), one cycle per orbit.
- Real: packs are built of discrete cells (a few Wh each), so capacity is quantized by series/parallel counts; 140 Wh/kg is a cell-level number, pack-level with protection and structure is lower (I would expect roughly 100 to 120 but am not certain). Cycle life at 30 percent DoD in LEO is usually quoted several times higher than 10,000 (several tens of thousands); the roll-up's implied life of order 2 years at 0.3 DoD (10,000 orbits at about 15/day is under 2 years, my arithmetic) looks short by about 2 to 3x. Cycle life is mostly temperature- and charge-rate-dependent.
- Severity: cosmetic for the trade; the effective-life roll-up is unused.
- Toy flag: yes for the life rule ("not a cited life").

F11. Star tracker figures.
- Model: coarse 30 arcsec / 0.15 kg / 0.4 W; medium 10 arcsec / 0.35 kg / 0.9 W; fine 2 arcsec / 0.90 kg / 1.5 W.
- Real: cubesat trackers at about 10 to 30 arcsec are commonly well under 0.15 kg at 0.5 to 1 W. Arcsec-class trackers exist but are typically larger and draw more power than 1.5 W; I am not certain of the figures. Mass monotone in accuracy is right in direction.
- Severity: cosmetic. Toy flag: yes (illustrative, "public component classes").

F12. Mass trade is narrow.
- Model: total mass 11.9 to 16.1 kg, with 10.6 kg of it fixed (bus, antenna, IMU).
- Real: that is the correct reading of a bus-dominated spacecraft, and honest. But it means the "mass" metric moves under 35 percent across the space; any mass-cost "trade" is a trim on a fixed bus.
- Severity: cosmetic, but relevant to the cost point in F1.
- Toy flag: not stated.

F13. Wheel electrical model.
- Model: loss = 5e4 x torque^2 (same coefficient all classes), idle 0.3 W per wheel; usable torque capped by available power; wheel torque limit ignores speed/back-EMF and wheel-speed saturation.
- Real: wheel power is dominated by drag/bearing and by tau x omega at speed; idle power rises with stored momentum; 0.3 W idle is plausible for a small wheel and low for a 100 mN.m.s class. Peak slew power ranges 1.3 to 7.4 W, probably low-to-OK order of magnitude.
- Severity: cosmetic. Toy flag: yes (labelled illustrative).

F14. Three wheels, no redundancy, no failure case.
- Model: three identical orthogonal wheels, single tracker.
- Real: a four-wheel skew configuration or a single-fault-tolerant ADCS is a common reliability requirement for a mission that matters; reliability, availability and fault tolerance are absent from the stakeholder layer (it has a sponsor and an operator, price and performance).
- Severity: would change before trusting any conclusion about "cheapest feasible". Toy flag: no.

F15. Stakeholder layer thin on the people who gate a flight.
- Model: sponsor (price, life), operator (performance). Verdicts are `satisfy`/`not satisfy` per named configuration.
- Real: the stakeholders who actually reshape a bus are the launch provider (mass cap, CG limits, vibration environment, orbital-debris end-of-life rule), the range/regulator (frequency, deorbit), and the integration and test team. None appears. Roll-ups (build cost, effective life) are computed but "read by no output".
- Severity: cosmetic for a method demonstrator; would change before trusting a "what a stakeholder wants" reading.
- Toy flag: partly (the file calls the roll-ups illustrative).

F16. No orbital lifetime or altitude.
- Model: orbital rate 1.13e-3 rad/s (about 93-minute period), eclipse 0.6 h, no altitude stated; 1 m wings imply drag area.
- Real: altitude drives drag torque, disturbance torque, eclipse fraction, deorbit time and radiation. Eclipse 0.6 h (36 min) is near the maximum for such an orbit, not a mean, and beta angle changes it; a single fixed eclipse is a worst-case choice not labelled as such.
- Severity: cosmetic. Toy flag: not stated.

## 3. Figures and structure off by more than 2x, or not matching practice

Off by more than 2x (my judgement; not independently verified):
- Build cost, hardware: baseline about 215k USD (by my sum from the stakeholders file, not run) against several times that for flight-grade 12U hardware (3 to 5x); program cost 10x or more.
- Battery cycle life: about 10,000 cycles at 0.3 DoD (roll-up only, not traded) vs commonly several-fold higher for LEO Li-ion at that DoD.
- Settling requirement: 600 s horizon for a 30 deg slew; typical requirement for a pointing mission is in the tens of seconds. Data median settling is 101 s (aggressive gains' median 52 s). Off by more than 2x for any mission needing agility.
- Momentum: disturbance accumulation in one orbit (about 0.011 N.m.s at the stated 2e-6 N.m) already exceeds the small wheel's 0.010 N.m.s capacity; the model has no accumulation check. (This is a structure gap, not a number gap.)
- Pointing error as low as 0.0006 deg (about 2 arcsec) from tracker alone; practice shows alignment and roll-axis terms dominating by 5 to 10x (from memory).

Structure not matching practice:
- Launch cost linear in mass; practice is a stepped price by slot with a mass cap.
- No cost in the trade; no schedule, TRL, lead time or heritage.
- No margins, no growth allowance, no CBE vs max-expected.
- Gains as design variables; PD saturation as the slew law.
- Constant payload+housekeeping load; no duty cycle.
- Requirements derived from pass fractions of the model's own sample.
- No momentum dumping hardware or requirement; no fault tolerance.
- "Verification" is solver/engine checking of a model, not hardware test; the word needs to be disambiguated for my audience.

Numbers I would leave alone (plausible order of magnitude): 12U envelope and 10 kg bus fraction, 24 kg-class cap not stated but total 12 to 16 kg is in range; panel yield about 120 W/m2 averaged; 12 W load; 20 to 200 Wh battery; wheel torque and momentum classes; orbit period; 0.6 h eclipse as a worst case; 6k USD/kg order of magnitude.

## 4. What I would change first, in order

1. Make cost a traded metric: put build cost (wheel, tracker, panel, battery) in the table so the trade has a cost axis, and replace the linear-in-mass launch cost with a stepped slot price plus a mass cap. State that the dollar constants are placeholders.
2. Derive each requirement from a stated mission need before looking at the data, or say in one sentence next to each limit that it is a pass-fraction choice and not a flow-down.
3. Add margin: a growth allowance on mass and power, and end-of-life battery derating and efficiency; re-run feasibility.
4. Add momentum accumulation over an orbit (or a mission) and a dump or desaturation element, or state that it is out.
5. Treat gains as fixed or tuned per configuration (a software step), not as two of six trade variables; or say that this is the controls-design step in the loop.
6. Replace the constant 12 W with a load profile (at least a peak and an average).
7. State what the case leaves out in one paragraph in the case section (thermal, comms, propulsion, flexibility, alignment, reliability, schedule), so I know where it is a toy.
8. Say what "verification" means in the model vs in a hardware campaign, once, in the case-model page.

## 5. The standing question: is this realistic enough to keep you interested, and where it is a toy, does it say so?

Partly. Interested: yes, for about a day, for two reasons: the budgets are transparent enough to audit without help and the numbers are the right order of magnitude for the parts and the power system; the baseline failing its own requirement and the "illustrative, not calibrated" statements read honestly. Where it loses me is the shape of the trade, not the numbers: no cost axis worth the name, requirements read off the model's own output, no margins, no momentum accumulation, controller gains traded as if hardware, and nothing on schedule, qualification or fault tolerance. On "does it say so": the constants are labelled illustrative everywhere, and the header says "not an engineering model", which is more than most. What it does not say is which structures are missing (the F1, F3, F4, F5, F7, F14 items); a reader with flight experience will find those in the first hour and wonder whether they were noticed. As a method demonstrator I would keep reading; as a stand-in for how a bus is traded I would not rely on any ranking from it.

Not done or uncertain: I did not run code or view rendered figures; numbers for real-world parts are from memory and flagged where unsure; I read Appendix C prose but not its generated tables.

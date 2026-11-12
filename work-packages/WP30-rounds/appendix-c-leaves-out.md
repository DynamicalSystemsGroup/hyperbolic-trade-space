# What the case leaves out: the final wording (Appendix C paragraph and the case page list)

The paper's Appendix C carries the paragraph; the case page (`examples/adcs/case-model.md` and the Examples page) carries the list.
Both say the same things, and each item is checked against `examples/adcs/model_v2/cubesat.sysml` (the lines named below).
The triage draft is `persona-baseline/triage.md`, "Class 3 texts"; this file replaces it where they differ (the cost coverage
now reads as the model's own `COVERAGE` text and the supervisor's exclusion order; the limits sentence names both kinds of limit).

## Appendix C paragraph (about 120 words)

> **What the case leaves out.** The model is a demonstration and its numbers are illustrative. Its cost is a lower bound on a full
> costing: it covers the bus (structure, power, radios and computer), the attitude-control parts, assembly and test, and wholesale
> launch, and leaves out the payload and its instruments, communications, flight software, environmental testing beyond the
> assembly line, licensing, a ground station network and operations, the launch slot minimum and broker fees. It has no schedule or
> qualification, no fault tolerance, no thermal or communications model, no mass or power growth allowance and a constant 12 W load.
> Momentum is checked over one slew, not accumulated or dumped, and the controller gains are trade variables though a flight
> project would tune them in software. Four requirement limits are read from the data's pass fractions and two are cost budgets;
> none is flowed down from a mission.

> What each omission does to a reading of the case (the list that follows the paragraph in C.8; the case page carries the
> pointing error, momentum, launch slot and scenario items below, in its own words):
> - **Pointing error.** The closed-form steady error summed in quadrature with the tracker's accuracy; its smallest value, 0.0006
>   degree, is a loop-and-tracker figure; alignment, the roll axis and jitter are not modelled.
> - **Momentum.** One slew against the wheel's capacity: that the small wheel is feasible is a one-slew reading.
> - **Launch.** The 50 kg slot (350,000 USD) is not a cost; understated 3.1 to 4.2 times at one satellite, 1.5 to 2.1 at two, at
>   most 1.4 at three (computed from the feasible designs' total mass, `tests/test_paper.py`).
> - **Scenario.** The 600 s horizon and the saturating proportional-derivative slew law are choices.
> - **Structure.** Rigid wings, no hinge mass; 1.3 to 5.7 kg of traded parts on about 10.6 kg of fixed bus.

## The list for the case page

Place after "The requirements and what each reads" and before "Coverage"; one clause at its head, then the list.

> ### What the case leaves out
> "Verification" on this page is a solver checking a requirement on a configuration, not a hardware test. The case does not model:
> - **Cost beyond a lower bound.** The unit cost and the fleet cost cover the bus (structure, power, radios and computer), the
>   attitude-control parts, assembly and test, and wholesale launch; they leave out the payload and its instruments,
>   communications and the payload interface, flight software, environmental testing beyond the assembly line, licensing, a ground
>   station network and operations, the launch slot minimum and broker fees. The fleet cost requirement holds the covered cost under
>   6,000,000 USD, inside the sponsor's full budget of 8,000,000 USD, the rest being the allowance for what is not covered.
> - **Schedule, lead time, heritage, qualification.** No attribute or requirement reads any of them.
> - **Fault tolerance.** Three identical wheels and one tracker; no failure case.
> - **Thermal, communications, load profile.** None modelled; payload and radio power sit inside one constant 12 W load.
> - **Margins and growth.** Mass and power are nominal sums; solar degradation is one fixed factor (0.9); no battery fade or charge loss.
> - **Pointing error.** It is the closed-form steady error with the star tracker's accuracy, summed in quadrature; boresight
>   alignment, the tracker's roll axis and wheel jitter are not modelled, so its smallest value, 0.0006 degree, is not a flight claim.
> - **Momentum management.** `momentum_ok` compares one slew's peak momentum with the wheel's capacity; the constant disturbance
>   torque is not accumulated over an orbit and no desaturation device exists, so that the small wheel is feasible is a one-slew
>   reading and not a sizing.
> - **Launch slot.** The 50 kg minimum slot (350,000 USD) is a note in the model and not a cost: a fleet of one to three pays it, so
>   the launch cost is understated by 3.1 to 4.2 times at one satellite and the low end of the fleet-size axis is underpriced.
> - **Gains as hardware.** Kp and Kd are traded like parts, though a flight project tunes them in software.
> - **One scenario.** One 30 degree slew in a 600 s horizon under a saturating proportional-derivative law (both choices of the case), one fixed 0.6 h eclipse of a LEO of about 95 minutes, no altitude.
> - **Requirement limits from a mission.** Four limits (peak slew power, pointing error, control effort, launch budget) are the
>   supervisor's choices from the data's ladder of pass fractions; the two cost limits are budget figures; none is flowed down
>   from a mission.

## Where each item is backed (`examples/adcs/model_v2/cubesat.sysml`)

| item | backing in the model file |
|---|---|
| cost coverage and its order of exclusions | the `COVERAGE` text of the cost model's doc (line 396 onwards) and of `UnitCostRequirement` and `FleetCostRequirement`; launch 7,000 USD/kg, slot minimum "not modelled" in `launchRate`'s doc |
| 6,000,000 inside 8,000,000 USD | `fleetCostLimit` (`6.0e6`) and its doc, `FleetCostRequirement`'s doc; the decision record of 2026-11-11, 10:30 |
| no schedule, no fault tolerance, no thermal or communications | no attribute, calc or requirement of those names; the three wheels are one `ReactionWheel` part with the idle power "3 x 0.3 W" of the header (line 1073) |
| constant 12 W load | `Environment` loads doc ("housekeeping and payload 12 W", line 236) and `BaseLoad` |
| one fixed degradation factor, one eclipse | `degradation = 0.9`, `eclipseDuration = 0.6 [h]`, "LEO of about 95 minutes" (lines 223 to 234) |
| momentum over one slew, no desaturation | `MomentumRequirement` and the measured peak momentum; no desaturation element in the file |
| limits from pass fractions and budgets | `Budgets` docs (the ladder rows and shares admitted; the cost limits as the supervisor's values) |

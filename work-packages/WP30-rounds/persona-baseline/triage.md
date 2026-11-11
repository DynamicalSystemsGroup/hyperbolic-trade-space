# P7 and P8 baseline reads: triage (head 0171ae7)

Classes: **1** answered by the model revision (WP30 decisions: the cost axis, "Stage 3b questions", "The supervisor's values",
"The assistant's calls on the spike D2 readout"; unit 350,000 USD, fleet 6,000,000 USD, launch 7,000 USD/kg). **2** defect in a
number: fixed. **3** the up-front statement of what the case leaves out (one Appendix C paragraph, one list on the case page).
**4** design choice that stays; where stated, or the one clause to add. **5** out of scope, no action. The high-level rule
(PM-BRIEF, 09:40) holds: the body gets nothing beyond a pointer.

| finding | class | disposition | owner / unit |
|---|---|---|---|
| P7 F1 cost is mass x constant | 1 | Answered: build and fleet cost traded, launch 7,000 USD/kg. Residual: launch stays linear; the 50 kg slot minimum is noted in the requirement's text, not modelled (call D) | model developer, WP30 |
| P7 F2 build cost outside the trade, low | 1 | Answered: build priced on 2026 sources, traded; coverage statement says lower bound on a full costing (hardware only, no NRE, ops) | model developer, WP30 |
| P7 F3 limits read off the data | 4 | Stated: `case-model.md` "The requirements" ("the supervisor's choice from the loop's ladder of pass fractions") and Appendix D.17 "read after the fit". Add the one clause "not flowed down from a mission" in the class 3 paragraph | Appendix C unit |
| P7 F4 no margins or growth | 3 | List item "Margins and growth" | case page unit |
| P7 F5 momentum one slew, no dumping | 3 | List item "Momentum" | case page unit |
| P7 F6 pointing = controller + tracker only | 5 | Flight alignment, roll-axis and jitter terms are flight realism the demonstration need not carry; the metric is already defined as computed from the loop and the tracker | none |
| P7 F7 gains as variables; saturated PD | 3 + 5 | List item "Gains". Shaped slew profiles: flight realism, no action | case page unit |
| P7 F8 rigid body, wings | 5 | Flexibility is flight realism; the paragraph's "illustrative" covers it | none |
| P7 F9 missing subsystems, constant 12 W | 3 | List items "Thermal, communications and load" | case page unit |
| P7 F10 battery cells, cycle life | 5 | Roll-up unused, labelled "not a cited life"; no action | none |
| P7 F11 star tracker figures | 5 | Labelled illustrative, cosmetic | none |
| P7 F12 mass trade narrow | 5 | An honest reading of a bus-dominated craft; the cost axis (F1) now carries the trade | none |
| P7 F13 wheel electrical model | 5 | Labelled illustrative, cosmetic | none |
| P7 F14 no redundancy or failure case | 3 | List item "Fault tolerance" | case page unit |
| P7 F15 thin stakeholder layer | 1 + 5 | Build cost is now read by a requirement, so "computed, read by no output" no longer holds for it. Launch provider, regulator and test team: flight realism, no action | none |
| P7 F16 no altitude, one eclipse | 3 | List item "One scenario" (eclipse fixed at 0.6 h, no altitude). The model header says "LEO of about 95 minutes"; no further action | case page unit |
| P7 (unnumbered, change 8) sense of "verification" | 4 | One clause at the head of the case page list: verification here is a solver checking a requirement on a configuration, not a hardware test | case page unit |
| P8 F1 no cost or schedule axis | 1 | Cost answered; schedule goes in the list. "Examples page and docs index do not say it": the pointer in class 3 covers it | model developer; case page unit |
| P8 F2 mass leads through equal log-spread | 4 | Conditioning "defines the question" is in the methods prose; adding the caveat beside the result is body growth. Where the exponent is read in kg or USD, Appendix C may state the spread at 7,000 USD/kg (4 kg is about 28,000 USD); no body edit | Appendix D unit, if at all |
| P8 F3 no candidate meets the requirements | 4 + 2 | The failing baseline is deliberate and stated. A compliant named candidate is new body content: a supervisor question, not done here. Side effect: the "meets the requirements" table moves when the data regenerate (two more requirements, new limits); regenerate, do not retype | supervisor; WP30 gate |
| P8 F4 requirement prices in bands | 1 (partial) | Cost columns now exist, so a requirement's price can be read in USD. Residual: D.17 still prices in bands; a worked conversion is one sentence in D.17 if the supervisor wants it | Appendix D unit |
| P8 F5 uniform sampling, no vendor discreteness | 4 | Stated: "worked example of design optimization, not a study" (Appendix C job) | none |
| P8 F6 one scenario | 3 | List item "One scenario" | case page unit |
| P8 F7 Examples vs paper three-term numbers | 2 | Verdict below | docs unit |
| P8 F8 no fleet | 1 | Answered: fleet size is a variable and the fleet cost is traded. Residual: no shared-launch packing | model developer, WP30 |
| P8 F9 executive cannot follow log V | 5 | Translation is the journeys work (WP33), not a case-model matter; the paper's honesty sentences are credited, no action | WP33 |

## F7: which page is of record

The paper is. `uv run python examples/adcs/k_terms.py` (primary regime, run at head) prints two tables.

- **Each K's own temperature** (tau = 113.22 at K = 3): contending sets of 4, 5 and 5 metrics, shares 0.034, 0.241, 0.724 (3, 24 and
  72 percent). Same as the paper's cell (`paper/paper.ipynb`, "The term shares are 0.03, 0.24 and 0.72") and the K record pinned in
  `tests/test_case.py` (from line 293).
- **The one-term temperature** (tau = 38.1, the "DIAGNOSTIC, fixed tau" table): sets of 5, 4 and 5, shares 0.167, 0.105, 0.728 (17, 10
  and 73 percent).

`docs/examples.md` lines 16 to 20 is the second table. It is labelled ("At the one-term temperature"), and its slack figures (0.243 to
0.132 to 0.088) are correctly fixed-tau, the like-for-like comparison. The sets and shares are not the ones the paper reports, and
a reader sees two answers to "three terms". The paper's sets are the finding of record.

**Change** (`docs/examples.md`, lines 18 to 20 only): keep the slack sentence at the one-term temperature; give the sets and shares
at each K's own temperature: sets of 4, 5 and 5 metrics, shares 3, 24 and 72 percent; the largest term alone contains peak slew
power, the smallest alone contains control effort, and the middle term is the one-term contending set (all three claims hold in the
re-selected table: term 3, term 1, term 2 respectively). Do not edit now: both pages' numbers move at the WP30 regeneration (eleven
metrics), so the sentence should be written from the regenerated record, with a test pinning it beside the existing K record.

## Class 3 texts (drafts)

**Appendix C paragraph** (`paper/supporting_material.ipynb`, after cell `app-C-job`; about 95 words). Net-neutral offset: delete the
"This appendix carries" bullet of that cell, which restates the section list the reader is about to see.

> **What the case leaves out.** The model is a demonstration and its numbers are illustrative. Its cost covers the attitude-control,
> power and structure parts, assembly and launch, a lower bound on a full cost. It has no schedule or qualification, no fault
> tolerance, no thermal or communications model, no mass or power growth allowance and a constant 12 W load. Momentum is checked over
> one slew, not accumulated or dumped, and the controller gains are trade variables though a flight program would tune them in
> software. The requirement limits are read from the data's pass fractions, not flowed down from a mission.

The cost sentence is true once the revision lands (WP30 coverage statement); it is wrong at head, where cost is launch alone.

**Case page list** (`examples/adcs/case-model.md`, after "The requirements and what each reads", before "Coverage"; about 150 words).
Each item checked against `model_v2/cubesat.sysml` at head.

> ### What the case leaves out
> "Verification" on this page is a solver checking a requirement on a configuration, not a hardware test. The case does not model:
> - **Schedule, lead time, heritage, qualification.** No attribute or requirement reads any of them.
> - **Fault tolerance.** Three identical wheels and one tracker; no failure case.
> - **Thermal, communications, load profile.** None modelled; payload and radio power sit inside one constant 12 W load.
> - **Margins and growth.** Mass and power are nominal sums; solar degradation is one fixed factor; no battery fade or charge loss.
> - **Momentum management.** `momentum_ok` compares one slew's peak momentum with the wheel's capacity; the constant disturbance torque
>   is not accumulated over an orbit and no desaturation device exists.
> - **Gains as hardware.** Kp and Kd are traded like parts; they reach the performance metrics but not the mass (below, "Coverage").
> - **One scenario.** One 30 degree slew in a 600 s horizon, one fixed 0.6 h eclipse, no altitude.

"No altitude" and "0.6 h" are the Environment's doc and attributes; "not the mass" is the case page's own statement (line 203).

## What the cost and fleet revision answers

Answers: P7 F1, F2, F15 (build cost read); P8 F1 (cost), F4 (partly), F8. Touches P7 F12 and P8 F2 (mass is no longer the only price).
Residual after the revision: linear launch with no slot cliff or integration fee; hardware-only cost (no NRE, operations, ground); assembly
at 100,000 USD unsourced; no schedule; no shared-launch packing; requirement prices in D.17 still in bands; the fleet limit (6,000,000 USD) is
a call against his stated 1,000,000 USD, flagged for his revert; the unit limit (350,000 USD) was chosen on the earlier calibration.

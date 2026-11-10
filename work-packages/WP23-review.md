# WP23 — Review record (the model-realism loop)

Scope: `WP23-scope-of-work.md`; decisions: `WP23-decisions.md`. The modeller stream writes this record as
it goes; the PM and the driver add the cold reads, the K = 1 and K = 3 readings and the gate items. The
model under review is `examples/adcs/model_v2/cubesat_r2.sysml` (D-1), beside the adopted
`cubesat.sysml` until the data gate.

## Proposed thresholds (for the supervisor at the data gate)

The supervisor's direction (OD3 to OD6, 2026-11-09, 21:10): "Loop proposes, you approve". The loop
proposes one rule for all four thresholds, so that no threshold is tuned to one metric or to a figure:
each is the baseline configuration's own value with a 20 % margin (the allowance an engineer carries on
a budget at an early phase; illustrative, like the model's other constants). In the model the four
limits are expressions of the baseline (`part budgets : Budgets`, `margin = 1.2`), not typed numbers;
the values below are read from the model by `tests/test_system_model_v2.py`
(`test_r2_proposed_thresholds_are_the_baselines_values_with_the_stated_margin`). If the supervisor
gives other values, they replace the expressions by literals.

| Metric (requirement) | Baseline value | Margin | Proposed threshold | Value taken from |
|---|---|---|---|---|
| pointing error (`PointingErrorRequirement`, `PointingError(c) <= budgets.pointingErrorLimit`) | 0.015535 degree (`PointingError(cubesatBaseline)`: medium tracker 10 arcsec, Kp 0.03) | 1.2 | 0.018642 degree | the baseline's calc, times the margin |
| control effort (`ControlEffortRequirement`, `controlEffort <= budgets.controlEffortLimit`) | 0.0094906 N.m.s (`baselineMeasurement.controlEffort`, the recorded slew) | 1.2 | 0.011389 N.m.s | the recorded baseline measurement, times the margin |
| peak slew power (`PeakSlewPowerRequirement`, `PeakSlewPower(c, peakTorque) <= budgets.peakSlewPowerLimit`) | 2.0 W (`PeakSlewPower(cubesatBaseline, baselineMeasurement.peakTorque)`: tracker 0.9 W, idle wheels 0.9 W, loss at 2 mN.m 0.2 W) | 1.2 | 2.4 W | the baseline's calc at its recorded peak torque, times the margin |
| total mass through the launch cost (`LaunchBudgetRequirement`, `c.launchCost <= budgets.launchBudget`) | 79,748.57 USD (13.2914 kg at 6000 USD/kg) | 1.2 | 95,698.29 USD (15.950 kg at the rate) | the baseline's launch cost, times the margin |

The two numeric literals the revision introduces (R-3; every other number in the diff is in a `doc` or a
comment, or is the model's `1.0 [unit]` normalisation idiom):

| Literal | Element | Rationale (illustrative, proposed) |
|---|---|---|
| `6000.0` USD/kg | `environment.launchRate` | a round figure at the order of magnitude of published small-satellite rideshare list prices to low Earth orbit; not a cited price (OD1: illustrative) |
| `1.2` | `budgets.margin` | the one 20 % margin above the baseline's value, for all four thresholds |

Where each proposed threshold binds over the declared ranges (read from the model's named configurations
and its ranges; a finding, not a tuning):

- Launch budget 95,698 USD is 15.950 kg at the rate. The agile configuration (15.66 kg) passes; the
  heaviest configuration of the declared ranges (large wheels, fine tracker, 1.0 m panels, 200 Wh:
  16.43 kg, 98,571 USD) fails. The budget binds in the heavy corner only.
- Peak slew power 2.4 W: with the medium tracker (0.9 W) and the idle wheels (0.9 W) the budget leaves
  0.6 W of wheel loss, a peak torque of 3.5 mN.m (5e4 x tau^2), so a saturating medium wheel (2 mN.m,
  0.2 W) passes and a saturating large wheel (10 mN.m, 5 W of loss) fails by a factor of about three;
  with the fine tracker (1.5 W) the tracker and the idle wheels use the budget up and any wheel loss
  exceeds it. With the baseline's recorded peak torque (2 mN.m) as the default, the agile
  configuration's verdict is `violated` (2.6 W); its own slew would be measured at the gate.
- Pointing error 0.018642 degree: in the aggressive gain box (Kp from 0.2) the steady error is at most
  a fifth of the baseline's and the tracker floor at most 0.0083 degree, so no configuration of the
  primary dataset's box exceeds it; in the baseline box the coarse tracker at Kp 0.03 gives
  0.0174 degree, which passes. The requirement is a stated bound that the declared space meets.
- Control effort 0.011389 N.m.s: measured; where it binds is read from the regenerated data at the
  gate.

None of these thresholds enters the dataset: the four flags of the data stay what they are (settled,
momentum_ok, power_ok, dod_ok), so a threshold cannot move the heatmap or any fit; it changes the model's
statement, the views and the coverage table only.

## MoE/MoP classification

The rule stated in the model's top comment: an MoE (measure of effectiveness) is a measure a
stakeholder states without knowing the design; an MoP (measure of performance) is a measure of the
system's performance under the scenario the engineer states. Each mark is the first word of the `doc`
on the metric's own element (the calc def the analysis returns, the measurement attribute, or the
`totalMass` attribute of `Cubesat`), so a reader of the model and a program read the same mark.

| Traded metric | Mark | Element | Rationale |
|---|---|---|---|
| settling time | MoP | `SlewMeasurement.settlingTime` | the response of the attitude loop to the nominal slew: the engineer's scenario, measured |
| pointing error | MoE | `calc def PointingError` | how well the payload points: the payload's need, stated without knowing the design |
| total mass | MoP | `Cubesat.totalMass` | the launch mass of the configuration; the stakeholder's measure on it is the launch cost (the MoE `calc def LaunchCost`, not traded: OD2, "MoE on mass, no new column") |
| control effort | MoP | `SlewMeasurement.controlEffort` | what the slew asks of the wheels under the scenario |
| power margin | MoP | `calc def PowerMargin` | the power system's margin at the peak of the scenario's slew |
| energy balance | MoP | `calc def EnergyBalance` | the orbit's energy account under the stated orbit and eclipse |
| eclipse reserve | MoP | `calc def EclipseReserve` | the battery's reserve through the stated eclipse |
| peak slew power | MoP | `calc def PeakSlewPower` | the electrical draw at the peak of the scenario's slew |
| depth of discharge | MoP | `calc def DepthOfDischarge` | the battery's cycling under the stated eclipse demand |

Two MoEs (pointing and launch cost) and eight MoPs: the model's stakeholders ask for a payload that
points and a launch they can afford; everything else is how the engineer's design performs under the
engineer's scenario. The P2 proxy reads this classification in the round's cold read.

## Coverage findings

The table: `examples/adcs/model_v2/views/coverage.md` (and `.csv`), generated by
`examples/adcs/model_v2/coverage.py` from `cubesat_r2.sysml`; the test `tests/test_model_coverage.py`.
The structural column walks the model through the opensysml client (calc invocations, attribute
reads, the redefinitions that bind a part's attribute to a root variable, the measurement's stated
simulator inputs); the empirical column changes each decision element one at a time at the three
named configurations through the oracle (tunes by a factor 1.1, swaps to the next level; an effect
counted above 1e-9 relative). The oracle at `dev` reads the adopted model; r2 keeps every calculation
of it (pinned by `test_r2_keeps_every_calculation_of_the_adopted_model`), so the column holds for both.

- **R-1 holds.** Every decision element has a non-empty row in both columns: the two swaps and the
  four tunes each reach at least one traded metric structurally and move at least one empirically.
  The slew's measurement reads every configuration input, so the settling time and the control effort
  depend on all six; the mass accounting has no gain in it (Kp, Kd do not reach the total mass) and the
  pointing error's closed form has Kp but not Kd: the walk reads the model, not a typed map.
- **Seven disagreements, one cause.** Structural yes, empirical no, for `peak slew power` and `power
  margin` against `panelSpan` (peak slew power only), `batteryCapacity`, `Kp` and `Kd`. Both metrics
  read the measured peak torque, which structurally depends on every simulator input (the gains, the
  inertia through the battery and panel masses, the torque cap through the available power). At all
  three named configurations the wheels saturate at their class's maximum torque and the power cap
  does not bind (`UsableWheelTorque` is the class maximum when the available power allows it: at the
  baseline 36 W of available power allows 15.5 mN.m against the medium wheel's 2 mN.m), so the measured
  peak torque is the wheel class's and nothing else moves it; the largest relative change is exactly 0.
  The structural column states the worst case the model allows (a configuration whose panels cannot
  feed the wheels, or whose loop never saturates, would show the effect); the empirical column states
  what the three named configurations do. Disposition: a finding recorded, not a model change; the
  seven cells are pinned in the test (`EXPECTED_DISAGREEMENTS`) so a change in either column is seen.
- **R-2 holds.** Every traded metric is marked (two MoEs: pointing error and, through the total mass,
  the launch cost; eight MoPs) and has a requirement that reads its own quantity, verified in
  `ConfigurationVerification` (pointing error, total mass through the launch cost) or
  `SlewVerification` (the rest); the second table of `coverage.md` lists them.
- Small effects worth a reader's eye: the wheel class and the battery move the pointing error only
  through the gravity-gradient torque (relative changes 1.8e-5 and 9.9e-7), real in the model and
  negligible against the disturbance torque; the panel span moves the eclipse reserve only through
  the slew loss energy (8.2e-5).

## Round 1 model change

The revision `cubesat_r2.sysml` against the adopted `cubesat.sysml` (D-1; the adopted file and the
frozen data untouched until the gate):

- Every traded metric marked MoE or MoP in the `doc` of its element (table above).
- Launch cost: `environment.launchRate` (6000 USD/kg, illustrative), `calc def LaunchCost` (rate times
  total mass, increasing in mass; marked MoE), `Cubesat.launchCost`, `LaunchBudgetRequirement` reading
  it, satisfied by the baseline and verified in `ConfigurationVerification`. No dataset column (OD2).
- The four metrics without a requirement now have one, each on its own quantity:
  `PointingErrorRequirement` (configuration only), `ControlEffortRequirement` (measured),
  `PeakSlewPowerRequirement` (measured peak torque), `LaunchBudgetRequirement` (configuration only);
  thresholds in `part budgets : Budgets` as expressions of the baseline (table above).
- Slew time leaves: `SlewTimeRequirement` and `SlewBandRequirement` fold into `SettledRequirement`
  (its doc states the fold; the settling time is the hold time, the last exit from the settling band by
  event detection, WP16); the measurement loses `slewTime` and `censored`; the scenario loses
  `slewBandSensitivity`; `SlewExperiment` loses `in censored`. Nine traded metrics: settling time
  (measured, passed through) and the eight the analysis returns in order (pointing error, total mass,
  control effort, power margin, energy balance, eclipse reserve, peak slew power, depth of discharge).
  `SlewMeasurement`'s doc states the inputs the simulator reads from the configuration, the environment
  and the scenario.
- Kept unchanged, by name, everything the case code reads from the model (`experiments/cubesat_oracle.py`,
  `feasibility.py`, `exclusion.py`, `compare.py`): the enumerations, the alternatives, `designRanges`,
  the gain boxes, `nominalSlew.{slewAngle, horizon, timeStep, slewBand, settlingFraction}`, the
  `Cubesat` attributes and parts, `environment.*`, the four flag requirements and their `in`
  parameters, `SlewLossEnergy`, `SlewExperiment`'s other inputs and its return tuple, the closed-form
  calcs of section 4 (`SlewTimeEstimate`, `IsTorqueLimited` and their parts keep their WP15 names: the
  comparison code reads them; R-5's grep of the gate model will find `SlewTime` in those names, an item
  for the PM).
- Interface items for the case-code stream (the oracle at `dev` runs on the adopted model, not on r2, so
  nothing breaks before the gate): the runtime refuses an unknown named argument, so `_analyse` must stop
  passing `censored` to `SlewExperiment`; `ModelReader.scenario` must stop reading
  `slewBandSensitivity`; `feasibility.SLEW_BAND_REQUIREMENT` and `slew_band_entered` have no requirement
  to read; `_measure_slew`'s `slew_time`, `slew_time_sensitivity` and `censored` leave with the column.
- Every calc def of the adopted model keeps its body in r2 and the eight computed attributes agree on
  the three named configurations (`test_r2_keeps_every_calculation_of_the_adopted_model`), so the
  revision changes no accounting: the empirical coverage column computed through the oracle on the
  adopted model (unit 2) holds for r2.
- Gates (R-11), both models: strict load, `self_check` holds, every `satisfy` holds (9 adopted, 11 r2,
  engine `run`, observed), toolkit `check` exit 0, `lint` 0 errors 0 warnings, `verify --solve` exit 0
  with 0 violated. `tests/test_system_model_v2.py` and `tests/test_model_checking_v2.py` are
  parametrized over the two models.
- The two views of r2 (D-5, D-6): `work-packages/WP23-rounds/round-1/` (`assembly_view`,
  `behavioural_view`, `.puml`, `.svg`, `.png`; the intent of each in `INTENT.md`), by the views
  generator revised (revision 3): the metric list is the CaseSpec's filtered to the metrics the model
  carries (r2 has no slew time), each metric's box carries its MoE or MoP mark, and a calc the model
  marks MoE that is not itself traded (the launch cost) is drawn between the requirement that reads
  it and the metric it reads. A strong line now means the requirement invokes the metric's own calc
  (or the calc of its attribute), not a calc the metric's calc invokes: on r2 the old rule would have
  drawn `PeakSlewPowerRequirement` to the power margin because `PowerMargin` calls `PeakSlewPower`.
  On the adopted model the generator's output is byte for byte the committed views, so the pinned
  views test stands. Read from the image: the behavioural view has no dashed "no requirement" box
  (R-2), every label is legible at 700 px and nothing overlaps; the assembly view is the adopted
  model's (the configuration space is unchanged). The views stay out of `examples/adcs/model_v2/views/`
  until the gate.

## R-5's check, amended

The closed-form calcs of section 4, `TorqueLimitedSlewTime`, `LinearSlewTime`, `SlewTimeEstimate` and
`IsTorqueLimited`, stay in the scenario section as the model-checking evidence of WP15: they estimate
the time the slew takes to enter the band, a physical quantity of the scenario, not a traded metric, a
measurement or a requirement, and the comparison code reads them by name. R-5's grep for `SlewTime` is
therefore read over the measurement (`SlewMeasurement`), the requirements (section 5) and the
experiment's outputs (`SlewExperiment`), where it finds nothing (`test_r2_slew_time_has_left_the_
measurement_and_the_requirements`), and not over section 4. The PM has recorded this reading for the
driver.

## Glossary entries (unit 3): drafted, held

Three entries were drafted for `glossary.yaml` in the file's own style (`moe`, `mop`, `launch-cost`;
the text below) and withdrawn before commit: the vocabulary tool reads the paper notebooks, `docs/*.md`,
`docs/user-guide/*.md`, `site/index.html`, `README.md` and the `src/` docstrings, and none of those
uses the three terms yet (the case prose of `examples/adcs/case-model.md`, D-7, is not in the tool's
corpus), so each entry is a `dead-entry` violation and `tests/test_vocabulary.py`'s repository guard
goes red. The entries go in with the first prose use in the corpus (the paper's case section after the
gate, or a docs page), or with a baseline row owned by WP23 if the PM prefers them in now; the tool
also reports two violations already on `dev` before this round (`src/hyperbolic_trade_space/plotting.py`,
"fitted surface", an `avoid` and a `stem`; commit 3d6d48a), not this package's.

```yaml
  - id: 'moe'
    term: 'MoE'
    short: 'Measure of effectiveness: a measure of how well a system serves its purpose that a stakeholder states without knowing the design; here the pointing error and the launch cost.'
    register: 'MoE'
    formal: 'a metric a stakeholder states on the system in use, independent of the design'
    not: 'an MoP, which measures the system''s performance under the engineer''s scenario'
    defined_in: 'cubesat_r2.sysml (the mark in the doc of the metric''s element); WP23-review.md'
    aliases:
      - 'MoEs'
      - 'measure of effectiveness'

  - id: 'mop'
    term: 'MoP'
    short: 'Measure of performance: a measure of a system''s performance under the scenario the engineer states; here the settling time, the total mass, the control effort, the power margin, the energy balance, the eclipse reserve, the peak slew power, the depth of discharge.'
    register: 'MoP'
    formal: 'a metric of the system''s performance under a stated scenario'
    not: 'an MoE, which a stakeholder states without knowing the design'
    defined_in: 'cubesat_r2.sysml (the mark in the doc of the metric''s element); WP23-review.md'
    aliases:
      - 'MoPs'
      - 'measure of performance'

  - id: 'launch-cost'
    term: 'launch cost'
    short: 'The launch rate, an illustrative USD per kilogram, times the total mass; the MoE the model ties to the total mass, read by the launch-budget requirement; not a traded metric and not a dataset column.'
    register: 'launch cost'
    formal: 'rate times total mass, increasing in mass'
    not: 'a traded metric or a dataset column; a cited launch price'
    defined_in: 'cubesat_r2.sysml (calc def LaunchCost, LaunchBudgetRequirement); WP23-decisions.md OD1, OD2'
```

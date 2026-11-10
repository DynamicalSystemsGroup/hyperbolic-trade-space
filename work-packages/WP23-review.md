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
| `1.0` 1/h (round 2) | `environment.batteryDischargeRate` | a continuous discharge rating of 1 C, the pack delivering its capacity in one hour, the plain rating of a small-satellite lithium-ion pack; the pack's peak power is this rate times its capacity (`BatteryPeakPower`); not a cited rating. Where it binds: "Round 2" below |

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

The round's cold reads, verbatim with each finding's disposition: `WP23-rounds/round-1/cold-reads.md`
("Rounds: the cold reads and their dispositions" below).

## Round 2: the battery coupling

The supervisor's input (`WP23-decisions.md`, 22:05 and 22:15): "maybe we should have 2 to 3 battery
options with different weights, storage capacities, peak charge rate and peak power" so that the model
"provides a fully coupled set of paths from the config values to the metrics of interest without
missing anything that is obviously coupled"; "fully coupled" meaning a connected graph of coupling
variables between subsystems, not all-to-all. The round assessed three options from the model and the
physics it already states (a battery's own ratings; no new physics), then decided on the evidence.

**What the battery reaches today** (`coverage.md`, tables 1 and 3). `batteryCapacity` feeds the power
subsystem alone, through `battery.capacity`; from there the pack mass `battery.mass` (the capacity over
the specific energy) is a coupling variable into the mass accounting, so the capacity reaches the total
mass and the launch cost; the capacity is read by `EclipseDemand`, `DepthOfDischarge` and
`EclipseReserve`, so it reaches the depth of discharge and the eclipse reserve; through the structure
mass and the inertias it reaches the slew, so the settling time and the control effort (relative
changes 5.9e-3 and 1.9e-3 at a 10 % change) and, structurally, the peak torque and so the power margin
and the peak slew power (empirically 0: the wheels saturate; "Coverage findings"). What the model did
not state: the pack's own ratings. A battery delivers at most its rated power; in eclipse it alone
carries the housekeeping load and the slew's peak draw. That path, capacity to the slew's peak draw,
is the obviously coupled one that was missing.

**The three options.**

- (a) *A battery swap*: two or three alternatives, each with a mass, a capacity, a peak charge rate and
  a peak power. Couples: the swap reaches the total mass and the launch cost (mass), the depth of
  discharge and the eclipse reserve (capacity), and the rating requirement (peak power), the same
  metric set the capacity tune reaches today, since the pack mass already follows from the capacity
  through the specific energy; the new information is one specific energy per alternative, which the
  data would see as three levels of the mass-to-capacity ratio in place of one. Costs: a categorical
  configuration column (the contract's `contract_version` + 1 for an added column; the sampler in
  `cubesat_model.py`; the oracle's `configure`; the CaseSpec's covariates in `case.py`; the paper's
  configuration-space slots, "two swaps, four tunes" becoming three and the assembly view redrawn);
  the case-code stream and WP19's slot decisions, not this package's loop.
- (b) *A derived battery peak power with a requirement*: the pack's peak power is a discharge rating
  (a C-rate, 1/h) times the capacity, and a requirement reads the eclipse peak load (the housekeeping
  load plus the peak slew power) against it. Couples: the capacity to the slew's peak draw through
  the model's own calcs (`battery.capacity` -> `BatteryPeakPower`; `peakTorque` from the controls ->
  `PeakSlewPower` -> `EclipsePeakLoad`; the requirement reads both). No new column, no change to the
  dataset, the flags, the contract or the paper's slots; one new constant with its rationale.
- (c) *Both*: (a)'s costs plus (b).

**Decision: (b).** The general test is that every configuration value has its obviously coupled paths
to the metrics present in the model. The battery's paths to the metrics are present (mass and launch
cost, depth of discharge, eclipse reserve, the slew through the pack mass); the one missing coupling
was the pack's rating against the slew's peak draw, and that is a bound on quantities the model already
computes, which one rating closes with no new column. (a) adds a column and its downstream costs for a
coupling the metrics already carry; it changes the configuration space rather than the evaluation of
it, which is a problem change for the supervisor at the gate, not a round of the loop.

**Implemented in `cubesat_r2.sysml`** (round 2; the adopted model and the frozen data untouched):
`environment.batteryDischargeRate = 1.0` (1/h; the literal in the thresholds table above);
`calc def BatteryPeakPower` (rate times capacity, W) and `calc def EclipsePeakLoad` (housekeeping plus
`PeakSlewPower`), neither traded; `BatteryPeakPowerRequirement` (`EclipsePeakLoad(c, peakTorque) <=
BatteryPeakPower(c)`, the measured peak torque as its `in`), satisfied by the baseline and verified in
`SlewVerification`. Twelve `satisfy` statements, all holding (engine `run`). The model is 871 lines;
the r2 pins of `tests/test_system_model_v2.py` carry the two calcs and a cap of 900.

**Where it binds** (read from the model; a finding, not a tuning). Pack peak power at 1 C: baseline
80 W, agile 140 W, compact 40 W. Eclipse peak load at the recorded baseline torque: 14.0, 14.6 and
13.5 W; at each class's maximum torque: 14.0, 19.4 and 13.3 W. The largest load the declared space
allows is 19.4 W (fine tracker 1.5 W, idle wheels 0.9 W, housekeeping 12 W, a large wheel saturating
at 10 mN.m: 5 W of loss) and the smallest pack is 20 Wh, 20 W: the requirement holds over the whole
declared space, by 0.6 W in that corner. A pack rated 0.5 C would need 38.8 Wh for the same corner
(19.4 W over 0.5 1/h). The rating is not set to bind: 1 C is the plain continuous rating; what it says
is that the smallest packs of the range carry the most agile slews with little to spare, and the
coverage table shows the path. None of this enters the dataset.

**Left for the gate (OD7).** The second rating the supervisor named, the peak charge rate: a charge
acceptance (a C-rate times the capacity) against the array's sunlit surplus (`GeneratedPower -
BaseLoad`) would tie the capacity to the panel span through a requirement, binding where a small pack
meets large panels (a 20 Wh pack at 0.5 C accepts 10 W against a surplus of up to 67 W at 1.0 m
panels). It bounds no traded metric and adds a second rating constant; it is listed here as a
candidate for his decision, not added in the loop.

**The coupling table** (unit 1; `coverage.md`, third table; `coverage.py`, `Coupling` and
`SUBSYSTEM_OF`). The design structure matrix of the MDAO literature (XDSM form): the configuration
values feed the subsystems' calcs, the subsystems exchange named coupling variables, the metrics and
the requirements are read off the subsystems. The three subsystems are the behavioural view's
(`controls`, `power and energy`, `mass`); which calc belongs to which is the analyst's decomposition,
stated once in `coverage.py`; every cell is read from the model. Read from the table:

- Configuration values to subsystems: `WheelClass` feeds the controls (`momentumCapacity`, that is
  `wheel.maxMomentum`), the power subsystem (`wheel.maxTorque`) and the mass accounting
  (`wheel.mass`); `TrackerGrade` the three likewise (`tracker.accuracy`, `tracker.power`,
  `tracker.mass`); `panelSpan` the power subsystem (`panelPlus.span`, `panelMinus.span`), the mass
  accounting (`panelPlus.span`, the inertia's geometry) and the slew (`panelPlus.span`, a simulator
  input); `batteryCapacity` the power subsystem alone (`battery.capacity`); `Kp` and `Kd` the controls
  alone (`controller.Kp`, `controller.Kd`).
- Coupling variables between subsystems: controls to power and energy, `peakTorque` and
  `torqueSquaredIntegral` (the measured slew into `PeakSlewPower`, `PowerMargin`, `EclipsePeakLoad`
  and `SlewLossEnergy`); power and energy to controls, `usableWheelTorque` (the torque cap the slew
  reads) and `panelPlus.mass`; power and energy to mass, `battery.mass`, `panelPlus.mass`,
  `panelMinus.mass`; mass to controls, `structureMass` and `InertiaX`, `InertiaY`, `InertiaZ`
  (the slew's inputs and the gravity-gradient torque). Mass feeds the power subsystem nothing and the
  controls feed the mass accounting nothing: the mass accounting reads configuration attributes only.
- Metrics read off: controls, settling time, pointing error, control effort; power and energy, power
  margin, energy balance, eclipse reserve, peak slew power, depth of discharge; mass, total mass
  (with the launch cost, its MoE). Requirements read off each subsystem likewise, twelve in all.
- Connectivity (the test `tests/test_model_coverage.py`): every configuration value feeds at least
  one subsystem and reaches at least one traded metric (by the structural column of table 1: the
  swaps, the panel span and the battery reach all nine; `Kp` eight, not the total mass; `Kd` seven,
  not the total mass or the pointing error); every metric is read off a subsystem; the graph of
  configuration values, subsystems and metrics is connected (18 nodes, 25 edges); no configuration
  value reaches nothing. The controls and the power subsystem feed each other (cells on both sides
  of the diagonal); the model resolves that loop in one pass, since the torque cap is a quantity of
  the configuration computed before the slew and the peak torque is read after it.
- The matrix is coarser than table 1: a subsystem two configuration values feed does not pass each of
  them to every metric it reads off (the gains reach the controls, not the mass accounting through
  them), so the per-metric reach is table 1's structural column, and the matrix states which
  subsystems exchange which variables. The coupling variables are pinned by name in the test
  (`EXPECTED_COUPLING`), so a model change that adds or removes one is seen.

**The views of round 2** (`work-packages/WP23-rounds/round-2/`, `INTENT.md`): the assembly view's
PlantUML is byte for byte round 1's (no configuration variable added); the behavioural view differs by
one box, `BatteryPeakPowerRequirement` in the dashed group of requirements with no line to a traded
metric (it bounds the eclipse peak load by the pack's rating, like the power requirement bounds the
available power), satisfied by the baseline and verified in `SlewVerification`. Read from the image:
every label legible at 700 px, nothing overlaps, the three subsystems and their metrics as in round 1.
The views generator is unchanged.

**Tests touched.** `tests/test_model_coverage.py` (unit 1: the connectivity tests, the three-table
CSV); `tests/test_system_model_v2.py` (the r2 pins: the calcs `BatteryPeakPower` and
`EclipsePeakLoad`, the line cap 900); `tests/test_model_checking_v2.py` (the r2 pins follow the
round-2 model: the requirement set, `satisfy` twelve, the `SlewVerification` set; the PM's
authorization, option (i) of the round-2 report).

**Legibility finding for the gate's figure redraw** (the PM's note; not fixed here). The round-1
heatmap draws the total mass's K = 1 exponent, 0.358, above the colourbar's cap of 0.30 as saturated
black, so the cap hides the largest value on the figure; the drawing is `case.tau_sweep_figure`'s,
read-only for WP23 (non-goals: no figure in `paper/`), so the cap is an item for the redraw after the
data gate (WP19): a cap at or above the largest exponent, or a scale that states its clipping.

## Coverage table, platform stability

The Linux run on `dev` (1501c53) failed `tests/test_model_coverage.py::test_committed_table_equals_a_full_regeneration_three_times`:
three Linux regenerations agreed with each other and not with the committed `coverage.md`. Interrogated
in `hts-paper` (image `57a0f23716f4`, linux/arm64, the worktree copied into a container `hts-wp23r3`
and removed after): the container's table against the committed one (generated on the Mac) differs
in four cells of the empirical column's magnitudes and in no yes/no, no structural cell, no
disagreement, no row of the metrics or the coupling tables.

| cell | committed (Mac) | container | raw cause |
|---|---|---|---|
| WheelClass -> settling time | 2.344e+01 | 2.341e+01 | settling times differ by up to 0.4 s between platforms (agile, large wheel: 342.97 s against 342.56 s) |
| panelSpan -> settling time | 1.276e-01 | 1.277e-01 | the same |
| batteryCapacity -> settling time | 5.852e-03 | 9.132e-03 | the agile configuration's settling time 14.0358 s against 14.0359 s, its battery-changed one 13.954 s against 13.908 s: a 0.05 s effect read on a grid that moves by that much |
| batteryCapacity -> energy balance | 7.801e-07 | 7.799e-07 | the raw energy balances differ by 2e-10 relative; a relative change of 7.8e-07 between two such values carries that noise in its fourth digit |

The cause. The settling time is `res.t[outside[-1]]`, the time of the last sample of the RK45 grid at
which the error exceeds the settling fraction (`experiments/cubesat_oracle.py`, `_last_outside`); the
grid is the adaptive step controller's, whose step sizes follow error estimates that differ between
the platforms' maths libraries in their last bits, so the sample times differ by up to a step
(`adcs_sim` states it: "settling time is quantized by `max_step`"). The raw differences over the 21
slews behind the column: settling time up to 4.9e-3 relative (0.4 s); control effort 1.6e-5; energy
balance, eclipse reserve and depth of discharge below 9e-10; pointing error, total mass, power margin
and peak slew power exactly 0 (configuration-only quantities, and the peak torque is the wheel
class's clipped maximum on both). Not a tie, not an ordering, not a one-at-a-time effect near the
1e-9 bound: the seven zero cells are exactly zero on both platforms and the smallest non-zero effect
(7.8e-07) is three orders above it, so the yes/no pattern and the disagreements are platform-stable;
what is not stable is a relative change between two settling times, which can differ in its first
digit when the effect of a 10 % tune (0.05 s on the agile configuration) is the size of the grid's
own movement.

The fix, in two parts, neither a tolerance. (1) Printing: the CSV printed the magnitudes to four
significant digits (`.3e`), beyond their stability for the slew's quantities (the three cells of the
fourth digit); it now prints two, as the Markdown table did, and the table's note states what the
settling time's column means (an order of magnitude, not a value). (2) The environment-of-record
rule (`paper/container/README.md`, `tests/_env.py`): the committed `coverage.md` and `coverage.csv` are
the container's, regenerated inside `hts-paper` `57a0f23716f4` on the model as round 2 left it
(two container runs byte-identical), committed with this section; the test asserts byte equality
only under `HTS_ENVIRONMENT_OF_RECORD=1` (the image sets it) and elsewhere asserts the structure:
the rows and columns, every structural cell, the empirical yes/no pattern and the disagreements, the
metrics table and the coupling table byte for byte, and prints the magnitudes that differ without
asserting them. Run: in the container with the variable set, 14 passed; in the container with it
unset, the structural path, no differing magnitude; on the Mac, 35 passed (with
`tests/test_check_script.py`), one differing magnitude printed (`batteryCapacity -> settling time`:
9.1e-03 of record, 5.9e-03 here); on the Mac with the variable forced to 1 the exact assertion
fails on that cell, as the rule expects off the record. `exact_only` was not used because it needs a
name in `paper/environment_values.toml`, a file outside this package's blast radius; `of_record()`
is the test's switch, as in `tests/test_soft_fit.py`; listing the table there is an item for the PM.

What the cell means for the modeller: the battery's effect on the agile configuration's settling time
is one step of the integrator's grid, below the measurement's resolution; the table's statement
"the battery moves the settling time" rests on the baseline and compact configurations (relative
changes 2.4e-3 and 1.2e-3 of record, 0.43 s and 0.08 s), not on the agile one.

## Round 3: the three metrics that never bind

The driver's focus from round 1: in the primary regime's K = 1 fit the power margin, the eclipse
reserve and the peak slew power have exponent zero at every temperature of the sweep (round 1's
`heatmap.png` and `k3_record.md`: 1.45e-17, 0 and 0 at the selected tau 38.1; in the baseline regime
only the peak slew power is at zero across tau, the power margin contends there with 0.178), and the
coverage table shows the gains, the battery and the panel span moving neither the peak slew power nor
the power margin at the three named configurations. Interrogated before any change, from the model
and the round-1 data (1000 designs per regime; 706 feasible in the primary regime, 780 in the
baseline), with the model's own constants.

**(a) Do the design ranges ever make power scarce?** No, at the slew's peak; yes, in eclipse energy,
and the flag already removes those designs.

- Power margin over the 1000 designs of the primary regime: minimum 6.57 W, first percentile 7.64,
  median 28.5, maximum 68.0 W; none below its requirement's zero (`power_ok` 1.000 in both regimes);
  none within 10 % of it. The three smallest margins are large wheels with the fine tracker at 0.30
  to 0.31 m of span (available power 11.2 W, peak slew power 6.1 to 6.3 W). The margin follows the
  panel span alone: Spearman 0.99 with the span, 0.04 with the battery, 0.01 with either gain; a
  straight line on the span explains 98 % of its variance. The generated power runs from 24.5 W at
  0.3 m to 81.7 W at 1.0 m against a housekeeping load of 12 W and a peak slew draw of 1.3 to 7.4 W.
- Eclipse reserve: minimum -2.59 Wh, fifth percentile -1.47, median 10.5, maximum 52.0 Wh; 13.1 % of
  designs negative, and those are exactly the `dod_ok` failures, because the reserve
  (0.3 C - D) and the depth of discharge (D / C) are the same inequality against their thresholds;
  5.0 % of designs sit within 1.05 Wh above zero. Among the feasible designs it is a function of the
  battery capacity and the tracker grade: the eclipse demand D is 7.98 to 8.68 Wh (the base load of
  13.3 to 14.4 W over 0.6 h; the slew loss energy at most 0.55 % of it), so the reserve is
  0.3 C less about 8.3 Wh; Spearman 1.00 with the battery, below 0.05 with everything else.
- Together (small panel, small battery, aggressive gains): the gains enter neither quantity
  measurably (|Spearman| at most 0.03; the slew energy is below 0.55 % of the eclipse demand), the
  battery does not enter the margin (0.04) and the span does not enter the reserve (0.03); each
  quantity is driven by one tune. The corner (0.30 m, 20 Wh, Kp 2) has a margin of about 6.6 W and a
  reserve of about -2.3 Wh: power at the slew's peak is never scarce in the declared ranges; eclipse
  energy is, for packs below 26.6 to 28.9 Wh by tracker grade, and the flag removes those designs before the fit.

**(b) Is the slew power-limited anywhere?** In a thin corner. The usable torque falls below the class
cap in 3.2 % of designs (10.3 % of the large-wheel designs), all with a span of at most 0.341 m: the
large wheel's cap of 10 mN.m needs 15 W of available power (3 x 5e4 x 1e-4), which 0.34 m of span
supplies; the medium cap needs 0.6 W and the small 13.5 mW, always available. Read back from the peak
slew power, the peak torque sits at the class cap in 96.8 % of the primary regime's designs and at
the power-limited usable torque in the other 3.2 %, unsaturated in none; in the baseline regime
90.4 %, 1.9 % and 7.7 % unsaturated (large wheels at the box's low gains: 24.8 % of them never reach
the cap). The wheel's torque cap is the limit; the power cap takes over only for large wheels below
0.34 m of span.

**(c) Are the three defined so that nothing in the configuration space moves them?** Two are
carried by another traded metric and one is a step function of the swaps.

- Peak slew power is the tracker's power plus the idle wheels (0.9 W) plus 5e4 x peakTorque^2. With
  the peak torque at the class cap it takes one value per wheel class and tracker grade: 1.3045,
  1.8045, 2.4045 W (small); 1.5, 2.0, 2.6 W (medium); 6.3, 6.8, 7.4 W (large). In the data every
  medium and small cell has exactly one value and only the large-wheel cells vary (the power-limited
  corner): 41 distinct values in the primary regime's 1000 designs, 34 among the feasible 706. A
  class constant plus a class constant: a step function of the two swaps, flat inside each of the
  nine cells, and across the cells ordered as the total mass is (Spearman 0.87 among the feasible
  designs; the heavy wheel draws the power).
- Power margin and energy balance are both affine in the generated power, which is proportional to
  the span (Pearson 0.986 and 0.999 with the generated power; between them Spearman 0.98, Pearson of
  the logs 0.96): a near-collinear pair, one instantaneous at the slew's peak in sunlight, one
  integrated over the orbit.
- Eclipse reserve and depth of discharge are one quantity: Spearman -0.9994 over the feasible designs,
  -1.0000 within a tracker grade.

**The n-lemma reading of each zero exponent** (for the case prose, D-7; `docs/theory.md`,
"Elasticities and the n-lemma": the K = 1 fit is one monomial term, a hyperplane in log-metric space,
whose exponents are the sparse solution of a linear program at tau = infinity and its soft version at
the fit temperature; a metric carries weight only where it trades against the others at the
frontier).

- *Eclipse reserve*: zero because the depth of discharge carries it. Given the tracker, the two are
  monotone functions of one capacity, so they cannot both contend; the fit gives the depth of
  discharge 0.158 and the reserve 0 (primary), 0.012 and 3.7e-4 (baseline). A collinearity in the
  data, not an absence of binding: the reserve binds as a flag on 13 % of the designs before the fit.
- *Power margin*: zero in the primary regime because the energy balance carries it (0.184); both are
  affine in the generated power. In the baseline regime the fit carries the power margin (0.178)
  and nearly drops the energy balance (0.019). Which of a near-collinear pair carries the weight is
  the linear program's choice, and that it changes between the regimes is the sign of the
  collinearity. At K = 3 in the baseline regime the two sit in different terms (term 2 power margin
  0.083; terms 1 and 3 energy balance 0.074 and 0.347).
- *Peak slew power*: zero at K = 1 because one hyperplane over all nine cells can use no elasticity
  from a metric that is flat inside each cell, and across the cells the metric orders the designs as
  the total mass does, which has the largest exponent (0.358). At K = 3 it leads a term in both
  regimes (primary term 3: 0.612; baseline term 2: 0.428, in a 6-lemma with the pointing error, the
  total mass, the power margin, the settling time and the depth of discharge): with three terms one
  cell is the large-wheel designs, where the 5 W draw trades against the settling time (Spearman
  -0.63 with it among the feasible designs: the large wheels slew fastest and draw most).

**Model change in round 3: none.** The rule was to change the model only where the system's purpose
justifies it, never for texture.

- A realistic power budget the system would have: the margin as defined leaves out the battery's
  recharge in sunlight (the eclipse demand over the 0.945 h sunlit arc, 8.4 to 9.2 W). Taking it into
  the margin would subtract a near-constant (the demand depends on the tracker, not on the span or
  the battery), turn 3.1 % of the feasible designs negative (large wheels at small spans) and leave
  the margin collinear with the energy balance as before: it would move no exponent for a reason the
  system has. Listed with the peak charge rate (round 2) as a candidate for the supervisor at the
  gate (OD7), not made.
- A saturation the system would have: the model has both, the class cap and the power cap through
  `UsableWheelTorque`, and the data shows which binds where (b). Nothing to add.
- The two collinearities are findings about the traded-metric set (two metrics for one eclipse
  quantity; two for one generated power), which is the contract's and the supervisor's to change
  (OD7, the gate), not the loop's.

Consequences for the record: the model is round 2's, so the coverage table, the coupling matrix and
the committed views of the round stand as unit 1 of this round left them (regenerated in `hts-paper`
on this model); the toolkit gates (R-11) were re-run on it: `REQUIRE_OPENSYSML=1 uv run pytest -q tests/test_model_checking_v2.py tests/test_system_model_v2.py tests/test_system_model_v2_r1.py tests/test_model_coverage.py`, 185 passed. One number for the supervisor's
threshold popup: the proposed peak-slew-power limit of 2.4 W (the baseline's 2.0 W times 1.2) fails
every large-wheel design, the medium wheel with the fine tracker (2.6 W) and the small wheel with the
fine tracker by 4.5 mW (2.4045 W): 56.4 % of the primary regime's feasible designs; it enters no
dataset column.

**The views of round 3** (`work-packages/WP23-rounds/round-3/`, `INTENT.md`, which now carries
what the legend carried and an intent sentence for the heatmap). The generator's revision 4
(`project.py --revision 4`; the default stays 3 and reproduces the committed views of the adopted
model byte for byte, `tests/test_system_model_v2_r1.py`, 14 passed) applies the round-1 cold reads'
dispositions: the legend cut to the colour key; one colour rule (orange requirement, green traded
metric, yellow derived and not traded) with MoE/MoP by stereotype only; the requirement boxes
reduced to the name and the verification case (the `requirement def`, `satisfy cubesatBaseline`
boilerplate, the same in every box, moved to the caption; the generator prints the satisfying
configuration again if the model makes them differ); the three requirements that read no traded
metric carry their `require constraint` in the model's words; the requirement-metric line is
headless (a shared quantity) and only the source arrows have heads; the lanes are titled as the
analyst's grouping; the assembly legend names the untagged parts as fixed and gives the gain ranges
per regime (primary, baseline; the regime of each gain box read from `experiments/definitions.py`).

Legibility, measured rather than judged: the first revision-4 render put the type at 5.8 px at
700 px (round 2: 6.9 px, which the cold reads called illegible), because the orphan group laid out
diagonally at the top right and the mass lane's extra rank made the natural width about 1450 px.
Three layout changes, tested on the PlantUML text and then put in the generator, bring it to 9.3 px:
the element a requirement reads is written in the metric's box (its calc or measured attribute, as
table 2 of `coverage.md` names it) and the line carries no label, so the ranks sit closer; the
launch-cost box sits at the metrics' rank beside the total mass (a same-rank line), so the mass
lane adds no rank; the orphan group hangs off the last lane and spans the lanes' width. The assembly
view's type is 9.0 px. Both images were read at native resolution after the render; nothing
overlaps. The naming rule: "primary" and "baseline" regime throughout the round's records and views;
`k3_record.md` and `heatmap_stock.png` still say "stock" because `case.py`'s CaseSpec keys the
baseline regime so and `diagnostic_pair.py` prints that key, both outside this round's blast radius
(an item for the PM).

The round's cold reads, verbatim with each finding's disposition: `WP23-rounds/round-3/cold-reads.md`
("Rounds: the cold reads and their dispositions" below).

## Round 4: the round-3 dispositions

The round-3 cold reads (a fresh P2 and a fresh P3) found nothing that blocks. The model is unchanged
(round 2's); the round executes the PM's five dispositions on the views, the pair generator and the
names, and records what each cold-read finding was and what changed. The folder is
`work-packages/WP23-rounds/round-4/` (`INTENT.md`, `README.md`); the generator is
`project.py --revision 5` (the default stays 3 and reproduces the committed views of the adopted
model byte for byte; revision 4 reproduces round 3's text byte for byte: `tests/test_system_model_v2_r1.py`,
14 passed).

**1. The behavioural view's mass chain.** Finding: the chain requirement -> launch cost -> total mass
was carried by a stub of about 5 px between two stacked boxes, and a cold reader missed it. Three
drawings were measured at 700 px by the type they leave (the SVG's font size; round 3: 9.3 px):
a label on each of the two lines, 8.6 px, because a label on a line between ranks widens the whole
layout; the two boxes side by side (an extra rank), 7.0 px; a label on the short line only, 9.2 px.
Changed: the line from the launch cost to the total mass carries the element the two share,
`totalMass`, and the gap between boxes at one rank (PlantUML `nodesep`) is 16 for revision 5 (8 in
round 3), which lengthens that line to about 30 px with the label beside it and costs height (910 px
against 867), not width; the requirement's line to the launch-cost box stays unlabelled, since it
lands on the box that names `LaunchCost`. The dashed group's title: finding, light grey at what
read as the smallest type; measured, it was body size already (9.3 px, bold) in grey `#808080`.
Changed: "requirements that read no traded metric", in black. The P2's question why the pointing
error is the one «MoE» among the metrics: the MoE/MoP rule in one caption item of `INTENT.md` (the
model's rule, with the pointing error and the launch cost as its two instances), nothing on the
image.

**2. The assembly view.** Finding: the text legend was about 45 % of the frame. Changed: the legend
keeps the two tag keys and the untagged rule ("untagged: fixed (Bus, Antenna, Imu)"); the levels and
ranges are the caption's, as the behavioural view's legend was moved in round 3; the generator still
reads them from the model and writes them beside the views as `assembly_caption.md`, which
`INTENT.md` carries (the frame is 245 px tall against 357; the type is 9.0 px as before, the width
being the boxes'). "Nine parts in eight kinds": the intent now says eight boxes and names the pair
(panelPlus, panelMinus, both in the solar panel's box). The renderer can draw two boxes, but a box is
a kind (`part def`) and the tune `panelSpan` is one variable bound to both usages, marked once; two
boxes would carry the tag twice or on one of two identical boxes, against the legend's own rule, so
the drawing stays at eight and the words agree with it.

**3. One name for each dataset.** "Primary regime" and "baseline regime" (the scope's words) in
everything WP23 writes. Changed in `diagnostic_pair.py`: the baseline heatmap is
`heatmap_baseline.png`; the record's regime headings and the script's printed lines say "baseline
regime" (the CaseSpec key `stock` is `case.py`'s and read-only; a map `REGIME` turns the key into
the word at the point of writing); each heatmap panel is titled with its regime ("K = 1 exponent of
each metric across tau, primary regime"), set on the figure `case.tau_sweep_figure` returns (a
`Figure`; the heatmap is its third axes), the function itself untouched. `tests/test_diagnostic_pair.py`
follows the file name and asserts the two headings and that "stock" is not in the record (4 passed).
The assembly caption and `INTENT.md` use the two names; `INTENT.md` says in one clause that the
heatmap's last column is the tau = infinity limit.

**4. Heatmap redraw, after the gate.** The round-3 cold readers' findings on the heatmap's own
drawing belong to `case.tau_sweep_figure` (read-only for WP23; the paper's `fig-tau-sweep`) and are
listed here, in their words, for the post-gate figure unit (with round 2's note on the cap):

- the colourbar is unnamed (it is the K = 1 exponent w);
- the selected tau is marked on the two top panels and not on the grid;
- the total-mass row is clipped at 0.30 (its exponent is 0.358; round 2's note: a cap at or above
  the largest exponent, or a scale that states its clipping);
- the row order (the rows are in the CaseSpec's attribute order, which the figure does not say);
- the top panels' intent (the fraction above V = 1 and the effective sample size against tau: the
  figure does not say what they are for beside the grid);
- the two axis titles ("temperature tau" on the panels, "tau" on the grid: one name).

**5. Round 4 regenerated.** Both views with `INTENT.md`; the heatmaps and `k3_record.md` regenerated
from the round-1 tables (unchanged since round 1, `README.md` there says why: no dataset-facing part
of the model changed in rounds 2 to 4, so no regeneration was run); the record differs from round 3's
in the one heading word. Checks as run: `uv run pytest -q tests/test_system_model_v2_r1.py
tests/test_diagnostic_pair.py tests/test_check_script.py`; `ruff check` and `ruff format` on
`diagnostic_pair.py` and its test clean; `project.py` sits under `docs/superpowers/notes/spike-*`,
which `pyproject.toml` excludes from `ruff check .` (a throwaway-spike folder kept for
reproducibility), so a run on its explicit path reads `docs/ruff.toml`'s 72 columns and reports the
file's pre-existing long lines (134 before this round); `ruff format` leaves it unchanged.

## Proposed thresholds, revised for the gate popup (the step's own terms; pass fractions)

The driver's ruling on round 3's finding: a 20 % margin on a step function is not a threshold; before
the gate the loop proposes the peak-slew-power limit on the step's own terms (the value that admits the
baseline's wheel class and tracker grade, and one step up), with the pass fraction of feasible designs
for each candidate, and the same pass-fraction column for the other three thresholds; the popup shows
what each choice admits and chooses nothing. This section is that reading. Nothing below is
preferred over anything else; the supervisor chooses.

**Data and definitions.** The round-1 datasets on the r2 model, 1000 designs per regime:
`adcs_designs_cubesat_gains.csv` (primary regime; sha256
`336288e57a2329ad5d573b4696efa27589ce8c2aec571a30853d605e55126693`) and `adcs_designs_cubesat.csv`
(baseline regime; sha256 `4cb65a2ffde19f9f17596859d91e599294dae4428bf8a15cc0dc9632921956d2`), in the
session scratchpad's `wp23-round-1/`. A design is feasible when its four flags hold (`settled`,
`momentum_ok`, `power_ok`, `dod_ok`): 706 of the primary regime's designs, 780 of the baseline regime's.
The pass fraction of a candidate is the share of the feasible designs whose metric is at or below it
(the requirements' `<=`, with an absolute tolerance of 1e-9 for floating-point ties on the cell
values), by regime. The baseline configuration is read from `cubesat_r2.sysml` (the swap has not
landed; `cubesat.sysml` on `dev` is the WP22 model, last touched at d3018ba): medium wheels, medium
tracker, 0.6 m of span, 80 Wh, Kp 0.03 and Kd 0.3; its values are those of the round-1 table
(pointing error 0.015535 degree, control effort 0.0094906 N.m.s, peak slew power 2.0 W, total mass
13.2914 kg, 79,749 USD at 6000 USD/kg). The script is
`scratchpad/wp23-thresholds/thresholds_pass_fractions.py` (not in the repository), run as
`uv run --project <repo> python -I thresholds_pass_fractions.py <the wp23-round-1 folder>`; it
prints the hashes and every number of this section.

**Why the round-1 data serve.** The regeneration of record changes only the settling time's read-off,
by at most one integration step (0.5 s), so the pointing error, the control effort, the peak slew
power and the total mass of every design are unchanged and so are the fractions below, provided the
feasible set is. In both datasets `settled` is `settling_time < 600 s` (checked), the largest settling
time among the settled designs is 594.9 s (primary) and 598.2 s (baseline), and 24 (primary) and 22
(baseline) designs sit at the horizon: no design is within 0.5 s of the horizon on the settled side,
so a shift of one step moves no flag, and the feasible sets stand.

**Peak slew power: the ladder of the nine cells.** With the peak torque at the wheel class's cap the
metric takes one value per (wheel class, tracker grade) cell, so a candidate is a cell value and it
admits whole cells. The value that admits the baseline's cell is 2.0 W; one step up is 2.4045 W. In the
primary regime every small- and medium-wheel design sits on its cell value and no large-wheel design
falls below 6.3 W (the power-limited corner of round 3 (b) lowers the large wheel's value, never below
its coarse-tracker cell); in the baseline regime 24.8 % of the large-wheel designs never reach the cap
(round 3 (b)), so 5 to 7 of the 262 feasible large-wheel designs fall below 2.6 W and the cumulative
fractions at 6.3 and 6.8 W count 135 and 207 of them. Round 1's 2.4 W sits between steps: it admits
the same designs as 2.0 W in the primary regime (43.6 %; the small wheel with the fine tracker fails
by 4.5 mW) and 46.7 % in the baseline regime.

| Candidate (cell it admits) | Pass, primary | Pass, baseline | Admits (feasible designs) |
|---|---|---|---|
| 1.3045 W (small wheel, coarse tracker) | 10.5 % | 10.9 % | small/coarse only |
| 1.5 W (medium wheel, coarse tracker) | 22.9 % | 23.6 % | adds medium/coarse |
| 1.8045 W (small wheel, medium tracker) | 32.7 % | 35.0 % | adds small/medium |
| **2.0 W** (medium wheel, medium tracker: the baseline's cell) | 43.6 % | 46.0 % | small and medium wheels with the coarse or medium tracker; no fine tracker, no large wheel |
| **2.4045 W** (small wheel, fine tracker: one step up) | 50.4 % | 55.0 % | adds small/fine (and 5 unsaturated large-wheel designs in the baseline regime); still no medium/fine, no saturating large wheel |
| 2.6 W (medium wheel, fine tracker) | 62.2 % | 67.3 % | every small and medium wheel; no saturating large wheel |
| 6.3 W (large wheel, coarse tracker) | 76.3 % | 83.7 % | adds large/coarse (and the power-limited large-wheel designs) |
| 6.8 W (large wheel, medium tracker) | 89.2 % | 92.9 % | adds large/medium |
| 7.4 W (large wheel, fine tracker) | 100.0 % | 100.0 % | every cell |

**Pointing error.** The baseline's own value, 0.015535 degree, admits every feasible design of the
primary regime (its largest is 0.00864 degree: the aggressive gain box holds the steady error to a
fifth of the baseline's, round 1) and 99.0 % of the baseline regime's (the eight excluded are
coarse-tracker designs at the lowest gains, Kp at most 0.0345, up to 0.01726 degree); +10 % admits
all but one, +20 % and +50 % admit all. The 90 % and 95 % values are therefore tighter than the
baseline's: in the primary regime 0.00842 and 0.00849 degree, inside the coarse tracker's own range
(0.00834 to 0.00864), so they exclude part of the coarse tracker and nothing else; in the baseline
regime 0.0118 and 0.0136 degree, which cut through every cell (the gains, not the tracker, set the
error there).

| Candidate | Value | Pass, primary | Pass, baseline | Admits |
|---|---|---|---|---|
| baseline | 0.015535 degree | 100.0 % | 99.0 % | every cell in full in the primary regime; 96 to 98 % of each coarse-tracker cell in the baseline regime |
| +10 % | 0.017089 degree | 100.0 % | 99.9 % | all but one medium/coarse design |
| +20 % (round 1) | 0.018642 degree | 100.0 % | 100.0 % | every feasible design |
| +50 % | 0.023303 degree | 100.0 % | 100.0 % | every feasible design |
| admits 90 % (primary) | 0.008422 degree | 89.9 % | 60.8 % | medium and fine trackers in full; 69 to 75 % of each coarse-tracker cell (baseline regime: 20 to 31 % of the coarse cells, 72 to 83 % of the others) |
| admits 95 % (primary) | 0.008495 degree | 94.9 % | 63.7 % | medium and fine trackers in full; 85 to 86 % of each coarse-tracker cell |
| admits 90 % (baseline) | 0.011814 degree | 100.0 % | 90.0 % | every primary design; 85 to 95 % of each cell in the baseline regime |
| admits 95 % (baseline) | 0.013561 degree | 100.0 % | 95.0 % | every primary design; 91 to 99 % of each cell in the baseline regime |

**Control effort.** Round 1 left this one to be read from the data; read, the baseline-anchored
candidates exclude the primary regime. The baseline configuration sits at the lower corner of the
baseline gain box (Kp 0.03, Kd 0.3), and the control effort (the integral of |tau| over the slew)
grows with the gains: the feasible primary designs run from 0.0086 to 0.345 N.m.s (median 0.050),
the baseline regime's from 0.0020 to 0.173 N.m.s (median 0.019). So the baseline's 0.0094906 N.m.s
admits 0.6 % of the primary regime's feasible designs and 26.2 % of the baseline regime's; round 1's
0.011389 N.m.s admits 2.3 % and 32.6 %; +50 % admits 5.2 % and 40.6 %. None of these admits any cell
in full in either regime. The 90 % and 95 % values cut across all nine cells and lean on the wheel
class: at 0.0592 N.m.s (the baseline regime's 90 %) the primary regime keeps 77 to 85 % of each
small-wheel cell and 38 to 42 % of each large-wheel cell (the large wheels slew hardest).

| Candidate | Value (N.m.s) | Pass, primary | Pass, baseline | Admits |
|---|---|---|---|---|
| baseline | 0.009491 | 0.6 % | 26.2 % | no cell in full; primary: 4 designs (3 small-wheel, 1 medium/fine); baseline: 18 to 42 % of each cell |
| +10 % | 0.010440 | 1.3 % | 29.1 % | no cell in full; primary: 9 designs, none with a large wheel |
| +20 % (round 1) | 0.011389 | 2.3 % | 32.6 % | no cell in full; primary: 16 designs, 1 with a large wheel; baseline: 22 to 48 % of each cell |
| +50 % | 0.014236 | 5.2 % | 40.6 % | no cell in full; primary: 37 designs; baseline: 29 to 62 % of each cell |
| admits 90 % (primary) | 0.13079 | 89.9 % | 99.1 % | primary: small/fine in full, 75 to 99 % of the other cells; baseline: all but 7 designs |
| admits 95 % (primary) | 0.16618 | 94.9 % | 99.7 % | primary: every small-wheel cell in full, 85 to 98 % of the others; baseline: all but 2 designs |
| admits 90 % (baseline) | 0.05922 | 58.9 % | 90.0 % | primary: 77 to 85 % of the small-wheel cells, 53 to 68 % medium, 38 to 42 % large |
| admits 95 % (baseline) | 0.07710 | 70.1 % | 95.0 % | primary: 89 to 90 % small, 64 to 77 % medium, 51 to 62 % large |

**Total mass, through the launch cost at 6000 USD/kg.** The mass is set by the swaps and the two
continuous tunes; the baseline's 13.2914 kg (79,749 USD) admits 40.1 % (primary) and 39.0 %
(baseline): no large-wheel design (the lightest is 13.33 kg), and the medium wheel with the fine
tracker at 16 % and 13 %. At +10 % (14.62 kg, 87,723 USD) every small-wheel cell and the medium
wheel with the coarse or medium tracker pass in full and the large wheel passes by tracker grade (82,
67, 36 %); at +20 % (round 1's 15.95 kg, 95,698 USD) every cell passes in full except the large wheel
with the fine tracker at 95 % (the heavy corner of round 1's reading); +50 % admits all. The 90 % and
95 % values are 14.79 to 14.83 kg (88,758 to 88,970 USD) and 15.07 to 15.11 kg (90,423 to
90,643 USD), where only the large-wheel cells are cut.

| Candidate | Value | Pass, primary | Pass, baseline | Admits |
|---|---|---|---|---|
| baseline | 13.2914 kg = 79,749 USD | 40.1 % | 39.0 % | no large wheel; small/coarse 96 %, small/medium 94 %, medium/coarse 76 %, medium/medium 55 %, small/fine 52 %, medium/fine 16 % (primary) |
| +10 % | 14.6205 kg = 87,723 USD | 85.6 % | 86.7 % | small wheels and medium/coarse, medium/medium in full; medium/fine 96 %; large/coarse 82 %, large/medium 67 %, large/fine 36 % |
| +20 % (round 1) | 15.9497 kg = 95,698 USD | 99.4 % | 99.5 % | every cell in full but large/fine at 95 % |
| +50 % | 19.9371 kg = 119,623 USD | 100.0 % | 100.0 % | every feasible design (the heaviest is 16.06 kg) |
| admits 90 % (primary) | 14.8283 kg = 88,970 USD | 89.9 % | 90.8 % | small wheels and medium/coarse, medium/medium in full; medium/fine 99 %; large/coarse 90 %, large/medium 79 %, large/fine 49 % |
| admits 95 % (primary) | 15.1072 kg = 90,643 USD | 94.9 % | 95.6 % | small and medium wheels in full; large/coarse 95 %, large/medium 93 %, large/fine 70 % |
| admits 90 % (baseline) | 14.7930 kg = 88,758 USD | 89.1 % | 90.0 % | as the row above it, with large/coarse 89 %, large/medium 76 %, large/fine 47 % |
| admits 95 % (baseline) | 15.0705 kg = 90,423 USD | 94.2 % | 95.0 % | small and medium wheels in full; large/coarse 95 %, large/medium 91 %, large/fine 67 % |

**Battery discharge rate.** The requirement (`BatteryPeakPowerRequirement`) reads the eclipse peak
load, the housekeeping load plus the peak slew power (`EclipsePeakLoad`), against the pack's peak
power, the discharge rate times the capacity (`BatteryPeakPower`). The columns to compute it exist:
`peak_slew_power_w` (which already carries the tracker's power and the idle wheels, as `PeakSlewPower`
is defined) and `battery_wh`, with the housekeeping load 12 W from the model
(`environment.housekeepingLoad`). Over the feasible designs the eclipse peak load runs from 13.3 to
19.4 W and the smallest pack is 26.9 Wh (the depth-of-discharge floor removes the smaller ones).

| Rate | Pack peak power | Pass, primary | Pass, baseline | Admits |
|---|---|---|---|---|
| 0.5 C | 0.5 W per Wh | 93.6 % | 95.3 % | fails 45 (primary) and 37 (baseline) feasible designs, all with packs of at most 37.4 Wh and medium or large wheels |
| 1 C (round 2) | 1 W per Wh | 100.0 % | 100.0 % | every feasible design, by 0.6 W in the corner (round 2) |
| 2 C | 2 W per Wh | 100.0 % | 100.0 % | every feasible design |

**The popup table** (metric, candidate, pass fraction of feasible designs in the primary and the
baseline regime, what it admits; the 90 % and 95 % rows carry the primary regime's value and both
regimes' fractions at it; the regime-specific values are in the tables above):

| Metric | Candidate | Pass, primary | Pass, baseline | What it admits |
|---|---|---|---|---|
| peak slew power | 2.0 W (the baseline's cell) | 43.6 % | 46.0 % | small and medium wheels with the coarse or medium tracker; no fine tracker, no large wheel |
| peak slew power | 2.4045 W (one step up) | 50.4 % | 55.0 % | adds the small wheel with the fine tracker; no medium/fine, no saturating large wheel |
| pointing error | 0.015535 degree (baseline) | 100.0 % | 99.0 % | everything but 8 coarse-tracker designs at the lowest gains |
| pointing error | 0.017089 degree (+10 %) | 100.0 % | 99.9 % | everything but 1 design |
| pointing error | 0.018642 degree (+20 %) | 100.0 % | 100.0 % | every feasible design |
| pointing error | 0.023303 degree (+50 %) | 100.0 % | 100.0 % | every feasible design |
| pointing error | 0.008422 degree (admits 90 %) | 89.9 % | 60.8 % | medium and fine trackers in full; part of the coarse tracker |
| pointing error | 0.008495 degree (admits 95 %) | 94.9 % | 63.7 % | medium and fine trackers in full; 85 % of the coarse tracker |
| control effort | 0.009491 N.m.s (baseline) | 0.6 % | 26.2 % | 4 primary designs; no cell in full in either regime |
| control effort | 0.010440 N.m.s (+10 %) | 1.3 % | 29.1 % | 9 primary designs; no cell in full |
| control effort | 0.011389 N.m.s (+20 %) | 2.3 % | 32.6 % | 16 primary designs; no cell in full |
| control effort | 0.014236 N.m.s (+50 %) | 5.2 % | 40.6 % | 37 primary designs; no cell in full |
| control effort | 0.13079 N.m.s (admits 90 %) | 89.9 % | 99.1 % | all cells in part, small wheels nearly in full, large/medium at 75 % |
| control effort | 0.16618 N.m.s (admits 95 %) | 94.9 % | 99.7 % | small wheels in full; 85 to 98 % of the medium and large cells |
| total mass | 13.2914 kg = 79,749 USD (baseline) | 40.1 % | 39.0 % | no large wheel; medium/fine at 16 % |
| total mass | 14.6205 kg = 87,723 USD (+10 %) | 85.6 % | 86.7 % | small wheels in full; large wheel by tracker 82 / 67 / 36 % |
| total mass | 15.9497 kg = 95,698 USD (+20 %) | 99.4 % | 99.5 % | every cell in full but large/fine at 95 % |
| total mass | 19.9371 kg = 119,623 USD (+50 %) | 100.0 % | 100.0 % | every feasible design |
| total mass | 14.8283 kg = 88,970 USD (admits 90 %) | 89.9 % | 90.8 % | small wheels in full; large wheel by tracker 90 / 79 / 49 % |
| total mass | 15.1072 kg = 90,643 USD (admits 95 %) | 94.9 % | 95.6 % | small and medium wheels in full; large wheel by tracker 95 / 93 / 70 % |
| battery discharge rate | 0.5 C | 93.6 % | 95.3 % | fails packs of at most 37.4 Wh with medium or large wheels |
| battery discharge rate | 1 C | 100.0 % | 100.0 % | every feasible design |
| battery discharge rate | 2 C | 100.0 % | 100.0 % | every feasible design |

None of these thresholds enters a dataset column; the four flags stay what they are, so no choice
moves a fit.

## R-5's check, amended

The closed-form calcs of section 4, `TorqueLimitedSlewTime`, `LinearSlewTime`, `SlewTimeEstimate` and
`IsTorqueLimited`, stay in the scenario section as the model-checking evidence of WP15: they estimate
the time the slew takes to enter the band, a physical quantity of the scenario, not a traded metric, a
measurement or a requirement, and the comparison code reads them by name. R-5's grep for `SlewTime` is
therefore read over the measurement (`SlewMeasurement`), the requirements (section 5) and the
experiment's outputs (`SlewExperiment`), where it finds nothing (`test_r2_slew_time_has_left_the_
measurement_and_the_requirements`), and not over section 4. The PM has recorded this reading for the
driver.

## REACH: the rule and the value (the data gate, 2026-11-10)

The gate's first regeneration stopped in `check_designs.Proposer.draw`: on the settling-time
four-metric view (D-3 replaced `slew_time_s` by `settling_time_s` in `check_designs.METRICS`) no
hole among the 300 most isolated has a seeded configuration predicted within REACH = 0.35, the
constant WP7 typed for the slew-time view (67eea92, `make_check_designs.py`, "predicted
[Z | 2 log V] distance within which a hole counts as reachable"; WP7's scope, review and decisions
state no rule for it). The same holds on the old primary data with the new view (the nearest pool
design is at 0.481 there, 0.484 on the regenerated data), so the view change moved the numbers,
not the regeneration. The driver's decision (`WP23-decisions.md`, "The proposer's reach on the
settling-time view"): the reach is set by a stated rule, a quantile of the pool's nearest predicted
distances to the holes the method reads, checked on the old view; never by the number that makes
the method produce three proposals.

**The rule.** A hole counts as reachable when a seeded configuration is predicted within the reach
of it; the reach admits the nearest few per cent of the isolated holes. The reach is the 2nd
percentile (`REACH_QUANTILE = 0.02`) of the nearest predicted `[Z | 2 log V]` distances from the
seeded pool (100,000 designs, seed 20261108) to the 300 most isolated holes of the view in use
(`HOLES = 300`, the holes the method reads), computed from the data at run time (so the value of
record is the container's own, not a number typed from this Mac).

**The check on the old slew-time view** (old primary data, the committed `@4` proposals' view, on
this Mac): the nearest predicted distances of the 300 holes have minimum 0.161, 10th percentile
0.444 and median 0.644; six holes lie within 0.35; the 2nd percentile is **0.351**, and the three
separated holes it admits are at 0.348, 0.340 and 0.327, the committed proposals' distances
(0.3478, 0.3399, 0.3265). The 1st percentile returns 0.340 (three holes, one at 0.161), the 3rd
0.362, the 5th 0.388. So the 2nd percentile is the rule WP7 used in effect, and 0.35 was not
arbitrary with respect to it.

**The value on the settling-time view** (regenerated primary data, this Mac; the run of record's
own value is in `WP23-rounds/gate/README.md`): the 300 nearest distances have minimum 0.484, 10th
percentile 0.717 and median 0.867; the 2nd percentile is **0.622**, and it admits three separated
holes at 0.587, 0.579 and 0.555 (hole scores 4.85, 4.85, 4.83). The 1st percentile (0.579) would
admit two. On both views the proposals sit close to the reach: the holes the method reads are the
most isolated, and the nearest reachable ones are, by the rule, a few per cent of them.

**In the code.** `check_designs.py` carries `REACH_QUANTILE` and `HOLES` with the rule in one
comment; the proposer returns the reachable, separated holes it finds, up to the count asked, and
prints the reach and the count (fewer than asked is a result, not a failure; the paper's check
sentence reads the count from the file). `make_check_designs.py`, the frozen generation's script,
is unchanged (its 0.35 produced the frozen file). Scripts of the derivation above:
`reach_probe.py`, `reach_dist.py`, `reach_rule.py` in the session scratch, not committed.

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

## Case prose (D-7): claims

The section "From the assembly to the dataset: measures of effectiveness and measures of
performance" of `examples/adcs/case-model.md` (R-14), read with the register of
`docs/superpowers/notes/claims-review.md`: each claim a reader could rely on, its kind and its
backing. Definitions (the metrics in their disciplines' words, the MoE/MoP rule) and statements of
intent (the hypothesis, the proposed thresholds marked proposed) are not claims and are not
listed. Vocabulary: the section uses "monomial term", "term", "cell" and "n-lemma" and no
"facet"; the vocabulary tool's corpus does not include `case-model.md` (`read_corpus` in
`scripts/check_vocabulary.py`: the paper notebooks, `docs/*.md`, `docs/user-guide/*.md`,
`site/index.html`, `README.md`, the `src/` docstrings), so the three glossary entries above stay
held: added now they would each be a `dead-entry` and `tests/test_vocabulary.py` would go red;
they enter with the paper's case section after the gate.

| Claim (fragment) | Kind | Backing | Verdict |
|---|---|---|---|
| "Two MoEs (the pointing error and the launch cost) and eight MoPs" | S | the `doc` marks in `cubesat_r2.sysml`; "MoE/MoP classification" above; `coverage.md`, second table | backed |
| "Each metric is read by a requirement on its own quantity and verified in a verification case" | S | `coverage.md`, second table; `tests/test_model_coverage.py::test_every_traded_metric_has_a_requirement_that_reads_it_and_a_mark` | backed |
| "computed by event detection as the last exit from the band, so a slew that never holds inside the band has the horizon as its settling time" | S | the `doc` of `SlewMeasurement.settlingTime` and of `SettledRequirement` in `cubesat_r2.sysml`; WP16 D-7 (the measurement change lands with the regeneration); today's read-off is `_last_outside` in `experiments/cubesat_oracle.py`, the same quantity on the integrator's grid ("Coverage table, platform stability" above) | backed |
| "the slew time ... left the traded metrics with WP16's decision" | S | `WP16-decisions.md`, "Slew time under event detection" ("One: settling time"); `tests/test_system_model_v2.py::test_r2_slew_time_has_left_the_measurement_and_the_requirements` | backed |
| "the launch rate times the total mass, increasing in mass ... the dataset gains no column" | S | `calc def LaunchCost`; `tests/test_system_model_v2.py::test_r2_launch_cost_is_the_rate_times_the_total_mass_and_increases_with_it`; `WP23-decisions.md` OD1, OD2 | backed |
| "The first four are the flags of the dataset, the verdicts of named requirements" | S | `experiments/feasibility.py` (`settled`, `momentum_ok`, `power_ok`, `dod_ok` to their requirement defs); the requirements table of the section against `cubesat_r2.sysml` section 5 | backed |
| "each threshold the baseline configuration's own value with a 20 % margin ... 0.018642 degree, 0.011389 N.m.s, 2.4 W, 95,698.29 USD (15.950 kg at the rate)" | R | `part budgets : Budgets` (`margin = 1.2`); `tests/test_system_model_v2.py::test_r2_proposed_thresholds_are_the_baselines_values_with_the_stated_margin`; "Proposed thresholds" above (the control-effort and peak-slew-power limits read the baseline's recorded measurement, so the regeneration can move them; the prose states them as proposed and read from the model) | backed |
| "a continuous rating of 1 C ... the pack delivering its capacity in one hour" | S | `environment.batteryDischargeRate = 1.0` (1/h), `calc def BatteryPeakPower`; "Round 2" above (the rationale is marked illustrative, not a cited rating) | backed |
| "None of these thresholds enters the dataset: the four flags stay what they are ... cannot move a fit" | S | the dataset's flag columns are the four of `feasibility.py`; "Proposed thresholds" above, last paragraph | backed |
| "Every swap and tune reaches at least one traded metric in both columns, and every traded metric is reached: ... all nine, Kp eight ... Kd seven" | R | `coverage.md`, first table and "Connectivity"; `tests/test_model_coverage.py::test_no_decision_element_row_is_empty_structurally`, `test_no_decision_element_row_is_empty_empirically`, `test_the_gains_do_not_reach_the_mass_and_kd_does_not_reach_the_pointing_error` | backed |
| "Seven cells disagree between the columns, with one cause: ... the wheel class's maximum, because the power cap does not bind there" | R | `coverage.md`, "Disagreements"; "Coverage findings" above; `EXPECTED_DISAGREEMENTS` in `tests/test_model_coverage.py` | backed |
| "the design structure matrix of multidisciplinary design analysis and optimization (MDAO), the family the paper names ... the XDSM of Lambe and Martins" | L | the paper's related-families table names MDAO with `sobieszczanski1997multidisciplinary`; `lambe2012extensions` in `docs/references.bib` (verified 2026-11-09, DOI resolved); `coverage.md`, third table's preamble | backed |
| "The graph of configuration values, subsystems and metrics is connected, and the controls and the power subsystem feed each other, a loop the model resolves in one pass" | R | `coverage.md`, "Connectivity" and its last paragraph; `tests/test_model_coverage.py::test_every_configuration_value_feeds_a_subsystem_and_the_graph_is_connected`, `test_coupling_variables_between_subsystems_are_the_models_named_quantities` | backed |
| "no metric, threshold or constant of the model was chosen because it moves the heatmap, and the fit runs unchanged" | S | `WP23-scope-of-work.md`, non-goals; "Model change in round 3: none" above; R-7's seam (`src/` untouched) | backed |
| "In the primary regime three metrics carry no exponent at any fit temperature of the sweep: ... in the baseline regime the peak slew power alone" | R | round 1's `heatmap.png` and `k3_record.md` (`WP23-rounds/round-1/`); "Round 3" above, first paragraph; marked in the prose as round 3's reading on the round-1 data, not a result of record | backed |
| "the K = 1 fit is one monomial term, a hyperplane in log-metric space, and a metric carries weight only where it trades against the others at the frontier: the contending set is found from the data" | M | `docs/theory.md`, "Elasticities and the n-lemma" (L3: the fit at tau = infinity is a linear program with a sparse solution; glossary `contending-set`, `n-lemma`) | backed |
| "Given the tracker grade, both are monotone functions of the one battery capacity ... one quantity to the fit ... the fit gave the depth of discharge the weight ... the two requirements are the same inequality" | R | `calc def EclipseReserve` and `DepthOfDischarge` (the reserve is `maxDepthOfDischarge * capacity - demand`, the depth `demand / capacity`); "Round 3" (a) and the n-lemma reading above (Spearman -0.9994 over the feasible designs; the depth of discharge 0.158 and the reserve 0 in the primary regime, round-1 data) | backed |
| "Both are affine in the generated power, which is proportional to the panel span ... it changed between the regimes (the energy balance in the primary regime, the power margin in the baseline regime)" | R | `calc def PowerMargin`, `EnergyBalance`, `GeneratedPower`; "Round 3" (c) and the n-lemma reading above (energy balance 0.184 and power margin 0 in the primary regime; 0.019 and 0.178 in the baseline regime, round-1 data) | backed |
| "With the peak torque at the wheel class's maximum it takes one value per wheel class and tracker grade ... orders the designs as the total mass does ... With three terms (K = 3) it leads a term in both regimes" | R | `calc def PeakSlewPower` (tracker power plus idle wheels plus 5e4 x peakTorque^2); "Round 3" (b) and (c) and the n-lemma reading above (one value per medium and small cell; Spearman 0.87 with the total mass among the feasible designs; K = 3 term leads 0.612 primary, 0.428 baseline; round-1 data) | backed |
| "round 3 changed none" (the model) | S | "Model change in round 3: none" above; the committed views and coverage table of the round stand | backed |

No row is broader than its backing and none is unbacked. Two sentences were narrowed while
writing: the slew angle is read from the model (30 degrees, `nominalSlew.slewAngle`), and the
hypothesis is cited to where the supervisor's words are quoted (`WP23-scope-of-work.md`, Purpose),
not to the decisions file, which does not carry them.

## Rounds: the cold reads and their dispositions

The cold reads of the loop (R-8: a fresh P2 proxy at L-B and a fresh P3 proxy at L-C per round,
image before caption, never reused across rounds) are quoted verbatim, each finding with its
disposition and where it was executed, in `WP23-rounds/round-1/cold-reads.md` (17 P2 and 20 P3
findings) and `WP23-rounds/round-3/cold-reads.md` (22 P2 and 17 P3 findings). Round 2 had no cold
read of its own: it changed the model (the battery's rating) and the coverage table, and its views
were read in round 3. Round 4 had none: it executed round 3's dispositions and was checked by its
author at 700 px ("Round 4" above). The K = 1 and K = 3 readings of each round are
`k3_record.md` in the round's folder; the data are round 1's in every round, since no
dataset-facing part of the model changed after round 1 (`round-4/README.md`).

**Round 1** (the views of `cubesat_r2.sysml` by the generator's revision 3; the heatmap pair and
the record on the round-1 datasets). One blocking finding, the P2's: the heatmap had no written
intent, so the loop's first test could not be run on it; closed in round 3, whose `INTENT.md`
carries the heatmap's sentence. Both readers found the behavioural view's legend illegible at
700 px (6.9 px of type), the P3 that green carried an MoE and an MoP while yellow carried the other
MoE, the P2 that the lanes drew the analyst's grouping as model structure and that the two
requirements without a metric named no quantity, and both that five names were in use for the two
datasets. These changed the views in round 3 (`abdb88f`): the legend cut to the colour key and the
rest moved to the caption; one colour rule with MoE or MoP by stereotype only; the requirement
boxes reduced to the name and the verification case; the requirements that read no traded metric
carrying their `require constraint`; the requirement-metric line headless; the lanes titled as the
analyst's grouping; the untagged parts named as fixed; the gain ranges per regime; "primary regime"
and "baseline regime" the two names. Deferred, with the reason: every finding on the heatmap's own
drawing (the colourbar unnamed, the total-mass row clipped at the cap of 0.30, the selected tau
not on the grid, V and the 0.1 line unexplained, the two axis titles) belongs to
`case.tau_sweep_figure`, read-only for this package, and goes to the redraw after the gate (the list
in "Round 4", item 4). Interrogated rather than drawn: the P3's observation that the three metrics
at zero exponent include the two columns carrying every coverage star, and the P2's question
whether the MoPs at zero are constraints, became round 3's work (`a93ce10`). The K = 1 reading:
in the primary regime a 5-lemma at tau 38.1 (total mass 0.358, energy balance 0.184, pointing error
0.164, depth of discharge 0.158, settling time 0.136) with the power margin, the eclipse reserve and
the peak slew power at zero at every tau; in the baseline regime a 5-lemma at tau 45.7 (control
effort 0.432, settling time 0.319, power margin 0.178, pointing error 0.039, depth of discharge
0.012) with the peak slew power alone at zero. The K = 3 reading: in the primary regime the peak
slew power leads term 3 (0.612; 363 rows, share 0.724) and the per-term report refuses at both of
its bands (3 and 7 near-frontier rows in a cell against its minimum of 10; the fit itself is
given); in the baseline regime, at the K = 1 band, three terms of 5, 6 and 4 metrics, the peak slew
power leading term 2 (0.428).

**Round 3** (the views by revision 4, the pair regenerated on the same data, the model unchanged
since round 2). Nothing blocked. The P3 missed the mass chain cold: the line requirement -> launch
cost -> total mass was a stub of about 5 px, the one place the view departs from
one-requirement-one-metric. The P2 could not read the dashed group's grey title and asked why the
pointing error is the one MoE; both found the heatmap's regime unnamed on the image (with
`heatmap_stock.png` beside it, still "stock"), the colourbar unnamed and the selected tau absent
from the grid; the P2 found the assembly legend to be 45 % of the frame. These changed the views in
round 4 (`43e1a7f`): the launch-cost line labelled `totalMass` and lengthened, the dashed title in
black, the MoE/MoP rule a caption item, the assembly legend cut to the tag keys with the levels and
ranges in `assembly_caption.md`, the baseline heatmap renamed `heatmap_baseline.png` with each panel
titled by its regime and the record's headings in the two names, and the tau = infinity column
named in the caption. Deferred, with the reason as in round 1: the heatmap's drawing (the
colourbar, the tau marker, the cap, the row order, the top panels' intent, the two axis titles),
listed in "Round 4", item 4 for the post-gate redraw. The readings of K = 1 and K = 3 are round
1's, on the same data and the same fit (round 4's record differs from round 3's in one heading
word), with the n-lemma reading of each zero exponent written in round 3: the eclipse reserve is
carried by the depth of discharge (one quantity), the power margin by the energy balance (both
affine in the generated power; the fit carries the other in the baseline regime), and the peak
slew power is a step function of the two swaps that one monomial term cannot use and that K = 3
gives a term of its own in both regimes.

**Open findings** (no disposition in the record; the tables name each by reader and number).
Grouped for the PM's decision at or after the gate:

- A. Heatmap items not in the post-gate redraw list: the grey scale's resolution near zero (a cell
  at 0.03 reads as white, so the control effort's fade cannot be seen: R1-P2-7, R3-P2-15); the
  horizontal mismatch between the log axis above and the equal-width columns below (R1-P2-6); the
  intent sentence's tau dependence (the panel shows the settling time weakening and the energy
  balance strengthening with tau, which the intent does not claim: R3-P3-7).
- B. The behavioural view against the model's other records: the total mass and the pointing error
  drawn from `SlewExperiment` while verified in `ConfigurationVerification`, the configuration-only
  entries not distinguished (R1-P3-13, R3-P2-7); `coverage.md`'s "passes through" and "traded
  metrics" sentences against the view's sources and the row order (R1-P3-12, R1-P3-16); the three
  requirements that read no traded metric placed in the coupling table's subsystems and in the
  view's dashed group (R3-P3-9); the coupling variables and the measurement-to-analysis path drawn
  in neither view (R3-P3-10).
- C. Names: "the analyst's grouping", "subsystems" and "lanes" for one object (R3-P3-11); "primary
  regime" and "baseline regime" against the model's `aggressiveGains` and `baselineGains`, which the
  caption does not name (R3-P3-13); the swap tags naming enum types and the tune tags naming
  attributes (R3-P3-14).
- D. `round-1/README.md` attributes both per-term report refusals to "term 1" while the estimator's
  messages say "facet 1" and "facet 0" (R1-P3-5); the index base is stated nowhere in the round
  record (WP24 renames the word; it does not settle the base).
- E. What the behavioural view does not show, by design: thresholds, units, directions and the
  configuration variables (R1-P2-15, R3-P2-8); the record answers with the threshold tables for the
  gate popup and the coverage table's first table, and records no decision on the view.
- F. The assembly view's composition lines cross two box headers (R3-P3-15); round 4 changed its
  legend, not its layout, and did not say whether the crossings remain.

**The PM's dispositions of A to F (2026-11-10, early; the round cap of four is reached, so each open
finding gets a disposition here rather than another round).** A: added to the post-gate heatmap redraw
list (the drawing is `case.tau_sweep_figure`'s, a non-goal of this package): the grey scale's
resolution near zero, one tau axis for both panels, and the intent sentence to claim exactly what the
panel shows. B, C and F: one post-gate view-consistency unit on `project.py` and `coverage.py`'s prose
(the sources drawn as the model's analysis returns them, with the verification case named where it
differs; one name for the analyst's grouping; the regime names tied to the model's gain boxes in the
caption; tags at one identifier level; the composition lines routed clear of box headers), run after the
gate so the committed views are regenerated once more with the paper's figures. D: a one-line
correction to `round-1/README.md` in that unit (the estimator's messages index terms from 0 in the K = 3
message and from 1 in the K = 1 message; the README's attribution is checked against the data, not
assumed). E: by design and recorded as such: the behavioural view is the "what is evaluated" half; the
thresholds and what each admits are the gate popup's tables, and the configuration variables are the
assembly view's; no change to the view.

## Trace table

WP22's trace table, updated for the r2 model (`cubesat_r2.sysml` at `dev`, sha256 `8363152af0b7`,
the file `coverage.md` names; the swap to `cubesat.sysml` is the gate's). One row per traded metric:
the model element that defines it with its mark, the decision elements that reach it (the coverage
table's structural column, with the empirical disagreements starred), the requirement that reads it
with its threshold and its verification case, how it leaves the model (the measurement, or
`SlewExperiment`'s return tuple, whose entries are numbered in the model's order), the dataset
column of the round-1 tables (the committed v2 header less `slew_time_s` and `slew_time_05deg_s`;
the contract amendment is D-4, on the `wp23case` branch until the regeneration), and where the paper
reads it. The paper today reads the frozen ten-metric data (`examples/adcs/data/*.csv`, `case.py`'s
CaseSpec): the K = 1 sweep (`fig-tau-sweep`), the K = 3 readings (`fig-tensions-k3`) and the two
regimes (`fig-regimes`) over all ten attributes, and the propose-predict-check (`fig-predict-check`)
over the four-metric view (slew time, pointing error, control effort, total mass); every reading on
the nine-metric data is "after the paper's regeneration" (WP16 order step (4), WP19).

| Traded metric | Defined by (mark) | Reached by (structural; `*` empirical no) | Requirement (threshold; value taken from) | Verified in | Leaves the model as | Dataset column | Where the paper reads it |
|---|---|---|---|---|---|---|---|
| settling time | `SlewMeasurement.settlingTime` (MoP): the hold time, the last exit from the settling band by event detection (WP16 D-7) | all six | `SettledRequirement` (`settlingTime < nominalSlew.horizon`, 600 s; the scenario's horizon) | `SlewVerification.settled` | measured; passes from the measurement to the output row, neither an input nor an entry of the return tuple | `settling_time_s` (and the flag `settled`) | `fig-tau-sweep`, `fig-tensions-k3`, `fig-regimes` on the frozen data; in the four-metric view and the check: after the paper's regeneration (the view carries the slew time today) |
| pointing error | `calc def PointingError` (MoE): the root-sum-square of the steady error and the tracker floor | all but Kd | `PointingErrorRequirement` (`PointingError(c) <= budgets.pointingErrorLimit`; proposed, the baseline's 0.015535 degree times 1.2 = 0.018642 degree; the gate popup's candidates in "Proposed thresholds, revised") | `ConfigurationVerification.pointingError` | return entry 1, `PointingError(cubesat)` (configuration only) | `pointing_error_deg` | the three figures and the check on the frozen data; after the paper's regeneration |
| total mass | `Cubesat.totalMass` (MoP), `calc def MassAccounting`; its MoE `calc def LaunchCost` = `environment.launchRate` (6000 USD/kg, illustrative) times the total mass | WheelClass, TrackerGrade, panelSpan, batteryCapacity (not the gains) | `LaunchBudgetRequirement` (`c.launchCost <= budgets.launchBudget`; proposed, the baseline's 79,749 USD times 1.2 = 95,698 USD, 15.950 kg at the rate; candidates in "Proposed thresholds, revised") | `ConfigurationVerification.launchBudget` | return entry 2, `cubesat.totalMass` (configuration only); the launch cost is not returned (OD2) | `total_mass_kg`; no launch-cost column | the three figures and the check on the frozen data; after the paper's regeneration |
| control effort | `SlewMeasurement.controlEffort` (MoP): the integral of \|tau\| over the slew, N.m.s | all six | `ControlEffortRequirement` (`controlEffort <= budgets.controlEffortLimit`; proposed, the baseline's recorded 0.0094906 N.m.s times 1.2 = 0.011389 N.m.s; the revised reading shows it admits 2.3 % of the primary regime's feasible designs; candidates in "Proposed thresholds, revised") | `SlewVerification.controlEffort` | measured; `SlewExperiment`'s `in controlEffort`, return entry 3 unchanged | `control_effort` | the three figures and the check on the frozen data; after the paper's regeneration |
| power margin | `calc def PowerMargin` (MoP): the generated power less the housekeeping load and the peak slew power | all six; `*` batteryCapacity, Kp, Kd (the wheels saturate at the class cap at the three named configurations) | `PowerMarginRequirement` (`PowerMargin(c, peakTorque) >= 0.0 [W]`; zero) | `SlewVerification.powerMargin` | return entry 4, `PowerMargin(cubesat, peakTorque)` (needs the measured peak torque) | `power_margin_w` | `fig-tau-sweep`, `fig-tensions-k3`, `fig-regimes` on the frozen data; after the paper's regeneration |
| energy balance | `calc def EnergyBalance` (MoP): over one orbit, the sunlit supply less the base load and the slew loss | all six | `EnergyBalanceRequirement` (`EnergyBalance(c, SlewLossEnergy(torqueSquaredIntegral)) >= 0.0 [W*h]`; zero) | `SlewVerification.energyBalance` | return entry 5 (needs the measured `torqueSquaredIntegral`) | `energy_balance_wh` | as the power margin |
| eclipse reserve | `calc def EclipseReserve` (MoP): the energy above the allowed depth of discharge after the eclipse demand | all six | `EclipseReserveRequirement` (`EclipseReserve(c, SlewLossEnergy(torqueSquaredIntegral)) >= 0.0 [W*h]`; zero) | `SlewVerification.eclipseReserve` | return entry 6 | `eclipse_reserve_wh` | as the power margin |
| peak slew power | `calc def PeakSlewPower` (MoP): the tracker's power, the idle wheels and the wheel loss at the peak torque | all six; `*` panelSpan, batteryCapacity, Kp, Kd (the same cause) | `PeakSlewPowerRequirement` (`PeakSlewPower(c, peakTorque) <= budgets.peakSlewPowerLimit`; proposed, the baseline's 2.0 W times 1.2 = 2.4 W in the model; the driver's ruling: the popup offers the step's own values, 2.0 W and 2.4045 W, with pass fractions) | `SlewVerification.peakSlewPower` | return entry 7, `PeakSlewPower(cubesat, peakTorque)` | `peak_slew_power_w` | as the power margin |
| depth of discharge | `calc def DepthOfDischarge` (MoP): the eclipse demand with the slew loss over the capacity | all six | `DepthOfDischargeRequirement` (`DepthOfDischarge(c, SlewLossEnergy(torqueSquaredIntegral)) <= environment.maxDepthOfDischarge`; 0.3, the environment's) | `SlewVerification.depthOfDischarge` | return entry 8 | `dod_eclipse` (and the flag `dod_ok`) | as the power margin |

Not traded, for the trace to close (the requirements the behavioural view draws with no line, and
what left):

| Quantity | Defined by | Requirement | Verified in | Dataset | Note |
|---|---|---|---|---|---|
| available power | `calc def AvailablePower`, `Cubesat.availablePower` | `PowerRequirement` (`c.availablePower > 0.0 [W]`) | `ConfigurationVerification.power` | the flag `power_ok` (and `available_power_w`) | holds for every design of both round-1 datasets ("Round 3" (a)) |
| peak momentum | `SlewMeasurement.peakMomentum` | `MomentumRequirement` (`peakMomentum <= c.momentumCapacity`) | `SlewVerification.momentum` | the flag `momentum_ok` (and `peak_momentum_nms`) | measured, not used by any return entry |
| eclipse peak load against the pack's peak power | `calc def EclipsePeakLoad`, `calc def BatteryPeakPower` (`environment.batteryDischargeRate` 1.0 1/h, illustrative; round 2) | `BatteryPeakPowerRequirement` (`EclipsePeakLoad(c, peakTorque) <= BatteryPeakPower(c)`) | `SlewVerification.batteryPeakPower` | no column; computable from `peak_slew_power_w`, `battery_wh` and the housekeeping load | holds over the whole declared space by 0.6 W in the corner ("Round 2"); the rate's candidates are in the popup table |
| launch cost | `calc def LaunchCost` (MoE), `Cubesat.launchCost` | `LaunchBudgetRequirement` (above) | `ConfigurationVerification.launchBudget` | no column (OD2: in the log metrics it is the total mass shifted by a constant) | the MoE on the total mass |
| slew time | gone (R-5): `SlewTimeRequirement` and `SlewBandRequirement` fold into `SettledRequirement`; the measurement loses `slewTime` and `censored` | — | — | `slew_time_s` and `slew_time_05deg_s` leave with the regeneration (D-4, the contract amendment on `wp23case`) | the closed-form `SlewTimeEstimate` and its parts stay in section 4 as WP15's model-checking evidence ("R-5's check, amended") |

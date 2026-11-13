# WP23 — Review record (the model-realism loop)

Screenshots for this record: commit `c680853`, `git show c680853:<path>` with `<path>` under `work-packages/WP23-rounds/gate/`.

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

## Data gate: the comparison (D-9)

The comparison of old v2 against new v2 (the files, every moved number with its cause, every conclusion identical or changed, the slot list) is `work-packages/swap-evidence.md`, section "WP23 data gate: old v2 (WP22 model, slew time, step-read settling time) against new v2 (WP23 model, nine metrics, event-detected settling time)"; its "Changed conclusions" list comes first there.

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

## Post-gate view-consistency unit

The PM's dispositions B, C, D and F of "Rounds: the cold reads and their dispositions", and the
pair's drawing (`diagnostic_pair.py`). The views are `project.py` revision 6 (the default; revisions
3 to 5 reproduce the earlier text), regenerated once and rendered by `render.sh` with PlantUML
1.2026.8 (the committed revision-5 text re-rendered to the committed bytes first, so the recipe is
the one the views were made with); the paper's two static copies are byte copies.

- **B, sources and verification.** The analysis box now says what the model's analysis returns: 8 of
  the 9 metrics, the pointing error and the total mass computed from the configuration alone (no
  slew), the control effort passed on as measured (an `in` returned unchanged); it replaces "computes
  7 of the 9 ... from the measured inputs", which read as if every entry needed a slew. The
  configuration-only entries are found from the model (an entry whose expression and calcs read no
  measured input), not typed. The arrows are unchanged (the control effort's starts at the
  measurement, where the value is measured; the settling time is read from the measurement and is
  not returned). The verification cases are the requirement boxes' own second line
  (`ConfigurationVerification` for the pointing error and the launch budget); the new
  `views/behavioural_caption.md` states both facts, that the three requirements that read no traded
  metric stand apart here and are listed under their calc's group in the coupling table, and that
  the coupling variables and the measured inputs of the analysis are the cells of that table and are
  not drawn (the view loses nothing the sentence needs by leaving them out). `coverage.py`'s prose
  (the preamble sentence "Traded metrics", the docstrings, the coupling table's introduction) now
  says the measurement attributes that the analysis neither takes nor returns, then its return
  entries in order (an input returned unchanged is one of them), which is the row order, and that a
  requirement is listed under the group of the calc it reads. `coverage.md` carries the same two
  sentences by hand-applied substitution; the structural build's two prose lines equal the
  committed ones, and no verdict, number or magnitude moved (the empirical column was not
  regenerated: the committed magnitudes are the environment of record's).
- **C, names.** The analyst's grouping is "the group(s)" in the new captions and in the changed
  coverage prose ("the three groups of the behavioural view, the analyst's grouping of the metrics");
  the lane titles keep "(the analyst's grouping)". The assembly caption names each regime with its
  gain box (`Kp: 0.03 .. 1 (baseline regime, baselineGains); 0.2 .. 2 (primary regime,
  aggressiveGains)`); the legend names neither. The swap tags now name the attribute, as the tune
  tags do (`wheelClass`, `grade`), and the caption gives the enum behind each (`wheelClass (enum
  WheelClass)`), which is the coverage table's name for the decision element. Residual: the coverage
  table's decision-element column still reads `WheelClass` and `TrackerGrade` for the swaps (its
  generator and `coverage.csv` are outside this unit).
- **D.** `round-1/README.md`: the cell with 3 near-frontier designs at the K = 1 band is term 2
  (181 rows, share 0.034), the cell with 7 at the K = 3 band is term 1, as the K = 3 messages number
  terms from 0 (`facet 1`, `facet 0`); checked against `k3_record.md`'s cells and the estimator,
  agreeing with `swap-evidence.md`, "Changed conclusions" 2. The library's K = 1 message carries no
  index at all (`tensions.py`: an empty prefix), so no K = 1 base is stated.
- **F.** The composition lines passed within a few pixels of the ReactionWheel and StarTracker
  headers (a line meets a same-height neighbour with a margin of slope times gap). Revision 6 orders
  the parts of the row so that the boxes of greatest height are spread with a shorter box between
  any two; the model's order is kept for the rest. Looked at at 2000 px
  (`assembly_2000.png`, below) and at 700 px: no line crosses or touches a box header; no crossing
  remains. The type grows from 9.0 to 9.6 px (the frame is 260 px tall against 245).
- **The pair.** `diagnostic_pair.py` no longer sets a panel title (`tau_sweep_figure` names the
  regime) and draws both regimes with one `vmax` (`shared_vmax`, the larger of the two sweeps' tops:
  0.435 on the data of record); `k3_record.md` states it ("Both heatmaps share one colour scale,
  from white at 0.001 to 0.435 ..."). The gate folder (`WP23-rounds/gate/`) is not re-rendered; no
  test pins it. Identifier renames (`facet_table`, `facet_`) are left to WP24.

Renders looked at (session scratchpad, 700 px unless named): before,
`wp23views-renders/before/assembly_view.png` and `behavioural_view.png`; after,
`wp23views-renders/after/assembly_view.png` and `behavioural_view.png` (byte-identical to the
committed ones), `wp23views-renders/zoom/assembly_2000.png` (the crossing check); the pair on
`examples/adcs/data/v2/*.csv`, `wp23views-renders/pair/heatmap.png` and `heatmap_baseline.png` (both
panels' scales end at 0.43, both named by regime). The behavioural view's lanes, lines and dashed
group are as before; the analysis box is wider by one word of text, the type unchanged (9.2 px).

## Acceptance review (work-acceptance, 2026-11-10)

| | |
|---|---|
| **Scope of work** | `work-packages/WP23-scope-of-work.md` (decisions folded in at 0769209) |
| **Scope approval verified** | `WP23-decisions.md`, "Scope gate (2026-11-09, 21:10)": "**Approved for execution by the driver under the mandate**, with the draft amended to these decisions"; the scope's gate line: "2026-11-09, 21:10: approved for execution by the driver under the mandate" (59f83ac) |
| **Work reviewed** | `dev` from 7ffb719 to ff5eb39, the commits labelled WP23 (af37cb1 to 0fab294); ea46637 and 628df90 (the paper's move) are WP16's order step (4), their own unit, and are not reviewed here |
| **Supervisor (accepts)** | mzargham; the acceptance is the driver's under his mandate ("Proceed, I review after") |
| **Acceptance record** | the supervisor's (here the driver's) verbal acceptance, quoted verbatim in `WP23-decisions.md`, after this review |

Run by a fresh reviewer in worktree `wp23accept` (origin/dev ff5eb39, `uv sync --locked`). Every
check below was run now; renders and regenerations went to the session scratchpad
`wp23accept-renders/`, never into the repository.

### Deliverables

| ID | Verdict | Evidence |
|---|---|---|
| D-1 | met | `examples/adcs/model_v2/cubesat.sysml` (871 lines; `cubesat_r2.sysml` gone after the swap, as scoped): `launchRate = 6000.0` (l. 225), `calc def LaunchCost` rate times total mass (l. 320-325), `LaunchBudgetRequirement` (l. 683), MoE/MoP as the first word of each metric's `doc` (ten marks, l. 281-584), the four new requirements, `SettledRequirement` with the fold, the measurement's simulator inputs listed in `coverage.md` |
| D-2 | met | `coverage.py`, `views/coverage.{md,csv}`, `tests/test_model_coverage.py`; `uv run python examples/adcs/model_v2/coverage.py --out <scratch>/coverage-full` (17 s, "7 disagreement(s)") is byte-identical to the committed `coverage.md` and `coverage.csv` on this Mac; `--no-empirical` runs too |
| D-3 | met | `cubesat_oracle.py`, `definitions.py`, `compare.py` changed (D-3 commits 7b9f05e, d60b1ea, 8b29bfa); the oracle has no slew-time output (grep: the docstring only). The three listed generator files `cubesat_model.py`, `generate_dataset.py`, `make_check_designs.py` are unchanged: they make the frozen data (G-8) |
| D-4 | met | amendment row 12 in `interface-contract.md` (slew-time columns out, no `launch_cost`, nine traded metrics, the approval named); `contract_version = 12`; the v2 header has no slew-time column |
| D-5 | met | `examples/adcs/model_v2/views/{assembly,behavioural}_view.{puml,svg,png}` and the two caption files, `project.py` revision 6. Looked at both PNGs at 700 px: the assembly view marks the two swaps and four tunes once each and agrees with `assembly_caption.md` (levels, ranges, the gain box of each regime); no composition line crosses a header. The behavioural view has the nine metrics, each with its requirement line, seven arrows from `SlewExperiment` and the control effort's from `SlewMeasurement`, as `behavioural_caption.md` says; the mass chain requirement, launch cost, `totalMass`, total mass is readable; the dashed group is the three requirements that read no traded metric |
| D-6 | not met (in part) | `WP23-rounds/round-{1,3,4}/` hold the five files; `round-2/` holds the views and `INTENT.md` only, no heatmap, `coverage.md` or `k3_record.md` (G-4). The gate pair regenerated now (`diagnostic_pair.py ... --out <scratch>/wp23accept-renders/`, 40 s) reads the same as `gate/k3_record.md` on the K = 1 sets, the zero sets and every printed exponent, and differs where later units changed the code (G-9) |
| D-7 | not met (in part) | `examples/adcs/case-model.md`, "From the assembly to the dataset ..." with its five subsections, present; the glossary entries for MoE, MoP and launch cost are drafted in this record and not in `glossary.yaml` (G-6) |
| D-8 | met | ledger: `v2-primary@5`, `v2-baseline@5`, `v2-check-predictions@5`, `v2-check-designs@5`, `scope-sensitivity-shared-subspace-v2@4`, commit 2b2e94e, not dirty (`gate/README.md`); `PYTHONPATH=examples/adcs uv run python -m experiments verify`: "34 entries (11 current); 0 drifts"; `paper/container/RECORD.md` names `3c7cfc8a2e27`; `tests/data/v2_first_designs_of_record.csv` regenerated |
| D-9 | met | `swap-evidence.md`, "WP23 data gate: old v2 ... against new v2": changed conclusions first, every moved column with its cause, the conclusions item by item, the slot list (its section 4) |
| D-10 | met | this file: the four rounds, the cold reads by reference to `round-{1,3}/cold-reads.md` with dispositions, the K = 1 and K = 3 readings, the trace table, the zero exponents explained (n-lemma reading); the texture record is short of R-9 (G-5) |

### Requirements

| ID | Verdict | Evidence |
|---|---|---|
| R-1 | met | `uv run pytest -q -m "not slow" tests/test_cubesat_model.py tests/test_cubesat_oracle.py tests/test_check_designs.py tests/test_v2_data.py tests/test_experiments.py tests/test_model_coverage.py tests/test_system_model_v2_r1.py tests/test_diagnostic_pair.py tests/test_interface_contract.py -n auto`: "258 passed in 89.95s"; `coverage.md` table 1: six rows, none empty in either column |
| R-2 | met | same run (`test_every_traded_metric_has_a_requirement_that_reads_it_and_a_mark`); `coverage.md` table 2; the behavioural view, looked at: no dashed "no requirement" box |
| R-3 | met | the model diff 7ffb719...HEAD outside comments and docs adds the literals `1.0` (1/h), `6000.0`, `1.2` and the `1.0 [unit]` normalisation, each traced in "Proposed thresholds" above |
| R-4 | met | `REQUIRE_OPENSYSML=1 uv run pytest -q tests/test_model_checking_v2.py tests/test_system_model_v2.py`: "90 passed", among them `test_launch_cost_is_the_rate_times_the_total_mass_and_increases_with_it` (three named configurations) |
| R-5 | not met as stated | `grep -rn "slew_time\|SlewTime" examples/adcs/model_v2/cubesat.sysml examples/adcs/data/v2`: nothing in the data; seven model lines, the section-4 calcs `TorqueLimitedSlewTime`, `LinearSlewTime`, `SlewTimeEstimate`; `grep` of `cubesat_model.py` finds `slew_time_s` and `slew_time_05deg_s` in `measure` (l. 444, 469: the frozen generator). Met under the reading "R-5's check, amended" (measurement, requirements and experiment clean; `test_slew_time_has_left_the_measurement_and_the_requirements` passes), which the PM recorded for the driver; no driver ruling on it is recorded (G-1) |
| R-6 | met | the 258-test run includes `test_interface_contract.py` and `test_v2_data.py` |
| R-7 | not met as stated | WP23's commits touch nothing under `src/` or `derivation/`, no frozen data, `case.py` or `k_terms.py`, and under `docs/` only `project.py`; under `paper/` they touch `container/RECORD.md` and also `figures/fig-assembly-view.png` and `fig-behavioural-view.png` (8507bd9, authorized by the PM at the push and stated in `gate/README.md`; again in 0fab294) (G-2) |
| R-8 | not met (in part) | rounds 1 and 3 were cold read by a fresh P2 and P3 (`round-1/cold-reads.md`, `round-3/cold-reads.md`, findings verbatim with dispositions); rounds 2 and 4 and the post-gate revision 6 of the views were not (G-3) |
| R-9 | not met (in part) | every zero exponent has a stated reason (round 3; `case-model.md`, "The texture hypothesis ..."); there is no "Texture" section recording the heatmap before (the frozen `fig-tau-sweep`) and after, and the prose states the outcome on the round-1 data "not a result of record" although the gate shows the same zero sets on the data of record (G-5) |
| R-10 | met | the 258-test run (`test_model_coverage.py`, `test_system_model_v2_r1.py`); my two regenerations of the table equal the committed bytes |
| R-11 | met | the R-4 run with `REQUIRE_OPENSYSML=1`: 90 passed |
| R-12 | met | as D-8 |
| R-13 | met | D-9 read by the driver: `WP23-decisions.md`, "The data gate: the comparison read, two calls (2026-11-10, 02:25)" and "The swap is final (2026-11-10, 02:45)" |
| R-14 | not checkable (vocabulary); met (claims) | the claims reading above ("Case prose (D-7): claims") backs every row; `uv run python scripts/check_vocabulary.py` reports 70 violations, none in a WP23 file, because `case-model.md` is outside the tool's corpus; the tool run with `--root` on a scratch tree holding `glossary.yaml` and the case prose reports two `stem` findings in it, "launch rate" and "power margin" (G-7) |
| R-15 | met at the gate | `uv run ruff check .`: "All checks passed!"; `uv run ruff format --check .`: "323 files already formatted"; `uv lock --check`: resolves; Linux green on 8507bd9 and the Mac watcher green on 241c63d (`WP23-decisions.md`, 02:45). At ff5eb39 the full suite on this Mac: "2 failed, 2225 passed, 16 skipped, 1 xfailed", both failures outside WP23 (G-10) |

### Definition of good enough

| Item | Verdict | Evidence |
|---|---|---|
| Coverage table complete (R-1, R-10) | met | R-1, R-10 |
| Every metric's requirement or MoE in the model; no dashed box (R-2, R-3, R-4) | met | R-2 to R-4; the behavioural view looked at |
| The four proposed thresholds with rationale for the popup, with candidate metrics (OD3 to OD7) | met | "Proposed thresholds" and "Proposed thresholds, revised for the gate popup"; OD7 candidates (peak charge rate, recharge in the power margin, the battery swap) in "Round 2" and "Round 3"; the popup is pending the supervisor |
| Slew time out, the fold, contract amended, its test passing (R-5, R-6) | not met as stated | R-6 met; R-5 met only under the amended reading (G-1) |
| At least two rounds; last cold reads clean, or the cap reached with each open finding disposed | met | four rounds, the cap; open findings A to F disposed by the PM ("Rounds: the cold reads ..."), B, C, D, F executed in the post-gate unit |
| Regenerated once in `hts-paper`; D-9 complete; changed conclusions resolved or with the driver (R-12, R-13) | met | R-12, R-13 |
| Texture outcome and each zero explained in review and prose (R-9) | not met (in part) | G-5 |
| R-7, R-11, R-14, R-15 hold | not met (in part) | R-11 and R-15 met; R-7 (G-2); R-14 vocabulary not checkable (G-7) |

### Outside the scope

- **Out-of-scope changes (WP23's own commits):** `examples/adcs/experiments/check_designs.py`
  (8b29bfa; the reach rule 0fab21a, which the driver's decision names), `feasibility.py` and
  `sensitivity.py` (8b29bfa, D-3's column change), `tests/test_check_script.py` (59c3407),
  `tests/test_diagnostic_pair.py` (new, beside D-6), the two paper figures (G-2). Every other file in
  `git diff --stat 7ffb719...HEAD` over the model, experiments, v2 data, contract and tests that WP23
  did not write belongs to other units (ea46637 and 628df90: WP16 order step (4), the paper's move,
  its own unit and left there; af6948c, 241c63d: WP19's heatmap redraw; 0be3449: WP24; 18d0064,
  3d6d48a, 0059264, 4b5a539, 73c14e5, 9e08ae3: library and docs units) (G-8).
- **Non-goals touched:** the paper (two binary figures, byte copies of the regenerated views; no
  prose or number) (G-2). Untouched: `src/`, `derivation/`, the fit; the swap was made at the
  recorded gate; no constant chosen for the heatmap (round 3 changed none); thresholds labelled
  proposed; frozen data, `case.py`, `k_terms.py` (by WP23); `adcs_sim.py`, sampling and seeds; WP22c
  and the search.

### Observations

- The gate folder is a record of the gate run and no longer what the generator gives at head (G-9).
- The full suite's two failures at ff5eb39 are the paper move's (G-10); 4a04e72 on `dev` already
  routes them.
- "Coverage table, platform stability" says the Mac differs from the committed table in one magnitude;
  on the data of record the Mac regeneration today is byte-identical to the committed table.

### Open decisions (for the driver)

Each gap with the three dispositions: accept as is (with a reason) / fix before acceptance / follow-up
work package.

- **G-1.** R-5's literal check fails (the model's section-4 `SlewTime` calc names; the frozen
  generator `cubesat_model.py` still measures slew time); the amended reading is the PM's, with no
  driver ruling recorded. Affects good enough (slew time out).
- **G-2.** Non-goal and R-7: WP23 changed `paper/figures/fig-assembly-view.png` and
  `fig-behavioural-view.png` (8507bd9, PM-authorized at the push; 0fab294). Affects good enough (R-7).
- **G-3.** R-8: no P2/P3 cold read of rounds 2 and 4 or of the views' post-gate revision 6; the
  committed views were read only by their author.
- **G-4.** D-6: `round-2/` has no heatmap, `coverage.md` or `k3_record.md`.
- **G-5.** R-9: no before-and-after texture record in this review; the case prose's outcome paragraph
  stays on the round-1 data "not a result of record" after the gate. Affects good enough (R-9).
- **G-6.** D-7: the glossary entries MoE, MoP and launch cost are held, not in `glossary.yaml`; no
  decision on holding them is recorded.
- **G-7.** R-14: the vocabulary tool does not read `case-model.md`; run on it from a scratch root it
  reports two `stem` findings ("launch rate", "power margin"). Affects good enough (R-14).
- **G-8.** Out of scope: the five WP23-written files outside the blast radius named above; D-3's
  three generator files unchanged.
- **G-9.** Observation: `WP23-rounds/gate/` differs from a regeneration at head (the shared colour
  scale sentence, the redrawn heatmap, a per-term K = 3 report table where the gate record says it
  refused, exponent noise at 1e-17; the gate copy of `coverage.md` lacks the post-gate prose).
- **G-10.** Observation, not WP23's: `tests/test_soft_fit.py::test_r2_default_cubesat_fits_equal_the_recording[primary]`
  and `[stock]` (slow) fail at head, the K = 2 tau recorded 113.2 against 94.4 observed, since ea46637
  made the nine-metric data the default; routed in 4a04e72.

Recorded decisions pending the supervisor, not reopened here (`driver-log.md`, "Waiting for the
supervisor"): the four thresholds and the discharge rate (the popup tables above); the two metric
redundancies (eclipse reserve with depth of discharge; power margin with energy balance); whether
proposals that fail a model requirement count as check designs.

### Gap dispositions

| Gap | Disposition | Reason or follow-up |
|---|---|---|
| G-1 to G-10 | open: the driver's | |

### Recommendation

Recommend acceptance with the listed gaps noted, because every deliverable that carries the case
exists and runs as recorded here (the model, the coverage table reproduced byte for byte, the views
looked at against their captions, the ledger at 0 drifts, the gate comparison read and decided) and
no gap moves a number or a conclusion of record; the gaps are literal checks the record replaced by
readings (G-1, G-2), cold reads and folder contents short of R-8 and D-6 (G-3, G-4), and record and
prose items (G-5 to G-7); four of them touch good-enough items and need the driver's disposition
first (G-1, G-2, G-5, G-7).

Acceptance is the supervisor's act (here the driver's under his mandate), recorded in
`WP23-decisions.md`. This report does not accept the work.

## G-3: cold reads of the views at revision 6 (2026-11-10)

The driver's acceptance condition for WP23 (`WP23-decisions.md`, "Acceptance review (f5a63c2): the driver's gap dispositions", G-3): two fresh cold reads of the committed views at revision 6, image before caption. The views are `examples/adcs/model_v2/views/assembly_view.png` (700 x 260) and `behavioural_view.png` (700 x 910), as committed in 0fab294 and unchanged since. Each reader was a fresh general-purpose subagent in its own context (a P2 practitioner at depth L-B, a P3 modeller at depth L-C; `reader-grid.md`), run in parallel, given only the persona and depth, the assembly image, the behavioural image, then the two caption files, and the return format (recall, sentence, friction, numbered findings); neither saw the review record, the model, the earlier reads, the other's return or the brief. The round-3 prompt text is not kept in the record, so the prompts follow its return format; they are kept in the session scratchpad (`g3reads-prompts/prompt-P2-L-B.txt`, `prompt-P3-L-C.txt`). The returns are quoted as written (the guillemets around the stereotypes dropped; nothing else edited). This section changes no view: the generator and the views belong to the unit named in the dispositions.

Three findings are tagged [blocks] (P2 findings 1 and 2, P3 finding 1), all on the behavioural view. Their dispositions are executed in one follow-up unit, named below, which also carries the three smaller behavioural-view items that share its files.

**Texture record for R-9 (G-5).** The before-and-after record of the zero-exponent sets is D-9's "Changed conclusions" in `swap-evidence.md` (item 1, the contending sets, with item 7, what is unchanged: three metrics at zero in the primary regime, one in the baseline) and the diagnostic pair at the gate (`WP23-rounds/gate/k3_record.md`, `heatmap.png`, `heatmap_baseline.png`), as the driver recorded in `WP23-decisions.md`.

### G-3, P2 proxy (practising engineer, depth L-B), fresh context, image before caption. Verbatim.

> RECALL
> Assembly view: a part tree. Cubesat is composed of eight parts: ReactionWheel, Bus, SolarPanel, Battery, StarTracker, Antenna, Imu and Controller. The wheel and the tracker are abstract, each with three concrete alternatives (Small/Medium/LargeWheel; Coarse/Medium/FineTracker). Orange "swap" marks a categorical choice (wheelClass, grade). Blue "tune" marks a continuous parameter (panelSpan, batteryCapacity, Kp, Kd). Bus, Antenna and Imu are fixed. After the caption: it adds the levels and ranges that the image lacks (the enum levels, the span and capacity ranges, and the Kp ranges that differ by regime), so the image alone gives variable names and kinds but no ranges.
>
> Behavioural view: requirements (orange) each point to the traded metric they read (green), and each requirement carries a verification name (SlewVerification or ConfigurationVerification). Metrics are grouped in the analyst's boxes: controls, power and energy, and mass. Three requirements read no traded metric and sit in a dashed box at the top. SlewExperiment (purple, an analysis) feeds arrows to most metrics. SlewMeasurement (grey) feeds control effort and settling time. LaunchCost (yellow) is derived and not traded; it hangs off totalMass. After the caption: the SlewExperiment returns 8 of the 9 traded metrics; settling time comes from SlewMeasurement, not from the analysis. Control effort is passed through unchanged, which is why its arrow starts at SlewMeasurement. The groups are the analyst's own, not the model's. Coupling variables are deliberately not drawn.
>
> SENTENCE
> Assembly: "A cubesat is assembled from eight parts; the wheel and the tracker are chosen from three alternatives each (swap), four parameters are tuned over a range, and three parts are fixed."
> Behavioural: "Each requirement reads one traded metric, the metrics are produced by a slew experiment or a measurement, and three requirements and one derived cost sit outside that chain."
>
> FRICTION
> Assembly view: at 700 px the image is close to its native width, so it is legible. The legend text is small but readable. The "part def" stereotype and the part-def names in parentheses (wheel, tracker, panelPlus/panelMinus) are small and unexplained: what is the difference between the bold name and the parenthetical? "panelPlus, panelMinus" is a mystery, as is what "abstract" means to a trade-study reader. Filled diamonds (composition) and hollow triangles (specialisation) are UML notation with no legend entry. I read the swap boxes as ordinary parts until I read the legend. The Kp/Kd ranges are not in the image at all. Controller shows Kp and Kd with no hint that they depend on regime.
> Behavioural view: it is tall and narrow, so at 700 px the text is about 8-9 px. The requirement sub-lines (e.g. "EclipsePeakLoad(c, peakTorque) <= BatteryPeakPower(c)") are barely readable, and the stereotypes MoP/MoE are tiny. I could not tell MoP from MoE without prior knowledge; the legend does not define them. The orange-brown lines (requirement to metric) and the grey arrows (data source to metric) are different things, but the legend does not say so. The grey arrows from SlewExperiment fan out and cross the group frames, and I could not tell which arrow ends where for control effort and pointing error. The arrow to pointing error crosses the controls box edge from far below. The SlewExperiment text ("returns 8 of the 9 metrics... Passed on as measured: control effort") is dense, and "passed on" is odd, since control effort's arrow actually comes from SlewMeasurement. The requirement-to-metric line to total mass is short and sits oddly: LaunchBudgetRequirement's line goes to LaunchCost (yellow), not to totalMass, and the "totalMass" label on the little connector is ambiguous. I took the yellow box as part of the mass group. The legend says "orange: requirement; green: traded metric; yellow: derived, not traded" but omits grey, purple and the dashed box. "Traded metric" and "9 metrics" are never counted visibly; I count 9 green boxes only after tallying. The dashed box says "read no traded metric", but the orange boxes in it do show SlewVerification etc., so I wondered what they do read (BatteryPeakPower, momentum capacity are not metrics?).
>
> FINDINGS
> 1. [blocks] Behavioural view: at 700 px the requirement expression lines and the MoP/MoE stereotypes are about 8-9 px and not reliably legible. Widen the view or enlarge the text.
> 2. [blocks] Behavioural view: the legend omits grey (measurement), purple (analysis), the dashed box, and the two line kinds (brown = requirement reads metric; grey arrow = value comes from). I took the purple and grey boxes as just more requirements until I read the caption.
> 3. [changes the view] Behavioural view: LaunchBudgetRequirement links to LaunchCost, not to a traded metric, yet it sits in the mass group. The link to totalMass is a short line labelled "totalMass", which is unclear. Draw it as a derived-from edge and say so in the legend.
> 4. [changes the view] Behavioural view: the arrows from SlewExperiment run through the group frames and cross one another. The arrow to pointing error looks like it comes from the group above. Reroute them or add a "returns" label.
> 5. [changes the view] Behavioural view: MoP and MoE are not defined in the figure or the caption, and I could not tell what difference the colours or the groups make between them. Add a one-line gloss to the legend.
> 6. [changes the view] Behavioural view: the SlewExperiment box text says control effort is "passed on as measured", but the arrow for it starts at SlewMeasurement. The caption has to resolve this. Say so in the box text.
> 7. [changes the view] Assembly view: the UML symbols (filled diamond, hollow triangle, "part def", "abstract") are not in the legend. A trade-study reader will not know them. Add "composed of" and "alternative of".
> 8. [changes the view] Assembly view: the image gives the variables but no ranges. The Kp/Kd regime ranges exist only in the caption, so a skimming L-B reader sees tune without ranges. Consider a compact range line under each tune tag.
> 9. [note] Assembly view: "panelPlus, panelMinus" and the parenthetical part-def names are unexplained.
> 10. [note] Assembly view: the "each marked once" legend sentence reads well, and the swap/tune split is clear after the legend. The orange/blue contrast is good.
> 11. [note] Behavioural view: the three-group layout and the dashed "read no traded metric" box are an effective way to show the structure. The caption's explanation of why settling time and control effort are special is needed, because the image alone cannot say it.
> 12. [note] Both views use orange for different meanings (swap in assembly, requirement in behavioural). Across the paper this could mislead a reader who skims the figures side by side.

#### Dispositions of the G-3 P2 findings

- **G3-P2-1.** Disposition: executed in a named follow-up, the G-3 view unit (the generator `docs/superpowers/notes/spike-sysml-diagrams/project.py`, behavioural view; regenerate, render, re-check at 700 px). Tagged [blocks]: the render is 700 px wide natively and its smallest type is 9.2 px (requirement second lines, stereotypes, the `totalMass` label), which this reader calls not reliably legible. The unit raises the smallest type of the behavioural view.
- **G3-P2-2.** Disposition: executed in the G-3 view unit (the generator `docs/superpowers/notes/spike-sysml-diagrams/project.py`, behavioural view; regenerate, render, re-check at 700 px). Tagged [blocks]: the reader took the lilac and grey boxes for more requirements until the caption. Round 3 cut the legend to the colour key for legibility, and an earlier P3 read grey and lilac correctly cold (R3-P3-8), but two readers now stumble, so the unit adds grey (measurement), lilac (analysis) and the two line kinds to the legend at the type size of item 1. Same as G3-P3-2.
- **G3-P2-3.** Disposition: deferred into the G-3 view unit (the generator `docs/superpowers/notes/spike-sysml-diagrams/project.py`, behavioural view; regenerate, render, re-check at 700 px) with G3-P3-1 (one fix serves both): not blocking by itself, since the reader read the structure correctly after the caption. The requirement's line to the launch cost is the model's reading and stays.
- **G3-P2-4.** Disposition: no change: the arrows end on the right boxes in the render at 700 px; they cross a group frame at its right edge because the groups nest the metrics, and rerouting lengthens them (as R3-P2-5, the lines need the room). Same as G3-P3-7.
- **G3-P2-5.** Disposition: deferred into the G-3 view unit (the generator `docs/superpowers/notes/spike-sysml-diagrams/project.py`, behavioural view; regenerate, render, re-check at 700 px) as one sentence in `behavioural_caption.md` (the MoE/MoP rule; pointing error and launch cost are the two MoEs): round 4 recorded the rule as a caption item (R3-P2-3) and the committed caption does not carry it. Not blocking: the stereotype reads as a label. Same as G3-P3-4.
- **G3-P2-6.** Disposition: deferred into the G-3 view unit (the generator `docs/superpowers/notes/spike-sysml-diagrams/project.py`, behavioural view; regenerate, render, re-check at 700 px) as a wording change in the analysis box (control effort and settling time come from the measurement): the caption states it and both readers resolved it there, so not blocking. Same as G3-P3-3.
- **G3-P2-7.** Disposition: no change: the sentence test holds without a key for the symbols (both readers' cold sentences are right: swap, tune, fixed, eight parts); round 3's P2 read the triangle as one alternative chosen and found nothing false in it (R3-P2-13).
- **G3-P2-8.** Disposition: no change, by design: the levels and ranges left the image for the caption in round 4 (R3-P2-11, closed); the image carries which parts are swapped, tuned or fixed.
- **G3-P2-9.** Disposition: no change: closed in round 4 (the pair is named in the caption; the drawing stays at eight boxes, R3-P2-10).
- **G3-P2-10.** Disposition: no change: a note confirming the legend sentence and the swap and tune colours.
- **G3-P2-11.** Disposition: no change: a note confirming the layout and the caption's job.
- **G3-P2-12.** Disposition: no change: each figure carries its own key and the keys state the meanings; a recolouring would break the behavioural view's colour rule for a cross-figure reading that neither figure alone needs.

### G-3, P3 proxy (systems modeller, depth L-C), fresh context, image before caption. Verbatim.

> RECALL
> Assembly view: a SysML-style part-definition diagram. A "Cubesat" part def is built (filled-diamond composition lines) from eight parts: ReactionWheel (abstract; specialised by SmallWheel, MediumWheel, LargeWheel via hollow triangles), Bus, SolarPanel, Battery, StarTracker (abstract; specialised by CoarseTracker, MediumTracker, FineTracker), Antenna, Imu, Controller. Some attributes are tagged: orange "swap" (wheelClass, grade) means categorical choice among alternatives; blue "tune" (panelSpan, batteryCapacity, Kp, Kd) means a continuous parameter tuned in a range; untagged parts (Bus, Antenna, Imu) are fixed. The legend box says each variable is marked once, in the part it belongs to. After the caption: same reading, plus the concrete levels and ranges (enums, 0.3-1 m span, 20-200 Wh, and Kp/Kd ranges that differ by gain regime). The caption is a list of data, not an explanation of the picture.
>
> Behavioural view: requirements (orange boxes), traded metrics (green boxes, each typed MoP or MoE), one derived non-traded metric (yellow, LaunchCost, MoE), an analysis (purple SlewExperiment) and a measurement source (grey SlewMeasurement). Orange-brown plain lines join each requirement to the metric it reads. Grey arrows with open heads go from the source (SlewExperiment or SlewMeasurement) to the metrics it supplies. Three grey-background folders group metrics and their requirements (controls; power and energy; mass), labelled as the analyst's own grouping. A dashed box at the top holds three requirements that read no traded metric. Each requirement names a verification (SlewVerification or ConfigurationVerification). Reading: the purple analysis produces 8 of 9 metrics from the configuration, control effort and settling time come from measurement; pointing error and total mass need no slew. After the caption I understood why control effort's arrow starts at SlewMeasurement while the purple box text says it is "passed on as measured", and why settling time has no arrow from SlewExperiment.
>
> SENTENCE
> Assembly (written before the caption): "A cubesat is assembled from a handful of parts, and the choices to be traded are the orange 'swap' (pick one alternative of an abstract part) and blue 'tune' (set a number in a range) marks on wheel class, tracker grade, panel span, battery capacity and the controller gains."
> Behavioural (written before the caption): "Each requirement reads one metric; most metrics come out of a single slew experiment, two come from a measurement, and the mass group also has a derived launch-cost metric that is not traded."
>
> FRICTION
> Assembly:
> - At ~700 px the image is only about 700 px wide natively, so it is mostly legible; the smallest text (part parenthetical types such as "(panelPlus, panelMinus)", "(bus)", "(imu)") is small but readable. The filled-diamond composition ends are tiny at the Cubesat box; I read them as plain lines until I thought "SysML". A reader not versed in SysML will not know diamond = "is made of" or hollow triangle = "is a kind of"; the legend does not explain these line kinds.
> - "(wheel)", "(tracker)", "(controller)" in parentheses under names: I did not know what they are (the type? the role?). "abstract" is fine to a SysML reader only.
> - The diagram shows no ranges or levels; they are only in the caption. A reader sees "tune Kp, Kd" with no values in the picture.
> - The caption says Kp/Kd have "one range per regime" and mentions baselineGains/aggressiveGains regimes; nothing in the image says what a regime is, and the Controller shows one tag only. I took the Controller as having a single range from the image.
> - "Configuration variables (each marked once, in the part it belongs to)" is clear. "untagged: fixed (Bus, Antenna, Imu)" clear, though Battery/SolarPanel's "(panelPlus, panelMinus)" suggested sub-parts that are not drawn.
> Behavioural:
> - The text in the boxes is small at 700 px: the second lines (e.g. "EclipsePeakLoad(c, peakTorque) <= BatteryPeakPower(c)") in the dashed box are borderline; the metric labels (green, e.g. "depth of discharge MoP DepthOfDischarge") and the purple box text are readable but tight. The tiny "totalMass" edge label near the yellow box is hard to read and I could not tell what it labels until the caption-free reading of the vertical orange line (it joins total mass to launch cost, apparently "launch cost is derived from totalMass"). The yellow LaunchCost is joined to the LaunchBudgetRequirement by an orange line but also to totalMass by a short orange line: same line colour for "requirement reads metric" and "derived from", so I took the second for a requirement link at first.
> - Orange-brown lines (requirement reads metric) versus grey arrows (source supplies metric) are distinguishable, but grey arrows from SlewExperiment have long diagonal routes that cross the group frames; I could not always tell which arrow ends where without following carefully (the arrow to "pointing error" runs up beside the group frame).
> - The two kinds of arrowhead I took as identical; the arrows from SlewMeasurement and SlewExperiment look the same, so provenance is told only by the origin box colour (grey vs purple).
> - "MoP" and "MoE" are unexplained in the image and legend (I know measure of performance/effectiveness, but a modeller from outside systems engineering may not). It is unclear why pointing error is an MoE and the others MoP; the picture gives no basis for the distinction.
> - The legend ("orange: requirement; green: traded metric; yellow: derived, not traded") omits grey (measurement), purple (analysis), the folders, the dashed box, and the two line kinds. Purple and grey are only explained by the box's own text.
> - "the analyst's grouping" in the folder titles: clear in intent, but the function of the groups (why group at all) is not apparent from the image.
> - Purple box text "returns 8 of the 9 metrics ... Passed on as measured: control effort." is cryptic without the caption: control effort is listed as a passed-through input, yet the arrow to it comes from SlewMeasurement, not from the experiment. I took this for an inconsistency until the caption.
> - The nine-metric count: I counted green boxes (control effort, settling time, pointing error, energy balance, power margin, depth of discharge, peak slew power, eclipse reserve, total mass) = 9, matches.
> - The dashed-box requirements (3) "read no traded metric" - understood, but "ConfigurationVerification" for PowerRequirement and "SlewVerification" for the others is not explained in the image; verification is a named thing I do not know what it is.
>
> FINDINGS
> 1. [blocks] The "totalMass" edge label between total mass and launch cost is too small to read at 700 px, and its orange line is the same colour and style as requirement-reads-metric lines, so the derivation is read as a requirement link. Behavioural view.
> 2. [changes the view] The legend omits grey (measurement), purple (analysis), the grey arrow meaning (supplies), the orange line meaning (reads) versus the derived-from line, the folders and the dashed box. Behavioural view.
> 3. [changes the view] Control effort's arrow comes from SlewMeasurement while the purple analysis box says control effort is "passed on as measured"; without the caption this looks contradictory. The purple box wording should say plainly that control effort and settling time come from the measurement, not the analysis. Behavioural view.
> 4. [changes the view] MoP versus MoE is unexplained and applied inconsistently-looking (pointing error MoE, other grouped metrics MoP); LaunchCost is also MoE. A legend line or a word is needed. Behavioural view.
> 5. [changes the view] Diamond (composition) and hollow-triangle (specialisation) line kinds, "abstract", and the parenthetical names under part names (wheel, tracker, controller, panelPlus/panelMinus) are not explained; a non-SysML reader cannot tell them from decoration. Assembly view.
> 6. [changes the view] The ranges and levels are absent from the picture and only in the caption, so the picture cannot be read for "what are the trade variables' values"; and the caption's Kp/Kd regimes (baseline vs primary/aggressive) are not visible anywhere in the diagram. Assembly view.
> 7. [changes the view] Grey arrows from SlewExperiment run long diagonal routes crossing group frames; hard to follow to the right endpoint, especially to pointing error and total mass. Behavioural view.
> 8. [note] Smallest text in both images (parenthetical types, requirement bodies in the dashed box, the legend text) is borderline legible at 700 px but readable; the behavioural view is the tighter. Both views.
> 9. [note] Verification names (SlewVerification, ConfigurationVerification) appear on every requirement but their meaning is unexplained in the image; only the caption says which metrics need a slew. Behavioural view.
> 10. [note] The caption of the behavioural view usefully says what is not drawn (coupling variables, measured inputs) and points to coverage.md; the assembly caption says nothing about how the view relates to the behavioural one (which parts feed which metrics), so a modeller cannot see from either view where their own evaluation plugs in. Both views.

#### Dispositions of the G-3 P3 findings

- **G3-P3-1.** Disposition: executed in the G-3 view unit (the generator `docs/superpowers/notes/spike-sysml-diagrams/project.py`, behavioural view; regenerate, render, re-check at 700 px). Tagged [blocks]: the label cannot be read at 700 px and the derived-from line is taken for a requirement link. The unit sets the `totalMass` label at the type size of G3-P2-1 and draws that line as a different kind from the requirement-reads-metric line, with the legend naming it.
- **G3-P3-2.** Disposition: as G3-P2-2 (executed in the same unit).
- **G3-P3-3.** Disposition: as G3-P2-6 (deferred into the same unit, the box wording).
- **G3-P3-4.** Disposition: as G3-P2-5 (deferred into the same unit, one caption sentence).
- **G3-P3-5.** Disposition: as G3-P2-7: no change; the reader's own sentence read swap and tune correctly.
- **G3-P3-6.** Disposition: no change, by design (as G3-P2-8); the caption names each regime with its gain box (`baselineGains`, `aggressiveGains`), which closes R3-P3-13; the Controller box cannot carry two ranges without the range text round 4 removed.
- **G3-P3-7.** Disposition: as G3-P2-4: no change.
- **G3-P3-8.** Disposition: as G3-P2-1: addressed by the type-size change in the same unit.
- **G3-P3-9.** Disposition: no change: the caption states which requirements are verified in `ConfigurationVerification` and why; the names are the model's.
- **G3-P3-10.** Disposition: no change, by design: the behavioural view is the 'what is evaluated' half and the assembly view the 'what is varied' half; the link from configuration variables to metrics is the coverage table's first table (open item E of 'Rounds', disposed by the PM as by design).

**Count.** P2: 12 findings (2 [blocks], 6 [changes the view], 4 [note]); P3: 10 findings (1 [blocks], 6 [changes the view], 3 [note]). The assembly view has no blocking finding.

## Behavioural view, revision 7 (G-3 blocks)

The G-3 view unit: dispositions G3-P2-1, G3-P2-2, G3-P2-3, G3-P2-5, G3-P2-6 and G3-P3-1 to G3-P3-4, executed in `docs/superpowers/notes/spike-sysml-diagrams/project.py` (`--revision 7`, now the default; revisions 3 to 6 reproduce the earlier text). Recipe checked first: the committed revision-6 `behavioural_view.puml` and `assembly_view.puml`, re-rendered by `render.sh` (PlantUML 1.2026.8), gave the committed PNG and SVG bytes. Revision 7 regenerates the behavioural view, its caption and its two images; the assembly view's sources and `fig-assembly-view.png` are byte-identical (no shared setting moved). `paper/figures/fig-behavioural-view.png` is a byte copy of the new image.

**Type.** The smallest type at 700 px was 9.238 px (the SVG's font size: requirement second lines, the stereotypes, the `totalMass` label, all one size) and is 12.512 px now (the paper's 9 pt at 100 dpi is 12.5 px); the legend is set at 14.6 px. What was cut or changed to get there, nothing shrunk: the width that set the scale was the group of requirements that read no traded metric (three boxes side by side, one statement 330 px wide) and the analysis box (lines of 22 characters). The three statements now break before their comparison (`EclipsePeakLoad(c, peakTorque)` / `<= BatteryPeakPower(c)`), and the analysis box is rewritten in lines of at most 19 characters. The image is 1341 px tall against 910 (the type is larger and the lanes' gap is 24 against 16, so the dashed line has room).

**Per finding.**

- **G3-P2-1 (type).** Closed by the image: the smallest type is 12.5 px against 9.2; the requirement second lines, the stereotypes and the `totalMass` label read at 700 px. `tests/test_system_model_v2_r1.py` now pins a floor of 12.5 px on the committed SVG.
- **G3-P2-2 and G3-P3-2 (legend).** Closed: the legend carries the five colours (requirement, traded metric, derived and not traded, analysis, measurement) as swatches of the box colours, and the three line kinds (requirement reads metric; computed from; value comes from) in three lines; the folders and the dashed group are titled in the drawing and stay out of the legend; the rest stays in the caption.
- **G3-P3-1 and G3-P2-3 (`totalMass` label and the launch-cost line).** Closed: the label is at body size (12.5 px), and the line from the launch cost to the total mass is dashed and thicker, the one dashed relation line, named in the legend ("computed from") and in the caption; the requirement's line to the launch cost stays solid, a requirement line. The dashes are fine at 700 px; they are seen, not measured.
- **G3-P2-5 and G3-P3-4 (MoE and MoP).** Closed in the caption: one sentence, generated from the model's marks (a metric marked MoE is one a stakeholder states without knowing the design, here the pointing error and the launch cost; MoP is a measure of performance under the engineer's scenario, here the others), with the sentence on the dashed line. The words follow `glossary.yaml`'s entries.
- **G3-P2-6 and G3-P3-3 (analysis box).** Closed: the box reads "returns 8 of 9 metrics. No slew for pointing error, total mass. From the measurement: control effort (passed on) and settling time (not returned)." The names are found from the model, as before; no word of the measurement's two entries is typed.
- Not changed, by their dispositions: G3-P2-4 and G3-P3-7 (arrow routes).

**Pins that followed strings** (no requirement weakened): the analysis box reads "returns 8 of 9" and names both measurement entries; the count of thickness-2 lines is the requirement lines (the MoE's second line is thickness 3 and dashed, counted separately); the analysis colour is used by one box (the legend's swatch is not a box); one new test, the legend names each colour and line kind, the caption carries the MoE rule, the type floor.

**Paper caption.** `paper/paper.ipynb`, cell `fig-behavioural-caption`: nothing it says is stale ("yellow: derived, not traded" still holds); the paper stream may add "a dashed line joins the launch cost to the total mass it is computed from" (the paper stream's, not made here).

Renders looked at (session scratchpad `wp23view7-renders/`, 700 px): `before/behavioural_view.png` (revision 6); `exp/e1.png` to `e3.png` (the layouts tried: no second lines, wrapped statements side by side, stacked); `gen7/behavioural_view.png` (the generator's output, byte-identical to the committed image) and `after/behavioural_view.png`; `r6check/` (the revision-6 recipe check).

## G-3: P3 cold read of revision 7 (2026-11-10)

The driver's acceptance condition: one fresh P3 cold read (a modeller at depth L-C), image before caption, of the committed revision-7 views, `examples/adcs/model_v2/views/behavioural_view.png` (700 x 1341) and `assembly_view.png` (700 x 260), with their caption files. The reader was a fresh general-purpose subagent (sonnet) in its own context; it was given the persona and depth, the two images, the two caption files and the return format, and no record, model, earlier read or brief. The prompt is the revision-6 P3 prompt verbatim with the file paths pointed at the committed revision-7 files (session scratchpad `g3reads-prompts/prompt-P3-L-C-rev7.txt`; the return is `p3-rev7.txt` beside it). The return is quoted as written. This section changes no view.

### Return, verbatim

> RECALL:
> Assembly view. Before the caption: a Cubesat part definition built from nine parts (diamond-ended lines mean "composed of"). ReactionWheel and StarTracker are abstract, each with three specialisations (hollow-triangle arrows). Orange "swap" tags mark categorical choices (wheelClass, grade). Blue "tune" tags mark continuous parameters (panelSpan, batteryCapacity, Kp/Kd). Bus, Antenna and Imu are fixed. After the caption: same, plus the actual levels and ranges (wheelClass small/medium/large, panelSpan 0.3-1 m, Kp and Kd ranges per regime). The caption supplies the numbers the figure lacks.
>
> Behavioural view. Before the caption: requirements (peach boxes, bold name plus the verification they belong to) joined by solid rust lines to metrics (green boxes). The metrics are grouped into "controls", "power and energy" and "mass". A grey box (SlewMeasurement) and a purple box (SlewExperiment) feed values into the metrics through grey arrows. One yellow metric (launch cost) hangs from total mass by a dashed line. Three requirements sit in a dashed box at the top because they read no traded metric. After the caption: the purple analysis returns 8 of 9 metrics. Control effort goes through the analysis unchanged, so its arrow starts at the measurement. Settling time is read from the measurement and not returned. MoE means a stakeholder-stated effectiveness measure and MoP means an engineer's scenario performance measure. The groups are the analyst's own, not model structure. The dashed line joins a derived quantity to what it is computed from.
>
> SENTENCE:
> Assembly: "A Cubesat is composed of nine parts, of which a few carry swappable categorical choices (swap) or tunable continuous parameters (tune)."
> Behavioural: "Requirements read metrics, and an analysis and a measurement supply the metric values, with the metrics grouped by theme."
>
> FRICTION:
> Assembly view, at 700 px the fonts are readable. Specific issues:
> - The diagram never says which of the swap/tune items are the actual design variables for the evaluation. The legend says "configuration variables", which is clear enough, but the figure gives no ranges. I only got them from the caption. A reader of the figure alone sees tune panelSpan with no range or units.
> - Kp and Kd both sit under Controller with no sign that they have regime-dependent ranges. The caption says "one range per regime" but the figure shows no regimes.
> - The meaning of the parenthesised lowercase names, e.g. "ReactionWheel (wheel)", is not explained. They look like usage names. "<<part def>>" appears only on Cubesat and the others are not labelled as part defs or usages. The arrow-type difference (filled diamond vs hollow triangle) is not in the legend. A SysML reader will know it; a non-SysML modeller may not.
> - "SolarPanel (panelPlus, panelMinus)" has two usage names and the meaning of that is not explained.
>
> Behavioural view, at 700 px the box body text is small but readable. The SlewExperiment box text is tiny and dense, and the legend is small. Specific issues:
> - The legend's "computed from" swatch is a dotted line, while in the figure the line is a short dashed segment (launch cost to total mass). They are distinguishable but the legend sample is faint. The line is also very short, so I almost took it for a stub or a border.
> - Arrow semantics: "value comes from" arrows point from the metric toward... actually the arrowheads sit at the metric end, with the tail at the source. I read this correctly only through the legend. Reading the figure alone, I would have taken the arrows as "analysis consumes metric".
> - The arrows from SlewExperiment fan out and cross the group frames, and the one to pointing error runs a long diagonal. I could not tell from the arrows alone which metrics the experiment does not return; the box text states it in prose ("No slew for pointing error, total mass") but the arrows' absence is the real signal. Pointing error does get an arrow from SlewExperiment, which seems to contradict "no slew for pointing error". The caption explains that the analysis returns it from the configuration alone, but this is confusing.
> - "SlewMeasurement" arrows go to control effort and settling time. The box text says control effort is "passed on" by SlewExperiment, but SlewExperiment has no arrow to control effort. The text reads as a contradiction until the caption is read.
> - The requirement names carry "SlewVerification" or "ConfigurationVerification" as a subtitle. This is never explained in the figure, and the caption only says which requirements are verified where. I took it for a type or class name at first.
> - The yellow "derived, not traded" box is also marked <<MoE>>, while the green traded ones are mostly MoP, and pointing error (green) is also MoE. So colour does not map to MoE/MoP, only the stereotype does. The legend does not explain MoE/MoP, abbreviations that appear only in the caption.
> - The line from LaunchBudgetRequirement to launch cost is a solid requirement-reads-metric line, but launch cost is the derived, not-traded metric. This conflicts with the legend wording, where the solid line is "requirement reads metric" and the box is "derived, not traded". It is not obvious why launch cost is a requirement target but not traded.
> - The top dashed box has a title but is not in the legend. The "(the analyst's grouping)" frames are explained only in the caption.
> - "peakTorque", "c.momentumCapacity" and the other expressions in the top box cannot be parsed without the model.
>
> FINDINGS:
> 1. [blocks] The "value comes from" arrows read as consumption unless the legend is read, and the arrowhead points at the metric, which is the destination of the value. Needs a clearer direction cue or label. Behavioural view.
> 2. [blocks] The SlewExperiment box says "control effort (passed on)" but no arrow runs from it to control effort, and the box also says "No slew for pointing error" while an arrow does run to pointing error. The text and the arrows look contradictory without the caption. Behavioural view.
> 3. [changes the view] MoE and MoP appear on every metric but are defined only in the caption, not the legend. The colours do not track them: green holds both MoP and MoE, and yellow is MoE. Add them to the legend, or state that colour means traded and the stereotype means kind. Behavioural view.
> 4. [changes the view] "SlewVerification" and "ConfigurationVerification" under each requirement are unexplained in the figure. Say what they are (the verification each requirement is checked in), and consider a legend entry. Behavioural view.
> 5. [changes the view] The dashed "computed from" line is very short and the legend sample is faint at 700 px. Behavioural view.
> 6. [changes the view] The solid line from LaunchBudgetRequirement to the yellow "derived, not traded" launch cost conflicts with how the legend words the colours. A reader asks how a requirement reads a metric that is not traded. Behavioural view.
> 7. [changes the view] The assembly figure shows no ranges or units. The caption holds them (wheelClass levels, panelSpan 0.3-1 m, regime-dependent Kp/Kd). A modeller needs them at hand; put the key ranges in the figure or tie the caption to the tags. Assembly view.
> 8. [changes the view] The SysML notation is unexplained: filled diamond for composition, hollow triangle for specialisation, "(usage)" names in parentheses, "<<abstract>>", and the two usage names on SolarPanel. Add them to the legend, or one line in the caption. Assembly view.
> 9. [note] The SlewExperiment box text is small and dense at 700 px, though it can be read. Behavioural view.
> 10. [note] Metric-group frames and the top dashed box are explained only in the caption; "analyst's grouping" in the frame titles carries most of it. Behavioural view.
> 11. [note] The assembly view otherwise reads well at 700 px: the swap/tune tags, the legend and the fixed-part note are all legible. Assembly view.

### Dispositions of the G3r7-P3 findings

The test for [blocks] is the driver's: a reader taking the view for something it is not, or unable to read a label or legend entry at 700 px. The reader tagged findings 1 and 2 [blocks]; neither meets that test, as below. The reader read every label and legend entry at 700 px (its friction notes only that the analysis box and the legend are small).

- **G3r7-P3-1.** Reader tag [blocks]; does not block: no change. The reader read the arrows correctly through the legend ("value comes from"), which is in the image; the view was not taken for something it is not.
- **G3r7-P3-2.** Reader tag [blocks]; does not block: deferred to WP25 / the subtraction pass. The box text, the arrows and the caption agree (the analysis returns pointing error and total mass without a slew; control effort is measured, passed on unchanged), but "No slew for pointing error, total mass" beside "returns 8 of 9" reads as "not returned" until the caption is read. The change it needs, one line of wording in the analysis box in `docs/superpowers/notes/spike-sysml-diagrams/project.py` (behavioural view): say these two are returned without a slew, and keep the two measurement entries. The wording was already changed in revision 7 (G3-P2-6) and is not fully closed by it.
- **G3r7-P3-3.** No change: the caption defines MoE and MoP in one generated sentence (revision 7); the legend is the colours and line kinds only, and the stereotype is the model's own mark.
- **G3r7-P3-4.** No change: as G3-P3-9; the verification names are the model's and the caption states which requirements are verified in each.
- **G3r7-P3-5.** No change: the legend sample is a heavy dashed glyph and the line is dashed at thickness 3; the reader saw the line and named it "computed from", the legend's word. It is short because the two boxes are adjacent.
- **G3r7-P3-6.** No change: the requirement's line to the launch cost is a requirement line (a requirement reads a derived quantity), as the legend's line kind says; the dashed line and the caption say what the launch cost is computed from. The view is not taken for something it is not.
- **G3r7-P3-7.** No change, by design: as G3-P3-6; levels and ranges are in the caption, and the Controller box cannot carry two regime ranges without the range text that round 4 removed.
- **G3r7-P3-8.** No change: as G3-P3-5; the notation is standard SysML and the reader's own sentence read swap and tune and composition correctly. The assembly view is unchanged in revision 7.
- **G3r7-P3-9.** No change: the smallest type is 12.5 px at 700 px (pinned by test); the reader read the box.
- **G3r7-P3-10.** No change: the frame titles and the caption carry the grouping, as G3-P3-10.
- **G3r7-P3-11.** No change: a confirmation.

**Count.** 11 findings as the reader tagged them (2 [blocks], 6 [changes the view], 3 [note]).

**Nothing blocks WP23.** The one view change worth making (G3r7-P3-2, analysis box wording in `project.py`) is deferred to WP25 / the subtraction pass.

## Behavioural view, revision 8 (G3r7-P3-2)

The one line the P3 cold read of revision 7 left open, executed in `docs/superpowers/notes/spike-sysml-diagrams/project.py` (`--revision 8`, now the default; revisions 3 to 7 reproduce the earlier text), the driver's decision (b) of 2026-11-10. Recipe checked first: the committed revision-7 `behavioural_view.puml` and `assembly_view.puml`, re-rendered by `render.sh`, gave the committed PNG and SVG bytes (all four identical).

**The line.** Before: "metrics. No slew / for pointing error, / total mass." Now: "metrics, computed / with no slew: / pointing error, / total mass." Beside "returns 8 of 9" it now reads as returned, computed without a slew; the two measurement entries ("control effort (passed on) and settling time (not returned)") are unchanged, and no line is longer than 19 characters. The generator still finds the two names from the model.

**Type.** The smallest type at 700 px is 12.512 px (the SVG's font sizes are 12.512 and 14.597 only), as in revision 7; nothing shrunk, the image is 700 x 1341 as before. Only the behavioural `.puml` line changed; the caption is byte-identical. The assembly view's sources, images and caption, and `fig-assembly-view.png`, are byte-identical. `paper/figures/fig-behavioural-view.png` is a byte copy of the new image. Looked at at 700 px with the image viewer: the box reads "returns 8 of 9 metrics, computed with no slew: pointing error, total mass", then the measurement's two entries.

Renders (session scratchpad `wp23view8-renders/`, 700 px): `before/behavioural_view.png` (revision 7), `r7check/` (the recipe check), `gen8/` (the generator's output, byte-identical to the committed files), `behavioural_view.png` (after).

## Close-out (the WP23 close-out's executor, 2026-11-10)

Scope `WP23-closeout-scope-of-work.md` (approved 944c564; OD10 = (a)). Commits on `dev`: f9a4da8 (the
model and its gates), 499ee63 (eight metrics in the case code, `dod_ok` a flag, contract row 15),
4409920 (`dod_ok` in the proposer's and the sensitivity run's filters), f1101ce (the host
regeneration and the records), b4d0132 (the tables, the association step, the prose), then this
section, the comparison and the Appendix E change.

**What was run, on the host (macOS arm64), with wall times.** `ledger_gate.py --host` 221 s (the
run of record; two earlier runs discarded and the tree restored, `swap-evidence.md`, "WP23
close-out", section 1); the first-20 recording 11 s; `coverage.py` 16 s; the views generator and
PlantUML (revision 9) a few seconds; `experiments compare` 5 s and `verify` (39 entries, 11
current, 0 drifts); `experiments.sensitivity regenerate` 18 min and `analyse` 3 min;
`paper/stability_extra.py` 3 min; `scripts/build_figures.py` 81 s; `paper/execute_notebooks.py`
140 s; the soft-fit reference re-recorded by the test's routine (about 60 s). Checks: the fast suite
(1733 passed); the slow files of the change with `REQUIRE_OPENSYSML=1` (test_case,
test_cubesat_oracle, test_v2_data, test_paper, the model tests, test_soft_fit, test_site, the
contract and the register: 607 passed, then the soft-fit pair after its recording); ruff check and
format, `uv lock --check`, the vocabulary tool with its baseline (0 new) clean.

**What was looked at.** The behavioural view at 700 px (revision 9: the eclipse reserve's boxes
gone, the pointing-error requirement's box reads "not satisfied by cubesatBaseline"; the assembly
view unchanged, byte-equal); the regenerated figures as images (`fig-tau-sweep`: eight metric rows,
the zero rows power margin and peak slew power; `fig-tensions-k3`, `fig-regimes`); the staged
supporting material (D.17's text and tables, Appendix E) and `docs/examples.md` in the browser
pane. Renders: the session scratchpad's `closeout-renders/`.

**Findings of the executor, for the reviewer.**

1. Under the feasible set's conditioning (OD10 (a)) the requirement-constrained set keeps the
   feasible set's one-term contending set in the primary regime and swaps power margin for energy
   balance in the stock regime; spike A's changed set was the re-conditioning (the comparison,
   section 6). The Discussion candidate says so.
2. The proposer's training rows had the same hidden dependency on the reserve's positivity as the
   case's fit (811 rows without it); `dod_ok` joined its filter before the run of record.
3. The radius of the certificate scales with the number of metrics; the stock K = 3 assignment moved
   by 1 to 3 rows and the primary's terms 1 and 2 traded labels (no sentence reads a term number).
4. **Not achieved: R-31.** Appendix E's mathematics still shows as raw `$...$` on the staged page.
   The page shows each table's HTML, made by `paper_common.Md._repr_html_` (markdown-it), and the
   site typesets no mathematics inside a notebook's HTML output; Appendix A's register table shows
   the same raw `$c$`. The generator now carries every `$...$` intact through that step (229 spans,
   no emphasis made of an underscore; `tests/test_paper.py::test_gaps_table_carries_its_mathematics_intact_into_the_page`),
   which is necessary and not sufficient. The rest needs `paper/paper_common.py` (outside the
   radius) or a renderer the lock does not hold: the question is the PM's.

**The two candidate Discussion sentences, verbatim, for the supervisor** (`sec-discussion`, the
paragraph "Requirements after the fit"; register rows C406, C407):

> Fitting first and reading the requirements after is the unconstrained-then-constrained reading of
> a trade study: Appendix D.17 prices each of the model's four requirements at the fitted frontier
> and counts the near-frontier designs it excludes.

> With every design set conditioned as the fit of record is, removing the infeasible designs or
> imposing the four requirements before the fit changes the one-term contending set by at most one
> of its five metrics, so on this case pre-imposing the requirements does not change what the
> frontier trades.

**The two spike tables against the spikes' numbers.** Spike B's requirements table reproduces at
the paper's precision (pass fractions, near-frontier designs excluded, prices 0.07, 0.56 and 7.9
bands, the elasticities with co-contenders of exponent at least 0.05), except pointing error in the
primary regime, 95.0 % against the gate's 94.9 % (one design within 1e-6 of the limit, which spike
B noted). Spike A's table differs where OD10 (a) says it should: the comparison's section 6.

### Fix-forward after the acceptance review (2026-11-10)

A fresh unit (worktree `closeoutfix` from origin/dev at ebd7dfe, on the host, macOS arm64) fixed the
review's gaps G-1 to G-4 and the observations O-1, O-2, O-5, and verified R-31 by looking. Radius:
the PM's brief, widened by the driver for O-5 ("(a). One object, one name: the regime is "primary"
everywhere ...") to `paper/generate_model.py`'s association sentence, the three
`supporting_material.ipynb` output cells that print it, and `tests/test_case.py`'s `DOCS_LABELS`.
The comparison (`swap-evidence.md`, "WP23 close-out") gained a paragraph in section 4, rows in
section 6 and a section 7; the reviewer's section above is unchanged.

- **G-1.** `tests/test_k_terms_case.py` pins the eight-metric fit of record: `exponents_.shape ==
  (3, 8)` and the margins and radii as `k_terms.run_regime` prints them on `data/v2/` (primary K = 2
  0.000697 / 0.000069, K = 3 0.001212 / 0.000121; stock K = 2 0.001413 / 0.000133, K = 3 0.000350 /
  0.000033), the tolerance unchanged (5e-7; the file has no environment-of-record branch).
  `REQUIRE_OPENSYSML=1`: 7 passed (ebce53b).
- **G-2.** `fig-planes-k1-caption`, `fig-planes-k1-lines`, `fig-planes-k3-caption`: "the other six
  metrics"; `fig-chart-level-caption`: "the first of seven position coordinates" (markdown only).
  `abstraction-gaps.md` rows G-2 and G-17 on the eight-metric data: "eight-metric data", "eight fitted
  attributes", "659 of 706 on eight attributes", "74 of 685 quantities" (counted from
  `sensitivity.json` by the report's printed-precision rule, which gives 80 of 693 on the gate's
  file); M3 and M5 re-measured (the stock K = 3 conditioning 9.32, 0.228, 10.2; six participants at
  τ/2 and 2τ; the primary's numbers unchanged). `tab-E-gaps` re-executed on the host and spliced; no
  register fragment carried a changed sentence.
- **G-3.** Section 6 now lists the stock requirements-met three-term fit and every placement number
  of the "all designs" and "requirements met" columns and the proposals, each with spike A's value,
  the recomputed value and the cause; the "feasible" column equals spike A's F column.
- **G-4.** A comment at `compare.py`'s `ORIENTATION`/`POWER` says why the reserve stays (the frozen v1
  frames carry it); `cubesat_oracle.py` is ledger-hashed (the v2 entries' `code`), and its docstring
  already says the output leaves the reserve out: left, recorded in section 7.
- **O-1.** Not changed, explained (section 7): 95.0 % is exact for the model's limit 0.008495 degree
  (671 of 706); 94.9 % is the share at the ladder's unrounded 95th percentile, 0.0084945 degree (670).
  The model's doc is ledger-hashed and `case-model.md` was outside the radius.
- **O-2.** `v1-v2-comparison.md` regenerated by `compare.main(["--out", ...])`: the deleted
  `k3-cubesat.md` row gone (37 records to 36), nothing else moved.
- **O-5.** The association sentence names "primary regime" and "stock regime" (C.5, D.3, D.4
  re-executed and spliced); the docs page's generated blocks print "primary | stock" and its opening
  paragraph says "the primary regime's table (aggressive controller gains)".
- **R-31, looked at.** The staged supporting material (`stage_site.py --serve`) in the browser pane at
  the pane's desktop width: Appendix A's register table holds 27 typeset formula elements and Appendix
  E's table 229, and the page's text holds no `$...$` span; both typeset (screenshots in the session
  scratchpad's `closeoutfix-renders/`). The executor's finding 4 is superseded: R-31 holds.

Checks (host): `REQUIRE_OPENSYSML=1 uv run pytest -n auto` on test_k_terms_case, test_case, test_paper,
test_gaps, test_claims_register, test_docs, test_site, test_v2_data, test_experiments (slow included):
401 passed, 4 skipped; the fast suite: 1733 passed, 16 skipped, 1 xfailed; `experiments verify`: 39
entries (11 current), 0 drifts; `check_vocabulary.py --baseline`: 0 new, 69 known; ruff check and
format clean on the changed Python files; `uv lock --check` clean.

## Close-out acceptance review (work-acceptance, 2026-11-10)

| | |
|---|---|
| **Scope of work** | `work-packages/WP23-closeout-scope-of-work.md` (with its amendment line, "during execution") |
| **Scope approval verified** | 944c564 (2026-11-10 09:44, mzargham's tree): `WP23-decisions.md`, "The close-out scope approved; OD10 (2026-11-10, 09:50; the driver)", "Approved for execution by the driver under the mandate", OD10 = (a); the radius amendment (`paper/generate_results.py`) recorded at f2a6927 |
| **Work reviewed** | `dev` 944c564...cc0e1c9; the close-out's commits f9a4da8, 499ee63, 4409920, f1101ce, b4d0132, cc0e1c9 (records eb88d40, f2a6927) |
| **Reviewer** | a fresh agent, worktree `closeoutreview` from origin/dev at cc0e1c9, `uv sync --locked`, on the host (macOS arm64); review only, no repair |
| **Supervisor (accepts)** | mzargham; the gate's container regression and Linux dispatch are the driver's |
| **Acceptance record** | the supervisor's verbal acceptance quoted in `WP23-decisions.md` |

**What was run (all on the host, at cc0e1c9).** `uv run pytest -q -m "not slow" -n auto`: 1733 passed, 16
skipped, 1 xfailed. The slow files of the change with `REQUIRE_OPENSYSML=1` (test_cubesat_model,
test_cubesat_oracle, test_check_designs, test_v2_data, test_case, test_k_terms_case, test_paper, test_site,
test_claims_register, test_interface_contract, test_soft_fit): **514 passed, 4 failed, 4 skipped**; the four
failures are all `tests/test_k_terms_case.py` (`test_k3_fits_and_three_reports[primary|stock]`: `assert
est.exponents_.shape == (3, 9)` gets `(3, 8)`; `test_certificate_margin_and_radius_columns[primary|stock]`:
radius 6.95e-05 against the pinned 5.7e-05). The model gates with `REQUIRE_OPENSYSML=1`
(test_model_checking_v2, test_system_model_v2, test_system_model_v2_r1, test_mutation_v2, test_model_coverage,
test_diagnostic_pair, test_adcs_enrichment): 174 passed. `coverage.py`: wrote `coverage.md`/`.csv`
byte-identical to the committed files (sha256 987500abd780 / a0488048fedc; 7 disagreements, as committed).
The views generator three times into a scratch folder: both `.puml` byte-equal to the committed ones each
time; `behavioural_view.png` and `assembly_view.png` byte-equal to `paper/figures/fig-*-view.png`.
`PYTHONPATH=examples/adcs uv run python -m experiments verify`: 39 entries (11 current), 0 drifts; the five
new entries none dirty, platform macOS-26.5.2-arm64, commit 931dbd8. `ruff check .` clean; `ruff format
--check .` 323 files formatted; `uv lock --check` clean; `check_vocabulary.py --baseline
scripts/vocabulary_baseline.toml`: 0 new, 69 known (exit 0; without `--baseline` it exits 1 on the same 69,
as at 944c564). `tests/test_claims_register.py`: 21 passed; the register 399 rows at 944c564, 402 at
cc0e1c9 (C405 to C407 new). `case.association_all_pairs`, `case.requirements_table`, `case.design_sets_table`
and `case.design_sets_placement` re-run in a scratch script; the diagnostic pair regenerated on
`examples/adcs/data/v2/` to a scratch folder and diffed against `WP23-rounds/gate/k3_record.md`; the v2 data's
configuration columns, seeds and flags compared to 944c564 (equal on all 2000 designs; only
`eclipse_reserve_wh` removed). The staged site (`scripts/stage_site.py --serve`) read in the browser pane:
Appendix C.5, D.3, D.4, D.17, E, the paper's check section and Discussion, `docs/examples.md`; server
stopped. Renders and screenshots: the session scratchpad's `closeoutreview-renders/`.

**What was looked at.** The behavioural view at 700 px: eight traded metrics, no eclipse-reserve box,
`PointingErrorRequirement` reads "not satisfied by cubesatBaseline", as its caption's fifth bullet says;
the assembly view unchanged. The diagnostic pair: eight metric rows, zero rows power margin and peak slew
power (primary), peak slew power (baseline); the K = 3 primary terms 1 and 2 trade labels against the
gate's record, as the comparison says. `fig-tau-sweep` (eight rows, the outlined column 38.1, 0.36 / 0.18 /
0.16 / 0.16 / 0.14) and `fig-planes-k1` against their captions. D.17's two tables and the placement table
in the page equal the re-run to the printed digits. Appendix E's table in the staged page is typeset by
MathJax (the table's text holds no `$`; each formula is a MathJax element); in G-3 the `/2` of
`\tfrac{1}{\tau}\log E e^{...} = \tau\sigma^2\|w\|^2/2` falls onto its own line in the narrow column.

### Deliverables

| ID | Verdict | Evidence |
|---|---|---|
| D-11 | met | `cubesat.sysml` 605-618: 0.008495 degree, 0.05922 N·m·s, 2.6 W, 90643.0 USD, each doc naming the ladder row and the share; 6,000 USD/kg labelled illustrative (228); no "PROPOSED", no "20 %", no `budgets.margin`; no `EclipseReserve`; header 18-24 states the reserve's removal and the baseline's failure, 0.0155 against 0.0085 degree, 63.7 % |
| D-12 | met | the model gates 174 passed; `coverage.py` byte-identical; views at revision 9 (`project.py` `behavioural(..., revision=9)`) byte-equal over three runs and to the paper's copies; `ledger_gate.py` in 499ee63 |
| D-13 | **not met** | `tests/test_k_terms_case.py` still pins nine metrics (`(3, 9)`) and the nine-metric radii (`MARGIN`): 4 failures under `REQUIRE_OPENSYSML=1` (above). The other listed files carry eight (R-17's grep; test_case, test_cubesat_oracle, test_diagnostic_pair, test_v2_data pass) |
| D-14 | met | `interface-contract.md` row 15 (the change, the side "technical", the approval 944c564); `contract_version = 15` in both; `case.v2.traded_metrics` eight; v2 headers without the reserve; the row states no manifest key pins the case's flags; `test_interface_contract.py` passes |
| D-15 | met | the five `@6`/`@5` ledger entries, verify 0 drifts; the data, records, reports, environment files and notebooks regenerated (f1101ce, b4d0132); the docs' numbers read in the page equal the re-run |
| D-16 | **not met** | the section exists in the form asked (changed conclusions first; files with hashes; numbers with causes; conclusions; section-4 cell list; section 6 for OD10), but it misses moved numbers that now read false: G-2 and G-3 below |
| D-17 | met | `association_all_pairs`, `requirements_table`, `design_sets_table`, `design_sets_placement` in `case.py`; C.5 row and sentence, D.3 and D.4 sentence, D.17's two tables and the placement table in the staged page; the docs page's "No metric twice" bullet and "Requirements read after the fit" (two generated blocks) |
| D-18 | met | `sec-case-analysis-5` and `num-predict-reading` state the proposals fail the depth-of-discharge requirement and reached the four-metric frontier by spending the battery; `sec-discussion` "Requirements after the fit", two sentences; C405 to C407; `case-model.md` 178-192; `glossary.yaml` one line; `generate_gaps.py` |
| D-19 | not checkable (pending) | the executor's record is `WP23-review.md`, "Close-out", not the scope's `WP23-closeout-review.md` (G-5); the checks, the candidates verbatim and the spike reading are there; this review and its dispositions are pending |
| D-20 | not checkable (pending) | the scope gate is recorded (944c564, eb88d40, f2a6927); the gate's dispositions and the acceptance are not yet due |

### Requirements

| ID | Verdict | Evidence |
|---|---|---|
| R-16 | met | the grep finds the four values and 6000 (illustrative); "margin" hits are the power-margin metric only; `coverage.md` lists the four limits; `test_the_four_thresholds_are_the_supervisors_values` passes |
| R-17 | **not met (as stated)** | the scope's `git grep` returns `experiments/compare.py:269,274` (`ORIENTATION` and `POWER` keep `eclipse_reserve_wh`, so the v1-v2 report can read the frozen frames, which carry it) and the docstring `experiments/cubesat_oracle.py:27` (says the reserve left). The v2 data, the model, `case.py`, `k_terms.py` and `coverage.md` (eight metric rows) are free of it (G-4) |
| R-18 | met | `cubesat.sysml` 22-24, 606-608, 659, 729; `case-model.md` 185-189: plain, with 63.7 % |
| R-19 | met | `test_case.py` 81-88 (`dod_ok` in `CUBESAT.flags`; 706 and 780; 131 failures each) passes in the slow run |
| R-20 | met | 174 passed; views byte-equal three runs; coverage regenerates byte-identical |
| R-21 | met | `test_interface_contract.py`, `test_v2_data.py` pass |
| R-22 | met | verify: 39 entries, 0 drifts; the five entries not dirty, the host's platform |
| R-23 | met | fast suite 1733 passed; ruff check and format clean; lock clean; vocabulary 0 new against its baseline (the tool without the baseline exits 1 on 69 known, unchanged since 944c564) |
| R-24 | **not met** | the comparison does not list the moved numbers of G-2 (Appendix E) or the stale counts of G-2 (the plane and chart captions), and section 6 omits the differences of G-3 |
| R-25 | met | re-run: 28 pairs per regime, none at \|Spearman\| ≥ 0.99 (strongest power margin/energy balance 0.982, 0.988); `test_association_step_covers_every_pair_and_names_the_one_axis_pairs` passes; the page's C.5 table is the same 28 rows and D.3, D.4 carry the sentence; the docs bullet reads it |
| R-26 | met | re-run against spike B sections 1 and 2: pass shares 62.2/67.3, 95.0/63.7, 58.9/90.0, 94.9/95.6, joint 40.8/38.7; excluded 0, 1, 18, 0 (19) of 56 and 2, 42, 1, 1 (43) of 77; exponents 0.164/0.039, 0/0.432, 0.358/0; prices 0.0019 (0.07), 0.012 (0.56), 0.173 (7.9 bands); elasticities settling −1.16 / energy balance +0.86; power margin +0.16 / settling −0.15; power margin +1.40 / settling −1.36: all equal spike B at the paper's precision |
| R-27 | **not met (narrow)** | the feasible rows equal spike A's F rows; the "all designs" and "requirements met" one-term rows and the primary R three-term row differ as section 6 lists. Not listed: the stock R three-term fit (spike A 0.63 / 0.00 / 0.38 led by energy balance, control effort, total mass; now 0.60 / 0.00 / 0.40 with peak slew power and total mass leading term 3) and every changed placement number (baseline configuration primary R −0.93 in spike A, −0.566 now; stock R −0.26, now −0.030; the candidates likewise; the proposals "not placeable" in spike A, placed now on eight metrics) (G-3) |
| R-28 | met | the fit of record is `fit_study` on `load_study`'s feasible study; `case.py`'s diff adds `dod_ok` to the flags and a `requirements` dict to the spec, read only by `requirement_mask` in the after-the-fact tables; no threshold in `load_study` or `feasible_mask` |
| R-29 | met | paper sources changed in five cells: the D-18 cells plus `sec-case-construction-1`, `-1b`, `fig-behavioural-caption`, each listed with its cause in section 4 (observation O-4); Discussion gains two sentences, C406 and C407 marked candidate in `source` and `note`, and the length-ledger row names them CANDIDATE; register and paper tests pass |
| R-30 | met (this review) | dispositions pending |
| R-31 | met (as seen) | the staged Appendix E table typesets every formula (MathJax; no `$` in the table text); `test_gaps_table_carries_its_mathematics_intact_into_the_page` passes. The executor's finding 4 above says the opposite (G-5) |
| R-32 | met | the close-out's commits touch nothing under `src/`, `derivation/`, `examples/adcs/data/*.csv` or `cubesat_tradespace.sysml`; every file is in the radius or the amendment line (below) |

### Definition of good enough

| Item | Verdict | Evidence |
|---|---|---|
| R-16 to R-23 hold on the host | not met | R-17 as stated (G-4); the others hold. The slow `test_k_terms_case.py` (D-13) is red on the host, outside R-23's fast suite |
| The comparison lists every moved number, changed conclusion and the cell list (R-24) | not met | G-2, G-3 |
| The three tables generated and placed (R-25 to R-27), the fit unchanged in kind (R-28) | not met (narrow) | R-27 (G-3); R-25, R-26, R-28 met |
| The prose items (R-29, R-31) and the candidates in the review | met | above |
| The fresh review recorded with every finding disposed (R-30); R-32 | not checkable | this review is recorded; the dispositions are the driver's |

### Non-goals

None touched: nothing under `src/` or `derivation/`; no figure added (seven `paper/figures/*.png` and the
behavioural view regenerated); the sampling, seeds, configurations and flags equal on all 2000 designs; the
proposer's filter gained `dod_ok` (4409920), which keeps its training rows at the 706 it had at the gate,
not a change of what it trains on (O-3); no container run, re-pin, `RECORD.md` or `hts-alt`; the frozen
data and v1 model untouched; `k3-cubesat.md` deleted and `method.md` re-pointed under the amendment line.

### Outside the scope

`git diff --stat 944c564...cc0e1c9`: 112 files. Attributed: the close-out's own commits (above) touch only
files of the scope's lists or the amendment line (`paper/generate_results.py`, `generate_findings.py`,
`length_ledger.toml`, `experiments/check_designs.py`, `experiments/sensitivity.py`, `method.md`, the
deletion of `k3-cubesat.md`, `test_v2_data.py`, `test_site.py`, `change-register.md`, `test_soft_fit.py`,
`tests/data/soft_fit_default_reference.npz`), plus `WP23-review.md` (the review record, G-5). The other
files in the range belong to other packages' commits on `dev`: WP24 (`docs/user-guide/*.md`, `docs/api.md`,
`scripts/rename_facet.py`, `tests/test_rename_facet.py`, `scripts/check.py`, `WP24-*.md`), WP25
(`docs/superpowers/notes/spike-{certificates,facet-refit,objective}/*`, `abstraction-gaps.md`,
`WP25-*.md`), WP26 (`WP26-decisions.md`), the driver (`site/index.html`, `site/paper-map.webp`,
`PM-BRIEF.md`, `driver-log.md`, `parallel-board.md`). No close-out change is outside its scope and amendment.

- **Out-of-scope changes:** none by the close-out.
- **Non-goals touched:** none.

### Observations (not counted as failures)

- **O-1.** The primary regime's pointing-error pass share is 94.9 % in the model's doc, `case-model.md` and the
  decisions, and 95.0 % in D.17 and the docs page (one design within 1e-6 of the limit; the tables read
  `<=` with tolerance 1e-9). One object, two printed values.
- **O-2.** The regenerated `experiments/reports/v1-v2-comparison.md` (line 264) still lists
  `docs/superpowers/notes/k3-cubesat.md`, which f1101ce deleted.
- **O-3.** The check's future work reads "a proposer that also predicts the feasibility flags", not the
  scope's "training on the fully feasible rows": the proposer already trains on the 706 feasible rows
  (C405's note), so the scope's wording would have been false; the change is backed.
- **O-4.** `paper.ipynb` sources changed in three cells beyond D-18's list, each with its cause in section 4.
- **O-5.** The association sentence prints "the strongest pair, Dataset cubesat-primary: power margin and
  energy balance, +0.982; Dataset cubesat-stock: ..." (a label pasted into prose); the docs page names the
  regimes "aggressive | stock", the paper "primary | stock".
- **O-6.** The vocabulary tool's exit status is 0 only with its baseline; both before and after the close-out.

### Open decisions (for the driver)

- **G-1. `tests/test_k_terms_case.py` pins nine metrics and the nine-metric radii** (D-13): four slow
  failures on the host; the CI job that runs the slow files would fail on `main`. Options: accept as is /
  fix before acceptance / follow-up work package.
- **G-2. Stale counts the comparison does not list** (D-16, R-24): the paper's `fig-planes-k1-caption`,
  `fig-planes-k1-lines` and `fig-planes-k3-caption` say "the other seven metrics" (six with eight metrics);
  `fig-chart-level-caption` says "Z0, the first of eight position coordinates" (seven; the docs page says
  seven); Appendix E (from `docs/superpowers/notes/abstraction-gaps.md`, outside the close-out's radius)
  says "on the nine-metric data" (its row G-2), "one of the nine fitted attributes" and "659 of 706 on nine
  attributes" and "80 of 693 quantities" (its row G-17; `sensitivity.json` now holds 685). Options: accept as is /
  fix before acceptance / follow-up work package.
- **G-3. Spike A's differences not all listed** (R-27): the placement table's numbers in the "all designs"
  and "requirements met" columns and the stock regime's constrained three-term fit differ from spike A
  without a line in section 6. Options: accept as is / fix before acceptance / follow-up work package.
- **G-4. R-17's grep is not empty**: `compare.py` keeps the reserve in `ORIENTATION` and `POWER` to read the
  frozen frames, and `cubesat_oracle.py`'s docstring names it. Options: accept as is / fix before
  acceptance / follow-up work package.
- **G-5. The review record**: it is `WP23-review.md`, "Close-out" (and this section), not the scope's
  `WP23-closeout-review.md`, which the scope's acceptance record names; and its finding 4 says R-31 was not
  achieved while the staged page typesets Appendix E. Options: accept as is / fix before acceptance /
  follow-up work package.
- **G-6. The observations O-1 to O-6, as one item.** Options: accept these as is / pick any to act on.

Pending with the supervisor (not open for this gate): his review of the two candidate Discussion sentences
(C406, C407); the proposals' future work (the flag-predicting proposer, O-3); his review of the redundancy
calls A1 and B1.

### Recommendation

Do not recommend acceptance yet, because the slow suite is red on the host (G-1: `test_k_terms_case.py`
still pins nine metrics), and the paper carries stale counts in four figure captions and Appendix E that
the comparison does not list (G-2), so D-13, D-16 and R-24 are not met. The model, the data, the
regeneration, the three tables and the prose stand on the evidence above: the requirements and spike B's
table reproduce exactly, the Discussion candidates are backed by D.17's tables, and R-31 holds in the
staged page.

Acceptance is the supervisor's act, recorded as named above. This report does not accept the work.

### Re-check after the fix-forward (work-acceptance step 5: the review rerun, 2026-11-10, head b9d8b80)

A fresh unit (worktree `closeoutrecheck` from origin/dev at b9d8b80, on the host, macOS arm64) re-ran the
review's evidence against the state at head. Reviewed, not repaired.

| item | state | evidence run now |
|---|---|---|
| **G-1** `test_k_terms_case.py` nine metrics | closed | `REQUIRE_OPENSYSML=1 uv run pytest -q tests/test_k_terms_case.py` (slow included): 7 passed. `k_terms.py` on `data/v2/` prints, per the test's pins: primary K = 2 gamma 0.000697 radius 0.000069, K = 3 0.001212 / 0.000121; stock K = 2 0.001413 / 0.000133, K = 3 0.000350 / 0.000033; the test pins `exponents_.shape == (3, 8)` and the same six-decimal pairs |
| **G-2** stale counts | closed | the four caption cells (`fig-planes-k1-caption`, `fig-planes-k1-lines`, `fig-planes-k3-caption`, `fig-chart-level-caption`) read "the other six metrics" (three cells) and "the first of seven position coordinates"; `abstraction-gaps.md` has no "nine" left, row G-2 reads "eight-metric data", row G-17 "eight fitted attributes", "659 of 706 on eight attributes", "74 of 685 quantities"; `sensitivity.json` holds 685 quantities and the printed-precision rule (committed, min and max equal at `.4g`) gives 74 not equal; the staged Appendix E text holds both phrases and no "nine-metric", "nine fitted" or "nine attributes" |
| **R-31** (Appendix A and E typeset) | holds | staged site (`stage_site.py`, served on 127.0.0.1:8791 after port 8765 was found taken by another process), browser pane at its desktop width, light scheme: `document.body.innerText` holds 0 `$` characters; 937 math elements; Appendix A's table and Appendix E's rows G-2, G-3, G-4 render as typeset formulas (screenshots: pane only for E; a file for A) |
| **G-3** spike A's differences | closed | section 6 of the comparison read against spike A's tables: the stock requirements-met three-term fit, the placement "all designs" and "requirements met" columns and the proposals each carry spike A's value, the recomputed value and the cause; `case.design_sets_placement()` run now prints every listed close-out value (for example primary baseline configuration -0.499 / -0.516 / -0.566, stock -0.075 / -0.057 / -0.030; proposals placed in every column), and its feasible column equals spike A's F column at spike A's printed digits (-0.52, -0.20, -0.15, -0.17; -0.06, -0.20, -0.06, -0.38) |
| **G-4** R-17's grep | open as stated, explained | `git grep -n "EclipseReserve\|eclipse_reserve" examples/adcs/model_v2 examples/adcs/data/v2 examples/adcs/case.py examples/adcs/k_terms.py examples/adcs/experiments/*.py` still returns `compare.py:260, 271, 276` (the comment and the frozen-frame lists) and `cubesat_oracle.py:27` (the docstring saying the output leaves the reserve out). Section 7 of the comparison states why (the v1 frames carry the column; the oracle file is ledger-hashed). The model, `data/v2`, `case.py`, `k_terms.py` are free of it. Whether the scope's R-17 is met as worded is the driver's call, as recorded in G-4's options |
| **G-5** record location and finding 4 | superseded | the fix-forward's R-31 note supersedes finding 4 (R-31 holds, above); the record stays `WP23-review.md`, not `WP23-closeout-review.md` as the scope's acceptance record names: a naming difference only |
| **O-1** 94.9 % and 95.0 % | explained, not changed | section 7: 671 of 706 at the limit 0.008495 degree (95.04 %); 670 at the unrounded percentile 0.0084945 degree (94.90 %); the model doc and `case-model.md` still print 94.9 % |
| **O-2** `k3-cubesat.md` in the v1-v2 report | closed | `grep -n k3-cubesat examples/adcs/experiments/reports/v1-v2-comparison.md` returns nothing |
| **O-3, O-4, O-6** | unchanged | as in the review; the vocabulary tool exits 1 without its baseline (69 violations) and 0 with it |
| **O-5** label pasted into prose; "aggressive" against "primary" | closed | the association sentence reads "primary regime, power margin and energy balance, +0.982; stock regime, ... +0.988" (no "Dataset cubesat-primary" in prose; the remaining "Dataset cubesat-..." strings are the generated reports' dataset headers); `docs/examples.md` prints "(primary | stock)" and its opening says "the primary regime's table (aggressive controller gains)"; `paper.ipynb` names "aggressive controller gains (the primary regime)" |

Checks (host, head b9d8b80):

- `uv run pytest -q -m "not slow" -n auto`: 1733 passed, 16 skipped, 1 xfailed.
- `PYTHONPATH=examples/adcs uv run python -m experiments verify`: 39 entries (11 current), 0 drifts.
- `uv run python scripts/check_vocabulary.py`: 69 violations, exit 1 (no baseline); with `--baseline scripts/vocabulary_baseline.toml`: 0 new, 69 known, exit 0.
- `uv run pytest -q tests/test_claims_register.py tests/test_paper.py tests/test_gaps.py tests/test_docs.py tests/test_site.py -n auto`: 280 passed, 4 skipped.
- `uv run ruff check .`: all checks passed; `uv run ruff format --check .`: 324 files already formatted; `uv lock --check`: resolved, clean.

**Recommendation (re-check):** recommend acceptance with the listed gaps noted. D-13, D-16 and R-24 now hold and the slow suite is green; the one item open as worded is G-4 (R-17's grep is not empty, two files kept on purpose and explained), with O-1's two printed values (94.9 % in the model doc, 95.0 % in the tables) explained and left for the model's next regeneration.

Acceptance is the supervisor's act, recorded as named above. This report does not accept the work.

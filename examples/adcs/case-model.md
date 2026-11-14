# The cubesat model, the experiment layer and how to plug in your own case

The method sees one thing: a map from configurations to attributes.

Two generations sit in the directory. The **frozen** generation is what the paper and the records
cite. The **v2** generation (`model_v2/cubesat.sysml`, `experiments/`,
`data/v2/`) is the tidied model with an experiment layer; it lands beside the frozen one. Every
file in `data/` and `data/v2/` has an entry in the ledger.

## The contract and this example's physics

The contract is the oracle: configuration in, attributes and flags out.

```python
class Oracle(Protocol):
    config_names: tuple[str, ...]  # the design variables
    attribute_names: tuple[str, ...]  # the measured attributes
    flag_names: tuple[str, ...]  # feasibility, as booleans

    def __call__(self, configuration) -> dict[str, float | bool]: ...
    def evaluate(self, designs: pandas.DataFrame) -> pandas.DataFrame: ...
```

`experiments/oracle.py` defines it and imports no modeling tool. The scenario and the gain box are
fixed when the oracle is constructed. A configuration outside the ranges, or with an unknown
categorical value, raises `ValueError` naming the variable. The runner and the ledger treat every
oracle alike and record which kind of evidence stood behind a run: `simulation`, `physical-test`
or `human-assessment`.

Everything else in this directory is the physics of one case:

| part | belongs to | where |
|---|---|---|
| configuration to attributes, flags | the method's contract | `experiments/oracle.py` |
| sampler, runner, ledger, comparison | the experiment layer, case-free | `experiments/runner.py`, `ledger.py`, `experiment.py`, `compare.py` |
| design variables, alternatives, accounting, scenario, requirements | this example's physics | `model_v2/cubesat.sysml` |
| the slew integration (the measurement of record) | this example's physics | `adcs_sim.py` |
| the glue that makes the model an oracle | this example's instance | `experiments/cubesat_oracle.py` |

To run your own case you replace three things and keep the rest. The **oracle** turns a
configuration into attributes. The **sampler** draws the configurations, or says which are tested.
The **experiment declaration** gives the names, count, seed and evidence kind.

## Reading the model top to bottom

`model_v2/cubesat.sysml` is one file and one package, `CubesatTradeSpaceV2`, read in this order.

<!-- sections:begin -->
| section | title | lines |
|---|---|---|
| 1 | CONFIGURATION SPACE (configuration view): what can be chosen | 106 to 214 |
| 2 | THE CUBESAT (configuration view): composition and environment | 216 to 335 |
| 3 | ACCOUNTING (assessment view): mass, power, energy, inertia, pointing | 337 to 698 |
| 4 | SCENARIOS (assessment view): the slew, and a closed-form approximation of it | 700 to 774 |
| 5 | REQUIREMENTS, SATISFACTION AND VERIFICATION (assessment view; 15.2, WP22) | 776 to 1122 |
| 6 | THE EXPERIMENT (assessment view): configuration and measured slew in, attributes out | 1124 to 1174 |
| 7 | NAMED CONFIGURATIONS (configuration view) | 1176 to 1199 |
<!-- sections:end -->

- **Configuration space.** It holds the two enumerations (wheel class, star-tracker grade) and the abstract
  part definitions, with a concrete alternative for each literal and its attribute table. The
  continuous ranges and both gain boxes (baseline and aggressive) are named parts. The sampler
  reads all of it from here; no range, literal or constant is copied into Python.
- **The cubesat.** The composition (panels, battery, wheel, tracker, controller) and the
  environment (eclipse, loads).
- **Accounting.** One `calc def` per accounting quantity: masses, power, energy balance, pointing
  error, depth of discharge. Each constant has a `doc` rationale beside it.
- **Scenarios.** The nominal slew as a named part (angle, horizon, step, bands), and a closed-form
  approximation of the slew for the solver. The integration of the slew itself is in Python
  (`adcs_sim.simulate_adcs`), because the model language cannot integrate the equations of motion.
- **Requirements.** Feasibility as named requirements, whose verdicts are `settled`,
  `momentum_ok`, `power_ok` and `dod_ok`, and the requirements over the other metrics. `satisfy`
  statements tie them to the baseline; the pointing-error requirement, which the baseline
  configuration fails, has a negated one, `not satisfy`. Verification definitions name what each
  verifies. Claims cover every in-range configuration.
- **The experiment.** `analysis def SlewExperiment` takes the configuration and the measured slew
  quantities and returns the attributes the model computes.
- **Named configurations.** The baseline and two contrasts (agile, compact).

The model has two views, generated from its elements and committed in `model_v2/views/`.
The assembly view (`assembly_view`) shows what a configuration is:
the parts, the alternatives swapped for a categorical variable and the parameters tuned for a
continuous one. The behavioural view (`behavioural_view`) shows how a configuration is assessed:
for each traded metric, the requirement that reads it, or none, and where the metric comes from
(the analysis or the measured slew).

## From the assembly to the dataset: measures of effectiveness and measures of performance

A configuration is what the assembly view shows: two swaps (the wheel class, the star-tracker
grade) and four tunes (the panel span, the battery capacity, the gains Kp and Kd). The assessment
turns a configuration into thirteen traded metrics. The slew is integrated once and measured, the
accounting calculations are evaluated, and the experiment returns the metrics as one row of the dataset,
with the four flags beside them. Each metric is marked in the model as a measure of effectiveness
(MoE) or a measure of performance (MoP) by one rule, stated in the model's top comment. An MoE is a
measure a stakeholder states without knowing the design. An MoP is a measure of the system's
performance under the scenario the engineer states. There are three MoEs (the pointing error, the
unit cost and the fleet cost) and ten MoPs. The stakeholders ask for a payload that points and a launch they can afford;
everything else is how the design performs under the engineer's slew and orbit. Each metric is read
by a requirement on its own quantity and verified in a verification case.

### The traded metrics in their disciplines' words

Control (the attitude loop under the nominal slew, a 30 degree slew with a 600 s horizon).

- **Settling time** (MoP, measured): the hold time, the first time after which the pointing error
  stays inside the settling band, a fraction of the slew's initial error. It is found as the last
  exit from the band, so a slew that never holds has the horizon as its settling time.
- **Pointing error** (MoE, a calc of the configuration): how well the payload points, the
  root-sum-square of the steady attitude error under the disturbance and gravity-gradient torques
  (the torque over Kp) and the star tracker's accuracy.
- **Control effort** (MoP, measured): the integral of the wheel torque magnitude over the slew,
  in N.m.s; what the slew asks of the wheels.
- **Momentum headroom** (MoP, from the measured peak momentum): the wheel class's momentum
  capacity over the peak wheel momentum of the slew; 1 where the peak just reaches the capacity,
  above 1 where the wheel keeps reserve.

Power and energy (the panels, the battery and the loads under the stated orbit and eclipse).

- **Power margin** (MoP): the generated power left after the housekeeping load and the peak slew
  power, at the peak of the slew in sunlight.
- **Energy balance** (MoP): over one orbit, the energy the panels supply in sunlight less the base
  load over the orbit and the slew's loss energy.
- **Depth of discharge** (MoP): the eclipse demand (the base load over the eclipse plus the slew's
  loss energy) over the battery capacity.
- **Peak slew power** (MoP): the electrical draw at the peak of the slew, the tracker's power plus
  the idle wheels plus the wheels' loss at the peak torque.
- **Available power** (MoP, a calc of the configuration): the generated power left after the
  housekeeping load and the tracker, before any slew; positive wherever the power requirement holds.
- **Battery peak power ratio** (MoP): the pack's peak power (its discharge rating times its
  capacity) over the eclipse peak load (the housekeeping load plus the peak slew power with the
  panels giving nothing). It is 1 where the pack just carries the slew in eclipse and above 1 where
  it keeps reserve.
<!-- vocab-exempt: power margin -->

Mass and cost.

- **Total mass** (MoP): the launch mass of the configuration, the sum of the part masses.
- **Unit cost** (MoE, a calc of the configuration): the cost per satellite to build and launch a
  fleet, the fleet cost over the fleet size; it falls
  as the fleet grows.
- **Fleet cost** (MoE, a calc of the configuration): the cost to build and launch the fleet. The
  parts and the assembly line each cost a fixed share paid once plus a learning curve in the fleet
  size, and the launch of every satellite costs 7,000 USD per kilogram of its total mass. It rises
  with the fleet size, more slowly on the build part than on the launch part.
- **Launch cost** (MoE, not traded): the total mass times 7,000 USD per kilogram
  (`launchRate` in `model_v2/cubesat.sysml`). It is the stakeholder's
  measure on the mass and the quantity the launch-budget requirement reads. The total mass stays the
  traded metric and the dataset gains no column.

### The requirements and what each reads

| requirement | reads | bound | where the bound comes from |
|---|---|---|---|
| `SettledRequirement` (the flag `settled`) | the measured settling time | below the slew's horizon | the scenario |
| `MomentumRequirement` (`momentum_ok`) | the momentum headroom | at least 1 | the wheel class's capacity |
| `PowerRequirement` (`power_ok`) | the available power | positive | the accounting |
| `DepthOfDischargeRequirement` (`dod_ok`) | the depth of discharge | within the environment's allowed depth | the environment |
| `PowerMarginRequirement` | the power margin | not negative | zero |
| `EnergyBalanceRequirement` | the energy balance | not negative | zero |
| `PointingErrorRequirement` | the pointing error | within `budgets.pointingErrorLimit`, 0.008495 degree | the supervisor's choice |
| `ControlEffortRequirement` | the measured control effort | within `budgets.controlEffortLimit`, 0.05922 N.m.s | the supervisor's choice |
| `PeakSlewPowerRequirement` | the peak slew power | within `budgets.peakSlewPowerLimit`, 2.6 W | the supervisor's choice |
| `LaunchBudgetRequirement` | the launch cost (the MoE on the total mass) | within `budgets.launchBudget`, 105,770 USD | the supervisor's choice |
| `UnitCostRequirement` | the unit cost | within `budgets.unitCostLimit`, 350,000 USD per satellite | the supervisor's choice |
| `FleetCostRequirement` | the fleet cost | within `budgets.fleetCostLimit`, 6,000,000 USD | the supervisor's choice |
| `BatteryPeakPowerRequirement` | the battery peak power ratio | at least 1 | the battery's rating |
<!-- vocab-exempt: power margin -->

The first four are the flags of the dataset: the verdicts of named requirements on each simulated
configuration. `dod_ok` is also one of the case's feasibility flags (`case.CUBESAT.flags`), so the
depth-of-discharge failures leave the fit by name. The four thresholds are the supervisor's choice.
They are literal values in `budgets`, each with the share of the feasible designs it admits (primary / baseline regime): a peak
slew power of 2.6 W (62.2 % / 67.3 %, every small and medium wheel), a pointing error of 0.008495
degree (94.9 % / 63.7 %), a control effort of 0.05922 N.m.s (58.9 % / 90.0 %) and a launch budget
of 105,770 USD, 15.11 kg at 7,000 USD per kilogram (94.9 % / 95.6 %). The baseline
configuration fails the pointing-error requirement: its pointing error is 0.0155 degree against
0.0085 degree, and 63.7 % of the baseline regime's feasible designs pass it. The model states the failure as `not satisfy baselinePointingError by
cubesatBaseline`, which the engine checks true. The battery's discharge rating is a
continuous rating of 1 C (`environment.batteryDischargeRate`, 1.0 per hour): the pack delivers its
capacity in one hour. It is the plain rating of a small-satellite lithium-ion pack and not a cited
one. None of these thresholds enters the dataset or the fit. The fit is on the feasible designs,
and the case reads the four requirements after it (`case.requirements_table`, `case.design_sets_table`; Appendix D.17 of the supporting material).

### What the case leaves out
"Verification" on this page is a solver checking a requirement on a configuration, not a hardware test. The model is a
demonstration.
- **Cost beyond a lower bound.** The unit cost and the fleet cost cover the bus, the attitude-control parts, assembly and test,
  and wholesale launch, and leave out the payload, communications, flight software, licensing, operations and the rest of the
  full costing. The fleet cost requirement holds the covered cost under 6,000,000 USD, inside the sponsor's full budget of
  8,000,000 USD; the rest is the allowance for what is not covered.
- **Pointing error.** It is the closed-form steady error with the star tracker's accuracy, summed in quadrature; boresight
  alignment, the tracker's roll axis and wheel jitter are not modelled, so its smallest value, 0.0006 degree, is not a flight claim.
- **Momentum management.** `momentum_ok` compares one slew's peak momentum with the wheel's capacity. The constant disturbance
  torque is not accumulated over an orbit and no desaturation device exists, so the small wheel's
  feasibility is a one-slew reading and not a sizing.
- **Launch slot.** The 50 kg minimum slot (350,000 USD) is a note in the model and not a cost: a fleet of one to three pays it, so
  the launch cost is understated by 3.1 to 4.2 times at one satellite and the low end of the fleet-size axis is underpriced.
- **Margins and growth.** Mass and power are nominal sums; solar degradation is one fixed factor (0.9); no battery fade or charge loss.
- **One scenario.** One 30 degree slew in a 600 s horizon under a saturating proportional-derivative law (both choices of the case), and one fixed 0.6 h eclipse in a low Earth orbit of about 95 minutes.

The full list is Appendix C.8 of the supporting material.

### Coverage: every swap and tune reaches a metric

The coverage table is `model_v2/views/coverage.md` (and `.csv`), generated from the model by
`model_v2/coverage.py`. For each decision element and each traded metric it states whether the
model has a path from the metric back to the element and whether a one-at-a-time change of the
element at the three named configurations moves the metric. Every swap and tune reaches at least
one traded metric in both columns, and every traded metric is reached. The tracker grade and the
panel span reach all thirteen, the wheel class and the battery twelve (not the available power), Kp
nine and Kd eight, and the fleet size the two costs. Neither gain reaches the total mass, the
available power or the two costs, because the accounting has no gain in it; Kd does not reach the
pointing error either, because its closed form has Kp alone. Ten cells disagree between the
columns, with one cause. The power margin, the peak slew power and the battery peak power ratio read
the measured peak torque, which at the named configurations is the wheel class's maximum, because
the power cap does not bind there. The model allows the effect; the three configurations do not
show it.
<!-- vocab-exempt: power margin -->

The table's third part is the coupling between subsystems, in the form of the design structure
matrix of multidisciplinary design analysis and optimization (MDAO), the family the paper names
beside this method; the form is the XDSM of Lambe and Martins (`lambe2012extensions` in
`docs/references.bib`) without its process line. Rows feed columns. The configuration values feed
the three subsystems of the behavioural view (controls; power and energy; mass). The subsystems
exchange named coupling variables: the measured peak torque and the torque-squared integral from
the controls to the power subsystem; the usable wheel torque and the panel mass back; the battery
and panel masses into the mass accounting; the structure mass and the inertias from the mass
accounting to the controls. The metrics and requirements are read off the subsystems. The
graph of configuration values, subsystems and metrics is connected. The controls and the power
subsystem feed each other, a loop the model resolves in one pass: the usable torque is a
quantity of the configuration computed before the slew, and the peak torque is read after it.

### The texture hypothesis and what the fit returned

The supervisor's hypothesis: once the configuration space and the metric
space are each explicit and joined by requirements, the K = 1 exponent heatmap across the fit
temperature shows more texture, more metrics carrying weight. The regenerated
figure checks it; it is never a target. No metric, threshold or constant of the model
was chosen because it moves the heatmap, and the fit runs unchanged on whatever the model produces.

What the fit returns on the thirteen-metric data is in Appendix D of the supporting material.

## Running an experiment and reading the ledger

An experiment is a declared object (`experiments/experiment.py`); the declarations of the v2
generation are in `experiments/definitions.py`. From the repository root:

```bash
PYTHONPATH=examples/adcs uv run python -m experiments verify
PYTHONPATH=examples/adcs uv run python -m experiments run v2-primary
PYTHONPATH=examples/adcs uv run python -m experiments adopt
PYTHONPATH=examples/adcs uv run python -m experiments compare
```

- `verify` recomputes every hash in the ledger (entry chain, model, code files, outputs, row counts,
  parents) of the current entries and prints one line per drift; it exits 1 on drift. Entries a
  later entry supersedes are listed after the drifts, not counted as drift.
- `run <id>` executes the declared experiment and appends one entry. It refuses an id that already
  has an entry: the ledger is append-only. The ids of the v2 generation are `v2-primary`,
  `v2-baseline`, `v2-check-predictions` and `v2-check-designs`; the predictions are committed
  before the check designs are simulated, and the ledger order shows it.
- `run <id> --supersede` is the re-run after the model or the code changed: a new entry
  `<id>@<n>` names the entry it replaces in `supersedes`, and its parents are the current entries of
  the parent experiments. Nothing earlier is rewritten. If the re-run overwrote the output file, the
  superseded entry is listed as `superseded, output replaced`.
- `adopt` registers the five frozen datasets without regenerating them.
- `compare` regenerates the v1 to v2 comparison report in `experiments/reports/`.

The ledger is `experiments/ledger/ledger.jsonl`, one JSON object per line. Each entry is chained to
the previous one by hash, so editing or deleting a line breaks `verify`.

### The ledger entry

| field | meaning |
|---|---|
| `id` | the experiment id (a sweep cell appends `[key=value]`) |
| `kind` | `generated` (the runner made the file), `adopted` (the file existed before the ledger) or `exclusion` (a model variant the solver proved infeasible; no file, `output_path` is null) |
| `time_utc` | when the entry was written |
| `git_commit` | the commit the run started from |
| `git_dirty` | whether files other than the run's own outputs differed from that commit |
| `evidence_kind` | `simulation`, `physical-test` or `human-assessment` |
| `model_path` | the model text, relative to the root (null when the oracle has none) |
| `model_sha256` | its hash (null when there is no model) |
| `code` | the files that determine the output, each with its sha256 |
| `output_path` | the output CSV |
| `output_rows` | its data rows |
| `output_sha256` | its hash |
| `versions` | tool and library versions, and the runtime and engine list when the oracle reports them |
| `platform` | the platform string |
| `inputs` | count, seed, scenario, gain box, oracle and sampler names, the column names, and anything the experiment declares (for the v2 runs the exclusion record) |
| `parents` | the entries whose outputs this run read, with their hashes taken before it ran |
| `supersedes` | the earlier entry ids this run replaces (empty when none; unknown ids and itself are refused) |
| `prev_hash` | the previous entry's hash |
| `entry_hash` | the hash of this entry without this field |

The output hash is an exact-match integrity check of the committed file. Regeneration is judged by
tolerances, because the integration of the slew is not bit-reproducible across platforms. The
tolerances of each dataset are in its entry (`adopted`) or in `tests/test_v2_data.py`.

## The cadCAD-like mapping

cadCAD is a Python library for simulating systems by state updates.

<!-- cadcad:begin -->
> An experiment reads like a cadCAD simulation configuration:
>
> * state = a configuration (the design variables) and its measurements;
> * policy = the sampler, which draws the configurations;
> * state-update block = configure, measure, account (the oracle's work on one configuration);
> * run = one seeded design (design ``i`` depends on ``(seed, i)`` only);
> * sweep = scenario or gain-box cells, one run of the experiment and one ledger entry per cell;
> * timestep = only where a flow has one (the slew simulation inside a measurement does; the
>   experiment itself does not).
>
> Where the mapping does not fit: the flow is one-shot (draw, measure, write), with no timesteps
> over the experiment, no feedback from one design to the next and no state carried between
> designs. The "policy" has no inputs. Physical-test and human-assessment oracles have no
> simulation inside the measurement at all.
<!-- cadcad:end -->

## The toolkit account

The model uses the runtime's checking and simulation machinery where it supports them, and Python
holds only what the model language cannot do. Probe numbers are those of
`experiments/probes/probe-record.md`, and `experiments/probes.py` re-runs them against the live
runtime. Documentation sections are those of the runtime's Python client and of the toolkit (README
and `CLI.md`). The client's own documents are `docs/clients/python/verification.md`, which is not a
path in this repository, and its README, "The service".

<!-- toolkit:begin -->
| capability | documentation section | used | why | probe |
|---|---|---|---|---|
| `verify_constraint`, `holds` and `satisfiable` questions | verification.md, "Questions beyond evaluation" | used | claims over every in-range configuration and the exclusion of regions, on the `solve` engine with proved or witnessed evidence; a claim that invokes a `calc def` is undecided on every engine, so claims are restated over scalar features | 5 |
| `verify_requirement` | verification.md, "Constraints, requirements and satisfaction" | used | the four flags are the verdicts of named requirements on a subject configuration, engine `run`, evidence observed; each has a negative control | 4 |
| `verify_satisfaction` | verification.md, "Constraints, requirements and satisfaction" | used | the model's `satisfy` statements hold on the baseline and fail on a deliberately infeasible part; a false `assert satisfy` still loads clean, so the check is run, not assumed | 2, 3, 4 |
| `calc` | verification.md, "Calculations, analyses and sweeps" | used | the accounting `calc def`s are evaluated by the model; values carry unsimplified base-unit labels, so every read converts with `in_unit` | 6, 8 |
| `run_analysis` | verification.md, "Calculations, analyses and sweeps" | used | `SlewExperiment` returns the computed attributes from the configuration and the measured slew handed in as `in` parameters | 6 |
| `run_sweep` | verification.md, "Calculations, analyses and sweeps" | used for checks, not for sampling | a grid over the energy integral reproduces the accounting; the sampler stays in Python because the sweep draw is uniform with no log range | 6 |
| `record_run` | verification.md, "Calculations, analyses and sweeps" | not used | the ledger is a hashed JSONL file with git state and file hashes; a recording returns a new document, leaves the loaded model unchanged and stamps a wall-clock time | 7 |
| `run_runs` | verification.md, "Calculations, analyses and sweeps" | not used | it repeats an action with modeled randomness; the oracle is deterministic and an ordinary analysis case is refused | 7 |
| engine `run` | verification.md, "Choosing an engine and reading evidence" | used | per-configuration requirement verdicts and analyses, evidence observed | 4, 10 |
| engine `solve` | verification.md, "Choosing an engine and reading evidence" | used | proved verdicts for claims and for the exclusion of regions and model variants; needs `z3` on `PATH` | 5, 10 |
| engine `sweep` | verification.md, "Choosing an engine and reading evidence" | used | behind `run_sweep` | 6, 10 |
| engine `smt` | verification.md, "Choosing an engine and reading evidence" | not used | it answers over schedules and answers no constraint claim here | 5, 10 |
| engine `check` | verification.md, "Choosing an engine and reading evidence" | not used | it cannot leave the inputs free, which a claim over a range needs | 5, 10 |
| engine `explore` | verification.md, "Choosing an engine and reading evidence" | not used | it explores behaviors and the model declares none | 10 |
| engine `tool:fmi` | verification.md, "Choosing an engine and reading evidence" | not used | not ready here (the runner variable is unset) and outside the scope | 10 |
| `check` (CLI) | toolkit CLI.md, `check` | used | static checks on the model in the default test suite, with the pinned binary | 11 |
| `lint` (CLI) | toolkit CLI.md, `lint` | used | no errors and no warnings on the model, in the default test suite | 11 |
| `verify --solve` (CLI) | toolkit README, "Calculation and static-analysis boundaries" | used | joint satisfiability of the model's asserted constraints with a gating exit code; the runtime's `solve` engine gives the three-way answer for claims, so the CLI is the CI gate and not the claim checker | 11 |
<!-- toolkit:end -->

The binary is pinned in `experiments/toolkit-pin.toml` with a checksum per platform.
`experiments/toolkit.py` fetches and verifies it, and nothing downloads unless that script is run.

## Z3 excludes infeasible configurations before simulation

Z3 is a constraint solver. A region of the configuration space (a battery range) is a box over scalar
variables. `experiments/exclusion.py` restates the feasibility condition of the region over the
same scalars, with the model's constants read from the model, and asks the `solve` engine two
questions about two constraints appended to the model text:

| question | constraint | answer | classification |
|---|---|---|---|
| `satisfiable` | the region and the condition | `unsatisfiable`, proved | excluded: no configuration of the region is feasible, none is simulated |
| `holds` | the region implies the condition | `holds`, proved | all feasible: nothing to exclude |
| both | otherwise | `satisfiable` and `violated` | mixed: keep the region, test each point |

The same classification applies to a model variant (the model text with other literal ranges or
constants, `model_variant`). A variant in which no configuration is feasible is excluded: `build` in
`experiments/cubesat_oracle.py` then raises `ExcludedVariant` and nothing is simulated.

The recipe, run by `tests/test_case_model_howto.py` (`ADCS` is `examples/adcs`):

```python exclusion-example
from experiments.exclusion import battery_region, classify_region, exclusion_record

text = (ADCS / "model_v2" / "cubesat.sysml").read_text()
verdict = classify_region(text, battery_region((20, 26)))  # battery 20 to 26 Wh
record = exclusion_record(verdict)  # what a ledger entry stores
assert verdict.verdict == "excluded"
assert record["satisfiable"] == ["unsatisfiable", "proved"]
```

The battery range 20 to 26 Wh is proved infeasible, and designs sampled there are simulated anyway
to compare. Every one has `dod_ok` false
(`tests/test_cubesat_oracle.py::test_flags_observe_the_excluded_battery_region`). The range 40 Wh
and up, with the slew loss bounded, is proved all feasible, and every sampled design has `dod_ok` true
(`tests/test_cubesat_oracle.py::test_flags_observe_the_all_feasible_battery_region`).

`build` classifies the declared design space once and stores the block in the experiment's
`inputs["exclusion"]`. When the whole variant is proved infeasible, `build` raises before anything
is simulated, and the runner first appends an `exclusion` entry. The entry holds the variant's
edits, the classified regions with claim, engine, verdict, strength and witnesses, the model hash
and the reason.
When the exclusion block in `inputs["exclusion"]` has a
region classified `excluded`, the runner wraps the sampler in `runner.ExcludingSampler`. It takes
the base sampler's designs in order, skips any design inside an excluded region and keeps the first
`count` others with their original `design_id` and `seed`. The entry's `inputs["excluded_sampling"]`
records the regions, the designs examined and the draws avoided (per region). The experiment names the
design column of each region variable in `inputs["exclusion_columns"]`; an excluded region without
it is an error rather than a silent no-op. Regions that are not excluded are sampled whole and the
flags remain observations. The declared space excludes nothing, so for every committed dataset the
sampler is the base sampler and no data changed.
`design_space_regions` covers power and depth of discharge, not momentum, because the momentum
condition depends on the configuration through the inertia and is the closed-form approximation.
The closed-form bang-bang peak momentum is an approximation that the
integrated slew overshoots, so an excluded wheel region is a necessary-condition result that the
simulation confirms, and "all feasible" there means feasible by the closed form. The momentum
condition on the integrated slew is outside what the solver can represent, so it is not classified
and stays an observation of the simulation.

The four Python flags (`settled`, `momentum_ok`, `power_ok`, `dod_ok`) are not the
definition of feasibility; the requirements and the solver's classification of regions are.

## The legacy geostationary oracle and the scope-sensitivity experiment

The first case of this repository, the geostationary spacecraft of `design_space.py`, is kept
frozen and runnable. `experiments/legacy_oracle.py` puts `design_space.evaluate_design` behind the
same `Oracle` protocol (`LegacyGeostationaryOracle`, evidence `simulation`, the frozen keys and
column order), with no edit to the frozen modules and no need for `opensysml`. The ledger entry
`adopted-adcs_designs` registers its dataset as the legacy oracle.

From the repository root, this runs both oracles on the same designs:

```
PYTHONPATH=examples/adcs uv run python -m experiments run scope-sensitivity-shared-subspace
```

There are 20 draws, over the variables the two variants share. Wheel class and tracker grade are
shared over the levels both declare; the controller gain Kp is shared over the overlap of the v2 gain box and the
frozen range. The gain Kd carries the same name but the ranges do not overlap, so it is fixed in each
variant (1.0 in v2, the frozen baseline 10.0). The variables that belong to one variant only
are fixed at declared values (panel span 0.6 m and battery 80 Wh in v2; panel mass 30 kg and
antenna mass 18 kg in the frozen variant). Each oracle keeps its own scenario. The two ledger
entries (`scope-sensitivity-shared-subspace-v2`, `-legacy`) record the subspace in
`inputs["shared_subspace"]`, and `legacy_oracle.side_by_side` joins the two CSVs on `design_id`.

## Provide the oracle: three small cases through the same runner and ledger

Your case needs an oracle, a sampler and an experiment declaration. The three oracles share two
design variables, `gain` and `size`. The runner, the sampler class and the ledger are the ones the
cubesat uses. The test in `tests/test_case_model_howto.py` extracts these blocks and runs them, so
the text shown is the fixture.

The common part: a base class that gives the batch form from the single-configuration call.

```python toy-common
import pandas as pd
from experiments.oracle import evaluate_rows
from experiments.runner import LogUniformSampler


class Base:
    config_names = ("gain", "size")

    def evaluate(self, designs):
        return evaluate_rows(self, designs)
```

### A simulator: a SysML model with a stub measurement

The toy model, in SysML (a systems-modelling language), declares the design ranges, one cost the
model computes, and a budget requirement. Save it as `toy.sysml`.

```sysml toy-model
package Toy {
    private import ScalarValues::*;
    doc /* A toy plant: two design variables, a cost the model computes, a budget requirement. */

    part def Plant {
        attribute gain : Real default = 1.0;
        attribute size : Real default = 1.0;
        attribute cost : Real = 2.0 * gain + size;
    }

    part ranges {
        doc /* The design ranges; the sampler reads them from here. */
        attribute gainMin : Real = 0.5;
        attribute gainMax : Real = 8.0;
        attribute sizeMin : Real = 1.0;
        attribute sizeMax : Real = 4.0;
    }

    requirement def Affordable {
        subject p : Plant;
        attribute budget : Real default = 10.0;
        require constraint { p.cost <= budget }
    }
}
```

The oracle configures a `Plant` from the design, reads the cost from the model, takes the flag from
verifying the requirement, and gets the settling time from a stub that stands in for a simulator.

```python toy-simulator
import opensysml


def settle_s(gain):  # the stub measurement; replace with your simulator
    return 10.0 / gain


def ranges(text):
    m = opensysml.connect().load_from_content(text, strict=True)
    g = lambda name: float(m.eval(f"Toy::ranges.{name}"))
    return {"gain": (g("gainMin"), g("gainMax")), "size": (g("sizeMin"), g("sizeMax"))}


class ToySimulator(Base):
    attribute_names = ("cost", "settle_s")
    flag_names = ("affordable",)

    def __init__(self, model_text):
        self.text, self.conn = model_text, opensysml.connect()

    def __call__(self, c):
        part = (
            "package Cfg { part p : Toy::Plant { "
            f":>> gain default = {float(c['gain']):.17g}; :>> size default = {float(c['size']):.17g}; "
            "} }"
        )
        m = self.conn.load_from_content(self.text + "\n" + part, strict=True)
        ok = m.verify_requirement("Toy::Affordable", subject="Cfg::p").holds
        return {
            "cost": float(m.instantiate("Cfg::p").get("cost")),
            "settle_s": settle_s(float(c["gain"])),
            "affordable": bool(ok),
        }
```

### A physical test campaign: recorded measurements, nothing simulated

The configurations are the ones the campaign tested, and the measurements are read from a file.
Save this as `campaign.csv`.

```csv campaign-file
gain,size,cost,settle_s
0.8,1.5,3.2,12.9
1.6,2.0,5.4,6.1
3.1,3.5,9.8,3.3
4.4,2.5,11.6,2.4
6.0,1.2,13.4,1.7
7.5,3.8,18.9,1.4
```

The sampler returns the tested configurations; the oracle looks each up and refuses a
configuration that was not tested.

```python toy-physical
class CampaignSampler:
    def __init__(self, path):
        self.table = pd.read_csv(path)

    def draw(self, n, seed):
        t = self.table.head(n)
        return pd.DataFrame(
            {"design_id": range(len(t)), "seed": seed, "gain": t["gain"], "size": t["size"]}
        )


class RecordedTests(Base):
    attribute_names = ("cost", "settle_s")
    flag_names = ("affordable",)

    def __init__(self, path):
        self.table = pd.read_csv(path).set_index(["gain", "size"])

    def __call__(self, c):
        try:
            r = self.table.loc[(c["gain"], c["size"])]
        except KeyError:
            raise ValueError(f"no recorded test for gain={c['gain']}, size={c['size']}") from None
        return {
            "cost": float(r.cost),
            "settle_s": float(r.settle_s),
            "affordable": bool(r.cost <= 10.0),
        }
```

### A human assessment: scores from a callable standing in for raters

The oracle collects scores for a configuration and averages them.

```python toy-human
class PanelRatings(Base):
    attribute_names = ("rating",)
    flag_names = ("acceptable",)

    def __init__(self, rater):
        self.rater = rater

    def __call__(self, c):
        scores = list(self.rater(c))
        mean = sum(scores) / len(scores)
        return {"rating": mean, "acceptable": mean >= 3.0}


def rater(c):  # three raters; replace with the collection of real scores
    base = 5.0 - 0.4 * float(c["size"])
    return [base - 0.5, base, base + 0.5]
```

### Run all three through the runner and the ledger

Each experiment declares its evidence kind. The simulator names its model, so the entry carries the
model hash. The campaign file is listed as a code file, because it determines the output and is
hashed with it. `root` is the directory holding `toy.sysml` and `campaign.csv`.

```python toy-run
from experiments import ledger as lg
from experiments import runner
from experiments.experiment import Experiment

ledger = root / "ledger.jsonl"
model = (root / "toy.sysml").read_text()
draw = LogUniformSampler({}, ranges(model))

simulation = Experiment(
    id="toy-simulation",
    output="out/simulation.csv",
    count=4,
    seed=0,
    oracle="toy-simulator",
    sampler="log-uniform",
    model_path="toy.sysml",
    evidence_kind="simulation",
)
physical = Experiment(
    id="toy-physical",
    output="out/physical.csv",
    count=4,
    seed=0,
    oracle="recorded-tests",
    sampler="campaign",
    code=("campaign.csv",),
    evidence_kind="physical-test",
)
human = Experiment(
    id="toy-human",
    output="out/human.csv",
    count=4,
    seed=0,
    oracle="panel-ratings",
    sampler="log-uniform",
    evidence_kind="human-assessment",
)

runner.run(simulation, ToySimulator(model), draw, root, ledger)
runner.run(
    physical,
    RecordedTests(root / "campaign.csv"),
    CampaignSampler(root / "campaign.csv"),
    root,
    ledger,
)
runner.run(human, PanelRatings(rater), draw, root, ledger)
assert lg.verify(ledger, root) == []
```

The three entries differ in `evidence_kind` and in what they hash: the simulation entry has the model
hash, the other two have none. The test checks this, that the ledger verifies, and that each
output holds what its evidence says. For the simulator that is the model's accounting and
requirement, for the campaign the recorded numbers, for the panel the averaged scores.

To plug in your own case: write the oracle, choose the sampler, and declare the experiment with its evidence kind. Estimators
downstream read the CSV the runner writes; they do not know which kind of evidence stood behind it.

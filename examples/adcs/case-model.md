# The cubesat model, the experiment layer and how to plug in your own case

This is the how-to for `examples/adcs/`. The method sees one thing: a map from configurations to
attributes. This page separates that map from the physics of this example, shows how to read the
model that provides it, how to run an experiment and read its ledger, and how to provide the
same map from a simulator, a physical test campaign or a human assessment.

Two generations sit in the directory until the swap gate. The **frozen** generation
(`cubesat_model.py`, `cubesat_tradespace.sysml`, `generate_dataset.py`, `make_check_designs.py`,
`design_space.py`, `extended_design_space.sysml`, and the CSVs in `data/`) is what the paper and the
records cite; it stays as it is. The **v2** generation (`model_v2/cubesat.sysml`, `experiments/`,
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

To run your own case you replace three things and keep the rest: the **oracle** (what turns a
configuration into attributes), the **sampler** (how configurations are drawn, or which are
tested), and the **experiment declaration** (names, count, seed, evidence kind). The runner and the
ledger are unchanged; the toy cases at the end of this page show it.

## Reading the model top to bottom

`model_v2/cubesat.sysml` is one file and one package, `CubesatTradeSpaceV2`, read in this order.
The table is generated from the file by `tests/test_case_model_howto.py`; the line pointers follow
the file.

<!-- sections:begin -->
| section | title | lines |
|---|---|---|
| 1 | CONFIGURATION SPACE (configuration view): what can be chosen | 80 to 180 |
| 2 | THE CUBESAT (configuration view): composition and environment | 182 to 292 |
| 3 | ACCOUNTING (assessment view): mass, power, energy, inertia, pointing | 294 to 466 |
| 4 | SCENARIOS (assessment view): the slew, and a closed-form approximation of it | 468 to 542 |
| 5 | REQUIREMENTS, SATISFACTION AND VERIFICATION (assessment view; 15.2, WP22) | 544 to 814 |
| 6 | THE EXPERIMENT (assessment view): configuration and measured slew in, attributes out | 816 to 845 |
| 7 | NAMED CONFIGURATIONS (configuration view) | 847 to 870 |
<!-- sections:end -->

What to take from each section:

- **Configuration space.** The two enumerations (wheel class, star-tracker grade), the abstract
  part definitions with one concrete alternative per literal carrying its attribute table, the
  continuous ranges, and both gain boxes (baseline and aggressive) as named parts. The sampler
  reads all of it from here; no range, literal or constant is copied into Python.
- **The cubesat.** The composition (panels, battery, wheel, tracker, controller) and the
  environment (eclipse, loads).
- **Accounting.** One `calc def` per accounting quantity: masses, power, energy balance, eclipse
  reserve, pointing error, depth of discharge. Each constant has a `doc` rationale beside it.
- **Scenarios.** The nominal slew as a named part (angle, horizon, step, bands), and a closed-form
  approximation of the slew for model checking. The integration of the slew itself is in Python
  (`adcs_sim.simulate_adcs`), because the model language cannot integrate the equations of motion.
- **Requirements.** Feasibility as named requirements (`settled`, `momentum_ok`, `power_ok`,
  `dod_ok` are their verdicts), the requirements over the other traded metrics, `satisfy`
  statements tying them to the baseline, verification definitions naming what each verifies, and
  claims over every in-range configuration. Which quantity each requirement reads is the table of
  the next section.
- **The experiment.** `analysis def SlewExperiment` takes the configuration and the measured slew
  quantities and returns the attributes the model computes. The measured quantities are not
  computed; they pass into the row from the measurement.
- **Named configurations.** The baseline and two contrasts (agile, compact).

The model has two views, generated from its elements and committed in `model_v2/views/`
(PlantUML text, SVG and PNG). The assembly view (`assembly_view`) shows what a configuration is:
the parts, the alternatives swapped for a categorical variable and the parameters tuned for a
continuous one. The behavioural view (`behavioural_view`) shows how a configuration is assessed:
for each traded metric, the requirement that reads it, or none, and where the metric comes from
(the analysis or the measured slew). The generator is
`docs/superpowers/notes/spike-sysml-diagrams/project.py` (`render.sh` there draws the SVG and PNG);
`tests/test_system_model_v2_r1.py` checks that the committed text is its output on this file.

## From the assembly to the dataset: measures of effectiveness and measures of performance

This section reads the model `model_v2/cubesat.sysml` as adopted at the package's data gate
(`work-packages/WP23-scope-of-work.md`, G8; the version it replaced is in history at d3018ba, and
the section table above is this file's). The chain is short.
A configuration is what the assembly view shows: two swaps (the wheel class, the star-tracker
grade) and four tunes (the panel span, the battery capacity, the gains Kp and Kd). The assessment
turns a configuration into nine traded metrics: the slew is integrated once and measured, the
accounting calcs are evaluated, and the experiment returns the metrics as one row of the dataset,
with the four flags beside them. Each metric is marked in the model as a measure of effectiveness
(MoE) or a measure of performance (MoP), by one rule stated in the model's top comment: an MoE is a
measure a stakeholder states without knowing the design; an MoP is a measure of the system's
performance under the scenario the engineer states. Two MoEs (the pointing error and the launch
cost) and eight MoPs: the stakeholders ask for a payload that points and a launch they can afford;
everything else is how the design performs under the engineer's slew and orbit. Each metric is read
by a requirement on its own quantity and verified in a verification case (`model_v2/views/coverage.md`,
second table; `tests/test_model_coverage.py::test_every_traded_metric_has_a_requirement_that_reads_it_and_a_mark`).

### The traded metrics in their disciplines' words

Control (the attitude loop under the nominal slew, a 30 degree slew with a 600 s horizon).

- **Settling time** (MoP, measured): the hold time, the first time after which the pointing error
  stays inside the settling band, a fraction of the slew's initial error; computed by event detection
  as the last exit from the band, so a slew that never holds inside the band has the horizon as its
  settling time. It is the case's one time metric: the slew time (first entry into a band) left the
  traded metrics with WP16's decision (`WP16-decisions.md`, "Slew time under event detection").
- **Pointing error** (MoE, a calc of the configuration): how well the payload points, the
  root-sum-square of the steady attitude error under the disturbance and gravity-gradient torques
  (the torque over Kp) and the star tracker's accuracy.
- **Control effort** (MoP, measured): the integral of the wheel torque magnitude over the slew,
  in N.m.s; what the slew asks of the wheels.

Power and energy (the panels, the battery and the loads under the stated orbit and eclipse).

- **Power margin** (MoP): the generated power left after the housekeeping load and the peak slew
  power, at the peak of the slew in sunlight.
- **Energy balance** (MoP): over one orbit, the energy the panels supply in sunlight less the base
  load over the orbit and the slew's loss energy.
- **Eclipse reserve** (MoP): the energy left in the battery above the allowed depth of discharge
  after the eclipse demand (the base load over the eclipse plus the slew's loss energy).
- **Depth of discharge** (MoP): the eclipse demand over the battery capacity.
- **Peak slew power** (MoP): the electrical draw at the peak of the slew, the tracker's power plus
  the idle wheels plus the wheels' loss at the peak torque.

Mass and cost.

- **Total mass** (MoP): the launch mass of the configuration, the sum of the bus, battery, panels,
  antenna, wheels, tracker and IMU masses.
- **Launch cost** (MoE, not traded): the launch rate times the total mass, increasing in mass. The
  rate (6000 USD per kilogram) is an illustrative constant labelled like the model's other
  constants, not a cited price. The launch cost is the stakeholder's measure on the mass and the
  quantity its requirement reads; the total mass stays the traded metric and the dataset gains no
  column (`WP23-decisions.md`, OD1 and OD2;
  `tests/test_system_model_v2.py::test_launch_cost_is_the_rate_times_the_total_mass_and_increases_with_it`).

### The requirements and what each reads

| requirement | reads | bound | where the bound comes from |
|---|---|---|---|
| `SettledRequirement` (the flag `settled`) | the measured settling time | below the slew's horizon | the scenario |
| `MomentumRequirement` (`momentum_ok`) | the measured peak momentum | within the wheel's momentum capacity | the wheel class |
| `PowerRequirement` (`power_ok`) | the available power | positive | the accounting |
| `DepthOfDischargeRequirement` (`dod_ok`) | the depth of discharge | within the environment's allowed depth | the environment |
| `EclipseReserveRequirement` | the eclipse reserve | not negative | zero |
| `PowerMarginRequirement` | the power margin | not negative | zero |
| `EnergyBalanceRequirement` | the energy balance | not negative | zero |
| `PointingErrorRequirement` | the pointing error | within `budgets.pointingErrorLimit` | proposed (below) |
| `ControlEffortRequirement` | the measured control effort | within `budgets.controlEffortLimit` | proposed |
| `PeakSlewPowerRequirement` | the peak slew power | within `budgets.peakSlewPowerLimit` | proposed |
| `LaunchBudgetRequirement` | the launch cost (the MoE on the total mass) | within `budgets.launchBudget` | proposed |
| `BatteryPeakPowerRequirement` | the eclipse peak load (housekeeping plus the peak slew power) | within the pack's peak power, its discharge rating times its capacity | the battery's rating (below) |

The first four are the flags of the dataset, the verdicts of named requirements on each simulated
configuration. The four thresholds marked proposed are not the supervisor's values and not the
model's own: the loop proposed one rule for all four, so that none is tuned to a metric or to a
figure, each threshold the baseline configuration's own value with a 20 % margin (`budgets.margin`,
1.2), the allowance an engineer carries on a budget at an early phase. They are pending the
supervisor's approval at the data gate and are read from the model by
`tests/test_system_model_v2.py::test_proposed_thresholds_are_the_baselines_values_with_the_stated_margin`:
a pointing error of 0.018642 degree, a control effort of 0.011389 N.m.s, a peak slew power of
2.4 W and a launch budget of 95,698.29 USD (15.950 kg at the rate) (`WP23-review.md`, "Proposed
thresholds"). The battery's discharge rating is proposed likewise: a continuous rating of 1 C
(`environment.batteryDischargeRate`, 1.0 per hour), the pack delivering its capacity in one hour,
the plain rating of a small-satellite lithium-ion pack and not a cited one (`WP23-review.md`,
"Round 2"). None of these thresholds enters the dataset: the four flags stay what they are, so a
threshold changes the model's statement, the views and the coverage table, and cannot move a fit.

### Coverage: every swap and tune reaches a metric

The coverage table (`model_v2/views/coverage.md` and `.csv`, generated from the model by
`model_v2/coverage.py`) states, for each decision element and each traded metric, whether the model
has a path from the metric back to the element and whether a one-at-a-time change of the element
at the three named configurations moves the metric. Every swap and tune reaches at least one
traded metric in both columns, and every traded metric is reached: the two swaps, the panel span
and the battery reach all nine, Kp eight (not the total mass: the mass accounting has no gain in
it) and Kd seven (not the total mass or the pointing error, whose closed form has Kp alone)
(`tests/test_model_coverage.py::test_no_decision_element_row_is_empty_structurally`,
`test_no_decision_element_row_is_empty_empirically`,
`test_the_gains_do_not_reach_the_mass_and_kd_does_not_reach_the_pointing_error`). Seven cells
disagree between the columns, with one cause: the power margin and the peak slew power read the
measured peak torque, which at all three named configurations is the wheel class's maximum, because
the power cap does not bind there; the model allows the effect, the three configurations do not
show it (`WP23-review.md`, "Coverage findings").

The table's third part is the coupling between subsystems, in the form of the design structure
matrix of multidisciplinary design analysis and optimization (MDAO), the family the paper names
beside this method; the form is the XDSM of Lambe and Martins (`lambe2012extensions` in
`docs/references.bib`) without its process line. Rows feed columns: the configuration values feed
the three subsystems of the behavioural view (controls; power and energy; mass), the subsystems
exchange named coupling variables (the measured peak torque and the torque-squared integral from
the controls to the power subsystem; the usable wheel torque and the panel mass back; the battery
and panel masses into the mass accounting; the structure mass and the inertias from the mass
accounting to the controls), and the metrics and requirements are read off the subsystems. The
graph of configuration values, subsystems and metrics is connected, and the controls and the power
subsystem feed each other, a loop the model resolves in one pass because the usable torque is a
quantity of the configuration computed before the slew and the peak torque is read after it
(`tests/test_model_coverage.py::test_every_configuration_value_feeds_a_subsystem_and_the_graph_is_connected`,
`test_coupling_variables_between_subsystems_are_the_models_named_quantities`).

### The texture hypothesis and what the fit returned

The hypothesis (the supervisor's, quoted in `WP23-scope-of-work.md`, Purpose): once the configuration space and the metric
space are each explicit and joined by requirements, the K = 1 exponent heatmap across the fit
temperature shows more texture, more metrics carrying weight. It is a hypothesis the regenerated
figure checks after the data gate, never a target: no metric, threshold or constant of the model
was chosen because it moves the heatmap, and the fit runs unchanged on whatever the model produces
(`WP23-scope-of-work.md`, non-goals).

What the fit returned in round 3, on the round-1 data (the regeneration moves these values; what
follows is their reading, not a result of record). In the primary regime three metrics carry no
exponent at any fit temperature of the sweep: the power margin, the eclipse reserve and the peak
slew power; in the baseline regime the peak slew power alone (`WP23-review.md`, "Round 3"). The
K = 1 fit is one monomial term, a hyperplane in log-metric space, and a metric carries weight
only where it trades against the others at the frontier: the contending set is found from the
data (`docs/theory.md`, "Elasticities and the n-lemma"). Read that way, each zero has a reason in
the metric set rather than in the configuration space.

- The eclipse reserve is carried by the depth of discharge. Given the tracker grade, both are
  monotone functions of the one battery capacity (the reserve is the allowed depth times the
  capacity less the eclipse demand; the depth of discharge is the demand over the capacity), so
  they are one quantity to the fit and cannot both contend; the fit gave the depth of discharge the
  weight. The reserve binds on the data before the fit, as the `dod_ok` flag, and the two
  requirements are the same inequality.
- The power margin is carried by the energy balance. Both are affine in the generated power, which
  is proportional to the panel span: one is instantaneous at the slew's peak in sunlight, the other
  integrated over the orbit. Which of the pair carries the weight is the linear program's choice,
  and it changed between the regimes (the energy balance in the primary regime, the power margin in
  the baseline regime), which is the sign of the collinearity.
- The peak slew power is a step function of the two swaps. With the peak torque at the wheel class's
  maximum it takes one value per wheel class and tracker grade, so it is flat inside each cell of the
  design space those swaps cut, and across the cells it orders the designs as the total mass does
  (the heavy wheel draws the power). One hyperplane over all the cells can use no elasticity from a
  metric that is flat inside each, and the ordering across them is the total mass's. With three
  terms (K = 3) it leads a term in both regimes, the cell of the large-wheel designs, where the
  draw trades against the settling time.

None of this is a change to the model (round 3 changed none: `WP23-review.md`, "Model change in
round 3"), and none of it says whether the texture is good or bad; it says what the metric set
contains, two pairs that are one quantity each and one metric that steps with the swaps, and that
is the supervisor's to change at the gate, not the loop's.

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
  the parent experiments. Nothing earlier is rewritten; the superseded entry keeps the hashes of the
  model and code it ran with, which is the history. If the re-run overwrote the output file, the
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
| `inputs` | count, seed, scenario, gain box, oracle and sampler names, the column names, and anything the experiment declares (for the v2 runs the exclusion record, below) |
| `parents` | the entries whose outputs this run read, with their hashes taken before it ran |
| `supersedes` | the earlier entry ids this run replaces (empty when none; unknown ids and itself are refused) |
| `prev_hash` | the previous entry's hash |
| `entry_hash` | the hash of this entry without this field |

The output hash is an exact-match integrity check of the committed file. Regeneration is judged by
tolerances, because the integration of the slew is not bit-reproducible across platforms; the
tolerances of each dataset are in its entry (`adopted`) or in `tests/test_v2_data.py`.

## The cadCAD-like mapping

An experiment reads like a cadCAD simulation configuration. The mapping is stated once, in the
docstring of `experiments/experiment.py`; the block below is that text, generated from it.

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
holds only what the model language cannot do. The table lists each capability with the
documentation section it rests on, whether this example uses it, why, and the probe that backs the
statement. Probe numbers are those of `experiments/probes/probe-record.md`; `experiments/probes.py`
re-runs them against the live runtime, and `tests/test_model_checking_v2.py::test_probe_still_holds`
fails by probe name when a recorded result no longer holds. Documentation sections are those of the
runtime's Python client (`docs/clients/python/verification.md`, and the client README, "The
service") and of the toolkit (README and `CLI.md`).

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

The binary is pinned in `experiments/toolkit-pin.toml` with a checksum per platform, and
`experiments/toolkit.py` fetches and verifies it; nothing downloads unless that command is run.

## Z3 excludes infeasible configurations before simulation

The solver side runs before any simulation. A region of the configuration space (a battery range, a
wheel class with a range of inertias on the nominal slew, a panel-span range) is a box over scalar
variables. `experiments/exclusion.py` restates the feasibility condition of the region over the
same scalars, with the model's constants read from the model, and asks the `solve` engine two
questions about two constraints appended to the model text:

| question | constraint | answer | classification |
|---|---|---|---|
| `satisfiable` | the region and the condition | `unsatisfiable`, proved | excluded: no configuration of the region is feasible, none is simulated |
| `holds` | the region implies the condition | `holds`, proved | all feasible: nothing to exclude |
| both | otherwise | `satisfiable` and `violated` | mixed: keep the region, test each point |

The same classification of a model variant (the model text with other literal ranges or constants,
`model_variant`) excludes a variant in which no configuration is feasible; `build` in
`experiments/cubesat_oracle.py` then raises `ExcludedVariant` and nothing is simulated
(`tests/test_cubesat_oracle.py::test_a_variant_without_a_feasible_configuration_is_not_simulated`).

The recipe, run by `tests/test_case_model_howto.py` (`ADCS` is `examples/adcs`):

```python exclusion-example
from experiments.exclusion import battery_region, classify_region, exclusion_record

text = (ADCS / "model_v2" / "cubesat.sysml").read_text()
verdict = classify_region(text, battery_region((20, 26)))  # battery 20 to 26 Wh
record = exclusion_record(verdict)  # what a ledger entry stores
assert verdict.verdict == "excluded"
assert record["satisfiable"] == ["unsatisfiable", "proved"]
```

An example from the tests: the battery range 20 to 26 Wh is proved infeasible, and designs sampled
there are simulated anyway to compare. Every one has `dod_ok` false
(`tests/test_cubesat_oracle.py::test_flags_observe_the_excluded_battery_region`); the range 40 Wh
and up, with the slew loss bounded, is proved all feasible and every sampled design has `dod_ok` true
(`tests/test_cubesat_oracle.py::test_flags_observe_the_all_feasible_battery_region`).

The ledger records what was excluded and why. `build` classifies the declared design space once and
stores the block in the experiment's `inputs["exclusion"]`: per region the claim text, the engine,
the verdict, the evidence strength, the witness and the model hash
(`tests/test_cubesat_oracle.py::test_the_exclusion_block_records_the_classification_of_the_declared_space`).
When the whole variant is proved infeasible, `build` raises before anything is simulated, and the
runner first appends an `exclusion` entry: the variant's edits, the classified regions with claim,
engine, verdict, strength and witnesses, the model hash and the reason
(`tests/test_cubesat_oracle.py::test_a_proved_infeasible_variant_is_recorded_in_the_ledger_before_the_error`).
The sampler consumes excluded regions. When the exclusion block in `inputs["exclusion"]` has a
region classified `excluded`, the runner wraps the sampler in `runner.ExcludingSampler`, which takes
the base sampler's designs in order, skips any design inside an excluded region and keeps the first
`count` others with their original `design_id` and `seed`. The result is the unexcluded sampler's
draws with the excluded ones skipped, reproducibly; the entry's `inputs["excluded_sampling"]` records
the regions, the designs examined and the draws avoided (per region). The experiment names the
design column of each region variable in `inputs["exclusion_columns"]`; an excluded region without
it is an error rather than a silent no-op. Regions that are not excluded are sampled whole and the
flags remain observations. The declared space excludes nothing, so for every committed dataset the
sampler is the base sampler and no data changed
(`tests/test_cubesat_oracle.py::test_declared_space_excludes_nothing_so_the_first_designs_are_unchanged`;
a constructed space with the battery range 20 to 26 Wh excluded:
`tests/test_cubesat_oracle.py::test_sampler_skips_a_solver_excluded_battery_region`).
`design_space_regions` covers power and depth of discharge, not momentum, because the momentum
condition depends on the configuration through the inertia and is the closed-form approximation.
The momentum condition uses the closed-form bang-bang peak momentum, an approximation that the
integrated slew overshoots; an excluded wheel region is a necessary-condition result that the
simulation confirms, and "all feasible" there means feasible by the closed form. The momentum
condition on the integrated slew (the peak momentum of the ODE against the wheel class capacity) is
outside what the solver can represent, so it is not classified and stays an observation of the
simulation.

The four Python flags (`settled`, `momentum_ok`, `power_ok`, `dod_ok`) are observations of single
simulated configurations, produced by verifying the model's requirements. They are not the
definition of feasibility; the requirements and the solver's classification of regions are.

## The legacy geostationary oracle and the scope-sensitivity experiment

The first case of this repository, the geostationary spacecraft of `design_space.py`, is kept
frozen and runnable. `experiments/legacy_oracle.py` puts `design_space.evaluate_design` behind the
same `Oracle` protocol (`LegacyGeostationaryOracle`, evidence `simulation`, the frozen keys and
column order, no edit to the frozen modules; it needs no `opensysml`), and the ledger entry
`adopted-adcs_designs` registers its dataset as the legacy oracle.

From the repository root, this runs both oracles on the same designs:

```
PYTHONPATH=examples/adcs uv run python -m experiments run scope-sensitivity-shared-subspace
```

The draws are 20 of the variables the two variants share. Wheel class and tracker grade are
shared over the levels both declare; Kp is shared over the overlap of the v2 gain box and the
frozen range. Kd carries the same name but the ranges do not overlap, so it is fixed in each
variant (1.0 in v2, the frozen baseline 10.0), and the variables that belong to one variant only
are fixed at declared values (panel span 0.6 m and battery 80 Wh in v2; panel mass 30 kg and
antenna mass 18 kg in the frozen variant). Each oracle keeps its own scenario. The two ledger
entries (`scope-sensitivity-shared-subspace-v2`, `-legacy`) record the subspace in
`inputs["shared_subspace"]`, and `legacy_oracle.side_by_side` joins the two CSVs on `design_id`.
What the comparison shows is a later study; this is its definition and a small run.

## Provide the oracle: three small cases through the same runner and ledger

Your case needs an oracle, a sampler and an experiment declaration. Three oracles follow, each
the same shape and each satisfying the protocol above. They share two design variables, `gain` and
`size`; the runner, the sampler class and the ledger are the ones the cubesat uses. The test in
`tests/test_case_model_howto.py` extracts the blocks named below and runs them, so the text shown is
the fixture.

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

The toy model is about thirty lines. It declares the design ranges, one cost the model computes,
and a budget requirement. Save it as `toy.sysml`.

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
In your case that line is the call to your simulator.

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

The oracle collects scores for a configuration and averages them. The callable `rater` stands in
for the people filling in a form.

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
model hash; the campaign file is listed as a code file, because it determines the output and is
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
hash, the other two have none. The test checks that, that the ledger verifies, and that each
output holds what its evidence says: the model's accounting and requirement for the simulator, the
recorded numbers for the campaign, the averaged scores for the panel.

To plug in your own case: write the oracle (from a SysML model with a simulator, from your test
records, or from your raters' scores), choose the sampler (a log-uniform draw over ranges, or the
list of configurations you can test), and declare the experiment with its evidence kind. Estimators
downstream read the CSV the runner writes; they do not know which kind of evidence stood behind it.

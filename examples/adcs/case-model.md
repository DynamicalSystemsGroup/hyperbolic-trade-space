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
| 1 | CONFIGURATION SPACE: what can be chosen | 49 to 149 |
| 2 | THE CUBESAT: composition and environment | 151 to 247 |
| 3 | ACCOUNTING: mass, power, energy, inertia, pointing | 249 to 382 |
| 4 | SCENARIOS: the slew, and a closed-form approximation of it | 384 to 454 |
| 5 | REQUIREMENTS, SATISFACTION AND VERIFICATION (15.2) | 456 to 588 |
| 6 | THE EXPERIMENT: configuration and measured slew in, attributes out | 590 to 619 |
| 7 | NAMED CONFIGURATIONS | 621 to 644 |
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
  `dod_ok` are their verdicts), `satisfy` statements tying them to the baseline, verification
  definitions naming what each verifies, and claims over every in-range configuration.
- **The experiment.** `analysis def SlewExperiment` takes the configuration and the measured slew
  quantities and returns the attributes the model computes. The settling time and the slew time
  are measured, not computed, and pass into the row from the measurement.
- **Named configurations.** The baseline and two contrasts (agile, compact).

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
  parents) and prints one line per drift; it exits 1 on drift.
- `run <id>` executes the declared experiment and appends one entry. It refuses an id that already
  has an entry: the ledger is append-only. The ids of the v2 generation are `v2-primary`,
  `v2-baseline`, `v2-check-predictions` and `v2-check-designs`; the predictions are committed
  before the check designs are simulated, and the ledger order shows it.
- `adopt` registers the five frozen datasets without regenerating them.
- `compare` regenerates the v1 to v2 comparison report in `experiments/reports/`.

The ledger is `experiments/ledger/ledger.jsonl`, one JSON object per line. Each entry is chained to
the previous one by hash, so editing or deleting a line breaks `verify`.

### The ledger entry

| field | meaning |
|---|---|
| `id` | the experiment id (a sweep cell appends `[key=value]`) |
| `kind` | `generated` (the runner made the file) or `adopted` (the file existed before the ledger) |
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
The momentum condition uses the closed-form bang-bang peak momentum, an approximation that the
integrated slew overshoots; an excluded wheel region is a necessary-condition result that the
simulation confirms, and "all feasible" there means feasible by the closed form.

The four Python flags (`settled`, `momentum_ok`, `power_ok`, `dod_ok`) are observations of single
simulated configurations, produced by verifying the model's requirements. They are not the
definition of feasibility; the requirements and the solver's classification of regions are.

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

# Note: tidying the system model (the cubesat example): seams, breakout, parallel safety

Drafted 2026-11-08 by the driver as input to the WP15 scope (drafted by the PM's bounded scope
subagent, taken to the supervisor's gate by the driver). The supervisor's request, verbatim
(`work-packages/README.md`): "another round of tightening revisions i'd like to do is focused on the
system model. it got built up a bit ad hoc and its under utilizing the sysml toolkit. the example
was accreted and thus may seem a bit illegible and opaque. tightening it up to make better use of
the simulation machinery and model checking capabilities native to sysmlv2 models would make the
example more interpretable. strictly speaking our method needs to work for a black box that maps
configurations to attributes but a clean sysmlv2 model here with python scripting extensions for
scoping and ledgering experiments (with cadcad like semantics) would make it much more
interpretable for someone interested in cross applying to other sysml models. can you scope this as
a tidying work package and identify how to break it out so it can be worked in parallel without
disruption".

## What the example is today (accreted over WP4, WP4b, WP7, WP9)

| File | Lines | Role | Origin |
|---|---|---|---|
| `examples/adcs/adcs_sim.py` | 286 | the slew physics: inertia, step response, pointing budget, control effort (Apache-licensed port of ADCS-lifecycle-demo) | WP4 |
| `examples/adcs/design_space.py` | 138 | the WP4 design space (wheel class, tracker grade, gains, mass perturbation) and `evaluate_design` for the 10° geostationary case | WP4 |
| `examples/adcs/extended_design_space.sysml` | 46 | documentation-only SysML of the WP4 space (part defs and attribute defs, no calc, no constraints) | WP4 |
| `examples/adcs/cubesat_tradespace.sysml` | 366 | the WP4b cubesat configuration space: enums, abstract part defs with concrete alternatives, `DesignSpace` and `AggressiveGainSpace` ranges, `Cubesat` with mass and power `calc def`s, two `constraint def`s (PowerOK, DepthOfDischargeOK), `analysis def ModelTest` as documentation of the configure → test → measure flow | WP4b |
| `examples/adcs/cubesat_model.py` | 539 | the opensysml client: load, read ranges from the model, sample configurations, evaluate calcs and constraints through the runtime, call `adcs_sim` for the slew, assemble the ten attributes and flags (`measure`) | WP4b |
| `examples/adcs/generate_dataset.py` | 190 | CLI: seeded sampling, multiprocessing, two models (`adcs`, `cubesat`), two gain boxes; writes the CSVs | WP4, WP4b |
| `examples/adcs/make_check_designs.py` | 251 | propose (regressor on the chart) and simulate the six check designs | WP7 |
| `examples/adcs/k_terms.py` | 344 | the K = 1, 2, 3 record for both regimes (reads CSVs only) | WP9 |
| `examples/adcs/data/*.csv` | | `adcs_designs.csv` (WP4, 1000 rows), `adcs_designs_cubesat.csv` (stock gains), `adcs_designs_cubesat_gains.csv` (aggressive, the primary), `check_designs_cubesat.csv`, `check_predictions_cubesat.csv` | WP4, WP4b, WP7 |

Two generations coexist (the WP4 geostationary 10° case with four attributes, and the WP4b
cubesat 30° case with ten), with two SysML files of different ambition, Python holding the slew
physics outside the model, feasibility split between SysML constraints (power, depth of discharge)
and Python flags (settled, momentum), and the experiment protocol (seeds, workers, scenario
parameters, gain boxes) living in CLI flags and module constants rather than in a ledger.

## What the rest of the repository consumes from it (the seam)

- **The datasets, by path and column.** `tests/test_notebook.py`, `tests/test_adcs_enrichment.py`,
  `tests/test_check_designs.py`, `examples/adcs/k_terms.py`, the WP7 notebook, the K = 3 record, and
  WP10's case module read `examples/adcs/data/*.csv` and nothing else. Every number in WP7, WP9,
  the paper's case and the records rests on these files as committed.
- **Reproducibility pins.** `tests/test_adcs_case.py` regenerates the first 20 designs of the WP4
  CSV within the WP4 Amendment 1 tolerances and checks same-platform exactness;
  `tests/test_cubesat_model.py` regenerates designs of the cubesat CSVs through the opensysml
  runtime (fails loudly without it under `REQUIRE_OPENSYSML=1`); `tests/test_adcs_enrichment.py`
  checks the dataset's shape, flags and the probe tensions.
- **The simulator as a live oracle.** WP12 (the search) will call a configuration → attributes
  function with noise; today that is `cubesat_model.measure` for the cubesat and
  `design_space.evaluate_design` for WP4. The WP14 interface contract should pin that oracle
  signature.
- **The SysML model as documentation.** `docs/method.md` and the paper describe stage 1
  (evaluation) as a black box; the model is the worked example of what sits inside it.

So the seam is: the CSV files with their columns and the committed values; the oracle signature;
the model as a readable artifact. Everything behind the seam can change without disturbing the
method, the paper or the records, provided the seam holds.

## The one decision that fixes parallel safety

Does the tidied model have to reproduce the committed datasets (to the WP4 tolerances, with
the same seeds), or may it produce a new generation of data (`v2`) beside the old, which WP10
switches to only at a recorded gate?

- *Reproduce:* no disruption anywhere; the tidy-up is a refactor with an equivalence test as its
  acceptance; it constrains the tidying to preserve the sampling order, the random streams, the
  scenario constants and the arithmetic; model checking and the experiment ledger are added around
  the unchanged evaluation.
- *New generation beside the old:* the tidy-up may improve the model (for example move the slew
  physics or the feasibility flags into the model, or re-derive constants from first principles);
  the old CSVs stay frozen and every record keeps citing them; the paper's case re-runs on `v2`
  only if the supervisor decides so at WP10's gate, with the numbers that change listed. More
  freedom, one later decision.

**Decided (2026-11-08).** Driver's question: reproduce the committed data / new generation beside
the old / decide at the gate. **Supervisor (mzargham), verbatim:** "do it in parallel to start but
eventually i'd like to be able to swap over onto the new data". So: the second option. The
originals stay frozen and cited; the tidied model writes a `v2` generation beside them under the
experiment ledger; the swap of the paper's case (and the records that depend on it) onto `v2` is a
recorded gate of its own, after WP15's acceptance, with every number that changes listed.

## Proposed package: WP15 System model tidy-up (the example as a readable SysML v2 model with an experiment ledger)

Goals, as the driver reads the request:

- G1. One clean SysML v2 model of the cubesat configuration space in which the design variables,
  the alternatives, the accounting (`calc def`), the feasibility (`constraint def`, `requirement
  def` with `satisfy`), and the experiment (`analysis def`, `verification def`) are native and
  named, so that a reader of the `.sysml` file sees the whole example; the WP4 geostationary
  variant either folded into the same model as a second scenario or retired to the record.
- G2. The simulation machinery and model checking native to SysML v2 used where the toolkit
  supports them (opensysml `verify_constraint`, `verify_satisfaction`, `run_analysis`,
  `run_sweep`; the sysml-toolkit `check`, `lint`, `verify --solve` for universal constraint
  claims; `list_engines()` is authoritative at the pinned version), with Python holding only what
  SysML cannot do (the ODE integration of the slew), called from the model's analysis.
- G3. A Python scripting extension for scoping and ledgering experiments with cadCAD-like
  semantics: an experiment is a declared object (the model and its version, the scenario, the
  sampled space, the seeds, the number of runs and timesteps, the state-update and measurement
  functions, the policies if any), executed by a runner that writes a ledger entry (inputs,
  hashes of model and code, the outputs' path and hash, the environment) so every dataset in
  `examples/adcs/data/` is traceable to an experiment record; `generate_dataset.py` and
  `make_check_designs.py` become experiments in that ledger.
- G4. Interpretability for cross-application: a reader with another SysML v2 model can see which
  parts are the method's contract (configuration → attributes), which are this example's physics,
  and how to plug their model into the same experiment runner; a short how-to page.
- G5. No disruption: the seam holds (the decision above); the method, the paper and the records
  are untouched; the equivalence or the `v2` generation is tested.

Breakout into parts that can be worked in parallel (one PM, bounded implementers, disjoint files):

| Part | Files owned | Depends on | Parallel with |
|---|---|---|---|
| 15.1 Model restructure | `examples/adcs/cubesat_tradespace.sysml` (+ a new `scenarios` section or file), retirement or folding of `extended_design_space.sysml` | the seam decision | 15.3 (reads the model only through the client API) |
| 15.2 Model checking | the model's `requirement def`s and `verification def`s; `tests/test_cubesat_model.py` additions; a `sysmlv2 check/lint` step in CI if the toolkit is pinned | 15.1 | 15.3 |
| 15.3 Experiment runner and ledger | new `examples/adcs/experiments/` (runner, ledger schema, experiment definitions for the three datasets and the check designs), `generate_dataset.py` and `make_check_designs.py` thinned to experiment definitions | the seam decision; `cubesat_model.measure`'s signature (pinned by WP14) | 15.1, 15.2 |
| 15.4 Equivalence or v2 | regeneration under the ledger; equivalence tests against the committed CSVs (reproduce) or the `v2` files beside the old (new generation) | 15.1–15.3 | — (last) |
| 15.5 The how-to page | `docs/case-model.md` (or a section of the docsite): the model, the ledger, how to plug in another SysML model | 15.1–15.3 | WP8a renders it |

Parallel safety against the other packages: WP15 owns `examples/adcs/` except `k_terms.py`
(WP9's record script, frozen) and `data/` (frozen under "reproduce"; append-only under "v2");
WP10 owns `paper/`, `examples/adcs/case.py` (reads CSVs only) and `tests/test_paper.py`; WP13 owns
`src/`, `derivation/`, `docs/method.md` and the method notes; WP8a owns `scripts/`, `mkdocs.yml`,
`site/`, the workflow; WP14 owns the contract and its test. No file is owned by two packages. WP12
(the search) consumes 15.3's oracle and runner and therefore follows WP15, or runs against the
pinned `measure` signature if it starts first.

Open decisions the scope must put to the supervisor (problem-level): (1) the seam decision above
(reproduce versus a new generation); (2) whether the WP4 geostationary variant is folded into the
model as a second scenario or retired to the record (it is cited by WP4's tests and the WP4 data);
(3) whether the slew physics stays in Python called from the model's analysis (the toolkit cannot
integrate ODEs) or is approximated inside SysML as a closed-form `calc def` for model-checking
purposes with the ODE kept as the measurement of record; (4) whether the sysml-toolkit (Rust) is
pinned as a dev dependency for `check`/`lint`/`verify --solve` in CI or stays optional.

Defaults the scope can propose: opensysml pinned at its current locked version and re-checked
against `list_engines()`; the ledger as JSON Lines under `examples/adcs/experiments/ledger/` with one
entry per run, hashed; cadCAD vocabulary (state, policy, state-update block, timestep, run,
sweep) used only where it fits the configure → measure flow, said once; experiment definitions as
Python dataclasses next to the model; the equivalence test at the WP4 Amendment 1 tolerances; no
change to `adcs_sim.py`'s numerics under "reproduce".

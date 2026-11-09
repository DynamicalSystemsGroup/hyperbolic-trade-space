# WP15 — Scope of work: System model tidy-up (the cubesat example as a legible SysML v2 model with an experiment ledger)

| | |
|---|---|
| **Status** | DRAFT. Approved only by the recorded act below. Nothing in this package is executed before then. |
| **Supervisor (accountable)** | mzargham |
| **Repository** | `DynamicalSystemsGroup/hyperbolic-trade-space` (local: `/Users/z/Documents/GitHub/posynomial-invariant-form`); work on `dev`, merged to `main` at acceptance |
| **Approval record** | Verbal approval in chat, quoted verbatim in `work-packages/WP15-decisions.md` |
| **Acceptance record** | Verbal acceptance in chat, quoted verbatim in `work-packages/WP15-decisions.md`, after `work-packages/WP15-review.md` |

Drafted 2026-11-08 from `docs/superpowers/notes/system-model-tidy.md` (the driver's breakout, seams and
parallel-safety analysis), the roadmap in `work-packages/README.md`, the WP4 and WP4b records, the
opensysml notes, the toaster repository's use of the toolkit, and the WP14 draft (the interface
contract). The state of the example is as read on `dev` at `f0f5279`.

## Purpose

The supervisor, 2026-11-08, verbatim: "another round of tightening revisions i'd like to do is focused
on the system model. it got built up a bit ad hoc and its under utilizing the sysml toolkit. the
example was accreted and thus may seem a bit illegible and opaque. tightening it up to make better use
of the simulation machinery and model checking capabilities native to sysmlv2 models would make the
example more interpretable. strictly speaking our method needs to work for a black box that maps
configurations to attributes but a clean sysmlv2 model here with python scripting extensions for
scoping and ledgering experiments (with cadcad like semantics) would make it much more interpretable
for someone interested in cross applying to other sysml models. can you scope this as a tidying work
package and identify how to break it out so it can be worked in parallel without disruption".

On the seam, the supervisor, verbatim: "do it in parallel to start but eventually i'd like to be able
to swap over onto the new data". So the committed datasets stay frozen and cited; the tidied model and
an experiment runner write a `v2` generation beside them under a ledger; the swap of the paper's case
and the records onto `v2` is a separate recorded gate after this package's acceptance.

Today the example is four generations of accretion (WP4, WP4b, WP7, WP9): two SysML files of different
ambition, the slew physics and half the feasibility flags in Python, scenario numbers in module
constants and CLI flags, the experiment protocol (seed, workers, gain box) in `generate_dataset.py`
flags, and no record tying a CSV to the run that made it. This package makes the example one model a
reader can follow, uses the SysML v2 runtime's model checking and simulation machinery where it
supports them, and adds a small Python experiment layer (declared experiments, a runner, an append-only
ledger) so that every dataset is traceable and another SysML model can be plugged into the same layer.
The method itself is unchanged: stage 1 remains a black box configuration to attributes.

## Goals

- G1. **One legible model.** A single SysML v2 file in which a reader sees the whole example in reading
  order: the configuration space (design variables, alternatives, ranges), the cubesat, the accounting
  (`calc def`), the scenarios, the feasibility as named requirements, and the experiment as an
  `analysis def` with `verification def`s.
- G2. **The toolkit's machinery, used where it supports it.** Model checking (`self_check`,
  `verify_constraint`, `verify_requirement`, `verify_satisfaction`, claims over the whole space where an
  engine reaches them, the static checks of the toolkit per OD3) and simulation (`run_analysis`,
  `run_sweep`) used for what they do; Python holds only what SysML cannot do (the ODE integration of the
  slew, per OD2). A written account of what the toolkit offers, what was used and what was not, and why.
- G3. **Experiments declared and ledgered, with cadCAD-like semantics.** An experiment is a declared
  object (model and its hash, scenario, sampled space, seed, count, measurement, outputs); a runner
  executes it and appends a hashed ledger entry; every dataset in `examples/adcs/data/`, frozen and `v2`,
  is traceable to an entry.
- G4. **Cross-application.** A reader with another SysML v2 model can tell which part is the method's
  contract (configuration to attributes), which is this example's physics, and how to plug their model
  into the same runner: a how-to, proved by a toy model run through the runner in a test.
- G5. **No disruption.** The seam holds: the frozen CSVs, the records, the paper, WP13's and WP10's files
  and the tests that pin the frozen data are untouched; `v2` lands beside, with a comparison report of
  what changed between the generations and why.

## Non-goals

- **No swap.** The paper's case, `examples/adcs/case.py` (WP10), `k_terms.py` (WP13), the notebook, the
  records and every test that reads the frozen CSVs stay on the frozen data. The swap is a follow-up
  item (below), a recorded gate of its own.
- **No edit to the frozen data** (`examples/adcs/data/*.csv`) or to the figures, the notebook, `k_terms.py`
  or `case.py`.
- **No change to the method**: nothing in `src/`, `derivation/`, `docs/*.md`, `paper/`, `scripts/`,
  `.github/`, or WP13's notes. The estimator's public names are used read-only, at the names WP14 pins.
- **No change to `adcs_sim.py`'s numerics** (the unchanged ODE simulator is the measurement of record).
- **No new physics or recalibration** beyond what OD4 permits; no new design variables or attributes.
- **No CI workflow edit** (WP8a owns the workflow); model checks run in the default `uv run pytest`.
- **No new bibliography entries**; no site, MkDocs or navigation work (WP8a); no `docs/` page (the how-to
  lives in WP15's own tree, see Agent's defaults).
- **No FMI or external-tool integration** (the runtime lists a `tool:fmi` engine, not ready at 0.12.1 here).
- **No search or oracle noise model** (WP12); WP15 provides the deterministic oracle it will call.
- **No fix of the generator's run-to-run nondeterminism** (a recorded WP4b follow-up candidate); the
  runner records the platform and library versions so the effect is visible, and the WP4b tolerances apply.

## Deliverables

| ID | Deliverable | Serves |
|---|---|---|
| D-1 | `examples/adcs/model_v2/cubesat.sysml` *(default)*: the single model file (15.1, 15.2) | G1, G2 |
| D-2 | `examples/adcs/experiments/`: `oracle.py`, `experiment.py`, `ledger.py`, `runner.py`, `definitions.py`, `compare.py`, `__init__.py`, `__main__.py` *(default names)*; `ledger/ledger.jsonl` (append-only) (15.3) | G3, G4 |
| D-3 | `examples/adcs/data/v2/` *(default)*: the `v2` generation, same file names and column order as the frozen files (15.4) | G3, G5 |
| D-4 | `examples/adcs/experiments/reports/v1-v2-comparison.md` *(default)*: generated tables plus the change register (what changed, why) (15.4) | G5 |
| D-5 | `examples/adcs/case-model.md` *(default)*: the how-to and the toolkit account (15.5) | G2, G4 |
| D-6 | Tests: `tests/test_system_model_v2.py`, `tests/test_model_checking_v2.py`, `tests/test_experiments.py`, `tests/test_v2_data.py`, `tests/test_case_model_howto.py` *(default names)* | G1 to G5 |
| D-7 | Additive rows in WP14's manifest for the new paths (floor rule, WP14 R-8), if WP14 is accepted by then; `work-packages/WP15-decisions.md`; at the gate `WP15-review.md`; status rows in `work-packages/README.md` | G5 |
| D-8 | Under OD3 option (a) only: the toolkit pin file and its provisioning helper inside `examples/adcs/experiments/` and the `case` group edit in `pyproject.toml`/`uv.lock` | G2 |

## Parts, file ownership and parallel safety

Execution is by the PM with bounded implementers on disjoint files. WP15 owns `examples/adcs/` except
`k_terms.py` (WP13), `case.py` (WP10, if it exists) and the frozen `data/*.csv`; `data/v2/` is a new
subtree owned by WP15. Other packages own: WP13 `src/`, `derivation/`, `docs/*.md`, the method notes,
`k_terms.py`; WP10 `paper/`, `case.py`, `tests/test_paper.py`; WP8a `scripts/`, `mkdocs.yml`, `site/`, the
workflow; WP14 the contract document, manifest and its test. No path below is owned by two packages.
Start condition for the whole package: approval recorded and WP14 accepted (the README dependency).

| Part | Files owned | Depends on | Parallel with WP13, WP10, WP8a | Must wait |
|---|---|---|---|---|
| 15.1 Model restructure | `model_v2/cubesat.sysml` (skeleton, configuration space, accounting, scenarios, analysis, baseline; marked regions left for 15.2); `tests/test_system_model_v2.py` | the seam decision (made); OD1, OD2, OD4 | fully: text file and its test, reads nothing of theirs | OD1 and OD2 answers before the scenario and analysis regions are final |
| 15.2 Model checking | the requirement, `satisfy` and `verification def` region of the same file; `tests/test_model_checking_v2.py`; OD3 pin files if chosen | 15.1 (same file, so sequential, not concurrent) | fully; the only shared file touched is `pyproject.toml`/`uv.lock` and only under OD3 (a), `case` group lines only, after reading `git diff` for concurrent edits by WP13 | OD3 answer; 15.1's skeleton |
| 15.3 Runner and ledger | `experiments/` (all but `compare.py`), `tests/test_experiments.py` | the oracle signature (below); WP14's manifest format | fully: develops against `cubesat_model.measure` (the frozen oracle) and a toy model fixture, and plugs the v2 model in when 15.1 lands | the v2 oracle waits for 15.1; ledger entries for `v2` wait for 15.4 |
| 15.4 `v2` generation and comparison | `data/v2/`, `ledger/` entries, `experiments/compare.py`, `experiments/reports/`, `tests/test_v2_data.py` | 15.1, 15.2, 15.3 | yes: writes only new paths; long runs (minutes) are the only load | all of 15.1 to 15.3; the richness section of the report uses only estimator names WP14 pins, so a WP13 rename surfaces as a contract amendment, not a silent break |
| 15.5 How-to | `case-model.md`, `tests/test_case_model_howto.py` | 15.1 to 15.3 (drafts alongside, completes last) | yes | a copy or link into `docs/` and the site navigation belong to the owners of `docs/` and `mkdocs.yml` (follow-up item) |

Parallel safety, in one sentence per neighbour. **WP13**: no shared file; WP15 reads `src/` through
the import names WP14 pins. **WP10**: no shared file; `case.py` reads the frozen CSVs and keeps doing so.
**WP8a**: no shared file; nothing here needs a workflow or site edit. **WP14**: WP15 appends manifest rows
for new paths and nothing else (see "Reconciliation with the WP14 draft"). **WP12**: follows WP15, or
runs against the frozen `cubesat_model.measure` if it starts first.

## The oracle signature (stated for WP14's contract)

The callable interface between the model and the analysis. The WP14 draft (R-3) pins module and
function names and the committed files but no oracle signature; this section states it so WP14 can
adopt it by an additive amendment (WP14 R-8) when WP15 is accepted. Until then the frozen pair
`cubesat_model.measure(configuration, model=None, **kw)` and `cubesat_model.sample_designs(n, seed,
model=None)` is the pinned oracle and is not changed by this package under OD5 option (a).

```python
class Oracle(Protocol):
    config_names: tuple[
        str, ...
    ]  # ("panel_span_m", "battery_wh", "wheel_class", "st_grade", "Kp", "Kd")
    attribute_names: tuple[str, ...]  # the ten attributes of the cubesat case, as in the frozen CSV
    flag_names: tuple[str, ...]  # ("settled", "momentum_ok", "power_ok", "dod_ok")

    def __call__(self, configuration: Mapping[str, float | str]) -> dict[str, float | bool]: ...
    def evaluate(
        self, designs: pandas.DataFrame
    ) -> pandas.DataFrame: ...  # batch, rows in design_id order
```

Semantics: deterministic (no noise; WP12 wraps it); one configuration in, a mapping out whose keys are
the frozen `measure` keys (attributes, flags and the auxiliary columns), values `float` or `bool`;
the scenario (slew angle, horizon, step, bands) and the gain box are fixed when the oracle is
constructed, not per call (the frozen `measure` takes `t_end`, `max_step`, `slew_deg` per call; that
difference is the one change of signature and is the reason both stay pinned); a configuration outside
the model's ranges or with an unknown categorical value raises `ValueError` naming the variable;
construction fails with a named cause when the runtime cannot start (the existing
`OpenSysMLUnavailable` behaviour).

## Requirements

Paths are the defaults above. "Frozen" means `examples/adcs/data/*.csv` as committed.

| ID | Requirement | Checked by |
|---|---|---|
| R-1 | **One model, strict load.** `model_v2/cubesat.sysml` is one file and one package; it loads through opensysml with `strict=True`, no error diagnostics, and `self_check().status == "holds"`. It contains, in this order and with a section header and a `doc` comment each: configuration space (the two `enum def`s, abstract part defs with concrete alternatives carrying their attribute tables, the continuous ranges including both gain boxes as named parts); the cubesat composition; accounting `calc def`s for every accounting quantity the frozen `measure` reports; scenarios as named parts; requirements; analysis and verification; named configurations including the baseline. Illustrative-only header and a `doc` rationale beside each constant, as in the frozen model. | `tests/test_system_model_v2.py`: strict load, `self_check`, symbol kinds by query, section order by position of header comments; negative control: a broken copy fails the strict load |
| R-2 | **No constants in Python.** The enumerations, ranges, gain boxes, scenario numbers (slew angle, horizon, step, bands) and every accounting constant are read from the model; a grep of `experiments/` finds no copy; editing a range, an enum literal or a scenario value in a copy of the model changes the sampler's draws or the scenario the oracle uses. | the frozen R-4 tests re-expressed on `v2`: grep test and copy-edit test |
| R-3 | **Feasibility is native.** The four flags `settled`, `momentum_ok`, `power_ok`, `dod_ok` are produced by verifying named model requirements or constraints (`verify_requirement` or `verify_constraint`) on the measured quantities; no inequality on these quantities remains in Python. Each has a negative control (a deliberately infeasible configuration gives `False`). | test: flags equal an independent Python evaluation of the same inequalities on a sample of 20; grep for the comparison operators in `oracle.py`; negative-control test per flag |
| R-4 | **Satisfaction and verification.** `satisfy` statements tie the requirements to the baseline configuration; `verify_satisfaction` holds on it and fails on a deliberately infeasible part; `verification def`s name which requirements each verifies. | `tests/test_model_checking_v2.py` |
| R-5 | **Claims over the whole space.** The model states a small number of claims about every in-range configuration *(default: at least two, chosen by the implementer from the model's own accounting, for example the mass-accounting identity and the monotonicity of available power in panel span)*, each checked by an engine that answers `holds` (opensysml `smt` or `solve`, or the toolkit CLI per OD3), with the verdict recorded; a claim no engine reaches is recorded with the reason and is not silently skipped. | test: verdicts per claim; the test fails with the claim name when an engine disagrees |
| R-6 | **Static checks.** `self_check` passes on `v2`; the toolkit's `check` and `lint` are run per OD3. | per the OD3 answer: test (a), documented command and a test that runs when the binary is found (b), none (c) |
| R-7 | **Analysis and sweep.** The model's `analysis def` takes the design variables (as `in` parameters or a `Cubesat` subject) and the measured slew quantities, and returns the attributes and flags; `run_analysis` on a configuration plus the Python measurement equals the oracle's output; `run_sweep` over a design variable reproduces the Python-side accounting on a grid (the frozen sweep test, re-expressed). Whether the slew enters as a measurement handed in, or also as a closed-form calc, follows OD2. | `tests/test_model_checking_v2.py` |
| R-8 | **Toolkit account.** The how-to has a table of the runtime and CLI capabilities (at least `verify_constraint`, `verify_requirement`, `verify_satisfaction`, `run_analysis`, `run_sweep`, `record_run`, `run_runs`, the engines from `list_engines()`, and the CLI's `check`, `lint`, `verify --solve`) with used, not used, and why, each row checked against the pinned version by a small probe whose result is recorded. | inspection against `list_engines()` and the probe notes; test that the engine names listed in the table exist in `list_engines()` |
| R-9 | **Oracle.** `experiments/oracle.py` defines `Oracle` as in the section above and `CubesatOracle`, whose output keys equal the keys of the frozen `cubesat_model.measure` for the same configuration, in the frozen CSV column order via `evaluate`. | test: key-set and order equality against `measure` on 3 configurations; `ValueError` on an out-of-range value |
| R-10 | **Experiments and ledger.** An `Experiment` declares: id, model path and hash, scenario name, gain box, count, seed, oracle, output path, and optionally a `sweep` over scenario or gain box (each cell its own run and entry). The runner executes it and appends one JSON line: id, kind (`generated` or `adopted`), UTC time, git commit and dirty flag, sha256 of the model text, the code files that determine the output, the output file and its row count, the opensysml and runtime versions and the engine list, Python/numpy/scipy/pandas versions, platform, the inputs, and parent entries (a `generated` entry whose input is another entry's output records that entry's hash before it runs). `verify` recomputes every hash and reports drift. | `tests/test_experiments.py`: a small experiment (`n = 4`, fast step) in a temporary directory produces an entry with every field; editing the output or the model makes `verify` fail naming the entry |
| R-11 | **Every dataset is traceable.** Each file in `data/` (the five frozen) has an `adopted` entry recording its sha256, the command that made it (from the frozen tests' command strings), the generating commit, and the tolerances of its reproducibility tests; each file in `data/v2/` has a `generated` entry. The frozen files are not rewritten. | test enumerates both directories and requires an entry per file and equal hashes; `git diff <start>..HEAD -- examples/adcs/data/*.csv` is empty |
| R-12 | **cadCAD-like semantics, said once.** The mapping (state = configuration and measurements; policy = the sampler; state-update block = configure, measure, account; run = one seeded design; sweep = scenario or gain-box cells; timestep only where a flow has one) is stated once in the how-to and in `experiment.py`'s docstring, with the places it does not fit. | inspection; the `sweep` expansion test in R-10 |
| R-13 | **`v2` generation.** `data/v2/` holds the cubesat primary (aggressive gains), the cubesat baseline gains, the check predictions and the check designs *(default; plus a geostationary file only under OD1 "fold")*, with the frozen files' column names and order, 1000 designs, seed 0 and the frozen scenario (30 degrees, 600 s, 0.5 s step) *(default)*, produced by ledger runs. The predictions file is committed, and its entry recorded, before the check-design simulation entry exists. | `tests/test_v2_data.py`: columns, row counts, ledger entries, entry order (predict before simulate) |
| R-14 | **`v2` is reproducible.** The first 20 designs of each `v2` file regenerate within the tolerances of the frozen aggressive-box reproducibility test *(default: rtol 1e-3, saturated fraction 10 percent, times within 0.5 s, categorical columns and flags equal)*; 40 designs regenerated twice on one platform are identical. | `tests/test_v2_data.py` (needs the runtime; fails with the named cause, never skips, under `REQUIRE_OPENSYSML=1`) |
| R-15 | **Comparison report, not a pin.** `v1-v2-comparison.md` is generated by `uv run python -m experiments compare` *(default)* and has: per dataset, the shared and differing columns, agreement of design ids, seeds, categorical values and flags, the maximum relative difference per column on shared design ids, quantiles and flag shares side by side; the list of frozen consumers (the swap checklist, from a grep); the WP4b richness conditions (a) to (e) evaluated on `v2` and reported without a pass requirement; and a hand-written **change register**, one row per deliberate or unavoidable difference: what, why, which columns and downstream numbers move. | `tests/test_v2_data.py`: every column or aggregate whose difference exceeds its reproducibility tolerance is covered by a register row, and every register row names a difference that exists; the test fails on an unexplained difference and on a stale row, and does not require equality |
| R-16 | **How-to.** `case-model.md` covers: the contract (configuration to attributes) versus this example's physics; reading the model top to bottom; running an experiment and reading the ledger; the cadCAD mapping; the toolkit table (R-8); and plugging in another SysML model, with a toy model of about thirty lines whose text in the how-to is extracted by the test and run through the runner and ledger with a stub measurement. | `tests/test_case_model_howto.py`; inspection |
| R-17 | **Nothing disrupted.** `git diff --stat <start>..HEAD` shows only WP15's paths, `work-packages/`, additive manifest rows, and (OD3 option a) `pyproject.toml`/`uv.lock` `case` lines; nothing under `src/`, `derivation/`, `docs/`, `paper/`, `scripts/`, `.github/`, `figures/`, the notebook, `k_terms.py`, `case.py`, or `data/*.csv`. Under OD5 option (a) also no change to `cubesat_model.py`, `generate_dataset.py`, `make_check_designs.py`, `design_space.py`, `adcs_sim.py`, `cubesat_tradespace.sysml`, `extended_design_space.sysml` or to the tests that pin them; every such test passes unchanged. | inspect `git diff --stat`; `uv run pytest` |
| R-18 | **Standard gates.** `REQUIRE_OPENSYSML=1 uv run pytest`, `uv run ruff check .`, `uv run ruff format --check .`, `uv lock --check` pass; commits prefixed "WP15: " and authored as Michael Zargham; no AI attribution lines (grep returns 0). | run the commands; `git log` grep |

## Follow-up items (not deliverables)

- **S-1. The swap gate.** After WP15's acceptance, scope a recorded gate that moves the paper's case and the
  dependent records onto `v2`: re-point `examples/adcs/case.py` (WP10) and the regime map in `k_terms.py`
  (WP13), the notebook and the tests that read the frozen CSVs; re-run the K = 1, 2, 3 record, the
  WP4b richness conditions and the check designs on `v2`; list every number that changes (starting from
  the comparison report's swap checklist); decide whether the frozen generation is kept as a cited
  `legacy/` generation; thin `generate_dataset.py` and `make_check_designs.py` to experiment definitions
  (if still present). `v2` keeps the frozen file names and column order so the re-pointing is a directory
  change. Decided by the supervisor at that gate, not here.
- **S-2.** Copy or link `case-model.md` into the docsite, and add `v2` and the oracle to WP14's manifest as
  pinned items (additive amendment), once those packages' owners are ready.
- **S-3.** A CI step for the toolkit (if OD3 option (a)) belongs to the owner of the workflow (WP8a).

## Reconciliation with the WP14 draft

Recorded here so neither package is surprised; WP14's file is not edited by this package.

- WP14 R-3 pins `generate_dataset.generate`, `generate_cubesat`, `main`; `design_space.sample_designs`,
  `evaluate_design`; `cubesat_model`, `adcs_sim`, `make_check_designs`; the two SysML files; and the five
  committed CSVs with their schemas. Under the defaults WP15 touches none of them. A different answer to
  OD1 ("retire") or OD5 option (b) removes or moves a pinned item and needs a WP14 amendment (WP14 R-8)
  with its own verbal approval, which this package lists as an acceptance item.
- WP14 does not pin an oracle signature; the README makes it a WP15 dependency on WP14. The signature
  above is offered for an additive amendment. If WP14 is accepted without it, WP15 proceeds against the
  pinned frozen names and proposes the clause at its own acceptance.
- The new paths (`model_v2/`, `experiments/`, `data/v2/`, `case-model.md`) are additions to the technical side's
  floor; WP15 appends the rows to WP14's manifest in the same commit as the files (WP14 R-8). This is the
  only edit WP15 makes to a WP14 file.
- WP14 R-6 lists the documentation pages the docsite reads; `case-model.md` is deliberately outside `docs/`
  (WP13 owns `docs/*.md`), so it is not in that list until S-2.
- WP14 R-7 gives the `dev` and `case` dependency groups to the technical side and the workflow to the
  presentation side; OD3 option (a) edits only the `case` group and adds no workflow step.

## Definition of good

- A reader who has never seen the example opens `model_v2/cubesat.sysml` and, reading top to bottom, can
  say what the design variables are, what each alternative is, how mass and power are accounted, what
  feasible means, and what the experiment measures, without opening Python; and, opening `case-model.md`,
  can name the three things they would replace to run their own SysML model through the same runner.
- Every number in `data/` can be walked back to a ledger entry, the model text and code that made it, and
  the command to remake it.
- The comparison report reads as an explanation, so the supervisor can decide the swap by reading it.
- The toolkit is used for what it is good at, and the account is honest about what was not used and why.
- The runner is small enough to read in one sitting and generic enough that the toy model needs no change to it.

## Definition of good enough

- D-1 to D-8 exist at the stated paths (D-8 only under OD3 option (a)).
- R-1 to R-18 are each met with their stated check; `REQUIRE_OPENSYSML=1 uv run pytest` passes, with the
  existing suite unchanged and green.
- Every `data/` file has a ledger entry and `verify` passes; the change register covers every difference above
  tolerance.
- The five OD answers are recorded and reflected in the model, the runner and the how-to.
- Non-goals untouched: R-17 shows no edit outside WP15's paths.

## Definition of done

Good enough is met, **no open item remains unresolved**, and the supervisor has accepted the work by the acceptance record above.

## Agent's defaults

The supervisor approves or changes this list as one item. Each is marked *(default)* where it appears.

- Model location and shape *(default)*: one file `examples/adcs/model_v2/cubesat.sysml`, one package
  `CubesatTradeSpaceV2`, because the runtime cannot import across separately loaded files (opensysml-usage
  note); scenarios, gain boxes and requirements are sections of that file. Appears in D-1, R-1.
- Experiment layer location and names *(default)*: `examples/adcs/experiments/` with the files listed in D-2,
  importable as `experiments` through the existing `examples/adcs` entry of `pythonpath`; ledger at
  `experiments/ledger/ledger.jsonl`, append-only, one hashed JSON line per run. Appears in D-2, R-10.
- `v2` data location *(default)*: `examples/adcs/data/v2/` with the frozen file names and column order, so the
  later swap is a directory change; provenance lives in the ledger, not in an added column. Appears in D-3, R-13.
- Which files get a `v2` *(default)*: primary, baseline gains, check predictions, check designs; the check
  designs are re-proposed from the `v2` primary data (predict, then simulate, ledger order enforced) and the
  report states whether they coincide with the frozen proposals. Appears in R-13.
- Scenario and sample *(default)*: 1000 designs, seed 0, 30 degrees, 600 s, step 0.5 s, per-design
  `SeedSequence` child seeds, log-uniform continuous variables and uniform categoricals; the sampler stays in
  Python reading ranges from the model (opensysml `run_sweep` with `samples` is probed and adopted only if
  it keeps design-i-independent-of-n and log ranges). Appears in R-2, R-13.
- Frozen entries *(default)*: the five frozen CSVs get `adopted` ledger entries from their recorded commands and
  generating commits (`7a175a4` primary, `a27502e` baseline, the WP4 and WP7 commits for the rest, read from
  `git log` at execution); they are not regenerated. Appears in R-11.
- Hashes *(default)*: sha256; output-file hashes are exact-match integrity checks of the committed file only;
  regeneration is judged by tolerances, because cross-platform ODE output is not bit-reproducible (WP4
  Amendment 1). Appears in R-10, R-14.
- Reproducibility tolerances for `v2` *(default)*: those of the frozen aggressive-box test. Appears in R-14.
- The ledger is the Python JSONL file the supervisor asked for; the runtime's native `record_run`
  (AnalysisRecords written into a model) is probed and described in the toolkit account, not adopted as the
  ledger. Appears in R-8, R-10.
- cadCAD vocabulary *(default)*: used only where it fits configure to measure, said once, with the misfits
  (one-shot flow, no timesteps) named. Appears in R-12.
- The analysis hands measured slew quantities in as `in` parameters *(default)*: SysML cannot call Python, so
  the Python runner measures the slew and passes `torqueSquaredIntegral`, the peak torque, the settling time,
  the peak momentum and the censoring to the model's `analysis def`, which returns attributes and flags.
  Appears in R-3, R-7.
- Model-check claims *(default)*: at least two, chosen from the model's own accounting at execution. Appears in R-5.
- The richness conditions (WP4b a to e) are evaluated on `v2` and reported, without a pass requirement, using
  only estimator names WP14 pins. Appears in R-15.
- How-to location *(default)*: `examples/adcs/case-model.md`, outside `docs/`, because WP13 owns `docs/*.md`;
  the toy model is a test fixture whose text is shown in the how-to. Appears in D-5, R-16.
- Test names and the `REQUIRE_OPENSYSML` discipline *(default)*: as listed in D-6; tests that need the runtime
  fail with the named cause, never skip, as in the frozen suite. Appears in D-6, R-14.
- Order inside WP15 *(default)*: 15.1 skeleton, then 15.3 (parallel), then 15.2, then 15.4, 15.5 last; commits
  prefixed "WP15: " on `dev`, merged to `main` at acceptance with `git merge --no-ff dev`. Appears in the parts table.
- Toolkit probe first *(default)*: the first task of 15.2 is a recorded probe of what `smt`, `solve`,
  `verify_requirement`, `record_run`, `run_runs` and (if present) the CLI do at the pinned version, because the
  notes were verified at 0.9.0 and 0.12.1 added capabilities; the probe fixes the claims in R-5. Appears in R-5, R-8.
- opensysml *(default)*: stays at the locked 0.12.1 (the `case` group requires `>=0.12.1`), re-checked against
  `list_engines()` at execution; no change to `uv.lock` unless OD3 option (a). Appears in R-1.

## Open decisions (for the supervisor)

Each is problem-level: it changes what is delivered, what may differ, or how acceptance is judged. The
seam decision is not among them (made 2026-11-08; quoted in Purpose).

- **OD1.** The WP4 geostationary variant (10 degree slew, four attributes, `design_space.py`,
  `extended_design_space.sysml`, `adcs_designs.csv`, cited by WP4's tests and the WP4 data): what happens to it in
  the tidy model? Options: (a) fold it into the model as a second scenario with its hardware tables, and
  generate a `v2` geostationary file under the ledger (the model is longer, one model covers both generations;
  the frozen data and WP4 tests stay as they are); (b) retire it to the record: `v2` does not model it, the
  frozen file, its tests and the WP4 modules stay as they are and are cited as history (the model is shorter
  and covers the cubesat only; if the two WP14-pinned files are later moved, that is an amendment).
- **OD2.** The slew physics. Options: (a) Python only: the ODE (`adcs_sim.simulate_adcs`, unchanged) is the
  one slew model; the runner calls it and hands the measured quantities to the model's analysis; the model
  has no slew calculation of its own; (b) Python plus a closed-form slew approximation as a `calc def` in
  the model, kept for model checking (claims over the whole space about slew time, torque-limited and
  linear regimes), with the ODE the measurement of record and a reported comparison of the two on a sample
  (a second slew model to maintain and explain; the model checks can then say something about agility).
- **OD3.** The sysml-toolkit (Rust CLI: `check`, `lint`, `verify --solve`; not on PyPI; toaster pins v0.9.1
  with per-platform sha256 and Z3). Options: (a) pinned: a pin file with checksums and a provisioning helper
  inside `examples/adcs/experiments/`, its checks run in the default test suite and fail if the binary is
  missing under the same discipline as opensysml (edits the `case` group; CI downloads the binary on first
  use; the CI workflow step is a follow-up for its owner); (b) optional: documented commands, and a test that
  runs the checks when the binary is found and says so when it is not (no new dependency, no CI download);
  (c) not used: model checking by opensysml only (`self_check`, the `smt` and `solve` engines), with the
  toolkit named in the how-to as an option for readers.
- **OD4.** How far may `v2` depart from the frozen generation? Options: (a) structure only: the physics,
  constants, scenario and attribute definitions are as in the frozen model, and `v2` differs only through
  numerics, sampling mechanics, and where the tidy moves a calculation (the report is expected to show small,
  explained differences, and the swap would change the paper's numbers little); (b) structure plus named
  corrections: where the tidy exposes an inconsistency or a constant that is better derived, the change is
  made and entered in the change register with its reason, and the supervisor accepts or rejects each
  register row at acceptance (the swap could change the paper's numbers visibly, each listed); (c) a
  redesign of the case is allowed (new constants, new couplings, new attributes), reviewed as a new case
  (largest freedom; the richness conditions, the fits and the check designs would need re-establishing before
  a swap).
- **OD5.** What happens to the frozen model and generator code (`cubesat_model.py`, `cubesat_tradespace.sysml`,
  `generate_dataset.py`, `make_check_designs.py`, `design_space.py`, `extended_design_space.sysml` and the tests
  that regenerate the frozen CSVs through them) when WP15 is accepted? Options: (a) they stay exactly as they
  are, beside the new files, until the swap gate (two models are in the directory for now and the how-to says
  which is which; the frozen reproducibility tests keep running; no WP14-pinned item changes); (b) they are
  archived under `examples/adcs/legacy/` at acceptance with shims keeping the WP14-pinned names importable,
  the reproducibility tests for the frozen CSVs are replaced by the ledger's `adopted` entries and the
  comparison report, and the data's generating commits are recorded in the ledger (one model in the directory;
  the frozen data is no longer regenerable from the code at `HEAD`; a WP14 amendment and several test edits
  are part of this package).

Unresolved before the gate: OD1, OD2, OD3, OD4, OD5, and the Agent's defaults list as one item.

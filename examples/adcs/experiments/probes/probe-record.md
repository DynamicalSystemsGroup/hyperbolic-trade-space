# Probe record: what the SysML runtime and the model-checking toolkit do

Observed at opensysml 0.12.1 (runtime `v0.12.1`) / toolkit v0.12.0 on darwin-arm64 (z3 on `PATH`),
2026-11-08, against the live runtime. Eleven probes, each a function in `../probes.py`; `run_all()`
re-runs them and compares each observed fact set with the recorded one (`EXPECTED` at the top of the
file), so a changed behaviour of the runtime or the toolkit fails by probe name. The pitfalls of
`work-packages/build-notes/opensysml-usage.md` were found at 0.9.0; each is re-checked below.

Run: `uv run python examples/adcs/experiments/probes.py [--write] [--network] [--facts]`.
`--write` rewrites the generated table; `--network` also compares probe 11 with the published release;
`--facts` prints the observed fact sets.

<!-- probes:begin -->
| probe | recorded result holds | observation |
|---|---|---|
| `cross_source_import` | yes | observed at opensysml 0.12.1 / toolkit v0.12.0 on darwin-arm64: an import across separately loaded sources resolves only through parse_sources (paths or named inline documents, any order); load and load_from_content see one source; concatenation still works; every import needs an explicit visibility. |
| `false_assert_satisfy` | yes | observed at opensysml 0.12.1 / toolkit v0.12.0 on darwin-arm64: a false assert satisfy loads with no diagnostic, also under strict=True; only verify_satisfaction (holds False, strength witnessed) and satisfied() (False) show it. |
| `satisfy_target_kinds` | yes | observed at opensysml 0.12.1 / toolkit v0.12.0 on darwin-arm64: satisfy accepts a requirement usage (named, or declared inline) and refuses a requirement definition and a part usage as target ('satisfy target must be a requirement usage'); verify_requirement takes a requirement definition with a subject. |
| `verify_requirement_satisfaction` | yes | observed at opensysml 0.12.1 / toolkit v0.12.0 on darwin-arm64: on the frozen baseline (13.2914 kg) a 20 kg mass-budget requirement holds (engine run, strength observed) and a 5 kg control is violated (witnessed); verify_satisfaction returns one verdict per satisfy and assert satisfy; an in-parameter takes a Quantity from eval, a plain number is refused as a type mismatch; the model's own constraint usages evaluate per configuration (slew energy 0.5 Wh passes, 50 Wh fails). |
| `holds_and_exclusion` | yes | observed at opensysml 0.12.1 / toolkit v0.12.0 on darwin-arm64: holds on a claim that invokes a calc def is undecided on every engine ('invocation not translatable'); the smt engine answers no constraint claim (it answers schedules); the solve engine (needs z3) proves claims restated over scalar features (strength proved, witness when violated), including range-bounded ones; a region of the design space or a model variant is excluded before simulation when the conjunction of its range and the feasibility condition is unsatisfiable (proved); the battery and slew-momentum regions classify as exclude, all_feasible and mixed. |
| `analysis_and_sweep` | yes | observed at opensysml 0.12.1 / toolkit v0.12.0 on darwin-arm64: run_analysis binds in parameters by name or position and fails on a missing one; run_sweep grids are inclusive with a step and first-range-slowest; samples+seed is reproducible, row i does not depend on n, and the draw is uniform (no log range, so a log range is drawn through an exponent parameter); a range cannot bind a quantity-typed parameter, so the case takes a dimensionless parameter and applies the unit inside. |
| `record_and_runs` | yes | observed at opensysml 0.12.1 / toolkit v0.12.0 on darwin-arm64: record_run returns the runs as a new Records document (Records::Cost_run1; one part per sweep row) and leaves the loaded model unchanged, so numbering continues only when the recorded document is loaded with the model through parse_sources (Cost_run2); each record is stamped with runAt (a wall-clock time: a ledger comparison must ignore it) and the tool version; run_runs repeats an action with modeled randomness, reproducibly per seed with run i independent of the count, and takes an analysis case only if it specializes Simulation::MonteCarlo. |
| `unit_labels` | yes | observed at opensysml 0.12.1 / toolkit v0.12.0 on darwin-arm64: a value of a plain unit keeps its label (kg), a product or quotient comes back with the unsimplified base-unit label (kg*m^2*s^-3 for a power), the magnitude is right, and in_unit converts to the unit the analyst names. |
| `query_blind_spots` | yes | observed at opensysml 0.12.1 / toolkit v0.12.0 on darwin-arm64: at 0.12.1 query sees the unnamed satisfy and connection usages (ids Q::@n) and to_api_json loads and serializes a package with duplicate-name and doubly redefined members; to_api_json raises ExperimentalFeatureWarning, so the form is not a stable interface. |
| `engines` | yes | observed at opensysml 0.12.1 / toolkit v0.12.0 on darwin-arm64: list_engines reports check, explore, run, smt, solve and sweep ready and tool:fmi unavailable (OPENSYSML_FMI_RUNNER unset); smt and solve become not ready when no z3 or cvc5 is on PATH, so a solving step needs the solver installed and a test that needs it fails by name. |
| `toolkit` | yes | observed at opensysml 0.12.1 / toolkit v0.12.0 on darwin-arm64: v0.12.0 publishes prebuilt archives for seven targets (aarch64 and x86_64 apple-darwin, linux gnu and musl for both, x86_64 windows) with a SHA256SUMS asset and a sha256 digest on every asset; it is not on PyPI; check, lint --format json and verify --solve run from a source build in about a minute, need a standard-library directory (--lib) and z3 on PATH, and read usage-level assert constraints (see the record). |
<!-- probes:end -->

## Summary: what to rely on, what to avoid

| Capability | Rely on | Avoid |
|---|---|---|
| Loading | `load_from_content(text, strict=True)` for one source; `parse_sources([...], strict=True)` for several sources that import each other (any order, paths or named inline text); every `import` carries `private`, `public` or `protected` | `load` or `load_from_content` for a source that imports another file; trusting a clean load for the truth of an `assert satisfy` |
| Satisfaction | `satisfy` to a named or inline requirement usage; `verify_satisfaction()` (one verdict per assertion) and `satisfied()` | `satisfy` or `assert satisfy` to a requirement definition or a part usage (a load error) |
| Requirements | `verify_requirement(fqn, subject=...)` with a requirement usage or definition; `in` parameters as `named_arguments` of `Quantity` values built by `model.eval("20.0 [SI::kg]")`; a negative control per check | a plain number for a quantity-typed parameter (`undecided`, type mismatch); `in` redefinition inside a requirement usage (`Subject must be first parameter`): use `attribute limit : T default = v` and `attribute :>> limit = w` |
| Per-configuration feasibility | the model's own constraint usages evaluated with `subject=` (engine `run`, strength `observed`) | |
| Claims over a region | engine `solve` (needs `z3`), question `holds` and `satisfiable`, strength `proved` or `witnessed`, claims stated over scalar features | `holds` on a claim that invokes a `calc def` (undecided on every engine); the `smt` engine for constraints (it answers schedules); `Integer` and `Real`-typed features in products with quantities; arguments with `holds` (refused: ranges go into the source text) |
| Analysis | `run_analysis` with `named_arguments` or `arguments`; dimensionless `Real` parameters with the unit applied inside the case | a quantity-typed parameter in a sweep range (type mismatch) |
| Sweep | `run_sweep` grid `(start, stop, step)`, inclusive; `samples` + `seed` (reproducible, row `i` independent of `n`) | a log range (none exists: draw the exponent and exponentiate inside the case); relying on an omitted step |
| Records | `record_run` for a ledger-style run log in the model; `run_runs` for modeled randomness | expecting `record_run` to change the loaded model; byte-comparing records (they carry `runAt`); `run_runs` on an ordinary analysis case |
| Units | `Quantity.in_unit(model.eval("1.0 [SI::W*SI::h]").unit)` | reading `unit.text` as the unit the analyst expects |
| Reading the model | `query(scope=[pkg])` (it lists unnamed `satisfy` and connection usages as `Pkg::@n`) | `to_api_json()` as a stable interface (it warns `ExperimentalFeatureWarning`) |
| Engines | `list_engines()` names and readiness (`check`, `explore`, `run`, `smt`, `solve`, `sweep` ready; `tool:fmi` not) | assuming `smt` and `solve` are ready without `z3` or `cvc5` on `PATH` |
| Toolkit | prebuilt archives with published sha256 (probe 11); `check`, `lint --format json`, `verify --solve` with `--lib` | `verify --solve` on definitions with unbound parts (undecided); reading its verdicts as `holds` answers (it conjoins the asserts) |

## 1. Cross-source `import`

Finding, observed at opensysml 0.12.1 / toolkit v0.12.0 on darwin-arm64: an import across separately loaded
sources does not resolve through `load` or `load_from_content` (each sees one source: `unresolved reference:
A`). `Connection.parse_sources` resolves it, for file paths or named inline documents, in either order
(`model.documents` lists the names). Concatenating the texts and loading once still works. The pitfall of
0.9.0 ("concatenate sources and load once") is therefore obsolete for the multi-file case, and
concatenation is no longer required. A bare `import` is a load error at 0.12.1 (`import without a visibility
indicator`): write `private import`.

Evidence: facts `single_source_unresolved`, `load_of_one_file_unresolved`, `parse_sources_resolves`,
`parse_sources_order_free`, `concatenation_resolves`, `bare_import_is_error` in `EXPECTED`.

## 2. A false `assert satisfy`

Finding: unchanged from 0.9.0. A model whose `assert satisfy light by car` is false loads with zero
diagnostics, also under `strict=True`. The falsity shows only in `verify_satisfaction()` (verdict `holds` False,
strength `witnessed`, engine `run`) and `satisfied()` (False). An analysis that relies on a satisfaction
assertion calls one of these; the loader is not the check.

## 3. `satisfy` target kinds

Finding: `satisfy` accepts a requirement usage, named (`requirement light : Light; satisfy light by car;`) or
declared inline (`satisfy requirement own : Light by car;`). A requirement definition (`satisfy Light by car`)
and a part usage (`satisfy car by car`) are load errors: `satisfy target must be a requirement usage, found
requirementDef` (`partUsage`). `verify_requirement` accepts the definition with a `subject=`. The note's
first-probe finding holds at 0.12.1.

## 4. `verify_requirement` and `verify_satisfaction` on the cubesat

Finding: on the frozen model (baseline total mass 13.2914 kg) with requirements appended to its package in the
probe text:

- `verify_requirement(budgetOk, subject=cubesatBaseline)` (limit 20 kg) holds, engine `run`, strength
  `observed`; the negative control `budgetTight` (limit 5 kg) is violated, strength `witnessed`.
- `verify_satisfaction()` returns one verdict per `satisfy` and `assert satisfy` (here `[True, False]`).
- A requirement definition with `in limit : MassValue` takes `named_arguments={"limit": model.eval("5.0
  [SI::kg]")}`; a plain number is reported `undecided` with `type mismatch`. A second configuration (`heavySat`:
  panel span 1.0 m, 200 Wh, large wheels, fine tracker) verifies the same way.
- `in limit` redefined inside a requirement usage is a load error (`Subject must be first parameter`;
  `Redefining feature must have a compatible direction`); an attribute with `default =` redefined with `:>>`
  works.
- The model's own constraint usages (`Cubesat::powerOk`, `Cubesat::dodOk`) evaluate per configuration with
  `subject=`; `dodOk` takes `slewEnergy` as a `Quantity` (0.5 Wh holds, 50 Wh is violated). The constraint
  definitions called directly (`PowerOK`) are `undecided` (`unbound parameter c`): call the usage.

## 5. `holds` on `smt` and `solve`; exclusion before simulation

Findings:

- A claim that invokes a `calc def` (`MassAccounting(c) > 0 [kg]`) is `undecided` on `smt`, `solve`, `check`,
  `auto` and `all`, reason `invocation not translatable for solving: it is outside the subset`. The
  documented boundary: the solver translates arithmetic, comparisons, boolean operators, enumeration literals
  and scalar feature chains; invocations (calc usages included), `**`, quantifiers and collections are refused,
  and one refused conjunct refuses the whole claim. An undecided result is never proof.
- The `smt` engine answers no constraint claim: status `undecided`, strength `not covered`, reason `smt answers
  over every schedule; the question fixes reverse`. The `check` engine: `check cannot leave the inputs free`.
  `auto` and `all` route to `solve`.
- The `solve` engine answers `holds` and `satisfiable`. It needs `z3` (or `cvc5`) on `PATH`; without one the
  answer is `undecided`, `no SMT solver found`. Strength is `proved` for `holds` and `unsatisfiable`,
  `witnessed` for `violated` and `satisfiable` (a witness assignment in the runtime's gram-based base units: powers in mW, energies in mJ).
- Claims restated over scalar features are decided with strength `proved`: the mass-accounting identity (the
  total minus the structure mass equals panels plus antenna, built from the model's own `calc def` bodies
  extracted from its text), the monotonicity of generated power in panel span, the range-bounded bound
  `P(s) <= P(span max)` for `s` in the model's span range, and `AvailablePower > 0` over the whole span range
  and every tracker grade. Each has a negative control that returns `violated` with a witness.
- Requirements for a restated claim: constants are written as literals read from the model with `eval`
  (a `Real`-typed feature in a product with a quantity makes the product a plain number, `incommensurable
  units`; an `Integer` feature likewise; a `Real` parameter gives `not covered` because the evaluator's
  floating point is not proved to agree); `holds` and `satisfiable` take no arguments, so a range is part of
  the source text; the subject's declared values are not pinned (pins of held sequences fail: `a sequence has
  no literal in the term language`), so every value a claim needs is stated in it.

Recipe for exclusion before simulation (works at 0.12.1 with `z3`). A region (a sampler box, or a model variant
is a source text with its ranges as literals) is excluded when the conjunction of its range and the
feasibility condition is unsatisfiable; it needs no simulation when the implication holds. Per region write two
constraint definitions over scalar `in` parameters, the conjunction `<stem>Sat` and the implication
`<stem>Holds`, load the text, and ask `solve`:

| region | `Sat`, `satisfiable` | `Holds`, `holds` | classification |
|---|---|---|---|
| battery 20 to 26 Wh (eclipse base load, any slew energy) | `unsatisfiable`, proved | `violated`, witnessed | exclude: no feasible configuration |
| battery 29 to 200 Wh | `satisfiable`, witnessed | `holds`, proved | all feasible: nothing to exclude |
| battery 20 to 200 Wh | `satisfiable`, witnessed | `violated`, witnessed | mixed: keep, test per point |
| small wheel, inertia 0.70 to 0.90 kg m^2, 30 degree slew (`tau * theta * I <= h^2`) | `unsatisfiable`, proved | `violated`, witnessed | exclude |
| small wheel, inertia 0.18 to 0.60 | `satisfiable` | `holds`, proved | all feasible |
| small wheel, inertia 0.18 to 0.90 | `satisfiable` | `violated` | mixed |
| large wheel, inertia 0.18 to 0.90 | `satisfiable` | `holds`, proved | all feasible |

The thresholds agree with the arithmetic (battery 26.6 to 28.8 Wh for the coarse to fine tracker; small-wheel
inertia limit 0.6366 kg m^2), so the solver verdicts are cross-checked. The momentum condition is the
bang-bang peak momentum `sqrt(tau theta I)` against the wheel's `maxMomentum`, the closed form of OD2. Per
configuration (one design, no region) the cheaper filter is the model's constraint usage evaluated with
`subject=` (engine `run`). The ledger entry for an exclusion records the claim text, the engine, the status, the
strength and the witness. What does not work: a claim that calls `AvailablePower(c)` or any `calc def`
(restate the body over features, as the probe does), a claim whose subject's declared values must be pinned,
and any claim without `z3`.

The monotonicity of available power in panel span is the generated-power claim minus a constant load, proved
the same way; the frozen model does not state either claim, so the tidy model states its claims over features
(or restates them in a claims section) for `holds` to reach them.

## 6. `run_analysis` and `run_sweep`

Finding:

- `run_analysis(fqn, subject=..., named_arguments={...})` or `arguments=[...]` binds `in` parameters; the
  engine is `run`, strength `observed`. A missing parameter raises `ExecutionError` (`operator '*' is not
  defined for a Real and null`).
- `run_sweep` grid ranges `(start, stop, step)` are inclusive; several ranges give the Cartesian product, the
  first range varying slowest. A row's outputs are `{name: [value]}` (a `calc` returns under `result`).
- `samples=n, seed=s` draws uniformly from each `(lo, hi)` range: the same seed gives the same rows; row `i` of
  an `n = 6` sweep equals row `i` of an `n = 4` sweep (independence of `n`); another seed differs.
- There is no log range. A 400-sample draw from `(1, 1000)` puts 0.75 percent below 10; drawing an exponent in
  `(0, 3)` and exponentiating inside the case (`10.0 ** e`) puts about a third below 10.
- A range cannot bind a quantity-typed parameter (`type mismatch: cannot write 0.0 (a Real) to a feature typed
  by EnergyValue`). The case takes a dimensionless `Real` parameter and applies the unit inside
  (`wh * 1.0 [W*h]`).

## 7. `record_run` and `run_runs`

Finding: `record_run(fqn, subject=..., named_arguments=..., ranges=...)` returns a `Recording`: `definition`
(`Records::CostRun`), `records` (`['Records::Cost_run1']`; one per sweep row, kind `sweep`), `run` (the
`AnalysisResult`), `source` (the new `Records` package, with the inputs and outputs of each run and the metadata
`runAt` (wall-clock UTC), `tool` (`v0.12.1`), `command`, `kind`). The loaded model is not changed: a second call
returns `Cost_run1` again. Numbering continues when the recorded document is loaded with the model through
`parse_sources` (`Cost_run2`). `runAt` differs between runs, so a ledger hash over records excludes it.
`run_runs(action=..., runs=n, seed=s)` repeats an action with modeled randomness (`uniform`): the same seed
gives the same table, run `i` does not depend on `n`, another seed differs; the table rows carry `inputs
{'run': i}` and a `clock`. An analysis case is accepted only if it specializes `Simulation::MonteCarlo` (an
ordinary case is refused, `specializes no Simulation::MonteCarlo`). The sampler for designs is `run_sweep`;
`run_runs` is for the model's own randomness.

## 8. Unit labels from `eval`

Finding: a value of a plain unit keeps its label (`totalMass` 13.2914 `kg`); a product or quotient comes back
with the unsimplified base-unit label (`generatedPower` 48.9764 `SI::'kg⋅m²⋅s⁻³'`, `usableWheelTorque` `SI::'N⋅m'`).
The magnitude is right (12 W times 0.6 h is 25920 J = 7.2 Wh by `in_unit`). Convert with `Quantity.in_unit(unit)`,
the unit built by `model.eval("1.0 [SI::W*SI::h]").unit`; do not display `unit.text`. Unchanged from 0.9.0.

## 9. `query` and `to_api_json`

Finding: at 0.12.1 `query(scope=["Q"])` lists the unnamed `satisfy` usages (two) and the unnamed connection
usage under ids `Q::@n`; the 0.9.0 blind spot no longer exists. `to_api_json()` serializes a package that
declares duplicate-name members and a doubly redefined attribute (load warnings only, `Duplicate of ...`) and
lists the same usages, but it emits `ExperimentalFeatureWarning` (the RDF and API JSON mapping is experimental;
its vocabulary may change). The crash on redeclared members of 0.9.0 did not reproduce. A redefinition of a member
bound with `=` is a load error; `default =` on the original allows it.

## 10. Engines and readiness

Finding: `list_engines()` returns: `check` (bounded; answers `holds`, `outcomes`, `sensitive`), `explore`
(proved; `outcomes`), `run` (observed; `evaluate`), `smt` (proved; `holds`, `sensitive`), `solve` (proved;
`holds`, `satisfiable`), `sweep` (observed; `sweep`), all ready, and `tool:fmi` (observed; `compute`) not ready:
`OPENSYSML_FMI_RUNNER is not set`. With no `z3` or `cvc5` on `PATH`, `smt` and `solve` are not ready (a fresh
client with `z3` removed from `PATH` reports `smt False, solve False`). The `case` group installs opensysml, not
the solver: a test that needs `holds` fails by name when the solver is missing.

## 11. The model-checking toolkit v0.12.0

Findings:

- Prebuilt binaries are published (GitHub release `v0.12.0`, 2026-11-08T23:27:14Z). The toolkit is not on PyPI
  under this name. Recorded assets (size in bytes, sha256 published with each asset; not downloaded):

| asset | size | sha256 |
|---|---|---|
| `sysmlv2-0.12.0-aarch64-apple-darwin.tar.gz` | 5593394 | `d2a2208e8b9ffbd570176d6122bfabf494e3344e67f65b9a87e8889c56238195` |
| `sysmlv2-0.12.0-aarch64-unknown-linux-gnu.tar.gz` | 5905427 | `21b1dfad0ea82b0dd379a988276c91e07256ee1958af38fdb81e25ae0a3c724a` |
| `sysmlv2-0.12.0-aarch64-unknown-linux-musl.tar.gz` | 5844612 | `10f43f21a7899de1c8698797c11d05b1fdbe3bfeec48898e6c2555ffb514bf70` |
| `sysmlv2-0.12.0-x86_64-apple-darwin.tar.gz` | 6055486 | `2a89c4ef1bb33fd5bf5bcf3f7430f9a1f4029f1981480152e307709ffe4b41c8` |
| `sysmlv2-0.12.0-x86_64-pc-windows-msvc.zip` | 5972068 | `a9f0daca2cb7697447fc77e59d4eaded37a55fa195181e0d722794a8182c3971` |
| `sysmlv2-0.12.0-x86_64-unknown-linux-gnu.tar.gz` | 6300846 | `0f17df5c0eefbfc1715e98a30c533476a7323c2d20145065589fbf7d2227d497` |
| `sysmlv2-0.12.0-x86_64-unknown-linux-musl.tar.gz` | 6379052 | `c84bb9cd0b79e67c4819d8646bc4e5123211b8c0922770a17fdf9a65ab26fd68` |
| `SHA256SUMS` | 869 | `aec6b4244b265e06675c57e2e2170489fbd49fa9a5cd9afa3af92c2f8680bfc9` |
| `SIZES.md` | 669 | `d16665390c129646bfad88cf3b9561d4211d1b8a8aeb5f932a4605002466989f` |
| `sysml-wasm-0.12.0.tgz` | 16049331 | `1c905c0edfcd3abaf23a82a71e770a52d2cef69a9b06f4e6ad7e49a4aaea08f2` |

  The digests are the ones the release page reports for each asset (checked with `--network`). The content
  of `SHA256SUMS` was not fetched; for a checksummed pin the digest of the chosen archive is the pin.
- A source build from the local clone (tag `v0.12.0`, commit `ab3d590`) succeeded: `cargo build --release
  --locked -p sysmlv2-cli` with the toolchain `1.98.1` that `rust-toolchain.toml` names, target directory in
  the session scratchpad, 59 seconds on darwin-arm64; the binary is 19 MB and reports `sysmlv2 0.12.0`. The
  repository's `rust-toolchain.toml` makes `rustup` install the pinned toolchain on first use inside the clone.
- The CLI needs a standard-library directory (`--lib`). The OMG release library is a git submodule that a
  shallow clone lacks; the `libs/stdlib` directory of the OpenSysML clone served as `--lib`. Without `--lib`
  `check` passes with `unresolved reference` warnings and `verify` cannot see `Real`.
- `check` on the frozen model: exit 0. `lint --format json` on the frozen model: 0 errors, 0 warnings, 10 infos
  (`naming-convention`). `verify --solve` on the frozen model: `PowerOK` and `DepthOfDischargeOK` are
  `undecided` (a chain through `environment`, which declares no multiplicity; `z3: not in the solvable
  fragment: non-scalar or unknown cardinality of c`; the CLI asks for `[1]` on the usage).
- `verify --solve` reads usage-level `assert constraint`s with `[1]` features as one conjunction and narrows
  domains: asserts `capacity in [20, 25]` and `demand <= 0.3 * capacity` (demand 7.98) give `VIOLATED
  (propagation: domains contract to empty, unsatisfiable)` on both and exit 1; with `[20, 200]` both are
  `satisfied (holds for all values in the narrowed ranges)`. It is an exclusion check (joint unsatisfiability),
  not a `holds` question. A `satisfy requirement ... by` claim over an unbound part stays `undecided` with a z3
  witness per constraint. The opensysml `solve` engine gives the cleaner three-way answer of probe 5 and needs
  no binary beyond `z3`; the toolkit adds `check` and `lint` and a CI-gating exit code.

## Recipes

Working code, run against 0.12.1. `MODEL` is `examples/adcs/cubesat_tradespace.sysml`.

### Strict single-file load

```python
import pathlib
import opensysml

conn = opensysml.connect()  # one private runtime per interpreter
text = pathlib.Path("examples/adcs/cubesat_tradespace.sysml").read_text()
model = conn.load_from_content(text, strict=True)  # ModelError carries the diagnostics
assert model.ok
# files that import each other:  conn.parse_sources([path_a, path_b], strict=True)
```

### `verify_requirement` with a negative control

```python
PKG = "CubesatTradeSpace::"
req = """
 requirement def MassBudget { subject c : Cubesat; in limit : MassValue;
   require constraint { c.totalMass <= limit } }
}"""
model = conn.load_from_content(text.rstrip()[:-1] + req, strict=True)
kg = lambda x: model.eval(f"{x} [SI::kg]")  # a Quantity; a plain number is a type mismatch
ask = lambda limit: model.verify_requirement(
    PKG + "MassBudget", subject=PKG + "cubesatBaseline", named_arguments={"limit": kg(limit)}
)
ok, control = ask(20.0), ask(5.0)
assert ok.holds and ok.engine == "run" and ok.strength == "observed"
assert not control.holds and control.strength == "witnessed"
```

### `verify_satisfaction`

```python
reqs = """
 requirement def Budget { subject c : Cubesat; attribute limit : MassValue default = 20.0 [kg];
   require constraint { c.totalMass <= limit } }
 requirement budgetOk : Budget;
 requirement budgetTight : Budget { attribute :>> limit = 5.0 [kg]; }
 satisfy budgetOk by cubesatBaseline;
 assert satisfy budgetTight by cubesatBaseline;
}"""
model = conn.load_from_content(
    text.rstrip()[:-1] + reqs, strict=True
)  # loads clean though one is false
verdicts = model.verify_satisfaction()
assert [v.holds for v in verdicts] == [True, False] and not model.satisfied()
```

### `holds` through the `solve` engine (the `smt` engine answers no constraint claim)

```python
claims = """
 constraint def PowerMonotone { in s1 : LengthValue; in s2 : LengthValue;
   (s1 <= s2) implies (81.6 [SI::W/SI::m] * s1 <= 81.6 [SI::W/SI::m] * s2) }
 constraint def BatteryRegionSat { in cap : EnergyValue; in t : PowerValue;
   (cap >= 20.0 [SI::W*SI::h] and cap <= 26.0 [SI::W*SI::h] and t >= 0.4 [SI::W] and t <= 1.5 [SI::W])
   and ((12.0 [SI::W] + t + 0.9 [SI::W]) * 0.6 [SI::h] <= 0.3 * cap) }
}"""
model = conn.load_from_content(
    text.rstrip()[:-1] + claims
)  # constants: read from the model in real use
v = model.verify_constraint(PKG + "PowerMonotone", engine="solve", question="holds")
assert (v.status, v.strength) == ("holds", "proved")
r = model.verify_constraint(PKG + "BatteryRegionSat", engine="solve", question="satisfiable")
assert (r.status, r.strength) == (
    "unsatisfiable",
    "proved",
)  # the region is excluded before simulation
```

### Analysis with `in` parameters

```python
src = """package T { private import ScalarValues::*;
 part def Veh { attribute mass : Real = 1.0; }
 part car : Veh;
 analysis def Cost { subject v : Veh; in rate : Real; in days : Real;
   return total : Real = rate * days * 2.0; }
}"""
m = conn.load_from_content(src, strict=True)
run = m.run_analysis("T::Cost", subject="T::car", named_arguments={"rate": 3.0, "days": 4.0})
assert run.outputs == {"total": [24.0]}
```

### Sweep

```python
grid = m.run_sweep(
    "T::Cost", {"rate": (1.0, 3.0, 1.0)}, subject="T::car", named_arguments={"days": 2.0}
)
assert [r.outputs["total"][0] for r in grid] == [4.0, 8.0, 12.0]  # inclusive grid
a = m.run_sweep(
    "T::Cost",
    {"rate": (1.0, 3.0)},
    subject="T::car",
    named_arguments={"days": 2.0},
    samples=4,
    seed=7,
)
b = m.run_sweep(
    "T::Cost",
    {"rate": (1.0, 3.0)},
    subject="T::car",
    named_arguments={"days": 2.0},
    samples=6,
    seed=7,
)
assert [r.inputs for r in b][:4] == [r.inputs for r in a]  # row i does not depend on n
# log-uniform: sweep the exponent (0, 3) and exponentiate inside the case: 10.0 ** e
```

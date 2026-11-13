# Note: using OpenSysML (opensysml) and sysml-toolkit for the cubesat configuration space (WP4b)

Sources, read 2026-11-08: PyPI metadata for `opensysml` (0.12.1, released 2026-11-06; Python client
over gRPC to the Go `sysml-grpc` runtime; deps grpcio, protobuf, sigstore; runtime binary and stdlib
fetched on first use into `~/.opensysml/bin`); the OpenSysML README (parse, symbols, eval,
instantiate, execute actions/states, verify_constraint / verify_requirement / verify_satisfaction,
calc, run_analysis, run_sweep; `list_engines()`); Open-MBEE/sysml-toolkit README (Rust toolchain:
`sysmlv2 check|fmt|lint|eval|verify --solve|viz`, Python bindings via maturin, not on PyPI under that
name); and `/Users/z/Documents/GitHub/toaster` (pins opensysml 0.9.0 and sysml-toolkit CLI v0.9.1;
supervisor: "almost certainly does not use the latest releases ... but you can learn a lot").
Everything from toaster is verified at 0.9.0 only; re-check each call against the 0.12.1 docs.

## Patterns worth copying (toaster)

- Session: `conn = opensysml.connect(version=...)`; `model = conn.load_from_content(text, strict=False)`;
  `assert model.ok, format_diagnostics(model.diagnostics)`; close in `finally`. The stdlib (`SI`, `ISQ`,
  `ScalarValues`, `MeasurementReferences`) is built into the runtime.
- Units inline in expressions: `model.eval("Pkg::rated.deliveredEnergy(800.0 [SI::W], 120.0 [SI::s])")`
  returns a Quantity with `.magnitude` and `.unit.text`. Dimensionless: `MeasurementReferences::
  DimensionOneValue` and `[MeasurementReferences::one]` (ISQ::DimensionOneValue / SI::one absent at 0.9.0).
- Design-space shape: `abstract part def` for the role, concrete `part def :>` for alternatives with
  `default` values, concrete `part` usages with `:>>` redefinitions as configurations, requirement
  thresholds read from the model rather than retyped, and a negative control per model check
  (`assert not satisfy`, or a deliberately infeasible part and `not verdict.holds`).
- Verification: `model.verify_constraint("Pkg::Def::constraintName", subject="Pkg::rated", engine="run")`
  → `.holds`; `verify_satisfaction(...)` → verdicts with `.kind .element .holds .error`.
- Query: `model.query(scope=, select=, where=...)` sees named elements only; fall back to
  `json.loads(model.to_api_json().content)` for the rest. Name everything you will need to find.
- Sweeps at 0.9.0 were Python loops over `model.eval`; the runtime advertised a `sweep` engine that
  toaster never used. 0.12.1 documents `run_sweep` (grid or `samples`+`seed`): verify reproducibility,
  per-design independence of n, and log-range support before using it as the sampler.

## Pitfalls (toaster DEFERRED/probes, re-check at 0.12.1)

- No cross-source `import` between separately loaded files: concatenate sources and load once.
- A false `assert satisfy` loads without a diagnostic: check with eval or verify_satisfaction.
- Unit labels from eval come back unsimplified; the arithmetic is right.
- "Holds for all values" was not reachable from the Python client at 0.9.0; toaster shelled out to
  `sysmlv2 verify --solve` (Z3). Only needed if we claim universal constraint satisfaction.
- Editor API rejected many constructs; author models as text.
- Engine names differ between docs and code (`run`, `check`, `ir`; `list_engines()` is authoritative).
- `to_api_json()` can crash on redeclared members; `query()` misses unnamed connectors and satisfy.

## CI and tests (toaster)

- Runner `ubuntu-24.04` (GLIBC for the toolkit CLI); `~/.opensysml` not cached in CI, the gRPC binary
  downloads on first `connect()`; `.tools` cache keyed on the pin file for the toolkit.
- Tests that need the runtime fail hard (no silent skip) under an env flag (`TOASTER_REQUIRE_TOOLS=1`);
  use the same discipline here (a session fixture that fails with the named cause).
- A test that pins the binary cache dir to a tmp path covers download, checksum mismatch and cache hit.

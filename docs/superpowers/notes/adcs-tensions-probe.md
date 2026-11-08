# Note: ADCS tension probe (does the current dataset expose recognizable, unasserted tensions?)

Date 2026-11-08. A read-only probe by the project manager, run before WP7 is scoped, on the accepted WP2 estimator
(`HyperbolicTradeSpace`) and the accepted WP4 dataset (`examples/adcs/data/adcs_designs.csv`, 1000 designs, seed 0).
Nothing here is committed code: the script was a scratch file. The WP3 tension report does not exist yet, so its
three parts were computed by hand with the same definitions as the WP3 scope.

## Method

- Rows: `settled` designs only (960 of 1000; the settling time of unsettled designs is censored at `t_end`).
- Conditioning by hand: each attribute becomes a larger-is-better log-metric u = −log(attribute), standardized to zero
  mean and unit standard deviation over the rows used; the estimator is given exp(u). Orientation is the reciprocal
  for all four (settling time, pointing error, mass, control effort), as the notebook will do with
  `LogAffinePreconditioner(orientation=[-1]*4)`. The standardization fixes the reference point, so the facet found is
  the one tangent at the balanced point of this conditioning (spec §4).
- Fits: τ = ∞ (LP, `min_exponent = 0`) for the contending set; a working τ found by bisection so that `frac_above_`
  is about 0.10.
- Near-frontier rows: |log V| < 1/τ at the working τ. Association is the Pearson correlation of u among those rows;
  tension directions are the PCA of the near-frontier Z (loadings mapped to metrics by `basis_`).
- Repeated on subsets by wheel class and by star-tracker grade.

## Results, all designs (n = 960)

- Contending set at τ = ∞: all four metrics, with exponents settling 0.202, pointing 0.143, mass 0.006, effort 0.649.
  Mass is in the support but almost inert (0.006).
- Working τ = 21.7: settling 0.198, pointing 0.146, mass 0.094, effort 0.562; 89 near-frontier rows, n_eff 16.9.
- Association among near-frontier designs: settling–effort −0.97 (tension), pointing–effort −0.73 (tension),
  pointing–mass −0.71 (tension), settling–pointing +0.62 (aligned), settling–mass −0.22, mass–effort +0.24.
- Principal tension directions: the first (72 % of the spread) loads settling +0.51, pointing +0.48, mass −0.54,
  effort −0.46: designs trade fast settling and good pointing against effort and mass together; the second (24 %)
  separates settling from pointing and effort.
- Unrestricted correlations of the four log-metrics over all designs are weak (|r| ≤ 0.37), so the structure above is
  frontier structure, not a global correlation.

## Results by subset

| subset | n | contending set at τ = ∞ (exponents) | notable near-frontier associations |
|---|---|---|---|
| wheel small | 332 | pointing .43, mass .55, effort .03 (size 3) | pointing–mass −1.00, pointing–effort −0.62 |
| wheel medium | 326 | pointing .42, mass .55, effort .03 (size 3) | pointing–mass −1.00, pointing–effort −0.87 |
| wheel large | 302 | pointing .41, mass .56, effort .04 (size 3) | pointing–mass −1.00, settling–effort −0.90 |
| ST coarse | 334 | settling .01, pointing .84, effort .15 (size 3) | pointing–effort −0.96, settling–effort −0.87 |
| ST medium | 327 | settling .05, pointing .50, mass .02, effort .43 (size 4) | pointing–effort −0.95, settling–effort −0.89 |
| ST fine | 299 | settling .14, pointing .25, effort .61 (size 3) | pointing–effort −0.99, settling–effort −0.98 |

Within a wheel class, mass takes three values (one per star-tracker grade), so the −1.00 pointing–mass association
there is the star-tracker grade itself: finer tracker, better pointing, more mass. Within a star-tracker grade, mass
varies only through the wheel class and is inert (exponent 0.00 to 0.02).

## Reading

What a spacecraft engineer would recognize, and the fit exposed without being told:

1. Settling speed against control effort (r = −0.97 near the frontier; the dominant exponent is on effort). Fast
   slews cost actuation effort. Recognizable.
2. Pointing against control effort (r = −0.73). The pointing budget is dominated by the steady-state error under the
   solar-pressure torque, which falls as 1/Kp, and high gains cost effort. Recognizable once explained.
3. Pointing against mass, through the star-tracker grade (r = −0.71 over all designs; −1.00 within a wheel class).
   A better sensor weighs more. Recognizable.
4. Settling and pointing are aligned (+0.62): both improve with the proportional gain. This is the co-movement the
   WP4 review noted; the fit reports it as alignment, not as tension.

What was not exposed:

5. Agility against mass through wheel class. Mass is weakly involved over all designs (τ = ∞ exponent 0.006, working
   0.094), and within a star-tracker grade it is inert. Wheel class changes settling little (median settling 301 s for
   small wheels against 264 s for large), because torque limits rarely bind (torque-saturated time fraction 0.7 % for
   large wheels, 7 % for small) and the gains dominate. The one place small wheels show up is the momentum flag
   (13.7 % of small-wheel designs violate it, none of the others), and the flag is not a metric.

## Caveats

- Near-frontier samples are small (89 rows over all designs, 19 to 34 per subset): the associations and the
  exponents below about 0.03 are noisy, and the LP support is sensitive to a few vertex designs. The 0.006 on mass is
  at the level of that sensitivity.
- The result depends on the hand conditioning (standardized reciprocals). A different reference point would pick
  another facet. The notebook will have to show the conditioning diagnostics and, ideally, a sensitivity check.
- Mass takes only nine discrete values, so any association with it is largely a statement about hardware strata.

## Verdict for the driver

The current dataset exposes three recognizable, unasserted tensions (settling vs effort, pointing vs effort, pointing
vs mass via star-tracker grade) and one recognizable alignment (settling and pointing). The contending set at τ = ∞ has
size 4 over all designs, with mass nearly inert, and size 3 within each wheel class and star-tracker grade. It does not
expose the agility-vs-mass story through wheel class, which the spec names as a candidate tension. Whether the
requirement ("recognizable and intuitive once explicated") is met by the first three alone, or the case should be
enriched so that wheel class matters (scenarios where small wheels saturate, a wider hardware spread, or a power-like
attribute), is a decision for the supervisor; WP7's scope carries it as an open decision.

## WP4b: opensysml verification

Draft written by the phase 1 implementer, 2026-11-07, for the WP4b note; another implementer finishes this note
(dataset, R-13 and R-14 results, tensions, levers). Client `opensysml` 0.12.1 (PyPI), runtime `sysml-grpc` v0.12.1,
Python 3.12, macOS arm64. The reference repository `toaster` pins 0.9.0; everything below was run against 0.12.1, not
read from the older notes. The checks are kept as tests in `tests/test_cubesat_model.py`.

### Start-up and engines

- `uv sync` installs the client (grpcio, protobuf, sigstore). The runtime binary is downloaded and cached in
  `~/.opensysml/bin` on the first `opensysml.connect()`; here it replaced a cached v0.9.1 (from `toaster`) with a
  `UserWarning`. `connect()` then reuses the running service for the rest of the process.
- A bad `OPENSYSML_BINARY` raises `opensysml.errors.ConnectionError` ("names ..., which is not an executable file");
  `cubesat_model.get_connection` turns the error classes into `OpenSysMLUnavailable` with the cause named (service
  binary unavailable / download failed, checksum mismatch, trust failure) and the test fixture fails with that
  message, never skips. The deliberate failure trial runs in a fresh interpreter, because a connection already made
  in the process is reused.
- `connection.list_engines()`: `check` (bounded; outcomes, holds, sensitive), `explore` (proved; outcomes), `run`
  (observed; evaluate), `smt` (proved; holds, sensitive), `solve` (proved; satisfiable, holds), `sweep` (observed;
  sweep), and `tool:fmi` (unavailable: `OPENSYSML_FMI_RUNNER` not set). Only `run` answers `evaluate` questions;
  `verify_constraint(..., engine="check"|"smt"|"solve")` returns a verdict with `error="<engine> does not answer
  evaluate questions"`. The model layer picks the engine from `list_engines()` (first ready engine answering
  `evaluate`) rather than a documented name. The universal questions (`question="holds"` with `smt`) were not
  exercised: WP4b makes no universal-satisfaction claim.

### Feature by feature

| feature | outcome at 0.12.1 |
|---|---|
| `connect`, `load_from_content(text, strict=True)` | works; the 351-line model loads in about 25 ms with no diagnostics; `self_check()` returns `holds` with no findings (349 elements); a broken source raises `ModelError` under `strict=True` (negative control). |
| Standard library | `ISQ::*`, `SI::*`, `ScalarValues::*`, `RealFunctions`, `NumericalFunctions`, `QuantityCalculations` resolve. `import` needs a visibility (`private import`) or strict load errors. Absent: `SI::Wh`, `SI::mW`, `SI::deg`, `ISQ::AngleValue` (`PlaneAngleValue`), `ISQ::MassPerAreaValue` (`SurfaceDensityValue`). Workarounds: `[SI::W*SI::h]`, N·m values written as `0.0005 [N*m]`, `[SI::arcsec]`. |
| Inline units, `eval` | `model.eval("Pkg::Calc(0.5 [SI::m], 3.0 [SI::J])")` works. Calc invocations come back as a one-element list of `Quantity`, attribute reads as a bare `Quantity`. The magnitude is in the written unit (`unit.text`), the unit labels of derived quantities are unsimplified (`SI::'kg⋅m²⋅s⁻³'` for watts), so values are converted with `Quantity.in_unit(unit)` using a unit object obtained from `model.eval("1.0 [SI::W]").unit`. |
| `model.calc` and calcs with quantity parameters | plain floats are rejected ("cannot write 0.5 (a Real) to a feature typed by LengthValue"); a `Quantity` with a client-built unit is accepted. `eval` with inline units is the simpler path and is used. |
| Expressions | `if c ? a else b` is the conditional; `sqrt` of a bare name is unresolved: `RealFunctions::sqrt` takes numbers only, `QuantityCalculations::sqrt` takes quantities (unit of power over loss coefficient is a perfect square and comes out in N·m); `min` is `NumericalFunctions::min` (numbers). Docs `doc /* */` before an element documents the package, not the element; plain comments are used. A value written with `=` is fixed (redefinition is an error), design variables use `default =`. |
| `instantiate` | works on part usages and part definitions; about 3.5 ms per `Cubesat` with 20 derived features, and 200 configurations written as `part cfg_i : Cubesat { :>> panelSpan default = ...; part :>> wheel : LargeWheel; ... }` in one extra package appended to the model text load in 0.1 s. Derived features are computed by the calcs at instantiation. A failing derived feature is reported as an error string in `instance.features`, not an exception: the layer reads only named, checked features. |
| Structural reads | `model.find(fqn).children()` gives enum literals in declaration order; `model.query(scope=[pkg], where={"property": "@type", "operator": "=", "value": "PartDefinition"})` lists definitions; `symbol.specializations[i].target_id` finds the alternatives of an abstract part; `instantiate(part_def_fqn).get("wheelClass")` returns the `EnumLiteral` the alternative is keyed by; `symbol.attribute_facts()` gives constant defaults with units without instantiating. Ranges are read as `model.eval("Pkg::designSpace.panelSpanMin")`. No source scraping and no `to_api_json()`. |
| `verify_constraint` | works with `subject=<usage>`; a constraint's `in` parameter is not bound by the subject, so the constraint is a member of `Cubesat` with `in c default = self;` (the form `in c = self;` loads with a warning "Bound features should have conforming types"). Extra inputs (the measured slew energy) go in `named_arguments` as `Quantity`. `Verdict.holds` is the answer, `Verdict.error` must be checked (an unbound parameter gives `holds=False` with an error); the layer raises on a non-empty error. Negative controls: a 20 Wh battery with a fine tracker gives `dod_ok=False`; a 60 W housekeeping load gives `power_ok=False`. |
| `run_analysis` | `analysis def ModelTest` with a subject and a returned attribute runs and returns the total mass; it stays a documented stub of the model test (the slew is Python). |
| `run_sweep`, grid | works on a calc with `Quantity` range endpoints and step; `PanelMass` over span 0.3 to 1.0 step 0.1 gave 8 rows, engine `sweep`, strength observed, equal to density × span × chord to 1e-12. |
| `run_sweep`, `samples` + `seed` | rows are drawn uniformly per range (no log option, no categorical draws); the same seed reproduces the table; the first rows are the same for 5 and for 8 samples (design `i` independent of `n`); the draw order is by row across parameters, so two-parameter sweeps are prefix-stable too; a different seed differs. Log-uniform sampling works through a `log10` parameter (`10.0 ** x` in the calc; verified on a toy calc). |
| Sampler decision | Python sampler kept (`SeedSequence(seed).spawn(n)`, one child seed per design, as in WP4), because the dataset records a per-design seed from which a design can be rebuilt alone, the categorical draws are not available from `run_sweep`, and the draws should not depend on the Go generator across platforms. The ranges and enumerations it uses are read from the model. `run_sweep` is used for the grid check of R-5 and its reproducibility is a test. |
| Cross-package reference in one source | `package Configurations { part cfg_0 : CubesatTradeSpace::Cubesat {...} }` appended to the model text resolves with qualified names. Separately loaded sources were not tried (the carried pitfall stands, one concatenated source is loaded). `to_api_json()`, `satisfy` and `verify_satisfaction` are not used, so those pitfalls were not re-tested. |

### Gaps and fallbacks used

- No `Wh`, `mW`, `deg` units: compound units and SI values.
- Quantity-typed calc and sweep arguments need `Quantity` objects, not floats: units are taken from `eval("1.0 [..]")`.
- Verdict errors are data, not exceptions: checked in `CubesatModel._holds`.
- Constraint parameters are not bound by `subject`: member constraints with `in c default = self`.
- Instance feature errors are strings: only features whose success the tests establish are read.
- The CI runner downloads the runtime binary on first use (not cached); `REQUIRE_OPENSYSML=1` is read by the test fixture only to say so in the failure message; the behaviour is the same without it.

### What the client provided for free

Parsing and diagnostics with a reflective self-check, unit-carrying arithmetic in the calcs,
derived-attribute evaluation at instantiation (the whole mass and power accounting of a configuration in one
round trip), constraint verification per concrete configuration, the grid sweep of a calc, the enumeration and
specialization reads that remove every table from the Python layer, and the documented analysis definition.

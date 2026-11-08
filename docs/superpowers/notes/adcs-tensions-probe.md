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
- The CI runner downloads the runtime binary on first use; `REQUIRE_OPENSYSML=1` is read by the test fixture only to say so in the failure message (the behaviour is the same without it). Phase 2 sets the flag in `.github/workflows/test.yml` and caches `~/.opensysml` keyed on the locked `opensysml` version.

### What the client provided for free

Parsing and diagnostics with a reflective self-check, unit-carrying arithmetic in the calcs,
derived-attribute evaluation at instantiation (the whole mass and power accounting of a configuration in one
round trip), constraint verification per concrete configuration, the grid sweep of a calc, the enumeration and
specialization reads that remove every table from the Python layer, and the documented analysis definition.

## WP4b results (phase 2): dataset, levers, R-13, R-14

Written by the phase 2 implementer, 2026-11-07. Dataset `examples/adcs/data/adcs_designs_cubesat.csv`, 1000 designs,
seed 0, generated with

    uv run python examples/adcs/generate_dataset.py --model cubesat --n 1000 --seed 0 --force

(the cubesat defaults are `--slew-deg 90 --t-end 450`; `max_step` 0.5 s; the scenario is also stored in the columns
`slew_deg`, `t_end_s`, `max_step_s`). The checks are `tests/test_adcs_enrichment.py` (hand version of the probe on the
committed CSV, deterministic seeds, plus an agreement test against `tension_report`) and the `-k reproduc` tests in
`tests/test_cubesat_model.py`. Thresholds are exactly those of the approved scope and were not touched.

### Status against R-14 (amended)

Status after amendment 4 (final): R-14 and the R-15 shares hold; R-13 (a), (b), (c) fail and (d), (e) hold on the committed
dataset (see "Amendment 4: results" below; the statement written in phase 2, that R-13 a to e held, referred to the 90 degree
dataset and is superseded by amendments 2 to 4). R-14 was amended (WP4b scope amendment 1, recorded in
`work-packages/WP4b-decisions.md`): the absolute small-wheel level of 0.25 was an arbitrary default of the scope and is
dropped; R-14 keeps its two relative clauses. Final numbers on the committed dataset: median `torque_saturated_frac` of
small-wheel designs 0.237 (large wheels 0.0139, ratio about 17 against the required 3); median settling 247 s small
against 76 s large, ratio 3.2 against the required 1.25 (these are the phase 2 numbers on the 90 degree dataset; the final
R-14 numbers are in "Amendment 4: results"). Both relative clauses held then. The test `test_torque_binds_for_small_wheels` carries no xfail marker and no longer asserts the
0.25 level. History kept for honesty: before the amendment the implementer stopped under the scope's stop rule after the
three allowed adjustments, and a truncation of the same runs at 400 s (small-wheel median 0.266) was noted but not
applied.

### Diagnosis of the phase 1 dataset, and the levers (every attempt)

Why torque did not bind at the defaults (45 degrees, 1500 s, Kp 0.003 to 0.1, Kd 0.03 to 1.0, wheels 0.5/2/10 mN.m):
`torque_saturated_frac` is the share of the whole horizon with a saturated axis, and a wheel saturates only during the
acceleration and braking of the slew (tens of seconds for a 0.5 mN.m wheel on a 0.5 kg.m2 inertia) while the horizon is
1500 s long: the flag is diluted by waiting time, and power never constrains torque either, because with c = 5e4
W/(N.m)2 the power-limited torque is above every wheel maximum for all but the smallest panels (3.2 % of final-dataset
designs have a power-capped torque, all with large wheels). A 400-design check of the defaults: median saturation
0.009 / 0.003 / 0.0 (small / medium / large), settling 231 s against 185 s, power_ok True for all.
Before the three adjustments I ran simulation-only scans (60 to 90 designs, gain multipliers, slew 45 and 90 degrees,
horizons 200 to 1500 s, Kd ranges, small-wheel torque) to see which mechanism moves saturation; I did not evaluate R-13
on any scan. The scans showed that (i) a steeper slew or a shorter horizon alone cannot reach 0.25 with 85 % settled;
(ii) the gains are what makes the command exceed the cap (command about 0.35 Kp N.m at 90 degrees, against caps of
0.3 to 10 mN.m); (iii) saturation and the settled fraction trade against each other through underdamped
saturated ringing (high Kp with low Kd does not settle).

| # | change (what, why) | R-14 (sat small / medium / large; settling small vs large) | settled | R-13 |
|---|---|---|---|---|
| 0 | none (45 deg, 1500 s, Kp .003-.1, Kd .03-1) | 0.009 / 0.003 / 0 ; 231 vs 185 s (400 designs) | 0.92 | (a) fails: mass exponent 0.002 |
| 1 | scenario: 90 deg, 600 s (the scope's first lever for R-14) | 0.034 / 0.013 / 0 ; 283 vs 196 s : FAIL | 0.761 (R-15 fails) | (a) fails: mass .024; (b) fails: mass in support 87 %; (c) fails: settling-mass -0.07; (e) fails: pointing-mass -0.02 |
| 2 | constants: Kp 0.1-3.0, Kd 0.5-2.0 (a stiff loop that saturates every wheel), horizon 400 s, 90 deg | 0.349 / 0.131 / 0.021 ; 208 vs 44 s : PASS | 0.919 | (a) pass (mass .318, energy balance .276); (b) pass; (c) FAILS: settling-mass -0.01 (near-frontier: small 45, medium 41, large 0); (d) pass; (e) FAILS: settling-effort +0.17, settling-pointing -0.13 |
| 3 | constants: Kp 0.03-1.0, Kd 0.3-1.5 (between the two earlier ranges, to keep gains mattering), small wheel maxTorque 0.5 -> 0.3 mN.m (public small cubesat wheels reach 0.2 mN.m class), horizon 450 s, 90 deg | 0.237 / 0.043 / 0.014 ; 247 vs 76 s : small-wheel saturation FAILS 0.25 (others pass) | 0.888 | all pass |

Adjustment 2 failed (c) and (e) for a physical reason that guided adjustment 3: once every wheel saturates, the control
effort integral is set by the momentum the slew has to carry (roughly the same for any gains) and the pointing floor is
set by the star tracker (steady error 4(tau)/Kp is negligible at Kp >= 0.1), so the gains stop acting as a design axis
and the settling-effort and settling-pointing relations disappear. Adjustment 3 keeps Kp low enough that the large
wheels hardly saturate, so the gains still matter for effort and pointing, and lowers the small wheel's cap instead.
Adjustments 2 and 3 each changed several constants at once; I count each as one adjustment (the scope's three), as
the scope's wording is "at most three times total".

### Phase 2 constants and scenario (history; the final scenario is 30 degrees, 600 s, wheel momentum 10 / 30 / 100 mN m s, see amendment 3)

The paragraph below describes the 90 degree phase 2 dataset and is kept as history; its numbers (feasible counts, flag shares,
ranges) do not describe the committed dataset. Final constants and scenario: slew 30 degrees about X, horizon 600 s,
`max_step` 0.5 s; Kp 0.03 to 1.0 N.m/rad and Kd 0.3 to 1.5 N.m.s/rad (log-uniform); wheels maxTorque 0.3 / 2 / 10 mN.m with
momentum 10 / 30 / 100 mN.m.s and mass 0.12 / 0.25 / 0.60 kg (small / medium / large); tracker, panel, battery and power constants as in the model.

Phase 2 (superseded) text: Unchanged from the defaults list except: Kp 0.03 to 1.0 N.m/rad, Kd 0.3 to 1.5 N.m.s/rad (log-uniform); small wheel
maxTorque 0.3 mN.m (momentum 5 mN.m.s, mass 0.12 kg; medium 2 mN.m, large 10 mN.m); scenario 90 degree slew about X,
horizon 450 s, `max_step` 0.5 s. Total mass spans 11.9 to 16.1 kg (the scope expected about 13 to 18; the 12U bus mass
of 10 kg is a default). The pointing floor, tracker, panel, battery and power constants are as in the model header.
Feasibility: `power_ok` is True for every design (available power is at least 11.1 W: the smallest panel gives 24 W, the
loads are 12 W plus at most 1.5 W), `dod_ok` is violated by 13.1 % of designs (small battery with a fine tracker or
a busy slew), `settled` by 11.2 % (76 % settled for small wheels, 95 % for the other two), `momentum_ok` by 55.1 %
(the 90 degree slew needs more momentum than small and many medium wheels store; the simulator does not clip momentum,
so the flag is informational, as in WP4). 772 designs are feasible (settled, `power_ok`, `dod_ok`). Attribute ranges
over all designs: power margin 6.6 to 68 W, energy balance 1.0 to 56 Wh, eclipse reserve -2.6 to 52 Wh, peak slew
power 1.3 to 7.4 W, depth of discharge 0.04 to 0.43.

### R-13 on the phase 2 dataset (90 degrees; superseded; feasible designs, n = 772; conditioning as in the Method section)

- Contending set at tau = infinity (LP, `min_exponent = 0`), size 6: settling 0.137, pointing 0.151, total mass 0.266,
  control effort 0.163, eclipse depth of discharge 0.065, energy balance 0.219; peak slew power, power margin and eclipse
  reserve are at 0 (power margin and energy balance are the same quantity up to a constant, correlation 0.98; reserve
  and depth of discharge likewise, 0.95).
- Working tau = 20.8 (`frac_above_` 0.0997), exponents: settling 0.223, pointing 0.090, mass 0.144, effort 0.240,
  depth of discharge 0.075, energy balance 0.228. Near-frontier rows |log V| < 1/tau: 87 (medium 43, small 34, large 10).
- Bootstrap (100 resamples, seed 0, LP support above 1e-3): mass in the support 100 % (median exponent 0.179), energy
  balance 100 % (0.213), settling 100 % (0.222), effort 100 % (0.228), pointing 95 % (0.100), depth of discharge 85 %
  (0.049), power margin 3 %, reserve 13 %, peak slew power 0 %.
- Near-frontier Pearson associations of the oriented log-metrics (negative = tension): settling-mass -0.57,
  settling-effort -0.88, settling-peak slew power -0.75, pointing-effort -0.57, pointing-mass -0.61, pointing-peak slew power
  -0.65, mass-depth of discharge -0.63, mass-eclipse reserve -0.60, mass-energy balance -0.40, mass-power margin -0.33,
  settling-pointing +0.50 (aligned), settling-power margin -0.16, settling-energy balance -0.05.
- (a) holds (size 6; mass 0.266 and energy balance 0.219 above 0.05); (b) holds; (c) holds (settling-mass -0.57, three wheel
  classes with at least 10 near-frontier designs, the large class with exactly 10); (d) holds (several power tensions, the
  strongest are peak slew power with settling -0.75 and depth of discharge with mass -0.63); (e) holds (-0.88, -0.57,
  -0.61, and settling-pointing +0.50). `tension_report` agrees with the hand computation (association matrix to 1e-9,
  same near-frontier count). Near-frontier samples are small (10 to 43 per wheel class), so the associations are
  noisy at the 0.1 level; the large-wheel class is thin; the mass exponent is stable under resampling.
- R-15: 1000 designs; settled fraction 0.888 (at least 0.85); violation shares of `settled`, `momentum_ok`, `power_ok`, `dod_ok`:
  0.112, 0.551, 0.0, 0.131.

### Physical explanation of the exposed tensions on the phase 2 dataset (R-17; superseded numerically by amendment 4 results)

- Agility against mass (settling-mass -0.57): the wheel class. A larger wheel gives more torque, so the saturated slew is
  shorter (median settling 247, 101 and 76 s for small, medium and large) and costs 0.5 to 1.4 kg more. With the small
  wheel's cap at 0.3 mN.m and the horizon at 450 s, torque limits bind for small wheels (median 24 % of the horizon, up to
  98 %) and not for large (1.4 %). Acts through the wheel-class variable.
- Power tensions: (1) energy balance (and power margin) against mass: the orbit-average surplus comes from panel area,
  and panel area costs mass (2.5 kg/m2) and, through the lever arm and panel mass, slew-axis inertia: -0.40 and -0.33
  with mass, +/-0.16 with settling. Acts through panel span. (2) Eclipse depth of discharge and reserve against mass: a
  larger battery rides through eclipse at a shallower depth and weighs 1/140 kg per Wh: -0.63 and -0.60. Acts through
  battery capacity. (3) Peak slew power against settling (-0.75) and pointing (-0.65): drawing less power in the slew
  means a smaller wheel or lower gains, hence a slower slew; low peak power comes with a coarse tracker (less load) hence
  poorer pointing. Acts through wheel class, gains and tracker grade. Peak slew power itself has exponent 0 in the
  contending set: it is aligned with mass (+0.75), so it rides on mass; it is a true but secondary tension.
  (Panel-power tensions mirror the energy balance; power margin and energy balance are redundant, as are reserve and depth
  of discharge.)
- Settling against effort (-0.88): faster settling needs stiffer gains and the effort integral grows with the torque
  commanded; recognizable. Acts through Kp and Kd.
- Pointing against effort (-0.57): the steady-state part of the pointing budget falls as 1/Kp and high gains cost effort;
  recognizable once explained.
- Pointing against mass (-0.61): a finer star tracker points better and weighs more (0.15, 0.35, 0.90 kg) and draws more.
  Acts through tracker grade.
- Settling and pointing are aligned (+0.50): both improve with Kp.
- Not recognizable / secondary: the strong mass-effort (+0.72) and mass-peak slew power (+0.75) alignments are two
  consequences of the same hardware choice (a large wheel is heavy, and with the high gains saturates and draws more); the
  alignment of power margin and energy balance with each other is an accounting identity, not a finding.
- What the power model does not do: power barely reaches the controls. The available-power cap on torque binds for only 3.2 %
  of the designs (large wheels with the smallest panels); the power attributes act mainly through panel and battery mass
  and inertia. The case is honest about this: the power story is the energy-sizing one (panel and battery against mass), not a
  power-limited slew.

### Amendment 2: R-13 and R-14 rerun on the momentum-feasible set (STOP RULE TRIGGERED; superseded by amendment 3 below)

Feasible now means settled, `power_ok`, `dod_ok` and `momentum_ok` (WP4b scope amendment 2, the supervisor's "Enforce as
feasibility"). Same dataset (1000 designs), method, conditioning and thresholds; no simulation, no tuning, no new levers.
Violation shares: settled 11.2 %, `momentum_ok` 55.1 %, `power_ok` 0 %, `dod_ok` 13.1 %.

Feasible designs: 346 of 1000 (previously 772), by wheel class: large 248 (of 311), medium 91 (of 345), small 7 (of 344).
Small-wheel designs are 98 % infeasible, medium 74 %, large 20 %.

R-14 on the feasible set (medians): saturated fraction small 0.0276, medium 0.0173, large 0.0146; the ratio small/large is
1.9, so "at least 3 times" FAILS. Settling time small 393 s, medium 196 s, large 73 s (ratio 5.4, the 1.25 clause passes).
Reason: the 7 surviving small-wheel designs have the smallest slews' worth of momentum (peak momentum about 0.004 N m s)
only because they are the sluggish, low-gain ones; torque saturation is no longer a discriminating feature.

R-13 on the feasible set (n = 346): working tau = 77.0, `frac_above_` = 0.101, 28 near-frontier rows (medium 20, large 8,
small 0).
- Contending set at tau = inf: settling time 0.320, pointing error 0.044, control effort 0.407, eclipse depth of discharge
  0.017, power margin 0.137, energy balance 0.077. Total mass exponent 0.000, peak slew power 0, eclipse reserve 0.
  (a) FAILS: the set has six attributes and a power attribute, but total mass is absent (needs >= 0.05).
- (b) FAILS: bootstrap support (100 resamples) of total mass is 0.00 (needs >= 0.90). Settling time, pointing error and
  control effort 1.00, power margin 0.92, depth of discharge 0.86, energy balance 0.56, mass 0.00.
- (c) FAILS on the near-frontier count: associations survive (settling time with total mass -0.79) but only one wheel class
  (medium, 20 rows) has >= 10 near-frontier designs; large has 8, small 0.
- (d) passes: strongest power tension peak slew power with settling time -0.899 (then with pointing error -0.614, energy
  balance with mass -0.515).
- (e) passes: settling time with control effort -0.984, pointing error with control effort -0.538, pointing error with mass
  -0.477, settling time with pointing error +0.512.
- R-15 share check (feasible > 50 % of the dataset) also fails, 346 of 1000.

Agility against mass: the association itself survives (-0.79, stronger than before) but the frontier does not
support it as a spread across wheel classes: with 7 small-wheel designs left, the near-frontier set is medium and large
only, and mass drops out of the contending set (mass is carried by the wheel class, which momentum feasibility now
filters on, so within the feasible set mass varies little: 13.4 to 16.1 kg for large, std about 0.5 kg).

Disposition: per the stop rule the failing tests are marked `xfail(strict=True)` citing amendment 2 (R-15 shares, R-14,
R-13 a, b, c); no threshold was weakened and nothing was tuned. For the supervisor.

### Amendment 3: physically consistent scenario (written before any simulation)

Supervisor choice: "Reopen levers for a physically consistent scenario" (`work-packages/WP4b-decisions.md`). Feasible stays settled, `power_ok` and `momentum_ok`, with every larger-is-better attribute positive. `dod_ok` is a reported
flag, not a filter in its own right, but it is not free: `dod_ok` is false exactly when the eclipse demand exceeds
(maximum depth of discharge x capacity), which is exactly when `eclipse_reserve_wh` (usable energy minus demand) is not
positive. A design with `dod_ok` false therefore has a non-positive larger-is-better attribute and is excluded for that
reason (scope Amendment 3), which is what the positivity filter already does; the test `feasible()` states it so.

**Step A: physics reasoning.**

Inertia range of the sampled designs (the existing `inertia_tensor` with the model's bus 10 kg, body 0.226 x 0.226 x 0.34 m,
panels 2.5 kg/m2 x span x 0.34 m, battery 140 Wh/kg, antenna and tracker as in the model): the slew axis is X, and
J_xx = 0.23 kg m2 (span 0.3 m, battery 20 Wh) to 0.99 kg m2 (span 1.0 m, battery 200 Wh); panel span dominates (0.23 to 0.97
over the span range, battery adds 0.02); median about 0.35 (corrected: 0.353 on the first 300 designs of the seed-0 sample, 0.338 on the feasible ones of them; the figure 0.5 first written here was wrong, and the table's 'at J = 0.5' column is not the median). The panel contribution scales like span^3.

Rest-to-rest slew of angle theta, torque saturated (accelerate for half the angle, brake for the other half): peak rate
sqrt(T theta / J), peak wheel momentum h_peak = J omega = sqrt(T J theta). A class with capacity h_max survives iff
theta <= h_max^2 / (T J). Using the SysML wheel numbers (T, h_max): small 0.3 mN m, 5 mN m s (h/T = 17 s); medium 2 mN m,
20 mN m s (10 s); large 10 mN m, 100 mN m s (10 s):

| class | h_max^2/(T) | theta_max at J = 0.23 | at J = 0.5 | at J = 0.99 |
|---|---|---|---|---|
| small | 0.083 | 0.36 rad (21 deg) | 0.17 rad (9.5 deg) | 0.084 rad (4.8 deg) |
| medium | 0.20 | 0.87 rad (50 deg) | 0.40 rad (23 deg) | 0.20 rad (11.6 deg) |
| large | 1.00 | 4.3 rad | 2.0 rad (115 deg) | 1.0 rad (58 deg) |

So the 90 degree slew of the previous scenario (1.57 rad) exceeds the capacity of every small wheel at every inertia, of
medium wheels above J = 0.13 (all designs) and of large wheels above J = 0.64 (the large-span half). That is why momentum
feasibility removed 98 % of small, 74 % of medium and 20 % of large designs: the scenario, not the design, was inconsistent
with the wheel classes. For small wheels to survive across most of the inertia range the slew must be of the order of 10
degrees or less; at 10 degrees (0.175 rad) the bang-bang bound is J <= 0.48 for small wheels (span up to about 0.66 m, over
half of the designs), J <= 1.1 for medium wheels (all) and everything for large wheels. The PD law lowers the peak rate
below the bang-bang one (the derivative term brakes early), so the bound is conservative.

Gains: the commanded torque is Kp/2 sin(theta/2) at the start of the slew. At 10 degrees that is 1.3 mN m (Kp = 0.03) to 44 mN m
(Kp = 1.0), so every small wheel (0.3 mN m) saturates at the start of every slew; a medium wheel (2 mN m) saturates for
Kp above about 0.046 (about 80 % of the log range of Kp); a large wheel (10 mN m) for Kp above about 0.23 (about 40 %). Torque
therefore binds hardest for small wheels, less for medium, least for large, which is the ordering needed for R-14, and at
10 degrees the large wheels are mostly PD-limited so the gains still act as a design axis. The linear closed loop is
J theta'' + Kd theta' + (Kp/4) theta = 0 (q_vec = theta/2); the slow pole when overdamped is Kp/(4 Kd), so a 1 % settling needs
about 4.6 Kd/(Kp/4) s: 920 s for the worst corner (Kp 0.03, Kd 1.5), 190 s for (0.03, 0.3), under 20 s for Kp >= 0.3. A
horizon of 600 s settles every design with Kp/Kd above 0.031 (the large majority of the gain box).

Wheel capacities: public cubesat wheels have momentum-to-torque ratios of roughly 5 to 20 s (for example 0.23 mN m with 1.7 mN m s
and 10 mN m with 180 mN m s in the commercial range), the brief's "tens of seconds" is the upper end. The current ratios (17,
10, 10 s) are within the plausible range, so the first adjustment changes only the scenario (slew angle and horizon); wheel
momentum capacities are changed only if the scenario alone leaves small wheels infeasible and that is recorded.

Choice for adjustment 1: slew 10 degrees about X, horizon 600 s, `max_step` 0.5 s, gains and wheel numbers as they are.

Simulation-only scans, if any, are declared below with their purpose; none evaluates R-13.

**Declared simulation-only scans.** After adjustment 2 and before adjustment 3, one scan: the first 200 designs of the seed-0
sample at 30 and at 40 degrees (horizon 600 s, wheel numbers of adjustment 2), to read momentum feasibility, saturation and
settling per wheel class. R-13 was not evaluated on it. Result (30 / 40 degrees): `momentum_ok` small 0.77 / 0.67, medium
0.93 / 0.90, large 1.0 / 1.0; median saturated fraction small 0.057 / 0.083, medium 0.015 / 0.018, large 0.008 / 0.009; median
settling small 152 / 169 s, medium 60 / 68 s, large 86 / 87 s. The bound of Step A predicted this (small wheels lose the
large-inertia designs as the angle grows). 30 degrees was chosen for adjustment 3 as the largest angle at which most small
wheels are still momentum-feasible (about 80 %).

**Every attempt** (1000 designs, seed 0, horizon 600 s, `max_step` 0.5 s, feasible = settled, `power_ok`, `momentum_ok`, all
attributes positive; no threshold or method change). Recorded command per attempt:
`uv run python examples/adcs/generate_dataset.py --model cubesat --n 1000 --seed 0 --slew-deg A --t-end 600 --force`.

| # | change and physics | feasible (small / medium / large) | R-14: sat. small / medium / large; settling small / medium / large | contending set (tau = inf) | bootstrap of mass | settling-mass; near-frontier rows (small / medium / large) |
|---|---|---|---|---|---|---|
| 1 | scenario only: 10 degrees (A = 10), wheels unchanged (5, 20, 100 mN m s). Small-wheel bang-bang bound J <= 0.48, medium J <= 1.1, large all | 796 (241 / 293 / 262); `momentum_ok` small 0.81, medium 0.997, large 1.0 | 0.0193 / 0.0102 / 0.0 (ratio unbounded, passes); 101 / 60 / 69 s (ratio 1.47, passes) | settling .338, effort .408, power margin .235, depth of discharge .019; mass 0 | 0.00 | -0.08; 66 / 32 / 16 |
| 2 | 20 degrees and wheel momentum capacities made consistent with torque: small 5 -> 10, medium 20 -> 30 mN m s (momentum/torque 33, 15, 10 s; a 20 degree rest-to-rest slew needs J <= 0.95 for small and 1.3 for medium by the bound; the larger angle lengthens the torque-limited phase) | 833 (279 / 292 / 262); `momentum_ok` small 0.94, medium 0.994, large 1.0 | 0.0376 / 0.0131 / 0.0068 (ratio 5.5, passes); 109 / 62 / 69 s (ratio 1.58, passes) | settling .305, mass .046, effort .403, depth of discharge .025, energy balance .165, reserve .055 | 0.69 | -0.13; 74 / 45 / 23 |
| 3 | 30 degrees (A = 30), wheel numbers of adjustment 2 (scan above) | 780 (239 / 279 / 262); `momentum_ok` small 0.81, medium 0.957, large 1.0 | 0.0409 / 0.0152 / 0.0080 (ratio 5.1, passes); 128 / 67 / 69 s (ratio 1.85, passes) | settling .310, pointing .044, effort .433, depth of discharge .006, power margin .207; mass 0 | 0.01 | -0.09; 56 / 16 / 4 |

Further numbers. Adjustment 1: working tau 41.4 (`frac_above_` 0.1005), 114 near-frontier rows; bootstrap support settling 1.0,
effort 1.0, power margin 0.97, depth of discharge 0.70, pointing 0.40, mass 0.00; associations settling-effort -0.96,
pointing-effort -0.65, pointing-mass -0.19 (e fails), settling-pointing +0.64, strongest power tension mass with depth of
discharge -0.54. Adjustment 2: working tau 28.4 (0.1008), 142 near-frontier rows; bootstrap settling 1.0, effort 1.0,
energy balance 1.0, mass 0.69, reserve 0.68, depth of discharge 0.63; settling-effort -0.97, pointing-effort -0.60,
pointing-mass -0.18 (e fails), settling-pointing +0.59, mass with depth of discharge -0.65; the mass exponent 0.046 misses
the 0.05 threshold of (a) by 0.004. Adjustment 3: working tau 46.1 (0.1013), 76 near-frontier rows; bootstrap settling 1.0,
pointing 1.0, effort 1.0, power margin 0.73, depth of discharge 0.72, energy balance 0.46, mass 0.01; settling-effort -0.95,
pointing-effort -0.63, pointing-mass -0.26 (e fails), settling-pointing +0.63, mass with depth of discharge -0.57, pointing
with peak slew power -0.50. In all three attempts total mass is absent or marginal in the contending set and the settling-mass
association is between -0.08 and -0.13 (threshold -0.30), so (a), (b), (c) fail in every attempt, and (e) fails on the
pointing-mass clause in every attempt (-0.19, -0.18, -0.26 against -0.30). (d) passes in every attempt. R-14 and the R-15
feasible-share check pass in every attempt.

**Committed dataset: adjustment 3** (30 degrees, 600 s, wheel capacities 10 / 30 / 100 mN m s). It is physically consistent: no
class is removed by the scenario beyond a boundary (small wheels lose 19 % of designs to momentum, medium 4 %, large none;
`settled` 97 to 98 % in each class; `momentum_ok` violated by 8.1 % overall, `settled` by 2.2 %, `power_ok` 0 %, `dod_ok`
13.1 %). Feasible 780 of 1000 (78 %; settled share 97.8 %).

**dod_ok.** `dod_ok` is false exactly when `eclipse_reserve_wh` is not positive (checked on the committed data, all 1000 rows:
no design with `dod_ok` false has a positive reserve), so the 13.1 % of designs with a violated `dod_ok` are excluded because
a larger-is-better attribute would be non-positive, not because `dod_ok` is a filter; `test_dod_violation_is_a_non_positive_reserve`
asserts it. R-13/R-14 evaluate on the same 780 designs.

**Disposition (STOP RULE TRIGGERED, amendment 3).** After three adjustments there is a physically consistent scenario and R-14
(and R-15) hold, but R-13 (a), (b), (c) and the pointing-mass clause of (e) do not. The tests that cannot hold are marked
`xfail(strict=True)` with the reason (`test_a_`, `test_b_`, `test_c_`, `test_e_`); the R-14 and R-15 tests have no marker.
Thresholds and method are untouched. Finding: with momentum respected, the agility-against-mass trade of wheel class does not
appear as a frontier tension. Corrected explanation (the sentence first written here, that wheel class moves mass by at most 1.4 kg
while other levers move it by several kg, was wrong: reviewer defect G-2): wheel mass is the largest single mass lever. The three wheels
weigh 0.36 (small), 0.75 (medium) or 1.80 kg (large), standard deviation 0.60 kg of the 0.84 kg total standard deviation (panel mass
std 0.16 kg, battery mass 0.34 kg), and wheel mass alone explains 55 % of the variance of total mass. Mass is nevertheless absent
from the contending set because heavier wheels do not settle faster: the 1 % settling time is set by the slow pole Kp/(4 Kd) of the PD
loop, corr(log settling, log(Kd/Kp)) = 0.992 for large wheels (0.993 in the review), so wheel class separates settling only at the
most aggressive gains; medium and large are indistinguishable (median settling small 128 s, medium 67 s, large 69 s). Where wheel class does act, it acts as a feasibility boundary: small wheels fail on momentum
for large-inertia designs (19 % of small designs at 30 degrees, 98 % at 90 degrees), not as a spread along the frontier. The
notebook should say so.

### Facts for WP7 interpretation

Final (amendment 4): dataset at 30 degrees, 600 s, wheel capacities 10 / 30 / 100 mN m s, ten attributes; feasible = settled,
`power_ok`, `momentum_ok`, all attributes positive; 780 of 1000 designs. Numbers in "Amendment 4: results" below.

(a) Power never limits a slew in this dataset. The available-power cap on torque is below the wheel maximum in 3.2 % of designs
(large wheels with the smallest panels), and `power_ok` is True for every design. The power attributes reach the controls only
through mass and inertia (panel and battery mass, lever arm), so power tensions are energy-sizing tensions, not power-limited-slew
tensions. On the feasible set the power margin is 7.0 to 68 W (median 27.6 W).

(b) Near-redundant attribute pairs (oriented, standardized log-metrics on the feasible set), so WP7 does not read them as
independent findings: power margin with energy balance 0.966; eclipse reserve with eclipse depth of discharge 0.921; and the new
slew time with settling time 0.947 (0.99 among near-frontier rows): the two measure the same slow-pole tail, see below.

(c) Wheel classes on the feasible set: small 239, medium 279, large 262 (of 344, 345, 311). Near-frontier rows at the working tau
(42.8): small 78, medium 23, large 1, so statements about large wheels rest on a single near-frontier design. Total mass (11.9 to
16.1 kg) is not in the contending set (exponent 0.000, bootstrap support 0.00): WP7 must read this as "mass is not a discriminating
attribute on this frontier", not "mass does not matter"; wheel mass is the largest single mass lever (0.36 to 1.80 kg, std 0.60 of
0.84), but heavier wheels do not settle or arrive faster at these gains. Mass associates with the energy attributes near the
frontier (depth of discharge -0.65, eclipse reserve -0.58, power margin -0.47, energy balance -0.44) and with pointing error
(-0.36: finer star trackers weigh more).

(d) R-13 (a), (b), (c) fail and (d), (e) hold; R-14 and R-15 hold. The tensions that hold: settling time and slew time each with
control effort (-0.95, -0.96), pointing error with control effort (-0.70), pointing with mass (-0.36), settling with pointing
aligned (+0.68; slew time with pointing +0.71), power tensions (mass with depth of discharge -0.65, pointing with peak slew
power -0.61). Wheel class acts as a feasibility boundary (small wheels lose 19 % of designs to momentum at 30 degrees, 98 % at 90),
not as a frontier tension; agility by slew time does not trade against mass either.

### What the SysML client provided for free (R-17)

Strict loading with diagnostics and `self_check` (a typo in the model is an error, not a silently wrong number);
instantiation of 10 configurations per load with all derived accounting (masses, generated and available power, usable
torque) computed by the model's `calc def`s; unit-aware arithmetic and the compound-unit checks of the accounting;
per-configuration constraint verification (`power_ok`, `dod_ok`); `run_sweep` for the panel-span grid check; enumeration
and specialization reads that removed every wheel or tracker table and every range from the Python. Costs: a runtime
download on first use, about 3.5 ms per instantiated cubesat, and a `fork` warning from the gRPC library when the generator's
pool is used (the pool is spawned, each worker opening its own connection, so it is harmless).

### Amendment 4: slew-time attribute (Step A, written before any simulation or any change to the model layer)

Supervisor choice: "One physics-justified lever: slew-time attribute" (`work-packages/WP4b-decisions.md`). This is adjustment 4
and the last; no further levers. Everything below is written and committed before `slew_time_s` is computed on any design.

**Why the 1 % settling time hides the actuator limits.** With the closed loop linearised, J theta'' + Kd theta' + (Kp/4) theta = 0
(q_vec = theta/2). When the loop is overdamped (the usual case in this gain box, Kd large against sqrt(J Kp)), one pole is
fast, about Kd/J, and one is slow, about Kp/(4 Kd). The error is the sum of the two modes and after the fast one has died
it decays as exp(-(Kp/(4 Kd)) t). The 1 % criterion waits for that tail: it needs about ln(100) = 4.6 time constants of the
slow pole, 4.6 x 4 Kd/Kp s, independent of the inertia and of the wheel torque as long as the saturated phase of the slew is
shorter than this tail. The saturated phase (accelerate and brake at the torque cap T: about 2 sqrt(J theta / T) s for
theta = 0.52 rad, so tens of seconds for a small wheel and under ten for a large one) happens first and is then followed by
the tail, so a wheel that is ten times stronger shortens the early part of the slew but moves the 1 % time hardly at all.
Settling therefore reads the controller (Kd/Kp) and not the actuator, which is why wheel class, and with it the largest
single mass lever, drops out of the frontier. The reviewer measured this on the committed data: corr(log settling,
log(Kd/Kp)) = 0.993 for large wheels.

**Definition.** `slew_time_s` = the first time at which the attitude error angle falls below a band of 1 degree, where the
error angle is 2 norm(q[:3]) in degrees, exactly the quantity `SimResult.summary()` computes as `theta_err_deg`; if the error
never falls below the band within the horizon the value is the horizon `t_end` (censored; such designs are not settled either).
First entry, not last exit: the time to arrive, not the time to remain. The reason for 1 degree: it is 1/30 of the 30 degree
slew (a tolerance within which a pointing slew would be considered arrived at), it is above the star-tracker floors (the
coarsest is a few hundredths of a degree) so it is not a sensor-floor measure, and it is reached when the fast, torque-limited
part of the slew is over, before the slow tail that sets the 1 % criterion (0.3 degree here). A second column
`slew_time_05deg_s` with a band of 0.5 degrees is recorded for sensitivity only, it is not an attribute of the fit; the
attribute is the 1 degree one, chosen here before any data is seen.

**Where it is computed.** Post-processing of the existing `SimResult` time histories (`t`, `q`) in the model layer
(`cubesat_model.measure`); `adcs_sim.py` is not touched and stays byte-identical. The SysML `analysis def ModelTest` documents
the outputs list; no constant is duplicated (the bands are scenario parameters of `measure`, like the slew angle).

**Expectation (stated in advance, to be compared with the data).**
1. Slew time depends on torque for small wheels at 30 degrees and on the gains otherwise. The small wheel (0.3 mN m cap) is
   saturated for about 5 times the share of the horizon that large wheels are (median saturated fraction 0.0409 against
   0.0080, ratio 5.1), so its first arrival is set by the bang-bang phase, roughly 2 sqrt(J theta / T) = 40 to 80 s at
   J = 0.25 to 1 kg m2, and larger J (larger panels) lengthens it. For medium and large wheels the cap is mostly not reached
   and the arrival is set by the PD response: time scale between J/Kd and 4 Kd/Kp times a few, so it moves with the gains.
2. Wheel-class medians (feasible designs). Slew time: small about 70 s, medium about 35 s, large about 35 s (small
   at least 1.5 times large; medium and large within 30 % of each other). Settling (existing, 128 / 67 / 69 s) stays as it is:
   it compresses the class differences, so the small/large ratio of slew time (about 2) is larger than that of settling (1.85),
   and the slew time is below settling in every class (slew time about half of settling for medium and large).
3. Slew time and settling are positively correlated but not redundant: I expect a correlation of the oriented log-metrics of
   0.5 to 0.8 over the feasible set.
4. Whether mass enters the frontier is open and not predicted to follow. If the small-wheel saturated phase now separates
   designs, the (oriented) slew time of small, light wheels is worse than that of large, heavy wheels, a slew-time/mass tension
   at the wheel class; if the weight of that effect is small against the panel and battery mass, mass stays absent and wheel
   class is reported as a feasibility boundary. Either result is recorded as found.

### Amendment 4: results (adjustment 4, the last; STOP RULE TRIGGERED, R-13 still fails)

Command (recorded, run after the model layer change): `uv run python examples/adcs/generate_dataset.py --model cubesat --n 1000
--seed 0 --slew-deg 30 --t-end 600 --force`. All earlier columns are unchanged to 1e-6 relative; two columns added
(`slew_time_s`, `slew_time_05deg_s`); the band never entered within 600 s for 4 designs (censored at the horizon). Feasible 780
of 1000 (small 239, medium 279, large 262); violation shares unchanged (settled 2.2 %, `momentum_ok` 8.1 %, `power_ok` 0 %,
`dod_ok` 13.1 %). Conditioning, method and thresholds as before, now with ten attributes (slew time oriented reciprocal).

Wheel-class medians on the feasible set:

| class | saturated fraction | slew time 1 deg (s) | slew time 0.5 deg (s) | settling 1 % (s) | slew/settling |
|---|---|---|---|---|---|
| small | 0.0409 | 82.7 | 97.1 | 128.3 | 0.74 |
| medium | 0.0152 | 50.7 | 60.2 | 67.1 | 0.74 |
| large | 0.0080 | 51.8 | 62.3 | 69.3 | 0.75 |

R-14 holds: saturation ratio small/large 5.1 (needs 3), settling ratio 1.85 (needs 1.25); slew time ratio 1.60.

R-13 on the ten attributes (n = 780):
- Contending set at tau = infinity (size 6): control effort 0.434, slew time 0.253, power margin 0.179, settling 0.081, pointing 0.040,
  eclipse reserve 0.013; total mass 0.000, energy balance 0.000, peak slew power 0, depth of discharge 0.
- Working tau = 42.8 (`frac_above_` 0.101), exponents: effort 0.430, slew time 0.329, power margin 0.176, settling 0.028,
  pointing 0.024, reserve 0.013, mass 0. Near-frontier rows 102: small 78, medium 23, large 1.
- Bootstrap (100 resamples, seed 0) support / median exponent: slew time 1.00 / 0.252, effort 1.00 / 0.429, pointing 0.95 / 0.041,
  settling 0.88 / 0.081, power margin 0.66 / 0.155, reserve 0.58 / 0.012, energy balance 0.50 / 0.015, depth of discharge 0.43 / 0,
  total mass 0.00 / 0, peak slew power 0.
- Near-frontier associations (negative = tension): settling-slew time +0.99; settling-mass -0.13; slew time-mass -0.11;
  settling-effort -0.95; slew time-effort -0.96; pointing-effort -0.70; pointing-mass -0.36; pointing-peak slew power -0.61;
  settling-pointing +0.68; slew time-pointing +0.71; mass-depth of discharge -0.65; mass-reserve -0.58; mass-power margin -0.47;
  mass-energy balance -0.44; mass-peak slew power +0.65; power margin-energy balance +0.99; reserve-depth of discharge +0.93.
- (a) FAILS: the set has size 6 and includes a power attribute (power margin 0.179), but total mass has exponent 0.000 (needs 0.05).
  (b) FAILS: mass bootstrap support 0.00 (needs 0.90). (c) FAILS: settling-mass -0.13 and slew time-mass -0.11, both above -0.30,
  and only the small (78) and medium (23) classes have 10 or more near-frontier designs, which would meet the class count but not
  the association. (d) holds (mass with depth of discharge -0.65). (e) now holds (settling-effort -0.95, pointing-effort -0.70,
  pointing-mass -0.36, settling-pointing +0.68; the pointing-mass clause that failed at -0.26 passes at -0.36 because the
  near-frontier set is different with the new attribute). `test_e_previous_tensions_retained` therefore has no xfail marker;
  `test_a_`, `test_b_`, `test_c_` stay `xfail(strict=True)` citing amendment 4.
- Sensitivity, 0.5 degree band in place of 1 degree: same contending set, mass exponent 0.000, slew time-mass -0.056,
  settling-mass -0.066, near-frontier small 77, medium 22, large 2. The band does not matter.

**Expectation against result (Step A).** Held: medium and large slew times are indistinguishable (50.7 against 51.8 s); small wheels
are the slow class (ratio 1.60 against the predicted at least 1.5); wheel-class medians of settling unchanged. Wrong: levels (small
82.7 s against 70 predicted; medium and large 51 s against 35); slew time is about three quarters of settling in every class, not
half, and its ratio small/large (1.60) is smaller than that of settling (1.85), not larger; slew time and settling are almost
redundant (correlation 0.947 over the feasible set, 0.99 near the frontier), not 0.5 to 0.8. The reason I got wrong: a 1 degree band
at a 30 degree slew is 1/30 of the initial error, 3.4 time constants of the slow pole against 4.6 for the 1 % criterion, so the
two are in the same tail and ln 30 / ln 100 = 0.74 is exactly the ratio seen. corr(log slew time, log(Kd/Kp)) = 0.998 for large
wheels, 0.990 for medium, 0.971 for small (settling: 0.992, 0.924, 0.707). Only at the most aggressive gains (Kd/Kp below 5) does
the wheel class show: slew time small 35.4 s, medium 29.5 s, large 28.0 s (settling 88, 41, 37 s). The torque-limited part of the
slew is short against the tail even for small wheels at 30 degrees, so a first-entry measure with a band of this size does not
escape the slow pole.

**Finding (reported, not tuned around).** Wheel class appears as a feasibility boundary (momentum: small wheels lose 19 % of the
designs at 30 degrees, 98 % at 90 degrees) and not as a frontier tension. Agility measured by slew time does not trade against mass:
its association with mass is -0.11 (-0.056 at 0.5 degree) and total mass has exponent 0.000 and bootstrap support 0.00, as settling
did. The statement for the notebook: on this case the mass-agility trade of the wheel class is a feasibility boundary; the
frontier tensions are control effort against agility, pointing against effort and mass, and the energy-sizing ones (mass against
depth of discharge, reserve and power margin). No further lever is used.

### Amendment 5: three levers (reasoning written and committed before any simulation or any new column)

Supervisor choice: "try both new levers then report back" (`work-packages/WP4b-decisions.md`, amendment 5). Momentum stays
enforced (feasible = settled and `power_ok` and `momentum_ok`, every attribute positive); the clauses and thresholds of R-13 and
R-14 are unchanged and the same hand probe (the tests of `tests/test_adcs_enrichment.py`, parametrized over the dataset) runs on
each dataset. The 30 degree baseline `adcs_designs_cubesat.csv` is not touched; new datasets go beside it. Everything in this
section is written before the new dataset is simulated and before the headroom attribute is computed on any row. The only
numbers used are non-dynamic ones: the slew-axis inertia of the sampled designs (accounting only, no `simulate_adcs`) and
closed-form bounds.

**Lever (i): aggressive-gain regime. Deriving the box.**

1. Linearised loop (q_vec = theta/2 as in Amendment 3): J theta'' + Kd theta' + (Kp/4) theta = 0. Damping ratio
   zeta = Kd / sqrt(J Kp); the slow pole when overdamped is Kp/(4 Kd), so the settling timescale is 4 Kd/Kp s and a 1 % settling
   takes 4.6 of those, a 1 degree arrival (1/30 of the slew) 3.4 of them.
2. The torque-limited (bang-bang) part of a rest-to-rest slew of theta = 0.52 rad takes about 2 sqrt(J theta / T). At the median
   inertia of the sampled designs (J = 0.36 kg m2; range 0.23 to 0.99) that is about 50 s for a small wheel (T = 0.3 mN m),
   19 s for a medium (2 mN m) and 8.5 s for a large (10 mN m). Wheel class can separate arrival time only when the PD tail
   (3.4 x 4 Kd/Kp = 13.6 Kd/Kp s) is not longer than these times, otherwise the tail hides the class, which is what Amendment 4
   found: at the baseline box the median Kd/Kp is 3.9 and the tail is about 53 s, longer than the bang-bang time of medium and
   large wheels. So the box must put Kd/Kp mostly at or below about 5 and, to make the demand exceed the cap of every class from the
   first instant, put the proportional torque Kp/2 sin(theta/2) = 0.13 Kp above 10 mN m (Kp above 0.08) so that all three
   wheels are torque-limited during the slew and the class sets the speed.
3. Damping must stay sensible for the whole inertia range: stability holds for any positive gains, but a very underdamped loop
   rings (long settling that is not a wheel effect and larger momentum reversals). Requirement: zeta of at least 0.5 for the
   large majority of the box over J = 0.23 to 0.99, and overdamping not so deep that the slow pole returns.
4. Chosen box (ranges, log-uniform as the baseline): **Kp 0.2 to 2.0 N m/rad, Kd 0.3 to 1.5 N m s/rad** (baseline: Kp 0.03 to 1.0,
   Kd 0.3 to 1.5: the Kd range is kept, the Kp floor is raised by 6.7 and its ceiling by 2). Computed on the inertias of the 1000
   sampled designs with independent log-uniform Kp, Kd: Kd/Kp at or below 5 for 97.8 % of the box (baseline 57 %), at or below 2
   for 76 %, at or below 1 for 47 %, median 1.07 (baseline 3.9); zeta at or above 0.7 for 84 %, below 0.5 for 5.3 %, below 1
   (underdamped) for 33 %. The slow-pole time constant 4 Kd/Kp has median 4.3 s (baseline 15.5 s). Other boxes were computed
   on paper only (Kp 0.1 to 1.0 with Kd 0.1 to 1.0: zeta below 0.3 for 8 %; Kp 0.3 to 3.0 with Kd 0.4 to 1.5: 100 % at or below 5
   but demand three times above the cap); this one was taken as the compromise, not tuned against any outcome.
5. Where it lives: the SysML model gets a second design-space part, `part def AggressiveGainSpace :> DesignSpace` redefining
   `KpMin`, `KpMax`, `KdMin`, `KdMax`, and `part aggressiveGains : AggressiveGainSpace`; the Python reads whichever part is selected
   (`gain_box="baseline"` default or `"aggressive"`), no number enters Python. Generator flag `--gain-box {baseline,aggressive}`;
   the aggressive dataset is written to `adcs_designs_cubesat_gains.csv`, the baseline default is unchanged.
6. Scenario unchanged: 30 degrees, wheels as committed (10 / 30 / 100 mN m s, 0.3 / 2 / 10 mN m). Horizon: the worst corner
   (Kd/Kp = 7.5) has a 1 % settling of 4.6 x 30 s = 138 s, so 300 s would suffice, but the horizon is kept at 600 s for
   comparability and because it costs nothing in the results.
7. Command (recorded): `uv run python examples/adcs/generate_dataset.py --model cubesat --gain-box aggressive --n 1000 --seed 0
   --slew-deg 30 --t-end 600 --force`. The designs are sampled with the same seed and the same enumerations; the sampler draws Kp, Kd from the
   chosen box, so the wheel, tracker, span and battery columns of design i are identical to the baseline's (same child seeds, the
   Kp, Kd draws differ because the range changed).

**Expected consequences of lever (i), stated before the data.**
- More torque saturation for every class: the demand is 26 to 260 mN m at the first instant, above every cap. The median
  saturated fraction of the horizon rises for all classes; the small/large ratio of R-14 may shrink (large wheels saturate far
  more than at baseline), so R-14 clause 1 (small at least 3 times large) is at risk and is evaluated, not assumed.
- More momentum violations for small wheels: with the demand always saturated the slew is bang-bang with little early braking,
  so the bound of Amendment 3 (peak momentum sqrt(T J theta) against the capacity, J of at most h_max^2/(T theta)) applies
  almost exactly: J at most 0.64 for small wheels, 0.86 for medium, 1.9 for large. The share of the sampled inertias above those
  bounds is 18 % (small), 6 % (medium), 0 % (large); the baseline observed 19.2 %, 4.3 % and 0, so the bound is accurate. Underdamped
  overshoot (33 % of the box) adds reversal momentum. Estimate: `momentum_ok` violated for about 25 % of small designs (range 20
  to 35), about 7 % of medium (5 to 12), about 0 to 1 % of large; feasible share overall about 75 % (70 to 80).
- Agility by wheel class: median 1 degree slew time about 55 to 65 s small, 25 to 30 s medium, 15 to 20 s large (small/large near
  3, against 1.6 at baseline); the PD tail still adds a few times 4 Kd/Kp. Settling still carries the slow pole, so its class ratio
  stays modest (about 1.5 to 2.5).
- Whether mass enters the frontier: open. Wheel class explains 55 % of the variance of total mass and, with this box, much of the
  variance of slew time, so a negative slew time-mass association near the frontier (heavier wheel, faster) of -0.3 to -0.5 is
  plausible and total mass entering the contending set at tau = infinity is possible, but the frontier is selected on ten
  attributes, and control effort and the pointing attribute (which now improves with Kp) are expected to keep dominating. I do not predict a pass.

**Lever (ii): momentum headroom attribute. Choice and orientation.**

- Definition: `momentum_utilisation` = `peak_momentum_nms` / wheel capacity (`maxMomentum` of the design's wheel class), the
  fraction of the momentum storage used by the slew. **Smaller is better** (more headroom for the same slew), so it is oriented
  with the reciprocal like the other smaller-is-better attributes (u = -log utilisation). For feasible designs `momentum_ok` is
  exactly utilisation at most 1, so it lies in (0, 1] on the feasible set and its log is finite and bounded above by 0.
- Why a ratio and not capacity minus peak: the ratio is dimensionless and bounded, it is the physical margin of the existing
  `momentum_ok` flag (utilisation at most 1), and it treats a small wheel run at 90 % the same as a large wheel run at 90 %. The
  difference is dominated by capacity (10 / 30 / 100 mN m s, a factor 10), so it would simply rank the classes and put mass on
  the frontier by construction, which tests the wheel table and not the trade. With the bang-bang formulas the ratio is
  1.25 sqrt(J), 1.07 sqrt(J), 0.72 sqrt(J) for small, medium, large (J in kg m2), a factor 1.7 between the extreme classes, which
  is a margin that wheel class moves without fixing it. As a sensitivity only (declared now, not an attribute of the verdict, like the
  0.5 degree band of Amendment 4) the difference capacity minus peak is also evaluated once on the datasets where the ratio is used.
- Where it lives: a function in the model layer, `cubesat_model.add_momentum_utilisation(df, capacities)`, with
  `CubesatModel.wheel_capacities()` reading the capacities of the wheel classes from the SysML model through the client
  (`maxMomentum` of each wheel part def). The committed CSVs are not rewritten; the column is derived when a dataset is read.
- Expectation (before the data): on the 30 degree baseline dataset the PD law is not saturated for most medium and large wheels, so
  peak momentum is set by the response (inertia and gains) and not by the wheel; utilisation is then mostly inversely proportional to the capacity,
  heavy wheels have a low utilisation and a high mass: a negative utilisation-mass association is plausible, but the wheel class
  also acts only as a factor 10 in capacity against a factor 5 in mass, so the margin does not make wheel class a frontier trade
  alone. I expect lever (ii) alone to fail R-13 (mass exponent below 0.05 or association above -0.30) but I do not know.

**Lever (iii): both.** The aggressive-gain dataset with the utilisation attribute (eleven attributes). Lever (i) moves the speed of
the class, lever (ii) its momentum margin; together heavy wheels would be fast and have low utilisation while light ones are slow and near their
capacity, which is a mass-against-agility-and-headroom trade by construction of the physics. This is the lever most likely to
change the answer; the expectation is a pass of (c) at best and a mass exponent above 0.05 only if the effort attribute does not absorb it.

**Reporting.** For each lever the probe note will carry: feasible per class, the contending set at tau = infinity with exponents, the
mass exponent and its bootstrap support (100 resamples, seed 0), the settling-mass and slew time-mass associations pooled over the
near-frontier rows at the working tau, and the near-frontier counts per class. STOP RULE after lever (iii): if R-13 fails on all
datasets the finding is recorded as the amendment to R-13 (for which lever mass entered the contending set and with what
exponent; whether wheel class is a feasibility boundary or not) and the failing tests are `xfail(strict=True)` per dataset; if
R-13 passes under a lever, that dataset's tests carry no xfail.

### Amendment 5: results (levers i, ii, iii; R-13 PASSES under lever i and lever iii, FAILS under lever ii)

Commands (recorded, run after the reasoning commit `75823dc`): the aggressive-gain dataset
`uv run python examples/adcs/generate_dataset.py --model cubesat --gain-box aggressive --n 1000 --seed 0 --slew-deg 30 --t-end 600 --force`
writes `examples/adcs/data/adcs_designs_cubesat_gains.csv` (same 35 columns as the baseline; wheel, tracker, span and battery columns identical
to the baseline's, only Kp, Kd differ). The baseline `adcs_designs_cubesat.csv` is untouched. The utilisation attribute is derived on read
(`cubesat_model.add_momentum_utilisation(df, CubesatModel.wheel_capacities())`, capacities 10 / 30 / 100 mN m s read from the model through
the client); no CSV was rewritten. Method, conditioning, bootstrap (100 resamples, seed 0) and thresholds as before; the tests of
`tests/test_adcs_enrichment.py` run the same R-13/R-14/R-15 checks over the four datasets (`baseline`, `headroom` = lever ii, `gains` =
lever i, `gains_headroom` = lever iii). Reproducibility: `tests/test_cubesat_model.py -k reproduc` regenerates the first 20 designs of both CSVs
with the WP4 per-column tolerances (relative 1e-4; for the aggressive box 1e-3 on the continuous columns, because the CI runner differed from the author's platform by 1.25e-4 in the control effort of one design, and by 6.2 % in the saturated fraction, for which the aggressive box allows 10 % instead of 2 %: the saturated trajectories are more platform-sensitive) and checks same-platform exactness for both gain boxes.

| | baseline (10 attr.) | lever ii: baseline + utilisation (11) | lever i: aggressive gains (10) | lever iii: gains + utilisation (11) |
|---|---|---|---|---|
| feasible n (small / medium / large) | 780 (239 / 279 / 262) | 780 (239 / 279 / 262) | 706 (191 / 248 / 267) | 706 (191 / 248 / 267) |
| momentum violated (small / medium / large) | 19.2 / 4.3 / 0 % | same | 37.2 / 17.4 / 0 % (overall 18.8 %) | same |
| contending set at tau = inf (size) | 6: effort .434, slew .253, power margin .179, settling .081, pointing .040, reserve .013 | 8: slew .304, effort .296, power margin .193, utilisation .086, mass .060, pointing .030, depth of discharge .027, reserve .005 | 6: slew .201, mass .223, energy balance .169, effort .143, pointing .135, depth of discharge .129 | 6: mass .249, utilisation .214, power margin .170, slew .141, depth of discharge .122, pointing .104 |
| total mass exponent at tau = inf / working tau | 0.000 / 0 | 0.060 / 0.077 | 0.223 / 0.179 | 0.249 / 0.259 |
| bootstrap support of mass (median exponent) | 0.00 (0) | 0.99 (0.060) | 1.00 (0.200) | 1.00 (0.249) |
| working tau, near-frontier rows (small / medium / large) | 42.8, 102 (78 / 23 / 1) | 51.4, 80 (15 / 41 / 24) | 35.2, 64 (21 / 36 / 7) | 58.8, 80 (0 / 49 / 31) |
| settling-mass association (near-frontier, pooled) | -0.129 | -0.126 | -0.503 | -0.329 |
| slew time-mass association | -0.109 | -0.078 | -0.453 | -0.139 |
| pointing-mass / settling-effort / pointing-effort / settling-pointing | -0.357 / -0.951 / -0.701 / +0.681 | -0.114 / -0.956 / -0.742 / +0.716 | -0.658 / -0.659 / -0.349 / +0.143 | -0.539 / -0.390 / -0.464 / +0.183 |
| strongest power tension (d) | depth of discharge-mass -0.65 | depth of discharge-mass -0.59 | peak slew power-settling -0.67 | peak slew power-utilisation -0.57 |
| utilisation associations (mass / slew / effort / settling) | n/a | -0.362 / -0.800 / +0.747 / -0.746 | n/a | -0.328 / -0.661 / +0.612 / -0.232 |
| R-14: saturated ratio small/large (needs 3), settling ratio (needs 1.25) | 5.12, 1.85 (holds) | same | 13.1, 4.85 (holds) | same |
| (a) (b) (c) (d) (e) | fail fail fail pass pass | pass pass FAIL pass FAIL | pass pass pass pass pass | pass pass pass pass pass |

Medians on the feasible set (small / medium / large). Baseline: saturated fraction 0.041 / 0.015 / 0.008, settling 128 / 67 / 69 s, slew time 83 / 51 / 52 s.
Aggressive gains: saturated fraction 0.165 / 0.044 / 0.013, settling 104 / 41 / 21 s, 1 degree slew time 33 / 18 / 14 s, total mass 12.65 / 13.31 / 14.46 kg.
Utilisation medians: baseline small 0.587, medium 0.38, large 0.13; gains 0.807, 0.638, 0.358. In the aggressive box the correlation of log slew
time with log(Kd/Kp) falls to 0.79 (small), 0.89 (medium), 0.97 (large) (baseline 0.971, 0.990, 0.998), the slew time and settling correlation
to 0.698 (baseline 0.947), and wheel mass explains 65 % of the variance of total mass.

**Reading, lever by lever.**
- Lever (i), aggressive gains: R-13 holds in full (a: size 6 with mass 0.223 and a power attribute, depth of discharge 0.129 and energy balance
  0.169; b: mass bootstrap support 1.00 with median 0.200; c: settling-mass -0.503 and slew time-mass -0.453, two classes with at least 10
  near-frontier rows (medium 36, small 21); d, e). The mechanism was the one reasoned in advance: with the proportional demand above every wheel
  cap and Kd/Kp mostly at or below 5, the class sets the arrival time (slew 33 / 18 / 14 s, a ratio 2.4 small/large against 1.6), so a
  heavier wheel buys a faster slew, and mass becomes a frontier attribute (heavier wheels are faster and cost mass). Wheel class is now both a
  feasibility boundary (37 % of small designs fail on momentum) and a frontier trade.
- Lever (ii), utilisation alone: mass enters the contending set (0.060, bootstrap support 0.99, median 0.060, so (a) and (b) hold) and the
  new attribute is itself in it (0.086, support 1.0), but the agility-mass associations stay at -0.126 and -0.078 (c fails) and the pointing-mass
  association falls to -0.114 (e fails: the near-frontier set shifts to medium and large wheels, 41 and 24 rows). Utilisation is
  tied to the mass (-0.362) and the slew (-0.800) but not strongly enough to make the agility trade appear at the baseline gains. Sensitivity
  (declared before): the headroom difference (capacity minus peak) in place of the ratio gives mass exponent 0.025, support 0.99, settling-mass -0.253,
  slew time-mass -0.238 (c still fails by a margin), pointing-mass -0.186 (e fails), so the choice of form does not change the verdict at
  the baseline gains; on the aggressive gains the difference gives mass 0.282, settling-mass -0.476, slew time-mass -0.371 (all pass).
- Lever (iii), both: R-13 holds in full (mass 0.249, support 1.00; settling-mass -0.329 passes (c) while slew time-mass is only -0.139; near-frontier
  rows medium 49, large 31, small 0). Utilisation adds a second, correlated wheel-class attribute and removes the small wheels from the near
  frontier. Lever (i) already suffices; the headroom attribute is not needed.

**Expectation against result (Step A of amendment 5).** Held: heavier wheels are faster and the class separates agility in the aggressive box; mass enters
the contending set under lever (i); lever (ii) alone does not pass (the prediction "fails" held, though (a) and (b) pass, only (c) and (e) fail); R-14
clause 1 held (ratio 13.1, my concern that it would shrink was wrong: the small wheel saturates for 16 % of the horizon against 1.3 % for the large).
Wrong in size: the momentum violations (small 37 %, medium 17 %, against my 25 % and 7 %; the closed-form bound gave 18 % and 6 % and
the underdamped overshoot added much more than I allowed for); the slew times (33 / 18 / 14 s against 55 to 65, 25 to 30, 15 to 20 s, because the
fraction of high Kp is larger and the PD braking starts earlier than a bang-bang); the feasible share (706 of 1000 = 70.6 % against about 75 %).
The associations are larger than I guessed (-0.45 to -0.50 against -0.3 to -0.5, within it).

**Disposition (stop rule after lever iii).** R-13 passes under lever (i) and lever (iii) with no change of clause or threshold, so the stop
rule does not apply to those datasets: their tests carry no `xfail`. R-13 fails under the baseline (a, b, c; amendment 4) and under lever (ii)
(c, e) on the 30 degree baseline gains: those tests are `xfail(strict=True)` per dataset (`EXPECTED_FAIL` in `tests/test_adcs_enrichment.py`).
Finding for the supervisor: the richness failure of amendment 4 is a property of the gain box, not of the case or the measures: at the committed
box (median Kd/Kp 3.9) the slow pole hides the wheel class; in the aggressive box (median Kd/Kp 1.07) it appears as a frontier tension (mass
exponent 0.22, support 1.00) and the wheel class is both a feasibility boundary and a frontier trade. Which dataset stands (the baseline or
`adcs_designs_cubesat_gains.csv`) is the supervisor's choice; WP7 and the notebook read it. Caveats: the aggressive box is a stiffer
attitude loop than the baseline and the choice of the box was reasoned from the physics but is still a choice of the case; in the gains datasets
the large-wheel near-frontier count is 7 (lever i) so large-wheel statements are weak there; 18.8 % of the aggressive designs fail momentum (small
wheels 37 %).

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

R-13 (all of a to e) holds on the final dataset. R-14 was amended (WP4b scope amendment 1, recorded in
`work-packages/WP4b-decisions.md`): the absolute small-wheel level of 0.25 was an arbitrary default of the scope and is
dropped; R-14 keeps its two relative clauses. Final numbers on the committed dataset: median `torque_saturated_frac` of
small-wheel designs 0.237 (large wheels 0.0139, ratio about 17 against the required 3); median settling 247 s small
against 76 s large, ratio 3.2 against the required 1.25. Both relative clauses hold. No new simulation was run and the
dataset is unchanged. The test `test_torque_binds_for_small_wheels` carries no xfail marker and no longer asserts the
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

### Final constants and scenario (all illustrative; superseded by amendment 3: slew 30 degrees, horizon 600 s, wheel momentum 10 / 30 / 100 mN m s)

Unchanged from the defaults list except: Kp 0.03 to 1.0 N.m/rad, Kd 0.3 to 1.5 N.m.s/rad (log-uniform); small wheel
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

### R-13 on the committed dataset (feasible designs, n = 772; conditioning as in the Method section)

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

### Physical explanation of the exposed tensions (R-17)

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
over the span range, battery adds 0.02); median about 0.5. The panel contribution scales like span^3.

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
appear as a frontier tension. Wheel class moves total mass by at most 3 x 0.48 = 1.4 kg of about 14 kg, while panel span,
battery capacity and tracker grade move it by several kg; and the settling time at the 1 % criterion is set by the slow pole
Kp / (4 Kd) of the gains rather than by the torque-limited phase (median settling: small 128 s, medium 67 s, large 69 s; medium
and large are indistinguishable). Where wheel class does act, it acts as a feasibility boundary: small wheels fail on momentum
for large-inertia designs (19 % of small designs at 30 degrees, 98 % at 90 degrees), not as a spread along the frontier. The
notebook should say so.

### Facts for WP7 interpretation

Updated for amendment 3 (dataset at 30 degrees, 600 s; feasible = settled, `power_ok`, `momentum_ok`, all attributes positive;
780 of 1000 designs). The amendment 2 section above describes the earlier 90 degree dataset and is superseded numerically.

(a) Power never limits a slew in this dataset. The available-power cap on torque is below the wheel maximum in 3.2 % of
designs (large wheels with the smallest panels), and `power_ok` is True for every design. The power attributes reach the
controls only through mass and inertia (panel and battery mass, lever arm), so power tensions are energy-sizing tensions, not
power-limited-slew tensions. On the feasible set the power margin is 7.0 to 68 W (median 27.6 W).

(b) Near-redundant attribute pairs, so that WP7 does not read them as independent findings: power margin with energy balance
(correlation 0.966 of the oriented, standardized metrics on the new feasible set) and eclipse reserve with eclipse depth of
discharge (0.921) are accounting near-identities, not separate findings.

(c) Wheel classes on the feasible set: small 239, medium 279, large 262 (of 344, 345, 311). Near-frontier rows at the working
tau (46.1): small 56, medium 16, large 4, so the frontier is mostly small-wheel designs and statements about large wheels rest
on 4 near-frontier rows. Total mass (11.9 to 16.1 kg over the feasible set) is not in the tau = inf contending set (exponent
0.000; bootstrap support 0.01): WP7 must read this as "mass is not a discriminating attribute on this frontier", not "mass
does not matter"; it does associate with the energy attributes near the frontier (with depth of discharge -0.57, with
eclipse reserve -0.46, with energy balance and power margin -0.35).

(d) R-13 a, b, c and the pointing-mass clause of e fail on this set (see "Every attempt"); R-14 (torque binds: saturated
fraction small 0.0409 against large 0.0080, ratio 5.1; settling small 128 s against large 69 s, ratio 1.85) and the R-15 shares
pass. The tensions that hold: settling time with control effort (-0.95), pointing error with control effort (-0.63), settling
with pointing aligned (+0.63), power tensions (mass with depth of discharge -0.57, pointing with peak slew power -0.50).
Wheel class acts as a feasibility boundary (small wheels lose 19 % of designs to momentum), not as a frontier tension.

### What the SysML client provided for free (R-17)

Strict loading with diagnostics and `self_check` (a typo in the model is an error, not a silently wrong number);
instantiation of 10 configurations per load with all derived accounting (masses, generated and available power, usable
torque) computed by the model's `calc def`s; unit-aware arithmetic and the compound-unit checks of the accounting;
per-configuration constraint verification (`power_ok`, `dod_ok`); `run_sweep` for the panel-span grid check; enumeration
and specialization reads that removed every wheel or tracker table and every range from the Python. Costs: a runtime
download on first use, about 3.5 ms per instantiated cubesat, and a `fork` warning from the gRPC library when the generator's
pool is used (the pool is spawned, each worker opening its own connection, so it is harmless).

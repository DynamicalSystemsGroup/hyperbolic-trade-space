# WP4b — Scope of work: ADCS case enrichment as a coherent illustrative satellite model

| | |
|---|---|
| **Status** | DRAFT (draft 2). Approved only by the recorded act below. Nothing in this package is executed before then. |
| **Supervisor (accountable)** | mzargham |
| **Repository** | `DynamicalSystemsGroup/posynomial-invariant-form` (local: `/Users/z/Documents/GitHub/posynomial-invariant-form`) |
| **Approval record** | Verbal approval in chat, quoted verbatim in `work-packages/WP4b-decisions.md` |
| **Acceptance record** | Verbal acceptance in chat, quoted verbatim in `work-packages/WP4b-decisions.md`, after the review report `work-packages/WP4b-review.md` |

## Purpose

The supervisor requires the example case to be rich enough that the fitted model exposes tensions that were not
asserted a priori and that are recognizable and intuitive once explained (spec §8). The probe of the accepted WP4
dataset (`docs/superpowers/notes/adcs-tensions-probe.md`) found settling vs effort, pointing vs effort and pointing
vs mass (through star-tracker grade), with settling and pointing aligned, but not agility vs mass through wheel class:
mass was nearly inert in the contending set (exponent 0.006 at τ = ∞), torque limits bound only about 7 % of the time for
small wheels and under 1 % for large wheels, and wheel class moved the median settling time only from 301 s to 264 s.

The supervisor's decision (recorded verbatim in `WP4b-decisions.md`) is to treat this as a modelling task, not a
scenario tweak: "do both mass and power, sizing the solar panels impacts the power generation, batterys for storage, mass
and power effect the controls most naturally. can also add star tracker grade. the whole sysml model for the satelite
illustrative but it should make sense. and the modeling language with abstract and concrete parts lines up really nicely
with sampling the space (configuring) then running model testing to get the measurements". WP4b therefore builds a
coherent, illustrative satellite model: abstract part definitions (satellite, bus, solar panel, battery, reaction
wheel, star tracker, controller), concrete configurations sampled from the design space, and a model test that
measures each configuration, mirroring the pipeline of spec §3 (sample the configuration, evaluate, obtain attributes).
Solar-panel sizing feeds both power generation and the inertia (through the existing `adcs_sim` inertia model), the
battery feeds mass and stored energy, and mass and power reach the controls through the physics. The dataset is then
regenerated and the case's richness is checked in the spec's terms.

## Goals

- G1. An illustrative satellite model, additive to the WP4 design-space and evaluation layer, whose design variables are solar-panel sizing, battery capacity, wheel class, star-tracker grade and the controller gains, and whose couplings to the controls are explicit and physical.
- G2. Measured attributes that the model can justify: settling time, pointing error, total mass, control effort and the power attribute(s) fixed by the open decisions, plus feasibility flags.
- G3. A slew scenario large enough that torque limits bind, so that wheel class trades agility against mass.
- G4. A SysML v2 text model of the satellite with abstract part definitions and a description of concrete configurations as sampled instances and of the analysis as the model test, documentation only, that reads as a sensible satellite.
- G5. A new committed, seed-stable dataset beside the original, and tests that make the case's richness a checked property (the probe's acceptance conditions as tests).
- G6. The probe note records the diagnosis, every modelling choice and lever tried, the results, and the physical explanation of each exposed tension.

## Non-goals

- No change to the simulator port `examples/adcs/adcs_sim.py` (physics, inertia function, controller): it stays byte-identical; the new mass, power and energy accounting lives in the design-space and evaluation layer, and panel and bus parameters flow into the existing inertia function through its existing parameters.
- No change to the estimator, solvers, coordinates, the analysis toolkit (WP2, WP3) or the notebook (WP7).
- No rewrite or replacement of the WP4 deliverables: the original CSV, its tests and the generator's default behaviour are unchanged.
- No calibration to real hardware and no claim of engineering fidelity: every new number is labelled illustrative and held to the plausibility rule.
- No orbit propagation, thermal, structural or full power-system model: the power and energy accounting is a coarse budget.
- No selection of which tensions should appear beyond the conditions of R-9.
- No new dependencies.

## Deliverables

| ID | Deliverable | Serves |
|---|---|---|
| D-1 | `examples/adcs/satellite_model.py`: abstract parts as dataclasses (satellite, bus, solar panel, battery, reaction wheel, star tracker, controller), their illustrative constants, mass and power accounting, and `measure(configuration)` (the model test) that calls the existing simulator | G1, G2, G3 |
| D-2 | `examples/adcs/design_space.py`: additive sampling of the new design variables (concrete configurations) and the enriched wheel set; existing functions and defaults unchanged | G1 |
| D-3 | `examples/adcs/generate_dataset.py`: additive flags selecting the satellite model and scenario; default behaviour unchanged | G5 |
| D-4 | `examples/adcs/data/adcs_designs_satellite.csv`: committed dataset, seed 0 | G5 |
| D-5 | `examples/adcs/satellite_model.sysml` (documentation only) and the update of `extended_design_space.sysml` to point to it | G4 |
| D-6 | `tests/test_satellite_model.py` (accounting, couplings, reproducibility) and `tests/test_adcs_enrichment.py` (the probe's acceptance conditions on the committed dataset) | G2, G5 |
| D-7 | `docs/superpowers/notes/adcs-tensions-probe.md` updated | G6 |
| D-8 | `work-packages/WP4b-decisions.md` (approval record) | G1–G6 |

## Requirements

| ID | Requirement | Checked by |
|---|---|---|
| R-1 | `examples/adcs/adcs_sim.py` is byte-identical to its WP4 state, and every WP4 test (inertia, regression pins at 78.0, 87.4, 120.5 and 310.6 s, port and design-space tests) passes unchanged | `git diff <start>..HEAD -- examples/adcs/adcs_sim.py` empty; `uv run pytest tests/test_adcs_case.py` |
| R-2 | The extensions are additive: with default options `evaluate_design`, `sample_designs` and `generate_dataset.py` produce exactly the WP4 results, and the original CSV is unchanged | the existing WP4 reproducibility tests pass; `git diff` shows `adcs_designs.csv` untouched; a test of the defaults |
| R-3 | Abstract parts and concrete configurations: each abstract part is a frozen dataclass with typed, unit-documented fields and illustrative constants; a concrete configuration is an instance obtained by sampling; the SysML text declares the same parts, attributes and units | inspection; `test_satellite_model.py` (fields and units present; SysML names match the dataclasses) |
| R-4 | Panel coupling: panel area (span and fixed chord) sets panel mass through an areal density that reproduces the baseline panel (2.5 m × 0.9 m, 30 kg) and sets the generated power; the panel span and mass flow into the existing `inertia_tensor` through its `panelSpan` and `panelMass` parameters, so that increasing the span increases Jxx and Jzz and slows the slew | `test_satellite_model.py`: monotonicity of inertia and of settling time with span on fixed other variables; generated power proportional to area |
| R-5 | Battery coupling: battery capacity (Wh) sets battery mass (through an illustrative specific energy), adds to the bus mass passed to `inertia_tensor`, and sets the stored energy used by the energy accounting | `test_satellite_model.py`: mass and inertia increase with capacity; the baseline configuration reproduces the WP4 baseline inertia (327.14, 107.48, 303.45) to 0.01 |
| R-6 | Power reaches the controls: the electrical power available for the wheels (generation minus housekeeping and sensor loads) caps the usable wheel torque, passed to the simulator through the existing wheel argument of `make_config`, and the energy used during the slew enters the power attribute(s); both couplings are documented and tested | `test_satellite_model.py`: usable torque decreases when available power decreases; energy used is nonnegative and increases with slew angle |
| R-7 | Total mass is the sum of the bus (fixed illustrative mass), battery, both panels, antenna, three wheels, star tracker and IMU; the mass passed to the simulator's bus is consistent with it | `test_satellite_model.py` (accounting identity to 1e-9) |
| R-8 | Attributes and flags: `measure` returns `settling_time_s`, `pointing_error_deg`, `total_mass_kg`, `control_effort`, the power attribute(s) fixed by OD1, and the flags `settled`, `momentum_ok`, `torque_saturated_frac` and (per OD2) the depth-of-discharge flag or metric; all attributes finite and strictly positive on a batch; each attribute is documented with the mechanism through which it depends on each design variable | `test_satellite_model.py`; inspection of docstrings |
| R-9 | Richness acceptance on the committed dataset, conditioning the attributes by hand as in the probe note (reciprocal orientation for smaller-is-better attributes, log, standardize, settled designs only), fitting `HyperbolicTradeSpace` at τ = ∞ (`min_exponent = 0`) and at the working τ with `frac_above_` ≈ 0.10, and using near-frontier rows |log V| < 1/τ: (a) the contending set at τ = ∞ has size at least 3 and includes total mass and the power attribute(s) with exponents at least 0.05; (b) total mass and the power attribute(s) are in the support in at least 90 % of 100 bootstrap resamples, with median exponent at least 0.05; (c) the pooled near-frontier association of settling with total mass is at most −0.30 (agility against mass), with at least two wheel classes represented by at least 10 near-frontier designs each; (d) at least one tension involving power (power with mass, or power with settling) has near-frontier association at most −0.30; (e) the previously exposed tensions are retained: settling–effort, pointing–effort and pointing–mass associations are each at most −0.30, and settling–pointing is not negative | `tests/test_adcs_enrichment.py` (the hand version of the probe, deterministic seeds); when the WP3 tension report is available the same quantities are also computed with `tension_report` and must agree |
| R-10 | Torque binds: in the enriched scenario the median `torque_saturated_frac` of small-wheel designs is at least 0.25 and at least three times that of large-wheel designs, and the median settling time of small-wheel designs is at least 1.25 times that of large-wheel designs | `test_adcs_enrichment.py` |
| R-11 | The dataset has at least 1000 designs, the WP4 columns where they apply plus the new design-variable, attribute and scenario columns, a settled fraction of at least 0.85, and the share of designs violating `momentum_ok` (and the depth-of-discharge flag if used) reported by a test | `test_adcs_enrichment.py`; pandas inspection |
| R-12 | Seed stability: for the first 20 designs, regenerating with the recorded options reproduces the committed rows with the WP4 per-column tolerances (categorical columns and flags equal, settling within 0.5 s, continuous columns rtol 1e-4, `torque_saturated_frac` rtol 2e-2), and 40 designs regenerated twice on the same platform are identical | `uv run pytest tests/test_satellite_model.py -k reproduc` |
| R-13 | Each exposed tension is physically explicable: the probe note gives, for agility vs mass, the power tension(s) of R-9(d), settling vs effort, pointing vs effort and pointing vs mass, the mechanism and the design variable through which it acts; any tension that appears but is not recognizable is stated as such; the note records every modelling choice, lever tried (including failures), the final constants and the R-9 results with near-frontier sample sizes | inspection of the probe note |
| R-14 | The SysML text parses as plain text, is non-empty, defines the abstract parts of R-3 with attributes and units, shows the relations (panel to power and inertia; battery to mass and energy; wheel to torque and power; star tracker to pointing and power), describes concrete configurations and the model test, states that it is illustrative and documentation only, and reads as a sensible satellite | inspection by the reviewer |
| R-15 | The full suite, linters and lock pass and nothing outside scope changed: `uv run pytest`, `uv run ruff check .`, `uv run ruff format --check .`, `uv lock --check`; `git diff --stat <start>..HEAD` shows only the deliverable paths and `work-packages/` | run the commands; inspect the diff |
| R-16 | No AI attribution lines; commits authored as Michael Zargham; CI green on every push | `git log` grep returns 0; `gh run list` |

## Definition of good

- The satellite makes engineering sense at a glance: bigger panels give more power, cost mass and slow the slew; bigger batteries ride through eclipse and weigh more; bigger wheels are agile, heavy and hungry; finer star trackers point better, weigh more and draw more. The fit finds these on its own.
- The model is minimal and physically plausible, not tuned until a test passes: constants are anchored to the WP4 baseline where possible (panel areal density, baseline inertia) and to textbook-scale orders of magnitude elsewhere, each labelled illustrative with its rationale.
- The measurement is the model test: configuration in, attributes out, the simulator reused untouched.
- The probe note is an honest record, including levers that failed, so WP7 can interpret the result without surprise.
- The WP4 deliverables are untouched and the new dataset sits beside the original.

## Definition of good enough

- Deliverables D-1 to D-8 exist at the stated paths.
- R-1 to R-16 pass as checked, with evidence in the review report; in particular the richness conditions of R-9 and R-10 hold on the committed dataset.
- Non-goals untouched (no simulator, estimator, toolkit or notebook change).

## Definition of done

Good enough is met, **no open item remains unresolved**, and the supervisor has accepted the work by the acceptance record above.

## Agent's defaults

All marked *(default)* where they appear; the supervisor approves or changes the list as one item. Every number is illustrative and held to the plausibility rule: chosen first for physical plausibility and anchoring to the WP4 baseline, adjusted at most three times if R-9 or R-10 fail, each adjustment recorded in the probe note (R-13). WP4b is independent of WP3 and may start as soon as its scope is approved; if the WP3 tension report is available at review it is also run (R-9).

- Design variables (configuration), sampled log-uniformly where continuous *(default, illustrative)*: panel span 1.5 to 5.0 m with chord fixed at 0.9 m (area 2·span·chord); battery capacity 1500 to 6000 Wh; wheel class small/medium/large (enriched set below); star-tracker grade coarse/medium/fine; Kp 0.5 to 16 and Kd 5 to 60 as in WP4; antenna mass with the WP4 10 % lognormal perturbation; panel mass is no longer perturbed (it is derived from area).
- Constants *(default, illustrative)*: panel areal density 30 kg / 2.25 m² = 13.33 kg/m² (reproduces the baseline panel); solar flux 1361 W/m²; cell efficiency 0.28; packing factor 0.85; end-of-life degradation 0.85 (generation about 275 W/m² of panel); battery specific energy 120 Wh/kg; bus fixed mass chosen so that the baseline configuration (span 2.5 m, battery 3600 Wh = 30 kg, medium wheels, medium star tracker) gives bus mass 550 kg and the WP4 baseline inertia; housekeeping and payload load 800 W; eclipse duration 1.2 h (GEO worst case) and maximum depth of discharge 0.8.
- Enriched wheel set *(default, illustrative)*: small (maxTorque 0.02 N·m, maxMomentum 1 N·m·s, mass 0.8 kg), medium (0.10, 4, 2.5), large (0.50, 16, 6.0); a wheel electrical-loss coefficient c (W per (N·m)²) per class, one value for all classes, chosen so a saturated large wheel draws a few hundred watts.
- Star-tracker grades *(default, illustrative)*: accuracy and mass as WP4 (15″/1.0 kg, 5″/2.0 kg, 1.5″/3.5 kg) plus electrical draw 3, 8 and 15 W.
- Scenario *(default)*: slew about X of 45° with horizon `t_end = 1200` s and `max_step = 0.5`; only if R-10 fails, steeper angles up to 90° or a shorter horizon, recorded.
- Couplings to the controls *(default)*: (1) panel span, panel mass and battery mass change the bus and panel parameters passed to the existing `inertia_tensor`, hence Jxx and Jzz, hence settling time, control effort, gravity-gradient torque and the pointing budget; (2) available wheel power P_avail = generation − housekeeping − sensor loads caps the usable wheel torque at min(maxTorque, sqrt(P_avail / (3c))), passed as the wheel's `maxTorque` to `make_config`; (3) wheel class sets maxTorque and maxMomentum; (4) star-tracker grade sets the pointing floor and the sensor load. Negative or zero P_avail makes the design infeasible and it is flagged and kept in the dataset with `power_ok = False` (its attributes are computed with a minimal torque cap of 1 % of maxTorque).
- Attributes *(default; subject to OD1 and OD2)*: `settling_time_s`, `pointing_error_deg` (the WP4 analytic budget with the new inertia and the star-tracker floor), `total_mass_kg` (R-7), `control_effort` (∫‖τ‖dt), the power attribute(s) of OD1; the WP4 column `adcs_mass_kg` is kept for continuity. Orientation for conditioning in the probe: reciprocal for settling, pointing, mass and effort; the power attribute(s) oriented larger-is-better (margin) or reciprocal (draw) as OD1 fixes.
- Energy accounting *(default)*: slew energy = ∫ (n_w·P_idle + c·‖τ_ctrl‖²) dt over the simulated slew, with a small idle power per wheel (`P_idle` 5 W); sunlit generation as above; eclipse energy = (housekeeping + sensor loads + mean ADCS draw) × eclipse duration, to be met from battery capacity × maximum depth of discharge.
- Flags *(default)*: `settled`, `momentum_ok`, `torque_saturated_frac` as in WP4, `power_ok` (P_avail > 0), and the depth-of-discharge item per OD2.
- Generator flags *(default)*: `--model` in {"adcs" (default, the WP4 behaviour), "satellite"}, `--slew-deg` (default 10.0 for "adcs", 45.0 for "satellite"), `--t-end`; the enriched run writes `examples/adcs/data/adcs_designs_satellite.csv`; the exact command is recorded in the probe note and in the reproducibility test.
- Dataset size *(default)*: 1000 designs, seed 0; 2000 if the near-frontier counts needed by R-9(c) are insufficient, recorded.
- Probe method *(default)*: the probe note's method (settled designs, standardized log-metrics, LP at τ = ∞ with `min_exponent = 0`, working τ by bisection to `frac_above_` ≈ 0.10, near-frontier |log V| < 1/τ, Pearson association, PCA of near-frontier Z), extended to the d of the attribute set; bootstrap 100 resamples seeded 0; thresholds as in R-9.
- Tests *(default)*: `test_satellite_model.py` uses the simulator with `FAST_SIM`-style settings where possible; `test_adcs_enrichment.py` fits `HyperbolicTradeSpace` and `solvers.solve_lp` on the committed CSV, no simulation, a few seconds.
- SysML *(default)*: `package SatelliteModel` with `part def Satellite`, `Bus`, `SolarPanel`, `Battery`, `ReactionWheel`, `StarTracker`, `Controller`, attributes with units, `part def` specializations for the wheel classes and star-tracker grades, a comment block describing concrete configurations as sampled instances and `measure` as the model test producing the attributes, mirroring spec §3's stages (configuration, evaluation, attributes); documentation only.
- Knock-on for WP7 *(default)*: d changes, the three-dimensional figures use a chosen three-metric subset, and the WP7 probe step reruns; WP7's draft scope is updated after WP4b's acceptance, not before.
- Commits prefixed "WP4b: "; model and tests, then dataset, then SysML, then probe note, then status table and decisions file; every push green and attribution-free *(default)*.
- If after the allowed adjustments R-9 does not hold, execution stops and the driver is told (a problem-level change: the case cannot be made to expose the intended tensions with this model) *(default)*.

## Open decisions (for the supervisor)

- **OD1.** What does the power attribute mean, that is, what is the model measuring? Panel size sets generation, the battery sets storage, and the wheels draw power during the slew, so the choice fixes how many attributes there are (d = 5 or 6) and what the fit's power tension reads as. — options: (a) one attribute, the sunlit power margin: generation minus housekeeping, sensor and peak slew loads, in watts, larger is better / (b) one attribute, the energy balance: orbit-average energy surplus (generation minus total energy used, in Wh), larger is better / (c) two attributes, the sunlit power margin and the eclipse energy reserve (usable battery energy minus eclipse demand, in Wh), larger is better, giving d = 6 / (d) one attribute, the peak power draw during the slew, in watts, smaller is better
- **OD2.** Is battery depth of discharge a feasibility flag or a metric? — options: (a) a flag (`dod_ok`: eclipse demand ≤ maximum depth of discharge × capacity); the battery enters the metrics only through mass and, per OD1, the energy attribute / (b) a metric (the depth of discharge in the design's eclipse, smaller is better), in addition to the OD1 choice

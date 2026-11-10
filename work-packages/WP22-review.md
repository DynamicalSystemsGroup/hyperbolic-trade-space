# WP22 review record: the modeller loop

## Round 1 (2026-11-09)

**Model change.** New file `examples/adcs/model_v2/cubesat_r1.sysml` beside `cubesat.sysml` (R-14: the old
file is byte-unchanged; a test ties its hash to the ledger's last entry). Added: `SlewMeasurement.slewTime` and
`peakTorque` (recorded baseline measurements); requirement defs `SlewTimeRequirement`,
`EclipseReserveRequirement`, `PowerMarginRequirement`, `EnergyBalanceRequirement`;
`DepthOfDischargeRequirement` restated over `DepthOfDischarge(...) <= maxDepthOfDischarge`; a `satisfy` by
`cubesatBaseline` for each new one; `verify` objectives in `SlewVerification`; `doc` on both verification
cases naming the four open metrics; the two views marked by documented section headers (D-1 allows packages
or sections; sections kept so qualified names and the opensysml reads do not change). Calc defs, the
analysis def, ranges and every number of `cubesat.sysml` are carried over unchanged.

**Checks (all run, all pass).** Strict load, `self_check` holds; 9 `satisfy` all hold (engine run);
pinned toolkit `check` exit 0, `lint` 0 errors 0 warnings, `verify --solve` 0 violated; the only numeric
literal added to the code is the measured slew time 133.6904772571943 s (R-4; zero and
`maxDepthOfDischarge` and `nominalSlew.horizon` are the thresholds).

**Equivalence (R-6, R-7, R-13).** Test on regenerated designs, same seed, both gain boxes (6 each,
0.5 s step): r1 analysis outputs are identical to the old v2 model's, and equal the frozen oracle to
< 1e-9; the four flags equal the frozen flags; the restated depth-of-discharge verdict equals the old one.
Ledger: `v2-primary-r1` regenerated 1000 designs, output sha256 `4dc4ae0b8e...` equal to `v2-primary@2`
(no difference, so no STOP). See the ledger section below for the baseline dataset.

**Views.** `out/r1/` (assembly and behavioural, puml, svg, png at 700 px); three runs byte-identical;
assembly text identical to the old one; mutation test (added alternative changes assembly only, added
requirement changes behaviour only). Projection script revision: the metric-to-element table is gone,
each metric is found by its own name in the model; only requirements that read the metric's own
quantity or calc are drawn (a shared upstream calc is not a bound: `PowerMargin` calls `PeakSlewPower`
and no requirement bounds the peak slew power); an open metric must be named in a verification case doc,
checked on every run. Still typed: layout, colours, and the subsystem of `MomentumRequirement`.

### Reviewer (fresh context, Sonnet, opened the rendered PNGs)

Findings and dispositions (round 2 takes the open ones):

| # | Finding | Severity | Disposition |
|---|---|---|---|
| A-1 | Assembly legend lists `baselineGains`/`aggressiveGains`, names that appear nowhere in the picture; one range per variable would read better | hinders | open, round 2 |
| A-2 | Alternatives are not in enum order (`Large, Medium, Small`; `Coarse, Fine, Medium`) | hinders | open, round 2 (sort by the enum's literals) |
| A-3 | Fixed parts (Bus, Antenna, Imu) look like omissions | polish | open, a `fixed` tag is a candidate |
| B-1 | Long grey arrows from `SlewExperiment` to pointing error and total mass run round the picture | blocks understanding | open, round 2 (layout: source boxes beside the metrics, or one arrow per group) |
| B-2 | Control effort is drawn from `SlewMeasurement`, but the model's `SlewMeasurement` has no `controlEffort`; it is an analysis `in` returned unchanged | blocks understanding | a real model gap, not a drawing slip: add `controlEffort` to `SlewMeasurement` (a measurement, not a threshold, so within R-4) and bind it, round 2 |
| B-3 | Green fills both covered metrics and the `SlewExperiment` source | hinders | open, round 2 (source boxes one colour) |
| B-4 | Dashed vs solid alone separates covered from open; a caption "no requirement" in each dashed box is suggested | hinders | open, round 2 |
| B-5 | Requirements with no line sit among those with lines, near unrelated metrics | hinders | open, round 2 (rank them apart) |
| B-6 | Line labels are calc names (`EnergyBalance`) repeating the metric | polish | accepted (the label is the model identifier, which is the point) |
| B-7 | `SlewTimeRequirement` is the same statement as `SlewBandRequirement` | candour | already stated in the requirement's doc (OD2); add a view caption, round 2 |

Trace check on the picture: settling time, slew time, power margin, energy balance, eclipse reserve,
depth of discharge each follow to one requirement and one source; pointing error, total mass, peak slew
power follow with effort (B-1); control effort cannot (B-2). Round 1 therefore does not end the loop:
the last round must find nothing that changes a view.

### Trace table (metric to model element)

| Metric | Configuration variables (via) | Measured or calculated by | Requirement (value taken from) | Verified in |
|---|---|---|---|---|
| settling time | span, capacity (inertia), Kp, Kd, wheel class, tracker power (torque cap) | `SlewMeasurement.settlingTime` | `SettledRequirement` (`nominalSlew.horizon`, 600 s) | `SlewVerification.settled` |
| slew time | same | `SlewMeasurement.slewTime` | `SlewTimeRequirement` (`nominalSlew.horizon`; completion within the horizon, OD2) | `SlewVerification.slewTime` |
| power margin | span, tracker grade, wheel class, gains (peak torque) | calc `PowerMargin` | `PowerMarginRequirement` (zero) | `SlewVerification.powerMargin` |
| energy balance | span, tracker grade, slew loss | calc `EnergyBalance` | `EnergyBalanceRequirement` (zero) | `SlewVerification.energyBalance` |
| eclipse reserve | capacity, tracker grade, slew loss | calc `EclipseReserve` | `EclipseReserveRequirement` (zero) | `SlewVerification.eclipseReserve` |
| depth of discharge | capacity, tracker grade, slew loss | calc `DepthOfDischarge` | `DepthOfDischargeRequirement` (`environment.maxDepthOfDischarge`, 0.3) | `SlewVerification.depthOfDischarge` |
| pointing error | Kp, tracker grade, inertia | calc `PointingError` | none: needs an angle bound (WP22b) | none |
| control effort | gains, inertia, torque cap | analysis `in` `controlEffort` (not yet a `SlewMeasurement` attribute, B-2) | none: needs an effort bound in N.m.s (WP22b) | none |
| total mass | span, capacity, wheel class, tracker grade | `Cubesat.totalMass` (`MassAccounting`) | none: needs a mass limit in kg (WP22b) | none |
| peak slew power | tracker grade, peak torque | calc `PeakSlewPower` | none: needs a power budget in W (WP22b) | none |

### Ledger (D-4, R-7)

`examples/adcs/model_v2/ledger_r1.py` declares the two v2 datasets' experiments again with the r1 model
and runs them into the same paths: `v2-primary-r1` (output sha256 `4dc4ae0b8e...`) and `v2-baseline-r1`
(`9450713cd7...`), each equal to the output hash of `v2-primary@2` and `v2-baseline@2`; `git status` shows
no change to either CSV. Nothing is superseded: the old entries stay current and cite the old model until
the gate. The check-design pair (100000-design pool) was not re-run in round 1; it reads the primary
dataset, which is unchanged.

## Round 2 (2026-11-09)

**Model change.** `SlewMeasurement.controlEffort` (integral of |tau| over the slew, N.m.s) added to
`cubesat_r1.sysml` with the baseline's recorded measurement 0.009490621914197469 N.m.s (re-measured by a test,
rel 1e-3); `SlewExperiment`'s `in controlEffort` now defaults to `baselineMeasurement.controlEffort`. A measurement,
not a threshold (R-4: the numeric-literal test now allows exactly the two recorded measurements). The analysis still
returns it unchanged, so outputs are identical.

**Views (projection script).** B-1: subsystems fed by the measurement come first and the requirements with no line
leave the frames (one separate dashed group), so the frames are short and the two analysis-fed outliers (pointing
error, total mass) sit next to the analysis box; B-2: control effort now traces to `SlewMeasurement`; B-3: the
analysis box is lilac, green is only covered metrics; B-4: each dashed box reads "(no requirement)"; B-5: the
no-line requirements are one group apart; A-2: alternatives in enum order (derived from the enum literal each part
def binds); A-1: one Kp and one Kd line, no instance names. Reviewer round 2 additions applied: the analysis box
says "computes 7 of the 10 metrics" (it said "eight attributes", seven arrows drawn); the legend says green for
covered; gains described as one range per dataset instead of "gain box".

**Checks.** ruff on changed files clean (the spike script is outside ruff's configured scope; it was reformatted by
`ruff format`, which makes its diff large); `tests/test_system_model_v2_r1.py` (15, incl. toolkit check/lint/verify
--solve, equivalence on both gain boxes, three-run determinism, mutation), `test_model_checking_v2.py`,
`test_system_model_v2.py`, `test_cubesat_model.py` (117) pass with `REQUIRE_OPENSYSML=1`. Ledger: `v2-primary-r1@2`
and `v2-baseline-r1@2` supersede the round-1 entries (the model file changed in place, which verify would report as
drift); output hashes `4dc4ae0b8ebe` and `9450713cd78c`, equal to `v2-primary@2` and `v2-baseline@2`; `verify`: 0
drifts, no data file changed.

### Reviewers (two fresh contexts, Sonnet, opened the PNGs; P1 decision maker at skim depth, P3 modeller at careful depth; each image alone, then with its caption; captions in the scratchpad)

Both traced all ten metrics to a requirement or an explicit "(no requirement)" and a source. Round-1 blocks gone.

| # | Finding | Severity | Disposition |
|---|---|---|---|
| R2-1 | Lines from SlewExperiment to pointing error and total mass are still long diagonals along the right edge (both reviewers) | hinders | open: shorter than round 1 and no longer round the frames; a reader can follow them. Round 3 candidate: per-frame source node |
| R2-2 | SlewExperiment lines to depth of discharge and eclipse reserve nearly overlap at the box | hinders | open, round 3 |
| R2-3 | Dashed group at the top reads as orphaned; PowerRequirement outside the power frame | hinders | caption carries it; wording of the frame title is a round-3 candidate |
| R2-4 | Box said "eight attributes", seven arrows | hinders | fixed (computes 7 of the 10) |
| R2-5 | Legend "gain box" and two Kp ranges unexplained | blocks (P3) | fixed (one range per dataset) |
| R2-6 | The SlewTimeRequirement-equals-horizon sentence is only in the caption; no counterpart in the picture | hinders | open; add to legend in round 3 |
| R2-7 | No bound values, no conditioning step, no link from Figure A variables to Figure B metrics | hinders | out of scope: values are WP22b; the link is the model's own trace table above |
| R2-8 | Fixed parts untagged; FineTracker line near Controller; W*h notation | polish | A-3 still open |

Result: round 2 does not end the loop. The last round must find nothing that changes a view; R2-1, R2-2 and R2-6
would change a view. A round 3 is needed (or the supervisor's call that R2-1 is good enough).

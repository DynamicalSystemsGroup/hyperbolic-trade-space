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

## Round 3 (2026-11-09)

**Model change.** None (`cubesat_r1.sysml`, the ledger and every output unchanged; the ledger `verify` reports 19
entries, 0 drifts; no new entry is needed because no model file or output changed).

**Views (projection script, layout parameters and model-derived text only; no hand-edited output).**
R2-2: a layout control `ANALYSIS_BOX_PAD` (blank lines in the analysis box) makes the box tall enough that each
metric it feeds gets its own line; the lines to depth of discharge and eclipse reserve no longer meet at one point.
R2-1: the same control shortens the long diagonals (the box now spans from the power frame to the mass frame);
rank, hidden links and ordering were already used in round 2 and were not enough alone. R2-6: a requirement whose
`doc` says it is "the same statement as the <other> requirement" now says so in its own box, with the doc's first
sentence ("The slew completes inside the horizon; same statement as SlewBandRequirement"), derived from the model's
doc text. The assembly view is byte-identical to round 2. Checks: ruff on the changed test and ledger files clean
(`ruff format` applied to `project.py`); `tests/test_system_model_v2_r1.py`, `test_model_checking_v2.py`,
`test_system_model_v2.py`, `test_cubesat_model.py`: 132 passed with `REQUIRE_OPENSYSML=1` (equivalence max rel diff 1.8e-16).

### Reviewers (two new fresh contexts, Sonnet, opened the PNGs; persona and depth from `docs/superpowers/notes/reader-grid.md`: P1 accountable decision maker at L-B skim; P3 modeller at L-C careful; each image alone, then with its caption; the caption no longer carries the SlewTime sentence)

| # | Finding | Severity | Disposition |
|---|---|---|---|
| R3-1 | R2-2 gone: no overlapping lines seen by either reviewer | | fixed |
| R3-2 | Long grey arrows to pointing error and total mass remain visible diagonals; P3 could confirm the pointing-error source only by counting 3+7=10 (one grazes SlewMeasurement) | hinders (both) | partly fixed (shorter, none cross another frame's boxes); residual accepted for this package: a per-frame source node would repeat the analysis box and misstate "one analysis"; a reader can follow every line |
| R3-3 | "same statement as SlewBandRequirement" is now in the picture, but SlewBandRequirement sits in the dashed top group with no connector | hinders (both) | open, one candidate for a round 4: a dashed "same statement" link drawn from the doc relation |
| R3-4 | Top dashed group far from everything; why PowerRequirement reads no traded metric | hinders | open; caption carries it (the requirement reads inputs of the analysis, not a metric) |
| R3-5 | No values anywhere; a decision maker reads a coverage map, not a result (P1: blocks) | blocks (P1 only) | out of scope: values are WP22b; a title naming the figure as a coverage map is a presentation-side wording candidate |
| R3-6 | Figure A legend: "baseline vs aggressive datasets", Kp/Kd undefined, "W*h", SysML stereotypes | hinders | open (A-3, R2-8 family); the presentation side defines these in the caption |
| R3-7 | Box says "7 of the 10"; P1 counted 11 boxes | hinders (P1) | misread: the picture has 10 metric boxes plus a placeholder; P3 reconciled 3+7=10. Accepted; the placeholder in the mass frame is the likely cause |
| R3-8 | Stereotype lines repeat in every requirement box; camelCase labels vs lower-case metric names; legend dense | polish | accepted (labels are model identifiers) |

### Stopping verdict against the scope's good enough

R-1 to R-11 hold for the six G2 metrics; two full rounds ran; the four uncovered metrics are named in the model
and here with the value each needs; the trace table is above. The strict clause ("the last round found nothing
that changes a view") is not met: R3-3 would change a view. Nothing found in round 3 blocks within the scope
(the one "blocks", R3-5, is the WP22b values question). The PM's recommendation: stop the loop; R3-3 is a small
round 4 only if the supervisor wants it. R2-1 is recorded as accepted in part, with the reason in R3-2.

## Gate comparison report (R-14; the swap is NOT done)

Old model `examples/adcs/model_v2/cubesat.sysml` (what the committed data and the paper cite) against the new one
`cubesat_r1.sysml`, in the shape of WP16's data gate. Evidence produced 2026-11-09 in a clean worktree at `3cd4c5a`
(`dev`), pinned toolkit v0.12.0, `REQUIRE_OPENSYSML=1`.

| Question | Answer | Evidence |
|---|---|---|
| Is the old file byte-unchanged? | Yes. Last change to it is WP15's commit `2d13465`; nothing since. Its sha256 equals the ledger's last old entries. | `git log --oneline -1 -- .../cubesat.sysml` gives `2d13465`; `git diff origin/dev -- .../cubesat.sysml` empty; `shasum -a 256` gives `28dbeeb23cf4...`, equal to `model_sha256` of `v2-primary@2`, `v2-baseline@2`, `v2-check-predictions@2`, `v2-check-designs@2` and `scope-sensitivity-shared-subspace-v2`. The new file is `e4c25a256ab1...`, equal to `model_sha256` of `v2-primary-r1@2` and `v2-baseline-r1@2` |
| What is identical? | Carried over unchanged: every calc def (accounting, power, energy, inertia, pointing, slew closed form), the analysis def `SlewExperiment` (its eight returned attributes), all ranges and enums, the named configurations, `SettledRequirement`, `MomentumRequirement`, `PowerRequirement`, `SlewBandRequirement`, the existing `satisfy` and `verify` elements, every number of the old model. Assembly view text identical to the old one | 114 differing diff lines in all (see added/restated); equivalence tests below; round 1's assembly-text comparison (within the 132 passed) |
| What is added? | `SlewMeasurement.slewTime`, `peakTorque`, `controlEffort` (recorded baseline measurements, the only two numeric literals added besides thresholds); `SlewTimeRequirement`, `EclipseReserveRequirement`, `PowerMarginRequirement`, `EnergyBalanceRequirement`; a `satisfy` by `cubesatBaseline` and a `verify` objective in `SlewVerification` for each of the four; `doc` on the two verification cases naming the four open metrics; the two views marked by header comments (sections kept) | `diff cubesat.sysml cubesat_r1.sysml`: 22 undecided constraint rows in `verify --solve` against 14 (the added ones) |
| What is restated? | `DepthOfDischargeRequirement` now reads `DepthOfDischarge(...) <= maxDepthOfDischarge` (was an inline `EclipseDemand(...) <= maxDepthOfDischarge * capacity`); `SlewExperiment`'s `in controlEffort` defaults to `baselineMeasurement.controlEffort`; the file's header comment and section headers name the views | the restated verdict equals the old one at every checked configuration (test) |
| Are the outputs equal? | Yes. Regenerated outputs are byte-identical; analysis outputs equal the old v2 model's, flags equal the frozen flags | `v2-primary-r1@2` output `4dc4ae0b8ebe` = `v2-primary@2`; `v2-baseline-r1@2` `9450713cd78c` = `v2-baseline@2`; 132 passed in 110 s (`test_system_model_v2_r1.py`, `test_model_checking_v2.py`, `test_system_model_v2.py`, `test_cubesat_model.py`); printed "[equivalence] eight computed attributes, 5 configs: max rel diff 1.83e-16 (dod_eclipse)" and "accounting, 8 configs: max rel diff 0.00e+00"; the oracle test requires < 1e-9; ledger `verify`: "19 entries (13 current); 0 drifts", exit 0 |
| Toolkit gates on both files | Both pass, same exit codes. The new file has 8 more constraint rows, all undecided (none violated) | via `experiments.toolkit.locate()`: `cubesat.sysml` check 0, lint errors 0 warnings 0 (6 infos), `verify --solve` 0 ("0 satisfied, 0 violated, 14 undecided"); `cubesat_r1.sysml` check 0, lint errors 0 warnings 0 (6 infos), `verify --solve` 0 ("0 satisfied, 0 violated, 22 undecided"). The test `test_toolkit_check_lint_and_verify_solve_pass_on_r1` runs the same three on r1 (needs the pinned binary; installed here) |
| What does the swap change for paper and docs? | The paper notebooks and generators do not name `cubesat.sysml` or `model_v2` (grep of `paper/`: none); they read the ledger (`paper/generate_model.py` takes each dataset's entry, command and hash from `ledger.jsonl`), so the paper's provenance rows change only by the entry id and model hash. The rest is in the lists below | WP22d list below |
| Gate decision | To be recorded by the driver in `WP22-decisions.md` | quoted verbatim there |

**WP22d: what the swap touches (by kind of change).**
- Path (one constant or sentence): `examples/adcs/experiments/definitions.py` (`V2_MODEL`, the experiments' `model_path`),
  `compare.py` (reads the model text), `cubesat_oracle.py` and `feasibility.py` (docstrings and the file they read),
  `examples/adcs/case-model.md` (4 references; the how-to text), `scripts/check.py` (the changed-path to test map).
- Tests that pin or open the model: `test_system_model_v2.py`, `test_model_checking_v2.py`, `test_mutation_v2.py`,
  `test_cubesat_oracle.py`, `test_v2_data.py`, `test_case_model_howto.py`, `test_paper.py` (a docstring only); each
  opens the old file and would open the new one; the model-hash assertions would be re-pinned to the new hash.
- Hash pinned: the ledger gets new entries superseding the five old ones that cite `28dbeeb23cf4` (the `-r1@2` entries
  already carry `e4c25a256ab1` and the same output hashes, so the paper's data hashes do not move); `ledger_r1.py` is retired.
- Regenerated (no figure changes expected): `paper/generate_model.py` provenance rows and, through them, Appendix C and
  F tables and `paper/supporting_material.ipynb`; `experiments/reports/v1-v2-comparison.md` and `change-register.md`
  (cite the file). `work-packages/interface-contract.{md,toml}` names the folder, not the file.
- Folder: `cubesat_r1.sysml` would be renamed or become `cubesat.sysml` and the old file kept in history only; the
  views generator `out/r1/` becomes the model's views.
- WP16 Amendment 2 (event detection and regeneration on the new model) adds, on top, a regeneration of the datasets
  with event-detected slew times, so the data hashes, the fits and the paper's numbers move; it is a data gate, not a
  path change.

**PM's reading.** The evidence supports: the old file is untouched and its hash is the one the ledger holds; the new
file passes the same strict load, check, lint and `verify --solve` as the old one; on the regenerated designs of both
datasets the new model returns the old model's outputs (byte-identical output files, analysis agreement to 1.8e-16,
flags and verdicts equal), so adopting it moves no committed number; it adds four requirements (and restates a fifth) with
their verification structure, and the two marked views. It does not support: any claim that the four uncovered metrics
(pointing error, control effort, total mass, peak slew power) are bounded (their thresholds are WP22b); any claim
about configurations other than the regenerated designs and the baseline (WP22c); and the picture's remaining open
items R3-2 and R3-3, which the loop's strict stopping clause counts and the PM's recommendation accepts. The 22
undecided rows in `verify --solve` are the unbound baseline chain, the same cause as the old file's 14, not a result.

# WP23 D-4: interface-contract amendment 11, the draft

Status: a draft for the driver (approval under the mandate, recorded in `WP23-decisions.md`). This
file is not the contract. The change lands in `work-packages/interface-contract.md` and
`work-packages/interface-contract.toml` in one commit, at the data gate, together with the
regenerated v2 datasets (the headers below are what the regeneration writes; the contract test on
them cannot be green before it).

## What changes

The v2 datasets (`examples/adcs/data/v2/`) lose the two slew-time columns, `slew_time_s` and
`slew_time_05deg_s` (WP23 G5; the supervisor, `WP16-decisions.md`: "One: settling time"). The case
has one time metric, the settling time, read by event detection (the hold time: the first time
after which the pointing error stays inside the band of the model's settling fraction, located as
the last exit on the dense solution; `experiments/cubesat_oracle.py`, `settling_time_method`
`"events"`, recorded in each ledger entry's `versions.runtime`). The traded metrics of the v2 data
are nine. The check-design predictions file carries the standard deviation of the predicted time
metric on the settling time (`pred_std_settling_time_s` in place of `pred_std_slew_time_s`),
because the check-design fit's four metrics are the time metric, pointing error, control effort and
total mass (`definitions.py`, `v2-check-predictions`, `inputs.metrics`; `experiments/check_designs.py`
`METRICS` follows).

Nothing else changes: the frozen datasets under `examples/adcs/data/` and their `case.data`
manifests keep every column (the frozen files are not regenerated: WP23 non-goals), and no
`launch_cost` column enters (`WP23-decisions.md`, OD1 and OD2: launch cost is the MoE on total mass,
no new column).

## The manifest: the v2 headers pinned (new tables in `interface-contract.toml`)

The contract pins the frozen headers in `case.data`; the v2 headers were not pinned (the v2 files
had the frozen columns by WP15 R-13). This amendment pins them beside the frozen ones, as the
frozen columns less the two slew-time columns, in the frozen order.

```toml
[case.v2]
dir = "examples/adcs/data/v2/"
data_rule = "committed, seeded, ledgered (experiments/ledger/ledger.jsonl); regenerated only by a package whose scope says so, once, in the container of record"
traded_metrics = [
  "settling_time_s", "pointing_error_deg", "total_mass_kg", "control_effort",
  "power_margin_w", "energy_balance_wh", "eclipse_reserve_wh", "peak_slew_power_w", "dod_eclipse",
]
time_metric = "settling_time_s"
settling_time_method = "events"

[case.v2.data."adcs_designs_cubesat_gains.csv"]
role = "primary regime dataset, v2"
rows = 1000

[case.v2.data."adcs_designs_cubesat_gains.csv".columns]
design_id = "int"
seed = "int"
wheel_class = "str"
st_grade = "str"
panel_span_m = "float"
battery_wh = "float"
Kp = "float"
Kd = "float"
settling_time_s = "float"
pointing_error_deg = "float"
total_mass_kg = "float"
adcs_mass_kg = "float"
control_effort = "float"
power_margin_w = "float"
energy_balance_wh = "float"
eclipse_reserve_wh = "float"
peak_slew_power_w = "float"
dod_eclipse = "float"
settled = "bool"
momentum_ok = "bool"
torque_saturated_frac = "float"
power_ok = "bool"
dod_ok = "bool"
peak_momentum_nms = "float"
panel_mass_kg = "float"
battery_mass_kg = "float"
generated_power_w = "float"
available_power_w = "float"
usable_torque_nm = "float"
slew_loss_energy_wh = "float"
slew_deg = "int"
t_end_s = "int"
max_step_s = "float"

[case.v2.data."adcs_designs_cubesat.csv"]
role = "stock (baseline) regime dataset, v2"
rows = 1000

[case.v2.data."adcs_designs_cubesat.csv".columns]
# the same 33 columns as the primary file, in the same order

[case.v2.data."check_designs_cubesat.csv"]
role = "propose-predict-check designs, simulated, v2"
rows = 6

[case.v2.data."check_designs_cubesat.csv".columns]
role = "str"
design_id = "int"
name = "str"
seed = "int"
panel_span_m = "float"
battery_wh = "float"
wheel_class = "str"
st_grade = "str"
Kp = "float"
Kd = "float"
settling_time_s = "float"
pointing_error_deg = "float"
total_mass_kg = "float"
control_effort = "float"
power_margin_w = "float"
energy_balance_wh = "float"
eclipse_reserve_wh = "float"
peak_slew_power_w = "float"
dod_eclipse = "float"
settled = "bool"
momentum_ok = "bool"
power_ok = "bool"
dod_ok = "bool"
torque_saturated_frac = "float"
adcs_mass_kg = "float"
peak_momentum_nms = "float"
panel_mass_kg = "float"
battery_mass_kg = "float"
generated_power_w = "float"
available_power_w = "float"
usable_torque_nm = "float"
slew_loss_energy_wh = "float"

[case.v2.data."check_predictions_cubesat.csv"]
role = "propose-predict-check predictions, v2"
rows = 3

[case.v2.data."check_predictions_cubesat.csv".columns]
role = "str"
design_id = "int"
name = "str"
panel_span_m = "float"
battery_wh = "float"
Kp = "float"
Kd = "float"
wheel_class = "str"
st_grade = "str"
target_z1 = "float"
target_z2 = "float"
target_z3 = "float"
pred_z1 = "float"
pred_z2 = "float"
pred_z3 = "float"
pred_log_v = "float"
pred_std_settling_time_s = "float"
pred_std_pointing_error_deg = "float"
pred_std_control_effort = "float"
pred_std_total_mass_kg = "float"
hole_score = "float"
distance_to_target = "float"
tau = "float"
band = "float"
n_train = "int"
```

The dtype classes of the scenario columns (`slew_deg`, `t_end_s` as `int`) follow the frozen
manifest, which pandas reads from the written values `30`, `600`; the regeneration keeps the
`%.9g` float format of the runner.

`contract_version = 11` in the manifest and in the document's "Quoted from the manifest".

## The document (`interface-contract.md`)

Section 7, "R-3 Case module and data", gains a paragraph after the frozen data files:

> The v2 datasets live in `examples/adcs/data/v2/` with the frozen file names (manifest `case.v2`):
> the frozen columns less the slew-time columns `slew_time_s` and `slew_time_05deg_s`, in the frozen
> order. The traded metrics of the v2 data are nine (`case.v2.traded_metrics`); the one time metric
> is the settling time, read by event detection (`case.v2.settling_time_method`), the hold time: the
> first time after which the pointing error stays inside the band of the model's settling fraction.
> The check-design predictions carry `pred_std_settling_time_s`. The v2 files are ledgered
> (`experiments/ledger/ledger.jsonl`) and regenerate once, in the container of record, by a package
> whose scope says so, which updates this manifest in the same commit.

Section 14, the change log, gains the row:

| Version | Date | Change | Side affected | Approval |
|---|---|---|---|---|
| 11 | 2026-11-10 | One time metric (WP23 G5, D-4; the supervisor, `WP16-decisions.md`: "One: settling time"): the v2 datasets lose `slew_time_s` and `slew_time_05deg_s`, their headers are pinned (`case.v2.data`, the frozen columns less those two, in the frozen order), the traded metrics of the v2 data are the nine of `case.v2.traded_metrics`, the settling time is read by event detection (`case.v2.settling_time_method = "events"`, WP16 Amendment 2 D-7), and the check-design predictions carry `pred_std_settling_time_s`. No `launch_cost` column (`WP23-decisions.md`, OD2). The frozen files and their `case.data` manifests are unchanged | technical (the paper's figures and numbers that used slew time regenerate in their own stream after the data gate; the docs follow) | the driver under the mandate, recorded in `WP23-decisions.md` |

## The test

`tests/test_interface_contract.py::test_r3_data_file_header_dtypes_rows` is parametrized over
`CASE["data"]` under `CASE["data_dir"]`. The amendment adds the same check over `CASE["v2"]["data"]`
under `CASE["v2"]["dir"]` (one parametrization; the contract test file is the contract's own, not
this stream's) and a check that `case.v2.traded_metrics` equals `cubesat_oracle.ATTRIBUTE_NAMES`.

## Dependencies the driver sees at once

- The headers above are what `experiments/cubesat_oracle.py` writes on `wp23case` (a 20-design
  run of each regime on the host wrote exactly the 33 columns of the primary and baseline files).
- The predictions header depends on `experiments/check_designs.py` `METRICS` following
  `definitions.py` (`settling_time_s` as the time metric); that file is outside the case-code
  stream's blast radius and is named in its report.
- The amendment commits with the regenerated data and the ledger's new entries, never before.

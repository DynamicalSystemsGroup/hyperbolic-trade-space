# Package-user test fixtures

Two small tables for readers who use the package without the case study. Neither has anything to do
with satellites.

- `plain_table.csv`: a synthetic materials-style table (`sample`, `batch`, `strength_mpa`,
  `weight_kg`, `stiffness_gpa`, `cost_usd`), no model behind it. Written by `make_plain_table.py`
  from the package's `make_frontier_data`, then given unit scales and two smaller-is-better columns,
  so it needs conditioning before a fit. Loads with `pandas.read_csv`.
- `pump_trade.sysml`, `export_pump_table.py`, `pump_table.csv`: a small SysML v2 model of a
  centrifugal-pump trade (three design variables, four calculations: flow, head, shaft power, mass)
  and the table it exports. The export script loads the model through the `opensysml` client (the
  `case` dependency group) and has the model evaluate its own `calc def`s for each seeded design; no
  number is copied into the script. It does not use the `sysmlv2` model-checking toolkit of
  `examples/adcs/experiments/toolkit.py`, which checks and verifies models and does not export a
  table. The model shares no element with `examples/adcs/`.

`tests/test_user_test_fixtures.py` regenerates both tables and compares them with the committed
files. Run a generator with `uv run python tests/fixtures/user-tests/<script>.py`.

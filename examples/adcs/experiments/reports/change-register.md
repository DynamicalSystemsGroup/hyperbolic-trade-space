### Register of differences between the frozen generation and v2

Hand-written after the v2 runs (2026-11-09). The generated report includes this file verbatim and
never rewrites it. `tests/test_v2_data.py` (R-15) requires the table of differences below to cover
exactly the columns and aggregates whose difference exceeds the reproducibility tolerance, no more
and no fewer.

**Finding.** No column and no aggregate of any of the four datasets differs from the frozen file by
more than its tolerance. On the generating platform (macOS arm64, Python 3.12.12, opensysml 0.12.1)
the four v2 files are byte-identical to the frozen files (equal sha256), so the maximum relative
difference is 0 in every column. The structure-only reading of OD4 holds: v2 changed where the
model, the sampler and the flags live, and no number. No new physics, constant or attribute was
introduced, although OD4 permitted a redesign.

Differences beyond tolerance (each row covers difference ids of the generated report):

| Row | What | Why | Covers | Downstream numbers that move |
|---|---|---|---|---|

The table has no rows: no difference exists beyond tolerance, and the test fails if one appears
without a row.

Changes that move no number (recorded so the swap gate can read them; the test does not check
this table):

| Row | What changed | Why | Where |
|---|---|---|---|
| NC-1 | The four flags `settled`, `momentum_ok`, `power_ok`, `dod_ok` are the verdicts of the model's requirements (`verify_requirement`, engine `run`, evidence `observed`), not Python inequalities. | Feasibility is a statement of the model (WP15 R-3 and the solver addition at the gate). The flags equal the frozen flags on all 1000 designs of both datasets. | `cubesat_oracle.py`, `feasibility.py`, model section 5 |
| NC-2 | Accounting (masses, powers, usable torque, energy balance, eclipse reserve, power margin, peak slew power, pointing error, depth of discharge) is evaluated by the model's `calc def`s and its `analysis def SlewExperiment` from the measured slew, instead of the frozen model's calcs called one by one. | One legible model; the measured quantities are the only numbers handed in from Python. Results agree to the CSV precision (`%.9g`), hence the identical bytes. | model sections 3 and 6 |
| NC-3 | The sampler reads the enumerations, the ranges and the gain box from the v2 model and draws with the same per-design `SeedSequence` child seeds, in the same order. | R-2: no constants in Python. Design ids, seeds, categorical values and continuous values equal the frozen designs. | `runner.LogUniformSampler`, `cubesat_oracle.build_sampler` |
| NC-4 | The settling time is the last time the error exceeds the model's `settlingFraction` of its start, computed from the simulation history with the same rule as `SimResult.summary`; the slew times use the model's two bands. | The scenario numbers come from the model (R-2). The values equal the frozen values. | `cubesat_oracle._last_outside`, `_first_inside` |
| NC-5 | When the settling time and the slew time are equal (one integration step crosses both thresholds: 1 design of the primary dataset, 5 of the baseline dataset), the analysis is called a second time with the slew time one float step higher and the two pass-through attributes are taken from the measurement. | The runtime (opensysml 0.12.1) refuses an analysis that returns a unique tuple with two equal entries (`uniqueness violation`); the first generation attempt stopped on such a design. No computed attribute depends on either value. The model could return the attributes as a non-unique feature or omit the two pass-through entries; `model_v2/` was not edited (owner: 15.1). | `cubesat_oracle._analyse` |
| NC-6 | Each v2 ledger entry stores the solver's classification of the declared ranges in `inputs.exclusion` before any design is simulated: power region all-feasible, battery region mixed, nothing excluded. | The gate addition: the solver excludes infeasible regions and model variants before simulation, and the ledger records what was excluded and why. A model variant with no feasible configuration raises before simulating. | `cubesat_oracle.exclusion_block`, `build` |
| NC-7 | The check predictions are re-proposed from the v2 primary data by the same method (fit, holes, seeded pool); all three proposals coincide with the frozen proposals. The six check designs are simulated through the runner, committed after the predictions entry exists. | The default of the scope: predict, then simulate, order enforced by the ledger parents. | `check_designs.py` |
| NC-8 | The scenario is addressed by the model's part name `nominalSlew` in the experiment declarations (the first draft of `definitions.py` carried a descriptive label, `slew30deg-600s-0p5s`, that names no part of the model). | R-2: the scenario is read from the model by name. | `definitions.py` |
| NC-9 | Provenance exists: every dataset, frozen and v2, has a ledger entry with its hash. `git_dirty` is true in the v2 entries because other packages' files were untracked in the working tree when they ran. | R-10, R-11. The code hashes in each entry identify the exact files. | `ledger/ledger.jsonl` |

Platform. The equality is a statement about this platform. The reproducibility tests keep their
tolerances (rtol 1e-3 on the aggressive box, saturated fraction 10 percent, times within 0.5 s)
because ODE output is not bit-reproducible across platforms (WP4 Amendment 1); `verify` checks the
committed bytes only.

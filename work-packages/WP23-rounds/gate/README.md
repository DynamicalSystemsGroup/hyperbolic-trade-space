# WP23 data gate: the regeneration of record (2026-11-10)

This folder holds the diagnostic pair of the gate (D-6 on the data of record: `heatmap.png`, the
primary regime; `heatmap_baseline.png`, the baseline regime; `k3_record.md`; `coverage.md`, copied
from beside the coverage table) and this record of the regeneration (D-8, G8, R-12): what ran,
where, on which commit and image, how long, and the hash of every regenerated file old and new.
The comparison of old and new (every moved number and changed conclusion with its cause, D-9) is
the gate section of `work-packages/swap-evidence.md`, written by the comparison agent from the old
files kept outside the repository and the new files committed here; the hand-written cause of each
difference beyond tolerance is `examples/adcs/experiments/reports/change-register.md` (CR-1 to CR-4).

## What was regenerated, and on what

- Model: `examples/adcs/model_v2/cubesat.sysml`, the WP23 revision adopted at this gate (sha256
  `fb1dbd061610...`; the WP22 version it replaced, `0a0b4a4b64d1...`, stays in history at d3018ba
  and in the old-files folder as `cubesat_wp22.sysml`).
- Code: the tree at commit `2b2e94e` (the gate branch rebased on `dev` 6c32981; the files the
  ledger hashes, `adcs_sim.py`, `cubesat_oracle.py`, `feasibility.py`, `check_designs.py`, are
  those of the D-3 commits plus the reach rule of `check_designs.py`, below). The fit is `case.py`
  at `dev`, unchanged, with its defaults.
- Environment: the container of record `hts-paper`, image id `3c7cfc8a2e27` (full
  `sha256:3c7cfc8a2e27081f14c793e5b88dbe62cda271dc29137435d7187ffe8f5dca4e`), built at `2b2e94e`
  by `sh paper/container/build.sh` (30 s, cached layers; the previous image `c798757482d7`, built
  at the superseded head 110bdd4, removed in the same step); linux/arm64, Python 3.12.16,
  `HTS_ENVIRONMENT_OF_RECORD=1`, `EXPERIMENTS_WORKERS=3`, `--network none`. `git log -1` inside
  prints `2b2e94e6ca795251383ae76da14b8733a81c124b`; `git status` before the run is clean.
- The settling time is read by event detection (the last exit from the band, WP16 D-7, D-3);
  the slew time is not measured (G5). Sampling, seeds and scenario constants are unchanged.

## Commands, in order, and wall times

Container step 1 (`hts-wp23gate` from the image, script `run1.sh` of the session scratch; one
tree, the five entries one unit):

| step | command (in `/app`, `REQUIRE_OPENSYSML=1 PYTHONPATH=examples/adcs`) | wall | result |
|---|---|---|---|
| ledger | `uv run python examples/adcs/model_v2/ledger_gate.py --image 3c7cfc8a2e27` | 459 s | five entries appended, none dirty (below) |
| coverage | `uv run python examples/adcs/model_v2/coverage.py` | 22 s | `views/coverage.{md,csv}` regenerated from `cubesat.sysml` |

The first-20 recording in that script was written as a here-document on standard input; the
oracle's worker pool (spawn) cannot import a main module named `<stdin>`, and the step failed
before writing anything. The five entries and the coverage table were copied out, the container
removed, and a second container of the same name was created from the same image with those
files copied in (so its tree is the first container's after step 1), running `run3.sh`:

| step | command | wall | result |
|---|---|---|---|
| recording | `uv run python /tmp/record20.py` (the test's own runner call, `tests/test_cubesat_oracle.py`, as a file) | 11 s | `tests/data/v2_first_designs_of_record.csv`, output `894277fb237c...` |
| the pair | `uv run python examples/adcs/model_v2/diagnostic_pair.py --dataset examples/adcs/data/v2/adcs_designs_cubesat.csv --gains examples/adcs/data/v2/adcs_designs_cubesat_gains.csv --out work-packages/WP23-rounds/gate` | 26 s | this folder's `heatmap.png`, `heatmap_baseline.png`, `k3_record.md`, `coverage.md` |
| compare | `uv run python -m experiments compare` | 5 s | the report, with the register as it stood |
| verify | `uv run python -m experiments verify` | seconds | `34 entries (11 current); 0 drifts` |

On the host afterwards: the change register rewritten (CR-1 to CR-4, covering exactly the
report's differences beyond tolerance), `compare` re-run so the committed report embeds it,
`verify` again `0 drifts`. The views of the model (`assembly_view`, `behavioural_view`, the
caption) are the generator's revision 5 on the host (PlantUML on the Mac; byte-equal to round 4's
text), not a container output.

A first container run at the superseded head 110bdd4 (image `c798757482d7`) produced the same
primary and baseline bytes and stopped at the check predictions (`fewer than 3 reachable,
separated holes`): the record of that stop and of the reach rule that replaced the typed constant
is `WP23-review.md`, "REACH: the rule and the value", and `WP23-decisions.md`, "The proposer's
reach on the settling-time view". In the run of record the proposer printed
`reach 0.6222 (quantile 0.02 of the nearest predicted distances of the 300 most isolated holes);
3 of 3 proposals` (the Mac gives 0.6222 to four decimals).

## Ledger entries

| new entry | supersedes | parents | output sha256 (first 12) | rows | dirty | commit | time (UTC) |
|---|---|---|---|---|---|---|---|
| `v2-primary@5` | `v2-primary@4` | none | `0bc823ceaf51` | 1000 | False | 2b2e94e | 2026-11-10T06:35:08Z |
| `v2-baseline@5` | `v2-baseline@4` | none | `4ec7514e9ac5` | 1000 | False | 2b2e94e | 06:38:48Z |
| `v2-check-predictions@5` | `v2-check-predictions@4` | `v2-primary@5` | `6b65b2843a99` | 3 | False | 2b2e94e | 06:38:54Z |
| `v2-check-designs@5` | `v2-check-designs@4` | `v2-check-predictions@5` | `b6facc345c68` | 6 | False | 2b2e94e | 06:38:58Z |
| `scope-sensitivity-shared-subspace-v2@4` | `scope-sensitivity-shared-subspace-v2@3` | none | `3e0d7df6cab8` | 20 | False | 2b2e94e | 06:39:07Z |

Each entry's note names the gate and the image id; `model_sha256` is `fb1dbd061610...` in all
five; platform `Linux-6.8.0-50-generic-aarch64-with-glibc2.41`. `git_dirty` is False for all five
because `ledger_gate.py` excludes the unit's five outputs and the ledger from the clean-tree
check (through `runner.run`, which excludes only the entry's own output, the second entry onward
was marked dirty by the first's regenerated file in the first run).

## Hashes of every regenerated file, old and new

The old files are kept outside the repository for the comparison agent, in the session scratch
folder `wp23-gate-old/` with `SHA256SUMS.txt` (the committed state at `dev` 71a5f74 before this
unit; `cubesat_wp22.sysml` is the model they were made with).

| file | old sha256 | new sha256 |
|---|---|---|
| `examples/adcs/data/v2/adcs_designs_cubesat_gains.csv` | `4dc4ae0b8ebe5e7a8aa747f7a8c11fa7d6b8adb316594c86ae2bda960a6f6ee4` | `0bc823ceaf512e68506fdfeeb415c8d891a659b2f4b2388a971aed8a6ce3532d` |
| `examples/adcs/data/v2/adcs_designs_cubesat.csv` | `9450713cd78cd6e0ce60ebcce0faa78388e53eba14256192a50b9ce5a9517bfa` | `4ec7514e9ac55ab2ee94bb4ac693ee927f1f659e45dd702ad4583056698864df` |
| `examples/adcs/data/v2/check_predictions_cubesat.csv` | `5794b7218dd94a71cd5337c16166c22990422b448429f11d8cc073c9a1bfada1` | `6b65b2843a99cf2b3510f791ab956e664a0ac488a94881cb606ead27d2522b39` |
| `examples/adcs/data/v2/check_designs_cubesat.csv` | `3e06e69bb3453099aa44bb502e798c68e4f8f63f6cf5e1fcfe927d2dc8030782` | `b6facc345c68e8d7d029e55b8f3dbedd40c5009777f248484a84261324742b2a` |
| `examples/adcs/data/scope-sensitivity/scope_sensitivity_v2.csv` | `97193d955a730bea73e6f2f082fdb02584321e422487ffc2a2a6c69a91ce1c84` | `3e0d7df6cab87092831416ad47c1754e10890a33d34e581f274f9d53d0b9c304` |
| `examples/adcs/experiments/ledger/ledger.jsonl` | `f23c9e0a7abf28749dc1d105c8dfc2bba1e6c7fce663c4caa2bcae6244080058` | `266dc9b6eea1932759456be24cfdee2a6f1285d1c9d39b76face91bb56dd1c5a` |
| `examples/adcs/model_v2/views/coverage.md` | `4056609198a231cdb5c63af272b9d448381ef85fd48ffa3301690cb3d37e9bf0` | `b2b6877565825883fb591fc32209ba66dd1dacd8df6ac3f5849cde5c7096f099` |
| `examples/adcs/model_v2/views/coverage.csv` | `2213a8a1a03ef3dc68d3c46dc0a2230b70e02aef095c7de2e03b40cf1b70cc15` | `494b10e961980aee03fa2fc1d63d6791a91ea1871ff0775811c77afb8802653f` |
| `tests/data/v2_first_designs_of_record.csv` | `1943d76cb2a6123d905b5b1761672c9b39f23e008f3f1092b5e5f47ba992d705` | `894277fb237c204fbaabae58eff718e8458271bb9b4f79b07f7705113b68cbeb` |
| `examples/adcs/experiments/reports/v1-v2-comparison.md` | `42f12d6c19c801ee9bd472d349d3eb2194af200f9d4150adfc74af87f646db60` | `cd52c45a1cbc2dfb552f1ca248670f27c13a57fc1fd9658ad9da53cba412772f` |
| `examples/adcs/experiments/reports/change-register.md` | `f1d607bb357bb998c3c5d3ad702606ca6572e2e90c73f3f8515d5a2867427073` | `273e4318e183fb274933547667215efd2cabe108b7ba4cae3842cc5bcf4529e9` |
| `examples/adcs/model_v2/views/assembly_view.puml` (host, revision 5) | `ba0d92f86dbc0f28641b93dee2c139c0beaf51a63724667d1bc804608f729cfb` | `d790de4accbbe253d3e9989626d5bef6b7bc22334003ab22345cbaaaeb2ee6bd` |
| `examples/adcs/model_v2/views/behavioural_view.puml` (host, revision 5) | `2b9e1ce97f117660465aa2299577106923b18742f1c5d7fc4cd19a11165f9d24` | `7fd77c7c536ebab07e0689764d4768b3470545940b41bf1579dcb2f1c3207e35` |
| `examples/adcs/model_v2/cubesat.sysml` (the model, swapped not regenerated) | `0a0b4a4b64d1504c2eb0d408ecba2542240c40d6c2c5fb7567daa2473b1963ef` | `fb1dbd061610ef0a44798b074aed9f9b354e9084fef3102efe0f665a5d395200` |

## What the regeneration shows (the gate's own readings; the comparison is D-9's)

- The two 1000-design tables: the same designs, seeds and categorical values; the four flags
  equal on every design (shares: settled 0.976 and 0.978, momentum_ok 0.812 and 0.919, power_ok
  1.0, dod_ok 0.869 in both); the settling time by event detection within 0.5 s of the frozen
  value on all 2000 designs (largest relative change 0.03); `torque_saturated_frac` beyond its
  tolerance in 3 primary and 35 baseline rows, and `control_effort` in one baseline row, the
  platform of record against the Mac (CR-2); the slew-time columns gone (CR-1).
- The check predictions and check designs: new proposals on the settling-time view with the reach
  by its rule; two of the three holes map to one seeded configuration, so the six check designs
  are five distinct designs; all three proposals fail `dod_ok` (CR-3, CR-4).
- The coverage table: the structural and empirical verdicts of every cell unchanged; the
  settling-time magnitudes of four cells (TrackerGrade, batteryCapacity, Kp, Kd) moved with the
  event-detected read-off (the header names `cubesat.sysml`, `fb1dbd061610`).
- The pair: in the primary regime the metrics at zero exponent across tau are power margin,
  eclipse reserve and peak slew power; in the baseline regime peak slew power; the same sets as
  rounds 1 to 4 (`k3_record.md`; the n-lemma reading of each is `WP23-review.md`, round 3).
  The fit lines, contending sets, exponents, cells and shares of `k3_record.md` equal round 4's
  (on round 1's host-made tables) to every printed digit, except that three K = 1 exponents of
  the primary regime printed as 0 there print as 1e-17 to 4e-17 here (zero by the figure's 1e-3
  threshold) and the K = 3 gaps G_k differ at 1e-15. K = 1, primary: tau 38.1, 56 near-frontier designs, contending set total mass, energy
  balance, pointing error, depth of discharge, settling time; baseline: tau 45.7, 77 designs,
  control effort, settling time, power margin, pointing error, depth of discharge.
- The first 20 designs of record: 33 columns (the frozen 35 less the two slew times), the
  container's rows, compared byte for byte in the container only.

## Checks after the regeneration

`PYTHONPATH=examples/adcs uv run python -m experiments verify`: 34 entries (11 current), 0 drifts,
no current entry dirty. R-5's greps: `grep -rn "slew_time\|SlewTime" examples/adcs/data/v2`
returns nothing; the model's seven `SlewTime` matches are section 4's closed-form calcs
(`TorqueLimitedSlewTime`, `LinearSlewTime`, `SlewTimeEstimate`), the model-checking evidence of
WP15, read as `WP23-review.md`, "R-5's check, amended", records; the oracle's only `slew_time`
text is the docstring naming the columns that left. The test runs are in the unit's report and
`paper/container/RECORD.md`.

# Record of the container runs (P10)

Run 2026-11-09 on the author's Mac (Apple M1 Max, macOS 26.5.2, arm64) with Colima 0.8.1
(Virtualization.Framework VM, aarch64 guest, Docker server 27.4.0), **linux/arm64 containers, native
(no emulation)**. The platform of record is linux/arm64 (ratified by the supervisor; the spike is
`docs/superpowers/notes/spike-container-platform/report.md`). Repository state: dev at the commit
named in each image (`git log -1` inside the image prints it: the history is rebuilt from a
`git bundle`). Every run below used `--network none`. Nothing was pushed to a registry.

The record has two parts. The first (run at eb8a710) is the P10 delivery. The second, "Regeneration in the
container of record" below, is the unit that followed the supervisor's decision that the container is the source
of the committed exact values (WP10-decisions.md): everything committed as exact was regenerated inside
`hts-paper`, the image was rebuilt at the head that carries it (d66c106), and both images then ran the whole
suite with 0 failed.

## Pins

- base image: `python:3.12-slim` (3.12.16-slim-trixie), pinned by the multi-arch index digest
  `sha256:5e2bdb1b0d542d5039cffb8181c65930093949194a65c365dfb1b0fe13a4fa5b`; the manifests in it:
  linux/arm64 `sha256:c61cffc3bacb94ed026ff8b45d5114b7693dd0420baca0a1ace0e3d0ce9035fd` (used),
  linux/amd64 `sha256:05a994d2344eb364cc186910f4fc8786a38215f39f00d0acc25bff33a08f4177`
- uv version: 0.9.18
- python version: 3.12.16
- Node.js v24.22.2 (linux-arm64 tarball, sha256 `eb187837...` checked, `SHASUMS256.txt.asc` verified
  against the pinned release key; x64 sha256 `48cc0e21...` for a PLATFORM=linux/amd64 build), npm 11.19.1, mystmd v1.12.0
- Debian trixie: glibc (libc6) 2.41, git 2.47.3, gnupg 2.4.7
- lock hash: `uv.lock` sha256 `53228fba6d98414269bf48a0d041849071345afbefaa5c555b84624bb1dd17b3`
- installed: numpy 2.5.4, scipy 1.18.1, sympy 1.14.0, scikit-learn 1.9.1, matplotlib 3.11.2,
  opensysml 0.12.1, z3-solver 5.3.3.0
- image id of `hts-paper` at the final head of the regeneration (d66c106):
  `sha256:92e878ce9d68c34eee6b712bbb7b2d35e45553f535aa358a81f14c37562b2582` (the id changes with every
  commit because the history layer carries it; the earlier run was commit eb8a710, id `4cfe46da2a23...`)
- the robustness image `hts-alt`: Ubuntu 24.04, index digest
  `sha256:fe81560990fae86dc4743202b2cb4d3df98d0bcf949173cecef15ce1127ef852` (CI's distribution; glibc 2.39,
  Python 3.12.3 from apt, git 2.43.0, gnupg 2.4.4), same `uv.lock`, same uv, same Node, image id at d66c106
  `sha256:81e06426f7b32739618ea05d77aae44383b8ec59a8eb4a5a54d26ce93239f7c0` (earlier: `459014909904...`); `HTS_ENVIRONMENT_OF_RECORD=0`
  (not asserting the exact comparisons). A first attempt on `python:3.12-slim-bookworm` failed in
  `uv sync --locked`: the locked z3-solver has no linux/aarch64 wheel for bookworm's glibc 2.36 and
  falls back to a CMake source build (no compiler in the slim image).

## Commands, wall times, results

| command (inside `hts-paper`, `--network none`) | wall time | result |
|---|---|---|
| `sh paper/container/build.sh hts-paper` (cold) | about 3 min | RECORD: image built |
| `docker run --rm --network none hts-paper` | 12 s | RECORD: toolchain printed; derivation chain ends "ALL LEMMAS PASS." |
| `uv run python -m derivation.proofmap` | seconds | PROOF MAP OK: 17 lemma files, 364 tagged steps |
| `uv run pytest -q tests/test_derivation.py` | 107 s | RECORD: 103 passed |
| `uv run python paper/paper_common.py` | 4 s | regenerates `paper/environment_reference.npz` |
| `uv run python paper/execute_notebooks.py` | 146 s | both notebooks executed |
| `sh paper/container/build-paper.sh` | 5 s | site built offline (135 files in `paper/_build/html`) |
| `uv run pytest -q -n 4` after the regeneration, `HTS_ENVIRONMENT_OF_RECORD=1` | 655 s | RECORD: 46 failed, 2011 passed, 17 skipped, 1 xfailed |
| same suite in `hts-alt` (after its own notebook execution and paper build) | 668 s | RECORD: 4 failed, 2053 passed, 17 skipped, 1 xfailed |

## The 46 failures in the environment of record (at eb8a710; resolved below)

All are exact (bit-identical) comparisons against recordings made on the Mac, which the image cannot
reproduce (different maths library and BLAS): `tests/test_soft_fit.py::test_r2_default_planted_fits_equal_the_recording`
(43), `::test_r2_default_cubesat_fits_equal_the_recording` (2), and
`tests/test_cubesat_oracle.py::test_declared_space_excludes_nothing_so_the_first_designs_are_unchanged` (1: settling_time_s
differs from the Mac rows by up to 0.05 s, inside the stated 0.5 s tolerance). The data files are outside this package's files:
`tests/data/soft_fit_default_reference.npz` and the recorded first designs. With `HTS_ENVIRONMENT_OF_RECORD` unset the soft-fit
test fails in the same image for four cases only (below). On the committed notebooks (not regenerated in the image) with the
variable set, `tests/test_paper.py::test_c_committed_output_is_current` also fails (the planted table's digest, below).

## Values that differ

Committed (Mac, arm64) against the container of record:

| quantity | committed | container |
|---|---|---|
| SHA-256 of the planted table (Appendix C datasets row) | c127dd4c99380d0409a7144811785537b272b0ad80bf64e3b6a6bcd0d9f8993f | b17d4f8fdd4679239900073994631fb76e806d84599f8805f1c4089d9e8e7add |
| `environment_reference.npz` arrays (planted_X, figure1_u, logV, Z) | Mac values | relative differences up to 3.5e-15 (planted_X), 1e-12 on single entries of figure1_u near zero; figure1_facet, design, corners, W, BETA bit-equal. Tolerance elsewhere: 1e-9 |
| Figure 1 data hash | pinned 4040cb8e... (Linux) | equal |
| paper figures (7 PNGs) and notebook metadata (interpreter, platform, Node.js, commit, locked-package count) | Mac | regenerated; the executed notebooks and figures are kept in the session scratchpad, not committed here |
| ConvergenceWarning text in two output cells (D.14 fit, iteration cap) | absent | present (stderr; the table is the same) |
| mean settling time of the first 20 v2 designs | Mac rows | up to 0.05 s |

`hts-paper` against `hts-alt` (Ubuntu 24.04, same arm64 hardware): all 69 executed notebook code cells give the same text
(including the planted-table digest b17d4f8f...) except the build-environment table (interpreter 3.12.16 / 3.12.3, glibc 2.41 /
2.39, commit); `environment_reference.npz` is bit-identical in both images. The only failures in `hts-alt` are four
`tests/test_soft_fit.py::test_r2_default_planted_fits_equal_the_recording` cases, K = 3, tau = inf, seeds 0 to 3: the same three
facets are found but numbered in another order (and the `facet_` label array differs with them), and for seed 2
`term_objective_change` differs by 5.3e-5 (0.3 percent) of a quantity that depends on the final step. This is the facet-numbering
label of gap G-10 in a test that compares labels exactly; reported to the PM, no tolerance changed.

## Regeneration in the container of record (R-31, head e699a54 regenerated, d66c106 final)

Steps, each `--network none`, in hts-* containers only: `sh paper/container/build.sh` at e699a54 (image
`a87ce242d641`, nothing committed before it); `docker run --name hts-exec hts-paper sh -c "uv run python
paper/paper_common.py && uv run python paper/execute_notebooks.py && sh paper/container/build-paper.sh"`
(2 min 35 s); the notebooks, `paper/figures/` and `environment_reference.npz` copied out with `docker cp`;
the soft-fit reference re-recorded inside the image with the test's own case list (1273 arrays as before,
plus the field `recorded_on` = linux, aarch64); the first 20 v2 designs re-run inside the image by the same
runner call the test makes. Committed: 03189c5 (outputs and figures), d66c106 (recordings, tests, values file).
Source and markdown cells of both notebooks are unchanged (checked cell by cell); datasets (CSVs) untouched.

| command | wall time | result |
|---|---|---|
| `sh paper/container/build.sh` at d66c106 (cached layers) | 37 s | RECORD: `hts-paper` 92e878ce9d68, `git log -1` inside prints d66c106 |
| `uv run pytest -q -n 4` in `hts-paper`, `HTS_ENVIRONMENT_OF_RECORD=1` | 593 s | RECORD: 2120 passed, 17 skipped, 1 xfailed, 0 failed |
| same in `hts-alt` rebuilt at d66c106 (no flag) | 555 s | RECORD: 2120 passed, 17 skipped, 1 xfailed, 0 failed |
| `uv run pytest -q -m 'not slow' -n auto --dist loadgroup` on the Mac, no flag | 60 s | RECORD: 1679 passed, 16 skipped, 1 xfailed, 0 failed |
| `tests/test_soft_fit.py` and the first-designs oracle test on the Mac (slow tests), no flag | 90 s | RECORD: 59 passed |

### What changed against the values committed before (Mac), with the tolerance of each row

| item | committed | regenerated in `hts-paper` | tolerance | reason |
|---|---|---|---|---|
| SHA-256 of the planted table (Appendix C datasets row) | c127dd4c99380d0409a7144811785537b272b0ad80bf64e3b6a6bcd0d9f8993f | b17d4f8fdd4679239900073994631fb76e806d84599f8805f1c4089d9e8e7add | exact in the container; elsewhere the table's values within rtol 1e-9, atol 1e-12 (`planted_table_sha256`) | maths library and processor |
| `environment_reference.npz` (planted_X, figure1_u, logV, Z; figure1_facet, design, corners, W, BETA) | the container values of the earlier run | bit-identical to the committed file (no change) | rtol 1e-9, atol 1e-12 elsewhere | none |
| Figure 1 data hash | 4040cb8e... (Linux) | equal | values within 1e-9 elsewhere | none |
| the 7 paper figures (PNG) | Mac renders | pixel-identical to the committed ones (0 differing pixels in six, 27 pixels by one level in fig-tau-sweep); the file bytes differ (encoder) | figures are not compared byte for byte | PNG encoding |
| notebook metadata and build-environment table | Python 3.12.12, macOS-26.5.2-arm64, Node v23.7.0, 176 locked packages, commit f6c5df37 | 3.12.16, Linux-6.8.0-50-generic-aarch64-with-glibc2.41, Node v24.22.2, 178 locked packages, commit e699a54f | observed, not compared | the environment of record; the lock grew from 176 to 178 packages since the old build |
| ConvergenceWarning (D.14 fit, iteration cap; stderr) in one cell of `paper.ipynb` and one of `supporting_material.ipynb` | absent | present; the printed table is the same | not compared | the iteration-cap fit warns where the Mac run did not |
| every other output cell (text, tables, numbers) of the 69 executed code cells | | identical | text_rtol 1e-3 elsewhere | none |
| `soft_fit_default_reference.npz`: 43 planted and 4 cubesat fits, 1273 arrays | Mac recording | all 47 fits differ in the last bits: largest absolute difference outside the four cases below 1.3e-13 (a conditioning number; exponents 1.9e-15, objective 4.2e-16, gaps 6.6e-15) | bit-identical in the container; 1e-12 elsewhere | maths library and BLAS |
| the same, planted0 to planted3, K = 3, tau = inf (4 fits) | Mac | the same three facets, numbered in another order for planted0 (237 labels), one tied row relabelled for planted1 and planted3; `n_iter_` 7 to 2 (seed 0) and 3 to 50 (seed 3, status `stationary_without_margin` to `iteration_cap`, `term_objective_change` 2.9e-4 to 2.2e-16); support weights differ in about 60 of 400 rows by up to 0.013; `term_objective_change` 5.3e-5 (seed 2) and 0.11 (seed 0) | facets matched by exponent vector within 1e-6, labels equal except on tied rows (EPS_FEAS), shares within 0.01 per relabelled row; the final-step quantities are not compared off the recording's platform | gap G-10: a degenerate LP whose solution and last steps follow the maths library |
| first 20 designs of the v2 primary dataset, 35 columns | Mac rows (the committed CSV) | 10 columns differ: settling_time_s up to 0.0505 s (15 rows, relative 2.9e-3), slew_time_s 0.030 s, slew_time_05deg_s 0.080 s, torque_saturated_frac 0.0046 (12 rows), control_effort 4.5e-6, the others at or below 7e-8; labels, flags and identifiers equal | byte-equal to the recording `tests/data/v2_first_designs_of_record.csv` in the container; elsewhere rtol 1e-3, times within 0.5 s, saturation within 0.01 (`v2_first_designs_rows`) | the adaptive solver's accepted steps |

### Conclusions

Unchanged. The contending sets, leading metrics, signs, certificates and check outcomes, and the counts
(671 of 706 among them), are in the notebooks' text outputs, which are identical cell for cell apart from the rows
above. The soft-fit reference and the first designs are test recordings, not printed results; their changes are at
the level of rounding, of facet numbering and of a degenerate fit's final steps (above).

### Test changes made with the regeneration

- `tests/test_soft_fit.py`: `RECORDED_ON` is read from the recording (`recorded_on`, now linux and aarch64); off that
  platform the tau = inf planted comparison no longer compares the status and reason, the iteration counts, the last
  objective change and the support weights (`RELAXED_SKIP`), and allows 0.01 per relabelled row on the facet shares.
  This widens a tolerance, for the four K = 3 cases of gap G-10 only, and is for the PM to ratify; the facets, exponents
  (1e-6) and labels keep their comparisons.
- `tests/test_cubesat_oracle.py`: in the container of record the first designs are compared byte for byte with
  `tests/data/v2_first_designs_of_record.csv` (a new file, the container's rows) instead of the Mac-made dataset; elsewhere
  the frozen tolerances against the dataset, unchanged. The dataset was not touched (WP16).
- `paper/environment_values.toml`: the reasons of two values updated; no value or tolerance changed.

### R-9: images and containers before and after

Read-only listings (`docker images`, `docker ps -a`, `docker system df`) taken before the first build and after the
last container was removed (full text kept in the session scratchpad). By image and container id, nothing outside the
hts- family differs.

| | before | after |
|---|---|---|
| `hts-paper` | 4cfe46da2a23 (latest) | 92e878ce9d68 (latest); 4cfe46da2a23 now untagged |
| `hts-alt` | 459014909904 (latest) | 81e06426f7b3 (latest); 459014909904 now untagged |
| `hts-spike-arm64`, `hts-pre` | bc79b10f891e, e739a4ba28cd | unchanged |
| untagged build layers created in this unit | | a87ce242d641 (the first rebuild at e699a54) |
| `docker system df`, images | 70 images, 43.53 GB | 73 images, 48.63 GB (the three new ids above) |
| `docker ps -a` | 21 containers, none hts-*, all the user's, exited | 21, the same ids; the hts-exec, hts-rec, hts-suite, hts-suite2 and hts-suite3 containers created here were removed by name |
| `docker system df`, containers | 21, 159.1 MB | 21, 159.1 MB |
| free disk of the Mac volume (`df -h /`) | 15 GiB | 17 GiB; memory and disk were not short at any point |

No image or container outside the hts- family was created, started, stopped or removed; no `colima` command was issued
and `~/.colima` was not touched.

## Regeneration of the recovery cells (the iteration-cap warning, 2026-11-09)

The committed output of the D.14 recovery cell (`tab-D-planted_recovery`) and of the Section 9 sentence that
reads the same fits (`num-recovery`) carried one stderr line, the estimator's ConvergenceWarning at the
alternation's iteration cap (driver-log, "A warning leaks into the rendered paper"). Two changes preceded
the regeneration: the estimator warns at the cap only when the max term gap or the last objective change
exceeds `tol` (18d0064), and D.14's closing paragraph reports the platform-stable status counts (the gap
of every fit against `tol`; the cap count itself differs by platform and stays unprinted, as the audit in
`paper/environment_values.toml` says). A test now asserts that no committed output of either notebook
carries a stderr stream or a warning's text (`tests/test_paper.py::test_committed_outputs_carry_no_stderr_or_warning`).

Steps, each `--network none`, in `hts-*` containers only: `sh paper/container/build.sh` at 04df5c3 (the head
carrying the generator and the test, before the regenerated outputs were committed), image `hts-paper`
`57a0f23716f4`; the previous image `92e878ce9d68` removed in the same step; `docker run --name hts-exec
hts-paper sh -c "uv run python paper/paper_common.py && uv run python paper/execute_notebooks.py && sh
paper/container/build-paper.sh"` (2 min 22 s); both notebooks copied out with `docker cp`; `hts-exec`
removed by name. Only the outputs of the two recovery cells were taken into the committed notebooks.

| item | result |
|---|---|
| the 40 fits of D.14 inside the image (seeds 0 to 19, tau = infinity and 50) | at the exact maximum seed 3 stops at the iteration cap (50 rounds, max term gap 6.7e-16), seeds 1, 8 and 16 `stationary_without_margin`; every other fit `certified`; the largest term gap of every fit is below `tol` (1e-10); no warning is raised |
| the same fits on the Mac (arm64, no flag) | no fit reaches the cap (seeds 1, 3, 8 and 16 `stationary_without_margin` at the exact maximum); every gap below `tol`; the printed sentence is identical, as designed |
| `tab-D-planted_recovery` | the stderr stream gone; the tables unchanged (16 of 20 at both temperatures, seeds 1, 3, 8, 16); the closing paragraph carries the counts (40 of 40 below `tol`, none at the cap with a gap at or above it) |
| `num-recovery` (paper.ipynb) | the stderr stream gone; the sentence byte-identical |
| every other executed cell | text identical; two figure cells of the paper differ in PNG bytes (encoder) and five sentence cells in output metadata only, the build-environment table in its commit; none taken |
| `uv run pytest -q tests/test_paper.py` on the Mac (slow included), no flag | 1 failed, 142 passed, 4 skipped (89 s): the failure is `test_cr2`'s `ids.index("fig-plane-k1")`, a cell id the paper stream renamed in cc409f8 (WP19 P-5) before this unit; its D.14 and sentence assertions, run by hand against the committed cells (`_current`, the row patterns, `in 16, at the exact maximum`), all hold; the new stderr test passes |
| `uv run pytest -q tests/test_claims_register.py` | 1 failed, 20 passed: C150 cites `test_convergence_warning_keyed_to_iteration_cap`, removed by 18d0064 (the estimator unit's row to mend) |

## Regeneration of the v2 data at WP23's data gate (2026-11-10, head 2b2e94e)

The v2 datasets, the check designs, the scope-sensitivity table, the coverage table and the first-20
recording were regenerated once in `hts-paper` on the WP23 model (`cubesat.sysml`, sha256
`fb1dbd061610...`, adopted at the gate; the slew time out, the settling time by event detection,
WP16 D-7 and WP23 D-3). The full account, with the hash of every regenerated file old and new and the
five ledger entries, is `work-packages/WP23-rounds/gate/README.md`; the hand-written cause of each
difference beyond tolerance is `examples/adcs/experiments/reports/change-register.md` (CR-1 to CR-4);
the comparison of old and new (D-9) is the gate section of `work-packages/swap-evidence.md`.

Steps, each `--network none`, in `hts-*` containers only: `sh paper/container/build.sh` at 2b2e94e
(30 s, cached layers), image `hts-paper` **`3c7cfc8a2e27`**
(`sha256:3c7cfc8a2e27081f14c793e5b88dbe62cda271dc29137435d7187ffe8f5dca4e`), the previous image
`c798757482d7` (built at the superseded head 110bdd4, whose run reproduced the same primary and
baseline bytes and stopped at the check predictions) removed in the same step; `docker create --name
hts-wp23gate --network none -e EXPERIMENTS_WORKERS=3 hts-paper sh /tmp/run1.sh 3c7cfc8a2e27`, the
script copied in, `docker start -a`; the outputs copied out with `docker cp`; a second container of
the same name, same image, with those outputs copied in, for the steps after the first script's
here-document recording failed (the oracle's spawned workers cannot import a `<stdin>` main module);
`hts-wp23gate` removed by name.

| command (inside `hts-paper`, `--network none`, `HTS_ENVIRONMENT_OF_RECORD=1`) | wall time | result |
|---|---|---|
| `uv run python examples/adcs/model_v2/ledger_gate.py --image 3c7cfc8a2e27` | 459 s | RECORD: `v2-primary@5`, `v2-baseline@5`, `v2-check-predictions@5`, `v2-check-designs@5`, `scope-sensitivity-shared-subspace-v2@4`; `git_dirty` False in all five; the proposer printed `reach 0.6222 ...; 3 of 3 proposals` |
| `uv run python examples/adcs/model_v2/coverage.py` | 22 s | `views/coverage.{md,csv}` from `cubesat.sysml`; every verdict unchanged, four settling-time magnitudes moved |
| the first 20 v2 designs by the test's own runner call (`/tmp/record20.py`) | 11 s | `tests/data/v2_first_designs_of_record.csv`, 33 columns, output `894277fb237c...` |
| `uv run python examples/adcs/model_v2/diagnostic_pair.py ... --out work-packages/WP23-rounds/gate` | 26 s | the gate's pair; zero-exponent sets as rounds 1 to 4 |
| `uv run python -m experiments compare` | 5 s | the report (re-run on the host after the register was written) |
| `uv run python -m experiments verify` | seconds | RECORD: `34 entries (11 current); 0 drifts` |

What changed against the committed files (the gate's reading; the comparison agent's D-9 section is
the record): the slew-time columns left all four v2 files and the first-20 recording (35 to 33
columns); the settling time, now event-detected, stays within 0.5 s of the frozen value on all 2000
designs (largest relative 0.03); `torque_saturated_frac` differs beyond its tolerance in 3 primary
and 35 baseline rows and `control_effort` in one baseline row (the container's integrator steps
against the Mac's, as the first-20 row of the earlier regeneration above); the flags, ids, seeds and
categorical values are equal on every design; the three check predictions are new proposals on the
settling-time view with the reach set by the rule recorded in `WP23-decisions.md` (the 2nd
percentile of the pool's nearest predicted distances to the 300 most isolated holes, 0.6222 here;
the typed 0.35 of WP7 admitted none on this view), two of them one configuration; the check designs
carry them. The frozen files under `examples/adcs/data/` are untouched. The paper's numbers were
not regenerated here (WP16 order step (4) and WP19 follow the gate); the tests that compare the
paper's committed outputs to the data are reported in the unit's report, not changed.

## Regeneration of the paper on the data of record (2026-11-10, head ea46637)

The paper moved onto the data of record (WP16 order step (4), after WP23's swap): the case module reads
`examples/adcs/data/v2/` (ledger entries @5) directly, the four frozen files under `examples/adcs/data/`
staying byte-identical (overwriting them broke the ledger's verification of the adopted entries); the case
spec lost the slew time (nine attributes, one view, three association pairs), and the paper's generators
read the K = 3 per-term report by `case.term_reports`: the library's guard of ten near-frontier rows is
bypassed at the `tension_report` call (`min_near_frontier=0`) and reapplied per term at ten in `case.py`
(`has_reading`, `thin_reason`), so a thin term keeps its fitted row and loses only its association map.

Steps, each `--network none`, in `hts-*` containers only: `sh paper/container/build.sh` at ea46637 (54 s,
cached layers), image `hts-paper` **`f7b7585c7c58`**
(`sha256:f7b7585c7c585e50de8b51d23706251b7fa0a09ed818d8d4bd5673ea8d0e6590`), the previous image
removed in the same step (`3c7cfc8a2e27`, the gate's; and `ca6e52eddb20`, built at an earlier local head of
this unit that overwrote the frozen files, whose run was discarded); `docker create --name hts-paper-exec --network none hts-paper sh
/tmp/run.sh`, the script copied in, `docker start -a`; the outputs copied out with `docker cp`;
`hts-paper-exec` removed by name.

| command (inside `hts-paper`, `HTS_ENVIRONMENT_OF_RECORD=1`) | wall time | result |
|---|---|---|
| `uv run python paper/paper_common.py` | 3 s | `environment_reference.npz` and `environment_values.toml` unchanged |
| `uv run python paper/execute_notebooks.py` | 117 s | both notebooks; every case number equal to the Mac run's at the printed precision |
| `sh paper/container/build-paper.sh` | 5 s | the site built (three favicon 404 lines from the builder's server, no error) |
| `uv run python scripts/build_figures.py` | 99 s | `fig-planes-k1`, `fig-planes-k3`, `fig-chart-level`, `fig-nlemma` (bytes only) rewritten; the two model views unchanged |
| `uv run python examples/adcs/k_terms.py` | 58 s | `examples/adcs/figures/k3_*.png`; the primary K = 3 tension panel of term 2 states its reason (3 of ten) |
| `uv run pytest -q -n 4` on the paper's test files (`test_paper`, `test_case`, `test_k_terms_case`, `test_notebook`, `test_paper_sources`, `test_paper_static_figures`, `test_narrative`, `test_claims_register`, `test_sensitivity`, `test_gaps`, and `test_experiments`, `test_v2_data`, `test_interface_contract` for the untouched frozen files and the ledger) | 200 s | 465 passed, 4 skipped |

What changed against the committed values is the data's change, read at the gate: the comparison of old and
new (D-9, `work-packages/swap-evidence.md`, the gate section) separates the column change from the
regenerated data, and its part 5 lists each cell of the paper that moved with its cause. The jitter record
`examples/adcs/experiments/reports/sensitivity.json` (D-6) was rewritten on the Mac from five regenerations
on the WP23 model (19 min): every listed conclusion is identical, the settling time moves by at most 1e-6 s,
and the ranges also hold the difference between the Mac and the environment of record. The recovery cells
(`num-recovery`, `tab-D-planted_recovery`) carry no stderr stream and no warning (18d0064); their sentence is
unchanged. The environment of record is now `f7b7585c7c58`.

## Re-recording of the default cubesat fits on the data of record (2026-11-10, head 69d20fe)

`tests/data/soft_fit_default_reference.npz` held the four default cubesat fits (primary and stock, K = 2 and 3) of the old data;
since ea46637 the case reads `examples/adcs/data/v2/` (the recorded K = 2 primary tau was 113.2, the fit gives 94.4), so
`test_r2_default_cubesat_fits_equal_the_recording[primary]` and `[stock]` failed on the Linux run at 628df90. The image is
unchanged, `hts-paper` `f7b7585c7c58` (`git log -1` inside prints ea46637).

Command: `docker create --name hts-softfit --network none -e HTS_ENVIRONMENT_OF_RECORD=1 hts-paper uv run python /tmp/rec_cubesat.py`,
the script copied in, `docker start -a` (66 s), the result copied out with `docker cp`, the container removed. The script runs the
test's own routine (`case.load_study`, `case.fit_study(K)`, `_record` of `tests/test_soft_fit.py`) for the four fits and writes
their 112 arrays; these replace the cubesat arrays of the file, and the 43 planted fits (which do not read the case data) are
kept. The file holds 1274 arrays as before (1273 and the field `recorded_on` = linux, aarch64). The test is unchanged.

| check | result |
|---|---|
| `uv run pytest -q tests/test_soft_fit.py` in `hts-paper` (a fresh container, the new file copied in), `HTS_ENVIRONMENT_OF_RECORD=1`, exact branch | 195 s: 58 passed |
| the same on the Mac, tolerance branch, slow tests included | 203 s: 58 passed |

## Regeneration after the review of the paper's move (2026-11-10, head 2155775)

The paper's fix-forward after the review (`work-packages/swap-evidence.md` part 6, dispositions in part 7). Steps,
each `--network none`, in `hts-*` containers only: `sh paper/container/build.sh` at 2155775 (the local head, on `dev` as 5270bf2 after the rebase; `tab-F-toolchain` prints it) (32 s, cached
layers), image `hts-paper` **`8e91e07fb08f`**
(`sha256:8e91e07fb08fe61dc3c2dd95b465a686ea249a5f731aef9dc26d3efcf2f1ac6b`), the previous image `f7b7585c7c58`
removed in the same step (`docker rmi`, no container on it); `docker create --name hts-paper1c --network none
hts-paper sh /tmp/run.sh`, the script copied in, `docker start -a`; the outputs copied out with `docker cp`;
`hts-paper1c` removed by name.

| command (inside `hts-paper`, `HTS_ENVIRONMENT_OF_RECORD=1`) | wall time | result |
|---|---|---|
| `uv run python paper/paper_common.py` | 3 s | `environment_reference.npz` and `environment_values.toml` unchanged |
| `uv run python paper/execute_notebooks.py` | 118 s | both notebooks; outputs changed only in `num-predict-reading`, `fig-tensions-k3`, `tab-D-stability`, `tab-F-toolchain` (the commit) |
| `sh paper/container/build-paper.sh` | 4 s | the site built (three favicon 404 lines from the builder's server, no error) |
| `uv run python scripts/build_figures.py` | 100 s | no paper figure but `fig-tensions-k3.png` changed; the two model views byte-equal to the committed copies |
| `uv run pytest -q -n 4` on `test_paper`, `test_case`, `test_k_terms_case`, `test_paper_sources`, `test_paper_static_figures`, `test_narrative`, `test_claims_register`, `test_sensitivity` | 137 s | 257 passed, 4 skipped (the gated ones) |
| `PAPER_EXECUTE=1 uv run pytest -q tests/test_paper.py -k "perturbation or clean_kernel or facet_order"` | 400 s | 4 passed (the perturbation test with `num-margin` listed; the clean-kernel test byte-equal) |

What changed: `num-predict-reading` (the antecedent, three proposals of two designs); the D.11 head (the jitter's
magnitudes dropped: no committed record holds the attributes' movement); `fig-tensions-k3` (the thin term's title
and sentence above term 3's map, 60 px where its panel took about 250, figure 1360 px tall from 1480);
`tab-F-toolchain` (the build commit). No number of the paper moved. `num-margin` is unchanged (11 of the 706 in the
fit of record) and is now listed under `[perturbation].moves_under_restart_shift` with its audit line. The
environment of record is now `8e91e07fb08f`. The soft-fit recording above (made in `f7b7585c7c58`) was re-checked in
it after the rebase: `uv run pytest -q -n 4 tests/test_soft_fit.py` with the recording and the test of `dev` 4bd6bac
copied in, exact branch, 81 s: 58 passed (container `hts-paper1c-sf`, removed).

## Regeneration after the rename of the model object's names (WP24 push 1, 2026-11-10, head 541efcd)

The word "facet" left the package, the case code and the paper's generators (WP24 push 1, interface-contract
amendment 14): the generated table headers, keys and figure labels say "term" (and "cell" for the assignment).
Steps, each `--network none`, in `hts-*` containers only: `sh paper/container/build.sh` at 541efcd (the local
head; `tab-F-toolchain` prints it) (31 s, cached layers), image `hts-paper` **`9c8a0c616386`**
(`sha256:9c8a0c61638691f5374ec857604eabfc0f960aeef3a48a10caaf622082c779bc`), the previous image `8e91e07fb08f`
removed in the same step (`docker rmi`, no container on it); `docker create --name hts-wp24 --network none
hts-paper sh /tmp/run.sh`, the script copied in, `docker start -a`; the outputs copied out with `docker cp`;
`hts-wp24` removed by name, then created again for Figure 1 and the two corrected test pins, and removed.

| command (inside `hts-paper`, `HTS_ENVIRONMENT_OF_RECORD=1`) | wall time | result |
|---|---|---|
| `uv run python paper/paper_common.py` | 3 s | `environment_reference.npz`: the array `figure1_facet` is now `figure1_term`, its bytes and the other eight arrays' unchanged; `environment_values.toml` not rewritten |
| `uv run python paper/execute_notebooks.py` | 116 s | both notebooks; 4 output cells of the paper and 12 of the supporting material change in words only (no numeric token moves), and `tab-F-toolchain` in the build commit |
| `sh paper/container/build-paper.sh` | 5 s | the site built |
| `uv run python scripts/build_figures.py` | 98 s | `fig-planes-k3` (the segment labels "term 1" to "term 3") and `fig-nlemma` (its key) rewritten; the other figures and the two model views unchanged |
| `uv run python paper/figures/figure1.py` | | `figure1.png` and `figure1.svg` (labels "term k", the third pane "terms laid flat") |
| Figure 1's data hash | | `ec68f512...`, pinned; with the old key name the same arrays give `4040cb8e...`, the earlier pin, so the data are unchanged |
| `uv run pytest -q -n 4` on `test_paper`, `test_case`, `test_k_terms_case`, `test_paper_sources`, `test_paper_static_figures`, `test_narrative`, `test_claims_register`, `test_sensitivity`, `test_interface_contract`, `test_soft_fit` | 222 s | 399 passed, 1 failed, 4 skipped: the failure was a pin of the generated recovery sentence still reading "facet", corrected and re-run below |
| `uv run pytest -q tests/test_paper.py -k "figure1 or cr2_the_planted"` with the corrected pins | 20 s | 4 passed |
| `PAPER_EXECUTE=1 uv run pytest -q tests/test_paper.py -k "perturbation or clean_kernel or term_order"` | 406 s | 4 passed |

No number of the paper moved. The jitter record `examples/adcs/experiments/reports/sensitivity.json` was not re-run
(its regeneration is the oracle's): its keys were renamed and the file re-serialized as the writer writes it (sorted
keys); every number and every string value is equal under the rename, and `test_sensitivity`'s comparison of its
committed column with the live case results passed in the image. `tests/data/soft_fit_default_reference.npz` has its
94 keys `.../facet_` and `.../facet_share_` renamed `.../cell_` and `.../term_share_`, all 1274 arrays equal in dtype,
shape and value; `test_soft_fit` passed in the image (exact branch). The environment of record is now `9c8a0c616386`.

## Regeneration of Appendix E after the narrowing of row G-17 (2026-11-10, image 9c8a0c616386, head 541efcd)

Only `tab-E-gaps` and its two echoes in `paper/supporting_material.ipynb` changed (row G-17 of `abstraction-gaps.md` narrowed
to the committed record); `paper/paper.ipynb` is byte-equal; the edited ledger file was copied into the container before the run.

## Regeneration of Appendix B after the derivation's rename (WP24 push 2, 2026-11-10, head 90c8848)

The word "facet" left the derivation (WP24 push 2): step text, statements, docstrings and the ledger say "term" for
the model object and "cell" for the assignment; `lemma_12_facet_gap.py` moved to `lemma_12_term_gap.py`
(`git mv`); `proof_map_record.json` regenerated with `uv run python -m derivation.proofmap --update` on the Mac.
R1's statement keeps the textbook word (the tau = infinity polyhedral sense, the scope's A1).
Steps, each `--network none`, in `hts-*` containers only: `sh paper/container/build.sh` at 90c8848 (35 s, cached
layers), image `hts-paper` **`e852cde39180`**
(`sha256:e852cde3918069d255d967fe2fd6f8aa6f7b53d148c84642c905861a447f38a1`), the previous image `9c8a0c616386`
removed in the same step (`docker rmi`, no container on it); `docker create --name hts-wp24p2 --network none
hts-paper sh /tmp/run.sh`, the script copied in, `docker start -a`; the notebook copied out with `docker cp`;
`hts-wp24p2` removed by name.

| command (inside `hts-paper`, `HTS_ENVIRONMENT_OF_RECORD=1`) | wall time | result |
|---|---|---|
| `uv run python derivation/run.py` | 9 s | "ALL LEMMAS PASS." |
| `uv run python -m derivation.proofmap` | 1 s | "PROOF MAP OK: 17 lemma files, 371 tagged steps" |
| `uv run python paper/paper_common.py` | 3 s | `environment_reference.npz` and `environment_values.toml` unchanged |
| `uv run python paper/execute_notebooks.py` | 129 s | both notebooks; `paper/paper.ipynb` byte-equal to the commit; in `paper/supporting_material.ipynb` the Appendix B cells (`tab-B-proof-map`, `tab-B-proofs-fit`, `tab-B-proofs-solver`, `tab-B-checker`) in words and the moved file's name, `tab-A-register` the three glossary entries of da2984e (MoE, MoP, launch cost) not yet compiled, `tab-F-toolchain` the build commit |
| `sh paper/container/build-paper.sh` | 5 s | the site built (a favicon 404 line from the builder's server, no error) |
| `uv run pytest -q tests/test_paper.py -k appendix_b` | 4 s | 8 passed, 140 deselected |
| `uv run pytest -q -n 4 tests/test_derivation.py tests/test_proof_map.py tests/test_matches_derivation.py tests/test_claims_register.py` | 77 s | 248 passed |

No number of the paper moved. The environment of record is now `e852cde39180`.

## History

The tests read git history (`git log` of the generating commits, `git diff` of the frozen CSVs). The build context excludes
`.git`; `paper/container/build.sh` writes `git bundle create HEAD` outside the context and passes it as the named build context
`history`, and the image runs `git init`, `git fetch` of the bundle and `git reset FETCH_HEAD` in `/app`, so the working tree is the
copied one and `git diff` shows any difference from HEAD. Without the bundle the image builds and those tests skip.

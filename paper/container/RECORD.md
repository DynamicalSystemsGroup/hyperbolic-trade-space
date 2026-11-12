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

The two commits were rebased onto dev before the push: 90c8848 is the first of them on dev, and the
image was not rebuilt: the rebase brought no change to `derivation/`, `paper/*.py`, `src/` or the notebooks (only the
behavioural view's files, its paper copy and `diagnostic_pair.py`, which no notebook cell executes), so the outputs
stand; `tab-F-toolchain` keeps 90c8848, the tree the outputs came from. `paper/supporting_material.ipynb` alone was
copied out.

## Regeneration of Appendix E after row G-17 dropped the decision record's number (WP25-2, 2026-11-10, image e852cde39180, head ba5a0cb)

Row G-17 of `abstraction-gaps.md` cited a relative move of the settling time under the jitter from
`work-packages/WP16-decisions.md`, a decision record; no committed generated file holds that move (the jitter record
`examples/adcs/experiments/reports/sensitivity.json` holds the quantities built on the settling time, not the time), so
the clause now says what the record holds: the settling time's regimes, the signs of its tensions and its Spearman
correlations are identical in all five regenerations. The image was not rebuilt (no change to `src/`, `paper/*.py` or
the derivation since 90c8848). Steps, `--network none`, `HTS_ENVIRONMENT_OF_RECORD=1`: `docker create --name hts-paperreg`,
the files changed on dev since 90c8848 that the paper or the tests read copied in with `docker cp` (the edited ledger,
both notebooks, the behavioural view's files and its paper copy, `diagnostic_pair.py`, the three paper-sources notes,
`tests/test_narrative.py`, `tests/test_system_model_v2_r1.py`), `docker start -a`; the notebook copied out;
`hts-paperreg` removed by name.

| command (inside `hts-paper`) | wall time | result |
|---|---|---|
| `uv run python paper/paper_common.py` | 3 s | `environment_reference.npz` and `environment_values.toml` unchanged |
| `uv run python paper/execute_notebooks.py` | 223 s | both notebooks; `paper/paper.ipynb` byte-equal to the commit; in `paper/supporting_material.ipynb` only `tab-E-gaps` (row G-17) |
| `sh paper/container/build-paper.sh` | 8 s | the site built (a favicon 404 line from the builder's server, no error) |
| `uv run pytest -q tests/test_paper.py tests/test_gaps.py tests/test_claims_register.py` | 104 s | 189 passed, 4 skipped |

The register's committed output (`tab-A-register`) is current here and on the Mac: the Linux failure at bd017dc of
`test_register_committed_output_is_current` and `test_cr18_regenerate_row_reproduces_the_committed_output_of_a_row`
was a stale output (da2984e added three glossary entries without compiling Appendix A: 51 rows committed, 54 entries),
compiled in the push 2 run above (27dab4d); no row differs across platforms. No number of the paper moved.

## Regeneration after the paper's prose took the vocabulary (WP24 push 3, 2026-11-10, image e852cde39180, head 3a66e78)

The word "facet" left the prose of both notebooks (WP24 push 3): "term" or "monomial term" for the model object,
"cell" for the designs a term scores highest, the abstract's gloss of "monomial term" and the Preliminaries' quilt
sentence; the two tau = infinity sentences of R1 keep the textbook word with the vocabulary tool's exempt marker. The
image was not rebuilt (no change to `src/`, `paper/*.py` or the derivation since 90c8848). Steps, `--network none`,
`HTS_ENVIRONMENT_OF_RECORD=1`: `docker create --name hts-wp24p3 --network none hts-paper sh /tmp/run.sh`, the files
changed since 90c8848 that the paper or the tests read copied in with `docker cp` (both notebooks,
`claims_register.toml`, `paper/length_ledger.toml`, `tests/test_paper.py`, and the files of the units since: the gaps
ledger, the behavioural view's files and its paper copy, `diagnostic_pair.py`, the three paper-sources notes,
`tests/test_narrative.py`, `tests/test_system_model_v2_r1.py`, `derivation/PROOF_MAP_FINDINGS.md`), `docker start -a`;
both notebooks copied out; `hts-wp24p3` removed by name.

| command (inside `hts-paper`) | wall time | result |
|---|---|---|
| `uv run python paper/paper_common.py` | 3 s | `environment_reference.npz` and `environment_values.toml` unchanged |
| `uv run python paper/execute_notebooks.py` | 115 s | both notebooks; every output cell byte-equal to the commit (the Markdown cells carry the change); `tab-F-toolchain` keeps 90c8848 |
| `sh paper/container/build-paper.sh` | 5 s | the site built (a favicon 404 line from the builder's server, no error) |
| `uv run pytest -q -n 4 tests/test_paper.py tests/test_paper_sources.py tests/test_narrative.py tests/test_claims_register.py tests/test_paper_static_figures.py` | 74 s | 187 passed, 2 failed, 4 skipped: the two failures are `test_register_phrases_are_used_in_the_body` and `test_register_phrases_are_used_in_the_main_text_itself`, which read the register phrase `facet gap` from `docs/superpowers/notes/notation.md` (outside the push; the paper says "term gap"); the Appendix B tests pass, so 7fad5ff's row is settled |
| `PAPER_EXECUTE=1 uv run pytest -q tests/test_paper.py -k "perturbation or clean_kernel or term_order"` | 411 s | 4 passed |

No number of the paper moved. The environment of record stays `e852cde39180`.

## Host regeneration of six generated tables after the docs and the glossary took the vocabulary (WP24 push 4, 2026-11-10, no container)

No container run, by the supervisor's rule of 2026-11-10, 09:05 (`work-packages/PM-BRIEF.md`, "The container is a gate
check, not a unit step"): a unit regenerates on the host and the container of record is the driver's regression check at
the gate. The sources that changed are text: `glossary.yaml` (two entries of the old word gone, `term gap` and the `monomial term`
entry), `paper/prior_art.yaml`, the gaps ledger `docs/superpowers/notes/abstraction-gaps.md`, and
`paper/generate_proofs.py`, which now appends the vocabulary tool's exempt marker (an HTML comment, rendered as nothing)
to a declared axiom whose statement uses the textbook polyhedral word (R1, step L3.9). The image was not rebuilt and
`e852cde39180` stays the environment of record. The cells were executed on the Mac (macOS, the project's locked
environment), each from a clean kernel with its notebook's setup cell only, and their outputs written in place
(execution counts kept): in `paper/supporting_material.ipynb` `tab-A-register`, `tab-B-proofs-fit`, `tab-E-gaps`,
`tab-G-register` changed and `tab-B-proofs-solver` was unchanged; in `paper/paper.ipynb` `tab-families` changed. Every
other cell is byte-equal to the commit before. The changes are words only; no number moved.

| command (host) | result |
|---|---|
| the six cells, each with its notebook's setup cell, by `nbclient` | five outputs changed in words, one unchanged |
| `uv run pytest -q -n 8 tests/test_paper.py tests/test_gaps.py tests/test_claims_register.py tests/test_build_generated.py tests/test_vocabulary.py tests/test_docs.py tests/test_site.py tests/test_paper_sources.py tests/test_narrative.py` | 342 passed, 1 failed, 4 skipped before the last rewording of the DEA row; after it and the two cells regenerated again, the vocabulary and paper tests pass (the whole fast suite in `WP24-review.md`, Push 4) |

## Container regression at the WP23 close-out gate (2026-11-10, image 877c42cc10e3, head 61cef31)

The driver's regression under the rule of 2026-11-10 ("The container is a gate check, not a unit step",
`PM-BRIEF.md`): the close-out's host regeneration (ledger `@6`, f1101ce and after) regenerated in the container of
record, the exact outputs the environment-of-record tests read re-pinned from it, the robustness image run on the
committed tree. Steps, each `--network none`, in `hts-*` containers only: `sh paper/container/build.sh` at 61cef31
(the local head: the `ledger_gate.py` note commit, on `dev` as 4b5dc46 after the driver's rebase; the container's
history, `tab-F-toolchain` and the five ledger entries name 61cef31) (36 s, cached layers), image `hts-paper`
**`877c42cc10e3`** (`sha256:877c42cc10e3873c1619564c4e30287cfcdee0544fa15ec1a1fcbd8c7e99e75d`), the previous image
`e852cde39180` removed after the build (`docker rmi`, no container on it); `docker create --name hts-gate-regression
--network none -e REQUIRE_OPENSYSML=1 -e PYTHONPATH=examples/adcs -e EXPERIMENTS_WORKERS=3 hts-paper sleep infinity`,
the scripts copied in, each step by `docker exec` (the copied-in `.claude/` lock directory removed first so the tree
is clean: untracked files count as dirty); the outputs copied out with `docker cp`; `hts-gate-regression` removed by
name. `git log -1` inside prints 61cef31; `git status` before the run is clean. The session scratchpad keeps the old
files, the scripts and every log.

| command (inside `hts-paper`, `HTS_ENVIRONMENT_OF_RECORD=1`) | wall time | result |
|---|---|---|
| `uv run python examples/adcs/model_v2/ledger_gate.py --image 877c42cc10e3` | 492 s | RECORD: `v2-primary@7`, `v2-baseline@7`, `v2-check-predictions@7`, `v2-check-designs@7`, `scope-sensitivity-shared-subspace-v2@6`; `git_dirty` False in all five; the proposer printed `reach 0.6222 (quantile 0.02 of the nearest predicted distances of the 300 most isolated holes); 3 of 3 proposals` |
| `uv run python examples/adcs/model_v2/coverage.py` | 17 s | `views/coverage.{md,csv}` byte-equal to the commit |
| the first 20 v2 designs by the test's own runner call (`/tmp/record20.py`) | 10 s | `tests/data/v2_first_designs_of_record.csv`, output `ba2457d3e031...` |
| every fit of the soft-fit reference by the test's own routines (`/tmp/rec_softfit_all.py`, below) | 44 s | `tests/data/soft_fit_default_reference.npz`: 1274 arrays as before, `recorded_on` = linux, aarch64 |
| `uv run python -m experiments compare` | 5 s | the report; re-run on the host after CR-2 returned to the register (below) |
| `uv run python -m experiments verify` | 1 s | RECORD: `44 entries (11 current); 0 drifts` |
| `uv run python -m experiments.sensitivity regenerate --out /tmp/sens --workers 3` | 2252 s | the five regenerations (7.2 to 8.3 min each) |
| `uv run python -m experiments.sensitivity analyse --out /tmp/sens --json .../sensitivity.json --md /tmp/sens/generated-section.md` | 205 s | `sensitivity.json`; "Every listed conclusion is identical across the regenerations and to the committed data"; the generated section kept in the scratchpad, not the repository |
| `uv run python paper/stability_extra.py /tmp/sens` | 193 s | `paper/stability_extra.json` |
| `uv run python paper/paper_common.py` | 3 s | `environment_reference.npz` and `environment_values.toml` unchanged |
| `uv run python paper/execute_notebooks.py` | 157 s, then 172 s | both notebooks, twice: on the host's jitter record, then on the regenerated one (the committed outputs are the second run's) |
| `sh paper/container/build-paper.sh` | 5 s | the site built (three favicon 404 lines from the builder's server, no error) |
| `uv run python scripts/build_figures.py` | 87 s | `fig-planes-k1`, `fig-planes-k3`, `fig-chart-level`, `fig-nlemma` rewritten, pixel-equal to the commit (bytes differ: the PNG encoder); the two model views byte-equal |
| `uv run python paper/figures/figure1.py` | 4 s | `figure1.png` byte-equal; `figure1.svg` differs in matplotlib's path ids only |
| `uv run python examples/adcs/k_terms.py` | 47 s | the K record printed: primary K = 1 tau 38.10, contending set total mass, energy balance, pointing error, depth of discharge, settling time; stock K = 1 tau 45.68, control effort, settling time, power margin, pointing error, depth of discharge (as the close-out's host record); primary K = 3 margin 0.001213 |
| `uv run pytest -q -n 4` (the whole suite, exact branches), first run, before the three re-pins below | 540 s | 47 failed, 2140 passed, 17 skipped, 1 xfailed: 43 planted soft-fit cases, the K = 3 margin pin, the jitter record's committed column, and two tree-state checks (`test_frozen_csvs_unchanged_in_git`, `test_the_frozen_csv_is_not_touched`: the regenerated v2 files were uncommitted inside the image) |
| `PAPER_EXECUTE=1 uv run pytest -q tests/test_paper.py -k "perturbation or clean_kernel or term_order"` | 408 s | 4 passed |
| `uv run pytest -q -n 4 tests/test_soft_fit.py` after the re-recording | 105 s | 58 passed |
| `uv run pytest -q tests/test_k_terms_case.py` with the re-pinned margin | 61 s | 7 passed |
| `uv run pytest -q tests/test_sensitivity.py` on the regenerated record | 54 s | 12 passed |
| `uv run pytest -q -n 4` on `test_paper`, `test_narrative`, `test_claims_register`, `test_case`, `test_paper_sources`, `test_paper_static_figures` on the second notebook execution | 199 s | 1 failed, 241 passed, 4 skipped: `test_generated_sentences_quote_the_ranges_from_the_results_file` (corrected below); the host's tolerance run of the same files also failed `test_term_numbered_tables_are_current` (corrected below); after the corrections the two tests: 3 passed, 1 skipped in the image (51 s) and on the host (40 s) |
| `uv run pytest -q -n 4` on `test_experiments`, `test_legacy_oracle`, `test_v2_data`, `test_container`, `test_k_terms_case`, `test_sensitivity`, `test_paper`, re-run in the image on this commit's tree (8a732ed: its history bundle fetched and `git reset` to it, the working tree unchanged) | 254 s | RECORD: 97 passed, 1 skipped (the two tree-state checks among them) |

**Three references the host units had re-recorded, re-pinned from the container** (the suite's first run in the image:
47 failed; the same lesson three times: a host unit re-recorded a reference that only the container should pin).

| reference | old provenance (host) | new provenance (container) | the difference |
|---|---|---|---|
| `tests/data/soft_fit_default_reference.npz` (`recorded_on` darwin, arm64 to linux, aarch64) | the close-out's host re-recording (f1101ce) rewrote all 47 fits, among them the 43 planted fits it did not need to touch (they read no case data), so the exact branch failed in the image on 43 planted cases at 1e-16 | every fit re-recorded in `hts-paper` by the test's own routines (`_cases()` fitted as `test_r2_default_planted_fits_equal_the_recording` does, the four cubesat fits as `test_r2_default_cubesat_fits_equal_the_recording` does, `_record`; `/tmp/rec_softfit_all.py`, 44 s) | 1274 arrays as before; the planted fits move at the last digits except `planted3_K3_tauinf_support`, a degenerate tau = infinity linear program whose final steps follow the platform (`status`, `reason`, 47 iterations, one row's `cell_`: gap G-10, the quantities `RELAXED_SKIP` names); the cubesat fits within 1.3e-4 absolute (the conditioning), exponents within 2.3e-7; 58 passed in the image (exact) and on the host (tolerance) |
| `tests/test_k_terms_case.py`, `MARGIN[("primary", 3)]` | the fix-forward G-1 (ebce53b) pinned the host's printed margin 0.001212 (abs 5e-7) | the image prints 0.001213 (`k_terms.py` above); the pin takes it | 0.001212 to 0.001213; 7 passed in the image and on the host, on the re-pinned data |
| `examples/adcs/experiments/reports/sensitivity.json`, `paper/stability_extra.json` | the close-out's host run (five regenerations on the Mac, 18 min; f1101ce): its committed column was the host's case results, 2.6e-5 relative from the container's on one K = 1 exponent (rel 1e-6 asked) | the five regenerations, the analysis and the extra file in `hts-paper` (37.5 min, 205 s, 193 s; `EXPERIMENTS_WORKERS=3`), then both notebooks executed again on them | every listed conclusion identical across the regenerations and to the committed data; 203 of 492 committed values move (the largest 3.7e-4 relative), no integer, string or verdict; seven `identical` flags False to True (the committed data and the regenerations now share the platform); 12 passed in the image and on the host |

Two assertions of `tests/test_paper.py` were corrected on the way, not pins: `_cells_of_table` (the tolerance branch of
`test_term_numbered_tables_are_current`) now reads `below 1e-12` and `0` as the same cell, since a zero exponent is an
exact 0 in the image and 2e-17 on the Mac and the generator prints the residue text only for a nonzero residue
(`residue_bound`); and `test_generated_sentences_quote_the_ranges_from_the_results_file` asked that the committed
effective sample size never be printed when the regenerations differ at any digit, where the sentence prints the digits
that hold at one decimal (`stable(name, .1f)`, "23.1" with the regenerations at 23.09868232 and 23.09868233); it now
asserts the stable text and, when the regenerations differ at that format, the absence of the committed value.

**What the container's regeneration changed against the committed host run** (the comparison of old and new from the files
kept in the scratchpad; the four flags equal on every design, the feasible counts 706 and 780 unchanged, no conclusion of
the paper or of the jitter record moved):

| file | old sha256 (the commit) | new sha256 (the container) | the difference |
|---|---|---|---|
| `examples/adcs/data/v2/adcs_designs_cubesat_gains.csv` | `d601d82833b60bd4db8ede22082bbedc1cf9dcf79a89a7e998ba98ead52910c5` | `a43ccc557bc6a572be315309fbe5f5b101df504fb38c2a2692f12ba15c4c1e2f` | settling time within 1e-6 s (9 rows); `torque_saturated_frac` 514 rows, up to 0.0095 absolute; `control_effort` up to 7.4e-5 relative; energy balance, depth of discharge, peak momentum, slew-loss energy at 1e-5 relative or below |
| `examples/adcs/data/v2/adcs_designs_cubesat.csv` | `9d1f4849ba461b409e74604eef8e77985915551c80e9d3be9783f0adc119feef` | `10ae79a224b5a0b370927d2419ca238e634d25f434a044385f920a3c1a77ee74` | as above: `torque_saturated_frac` 168 rows, up to 0.0071 absolute; `control_effort` up to 1.2e-4 relative; the rest at 1e-5 or below |
| `examples/adcs/data/v2/check_predictions_cubesat.csv` | `48493bf3f6e6a3566a447dc0bc8a45b12cb7a6761089411c8383e878ffe92605` | `6b65b2843a99cf2b3510f791ab956e664a0ac488a94881cb606ead27d2522b39` | byte-identical to the data gate's `@5` output (`6b65b2843a99`); against the host's, every predicted coordinate within 1e-5 relative |
| `examples/adcs/data/v2/check_designs_cubesat.csv` | `e3f22d93c7d783068b3c578d56798010ce6e1edabf8868cce54a234adfb13919` | `5b47f53b4d7b5e53a738915b9d4c44e887139948c5bf15720abda536c8b82d9a` | `torque_saturated_frac` 4 rows, up to 0.0036 absolute; the rest at 2e-5 relative or below |
| `examples/adcs/data/scope-sensitivity/scope_sensitivity_v2.csv` | `fd46402c2f617ff8af341fa753d05a839fef27538e905a982d574ea53373f502` | `d16ae3648c402c615a03f99d14a85e38405ad28781580b7d3cd838dd5d51e522` | `torque_saturated_frac` 15 rows, up to 0.0024 absolute; the rest at 2e-5 or below |
| `tests/data/v2_first_designs_of_record.csv` | `81241be0b88321ab09e8dd031aec7f1162fcf5fedc084703aa17951a0ae9e159` | `ba2457d3e031d754a2e4f2838b17908fd39cdfa0dfe82be87cbe1695ef8d99c2` | `torque_saturated_frac` 12 rows, up to 0.0046 absolute; the rest at 5e-5 or below |
| `examples/adcs/experiments/ledger/ledger.jsonl` | `4508e1770176998088b3a9d4441ced667c114e96c2c33db425e245657701638b` | `b5a1f83be514b184b58f155d21f5ade1cfe971ea53c58eab99a61e7445db7a47` | the five entries appended (`git_commit` 61cef31, platform `Linux-6.8.0-50-generic-aarch64-with-glibc2.41`) |
| `examples/adcs/experiments/reports/change-register.md` | `e8969c16fd8f761a6fca697c875c536d972698c37e16db64214d4654b5ec438f` | `f84899df3733880babc46ff47d27740b043c7c1c0fd38c00632c6e794ccafb18` | CR-2 returned; the header and the close-out-gate finding |
| `examples/adcs/experiments/reports/v1-v2-comparison.md` | `44c832dda15befd24f6301e66ed621f5c2615757f4416de06e496d18a6b4dc5e` | `e0d766c3434741bfaa762619d5b5aa4c7ef0191ed16a168bc04f50a9aceb77a4` | the `@7` entries; `primary:torque_saturated_frac`, `baseline:torque_saturated_frac`, `baseline:control_effort` beyond tolerance |
| `examples/adcs/experiments/reports/sensitivity.json` | `469bbf138a7a8bf041c66ea17bff2269105a9e9d1602d01c06b1f5e26297f266` | `d561cbb130da8106659e329b309d06660c3769f306e35df81f7293909feef4fa` | 685 quantities as before; 203 committed values move, the largest 3.7e-4 relative (proposal 2's ||dZ||), 25 above 1e-4, none above 1e-3; no integer, string or verdict moved; seven `identical` flags False to True (the three proposals' predicted log V and one K = 3 zero exponent: the committed data and the regenerations now share the platform) |
| `paper/stability_extra.json` | `82bf1d401168a82908403265d5427179aca92c4814933cd5185d3177993179bd` | `21b8245490eb3c804fa48a8bd932f064908a8f6921d102a2c01b0c778dda506b` | 31 quantities as before; 19 committed values move, the largest 1e-5 relative (the stock K = 3 median margin) |
| `tests/data/soft_fit_default_reference.npz` | `eaa4f647baebf41f2e7c13b389ab81eb715a30774acfa002c8f8fbe5c9299e73` | `52e55f7e7add8a9440bdfe014f082b2fc8720b349660c97be0779f884d2f9d0b` | every fit re-recorded (below); `recorded_on` linux, aarch64 |
| `tests/test_k_terms_case.py` | `eedd0f79461282c14eaac112fa868ad2ef5867ef69c227e74a7ea5ec9d699ee0` | `bf7bd4422eba5540d86cc19792abb3e3f40bc0a3be37ccc50427b38c1d775f2c` | `MARGIN[("primary", 3)]` 0.001212 to 0.001213 (below) |
| `paper/paper.ipynb` | `60f25a55d3600eb603a61a2a0404fdf52af1190ea5ce6cc2c9bc47c3f2310d75` | `9f11a534dafd3cff8d4a71908c56ec2e0c914989768b5c3d04d35b38e079070d` | `num-margin` (the stable radius 0.000121 to 0.0001209: the digits that held); the PNG bytes of `fig-tau-sweep`, `fig-tensions-k3`, `fig-regimes` (pixel-equal but 12 pixels of the tau sweep); no other output |
| `paper/supporting_material.ipynb` | `a4e65d7e1d636acda70c946c9d62a0338cd9e9d5555d6fb829bd738b7a8a4824` | `b95db6bfdc503ad958c914cea7f33e280d3cf2303e8fcffe2e6c4c6b24dc6e1a` | `tab-C-datasets` (the `@7` entries and hashes; the planted table's digest back to the container's `b17d4f8f...`), `tab-D-k_diagnostics`, `tab-D-termination_records`, `tab-D-margin_reading`, `tab-D-exponents_and_terms` (a zero exponent printed 0 for "below 1e-12"), `tab-D-propose_predict_check` (1.055 to 1.05, 0.04836 to 0.0484: three digits held), `tab-D-stability` (243 numbers move at all, was 250; the radius row of K = 3 is the stock regime's, the primary's now holds its digits), `tab-F-toolchain` (Node v24.22.2, Python 3.12.16, the platform, the commit) |
| `paper/figures/fig-chart-level.png` | `cbe75c8bb3cfa5a11f6ec34ca6ca0adb9cc63ddca249313a473ea2c444e19f3f` | `04e70d2b94f1191c5c36d22e753d9592992068d00d6ef7540e226112d71b0120` | pixel-equal; bytes by the encoder |
| `paper/figures/fig-nlemma.png` | `7b56fe6da2c9ee54effd7253dd92ef3db2bba4fbdcfbcdc554c2bff58bda31b9` | `5a906f8dcc6a5b3680ea240081250934723a9489ff5c911ee01b20bae42cc9a6` | pixel-equal; bytes by the encoder |
| `paper/figures/fig-planes-k1.png` | `81988245d062eb1be71fb68cd44f95b2b931b3431fe6756c9b6a0b0570b06320` | `915d146c7039d003c1e2e8fbbea3d03f0ae9e31cf2ada1cab53ef59fd7a077ed` | pixel-equal; bytes by the encoder |
| `paper/figures/fig-planes-k3.png` | `4eda5d1f177fc587946c2c73c60c6ef702b24cffc6fe6313b5d65d65a2a4fa4d` | `294031005645ed567e7b8e670605ecf31d87efdb402f645aa695617d13c93aa1` | 4 pixels at antialiasing; bytes by the encoder |
| `paper/figures/fig-regimes.png` | `6297e6788451370e41f0ddac5c73f3228a2d2ef772ec016e1ad87516000c10de` | `4d3bec0b1735d0d8ff169eff8b772c267205d387fd454c8bf0dc501ba6f600a0` | pixel-equal; bytes by the encoder |
| `paper/figures/fig-tau-sweep.png` | `5f8eada246242a1d76e4cc281ef15230f10d37943dfb4a1b01258023669386bc` | `d386b27c65c2e7540807078eb824f42081e5b4a2e92d4d6d9279a8f40f9397fb` | 12 pixels at antialiasing; bytes by the encoder |
| `paper/figures/fig-tensions-k3.png` | `037e262b8b5c71a4fd84648923702681c4f2423ddd2393a46f72b58937a81a9a` | `26f613b2651e2f28047ebab88ee67ef51d1d7b5559078a68b88d11626bb4e52f` | pixel-equal; bytes by the encoder |
| `paper/figures/figure1.svg` | `a47d820757e7cc1691b1a151773144b4fdae95784afacbbbc0200ccf0091d114` | `fcc42833d9f5bb4d56df6cb7b072a8bb0a2ef54bae8d1f393f36b4bd45cec3aa` | matplotlib's path ids only |

**CR-2 returned.** Against the frozen Mac files the container's two 1000-design tables exceed the reproducibility
tolerance on `torque_saturated_frac` in 3 primary and 35 baseline rows and on `control_effort` in 1 baseline row, the same
designs with the same largest differences as the data gate's container run (designs 781, 354 and 488; the adaptive
integrator's accepted steps differ between the platforms). The register had retired CR-2 at the host run and said the
row returns if the container's rows exceed again; it is back, covering those three ids, and `compare` was re-run on the
host so the committed report embeds it (`verify` 0 drifts; the register tests pass on the host and in the image).
`check_predictions@7` is byte-identical to the data gate's `@5` output. Not regenerated here: the model's views
(PlantUML on the host) and `docs/examples.md`'s numbers (the docs tests read them within tolerance). The environment of
record is now `877c42cc10e3`.

**The robustness image** (`hts-alt` 81e06426f7b3, Ubuntu 24.04, the same `uv.lock`, `HTS_ENVIRONMENT_OF_RECORD=0`): a container `hts-alt-gate` from the image, this commit's history bundle fetched and the tree reset to it (the lock is unchanged since the image's head d66c106, so its environment is the locked one), the full suite with the tolerance branches, `uv run pytest -q -n 4` on 8a732ed (`git status` clean): RECORD: **2187 passed, 17 skipped, 1 xfailed, 0 failed** in 735 s. `hts-alt-gate` removed by name afterwards; the image untouched.

## Container regression at the WP30 data gate (2026-11-11, image 27add815d66c, head c64430e)

The assistant's regression under the gate checklist's step 14 (one container run; the container's outputs and
entries become the data of record, the host's `@11` kept in the ledger as superseded). `sh paper/container/build.sh`
at c64430e (the dev head carrying the thirteen-metric model, the term order and the proposer's chunked pool
prediction), image `hts-paper` **`27add815d66c`**; `docker create --name hts-gate-regression --network none
-e REQUIRE_OPENSYSML=1 -e PYTHONPATH=examples/adcs -e EXPERIMENTS_WORKERS=1 hts-paper sleep infinity`; every step by
`docker exec`; the outputs copied out with `docker cp`; the container removed by name. One worker, not three: at
3,000 designs per regime the Docker VM (four CPUs, 7.7 GB) killed the run at three workers and once more at one
worker in the proposer, whose pool prediction then took its chunking (65dcd38). `git log -1` inside prints c64430e;
`git status` before the run is clean; every entry's `git_dirty` reads False.

| command (inside `hts-paper`, `HTS_ENVIRONMENT_OF_RECORD=1`) | wall time | result |
|---|---|---|
| `uv run python examples/adcs/model_v2/ledger_gate.py --image 27add815d66c --wp30 regen` | 61 min | RECORD: `v2-primary@12` `f7632865f2e4`, `v2-baseline@12` `e72cd954f122`, `v2-check-predictions@12` `9abafdf1ce85`, `v2-check-designs@12` `e82725af7739`, `scope-sensitivity-shared-subspace-v2@11` `e7051ec617fa`; 3,000, 3,000, 3, 6 and 20 rows; `oom=false` |
| the four default cubesat fits of the soft-fit reference by the test's own routines (the planted entries untouched) | 2 min | `tests/data/soft_fit_default_reference.npz`: 1274 arrays, 49 rewritten, `recorded_on` = linux, aarch64 |
| the first 20 v2 designs by the test's own runner call | 14 s | `tests/data/v2_first_designs_of_record.csv` (21 lines, every line changed: the five new columns) |
| `uv run pytest tests/test_soft_fit.py` and the first-designs test, inside | 6 min | 59 passed after the re-recording |
| `uv run python -m experiments verify`, inside | 1 s | RECORD: `74 entries (11 current); 0 drifts` |

Against the host's `@11` outputs (the data the cascade's first unit executed on), the differences are platform drift
and nothing the paper prints: in the two 3,000-design tables settling time within 1e-6 s, control effort and momentum
headroom within 1.2e-4 relative, `torque_saturated_frac` within 0.014 absolute (a fraction of accepted solver steps),
the categorical columns and flags equal; the three proposals are the same designs with their chart coordinates
within 1e-4 relative; the six checked rows and the 20 sensitivity rows within the same drift. The case fits on the
container's data agree with the fits on the host's to every printed digit (K = 1 exponents to four decimals in both
regimes, K = 3 term shares to three, the selected temperature identical; mean slack differs at 1e-8). The first 20
designs sit inside the frozen tolerances of `v2_first_designs_rows`. The earlier container attempts of this gate
(image 447cb4853cd9 at 910a57d: killed at three workers, then at one worker in the proposer; its two completed
entries equal this run's byte for byte) are not in the ledger.

## Host regeneration at the WP30 data gate (2026-11-11, no container)

The host (macOS arm64, ten cores, nine workers) regenerated the five ledger entries on the model at
`fe6de947d18f` with thirteen traded metrics, the fleet size and 3,000 designs per regime. The container
regression of the same gate is a separate section, added when it runs.

| What | Command | Time | Result |
|---|---|---|---|
| the five entries | `EXPERIMENTS_WORKERS=9 PYTHONPATH=examples/adcs uv run python examples/adcs/model_v2/ledger_gate.py --host --wp30 regen` | 9.2 min | `v2-primary@11` `e4ab2fca5c74`, `v2-baseline@11` `57c208c91c59`, `v2-check-predictions@11` `05649b15348c`, `v2-check-designs@11` `1cab3bafa3fe`, `scope-sensitivity-shared-subspace-v2@10` `25425be01309`; none dirty |
| the K = 1, 2, 3 record | `PYTHONPATH=examples/adcs uv run python examples/adcs/k_terms.py` | 3 min 7 s | `work-packages/WP30-rounds/data-gate/k-record.txt` |
| re-adoption of the entries that hash a changed code file | `PYTHONPATH=examples/adcs uv run python -m experiments adopt --readopt` | seconds | `adopted-adcs_designs_cubesat@2`, `adopted-adcs_designs_cubesat_gains@2`, `adopted-check_predictions_cubesat@2`, `adopted-check_designs_cubesat@2`, `scope-sensitivity-shared-subspace-legacy@2`; `verify`: 0 drifts |

Earlier runs of the same gate, kept in the ledger as history: the 2,000-design run (`@9`, shared `@8`) and a
first 3,000-design run written with an uncommitted tree (`@10`, shared `@9`, `git_dirty` true), whose outputs
equal the clean run's byte for byte.

## History

The tests read git history (`git log` of the generating commits, `git diff` of the frozen CSVs). The build context excludes
`.git`; `paper/container/build.sh` writes `git bundle create HEAD` outside the context and passes it as the named build context
`history`, and the image runs `git init`, `git fetch` of the bundle and `git reset FETCH_HEAD` in `/app`, so the working tree is the
copied one and `git diff` shows any difference from HEAD. Without the bundle the image builds and those tests skip.

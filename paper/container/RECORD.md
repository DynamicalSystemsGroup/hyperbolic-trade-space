# Record of the container runs (P10)

Run 2026-11-09 on the author's Mac (Apple M1 Max, macOS 26.5.2, arm64) with Colima 0.8.1
(Virtualization.Framework VM, aarch64 guest, Docker server 27.4.0), **linux/arm64 containers, native
(no emulation)**. The platform of record is linux/arm64 (ratified by the supervisor; the spike is
`docs/superpowers/notes/spike-container-platform/report.md`). Repository state: dev at the commit
named in each image (`git log -1` inside the image prints it: the history is rebuilt from a
`git bundle`). Every run below used `--network none`. Nothing was pushed to a registry.

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
- image id of `hts-paper`: `sha256:4cfe46da2a232959c3c09134c6f93e3e606dda842caddedf6a9504188e6bdffc`
  (built from commit eb8a710; the id changes with every commit because the history layer carries it)
- the robustness image `hts-alt`: Ubuntu 24.04, index digest
  `sha256:fe81560990fae86dc4743202b2cb4d3df98d0bcf949173cecef15ce1127ef852` (CI's distribution; glibc 2.39,
  Python 3.12.3 from apt, git 2.43.0, gnupg 2.4.4), same `uv.lock`, same uv, same Node, image id
  `sha256:459014909904c53909f36858a1efa0b03bcc1e955ad321cb6dd61f80d2d32735`; `HTS_ENVIRONMENT_OF_RECORD=0`
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

## The 46 failures in the environment of record

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

## History

The tests read git history (`git log` of the generating commits, `git diff` of the frozen CSVs). The build context excludes
`.git`; `paper/container/build.sh` writes `git bundle create HEAD` outside the context and passes it as the named build context
`history`, and the image runs `git init`, `git fetch` of the bundle and `git reset FETCH_HEAD` in `/app`, so the working tree is the
copied one and `git diff` shows any difference from HEAD. Without the bundle the image builds and those tests skip.

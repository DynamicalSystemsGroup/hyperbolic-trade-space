# P10 acceptance review: the container of record

Reviewer: fresh context, read-only. Reviewed: commits bf80af4, e1f3267, 3c46237, 48df440 and the
test edits confirmed in 150f6b3, against the P10 scope checklist (R-1 to R-9, good enough,
non-goals) and WP10 Amendment 1 (D-13, R-31). Not accepted here; acceptance is the supervisor's.

Checks run by the reviewer: `uv run pytest tests/test_container.py` (8 passed), `uv run ruff check .`
(clean), reading `Dockerfile`, `paper/container/README.md`, `RECORD.md`, `build.sh`, `git diff --stat`
of the delivery commits, `docker images` and `docker ps -a` (read only). No container was run, built,
stopped or removed, and no Colima command was issued, so any item that needs a run is "not checkable".

## Item by item

| ID | Verdict | Evidence |
|---|---|---|
| R-1 digest, arm64, Node pins | Met | `ARG BASE_IMAGE=python:3.12-slim@sha256:5e2bdb1b...` (index digest, matches RECORD); `ARG PLATFORM=linux/arm64`; `NODE_ARCH=arm64`, `NODE_SHA256`, signing fingerprint, releasers commit and key checksum pinned; container tests pass. |
| R-2 build arguments | Met | `BASE_IMAGE`, `PLATFORM`, `NODE_ARCH`/`NODE_SHA256`, `OF_RECORD`, `EXTRA_APT`, `UV_VERSION` are ARGs; `FROM --platform=${PLATFORM} ${BASE_IMAGE}`; tests assert it. |
| R-3 native build, `hts-` name | Met on the record; not independently checkable | RECORD states linux/arm64 native on an aarch64 guest, cold build about 3 min; images `hts-paper` (id 4cfe46da2a23, matches RECORD) and `hts-alt` exist. The record has no verbatim `uname -m` or build line; the claim is prose. |
| R-4 offline run: env, lemma chain, suite, notebooks, paper build | Partly met; rerun not checkable | Command table, all `--network none`: chain ends "ALL LEMMAS PASS.", proofmap OK, `test_derivation` 103 passed, both notebooks executed, site built offline (135 files). Full suite: 46 failed, 2011 passed, so "the full suite succeeds" is not met as written. I did not rerun the chain (a `docker run` is outside my read-only allowance). |
| R-5 record contents | Met | RECORD lists base digest and manifests, image id, uv 0.9.18, Python 3.12.16, Node 24.22.2 / npm, package versions, lock sha256, commit (eb8a710, with why it changes). The container tests check the lines exist. |
| R-6 values regenerated; exact comparison passes inside | Not met at delivery | Arrays regenerated and the digest note updated, but exact comparisons fail in the image (46). RECORD also says `test_paper.py::test_c_committed_output_is_current` fails on the not-regenerated committed notebooks. Resolution is routed by the driver's call in 150f6b3 and WP17, and is open. |
| R-7 second base passes whole suite | Not met as written | `hts-alt` (Ubuntu 24.04, same lock, Python 3.12): 4 failed, 2053 passed. The 4 are soft-fit planted cases (K=3, tau=inf, seeds 0 to 3): same facets numbered differently (gap G-10); seed 2 `term_objective_change` differs by 5.3e-5. Conclusions agree (69 executed cells identical apart from the environment table). No tolerance loosened. |
| R-8 differences listed with both values and tolerance | Partly met; completeness not checkable | RECORD has a differences table and an hts-paper vs hts-alt paragraph. Several rows are prose ("Mac values", "up to 0.05 s") with no per-row tolerance column; the figure and metadata rows are not enumerated. A diff of the two runs' outputs needs running images, so "none omitted" is unverified. |
| R-9 limits | Partly met; two parts not checkable | Outside the container: container tests and ruff pass. Images present: `hts-paper`, `hts-alt`, `hts-pre`, `hts-spike-arm64`; no `hts-*` container exists. About fourteen untagged images (1 to 19 h old, 1.5 to 2.2 GB) look like build layers but cannot be attributed by name. `python:3.12-slim`, an untagged `python`, `ubuntu:24.04`, `alpine` are pulled bases. The user's other images and exited containers (flexo, fuseki, minio, etc.) are present. The before/after listing R-9 requires "in the record" is NOT in RECORD.md, so no comparison is possible. Colima never stopped and `~/.colima` unchanged: not checkable by this review. Blast radius: see below. |

## Out-of-scope files

`git diff --stat bf80af4~1 48df440`: `.dockerignore`, `Dockerfile`, `paper/container/{README,RECORD}.md`,
`paper/container/build.sh` (inside `paper/container/`), `paper/environment_values.toml`,
`tests/test_container.py`, all inside the blast radius, plus **`paper/environment_reference.npz`**
(binary), which is not listed in it. 150f6b3 touches only `work-packages/WP10-decisions.md` (the
driver's record). The npz regeneration is implied by D-4 / G3 and declared in the commit message, but it
is a blast-radius deviation to be ratified.

## Judgement on the three test edits (`tests/test_container.py`)

- Digest check: from "every FROM has @sha256" to "the `ARG BASE_IMAGE` default ends in @sha256 and every
  non-scratch FROM goes through `${BASE_IMAGE}`". Required by R-2 and still fails on an unpinned default;
  not a weakening. Residual: the alt image's digest lives in `build.sh` and is not tested.
- arm64 expectation: `linux/amd64` replaced by `ARG PLATFORM=linux/arm64`, `NODE_ARCH=arm64`, plus a new
  test for `OF_RECORD`. Follows the ratified platform and adds coverage; not a weakening.
- Needle `101 passed` to `103 passed`: matches the record's actual count. It remains a string match on
  prose (checks the line exists, as before); not a weakening.

No edit loosens a requirement. The driver confirmed the three edits in 150f6b3.

## The 46 failures and how RECORD.md explains them

RECORD: 43 + 2 `test_soft_fit` recording cases (planted and cubesat; bit-identical comparison against
Mac recordings in `tests/data/soft_fit_default_reference.npz`), i.e. 45, and 1
`test_cubesat_oracle` (settling time up to 0.05 s from the recorded row, inside the stated 0.5 s
tolerance): 46 in all. The cause given (different maths library and BLAS) is specific, and the data
files are outside P10's files. The driver has routed the fix (150f6b3: regenerate in the container;
facet matching by exponent vector under WP17, with HEAD already carrying the planted-fit change).
150f6b3 also returns a finding that the full suite rewrites a tracked file
(`examples/adcs/experiments/reports/v1-v2-comparison.md`).

## Gaps

1. R-6 not met and R-4's "full suite" not met at the delivered commit: 46 exact-comparison failures remain, depending on files outside P10's blast radius; routed, not closed.
2. R-7 not met as written: `hts-alt` fails 4 soft-fit cases (facet numbering, G-10); conclusions agree, no tolerance loosened; rerun both images after the WP17 matching fix to close it.
3. R-9: no before/after docker listing in RECORD.md; untagged images unattributed; Colima and `~/.colima` unchecked here; `paper/environment_reference.npz` is outside the stated blast radius.
4. R-8: differences table lacks per-row tolerances and a completeness check; no committed diff of the two runs.
5. Minor: second image is `hts-alt`, not the default name `hts-paper-alt` (a default, not a requirement); R-3 evidence is prose rather than captured output; the image id is tied to commit eb8a710, which predates e1f3267 and 3c46237 and 48df440, and no rebuild at the final HEAD is recorded.

## Recommendation

Do not accept as done. The pinning, build arguments, arm64 Dockerfile, README, tests and record
structure (R-1, R-2, R-5, test edits) are acceptable. Keep R-4, R-6 and R-7 open until the container is
rebuilt at the final HEAD after the WP17 facet matching and the in-container regeneration of the
committed exact values, and the suite is rerun in both images; add the before/after docker listing and
per-row tolerances to RECORD.md; ratify `environment_reference.npz` as a blast-radius addition.

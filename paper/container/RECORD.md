# Record of the local container run

Run 2026-11-08 on the author's Mac (Apple M1 Max, 32 GiB, macOS 26.5.2, arm64) with Colima 0.8.1
(Virtualization.Framework VM, aarch64 guest, Docker server 27.4.0, linux/amd64 containers by
emulation; `colima start --arch x86_64 --cpu 4 --memory 8 --disk 60`). Repository state: dev at
commit 750ff12 plus the uncommitted Dockerfile. Nothing was pushed to a registry.

## Pins

- base image: `python:3.12-slim` (3.12.16-slim-trixie), linux/amd64 manifest digest
  `sha256:05a994d2344eb364cc186910f4fc8786a38215f39f00d0acc25bff33a08f4177` (multi-arch index
  digest at resolution: `sha256:5e2bdb1b0d542d5039cffb8181c65930093949194a65c365dfb1b0fe13a4fa5b`)
- uv version: 0.9.18
- python version: 3.12.16
- lock hash: `uv.lock` sha256 `3629c35e910038f3bd712c8c1828a44bdc7c5b9943fd7e7ede15a97c26d22721`
- image id: `sha256:726fc236d1ed106619e1c26a3cdcad7f7dc05bbd73dd9636d8c242d6a1fcac36` (amd64, linux)
- installed (from the image): numpy 2.5.4, scipy 1.18.1, sympy 1.14.0, scikit-learn 1.9.1,
  opensysml 0.12.1, z3-solver 5.3.3.0

## Commands, wall times, results

| command | wall time | result |
|---|---|---|
| `docker build --platform linux/amd64 -t hts-paper .` (base already pulled; uv sync of the locked environment about 10 s) | 20 s (a rebuild with warm layers: 15 s) | RECORD: image built |
| `docker run --rm --platform linux/amd64 hts-paper` | 6.5 s | RECORD: toolchain printed; derivation chain ends "ALL LEMMAS PASS." |
| `docker run --rm --platform linux/amd64 hts-paper uv run pytest -q tests/test_derivation.py` | 59 s (pytest 57.5 s) | RECORD: 101 passed |
| `docker run --rm --platform linux/amd64 hts-paper uname -m` | 1 s | RECORD: x86_64 |

linux/amd64 was workable under Colima on this Mac (emulated); the full suite and the paper build
inside the container were not run for this record.

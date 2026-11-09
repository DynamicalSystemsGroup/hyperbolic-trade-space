# P10 - Scope of work: the container of record

| | |
|---|---|
| **Status** | DRAFT. Approval is the driver's approval message under the mandate of `work-packages/release-candidate.md`, recorded in `work-packages/driver-log.md`. Nothing is executed before then. |
| **Supervisor (accountable)** | mzargham |
| **Repository** | `posynomial-invariant-form`, branch `dev` |
| **Approval record** | The driver's approval message, in `work-packages/driver-log.md`. |
| **Acceptance record** | A fresh-context reviewer's check against these requirements, recorded in this file; then the driver's verification; the supervisor's acceptance at the PR. |

## Blast radius
The stream may touch exactly these files and nothing else: `Dockerfile`, `.dockerignore`, `paper/container/`,
`paper/environment_values.toml`, `tests/test_container.py`. Its own git worktree is
`/private/tmp/claude-501/-Users-z--claude-spares-spare-4Zb8mW/71474a52-35d3-48fa-82b0-c1328e96b5d6/scratchpad/pm-worktrees/P10`
(branch `p10b` off `origin/dev`). One push per unit to `dev`: rebase on `origin/dev`, `git push origin HEAD:dev`; on refusal, rebase and retry.

## Starting point
Unpushed prior work exists on local branch `p10` (commits 96ba622, 6e028de, eb8a710; worktree
`.../scratchpad/wt-P10`). The agent starts from it, cherry-picked onto the fresh worktree off `origin/dev`, not from scratch.

## Purpose
The paper's numbers must be reproducible, and the supervisor wants that by pinning, without brittleness. On the
environment of record he said: "seems fine to me. i don't care about the details, i just want reproducibility (via
pinning) but also robustness, doesn't go to shit if you swap a different but generally comparable image". On
Colima, on 2026-11-09: "go ahead. you can use colima. to be clear i made that available to you for reproducibility
reasons". linux/arm64 in the pinned container is the environment of record (ratified); Linux amd64 is covered by CI.
The committed Dockerfile and `RECORD.md` still describe linux/amd64 under emulation and did not run the full suite or the paper build.

## Goals
- G1. A Dockerfile that builds natively for linux/arm64, with Node pinned for that architecture, and the base image a build argument.
- G2. Inside the container, offline at run time: the locked environment, the lemma chain, the full suite, the notebooks and the paper build all work.
- G3. The run is recorded (image digest, tool versions, results) and the environment values are regenerated there; the exact comparisons pass inside it.
- G4. Robustness: a second image from a different comparable base, same Python minor, same lock, passes the whole suite within the stated tolerances with the same conclusions, every differing value listed.

## Non-goals
HARD limits (supervisor's, word for word from the board and the 2026-11-09 decision):

- images and containers named `hts-*` only; nothing under `~/.colima`; no stop, start, restart or reconfiguration of Colima;
  his other containers and images untouched; stop and report if memory or disk is short.
- No `colima stop`, `start`, `delete` or restart, and no change of its settings (this has gone wrong twice, see `WP10-decisions.md`).
- No change to any file outside the blast radius; no registry publishing; no merge to `main`, no tag; no AI attribution.
- No new emulation experiments (amd64, Rosetta settings); amd64 stays with CI.

## Deliverables
| ID | Deliverable | Serves |
|---|---|---|
| D-1 | `Dockerfile` and `.dockerignore` (arm64 native, Node arm64 pinned, base image and platform as build arguments) | G1 |
| D-2 | `paper/container/README.md` updated to arm64 and the run commands | G1, G2 |
| D-3 | `paper/container/RECORD.md`: the pinned run, its results and the robustness run with the differences list | G2, G3, G4 |
| D-4 | `paper/environment_values.toml` regenerated in the container | G3 |
| D-5 | `tests/test_container.py` updated to the new pins and record | G1, G3 |

## Requirements
| ID | Requirement | Checked by |
|---|---|---|
| R-1 | The base image is pinned by digest, the platform is linux/arm64, Node is the arm64 build with its checksum and signature pins | `uv run pytest tests/test_container.py`; read the Dockerfile |
| R-2 | The base image and platform are build arguments | the container tests; read the Dockerfile |
| R-3 | The image builds natively (no emulation) and carries the `hts-` name | the record's build line, `uname -m` result and image name |
| R-4 | Inside the container, with the network off at run time, the locked environment, the lemma chain (ends "ALL LEMMAS PASS."), the full suite, the notebooks and the paper build succeed | the record's command table with results; a reviewer reruns the lemma chain and one test file in the image |
| R-5 | The record lists the image digest, image id, tool versions (Python, uv, Node, packages), lock hash and commit | read `RECORD.md`; the container tests check the lines exist |
| R-6 | Environment values are regenerated in the container and the exact-comparison test passes inside it (reproducible side) | the test run inside the image, in the record |
| R-7 | A second image from a different comparable base, same Python minor, same lock, passes the whole suite within the stated tolerances with the same conclusions (robust side) | the record's second run |
| R-8 | Every value that differs between the two images is listed with both values and its tolerance, none omitted | the record's differences table, checked against a diff of the two runs' outputs |
| R-9 | The limits hold: only `hts-*` images and containers created, nothing under `~/.colima` changed, Colima never stopped, started or reconfigured, the diff touches only the blast radius | `git diff --stat origin/dev` on the worktree; the listing of images and containers before and after, in the record; `uv run pytest` and `uv run ruff check .` pass outside the container |

## Definition of good
Reproducible: the pinned image reproduces the committed values exactly. Robust: a different comparable base (same
Python minor, same lock) passes the whole suite within the stated tolerances, reaches the same conclusions, and its
differences are listed. Both sides recorded in `RECORD.md` so a reader can rerun them.

## Definition of good enough
- The arm64 image builds, and the full suite passes inside it offline at run time (R-3, R-4).
- Environment values are regenerated and the exact comparisons pass inside it (R-6).
- One second-base image passes with its differences listed (R-7, R-8).
- The record is written (R-5), the container tests pass, and the limits are shown to hold (R-9).
- If memory or disk is short at any point, the agent stops and reports what is done and what is not.

## Definition of done
Good enough is met, **no open item remains unresolved**, and the supervisor has accepted the work by the acceptance record above.

## Agent's defaults
- The second base is Ubuntu 24.04 (the prior work found Debian bookworm has no z3 wheel for arm64) *(default)*; the agent may pick another comparable base if it can show the reason in the record.
- The image names are `hts-paper` and `hts-paper-alt` *(default)*; tolerances are the ones the existing tests already state; none are loosened.
- The paper build uses the warm-up approach already in the Dockerfile (site template fetched once at build time) *(default)*.

## Open decisions (for the supervisor)
None.

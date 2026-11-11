# WP34 — Scope of work: Windows as a third platform

| | |
|---|---|
| **Status** | DRAFT. Approved only by the recorded act below. Stage 1 (the spike) is a dispatch-only workflow and changes no code. |
| **Supervisor (accountable)** | mzargham |
| **Repository** | `DynamicalSystemsGroup/hyperbolic-trade-space`; work on `dev`, merged to `main` when the driver judges it merits CI |
| **Approval record** | The driver's approval under the mandate (`release-candidate.md`), quoted verbatim in `work-packages/WP34-decisions.md` |
| **Acceptance record** | The driver's acceptance under the mandate, quoted verbatim in `WP34-decisions.md` after `WP34-review.md` |

## Purpose

The supervisor, 2026-11-11, 11:30, verbatim (`release-candidate.md`, "Windows"): "i have another parallel workpackage
for you to get going. we have mac and linux environments, but can you emulate windows and make sure that works as
well?" Windows cannot be emulated on this Mac; a real Windows runner in GitHub Actions (`windows-latest`) is a true
Windows. The outcome: the package, its tests and as much of the toolchain as stands up run on Windows, and the README
and the reproducibility appendix say what runs where.

## Goals

- G1. The failures of one Windows run are read and classified (path or line ending, encoding, temp directory, fonts,
  subprocess or shell, missing wheel for scipy, HiGHS, Z3 or the SysML toolkit, node for mystmd, a Unix-assuming test).
- G2. The shards Windows runs are decided with the supervisor-facing options stated plainly.
- G3. What is ours is fixed, each fix with a test.
- G4. Windows is an OS matrix entry of `test.yml`, run on dispatch and at gates.
- G5. The README environment line and the reproducibility appendix say what runs where, and why for anything Linux-only.
- G6. Three platforms are green at the head.

## Non-goals

- No emulation, VM or container of Windows on the Mac.
- No change to the model, the data or any generated number; no change of the mathematics for a platform.
- No weakening of a test for Windows without a reason stated in the commit message.
- No Windows-specific code path where a portable one (pathlib, explicit utf-8, newline handling) does the job.
- Not a support promise beyond what the green runs show.

## Stages

1. **Spike.** a `windows` job in `.github/workflows/test.yml` (GitHub dispatches only workflow files on the default branch, and `main` has no separate `windows.yml`), behind a boolean `workflow_dispatch` input `windows` (default false; never on push or pull request), dispatched with `gh workflow run test.yml --ref dev -f windows=true`: `windows-latest`, `astral-sh/setup-uv`, Python 3.12,
   `uv sync --locked`, lock check, ruff check and format check, the fast suite as `test.yml`'s fast shard runs it,
   a step printing OS, uv, python and node versions, `fail-fast` not needed (one job). The driver dispatches
   (`gh workflow run test.yml --ref dev -f windows=true`); the log is read and each failure classified in `WP34-readout.md`.
2. **Readout.** The classification table, and a plain-options question to the supervisor on which shards Windows runs
   (the fast suite at least; slow and docs-paper if the toolchain stands up, otherwise Linux-only with the reason).
3. **Fixes** to what is ours (pathlib, utf-8 opens, newline handling, a Windows-safe staging script), each with a test;
   a test is never weakened for Windows without a stated reason in the commit.
4. **CI.** Windows folded into `test.yml` as an OS matrix entry (the shards stage 2 chose), dispatch and gates only;
   the spike job becomes the matrix entry (the input is then dropped).
5. **Documentation.** The README environment line and the reproducibility appendix (and the ledger row if the paper's
   words change, net neutral or negative) say what runs where.
6. **Review.** `WP34-review.md`: the three platforms green at one named head, the run links, the shards table.

## Requirements

| ID | Requirement | Checked by |
|---|---|---|
| R-1 | The spike job parses and runs on `windows-latest` and prints the four versions | the dispatched run's log |
| R-2 | Every failure of the spike is classified, with the log line, in `WP34-readout.md` | read |
| R-3 | Each fix has a test that fails without it on the platform it concerns, or a stated reason none can | `git diff`, the run |
| R-4 | No test is weakened for Windows without a reason in the commit message | `git log -p` on `tests/` |
| R-5 | `test.yml` carries Windows as a matrix entry | the file |
| R-6 | README and appendix state, per shard, the platforms it runs on and the reason for any exclusion | read; the claims register where a claim is made |
| R-7 | Linux and macOS results are unchanged by the fixes | the green runs at the head |
| R-8 | Repository gates: `uv run pytest`, `uv run ruff check .`, `uv run ruff format --check .`, `uv lock --check`; no AI attribution | the commands; the CI grep |

## Definition of good enough

Spike read and classified; shard decision recorded; fixes in with tests; `test.yml` runs Windows for the chosen shards;
README and appendix updated; three platforms green at the head, links in the review.

## Definition of done

Good enough is met, no open item remains unresolved, and the supervisor has accepted the work by the acceptance record.

## Agent's defaults

- Python 3.12 on Windows, matching `.python-version`.
- `bash` (Git for Windows) as the step shell so the CI scripts stay shared with Linux *(default)*.
- The spike provisions the pinned sysml-toolkit with `continue-on-error` so its failure is data.
- Node comes from the runner image; its version is printed, not pinned, in the spike.

## Blast radius

`.github/workflows/test.yml`; `WP34-*` records; `README.md`; the reproducibility appendix cell and
`paper/length_ledger.toml` if its words change; the source or test files a classified failure names, each listed in the
readout before it is touched. Anything else is a stop and a question to the PM.

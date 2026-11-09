# Note: verification in tiers (unblocked without forgoing the checks)

Written 2026-11-09 by the driver on the supervisor's direction: "are you regularly blocked waiting on
ci (which takes a long time); i think you should design a strategy to be employed by our PM that
helps keep us unblocked while also not completely forgoing the checks".

## Where the time went

| Check | Wall clock today | Who waited |
|---|---|---|
| Full suite on the Mac, one clean worktree | 12 to 20 minutes, growing with the suite (2,059 tests) | the driver, on every delivery |
| Linux run on GitHub (manual dispatch) | 16 to 26 minutes | the driver, before an acceptance |
| Staged site build for a browser pass | 3 to 5 minutes | the driver |
| The PM's former pre-push list (full paper, site, docs and contract tests in a clean worktree) | 10 to 40 minutes per push | the PM; it also held one lemma commit so long that it was pushed without its appendix |

The PM's wait is gone (pushes now follow short checks). The driver's remains, and it was spent
waiting rather than driving. Two things fix it: run the checks where nobody waits, and make the
suite fast enough that the full run is routine.

## The tiers

| Tier | When | What | Takes | Who waits |
|---|---|---|---|---|
| 0 | before every commit | lint and format on the files changed; the tests mapped to the paths changed (`scripts/check.py --changed`); for `derivation/`, the proof map and the Appendix B test with the appendix regenerated | seconds to two minutes | the author, briefly |
| 1 | before every push | the fast suite: the whole suite without the tests marked `slow` (`uv run pytest -m "not slow"`), in parallel workers | under three minutes | the author |
| 2 | continuously, on `dev` | the full suite with every check (lemma chain, proof map, ledger, lint, format, lock, attribution) on each new head, run by a watcher in the driver's clean worktree; verdicts appended to a log; the Linux run dispatched once per batch of pushes (about hourly) or when numerics changed, never per push | 15 to 25 minutes, in the background | nobody; a red verdict names the commit range since the last green and goes to the owner to fix forward within the hour |
| 3 | at an acceptance, and before any merge to `main` | tier 2 green on both platforms on the exact commit, plus the driver's browser pass | once per package | the driver, once |

The browser pass has its own worktree and server, so a staged build never waits for a suite and a
suite never waits for a build.

## What makes tier 1 possible (stream P11 of the board)

- **Slow markers.** Every test over about five seconds is marked `slow` (the perturbation test,
  notebook executions, regenerations, the planted benchmarks, site builds); `pytest --durations=30`
  lists them. The fast suite still runs every quick test, which is most of the correctness checks.
- **A path-to-tests map** (`scripts/check.py`): changed paths under `src/` run the package tests and
  doctests; `derivation/` runs the derivation and proof-map tests and the Appendix B test; `paper/`
  the paper tests; `docs/`, `site/`, `scripts/` the site and docs tests; `examples/` the case,
  experiment and notebook tests. `--changed` reads `git diff --name-only origin/dev...HEAD`.
- **Parallel workers.** `pytest-xdist` as a dev dependency (the driver owns `pyproject.toml`), with
  the tests that build the site or write shared files put in one `xdist_group` so they never run at
  the same time (a concurrent site build broke eight tests once). On this machine's ten cores the
  full suite should take a quarter of its present time, which makes tier 2 verdicts faster too.
- **CI in shards.** The Linux workflow splits the suite over two or three jobs when dispatched.

## Rules

- A push never waits for tier 2 or for CI. A merge to `main` and an acceptance always do.
- A tier 2 failure is not a reason to stop pushing: the owner of the failing files fixes forward,
  and the watcher's next verdict closes it. A failure that lasts over an hour is escalated to the
  driver.
- A test that is slow for no reason is a finding; a test that must be slow is marked, not deleted.
- The watcher's log is the evidence of record for tier 2 (`work-packages/driver-log.md` cites it).

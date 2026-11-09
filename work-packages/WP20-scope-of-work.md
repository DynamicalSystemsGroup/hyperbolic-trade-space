# WP20 - Scope of work: verification in tiers

| | |
|---|---|
| **Status** | DRAFT. Approved only by the recorded act below. Nothing in this package is executed before then. |
| **Supervisor (accountable)** | mzargham |
| **Repository** | posynomial-invariant-form, branch `dev` |
| **Approval record** | The driver's approval under the mandate of `work-packages/release-candidate.md`, quoted in `work-packages/WP20-decisions.md` |
| **Acceptance record** | A fresh-context reviewer's check against these requirements, then the driver's verification; the supervisor's acceptance at the PR |

## Purpose

The supervisor: "are you regularly blocked waiting on ci (which takes a long time); i think you should design a strategy to be employed by our PM that helps keep us unblocked while also not completely forgoing the checks." The strategy is `docs/superpowers/notes/verification-strategy.md`. This package builds what makes its tier 1 possible: a fast suite under three minutes, a path-to-tests map, safe parallel workers and a sharded Linux run. The full suite (2,059 tests, 12 to 20 minutes) stays, and runs where nobody waits.

## Goals

- G1. Every slow test is marked `slow`, so the fast suite is quick and still holds every quick check.
- G2. A changed-paths runner (`scripts/check.py`) runs the tests mapped to what changed.
- G3. The suite runs in parallel workers without tests that build the site or write shared files colliding.
- G4. The Linux workflow runs in shards.
- G5. No check is lost: no test deleted or weakened.

## Non-goals

- Deleting, rewriting or speeding up tests (a test that is slow for no reason is reported as a finding, not fixed here).
- Changing what any test asserts; editing `pyproject.toml` or `uv.lock` (the driver's); adding dependencies.
- The tier 2 watcher and the browser pass; `tests/test_container.py` (WP10 container work owns it).
- Any file outside the blast radius.

## Blast radius

Exactly these, and nothing else:

- `scripts/check.py` (new), `tests/conftest.py`, `.github/workflows/test.yml`.
- Marker lines in `tests/*.py` (added `@pytest.mark.slow` / `xdist_group` lines only), except `tests/test_container.py`.
- The `slow` marker is registered in `tests/conftest.py` (`pytest_configure` with `addinivalue_line`); `pytest-xdist` is already a dependency.
- Worktree: `/private/tmp/claude-501/-Users-z--claude-spares-spare-4Zb8mW/71474a52-35d3-48fa-82b0-c1328e96b5d6/scratchpad/pm-worktrees/WP20`. Pushes to `dev` follow `work-packages/README.md`.

## Starting point

Prior uncommitted work (28 modified files, mostly marker lines, plus `tests/conftest.py`) sits in the scratchpad worktree `wt-P11` (branch `p11`, behind `dev`). The agent takes its `git diff` as a patch, re-applies it in the WP20 worktree, drops any hunk outside the blast radius (such as a report under `examples/`), and continues.

## Deliverables

| ID | Deliverable | Serves |
|---|---|---|
| D-1 | `slow` marker registered in `tests/conftest.py`; `@pytest.mark.slow` lines in `tests/*.py` | G1, G5 |
| D-2 | `scripts/check.py` with `--changed` and `--dry-run`, plus its test or a documented `--dry-run` | G2 |
| D-3 | `xdist_group` lines on the site-building and shared-file tests | G3, G5 |
| D-4 | `.github/workflows/test.yml` in 2 to 3 shards | G4 |
| D-5 | A findings list (slow-for-no-reason tests; unmapped paths) in the handback | G1, G2 |

## Requirements

| ID | Requirement | Checked by |
|---|---|---|
| R-1 | Every test over about 5 s is marked `slow` | `uv run pytest --durations=30`: no unmarked test listed is over about 5 s |
| R-2 | `uv run pytest -m "not slow" -n auto` passes in under 3 minutes on this machine | run it and read the wall clock |
| R-3 | `scripts/check.py --changed` maps `src/` to package tests and doctests; `derivation/` to derivation, proof-map and Appendix B tests; `paper/` to paper tests; `docs/`, `site/`, `scripts/` to site and docs tests; `examples/` to case, experiment and notebook tests; reads `git diff --name-only origin/dev...HEAD` | `uv run python scripts/check.py --dry-run --changed` on a branch touching one path of each class prints the mapped tests; or its own test passes |
| R-4 | Tests that build the site or write shared files share one `xdist_group`; the full suite passes in parallel | `uv run pytest -n auto --dist loadgroup` green, once |
| R-5 | The workflow runs in 2 to 3 shards, is valid YAML, keeps the attribution check, `uv lock --check`, the locked install and the toolkit provisioning, and the shards together cover the whole suite | `uv run python -c "import yaml; yaml.safe_load(open('.github/workflows/test.yml'))"`; read the diff; compare the union of shard selections with the full collection |
| R-6 | No test deleted or weakened: the collected count is unchanged | `uv run pytest --collect-only -q` on `origin/dev` and on the result give the same count; the diff in `tests/` adds only marker lines |
| R-7 | Nothing outside the blast radius changed; lock, lint and format pass | `git diff --stat origin/dev...HEAD` names only blast-radius paths; `uv lock --check`, `uv run ruff check .`, `uv run ruff format --check .` |

## Definition of good

- The fast suite is routine to run before every push, the map covers every path in the repository, and the shards are balanced so the Linux run takes about a third of today's time.

## Definition of good enough

- Fast suite green in under 3 minutes (R-2); full suite green once with xdist (R-4); `check.py` works for each mapped path class (R-3); workflow shards valid and complete (R-5); collected count unchanged (R-6); blast radius respected (R-7); every test over 5 s marked (R-1); the reviewer's check recorded in `work-packages/WP20-review.md`.

## Definition of done

Good enough is met, **no open item remains unresolved**, the driver has verified the result, and the supervisor has accepted the work by the acceptance record above.

## Agent's defaults

- *(default)* Slow threshold: a durations entry over 5 s on this machine (R-1).
- *(default)* `check.py` runs `uv run pytest` on the mapped test files, prints the mapping with `--dry-run`, and falls back to the fast suite for an unmapped path.
- *(default)* Three shards split by test-file lists in the workflow matrix, so no new dependency (such as `pytest-split`) is needed.
- *(default)* Shards run `-n auto`; the `xdist_group` is named `site`.
- *(default)* The first push carries the re-applied patch; later pushes are one per unit (markers, group, check.py, workflow).
- *(default)* The review is recorded in `work-packages/WP20-review.md`.

## Open decisions (for the supervisor)

None.

## Gate outcomes

- 2026-11-09: approved for execution by the driver under the mandate (`release-candidate.md`), for the supervisor's review at the PR; no open decision remained. Recorded in `driver-log.md`.

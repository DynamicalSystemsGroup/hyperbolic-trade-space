# P11 - Scope of work: verification in tiers

| | |
|---|---|
| **Status** | DRAFT. Approved only by the driver's approval message under the mandate of `work-packages/release-candidate.md`, recorded in `work-packages/driver-log.md`. Nothing here is executed before then. |
| **Supervisor (accountable)** | mzargham |
| **Repository** | posynomial-invariant-form, branch `dev` |
| **Approval record** | The driver's approval message, recorded in `work-packages/driver-log.md` |
| **Acceptance record** | A fresh-context reviewer's check against these requirements, recorded in this file, then the driver's verification; the supervisor's acceptance at the PR |

## Blast radius

Exactly these, and nothing else:

- `scripts/check.py` (new), `tests/conftest.py`, `.github/workflows/test.yml`.
- Marker lines in `tests/*.py`: only the added `@pytest.mark.slow` / `xdist_group` lines, nothing else in them. Not `tests/test_container.py` (stream P10 owns it).
- NOT `pyproject.toml` or `uv.lock` (the driver's; `pytest-xdist` is already a dependency). The `slow` marker is registered in `tests/conftest.py` with `pytest_configure` / `addinivalue_line`.

Worktree: `/private/tmp/claude-501/-Users-z--claude-spares-spare-4Zb8mW/71474a52-35d3-48fa-82b0-c1328e96b5d6/scratchpad/pm-worktrees/P11` (branch `p11b` off `origin/dev`). One push per unit to `dev`: rebase on `origin/dev`, `git push origin HEAD:dev`; on refusal, rebase and retry.

## Starting point

Uncommitted prior work (28 modified files, mostly marker lines, plus `tests/conftest.py`) sits in worktree `.../scratchpad/wt-P11` (branch `p11`, behind `dev`). The agent takes it as a patch (`git diff` there), re-applies it on the fresh worktree, checks it against the blast radius (drops any hunk outside it, such as the report under `examples/`), and continues.

## Purpose

The supervisor: "are you regularly blocked waiting on ci (which takes a long time); i think you should design a strategy to be employed by our PM that helps keep us unblocked while also not completely forgoing the checks." The strategy is `docs/superpowers/notes/verification-strategy.md`. This stream builds what makes its tier 1 possible: a fast suite under three minutes, a path-to-tests map, safe parallel workers and a sharded Linux run. The full suite (2,059 tests, 12 to 20 minutes) stays, and runs where nobody waits.

## Goals

- G1. Every slow test is marked `slow`, so the fast suite is quick and still holds every quick check.
- G2. A changed-paths runner (`scripts/check.py`) runs the tests mapped to what changed.
- G3. The suite runs in parallel workers without tests that build the site or write shared files colliding.
- G4. The Linux workflow runs in shards.
- G5. No check is lost: no test deleted or weakened.

## Non-goals

- Deleting, rewriting or speeding up tests (a test that is slow for no reason is reported as a finding, not fixed here).
- Adding dependencies or editing `pyproject.toml` / `uv.lock`; the tier 2 watcher; the browser pass; `tests/test_container.py`.
- Changing what any test asserts, or any file outside the blast radius.

## Deliverables

| ID | Deliverable | Serves |
|---|---|---|
| D-1 | `slow` marker registered in `tests/conftest.py`; `@pytest.mark.slow` lines in `tests/*.py` | G1, G5 |
| D-2 | `scripts/check.py` with `--changed` and `--dry-run`, plus its test or a documented `--dry-run` | G2 |
| D-3 | `xdist_group` lines on the site-building and shared-file tests | G3, G5 |
| D-4 | `.github/workflows/test.yml` with 2 to 3 shards | G4 |
| D-5 | A findings list (slow-for-no-reason tests; unmapped paths) in the stream's handback | G1, G2 |

## Requirements

| ID | Requirement | Checked by |
|---|---|---|
| R-1 | Every test over about 5 s is marked `slow` | `uv run pytest --durations=30`: no unmarked test in the list is over about 5 s |
| R-2 | `uv run pytest -m "not slow" -n auto` passes and completes under 3 minutes on this machine | run it, read the wall clock |
| R-3 | `scripts/check.py --changed` maps changed paths per the note: `src/` to package tests and doctests; `derivation/` to derivation, proof-map and Appendix B tests; `paper/` to paper tests; `docs/`, `site/`, `scripts/` to site and docs tests; `examples/` to case, experiment and notebook tests; it reads `git diff --name-only origin/dev...HEAD` | `uv run python scripts/check.py --dry-run --changed` on a branch touching one path of each class prints the mapped tests; or its own test passes |
| R-4 | Tests that build the site or write shared files share one `xdist_group`, and the full suite passes with `-n auto` | `uv run pytest -n auto --dist loadgroup` green, once |
| R-5 | The CI workflow runs in 2 to 3 shards, is valid YAML, and keeps the attribution check, `uv lock --check`, the locked install and the toolkit provisioning | parse with `uv run python -c "import yaml; yaml.safe_load(open('.github/workflows/test.yml'))"`; read the diff; the union of shards covers the whole suite |
| R-6 | No test deleted or weakened: the collected count is unchanged | `uv run pytest --collect-only -q` on `origin/dev` and on the result give the same count; the diff in `tests/` adds only marker lines |
| R-7 | Nothing outside the blast radius changed; `uv lock --check`, `ruff check .` and `ruff format --check .` pass | `git diff --stat origin/dev...HEAD` names only blast-radius paths |

## Definition of good

- The fast suite is routine to run before every push, the map is complete for every path in the repository, and the shards are balanced so the Linux run takes a third of today's time.

## Definition of good enough

- Fast suite under 3 minutes and green (R-2); full suite green once with xdist (R-4); `check.py` works for each mapped path class (R-3); workflow shards valid and complete (R-5); collected count unchanged (R-6); blast radius respected (R-7); reviewer's check recorded in this file.

## Definition of done

Good enough is met, **no open item remains unresolved**, the driver has verified the result, and the supervisor has accepted the work by the acceptance record above.

## Agent's defaults

- *(default)* Slow threshold: a test whose durations entry exceeds 5 s on this machine (R-1).
- *(default)* `check.py` runs `uv run pytest` on the mapped test files, prints the mapping with `--dry-run`, and falls back to the fast suite for an unmapped path.
- *(default)* Three shards using `pytest-split`-free splitting (by test file groups, via matrix and `-k` / path lists), so no new dependency is needed.
- *(default)* Shards run `-n auto`; the `xdist_group` is named `site`.
- *(default)* The first push carries the re-applied patch; later pushes are one per unit (markers, group, check.py, workflow).

## Open decisions (for the supervisor)

None.

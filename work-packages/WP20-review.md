# WP20 - Acceptance review (first delivery: 04a3471, 78f5e1c)

Reviewer: fresh context, clean detached worktree at origin/dev (4243145). Nothing was edited or repaired.
The reviewer does not accept; the driver verifies and the supervisor accepts at the PR.

## Requirements

| ID | Verdict | Evidence |
|---|---|---|
| R-1 every test over about 5 s is marked slow | **Not met** (marginal, one clear case) | `pytest -m "not slow" --durations` on the fast suite lists unmarked entries over 5 s. Serial rerun of the heavy modules (`-p no:cacheprovider`, no xdist): `test_paper.py::test_generated_sentences_committed_output_is_current` 39.7 s setup (the first user of a fixture that is not in `SLOW_FIXTURES`); sklearn-compat checks 5.2 to 8.9 s (`check_transformer_data_not_an_array` 8.9 s, `check_estimators_dtypes` 6.3 s, `check_pipeline_consistency` 5.7 s, `check_dtype_object` 5.2 s); `test_plotting.py::test_ternary_marker_table_matches_the_drawn_markers_and_levels` 5.05 s (9.1 s under xdist); `plot_ternary` doctest 5.4 s under xdist. Under xdist load more entries pass 5 s. The 40 s paper setup is the clear miss: that test is billed for a fixture that costs 40 s. |
| R-2 fast suite under 3 min | **Met** | `uv run pytest -m 'not slow' -n auto --dist loadgroup`: 1734 passed, 16 skipped, 1 xfailed in 129.9 s (2:11 wall) on 10 cores. (Serial run of the five heavy modules alone took 165 s, so the margin rests on xdist.) |
| R-3 check.py maps path classes | **Met, with two deviations** | `--list` prints the map. `mapped_tests` per path class: `src/` to package tests and doctests (`src` collected); `derivation/` to test_derivation, test_matches_derivation, test_proof_map and `test_paper.py -k appendix_b`; `paper/` to test_paper, test_paper_sources, test_case (`paper/container/` to test_container); `docs/` to test_site, test_docs, test_narrative, test_references; `site/` to test_site, test_narrative; `scripts/` to test_site, test_build_generated, test_check_script; `examples/` to adcs, case, k_terms, cubesat model, notebook tests, plus experiments, v2 model and oracle tests for their subtrees; `tests/test_*.py` runs itself; also `.github/`, `mkdocs.yml`, `glossary.yaml`, `Dockerfile`, `pyproject.toml`, interface contract. `tests/test_check_script.py` passed in the full run. I called `mapped_tests` directly and `--list`; I did not run `--dry-run --changed` on a real branch. Deviation 1: it reads `git diff --name-only origin/dev` (working tree against origin/dev, plus untracked files), not `origin/dev...HEAD`; on a branch behind origin/dev it lists upstream changes as local. Deviation 2: an unmapped path (`README.md`, `work-packages/*`, `uv.lock`, `tests/conftest.py`) maps to nothing and there is no fallback to the fast suite, which the agent's default stated and "the map covers every path" (definition of good) implies. |
| R-4 xdist_group; full suite parallel | **Met** | `conftest.py` puts every test using the `assembled` or `generated_dir` fixtures, or in `test_build_generated.py`, into `xdist_group("site")` (marker lines in test files add the rest). `uv run pytest -n auto --dist loadgroup`: 2116 passed, 16 skipped, 1 xfailed in 544 s (9:04). (A first attempt was spoiled by my own probe files in the worktree and was killed; the figures are from a clean second run.) |
| R-5 workflow shards | **Met** | `yaml.safe_load` succeeds. Matrix `[fast, slow, docs-paper]`. Attribution check, `uv lock --check`, `uv sync --locked`, toolkit restore/provision/save and `REQUIRE_OPENSYSML` all retained in every shard. Union check by collection: fast (`-m "not slow"`) 1751 + slow outside the six docs modules 325 + slow inside them 57 = 2133 = the full collection. Not measured: shard balance (no CI run exists). Observation: the docs-paper shard runs only 57 tests; fast carries 1751. |
| R-6 collected count unchanged | **Met** | Parent of 04a3471 (26b62ae): 2114 collected. At 78f5e1c: 2133; with the two new files excluded (`test_check_script.py`, `test_ci_shards.py`): 2114. Diff of existing `tests/*.py`: only `@pytest.mark.slow` / `xdist_group` lines and five `pytestmark = pytest.mark.slow` module lines (with a comment); no line removed. |
| R-7 blast radius; lock, lint, format | **Met, one observation** | `git diff --stat 04a3471^ 78f5e1c`: `.github/workflows/test.yml`, `scripts/check.py`, `tests/conftest.py`, 28 `tests/*.py` marker edits, and two new test files; `test_container.py` untouched; `pyproject.toml` and `uv.lock` untouched. `uv lock --check` ok; `ruff check .` passes; `ruff format --check .` 270 files formatted. No attribution lines in the two commits. Observation: the two new test files are not named in the blast radius (D-2 permits the check script's test; `test_ci_shards.py` is an addition). |

## Goals, non-goals, deliverables

- G1 to G5: G1 mostly (see R-1), G2 yes, G3 yes, G4 yes, G5 yes (count unchanged, markers only).
- D-1 to D-4 present. **D-5 (findings list in the handback): not checkable** here; the handback was not in my input. The R-1 list above is a finding the delivery should have carried.
- Non-goals: no test deleted or rewritten, no assertion changed, no dependency added, `test_container.py` not touched.

## Gaps for the driver

1. R-1: mark the 40 s `test_paper` set-up consumer (add its fixture to `SLOW_FIXTURES`), the slowest sklearn-compat checks (or the module's parametrized cases over 5 s), and the ternary-marker table test; or the supervisor accepts "about 5 s" as covering 5 to 9 s.
2. R-3: add the unmapped-path fallback (fast suite) and say whether `origin/dev` (working tree) or `origin/dev...HEAD` is intended.
3. Unrequested behaviour change: the workflow no longer runs on push or pull request to `main`; it is `workflow_dispatch` only (`test_ci_shards.py` asserts it). The scope's G4 asks for shards only, and CLAUDE.md says `main` gets a no-ff merge "when content merits a CI run". The driver should confirm this was intended and recorded.
4. Shard balance is unmeasured; fast shard holds 1751 of 2133 tests.

## Recommendation

Accept after gap 1 and gap 3 are resolved (R-1 is not met as written; the rest is met). Gap 2 and 4 are minor and may be follow-ups. Full suite: 9:04 parallel, green.

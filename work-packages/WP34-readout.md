# WP34 — Readout of the Windows spike (stage 2)

Run 43070927422, job "windows (fast)" (job 130698271215), `windows-latest` on branch `dev` at the spike's head.
Every quotation below is a line of that job's log.

## The run

| Item | Value |
|---|---|
| Runner | `Microsoft Windows Server 2025 10.0.26100`, image `windows-2025-vs2026` |
| Versions step | `uv 0.13.7`, `Python 3.12.10`, `v22.23.4` (node), `git version 2.56.0.windows.4`; `core.autocrlf` prints `true` |
| Setup, lock check, ruff check, ruff format check | pass (`All checks passed!`, `577 files already formatted`, `Resolved 178 packages`) |
| Pinned sysml-toolkit provisioning | pass: `binary: C:\Users\runneradmin\.cache\hyperbolic-trade-space\sysml-toolkit\v0.12.0\bin\sysmlv2.exe` |
| Fast suite, last line | `20 failed, 1755 passed, 17 skipped, 2 xfailed, 6 warnings, 54 errors in 245.36s (0:04:05)` |
| Test step time | 4 min 5 s (245.36 s); job from 17:43:44Z to 17:48:15Z, about 4.5 min |
| Job result | `##[error]Process completed with exit code 1.` |

Passed 1755, failed 20, errors 54 (74 non-passing items), skipped 17, xfailed 2.

## Classes

| Class | Items | Tests | Cause, from the log | Fix class and size |
|---|---|---|---|---|
| Tooling or environment: no `z3` on PATH | 54 errors + 1 failure | `test_model_checking_v2.py` 44 errors; `test_cubesat_oracle.py` 8 errors; `test_legacy_oracle.py` 2 errors; `test_case_model_howto.py::test_the_exclusion_example_runs` (failure) | `the solve engine needs z3 or cvc5 on PATH and none was found: run through `uv run``; the code checks `shutil.which("z3") or shutil.which("cvc5")` (`examples/adcs/experiments/exclusion.py:60`); the install step did add `+ z3-solver==5.3.3.0`, so the package is present and no `z3` executable is found on PATH | One source function (find the solver through the `z3` module when no executable is on PATH) or one CI step; small. The log does not show whether the Windows wheel ships an executable; decide after one local look at the wheel |
| Path or encoding: `read_text()` with no encoding | 6 failures | `test_case_model_howto.py::test_each_toolkit_row_is_complete_and_cites_a_recorded_probe`, `::test_probe_numbers_are_the_probes_of_the_module_in_order`; `test_model_checking_v2.py::test_pin_agrees_with_the_probe_record_assets`, `::test_engine_names_of_the_probe_record_exist`; `test_system_model_v2_r1.py::test_the_legend_names_every_colour_and_line_kind_and_the_type_has_a_floor`, `::test_committed_views_are_the_generators_output_on_the_model` | `UnicodeDecodeError: 'charmap' codec can't decode byte 0x81 in position 19442` raised in `cp1252.py:23`, from `text = RECORD.read_text()`, `PROBE_RECORD.read_text()`, `(VIEWS / "behavioural_view.svg").read_text()` | Test-side: add `encoding="utf-8"` to those reads (6 tests, about 4 call sites); small. A source-side audit of other `read_text()` / `open()` calls without an encoding is a separate grep |
| Line endings: committed text read as CRLF, hashes differ | 5 failures + 1 failure with the same symptom | `test_experiments.py::test_adopted_entries_for_each_frozen_file_with_equal_hashes`, `::test_committed_ledger_verifies_and_predictions_precede_checks` (`Left contains 58 more items, first extra item: Drift(entry_id='adopted-adcs_designs', what='code file changed'`); `test_mutation_v2.py::test_the_oracles_model_path_is_the_committed_file_the_ledger_hashes` (`AssertionError: v2-primary`); `test_v2_data.py::test_every_frozen_and_v2_file_has_a_ledger_entry_with_the_file_hash` (`AssertionError: examples/adcs/data/adcs_designs.csv`), `::test_experiments_verify_passes`; `test_paper.py::test_appendix_b_committed_output_is_current` (`tab-B-checker`, one differing line: the `record` digest) | The checkout step ran with `core.autocrlf` = `true`; the text read in the encoding failures shows `\r\n` in the bytes (`b'# Probe record: ... runtime ... observed ...\r\n\r\nObserved at opensysml 0.12.1'`); each failure is a sha256 of a committed file differing from the ledger (`72b20f6b...` against `6c257ddb...`). The log shows the CRLF and the digest mismatch; it does not show the digests were computed over CRLF bytes, which one local run with `git config core.autocrlf true` would show | One `.gitattributes` (`* text=auto eol=lf`, or `eol=lf` for the hashed paths); small, and it changes how Windows checks out, not Linux or macOS |
| Platform difference in the code under test: executable form of the test archive | 6 failures | `test_toolkit.py::test_cache_hit_opens_no_connection`, `::test_retry_on_transient_then_success`, `::test_fallback_to_the_release_assets_api`, `::test_api_fallback_sends_the_token`, `::test_local_archive_installs_when_it_matches`, `::test_cli_fetch_archive` | `OSError: [WinError 216] This version of %1 is not compatible with the version of Windows you're running` at `examples\adcs\experiments\toolkit.py:382`, `subprocess.run([str(binary), "--version"], ...)`; the fixture's archive payload is `#!/bin/sh\necho 'sysmlv2 0.12.0'` (`tests/test_toolkit.py:24`), a POSIX script that Windows cannot execute | Test written for POSIX: a Windows branch of the fixture payload (a `.cmd` or the Python executable) or a skip with the reason; small. The real provisioning step passed, so the code under test works on the real Windows binary |
| Other: cause not in the log | 1 failure | `test_paper.py::test_c_committed_output_is_current` | `AssertionError: tab-C-datasets: re-run `uv run python paper/execute_notebooks.py` to refresh the committed outputs`, `assert False` after the tolerance comparison (`_same_text(... rtol)`); no differing line is printed | Needs one local reproduction with the printed text diff before it can be classed: line endings (as the neighbouring tab-B), registered numerical drift, or a path in the output |

Counts by class: tooling 55 (54 errors and 1 failure), encoding 6, line endings 6 (5 plus tab-B), POSIX-written test 6, other 1. Items: 20 failures and 54 errors; 20 + 54 = 74 = 55 + 6 + 6 + 6 + 1.
Not seen in this run: path separators, temp directories, fonts, missing wheels for scipy, HiGHS or Z3, node for mystmd (the fast shard does not run them), and registered numerical drift.

## Not in this run

The slow shard and the docs-paper shard did not run on Windows in this spike; their toolchain (mystmd and node, the paper build, the container tests) is not tested by this readout. The versions step shows node `v22.23.4` on the image.

## Options for the supervisor

Which shards should Windows run in `test.yml` once the fixes are in?

1. The fast shard only. Smallest set; the failures above are the whole work; the README says slow and docs-paper are Linux and macOS.
2. The fast shard and the slow shard. One more spike run (dispatch with the slow shard) before the decision; adds the cost of the slow shard's time on Windows at each gate.
3. All three shards. Needs a spike of the docs-paper shard (node, mystmd and the paper build on Windows) first; the README then states three platforms for all shards.

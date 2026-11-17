# WP68 D-3: the local checks on the head (G4; checklist rows B1 to B5, R-1, R-4)

Run on this Mac in the `wp68` worktree on 2026-11-17, on the tree the two WP68 commits carry (the version, the
changelog, the punch list and this file), with `MPLCONFIGDIR` in the scratchpad and `NO_MKDOCS_2_WARNING=1`.
Every command is the one in the row, from the repository root; pytest output went to a log, never a pipe. The
hosted-runner links are the release pull request's checks and the `qc/release` dry run, recorded in
`record.md` when the driver runs them (R-2, C6).

| Row | Check | Command | Exit | Last line of the log |
|---|---|---|---|---|
| B1 | The software suite, paper tests deselected (includes the slow tests) | `uv run pytest -q -m "not paper"` (under `nohup`) | 1 | `1 failed, 2465 passed, 12 skipped, 266 deselected, 2 xfailed, 27 warnings in 4423.11s (1:13:43)`; the failure is `tests/test_interface_contract.py::test_r2_version_one_authority_pep440`: `manifest version '0.0.1' must equal '0.1.0'; a bump edits both together` (the interface contract's manifest holds a fifth copy of the version; its R-2 says the bump edits it in the same commit). Fixed inside G1: `work-packages/interface-contract.toml` `[package].version`, the quoted block and section 5's current value read 0.1.0; no amendment (R-2 pre-authorises the bump; `contract_version` stays 29). The 266 deselected are the paper's tests |
| B1 | Lint | `uv run ruff check .` | 0 | All checks passed! |
| B1 | Format | `uv run ruff format --check .` | 0 | 527 files already formatted |
| B1, A6 | Lock | `uv lock --check` | 0 | Resolved 194 packages in 6ms |
| B1 | The lemma chain | `uv run python derivation/run.py` | 0 | ALL LEMMAS PASS. |
| B1 | The proof-map checker | `uv run python -m derivation.proofmap` | 0 | PROOF MAP OK: 22 lemma files, 549 tagged steps (L1:8, L2:8, ... (22 lemma files, 549 tagged steps) |
| B2s | Vocabulary, software surfaces | `uv run python scripts/check_vocabulary.py --surface software --baseline scripts/vocabulary_baseline.toml` | 0 | 0 new violation(s), 28 known (surface software) |
| B3s | Claims register, software surfaces | `uv run pytest -q tests/test_claims_register.py` | 0 | 22 passed, 1 deselected in 3.22s |
| B4s, R-4 | Attribution lines, the scope's command | `git log --format=%B e7fd1165..HEAD \| grep -ciE "co-authored-by\|generated with"` | 0 (grep found lines) | count 2: both are the words "regenerated with" inside sentences of e8abe46e (the CI step's own commit, whose subject says this) and 6de8f687 (a report regenerated with new data); neither is an attribution line |
| B4s, R-4 | Attribution lines, the CI step's rule (`test.yml`, whole words) | `git log --format=%B e7fd1165..HEAD \| grep -ciE '\bco-authored-by\b\|\bgenerated with\b\|🤖'` | 1 (grep found no line) | count 0; the same over the whole history (`git log --format=%B`): count 0 |
| B5 | Generated pages, figures and site figures before the build | `uv run python scripts/build_generated.py`; `uv run python scripts/build_figures.py`; `uv run python scripts/build_site_figures.py` | 0 / 0 / 0 | `labels ['all three trade', 'metric 3 trades against metric 1', 'metric 3 trades against metric 2']` (the glossary written; 22 images built) |
| B5 | Docs build, strict, abstract slot | `HTS_PAPER_SLOT=abstract uv run --group docs mkdocs build --strict` | 0 | `INFO    -  Documentation built in 1.37 seconds` |
| B5 | Docs build, strict, pin slot | `HTS_PAPER_SLOT=pin uv run --group docs mkdocs build --strict` | 0 | `INFO    -  Documentation built in 1.03 seconds` |
| B1 (rerun) | The contract, index and release tests after the manifest fix, on the final tree | `uv run pytest -q tests/test_interface_contract.py tests/test_index.py tests/test_release_version.py tests/test_release_checks.py` | 0 | `121 passed in 64.42s (0:01:04)`; the rest of the suite was not re-run: the manifest edit is read by these tests only |
| (index) | The index test (every hash and path in `INDEX.md` dereferences; no bare mention of a removed path) | `uv run pytest -q tests/test_index.py` | 0 | 5 passed in 3.66s |
| R-1 | The version in the four places | `grep -rn "0\.0\.1" pyproject.toml CITATION.cff src CHANGELOG.md`; `uv run python -c "import hyperbolic_trade_space as h; print(h.__version__)"` | 1 (no match) / 0 | (no match); `0.1.0` |
| A2 | The changelog gate as `release.yml` runs it | `uv run python scripts/release_checks.py changelog --version 0.1.0`; the same with `--final --notes <file>` | 0 / 0 | (silent); the notes file begins at `### Added` |

Reading of the rows: the suite's one failure was the version itself and is fixed above; the one count above zero is the scope's attribution grep, which has no word boundaries and
so matches "regenerated with"; the rule the release pull request runs is the CI step's, which counts 0.
`grep -n -i 'unreleased\|target' CHANGELOG.md` (A2's command) matches one line, the public function name
`frontier_targets` in the WP3 entry, which stays.

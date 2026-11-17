# WP79 G1: the rehearsal of parallel work on `paper` and `dev`

Unit A, 2026-11-17, in a worktree on the branch `rehearsal` (cut from `origin/paper` at c0e210cc). This file and
`WP79-decisions.md` are the unit's only tree changes; `dev`, `main` and `paper` were not edited, no tag was created,
no pull request, release or issue was opened. Every command below ran in the worktree; exit codes are the shell's.

## The branches at the start

| Ref | Head | Note |
|---|---|---|
| `origin/paper` | c0e210cc | the cut named by the scope |
| `origin/dev` | efb74de6 | three commits behind `paper`: 6ba9ad9e (records), 922520fd (the rename to `tradespace`), c0e210cc (the ledger re-adoption) |
| local `dev` (the main checkout) | c0e210cc | equal to `paper`; not pushed |
| `origin/main` | e7fd1165 | |

`git rev-list --count origin/paper..origin/dev` = 0; `git merge-base origin/paper origin/dev` = efb74de6. The
rename commit 922520fd is on `paper` and on the local `dev`, not on `origin/dev`.

Baseline of the outward state (R-2 of WP67, repeated): `git ls-remote --tags origin` empty; `gh release list` empty;
`git ls-remote --heads origin 'qc/*'` empty. The same at the end (section 7).

## 1. The paper built and tested from `paper` on hosted runners

Two runs of `paper.yml` on c0e210cc, both on `ubuntu-24.04` (x64, Python 3.12.3), neither publishing anything:

| Event | Run | Clock | Result |
|---|---|---|---|
| push of c0e210cc to `paper` (the branch's creation) | [44122627220](https://github.com/DynamicalSystemsGroup/tradespace/actions/runs/44122627220) | 16:10:03Z to 17:20:08Z (1 h 10 min); the tests step 16:11:11Z to 17:20:03Z | `build` failed at "The paper's tests": `3 failed, 263 passed in 4132.42s (1:08:52)`; the steps after it (the myst build, the key manifest, the pack, the artefact) did not run; `release` and `on-failure` skipped |
| `gh workflow run paper.yml --ref paper` (17:20:46Z, after the push run ended; `workflow_dispatch` takes no inputs, so the build-and-test form is the only one) | [44135949342](https://github.com/DynamicalSystemsGroup/tradespace/actions/runs/44135949342) | 17:20:46Z to 19:00:00Z (1 h 39 min) | `build` failed at "The paper's tests": `3 failed, 263 passed in 5896.69s (1:38:16)`, the same three tests; the later steps did not run; `release` and `on-failure` skipped. One difference from the push run: the fresh planted-table digest on this runner is `fa86f857...`, not the push run's `f6c45d25...` (section 2.2) |

The push run's three failures (`gh run view 44122627220 --log-failed`), the same three as WP67 G4 and G5:

- `tests/test_paper.py::test_myst_builds_the_html_site - assert 0 == 3`
- `tests/test_paper.py::test_notebooks_execute_from_a_clean_kernel_and_match_the_committed_outputs - AssertionError: tab-F-datasets`
  (`+ 0 | 900 | c127dd4c...993f | none |` committed, `- 0 | 900 | f6c45d25...586e | none |` fresh on the runner)
- `tests/test_residuals.py::test_paper_residual_counts_do_not_rise - AssertionError: against the baseline (head c0fe11b): 52 count(s) rose`

No other step failed; the mode check read the committed abstract mode, the lockfile check, the locked install, the
toolkit provisioning and the generated pages passed. Section 2 has the causes.

## 2. The three paper tests that fail on hosted runners

Source of the failures: WP67 G4, run 43988092221 (`qc/paper/build` at f05ad97c), job `build`, step "The paper's tests",
`gh run view 43988092221 --log-failed`; the lines quoted are that log's.

### 2.1 `tests/test_residuals.py::test_paper_residual_counts_do_not_rise`

**Log.** `AssertionError: against the baseline (head c0fe11b): 52 count(s) rose`, then the 52 lines
(`paper/paper.ipynb: long_sentences 46 -> 66`, `paper/methods: parens 19 -> 35`, `appendix/title: long_sentences 1 -> 10`, ...).

**Cause.** Not the platform: the committed baseline `scripts/residuals_baseline.json` was written at c0fe11b (WP38,
"taken at the dev head c0fe11b; taken again when the pass starts") and the paper's prose has moved since (WP56, WP57,
WP66). The same comparison on the Mac at c0e210cc fails with the identical 52 lines:

```
uv run python scripts/check_residuals.py --compare scripts/residuals_baseline.json --strict --views paper,appendix
# exit 1; "against the baseline (head c0fe11b): 52 count(s) rose"; the 52 lines sorted are byte-equal to the runner's
```

WP64-decisions (the driver's run on the rebased WP66 branch, 2026-11-16) and WP67 both record it as known. The test
fails everywhere the paper tests run; it is listed with the two platform items because the three fail together on the
runner, where the paper tests run and nowhere else by his decision.

**Smallest fix (proposal, not applied).** Re-take the baseline on `paper` at the head that is tagged first:

```
uv run python scripts/check_residuals.py --write-baseline scripts/residuals_baseline.json
uv run python scripts/check_residuals.py --compare scripts/residuals_baseline.json --strict --views paper,appendix
```

Done into the scratchpad at c0e210cc: the baseline written (`head c0e210cc`, 94 surfaces), the comparison exits 0 with
"0 count(s) rose". `--write-baseline` takes no `--views` (it writes the whole report), so the re-taken file also
re-baselines the docs and README views, which the fast suite's residual tests compare with their own views. Two
ways to narrow instead: accept the 52 rises row by row (his read; the WP64 line "retake the baseline with his read,
or accept the rises row by row"), or re-take and record in the file's `note` which package moved the counts. The
baseline is a software-side file (`scripts/`) that the paper's test reads: re-taking it on `paper` puts the change on
the path `paper` → `dev`, which the design allows (2.1) but which a contributor to the paper cannot do alone.

### 2.2 `tests/test_paper.py::test_notebooks_execute_from_a_clean_kernel_and_match_the_committed_outputs`

**Log.** `AssertionError: tab-F-datasets`; the one differing line is the planted table's row:

```
- 0 | 900 | f6c45d25f1de48f534c680e1ebfd878fc935fe34177b1d5bc2a2685a7850586e | none |   (the fresh execution on the runner)
+ 0 | 900 | c127dd4c99380d0409a7144811785537b272b0ad80bf64e3b6a6bcd0d9f8993f | none |   (the committed output)
```

**Cause.** The platform's floating point. The row's `SHA-256` column is
`hashlib.sha256(np.ascontiguousarray(X).tobytes())` of the 900-row planted table (`paper/generate_model.py::datasets`,
`make_frontier_data` with `random_state` 0): a hash of floats. `paper/environment_values.toml` lists this value
(`planted_table_sha256`) with its three digests: `b17d4f8f...` in the container of record (Linux arm64), `c127dd4c...`
on macOS arm64, `f6c45d25...` on Linux amd64 (CI). The committed `paper/supporting_material.ipynb` carries `c127dd4c`
three times and neither of the other two (`grep -c`): the notebook was last executed on the Mac (922520fd), not in
the container, and the hosted runner is amd64. The per-cell test of the F tables
(`tests/test_paper.py`, `_cells_of("F")`, lines 1346-1357) already handles this: outside the environment of record it
compares the text with `_mask_exact_only` (the digest blanked) and `_same_text` (numbers within `text_rtol`). The
clean-kernel test compares `_out_text` byte for byte for every cell but `tab-H-toolchain`, so it asserts an exact
equality that `tests/_env.py` says holds only in the environment of record.

The two runs of section 1 add a fourth digest: the push run's fresh value was `f6c45d25...` (the toml's "Linux
amd64") and the dispatch run's, on another `ubuntu-24.04` x64 runner an hour later with the same code and lockfile,
was `fa86f857...`. The hash of the floats differs between two hosted runners of the same image, so "Linux amd64" is
not one value either (the maths library's code path follows the processor); an exact comparison of this digest is
exact only in the container of record, as `tests/_env.py` says.

**Reproduction.** On the Mac the committed digest is the Mac's, so the test passes; on any amd64 Linux (a hosted
runner, or `docker run --platform linux/amd64` of the `hts-alt` image) it fails on this row; in the container of record
it fails too, on `b17d4f8f` against `c127dd4c`, until the notebook is re-executed there (the re-pin gate of 2.5, which a
`working` tag does not require).

**Smallest fix (proposal, not applied).** In the clean-kernel test, compare each cell the way the F-table test does when
`not exact_only("planted_table_sha256")`:

```python
if exact_only("planted_table_sha256"):
    assert _out_text(ca) == _out_text(cb), ca.id
else:
    rtol = listed()["planted_table_sha256"]["text_rtol"]
    assert _same_text(_mask_exact_only(_out_text(ca)), _mask_exact_only(_out_text(cb)), rtol), ca.id
```

`_mask_exact_only` blanks only the planted row's digest and `_same_text` keeps every other digest exact, so the
file hashes of the regimes' CSVs stay compared. The `elsewhere` text of `planted_table_sha256` in
`environment_values.toml` gains this test's name. Alternative with a wider effect: execute the notebooks in the
container of record before the first tag, so the committed digest is the record's (`b17d4f8f`); the runner would still
differ (amd64), so the test change is needed in either case.

### 2.3 `tests/test_paper.py::test_myst_builds_the_html_site`

**Log.** `assert 0 == 3`, `where 0 = len([])`, at
`urls = re.findall(r'"url":"(/build/fig[\w.-]+\.png)"[^]]*?full-size figure', page)`.

**Cause.** The workflow's environment. `paper.yml` sets `BASE_URL: /tradespace/paper` for the whole run (its line 26,
specification 2.2) so the published build's asset paths carry the Pages prefix; the test step inherits it, the test's
own `myst build --html` subprocess inherits the test's environment, and the built `index.json` names the figures as
`/tradespace/paper/build/fig-...png`. The regular expression anchors on `"/build/fig`, so it matches nothing.
Locally `BASE_URL` is unset and the paths are `/build/fig-...png`.

**Reproduction on the Mac** (the runner's variable, nothing else):

```
BASE_URL=/tradespace/paper PAPER_BUILD=1 uv run pytest -q tests/test_paper.py::test_myst_builds_the_html_site
# exit 1: FAILED ... - assert 0 == 3   (19.5 s)
PAPER_BUILD=1 uv run pytest -q tests/test_paper.py::test_myst_builds_the_html_site
# exit 0: 1 passed in 8.35s
```

The pin-flow build of section 4 (`BASE_URL=/paper`) shows the same prefix in its `index.json`:
`"url":"/paper/build/fig-fleet-ternary-8aab...png"`.

**Smallest fix (proposal, not applied).** The test reads the prefix it was built under:

```python
base = os.environ.get("BASE_URL", "").rstrip("/")
urls = re.findall(rf'"url":"{re.escape(base)}(/build/fig[\w.-]+\.png)"[^]]*?full-size figure', page)
```

and the file check `(html / u.lstrip("/")).is_file()` is unchanged, since the build writes the files under
`_build/html/build/` whatever the prefix. The alternative, running the test's subprocess with `BASE_URL` removed,
would test a build other than the one published.

## 3. Where the branches touch

**The merge as scoped.** On the local branch `qc/paper/touch` (from `origin/paper`, never pushed), one paper-only
edit: a sentence appended to the last headed markdown cell of `paper/paper.ipynb` (cell `bibliography`, written
with `nbformat` so the file's formatting is untouched): `git diff --stat` = `paper/paper.ipynb | 4 +++-`, three
inserted lines and one changed. Committed as 43ac9334. Then:

```
git merge --no-edit origin/dev      # "Already up to date."  exit 0
```

Nothing to merge: `origin/dev` (efb74de6) is an ancestor of `paper` (section 0), so the merge the scope asked for
cannot show where the branches touch until `dev` moves. `git diff --stat origin/dev qc/paper/touch` is the other
direction, 176 files (the three unpushed commits and the edit).

**The same merge with a software-side change standing in for `dev`.** A second local branch `qc/paper/touch-dev`
(from `origin/paper`) carries one commit, 143691bf, appending a comment line to each of the two files the
specification names as edited by both sides (2.1: `docs/references.bib`, `glossary.yaml`). Merged into
`qc/paper/touch`:

```
git merge --no-edit qc/paper/touch-dev
# Merge made by the 'ort' strategy.  docs/references.bib | 2 ++   glossary.yaml | 2 ++   exit 0
git status --short                  # clean (the record's directory untracked)
git diff --stat origin/paper HEAD   # docs/references.bib 2, glossary.yaml 2, paper/paper.ipynb 4 (+7, -1)
```

No conflict: different files, and in the shared files different lines. A conflict needs the same lines of
`references.bib` or `glossary.yaml` edited on both sides, which the specification already names as the case
resolved on `paper` (2.1).

**Where they touch, by inspection** (the links the design expects, read from the files):

| Software side reads from `paper/` | Paper side reads from the software |
|---|---|
| `scripts/paper_keys.py` (MkDocs hook): `paper/paper-keys.json`, `paper/mode.toml` | `paper/myst.yml`: `../docs/references.bib` |
| `scripts/assemble_site.py`, `scripts/stage_site.py`: `paper/mode.toml`, `paper/paper-keys.json` | the generators: `examples/adcs/data/v2/`, `examples/adcs/experiments/ledger/`, `glossary.yaml`, `derivation/`, `docs/superpowers/notes/abstraction-gaps.md`, `uv.lock`, `pyproject.toml` |
| `scripts/paper_abstract.py`: the front matter of `paper/paper.ipynb` (title, abstract), `paper/myst.yml` (author) | `tests/test_paper.py`, `tests/test_residuals.py`, `tests/_env.py`: the paper's tests live in the software's `tests/` and read `scripts/residuals_baseline.json`, `paper/environment_values.toml` |
| `scripts/check_vocabulary.py`, `scripts/prose_surfaces.py`, `scripts/check_residuals.py`: the notebooks' prose | |

One instance of the software side editing `paper/` on `dev`, against 2.1's "`dev` does not edit `paper/` except by
merging `paper` in", is on the branch already: the rename commit 922520fd changed 14 files under `paper/` (the
generators' imports, `myst.yml`'s address, `pin_links.py`, `paper.ipynb`, `supporting_material.ipynb` by 2,810
lines after a re-execution, `supplement/reading-pass.md`). It landed before the cut, so no merge was needed; a
rename after the cut would have been the first `dev` → `paper` merge with content, not links, on both sides.

## 4. The pin flow with a local artefact

As WP67 G8, with the composer's strict slot, on this worktree only; `paper/mode.toml` restored at the end.

1. The paper built with the path the staging server serves it at, and packed as `paper.yml` packs it (GNU tar
   writes no resource forks; on the Mac `COPYFILE_DISABLE=1`):

   ```
   cd paper && BASE_URL=/paper ../.venv/bin/myst build --html      # exit 0
   uv run python paper/build_keys.py --check --xref paper/_build/html/myst.xref.json   # build_keys: ok (121 keys), exit 0
   COPYFILE_DISABLE=1 tar -czf <scratch>/artefact/paper-html.tar.gz -C paper/_build/html .
   cp paper/paper-keys.json <scratch>/artefact/
   # 1,299 members, 0 of them ._ forks (WP67's second packing had the same 1,299)
   # sha256 paper-html.tar.gz e0f3668d9ff6181fc18506ee7347060f5289295b2c57897c9f3715c82be50c68
   # sha256 paper-keys.json   8777f468067d1ba71cc6b76ec11c39593b3c97c1511e565a06c27b9c698f262d (= WP67's)
   ```

2. The mode file, as a pin would write it (step 1 of 2.4 by the script; steps 3 and 4 by hand, since no tag and no
   release exist):

   ```
   uv run --no-project python scripts/paper_pin.py prepare --tag paper-working-20261117 --dry-run   # exit 0
   uv run --no-project python scripts/paper_pin.py prepare --tag paper-working-20261117             # written, exit 0
   # doi = "10.5281/zenodo.123" and sha256 = e0f3668d... written by sed (record needs gh release download)
   uv run --no-project python scripts/paper_mode.py check --stage served   # paper_mode: ok working paper-working-20261117
   uv run --no-project python scripts/paper_mode.py show | tail -1
   # banner: Working paper · paper-working-20261117 · 2026-11-17 · DOI 10.5281/zenodo.123
   ```

3. The composer. `stage_site.py` has no `--strict-slot` (its `--help`: `--serve`, `--port`, `--no-build`, `--slot`,
   `--artefact`); the flag is `assemble_site.py`'s:

   ```
   uv run python scripts/stage_site.py --slot auto --artefact <tar> --strict-slot
   # stage_site.py: error: unrecognized arguments: --strict-slot   exit 2
   uv run python scripts/assemble_site.py --out _stage --slot auto --artefact <tar> --strict-slot
   # first attempt, exit 1 after 5 min 12 s: assemble_site: FAILED: ValueError: Failed to find font DejaVu Sans ... and
   #   fallback to the default font was disabled  (the figure builders; the user's ~/.matplotlib/fontlist-v3.11.0.json,
   #   built 2026-11-11, lists no bundled matplotlib font at all; the worktree's venv ships the 42 DejaVu files)
   MPLCONFIGDIR=<scratch>/mpl uv run python scripts/assemble_site.py --out _stage --slot auto --artefact <tar> --strict-slot
   # exit 0 after 9 min 53 s: assembled site in .../_stage ; assemble_site: slot pin paper-working-20261117 -
   uv run python scripts/stage_site.py --no-build --serve --port 8947
   # (8791 was taken by another python3.9 server on this machine, not this unit's; its pages were served to the
   #  first curl pass and read as an unpinned paper, which is why the port was changed)
   ```

4. The served site (curl, status codes and greps):

   | Path | Status |
   |---|---|
   | `/` | 200; the paper card reads "the argument and the proofs" |
   | `/paper/` | 200, byte-equal to `_stage/paper/index.html` (`cmp`); `hts-paper-banner` twice (the `<template>` and the stylesheet); the installer `id="hts-paper-banner-source"` once; `<p class="hts-paper-banner"><a href="https://doi.org/10.5281/zenodo.123">Working paper · paper-working-20261117 · 2026-11-17 · DOI 10.5281/zenodo.123` |
   | `/paper/supporting-material/` | 200; `hts-paper-banner` twice |
   | `/paper/build/fig-fleet-ternary-8aab...png` | 200 (the `BASE_URL=/paper` build's asset path) |
   | `/docs/theory/` | 200; the citations carry anchors: `../../paper/#def-nlemma`, `#fig-nlemma`, `#sect-results` |
   | `/paper/nothing-here/` | 404 |

   The banner's rendering by the theme's hydration was WP67 G8's browser pass (D-4 item 3); the composer is unchanged
   since (cb0ad18f, b8197b52 are ancestors of c0e210cc), so the static checks above are what this pass adds.

5. The fallback under the strict slot, the first hex digit of `sha256` altered:

   ```
   # exit 1 before any build: assemble_site: FAILED: the paper slot fell back under --strict-slot
   # assemble_site: slot fallback paper-working-20261117 checksum mismatch: paper-html.tar.gz has SHA-256 e0f3668d9ff6...,
   #   mode.toml names f0f3668d9ff6...   and the ::warning annotation
   ```

6. Server stopped (`kill`, exit 0); `git checkout -- paper/mode.toml`; `paper_mode.py check --stage served` reads
   `paper_mode: ok abstract -`; `git status --short` shows only the record's directory.

**What a real pin additionally needs**, none of it exercised here:

- the tag: `paper_pin.py prepare` committed and pushed on `paper` (the branch build runs), then `git tag
  paper-working-<date> && git push origin <tag>` by a person; `paper.yml` then runs `build` with the tag checks
  ("The tag is on paper and the mode file names it") and, after `build`, the `release` job;
- the `paper-release` approval: the environment exists with required reviewers `mzargham` and `jshorish`,
  `prevent_self_review: true` (`gh api repos/DynamicalSystemsGroup/tradespace/environments`), so the `release` job
  waits for one of them, and the tagger cannot approve their own tag; the WP67 G5 and G4 runs never reached it
  (branch pushes skip `release`), and no dry run can reach it without a `paper-*` tag, which this unit may not create;
- the DOI: `paper_pin.py record --tag <tag> --doi 10.5281/zenodo.<n>` needs the release's `paper-html.tar.gz` (it
  downloads it with `gh`) and a minted DOI; Zenodo is off until a first full draft is approved (his word,
  `WP65-design/his-items.md` section 5), so until then `record` has no DOI to write, `check --stage served` fails on
  the empty `doi`, and the composer serves the abstract page in its fallback form; the banner and
  `assemble_site.read_mode` both require the DOI (`_DOI.match`);
- then the merge of `dev` into `paper` and of `paper` into `dev`, and the next release of the software, for the pin
  to reach the site (2.4 step 5).

## 5. What parallel work needs that is not in place

| | Needed | Evidence |
|---|---|---|
| 1 | `dev` pushed. `origin/dev` is three commits behind `paper` (the rename among them); nothing on `origin/dev` has run the software's CI on the renamed tree, and a contributor branching from `origin/dev` starts before the rename | section 0: `git rev-list --count origin/paper..origin/dev` = 0; `git log origin/dev..dev` = 6ba9ad9e, 922520fd, c0e210cc |
| 2 | The paper's checks green on `paper`, or the three tests fixed before the first tag. R-2 of the scope is met in its second form (the failures named with their causes) | section 2; the push run of c0e210cc and the dispatch (section 1) |
| 3 | A place for the paper's test fixes. Two of the three fixes are in `tests/test_paper.py` and the third re-takes `scripts/residuals_baseline.json`: software-side files on the route `paper` → `dev` → `main` (2.1 allows it), which a paper contributor's pull request into `paper` cannot carry under a `paper/`-only ownership line | section 2; the files' paths |
| 4 | A check before a pull request into `paper` merges. `paper.yml` runs on `push` to `paper` and `qc/paper/**`, on `paper-*` tags and on dispatch, not on `pull_request`; the `paper` ruleset has `deletion` and `non_fast_forward` only (no required check, no review rule, no bypass actors), so a contributor's pull request is built only after it lands. The route of G2 says the checks cover build, tests, residuals and keys: today they do so after the merge | `.github/workflows/paper.yml` `on:`; `gh api repos/DynamicalSystemsGroup/tradespace/rulesets/27471877` |
| 5 | The ownership of G3: `.github/CODEOWNERS` has the one line `* @mzargham @danlessa @rororowyourboat`; `jshorish`, a `paper-release` reviewer, is not a code owner, and `paper/` has no line; `CONTRIBUTING.md` has no mention of the paper (`grep -ci paper` = 0); `GOVERNANCE.md` does not exist (WP78); no paper pull request template; `scripts/admissibility.py`'s merge row does not know `paper` | the files; unit B's deliverables D-2, D-3 |
| 6 | Runner time. The paper's tests took 50 min (G4) and 1 h 45 min (G5) per push; every push to `paper` starts a run and `cancel-in-progress` cancels the previous one on the branch; a dispatch on `paper` shares the branch's concurrency group `paper-refs/heads/paper`, so a dispatch while a push run is in progress cancels that run (the reason this unit's dispatch waited for the push run to end; the cancellation itself was not exercised) | `paper.yml` `concurrency`; WP67's durations; the push run's clock in section 1 |
| 7 | Zenodo, for any served pin. `paper_mode.py check --stage served` and `assemble_site.read_mode` both require a DOI outside `abstract` mode, and `paper_pin.py record` takes `--doi` as required; with Zenodo off (his word) a `working` tag can be published as a release but not served: the composer falls back to the abstract page with the reason, and the docs' citations lose their anchors | `scripts/paper_mode.py` `problems` (`required when the site serves a pin`); `scripts/assemble_site.py` `read_mode`; `his-items.md` section 5 |
| 8 | `stage_site.py --strict-slot`, which the scope's R-3 and this unit's brief name: the flag belongs to `assemble_site.py`; and a local review of a hosted `paper-release` artefact (built with `BASE_URL=/tradespace/paper`) cannot be served by `stage_site.py` at `/paper/` without rebuilding, an item WP67 G8 left open | section 4 step 3; WP67 record, G8 second attempt |
| 9 | A documented local environment for the composer. In a fresh worktree the compose failed on the machine's stale matplotlib font cache (`~/.matplotlib/fontlist-v3.11.0.json` of 2026-11-11 lists no bundled font; the figure builders disable the fallback font) until `MPLCONFIGDIR` pointed at a fresh directory; the staging port 8791 was held by a leftover `python3.9` server of an earlier review, which answered the first curl pass with another site | section 4 step 3 and step 4's note |
| 10 | The clean-kernel test's premise on the committed notebooks: the committed outputs were executed on the Mac (the planted digest `c127dd4c`), not in the container of record (`b17d4f8f`), so the notebooks are "host-recorded, re-pin at the gate" without the marker the container README asks for in the commit message; a `working` tag needs no re-pin (2.5), so the first working paper would publish Mac-executed outputs | section 2.2; `paper/container/README.md` ("Units run on the host ... marking each such file") |

In place and confirmed: the `paper-release` environment (required reviewers `mzargham`, `jshorish`,
`prevent_self_review: true`, `can_admins_bypass: false`, deployment policy tags `paper-*` only); the `github-pages`
environment admits `main` only; `release.yml` excludes `qc/paper/**` (`"!qc/paper/**"`), so a push there runs
`paper.yml` alone; the `paper` and `dev` rulesets forbid deletion and force pushes; no tag, release or `qc/*` branch
exists at the start or the end.

## 6. Branches created and deleted

| Branch | Where | Head | Fate |
|---|---|---|---|
| `rehearsal` | the worktree only, from `origin/paper` | this record's commit | kept for the caller; not pushed |
| `qc/paper/touch` | local only, from `origin/paper` | 4aeb87c3 (43ac9334 the sentence, then the merge of `touch-dev`) | deleted (`git branch -D`); never pushed |
| `qc/paper/touch-dev` | local only, from `origin/paper` | 143691bf | deleted; never pushed |

No branch was pushed, so no `qc/paper/**` run was started; the two hosted runs of section 1 are the push that
created `paper` and this unit's dispatch. No tag, release, pull request or issue was created.

## 7. The outward state at the end

`git ls-remote --tags origin` empty; `gh release list` empty; no open issue labelled `release-failure`;
`paper/mode.toml` restored (`abstract`); the worktree's `git status` shows this record and the decisions note only.
`git ls-remote --heads origin 'qc/*'` shows `qc/release` at f305f548, absent at this unit's start and not this
unit's (its name is the software release's dry-run branch); left in place.

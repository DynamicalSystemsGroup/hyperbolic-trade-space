# WP25 — Review report (fourth instance)

| | |
|---|---|
| **Scope of work** | `work-packages/WP25-4-scope-of-work.md` (approved by the driver under the mandate; `WP25-decisions.md`, "Instance 4: the gate": OD1 (a), OD2 (b), OD3 (b)) |
| **Work reviewed** | `dev` from 552fbc9 (WP28 accepted) to the head: 9216154 (T-11, before this report), 037d9cc (T-4), 898f1de (T-1), a4fe8f7 and bf3929d (T-2), ef04524 (the deletion commit), ad1eea9 (the inventory) |
| **Written by** | the instance's executor, 2026-11-11; the checks below ran in its worktree; **a reviewer other than the executor reruns R-1 to R-10 at the head and fills "Checks (D-5)"** |

Rewritten per instance (A3); the third instance's report is at `1d9fae1`.

## Rows (D-4, R-9)

| Row | State | Where, or what the read found |
|---|---|---|
| T-1 (the contract names a deleted file) | fixed, 898f1de | amendment 18 (the scope said 17; WP31's page took 17 at the head): `examples/adcs/adcs_trade_study.ipynb` leaves `[ownership.technical].paths`, `contract_version` 18 in the manifest and the document, a change-control row in section 14. `tests/test_interface_contract.py`: 92 passed. R-5's loop lists only the three the scope allows (`examples/adcs/figures/`, `docs/generated/`, `.github/workflows/release.yml`) |
| T-2 (a record's miscount) | fixed, a4fe8f7 (`WP28-scope-of-work.md` line 33) and bf3929d (`PM-BRIEF.md`, now line 512, not 489) | both read "122 units (corrected by WP25-4; the scope's terms sum to 122, `WP28-inventory.md`)" |
| T-3 (an unpinned sentence in D.12) | routed: the paper stream, one unit. S-10 is decided (the supervisor: "keep and clarify why it matters", `WP28-decisions.md`), so D.12 stays and the unit is unblocked | cell `app-D-cond` of `paper/supporting_material.ipynb` still reads "a small value flags a nearly flat direction, so weakly identified exponents" (line 8141 at the head). Unit: the clause ", so weakly identified exponents" leaves; one register row pins the remaining sentence with C340's backing (L17.5, `test_conditioning_drops_for_nearly_collinear_metrics`); the supervisor's "clarify why it matters" is the same cell's, so one unit. Files: `paper/supporting_material.ipynb`, `claims_register.toml` |
| T-4 (the vocabulary command fails) | fixed, 037d9cc, OD1 (a) | `scripts/check_vocabulary.py`: on the repository (`--root` at its default) the baseline defaults to `scripts/vocabulary_baseline.toml`; `--no-baseline` lists every violation; docstring updated. `tests/test_vocabulary.py` gains `test_the_documented_bare_command_exits_zero_on_the_repository` (bare exits 0, `--no-baseline` exits 1). `CLAUDE.md` stays as written. Bare command: `0 new violation(s), 69 known`, exit 0 |
| T-5 (generated images no page uses) | decided and done, OD2 (b), by hand | removed in the main checkout's git-ignored `docs/generated/figures/`: `ternary-cubesat-{light,dark}.png`, `three-facets-{light,dark}.png`, `chart-holes-{light,dark}.png`, `adcs-coordinates-{light,dark}.png` (8 files; no tracked file outside records names any of the four); 12 files remain, each the output of a figure a page embeds (`adcs-tensions`, `first-fit`, `log-plane`, `tension-report`, `ternary-planted`, `three-terms`). The pattern is ignored already (`.gitignore` line 19, `docs/generated/`), so no tracked change |
| T-6 (the grep misses constant names) | fixed, ad1eea9 | the A2 command gains the hop (A4, one level); at the head it finds no constant-name reader the other greps missed. The inventory is not counted as a reader (it names every row) |
| T-7 (scratch beside WP28's cut list) | decided, ad1eea9 | WP28 is accepted (552fbc9). Its 151 reader-run files (`WP28-inventory/` 122, `WP28-retest/` 29) are held for the next instance (see "What remains"); its 32 review screenshots are keep (A9) |
| T-8 (`release-punch-list.md`) | not here: WP8b's (D-3, R-3) | nothing touched |
| T-9 (files only records cite) | decided, OD3 (b), with one exception | `paper-appendices-sketch.md` and `view-editor-harness.md` deleted (ef04524). **`paper-outline-v1-baseline.md` is not deleted: it has two live readers** the scope's evidence missed: `paper-outline-v2-search.md` line 3 ("Supersedes `paper-outline-v1-baseline.md`, which is kept as the baseline") and `paper-prior-art-sources.md` lines 47 and 79 ("from `paper-outline-v1-baseline.md` (addendum)"), the second read by `paper/prior_art.yaml` and `tests/test_references.py`. Held for the PM. `search-prior-art.md` held for WP12 |
| T-10 (the stage note) | not here: WP8b's (its theme pin) | the executor staged with `--paper placeholder`, which needs no theme |
| T-11 (two orphan PNGs) | fixed, 9216154 | deleted before this instance's other units; the contract grep 0 (inventory) |
| O-8 (Section 9's "+0.99" against D.4's 0.99 threshold) | routed: the paper stream, one unit; not a WP25 row | the paper is a Non-goal of this package. Evidence: Section 9's generated sentence prints "Spearman +0.98 and +0.99" for the two regimes' strongest pair; Appendix D.4's table prints +0.982 / +0.988 (the strongest pair, power margin and energy balance) and says "No pair of traded metrics reaches |Spearman| 0.99". 0.988 rounds to 0.99 at two places, so the page contradicts the appendix by rounding only. Unit: print the sentence's two values at three places (+0.982 and +0.988), as D.4 does; one generated string in the paper's cell, no number changes |

## Deletions (D-2, R-2, R-3, R-4)

Commit ef04524, "WP25: 2 files deleted (fourth instance)": `docs/superpowers/notes/paper-appendices-sketch.md` and
`docs/superpowers/notes/view-editor-harness.md`, each line naming what the file no longer did. R-2: the grep over the
contract, the manifest and `tests/test_interface_contract.py` is 0 by path and by basename for each (the inventory's
section). R-3: the only live hit is `parallel-board.md`, a history row of WP26's round 1 naming the harness note, kept as
history; the rest are records. T-11's two PNGs went in 9216154 (grep 0). The OD3 deletion touched no paper output, so
A10's wait on the container regression did not apply.

## Checks (D-5), at ad1eea9 before this report, by the executor; the reviewer reruns

| Check | Command | Result |
|---|---|---|
| Inventory (R-1) | the A2 command at the head, first column against the Rows table; `grep -ciE "undecided\|tbd\|\?\?" work-packages/WP25-inventory.md` | the diff is empty (466 rows); 0 |
| Vocabulary (R-6) | `uv run python scripts/check_vocabulary.py`; `uv run pytest -q tests/test_vocabulary.py` | `0 new violation(s), 69 known`, exit 0 (the count is 69, not higher); 16 passed |
| Contract (R-5) | `uv run pytest -q tests/test_interface_contract.py`; the existence loop over `[ownership.*]` | 92 passed; missing: the three the scope allows |
| Site, suite, lock (R-7) | `uv run python scripts/stage_site.py --paper placeholder`; `uv run pytest -q -m "not slow" -n auto`; `uv run python scripts/check.py --changed`; `uv lock --check`; `uv run ruff check .`; `uv run ruff format --check .` | `Documentation built in 1.26 seconds`; `1755 passed, 16 skipped, 1 xfailed`; `no changes`; `Resolved 178 packages`; `All checks passed!`; `525 files already formatted` |
| Untouched (R-8) | `git diff --stat 552fbc9..HEAD -- src derivation examples/adcs paper glossary.yaml`; `--diff-filter=R` | empty; empty |
| Attribution (R-10) | `git log --format=%B 552fbc9..HEAD \| grep -ciE "co-authored-by\|generated (with\|by)"` | 0 |
| Watcher verdict per push (R-10) | the CI run of each push | not in hand; the PM or the reviewer reads it |
| Staged pages looked at (R-11) | none: no fix touched a page (OD1 (a) and OD2 (b) touch a script, a test and ignored images) | the reviewer stages and looks, per the scope |

## What remains, and why

- Routed: T-3 and O-8 (the paper stream, one unit each or one together: both are in the paper's cells); T-8 and T-10
  (WP8b).
- Held: WP28's 151 reader-run files (the next instance, as WP11's round 1 raw reports went after triage), WP31's 18,
  WP11's 16, WP29's and WP30's 4, the 3 S-5 candidate files (S-5), `search-prior-art.md` (WP12),
  `streams/P10-review.md` (WP10's acceptance).
- For the PM: `paper-outline-v1-baseline.md` (T-9), the one OD3 file not deleted, because two live notes cite it.

## Recommendation for the driver

Accept D-1 to D-6 of the fourth instance as met, with the exception of T-9's third note recorded above, on the reviewer's
rerun of the checks. The acceptance record is the driver's, quoted verbatim in `WP25-decisions.md`.

## Reviewer's section (D-5, R-11): a reviewer who did not build the instance, 2026-11-11

Reviewed at `dev` 3543f09 in the worktree `wp254review` (checks run there; `uv sync --locked`). Commits landed during the
review and are noted, not reviewed: 61364fc and f7a6532 (the driver's acceptance and the restoration of
`view-editor-harness.md`), 823dc2c (WP28 post-acceptance: T-3 and O-8). Evidence files (screenshots, command output)
are in `/private/tmp/claude-501/-Users-z--claude-spares-spare-4Zb8mW/71474a52-35d3-48fa-82b0-c1328e96b5d6/scratchpad/wp254review/`.

### Requirement table

| ID | Verdict | Evidence (run at 3543f09) |
|---|---|---|
| R-1 | met at 3543f09; **one row short at the head** | The inventory's command block extracted and run: 466 lines; first column against the Rows table (466 rows): diff empty. `grep -ciE "undecided\|tbd\|\?\?"` is 0. Dispositions: 272 keep, 194 hold, 0 delete (as stated). The hop is in the block (`git grep -hE ... = ...$b`). At 823dc2c the diff has one line: `docs/superpowers/notes/view-editor-harness.md` (restored by 61364fc) has no row; the keep-by-decision row is the next instance's, or a one-line fix now (G-1) |
| R-2 | met | For each of the four deleted paths, `git grep -n -F -e <path> -e <basename> -- interface-contract.md interface-contract.toml tests/test_interface_contract.py` returns 0 lines |
| R-3 | met for the three still deleted; **not as a standard for the fourth** | Basename hits for the three: only records (`WP10-*`, `WP25-*`, `WP26-*`, `WP27-*`, `WP28-*`, `PM-BRIEF.md`, `swap-evidence.md`, `parallel-board.md`: history rows). `view-editor-harness.md` was restored because its readers (the editor loops' agents, briefs outside the repository) are invisible to any grep: the check was run and passed, and the file was not dead (G-2) |
| R-4 | met | `git show --stat ef04524`: two files, 497 deletions, the message names each path with "No longer did" |
| R-5 | met | The existence loop over `[ownership.*].paths` of the manifest: missing only `examples/adcs/figures/`, `docs/generated/`, `.github/workflows/release.yml`. `uv run pytest -q tests/test_interface_contract.py`: 92 passed. Amendment 18: manifest (`contract_version = 18`, one list entry removed) and document (`Contract version 18`, the quoted block's `contract_version = 18`, row 18 in section 14) agree; `test_r8_contract_version_matches_document_and_change_log` is in the 92. The removal is a shrink of a pinned list and carries its amendment in the same commit (floor rule) |
| R-6 | met | `uv run python scripts/check_vocabulary.py` (bare): `0 new violation(s), 69 known`, exit 0. `--no-baseline`: 69 `FAIL` lines, `69 new violation(s), 0 known`, exit 1. `--root /tmp` (not the repository) exits 1, so the default applies only to the repository, as the docstring says. `uv run pytest -q tests/test_vocabulary.py`: 16 passed, including `test_the_documented_bare_command_exits_zero_on_the_repository` (asserts bare 0 and `--no-baseline` 1). `CLAUDE.md` line 56 and `vocabulary-review.md` line 47 unchanged and now true |
| R-7 | met | `uv run pytest -q -m "not slow" -n auto`: `1755 passed, 16 skipped, 1 xfailed`; `uv lock --check`: `Resolved 178 packages`; `ruff check .`: all passed; `ruff format --check .`: 525 files formatted; `scripts/check.py --changed`: `no changes`. A fresh worktree has no `docs/generated/`: `build_generated.py` then `mkdocs build --strict` aborts on the missing figures until `scripts/build_figures.py` runs (it printed `built 12 images`); then `mkdocs build --strict`: `Documentation built in 0.93 seconds`. `stage_site.py --paper placeholder`: `staged site in .../_stage`. CI: the dispatched Tests run on 3543f09 (42967854304) was still in progress when I looked; the dispatched runs on its ancestors 7d25ce3, 18c258c, a2a0f14 are success |
| R-8 | met | `git diff --stat 552fbc9..3543f09 -- src derivation examples/adcs/data examples/adcs/model_v2 glossary.yaml paper`: empty; `--diff-filter=R`: empty. Whole diff: 12 files, all within the rows' blast radii (two deleted notes, `check_vocabulary.py`, `test_vocabulary.py`, the two contract files, `PM-BRIEF.md` and `WP28-scope-of-work.md` line edits, the WP25 records). T-11's PNGs went in 9216154 (message "WP28:"), before 552fbc9 and inside the 0ad9153..552fbc9 window: measured from the scope's own base 0ad9153 the paper diff lists WP28's work and T-11, none of it this instance's |
| R-9 | met | Every row T-1..T-11 has a state in the Rows table above; OD1 (a), OD2 (b) and OD3 (b) applied as decided, OD3's third note excepted and disclosed (below). T-3 and O-8 are now fixed by 823dc2c (outside this instance; `weakly identified exponents` left D.12, C441 pins it, Section 9 prints +0.982 and +0.988) |
| R-10 | met for attribution, partly for the watcher | `git log --format=%B 552fbc9..3543f09 \| grep -ciE "co-authored-by\|generated (with\|by)"`: 0. The watcher per push is the dispatched Tests workflow: green at the ancestors named above; 3543f09's run in progress at review time (not a verdict) |
| R-11 | met | This section: commands, output lines and three screenshots (below) |

### Other checks the scope names

- **T-4 change read.** The diff (037d9cc) is the baseline default on the repository only (`root.resolve() == ROOT`), a `--no-baseline` flag, docstring edits and one test: nothing else moved.
- **T-5.** The eight removed images were git-ignored (`git check-ignore -v docs/generated/figures/x.png`: `.gitignore:19`; `git ls-files docs/generated`: 0), so there is no tracked change. In the main checkout 12 files remain. In a fresh worktree `build_figures.py` writes exactly 12, none of the eight removed names; no tracked file outside records names them. The six figures the 12 files belong to are embedded: `adcs-tensions` and `ternary-planted` (examples), `three-terms` (fitting), `tension-report` (tensions), `first-fit` (getting started), `log-plane` (chart).
- **T-6.** Tried on the repository: no row has a constant-name reader the first two greps missed (the inventory states it; 311 rows have no reader by any of the three greps, all records of held or kept packages or spike scripts kept by the decision of 2026-11-10 07:00).

### Staged pages looked at (R-11)

No fix touched a page, as the scope expected. I staged anyway (`stage_site.py --paper placeholder --no-build --serve --port 8765`) and looked, in my own tab, at the three pages that embed the surviving generated images: `/docs/user-guide/tensions/` (the tension heatmap renders, 576x448, both themes' images loaded), `/docs/examples/` (`adcs-tensions` and `ternary-planted` loaded), `/docs/user-guide/fitting/` (`three-terms` loaded): `shot-tensions.jpg`, `shot-examples.jpg`, `shot-fitting.jpg`. The pane was narrow (800 px), so I read each page's image list with `document.images` (every `naturalWidth` > 0, `complete` true) as well. No `??`, no broken image. (One side effect, reverted: `build_figures.py` regenerates `paper/figures/fig-nlemma.png` byte-differently in a fresh checkout.)

### The two open questions and the routings

- **`paper-outline-v1-baseline.md` (two live readers).** The executor is right that the scope's evidence missed them: `paper-outline-v2-search.md` line 3 ("kept as the baseline") and `paper-prior-art-sources.md` lines 47 and 79 (provenance of the contrast and the points of comparison; the second note is the `SOURCES` file of `tests/test_references.py`). Neither is read as a path by a test, so deleting breaks nothing mechanical; it would leave three live provenance citations dangling. Holding it for the PM is sound. The alternative the scope's A1 already provides ("citations of deleted files in kept notes gain the hash of the last version") would let the driver delete it with a three-line edit; that is a ruling, not a gap.
- **WP28's 151 reader-run files held.** Sound: they are verbatim reader records cited by path from the live `WP28-inventory.md`, `WP28-cut-list.md`, `WP28-retest.md`, `WP28-review.md`, and T-7 itself says "WP28's acceptance, then the next instance". 1.0 MB, cited, not cruft yet; the fifth instance decides, with the keep-by-decision rule now recorded.
- **T-3 and O-8.** Sound, and borne out: routed to the paper stream, closed in 823dc2c with a register row (C441) and a test.
- **T-8 and T-10.** Sound as "not here": both are in the scope's non-goals and `WP8b` D-3 and R-3 own the punch list and the theme pin. T-10 matters to a reviewer (a fresh worktree needs the main checkout's `paper/_build/templates`); `--paper placeholder` did not need it, as the executor said.

### Gaps

| ID | Gap | Disposition proposed |
|---|---|---|
| G-1 | The inventory at the head has no row for `docs/superpowers/notes/view-editor-harness.md` (restored by 61364fc after the inventory was written); R-1's diff is one line at 823dc2c | one keep-by-decision row (reader: `WP26-decisions.md`, "Computer-use access and a minimal harness"), or the next instance's inventory |
| G-2 | The deletion was a mistake the checks could not see: R-2 and R-3 passed for `view-editor-harness.md` (0 live greps) and the file was a deliverable of an accepted package whose readers are agents with briefs outside the repository. The driver's acceptance recorded this and the keep-by-decision rule | accept as is: the rule is recorded; the process catches it by a reviewer reading the names, which happened (the driver's) |
| G-3 | `PM-BRIEF.md` line numbers cited by the scope (489, 494-496) had moved (the executor said 512 for T-2); `stage_site`/`build_figures` need the order `build_figures.py` before `mkdocs build --strict` in a fresh worktree, which no document says in one place | observation: accept as is, or one line in the stage note (WP8b's, T-10) |
| G-4 | The executor's report predates the driver's restoration (its "T-9 ... deleted" line and its counts: "2 files deleted", "4 deleted files are gone") and WP25-review's T-9 row now overstate | observation: the driver's decision record is the later word; correct the row at the next touch |

Observation, not a gap: the CI verdict at 3543f09 was not in hand; the ancestor runs are green.

### Recommendation

Recommend acceptance with the listed gaps noted. R-1 to R-11 are met at 3543f09 by my own run (R-1 and the fourth deletion's R-3 as qualified in G-1 and G-2); the executor's pre-report checks reproduce exactly (466 rows, 69 known, 92 passed, 1755 passed, the same missing three contract paths). I do not accept: the acceptance is the driver's, and the driver's record of 00:50 already lies ahead of this review.

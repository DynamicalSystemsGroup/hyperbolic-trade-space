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

# WP25-4 — Scope of work: Repository tidiness, fourth instance (after WP28's cuts; step 3h, recurring)

| | |
|---|---|
| **Status** | DRAFT. Approved only by the recorded act below. Nothing in this package is executed before then. |
| **Supervisor (accountable)** | mzargham |
| **Repository** | `DynamicalSystemsGroup/hyperbolic-trade-space` (local: `/Users/z/Documents/GitHub/posynomial-invariant-form`); work on `dev` |
| **Approval record** | The driver's approval under the mandate (`release-candidate.md`), quoted verbatim in `work-packages/WP25-decisions.md` |
| **Acceptance record** | The driver's acceptance under the mandate, quoted verbatim in `work-packages/WP25-decisions.md`, after `work-packages/WP25-review.md` |

**Header note: the fourth instance of a recurring package, after WP28's executed cuts.** WP26 and WP27 are accepted
(`WP26-decisions.md`, `WP27-decisions.md`, 2026-11-10, 18:20); WP28 has executed X-1 to X-3 and holds X-4 and the S
rows for the supervisor (`WP28-cut-list.md`); contract amendment 16 (2bbdf3b) closed the third instance's gap P-1.
The third instance left 61 hold rows to this one (its acceptance, `WP25-decisions.md`) and one method note: its OD2
sizing missed a reader because `cmp.REPORT` is a constant, not a path. This instance is its own file, as the second
and third were; everything in `WP25-scope-of-work.md`, `WP25-2-scope-of-work.md` and `WP25-3-scope-of-work.md` that
this document does not change still governs. Scoped at `dev` 0ad9153, 2026-11-10.

Sizing at 0ad9153 (the A2 command rerun in a scratch worktree with the package list of A2 below): 670 tracked files,
281 in the live set, **390 rows**. 146 rows are named by nothing in the live set: 122 of WP28's reader-run files
under `WP28-inventory/` and `WP28-retest/` (WP28 is running: hold), 21 of WP26's and WP27's review screenshots, and
the three accepted records `WP26-review.md`, `WP27-review.md`, `WP27-acceptance-review.md` (kept by A1). Every note under `docs/superpowers/notes/` has at least one live reader by
path; four are read only by records (T-9). Every row below was checked in the tree at 0ad9153.

## Purpose

The supervisor, 2026-11-09, 22:20, verbatim (`WP25-decisions.md`, "Origin"): "i appreciate you clean up all the images,
i think we are also starting to accumulate a pretty big documentation cruft/drift/gap i want you to periodically deploy
clean up work packages to address repo tidiness, this is essentially context management. the git history keeps
everything so tidying doesnt eliminate history, history keeping is gits job the repo state itself does not need to
duplicte that effort". `PM-BRIEF.md` "Repository tidiness" makes it one small instance at each gate and adds the
driver's rule of 2026-11-10: deletions check the contract first.

The outcome of this instance: what WP28's cuts and the WP7 notebook's deletion left behind (a contract path to a
deleted file, two tracked figure files no cell writes, generated images no page uses, a record's miscount) is gone or
corrected; a sentence of the supporting material with no register row is pinned or narrowed; the vocabulary tool's
documented command exits as documented; the inventory's grep sees constant names as well as paths.

## Goals

- G1. **Cruft, fourth pass.** The inventory rewritten at the head (the 61 hold rows of the third instance decided or
  re-held with the package they wait for), its command extended to constant names (T-6); delete rows, if any,
  removed in one commit listing each path with what it no longer did; the contract and its test in the grep first.
- G2. **Drift closed.** Rows T-1 to T-5 and T-11 below each end fixed (hash), routed (owner and unit) or decided.
- G3. **What belongs to another package said so.** T-8 and T-10 recorded as WP8b's, with the line that names them,
  not done here.
- G4. **Checked as run.** A reviewer, not the executor, reruns every requirement's check at the head and records the
  output lines and the staged pages looked at in `WP25-review.md`.

## The rows

Blast radius is the set of files the row's fix may touch. "Not here" rows touch nothing.

| Row | Evidence at 0ad9153 | Fix | Blast radius |
|---|---|---|---|
| **T-1.** The contract names a deleted file | `interface-contract.toml` line 335, `[ownership.technical].paths`, lists `examples/adcs/adcs_trade_study.ipynb`, deleted at 4bd6bac (the commit removed its test and its entries in three scripts, not the manifest's ownership entry). Read by `tests/test_interface_contract.py` (`SIDES` from `MAN["ownership"]`: the R-10 tests, globs, disjointness, carve-outs); they check form, not existence, so they pass and the stale path stays. `interface-contract.md` does not name the notebook (R-9's table lists the non-technical sides only). The same section's `examples/adcs/figures/` names a directory that no longer exists; `[case.figures]` pins it with `files = []` (amendment 14), and `test_r4_figure_directory_holds_exactly_the_pinned_files` passes on the empty glob: a deliberate guard against figures returning *(default, A6: kept)*. `.github/workflows/release.yml` and `docs/generated/` are WP8b's planned file and a generated directory, not stale | Contract amendment 17: the notebook's path leaves `[ownership.technical].paths`; a change-control row in `interface-contract.md` section 14 | `work-packages/interface-contract.toml` (one list entry), `work-packages/interface-contract.md` (one change-control row); test run, not edited: `tests/test_interface_contract.py` |
| **T-2.** A record's miscount | `WP28-scope-of-work.md` line 33 says "123 units"; its own terms (14, 27, 10, 7, 40, 14, 8, 1, 1) sum to 122, as `WP28-inventory.md` lines 651-652 record. `PM-BRIEF.md` line 489 repeats "123 units" | Both read "122 units", each with "(corrected by WP25-4; the scope's terms sum to 122, `WP28-inventory.md`)" so the approved scope's change is visible, not silent *(default, A7)* | `work-packages/WP28-scope-of-work.md` line 33; `work-packages/PM-BRIEF.md` line 489 |
| **T-3.** An unpinned sentence in the supporting material | Appendix D.12, cell `app-D-cond` of `paper/supporting_material.ipynb`: "a small value flags a nearly flat direction, so weakly identified exponents". No register row has a fragment from that cell; C340 (`docs/user-guide/termination.md`) carries "A small value marks a nearly flat direction." backed by L17.5 and `test_conditioning_drops_for_nearly_collinear_metrics`, and its note says "The page no longer adds the 'weakly identified exponents' reading". `claims-review.md` line 17: backed, narrowed to what is backed, or dropped | Narrowed and pinned *(default, A8)*: the clause ", so weakly identified exponents" leaves; a register row pins the remaining sentence with C340's backing. **Routed**: the paper is the paper stream's; one paper unit, after WP28's S-10 is decided (S-10 asks the supervisor whether D.12 goes; if it goes, T-3 closes with it) | Paper stream's unit: `paper/supporting_material.ipynb` (cell `app-D-cond`), `claims_register.toml` (one row); this instance records the outcome only |
| **T-4.** The vocabulary tool's documented command fails | `uv run python scripts/check_vocabulary.py` exits 1 ("69 new violation(s), 0 known"); with `--baseline scripts/vocabulary_baseline.toml` it exits 0 ("0 new violation(s), 69 known"). `CLAUDE.md` line 56 and `vocabulary-review.md` line 47 ("report; non-zero exit on a failure") give the bare command; the script's own docstring (line 7) gives the flag | OD1 | (a): `scripts/check_vocabulary.py`, `tests/test_vocabulary.py` if a test pins the exit status without the flag; (b): `CLAUDE.md` line 56, `docs/superpowers/notes/vocabulary-review.md` line 47 |
| **T-5.** Generated images no page uses | `docs/generated/figures/ternary-cubesat-{light,dark}.png` and `three-facets-{light,dark}.png` exist in the main checkout, git-ignored (`.gitignore` line 19), dated 2026-11-09; no tracked file names them (`git grep` over the tree: only `PM-BRIEF.md` line 495 and `WP28-scope-of-work.md`). No script generates them now: `scripts/build_figures.py` writes the figures the pages embed (the `IMAGE` pattern) and never removes a file it did not write, so outputs of figures that left a page stay. WP28's X-1 and X-2 left two more the same way (`chart-holes-*`, `adcs-coordinates-*`, dated before the cuts). A CI checkout never has them; a local stage copies the directory into the site | OD2 | (a): `scripts/build_figures.py` (the output step); (b): nothing tracked; the review records the local `rm` |
| **T-6.** The inventory's grep misses constant names | The third instance's OD2: `tests/test_v2_data.py` read `v1-v2-comparison.md` through `cmp.REPORT` (`compare.py` line 61 at 5a3ee03^: `REPORT = "v1-v2-comparison.md"`), which neither the path grep nor the basename grep sees | The A2 command gains one hop: in each live Python file, an assignment `NAME = ...<basename>...` makes `NAME` a reference, and every live file naming `NAME` (word match) is a reader. Tried at 0ad9153 on `figure1.png`: the hop finds `FIGURE1`, `FIGURE1_NAME`, `BUILT_IMAGES` and the readers `scripts/assemble_site.py`, `tests/test_site.py`. Names built at run time (`f"{cell.id}.png"` in `paper/execute_notebooks.py`) are still invisible to it: the inventory checks such writers by hand and says so (T-11) | `work-packages/WP25-inventory.md` (the command block) |
| **T-7.** Scratch beside WP28's cut list | None. No untracked file in the tree; `WP28-inventory/` (3 + 56 briefs + 56 returns + 7 templates) and `WP28-retest/` (README, 14 briefs, 14 returns) are WP28's verbatim reader records, cited by `WP28-inventory.md` and `WP28-cut-list.md` | Hold rows: WP28's acceptance, then the next instance (as WP11 round 1's raw reports went after triage) | none |
| **T-8.** `release-punch-list.md`'s stale lines | Line 38: "Status: not yet archived; the notebook is pinned by `tests/test_notebook.py` ..." (the notebook and the test went at 4bd6bac); `pyproject.toml` `version = "0.0.1"` against line 43's 0.1.0 item; lines 10-12 and 24-32 list the root and paper pages twice. `WP8b-scope-of-work.md` D-3 and R-3 own the punch list ("no stale line") | **WP8b's, not here** | none |
| **T-9.** Files nothing live cites, or only records cite | Read only by records (each has a path reader, none outside records): `docs/superpowers/notes/paper-appendices-sketch.md` (`WP10-decisions.md`, `WP10-scope-of-work.md`), `paper-outline-v1-baseline.md` (`WP10-decisions.md`), `view-editor-harness.md` (`parallel-board.md`; WP26 accepted), `search-prior-art.md` (`WP12-decisions.md`; held for WP12). Named by nothing live: 21 screenshots under `WP26-review/` (11) and `WP27-review/` (10); `WP26-review.md`, `WP27-review.md`, `WP27-acceptance-review.md` | Candidates listed with this evidence; the screenshots and the three reviews are records of accepted packages (A1; `CLAUDE.md`: reviews put "screenshots in the record") and stay *(default, A9)*; the four notes OD3 | under OD3 (b): the deleted notes, in the deletion commit |
| **T-10.** The stage note | A fresh worktree must copy the main checkout's `paper/_build/templates` (article-theme 1.4.1, fetched at build time, not pinned; `driver-log.md` line 204, `PM-BRIEF.md` line 496) before `scripts/stage_site.py` builds the paper | **WP8b's, not here** (its theme pin); the reviewer of this instance follows the note to stage | none |
| **T-11.** Two tracked figure files no cell writes (found by this scope's grep) | `paper/figures/fig-chart-k3.png`, `paper/figures/fig-predict-check.png`: tracked, last written at 03189c5; `paper/execute_notebooks.py` line 53 writes `{cell.id}.png` for each figure cell, and neither cell id is in `paper.ipynb` or `supporting_material.ipynb` (WP19 removed the cells, `WP19-figure-review.md` line 629); not in `paper/container/RECORD.md`'s hash rows, the contract, a test or a script (grep 0). `PM-BRIEF.md` line 494 lists them as orphans | Deleted in the deletion commit, the contract grep first (R-2). Under OD2 (a), `paper/execute_notebooks.py` also removes a `{cell.id}.png` whose id is in no notebook | the two PNGs; under OD2 (a) `paper/execute_notebooks.py` |

## Non-goals

- The paper's prose and figures beyond T-11's two orphan files (T-3 is the paper stream's unit), `src/`,
  `derivation/`, the data, the model files, any committed number, `glossary.yaml`.
- WP28's surfaces and decisions (the cut list, its S rows, `WP28-inventory/`, `WP28-retest/`); WP11's round-2 reports
  (held for WP11); WP8b's deliverables (the punch list, the changelog, the theme pin: T-8, T-10).
- `docs/superpowers/specs/` (the spec's lines 396 and 436 name the notebook as the design of record of its day) and
  every other package's records except the two lines of T-2.
- Not step 5a, not a judgement of prose or figures; no new script, test or CI step; no archive folder, no renaming.

## Deliverables

| ID | Deliverable | Serves |
|---|---|---|
| D-1 | `work-packages/WP25-inventory.md` rewritten at the head: the A2 command with T-6's hop and the package list of A2; one row per file outside the live set (keep with reader, delete with what it no longer did, hold with package and instance); the section "Contract and tests" with the grep for every delete row | G1 |
| D-2 | One deletion commit if any row deletes (T-11's two files, OD3's notes if (b)): every delete row and nothing else, message "WP25: <n> files deleted (fourth instance)" with one line per path | G1 |
| D-3 | Fixes, one commit per file, each citing its row: T-1 (amendment 17), T-2, T-4 (per OD1), T-5 and T-11's script part (per OD2) | G2 |
| D-4 | `work-packages/WP25-review.md` rewritten: one line per row T-1 to T-11 with its state (fixed and hash, routed with owner and unit, not here with owner, decided); the hold rows carried | G2, G3 |
| D-5 | The reviewer's section of `WP25-review.md`, "Checks": every requirement's command and its output line at the head, and the staged pages looked at | G4 |
| D-6 | `WP25-decisions.md`: the driver's approval and acceptance verbatim, OD1 to OD3's outcomes; one instance line in `WP25-scope-of-work.md`'s header note | all |

## Requirements

| ID | Requirement | Checked by |
|---|---|---|
| R-1 | The inventory has no undecided row and no path outside the live set without a row; its command includes the constant-name hop | rerun D-1's command at the head, diff its first column against the rows (empty); `grep -ciE "undecided\|tbd\|\?\?" work-packages/WP25-inventory.md` returns 0; the command block contains the hop |
| R-2 | **The contract and its test are in the grep before any file goes**: for every delete row, `git grep -n -F -e <path> -e <basename> -- work-packages/interface-contract.md work-packages/interface-contract.toml tests/test_interface_contract.py` is empty, or the amendment retiring the pin is in the same push | D-1's "Contract and tests"; the reviewer reruns it per delete row |
| R-3 | Nothing live references a deleted file by path, basename or constant name | for each deleted path, the D-1 command's three greps over the live set: hits only in records, each listed in D-5 |
| R-4 | The deletions are one commit whose paths equal D-1's delete rows | `git show --stat <hash>`; the message names each path |
| R-5 | The contract names no tracked-file path absent from the tree other than those it marks as planned or generated (`release.yml`, `docs/generated/`) and amendment 14's guard (`examples/adcs/figures/`); the contract's test passes | a short loop over `[ownership.*].paths` testing existence (the scope's sizing used one); `uv run pytest -q tests/test_interface_contract.py` |
| R-6 | The vocabulary tool's command as `CLAUDE.md` gives it exits 0 at the head, and its count is not higher than 69 | run the command exactly as `CLAUDE.md` line 56 states it; `uv run pytest -q tests/test_vocabulary.py` |
| R-7 | The site builds; the fast suite is green apart from failures already on the head, each named; the lock holds | `uv run python scripts/stage_site.py --paper placeholder` (after the stage note, T-10); `uv run pytest -q -m "not slow" -n auto`; `uv run python scripts/check.py --changed`; `uv lock --check` |
| R-8 | Untouched: `src/`, `derivation/`, the data, the model files, `glossary.yaml`, the paper apart from T-11's two files (and, under OD2 (a), `paper/execute_notebooks.py`); no file of a Non-goals surface; nothing renamed | `git diff --stat <start>..HEAD -- src derivation examples/adcs/data examples/adcs/model_v2 glossary.yaml paper` lists only the allowed paths; `--diff-filter=R` empty |
| R-9 | Every row T-1 to T-11 ends fixed, routed with owner and unit, not here with owner, or decided; OD1 to OD3 applied as decided | inspection of D-4 against the rows table |
| R-10 | No attribution line; each push leaves `dev` green at tier 2 | `git log --format=%B <start>..HEAD \| grep -ciE "co-authored-by\|generated (with\|by)"` returns 0; the watcher's verdict per push in D-5 |
| R-11 | The review runs the thing: a reviewer other than the executor reruns R-1 to R-10 at the head, stages the site and looks at the pages a fix touched (none expected under OD1 (b) and OD2 (b); `vocabulary-review.md` is not a page), and records commands, output lines and screenshots | D-5; the PM reads it before the driver's acceptance |

## Sequence

1. The inventory (D-1) with T-6's hop, so T-9 and T-11 rest on the extended grep.
2. The fixes (D-3): T-1 with the test run in the same push; T-2; T-4 and T-5 per OD1 and OD2.
3. The deletion commit (D-2), after its contract grep, in its own push. T-11 deletes tracked paper outputs: it
   regenerates nothing, but lands only when the PM says no container regression is running *(default, A10)*.
4. The review (D-4), then the reviewer's checks (D-5), then D-6. T-3's paper unit is the paper stream's and waits
   for WP28's S-10; the review records whichever state it is in at the time.

## Definition of good

- A tree in which every tracked file has a reader a newcomer can name, by path, basename or constant; the contract
  names only what exists or what it says is planned; every documented command does what its documentation says; a
  fresh PM reads only the present.

## Definition of good enough

- The inventory has no undecided row, its command has the constant hop, and R-2 holds for every delete row (R-1, R-2).
- One deletion commit listing each path, or the review's line that no row deleted; nothing live references a deleted
  file (R-3, R-4).
- Amendment 17 landed with the contract's test green (R-5); the vocabulary command exits 0 as documented (R-6); the
  site builds, the suite and the lock are as at the start or better (R-7); the untouched surfaces untouched (R-8).
- Every row has its end state, OD1 to OD3 applied (R-9); no attribution, `dev` green (R-10); the reviewer's run
  recorded (R-11). Stop there and present.

## Definition of done

Good enough is met, **no open item remains unresolved**, and the supervisor has accepted the work by the acceptance record above.

## Agent's defaults

Approved or changed as one item at the scope gate. Each is marked *(default)* where it appears.

- **A1. Inherited.** The earlier instances' definitions of the live set and of a reference, the message form, "a
  pre-classification is a proposal; the inventory is the decision", "zero deletes is a valid outcome", and
  "citations of deleted files in kept notes gain the hash of the last version" hold unchanged *(default)*.
- **A2. The command's package list.** WP8a, WP8b, WP10, WP11, WP12, WP15, WP16, WP17, WP18, WP19, WP20, WP21, WP22,
  WP25, WP28 (WP26 and WP27 leave, accepted; WP28 joins). The sizing used this list *(default)*.
- **A3. Own file.** `WP25-4-scope-of-work.md`, following `WP25-2-` and `WP25-3-` *(default)*.
- **A4. The hop is one level.** Constant names are followed once (assignment to readers), not transitively *(default)*.
- **A5. The 61 hold rows** of the third instance: WP26's and WP27's rows become keep (records of accepted packages,
  A9); WP11's 16 and `P10-review.md` stay held for their packages; `search-prior-art.md` goes to OD3 *(default)*.
- **A6. Amendment 14's guard stays** (`examples/adcs/figures/` in ownership and `[case.figures]`) *(default)*.
- **A7. A record's arithmetic is corrected visibly** with a parenthesis naming this instance, not silently (T-2) *(default)*.
- **A8. T-3 follows the claims rule as C340 did** (narrow to the backed sentence, pin it with C340's backing) and is
  routed to the paper stream after WP28's S-10 *(default)*.
- **A9. Review screenshots of accepted packages are records** (`CLAUDE.md`, "screenshots in the record") *(default)*.
- **A10. Order** as under "Sequence"; T-11's deletion waits for the PM's word on the container regression *(default)*.

## Open decisions (for the supervisor)

- **OD1.** T-4: the vocabulary tool's bare command exits 1 on the 69 known violations, while `CLAUDE.md` gives it bare
  and `vocabulary-review.md` says it is non-zero "on a failure". What does the documented command check? — options:
  (a) the script's default reads `scripts/vocabulary_baseline.toml`, so the bare command reports only new violations
  (a flag prints the full list) / (b) the script is unchanged and `CLAUDE.md` and `vocabulary-review.md` name the
  `--baseline scripts/vocabulary_baseline.toml` flag.
- **OD2.** T-5 and T-11: no script generates the stale images; they remain because `scripts/build_figures.py` and
  `paper/execute_notebooks.py` never remove an output whose figure left a page or a notebook. What stops them
  returning? — options: (a) each generator removes, in its own output directory, the images it no longer writes; the
  two tracked orphans are deleted / (b) no script change; the two tracked orphans are deleted once, and the git-ignored
  leftovers are removed by hand in the checkout that has them, recorded in the review.
- **OD3.** T-9: four notes are read only by records: `paper-appendices-sketch.md` and `paper-outline-v1-baseline.md`
  (WP10's records; their results are the paper's appendices and the paper's outline), `view-editor-harness.md`
  (`parallel-board.md`; WP26 accepted), `search-prior-art.md` (WP12's decisions; WP12 not accepted). Keep or delete?
  — options: (a) keep, each row naming the record that cites it / (b) delete the three whose package is decided
  (the first three), the citing records keeping the name as history, `search-prior-art.md` held for WP12.

The driver decides OD1 to OD3 under the mandate; the rest is the Agent's defaults as one item.

## Gate outcomes

- None yet.

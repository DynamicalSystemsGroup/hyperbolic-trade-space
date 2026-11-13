# WP26 — Review report

Screenshots for this record: commit `2a669de`, `git show 2a669de:<path>` with `<path>` under `work-packages/WP26-review/`, `work-packages/WP26-view-editor-feedback/`.

| | |
|---|---|
| **Scope of work** | `work-packages/WP26-scope-of-work.md` (74b2402; gate outcomes added in 9a77d5c) |
| **Scope approval verified** | `WP26-decisions.md`, "Scope approved; OD1 (2026-11-10, 12:40; the driver)": approved for execution by the driver under the mandate, OD1 (b), the Agent's defaults as one item; OD1 (b) amended 15:05 (f504c44). The supervisor's origin, verbatim, in the same file (11:20). |
| **Work reviewed** | `dev` from `<start>` cc0e1c9 to 46cd9a2 (the `origin/dev` head at the review); WP26's own commits: 74b2402, 9a77d5c, 258b197, d793a95, 2ce3c14, 907c135, 2d693fe, f504c44, ad9df4b, 50df9ac, 05fbd3c |
| **Supervisor (accepts)** | mzargham |
| **Acceptance record** | The supervisor's verbal acceptance, quoted verbatim in `WP26-decisions.md` |

The reviewer did not build the work. Every check below was run in a fresh worktree at 46cd9a2 (`uv sync --locked`),
and the editor was read in the reviewer's own browser tab (tab-29, created and closed for this review; the modeller's
tab-23 untouched), read-only: the recovery restored, the Issues panel, the seven views, the requirements table and the
traceability matrix. The screenshots this report cites are in `work-packages/WP26-review/`.

## Deliverables

| ID | Verdict | Evidence |
|---|---|---|
| D-1 (a) `views.sysml` | met | `examples/adcs/model_v2/views.sysml` (d793a95; 112 lines at the head, the seventh view `stakeholders` added by WP27). Package `CubesatViews`, six views of the round by `expose` and `filter` on the model's own elements, each `doc` naming its intent (R-5). Parse test `tests/test_system_model_v2.py::test_views_file_loads_with_the_model_and_every_exposed_name_resolves` passes (`REQUIRE_OPENSYSML=1`; 1 passed). Rendered in the reviewer's tab: every view draws a diagram, none "Rendering unavailable" (R-4). |
| D-1 (b) the changes list | met | `work-packages/WP26-model-changes.md` (2ce3c14, 05fbd3c; 200 lines): 17 findings, each with its intent (I1 to I4, quoted), its class by the scope's own definition and its evidence: landed 8, held 1 (N4), gate 5 (N5, N6, T3, T4, T5), observations 3; the held and gate entries listed for the driver with diffs or sketches. |
| D-1 (c) the in-file changes | met | N1, N2, N3 (and WP23's O-1) in `cubesat.sysml` at ad9df4b, the ledger's five entries at 50df9ac. `git diff --stat cc0e1c9..HEAD -- examples/adcs/model_v2/cubesat.sysml`: 20 insertions, 19 deletions, four hunks: the header's three lines (N3), section 5's doc restated (N1), `SlewVerification`'s line rewrapped (N2), `pointingErrorLimit`'s doc "94.9 %" to "95.0 %" (O-1). The five `@8` entries (`scope-sensitivity-shared-subspace-v2@7`) each carry `model_sha256 65ecd7a7e731…`, the note "regenerated in the container of record hts-paper (image 877c42cc10e3)", `git_dirty` False, and an `output_sha256` equal to the `@7` entry's: a43ccc557bc6, 10ae79a224b5, 6b65b2843a99, 5b47f53b4d7b, d16ae3648c40 (read from `ledger.jsonl`). No name the generator reads changed; the committed views are the generator's output (`test_committed_views_are_the_generators_output_on_the_model`: 1 passed). The three commits ad9df4b, 50df9ac, 05fbd3c carry one committer time (20:10 UTC): pushed as one unit. |
| D-2 the feedback report | met | `work-packages/WP26-view-editor-feedback.md` (2d693fe, extended by WP27's units; 348 lines): Context with the loading recipe; 1 What worked well (8 items); 2 What did not work well (11, each with what was tried); 3 Bugs 1 to 6; 4 Workarounds (9 rows); 5 Suggestions (10); 6 the second session (bugs 7 to 10, feature requests F-1 to F-5); 7 a cold reader's first use. 31 screenshots cited, 31 in `WP26-view-editor-feedback/`, none missing, none uncited (checked by script). |
| D-3 the step log | met | `scratchpad/view-editor/wp26/steps.md`: 22 numbered steps with time (UTC), action, revision, issues count, screenshot and expected-vs-observed; the M0 to M4 rows; 22 `.jpg` files beside it (R-10). |
| D-4 the decision records | met, with one gap (G-1) | `work-packages/WP26-decisions.md`: the origin (verbatim), the scope gate with OD1 (b), the computer-use grant and the harness deliverable (verbatim), the ledger sequencing, OD1 (b) amended. The milestone calls (M0 to M4) are in the step log, not in this file; no gate-class change landed, so no driver's go was needed; the supervisor's acceptance is pending (this review's gate). |

The harness note the supervisor added on 13:10 (`WP26-decisions.md`) exists: `docs/superpowers/notes/view-editor-harness.md`
(2ce3c14, 0869ecf; 126 lines, sections 1 to 8); its snippets of §3 to §5 were used for this review's readings and worked
as written.

## Requirements

| ID | Verdict | Evidence |
|---|---|---|
| R-1 | met | `PYTHONPATH=examples/adcs uv run python -m experiments verify` at 46cd9a2: "49 entries (11 current); 0 drifts". |
| R-2 | met | `REQUIRE_OPENSYSML=1 uv run pytest -q` on the six listed files plus `tests/test_verification_pointers.py`: 228 passed in 136 s. |
| R-3 | met | `uv run python examples/adcs/model_v2/coverage.py --out <tmp>`; `diff` against `views/coverage.md` and `coverage.csv`: identical. Against `<start>`, `coverage.md` differs in its two model-hash lines (13c10e1c5ef5 to 65ecd7a7e731; OD1 (b)) and in the swaps' names (WheelClass/TrackerGrade to wheelClass/grade), the latter WP25-3's 6c8481a, not WP26's. The committed-views test passes. |
| R-4 | met | The reviewer's own pass (tab-29, 1600 x 1000): after "Restore recovery" the source pane held 75,542 characters, sha256 afeaebf9b100, equal to `cubesat.sysml` + `stakeholders.sysml` + `views.sysml` at the head joined by newlines; "Issues (0)", "No issues in the current applied model", "Source applied", no red banner (`01-restored-issues-0.jpg`). Each view, node and edge counts read from the canvas (harness §4): `assembly` 24 nodes, 4 binding edges (panelSpan to both panel spans, batteryCapacity to the battery, momentumCapacity to the wheel) (`02-…`); `alternatives` 12 / 8 (`03-…`); `configurations` 19 / 16, each configuration with what it redefines (`04-…`); `metrics` 32 / 0 (29 calc defs, 2 verification defs, the analysis def) (`05-…`); `requirements` 41 / 81 (11 typed-by, 41 satisfy, 6 not satisfy, 23 verify; the six negated: the baseline's pointing error, and the concerns' verdicts WP27 added) (`06-…`); `metricCarriers` 13 / 9 (`07-…`); `stakeholders` 54 / 26 (`08-…`). None "Rendering unavailable". Requirements table: 34 requirements = 11 defs + 11 baseline usages + 12 concern-held usages, every requirement of the two model files (`09-…`). Traceability matrix, Satisfaction: 34 rows x 3 linked elements (cubesatAgile, cubesatBaseline, cubesatCompact), 41 "Declared", 6 "Negated declaration" (`10-…`); Verification: 34 x 4 (configurationEvidence, slewEvidence, ConfigurationVerification, SlewVerification), 23 "Declared" (`11-…`). The model files hold 41 `satisfy`, 6 `not satisfy`, 23 `verify` (grep): one for one. The parse test (above) is the toolkit's half of the check. |
| R-5 | met | Each view's `doc` quotes WP22 or WP23 (the stakeholder view WP27); each changes-list entry names I1 to I4, quoted at the list's head. `uv run python scripts/check_vocabulary.py`: "69 new violation(s), 0 known", exit 0: the base, none added by WP26's files. |
| R-6 | met | Under OD1 (b) as amended the model diff is not empty by design; its four hunks are N1 to N3 and O-1 (D-1 (c)), each byte-identical in outputs by the `@8` hashes. No gate-class entry landed: N5, N6, T3, T4, T5 are listed unlanded with sketches; T3 later landed under WP27's own scope (its decisions), not here. `git log cc0e1c9..HEAD` read against the list: every landed entry has a commit; every landed unit has R-1 to R-3 green at the head. |
| R-7 | met | Followed cold on the screenshots alone: Bug 3 (`no-add-file.jpg`: the Explorer's menu open over "Files: model.sysml" with "Narrow Explorer" and "Widen Explorer" only; `cold-explorer-menu.jpg` the same at 1600 px) and Bug 5 (`inherited-parts-missing.jpg`: `assembly` on `cubesatBaseline`, three nodes, the usage with `wheel : MediumWheel` and `tracker : MediumTracker` only; `cold-inherited-parts.jpg`: `sat1` with `a`, `b`, no `c`). Each bug has numbered steps from `/app`, expected, observed, a screenshot and a "Reproduced" line. Bug 10 reproduced itself during this review: in the reviewer's read-only tab the header showed "Recovery could not be saved. Your current project is unchanged. Another tab changed local recovery." (`07-…bug10-banner.jpg`), the other tab being the modeller's; nothing was retried or discarded. |
| R-8 | met | The scope's grep on `WP26-view-editor-feedback.md` finds nothing. |
| R-9 | met | Read: section 2's eleven items each name what was tried and point to the bug, workaround or suggestion; each bug ends in a suggestion; the opening thanks the author; the closing note separates what was not the editor's doing. |
| R-10 | met | 22 numbered steps, 22 `.jpg` files. Each row carries the revision and the issues count; step 05's issues read "?" (the apply was lost to a navigation of the tab, stated in the row) and step 06's "-" (the landing page before the restore). |
| R-11 | met | Step 03 names the source of the model text (the repository's public raw URL at b9d8b80, 51,612 characters); step 07 the `view` package (56,092 characters together); steps 17, 19, 21 edits to the views part in the page; the final text checked equal to the two committed files (56,550 characters, sha256 a4ff88cc447f). No account: the editor's landing page offers none (seen in this review). |
| R-12 | met | The scope's attribution grep over `git log cc0e1c9..HEAD --format=%B`: two lines, both the phrase "regenerated by" in the bodies of 6c8481a (WP25-3) and ca6ce94 (case-model), not attribution; WP26's commits carry none. Blast radius: see Outside the scope. |
| R-13 | met | The modeller: 17:54:19 UTC (step 01) to 18:13:41 (M4, units pushed), the round's end 19:09:04: under two hours of editor work. The researcher: notes started 17:53 UTC, the report committed 19:12 UTC (2d693fe): under two hours. The sequel (19:47 to 20:10 UTC) and the cold passes (21:05 to 21:10 UTC) were later units on the driver's word, outside the round's box and so stated in the step logs. |

## Definition of good enough

| Item | Verdict | Evidence |
|---|---|---|
| D-1 (a) pushed, R-4 on screenshots, R-1 to R-3 at its commit | met | d793a95 on `dev`; R-4 by this review's own pass and the step log's; R-1 to R-3 green at the head (above). |
| The changes list with every finding classed and its intent; landed entries pass R-6; held and gate listed | met | 17 findings classed, each with an intent; by the tables: landed 8 (C1, C2, N1 to N3, T1, T2, A1), held 1 (N4), gate 5 (N5, N6, T3, T4, T5), observations 3 (C3, T6, A2); the list's own counts line says gate 6 and observations 4 (G-5). The held and gate entries carry a diff or a sketch for the driver. |
| D-2 pushed with the four sections and each bug meeting R-7; R-8, R-9 | met | 2d693fe and WP27's extensions; sections 1 to 5 plus 6 and 7; ten bugs each with steps, expected, observed, screenshot, reproduction line. |
| The step log meets R-10 and R-11; R-13 kept or stated | met | Above. |
| R-12 | met | Above. |

## Outside the scope

`git diff --stat cc0e1c9..HEAD` is 139 files; the range carries WP27, WP25-3, WP11's round 2, the close-out's
container regression and the paper's units. Read against WP26's own commits only:

- **Out-of-scope changes:**
  - ad9df4b carries WP23's O-1 (`pointingErrorLimit`'s doc, "94.9 %" to "95.0 %") in a WP26 commit; the changes list's
    prose says so, but its embedded diff block omits that hunk (G-2).
  - 50df9ac changes two lines of `examples/adcs/model_v2/stakeholders.sysml` (WP27's file: its evidence pointers move
    to `v2-primary@8`); 05fbd3c changes `paper/supporting_material.ipynb` (the outputs of `tab-C-datasets`, the entry
    ids `@7` to `@8`; "host-recorded, re-pin at the gate") and `work-packages/WP27-review.md`. All three are
    consequences of the new ledger entries, outside WP26's blast radius (G-3).
- **Non-goals touched:**
  - "No docs page (`docs/`…)": `docs/superpowers/notes/view-editor-harness.md` added; the supervisor's 13:10 amendment
    made it a deliverable (recorded in `WP26-decisions.md`), though the scope's deliverables table was not amended (G-4).
  - "No change to … any output … without the data gate": the five ledger entries and `coverage.md`'s hash lines, under
    OD1 (b) as amended, with every output hash equal; the notebook's datasets table moved with the entry ids (G-3).
  - The UX researcher wrote no model change and did not drive the pane: held (2d693fe touches its two paths only).
    No account, no sign-in: held. Nothing under `src/`, `derivation/`, `examples/adcs/data/`: held
    (`examples/adcs/experiments/ledger/ledger.jsonl` appended under OD1 (b) only).

## Observations (not counted as failures)

- The changes list's "as rendered" table is a record of the round: at the head the `requirements` view draws 41 nodes
  and 81 edges, not 25 and 33, because WP27's concern requirements and their 36 verdicts enter as related context; the
  other five views' counts are unchanged (G-5).
- `views.sysml`'s `alternatives` doc names the swaps "WheelClass, TrackerGrade" (the enumerations) where the coverage
  table, since WP25-3 OD3 (b), names them by their selecting attributes `wheelClass` and `grade` as the assembly view
  tags them; one object, one name would pick one (G-5).
- The editor's revision counter restarted at 1 on the reviewer's restore (feedback report, Bug 2's cold pass, confirmed).
- The requirements table's Identifier column is "—" for all 34 rows and Documentation "—" for the 23 usages (N6, gate
  class, listed for the driver).
- The scope's D-4 names "the milestone calls" among the decision records; the step log is where they are (G-1).

## Open decisions (for the supervisor)

Each gap below is put through the decision loop by the driver; none is resolved here.

- **G-1.** D-4: the milestone calls M0 to M4 are recorded in the step log, not in `WP26-decisions.md` — options:
  accept as is / fix before acceptance / follow-up work package
- **G-2.** WP23's O-1 landed inside WP26's commit ad9df4b, and the changes list's diff block omits its hunk while the
  prose names it — options: accept as is / fix before acceptance / follow-up work package
- **G-3.** Three files outside the blast radius changed in WP26's commits as consequences of the `@8` entries
  (`stakeholders.sysml`, `paper/supporting_material.ipynb`, `WP27-review.md`) — options: accept as is / fix before
  acceptance / follow-up work package
- **G-4.** The harness note is a deliverable by the decision record, under `docs/`, which the scope's non-goals name;
  the scope's deliverables table was not amended — options: accept as is / fix before acceptance / follow-up work package
- **G-5.** Three record observations in the changes list and the views file: the `requirements` view's counts are the
  round's, not the head's; the counts line says gate 6 and observations 4 where the tables hold 5 and 3; the
  `alternatives` doc's swap names differ from the coverage table's — options: accept as is / fix before acceptance /
  follow-up work package

## Gap dispositions

| Gap | Disposition (accept as is / fix before acceptance / follow-up work package) | Reason or follow-up |
|---|---|---|
| G-1 | | |
| G-2 | | |
| G-3 | | |
| G-4 | | |
| G-5 | | |

## Recommendation

Recommend acceptance with the listed gaps noted, because: every deliverable exists at its path and serves its goal;
all thirteen requirements are met on evidence this review produced (0 drifts, 228 model tests, the coverage table
regenerated identical, the parse test, the greps); the editor, read in a fresh tab at the head, shows the model applied
at 0 issues with all seven views rendering and node and edge counts equal to the changes list's where WP27 did not add
to them, the requirements table listing every requirement of the two model files, and the traceability matrix
agreeing with the model's 41 `satisfy`, 6 `not satisfy` and 23 `verify` statements one for one; the in-file edits
landed under the amended OD1 (b) with every output hash equal to the container's `@7`; and the five gaps are
record-keeping and out-of-scope riders, none of which touches an output or a test.

Acceptance is the supervisor's act, recorded as named above. This report does not accept the work.

# WP27 — Review report (acceptance)

Screenshots for this record: commit `2a669de`, `git show 2a669de:<path>` with `<path>` under `work-packages/WP27-review/`.

| | |
|---|---|
| **Scope of work** | `work-packages/WP27-scope-of-work.md` |
| **Scope approval verified** | `WP27-decisions.md`, "Scope approved (2026-11-10, 14:20; the driver)", under the mandate; `<start>` = 1cf319a (the commit that records it) |
| **Work reviewed** | `dev` from 1cf319a to 46cd9a2 (the `origin/dev` head at review time; the last WP27 commit is 3cce6cd, the two after it are the driver's records). WP27's commits: 28f7c9c, a4cde2f, 7509978, 331c9e4, fbee839, f840bf3, b9c8819, a50db5d, 85ae173, d5d0c3d, 73b4e89, bcf81b0, 3cce6cd; the WP26 sequel's 05fbd3c carries WP27's record edits |
| **Supervisor (accepts)** | mzargham |
| **Acceptance record** | The supervisor's verbal acceptance, quoted verbatim in `WP27-decisions.md` |

A fresh-context reviewer who did not build the work. Everything below was run in a worktree at the head
(`uv sync --locked`) or read in the view editor in a tab of the reviewer's own (read only; restored the "cubesat"
recovery, applied nothing, closed the tab). The reviewer's screenshots are `WP27-review/accept-*.jpg`. The modeller's
record is `WP27-review.md`; this report checks it item by item and does not repeat it.

## Deliverables

| ID | Verdict | Evidence |
|---|---|---|
| D-1 | met | `WP27-review.md` §D-1: 18 constructs, each with the strict-load result, the editor's issues count and rendering, and the choice; the two parser disagreements (rows 10, 13) and the cross-file conclusion stated. The chosen constructs are the ones in `stakeholders.sysml` (read). Rows marked "not tried" in the editor (5, 9, 16) are unused |
| D-2 | met | `examples/adcs/model_v2/stakeholders.sysml` (two stakeholders, two concern defs, four concerns holding the eleven requirement defs' usages, 36 verdict statements, the roll-ups marked illustrative, two evidence cases with four pointers each); `views.sysml` gains `stakeholders`; the changes list classes L-1 to L-8, H-1 to H-3, G-1 to G-3 with commits. Nothing of WP27 is in `cubesat.sysml` (R-5). Tests: R-1, R-2, R-6, R-7 below |
| D-3 | met | The editor at the restored recovery: 75,542 characters, sha256 `afeaebf9b100` (equal to the review's and to the three files on disk), Issues (0), "No issues in the current applied model" (`accept-restored-issues.jpg`); the `stakeholders` view 54 nodes, 26 edges, `unavailable` false, node texts equal to the review's list (`accept-stakeholders-view.jpg`); the Requirements table searched for `CubesatStakeholders`: 12 rows, each with its declared satisfaction by the three configurations (negated where the engine negates) and its evidence case (`accept-requirements-table.jpg`); the Traceability matrix, Satisfaction: "12 requirements · 3 linked elements", per column Declared / Negated declaration agile 9 / 3, baseline 11 / 1, compact 11 / 1, no blank cell (`accept-matrix-satisfaction.jpg`); Verification: "12 requirements · 2 linked elements", configurationEvidence 3, slewEvidence 9 (`accept-matrix-verification.jpg`). One cited screenshot is not in the folder: G-1 |
| D-4 | met | The prompt and the return in `WP27-review.md` §D-4 are byte-identical to `scratchpad/view-editor/wp27/d4-return.md` (prompt 3,010 characters, return 13,178; compared by script). Eight dispositions cover (a) to (g); each point the reader could not follow is changed (b9c8819, 73b4e89), held with its reason, with the supervisor (H-2), with the driver (the life-against-slew trade, G-1 of the review) or with the researcher. The non-goal's record on WP26's gate-class findings is absent: G-2 |
| D-5 | met | "none" with its reason (§D-5): the reader's needs that prose could serve are already in `docs/examples.md` ("Requirements read after the fit") and now in the model and the matrix; a pointer sentence would not have reached a reader who read the editor. `examples/adcs/case-model.md` and `docs/examples.md` untouched by WP27 (the range's edits to `case-model.md` are 2f1c2d9 and ca6ce94, other streams) |
| D-6 | met, with G-3 | `WP26-view-editor-feedback.md` §6: Bugs 7 to 10 (steps, expected, observed, screenshot, cold-pass result) and F-1 to F-5. Every screenshot the section names exists in `WP26-view-editor-feedback/` (11 checked). F-5 has no numbered steps, no expected/observed and no screenshot of its own (G-3) |
| D-7 | met | `WP27-review.md` has D-1, the classed changes, D-3, D-4, the tensions-to-concerns table, the checks, "For the lifecycle demo" (notes only; nothing in the diff builds any of its four items) |
| D-8 | met so far | `WP27-decisions.md`: Origin, the scope gate (14:20), the driver's go for the verdict unit (16:20). The supervisor's acceptance is the act this report waits for |

## Requirements

| ID | Verdict | Evidence |
|---|---|---|
| R-1 | met | `REQUIRE_OPENSYSML=1 uv run pytest -q tests/test_system_model_v2.py tests/test_verification_pointers.py`: 31 passed. `test_stakeholders_file_loads_strictly_and_its_names_resolve` loads the three files strictly and finds each stakeholder, concern, evidence case, roll-up and the view; negative control: `launchBudgt` raises `ModelError` matching the misspelt name (read) |
| R-2 | met | `test_the_trace_from_who_cares_to_every_requirement_is_complete` (read, passed): four concerns, each bound to `sponsor` or `operator` (both typed), each with requirements; the served requirement defs equal the model's eleven `RequirementDefinition`s (so every traded metric's requirement reaches a concern); every held requirement is verified by an evidence case |
| R-3 | met | The reviewer's own readings (D-3 row): Issues (0), the view renders (54 / 26, `unavailable` false), the matrix populated in both relationships |
| R-4 | met | `PYTHONPATH=examples/adcs uv run python -m experiments verify`: "49 entries (11 current); 0 drifts". `REQUIRE_OPENSYSML=1 uv run pytest -q` on the six listed files plus the pointer test: 31 + 197 = 228 passed. `REQUIRE_OPENSYSML=1 PYTHONPATH=examples/adcs uv run python examples/adcs/model_v2/coverage.py` rewrote `views/coverage.md` and `coverage.csv`; `git status` and `git diff --stat -- examples/adcs/model_v2/views/` show no change. The committed views: `test_model_coverage.py` passed |
| R-5 | met | `git log 1cf319a..HEAD -- examples/adcs/model_v2/cubesat.sysml` lists one commit, ad9df4b ("WP26 held edits and WP23 O-1"), the WP26 sequel under the amended OD1 (b) (`WP26-decisions.md`, 15:05): the ledger's `@8` entries (and `scope-sensitivity-shared-subspace-v2@7`) have `output_sha256` equal to their `@7` predecessors for all five, `model_sha256` 13c10e1c → 65ecd7a7, commit 3ffd8d5, `git_dirty` false, platform the container's (`Linux-…-aarch64`). `ledger_gate.py` carries the `--wp26` note; no WP27 note is needed because nothing of WP27 is in-file |
| R-6 | met | `tests/test_verification_pointers.py` passed (4 tests; negative controls: `v2-primary@999`, the superseded `@5`, an unknown heading, an unknown image). By hand: `v2-primary@8` is the current `v2-primary` entry (ledger read); `## Container regression at the WP23 close-out gate (2026-11-10, image 877c42cc10e3, head 61cef31)` is line 447 of `paper/container/RECORD.md`; `877c42cc10e3` appears there as the `hts-paper` image of record; `uv run pytest --collect-only -q` collects both named nodes (2 collected) |
| R-7 | met | `grep -rnwE "CostToBuild\|EffectiveLife\|UnitCosts\|BatteryLife\|unitCosts\|batteryLife"` over `examples/adcs/*.py`, `model_v2/coverage.py`, `spike-sysml-diagrams/project.py`, `examples/adcs/data/`, `interface-contract.toml`: no match (exit 1). Both `calc def` docs begin "Illustrative roll-up" and name their inputs (read); `test_the_rollups_are_illustrative_and_read_by_no_output` passed |
| R-8 | met | The prompt is quoted and the return is verbatim (byte-identical to `d4-return.md`); the prompt gives the reader the image first, no repository access and its own tab; the return's first line confirms the order. A disposition per point (eight rows) |
| R-9 | met | D-5 "none" with its reason; `uv run pytest -q tests/test_case_model_howto.py tests/test_docs.py`: 61 passed |
| R-10 | not met for F-5 | Bugs 7 to 10 and F-1 to F-4 each have numbered steps (steps 1 to 3 the loading recipe, which starts at `/app`), expected, observed and a screenshot that exists. F-5 has none of the three (G-3). WP26 R-8's `grep -nE "WP[0-9]\|driver\|\bPM\b\|supervisor\|ledger\|work-packages\|Claude\|agent"` over the report: 0 matches |
| R-11 | met | `uv run python scripts/check_vocabulary.py` at the head: "69 new violation(s), 0 known"; at 1cf319a (a detached worktree, same environment): 69. No new violation |
| R-12 | met, with observations | Blast radius: WP27's commits touch `stakeholders.sysml`, `views.sysml`, `tests/test_system_model_v2.py`, `tests/test_verification_pointers.py`, `WP27-review.md` and its folder, `WP26-view-editor-feedback.md` and its folder, `WP27-decisions.md`. Outside the list: 0869ecf (the harness note's §8) and 05fbd3c (see Outside the scope). "For the lifecycle demo" lists four items; the diff builds none (no typed pointers, no stages, no third stakeholder, no calibration). Attribution: the CI's pattern (`.github/workflows/test.yml`, the "No AI attribution lines" step) over `git log 1cf319a..HEAD --format=%B`: 0 hits; the scope's literal pattern hits "regenerated by" in two commits of other streams (6c8481a, ca6ce94), not attribution; no WP27 file carries an attribution line |

## Definition of good enough

| Item | Verdict | Evidence |
|---|---|---|
| D-1 recorded; D-2's landed units pass R-1, R-2, R-4, R-6, R-7; every in-file change landed under R-5 or listed held or gate | met | Above; H-1 (the in-file `frame`) is listed held with its reason; no in-file WP27 change |
| 0 issues; the stakeholder view and the traceability matrix in D-3 (R-3) | met | Above |
| The P1 reader goes from "who cares" to the metrics and says what they learned; the return recorded with dispositions; no point left unanswered | met | The return's (b) and (c) name each concern's requirements and where they were found, (d) says what is and is not trusted; every (e) to (g) point has a disposition |
| The tensions-to-concerns table in the review | met | Ten rows. Checked against `examples/adcs/case-model.md` ("The K = 1 contending set is a 5-lemma in both regimes"): primary total mass (0.358), energy balance, pointing error, depth of discharge, settling time; baseline control effort (0.432), settling time, power margin, pointing error, depth of discharge: equal. Each metric's requirement and concern follow `stakeholders.sysml` (total mass through the launch budget → lowCost; depth of discharge → longLife and powerAndEnergy) |
| D-5 by R-9; D-6 meets R-10; "For the lifecycle demo"; R-11 and R-12 | met except R-10 for F-5 | Above |

The verdicts (b9c8819, 73b4e89), run by the reviewer: the three files loaded strictly, `verify_satisfaction()` returns 47
verdicts, 47 hold, engine "run" for all, 12 per named configuration, 6 negated (the model's `baselinePointingError`; the
concerns' pointing error for baseline and compact; the agile launch budget, control effort and peak slew power), equal to
the matrix's cells. The negative controls (a negated verdict stated as satisfied is false; the agile control effort holds
once bound to the baseline's measurement) are in the tests, read and passed.

## Outside the scope

- **Out-of-scope changes:** 0869ecf, `docs/superpowers/notes/view-editor-harness.md` §8 ("What the second round
  taught"): WP26's deliverable, not in WP27's blast radius, edited by WP27's round (G-4). 05fbd3c, the WP26 sequel's
  commit, changes `paper/supporting_material.ipynb` (the dataset table's printed entry ids, `@7` to `@8`) under WP26's
  rule and in the same commit edits `WP27-review.md` (L-3, H-3, G-2, G-3): a WP26 unit carrying WP27's record, not WP27
  work under `paper/` (G-4).
- **Non-goals touched:** none. The paper is unchanged by WP27's own commits; no roll-up is read by any output (R-7);
  the data of record and every output are unchanged (0 drifts); nothing for the lifecycle demo is built; the editor's
  code untouched; no account; `glossary.yaml`, `claims_register.toml`, `interface-contract.*`, `src/`, `derivation/`
  untouched by WP27's commits. The non-goal on WP26's gate-class findings asks D-4 to record whether any of T3, T5, N5,
  N6 blocks the sponsor's reading; that record is not in the review (G-2).

## Observations (not counted as failures)

- The review cites its screenshots by step number ("step 24", "steps 23 to 25") and names the folder once; the
  folder holds steps 01 to 09, 11, 23 and 25. Step 24's screenshot (the Satisfaction matrix read as data, cited in
  D-1 row 18, L-8 and D-3) is in the session scratchpad only (G-1). Steps 10 and 12 to 22 are not cited by the review
  (12 to 21 are the feedback report's cold passes, copied there under their own names).
- Section 7 of the feedback report (the cold reader's observations, sent from D-4's dispositions) says no screenshots
  were kept; those items are observations, not feature requests, so R-10 does not reach them.
- `recordEntry` names the close-out gate's RECORD.md section (image `877c42cc10e3`, head 61cef31) while the current
  entry `v2-primary@8` was produced by the WP26 container re-run at head 3ffd8d5, which has no RECORD.md section; the
  review's G-3 settles it as the record of the image the entries were run in. R-6 as written is met.
- The scope's R-12 pattern (`generated by`) matches ordinary prose ("regenerated by the generator"); the CI's pattern
  is the one that binds and is clean. The review's quoted prompt names the browser tools (`mcp__Claude_Browser__*`),
  a tool name inside a verbatim quotation, not an attribution line; the driver may want it noted against the rule
  "no mention of Claude or any model in … documents".
- The tensions table covers the K = 1 contending sets, as the scope's default says; `case-model.md` also reports the
  K = 3 term led by the peak slew power, which maps to powerAndEnergy (operator) and is not in the table.
- The reviewer restored the "cubesat" recovery in a fresh tab and applied nothing; by the harness's §8 the modeller's
  tab-23 may show the recovery-clash message on its next save (Bug 10). The recovery record was not changed.
- The `origin/dev` head moved from 3cce6cd (the review's last commit) to 46cd9a2 during the review; the two commits
  are the driver's records and touch nothing of WP27.

## Open decisions (for the supervisor)

- **G-1.** Step 24's screenshot is cited by the review and not in `WP27-review/` — options: accept as is / fix before
  acceptance / follow-up work package
- **G-2.** D-4 does not record whether WP26's gate-class findings (T3, T5, N5, N6) block the sponsor's reading, as the
  non-goal asks; the decisions file routes T3 only — options: accept as is / fix before acceptance / follow-up work
  package
- **G-3.** F-5 of the feedback report has no numbered steps, expected/observed or screenshot (R-10) — options: accept
  as is / fix before acceptance / follow-up work package
- **G-4.** Two changes outside the blast radius: the harness note's §8 (0869ecf) and the WP26 sequel's commit 05fbd3c
  carrying WP27's record edits beside a `paper/` notebook output — options: accept as is / fix before acceptance /
  follow-up work package
- The observations above as one item: accept as is, or pick any to act on.

H-2 (a cost-to-build budget) is the supervisor's number and is not a gap.

## Gap dispositions

Each gap is resolved through the decision loop (`~/.claude/skills/CLAUDE.md`); the records go in `WP27-decisions.md`.

| Gap | Disposition (accept as is / fix before acceptance / follow-up work package) | Reason or follow-up |
|---|---|---|
| G-1 | — | — |
| G-2 | — | — |
| G-3 | — | — |
| G-4 | — | — |
| Observations | — | — |

## Recommendation

Recommend acceptance with the listed gaps noted, because every check the scope names was reproduced from a fresh
worktree and the editor shows what the review says: the three files load strictly and the trace, pointer, roll-up and
verdict tests pass (228 in the listed files; 47 of 47 verdicts hold, 6 negated); `experiments verify` reports 0 drifts
and the coverage table regenerates byte-identical; the pointers resolve by hand to the current ledger entry, the
RECORD.md heading, the image of record and two collected tests; the model's bytes moved only under WP26's rule with
every output hash equal; the P1 return is verbatim and every point has a disposition; in the editor the applied model
has 0 issues, the stakeholder view draws 54 nodes and 26 edges, and the Satisfaction matrix shows the three designs
(agile 9 / 3, baseline 11 / 1, compact 11 / 1) and the Verification matrix the two evidence cases (3 and 9). The gaps
are completeness of the record (one screenshot file, one non-goal record, one feature request's reproduction, two
edits outside the blast radius); none touches the model, the data, the outputs or the paper.

Acceptance is the supervisor's act, recorded as named above. This report does not accept the work.

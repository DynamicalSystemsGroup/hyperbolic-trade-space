# WP25-3 — Scope of work: Repository tidiness, third instance (at the WP23 close-out gate; step 3h, recurring)

| | |
|---|---|
| **Status** | DRAFT. Approved only by the recorded act below. Nothing in this package is executed before then. |
| **Supervisor (accountable)** | mzargham |
| **Repository** | `DynamicalSystemsGroup/hyperbolic-trade-space` (local: `/Users/z/Documents/GitHub/posynomial-invariant-form`); work on `dev` |
| **Approval record** | The driver's approval under the mandate (`release-candidate.md`), quoted verbatim in `work-packages/WP25-decisions.md` |
| **Acceptance record** | The driver's acceptance under the mandate, quoted verbatim in `work-packages/WP25-decisions.md`, after `work-packages/WP25-review.md` |

**Header note: the third instance of a recurring package, at the WP23 close-out gate.** The close-out was accepted
on three greens (`WP23-decisions.md`, 2026-11-10, 14:50; step 4 complete with it) and WP24 is final (19be468): the
model carries eight traded metrics (contract row 15), the data of record is at ledger @7, and the word "facet" has
left the package and the paper. The second instance (`WP25-2-scope-of-work.md`, `WP25-review.md` "Unit B") left four
items open: the held `spike-ternary/report.md`, the routed rows N-a and N-b, and the stale `k3-cubesat.md` (deleted
since by the close-out, f1101ce). This instance is its own file, as the second was (A3); everything in
`WP25-scope-of-work.md` and `WP25-2-scope-of-work.md` that this document does not change still governs. Scoped at
`dev` fbee839, 2026-11-10.

Sizing at fbee839 (the A2 command rerun in a scratch worktree with the package list of A2 below; 465 tracked files,
285 in the live set): **181 rows** outside the live set. By class: 58 records of accepted packages (kept by A1); 27
spike READMEs and generators under `docs/superpowers/notes/spike-*` (kept by the second instance's OD1); 7
`paper-sources/*.md` (read by `tests/test_narrative.py`, `tests/test_paper_sources.py`, the docs pages); 14 other
notes; 24 under `work-packages/WP23-rounds/` (5 in `gate/`, 19 round records, the ledger `.jsonl`, two spike
records); 22 of WP26 and 9 of WP27 (running packages; not this instance's); 4 external-assessment and review files;
1 `streams/P10-review.md`; 2 CI workflows; 13 repository-root and config files. **29 rows are named by nothing in the
live set, all of them WP26's and WP27's screenshots**; every other row has a live reader by path or basename. Only
two rows and one live-set file are candidates to leave: `spike-ternary/report.md` (OD1), `WP23-rounds/round-1/
generation-ledger.jsonl` (kept by the second instance as the ledger of the run that produced the data; re-read once
against @7), and `examples/adcs/experiments/reports/v1-v2-comparison.md` (OD2). The checks at the head: register,
docs, site, vocabulary and narrative tests 136 passed; doctests 57 passed; the vocabulary tool 69; `scripts/check.py`'s
path map has no stale path; every page of `mkdocs.yml`'s navigation exists.

## Purpose

The supervisor, 2026-11-09, 22:20, verbatim (`WP25-decisions.md`, "Origin"): "i appreciate you clean up all the images,
i think we are also starting to accumulate a pretty big documentation cruft/drift/gap i want you to periodically deploy
clean up work packages to address repo tidiness, this is essentially context management. the git history keeps
everything so tidying doesnt eliminate history, history keeping is gits job the repo state itself does not need to
duplicte that effort". The driver's disposition makes it step 3h, "one small instance at each gate and one before the
PR"; `PM-BRIEF.md` "Repository tidiness" adds the rule that deletions check the contract first.

The outcome of this instance: the four items the second instance left are closed or decided; the docs pages, the notes
and the records a test reads say what the code and the data of record say after the close-out (eight metrics, ledger
@7) and the rename; what the code and the paper do with no page is listed and filled or scheduled; every tracked file
outside the live set has a named reader or is gone.

## Goals

- G1. **Cruft, third pass.** The inventory rewritten at the head with one disposition per row (keep: reader named;
  delete; hold: package and instance); the delete rows, if any, removed in one commit that lists each path with what
  the content no longer did (A8 of the first instance). The two open files decided (OD1, OD2).
- G2. **Drift closed or routed after the close-out and the rename.** Found by: `uv run python scripts/check_vocabulary.py`
  (count not higher than 69); the claims register's test; a read of each docs page, the README and the notes a test or
  the paper reads that cite a number, a metric name or a public name, against the current API defaults and
  `examples/adcs/data/v2/` at @7; and the rows under "Drift, found by the survey" below. Each row ends closed (hash),
  fixed (this instance), or routed (owner and unit). N-a decided (OD3); N-b recorded closed.
- G3. **Gaps listed and filled or scheduled.** What exists in the code, the model or the paper with no documentation:
  the rows under "Gaps, found by the survey" plus what the read of G2 finds; each filled, dropped with a reason, or
  scheduled with an owner.
- G4. **Checked as run.** The site build, the fast suite, the guards, and `git show --stat` of the deletion commit,
  with their output lines in the review.

### Proposed dispositions (the inventory confirms or changes each at the head)

| Class | Rows | Proposed |
|---|---|---|
| Records of accepted packages (scope, decisions, review; the WP10 and WP19 review files; `WP11-round-1/triage.md`; `WP23-closeout-scope-of-work.md`) | 58 | keep (A1) |
| Spike READMEs and generators (`spike-certificates` 8, `spike-facet-refit` 6, `spike-objective` 7, `spike-figure1` 2, `spike-sysml-diagrams` 2, `spike-container-platform` 1) | 26 | keep: the second instance's OD1 (README and generator stay; outputs went in 14a41a4); readers `paper/supporting_material.ipynb`, `paper/generate_results.py`, `paper/figures/figure1.py`, `examples/adcs/case-model.md`, `paper/container/README.md` |
| `spike-ternary/report.md` | 1 | OD1 |
| `paper-sources/*.md` | 7 | keep: read by `tests/test_narrative.py`, `tests/test_paper_sources.py`, `docs/api-reference.md`, `docs/theory.md`, the register |
| Other notes (`abstraction-gaps`, `adcs-port`, `adcs-tensions-probe`, `notation`, `opensysml-usage`, `paper-appendices-sketch`, `paper-outline-v1-baseline`, `paper-outline-v2-search`, `paper-prior-art-sources`, `reader-grid`, `references-verified`, `search-prior-art`, `system-model-tidy`, `view-editor-harness`) | 14 | keep; each reader named (the second instance named them; `adcs-tensions-probe.md` is the v1 probe's record read by `examples/adcs/cubesat_model.py`, and its v1 names stay; `view-editor-harness.md` is WP26's) |
| `WP23-rounds/gate/*` | 5 | keep: the gate's record |
| `WP23-rounds/round-*/*.md`, `spike-redundancy.md`, `spikes/*.md` | 18 | keep: the modeller loop's and the close-out's records (`spike-B` is named by the close-out scope; `spike-redundancy.md` by `case-model.md` and contract row 15) |
| `WP23-rounds/round-1/generation-ledger.jsonl` | 1 | keep, re-read once: the ledger of the generation the data of record descends from (round-1 and round-4 READMEs cite it); the row names @7's relation to it |
| WP26 and WP27 files (reports, model-changes list, screenshots) | 31 | not this instance's (running packages); rows say so, no disposition |
| External assessment (3), `external-review-2026-11.md`, `streams/P10-review.md` | 5 | keep (assessment.md cited by the supporting notebook; `verification.json` by it); `P10-review.md` hold for WP10's acceptance, as before |
| CI, root and config (`.github/workflows/*`, `.dockerignore`, `.gitignore`, `.python-version`, `Dockerfile`, `LICENSE`, `CHANGELOG.md`, `pyproject.toml`, `uv.lock`, `mkdocs.yml`, `docs/{references.bib,ruff.toml,stylesheets/extra.css}`, `site/paper/index.html`) | 15 | keep: read by a test, a script, the build or the release |
| `examples/adcs/experiments/reports/v1-v2-comparison.md` (in the live set, not a row) | 0 | OD2 |

Counts if every proposal holds: 0 to 2 files deleted (OD1, OD2), 1 hold, the rest keep. This instance is small on
cruft and carries its weight in drift and gaps.

### Drift, found by the survey (each a row of D-3; the read of G2 adds to them)

- **S-1.** `claims_register.toml` C001's `note` and `docs/superpowers/notes/claims-review.md` line 74 cite
  `spike-ternary/report.md`'s Correction for "the largest log V of any design is 0.071", a figure measured on the
  earlier (v1) table; `docs/examples.md` (C001's page) does not state the figure; C001's listed backing is two tests
  and `plot_ternary`. Resolved by OD1.
- **S-2.** `docs/superpowers/notes/spike-certificates/README.md` line 106 and `run_cubesat.py` lines 20-21 cite
  `k3-cubesat.md` (deleted at f1101ce) and the earlier taus (195.18, 162.78): a record of the spike's own run on the
  earlier generation. Fix: the citation gains the hash of the last version, as `derivation/PROOF_MAP_FINDINGS.md`
  did (the second instance's row 19); the numbers stay as the spike's *(default, A6)*.
- **S-3.** "facet" in the model's sense in notes `CLAUDE.md` names, which the vocabulary tool does not scan:
  `proof-conventions.md` (lines 96, 99, 107, 109, 118, 126, 127), `claims-review.md` (the reviewer's own words at
  lines 10 and 74; the quoted paper fragments at 76-95 are quotations), `figure-review.md` (line 7 quotes a caption;
  lines 70-72 discuss the word). WP24's close says the word remains only in the three polyhedral sentences, the
  decision records and the supervisor's quotations. Fix per A5: the notes take the vocabulary where the word is the
  model object; quotations and the discussion of the word keep it *(default)*.
- **S-4.** `examples/adcs/case-model.md` line 363 cites `docs/clients/python/verification.md`, not in the tree
  (the runtime's own docs path, by its sentence): confirm and say whose path it is, or fix the link *(default: A6's
  form, "the runtime's `<path>`")*.
- **S-5.** `CHANGELOG.md` names no package after WP18: WP19 (figures), WP22 and WP23 with its close-out (the model,
  eight metrics, the data of record), WP24 (the rename; its line 20 was fixed at c3c1ce3), WP25 (the deletions).
  Routed to WP8b, whose deliverable the changelog is *(default, A7)*; the row lists the packages.
- **S-6.** The docs pages carrying numbers, sized for the read of G2: `fitting.md` 14 lines with a decimal,
  `examples.md` 8, `tensions.md` 6, `getting-started.md` 6, `chart.md` 5, `termination.md` 3, `README.md` 2,
  `prediction.md` 1, `conditioning.md` 1 (46 lines); `examples.md` is the only page naming the case's metrics (22
  lines; it says "eight metrics"). Each number read against the default that produces it or `data/v2` at @7, by the
  command or doctest that prints it (A10).
- **S-7.** Checked and found current, recorded for the reviewer: `glossary.yaml`'s MoE and MoP entries name the
  eight traded metrics between them (pointing error and launch cost; the other seven); no live docs page, the
  README, the glossary or the register says "nine" or "ten metrics", "slew time" or "eclipse reserve" (the
  `case-model.md` lines on the reserve narrate its leaving); the contract's current sections carry no old name (the
  old names sit in the change-control log and in the frozen-columns history of section 7); the `RENAMED` map (N-c)
  stays gone.
- **N-a** (`examples/adcs/model_v2/views/coverage.csv` names its decision-element column by the enum type
  `WheelClass`; the view's tags name the attribute): the file is now in WP26's and WP27's blast radius, changed only
  through the generator. Resolved by OD3.
- **N-b** (`paper/length_ledger.toml`, "the earlier radius was a typed constant"): closed. WP24 push 3's ledger
  comment (now line 612) records that the row no longer names the clause; `grep -n "typed constant"
  paper/length_ledger.toml` finds the comment only. Recorded in D-3 with the hash.

### Gaps, found by the survey (each a row of D-3)

- **P-1.** Four public module constants on no page and in no contract row: `estimator.EPS_ZERO_EXPONENT`,
  `estimator.PARTICIPATION_THRESHOLD`, `plotting.CATEGORY_COLORS`, `plotting.DATA_COLOR`. Fill (one sentence on the
  Fitting and Chart pages, within their word budgets) or drop with a reason.
- **P-2.** Of the 145 backticked names in `work-packages/interface-contract.md`, 87 appear on no docs page. Classed
  at execution: old names in the change-control log; case-module and data names documented in
  `examples/adcs/case-model.md`; what is left is a public name with no page, filled or dropped with a reason. The
  second instance's dropped rows (the 18 `solvers` names, the submodule names `tuning`, `predictive`,
  `preconditioning`) stand and are not re-asked (A7).
- **P-3.** The close-out's case functions (`case.association_all_pairs`, `case.requirements_table`,
  `case.design_sets_table`) are on `case-model.md`; `docs/examples.md` is read for whether it says what they add
  (the association step, the requirements read after the fit) and a sentence is filled or the row is dropped with the
  reason that the page is the user's, not the case's.
- **P-4.** The gate rule "the container is a gate check, not a unit step" and the "host-recorded, re-pin at the
  gate" marking live in `PM-BRIEF.md` only; `paper/container/README.md` does not say them. Listed and routed to the
  driver (the container's README and RECORD are his) *(default, A7)*.
- **P-5.** WP26's `views.sysml` and WP27's `stakeholders.sysml` have no page outside their packages' records; the
  row names them as those packages' to document at their acceptance (not this instance's).

## Non-goals

- The paper's prose and figures (`paper/`), `src/`, `derivation/`, the data (`examples/adcs/data/*`, the ledgers),
  the model files (`examples/adcs/model_v2/*.sysml`, `cubesat_tradespace.sysml`, `cubesat_model.py`), and any
  committed number.
- Glossary entries (`glossary.yaml`; an entry regenerates Appendix A): a drift row on an entry is listed and routed
  to the PM, not fixed here.
- Anything a running package owns: WP26 and WP27 (`examples/adcs/model_v2/*`, `work-packages/WP26-*`,
  `work-packages/WP27-*`, `docs/superpowers/notes/view-editor-harness.md`, the browser pane's tab-23); WP11
  (`work-packages/WP11-*`); WP10 (`work-packages/streams/P10-review.md` holds).
- `interface-contract.md`, `interface-contract.toml` and `tests/test_interface_contract.py`: read for every delete
  row (R-2), never edited (an amendment is the PM's to route).
- Not step 5a (improvement by subtraction); not a judgement of prose or figures; no archive folder, no renaming, no
  new tooling (no script, test or CI step for the inventory).
- `CHANGELOG.md`'s entries (WP8b's); `paper/container/README.md` and `RECORD.md` (the driver's).

## Deliverables

| ID | Deliverable | Serves |
|---|---|---|
| D-1 | `work-packages/WP25-inventory.md` rewritten at the head: the command (A2, with its package list) and the live set in the header; one row per file outside the live set with references, disposition and, for deletes, what the content no longer did; the first section "Contract and tests" listing the grep over `interface-contract.md`, `interface-contract.toml` and `tests/test_interface_contract.py` for every delete row, OD2's file included if it goes | G1 |
| D-2 | One deletion commit if any row deletes: every delete row, nothing else, message "WP25: <n> files deleted (third instance)" with one line per path; the register and note edits of OD1 in the same push, before the deletion in the sequence | G1 |
| D-3 | `work-packages/WP25-review.md` rewritten: "Drift" (S-1 to S-7, N-a, N-b, and every row the read of G2 adds, each closed with a hash, fixed, or routed with owner and unit) and "Gaps" (P-1 to P-5 and what the read adds, each filled, dropped with reason, or scheduled with owner), with the vocabulary count, the register test and doctest lines before and after | G2, G3 |
| D-4 | Fixes for the drift rows and gap fills on a free surface, one commit per file, each citing its row | G2, G3 |
| D-5 | `WP25-review.md`, "Checks": site build, fast suite, guards, lock, `git show --stat` of D-2, with output lines | G4 |
| D-6 | `WP25-decisions.md`: the driver's approval and acceptance verbatim, OD1 to OD3's outcomes; one instance line in `WP25-scope-of-work.md`'s header note | all |

## Requirements

| ID | Requirement | Checked by |
|---|---|---|
| R-1 | The inventory has no undecided row and no path outside the live set without a row | rerun the D-1 command at the head and diff its first column against D-1's rows (empty); `grep -ciE "undecided\|tbd\|\?\?" work-packages/WP25-inventory.md` returns 0 |
| R-2 | **The contract and its test are in the grep before any file goes**: for every delete row, `git grep -n -F -e <path> -e <basename> -- work-packages/interface-contract.md work-packages/interface-contract.toml tests/test_interface_contract.py` is empty (a hit that is another file's name is explained in the row), or the amendment retiring the pin is in the same push | the D-1 section "Contract and tests"; the reviewer reruns the grep per delete row |
| R-3 | Nothing live references a deleted file | `for f in $(git diff --name-only --diff-filter=D <start>..HEAD); do git grep -l -F "$f" -- . ':!work-packages/WP25-*'; done`: hits only in records, each listed in D-5; 0 in every other live file |
| R-4 | The deletions are one commit whose paths equal D-1's delete rows | `git show --stat <hash>`; `git show --format=%B -s <hash>` names each path |
| R-5 | The site builds; the fast suite is green apart from failures already on the head, each named | `uv run python scripts/stage_site.py --paper placeholder`; `uv run pytest -q -m "not slow" -n auto`; `uv run python scripts/check.py --changed` |
| R-6 | The vocabulary tool's count is not higher than 69; the register test, the docs tests and the doctests pass as at the start; the lock holds | `uv run python scripts/check_vocabulary.py`; `uv run pytest -q tests/test_claims_register.py tests/test_docs.py tests/test_site.py tests/test_vocabulary.py tests/test_narrative.py`; `uv run pytest -q --doctest-modules src`; `uv lock --check` |
| R-7 | The paper, `derivation/`, `src/`, the data, the model files and the committed numbers are untouched; nothing renamed | `git diff --stat <start>..HEAD -- paper derivation src examples/adcs/data examples/adcs/model_v2 examples/adcs/experiments/ledger` empty; `--diff-filter=R` empty |
| R-8 | No file of a surface under Non-goals is edited: `glossary.yaml`, the contract files, `CHANGELOG.md`, `paper/container/*`, every WP26, WP27, WP11 and WP10 path | `git diff --stat <start>..HEAD` against the Non-goals paths: empty |
| R-9 | Every drift row ends closed, fixed or routed with an owner; every gap row ends filled, dropped with a reason or scheduled with an owner; OD1 to OD3's outcomes are applied as decided | inspection of D-3 against this document's S-, N- and P- rows and the rows the read added; none open without an owner |
| R-10 | No attribution line; each push leaves `dev` green at tier 2 | `git log --format=%B <start>..HEAD \| grep -ciE "co-authored-by\|generated (with\|by)"` returns 0; the watcher's verdict per push in D-5 |
| R-11 | Every number a drift fix writes on a page is the value a named command or doctest prints at the head (no number re-derived by hand) | each D-4 commit message names the command; the reviewer reruns one per page |

## Blast radius

Delete, per the inventory's delete rows: `docs/superpowers/notes/spike-ternary/report.md` (under OD1 (b) or (c)) and
`examples/adcs/experiments/reports/v1-v2-comparison.md` (under OD2 (b)). Edit: `claims_register.toml` (C001's note
only, under OD1 (b) or (c)); `docs/superpowers/notes/{claims-review,proof-conventions,figure-review}.md` (S-1, S-3);
`docs/superpowers/notes/spike-certificates/{README.md,run_cubesat.py}` (S-2, a citation line and a comment);
`examples/adcs/case-model.md` (S-4's one link; nothing else on the page); the docs pages `docs/*.md`,
`docs/user-guide/*.md` and `README.md` for the rows the read of G2 and the fills of P-1 to P-3 land (within
`tests/test_site.py`'s word budgets); `docs/superpowers/notes/abstraction-gaps.md` only if the read finds a number
that moved at @7 (it was rewritten at b9d8b80). Records: `WP25-3-scope-of-work.md`, `WP25-inventory.md`,
`WP25-review.md`, `WP25-decisions.md`, the header note of `WP25-scope-of-work.md`.

Never: the Non-goals list; `pyproject.toml`, `uv.lock`, `.python-version`, `mkdocs.yml`, the CI workflows,
`docs/superpowers/specs/`, every other package's records, `work-packages/WP23-rounds/*` (the gate's and the loop's
records).

## Sequence

No gate waits: the close-out and WP24 are accepted, and nothing of WP26 or WP27 is touched. While a container
regression runs for another gate, this instance pushes prose, docs and records only (it regenerates nothing).

1. The inventory at the head (D-1), with its "Contract and tests" section for the OD1 and OD2 rows.
2. The drift fixes and gap fills on free surfaces (D-4), one commit per file; the read of S-6's nine pages first,
   then S-2, S-3, S-4, P-1 to P-3.
3. OD1's edits (the register note, `claims-review.md` line 74) and then the deletion commit (D-2), in one push, so
   no citation dangles.
4. The review last (D-3, D-5), rerunning R-1 to R-11 at the head; the instance line in the first scope's header
   note; D-6.

## Definition of good

- A tree in which every tracked file has a reader a newcomer can name; the docs, the notes and the records a test
  reads say what the code and the data of record say after the close-out and the rename; nothing the second
  instance left open is still open; a fresh PM reads only the present.

## Definition of good enough

- The inventory has no undecided row, and R-2 holds for every delete row (R-1, R-2).
- One deletion commit for what OD1 and OD2 free, listing each path (R-4), or the review's statement that no row
  deleted; nothing live references a deleted file (R-3); the site builds and the suite, guards and lock are as at
  the start or better (R-5, R-6).
- The paper, `derivation/`, `src/`, the data, the model files and the committed numbers untouched; no Non-goals
  surface edited (R-7, R-8).
- S-1 to S-7, N-a, N-b, P-1 to P-5 and every row the read adds end closed, fixed, routed, filled, dropped or
  scheduled with a named owner; OD1 to OD3 applied as decided (R-9); every written number traces to a command
  (R-11); no attribution; `dev` green (R-10). Stop there and present.

## Definition of done

Good enough is met, **no open item remains unresolved**, and the supervisor has accepted the work by the acceptance record above.

## Agent's defaults

Approved or changed as one item at the scope gate. Each is marked *(default)* where it appears.

- **A1. Inherited.** The first instance's A1 (live set, what a reference is), A2 (the command), A7 (outputs nothing
  reads), A8 (message form), and the second instance's A2 (pre-classification is a proposal; the inventory is the
  decision), A4 and A6's reasoning hold unchanged *(default)*.
- **A2. The command's package list.** The live set's "packages not yet accepted" list becomes WP8a, WP8b, WP10,
  WP11, WP12, WP15, WP16, WP17, WP18, WP19, WP20, WP21, WP22, WP25, WP26, WP27 (WP23 and WP24 leave, accepted; WP26
  and WP27 join); `WP23-closeout-scope-of-work.md` is a record kept by A1. The sizing above used this list *(default)*.
- **A3. Own file.** The instance is its own document because it carries the two open decisions on files and the
  survey; D-6 adds the one recurrence line to the first scope's header note *(default)*.
- **A4. Zero deletes is a valid outcome.** If OD1 and OD2 both keep, there is no D-2 commit and the review says so
  in one line; the package is then drift and gaps *(default)*.
- **A5. Fixes on free surfaces are made; the rest routed.** A drift row on a docs page, the README, a note
  `CLAUDE.md` names or a kept spike's README is fixed here, one commit per file. A row on a glossary entry, the
  contract, the paper, the model, the changelog or the container's records is listed and routed (the PM, the paper
  stream, WP26, WP8b, the driver). The notes `CLAUDE.md` names take the vocabulary where "facet" is the model
  object; quotations of older text and the discussion of the word keep it (S-3) *(default)*.
- **A6. Citations of deleted files in kept notes gain the hash of the last version** ("deleted; last version at
  <hash>"), the form of the second instance's row 19; a cited path outside the tree that belongs to another project
  is named as that project's (S-2, S-4) *(default)*.
- **A7. Gap rows dropped with a reason by the second instance are not re-asked**; new rows are P-1 to P-5; S-5 and
  P-4 are routed, not filled *(default)*.
- **A8. The read of S-6 is by command, not by eye**: each number on a page is checked against what the doctest, the
  example block or `examples/adcs/case.py` on `data/v2` prints at the head; a moved number is fixed with that command
  named in the commit (R-11) *(default)*.
- **A9. OD2 (b) leaves the pins as history.** If `v1-v2-comparison.md` goes, `paper/container/RECORD.md`'s and
  `WP23-rounds/gate/README.md`'s hash rows for it stay as records (they are not edited); `uv run python -m experiments
  compare` regenerates the file on demand and `tests/test_experiments.py` writes its copy to a temporary path; the
  inventory names `docs/superpowers/notes/system-model-tidy.md`'s remaining reader (`work-packages/README.md`) *(default)*.
- **A10. Order of units** as under "Sequence" *(default)*.

## Open decisions (for the supervisor)

- **OD1.** `docs/superpowers/notes/spike-ternary/report.md` is held because `claims_register.toml` C001's note and
  `claims-review.md` line 74 cite its Correction for "the largest log V of any design is 0.071", a figure measured on
  the earlier (v1) table and stated on no page; C001's listed backing is two tests and `plot_ternary`'s Notes, and
  the page's sentence ("a marker is not where V = 1") does not use the figure. What happens to the report, and what
  does C001 then rest on? — options: (a) keep the report as the note's reader (the row is keep, the hold ends) /
  (b) delete it; the register note and line 74 drop the 0.071 sentence, and C001 rests on its listed backing /
  (c) delete it, and the paper stream replaces 0.071 with the same figure printed by a generator on the data of
  record, in a unit before the deletion.
- **OD2.** `examples/adcs/experiments/reports/v1-v2-comparison.md` (50 kB, the gate's comparison of WP15's D-9;
  regenerated by `uv run python -m experiments compare`; its hash pinned in `paper/container/RECORD.md` and
  `WP23-rounds/gate/README.md`; cited by `swap-evidence.md`, `WP23-review.md`, `streams/P10-review.md`; read by no
  test or page; the second instance's A6 kept it and named this instance to decide). Keep or delete? — options:
  (a) keep as the gate's comparison of record, the row names its readers / (b) delete; the generator regenerates it
  on demand and the hash rows stay as history (A9).
- **OD3.** N-a: `examples/adcs/model_v2/views/coverage.csv` names its decision-element column by the enum type
  (`WheelClass`) while the view's tags name the attribute, and the caption bridges the two. The file is now changed
  only through WP26's and WP27's generator. What closes the row? — options: (a) the caption's bridge is the intended
  reading; closed in the review / (b) routed to WP26's modeller as one unit through the generator, with the model
  tests' pins re-read / (c) deferred to the instance after WP26 and WP27 are accepted.

The driver decides OD1 to OD3 under the mandate; the rest is the Agent's defaults as one item.

## Gate outcomes

- None yet.

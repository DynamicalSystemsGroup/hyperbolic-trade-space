# WP14 — Review report

| | |
|---|---|
| **Scope of work** | `work-packages/WP14-scope-of-work.md` |
| **Scope approval verified** | `work-packages/WP14-decisions.md`, "Scope approval": supervisor (mzargham), verbatim "Approved", 2026-11-08, scope at commit 0ece73e (no open items; R-12 added). OD1, OD2 and the defaults recorded with verbatim quotes. Verbal record, as the scope names; no PR. |
| **Work reviewed** | `dev` at HEAD 328371a. WP14 commits: 3b79cb4, 4b559cb, 1f2356b, 0ece73e (records/scope/README), df475b8, 02b9731 (document, links), 9f8e5f7 (test), 328371a (contract follows the delivered site machinery). The manifest was first committed inside a WP8a-titled commit, a854cc4 (see gap G-3). |
| **Supervisor (accepts)** | mzargham |
| **Acceptance record** | Verbal acceptance in chat, quoted verbatim in `work-packages/WP14-decisions.md`, after this report |

Reviewer: fresh context, did not build the work. Nothing fixed; the only file written is this report. Break demonstrations and scripts live in the session scratchpad, outside the repository.

## Checks run

| Check | Command | Result |
|---|---|---|
| Contract test | `uv run pytest tests/test_interface_contract.py -q -rs` | `85 passed, 2 skipped in 26.76s`. Skips are legitimate and reasoned: R-7 paper configuration (`paper/myst.yml` absent, WP10) and R-3a Oracle protocol (`examples/adcs/experiments/oracle.py` absent, WP15). |
| Lint / format / lock | `ruff check tests/test_interface_contract.py`; `ruff format --check` on the test and the contract; `uv lock --check` | all clean; lock resolves (173 packages) |
| Staging | `uv run python scripts/stage_site.py` | exit 0, "staged site in .../_stage" (docs built with mkdocs, root index and paper slot present). `--serve` not run (blocks); the test asserts the flag exists. |
| Attribution | `git log fc2363e..HEAD --format=%B \| grep -iE 'co-authored\|generated'` | two hits, both the word "generated" in subjects ("generated pages", "generated from docstrings"); no trailer or generated-by line |
| Whole suite | not rerun by me (only the contract test, lint and lock) | |

### Deliberate temporary breaks (scratch copy of HEAD, not in the repo; `git archive` into the scratchpad)

1. Renamed `select_temperature` throughout `src/` (package consistent, so only the contract notices): `6 failed, 1 error`; messages include `[contract R-1] public name 'select_temperature' must be in __all__ (floor) (side: technical; change by amendment, work-packages/interface-contract.md)` and `[contract R-1] hyperbolic_trade_space.tuning must provide 'select_temperature' (floor) ...`.
2. Manifest `EPS_KKT = 1e-7`: `[contract R-1] solvers.EPS_KKT must equal 1e-07 (side: technical; change by amendment, ...)`.
3. Manifest `contract_version = 2`: `[contract R-8] document version 1 differs from manifest 2 (side: both; ...)` and `quoted contract_version = 1 differs from manifest 2`.
4. Added "Uses SysML internally." to the document: `[contract R-3a] 'sysml' (modeling-tool word) found in work-packages/interface-contract.md`.
5. Put `docs/` into the WP10 ownership set: `[contract R-10] ownership sets overlap: [('technical','docs/method.md','wp10','docs/'), ...]` and `[contract R-9] path 'docs/' of side 'wp10' is missing from document section 16`.

Every message names the clause, the side and the amendment path.

### Independent fact check (my own script `scratchpad/rev.py`, reads the manifest, checks the repository): 101 checks, 0 failures

Package: import and distribution names; version equal in `pyproject.toml`, `__version__`, manifest (0.0.1); every public name in `__all__` (`__all__` has no extra); every name in all 10 `submodule_names` lists importable; 4 certificate signatures equal `inspect.signature` parameters; `Termination` fields and `TensionReport` fields; 4 tolerances (EPS_FEAS 1e-9, EPS_KKT 1e-8, GUARD_TOL 1e-12, POLISH_STEPS 5). Case: all 28 signature rows across `k_terms`, `generate_dataset`, `design_space`, `cubesat_model`, `adcs_sim`, `make_check_designs`; `REGIMES`; the cubesat `measure` pair. Data: all 5 CSV headers equal the manifest columns exactly, in order, and row counts (1000, 1000, 1000, 6, 3). Figures: all 15 listed files have the PNG signature; no figure file is outside the list. Derivation: `len(CHAIN) = 14`, all `run_attributes` present, lemma numbers contiguous 1..14. Docs: six pages and `references.bib` exist. Build: `scripts/stage_site.py`, `scripts/build_generated.py`, `mkdocs.yml`, `site/index.html`, `pages.yml`, `test.yml`, `docs/api-reference.md`, `docs/index.md`, `docs/case.md` exist; `default-groups = ["dev","case","docs"]`; `.python-version` 3.12; `docs/generated/` and `_stage/` are git-ignored.

Ownership: my own overlap check (equal, or directory prefix, carve-outs exempt only against the enclosing prefix) over the 8 sides: **no overlaps**. Coverage: every one of the tracked files (`git ls-files`) falls in some side's set (none unowned).

## Goals

| ID | Verdict | Evidence |
|---|---|---|
| G0 | met | Section 3 pins the table and the `Oracle` signature; case-insensitive grep for `opensysml`/`sysml` over the contract text, `__init__.py` and all of `src/`: none; no tool-version string in the document (only the package version and a localhost URL carry dotted numbers). Break 4 shows the test catches it. |
| G1 | met | Sections 3-13 give path, entry point or command, format for each consumed thing; section 15 gives may-assume and must-not-touch per consumer. |
| G2 | met | Section 14 (amendment), section 16 (ownership by side, disjoint, "no file is shared beyond links"). |
| G3 | met | Test in the default `uv run pytest`, offline; 50 test functions; messages as shown. |
| G4 | met | Docsite, paper and release machinery each have a section and a paragraph; the manifest and ownership let each proceed independently. |

## Deliverables

| ID | Verdict | Evidence |
|---|---|---|
| D-1 | met | `work-packages/interface-contract.md`, 18 sections; 2,465 words in all, about 2,250 outside the quoted TOML block: readable in about ten minutes. |
| D-2 | met | `work-packages/interface-contract.toml`, header documents the schema; read by `tomllib`; section 2 of the document quotes it and the test compares line by line (break 3). |
| D-3 | met | `tests/test_interface_contract.py`. |
| D-4 | met | `work-packages/README.md` row 99 links the contract; the README Branching bullet carries the release-control step; `CLAUDE.md` lines 12-13 link the contract and manifest. The scope's "Status table" link: the Status table row for WP14 was updated in 3b79cb4 (status), the breakdown row links the document. |
| D-5 | met (review part) | `WP14-decisions.md` exists with origin, OD1, OD2, defaults, scope approval; this file is the review. |

## Requirements

| ID | Verdict | Evidence |
|---|---|---|
| R-1 | met | Import and distribution names, `__all__` floor, 10 submodules with importable names, certificate functions and their parameter names, fitted attributes, `Termination` fields and statuses, `TensionReport` fields: all verified by my script; break 1 fails with the clause message. Submodules include `estimator`, added beyond the scope's list (additive, allowed). |
| R-2 | met | Version equality and PEP 440 verified; manifest value equal; section 5 states format, value, WP8b as the only changer, read-only for presentation. |
| R-3a | met | Section 3 states table, oracle protocol in full, black box, cubesat instance, and the "pinned at WP15" status; toy oracle in the test; grep clean; break 4. Oracle protocol not yet pinned, as scoped (gap G-5). |
| R-3 | met | Modules, functions, parameter names, regimes, five CSVs with exact header and dtype class all match; `run_regime` smoke test is in the passing suite (per manifest `smoke_run`). |
| R-4 | met | Directory, naming patterns, PNG format, producing commands, read-only rule; 15 files verified; the test also rejects a figure that matches no pinned naming. |
| R-5 | met | Chain of 14, ordered, contiguous numbering, `run`/`axioms` interface, generated pages named and located; `scripts/build_generated.py` now exists and the clause is enforced. |
| R-6 | met | Six pages plus bib, syntax rules, rename rule, presentation-owned paths listed; OD2 reflected (api.md hand-written overview, `api-reference.md` generated from numpydoc docstrings, manifest `package.docstrings.source_of_api_reference = true`). |
| R-7 | met, with a recorded change (gap G-2) | Commands, outputs, public paths, dependency-group owners, default groups, branches verified. Deploy trigger now "release tag v* and manual dispatch only" and workflow `pages.yml`, not the scope's `publish.yml` from `main`; follows WP8a OD2 (commit 2eddca1). |
| R-8 | met | `contract_version = 1` equal in manifest, document and last change-log row (break 3); amendment procedure with supervisor-quote rule, floor rule and deprecation rule in section 14. |
| R-9 | met with a judgment (gap G-1) | `git show --name-only` over the eight WP14 commits: `tests/test_interface_contract.py`, `interface-contract.md`, `interface-contract.toml`, `work-packages/README.md`, `CLAUDE.md`, `WP14-decisions.md`, `WP14-scope-of-work.md` (record edit 0ece73e), and one foreign path, `.github/workflows/pages.yml` (328371a). No WP13-owned path (`src/`, `derivation/`, `docs/`, `examples/`, `pyproject.toml`, `uv.lock`) touched. Ownership table by side is in section 16 and the test checks the document against the manifest. |
| R-10 | met | Per-package sets (WP8a, WP10, WP12 empty, WP8b, driver, process, WP14, technical); my script finds no overlap and full coverage; break 5. |
| R-11 | met | Section 17 lists five gaps, each with a closing package (WP8b, WP10, WP10, WP10, WP15); verified true: `__init__` docstring still says "arrive in later work packages"; no `paper/`; no `paper` group. |
| R-12 | met | Section 13 and manifest `build.stage` pin `uv run python scripts/stage_site.py --serve`, `_stage/`, `http://127.0.0.1:8000`, no network, no kernel; the script exists and `uv run python scripts/stage_site.py` stages the site (exit 0); README Branching bullet carries the review step and the recording rule; test asserts both. |

## Definitions

| Item | Verdict | Evidence |
|---|---|---|
| Good: two sides need only the contract | met | Sections 15 and 16 |
| Good: ten-minute read, test is the review | met | ~2,250 words; 85 assertions |
| Good: failure messages name clause, side, amendment | met | All five breaks |
| Good: manifest single source, no drift | met | Section 2 block compared line by line; break 3 |
| Good enough: D-1 to D-5, R-1 to R-11, plus R-12 | met | above |
| Good enough: test fails on a removed or renamed item, shown once | met | Breaks 1-2, not committed |
| Good enough: four consumers with assume / not touch | met | Docsite, paper, release machinery, technical side in section 15 |
| Good enough: OD1/OD2 recorded as decided, with quote | met | Sections 8, 10, 13; `WP14-decisions.md` |
| Good enough: supervisor can name his WP8a/WP10 files | met | Section 16 rows WP8a and WP10 |

## Non-goals respected

No docsite, paper or release files authored by WP14 (they exist from WP8a); no package, derivation, data or narrative change; no new dependency (the test imports `packaging`, a locked transitive dependency of pytest, not declared in `pyproject.toml`; see G-4); no tool names in the contract.

## Gaps: open decisions with suggested dispositions

- **G-1 (R-9 ownership).** Commit 328371a, titled for both packages, edits `.github/workflows/pages.yml` (adds `permissions: contents: read`, a WP8a-owned file) alongside WP14's contract files. Suggested: accept as is; the hunk is two lines, labeled "WP8a: least-privilege build job" in the subject, and the contract's own R-7 test reads that file. Future commits should keep the packages separate.
- **G-2 (R-8 change control).** Between the approved scope and delivery the pinned deploy rule changed (from `main` via `publish.yml` to release tag v* or dispatch via `pages.yml`) and `docs` joined `default-groups`, with `contract_version` still 1 and no change-log row beyond the initial one. Suggested: accept as is, because v1 was not yet accepted and the change follows the supervisor's WP8a OD2; ask the supervisor to confirm that acceptance fixes v1 as including it. The first amendment after acceptance is version 2.
- **G-3 (provenance).** The manifest first entered the repository in a WP8a-titled commit (a854cc4), not a "WP14: " commit, and WP14's own commits then modify it. Suggested: accept as is; history is final and the content is correct.
- **G-4 (stale skip list).** Section 18 of the document and the manifest `[skips.*]` still list eight clauses, six of which now run (their files exist); only the `paper/myst.yml` and Oracle clauses actually skip. The statement "skips until the file exists, then enforces" remains true, but the table reads as current. Also the WP8a row of the `work-packages/README.md` still says the Pages workflow deploys "from `main` on merge". Suggested: follow-up, trim the skip list when WP10 and WP15 close theirs (amendment-free housekeeping), and fix the README row at the next process commit; neither blocks acceptance. The test depends on `packaging` without declaring it: accept as is (pytest requires it), or have the driver add it to `dev`.
- **G-5 (open by design).** Oracle protocol unpinned (WP15); `paper/myst.yml` and `paper` group missing (WP10); `__init__` docstring (WP8b); WP12 ownership empty. Suggested: accept as is; each has a closing package and a skipped or recorded clause.
- **G-6 (verification limit).** I ran the staging build but not the `--serve` mode, and did not rerun the whole suite. Suggested: the supervisor's first staged review (WP8a's gate) exercises `--serve`; the full suite is covered by the local checks the delivery paragraph requires.

No gap requires a fix before acceptance. Acceptance is the supervisor's, by the recorded act above.

# WP67 — Scope of work: quality control of the two release control models (stage 4)

| | |
|---|---|
| **Status** | DRAFT, approved by the driver as his proxy under his approval of the plan (2026-11-16, `WP64-decisions.md`) |
| **Supervisor (accountable)** | mzargham |
| **Repository** | `DynamicalSystemsGroup/hyperbolic-trade-space`; `dev` after the three build units (WP66b ea82a15e, WP66c bf823f22, WP66a); QC branches `qc/**` and `qc/paper/**` on `origin`, deleted when the record is in |
| **Approval record** | The driver's approval under his mandate, quoted in `WP64-decisions.md` |
| **Acceptance record** | The QC record `work-packages/WP67-rounds/record.md` with every run's id and conclusion, the captures, and the machinery diff explained; the driver's acceptance as proxy; his read before WP68's pull request |

## Purpose

Run the two release control models as built, on hosted runners and in a browser, before the first merge into `main`
(`work-packages/WP65-design/build-plan.md`, section 4). No dispatch of `release.yml` or `paper.yml` exists before
that merge, so every run is a push to a `qc/**` branch, which the workflows treat as a dry run: nothing tags,
publishes or deploys.

## Goals

- G1. The release dry run on `qc/release` from `dev`'s head: `admissibility`, `test`, `build`, `site` green;
  `tag`, `publish-*`, `deploy-site`, `publish-release`, `on-failure` skipped; the summary names the slot `abstract`.
- G2. The release dry run that fails, on `qc/release-fail`, from a commit whose `CHANGELOG.md` lacks the entry:
  `admissibility` fails naming the changelog; nothing after it runs; no issue is opened.
- G3. The `_site` artefact of G1 downloaded and staged locally; `/paper/` is the abstract page; the composer's line
  in the run log reads `slot abstract`.
- G4. The paper branch build on `qc/paper/build` from `dev`'s head: the paper tests, the HTML build and the keys
  check; the `paper-release` artefact holds the HTML archive and the key manifest. The residual-baseline test is
  known to fail on `dev` (WP66b's landing record); the run's other steps are judged on their own, and the failure is
  recorded as the paper branch's first item, not repaired here.
- G5. The paper failure path on `qc/paper/broken`, from a commit that breaks one paper test: `build` fails and the
  summary names the step; no release, no issue.
- G6. The clean-up script by hand: `release_cleanup.py --tag v0.0.0 --dry-run` and `--tag paper-working-20000101
  --dry-run` exit 0 with "nothing to remove".
- G7. The machinery diff: `work-packages/WP64-rounds/machinery.toml` against the built tree; every row changed,
  removed or added explained in the record.
- G8. The browser pass per mode: staged with `--slot abstract`; then with `--artefact` at the `paper-release`
  artefact of G4 (or, if G4's artefact is not produced, a local build of the paper) under a temporary, uncommitted
  `paper/mode.toml` in each of `working`, `submitted` and `revision` with test `doi` and `sha256`; then the fallback
  (a wrong checksum). For each: `/`, `/paper/`, `/paper/supporting-material/`, one docs page with a citation (the
  link lands on the anchor in a pinned slot and on `/paper/` otherwise), 1,280 and 375 px, light and dark; the
  banner read in each mode; the console free of errors; captures in the record.
- G9. Lint and the fast shard on every push to `dev` (the external review of 2026-11-16, finding 1): `test.yml`
  gains a `push` trigger on `dev` that runs the Linux `fast` shard and lint only; the pull-request and call paths
  unchanged; `tests/test_ci_shards.py` amended; amendment 29's description of `test.yml`'s triggers amended in the
  contract.

## Non-goals

No merge into `main`, no tag, no publish, no deploy, no change to his keyboard settings; no repair of what a run
finds beyond G9 and a fix of a defect in the build units' own files that a run exposes (each such fix a commit on
`dev` named in the record, re-run afterwards); no change to the paper's content, the residual baseline or the
package's public surface; the `qc/**` branches deleted at the end.

## Deliverables

| ID | Deliverable | Serves |
|---|---|---|
| D-1 | `work-packages/WP67-rounds/record.md`: one row per run (branch, head, run id, conclusion per job, the expected result, met or not), the clean-up outputs, the machinery diff explained, the browser pass table | G1 to G8 |
| D-2 | `work-packages/WP67-rounds/captures/` | G8 |
| D-3 | The `push` trigger on `dev` in `.github/workflows/test.yml`, its test and the contract amendment | G9 |
| D-4 | Fixes a run exposes, each a commit on `dev` named in D-1, re-run green | G1 to G5 |

## Requirements and checks

| ID | Requirement | Check |
|---|---|---|
| R-1 | Every run of the build plan's section 4 table has a run id and a conclusion matching the expected result, or the mismatch is explained and either fixed (D-4) or recorded as the paper branch's item | D-1 read against `gh run view <id>` |
| R-2 | No run tags, publishes, deploys or opens an issue | `gh release list`, `git ls-remote --tags`, `gh issue list` before and after, unchanged |
| R-3 | The browser pass covers every mode, page, width and scheme of G8 | the capture names enumerate the grid; the console read for each |
| R-4 | After G9, `uv run pytest -q tests/test_ci_shards.py tests/test_interface_contract.py`, lint, format and the fast suite pass; a push to `dev` runs the fast shard and lint | the commands; the first run on `dev` after the push |
| R-5 | No attribution line; no metanarration in the record; the `qc/**` branches gone | the grep; a read; `git ls-remote --heads origin 'qc/*'` empty |

## Definition of good

Every path of both models exercised on a hosted runner before the first merge, with the evidence in the record, so
that WP68's merge is the first live run of a flow already seen green, and its failure paths seen to stop where they
should.

## Definition of good enough

R-1 to R-5 met; the driver's acceptance as proxy; the record ready for his read.

## Definition of done

Good enough met; WP68's pull request opened on his word with D-1 cited in the release issue.

## Open decisions

None for the scope. Two things the runs may raise are his: a hosted-runner failure the build units cannot fix
without a design change (an amendment to `WP65-design/specification.md`), and the residual baseline retake, which is
the paper branch's.

## Agent's defaults

- One unit for the runs and the browser pass (G1 to G8), run by the driver or a unit in a worktree on `dev`'s head;
  G9 a second, small unit on `test.yml`, `tests/test_ci_shards.py` and the contract, landed before the dry run so
  the dry run exercises the final file.
- `qc/release-fail` and `qc/paper/broken` carry one commit each on top of `dev`'s head, never merged.
- The temporary mode files for the browser pass use `doi = "10.5281/zenodo.123"` and the artefact's real
  `sha256`; the fallback case alters one hex digit.

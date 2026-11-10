# WP25 — Inventory (third instance, at the head after OD2's deletion; first written at `dev` de3ce61)

One row per tracked file outside the live set (A1), each with one disposition: keep (its reader named), delete (what
the content no longer did; the same line is in the deletion commit's message), or hold (the package it waits for and
the instance that then acts). Rewritten per instance (A3); the first instance's inventory (346 rows) is at `db150fc`
and the second's (198 rows) at `ca6ce94`, in git.

**The live set (A1), with this instance's package list (A2).** The pages of `mkdocs.yml`'s navigation; `README.md`,
`site/index.html`, `CLAUDE.md`, `glossary.yaml`, `claims_register.toml`; everything under `src/`, `tests/`, `scripts/`,
`derivation/`, `paper/`, `examples/adcs/`, `docs/superpowers/specs/`; the notes `CLAUDE.md` and `PM-BRIEF.md` name;
`work-packages/{README,PM-BRIEF,release-candidate,parallel-board,driver-log,release-punch-list,swap-evidence,
interface-contract}.*`; the scope, decisions and review of every package not yet accepted (WP8a, WP8b, WP10, WP11,
WP12, WP15, WP16, WP17, WP18, WP19, WP20, WP21, WP22, WP25, WP26, WP27: WP23 and WP24 left the list, accepted; WP26 and
WP27 joined); and this inventory. 284 paths (`docs/generated/glossary.md` is in the navigation but generated, not
tracked; `v1-v2-comparison.md` left the set when deleted). Tracked files at the head: 492; rows below: 209.

**The command (A2), run at the repository root; it prints one line per row: path, live files naming the path, live
files naming only the basename.** Rerun at the head and diff the first column against the table under "Rows" (R-1).

```sh
{
  grep -oE '[A-Za-z0-9_./-]+\.md' mkdocs.yml | sed 's|^|docs/|'
  printf '%s\n' README.md site/index.html CLAUDE.md glossary.yaml claims_register.toml
  git ls-files src tests scripts derivation paper examples/adcs docs/superpowers/specs
  grep -ohE 'docs/superpowers/notes/[A-Za-z0-9_./-]+\.md' CLAUDE.md work-packages/PM-BRIEF.md
  git ls-files 'work-packages/README.*' 'work-packages/PM-BRIEF.*' 'work-packages/release-candidate.*' \
    'work-packages/parallel-board.*' 'work-packages/driver-log.*' 'work-packages/release-punch-list.*' \
    'work-packages/swap-evidence.*' 'work-packages/interface-contract.*'
  for p in WP8a WP8b WP10 WP11 WP12 WP15 WP16 WP17 WP18 WP19 WP20 WP21 WP22 WP25 WP26 WP27; do
    git ls-files "work-packages/$p-scope-of-work.md" "work-packages/$p-decisions.md" "work-packages/$p-review.md"
  done
  echo work-packages/WP25-inventory.md
} | sort -u > "${LIVE:=/tmp/wp25-live.txt}"
git ls-files | sort | comm -23 - "$LIVE" | while IFS= read -r f; do
  b=$(basename "$f")
  byp=$(git grep -l -F -e "$f" -- $(cat "$LIVE") | tr '\n' ' ')
  byb=$(git grep -l -F -e "$b" -- $(cat "$LIVE") | tr '\n' ' ')
  printf '%s\t%s\t%s\n' "$f" "${byp:-nothing}" "${byb:-nothing}"
done
```

**Triage by hand (A2).** What decided the rows this instance changed or re-read:

- `docs/superpowers/notes/spike-ternary/report.md` went (OD1 (b), `WP25-decisions.md`, "Instance 3"): the register's
  C001 note and `claims-review.md` line 74 dropped the 0.071 sentence first (6e34f2b), then the file was deleted in
  de3ce61 ("WP25: 1 file deleted (third instance)"); its last version is at b555be7. The records that cite it
  (`WP18-scope-of-work.md`, `WP8a-decisions.md`) keep the name, which now points into history.
- `examples/adcs/experiments/reports/v1-v2-comparison.md` went (OD2 (b)), in a second deletion commit of this
  instance. The scope's sizing said "read by no test or page", but `tests/test_v2_data.py` read the committed file
  through `cmp.REPORT` (a reference neither the path grep nor the basename grep sees) and failed without it; the PM
  ruled (OD2 closed by option (a) of the executor's report) that the driver's decision changed the requirement that test
  pinned, so the test now regenerates the comparison to a temporary path and checks the same content
  (`test_the_regenerated_report_includes_the_register`), and the file went in the same push. Its last version is at
  f517875; the hash rows in `paper/container/RECORD.md` and `WP23-rounds/gate/README.md` stay as history (A9);
  `uv run python -m experiments compare` regenerates it. The file was in the live set (`examples/adcs/`), so it was
  not a row; the rows that named it as a reader were rewritten from the command rerun after the deletion.
- `work-packages/WP23-rounds/round-1/generation-ledger.jsonl`, re-read once against @7: it holds the two entries of
  the first v2 generation (`v2-primary`, `v2-baseline`; `round-1/README.md` names it as the ledger of the run);
  rounds 2 to 4 regenerated nothing (`round-4/README.md`); the data of record is the @7 entries of
  `examples/adcs/experiments/ledger/ledger.jsonl` (49 entries), regenerated at the close-out on the host, and descends
  from that run. Keep: the cited ancestor of the data of record.
- The 16 files under `work-packages/WP11-round-1/round2-reads/` and `round2-docs-reads/` (round 2's raw reader reports
  and the task readers' reports, 31fedfc and fdab633; triaged at e76f520 and 308dc5a) are WP11's (Non-goals): hold,
  WP11's acceptance or the next instance, as round 1's raw reports went after triage.
- The 33 WP26 files (two records and 31 screenshots under `WP26-view-editor-feedback/`) and the 10 WP27 screenshots
  under `WP27-review/` are running packages' (Non-goals): hold, their acceptance or the next instance. The 41
  screenshots are the rows named by nothing in the live set; the reports name the views they show, not the files.
- `docs/superpowers/notes/view-editor-harness.md` is WP26's note (Non-goals): keep, read by `WP26-decisions.md`,
  `WP27-scope-of-work.md` and `parallel-board.md`.

**Counts.** 209 rows: 148 keep, 61 hold, 0 delete at the head (the instance's two deleted files,
`spike-ternary/report.md` and OD2's `v1-v2-comparison.md`, are gone and so no longer rows). Held rows: 16 of WP11, 33 of WP26, 10 of WP27,
`search-prior-art.md` (WP12), `streams/P10-review.md` (WP10's acceptance).

## Contract and tests (R-2): the grep before any file goes

For every delete row, and for OD2's file: `git grep -n -F -e <path> -e <basename> -- work-packages/interface-contract.md
work-packages/interface-contract.toml tests/test_interface_contract.py`. Counts of matching lines (0 means no pin):

| File | path | basename | Live surfaces naming the path (`git grep -l -F <path> -- . ':!work-packages/WP25-*'`) |
|---|---|---|---|
| `docs/superpowers/notes/spike-ternary/report.md` (deleted, de3ce61) | 0 | 0 | `docs/superpowers/notes/claims-review.md` (re-pointed in 6e34f2b); `work-packages/WP18-scope-of-work.md`, `work-packages/WP8a-decisions.md` (records, kept). The basename `report.md` hits elsewhere are other files (`spike-ggp-fit`, `spike-container-platform`, the tests' temporary output) |
| `examples/adcs/experiments/reports/v1-v2-comparison.md` (OD2 (b); deleted in the second deletion commit) | 0 | 0 | `paper/container/RECORD.md`, `work-packages/WP23-rounds/gate/README.md` (the hash rows), `WP10-decisions.md`, `WP15-scope-of-work.md`, `WP23-review.md`, `driver-log.md`, `swap-evidence.md`, `streams/P10-review.md` (records); by basename `examples/adcs/experiments/compare.py` (the generator's `REPORT`); by neither, `tests/test_v2_data.py` (`cmp.REPORT`; the test now regenerates the report, same push) |

## Rows

| Path | Disposition | Reader, or what it waits for |
|---|---|---|
| `.dockerignore` | keep | `tests/test_container.py`; the container build |
| `.github/workflows/pages.yml` | keep | the Pages deployment (`tests/test_site.py`) |
| `.github/workflows/test.yml` | keep | CI (`tests/test_ci_shards.py`) |
| `.gitignore` | keep | `tests/test_interface_contract.py`, `tests/test_paper.py` |
| `.python-version` | keep | `CLAUDE.md`; uv and CI read it |
| `CHANGELOG.md` | keep | the release notes (WP8b's deliverable); read by `tests/test_release_hygiene.py` |
| `Dockerfile` | keep | `paper/container/build.sh`, `paper/container/README.md` |
| `LICENSE` | keep | the licence file (`pyproject.toml`, the distribution) |
| `docs/references.bib` | keep | `tests/test_references.py`, the paper and docs bibliography |
| `docs/ruff.toml` | keep | `tests/test_site.py`: lints the docs code cells |
| `docs/stylesheets/extra.css` | keep | `mkdocs.yml` (the site theme) |
| `docs/superpowers/notes/abstraction-gaps.md` | keep | `claims_register.toml`, `docs/superpowers/notes/proof-conventions.md`, the case study |
| `docs/superpowers/notes/adcs-port.md` | keep | the design spec |
| `docs/superpowers/notes/adcs-tensions-probe.md` | keep | `examples/adcs/cubesat_model.py`, the case study experiments |
| `docs/superpowers/notes/notation.md` | keep | `glossary.yaml`, `tests/test_docs.py`, `paper/supporting_material.ipynb` |
| `docs/superpowers/notes/opensysml-usage.md` | keep | `examples/adcs/experiments/probes/probe-record.md` |
| `docs/superpowers/notes/paper-appendices-sketch.md` | keep | the result is not in a decision record: `WP10-decisions.md` points to it as the sketch (the three tiers per appendix) and `WP10-scope-of-work.md` Amendment 1 and `WP10-review-2.md` name it as their source. Reader: those records |
| `docs/superpowers/notes/paper-outline-v1-baseline.md` | keep | the result is not in a decision record: `WP10-decisions.md` only names it the baseline; `paper-outline-v2-search.md` says it "supersedes ... kept as the baseline" and `paper-prior-art-sources.md` cites its addendum for the contrast and the points of comparison (twice). Reader: those two notes |
| `docs/superpowers/notes/paper-outline-v2-search.md` | keep | `work-packages/README.md`, `WP10-decisions.md`; WP12 reads it |
| `docs/superpowers/notes/paper-prior-art-sources.md` | keep | `paper/prior_art.yaml`, `tests/test_references.py` |
| `docs/superpowers/notes/paper-sources/README.md` | keep | the paper's source notes: `CLAUDE.md`, `README.md`, `claims_register.toml` (+29) |
| `docs/superpowers/notes/paper-sources/api.md` | keep | the paper's source notes: `claims_register.toml`, `docs/api-reference.md`, `docs/index.md` (+13) |
| `docs/superpowers/notes/paper-sources/limitations.md` | keep | the paper's source notes: `claims_register.toml`, `docs/theory.md`, `docs/user-guide/overview.md` (+11) |
| `docs/superpowers/notes/paper-sources/literature.md` | keep | the paper's source notes: `claims_register.toml`, `paper/supporting_material.ipynb` |
| `docs/superpowers/notes/paper-sources/method.md` | keep | the paper's source notes: `work-packages/WP24-decisions.md` |
| `docs/superpowers/notes/paper-sources/preconditioning.md` | keep | the paper's source notes: `docs/superpowers/specs/2026-11-07-posynomial-invariant-form-design.md`, `tests/test_paper_sources.py`, `work-packages/README.md` (+4) |
| `docs/superpowers/notes/paper-sources/why-and-how.md` | keep | the paper's source notes: `tests/test_narrative.py`, `tests/test_paper_sources.py`, `work-packages/WP10-scope-of-work.md` (+3) |
| `docs/superpowers/notes/reader-grid.md` | keep | `work-packages/README.md`, the WP11 reader rounds |
| `docs/superpowers/notes/references-verified.md` | keep | `derivation/PROOF_MAP_FINDINGS.md`, `WP17-decisions.md` |
| `docs/superpowers/notes/search-prior-art.md` | hold: WP12 (unscoped) | the result is not in a decision record: `WP12-decisions.md` points to this note for "the explanation back, the prior art and the proof assessment" (the prior-art table with DOIs, the procedure, the low-hanging proofs L11 to L14, I6, I7, T1), and WP12 has no scope yet to carry them. Delete when WP12 records them or is dropped |
| `docs/superpowers/notes/spike-certificates/README.md` | keep | the README is cited by path from `paper/supporting_material.ipynb`; the script regenerates the spike's outputs (decision of 2026-11-10 07:00) |
| `docs/superpowers/notes/spike-certificates/certificates.py` | keep | the README is cited by path from `paper/supporting_material.ipynb`; the script regenerates the spike's outputs (decision of 2026-11-10 07:00) |
| `docs/superpowers/notes/spike-certificates/check_identities.py` | keep | the README is cited by path from `paper/supporting_material.ipynb`; the script regenerates the spike's outputs (decision of 2026-11-10 07:00) |
| `docs/superpowers/notes/spike-certificates/dup_facets.py` | keep | the README is cited by path from `paper/supporting_material.ipynb`; the script regenerates the spike's outputs (decision of 2026-11-10 07:00) |
| `docs/superpowers/notes/spike-certificates/polish_and_ties.py` | keep | the README is cited by path from `paper/supporting_material.ipynb`; the script regenerates the spike's outputs (decision of 2026-11-10 07:00) |
| `docs/superpowers/notes/spike-certificates/run_cubesat.py` | keep | the README is cited by path from `paper/supporting_material.ipynb`; the script regenerates the spike's outputs (decision of 2026-11-10 07:00) |
| `docs/superpowers/notes/spike-certificates/run_planted.py` | keep | the README is cited by path from `paper/supporting_material.ipynb`; the script regenerates the spike's outputs (decision of 2026-11-10 07:00) |
| `docs/superpowers/notes/spike-certificates/sympy_feasibility.py` | keep | the README is cited by path from `paper/supporting_material.ipynb`; the script regenerates the spike's outputs (decision of 2026-11-10 07:00) |
| `docs/superpowers/notes/spike-container-platform/report.md` | keep | the container platform report: `paper/container/README.md`, `paper/container/RECORD.md`, `claims_register.toml` |
| `docs/superpowers/notes/spike-facet-refit/README.md` | keep | the README is cited by path from `paper/supporting_material.ipynb`; the script regenerates the spike's outputs (decision of 2026-11-10 07:00) |
| `docs/superpowers/notes/spike-facet-refit/bench_cubesat.py` | keep | the README is cited by path from `paper/supporting_material.ipynb`; the script regenerates the spike's outputs (decision of 2026-11-10 07:00) |
| `docs/superpowers/notes/spike-facet-refit/bench_oracle.py` | keep | the README is cited by path from `paper/supporting_material.ipynb`; the script regenerates the spike's outputs (decision of 2026-11-10 07:00) |
| `docs/superpowers/notes/spike-facet-refit/bench_planted.py` | keep | the README is cited by path from `paper/supporting_material.ipynb`; the script regenerates the spike's outputs (decision of 2026-11-10 07:00) |
| `docs/superpowers/notes/spike-facet-refit/bench_restarts.py` | keep | the README is cited by path from `paper/supporting_material.ipynb`; the script regenerates the spike's outputs (decision of 2026-11-10 07:00) |
| `docs/superpowers/notes/spike-facet-refit/methods.py` | keep | the README is cited by path from `paper/supporting_material.ipynb`; the script regenerates the spike's outputs (decision of 2026-11-10 07:00) |
| `docs/superpowers/notes/spike-figure1/README.md` | keep | the generator and README of the paper's Figure 1: `paper/figures/figure1.py`, `CLAUDE.md` |
| `docs/superpowers/notes/spike-figure1/make_schematics.py` | keep | the generator and README of the paper's Figure 1: `paper/figures/figure1.py`, `CLAUDE.md` |
| `docs/superpowers/notes/spike-objective/README.md` | keep | the README is cited by path from `paper/supporting_material.ipynb`; the script regenerates the spike's outputs (decision of 2026-11-10 07:00) |
| `docs/superpowers/notes/spike-objective/bench_ab.py` | keep | the README is cited by path from `paper/supporting_material.ipynb`; the script regenerates the spike's outputs (decision of 2026-11-10 07:00) |
| `docs/superpowers/notes/spike-objective/bench_c.py` | keep | the README is cited by path from `paper/supporting_material.ipynb`; the script regenerates the spike's outputs (decision of 2026-11-10 07:00) |
| `docs/superpowers/notes/spike-objective/bench_cubesat2.py` | keep | the README is cited by path from `paper/supporting_material.ipynb`; the script regenerates the spike's outputs (decision of 2026-11-10 07:00) |
| `docs/superpowers/notes/spike-objective/check_identifiability.py` | keep | the README is cited by path from `paper/supporting_material.ipynb`; the script regenerates the spike's outputs (decision of 2026-11-10 07:00) |
| `docs/superpowers/notes/spike-objective/fail_seeds.py` | keep | the README is cited by path from `paper/supporting_material.ipynb`; the script regenerates the spike's outputs (decision of 2026-11-10 07:00) |
| `docs/superpowers/notes/spike-objective/objectives.py` | keep | the README is cited by path from `paper/supporting_material.ipynb`; the script regenerates the spike's outputs (decision of 2026-11-10 07:00) |
| `docs/superpowers/notes/spike-sysml-diagrams/project.py` | keep | the generator of the model's views: `examples/adcs/case-model.md`, `tests/test_system_model_v2_r1.py` (WP23 is accepted at db59365; the file is read by a test) |
| `docs/superpowers/notes/spike-sysml-diagrams/render.sh` | keep | the render recipe `examples/adcs/case-model.md` names |
| `docs/superpowers/notes/system-model-tidy.md` | keep | `work-packages/README.md` |
| `docs/superpowers/notes/view-editor-harness.md` | keep | WP26's note (Non-goals); read by `work-packages/WP26-decisions.md`, `work-packages/WP27-scope-of-work.md`, `work-packages/parallel-board.md` |
| `mkdocs.yml` | keep | `scripts/assemble_site.py`, `tests/test_site.py` |
| `pyproject.toml` | keep | uv, the build and CI |
| `site/paper/index.html` | keep | the paper placeholder the Pages build stages (`scripts/stage_site.py`, `tests/test_site.py`) |
| `uv.lock` | keep | uv sync --locked; CI |
| `work-packages/WP0-decisions.md` | keep | the record of an accepted package (A1); read by `work-packages/README.md` |
| `work-packages/WP0-review.md` | keep | the record of an accepted package (A1); read by `work-packages/README.md` |
| `work-packages/WP0-scope-of-work.md` | keep | the record of an accepted package (A1); read by `work-packages/README.md` |
| `work-packages/WP1-decisions.md` | keep | the record of an accepted package (A1); read by `work-packages/README.md` |
| `work-packages/WP1-review.md` | keep | the record of an accepted package (A1); read by `work-packages/README.md` |
| `work-packages/WP1-scope-of-work.md` | keep | the record of an accepted package (A1); read by `work-packages/README.md` |
| `work-packages/WP10-claims-review.md` | keep | a record of WP10, WP11, WP14 or WP19 read by `work-packages/WP10-scope-of-work.md`, `work-packages/parallel-board.md` |
| `work-packages/WP10-cold-reads-triage.md` | keep | a record of WP10, WP11, WP14 or WP19 read by `work-packages/driver-log.md`, `work-packages/interface-contract.md` |
| `work-packages/WP10-reading-pass.md` | keep | a record of WP10, WP11, WP14 or WP19 read by `paper/generate_reading_pass.py`, `paper/reading_pass.yaml` |
| `work-packages/WP10-review-2.md` | keep | a record of WP10, WP11, WP14 or WP19 read by `work-packages/README.md`, `work-packages/WP10-decisions.md`, `work-packages/WP10-scope-of-work.md` (+1) |
| `work-packages/WP10-vocabulary-review.md` | keep | a record of WP10, WP11, WP14 or WP19 read by `scripts/vocabulary_baseline.toml`, `work-packages/WP10-scope-of-work.md` (+1) |
| `work-packages/WP11-round-1/round2-docs-reads/R1.md` | hold: WP11 (running package; next instance) | round 2's raw reader reports (depths B and C, 31fedfc) and the task readers' reports (fdab633), after triage (e76f520, 308dc5a): WP11's (Non-goals); their deletion after triage, as round 1's, is WP11's to decide at its acceptance or the next instance's |
| `work-packages/WP11-round-1/round2-docs-reads/R2.md` | hold: WP11 (running package; next instance) | round 2's raw reader reports (depths B and C, 31fedfc) and the task readers' reports (fdab633), after triage (e76f520, 308dc5a): WP11's (Non-goals); their deletion after triage, as round 1's, is WP11's to decide at its acceptance or the next instance's |
| `work-packages/WP11-round-1/round2-docs-reads/R3.md` | hold: WP11 (running package; next instance) | round 2's raw reader reports (depths B and C, 31fedfc) and the task readers' reports (fdab633), after triage (e76f520, 308dc5a): WP11's (Non-goals); their deletion after triage, as round 1's, is WP11's to decide at its acceptance or the next instance's |
| `work-packages/WP11-round-1/round2-docs-reads/README.md` | hold: WP11 (running package; next instance) | round 2's raw reader reports (depths B and C, 31fedfc) and the task readers' reports (fdab633), after triage (e76f520, 308dc5a): WP11's (Non-goals); their deletion after triage, as round 1's, is WP11's to decide at its acceptance or the next instance's |
| `work-packages/WP11-round-1/round2-reads/P1-B.md` | hold: WP11 (running package; next instance) | round 2's raw reader reports (depths B and C, 31fedfc) and the task readers' reports (fdab633), after triage (e76f520, 308dc5a): WP11's (Non-goals); their deletion after triage, as round 1's, is WP11's to decide at its acceptance or the next instance's |
| `work-packages/WP11-round-1/round2-reads/P1-C.md` | hold: WP11 (running package; next instance) | round 2's raw reader reports (depths B and C, 31fedfc) and the task readers' reports (fdab633), after triage (e76f520, 308dc5a): WP11's (Non-goals); their deletion after triage, as round 1's, is WP11's to decide at its acceptance or the next instance's |
| `work-packages/WP11-round-1/round2-reads/P2-B.md` | hold: WP11 (running package; next instance) | round 2's raw reader reports (depths B and C, 31fedfc) and the task readers' reports (fdab633), after triage (e76f520, 308dc5a): WP11's (Non-goals); their deletion after triage, as round 1's, is WP11's to decide at its acceptance or the next instance's |
| `work-packages/WP11-round-1/round2-reads/P2-C.md` | hold: WP11 (running package; next instance) | round 2's raw reader reports (depths B and C, 31fedfc) and the task readers' reports (fdab633), after triage (e76f520, 308dc5a): WP11's (Non-goals); their deletion after triage, as round 1's, is WP11's to decide at its acceptance or the next instance's |
| `work-packages/WP11-round-1/round2-reads/P3-B.md` | hold: WP11 (running package; next instance) | round 2's raw reader reports (depths B and C, 31fedfc) and the task readers' reports (fdab633), after triage (e76f520, 308dc5a): WP11's (Non-goals); their deletion after triage, as round 1's, is WP11's to decide at its acceptance or the next instance's |
| `work-packages/WP11-round-1/round2-reads/P3-C.md` | hold: WP11 (running package; next instance) | round 2's raw reader reports (depths B and C, 31fedfc) and the task readers' reports (fdab633), after triage (e76f520, 308dc5a): WP11's (Non-goals); their deletion after triage, as round 1's, is WP11's to decide at its acceptance or the next instance's |
| `work-packages/WP11-round-1/round2-reads/P4-B.md` | hold: WP11 (running package; next instance) | round 2's raw reader reports (depths B and C, 31fedfc) and the task readers' reports (fdab633), after triage (e76f520, 308dc5a): WP11's (Non-goals); their deletion after triage, as round 1's, is WP11's to decide at its acceptance or the next instance's |
| `work-packages/WP11-round-1/round2-reads/P5-B.md` | hold: WP11 (running package; next instance) | round 2's raw reader reports (depths B and C, 31fedfc) and the task readers' reports (fdab633), after triage (e76f520, 308dc5a): WP11's (Non-goals); their deletion after triage, as round 1's, is WP11's to decide at its acceptance or the next instance's |
| `work-packages/WP11-round-1/round2-reads/P5-C.md` | hold: WP11 (running package; next instance) | round 2's raw reader reports (depths B and C, 31fedfc) and the task readers' reports (fdab633), after triage (e76f520, 308dc5a): WP11's (Non-goals); their deletion after triage, as round 1's, is WP11's to decide at its acceptance or the next instance's |
| `work-packages/WP11-round-1/round2-reads/P6-B.md` | hold: WP11 (running package; next instance) | round 2's raw reader reports (depths B and C, 31fedfc) and the task readers' reports (fdab633), after triage (e76f520, 308dc5a): WP11's (Non-goals); their deletion after triage, as round 1's, is WP11's to decide at its acceptance or the next instance's |
| `work-packages/WP11-round-1/round2-reads/P6-C.md` | hold: WP11 (running package; next instance) | round 2's raw reader reports (depths B and C, 31fedfc) and the task readers' reports (fdab633), after triage (e76f520, 308dc5a): WP11's (Non-goals); their deletion after triage, as round 1's, is WP11's to decide at its acceptance or the next instance's |
| `work-packages/WP11-round-1/round2-reads/README.md` | hold: WP11 (running package; next instance) | round 2's raw reader reports (depths B and C, 31fedfc) and the task readers' reports (fdab633), after triage (e76f520, 308dc5a): WP11's (Non-goals); their deletion after triage, as round 1's, is WP11's to decide at its acceptance or the next instance's |
| `work-packages/WP11-round-1/triage.md` | keep | a record of WP10, WP11, WP14 or WP19 read by `work-packages/WP19-scope-of-work.md`, `work-packages/WP21-scope-of-work.md`, `work-packages/driver-log.md` (+1) |
| `work-packages/WP13-decisions.md` | keep | the record of an accepted package (A1); read by `work-packages/README.md` |
| `work-packages/WP13-review.md` | keep | the record of an accepted package (A1); read by `work-packages/README.md` |
| `work-packages/WP13-scope-of-work.md` | keep | the record of an accepted package (A1); read by `work-packages/README.md` |
| `work-packages/WP14-decisions.md` | keep | the record of an accepted package (A1); read by `work-packages/WP8a-scope-of-work.md`, `work-packages/interface-contract.md` |
| `work-packages/WP14-review.md` | keep | the record of an accepted package (A1); read by `work-packages/README.md` |
| `work-packages/WP14-scope-of-work.md` | keep | the record of an accepted package (A1); read by `work-packages/README.md` |
| `work-packages/WP19-backlog.md` | keep | a record of WP10, WP11, WP14 or WP19 read by `work-packages/WP10-decisions.md` |
| `work-packages/WP19-figure-review.md` | keep | a record of WP10, WP11, WP14 or WP19 read by `paper/length_ledger.toml`, `work-packages/WP19-scope-of-work.md` |
| `work-packages/WP19-slots.md` | keep | a record of WP10, WP11, WP14 or WP19 read by `work-packages/WP19-scope-of-work.md`, `work-packages/parallel-board.md` |
| `work-packages/WP2-decisions.md` | keep | the record of an accepted package (A1); read by `work-packages/README.md` |
| `work-packages/WP2-review.md` | keep | the record of an accepted package (A1); read by `work-packages/README.md` |
| `work-packages/WP2-scope-of-work.md` | keep | the record of an accepted package (A1); read by `work-packages/README.md` |
| `work-packages/WP23-closeout-scope-of-work.md` | keep | the record of an accepted package (A1); read by `examples/adcs/experiments/reports/change-register.md`, `examples/adcs/model_v2/cubesat.sysml` (+7) |
| `work-packages/WP23-decisions.md` | keep | the record of an accepted package (A1); read by `examples/adcs/model_v2/ledger_gate.py` |
| `work-packages/WP23-review.md` | keep | the record of an accepted package (A1); read by `examples/adcs/model_v2/coverage.py` |
| `work-packages/WP23-rounds/gate/README.md` | keep | the gate's record (`WP23-rounds/gate/README.md`, the data gate): `examples/adcs/experiments/reports/change-register.md`, `paper/container/RECORD.md` (+1) |
| `work-packages/WP23-rounds/gate/coverage.md` | keep | the gate's record (`WP23-rounds/gate/README.md`, the data gate): `examples/adcs/case-model.md`, `examples/adcs/model_v2/coverage.py`, `examples/adcs/model_v2/diagnostic_pair.py` (+6) |
| `work-packages/WP23-rounds/gate/heatmap.png` | keep | the gate's record (`WP23-rounds/gate/README.md`, the data gate): `examples/adcs/model_v2/diagnostic_pair.py`, `tests/test_diagnostic_pair.py`, `work-packages/WP23-review.md` (+2) |
| `work-packages/WP23-rounds/gate/heatmap_baseline.png` | keep | the gate's record (`WP23-rounds/gate/README.md`, the data gate): `examples/adcs/model_v2/diagnostic_pair.py`, `tests/test_diagnostic_pair.py`, `work-packages/WP23-review.md` |
| `work-packages/WP23-rounds/gate/k3_record.md` | keep | the gate's record (`WP23-rounds/gate/README.md`, the data gate): `examples/adcs/case-model.md`, `examples/adcs/model_v2/diagnostic_pair.py` (+4) |
| `work-packages/WP23-rounds/round-1/INTENT.md` | keep | a round record of WP23's cold reads, quoted by `WP23-review.md` and `swap-evidence.md` |
| `work-packages/WP23-rounds/round-1/README.md` | keep | a round record of WP23's cold reads, quoted by `WP23-review.md` and `swap-evidence.md` |
| `work-packages/WP23-rounds/round-1/cold-reads.md` | keep | a round record of WP23's cold reads, quoted by `WP23-review.md` and `swap-evidence.md` |
| `work-packages/WP23-rounds/round-1/coverage.md` | keep | a round record of WP23's cold reads, quoted by `WP23-review.md` and `swap-evidence.md` |
| `work-packages/WP23-rounds/round-1/generation-ledger.jsonl` | keep | the generation ledger of the run that produced the data of record: cited by `round-1/README.md` and `round-4/README.md`; ledgers stay (scope, Non-goals) |
| `work-packages/WP23-rounds/round-1/k3_record.md` | keep | a round record of WP23's cold reads, quoted by `WP23-review.md` and `swap-evidence.md` |
| `work-packages/WP23-rounds/round-2/INTENT.md` | keep | a round record of WP23's cold reads, quoted by `WP23-review.md` and `swap-evidence.md` |
| `work-packages/WP23-rounds/round-3/INTENT.md` | keep | a round record of WP23's cold reads, quoted by `WP23-review.md` and `swap-evidence.md` |
| `work-packages/WP23-rounds/round-3/cold-reads.md` | keep | a round record of WP23's cold reads, quoted by `WP23-review.md` and `swap-evidence.md` |
| `work-packages/WP23-rounds/round-3/coverage.md` | keep | a round record of WP23's cold reads, quoted by `WP23-review.md` and `swap-evidence.md` |
| `work-packages/WP23-rounds/round-3/k3_record.md` | keep | a round record of WP23's cold reads, quoted by `WP23-review.md` and `swap-evidence.md` |
| `work-packages/WP23-rounds/round-4/INTENT.md` | keep | a round record of WP23's cold reads, quoted by `WP23-review.md` and `swap-evidence.md` |
| `work-packages/WP23-rounds/round-4/README.md` | keep | a round record of WP23's cold reads, quoted by `WP23-review.md` and `swap-evidence.md` |
| `work-packages/WP23-rounds/round-4/assembly_caption.md` | keep | a round record of WP23's cold reads, quoted by `WP23-review.md` and `swap-evidence.md` |
| `work-packages/WP23-rounds/round-4/coverage.md` | keep | a round record of WP23's cold reads, quoted by `WP23-review.md` and `swap-evidence.md` |
| `work-packages/WP23-rounds/round-4/k3_record.md` | keep | a round record of WP23's cold reads, quoted by `WP23-review.md` and `swap-evidence.md` |
| `work-packages/WP23-rounds/spike-redundancy.md` | keep | the close-out's record: `examples/adcs/case-model.md`, `examples/adcs/case.py`, `work-packages/interface-contract.md`; `spike-B` is named by `WP23-closeout-scope-of-work.md`, `spike-redundancy.md` by `case-model.md` and contract row 15 |
| `work-packages/WP23-rounds/spikes/spike-A-with-and-without-infeasible.md` | keep | the close-out's record: `claims_register.toml`; `spike-B` is named by `WP23-closeout-scope-of-work.md`, `spike-redundancy.md` by `case-model.md` and contract row 15 |
| `work-packages/WP23-rounds/spikes/spike-B-requirements-and-the-fit.md` | keep | the close-out's record: `tests/test_case.py`; `spike-B` is named by `WP23-closeout-scope-of-work.md`, `spike-redundancy.md` by `case-model.md` and contract row 15 |
| `work-packages/WP23-scope-of-work.md` | keep | the record of an accepted package (A1); read by `examples/adcs/case-model.md` |
| `work-packages/WP24-decisions.md` | keep | the record of an accepted package (A1); read by `work-packages/interface-contract.md` |
| `work-packages/WP24-review.md` | keep | the record of an accepted package (A1); read by `paper/container/RECORD.md`, `work-packages/parallel-board.md` |
| `work-packages/WP24-scope-of-work.md` | keep | the record of an accepted package (A1); read by `paper/length_ledger.toml`, `work-packages/interface-contract.md` |
| `work-packages/WP25-2-scope-of-work.md` | keep | this instance's scope (an unaccepted package's record, A1) |
| `work-packages/WP25-3-scope-of-work.md` | keep | this instance's scope (a record; `WP25-decisions.md`, "Instance 3", names it) |
| `work-packages/WP26-model-changes.md` | hold: WP26 (running package; next instance) | WP26's record, read by `work-packages/WP26-scope-of-work.md`; WP26's (Non-goals) |
| `work-packages/WP26-view-editor-feedback.md` | hold: WP26 (running package; next instance) | WP26's record, read by `work-packages/WP26-decisions.md`, `work-packages/WP26-scope-of-work.md`, `work-packages/WP27-scope-of-work.md`; WP26's (Non-goals) |
| `work-packages/WP26-view-editor-feedback/assembly-tall-column.jpg` | hold: WP26 (running package; next instance) | a screenshot of WP26's view-editor review, named by nothing in the live set (its report names the views, not the files): WP26's (Non-goals); disposition at its acceptance or the next instance |
| `work-packages/WP26-view-editor-feedback/case-no-renderer.jpg` | hold: WP26 (running package; next instance) | a screenshot of WP26's view-editor review, named by nothing in the live set (its report names the views, not the files): WP26's (Non-goals); disposition at its acceptance or the next instance |
| `work-packages/WP26-view-editor-feedback/cold-base-applied.jpg` | hold: WP26 (running package; next instance) | a screenshot of WP26's view-editor review, named by nothing in the live set (its report names the views, not the files): WP26's (Non-goals); disposition at its acceptance or the next instance |
| `work-packages/WP26-view-editor-feedback/cold-case-filter.jpg` | hold: WP26 (running package; next instance) | a screenshot of WP26's view-editor review, named by nothing in the live set (its report names the views, not the files): WP26's (Non-goals); disposition at its acceptance or the next instance |
| `work-packages/WP26-view-editor-feedback/cold-explorer-menu.jpg` | hold: WP26 (running package; next instance) | a screenshot of WP26's view-editor review, named by nothing in the live set (its report names the views, not the files): WP26's (Non-goals); disposition at its acceptance or the next instance |
| `work-packages/WP26-view-editor-feedback/cold-expose-filtered.jpg` | hold: WP26 (running package; next instance) | a screenshot of WP26's view-editor review, named by nothing in the live set (its report names the views, not the files): WP26's (Non-goals); disposition at its acceptance or the next instance |
| `work-packages/WP26-view-editor-feedback/cold-expose-star.jpg` | hold: WP26 (running package; next instance) | a screenshot of WP26's view-editor review, named by nothing in the live set (its report names the views, not the files): WP26's (Non-goals); disposition at its acceptance or the next instance |
| `work-packages/WP26-view-editor-feedback/cold-expose-tree.jpg` | hold: WP26 (running package; next instance) | a screenshot of WP26's view-editor review, named by nothing in the live set (its report names the views, not the files): WP26's (Non-goals); disposition at its acceptance or the next instance |
| `work-packages/WP26-view-editor-feedback/cold-inherited-dup.jpg` | hold: WP26 (running package; next instance) | a screenshot of WP26's view-editor review, named by nothing in the live set (its report names the views, not the files): WP26's (Non-goals); disposition at its acceptance or the next instance |
| `work-packages/WP26-view-editor-feedback/cold-inherited-parts.jpg` | hold: WP26 (running package; next instance) | a screenshot of WP26's view-editor review, named by nothing in the live set (its report names the views, not the files): WP26's (Non-goals); disposition at its acceptance or the next instance |
| `work-packages/WP26-view-editor-feedback/cold-owned-dup.jpg` | hold: WP26 (running package; next instance) | a screenshot of WP26's view-editor review, named by nothing in the live set (its report names the views, not the files): WP26's (Non-goals); disposition at its acceptance or the next instance |
| `work-packages/WP26-view-editor-feedback/cold-recovery-restore.jpg` | hold: WP26 (running package; next instance) | a screenshot of WP26's view-editor review, named by nothing in the live set (its report names the views, not the files): WP26's (Non-goals); disposition at its acceptance or the next instance |
| `work-packages/WP26-view-editor-feedback/concern-view-no-values.jpg` | hold: WP26 (running package; next instance) | a screenshot of WP26's view-editor review, named by nothing in the live set (its report names the views, not the files): WP26's (Non-goals); disposition at its acceptance or the next instance |
| `work-packages/WP26-view-editor-feedback/configurations-bare.jpg` | hold: WP26 (running package; next instance) | a screenshot of WP26's view-editor review, named by nothing in the live set (its report names the views, not the files): WP26's (Non-goals); disposition at its acceptance or the next instance |
| `work-packages/WP26-view-editor-feedback/configurations-overview.jpg` | hold: WP26 (running package; next instance) | a screenshot of WP26's view-editor review, named by nothing in the live set (its report names the views, not the files): WP26's (Non-goals); disposition at its acceptance or the next instance |
| `work-packages/WP26-view-editor-feedback/duplicate-inherited-member.jpg` | hold: WP26 (running package; next instance) | a screenshot of WP26's view-editor review, named by nothing in the live set (its report names the views, not the files): WP26's (Non-goals); disposition at its acceptance or the next instance |
| `work-packages/WP26-view-editor-feedback/duplicate-owned-member.jpg` | hold: WP26 (running package; next instance) | a screenshot of WP26's view-editor review, named by nothing in the live set (its report names the views, not the files): WP26's (Non-goals); disposition at its acceptance or the next instance |
| `work-packages/WP26-view-editor-feedback/expose-overview-tree.jpg` | hold: WP26 (running package; next instance) | a screenshot of WP26's view-editor review, named by nothing in the live set (its report names the views, not the files): WP26's (Non-goals); disposition at its acceptance or the next instance |
| `work-packages/WP26-view-editor-feedback/expose-star-imports.jpg` | hold: WP26 (running package; next instance) | a screenshot of WP26's view-editor review, named by nothing in the live set (its report names the views, not the files): WP26's (Non-goals); disposition at its acceptance or the next instance |
| `work-packages/WP26-view-editor-feedback/inherited-parts-missing.jpg` | hold: WP26 (running package; next instance) | a screenshot of WP26's view-editor review, named by nothing in the live set (its report names the views, not the files): WP26's (Non-goals); disposition at its acceptance or the next instance |
| `work-packages/WP26-view-editor-feedback/matrix-concern-rows.jpg` | hold: WP26 (running package; next instance) | a screenshot of WP26's view-editor review, named by nothing in the live set (its report names the views, not the files): WP26's (Non-goals); disposition at its acceptance or the next instance |
| `work-packages/WP26-view-editor-feedback/no-add-file.jpg` | hold: WP26 (running package; next instance) | a screenshot of WP26's view-editor review, named by nothing in the live set (its report names the views, not the files): WP26's (Non-goals); disposition at its acceptance or the next instance |
| `work-packages/WP26-view-editor-feedback/recovery-clash-wording.jpg` | hold: WP26 (running package; next instance) | a screenshot of WP26's view-editor review, named by nothing in the live set (its report names the views, not the files): WP26's (Non-goals); disposition at its acceptance or the next instance |
| `work-packages/WP26-view-editor-feedback/recovery-condensed-copy.jpg` | hold: WP26 (running package; next instance) | a screenshot of WP26's view-editor review, named by nothing in the live set (its report names the views, not the files): WP26's (Non-goals); disposition at its acceptance or the next instance |
| `work-packages/WP26-view-editor-feedback/requirements-table.jpg` | hold: WP26 (running package; next instance) | a screenshot of WP26's view-editor review, named by nothing in the live set (its report names the views, not the files): WP26's (Non-goals); disposition at its acceptance or the next instance |
| `work-packages/WP26-view-editor-feedback/requirements-view.jpg` | hold: WP26 (running package; next instance) | a screenshot of WP26's view-editor review, named by nothing in the live set (its report names the views, not the files): WP26's (Non-goals); disposition at its acceptance or the next instance |
| `work-packages/WP26-view-editor-feedback/stale-banner.jpg` | hold: WP26 (running package; next instance) | a screenshot of WP26's view-editor review, named by nothing in the live set (its report names the views, not the files): WP26's (Non-goals); disposition at its acceptance or the next instance |
| `work-packages/WP26-view-editor-feedback/table-concern-rows.jpg` | hold: WP26 (running package; next instance) | a screenshot of WP26's view-editor review, named by nothing in the live set (its report names the views, not the files): WP26's (Non-goals); disposition at its acceptance or the next instance |
| `work-packages/WP26-view-editor-feedback/traceability-satisfaction.jpg` | hold: WP26 (running package; next instance) | a screenshot of WP26's view-editor review, named by nothing in the live set (its report names the views, not the files): WP26's (Non-goals); disposition at its acceptance or the next instance |
| `work-packages/WP26-view-editor-feedback/traceability-verification.jpg` | hold: WP26 (running package; next instance) | a screenshot of WP26's view-editor review, named by nothing in the live set (its report names the views, not the files): WP26's (Non-goals); disposition at its acceptance or the next instance |
| `work-packages/WP26-view-editor-feedback/verification-no-renderer.jpg` | hold: WP26 (running package; next instance) | a screenshot of WP26's view-editor review, named by nothing in the live set (its report names the views, not the files): WP26's (Non-goals); disposition at its acceptance or the next instance |
| `work-packages/WP27-review/01-m0-probe-applied.jpg` | hold: WP27 (running package; next instance) | a screenshot of WP27's view-editor review, named by nothing in the live set (its report names the views, not the files): WP27's (Non-goals); disposition at its acceptance or the next instance |
| `work-packages/WP27-review/02-probeview-expose-star.jpg` | hold: WP27 (running package; next instance) | a screenshot of WP27's view-editor review, named by nothing in the live set (its report names the views, not the files): WP27's (Non-goals); disposition at its acceptance or the next instance |
| `work-packages/WP27-review/03-verify-nested-duplicate-name.jpg` | hold: WP27 (running package; next instance) | a screenshot of WP27's view-editor review, named by nothing in the live set (its report names the views, not the files): WP27's (Non-goals); disposition at its acceptance or the next instance |
| `work-packages/WP27-review/04-probe3-table.jpg` | hold: WP27 (running package; next instance) | a screenshot of WP27's view-editor review, named by nothing in the live set (its report names the views, not the files): WP27's (Non-goals); disposition at its acceptance or the next instance |
| `work-packages/WP27-review/05-stakeholders-duplicate-verify.jpg` | hold: WP27 (running package; next instance) | a screenshot of WP27's view-editor review, named by nothing in the live set (its report names the views, not the files): WP27's (Non-goals); disposition at its acceptance or the next instance |
| `work-packages/WP27-review/06-applied-rev9-clean.jpg` | hold: WP27 (running package; next instance) | a screenshot of WP27's view-editor review, named by nothing in the live set (its report names the views, not the files): WP27's (Non-goals); disposition at its acceptance or the next instance |
| `work-packages/WP27-review/07-matrix-verification-concerns.jpg` | hold: WP27 (running package; next instance) | a screenshot of WP27's view-editor review, named by nothing in the live set (its report names the views, not the files): WP27's (Non-goals); disposition at its acceptance or the next instance |
| `work-packages/WP27-review/08-table-concern-rows.jpg` | hold: WP27 (running package; next instance) | a screenshot of WP27's view-editor review, named by nothing in the live set (its report names the views, not the files): WP27's (Non-goals); disposition at its acceptance or the next instance |
| `work-packages/WP27-review/09-stakeholders-view.jpg` | hold: WP27 (running package; next instance) | a screenshot of WP27's view-editor review, named by nothing in the live set (its report names the views, not the files): WP27's (Non-goals); disposition at its acceptance or the next instance |
| `work-packages/WP27-review/11-satisfaction-matrix-verdicts.jpg` | hold: WP27 (running package; next instance) | a screenshot of WP27's view-editor review, named by nothing in the live set (its report names the views, not the files): WP27's (Non-goals); disposition at its acceptance or the next instance |
| `work-packages/WP3-decisions.md` | keep | the record of an accepted package (A1); read by `work-packages/README.md` |
| `work-packages/WP3-review.md` | keep | the record of an accepted package (A1); read by `work-packages/README.md` |
| `work-packages/WP3-scope-of-work.md` | keep | the record of an accepted package (A1); read by `work-packages/README.md` |
| `work-packages/WP4-decisions.md` | keep | the record of an accepted package (A1); read by `work-packages/README.md` |
| `work-packages/WP4-review.md` | keep | the record of an accepted package (A1); read by `work-packages/README.md` |
| `work-packages/WP4-scope-of-work.md` | keep | the record of an accepted package (A1); read by `work-packages/README.md` |
| `work-packages/WP4b-decisions.md` | keep | the record of an accepted package (A1); read by `tests/test_adcs_enrichment.py` |
| `work-packages/WP4b-review.md` | keep | the record of an accepted package (A1); read by `work-packages/README.md` |
| `work-packages/WP4b-scope-of-work.md` | keep | the record of an accepted package (A1); read by `work-packages/README.md` |
| `work-packages/WP5-decisions.md` | keep | the record of an accepted package (A1); read by `work-packages/README.md` |
| `work-packages/WP5-review.md` | keep | the record of an accepted package (A1); read by `work-packages/README.md` |
| `work-packages/WP5-scope-of-work.md` | keep | the record of an accepted package (A1); read by `work-packages/README.md` |
| `work-packages/WP6-decisions.md` | keep | the record of an accepted package (A1); read by `work-packages/README.md` |
| `work-packages/WP6-review.md` | keep | the record of an accepted package (A1); read by `work-packages/README.md` |
| `work-packages/WP6-scope-of-work.md` | keep | the record of an accepted package (A1); read by `work-packages/README.md` |
| `work-packages/WP7-decisions.md` | keep | the record of an accepted package (A1); read by `work-packages/README.md` |
| `work-packages/WP7-review.md` | keep | the record of an accepted package (A1); read by `work-packages/README.md` |
| `work-packages/WP7-scope-of-work.md` | keep | the record of an accepted package (A1); read by `work-packages/README.md` |
| `work-packages/WP8-decisions.md` | keep | the record of an accepted package (A1); read by `work-packages/README.md`, `work-packages/WP8a-decisions.md`, `work-packages/WP8a-scope-of-work.md` (+1) |
| `work-packages/WP8-scope-of-work.md` | keep | the record of an accepted package (A1); read by `work-packages/README.md` |
| `work-packages/WP8a-driver-browser-pass.md` | keep | the record of an accepted package (A1); read by `work-packages/README.md`, `work-packages/WP8a-decisions.md`, `work-packages/driver-log.md` |
| `work-packages/WP8a-figure-review.md` | keep | the record of an accepted package (A1); read by `work-packages/parallel-board.md` |
| `work-packages/WP8a-review-amendment2.md` | keep | the record of an accepted package (A1); read by `work-packages/README.md` |
| `work-packages/WP9-decisions.md` | keep | the record of an accepted package (A1); read by `work-packages/README.md`, `work-packages/WP10-decisions.md` |
| `work-packages/WP9-review.md` | keep | the record of an accepted package (A1); read by `paper/supporting_material.ipynb` |
| `work-packages/WP9-scope-of-work.md` | keep | the record of an accepted package (A1); read by `work-packages/README.md`, `work-packages/WP10-decisions.md` |
| `work-packages/external-assessment-2026-11-09/assessment.md` | keep | `paper/supporting_material.ipynb`, `WP21-scope-of-work.md` |
| `work-packages/external-assessment-2026-11-09/triage.md` | keep | the triage of the outside assessment: `WP21-scope-of-work.md`, `WP19-scope-of-work.md` |
| `work-packages/external-assessment-2026-11-09/verification.json` | keep | `assessment.md` (cited by `paper/supporting_material.ipynb`) sends its reader to this file for "exact outcomes and numerical comparisons"; `WP21-scope-of-work.md` lists it as evidence; 2.6 kB; deleting leaves a cited document with a dangling pointer. Revisit when `assessment.md` goes |
| `work-packages/external-review-2026-11.md` | keep | the outside review the abstraction-gaps ledger cites (E-10): `WP10-decisions.md`, `work-packages/README.md` |
| `work-packages/streams/P10-review.md` | hold: WP10 acceptance | named by no file (`WP10-decisions.md` mentions P10); folded into `WP10-review.md` or deleted when WP10 is finally accepted (WP10 is a working draft) |

Every row above carries one disposition; the R-1 grep over this file returns 0. The 18 rows that named the deleted
`v1-v2-comparison.md` as a reader now name their other readers, as the command rerun after the deletion lists them.

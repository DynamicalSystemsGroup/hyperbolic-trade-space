# WP25 — Inventory (second instance, at `dev` a9e23b2)

One row per tracked file outside the live set (A1), each with one disposition: keep (its reader named), delete (what
the content no longer did; the same line is in the deletion commit's message), or hold (what it waits for and who
then acts). Rewritten per instance (A3); the first instance's inventory (346 rows) is at `db150fc`, in git.

**The live set (A1), unchanged.** The pages of `mkdocs.yml`'s navigation; `README.md`, `site/index.html`, `CLAUDE.md`,
`glossary.yaml`, `claims_register.toml`; everything under `src/`, `tests/`, `scripts/`, `derivation/`, `paper/`,
`examples/adcs/`, `docs/superpowers/specs/`; the notes `CLAUDE.md` and `PM-BRIEF.md` name; `work-packages/{README,
PM-BRIEF,release-candidate,parallel-board,driver-log,release-punch-list,swap-evidence,interface-contract}.*`; and the
scope, decisions and review of every package not yet accepted (WP8a, WP8b, WP10, WP11, WP12, WP15, WP16, WP17, WP18,
WP19, WP20, WP21, WP22, WP23, WP24, WP25; the list is the command's); and this inventory. 285 paths, 284 tracked
(`docs/generated/glossary.md` is in the navigation but generated, not tracked). Tracked files at the head: 482; rows
below: 198.

**The command (A2), run at the repository root; it prints one line per row: path, live files naming the path, live
files naming only the basename.** Rerun at the head and diff the first column against this table (R-1).

```sh
{
  grep -oE '[A-Za-z0-9_./-]+\.md' mkdocs.yml | sed 's|^|docs/|'
  printf '%s\n' README.md site/index.html CLAUDE.md glossary.yaml claims_register.toml
  git ls-files src tests scripts derivation paper examples/adcs docs/superpowers/specs
  grep -ohE 'docs/superpowers/notes/[A-Za-z0-9_./-]+\.md' CLAUDE.md work-packages/PM-BRIEF.md
  git ls-files 'work-packages/README.*' 'work-packages/PM-BRIEF.*' 'work-packages/release-candidate.*' \
    'work-packages/parallel-board.*' 'work-packages/driver-log.*' 'work-packages/release-punch-list.*' \
    'work-packages/swap-evidence.*' 'work-packages/interface-contract.*'
  for p in WP8a WP8b WP10 WP11 WP12 WP15 WP16 WP17 WP18 WP19 WP20 WP21 WP22 WP23 WP24 WP25; do
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

**Triage by hand (A2).** What decided the rows the command lets through with a live reader:

- The 30 `WP23-rounds` images (rounds 1 to 4: `assembly_view`/`behavioural_view` `.png .puml .svg`, `heatmap.png`,
  `heatmap_stock.png`, `heatmap_baseline.png`) go: WP23 is accepted at db59365; no markdown embeds or links any of them
  (`git grep -E '!\[[^]]*\]\([^)]*\.(png|svg)' -- work-packages` returns nothing), the round records name them in
  backticks as what the readers saw and quote the reading, the live views are `examples/adcs/model_v2/views/`
  (revision 8) and the gate's pair is `WP23-rounds/gate/`, and `diagnostic_pair.py` and `project.py` regenerate both.
  `tests/test_diagnostic_pair.py` and `tests/test_system_model_v2_r1.py` write to a temporary directory and to
  `model_v2/views/`; none reads `WP23-rounds/`. The round records keep the names; the names now point into history
  (last version at a9e23b2).
- `WP23-rounds/round-1/generation-ledger.jsonl` stays: it is the ledger of the run that produced the data of record
  (cited by `round-1/README.md` and `round-4/README.md`); the scope keeps ledgers.
- `WP10-cold-reads.md` goes (the raw reports; the triage and the review keep the findings). Its other namers are
  records (`work-packages/README.md` row for WP10, `WP10-decisions.md`, `WP10-review-2.md`, `WP11-decisions.md`,
  `driver-log.md`, `WP10-cold-reads-triage.md`); the README row is reworded to say the file is deleted.
- `external-assessment-2026-11-09/verification.json` stays: the kept `assessment.md`, which the supporting notebook
  cites, tells its reader to see it for the exact outcomes.
- The three notes `search-prior-art.md`, `paper-outline-v1-baseline.md`, `paper-appendices-sketch.md` stay: the decision
  records name them as where the result lives and do not hold it (rows say which text points where).
- The spike outputs (26 `.txt` and `.csv` files of `spike-certificates`, `spike-facet-refit`, `spike-objective`) wait for
  the paper unit to re-point the notebook's and `generate_results.py`'s citations; the 20 READMEs and generators stay.
- `spike-ternary/report.md` waits for WP24 to move its two glossary entries and the register row.
- Not rows (inside the live set): `scripts/rename_facet.py`, `tests/test_rename_facet.py` and their line in
  `scripts/check.py`'s map: hold, WP24's last push, then delete in the instance's later unit.

**Counts.** 198 rows: 138 keep, 31 delete, 29 hold. Held rows: 26 spike outputs (paper unit),
`spike-ternary/report.md` (WP24), `search-prior-art.md` (WP12), `P10-review.md` (WP10 acceptance).

## Contract and tests (R-2): the grep before any file goes

For every delete row: `git grep -n -F <path> -- work-packages/interface-contract.md work-packages/interface-contract.toml tests/test_interface_contract.py`
and the same with the basename. Counts of matching lines (0 means no pin):

| Delete row | path | basename |
|---|---|---|
| `work-packages/WP10-cold-reads.md` | 0 | 0 |
| `work-packages/WP23-rounds/round-1/assembly_view.png` | 0 | 0 |
| `work-packages/WP23-rounds/round-1/assembly_view.puml` | 0 | 0 |
| `work-packages/WP23-rounds/round-1/assembly_view.svg` | 0 | 0 |
| `work-packages/WP23-rounds/round-1/behavioural_view.png` | 0 | 0 |
| `work-packages/WP23-rounds/round-1/behavioural_view.puml` | 0 | 0 |
| `work-packages/WP23-rounds/round-1/behavioural_view.svg` | 0 | 0 |
| `work-packages/WP23-rounds/round-1/heatmap.png` | 0 | 0 |
| `work-packages/WP23-rounds/round-1/heatmap_stock.png` | 0 | 0 |
| `work-packages/WP23-rounds/round-2/assembly_view.png` | 0 | 0 |
| `work-packages/WP23-rounds/round-2/assembly_view.puml` | 0 | 0 |
| `work-packages/WP23-rounds/round-2/assembly_view.svg` | 0 | 0 |
| `work-packages/WP23-rounds/round-2/behavioural_view.png` | 0 | 0 |
| `work-packages/WP23-rounds/round-2/behavioural_view.puml` | 0 | 0 |
| `work-packages/WP23-rounds/round-2/behavioural_view.svg` | 0 | 0 |
| `work-packages/WP23-rounds/round-3/assembly_view.png` | 0 | 0 |
| `work-packages/WP23-rounds/round-3/assembly_view.puml` | 0 | 0 |
| `work-packages/WP23-rounds/round-3/assembly_view.svg` | 0 | 0 |
| `work-packages/WP23-rounds/round-3/behavioural_view.png` | 0 | 0 |
| `work-packages/WP23-rounds/round-3/behavioural_view.puml` | 0 | 0 |
| `work-packages/WP23-rounds/round-3/behavioural_view.svg` | 0 | 0 |
| `work-packages/WP23-rounds/round-3/heatmap.png` | 0 | 0 |
| `work-packages/WP23-rounds/round-3/heatmap_stock.png` | 0 | 0 |
| `work-packages/WP23-rounds/round-4/assembly_view.png` | 0 | 0 |
| `work-packages/WP23-rounds/round-4/assembly_view.puml` | 0 | 0 |
| `work-packages/WP23-rounds/round-4/assembly_view.svg` | 0 | 0 |
| `work-packages/WP23-rounds/round-4/behavioural_view.png` | 0 | 0 |
| `work-packages/WP23-rounds/round-4/behavioural_view.puml` | 0 | 0 |
| `work-packages/WP23-rounds/round-4/behavioural_view.svg` | 0 | 0 |
| `work-packages/WP23-rounds/round-4/heatmap.png` | 0 | 0 |
| `work-packages/WP23-rounds/round-4/heatmap_baseline.png` | 0 | 0 |

## Rows

| Path | Disposition | Reader, or what it waits for, or what it no longer did | Whole-tree grep before deletion (outside this package's records) |
|---|---|---|---|
| `.dockerignore` | keep | `tests/test_container.py`; the container build |  |
| `.github/workflows/pages.yml` | keep | the Pages deployment (`tests/test_site.py`) |  |
| `.github/workflows/test.yml` | keep | CI (`tests/test_ci_shards.py`) |  |
| `.gitignore` | keep | `tests/test_interface_contract.py`, `tests/test_paper.py` |  |
| `.python-version` | keep | `CLAUDE.md`; uv and CI read it |  |
| `CHANGELOG.md` | keep | the release notes; `scripts/rename_facet.py` and WP24 name it (WP24 surface) |  |
| `Dockerfile` | keep | `paper/container/build.sh`, `paper/container/README.md` |  |
| `LICENSE` | keep | the licence file (`pyproject.toml`, the distribution) |  |
| `docs/references.bib` | keep | `tests/test_references.py`, the paper and docs bibliography |  |
| `docs/ruff.toml` | keep | `tests/test_site.py`: lints the docs code cells |  |
| `docs/stylesheets/extra.css` | keep | `mkdocs.yml` (the site theme) |  |
| `docs/superpowers/notes/abstraction-gaps.md` | keep | `claims_register.toml`, `docs/superpowers/notes/proof-conventions.md`, the case study |  |
| `docs/superpowers/notes/adcs-port.md` | keep | the design spec |  |
| `docs/superpowers/notes/adcs-tensions-probe.md` | keep | `examples/adcs/cubesat_model.py`, the case study experiments |  |
| `docs/superpowers/notes/k3-cubesat.md` | keep | `paper/supporting_material.ipynb`, the tests |  |
| `docs/superpowers/notes/notation.md` | keep | `glossary.yaml`, `tests/test_docs.py`, `paper/supporting_material.ipynb` |  |
| `docs/superpowers/notes/opensysml-usage.md` | keep | `examples/adcs/experiments/probes/probe-record.md` |  |
| `docs/superpowers/notes/paper-appendices-sketch.md` | keep | the result is not in a decision record: `WP10-decisions.md` points to it as the sketch (the three tiers per appendix) and `WP10-scope-of-work.md` Amendment 1 and `WP10-review-2.md` name it as their source. Reader: those records |  |
| `docs/superpowers/notes/paper-outline-v1-baseline.md` | keep | the result is not in a decision record: `WP10-decisions.md` only names it the baseline; `paper-outline-v2-search.md` says it "supersedes ... kept as the baseline" and `paper-prior-art-sources.md` cites its addendum for the contrast and the points of comparison (twice). Reader: those two notes |  |
| `docs/superpowers/notes/paper-outline-v2-search.md` | keep | `work-packages/README.md`, `WP10-decisions.md`; WP12 reads it |  |
| `docs/superpowers/notes/paper-prior-art-sources.md` | keep | `paper/prior_art.yaml`, `tests/test_references.py` |  |
| `docs/superpowers/notes/paper-sources/README.md` | keep | the paper's source notes: `CLAUDE.md`, `README.md`, `claims_register.toml` (+29) |  |
| `docs/superpowers/notes/paper-sources/api.md` | keep | the paper's source notes: `claims_register.toml`, `docs/api-reference.md`, `docs/index.md` (+13) |  |
| `docs/superpowers/notes/paper-sources/limitations.md` | keep | the paper's source notes: `claims_register.toml`, `docs/theory.md`, `docs/user-guide/overview.md` (+11) |  |
| `docs/superpowers/notes/paper-sources/literature.md` | keep | the paper's source notes: `claims_register.toml`, `paper/supporting_material.ipynb` |  |
| `docs/superpowers/notes/paper-sources/method.md` | keep | the paper's source notes: `work-packages/WP24-decisions.md` |  |
| `docs/superpowers/notes/paper-sources/preconditioning.md` | keep | the paper's source notes: `docs/superpowers/specs/2026-11-07-posynomial-invariant-form-design.md`, `tests/test_paper_sources.py`, `work-packages/README.md` (+4) |  |
| `docs/superpowers/notes/paper-sources/why-and-how.md` | keep | the paper's source notes: `tests/test_narrative.py`, `tests/test_paper_sources.py`, `work-packages/WP10-scope-of-work.md` (+3) |  |
| `docs/superpowers/notes/reader-grid.md` | keep | `work-packages/README.md`, the WP11 reader rounds |  |
| `docs/superpowers/notes/references-verified.md` | keep | `derivation/PROOF_MAP_FINDINGS.md`, `WP17-decisions.md` |  |
| `docs/superpowers/notes/search-prior-art.md` | hold: WP12 (unscoped) | the result is not in a decision record: `WP12-decisions.md` points to this note for "the explanation back, the prior art and the proof assessment" (the prior-art table with DOIs, the procedure, the low-hanging proofs L11 to L14, I6, I7, T1), and WP12 has no scope yet to carry them. Delete when WP12 records them or is dropped |  |
| `docs/superpowers/notes/spike-certificates/README.md` | keep | the README is cited by path from `paper/supporting_material.ipynb`; the script regenerates the spike's outputs (decision of 2026-11-10 07:00) |  |
| `docs/superpowers/notes/spike-certificates/certificates.py` | keep | the README is cited by path from `paper/supporting_material.ipynb`; the script regenerates the spike's outputs (decision of 2026-11-10 07:00) |  |
| `docs/superpowers/notes/spike-certificates/check_identities.py` | keep | the README is cited by path from `paper/supporting_material.ipynb`; the script regenerates the spike's outputs (decision of 2026-11-10 07:00) |  |
| `docs/superpowers/notes/spike-certificates/cubesat.csv` | hold: the paper unit, then delete | the decision of 2026-11-10 07:00 (`WP25-decisions.md`, "Instance 2"): outputs go once the paper stream has re-pointed the citations in `paper/supporting_material.ipynb` and `paper/generate_results.py` to the README and the generator; the generator regenerates it |  |
| `docs/superpowers/notes/spike-certificates/cubesat.txt` | hold: the paper unit, then delete | the decision of 2026-11-10 07:00 (`WP25-decisions.md`, "Instance 2"): outputs go once the paper stream has re-pointed the citations in `paper/supporting_material.ipynb` and `paper/generate_results.py` to the README and the generator; the generator regenerates it |  |
| `docs/superpowers/notes/spike-certificates/dup_facets.py` | keep | the README is cited by path from `paper/supporting_material.ipynb`; the script regenerates the spike's outputs (decision of 2026-11-10 07:00) |  |
| `docs/superpowers/notes/spike-certificates/planted.csv` | hold: the paper unit, then delete | the decision of 2026-11-10 07:00 (`WP25-decisions.md`, "Instance 2"): outputs go once the paper stream has re-pointed the citations in `paper/supporting_material.ipynb` and `paper/generate_results.py` to the README and the generator; the generator regenerates it |  |
| `docs/superpowers/notes/spike-certificates/planted.txt` | hold: the paper unit, then delete | the decision of 2026-11-10 07:00 (`WP25-decisions.md`, "Instance 2"): outputs go once the paper stream has re-pointed the citations in `paper/supporting_material.ipynb` and `paper/generate_results.py` to the README and the generator; the generator regenerates it |  |
| `docs/superpowers/notes/spike-certificates/planted_restarts.csv` | hold: the paper unit, then delete | the decision of 2026-11-10 07:00 (`WP25-decisions.md`, "Instance 2"): outputs go once the paper stream has re-pointed the citations in `paper/supporting_material.ipynb` and `paper/generate_results.py` to the README and the generator; the generator regenerates it |  |
| `docs/superpowers/notes/spike-certificates/polish_and_ties.py` | keep | the README is cited by path from `paper/supporting_material.ipynb`; the script regenerates the spike's outputs (decision of 2026-11-10 07:00) |  |
| `docs/superpowers/notes/spike-certificates/polish_and_ties.txt` | hold: the paper unit, then delete | the decision of 2026-11-10 07:00 (`WP25-decisions.md`, "Instance 2"): outputs go once the paper stream has re-pointed the citations in `paper/supporting_material.ipynb` and `paper/generate_results.py` to the README and the generator; the generator regenerates it |  |
| `docs/superpowers/notes/spike-certificates/run_cubesat.py` | keep | the README is cited by path from `paper/supporting_material.ipynb`; the script regenerates the spike's outputs (decision of 2026-11-10 07:00) |  |
| `docs/superpowers/notes/spike-certificates/run_planted.py` | keep | the README is cited by path from `paper/supporting_material.ipynb`; the script regenerates the spike's outputs (decision of 2026-11-10 07:00) |  |
| `docs/superpowers/notes/spike-certificates/sympy_feasibility.py` | keep | the README is cited by path from `paper/supporting_material.ipynb`; the script regenerates the spike's outputs (decision of 2026-11-10 07:00) |  |
| `docs/superpowers/notes/spike-certificates/sympy_feasibility.txt` | hold: the paper unit, then delete | the decision of 2026-11-10 07:00 (`WP25-decisions.md`, "Instance 2"): outputs go once the paper stream has re-pointed the citations in `paper/supporting_material.ipynb` and `paper/generate_results.py` to the README and the generator; the generator regenerates it |  |
| `docs/superpowers/notes/spike-container-platform/report.md` | keep | the container platform report: `paper/container/README.md`, `paper/container/RECORD.md`, `claims_register.toml` |  |
| `docs/superpowers/notes/spike-facet-refit/README.md` | keep | the README is cited by path from `paper/supporting_material.ipynb`; the script regenerates the spike's outputs (decision of 2026-11-10 07:00) |  |
| `docs/superpowers/notes/spike-facet-refit/bench_cubesat.py` | keep | the README is cited by path from `paper/supporting_material.ipynb`; the script regenerates the spike's outputs (decision of 2026-11-10 07:00) |  |
| `docs/superpowers/notes/spike-facet-refit/bench_oracle.py` | keep | the README is cited by path from `paper/supporting_material.ipynb`; the script regenerates the spike's outputs (decision of 2026-11-10 07:00) |  |
| `docs/superpowers/notes/spike-facet-refit/bench_planted.py` | keep | the README is cited by path from `paper/supporting_material.ipynb`; the script regenerates the spike's outputs (decision of 2026-11-10 07:00) |  |
| `docs/superpowers/notes/spike-facet-refit/bench_restarts.py` | keep | the README is cited by path from `paper/supporting_material.ipynb`; the script regenerates the spike's outputs (decision of 2026-11-10 07:00) |  |
| `docs/superpowers/notes/spike-facet-refit/cubesat.csv` | hold: the paper unit, then delete | the decision of 2026-11-10 07:00 (`WP25-decisions.md`, "Instance 2"): outputs go once the paper stream has re-pointed the citations in `paper/supporting_material.ipynb` and `paper/generate_results.py` to the README and the generator; the generator regenerates it |  |
| `docs/superpowers/notes/spike-facet-refit/cubesat.txt` | hold: the paper unit, then delete | the decision of 2026-11-10 07:00 (`WP25-decisions.md`, "Instance 2"): outputs go once the paper stream has re-pointed the citations in `paper/supporting_material.ipynb` and `paper/generate_results.py` to the README and the generator; the generator regenerates it |  |
| `docs/superpowers/notes/spike-facet-refit/methods.py` | keep | the README is cited by path from `paper/supporting_material.ipynb`; the script regenerates the spike's outputs (decision of 2026-11-10 07:00) |  |
| `docs/superpowers/notes/spike-facet-refit/oracle.csv` | hold: the paper unit, then delete | the decision of 2026-11-10 07:00 (`WP25-decisions.md`, "Instance 2"): outputs go once the paper stream has re-pointed the citations in `paper/supporting_material.ipynb` and `paper/generate_results.py` to the README and the generator; the generator regenerates it |  |
| `docs/superpowers/notes/spike-facet-refit/oracle.txt` | hold: the paper unit, then delete | the decision of 2026-11-10 07:00 (`WP25-decisions.md`, "Instance 2"): outputs go once the paper stream has re-pointed the citations in `paper/supporting_material.ipynb` and `paper/generate_results.py` to the README and the generator; the generator regenerates it |  |
| `docs/superpowers/notes/spike-facet-refit/planted_flipped.csv` | hold: the paper unit, then delete | the decision of 2026-11-10 07:00 (`WP25-decisions.md`, "Instance 2"): outputs go once the paper stream has re-pointed the citations in `paper/supporting_material.ipynb` and `paper/generate_results.py` to the README and the generator; the generator regenerates it |  |
| `docs/superpowers/notes/spike-facet-refit/planted_flipped.txt` | hold: the paper unit, then delete | the decision of 2026-11-10 07:00 (`WP25-decisions.md`, "Instance 2"): outputs go once the paper stream has re-pointed the citations in `paper/supporting_material.ipynb` and `paper/generate_results.py` to the README and the generator; the generator regenerates it |  |
| `docs/superpowers/notes/spike-facet-refit/planted_solver.csv` | hold: the paper unit, then delete | the decision of 2026-11-10 07:00 (`WP25-decisions.md`, "Instance 2"): outputs go once the paper stream has re-pointed the citations in `paper/supporting_material.ipynb` and `paper/generate_results.py` to the README and the generator; the generator regenerates it |  |
| `docs/superpowers/notes/spike-facet-refit/planted_solver.txt` | hold: the paper unit, then delete | the decision of 2026-11-10 07:00 (`WP25-decisions.md`, "Instance 2"): outputs go once the paper stream has re-pointed the citations in `paper/supporting_material.ipynb` and `paper/generate_results.py` to the README and the generator; the generator regenerates it |  |
| `docs/superpowers/notes/spike-facet-refit/restarts.csv` | hold: the paper unit, then delete | the decision of 2026-11-10 07:00 (`WP25-decisions.md`, "Instance 2"): outputs go once the paper stream has re-pointed the citations in `paper/supporting_material.ipynb` and `paper/generate_results.py` to the README and the generator; the generator regenerates it |  |
| `docs/superpowers/notes/spike-facet-refit/restarts.txt` | hold: the paper unit, then delete | the decision of 2026-11-10 07:00 (`WP25-decisions.md`, "Instance 2"): outputs go once the paper stream has re-pointed the citations in `paper/supporting_material.ipynb` and `paper/generate_results.py` to the README and the generator; the generator regenerates it |  |
| `docs/superpowers/notes/spike-figure1/README.md` | keep | the generator and README of the paper's Figure 1: `paper/figures/figure1.py`, `CLAUDE.md` |  |
| `docs/superpowers/notes/spike-figure1/make_schematics.py` | keep | the generator and README of the paper's Figure 1: `paper/figures/figure1.py`, `CLAUDE.md` |  |
| `docs/superpowers/notes/spike-objective/README.md` | keep | the README is cited by path from `paper/supporting_material.ipynb`; the script regenerates the spike's outputs (decision of 2026-11-10 07:00) |  |
| `docs/superpowers/notes/spike-objective/ab.txt` | hold: the paper unit, then delete | the decision of 2026-11-10 07:00 (`WP25-decisions.md`, "Instance 2"): outputs go once the paper stream has re-pointed the citations in `paper/supporting_material.ipynb` and `paper/generate_results.py` to the README and the generator; the generator regenerates it |  |
| `docs/superpowers/notes/spike-objective/bench_ab.py` | keep | the README is cited by path from `paper/supporting_material.ipynb`; the script regenerates the spike's outputs (decision of 2026-11-10 07:00) |  |
| `docs/superpowers/notes/spike-objective/bench_c.py` | keep | the README is cited by path from `paper/supporting_material.ipynb`; the script regenerates the spike's outputs (decision of 2026-11-10 07:00) |  |
| `docs/superpowers/notes/spike-objective/bench_cubesat2.py` | keep | the README is cited by path from `paper/supporting_material.ipynb`; the script regenerates the spike's outputs (decision of 2026-11-10 07:00) |  |
| `docs/superpowers/notes/spike-objective/c.txt` | hold: the paper unit, then delete | the decision of 2026-11-10 07:00 (`WP25-decisions.md`, "Instance 2"): outputs go once the paper stream has re-pointed the citations in `paper/supporting_material.ipynb` and `paper/generate_results.py` to the README and the generator; the generator regenerates it |  |
| `docs/superpowers/notes/spike-objective/check_identifiability.py` | keep | the README is cited by path from `paper/supporting_material.ipynb`; the script regenerates the spike's outputs (decision of 2026-11-10 07:00) |  |
| `docs/superpowers/notes/spike-objective/cubesat2.csv` | hold: the paper unit, then delete | the decision of 2026-11-10 07:00 (`WP25-decisions.md`, "Instance 2"): outputs go once the paper stream has re-pointed the citations in `paper/supporting_material.ipynb` and `paper/generate_results.py` to the README and the generator; the generator regenerates it |  |
| `docs/superpowers/notes/spike-objective/cubesat2.txt` | hold: the paper unit, then delete | the decision of 2026-11-10 07:00 (`WP25-decisions.md`, "Instance 2"): outputs go once the paper stream has re-pointed the citations in `paper/supporting_material.ipynb` and `paper/generate_results.py` to the README and the generator; the generator regenerates it |  |
| `docs/superpowers/notes/spike-objective/fail_seeds.py` | keep | the README is cited by path from `paper/supporting_material.ipynb`; the script regenerates the spike's outputs (decision of 2026-11-10 07:00) |  |
| `docs/superpowers/notes/spike-objective/mono.csv` | hold: the paper unit, then delete | the decision of 2026-11-10 07:00 (`WP25-decisions.md`, "Instance 2"): outputs go once the paper stream has re-pointed the citations in `paper/supporting_material.ipynb` and `paper/generate_results.py` to the README and the generator; the generator regenerates it |  |
| `docs/superpowers/notes/spike-objective/objectives.py` | keep | the README is cited by path from `paper/supporting_material.ipynb`; the script regenerates the spike's outputs (decision of 2026-11-10 07:00) |  |
| `docs/superpowers/notes/spike-objective/planted_vs_found.csv` | hold: the paper unit, then delete | the decision of 2026-11-10 07:00 (`WP25-decisions.md`, "Instance 2"): outputs go once the paper stream has re-pointed the citations in `paper/supporting_material.ipynb` and `paper/generate_results.py` to the README and the generator; the generator regenerates it |  |
| `docs/superpowers/notes/spike-objective/recovery_restarts.csv` | hold: the paper unit, then delete | the decision of 2026-11-10 07:00 (`WP25-decisions.md`, "Instance 2"): outputs go once the paper stream has re-pointed the citations in `paper/supporting_material.ipynb` and `paper/generate_results.py` to the README and the generator; the generator regenerates it |  |
| `docs/superpowers/notes/spike-objective/recovery_single.csv` | hold: the paper unit, then delete | the decision of 2026-11-10 07:00 (`WP25-decisions.md`, "Instance 2"): outputs go once the paper stream has re-pointed the citations in `paper/supporting_material.ipynb` and `paper/generate_results.py` to the README and the generator; the generator regenerates it |  |
| `docs/superpowers/notes/spike-objective/restarts_all.csv` | hold: the paper unit, then delete | the decision of 2026-11-10 07:00 (`WP25-decisions.md`, "Instance 2"): outputs go once the paper stream has re-pointed the citations in `paper/supporting_material.ipynb` and `paper/generate_results.py` to the README and the generator; the generator regenerates it |  |
| `docs/superpowers/notes/spike-sysml-diagrams/project.py` | keep | the generator of the model's views: `examples/adcs/case-model.md`, `tests/test_system_model_v2_r1.py` (WP23 is accepted at db59365; the file is read by a test) |  |
| `docs/superpowers/notes/spike-sysml-diagrams/render.sh` | keep | the render recipe `examples/adcs/case-model.md` names |  |
| `docs/superpowers/notes/spike-ternary/report.md` | hold: WP24, then delete | a `file:` backing of a row in `claims_register.toml` (L32) and the `defined_in` of two entries in `glossary.yaml` (L515, L535); `tests/test_claims_register.py` fails on a missing backing file. Deleted by the instance after WP24's last push, once both point at `plot_ternary`'s Notes |  |
| `docs/superpowers/notes/system-model-tidy.md` | keep | `examples/adcs/experiments/reports/v1-v2-comparison.md`, `work-packages/README.md` |  |
| `mkdocs.yml` | keep | `scripts/assemble_site.py`, `tests/test_site.py` |  |
| `pyproject.toml` | keep | uv, the build and CI |  |
| `site/paper-map.webp` | keep | `site/index.html`, `tests/test_site.py` |  |
| `site/paper/index.html` | keep | the paper placeholder the Pages build stages (`scripts/stage_site.py`, `tests/test_site.py`) |  |
| `uv.lock` | keep | uv sync --locked; CI |  |
| `work-packages/WP0-decisions.md` | keep | the record of an accepted package (A1); read by `work-packages/README.md` |  |
| `work-packages/WP0-review.md` | keep | the record of an accepted package (A1); read by `work-packages/README.md` |  |
| `work-packages/WP0-scope-of-work.md` | keep | the record of an accepted package (A1); read by `work-packages/README.md` |  |
| `work-packages/WP1-decisions.md` | keep | the record of an accepted package (A1); read by `work-packages/README.md` |  |
| `work-packages/WP1-review.md` | keep | the record of an accepted package (A1); read by `tests/test_rename_facet.py` |  |
| `work-packages/WP1-scope-of-work.md` | keep | the record of an accepted package (A1); read by `work-packages/README.md` |  |
| `work-packages/WP10-claims-review.md` | keep | a record of WP10, WP11, WP14 or WP19 read by `examples/adcs/experiments/reports/v1-v2-comparison.md`, `work-packages/WP10-scope-of-work.md`, `work-packages/parallel-board.md` |  |
| `work-packages/WP10-cold-reads-triage.md` | keep | a record of WP10, WP11, WP14 or WP19 read by `work-packages/driver-log.md`, `work-packages/interface-contract.md` |  |
| `work-packages/WP10-cold-reads.md` | delete | the raw reports of the first cold reads (53 kB, one fresh reader per depth); `WP10-cold-reads-triage.md` holds the 22 findings and the driver's calls, `WP10-review-2.md` G-8 closes on the triage; no live file reads it | path: 0 files. basename: 6 file(s), 6 in records |
| `work-packages/WP10-reading-pass.md` | keep | a record of WP10, WP11, WP14 or WP19 read by `paper/generate_reading_pass.py`, `paper/reading_pass.yaml` |  |
| `work-packages/WP10-review-2.md` | keep | a record of WP10, WP11, WP14 or WP19 read by `work-packages/README.md`, `work-packages/WP10-decisions.md`, `work-packages/WP10-scope-of-work.md` (+1) |  |
| `work-packages/WP10-vocabulary-review.md` | keep | a record of WP10, WP11, WP14 or WP19 read by `examples/adcs/experiments/reports/v1-v2-comparison.md`, `scripts/vocabulary_baseline.toml`, `work-packages/WP10-scope-of-work.md` (+1) |  |
| `work-packages/WP11-round-1/triage.md` | keep | a record of WP10, WP11, WP14 or WP19 read by `work-packages/WP19-scope-of-work.md`, `work-packages/WP21-scope-of-work.md`, `work-packages/driver-log.md` (+1) |  |
| `work-packages/WP13-decisions.md` | keep | the record of an accepted package (A1); read by `work-packages/README.md` |  |
| `work-packages/WP13-review.md` | keep | the record of an accepted package (A1); read by `work-packages/README.md` |  |
| `work-packages/WP13-scope-of-work.md` | keep | the record of an accepted package (A1); read by `work-packages/README.md` |  |
| `work-packages/WP14-decisions.md` | keep | the record of an accepted package (A1); read by `work-packages/WP8a-scope-of-work.md`, `work-packages/interface-contract.md` |  |
| `work-packages/WP14-review.md` | keep | the record of an accepted package (A1); read by `work-packages/README.md` |  |
| `work-packages/WP14-scope-of-work.md` | keep | the record of an accepted package (A1); read by `examples/adcs/experiments/reports/v1-v2-comparison.md` |  |
| `work-packages/WP19-backlog.md` | keep | a record of WP10, WP11, WP14 or WP19 read by `work-packages/WP10-decisions.md` |  |
| `work-packages/WP19-figure-review.md` | keep | a record of WP10, WP11, WP14 or WP19 read by `paper/length_ledger.toml`, `work-packages/WP19-scope-of-work.md` |  |
| `work-packages/WP19-slots.md` | keep | a record of WP10, WP11, WP14 or WP19 read by `work-packages/WP19-scope-of-work.md`, `work-packages/parallel-board.md` |  |
| `work-packages/WP2-decisions.md` | keep | the record of an accepted package (A1); read by `work-packages/README.md` |  |
| `work-packages/WP2-review.md` | keep | the record of an accepted package (A1); read by `work-packages/README.md` |  |
| `work-packages/WP2-scope-of-work.md` | keep | the record of an accepted package (A1); read by `work-packages/README.md` |  |
| `work-packages/WP23-rounds/gate/README.md` | keep | the gate's record (`WP23-rounds/gate/README.md`, the data gate): `examples/adcs/experiments/reports/change-register.md`, `examples/adcs/experiments/reports/v1-v2-comparison.md`, `paper/container/RECORD.md` (+1) |  |
| `work-packages/WP23-rounds/gate/coverage.md` | keep | the gate's record (`WP23-rounds/gate/README.md`, the data gate): `examples/adcs/case-model.md`, `examples/adcs/model_v2/coverage.py`, `examples/adcs/model_v2/diagnostic_pair.py` (+6) |  |
| `work-packages/WP23-rounds/gate/heatmap.png` | keep | the gate's record (`WP23-rounds/gate/README.md`, the data gate): `examples/adcs/model_v2/diagnostic_pair.py`, `tests/test_diagnostic_pair.py`, `work-packages/WP23-review.md` (+2) |  |
| `work-packages/WP23-rounds/gate/heatmap_baseline.png` | keep | the gate's record (`WP23-rounds/gate/README.md`, the data gate): `examples/adcs/model_v2/diagnostic_pair.py`, `tests/test_diagnostic_pair.py`, `work-packages/WP23-review.md` |  |
| `work-packages/WP23-rounds/gate/k3_record.md` | keep | the gate's record (`WP23-rounds/gate/README.md`, the data gate): `examples/adcs/case-model.md`, `examples/adcs/experiments/reports/v1-v2-comparison.md`, `examples/adcs/model_v2/diagnostic_pair.py` (+4) |  |
| `work-packages/WP23-rounds/round-1/INTENT.md` | keep | a round record of WP23's cold reads, quoted by `WP23-review.md` and `swap-evidence.md` |  |
| `work-packages/WP23-rounds/round-1/README.md` | keep | a round record of WP23's cold reads, quoted by `WP23-review.md` and `swap-evidence.md` |  |
| `work-packages/WP23-rounds/round-1/assembly_view.png` | delete | a render of round 1 of the WP23 cold reads; the records name it as what was read, and the reading is quoted there; superseded by `examples/adcs/model_v2/views/` (revision 8) and `WP23-rounds/gate/`; regenerated by `diagnostic_pair.py` and `project.py` | path: 0 files. basename: 10 file(s), 9 in records; outside records: `scripts/build_figures.py` (same-named files elsewhere: `examples/adcs/model_v2/views/`, `gate/`, a test's tmp output; none reads this path) |
| `work-packages/WP23-rounds/round-1/assembly_view.puml` | delete | a render of round 1 of the WP23 cold reads; the records name it as what was read, and the reading is quoted there; superseded by `examples/adcs/model_v2/views/` (revision 8) and `WP23-rounds/gate/`; regenerated by `diagnostic_pair.py` and `project.py` | path: 0 files. basename: 5 file(s), 3 in records; outside records: `docs/superpowers/notes/spike-sysml-diagrams/project.py`, `tests/test_system_model_v2_r1.py` (same-named files elsewhere: `examples/adcs/model_v2/views/`, `gate/`, a test's tmp output; none reads this path) |
| `work-packages/WP23-rounds/round-1/assembly_view.svg` | delete | a render of round 1 of the WP23 cold reads; the records name it as what was read, and the reading is quoted there; superseded by `examples/adcs/model_v2/views/` (revision 8) and `WP23-rounds/gate/`; regenerated by `diagnostic_pair.py` and `project.py` | path: 0 files. basename: 0 file(s) |
| `work-packages/WP23-rounds/round-1/behavioural_view.png` | delete | a render of round 1 of the WP23 cold reads; the records name it as what was read, and the reading is quoted there; superseded by `examples/adcs/model_v2/views/` (revision 8) and `WP23-rounds/gate/`; regenerated by `diagnostic_pair.py` and `project.py` | path: 0 files. basename: 10 file(s), 9 in records; outside records: `scripts/build_figures.py` (same-named files elsewhere: `examples/adcs/model_v2/views/`, `gate/`, a test's tmp output; none reads this path) |
| `work-packages/WP23-rounds/round-1/behavioural_view.puml` | delete | a render of round 1 of the WP23 cold reads; the records name it as what was read, and the reading is quoted there; superseded by `examples/adcs/model_v2/views/` (revision 8) and `WP23-rounds/gate/`; regenerated by `diagnostic_pair.py` and `project.py` | path: 0 files. basename: 5 file(s), 3 in records; outside records: `docs/superpowers/notes/spike-sysml-diagrams/project.py`, `tests/test_system_model_v2_r1.py` (same-named files elsewhere: `examples/adcs/model_v2/views/`, `gate/`, a test's tmp output; none reads this path) |
| `work-packages/WP23-rounds/round-1/behavioural_view.svg` | delete | a render of round 1 of the WP23 cold reads; the records name it as what was read, and the reading is quoted there; superseded by `examples/adcs/model_v2/views/` (revision 8) and `WP23-rounds/gate/`; regenerated by `diagnostic_pair.py` and `project.py` | path: 0 files. basename: 1 file(s), 0 in records; outside records: `tests/test_system_model_v2_r1.py` (same-named files elsewhere: `examples/adcs/model_v2/views/`, `gate/`, a test's tmp output; none reads this path) |
| `work-packages/WP23-rounds/round-1/cold-reads.md` | keep | a round record of WP23's cold reads, quoted by `WP23-review.md` and `swap-evidence.md` |  |
| `work-packages/WP23-rounds/round-1/coverage.md` | keep | a round record of WP23's cold reads, quoted by `WP23-review.md` and `swap-evidence.md` |  |
| `work-packages/WP23-rounds/round-1/generation-ledger.jsonl` | keep | the generation ledger of the run that produced the data of record: cited by `round-1/README.md` and `round-4/README.md`; ledgers stay (scope, Non-goals) |  |
| `work-packages/WP23-rounds/round-1/heatmap.png` | delete | a render of round 1 of the WP23 cold reads; the records name it as what was read, and the reading is quoted there; superseded by `examples/adcs/model_v2/views/` (revision 8) and `WP23-rounds/gate/`; regenerated by `diagnostic_pair.py` and `project.py` | path: 0 files. basename: 12 file(s), 10 in records; outside records: `examples/adcs/model_v2/diagnostic_pair.py`, `tests/test_diagnostic_pair.py` (same-named files elsewhere: `examples/adcs/model_v2/views/`, `gate/`, a test's tmp output; none reads this path) |
| `work-packages/WP23-rounds/round-1/heatmap_stock.png` | delete | a render of round 1 of the WP23 cold reads; the records name it as what was read, and the reading is quoted there; superseded by `examples/adcs/model_v2/views/` (revision 8) and `WP23-rounds/gate/`; regenerated by `diagnostic_pair.py` and `project.py` | path: 0 files. basename: 5 file(s), 5 in records |
| `work-packages/WP23-rounds/round-1/k3_record.md` | keep | a round record of WP23's cold reads, quoted by `WP23-review.md` and `swap-evidence.md` |  |
| `work-packages/WP23-rounds/round-2/INTENT.md` | keep | a round record of WP23's cold reads, quoted by `WP23-review.md` and `swap-evidence.md` |  |
| `work-packages/WP23-rounds/round-2/assembly_view.png` | delete | a render of round 2 of the WP23 cold reads; the records name it as what was read, and the reading is quoted there; superseded by `examples/adcs/model_v2/views/` (revision 8) and `WP23-rounds/gate/`; regenerated by `diagnostic_pair.py` and `project.py` | path: 0 files. basename: 10 file(s), 9 in records; outside records: `scripts/build_figures.py` (same-named files elsewhere: `examples/adcs/model_v2/views/`, `gate/`, a test's tmp output; none reads this path) |
| `work-packages/WP23-rounds/round-2/assembly_view.puml` | delete | a render of round 2 of the WP23 cold reads; the records name it as what was read, and the reading is quoted there; superseded by `examples/adcs/model_v2/views/` (revision 8) and `WP23-rounds/gate/`; regenerated by `diagnostic_pair.py` and `project.py` | path: 0 files. basename: 5 file(s), 3 in records; outside records: `docs/superpowers/notes/spike-sysml-diagrams/project.py`, `tests/test_system_model_v2_r1.py` (same-named files elsewhere: `examples/adcs/model_v2/views/`, `gate/`, a test's tmp output; none reads this path) |
| `work-packages/WP23-rounds/round-2/assembly_view.svg` | delete | a render of round 2 of the WP23 cold reads; the records name it as what was read, and the reading is quoted there; superseded by `examples/adcs/model_v2/views/` (revision 8) and `WP23-rounds/gate/`; regenerated by `diagnostic_pair.py` and `project.py` | path: 0 files. basename: 0 file(s) |
| `work-packages/WP23-rounds/round-2/behavioural_view.png` | delete | a render of round 2 of the WP23 cold reads; the records name it as what was read, and the reading is quoted there; superseded by `examples/adcs/model_v2/views/` (revision 8) and `WP23-rounds/gate/`; regenerated by `diagnostic_pair.py` and `project.py` | path: 0 files. basename: 10 file(s), 9 in records; outside records: `scripts/build_figures.py` (same-named files elsewhere: `examples/adcs/model_v2/views/`, `gate/`, a test's tmp output; none reads this path) |
| `work-packages/WP23-rounds/round-2/behavioural_view.puml` | delete | a render of round 2 of the WP23 cold reads; the records name it as what was read, and the reading is quoted there; superseded by `examples/adcs/model_v2/views/` (revision 8) and `WP23-rounds/gate/`; regenerated by `diagnostic_pair.py` and `project.py` | path: 0 files. basename: 5 file(s), 3 in records; outside records: `docs/superpowers/notes/spike-sysml-diagrams/project.py`, `tests/test_system_model_v2_r1.py` (same-named files elsewhere: `examples/adcs/model_v2/views/`, `gate/`, a test's tmp output; none reads this path) |
| `work-packages/WP23-rounds/round-2/behavioural_view.svg` | delete | a render of round 2 of the WP23 cold reads; the records name it as what was read, and the reading is quoted there; superseded by `examples/adcs/model_v2/views/` (revision 8) and `WP23-rounds/gate/`; regenerated by `diagnostic_pair.py` and `project.py` | path: 0 files. basename: 1 file(s), 0 in records; outside records: `tests/test_system_model_v2_r1.py` (same-named files elsewhere: `examples/adcs/model_v2/views/`, `gate/`, a test's tmp output; none reads this path) |
| `work-packages/WP23-rounds/round-3/INTENT.md` | keep | a round record of WP23's cold reads, quoted by `WP23-review.md` and `swap-evidence.md` |  |
| `work-packages/WP23-rounds/round-3/assembly_view.png` | delete | a render of round 3 of the WP23 cold reads; the records name it as what was read, and the reading is quoted there; superseded by `examples/adcs/model_v2/views/` (revision 8) and `WP23-rounds/gate/`; regenerated by `diagnostic_pair.py` and `project.py` | path: 0 files. basename: 10 file(s), 9 in records; outside records: `scripts/build_figures.py` (same-named files elsewhere: `examples/adcs/model_v2/views/`, `gate/`, a test's tmp output; none reads this path) |
| `work-packages/WP23-rounds/round-3/assembly_view.puml` | delete | a render of round 3 of the WP23 cold reads; the records name it as what was read, and the reading is quoted there; superseded by `examples/adcs/model_v2/views/` (revision 8) and `WP23-rounds/gate/`; regenerated by `diagnostic_pair.py` and `project.py` | path: 0 files. basename: 5 file(s), 3 in records; outside records: `docs/superpowers/notes/spike-sysml-diagrams/project.py`, `tests/test_system_model_v2_r1.py` (same-named files elsewhere: `examples/adcs/model_v2/views/`, `gate/`, a test's tmp output; none reads this path) |
| `work-packages/WP23-rounds/round-3/assembly_view.svg` | delete | a render of round 3 of the WP23 cold reads; the records name it as what was read, and the reading is quoted there; superseded by `examples/adcs/model_v2/views/` (revision 8) and `WP23-rounds/gate/`; regenerated by `diagnostic_pair.py` and `project.py` | path: 0 files. basename: 0 file(s) |
| `work-packages/WP23-rounds/round-3/behavioural_view.png` | delete | a render of round 3 of the WP23 cold reads; the records name it as what was read, and the reading is quoted there; superseded by `examples/adcs/model_v2/views/` (revision 8) and `WP23-rounds/gate/`; regenerated by `diagnostic_pair.py` and `project.py` | path: 0 files. basename: 10 file(s), 9 in records; outside records: `scripts/build_figures.py` (same-named files elsewhere: `examples/adcs/model_v2/views/`, `gate/`, a test's tmp output; none reads this path) |
| `work-packages/WP23-rounds/round-3/behavioural_view.puml` | delete | a render of round 3 of the WP23 cold reads; the records name it as what was read, and the reading is quoted there; superseded by `examples/adcs/model_v2/views/` (revision 8) and `WP23-rounds/gate/`; regenerated by `diagnostic_pair.py` and `project.py` | path: 0 files. basename: 5 file(s), 3 in records; outside records: `docs/superpowers/notes/spike-sysml-diagrams/project.py`, `tests/test_system_model_v2_r1.py` (same-named files elsewhere: `examples/adcs/model_v2/views/`, `gate/`, a test's tmp output; none reads this path) |
| `work-packages/WP23-rounds/round-3/behavioural_view.svg` | delete | a render of round 3 of the WP23 cold reads; the records name it as what was read, and the reading is quoted there; superseded by `examples/adcs/model_v2/views/` (revision 8) and `WP23-rounds/gate/`; regenerated by `diagnostic_pair.py` and `project.py` | path: 0 files. basename: 1 file(s), 0 in records; outside records: `tests/test_system_model_v2_r1.py` (same-named files elsewhere: `examples/adcs/model_v2/views/`, `gate/`, a test's tmp output; none reads this path) |
| `work-packages/WP23-rounds/round-3/cold-reads.md` | keep | a round record of WP23's cold reads, quoted by `WP23-review.md` and `swap-evidence.md` |  |
| `work-packages/WP23-rounds/round-3/coverage.md` | keep | a round record of WP23's cold reads, quoted by `WP23-review.md` and `swap-evidence.md` |  |
| `work-packages/WP23-rounds/round-3/heatmap.png` | delete | a render of round 3 of the WP23 cold reads; the records name it as what was read, and the reading is quoted there; superseded by `examples/adcs/model_v2/views/` (revision 8) and `WP23-rounds/gate/`; regenerated by `diagnostic_pair.py` and `project.py` | path: 0 files. basename: 12 file(s), 10 in records; outside records: `examples/adcs/model_v2/diagnostic_pair.py`, `tests/test_diagnostic_pair.py` (same-named files elsewhere: `examples/adcs/model_v2/views/`, `gate/`, a test's tmp output; none reads this path) |
| `work-packages/WP23-rounds/round-3/heatmap_stock.png` | delete | a render of round 3 of the WP23 cold reads; the records name it as what was read, and the reading is quoted there; superseded by `examples/adcs/model_v2/views/` (revision 8) and `WP23-rounds/gate/`; regenerated by `diagnostic_pair.py` and `project.py` | path: 0 files. basename: 5 file(s), 5 in records |
| `work-packages/WP23-rounds/round-3/k3_record.md` | keep | a round record of WP23's cold reads, quoted by `WP23-review.md` and `swap-evidence.md` |  |
| `work-packages/WP23-rounds/round-4/INTENT.md` | keep | a round record of WP23's cold reads, quoted by `WP23-review.md` and `swap-evidence.md` |  |
| `work-packages/WP23-rounds/round-4/README.md` | keep | a round record of WP23's cold reads, quoted by `WP23-review.md` and `swap-evidence.md` |  |
| `work-packages/WP23-rounds/round-4/assembly_caption.md` | keep | a round record of WP23's cold reads, quoted by `WP23-review.md` and `swap-evidence.md` |  |
| `work-packages/WP23-rounds/round-4/assembly_view.png` | delete | a render of round 4 of the WP23 cold reads; the records name it as what was read, and the reading is quoted there; superseded by `examples/adcs/model_v2/views/` (revision 8) and `WP23-rounds/gate/`; regenerated by `diagnostic_pair.py` and `project.py` | path: 0 files. basename: 10 file(s), 9 in records; outside records: `scripts/build_figures.py` (same-named files elsewhere: `examples/adcs/model_v2/views/`, `gate/`, a test's tmp output; none reads this path) |
| `work-packages/WP23-rounds/round-4/assembly_view.puml` | delete | a render of round 4 of the WP23 cold reads; the records name it as what was read, and the reading is quoted there; superseded by `examples/adcs/model_v2/views/` (revision 8) and `WP23-rounds/gate/`; regenerated by `diagnostic_pair.py` and `project.py` | path: 0 files. basename: 5 file(s), 3 in records; outside records: `docs/superpowers/notes/spike-sysml-diagrams/project.py`, `tests/test_system_model_v2_r1.py` (same-named files elsewhere: `examples/adcs/model_v2/views/`, `gate/`, a test's tmp output; none reads this path) |
| `work-packages/WP23-rounds/round-4/assembly_view.svg` | delete | a render of round 4 of the WP23 cold reads; the records name it as what was read, and the reading is quoted there; superseded by `examples/adcs/model_v2/views/` (revision 8) and `WP23-rounds/gate/`; regenerated by `diagnostic_pair.py` and `project.py` | path: 0 files. basename: 0 file(s) |
| `work-packages/WP23-rounds/round-4/behavioural_view.png` | delete | a render of round 4 of the WP23 cold reads; the records name it as what was read, and the reading is quoted there; superseded by `examples/adcs/model_v2/views/` (revision 8) and `WP23-rounds/gate/`; regenerated by `diagnostic_pair.py` and `project.py` | path: 0 files. basename: 10 file(s), 9 in records; outside records: `scripts/build_figures.py` (same-named files elsewhere: `examples/adcs/model_v2/views/`, `gate/`, a test's tmp output; none reads this path) |
| `work-packages/WP23-rounds/round-4/behavioural_view.puml` | delete | a render of round 4 of the WP23 cold reads; the records name it as what was read, and the reading is quoted there; superseded by `examples/adcs/model_v2/views/` (revision 8) and `WP23-rounds/gate/`; regenerated by `diagnostic_pair.py` and `project.py` | path: 0 files. basename: 5 file(s), 3 in records; outside records: `docs/superpowers/notes/spike-sysml-diagrams/project.py`, `tests/test_system_model_v2_r1.py` (same-named files elsewhere: `examples/adcs/model_v2/views/`, `gate/`, a test's tmp output; none reads this path) |
| `work-packages/WP23-rounds/round-4/behavioural_view.svg` | delete | a render of round 4 of the WP23 cold reads; the records name it as what was read, and the reading is quoted there; superseded by `examples/adcs/model_v2/views/` (revision 8) and `WP23-rounds/gate/`; regenerated by `diagnostic_pair.py` and `project.py` | path: 0 files. basename: 1 file(s), 0 in records; outside records: `tests/test_system_model_v2_r1.py` (same-named files elsewhere: `examples/adcs/model_v2/views/`, `gate/`, a test's tmp output; none reads this path) |
| `work-packages/WP23-rounds/round-4/coverage.md` | keep | a round record of WP23's cold reads, quoted by `WP23-review.md` and `swap-evidence.md` |  |
| `work-packages/WP23-rounds/round-4/heatmap.png` | delete | a render of round 4 of the WP23 cold reads; the records name it as what was read, and the reading is quoted there; superseded by `examples/adcs/model_v2/views/` (revision 8) and `WP23-rounds/gate/`; regenerated by `diagnostic_pair.py` and `project.py` | path: 0 files. basename: 12 file(s), 10 in records; outside records: `examples/adcs/model_v2/diagnostic_pair.py`, `tests/test_diagnostic_pair.py` (same-named files elsewhere: `examples/adcs/model_v2/views/`, `gate/`, a test's tmp output; none reads this path) |
| `work-packages/WP23-rounds/round-4/heatmap_baseline.png` | delete | a render of round 4 of the WP23 cold reads; the records name it as what was read, and the reading is quoted there; superseded by `examples/adcs/model_v2/views/` (revision 8) and `WP23-rounds/gate/`; regenerated by `diagnostic_pair.py` and `project.py` | path: 0 files. basename: 8 file(s), 6 in records; outside records: `examples/adcs/model_v2/diagnostic_pair.py`, `tests/test_diagnostic_pair.py` (same-named files elsewhere: `examples/adcs/model_v2/views/`, `gate/`, a test's tmp output; none reads this path) |
| `work-packages/WP23-rounds/round-4/k3_record.md` | keep | a round record of WP23's cold reads, quoted by `WP23-review.md` and `swap-evidence.md` |  |
| `work-packages/WP25-2-scope-of-work.md` | keep | this instance's scope (an unaccepted package's record, A1) |  |
| `work-packages/WP3-decisions.md` | keep | the record of an accepted package (A1); read by `work-packages/README.md` |  |
| `work-packages/WP3-review.md` | keep | the record of an accepted package (A1); read by `work-packages/README.md` |  |
| `work-packages/WP3-scope-of-work.md` | keep | the record of an accepted package (A1); read by `work-packages/README.md` |  |
| `work-packages/WP4-decisions.md` | keep | the record of an accepted package (A1); read by `work-packages/README.md` |  |
| `work-packages/WP4-review.md` | keep | the record of an accepted package (A1); read by `work-packages/README.md` |  |
| `work-packages/WP4-scope-of-work.md` | keep | the record of an accepted package (A1); read by `examples/adcs/experiments/reports/v1-v2-comparison.md` |  |
| `work-packages/WP4b-decisions.md` | keep | the record of an accepted package (A1); read by `examples/adcs/experiments/reports/v1-v2-comparison.md`, `tests/test_adcs_enrichment.py` |  |
| `work-packages/WP4b-review.md` | keep | the record of an accepted package (A1); read by `examples/adcs/experiments/reports/v1-v2-comparison.md` |  |
| `work-packages/WP4b-scope-of-work.md` | keep | the record of an accepted package (A1); read by `examples/adcs/experiments/reports/v1-v2-comparison.md` |  |
| `work-packages/WP5-decisions.md` | keep | the record of an accepted package (A1); read by `work-packages/README.md` |  |
| `work-packages/WP5-review.md` | keep | the record of an accepted package (A1); read by `work-packages/README.md` |  |
| `work-packages/WP5-scope-of-work.md` | keep | the record of an accepted package (A1); read by `work-packages/README.md` |  |
| `work-packages/WP6-decisions.md` | keep | the record of an accepted package (A1); read by `work-packages/README.md` |  |
| `work-packages/WP6-review.md` | keep | the record of an accepted package (A1); read by `work-packages/README.md` |  |
| `work-packages/WP6-scope-of-work.md` | keep | the record of an accepted package (A1); read by `work-packages/README.md` |  |
| `work-packages/WP7-decisions.md` | keep | the record of an accepted package (A1); read by `examples/adcs/experiments/reports/v1-v2-comparison.md` |  |
| `work-packages/WP7-review.md` | keep | the record of an accepted package (A1); read by `examples/adcs/experiments/reports/v1-v2-comparison.md` |  |
| `work-packages/WP7-scope-of-work.md` | keep | the record of an accepted package (A1); read by `examples/adcs/experiments/reports/v1-v2-comparison.md` |  |
| `work-packages/WP8-decisions.md` | keep | the record of an accepted package (A1); read by `work-packages/README.md`, `work-packages/WP8a-decisions.md`, `work-packages/WP8a-scope-of-work.md` (+1) |  |
| `work-packages/WP8-scope-of-work.md` | keep | the record of an accepted package (A1); read by `work-packages/README.md` |  |
| `work-packages/WP8a-driver-browser-pass.md` | keep | the record of an accepted package (A1); read by `work-packages/README.md`, `work-packages/WP8a-decisions.md`, `work-packages/driver-log.md` |  |
| `work-packages/WP8a-figure-review.md` | keep | the record of an accepted package (A1); read by `work-packages/parallel-board.md` |  |
| `work-packages/WP8a-review-amendment2.md` | keep | the record of an accepted package (A1); read by `work-packages/README.md` |  |
| `work-packages/WP9-decisions.md` | keep | the record of an accepted package (A1); read by `work-packages/README.md`, `work-packages/WP10-decisions.md` |  |
| `work-packages/WP9-review.md` | keep | the record of an accepted package (A1); read by `paper/supporting_material.ipynb` |  |
| `work-packages/WP9-scope-of-work.md` | keep | the record of an accepted package (A1); read by `examples/adcs/experiments/reports/v1-v2-comparison.md` |  |
| `work-packages/external-assessment-2026-11-09/assessment.md` | keep | `paper/supporting_material.ipynb`, `WP21-scope-of-work.md` |  |
| `work-packages/external-assessment-2026-11-09/triage.md` | keep | the triage of the outside assessment: `WP21-scope-of-work.md`, `WP19-scope-of-work.md` |  |
| `work-packages/external-assessment-2026-11-09/verification.json` | keep | `assessment.md` (cited by `paper/supporting_material.ipynb`) sends its reader to this file for "exact outcomes and numerical comparisons"; `WP21-scope-of-work.md` lists it as evidence; 2.6 kB; deleting leaves a cited document with a dangling pointer. Revisit when `assessment.md` goes |  |
| `work-packages/external-review-2026-11.md` | keep | the outside review the abstraction-gaps ledger cites (E-10): `WP10-decisions.md`, `work-packages/README.md` |  |
| `work-packages/streams/P10-review.md` | hold: WP10 acceptance | named by no file (`WP10-decisions.md` mentions P10); folded into `WP10-review.md` or deleted when WP10 is finally accepted (WP10 is a working draft) |  |

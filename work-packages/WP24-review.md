# WP24 — Review report (the vocabulary rename)

| | |
|---|---|
| **Scope of work** | `work-packages/WP24-scope-of-work.md` |
| **Approval** | `work-packages/WP24-decisions.md` (the driver under the mandate, 2026-11-09, 22:50; the gate line in the scope) |
| **Work reviewed** | the pushes below, in order |

The review proper (the checklist against D-1 to D-14 and R-1 to R-16, and the cold reads of R-16) is written by the fresh
reviewer after the last push. The per-push sections below are the evidence trail, written as each push landed from the
repository's own records and from commands run at the time of writing.

## Push 1 (src, contract row 14, tests, case code, generators; the container regeneration)

Commits: `204e7c3` (the rename) and `5b01248` (the regeneration in the container of record).

### Files changed

`git show --stat` of each commit, by surface.

| Surface | `204e7c3` | `5b01248` |
|---|---|---|
| `src/` | 6 files (`datasets`, `estimator`, `plotting`, `solvers`, `tensions`, `tuning`) | 0 |
| `tests/` | 17 files (plus `tests/data/soft_fit_default_reference.npz` among them) | 1 (`test_paper.py`) |
| `examples/adcs/` | 10 files (`case.py`, `k_terms.py`, `experiments/sensitivity.py`, `experiments/reports/sensitivity.json`, six deleted PNGs) | 0 |
| `paper/` | 11 files (generators, `paper_facets.py` moved to `paper_terms.py`, `environment_values.toml`, `supporting_material.ipynb`) | 9 (`container/RECORD.md`, `environment_reference.npz`, `environment_values.toml`, three figures, `figure1.svg`, both notebooks) |
| `scripts/` | 2 (`build_figures.py`, `build_site_figures.py`) | 0 |
| `work-packages/` | 2 (`interface-contract.md`, `interface-contract.toml`) | 0 |
| other | 1 (`claims_register.toml`) | 0 |

Totals: `204e7c3` 49 files, 1156 insertions, 1307 deletions; `5b01248` 10 files, 1091 insertions, 1056 deletions.

### The renamed identifiers (A2)

From the commit message of `204e7c3`: the package's `facet_` and `facet_share_` are `cell_` and `term_share_`;
`assign_facets`, `facet_step`, `facet_gap`, `facet_objective`, `single_facet_termination` are `assign_cells`,
`refit_step`, `term_gap`, `term_objective`, `single_term_termination`; `color="facet"` is `color="cell"`;
`info["facet"]` is `info["term"]`; the report prefix is "term k: "; the case's `facet_record` and `facet_table` are
`term_record` and `term_table`; `paper/paper_facets.py` is `paper/paper_terms.py`; the plotting label helper is
`cell_labels`. Each new name found in the tree now (files containing the name as a whole word):

| Name | `src/` | `examples/adcs/` |
|---|---|---|
| `cell_` | 1 | 3 |
| `term_share_` | 1 | 3 |
| `assign_cells` | 3 | 0 |
| `refit_step` | 2 | 0 |
| `term_gap` | 1 | 0 |
| `term_objective` | 1 | 0 |
| `single_term_termination` | 2 | 0 |
| `cell_labels` | 1 | 1 |
| `term_record` | 0 | 1 |
| `term_table` | 0 | 3 |

### Checks run now

| Check | Command | Output |
|---|---|---|
| R-4, no old name in the package | `grep -rn facet src/` | no output (exit status 1) |
| R-14, attribution | `git log --format=%B 204e7c3^..5b01248 \| grep -ci "co-authored-by\|generated"` | **3** (the scope expects 0) |
| R-14, attribution, the trailer alone | `git log --format=%B 204e7c3^..5b01248 \| grep -ci "co-authored-by"` | 0 |

The three lines the pattern matches (`grep -in`) are words, none an attribution line: the subject of `5b01248` ("...outputs
and figures **regenerated** in hts-paper..."), its body line "The **generated** recovery sentence's pin follows its word", and
the last line of the body of `204e7c3` ("The **generated** outputs follow from the container run"). The trailer search alone
returns 0. The R-14 command as the scope words it does not return 0 for this range; whether the check is the trailer or
the pattern is the reviewer's call.

### The container regeneration (`paper/container/RECORD.md`, the entry for WP24 push 1)

- Image `hts-paper` `9c8a0c616386` (`sha256:9c8a0c61638691f5374ec857604eabfc0f960aeef3a48a10caaf622082c779bc`), built by
  `sh paper/container/build.sh` at local head `541efcd` (31 s, cached layers); the previous image `8e91e07fb08f` removed
  in the same step. Every step `--network none`, in `hts-*` containers only; `hts-wp24` created, started and removed by
  name.
- `uv run python paper/paper_common.py` (3 s): the array `figure1_facet` is now `figure1_term`, bytes unchanged, the other
  eight arrays unchanged; `environment_values.toml` not rewritten by it.
- `uv run python paper/execute_notebooks.py` (116 s): both notebooks; 4 output cells of the paper and 12 of the supporting
  material change in words only; `tab-F-toolchain` prints the build commit.
- `sh paper/container/build-paper.sh` (5 s): the site built.
- `uv run python scripts/build_figures.py` (98 s): `fig-planes-k3` (segment labels "term 1" to "term 3") and `fig-nlemma`
  (its key) rewritten; the other figures and the two model views unchanged.
- `uv run python paper/figures/figure1.py`: `figure1.png` and `figure1.svg` (labels "term k", third pane "terms laid flat").
- Tests inside the image (`uv run pytest -q -n 4` on `test_paper`, `test_case`, `test_k_terms_case`,
  `test_paper_sources`, `test_paper_static_figures`, `test_narrative`, `test_claims_register`, `test_sensitivity`,
  `test_interface_contract`, `test_soft_fit`, 222 s): **399 passed, 1 failed, 4 skipped**. The failure was a pin of the
  generated recovery sentence still reading "facet"; corrected, then `uv run pytest -q tests/test_paper.py -k "figure1 or
  cr2_the_planted"` (20 s): **4 passed**.
- `PAPER_EXECUTE=1 uv run pytest -q tests/test_paper.py -k "perturbation or clean_kernel or term_order"` (406 s):
  **4 passed**.
- The record's ledger line, from an earlier entry of the same file (not a WP24 run): `uv run python -m experiments verify`,
  "34 entries (11 current); 0 drifts". RECORD.md carries no ledger run for this push; **R-5's "0 drifts" at the push-1 head
  is not recorded** in any file I could read.

### R-5 and R-6 evidence as the records state it

- No number of the paper moved (RECORD.md). Outputs change in words only (`5b01248` message).
- `examples/adcs/experiments/reports/sensitivity.json` was not re-run (its regeneration is the oracle's): keys renamed and
  the file re-serialized as the writer writes it (sorted keys); every number and string value equal under the rename;
  `test_sensitivity`'s comparison of the committed column with the live case results passed in the image.
- `tests/data/soft_fit_default_reference.npz`: 94 keys `.../facet_` and `.../facet_share_` renamed `.../cell_` and
  `.../term_share_`; all 1274 arrays equal in dtype, shape and value; `test_soft_fit` passed in the image (exact branch).
- `paper/environment_reference.npz`: `figure1_facet` is `figure1_term`, bytes unchanged.
- Figure 1's data hash: the key name enters the hash. New pin `ec68f512...` in the image; with the old key the same arrays
  give `4040cb8e...`, the earlier pin (macOS `d3a29d79...` against `f9d7219d...`); `paper/environment_values.toml` carries
  both, with the sentence that the key was "facet". The data are unchanged; the hash moved because the key name is in it.
- "Tests change by identifier and phrase only" (message of `204e7c3`); `tests/test_vocabulary.py`'s made-up term is "tile" (A9).
  I did not diff the test files for this review; the reviewer runs the R-6 command and the diff.

### Statement blocks touched

`claims_register.toml` (48 lines changed in `204e7c3`): the identifier-only edits of the `backing` and `note` fields, each
the old name replaced by its new one, for example `test_k_terms_recovers_planted_facets` is `..._planted_terms`;
`test_assignment_margin_values_and_duplicate_facets` is `..._duplicate_terms`; `test_k3_reports_one_per_facet_recover_planted_supports`
is `..._one_per_term_...`; and the notes "facet_ is argmax over the fitted scores..." read "cell_ is argmax..."; "exponents_,
facet_, coefficients_, facet_share_ exist at K=1 and K>1" reads "exponents_, cell_, coefficients_, term_share_ ...". The full
before and after is `git show 204e7c3 -- claims_register.toml`.
`paper/environment_values.toml`: the comment rows of the table of what moves, "facet planes" and "thin-facet rows" read
"term planes" and "thin-term rows"; the row "facet numbering, order of facet sizes and shares" reads "term numbering, ...";
the key `values.facet_numbered_tables` is `values.term_numbered_tables`; the Figure 1 hash sentence (above). Full diff:
`git show 204e7c3 5b01248 -- paper/environment_values.toml`.
The paper's and the supporting material's prose cells were **not** edited in this push (see below); their output cells
were regenerated (4 and 12, above).

### The tau = infinity sentences list

Not a push-1 item (no sentence of the paper was edited in push 1); the list belongs to the prose pushes.

### Deletions

- `examples/adcs/figures/k3_frontier_coordinates_{primary,stock}.png`, `k3_log_planes_{primary,stock}.png`,
  `k3_tensions_{primary,stock}.png` (six files; the directory no longer exists), and `k_terms.save_figures` with the helpers
  only it used (`log_plane_slices`, `cond_label`, `UNITS`). What they no longer do: they coloured the designs by cell, the
  cluster idiom `figure-review.md` forbids, and nothing read them (message of `204e7c3`); the paper's log-plane slices are
  drawn by `paper/figures/planes.py`. `run_regime` loses its `figs` argument and `make_figures`; `case.figures` pins no file.
- The nine `NN_name.png` pins of contract row 14's predecessor, whose files went with the WP7 case notebook in `4bd6bac`,
  leave the manifest in the same amendment (contract version 13 to 14), so the R-4 test asserts the directory holds exactly the
  pinned files (message of `204e7c3`). Contract check performed for the deletion: the pins left the manifest and the prose
  in the same commit (`git show 204e7c3 -- work-packages/interface-contract.md work-packages/interface-contract.toml`).

### Left for later pushes

- The paper's and the supporting material's prose cells: `grep -c facet` at this head gives 62 lines in `paper/paper.ipynb` and
  256 in `paper/supporting_material.ipynb` (notebook JSON lines, outputs included). The counts of 37 paper and 9 supporting
  prose cells are not stated in any file I read and are left out.
- `examples/adcs/model_v2/diagnostic_pair.py`: done by WP23's stream, `3ad66fe` (identifiers follow `term_table`, `cell_`,
  `term_share_`; the column-name regex dropped), as `WP24-decisions.md` assigned.
- `tests/test_narrative.py`: `204e7c3` added a `RENAMED` map (four names: `facet_objective`, `facet_gap`,
  `single_facet_termination`, `assign_facets`) resolving the renamed names the preserved sources keep. The map is still in
  `tests/test_narrative.py` at this head (`RENAMED` at line 132). `WP24-decisions.md` (06:35 and 06:45) records the driver's
  decision that the records take identifier edits and both test maps are dropped; the call on the test file itself is pending.

## Push 2 (derivations)

Pending; built locally on worktree wp24p2, held on the test_narrative call.

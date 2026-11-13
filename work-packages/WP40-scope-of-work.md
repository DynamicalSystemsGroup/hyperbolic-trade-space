# WP40 — Scope of work: release thinning and repository organization

| | |
|---|---|
| **Status** | DRAFT, for the assistant's approval. Approved only by the recorded act below; nothing is built before then. |
| **Supervisor (accountable)** | mzargham |
| **Repository** | `DynamicalSystemsGroup/hyperbolic-trade-space`; work on `dev` |
| **Approval record** | The assistant's approval, quoted verbatim in `work-packages/WP40-decisions.md` |
| **Acceptance record** | The supervisor's acceptance, quoted verbatim in `WP40-decisions.md`, after `WP40-review.md` |

## Purpose

The supervisor's direction, verbatim (`WP40-decisions.md`, 2026-11-13, 18:55): "stuff link this
'(docs/superpowers/notes/abstraction-gaps.md).' reads as LLM but i am also thinking that may just be that we've got a repo
a bit bloated with materials from the build and that some thinning and organizational cleanup is merited as we approach
our release".

The parenthetical-path half is WP38's residual pass (the checker gains the pattern; the three paths in the supporting
material go in the WP39 or Appendix H wake). This package is the other half: the repository a release reader meets. The
stage-1 readout (`WP40-rounds/inventory/readout.md`, 64aa577) found 65 MB of tracked bytes, 52 MB of them in
`work-packages/`, 44.7 MB of those 324 screenshots that no test or script reads, a README Layout list of seven entries that
omits eight top-level items, and a 49.4 MB `git archive`. Stage 2 is decided (`WP40-decisions.md`, 832f040, the assistant's
calls 1 to 8): screenshots leave the tree and git keeps them; the text of the record stays; ten build materials move under
`work-packages/`; superseded inventories go; the README says where things are. This package is the build, quality
control, integration and review of that. Head at scoping: `dev` at `832f040` or later.

## Goals

- G1. **A release reader meets a repository whose top level and README say where things are:** the README's Layout list
  names every top-level entry a stranger will see, in one line each, and `work-packages/README.md` opens with what the
  folder holds and that it is not needed to use the method.
- G2. **The build's materials are thinned:** the screenshots, the superseded inventories and the build-only notes and spike
  folders no longer sit in the places a reader of the method looks, and the checkout and the archive fall by the readout's
  figures.
- G3. **Nothing the record needs is lost:** the images stay retrievable from git by a named commit; every review,
  round and reader-run text stays; no decision record, claim, datum or paper input is touched; no reference to a moved or
  removed path remains anywhere.
- G4. **The drift is closed:** the three code comments that point at notes absent from the tree name something that exists
  or say nothing.

## Non-goals

- Any rewrite of git history, the pack (100.6 MiB) or any commit hash the records quote (call 6).
- Any change to the paper's content, figures, claims, numbers or the data of record; any edit to a decision record other
  than a path made to point at a moved file where the record names one as text (and then none: records keep their words;
  a path inside a record is left as quoted and the move table in D-5 is its key).
- Thinning the reviews', rounds' or reader runs' text (calls 2 and 3), the scopes of work, the driver log, the process
  documents or the contract.
- A pointer or index file standing in for removed text, a release asset, or a branch or tag for the images: the commit
  hash in the review file is the pointer (call 1).
- Anything in `WP11-*`: the held-out material is neither opened, moved nor described.
- Moving the eight convention notes or the six live notes (`abstraction-gaps.md`, `notation.md`, `paper-sources/`, the spikes
  with live imports); moving `CLAUDE.md`; renaming `docs/superpowers/`.
- The WP38 checker's new parenthetical-path pattern and the three supporting-material paths (WP38's and the notebook
  units').
- Anything under `src/` and `derivation/` beyond the two comment edits of D-7 (named there); `uv.lock`; the answer key.
- New prose beyond the Layout list, the `work-packages/README.md` header and one retrieval line per affected file.

## Deliverables

| ID | Deliverable | Serves |
|---|---|---|
| D-0 | This scope of work, committed and pushed alone | all |
| D-1 | **Screenshots out of the tree.** At the build's start head H, one commit adds to each review, round and readout file that embeds or lists images (the eight review directories, `WP30-rounds`, `WP26-view-editor-feedback`, `WP37-rounds`, and every other directory the build's grep finds holding png/jpg) one line: "Screenshots for this record: commit `H`, `git show H:<path>`" (or the directory form), then a second commit deletes the images. Embedded image links in markdown become the plain file name in backticks, so no link dangles. `work-packages/README.md` states the retrieval once, in two commands: `git show <H>:<path> > out.png` for one image and `git worktree add <dir> <H>` (then the folder is there in full) for a directory. No script | G2, G3 |
| D-2 | **Superseded inventories removed:** `WP25-inventory.md`, `WP25-5-inventory.md`, `WP28-inventory.md`, `WP28-cut-list.md` (the deleted rows are in git; the current tidiness record is this package). A one-line note in `work-packages/README.md` names them and the commit that last holds them. The WP28 reader-run directories (`WP28-inventory/`, `WP28-retest/`) stay | G2, G3 |
| D-3 | **Notes moved under `work-packages/`** (call 4), by `git mv`, to `work-packages/build-notes/`: `docs/superpowers/notes/adcs-port.md`, `opensysml-usage.md`, `system-model-tidy.md`, `view-editor-harness.md`; `paper-outline-v1-baseline.md`, `paper-outline-v2-search.md`, `search-prior-art.md` to `work-packages/outlines/`; the spike folders `spike-objective/`, `spike-certificates/` and `spike-container-platform/` to `work-packages/spikes/` (counts: see the defaults list) | G2 |
| D-4 | **Every path updated**, from a grep-verified list made at the build's start and kept in `WP40-rounds/build/paths.md`: the tests that name a moved path, the scripts, `claims_register.toml` rows, `docs/` links, the interface contract and its manifest if either names one, the paper's source map and `paper/prior_art.yaml` if they do, the notebooks' cells (D-8), `pyproject.toml`'s ruff exclusion for the spike folders, `paper/container/README.md` and `RECORD.md`, `abstraction-gaps.md`, `paper-sources/limitations.md` and `method.md`, `examples/adcs/experiments/probes/probe-record.md`, code comments, and the processes' documents (`PM-BRIEF.md`, `README.md`) | G3 |
| D-5 | **The move table** in `WP40-rounds/build/moves.md`: old path, new path, commit, for each moved or removed item. It is the key for the decision records and scopes that quote old paths and are not edited | G3 |
| D-6 | **README Layout list** per the readout's section 7 draft, with the correction of call 7: `history.yaml` is described as the record behind the history and acknowledgements page, not the release history; `work-packages/` described as the build's record (scopes, reviews, decisions) and not needed to use the method; `docs/superpowers/` described as the notes the checks apply. The entry-surface edit is listed in `supervisor-review-list.md` "Entry surfaces" with reason and commit. A short header at the top of `work-packages/README.md`: what the folder holds, what is in `build-notes/`, `outlines/`, `spikes/`, how to retrieve the screenshots, and that none of it is needed to use the method | G1 |
| D-7 | **Drift closed:** `tests/test_case.py` (the `superpowers/notes/k3-cubesat.md` comment), `derivation/PROOF_MAP_FINDINGS.md` and `derivation/lemma_16_soft_fit_alternation.py` (the `spike-soft-fit/` and `spike-ggp-fit/report.md` comments), each reworded to say what the removed thing recorded or repointed to a file that exists. Comment edits only; no code line changes | G4 |
| D-8 | **Notebook cells that name a moved path** (`paper/supporting_material.ipynb` for `spike-objective` and `spike-certificates` at the least; the build's grep says whether any cell of `paper/paper.ipynb` does), changed as one small unit through the paper notebook's single-writer queue, with the notebooks and `paper/figures/` in one commit | G3 |
| D-9 | **Before and after** in `WP40-rounds/build/before-after.md`: tracked bytes and file counts for the repository, by top-level directory and for `work-packages/`; screenshots counted; `git archive HEAD | wc -c` and gzipped, before and after | G2 |
| D-10 | `WP40-review.md` and `WP40-decisions.md` (the approval and the acceptance quoted) | all |

## Requirements

| ID | Requirement | Checked by |
|---|---|---|
| R-1 | No tracked png or jpg remains under `work-packages/`, and no image that a markdown page, a test or a script reads is removed (the readout found none; the build re-greps first, and an image that something reads stays and is listed) | `git ls-files work-packages | grep -E '\.(png|jpe?g)$'` is empty or lists only named readers; the grep list in `paths.md` |
| R-2 | Every file that embedded or listed a removed image names H and the retrieval; H holds all of them; a sample of ten is retrieved with `git show` and opened (images viewed) | `git grep` for the line over the touched files; the ten retrievals logged in the review |
| R-3 | No reference to a moved or removed path remains in a tracked file, other than the decision records, `driver-log.md`, scopes of work and reviews, which quote paths of their time and are keyed by the move table; each such residue is counted and listed by file | `git grep` for each old path (the move table is the pattern list) with the exempt classes excluded, empty; the exempt count reported |
| R-4 | Every repository path that the docs, the README, the paper sources, the notebooks' text and the tests name exists in the tree | a link and path check over `docs/`, `README.md`, `work-packages/README.md`, `paper/*.ipynb`, `docs/superpowers/notes/paper-sources/`, `tests/` (a throwaway script in the scratchpad; not committed), empty of misses |
| R-5 | The protected items are byte-identical to the build's start: the paper and what builds it except D-8, the data of record, the 42 `WP*-decisions.md` files, `driver-log.md`, `claims_register.toml` apart from path updates, `glossary.yaml`, `history.yaml`, the contract apart from any path update, everything in `WP11-*` | `git diff --stat H..HEAD -- <protected paths>` shows only the named edits; `git diff --name-only` has no `WP11-` entry and no `-decisions.md` entry |
| R-6 | The full fast suite, the site, docs, paper and claims tests, the interface-contract and text-encoding tests, ruff, format and lock pass | `uv run pytest -q -m "not slow"`; `uv run pytest -q tests/test_site.py tests/test_docs.py tests/test_paper.py tests/test_claims_register.py tests/test_interface_contract.py tests/test_text_encoding.py`; `uv run ruff check .`; `uv run ruff format --check .`; `uv lock --check` |
| R-7 | The build is measured: the before and after table for tracked bytes and file counts, and for `git archive` size, with the screenshot count falling from 324 to the number that stay | `before-after.md`; the commands in it |
| R-8 | The README Layout list names every top-level tracked entry (directories and files), one line each, and its links resolve; `history.yaml` is described as the record behind the history page; `work-packages/README.md` begins with the header | `ls` of the top level against the list; the link check of R-4; read |
| R-9 | The three drift comments no longer name an absent path | `git grep` for `k3-cubesat`, `spike-soft-fit`, `spike-ggp-fit` outside the exempt classes, empty; `git diff` of the two derivation files and `tests/test_case.py` shows comment lines only |
| R-10 | The vocabulary check and the residual checker's baseline do not rise | `uv run python scripts/check_vocabulary.py`; the WP38 checker, if landed, against its baseline |
| R-11 | No AI attribution; encoding clean | grep of `git log`; `tests/test_text_encoding.py` |

## Definition of good

- A stranger who clones or downloads the archive reads the README, knows in a minute what each top-level entry is and
  which they can ignore, and opens `work-packages/` to find a folder of text that says what it is. The archive is a
  fraction of its former size, and the build's record is not poorer: any image a record cites can be seen with one
  command.
- The moves read as a tidy, not a loss: a grep for any old name finds only the records that quote it, and the move table
  tells where it went.

## Definition of good enough

- D-1 to D-9 landed and R-1 to R-11 pass.
- A cold look at the README on the rendered site page and as markdown (the acceptance below) finds the Layout list
  accurate and its links alive.
- The cascade review finds the repository in a clean merged state: no dangling path, the suite green, the tree measured.

## Definition of done

Good enough is met, **no open item remains unresolved**, and the supervisor has accepted the work by the acceptance
record above.

## Sequencing

The build runs after WP39 lands and before the final reader round, so no reader meets a moving path; the residual pass
(WP38) runs on the surfaces after it. The build touches paper-adjacent files, so D-8 (any notebook cell that names a moved
path) is one small unit in the paper notebook's single-writer queue, after the units already in it; while a gate's
container regression runs, nothing that regenerates paper outputs is pushed (D-8 changes text, not outputs, and waits
all the same if the PM says so). The rest of the build touches no notebook and can run in its own worktree concurrently
with units that do not edit the same files; it rebases on `origin/dev` before each push and re-runs the grep of R-3 after
the rebase, because a unit landing meanwhile may add a reference to a path that has moved.

## Lifecycle stages

(1) Research spike: done (the inventory and readout, `WP40-rounds/inventory/`, 64aa577). (2) Decide: done
(`WP40-decisions.md`, 832f040). (3) Build: D-1 to D-9 in the order: the path list and move table; the pointer lines at H;
the moves and removals; the path updates; the Layout list and header; the drift comments; D-8 through the queue; the
measure. (4) Quality control: R-1 to R-11. (5) Integrate: the review-list row for the entry surface, `CHANGELOG.md` if it
names the moved notes, the retrieval note. (6) Review the cascade to a clean merged state: a fresh reviewer retrieves the
sample of ten images, runs the greps and the suite, and reads the README on the rendered site page and as markdown, with
screenshots; `WP40-review.md`.

## Agents and models

Sonnet for the implementer, the path-update unit and the reviewer; Haiku for the counts, the greps, the file moves and
the before-and-after table. No sub-agent without the PM. Nobody opens `WP11-*`. The reviewer works in its own worktree
under the scratchpad and is not the builder.

## Agent's defaults

One item for the assistant: the destination folders (`work-packages/build-notes/`, `work-packages/outlines/`,
`work-packages/spikes/`); `spike-container-platform/` moving with the two spike folders (the readout names it "goes or
stays", the decision's count of ten items, five notes plus three outline notes plus two folders, matches four build notes
and three folders; if the build finds a fifth note or a different count it reports and does not guess); the screenshot
pointer line's wording and the retrieval commands in `work-packages/README.md`; H being the build's start head and the
pointer commit sitting just before the removal commit; the build's records in `WP40-rounds/build/` (`paths.md`,
`moves.md`, `before-after.md`); the throwaway link-check script kept in the scratchpad; the sample of ten images drawn
across at least five review directories; `CHANGELOG.md` edited only if it names a moved path.

## Open decisions (for the assistant)

None. Every item was resolved through the decision loop (`WP40-decisions.md`: the direction, and stage 2's calls 1 to 8).

## Blast radius

- New: `WP40-rounds/build/` (`paths.md`, `moves.md`, `before-after.md`), `WP40-review.md`, `WP40-decisions.md` entries,
  the folders `work-packages/build-notes/`, `outlines/`, `spikes/`.
- Moved or removed: the screenshots under `work-packages/` (324), the four superseded inventory files, the ten notes and
  spike folders of D-3.
- Edited: the review, round and readout markdown that embeds images (one line each); `README.md` (Layout list; an entry
  surface, listed); `work-packages/README.md` (header); `tests/` files and `scripts/` that name a moved path (path strings
  only); `claims_register.toml`, `paper/prior_art.yaml`, `docs/` pages, the contract and manifest where they name a moved
  path (paths only); `pyproject.toml` (the ruff exclusion path only; the standing rule against editing it is lifted for
  this one line by this scope); `derivation/PROOF_MAP_FINDINGS.md` and `derivation/lemma_16_soft_fit_alternation.py`
  (comments only; if either is pinned by a hash or ledger the build reports it and does not edit);
  `paper/supporting_material.ipynb` (D-8, through the queue); `supervisor-review-list.md`.
- Never: the decision records' text, `driver-log.md`, the paper's prose and figures, the data of record, `src/`, `uv.lock`,
  `WP11-*`, the answer key, the `verify` and `stage` worktrees, tab-23.

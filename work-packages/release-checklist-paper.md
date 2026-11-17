# Release checklist: the paper

The paper's lifecycle on the `paper` branch (`work-packages/WP65-design/specification.md` (`git show 4f81a4ea:work-packages/WP65-design/specification.md`), section 2): modes
`abstract`, `working`, `submitted`, `revision`, a pin per `paper-*` tag, published by `.github/workflows/paper.yml`.
The software's list is `release-checklist-software.md`. Rows keep their numbers from `WP8b-release-checklist.md`
(suffix `p` where a row was split between the two lists); rows M, L and P are the paper's own. State: `-` not done;
otherwise a short word (done, part, rule, accepted) with the commit or record that shows it. States are those of
`WP8b-release-checklist.md` (read at dev `c23cf60`) unless a newer record is named. Paths are under
`work-packages/` unless they start with `.github/`, `paper/`, `scripts/` or `tests/`.

## M. Changing mode (one row per change; each is a pin)

| # | Item | Command or evidence | Owner | State | Source |
|---|---|---|---|---|---|
| M1 | `abstract` to `working`: prepare the pin on `paper`, write its section in `paper/CHANGES.md`, push (the branch build green), tag, record the checksum and the DOI, merge `dev` into `paper` and `paper` into `dev` | `uv run --no-project python scripts/paper_pin.py prepare --tag paper-working-<YYYYMMDD>`; `git tag <tag> && git push origin <tag>`; `scripts/paper_pin.py record --tag <tag> --doi 10.5281/zenodo.<n>` | assistant | - (mode `abstract` at 0.1) | spec 2.4; `WP64-decisions.md`, his direction 12:30 and his approval of the abstract |
| M2 | A later working pin (the paper iterated): the same steps with a new date, or `-2`, `-3` on the same day | as M1 | assistant | - | spec 2.3 (the working shape) |
| M3 | `working` to `submitted`: the same steps with `paper-submitted-<venue>`, after rows C1 to C5 at the commit to be tagged and rows D1 to D4 on the paper at that commit | as M1; `paper/container/RECORD.md` names the commit | assistant | - | spec 2.4, 2.5; `WP64-decisions.md`, his direction 12:30 ("pin it to align with a submission") |
| M4 | `submitted` to `revision`, once per round: `paper-revision-<venue>-r<n>`, after rows C1 to C5 | as M1 | assistant | - | spec 2.3, 2.5; `WP64-decisions.md` ("pin it again to deal with peer-review type revisions") |
| L1 | The paper's links to repository files point at `dev` while the paper iterates and at `main` from the paper's release on; before a pin's tag the generators' constants (`REPO_BLOB` in `paper/paper_common.py`, `BLOB` in `paper/generate_proofs.py`) name `blob/main/`, which `paper/pin_links.py` rewrites to the tag in the published artefact | `grep -c 'hyperbolic-trade-space/blob/main/' paper/paper.ipynb paper/supporting_material.ipynb`; the `pin_links` count in the tag run's log | assistant | - (the notebooks name `blob/main/`, 2,482 links, at WP66b's head) | `WP64-decisions.md`, Q1 ("you can reference dev for now"); spec 2.7 |

## B. Local checks on the paper's head

| # | Item | Command or evidence | Owner | State | Source |
|---|---|---|---|---|---|
| B2p | Vocabulary check clean on the paper's surface | `uv run python scripts/check_vocabulary.py --surface paper` exits 0 | agent | done c0fe11b for the whole (0 new, 61 known); WP66b's head: 0 new, 39 known on `paper` | spec 5.2; `WP30-gate-checklist.md`, step 15 |
| B3p | The register holds for the paper's rows | `HTS_PAPER_TESTS=1 uv run pytest -q tests/test_claims_register.py -m paper` | agent | done 116c929 for the whole register | spec 5.2; `WP8b-decisions.md`, "Claims register after the D-6 citations" |
| B4p | No attribution line in any commit on `paper`; no tag but the pin's | the attribution step of `.github/workflows/paper.yml`; `git tag --list 'paper-*'` | agent | part: 0 matches since 8e846a9 at c0fe11b | spec 6.3 (B4 both); `.github/workflows/test.yml` (the step copied verbatim) |

## C. The container re-pin gate (before a `submitted` or `revision` tag)

| # | Item | Command or evidence | Owner | State | Source |
|---|---|---|---|---|---|
| C1 | Build `hts-paper` and `hts-alt` from the commit to be tagged | `sh paper/container/build.sh`; `sh paper/container/build.sh hts-alt` | assistant | done c64430e (WP30 gate; none at a pin) | spec 2.5; `WP30-gate-checklist.md`, step 14 and Gaps row 2 (option B) |
| C2 | Ledger entries regenerated in `hts-paper`; 0 drifts | `PYTHONPATH=examples/adcs uv run python examples/adcs/model_v2/ledger_gate.py --image <id> --wp30 regen`; `PYTHONPATH=examples/adcs uv run python -m experiments verify` | assistant | done c64430e (`RECORD.md`: 74 entries, 0 drifts) | `WP30-gate-checklist.md`, steps 8 and 14 |
| C3 | Paper executed in the container; exact outputs re-pinned; full suite in `hts-paper` and `hts-alt`, 0 failed | `docker run ... build-paper.sh`; `docker run --rm --network none hts-paper uv run pytest -q -n 4` | assistant | part c64430e: `hts-paper` regeneration and tests; `hts-alt` not in that section | spec 2.5; `paper/container/README.md` |
| C4 | Container record: the commit, the `uv.lock` hash, every re-pinned file old and new, "regression landed" | `paper/container/RECORD.md` | assistant, PM | part c64430e (no "regression landed" line found) | spec 2.5; `WP30-gate-checklist.md`, step 14 |
| C5 | A cold reproduction from Appendix F alone regenerates the committed numbers and figures | commands in Appendix F and `paper/container/README.md`; result in the container record | assistant | - | `release-candidate.md`, "What candidate means"; `deliverables-grid.md`, Paper appendices |
| C9p | Appendix F states what runs where (the paper's tests in the paper's workflow, the platform of record linux/arm64) | read Appendix F | PM | - | spec 6.3 (C9 both); `release-candidate.md`, "Windows" item (5) |

## D. Reader and answer-key gates (on the paper at a pin)

| # | Item | Command or evidence | Owner | State | Source |
|---|---|---|---|---|---|
| D1 | Answer key written outside the repository; its SHA-256 committed in `WP11-decisions.md` before any reader that uses it runs; never shown to authors | hash line in `WP11-decisions.md` | assistant, PM | done 77084fa (version 5) | `WP30-gate-checklist.md`, step 13 |
| D2 | Reader round on the paper at the pin, depths A to D, grid including P7 and P8; change requests landed | round record under `WP11-*` | assistant | part: 46 core and 12 held-out reads at c23cf60 (`WP11-final/`) | spec 6.3 (the reader round reads the paper at a pin); `PM-BRIEF.md`, "Mathematical presentation" |
| D3 | Reader grid stopping rule met; held-out cells read once; whole grid reported with its worst cells | grid report | assistant | part: held-out cells read once; whole-grid report not written | `release-candidate.md`, "What candidate means" |
| D4 | The expert and novice mathematics pair read at a named head before the round, triaged together | read and triage records | assistant | - | `PM-BRIEF.md`, "Mathematical presentation, expert and novice" |

## E. The build and the browser

| # | Item | Command or evidence | Owner | State | Source |
|---|---|---|---|---|---|
| E2 | A clean checkout of `paper` builds the paper on the pinned article theme | the `build` job of `.github/workflows/paper.yml` on a push to `paper` | agent | - | spec 2.2; `WP8b-scope-of-work.md`, Amendment 1, R-14 |
| E3p | Browser pass on the built paper at the pin (the artefact staged with `--artefact`), desktop and 375 px, light and dark, the banner read; screenshots in the record | `uv run python scripts/stage_site.py --artefact paper-html.tar.gz` | assistant | - | spec 3.2, 6.3; `PM-BRIEF.md` ("Reviews run the thing") |
| E4 | Tab rules for the browser pane | the software list's row E4 | PM, agent | rule | `release-checklist-software.md`, E4 |
| E5 | Paper figures need not read on a phone | n/a (accepted) | PM | accepted (`WP8b-decisions.md`, G-4) | `WP8b-decisions.md`, "Amendment 1 review", G-4 |

## F, G. The guide and the links

| # | Item | Command or evidence | Owner | State | Source |
|---|---|---|---|---|---|
| F3p | The paper's reviewer's guide: the pin, its tag and release, the mode it enters; the paper at the pin; the reader round and the container record; the calls on the paper | `reviewers-guide/paper/` | assistant | - (the one guide refreshed on branch guide-refresh; recut at WP69) | spec 6.5 |
| G2p | After a pin's release: fetch every GitHub link of the published paper, unauthenticated (the repository is public); all 200 | extract the `github.com` links from the unpacked `paper-html.tar.gz`; `curl -s -o /dev/null -w '%{http_code}' -L <url>` for each | assistant | - | spec 6.2 (G2: public), 6.3 |

## P. The pin's release

| # | Item | Command or evidence | Owner | State | Source |
|---|---|---|---|---|---|
| P1 | `paper/mode.toml` checks for serving | `uv run --no-project python scripts/paper_mode.py check --stage served` | agent | done at WP66b's head (`abstract`) | spec 3.1, 6.3 |
| P2 | The pin's release names both assets (`paper-html.tar.gz`, `paper-keys.json`) and the DOI Zenodo minted is in `paper/mode.toml` | `gh release view <tag> --json assets`; `scripts/paper_pin.py record` | assistant | - | spec 2.2 (`release`), 2.4, 6.3 |

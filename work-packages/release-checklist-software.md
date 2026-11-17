# Release checklist, the software (0.1)

Working document, not for users. The software's release is the merge of the pull request from `dev` into `main`
(`WP65-design/specification.md` (`git show 4f81a4ea:work-packages/WP65-design/specification.md`), section 1); this list holds the rows that decide it. The paper's rows are in
`release-checklist-paper.md`. Both replace `WP8b-release-checklist.md` (specification 6.3): each row keeps its old
number, with `s` where the old row was split between the two lists, and the rows added for the new model are R1 and
R2. Every row is sourced. State, read at dev `5e85196b`: `-` not done; otherwise a short word with the commit or
record that shows it. Owner: assistant (the driver, in the files' wording), PM, or agent (a Sonnet implementer or
reviewer). Paths are under `work-packages/` unless they start with `.github/`, `paper/`, `scripts/` or `tests/`.

## A. Version, changelog, lock

| # | Item | Command or evidence | Owner | State | Source |
|---|---|---|---|---|---|
| A1 | Version 0.1.0 in `pyproject.toml`, `uv.lock`, `src/tradespace/__init__.py` `__version__` and `CITATION.cff` (with `date-released`); last of the release items | `grep -n version pyproject.toml CITATION.cff`; `uv run python -c "import tradespace as h; print(h.__version__)"`; `uv lock --check` | assistant | - (0.0.1) | `WP8b-scope-of-work.md`, D-5 and R-5; `WP65-design/specification.md`, 6.2 (`CITATION.cff`) |
| A2 | Changelog heading `[Unreleased] - target 0.1.0` becomes `[0.1.0] - <date>`; the "Not yet released" lines go; nothing reads "Unreleased" or "target" | `grep -n -i 'unreleased\|target' CHANGELOG.md`; the release workflow's `changelog --final` check on the pull request | assistant | - | `WP8b-scope-of-work.md`, Amendment 1, D-2 and R-11; `WP65-design/build-plan.md`, section 6 |
| A3 | Changelog names every package that changed what a user sees, WP19 on; the paper's packages are named in `paper/CHANGES.md` from the first pin | `grep -o 'WP[0-9]*[a-z]*' CHANGELOG.md \| sort -u` against `release-candidate.md`'s path | PM | - | `WP8b-scope-of-work.md`, R-11; `WP65-design/specification.md`, 6.3 |
| A4 | Punch list has no line the tree contradicts; its "Version 0.1.0" box ticked with the version step | read `release-punch-list.md` beside `git log` | PM | done at 6b487929 | `WP8b-scope-of-work.md`, R-12; `WP8b-review.md`, G-1 |
| A5 | LICENSE is MIT, Dynamical Systems Group, agrees with `pyproject.toml` and `CITATION.cff` | `head -5 LICENSE`; `grep -n license pyproject.toml CITATION.cff` | agent | done at 5e85196b | `WP8b-scope-of-work.md`, R-1 |
| A6 | Lock check passes | `uv lock --check` | agent | done at 5e85196b | `WP8b-scope-of-work.md`, R-10; `CLAUDE.md`, Tooling |

## B. Local checks on the head

| # | Item | Command or evidence | Owner | State | Source |
|---|---|---|---|---|---|
| B1 | The software suite (paper tests deselected), lint, format, lock, lemma chain and proof-map checker pass on this machine | `uv run pytest`; `uv run ruff check .`; `uv run ruff format --check .`; `uv lock --check`; `uv run python -m derivation.proofmap` | agent | done at ab8fc0f9 (`WP68-rounds/checks.md`: the suite 2,465 passed; lemma chain and proof map pass; lint, format, lock) | `release-candidate.md`, "What candidate means"; `WP65-design/specification.md`, 5.1 |
| B2s | Vocabulary check clean on the software surfaces | `uv run python scripts/check_vocabulary.py --surface software --baseline scripts/vocabulary_baseline.toml` exits 0 | agent | done at ab8fc0f9 (0 new, 28 known) | `WP65-design/specification.md`, 5.2; `CLAUDE.md`, Derivations and docs |
| B3s | Claims register holds for the software surfaces | `uv run pytest -q tests/test_claims_register.py` (the software test runs without the paper switch) | agent | done at ab8fc0f9 (22 passed) | `WP65-design/specification.md`, 5.2 |
| B4s | No attribution line in any commit; no tag but the ones the two release workflows make | `git log --format=%B \| grep -ciE '\bco-authored-by\b\|\bgenerated with\b'` is 0 (the step in `test.yml`); `git tag` | agent | `git tag` empty at 5e85196b | `WP8b-scope-of-work.md`, R-9; `.github/workflows/test.yml` (attribution step) |
| B5 | Reference keys from the manifest: docs build strict in both slots; an undefined key fails | `HTS_PAPER_SLOT=abstract uv run --group docs mkdocs build --strict`; the same with `pin` | agent | done at ab8fc0f9 (both slots strict, exit 0) | `WP8b-scope-of-work.md`, Amendment 1, R-13; `WP65-design/specification.md`, section 4 |

## C. CI

| # | Item | Command or evidence | Owner | State | Source |
|---|---|---|---|---|---|
| C6 | CI on the release pull request: `test (fast)`, `test (slow)`, `test (docs)` and `admissibility` green | the pull request's checks; run links in the release issue | assistant | - | `.github/workflows/test.yml` (matrix `shard: [fast, slow, docs]`); `WP65-design/specification.md`, 1.1 and 5.3 |
| C7 | CI on Windows at the head: fast and slow shards by dispatch (never on a pull request); the docs shard stays on Linux, with the reason stated in the README | `gh workflow run test.yml --ref dev -f windows=true` | assistant | done at 7e6839a0 (run 44051921030) and at f305f548 after the rename (run 44133871912: Linux shards, Windows fast and slow green) | `WP34-decisions.md`, "Stage (2)", Option 2; `release-candidate.md`, "Windows" |
| C8 | macOS through the maintainer's tier 2 watcher on this Mac, verdict in `driver-log.md` at the head | the watcher's verdict at the named head | assistant | - | `PM-BRIEF.md`, "Verification in tiers" |
| C9s | README states what runs where, for the software | read `README.md` | PM | - | `release-candidate.md`, "Windows" item (5); `WP65-design/specification.md`, 6.3 |
| C10 | CI runs on the release pull request and when the release workflow calls it (every shard); a push to `dev` runs lint and the Linux fast shard only | n/a (rule) | PM | rule | `PM-BRIEF.md`, "Verification in tiers"; `WP65-design/specification.md`, 5.3 |
| R2 | A dry run of the release on a `qc/` branch is green at the head: admissibility, the suite, the build and the site; nothing after them runs | `git push origin HEAD:qc/release`; the run's summary names the slot `abstract` | assistant | done at ab8fc0f9, at f305f548 after the rename (run 44134005344) and at 19c7e528 after WP78 with the `controls` job first (run 44153489031, green; the TestPyPI rehearsal 44153488933 at the same head published `tradespace` 0.1.0 to the test index through the `testpypi` environment: trusted publishing proven end to end); earlier run 44134005344 ( admissibility, build, the three shards, the site compose green; the rest skipped; `qc/release` deleted); earlier run 44069685478 ( admissibility, build, the three shards, the site compose green; tag, publish, deploy, release, on-failure skipped; the branch deleted) | `WP65-design/specification.md`, 6.3 and section 9, item 1; `WP65-design/build-plan.md`, section 4 |

## D. The grid

| # | Item | Command or evidence | Owner | State | Source |
|---|---|---|---|---|---|
| D5 | Deliverables grid current; printed whole in the handover | `deliverables-grid.md` | PM | - | `release-candidate.md`, "The deliverables grid"; `status-report-template.md` |

## E. The staged site and the browser

| # | Item | Command or evidence | Owner | State | Source |
|---|---|---|---|---|---|
| E1 | Site staged at the named head, `/paper/` as it will deploy: the abstract page (`--slot abstract`) or the pin's artefact (`--artefact`) | `uv run python scripts/stage_site.py --serve` | PM or assistant | done at 7e6839a0 (`WP68-rounds/record.md`) | `WP65-design/specification.md`, 3.4; `WP8b-decisions.md`, "The strict paper build" |
| E3s | Full browser pass on the staged root page, docs and `/paper/` slot, desktop and phone width (375 px), light and dark, findings fixed or listed; screenshots in the release issue's record | own tab, screenshots as files under the review record | assistant | done at 7e6839a0 (sixteen captures, `WP68-rounds/captures/`); the pinned modes at WP67 | `release-candidate.md`, "What candidate means"; `PM-BRIEF.md` ("Reviews run the thing") |
| E4 | Tab rules: any agent needing the browser pane creates its own tab and closes it; nobody navigates another's tab (the paper's list points here) | n/a (rule) | PM, agent | rule | `pm5-rules.md`, "Rules added 2026-11-10"; `PM-BRIEF.md` |

## F. The merge and the hand-off

| # | Item | Command or evidence | Owner | State | Source |
|---|---|---|---|---|---|
| R1 | His keyboard items done and read back: the `main`, `dev` and `paper` rulesets, the four environments, Pages from GitHub Actions, the PyPI and TestPyPI pending publishers; Zenodo stays off for 0.1 (his word, 2026-11-17) | `gh api repos/DynamicalSystemsGroup/tradespace/rulesets`; `.../environments`; `.../pages`; the publishers and Zenodo read in their pages | assistant (read-back), the supervisor (settings) | done 2026-11-17: his five steps with a screenshot each, read back in `WP68-rounds/record.md` G7 (Pages on the workflow; four environments; four rulesets); the publishers by his screenshots; Zenodo off | `WP65-design/his-items.md`; `docs/code-owners.md`, "Repository settings" |
| F1 | The release is the merge of the pull request from `dev` into `main`, closing the release issue, with the staged-site review recorded there; the merge commit's message names the packages carried | the pull request; the release issue; the Release run on the merge commit green | the supervisor (merge), assistant (pull request, issue) | - | `WP65-design/specification.md`, 1.1; `README.md` (work-packages), Branching |
| F2 | (No PR from us) The candidate is dev at a named head, with the review list and the reviewer's guide; the chief engineer opens or merges the PR after his review | n/a | chief engineer | - | `release-candidate.md`, "The mandate" and "extended" ("don't make the pull request") |
| F3s | The software's reviewer's guide (`reviewers-guide/software/`): the release pull request, the staged site, the code and the derivations, the calls made for him and his keyboard items | open each entry point after staging | assistant | - | `WP65-design/specification.md`, 6.5 |
| F4 | Guide lists every call with its evidence, every changed number with its reason, what is known weak | compare with `supervisor-review-list.md`, `driver-log.md`, `swap-evidence.md` | assistant | - | `WP8b-scope-of-work.md`, R-8; `release-candidate.md`, "What candidate means" |
| F5 | `supervisor-review-list.md` current: every call with record and landing commit | read | PM | - | `release-candidate.md`, "The mandate, extended"; `supervisor-review-list.md`, header |
| F6 | Repository tidiness instance before the pull request | the tidiness inventory executed on approval | agent | - | `release-candidate.md`, step 3h ("one before the PR") |
| F7 | No tag but the one `release.yml` creates; nothing published but what the Release run publishes: no registry image, no PDF export | `git tag`; the run's jobs | assistant | `git tag` empty at 5e85196b | `WP65-design/specification.md`, 1.2 and section 8 (C13); `release-candidate.md`, "Already decided" |

## G. After the merge

Each row names what it catches that the earlier rows cannot, because it is only visible once the merge, the tag and
the deploy exist.

| # | Item | Command or evidence | Owner | State | Source |
|---|---|---|---|---|---|
| G1 | After the tag: reload a docs page once and watch for a 404 from the releases widget (the widget asks for a release that did not exist before the tag, so no staged build shows it) | open any docs page in a fresh tab after the release; browser console and network list show no 404 for the releases request; record the screenshot | assistant | - | `PM-BRIEF.md`, handover of the thirteenth PM, open item 6 |
| G2s | After the merge: fetch every GitHub link on the site and the README, unauthenticated (the repository is public; the links resolve once `main` holds the paths they name) | extract the `github.com` links from the deployed site and `README.md`, then `curl -s -o /dev/null -w '%{http_code}' -L <url>` for each; all 200 | assistant | - | `PM-BRIEF.md`, handover of the thirteenth PM, open item 6; `WP65-design/specification.md`, 6.2 |

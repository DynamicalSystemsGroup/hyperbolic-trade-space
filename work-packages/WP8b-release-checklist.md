# WP8b release checklist, 0.1 candidate (DRAFT, for the PM)

Working document, not for users. Every row is sourced; a row is here only if a file supports it. State: `-` not
started. Owner: assistant (the driver, in the files' wording), PM, or agent (a Sonnet implementer or reviewer).
Paths are under `work-packages/` unless they start with `.github/`, `paper/`, `scripts/` or `tests/`.

**Read first.** The mandate of 2026-11-11 10:00 changed the end state: "don't make the pull request" ... the package is
`dev` at a named head, the list of calls and the reviewer's guide in sittings (`release-candidate.md`, "The mandate,
extended"). The earlier path still lists step 7, "The PR from `dev` to `main`" (`release-candidate.md`, "The path
to the candidate"). Rows below marked (PR) apply only when the supervisor asks for the PR.

## A. Version, changelog, lock

| # | Item | Command or evidence | Owner | State | Source |
|---|---|---|---|---|---|
| A1 | Version 0.1.0 in `pyproject.toml` (now 0.0.1), `uv.lock`, `src/hyperbolic_trade_space/__init__.py` `__version__` (now 0.0.1); last of the release items | `grep -n version pyproject.toml`; `uv run python -c "import hyperbolic_trade_space as h; print(h.__version__)"`; `uv lock --check` | assistant | - | `WP8b-scope-of-work.md`, D-5 and R-5 ("D-5 last, so the version is not set before the content is") |
| A2 | Changelog heading `[Unreleased] - target 0.1.0` (today's `CHANGELOG.md` heading) becomes `[0.1.0] - <date>`; the "Not yet released" lines go; nothing reads "Unreleased" or "target" | `grep -n -i 'swap\|unreleased\|target' CHANGELOG.md` | assistant | - | `WP8b-scope-of-work.md`, Amendment 1, D-2 and R-11; `WP8b-decisions.md`, "Amendment 1 review", G-1 |
| A3 | Changelog names every package that changed what a user or reader sees, WP19 on; WP31 enters when accepted (accepted 1d26560); later packages (WP29 to WP34) checked the same way | `grep -o 'WP[0-9]*[a-z]*' CHANGELOG.md \| sort -u` against `release-candidate.md`'s path | PM | - | `WP8b-scope-of-work.md`, R-11; `WP8b-decisions.md`, "Amendment 1 review", G-3 ("WP31 enters the changelog when it is accepted") |
| A4 | Punch list has no line the tree contradicts; its "Version 0.1.0" box ticked with the version step | read `release-punch-list.md` beside `git log`; `uv run pytest -q tests/test_site.py -k "punch or link"` | PM | - | `WP8b-scope-of-work.md`, R-12; `WP8b-review.md`, G-1 |
| A5 | LICENSE is MIT, Dynamical Systems Group, agrees with `pyproject.toml` | `head -5 LICENSE`; `grep -n license pyproject.toml` | agent | - | `WP8b-scope-of-work.md`, R-1 |
| A6 | Lock check passes | `uv lock --check` | agent | - | `WP8b-scope-of-work.md`, R-10; `CLAUDE.md`, Tooling |

## B. Local checks on the head

| # | Item | Command or evidence | Owner | State | Source |
|---|---|---|---|---|---|
| B1 | Whole suite, lint, format, lock, lemma chain and proof-map checker pass on this machine | `uv run pytest`; `uv run ruff check .`; `uv run ruff format --check .`; `uv lock --check`; `uv run python -m derivation.proofmap` | agent | - | `release-candidate.md`, "What candidate means"; `WP8b-scope-of-work.md`, R-10; `paper/container/README.md` (proofmap command) |
| B2 | Vocabulary check clean | `uv run python scripts/check_vocabulary.py --baseline scripts/vocabulary_baseline.toml` exits 0 | agent | - | `WP30-gate-checklist.md`, step 15; `CLAUDE.md`, Derivations and docs |
| B3 | Claims register holds | `uv run pytest -q tests/test_claims_register.py` | agent | - | `WP8b-decisions.md`, "Claims register after the D-6 citations"; `WP30-gate-checklist.md`, step 15 |
| B4 | No attribution line in any commit; no tag, deployment or publication | `git log --format=%B \| grep -ciE '\bco-authored-by\b\|\bgenerated with\b'` is 0; `git tag` empty | agent | - | `WP8b-scope-of-work.md`, R-9; `.github/workflows/test.yml` (attribution step); `release-candidate.md`, "What candidate means" |
| B5 | Reference keys: docs build strict; undefined key fails | `uv run --group docs mkdocs build --strict` | agent | - | `WP8b-scope-of-work.md`, Amendment 1, R-13; `WP8b-review.md`, D-6 rows |

## C. Container and CI (the gate)

| # | Item | Command or evidence | Owner | State | Source |
|---|---|---|---|---|---|
| C1 | Container regression at the gate, option B (container to container): build `hts-paper` and `hts-alt` from a committed HEAD | `sh paper/container/build.sh`; `sh paper/container/build.sh hts-alt` | assistant | - | `WP30-gate-checklist.md`, step 14 and Gaps row 2 (option B); `PM-BRIEF.md`, "The container is a gate check, not a unit step"; `release-candidate.md`, "What candidate means" |
| C2 | Ledger entries regenerated in `hts-paper`; 0 drifts | `PYTHONPATH=examples/adcs uv run python examples/adcs/model_v2/ledger_gate.py --image <id> --wp30 regen` (spelled out in `paper/container/README.md`); `PYTHONPATH=examples/adcs uv run python -m experiments verify` | assistant | - | `WP30-gate-checklist.md`, steps 8 and 14; Gaps row 8 |
| C3 | Paper executed in the container; exact outputs re-pinned; full suite in `hts-paper` and `hts-alt`, 0 failed | `docker run ... build-paper.sh`; `docker run --rm --network none hts-paper uv run pytest -q -n 4` | assistant | - | `WP30-gate-checklist.md`, step 14; `paper/container/README.md` |
| C4 | Container record: every re-pinned file, old and new; "regression landed" announced, freeze lifted | `paper/container/RECORD.md` | assistant, PM | - | `WP30-gate-checklist.md`, step 14 ("PM announces regression landed"); the rules file `pm5-rules.md` in the scratchpad (2026-11-10 afternoon: no push regenerating paper outputs during the regression) |
| C5 | A cold reproduction from Appendix F alone regenerates the committed numbers and figures | commands in Appendix F and `paper/container/README.md`; result in the container record | assistant | - | `release-candidate.md`, "What candidate means"; `deliverables-grid.md`, Paper appendices (Appendix F: "not yet recorded") |
| C6 | CI on Linux at the head: fast, slow, docs-paper shards green | `gh workflow run test.yml --ref dev`; run link in the review record | assistant | - | `.github/workflows/test.yml` (matrix `shard: [fast, slow, docs-paper]`); `WP34-scope-of-work.md`, item 6 Review ("the three platforms green at one named head, the run links, the shards table") |
| C7 | CI on Windows at the head: fast and slow shards; docs-paper stays Linux and macOS, with the reason stated in the README and the reproducibility appendix | `gh workflow run test.yml --ref dev -f windows=true`; stage 4 folds the Windows job into the matrix at gates | assistant | - | `WP34-decisions.md`, "Stage (2)", Option 2; `release-candidate.md`, "Windows", items (2), (4), (5), (6) |
| C8 | CI at the head: Linux, and after WP34 stage 4 Windows (fast and slow); macOS through the maintainer's tier 2 watcher on this Mac, verdicts in `driver-log.md` | the watcher's verdict at the named head, recorded in `driver-log.md` | assistant | - | `PM-BRIEF.md`, "Verification in tiers" (tier 3: "both platforms green on the exact commit"); `driver-log.md`, row of 2026-11-11 on f5e329f ("the tier 2 watcher on this Mac") |
| C9 | README and reproducibility appendix state what runs where | read both | PM | - | `release-candidate.md`, "Windows" item (5); `deliverables-grid.md`, README row ("the what-runs-where line waits on the Windows package") |
| C10 | CI never dispatched per push, only per batch and at gates | n/a (rule) | PM | - | `PM-BRIEF.md`, "Verification in tiers" ("Never dispatch the Linux run per push") |

## D. Reader and answer-key gates

| # | Item | Command or evidence | Owner | State | Source |
|---|---|---|---|---|---|
| D1 | Answer key v5 written by the assistant outside the repository; its SHA-256 committed in `WP11-decisions.md` before any reader or reviewer that uses the key runs; never shown to authors | hash line "Answer key, version 5" in `WP11-decisions.md` | assistant, PM (commits the hash) | - | `WP30-gate-checklist.md`, step 13; `WP11-decisions.md` (versions 1 to 4, key held outside the repository) |
| D2 | Final reader round on the finished paper and docs at depths A to D, grid including P7 and P8; change requests landed | round record under `WP11-*` | assistant | - | `release-candidate.md`, "The mandate, extended"; `PM-BRIEF.md`, "Mathematical presentation" ("First pass before the final reader round ... again inside the round") |
| D3 | Reader grid stopping rule met; held-out cells read once; whole grid reported with its worst cells | grid report | assistant | - | `release-candidate.md`, "What candidate means" |
| D4 | The expert/novice mathematics pair read at a named head before the round, triaged together | read and triage records | assistant | - | `PM-BRIEF.md`, "Mathematical presentation, expert and novice" |
| D5 | Deliverables grid current; printed whole in the handover | `deliverables-grid.md` | PM | - | `release-candidate.md`, "The deliverables grid"; `status-report-template.md` |

## E. The staged site and the browser

| # | Item | Command or evidence | Owner | State | Source |
|---|---|---|---|---|---|
| E1 | Site staged strict (root page, docsite, paper) at the named head; a failed paper build exits non-zero | `uv run python scripts/stage_site.py` | PM or assistant | - | `WP30-gate-checklist.md`, step 19; `WP8b-decisions.md`, "The strict paper build" |
| E2 | A clean worktree with no `paper/_build` stages the real paper (pinned article theme) | `git worktree add <tmp> origin/dev`; `uv run python scripts/stage_site.py` | agent | - | `WP8b-scope-of-work.md`, Amendment 1, R-14; `WP8b-decisions.md`, "OD-A1 evidence" |
| E3 | Full browser pass on every page of the staged site, desktop and phone width (375 px), light and dark, findings fixed or listed; screenshots saved in the record | own tab, screenshots as files under the review record | assistant | - | `release-candidate.md`, "What candidate means"; `PM-BRIEF.md` line 78 (width and 375 px, light and dark) and "Reviews run the thing" |
| E4 | Tab rules: tab-23 belongs to the WP26 modeller, nobody else navigates or clicks in it; any agent needing the pane creates its own tab with `tabs_create` and closes it | n/a (rule) | PM, agent | - | `pm5-rules.md`, "Rules added 2026-11-10"; `PM-BRIEF.md` lines 551-552 |
| E5 | Paper figures need not read on a phone | n/a (accepted) | PM | - | `WP8b-decisions.md`, "Amendment 1 review", G-4 |

## F. Merge and the hand-off

| # | Item | Command or evidence | Owner | State | Source |
|---|---|---|---|---|---|
| F1 | `main` gets `git merge --no-ff dev`, merge message naming the packages carried; preceded by the review of the staged localhost build, recorded | `git merge --no-ff dev` | assistant, after the supervisor asks | - | `README.md` (work-packages), Branching and release control; `CLAUDE.md`, Process |
| F2 | (No PR from us) The candidate is dev at a named head, with the review list and the reviewer's guide; the chief engineer opens or merges the PR after his review | n/a | chief engineer | - | `release-candidate.md`, "The mandate" and "extended" ("don't make the pull request"); path step 7 |
| F3 | Reviewer's guide in sittings (the paper; the docsite and root page; the code and derivations; the calls made for him), each a short checklist with its own localhost entry point; skeleton in `WP8b-reviewers-guide-skeleton.md` | open each entry point after staging | assistant | - | `release-candidate.md`, "The hand-off"; `WP8b-scope-of-work.md`, D-7 and R-7 |
| F4 | Guide lists every call with its evidence, every changed number with its reason, what is known weak | compare with `supervisor-review-list.md`, `driver-log.md`, `swap-evidence.md` | assistant | - | `WP8b-scope-of-work.md`, R-8; `release-candidate.md`, "What candidate means" |
| F5 | `supervisor-review-list.md` current: every call with record and landing commit | read | PM | - | `release-candidate.md`, "The mandate, extended"; `supervisor-review-list.md`, header |
| F6 | Repository tidiness instance before the PR (WP25-5) | `WP25-5-inventory.md` executed on approval | agent | - | `release-candidate.md`, step 3h ("one before the PR") and "extended" |
| F7 | Nothing tagged, deployed, published: no PyPI, no registry image, no PDF export | `git tag` empty | assistant | - | `WP8b-scope-of-work.md`, Non-goals; `release-candidate.md`, "Already decided" |

## G. After the tag and after the merge to main

Added at the WP8b drafts (handover of the thirteenth PM, open item 6). Each row names what it catches that the earlier
rows cannot, because it is only visible once the tag or the merge exists.

| # | Item | Command or evidence | Owner | State | Source |
|---|---|---|---|---|---|
| G1 | After the tag: reload a docs page once and watch for a 404 from the releases widget (the widget asks for a release that did not exist before the tag, so no staged build shows it) | open any docs page in a fresh tab after the tag; browser console and network list show no 404 for the releases request; record the screenshot | assistant | - | `PM-BRIEF.md`, handover of the thirteenth PM, open item 6 |
| G2 | After the merge to main: fetch every GitHub link on the site, paper, README and docs, with and without sign-in (the repository is private, so an unauthenticated fetch returns 404 even for files `main` holds; the links resolve only once `main` holds the paths they name) | extract the `github.com` links from the staged site and `README.md`, then `curl -s -o /dev/null -w '%{http_code}' -L <url>` for each, and again with a signed-in session (`gh api` or the browser); all 200 when signed in | assistant | - | `PM-BRIEF.md`, handover of the thirteenth PM, open item 6 |

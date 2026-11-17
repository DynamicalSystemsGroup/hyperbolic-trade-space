# WP65 D-1: the two release control models, specified

Written at `dev` d9e4922f on 2026-11-16 from his six answers (`WP64-decisions.md`) and the WP64 readout. Paths
without a prefix are repository paths. "The paper side" is everything that serves the paper's lifecycle; "the
software side" is the package, the docs and the root page. Workflow outlines name each third-party action by its
repository; every `uses:` is pinned to a full commit SHA with the release tag in a trailing comment, as today
(`scripts/release_checks.py pins` refuses anything else). New pins (`actions/setup-node`) are resolved by the builder
with `gh api repos/<owner>/<repo>/git/ref/tags/<tag>`.

## 0. The GitHub semantics relied on

| # | Semantics | Source | Where it binds |
|---|---|---|---|
| S-1 | Events made with the repository's `GITHUB_TOKEN` "will not create a new workflow run"; `workflow_dispatch` and `repository_dispatch` are the exceptions | docs.github.com/en/actions/how-tos/write-workflows/choose-when-workflows-run/trigger-a-workflow, "Triggering a workflow from a workflow" | the `v<version>` tag created in `release.yml` starts nothing; every step after the tag is a job of the same run |
| S-2 | A reusable workflow is called with `uses`, `with`, `secrets`; "The job that calls the reusable workflow can't use the `environment` keyword"; the environment is set on the job inside the called workflow; permissions "can only be maintained or reduced" down the chain; at most ten levels | docs.github.com/en/actions/how-tos/reuse-automations/reuse-workflows | `site.yml`, `pages-deploy.yml`, `test.yml` called from `release.yml`; `github-pages` set inside `pages-deploy.yml` |
| S-3 | A Pages deploy job needs at least `pages: write` and `id-token: write`; the default environment is `github-pages`; `upload-pages-artifact` packages the artefact and `deploy-pages` deploys it | docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages | `site.yml`, `pages-deploy.yml` |
| S-4 | A concurrency group holds "at most one running job or workflow"; a newly queued one cancels "any existing `pending`" one; `cancel-in-progress: true` also stops the running one | docs.github.com/en/actions/how-tos/write-workflows/choose-when-workflows-run/control-workflow-concurrency | the release group on `main` and `pages` (never cancel a running one), the pull-request and paper-branch groups (cancel) |
| S-5 | A GitHub trusted publisher on PyPI names owner, repository, the workflow's filename and optionally an environment; "Reusable workflows cannot currently be used as the workflow in a Trusted Publisher"; a pending publisher creates the project on first publish | docs.pypi.org/trusted-publishers/adding-a-publisher/; .../troubleshooting/; .../creating-a-project-through-oidc/ | the PyPI and TestPyPI jobs stay jobs of `release.yml` itself, not called jobs |
| S-6 | Ruleset rules: required status checks with an expected source app; pull request with required approvals, code-owner review, allowed merge methods; restrict deletions; block force pushes; restrict creations and updates; rules of several rulesets on one branch "are aggregated" and "the most restrictive version of the rule applies"; bypass actors are roles, teams or apps | docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/available-rules-for-rulesets; .../about-rulesets | the `main`, `dev` and `paper` rulesets (`his-items.md`) |
| S-7 | "Pull request authors cannot approve their own pull requests" | docs.github.com/en/pull-requests/collaborating-with-pull-requests/reviewing-changes-in-pull-requests/approving-a-pull-request-with-required-reviews | his question 1 |
| S-8 | Environments: up to six required reviewers, one approval suffices; prevent self-review stops the initiator approving; "Only branches and tags that match your specified name patterns can deploy" | docs.github.com/en/actions/reference/workflows-and-actions/deployments-and-environments | `pypi`, `testpypi`, `github-pages`, `paper-release` |
| S-9 | Re-running failed jobs re-runs "the jobs that depend on them" with "the same `GITHUB_SHA`" and `GITHUB_REF`, up to 30 days after the run; `gh run rerun RUN_ID --failed` | docs.github.com/en/actions/how-tos/manage-workflow-runs/re-run-workflows-and-jobs | the retry path of a failed release |
| S-10 | Zenodo "archives your repository and issues a new DOI each time you create a new GitHub release"; once a repository is switched on, "new releases from the repository will be automatically ingested and archived"; metadata from `CITATION.cff` or `.zenodo.json` (the latter wins when both exist) | docs.github.com/en/repositories/archiving-a-github-repository/referencing-and-citing-content; help.zenodo.org/docs/github/enable-repository/; help.zenodo.org/docs/github/describe-software/ | every published release of either side is archived; the DOI exists only after publication |
| S-11 | A `push` workflow runs from the pushed commit's file, including workflows not on the default branch; `workflow_dispatch` needs the file on the default branch (WP64 readout, section 1a, with its citation) | readout 1a | the quality-control runs before the first merge use `qc/**` branch pushes, not dispatches |

Not stated by either service and taken as working assumptions, each checked at the first live use (build plan,
"What the first live runs confirm"): that Zenodo archives a release when it is published and not while it is a
draft; that all releases of one repository become versions of one Zenodo record; that Zenodo reads the metadata
file at the release's tagged commit.

## 1. G1: the software's release model

### 1.1 The gate and the event

The release of the package and the docs is the merge of a pull request from `dev` into `main` (Q6). The pull request
is the gate: the required checks `test (fast)`, `test (slow)`, `test (docs)` (from `test.yml`) and `admissibility`
(from `release.yml`), the review rule his question 1 settles, merge commits only. The merge pushes to `main`; that
push runs `release.yml`, which checks admissibility again on the merge commit, runs the suite, builds, composes the
site, creates the tag `v<version>` and a draft GitHub release, publishes to PyPI, deploys the site and publishes the
release. The publish turns the draft into a release, which Zenodo archives (S-10). Nothing in the run depends on the
tag as an event (S-1). The pull request names a release issue (`closes #n`), which satisfies
`pr-linked-issue.yml` and records the release's fitness decision.

### 1.2 `release.yml` (replaces today's file)

**Triggers.**

- `pull_request: branches: [main]`: the job `admissibility` only (a required check).
- `push: branches: [main, "qc/**"]`: on `main` the release; on `qc/**` the dry-run path (no tag, no publish, no
  deploy, no issue), for quality control before the first merge (S-11).
- `workflow_dispatch` with `target` (choice `dry-run` default, `testpypi`) and `tag` (string, default empty), as
  today; `testpypi` refused off `dev`.
- No `push: tags`. A `v*` tag pushed by hand starts nothing.

**Top-level permissions:** `contents: read`. Jobs widen only what they need.

**Concurrency:** `group: ${{ github.event_name == 'pull_request' && format('release-pr-{0}',
github.event.pull_request.number) || format('release-{0}', github.ref) }}`; `cancel-in-progress: ${{
github.event_name == 'pull_request' }}`. A running release is never cancelled. A second merge waits as pending; a
third would cancel the second's pending run (S-4), so the rule (code owners' page) is one release pull request at a
time, merged after the previous release run has ended; `admissibility` on a pull request into `main` fails while a
`release.yml` run on `main` is queued or in progress (`gh run list --workflow release.yml --branch main --status
in_progress` and `--status queued` both empty).

**A `RELEASE` expression**, used in the `if:` conditions: `github.event_name == 'push' && github.ref == 'refs/heads/main'`.

**Jobs.**

| Job | Needs | Runs when | Permissions, environment | Steps (action or command) | Outputs |
|---|---|---|---|---|---|
| `admissibility` (job id `check`) | none | always | `contents: read`, `actions: read` | checkout (`fetch-depth: 0`); setup-uv; `uv run --no-project python scripts/check_release_version.py` → `version`; `uv run --no-project python scripts/release_checks.py tag --tag v$version --sha $SHA` → `tag_state` (`new`, `ours`, `taken`; `taken` fails, see his question 2); `release_checks.py changelog --version $version --final` (not `--final` on a dispatch without `tag`); `uv lock --check`; `release_checks.py pins`; `uv run python scripts/paper_mode.py check --stage served`; on `RELEASE`: `release_checks.py merge --sha $GITHUB_SHA --from origin/dev` (the commit has two parents and its second parent is on `dev`); on a `testpypi` dispatch: the ref is `refs/heads/dev` | `version`, `tag` (`v<version>`), `tag_state` |
| `test` | `check` | `RELEASE`, `qc/**`, `testpypi` dispatch | caller of `./.github/workflows/test.yml` with `windows: false` | the suite (section 5) | none |
| `build` | `check` | not on `pull_request` | `contents: read` | as today: `uv build`; `twine check`; wheel contents; built version equals `version`; CycloneDX bill; `release_checks.py sbom`; upload artefacts `dist`, `sbom` | artefacts |
| `site` | `check` | not on `pull_request` | caller of `./.github/workflows/site.yml` | compose `_site`, upload the Pages artefact (section 3.4) | `slot`, `pin` |
| `tag` | `check`, `test`, `build`, `site` | `RELEASE` | `contents: write` | checkout (`fetch-depth: 0`); if `tag_state == new`: `git tag -a v$V -m "hyperbolic-trade-space $V" $GITHUB_SHA && git push origin refs/tags/v$V`; `release_checks.py changelog --version $V --final --notes notes.md`; download `dist`, `sbom`; `gh release view v$V` → if absent `gh release create v$V dist/* sbom/sbom.cdx.json --draft --verify-tag --title v$V --notes-file notes.md`, if a draft exists `gh release upload v$V dist/* sbom/sbom.cdx.json --clobber` | none |
| `publish-pypi` | `check`, `tag` | `RELEASE` | `id-token: write`; environment `pypi` (url `https://pypi.org/p/hyperbolic-trade-space`) | download `dist`; `pypa/gh-action-pypi-publish` with `skip-existing: true`; then `uv run --no-project python scripts/release_checks.py pypi --version $V --dist dist` (the files PyPI holds for the version have the SHA-256 of `dist/*`; a mismatch fails) | none |
| `publish-testpypi` | `build`, `test` | `testpypi` dispatch | `id-token: write`; environment `testpypi` | as today | none |
| `deploy-site` | `publish-pypi`, `site` | `RELEASE` | `pages: write`, `id-token: write`; caller of `./.github/workflows/pages-deploy.yml` | deploy the run's Pages artefact (section 3.4) | `page_url` |
| `publish-release` | `check`, `deploy-site` | `RELEASE` | `contents: write`, `issues: write` | `gh release edit v$V --draft=false --latest`; close every open issue labelled `release-failure` whose title names `v$V`, with a comment linking the run | none |
| `on-failure` | every other job | `always() && (failure() \|\| cancelled()) && github.event_name == 'push' && github.ref == 'refs/heads/main'` | `contents: write`, `issues: write`, `actions: read` | checkout; setup-uv; `gh run view $GITHUB_RUN_ID --json jobs` → the failed jobs and, for each, the first step whose conclusion is `failure`; write them to `$GITHUB_STEP_SUMMARY`; `uv run --no-project python scripts/release_cleanup.py --tag v$V --run-id $GITHUB_RUN_ID --report cleanup.md`; append `cleanup.md` to the summary; `gh label create release-failure --force --color B60205`; if an open issue titled `Release v$V failed` exists, `gh issue comment` with the summary and the report, else `gh issue create --title "Release v$V failed" --label release-failure --body-file body.md` | the issue |

Order and why: the reversible steps (tag, draft release, the composed site as an artefact) come before the one step
that cannot be undone (PyPI accepts a version's files once), and the deploy and the release's publication come after
it. A failure before PyPI leaves only a tag and a draft, which the clean-up removes; a failure after PyPI leaves a
version on PyPI, which the clean-up keeps (1.4).

On `qc/**` and on a `dry-run` dispatch the jobs `check`, `test` (on `qc/**`), `build` and `site` run and nothing
after them; `on-failure` does not run; the run's own summary carries the failure.

### 1.3 Failure detection

Every job's failure is visible three ways, chosen for what each adds:

- the run's own status on the merge commit (GitHub's check of the run; no extra mechanism, and it is what the
  commit page and the Actions list show);
- the run summary, which `on-failure` writes: "Failed: job `<job>`, step `<step>`" for each failed job, then the
  clean-up report;
- a GitHub issue labelled `release-failure`, opened or commented by `on-failure`. An issue and not an added check:
  a push to `main` has no open pull request for a check to sit on, a check on the merge commit duplicates the run's
  own status, and an issue persists, notifies the code owners by e-mail, holds the clean-up report and the retry
  command, and is closed by the next successful run of the same version (`publish-release`).

A cancelled run takes the same path (`cancelled()`). A failure of `on-failure` itself shows in the run status only.

### 1.4 `scripts/release_cleanup.py`

Uv-run Python, standard library plus `gh` on `PATH`; run by `on-failure` and by hand.

```
uv run --no-project python scripts/release_cleanup.py --tag TAG [--repo OWNER/NAME] [--run-id ID]
                                                      [--dry-run] [--json] [--report FILE]
```

- `--tag` (required): `v<version>` (PEP 440 as `check_release_version.VERSION`) or a paper tag (section 2.3).
  Anything else is a usage error.
- `--repo`: default `$GITHUB_REPOSITORY`, else `gh repo view --json nameWithOwner`.
- `--run-id`: named in the retry lines.
- `--dry-run`: reads everything, removes nothing, prints "would remove".
- `--json`: prints `{"tag", "repo", "found": {...}, "removed": [...], "kept": [...], "retry": [...], "exit"}`.
- `--report FILE`: also writes the text report as Markdown.

What it reads: the tag ref (`gh api repos/R/git/ref/tags/TAG` → SHA or absent); the release of the tag
(`gh release view TAG --json isDraft,assets`); for a `v` tag, PyPI's record of the version
(`https://pypi.org/pypi/hyperbolic-trade-space/<version>/json`: 200 present, 404 absent, anything else an error).

What it does:

| State | Action | Exit |
|---|---|---|
| no tag, no release | nothing | 0 |
| the release is published (not a draft) | nothing removed: a published release is archived by Zenodo and is public | 3 |
| a `v` tag whose version PyPI holds | tag and draft kept: PyPI's files point at this version | 3 |
| otherwise | `gh release delete TAG --yes` if a draft exists, then `gh api -X DELETE repos/R/git/refs/tags/TAG` | 0 |
| PyPI or `gh` unreadable, or a deletion fails | stops at that point; prints what was removed before it | 1 |
| bad arguments or tag shape | nothing | 2 |

What it prints (text form):

```
release_cleanup: v0.1.0 in DynamicalSystemsGroup/hyperbolic-trade-space
found: tag v0.1.0 -> 1a2b3c4; draft release v0.1.0 (3 assets); PyPI 0.1.0 absent
removed: draft release v0.1.0
removed: tag v0.1.0
retry: gh run rerun 123456 --failed   (same commit, within 30 days of the run)
retry: after a fix on dev, merge a new pull request into main; v0.1.0 is free
```

When it keeps state (exit 3) the retry lines read: `gh run rerun ID --failed` for a failure after PyPI (the jobs
re-run reuse the PyPI files through `skip-existing` and the hash check), and, when the cause needs a code change, "the
next release is a new version: PyPI holds 0.1.0". For a paper tag the retry lines read "fix on `paper`, push, and
push the tag again; the name is free".

## 2. G2: the paper's release model

### 2.1 The branch and the flow

`paper` is created from `dev` at the first merge to `main` (build plan). The paper is edited on `paper` only; `dev`
does not edit `paper/` except by merging `paper` in. The flows:

- software into the paper: `git checkout paper && git merge --no-ff dev`, push; `paper.yml` runs every paper test,
  so a software change that breaks the paper fails there (Q5);
- the paper into the software: first merge `dev` into `paper` (so the next merge carries no conflict), then
  `git checkout dev && git merge --no-ff paper`; then the next pull request from `dev` into `main` releases it to the
  public site (Q2). Conflicts are resolved on `paper` in the first step.

Files both sides edit (`docs/references.bib`, `glossary.yaml`) can conflict in more than links; they are resolved
on `paper` by the same first step.

### 2.2 `paper.yml` (new)

**Triggers:** `push: branches: [paper, "qc/paper/**"]`; `push: tags: ["paper-*"]`; `workflow_dispatch` (no inputs;
builds and tests the dispatched ref, publishes nothing). A tag is pushed by a person, so it raises its event.

**Permissions:** `contents: read`; the `release` job widens.

**Concurrency:** `group: paper-${{ github.ref }}`; `cancel-in-progress: ${{ github.ref_type == 'branch' }}` (a newer
push supersedes a branch build; a tag run always completes).

**Environment variables for the whole run:** `HTS_PAPER_TESTS=1`, `PAPER_EXECUTE=1`, `PAPER_BUILD=1`,
`REQUIRE_OPENSYSML=1`, `BASE_URL=/hyperbolic-trade-space/paper`.

**Jobs.**

`build` (ubuntu-24.04, `contents: read`):

1. checkout (`fetch-depth: 0`); the attribution grep of `test.yml`, copied verbatim.
2. On a tag: `git merge-base --is-ancestor $GITHUB_SHA origin/paper` (the tag is on `paper`);
   `uv run --no-project python scripts/paper_mode.py check --stage tag --tag $GITHUB_REF_NAME` (the committed mode
   names this tag).
3. On a branch push: `uv run --no-project python scripts/paper_mode.py check --stage tag` (consistent fields; DOI and
   checksum may be empty).
4. setup-uv; `uv lock --check`; `uv sync --locked`; setup-node (Node 22); the opensysml cache and the toolkit
   provisioning steps of `test.yml`, copied.
5. `uv run python scripts/build_generated.py` (the derivations and verification pages the paper's build reads; C7).
6. The paper's tests: `uv run pytest -q -n auto --dist loadgroup -m paper` (section 5.2; includes the execution
   test, the HTML build test, the length ledger, the paper's claims, the paper's vocabulary and residuals).
7. `cd paper && uv run myst build --html` (the build published, with `BASE_URL`).
8. `uv run python paper/build_keys.py --check --xref paper/_build/html/myst.xref.json` (the committed manifest
   equals the notebooks' labels and each key is an identifier on the page it names).
9. On a tag: `uv run python paper/pin_links.py --ref $GITHUB_REF_NAME paper/_build/html` (C16).
10. `tar -czf paper-html.tar.gz -C paper/_build/html .`; `cp paper/paper-keys.json .`; `sha256sum` of both to
    `$GITHUB_STEP_SUMMARY`; upload both as the workflow artefact `paper-release`.

`release` (needs `build`; only on a tag; `contents: write`; environment `paper-release` when his question 3 says
so):

1. checkout; download `paper-release`.
2. Notes: mode, venue, round and date from `scripts/paper_mode.py show --json`; the software it was built with
   (`git describe --tags --match 'v*' --abbrev=12` or the commit when no `v` tag precedes it) and the `uv.lock`
   SHA-256 (Q1: a paper version cites the release active when it shipped); the section of `paper/CHANGES.md` for the
   tag when one exists.
3. `gh release create $TAG paper-html.tar.gz paper-keys.json --draft --verify-tag --title $TAG --notes-file notes.md
   --latest=false` (a paper release never becomes the repository's "latest", which stays the software's).
4. `gh release view $TAG --json assets` names both assets with the sizes uploaded; then
   `gh release edit $TAG --draft=false`. Zenodo archives it (S-10).

`on-failure` (needs `build`, `release`; `always() && (failure() || cancelled()) && github.ref_type == 'tag'`;
`contents: write`, `issues: write`, `actions: read`): the failing job and step to the summary as in 1.3;
`scripts/release_cleanup.py --tag $TAG --run-id $GITHUB_RUN_ID --report cleanup.md` (deletes the draft and the tag;
refuses a published release); an issue `Paper release <tag> failed`, label `release-failure`. A failed branch push
reports in the run status and summary only; nothing was created.

`paper.yml` never deploys Pages and never writes to a branch.

### 2.3 Tags and modes

| Mode | Tag shape (regular expression) | Example |
|---|---|---|
| `abstract` | no tag | |
| `working` | `^paper-working-(?P<date>\d{8})(?:-(?P<n>[2-9]\|[1-9]\d+))?$` | `paper-working-20261120`, `paper-working-20261120-2` |
| `submitted` | `^paper-submitted-(?P<venue>[a-z0-9]+(?:-[a-z0-9]+)*)$` | `paper-submitted-ieee-tse` |
| `revision` | `^paper-revision-(?P<venue>[a-z0-9]+(?:-[a-z0-9]+)*)-r(?P<round>[1-9]\d*)$` | `paper-revision-ieee-tse-r2` |

No shape starts with `v` (C13). The prefix `paper` and the shapes are placeholders he can rename.

### 2.4 Publishing a pin, step by step

1. On `paper`: `uv run --no-project python scripts/paper_pin.py prepare --tag <tag>` writes `mode`, `pin`, `venue`,
   `round`, `date` into `paper/mode.toml`, empties `doi` and `sha256`; commit; push (the branch build runs).
2. For `submitted` and `revision` only: the container re-pin gate (2.5), recorded, before the tag.
3. `git tag <tag> && git push origin <tag>`: `paper.yml` builds, tests and publishes the release; Zenodo mints the
   DOI.
4. `uv run --no-project python scripts/paper_pin.py record --tag <tag> --doi 10.5281/zenodo.<n>` downloads
   `paper-html.tar.gz` from the release, writes its SHA-256 and the DOI into `paper/mode.toml`, checks
   `--stage served`; commit; push.
5. Merge `dev` into `paper`, then `paper` into `dev` (2.1); the next release of the software serves the pin.

`scripts/paper_pin.py`: subcommands `prepare --tag T [--date YYYY-MM-DD]` and `record --tag T --doi D [--repo R]`,
both with `--dry-run` (prints the new `mode.toml` and changes nothing). Exit 0 written, 1 a check failed (reason
printed), 2 usage. It never commits or pushes.

### 2.5 The container re-pin gate

Before a `submitted` or `revision` tag, the commit to be tagged passes the container gate of
`paper/container/README.md` (build `hts-paper` and `hts-alt`, execute in the container, re-pin the exact outputs,
the full suite in both images), recorded in `paper/container/RECORD.md` with the commit, the `uv.lock` hash and
"regression landed". The paper checklist's rows C1 to C5 hold it (section 6.3). It is a person's gate, not a
workflow step: the platform of record is linux/arm64 and hosted runners are x64 (`paper/container/README.md:39-40`).
A `working` tag needs no re-pin.

### 2.6 The key manifest's producer: `paper/build_keys.py`

```
uv run python paper/build_keys.py [--check] [--xref PATH]
```

Reads the `:label:` lines and `(key)=` targets of `paper/paper.ipynb` (route `paper/`) and
`paper/supporting_material.ipynb` (route `paper/supporting-material/`), the parse that `scripts/paper_keys.py` does
today, moved. Without `--check` it writes `paper/paper-keys.json`; with `--check` it writes nothing and exits 1 if the
committed file differs, printing the keys added, removed or moved. With `--xref` it also checks every key against the
built `myst.xref.json` (identifier on the page the route names) and exits 1 naming each miss. Exit 2 on a key defined
twice.

### 2.7 `paper/pin_links.py`

`uv run python paper/pin_links.py --ref REF DIR` replaces
`https://github.com/DynamicalSystemsGroup/hyperbolic-trade-space/blob/main/` and `.../tree/main/` by the same with
`REF` in every `.html` and `.json` file under `DIR`; prints the count per file; exit 0, or 1 when nothing was
replaced (the generators' constant moved without this script following). The committed notebooks keep `blob/main`
(true once `main` carries the release); the published artefact links the files as they were at the pin.

### 2.8 `paper/CHANGES.md`

The paper's change record (C22): one section per pin, `## <tag> - <date>`, written in step 1 of 2.4. `CHANGELOG.md`
records the package and the docs from 0.1.0 on.

## 3. G3: the mode and the slot

### 3.1 `paper/mode.toml`

```toml
schema = 1
mode = "abstract"   # abstract | working | submitted | revision
pin = ""            # the paper tag served; empty in abstract mode
venue = ""          # slug; submitted and revision only
round = 0           # revision only, from 1
date = ""           # YYYY-MM-DD of the pin
doi = ""            # 10.5281/zenodo.<n>, minted for the pin's release
sha256 = ""         # SHA-256 of the pin's paper-html.tar.gz
```

The fields beyond mode, pin, venue and date: `round` because a revision tag carries one; `doi` because the banner
names it; `sha256` so the composer serves the bytes the pin published and nothing re-uploaded later; `schema` so a
later field is an explicit change.

Validation (`scripts/paper_mode.py`):

| Rule | `--stage tag` | `--stage served` |
|---|---|---|
| `schema == 1`; no unknown key; types as in the file | yes | yes |
| `mode` in the four | yes | yes |
| `abstract`: every other field empty, `round == 0` | yes | yes |
| `pin` matches the shape of `mode` (2.3) | yes | yes |
| `venue`, `round` equal the tag's groups; empty and 0 where the shape has none | yes | yes |
| `date` is ISO; for `working` it equals the tag's date | yes | yes |
| with `--tag T`: `pin == T` | yes | yes |
| `doi` matches `^10\.5281/zenodo\.\d+$`; `sha256` matches `^[0-9a-f]{64}$` | when not empty | required in every mode but `abstract` |

```
uv run --no-project python scripts/paper_mode.py check [--stage tag|served] [--tag T] [--file PATH]
uv run --no-project python scripts/paper_mode.py show [--json] [--file PATH]
uv run --no-project python scripts/paper_mode.py parse TAG
```

`check` prints `paper_mode: ok <mode> <pin>` or one line per broken rule (`paper_mode: <field>: <reason>`) and exits
0 or 1. `show` prints the fields and the banner line. `parse` prints the mode and groups of a tag, exit 2 when it is
no paper tag. Exit 2 is usage everywhere. Standard library only (`tomllib`).

The value at 0.1: `mode = "abstract"`, the rest empty.

### 3.2 What `/paper/` serves

| Mode | `/paper/` | Banner |
|---|---|---|
| `abstract` | the abstract page (3.3) | none |
| `working` | the unpacked `paper-html.tar.gz` of `pin` | `Working paper · paper-working-20261120 · 2026-11-20 · DOI 10.5281/zenodo.123` |
| `submitted` | the same | `Submitted to <venue> · <tag> · <date> · DOI <doi>` |
| `revision` | the same | `Revision <round> for <venue> · <tag> · <date> · DOI <doi>` |

One banner line, a `<p class="hts-paper-banner">` linked to `https://doi.org/<doi>`, on every HTML page of the
artefact as `<body>`'s first element. It is installed by a script placed directly before `</body>` (the banner in a
`<template>` beside it), not written after `<body>`: the article theme hydrates the whole document with React, a
static element there fails that hydration (React error 418) and the theme's client render drops it (WP67 D-4, found
by the browser pass). The script adds the banner after the load event and puts it back if the theme removes it in
its first seconds. The banner carries its own colours for the theme's light and dark schemes (the theme colours its containers, not
`<body>`, so an unstyled banner read black on the dark background) and side padding that clears the theme's fixed
scheme button at phone width. Only the current pin is served (Q4); earlier pins stay as tags,
releases and DOIs.

### 3.3 The abstract page

Rendered by `scripts/paper_abstract.py` from the template `site/paper/abstract.html` (replacing
`site/paper/index.html`, the placeholder), at build time:

- the title and the abstract from the YAML front matter of `paper/paper.ipynb`'s first cell (`title`, `abstract`);
  the abstract's paragraphs become `<p>` elements, the text escaped (it holds no markup today; a `$`, a role or a link
  in it fails the render, so a later abstract with markup is a deliberate change);
- the author from `paper/myst.yml`, `project.authors[*].name` with the affiliation (the front matter has no
  author field);
- the line: "The paper is iterated towards release on the `paper` branch of the repository and builds from it with
  `uv run myst build --html` in `paper/`." with the branch linked;
- two cards in the root page's style: `../docs/getting-started/` ("Use the code") and `../` (the root page);
- the root page's colour tokens, light and dark, no script, the existing meta tags with the description taken from
  the abstract's first sentence.

Never on the page: "forthcoming", "in preparation", "coming soon", a date. The fallback form (3.4) adds one line
before the abstract: "The pin `<tag>` was not reachable when the site was composed (`<reason>`); its abstract
follows."

### 3.4 The composer

`scripts/assemble_site.py`, rewritten around the slot; it never builds the paper (no `myst`, no
`execute_notebooks`):

```
uv run python scripts/assemble_site.py [--out DIR] [--generated-dir DIR] [--slot auto|abstract]
                                       [--artefact PATH] [--strict-slot] [--summary FILE]
```

1. Resolve the slot. `--slot abstract`: the abstract page. `--slot auto` (default): read `paper/mode.toml`
   (`check --stage served`); `abstract` mode gives the abstract page; otherwise obtain the artefact from `--artefact
   PATH` or from `https://github.com/DynamicalSystemsGroup/hyperbolic-trade-space/releases/download/<pin>/paper-html.tar.gz`
   (stdlib `urllib`, 60 s timeout, two attempts), check its SHA-256 against `sha256`, fetch the release's
   `paper-keys.json` (or `paper-keys.json` beside `--artefact`) and check it equals the committed
   `paper/paper-keys.json` byte for byte. Any failure gives the fallback abstract page with the reason. The slot is
   `abstract`, `pin` or `fallback`.
2. Build the docs with `HTS_PAPER_SLOT` set to `pin` or `abstract` (fallback counts as abstract), so their citations
   match what `/paper/` holds (section 4).
3. Root page, history page, figures as today; the paper card's line per mode (C14): `abstract` and fallback: the
   card's `<span>` becomes "its abstract; the paper is iterated towards release"; pinned modes keep "the argument
   and the proofs". The card's link stays `paper/`.
4. Place the slot at `<out>/paper/`.
5. Print `assemble_site: slot <slot> <pin or -> <reason or ->` to stdout, and with `--summary FILE` append it as
   Markdown; a fallback also prints a GitHub warning annotation (`::warning::`).

Exit 0 built (any slot); 1 a build failure, or a fallback under `--strict-slot`; 2 usage. `--paper` is removed.

`scripts/stage_site.py`: `--slot` and `--artefact` passed through; default `--slot abstract` when no `--artefact` is
given, so staging stays offline (the contract's `network = false`); `--paper` removed.

### 3.5 `site.yml` and `pages-deploy.yml` (new; `pages.yml` deleted)

`site.yml`: `on: workflow_call` (outputs `slot`, `pin`) and `workflow_dispatch` (builds on any branch; never
deploys). `permissions: contents: read`. Job `compose` (ubuntu-24.04): checkout (`fetch-depth: 0`); setup-uv;
`uv sync --locked`; the opensysml cache; `uv run python scripts/assemble_site.py --out _site --summary
$GITHUB_STEP_SUMMARY`; `actions/upload-pages-artifact` with `path: _site`. No `pytest` step (the suite runs once, in
`release.yml`'s `test`; C5). Outputs read from the composer's stdout line.

`pages-deploy.yml`: `on: workflow_call` only. Job `deploy` (ubuntu-24.04): `permissions: pages: write, id-token:
write`; `environment: {name: github-pages, url: ${{ steps.deployment.outputs.page_url }}}` (set here, S-2);
`concurrency: {group: pages, cancel-in-progress: false}` (S-4); one step, `actions/deploy-pages`
(id `deployment`); output `page_url`. Called only by `release.yml` on a push to `main`, and the `github-pages`
environment admits only `main` (S-8), so `dev`, `paper` and `qc/**` cannot deploy.

## 4. G4: the docs' citations

`paper/paper-keys.json`, committed on both branches, written only by `paper/build_keys.py` on `paper` and carried
to `dev` by the merge:

```json
{
  "schema": 1,
  "keys": {
    "appendix-e": "paper/supporting-material/",
    "thm-kkt": "paper/"
  }
}
```

Rules: `schema == 1`; `keys` non-empty; each key matches `^[A-Za-z0-9_-]+$`; each route is `paper/` or
`paper/supporting-material/`; keys sorted; two-space indent; one trailing newline (so the bytes compare equal to
the pin's asset).

`scripts/paper_keys.py` (the MkDocs hook, same path and hook entry):

- `load_manifest(path=paper/paper-keys.json) -> dict[str, str]`; raises `ValueError` on a broken rule;
- `slot()`: `HTS_PAPER_SLOT` when set (`pin` or `abstract`), else `abstract` when `paper/mode.toml` says so and
  `pin` otherwise (a bare `mkdocs build`);
- `resolve(markdown, page_url, keys, slot)`: `pin` gives `../paper/#key` or `../paper/supporting-material/#key`
  relative to the page, as today; `abstract` gives `../paper/` relative to the page, no anchor; code fences left as
  written;
- an unknown key raises `UnknownPaperKey` in both slots, which fails the strict docs build.

No notebook is read by the docs build (C1).

## 5. G5: the software's test gate

### 5.1 The cut

A pytest marker `paper` (registered in `tests/conftest.py`) marks every paper test. `tests/conftest.py` deselects
items marked `paper` unless `HTS_PAPER_TESTS=1`, and prints the number deselected. So `uv run pytest` on `dev` is the
software suite, `paper.yml` sets the switch, and the paper's author runs `HTS_PAPER_TESTS=1 uv run pytest -m paper`
on `paper`.

Marked `paper`: the whole of `tests/test_paper.py`, `tests/test_paper_static_figures.py` and `tests/test_container.py`
(module-level `pytestmark`); in mixed modules, the paper's half (5.2). Not marked, so in the software gate: the mode
file, the manifest's form, the workflow structure, `tests/test_paper_sources.py` (snapshots under `docs/superpowers/`)
and `tests/test_narrative.py`.

### 5.2 Tests that change, by name

| Module | Test | Marked | Assertion |
|---|---|---|---|
| `test_claims_register.py` | `test_the_register_holds_for_the_software_surfaces` | no | `check_register` on the rows whose `file` does not start with `paper/` returns no problem (386 rows today) |
| | `test_the_register_holds_for_the_paper` | paper | the same on the rows whose `file` starts with `paper/` (362 today) |
| | `test_every_row_is_in_exactly_one_surface` | no | the two filters partition the register |
| `test_vocabulary.py` | `test_real_repo_has_no_new_vocabulary_violation_on_the_software_surfaces` | no | `check_vocabulary.py --surface software` exits 0 against the baseline |
| | `test_real_repo_has_no_new_vocabulary_violation_in_the_paper` | paper | `--surface paper` exits 0 |
| | `test_surface_filter_selects_by_path` | no | on a planted tree a violation under `paper/` appears only with `--surface paper` or `all`; a dead glossary entry appears with `software` (the glossary is the software side's) |
| `test_residuals.py` | `test_views_filter_limits_the_report_and_the_compare` | no | `check_residuals.py --views paper,appendix` reports only those views and compares only their counts |
| | `test_paper_residual_counts_do_not_rise` | paper | `--compare scripts/residuals_baseline.json --strict --views paper,appendix` exits 0 |
| `test_site.py` | `test_every_paper_key_is_a_label_of_the_built_paper` | removed | moves to `test_paper_model.py` as `test_key_manifest_equals_the_built_paper_labels` |
| | `test_paper_theme_is_pinned_to_a_commit` | removed | moves to `test_paper_model.py`, marked paper |
| | `test_workflow_triggers_release_tag_and_dispatch_only`, `test_workflow_build_and_deploy_jobs` | removed | `pages.yml` is gone; `test_site_workflow_*` and `test_release_workflows.py` replace them |
| `test_build_generated.py` | the eight `build_paper` and strict-paper tests (`:412` to `:529`) | removed | replaced by the slot tests of `test_paper_slot.py` and two staging tests (build plan) |

`scripts/check_vocabulary.py` gains `--surface software|paper|all` (default `all`): violations whose file is under
`paper/` belong to `paper`, the rest to `software`; the baseline's stale rows are reported within the surface only.
`scripts/check_residuals.py` gains `--views V[,V...]` over the views of `scripts/prose_surfaces.py`.

### 5.3 `test.yml`

- Triggers: `workflow_call` (`windows`, default false), `workflow_dispatch` (`windows`, default true), and
  `pull_request: branches: [main]` (the required checks), and `push: branches: [dev]`, which runs lint and the
  Linux `fast` shard only (added 2026-11-16, WP67 G9, the external review's first finding; the matrix condition
  also names the workflow because a called workflow sees the caller's event).
- Shards: `fast`, `slow`, `docs` (renamed from `docs-paper`). `DOCS_MODULES` = `tests/test_site.py
  tests/test_build_generated.py tests/test_docs.py tests/test_narrative.py tests/test_paper_slot.py`
  (`test_paper.py` and `test_container.py` leave it). Commands: `fast` `-m "not slow and not paper"`; `slow`
  `-m "slow and not paper"` with the docs modules ignored; `docs` `-m "slow and not paper" $DOCS_MODULES`. The
  marker expression is belt and braces: `HTS_PAPER_TESTS` is never set, so the conftest deselects paper tests too.
- The strict site stage: the `assembled` fixture of `test_site.py` calls `assemble_site.py --slot abstract`, offline,
  with no paper build; `test_assembled_layout` asserts the abstract page.
- Windows: `fast` and `slow` with the same expressions; never on a pull request (`inputs.windows` is false there).
- Check names on a pull request: `test (fast)`, `test (slow)`, `test (docs)`; called from `release.yml` they read
  `test / test (fast)` and are not the required ones.

## 6. G6: the records

### 6.1 The interface contract, amendment 29

`work-packages/interface-contract.toml` (`contract_version = 29`) and `.md` (row 29 of the change table; sections
10, 11, 13 and 16 rewritten):

- `[docs]`: `reference_key_sources = ["paper/paper-keys.json"]`; new `reference_key_manifest_generator =
  "paper/build_keys.py"`, `reference_key_slot_variable = "HTS_PAPER_SLOT"`, `reference_key_abstract_target =
  "/paper/"`; syntax and resolver unchanged.
- `[build]`: `workflow = ".github/workflows/release.yml"`; new `site_workflow = ".github/workflows/site.yml"`,
  `pages_deploy_workflow = ".github/workflows/pages-deploy.yml"`; `workflow_deploys_on = "a push to main (a merged
  pull request from dev), through release.yml's called jobs; a dispatch or a qc/** push builds and never deploys"`;
  `workflow_never_deploys_from = "dev"` kept; `branches = ["dev", "main", "paper"]`; `paper_cmd`, `paper_cwd`,
  `paper_config` kept and `paper_out` becomes `"paper/_build/html (published as paper-html.tar.gz)"`; new
  `paper_workflow = ".github/workflows/paper.yml"`, `paper_branch = "paper"`, `paper_artefacts =
  ["paper-html.tar.gz", "paper-keys.json"]`, `paper_tag_prefix = "paper-"`, `paper_mode_file = "paper/mode.toml"`,
  `paper_modes = ["abstract", "working", "submitted", "revision"]`, `paper_slot = "abstract page in abstract mode,
  the pin's published artefact otherwise; the composer never builds the paper"`. `public_paths` unchanged.
- `[build.stage]`: `release_control = "a merge to main is a release; the pull request's review includes the staged
  site, recorded in the release issue"`; new `paper_slot = "abstract unless --artefact names a local artefact of
  the pin"`; `network = false` kept.
- `[ownership]`: `.github/workflows/pages.yml` leaves `wp8a`; `site.yml` and `pages-deploy.yml` join `wp8a`;
  `paper.yml` joins `wp10`; `CITATION.cff` joins `wp8b`; carve-outs `tests/test_paper_model.py` → `wp10`,
  `tests/test_paper_slot.py` → `wp8a`, `tests/test_release_workflows.py` and `tests/test_release_cleanup.py` →
  `wp8b`; `scripts/release_cleanup.py` → `wp8b`.
- Section 13 (R-12) of the `.md`: the quoted release-control rule stays verbatim; the paragraph after it says that
  the review is part of the release pull request.

### 6.2 The three drifts, and a fourth

| Record | Drift | Correction |
|---|---|---|
| `work-packages/README.md:68-69` | CI "runs on pushes and pull requests to `main`" | "`test.yml` runs on pull requests into `main`, when `release.yml` calls it, and on dispatch; `paper.yml` runs on pushes to `paper` and on `paper-*` tags; a merge into `main` is a release" (the Branching paragraph names the three branches) |
| `docs/code-owners.md:27` against `:76` | `main` requires a pull request; step 3 pushes to `main` directly | "The flow" and "Cutting a release" rewritten: the release is the merge of the pull request; step 3 becomes "open the pull request from `dev` into `main`", step 4 "merge it", step 5 "watch the run; on failure read the issue it opens" |
| `WP8b-release-checklist.md:88` (G2) | "the repository is private" | public; the row keeps the fetch of every GitHub link, unauthenticated only |
| `docs/code-owners.md:30-32` | `dev` "require a pull request before merging and approval from code owners", while the driver commits to `dev` directly (`work-packages/README.md`, Branching) and a sole code owner cannot approve his own pull request (S-7) | the `dev` ruleset of `his-items.md`: deletions and force pushes blocked, no pull-request rule |

`CHANGELOG.md`: under `[Unreleased]`, one entry for the two release models (the merge releases the package and the
docs; the paper's own branch, tags and change record); the WP34 line's "the paper build stays on Linux and macOS"
becomes "the paper's tests run in the paper's workflow". `.github/RELEASE_ADMISSIBILITY.md`: the rows read "the
merge of a pull request from `dev` into `main`" for "a tag"; the fitness row is recorded by the merge (the merger and
the release issue), since the `pypi` environment has no required reviewer (`his-items.md`). `CITATION.cff` (new):
the software's citation (title, Michael Zargham with ORCID, Dynamical Systems Group, repository URL, licence, version
and date set by the release package), read by Zenodo for every release (S-10).

### 6.3 The checklist, split

`WP8b-release-checklist.md` leaves the tree; `work-packages/release-checklist-software.md` and
`work-packages/release-checklist-paper.md` replace it, each row keeping its number with a suffix where split.

| Old row | Goes to | Note |
|---|---|---|
| A1, A2, A3, A4, A5, A6 | software | A3's package list from WP19 on, paper packages named in `paper/CHANGES.md` from the first pin |
| B1 | software | `uv run pytest` is now the software suite |
| B2 | both | B2s `--surface software`; B2p `--surface paper` |
| B3 | both | B3s and B3p, the two register tests |
| B4 | both | the attribution grep runs in `test.yml` and `paper.yml` |
| B5 | software | the manifest, both slots |
| C1, C2, C3, C4, C5 | paper | the re-pin gate before a `submitted` or `revision` tag |
| C6, C7, C8, C10 | software | shards `fast`, `slow`, `docs`; C10 becomes "CI runs on the release pull request" |
| C9 | both | README (software); Appendix F (paper) |
| D1, D2, D3, D4 | paper | the reader round reads the paper at a pin |
| D5 | software | |
| E1 | software | staged with `--slot abstract` or `--artefact` |
| E2 | paper | a clean worktree of `paper` builds the paper (the branch build does it) |
| E3 | both | software: root, docs, `/paper/` slot; paper: the built paper at the pin |
| E4 | software | a rule for every agent; the paper list points to it |
| E5 | paper | |
| F1, F2 | software | F1 is the merge of the release pull request; F2 stays his mandate as written |
| F3 | both | the two guides (6.5) |
| F4, F5, F6, F7 | software | F7 becomes "no tag but the one `release.yml` creates" |
| G1 | software | |
| G2 | both | G2s the site and README after the merge; G2p the paper's links at the pin |

Software rows added: R1 his keyboard items confirmed with `gh api` (rulesets, environments, Pages, publishers);
R2 a `dry-run` on `qc/**` green at the head. Paper rows added: P1 `paper/mode.toml` checks `--stage served`; P2 the
release names both assets and the DOI is recorded.

### 6.4 `release-candidate.md`'s dated section

A section "Two release models (2026-11-16)", quoting nothing new: 0.1 is the software's release (package, docs, root
page) by the merge of the pull request from `dev` into `main`; the paper is in `abstract` mode at 0.1 (his approval of
the abstract, `WP64-decisions.md`); "candidate" for 0.1 is the software checklist's rows; the reader round, the
container gate and the paper's appendices move to the paper's lifecycle and its checklist; the path's step 7 is the
release pull request.

### 6.5 The reviewer's guide, recut in outline

- `reviewers-guide/software/`: README (the release pull request, its head, the release issue); sitting 1 the staged
  site (root, docs, the abstract page at `/paper/`, phone and desktop, light and dark); sitting 2 the code and the
  derivations; sitting 3 the calls made for him and the keyboard items.
- `reviewers-guide/paper/`: README (the pin, its tag and release, the mode it enters); sitting 1 the paper as
  published at the pin (the artefact staged with `--artefact`); sitting 2 the reader round and the container record;
  sitting 3 the calls on the paper.
- `gaps-and-evidence.md` and `verified.md` split by side; the current `sitting-1-paper.md` becomes the paper's
  sitting 1, `sitting-2-docsite.md` the software's sitting 1.

## 7. R-1: his answers to the sections

| Answer | Element | Section |
|---|---|---|
| Direction 12:30 | the paper's release apart from the software and docs; the code and docs released now | 1, 2 |
| Decision 12:30 | four modes: forthcoming (abstract only), working, submitted (pin), revision (pin again) | 2.3, 3.1, 3.2 |
| | a paper lifecycle and an open-source software lifecycle | 1, 2 |
| | at the software's release the abstract suffices; the abstract approved | 3.1 (value at 0.1), 3.3, 6.4 |
| Clarification 12:32 | anyone who pulls the repository can build the paper; "iterating towards a paper release", not forthcoming | 3.3 (the line, the command, the forbidden words) |
| Widened 12:34 | two release control models | 1, 2 |
| | the paper's model event-driven, from its own branch | 2.1, 2.2 |
| | docs and PyPI gated around the merge to `main` | 1.1, 1.2 |
| | spike, design, implement, test, integrate, test again | build plan |
| Q1 | a paper version cites the release active when it shipped | 2.2 (`release`, step 2) |
| | no stable release yet | 3.1 (value at 0.1) |
| | `paper` and `dev` as two branches | 2.1 |
| | reference `dev` for now: the sources stay on `dev` | 2.1, 3.3 (read from `dev`'s notebook) |
| | `dev` into `main` for 0.1 as soon as reasonable | build plan (landing order, first merge) |
| Q2 | one site with `/paper/` | 3.2, 3.5 |
| | `/paper/` on `dev` is title, author and abstract | 3.3 |
| | the full paper build on the `paper` branch | 2.2 |
| | merge `paper` into `dev`, then into `main`, to rebuild | 2.1, 2.4 step 5, 1.1 |
| | merge conflicts expected in link correctness | 2.1, 2.7 |
| | the paper is a website whose code components are pinned | 2.2 (the artefact), 2.5 |
| Q3 | Zenodo through the GitHub integration, every release | 1.2 (`publish-release`), 2.2 (`release`), 6.2 (`CITATION.cff`), his items |
| Q4 | only the current pin served | 3.2 |
| Q5 | all paper tests leave the software's gate | 5 |
| | a software change that breaks the paper shows on `paper` when it merges `dev` | 2.1, 2.2 |
| Q6 | the merge itself releases | 1.1, 1.2 |
| | failure detection | 1.3, 2.2 (`on-failure`) |
| | a clean-up script | 1.4 |
| Expectation 15:41 (on `dev` after d9e4922f) | the package clean for 0.1, `/paper/` holding only the abstract; the configuration and release work his, soon | 3.1 (value at 0.1), 3.3, build plan 5 and 6, `his-items.md` |

## 8. R-2: the couplings

| # | Coupling | Disposition | Mechanism |
|---|---|---|---|
| C1 | docs keys resolved from the notebooks | bridged | `paper/paper-keys.json` written by `paper/build_keys.py` on `paper`, carried by the merge, read by `scripts/paper_keys.py` (4) |
| C2 | citations are links to `/paper/#key` | bridged | `HTS_PAPER_SLOT`: anchors in a pinned slot, `/paper/` in abstract or fallback (3.4, 4) |
| C3 | the paper's numbers come from the package at execution | left | by Q5's design: `paper` merges `dev` and `paper.yml` re-runs the execution test; a break shows there (2.1) |
| C4 | the software gate runs the paper's tests | cut | marker `paper`, deselected without `HTS_PAPER_TESTS`; `test.yml` excludes it; `paper.yml` runs it (5) |
| C5 | Pages runs the suite and the strict paper build | cut | the composer never builds the paper; the suite runs once in `release.yml` (1.2, 3.4, 3.5) |
| C6 | one Pages site, one artefact per deploy | bridged | only `release.yml` deploys, through `pages-deploy.yml`, group `pages`; every deploy is the whole composed site; `paper.yml` never deploys (3.5) |
| C7 | the paper's build reads generated pages | cut | `paper.yml` runs `scripts/build_generated.py` itself (2.2 step 5) |
| C8 | one bibliography | left | `docs/references.bib` stays one file; conflicts resolved on `paper` before the merge into `dev` (2.1) |
| C9 | one glossary and vocabulary checker | left | as C3; the checker's `--surface` splits the gate, not the glossary (5.2) |
| C10 | the derivation ledger | left | as C3 |
| C11 | the case's ledger and data | left | as C3 |
| C12 | one lock, environment, container | left | one `uv.lock`; the paper's release notes name its hash; the re-pin gate records it (2.2, 2.5) |
| C13 | one version field and tag space | cut | paper tags `paper-*` (2.3); no workflow triggers on `v*`; `v` tags created only by `release.yml` (1.2) |
| C14 | the root page names both | bridged | the composer writes the paper card's line per mode (3.4 step 3) |
| C15 | the placeholder and its test | cut | `site/paper/index.html` deleted; the abstract page and `test_paper_slot.py` replace them (3.3) |
| C16 | the paper links `blob/main` | bridged | `paper/pin_links.py` rewrites the published artefact to the tag (2.7) |
| C17 | one claims register | bridged | the register test filters rows by `file` prefix (5.2) |
| C18 | the container gate covers both | cut | the re-pin gate belongs to `submitted` and `revision` tags; the software checklist has no container row (2.5, 6.3) |
| C19 | one staged review before a deploying merge | bridged | the release pull request's review stages the site with the slot as it will deploy (`--artefact` or abstract); the paper is reviewed at its pin (3.4, 6.5) |
| C20 | one reviewer's guide and candidate | bridged | two guides (6.5); the candidate's dated section (6.4) |
| C21 | the contract pins `/paper/` and the build | bridged | amendment 29 (6.1) |
| C22 | README, changelog, URLs mix both | bridged | `paper/CHANGES.md` for pins, `CHANGELOG.md` for the software (2.8, 6.2); README's routes stay valid |
| C23 | one branch line, one checklist | cut | two checklists (6.3); the Branching paragraph names three branches (6.2) |

## 9. What the decided design made impossible or inconsistent

1. **A dry-run dispatch on `dev` cannot run before the first merge to `main`.** A dispatch needs the workflow on the
   default branch (S-11), and `main` holds only `test.yml`. Quality control therefore runs `release.yml` and
   `paper.yml` by pushes to `qc/**` and `qc/paper/**` (1.2, 2.2); the dispatch on `dev` exists from the first merge.
2. **A failed release cannot always be undone.** PyPI keeps a version's files once accepted. After `publish-pypi`
   succeeds, the clean-up keeps the tag and the draft (exit 3) and the retry is a re-run of the failed jobs; a fix
   that needs new code ships as a new version (1.4).
3. **The PyPI publish is not a called job.** Trusted publishing does not accept a reusable workflow (S-5); the PyPI
   and TestPyPI jobs stay in `release.yml`. The site's jobs are called jobs as decided.
4. **A required code-owner review blocks a sole code owner's own pull request** (S-7). His question 1.
5. **Every merge into `main` is a release**, so a paper pin reaches the public site only with a new software
   version, and a correction to published docs needs one too. His question 2.
6. **Zenodo's archive is per repository**, by its own pages and practice: the paper's pins and the software's
   releases become versions of one record and take one metadata file (`CITATION.cff`, the software's) unless the
   paper's tagged commits carry a different one, which the merges would then carry back to `dev`. Whether a draft
   release is archived on creation or on publication is not stated by Zenodo; the design publishes drafts last.
7. **The mode file needs more than mode, pin, venue and date**: `round`, `doi`, `sha256`, `schema`; the DOI and the
   checksum exist only after the tag, so a recording commit on `paper` sits between the tag and the merge (2.4).
8. **The notebook's front matter has no author**; the page reads the author from `paper/myst.yml`.
9. **The root card says "the argument and the proofs"**, which the abstract page is not; the composer writes a line
   per mode, a wording for his read (3.4).
10. **Offline staging and a pinned slot**: the contract's staging has no network; a pinned mode stages from a local
    artefact or shows the abstract (3.4).
11. **The execution test compares text outputs exactly**, and `paper.yml` runs on x64 while the environment of record
    is linux/arm64; whether it passes there is known only at the first `qc/paper/**` run. If it does not, the test's
    exact comparisons take the existing `exact_only` mechanism of `tests/_env.py`, as the container's values do.
12. **`docs/code-owners.md` asks `pypi` for a required approval**, and Q6 makes the merge the release; the design
    drops the reviewer and records the fitness decision at the merge (6.2). `his-items.md` lists the setting.

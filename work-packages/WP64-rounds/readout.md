# WP64 readout: two release control models (stage 1, the research spike)

Read at `dev` 537f54ea on 2026-11-16; every `path:line` is at that commit. Live GitHub state was read the same
day with `gh api` (read-only). The inventory as data is `machinery.toml`.

## Summary

Today one pipeline carries both products. The paper's sources, its generators and its tests sit on `dev` beside the
package; every software gate runs the paper's tests; one strict site build builds the paper and fails without it;
one Pages deploy on a `v*` tag publishes the root page, the docs and the paper together; the docs resolve their 23
citations of the paper against the notebooks in the same checkout. There are 23 couplings (C1 to C23); five of them
must be cut or bridged for either side to move alone (C1, C4, C5, C6, C13).

Three facts about the live repository change the starting point. `main` is at e7fd1165 (2026-11-08), 2,018 commits
behind `dev`, and holds only `.github/workflows/test.yml`: `pages.yml` and `release.yml` have never been on the default
branch, so neither can be dispatched from the Actions page and neither has run. `main` has no branch protection
(`rules/branches/main` returns `[]`, `branches/main/protection` 404), the repository has no environments (count 0)
and Pages is not configured (`/pages` 404). The repository is public; the checklist row G2
(`work-packages/WP8b-release-checklist.md:88`) still says private.

## 1. The map (G1)

### 1a. Workflows

| Component | Trigger or caller | Inputs | Outputs | Path:line |
|---|---|---|---|---|
| Tests | `workflow_dispatch` (input `windows`, default true); `workflow_call` (`windows`, default false); no push or PR trigger | the checked-out ref; `uv.lock`; the toolkit pin | three Linux shards `fast`, `slow`, `docs-paper`; Windows `fast`, `slow` when asked; an attribution grep over the whole history | `.github/workflows/test.yml:6-18`, `:32`, `:39-46`, `:97-110`, `:112-120` |
| Tests, the docs-paper shard | the matrix entry `docs-paper` | `DOCS_MODULES` = `test_site`, `test_build_generated`, `test_docs`, `test_paper`, `test_container`, `test_narrative` | the slow tests of those modules | `.github/workflows/test.yml:22-24`, `:109` |
| Pages | push of a tag `v*`; `workflow_dispatch` (builds, does not deploy) | the tagged commit | the whole suite, then `assemble_site.py` (strict paper), uploaded as one Pages artefact `_site`; `deploy` to environment `github-pages` only on `refs/tags/v` | `.github/workflows/pages.yml:5-8`, `:10-12`, `:36-45`, `:47-60` |
| Release | `workflow_dispatch` (`target` dry-run or testpypi; `tag`); push of a tag `v*` | the ref; `pyproject.toml` version; `CHANGELOG.md`; `uv.lock` | checks (version equals tag, changelog entry, lock, pins, tag on `main`, TestPyPI only from `dev`); the suite through `test.yml`; wheel, sdist, CycloneDX bill; TestPyPI (env `testpypi`) or PyPI (env `pypi`); a GitHub release with the assets | `.github/workflows/release.yml:12-25`, `:41-72`, `:74-80`, `:82-121`, `:123-140`, `:142-157`, `:159-184` |
| Merge by a code owner | `pull_request_target` closed, base `dev` | the event payload; `CODEOWNERS` | a comment on failure | `.github/workflows/merge-by-code-owner.yml:6-9` |
| Pull request fields | `pull_request_target` opened, edited, synchronize | the PR description | a comment on failure | `.github/workflows/pr-fields.yml:5-7` |
| Pull request names its issue | `pull_request_target` opened, edited, labeled, unlabeled | description, labels | a comment on failure | `.github/workflows/pr-linked-issue.yml:5-7` |
| Issue admissibility | `issues` opened, edited | the issue body | `draft` label kept, comment | `.github/workflows/issue-admissibility.yml:5-7` |
| Draft label gate | `issues` unlabeled | the actor | `draft` restored when not a code owner | `.github/workflows/draft-label-gate.yml:5-7` |
| Release admissibility | read by people; enforced by `release.yml` | nine rows | the rules a `v*` tag must meet | `.github/RELEASE_ADMISSIBILITY.md:10-18` |
| Code owners | read by the admissibility scripts | one line | `@mzargham` | `.github/CODEOWNERS:3` |
| The flow and settings as written | read by people | none | `main` holds releases only; settings to make (rulesets, environments); the cut-a-release steps | `docs/code-owners.md:14-16`, `:27-38`, `:72-82` |

GitHub semantics that matter here. A `push` workflow runs for "workflows that are not merged into the default
branch", so a tag runs the workflow file at the tagged commit; `workflow_dispatch` shows its button and
`repository_dispatch` runs only when the file is on the default branch; `pull_request_target` "runs in the context of
the default branch of the base repository"; events made with the `GITHUB_TOKEN`, other than the two dispatches,
"do not create workflow runs" (docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows).
An environment can restrict deployment to "branches and tags that match your specified name patterns", and "users
who initiate a deployment cannot approve" it when self-review is prevented
(docs.github.com/en/actions/reference/workflows-and-actions/deployments-and-environments). A Pages deployment takes
one artefact and needs `pages: write` and `id-token: write`; the guide recommends that only the default branch deploy
to `github-pages` (docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages;
.../configuring-a-publishing-source-for-your-github-pages-site). That a later deployment replaces the whole site is
the reading of "one artefact per deployment"; the pages do not say it in words, and the build stage confirms it on a
dispatch. Zenodo's GitHub integration archives "new releases from the repository" without a filter
(help.zenodo.org/docs/github/enable-repository/).

### 1b. Site assembly

| Component | Trigger or caller | Inputs | Outputs | Path:line |
|---|---|---|---|---|
| `assemble_site.py` | `pages.yml:41`; `stage_site.py`; the `assembled` fixture of `tests/test_site.py:1241-1264` | `site/index.html`, `site/history.html`, `docs/`, `mkdocs.yml`, `paper/` | `_site/` with `index.html`, `history.html`, `docs/`, `paper/` | `scripts/assemble_site.py:43-48`, `:143-178` |
| The paper slot | `assemble()` | `--paper strict` (default) or `placeholder`; route `/hyperbolic-trade-space/paper` | `paper/_build/html` copied to `_site/paper/`, or `site/paper/index.html` | `scripts/assemble_site.py:68-83`, `:86-114`, `:189-195` |
| Generated pages | `assemble()` before MkDocs | `glossary.yaml`, `derivation/` | `docs/generated/glossary.md`; `build/generated/derivations.md`, `verification.md` for the paper's build | `scripts/assemble_site.py:161-166`; `scripts/build_generated.py:30-31` |
| Root figures | `assemble()` | the package's planted table and `plot_ternary` | `ternary-planted-*.png`, `site-slices-*.png` in `_site/` | `scripts/assemble_site.py:176`; `scripts/build_site_figures.py:36-42` |
| `stage_site.py` | by hand, the reviewer's guide | as assemble, route `/paper` | `_stage/` served on 127.0.0.1; nine review pages including `/paper/` | `scripts/stage_site.py:25-35`, `:56-66` |
| MkDocs hook `paper_keys.py` | `mkdocs.yml:41-42`, on every page | `paper/paper.ipynb`, `paper/supporting_material.ipynb` (`:label:` lines and `(key)=` targets) | `[text](paper:key)` becomes `../paper/#key` or `../paper/supporting-material/#key`; an unknown key fails the strict build | `scripts/paper_keys.py:24-27`, `:38-51`, `:54-70`, `:73-80` |
| Root page | copied verbatim | none | the "Read the paper" and "Use the code" cards; footer links to PyPI and releases | `site/index.html:176-180`, `:183-184` |
| Paper placeholder | `--paper placeholder` | none | "The paper is in preparation" | `site/paper/index.html:8`, `:145-151` |
| History page | `assemble()` | `history.yaml` | a link to `paper/` in the prose | `site/history.html:89` |

### 1c. The paper's build and record

| Component | Trigger or caller | Inputs | Outputs | Path:line |
|---|---|---|---|---|
| `myst.yml` | `myst build --html` in `paper/` | `paper.ipynb`, `supporting_material.ipynb`, `../docs/references.bib`, the article theme pinned to a commit | `paper/_build/html`, `myst.xref.json` | `paper/myst.yml:9`, `:12-14`, `:46-47`, `:69` |
| `execute_notebooks.py` | by hand; the container; `PAPER_EXECUTE=1` test | the two notebooks; the project kernel | outputs written in place; `figures/fig-*.png` | `paper/execute_notebooks.py:1-8`, `:19-21` |
| `paper_paths.py` | imported by every cell and generator | `PAPER_REPO_ROOT` or the parent | `sys.path` gets the root, `src`, `examples/adcs`, `paper` | `paper/paper_paths.py:15-19` |
| Generators | cells of the notebooks | the package (`generate_findings.py:18`), `case` (`generate_model.py:15`), the ledger (`generate_model.py:21`), coverage (`generate_findings.py:206`), `derivation/` (`generate_proofs.py:23`, `generate_gaps.py:20`, `:127`), `glossary.yaml` and `scripts/check_vocabulary.py` (`generate_register.py:23`, `:29`), `docs/references.bib` (`generate_prior_art.py:34`), `uv.lock` and `pyproject.toml` (`generate_repro.py:20-22`) | the appendices' tables and the paper's numbers | as listed |
| Repository links in the paper | the generators | the constant `REPO_BLOB` | links to `blob/main/...` | `paper/paper_common.py:20`; `paper/generate_proofs.py:25` |
| Container of record | by hand at gates | `Dockerfile`, a `git bundle` of HEAD, `uv.lock` | images `hts-paper`, `hts-alt`; the offline paper build | `paper/container/README.md:17-22`, `:42-49`; `paper/container/build.sh:15-21`; `paper/container/build-paper.sh:30-31` |
| `RECORD.md` | written at gates | the runs | pins including the lock hash | `paper/container/RECORD.md:16-27` |
| Length ledger | `tests/test_paper.py` | the rendered prose | the paper's ceilings | `paper/length_ledger.toml:18-19` |
| Claims register | `tests/test_claims_register.py` | 748 claims: 361 in `paper/`, 307 in `docs/`, 57 in `site/` | one register for both | `claims_register.toml` (counted with `grep '^file ='`) |
| Paper tests | the `fast` shard (unmarked) and the `docs-paper` shard (slow) | committed outputs, generators | stale outputs fail with "re-run `execute_notebooks.py`" | `tests/test_paper.py:61`, `:723`, `:879`; gated `PAPER_EXECUTE` `:2583`, `PAPER_BUILD` `:2605-2608` |

### 1d. Docs-to-paper couplings in the tests

| Component | Trigger or caller | Inputs | Outputs | Path:line |
|---|---|---|---|---|
| Docs cite only by key | `test_site.py` | docs pages | no raw `paper/` link in a docs page | `tests/test_site.py:387` |
| Keys equal the built labels | `test_site.py`, skips without a built paper | `paper/_build/html/myst.xref.json` | each key on the page the resolver names | `tests/test_site.py:420-433` |
| Root doors | `test_site.py` | `site/index.html` | exactly `paper/` and `docs/getting-started/` | `tests/test_site.py:484-496` |
| Assembled layout | `test_site.py`, slow | `--paper placeholder` | `_site/paper/index.html` equals the placeholder | `tests/test_site.py:1257`, `:1267-1279` |
| Live routes | `test_site.py` | the contract | `paper/` among the eight live routes | `tests/test_site.py:108-117` |
| Pages triggers pinned | `test_site.py` | `pages.yml` | triggers exactly `v*` tags and dispatch; deploy `if` on `refs/tags/v` | `tests/test_site.py:1199-1229` |
| Shard names | `tests/test_ci_shards.py` | `test.yml` | `["fast", "slow", "docs-paper"]` | `tests/test_ci_shards.py:19` |
| Interface contract | amended, never drifted | the `[docs]` and `[build]` tables | `reference_key_*`, `paper_cmd`, `public_paths` with `/paper/` | `work-packages/interface-contract.toml:90-97`, `:245`, `:268-270`, `:293-300` |

### 1e. Release records

| Component | Trigger or caller | Inputs | Outputs | Path:line |
|---|---|---|---|---|
| Version | `release.yml` version check | `pyproject.toml` | `0.0.1`; `__version__` 0.0.1 | `pyproject.toml:3`; `src/hyperbolic_trade_space/__init__.py:16` |
| URLs | PyPI metadata | none | Homepage, Documentation, Changelog on `blob/main` | `pyproject.toml:30-35` |
| One environment | `uv sync` | groups | `paper` is a default group beside `dev`, `case`, `docs` | `pyproject.toml:48`, `:52` |
| Changelog | `release_checks.py changelog` | entries | `[Unreleased] - target 0.1.0`, paper and software entries mixed | `CHANGELOG.md:8-11`, `:36-38`, `:46` |
| README | read | none | links to `/docs/` and `/paper/` | `README.md:3-6`, `:33` |
| Release checklist | by hand | sections A to G | A (version) and F (merge) software; C3, C5, D1 to D4 paper; B, C1, C2, C6 to C9, E both | `work-packages/WP8b-release-checklist.md:12-88` |
| Release candidate | by hand | mandate, path, entry surfaces | the candidate as one thing | `work-packages/release-candidate.md:5`, `:46`, `:68`, `:163` |
| Punch list | by hand | live URLs | the `/paper/` route; version; Pages first deployment | `work-packages/release-punch-list.md:16`, `:49-50` |
| Reviewer's guide | by hand | the staged site | four sittings, the first is the paper | `work-packages/reviewers-guide/README.md:7-11`; `sitting-1-paper.md:3-5` |
| Branching convention | read | none | commit to `dev`; `git merge --no-ff dev` into `main` when content merits CI; a merge that would deploy is preceded by a staged review of root, docs and paper | `work-packages/README.md:62-74` |

Three records drift from the tree. `work-packages/README.md:68-69` says CI "runs on pushes and pull requests to
`main`"; `test.yml:3-6` runs on dispatch and call only. `docs/code-owners.md:27` asks `main` to require a pull
request while `:76` merges and pushes to `main` directly. The checklist's G2 calls the repository private; it is public.

## 2. The couplings (G2)

| # | Coupling | Mechanism (path:line) | What breaks if one side moves alone | What cuts or bridges it |
|---|---|---|---|---|
| C1 | The docs' 23 citations resolve against the notebooks in the same checkout | `scripts/paper_keys.py:38-51`; `mkdocs.yml:41-42` | notebooks leave the software's tree: every docs build fails; a key renamed on the paper's side: the next docs build fails | a committed key manifest (key to page) on the software side, refreshed by a paper pin; or the notebooks stay on the software side |
| C2 | The citations are relative links to `/paper/#key` on the same site | `scripts/paper_keys.py:61-67` | in abstract mode the anchors do not exist; a paper served elsewhere breaks every link | the resolver takes a base and a mode; in abstract mode it links the abstract page |
| C3 | The paper's numbers come from the package and the case at execution | `paper/paper_paths.py:15-19`; `paper/generate_findings.py:18`; `paper/generate_model.py:15`, `:21` | a package change makes committed outputs stale | the paper pins a software commit or version and executes against it |
| C4 | The software gate runs the paper's tests | `.github/workflows/test.yml:22-24`, `:104`, `:109`; `tests/test_paper.py:723`, `:879` | a software PR fails on a paper staleness test | the paper's tests move to the paper's workflow, or the stale-output tests are marked and leave the software gate |
| C5 | Pages runs the whole suite and the strict paper build before deploying the docs | `.github/workflows/pages.yml:36-41`; `scripts/assemble_site.py:189-195` | a paper that does not build blocks a software release | the software deploy takes the paper slot from the paper's last published artefact, or from the mode page |
| C6 | One Pages site, one artefact per deployment | `.github/workflows/pages.yml:42-45`, `:47-60` | a paper deploy and a docs deploy overwrite each other | one composer that always builds the whole site from both latest artefacts; or a second site for the paper |
| C7 | The paper's build reads pages the software side generates | `scripts/assemble_site.py:161-164`; `scripts/build_generated.py:30`; `work-packages/interface-contract.toml:245` | the paper built alone lacks `derivations.md`, `verification.md` | the paper workflow runs `build_generated` itself |
| C8 | One bibliography | `paper/myst.yml:46-47`; `paper/generate_prior_art.py:34`; mkdocs `bibtex` | an entry added for the paper lands in the docs' bib, and the reverse | one owner side; the other reads it at its pin |
| C9 | One glossary and one vocabulary checker | `paper/generate_register.py:23`, `:29` | a glossary edit makes Appendix D stale | as C3 |
| C10 | The derivation ledger and proof record | `paper/generate_proofs.py:23`; `paper/generate_gaps.py:20`, `:127` | a new lemma makes the appendices stale | as C3 |
| C11 | The case's ledger, data and coverage | `paper/generate_model.py:21`; `paper/generate_findings.py:206`; `paper/generate_repro.py:41` | a case re-run moves the paper's numbers | as C3 |
| C12 | One lock, one environment, one container | `pyproject.toml:48`, `:52`; `paper/container/README.md:8-11`; `paper/container/RECORD.md:27` | a dependency bump for the package changes the paper's environment of record | the paper pins the lock with its software commit |
| C13 | One version field and one tag namespace | `pyproject.toml:3`; `.github/workflows/release.yml:24-25`, `:41-51`; `.github/workflows/pages.yml:6-7` | a paper tag that starts with `v` would publish to PyPI and deploy | paper tags that cannot match `v*` (`paper-...`) |
| C14 | The root page names both | `site/index.html:176-180`; `tests/test_site.py:484-496` | the paper card says nothing of the mode | the root card reads the mode |
| C15 | The placeholder and its test | `site/paper/index.html:8`, `:150`; `tests/test_site.py:1267-1279` | "in preparation" is the wording he set aside | the abstract page replaces the placeholder |
| C16 | The paper links the repository at `blob/main` | `paper/paper_common.py:20`; `paper/generate_proofs.py:25` | a pin built from the paper's branch links files at today's `main`, which may differ or 404 | link at the pinned commit |
| C17 | One claims register for both | `claims_register.toml` (361 paper rows of 748) | a paper edit on its branch fails the software's register test, or the reverse | split by surface, or the test filters by `file` |
| C18 | The container gate covers both | `paper/container/README.md:42-49`; checklist C1 to C5 (`WP8b-release-checklist.md:37-41`) | a software release waits on the paper's re-pins | the container gate belongs to the paper's pins; the software gate keeps the suite |
| C19 | One staged review of root, docs and paper before a deploying merge | `work-packages/README.md:71-74`; `scripts/stage_site.py:25-35`; checklist E1, E2 (`:62-63`) | a docs release needs the paper staged | a review per side, with the slot staged from the paper's artefact |
| C20 | The reviewer's guide and the candidate are one | `work-packages/reviewers-guide/README.md:7-11`; `work-packages/release-candidate.md:68` | his sign-off covers both at once | a guide per release model |
| C21 | The interface contract pins `/paper/` and the build | `work-packages/interface-contract.toml:268-270`, `:293-300`; `tests/test_site.py:108-117` | any change drifts from the contract | an amendment |
| C22 | README, changelog and URLs mix both | `README.md:3-6`; `CHANGELOG.md:36-38`, `:46`; `pyproject.toml:30-35` | the software changelog announces paper work | a paper change record of its own |
| C23 | One branch line, one checklist | `work-packages/README.md:62-70`; `WP8b-release-checklist.md:12-88` | rows of one side block the other | the checklist split by side |

## 3. Candidate designs (G3)

The paper's branch is called `paper` throughout, a placeholder. "The mode file" is `paper/mode.toml` (mode, pin,
venue, date) in every design; only where it lives changes.

### 3a. The paper's model

| | P1: pointer branch, sources stay on `dev` | P2: the paper owns its branch | P3: tags on `dev`, no branch |
|---|---|---|---|
| What lives on `paper` | the mode file and nothing else; the branch is fast-forwarded to a commit of `dev` or `main` that the author chooses | `paper/` (notebooks, generators, figures, myst, ledger, container record) and the paper's tests; `main` and `dev` lose `paper/` except the key manifest | no branch; the mode file on `dev` |
| How it takes software changes | by moving the pointer to a newer commit of `dev` | `git merge main` into `paper` (one way), then re-execute | it is on `dev` |
| How its edits flow back | they are made on `dev` already | shared files (`references.bib`, `glossary.yaml`) by a PR to `dev`; the key manifest by the paper workflow's PR to `dev` | none needed |
| Events | push to `paper` (a mode or pointer change) builds; a tag `paper-working-<date>`, `paper-submitted-<venue>`, `paper-revision-<venue>-r<n>` publishes; `workflow_dispatch` with a dry-run input | push to `paper` builds the working paper; the same tag shapes pin | a `paper-*` tag on a `dev` commit publishes; `workflow_dispatch` |
| Gates | paper tests (structural, executed outputs, `PAPER_BUILD`), the key check, the length ledger, the paper rows of the claims register; he approves a `paper-pages` environment; record in `work-packages/paper-decisions.md` | as P1, run on `paper`; the container re-pin before a `submitted` or `revision` tag | as P1, run on the tagged commit |
| Artefacts | `paper-html.tar.gz` and `paper-keys.json` attached to a GitHub release of the tag; the composed site; optional deposit per pin | as P1 | as P1 |
| Abstract mode | `/paper/` is the abstract page: title, author, the approved abstract read from the notebook's front matter, "iterated towards release", the build command | same | same |
| Working mode | `/paper/` is the paper built at the pointer, a banner naming the commit and date | built at `paper`'s head | built at the last `paper-working-*` tag |
| Submitted mode | `/paper/` is the paper at `paper-submitted-<venue>`, banner with venue and date (and DOI if deposited) | same | same |
| Revision mode | `/paper/` is the paper at `paper-revision-<venue>-r<n>`; earlier pins kept or dropped per Q4 | same | same |
| Failure modes | the pointer names a commit whose outputs are stale (the workflow re-executes or refuses); the software's tests on `dev` still fail on paper staleness (C4 stays); a paper deploy without the composer erases the docs (C6) | `main` merged into `paper` conflicts in shared files; the docs' manifest lags the paper; links in the paper at `blob/main` miss `paper/` files (C16) | a paper tag on a commit not on `main` links files `main` lacks (C16); C4 stays |
| Cost to build | new `paper.yml`; `assemble_site.py` (mode, slot from artefact); `paper_keys.py` (manifest or notebooks); `site/paper/` abstract page; `test.yml` (move paper tests or not); `test_site.py`, `test_paper.py`; mode file; contract amendment | as P1, plus removing `paper/` and the paper's tests from `dev`; `paper_paths.py` stays; the manifest as the docs' only key source; claims register split | as P1 without the branch |
| Cost to the reader | sees one site; the paper's mode and date stated | same | same |
| Cost to the author | edits the paper on `dev` as now; moves a pointer to publish | edits on `paper`; merges `main` in to see new software | edits on `dev`; tags to publish |
| Cost to the maintainer | software PRs still carry paper staleness unless C4 is cut | two lines of history to keep in step | least to keep; nothing separates the two histories |

### 3b. The site's composition (both models deploy one site)

| | H1: one composer, both events | H2: a second site for the paper |
|---|---|---|
| Mechanism | one workflow `site.yml` builds root and docs from the latest `v*` tag and the paper slot from the latest paper release asset (or the abstract page from the mode file); triggered by a `v*` tag and by a paper tag; one `concurrency: pages` group | the paper deploys to the Pages of a second repository; `/paper/` on the main site is the abstract page that links there |
| Failure modes | a paper event rebuilds docs from the last tag (intended); a failed fetch of the paper asset falls back to the abstract page and says so | two URLs; the docs' anchors cross sites; a second repository to govern |
| Cost | `pages.yml` replaced; `assemble_site.py`; tests | a repository, its settings and its workflow |

### 3c. The software's model

| | S1: merge, then tag by hand | S2: the PR to `main` is the gate, the merge releases | S3: merge deploys docs, tag publishes the package |
|---|---|---|---|
| The gate around `main` | a PR `dev`→`main` (ruleset: PR required, checks `test (fast)`, `test (slow)`, `test (docs)`, code-owner review); merged `--no-ff` | same PR and checks; the PR carries the version and the changelog entry | same PR and checks |
| Events | a `v*` tag pushed by a code owner on the merge commit | the merge (push to `main`) runs `release.yml`, which creates the tag and runs Pages and PyPI as called jobs (a tag created by `GITHUB_TOKEN` starts no other workflow) | push to `main` deploys the docs; a `v*` tag publishes to PyPI |
| Artefacts | wheel, sdist, bill, GitHub release, the site from the tag | same, from the merge commit | the site from `main`'s head; the package from the tag |
| Docs' citations when `paper` is ahead | the docs resolve against the manifest pinned on `main`; a newer paper pin may drop a key: the composer checks the docs' keys against the deployed paper's labels and falls back to the abstract page per link | same | same |
| When `paper` is behind | a key the docs need is not yet in a pin: the build fails at the `main` PR, not at deploy | same | same |
| The root page | the paper card reads the mode and pin from the paper's latest release; the abstract in abstract mode | same | same |
| Failure modes | a tag forgotten after the merge leaves `main` ahead of PyPI and the site; a tag on the wrong commit is refused (`release.yml:63-67`) | a failed release after the merge leaves `main` holding an unreleased version; a re-run needs the tag deleted | the docs describe `main`'s head, which is a release only while `main` holds releases only (`docs/code-owners.md:14`) |
| Cost to build | `release.yml` (unchanged in shape), `site.yml`, `test.yml` (shard rename if C4 is cut), the ruleset and environments (his keyboard), `docs/code-owners.md`, checklist | as S1, plus `release.yml` takes `push: main` and calls the site and publish jobs; `test_site.py` pins | as S1, plus a `push: main` trigger on the site workflow; `test_site.py:1199-1203` changes |
| Cost to the reader | the docs and PyPI move together at a tag | same | the docs may lead PyPI by the time between merge and tag |
| Cost to the author | one more command after the merge | none after the merge | as S1 |
| Cost to the maintainer | today's documented flow, least change | the most automation to test; a failure mid-release is harder to recover | two publication events to keep in step |

## 4. His decisions (G4)

In the order he would answer them, one at a time.

1. **Where do the paper's sources live?**
   (a) On `dev`, as now; the `paper` branch holds only the mode and which commit to build (P1). The paper keeps
   reading the newest software; the software's tests keep checking the paper unless question 5 cuts them.
   (b) On the `paper` branch only; `dev` and `main` keep the package, the docs and a key list (P2). The two histories
   separate; the paper takes software changes by merging `main` in.
   (c) On `dev`, with no paper branch; a paper release is a tag on a `dev` commit (P3). Least to build; nothing
   separates the two histories.
2. **Where is the paper read?**
   (a) At `/paper/` on the one site, rebuilt whenever either side releases (H1).
   (b) On a site of its own, with `/paper/` on the main site holding the abstract and a link (H2).
3. **Does each pinned version get a DOI?**
   (a) No deposit.
   (b) Zenodo through its GitHub integration: every GitHub release is archived, the software's as well.
   (c) Zenodo for the paper's pins only, by an upload step in the paper's workflow (a stored token).
   (d) arXiv at submission, by hand.
4. **When the paper is pinned again, does the site keep the earlier pins?**
   (a) Only the current one at `/paper/`.
   (b) The current one at `/paper/` and each earlier pin at `/paper/<tag>/`.
5. **Do the paper's tests leave the software's gate?**
   (a) All of them: they run only in the paper's workflow.
   (b) The checks of committed outputs leave; the structural checks of the notebooks stay.
   (c) All stay, as now.
6. **What publishes the software?**
   (a) A code owner merges the PR into `main`, then pushes the `v*` tag (S1, today's written flow).
   (b) The merge of the PR itself: the workflow tags and publishes (S2).
   (c) The merge deploys the docs; the tag publishes the package (S3).

His keyboard items, whatever he answers: the `main` and `dev` rulesets, the environments (`pypi`, `testpypi`,
`github-pages`, a paper environment), Pages set to GitHub Actions, the trusted publisher on PyPI and TestPyPI
(`docs/code-owners.md:25-38`). None exists today.

### The driver's own calls

- The branch name `paper` and the tag shapes `paper-working-<yyyymmdd>`, `paper-submitted-<venue>`,
  `paper-revision-<venue>-r<n>`; none starts with `v`, so `release.yml:24-25` and `pages.yml:6-7` cannot fire on them.
- The mode file's name and fields (`paper/mode.toml`: mode, pin, venue, date).
- The key manifest's form (`paper-keys.json`: key, page) and that the docs' build fails on a key it lacks.
- One `concurrency: pages` group for every deploy.
- The paper's repository links at the pinned commit instead of `blob/main` (`paper/paper_common.py:20`,
  `paper/generate_proofs.py:25`).
- The three drifts (records against the tree) corrected in the build stage (`work-packages/README.md:68-69`,
  `docs/code-owners.md:27`/`:76`, checklist G2).
- The first merge to `main` since e7fd1165 carries the new workflows, so the dispatch buttons and any
  `repository_dispatch` exist only after it.

## 5. The sequence (G5)

| Stage | Package | Deliverable | Gate | Records it amends |
|---|---|---|---|---|
| 2 decide | WP65, design | the chosen designs written as specifications: workflow files in outline, the mode file, the manifest, the abstract page's content, the test list, the contract amendment; the checklist split drafted | his answers to questions 1 to 6 recorded verbatim; the design approved | `WP64-decisions.md`; `interface-contract.toml` (amendment drafted) |
| 3 build | WP66a software model, WP66b paper model, WP66c composer and abstract page, in parallel, one file set each | the workflows, `assemble_site.py`, `paper_keys.py`, `site/paper/`, the tests | each unit's tests green locally; dispatches in dry-run only | `docs/code-owners.md`; `.github/RELEASE_ADMISSIBILITY.md`; contract amendment landed |
| 4 quality control | WP67 | `release.yml` dry-run dispatch, the site workflow's build without deploy, the paper workflow's dry run, on `dev`; `machinery.toml` diffed against the built state; the staged site in a browser in each of the four modes, with captures | every row of the diff explained; captures in the record | `WP8b-release-checklist.md` (split into the software's and the paper's) |
| 5 integrate | WP68 | the land on `dev`; the first `--no-ff` merge to `main` since e7fd1165; his keyboard items; the paper in abstract mode | CI green on `main`'s head; his settings confirmed with `gh api` | `release-candidate.md`; `release-punch-list.md`; `CHANGELOG.md`; `README.md`; root page |
| 6 review the cascade | WP69 | a re-read of every record and page that names the release, the paper's route or the branches, to a clean merged state; the reviewer's guide recut into the software's and the paper's | no record contradicts the tree; his read | `work-packages/reviewers-guide/`; `INDEX.md`; `driver-log.md` |

## What could not be established

- Whether a later Pages deployment replaces the whole site is not stated in GitHub's pages; the build stage confirms
  it on a dispatch before H1 is relied on.
- No workflow of `pages.yml` or `release.yml` has ever run (they are not on `main`), so their behaviour on GitHub is
  untested; the tag-on-`main` check, the environment approvals and the Pages deploy are known from the files only.
- Whether the PyPI and TestPyPI trusted publishers are registered was not readable without his accounts.
- The time a full paper execution and container re-pin take in a paper workflow on a hosted runner (the record has
  146 s for execution on his machine, `paper/container/RECORD.md:50`); the platform of record is linux/arm64, which a
  hosted Linux x64 runner is not, so exact values may differ outside the container (`paper/container/README.md:39-40`).

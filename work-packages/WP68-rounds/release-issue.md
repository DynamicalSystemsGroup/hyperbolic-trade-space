# Release 0.1.0 (the issue's text; opened on GitHub with the pull request, on his word)

The first merge of `dev` into `main` since e7fd1165 (2026-11-08). The merge is the release
(`work-packages/WP65-design/specification.md`, section 1): `release.yml` tags `v0.1.0`, publishes the package to
PyPI, composes and deploys the site with the abstract page at `/paper/`, publishes the GitHub release. Zenodo stays off (his word, 2026-11-17: until a first full draft of the paper is
approved), so this release is not archived and mints no DOI. This issue is closed by the pull request.

## What the merge carries

2,094 commits since e7fd1165 and the packages below, newest first, by their rows in `work-packages/INDEX.md`
(the documents of the landed ones are read at `git show 4f81a4ea:work-packages/<file>`, WP73).

- WP78 governance as executable: the release rules declared in the tree, checked first in CI, attested in the
  release notes (in flight, part of 0.1)
- WP77 the package renamed `tradespace` (import, distribution, repository, Pages address; contract amendment 30)
- WP74 both requirement-usage type names accepted (the external review's finding 7)
- WP73 the process record left the tree; the index dereferences; `tests/test_index.py`
- WP67 quality control of the two release control models: dry runs on `qc/**`, the browser pass per mode, the
  machinery diff; lint and the fast shard on every push to `dev` (record: `work-packages/WP67-rounds/record.md`)
- WP66a, WP66b, WP66c the two release control models built: `release.yml`, `paper.yml`, `site.yml`,
  `pages-deploy.yml`, the composer and the abstract page, the key manifest, the paper marker
- WP65, WP64 the two release control models designed (his six decisions)
- WP71 the wheat page: the level V against biomass; WP70 the iron triangle probed; WP72 the invariant estimator
  spike (records only; nothing in `src/`)
- WP63 the examples with an arc; WP60 the three example pages; WP59 conditioning on the three public cases
- WP62, WP61 the tree holds the current state; the work-packages directory indexed and thinned
- WP57, WP56, WP55, WP54, WP53 the paper: appendices, Sections 7 to 9, the mathematics, the skeleton, his review
  batch of 2026-11-15
- WP52 the governance lineage on the history page; WP51 the root page recast; WP50, WP49, WP48 research spikes
  (holes by persistent homology; the contributor covenant; governance checks)
- WP47 release engineering and repository governance; WP46 the fit temperature as a path
- WP45 two public case studies and a two-metric example; WP44 the second case study found; WP43 the kernel
  direction tested; WP42 tension and the glossary; WP41 the bridge to the search, part 1
- WP40 release thinning; WP39 the case ends in a decision; WP38 the residual pass; WP37 the history page
- WP36 future directions (formal results, Rust/WASM); WP35 HoroPCA distinguished; WP34 Windows as a third
  platform; WP33 journeys and signposting; WP32 package-user tests; WP31 choosing K
- WP30 the model revision (momentum headroom, the fleet-size variant); WP29 the noise result
- WP28 improvement by subtraction; WP27, WP26 the model in the view editor; WP24 "facet" goes; WP23 the
  model-realism loop; WP22 the system model's two views
- WP20 verification in tiers; WP19 the paper's figures; WP18 ternary plots; WP17 the several-term fit with soft
  weights; WP16 the data swap; WP15 the system model tidy-up; WP14 the interface contract

In flight and not part of the release decision: WP8b (its checklist is `release-checklist-software.md`), WP11
(reader loops), WP25 (tidiness, recurring), WP58 (the sweep after the merge).

## Version, changelog, checks

- Version 0.1.0 in `pyproject.toml`, `uv.lock`, `__version__` and `CITATION.cff` (commit: _to fill_).
- `CHANGELOG.md` `[0.1.0] - <merge day>`.
- The checks at the head: `work-packages/WP68-rounds/checks.md` (the software suite with paper tests deselected,
  lint, format, lock, the lemma chain and the proof-map checker, the vocabulary and claims checks on the software
  surfaces, the strict docs build in both slots, the index test).
- CI: the dispatched run at the head (_link to fill_: every shard on Linux, the Windows fast and slow shards); the
  `qc/release` dry run at the head (_link to fill_: admissibility, test, build, site green; tag, publish, deploy,
  release skipped; the summary names the slot `abstract`).
- The staged site at the head looked at: `/`, `/paper/`, one docs page, 1,280 and 375 px, light and dark
  (`work-packages/WP68-rounds/record.md`); the pinned modes and the fallback in WP67's record.

## Before the merge (his keyboard; `work-packages/WP65-design/his-items.md`)

- [x] Pages: Source = GitHub Actions
- [x] Environments: `github-pages` (branch `main`), `pypi` (branch `main`, no reviewers), `testpypi` (branch
      `dev`), `paper-release` (tags `paper-*`, reviewer `mzargham`, self-review allowed)
- [x] Rulesets: `main-review` (the review rule with him as bypass for 0.1) and `main-checks` ( the four required checks `test (fast)`, `test (slow)`,
      `test (docs)`, `admissibility`; merge commits only; no force push, no deletion); `dev` and `paper` (no
      force push, no deletion)
- [x] Trusted publishers: PyPI and TestPyPI pending publishers for `release.yml`, environments `pypi` and `testpypi`
- [x] Zenodo stays off (his word, 2026-11-17)
- [x] The driver reads the settings back with `gh api` and records them in `WP68-rounds/record.md` (G7, 2026-11-17)

## After the merge

- The release run watched to its end: the tag, PyPI, the site, the GitHub release.
- `git branch paper dev && git push origin paper`; the `paper` ruleset applied.
- `danlessa` (and Rohan, once his GitHub login is in `CODEOWNERS`) added as Owner of `tradespace` on PyPI
  and TestPyPI (Manage, Collaborators), by him in his signed-in session: the project exists only after the first
  publish, and trusted publishing creates it under the account that registered the pending publisher.
- The punch list's post-release checks loaded live (`work-packages/release-punch-list.md`).
- The paper branch's first items filed in `release-checklist-paper.md`: the three paper tests that fail on hosted
  runners (the residual-count baseline; the clean-kernel notebook check's tab-F-datasets drift; the myst build's
  full-size figure links), from WP67's G4 and G5.
- The `qc/release` branch deleted.

# Release punch list (WP8b)

Links and checks that are placeholders until the first release. `tests/test_site.py` reads the
URLs in the first section as expected-at-release: they are not counted as broken before the
release. After the merge and the first deployment, tick each post-release check after loading it
live. A broken link found live is fixed in a patch release. Every box below is ticked (done), struck
through with the decision that moved it, or labelled post-release.

## Expected-at-release links

The root and paper pages are checked live under "Post-release live checks".

- https://github.com/DynamicalSystemsGroup/tradespace/releases (release notes; linked from the package card on the root page)
- https://pypi.org/project/tradespace/ (PyPI project page; a placeholder link in the root page's footer until the first publish, 404 before it: "this should also have a placeholder link for pypi", 2026-11-14 night)
- https://dynamicalsystemsgroup.github.io/tradespace/ (root; the public URL and `site_url` base)
- https://dynamicalsystemsgroup.github.io/tradespace/paper/ (paper page; `/paper/` serves the mode named in `paper/mode.toml`, which is `abstract` for 0.1.0: the title, the author and the abstract; the pinned paper's artefact once the mode names a pin (WP66c, `bf823f22`; WP65 specification 3.4, `git show 4f81a4ea:work-packages/WP65-design/specification.md`))

## Not linked yet

- PyPI: published by the Release run on the merge into `main`, by trusted publishing (WP47, `1cd23dbd`; WP65
  specification 1.1); the root page's footer carries the project-page link (listed above as expected-at-release),
  live once that run has published.

## Post-release live checks


After the first tag deployment, each URL loads and shows its page (base
`https://dynamicalsystemsgroup.github.io/tradespace/`):

- [ ] GitHub releases page (release notes) loads and lists 0.1.0 (post-release)
- [ ] `/` root, two cards (the paper, getting started) and the footer links work; the Why triangle (light and dark scheme) and the What slices load and open at full size on click. Both images are generated at build time from the planted table (`scripts/build_site_figures.py`; WP51, `01ad0839`): confirm the triangle's three region labels read "all three trade", "metric 3 trades against metric 1", "metric 3 trades against metric 2" on the deployed build, as the build on this Mac printed them at WP68's checks (labels come from the fit and could differ by platform)
- [ ] `docs/`
- [ ] `docs/getting-started/` (the five-line example matches the output shown)
- [ ] `docs/user-guide/overview/` (the user-guide pages load from its navigation)
- [ ] `docs/theory/` (math renders)
- [ ] `docs/generated/glossary/` (compiled from `glossary.yaml`)
- [ ] `docs/api-reference/`
- [ ] `docs/further-reading/` (references listed)
- [ ] `paper/`

## Items for the release package (WP8b)

Collected from the records; each is ticked, struck with the decision that moved it, or labelled post-release.

- [x] Archive cleared: the retired WP7 notebook, its test and its figures were deleted at 4bd6bac (the driver's negative-edit decision of 2026-11-10; supervisor, `WP10-decisions.md` OD3: "plan to clean out the archive before the first release"); the stale manifest entry left the contract at amendment 18 (WP25-4 row T-1).
- [ ] ~~PDF export through the SciPy typst template~~ after 0.1 (supervisor, `WP10-decisions.md` OD4: later, once the content has settled; the candidate path of `release-candidate.md`: "the PDF export later").
- [x] Docsite references to the paper by stable reference keys (supervisor, 2026-11-08; `WP8b-scope-of-work.md` D-6, `WP8b-decisions.md` OD-A2 (a)): landed inside 0.1, after WP28's acceptance; `[text](paper:key)`, resolved by `scripts/paper_keys.py` (contract amendment 19).
- [ ] ~~Publish the pinned container image (`Dockerfile`; WP10 D-13) to a registry~~ not for 0.1 (supervisor, WP10: "we can optionally publish it to a registry later"; mandate: no image on a registry for 0.1); the paper documents the local build only.
- [ ] ~~PyPI / TestPyPI deferred ("pypi deferred for pending feedback from friends and collaborators")~~ moved by WP47's Amendments 1 and 2 (his word, `c6faaf72`, `451d58f9`) and WP65's specification 1.1: the Release run publishes to PyPI by trusted publishing on the merge into `main`; the footer's project-page link and the "Not linked yet" entry go live with it (post-release).
- [x] Version 0.1.0 (driver, WP8b D-5, `WP8b-scope-of-work.md`; `CITATION.cff` added to the set by WP65 specification 6.2): `pyproject.toml`, `uv.lock`, `__version__` and `CITATION.cff` (with `date-released`) read 0.1.0 and `CHANGELOG.md`'s `[Unreleased] - target 0.1.0` heading became `[0.1.0] - <date>`, written by WP68 (D-1, D-2) as the last change before the pull request, no tag; the date is the merge's day. The tag and the GitHub release follow the supervisor's merge (post-release).
- [ ] The site deploys from the Release run on the merge into `main` (`release.yml`, through `site.yml` and `pages-deploy.yml`; the tag-triggered `pages.yml` of WP14 G-2 was removed by WP66a, `708ef565`, contract amendment 29): confirm the first deployment runs from that run and that the staged-site review preceded it (branching convention, `work-packages/README.md`) (post-release).
- [ ] Reading pass: 9 rows marked "confirm" (author to confirm) and 1 "supervisor" (INCOSE) in `paper/reading_pass.yaml`, Appendix G.2 (`WP10-review-2.md` C-3) (the author's, post-release).
- [ ] Paper venue and byline: sole author, Dynamical Systems Group, ORCID as in the SciPy template (`WP10-decisions.md`); confirm when a venue is chosen (post-release).
- [x] `LICENSE` (MIT, Dynamical Systems Group) agrees with `license = { text = "MIT" }` in `pyproject.toml`; check the GitHub repository's license badge after the first push to the public repository (post-release).

## After 0.1 (recorded during the candidate; not release items)

- `trade_off_report` (named `tension_report` until WP42) at K > 1 refuses at the first term whose near-frontier rows fall below `min_near_frontier`,
  so the paper's case module gets the other terms' readings by calling it with the guard off and applying the
  same guard of ten per term itself (the driver's call of 2026-11-10, `driver-log.md`). After 0.1 the public
  function should return per-term availability itself: a reading for each term that meets the guard and a
  stated refusal, with the count, for each that does not.

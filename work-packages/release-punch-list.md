# Release punch list (WP8b)

Links and checks that are placeholders until the first release. `tests/test_site.py` reads the
URLs in the first section as expected-at-release: they are not counted as broken before the
release. At the first release (WP8b), tick each line after loading it live. A broken link found
live is fixed in a patch release.

## Expected-at-release links

- [ ] https://github.com/DynamicalSystemsGroup/hyperbolic-trade-space/releases (release notes; linked from the package card on the root page)
- [ ] https://dynamicalsystemsgroup.github.io/hyperbolic-trade-space/ (root; the public URL and `site_url` base)
- [ ] https://dynamicalsystemsgroup.github.io/hyperbolic-trade-space/paper/ (paper page; `scripts/assemble_site.py` stages the real paper, built by `myst build --html` in `paper/` for the route `/hyperbolic-trade-space/paper`, and falls back to the placeholder page when the paper does not build)

## Not linked yet

- PyPI project page: no link on any page (PyPI is deferred). Add the link to the package card
  and this list when the package is published.

## Post-release live checks

After the first tag deployment, each URL loads and shows its page (base
`https://dynamicalsystemsgroup.github.io/hyperbolic-trade-space/`):

- [ ] `/` root, three cards, links work; the Why triangle (light and dark scheme) and the What figure load and open at full size on click. The Why image is generated at build time from the planted table (`scripts/build_site_figures.py`): confirm its three region labels read "all three trade", "metric 3 trades against metric 1", "metric 3 trades against metric 2" on the deployed build (labels come from the fit and could differ by platform)
- [ ] `docs/`
- [ ] `docs/getting-started/` (the five-line example matches the output shown)
- [ ] `docs/user-guide/overview/` (the user-guide pages load from its navigation)
- [ ] `docs/theory/` (math renders)
- [ ] `docs/generated/glossary/` (compiled from `glossary.yaml`)
- [ ] `docs/api-reference/`
- [ ] `docs/further-reading/` (references listed)
- [ ] `paper/`

## Items for the release package (WP8b)

Collected from the records; tick each when done or decided.

- [ ] Archive cleared: `examples/adcs/adcs_trade_study.ipynb` (the retired WP7 notebook) is to be archived with a banner, then the archive removed before the first release (supervisor, `WP10-decisions.md` OD3: "archive it with banner for now so we can use it as reference but plan to clean out the archive before the first release"). Status: not yet archived; the notebook is pinned by `tests/test_notebook.py` and `work-packages/interface-contract.toml` (lines for `produced_by_numbered` and the examples list), so moving or removing it is a contract amendment.
- [ ] PDF export through the SciPy typst template: later, once the content has settled (supervisor, `WP10-decisions.md` OD4); added at the release package or when a venue is chosen.
- [ ] Docsite references to the paper by stable reference keys (a key registry resolved at build time, like LaTeX labels and refs), after the paper and its appendices are stable (supervisor, 2026-11-08; `WP8a-scope-of-work.md`; `driver-log.md` 2026-11-08 entry on docstrings). Until then the docsite carries no citations into the paper.
- [ ] Optionally publish the pinned container image (`Dockerfile`; WP10 D-13) to a registry (supervisor, WP10: "we can optionally publish it to a registry later"); the paper documents the local build only. Release-candidate mandate: no image on a registry for 0.1.
- [ ] PyPI / TestPyPI: deferred ("pypi deferred for pending feedback from friends and collaborators"); when published, add the link to the package card and this list.
- [ ] Version 0.1.0, tag and GitHub release (WP8b): `CHANGELOG.md` section `Unreleased` to be dated and renamed to `0.1.0` at the tag; `__version__` in `src/hyperbolic_trade_space/__init__.py` currently reads 0.0.1 and must match `pyproject.toml` (to confirm with the driver, who owns the version).
- [ ] Pages workflow (`pages.yml`) triggers on a release tag `v*` or manual dispatch only (WP14 G-2): confirm the first deployment runs from the tag and that the staged-site review preceded it (branching convention, `work-packages/README.md`).
- [ ] Reading pass: 9 rows marked "confirm" (author to confirm) and 1 "supervisor" (INCOSE) in `paper/reading_pass.yaml`, Appendix G.2 (`WP10-review-2.md` C-3).
- [ ] Paper venue and byline: sole author, Dynamical Systems Group, ORCID as in the SciPy template (`WP10-decisions.md`); confirm at release.
- [ ] `LICENSE` present and consistent with `pyproject.toml` (`license = { text = "MIT" }`); check the GitHub repository's license badge after the first push to the public repository.

- Deferred (supervisor, 2026-11-08): docsite references to the paper by stable reference keys (a key registry resolved at build time, like LaTeX labels and refs), added only after the paper and its appendices are stable (post-WP11); until then the docsite carries no citations into the paper.
- Optionally publish the pinned container image (Dockerfile; WP10 D-13) to a registry (supervisor, WP10: "we can optionally publish it to a registry later"); the paper documents the local build only.

## After 0.1 (recorded during the candidate; not release items)

- `tension_report` at K > 1 refuses at the first term whose near-frontier rows fall below `min_near_frontier`,
  so the paper's case module gets the other terms' readings by calling it with the guard off and applying the
  same guard of ten per term itself (the driver's call of 2026-11-10, `driver-log.md`). After 0.1 the public
  function should return per-term availability itself: a reading for each term that meets the guard and a
  stated refusal, with the count, for each that does not.

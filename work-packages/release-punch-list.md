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

- Deferred (supervisor, 2026-11-08): docsite references to the paper by stable reference keys (a key registry resolved at build time, like LaTeX labels and refs), added only after the paper and its appendices are stable (post-WP11); until then the docsite carries no citations into the paper.
- Optionally publish the pinned container image (Dockerfile; WP10 D-13) to a registry (supervisor, WP10: "we can optionally publish it to a registry later"); the paper documents the local build only.

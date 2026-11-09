# Release punch list (WP8b)

Links and checks that are placeholders until the first release. `tests/test_site.py` reads the
URLs in the first section as expected-at-release: they are not counted as broken before the
release. At the first release (WP8b), tick each line after loading it live. A broken link found
live is fixed in a patch release.

## Expected-at-release links

- [ ] https://github.com/DynamicalSystemsGroup/hyperbolic-trade-space/releases (release notes; linked from the package card on the root page)
- [ ] https://dynamicalsystemsgroup.github.io/hyperbolic-trade-space/ (root; the public URL and `site_url` base)
- [ ] https://dynamicalsystemsgroup.github.io/hyperbolic-trade-space/paper/ (paper page; today a placeholder that says the paper is in preparation, WP10 replaces it with the paper)

## Not linked yet

- PyPI project page: no link on any page (PyPI is deferred). Add the link to the package card
  and this list when the package is published.

## Post-release live checks

After the first tag deployment, each URL loads and shows its page (base
`https://dynamicalsystemsgroup.github.io/hyperbolic-trade-space/`):

- [ ] `/` root, three cards, links work
- [ ] `docs/`
- [ ] `docs/method/` (math renders)
- [ ] `docs/generated/derivations/`
- [ ] `docs/generated/verification/`
- [ ] `docs/api-reference/`
- [ ] `docs/literature/` (bibliography listed)
- [ ] `paper/`

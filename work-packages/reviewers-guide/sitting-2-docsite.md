# Sitting 2: the docsite, the root page and the history page

Entry point: http://127.0.0.1:8791/ (root page), then http://127.0.0.1:8791/docs/ and
http://127.0.0.1:8791/history.html. The pages `scripts/stage_site.py` prints are `/`, `/docs/`,
`/docs/getting-started/`, `/docs/user-guide/overview/`, `/docs/theory/`, `/docs/generated/glossary/`,
`/docs/api-reference/`, `/docs/further-reading/` and `/paper/`. Not opened for this draft.

- [ ] Root page, `site/index.html` (close read, surface 1 of 5): does it route you by need, and say whom it is for?
  The change record is the "Entry surfaces" section of `work-packages/supervisor-review-list.md`.
- [ ] `README.md` (surface 2 of 5), read as GitHub shows it: the first screen is an install line and a first call.
- [ ] The abstract (surface 3 of 5): read it in the paper, sitting 1; tick it here too.
- [ ] History page, `site/history.html` (surface 4 of 5), with its record `history.yaml`. Open items for you are in
  `work-packages/WP37-rounds/open-items.md`; its acceptance is pending.
- [ ] Docs home, `docs/index.md` (surface 5 of 5), rendered at `/docs/`.
- [ ] Walk the user guide from Getting started to the Overview; run the five-line example and compare it with the
  output shown (`work-packages/release-punch-list.md`, post-release checks).
- [ ] Theory page: does the mathematics render, no `$` left on the page?
- [ ] Resize to phone width (375 px), light and dark; tables should become lists, nothing scrolls sideways.
- [ ] Follow every link out of the root page and the README. The release-notes and public-site links are expected to
  fail until the release (`work-packages/release-punch-list.md`, "Expected-at-release links").
- [ ] Decide whether the residual pass's remaining flags on these pages matter (`work-packages/WP38-review.md`).

Evidence: `work-packages/WP33-review.md` (wayfinding rounds), `work-packages/WP37-review.md`,
`work-packages/WP40-review.md`, `work-packages/WP32-review.md` (package-user tests). Browser-pass screenshots are
retrievable from commit `2a669de` (`work-packages/README.md`). The checks for the docs build fixtures
(`tests/test_site.py`, `tests/test_docs.py`) failed in one review worktree; see `gaps-and-evidence.md`.

# Sitting 2: the root page, the docsite and the history page

Entry point: http://127.0.0.1:8791/ (root page), then http://127.0.0.1:8791/docs/ and
http://127.0.0.1:8791/history.html. The pages `scripts/stage_site.py` prints are `/`, `/docs/`,
`/docs/getting-started/`, `/docs/user-guide/overview/`, `/docs/theory/`, `/docs/generated/glossary/`,
`/docs/api-reference/`, `/docs/further-reading/` and `/paper/`.

- [ ] Root page, `site/index.html` (entry surface 1 of 5): the order is the summary paragraph, Why, What, then the
  closing doors. The summary paragraph and "bespoke or opaque" are the two sentences that are yours. Review it
  against your prose and rulings in `work-packages/WP51-decisions.md` and the "Entry surfaces" section of
  `work-packages/supervisor-review-list.md`. Its second figure is still the paper's Figure 1; the fan figure is
  waiting (sitting 4).
- [ ] `README.md` (surface 2 of 5), as GitHub shows it: an install line and a first call on the first screen, the
  package-only install, a layout that names every top-level entry. Run the first call.
- [ ] The abstract (surface 3 of 5): read in sitting 1; tick it here too.
- [ ] History page, `site/history.html` (surface 4 of 5): the essay, about 1,660 words against your bound of 2,000,
  the dissertation opening the arc, the closing on Meltdown, no generated list on the page. Review it against your
  rulings in `work-packages/WP52-decisions.md`. Your carving pass ("every word and reference earns its place") is
  still ahead; the record behind the page is `history.yaml`, kept for fact-checking, with the tests that tie every link,
  name and year to it. Open items: `work-packages/WP37-rounds/open-items.md`.
- [ ] Docs home, `docs/index.md` (surface 5 of 5), at `/docs/`: five need links, the quickstart block and the figure
  it draws (a preview of Getting started's Figure 1), at your bound of 350 words
  (`work-packages/WP51-decisions.md`, "The docs home").
- [ ] Walk the user guide from Getting started to the Overview; run the five-line example and compare it with the
  output shown (`work-packages/release-punch-list.md`, post-release checks). New pages to read: the tension pages
  (`docs/user-guide/tensions.md` and `docs/user-guide/tension-routes.md`) against `work-packages/WP42-decisions.md`.
- [ ] The two pages landed last: the bridge page (`docs/bridge.md`) against
  `work-packages/WP41-decisions.md`, and the temperature page (`docs/user-guide/temperature.md`) against
  `work-packages/WP46-decisions.md`. The fresh reader's page requests on the bridge page are in
  `work-packages/WP41-review.md`.
- [ ] The word "white space" is the one word for the chart's unoccupied region; "hole" is reserved for the topological
  work (`work-packages/WP42-decisions.md`, "Naming item 1"). Look for the word "hole" on the pages you read.
- [ ] Theory page: does the mathematics render, no `$` left on the page? Then phone width (375 px), light and dark:
  tables become lists and nothing scrolls sideways.
- [ ] Follow every link out of the root page and the README. The release-notes and public-site links are expected to
  fail until the release (`work-packages/release-punch-list.md`, "Expected-at-release links").

Evidence: `work-packages/WP33-review.md` (wayfinding rounds), `work-packages/WP37-review.md`,
`work-packages/WP40-review.md`, `work-packages/WP32-review.md` (package-user tests). Browser-pass screenshots of the
earlier passes are retrievable from commit `2a669de` (`work-packages/README.md`).

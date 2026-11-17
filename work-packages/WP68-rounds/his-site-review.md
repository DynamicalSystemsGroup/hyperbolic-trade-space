# His click-through of the site and the documentation (before the pull request)

His word (2026-11-17): "i need to do a full review of the documentation and top level static site for me to click
through." The site at the head of `dev` (the commit that adds this file, named in `driver-log.md`) is staged with `scripts/stage_site.py --slot abstract` and served
on `http://127.0.0.1:8797/`. It is the site the Release run deploys at the merge, with three local differences:
it is served at the root rather than under `/hyperbolic-trade-space/`; the docs theme's lookup of the latest GitHub
release prints one console error (404 until a release exists); and the two external links in the root page's footer
(the releases page, the PyPI project page) go live only with the release. The paper slot is the abstract page in
every case until a paper pin exists.

Findings go in the last column, or in chat; the driver carries each into a unit (a wording cut, a figure, a page) or
into a question here, and nothing is opened on GitHub until the table is his.

## The top-level site (three pages)

| Page | URL | What it is | His notes |
|---|---|---|---|
| Root | `/` | the title, the author, three paragraphs, the ternary figure with its three regions, the two cards (the paper, getting started), the footer | |
| History | `/history.html` | the governance lineage (WP37, WP52) | |
| Paper | `/paper/` | the abstract page; the full paper comes with the paper branch | |

## The documentation, in the navigation's order

| Page | URL | His notes |
|---|---|---|
| Home | `/docs/` | |
| Getting started | `/docs/getting-started/` | |
| User guide: start here | `/docs/user-guide/overview/` | |
| Conditioning | `/docs/user-guide/conditioning/` | |
| Fitting | `/docs/user-guide/fitting/` | |
| The fit temperature | `/docs/user-guide/temperature/` | |
| Choosing K | `/docs/user-guide/choosing-k/` | |
| Trade-offs and tensions | `/docs/user-guide/tensions/` | |
| Routes back from a tension | `/docs/user-guide/tension-routes/` | |
| Chart | `/docs/user-guide/chart/` | |
| Prediction | `/docs/user-guide/prediction/` | |
| Termination | `/docs/user-guide/termination/` | |
| Limitations | `/docs/user-guide/limitations/` | |
| API | `/docs/api-reference/` | |
| Examples (the cubesat case) | `/docs/examples/` | |
| Perovskite solar cells | `/docs/examples/perovskite/` | |
| Amniote life histories | `/docs/examples/amniote/` | |
| Broadbalk wheat | `/docs/examples/wheat/` (WP71's sentence on the level V and biomass is his call: keep or cut) | |
| From the chart back to a design | `/docs/bridge/` | |
| Theory in brief | `/docs/theory/` (its nine citations of the paper land on the abstract page until a pin exists) | |
| Glossary | `/docs/generated/glossary/` | |
| Further reading | `/docs/further-reading/` | |
| Code owners | `/docs/code-owners/` | |

## What the driver checked at the head

Every route above answers 200 (`driver-log.md`, 2026-11-17); the rendering pass at 7e6839a0 (`record.md`, G5) and
WP67's per-mode pass stand, since no page changed between 7e6839a0 and that commit except the Zenodo lines of `docs/code-owners.md`.

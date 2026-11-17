# Reviewer's guide, 0.1 candidate

For the supervisor, Michael Zargham, who alone decides on the merge (`work-packages/release-candidate.md`, "The
mandate"). Nothing is tagged, published or merged.

## What the package is

The candidate is the `dev` branch at the head `a63d390` (commits after it on `dev` are records: this guide, the
driver log and the cleanup manifest). It holds the Python package
`tradespace`, the paper with its supporting material, the docsite, the root page with the history page, the
derivations, the cubesat case study, and the release engineering for the first publication (workflows, code owners,
contributing page, covenant, templates). The package is at version 0.0.1 on `dev`: a candidate for 0.1, not 0.1 until the
merge to `main` is being done; 0.1.0 is the first release's version and is set in that workflow, on your word, before
the tag (`work-packages/WP8b-decisions.md`, "The version and the candidate"; the release checklist's rows A1 to A3).

Landed on `dev` since the first reader round: your acceptances of WP33, WP35, WP37, WP38, WP39 and WP40; the root page
recast to your prose; the history page as an essay; the docs home with its quickstart block and figure; the three
test records of WP45 (perovskite, amniote, Broadbalk wheat); the figure loop's fixes (fix4); the WP42 build (tension,
the tension matrix as Figure 7, the glossary's layers, the renamed package functions); the WP43 spike on the kernel
direction; WP47 release engineering with the covenant and the contributing page of WP49; the WP48 and WP50 readouts;
the abstract with its three thrusts.

Landed after those, in order: the fifth paper unit (the record defects of the held-out reads, a573155), the bridge
page of WP41 (af54b3b), the docs home's quickstart block drawing the figure it shows (30ba54d) and the temperature
page of WP46 (a63d390); each landing is recorded with its checks in `work-packages/driver-log.md`.

Waiting on your word: the fan figure of WP51 (branch `wp51fig`, served apart from the staged site), the abstract
phrases the readers flagged (change request 172), the dependency and the first package that WP50 leaves for after 0.1,
and the keyboard items for PyPI, the GitHub environments and branch protection
(`work-packages/WP47-rounds/pypi-checklist.md`). Sitting 4 lists them.

## Four sittings, one entry point each

Each sitting is a checklist of about ten lines; each line says where to look and what you review it against. Take them
on different days, in any order; the order below is the one that reads best. Stage once with
`uv run python scripts/stage_site.py --serve --port 8791` (it prints the pages and stops with Ctrl-C). Use another
port if 8791 is taken.

| Sitting | What it covers | Entry point |
|---|---|---|
| [1](sitting-1-paper.md) | the paper and its appendices | http://127.0.0.1:8791/paper/ |
| [2](sitting-2-docsite.md) | the root page, the docsite, the history page | http://127.0.0.1:8791/ |
| [3](sitting-3-code.md) | the code, the derivations and the release engineering | `src/tradespace/`, `derivation/`, `.github/` (files, not a page) |
| [4](sitting-4-calls.md) | the calls made for you, every changed number, what waits on you | `work-packages/supervisor-review-list.md` (a file) |

The close read you announced (the five entry surfaces: the root page, the README, the abstract, the history page and
the docs home; and the reading pass of Appendix G.2) is spread across sittings 1 and 2 and gathered in sitting 4.

The pages the staging script prints are `/`, `/docs/`, `/docs/getting-started/`, `/docs/user-guide/overview/`,
`/docs/theory/`, `/docs/generated/glossary/`, `/docs/api-reference/`, `/docs/further-reading/` and `/paper/`
(`scripts/stage_site.py`, `REVIEW_PAGES`); the appendices are at `/paper/supporting-material/` and the history page at
`/history.html` (`work-packages/WP40-review.md`).

## What a pass looks like

A sitting is done when each checklist line is ticked or turned into a note to the assistant. The assistant's
verification is recorded in [verified.md](verified.md); it does not replace your read.

## The rest of the guide

- [verified.md](verified.md): what was verified by machine and what was validated by people, kept apart.
- [gaps-and-evidence.md](gaps-and-evidence.md): known gaps, each with where its record lives, and an index of the
  records.

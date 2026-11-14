# Reviewer's guide, 0.1 candidate (draft)

For the supervisor, Michael Zargham, who alone decides on the merge (`work-packages/release-candidate.md`, "The
mandate"). Drafted from `work-packages/WP8b-reviewers-guide-skeleton.md`; not yet approved. Nothing is tagged,
published or merged.

## What the package is

The candidate is the `dev` branch at a named head (the head is named when the guide is handed over; this draft was
written at `c23cf60`). It holds the Python package `hyperbolic_trade_space`, the paper with its supporting material,
the docsite, the root page with the history page, the derivations, and the cubesat case study. The package is at
version 0.0.1 until the last release step (`work-packages/WP8b-release-checklist.md`, row A1).

## Four sittings, one entry point each

Each sitting is a checklist of about ten lines. Take them on different days, in any order; the order below is the
one that reads best. Stage once with `uv run python scripts/stage_site.py --serve --port 8791` (it prints the pages
and stops with Ctrl-C). Use another port if 8791 is taken.

| Sitting | What it covers | Entry point |
|---|---|---|
| [1](sitting-1-paper.md) | the paper and its appendices | http://127.0.0.1:8791/paper/ |
| [2](sitting-2-docsite.md) | the docsite, the root page, the history page | http://127.0.0.1:8791/ |
| [3](sitting-3-code.md) | the code and the derivations | `src/hyperbolic_trade_space/`, `derivation/` (files, not a page) |
| [4](sitting-4-calls.md) | the calls made for you, every changed number, what is weak | `work-packages/supervisor-review-list.md` (a file) |

The close-read list (the five entry surfaces and Appendix G.2) is one named item, split across sittings 1 and 2 and
gathered in sitting 4.

## What a pass looks like

A sitting is done when each checklist line is ticked, or the line is turned into a note to the assistant. The
assistant's own verification is recorded elsewhere (see [verified.md](verified.md)); it does not replace your read.
Where the guide says "pending", the thing has not been run.

## The rest of the guide

- [verified.md](verified.md): what was verified by machine and what was validated by people, kept apart.
- [gaps-and-evidence.md](gaps-and-evidence.md): known gaps, and an index of where each record lives.

## Not confirmed when this draft was written

The staged site was not built for this draft, so no localhost address here was opened. The page paths come from
`scripts/stage_site.py` (`REVIEW_PAGES`), from `work-packages/WP40-review.md` (R-8: `/`, `/docs/`, `/paper/`,
`/history.html`, `/paper/supporting-material/` all 200) and from `scripts/assemble_site.py`. The final reader round
(`work-packages/WP11-decisions.md`, "The final reader round") has not run: results are pending.

# WP8a — Decision records (site skeleton up)

Records typed by the agent (driver session). Decisions are the supervisor's.

## Origin (2026-11-08)

- Breakdown row WP8a (`README.md`), OK'd by the supervisor with the interface-contract condition;
  the draft scope by the PM's bounded subagent (`WP8a-scope-of-work.md`, f341690). Layout and tone
  decisions inherited from `WP8-decisions.md` ("Amendment 1 revised", the root index as thin HTML
  after hc-marimo, a growing landing page for talks). Release control from WP14's gate: a deploying
  merge is preceded by a recorded review of the staged localhost site.

## Decision loop (2026-11-08)

- **OD1, where the live-site check sits.** Options: accept on the staged site with the live check
  after the merge / acceptance waits for the live site. **Supervisor (mzargham), verbatim:** "Accept
  on the staged site; live check after the merge". Disposition: decided; acceptance is judged on the
  localhost assembly reviewed by the supervisor plus a green manual build run on `dev`; the merge to
  `main` follows; the public URL is checked afterwards and recorded in this file, fix-forward if it
  fails.

- **OD2, a working-draft label on the public site.** Options: visible line / no label.
  **Supervisor (mzargham), verbatim:** "no label we don't deploy to main and thus github pages until
  we have an actual first release. in the mean time its local host review loops"
- Disposition: decided, no label; and a consequence for the package: nothing is deployed to GitHub
  Pages before the first release (WP8b). WP8a still delivers the Pages workflow, but it must not
  trigger on pushes to `main` (merges to `main` continue for CI); it triggers on the release tag or
  on manual dispatch only, and the first deployment is WP8b's. Review loops run on the localhost
  staging build (WP14 R-12). OD1's "live check after the merge" therefore moves to WP8b's release;
  WP8a's acceptance is judged on the staged localhost site plus a green manual build run on `dev`.
  OD3 (the paper card before WP10) no longer concerns a public page and becomes a default: the card
  is shown and links to the placeholder on the staging site.

- **Agent's defaults, as one item** (OD3 folded in). **Supervisor (mzargham), verbatim:** "you are
  allowed to include placeholder links that are not live yet as long as they will be live on an
  official release. don't make extra steps for yourself and don't crowd your attention with
  caveats. just keep a bang list for review once its live and if a link is broken we detect and fix
  it in a patch"
- Disposition: defaults approved with that change: links to pages that will exist at the first
  release (the paper under `/paper/`, the PyPI page once published, release notes) may be placed
  now; the link test treats them as expected-at-release rather than broken; a punch list
  (`work-packages/release-punch-list.md`) records every such link and anything else to verify once
  the site is live, checked at WP8b and fixed in a patch where broken; no caveat text on the pages.
  Loop closed: decided 2 (OD1, OD2), OD3 folded into the defaults, raised 0, defaults approved with
  the link policy.

## Scope approval (approval gate)

- **Document:** `work-packages/WP8a-scope-of-work.md` with its "Gate outcomes" and link policy
  (no open items).
- **Date:** 2026-11-08.
- **Driver's question:** "WP8a, the site skeleton: root index after hc-marimo, MkDocs docsite under
  /docs/, the /paper/ slot, the generated ledger and verification pages, one assembly-and-serve
  command for localhost review, the Pages workflow armed for the release tag and manual dispatch
  only, tests, the punch list; no open items. Do you approve the scope for execution?" (options:
  Approved / Not yet).
- **Supervisor (mzargham), verbatim:** "Approved"
- **Disposition:** approved; the PM executes on `dev` against WP14's contract as it lands;
  acceptance is judged on the supervisor's review of the staged localhost site plus a green
  dispatch build on `dev`; no deployment before the first release.

## Front matter and link fixes

Applied last (D-9). The only change to each page is the front-matter block of four lines at the top of the file, with the page's world (`world: embodied | symbolic | formal`, rendered as the world line under the title by `overrides/partials/content.html`):

| File | Line | Before | After |
|---|---|---|---|
| `docs/why-and-how.md` | 1 | (none) | `---` / `world: embodied` / `---` / blank line |
| `docs/method.md` | 1 | (none) | `world: formal` block |
| `docs/preconditioning.md` | 1 | (none) | `world: symbolic` block |
| `docs/api.md` | 1 | (none) | `world: symbolic` block |
| `docs/limitations.md` | 1 | (none) | `world: formal` block |
| `docs/literature.md` | 1 | (none) | `world: formal` block |

`docs/index.md` carries no world (it maps all three). The generated pages carry no front matter; the override sets their world (`formal`). No title key was needed. Link fixes: none; `mkdocs build --strict` and `tests/test_site.py` find no broken relative link in the six pages.

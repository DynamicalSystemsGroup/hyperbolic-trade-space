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

## Scope approval (approval gate)

- pending (OD2, OD3, the defaults as one item, then approval)

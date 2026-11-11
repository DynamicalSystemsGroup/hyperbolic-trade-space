# WP34 — Decisions (Windows as a third platform)

The supervisor's words are quoted verbatim where they bind (release-candidate.md, "Windows"); the assistant's calls are listed for his review.

## Scope gate (2026-11-11, 12:20; scope at 95c3c03; the assistant)

No open decisions; the Agent's defaults approved as one item, with one change to the mechanism: GitHub dispatches only a workflow file that exists on the default branch, and `main` has no `windows.yml`, so the spike job moves into `test.yml` as a `windows-latest` job behind a `workflow_dispatch` input (`windows`, default false) that the assistant sets to true when dispatching; pushes do not run it until stage 4 folds it into the matrix at gates. **Assistant, verbatim:** "WP34 approved as drafted; the spike runs from test.yml behind a dispatch input."

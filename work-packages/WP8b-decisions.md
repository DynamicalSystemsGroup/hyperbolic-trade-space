# WP8b — Decisions (release preparation for 0.1.0)

Approvals and acceptances are the driver's under the mandate (`release-candidate.md`, "The mandate"); the
supervisor's words are quoted verbatim where they bind; the driver's calls are listed for his review at the PR.
The driver records each deliverable's verdict here (`WP8b-scope-of-work.md`, Agent's defaults).

## Scope gate (2026-11-09)

Recorded in `driver-log.md` (2026-11-09), quoted verbatim:

> - 2026-11-09: WP8b (release preparation) and WP20 (verification in tiers) scoped by the fresh PM's
>   bounded scope subagents in the template, no open decisions; approved by the driver under the
>   mandate. WP8b brings the items done ahead of its scope (LICENSE, changelog, punch list, archive)
>   under it and sequences the reference keys and the reviewer's guide after WP11's stopping rule and
>   the version last. WP20 covers the slow markers, `scripts/check.py`, the xdist group and the CI
>   shards; its first two commits are already on `dev` (04a3471, 78f5e1c) and are accepted against it.

For the driver: the scope's header (`WP8b-scope-of-work.md`, Status) still reads DRAFT although its Gate outcomes
section records this approval. The header is left as it is until the driver updates it.

## Amendment 1


## Amendment 1, the driver's decisions (2026-11-10, 23:05)

- **OD-A1 (a), with (c) as the fallback.** Pin the article theme's version in `paper/myst.yml` if `mystmd` resolves a
  versioned site template; if it does not (the implementer shows the attempt), `scripts/stage_site.py` fetches or
  copies the templates itself before the build (c). Either way the proof is a test or a CI step that stages the site
  from a clean worktree with no copy by hand.
- **OD-A2 (a).** D-6 lands inside 0.1 after WP28 is accepted, as the supervisor's words of 2026-11-08 and step 6 of the
  path record; nothing here changes his recorded word.

**Driver, verbatim:** "Amendment 1 approved with OD-A1 (a) falling back to (c) on evidence, and OD-A2 (a)."

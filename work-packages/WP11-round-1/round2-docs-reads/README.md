# WP11 D-6, docsite round 2: the three task readers' reports, verbatim

Committed before their triage (R-3). Each file is the reader's report byte for byte, with the
header table the harness wrote (task, model, date, site commit, checkout). Nothing was edited; the
hash of each file equals the hash of the file the reader wrote.

## The staged site

- Commit c6d0fffd4193a26f0ce66eff4185fe92d174f7ad (c6d0fff on `dev`), built with
  `uv run python scripts/stage_site.py` and served locally at `http://127.0.0.1:8791/`: the root
  page, `/docs/` (the docsite as built by MkDocs) and `/paper/`. Each reader also had a clean
  worktree of the repository at c6d0fff (`readers/round2-docs/wt-{1,2,3}`), synced with `uv sync`,
  in which to run what the pages say to run.
- The docs pages (`docs/*.md`, `docs/user-guide/*.md`, the generated glossary) are unchanged
  between c6d0fff and the head of `dev` at the triage (ca6ce94).

## The tasks and the models

D-6's loop gives a package user one task each and nothing else: no persona brief, no slice, the
whole site and the checkout open to them.

| Reader | Task | Model | Report |
|---|---|---|---|
| R1 | Install the package and run a first fit on the package's own example data; say what the fit told you | sonnet | `R1.md` |
| R2 | Read a tension report for the example and choose K (how many terms); say what you chose and why | the session's default model | `R2.md` |
| R3 | Read a termination record (what the fit's stopping diagnostics say) for the example; say whether the fit converged and how you know | the session's default model | `R3.md` |

## What a reader returns

In its own words: what the site is about; the pages followed, in order; the commands run and
their output; where it got stuck or stopped, quoting the passage; terms it had to guess; the
task's answer (what the fit told it; what K it chose and why; whether the fit converged and how
it knows); what it believes the method does and does not do; what it would do next. No ratings.
The reader was not told that other readers exist, that a triage follows, or what the triage
checks.

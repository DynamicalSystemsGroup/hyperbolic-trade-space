# WP79 decisions

The scope's approval is the driver's under his mandate, quoted in `WP64-decisions.md` (his words of 2026-11-17: "No
read-through before the release"; "Contributing to the paper takes its own route"; OD-1 "paper PRs are approved by
mzargham or jshorish", 13:05 EST). Nothing below is an approval; the items are the unit's defaults, applied, and the
questions the rehearsal leaves for him, each with its plain options.

## Unit A (the rehearsal, G1), 2026-11-17

Record: `WP79-rounds/rehearsal.md`.

**Defaults applied by the unit.**

- The dispatch of `paper.yml --ref paper` waited for the push run of c0e210cc (44122627220) to end: the two share the
  concurrency group `paper-refs/heads/paper` with `cancel-in-progress` on, so a dispatch during the push run would have
  cancelled it.
- The merge test ran locally only; the `qc/paper/touch` and `qc/paper/touch-dev` branches were never pushed (a push
  would have cost one 50-minute paper run each for no new information beyond the dispatch), and both were deleted at
  the end.
- The three fixes of the failing paper tests are proposals in the record, not commits on `paper`.

**For him, one at a time when the record is read.**

1. The residual baseline (`scripts/residuals_baseline.json`, taken at c0fe11b; 52 paper and appendix counts above it
   at c0e210cc, the same 52 locally and on the runner). Options: (a) re-take it at the head that is tagged first
   (`check_residuals.py --write-baseline`, the whole report; the comparison then exits 0); (b) accept the 52 rises row
   by row with his read, leaving the baseline; (c) re-take it and note in the file which packages moved the counts.
2. The clean-kernel notebook test's exact comparison of the datasets table outside the environment of record. Options:
   (a) the test compares the way the F-table test does (the planted digest masked, numbers within `text_rtol`), one
   `if` in `tests/test_paper.py`; (b) execute the notebooks in the container of record before the first tag and keep
   the exact comparison, which still fails on amd64 runners; (c) both.
3. The myst build test under `BASE_URL`. Options: (a) the test reads `BASE_URL` and matches the prefixed path (two
   lines); (b) the test's subprocess runs with `BASE_URL` removed, testing a build other than the one published.
4. Serving a pin while Zenodo is off: the mode file, the composer and the banner require a DOI. Options: (a) keep it
   (no served pin before the first full draft, which is his sequence); (b) let `doi` be empty in `working` mode and
   drop "DOI ..." from the banner until it is minted; (c) a placeholder DOI, which the record advises against (it would
   be a link to nothing on every page).
5. The fixes' home: the three are software-side files (`tests/`, `scripts/`), so either the paper's branch carries
   them to `dev` by the design's merge (2.1) or a software unit lands them on `dev` first and `paper` merges `dev` in.

## Unit B (the route made clear and enabled, G2 to G4; the two test fixes), 2026-11-17

Branch `wp79b`, cut from `dev` at 99b24b9f; nothing pushed, nothing opened on GitHub. OD-1 applied as answered:
the paper's approvers are `mzargham` and `jshorish`.

**Defaults applied by the unit.**

- The CODEOWNERS line is written `/paper/   @mzargham @jshorish`, with the leading slash: GitHub reads `paper/` as
  any directory of that name and the tree also has `site/paper/` (the abstract page the software composes), which
  stays with the `*` line. Both readers (`scripts/admissibility.py`, and `scripts/check_repo_settings.py` through
  it) accept `paper/` and `/paper/`; the prose calls it the `paper/` line. The `*` line's logins remain the code
  owners alone: `jshorish` is a paper approver and not a code owner, `danlessa` and `rororowyourboat` are code
  owners and not paper approvers, `mzargham` is both.
- The declaration's `[paper_approvers]` section sets `minimum_permission = "read"` (approval needs no write);
  the live check reads `write` (maintain) for `jshorish` and `admin` for `mzargham`, so it conforms with margin.
  GitHub itself asks write access of a login on a CODEOWNERS line before it requests their review; the declaration
  states the floor the route needs, not GitHub's.
- The declaration's `governed_files` entry for CODEOWNERS now names both lines and both readers; no file was added
  to the set of secondary rules.
- One pull request template (the scope's default), with a `Paper` section at the end; the pr-fields check reads
  that section on a pull request into `paper` only, and a pull request into `dev` leaves it empty. The paper's row
  in `PR_ADMISSIBILITY.md` says so. The linked-issue check is unchanged and has no branch filter: a pull request into
  `paper` names an issue or carries `small-fix`, as the software's does; whether the paper wants its own issue form
  is not decided here.
- The merge check on `paper` has no one-person notice (the approvers are two); with no `paper/` line at all it
  fails and says so, rather than passing silently.
- The merge workflow (`merge-by-code-owner.yml`) keeps its file name (the declaration names it) and fires on pull
  requests closed into `dev` and `paper`; its job is renamed to say which role merges on which base.
- `docs/code-owners.md` gains the one pointing sentence, and its "Adding a code owner" paragraph now says where the
  paper's approvers are declared (the `paper/` line and the environment), since its old wording named the
  environment alone.
- The two test fixes are unit A's options 2(a) and 3(a), on `dev` (software-side files): the clean-kernel test
  compares each cell with the helper the F-table tests already use (`_current`: byte-equal in the environment of
  record, elsewhere the planted digest masked and numbers within `text_rtol`), and the myst build test takes
  `BASE_URL` as the figure paths' prefix. `paper/environment_values.toml` names the clean-kernel test in the
  `elsewhere` text. `scripts/residuals_baseline.json` is untouched (question 1 is his).
- `CONTRIBUTING.md` says that `tests/` and `scripts/` are the software's even when the paper's tests read them, and
  change on `dev`; this is the practice the two fixes follow and the answer to question 5 in practice, recorded here
  for him to confirm or reverse.

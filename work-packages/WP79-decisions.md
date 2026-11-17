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

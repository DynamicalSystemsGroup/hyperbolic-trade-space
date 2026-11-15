# Sitting 4: the calls made for you, and what waits on you

Entry point: `work-packages/supervisor-review-list.md` (a file; open it in an editor or on GitHub). It lists each call
the assistant made that you did not rule on yourself, with the reason, the record and the landing commit, so a revert
is one `git revert`. Its main table runs from 2026-11-08 to the WP39 rows of 2026-11-13, and its "Entry surfaces" rows
run to the root page rows of 2026-11-14. Calls after that (WP41 to WP52, the integration of the units on landing
branches, the figure fix, the cleanup) are in `work-packages/driver-log.md`, in the entries from "PM16 reported after
two hours" to the last one, and in the decision files of the same packages.

- [ ] Read the main table, newest first; mark any call you would revert and check it against the file it cites.
- [ ] Read the later calls in `work-packages/driver-log.md`: the abstract's Pareto sentence kept, the abstract's three
  thrusts, the docs home budget, the figure-numbering fix, the renumbering of the claims and the lemma (Lemma 22) at
  landing, the WP43 rerun, and the WP47 to WP50 landings. Each entry says what was decided and why.
- [ ] "Entry surfaces" and "Further items of the supervisor's close read" in the review list, then the history page,
  docs home and abstract changes made after them (above). Take the five surfaces and Appendix G.2 as one close read
  (`work-packages/supervisor-tasks.md`, W7 and W8); the residual checker does not replace it.
- [ ] Every changed number: `work-packages/WP30-rounds/data-gate/conclusions.md` (changed conclusions first),
  `work-packages/swap-evidence.md`, and the "Data of record" line in `work-packages/deliverables-grid.md`. The case is
  read at K = 2, on the container's data.
- [ ] Overruled calls, kept so the pattern shows: `work-packages/driver-log.md`, "Overruled or corrected".
- [ ] Acceptances you have given: WP33, WP35, WP37, WP38, WP39 and WP40, in one line, recorded in each decisions
  file; WP49's covenant texts, signed off (`work-packages/WP49-decisions.md`, "Sign-off"); WP48's readout was accepted by the assistant under the mandate, and its questions are yours (below). Still
  yours: the third paper unit and the abstract landing (W2), and each remaining delivery as it lands (W9)
  (`work-packages/supervisor-tasks.md`).
- [ ] Waiting on your word, as plain options (no order, none steered): the fan figure of WP51, branch `wp51fig`,
  served apart from the staged site (it merges only on your word; `work-packages/WP51-decisions.md`, last section);
  the abstract's phrases of change request 172; WP50's dependency choice (GUDHI, which carries a GPL v3 dependency,
  or ripser with scipy) and the first package of the later release, options A to D
  (`work-packages/WP50-rounds/spike/readout.md`); WP48's three questions (the form of a check, the first checks, when
  they run), after 0.1 (`work-packages/WP48-rounds/spike/readout.md`).
- [ ] The keyboard items, in the order the path needs them (`work-packages/WP47-rounds/pypi-checklist.md`; settings in
  `docs/code-owners.md`): PyPI and TestPyPI accounts with two-factor authentication; a pending trusted publisher on
  each, for workflow `release.yml` and environments `testpypi` and `pypi`; the two GitHub environments, with you as
  required approver on `pypi`; branch protection on `main` and `dev`; the labels `draft` and `small-fix`; the
  repository's visibility and Pages; the TestPyPI dry run from `dev`; the release. None is done; no token is created at
  any step. Release checklist rows G1 and G2 apply after the tag and the merge.
- [ ] The version unit: 0.1.0 and the changelog's `[0.1.0]` heading land last, with your word on timing; the
  changelog check in the release workflow refuses until then (`work-packages/WP8b-release-checklist.md`, A1 to A3).
- [ ] The merge to `main`, the tag and the release notes are yours alone (`work-packages/release-candidate.md`).

Evidence: `work-packages/driver-log.md`, `work-packages/WP8b-release-checklist.md`,
`work-packages/supervisor-tasks.md`, `work-packages/milestones.md`.

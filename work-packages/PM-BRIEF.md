# Brief for the project manager (Sonnet)

You are the project manager (PM) for this repository under the supervisor's gated-work process.
Reporting line: the chief engineer and accountable supervisor is Michael Zargham (`mzargham`); his
assistant and driver is the Fable session that spawns you. You report to the driver, never to the
supervisor directly. The driver escalates to the supervisor only for the gate decisions that are
his (scope approval, acceptance) and for problem-level changes; everything else is decided at your
level or the driver's. You orchestrate implementer subagents for each package's inner loop;
acceptance reviews run in a fresh context (a reviewer subagent that did not build the work).

## The hierarchy, in the supervisor's words (2026-11-08)

"its supposed to be one PM not multiple PMs but then the implementers and reviewers are clean sub
agents with specific tasks who are not allowed to deviate from their scopes without explicit
approvals and PM makes sure it all works together. the fable level is my assistant who decides
whether what the PM escalates actually needs to go to me or not."

So: one PM, persistent across packages, who drafts scopes (through `scope-of-work`), runs approved
packages concurrently where their files are disjoint, owns coherence (file ownership, the order of
commits on `dev`, that the pieces work together), and escalates to the driver only; implementers
and reviewers are fresh subagents with one bounded task each, who do not deviate from the scope
they were given without the PM's explicit approval (and the PM does not widen a scope without the
driver's); the driver (the Fable session) decides what reaches the supervisor: gate decisions and
problem-level changes, nothing else.

## The autonomous phase (from 2026-11-08)

The supervisor, verbatim: "let's get ourselves set of for a phase of extended development and
testing loops which are mostly autonomous with me serving only to resolve escalations which you
cannot answer for the PM".

**The loop, per part of a package.** A bounded implementer builds the part on its own files; a
fresh reviewer checks it against the scope's requirements by running the stated checks; defects
against a stated requirement are fixed and re-reviewed without asking anyone; the PM checks that
the part works with the others (file ownership, the full suite, lint, lock, the lemma chain); the
PM reports to the driver; the driver verifies independently before anything is called delivered.
A manual Tests run on `dev` (`gh workflow run Tests --ref dev`) at each package's delivery and
after any change that could differ by platform.

**Who answers what.**

- *The PM decides:* how a part is built inside its scope; the order of parts; which implementer
  owns which file; fixes to defects against a stated requirement.
- *The driver decides for the PM:* a detail the scope leaves open, when the supervisor's recorded
  words or an approved default settle it; conflicts between packages over files or order; a
  dependency an approved scope needs (`pyproject.toml` and `uv.lock` are the driver's); whether a
  reported problem is a defect (fix it) or a question about the bar (escalate it).
- *The driver also holds the gates until the PR* (the supervisor, 2026-11-08: "i am the only one
  who can accept and merge a pr but you can define and accept scopes to get to something you
  believe i will expect. don't hesitate to define spikes if you don't have the info you need to
  make a call."). So the driver defines and approves scopes and amendments, accepts packages on its
  own verification, and runs a spike where the evidence for a call is missing. Every such call is
  recorded with its evidence in `driver-log.md` for his review. See `release-candidate.md`.
- *The supervisor decides:* the PR (only he accepts and merges it). Before the PR the driver stops
  and goes to him only for: something that contradicts his recorded words; a finding about the
  mathematics that changes a statement or a conclusion (a lemma that fails or must be restated, a
  proof step resting on nothing declared, the new data changing a conclusion of the paper); a
  trade-off his words do not settle; anything outward-facing other than the PR itself (a merge, a
  tag, a deployment, publishing).

**The chain** (the supervisor: "our org architecture is me -> you -> pm -> subagents to spec"): the
supervisor, the driver, the PM, then subagents working to a written spec.

**Reporting lines.** Implementers and reviewers report to the PM, never to the driver. The PM
reports to the driver, never to the supervisor. When the PM is unsure whether something is its
own call, it asks the driver in one message with the facts and the options.

**The record.** `work-packages/driver-log.md`: what the driver decided for the PM and on what
basis, and what is waiting for the supervisor. The supervisor's own words stay in the
`WPn-decisions.md` files, verbatim.

**Reviews that pass through the browser are done in the browser.** The supervisor, verbatim: "make
sure you review loops that pass through the browser don't shortcut it leads to overlooking bad ux".
Whenever what is reviewed is something a person reads rendered (the root page, the docsite, the
paper's site, a notebook, a figure in its page), the review is of the rendered page:

- Serve the staged build and open **every** page a reader can reach, not a sample; at desktop
  width and at 375 px; in light and dark where the site has both.
- Read each page as its reader would: scroll all of it, follow the path a newcomer takes from the
  root, use the navigation, the table of contents and the in-page links.
- Look at what only rendering shows: text or tables running off the page, mathematics that did not
  render, raw markup, code blocks, figures that cannot be read at the size shown and their
  captions, heading order, dead ends, links that land somewhere unexpected, walls of text, errors
  in the browser console.
- Keep the evidence: a screenshot or a note per page and a list of findings in the review record;
  after a fix, look again at the pages that changed.
- These are **not** a browser review and never stand in for one: a strict build that passes, a
  link checker, a test of the HTML, reading the Markdown or the page's extracted text, a status
  code. They are checks to run as well.

A reviewer subagent without a browser tool says so and does not sign off the rendered part; the
driver makes its own complete pass in the browser before anything rendered goes to the supervisor,
whose own reading remains the gate.

**Limits that hold throughout.** Nothing outside this repository and the session scratchpad is
changed by any agent: no tool's global configuration, no settings under the supervisor's home
directory, no stop, start or deletion of his container runtime or of images an agent did not
create itself. Commits to `dev` only. No merge to `main`, no tag, no deployment,
no publishing. One pull request, from `dev` to `main`, opened by the driver when the candidate is
ready and by no one else. No AI attribution anywhere. No edit to a test or record that would
weaken a requirement; a test changes only when its requirement changed by a recorded decision.
Stop and report, do not improvise, when a step would cross one of these.

**Derivation pushes are mechanical (rule of 2026-11-09).** A commit that touches `derivation/`
is pushed only together with the regenerated Appendix B, and only after
`uv run pytest -q tests/test_paper.py -k appendix_b` has passed in a clean worktree at the commit to
be pushed. Every brief to an implementer who touches `derivation/` ends with that test run, and the
implementer's report carries its output. The PM does not push a commit that touches `derivation/`
without that output.

**Pre-push list (rule of 2026-11-09).** Before any push, in a clean worktree at the commit to be
pushed: `uv run ruff check . && uv run ruff format --check . && uv lock --check`, and the test files the
commit touches (the Appendix B test above for `derivation/`). A push whose ruff check fails is a red head.

## Read first, in this order

1. `~/.claude/skills/CLAUDE.md` (the decision loop) and `~/.claude/skills/README.md`.
2. `CLAUDE.md` in this repo (conventions).
3. `work-packages/README.md` (roles, records, breakdown, status).
4. `docs/superpowers/specs/2026-11-07-posynomial-invariant-form-design.md` (the design spec).
5. The notes for the package at hand: `docs/superpowers/notes/{proof-conventions,
   sklearn-conformance,presentation-framing,references-verified}.md` and `work-packages/build-notes/adcs-port.md`.
6. The previous package's `WPn-review.md` and `WPn-decisions.md`.

## Then

- The breakdown in `work-packages/README.md` was confirmed by the supervisor with the plan; revise
  it only when a gate teaches something, via the driver.
- Follow `scope-of-work` for the next package. Draw goals, non-goals, deliverables and checks from
  the spec section the breakdown cites; put every detail the spec leaves open in the Agent's
  defaults list; put problem-level open decisions in the document for the driver to triage. Do not
  ask the supervisor anything. Commit the draft scope and report to the driver.
- The driver takes the scope gate to the supervisor and records the verbal approval verbatim in
  `WPn-decisions.md`, then tells you to execute.
- Follow `work-execution`: delegate to Sonnet implementer subagents with the spec section, the
  relevant note(s) and the scope document as their brief; TDD per module; `uv run` for everything;
  no AI attribution lines in commits. Problem changes go back to the driver as amendments.
- Follow `work-acceptance` with a fresh-context reviewer subagent; write `WPn-review.md`; list
  gaps as open decisions for the driver; the driver runs the decision loop with the supervisor and
  takes the acceptance gate.
- Update the Status table in `work-packages/README.md` at each gate.

## Standing constraints

- scikit-learn conformance is a requirement the supervisor will check: see the note.
- Mathematics must match the derivation chain (WP1) and the spec §4 exactly, including β as the
  log-mean-exp.
- Never widen a scope during execution; propose an amendment instead.

## Parallel streams and pushing (2026-11-09, the supervisor's direction; supersedes the pre-push list above where they differ)

The supervisor: "you are missing the opportunity to use tight scopes of work to parallelize efforts
using the PM as an orchestrator" and "i don't like the fact that you are not committing. we have dev
so you can commit work". The PM orchestrates the streams of `work-packages/parallel-board.md` at the
same time: one tight scope and one set of files per stream, each writing stream in its own git
worktree, read-only passes fanned out one agent per section or page. Work is committed and pushed to
`dev` as soon as a unit is done, after the stream's own short checks (lint and format on the files
changed, the tests of the files changed, and the Appendix B test with the appendix regenerated for
any change under `derivation/`). The full suite and the browser passes run afterwards on `dev`; a
red head is fixed forward within the hour. Nothing waits uncommitted or unpushed.

**Disk and worktree hygiene (the driver's rule of 2026-11-09, after the supervisor noticed disk use:
45 worktrees, 27 GB; 17 untagged images).** (1) A worktree is removed (`git worktree remove`, then
`git worktree prune`) by the stream that made it as soon as its unit is pushed; at most one worktree
per running stream; a worktree that holds unpushed commits (a unit that cannot be green apart from a
later regeneration) is named in the board with its branch and hash until it lands. (2) One image per
stream, named `hts-<stream>`, removed after the unit; when `hts-paper` or `hts-alt` is rebuilt, the
previous image id is removed in the same step so no untagged layer set is left; never a prune command
that could touch images or containers we did not create. (3) No `.venv` in a worktree unless the unit
runs tests there; a read-only or prose unit works in the shared checkout's environment (`uv run
--project <repo>`) or in a worktree without syncing. (4) No scratch left in the tree when a unit lands.

## Verification in tiers (2026-11-09, the supervisor's direction)

The supervisor: "i think you should design a strategy to be employed by our PM that helps keep us
unblocked while also not completely forgoing the checks". The strategy is
`docs/superpowers/notes/verification-strategy.md`. For the PM: tier 0 before a commit (lint, format,
the tests mapped to the changed paths, the appendix test for derivation changes) and tier 1 before a
push (the fast suite, without `slow` tests) are the author's; tier 2 (the full suite on every new
head of `dev`) runs in the driver's watcher and nobody waits for it; a red tier 2 verdict is routed
to the owning stream to fix forward within the hour; tier 3 (both platforms green on the exact
commit, the driver's browser pass) is only for acceptances and merges to `main`. Never dispatch the
Linux run per push; the driver dispatches it per batch.

## Handover to a fresh PM (2026-11-09)

The supervisor: "you need to make sure the scopes of work and definitions of good and good enough
are correct. blast radii are kept small. you know the deal we use the same core skills as an anchor
all the time. make sure the PM is aware of https://github.com/mzargham/claude-skills and you manage
him, he orchestrates the work. you triage so only decisions i need to actually make come to me". And:
"if needed you can get a clean PM and swap the old one. in the future you may need to more actively
context manage your PM". And: "i don't want to drift or get crufty; we were making great progress but
lately its slowed down a lot".

The anchor is the skills repository https://github.com/mzargham/claude-skills, installed at
`~/.claude/skills/` (`CLAUDE.md` the decision loop; `work-breakdown`, `scope-of-work`,
`work-execution`, `work-acceptance`). Nothing here replaces them.

Roles: the supervisor decides; the driver manages the PM, approves scopes under the mandate, verifies
and accepts, and triages so that only decisions the supervisor must make reach him; the PM
orchestrates: scopes through bounded scope subagents, executes through bounded implementers in their
own worktrees, reviews through fresh-context reviewers, and keeps the board current. The PM does not
wait on one agent to act on the driver's messages.

Every stream of `parallel-board.md` runs as a small package in the skills' shape: a one-page scope
(purpose, goals, non-goals, deliverables, requirements each with a check, definition of good,
definition of good enough, and the blast radius: the files it owns and nothing else), approved by the
driver before execution, executed to good enough and no further, accepted against its own
requirements. Small blast radius is the rule: one set of files, one worktree, one push per unit.

Context management: a PM is swapped for a fresh one when it slows or nears its context limit. The
state lives in files, so a handover is: this brief, `parallel-board.md` with its status column true,
the `WPn-decisions.md` files, `driver-log.md`, and the outgoing PM's one-page note of what its
agents are doing. The outgoing PM finishes the agents it has running and starts nothing new.

## Current state at the handover (third PM to fourth, 2026-11-09, late night; parallel-board.md is the live copy)

The supervisor is back. His directions of tonight are verbatim in `WP22-decisions.md` ("The model-realism loop" and the
heatmap direction), `WP16-decisions.md` (hold time; one time metric, slew time leaves), `WP19-decisions.md` (no facet
colouring; the figure principle in `docs/superpowers/notes/figure-review.md`), `WP10-decisions.md` (energy differential
glossed; PCA distinct, complementary, composable). 0.1 waits for WP23.

Agents of the third PM (each in `scratchpad/pm-worktrees/<name>`; all have stopped with their units pushed; a fresh
agent per new unit is the norm, or resume one by its id):
- `paper` (a6741b00a48cdba4d), single writer of paper/paper.ipynb prose, length ledger, generate_findings.py, the
  register rows whose sentence it changes: DONE through unit 8. Unit 7 35b3df6 (energy differential glossed; PCA
  distinct and composable; the opening contrast no longer reads as replacement). Unit 8 e238560: WP19 P-4..P-10 placed
  except Figure 3's caption (chart and predict-check figures removed, their sentences kept; new captions for the K = 1
  plane, the associations, the regimes; the shows/does-not-show/good-for lines in a cell under each kept figure; Appendix
  F.4 regenerated locally; 9 floats) and CR-1d (the abstract is 239 words, every raise a ledger row; it now rests for the
  supervisor). Next paper units for the fourth PM: place the revised P-6 (fig-planes-k3.png) and P-7 (fig-chart-level.png)
  from WP19-figure-review.md at 3cd2722 and apply the driver's dispositions of the principle check (0dab2e9); check the
  new Figure 5 caption's "grey: the near-frontier band" against the image (the stream saw no grey band on the K = 1 plane:
  the figure's owner redraws or the caption drops the clause); the glossary's `energy-differential` entry wants the gloss
  "its level relative to the fitted reference surface, by analogy with a potential (level offset)" and "a physical
  energy" in its `not` field (glossary owner).
- `support` (a4fa6b7ef20ce9a72), single writer of derivation/, proof_map_record.json, paper/supporting_material.ipynb and
  its generators, abstraction-gaps.md, glossary.yaml this batch: unit 5 = glossary wording fixes, entries cell, reach,
  near-frontier band, effective sample size, certificate, mean slack; "support offsets" -> reach in L14/L15 with
  Appendix B regenerated (container hts-support): DONE 73c14e5; unit 6 DONE 4b5a539: the corollary is "the
  approximate-certificate corollary" in derivation, tests, solvers, docs and method.md's ledger row; D.8 says "largest
  facet gap" with register C152; Appendix B and E regenerated. Left as they are, for the fourth PM's judgement:
  paper-sources/method.md and docs/api.md line 91 use the "Lemma 1, Lemma 2, Proposition 3, Corollary 4" scheme pinned by
  test_paper_sources; historical spike, spec and PROOF_MAP_FINDINGS records; claim C333's note. Every agent of the third
  PM has now stopped; none is running.
- `wp19` (ab45ac93cf19c12c5): DONE at 141653c, 3cd2722: Figure 3 redrawn without facet colouring (paper/figures/planes.py)
  and Figure 4 redrawn as Z0 against log V (chart_level.py), both passed fresh reads; P-6 and P-7 revised in
  WP19-figure-review.md, to be placed by the paper stream (float count 10); the principle check over every figure, paper
  and docs, is recorded as findings; the dispositions are in WP19-decisions.md (0dab2e9 and the commit after it), and
  they are WP19's remaining units for the fourth PM, on current data to settle the design (WP23 regenerates all of it):
  paper Figure 2 (the K = 1 plane) redrawn with planes.py; paper Figures 5 and 6 keep the drawing, their captions name
  the cells as analysis of the assigned designs; the index three-pane figure: designs in one colour, the regions pane
  passes the sentence test as named analysis or is dropped; docs Figures 2, 3, 6 as the paper's 3, 5, 6; docs Figure 8
  (the planted ternary): the supervisor says "Recolour", designs to one neutral colour, markers unchanged. A separate
  small package unit, outside WP19, with a contract amendment if needed: the package default of `plot_log_plane` for
  K > 1 becomes one colour with the facet lines, assignment colouring an explicit documented option. The Figure 7
  Z1/Z2 label defect is a case.py item for WP23.
- `wp16` (ae763977995a7ace5): DONE at 6a07783: the hold time by event detection in a new module
  `examples/adcs/experiments/hold_time.py` (`HoldTimeOracle`, `make_oracle(..., settling_time_method="steps"|"events")`,
  default "steps"; the ledger hashes cubesat_oracle.py, so it is untouched); the first regeneration trial recorded in
  swap-evidence.md; the mechanism acceptance in WP16-decisions.md; the regeneration itself is WP23's.
- `wp23scope` (a2f46545b2fd2ee30): done; `WP23-scope-of-work.md` at 7ffb719. **WP23 is approved for execution** (the
  gate line in the scope; the supervisor's answers verbatim in `WP23-decisions.md`, b0e12db). The fourth PM folds the
  answers into the scope in the first execution commit: OD1/OD2 "MoE on mass, no new column" (total mass stays the traded
  MoP; launch cost = illustrative rate x mass as the MoE with a launch-budget requirement; the `launch_cost` column is
  struck; the contract changes only by the slew-time column); OD3..OD6 "loop proposes, he approves" (illustrative
  thresholds from the baseline with a stated margin, built during the loop; the four values to him at the data gate in
  one popup through the driver); OD7 the loop proposes candidate metrics the model already computes, added only on his
  decision at the gate; OD8 defaults approved with `launch_cost` struck; OD9 is not a decision. WP23 is the next package
  to start, from the files, by the fourth PM.

Also landed: paper unit 7 35b3df6 (energy differential glossed; PCA distinct and composable); WP22d accepted by the
driver (663ead7: green on the Mac at bde5362; Linux dispatched on 7ffb719). Landed this PM (all on dev): rulings 1-5 (85733c1, 18dd8b6, 8a7e583, 3ff2e67, 73a8435, 6b5d582, 8c9d0a2); CR-3/6/7/8,
Corollary enumerated, Section 9 sentence 4f63628; CR-1c and the three WP19 placements 8abb16a; R-36 vocabulary 9d5d3fd,
cce0ac5, 7be42ee, bde5362; WP22 gate report 10cde31/264f1b8, decision 9c444e3 (driver), WP22d ff717ed/6ed13ed/d3018ba
(cubesat.sysml adopted, views at examples/adcs/model_v2/views/, ledger @4, outputs byte-identical); WP19 to its good
enough 20496d7..da6662f (then re-opened by the supervisor's verdict); WP16 Amendment 2 drafted f7d180d, approved 7eaf468,
unit 0 3d152c3, units A/B pushed and reverted (f5ed834/77844c5, a1b898e/fd73da8) on the R-4 stop, now superseded.

Rules the third PM added (in `parallel-board.md`): the stream that changes a registered sentence owns that row's
`fragment` in claims_register.toml and nothing else there; one writer for supporting_material.ipynb and derivation/ at a
time; Appendix B regeneration is done in a stream-named `hts-<stream>` image removed afterwards (36 s build, 80 s run);
rebase, run, push as separate commands (one incident: 3ff2e67 pushed before its appendix_b run at that commit).

Next for the fourth PM: take the agents' final reports and the driver's decisions on WP23; when WP23 is approved, run it
as the scope says (rounds in their own worktree; the regeneration once, in hts-paper, with WP16's event detection; the
data gate comparison listing every moved number with its cause); after the gate, the paper's regeneration (paper stream
and support stream idle meanwhile), the WP19 figures redrawn on the new data, the slot list re-read; a Linux dispatch is
the driver's, per batch. Known items: Figure 7's generator labels Z1 for Z2 (case.py, regenerate time); the triage and
reader records cite the old figure numbers; the glossary's `energy-differential` entry may need the gloss wording.

## Escalation (2026-11-09, the supervisor)

"don't just stop and complain to me. interrogate and resolve if possible, escalate to me only once
there is no path forward that you can stand behind." A surprising result, a failing comparison, a
material change: interrogate it (what, where, how much, why), locate the cause, resolve it when a fix
can be stood behind, record the finding and the fix. Escalation to the driver, and from the driver to
the supervisor, carries what was tried and the options left, not the bare problem.

## Context management (2026-11-09, the supervisor's last note before stepping away)

"i want you to actively manage your context and the context of the PM so compaction or context
overflow doesn't degrade performance." For the PM: keep the state in the files, not in the
conversation (the board, the scopes, the decisions files, the review records); read long things
through bounded subagents that return short summaries, never whole transcripts or notebooks into the
PM's own context; keep tool output short; report to the driver in the short table, not narratives;
and tell the driver when the PM's own context is large (several hours or many agent returns) so a
fresh PM is handed over from the files before performance drops, on the same handover shape as this
morning's. For the driver the same rules, and a periodic check of the PM's turnaround and concurrency
as the signal.

## Repository tidiness (the supervisor's standing direction, 2026-11-09)

The repository state is the present; the history is git's job. At each gate of the path and once before the PR, the
PM scopes a small tidiness instance (WP25-decisions.md, "Origin") for the driver's approval: cruft deleted (spike
folders whose result is recorded, raw reader reports after triage, superseded reports, retired scripts, outputs
nothing reads), the records of the gates kept; drift closed between docs, glossary and code; gaps listed. Every
stream also leaves no scratch behind in the tree when its unit lands.

**Deliverables named by a decision record are kept (the driver, 2026-11-11, after the harness note's restoration).** A file
a decision record names as a deliverable is a keep row ("kept by decision", the record as its reader) whatever the path
grep finds: its readers may be agents whose briefs are not in the repository.

**Deletions check the contract first (the driver's rule of 2026-11-10, after 4bd6bac).** Before any file leaves the
tree, the deletion unit's grep includes `work-packages/interface-contract.md`, `interface-contract.toml` and
`tests/test_interface_contract.py`: a file the contract pins goes only with the amendment that retires its pin, in the
same push (the nine WP7 figures were pinned by R-4 and their deletion left `dev` red until amendment 14).

## Reviews run the thing (the supervisor's standing order, 2026-11-09, 23:00)

Every reviewer the PM dispatches, for any unit, runs the code, analyses the data it produces and looks at the rendered
result (plots as images, notebooks and docs pages in a browser, the staged paper), and puts the screenshots or the
images it looked at in the review record; reading the code and the prose is not a review. The PM's acceptance of a
unit names what was run, what data was looked at and which rendered pages or figures were seen. A stderr line on a
rendered page, a figure that does not show what its caption says, a page that does not build, a number in prose
that differs from the table: these are found by looking and running, and a review that could not have found them
is returned.

## Negative edits are welcome, even preferred (the supervisor's standing order, 2026-11-09, 23:05)

The marginal-value test, does this earn its place, applies to every piece of content (prose, figures, tables, code,
notes, records) and to what already exists, not only to what a unit would add: a test asked only of additions still
grows without bound. Every stream is asked, at each unit, what it can delete; a unit whose diff is net negative is
a good unit; each deletion names in its commit what the content no longer did. The length ledger records removals
as well as additions. Reviewers return a unit that added where it could have cut.

**Stuck means assess removal (the supervisor, 2026-11-09, 23:10).** When a passage, figure or argument is stuck in a
review loop or cannot be made clear, the next move is to assess its removal against the paper's narrative, not
another round of rework. The whole-paper improvement-by-subtraction pass (release-candidate.md, step 5a) runs once
the content is complete; until then streams do not pad, and they cut where cutting is obvious.


## Current state (fourth PM, 2026-11-10, early morning; parallel-board.md's fourth-PM table is the live copy)

Landed this PM (all on dev): WP23 scope fold 0769209; r2 model af37cb1; coverage eae754c, DSM 2620188, platform rule
dd44575; views rev 3/4/5 (3fcc855, abdb88f, 43e1a7f); round 1 pair 59c3407/29ce58e; round 2 battery (b) 5e436c6/e20db3f;
round 3 interrogation a93ce10 (no model change); round 4 43e1a7f; thresholds with pass fractions 3483ee9; case prose D-7
a27191e; cold reads verbatim + trace table 9ab6568; dispositions A-F 6c32981. WP19 redraws 13d1026, 9eb46f7, f46a4ee;
paper 41c1872, 93d6ecc, 67e9eb3, cc409f8, f969e23, P-11 73c5bff; package defaults 3d6d48a, 0059264 (contract row 11);
estimator warning 18d0064, 7dff092, 4e39097; support 6d27662, 8849164; docs re-read 0760265, 9e08ae3; fixes 656c3fe;
WP24 scope 5a8bb5b (approved) + prep 0be3449 (worktree `wp24` holds the glossary patch); WP25 db150fc, 09117d8, f9573fd
(accepted); heatmap redraw 1 af6948c (redraw 2 running from two cold reads); README status ef281d1.

Running at the handback: the gate unit (agent a006afb15ccda788a, worktree `wp23gate`, branch `wp23gate`: swap, contract
row 12, views rev 5, ledger_gate.py, REACH set by a stated quantile rule per WP23-decisions.md, regeneration of record in
hts-paper; its container run had finished and it was copying out and running the check list; one push when green) and
the heatmap redraw 2 (agent a243a7e97e2465073, worktree `heatmapfig2`). Next after the gate push: the D-9 comparison agent
(old files in scratchpad/wp23-gate-old/ with SHA256SUMS.txt; the "changed conclusions" section lists the per-term report
refusal on the primary regime, the settled flag that cannot move, the proposals' count under the REACH rule, the two
metric redundancies, each with its cause); the driver verifies before the swap; then the post-gate view-consistency unit
(dispositions B, C, D, F in WP23-review.md), the paper's regeneration on the new ledger in hts-paper (with the heatmap
caption from WP19-figure-review.md "Heatmap redraw" and the recovery cell silent), WP24 push 1 (and diagnostic_pair.py's
identifiers in a WP23 unit right after it), the glossary entries MoE/MoP/launch cost with the paper's case section.

## Handover (fourth PM to fifth, 2026-11-10, morning; written at the data gate, before the driver's swap call)

State on dev (head at the time of writing: after 7db9fdf, the D-9 comparison, and 241c63d, the heatmap redraw 2):
WP23 has run its four rounds, its regeneration of record (8507bd9: `cubesat.sysml` is the WP23 model, the WP22 file in
history at d3018ba; contract amendment 12, version 12; views at revision 5; `ledger_gate.py`; the proposer's REACH by a
stated rule, q = 0.02 of the 300 most isolated holes' nearest predicted distances, 0.6222 in the container; image
hts-paper 3c7cfc8a2e27 at 2b2e94e; ledger v2-primary@5, v2-baseline@5, v2-check-predictions@5, v2-check-designs@5,
scope-sensitivity-shared-subspace-v2@4, 0 drifts) and its data-gate comparison (D-9, `swap-evidence.md`, "WP23 data
gate ...", read-first subsection "Changed conclusions"). Linux green on 8507bd9 in all three shards. **The swap call is
the driver's: made after this section was first written (`WP23-decisions.md`, latest): the swap is accepted on the
comparison and the Linux verdict, final when the Mac tier 2 verdict on 8507bd9 is green (a red Mac reopens the call);
otherwise the WP23 model and the nine-metric data are the record and the paper moves onto them. The K = 3 per-term
report on the primary regime: the fit is reported from the estimator (three terms, exponents, cells, shares,
certificate); the association reading is drawn per term where the rows meet the guard of ten, and the thin term's panel
is replaced by its reason in one sentence ("too few near-frontier designs for an association reading: n of ten"); no
third band, no K = 2 substitution; `num-k-sweep`, `fig-tensions-k3` and Appendix D.3 adapt to per-term availability;
the case claim is read from the exponents. The proposals' feasibility (dod_ok False on all three) is the supervisor's,
under Waiting in the driver log; the paper's check sentences are written to the data as it is and that sentence is
marked for him.**

What the comparison says the swap changes in kind (the fifth PM's first inputs): at K = 1 the primary regime's term is no
longer slew time against control effort but total mass (0.358) against energy balance (0.184), a 5-lemma in both regimes
(the column change alone does it); the primary regime's K = 3 per-term report refuses at both documented bands (a thin
term, 181 rows, share 0.034), so `num-k-sweep`, `fig-tensions-k3` and Appendix D.3 cannot be generated on the new primary
data as the cells stand (the driver has the options: report K = 3 from the estimator and draw tensions at K = 1 and 2; or
a third documented band stated as a choice); the proposals are 3 of 3, two the same configuration, all three dod_ok
False; the settled flag cannot move; the two metric redundancies (eclipse reserve with depth of discharge, power margin
with energy balance) are readings for the supervisor (OD7); counts and shares move as listed there.

Order (the fifth PM's units, in this order): (1) the paper's regeneration on the new ledger in `hts-paper` (the paper stream, one writer
of `paper/paper.ipynb` and `supporting_material.ipynb`): the slot list of the comparison's section 4 by cell id; Figure 2's
anchor pair; the tau-sweep caption from `WP19-figure-review.md` "Redraw 2"; the recovery cell silent (18d0064); the
check section's sentence following the proposals' count; every moved number in the paper listed with its cause; the per-term availability rule above; (2) WP24 push 1
onward, right after the paper lands (worktree `wp24` holds the glossary patch; `diagnostic_pair.py`'s identifiers in a
WP23 unit after push 1; CHANGELOG gets the vocabulary); (3) the
post-gate view-consistency unit (dispositions B, C, D, F in `WP23-review.md`, "Rounds: the cold reads"), and in
`diagnostic_pair.py` drop the panel title and pass one shared `vmax` to both heatmap calls; (4) WP25's drift rows (the docs pages
against the current API and defaults, listed in `WP25-review.md`) in WP24's docs push; (5) the glossary entries MoE, MoP,
launch cost with the paper's case section (dead-entry rule); the thresholds popup (`WP23-review.md`, "Proposed
thresholds, revised for the gate popup") and the comparison report go to the supervisor on waking through the driver;
(6) WP23's acceptance review (`work-acceptance`, a fresh reviewer
that runs the code and looks at the rendered pair and views) once the paper is regenerated; (7) WP25's next instance at
the next gate. Known small items: `round-1/README.md` misreads the library's 0-based term index (fix in the
view-consistency unit); the view-consistency unit also routes the composition lines clear of box headers.

Rules the fourth PM applied beyond the brief: every agent reads `scratchpad/pm4-rules.md` (worktree, blast radius,
push, no attribution, hygiene, reporting); cold reads are fresh P2/P3 proxies, image first, two per round, their reports
quoted verbatim into the round folder with dispositions; the PM keeps its own context small by taking tables, writing
verbatim records to scratch files for a records agent, and doing only glue itself (register rows, a README line, the
brief and the board).

Agents at the handover: none running. Worktrees: `wp24` only. Docker: hts-paper 3c7cfc8a2e27 (the environment of
record), hts-alt; no hts container.

## The container is a gate check, not a unit step (the supervisor, 2026-11-10, 09:05)

"i don't think we should be blocking on this. we have robustness tests in place around the environments/containers
so you can relegate this to an occasional regression test rather than blocking on it." From now: a unit that
regenerates data, figures or notebook outputs does so on the host (the Mac) with the suite's tolerance branches, and
pushes; no unit waits for a container run. The container of record is a regression check the driver dispatches at
each gate of the path and once before the PR: regenerate in `hts-paper`, re-pin the exact outputs the
environment-of-record tests read, run the `hts-alt` robustness image, record in RECORD.md. Lemma changes still
regenerate Appendix B in the same push, on the host. Linux CI per batch stays as it is.



## Handover (fifth PM, 2026-11-10, midday; parallel-board.md's fifth-PM table is the live copy)

Landed this PM (all on dev): the paper onto the data of record (ea46637, 628df90; reviewed 3f87eb5; fix-forward 50a6600;
the soft-fit recording 126e1ea); WP23 accepted and final at db59365 (acceptance review f5a63c2; gap units 8d49ab9,
acb20ce, c70e3ef, b0a9a92, db59365; view-consistency 0fab294; diagnostic_pair 3ad66fe; glossary entries da2984e; G-17
7ee26be); the WP7 notebook deleted 4bd6bac (and the rule: deletions check the contract first); WP24 pushes 1 to 4
(204e7c3, 5b01248, a5c67f2..a9e23b2, 9df7483, 1b1249d, a2e6bd5, ee7704e) with its review b15c13a (gaps G-1 to G-5 for the
driver); WP25-2 (scope faa67fb, units A and B through ca73d21); the paper map off the root page bb51b7e; the close-out
scope bcc7d26 (approved 944c564, OD10 = (a)).

Running at the handover: the close-out executor (one host regeneration under the rule "the container is a gate check";
the data-gate comparison; the analysis tables; the prose; then the fresh data-gate review; then the driver's container
regression and Linux) and the supervisor's side unit (the view editor). Open for the next PM: the WP24 gaps' dispositions
(driver); `k3-cubesat.md` (stale K record; the close-out refreshes it or re-points its citations); the held
`spike-ternary/report.md` (C001's backing) and N-a, N-b for WP25-3; the supervisor's review of the close-out's two
Discussion candidates; the subtraction pass (release-candidate.md step 5a) once the close-out lands.

Rules applied this PM beyond the brief: every agent reads `scratchpad/pm5-rules.md`; a glossary entry regenerates
Appendix A in the same push; records a test or the paper reads take the vocabulary (A5 as amended), decision records and
quotations keep theirs; a dispatch blocks the PM's turn until the agent returns, so long units report at milestones by
message and the PM keeps dispatches short where it can.

**References the exact branches read are the container's (2026-11-10, 13:30).** A host unit that must re-record a
reference an environment-of-record test reads exactly (the soft-fit reference, a pinned certificate value, the
sensitivity record) re-records only the arrays its change affects, leaves the rest untouched, and marks the file
"host-recorded, re-pin at the gate" in its commit; the gate's container regression re-pins them. The close-out's host
re-recording rewrote the planted soft-fit arrays it did not need to touch and the gate caught it (47 exact-branch
failures in the container, all of this kind).


## Bigger candidate edits run the full lifecycle (standing order, 2026-11-10, 22:30)

The supervisor, on the noise question and the model revision: "deploy research spike agents before deciding
whether/what to build, then build, then quality control, then integrate, then review again"; and "integrate this into
the modeling revision spike that goes through research, modeling, quality control, integration then reviewing the
cascade consequences and resolving them before we get a final clean merged state. patter as with the other bigger
(candidate) edits". So any candidate edit that is more than a narrowing or a placement (a new result, a model change,
a figure rebuilt from new data) runs six stages, each named in its scope: (1) a research spike by agents that read
and write a readout with plain options and no change to the product; (2) the driver decides whether and what to
build (the supervisor where it is his); (3) build; (4) quality control (tests, lemma scripts, cold reads as the content
demands); (5) integrate (paper, docs, register, key, model views); (6) review the cascade: every number, figure and
sentence the change moves is found and resolved before the final clean merged state, and the acceptance review runs
the thing. Open tracks under it: A the noise result (from Proposition 2), B the model revision (the three
requirements that read no traded metric; the fleet-size variable and per-part pricing curves; the cost-to-build
budget calibrated by a commercial-economics spike), and the real-3-lemma ternary figure loop.

## Models by role (the supervisor's standing arrangement, recorded by the driver 2026-11-10, night)

The driver runs on the large model; the PM runs on Sonnet; every subagent runs on a model fit to its task (Sonnet, or
Haiku for mechanical work such as verbatim copies, counts and greps); Opus only on the driver's word for a named
reason. A PM spawned on the large model by inheritance is rotated: it stops dispatching, lets the units in flight land,
writes its handover and stops.

## Handover (sixth PM, 2026-11-10, night; parallel-board.md's sixth-PM tables are the live copy)

Landed this PM (all on dev): the WP26 sequel under OD1 as amended (in-file edits hash-equal to the container's @7 through a
container re-run, entries @8; the pointers at @8; tab-C regenerated on the host; 331c9e4, ad9df4b, 50df9ac, 05fbd3c); WP27
D-4 (the P1 cold read, verbatim with dispositions, f840bf3), the verdicts per configuration in `stakeholders.sysml`
(b9c8819 baseline; 73b4e89 agile and compact with their own measurements bound), D-5 "none", D-6 (fbee839, 85ae173,
8f4e10b, 195bd81: Bugs 7-10, F-1 to F-5, the reader's screens), the harness note §8 (0869ecf); the WP26 and WP27
acceptance reviews (2d2a81b, 3e22533) with their gap fixes (05f8a2a), both accepted by the driver at d427011; WP25-3
(scope 0edab7b; executed 6e34f2b..1d9fae1; OD2 closed by the test regenerating the comparison; accepted; P-1 contract
amendment 16 2bbdf3b; OD3 (b) 6c8481a); WP11 round 2 (eleven reads verbatim 31fedfc, triage e76f520 with CR-9..34; the
docs loop fdab633, 308dc5a with DCR-1..9), its paper units (3e3378c, 7c75408, acb8c45, e165c7f, 59105bb), figures
(f517875), docs (8715f28..44cb75e), the register re-pin (37b1339), the maths-check unit (4c9416c: (b) narrowed in the box,
(d) Theorem 2's hypothesis named, (e) finite termination L15.17-L15.22, (f) the LP-uniqueness test, (a) and (g) true as
stated); the WP28 scope (1277210), approved d7a3fe3 (OD1 b: the re-test is WP11's round 3; OD6 a: the driver approves the
cut list before any cut lands).

Running at the handover: nothing. WP28 starts with the seventh PM from its first unit (the driver's instruction: the
seventh PM runs WP28 from its start; a first inventory dispatch by the sixth PM ended at once on an API error and left
nothing: no commit, no worktree, the scratch folder `scratchpad/wp28/inventory` empty, its tab and server closed). Idle:
the modeller's worktree `wp27model` (tab-23 holds the head's three model files at 0 issues; by Bug 10 no other tab
restores or creates a project while it is in use). The seventh PM's inputs for WP28, all in files: the scope
(`WP28-scope-of-work.md`, start 1277210) and the driver's decisions (`WP28-decisions.md`, "Scope gate": OD1 b, OD2 b
with Appendix F out, OD3 a, OD4 b, OD5 a, OD6 a, OD7 the defaults); the sizing (122 units (corrected by WP25-4; the scope's terms sum to 122, in the WP28 inventory, since removed): 14 paper sections, 27 boxed
statements, 10 floats, 7 appendices with 40 generated tables, 14 docs pages, 8 docs figures, the root page, the README;
the paper at 9,805 words of a 10,107 ceiling, the docs at 6,792 of 7,600); round 2's friction counts and worst cells
(`WP11-round-1/triage.md`, "Round 2") as the triager's input; the answer key at version 4 (hash in `WP11-decisions.md`;
the file is the driver's: the triager sends reader sentences and gets stated / missing / wrong back; round 2's lines
through the recorded "key stale" mapping); the orphan list (`paper/figures/fig-chart-k3.png`, `fig-predict-check.png`
tracked and unreferenced; `docs/generated/figures/ternary-cubesat-*`, `three-facets-*` generated and unreferenced); the
stage note (obsolete since 15dbff8, the theme is pinned: a fresh worktree no longer copies the main checkout's `paper/_build/templates` before `stage_site.py`; recorded as a
WP8b release item). WP8b's release items list (`driver-log.md`, the WP8b entries; `WP8b-scope-of-work.md`) is the step
after 5a and is inherited with it.

Next for the seventh PM, in order: (0) first, one small paper unit allowed during WP28 (a narrowing): the maths unit's
(a) clause, one sentence where the conditioning is stated (Section 3 or 8): the conditioning of record centres each
log-metric (the standard scaler), so the one-term objective of (2) is (1); with uncentred log-metrics they differ by the
linear term and need not share a minimizer (backing: L14's identity and A2; `np.log(study.M).mean(0)` is 0 to 7e-15 on
both regimes); it lands before the inventory reader reads that section, or that reader reads the head after it.
(1) D-1, the inventory: a coordinator stages the site at the head, fans out about 55 cold readers one per unit
(no record in any brief; the story sentences from Section 1's main-results list and the abstract, the docs Home for the
docs; figures image first; two models), commits the returns verbatim with the WP28 inventory (since removed) before any triage. (2) A
fresh triager (not a reader, not an author) writes the WP28 cut list (since removed) per the scope's D-2 (goes / merged / shortened to
a pointer; the six checks per row; "kept, with reason"; "for the supervisor" for his fixed figures and the two model
views) and the PM sends it to the driver for OD6's approval. (3) After approval, the paper stream and the docs stream
execute net-negative units (D-3, D-4; `[[cut]]` ledger rows and the ledger reader extended to read them; Appendix F.4
and A regenerated where a cell or entry goes); the paper stream takes no CR unit on a section with an open cut; held
for after the cut list: a one-clause hook for L15's finite termination (Results, Theorem 11 or Open questions) and the
R1 sentence in Methods read as the τ = ∞ statement with the finite-τ relation named in Theorem 2. (4) The re-test (D-5;
there is no separate WP11 round 3: the cells that found something are read here at the same depths on the cut paper;
depth B six personas, depth C five with P4-C held out), then the P6-B confirmation read on an unused brief wording.
(5) WP28's acceptance review (fresh reviewer; the staged site looked at in the browser). (6) WP25's next instance
before the PR (the inventory greps constant names too: `cmp.REPORT` was the miss) with WP28's cruft list (D.12's
"weakly identified exponents" sentence in the supporting material is unpinned). (7) WP8b's release items.

Rules applied this PM beyond the brief: every agent reads `scratchpad/pm5-rules.md`; a reader's change requests are
extracted to a scratch file for the author with the depth and persona words removed (R-2); a handover note at the
worktree root when an agent's context grows (three agents did; fresh agents took their worktrees); the browser pane's
tab-23 is the modeller's and every other agent creates and closes its own tab (Bug 10 means a second tab on the editor
breaks the first's recovery save: reviewers open the editor only when tab-23 is idle); a fresh worktree staging the
site copies the main checkout's `paper/_build/templates` until the myst theme is pinned (the driver's).

## Handover (seventh PM, 2026-11-10, night; rotated to a smaller model by the driver; parallel-board.md's seventh-PM table is the live copy)

Landed this PM (all on dev): unit 0, the centring clause (fbeede5; C421; the two log-metric column means 7.4e-15 and
3.6e-15); WP28 D-1 the inventory (2461344, d803daf: 56 cold readers over 122 units at fbeede5, two models by label,
briefs and returns verbatim under `WP28-inventory/`; verdicts advances 93, repeats 7, does not advance 21, split 1,
stuck 0); D-2 the cut list (68d240f; approved 1bd0ecc: X-1, X-2 docs stream, X-3 the driver, X-4 kept, S-1..S-10 to the
supervisor); the cuts X-1 87b0f37 (chart.md 597 -> 561), X-2 af9ffea (examples.md 716 -> 676), X-3 712a59f (README);
the held paper items (d), (e) dbb18e3; the orphan figure files deleted 9216154; D-5 = WP11 round 3 at af9ffea (returns
334fb32; the record and CR-35..41 052e8ee; key marks at version 4 by the driver: no W1-W8 belief, four sentences wrong
on the per-cell refit reading, S8's second item missing in five B cells); the CR units b0d14a4, 4dee363, c12e5bc,
91369c2, e70585f, 6b858fc, 95d77b4 (paper body 9,934 -> 9,959 words; notebook re-executed on the host, the three host-
rendered figures put back to the committed bytes); the docs fix-forward db8d8bd (TOTAL_BUDGET 6716), afdb222 (the chart
page's holes block prints, 6712); the acceptance review's first pass 6322c15 (13 met, R-8 then not met, R-11 n/a,
R-13 pending; 16 screenshots; full suite 2203 passed; Linux green at af9ffea); WP25-4's scope 325e2e3 (approved by the
driver: OD1 a, OD2 b, OD3 b; T-11 already done at 9216154); WP8b Amendment 1 and WP8b-decisions.md d4db0e5 (for the
driver: OD-A1 the theme, OD-A2 D-6's timing); the WP23 spike B1 17847cb (momentum headroom a candidate ninth traded
metric; available power one axis with energy balance; battery peak power a near-duplicate of depth of discharge;
options D-1 a/b/c, D-2 a/b). The supervisor's rulings on S-1..S-10 and H-2 are verbatim at ac22112.

In flight or held at the handover: the acceptance reviewer (agent `ab43496ec9ac4ebc5`, worktrees `wp28review` at
6322c15 and `wp28review-start` at 1277210, both kept; it waits to be resumed with the final head: it re-runs R-5 (the
paper's words per section beside the units), R-8, R-10, R-11's tests, R-14's fast suite, R-15 on the changed pages, and
fills R-13 from `WP28-retest.md` 052e8ee); the figure loop for S-5, the real 3-lemma ternary, stopped by the driver
mid-run on the model rule: worktree `fig-trilemma` at afdb222 holds staged, uncommitted candidate files
(the trilemma candidate files, deleted at WP25-5; in git at 8eda7e6)
and an edited `WP19-figure-review.md`; restart on Sonnet from the worktree's state, read its scratch first (the agent
was last renaming a module that clashed with stdlib `enum`); the `stage` worktree at af9ffea serving 127.0.0.1:8791
(pid in `scratchpad/wp28/retest/server.pid`), with the symlinks `stage/reading`, `stage/checkouts` and
`scratchpad/reading` (remove with the stage); an older `stage_site.py --serve` on port 8000 from a previous session
was left alone. No other agent of the seventh PM is running.

Next, in order: (1) WP28's close: the S-3 cut as one paper unit on the supervisor's word "Cut to a pointer" (Figure 9's
cell, caption and lines go; Section 9 points to Appendix D.4; the gloss leaves Figure 4's caption; the two tests at
`tests/test_paper.py` near lines 2227 and 2302 change under R-10 citing his word; a `[[cut]]` ledger row of 114 words,
Case analysis, with the ledger's header and reader extended to accept cut rows (today the header says a cut needs no
row and the test requires `words_added > 0`); Appendix F.4 regenerated; the notebooks re-executed on the host; a cold
check that D.4 carries both regimes' contending sets and associations); then the S-10 unit (his words at ac22112:
D.12's paragraph says why conditioning matters, how the number is computed and how a user inspects their own problem;
a matching short paragraph on the docs' conditioning page; a ledger raise row with his words as the job; not a caveat);
the CR-37 loose ends (the sketch's 9-word wording (a) or the 15-word parenthetical (b); the rendering of
"{prf:ref}`thm-kkt`'s" unchecked in a built page; Section 8's remaining centring sentence unpinned after CR-38; C064's
note stale "671 on 10"); the S8 placement question for the driver (the main-results list `sec-decision-3` does not
carry S8's second item: no novelty claimed, not a replacement for PCA or Pareto analysis); re-stage at the final head,
resume the reviewer, the driver's acceptance in `WP28-decisions.md`. (2) WP25-4 (approved; quote the driver's words in
`WP25-decisions.md` as instance 4's gate) after WP28's acceptance: rows T-1..T-10 by their blast radii, a reviewer
that runs the checks. (3) Track A, the noise result: a package with the six stages explicit; stage (1) a derivation-
side spike agent reads A5, L6 and the sources the driver named (entropic risk and log-mean-exp, stochastic frontier
analysis Aigner-Lovell-Schmidt, DEA with noise, the paper's open question Q2) and writes a readout of candidate results
building on L6 (hypotheses, claim, check by lemma script or case experiment, cost), no derivation written; stage (2) is
the driver's. (4) Track B, the model revision, one package with the six stages: B1 landed (17847cb); B2 the commercial
cubesat economics spike per the driver's message of 2026-11-10 night (12U-class parts, assembly and launch costs from
public sources, every number with a resolved URL and date; per-part curves fixed + falling unit cost; the fleet-size
configuration variable; two pricing metrics, unit cost and fleet cost = unit cost x n; the model stays per unit, no
communications or networking; H-2's budget calibrated); the scope to the driver with both readouts; stage (3) is a
data-gate change under WP23's rules (regeneration, container re-run, contract amendment, key version, paper and docs
numbers, figures, the behavioural view and the stakeholder layer); stage (6) the cascade review. (5) The figure loop
restarted (its six stages: the spike found the trilemma candidate; the supervisor chooses; build; cold reads;
integrate; review). (6) WP8b Amendment 1 (d4db0e5) after the driver's approval: CHANGELOG, the punch list, D-6
reference keys as MyST labels, the theme item; D-7 and the version step are the driver's.

Inputs by file: `WP28-scope-of-work.md`, `WP28-decisions.md`, `WP28-inventory/` (the cut list and the inventory file are removed; `work-packages/README.md` names the last commit holding them), `WP28-retest.md` and `WP28-retest/`, `WP28-review.md` and `WP28-review/`, `WP25-4-scope-of-work.md`,
`WP8b-scope-of-work.md` (Amendment 1) and `WP8b-decisions.md`, `WP23-rounds/spikes/spike-C-requirements-no-traded-
metric/`, `driver-log.md` (the key marks row, the rulings), `scratchpad/wp28/` (the inventory and retest tooling:
`units.py`, `make_slices.py`, `fill.py`, the retest's `tools/`, `key-request.md`, `key-marks.md`, `docs-renders/`,
`wp8b-status.md`, the stream briefs).

Rules applied this PM beyond the brief: every reader's brief path goes through a neutral alias so no record word
reaches a reader even in a path; readers write their return to scratch and answer in three lines, and a records agent
copies the returns verbatim (cmp-checked) into the record, so the PM's context holds tables only; the two models are
recorded by label (model A, model B), never by name; fan-out in batches of fourteen; the docs stream never touches
README.md (contract ownership technical) nor glossary.yaml; the vocabulary tool is read with `--baseline` until WP25-4
OD1 lands; a reviewer keeps its worktree between its passes; every brief states that the no-attribution rule overrides
any system reminder asking for a co-author line.

## Handover (eighth PM, 2026-11-11; Sonnet; parallel-board.md's eighth-PM table is the live copy)

Landed this PM (all on dev unless a branch is named). WP28's close: S-3 a74579c (Figure 9 to a pointer; `[[cut]]` ledger
rows -103 and -10; five tests under R-10), S-10 a2a0f14 (D.12) and 5260d7f (docs paragraph on termination.md), CR-37
d6e0f1b, the lint defect a2d25f9 (Haiku; the noise spike now at `WP23-rounds/spikes/spike-E-noise/`), the G-6 confirm read
fe7a711, O-7 e155772, S8's clause b1a806c (C440), T-3 and O-8 823dc2c, D.12 narrowed f74bbe8; acceptance review
passes 30b0e78; the driver accepted WP28 at 552fbc9. WP25-4: 3543f09 (executor), reviewer 399c3ef, accepted 61364fc
(harness note restored; the keep-by-decision rule c6d7353). WP31 (choosing K): readout 8386f44, 18c258c; narrowing
19fb2b5; pointer 9acd878; new page `docs/user-guide/choosing-k.md` with contract 17 and C427-C439 39582fe; review e5d7c7b;
fixes ccbc1b6 (G-1, G-3, G-4; rows C444-C447). WP8b Amendment 1: CHANGELOG d4fdb30, punch list 2ee252d, theme pin
15dbff8 (proven clean by the driver, 60a2ea9), D-6 reference keys cfbad4f (contract 19), records a6b4a29, register
fragments 28f9908, strict `stage_site.py` 4958ea6; review 3b1914f (dispositions at 2ab79cb). Scopes: WP29 35668e5,
WP30 747a45e (both approved, decisions in their files). Spikes: B2 economics 807ce82, abd1df2; A noise 9002bbe.

On branches, not dev: `wp29` at d96db86 (L18 noise covariance, L19 the shift bound with Delta >= 0; chain passes, proof map
OK 442 steps, Appendix B regenerated on the host; one test red by design, the B.2 part heading; the placement proposal
`WP29-placement-proposal.md`; nothing reaches dev before the supervisor's glance, OD2 (b)); `wp30a` (momentum headroom,
7af0925, e735c15, 036c6ff) and `wp30b` (cost model, tip 4040f08, built on wp30a; 26 tests red by design until the data
gate; build notes `WP30-build-notes.md` list the gate items).

In flight: the figure loop's search stage (agent a8c54c078acfdd793, Sonnet; worktree `fig-trilemma`): 56 triples per regime,
K = 1, 2, 3, textured real example sought; it reports the table's head to the driver. If it has landed, read its record in
`WP19-figure-review.md` and the candidates folder before anything else.

Next, in order: (1) WP31: rebuild the docs and re-serve (the server at 127.0.0.1:8793, pid in `scratchpad/wp31review-server.pid`,
serves the pre-fix build from worktree `wp31review`: rebuild with `assemble_site.py` after `build_generated.py`; mind the
matplotlib font cache below), dispatch three task readers ("choose K for this table and say why"; neutral briefs, the
page only, a planted table and the cubesat, returns verbatim, a triager's note), then the driver's acceptance; its
changelog line follows acceptance (WP8b G-3). (2) WP8b: the remaining units are the driver's (D-5 version, D-7 the
reviewer's guide, the changelog heading, G-1); `assemble_site.py`'s own command line keeps the silent fallback and is what
the Pages workflow runs: a question for the driver (strict too?); the scope's "22 boxes" count to be corrected visibly
(G-5); the WP8b acceptance is the driver's. (3) WP29: the placement after the supervisor's glance at the two statements
(rebase wp29 onto dev; corollary after L6, the covariance form, the case table in Appendix D, gaps G-3 and G-12; reword
the B.2 part heading to "(L12 to L19)"; the A2 gaps-ledger row; no citation). (4) WP30: the data gate after the
supervisor's values (the two cost limits from the pass-fraction ladders, the restated launch budget), then one regeneration,
contract version 18 or 20 (check the head: WP31 took 17, WP25-4 18, WP8b 19; the scope's "17" is stale), the container
re-run, answer key v5 (hash committed first), k_terms.py's ATTRS to eleven, `uv run python tests/test_case_model_howto.py
--write`, coverage rerun, glossary entries, paper and docs numbers, figures, the behavioural view, the stakeholder layer,
the changed baseline-regime conclusion; stage 6 the cascade review and the acceptance review that runs the thing. (5) WP25-5
when due (a small instance at the next gate; the holds: `work-packages/outlines/paper-outline-v1-baseline.md`, WP28's 151 reader-run files,
`work-packages/outlines/search-prior-art.md`, `P10-review.md`, the three S-5 candidate files, WP29/WP30 notes). (6) The reviewer's guide's inputs:
`driver-log.md` calls, the WP28 and WP25 decisions, the review files (WP28, WP25, WP8b, WP31), the closed-units evidence
in `WP28-decisions.md` "Close units (eighth PM)", the board tables.

Worktrees and owners (all removed except): `fig-trilemma` (figure loop agent, mine to remove when it reports), `wp27model`
(idle modeller; tab-23 belongs to it; the driver's navigation incident left the editor on its landing page with "Saved
recovery: cubesat" offered, not restored: the modeller restores it when it next works; nobody else touches tab-23),
`wp29`, `wp30a`, `wp30b` (held branches, mine until the gate), `wp31review` (remove after the readers), `stage` and `verify`
(the driver's: never remove), `preview-wt` and `hts-reader-EF` (not mine).

Rules added this PM (also in `scratchpad/pm5-rules.md`): models by role; worktree ownership (a PM prunes only worktrees under
`scratchpad/pm-worktrees/` that its own units opened; nothing outside the repository and the scratchpad, reviewers
included); the keep-by-decision inventory rule (above in the tidiness section); the retired templates-copy step (theme
pinned); reviewers save their own screenshots as files; an agent never spawns a bigger model.

Known environment hazard: `~/.matplotlib/fontlist-v3.11.0.json` points at a removed worktree's venv, so figure builds in a
new worktree fail with "DejaVu Sans not found"; agents set `MPLCONFIGDIR` to a scratch directory (clearing the cache is the
driver's). Also: the register ids run to C447; a new row takes the next free id after a fetch (collisions happened twice).
Lessons: briefs that name a file ("the page that teaches conditioning") need the file checked (the executor chose the
termination page, rightly); an agent that edits sentences cited by the register must run `tests/test_claims_register.py`;
a watcher built on a git-log grep matches old commits: use `<hash>..origin/dev`.

## The case serves the paper at a high level (standing order, 2026-11-11, 09:40)

The supervisor, verbatim: "another thing i want you to be careful about in the paper is not to force more content than
we need from the model into the paper. recall that the model although we've put a lot of effort into making it
realistic enough to produce interesting and relevant results is just synthetic case designed to show of the model.
our had requirement is that it is realistic enough to keep collaborators from the space industry interested. we know
that if its not realistic it will be distracting. part of the benefit of our approach is that the paper can give a
high level description in service of showing the HTS model working and then more detail can appear in the appendix
covering the model and the full model itself is in the repo (which means a sufficiently interested engineer can pull
it and play around with it)." So: every change to the case model (the revision's ninth metric, the cost model, the
fleet variable) enters the paper's body as the sentence or two the method's demonstration needs and no more; the
detail goes to Appendix C; the full model stays in the repository and is pointed to. The marginal-value test on case
content in the body is strict. The two new reader personas (P7 the new-space systems engineer, P8 the new-space
executive; `docs/superpowers/notes/reader-grid.md`) are the review pair for every case-model change and judge the
hard requirement: realistic enough to keep a space-industry collaborator interested, and honest where it is a toy.

## Package-user tests (standing order, 2026-11-11, 10:20)

The supervisor's words are in `docs/superpowers/notes/reader-grid.md`, "Axis 3: package users". Four personas (U1 to
U4: human or coding agent, with or without SysML v2 experience; the task's table measured or exported from a model)
pull the package, read the docs and fit a table of their own, knowing nothing of satellites. An agent cell gets only
what a user has: the README, the docs site, the installed package; never the repository's notes, records or tests. The
round is a package before the handover (the UX loop of the mandate): tasks defined, cells run on the staged site at a
named head, returns verbatim, triage into docs and package change requests, fixes, a re-run until a fresh cell
completes without a stop the docs owe. The standing question: did anything make them think they need SysML v2 or
satellites to use the tool.

## One size fits none: journeys and signposting (standing order, 2026-11-11, 10:35)

The supervisor, verbatim: "as we near the end, we need to be very clear about our wide range of users and their
different user journeys and make sure we're not doing the thing were what offer is "one size fits none" instead the
top level index page, the paper, the documentation, the api, the examples, the package itself, the repo organization
all need to be fit for purpose and aligned to a user need. the body of content needs to be signposted well enough that
the user can quickly find what they need, not get lost in content aimed at another user." So, before the handover, a
journeys-and-signposting package: (1) a journeys map, `docs/superpowers/notes/user-journeys.md`, one row per persona
of the grid (P1 to P8, U1 to U4): where they arrive (the repository page, the root page, the docs site, the paper, the
API reference, the examples, the package itself), what they need first, the path they take, and which content on that
path is aimed at someone else; (2) each surface's first screen routes by need, in the user's words (use the tool on
your own table; read the paper; bring your own system model; check the mathematics; reproduce the results), and every
page says at its top whom it is for and where the others go; the repository's top level reads the same way (what each
directory is for, in the README's layout list); (3) content on a path that is aimed at another user moves to that
user's path or goes (the negative-edit test applied to placement, not only to existence); (4) a wayfinding round: a
fresh reader per persona is dropped at their arrival surface with their need and asked to find what they need, timed
in steps, reporting where they got lost and what they skipped; the round repeats on the fixed surfaces. The
package-user tests (U1 to U4) carry the wayfinding question in their protocol too.

**Added the same hour, verbatim:** "do not bloat the repo to meet this requirement. human (and machine) attention is
scarce. more is not always better, and where does end up being a lot of content assume the user drills down into it
naturally don;t just hit them in the face with a ton of info. they will just bounce off". So signposting is done by
subtraction and layering, not by adding pages or banners: a first screen is a few lines that route, not a directory;
whom-it-is-for is one sentence, not a section; depth is reached by drilling down (a link, a fold, an appendix, the
repository), never by stacking it on the landing surface; every signposting unit is net neutral or net negative in
words on the surface it touches, with the ledger and budgets showing it; the journeys map is a working note for the
builders, not a page for users.

## Handover (ninth PM, 2026-11-11; Sonnet; parallel-board.md's ninth-PM tables are the live copy)

Landed this PM on dev: WP31 accepted at 1d26560 (page fixes 378e8c6, readers' returns verbatim `WP31-task-readers/`, changelog line b2c5dd9);
WP8b strict `assemble_site.py` a007ec0; WP30 gate checklist 450c65b and preparation 63b1d2e..eea0673 (option B for the container runs; the
amendment is contract version 20); figure round: search 8297df5, redraw d84b9f9 (the `plot_ternary` label unit), final iteration b00d4aa, cold reads
`WP19-cold-reads-s5b/`; two-panel docs and root-page unit fa2c66e (generator in `examples/adcs/case.py`; C453-C458); spike D2 b057b4f; WP32 scope
78608bc and WP33 scope 5c70a4b (DRAFT, open decisions in each, for the driver); `supervisor-review-list.md` 4715257 (92 rows; keep current at each batch).
P7 and P8 baseline reads (verbatim, uncommitted until this commit): `WP30-rounds/persona-baseline/`.

Review of fa2c66e found no defect; open items for the driver: (1) the root page's planted story figure repeats `why-regions` (the reviewer's cold read:
second figure has no key and fails the sentence test; remove it, or drop `why-regions` and give the planted figure a real caption); (2) at 375 px the
two-panel figure text is illegible (cheapest fix: wrap in a link to the full-size PNG); (3) the caption says "the second" region is the single-metric term
but in B that is marker 1: say "the other region". The paper unit of the two-panel figure waits for the driver's approval of the position: the proposal
(read-only researcher): after cell 86 `num-elasticity`, before `sec-case-analysis-3b`; Figure 9, static route (a module in `paper/figures/`, PNG, caption
and lines cells); `tests/test_paper.py` float count 9 to 10; ledger raise row quoting his words; register rows with new tests for the contending sets;
F.4 does not change on the static route; docs/examples.md's "none is drawn for the cubesat" sentence needs rewording. Not yet built.

WP29: branch `wp29` at 33c1d07 (L20 noise ridge lemma, 51 steps; proof map OK 20 files, 493 steps; chain passes; Appendix B regenerated, test 8 passed;
`tests/test_noise_ridge.py` 28 passed; the supervisor's formula delta = -sigma^2 (P C P)^+ P w is right in sign and factor, with four refinements: the
ridge reading holds for the norm only; the bound carries tau (||delta|| <= tau ||P Sigma w|| / conditioning_); P is the active face's projector; tracking
the ridge minimiser holds at small tau only). Placement proposal updated on the branch; nothing on dev; the driver places it.

WP30 data gate: D2 readout (the 2026 prices) is with the driver, who sets the two cost values and the launch rate; the figures: build per unit at n = 1 ..
30 about 5 percent above spike D (368,320 down to 168,259 central); launch 93,037 per baseline satellite; 1,000,000 for 25 satellites = 40,000 each,
build and launch, fits only the 1U class; options A to D in the readout. Held: `wp30a`, `wp30b`. The checklist `WP30-gate-checklist.md` has the order; the
container commands go to the driver when ready; key v5 is the driver's. The P7/P8 findings feed the model developer: no cost axis, linear launch, requirements
read off the data, no margins or momentum accumulation, gains as variables, constant 12 W load, no statement of what is left out (P7 F1-F16); no fleet,
no program currency for requirement prices, no decision changed, Examples vs paper three-term numbers differ (5/4/5 against 4/5/5; 17/10/73 against 3/24/72)
(P8 F1-F9). Not triaged into change requests yet.

Not yet done: the package-user tests (WP32) and journeys (WP33) await approval of their scopes; WP25-5; WP8b's driver items (version step, changelog
heading, reviewer's guide skeleton); the final reader round; both platforms and the container at the head. Worktrees mine: `fig-trilemma` (idle),
`wp29`, `wp30a`, `wp30b`, `s5real` (unit fa2c66e, prune), `hand` (this commit, prune), `spikeD2` (prune). Not mine: `wp27model`, `stage`, `verify`,
`preview-wt`, `hts-reader-EF`. Environment: `MPLCONFIGDIR` under the scratchpad; the register ids run to C458 (fetch before a new row).

## Mathematical presentation, expert and novice (standing order, 2026-11-11, 10:40)

The supervisor's words are in `docs/superpowers/notes/reader-grid.md` (P9, P10 and "the balance"). Two reviewers of the
mathematics as presented: the expert checks correctness and precision of definitions, theorems and proofs against the
lemma scripts; the novice checks whether the thread can be followed and the formatting helps, never correctness. They
are read and triaged as a pair: precision that costs the novice the thread moves to Appendix B or the script; clarity
that costs a hypothesis is not clarity; caveats are never the fix; and no change for them may disrupt the other
personas' experience (their last reads are checked before a change lands). First pass before the final reader round,
on the paper at a named head; again inside the round.

## Handover (tenth PM, 2026-11-11; Sonnet; context near its limit)

Rule zero of every brief (also first line of scratchpad/pm5-rules.md): the agent opens `git worktree add <path under scratchpad/pm-worktrees/> -b <branch> origin/dev`, names it, never edits the main checkout (agent a9af01695ad475450 broke this twice).

Landed on dev: triage 981b7d7 (approved; Examples page three-term numbers to be fixed from the regenerated record, paper is of record; the "what the case leaves out" paragraph for Appendix C and the case-page list are drafted in the triage and land after the WP30 cascade); WP29 corollary 8b5c4f4, P9/P10 reads bcb864e, triage 6140ace, narrowings 3f8c49b, face step d7ac579, re-read and acceptance package 7e7acdd (WP29-review.md; open wording items from reads2 not yet triaged: "conditioned metrics" means log-metrics, "the fit" is the clean fit, "lowers" first order only, A5 missing from the hypotheses line, Appendix B "quoted from the statement" lines); S-5 units 8fc2d47 (Figure 9), fc9aa58 (root page, docs), ef85f35 (screenshots); lint 1814496; review list 4b7ca4a; deliverables grid f5e329f (P4 maps to Use: add the note); thin-term panel aa11445; Figure 1 rings 10a32d2 (open: footer "Weight ... 1.00, 1.00, 1.00" cryptic, caption does not say the dots are one fitted posynomial's terms: for the supervisor); WP34 scope and Windows job in test.yml b4c8c96 (coordinator dispatches `gh workflow run test.yml --ref dev -f windows=true`; resume agent a27de0d962d3e2155 to read the log and write WP34-readout.md).

WP30 (branches wp30a 4128a13, wp30b d6db4bf, unpushed, rebased on 8b5c4f4; rebase again on dev before the gate): final values (350,000 unit; 6,000,000 covered fleet with 8,000,000 full budget; launch 7,000 USD/kg, budget 105,770; 2026 coefficients; wheel relation 4,000 + 2.0e6/N.m, small and large are relation values), thirteen traded metrics, sample size 1,250 per regime (203 s per 1000 at 3 workers; 3,000 would take about 2 h; the supervisor's default of 3,000 is not met: a question for him, or run nine workers), contract version 20 prepared, red set 33 failed + 3 errors, all data-bound (listed in WP30-build-notes.md). Gate checklist updated on the branch (no placeholder model, one container run @10 shared @9). Next: merge to dev, step 8 regeneration (commands in the build notes), steps 9 to 12, the container commands to the coordinator, the cascade (paper sentences: two of thirteen do not bind; Sections 7 and 8 sampling sentences with ledger raise row; coverage and 6M/8M statement in the body once, detail in Appendix C; the left-out paragraph and case list; Examples page fix with a test), stage 6.

Not started: WP25-5, WP32, WP33, WP8b guide skeleton and checklist, final reader round, key v5 sentences (statements the readers were asked about are in WP29-review/reads/README.md; list for thirteen metrics and corollary still to send), both-platform runs at the head. Mine to prune: worktrees under pm-worktrees (wp29, wp29face, wp30a, wp30b after the gate, thinterm, fig1, windows, hand10, fig-trilemma, s5real, spikeD2 if present).

## Handover (twelfth PM, 2026-11-12; Sonnet; context near its limit)

Rule zero stands (own worktree under scratchpad/pm-worktrees/, named in every brief). New rules this PM learned: a browser-using agent opens its own tab and closes only that tab, never lists or closes others (the assistant's tabs and any cell's are theirs; the twelfth PM closed tab-84, the assistant's, in a stale-tab cleanup during WP32 round 3); agents never use the `gh` CLI for research (its credentials expose private repositories; unauthenticated curl/WebFetch only); verbatim cell returns are excluded from ruff (work-packages/WP32-cells/round-*); every unit runs whole-repo ruff check and format --check, the encoding test, and the claims-register test with the site/docs tests before a push; one writer of paper/ at a time.

Landed on dev this PM (heads in order): WP25-5 deletions 1a20557; WP29 wording e10a4f1; Windows slow shard cfd85a8, stage 4 fixes (accepted 9418183); entry surfaces e5d2c35; cascade: term order a4d4fc7/7adfb84, chunked pool 65dcd38, paper re-execution a5cd754/4162a61, choosing-K K = 2 755e151, sensitivity K = 2 keys 95f6f5d, @12 pointers e7141da, six requirements 320fead, design-sets wording 9b055ec, D.2 order and number format a8b927d, stage 6 fixes 94464bb; stage 6 reads: review 2511508 (WP30-review/), P7/P8 finals ee3039b/777e806 and triage 77fe83c; WP32 accepted (6be8a9f; review closure c33b108); WP33 baseline reads 0fc6b29, journeys map cde6e5d, D-2 units: root page ebacd28, docs home fa612f4, README a80a403, paper d8d650e (breach of the abstract non-goal, corrected by 2298720, which restored the abstract verbatim and put the reader line at the end of Section 1's Organization paragraph); WP35 spike ace2840, scope 1d27f8c approved, build b1b43cf (prior_art split, glossary 'hyperbolic', Appendix G); WP36 spikes W1 3d73cea, W2 e11fe60, W3 07217d4; WP37 research W1 d5ab21d, W2 822d80b, W3 5073055, W4 4846450/a3200c4, W5 a5d5607, scope 2a1d4fa (D-9 amendment f8cb99c), history.yaml record 71d45c5, generator 45877ec, tests a5089b6, prose df0cad9 (85 entries, 418 words).

Open, in the order I would take them:
1. WP33 D-2 items 5 and 6 are STOPPED and with the assistant (api.md/api-reference.md merge is contract-pinned; the 'User guide' nav heading needs overview.md renamed to user-guide/index.md): options reported, no answer yet. The docs home first screen at 390 px shows two of five links above the fold (PCA paragraph sits above the list). WP33 repeat round (second wayfinding round on the rebuilt stage) and the fresh U1 cell (WP32 R-10) are to be released on the assistant's head message; WP33-review.md, WP33 acceptance, then WP33 D-3/D-4/D-5 records (WP33-decisions.md placements/cuts, WP33-wayfinding.md) are not written. The 'Loading...' placeholders and wide tables clipping at the right edge are recorded for the review list and WP8b, not units.
2. WP35: build landed (b1b43cf); stage 6 not done: WP35-review.md with a fresh reader of Section 2 and Appendix G rendered (P9/P10 balance rule), docs pages screenshotted, WP35-decisions acceptance. Appendix F's 'observed commit' cell and the K-row notebook outputs were patched in place for two tables: re-execute fully at the next paper unit.
3. WP36: readouts exist (W1, W2, W3). Still to do: the PM-side synthesis readout work-packages/WP36-rounds/spike/readout.md ending with the draft paragraph for the paper's future-directions place and one for the docs, each under fifty words per idea, with plain options on where and how much, no recommendation tags; the W2 readout's two URLs (highs-js, slsqp-rssl) to correct per W3's sources file (ask the assistant: correct or leave). Integration would run through the paper notebook's single-writer queue.
4. WP37: D-9 delivered at df0cad9 (the fixed history page is on the stage and open for the supervisor); to do: the fresh reader's walk (R-11) and WP37-review.md; the supervisor's approvals of the nine defaults; open items in WP37-rounds/open-items.md (Wiley DOI to open by hand; Penland workshops 2 and 3 videos not found; Medium links; the Edinburgh talk rests on the CV alone; the Clark journal page unread).
5. The abstract and the five entry surfaces: every change is listed in supervisor-review-list.md 'Entry surfaces' (e5d2c35); no release is pushed until the supervisor has approved the abstract. Keep the section current.
6. WP34 stage 4 'gates matrix' is accepted; both-platform green runs belong to the assistant (CI at each batch head); the container at the gate was done by him at b4606f5 (data of record).
7. Final reader round (depths A to D, P1 to P10, key sentences to the assistant: the key is his; I sent six draft sentences), WP8b reviewer's guide and release checklist drafts (WP8b-release-checklist.md, WP8b-reviewers-guide-skeleton.md, fill after the above), deliverables grid and review list refreshed at 8806b0e (refresh again), the claims register current, the machinery defect fix 71df406 (docs figure build now writes only its own figures; `--paper` regenerates the tracked ones).
8. Pending small items: the assistant's review-list row for Figure 6's retirement is in (17753f9); the 1,250 sample-size mention in the gate checklist is history, left; WP32 residuals (K = 1 tension_report error right after select_temperature on exact-relation tables; matplotlib font line) stand as written.

Worktrees still open that I created (prune once their units are closed; never wp30b, stage, verify, rec, gate30, wp27model, preview-wt, hts-reader-EF): wp37d9, wp37fix2, wp37fix, wp37draft, wp37w1, wp37w2, wp37w3, wp37r2a, wp37r2b, wp37r3, wp37scope, wp35spike, wp35build, wp35scope, wp36w1, wp36w2, wp36w3, wp33root, wp33docs, wp33paper, wp33readme, wp33d1, abstractfix, figdet, wp32rev, wp32close, wp32rec, entrysurf. Agent ids that may still report: none known running.

## Handover (thirteenth PM, 2026-11-13, night; Sonnet; its run ended at dev 6d83d95; written by the assistant from the PM's hand-back)

Rule zero stands (own worktree under `scratchpad/pm-worktrees/`, named in every brief; remove it when the unit lands).
A browser-using agent opens its own tab and closes only that tab. Models by role: the PM on Sonnet; implementers,
readers and reviewers on Sonnet; mechanical units on Haiku; `model` named on every spawn. Heads only to the assistant,
who verifies, rebuilds the stage and accepts. No attribution lines anywhere.

Landed this PM (accepted by the assistant unless marked): the summed-pairs table f10c7bf; G.2 as a three-column table
e249460; Appendix E's mathematics ebd26ee and widths 1d741d2; Appendix A's mathematics 794a4e8; the WP36 integration
7fe47de and 9b284fa; the WP33 closing round 36e0e9f, 2dcfbd1, b943eba (contract 23), 15d00af, eb08f27, 79015eb, the
fresh U3 cell e14ba68, the review 800a90a/44db494 with its addendum 809b8b8 (on the review list for the supervisor);
WP37's review 940e238 and closing units 36386eb and 7a14cea with the open items 4f7cc8b (the supervisor's acceptance
pending); the WP38 machinery 94f33ae and 3e2b60d (baseline 1d741d2); the WP39 spike fb6adcc and scope fe2335e
(approved 518b5ab); the WP40 inventory 64aa577 and scope dfc7c95 (approved 6d83d95); Appendix H cfa943f (NOT yet
accepted: its follow-up is in flight).

In flight, not the next PM's to duplicate: the Appendix H follow-up, agent a93614e4fd602291f in worktree `wp35hnb`,
carrying the reviewer's five points (`WP35-decisions.md`, 1862491), the "count not rate" wording with the two
baseline rows dropped, the readout's closing section, and the five repository-path parentheticals on the supporting
material page. Its result reaches the assistant as a commit on dev or a hand-back; the next PM waits for the
assistant's word that Appendix H is accepted.

Open, in the order to take them:
1. When the assistant says Appendix H is accepted: WP35's R-13 and R-14, three fresh readers (Sonnet) on the finished
   Appendix H and Section 2 as rendered, with the reader criticisms as checks (RA-10, RA-11 of the amendment);
   `WP35-review.md` completed; then WP35 to the review list.
2. WP39 build per its approved scope, through the paper notebook's single-writer queue: the generator and tests first in
   a parallel worktree, then the subsection, Appendix D's table, the register and ledger rows, the notebooks re-executed
   once; then the P8 and P7 cold reads and the skim test (R-7, R-8); `WP39-review.md`.
3. WP40 build per its approved scope, after WP39 lands and before the final reader round (D-1 to D-9 in the scope's
   order; D-8 through the paper queue; the three PM-raised defaults as approved).
4. The WP38 pass, on the assistant's word once WP39 and WP40 have landed: the reader's brief of
   `docs/superpowers/notes/residual-review.md`, copy-editing only, the checker before and after.
5. The final reader round, depths A to D, P1 to P10, against key version 5 (the key is the assistant's; readers never
   see it); then the register, the grid and the review list refreshed.
6. WP8b drafts: version 0.1.0, the changelog heading, the reviewer's guide (naming the WP38 machinery and the
   supervisor's close-read list: the five entry surfaces and G.2), the release checklist with the two rows (reload a
   docs page after the tag for the releases-widget 404; fetch every GitHub link after the merge to main).
Not the PM's: the abstract and the five entry surfaces (the supervisor's close read), the history page's acceptance,
the stage (port 8791, tab-100) and the CI dispatches (the assistant's), the merge to main, the tag.

Worktrees at handover (8): the main checkout, pm13main, wp27model (an untracked handover note), wp35hnb (in flight),
stage, verify, preview-wt, hts-reader-EF. Never touch stage, verify, preview-wt, hts-reader-EF or tab-100.

## Fourteenth PM rules added (2026-11-13)

- Never wait on `pgrep -f <pattern>` where the pattern matches the waiting command itself (the WP39 implementer's
  `until ! pgrep -f ...` loops hung two hours on their own command line). Wait on the child's pid or a done-file, or
  bracket the pattern (`"[e]xecute_notebooks.py"`). Put this in every implementer brief.
- Units land on dev by rebase onto origin/dev and fast-forward (`git push origin <branch>:dev`), never by a merge
  commit (1235f7f was one by mistake).
- Set `MPLCONFIGDIR` to a scratch directory before executing notebooks or running the site and figure tests (font-cache
  stderr otherwise).
- An implementer iterates on the failing tests alone and runs the full group once before the push (the WP39 fix unit
  spent two and a half hours on repeated full runs).
- Section 9's decision paragraph rose to 159 words; the ceiling test's bound (150 to 160) moved with the reader
  definitions.

## Handover (fourteenth PM, 2026-11-14; Sonnet; written by the PM at its hand-back)

Landed this PM (all on dev, units by rebase and fast-forward): WP35 reader briefs and WP8b rows 8aef509; WP35 reads
c073362 and wording unit 940d6f0 (Appendix H accepted at 3d5a53e); WP39 notebook unit 20bff6e, clean execution
a538fc4, fixes 50d8427 and f89c663, reads c3d66a3, review 94cb6a1; root page order and summary 4b8aa94 and 26555f2;
WP40 build cb91835 (records under WP40-rounds/thinning/), D-8 995075b, review 1be1e12; WP38 pass: flags 6007221,
landings L1 7f790f2, L2 0b31ef1, L3 d417196, N1+N2+X 7caf05d, residue 368f3a1, round 2 ba22d92, l1 nit 116c929,
confirmations and closing records (WP38-review.md, baseline retaken) 5fa00a5. Review-list rows for WP35, WP39, WP40
and WP38 are in. The pass is not "every surface reads clean": 18 of 96 confirmation rows clean; the rest listed in
WP38-review.md as the post-0.1 list (with the 163 lemma rows and the history page's 30 rows).

Open for the next PM: (1) the docs-site build fixtures in tests/test_site.py and tests/test_docs.py failed in the
WP38 review unit's worktree (2 failed, 11 errors, a MkDocs 2 warning banner); earlier units had them green: re-run
on a clean checkout before acceptance. (2) The final reader round: PLAN.md and 28 briefs (F01 to F28) are ready under
scratchpad/final-round/ (assistant settles five options in PLAN.md section 8; slices are to be recaptured; the key is
the assistant's). (3) WP8b drafts (version 0.1.0, changelog heading, reviewer's guide, release checklist rows); the
rows G1 and G2 are in. (4) Register and grid refresh. Not the PM's: abstract, entry surfaces, history page, the
merge to main, the tag.
Worktrees held at hand-back: none of mine except pm13main and wp27model (older PMs); never touch stage, verify,
preview-wt, hts-reader-EF.


## The supervisor's intents, in his words (2026-11-14; a guide for every PM and unit, never a substitute for his word)

Built at his request on 2026-11-14 so the team stays close to his intents; the full sketch is the driver's, and this is
the part a PM and its units need. Where he has not spoken, his next sentence overrides it.

- **The product.** "at the end of the day i care about having a well documented practically useful HTS package, the
  paper is just means to an end." The package's API, its examples and its docs come first when work must be ordered;
  a reader's trouble using the tool is a product defect, not a paper friction.
- **The release line.** He places work outside 0.1 on purpose and clarifies the boundary "so there are concrete items
  on the other side of the limit and we feel confident about what we say in the paper because we have some foresight
  about our forward looking claims even if we're not trying to defend them in the paper." Research that could show the
  method missed or got something wrong lands before 0.1; documentation that extends the examples lands after. Every
  spike's readout ends with what the paper may say now, what it may not, and what the next release builds.
- **Two requirements, never confused.** The work that tests the method (a test record: the expected answer written
  before the fit, reported whether it passes or fails) and the didactic story drawn from it for the user. "don't
  confuse readers to convince us." Unrelated cases, because "the point here is to truly show the method works."
- **Words.** Settled in the glossary, then held to; intuitive at the top level, caveats only in detailed content. The
  three layers of optimization keep their words apart: objective (the decision-maker's subset of the metrics),
  constraint, Pareto notions at the decision layer; GGP and log-convex at the design layer (the model as a function of
  the metrics); loss at the method layer (what the solver minimizes). Tension is the local partial derivative between
  two metrics on the surface; elasticity its log-log constant-per-term form; trade-off the plain word; decision-maker,
  not executive. One object, one name. No borrowed idiom with a false analogy; an intuition word is welcome when the
  object behind it is named.
- **Claims.** Aligned to the facts, in this order of preference: first ask what would back the claim he wants and what
  it costs; then narrow; never caveat. "formally verified" and "machine-checked" are never said of the SymPy scripts.
- **Deciding.** One problem-level question at a time, plain options, no recommended tag; his one-line answer is the
  record, quoted verbatim. He corrects by restating intent, not by editing prose: smooth his wording outside decision
  records. He expects a conflation of two objects to be caught and carried through ("one is from the fit and one is
  from the sampled data").
- **What loses him.** Jargon in an intuitive section; a sentence written to convince; content forced into the paper
  that belongs in the repository or the docs; a method shown only on its own synthetic case; a report that did not run
  the thing or look at the render.
- **The breadth of the examples (20:00).** The examples should show the breadth of the model along the axes he named:
  dimension (attributes, metrics and objectives vary), the number of terms, tight against soft fits, measured against
  simulated, the engineering lifecycle stage from research to end of life, and the measurement method, synthetic or
  actual, mixed within one problem. An intent for the build-out, "as we establish this first release as an initial
  condition", recorded in `work-packages/examples-coverage.md`; each WP45 test record states its case's row.
- **The search's two aims (22:25).** "find and where possible characterize and potentially 'fill in' holes within the
  envelope, and push the envelope." Filling in is sampling for witnesses of a candidate hole (a persistent class may be
  only an absence of witnesses); pushing is a proposal beyond the surface; both are conjectures settled by building and
  measuring. White space is 0.1's word; hole is reserved for WP50's object and is not defined in 0.1.


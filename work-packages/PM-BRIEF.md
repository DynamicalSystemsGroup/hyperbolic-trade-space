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
5. The notes for the package at hand: `docs/superpowers/notes/{adcs-port,proof-conventions,
   sklearn-conformance,presentation-framing,references-verified}.md`.
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
with Appendix F out, OD3 a, OD4 b, OD5 a, OD6 a, OD7 the defaults); the sizing (123 units: 14 paper sections, 27 boxed
statements, 10 floats, 7 appendices with 40 generated tables, 14 docs pages, 8 docs figures, the root page, the README;
the paper at 9,805 words of a 10,107 ceiling, the docs at 6,792 of 7,600); round 2's friction counts and worst cells
(`WP11-round-1/triage.md`, "Round 2") as the triager's input; the answer key at version 4 (hash in `WP11-decisions.md`;
the file is the driver's: the triager sends reader sentences and gets stated / missing / wrong back; round 2's lines
through the recorded "key stale" mapping); the orphan list (`paper/figures/fig-chart-k3.png`, `fig-predict-check.png`
tracked and unreferenced; `docs/generated/figures/ternary-cubesat-*`, `three-facets-*` generated and unreferenced); the
stage note (a fresh worktree copies the main checkout's `paper/_build/templates` before `stage_site.py`; recorded as a
WP8b release item). WP8b's release items list (`driver-log.md`, the WP8b entries; `WP8b-scope-of-work.md`) is the step
after 5a and is inherited with it.

Next for the seventh PM, in order: (0) first, one small paper unit allowed during WP28 (a narrowing): the maths unit's
(a) clause, one sentence where the conditioning is stated (Section 3 or 8): the conditioning of record centres each
log-metric (the standard scaler), so the one-term objective of (2) is (1); with uncentred log-metrics they differ by the
linear term and need not share a minimizer (backing: L14's identity and A2; `np.log(study.M).mean(0)` is 0 to 7e-15 on
both regimes); it lands before the inventory reader reads that section, or that reader reads the head after it.
(1) D-1, the inventory: a coordinator stages the site at the head, fans out about 55 cold readers one per unit
(no record in any brief; the story sentences from Section 1's main-results list and the abstract, the docs Home for the
docs; figures image first; two models), commits the returns verbatim with `WP28-inventory.md` before any triage. (2) A
fresh triager (not a reader, not an author) writes `WP28-cut-list.md` per the scope's D-2 (goes / merged / shortened to
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

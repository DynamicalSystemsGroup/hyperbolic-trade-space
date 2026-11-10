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


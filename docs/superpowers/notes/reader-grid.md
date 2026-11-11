# Note: the reader grid (depths by personas) and the cold-read protocol

Drafted 2026-11-08 by the driver as input to WP11's scope (not scoped yet). The depths are the
supervisor's and are recorded; the six personas were drawn from his words and **decided by him on
2026-11-08 ("Use these six", `WP10-decisions.md`)**; the protocol is the driver's proposal and is
decided in WP11's scope.

## The supervisor's words

On the paper (2026-11-08): "we'll need to run a grid of user reads (cold) at the depth levels
previously outlined and with differing personas."

On the testing loops (2026-11-08): "do you have a grid of our reader depths cross our reader
personas? that will be key for the testing loops. you'll need context gapped user tests and expect
them to give contradictory feedback which you will then needs to triage to get clean, clear, robust
results. it will help prevent metric gaming to reviewers persona or read depth"

## What existed before this note

The six depths, in his words, in `WP10-scope-of-work.md` ("Reader model"). No personas anywhere in
the repository: the phrase "depth levels x personas" appears in three records and nothing defines
the second axis. WP10's own acceptance uses the depth axis only (one cold reader per level,
structural).

## Axis 1: depths (decided), with what each reader is given

| Depth | The reader (his words) | Given to the test reader, and nothing else | The depth's job |
|---|---|---|---|
| L-A | just abstract / hero image | the rendered title, abstract and Figure 1 with its caption | know the decision problem, the idea and the finding; want to read on |
| L-B | skim the headers, main results and figures | rendered headers, the main-results list, statement blocks, figures and captions | be able to state the main results and what is and is not claimed |
| L-C | read the whole paper | the rendered main text, appendices withheld | follow the argument; no unanswered "why" that the main text owes |
| L-D | the paper and the supplemental materials | main text and appendices, no repository | find the full version of anything the main text points to |
| L-E | pull the code to reproduce it | the paper, the repository at the commit, the container | regenerate what the paper shows by following Appendix F alone |
| L-F | reproduce it and adapt it for their own case | as L-E, plus a table the authors did not tune on | run the method on that table and read the result correctly |

The slices for L-A to L-D are captured from the rendered pages in the browser (so the reader sees
what a person sees, and cannot read past its depth); L-E and L-F readers work in a clean checkout.

## Axis 2: personas (decided; each traced to the supervisor's words)

| | Persona | Traced to | Comes with | Wants |
|---|---|---|---|---|
| P1 | The accountable decision maker | "interpretable and intuitive to an accountable executive"; "make and defend a judgement call" | domain judgement, little time, no convex analysis | to know what trades against what, and whether to trust the method |
| P2 | The trade-study practitioner | "today they are mostly done as documents, grids or tables in a pdf"; "ongoing configuration management" | systems engineering practice, spreadsheets, some statistics | a method they can run, rerun and defend |
| P3 | The modeller with their own system model | "someone interested in cross applying to other sysml models"; the configuration-to-attributes abstraction | their own model or test data, SysML or not | to plug their evaluation in and know what must hold |
| P4 | The machine-learning practitioner | notation anchored on scikit-learn; "similar feel to PCA"; "unsupervised learning / feature engineering" | PCA, scikit-learn, pipelines | where this sits beside PCA and how to use it |
| P5 | The optimization reader | "multivariate calculus, linear algebra, convex optimization"; Boyd and Vandenberghe | convex analysis, geometric programming | to check the mathematics and the algorithm's claims |
| P6 | The sceptical neighbour | "we don't want to be told this is just X where X is some existing work" | deep knowledge of one adjacent method (Pareto, DEA, frontier analysis) | to decide whether this is new to them or a renaming |
| P7 | The new-space systems engineer | the supervisor, 2026-11-11: "a systems engineer from a blue origin or spacex, someone who really knows how these things get built"; "more like our modeler or a quality engineer" | ten or more years building and flying hardware at a vertically integrated launch-and-satellite company: requirements to test to flight, mass and power budgets, vendor parts and in-house parts, qualification campaigns, what a bus actually costs and how long it takes; reads a SysML model and a data table without help; impatient with a case that is not how things get built | to see whether the case's choices, numbers, couplings and requirements are how a real program behaves, where the model is a toy and says so, and what they would change before trusting the trade reading on their own program |
| P8 | The new-space executive | the supervisor, 2026-11-11: "an execute from such a company"; "the other is more like our sponsor" | runs a program or a business line at such a company: budgets per satellite and per fleet, schedule, launch procurement, what the board asks; reads a figure and a sentence of numbers, not a derivation; decides with incomplete information and is accountable for it | to know whether the method would change a decision they make, what it costs them to adopt, whether the case's economics and verdicts read sanely to someone who buys launches and parts, and what the method does not tell them |

## The grid: which cells are tested

Not every persona reads at every depth. *Core* cells are where that reader is expected; *edge*
cells are plausible and sampled less often; blank cells are not tested.

| | L-A | L-B | L-C | L-D | L-E | L-F |
|---|---|---|---|---|---|---|
| P1 decision maker | core | core | edge | | | |
| P2 practitioner | core | core | core | edge | core | core |
| P3 modeller | core | core | core | core | edge | core |
| P4 ML practitioner | core | core | core | edge | core | core |
| P5 optimization reader | edge | core | core | core | edge | |
| P6 sceptical neighbour | core | core | core | core | | |
| P7 new-space systems engineer | edge | core | core | core | edge | core |
| P8 new-space executive | core | core | edge | | | |

Thirty core cells and nine edge cells (P7 and P8 added 2026-11-11).

**P7 and P8, how they are built (2026-11-11).** The companies are not named in any brief or record; the personas'
characteristics are backed out of the public shape of such companies: vertically integrated, hardware-rich, fast
iteration, in-house manufacture of most subsystems, launch bought or flown in-house, programs priced per unit and per
fleet, a culture that trusts test data over models. P7 reads at depths B to F with the case model, Appendix C and the
model in the repository or the editor in front of them; P8 reads at depths A and B, the case narrative, the figures,
the stakeholder layer and the verdicts. They are the review pair for every change to the case model (the model
revision's stage 6 review first) and join the reader rounds from the next round on. Their standing question is the
supervisor's hard requirement: is the case realistic enough to keep a collaborator from the space industry interested,
and where it is not, does it say so.

## Axis 3: package users (added 2026-11-11)

The supervisor, verbatim: "make sure to add more user test cases for people who show up and just want to pull the
package and read the docs. do personas for both humans coding and coding agents coding. this is specifically for the
HTS package, from that perspective they no little if anything about satellites or even sysmlv2 they just want to use
our feature engineering tool. we want users with and without sysmlv2 models generatign their data (it could just be
measured, or generated another way), and users with and without sysmlv2 model experience because we don't want to
scare not sysmlv2 users away from using the package".

These readers do not read the paper. They arrive at the repository or the docs site, install the package and try to
use it on a table of their own. Two axes crossed: who is coding (a human; a coding agent given only what a user has:
the README, the docs site and the installed package, never the repository's notes, records or tests) and whether they
have SysML v2 experience (none; some). A third axis is the task's data: a table measured or generated by other means
(a CSV with no model behind it) or a table exported from a SysML v2 model. Every cell knows little or nothing about
satellites.

| | Persona | Comes with | Task | Returns |
|---|---|---|---|---|
| U1 | The human coder, no SysML v2 | Python and pandas, a table of evaluated designs from a spreadsheet or an experiment, no model | install from the README; condition the table; fit; choose K; read the tension report and the chart; say which metrics trade | where they stopped, what they could not find, what they would ask a colleague; whether anything made them think the package needs SysML v2 or satellites |
| U2 | The human coder, with SysML v2 | the same, plus a SysML v2 model that produced the table | U1's task from the exported table, then: does the docs' case model help or distract; could they connect their own model as the case does | as U1, plus what the model side of the docs did for them |
| U3 | The coding agent, no SysML v2 | a fresh agent with the README, the docs site and the installed package only, a CSV table it is handed | U1's task end to end, writing the code; it reports every page it opened and every error it hit | the code it wrote, the pages it used, the stumbles, the result it read off |
| U4 | The coding agent, with SysML v2 | as U3, with the task's table exported from a SysML v2 model it is given | U3's task, then the model-side question of U2 | as U3, plus the model side |

The tasks are run on the staged docs site at a named head, with the package installed from the repository at that
head (`uv pip install` or `uv sync` as the README says), never with the repository's `work-packages/` or notes in
reach. The returns are recorded verbatim and triaged like a reader round: each stumble becomes a docs change request
or a package change request with the page or function named, and the round repeats on the fixed site until a fresh
cell completes the task without a stop the docs owe. The human cells are played by fresh agents in the human's role
until a human sits down; the agent cells are agents as themselves. The first round runs before the package is handed
to the supervisor; it is the UX loop his mandate names.

## Three roles that never share context

- **The author** (implementer subagents) writes and revises. Never sees a reader's prompt, the
  answer key, or which persona or depth a finding came from.
- **The reader** (a fresh subagent per read) gets a persona brief, its depth's slice and a neutral
  task. Never sees the repository's records, the scope, the register, the story as we tell it, the
  answer key, another reader's report, or the fact that it is one cell of a grid.
- **The triager** (the driver) holds the answer key and all reports, and writes change requests.
  Never writes the paper's prose.

## What a reader returns: recall and friction, not scores

In its own words: what this is about; the main result; what it would do next with it; what it would
tell a colleague; what it thinks the method does not do. Then: where it was confused or stopped,
quoting the passage; any term it had to guess; whether it would go one depth further and why. L-E
and L-F readers add the commands they ran and where anything broke. No ratings: a number invites
tuning to the number and hides what was misunderstood.

## The answer key

Written by the triager from the records before the first read, and fixed for a round: the story's
parts, the main results, each depth's job, and the things a reader must *not* come away believing
(that the method picks the design; that it claims novelty; that the frontier is the only level
surface; that a certificate proves a global optimum; that it replaces Pareto analysis or PCA). Each
recalled statement is marked against it: stated correctly, missing, or stated wrongly. A wrong
belief is the worst outcome a read can have; a missing one is next; friction is third.

## Triage: expecting contradiction

1. **Classify** each finding: wrong belief, missing, friction, defect (a broken link, a wrong
   number), or preference.
2. **Replicate.** Each tested cell is read by at least two independent readers. A preference or a
   friction reported once is logged, not acted on. A wrong belief or a defect counts at once.
3. **Read the pattern.** The same finding across personas at one depth is a problem of structure at
   that depth; across depths for one persona it is a problem of fit to that reader; in one cell it
   is local.
4. **Resolve contradictions in this order:**
   a. *the depth contract:* a wish for more at one depth is met by a better pointer to the next
      depth, not by moving material up (the main text is not crowded);
   b. *the recorded intents:* the story, the register's words, the separation of the paper from the
      docsite, map and territory, claiming nothing as novel;
   c. *the reader model:* the assumed mathematics holds from L-C down; a reader below it is served
      at L-A and L-B only;
   d. what is still contradictory is a real trade-off and goes to the supervisor with both
      readers' words.
5. **Change requests** to the author state the passage, the problem and the constraint. They do
   not name the persona or the depth.
6. **Re-test with new readers:** the cell that found the problem, the same depth for the other
   personas, and the same persona one depth either side. A fix that helps one cell and hurts its
   neighbour is not a fix.

## Against tuning to the test

- Fresh readers every round; persona briefs reworded each round; replicates on different models.
- A held-out set of cells and of brief wordings is never used while revising; it is read once, at
  the end, as the confirmation.
- The result is always reported as the whole grid with its worst cells, never as an average, and
  "passes" is defined per cell on the answer key (no wrong belief; the depth's job done), not on
  how pleased the reader was.
- These readers are models, not people: they parse dense text more easily than a person and tire
  less. A comprehension failure they report is informative; their silence is weak evidence. The
  supervisor's own reading, and later his collaborators', remain the test that counts.

## A round, and when to stop

A round reads every core cell twice and a sample of edge cells, triages, issues change requests,
and re-tests after the revision. The loops stop when two consecutive rounds show no wrong belief in
any core cell and no replicated friction; then the held-out set is read once; then the supervisor
reads.

## Open for the supervisor

Nothing on the axes. The protocol (roles, what readers return, the answer key, triage, the guards
against tuning, the stopping rule) is the driver's proposal and is decided in WP11's scope. A grid
for the docsite (a package user doing tasks) would be a separate, smaller one and is not drafted.

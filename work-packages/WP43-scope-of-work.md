# WP43 — Scope of work: beyond the posynomial, the kernel direction tested (research spike)

| | |
|---|---|
| **Status** | DRAFT. Approved only by the recorded act below; nothing is built before then. |
| **Supervisor (accountable)** | mzargham |
| **Repository** | `DynamicalSystemsGroup/hyperbolic-trade-space`; work on `dev`, in a spike folder |
| **Approval record** | The supervisor's verbal approval, quoted verbatim in `work-packages/WP43-decisions.md` |
| **Acceptance record** | The supervisor's acceptance of the readout, quoted verbatim in `WP43-decisions.md` |

## Purpose

The supervisor's question and direction of 2026-11-14 (`WP43-decisions.md`, verbatim there): the one-term line in the
adjusted plane leaves a visible downward bend at the upper right; what function beyond a posynomial would hug it, and
can the solver be generalized to fit it. The spike tests and defines the kernel direction the paper names but does not
build, on more test cases than the cubesat; its findings refine the implementation and expand the documentation's
examples, and the paper gains no new complexity: at most a word in its three sentences on alternatives, where the
spike shows the right class name. This is stage 1 (research spike) and stage 2 (decide) of the six-stage lifecycle;
the build, quality control, integration and review are scoped from the readout.

## Goals

- G1. **The class is stated and tested:** the readout states the class of models for which the fit stays convex in the
  parameters and the designer's problem stays convex in log-metrics (log V convex in u, degree-one homogeneous; the
  posynomial at kappa = infinity and at finite kappa as members; the log-quadratic form w.u + (1/2) u'Qu - beta with Q
  positive semidefinite and Q1 = 0 as the first member beyond it), names what the class cannot represent (a
  non-log-convex edge), and says which of "GGP" and "log-convex" the paper's three alternatives sentences should carry.
- G2. **The question in the drawing is answered on the data:** on the case's two regimes, the one-term line, K = 2 and
  K = 3 sharp, K = 2 soft, and one log-quadratic term are fitted and compared in the adjusted plane and in full d by a
  held-out protocol stated before any run (slack of held-out rows below the surface; the fraction above; the band),
  with solve times; the comparison says whether the bend is more terms' work or a kernel's.
- G3. **More test cases than the cubesat:** planted tables from the generator family of Appendix C.7 extended by two
  kinds, a log-quadratic edge and a non-log-convex dent, each with its answer known, so recovery and the class
  boundary are measured and not argued; the existing three-term planted tables are the third kind.
- G4. **The implementation's extension point is designed, not built:** the readout names the smallest change to the
  estimator and solver that admits a feature map and a convex parameter set without reimplementation (the LME
  objective over designs with parameters in a convex set; the exact maximum as an LP or an SDP), with the solver
  route (cvxpy with Clarabel or SCS, or scipy's constrained solvers) and what each needs in the lock.
- G5. **The documentation's examples are planned:** the readout drafts the outline of one new Examples section (the
  bend in the plane; more terms against a kernel; the boundary case) built from the spike's runs, for the build stage.

## Non-goals

- Any change to the paper's text, figures or claims register (the three sentences are backed or narrowed later, by
  the integrate stage, on the supervisor's word).
- Any change to `src/hyperbolic_trade_space/` or to `uv.lock`; the spike's code lives in `work-packages/WP43-rounds/spike/`
  and runs with `uv run --with cvxpy` (or the solver the readout chooses) in the spike's own environment.
- A theory of which kernel is right for a given table, or any lemma; the class statement is a definition with its two
  convexity facts, each cited to Boyd and Vandenberghe or to L4, not a new result.
- Public or external tables; the readout may name candidates with their licences and stable sources for a later
  package.

## Deliverables

| ID | Deliverable | Serves |
|---|---|---|
| D-1 | `work-packages/WP43-rounds/spike/protocol.md`, written before any fit: the held-out protocol, the test tables, the models compared, the measures, the solvers | G2, G3 |
| D-2 | `work-packages/WP43-rounds/spike/` scripts and records: the planted generators (log-quadratic edge, dent), the fits, the held-out tables, the plane figures for each model, solve times; every number regenerable from the data of record and the generators' seeds | G2, G3 |
| D-3 | `work-packages/WP43-rounds/spike/readout.md`: the class statement with its two facts cited; the comparison read; the boundary case shown; the extension-point design; the solver route and its lock needs; the Examples outline; plain options for the build stage and for the three sentences' word | G1 to G5 |
| D-4 | A note in `docs/superpowers/notes/` (one page) stating the class and the boundary for the glossary's "kernel direction" entry to cite | G1 |

## Requirements

| ID | Requirement | Checked by |
|---|---|---|
| R-1 | The protocol is committed before the first fit and the readout's numbers follow it | commit order in `git log`; the readout's tables against the protocol's measures |
| R-2 | Every fit runs from the committed data of record (the container ledger entries) or from a seeded generator, and reruns to the printed digits | the spike's `make` or `run.py`, run once by the reviewer |
| R-3 | The held-out comparison is out of sample for every model, with the same folds | the protocol; the scripts' fold seeds |
| R-4 | The class statement's two convexity facts each carry a citation or a lemma id | the readout's text |
| R-5 | No file under `src/`, `paper/`, `docs/` (beyond D-4's note) or `uv.lock` changes | `git diff --stat` of the delivery |
| R-6 | The dent table shows the boundary: every model in the class leaves the dent's rows above the surface or below it in the same way, recorded | the readout's boundary section with its figure |

## Definition of good

- A reader of the readout can say, for a table with a visibly curved edge, whether to add a term or change the kernel,
  what each costs, and where the class ends; and the implementer of the build stage can start from the extension-point
  design without asking a question.

## Definition of good enough

- D-1 to D-4 delivered; R-1 to R-6 pass; the comparison answers the drawing's question on the case with a held-out
  number per model; the three planted kinds each have a recovery or boundary result; the readout's options are plain
  and carry no recommended tag.

## Definition of done

Good enough is met, no open item remains unresolved, and the supervisor has accepted the readout by the acceptance
record above; the build stage is then scoped from it.

## Agent's defaults

- Held-out protocol: five folds over rows, stratified by regime; the measures are the mean slack of held-out rows below
  the surface, the held-out fraction above V = 1 against the fit's convention, and the band *(default)*.
- Solver for the log-quadratic term: cvxpy with Clarabel, falling back to SCS; the posynomial fits by the package as
  shipped *(default)*.
- Planted kinds: the existing three-term tables; a log-quadratic edge with Q of rank one and two; a dent made by
  removing a convex cap of rows from a planted table's edge *(default)*.
- Four metrics and 400 rows per planted table, as Appendix C.7; twenty tables per kind *(default)*.
- The spike runs in a worktree on Sonnet; the reviewer of the readout is a fresh Sonnet reader who reruns `run.py`
  *(default)*.

## Open decisions (for the supervisor)

None. Every item was resolved through the decision loop (the direction of 13:55).

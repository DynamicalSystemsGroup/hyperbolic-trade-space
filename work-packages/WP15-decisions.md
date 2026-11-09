# WP15 — Decision records (system model tidy-up)

Records typed by the agent (driver session). Decisions are the supervisor's.

## Origin (2026-11-08)

- The supervisor's request, verbatim in `README.md` (roadmap section); the driver's breakout note
  `docs/superpowers/notes/system-model-tidy.md`; the seam decided there: "do it in parallel to start
  but eventually i'd like to be able to swap over onto the new data" (v2 data beside the frozen
  originals, swap at a later gate); the tooling note ("you probably need a clean pull of both
  opensysml and sysml-toolkit, my pins are out of date"); the abstraction rule ("we're keeping an
  abstraction of config variables and measured attributes ..."). Draft scope by the PM's bounded
  subagent (`WP15-scope-of-work.md`, revised f341690+).

## Decision loop (2026-11-08)

- **OD1, the WP4 geostationary variant.** Options: fold it in as a second scenario / retire it to
  the record. **Supervisor (mzargham), verbatim:** "i think i want to retire it but before we do
  lets make sure we preserve what we need to ensure we can test our approaches sensitivity to
  modeling assumptions. the main benefit of folding it in is that we can look at how two models of
  the same system can produce different results depending on what phenomena are in or out of scope.
  i want that to be a concept we explore in our repo even if it doesn't raise to the level of
  appearing in the paper itself."
- Disposition: retire with preservation. The tidied `v2` model covers the cubesat only; the WP4
  variant's modules, SysML file, dataset and tests stay frozen and runnable, registered in the
  experiment ledger as a second, legacy oracle (configuration → attributes, the WP14 signature) so
  that a sensitivity-to-modelling-scope experiment can be defined: the same system modelled with
  different phenomena in scope, run on a shared configuration subspace, the frontiers and tensions
  compared. WP15 delivers the ledger registration and the hooks (both oracles callable through one
  interface; an experiment definition that runs them side by side); the exploration itself (the
  comparison and its write-up) is a candidate for a later package and lives in the repository's
  notes and the abstraction-gaps ledger, not necessarily in the paper.

- **OD2, the slew physics.** Options: Python only / Python plus a closed-form calc. **Supervisor
  (mzargham), verbatim:** "Python plus a closed-form calc". Disposition: decided; the ODE in
  `adcs_sim` remains the measurement of record, called from the model's analysis; a closed-form slew
  approximation enters the SysML model as a `calc def` for model checking over the whole space
  (torque-limited and linear regimes), with a reported comparison of the two on a sample; the
  approximation is named as such wherever it is used.

- **OD3, the sysml-toolkit.** Options: pinned / optional / not used. **Supervisor (mzargham),
  verbatim:** "Pinned". Disposition: decided; a pin file with checksums and a provisioning helper
  under `examples/adcs/experiments/`, the toolkit's checks (`check`, `lint`, `verify --solve`) in
  the default test suite, failing with a named cause if the binary is missing (the opensysml
  discipline); CI downloads it on first use; the `case` dependency group and the CI workflow step
  are requested from their owners (the driver for `pyproject.toml`; the workflow is WP0's,
  amended by request).

- **OD4, how far v2 may depart.** Options: structure only / structure plus named corrections /
  redesign allowed. **Supervisor (mzargham), verbatim:** "Redesign allowed". Disposition: decided;
  the tidy may redesign the case (constants, couplings, attributes) where that makes the model
  cleaner or more faithful, each change entered in the change register with its reason; the v2
  generation is reviewed as a new case (richness conditions, fits, check designs re-established)
  before any swap; the frozen generation and every number that depends on it stay untouched until
  the swap gate.
- On model checking. **Supervisor (mzargham), verbatim:** "the z3 model checking is key because it
  can exclude infeasible models". Disposition: a goal of WP15 made explicit: the toolkit's
  `verify --solve` (Z3) and opensysml's `smt`/`solve` engines are used to exclude infeasible
  configurations and infeasible model variants before simulation (constraints and requirements
  as the feasibility definition, checked for satisfiability over the design space), so the
  experiment runner samples only what the model admits and the ledger records what was excluded
  and why; the Python feasibility flags become observations of the simulated run, not the
  definition of feasibility.

- **OD5, the frozen code at acceptance.** Options: stay as they are until the swap gate / archive at
  acceptance with shims. **Supervisor (mzargham), verbatim:** "Stay as they are until the swap gate".
  Disposition: decided; two models in the directory until the swap, the how-to says which is which,
  the frozen reproducibility tests keep running, no contract-pinned item changes; archiving is a
  swap-gate item.

- **Agent's defaults, as one item** (with OD1 to OD5 and the Z3 role folded in). **Supervisor
  (mzargham), verbatim:** "Approve the defaults as listed". Disposition: approved. Loop closed:
  decided 5 (OD1 to OD5), deferred 0, raised 1 (the Z3 feasibility role, folded into G2's goal),
  defaults approved as one item.

## Scope approval (approval gate)

- **Document:** `work-packages/WP15-scope-of-work.md` with its "Gate outcomes" (no open items).
- **Date:** 2026-11-08.
- **Driver's question:** "WP15, the system-model tidy-up: one clean SysML v2 model of the cubesat with
  a closed-form slew calc beside the Python ODE of record, Z3 and the runtime's solvers excluding
  infeasible configurations before simulation, the pinned toolkit, an experiment runner with a
  hashed ledger and the legacy WP4 oracle registered for scope-sensitivity experiments, a v2
  generation beside the frozen data with a change register and a comparison report, a how-to for
  plugging in another model; redesign allowed, frozen code untouched until the swap gate; no open
  items. Do you approve the scope for execution?" (options: Approved / Not yet).
- **Supervisor (mzargham), verbatim:** "Approved"
- **Disposition:** approved; the PM executes on `dev` on WP15's own files, the probe record first;
  `pyproject.toml`, `uv.lock` and the CI workflow step by request to the driver.

## Driver-owned dependency change (2026-11-08, on the PM's request; not a decision)

- The PM asked for `z3-solver>=4.13` in the `case` group: probes 5 and 11 at opensysml 0.12.1 found
  that the `solve` engine and the toolkit's `verify --solve` need a `z3` executable on PATH. This
  serves the supervisor's recorded role for Z3 ("the z3 model checking is key because it can exclude
  infeasible models") and is inside the approved scope.
- Done by the driver: `case = ["opensysml>=0.12.1", "z3-solver>=4.13"]`; the lock resolves
  z3-solver 5.3.3.0 (Linux wheels present in the lock); the wheel installs `.venv/bin/z3`, and
  `uv run z3 --version` reports 5.3.3; `uv lock --check` passes. Note: this machine also has a
  Homebrew `z3`, so only the first Tests run on `dev` shows that the wheel alone suffices on Linux;
  an `apt-get install z3` step is added to the workflow only if that run shows it is needed.

## The driver's calls under the mandate (not the supervisor's words; for his review at the PR)

- **2026-11-09. The fresh review (`WP15-review.md`, 21df997) and the gaps.** The review answers the
  driver's question, whether the clean model is what is evaluated, with a trace from the experiment
  definition to the loaded model text (equal hashes) and with the reviewer's own mutations of the
  model (battery specific energy, housekeeping load, tracker mass), each of which moves the
  attributes and, at the extreme, flips the feasibility flags. Identity of the new data with the
  frozen data is therefore a result. Calls on the gaps:
  - **A (both oracles through one interface, run side by side): fix before acceptance.** It is an
    approved outcome, in the supervisor's words: "we can look at how two models of the same system
    can produce different results depending on what phenomena are in or out of scope. i want that to
    be a concept we explore in our repo". A wrapper over the legacy evaluation, one experiment
    definition on the shared variables, a test, a paragraph in the how-to.
  - **B(1) (a variant proved infeasible is not written to the ledger): fix.** An exclusion that
    leaves no record is not usable evidence.
  - **B(2) (the sampler does not consume excluded regions): fix, tested on a constructed space.**
    His stated role for the solver is to exclude infeasible models; recording an exclusion without
    acting on it is not exclusion. The declared space excludes nothing, so no dataset changes.
  - **B(3) (the momentum condition is outside the solver's regions): accept, with the reason
    recorded** (it depends on the integrated slew, which the solver cannot represent).
  - **C (a stale sentence in the change register): fix. D: confirm whether it is still true** after
    the model fix of 2d13465. **E, F: accept with the reviewer's reasons.**
  WP15 is returned for A, B(1), B(2), C and D; the driver verifies and accepts after that.

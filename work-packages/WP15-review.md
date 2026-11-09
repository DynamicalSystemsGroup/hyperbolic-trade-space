# WP15 — Review report

| | |
|---|---|
| **Scope of work** | `work-packages/WP15-scope-of-work.md`, with its "Gate outcomes" (OD1 to OD5, the Z3 addition) |
| **Scope approval verified** | `work-packages/WP15-decisions.md`, "Scope approval": supervisor (mzargham), verbatim "Approved", 2026-11-08; defaults approved as one item ("Approve the defaults as listed"). |
| **Work reviewed** | `dev` at a7eebde, in a clean worktree (`git worktree add ../hts-wp15-review HEAD`, `uv sync --locked`), against start commit fc2363e |
| **Supervisor (accepts)** | mzargham |
| **Acceptance record** | Verbal acceptance in chat, quoted verbatim in `work-packages/WP15-decisions.md`, after this report |

Reviewer: fresh context, did not build the work. Nothing fixed; the only file written is this report. Scratch scripts live under the session scratchpad (`wp15rev/`). No Docker or colima was used; the worktree was removed after the checks.

## Checks run

| Check | Result |
|---|---|
| `REQUIRE_OPENSYSML=1 uv run pytest tests/test_system_model_v2.py tests/test_model_checking_v2.py tests/test_experiments.py tests/test_v2_data.py tests/test_cubesat_oracle.py tests/test_case_model_howto.py tests/test_mutation_v2.py -q` | `193 passed in 112s` |
| Frozen suite, unchanged files (`test_cubesat_model`, `test_adcs_case`, `test_adcs_enrichment`, `test_check_designs`, `test_k_terms_case`, `test_notebook`) | `121 passed in 180s` |
| `PYTHONPATH=examples/adcs uv run python -m experiments verify` | `13 entries (9 current); 0 drifts` |
| `uv lock --check`, `ruff check .`, `ruff format --check .` | pass (176 packages; all checks passed; 217 files formatted) |
| Whole `REQUIRE_OPENSYSML=1 uv run pytest` and CI | not run by this review (named files only); no CI run on these commits |
| R-17 diff `fc2363e..HEAD` over the frozen paths | only `k_terms.py` (+12/-3) and `figures/k3_log_planes_{primary,stock}.png`, all from commit 59f29b6 (WP13, legitimate). Data CSVs, `cubesat_model.py`, `generate_dataset.py`, `make_check_designs.py`, `design_space.py`, `adcs_sim.py`, both frozen `.sysml` files, the notebook and the five frozen test files: no change. `pyproject.toml`: `case` group gains `z3-solver>=4.13` (driver-owned, WP15) plus the paper/docs groups (other packages). |
| sha256, data/v2 vs frozen vs ledger | the four v2 CSVs equal the frozen files byte for byte and equal `output_sha256` of the `@2` entries (4dc4ae0b..., 9450713c..., 5794b721..., 3e06e69b...). `adcs_designs.csv` has no v2 (OD1). |
| Attribution | no `Co-Authored-By` or "Generated with/by" line in the range; 187 commits, all authored Michael Zargham |

## Is the clean model what is evaluated? Yes.

(a) Trace. `definitions.py` `V2` entries name oracle `cubesat-v2` -> `ORACLES` -> `experiments.cubesat_oracle:build` -> `_model_text(experiment)` reads `examples/adcs/model_v2/cubesat.sysml` -> `CubesatOracle(model_text)` -> `connection.load_from_content(model_text, strict=True)`; each chunk appends the configurations to the same text. Measured: sha256 of the text the oracle loads = sha256 of the file = `model_sha256` of `v2-primary@2` = `28dbeeb23cf46c6fb82d0a2ed43c7467592001ae2b71e551d90918725dadd88f`; `oracle.model_text is` the loaded text.

(b) Mutation by me, scratch copies of the model text (not the implementer's bus-mass change), config large wheel, medium tracker, 0.55 m, 90 Wh, Kp 1.8, Kd 1.4. Base: mass 14.3279 kg, power margin 26.095 W, energy balance 21.082 Wh, dod 0.0921. Battery specific energy 140 to 70: mass 14.9707, slew time 12.145 to 12.237, eclipse reserve moves. Housekeeping load 12 to 30 W: margin 8.430, balance -6.720, dod 0.2121. Housekeeping 80 W: margin -36.9, `power_ok` and `dod_ok` flip to False (flags come through the model). Medium tracker mass and accuracy changed: total mass +1.000 kg. Every change moves attributes; identity of the committed outputs is therefore a result, not a reused path. `tests/test_mutation_v2.py` also fails against a stub.

(c) R-2/R-3 grep. `experiments/` and `cubesat_oracle.py` hold no enum literal, range, gain box, scenario number or accounting constant: ranges, gain boxes, enumerations, alternatives and the scenario (30 deg, 600 s, 0.5 s, bands, settling fraction) are read from the model by `ModelReader`. Remaining numbers are algorithm parameters (`_EDGE` 1e-9 slack, `CHUNK` 10, check-design `REACH` 0.35, pool 100000) and the three hand-written candidate design points in `definitions.py`. `feasibility.py` has no ordering comparison: it calls `verify_requirement` on the four named requirements (engine `run`, evidence observed). Ordering comparisons on measured quantities remain only in the measurement definitions `_first_inside`, `_last_outside` and `censored` (band crossing on the simulated error history), none of them a flag.

(d) Still Python: the ODE slew (`adcs_sim.simulate_adcs`, with the non-overridden `BASELINE` ODE parameters), the band-crossing measurement of settling and slew times, the sampler (`LogUniformSampler`, seeded `SeedSequence`), the multiprocess chunking, CSV writing, the ledger, and the check-design flow (fit, holes, pool). The closed-form slew exists as `calc def`s (section 4). The model's section-5 claims restate the accounting over scalar features because the solver cannot translate `calc def` invocations (probe 5).

## Goals, deliverables, requirements

| ID | Verdict | Evidence |
|---|---|---|
| G1, D-1, R-1 | met | one 647-line file, sections 1 to 7 in order; strict load and `self_check` tests pass; negative control passes |
| G2, D-8, R-6, R-8 | met | pin matches all five GitHub release digests and sizes (`gh release view v0.12.0`) and the tag commits (toolkit ab3d590..., stdlib b2f0e9b...); cached binary reports `sysmlv2 0.12.0`. With `SYSML_TOOLKIT_BIN=/nonexistent` and `SYSML_TOOLKIT_CACHE=/nonexistent` in a subprocess the five toolkit tests ERROR at setup, naming the cause and the fetch command (not skipped). Toolkit table: 18 rows, each with a probe number; tests check engine names against `list_engines()` and probe numbers against `probes.py` |
| R-2, R-3, R-4, R-5, R-7 | met | see (c); tests pass; claims and verdicts recorded |
| D-2, G3, R-9, R-10, R-11, R-12 | met | `oracle.py`, `experiment.py`, `ledger.py`, `runner.py` import no SysML tool; `verify` 0 drifts; five adopted and eight generated entries; superseding chain `@2` with parents re-pointed (checks parent `v2-primary@2`, designs parent predictions `@2`); `@2` entries not dirty, commit 2d13465 |
| D-3, R-13, R-14 | met | n=1000, seed 0, 30 deg, 600 s, 0.5 s; predictions entry precedes designs entry |
| D-4, R-15 | met, honest | report states zero differences on this platform as a finding, with tolerances; change register has no rows beyond tolerance, nine "moves no number" rows; the test requires coverage both ways |
| D-5, R-16, G4 | met | three oracles run in the test with differing `evidence_kind`; hedging test present; no forbidden phrase in the new prose |
| OD2 | met | closed-form `calc def`s beside the ODE of record |
| OD3 | met | pinned; CI step and `case` group are by request (z3-solver added) |
| OD4 | met, noted | redesign allowed but none made: v2 is byte-identical, stated in the register |
| OD5, G5, R-17 | met | frozen code and tests untouched (above) |
| Z3 addition | met in part | see gaps B |
| OD1 | **not met in full** | see gap A |
| R-18 | met, with a note | gates pass; three early commits are prefixed "WP15 15.1:" and one "pyproject:" rather than "WP15: " |
| D-7 | partial, as the scope allows | `interface-contract.toml` names `examples/adcs/model_v2/` and `experiments/` and lists the Oracle protocol as a recorded gap ("stated but not yet pinned"); no `data/v2` rows. S-2 follow-up |

Z3 evidence. `exclusion.py` builds `<stem>Sat` and `<stem>Holds` constraint definitions and asks the opensysml `solve` engine (z3). I ran `classify_region` on the probe-record cases: battery 20 to 26 Wh excluded (`unsatisfiable`, proved), battery 29 to 200 all-feasible (`holds`, proved), small wheel at inertia 0.70 to 0.90 excluded; and on new regions: panel 0.30 to 0.31 m all-feasible, battery 20 to 21.5 Wh with tracker 1.2 to 1.5 W excluded (hand check: (12+1.5+0.9) x 0.6 = 8.64 Wh against 0.3 x 21.5 = 6.45), the whole battery range mixed, a large wheel at low inertia all-feasible. The v2 ledger entries carry the `inputs.exclusion` block (claim text, engine, verdict, strength, witness, model hash); the real space gave power all-feasible, battery mixed, nothing excluded. Tests show the solver's verdicts agree with simulated flags.

## Gaps (open decisions)

- **A. OD1 preservation is not delivered (GAP).** The approved outcome includes "both oracles callable through one interface; an experiment definition that runs them side by side". Present: the `adopted-adcs_designs` ledger entry with the note "the legacy oracle of OD1", and the frozen modules and tests unchanged. Absent: an Oracle-protocol wrapper over `design_space.evaluate_design`, any experiment definition running both oracles on a shared configuration subspace, a test, and any mention in `case-model.md` (grep for geostationary, legacy: nothing). Suggested: fix before acceptance (a wrapper, one two-oracle definition on the shared variables, one test, one how-to paragraph); or the supervisor accepts it explicitly as a follow-up.
- **B. Exclusion is partial.** (1) A variant proved infeasible raises `ExcludedVariant` before simulation but writes no ledger entry, so that exclusion is recorded only on the in-memory experiment; (2) the sampler does not consume excluded regions (record only; the real space excludes nothing); (3) `design_space_regions` covers power and battery only (slew energy fixed at zero), not the momentum condition. Suggested: fix (1) before acceptance if cheap; (2) and (3) accept as stated, with the reason that nothing in the declared space is excluded.
- **C. Stale register row.** NC-9 says the v2 entries are `git_dirty` true; the current `@2` entries are clean. Fix the sentence (hand-written file, no test).
- **D. NC-5 workaround.** The analysis is called a second time with the slew time one float step higher to avoid a runtime uniqueness error. Accept with reason: no computed attribute depends on it; recorded.
- **E. Identity holds on one platform.** Cross-platform is WP16's evidence. Accept.
- **F. Commit prefixes and D-7 rows.** Accept with reason (history; the contract records the gap).

## Addendum (PM)

Gap D was the stale NC-5 text; at HEAD the model returns no equal-valued entries and the oracle makes one analysis call; corrected in 90b1204; gap A, B(1), C closed in 33a249b, e50d1e2, 90b1204; B(2) closed in the commit that adds `runner.ExcludingSampler` (WP15: the sampler consumes excluded regions; see `git log -S ExcludingSampler`); B(3) momentum condition outside what the solver can represent, stated in `examples/adcs/case-model.md`.

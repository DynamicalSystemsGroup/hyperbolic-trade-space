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

## Scope approval (approval gate)

- pending (OD2 to OD5, the defaults as one item, then approval)

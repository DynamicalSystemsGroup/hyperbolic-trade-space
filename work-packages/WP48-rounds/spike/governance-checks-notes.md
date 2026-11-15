# WP48 D-2: the Open-MBEE governance-checks repository, read

Read 2026-11-14 from shallow clones: `https://github.com/Open-MBEE/governance-checks.git` at commit
`82e54c0e1bd40e2871648867357c1bc002683627` (2026-11-12) and, for the engine it depends on,
`https://github.com/Open-MBEE/OpenSysML.git` at `97e7eedb29a45828420a0d9761823323481e5fed` (2026-11-14); the package
metadata at `https://pypi.org/pypi/opensysml/json` (opensysml 0.12.1, licence expression Apache-2.0). Files read in
full: `README.md`, `.github/workflows/check.yml`, `requirements.txt`, `repos.yaml` (head), `LICENSE`, `SECURITY.md`;
`model/governance.sysml` and `model/repositories.sysml` in part; `check.py` and `sense.py` by structure and head, not
every line (`common.py`, `model.py` and the 19 tests only listed).

## Correction to the first pass

The first pass said the phrase "verification case" does not appear and that governance-checks uses `verify_satisfaction`
only. Reading the files: the repository does not use a `verification def` either, but it does state each check as a
SysML v2 `requirement def` with `assume constraint` and `require constraint`, binds one `satisfy requirement ... by`
per repository and check, and asks the engine for `verify_satisfaction()` (README "How it works"; `check.py:83`). That
is the satisfaction half of SysML v2 verification, one level below a `verification def`. This repository's own case
model already goes one step further: `examples/adcs/model_v2/cubesat.sysml` section 5 declares `verification def
ConfigurationVerification` and `SlewVerification` with `subject c : Cubesat; objective { verify requirement ...; }`
(lines 1033 to 1066 at dev `070cc54`), and `tests/test_system_model_v2.py` calls `verify_requirement` and
`verify_satisfaction` on it. So the supervisor's "verification cases" already has a house meaning here.

## What it checks and how

Purpose (README): measures Open-MBEE repositories against the repo-registry policies; "the stopgap" until the registry
reports compliance itself, then "this repository retires". Four stages:

1. `model/governance.sysml`, hand-written, 407 lines, 35 `requirement def`s in 17 policy packages named after the
   registry's check IDs (for example `Policies::HistoryProtection::NoForcePush`). Each has `subject repo : Repository`,
   an `assume constraint inEffect` (the policy's applicability by type and stage), and a `require constraint` over a
   fact attribute (`repo.forcePushBlocked`). Deadlines (14, 60, 365 days) and the semver regular expression and SBOM
   globs live in the model, so the sensors carry none.
2. `model.py` generates `model/repositories.sysml` from `repos.yaml` (one part per repository, one `satisfy` per check);
   CI fails if the committed file is stale (`model.py --check`).
3. `sense.py` reads facts through `gh api` and GraphQL, one sensor per check, returning counts, flags, strings, ages in
   days, never verdicts; a fact the token cannot read is left out and reported unreadable.
4. `check.py` binds the facts into the model (`import_data`) and calls `verify_satisfaction()` through the `opensysml`
   Python client, mapping `holds`, `violated`, `undecided` to pass, fail, unreadable, plus `exception`, `attested`,
   `unattested`, `n/a`, `unimplemented`.

Outputs: a table per repository in the job summary, `summary.md`, `results.json` (uploaded as an artifact). Exit code
1 only when a check that passed in `baseline.json` no longer does (an unreadable counts), so known open items stay
visible without turning every run red.

## How it runs

`.github/workflows/check.yml` (workflow `governance`): triggers Monday 06:17 UTC, manual dispatch, any pull request, and
pushes to `develop` and `main`; jobs `unit` (pytest, 19 tests) then `measure`. Top-level `permissions: {}`, `contents:
read` per job, every action pinned to a commit SHA, checkout with `persist-credentials: false`. The scheduled run reads
with the secret `GOVERNANCE_TOKEN` (fine-grained: Administration, Code scanning alerts, Dependabot alerts, Metadata,
Contents, all read; Members: read for org checks); pull requests get only the job token and skip the baseline, "they
prove the script runs, not the repositories' state". Not reusable: no `workflow_call`, no composite action.

## Licence and what can be reused

- Repository licence: Apache-2.0 (`LICENSE`, read 2026-11-14), appendix copyright line left as the template; no `NOTICE`
  file. Reuse with the licence text and a statement of changes is permitted.
- Engine licence: `opensysml` is Apache-2.0 (PyPI, 2026-11-14), and this repository already installs it (`pyproject.toml`
  `case = ["opensysml>=0.12.1", "z3-solver>=4.13"]`, the group the case-model tests use and the test workflow caches).
  The first pass's open question (availability and licence of the engine) is closed: it is already a dependency.
  OpenSysML also ships a GitHub Action (`action.yml`, "OpenSysML validate") that runs `sysml -validate` and reports
  SARIF, JUnit XML or JSON; not read beyond its inputs.

| Part | Reusable here? |
|---|---|
| The pattern: facts sensed apart from the verdict, verdict stated in the model | Yes, as design; the best single idea |
| `requirement def` per check with `assume` and `require constraint`, `satisfy ... by` binding, `verify_satisfaction()` | Yes, directly: same engine, same client, already in the dependency group |
| `sense.py` endpoint recipes (rules, protection, releases, community profile, Dependabot, workflow permissions) | Yes, as code to adapt; they target `Open-MBEE` full names and a `Registry` object, so each would be adapted to one repository's name and facts |
| Baseline-regression exit logic (`regressions`, 14 lines) | Yes, small; useful once checks fail on purpose |
| `check.yml` workflow shape: SHA pins, empty top-level permissions, summary table, artifact upload | Yes as a template; to be called from the release workflow rather than on its own schedule |
| `repos.yaml`, `registry.ref`, `model.py`, the registry fixtures, the organisation-level and maintainers checks | No: they serve an organisation of 182 repositories and a registry data layout this repository does not have |

## What it does not do

It reads no repository's files for content (attested checks pass when a link resolves: "nothing reads what the file
says", README), signs nothing, and runs no check inside a release; it is an after-the-fact audit of settings.

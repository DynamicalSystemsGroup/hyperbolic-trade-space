# WP54 review: the paper's skeleton

Branch `wp54`, from `dev` at `432ae4f`. Scope: `WP54-scope-of-work.md`; his words: `WP54-decisions.md`.

## What changed

- The section "Search of the design space (preliminary)" is gone (cell `sec-search`; label `sect-search` retired).
- "Reproducibility and your own case" (`sect-reproducibility` retired) and "Acknowledgments and process" are one section,
  "AI acknowledgement and Reproducibility" (label `sect-process` kept, cell `acknowledgments`).
- "Future work and final remark" is "Future work" (label `sect-future` kept, cell `sec-future`), written fresh.
- The roadmap paragraph of Section 1 lost the search sentence and ends: Section 9 discusses interpretation and limits,
  Section 10 gives future work, Section 11 closes with the use of AI assistance and the reproduction of every result.
  The sections are 1 The decision problem, 2 Prior art, 3 Preliminaries and notation, 4 Definitions, 5 Methods, 6 Results,
  7 Case construction, 8 Case analysis, 9 Discussion, 10 Future work, 11 AI acknowledgement and Reproducibility, then
  Works cited.
- Hard-coded section numbers in generated sentences follow the renumbering (Case construction 8 to 7, Case analysis 9 to 8):
  `paper/generate_findings.py`, `paper/generate_results.py`; the committed outputs of both notebooks were regenerated.
- `docs/bridge.md`: both pointers go to `paper:sect-future` (the search direction of Future work).
- `paper/supporting_material.ipynb`, Appendix F's job block: its `numref` to `sect-reproducibility` goes to `sect-process`.
- `paper/BROWSER_NOTES.md`: the heading note names the new section.
- `work-packages/review/open-questions.md` created (OQ-1 to OQ-4).

## Word counts (the counter of `tests/test_paper.py`, `words_by_section`)

| Section | Words | Limit |
|---|---|---|
| Future work | 233 | under 250 |
| AI acknowledgement and Reproducibility | 150 | under 200 |

Length ledger: baseline entries added at 0 for the two new sections; one `[[raise]]` row each (233 and 150); one `[[cut]]`
row for each of the four sections that left (304, 182, 190 and 73, each ceiling taken to zero).

## Old sentences and their fate

### Old Section 7, "Search of the design space (preliminary)"

| Sentence (opening words) | Fate | Record behind the new sentence |
|---|---|---|
| "A trade study also decides what to evaluate next, today by expert intuition or exhaustive sampling." | cut (framing; no record, a general claim) | |
| "The fitted terms say where better is, so sampling can be trade-off aware." | cut (framing) | |
| "The method assumes nothing about how a table's designs were drawn ..." | to the open-questions file, OQ-4 | `length_ledger.toml` raise row of 2026-11-11 |
| "This section is future work with no results, and it stops short of selecting a design ..." | cut (the section is now a direction under Future work) | |
| "A configuration chosen for a chart point is a **proposal** ..." | kept in Future work, direction 1, sentence 1 (reworded) | `WP41-rounds/spike/readout.md` section 1; C910 |
| "A **selection rule** picks one of the many configurations predicted near a point." | kept inside the same sentence | C910, glossary `selection-rule` |
| "A move along the ascent direction is a Pareto improvement of the prediction; a design built to reach it need not follow; the **check** finds out." | cut; the check survives as "built and measured" in sentence 1 and as "its check" in sentence 3 | WP41 readout section 1 |
| "The inner loop identifies, fitting the terms to the current table." | cut (the fit is Section 5's) | |
| "The middle loop proposes. On each term the normal is an ascent direction ... chained back through the conditioning and the evaluation ..." | kept in Future work, direction 1, sentence 2 (shortened to "Ascent directions chained back ... steer the proposals") | WP41 readout section 1; C911 |
| "A categorical variable is a finite comparison." | cut (no record in the spikes) | |
| "The outer loop evaluates the proposals, appends them to the table, refits, and repeats until the supporting envelope stops moving ..." | kept in sentence 2 ("an outer loop evaluates them, appends the rows and refits"); the stopping clause cut | WP41 readout section 1: "The outer loop is the refit" |
| "Ascent may reach only the log-convex part of the Pareto boundary." | to the open-questions file, OQ-3 | WP41 readout sections 3 and 5 |
| "**Open.** The loop may move inward on a step." | to the open-questions file, OQ-1 | `WP36-decisions.md`, 2026-11-14 12:20 |
| "The conjecture is a submartingale property ..." | to the open-questions file, OQ-1 (C675 retired) | same |
| "The theory treats variables as continuous within a category." | cut here; stated in Methods | |
| "A convergence theorem for the nested scheme is a goal, and the scheme motivates the kernel direction of Section 12." | to the open-questions file, OQ-2; the kernel direction stays in the Discussion (WP56) | WP36-decisions.md; WP43 spike |

### Old "Future work and final remark"

| Sentence (opening words) | Fate | Record behind the new sentence |
|---|---|---|
| "Beyond one term, K > 1 is built; beyond sharp weights, a nonsmooth search ..." | cut; K > 1 built is the "several-term fit" of the opening paragraph; sharp weights are Methods' assumption | |
| "Beyond the analyst's K, selection rules." | cut (the selection rule is in direction 1) | |
| "Beyond small K, scalability and speed, and a global search or certificate for the alternation (Q1)." | cut; Q1 is in Results' open list and the gaps ledger | |
| "Beyond log-affine conditioning, kernels that keep the model a GGP ..." | cut here; the kernel direction is the Discussion's (WP56) | WP43 spike |
| "Beyond continuous variables within a category, discrete design variables." | cut (not a thrust of the abstract; a limit, Appendix E) | |
| "Beyond a log-convex surface, the detection of dents and disconnected regions." | cut (not a thrust of the abstract) | |
| "Beyond illustrative hardware values, datasheet values." | cut (a limit of the case, Appendix C) | |
| "Beyond pencil-and-paper checks, the Lean theorem prover, starting with the log-mean-exp bounds and the convexity of the fit's loss." | kept, direction 3, sentence 1 (reworded; C564 retired, C915 added) | WP36 decision (placement (a)) |
| "A proof over the reals backs the mathematics, not the floating-point computation, which the certificates check." | kept in the same sentence, without the certificate clause (C565 retired) | WP36 readout |
| "Beyond Python, a Rust core compiled to WebAssembly, whose verification tools address crashes and overflow, not numerical accuracy." | kept, direction 3, sentence 2 (C566 retired, C916 added) | WP36 decision |
| "**Final remark.** A forecast V for a new capability ..." | cut (the agent's default: an aside, not a result or a direction; one line restores it) | |

New to Future work: the opening paragraph (the release's accomplishments: C909); direction 2, holes (C913, C914; WP50
readout, "The boundary", the suggested sentence and "What the next release builds"; the topology library choice left open in
one clause, the licence difference not stated); direction 3, sentence 3, governance checks as the gates (C917; WP48
readout section 5, "May say now"); direction 1, sentence 3, the next release scopes the proposal and its check (C912; WP41
readout section 4). The body names no SysML, as the paper's tool-agnostic rule holds, so the gates are "requirements with
verification cases".

### Old "Reproducibility and your own case"

| Sentence | Fate |
|---|---|
| "Every figure, table and reported number comes from a call into a tested module." | kept in the closing section, paragraph 3 |
| "Appendix F gives the pinned toolchain, the environment of record, the commands and one row per item." | kept as "The pinned toolchain, the environment of record and the commands are in Appendix F." (subject no longer the appendix) |
| "To run your own table, supply configurations, attributes and a conditioning rule, and use the same calls." | kept, with "the" and "make the same calls" (C124 retired, C921 added) |
| "The docsite's Getting started page is where to begin." | kept in the same sentence (C125 retired) |

### Old "Acknowledgments and process"

| Sentence | Fate |
|---|---|
| "Work was done in supervisor-gated work packages: a written scope ..." | kept, paragraph 1 (C129 retired, C918 added) |
| "AI coding assistance (Claude Code, Anthropic) drafted code, derivation scripts and text inside those packages, in a process modelled on the harness described in [@zargham2026incose]." | kept, paragraph 1, in one sentence with the first (C130 retired); the citation key `zargham2026incose` resolves in `docs/references.bib` |
| "Its deterministic checks and named human approver are the verification mechanism this paper inherits." | cut (the claim that no claim enters without a backing says it with a test) |
| "The derivations are machine-checked." | cut and replaced by "scripted checks in place of pencil and paper" (C920; `proof-conventions.md`) |
| "The author takes responsibility." | kept, paragraph 1 |

New: "No claim enters without a lemma step, a generated value, a test or a verified source" (C919; the claims register's rule,
`claims-review.md`); the proof map sentence (the proof map is checked by `tests/test_proof_map.py`).

## Register

- Retired: C108, C124, C125, C126, C127, C129, C130, C564, C565, C566, C675, C820, C821, C822 (fourteen; their fragments left
  the paper, and the three of the search section whose content survives, C820 to C822, are replaced by C910 and C911).
- Added: C909 to C921 (thirteen): C909 to C917 under Future work, C918 to C921 under AI acknowledgement and Reproducibility.
- Ids are append-only; the retired ids are not reused.

## Tests changed

`tests/test_paper.py`: the section list; the two tests of the preliminary search section replaced by
`test_no_section_is_preliminary_or_a_remark` and `test_future_work_is_short_and_names_the_three_thrusts_in_the_abstracts_order`;
a new `test_closing_section_is_short_and_calls_the_derivations_scripted_checks`; the roadmap test's label list; the
disclosure test and the "machine-checked" assertion (now its absence); the assumptions test no longer reads Future work for
the Beyond-markers; two search-section assertions of the C-1 test dropped with the text; one id anchor
(`sec-search` to `sec-case-construction`).

## Checks

| Check | Result (last line) |
|---|---|
| `uv run --frozen python paper/execute_notebooks.py` | exit 0 (30 min); committed outputs of both notebooks regenerated |
| `uv run --frozen mkdocs build -q` | exit 0 |
| `cd paper && BASE_URL=/paper myst build --html` | exit 0; no warning about a missing label or figure; one warning, `Duplicate identifier in file "fig-tension-matrix"`, present on `dev` as well (eight occurrences of the id before and after) |
| `scripts/check_residuals.py` | exit 0 |
| `scripts/check_vocabulary.py` | `0 new violation(s), 67 known` |
| `ruff check .` / `ruff format --check .` | `All checks passed!` / `1034 files already formatted` |
| `uv lock --check` | `Resolved 194 packages` |
| fast suite, `-m "not slow"` | `2085 passed, 17 skipped, 505 deselected, 2 xfailed` |
| slow paper tests, `-m slow tests/test_paper.py` | `27 passed, 207 deselected` |
| `grep sect-search, sect-reproducibility` in paper, docs, tests | no match left except retired-label mentions in this file and the ledger text |

## Red, or not done

- The rendered pages were not looked at in a browser by this unit; the checks above are builds and tests. The soft-confirm
  on screenshots of the two sections is the driver's.
- The duplicate `fig-tension-matrix` identifier is older than this package and is left.
- The internal note `notes/user-journeys.md` still cites old section numbers (8 to 11, "Reproducibility
  and your own case"); it is a historical note and was not edited.

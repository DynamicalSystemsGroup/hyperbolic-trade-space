# The second regime renamed: "baseline regime"

The supervisor's decision (`work-packages/WP56-decisions.md`, "The supervisor, on the second regime's name"): the
second regime of the case is the baseline regime. Section 7 defines the two regimes by the sampled range of the
proportional gain (Kp from 0.2 to 2, aggressive, the primary regime; Kp from 0.03 to 1, the stock gains, the
baseline regime). Only the regime's name changed. "Stock" where it names the gains ("stock gains", "the stock gain
box"), the dataset identifier `cubesat-stock`, the CaseSpec key `stock` and code identifiers (`study_stock`,
`load_study("stock")`, the stability keys `... | stock | ...`) stay.

## Files, before and after

Lines naming the regime by the old name (`stock regime`, `stock-regime`, `stock-gain regime`, `stock (baseline)
regime`, `stock set`, `stock preview`, `the stock K = 3`), `git grep -ci` on dev and on the branch:

| File | dev | rename |
|---|---|---|
| `paper/paper.ipynb` (source and outputs) | 10 | 0 |
| `paper/supporting_material.ipynb` (source and outputs) | 7 | 0 |
| `paper/generate_findings.py` | 3 | 0 |
| `paper/generate_model.py` | 1 | 0 |
| `paper/generate_supplement.py` | 2 | 0 |
| `paper/supplement/metric-associations.md` (regenerated) | 3 | 0 |
| `paper/length_ledger.toml` | 3 | 0 |
| `paper/environment_values.toml` | 1 | 0 |
| `paper/container/RECORD.md` | 2 | 0 |
| `claims_register.toml` | 4 | 0 |
| `docs/examples.md` | 1 | 0 |
| `docs/superpowers/notes/notation.md` | 1 | 0 |
| `tests/test_paper.py` | 8 | 0 |
| `tests/test_docs.py` | 1 | 0 |
| `docs/superpowers/notes/paper-sources/method.md` | 2 | 2 (left: a verbatim snapshot, see below) |
| `examples/adcs/spikes/fleet_performance.py` | 1 | 1 (left: outside the listed scope) |
| `tests/test_adcs_enrichment.py` | 1 | 1 (left: outside the listed scope) |

Labels that printed the CaseSpec key `stock` where the paper names the regime now print `baseline`, through
`case.regime_word`, which now also takes a key: D's regime-comparison table header (`| quantity | primary |
baseline |`), D.11's moving-quantity rows (`margin, K = 2, baseline`, ...), the one-axis sentence of C.5, D.3 and
D.4 (`baseline regime: energy balance and available power`), the regime sentence of Section 7 (`the primary set lies
inside the baseline set ... The baseline set spans ... mass enters only in the baseline regime`), the "Two terms"
sentence (`the primary regime and the baseline regime`), and the docs page's two printed blocks
(`docs/examples.md`, `DOCS_LABELS` in `tests/test_case.py`). The short regime labels in four register notes
(`(stock)`) read `(baseline)`.

## Rewordings

One, in the sentence that defines the regimes (`paper/paper.ipynb`, cell `sec-case-construction-1b`; claim C663
quotes it):

- before: "the proportional gain $K_p$ from 0.2 to 2 in the aggressive (primary) regime and from 0.03 to 1 in the
  stock (baseline) regime"
- after: "the proportional gain $K_p$ from 0.2 to 2 in the aggressive (primary) regime and from 0.03 to 1 in the
  baseline regime"

The gloss "(baseline)" became the name, so the parenthesis went. No other sentence changed beyond the name.

## The glossary entry

```yaml
  - id: 'baseline-regime'
    term: 'baseline regime'
    short: 'The second regime of the case: the designs drawn with the proportional gain Kp from 0.03 to 1 (the stock gains), dataset cubesat-stock.'
    register: 'baseline regime'
    formal: 'the data of record whose gains are sampled from the stock gain box, Kp from 0.03 to 1; dataset identifier cubesat-stock (the CaseSpec key stock)'
    not: 'the primary regime (aggressive gains, Kp from 0.2 to 2), the baseline configuration (one design of the SysML v2 model), or a term of the fit'
    defined_in: 'Section 7, Case construction; examples/adcs/case.py (CaseSpec.regimes, regime_word)'
    aliases:
      - 'baseline regimes'
    avoid:
      - phrase: 'stock regime'
        reason: 'the supervisor named the second regime the baseline regime (WP56-decisions.md); one object, one name; the identifier cubesat-stock and the key stock stay in the data'
```

The glossary had no entry for the primary regime or the stock regime. The `avoid` row makes the vocabulary check
fail on the old name. The entry also appears in the supporting material's register table.

## Checks

| Check | Exit | Result |
|---|---|---|
| `uv run ruff check .` | 0 | |
| `uv run ruff format --check .` | 0 | 625 files formatted |
| `uv lock --check` | 0 | |
| `uv run python scripts/check_vocabulary.py` | 0 | 0 new violations, 67 known |
| `uv run python scripts/check_residuals.py --compare scripts/residuals_baseline.json --strict` | 1 | 1 on dev too; see below |
| `uv run python -m derivation.proofmap` | 0 | 22 lemma files, 549 steps |
| `uv run pytest -q tests/test_claims_register.py` | 0 | 21 passed |
| `uv run python paper/generate_supplement.py --check` | 0 | `metric-associations.md` regenerated |
| `uv run pytest -q -m "not slow" -n auto` (with `MPLCONFIGDIR`) | 0 | 2,090 passed, 18 skipped, 2 xfailed |
| `uv run pytest -q -m slow -n auto tests/test_paper.py tests/test_case.py::test_docstrings_run_and_are_numpydoc` | 0 | 31 passed (14 min) |
| `uv run pytest -q tests/test_case.py::test_the_docs_design_sets_block_is_the_case_modules` (slow) | 0 | 1 passed |
| `uv run mkdocs build -q` | 0 | only the theme's end-of-life banner |
| `BASE_URL=/paper uv run --frozen myst build --html` | 0 | no warnings or errors |

The first run of the not-slow suite without `MPLCONFIGDIR` failed four plotting tests and errored three on "Failed
to find font DejaVu Sans" (a font-cache race in a fresh environment); with `MPLCONFIGDIR` set all passed. dev
reports 2,091 passed; the 18 skips here are environment conditions (`PAPER_EXECUTE`, `PAPER_BUILD`, an archive not
fetched), none a failure.

Residuals against dev (the same script run on a detached checkout of dev): both notebooks are at or below dev on
every residual count (Section 7 "case-construction" parentheses 35 to 34, words 1,378 to 1,377); their
"terms met" column rises by one each (61 to 62, 46 to 47) because the new entry is a glossary term the prose uses,
and their "undefined at first use" is unchanged (20, 16). Outside the notebooks: `glossary/long-forms` parentheses
57 to 61 (the entry's own four), `docs/examples.md` and `examples/adcs/case-model.md` terms undefined at first use
each up by one (the new term met there before a definition).

No stability baseline changed: `stability_extra.json` and the sensitivity report key the regimes by the CaseSpec key,
and no recorded sentence text carries the name.

## The remaining "the stock" (paths `paper docs examples tests glossary.yaml claims_register.toml src`)

| Line | Names |
|---|---|
| `glossary.yaml:829` "(the stock gains)" | the gains |
| `glossary.yaml:831` "the stock gain box" | the gains |
| `paper/supporting_material.ipynb:506, 579, 582` (the register table's copy of the entry) | the gains |
| `docs/superpowers/notes/adcs-tensions-probe.md:767` "at the stock gains" | the gains |
| `tests/test_adcs_enrichment.py:301` "at the stock gains" | the gains |
| `examples/adcs/spikes/fleet_performance.py:351` "the stock-gain regime" | the regime (left, outside scope) |
| `docs/superpowers/notes/paper-sources/method.md:967, 968` "the stock regime" | the regime (left, snapshot) |

## Left for the driver

1. `docs/superpowers/notes/paper-sources/method.md` lines 967 and 968 say "stock regime". The file is a verbatim
   snapshot (`tests/test_paper_sources.py`; `notation.md`: "a snapshot is not edited"), so it was not edited, and the
   grep the scope asked to be empty finds these two lines. Edit the snapshot or accept the two lines.
2. The comments in `examples/adcs/spikes/fleet_performance.py:351` ("the stock-gain regime") and
   `tests/test_adcs_enrichment.py:74` ("stock-gain regime") lie outside the listed files.
3. `docs/examples.md:17` "The stock-gains table" names the table by its gains and was kept; `paper/container/RECORD.md:270`
   "(primary and stock, K = 2 and 3)" sits beside the test ids `[stock]` and was kept.
4. "Baseline" now names two objects of the case, the baseline regime and the baseline configuration; the entry's
   `not` field separates them, and the prose already wrote "the baseline regime (stock gains)" in D.19.

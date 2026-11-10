# WP23 round 4: the views by the round-3 dispositions, the pair on round 1's data

This folder holds round 4 of the model-realism loop (D-6): the two views of the model (`INTENT.md`
states what each should say and what changed; `assembly_caption.md` is the assembly view's levels
and ranges, written by the generator from the model), the coverage table (`coverage.md`, copied
from `examples/adcs/model_v2/views/`), the K = 1 exponent heatmap across tau (`heatmap.png`, the
primary regime; `heatmap_baseline.png`, the baseline regime) and the K = 1 and K = 3 record
(`k3_record.md`).

## The round's model and data

- Model: `examples/adcs/model_v2/cubesat_r2.sysml` as round 2 left it; rounds 3 and 4 changed no
  element of it (`WP23-review.md`, "Round 3: the three metrics that never bind", "Round 4").
- Data: the two tables of round 1, used as they are
  (`work-packages/WP23-rounds/round-1/README.md`: `adcs_designs_cubesat_gains.csv` sha256
  `336288e57a23...`, `adcs_designs_cubesat.csv` `4cb65a2ffde1...`, full hashes in that folder's
  `generation-ledger.jsonl`). No regeneration was run in rounds 2 to 4: the part of the model the
  datasets face (the configuration space, the oracle's inputs, the metric columns) did not change
  in those rounds; round 2 added two calcs and a requirement that no column reads, and rounds 3
  and 4 changed the views and the records only.
- The fit: `examples/adcs/case.py` at `dev`, unchanged, with its defaults (target fraction above
  V = 1 0.10, temperature bounds 3 to 1000, seed 0; the temperature re-selected at each K).

## How the folder was generated

From the worktree of the round (branch `wp23r4` on `dev`), with the round-1 tables in the session
scratch at `$R`:

```
uv run python docs/superpowers/notes/spike-sysml-diagrams/project.py \
  examples/adcs/model_v2/cubesat_r2.sysml work-packages/WP23-rounds/round-4 --revision 5
cd work-packages/WP23-rounds/round-4 && for f in assembly_view.puml behavioural_view.puml; do
  sh ../../../docs/superpowers/notes/spike-sysml-diagrams/render.sh $f; done
uv run python examples/adcs/model_v2/diagnostic_pair.py \
  --dataset $R/adcs_designs_cubesat.csv --gains $R/adcs_designs_cubesat_gains.csv \
  --coverage examples/adcs/model_v2/views/coverage.csv --out work-packages/WP23-rounds/round-4
```

The pair ran in 50 s. Its record differs from round 3's `k3_record.md` in one line, the heading of
the second regime ("baseline regime" for "stock regime"); every number is the same, as it must be
on the same data and the same fit. The generator's revision 4 still reproduces round 3's PlantUML
text byte for byte, and its default revision the committed views of the adopted model
(`tests/test_system_model_v2_r1.py`).

## The metrics at zero exponent across tau (unchanged since round 1)

| Regime | At zero (at most 1e-3 at every one of the thirteen temperatures) |
|---|---|
| primary (aggressive gain box) | power margin, eclipse reserve, peak slew power |
| baseline (baseline gain box) | peak slew power |

The reading of each zero is round 3's (`WP23-review.md`, "The n-lemma reading of each zero
exponent").

# Rerun record (R-2)

Run from a clean state on the machine of the first run: `results/`, `figures/` and `cache/` removed, then
`uv run --with cvxpy python work-packages/WP43-rounds/spike/run.py all` (2554 s; `all` now includes the `lqm` stage and
the monotonicity diagnostic, a change to `run.py` only). The regenerated files were compared with the committed ones.

**Same, byte for byte:** `environment.txt`, `lq_monotone.md`, `plane_*.json`, `planted_summary.md`,
`planted_recovery.csv`, `real_summary.md`, `real_verdicts.json`. No verdict changed.

**The three figures (`plane_primary.png`, `plane_stock.png`, `dent.png`): same data, not the same bytes.** A third
run on 2026-11-14 (2,546 s, the same environment, after the lint pass on the scripts) regenerated them with about
8 percent of pixels differing in `dent.png` and 18 percent in the two plane figures, in the placement of text; the
scripts as committed before the lint pass produce the same new bytes, so the difference is the renderer's state and not
the code, and the JSON and CSV files the figures are drawn from are unchanged. The committed figures are kept; a reader
who regenerates them should expect the layout to shift by a few pixels and the content not to.

**Differ, in wall-clock columns only:** `planted_fits.csv`, `real_fits.csv`, `real_fits_lqm.csv` (`t_fit`, `t_select`,
`t_wall`) and `times.csv`, `times_summary.md` (all columns are times). Every other column of the four CSVs is identical
(maximum absolute difference 0.0 over the numeric columns; text columns equal). The cause is that fit times depend on the
load of the machine. The committed times are kept, as the readout cites them.

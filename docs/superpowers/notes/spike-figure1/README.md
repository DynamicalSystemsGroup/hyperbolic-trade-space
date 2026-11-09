# Figure 1 schematics (design spike, throwaway)

Three conceptual candidates for the paper's hero image, drawn from one synthetic d = 2, K = 3
world (`W`, `BETA` at the top of `make_schematics.py`). Colours come from
`hyperbolic_trade_space.plotting` (`CATEGORY_COLORS` per facet, `FRONTIER_COLOR` for V = 1).
Nothing here touches the repository.

## Regenerate

From the repository root (uv only):

    uv run python /private/tmp/claude-501/-Users-z--claude-spares-spare-4Zb8mW/71474a52-35d3-48fa-82b0-c1328e96b5d6/scratchpad/figure1-schematics/make_schematics.py

Optionally `--out DIR` to write elsewhere. Outputs: `S1.png`, `S2.png`, `S3.png` (1600 px wide,
150 dpi), `S4.png` (the three-pane combination of S1 and S3, 2400 px wide, finite-kappa rounded
envelope with a few designs beyond V = 1) and the `@2x` versions of each (300 dpi). Deterministic (`numpy`
`default_rng(20261108)` per figure).

## View

Open `index.html` in this folder (served at http://127.0.0.1:8765/figure1-schematics/index.html
when the parent folder's `python -m http.server 8765` is running).

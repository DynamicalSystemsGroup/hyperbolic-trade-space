# Spike: HoroPCA beside the posynomial invariant form (WP35 stage 1)

Readout: `work-packages/WP35-rounds/spike/readout.md`. Nothing here enters the package, `pyproject.toml` or `uv.lock`.

Reproduce (the HoroPCA clone and its venv live outside the repository; commit `c9a99967a62688711f6b63dab3baee53fe2d8430`
of https://github.com/HazyResearch/HoroPCA, no licence file):

1. `uv run python docs/superpowers/notes/spike-horopca/make_tables.py` (repository environment) writes `tables.npz`.
2. `uv venv <dir> --python 3.12 && uv pip install --python <dir>/bin/python torch numpy scipy networkx scikit-learn pandas`
   (recorded: torch 2.15.0, numpy 2.5.4, scipy 1.18.1, networkx 3.7, scikit-learn 1.9.1), then
   `git clone https://github.com/HazyResearch/HoroPCA <clone> && git -C <clone> checkout c9a9996`.
3. `<dir>/bin/python run_horopca.py <clone> tables.npz results.json` (about half an hour on CPU: the repository's
   variance objective is O(n^2 d) per step); `python analyze.py tables.npz results.json > analysis.txt`;
   `python gromov.py <clone> tables.npz`; from inside `<clone>`: `python <this folder>/run_main.py <clone> --dataset smalltree
   --model horopca --dim 10 --n-components 2 --n-runs 3` (the authors' own CLI under the one shim in `compat.py`).
4. `uv run pytest docs/superpowers/notes/spike-horopca/test_spike_results.py` needs only `results.json`.

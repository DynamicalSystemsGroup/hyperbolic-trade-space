# WP40 D-8: what the notebook unit edits (not done in this build)

At the build's start head `94cb6a1`. Nothing under `paper/*.ipynb` or `docs/superpowers/notes/abstraction-gaps.md` is
edited by the thinning build; the one unit below goes through the paper notebook's single-writer queue.

- Note: `docs/superpowers/notes/abstraction-gaps.md`, lines 33 (G-7), 34 (G-8), 36 (G-10) and 41 (G-15): the paths
  `docs/superpowers/notes/spike-objective/` and `docs/superpowers/notes/spike-certificates/` become
  `work-packages/spikes/spike-objective/` and `work-packages/spikes/spike-certificates/` (the folders moved by
  `moves.md`).
- Notebook: `paper/supporting_material.ipynb`, one cell, index 87, id `tab-E-gaps` (Appendix E, the gaps table; code
  cell `from generate_gaps import gaps_table; gaps_table()`). Its source needs no edit; its stored outputs (HTML and
  Markdown renderings, lines 12547, 12555, 12571, 12611, 12650, 12651, 12653, 12658 and 12664 at `94cb6a1`) carry the
  four paths above and are regenerated from the edited note; nine lines, 21 occurrences.
- `paper/paper.ipynb`: no cell names a moved path (0 hits).
- Commit with the notebooks and `paper/figures/` together, as the scope says; the paper-sources notes
  `limitations.md` and `method.md` were edited in this build (their prose cites the same folder).

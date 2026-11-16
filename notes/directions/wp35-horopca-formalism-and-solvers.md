# WP35: how HoroPCA's formalism and solver differ from this work's

Appendix H.5 of the supporting material until WP57d (the text as it stood:
`git show 2db089d5:paper/supporting_material.ipynb`, cell `app-H-5`); Appendix H.4 cites this note in one line.
The experiment's record is `work-packages/WP35-rounds/spike-h/`. The paper's register of prior art carries the same
contrast in HoroPCA's "differs" field (`paper/prior_art.yaml`, Appendix G).

HoroPCA optimizes a frame, k orthonormal directions, so that points projected along horospheres (the curved
counterparts of hyperplanes in flat space) keep the most variance. That loss is not convex: the authors' code runs Adam
from random starts, and nothing bounds how far its loss is from the best frame's. This work minimizes a soft maximum
(log-mean-exp) of weighted log-metrics over the simplex, which for one term is convex, and returns a gap bounding the
result's shortfall from the best value.

Sources: the paper (Chami, Gu, Nguyen and Ré 2021, `docs/references.bib` key `chami2021horopca`; its loss); the
authors' repository at commit c9a9996 (Adam, random starts); `src/hyperbolic_trade_space/solvers.py`;
`derivation/lemma_04_convexity.py`. The readout that read the authors' code is
`work-packages/WP35-rounds/spike-h/readout.md`, section 5.

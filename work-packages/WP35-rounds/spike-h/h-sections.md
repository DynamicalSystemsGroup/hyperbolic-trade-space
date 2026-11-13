# Appendix H, draft for the notebook unit (WP35, amendment 1)

Written by the build unit for `paper/supporting_material.ipynb`. Not part of the paper's record by itself: the notebook unit
pastes the cells below, in order, after the last cell of Appendix G (`tab-G-reading_pass_table`), re-executes, and the
register rows staged in `h-claims-rows.toml` go into `claims_register.toml` in the same commit. Each block starts
with a line `=== id | type` (`markdown`, or `code` for a generated cell, whose whole source is the one call shown).
Generated cells import from `generate_prior_art`; every number that comes from the record is in a generated cell or in
the table; the design constants of H.2 are those of `hypothesis.md` at 830cf54 and are pinned by a test.

Count by the visible-prose rule (`rendered_words` of `tests/test_paper.py`: Markdown, the caption and the generated
sentences expanded; the table not counted): 886 words, ceiling 900 (`length_ledger.toml`, "Appendix H"). A connecting
phrase may change; the total may not pass 900 (`test_appendix_h_is_within_its_ledger_ceiling`).

## Placement list for the notebook unit

`paper/supporting_material.ipynb`:

1. Delete `app-G-horopca`, `tab-G-horopca`, `app-G-horopca-reading` (659 words of Markdown, measured; the ledger cut row says 659).
2. Insert at that place (before `app-G-2`) one Markdown cell `app-G-horopca-pointer`: `The HoroPCA row above is tested by experiment in {ref}`Appendix H <appendix-h>`.` (11 words; the ledger raise row says 11). Edit nothing else in G (`app-G-job` stays).
3. Append the cells below, in order, after `tab-G-reading_pass_table` (the last cell). The generated cells are code cells whose output is the one call's; the table cell `tab-H-hypothesis` carries the tag `remove-input` like the other table cells; the sentence cells too.
4. `paper/paper.ipynb`, cell `sec-prior-art-3`: replace the last sentence of the HoroPCA paragraph, `The authors' code, run on this paper's tables after an embedding of ours, recovered the planted exponents only where the generator made them the direction of largest spread ({ref}`Appendix G <appendix-g>`).` (30 words), by `In a pre-registered test, on an embedding of ours, the authors' code recovered planted exponents only where they were the direction of largest spread ({ref}`Appendix H <appendix-h>`).` (27 words). Section 2's other `Appendix G` pointers (the register, the lineage) stay: they point at the register.
5. The supporting material's opening cell that links the appendices (`<appendix-a>` to `<appendix-g>`) and the test lists that run over `APPENDICES` need an Appendix H entry: the switch `H_LANDED` of `tests/test_paper.py` adds "H" to `APPENDICES` once the notebook holds the heading.
6. Re-execute both notebooks with their figure files in one commit; then, in the same commit, apply `h-yaml-edits.patch` (the register's HoroPCA `differs` pointer and the reading pass row 44, whose text is printed by `tab-G-register` and `tab-G-reading_pass_table`, so they change only with the re-execution: `git apply work-packages/WP35-rounds/spike-h/h-yaml-edits.patch` before executing), delete the old generator functions `horopca_rows`, `horopca_table` and the constants they use (`SPIKE`, `HOROPCA_SCALE`, `_PLANTED_LABEL`) from `paper/generate_prior_art.py`, the two old tests (`test_the_horopca_table_equals_the_spike_record`, `test_the_horopca_passage_numbers_are_in_the_record`, with `_spike_table_cells`) and the `horopca_table()` entry of `READS_BY_CALL` in `paper/generate_repro.py`, append `h-claims-rows.toml` to `claims_register.toml` (delete C538 to C546, replace C532, see that file), and delete the `H_LANDED` switch and the strict xfail test `test_appendix_h_has_landed` (the `needs_h` marker with them).
7. Then `uv run pytest tests/test_paper.py tests/test_claims_register.py tests/test_site.py tests/test_docs.py`, `tests/test_text_encoding.py`, whole-repo `uv run ruff check . && uv run ruff format --check .`, `uv lock --check`, `uv run python scripts/check_vocabulary.py`.

The cells (in order):

=== app-H | markdown
(appendix-h)=
## Appendix H. HoroPCA beside this work: a tested hypothesis

=== app-H-job | markdown
**Job.** To test whether HoroPCA, the closest existing analog, estimates what this work estimates.

- **Main text keeps:** {numref}`section %s <sect-prior-art>`, one paragraph on the two.
- **This appendix carries:** the hypothesis, the experiment, the results, their reading and how the solvers differ.
- **The repository keeps:** the record and the scripts in `work-packages/WP35-rounds/spike-h/`.

=== app-H-1 | markdown
(sub-h-1)=
### H.1 The hypothesis and what would refute it

HoroPCA [@chami2021horopca] carries principal component analysis (PCA), the directions along which a table spreads most, into hyperbolic space. This work finds the edge of the table instead: a vector of exponents defining a surface that bounds the rows from above. The hypothesis, committed with its refutation conditions before any table existed ([`hypothesis.md`](https://github.com/DynamicalSystemsGroup/hyperbolic-trade-space/blob/830cf54/work-packages/WP35-rounds/spike-h/hypothesis.md)), is that PCA and HoroPCA follow the spread and this work follows the edge. Tables of kind A keep the edge and vary the spread ratio ρ, the spread along the edge's vector over that along the next largest direction. Kind B moves the vector, by t, off the package generator's depth direction, and kind C removes the edge. A method *recovers* the vector when the absolute cosine (|cos|, agreement of directions ignoring sign) of its direction with it reaches the threshold below; its rate is the share of tables recovered.

=== sent-H-conditions | code
from generate_prior_art import horopca_conditions

horopca_conditions()

=== app-H-2 | markdown
(sub-h-2)=
### H.2 The experiment

Four metrics, 300 rows, no noise, 30 percent of the rows on the edge, six tables per setting. In A the vector is random and ρ runs from 0.25 to 4. In B, t runs from 0 to 0.9. In C, ρ is 2 or 0.5 and the rows are symmetric. Each table goes to this work (one term), to PCA (first component) and to HoroPCA (first direction; the authors' code, five restarts). HoroPCA needs a ball, so the log-metrics are centred and scaled until the farthest lies at distance R from the centre: nearly flat at R = 0.25, moderately curved at R = 1.

=== app-H-3 | markdown
(sub-h-3)=
### H.3 Results

=== sent-H-threshold | code
from generate_prior_art import horopca_threshold_sentence

horopca_threshold_sentence()

=== tab-H-hypothesis-caption | markdown
::::{table} Tables out of six in which each method recovered the vector; the hypothesis makes no prediction for PCA and HoroPCA at ρ = 1. Source: [results.json](https://github.com/DynamicalSystemsGroup/hyperbolic-trade-space/blob/main/work-packages/WP35-rounds/spike-h/results.json), [readout.md](https://github.com/DynamicalSystemsGroup/hyperbolic-trade-space/blob/main/work-packages/WP35-rounds/spike-h/readout.md).
:label: tab-H-hypothesis-1
:::{embed} #tab-H-hypothesis
:remove-input: true
:::
::::

=== tab-H-hypothesis | code
from generate_prior_art import horopca_hypothesis_table

horopca_hypothesis_table()

=== sent-H-verdict | code
from generate_prior_art import horopca_verdict_sentence

horopca_verdict_sentence()

=== sent-H-contrast | code
from generate_prior_art import horopca_contrast_sentence

horopca_contrast_sentence()

=== app-H-4 | markdown
(sub-h-4)=
### H.4 What the table shows

PCA and HoroPCA return the direction of largest spread. They recover the vector when it is that direction and miss it when another spreads more, edge or no edge. This work returns the edge at every spread, and nothing like the vector where there is none. PCA says along which combinations the sampled designs differ, this work where the table stops: they are complementary, and {ref}`Appendix D.16 <sub-d-16>` already chains them, running PCA on the chart of the near-frontier designs. A HoroPCA of the chart would be the same kind of chain and was not run.

=== sent-H-slab | code
from generate_prior_art import horopca_slab_sentences

horopca_slab_sentences()

=== app-H-4b | markdown
**Reading limits.** The embedding is ours: the centre, the scale R and the map into the ball are our choices, and a second embedding was not run. HoroPCA at R = 3 is in the record, not tested. The tables are not tree-like, the data HoroPCA was built for, and are noise-free, four-dimensional and six per cell; HoroPCA ran one direction at its default settings.

=== app-H-5 | markdown
(sub-h-5)=
### H.5 How the formalism and the solvers differ

HoroPCA optimizes a frame, k orthonormal directions, so that points projected along horospheres (curved surfaces standing where hyperplanes do in flat space) keep the most variance. That objective is not convex: the authors' code runs Adam from random starts, and nothing bounds the result's distance from the best frame. This work minimizes a soft maximum (log-mean-exp) of weighted log-metrics over the simplex, which for one term is convex, by a linear program or a sequential quadratic program, and returns a gap bounding the result's distance from the best. HoroPCA is a PyTorch module; this work is a scikit-learn transformer. Sources: the authors' repository at commit c9a9996; `src/hyperbolic_trade_space/solvers.py`; `derivation/lemma_04_convexity.py`.

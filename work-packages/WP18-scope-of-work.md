# WP18 — Scope of work: ternary plots in the documentation's examples

| | |
|---|---|
| **Status** | DRAFT. Approved only by the recorded act below. Nothing in this package is executed before then. |
| **Supervisor (accountable)** | mzargham |
| **Repository** | `posynomial-invariant-form`, branch `dev`; this document at `work-packages/WP18-scope-of-work.md` |
| **Approval record** | The driver's approval under the mandate (`release-candidate.md`), quoted verbatim in `work-packages/WP18-decisions.md`; for the supervisor's review at the PR |
| **Acceptance record** | The driver's verification in the browser, recorded in `WP18-decisions.md`; the supervisor's acceptance at the PR from `dev` to `main` |

## Purpose

The supervisor, verbatim (`WP8a-decisions.md`, last section): "adding examples using the ternary
plots to the documentation. keep it simple like with the other plots in the examples; we just want
that visualization pattern to be documented, accessible and interpretable for users." The root page's
Why image already draws the triangle, with its own private projection code in
`scripts/build_site_figures.py`. This package makes that pattern a public plotting function, shows it
in two documented examples, and gives a reader who has never met a ternary diagram a key to read it.
Evidence: `docs/superpowers/notes/spike-ternary/report.md` (with its Addendum and Correction),
`make_why3.py`, `make_why5.py`, `mock/index.html`. This is step 3c of `release-candidate.md`.

What the triangle shows (settled with the supervisor, from the Correction): a position is a set of
shares of a total among three metrics; a facet's exponent vector is a point of the triangle, and it
is where that facet's V peaks at a fixed total; the regions are where each facet dominates
(analysis, not assignment); lines of equal V at a fixed total are an optional overlay; the stars are
not places where V = 1, because V also depends on the total.

## Goals

- G1. One public plotting function draws the triangle (shares, regions, exponent-vector stars,
  designs, optional equal-V lines) in plain Matplotlib, with a doctest. The root page's Why image and
  the docs examples are two consumers of that one implementation.
- G2. Example (i) in the docs: three metrics on a planted table, showing designs, regions and
  exponent vectors.
- G3. Example (ii) in the docs: the cubesat by its exponents grouped by subsystem (power, mass,
  attitude control), exact because exponents add over groups.
- G4. The pattern is documented, accessible and interpretable: a short key for a reader who has never
  read a ternary diagram, alt text, labels that do not rely on colour alone, light and dark, legible
  at 375 px, and the limits stated.
- G5. The standing rules hold: vocabulary resolves in `glossary.yaml`, every claim is backed, the
  word budgets are not raised, and the interface contract is amended for the new public name.

## Non-goals

- A new dependency (no mpltern; the spike used it only to explore).
- A ternary plot of cubesat designs: in a three-metric sub-composition of a ten-metric case they do
  not separate by facet (spike, C right). Not drawn, not offered.
- More than two examples; ternary figures in the paper, the notebooks or the root page beyond the
  Why image's switch to the shared function.
- Choosing the three metrics or the grouping for the user: both are the analyst's choices, stated as
  such. No automatic selection of triples or groups.
- Any change to the fit, `solvers.py` or `estimator.py` (WP17 owns them), the Why image's appearance
  (it is re-drawn pixel-for-pixel in intent; see R-3), the data swap, or the reader grid.
- Distances read off the triangle: it is for reading, not for measuring.

## Deliverables

| ID | Deliverable | Serves |
|---|---|---|
| D-1 | `plot_ternary` (name *(default)*) in `src/hyperbolic_trade_space/plotting.py`, added to `__all__`, with numpydoc docstring and doctest | G1 |
| D-2 | `scripts/build_site_figures.py` calls D-1; its private barycentric projection and region code are removed | G1 |
| D-3 | Example (i) in the docs: a runnable block calling D-1 on a planted table, its light and dark figure, caption, alt text | G2, G4 |
| D-4 | Example (ii) in the docs: the cubesat by subsystem groups, runnable block, figure pair, caption, alt text | G3, G4 |
| D-5 | "How to read this plot": a short key beside the first example, plus the limits | G4 |
| D-6 | Interface-contract amendment: `plotting` list in `interface-contract.toml` gains the name, `contract_version` 6 with a change-log row in `interface-contract.md` | G5 |
| D-7 | `glossary.yaml` entries (see R-9) and the stems list if a new stem is needed | G5 |
| D-8 | Tests in `tests/` (plotting, site, figures) and the budget/figure-cap handling per OD1 and OD2 | G1, G4, G5 |
| D-9 | Browser review record in `work-packages/WP18-decisions.md` (desktop and 375 px, light and dark) | G4 |

## Requirements

| ID | Requirement | Checked by |
|---|---|---|
| R-1 | `plot_ternary` is public in `hyperbolic_trade_space.plotting`, uses only Matplotlib and NumPy, takes named metrics (three) and returns the axes; it follows the other `plot_*` functions' `ax=` and colour conventions *(default)* | Read `plotting.py`; `uv run pytest tests/test_package.py tests/test_interface_contract.py`; `pyproject.toml` has no new dependency |
| R-2 | Its doctest runs and asserts something nontrivial (the stars sit at the exponent vectors; the regions partition the triangle) | `uv run pytest src/hyperbolic_trade_space/plotting.py` (doctests are enabled) |
| R-3 | One implementation, two consumers: `scripts/build_site_figures.py` imports it; no second barycentric projection remains; the existing Why-image tests (`tests/test_site.py`: partition, labels from exponents, label placement, size, lines overlay) pass unchanged, and a new test asserts the script's drawing code goes through the package function | `uv run pytest tests/test_site.py`; `grep -n "def project" scripts/build_site_figures.py` returns nothing; no test is edited to weaken a requirement |
| R-4 | The function draws: shares of a total as positions; each facet's exponent vector as a star in the facet's colour; regions by dominating facet; designs as points; the optional equal-V lines at a fixed total, off by default in the function *(default)* and on in example (i) *(default)*; star and line values are computed from the fit, not hand-set | Unit test against `score_samples` at a fixed total (log V = log S + max_k(a_k + sum_j w_kj log c_j), to 1e-10, the Correction's identity); test that each star lies at its facet's `exponents_` row |
| R-5 | The text never says a star is where V = 1; it says V peaks there at a fixed total, and says V also depends on the total | Docs claim test or review of the key and caption against the Correction; `claims-review.md` row added |
| R-6 | Example (i) is a runnable block on a seeded planted table (`make_frontier_data`), figure built by `scripts/build_figures.py` in both schemes from the code shown above it | `uv run pytest tests/test_site.py -k "figure"` (figures-from-shown-code test) |
| R-7 | Example (ii) draws the cubesat's fitted exponents summed within three groups (power, mass, attitude control), from the committed ADCS data via the case module; the grouping is stated as the analyst's choice; the printed weight each facet carries is exact (group sums of the exponents) | A test that the grouped vector is the group sum of `exponents_` and sums to one; runnable block builds the figure |
| R-8 | Accessibility: alt text of at least 8 words, describing what the plot shows and what it says; facets and groups are distinguished by label and marker shape as well as colour; light and dark both legible (text contrast stays at least 4.5:1 *(default)*); legible at 375 px (labels not clipped or overlapping) | Alt-text and caption tests (`test_figures_are_few_captioned_and_in_both_colour_schemes`); label-overlap test as for the Why image; the browser review (D-9) |
| R-9 | Vocabulary: every term of art on the new text resolves in `glossary.yaml`. Added entries *(default)*: "ternary plot" (alias "triangle plot"), "share" (of a total; position in the triangle), "region" (where a facet dominates; analysis, not a label on a design). "Simplex" is already an assumed term; "exponent vector", "facet" and "metric" exist. Phrases avoided: any membership claim ("a design belongs to a facet") | `uv run pytest tests/test_docs.py tests/test_build_generated.py`; the vocabulary-review check; glossary page builds |
| R-10 | The limits are stated in the docs: three parts only; choosing three metrics and grouping are the analyst's choices (and can be cherry-picked); the triangle is for reading, not measuring distance; designs of a ten-metric case do not separate in a three-metric triangle | Read the page; each limit cites the spike report or a lemma/claims-review row |
| R-11 | Word budgets hold with no budget raised beyond OD1's answer; every page within its budget, total at most 7,600 | `uv run pytest tests/test_site.py::test_word_budgets_hold` |
| R-12 | Browser review at desktop and 375 px in light and dark, on the built docsite pages, recorded with what was seen | Driver's browser pass; D-9 |
| R-13 | `uv run pytest`, `uv run ruff check .`, `uv run ruff format --check .` and `uv lock --check` pass; the docsite builds | Run them |
| R-14 | Commits to `dev` only, staged by path, no AI attribution; nothing outside the repository or the scratchpad changed; no push, merge, tag or deployment | `git log`; `git status` |

## Definition of good

- A reader who has never seen a ternary diagram reads example (i), says where a design sits in terms
  of shares, finds each facet's peak, and says what a region means, from the key alone.
- The two examples are as simple as the other example plots: a few lines of code each, one figure each.
- The same function draws the root page's Why image, so the picture a reader meets first is the one
  they can reproduce.

## Definition of good enough

- R-1 to R-14 each pass their check, with evidence recorded in `WP18-decisions.md`.
- Both examples render in both schemes, are legible at 375 px, and carry alt text and captions.
- The key, the limits and the glossary entries are in place; no page exceeds its budget.
- The existing Why-image tests pass unchanged.

## Definition of done

Good enough is met, **no open item remains unresolved**, and the supervisor has accepted the work by the acceptance record above.

## Order of work

1. Contract amendment (D-6) and glossary entries (D-7) first, so the name and terms exist.
2. Write `plot_ternary` and its doctest by moving the projection, regions, label placement and star
   code from `scripts/build_site_figures.py` into `plotting.py`; unit tests (R-2, R-4).
3. Point `build_site_figures.py` at it; run the Why-image tests unchanged (R-3).
4. Example (i): block, figure, key, limits (D-3, D-5).
5. Example (ii): grouped cubesat block and figure (D-4); the group-sum test (R-7).
6. Budget, caption, alt-text and figure-count tests per OD1 and OD2; claims-review row (R-5, R-11).
7. Full suite, lint, lock check, docsite build (R-13); browser review, desktop and 375 px, light and
   dark; fix and repeat once (R-12). Record in `WP18-decisions.md`; hand to the driver.

## Estimate

One agent, about one working session: the move and tests are the bulk (about 40 percent); the two
examples, the key and the glossary about 35 percent; the browser loop about 25 percent. Risk: the
Why-image tests are tight on label placement, so the move must keep the code path identical.

## File ownership

WP18 touches: `src/hyperbolic_trade_space/plotting.py`; `docs/examples.md` and/or
`docs/user-guide/chart.md` (or a new page per OD1); `scripts/build_figures.py` and
`scripts/build_site_figures.py`; `tests/test_site.py`, a plotting test file and, if needed,
`tests/test_docs.py`; `work-packages/interface-contract.toml` and `.md`; `glossary.yaml`; `docs/api.md`
only if the API-page test requires it; `docs/superpowers/notes/claims-review.md` (one row);
`work-packages/WP18-decisions.md`. WP17 owns `src/hyperbolic_trade_space/solvers.py` and
`estimator.py`; WP18 does not touch them, and reads `exponents_`, `log_offset_`, `facet_` and
`score_samples` only through their public interface, so a WP17 change to the soft weights reaches
the plot without a WP18 edit. Collision to watch: if WP17 changes the public attribute names, WP18
follows the contract.

## Agent's defaults

- Function name `plot_ternary` and its parameter layout (named metrics or groups, exponents and
  offsets from a fitted estimator or given directly, `designs=`, `lines=`, `ax=`); it returns the axes.
- Equal-V lines are off by default in the function and ON for example (i) (the driver's instruction).
  **They are listed here so the supervisor can strike them**; striking them changes only the `lines=`
  argument in that block and one caption sentence.
- Lines drawn at fixed fractions of the highest peak (0.97 down to 0.3), unlabelled, as in `make_why5.py`.
- Plot style follows the other `plot_*` functions and the Why image's palette (blue, amber, green;
  marker shapes added to the stars so colour is not the only cue).
- Example (i) data: the Why image's planted table (`make_frontier_data(900, 3, n_terms=3, random_state=11)`,
  temperature 50) so the root page and the example agree.
- Example (ii) grouping: power (power margin, energy balance, eclipse reserve, peak slew power, depth
  of discharge), mass (total mass), attitude control (settling time, slew time, pointing error,
  control effort); the printed weight on each facet is exact.
- Glossary entries added: "ternary plot", "share", "region" (R-9).
- Contrast threshold 4.5:1 for text; 375 px checked at that width in the browser pane.
- Tests: new plotting tests in a new file under `tests/`; the site tests extended, not weakened.
- The key is four short sentences (corner, edge, interior, a worked read), set as a list.

## Open decisions (for the supervisor)

- **OD1.** Where the new prose goes. `examples.md` is at 399 of 400 words and `chart.md` at 543 of
  600, so the key, the two captions and the limits (about 250 words) do not fit in either without a
  change. Options: (a) a new page `user-guide/ternary.md` with its own budget of 350 words, inside the
  7,600 total (currently 6,065), holding the key and the limits, with the two examples' figures
  and code on `examples.md` and the page linked from both / (b) `examples.md` budget raised from 400 to
  650 and the key and limits there, no new page / (c) the key and limits in `chart.md` (57 words
  free) with `chart.md`'s budget raised to about 800 and the examples on `examples.md` with a
  smaller raise.
- **OD2.** The figure cap. The docsite has seven figures, the cap in `build_figures.MAX_FIGURES` and
  `test_figures_are_few_captioned_and_in_both_colour_schemes`, so two more need a raise to nine.
  Options: raise the cap to nine / keep seven by dropping the equal-V overlay and showing both
  examples in one two-panel figure / keep seven by retiring an existing figure (the supervisor names which).

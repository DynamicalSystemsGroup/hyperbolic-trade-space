# Note: citing the paper from the docs (WP81)

The paper is a working paper on its own branch (`paper`) with its own tags and change record. Its abstract is published
at `/paper/` (`paper/mode.toml`, mode `abstract`); the full text builds from the repository (`paper/`, two notebooks
and what rebuilds them). A docs page cites the paper with `[text](paper:key)`, which `scripts/paper_keys.py` resolves
to the page and anchor that carry the key when a pin is served and to the abstract page with no anchor otherwise.

## The rule (his decision, 2026-11-17: "Remove until a pin")

While the paper is in abstract mode the docs carry no `paper:` link. The two surfaces do different jobs (his words,
`work-packages/WP81-decisions.md`): the docs support a user, the paper a researcher. A former pointer either states
the result in the docs' own words, drawn from the working paper in brief and for a user and no wider than its
backing in `claims_register.toml` (a theorem's statement is backed by its lemma, as the theory page's rows are), or
is removed where its content is the paper's job (a proof, an appendix, the prior-art argument, the search programme). Two sentences name the paper: one on the docs home and one in Further reading, each
saying that it is a working paper, that its abstract is published at `/paper/`, and that the full text builds from
the repository. The paper is called "the working paper" wherever it is named. When a pin is served the links may
return, one per named result, under the rule of that day. A test in `tests/test_site.py` holds this: no `paper:`
citation on a docs page while the mode is abstract, and the two naming sentences present.

## The inventory (R-1), read 2026-11-17 at the WP81 base

Every pointer into the paper on a reader-facing surface (23 `paper:` citations, three more than the scope's first count, and five prose surfaces), with its sentence and its disposition. Dispositions (brief from the paper; removed as the paper's role; names the working paper) are decided after the
persona journeys (`work-packages/WP81-rounds/journeys.md`, R-8); until then a row reads "pending".

| # | Surface | Sentence (the pointer in it) | Key | Disposition |
|---|---|---|---|---|
| 1 | `docs/index.md` | "The [paper](paper:sect-problem) makes the argument for the method; the [project page](../) links it, these docs and the package." | sect-problem | names the working paper (moved to the foot of the page; the opening clause removed) |
| 2 | `docs/theory.md` | "definitions only, no proofs; the [paper](paper:sect-results) has them." | sect-results | removed as the paper's role |
| 3 | `docs/theory.md` | "Because the weights sum to one, V(λm) = λV(m): [doubling every metric doubles V](paper:thm-invariant)." | thm-invariant | brief: the statement stays, the link goes |
| 4 | `docs/theory.md` | "[the fit is] a convex program](paper:thm-convex) after the logarithmic change of variables." | thm-convex | brief: the statement stays, the link goes |
| 5 | `docs/theory.md` | "[The map is reversible](paper:thm-chart) for every row with strictly positive metrics." | thm-chart | brief: the statement stays, the link goes |
| 6 | `docs/theory.md` | "[n-lemma](paper:def-nlemma), drawn in [Figure 1 of the paper](paper:fig-nlemma)." | def-nlemma, fig-nlemma | brief: the figure clause removed, n-lemma links the glossary |
| 7 | `docs/bridge.md` | "It is the bridge to [the search direction of Future work](paper:sect-future)." | sect-future | removed as the paper's role (the search loop, planned and not shipped, in the docs' words) |
| 8 | `docs/bridge.md` | "([the chart theorem](paper:thm-chart)), so a chart point maps back to attributes and to metrics." | thm-chart | brief: links the theory page's reversibility statement |
| 9 | `docs/bridge.md` | "(... Appendix B, [section 6](paper:sub-b-6))." | sub-b-6 | removed as the paper's role (the finding stays; its numbers are a later package's) |
| 10 | `docs/bridge.md` | "the outer loop of the search named in the paper's [Future work](paper:sect-future) is the refit." | sect-future | removed as the paper's role (the outer loop named by its steps) |
| 11 | `docs/user-guide/temperature.md` | "The fit temperature tau sets how hard the maximum is ([definition](paper:def-temperature))." | def-temperature | brief: links the glossary's temperature entry |
| 12 | `docs/user-guide/temperature.md` | "([the n-lemma's members](paper:def-nlemma)): here the first four metrics." | def-nlemma | brief: links the glossary's n-lemma entry |
| 13 | `docs/user-guide/temperature.md` | "supporting envelope (lemma 5 in [Appendix E](paper:appendix-e))." | appendix-e | brief: the result stays in words; the lemma named without a link |
| 14 | `docs/user-guide/temperature.md` | "(lemma 22 in [Appendix E](paper:appendix-e))." | appendix-e | brief: the result stays in words; the lemma named without a link |
| 15 | `docs/examples.md` | "described by a [SysML v2 system model](paper:sect-case-construction)." | sect-case-construction | removed as the paper's role (the GitHub path to the model stays) |
| 16 | `docs/further-reading.md` | "HoroPCA: the nearest analog in setting; [how this work differs](paper:sect-prior-art)." | sect-prior-art | brief: one clause on the difference; the page carries the second naming sentence |
| 17 | `docs/user-guide/fitting.md` | "`n_terms=K` [terms](paper:thm-extension), where you choose K" | thm-extension | brief: terms links the glossary |
| 18 | `docs/user-guide/termination.md` | "[`certified`](paper:thm-certificate) is the first: a local optimum of the loss, not of other restarts." | thm-certificate | brief: certified links the glossary |
| 19 | `docs/user-guide/limitations.md` | "Appendix E of the paper states what they do and do not establish" (the lemma scripts) | prose | removed as the paper's role (the lemma scripts' folder named) |
| 20 | `docs/code-owners.md` | the paper's lifecycle, branch, tags and Zenodo (a maintainers' page) | prose | names (a governance page; the document called the working paper) |
| 21 | `site/index.html` | "The paper makes the argument and gives the proofs; the documentation gets the method running on a dataset of your own." and the card "Read the paper: the argument and the proofs" | root page | names the working paper (the body sentence; the card's mode line is the composer's) |
| 22 | `README.md` | "See the [docs], [the paper] and `examples/adcs/` for a case study." and the repository map's `paper/` line | README | names the working paper (the first paragraph) |
| 24 | `docs/theory.md` | "using the [log-mean-exp (entropic) soft maximum](paper:thm-lme) of w·u" | thm-lme | brief: the statement stays, the link goes |
| 25 | `docs/theory.md` | "the contending metrics at [constant elasticities](paper:thm-elasticity)" | thm-elasticity | brief: the statement stays, the link goes |
| 26 | `docs/bridge.md` | "The conditioning is invertible ([pull-back to attributes](paper:thm-pullback))" | thm-pullback | brief: the statement stays, the link goes |
| 23 | `docs/api-reference.md` | a docstring's "Theorem 1" (package text, out of scope; a candidate for the package's next release) | docstring | out of scope |

## The journeys (R-8)

Traced per persona in `work-packages/WP81-rounds/journeys.md` before any edit; the competing preferences and the
choice per pointer are written there and summarised in the dispositions above.

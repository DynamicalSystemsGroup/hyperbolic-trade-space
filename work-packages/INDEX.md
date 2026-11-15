# Index of work packages

This index is the status of every package; the scope files carry no live status line. `milestones.md` is the release board. A package is archived at its landing: its documents leave the tree with the hash where it was accepted, and the index row says how to read them back.

Reading a removed document: `git show <accepted>:work-packages/<file>`. A file added after the accepted commit is read from the commit before its removal: `git log --all --diff-filter=D --format=%h -1 -- work-packages/<file>`, then `git show <that hash>^:work-packages/<file>`. Local copies go in `work-packages/archive/` (git-ignored).

Scope locked is the later of the commit that added the scope and the first commit of the decisions file that records his approval. Accepted is the commit that landed the package or recorded its acceptance on `dev`. Packages 8, 12, 21, 56 and 58 have no accepted commit.

| WP | Title | State | Scope locked | Accepted | Documents |
|---|---|---|---|---|---|
| 0 | Setup and persisted working agreements | accepted | 4281350 | f5cde59 | in history: `git show f5cde59:work-packages/<file>` |
| 1 | Derivations (SymPy lemma chain L1–L10, abstract spaces) | accepted | 5d2b0ec | 82fdd47 | in history: `git show 82fdd47:work-packages/<file>` |
| 2 | Core estimator (solvers, chart, HyperbolicTradeSpace) | accepted | b8a6c69 | 5c3dc1c | in history: `git show 5c3dc1c:work-packages/<file>` |
| 3 | Conditioning, prediction and analysis toolkit | accepted | 83f4038 | 07fe9d3 | in history: `git show 07fe9d3:work-packages/<file>` |
| 4 | ADCS case generator (simulation port, design space, dataset) | accepted | bcfe110 | ef79e83 | in history: `git show ef79e83:work-packages/<file>` |
| 4b | ADCS case enrichment as a SysML-modelled illustrative cubesat | accepted | 4c2e557 | f1e38ca | in history: `git show f1e38ca:work-packages/<file>`; `WP4b-decisions.md` in place (read by tests/test_adcs_enrichment.py, docs/superpowers/notes/adcs-tensions-probe.md) |
| 5 | Literature review and bibliography | accepted | bcfe110 | 4ce27d4 | in history: `git show 4ce27d4:work-packages/<file>` |
| 6 | Mathematics narrative | accepted | 83f4038 | f6d9b9a | in history: `git show f6d9b9a:work-packages/<file>` |
| 7 | ADCS case notebook (draft 3, two regimes of the SysML-modelled cubesat) | accepted | b1ba105 | 755bf5e | in history: `git show 755bf5e:work-packages/<file>` |
| 8 | Site and first release | superseded (split into WP8a and WP8b) | 5b1d087 | not landed | in history: read from the commit before its removal (recipe above) |
| 8a | Site skeleton up | landed, accepted | 96086cc | 2d2a751 | in history: `git show 2d2a751:work-packages/<file>` |
| 8b | Release preparation for 0.1.0 | in flight (release preparation) | d4db0e5 | not landed | in place (not landed or in flight) |
| 9 | Posynomial solver for K > 1 | accepted | 3082200 | c4133c8 | in history: `git show c4133c8:work-packages/<file>`; `WP9-decisions.md` in place (read by docs/superpowers/notes/spike-facet-refit/README.md, docs/superpowers/notes/notation.md); `WP9-review.md` in place (read by paper/supporting_material.ipynb, docs/superpowers/notes/abstraction-gaps.md) |
| 10 | The paper, working draft | landed, accepted | d3abf28 | 4ede5bd | in history: `git show 4ede5bd:work-packages/<file>`; `WP10-decisions.md` in place (read by paper/container/README.md, paper/myst.yml); `WP10-reading-pass.md` in place (read by paper/generate_reading_pass.py, paper/reading_pass.yaml); `WP10-scope-of-work.md` in place (read by docs/superpowers/notes/paper-sources/README.md); `WP10-vocabulary-review.md` in place (read by scripts/vocabulary_baseline.toml) |
| 11 | Readability and correctness loops over the reader grid | in flight (reader-grid loops; WP11-final and WP11-round-1 are read by tests and the paper) | 94ff559 | not landed | in place (not landed or in flight) |
| 12 | Trade-off-aware search of the design space | scoped later (the search follows the release); decisions only, no scope | d3abf28 | not landed | in place (not landed or in flight) |
| 13 | Response to the external review | accepted | 093e8d3 | 655d978 | in history: `git show 655d978:work-packages/<file>` |
| 14 | Interface contract (technical ↔ presentation) | accepted | 4b559cb | 328371a | in history: `git show 328371a:work-packages/<file>` |
| 15 | System model tidy-up (the cubesat example as a legible SysML v2 model with an experiment ledger) | landed, accepted | c1595e6 | 2d2a751 | in history: `git show 2d2a751:work-packages/<file>` |
| 16 | The data swap (the paper's case on the generation of record) | landed | 4f0f307 | ea46637 | in history: `git show ea46637:work-packages/<file>`; `WP16-decisions.md` in place (read by paper/container/RECORD.md) |
| 17 | The several-term fit with soft weights (the fit at the model's own sharpness) | landed | 480937e | 4425666 | `WP17-decisions.md` in place (read by docs/superpowers/notes/claims-review.md, claims_register.toml); `WP17-scope-of-work.md` in place (read by docs/superpowers/notes/claims-review.md, claims_register.toml) |
| 18 | Ternary plots in the documentation's examples | landed | 829bce2 | 0a18b5b | in history: `git show 0a18b5b:work-packages/<file>`; `WP18-decisions.md` in place (read by docs/superpowers/notes/figure-review.md) |
| 19 | The paper's figures (slots, candidates, placement, by section) | landed | 548fb1d | 96aa493 | in history: `git show 96aa493:work-packages/<file>`; `WP19-decisions.md` in place (read by paper/figures/figure1.py, paper/figures/ternary_pair.py); `WP19-figure-review.md` in place (read by paper/length_ledger.toml, claims_register.toml) |
| 20 | Verification in tiers | landed | 5084f99 | 5775220 | in history: `git show 5775220:work-packages/<file>`; `WP20-review.md` in place (read by tests/test_check_script.py) |
| 21 | The response to the independent assessment | approved by the driver, no landing recorded | e699a54 | not landed | in place (not landed or in flight) |
| 22 | The system model's two views (configuration and assessment in one SysML v2 model) | landed | afc441e | 6ed13ed | in history: `git show 6ed13ed:work-packages/<file>` |
| 23 | The model-realism loop (configuration space and metric space explicit, the case regenerated once) | accepted | b0e12db | 657bc41 | in history: `git show 657bc41:work-packages/<file>`; `WP23-decisions.md` in place (read by examples/adcs/model_v2/ledger_gate.py, claims_register.toml); `WP23-review.md` in place (read by examples/adcs/model_v2/coverage.py); `WP23-rounds` in place (read by paper/container/RECORD.md, examples/adcs/experiments/reports/change-register.md) |
| 24 | The word "facet" goes (one name for the model object, on every surface, before 0.1) | accepted | 71a5f74 | 19be468 | in history: `git show 19be468:work-packages/<file>` |
| 25 | Repository tidiness, first instance (cruft deleted, drift and gaps listed; step 3h, recurring) | in flight (recurring tidiness; instance 4) | 0df9d0b | not landed | in place (not landed or in flight) |
| 26 | The model in the view editor (a modeller and a UX researcher, one round) | landed, accepted | 74b2402 | d427011 | in history: `git show d427011:work-packages/<file>` |
| 27 | Stakeholder concerns in the case model, in the view editor | landed, accepted | 7941c63 | d427011 | in history: `git show d427011:work-packages/<file>` |
| 28 | Improvement by subtraction (step 5a of the path) | accepted | d7a3fe3 | 552fbc9 | in history: `git show 552fbc9:work-packages/<file>` |
| 29 | Track A, the noise result (a new result from Proposition 2) | landed, accepted | 845de4d | e10a4f1 | in history: `git show e10a4f1:work-packages/<file>`; `WP29-review` in place (read by paper/length_ledger.toml) |
| 30 | Track B, the model revision (momentum headroom as the ninth traded metric; the fleet-size variable and the cost model) | landed | 845de4d | 77fe83c | in history: `git show 77fe83c:work-packages/<file>`; `WP30-build-notes.md` in place (read by examples/adcs/experiments/definitions.py); `WP30-rounds` in place (read by scripts/wp30_cost_ladders.py) |
| 31 | Choosing K in the documentation | landed, accepted | 3c9e1c1 | 0eb6ace | in history: `git show 0eb6ace:work-packages/<file>`; `WP31-readout.md` in place (read by claims_register.toml) |
| 32 | Package-user tests (U1 to U4) | landed, accepted | 0171ae7 | 6be8a9f | in history: `git show 6be8a9f:work-packages/<file>` |
| 33 | Journeys and signposting (one size fits none) | accepted | 0171ae7 | 282b479 | in history: `git show 282b479:work-packages/<file>`; `WP33-scope-of-work.md` in place (read by paper/length_ledger.toml) |
| 34 | Windows as a third platform | landed, accepted | 483b1f4 | 9418183 | in history: `git show 9418183:work-packages/<file>` |
| 35 | HoroPCA acknowledged and distinguished, "hyperbolic" defined once, Table 1's "differs" column made uniform | accepted | 1d27f8c | 282b479 | in history: `git show 282b479:work-packages/<file>`; `WP35-amendment-1-scope.md` in place (read by paper/length_ledger.toml); `WP35-decisions.md` in place (read by paper/length_ledger.toml, claims_register.toml); `WP35-review.md` in place (read by paper/length_ledger.toml); `WP35-rounds` in place (read by tests/test_paper.py, paper/generate_repro.py) |
| 36 | Future directions: formal results and Rust/WASM (decisions and rounds only) | landed, accepted | 200b31a | 9456caa | `WP36-decisions.md` in place (read by claims_register.toml); `WP36-rounds` in place (read by claims_register.toml) |
| 37 | A history and acknowledgements page, linked from the root page | accepted | bf9dee8 | 282b479 | in history: `git show 282b479:work-packages/<file>`; `WP37-rounds` in place (read by scripts/history_record.py, tests/test_site.py) |
| 38 | The residual pass (patterns that read as machine-written) | accepted | ff9c410 | 282b479 | in history: `git show 282b479:work-packages/<file>`; `WP38-confirmations` in place (read by docs/superpowers/notes/residual-review.md); `WP38-flags` in place (read by docs/superpowers/notes/residual-review.md); `WP38-scope-of-work.md` in place (read by docs/superpowers/notes/residual-review.md) |
| 39 | The case ends in a decision | accepted | 518b5ab | 282b479 | in history: `git show 282b479:work-packages/<file>`; `WP39-scope-of-work.md` in place (read by paper/length_ledger.toml) |
| 40 | Release thinning and repository organization | accepted | dfc7c95 | 282b479 | in history: `git show 282b479:work-packages/<file>` |
| 41 | The bridge to the search, part 1 (framing and docs page) | landed | 17ece6e | af54b3b | in history: `git show af54b3b:work-packages/<file>`; `WP41-rounds` in place (read by claims_register.toml) |
| 42 | Tension, and the glossary's terms across decision analysis, optimization and learning | landed | 4d5c339 | a2a6ab2 | in history: `git show a2a6ab2:work-packages/<file>` |
| 43 | Beyond the posynomial, the kernel direction tested (research spike) | landed | 02d8142 | d0a97cd | in history: `git show d0a97cd:work-packages/<file>`; `WP43-rounds` in place (read by docs/superpowers/notes/kernel-direction.md) |
| 44 | A second case study from a public dataset (research spike) | landed (research spike readout; accepted under the mandate) | d5c2576 | d16309e | in history: `git show d16309e:work-packages/<file>` |
| 45 | Two public case studies and a two-metric example for the documentation | landed | d14158c | 6482f6d | in history: `git show 6482f6d:work-packages/<file>`; `WP45-rounds` in place (read by examples/perovskite/run.py, examples/amniote/run.py) |
| 46 | The fit temperature as a path | landed | 80b6f13 | 415d889 | in history: `git show 415d889:work-packages/<file>`; `WP46-decisions.md` in place (read by claims_register.toml); `WP46-rounds` in place (read by claims_register.toml) |
| 47 | Release engineering and repository governance for v0.1 | landed | a97e774 | 1cd23db | in history: `git show 1cd23db:work-packages/<file>`; `WP47-rounds` in place (read by tests/test_admissibility.py, tests/test_release_checks.py) |
| 48 | Governance control checks for the release process (research spike; after v0.1) | landed | 9e839a4 | ba62c15 | in history: `git show ba62c15:work-packages/<file>` |
| 49 | A contributor covenant for an AI-native, trustworthy package (research spike) | landed | a97e774 | a62b9bb | in history: `git show a62b9bb:work-packages/<file>` |
| 50 | Topological holes in the chart by persistent homology (research spike; future direction) | landed | a5f1278 | 5233126 | in history: `git show 5233126:work-packages/<file>` |
| 51 | The root page recast (why, what, how) with the three-metric figure | landed | 83b2e36 | 01ad083 | in place (landed, not yet archived: in flight) |
| 52 | The governance lineage on the history page (research spike, then a proposal) | landed, accepted | d63e7a6 | 03790a0 | in history: `git show 03790a0:work-packages/<file>` |
| 53 | Integrate his review batch of 2026-11-15 (abstract, Sections 1 to 3) | landed, his read pending | 0dd4e79 | da8d57a | in place until his read; then in history |
| 54 | The paper's skeleton (Section 7 into Future work; AI acknowledgement and Reproducibility) | landed, his read pending | 65624d3 | e435e4a | in place until his read; then in history |
| 55 | The mathematics builds up (Section 3's fitting problem, Sections 4 to 6) | scoped (after WP54) | 022c4d2 | not landed | in place (not landed or in flight) |
| 56 | Sections 7 to 9 from the current model; the decision-maker's ternary | directed (decisions only; its spikes delivered) | 2b160b4 | not landed | in place (not landed or in flight) |
| 57 | The appendices (a planning package and its children) | scoped (planning package) | e0b4ee4 | not landed | in place (not landed or in flight) |
| 58 | The docsite, root page and README swept; the reviewer's guide at the new head | directed (no documents yet) | - | not landed | in place (not landed or in flight) |
| 59 | Conditioning and feature engineering on the three public cases (spike) | landed, accepted by the driver, his read pending | a2533ca | a9cfb60 | in place until his read; `examples/*/variants.py` stay (code) |
| 60 | The three example pages | landed, his read pending | 022c4d2 | 65b0683 | in place until his read; then in history |
| 61 | The work-packages directory indexed and thinned | landed | 48d1e39 | a1a73ab | in place (the protocol) |

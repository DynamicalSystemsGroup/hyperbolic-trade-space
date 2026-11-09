# WP8a — Decision records (site skeleton up)

Records typed by the agent (driver session). Decisions are the supervisor's.

## Origin (2026-11-08)

- Breakdown row WP8a (`README.md`), OK'd by the supervisor with the interface-contract condition;
  the draft scope by the PM's bounded subagent (`WP8a-scope-of-work.md`, f341690). Layout and tone
  decisions inherited from `WP8-decisions.md` ("Amendment 1 revised", the root index as thin HTML
  after hc-marimo, a growing landing page for talks). Release control from WP14's gate: a deploying
  merge is preceded by a recorded review of the staged localhost site.

## Decision loop (2026-11-08)

- **OD1, where the live-site check sits.** Options: accept on the staged site with the live check
  after the merge / acceptance waits for the live site. **Supervisor (mzargham), verbatim:** "Accept
  on the staged site; live check after the merge". Disposition: decided; acceptance is judged on the
  localhost assembly reviewed by the supervisor plus a green manual build run on `dev`; the merge to
  `main` follows; the public URL is checked afterwards and recorded in this file, fix-forward if it
  fails.

- **OD2, a working-draft label on the public site.** Options: visible line / no label.
  **Supervisor (mzargham), verbatim:** "no label we don't deploy to main and thus github pages until
  we have an actual first release. in the mean time its local host review loops"
- Disposition: decided, no label; and a consequence for the package: nothing is deployed to GitHub
  Pages before the first release (WP8b). WP8a still delivers the Pages workflow, but it must not
  trigger on pushes to `main` (merges to `main` continue for CI); it triggers on the release tag or
  on manual dispatch only, and the first deployment is WP8b's. Review loops run on the localhost
  staging build (WP14 R-12). OD1's "live check after the merge" therefore moves to WP8b's release;
  WP8a's acceptance is judged on the staged localhost site plus a green manual build run on `dev`.
  OD3 (the paper card before WP10) no longer concerns a public page and becomes a default: the card
  is shown and links to the placeholder on the staging site.

- **Agent's defaults, as one item** (OD3 folded in). **Supervisor (mzargham), verbatim:** "you are
  allowed to include placeholder links that are not live yet as long as they will be live on an
  official release. don't make extra steps for yourself and don't crowd your attention with
  caveats. just keep a bang list for review once its live and if a link is broken we detect and fix
  it in a patch"
- Disposition: defaults approved with that change: links to pages that will exist at the first
  release (the paper under `/paper/`, the PyPI page once published, release notes) may be placed
  now; the link test treats them as expected-at-release rather than broken; a punch list
  (`work-packages/release-punch-list.md`) records every such link and anything else to verify once
  the site is live, checked at WP8b and fixed in a patch where broken; no caveat text on the pages.
  Loop closed: decided 2 (OD1, OD2), OD3 folded into the defaults, raised 0, defaults approved with
  the link policy.

## Scope approval (approval gate)

- **Document:** `work-packages/WP8a-scope-of-work.md` with its "Gate outcomes" and link policy
  (no open items).
- **Date:** 2026-11-08.
- **Driver's question:** "WP8a, the site skeleton: root index after hc-marimo, MkDocs docsite under
  /docs/, the /paper/ slot, the generated ledger and verification pages, one assembly-and-serve
  command for localhost review, the Pages workflow armed for the release tag and manual dispatch
  only, tests, the punch list; no open items. Do you approve the scope for execution?" (options:
  Approved / Not yet).
- **Supervisor (mzargham), verbatim:** "Approved"
- **Disposition:** approved; the PM executes on `dev` against WP14's contract as it lands;
  acceptance is judged on the supervisor's review of the staged localhost site plus a green
  dispatch build on `dev`; no deployment before the first release.

## Front matter and link fixes

Applied last (D-9). The only change to each page is the front-matter block of four lines at the top of the file, with the page's world (`world: embodied | symbolic | formal`, rendered as the world line under the title by `overrides/partials/content.html`):

| File | Line | Before | After |
|---|---|---|---|
| `docs/why-and-how.md` | 1 | (none) | `---` / `world: embodied` / `---` / blank line |
| `docs/method.md` | 1 | (none) | `world: formal` block |
| `docs/preconditioning.md` | 1 | (none) | `world: symbolic` block |
| `docs/api.md` | 1 | (none) | `world: symbolic` block |
| `docs/limitations.md` | 1 | (none) | `world: formal` block |
| `docs/literature.md` | 1 | (none) | `world: formal` block |

`docs/index.md` carries no world (it maps all three). The generated pages carry no front matter; the override sets their world (`formal`). No title key was needed. Link fixes: none; `mkdocs build --strict` and `tests/test_site.py` find no broken relative link in the six pages.

## Root index: why, what, how (2026-11-08, during execution)

- **Supervisor (mzargham), verbatim:** "also i want the index to be more why, what, how. why is the
  motivation, what is the pca analog for tensions, and how is the essentially the chart from the
  reviewer (fyi i am the reviewer, that chart was generated by chatgpt so there is no conflict to
  using it).

  the details of the sympy work and the worked example don't need to be in the top level index page
  at this time"
- Disposition: an amendment to WP8a's D-4 (the root page): three sections in order, Why (the
  motivation: trade studies as documents, the bar for a trusted model-based method), What (the PCA
  analogue: PCA explains variance, this explains tensions; the n-lemma as the unit), How (the paper
  map from the external review, `docs/superpowers/notes/external-review/paper-map.webp`, as the
  figure, with its boxes as the reading order), then the cards (paper, docs, package); no SymPy
  detail and no worked example on the index for now. Provenance recorded here: the review is the
  supervisor's own, and the map was generated with ChatGPT at his direction; he states there is no
  conflict in using it; the page credits it as the map of the mathematics without tool attribution,
  per the repository's attribution rule.
- **Supervisor (mzargham), verbatim:** "the scikit learn compatability can appear in the what".
  Disposition: the WHAT section of the root index also states that the method is delivered as a
  scikit-learn-compatible estimator (fit, transform, inverse_transform, score_samples; the
  conformance checks pass), in one sentence, with the same feel as PCA in the ecosystem.
- **Supervisor (mzargham), verbatim:** "it can also be chained with pca its not a strict substitute.
  it just belongs in unsupervised learning / feature engineering". Disposition: the WHAT section
  says so: the method belongs to unsupervised learning and feature engineering beside PCA, not in
  place of it, and the two chain (for example PCA on the near-frontier chart coordinates, as the
  tension report already does); the same wording goes to the register and WP10's framing.

- **Delivery note (root index: why, what, how).** `site/index.html` now runs Why, What, How, then
  the three cards and "Start wherever suits you", then the source link. What states the PCA
  analogue (explains tensions, not variance; the n-lemma as the unit), the placement in
  unsupervised learning and feature engineering beside PCA (kin, chainable; the tension report
  runs PCA on the near-frontier chart coordinates) and the scikit-learn-compatible estimator in
  one sentence. How carries `site/paper-map.webp` (copied from
  `docs/superpowers/notes/external-review/paper-map.webp`), full width, with alt text and the
  caption "A map of the mathematics: assumptions, the single-term core, the chart and its uses, the
  multi-facet extension, the open questions", and one line naming the boxes as the reading order. No
  SymPy or worked-example material remains on the page; still thin HTML, no scripts, light and
  dark. `scripts/assemble_site.py` gained a minimal edit to copy `site/*.webp` next to
  `index.html` (the staged output uses the same function). A long install command overflowed at
  phone width and now wraps. Checked in the browser pane at desktop and 375 px width. MathJax in
  the docs loads from a CDN, so math on docs pages needs network access during localhost review.

## Delivery notes (PM, factual; not decisions)

- Execution on `dev`: commits "WP8a: ..." 53919c3 to e85a97c; fresh-context review `WP8a-review.md` (2c35dd1).
- The PM added `permissions: contents: read` to the build job of `.github/workflows/pages.yml` (security review of the workflow); the deploy job keeps `pages: write` and `id-token: write`. Candidate for a later package: pin both workflows' actions to full commit SHAs with the version in a comment.
- The docs `default-groups` change was committed by the driver (ee68bfa); `uv lock --check` unchanged.
- Math in the docsite loads MathJax from a CDN, so math needs network during the localhost review.

## The supervisor's staged-site review (2026-11-08)

- Served with `uv run python scripts/stage_site.py --serve`, read in the browser pane.
  **Supervisor (mzargham), verbatim:** "a few thoughts.
  (1) the top level page can include the figure for how but it also needs text to summarize it.
  (2) the paper is not something i've done a full read on yet. fist pass seems okay but it will
  definitely need readability and correctness loops. we'll need to run a grid of user reads (cold)
  at the depth levels previously outlined and with differing personas. this means the paper
  acceptance is stuctural not final sign off on content or aesthetics.

  the lemmas for example are not very readable and might be better organized as traditional
  theorem like statements from academic papers but with the proof sketches narrative and the reader
  directed to the specific scipy scripts or independent verification. some of that can be relegated
  to appendices if it helps with the flow.

  actually i think you muddle togethe the doc site and the paper. i cannot tell what is what. i
  want the docsite to be more like scikit learn docs and the paper to me more like my scipy paper."
- Driver's reading, for the record: the `/paper/` slot is a placeholder (WP10 has not started); the
  lemma pages read were the docsite's Mathematics page (`docs/method.md`, WP6's discursive
  narrative with lemma blocks, extended by WP13). The finding stands as stated: the docsite carries
  paper-register material and the site does not make the distinction visible.
- Consequences to put to the supervisor: (1) is a WP8a amendment (a summarizing paragraph under
  the How figure); (2) shapes WP10 (acceptance structural; theorem-style statements with narrative
  proof sketches pointing to the scripts; appendices) and WP11 (a grid of cold reads: depth levels
  × personas); (3) is a docsite restructure in the scikit-learn style (getting started, user guide,
  API reference, a theory section with theorem-style statements and the ledger, examples,
  literature), which is beyond WP8a's skeleton and either holds WP8a's acceptance or becomes a
  package of its own.
- Driver's question: accept the skeleton and restructure in a new package / hold WP8a until the
  docsite is restructured / fold the restructure into WP10. **Supervisor (mzargham), verbatim:**
  "hold until the doc site is restructured. i think it can be thinned out. should be more scikit
  learn doc site like. don't force things into the doc site that belong in the paper"; and then,
  verbatim: "i need a seperation of concerns between the paper and the doc site
  the doc site is for a user of the package. the paper is for someone who wants to understand the
  how and why underneath"
- **Disposition:** WP8a is HELD at its gate; Amendment 2 (drafted by the PM's bounded subagent,
  re-approved at the gate) extends WP8a to the docsite restructure under the separation of concerns:
  the docsite is for a user of the package (getting started and install, a user guide that walks
  conditioning, fitting, reading the tension report, the chart and the plots, the API reference
  generated from the docstrings, a short example that points to the paper for the case, a one-page
  "theory in brief" that links to the paper for the how and why, limitations as they bear on use,
  changelog); the paper is for someone who wants the how and why underneath (the mathematics
  narrative, the lemmas as theorem-style statements with narrative proof sketches pointing to the
  derivation scripts, the derivation ledger, the literature review, the full case, the abstraction
  gaps), so `docs/method.md`, `docs/literature.md`, the derivation narrative and the long
  limitations move into the paper and its appendices or supporting material (WP10's sources), and
  the docsite is thinned accordingly; the root page's How figure gets a summarizing paragraph.
  Nothing is forced into the docsite that belongs in the paper; nothing a package user needs is
  left only in the paper. The staged review is repeated after the restructure.

## Amendment 2 decision loop (2026-11-08; draft appended to `WP8a-scope-of-work.md`, ccb0cb6)

- **OD1, the generated Derivations and Verification pages.** Options: keep only Verification / keep
  both as a section / move both to the paper. **Supervisor (mzargham), verbatim:** "move both to the
  paper. and even there they are likely going to be appendices". Disposition: decided; neither
  generated page is on the docsite; the derivation ledger and the verification audit go to the
  paper's supporting material as appendices (WP10's draft: Appendix B theory and lemma coverage,
  Appendix D algorithm; the audit under its verification appendix); `scripts/build_generated.py`
  keeps producing them for the paper's build, not for the docsite.
- **OD2, a docsite page for the abstraction-gaps ledger.** Options: no page, paper appendix only /
  a short table. **Supervisor (mzargham), verbatim:** "No docsite page; paper appendix only".
  Disposition: decided; the user guide's limitations section names the gaps that bear on use and
  links to the paper's appendix.
- **OD3, the Changelog page before the first release.** Options: an empty Unreleased section / a
  0.0.1 entry / no page until WP8b. **Supervisor (mzargham), verbatim:** "No page until WP8b".
  Disposition: decided; the docsite has no changelog until the release package adds it.
- **OD4, the world line under page titles.** Options: drop it from the docsite / keep only on
  Theory in brief / keep on every page. **Supervisor (mzargham), verbatim:** "Drop it from the
  docsite". Disposition: decided; the three-worlds framing stays in the paper and the root page's
  How; the docsite pages carry no world line; WP14's contract item C-9 (the world key) is
  withdrawn in the contract v2 amendment.
- **OD5, a glossary.** Options: a short glossary / none. **Supervisor (mzargham), verbatim:** "yes to
  glossary but let's generate it programmatically rather than hand write it. you can make
  glossary.yaml so that the source is skimmable but the glossary should be compiled from that not
  free text". Disposition: decided; a `glossary.yaml` (skimmable: term, the register's one-phrase
  definition, what it is not where the register says so, the code name, the paper anchor) is the
  single source; `scripts/build_generated.py` compiles the docsite's Glossary page from it; the
  same file is proposed to WP10 as the source of the paper's register table (Appendix A), so the
  docsite and the paper cannot drift apart on the words; the register note stays the human record
  of how each word was settled.
- **Amendment 2's Agent's defaults, as one item** (OD1 to OD5 folded in; the world-line override
  removed; the glossary compiled from `glossary.yaml`). **Supervisor (mzargham), verbatim:** "Approve
  the defaults as listed". Disposition: approved. Loop closed for Amendment 2: decided 5 (OD1 to
  OD5), deferred 0, raised 0, defaults approved as one item.
- At the approval question for Amendment 2 and contract version 2. **Supervisor (mzargham),
  verbatim:** "make sure we don't have left over references to content we removed. if we want to add
  references to content in the paper we can come back and do that later after the paper is stable,
  and we should do the references in a manner that they don't break when things move around
  (similar to ref keys in latex) the citations to the paper in the docsite are deferred until there
  is a paper and appendices to cite"
- Disposition (changes to the draft before approval): (1) a requirement and a test that no docsite
  page, navigation entry, docstring-rendered page or site script refers to removed content (moved
  file names, old anchors, lemma tags, "see Mathematics", the generated pages, the world key); (2)
  G9 and its machinery are withdrawn from Amendment 2: no citations from the docsite into the paper
  for now, no `paper_sections.toml`, no expected-at-release paper-section links in docs pages, and
  the contract's version-2 item for paper anchors is dropped (the root page's Paper card to the
  `/paper/` slot stays as site navigation); (3) a deferred follow-up, recorded on the punch list and
  as a later-package candidate: once the paper and its appendices are stable (after WP11), add the
  docsite's references to the paper through stable reference keys (a key registry resolved at build
  time, in the manner of LaTeX labels and refs), so links do not break when sections move.

## Amendment 2 and contract version 2: approval (2026-11-08)

- **Documents:** `WP8a-scope-of-work.md`, "Amendment 2 (draft)" with its gate outcomes (G9
  withdrawn, R-26 added); the contract's version-2 items listed there, without the paper-anchors
  item.
- **Driver's question:** "Amendment 2 is changed as you said: a test that nothing on the docsite
  refers to removed content; no citations from the docsite into the paper for now (...); references
  to the paper by stable keys recorded as deferred until the paper and appendices are stable. With
  that, do you approve Amendment 2 and contract version 2 for execution?" (options: Approved / Not
  yet).
- **Supervisor (mzargham), verbatim:** "Approved"
- **Disposition:** approved; the PM executes Amendment 2 and the contract's version 2 on `dev`;
  acceptance of WP8a (skeleton plus Amendment 2) on the supervisor's second staged review and a
  green Tests run; the Pages dispatch build after the merge.

## Amendment 2 delivery notes (2026-11-08; presentation side: configuration, scripts, tests, contract)

Facts only. The docsite pages and `paper-sources/` are recorded by the writer of the pages.

**What changed**

- `glossary.yaml` (new, repository root): 37 entries with fields `id`, `term`, `symbol` (optional),
  `short`, `register`, `formal`, `not`, `defined_in` (optional). Seeded from the register phrases of
  `docs/superpowers/notes/notation.md` (all ten) and the terms the user guide uses.
- `scripts/build_generated.py`: `load_glossary` validates the source (required and unknown fields,
  non-empty strings, one-line `term` and `short`, slug ids, unique ids and terms) and `glossary_page`
  compiles `docs/generated/glossary.md` (title, letter headings, one `- **term**: short` per entry;
  no other text; sorted by term). `derivations.md` and `verification.md` are written to
  `build/generated/` (outside `docs/`, git-ignored through `build/`) for the paper's build; their
  content is unchanged. `--out` sets the first directory, `--docs-out` the glossary directory. An
  invalid glossary stops the build.
- `scripts/assemble_site.py` passes both directories; `scripts/stage_site.py` `REVIEW_PAGES` follows
  the new routes.
- `overrides/partials/content.html` removed; `custom_dir` removed from `mkdocs.yml`; navigation is
  Home, Getting started, User guide (eight pages), API, API reference, Examples, Theory in brief,
  Glossary (`generated/glossary.md`), Further reading.
- `work-packages/release-punch-list.md`: post-release routes replaced (`docs/method/`,
  `docs/generated/derivations/`, `docs/generated/verification/`, `docs/literature/` removed;
  `docs/getting-started/`, `docs/user-guide/overview/`, `docs/theory/`, `docs/generated/glossary/`,
  `docs/further-reading/` added). The deferred paper-reference item stays.
- Contract version 2 (`interface-contract.md`, `.toml`, `tests/test_interface_contract.py`, one
  commit): `docs.pages` is the fourteen hand-written pages; `docs.presentation_pages` is those plus
  `docs/api-reference.md`; new keys `docs.generated_dir`, `docs.generated_pages`,
  `docs.glossary_source`, `docs.paper_sources_dir`; `derivation.generated_dir` is `build/generated/`;
  the five technical docs pages leave the technical set and `docs/literature.md` leaves WP10's; WP8a
  gains the docs pages, `glossary.yaml` and the `paper-sources/` carve-out and loses `overrides/` and
  `docs/case.md`; six delivered clauses leave the skip list; the bibliography gap row is rewritten.
  The paper-anchors item is not present (G9 withdrawn); the world key (C-9) is not pinned in version
  1 and is recorded as withdrawn in change-log row 2.

**Test repoints (no assertion weakened)**

| Test | Before | After |
|---|---|---|
| `tests/test_build_generated.py` | derivations and verification built into one directory | glossary built into a second directory; new tests: schema validation (bad sources rejected), page equals the compiled yaml with no other text, alphabetical grouping, determinism, build stops on an invalid glossary, outputs outside `docs/` |
| `tests/test_docs.py` | `PAGES = preconditioning.md, api.md`; lemma tags, ledger ids, "cites a lemma/ledger id", method assertions on `docs/method.md` | pages are the recursive docsite glob; tag and id range checks over every docsite page; exported names and submodule functions over `api.md` plus the user guide; statuses, tolerances, `termination_`, `conditioning_` over `user-guide/termination.md`; policy paragraph not restated on any docsite page; register phrases over the docsite; forbidden phrases over the docsite, `paper-sources/` and `glossary.yaml`; new runnable-block execution test |
| `tests/test_paper_sources.py` (new) | n/a | the assertions that required lemma/ledger citations, "Map and territory" exactly once, the three-levels headings, L12 to L14 cited, statuses and tolerances, run unchanged against the snapshots in `docs/superpowers/notes/paper-sources/` |
| `tests/test_narrative.py` | `METHOD`, `PAGES` under `docs/` | constants point at the snapshots; new docsite hygiene test (no attribution, no emoji) |
| `tests/test_site.py` | eleven old nav pages, world-key and world-line tests, `custom_dir == overrides`, math markers on `method`/`preconditioning`, literature bibliography test, old punch-list routes | sixteen-page nav, word budgets (per page and 7,600 total), forbidden-content regexes and the six-formula limit, internal anchors, no docsite link into the paper, no `custom_dir`, math markers on `theory` and any page with inline math, further-reading bibliography, live routes and `REVIEW_PAGES`, generated directory holds only the glossary, and R-26 (below) |
| `tests/test_interface_contract.py` | skips for six WP8a deliveries; pinned pages owned by exact path | those clauses enforced, skip list asserted equal to `myst_config` and `oracle_protocol`; ownership by prefix; generated location and `.gitignore` checks; glossary source and paper-sources carve-out |
| `tests/test_notebook.py` | asserts the retired notebook's closing cell names `docs/method.md` | unchanged: the assertion reads the notebook text, which is not edited; WP10 archives the notebook |

**R-26 (nothing refers to removed content):** `tests/test_site.py` scans the hand-written pages, the
root and paper pages, `mkdocs.yml`, `scripts/assemble_site.py`, `scripts/stage_site.py`, the nav and
route lists, the punch-list routes and the built docsite for moved file names, moved routes,
`generated/derivations` and `generated/verification`, the Mathematics page, lemma tags L1 to L14 (docs
pages), and the world key; it asserts the moved pages, `overrides/` and the two generated pages are
absent from `docs/` and from the built site.

**Removed:** `overrides/`; `docs/generated/derivations.md` and `verification.md` as docsite pages;
the world-key tests.

**Not changed by W2:** `tests/test_references.py` still points `LIT` at `docs/literature.md` and is
being edited by WP10; it needs the repoint to `paper-sources/literature.md`.

## Amendment 2 fixes (implementer, after the fresh review)

- **Concurrency:** `tests/test_site.py` builds the site and the paper's generated pages into pytest temporary directories (`assemble_site.py --out` and the new `--generated-dir`); `build_generated` writes every page atomically (temp file and `os.replace`); `assemble()` takes an `fcntl` lock (`build/.site-build.lock`) around the glossary step and the MkDocs read of `docs/`. Two simultaneous `uv run pytest tests/test_site.py -q` runs both passed (29 passed each).
- **G-2:** one plain-text sentence closes `docs/theory.md` (derivation scripts under `derivation/`, full account in the paper when published; no link).
- **O-4:** `mkdocs.yml` sets `site_dir: build/docsite` (ignored); new test runs a bare `mkdocs build --strict` and asserts `site/index.html` and `site/paper/index.html` survive.
- **O-3:** footnote INFO removed (a line starting `[@key]:` parsed as a definition; reworded). Only Home's `../` INFO remains (accepted).
- **O-2:** `docs/generated/` is already in `.gitignore` and `glossary.md` is not tracked (`git ls-files docs/generated` empty); it is generated by build_generated, assemble, stage and the tests. A bare `mkdocs build --strict` needs `uv run python scripts/build_generated.py` first.
- **O-1:** accepted. **O-5:** pending at acceptance.
- **G-1 (for the PM; src/ is the technical side, not edited here).** Docstring lines citing L1 to L14, A1/A2/A4 or "spec section 4" (the L1-norm uses in datasets.py:35,86 and solvers.py:292-293 are not citations):
- `src/hyperbolic_trade_space/coordinates.py:27`
- `src/hyperbolic_trade_space/coordinates.py:4`
- `src/hyperbolic_trade_space/datasets.py:119`
- `src/hyperbolic_trade_space/datasets.py:120`
- `src/hyperbolic_trade_space/estimator.py:159`
- `src/hyperbolic_trade_space/estimator.py:160`
- `src/hyperbolic_trade_space/estimator.py:163`
- `src/hyperbolic_trade_space/estimator.py:3`
- `src/hyperbolic_trade_space/estimator.py:491`
- `src/hyperbolic_trade_space/estimator.py:4`
- `src/hyperbolic_trade_space/estimator.py:549`
- `src/hyperbolic_trade_space/estimator.py:56`
- `src/hyperbolic_trade_space/estimator.py:592`
- `src/hyperbolic_trade_space/estimator.py:5`
- `src/hyperbolic_trade_space/estimator.py:645`
- `src/hyperbolic_trade_space/estimator.py:64`
- `src/hyperbolic_trade_space/estimator.py:688`
- `src/hyperbolic_trade_space/gaps.py:136`
- `src/hyperbolic_trade_space/gaps.py:3`
- `src/hyperbolic_trade_space/gaps.py:6`
- `src/hyperbolic_trade_space/preconditioning.py:261`
- `src/hyperbolic_trade_space/preconditioning.py:266`
- `src/hyperbolic_trade_space/preconditioning.py:27`
- `src/hyperbolic_trade_space/preconditioning.py:3`
- `src/hyperbolic_trade_space/preconditioning.py:65`
- `src/hyperbolic_trade_space/preconditioning.py:67`
- `src/hyperbolic_trade_space/preconditioning.py:7`
- `src/hyperbolic_trade_space/predictive.py:1`
- `src/hyperbolic_trade_space/solvers.py:137`
- `src/hyperbolic_trade_space/solvers.py:172`
- `src/hyperbolic_trade_space/solvers.py:388`
- `src/hyperbolic_trade_space/solvers.py:4`
- `src/hyperbolic_trade_space/solvers.py:99`
- `src/hyperbolic_trade_space/tensions.py:14`
- `src/hyperbolic_trade_space/tensions.py:5`
- `src/hyperbolic_trade_space/tensions.py:69`
- `src/hyperbolic_trade_space/tuning.py:18`
- `src/hyperbolic_trade_space/tuning.py:19`
- `src/hyperbolic_trade_space/tuning.py:1`

## The driver's first browser pass: fixes (implementer, round 2)

The driver's calls on `WP8a-driver-browser-pass.md` are binding and applied as follows.

- **D1 (reverses the approved default "figures not copied"; the driver's call).** Seven figures, each
  built by `scripts/build_figures.py` from the `{.runnable}` block directly above it, in a light and a
  dark image (`docs/generated/figures/`, ignored, built by `assemble_site.py` before MkDocs reads
  `docs/`): Getting started 1, Fitting 1, Tensions 1, Chart 2, Examples 2 (the case module on the
  committed data). None is copied from the paper. `tests/test_site.py` holds the count, the pairs, the
  captions and that the builder's output equals what the pages embed. The word budgets count captions
  and not image alt text.
- **D2.** Code lines are at most 72 characters (the column holds 80 at 1280 px in the browser);
  a test keeps them there. The API reference renders docstring examples as written: a few of those
  lines are longer (`src/`, technical side).
- **D3.** The API overview and the termination statuses are lists; `docstring_section_style: list` in
  `mkdocs.yml` renders parameters as lists.
- **D4.** The first display equation is split over two lines; `docs/stylesheets/extra.css` lets a wide
  display scroll inside its box.
- **D5.** Inventories of attribute and function names are lists (Fitting, Chart, Tensions).
- **D6.** Not reproduced on any docsite page in a fresh browser tab (server log and console clean). The
  only 404 reproduced was the browser's request for `/favicon.ico` on the root page and the paper
  placeholder, which declare no icon; both now carry `<link rel="icon" href="data:,">`. The real paper's
  page logs two 404s from its own CDN requests (thebe, MathJax 2); not changed here.
- **R1.** The map is a plain link to `paper-map.webp` and takes up to 94 percent of a wide window
  (CSS only). The map is not redrawn.
- **R2.** The install command breaks between words (nowrap segments, `<wbr>` after slashes).
- **R3.** Root and placeholder wording follows the thinned docsite. `assemble_site.py` and
  `stage_site.py` build the real paper (`uv run myst build --html` in `paper/`, with `BASE_URL` set to
  the route: `/hyperbolic-trade-space/paper` on the site, `/paper` when staged) and copy
  `paper/_build/html` into `<out>/paper/`; they fall back to the placeholder when the build does not
  run or fails, or with `--paper placeholder`. Both branches are tested with an injected runner.
- **CI defect.** `test_generated_pages_in_the_build` read `build/generated/` left by another command;
  its fixture now builds the generated pages into a temporary directory and the test asserts those.
  Checked in a fresh worktree (`git worktree add`, `uv sync --locked`, the six test files): 220 passed.

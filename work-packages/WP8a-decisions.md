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

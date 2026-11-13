# Note: user journeys (a builders' working note, WP33 D-1)

Not a page for users and not linked from the site, the paper or `docs.pages`. Built from existing returns only, no new
readers. Evidence key: **W11** `work-packages/WP11-round-1/triage.md`; **W28** `WP28-retest.md` and `WP28-retest/returns/`;
**W29** `WP29-review/P9-P10-triage.md`; **W30** `WP30-rounds/persona-{baseline,final}/`; **W32** `WP32-cells/triage.md` and
`round-1/`, `round-2/`. Personas and depths: `reader-grid.md`. Paper cells are cited by notebook cell id or heading
(`paper/paper.ipynb`; `supporting_material.ipynb` is the appendices). "Other" is the user the content is aimed at.

Surfaces: repo page = `README.md`; root = `site/index.html`; docs = `docs/` (nav in `mkdocs.yml`); paper; API =
`docs/api.md`, `docs/api-reference.md`; examples = `docs/examples.md`, `examples/adcs/`; package = the installed import.

## The twelve journeys

| Persona | Arrives at | First need (their words) | Path (evidence) | Content on the path aimed at another user (file, heading, other) |
|---|---|---|---|---|
| P1 | root, then paper | "What trades against what, and can I trust it?" | root card "Paper" to abstract and Figure 1 to main-results list to Sections 8 to 11; reads on selectively (W11 round 1b, W28 P1-B/P1-C) | abstract's kernel and "soft support" clauses (paper, Abstract; P5); Definition 4 band sentence, "weighs within a factor e" (paper, Definitions; P5); Figure 3 box "returns 7 of 8 metrics" (paper, Case construction; P7) |
| P2 | paper depth B/C, then docs | "A method I can run, rerun and defend" | main results to Sections 8 to 11 (Case) to `docs/examples.md` to `choosing-k.md` (W11, W28 P2-B/P2-C, R2/R3 task reads) | Theorem 11 "K^N + 1" sentence (`res-L15`; P5, P9); Methods R1 sentence (`sec-methods`; P5, P9); Definition 6 against Section 6.2 (paper, Definitions; P5) |
| P3 | paper (Figures 2, 3), then repo | "Plug my evaluation in; what must hold?" | Figure 2 and 3 (SysML views) to Methods to Section 11 "Reproducibility and your own case"; infers conditioning is theirs (W28 P3-B/P3-C) | Figure 1 legend "1.00, 1.00, 1.00" and "planted" (paper, Preliminaries; P5); Definition 6's 1e-9 support against Figure 1's face (paper, Definitions; P5) |
| P4 | docs Home "beside PCA", paper Sections 5 to 6 | "Where does this sit beside PCA, how do I use it?" | `docs/index.md` third paragraph to getting-started to `choosing-k.md` "Large K and the elbow in PCA"; paper results and Figure 5 (W11 1b/1d, W28 P4-B; no P4 depth-C read, held out) | main-results item "Numerical: the termination status" (paper, Results lead; P5; 3 cells stopped); Definition 3 centring and bounds (paper, Definitions; P5, P9) |
| P5 | paper depth B to D, then `derivation/` | "Check the mathematics and the algorithm's claims" | Definitions to Theorems 3 to 12 to Appendix B (L1 to L20) to lemma scripts; `docs/theory.md` (W28 P5-B/P5-C, W29) | Figures 1 to 3 (paper, Preliminaries and Case construction; P1, P3); selection effect in the association maps (Case analysis; P2) |
| P6 | paper abstract to Section 2 | "Is this new to me, or a renaming?" | Abstract to "Prior art, by family" to Case analysis to Appendix G; wants the centring sentence before equation (1) (W11, W28 P6-B/P6-B2/P6-C) | Theorem 11 "K^N + 1" sentence, read as empty by P6-B2 and P6-C (`res-L15`; P5, P9); R1 sentence (`sec-methods`; P5); Figures 5 and 6 association heatmaps, which P6 suspects of being cluster evidence (paper, Case analysis; P2) |
| P7 | root, paper Sections 8 to 10, App. C, repo model | "Is the case how a real program behaves; where is it a toy?" | paper Case construction and Case analysis to C.8 to `examples/adcs/case-model.md` to `model_v2/cubesat.sysml`; no docs pages (W30 baseline, final) | no replicated item. Stops were absences: the toy statement sat only in C.8 and `case-model.md`, not where findings are read (W30 triage N-F5, answered by one body clause) |
| P8 | root (Q4), paper abstract, `docs/examples.md` | "Would this change a decision I make, and what does it cost me?" | abstract to Sections 8, 9 (two money numbers) to D.17 and Examples; checks economics in C.8 (W30 baseline, final F1 to F9) | abstract sentences 2 to 9: surface, posynomial, n-lemma, energy differential, GGP, kernel (paper, Abstract; P4, P5); root page figure caption "energy differential" (`site/index.html`, second figure; P4, P5); Examples names limits without values (`docs/examples.md`, "Requirements read after the fit"; absent, not aimed away) |
| U1 | repo page, then site | "Fit my table; which metrics trade?" | README `uv sync` to root to docs Home to getting-started to conditioning to fitting to choosing-k to tensions to chart: 8 to 10 pages, one backtrack (W32 r1, r2) | `choosing-k.md` "Helpers" import of `case` and "The cubesat" (case-study reader; all four cells skipped or rewrote); Home bullet "a cubesat trade study" (`docs/index.md`, Where to start; P7, P3); README Status and CI sentences (maintainer; moved in r2) |
| U2 | repo page, then docs | "Fit my model's table; does the model side matter?" | as U1, plus `overview.md` (read last in r1, 5th in r2) and eight further pages fetched by script to search for "SysML" (W32 r2) | `choosing-k.md` "The cubesat" (case-study reader); `examples.md` cubesat blocks (P7); `docs/index.md` cubesat bullet |
| U3 | repo page (README), docs by curl | "Install to a first fit, as code" | README example to docs Home to getting-started to conditioning, fitting, choosing-k, tensions, chart: 9 pages, 6 s install in r2 (W32 r1, r2) | `choosing-k.md` "Helpers" (case-study reader; wrote a five-line loop in both rounds); Home cubesat bullet; `termination.md` opened in r1 only to read `not_applicable` at K = 1 (P5) |
| U4 | repo page, then docs | "U3's task, plus connect the model" | as U3; guessed `/docs/guide/` (404: the nav slug is `user-guide`) and reached `overview.md` only after getting-started (W32 r2) | `choosing-k.md` "The cubesat" and Helpers (case-study reader); `docs/index.md` cubesat bullet |

P9 and P10 (the mathematical-presentation pair) are not rows: they read the same paper boxes as P5 and are folded into
P5's path. Their finding for placement is in the table below (W29 triage C4, C6: the expert's hypothesis codes and
`sigma_j` detail loses the novice, and belongs in Appendix B).

## Placements and cuts it implies

Candidates only; each is net neutral or negative in words on its surface. Flags: [pin] touches a pinned name or the
interface contract (amendment, R-7); [reg] has claims-register rows to re-point; [led] paper ledger `[[cut]]` row.

| Candidate | File | One-line reason |
|---|---|---|
| Move "The cubesat" section to the examples page; leave Helpers installed-package-only | `docs/user-guide/choosing-k.md`, `docs/examples.md` [reg] | skipped by all four U cells in both rounds; it is the case-study reader's |
| Reword the Home Examples bullet to name the case study, not the user's path | `docs/index.md` | all four U cells met "cubesat" first and set it aside |
| Cut Home bullets that no U or persona path used (Theory, Glossary, Further reading) down to the five need-phrases | `docs/index.md` | none opened in either round; P5 and P6 reach them by nav |
| Place the "design variables and labels are configuration" clause where "Your own data" sends the reader | `docs/getting-started.md` (from `overview.md`, "The pipeline") | U1 and U3 never opened the overview; their `batch` and `sample` handling was a guess |
| Move the needs block (the five doors and the adoption line) to the end of the root page, as the call to action; the whom sentence stays at the top | `site/index.html` | the supervisor's ruling (WP33-decisions.md, 2026-11-14 09:15): the block closes the page as the call to action, not first |
| Cut the root page's second-figure caption sentence in the PCA/energy voice, or move it under the Paper card | `site/index.html` [reg] | the executive's arrival speaks to P4 and P5 above the three doors |
| Move the K^N + 1 sentence to Appendix B, L15 | `paper.ipynb` `res-L15` [reg][led] | seven cells found it empty; only P5 and P9 need it (W28 CR-36) |
| Move the R1 sentence's finite-tau reading to the Theorem 5 sketch | `paper.ipynb` `sec-methods`, `res-L7` [reg][led] | eight cells stopped; it is a P5 check (W28 CR-37) |
| Drop "Numerical: the termination status" from the main-results list; `termination.md` carries it | `paper.ipynb`, Results lead [led] | three P4 cells stopped; the item is P5's and the docs page holds it |
| Move the hypothesis-code clauses and the `sigma_j` sentence to App. B and L18 | `paper.ipynb` Corollary 1 box, Section 3 list [reg][led] | P10 loses the thread, P9 keeps the detail (W29 C4, C6) |
| Review whether `api.md` and `api-reference.md` serve any path | `docs/api.md`, `docs/api-reference.md`, `mkdocs.yml` [pin] | no U cell or persona opened either in the returns; Q3 merge only if a docstring pin allows |
| Add the top-level directories the list omits, with their job (`paper/`, `site/`, `scripts/`, `tests/`) | `README.md` Layout | R-4; the five-line list is out of date |

## P8 journey requirements

From `WP30-rounds/persona-final/triage.md` (P8 F2, F6, F8). The executive arrives at the root page (Q4); the paper's
first screen stays the paper's. Routing, not a new body paragraph.

- **Route to the requirements reading:** one link from the root page to Appendix D.17 (and the Examples block) under a
  need-phrase on the executive's question, which requirement is dear and what imposing them first changes. P8 found the
  decision mechanism present but "priced in bands" (F3, answered in D.17) and shown nowhere on the screens they were sent to.
- **Dense first screens (F8):** the root page's lead and figure captions are the P4 and P5 voice; the wayfinding read
  measures the executive's steps to D.17 at both widths.
- **Adoption cost, three lines** (Q1):
  1. *Who writes the conditioning:* the analyst, who decides orientation and scale; the line points at the conditioning
     page (`docs/user-guide/conditioning.md`). Backed by what the docs already ask of the user.
  2. *Time to a first fit:* a number the WP32 cells measured, install to first fit 6 s (U3, round 2; 1.3 s sync for U1),
     U1's whole task about 100 s of reading and writing. To be recorded as a register row before the line is written.
  3. *Designs needed:* only as `docs/user-guide/limitations.md` says under "Small samples": with few designs, exponents are
     weakly determined. No number is invented.

# Note: presentation framing and site (WP6, WP8)

## Source: the supervisor's SciPy 2026 paper

"Derivations, Not Just Simulations: Teaching Applied Mathematics with Scientific Python", Michael
Zargham. Source notebook `/Users/z/Documents/GitHub/hc-scipy-2026/papers/michael_zargham/paper.ipynb`
(MyST/Curvenote build via `myst.yml`); published at https://proceedings.scipy.org/articles/wdyr6752.
Companion: `/Users/z/Documents/GitHub/hc-marimo` (notebook, talk deck, site, `derivation/` chain).

Thesis: the SciPy stack covers two of Tall's three worlds (NumPy/SciPy = operational-symbolic,
matplotlib and reactive notebooks = conceptual-embodied); SymPy brings the axiomatic-formal world
into the same kernel, making the glass-box principle (Buchberger 1990; Artigue 2002) practicable:
every seam (derivation → lambdify → solve → figure) is inspectable source.

Prescriptions to follow: one module per world with its own test file; the artifact is executable
(notebook is the article); embodied hook first, then small visible derivation steps, then the
glass-box moment; consistent visual vocabulary documented in the plotting module; notation
quickstart in the body, full glossary in supporting material; credit sources, claim only the
implementation; tests make the formal and operational worlds auditable in CI while figures require
human inspection. From the hc-marimo talk: "Verify with the machine (did we build it right?).
Validate as a human (did we build the right thing?)"; ledger of Derived / Posited / Inherited /
Leaned-on regularity; six-stage pattern Motivate, Symbolize, Derive, Lambdify, Simulate, Validate.

Citations as used in the paper: Tall, D. O. (2008), "The Transition to Formal Thinking in
Mathematics", Mathematics Education Research Journal 20(2), 5–24; Tall, D. O. (2013), *How Humans
Learn to Think Mathematically: Exploring the Three Worlds of Mathematics*, Cambridge University
Press, ISBN 9781107035706; Sfard (1991) Educ. Stud. Math. 22(1), doi 10.1007/BF00302715;
Buchberger (1990) ACM SIGSAM Bulletin 24(1), 10–17; Artigue (2002) Int. J. Computers for Math.
Learning 7(3), 245–274, doi 10.1023/A:1022103903080; Tall & Dubinsky (1991) in *Advanced
Mathematical Thinking*, Kluwer.

## Site plan (spec §9)

MkDocs Material + `pymdownx.arithmatex` (MathJax) + `mkdocs-jupyter` + `mkdocstrings[python]` +
`mkdocs-bibtex`. Pages: Home (cards, three-worlds map); Why and how to use it; Mathematics;
Derivations (generated ledger); Preconditioning; Case: ADCS trade study; Verification & validation
(generated); API and API reference; Extensions and limitations; Literature. Each page names the
world it serves. `scripts/build_generated.py` writes `docs/generated/` (gitignored) at build time.

## Deployment pattern (copy from)

- `/Users/z/Documents/GitHub/adcs-lifecycle-demo/.github/workflows/publish.yml`: build on push and
  PR to main, deploy only from main; `astral-sh/setup-uv` → `uv sync` → export steps into `_site/`
  → `actions/upload-pages-artifact@v3` → `actions/deploy-pages@v4` with `pages: write`,
  `id-token: write`, environment `github-pages`.
- `/Users/z/Documents/GitHub/hc-marimo/.github/workflows/deploy.yml`: same shape with
  `actions/checkout@v5`, `astral-sh/setup-uv@v7`, `upload-pages-artifact@v4`.
- Landing pages in both repos are hand-written `site/index.html` with one card per artifact and a
  "start wherever suits you" paragraph; reuse the tone, let MkDocs render the page.

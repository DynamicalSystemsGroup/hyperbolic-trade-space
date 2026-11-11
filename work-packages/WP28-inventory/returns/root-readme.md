# root-readme

## Q1. What each conveys

- Root page: why a trade-study method has to show its reasoning, say where the data stop and be rerunnable; what this method is (it explains tensions where PCA explains variance, it is a scikit-learn estimator); then it sends the reader to one of three places: the paper, the docs or the package.
- README: a one-paragraph technical description of the method (a monomial frontier V(m) = Π m_j^{w_j}, a coordinate chart, a scikit-learn estimator, SymPy derivations, an ADCS case), then a contributor's status line, a `uv sync` / `uv run pytest` quickstart and the repository layout keyed to work packages.

## Q2. Which Home page sentence each serves

- Root page: "The project page links the paper, ... these docs and the package." It is the only thing that sentence points to. Its "What" section also restates "beside PCA: PCA finds where the data spread, this finds where they stop, and the two chain."
- README: none directly. Its description paraphrases Home's opening ("learns the shape of a design trade space from evaluated designs ... fits a frontier model"), and its quickstart does not do what Home's "Getting started: install from source and run a first fit" promises: it builds a development environment and runs tests, with no fit.

## Q3. Verdicts

- Root page: **advances.** The Home page's closing sentence needs a project page that links the paper, the docs and the package, and only the root page does that. The "Why" section (what a decision-maker needs before trusting a model-based method) is also not carried on Home. The "What" section's PCA comparison repeats Home, but the page as a whole carries something nothing else does.
- README: **repeats.** Its description says what Home's first paragraph and the root page's opening sentence already say, in different and harder words. What it adds (the status line pointing to `work-packages/`, the layout with "WP1", "WP4, WP7", "site in WP8") is for someone working on the repository, and no sentence of the story needs it.

## Q4. What it repeats

- README repeats docs-index (Home page, first paragraph) and the root page (its opening sentence and its "What" section's "scikit-learn-compatible estimator").
- Within the root page, the "What" paragraph's PCA comparison repeats docs-index (Home's third paragraph).

## Q8. Judged against Home and against its own opening sentence

- Root page vs Home: it agrees with Home in substance but names the same things differently. Home says a monomial term "is one trade-off" and the package tells you "which metrics contend"; the root page calls this unit an "n-lemma" and talks about "tensions". Home says "where each design sits relative to the fitted reference surface"; the root page's second caption says "energy differential to that surface". A reader coming from one to the other has to work out that these are the same objects.
- Root page vs its own opening ("An unsupervised learning method which applies a posynomial invariant form ... to learn the shape of a trade space from evaluated designs"): the page delivers this. "Why" motivates it, "What" places it in unsupervised learning, the two figures show the shape, and the three cards point to where to go next.
- README vs Home: the same claim in other words, and with new terms Home does not use: "noisy, biased observations", a hyperbolic "space", "unit level set is the Pareto frontier", "SymPy-verified derivations", "ADCS" (Home says "cubesat"). Its install path (`uv sync`) differs from the root page's (`pip install git+...`) and Home's ("install from source").
- README vs its own opening ("Python package `hyperbolic_trade_space` (import alias `hts`); the method is the posynomial invariant form."): the description follows it, but the status, quickstart and layout sections are about the repository's internal process, not about the package or the method.

Paragraphs that serve neither:

- README: "Status: a 0.1 release candidate in preparation on `dev`. See `work-packages/README.md` ..." (internal process; "on `dev`" ties it to a moment in time).
- README: "## Layout" list, from "`src/hyperbolic_trade_space/` — the package" (work-package tags such as "(WP1)" and "site in WP8" mean nothing to an outside reader).
- README: "## Quickstart", from "uv sync # reproducible environment" (it runs the tests, not a first fit; it partly serves the opening sentence's package but not Home's "run a first fit").
- Root page: the parenthesis "(the tension report already runs PCA on the near-frontier chart coordinates)" serves neither: "tension report" and "chart coordinates" have not been introduced at that point.

## Q9. Read twice and still could not place

- Root page: "Its unit is the n-lemma": I cannot tell from the page alone whether the n-lemma is Home's "monomial term" or something else.
- Root page: "a design's energy differential to that surface": not defined on the page; I assume it is how far the design is from the reference surface, but the page does not say so.
- README: "a monomial, later posynomial, frontier": "later" could mean a later release or a later step of the fit.
- README: "learns a hyperbolic \"space\"": the quotation marks around "space" are not explained.
- README: "From noisy, biased observations": nothing else in the README, the root page or Home says what the method does about noise or bias.

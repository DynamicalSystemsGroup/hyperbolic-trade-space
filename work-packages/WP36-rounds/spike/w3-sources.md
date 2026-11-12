# WP36 spike W3: the sources of the two readouts, resolved and checked

Worker W3, 2026-11-12. Collects every source named in the sources lists of `w1-theorem-prover.md` (its "Sources" section) and
`w2-rust-wasm.md` (S-1 to S-27), groups URLs by work (one row per work, several URLs where the readout gives several for it), and
checks each with `curl -sIL` (a GET is retried when HEAD returns a non-200). `docs/references.bib` was not edited. The "in bib?"
column is a `grep -c` of the work's distinctive URL, DOI or name in `docs/references.bib` (0 hits for every work).

Count: 30 works, 52 URLs. Resolved: 30. Not resolved: 0. Two readout URLs did not resolve as written and were replaced, for
the same work, by a URL that does (both recorded in the table): the npm page for highs-js (403 to automated checks; the npm
registry URL returns 200) and the rust-digger page for slsqp-rssl (404; docs.rs returns 200). The W2 readout still cites the
two original URLs; the PM may want them corrected.

Not in the sources lists, so not checked and not in this table: Flocq (named in W1 section 5 as the Coq floating-point
library, no source entry); lean-mcp-lsp (named in W1 section 1 in the Dodds row, no source entry).

## Table

| key | what it is | resolved DOI or stable URL | checked (curl -sIL status, date) | already in docs/references.bib? (grep) |
|---|---|---|---|---|
| dodds2025claude | Mike Dodds, "Claude can (sometimes) prove it", Galois, 16 September 2025 (W1 s.1) | https://www.galois.com/articles/claude-can-sometimes-prove-it | 200, 2026-11-12 | no (grep "galois", "Dodds": 0) |
| anthropic2026fermat | Anthropic, "Formalizing Fermat's Last Theorem", research page; page metadata datePublished 2026-09-04 (W1 s.1) | https://www.anthropic.com/research/formalizing-fermats-last-theorem | 200, 2026-11-12 | no (grep "anthropic": 0) |
| dvorak2024duality | Dvo{\v r}{\'a}k and Kolmogorov, "Duality theory in linear optimization and its extensions -- formally verified" (arXiv 2409.08119; the arXiv record also gives journal DOI 10.46298/afm.14253, online 2026-03-06, which resolves; the journal version was not read) (W1 s.1) | DOI 10.48550/arXiv.2409.08119 (also https://arxiv.org/abs/2409.08119; journal DOI https://doi.org/10.46298/afm.14253) | 200 (arXiv abs, DOI, journal DOI), 2026-11-12 | no (grep "2409.08119", "46298": 0) |
| dvorak2024dualitycode | the Lean 4 duality code, tag v3.2.0 (W1 s.1) | https://github.com/madvorak/duality/tree/v3.2.0 | 200, 2026-11-12 | no (grep "madvorak": 0) |
| bentkamp2023verified | Bentkamp, Fernandez Mir and Avigad, "Verified reductions for optimization" (arXiv 2301.09347) (W1 s.1) | DOI 10.48550/arXiv.2301.09347 (also https://arxiv.org/abs/2301.09347) | 200 (arXiv abs, DOI), 2026-11-12 | no (grep "2301.09347", "Verified reductions": 0) |
| cvxlean | CvxLean, the Lean 4 convex-optimization reduction framework and GP case study (W1 s.1) | https://github.com/verified-optimization/cvxlean | 200, 2026-11-12 | no (grep "cvxlean", "CvxLean": 0) |
| fernandezmir2025iccopt | Fernandez Mir, Jackson, Bentkamp and Avigad, CvxLean ICCOPT 2025 slides (W1 s.1). The W1 readout used a search snippet only; the PDF was downloaded and read here for its metadata and text: title, four authors and creation date 2025-07-20 confirmed; "107 atoms" and "123 rewrite steps" appear in the text; the "4 variables, 8 constraints" detail was not checked | https://homepages.inf.ed.ac.uk/pbj/papers/iccopt25.pdf | 200, 2026-11-12 | no (grep "iccopt": 0) |
| mathlib4 | Mathlib, at commit af6dcfbf23867d9df7ee4835e28567fe509a2677 (W1 s.2 and sources) | https://github.com/leanprover-community/mathlib4/commit/af6dcfbf23867d9df7ee4835e28567fe509a2677 (repository https://github.com/leanprover-community/mathlib4) | 200 (commit URL, repository), 2026-11-12 | no (grep "mathlib": 0) |
| lean4floatref | Lean Language Reference, "Floating-Point Numbers", version 4.33.0 (W1 s.5) | https://lean-lang.org/doc/reference/4.33.0/Basic-Types/Floating-Point-Numbers/ | 200, 2026-11-12 | no (grep "lean-lang": 0) |
| george2026floatlib | George, Adkisson and Anandkumar, "FloatLib: Verified Floating-Point Arithmetic in Lean" (arXiv 2609.19352; date 2026-09-16) (W1 s.5) | DOI 10.48550/arXiv.2609.19352 (also https://arxiv.org/abs/2609.19352) | 200 (arXiv abs, DOI), 2026-11-12 | no (grep "2609.19352", "FloatLib": 0) |
| floatspec | FloatSpec, Lean package on Reservoir, a port of Flocq, incomplete per W1 (W1 s.5) | https://reservoir.lean-lang.org/@Beneficial-AI-Foundation/FloatSpec | 200, 2026-11-12 | no (grep "FloatSpec": 0) |
| flean | Flean, Lean floating-point formats and rounding modes (W1 s.5) | https://github.com/minusgix/flean | 200, 2026-11-12 | no (grep "flean": 0) |
| clarabel | Clarabel.rs, interior-point conic solver in Rust, version 0.11.1 (S-1 to S-4, S-23) | https://github.com/oxfordcontrol/Clarabel.rs ; docs https://clarabel.org/stable/ , https://docs.rs/clarabel/latest/clarabel/ ; changelog https://raw.githubusercontent.com/oxfordcontrol/Clarabel.rs/main/CHANGELOG.md | 200 (all five URLs), 2026-11-12 | no (grep "Clarabel", "clarabel": 0) |
| goodlp | good_lp, Rust modelling layer over several solvers (S-5) | https://docs.rs/good_lp/latest/good_lp/ ; README https://raw.githubusercontent.com/rust-or/good_lp/main/README.md | 200 (both), 2026-11-12 | no (grep "good_lp": 0) |
| microlp | microlp, pure-Rust simplex LP (S-6) | https://github.com/Specy/microlp/ ; https://docs.rs/crate/microlp/0.4.0 | 200 (both), 2026-11-12 | no (grep "microlp": 0) |
| minilp | minilp, archived 2022-09-22 (S-7) | https://github.com/ztlpn/minilp | 200, 2026-11-12 | no (grep "minilp": 0) |
| highsrust | highs crate, Rust bindings to HiGHS (S-8) | https://github.com/rust-or/highs | 200, 2026-11-12 | no (grep "rust-or/highs": 0) |
| highsjs | highs-js, HiGHS compiled to WebAssembly with Emscripten (S-9). The readout's npm page returns 403 to automated checks; the npm registry record for the same package is used as the resolved URL | https://github.com/lovasoa/highs-js ; https://registry.npmjs.org/highs (readout URL https://www.npmjs.com/package/highs: 403) | 200 (github), 200 (registry), npm page 403, 2026-11-12 | no (grep "highs-js", "lovasoa": 0) |
| slsqpcrate | slsqp crate, Rust translation of NLopt's SLSQP, version 1.0.x (S-10) | https://docs.rs/crate/slsqp/latest ; https://docs.rs/slsqp | 200 (both), 2026-11-12 | no (grep "slsqp": 0) |
| slsqprssl | slsqp-rssl, Rust port of SciPy's Fortran SLSQP (S-10). The readout's rust-digger URL returns 404 and crates.io returns 404; docs.rs returns 200 | https://docs.rs/slsqp-rssl (readout URL https://rust-digger.code-maven.com/crates/slsqp-rssl: 404) | 200 (docs.rs), 404 (rust-digger, crates.io), 2026-11-12 | no (grep "slsqp-rssl": 0) |
| argmin | argmin, Rust optimization toolbox (S-11) | https://argmin-rs.github.io/argmin/argmin/ | 200, 2026-11-12 | no (grep "argmin": 0) |
| verus | Verus, deductive verifier for Rust (S-12 to S-14) | https://github.com/verus-lang/verus ; guide https://verus-lang.github.io/verus/guide/ ; project goals https://raw.githubusercontent.com/verus-lang/verus/main/source/docs/project-goals.md | 200 (all three), 2026-11-12 | no (grep "Verus": 0) |
| creusot | Creusot, deductive verifier for Rust via Why3 (S-15) | https://github.com/creusot-rs/creusot ; guide https://guide.creusot.rs | 200 (both), 2026-11-12 | no (grep "Creusot": 0) |
| kani | Kani, model checker for Rust (S-16 to S-18) | https://model-checking.github.io/kani/ ; https://github.com/model-checking/kani/blob/main/docs/src/tool-comparison.md ; https://github.com/model-checking/kani/blob/main/docs/src/rust-feature-support.md | 200 (all three), 2026-11-12 | no (grep "Kani": 0) |
| prusti | Prusti, Viper-based verifier for Rust (S-19, S-20) | https://www.pm.inf.ethz.ch/research/prusti.html ; https://github.com/viperproject/prusti-dev ; guide https://prusti.github.io/prusti/user-guide/ | 200 (all three), 2026-11-12 | no (grep "Prusti": 0) |
| rustf64 | Rust standard library documentation, primitive f64 (S-21) | https://doc.rust-lang.org/std/primitive.f64.html | 200, 2026-11-12 | no (grep "rust-lang.org": 0) |
| rustwasm32 | Rust platform support, wasm32-unknown-unknown target (S-22) | https://doc.rust-lang.org/rustc/platform-support/wasm32-unknown-unknown.html | 200, 2026-11-12 | no (grep "wasm32": 0) |
| jangda2019wasm | Jangda, Powers, Berger and Guha, "Not So Fast: Analyzing the Performance of WebAssembly vs. Native Code", USENIX ATC 2019, pp. 107-120 (S-24). No DOI; the USENIX page is the stable URL | https://www.usenix.org/conference/atc19/presentation/jangda | 200, 2026-11-12 | no (grep "Jangda", "usenix": 0) |
| wasmspec | WebAssembly Core Specification, numerics (S-25) | https://webassembly.github.io/spec/core/exec/numerics.html | 200, 2026-11-12 | no (grep "webassembly.github.io": 0) |
| pyodide | Pyodide documentation: packages in Pyodide (S-26) and WebAssembly constraints (S-27) | https://pyodide.org/en/stable/usage/packages-in-pyodide.html ; https://pyodide.org/en/stable/usage/wasm-constraints.html | 200 (both), 2026-11-12 | no (grep "pyodide": 0) |

Not resolved: none. The two readout URLs that failed as written are the npm page (highsjs) and the rust-digger page (slsqprssl), both
listed above with the URL that resolves for the same package.

## BibTeX for the resolved works not yet in docs/references.bib

Paste into `docs/references.bib` in one block. The file's convention is kept: each entry carries a `verified` field
(date; how it was checked; record URL). Software and documentation entries have no authorship in the readouts; where the
author field is the project's organization or account name taken from the URL, it is marked as such in the `verified` field,
and `year = {n.d.}` follows the file's existing convention for undated pages.

```bibtex
@misc{dodds2025claude,
  author       = {Dodds, Mike},
  title        = {Claude Can (Sometimes) Prove It},
  howpublished = {Galois article},
  year         = {2025},
  note         = {Published 16 September 2025},
  url          = {https://www.galois.com/articles/claude-can-sometimes-prove-it},
  verified     = {2026-11-12; curl -sIL 200; page metadata read from the Galois record: title, author Mike Dodds, date September 16 (year 2025 from the W1 readout); https://www.galois.com/articles/claude-can-sometimes-prove-it},
}

@misc{anthropic2026fermat,
  author       = {{Anthropic}},
  title        = {Formalizing {Fermat}'s Last Theorem},
  howpublished = {Anthropic research page},
  year         = {2026},
  note         = {Page metadata: datePublished 2026-09-04, dateModified 2026-10-14},
  url          = {https://www.anthropic.com/research/formalizing-fermats-last-theorem},
  verified     = {2026-11-12; curl -sIL 200; page metadata read (title, datePublished 2026-09-04); the article text was read by W1 through a fetch tool, not here; https://www.anthropic.com/research/formalizing-fermats-last-theorem},
}

@misc{dvorak2024duality,
  author       = {Dvo{\v r}{\'a}k, Martin and Kolmogorov, Vladimir},
  title        = {Duality theory in linear optimization and its extensions -- formally verified},
  howpublished = {arXiv:2409.08119},
  year         = {2024},
  doi          = {10.48550/arXiv.2409.08119},
  note         = {The arXiv record gives journal DOI 10.46298/afm.14253 (online 2026-03-06), which also resolves; the journal version was not read},
  verified     = {2026-11-12; curl -sIL 200 for the arXiv abstract, the arXiv DOI and the journal DOI; arXiv citation metadata read (title, authors, date 2024/09/12, abstract: Farkas-like theorems over linearly ordered fields in Lean 4); https://arxiv.org/abs/2409.08119},
}

@misc{dvorak2024dualitycode,
  author       = {{madvorak}},
  title        = {duality},
  howpublished = {Lean 4 code repository, tag v3.2.0},
  year         = {n.d.},
  url          = {https://github.com/madvorak/duality/tree/v3.2.0},
  verified     = {2026-11-12; curl -sIL 200; author field is the GitHub account name from the URL; https://github.com/madvorak/duality/tree/v3.2.0},
}

@misc{bentkamp2023verified,
  author       = {Bentkamp, Alexander and Fern{\'a}ndez Mir, Ramon and Avigad, Jeremy},
  title        = {Verified reductions for optimization},
  howpublished = {arXiv:2301.09347},
  year         = {2023},
  doi          = {10.48550/arXiv.2301.09347},
  verified     = {2026-11-12; curl -sIL 200 for the arXiv abstract and the arXiv DOI; arXiv citation metadata read (title, three authors, date 2023/01/23, abstract: a Lean framework for verified reductions of optimization problems); https://arxiv.org/abs/2301.09347},
}

@misc{cvxlean,
  author       = {{verified-optimization}},
  title        = {{CvxLean}},
  howpublished = {GitHub repository},
  year         = {n.d.},
  url          = {https://github.com/verified-optimization/cvxlean},
  verified     = {2026-11-12; curl -sIL 200; author field is the GitHub organization name from the URL; the README was read by W1, not here; https://github.com/verified-optimization/cvxlean},
}

@misc{fernandezmir2025iccopt,
  author       = {Fern{\'a}ndez Mir, Ramon and Jackson, Paul and Bentkamp, Alex and Avigad, Jeremy},
  title        = {{CvxLean}: a convex optimization modeling framework based on the {Lean} 4 proof assistant},
  howpublished = {ICCOPT 2025 slides},
  year         = {2025},
  url          = {https://homepages.inf.ed.ac.uk/pbj/papers/iccopt25.pdf},
  verified     = {2026-11-12; curl -sIL 200; PDF downloaded and text extracted (16 pages, creation date 2025-07-20): title and four authors as printed; the figures 107 atoms and 123 rewrite steps appear in the text; https://homepages.inf.ed.ac.uk/pbj/papers/iccopt25.pdf},
}

@misc{mathlib4,
  author       = {{The mathlib Community}},
  title        = {Mathlib, commit af6dcfbf23867d9df7ee4835e28567fe509a2677},
  howpublished = {Lean 4 library, GitHub},
  year         = {2026},
  url          = {https://github.com/leanprover-community/mathlib4/commit/af6dcfbf23867d9df7ee4835e28567fe509a2677},
  note         = {Head of master on 2026-11-12, as read by W1 over a shallow clone},
  verified     = {2026-11-12; curl -sIL 200 for the commit URL and the repository; https://github.com/leanprover-community/mathlib4/commit/af6dcfbf23867d9df7ee4835e28567fe509a2677},
}

@misc{lean4floatref,
  title        = {Floating-Point Numbers},
  howpublished = {Lean Language Reference, version 4.33.0},
  year         = {n.d.},
  url          = {https://lean-lang.org/doc/reference/4.33.0/Basic-Types/Floating-Point-Numbers/},
  verified     = {2026-11-12; curl -sIL 200; page read by W1 through a fetch tool: logical model Float.Model, transcendental functions opaque in the logic; https://lean-lang.org/doc/reference/4.33.0/Basic-Types/Floating-Point-Numbers/},
}

@misc{george2026floatlib,
  author       = {George, Robert Joseph and Adkisson, Will and Anandkumar, Anima},
  title        = {{FloatLib}: Verified Floating-Point Arithmetic in {Lean}},
  howpublished = {arXiv:2609.19352},
  year         = {2026},
  doi          = {10.48550/arXiv.2609.19352},
  verified     = {2026-11-12; curl -sIL 200 for the arXiv abstract and DOI; arXiv citation metadata read (title, three authors, date 2026/09/16, abstract); proofs and benchmarks not read; https://arxiv.org/abs/2609.19352},
}

@misc{floatspec,
  author       = {{Beneficial-AI-Foundation}},
  title        = {{FloatSpec}},
  howpublished = {Lean package, Reservoir},
  year         = {n.d.},
  url          = {https://reservoir.lean-lang.org/@Beneficial-AI-Foundation/FloatSpec},
  verified     = {2026-11-12; curl -sIL 200; author field is the Reservoir owner name from the URL; W1 reports it incomplete with sorry while porting; https://reservoir.lean-lang.org/@Beneficial-AI-Foundation/FloatSpec},
}

@misc{flean,
  author       = {{minusgix}},
  title        = {{Flean}},
  howpublished = {GitHub repository},
  year         = {n.d.},
  url          = {https://github.com/minusgix/flean},
  verified     = {2026-11-12; curl -sIL 200; author field is the GitHub account name from the URL; https://github.com/minusgix/flean},
}

@misc{clarabel,
  author       = {{oxfordcontrol}},
  title        = {{Clarabel.rs}: an interior-point solver for conic problems in {Rust}},
  howpublished = {Rust crate, version 0.11.1, repository and documentation},
  year         = {n.d.},
  url          = {https://github.com/oxfordcontrol/Clarabel.rs},
  note         = {Documentation https://clarabel.org/stable/ and https://docs.rs/clarabel/latest/clarabel/; changelog in the repository},
  verified     = {2026-11-12; curl -sIL 200 for all five URLs; author field is the GitHub organization name from the URL; https://github.com/oxfordcontrol/Clarabel.rs},
}

@misc{goodlp,
  author       = {{rust-or}},
  title        = {{good\_lp}: a linear programming modelling layer for {Rust}},
  howpublished = {Rust crate, documentation and README},
  year         = {n.d.},
  url          = {https://docs.rs/good_lp/latest/good_lp/},
  note         = {README https://raw.githubusercontent.com/rust-or/good_lp/main/README.md},
  verified     = {2026-11-12; curl -sIL 200 for both URLs; author field is the GitHub organization of the rust-or project; the solver table and determinism statement were read by W2; https://docs.rs/good_lp/latest/good_lp/},
}

@misc{microlp,
  author       = {{Specy}},
  title        = {{microlp}},
  howpublished = {Rust crate and GitHub repository},
  year         = {n.d.},
  url          = {https://github.com/Specy/microlp/},
  note         = {Crate page https://docs.rs/crate/microlp/0.4.0},
  verified     = {2026-11-12; curl -sIL 200 for both URLs; author field is the GitHub account name from the URL; https://github.com/Specy/microlp/},
}

@misc{minilp,
  author       = {{ztlpn}},
  title        = {{minilp}},
  howpublished = {Rust crate, GitHub repository, archived 2022-09-22},
  year         = {n.d.},
  url          = {https://github.com/ztlpn/minilp},
  verified     = {2026-11-12; curl -sIL 200; author field is the GitHub account name from the URL; archive status as read by W2; https://github.com/ztlpn/minilp},
}

@misc{highsrust,
  author       = {{rust-or}},
  title        = {{highs}: Rust bindings to the {HiGHS} solver},
  howpublished = {Rust crate, GitHub repository},
  year         = {n.d.},
  url          = {https://github.com/rust-or/highs},
  verified     = {2026-11-12; curl -sIL 200; author field is the GitHub organization of the rust-or project; https://github.com/rust-or/highs},
}

@misc{highsjs,
  author       = {{lovasoa}},
  title        = {{highs-js}: {HiGHS} compiled to {WebAssembly}},
  howpublished = {GitHub repository and npm package {highs}},
  year         = {n.d.},
  url          = {https://github.com/lovasoa/highs-js},
  note         = {npm registry record https://registry.npmjs.org/highs},
  verified     = {2026-11-12; curl -sIL 200 for the GitHub repository and the npm registry record; the npm web page https://www.npmjs.com/package/highs returns 403 to automated checks; author field is the GitHub account name from the URL; https://github.com/lovasoa/highs-js},
}

@misc{slsqpcrate,
  title        = {{slsqp}: {SLSQP} in {Rust}, a translation of {NLopt}'s {SLSQP}},
  howpublished = {Rust crate, version 1.0.x, documentation},
  year         = {n.d.},
  url          = {https://docs.rs/crate/slsqp/latest},
  note         = {Documentation https://docs.rs/slsqp},
  verified     = {2026-11-12; curl -sIL 200 for both URLs; no author field taken from the crate page, which W2 read through a search summary; https://docs.rs/crate/slsqp/latest},
}

@misc{slsqprssl,
  title        = {{slsqp-rssl}: a port of {SciPy}'s {Fortran} {SLSQP} to {Rust}},
  howpublished = {Rust crate, documentation},
  year         = {n.d.},
  url          = {https://docs.rs/slsqp-rssl},
  note         = {The readout's rust-digger page https://rust-digger.code-maven.com/crates/slsqp-rssl returned 404 on 2026-11-12},
  verified     = {2026-11-12; curl -sIL 200 for docs.rs; rust-digger and crates.io returned 404; no author field taken from the page; https://docs.rs/slsqp-rssl},
}

@misc{argmin,
  title        = {{argmin}: a pure-{Rust} numerical optimization toolbox},
  howpublished = {Rust crate, documentation},
  year         = {n.d.},
  url          = {https://argmin-rs.github.io/argmin/argmin/},
  verified     = {2026-11-12; curl -sIL 200; no author field taken from the documentation page; https://argmin-rs.github.io/argmin/argmin/},
}

@misc{verus,
  author       = {{The Verus project}},
  title        = {{Verus}: a verifier for {Rust}},
  howpublished = {GitHub repository and guide},
  year         = {n.d.},
  url          = {https://github.com/verus-lang/verus},
  note         = {Guide https://verus-lang.github.io/verus/guide/; project goals in the repository},
  verified     = {2026-11-12; curl -sIL 200 for the repository, the guide and the project-goals file; the feature table (floating point: partially supported) was read by W2; https://verus-lang.github.io/verus/guide/},
}

@misc{creusot,
  author       = {{The Creusot project}},
  title        = {{Creusot}: a deductive verifier for {Rust}},
  howpublished = {GitHub repository and guide},
  year         = {n.d.},
  url          = {https://github.com/creusot-rs/creusot},
  note         = {Guide https://guide.creusot.rs},
  verified     = {2026-11-12; curl -sIL 200 for the repository and the guide; the guide page returned a fragment to W2; https://github.com/creusot-rs/creusot},
}

@misc{kani,
  author       = {{The Kani developers}},
  title        = {{Kani}: a model checker for {Rust}},
  howpublished = {Documentation book and repository},
  year         = {n.d.},
  url          = {https://model-checking.github.io/kani/},
  note         = {Tool comparison https://github.com/model-checking/kani/blob/main/docs/src/tool-comparison.md; floating-point support https://github.com/model-checking/kani/blob/main/docs/src/rust-feature-support.md},
  verified     = {2026-11-12; curl -sIL 200 for the book and both repository pages; the statements on bounded checking and on precision properties were read by W2; https://model-checking.github.io/kani/},
}

@misc{prusti,
  author       = {{The Viper project}},
  title        = {{Prusti}: an automated verifier for {Rust}},
  howpublished = {Project page, GitHub repository and user guide},
  year         = {n.d.},
  url          = {https://www.pm.inf.ethz.ch/research/prusti.html},
  note         = {Repository https://github.com/viperproject/prusti-dev; user guide https://prusti.github.io/prusti/user-guide/},
  verified     = {2026-11-12; curl -sIL 200 for all three URLs; author field is the GitHub organization of the Viper project (viperproject) from the repository URL; https://www.pm.inf.ethz.ch/research/prusti.html},
}

@misc{rustf64,
  author       = {{The Rust Project}},
  title        = {Primitive type {f64}},
  howpublished = {Rust standard library documentation},
  year         = {n.d.},
  url          = {https://doc.rust-lang.org/std/primitive.f64.html},
  verified     = {2026-11-12; curl -sIL 200; the statements on exp, ln and sqrt precision were read by W2; https://doc.rust-lang.org/std/primitive.f64.html},
}

@misc{rustwasm32,
  author       = {{The Rust Project}},
  title        = {{wasm32-unknown-unknown}} target},
  howpublished = {Rust platform support documentation},
  year         = {n.d.},
  url          = {https://doc.rust-lang.org/rustc/platform-support/wasm32-unknown-unknown.html},
  verified     = {2026-11-12; curl -sIL 200; https://doc.rust-lang.org/rustc/platform-support/wasm32-unknown-unknown.html},
}

@inproceedings{jangda2019wasm,
  author    = {Jangda, Abhinav and Powers, Bobby and Berger, Emery D. and Guha, Arjun},
  title     = {Not So Fast: Analyzing the Performance of {WebAssembly} vs. Native Code},
  booktitle = {2019 USENIX Annual Technical Conference (USENIX ATC 19)},
  year      = {2019},
  pages     = {107--120},
  url       = {https://www.usenix.org/conference/atc19/presentation/jangda},
  verified  = {2026-11-12; curl -sIL 200; USENIX page metadata read (title, four authors, pages 107-120, ISBN 978-1-939133-03-8); no DOI; https://www.usenix.org/conference/atc19/presentation/jangda},
}

@misc{wasmspec,
  author       = {{WebAssembly Community Group}},
  title        = {{WebAssembly} Core Specification: Numerics},
  howpublished = {Specification},
  year         = {n.d.},
  url          = {https://webassembly.github.io/spec/core/exec/numerics.html},
  verified     = {2026-11-12; curl -sIL 200; the IEEE 754 and NaN statements were read by W2; https://webassembly.github.io/spec/core/exec/numerics.html},
}

@misc{pyodide,
  author       = {{The Pyodide project}},
  title        = {Pyodide documentation: packages in Pyodide and {WebAssembly} constraints},
  howpublished = {Documentation},
  year         = {n.d.},
  url          = {https://pyodide.org/en/stable/usage/packages-in-pyodide.html},
  note         = {Constraints https://pyodide.org/en/stable/usage/wasm-constraints.html},
  verified     = {2026-11-12; curl -sIL 200 for both URLs; the package list (scipy 1.18.0, numpy 2.4.6, scikit-learn 1.8.0, clarabel 0.11.1, highspy 1.13.1 and others) was read by W2; https://pyodide.org/en/stable/usage/packages-in-pyodide.html},
}
```

## Notes for the PM

- Keys follow the file's style (surname, year, first title word), with software keyed by its name. Before pasting, check that none of these keys already exists in `docs/references.bib` (the grep above found none of the URLs or DOIs, so none is expected).
- `dvorak2024duality` cites the arXiv record and its DOI, as the W1 readout does; the journal DOI found in the arXiv record resolves and may be preferred once the journal version is read.
- The `fernandezmir2025iccopt` entry is backed by the PDF text for the two figures named; the W1 readout's "4 variables, 8 constraints" figure is not checked here.
- Entries for software and documentation carry a GitHub or Reservoir account name as the author field where the readouts gave no author; the `verified` field says so, and a reviewer may replace them with the maintainers' names.

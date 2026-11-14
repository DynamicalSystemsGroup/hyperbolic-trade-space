# WP42 — Decisions: tension, the glossary's layers, the entry surfaces (the build after the spike)

The scope's approval of 2026-11-14, 16:55 and the rulings that shaped it are in `WP11-decisions.md` ("The abstract pass"). This file holds his calls on the spike's readout (`WP42-rounds/spike/readout.md`) and on the build.


## The readout's build shape (2026-11-14, 20:30; popup over the readout's Scope A, B, C)

**Supervisor, verbatim:** "Scope A, all of it"

**Applied as:** the build is the readout's Scope A: lemma L21 into `derivation/`, the definition beside elasticity
(Section 4) with the Appendix A and B rows, `tension_matrix` and `design_tensions` in the package with doctests and
finite-difference tests, the Figure 7 decision (item 3, after the cold read), the glossary and checker changes with the
schema amendment to the interface contract, the mechanical loss pass over paper, `src/` and docs, the entry-surface
edits, Section 3's paragraph, and the docs page on the routes back to attributes and the design space. The naming items
of the readout's section 7 are put to him one at a time; the build's scope amendment waits for them.

## Naming item 1, the unoccupied region of the chart (2026-11-14, 20:35; popup)

**Supervisor, verbatim:** "whitespace. we should reserve hole for future work where we use this peicewise-affine space and data to create distances and
then simplicial complexes to find topological holes. these will emerge naturally when we start sampling strategically, and we
need a way to define them which will allow us to go beyond the envelope method. this is its research spike but to characterize
a direction of future work that leverages our coordinate system and data points along with persistent homology. you will
notice from my other work that i am very interested in topological data analysis. white space for now. hole reserve for future
work. current spike is just research to establish a clear future direction based on TDA"

**Applied as:** the one word is **white space** (the glossary entry, with hole and gap for this object as avoided
variants; gap stays with the term gap and the gaps ledger). **Hole is reserved**: it is not defined in 0.1 and the
checker flags it, so that it is free for the object he names, a topological hole found from the chart's coordinates and
the data by persistent homology. That direction is its own research spike, WP50 (`WP50-scope-of-work.md`, decisions in
`WP50-decisions.md`): a readout that characterizes the future work (distances from the piecewise-affine chart and the
sampled designs, simplicial complexes, persistent homology, strategic sampling, beyond the envelope method), nothing
built.

## Naming item 2, the package's names (2026-11-14, 22:50; popup with the driver's recommendation, at his request: "give me the open questions for scope 42A one at a time with recommendations and justifications")

**Supervisor, verbatim:** "Rename all (Recommended)"

**Applied as:** `tension_report` becomes `trade_off_report`; `tension_directions` and `tension_loadings` become
`spread_directions` and `spread_loadings`; `plot_tensions` becomes `plot_association`; `tension_matrix` and
`design_tensions` are new members of the report. README, root page, user guide and paper follow in the same unit;
no deprecation path (nothing released); the interface contract is amended with the build.


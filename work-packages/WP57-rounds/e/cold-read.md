# WP57e: the unit's cold read of the re-lettered supporting material (1,280 px)

The built site (`cd paper && BASE_URL=/paper uv run --frozen myst build --html`, a clean log) served on port 8907
(`scratchpad/serve57e`, a link to `paper/_build/html`), captured headless by Playwright (Chrome) at 1,280 by 900 with
`work-packages/WP57-rounds/e/capture.py`; the server was stopped after. Page checks by the capture script: the eight
appendix headings read A to H in the order of first mention (A Register of prior art, B Extended results, C HoroPCA,
D Notation and terms, E Proofs, F The case's model, G Assumptions, limitations and open questions, H Computational
reproducibility); every new anchor (`appendix-a` to `appendix-h`, `sub-a-1`, `sub-b-1` to `sub-b-14`, `sub-c-1` to
`sub-c-4`, `sub-e-1` to `sub-e-3`, `sub-f-1` to `sub-f-8`, `sub-g-1` to `sub-g-3`, `sub-h-1` to `sub-h-4`, the four
table labels `tab-g-assumptions-1`, `tab-g-cited-1`, `tab-g-gaps-1`, `tab-c-hypothesis-1`) resolves; none of the
sampled old anchors (`sub-d-3`, `sub-d-16`, `sub-d-19`, `sub-c-8`, `sub-g-4`, `sub-h-5`, `sub-e-4`) is on the page; no
in-page link points at a missing id; page scroll width 1,280.

| Capture | What a reader meets | Found | Done |
|---|---|---|---|
| `nav-top.png` | The supporting page opens on Appendix A, the register of prior art, and A.1; the outline "In this article" is collapsed | the register is the first thing under the page title, as Section 2's first mention puts it | nothing |
| `nav-open.png` | The outline opened: A and A.1, then B.1 to B.14 in order (the full list, C.1 to C.4, D with no subsection, E.1 to E.3, F.1 to F.8, G.1 to G.3, H.1 to H.4, is in the capture script's printed text) | consecutive numbers under every letter; D (the notation table) has no subsection, as before | nothing |
| `A-opening.png` | Appendix A, A.1 The register, the first family | further down (the page text, not in the frame), the register's HoroPCA row names "Appendix C" and the hyperbolic-graph row "Appendix D" for the word, both from `prior_art.yaml` and both the new letters | nothing |
| `B-opening.png` | Appendix B, its pointer line to the supplement files, B.1 Exponents and terms | B opens where D opened; its subsections run B.1 to B.14 | nothing |
| `C-opening.png` | Appendix C, C.1 to C.3: the hypothesis, the experiment, the results | the text is H's word for word; the table caption reads "Appendix C's hypothesis table" | nothing (see the review: a plain-text appendix name in a caption that the references test never read) |
| `D-opening.png` | Appendix D, the notation table, its first rows | further down (the page text), the "Defined in" column's two rows that name a subsection read B.12 and B.6, from `glossary.yaml` | nothing |
| `E-opening.png` | Appendix E, "What the scripts establish" (links to Appendix G and Appendix F), the proof map | the links name the new letters and land on the assumptions and the case model | nothing |
| `F-opening.png` | Appendix F, F.1 Configurations and its table | C's text under F | nothing |
| `G-opening.png` | Appendix G, G.1 Assumptions, Table 2 | the supporting page's table numbers follow the new order: the HoroPCA table is now Table 1, so the assumptions table is Table 2 (it was Table 1 under E) | nothing; tables are numbered by MyST in page order |
| `H-opening.png` | Appendix H, H.1 The pinned toolchain | the commit row reads the base commit of this branch, as at every execution | nothing |
| `pointer-s2-b11-source.png`, `pointer-s2-b11-target.png` | Section 2's HoroPCA paragraph: "use PCA as a downstream step (Appendix B.11)"; the link opens the supporting page at B.11 Chaining with PCA, the outline highlighting B.11 | lands on its target (`#sub-b-11`) | nothing |
| `pointer-s6-g-source.png`, `pointer-s6-g-target.png` | Section 6's last line, "Appendix G records what the results leave open"; the link opens G, G.1 Assumptions and Table 2 | lands on its target (`#appendix-g`) | nothing |

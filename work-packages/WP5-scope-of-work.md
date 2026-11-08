# WP5 — Scope of work: Literature review and bibliography

| | |
|---|---|
| **Status** | DRAFT. Approved only by the recorded act below. Nothing in this package is executed before then. |
| **Supervisor (accountable)** | mzargham |
| **Repository** | `DynamicalSystemsGroup/posynomial-invariant-form` (local: `/Users/z/Documents/GitHub/posynomial-invariant-form`) |
| **Approval record** | Verbal approval in chat, quoted verbatim in `work-packages/WP5-decisions.md` |
| **Acceptance record** | Verbal acceptance in chat, quoted verbatim in `work-packages/WP5-decisions.md`, after the review report `work-packages/WP5-review.md` |

## Purpose

The method's lineage claims (spec §2 "Kind of model", §4 "Lineage", novelty and white space, the posynomial/GGP
extension and the kernel research direction) must rest on sources that exist and say what we claim. WP5 builds the
bibliography and a discursive literature review in which every entry has been resolved, during this package, by a
DOI or stable URL, and a hygiene test that keeps the bibliography in that state. Later packages (WP3's `api.md`, WP6's
mathematics narrative, WP8's site) cite its keys. The names in the plan and in
`docs/superpowers/notes/references-verified.md` are candidates to verify, not facts.

## Goals

- G1. `docs/references.bib`: every entry resolved by DOI or stable URL against the live record, with its resolution recorded.
- G2. `docs/literature.md`: a discursive review organized around the method's lineage, in which every claim cites a bib key and no reference appears that is not in the bib.
- G3. A citation-hygiene test that guards both files.
- G4. Candidates that could not be verified are dropped explicitly, with a reason, instead of being cited from memory.

## Non-goals

- No MkDocs configuration, `mkdocs-bibtex` wiring or site build (WP8); the review uses the `[@key]` citation syntax that mkdocs-bibtex consumes.
- No mathematics narrative, `method.md`, limitations page or `api.md` (WP6, WP3); WP5 supplies keys, not those pages.
- No new runtime or test dependencies (the hygiene test is offline and parses BibTeX with the standard library).
- No claims beyond what a source says: the review characterizes lineage and prior art, it does not assert priority or novelty of the method.
- No change to the spec or notes, except that a corrected fact found while verifying is reported as an observation for the supervisor.

## Deliverables

| ID | Deliverable | Serves |
|---|---|---|
| D-1 | `docs/references.bib` | G1 |
| D-2 | `docs/literature.md` | G2, G4 |
| D-3 | `tests/test_references.py` | G3 |
| D-4 | `work-packages/WP5-decisions.md` (approval record) | G1–G4 |

## Requirements

| ID | Requirement | Checked by |
|---|---|---|
| R-1 | Every entry in `docs/references.bib` has a resolvable DOI or, when no DOI exists, a stable URL (publisher, repository handle, institutional archive or arXiv), and records its verification date and what was checked in a `verified` field | `uv run pytest tests/test_references.py`; inspection of the `verified` fields |
| R-2 | Each entry was resolved during this package against the live record (WebFetch or WebSearch of the DOI/URL or publisher page): authors, year, title, venue, volume and pages in the entry match the record; nothing enters the bib from memory | reviewer re-resolves a sample of at least 10 entries, including every entry cited in spec §4 |
| R-3 | The bib is syntactically valid: unique keys in `author<year><word>` form, balanced braces, required fields per entry type | `test_references.py` |
| R-4 | Every citation `[@key]` in `docs/literature.md` resolves to a bib key, and every bib key is cited at least once in `docs/literature.md` | `test_references.py` |
| R-5 | The review covers each lineage topic of spec §2 and §4, each with at least one verified source: Cobb–Douglas and Shephard distance functions; deterministic/stochastic frontiers (Aigner–Chu, Aigner–Lovell–Schmidt, COLS); DEA and super-efficiency (Charnes–Cooper–Rhodes, Andersen–Petersen) and Malmquist/productivity indices (Färe et al.); entropic risk and the softened support function; log-ratio/compositional analysis (Aitchison, Egozcue et al.) and PCA; geometric programming and generalized posynomials (Boyd et al., Hoburg et al., Magnani–Boyd); kernel PCA and disambiguation from hyperbolic PCA (HoroPCA); Pareto/hypervolume and tradespace exploration; convex-analysis and duality foundations used by the inherited axioms I1 to I4 (Boyd–Vandenberghe, Rockafellar, strong law of large numbers); scikit-learn's API and design; and the framing sources (Tall, Sfard, Buchberger, Artigue, the SciPy 2026 paper) | inspection against this list |
| R-6 | Each citation supports the specific statement it is attached to; the review marks claims about method priority or novelty as the supervisor's, not established by the sources | reviewer reads the passages around a sample of citations against the sources |
| R-7 | Every candidate named in `references-verified.md` or in the plan that was dropped is listed in a short appendix to `docs/literature.md` with the reason (unverifiable, not relevant, superseded) | inspection |
| R-8 | The inherited axioms I1 to I6 of the WP1 ledger each have a verified source for their stated theorem (e.g. LP strong duality, strong law of large numbers, support functions, the square-matrix inverse fact), with the citation key listed next to the axiom in the review's appendix | inspection against `derivation/axioms.py` |
| R-9 | Suite, linters and lock pass; nothing outside scope changed: `git diff --stat` shows only `docs/references.bib`, `docs/literature.md`, `tests/test_references.py` and `work-packages/` | run the commands; inspect the diff |
| R-10 | No AI attribution lines; commits authored as Michael Zargham | `git log` grep returns 0; CI check |

## Definition of good

- A reader sees where the method sits: what is classical (Cobb–Douglas, frontiers, DEA, GP), what is borrowed (entropic risk, log-ratio analysis), what is the supervisor's combination, and what the sources do not say.
- Honest on priority: close neighbours (super-efficiency, stochastic frontier, Malmquist, Pareto-based gap metrics) are presented as prior art, with the difference stated carefully.
- The verification trail is auditable: a reader can follow each `verified` note to the record that was checked.
- Concise: the review is proportionate to the package and does not turn into a survey of unrelated fields.

## Definition of good enough

- Deliverables D-1 to D-4 exist at the stated paths.
- R-1 to R-10 pass as checked, with evidence in the review report.
- Non-goals untouched (no site wiring, no narrative pages, no new dependencies).
- No bib entry is unresolved; unverifiable candidates are dropped and listed (R-7), not included.

## Definition of done

Good enough is met, **no open item remains unresolved**, and the supervisor has accepted the work by the acceptance record above.

## Agent's defaults

All marked *(default)* where they appear; the supervisor approves or changes the list as one item.

- Bib keys `author<year><firstword>` in lower case, e.g. `hoburg2016data`; entry types `article`, `book`, `inproceedings`, `misc` as appropriate *(default)*.
- Verification field *(default)*: a custom `verified = {YYYY-MM-DD; <how>; <record URL>}` on every entry; BibTeX ignores unknown fields. The hygiene test requires its presence and a date.
- DOI is stored in `doi`; where there is no DOI the stable URL is in `url`; arXiv-only items are allowed when the arXiv record is the stable record *(default)*.
- Hygiene test *(default)*: parses the bib with a small regex/brace-matching parser using only the standard library (no new dependency, no lock change); checks key uniqueness and format, required fields per type, DOI pattern `10.\d{4,9}/\S+` or an `https://` URL, a `verified` field with an ISO date; checks citations in `literature.md` of the form `[@key]` (multiple keys separated by `;`) against the bib and that every key is cited. It is offline (CI has no network); live resolution is done in the package and audited in review.
- Citation syntax in `literature.md` is `[@key]` and `[@key1; @key2]` for mkdocs-bibtex compatibility *(default)*.
- Structure of `literature.md` *(default)*: Introduction and how to read it; one section per lineage topic in R-5 order; "What is the supervisor's combination, and what the sources do not say"; Appendix A: candidates dropped (R-7); Appendix B: sources for inherited axioms I1 to I6 (R-8).
- Candidate list handling *(default)*: verify each name in `references-verified.md` and the plan (Aigner & Chu 1968; Charnes, Cooper & Rhodes 1978; Ahmadi-Javid; Aitchison 1983 and 1986; Egozcue et al. 2003; Rockafellar; Boyd & Vandenberghe; Schölkopf et al.; Chami et al. 2021; Zitzler & Thiele 1999; Ross, Hastings et al. 2004; Buchberger 1990; Artigue 2002; Sfard 1991; Tall 2008 and 2013; Tall & Dubinsky 1991; Pedregosa et al. 2011; Buitinck et al. 2013) and add other sources only when a lineage claim needs one; verified details replace remembered ones.
- Where a book has no DOI, an ISBN-bearing publisher or library record is the stable URL *(default)*.
- Tools *(default)*: WebFetch and WebSearch for resolution; Crossref/DOI.org/publisher/arXiv records as the checked record; paywalled items are checked against the publisher's abstract page or Crossref metadata, and the `verified` note says so.
- Length *(default)*: the review is about 2000 to 4000 words; entries about 30 to 50.
- Style: Markdown with LaTeX only where a formula is needed; discursive prose; no emojis *(default)*.
- Commits prefixed "WP5: "; bib and test first, then the review, then status table and decisions file; files `work-packages/WP5-decisions.md` and `WP5-review.md` follow the WP1 format *(default)*.
- WP6 and WP3's `api.md` consume the keys; if later packages need a source not in the bib they add it under the same hygiene test in their own scope *(default)*.

## Open decisions (for the supervisor)

None at problem level: spec §2, §4 and §9 and the references note answer them. The Agent's defaults list above is the one item for the supervisor to approve or change at the scope gate.

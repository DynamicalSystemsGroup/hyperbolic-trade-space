# WP5 — Review report

| | |
|---|---|
| **Scope of work** | `work-packages/WP5-scope-of-work.md` |
| **Scope approval verified** | Recorded in `work-packages/WP5-decisions.md` ("Scope approval", commit bcfe110, 2026-11-07 21:11, before the work commits at 21:19): supervisor (mzargham) verbatim "double check with the github cli but then let's move forward"; defaults approved as one item; open decisions none. The project has no PRs; this is the recorded act the scope names. The record is typed by the agent, so the review cannot confirm the chat itself. The approval is worded conditionally ("double check ... but then") and the file does not record that the check was done (see G-1). The file dates the approval 2026-11-08 while the commit is dated 2026-11-07. |
| **Work reviewed** | `main`, commits `442a538` and `2d2c10e` (touching `docs/references.bib`, `docs/literature.md`, `tests/test_references.py`). Diff base `bcfe110`. Reviewer did not build the work. Trial edits were restored with `git checkout`; none committed. |
| **Supervisor (accepts)** | mzargham |
| **Acceptance record** | Verbal acceptance in chat, quoted verbatim in `work-packages/WP5-decisions.md`, after this report |

Every command below was run in this session (`unset VIRTUAL_ENV`, `uv run ...`). The working tree also holds other packages' uncommitted files (`pyproject.toml`, `examples/`, `tests/test_adcs_case.py`); they are ignored.

## Deliverables

| ID | Verdict | Evidence |
|---|---|---|
| D-1 | met | `docs/references.bib`: 35 entries (`grep -c '^@'`). |
| D-2 | met | `docs/literature.md`: 2393 words, 223 lines; Appendix A (dropped candidates) and Appendix B (axiom sources) present. |
| D-3 | met | `tests/test_references.py`, 150 lines, standard library only. |
| D-4 | met | `work-packages/WP5-decisions.md` exists with an approval record (see the caveat in the table header and G-1). The acceptance entry reads "pending". |

## Requirements

| ID | Verdict | Evidence |
|---|---|---|
| R-1 | met | `uv run pytest tests/test_references.py`: 7 passed. All 35 entries carry a DOI or https URL and a `verified` field with a date and an http record URL (`test_every_entry_has_doi_or_https_url`, `test_every_entry_records_its_verification`). Inspection of the fields: each says what was checked and whether the text was read. |
| R-2 | met, with weak spots | I re-resolved 22 entries. 18 via live Crossref (`curl https://api.crossref.org/works/<doi>`): andersen1993, aigner1977, charnes1978, hoburg2016, boyd2007 (page range not in Crossref; the author's page is the stated source), magnani2009, boyd2004, rockafellar1970, horn2012, aitchison1983, zitzler1999, ross2004, ahmadijavid2012, egozcue2003, zargham2026, dubinsky1991, shephard1970, buchberger1990. Authors, year, title, venue, volume, issue and pages all match the bib. Crossref confirms the recorded oddities (Shephard spelled "Shepherd"; Dubinsky first; Magnani online 2008-03-25). By WebFetch: fare1994 (IDEAS page: four authors, AER 84(1), 66-83, 1994, matches) and chami2021 (PMLR: title, four authors, PMLR 139, 1419-1429, matches). By WebSearch only: aigner1968 (EconBiz: Aigner and Chu, AER 58(4), 826-839, matches; ALS 1977 described by secondary text as the mathematical-programming approach) and cobb1928 (AER 18 supplement, pp. 139-165, JSTOR 1811556 matches via web search only; the JSTOR page was not opened). The Föllmer PDF URL resolves (HTTP 200, PDF). Those two (Aigner and Chu 1968, Cobb-Douglas 1928) and the Föllmer notes remain secondary-record or single-source checks, as the implementer disclosed. All spec section 4 entries (Andersen-Petersen, Färe et al., ALS, Aigner-Chu, Cobb-Douglas, Hoburg et al., Aitchison, Charnes et al.) were in the sample. 3 inherited-axiom sources (boyd2004, rockafellar1970, horn2012) were resolved at the bibliographic level only; billingsley2012 was not re-fetched (Open Library, not Crossref). |
| R-3 | met | Tests `test_keys_unique_and_well_formed`, `test_required_fields_per_type` pass. Observation O-3: `foellmer2026entropic` carries `year = {n.d.}` but a 2026 key. |
| R-4 | met | `test_every_citation_resolves_to_the_bib` and `test_every_bib_key_is_cited` pass. Trials: (a) appending an entry with no `verified` field to the bib made `test_every_entry_records_its_verification` and `test_every_bib_key_is_cited` fail (2 failed, 5 passed); (b) appending `[@missing2020key]` to `literature.md` made `test_every_citation_resolves_to_the_bib` fail (1 failed, 6 passed); both restored with `git checkout`, tree clean for these files. |
| R-5 | partly met | Covered with a verified source: Cobb-Douglas, Shephard (Shephard, Färe-Primont, Farrell); Aigner-Chu and ALS; DEA, super-efficiency, Malmquist; entropic risk (Föllmer notes, Ahmadi-Javid); Aitchison, Egozcue; Boyd et al., Hoburg et al., Magnani-Boyd; kernel PCA and HoroPCA; hypervolume and tradespace; Boyd-Vandenberghe, Rockafellar, Billingsley; scikit-learn; Tall, Sfard, Buchberger, Artigue, SciPy 2026 paper. Gaps: (1) COLS has no source (the scope lists it as a topic); it is honestly dropped in Appendix A and the text says so. (2) Pareto gap and spacing metrics have no source (Appendix A); hypervolume is attached to Zitzler and Thiele with the admission that the abstract does not confirm it. (3) PCA itself is covered only through Aitchison. See G-2. |
| R-6 | partly met | Passages around 10 citations read against the sources (see the passage review below). Priority and novelty are consistently marked as the supervisor's, and the COLS attribution is not asserted. Three small citation-support issues: G-3, G-4, G-5. |
| R-7 | met | Appendix A lists COLS, Malmquist originals, Pareto gap/spacing, Kolmogorov's paper, GPfit docs, Föllmer-Schied and COLS/Greene-Winsten with reasons. Every named candidate in `references-verified.md` and the scope's defaults list is either in the bib or in Appendix A. The appendix also records corrections to the seed notes. |
| R-8 | met, with a note | Appendix B lists I1 to I6 with keys, and its statements agree with `derivation/axioms.py` (I1 LP strong duality, I2 SLLN, I3 support function, I4 softmax-affine GP-compatibility, I5 MGF of independent sums, I6 left inverse equals right inverse). Keys match the citations in `axioms.py` (Boyd-Vandenberghe 5.2, Billingsley, Rockafellar 13, Hoburg et al., Horn-Johnson). Only I1 (table of contents of the authors' PDF) and I4 (abstract) have any content check; I2, I3, I5, I6 are bibliographic records only, and the mapping of I5 to Billingsley and I6 to Horn-Johnson passages was not read. The appendix says this. |
| R-9 | met | `uv run pytest -q`: 133 passed. `uv run ruff check .`: all checks passed. `uv run ruff format --check .`: 51 files already formatted. `uv lock --check`: resolved, no change. `git diff --stat 442a538^..2d2c10e`: only `docs/literature.md`, `docs/references.bib`, `tests/test_references.py` (773 insertions). |
| R-10 | met | `git log bcfe110..HEAD` grep for Co-Authored-By or Generated: 0 hits. Authors of both commits: Michael Zargham. |

### Passage review for R-6

| Citation and statement | Judgement |
|---|---|
| cobb1928: weighted geometric mean with exponents summing to one is the Cobb-Douglas form introduced in 1928 | Supported by the record; consistent with the paper's 1/4, 3/4 exponents. |
| shephard1970, fare1995: distance function as an alternative description of technology; chapter "Distance Functions" | Supported by title and chapter record; reading of V as a distance function explicitly assigned to the spec. |
| aigner1968: deterministic frontier, mathematical-programming estimation | Supported by secondary text only; the review says the paper was not read. Mild: "estimated ... so that outputs do not exceed the function" goes slightly past the secondary evidence. G-3. |
| andersen1993, fare1994: closest prior art; super-efficiency scores above one | Supported by abstracts. "Closest prior art" is a judgement; the text hedges the difference as untested. |
| foellmer2026: definition, limits mean and essential supremum | Supported by the extracted PDF text; the identification with the method's objective is labelled as the authors' algebra. Source is unpublished notes, see O-3. |
| rockafellar1970: closed convex set determined by support function | Supported by section title only; the text says so. |
| egozcue2003: chart "in the spirit of" an ilr chart | Hedged correctly. |
| magnani2009: "the max of affine functions is the kappa-to-infinity limit of the softmax-affine form" | The citation follows a statement the paper (as checked: bibliographic record) is not shown to make. The limit is the project's own mathematics. G-4. |
| ross2004: "closest named prior art for exploring a design space by its attributes" | Superlative not supported by any checked source. G-5. |
| chami2021: HoroPCA extends PCA components to hyperbolic space; unrelated to the spec's "hyperbolic" | Supported by the abstract. |
| zitzler1999: cited for hypervolume | Text admits this was not confirmed. Honest. |
| Final section: priority and novelty not established; COLS not sourced | Appropriately modest; no priority or novelty claim found anywhere in the text. The COLS attribution in the spec is flagged as unconfirmed, not repeated. |

## Definition of good enough

| Item | Verdict | Evidence |
|---|---|---|
| D-1 to D-4 exist at the stated paths | met | See Deliverables. |
| R-1 to R-10 pass as checked | not met strictly | R-5 and R-6 are partly met (G-2 to G-5); the rest pass. |
| Non-goals untouched (no site wiring, no narrative pages, no new dependencies) | met | Diff shows three files only; `uv lock --check` unchanged; no mkdocs files. |
| No unresolved bib entry; unverifiable candidates dropped and listed | met | Appendix A; test passes. |

## Outside the scope

- **Out-of-scope changes:** none by WP5. `git diff --stat 442a538^..2d2c10e` lists only the three deliverable files. The spec and notes were not modified; corrections are reported as observations in Appendix A.
- **Non-goals touched:** none. The `[@key]` syntax is used; no mkdocs configuration.

## Observations (not counted as failures)

- **O-1.** The offline test checks that a `verified` field has a date and an http URL; it cannot detect a wrong or stale record. Accuracy rests on the live resolution (re-run by this review for 22 entries, no mismatch found).
- **O-2.** Only Boyd-Vandenberghe (table of contents) and Hoburg et al. (abstract) have any content check among the axiom sources. The Appendix B closing paragraph says strong duality in 5.2.3 "was read in the authors' PDF" but the entry says only the table of contents was read; the wording slightly overstates.
- **O-3.** The sole source for the entropic risk definition is unpublished notes with an unknown year (key `foellmer2026entropic` suggests 2026). A published source (Föllmer and Schied) was considered and dropped.
- **O-4.** The scope's reference to "SLLN" as a topic is met by a textbook (Billingsley) rather than the original; Appendix A says so.
- **O-5.** The decisions-file approval date (2026-11-08) differs from the commit date (2026-11-07).

## Open decisions (for the supervisor)

- **G-1.** The recorded approval is "double check with the github cli but then let's move forward" and the decisions file does not say the check was done. Is the approval effective as recorded? Options: accept as is / fix before acceptance (record that the check was done and re-confirm) / follow-up work package.
- **G-2.** R-5 has no source for COLS and none for Pareto gap/spacing metrics; the review states this openly and does not cite them. Options: accept as is / fix before acceptance / follow-up work package.
- **G-3.** Aigner and Chu 1968 and Cobb-Douglas 1928 are checked only through secondary or search records, and the Aigner-Chu sentence slightly exceeds that evidence. Options: accept as is / fix before acceptance / follow-up work package.
- **G-4.** Magnani and Boyd is cited after a statement (max of affine is the limit of the softmax-affine form) that is the project's own mathematics, not shown to be in the paper. Options: accept as is / fix before acceptance / follow-up work package.
- **G-5.** Ross et al. is called "the closest named prior art" for attribute-based design-space exploration, which no checked source supports. Options: accept as is / fix before acceptance / follow-up work package.
- **G-6 (observations O-1 to O-5, as one item).** Accept these as is, or pick any to act on. Options: accept as is / fix before acceptance / follow-up work package.

## Gap dispositions

Resolved through the decision loop (`~/.claude/skills/CLAUDE.md`); records go in `work-packages/WP5-decisions.md`.

| Gap | Disposition (accept as is / fix before acceptance / follow-up work package) | Reason or follow-up |
|---|---|---|
| G-1 | pending | |
| G-2 | pending | |
| G-3 | pending | |
| G-4 | pending | |
| G-5 | pending | |
| G-6 | pending | |

## Recommendation

Provisional on the dispositions above: recommend acceptance with the listed gaps noted. The deliverables exist, the hygiene test passes and fails correctly on both trials, the suite, linters and lock are green, nothing outside scope changed, 22 entries re-resolved with no bibliographic mismatch, and the text never asserts priority or novelty. The gaps are a missing COLS source (honestly dropped), three thinly checked sources, and two citation-support wording issues. Gaps G-2 to G-5 touch good-enough items R-5 and R-6, so the supervisor should decide them before accepting. If any is set to fix before acceptance, the whole review is rerun.

Acceptance is the supervisor's act, recorded as named above. This report does not accept the work.

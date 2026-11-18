# WP81 — Review report: the paper as a working paper (0.2 documentation improvement, package 1)

| | |
|---|---|
| **Scope of work** | `work-packages/WP81-scope-of-work.md` |
| **Scope approval verified** | His answer "Approved" in the popup of 2026-11-17, quoted verbatim in `work-packages/WP81-decisions.md` ("WP81 approved"), after OD1 ("Remove until a pin") and OD2 ("Approve the list", with his review method folded in as R-8) |
| **Work reviewed** | Branch `v0.2`, from the scope's commit 41d3dce9 to the head that carries this report; nothing on `dev` or `main` (`git branch --contains HEAD` lists only `v0.2`) |
| **Supervisor (accepts)** | mzargham |
| **Acceptance record** | His word in chat after the technical verification and his read of the reworded pages, quoted verbatim in `WP81-decisions.md` |

Three fresh-context passes by reviewers who did not build the work: the first at 87547daa checked every item and
found six gaps (four of bookkeeping, two of checks still running); his direction on the lemma scripts then changed
six pages; the second pass re-checked the changed items and the closed gaps at 2703c0f9. Every command ran with
`MPLCONFIGDIR` set to a scratch folder (the worktree's matplotlib font cache, recorded in `WP76-decisions.md`).

## Deliverables

| ID | Verdict | Evidence |
|---|---|---|
| D-1 | met | `git diff 41d3dce9..HEAD` touches the eleven surfaces: every `(paper:` citation gone from the home, theory (8), bridge (4), temperature (4), examples, Further reading, fitting, termination; the limitations page's "Appendix E of the paper" and, on his word, its three sentences on the lemma scripts and theorem provers gone; the root page's body sentence and the README's first paragraph reworded |
| D-2 | met | `notes/paper-references.md`: the rule (no `paper:` link while the mode is abstract; the two jobs; no lemma scripts in the docs), the 26-row inventory with a disposition on every row (brief from the paper; removed as the paper's role; names the working paper; one out of scope), the naming sentences as landed, the test named |
| D-3 | met | register rows C192, C195, C216, C375, C841 re-anchored to the new text; C083's source note records the HoroPCA rewording; rows C390, C567, C568 retired with the sentences that left the limitations page (ids never reused); no fragment carries `paper:`; `tests/test_claims_register.py` 22 passed |
| D-4 | met | `WP81-decisions.md` (his direction, the breakdown, the 0.2 line, OD1, OD2, the review method, the two jobs, the lemma scripts, the page's name, the word budget); `WP81-rounds/`: `journeys.md` (sections 1 to 3), `journeys/` (twelve before- and twelve after-reports, verbatim), `captures/` (27 pages before), `captures-after/` (the touched pages after), `captures-review/` (the touched pages at 1280 and 375 px, light and dark), `capture.mjs`, `site-read-2026-11-17.md`; the INDEX row 81; this report |

## Requirements

| ID | Verdict | Evidence |
|---|---|---|
| R-1 | met | `grep -rn "paper:" docs README.md site/index.html` finds no citation on a docs page; the greps of "the paper" and "working paper" over the docs, README and root page match the inventory's rows (the first pass found the README's two map lines missing; added to row 22; row 20 corrected to describe the untouched code-owners page) |
| R-2 | met | The first pass read five rewritten sentences against the diff: each is the docs' own statement no wider than before (theory's homogeneity, bridge's "planned and not shipped", temperature's two limits, limitations, Further reading's HoroPCA clause backed by the WP35 readout); the second pass read the lemma-script removals as removals, not rewordings; the two naming sentences say the abstract is published and the full text builds from the repository (`test_the_working_paper_is_named_where_the_rule_says`, `test_docsite_cites_the_paper_only_through_keys` pass); the paper's apparatus (lemma scripts, `derivation/`) is named nowhere on a docs page (his word) |
| R-3 | met | Root page: "The working paper makes the argument and gives the proofs; its abstract is published here and the full text builds from the repository." README: "the working paper's abstract (the full text builds from `paper/`)". The root-page tests pass (`-k "root_index or history" -m "not slow"`, 21 passed); the register holds; the root card's line per mode is the composer's and is left (passed to the v0.1 session with the readers' words) |
| R-4 | met | `mkdocs build --strict` in the abstract slot and with `HTS_PAPER_SLOT=pin`: "Documentation built", no warning, in both passes |
| R-5 | met | Vocabulary 0 new; the budgets hold on every page; the docsite total is 12,030 against the cap of 12,055 (the home 289 of 350, Further reading 228 of 300), 19 words fewer than before the package, so the default "the docsite total stays" holds and `TOTAL_BUDGET` is unchanged (an earlier rise was recorded and superseded, `WP81-decisions.md`, "The word budget"); the residual check's strict exit is the repository's pre-existing baseline drift on untouched surfaces (WP76's G-1); the checker's metanarration patterns over the touched pages find only each page's pre-existing lead line |
| R-6 | met | The touched pages captured at 1280 and 375 px in light and dark (`captures-review/`; no sideways scroll; the scheme applied per capture); the reviewers and the author looked at the home, theory, Further reading, bridge, temperature and limitations captures and read the sentences as the files say; the cold reader of the home and theory pages said what the paper is (a working paper, abstract public), where it is (the abstract on the project page, the full text built from the repository) and what a link gets them (the abstract, not the full text), right on both |
| R-7 | met | `ruff check .` clean; `ruff format --check .` clean; `uv lock --check` resolved; the page tests (site, docs, register, references, contract, index) pass; the fast suite 2,012 passed at 87547daa and at the content head 2703c0f9 (2,012 passed, 12 skipped, 2 xfailed, 329 s); no attribution line in the files or the commit messages; `git diff --name-only 41d3dce9..HEAD` maps to D-1 to D-4 and the defaults, plus the Kitchenham page's title and navigation entry on his word, recorded in the decisions file |
| R-8 | met | The twelve journeys traced before any edit with a screenshot per page (`captures/`), the returns verbatim, the findings per persona and per pointer with the competing preferences and the choice (section 2), the journeys re-traced after (section 3, `captures-after/`), and his word on the one preference that outlived the re-trace (the theorists' route through the lemma scripts) recorded there |

## Definition of good enough

| Item | Verdict | Evidence |
|---|---|---|
| R-1 to R-8 on one commit, evidence from a fresh-context reviewer | met | the two passes above |
| The cold reader's two answers right | met | R-6 |
| His read of the reworded pages | pending by design | the acceptance gate |

## Outside the scope

- **Out-of-scope changes:** the Kitchenham example page's title and navigation entry ("Kitchenham software projects"), on his word of 2026-11-17 (`WP81-decisions.md`, "The page's name").
- **Non-goals touched:** none. Nothing under `src/` or `paper/`; `pyproject.toml`, `uv.lock`, `scripts/paper_keys.py`, `scripts/assemble_site.py`, `paper/mode.toml` and `paper/paper-keys.json` untouched; `dev` and `main` untouched; no pull request.

## Observations (not counted as failures)

- The root page's card title "Read the paper" with the composer's abstract-mode line still read as a promise to four persona readers; the card is the composer's, passed to the v0.1 session with their words.
- The readers' residuals that are later packages' are listed in `journeys.md` section 2 (packages 3 to 6) and section 3 (a build command or lemma index, which his word on the lemma scripts settles against).
- The scope's R-3 command needs `-m "not slow"`: without it the selection pulls in a network-bound history test.
- The persona readers saw a stage whose root page lacked its two figures (the hand-assembled stage; the composer copies them); the root capture was retaken and the after-state readers saw the figures.
- The fast suite at the content head 2703c0f9: 2,012 passed, 12 skipped, 2 xfailed in 329 s (`uv run pytest -q -m "not slow and not paper"`); the six changed pages' four-way captures retaken at that head (`captures-review/`, 40 files).

## Open decisions (for the supervisor)

None. Every item was resolved through the decision loop (`WP81-decisions.md`); the two gaps the first pass left to
running checks closed with their results, and the four bookkeeping gaps were fixed and re-checked.

## Gap dispositions

| Gap | Disposition | Reason or follow-up |
|---|---|---|
| First pass, gaps 1 and 2 (the four-way captures and the cold read and fast suite still running) | closed | `captures-review/` retaken at 2703c0f9; the cold read; the fast suite 2,012 passed at 2703c0f9 |
| First pass, gaps 3 to 6 (the README map lines and the code-owners row in the inventory; the budget numbers; the Kitchenham rename unrecorded) | fixed, re-checked by the second pass | unit 3 |

## Recommendation

Recommend acceptance: every pointer into the paper is out of the docs under his rule, each former pointer is the
docs' own brief statement or gone as the paper's role, the paper is named as a working paper on the home, in Further
reading, on the root page and in the README, the lemma scripts are named nowhere in the docs on his word, the twelve
persona journeys were traced before and after with screenshots and their competing preferences written out, and the
checks are green on the reviewed head.

Acceptance is the supervisor's act, recorded as named above. This report does not accept the work.

## Unit 4: the README and the install text (after acceptance, on his word of 2026-11-17, late evening)

Reviewed against his words quoted in `WP81-decisions.md` ("The README and the install text") and the driver
session's brief: the README reflects the released state; the docs' install text leads with the released package.

| Item | State | Evidence |
|---|---|---|
| The one-line description | met | the first sentence is `pyproject.toml`'s `description` with the package named as its subject; the second is his clause for observed cases (2026-11-17) |
| Install from PyPI, clone for contributors | met | `pip install tradespace`, `uv add tradespace`; then `git clone` and `uv sync`; the same order on `docs/getting-started.md`, whose prose count is 348 of 348 (`tests/test_site.py::test_word_budgets_hold`) |
| The first fit: the same code, the same output | met | the block is the getting-started page's first block; run on the branch it prints `trilemma [0 1 2]` and `[0.3  0.37 0.33]`, the page's words |
| The links | met | the docs, the project page, the working paper's abstract with the full text building from the repository (the naming of unit 1), `CONTRIBUTING.md`, `GOVERNANCE.md`, the code owners' page, `CODE_OF_CONDUCT.md`, `SECURITY.md`, `CHANGELOG.md`, `CITATION.cff`; every repository file exists; every docs address is a navigation entry of `mkdocs.yml` |
| The layout, line by line against the tree | met | `ls` of the root: seven lines keep `src/`, `docs/`, `examples/` (five examples; `examples/adcs/` named), `paper/` and `site/`, `derivation/`, `tests/` and `scripts/`, `work-packages/` and `notes/`; dropped: the register, `glossary.yaml` and `history.yaml`, `CLAUDE.md`, `mkdocs.yml`, `Dockerfile`, `pyproject.toml`, `uv.lock`, `.python-version`, `LICENSE`, `.github/` and the dot-files (a user does not open them); `CHANGELOG.md` and `GOVERNANCE.md` are linked in Contributing |
| No metanarration | met | `scripts/check_residuals.py`: `README.md` metanarration 0; no opener of the kind on the README or the page |
| Vocabulary check | met | `uv run python scripts/check_vocabulary.py`: 0 new violations, 67 known |
| Rendered in a browser, captured | met | the README rendered through GitHub's own Markdown renderer (`gh api /markdown`, file mode) with GitHub's stylesheet, served locally and captured headless at 1280 px, light and dark: `WP81-rounds/readme/readme-1280-{light,dark}.png`, `captures.json` (no console error, no sideways scroll); after the driver session pushed the branch, the blob view on GitHub at 9e64d44d captured the same way: `readme-github-blob-9e64d44d-1280-light.png`, the same rendering |
| The install verified against PyPI | met | PyPI served `tradespace` 0.1.0 at 01:35 UTC (the Release run 44207809538 green; tag `v0.1.0` on 74e62fda). In a fresh virtual environment outside the repository: `uv venv venv --python 3.12`, `uv pip install --python venv/bin/python tradespace` (`+ tradespace==0.1.0`), `__version__` `0.1.0`, then the getting-started block prints `trilemma [0 1 2]` and `[0.3  0.37 0.33]`; the commands and their output verbatim in `WP81-rounds/readme/pypi-install.txt` |

Observations: the residual checker, against its baseline of `c0fe11b` (stale for the whole tree, WP76 G-1), reports the
README's compound sentences 1 to 3, acronyms at first use 0 to 3 (PyPI, MIT, API, names in a README) and glossary
terms at first use 1 to 6 (the first-fit paragraph's terms, defined on the getting-started page it links); the README
grew from 191 to about 370 prose words. The README on `dev` since 0.1 (WP78's pointer at `GOVERNANCE.md`) is kept
in the Contributing paragraph. With the 0.1 site deployed, every address the README links to answers 200 except the
Kitchenham page, which is this branch's content (WP76) and is served from the 0.2 release; the link holds on the branch
and in the pull request's review, and dangles on the live site until then.

The fast suite at the unit's head 9e64d44d (`uv run pytest -q -m "not slow and not paper"`): 2,045 passed, 12 skipped, 2 xfailed.

Addendum (his word of 22:55 EST, the figure): the root page's planted triangle is in the README by its deployed address,
which answers 200 (`image/png`, 282,360 bytes); PyPI's own renderer (`readme_renderer` with its Markdown extra) accepts
the file and emits the image; GitHub's renderer shows it (`readme-1280-{light,dark}.png` retaken); the sentence under it
uses the glossary's terms (metrics, shares, trade, term, characteristic point); the vocabulary check is unchanged at 0
new violations. Observation: the figure's background is transparent (63 per cent of its pixels), so in GitHub's dark scheme the three
corner labels (`favours metric 1`, `2`, `3`), dark ink outside the tinted triangle, are lost against the page, while the
triangle, its regions, labels and markers read; pypi.org renders a light page only, where the figure reads whole
(`readme-1280-dark.png`). A dark variant through `<picture>` is stripped by PyPI's renderer, and GitHub's per-scheme
address fragments would show two images on PyPI; an opaque background would need the site's figure rebuilt, a root-page
change outside this unit. Left for his word.


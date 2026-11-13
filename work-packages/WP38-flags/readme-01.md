# WP38 flags: readme-01

Slot: readme-01. Head: 8e846a9. Pages read: README.md (as the file text; the GitHub-rendered view was not opened, per the brief's fallback). Checker signals read via `scripts/check_residuals.py`.

| Surface | Location | Sentence (in full) | Kind (1 to 10) | Disposition | Reason |
|---|---|---|---|---|---|
| README.md | line 3 | For analysts with a table of evaluated designs, to learn which metrics trade: the [docs](https://dynamicalsystemsgroup.github.io/hyperbolic-trade-space/docs/), [the paper](https://dynamicalsystemsgroup.github.io/hyperbolic-trade-space/paper/), `examples/adcs/` for a case study. | 9 | split | Colon-and-comma fragment is hard to parse in one pass; reorder as two sentences without adding words. |
| README.md | line 11 | # package only: uv sync --no-default-groups; uv run --no-default-groups | 4 | keep | Code comment giving the install variant a package-only user needs; earns its place. |
| README.md | line 25 | ts = HyperbolicTradeSpace(temperature=20.0).fit(M)  # real table: `select_temperature` | 4 | keep | Short pointer in code that names the function a real table needs; carries a fact. |
| README.md | line 32 | `docs/`: the user guide and API reference, built into the docs site; `docs/superpowers/` holds the notes the checks apply (conventions, notation, source lists). | 4 | cut | The second clause and its parenthetical detail the internals of a notes folder a new reader does not need here. |
| README.md | line 41 | `work-packages/`: the build's record (scopes, reviews, decisions, round outputs, build notes, outlines and spike folders); not needed to use the method. | 4 | cut | The seven-item list gives detail the closing clause ("not needed to use the method") makes unnecessary; cut the list, keep the clause. |
| README.md | line 44 | `mkdocs.yml`, `Dockerfile`, `pyproject.toml`, `uv.lock`, `.python-version`: build and environment files; `LICENSE`; `.github/` (the CI workflows), `.gitattributes`, `.gitignore` and `.dockerignore`: repository settings. | 9 | split | Two colons, a semicolon and a parenthesis in one sentence; split into two list items. |
| README.md | line 44 | `.github/` (the CI workflows), `.gitattributes`, `.gitignore` and `.dockerignore`: repository settings. | 4 | cut | Naming each housekeeping file is detail a reader does not need; "repository settings" covers it. |
| README.md | line 43 | `CLAUDE.md`: conventions for contributors working with Claude Code. | 10 | keep | "Claude Code" is a proper product name, clear in context; stays. |

Count by disposition: cut 3, split 2, keep 3, move 0, define 0, routed 0. Total 8 rows.
Could not read: the GitHub-rendered view (file text read instead, as the brief directs); the browser was not needed for any other surface.

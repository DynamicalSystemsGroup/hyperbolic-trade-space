# WP8b — Decisions (release preparation for 0.1.0)

Approvals and acceptances are the driver's under the mandate (`release-candidate.md`, "The mandate"); the
supervisor's words are quoted verbatim where they bind; the driver's calls are listed for his review at the PR.
The driver records each deliverable's verdict here (`WP8b-scope-of-work.md`, Agent's defaults).

## Scope gate (2026-11-09)

Recorded in `driver-log.md` (2026-11-09), quoted verbatim:

> - 2026-11-09: WP8b (release preparation) and WP20 (verification in tiers) scoped by the fresh PM's
>   bounded scope subagents in the template, no open decisions; approved by the driver under the
>   mandate. WP8b brings the items done ahead of its scope (LICENSE, changelog, punch list, archive)
>   under it and sequences the reference keys and the reviewer's guide after WP11's stopping rule and
>   the version last. WP20 covers the slow markers, `scripts/check.py`, the xdist group and the CI
>   shards; its first two commits are already on `dev` (04a3471, 78f5e1c) and are accepted against it.

For the driver: the scope's header (`WP8b-scope-of-work.md`, Status) still reads DRAFT although its Gate outcomes
section records this approval. The header is left as it is until the driver updates it.

## Amendment 1


## Amendment 1, the driver's decisions (2026-11-10, 23:05)

- **OD-A1 (a), with (c) as the fallback.** Pin the article theme's version in `paper/myst.yml` if `mystmd` resolves a
  versioned site template; if it does not (the implementer shows the attempt), `scripts/stage_site.py` fetches or
  copies the templates itself before the build (c). Either way the proof is a test or a CI step that stages the site
  from a clean worktree with no copy by hand.
- **OD-A2 (a).** D-6 lands inside 0.1 after WP28 is accepted, as the supervisor's words of 2026-11-08 and step 6 of the
  path record; nothing here changes his recorded word.

**Driver, verbatim:** "Amendment 1 approved with OD-A1 (a) falling back to (c) on evidence, and OD-A2 (a)."

## Amendment 1, the executor's units (2026-11-11, from `dev` c6d7353; the driver's D-5 and D-7 not touched)

Screenshots and logs are under `/private/tmp/claude-501/-Users-z--claude-spares-spare-4Zb8mW/71474a52-35d3-48fa-82b0-c1328e96b5d6/scratchpad/wp8b/`.

| Unit | Commit | What and evidence |
|---|---|---|
| D-2 (R-2, R-11) | d4fdb30 | The swap sentence replaced by what WP16 and WP23 changed (the nine-attribute datasets, event-detected settling time, the K = 1, 2, 3 record and the paper's numbers regenerated, every moved number in `swap-evidence.md`); entries for WP19 to WP28 that changed what a user or reader sees (WP20 as developer tooling). `grep -o 'WP[0-9]*[a-z]*' CHANGELOG.md` now lists WP19 to WP28. The heading `[Unreleased] - target 0.1.0` is left for the candidate PR's rename (the driver's step). |
| D-3 (R-3, R-12; WP25-4 T-8) | 2ee252d | Archive item ticked (4bd6bac; contract amendment 18 for the manifest line); the version item rewritten to D-5's wording, "at the candidate PR, no tag"; root and paper pages listed once under the post-release checks (the three URLs stay in "Expected-at-release links" for the link check); the reference-keys and container-image duplicates kept once; 22 boxes become 20 (the three expected-link boxes left, the releases-page box joined the post-release checks), each ticked, struck with a cited decision, or labelled post-release. `uv run pytest tests/test_site.py -k "punch or link"`: 6 passed. |
| D-8 (OD-A1; R-14; WP25-4 T-10) | 15dbff8 | See "OD-A1 evidence" below. |
| D-6 (R-6, R-13) | cfbad4f | See "D-6" below. |

### OD-A1 evidence

- **Reproduced.** A fresh worktree with no copy: `scripts/stage_site.py` falls back to the placeholder after the theme's prerender fails (`Error: No route matches URL "/paper/_public/fig-nlemma-....png"`; `baseline-stage.log`).
- **Cause.** `template: article-theme` resolves through `api.mystmd.org` to the git URL `https://github.com/myst-templates/article-theme.git`, which `mystmd` 1.12.0 turns into `archive/refs/heads/main.zip` (`myst.cjs`, `downloadTemplate`: the branch is `main` unless the command line says `--branch`; there is no version syntax in a template name). That repository's `main` moved to v2.0.0 on 2026-11-10 (commit af3f43a20c; layout `renderer/` and `server/` where 1.4.1 had `build/` and `server.js`). The main checkout's `paper/_build/templates` holds `template.zip` of commit 4acce1eba558 (v1.4.1, 2026-09-21), which is why it kept working.
- **Answer to the driver's (a) test.** `mystmd` does not resolve a versioned template name, but it takes a template that is a URL ending in `.zip` (`resolveInputs`, `validateUrl`; no API lookup), and GitHub serves any commit as a zip. `paper/myst.yml` now reads `template: https://github.com/myst-templates/article-theme/archive/4acce1eba558b301c2aadca99a7804aa6e294e1e.zip` (v1.4.1, the commit the paper was reviewed on), with a comment saying why. This is a pin in `paper/myst.yml` (option (a)'s file); no fallback to (c) was needed. It depends on GitHub serving that archive (a network fetch at build time, as before).
- **Test.** `tests/test_site.py::test_paper_theme_is_pinned_to_a_commit` fails if the template is a name or a branch archive.
- **Clean-worktree staging (R-14).** `git worktree add .../clean-stage 15dbff8` (no `paper/_build`), `uv sync --locked`, `uv run python scripts/stage_site.py`: log line `Fetching template from .../archive/4acce1e....zip`, no "did not build", `_stage/paper/` holds the real paper (`clean-stage.log`; 101 s with the sync). Served at 127.0.0.1:8793 and read in the executor's own tab: title and table of contents of the paper, Figure 1 with its caption and the "Shows / Does not show" line, 0 broken images of 10 (`theme-pin-clean-worktree-paper-top.jpg`, `theme-pin-clean-worktree-paper-figure1.jpg`). Worktree removed.
- **Not done here.** `PM-BRIEF.md` line 523 still says a fresh worktree copies the main checkout's templates before staging; that note is obsolete with this pin (PM-BRIEF is not in this unit's files; reported to the PM). `stage_site.py` still falls back to the placeholder with a stderr line when the paper does not build, by design; WP25-4 G-3's note (the figures before MkDocs) needs no sentence because `assemble_site` builds the figures first.

### D-6

- **Keys.** The scope's "none carry one today" is out of date: every numbered section and appendix of the two notebooks already carries a MyST target (`(sect-problem)=`, `(appendix-b)=`, `(sub-d-4)=`), beside the 37 `:label:` values (90 keys in all). No paper edit was needed (no notebook, text, figure or number touched).
- **Mechanism.** A docs page writes `[text](paper:key)`. `scripts/paper_keys.py` reads the keys from the two notebooks (a `:label:` line or a `(key)=` target in a markdown cell: no second list), and is a `mkdocs.yml` hook (`on_page_markdown`): it replaces the citation outside code fences with a relative link to the paper page and anchor (`../../paper/#thm-kkt`; the appendices are `paper/supporting-material/`) and raises a `PluginError` for a key the paper does not define.
- **Citations added** (links over existing words, plus a few words: the word budgets hold): theory (six: homogeneity, convexity, the soft maximum, the chart, elasticities, the n-lemma and its Figure 1; the sentence that said the account "will be in the paper when it is published" now says it is), limitations (Appendix B), termination (the certificate), fitting (the several-term extension), examples (the case's construction) and the home page (the paper).
- **Contract amendment 19** (the pattern of section 14): the three `docs.reference_key_*` facts in the manifest, the quoted block and section 10, the change-log row, and a line in `tests/test_interface_contract.py` that pins them. The amendment is additive (the floor grows). The presentation side owns `scripts/`, so no ownership entry changed.
- **Tests** (`tests/test_site.py`): `test_docsite_cites_the_paper_only_through_keys` (replaces the old "docs do not cite the paper" test; the same bar on a bare link, plus every cited key defined and at least one citation); `test_paper_keys_resolve_to_relative_links_and_unknown_keys_fail`; `test_every_paper_key_is_a_label_of_the_built_paper` (reads `paper/_build/html/myst.xref.json`, skipped when no paper was built); the assembled-site link test no longer requires the paper's second page when only the placeholder paper is staged (the key test above covers it against a built paper).
- **R-6 negative check.** In a scratch edit, `paper:thm-lme` renamed to `paper:thm-lme-RENAMED` in `docs/theory.md`: `uv run --group docs mkdocs build --strict` exits 1 with `theory.md: the paper defines no key 'thm-lme-RENAMED'` (`negative-key-build.log`); the edit was reverted.
- **R-13 browser pass** (own tab, the staged site at c6d7353 plus the unit, real paper): the Theory page's link "doubling every metric doubles V" opens `/paper/#thm-invariant` and lands on Theorem 1 (`d6-docs-theory-with-key-links.jpg`, `d6-link-lands-on-theorem-1.jpg`); the Limitations page's "Appendix B" opens `/paper/supporting-material/#appendix-b` on Appendix B (`d6-link-lands-on-appendix-b.jpg`). In the built docs no `href="paper:` remains.
- **Checks.** `uv run ruff check .`, `ruff format --check .` clean; `check_vocabulary.py` 0 new violations; `uv run pytest -q -n auto tests/test_site.py tests/test_interface_contract.py` (slow included): 140 passed; `uv lock --check` passes.

The punch list's reference-keys box is ticked and the CHANGELOG names the keys and the pin (WP8b).

**OD-A1 outcome (2026-11-11, 01:40):** the commit-archive pin in `paper/myst.yml` is accepted as (a): a versioned
template reference, proven by the driver's clean-worktree staging (driver-log.md). One defect found beside it:
`scripts/stage_site.py` falls back silently to the placeholder paper when the paper build fails; a release build must
not. Unit: the script exits non-zero and says so when the paper build fails, the placeholder only behind an explicit
flag; a test covers it. WP31's executor checked the light and phone renders in its tab without saving them: accepted
for the executor; the page's reviewer saves the screenshots in the record, as the standing order says.

**Amendment 1 review (3b1914f), the driver's dispositions (2026-11-11, 02:05):** G-1 (the version box and the changelog
heading) is the driver's at the candidate, with D-5; G-2 (the silent fallback) is the running unit; G-3 fix: WP31 enters
the changelog when it is accepted; G-4 (Figure 1's panel text at phone width) accept as is: the supervisor does not
require the paper's figures to read on a phone ("i don't need the paper to be fully readable on a phone"); G-5 fix: the
scope's "22 boxes" corrected visibly to the list's count; G-6 accept as is: the status line says DRAFT by the scope
convention, the approval being the recorded act, not an edit to the line.

### Claims register after the D-6 citations (2026-11-11)

`tests/test_claims_register.py::test_the_register_holds` failed on `dev` for C192, C195 (`docs/theory.md`) and C375 (`docs/user-guide/termination.md`): cfbad4f's `paper:key` citations rewrote the three sentences the rows quote. The fragments now read the new text (C192 "[doubling every metric doubles V](paper:thm-invariant)", C195 "...(GP), [solved as", C375 "[`certified`](paper:thm-certificate) is the first: ..."). Each claim, kind, backing and disposition are unchanged: a link adds no claim. `uv run pytest -q tests/test_claims_register.py tests/test_site.py -k "not slow"`: 52 passed, 1 skipped.

### The strict paper build in `stage_site.py` (the driver's unit of 2026-11-11, cd2aad2)

- **Change.** `scripts/assemble_site.py` gains the mode `paper="strict"`: it builds the real paper and raises `RuntimeError("the paper did not build (its error is printed above); use --paper placeholder to stage the site without it")` when the build fails or writes no `index.html`. `scripts/stage_site.py`'s `--paper` takes `strict` (the default) or `placeholder`; a failed paper build now prints `stage_site: FAILED: RuntimeError: ...` and exits 1, and `_stage/paper/` is not left holding a placeholder. `assemble_site.py`'s own command line (the Pages workflow's `uv run python scripts/assemble_site.py`) keeps `auto` with its fallback: the driver's unit named `stage_site.py`; the deployment's behaviour is the driver's to decide (reported).
- **Callers checked** (`git grep stage_site assemble_site`): tests that stage with the placeholder (`tests/test_site.py`'s `assembled` fixture) already pass `--paper placeholder` to `assemble_site.py`; `tests/test_build_generated.py` calls `stage_site.stage(..., paper="auto")` on a faked assemble (unchanged meaning); the work-package briefs that stage with `--paper placeholder` already carry the flag; none relied on the silent default of `stage_site.py`.
- **Tests** (`tests/test_build_generated.py`): `test_strict_paper_build_raises_instead_of_falling_back` (a failing runner, and a runner that reports success but writes nothing, both raise; a good build returns "paper"); `test_stage_site_exits_non_zero_when_the_paper_does_not_build` (default arguments, exit 1, the message names the failure and the flag, no placeholder staged); `test_stage_site_placeholder_flag_still_stages` (exit 0, placeholder staged).
- **Environment note.** The shared matplotlib font cache `~/.matplotlib/fontlist-v3.11.0.json` still named the removed worktree's venv, so every figure build in a new worktree failed with "Font family 'DejaVu Sans' not found" (also with these changes stashed). Not a repository defect; the checks below ran with `MPLCONFIGDIR` set to a scratch directory.

### assemble_site.py's command line made strict (ninth PM unit)

- **Change.** `scripts/assemble_site.py`'s `--paper` now takes `strict` (the default) or `placeholder`, as `stage_site.py` does since 4958ea6: a paper that does not build, or writes no `index.html`, prints `assemble_site: FAILED: RuntimeError: ...` naming the failure and `--paper placeholder`, and exits 1; the placeholder only behind that flag. The module docstring says so. The function `assemble(paper="auto")` keeps its default and fall-back for its callers; only the command line changed.
- **Callers checked.** The Pages workflow runs `uv run python scripts/assemble_site.py` on a release tag to publish: it must build the real paper, so it takes the strict default and is not edited (the earlier unit's note left this to the driver; a deployed placeholder in place of the paper is the failure strict exists to stop). `tests/test_site.py`'s `assembled` fixture already passes `--paper placeholder`; the tests that call `assemble`/`build_paper` pass `paper=` explicitly.
- **Tests** (`tests/test_build_generated.py`): `test_assemble_site_command_line_is_strict_by_default` (default arguments, failing paper, exit 1, message names the failure and the flag, no placeholder written) and `test_assemble_site_placeholder_flag_still_assembles` (exit 0, placeholder in place).
- **Scope count.** `WP8b-scope-of-work.md` D-3 and R-12 now say 20 boxes (corrected from 22, the count of the list; WP8b review G-5). The sentence in the context section ("All 22 boxes are unticked") describes the list as the scope found it and is left as written.

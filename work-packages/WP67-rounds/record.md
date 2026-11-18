# WP67 quality control: the record

`dev` head under test: f05ad97c (WP66b ea82a15e, WP66c bf823f22, WP66a 708ef565, the push trigger f05ad97c).
Baseline before any run (R-2): `gh release list` empty; `git ls-remote --tags origin` empty; no open issue. After
every run (21:20): the same; the four `qc/**` branches deleted (`git ls-remote --heads origin 'qc/*'` empty).

## The runs

| Goal | Branch | Head | Run | Expected | Result |
|---|---|---|---|---|---|
| G1 release dry run | `qc/release` | f05ad97c | 43988088453 | admissibility, test, build, site green; tag, publish-*, deploy-site, publish-release, on-failure skipped; summary names the slot `abstract` | met except the shards: `admissibility`, `build and check`, `test / test (fast)`, `site / compose` success; `tag and draft release`, `publish to TestPyPI`, `publish to PyPI`, `deploy the site`, `publish the release`, `on failure` skipped; the compose log reads `assemble_site: slot abstract - -`; `test` ran the fast shard alone (D-4 item 1) |
| G2 release dry run that fails | `qc/release-fail` | 656ac9fe | 43988193282 | admissibility fails naming the changelog; nothing after it; no issue | met: `admissibility` failed at the step "The changelog has an entry for this version" (`refused: CHANGELOG.md has no entry \`## [0.0.1]\` with content` (the version is 0.0.1 until WP68)); the nine later jobs skipped; no issue opened |
| G4 paper branch build | `qc/paper/build` | f05ad97c | 43988092221 | the paper tests, the HTML build, the keys check; the artefact holds two files; the residual-baseline test known to fail | not met on the runner: `build` failed at "The paper's tests" (3 failed, 263 passed, 50 min); the build, keys and pack steps skipped; `release` and `on-failure` skipped (no release, no issue, as the QC path expects). The three: `test_paper_residual_counts_do_not_rise` (known, 52 counts above the c0fe11b baseline); `test_notebooks_execute_from_a_clean_kernel_and_match_the_committed_outputs` (the datasets table `tab-F-datasets`: one dataset's sha256 differs between the committed output and a fresh execution on the runner); `test_myst_builds_the_html_site` (0 of 3 full-size figure links in the built `index.json` on the runner; the same test passes locally on this head in 9 s). All three are the paper branch's items (his decision: the paper's tests run only there); none touches the software gate. The artefact for G8 was built locally from this head: `build_keys.py --check` ok (121 keys), `paper-html.tar.gz` sha256 a2d51496…5fb1, `paper-keys.json` 8777f468…f262d |
| G5 paper failure path | `qc/paper/broken` | 65160e65 | 43988197406 | build fails, the summary names the step; no release, no issue | met in its observables: `build` failed at the step "The paper's tests" (3 failed, 263 passed, 1 h 44 min on a slower runner); `release` and `on-failure` skipped; no release, no tag, no issue. The planted test was not collected: `tests/test_paper_model.py` is a software module (its tests run in the fast suite; the `paper` marker in it belongs to a planted tree inside a string), so `-m paper` never saw it, and the failure the run shows is G4's three. Not re-run with a test in a paper-marked module: the observable is the same step and the same skips, at 1 h 45 min of runner time |
| G9 push to dev | `dev` | f05ad97c | 43988085221 | lint and the fast shard only, Linux | met: `test (fast)` success, `windows` skipped |
| G1 release dry run, after D-4 | `qc/release` | 57a0dc25 | 43988524238 | as G1, with `test` running all three shards | met: `admissibility`, `build and check`, `test / test (fast)`, `test / test (slow)`, `test / test (docs)`, `site / compose` success; `windows`, `tag and draft release`, `publish to TestPyPI`, `publish to PyPI`, `deploy the site`, `publish the release`, `on failure` skipped |
| G9 push to dev, after D-4 | `dev` | 57a0dc25 | 43988521076 | lint and the fast shard only, Linux | met: `test (fast)` success, `windows` skipped |

## G3 the site artefact of G1, staged locally

Artefacts of 43988088453: `github-pages` (4.1 MB), `dist`, `sbom`. `artifact.tar` unpacked under the scratchpad:
`/paper/index.html` is the abstract page (title "Scaling Decision Analysis with Hyperbolic Trade Space
Identification", the author line, the sentence that the paper is iterated towards release, no script element); the
root card reads "its abstract; the paper is iterated towards release"; the docs' citations point at `/paper/`.

## D-4 fixes the runs exposed

1. The first release dry run (43988088453) ran `test / test (fast)` alone: a called workflow sees the caller's event
   (`push`), so the push-to-dev condition of G9 also caught the call from `release.yml`. Fixed on `dev` by tying the
   push case to the workflow's own name (`github.workflow == 'Tests'`); `qc/release` re-pushed; see the second G1
   row.
2. The machinery diff found three records describing `test.yml` without the push trigger (software checklist C10,
   `docs/code-owners.md`, `work-packages/README.md`) and the specification's 5.3 bullet reading "No push trigger"
   before stating it; all four amended on `dev`.
3. The pinned slot's banner was dropped by the theme's hydration: `scripts/assemble_site.py` wrote the banner as
   a static `<p>` directly after `<body>` (specification 3.2); the article theme hydrates the document with React,
   the extra node fails the hydration (React error 418) and the client render removes it, so no pinned page showed
   its banner once its scripts ran. Fix: the composer writes the banner in a `<template>` with a script directly
   before `</body>` that installs it as `<body>`'s first element after the load event and keeps it there through
   the theme's first seconds; `banner_html` and `banner_line` unchanged; `tests/test_paper_slot.py` asserts the
   installer and its template; specification 3.2 amended to say how and why. A second look at the installed banner
   measured its text black (`rgb(0,0,0)`) on the dark scheme's background `rgb(28,25,23)`, since the theme colours
   its containers and not `<body>`, and the theme's fixed scheme button over the banner's end at 375 px; the
   installer now carries a stylesheet naming the banner's colours for `html.dark` and the light scheme (measured
   `rgb(231,229,228)` on `rgb(41,37,36)` and `rgb(28,25,23)` on `rgb(245,245,244)`) and side padding of 3.5 rem.
   Two commits on `dev`: cb0ad18f (the installer) and b8197b52 (the colours and the padding).

## G6 the clean-up script by hand

```
release_cleanup: v0.0.0 in DynamicalSystemsGroup/tradespace
found: no tag v0.0.0; no release
nothing to remove            (exit 0)
release_cleanup: paper-working-20000101 in DynamicalSystemsGroup/tradespace
found: no tag paper-working-20000101; no release
nothing to remove            (exit 0)
```

## G7 the machinery diff

`machinery-diff.md`: 104 rows. Of `machinery.toml`'s 48 components 25 unchanged, 18 changed, 5 removed (`pages.yml`,
`site/paper/index.html`, `WP8b-release-checklist.md`, two `test_site.py` tests); 44 rows added for what exists now
and had no row then. Departures from the specification, each by his later answers or recorded in the units' notes:
`release.yml` excludes `qc/paper/**` from its push trigger (the build plan's split of the QC branches); the fourth
tag state `site-only` with `deploy-site` needing `check` and `test` and `publish-release` running on a site-only
merge (his second design answer); `release_cleanup.py` retries with a whole-run rerun rather than `--failed` and
reports three extra JSON fields (WP66a's notes). `release-punch-list.md` still describes the placeholder and
`pages.yml`; the build plan assigns it to WP68.

## G8 the browser pass

The eighty captures this section cites left the tree with WP73; each is read at `4f81a4ea` (`git show 4f81a4ea:work-packages/WP67-rounds/captures/<file>`).

Five cases, each staged in a worktree at 57a0dc25 and served on its own port, captured headless (Playwright,
Chromium) at 1,280 and 375 px in light and dark: `/`, `/paper/`, `/paper/supporting-material/` and `/docs/theory/`
(the docs page with eight paper citations). The abstract case is the tree as it is; the other four stage with
`--artefact` at a paper build made locally from f05ad97c (G4's hosted artefact was not produced) under a temporary,
uncommitted `paper/mode.toml` per case (`doi = "10.5281/zenodo.123"`; the archive's real SHA-256; the fallback case
with its first hex digit altered), restored after each case. The capture script records, per page, the HTTP status,
the banner (text, link, whether it is the first element after `<body>`), the citation targets, the fallback line,
sideways overflow and the console. Eighty captures in `captures/`, one per (case, page, width, scheme).

**First attempt, set aside.** The local archive was packed with macOS `tar`, which adds an AppleDouble member
(`._name`) beside every file: 2,598 members, 1,299 of them resource forks. The composer reads every page of the
archive as UTF-8 and refused the first fork it met, so the three pinned cases fell back with the line "The pin
`paper-working-20261116` was not reachable when the site was composed (`paper-html.tar.gz: ._index.html is not
UTF-8 text`); its abstract follows." (and the same for the submitted and revision pins), a `::warning::` annotation
each, exit 0, and `--strict-slot` exit 1: the fallback path as designed, for a reason the hosted path cannot
produce (`paper.yml` packs with GNU tar on Ubuntu, which writes no forks). The archive was repacked without the
forks (1,299 members, SHA-256 `6a073f87…fd48c`) and the four cases re-run; the first attempt's captures and rows are
kept outside the tree (`wp67-browser-logs/attempt1-*` in the driver's scratchpad). One question for him, not a fix
here: whether the composer should skip `._*` members and `__MACOSX/` so a paper archive packed by hand on a Mac
serves instead of falling back. Options: (a) skip them, one line in `unpack`; (b) keep the refusal, since the paper
archive is the workflow's to pack and a foreign member is a reason to fall back; (c) refuse them with a reason that
names the cause ("macOS resource forks; pack with `COPYFILE_DISABLE=1`").

**The unit.** The browser-pass unit wrote the capture tooling and the abstract case's sixteen captures, then its loop
hung: the staged site's server did not stop on the interrupt the loop sent, and the unit ended without a hand-back
while waiting. The driver stopped the server and the unit, changed the loop's stop to a kill by port, and ran the
remaining cases.

**Second attempt, set aside.** With the forks removed the three pinned cases staged with `slot pin <tag>`, the
banner the first element after `<body>` on `/paper/` and `/paper/supporting-material/` with the mode's wording and
the DOI linked, and the docs page's eight citations carrying their anchors (`../../paper/#thm-chart` and the rest).
But the paper's pages rendered unstyled: 38 requests on `/paper/` and 25 on the supporting material returned 404
(`build/root-*.js`, `build/_assets/app-*.css`, `myst-theme.css`, the figures), and the 375 px pages overflowed
sideways by 414 and 156 px. The cause is the local build again: `paper.yml` builds with
`BASE_URL=/tradespace/paper` (its line 26; specification 5.3), and the local `myst build` ran without
`BASE_URL`, so the page asked for its assets at the server's root. The paper was rebuilt with `BASE_URL=/paper`
(the path the staging server serves it at), repacked without forks, and the four cases run a third time. Two things
this leaves: a local review of a hosted `paper-release` artefact serves it under `/paper/` while its assets point at
`/tradespace/paper/`, so `stage_site.py --serve` would need to serve under the Pages prefix for that
review to render (an item for the staging script, not the release path); and whether the overflow at 375 px belongs
to the paper's own theme is read from the third attempt.

**Third attempt, set aside: the defect.** With the base path set the pages rendered styled, no request failed,
and nothing overflowed at 375 px (the earlier overflow was the unstyled page's). But the banner was gone from every
pinned page and the console logged React error 418 (a hydration mismatch). The article theme hydrates the whole
document with React; a static element inserted after `<body>` is a node the client render does not expect, the
hydration fails, the theme renders the page afresh on the client and the banner is dropped. The second attempt had
shown the banner only because the page's scripts had not loaded. Confirmed on the raw artefact served alone: no
error and no banner; with the static banner, error 418 and no banner; with the banner installed by a script after the
load event (and put back if removed within its first seconds), no error and the banner `<body>`'s first visible
element on both paper pages. That is D-4 item 3 above; the four cases were run a fourth time on the fixed composer, and a fifth after its colours.

**Fourth and fifth attempts, on the fixed composer (cb0ad18f, then b8197b52 with the banner's colours; the table
is the fifth).** Every row below. In the three pinned cases the banner is `<body>`'s first visible element on
`/paper/` and `/paper/supporting-material/` at both widths and in both schemes, its text the mode's ("Working
paper · paper-working-20261116 · 2026-11-16 · DOI 10.5281/zenodo.123"; "Submitted to ieee-tse · …"; "Revision 1
for ieee-tse · …"), linked to `https://doi.org/10.5281/zenodo.123`, legible in both schemes and clear of the
theme's scheme button; no console error, no failed request, no sideways scroll; the docs page's eight citations
carry their anchors (`../../paper/#thm-chart` and the rest). In the abstract and fallback cases `/paper/` is the
abstract page (the fallback form with its line naming the pin and the checksum mismatch),
`/paper/supporting-material/` is absent (404: the route belongs to the pinned paper and nothing in those sites
links to it) and the eight citations land on `../../paper/`. The one console line on every docs page is the
theme's lookup of the latest GitHub release (404 until a release exists), known from WP66c. The fallback case's
`--strict-slot` run exits 1 with "the paper slot fell back". G8 met; R-3 met (the capture names enumerate case,
page, width and scheme). The measurements in the table are of the full pages; a capture taller than 2,000 px (the
pinned paper pages, 40,000 to 133,000 px, and the docs page) is kept in `captures/` as its top 1,200 px, since the
full set weighed 364 MB and the rest of the page is the paper's own render.

| Case | Page | Width | Scheme | Status | Banner | Citation target | Sideways scroll | Console errors | Capture |
|---|---|---|---|---|---|---|---|---|---|
| abstract | `/` | 1280 | light | 200 | none | - | none | none | `captures/abstract-root-1280-light.png` |
| abstract | `/` | 1280 | dark | 200 | none | - | none | none | `captures/abstract-root-1280-dark.png` |
| abstract | `/` | 375 | light | 200 | none | - | none | none | `captures/abstract-root-375-light.png` |
| abstract | `/` | 375 | dark | 200 | none | - | none | none | `captures/abstract-root-375-dark.png` |
| abstract | `/paper/` | 1280 | light | 200 | none | - | none | none | `captures/abstract-paper-1280-light.png` |
| abstract | `/paper/` | 1280 | dark | 200 | none | - | none | none | `captures/abstract-paper-1280-dark.png` |
| abstract | `/paper/` | 375 | light | 200 | none | - | none | none | `captures/abstract-paper-375-light.png` |
| abstract | `/paper/` | 375 | dark | 200 | none | - | none | none | `captures/abstract-paper-375-dark.png` |
| abstract | `/paper/supporting-material/` | 1280 | light | 404 | none (page absent) | - | none | Failed to load resource: the server responded with a status of 404 (File not found); request 404 :8892/paper/supporting-material/ | `captures/abstract-paper-supporting-material-1280-light.png` |
| abstract | `/paper/supporting-material/` | 1280 | dark | 404 | none (page absent) | - | none | Failed to load resource: the server responded with a status of 404 (File not found); request 404 :8892/paper/supporting-material/ | `captures/abstract-paper-supporting-material-1280-dark.png` |
| abstract | `/paper/supporting-material/` | 375 | light | 404 | none (page absent) | - | none | Failed to load resource: the server responded with a status of 404 (File not found); request 404 :8892/paper/supporting-material/ | `captures/abstract-paper-supporting-material-375-light.png` |
| abstract | `/paper/supporting-material/` | 375 | dark | 404 | none (page absent) | - | none | Failed to load resource: the server responded with a status of 404 (File not found); request 404 :8892/paper/supporting-material/ | `captures/abstract-paper-supporting-material-375-dark.png` |
| abstract | `/docs/theory/` | 1280 | light | 200 | none | 8 citation links, all `../../paper/` | none | the known 404 (theme's release lookup) | `captures/abstract-docs-theory-1280-light.png` |
| abstract | `/docs/theory/` | 1280 | dark | 200 | none | 8 citation links, all `../../paper/` | none | the known 404 (theme's release lookup) | `captures/abstract-docs-theory-1280-dark.png` |
| abstract | `/docs/theory/` | 375 | light | 200 | none | 8 citation links, all `../../paper/` | none | the known 404 (theme's release lookup) | `captures/abstract-docs-theory-375-light.png` |
| abstract | `/docs/theory/` | 375 | dark | 200 | none | 8 citation links, all `../../paper/` | none | the known 404 (theme's release lookup) | `captures/abstract-docs-theory-375-dark.png` |
| working | `/` | 1280 | light | 200 | none | - | none | none | `captures/working-root-1280-light.png` |
| working | `/` | 1280 | dark | 200 | none | - | none | none | `captures/working-root-1280-dark.png` |
| working | `/` | 375 | light | 200 | none | - | none | none | `captures/working-root-375-light.png` |
| working | `/` | 375 | dark | 200 | none | - | none | none | `captures/working-root-375-dark.png` |
| working | `/paper/` | 1280 | light | 200 | Working paper · paper-working-20261116 · 2026-11-16 · DOI 10.5281/zenodo.123 (linked `https://doi.org/10.5281/zenodo.123`; first element after `<body>`; 1 on the page) | - | none | none | `captures/working-paper-1280-light.png` |
| working | `/paper/` | 1280 | dark | 200 | Working paper · paper-working-20261116 · 2026-11-16 · DOI 10.5281/zenodo.123 (linked `https://doi.org/10.5281/zenodo.123`; first element after `<body>`; 1 on the page) | - | none | none | `captures/working-paper-1280-dark.png` |
| working | `/paper/` | 375 | light | 200 | Working paper · paper-working-20261116 · 2026-11-16 · DOI 10.5281/zenodo.123 (linked `https://doi.org/10.5281/zenodo.123`; first element after `<body>`; 1 on the page) | - | none | none | `captures/working-paper-375-light.png` |
| working | `/paper/` | 375 | dark | 200 | Working paper · paper-working-20261116 · 2026-11-16 · DOI 10.5281/zenodo.123 (linked `https://doi.org/10.5281/zenodo.123`; first element after `<body>`; 1 on the page) | - | none | none | `captures/working-paper-375-dark.png` |
| working | `/paper/supporting-material/` | 1280 | light | 200 | Working paper · paper-working-20261116 · 2026-11-16 · DOI 10.5281/zenodo.123 (linked `https://doi.org/10.5281/zenodo.123`; first element after `<body>`; 1 on the page) | - | none | none | `captures/working-paper-supporting-material-1280-light.png` |
| working | `/paper/supporting-material/` | 1280 | dark | 200 | Working paper · paper-working-20261116 · 2026-11-16 · DOI 10.5281/zenodo.123 (linked `https://doi.org/10.5281/zenodo.123`; first element after `<body>`; 1 on the page) | - | none | none | `captures/working-paper-supporting-material-1280-dark.png` |
| working | `/paper/supporting-material/` | 375 | light | 200 | Working paper · paper-working-20261116 · 2026-11-16 · DOI 10.5281/zenodo.123 (linked `https://doi.org/10.5281/zenodo.123`; first element after `<body>`; 1 on the page) | - | none | none | `captures/working-paper-supporting-material-375-light.png` |
| working | `/paper/supporting-material/` | 375 | dark | 200 | Working paper · paper-working-20261116 · 2026-11-16 · DOI 10.5281/zenodo.123 (linked `https://doi.org/10.5281/zenodo.123`; first element after `<body>`; 1 on the page) | - | none | none | `captures/working-paper-supporting-material-375-dark.png` |
| working | `/docs/theory/` | 1280 | light | 200 | none | 8 links: ['../../paper/#def-nlemma', '../../paper/#fig-nlemma', '../../paper/#sect-results', '../../paper/#thm-chart', '../../paper/#thm-convex', '../../paper/#thm-elasticity', '../../paper/#thm-invariant', '../../paper/#thm-lme'] | none | the known 404 (theme's release lookup) | `captures/working-docs-theory-1280-light.png` |
| working | `/docs/theory/` | 1280 | dark | 200 | none | 8 links: ['../../paper/#def-nlemma', '../../paper/#fig-nlemma', '../../paper/#sect-results', '../../paper/#thm-chart', '../../paper/#thm-convex', '../../paper/#thm-elasticity', '../../paper/#thm-invariant', '../../paper/#thm-lme'] | none | the known 404 (theme's release lookup) | `captures/working-docs-theory-1280-dark.png` |
| working | `/docs/theory/` | 375 | light | 200 | none | 8 links: ['../../paper/#def-nlemma', '../../paper/#fig-nlemma', '../../paper/#sect-results', '../../paper/#thm-chart', '../../paper/#thm-convex', '../../paper/#thm-elasticity', '../../paper/#thm-invariant', '../../paper/#thm-lme'] | none | the known 404 (theme's release lookup) | `captures/working-docs-theory-375-light.png` |
| working | `/docs/theory/` | 375 | dark | 200 | none | 8 links: ['../../paper/#def-nlemma', '../../paper/#fig-nlemma', '../../paper/#sect-results', '../../paper/#thm-chart', '../../paper/#thm-convex', '../../paper/#thm-elasticity', '../../paper/#thm-invariant', '../../paper/#thm-lme'] | none | the known 404 (theme's release lookup) | `captures/working-docs-theory-375-dark.png` |
| submitted | `/` | 1280 | light | 200 | none | - | none | none | `captures/submitted-root-1280-light.png` |
| submitted | `/` | 1280 | dark | 200 | none | - | none | none | `captures/submitted-root-1280-dark.png` |
| submitted | `/` | 375 | light | 200 | none | - | none | none | `captures/submitted-root-375-light.png` |
| submitted | `/` | 375 | dark | 200 | none | - | none | none | `captures/submitted-root-375-dark.png` |
| submitted | `/paper/` | 1280 | light | 200 | Submitted to ieee-tse · paper-submitted-ieee-tse · 2026-11-16 · DOI 10.5281/zenodo.123 (linked `https://doi.org/10.5281/zenodo.123`; first element after `<body>`; 1 on the page) | - | none | none | `captures/submitted-paper-1280-light.png` |
| submitted | `/paper/` | 1280 | dark | 200 | Submitted to ieee-tse · paper-submitted-ieee-tse · 2026-11-16 · DOI 10.5281/zenodo.123 (linked `https://doi.org/10.5281/zenodo.123`; first element after `<body>`; 1 on the page) | - | none | none | `captures/submitted-paper-1280-dark.png` |
| submitted | `/paper/` | 375 | light | 200 | Submitted to ieee-tse · paper-submitted-ieee-tse · 2026-11-16 · DOI 10.5281/zenodo.123 (linked `https://doi.org/10.5281/zenodo.123`; first element after `<body>`; 1 on the page) | - | none | none | `captures/submitted-paper-375-light.png` |
| submitted | `/paper/` | 375 | dark | 200 | Submitted to ieee-tse · paper-submitted-ieee-tse · 2026-11-16 · DOI 10.5281/zenodo.123 (linked `https://doi.org/10.5281/zenodo.123`; first element after `<body>`; 1 on the page) | - | none | none | `captures/submitted-paper-375-dark.png` |
| submitted | `/paper/supporting-material/` | 1280 | light | 200 | Submitted to ieee-tse · paper-submitted-ieee-tse · 2026-11-16 · DOI 10.5281/zenodo.123 (linked `https://doi.org/10.5281/zenodo.123`; first element after `<body>`; 1 on the page) | - | none | none | `captures/submitted-paper-supporting-material-1280-light.png` |
| submitted | `/paper/supporting-material/` | 1280 | dark | 200 | Submitted to ieee-tse · paper-submitted-ieee-tse · 2026-11-16 · DOI 10.5281/zenodo.123 (linked `https://doi.org/10.5281/zenodo.123`; first element after `<body>`; 1 on the page) | - | none | none | `captures/submitted-paper-supporting-material-1280-dark.png` |
| submitted | `/paper/supporting-material/` | 375 | light | 200 | Submitted to ieee-tse · paper-submitted-ieee-tse · 2026-11-16 · DOI 10.5281/zenodo.123 (linked `https://doi.org/10.5281/zenodo.123`; first element after `<body>`; 1 on the page) | - | none | none | `captures/submitted-paper-supporting-material-375-light.png` |
| submitted | `/paper/supporting-material/` | 375 | dark | 200 | Submitted to ieee-tse · paper-submitted-ieee-tse · 2026-11-16 · DOI 10.5281/zenodo.123 (linked `https://doi.org/10.5281/zenodo.123`; first element after `<body>`; 1 on the page) | - | none | none | `captures/submitted-paper-supporting-material-375-dark.png` |
| submitted | `/docs/theory/` | 1280 | light | 200 | none | 8 links: ['../../paper/#def-nlemma', '../../paper/#fig-nlemma', '../../paper/#sect-results', '../../paper/#thm-chart', '../../paper/#thm-convex', '../../paper/#thm-elasticity', '../../paper/#thm-invariant', '../../paper/#thm-lme'] | none | the known 404 (theme's release lookup) | `captures/submitted-docs-theory-1280-light.png` |
| submitted | `/docs/theory/` | 1280 | dark | 200 | none | 8 links: ['../../paper/#def-nlemma', '../../paper/#fig-nlemma', '../../paper/#sect-results', '../../paper/#thm-chart', '../../paper/#thm-convex', '../../paper/#thm-elasticity', '../../paper/#thm-invariant', '../../paper/#thm-lme'] | none | the known 404 (theme's release lookup) | `captures/submitted-docs-theory-1280-dark.png` |
| submitted | `/docs/theory/` | 375 | light | 200 | none | 8 links: ['../../paper/#def-nlemma', '../../paper/#fig-nlemma', '../../paper/#sect-results', '../../paper/#thm-chart', '../../paper/#thm-convex', '../../paper/#thm-elasticity', '../../paper/#thm-invariant', '../../paper/#thm-lme'] | none | the known 404 (theme's release lookup) | `captures/submitted-docs-theory-375-light.png` |
| submitted | `/docs/theory/` | 375 | dark | 200 | none | 8 links: ['../../paper/#def-nlemma', '../../paper/#fig-nlemma', '../../paper/#sect-results', '../../paper/#thm-chart', '../../paper/#thm-convex', '../../paper/#thm-elasticity', '../../paper/#thm-invariant', '../../paper/#thm-lme'] | none | the known 404 (theme's release lookup) | `captures/submitted-docs-theory-375-dark.png` |
| revision | `/` | 1280 | light | 200 | none | - | none | none | `captures/revision-root-1280-light.png` |
| revision | `/` | 1280 | dark | 200 | none | - | none | none | `captures/revision-root-1280-dark.png` |
| revision | `/` | 375 | light | 200 | none | - | none | none | `captures/revision-root-375-light.png` |
| revision | `/` | 375 | dark | 200 | none | - | none | none | `captures/revision-root-375-dark.png` |
| revision | `/paper/` | 1280 | light | 200 | Revision 1 for ieee-tse · paper-revision-ieee-tse-r1 · 2026-11-16 · DOI 10.5281/zenodo.123 (linked `https://doi.org/10.5281/zenodo.123`; first element after `<body>`; 1 on the page) | - | none | none | `captures/revision-paper-1280-light.png` |
| revision | `/paper/` | 1280 | dark | 200 | Revision 1 for ieee-tse · paper-revision-ieee-tse-r1 · 2026-11-16 · DOI 10.5281/zenodo.123 (linked `https://doi.org/10.5281/zenodo.123`; first element after `<body>`; 1 on the page) | - | none | none | `captures/revision-paper-1280-dark.png` |
| revision | `/paper/` | 375 | light | 200 | Revision 1 for ieee-tse · paper-revision-ieee-tse-r1 · 2026-11-16 · DOI 10.5281/zenodo.123 (linked `https://doi.org/10.5281/zenodo.123`; first element after `<body>`; 1 on the page) | - | none | none | `captures/revision-paper-375-light.png` |
| revision | `/paper/` | 375 | dark | 200 | Revision 1 for ieee-tse · paper-revision-ieee-tse-r1 · 2026-11-16 · DOI 10.5281/zenodo.123 (linked `https://doi.org/10.5281/zenodo.123`; first element after `<body>`; 1 on the page) | - | none | none | `captures/revision-paper-375-dark.png` |
| revision | `/paper/supporting-material/` | 1280 | light | 200 | Revision 1 for ieee-tse · paper-revision-ieee-tse-r1 · 2026-11-16 · DOI 10.5281/zenodo.123 (linked `https://doi.org/10.5281/zenodo.123`; first element after `<body>`; 1 on the page) | - | none | none | `captures/revision-paper-supporting-material-1280-light.png` |
| revision | `/paper/supporting-material/` | 1280 | dark | 200 | Revision 1 for ieee-tse · paper-revision-ieee-tse-r1 · 2026-11-16 · DOI 10.5281/zenodo.123 (linked `https://doi.org/10.5281/zenodo.123`; first element after `<body>`; 1 on the page) | - | none | none | `captures/revision-paper-supporting-material-1280-dark.png` |
| revision | `/paper/supporting-material/` | 375 | light | 200 | Revision 1 for ieee-tse · paper-revision-ieee-tse-r1 · 2026-11-16 · DOI 10.5281/zenodo.123 (linked `https://doi.org/10.5281/zenodo.123`; first element after `<body>`; 1 on the page) | - | none | none | `captures/revision-paper-supporting-material-375-light.png` |
| revision | `/paper/supporting-material/` | 375 | dark | 200 | Revision 1 for ieee-tse · paper-revision-ieee-tse-r1 · 2026-11-16 · DOI 10.5281/zenodo.123 (linked `https://doi.org/10.5281/zenodo.123`; first element after `<body>`; 1 on the page) | - | none | none | `captures/revision-paper-supporting-material-375-dark.png` |
| revision | `/docs/theory/` | 1280 | light | 200 | none | 8 links: ['../../paper/#def-nlemma', '../../paper/#fig-nlemma', '../../paper/#sect-results', '../../paper/#thm-chart', '../../paper/#thm-convex', '../../paper/#thm-elasticity', '../../paper/#thm-invariant', '../../paper/#thm-lme'] | none | the known 404 (theme's release lookup) | `captures/revision-docs-theory-1280-light.png` |
| revision | `/docs/theory/` | 1280 | dark | 200 | none | 8 links: ['../../paper/#def-nlemma', '../../paper/#fig-nlemma', '../../paper/#sect-results', '../../paper/#thm-chart', '../../paper/#thm-convex', '../../paper/#thm-elasticity', '../../paper/#thm-invariant', '../../paper/#thm-lme'] | none | the known 404 (theme's release lookup) | `captures/revision-docs-theory-1280-dark.png` |
| revision | `/docs/theory/` | 375 | light | 200 | none | 8 links: ['../../paper/#def-nlemma', '../../paper/#fig-nlemma', '../../paper/#sect-results', '../../paper/#thm-chart', '../../paper/#thm-convex', '../../paper/#thm-elasticity', '../../paper/#thm-invariant', '../../paper/#thm-lme'] | none | the known 404 (theme's release lookup) | `captures/revision-docs-theory-375-light.png` |
| revision | `/docs/theory/` | 375 | dark | 200 | none | 8 links: ['../../paper/#def-nlemma', '../../paper/#fig-nlemma', '../../paper/#sect-results', '../../paper/#thm-chart', '../../paper/#thm-convex', '../../paper/#thm-elasticity', '../../paper/#thm-invariant', '../../paper/#thm-lme'] | none | the known 404 (theme's release lookup) | `captures/revision-docs-theory-375-dark.png` |
| fallback | `/` | 1280 | light | 200 | none | - | none | none | `captures/fallback-root-1280-light.png` |
| fallback | `/` | 1280 | dark | 200 | none | - | none | none | `captures/fallback-root-1280-dark.png` |
| fallback | `/` | 375 | light | 200 | none | - | none | none | `captures/fallback-root-375-light.png` |
| fallback | `/` | 375 | dark | 200 | none | - | none | none | `captures/fallback-root-375-dark.png` |
| fallback | `/paper/` | 1280 | light | 200 | none | - | none | none | `captures/fallback-paper-1280-light.png` |
| fallback | `/paper/` | 1280 | dark | 200 | none | - | none | none | `captures/fallback-paper-1280-dark.png` |
| fallback | `/paper/` | 375 | light | 200 | none | - | none | none | `captures/fallback-paper-375-light.png` |
| fallback | `/paper/` | 375 | dark | 200 | none | - | none | none | `captures/fallback-paper-375-dark.png` |
| fallback | `/paper/supporting-material/` | 1280 | light | 404 | none (page absent) | - | none | Failed to load resource: the server responded with a status of 404 (File not found); request 404 :8896/paper/supporting-material/ | `captures/fallback-paper-supporting-material-1280-light.png` |
| fallback | `/paper/supporting-material/` | 1280 | dark | 404 | none (page absent) | - | none | Failed to load resource: the server responded with a status of 404 (File not found); request 404 :8896/paper/supporting-material/ | `captures/fallback-paper-supporting-material-1280-dark.png` |
| fallback | `/paper/supporting-material/` | 375 | light | 404 | none (page absent) | - | none | Failed to load resource: the server responded with a status of 404 (File not found); request 404 :8896/paper/supporting-material/ | `captures/fallback-paper-supporting-material-375-light.png` |
| fallback | `/paper/supporting-material/` | 375 | dark | 404 | none (page absent) | - | none | Failed to load resource: the server responded with a status of 404 (File not found); request 404 :8896/paper/supporting-material/ | `captures/fallback-paper-supporting-material-375-dark.png` |
| fallback | `/docs/theory/` | 1280 | light | 200 | none | 8 citation links, all `../../paper/` | none | the known 404 (theme's release lookup) | `captures/fallback-docs-theory-1280-light.png` |
| fallback | `/docs/theory/` | 1280 | dark | 200 | none | 8 citation links, all `../../paper/` | none | the known 404 (theme's release lookup) | `captures/fallback-docs-theory-1280-dark.png` |
| fallback | `/docs/theory/` | 375 | light | 200 | none | 8 citation links, all `../../paper/` | none | the known 404 (theme's release lookup) | `captures/fallback-docs-theory-375-light.png` |
| fallback | `/docs/theory/` | 375 | dark | 200 | none | 8 citation links, all `../../paper/` | none | the known 404 (theme's release lookup) | `captures/fallback-docs-theory-375-dark.png` |


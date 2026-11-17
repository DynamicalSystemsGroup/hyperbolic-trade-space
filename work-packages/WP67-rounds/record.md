# WP67 quality control: the record

`dev` head under test: f05ad97c (WP66b ea82a15e, WP66c bf823f22, WP66a 708ef565, the push trigger f05ad97c).
Baseline before any run (R-2): `gh release list` empty; `git ls-remote --tags origin` empty; no open issue.

## The runs

| Goal | Branch | Head | Run | Expected | Result |
|---|---|---|---|---|---|
| G1 release dry run | `qc/release` | f05ad97c | 43988088453 | admissibility, test, build, site green; tag, publish-*, deploy-site, publish-release, on-failure skipped; summary names the slot `abstract` | met except the shards: `admissibility`, `build and check`, `test / test (fast)`, `site / compose` success; `tag and draft release`, `publish to TestPyPI`, `publish to PyPI`, `deploy the site`, `publish the release`, `on failure` skipped; the compose log reads `assemble_site: slot abstract - -`; `test` ran the fast shard alone (D-4 item 1) |
| G2 release dry run that fails | `qc/release-fail` | 656ac9fe | 43988193282 | admissibility fails naming the changelog; nothing after it; no issue | met: `admissibility` failed at the step "The changelog has an entry for this version" (`refused: CHANGELOG.md has no entry \`## [0.0.1]\` with content` (the version is 0.0.1 until WP68)); the nine later jobs skipped; no issue opened |
| G4 paper branch build | `qc/paper/build` | f05ad97c | 43988092221 | the paper tests, the HTML build, the keys check; the artefact holds two files; the residual-baseline test known to fail | not met on the runner: `build` failed at "The paper's tests" (3 failed, 263 passed, 50 min); the build, keys and pack steps skipped; `release` and `on-failure` skipped (no release, no issue, as the QC path expects). The three: `test_paper_residual_counts_do_not_rise` (known, 52 counts above the c0fe11b baseline); `test_notebooks_execute_from_a_clean_kernel_and_match_the_committed_outputs` (the datasets table `tab-F-datasets`: one dataset's sha256 differs between the committed output and a fresh execution on the runner); `test_myst_builds_the_html_site` (0 of 3 full-size figure links in the built `index.json` on the runner; the same test passes locally on this head in 9 s). All three are the paper branch's items (his decision: the paper's tests run only there); none touches the software gate. The artefact for G8 was built locally from this head: `build_keys.py --check` ok (121 keys), `paper-html.tar.gz` sha256 a2d51496…5fb1, `paper-keys.json` 8777f468…f262d |
| G5 paper failure path | `qc/paper/broken` | 65160e65 | 43988197406 | build fails, the summary names the step; no release, no issue | pending |
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

## G6 the clean-up script by hand

```
release_cleanup: v0.0.0 in DynamicalSystemsGroup/hyperbolic-trade-space
found: no tag v0.0.0; no release
nothing to remove            (exit 0)
release_cleanup: paper-working-20000101 in DynamicalSystemsGroup/hyperbolic-trade-space
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

pending

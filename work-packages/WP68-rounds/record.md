# WP68 record: the first merge into `main`

## G5 the staged site at the head, looked at

Head 7e6839a0 (`dev` after WP73's landing), staged with `scripts/stage_site.py` (slot `abstract`) and served on
127.0.0.1:8797; captured headless (Chromium) at 1,280 and 375 px, light and dark, the capture tooling of WP67's
browser pass. A capture taller than 2,000 px is kept as its top 1,200 px. The root page read as a whole at 1,280 px
light: the title, the author, the three paragraphs, the ternary figure with its three regions and three markers,
its caption; no element out of place. The pinned modes and the fallback were looked at in WP67 (five attempts, the
banner fixed) and are not re-run here: nothing in the composer changed since b8197b52.

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
| abstract | `/paper/supporting-material/` | 1280 and 375, both schemes | | 404 | none (page absent: the route belongs to a pinned paper; nothing in the abstract-mode site links to it) | - | none | the 404 itself | `captures/abstract-paper-supporting-material-*.png` |
| abstract | `/docs/theory/` | 1280 | light | 200 | none | 8 citation links, all `../../paper/` | none | the theme's release lookup (404 until a release exists) | `captures/abstract-docs-theory-1280-light.png` |
| abstract | `/docs/theory/` | 1280 | dark | 200 | none | 8 citation links, all `../../paper/` | none | the same | `captures/abstract-docs-theory-1280-dark.png` |
| abstract | `/docs/theory/` | 375 | light | 200 | none | 8 citation links, all `../../paper/` | none | the same | `captures/abstract-docs-theory-375-light.png` |
| abstract | `/docs/theory/` | 375 | dark | 200 | none | 8 citation links, all `../../paper/` | none | the same | `captures/abstract-docs-theory-375-dark.png` |

G5 met at 7e6839a0. The version commit changes no page; the pass is not repeated for it.

## G7 his settings, read back

Done by him on 2026-11-17 (09:30 to 12:00 EST), one step at a time in chat with a screenshot per step, and read
back through the API (`gh api repos/DynamicalSystemsGroup/tradespace/{pages,environments,rulesets}` and each
environment's `deployment-branch-policies`). Zenodo stays off (his word). The read-back, verbatim from the calls:

```
## pages
build_type=workflow url=https://dynamicalsystemsgroup.github.io/tradespace/ https=true
## environments
github-pages: reviewers= prevent_self_review= can_admins_bypass=true
paper-release: reviewers=mzargham,jshorish prevent_self_review=true can_admins_bypass=false
pypi: reviewers= prevent_self_review= can_admins_bypass=true
testpypi: reviewers= prevent_self_review= can_admins_bypass=true
github-pages rules: branch:main
pypi rules: branch:main
testpypi rules: branch:dev
paper-release rules: tag:paper-*
## pending publishers (his screenshots 2026-11-17): PyPI tradespace/release.yml/pypi; TestPyPI tradespace/release.yml/testpypi
## rulesets
dev: active; target=refs/heads/dev; bypass=; rules=non_fast_forward; deletion
main-checks: active; target=~DEFAULT_BRANCH; bypass=; rules=deletion; required_status_checks(strict=true,checks=test (fast)|test (slow)|test (docs)|admissibility); non_fast_forward
main-review: active; target=~DEFAULT_BRANCH; bypass=RepositoryRole:pull_request; rules=pull_request(approvals=1,codeowners=true,methods=merge)
paper: active; target=refs/heads/paper; bypass=; rules=deletion; non_fast_forward
```

The `paper-release` reviewers are the paper's (`jshorish`, `mzargham`), not the code owners (his word, 12:05 EST);
the `main-review` bypass is his for 0.1 (his answer, 11:25 EST). WP78 makes this read-back a declaration in the tree
and a check that runs first in CI.

From WP78 the read-back is the checker's output: `uv run python scripts/check_repo_settings.py` compares the live
settings with `.github/governance.toml` (the values above, the code owners' access and the default workflow
permissions, which read back `write`: `WP78-rounds/gaps.md`, item 1) and reported `conforming (61 fields)` on
2026-11-17; the `controls` job runs it first in CI (`--runner`: 55 fields; local-only, the two workflow-permission
fields, whose endpoint needs Administration, and the four rulesets' bypass actors, which the API returns to
administrators only) and its report is the record at each head. At 13:37 EST he changed the `main-review` bypass
actor from the Repository admin role to his user (`User:10465438`, pull requests only); the declaration and the
recorded responses follow (`tests/data/wp78/`).

## G8 the pull request

His word, 23:15 EST 2026-11-17: "Go, open the PR" (`WP64-decisions.md`). The issue and the pull request opened by
the driver from `dev` at eada5a3e; links in `driver-log.md`.

Merged by him at 19:25:57 EST (the bypass through the API, `gh pr merge 3 --merge --admin`, after the merge box
did not render the bypass checkbox; `WP64-decisions.md`, "The merge"): merge commit 74e62fda, issue #2 closed by it.

## G9 after the merge

The Release run on the merge commit, https://github.com/DynamicalSystemsGroup/tradespace/actions/runs/44207809538
(00:26:20Z to 01:35Z on 2026-11-18, 19:26 to 20:35 EST on the 17th), conclusion success; its jobs in order:

| Job | Result |
|---|---|
| controls | success (`conforming (58 fields on the runner; 6 local-only)`) |
| admissibility | success |
| build and check | success |
| test / test (fast), test (slow), test (docs) | success (the slow shard 66 min, as in the dry run) |
| site / compose | success |
| tag and draft release | success: `v0.1.0` at 74e62fda |
| publish to TestPyPI | skipped (a push, not a dispatch) |
| publish to PyPI | success: https://pypi.org/project/tradespace/0.1.0/ (wheel and sdist) |
| deploy the site / deploy | success |
| publish the release | success: https://github.com/DynamicalSystemsGroup/tradespace/releases/tag/v0.1.0 (01:35:03Z; assets `sbom.cdx.json`, the wheel, the sdist) |
| on failure, clean up and open an issue | skipped |

The release notes carry the attestation line, verbatim:
`Controls: .github/governance.toml@4088a462f015 checked at 74e62fdaf256cc6e4f2db4fb90e10a02c3df9d6b: conforming (58 fields on the runner; 6 local-only)`.

The punch list's post-release checks, loaded live at 20:40 EST (the script and its output in the driver's scratch,
quoted here):

| Check | Result |
|---|---|
| `/`, `/paper/`, `/docs/`, `/docs/getting-started/`, `/docs/user-guide/overview/`, `/docs/theory/`, `/docs/generated/glossary/`, `/docs/api-reference/`, `/docs/further-reading/` | 200 each |
| `robots.txt`, `sitemap.xml` (27 entries), `preview.png` | 200 each |
| The root page's metadata | `og:title`, `rel="canonical"`, JSON-LD present |
| The Why triangle's three region labels on the deployed build | "all three trade", "metric 3 trades against metric 1", "metric 3 trades against metric 2" (the deployed `ternary-planted-light.png` looked at; the same labels as the Mac build) |
| GitHub releases page | lists 0.1.0; `releases/latest` 200 |
| PyPI | `tradespace` 0.1.0, two files |
| G1: a docs page loaded in a fresh tab after the release | no console error, no failed request (the theme made no releases request on this load) |
| G2s: every `github.com` link on the deployed pages (from the sitemap) and in `README.md`, `CITATION.cff`, `pyproject.toml`, unauthenticated | 15 on the site and 3 in the files, all 200 |

Also done: `paper` fast-forwarded to `dev`'s head 0dc2f4d2 at 19:27 EST (the branch had no commits of its own since
its cut at c0e210cc, so no merge commit and no pull request; the paper workflow's push run 44207902935 on it is the
first with WP79's two fixes, in progress at the time of writing); `qc/release` already deleted; the README's links
checked from `main`.

Left to him: `danlessa` added as Owner of `tradespace` on PyPI and TestPyPI (Manage, Collaborators), now that the
project exists under his account. Left to the driver: the paper checklist's first items (`release-checklist-paper.md`,
row B5p), the worktrees of the landed units retired, his acceptance of WP68 recorded.

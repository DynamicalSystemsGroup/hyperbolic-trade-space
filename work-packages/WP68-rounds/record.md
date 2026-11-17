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

## G8 the pull request

Pending his word.

## G9 after the merge

Pending.

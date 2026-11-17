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

Pending his keyboard items.

## G8 the pull request

Pending his word.

## G9 after the merge

Pending.

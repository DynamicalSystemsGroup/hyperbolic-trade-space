# WP40 before and after (D-9, R-7)

Before: `94cb6a1` (the build's start head H0). After: `da717e1` (the head the table was computed at, before this file's own commit).
Bytes are tracked blob bytes (`git ls-tree -r -l`), not blocks; MB = 10^6 bytes.

## By top-level entry

| Entry | Files before | Files after | MB before | MB after |
|---|---|---|---|---|
| `(root files)` | 15 | 15 | 0.69 | 0.69 |
| `.github` | 2 | 2 | 0.01 | 0.01 |
| `derivation` | 30 | 30 | 0.63 | 0.63 |
| `docs` | 90 | 67 | 1.54 | 1.37 |
| `examples` | 60 | 60 | 4.40 | 4.40 |
| `paper` | 47 | 47 | 4.27 | 4.27 |
| `scripts` | 15 | 15 | 0.28 | 0.28 |
| `site` | 3 | 3 | 0.02 | 0.02 |
| `src` | 12 | 12 | 0.21 | 0.21 |
| `tests` | 72 | 72 | 1.65 | 1.65 |
| `work-packages` | 807 | 495 | 56.28 | 7.91 |
| **all tracked** | **1153** | **818** | **69.99** | **21.45** |

## `work-packages/`

| | Before | After |
|---|---|---|
| files | 807 | 495 |
| MB | 56.28 | 7.91 |
| png/jpg screenshots | 333 | 0 |
| screenshot MB | 48.12 | 0.00 |

## Archive (what "Download ZIP" or a source tarball is)

| | Before | After |
|---|---|---|
| `git archive <rev> \| wc -c` (MB) | 70.94 | 22.15 |
| `git archive <rev> \| gzip -6 \| wc -c` (MB) | 53.07 | 7.88 |

The pack and the history are not changed (no rewrite; WP40 non-goal): `git count-objects -vH` is unchanged by a tree edit.

## Commands

```
git ls-tree -r -l <rev>   # sizes and counts, summed by top-level path
git archive <rev> | wc -c
git archive <rev> | gzip -6 | wc -c
```

Screenshots counted: 333 before (the readout counted 324 at 1d741d2; later packages added nine); 0 after.

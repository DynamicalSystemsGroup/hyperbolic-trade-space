# WP66a: choices made where the specification was silent

Each choice names the section it fills and why. The specification is `WP65-design/specification.md`; his three
answers of 2026-11-16 are in `WP64-decisions.md`.

## `release.yml`

1. **`qc/paper/**` is excluded from the release's push trigger** (`branches: [main, "qc/**", "!qc/paper/**"]`).
   Section 1.2 names `qc/**`, which also matches the paper's quality-control branches of 2.2; without the
   exclusion a push to `qc/paper/build` runs the software's suite and site as well as `paper.yml`.
2. **The tag check has four states.** `scripts/release_checks.py tag` prints `new`, `ours`, `site-only` or
   `taken`; `site-only` is his second answer (the tag on an earlier commit that is an ancestor, `src/`,
   `pyproject.toml` and `uv.lock` unchanged since it). A tag on a commit that is not an ancestor is `taken`.
3. **`deploy-site` needs `check` and `test` as well as `publish-pypi` and `site`**, and its condition reads the
   results: on a site-only merge `publish-pypi` is skipped, so the deploy must name the suite and the site
   directly and must read `needs.check.outputs.tag_state`, which only a direct need exposes. It uses `!cancelled()`
   rather than `always()`, so a cancelled run deploys nothing.
4. **`publish-release` runs on a site-only merge too**, with its publication step skipped, to close an open
   `Site redeploy of v<version> failed` issue. Its condition checks the results of its needs explicitly, since a
   skipped job anywhere upstream otherwise skips it.
5. **The changelog check is `--final` on a push to `main`, on a pull request and on a dispatch with `tag`**, and not
   on a `qc/**` push or a dispatch without `tag`. Section 1.2 names only the dispatch; the build plan's first QC run
   expects `check` green on `dev`'s head, whose changelog has only the `[Unreleased]` entry until WP68.
   It is skipped on a site-only merge (his second answer).
6. **`on-failure` on a site-only merge runs no clean-up**: the tag belongs to an earlier, published release, which
   the script refuses (exit 3). The issue is titled `Site redeploy of v<version> failed`. When `check` failed
   before the version was read, nothing was created; the issue is `Release at <sha> failed`.
7. **The clean-up's exit code does not fail `on-failure`**: it is written under the report, so the issue is opened
   in every case (exit 3 is an expected outcome after PyPI).
8. **The pull request's "no release in flight" check** lists runs of `release.yml` on `main` with event `push`, so a
   pull request's own runs do not count.
9. **`publish-pypi` checks out before it downloads `dist`** (a checkout cleans the workspace) and runs the hash check
   after the upload; the tag job fails if the release of the tag is already published.

## `scripts/release_cleanup.py`

10. **The retry after a removal is a re-run of the whole run** (`gh run rerun ID`), not `--failed` as the sample in
    1.4 prints: after the clean-up deletes the tag and the draft, a failed-jobs re-run would not repeat a `tag` job
    that had succeeded, and `publish-release` would find no release. When the script keeps state (exit 3) the retry
    is `--failed`, as specified.
11. **PyPI is read only when a tag or a release exists**: with nothing to remove the answer does not depend on PyPI,
    and the by-hand dry run reads nothing outside GitHub.
12. **The paper's tag shapes are copied from 2.3** rather than imported from `scripts/paper_mode.py` (WP66b's file):
    the script stays standard library, runnable with `--no-project` and independent of the paper unit's landing.
    The version shape is read from `scripts/check_release_version.py` as 1.4 says.
13. **The JSON report has three fields beyond 1.4's**: `dry_run`, `would_remove` and `errors`.

## `scripts/release_checks.py pypi`

14. **The PyPI read is retried** (six attempts, twenty seconds apart) when PyPI has no record or cannot be read,
    since its JSON can trail an upload; a hash mismatch fails at once. The file sets must be equal by name.

## `test.yml`

15. **Top-level permissions `contents: read`** (none were declared). **Windows's condition names the event**
    (`github.event_name != 'pull_request' && inputs.windows`), so a pull request never runs it even if an input
    default changes.

## Records

16. **`CHANGELOG.md`'s Notes no longer list PyPI as outside 0.1.0**: the release model publishes 0.1.0 to PyPI at
    the merge (build plan, section 6).
17. **`CITATION.cff` carries `version: 0.0.1`**, the version of `pyproject.toml` today; the release package sets
    0.1.0 and `date-released` with the version (software checklist row A1).
18. **The software checklist's states are read at `5e85196b`**; the old file's states, read at `c23cf60`, are not
    carried, since most of its rows changed meaning with the split.
19. **The contract's quoted block** gains the new keys that a reader of the contract needs (`build.site_workflow`,
    `build.pages_deploy_workflow`, `build.branches`, `build.paper_workflow`, `build.paper_artefacts`,
    `build.paper_mode_file`, `build.paper_modes`, and the three `docs.reference_key_*` keys).

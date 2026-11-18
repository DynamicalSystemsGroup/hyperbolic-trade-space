# WP77 — Decisions: the package is named `tradespace`

## His decision (2026-11-17, 10:20 EST), verbatim

Before the pending publisher was created:

> so this is our last chance to reconsider the name. one question. is just `trade-space` available?

The driver's answer: nothing named `trade-space` or `tradespace` on PyPI or TestPyPI (the simple index 404 for both;
PyPI treats the two as one name), no such repository under the organisation; a rename touches the import path, the
repository name, the Pages address and about 170 tracked files, and repeats the full verification.

> i want the shorter name. tradespace, let's rename the package in github and take the tradespace name in pypi

## Approval

The unit (the rename in the tree, verified) was approved by the driver as his proxy under the mandate, his words
above being the scope: distribution and import `tradespace`; repository `DynamicalSystemsGroup/tradespace` (renamed by
the driver with `gh repo rename` the same hour; the old address redirects); Pages at
`https://dynamicalsystemsgroup.github.io/tradespace/`; the pending publishers name project and repository
`tradespace` (created by him, 2026-11-17, screenshots in the session). Interface contract amendment 30 cites this
file. Dated records and verbatim quotations (`*-decisions.md`, `driver-log.md`) keep the old name as history.

## Landing (2026-11-17)

Two commits from the unit's branch, rebased onto `dev` and fast-forwarded: the rename (168 tracked files by exact
replacement; `uv.lock` re-locked; contract amendment 30; the CHANGELOG line under 0.1.0) and the experiment
ledger's re-adoption of four entries whose hashed files changed only in their import, by the ledger's own
`readopt` (which now keeps the superseded run's toolkit runtime, since a re-adoption runs nothing). The unit's
checks and the driver's are in `driver-log.md`. A local SysML toolkit cache moves from
`~/.cache/hyperbolic-trade-space` to `~/.cache/tradespace`; CI refetches it once.

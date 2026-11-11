# WP34 — Decisions (Windows as a third platform)

The supervisor's words are quoted verbatim where they bind (release-candidate.md, "Windows"); the assistant's calls are listed for his review.

## Scope gate (2026-11-11, 12:20; scope at 95c3c03; the assistant)

No open decisions; the Agent's defaults approved as one item, with one change to the mechanism: GitHub dispatches only a workflow file that exists on the default branch, and `main` has no `windows.yml`, so the spike job moves into `test.yml` as a `windows-latest` job behind a `workflow_dispatch` input (`windows`, default false) that the assistant sets to true when dispatching; pushes do not run it until stage 4 folds it into the matrix at gates. **Assistant, verbatim:** "WP34 approved as drafted; the spike runs from test.yml behind a dispatch input."

## Stage (2), the assistant (2026-11-11, 13:20; readout 19635a2)

The spike's 74 items fall in five classes: 55 from no `z3` on the Windows runner's PATH (an environment item), 6 from
`read_text()` without an encoding, 6 from CRLF checkouts changing the hashes of committed text, 6 from tests that
assume a POSIX executable bit, 1 not yet explained (`tab-C` committed output under the tolerance comparison).
**Option 2:** Windows runs the fast and the slow shards once the fixes are in; the docs-paper shard stays Linux and
macOS, with the reason stated in the README and the reproducibility appendix (the paper's build toolchain is pinned to
the container and the Linux runner; a Windows user builds the paper in the container). Stage 3, the fixes, each with
its test: `z3` on PATH in the Windows job (the wheel's executable or a package step), a `.gitattributes` that keeps
the hashed text files at LF on every checkout (and the hashing code reading bytes as committed), `encoding="utf-8"`
on every `open` and `read_text`/`write_text` with a test that greps for the bare forms, the six POSIX-bit tests made
platform-aware (a Windows branch that tests the same behaviour, or a skip with the reason when the behaviour has no
Windows meaning), and the `tab-C` item explained before it is touched. Then a second spike with the fast and slow
shards; then stage 4, the matrix entry run on dispatch and at gates.

**Stage 3 landed (843d2eb and its commits; the assistant, 13:45):** the five fixes are on dev; the three
ledger-hashed files that keep bare reads (`cubesat_model.py`, `legacy_oracle.py`, `cubesat_oracle.py`) get their
`encoding="utf-8"` at the WP30 regeneration, which re-hashes them anyway, and are re-adopted there; the second Windows
spike runs when the workflow's input allows the slow shard (checked below). The fast suite at the head is the
watcher's and Linux's to confirm; Linux dispatched.

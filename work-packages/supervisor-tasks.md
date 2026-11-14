# The supervisor's tasks (kept apart from the autonomous work)

Written 2026-11-14, 21:20, at his request: "a clear separate list of tasks that i need to do (facilitated by you but may
involve configuring accounts in the browser with lots of guarded activites meriting explicit approvals or my own hands on
keyboard so we need to do them together)". Two kinds: **his word** (a reading, an acceptance, a call, given in chat or
a popup, recorded verbatim) and **together at a keyboard** (accounts, settings, forms; the assistant prepares the exact
names and steps, he performs the guarded actions). Order within each kind is the order the path needs them.

## His word

| # | Task | When | Prepared by |
|---|---|---|---|
| W1 | Accept WP33, WP35, WP37, WP38, WP39, WP40 (delivered, driver-verified; one line each) | any time | `supervisor-review-list.md` |
| W2 | Accept the third paper unit (ca352f5) and the abstract landing (735fa51) | after CI is green on both | the driver log's entries |
| W3 | WP42 naming item 2: `tension_report`, its `tension_directions`, `tension_loadings`, `plot_tensions` (rename all; keep the report, rename the rest; keep all) | before the WP42 build starts | `WP42-rounds/spike/readout.md`, section 7 |
| W4 | WP42 naming item 3: Figure 7 (replace by the full tension matrix; by the compact one; keep and add; neither) | after the figure's cold read lands | the cold-read reports on branch wp42 |
| W5 | The Section 9 sentence on the pick's tension: accept, amend or decline | with W4 | readout section 6 |
| W6 | Approve WP50 (topological holes by persistent homology, research only) | any time | `WP50-scope-of-work.md` |
| W7 | Close read of the five entry surfaces; the two root-page sentences that are his (the summary paragraph; "bespoke or opaque") | before the PR | `WP11-final/abstract/entry-surfaces-consistency.md` |
| W8 | Reading pass G.2 | before the PR | the paper's Appendix G.2 |
| W9 | Accept each remaining package as it is delivered and verified (WP41, WP43, WP45, WP46, WP47, WP48, WP49 readouts; the WP42 build; the held-out reads' triage) | as they land | the driver log |
| W10 | The contributor guideline: read the WP49 readout, choose the shape, sign off the covenant's text | after the WP49 readout; placement in 0.1 or after is his call then | `WP49-rounds/spike/readout.md` |
| W11 | The version unit's timing (0.1.0 lands with WP47's metadata) | when WP47 delivers | `WP47-rounds/pypi-checklist.md` |
| W12 | Review the PR from `dev` to `main` with the reviewer's guide, in sittings; merge it `--no-ff`; push the `v0.1.0` tag | the last step | WP8b |

## Together at a keyboard

| # | Task | What he does | What the assistant prepares | When |
|---|---|---|---|---|
| K1 | A readable copy of "Protocols and Institutions v.1" | copies the file into `~/Downloads` (the iCloud folder is not readable from the session) | hands it to the WP49 unit as background | any time |
| K2 | Broadbalk wheat data | requests the dataset through the e-RA form (doi:10.23637/rbk1-yld6822-01, CC BY 4.0) and places the file where the WP45 unit's note says | the exact file name and location; the record waits on it | any time |
| K3 | PyPI and TestPyPI accounts | signs in or creates the accounts, enables two-factor authentication | nothing to prepare; his credentials are never typed by the assistant | before W11 |
| K4 | Pending trusted publishers on TestPyPI and PyPI | adds a pending publisher for `DynamicalSystemsGroup/hyperbolic-trade-space` with the workflow file name and the environment names WP47 delivers | the exact names in `WP47-rounds/pypi-checklist.md` | when WP47 delivers |
| K5 | GitHub environments `testpypi` and `pypi` | creates them on the repository with himself as required reviewer, so no publish runs without his click | the names and the reviewer rule | with K4 |
| K6 | Branch protection | `main`: require a pull request, require the test workflow, require review from code owners, restrict who can merge; `dev`: require the test workflow | the checklist in `docs/maintainers.md` with exact setting names | when WP47 delivers |
| K7 | CODEOWNERS enforcement and the maintainers' team | confirms the `CODEOWNERS` file names him; creates the organisation team if he wants onboarding to be one line later | the file and the page | with K6 |
| K8 | Repository visibility and Pages | decides when the repository goes public (PyPI's source link and the docs site need it) and enables GitHub Pages from the workflow | the Pages source setting and the order of steps | before the publish |
| K9 | The TestPyPI dry run | clicks the environment's approval when the dispatch from `dev` asks | the dispatch and the check of the uploaded package | after K4, K5 |
| K10 | The release | after W12's merge and tag, approves the `pypi` environment; checks the project page | the checklist's last section | the last step |
| K11 | Governance checks as release gates (after v0.1) | the settings or tokens the chosen checks need, if any | WP48's readout names them | after v0.1 |

Items move to the record (`WPn-decisions.md`, `driver-log.md`) as they are done; this list is rewritten, not appended.

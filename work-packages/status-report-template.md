# 0.1 candidate status report (template)

The report the assistant posts at each tick and the PM fills at each batch, built on the deliverables grid
(`deliverables-grid.md`). The supervisor, 2026-11-11: "use that grid to create a status report template so we can
start converging to our 0.1 release candidate". Short by design: the grid is the table, everything else is a line or
a few bullets; under about 250 words besides the grid. Changed cells since the last report are marked with an
asterisk. Blank cells are not applicable and stay blank.

---

**0.1 candidate status, <date>, dev at <head>.** Needs the chief engineer: <no | yes: one line>.

| Deliverable | Explore | Use | Theory | Model | Evaluate |
|---|---|---|---|---|---|
| Root page | <state, evidence> | | | | |
| README and repository layout | <> | <> | | | <> |
| Docs user guide | | <> | | | <> |
| API reference and examples | | <> | | | <> |
| Package (install, API, tests) | | <> | | | <> |
| Paper body | <> (abstract) | | <> | <> | |
| Paper appendices | | | <> | <> | <> |
| Derivations and proof map | | | <> | | <> |
| Case model, views, stakeholders, data | | | | <> | <> |
| Release items (container, CI x3, changelog, version, guide) | | <> | | | <> |

State: `-` not started, `~` in progress, `d` delivered to the assistant, `A` accepted. Evidence: the last reader round
or user test for that column and its verdict (for example `R3 B 6/6`, `U1 done/2 stops`), or the check that ran
(`CI 3/3`, `watcher 2285`), with the commit where it matters. Columns: Explore P1, P8; Use P2, U1 to U4; Theory P5,
P6, P9, P10; Model P3, P7; Evaluate P8, P2, the reviewer.

**Distance to the candidate.** One line per open package or gate: `<package>: <state>; next gate: <what, who>`.

**Verified since the last report.** Platform greens (head, result), the assistant's own passes (what, result).

**Calls since the last report.** The rows added to `supervisor-review-list.md` (one line each) and any supervisor
ruling applied.

**Risks and incidents.** One line each, with what was done; `none` when none.

**Next expected.** The next two or three things, with who delivers them.

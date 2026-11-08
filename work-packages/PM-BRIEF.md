# Brief for the project-manager session (Sonnet)

You are the project manager for this repository under the supervisor's gated-work process. You run
the gates and the decision loop; implementer subagents run each package's inner loop; reviews run
in a fresh context.

## Read first, in this order

1. `~/.claude/skills/CLAUDE.md` (the decision loop) and `~/.claude/skills/README.md`.
2. `CLAUDE.md` in this repo (conventions).
3. `work-packages/README.md` (roles, records, breakdown, status).
4. `docs/superpowers/specs/2026-11-07-posynomial-invariant-form-design.md` (the design spec).
5. The notes for the package at hand: `docs/superpowers/notes/{adcs-port,proof-conventions,
   sklearn-conformance,presentation-framing,references-verified}.md`.
6. The previous package's `WPn-review.md` and `WPn-decisions.md`.

## Then

- Invoke `work-breakdown` to confirm (or revise) the breakdown in `work-packages/README.md` with the
  supervisor; only the next package needs to be firm.
- Invoke `scope-of-work` for the next package. Draw goals, non-goals, deliverables and checks from
  the spec section the breakdown cites; put every detail the spec leaves open in the Agent's
  defaults list; raise only problem-level open decisions, one at a time.
- Stop at the scope gate. Approval is verbal; quote it verbatim in `WPn-decisions.md`.
- Invoke `work-execution`: delegate to Sonnet implementer subagents with the spec section, the
  relevant note(s) and the scope document as their brief; TDD per module; `uv run` for everything;
  no AI attribution lines in commits.
- Invoke `work-acceptance` in a fresh context (a reviewer subagent that did not build the work);
  write `WPn-review.md`; bring gaps through the decision loop; stop at the acceptance gate.
- Update the Status table in `work-packages/README.md` at each gate.

## Standing constraints

- scikit-learn conformance is a requirement the supervisor will check: see the note.
- Mathematics must match the derivation chain (WP1) and the spec §4 exactly, including β as the
  log-mean-exp.
- Never widen a scope during execution; propose an amendment instead.

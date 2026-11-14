# WP49 — Scope of work: a contributor covenant for an AI-native, trustworthy package (research spike)

| | |
|---|---|
| **Status** | DRAFT, a research spike. Approved only by the recorded act below; nothing is built before then. |
| **Supervisor (accountable)** | mzargham |
| **Repository** | `DynamicalSystemsGroup/hyperbolic-trade-space`; the readout under `work-packages/WP49-rounds/` |
| **Approval record** | The supervisor's verbal approval, quoted verbatim in `work-packages/WP49-decisions.md` |
| **Acceptance record** | The supervisor's acceptance of the readout, quoted verbatim |

## Purpose

The supervisor's direction (`WP49-decisions.md`): a contributor covenant, tied explicitly to how AI is used and
supervised, for a package that is AI native and must also be trusted and trustworthy. The spike finds out what such a
covenant would say, what exists to build on, and what this repository already does, and returns options. It writes no
covenant.

## Goals

- G1. **The Contributor Covenant, read:** its current and previous versions, what each covers (conduct between people,
  enforcement, scope), its licence and attribution terms, and what it does not cover (how the work itself is produced).
- G2. **What other projects say about AI-assisted contributions, read:** the published positions of open-source projects
  and foundations, from bans to required disclosure to accountability rules; for each, what it requires of a
  contributor (disclosure, a human who stands behind the change, provenance and licensing, review burden), the problem
  it answers, and the source with its date. Projects of several sizes and ecosystems, so the readout is not one
  community's view.
- G3. **This repository's practice, written as it is:** supervisor-gated work packages with approval and acceptance in
  his words; the no-AI-attribution rule with human accountability on every commit; reviews that run the code and look
  at the render; claims backed or narrowed, never caveated; the driver log; what each of these promises a user and
  which of them a covenant would state as a commitment rather than a process.
- G4. **A readout with plain options** for the covenant's shape, at least: the Contributor Covenant adopted as published
  beside a separate AI-use and supervision statement; the Covenant extended with that statement; a covenant of this
  repository's own. For each: what it promises a user (how a reader knows a human stood behind a change and what was
  checked), what it asks of a contributor, how it would be checked (the hook into WP48's verification cases), and its
  cost. The accountability principle he stated on 2026-11-14, 20:50 (`WP49-decisions.md`) is a given, not a tension:
  actor agnostic at the code level, a named human who owns what they merge, no AI trailers, AI use neither disclosed by
  rule nor an excuse; the readout sets the other projects' disclosure norms against it (what each secures, and whether
  the protocol approach secures it another way) and drafts the covenant's accountability clause in those terms for his
  sign-off. One tension remains named, not resolved: what "AI native" commits the project to in public.

## Non-goals

- Writing or adopting the covenant, a code of conduct or an AI-use policy; changing `CONTRIBUTING.md` or any other
  file outside `work-packages/WP49-rounds/`.
- Any position on the law of AI-generated contributions beyond what the sources read say, cited.

## Deliverables

| ID | Deliverable | Serves |
|---|---|---|
| D-1 | `work-packages/WP49-rounds/spike/covenant-notes.md`: the Contributor Covenant read, versions, terms, coverage | G1 |
| D-2 | `work-packages/WP49-rounds/spike/policies-survey.md`: one table row per project (position, what it requires, the problem it answers, source, date read), with a short reading of the spread | G2 |
| D-3 | `work-packages/WP49-rounds/spike/our-practice.md`: this repository's practice as it is, each item citing the file that records it | G3 |
| D-4 | `work-packages/WP49-rounds/spike/readout.md`: the options with promises, asks, checks and costs; the tensions; what the supervisor decides next | G4 |

## Requirements

| ID | Requirement | Checked by |
|---|---|---|
| R-1 | Every statement about a source cites it with the date read; quotations are short and attributed; no source enters without a resolved URL | the notes; the assistant resolves three citations at random |
| R-2 | No file outside `work-packages/WP49-rounds/` changes | `git diff --stat` |
| R-3 | D-3 describes the practice as recorded, not as intended: each item points at `CLAUDE.md`, `work-packages/README.md`, `PM-BRIEF.md`, a decisions file or the driver log | the file |
| R-4 | The readout's options are plain, in no steering order and with no recommended tag | the file |

## Definition of good

The supervisor reads the readout and can say which shape he wants and what the covenant must say about AI, with the
sources and this repository's own record in front of him.

## Definition of good enough

- D-1 to D-4 delivered; R-1 to R-4 pass; the readout's options each carry promises, asks, checks and costs.

## Definition of done

Good enough met, no open item remaining, and the supervisor's acceptance of the readout recorded verbatim in
`WP49-decisions.md`. The covenant itself is a later package scoped from his answer.

## Agent's defaults

- The spike runs as one research agent on Sonnet with web access, in a worktree; the assistant checks three citations
  and reads D-3 against the files it cites *(default)*.
- The survey covers at least eight projects or foundations across more than one language ecosystem and includes at
  least one ban, one disclosure rule and one accountability rule *(default)*.
- The readout lands before the v0.1 pull request so the covenant's adoption can be decided with the release in view;
  whether the covenant is in v0.1 or after it is his call at the readout *(default)*.

## Open decisions (for the supervisor)

None. The direction of 19:40 settles the aim; placement is decided at the readout.

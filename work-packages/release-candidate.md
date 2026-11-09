# The 0.1 release candidate: mandate, decisions, path

Records typed by the driver. Decisions are the supervisor's, quoted verbatim.

## The mandate (2026-11-08)

**Supervisor (mzargham), verbatim:** "your job is to loop on the dev using local host and all the
tools at your disposal to get me a candidate release. when you are done you can give me a PR. i will
do my own comprehensive review. i am a human not a computer so although this work is my core
intellectual contribution if you present the information badly i wont be able to sign off on it. you
have a pretty clear picture of what i want for a first 0.1 release and how i expect you to verify
the correctness and how i expect you to make the UX and information design robust to diverse
readers but if you have any other questions you want to resolve you should clarify them now"

**The chain, verbatim:** "our org architecture is me -> you -> pm -> subagents to spec"

## Clarified before the run (popups, one at a time)

- **Who holds the gates until the PR.** Options put: the driver holds them provisionally /
  acceptances the driver's, scopes his / gates stay with him. **Verbatim:** "i am the only one who
  can accept and merge a pr but you can define and accept scopes to get to something you believe i
  will expect. don't hesitate to define spikes if you don't have the info you need to make a call.
  at will eventually review the calls you made as part of my acceptance but if you approach them
  scientifically its unlikely i'll reject them. (though it is my perogative to do so)".
  Disposition: the driver defines and approves scopes and amendments and accepts packages, each
  recorded as the driver's call with its evidence; a spike is run where the evidence for a call is
  missing; every call is listed for his review; only he accepts and merges the PR.
- **The trade-off-aware search.** Options put: in the candidate / after 0.1 / spike first.
  **Verbatim:** "After 0.1". Disposition: WP12 follows the release; the paper's search section
  stays short, marked as future work, with no results.
- **The data under the paper's case.** Options put: swap for 0.1 if the evidence supports it / stay
  on the frozen data. **Verbatim:** "Swap for 0.1 if the evidence supports it". Disposition: after
  the system model package is verified, the case and its records move to the new data; every number
  that changes is listed with its reason; the frozen data stays as the cited comparison; if the new
  data changes a conclusion, the driver stops and brings it to him.
- **The hand-off.** Options put: one guide in reading order / sittings by output / several smaller
  PRs. **Verbatim:** "Sittings by output". Disposition: one PR from `dev` to `main` with a
  reviewer's guide split into sittings he can take on different days (the paper; the docsite and
  root page; the code and derivations; the calls made for him), each with a short checklist and its
  own localhost entry point.

Already decided in earlier records and not asked again: version 0.1.0; MIT, copyright Dynamical
Systems Group (`WP8-decisions.md`); PyPI deferred; no image on a registry; nothing deploys before
the release; the PDF export later.

## The path to the candidate

| Step | What | Depends on |
|---|---|---|
| 1 | System model tidy-up (WP15) delivered, verified, accepted by the driver | in execution |
| 2 | Docsite restructure (WP8a Amendment 2) delivered; the driver's full browser pass; accepted | in execution |
| 3 | The paper (WP10 with Amendment 1) delivered: proofs step for step, appendices, the container of record; structural acceptance by the driver | in execution |
| 3b | The several-term fit with soft weights (WP17, scoped by the driver on the supervisor's conditional direction of 2026-11-09), and WP10 Amendments 4 and 5 (the abstract, the vocabulary review, the claims review) | 3 |
| 3c | Ternary plots in the documentation's examples (WP18; the supervisor's request of 2026-11-09; scoped by the PM, approved by the driver): the pattern documented, accessible and interpretable, as simple as the other example plots | 2, 3b |
| 3d | Figures: selection, generation and narration by section (WP19, backlog; the supervisor's direction of 2026-11-09; two gates held by him: the slots, then the figures), with the diagram spike in parallel | 3, 3c |
| 4 | The data swap (a package the driver scopes): the case, the K = 1, 2, 3 record and the paper's numbers on the new data, every change listed | 1, 3 |
| 5 | Readability and correctness loops over the reader grid (WP11, the driver scopes): context-gapped reads, triage, revision, re-test; browser passes | 3, 4 |
| 6 | Release candidate (WP8b, the driver scopes): version, license file, changelog, the archive cleared, stable reference keys from the docsite into the paper, the punch list, the reviewer's guide in sittings | 2, 5 |
| 7 | The PR from `dev` to `main` | 6 |

After 0.1: the search (WP12); publishing to an index or a registry; the PDF export.

## What "candidate" means (the driver's definition of done; his review may change it)

- Every package above delivered, verified by the driver independently, and recorded.
- The whole suite, lint, format, the lock check, the lemma chain and the proof-map checker pass:
  on this machine, inside the container of record, and on CI by a manual run on `dev`.
- The paper's committed numbers and figures were produced inside the container of record, and a
  cold reproduction from Appendix F alone regenerates them.
- The staged site (root page, docsite, paper) has had the driver's full browser pass on every
  page, at desktop and phone width, in light and dark, with the findings fixed or listed.
- The reader grid's stopping rule is met and the held-out cells have been read once; the whole
  grid is reported with its worst cells.
- No commit carries an attribution line; nothing has been merged to `main`, tagged, deployed or
  published.
- The reviewer's guide exists, sized for a person, and lists every call the driver made with its
  evidence, every number that changed, and what is known to be weak.

## The driver's calls (each for the supervisor's review)

Kept in `driver-log.md` ("Scopes and acceptances by the driver"), with the evidence for each.

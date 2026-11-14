# WP49 D-4: readout, a contributor covenant for this package

Read 2026-11-14 at `dev` a5f1278. Sources: `covenant-notes.md` (D-1), `policies-survey.md` (D-2), `our-practice.md` (D-3).
This readout writes no covenant and changes no file outside `work-packages/WP49-rounds/`. The two clauses in
"The clauses, drafted" are drafts for the supervisor's sign-off.

## What was found

- The Contributor Covenant (3.0, released 2025-07-28, licensed CC BY-SA 4.0) is a conduct document: how people treat each
  other, who enforces, with what ladder. It says nothing about how work is produced, who may be the named author of a
  change, or tools (D-1). The Linux kernel carries it and keeps its rules for tool-generated work in separate pages.
- Fourteen projects and foundations state positions on AI-assisted contributions (D-2): four bans (Gentoo, NetBSD, QEMU,
  Zig), disclosure rules of three kinds (kernel, scikit-learn, statsmodels, Ghostty, curl for reports; LLVM, Fedora,
  Apache with a trailer), accountability rules (kernel, Fedora, CPython, statsmodels, QEMU) and permissions under
  conditions (Apache, Linux Foundation).
- This repository's record (D-3) already has the process the principle needs: gated scopes, reviews that run the thing,
  one named supervisor, a CI check against attribution lines, and one author name on all 1,869 commits. What it does not
  have is any document that tells a user so: no `CONTRIBUTING.md`, no `CODE_OF_CONDUCT.md`, no pull-request template.

## His principle and stance, as given

Given, not weighed (`WP49-decisions.md`, 20:50 and 21:10): the bar for a contribution is actor agnostic at the code level;
a named human is the contributor and owns what they merge; AI use is neither required to be disclosed nor forbidden, and
never an excuse; what is enforced is the rules (narrow scopes, review against the scope, blast radius, readable
history); no AI trailers; coding agents and agent-based editors are part of the landscape as an editor is; tool use may,
and in some cases should, be documented where that belongs, never as the contributor in the git history; laundering
code through a model to escape its licence is a licence violation; governance holds as well for any model as for any
editor.

## The other projects' disclosure norms set against the principle

For each norm: what it tries to secure, and whether the protocol approach secures it another way. Where the answer is
"partly" or "no", the row says what is given up.

| Norm (who) | What it secures | Does the protocol approach secure it another way? |
|---|---|---|
| Ban (Gentoo, NetBSD, QEMU, Zig) | Clean provenance: no output of a tool whose training data and licence status are unsettled; for QEMU and the kernel, the Developer Certificate of Origin, which only a person can certify | Partly. The licence rule (laundering is a licence violation) and the owner's duty to answer for what they merge cover the same legal exposure by putting it on a named person; they do not remove the exposure itself. Nothing here checks a patch's origin by machine. A project that wants no model-derived code at all gets that only from a ban. The principle declines it (refusing models is not asked) |
| Required disclosure that a reviewer acts on (scikit-learn, statsmodels, Ghostty, kernel cover letters) | Lets a maintainer scale scrutiny to the tool's share; filters automated and unreviewed submissions; a rejection ground for a missing statement | Partly. Every change meets the same bar whatever made it (narrow scope, review against the scope, small blast radius), so scrutiny is not graded by a statement. What is given up: a reviewer cannot read the tool's share from a statement, and a missing statement is not a ground to reject. What is gained: no statement that cannot be checked is relied on, and no one is penalised for honesty |
| Disclosure that supports licence tracing (Apache, Linux Foundation, curl for patches) | A record of where output came from, so third-party material and tool terms can be examined later | Partly. The tools clause lets contributors record tools where the work's record is kept, and makes a licence-violating import a violation however it arrived. The licence of a tool's terms (Apache and the Foundation ask contributors to check them) is not checked by this repository's process today |
| Trailer in the commit (LLVM `Assisted-by:`, Fedora `Assisted-by:`, Apache `Generated-by:`) | A machine-readable provenance field that a script can count | No, by design. The principle puts no tool in the contributor fields of git, because a trailer blurs the single accountable name; tool use is recorded in the pull request description and the work package's record, which a person reads and a script does not parse. What is given up is a git-parseable count of tool-assisted commits |
| Accountability (kernel `Signed-off-by`, Fedora "always the author", CPython "owns", statsmodels, QEMU) | A person answers for the change | Yes: this is the principle. The kernel is the nearest neighbour: it forbids an agent's `Signed-off-by` and requires the human to take "full responsibility"; this repository goes one step further and puts no tool in the contributor fields at all |
| Reviewer-burden rules (LLVM "extractive", scikit-learn "fully-automated", Ghostty denouncement list, CPython close-without-explanation) | Maintainer time; a stop on unattended automation and on volume | Partly. Narrow scopes and review against the scope make an unreviewed change fail the bar, and a named owner is needed to merge. A rule against agents acting in project spaces with no person behind them is not stated by the principle; it is implied by "a named human owns what they merge". Whether to say it in the clause is for him |

## Where tool documentation belongs in this repository's own records

From D-3, tool use is documented today in the package records (roles and models named in `work-packages/README.md` and
`PM-BRIEF.md`, reviews as files, decisions quoted verbatim) and nowhere else. The places that fit the stance, in
order from the contributor's act to the record:

1. **The pull request description** (a "tools used" field in a template is WP47's area; no template exists in `.github/`
   today).
2. **The work package's record**: its scope of work (what agents may do and what blast radius), its review (what was run
   and by whom or by what), its decisions file (his words), and the driver log (what was decided for the PM, with the
   checks run at which commit).
3. **Not** the git author, co-author or trailer fields, and not a source-file header: these are the places the CI grep
   already refuses (`.github/workflows/test.yml` lines 32 to 39) and where it would blur who owns the change.

## The clauses, drafted (for his sign-off; not adopted)

**Accountability clause (draft).**

> Every change merged here has a named human contributor: the person who submits it, who owns it. To own a change is to be
> able to explain it, to have checked it against its scope, and to answer for it afterwards. The bar a change must meet
> does not depend on what produced it: the same scope, the same review, the same blast radius, the same readable history.
> You are not asked whether or how you used AI, and "a tool wrote it" is never an answer to a question about the change.
> Commits name people. No tool is a contributor, so no commit carries a trailer or line naming a tool as author,
> co-author or generator.

**Tools clause (draft).**

> Coding agents and agent-based editors (Claude Code, Codex, Devin, Cursor and their like) are part of how software is
> written today, as an editor is; nobody is asked to avoid them or the models behind them. You may document which tools
> you used, and in some cases should, in the pull request's description or the work package's record; this is never
> done in the git history as the contributor. Putting someone else's code through a model to escape its licence is a
> licence violation exactly as copying it would be. This project's checks are written to hold whichever model or editor
> you use.

Open in the wording, for him: (a) "in some cases should": which cases (the draft names none, because his words give
none); (b) whether the accountability clause also states that no agent merges or opens a change without a named person
behind it (the reviewer-burden row above); (c) whether "an editor is" stays in the user-facing text or is replaced.

## The covenant's shape: three options

The order is alphabetical and carries no meaning. Each option includes the two clauses; they differ in where the clauses
and the conduct text live.

| | Option A: the Covenant as published, beside a separate statement | Option B: the Covenant extended with the statement | Option C: a covenant of this repository's own |
|---|---|---|---|
| What it is | `CODE_OF_CONDUCT.md` is Contributor Covenant 3.0 unaltered, with its attribution line and a filled-in reporting contact; a separate `CONTRIBUTING.md` (or a section of it) holds the two clauses and the process they rest on | One `CODE_OF_CONDUCT.md`: Covenant 3.0 with a section added for how work is produced and who owns it | One document written by this project, containing conduct rules, the two clauses and the process; it may borrow the Covenant's enforcement ladder with attribution |
| Promises a user | Conduct standard that a reader recognises; a separate, readable statement of who owns a change and what was checked | One document holds both promises, so a reader meets the ownership rule where they meet conduct | The promises are exactly this project's; wording and defined terms match the glossary |
| Asks of a contributor | Follow the Covenant; follow the two clauses and the scope and review process; a reading of two documents | Same asks, in one document | Same asks, in one document in the project's own terms |
| How it would be checked (WP48's verification cases: requirement, method, evidence, verdict) | The clauses are checkable separately from conduct; for example: V1, no commit message carries an attribution line (automated; the CI grep, `.github/workflows/test.yml`; evidence: the CI log; verdict pass or fail); V2, every package under review has a scope, a review and a decisions record (a script over `work-packages/`; evidence: the report); V3, the merged history names a person as author on every commit (a script over `git log`; names only, see below); V4, the claims register's test passes. The licence rule has no automated check (a reviewer's inspection; evidence: the review record) | Same checks; the extended text gives the checks a single document to cite | Same checks, and each clause can name its check in the text because the document is the project's own |
| Cost | Lowest drafting cost: two short documents, adoption of the published text with attribution. Share-alike (CC BY-SA 4.0) applies only to any adapted text, not to the separate statement. The Covenant's reporting placeholder must be filled (WP47's maintainers page) | An adapted text: attribution as "adapted from" and the adapted covenant shared under CC BY-SA 4.0; a later Covenant version means re-merging the edit | Highest: all conduct and enforcement wording is the project's to write and keep; no external text to track; borrowing the enforcement ladder carries the attribution and licence terms in D-1 |

What the checks can and cannot show, which applies to all three: V1 and V3 show that no tool is named in the contributor
fields and that a name is there; they do not show that a human sat behind the name. The principle rests on the
accountability of the named person, which no repository check establishes; the records (scope, review, decisions) show
that the process was followed, not who typed.

## Tensions to name

1. **Covenant 3.0 already has one line near provenance** ("Failing to credit sources", D-1) and the tools clause's
   licence rule is a second statement of something like it. Which document hosts the licence rule is a drafting choice
   under each option.
2. **The history is one author name.** Agents commit under the supervisor's identity (R-16 of WP1: authored as Michael
   Zargham), so today the named owner of everything is the supervisor. The principle holds for outside contributors by each
   owning what they merge; nothing in the record shows how that works in practice because there has been no such
   contributor yet (D-3, "What the record does not contain").
3. **Giving up disclosure's benefits is a choice with a price** (the norms table): scrutiny that scales to a stated tool
   share, a git-parseable count. The approach substitutes a uniform bar. The readout states it so the supervisor signs
   it knowing.
4. **The conduct ladder needs someone to run it.** Covenant 3.0 names "Community Moderators" and leaves the reporting
   method blank; a single accountable supervisor fills both until there are others. WP47's maintainers page is the
   record for it.
5. **Policy dates.** Several of the sources have no date on the page (D-2); the readout's picture is of the pages as read on
   2026-11-14, and a source's later edit is not tracked.

## What the supervisor decides next

1. The shape: A, B or C.
2. The wording of the two clauses, including the three open points under the drafts.
3. Placement: in v0.1 or after (the scope's default leaves this to him at the readout).
4. Whether a pull-request template (WP47) carries a "tools used" field.

## For the paper and the next release

- **May say now:** the repository is built as supervisor-gated packages with a named accountable person and an
  automated check that no history line names an AI tool as a contributor (D-3, P1, P2, P5).
- **May not say:** that the project has a published contributor covenant or an AI-use policy; that a human reviewed every
  line (the record shows process, D-3); anything about other projects' policies beyond what D-2 cites and dates.
- **The next release builds:** the covenant text and files he chooses (a later package), the template field if chosen,
  and the verification cases that check the clauses (WP48's build).

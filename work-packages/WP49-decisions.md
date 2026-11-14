# WP49 — Decisions: a contributor covenant for an AI-native package (research spike)

## The direction (2026-11-14, 19:40), answering WP47's OD1

**Supervisor, verbatim:** "i think it would be good to have a contributor covenant and given the nature of this work to
date it may need to be explicitly tied to how AI is used and supervised. i want this to be an AI native open source
package but i also need it be trusted and trustworthy. so i think the contributor covenant is its own spike."

**Applied as:** a research spike with a readout, `WP49-scope-of-work.md`. The spike reads the Contributor Covenant,
reads what other open-source projects have published on AI-assisted contributions, writes down this repository's own
practice as it already is (supervisor-gated work packages, decision records in his words, human accountability on every
commit with no AI attribution lines, reviews that run the thing, claims backed or narrowed), and returns plain options
for a covenant that states how AI is used and supervised here and what a user may trust because of it. The covenant
itself is written only after his word on the readout.

## Approval

**Supervisor, verbatim (2026-11-14, 19:50; popup, multi-select over WP47, WP48, WP49):** "WP47,WP48,WP49"

**Applied as:** WP49 approved as scoped; the spike starts, readout before the v0.1 pull request.

## The principle behind the no-attribution rule (2026-11-14, 20:50), with two of his papers attached

**Supervisor, verbatim** (the papers: "Formalizing Document Assurance" and "Protocols and Institutions v.1", given as
background to understand the approach, not to cite or copy): "\"no-attribution rule against the disclosure norms other projects use\" the no attribution rule is a git rule; my feeling is
that it offers an easy punt of responsibility. \"oh claude wrote that\" it is not an acceptable excuse. the idea here is that
our approach is that the bar for contributions to this repo is actor agnostic at the code level, and human actors are the
named contributors. if you want to merge code you have to own it. we are going to be enforcing narrow well defined scopes,
reviews against those scopes, blast radius, git history readability and much more. but my requirement that AIs are not the
named committers is about having a named responsible party. i don't care whether or how you used AI as long as you follow
the rules and stand behind your work. while i understand the no AI trailers is an uncommon move, its designed to move the
question away from AI or not AI towards explicit accountability for the committer.

i will ultimately need to be the person finally signing off this contributor guideline but you should look at my work on
here and here. keep in mind that you don't need to cite these directly or crib from them literally, they are there to help
you understand why i want an AI agnostic, \"protocol\" based approach but with a named accountable human (not allowing AI to
be the named committer). even when AI does contribute its on a specific humans authority and its the human who is
accountable. i don't want that blurred with trailers"

**Applied as:** the spike's G4 no longer treats "no attribution against disclosure" as a tension to name; it is settled
as a principle the covenant states: the bar for a contribution is actor agnostic at the code level; a named human is the
contributor and owns what they merge; AI use is neither required to be disclosed nor forbidden, and never an excuse; the
rules (narrow scopes, review against the scope, blast radius, readable history) are what is enforced; no AI trailer, so
the question is accountability of the committer, not AI or not. The readout places the other projects' disclosure norms
against this principle (what each tries to secure and whether the protocol approach secures it another way), and drafts
the covenant's accountability clause in those terms for him to sign off. The two papers are read by the unit for the
reasoning behind a protocol-based, actor-agnostic approach with a named accountable human; the readout does not cite or
quote them unless he later asks. He signs off the guideline himself.

## The stance on tools (2026-11-14, 21:10)

**Supervisor, verbatim:** "we don't have to use the phrase \"AI native\". but my point is really that we're a new project that came into existence after
abundant coding agents that produce high quality code when exercised under expert human direction. we're not litigating AI
not AI because at this point that's a bit like saying you used an IDE. stealing someone elses code bypassing it through an LLM
to get around a license is still not OKAY, but refusing to use LLMs because they broadly leaned from code published on the
internet would be unecessarily tying the developers hands behind their back. do you see my point? so our contributor guide
takes LLMs and LLMs based IDEs (like claude code, Codex, Devin, Cursor, etc) as a given part of the modern coding landscape;
asserts that you can (and should in some cases) document which tools you are using but that does not belong in the git
history as the contributor because it blurs accountability. noting that it successful repo governance will be as robust to
what models the contributor uses as it is to what IDE they use."

**Applied as:** the readout's last named tension (what "AI native" commits the project to) is dissolved; the phrase is
not required. The guide's stance, for the readout to draft: coding agents and agent-based editors (Claude Code, Codex,
Devin, Cursor and their like) are a given part of the landscape, as an editor is; which tools were used can be
documented, and in some cases should be, in the places made for it (a pull request's description, a work package's
record), never as the contributor in the git history, because that blurs accountability; laundering someone else's code
through a model to escape its licence is not acceptable, and that is a licence rule, not a model rule; refusing models
because they learned from published code is not asked of anyone; the governance is as robust to the contributor's
choice of model as to their choice of editor. The readout states where tool documentation belongs and drafts that
clause with the accountability clause.

## His wording for the clauses (2026-11-14, 03:05), on the drafts in the readout

**Supervisor, verbatim:** "No tool is a contributor, so commits should not carry a trailer or line naming a tool as author.

Tool use documentation gets coupled with other tool use documentation. this is a matter of how the facts are organized.
humans make commits, humans use tools. AI use goes where relevant with tools used not committers"

**Applied as:** the accountability clause's last sentence takes his words ("No tool is a contributor, so commits should
not carry a trailer or line naming a tool as author."). The tools clause is reorganised around his rule of how the
facts are kept: humans make commits and humans use tools, so the commit history names people, and the use of AI tools
is recorded where tool use is recorded, beside the editor, the build tools and the environment, in the "tools used"
part of a pull request's description or a work package's record, never in the committer or author fields. The shape
(A, B or C) is still his open call.

## The covenant's shape (2026-11-14, 17:20 EST; after the three shapes were shown as a contributor meets them)

**Supervisor, verbatim:** "A"

**Applied as:** Option A. `CODE_OF_CONDUCT.md` is Contributor Covenant 3.0 unaltered, with its attribution line and the
reporting contact filled in (him, until there are other maintainers); `CONTRIBUTING.md` opens with the two clauses
("Who owns a change", "Tools") in the wording he gave on 03:05 (order) and then states the process (scopes, review
against the scope, blast radius, readable history, candidates on `dev`, releases from `main` by the maintainer). The
three wording points of the readout remain his (which cases "should" document tools; whether no agent opens or merges
a change without a named person; whether "as an editor is" stays) and are put to him one at a time before the text is
written. Placement: with WP47's `CONTRIBUTING.md` in v0.1 unless he says otherwise. The covenant's verification cases
(no attribution line in any commit; a scope, a review and a decisions record per package; a person's name on every
commit) go to WP48's list. He signs off the final text.

## Wording point 1 of 3, "in some cases should" (2026-11-14, 17:25 EST; popup)

**Supervisor, verbatim:** "When it helps a reviewer"

**Applied as:** the tools clause reads "You may document which tools you used, and should when it helps a reviewer
reproduce or check the work."

## Wording point 2 of 3, agents acting on their own (2026-11-14, 17:30 EST; popup)

**Supervisor, verbatim:** "state it. though i want to be clear that this is not an injunction against AI coding its that the AI
is not the comitter the human on whose authority they commit is."

**Applied as:** the sentence is stated in his terms, not as a stop on AI coding: "A tool may write code, open a draft
or run a check, but it is never the committer: every act in this repository is done on the authority of a named
person, and that person is the one who answers for it." Placed in the accountability clause after "No tool is a
contributor, so commits should not carry a trailer or line naming a tool as author."

## Wording point 3 of 3, the editor analogy (2026-11-14, 17:35 EST; popup)

**Supervisor, verbatim:** "name IDEs, smooth the language. its not intended as an attack its simply a clarifcation and a heuristic. the AI has become
part of the Integrated Development Environement in practice. Developer (not IDEs) are responsible for what they produce,
commit, review, merge etc. i am comfortable with you doing some word smithing but my intents should be clear here. if they
are not, ask me clarifying questions"

**Applied as:** the analogy stays, names the integrated development environment, and is written as a heuristic: AI has
in practice become part of the development environment, and developers, not their environments, are responsible for
what they produce, commit, review and merge. The two clauses are assembled below with all three points and his
wording of 03:05 (order), for his sign-off; the text lands in `CONTRIBUTING.md` by WP47's unit only after that.

## The two clauses, assembled for his sign-off

**Who owns a change.**

> Every change merged here has a named human contributor: the person who submits it, who owns it. To own a change is
> to be able to explain it, to have checked it against its scope, and to answer for it afterwards. The bar a change
> must meet does not depend on what produced it: the same scope, the same review, the same blast radius, the same
> readable history. You are not asked whether or how you used AI, and "a tool wrote it" is never an answer to a
> question about the change. No tool is a contributor, so commits should not carry a trailer or line naming a tool as
> author. A tool may write code, open a draft or run a check, but it is never the committer: every act in this
> repository is done on the authority of a named person, and that person is the one who answers for it.

**Tools.**

> Humans make commits, and humans use tools. The commit history names people. Coding agents and agent-based editors
> (Claude Code, Codex, Devin, Cursor and their like) have in practice become part of the integrated development
> environment, and this project treats them so: nobody is asked to avoid them or the models behind them, and a
> developer, not their environment, is responsible for what they produce, commit, review and merge. The use of AI
> tools is documented where tool use is documented, together with the editor, the build tools and the environment:
> in the "tools used" part of the pull request's description or of the work package's record, and never as the
> committer or author. You may document which tools you used, and should when it helps a reviewer reproduce or check
> the work. None of this is a blanket approval of what a tool produces, because the rules of this work do not depend on
> who or what did the writing: rewriting someone else's code to escape its licence is a violation whether it is done by
> hand or through a model, and the person who commits it answers for it, as for every other question of ethics here.
> This project's checks are written to hold whichever model or editor you use.

## The licence sentence as the limit (2026-11-14, 17:45 EST), on the assembled clauses

**Supervisor, verbatim:** "we use the comment about using AI to launder code around a license as explicitly unacceptable as a point about AI coding is
not blanket approved either. the human is responsible for ethical behavior"

**Applied as:** the tools clause's licence sentence now carries the point it makes: "None of this is a blanket approval
of what a tool produces: putting someone else's code through a model to escape its licence is a licence violation
exactly as copying it would be, and the person who commits it answers for it, as for every other question of ethics
in this work." The assembled text above is updated in place.

## The rule is actor agnostic (2026-11-14, 17:50 EST), on the licence sentence

**Supervisor, verbatim:** "rewriting someones code by hand to get around a license is unethical without AI too. you see what i am getting at?"

**Applied as:** yes: the ethics do not depend on the actor, which is the same principle as the bar on the code. The
sentence no longer singles out the model: "the rules of this work do not depend on who or what did the writing:
rewriting someone else's code to escape its licence is a violation whether it is done by hand or through a model, and
the person who commits it answers for it, as for every other question of ethics here." Updated in the assembled text.

## Issues as scopes of work (2026-11-14, 18:05 EST), on the CONTRIBUTING draft

**Supervisor, verbatim:** "i think we need to tie this more directly to the use of Issues. issues should be scopes of work, they do not themselves
specify the approach to delivering on that work as that belongs to the person doing the work. PRs merge into dev and close
issues they resolve, merges into main are releases. i think the work i did previously on scoping and reviewing work needs
to be integrated into the guidance but let's be careful not to add more detail than is actually needed to author issues and
to evaluate and merge code. its probably worth noting that issues (as scopes of work are not automatically accepted or
prioritized), a candidate scope of work should be a draft issue and and draft issue should become an issue when its
approved"

**Applied as:** the draft's "How a change moves" is rewritten around issues: an issue is a scope of work (what is
delivered, what is not, what good enough means, and the open decisions) and not the approach, which belongs to whoever
does the work; a candidate scope is a draft issue and becomes an issue when the maintainer approves it, so an issue is
neither automatically accepted nor prioritised by being filed; a pull request delivers against its issue, merges into
`dev` and closes the issues it resolves, reviewed item by item against the scope with the evidence named; merges into
`main` are releases. His scoping and acceptance practice (the scope's goals, non-goals and definition of good enough; the
review against the scope with evidence; the recorded acceptance) is folded in at the depth needed to write an issue and
to evaluate and merge code, and no deeper.

## Admissibility of an issue (2026-11-14, 18:15 EST), on the CONTRIBUTING draft

**Supervisor, verbatim:** "issues themselves have admissibility conditions which we're enforcing since they need to have bounded scopes, sane blast
radiuses, and definitions of good and good enough"

**Applied as:** the draft states the admissibility conditions a draft issue must meet before it can become an issue,
and that they are enforced: a bounded scope (what is delivered and what is not), a sane blast radius (the files and
surfaces it may touch, small enough to review), and definitions of good (what the work aims at) and good enough (the
items a reviewer checks). A draft that lacks one is returned, not approved. The issue template asks for each.

## Conformance and fitness (2026-11-14, 18:40 EST), on the CONTRIBUTING draft

**Supervisor, verbatim:** "we also need to clearly separate verifiable conformance from validated fitness. have you accounted for that in your
draft?"

**Applied as (pending his word on the text):** not accounted for in the draft as it stood; the review paragraph mixed
the two in one list. The draft is to separate them: verification of conformance (does the change meet what the scope
and the repository's checks state: tests, lint, format, lock, the checkers, CI; machine-run, pass or fail, and what a
tool may run) from validation of fitness (does the change do what the issue intends, read as intended, render right;
a judgement a named reviewer makes and signs). The issue's good-enough items are written so each is one or the other;
the review reports both; a pull request merges only when conformance passes and a named person has validated fitness;
no check stands in for that judgement. The four thinner points of the validation of 18:25 (amendments; done is good
enough plus no open gap with the three dispositions; agent's defaults; merged by a maintainer who is not the author)
are drafted with it.

**Supervisor, verbatim (18:50 EST):** "apply all of them, then i will review the md doc and provide feedback"

**Applied as:** the conformance and fitness split and the four sentences from the skills check are in the draft; the
file goes to him for review.

## Code owners, not maintainers (2026-11-14, 19:00 EST), on the CONTRIBUTING draft

**Supervisor, verbatim:** "pretty good. though i want "codeowners" in place of maintainers. that way its a permissioned set
and the fact that i am the only member at present doesn't force a change to these markdown files if we add other
codeowners in the future"

**Applied as:** every "maintainer" in the draft becomes "a code owner" or "code owners", the permissioned set named in
`.github/CODEOWNERS`; the closing paragraph says that file is the record of who may approve, merge and release, and
that adding one changes that file and nothing on the page. The page WP47 writes keeps its path `docs/maintainers.md`
until WP47's unit renames it with the same rule (a note to PM16); the word on this page is code owner throughout.

## Enforcement (2026-11-14, 19:10 EST), on the CONTRIBUTING draft

**Supervisor, verbatim:** "we also may need some scripts and some github actions using the github cli and triggering conditions to enforce some of
what we just asserted"

**Applied as:** the assertions of the page that are conformance (checkable by machine) get a check each, with its
trigger, as verification cases in WP48's readout and built by WP47 or a follow-on package as he places them; the
assertions that are fitness (a code owner's judgement) get no script, only the record of who judged. The candidate
list, for his placement: (1) an issue's admissibility, on issue opened or edited: the template's fields (scope and
non-goals, blast radius, good, good enough) present and non-empty, else a comment naming the gap and a `draft` label
kept; (2) the draft gate: only a code owner removes the `draft` label (an action reverts any other removal); (3) a pull
request names the issue it resolves ("closes #n") or carries the small-fix label, on pull request opened or edited;
(4) the pull request description's fields (what changed, what backs it, tests, tools used) filled, same trigger;
(5) the merge into `dev` by a code owner who is not the author: branch protection (review from code owners, no
self-approval) plus a check on the merge event; (6) no commit message names a tool as author (exists, `test.yml`);
(7) releases only from `main` by tag through the release workflow with the environment's code-owner approval
(exists in WP47's `release.yml`); (8) the review record exists for each merged pull request (a file or a comment
naming conformance results and the fitness judgement by name), on merge. Each as a verification case: requirement,
method, evidence, verdict.

## Tooling as a reference, dependencies tracked elsewhere (2026-11-14, 19:30 EST), on the CONTRIBUTING draft

**Supervisor, verbatim:** "i am curious about tooling, practically i don't want to get stuck at 3.12 and i don't want to have to update a governance
doc when dependencies move. maybe we should make this a reference and track our dependencies elsewhere. dependency tracking
is also important for the supply chain aspect of security"

**Applied as:** the draft's closing section "Tooling in one line" (which named Python 3.12) becomes "Tooling and
dependencies": the page names no version and refers to where each is tracked (`.python-version`, `pyproject.toml`,
`uv.lock` with hashes), says CI installs from the lock only and fails on drift, that dependency updates arrive as pull
requests from the update bot (WP47's Dependabot configuration) and are reviewed like any change, that actions are
pinned to commits, and that a release ships with a software bill of materials (WP48's check 2; WP47 builds it if he
places it in v0.1). The supply-chain assertions become verification cases for WP48's list: lock matches declaration;
install from lock only; every action pinned; SBOM present on the release.

**Supervisor, verbatim (19:45 EST), on the tooling section:** ""This page names no version." this statement is llm-ish. you
don;t have to say you don't name something you don't name. you have the direct links to the file paths that do name, so
they can change without this document changing"

**Applied as:** the sentence is gone; the section opens on the three files as links, with "those files change, this page
does not", and the closing meta-sentence about the supply chain is cut too.

**Supervisor, verbatim (19:50 EST), on the page's release sentence:** "sbom in v0.1"

**Applied as:** the page's "A release ships with a software bill of materials" holds for v0.1; WP47 Amendment 2 builds it.


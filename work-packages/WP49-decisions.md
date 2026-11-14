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


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


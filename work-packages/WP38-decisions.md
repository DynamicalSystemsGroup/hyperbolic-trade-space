# WP38 decisions: the residual pass (patterns that read as machine-written)

Supervisor: Michael Zargham (`mzargham`). A review near the end of the 0.1 candidate, over every prose surface,
with a reader's lens the earlier loops did not apply.

## The supervisor's direction (2026-11-13, verbatim)

> as we get close to the end there is another kind of a review i want. this review eliminates LLM residuals or
> patterns that feel like LLM. often this is unecessary metanarration, parentheticals or out of place caveats or
> spurious details that either dont belong in that location or dont belong at all. llms love details so much so
> they inject them where they dont belong

## The assistant's reading

A pass, not a rewrite: fresh readers go over each prose surface (the paper's body and appendices, the docs pages,
the README, the root page, the history page, the glossary's long forms) with one lens, where does this read as
machine-written, and flag each instance with its sentence and its kind: metanarration (a sentence that announces
or summarizes instead of saying); a parenthetical that carries a second thought; a caveat placed where no claim
is made, or repeated; a detail that belongs elsewhere or nowhere (precision, an aside, a list of three where one
word does); a hedge where the record is definite; signposting that the structure already gives; a restatement.
Each flag gets a disposition, cut, move or keep with a reason, and the cuts land as negative edits under the
ledger and the claims register (a moved claim keeps its backing; a cut states what the sentence no longer did);
a second fresh reader confirms the surface reads clean. It runs once the surfaces are stable, after WP33, WP35,
WP36 and WP37 land and before the final reader round, so that round reads the cleaner text. The five entry
surfaces are read in it too, their changes listed for the supervisor as always. The scope comes to the assistant
in the usual form; Sonnet readers and implementer, Haiku for counts.

> you can work in parallel to build the review machinery for this review

**The assistant's reading.** The machinery is built now, in parallel with the running packages, and the pass runs
when the surfaces are stable. The machinery: the lens as a written reader's brief with the kinds of residual and
an example of each from this repository's own earlier drafts where one exists; a flag table format (surface,
location, the sentence, kind, proposed disposition, reason); a script that lists the prose surfaces and their
word counts so every surface is assigned and none missed; a checker for the mechanical patterns that can be
searched (the metanarrative openers, the hedges, the stock intensifiers, parenthetical density per paragraph) as a
report, never an automatic edit, with its baseline; the ledger and claims-register hooks the cuts already use; and
the second reader's confirmation form. A scope in the usual form names them as deliverables.

> the use of this review machinery becomes part of the final deliverable but i didn't want to do premature copy
> editing so i left this to be applied in the late stage reviews since it shouldn't really cover anything but style
> improvements and minor copy editing level decisions.

**The assistant's reading.** Two consequences. The machinery and its use are part of the 0.1 package: the brief,
the inventory, the checker with its baseline and the pass's records ship with the deliverable and are named in
the reviewer's guide, so a later reader can re-run the pass. And the pass's reach is copy-editing: style and
minor wording decisions on stable text, never a claim, a number, a structure or a placement; anything a reader
flags that is more than that goes to the owning package or to the supervisor's list, not into the pass. It
runs late, after the content loops, for exactly the reason he gives.

> LLMs also construct overly complex gramatical structures that are hard for human readers to parse.

**The assistant's reading.** A ninth kind for the brief: sentence structure a human reader cannot parse at one
pass, long sentences with stacked subordinate clauses, several ideas joined by semicolons or colons, a subject
far from its verb, nested qualifications. The disposition is to split or reorder, never to add words; the checker
can report sentence length and clause depth per surface as a signal, the reader decides.

> another pattern to look out for is jargon use. within any particular document we should use plain language
> where it suffice and terms of art where needed to streamline or reference properly. define clearly on first
> use. this holds for acronyms as especially.

**The assistant's reading.** A tenth kind for the brief, with a rule attached: within each document, plain language
where it suffices and a term of art only where it streamlines or references properly; every term of art and every
acronym defined clearly at its first use in that document (the glossary is the one source of definitions, and the
first use points at it or carries the definition). The reader flags a term used before its definition, an
acronym never expanded in that document, and jargon doing no work; the disposition is replace with the plain
word, or define at first use, never a parenthetical gloss at every later use. The checker can list acronyms and
glossary terms per document with the line of first use and whether a definition precedes it; the vocabulary
check already covers the project's own terms.

## The supervisor, on Appendix G.2 (verbatim)

> one more observation: G.2 two is an important sanity check but reads like LLM residual in the paper. my intuition
> is we keep it in its yaml form for our own checking but we may want to drop it from the supporting materials.
> or maybe we just drop the "verdict" column? from the view presented in the supporting materials? in practice i
> like the rigor of this check but as written if feel like it undermines rather than supports. i want to keep
> traceability records and assessments without giving the feeling that no human validated the citations.
> ultimately we humans have to be happy with the way the cited material was used, an LLM cannot read everything
> and has fundamental limits in terms of whether it can assess how we interpreted and reflected the cited claims
> into the context of this paper.

**The assistant's reading and call.** The record stays and the view changes. `paper/reading_pass.yaml` remains the
traceability record of the reading pass (every cited sentence, the source read, what it says, the status), tested
as now, and the claims rows that cite its lines stay. Appendix G.2's rendered table of sentence, verdict and why
goes; in its place G.2 states the check in a few sentences: what was done (each citing sentence read against the
source named, the sentence kept, reworded or cut), its counts (sentences, sources, rewordings, cuts), where the
record lives (`paper/reading_pass.yaml` in the repository), and whose the readings are: the authors', who
validate the record before release. That last sentence is a claim about the supervisor's own act, so it enters
the paper only when he has done it: the reading pass becomes an item of his close read before release, listed
with the entry surfaces, and the sentence is worded to what he has done. No machine verdict is rendered on any
surface. A unit through the paper notebook's queue: the G.2 generator, a test that G.2 renders the summary and no
verdict column, the register rows and the ledger (a cut of the table's words), the review list.

> the G.2 we present should be sufficient for a reader to check for themselves and decide that we've reflected
> the result. its less that an LLM checked and more that we are saying what we took from where and the reader is
> given enough information to dereference it themselves and form their own opinion if they want to

**The assistant's reading, revising the call above.** G.2 keeps a table, with different columns: what we say (the
citing sentence or its claim), the source (the reference), and where in it (the locator the record holds: the
abstract, a section, a page, a figure, a URL), one row per citing sentence, so a reader can dereference each claim
and judge the reflection for themselves. The machine's columns (verdict, why, status) and the summary counts go
from the view; the record keeps them. The lead sentence says what the table is: what the paper took from where,
for the reader to check. The reading pass's validation by the authors before release stands as recorded.

## Approval of the scope (2026-11-13, 07:30; the assistant, under the supervisor's mandate; scope at 652c27d)

**Assistant, verbatim:** "WP38-scope-of-work.md at 652c27d is approved as written: the five goals, the non-goals
(copy-editing only; the checker reports and never edits; the pass waits for stable surfaces), deliverables D-0 to
D-7, the requirements and good enough, the agent models and the defaults as one item. Build D-1, D-3 and D-4 now;
the pass runs on my word once the surfaces are stable."

## The pass begins (2026-11-14, 14:20; the assistant's word; surfaces at 995075b)

**Assistant, verbatim:** "The surfaces are stable: WP39's decision section and its fixes, WP40's thinning with its last
notebook step, the WP35 and WP36 units and the history page are all on dev at 995075b and the stage is rebuilt there.
The WP38 pass runs now per the scope and docs/superpowers/notes/residual-review.md: 29 reader slots over the prose
surfaces, the flag table and the second reader's confirmation, copy-editing only, the checker before and after, one
landing unit per surface group through the owning package's ledger and the paper queue. The abstract is read and
flagged like every surface and changed by no one but the supervisor; the five entry surfaces' changes are listed for
his close read."

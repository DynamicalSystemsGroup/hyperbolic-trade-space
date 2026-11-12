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

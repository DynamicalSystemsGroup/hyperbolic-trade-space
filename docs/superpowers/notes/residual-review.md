# Note: the residual review (where prose reads as machine-written)

The reader's brief for WP38 (`work-packages/WP38-scope-of-work.md`, `WP38-decisions.md`). A late pass over every
prose surface, run once the surfaces are stable, before the final reader round. The supervisor's direction: remove
the patterns that read as machine-written, "unecessary metanarration, parentheticals or out of place caveats or
spurious details that either dont belong in that location or dont belong at all", and sentences "hard for human
readers to parse"; plain language where it suffices, a term of art defined at its first use, acronyms above all.

## The lens

One question, asked of each sentence: **where does this read as machine-written?** Not whether it is true (the
claims register and the lemma chain answer that), not whether it is the right content (the content loops did that),
but whether a human author would have written it, in that place, in those words.

## The reach

The pass is copy-editing: style and minor wording on stable text. It never changes a claim, a number, a figure, a
structure or a placement. A flag that would need any of those is **routed**: to the package that owns the surface,
or to the supervisor's list (`work-packages/supervisor-review-list.md`), and the sentence is left as it is. A cut is
allowed only when the sentence no longer does anything the reader needs, and the cut says what it no longer did.
The five entry surfaces (`site/index.html`, `README.md`, the paper's abstract, `site/history.html`, `docs/index.md`)
are read in the pass like the rest; their changes are listed in the supervisor review list ("Entry surfaces") with
reason and commit.

## The ten kinds

Each kind has a definition, the question that finds it, the dispositions allowed, and an example from this
repository's own earlier drafts where one survives (found with `git log -S`; under 25 words; the commit introduced
or carried the text). A kind with no example says so. A pattern in the examples is a shape to look for, not a
verdict: the reader judges the sentence in its place.

### Kind 1. Metanarration

A sentence that announces or summarizes the text instead of saying something. Ask: delete it, does the reader lose
a fact? Disposition: cut, or fold the one fact it carries into the sentence that needs it.
Example (`9a715f3`): "This section is future work with no results, and it stops short of selecting a design, which
falls to experts."

### Kind 2. A parenthetical that carries a second thought

A parenthesis that adds a separate idea, qualification or aside, rather than an abbreviation, a symbol or a
reference. Ask: is the parenthetical a sentence in disguise? Disposition: cut; or promote to its own sentence if the
idea is needed; or move to where it belongs. The checker counts parentheticals of eight words or more.
Example: none survives in the history; the first reading supplies them.

### Kind 3. A caveat where no claim is made or repeated

A qualification attached to nothing, or the same qualification stated a second time. Ask: which claim does this
qualify, and is it already qualified where the claim is made? Disposition: cut; if the caveat is needed it belongs
at the claim, once. A caveat is never added to fix a flag.
Example: none survives in the history.

### Kind 4. A detail that belongs elsewhere or nowhere

Spurious precision, an aside, a list of three where one word does, a fact true but not needed here. Ask: does the
argument of this paragraph need it? Disposition: cut; or move to the surface where it earns its place (a move keeps
the backing, and a move across surfaces is routed, not done: kind 4 is the one most likely to leave the pass's reach).
Shape seen in an earlier draft (`4867478`): "four thresholds (peak slew power, pointing error, control effort,
launch cost) and two limits (unit cost, fleet cost)".

### Kind 5. A hedge where the record is definite

"May", "perhaps", "somewhat", "generally" over something the register, a test or a lemma states flatly. Ask: what
does the record say? Disposition: state it as the record does; if the record is itself hedged, keep and route
nothing. Example: none survives in the history.

### Kind 6. Signposting the structure already gives

A pointer to what the heading, the numbering or the layout already shows: "the comparison above", "see below", a
sentence that lists the parts about to come. Ask: would the reader find it without the pointer? Disposition: cut.
Example (`38b7f0e`): "two at the one-term temperature (the comparison above) and a seed check at three terms".

### Kind 7. Restatement

A sentence or clause that says again what the previous one said, in other words. Ask: does the second add a fact?
Disposition: cut the weaker of the two. The checker reports adjacent sentences that share most of their content
words. Example: none survives in the history.

### Kind 8. Stock intensifiers

"Very", "crucial", "robust" (outside its technical sense), "seamless", "importantly", "indeed", "simply", "carefully".
Words that raise the temperature without adding a fact. Ask: what does the sentence lose without the word?
Disposition: cut the word. Example: none survives in the history.

### Kind 9. Grammatical complexity

Sentence structure a human cannot parse in one pass: a long sentence with stacked subordinate clauses; several ideas
joined by semicolons or colons; a subject far from its verb; qualifications nested inside qualifications. Ask: can a
reader at a normal pace say what the sentence says after one reading? Disposition: **split or reorder, never add
words.** The checker reports sentences over 35 words, sentences with two or more semicolons or colons, and sentences
with four or more subordinating words, as signals only.
Example (`8c156ab`): "A posynomial surface fitted to the table gives it a coordinate system; the surface models the
table and is not the Pareto boundary."

### Kind 10. Jargon

Within each document: plain language where it suffices, and a term of art only where it streamlines or references
properly. Every term of art and every acronym is defined clearly at its first use in that document. The glossary
(`glossary.yaml`) stays the one source of definitions: the first use points at it or carries the definition. Readers
flag (a) a term used before its definition, (b) an acronym never expanded in that document, (c) jargon doing no work.
Disposition: **the plain word, or a definition at first use; never a gloss repeated at later uses.** The checker lists,
per document, every acronym and glossary term with the place of its first use and whether a definition or glossary
link is in that paragraph. The project's own terms and their variants stay under `scripts/check_vocabulary.py`.
Example (`b7df6be`, the vocabulary reading): "The cheap diagnostic is the sign of the pulled-back exponent below."

## How a reader works

1. Open the surface as the reader sees it (the assigned view in the inventory), not the source. Read it once at
   reading pace and mark where it feels machine-written, then go back through the ten kinds.
2. Flag each instance as one row of the flag table. Do not edit. One flag, one sentence; if a paragraph has the
   same problem three times, three rows.
3. Run `uv run python scripts/check_residuals.py` for the surface and look at its signals; a signal is a place to
   look, not a flag. Do not flag what the checker found without reading the sentence.
4. Mark a flag **routed** when the disposition would be a claim, a number, a figure, a structure or a placement.

### The flag table

One table per reader slot, `work-packages/WP38-flags/<slot>.md`. Columns:

| Surface | Location | Sentence | Kind | Disposition | Reason |
|---|---|---|---|---|---|
| `paper/discussion` | cell 99 | the sentence, in full | 1 to 10 | cut / move / keep / split / define / routed | one line: what it no longer does, or why it stays |

Dispositions: **cut** (delete); **move** (to a named place; backing kept; a cross-surface move is routed); **keep**
(flagged, read, left, with the reason); **split** (a sentence divided or reordered, no word added); **define** (a
definition at first use, or the plain word, for kind 10); **routed** (to the owning package or the supervisor's list,
named). Location is the inventory's first-location form (`cell N`, `line N`) plus the sentence's own words.

### The second reader's confirmation form

A second fresh reader, who has not seen the first table, reads the **landed** text of the surface in its rendered
view and fills one form per surface, `work-packages/WP38-confirmations/<slot>.md`:

| Surface | Reader | Rendered view and head | Reads clean | Remaining flags (kind, sentence) | Cuts that lost something |
|---|---|---|---|---|---|
| `paper/discussion` | a name | the page opened, the commit | yes / no | none, or rows as in the flag table | none, or the sentence and what it lost |

A "no" or a lost fact sends the surface back for one more round; after that the remainder is listed for the
supervisor.

## The machinery

- `scripts/prose_surfaces.py` lists every prose surface with its word count, rendered view and reader slot; every
  surface is assigned and none missed. (`uv run python scripts/prose_surfaces.py`; `--json`.)
- `scripts/check_residuals.py` reports the mechanical patterns per surface and the first uses of acronyms and
  glossary terms per document, against a baseline (`scripts/residuals_baseline.json`, generated at a recorded head).
  It edits nothing. (`--compare scripts/residuals_baseline.json` lists the counts that rose; `--strict` exits 1.)
- `tests/test_residuals.py` plants each pattern and checks the report's form.

## The pass

1. **Inventory and baseline.** Run the inventory and the checker at the head the pass starts from; keep the report in
   the review.
2. **First reading.** One fresh Sonnet reader per reader slot, rendered pages only (the built site for the paper and
   docs, the root and history pages as served, the README as GitHub renders it). Each returns a flag table; no
   edits.
3. **Triage and landing.** One implementer (Sonnet) takes the tables, decides each disposition, and lands the cuts
   as negative edits, one unit per surface and one push each. Every cut goes through the ledger
   (`paper/length_ledger.toml`, down only) and the claims register (a moved claim keeps its backing; a cut states
   what the sentence no longer did, in the decision record). Routed flags go to their owners. Entry-surface changes
   are listed for the supervisor.
4. **Second reading.** A second fresh reader per surface fills the confirmation form on the rendered result.
5. **Close.** `uv run python scripts/check_residuals.py --compare scripts/residuals_baseline.json --strict`: no
   count rises; the generated paper outputs and the claims tests unchanged; the flag tables, confirmations and the
   before-and-after counts are in `WP38-review.md` and named in the reviewer's guide.

A surface whose confirmation lists remaining flags gets one more round; after that the remainder is listed for the
supervisor.

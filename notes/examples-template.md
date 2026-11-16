# The example page: one arc in five parts

A note for authors of the docsite's example pages (`docs/examples.md`, `docs/examples/*.md`). The
supervisor's direction (2026-11-16, `work-packages/WP63-decisions.md`): "you can fit any data" but why
did you do that and what do the results mean. An example page shows the method at work and gives a
cold reader the intuition for it: where the rows came from, what each column means, what the fit was
asked, the fit itself, and what its answer means in the field's terms. Rigor and interpretability
together; as concise as the arc allows.

The headings are the page's own words, not the part names below. No sentence has the page, a
section, a figure's placement or the reader as its subject (`CLAUDE.md`, "No metanarration").
Every number keeps its `<!-- register: ... -->` comment and its results file.

## 1. Where the rows come from (one paragraph, 60 to 100 words)

- **Must:** the research programme or engineering application that produced the data, in the
  field's words; who compiled it and how (the cited paper, `[@key]`); what one row is (a device, a
  species, a plot-year, a design); the release, its DOI and licence; the command that fetches and
  refits.
- **Must not:** the method's vocabulary, any result, a history of the field.
- **Source:** the manifest's paper and the dataset's landing page; a fact found in neither is not
  written.

## 2. The attributes (a dictionary, then one or two sentences)

- **Must:** for each attribute used: its meaning, unit, source column, and orientation (+1 larger is
  better, -1 a cost inverted, with the reason); the covariates and any attribute set aside, with why;
  the rows kept, of how many, and the rule that dropped the rest.
- **Form:** a ```` ```text ```` block laid out as a table (the site forbids Markdown tables, and a
  list of five attributes costs a hundred words of the page's budget); lines within the 72-character
  code column; no line starts with `|`.
- **Must not:** conditioning choices beyond the orientation (those are the analysis).

## 3. What the fit is asked (one short paragraph, 40 to 80 words)

- **Must:** the trade-off the domain expects, named in its scientific or engineering terms with its
  citation (a physical limit, a life-history continuum, an allocation index, a stakeholder's needs),
  posed as a question the fit can answer either way: is the expected pair in the contending set, and
  is its association near the frontier negative?
- **Must not:** the answer, or any word that presumes it ("confirms", "the dilemma shows").

## 4. The fit (as long as the code and the figures need)

- **Must:** the conditioning rule (scaler, shift, why); the fit temperature and how it was chosen;
  K = 1, then K = 2 when the data carry it; the runnable block and directly below it the figure it
  makes, with alt text and a numbered caption; the variants a reader needs to judge the reading
  (the conditioning ladder, the extremes, a derived metric); the check on one's own dataset.
- **Must not:** the field's interpretation (part 5); a sentence that restates a number already on the
  page.

## 5. What the fit says, and what the example cannot show (60 to 120 words, then two or three sentences)

- **Must:** the answer to part 3's question in the field's terms, each claim resting on a number shown
  in part 4; which part of the reading held across the variants and which moved; then, under its own
  heading, what the data cannot carry (a frontier of published or evolved rows is not a design
  limit; a confound; the subset kept).
- **Must not:** a new number, a claim part 4 does not back, a caveat added to soften a claim.

## Length

A dataset page runs 500 to 700 prose words (`tests/test_site.py` holds the page budgets and the
docsite's total, which binds first; code, the dictionary blocks, alt text and comments do not count).
Link a method term (the contending set, the fit temperature) to the glossary at its first use: it costs
no words, and cold readers stop at those terms. Cutting is preferred to adding: a sentence
that repeats a number, explains the method in general (the user guide does) or describes the page
goes.

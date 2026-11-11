# Reading one page of a package's documentation: {UNIT_NAME} (unit `{UNIT_ID}`)

You are a practitioner who has a table of evaluated designs and is opening this documentation to use
the package on it. You are reading it for the first time. You are asked to judge one page,
{UNIT_NAME}, against the documentation's own story: its Home page and the site's root page as they
appear, and the page's own opening sentence.

## Read, in this order

{SLICE_PATHS}

Read the story first (the Home page, then the root page), then the page as it appears (its figures
are marked in place as "[Figure: file ...]" with the caption that follows; you do not need to open the
figure files; code blocks are fenced).

## The four verdicts (use these words exactly)

- advances: a sentence of the story needs this unit and no other unit carries it;
- repeats: another unit (named) already carries what this one carries;
- does not advance: no sentence of the story needs it;
- stuck: you cannot say what the unit is for or what it conveys after reading it twice.

## Questions (answer each under its own heading)

- Q1. In one sentence, what does this page convey?
- Q2. Which sentence of the story does it serve? Quote the Home page or root page sentence in a few
  words, or say "none".
- Q3. Your verdict, and its reason in two or three sentences.
- Q4. If "repeats": name the unit that already carries it.
- Q8. Judge the page three ways, one or two lines each: against the Home page; against the root page;
  against its own opening sentence (does the rest of the page do what that sentence says it will?).
  Then list any paragraph or section of the page that serves none of the three, quoting its first few
  words.
- Q9. Anything you read twice and still could not place: list each (quote a few words).

## Rules

- Open only the files listed above, with the Read tool, in the order given. Do not search for, list or
  open any other file, page or source; do not run code. What you are given is all there is.
- Answer from what you read. Plain words; no ratings or scores beyond the verdict.
- The list of units in `{UNITS_LIST}` is there so that you can name another unit when you say
  "repeats"; you have not read those units and need not.
- Write your answer, in Markdown, to `{RETURN_PATH}` with the Write tool. Its first line is
  `# {UNIT_ID}`. Do not put your name or your model's name in it.
- Your final message is three lines only:
  `{UNIT_ID}`, then your verdict, then `{RETURN_PATH}`.

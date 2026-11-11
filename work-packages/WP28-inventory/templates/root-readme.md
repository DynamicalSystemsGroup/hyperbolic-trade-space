# Reading the front door of a package: {UNIT_NAME} (unit `{UNIT_ID}`)

You are a practitioner who has a table of evaluated designs and has just found this package. You
are reading its front door for the first time: the site's root page and the repository's README.
You are asked to judge the two together against the documentation's own story: its Home page, and
each page's own opening sentence.

## Read, in this order

{SLICE_PATHS}

Read the story first (the Home page, then the root page), then the root page again as its own unit
(its two figures are marked in place as "[Figure: file ...]" with the caption that follows; you do
not need to open the image files), then the README as it is in the repository (Markdown source).

## The four verdicts (use these words exactly)

- advances: a sentence of the story needs this unit and no other unit carries it;
- repeats: another unit (named) already carries what this one carries;
- does not advance: no sentence of the story needs it;
- stuck: you cannot say what the unit is for or what it conveys after reading it twice.

## Questions (answer each under its own heading)

- Q1. In one sentence each, what does the root page convey, and what does the README convey?
- Q2. Which sentence of the Home page does each serve? Quote it in a few words, or say "none".
- Q3. Your verdict for the root page and for the README, each with its reason in two or three
  sentences.
- Q4. If "repeats": name the unit that already carries it (the two may repeat each other, or the Home
  page).
- Q8. Judge each against the Home page and against its own opening sentence, one or two lines each.
  Then list any paragraph of either that serves neither, quoting its first few words.
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

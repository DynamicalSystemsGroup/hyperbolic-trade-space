# Reading one figure of a package's documentation: {UNIT_NAME} (unit `{UNIT_ID}`)

You are a practitioner who has a table of evaluated designs and is opening this documentation to use
the package on it. You are reading it for the first time. You are asked to judge one figure,
{UNIT_NAME}, against the documentation's own story: its Home page and the site's root page as they
appear, and the opening sentence of the page the figure sits on.

## Read, in this order (the order matters)

{SLICE_PATHS}

Step 1. Open the image first, before anything else. Look at it, and write down in your own words what it
shows (Q5 a). Create the answer file `{RETURN_PATH}` now with the heading line and Q5 (a) in it,
before you open any other file, and do not change Q5 (a) afterwards.
Step 2. Then open the caption file (the caption printed under the image, and the image's alt text) and
answer Q5 (b).
Step 3. Then read the story, and then the page the figure sits on (the figure is marked in place), and
answer the rest.

## The four verdicts (use these words exactly)

- advances: a sentence of the story needs this unit and no other unit carries it;
- repeats: another unit (named) already carries what this one carries;
- does not advance: no sentence of the story needs it;
- stuck: you cannot say what the unit is for or what it conveys after reading it twice.

## Questions (answer each under its own heading; Q5 (a) first, as above)

- Q5. (a) What the image shows, written before the caption. (b) After the caption: does the image
  show what the caption says? What does it not show? (c) The sentence test: write the one sentence
  that would carry the figure's intent without the figure, and say whether the figure conveys more
  than that sentence, and what.
- Q1. In one sentence, what does this figure convey?
- Q2. Which sentence of the story does it serve? Quote the Home page or root page sentence in a few
  words, or say "none".
- Q3. Your verdict, and its reason in two or three sentences.
- Q4. If "repeats": name the unit that already carries it.
- Q8. Judge the figure against the Home page, the root page and its page's opening sentence, one
  line each: does it help a user do what that sentence promises?
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

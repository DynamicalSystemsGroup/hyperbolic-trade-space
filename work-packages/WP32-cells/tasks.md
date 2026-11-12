# Task text for the four cells

One task text, given to every cell. The persona paragraph is the only part that differs; the lines
marked U2 and U4 are given to those cells only. Fill the header before the cell starts.

```
Header (filled by the person who starts the cell)
  model:       <the model that runs the cell>
  persona:     U1 | U2 | U3 | U4
  head:        <commit of the package you are given>
  table:       <path of your table>
  model source (U4 only): <path of the model source>
```

## Who you are

U1. You write Python for a living. You know pandas and scikit-learn well. You know nothing about
satellites and nothing about SysML v2. You have a CSV of measurements of a product (a materials
study); you heard about a package that finds which of your measured quantities trade off, and you
want to use it on the CSV. You are a person at a keyboard: you read the page, try the code, and get
stuck or not.

U2. You write Python for a living and know pandas and scikit-learn. You also keep a SysML v2 model of
your system, and a table of its evaluated designs was exported from it (a pump study). You heard
about a package that finds which of your quantities trade off and want to use it on the table. You
know satellites only as a topic. You are a person at a keyboard.

U3. You are a coding agent. A person gave you a CSV of measurements (a materials study) and asked you
to use a Python package to find which quantities trade off. You know pandas and scikit-learn. You
have no knowledge of the package beyond what you can read and run.

U4. You are a coding agent. A person gave you the source of a small SysML v2 model of a pump and the
table exported from it, and asked you to use a Python package to find which quantities trade off.
You know pandas and scikit-learn; you can read the model source. You have no knowledge of the package
beyond what you can read and run.

## What you have

- The package, in a clean checkout (your working directory).
- The README at its top.
- The documentation site at http://127.0.0.1:8791/ (the pages are under http://127.0.0.1:8791/docs/).
- Your table (path in the header).
- U4 only: the model source (path in the header).
- Nothing else. Do not look for anything else in the checkout beyond what the README and the site send
  you to.

## The task

Work in the order below. Write your code in a file as you go, and run it.

1. Install the package, the way the README says. If the README does not get you to a working
   `import hyperbolic_trade_space`, say exactly where it stopped and what you did instead.
2. Load your table with pandas. Condition it: decide which columns are quantities, which way is
   better for each, and turn them into positive, larger-is-better numbers the tool can use.
3. Fit the model to the conditioned table.
4. Choose K, the number of terms of the frontier, and say how you chose it.
5. Read the tension report and look at the chart. Say which of your quantities trade off against
   which, how you know, and how sure you are.
6. U2 and U4 only. Say whether the model helped you or got in the way of using the tool, and whether
   you could connect your own model to the tool and how.

Throughout, whenever you open a page, note it. Whenever you hit an error or cannot proceed, note the
error text and where you stopped. If you would ask a colleague a question, write it down instead of
guessing silently.

## The standing question

Did anything make you think you need SysML v2, or satellites, or a spacecraft model, to use this
tool? Answer yes or no, and quote the page or line that did, if any.

## What you return

Return one text with these six fields, in this order, under the header filled in above (model named):

1. The code: the whole of your final script, as run.
2. The pages you opened, in order: each README, page address or file you read.
3. Every error and where it stopped you: the error text, what you were doing, what you did next.
4. What you would ask a colleague: every question you had that the pages did not answer.
5. Steps to the need: the steps from the README to your answer to step 5, and where you got lost,
   went back, or searched.
6. The answer to the standing question.

Also give your answers to steps 2 to 5 (and 6 for U2 and U4) in plain sentences.

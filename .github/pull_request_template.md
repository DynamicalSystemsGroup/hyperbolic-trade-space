<!-- Target `dev`. A change to the paper targets `paper` and fills the Paper section at the end as well.
     Every other section is read by the pull request check on both kinds; none may be empty. -->

## Issue

<!-- `closes #n`, or leave this section with "small fix" and apply the small-fix label (a typo, a broken link). -->

## What changed

## What backs it

<!-- A test, a lemma step, a generated value, or a source. -->

## Tests

<!-- Which tests cover it, and the result of `uv run pytest`, `uv run ruff check .`, `uv run ruff format --check .`. -->

## Defaults

<!-- Details the scope did not settle, listed for the reviewer to approve as one item. Write "none" if there are none. -->

## Tools used

<!-- The editor, build tools and any AI tools; never as the committer or author. Write "none" if there are none. -->

## Paper

<!-- For a pull request into `paper` only (the check reads this section on that base; leave it empty otherwise):
     the section or figure changed; the residual check's result
     (`uv run python scripts/check_residuals.py --compare scripts/residuals_baseline.json --strict --views paper,appendix`);
     the build (`cd paper && uv run myst build --html`, exit code). The paper's approvers read it for the argument;
     the paper workflow runs the build, the tests, the residuals and the keys once the merge lands on `paper`. -->

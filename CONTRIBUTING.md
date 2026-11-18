# Contributing to tradespace

## Start contributing

Search [existing issues](https://github.com/DynamicalSystemsGroup/tradespace/issues) before reporting
a bug. Include your package version, a minimal example, and expected and actual behavior.
Report vulnerabilities privately through [SECURITY.md](SECURITY.md).

For a small fix, open a pull request without an issue and ask a maintainer to apply the `small-fix`
label. For a new method, feature or public API change, open an issue and wait for a code owner to
approve the scope before implementing it.

### Set up a development checkout

Install [uv](https://docs.astral.sh/uv/getting-started/installation/) and
[just](https://just.systems/man/en/packages.html). The package requires Python 3.12.
Fork the repository on GitHub, then clone your fork, replacing `YOUR-USERNAME`:

```bash
git clone https://github.com/YOUR-USERNAME/tradespace.git
cd tradespace
git remote add upstream https://github.com/DynamicalSystemsGroup/tradespace.git
git fetch upstream
git switch -c fix/short-description upstream/dev
just setup
```

### Check your change

Run the fast software tests and the style and dependency checks from the repository root:

```bash
just check
```

Run `just` to list commands. Each recipe calls uv and uses the committed lockfile.
`just setup` checks the lockfile before installing dependencies. Test and lint recipes use
`uv run --frozen` so they do not rewrite it; `just check` includes `uv lock --check`.

| Command | What it runs |
|---|---|
| `just setup` | `uv sync --locked` |
| `just check` | Lint, formatting and lock checks, then fast tests |
| `just lint` | `uv run --frozen ruff check .` |
| `just format` | `uv run --frozen ruff format .` |
| `just format-check` | `uv run --frozen ruff format --check .` |
| `just lock-check` | `uv lock --check` |
| `just test-fast` | Software tests excluding slow and paper tests |
| `just test` | The full software suite |
| `just docs-check` | Vocabulary and prose checks |

Pass pytest arguments after `just test` or `just test-fast` to select tests:

```bash
just test tests/test_coordinates.py -q
```

For documentation changes, run `just docs-check`.
Run the relevant slow tests for changes to numerical behavior, examples or site builds.
For paper tests, follow
[Contributing to the paper](#contributing-to-the-paper).

Open a pull request targeting `dev`. Describe the problem, your change and the checks you ran,
including their results. Changes to the paper target `paper`. The Tests workflow runs the Linux
fast, slow and documentation test groups on pull requests into `dev` and `main`.
Code owners run Windows checks by manual dispatch and review changes before merging.

Start in `src/tradespace/` for package code, `tests/` for tests, `docs/` for user documentation and
`examples/` for applications. `work-packages/` and `notes/` hold development records and research
guidance. You can try the package and report bugs without reading those records.

## Contribution policy

All contributors must follow the [code of conduct](CODE_OF_CONDUCT.md).
The project adopts the Contributor Covenant unaltered.

## Who owns a change

Every change merged here has a named human contributor: the person who submits it, who owns it. To own a change is to
be able to explain it, to have checked it against its scope, and to answer for it afterwards. The bar a change must
meet does not depend on what produced it: the same scope, the same review, the same blast radius, the same readable
history. You are not asked whether or how you used AI, and "a tool wrote it" is never an answer to a question about the
change. No tool is a contributor, so commits should not carry a trailer or line naming a tool as author. A tool may
write code, open a draft or run a check, but it is never the committer: every act in this repository is done on the
authority of a named person, and that person is the one who answers for it.

## Tools

Humans make commits, and humans use tools. The commit history names people. Coding agents and agent-based editors
(Claude Code, Codex, Devin, Cursor and their like) have in practice become part of the integrated development
environment, and this project treats them so: nobody is asked to avoid them or the models behind them, and a developer,
not their environment, is responsible for what they produce, commit, review and merge. The use of AI tools is
documented where tool use is documented, together with the editor, the build tools and the environment: in the "tools
used" part of the pull request's description or of the work package's record, and never as the committer or author.
You may document which tools you used, and should when it helps a reviewer reproduce or check the work. None of this
is a blanket approval of what a tool produces, because the rules of this work do not depend on who or what did the
writing: rewriting someone else's code to escape its licence is a violation whether it is done by hand or through a
model, and the person who commits it answers for it, as for every other question of ethics here. This project's checks
are written to hold whichever model or editor you use.

## How a change moves

**An issue is a scope of work.** It says what will be delivered and what will not, what the work aims at (good),
and what a reviewer will check item by item (good enough). It does not say how the work is to be done; the approach
belongs to the person doing it. Details the scope does not settle are the worker's call, listed in the pull request as
defaults for the reviewer to approve as one item. Where the scope depends on a decision only a code owner can make,
the issue lists it as an open decision with plain options.

**An issue's good-enough items are of two kinds.** Conformance items say what must hold and are checked by machine: a
test, a lint or format rule, the lock check, a checker script, the workflow. Fitness items say what the change must do
or how it must read, and are validated by a person: it does what the issue intends, it reads as intended, it renders
right. Write each item so a reviewer can tell which it is.

**An issue must be admissible, and this is enforced.** A draft becomes an issue only when it has a bounded scope, a
sane blast radius (the files and surfaces it may touch, small enough to review in one sitting), and definitions of good
and good enough. A draft missing one of these is returned with the gap named, not approved. The conditions, each with
the check that enforces it, are in [the issue admissibility conditions](.github/ISSUE_ADMISSIBILITY.md); [the issue
template](.github/ISSUE_TEMPLATE/scope-of-work.yml) asks for each.

**A candidate scope is a draft issue.** Filing one proposes work; it does not accept or prioritise it. A code owner
approves a draft by making it an issue, after the open decisions are settled, and that approval is the record. Small
fixes, a typo or a broken link, need no issue: open the pull request and say what it fixes.

**A pull request delivers against its issue.** It does one thing its title says and names the issue it resolves. Its
description states what changed, what backs it (a test, a lemma step, a generated value, a source), which tests cover
it, and the tools used. History stays readable: commits that each build and pass, no merges of `main` into a feature
branch, no force-pushes to shared branches. A change that must reach beyond the files its scope names says so, and is
split when it can be. If the work shows the scope itself must change, the change goes back to the issue as an
amendment and is approved there; a pull request does not widen its scope on its own. What a pull request must carry
before it is reviewed, each with the check that enforces it, is in [the pull request admissibility
conditions](.github/PR_ADMISSIBILITY.md); [the pull request template](.github/pull_request_template.md) asks for each.

**Review is against the scope, and reports both kinds.** A reviewer takes the issue's good-enough items one by one.
Conformance is verified by running the checks and quoting the result; a tool may run them. Fitness is validated by a
named reviewer who looks at the thing, the page in a browser, the figure, the output of the example, and signs the
judgement in the review. No passing check stands in for that judgement, and no judgement excuses a failing check. A
pull request merges into `dev`, by a code owner who is not its author (a rule that cannot hold while the code owners
are one person, and binds by design the moment there are two), when every conformance item passes, every fitness item
is validated, and no gap is left open: each gap is accepted as is with a reason, fixed before the merge,
or made its own issue. The merge closes the issues the pull request resolves.

**Checks a pull request must pass.** `uv run ruff check .`, `uv run ruff format --check .`, `uv lock --check`, `uv run
pytest`, the vocabulary and residual checks, and the test workflow on both platforms. The workflow also refuses any
commit whose message names a tool as an author or generator. These are conformance; they are necessary and never
sufficient.

**Merges into `main` are releases.** Only a code owner merges `dev` into `main`, with a merge commit.
The merge starts the release workflow, which creates the version tag, publishes to PyPI by trusted
publishing, deploys the site and publishes the GitHub release. The code owner approves the release
by merging it. The PyPI environment requires no further approval. A merge whose version is already released
and whose package files are unchanged since its tag redeploys the site only. Versions follow
semantic versioning. Use a patch version for a fix, a minor version for a compatible addition and
a major version for a breaking change. Record each change in the changelog.
The release workflow rejects candidates that fail the
[release checks](.github/RELEASE_ADMISSIBILITY.md).

**Code owners.** The code owners are the permissioned set named in `.github/CODEOWNERS`; the file is the record of who may
approve, merge and release, and adding one changes that file and nothing here. How a code owner is added, how a
release is cut, and the repository settings that enforce the above are in the [code owners' page](docs/code-owners.md).
The release rules in one page, the two reviews, the file that declares the settings and the check that runs first in
every workflow are in [`GOVERNANCE.md`](GOVERNANCE.md). Security reports go as [SECURITY.md](SECURITY.md) says, not to
the issue tracker; that file is for reporting a vulnerability and does not govern releases.

## Contributing to the paper

The paper takes its own route, apart from the software's. It lives in `paper/` (the two notebooks, `paper.ipynb` and
`supporting_material.ipynb`, their generators, the MyST configuration and the mode file) and is edited on the `paper`
branch: a change to it is a pull request against `paper`, from a branch cut from `paper`, never a pull request into
`dev`. Files under `tests/` and `scripts/` are the software's even when the paper's tests read them (the paper's tests,
the residual baseline); they change on `dev` by the route above, and `paper` merges `dev` in.

**Who reviews and approves.** The paper's approvers are the logins on the `paper/` line of `.github/CODEOWNERS`
(today `mzargham` and `jshorish`), set apart from the code owners of the `*` line, who approve, merge and release the
code and the documentation. A pull request into `paper` is merged by an approver who is not its author; the merge
check records it. The same pull request template serves, with its `Paper` section filled: the section or figure
changed, the residual check's result (`uv run python scripts/check_residuals.py --compare scripts/residuals_baseline.json
--strict --views paper,appendix`) and the build (`cd paper && uv run myst build --html`). Run both before opening the
pull request: the paper workflow runs on a push to `paper`, not on a pull request, so its checks run once the merge
lands.

**What is judged and what is checked.** The approver reads for the argument: that the change says what the paper
claims, each claim backed by a lemma step, a generated value, a test or a verified source, in the glossary's words and
without metanarration; no passing check stands in for that reading. The machine covers the rest, in the paper workflow
(`.github/workflows/paper.yml`): the notebooks execute from a clean kernel and match their committed outputs, the
paper's tests pass, the residual counts do not rise above the baseline, the HTML builds, and the key manifest equals
the built identifiers.

**How it is published.** A pin is one tag, one approval, one record. An approver prepares it on `paper` (`uv run
--no-project python scripts/paper_pin.py prepare --tag paper-<shape>-<date>`, which writes the mode file; a section
in `paper/CHANGES.md`), commits, and pushes the tag `paper-*`. The workflow builds and tests the tag, then waits at
the `paper-release` environment for the other approver (the one who pushed the tag cannot approve it) and publishes
the built paper and its key manifest as a GitHub release. Once the release has a DOI, `paper_pin.py record` writes it
and the artefact's checksum into the mode file, and the pin is complete.

**How it reaches the site.** The site is the software's: `paper` is merged into `dev` (the mode file and the paper's
files travel with it), and the next merge of `dev` into `main` serves the pinned paper at `/paper/`, with its banner.
A merge whose software version is already released redeploys the site only, so a new pin needs no software release.

## Tooling and dependencies

The Python version is in [`.python-version`](.python-version), the dependencies in [`pyproject.toml`](pyproject.toml),
and the exact resolution with hashes in [`uv.lock`](uv.lock); those files change, this page does not. Install with
`uv sync`; every command is `uv run ...`. Continuous integration installs from the lock file only (`uv sync --locked`)
and fails if the lock no longer matches `pyproject.toml`, so what is tested is what is declared, and nothing is
fetched that the lock does not name. Dependency updates arrive as pull requests from the update bot and go through
the same review as any change. Every workflow action is pinned to a commit, not a tag. A release ships with a software
bill of materials, so what a version contains can be audited afterwards.

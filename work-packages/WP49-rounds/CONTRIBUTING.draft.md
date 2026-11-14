# Contributing to hyperbolic-trade-space

This page says who owns a change here, how tools fit, and how a change moves from an idea to a release. Conduct
between people is the [code of conduct](CODE_OF_CONDUCT.md), the Contributor Covenant, which this project adopts
unaltered.

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
and good enough. A draft missing one of these is returned with the gap named, not approved. The issue template asks for
each.

**A candidate scope is a draft issue.** Filing one proposes work; it does not accept or prioritise it. A code owner
approves a draft by making it an issue, after the open decisions are settled, and that approval is the record. Small
fixes, a typo or a broken link, need no issue: open the pull request and say what it fixes.

**A pull request delivers against its issue.** It does one thing its title says and names the issue it resolves. Its
description states what changed, what backs it (a test, a lemma step, a generated value, a source), which tests cover
it, and the tools used. History stays readable: commits that each build and pass, no merges of `main` into a feature
branch, no force-pushes to shared branches. A change that must reach beyond the files its scope names says so, and is
split when it can be. If the work shows the scope itself must change, the change goes back to the issue as an
amendment and is approved there; a pull request does not widen its scope on its own.

**Review is against the scope, and reports both kinds.** A reviewer takes the issue's good-enough items one by one.
Conformance is verified by running the checks and quoting the result; a tool may run them. Fitness is validated by a
named reviewer who looks at the thing, the page in a browser, the figure, the output of the example, and signs the
judgement in the review. No passing check stands in for that judgement, and no judgement excuses a failing check. A
pull request merges into `dev`, by a code owner who is not its author, when every conformance item passes, every
fitness item is validated, and no gap is left open: each gap is accepted as is with a reason, fixed before the merge,
or made its own issue. The merge closes the issues the pull request resolves.

**Checks a pull request must pass.** `uv run ruff check .`, `uv run ruff format --check .`, `uv lock --check`, `uv run
pytest`, the vocabulary and residual checks, and the test workflow on both platforms. The workflow also refuses any
commit whose message names a tool as an author or generator. These are conformance; they are necessary and never
sufficient.

**Merges into `main` are releases.** Only a code owner merges `dev` into `main`, with `git merge --no-ff` and a
version tag. Versions follow semantic versioning: a patch for a fix, a minor for a compatible addition, a major for a
breaking change; the changelog names each. Publishing to PyPI runs from the tag through the release workflow and needs
a code owner's approval of its environment.

**Code owners.** The code owners are the permissioned set named in `.github/CODEOWNERS`; the file is the record of who may
approve, merge and release, and adding one changes that file and nothing here. How a code owner is added, how a
release is cut, and the repository settings that enforce the above are in the [code owners' page](docs/maintainers.md). Security reports go as [SECURITY.md](SECURITY.md) says, not to
the issue tracker.

## Tooling and dependencies

The Python version is in [`.python-version`](.python-version), the dependencies in [`pyproject.toml`](pyproject.toml),
and the exact resolution with hashes in [`uv.lock`](uv.lock); those files change, this page does not. Install with
`uv sync`; every command is `uv run ...`. Continuous integration installs from the lock file only (`uv sync --locked`)
and fails if the lock no longer matches `pyproject.toml`, so what is tested is what is declared, and nothing is
fetched that the lock does not name. Dependency updates arrive as pull requests from the update bot and go through
the same review as any change. Every workflow action is pinned to a commit, not a tag. A release ships with a software
bill of materials, so what a version contains can be audited afterwards.

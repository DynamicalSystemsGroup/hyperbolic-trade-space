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

**Scope first.** Work here is done in packages with a written scope: what is delivered, what is not, and what good
enough means, approved by the maintainer before the work starts. A small fix needs no package; anything that changes
what a user sees, a result the paper states, or a public name does. Open an issue to propose one; the templates ask for
what the scope needs.

**Narrow and readable.** A pull request does one thing its title says. Its description states what changed, what backs
it (a test, a lemma step, a generated value, a source), which tests cover it, and the tools used. History stays
readable: commits that each build and pass, no merges of `main` into a feature branch, no force-pushes to shared
branches.

**Review against the scope.** A reviewer checks the change against its scope and runs it: the suite, the lint and
format checks, the lock check, and, for anything rendered, the page or figure in a browser. Reading the diff alone is
not a review. The reviewer's record of what was run is part of the delivery.

**Blast radius.** A change touches the files its scope names. A change that must reach further says so in its scope
and is split when it can be.

**Checks a pull request must pass.** `uv run ruff check .`, `uv run ruff format --check .`, `uv lock --check`, `uv run
pytest`, the vocabulary and residual checks, and the test workflow on both platforms. The workflow also refuses any
commit whose message names a tool as an author or generator.

**Branches and releases.** Candidates are built on `dev`. Releases are cut from `main` by the maintainer, who alone
merges to it, with `git merge --no-ff dev` and a version tag. Versions follow semantic versioning: a patch for a fix, a
minor for a compatible addition, a major for a breaking change; the changelog names each. Publishing to PyPI runs
from the tag through the release workflow and needs the maintainer's approval of its environment.

**Maintainers.** How a maintainer is added, how a release is cut, and the repository settings that enforce the above
are in the [maintainers' page](docs/maintainers.md). Security reports go as [SECURITY.md](SECURITY.md) says, not to
the issue tracker.

## Tooling in one line

Python 3.12 and [uv](https://docs.astral.sh/uv/): `uv sync`, then every command is `uv run ...`. The test suite runs
doctests; a public function has a numpydoc docstring with one.

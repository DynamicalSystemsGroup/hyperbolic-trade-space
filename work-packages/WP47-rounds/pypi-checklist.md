# The supervisor's PyPI steps (WP47, D-5)

Nothing here is done by the assistant. Names are exact; the package is `hyperbolic-trade-space`.

## The names

| Item | Value |
|---|---|
| Repository | `DynamicalSystemsGroup/hyperbolic-trade-space` |
| Workflow file | `release.yml` (`.github/workflows/release.yml`; workflow name "Release") |
| TestPyPI publish job | `publish-testpypi`, environment `testpypi` |
| PyPI publish job | `publish-pypi`, environment `pypi` |
| GitHub release job | `github-release` (no environment; attaches the wheel, the sdist and the bill of materials) |

## Steps

1. Accounts: create (or sign in to) accounts on <https://test.pypi.org> and <https://pypi.org>; turn on two-factor
   authentication on both.
2. Pending trusted publisher on TestPyPI (Your account, Publishing, Add a new pending publisher, GitHub):
   PyPI project name `hyperbolic-trade-space`; owner `DynamicalSystemsGroup`; repository `hyperbolic-trade-space`;
   workflow name `release.yml`; environment name `testpypi`.
3. The same on PyPI with environment name `pypi`.
4. GitHub, Settings, Environments: create `testpypi` and `pypi` (details in `docs/code-owners.md`).
5. GitHub, Settings, Branches: the rulesets in `docs/code-owners.md`; Settings, Labels: create `draft` and `small-fix`.
   On the `pypi` environment add yourself as required approver (a code owner).
6. Dry run on TestPyPI: Actions, Release, Run workflow, branch `dev`, target `testpypi` (use a candidate version
   such as `0.1.0rc1` if the head's version is to be kept for PyPI; a version uploads once per index).
7. Real release, only after the merge to `main`: tag `v0.1.0` on `main` and push it.

Neither index is touched by anything before step 6. No token is created or stored at any step.

## Dry-run record

Pending: the TestPyPI dry run is run with the assistant after step 2.

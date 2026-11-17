# The settings fixture

Responses of the GitHub API recorded on 2026-11-17 by `uv run python scripts/check_repo_settings.py --record
tests/data/wp78` (WP78; `collaborators__jshorish__permission.json` added by WP79), one file per endpoint, the
`__` standing for `/`. The fixture is the declared state, so `test_the_conforming_fixture_passes` holds it to
`.github/governance.toml`.

Three files are not recordings but the declared state written by hand (WP82, 2026-11-17), since a setting changes
on GitHub only after the declaration's pull request is merged: `rulesets__27470804.json` (`main-review`, bypass
actors empty), `actions__permissions__workflow.json` (read, no approving reviews), `rulesets__27471737.json`
(`main-checks`, `controls` among the required checks); and `rulesets__1.json` with its entry in `rulesets.json` is
the `governance-files` push ruleset in the API's shape with a placeholder id. A `--record` run after the settings
are changed replaces all of them with recordings.

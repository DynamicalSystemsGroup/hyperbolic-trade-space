"""The CI workflow runs every test in some shard (offline: reads the YAML and the markers)."""

from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
WF = yaml.safe_load((ROOT / ".github" / "workflows" / "test.yml").read_text(encoding="utf-8"))
JOB = WF["jobs"]["test"]
RUN = next(s["run"] for s in JOB["steps"] if "pytest" in s.get("run", ""))


def test_workflow_is_manual_dispatch_only():
    triggers = WF.get("on", WF.get(True))
    assert set(triggers) == {"workflow_dispatch"}


def test_three_shards_cover_every_test():
    assert JOB["strategy"]["matrix"]["shard"] == ["fast", "slow", "docs-paper"]
    # fast: unmarked; slow: marked, outside the docs modules; docs-paper: marked, inside them.
    assert 'fast) uv run pytest $opts -m "not slow"' in RUN
    assert "uv run pytest $opts -m slow $ignores" in RUN
    assert "--ignore=$m" in RUN
    assert "uv run pytest $opts -m slow $DOCS_MODULES" in RUN
    assert "--deselect" not in RUN and "-k " not in RUN


def test_docs_modules_exist_and_the_group_marker_is_applied():
    for m in WF["env"]["DOCS_MODULES"].split():
        assert (ROOT / m).is_file(), m
    assert "--dist loadgroup" in RUN


def test_every_shard_keeps_the_provisioning():
    text = yaml.safe_dump(JOB)
    for needle in (
        "experiments.toolkit fetch",
        "~/.opensysml",
        "REQUIRE_OPENSYSML",
        "actions/cache",
    ):
        assert needle in text, needle
    assert "uv sync --locked" in text

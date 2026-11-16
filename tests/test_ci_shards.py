"""The CI workflow (specification 5.3): its triggers, and three shards that run every software test
and no paper test (offline: reads the YAML and the modules)."""

import re
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
TEXT = (ROOT / ".github" / "workflows" / "test.yml").read_text(encoding="utf-8")
WF = yaml.safe_load(TEXT)
TRIGGERS = WF.get("on", WF.get(True))
JOB = WF["jobs"]["test"]
RUN = next(s["run"] for s in JOB["steps"] if "pytest" in s.get("run", ""))
WINDOWS = WF["jobs"]["windows"]
WINDOWS_RUN = next(s["run"] for s in WINDOWS["steps"] if "pytest" in s.get("run", ""))
DOCS_MODULES = WF["env"]["DOCS_MODULES"].split()
PAPER_MODULES = {
    "tests/test_paper.py",
    "tests/test_paper_static_figures.py",
    "tests/test_container.py",
    "tests/test_paper_model.py",
}


def test_workflow_runs_on_dispatch_call_and_pull_requests_to_main():
    assert set(TRIGGERS) == {"pull_request", "workflow_dispatch", "workflow_call"}
    assert TRIGGERS["pull_request"] == {"branches": ["main"]}
    assert TRIGGERS["workflow_call"]["inputs"]["windows"]["default"] is False
    assert TRIGGERS["workflow_dispatch"]["inputs"]["windows"]["default"] is True
    # The required checks on a pull request read `test (fast)`, `test (slow)`, `test (docs)`.
    assert JOB["name"] == "test (${{ matrix.shard }})"


def test_three_shards_cover_every_software_test():
    assert JOB["strategy"]["matrix"]["shard"] == ["fast", "slow", "docs"]
    # fast: unmarked; slow: marked, outside the docs modules; docs: marked, inside them.
    assert 'fast) uv run pytest $opts -m "not slow and not paper" ;;' in RUN
    assert 'uv run pytest $opts -m "slow and not paper" $ignores ;;' in RUN
    assert "--ignore=$m" in RUN
    assert 'docs) uv run pytest $opts -m "slow and not paper" $DOCS_MODULES ;;' in RUN
    for run in (RUN, WINDOWS_RUN):
        commands = [line for line in run.splitlines() if "uv run pytest" in line]
        assert commands and all("not paper" in c for c in commands), commands
    assert "--deselect" not in RUN and "-k " not in RUN
    assert "--dist loadgroup" in RUN


def test_docs_modules_exist_and_hold_no_paper_module():
    assert DOCS_MODULES == [
        "tests/test_site.py",
        "tests/test_build_generated.py",
        "tests/test_docs.py",
        "tests/test_narrative.py",
        "tests/test_paper_slot.py",
    ]
    for m in DOCS_MODULES:
        assert (ROOT / m).is_file(), m
        assert m not in PAPER_MODULES, m
        text = (ROOT / m).read_text(encoding="utf-8")
        assert not re.search(r"^pytestmark\s*=.*\bpaper\b", text, re.M), m


def test_no_shard_sets_the_paper_switch():
    assert "HTS_PAPER_TESTS" not in TEXT
    assert "PAPER_BUILD" not in TEXT and "PAPER_EXECUTE" not in TEXT


def test_windows_never_runs_on_a_pull_request():
    assert "github.event_name != 'pull_request'" in WINDOWS["if"]
    assert "inputs.windows" in WINDOWS["if"]
    assert WINDOWS["strategy"]["matrix"]["shard"] == ["fast", "slow"]
    assert "push" not in TRIGGERS


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

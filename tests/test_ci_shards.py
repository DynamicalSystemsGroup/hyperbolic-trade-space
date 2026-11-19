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


CONTROLS = WF["jobs"]["controls"]
# Every pull request into dev, a person's or Dependabot's, runs lint and the fast shard; the
# settings check (controls) is skipped there, since a pull request may carry a declaration ahead
# of the live settings.
CONTROLS_IF = (
    "${{ (github.workflow == 'Tests' || inputs.controls) && "
    "(github.event_name != 'pull_request' || github.base_ref != 'dev') }}"
)
TEST_IF = (
    "${{ !cancelled() && (needs.controls.result == 'success' || "
    "needs.controls.result == 'skipped') }}"
)


def test_workflow_runs_on_dispatch_call_pull_requests_to_main_and_pushes_to_dev():
    assert set(TRIGGERS) == {"push", "pull_request", "workflow_dispatch", "workflow_call"}
    assert TRIGGERS["pull_request"] == {"branches": ["main", "dev"]}
    assert TRIGGERS["push"] == {"branches": ["dev"]}
    assert TRIGGERS["workflow_call"]["inputs"]["windows"]["default"] is False
    assert TRIGGERS["workflow_dispatch"]["inputs"]["windows"]["default"] is True
    # The required checks on a pull request read `test (fast)`, `test (slow)`, `test (docs)`.
    assert JOB["name"] == "test (${{ matrix.shard }})"


def test_three_shards_cover_every_software_test():
    assert all(
        f'"{shard}"' in JOB["strategy"]["matrix"]["shard"] for shard in ("fast", "slow", "docs")
    )
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
    assert "github.event_name != 'push'" in WINDOWS["if"]


def test_a_push_to_dev_and_a_pull_request_into_dev_run_the_fast_shard_alone():
    # A called workflow sees the caller's event, so both cases name this workflow too (the WP67
    # dry run found the release's test job reduced to the fast shard without it).
    into_dev = "(github.event_name == 'push' || github.base_ref == 'dev')"
    on_push = f"""({into_dev} && github.workflow == 'Tests') && '["fast"]'"""
    otherwise = """|| '["fast", "slow", "docs"]'"""
    assert JOB["strategy"]["matrix"]["shard"] == f"${{{{ fromJSON({on_push} {otherwise}) }}}}"


def test_a_pull_request_into_dev_runs_the_fast_shard_for_anyone_and_skips_controls():
    # controls is skipped on a pull request into dev; test accepts a skipped controls (the release's
    # call skips it too) and carries no condition on the event or the actor. Windows is already off
    # on every pull request.
    assert CONTROLS["if"] == CONTROLS_IF
    assert JOB["if"] == TEST_IF
    assert "github.actor" not in TEXT
    # The controls job declares the reads its endpoints need.
    assert CONTROLS["permissions"] == {"contents": "read", "actions": "read", "pages": "read"}


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

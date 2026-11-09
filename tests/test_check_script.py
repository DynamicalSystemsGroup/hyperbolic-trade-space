"""scripts/check.py: the path-to-tests map and the modes (offline, no test is run)."""

import importlib.util
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
_spec = importlib.util.spec_from_file_location("check_script", ROOT / "scripts" / "check.py")
check = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(check)


def flat(paths):
    return [a for g in check.mapped_tests(paths) for a in g]


def test_every_mapped_test_file_exists():
    for _, args in check.PATH_TESTS:
        for a in args:
            if a.startswith(("tests/", "src")):
                assert (ROOT / a).exists(), a


@pytest.mark.parametrize(
    ("path", "expected"),
    [
        ("derivation/lemma_01.py", "tests/test_proof_map.py"),
        ("paper/paper.ipynb", "tests/test_case.py"),
        ("docs/theory.md", "tests/test_docs.py"),
        ("site/index.html", "tests/test_site.py"),
        ("scripts/assemble_site.py", "tests/test_build_generated.py"),
        ("src/hyperbolic_trade_space/estimator.py", "tests/test_estimator.py"),
        ("examples/adcs/experiments/runner.py", "tests/test_experiments.py"),
        ("work-packages/interface-contract.toml", "tests/test_interface_contract.py"),
        ("glossary.yaml", "tests/test_build_generated.py"),
        ("Dockerfile", "tests/test_container.py"),
        ("paper/container/x", "tests/test_container.py"),
    ],
)
def test_path_maps_to_its_tests(path, expected):
    assert expected in flat([path])


def test_derivation_adds_the_appendix_b_test():
    assert ["tests/test_paper.py", "-k", "appendix_b"] in check.mapped_tests(["derivation/x.py"])


def test_a_changed_test_file_runs_itself_and_unmapped_paths_have_no_mapping():
    assert check.mapped_tests(["tests/test_check_script.py"]) == [["tests/test_check_script.py"]]
    assert check.mapped_tests(["README.md"]) == []


@pytest.mark.parametrize(
    "path",
    ["README.md", "work-packages/WP20-review.md", "uv.lock", "tests/conftest.py"],
)
def test_unmapped_paths_fall_back_to_the_fast_suite(path, monkeypatch, capsys):
    assert check.unmapped([path]) == [path]
    assert check.unmapped(["src/hyperbolic_trade_space/estimator.py"]) == []
    monkeypatch.setattr(check, "changed_paths", lambda base="origin/dev": [path])
    assert check.main(["--changed", "--dry-run"]) == 0
    assert "-m not slow" in capsys.readouterr().out


def test_changed_paths_diff_against_the_merge_base(monkeypatch):
    calls = []

    def fake_run(cmd, **kw):
        calls.append(cmd)

        class R:
            stdout = ""

        return R()

    monkeypatch.setattr(check.subprocess, "run", fake_run)
    check.changed_paths("origin/dev")
    assert ["git", "diff", "--name-only", "origin/dev...HEAD"] in calls
    assert ["git", "diff", "--name-only", "origin/dev"] not in calls


def test_list_and_dry_run_modes(capsys):
    assert check.main(["--list"]) == 0
    assert "derivation/*" in capsys.readouterr().out
    assert check.main(["--fast", "--dry-run"]) == 0
    assert "not slow" in capsys.readouterr().out
    assert check.main(["--changed", "--dry-run"]) == 0

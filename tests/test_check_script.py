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


def test_a_changed_test_file_runs_itself_and_unmapped_paths_run_nothing():
    assert check.mapped_tests(["tests/test_check_script.py"]) == [["tests/test_check_script.py"]]
    assert check.mapped_tests(["README.md"]) == []


def test_list_and_dry_run_modes(capsys):
    assert check.main(["--list"]) == 0
    assert "derivation/*" in capsys.readouterr().out
    assert check.main(["--fast", "--dry-run"]) == 0
    assert "not slow" in capsys.readouterr().out
    assert check.main(["--changed", "--dry-run"]) == 0

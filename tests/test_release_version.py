"""The release version check: a tag must equal v plus the package version."""

import importlib.util
from pathlib import Path

SCRIPT = Path(__file__).resolve().parent.parent / "scripts" / "check_release_version.py"
spec = importlib.util.spec_from_file_location("check_release_version", SCRIPT)
crv = importlib.util.module_from_spec(spec)
spec.loader.exec_module(crv)


def _tree(tmp_path, version):
    (tmp_path / "pyproject.toml").write_text(
        f'[project]\nname = "x"\nversion = "{version}"\n', encoding="utf-8"
    )
    return ["--root", str(tmp_path)]


def test_matching_tag_passes(tmp_path):
    assert crv.main(["--tag", "v0.1.0", *_tree(tmp_path, "0.1.0")]) == 0


def test_mismatched_tag_is_refused(tmp_path, capsys):
    assert crv.main(["--tag", "v0.1.1", *_tree(tmp_path, "0.1.0")]) == 1
    assert "does not match" in capsys.readouterr().err


def test_no_tag_needs_only_a_valid_version(tmp_path):
    assert crv.main(_tree(tmp_path, "0.1.0rc1")) == 0
    assert crv.main(_tree(tmp_path, "0.1")) == 1


def test_this_repository_has_a_valid_version():
    assert crv.check(crv.package_version(), None) is None

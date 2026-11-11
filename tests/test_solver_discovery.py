"""The solver is found where the ``z3-solver`` wheel installs it, not only on ``PATH`` (WP34, Windows)."""

import os
import stat
import sys

from experiments import exclusion


def _fake_prefix(tmp_path):
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    exe = bin_dir / ("z3.exe" if sys.platform == "win32" else "z3")
    exe.write_text("", encoding="utf-8")
    exe.chmod(exe.stat().st_mode | stat.S_IXUSR)
    return bin_dir


def test_solver_in_the_wheel_directory_is_found_and_put_on_path(tmp_path, monkeypatch):
    bin_dir = _fake_prefix(tmp_path)
    monkeypatch.setenv("PATH", str(tmp_path / "empty"))
    monkeypatch.setattr(sys, "prefix", str(tmp_path))
    assert exclusion.solver_available()
    assert os.environ["PATH"].split(os.pathsep)[0] == str(bin_dir)


def test_no_solver_anywhere_is_unavailable(tmp_path, monkeypatch):
    monkeypatch.setenv("PATH", str(tmp_path / "empty"))
    monkeypatch.setattr(sys, "prefix", str(tmp_path))
    assert not exclusion.solver_available()

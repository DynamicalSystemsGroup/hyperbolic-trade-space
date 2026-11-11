"""The WP30 mode of ledger_gate.py: the notes, the entry numbers and the neutrality rule."""

from __future__ import annotations

import importlib.util
from pathlib import Path

import pytest

SCRIPT = Path(__file__).resolve().parents[1] / "examples/adcs/model_v2/ledger_gate.py"


@pytest.fixture(scope="module")
def gate():
    spec = importlib.util.spec_from_file_location("ledger_gate", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _entries(gate):
    return gate.lg.read(gate.lg.LEDGER_PATH)


def test_each_wp30_note_names_where_the_run_is_made(gate):
    exp = gate.ORDER[0]
    host = gate.declared(exp, _entries(gate), None, wp30="regen")
    image = gate.declared(exp, _entries(gate), "abc123", wp30="values")
    assert "on the host" in host.inputs["note"] and "thirteen traded metrics" in host.inputs["note"]
    assert "image abc123" in image.inputs["note"] and "equal to the hash" in image.inputs["note"]


def test_an_unknown_wp30_kind_is_refused(gate):
    with pytest.raises(ValueError, match="regen"):
        gate.declared(gate.ORDER[0], _entries(gate), None, wp30="other")


def test_the_other_modes_keep_their_notes(gate):
    exp, entries = gate.ORDER[0], _entries(gate)
    assert gate.declared(exp, entries, None, wp26=True).inputs["note"].startswith("WP26")
    assert gate.declared(exp, entries, "i").inputs["note"].startswith("WP23 close-out gate")


def test_the_regeneration_supersedes_the_current_entries_and_numbers_them_next(gate):
    entries = _entries(gate)
    for exp in gate.ORDER:
        current = gate.lg.latest(entries, exp.id)["id"]
        run = gate.declared(exp, entries, None, wp30="regen")
        n = int(current.rsplit("@", 1)[1]) + 1
        assert run.id == f"{exp.id}@{n}" and run.supersedes == (current,)


def test_moved_compares_output_hashes(gate):
    assert not gate.moved({"output_sha256": "a"}, {"output_sha256": "a"})
    assert gate.moved({"output_sha256": "a"}, {"output_sha256": "b"})


@pytest.mark.parametrize("same,code", [(True, 0), (False, 1)])
def test_values_mode_exits_one_when_an_output_hash_moves(gate, monkeypatch, capsys, same, code):
    def fake_run_one(run):
        prev = gate.lg.latest(_entries(gate), run.supersedes[0])
        out = prev["output_sha256"] if same else "0" * 64
        return {**prev, "output_sha256": out, "git_dirty": False}

    monkeypatch.setattr(gate, "run_one", fake_run_one)
    args = ["--host", "--wp30", "values"]
    assert gate.main(args) == code
    assert ("not neutral" in capsys.readouterr().out) is (not same)


def test_regeneration_mode_requires_nothing_of_the_hashes(gate, monkeypatch):
    def fake_run_one(run):
        prev = gate.lg.latest(_entries(gate), run.supersedes[0])
        return {**prev, "output_sha256": "0" * 64, "git_dirty": False}

    monkeypatch.setattr(gate, "run_one", fake_run_one)
    assert gate.main(["--host", "--wp30", "regen"]) == 0


def test_the_wp30_and_wp26_flags_are_exclusive(gate):
    with pytest.raises(SystemExit):
        gate.main(["--host", "--wp26", "--wp30", "regen", "--dry"])

"""WP15 part 15.3: experiment declaration, runner, ledger and the adopted frozen entries."""

import json
import pathlib
import subprocess
import sys
from types import SimpleNamespace

import pandas as pd
import pytest
from experiments import definitions as defs
from experiments import ledger as lg
from experiments import runner
from experiments.experiment import Experiment
from experiments.oracle import Oracle, evaluate_rows

REPO = pathlib.Path(__file__).resolve().parents[1]
ADCS = REPO / "examples" / "adcs"
FROZEN_CSVS = sorted((ADCS / "data").glob("*.csv"))


# -- toy oracles of the three evidence kinds (pure Python) -------------------------------------
class _Base:
    config_names = ("a", "b")
    attribute_names = ("sum_ab",)
    flag_names = ("positive",)

    def evaluate(self, designs):
        return evaluate_rows(self, designs)


class SimulatorToy(_Base):
    """Evidence from a computation."""

    def __call__(self, c):
        s = float(c["a"]) + float(c["b"])
        return {"sum_ab": s, "positive": s > 0, "aux": 1.0}


class PhysicalToy(_Base):
    """Evidence from recorded test measurements read from a file."""

    def __init__(self, path):
        self.table = pd.read_csv(path).set_index("design_id")

    def __call__(self, c):
        r = self.table.loc[int(c["design_id"])]
        return {"sum_ab": float(r.measured), "positive": bool(r.measured > 0)}


class HumanToy(_Base):
    """Evidence from a callable standing in for raters."""

    def __init__(self, rater):
        self.rater = rater

    def __call__(self, c):
        score = float(self.rater(c))
        return {"sum_ab": score, "positive": score > 0}


def _sampler():
    return runner.LogUniformSampler({"kind": ["x", "y"]}, {"a": (1.0, 10.0), "b": (0.1, 1.0)})


def _tree(tmp_path):
    (tmp_path / "model.txt").write_text("toy model v1\n")
    (tmp_path / "code.py").write_text("# toy code\n")
    return tmp_path


def _exp(**kw):
    base = dict(
        id="toy",
        output="out/toy.csv",
        count=4,
        seed=7,
        oracle="toy",
        sampler="toy",
        scenario="s0",
        model_path="model.txt",
        code=("code.py",),
    )
    return Experiment(**(base | kw))


def test_oracle_protocol_is_tool_free_and_satisfied_by_toys():
    assert isinstance(SimulatorToy(), Oracle)
    assert {"config_names", "attribute_names", "flag_names", "__call__", "evaluate"} <= set(
        dir(SimulatorToy())
    )


def test_core_modules_import_without_opensysml():
    code = (
        "import sys\n"
        "for m in ('opensysml', 'opensysml.values'):\n"
        "    sys.modules[m] = None\n"
        "import experiments.oracle, experiments.experiment, experiments.ledger\n"
        "import experiments.runner, experiments.definitions\n"
        "assert sys.modules['opensysml'] is None\n"
    )
    r = subprocess.run(
        [sys.executable, "-c", code],
        capture_output=True,
        text=True,
        env={"PYTHONPATH": str(ADCS), "PATH": ""},
    )
    assert r.returncode == 0, r.stderr


def test_small_experiment_entry_has_every_field(tmp_path):
    root = _tree(tmp_path)
    led = root / "ledger.jsonl"
    [e] = runner.run(_exp(), SimulatorToy(), _sampler(), root, led)
    assert set(lg.FIELDS) <= set(e)
    assert e["kind"] == "generated" and e["evidence_kind"] == "simulation"
    assert e["output_rows"] == 4
    assert e["model_sha256"] == lg.sha256_file(root / "model.txt")
    assert e["code"] == {"code.py": lg.sha256_file(root / "code.py")}
    assert e["output_sha256"] == lg.sha256_file(root / "out" / "toy.csv")
    assert e["prev_hash"] is None and e["entry_hash"] == lg.hash_entry(e)
    assert set(e["versions"]) >= {"opensysml", "python", "numpy", "scipy", "pandas"}
    assert e["inputs"]["seed"] == 7 and e["inputs"]["scenario"] == "s0"
    assert e["time_utc"].endswith("Z") and e["platform"]
    assert "git_commit" in e and "git_dirty" in e
    assert lg.verify(led, root) == []
    cols = list(pd.read_csv(root / "out" / "toy.csv").columns)
    assert cols == ["design_id", "seed", "kind", "a", "b", "sum_ab", "positive", "aux"]


def test_model_none_is_null(tmp_path):
    root = _tree(tmp_path)
    [e] = runner.run(_exp(model_path=None), SimulatorToy(), _sampler(), root)
    assert e["model_path"] is None and e["model_sha256"] is None


@pytest.mark.parametrize("what", ["output", "model", "code", "entry"])
def test_editing_makes_verify_fail_naming_the_entry(tmp_path, what):
    root = _tree(tmp_path)
    led = root / "ledger.jsonl"
    runner.run(_exp(), SimulatorToy(), _sampler(), root, led)
    if what == "output":
        (root / "out" / "toy.csv").write_text("tampered\n")
    elif what == "model":
        (root / "model.txt").write_text("toy model v2\n")
    elif what == "code":
        (root / "code.py").write_text("# changed\n")
    else:
        text = led.read_text().replace('"seed": 7', '"seed": 8')
        led.write_text(text)
    drifts = lg.verify(led, root)
    assert drifts and all(d.entry_id == "toy" for d in drifts)
    assert any(what in d.what or what == "entry" for d in drifts)


def test_append_refuses_to_rewrite(tmp_path):
    root = _tree(tmp_path)
    led = root / "ledger.jsonl"
    runner.run(_exp(), SimulatorToy(), _sampler(), root, led)
    with pytest.raises(lg.LedgerError):
        runner.run(_exp(), SimulatorToy(), _sampler(), root, led)
    entry = lg.read(led)[0]
    with pytest.raises(lg.LedgerError):
        lg.append(led, entry)
    lines = led.read_text().splitlines()
    led.write_text(lines[0].replace("toy", "toz", 1) + "\n")
    with pytest.raises(lg.LedgerError):
        lg.append(led, {**entry, "id": "other"})


def test_sweep_expands_to_one_entry_per_cell(tmp_path):
    root = _tree(tmp_path)
    led = root / "ledger.jsonl"
    exp = _exp(sweep={"scenario": ["s1", "s2"], "gain_box": ["g1", "g2", "g3"]})
    assert len(exp.expand()) == 6
    seen = []

    def oracle_factory(cell):
        seen.append((cell.scenario, cell.gain_box))
        return SimulatorToy()

    entries = runner.run(exp, oracle_factory, lambda cell: _sampler(), root, led)
    assert len(entries) == 6 == len(lg.read(led))
    assert len({e["id"] for e in entries}) == 6 and len({e["output_path"] for e in entries}) == 6
    assert sorted(set(seen)) == sorted({(s, g) for s in ("s1", "s2") for g in ("g1", "g2", "g3")})
    assert {e["inputs"]["gain_box"] for e in entries} == {"g1", "g2", "g3"}
    assert lg.verify(led, root) == []


def test_sweep_rejects_unknown_axis():
    with pytest.raises(ValueError):
        _exp(sweep={"seed": [1]})


def test_design_i_is_independent_of_n():
    s = _sampler()
    small, large = s.draw(3, 11), s.draw(50, 11)
    pd.testing.assert_frame_equal(small, large.iloc[:3])


def test_sampler_matches_the_frozen_generator_scheme():
    """Same draws as the frozen ``CubesatModel.sample_designs`` for the same ranges."""
    import cubesat_model as cm

    stub = SimpleNamespace(
        wheel_classes=["small", "medium", "large"],
        tracker_grades=["coarse", "medium", "fine"],
        panel_span_range=(0.3, 1.0),
        battery_wh_range=(20.0, 200.0),
        kp_range=(0.2, 2.0),
        kd_range=(0.3, 1.5),
    )
    frozen = cm.CubesatModel.sample_designs(stub, 25, 0)
    ours = runner.LogUniformSampler(
        {"wheel_class": stub.wheel_classes, "st_grade": stub.tracker_grades},
        {
            "panel_span_m": stub.panel_span_range,
            "battery_wh": stub.battery_wh_range,
            "Kp": stub.kp_range,
            "Kd": stub.kd_range,
        },
    ).draw(25, 0)
    pd.testing.assert_frame_equal(frozen, ours)


def test_three_evidence_kinds_run_through_runner_and_ledger(tmp_path):
    root = _tree(tmp_path)
    led = root / "ledger.jsonl"
    designs = _sampler().draw(4, 3)
    (root / "campaign.csv").write_text(
        pd.DataFrame({"design_id": range(4), "measured": [1.5, -0.5, 2.0, 0.25]}).to_csv(
            index=False
        )
    )

    class Fixed:
        def draw(self, n, seed):
            return designs.iloc[:n]

    sim = runner.run(_exp(id="sim"), SimulatorToy(), Fixed(), root, led)[0]
    phys = runner.run(
        _exp(id="phys", output="out/phys.csv", evidence_kind="physical-test"),
        PhysicalToy(root / "campaign.csv"),
        Fixed(),
        root,
        led,
    )[0]
    hum = runner.run(
        _exp(id="hum", output="out/hum.csv", evidence_kind="human-assessment"),
        HumanToy(lambda c: 3.0 - float(c["a"])),
        Fixed(),
        root,
        led,
    )[0]
    assert [sim["evidence_kind"], phys["evidence_kind"], hum["evidence_kind"]] == [
        "simulation",
        "physical-test",
        "human-assessment",
    ]
    assert pd.read_csv(root / "out" / "phys.csv").sum_ab.tolist() == [1.5, -0.5, 2.0, 0.25]
    assert lg.verify(led, root) == []
    with pytest.raises(ValueError):
        _exp(evidence_kind="vibes")


def test_parent_hash_is_recorded_and_checked_before_running(tmp_path):
    root = _tree(tmp_path)
    led = root / "ledger.jsonl"
    [p] = runner.run(_exp(id="parent"), SimulatorToy(), _sampler(), root, led)
    child = _exp(id="child", output="out/child.csv", parents=("parent",))
    [c] = runner.run(child, SimulatorToy(), _sampler(), root, led)
    assert c["parents"] == [
        {"id": "parent", "entry_hash": p["entry_hash"], "output_sha256": p["output_sha256"]}
    ]
    assert c["prev_hash"] == p["entry_hash"]
    with pytest.raises(lg.LedgerError):
        runner.run(_exp(id="orphan", parents=("nope",)), SimulatorToy(), _sampler(), root, led)
    (root / "out" / "toy.csv").write_text("tampered\n")
    with pytest.raises(lg.LedgerError):
        runner.run(
            _exp(id="late", output="out/late.csv", parents=("parent",)),
            SimulatorToy(),
            _sampler(),
            root,
            led,
        )
    assert not (root / "out" / "late.csv").exists()


def test_declared_model_hash_must_match(tmp_path):
    root = _tree(tmp_path)
    with pytest.raises(lg.LedgerError):
        runner.run(_exp(model_sha256="0" * 64), SimulatorToy(), _sampler(), root)


def test_definitions_import_without_runtime_and_declare_v2():
    ids = [e.id for e in defs.V2]
    assert ids == ["v2-primary", "v2-baseline", "v2-check-predictions", "v2-check-designs"]
    assert all(e.output.startswith("examples/adcs/data/v2/") for e in defs.V2)
    prim = defs.EXPERIMENTS["v2-primary"]
    assert (prim.count, prim.seed, prim.gain_box) == (1000, 0, "aggressive")
    assert defs.EXPERIMENTS["v2-check-designs"].parents == ("v2-check-predictions",)
    with pytest.raises(KeyError):
        defs.resolve_oracle("no-such-oracle")


# -- the committed ledger ------------------------------------------------------------------------
def test_adopted_entries_for_each_frozen_file_with_equal_hashes():
    entries = {e["output_path"]: e for e in lg.read(lg.LEDGER_PATH)}
    assert len(FROZEN_CSVS) == 5
    for csv in FROZEN_CSVS:
        rel = csv.relative_to(REPO).as_posix()
        e = entries[rel]
        assert e["kind"] == "adopted"
        assert e["output_sha256"] == lg.sha256_file(csv)
        assert e["inputs"]["command"] and e["inputs"]["generating_commit"]
        assert e["inputs"]["tolerances"]
        assert e["evidence_kind"] == "simulation"


def test_generating_commits_touched_the_files():
    for e in lg.read(lg.LEDGER_PATH):
        if e["kind"] != "adopted":
            continue
        out = subprocess.run(
            ["git", "-C", str(REPO), "log", "-1", "--format=%H", "--", e["output_path"]],
            capture_output=True,
            text=True,
        )
        assert out.stdout.strip() == e["inputs"]["generating_commit"]


def test_committed_ledger_verifies_and_predictions_precede_checks():
    assert lg.verify(lg.LEDGER_PATH, REPO) == []
    ids = [e["id"] for e in lg.read(lg.LEDGER_PATH)]
    assert ids.index("adopted-check_predictions_cubesat") < ids.index(
        "adopted-check_designs_cubesat"
    )


def test_frozen_csvs_unchanged_in_git():
    out = subprocess.run(
        ["git", "-C", str(REPO), "diff", "--stat", "--", "examples/adcs/data/*.csv"],
        capture_output=True,
        text=True,
    )
    assert out.stdout.strip() == ""


def test_adopt_is_idempotent_and_does_not_touch_the_files(tmp_path):
    led = tmp_path / "l.jsonl"
    before = {c: lg.sha256_file(c) for c in FROZEN_CSVS}
    first = runner.adopt(defs.FROZEN, REPO, led)
    assert len(first) == 5 and runner.adopt(defs.FROZEN, REPO, led) == []
    assert before == {c: lg.sha256_file(c) for c in FROZEN_CSVS}
    assert json.loads(led.read_text().splitlines()[3])["parents"][0]["id"].startswith("adopted-")


def test_cli_verify_and_compare_message():
    env = {"PYTHONPATH": str(ADCS), "PATH": "/usr/bin:/bin"}
    v = subprocess.run(
        [sys.executable, "-m", "experiments", "verify"],
        capture_output=True,
        text=True,
        env=env,
        cwd=REPO,
    )
    assert v.returncode == 0, v.stdout + v.stderr
    c = subprocess.run(
        [sys.executable, "-m", "experiments", "compare"],
        capture_output=True,
        text=True,
        env=env,
        cwd=REPO,
    )
    assert c.returncode in (0, 2)

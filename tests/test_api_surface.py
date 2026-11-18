"""The record of the public surface (GOVERNANCE.md, "Versions"): tests/data/api_surface.json equals
the package as imported, so a pull request that changes the surface rewrites the record; and
scripts/api_surface.py names each difference."""

import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SNAPSHOT = ROOT / "tests" / "data" / "api_surface.json"
spec = importlib.util.spec_from_file_location("api_surface", ROOT / "scripts" / "api_surface.py")
api = importlib.util.module_from_spec(spec)
spec.loader.exec_module(api)

REWRITE = (
    "The public surface of tradespace differs from tests/data/api_surface.json:\n{}\n"
    "If the change is intended, run `uv run python scripts/api_surface.py --write "
    "tests/data/api_surface.json`, commit the record, and name the change in CHANGELOG.md "
    '(a surface change is a minor release; GOVERNANCE.md, "Versions").'
)


def test_the_committed_record_is_the_live_surface():
    recorded = json.loads(SNAPSHOT.read_text(encoding="utf-8"))
    problems = api.differences(recorded, api.surface())
    assert problems == [], REWRITE.format("\n".join(problems))


def test_the_record_is_written_sorted_and_byte_stable():
    live = api.surface()
    assert api.dumps(live) == SNAPSHOT.read_text(encoding="utf-8")
    assert list(live) == sorted(live)
    assert "tradespace" in live and "tradespace.estimator" in live
    assert "__version__" not in live["tradespace"]
    estimator = live["tradespace.estimator"]["HyperbolicTradeSpace"]
    assert estimator["kind"] == "class" and {"fit", "transform"} <= set(estimator["methods"])
    # Inherited methods belong to the base's surface, not the package's.
    assert "get_params" not in estimator["methods"]


def test_differences_name_added_removed_and_changed_entries():
    f = {"kind": "function", "signature": "(a)"}
    old = {"m": {"f": f, "C": {"kind": "class", "signature": "(x)", "methods": {"go": "(self)"}}}}
    new = {
        "m": {
            "f": {"kind": "function", "signature": "(a, b=1)"},
            "C": {"kind": "class", "signature": "(x)", "methods": {"go": "(self)", "stop": "()"}},
            "K": {"kind": "float", "value": "1.0"},
        }
    }
    assert api.differences(old, new) == [
        "added: m.C.stop",
        "added: m.K",
        "changed: m.f: function (a) -> function (a, b=1)",
    ]
    assert api.differences(new, old) == [
        "removed: m.C.stop",
        "removed: m.K",
        "changed: m.f: function (a, b=1) -> function (a)",
    ]
    assert api.differences(new, new) == []


def test_check_exits_one_and_names_the_entry_when_the_record_is_stale(tmp_path, capsys):
    stale = json.loads(SNAPSHOT.read_text(encoding="utf-8"))
    del stale["tradespace.tuning"]["select_temperature"]
    path = tmp_path / "api_surface.json"
    path.write_text(json.dumps(stale), encoding="utf-8")
    assert api.main(["--check", str(path)]) == 1
    assert "refused: added: tradespace.tuning.select_temperature" in capsys.readouterr().err
    assert api.main(["--write", str(path)]) == 0
    assert api.main(["--check", str(path)]) == 0
    assert api.main(["--check", str(tmp_path / "missing.json")]) == 1

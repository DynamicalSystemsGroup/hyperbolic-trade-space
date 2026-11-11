"""The diagnostic pair of a WP23 round (`examples/adcs/model_v2/diagnostic_pair.py`, D-6).

Runs the script on a short slice of the committed v2 data with the slew-time columns dropped (the
round's header: the traded metrics, no slew time) and a coverage table of its own, into a
temporary folder.
"""

from __future__ import annotations

import csv
import importlib.util
import pathlib
import re

import pandas as pd
import pytest

ROOT = pathlib.Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "examples" / "adcs" / "model_v2" / "diagnostic_pair.py"
V2 = ROOT / "examples" / "adcs" / "data" / "v2"
COVERAGE = ROOT / "examples" / "adcs" / "model_v2" / "views" / "coverage.csv"
SLEW = ("slew_time_s", "slew_time_05deg_s")
ROWS = 200  # about 160 feasible designs per slice: the K = 3 temperature selection brackets its
# target there (test_case.py fits its K sweep on 150), and the two regimes run in seconds

_spec = importlib.util.spec_from_file_location("diagnostic_pair", SCRIPT)
dp = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(dp)


def _slice(src: pathlib.Path, dst: pathlib.Path) -> None:
    df = pd.read_csv(src).iloc[:ROWS]
    df.drop(columns=[c for c in SLEW if c in df.columns]).to_csv(dst, index=False)


def _coverage(path: pathlib.Path, metrics: list[str]) -> None:
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["table", "decision_element", "kind", "metric", "structural"])
        w.writerow(["coverage", "Kp", "tune", metrics[0], "yes"])  # another table: not read
        w.writerow(["table", "metric", "mark", "element"])
        for m in metrics:
            w.writerow(["metrics", m, "MoP", "x"])


@pytest.fixture(scope="module")
def pair(tmp_path_factory):
    tmp = tmp_path_factory.mktemp("round")
    _slice(V2 / "adcs_designs_cubesat.csv", tmp / "dataset.csv")
    _slice(V2 / "adcs_designs_cubesat_gains.csv", tmp / "gains.csv")
    metrics = ["total mass", "control effort", "pointing error", "settling time", "energy balance"]
    _coverage(tmp / "coverage.csv", metrics)
    (tmp / "coverage.md").write_text("# coverage of the test\n", encoding="utf-8")
    out = tmp / "out"
    result = dp.write_pair(tmp / "dataset.csv", tmp / "gains.csv", tmp / "coverage.csv", out)
    return out, metrics, result


def test_the_two_files_and_the_copy_exist(pair):
    out, _, _ = pair
    assert (out / "heatmap.png").stat().st_size > 1000
    assert (out / "heatmap_baseline.png").stat().st_size > 1000
    assert (out / "k3_record.md").exists()
    assert (out / "coverage.md").read_text(encoding="utf-8") == "# coverage of the test\n"


def test_the_two_heatmaps_share_one_colour_scale_and_the_record_says_so(pair):
    out, _, result = pair
    record = (out / "k3_record.md").read_text(encoding="utf-8")
    assert result["vmax"] > dp.case.EXPONENT_FLOOR
    assert (
        f"Both heatmaps share one colour scale, from white at 0.001 to {result['vmax']:.3f}"
        in record
    )


def test_the_shared_top_is_the_larger_of_the_two_figures_own_tops():
    class Image:
        def __init__(self, top):
            self.top = top

        def get_clim(self):
            return (0.001, self.top)

    class Fig:
        def __init__(self, top):
            self.axes = [None, None, type("Ax", (), {"images": [Image(top)]})()]

    assert dp.shared_vmax([Fig(0.25), Fig(0.4), Fig(0.1)]) == 0.4


def test_the_metric_list_is_the_coverage_tables_in_its_order(pair):
    out, metrics, result = pair
    assert result["metrics"] == metrics
    record = (out / "k3_record.md").read_text(encoding="utf-8")
    assert f"traded metrics ({len(metrics)}, from `coverage.csv`): {', '.join(metrics)}" in record
    # the exponent table of each regime lists exactly those metrics, in that order
    tables = re.findall(r"K = 1 exponents:\n\n((?:\|.*\n)+)", record)
    assert len(tables) == 2
    for t in tables:
        names = [line.split("|")[1].strip() for line in t.strip().splitlines()[2:]]
        assert names == metrics
    assert "slew time" not in record
    # the two regimes are "primary" and "baseline" in the record; the CaseSpec's key "stock" is not
    assert "### primary regime (gains.csv)" in record
    assert "### baseline regime (dataset.csv)" in record
    assert "stock" not in record
    # the record's own tables say "term"; the package's refusal messages, quoted verbatim, may not
    headers = [line for line in record.splitlines() if line.startswith("| metric |")]
    assert headers and all("facet" not in h for h in headers)


def test_the_committed_coverage_table_names_eight_metrics_the_spec_knows():
    """Eight since the WP23 close-out (the eclipse reserve left the model)."""
    metrics = dp.metrics_from_coverage(COVERAGE)
    assert len(metrics) == 8 and "slew time" not in metrics and "eclipse reserve" not in metrics
    spec = dp.round_spec(V2 / "adcs_designs_cubesat.csv", V2 / "adcs_designs_cubesat_gains.csv",
                         metrics)  # fmt: skip
    assert [spec.short[a] for a in spec.attributes] == metrics
    assert spec.target_frac == dp.case.CUBESAT.target_frac
    assert spec.tau_bounds == dp.case.CUBESAT.tau_bounds
    assert spec.seed == dp.case.CUBESAT.seed


def test_an_unknown_metric_is_refused(tmp_path):
    _coverage(tmp_path / "coverage.csv", ["total mass", "launch cost"])
    with pytest.raises(ValueError, match="launch cost"):
        dp.round_spec(V2 / "adcs_designs_cubesat.csv", V2 / "adcs_designs_cubesat_gains.csv",
                      dp.metrics_from_coverage(tmp_path / "coverage.csv"))  # fmt: skip

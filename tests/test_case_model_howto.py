"""WP15 part 15.5: the how-to ``examples/adcs/case-model.md`` (R-8, R-16).

The how-to is executable documentation:

* the section list with line pointers and the cadCAD mapping are generated from the model file
  and from ``experiments/experiment.py``; the tests fail when the how-to differs, and
  ``uv run python tests/test_case_model_howto.py --write`` rewrites the generated blocks;
* the fenced blocks named in the how-to (``lang name``) are extracted and run: the toy SysML model
  (the text shown is the fixture), a simulator oracle on it, a physical test campaign read from a
  file, a human assessment from a callable standing in for raters, and the exclusion example; the
  three oracles go through the runner and the ledger and the entries differ in ``evidence_kind``;
* the toolkit table (R-8) names every capability, cites a recorded probe in each row, and its
  engine names exist in ``list_engines()``.

Tests that need the runtime or the solver FAIL with the named cause, never skip.
"""

from __future__ import annotations

import pathlib
import re
import sys
import textwrap

import pytest

ROOT = pathlib.Path(__file__).resolve().parents[1]
ADCS = ROOT / "examples" / "adcs"
HOWTO = ADCS / "case-model.md"
MODEL = ADCS / "model_v2" / "cubesat.sysml"
RECORD = ADCS / "experiments" / "probes" / "probe-record.md"
FENCE = re.compile(r"^```(\w+) +([\w-]+)\n(.*?)^```$", re.M | re.S)
HEADER = re.compile(r"^    // (\d+)\. ([^\n]+)$", re.M)

# the capabilities R-8 requires in the toolkit table, as the first cell shows them
CAPABILITIES = (
    "verify_constraint",
    "verify_requirement",
    "verify_satisfaction",
    "calc",
    "run_analysis",
    "run_sweep",
    "record_run",
    "run_runs",
    "check",
    "lint",
    "verify --solve",
)


# -- generated blocks ---------------------------------------------------------------------------
def render_sections() -> str:
    """The model's sections with line pointers, read from its header comments."""
    text = MODEL.read_text(encoding="utf-8")
    lines = text.splitlines()
    found = [
        (m.group(1), m.group(2), text.count("\n", 0, m.start()) + 1) for m in HEADER.finditer(text)
    ]
    last = max(i for i, line in enumerate(lines, 1) if line.strip())  # the package's closing brace
    rows = ["| section | title | lines |", "|---|---|---|"]
    for i, (num, title, start) in enumerate(found):
        end = (found[i + 1][2] - 2) if i + 1 < len(found) else last - 1
        rows.append(f"| {num} | {title.strip()} | {start} to {end} |")
    return "\n".join(rows)


def render_cadcad() -> str:
    """The cadCAD mapping, in the words of ``experiments.experiment``'s docstring."""
    from experiments import experiment

    doc = experiment.__doc__
    body = doc.split("cadCAD-like mapping, stated once\n", 1)[1].split("\n", 1)[1].strip("\n")
    return "\n".join(f"> {line}".rstrip() for line in body.splitlines())


def _between(text: str, name: str) -> str:
    m = re.search(rf"<!-- {name}:begin -->\n(.*?)\n<!-- {name}:end -->", text, re.S)
    assert m, f"the how-to lacks the generated block {name!r}"
    return m.group(1)


def write_generated() -> None:
    """Rewrite the generated blocks of the how-to."""
    text = HOWTO.read_text(encoding="utf-8")
    for name, body in (("sections", render_sections()), ("cadcad", render_cadcad())):
        text = re.sub(
            rf"(<!-- {name}:begin -->\n).*?(\n<!-- {name}:end -->)",
            lambda m, b=body: m.group(1) + b + m.group(2),
            text,
            flags=re.S,
        )
    HOWTO.write_text(text, encoding="utf-8")


@pytest.fixture(scope="module")
def howto() -> str:
    return HOWTO.read_text(encoding="utf-8")


@pytest.fixture(scope="module")
def blocks(howto) -> dict[str, tuple[str, str]]:
    return {m.group(2): (m.group(1), m.group(3)) for m in FENCE.finditer(howto)}


@pytest.fixture(scope="module")
def connection():
    import cubesat_model as cm

    try:
        return cm.get_connection()
    except cm.OpenSysMLUnavailable as exc:
        pytest.fail(f"the opensysml client could not start: {exc}", pytrace=False)


# -- the structure of the how-to ------------------------------------------------------------------
def test_howto_has_the_six_parts_in_order(howto):
    heads = re.findall(r"^## (.+)$", howto, re.M)
    keys = [
        "contract",
        "Reading the model",
        "Running an experiment",
        "cadCAD",
        "Toolkit",
        "Z3",
        "Provide the oracle",
    ]
    idx = [next(i for i, h in enumerate(heads) if k.lower() in h.lower()) for k in keys]
    assert idx == sorted(idx), heads


def test_sections_block_is_generated_from_the_model(howto):
    assert _between(howto, "sections") == render_sections(), (
        "run: uv run python tests/test_case_model_howto.py --write"
    )
    assert render_sections().count("\n") == 2 + 6  # header rows and seven sections


def test_cadcad_block_is_the_docstring_of_experiment_py(howto):
    assert _between(howto, "cadcad") == render_cadcad(), (
        "run: uv run python tests/test_case_model_howto.py --write"
    )
    from experiments import experiment

    for needle in ("state = a configuration", "Where the mapping does not fit", "one-shot"):
        assert needle in experiment.__doc__ and needle in howto


def test_the_ledger_fields_table_names_every_field(howto):
    from experiments import ledger as lg

    section = howto.split("### The ledger entry", 1)[1].split("\n## ", 1)[0].split("\n### ", 1)[0]
    named = re.findall(r"^\| `(\w+)` \|", section, re.M)
    assert tuple(named) == lg.FIELDS


def test_the_commands_shown_exist(howto):
    from experiments import definitions as df
    from experiments.__main__ import main

    cmds = re.findall(r"python -m experiments (\w+)(?: (\S+))?", howto)
    assert {c for c, _ in cmds} == {"run", "verify", "adopt", "compare"}
    for cmd, arg in cmds:
        if cmd == "run":
            assert arg in {*df.EXPERIMENTS, *df.SHARED_EXPERIMENTS, *df.GROUPS}, arg
    with pytest.raises(SystemExit):
        main(["not-a-command"])


def test_no_hedging_prose(howto):
    prose = FENCE.sub("", howto)
    for word in ("probably", "perhaps", "maybe", "might ", "hopefully", "somewhat", "I think"):
        assert word not in prose, word


# -- the toolkit table (R-8) ----------------------------------------------------------------------
def _table_rows(howto: str) -> list[list[str]]:
    section = _between(howto, "toolkit")
    rows = [
        [c.strip() for c in line.strip().strip("|").split("|")] for line in section.splitlines()
    ]
    return [r for r in rows[2:] if len(r) == 5]


def _probe_numbers() -> dict[int, str]:
    """Probe number -> probe name, from the recorded table (generated in probe order)."""
    text = RECORD.read_text(encoding="utf-8")
    table = text.split("<!-- probes:begin -->", 1)[1].split("<!-- probes:end -->", 1)[0]
    names = re.findall(r"^\| `(\w+)` \|", table, re.M)
    return dict(enumerate(names, 1))


def test_toolkit_table_has_every_required_capability(howto):
    firsts = [r[0] for r in _table_rows(howto)]
    for cap in CAPABILITIES:
        assert any(f"`{cap}`" in f for f in firsts), cap
    assert any("`holds`" in f for f in firsts)


def test_each_toolkit_row_is_complete_and_cites_a_recorded_probe(howto):
    probes = _probe_numbers()
    assert len(probes) == 11
    headings = {
        int(n) for n in re.findall(r"^## (\d+)\. ", RECORD.read_text(encoding="utf-8"), re.M)
    }
    assert headings == set(probes)
    for cap, section, used, why, probe in _table_rows(howto):
        assert section and why, cap
        assert used.split()[0] in ("used", "not"), (cap, used)
        cited = [int(n) for n in re.findall(r"\b(\d+)\b", probe)]
        assert cited and set(cited) <= set(probes), (cap, probe)


def test_engine_names_in_the_table_exist_in_list_engines(howto, connection):
    live = {e.name for e in connection.list_engines()}
    engine_rows = [r for r in _table_rows(howto) if r[0].startswith("engine ")]
    named = {re.search(r"`([^`]+)`", r[0]).group(1) for r in engine_rows}
    assert named == live, (named, live)


def test_probe_numbers_are_the_probes_of_the_module_in_order():
    """A row citing probe n cites the n-th probe of ``probes.py``; ``test_probe_still_holds`` in
    ``test_model_checking_v2.py`` re-runs each by name against the live runtime."""
    from experiments import probes

    names = [fn.__name__.removeprefix("probe_") for fn in probes.PROBES]
    assert names == list(_probe_numbers().values()) == list(probes.EXPECTED)


# -- the Z3 role ----------------------------------------------------------------------------------
def test_the_tests_the_howto_points_to_exist(howto):
    cited = re.findall(r"`(tests/test_\w+\.py)::(test_\w+)`", howto)
    assert cited, "the Z3 section cites tests"
    for path, name in cited:
        assert f"def {name}(" in (ROOT / path).read_text(encoding="utf-8"), (path, name)


def test_the_exclusion_example_runs(blocks, connection):
    from experiments import exclusion

    if not exclusion.solver_available():
        pytest.fail(
            "the solve engine needs z3 or cvc5 on PATH; run through `uv run`", pytrace=False
        )
    _, code = blocks["exclusion-example"]
    ns: dict = {"ADCS": ADCS}
    exec(compile(code, "exclusion-example", "exec"), ns)
    assert ns["verdict"].excluded and ns["record"]["excluded"] is True


# -- plug in another model: three oracles through the runner and the ledger -----------------------
def test_toy_model_is_about_thirty_lines(blocks):
    lang, text = blocks["toy-model"]
    assert lang == "sysml" and 20 <= len(text.strip().splitlines()) <= 40


def test_three_oracles_run_through_the_runner_and_the_ledger(blocks, tmp_path, connection):
    from experiments import ledger as lg

    (tmp_path / "toy.sysml").write_text(blocks["toy-model"][1], encoding="utf-8")
    (tmp_path / "campaign.csv").write_text(blocks["campaign-file"][1], encoding="utf-8")
    ns: dict = {"root": tmp_path}
    for name in ("toy-common", "toy-simulator", "toy-physical", "toy-human", "toy-run"):
        exec(compile(blocks[name][1], name, "exec"), ns)
    entries = lg.read(tmp_path / "ledger.jsonl")
    by_id = {e["id"]: e for e in entries}
    assert [e["id"] for e in entries] == ["toy-simulation", "toy-physical", "toy-human"]
    assert {e["evidence_kind"] for e in entries} == {
        "simulation",
        "physical-test",
        "human-assessment",
    }
    assert by_id["toy-simulation"]["model_sha256"] == lg.sha256_file(tmp_path / "toy.sysml")
    assert (
        by_id["toy-physical"]["model_sha256"] is None and by_id["toy-human"]["model_sha256"] is None
    )
    assert by_id["toy-physical"]["code"] == {
        "campaign.csv": lg.sha256_file(tmp_path / "campaign.csv")
    }
    assert all(e["output_rows"] == 4 and e["kind"] == "generated" for e in entries)
    assert lg.verify(tmp_path / "ledger.jsonl", tmp_path) == []


def test_each_oracle_returns_what_its_evidence_says(blocks, tmp_path, connection):
    import pandas as pd

    (tmp_path / "toy.sysml").write_text(blocks["toy-model"][1], encoding="utf-8")
    (tmp_path / "campaign.csv").write_text(blocks["campaign-file"][1], encoding="utf-8")
    ns: dict = {"root": tmp_path}
    for name in ("toy-common", "toy-simulator", "toy-physical", "toy-human", "toy-run"):
        exec(compile(blocks[name][1], name, "exec"), ns)
    sim = pd.read_csv(tmp_path / "out" / "simulation.csv")
    assert (
        (sim.cost - (2.0 * sim.gain + sim["size"])).abs() < 1e-6
    ).all()  # the model's accounting
    assert ((sim.cost <= 10.0) == sim.affordable).all()  # the model's requirement
    assert ((sim.settle_s * sim.gain - 10.0).abs() < 1e-6).all()  # the stub measurement
    campaign = pd.read_csv(tmp_path / "campaign.csv").head(4)
    phys = pd.read_csv(tmp_path / "out" / "physical.csv")
    assert phys.cost.tolist() == campaign.cost.tolist()  # recorded, nothing simulated
    human = pd.read_csv(tmp_path / "out" / "human.csv")
    assert ((human.rating >= 3.0) == human.acceptable).all()


def test_the_oracles_satisfy_the_protocol_and_reject_unknown_configurations(
    blocks, tmp_path, connection
):
    from experiments.oracle import Oracle

    (tmp_path / "toy.sysml").write_text(blocks["toy-model"][1], encoding="utf-8")
    (tmp_path / "campaign.csv").write_text(blocks["campaign-file"][1], encoding="utf-8")
    ns: dict = {"root": tmp_path}
    for name in ("toy-common", "toy-simulator", "toy-physical", "toy-human"):
        exec(compile(blocks[name][1], name, "exec"), ns)
    assert isinstance(ns["RecordedTests"](tmp_path / "campaign.csv"), Oracle)
    assert isinstance(ns["PanelRatings"](ns["rater"]), Oracle)
    with pytest.raises(ValueError, match="no recorded test"):
        ns["RecordedTests"](tmp_path / "campaign.csv")({"gain": 99.0, "size": 99.0})


if __name__ == "__main__":
    if "--write" in sys.argv:
        sys.path.insert(0, str(ADCS))
        write_generated()
        print(textwrap.dedent(f"rewrote the generated blocks of {HOWTO}"))

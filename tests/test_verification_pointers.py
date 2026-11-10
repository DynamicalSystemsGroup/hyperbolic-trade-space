"""WP27 R-6: every verification case of ``stakeholders.sysml`` points at evidence that exists.

The model carries the pointer, the repository the evidence (WP27-decisions.md, 14:10). Each
verification case typed by ``EvidenceCase`` names a ledger entry, an entry of the environment's
record, the test that reads the evidence, and the environment that produced it. The pointers are
read from the model through the toolkit (``REQUIRE_OPENSYSML=1``), not from the text. When a gate's
re-run supersedes the entry a pointer names, this test fails until the pointer is updated in the
same unit.
"""

from __future__ import annotations

import os
import pathlib
import subprocess
import sys

import cubesat_model as cm
import pytest
from experiments import ledger as lg

ROOT = pathlib.Path(__file__).resolve().parents[1]
MODEL_DIR = ROOT / "examples" / "adcs" / "model_v2"
RECORD = ROOT / "paper" / "container" / "RECORD.md"
S = "CubesatStakeholders"
POINTERS = ("ledgerEntry", "recordEntry", "testNode", "environment")


@pytest.fixture(scope="module")
def cases() -> dict[str, dict[str, str]]:
    """Each ``EvidenceCase`` usage of the model with its four pointers, read through the toolkit."""
    text = (
        (MODEL_DIR / "cubesat.sysml").read_text()
        + "\n"
        + (MODEL_DIR / "stakeholders.sysml").read_text()
    )
    try:
        model = cm.get_connection().load_from_content(text, strict=True)
    except cm.OpenSysMLUnavailable as exc:
        flag = " (REQUIRE_OPENSYSML is set)" if os.environ.get("REQUIRE_OPENSYSML") else ""
        pytest.fail(f"the opensysml client could not start{flag}: {exc}", pytrace=False)
    out = {}
    for q in model.query(
        scope=[S], where={"property": "@type", "operator": "=", "value": "VerificationCaseUsage"}
    ):
        inst = model.instantiate(q.id)
        out[q.id.split("::")[-1]] = {k: str(inst.get(k)) for k in POINTERS}
    return out


def problems(pointers: dict[str, str]) -> list[str]:
    """What does not resolve among one case's pointers (empty when every pointer resolves)."""
    found = []
    entries = lg.read(lg.LEDGER_PATH)
    entry = next((e for e in entries if e["id"] == pointers["ledgerEntry"]), None)
    if entry is None:
        return [f"ledger entry {pointers['ledgerEntry']} not in the ledger"]
    current = lg.latest(entries, pointers["ledgerEntry"].split("@")[0])
    if current is None or current["id"] != entry["id"]:
        found.append(f"ledger entry {entry['id']} is not current ({current and current['id']})")
    record = RECORD.read_text()
    if f"## {pointers['recordEntry']}\n" not in record:
        found.append(f"no RECORD.md heading {pointers['recordEntry']!r}")
    env = pointers["environment"]
    if env == "host":
        note = (entry.get("inputs") or {}).get("note", "")
        if not entry.get("platform") or "hts-paper (image" in note:
            found.append(f"{entry['id']} is not a host entry naming its platform")
    elif not (env in record and "hts-paper" in record):
        found.append(f"image {env} is not an hts-paper image in RECORD.md")
    return found


def test_every_evidence_case_has_its_four_pointers(cases):
    assert set(cases) == {"configurationEvidence", "slewEvidence"}
    for name, ptr in cases.items():
        assert all(ptr[k] and ptr[k] != "None" for k in POINTERS), (name, ptr)


def test_every_pointer_resolves(cases):
    """R-6: the ledger entry exists and is current; the RECORD.md heading exists; the environment
    is an hts-paper image in RECORD.md, or the host and the entry's platform names it."""
    for name, ptr in cases.items():
        assert problems(ptr) == [], name


def test_every_named_test_is_collected(cases):
    """R-6: the test a case names exists (pytest collects exactly that node)."""
    for name, ptr in cases.items():
        run = subprocess.run(
            [sys.executable, "-m", "pytest", "--collect-only", "-q", "-p", "no:cacheprovider",
             ptr["testNode"]],
            cwd=ROOT, capture_output=True, text=True, check=False,
        )  # fmt: skip
        assert run.returncode == 0 and ptr["testNode"] in run.stdout, (name, run.stdout[-500:])


def test_negative_controls_an_unknown_or_superseded_entry_fails(cases):
    ptr = dict(next(iter(cases.values())))
    assert problems({**ptr, "ledgerEntry": "v2-primary@999"})
    assert problems({**ptr, "ledgerEntry": "v2-primary@5"})  # superseded by @6
    assert problems({**ptr, "recordEntry": "No such heading"})
    assert problems({**ptr, "environment": "deadbeef0000"})

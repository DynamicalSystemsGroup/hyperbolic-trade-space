"""Appendix B: proofs, step for step with their scripts (a shell until the record is delivered).

The appendix is compiled from ``derivation/proof_map_record.json``, the committed record of the
proof-map checker (the derivation implementer's deliverable). This stub reads the record when it
exists and states the tier structure; when it is absent it says so. It types no proof and no step.
"""

from __future__ import annotations

import json

from paper_common import Md
from paper_paths import ROOT

RECORD = ROOT / "derivation" / "proof_map_record.json"
PARTS = (
    ("The fit and its geometry", "L1 to L11"),
    ("The solver for K > 1 and its three levels of guarantee", "L12 to L14, stopping declaration"),
)  # fmt: skip


def _count(record) -> str:
    """A neutral count of what the record holds, whatever its container."""
    if isinstance(record, dict) and isinstance(record.get("steps"), list | dict):
        return f"{len(record['steps'])} steps"
    if isinstance(record, list | dict):
        return f"{len(record)} entries"
    return "a record"


def proof_map(path=RECORD) -> Md:
    """The state of the proof-map record and the two parts the appendix is organized in.

    Parameters
    ----------
    path : pathlib.Path, optional
        The record; default ``derivation/proof_map_record.json``.

    Returns
    -------
    Md
        The parts of the appendix and whether the record exists to compile them from.
    """
    parts = "\n".join(f"- {name} ({lemmas})" for name, lemmas in PARTS)
    if path.exists():
        held = _count(json.loads(path.read_text(encoding="utf-8")))
        state = f"The record `derivation/proof_map_record.json` holds {held}."
    else:
        state = (
            "The record `derivation/proof_map_record.json` is not delivered yet; the proofs "
            "are compiled from it when it is."
        )
    return Md(f"The appendix has two parts:\n\n{parts}\n\n{state}")

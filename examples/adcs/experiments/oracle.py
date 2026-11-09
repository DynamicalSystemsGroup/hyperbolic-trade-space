"""The oracle protocol: the configuration-to-attributes boundary, free of any modeling tool.

Nothing here imports a SysML tool. A SysML-backed simulator, a lookup of recorded physical-test
measurements and a function that collects human scores satisfy it alike; the ledger records which
kind of evidence stood behind a run (``Experiment.evidence_kind``).
"""

from __future__ import annotations

from collections.abc import Mapping
from typing import Protocol, runtime_checkable

import pandas as pd

EVIDENCE_KINDS = ("simulation", "physical-test", "human-assessment")


@runtime_checkable
class Oracle(Protocol):
    """Configuration in, attributes and flags out.

    The scenario and the gain box are fixed when the oracle is constructed, not per call. A
    configuration outside the ranges or with an unknown categorical value raises ``ValueError``
    naming the variable.
    """

    config_names: tuple[str, ...]
    attribute_names: tuple[str, ...]
    flag_names: tuple[str, ...]

    def __call__(self, configuration: Mapping[str, float | str]) -> dict[str, float | bool]:
        """One configuration to a mapping of attributes, flags and auxiliary values."""
        ...

    def evaluate(self, designs: pd.DataFrame) -> pd.DataFrame:
        """Batch form: the designs joined with their outputs, rows in ``design_id`` order."""
        ...


def evaluate_rows(oracle: Oracle, designs: pd.DataFrame) -> pd.DataFrame:
    """Reference ``evaluate``: call the oracle on every row, join the outputs to the designs.

    Columns are the design columns followed by the oracle's output keys in the order the oracle
    returns them, so an oracle whose ``__call__`` orders its keys (attributes, flags, auxiliary)
    gets that order in the file.

    >>> class Double:
    ...     config_names = ("x",)
    ...     attribute_names = ("y",)
    ...     flag_names = ("ok",)
    ...     def __call__(self, c):
    ...         return {"y": 2.0 * c["x"], "ok": True}
    >>> evaluate_rows(Double(), pd.DataFrame({"design_id": [1, 0], "x": [1.0, 2.0]})).to_dict("list")
    {'design_id': [0, 1], 'x': [2.0, 1.0], 'y': [4.0, 2.0], 'ok': [True, True]}
    """
    ordered = designs.sort_values("design_id").reset_index(drop=True)
    rows = [oracle(r.to_dict()) for _, r in ordered.iterrows()]
    return pd.concat([ordered, pd.DataFrame(rows)], axis=1)

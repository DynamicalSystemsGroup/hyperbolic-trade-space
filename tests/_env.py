"""The environment of record: where exact equality is asserted (WP10).

A few committed values are exact only where they were produced: the planted table and the data of
Figure 1 follow the operating system's maths library and the processor's floating-point
behaviour, so their hashes differ between a Mac, Linux on amd64 and Linux on arm64 although the
values agree to rounding. The container image is the environment of record. Exact equality
(hashes of generated data, byte-equal committed outputs) is asserted only when the environment
variable named by :data:`ENV_VAR` is set to ``1``; everywhere else the same quantities are compared
on their values within the tolerance stated for them in ``paper/environment_values.toml``. No test
is skipped off the environment of record.

Every exact-only assertion calls :func:`exact_only` with a name from that file, and a test
(``tests/test_paper.py``) checks that each call names a listed value and that no listed value is
unused. Setting the variable on a machine that is not the environment of record is expected to
fail for those values; the exact path is for the image.
"""

from __future__ import annotations

import os
import tomllib
from pathlib import Path

ENV_VAR = "HTS_ENVIRONMENT_OF_RECORD"
"""Name of the one environment variable that marks the environment of record (set it to ``1``)."""

VALUES_FILE = Path(__file__).resolve().parent.parent / "paper" / "environment_values.toml"
REFERENCE_FILE = VALUES_FILE.with_name("environment_reference.npz")


def of_record() -> bool:
    """Whether the process runs in the environment of record (``ENV_VAR`` is ``1``)."""
    return os.environ.get(ENV_VAR) == "1"


def listed() -> dict:
    """The values exact only in the environment of record: name -> entry of the TOML list."""
    return tomllib.loads(VALUES_FILE.read_text(encoding="utf-8"))["values"]


def exact_only(name: str) -> bool:
    """Whether the exact assertion named ``name`` applies here; the name must be in the list."""
    if name not in listed():
        raise KeyError(f"{name!r} is not in {VALUES_FILE.name}; list it with its reason first")
    return of_record()

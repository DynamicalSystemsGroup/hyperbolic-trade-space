"""The ``Experiment`` declaration.

cadCAD-like mapping, stated once
--------------------------------
An experiment reads like a cadCAD simulation configuration:

* state = a configuration (the design variables) and its measurements;
* policy = the sampler, which draws the configurations;
* state-update block = configure, measure, account (the oracle's work on one configuration);
* run = one seeded design (design ``i`` depends on ``(seed, i)`` only);
* sweep = scenario or gain-box cells, one run of the experiment and one ledger entry per cell;
* timestep = only where a flow has one (the slew simulation inside a measurement does; the
  experiment itself does not).

Where the mapping does not fit: the flow is one-shot (draw, measure, write), with no timesteps
over the experiment, no feedback from one design to the next and no state carried between
designs. The "policy" has no inputs. Physical-test and human-assessment oracles have no
simulation inside the measurement at all.
"""

from __future__ import annotations

import dataclasses
import itertools
from collections.abc import Mapping, Sequence
from dataclasses import dataclass, field
from pathlib import Path

from .oracle import EVIDENCE_KINDS

SWEEP_KEYS = ("scenario", "gain_box")


@dataclass(frozen=True)
class Experiment:
    """A declared experiment.

    Parameters
    ----------
    id : str
        Ledger identifier, unique in the ledger.
    output : str
        Output CSV path, relative to the run's root directory.
    count : int
        Number of designs drawn.
    seed : int
        Root seed; design ``i`` uses child ``i`` of ``SeedSequence(seed).spawn(count)``.
    oracle : str
        Oracle name, resolved lazily by ``definitions.resolve_oracle``.
    sampler : str or None
        Sampler name, resolved lazily like the oracle.
    scenario, gain_box : str or None
        Scenario and gain-box names, read from the model by the oracle and the sampler.
    model_path : str or None
        Model text, relative to the root; ``None`` when the oracle has none.
    model_sha256 : str or None
        Declared model hash; the runner refuses to run when the file differs.
    evidence_kind : str
        ``simulation``, ``physical-test`` or ``human-assessment``.
    code : tuple of str
        Code files that determine the output (root-relative); hashed into the entry.
    inputs : dict
        Further inputs recorded verbatim in the entry.
    parents : tuple of str
        Ledger ids whose outputs this experiment reads; their hashes are recorded before it runs.
    supersedes : tuple of str
        Earlier ledger ids this run replaces (a re-run after the model or the code changed).
    sweep : mapping or None
        ``{"scenario": [...]}`` and/or ``{"gain_box": [...]}``; one run per cell.
    """

    id: str
    output: str
    count: int
    seed: int
    oracle: str
    sampler: str | None = None
    scenario: str | None = None
    gain_box: str | None = None
    model_path: str | None = None
    model_sha256: str | None = None
    evidence_kind: str = "simulation"
    code: tuple[str, ...] = ()
    inputs: Mapping = field(default_factory=dict)
    parents: tuple[str, ...] = ()
    supersedes: tuple[str, ...] = ()
    sweep: Mapping[str, Sequence[str]] | None = None

    def __post_init__(self):
        if self.evidence_kind not in EVIDENCE_KINDS:
            raise ValueError(f"evidence_kind {self.evidence_kind!r} not in {EVIDENCE_KINDS}")
        if self.count < 1:
            raise ValueError("count must be at least 1")
        if self.sweep:
            bad = set(self.sweep) - set(SWEEP_KEYS)
            if bad:
                raise ValueError(f"sweep keys {sorted(bad)} not in {SWEEP_KEYS}")
            if any(len(v) == 0 for v in self.sweep.values()):
                raise ValueError("a sweep axis is empty")

    def expand(self) -> list[Experiment]:
        """One experiment per sweep cell (itself when there is no sweep).

        A cell sets ``scenario`` and/or ``gain_box``, takes the id ``<id>[key=value,...]`` and the
        output path with ``__key=value`` appended to the stem.

        >>> e = Experiment("e", "d/o.csv", 4, 0, "toy", sweep={"scenario": ["a", "b"]})
        >>> [(c.id, c.output) for c in e.expand()]
        [('e[scenario=a]', 'd/o__scenario=a.csv'), ('e[scenario=b]', 'd/o__scenario=b.csv')]
        """
        if not self.sweep:
            return [self]
        keys = [k for k in SWEEP_KEYS if k in self.sweep]
        cells = []
        for values in itertools.product(*(self.sweep[k] for k in keys)):
            tag = ",".join(f"{k}={v}" for k, v in zip(keys, values, strict=True))
            out = Path(self.output)
            suffix = "__" + "_".join(f"{k}={v}" for k, v in zip(keys, values, strict=True))
            cells.append(
                dataclasses.replace(
                    self,
                    id=f"{self.id}[{tag}]",
                    output=out.with_name(out.stem + suffix + out.suffix).as_posix(),
                    sweep=None,
                    **dict(zip(keys, values, strict=True)),
                )
            )
        return cells


@dataclass(frozen=True)
class AdoptedSpec:
    """A dataset made before the ledger existed, registered without regenerating it."""

    id: str
    output: str
    command: str
    model_path: str | None
    code: tuple[str, ...]
    tolerances: Mapping
    evidence_kind: str = "simulation"
    parents: tuple[str, ...] = ()
    note: str = ""

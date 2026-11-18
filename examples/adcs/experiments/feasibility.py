"""Feasibility by verification: the four flags produced by the model's own requirements (WP15 R-3).

``settled``, ``momentum_ok``, ``power_ok`` and ``dod_ok`` are not decided here. Each is the verdict
of ``verify_requirement`` on a named requirement of the model (section 5 of
``model_v2/cubesat.sysml``) for a subject configuration and, where the requirement reads one, the
measured quantity of the slew bound by name. This module holds the names of the requirements and
the translation of a measurement into the arguments the model expects; no inequality on these
quantities appears in it. The solver side (``exclusion.py``) decides regions of the space before
simulation; these verdicts, engine ``run`` with evidence ``observed``, are the observations on
single configurations after it.
"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass

from opensysml.values import Quantity

# flag -> requirement definition of the model
FLAG_REQUIREMENTS = {
    "settled": "SettledRequirement",
    "momentum_ok": "MomentumRequirement",
    "power_ok": "PowerRequirement",
    "dod_ok": "DepthOfDischargeRequirement",
}
# requirement definition -> (its `in` parameter, the measurement key, the unit it is read in)
_ARGUMENTS = {
    "SettledRequirement": ("settlingTime", "settling_time", "SI::s"),
    "MomentumRequirement": ("peakMomentum", "peak_momentum", "SI::N*SI::m*SI::s"),
    "DepthOfDischargeRequirement": ("torqueSquaredIntegral", "torque_squared_integral", None),
}


@dataclass(frozen=True)
class FlagVerdict:
    """One verdict: whether the requirement holds, with the engine and the evidence strength."""

    flag: str
    requirement: str
    holds: bool
    status: str
    engine: str
    strength: str


class FeasibilityChecker:
    """Verify the model's requirements for configurations in a loaded model.

    ``model`` is an opensysml model that contains the requirement definitions of ``package`` and
    the subjects to verify (a configuration is a ``Cubesat`` part in the same loaded text).
    """

    def __init__(self, model, package: str):
        self.model = model
        self.package = package

    def _unit(self, expression: str):
        return self.model.eval(f"1.0 [{expression}]").unit

    def _arguments(self, requirement: str, measured: Mapping | None) -> dict:
        if requirement not in _ARGUMENTS:
            return {}
        param, key, unit = _ARGUMENTS[requirement]
        if measured is None or key not in measured:
            return {}  # the model's default: the recorded baseline measurement
        value = measured[key]
        if unit is not None:
            return {param: Quantity(float(value), self._unit(unit))}
        return {param: float(value)}

    def verify(self, flag_or_requirement: str, subject: str, measured: Mapping | None = None):
        """The raw verdict of one requirement (a flag name or a requirement name)."""
        requirement = FLAG_REQUIREMENTS.get(flag_or_requirement, flag_or_requirement)
        return self.model.verify_requirement(
            f"{self.package}::{requirement}",
            subject=subject,
            named_arguments=self._arguments(requirement, measured),
        )

    def verdicts(self, subject: str, measured: Mapping | None = None) -> dict[str, FlagVerdict]:
        """The four flags' verdicts for ``subject``; ``measured`` keys: ``settling_time`` (s),
        ``peak_momentum`` (N m s), ``torque_squared_integral`` (N^2 m^2 s)."""
        out = {}
        for flag, requirement in FLAG_REQUIREMENTS.items():
            v = self.verify(requirement, subject, measured)
            out[flag] = FlagVerdict(
                flag, requirement, bool(v.holds), v.status, v.engine, v.strength
            )
        return out

    def flags(self, subject: str, measured: Mapping | None = None) -> dict[str, bool]:
        """``{flag: bool}`` for ``subject``; an undecided verdict raises (it is never ``False``)."""
        verdicts = self.verdicts(subject, measured)
        undecided = [f for f, v in verdicts.items() if v.status not in ("holds", "violated")]
        if undecided:
            raise RuntimeError(f"requirement verdict undecided for {undecided} on {subject}")
        return {flag: v.holds for flag, v in verdicts.items()}

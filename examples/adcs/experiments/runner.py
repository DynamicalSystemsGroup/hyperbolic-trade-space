"""Run an experiment and ledger it; adopt datasets made before the ledger.

No constants about any case live here: ranges, enumerations, scenarios and gain boxes arrive in the
sampler and the oracle, which read them from the model.
"""

from __future__ import annotations

from collections.abc import Callable, Mapping, Sequence
from pathlib import Path

import numpy as np
import pandas as pd

from . import ledger as lg
from .experiment import AdoptedSpec, Experiment
from .oracle import Oracle


class LogUniformSampler:
    """Sampler matching the frozen generator: one ``SeedSequence`` child seed per design.

    Design ``i`` depends only on ``(seed, i)``, not on ``count``. Categorical variables are uniform
    over their levels, drawn first in mapping order; continuous variables are log-uniform in their
    ranges, drawn next in mapping order. Columns: ``design_id``, ``seed``, categoricals,
    continuous variables.

    >>> s = LogUniformSampler({"c": ["a", "b"]}, {"x": (1.0, 10.0)})
    >>> s.draw(3, 0).iloc[0].to_dict() == s.draw(5, 0).iloc[0].to_dict()
    True
    """

    def __init__(
        self,
        categorical: Mapping[str, Sequence[str]],
        log_ranges: Mapping[str, tuple[float, float]],
    ):
        self.categorical = {k: list(v) for k, v in categorical.items()}
        self.log_ranges = {k: (float(lo), float(hi)) for k, (lo, hi) in log_ranges.items()}

    def draw(self, n: int, seed: int) -> pd.DataFrame:
        """``n`` designs for root seed ``seed``."""
        children = np.random.SeedSequence(int(seed)).spawn(n)
        child_seeds = [int(c.generate_state(1, dtype=np.uint64)[0] >> 2) for c in children]
        rows = []
        for i, cs in enumerate(child_seeds):
            g = np.random.default_rng(cs)
            row = {"design_id": i, "seed": cs}
            for name, levels in self.categorical.items():
                row[name] = levels[g.integers(len(levels))]
            for name, (lo, hi) in self.log_ranges.items():
                row[name] = float(np.exp(g.uniform(*np.log((lo, hi)))))
            rows.append(row)
        return pd.DataFrame(
            rows, columns=["design_id", "seed", *self.categorical, *self.log_ranges]
        )

    __call__ = draw


def _instance(obj, marker: str, cell: Experiment):
    """``obj`` itself when it has ``marker``; otherwise a factory called with the sweep cell."""
    return obj if hasattr(obj, marker) else obj(cell)


def _parent_records(experiment: Experiment, entries: list[dict], root: Path) -> list[dict]:
    records = []
    for pid in experiment.parents:
        pe = lg.find(entries, pid)
        if pe is None:
            raise lg.LedgerError(f"{experiment.id}: parent {pid!r} has no ledger entry yet")
        out = root / pe["output_path"]
        if not out.exists() or lg.sha256_file(out) != pe["output_sha256"]:
            raise lg.LedgerError(f"{experiment.id}: output of parent {pid!r} has drifted")
        records.append(
            {"id": pid, "entry_hash": pe["entry_hash"], "output_sha256": pe["output_sha256"]}
        )
    return records


def _check_oracle(oracle: Oracle, designs: pd.DataFrame, table: pd.DataFrame) -> None:
    missing = [c for c in oracle.config_names if c not in designs.columns]
    if missing:
        raise ValueError(f"sampler lacks the oracle's configuration columns {missing}")
    absent = [c for c in (*oracle.attribute_names, *oracle.flag_names) if c not in table.columns]
    if absent:
        raise ValueError(f"oracle output lacks declared columns {absent}")


def run(
    experiment: Experiment,
    oracle: Oracle | Callable[[Experiment], Oracle],
    sampler,
    out_dir: Path,
    ledger: Path | None = None,
) -> list[dict]:
    """Execute ``experiment`` (every sweep cell) and append one ledger entry per cell.

    Parameters
    ----------
    experiment : Experiment
        The declaration; ``output``, ``model_path`` and ``code`` resolve against ``out_dir``.
    oracle : Oracle or callable
        An oracle, or a factory taking the sweep cell (when scenario or gain box vary).
    sampler : object with ``draw(n, seed)`` or callable
        A sampler, or a factory taking the cell. ``draw`` returns designs with ``design_id``.
    out_dir : Path
        The root directory for all relative paths (the ledger records paths relative to it).
    ledger : Path, optional
        Ledger file; default ``out_dir / "ledger.jsonl"``.

    Returns
    -------
    list of dict
        The appended entries, one per cell.
    """
    root = Path(out_dir)
    ledger = Path(ledger) if ledger is not None else root / "ledger.jsonl"
    cells = experiment.expand()
    existing = {e["id"] for e in lg.read(ledger)}
    clash = [c.id for c in cells if c.id in existing]
    if clash:
        raise lg.LedgerError(f"entries {clash} exist; the ledger is append-only")
    own = [ledger, *(root / c.output for c in cells)]
    return [_run_cell(c, oracle, sampler, root, ledger, own) for c in cells]


def _run_cell(cell: Experiment, oracle, sampler, root: Path, ledger: Path, own) -> dict:
    entries = lg.read(ledger)
    parents = _parent_records(cell, entries, root)
    model_hash = None
    if cell.model_path:
        model_hash = lg.sha256_file(root / cell.model_path)
        if cell.model_sha256 and cell.model_sha256 != model_hash:
            raise lg.LedgerError(
                f"{cell.id}: model {cell.model_path} differs from its declared hash"
            )
    code = lg.hash_files(root, cell.code)
    orc = _instance(oracle, "evaluate", cell)
    smp = _instance(sampler, "draw", cell)
    designs = smp.draw(cell.count, cell.seed)
    table = orc.evaluate(designs)
    if len(table) != len(designs):
        raise ValueError(f"{cell.id}: oracle returned {len(table)} rows for {len(designs)} designs")
    _check_oracle(orc, designs, table)
    table = table.sort_values("design_id").reset_index(drop=True)
    out = root / cell.output
    out.parent.mkdir(parents=True, exist_ok=True)
    table.to_csv(out, index=False, float_format="%.9g")
    commit, dirty = lg.git_state(root, own)
    vers = lg.versions()
    runtime = getattr(orc, "runtime_info", None)
    if runtime:
        vers["runtime"] = dict(runtime)
    entry = {
        "id": cell.id,
        "kind": "generated",
        "time_utc": lg.utc_now(),
        "git_commit": commit,
        "git_dirty": dirty,
        "evidence_kind": cell.evidence_kind,
        "model_path": cell.model_path,
        "model_sha256": model_hash,
        "code": code,
        "output_path": cell.output,
        "output_rows": len(table),
        "output_sha256": lg.sha256_file(out),
        "versions": vers,
        "platform": lg.platform_string(),
        "inputs": {
            "count": cell.count,
            "seed": cell.seed,
            "scenario": cell.scenario,
            "gain_box": cell.gain_box,
            "oracle": cell.oracle,
            "sampler": cell.sampler,
            "config_names": list(orc.config_names),
            "attribute_names": list(orc.attribute_names),
            "flag_names": list(orc.flag_names),
            **dict(cell.inputs),
        },
        "parents": parents,
        "supersedes": list(cell.supersedes),
    }
    try:
        return lg.append(ledger, entry)
    except Exception:
        out.unlink(missing_ok=True)
        raise


def adopt(specs: Sequence[AdoptedSpec], root: Path, ledger: Path) -> list[dict]:
    """Append an ``adopted`` entry per spec for a dataset that already exists; never rewrite it.

    Records the output hash, the command that made it, the generating commit (newest commit that
    touched the file) and the reproducibility tolerances. Specs already in the ledger are skipped.
    """
    root = Path(root)
    done = []
    for s in specs:
        if lg.find(lg.read(ledger), s.id) is not None:
            continue
        out = root / s.output
        commit, dirty = lg.git_state(root, [ledger])
        entries = lg.read(ledger)
        entry = {
            "id": s.id,
            "kind": "adopted",
            "time_utc": lg.utc_now(),
            "git_commit": commit,
            "git_dirty": dirty,
            "evidence_kind": s.evidence_kind,
            "model_path": s.model_path,
            "model_sha256": lg.sha256_file(root / s.model_path) if s.model_path else None,
            "code": lg.hash_files(root, s.code),
            "output_path": s.output,
            "output_rows": lg.count_rows(out),
            "output_sha256": lg.sha256_file(out),
            "versions": lg.versions(),
            "platform": lg.platform_string(),
            "inputs": {
                "command": s.command,
                "generating_commit": lg.last_commit_of(root, s.output),
                "tolerances": dict(s.tolerances),
                "note": s.note,
            },
            "parents": _parent_records(
                Experiment(s.id, s.output, 1, 0, "adopted", parents=s.parents), entries, root
            ),
        }
        done.append(lg.append(ledger, entry))
    return done

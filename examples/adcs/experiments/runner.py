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
    ranges, drawn next in mapping order. Integer variables (``integer_ranges``, uniform on the
    integers of the closed range) are drawn from a generator of their own, a second stream of the
    design's child seed, so adding one moves no draw of the other variables. Columns:
    ``design_id``, ``seed``, categoricals, continuous variables, integer variables.

    >>> s = LogUniformSampler({"c": ["a", "b"]}, {"x": (1.0, 10.0)})
    >>> s.draw(3, 0).iloc[0].to_dict() == s.draw(5, 0).iloc[0].to_dict()
    True
    >>> t = LogUniformSampler({"c": ["a", "b"]}, {"x": (1.0, 10.0)}, {"k": (1, 30)})
    >>> bool((t.draw(5, 0)[["design_id", "seed", "c", "x"]] == s.draw(5, 0)).all().all())
    True
    """

    def __init__(
        self,
        categorical: Mapping[str, Sequence[str]],
        log_ranges: Mapping[str, tuple[float, float]],
        integer_ranges: Mapping[str, tuple[float, float]] | None = None,
    ):
        self.categorical = {k: list(v) for k, v in categorical.items()}
        self.log_ranges = {k: (float(lo), float(hi)) for k, (lo, hi) in log_ranges.items()}
        self.integer_ranges = {
            k: (round(lo), round(hi)) for k, (lo, hi) in (integer_ranges or {}).items()
        }

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
            if self.integer_ranges:
                own = np.random.default_rng(np.random.SeedSequence(cs, spawn_key=(1,)))
                for name, (lo, hi) in self.integer_ranges.items():
                    row[name] = float(own.integers(lo, hi + 1))
            rows.append(row)
        return pd.DataFrame(
            rows,
            columns=[
                "design_id",
                "seed",
                *self.categorical,
                *self.log_ranges,
                *self.integer_ranges,
            ],
        )

    __call__ = draw


class ExcludingSampler:
    """A sampler that never draws a design from a region the solver proved infeasible.

    Rejection on the base sampler's own stream: designs ``0, 1, 2, ...`` of ``base.draw`` are taken
    in order, a design inside any excluded region is skipped and counted, and the first ``n``
    others are returned with their original ``design_id`` and ``seed``. So the result equals the
    unexcluded sampler's draws with the excluded ones skipped, reproducibly, and with no excluded
    region it equals the base draw exactly. The flags stay observations: a region that is not
    excluded is sampled whole.

    Parameters
    ----------
    base : sampler
        Object with ``draw(n, seed)``; design ``i`` must depend only on ``(seed, i)``.
    regions : sequence of mapping
        ``exclusion.exclusion_record`` dicts (or anything with ``region.name`` and
        ``region.box``); only those with ``excluded`` true are used.
    columns : mapping
        Region variable to design column, e.g. ``{"capacity_wh": "battery_wh"}``. A region
        variable with no column (the tracker power, the slew energy) is not a design axis of the
        sampler: the region was proved over that variable's whole stated interval, which holds
        for every value the designs take, so it does not narrow the region.
    max_draws : int
        Safety cap on designs examined; exceeded only when nearly the whole space is excluded.

    Attributes
    ----------
    avoided, examined : int
        Draws skipped and designs examined by the last ``draw``.

    >>> class U:
    ...     def draw(self, n, seed):
    ...         return pd.DataFrame({"design_id": range(n), "x": [float(i) for i in range(n)]})
    >>> reg = {"excluded": True, "region": {"name": "low", "box": {"cap": [0.0, 1.5]}}}
    >>> s = ExcludingSampler(U(), [reg], {"cap": "x"})
    >>> s.draw(3, 0)["design_id"].tolist(), s.avoided
    ([2, 3, 4], 2)
    """

    def __init__(self, base, regions, columns: Mapping[str, str], max_draws: int = 100_000):
        self.base = base
        self.columns = dict(columns)
        self.max_draws = int(max_draws)
        self.regions = []
        for r in regions:
            if not _get(r, "excluded"):
                continue
            reg = _get(r, "region")
            box = {k: tuple(map(float, v)) for k, v in dict(_get(reg, "box")).items()}
            unmapped = [k for k in box if k not in self.columns]
            self.regions.append((_get(reg, "name"), box, unmapped))
        self.avoided = 0
        self.examined = 0
        self.avoided_by_region: dict[str, int] = {}

    @property
    def names(self) -> list[str]:
        return [name for name, _, _ in self.regions]

    def _inside(self, row) -> str | None:
        for name, box, _ in self.regions:
            if all(
                lo <= float(row[self.columns[k]]) <= hi
                for k, (lo, hi) in box.items()
                if k in self.columns
            ):
                return name
        return None

    def draw(self, n: int, seed: int) -> pd.DataFrame:
        """``n`` designs outside every excluded region; ``avoided`` counts the skipped draws."""
        self.avoided, self.avoided_by_region = 0, {name: 0 for name in self.names}
        if not self.regions:
            self.examined = n
            return self.base.draw(n, seed)
        m = n
        while True:
            designs = self.base.draw(m, seed)
            kept, skipped = [], {}
            for pos, (_, row) in enumerate(designs.iterrows()):
                hit = self._inside(row)
                if hit is None:
                    kept.append(pos)
                    if len(kept) == n:
                        break
                else:
                    skipped[hit] = skipped.get(hit, 0) + 1
            if len(kept) == n:
                break
            if m >= self.max_draws:
                raise ValueError(
                    f"only {len(kept)} of {n} designs lie outside the excluded regions "
                    f"after {m} draws"
                )
            m = min(m * 2, self.max_draws)
        self.examined = kept[-1] + 1
        self.avoided = sum(skipped.values())
        self.avoided_by_region.update(skipped)
        return designs.iloc[kept].reset_index(drop=True)

    __call__ = draw

    def record(self) -> dict:
        """What the last ``draw`` did, for the ledger entry."""
        return {
            "regions": self.names,
            "columns": dict(self.columns),
            "examined": self.examined,
            "avoided": self.avoided,
            "avoided_by_region": dict(self.avoided_by_region),
            "rule": (
                "rejection on the base stream: a design inside an excluded region is skipped, "
                "the first count others are kept with their original design_id and seed"
            ),
        }


def _get(obj, key):
    return obj[key] if isinstance(obj, Mapping) else getattr(obj, key)


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
    try:
        orc = _instance(oracle, "evaluate", cell)
    except Exception:
        # a factory that classified the model and proved the variant infeasible left the record in
        # the experiment's inputs; write it to the ledger before the error goes on
        block = dict(cell.inputs).get("exclusion")
        if isinstance(block, Mapping) and block.get("variant_excluded"):
            record_exclusion(cell, block, root, ledger, model_hash, code)
        raise
    smp = _instance(sampler, "draw", cell)
    sampling = None
    block = dict(cell.inputs).get("exclusion")
    skip = [r for r in (block or {}).get("regions", []) if r.get("excluded")]
    if skip and not block.get("variant_excluded"):
        columns = dict(cell.inputs).get("exclusion_columns")
        if not columns:
            raise ValueError(
                f"{cell.id}: regions {[r['region']['name'] for r in skip]} are excluded but the "
                "experiment names no inputs['exclusion_columns'] to apply them to the designs"
            )
        smp = ExcludingSampler(smp, skip, columns)
    designs = smp.draw(cell.count, cell.seed)
    if isinstance(smp, ExcludingSampler):
        sampling = smp.record()
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
            **({"excluded_sampling": sampling} if sampling else {}),
        },
        "parents": parents,
        "supersedes": list(cell.supersedes),
    }
    try:
        return lg.append(ledger, entry)
    except Exception:
        out.unlink(missing_ok=True)
        raise


def record_exclusion(
    cell: Experiment,
    block: Mapping,
    root: Path,
    ledger: Path,
    model_hash: str | None,
    code: Mapping[str, str],
) -> dict | None:
    """Append the ``exclusion`` entry for a model variant proved infeasible; nothing is simulated.

    The entry carries the variant's edits (``inputs['variant_edits']`` of the experiment, when it
    names them), the classified regions with claim, engine, verdict, strength and witnesses, the
    model hash and the reason. It has no output file. A variant already recorded (same model hash)
    is not recorded twice; ``None`` is returned then.
    """
    tag = (model_hash or block.get("model_sha256") or "unknown")[:12]
    entry_id = f"{cell.id}:exclusion@{tag}"
    entries = lg.read(ledger)
    if lg.find(entries, entry_id) is not None:
        return None
    regions = list(block.get("regions", []))
    excluded = [r for r in regions if r.get("excluded")]
    commit, dirty = lg.git_state(root, [ledger])
    entry = {
        "id": entry_id,
        "kind": "exclusion",
        "time_utc": lg.utc_now(),
        "git_commit": commit,
        "git_dirty": dirty,
        "evidence_kind": cell.evidence_kind,
        "model_path": cell.model_path,
        "model_sha256": model_hash,
        "code": dict(code),
        "output_path": None,
        "output_rows": 0,
        "output_sha256": None,
        "versions": lg.versions(),
        "platform": lg.platform_string(),
        "inputs": {
            "experiment": cell.id,
            "variant_edits": dict(dict(cell.inputs).get("variant_edits") or {}),
            "regions": regions,
            "excluded_regions": [r["region"]["name"] for r in excluded],
            "claims": [r["claim"] for r in excluded],
            "engine": block.get("engine"),
            "verdicts": dict(block.get("verdicts", {})),
            "witnesses": {
                r["region"]["name"]: {
                    "feasible": r["witness_feasible"],
                    "violation": r["witness_violation"],
                }
                for r in excluded
            },
            "model_sha256": block.get("model_sha256"),
            "reason": (
                "the solver proved no configuration of the variant feasible; "
                "no design was sampled or simulated"
            ),
        },
        "parents": [],
        "supersedes": [],
    }
    return lg.append(ledger, entry)


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

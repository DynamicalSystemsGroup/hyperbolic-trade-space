"""Appendix F: computational reproducibility, generated from the lock and the repository.

The pinned toolchain is read from ``uv.lock``, ``pyproject.toml`` and ``.python-version`` and never
typed (R-30). The row-per-item table is read from the paper's own cells (R-23, R-24). The container
paragraph is written by the container work package and is not produced here.
"""

from __future__ import annotations

import json
import platform
import re
import shutil
import subprocess
import tomllib

from paper_common import Md, md_table
from paper_paths import PAPER, ROOT

LOCK = ROOT / "uv.lock"
PYPROJECT = ROOT / "pyproject.toml"
PYTHON_VERSION = ROOT / ".python-version"
NOTEBOOKS = ("paper.ipynb", "supporting_material.ipynb")

# What a generator module reads (the "input" column of the reproduction table).
READS = {
    "generate_register": "glossary.yaml",
    "generate_prior_art": "paper/prior_art.yaml",
    "generate_gaps": "docs/superpowers/notes/abstraction-gaps.md",
    "generate_repro": "uv.lock, pyproject.toml, .python-version",
    "generate_proofs": "derivation/proof_map_record.json",
    "generate_reading_pass": "paper/reading_pass.yaml",
}
CASE_DATA = "examples/adcs/data/ (the regimes' CSV files named by the case module)"


def locked_packages(path=LOCK) -> dict[str, str]:
    """Package name to locked version, from ``uv.lock``."""
    data = tomllib.loads(path.read_text(encoding="utf-8"))
    return {p["name"]: p["version"] for p in data["package"] if "version" in p}


def lock_revision(path=LOCK) -> int:
    """The lock file's format revision."""
    return tomllib.loads(path.read_text(encoding="utf-8")).get("revision", 0)


def _name(requirement: str) -> str:
    return re.match(r"[A-Za-z0-9_.-]+", requirement).group(0).lower().replace("_", "-")


def direct_dependencies(path=PYPROJECT) -> dict[str, list[str]]:
    """Dependency names by group: ``runtime`` first, then each dependency group."""
    pp = tomllib.loads(path.read_text(encoding="utf-8"))
    out = {"runtime": [_name(r) for r in pp["project"]["dependencies"]]}
    for group, reqs in pp.get("dependency-groups", {}).items():
        out[group] = [_name(r) for r in reqs]
    return out


def _run(cmd) -> str:
    exe = shutil.which(cmd[0])
    if exe is None:
        return "not found"
    out = subprocess.run([exe, *cmd[1:]], capture_output=True, text=True, check=False, cwd=ROOT)
    return (out.stdout or out.stderr).strip().splitlines()[0] if (out.stdout or out.stderr) else ""


def toolchain() -> Md:
    """The pinned toolchain: interpreter, package manager, the packages the results rest on, commit.

    Returns
    -------
    Md
        A table of item, value and where it is pinned; the versions of packages are the lock's.
    """
    locked, deps = locked_packages(), direct_dependencies()
    pp = tomllib.loads(PYPROJECT.read_text(encoding="utf-8"))
    requires = pp["project"]["requires-python"]
    uv = re.match(r"uv \S+", _run(["uv", "--version"]))
    python = PYTHON_VERSION.read_text(encoding="utf-8").strip()
    revision = f"uv.lock (format revision {lock_revision()})"
    rows = [
        ["Python", python, f".python-version; requires-python {requires}"],
        ["Package manager", uv.group(0) if uv else "not found", revision],
        ["Locked packages", len(locked), "uv.lock"],
    ]
    for name in deps["runtime"]:
        rows.append([name, locked.get(name, "not locked"), "uv.lock; runtime dependency"])
    rows.append(
        [pp["project"]["name"], pp["project"]["version"], "pyproject.toml; this repository"]
    )
    for name in deps.get("paper", []):
        rows.append([name, locked.get(name, "not locked"), "uv.lock; dependency group paper"])
    rows.append(
        ["Node.js", _run(["node", "--version"]), "not pinned by uv.lock; MyST requires 22 or newer"]
    )
    rows.append(
        ["Interpreter of this build", platform.python_version(), "observed when the cell ran"]
    )
    rows.append(["Platform of this build", platform.platform(), "observed when the cell ran"])
    rows.append(["Commit", _run(["git", "rev-parse", "HEAD"]), "observed when the cell ran"])
    return Md(md_table(["Item", "Value", "Pinned by"], rows))


def commands() -> Md:
    """The commands that rebuild the paper and check the repository, with what a pass looks like.

    Returns
    -------
    Md
        Only commands whose target exists in the repository.
    """
    last = max(int(p.name.split("_")[1]) for p in (ROOT / "derivation").glob("lemma_*.py"))
    rows = [
        ("uv sync --locked", "install the locked environment", "exits 0"),
        ("uv lock --check", "check that the lock matches pyproject.toml", "exits 0"),
        ("uv run pytest", "run the test suite, doctests included", "all tests pass"),
        (
            "uv run python -m derivation.run",
            f"run the chain L1 to L{last}",
            "every lemma reports PASS",
        ),
    ]
    if (ROOT / "derivation" / "proofmap.py").exists():
        rows.append(
            (
                "uv run python -m derivation.proofmap",
                "check the proof map against the scripts",
                "exits 0",
            )
        )
    rows += [
        (
            "uv run python paper/execute_notebooks.py",
            "execute both notebooks from a clean kernel and write the outputs",
            "exits 0; the outputs are unchanged when the data and the seeds are",
        ),
        (
            "cd paper && uv run myst build --html",
            "build the paper as a static site, written to paper/_build/html",
            "exits 0; no error reported",
        ),
    ]
    return Md(md_table(["Command", "What it does", "A pass looks like"], rows))


def _is_import(line: str) -> bool:
    return line.startswith(("import ", "from "))


def reproduction_rows(paper_dir=PAPER) -> list[list[str]]:
    """One row per labelled figure or table cell of the two notebooks: item, call, input, output."""
    rows = []
    for nb_name in NOTEBOOKS:
        nb = json.loads((paper_dir / nb_name).read_text(encoding="utf-8"))
        for cell in nb["cells"]:
            cid = cell.get("id", "")
            if cell["cell_type"] != "code" or not cid.startswith(("fig-", "tab-")):
                continue
            src = [ln for ln in "".join(cell["source"]).splitlines() if ln and not _is_import(ln)]
            call = " ".join(src)
            mod = next((m.group(1) for ln in "".join(cell["source"]).splitlines()
                        if (m := re.match(r"from (generate_\w+) import", ln))), None)  # fmt: skip
            reads = READS.get(mod, CASE_DATA)
            rows.append([cid, f"`{call}`", reads, f"cell {cid} of {nb_name}"])
    return rows


def reproduction_table() -> Md:
    """The row-per-item table: every figure and table cell, its call, its input and its output.

    Returns
    -------
    Md
    """
    return Md(md_table(["Item", "Call", "Reads", "Writes"], reproduction_rows()))

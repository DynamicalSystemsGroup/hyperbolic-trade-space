"""WP14 (R-1 to R-12): the interface contract, asserted against the repository.

``work-packages/interface-contract.toml`` is the single source of the pinned facts. This
module asserts the manifest against the repository and
``work-packages/interface-contract.md`` against it.
Offline, no kernel, no site or paper build; standard library plus what is locked.

Every assertion message reads ``[contract R-n] <what> (side: <side>; change by amendment,
work-packages/interface-contract.md)``. A clause whose delivering file does not exist yet is skipped
with the reason recorded in the manifest (``[skips.*]``) and enforced once the file exists.
"""

import contextlib
import dataclasses
import importlib
import importlib.util
import inspect
import re
import tomllib
from collections.abc import Mapping
from pathlib import Path
from typing import Protocol, runtime_checkable

import pandas as pd
import pytest
from packaging.version import Version

ROOT = Path(__file__).resolve().parent.parent
MANIFEST_PATH = ROOT / "work-packages" / "interface-contract.toml"
DOC_PATH = ROOT / "work-packages" / "interface-contract.md"

MAN = tomllib.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
DOC = DOC_PATH.read_text(encoding="utf-8")

# The modeling-tool words the contract and the package surface must not carry (R-3a). The longer
# word contains the shorter one; both are listed so a failure message can name which was found.
FORBIDDEN = ("opensysml", "sysml")

AMEND = "change by amendment, work-packages/interface-contract.md"


def msg(rule: str, what: str, side: str = "technical") -> str:
    return f"[contract {rule}] {what} (side: {side}; {AMEND})"


def _skip_unless_delivered(key: str) -> None:
    """Skip the clause named by ``[skips.<key>]`` until its file exists."""
    s = MAN["skips"][key]
    if not (ROOT / s["file"]).exists():
        pytest.skip(f"[contract] {s['clause']}: {s['reason']} (file {s['file']} not yet present)")


def _read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


def _sig_names(obj) -> list[str]:
    return list(inspect.signature(obj).parameters)


# -----------------------------------------------------------------------------------------------
# Document helpers
# -----------------------------------------------------------------------------------------------
def _section(number: int) -> str:
    m = re.search(rf"^## {number}\. .*?$(.*?)(?=^## \d+\. |\Z)", DOC, re.S | re.M)
    assert m, msg("R-8", f"document lacks section {number}", "both")
    return m.group(1)


def _table_rows(text: str) -> list[list[str]]:
    rows = []
    for line in text.splitlines():
        if not line.startswith("|"):
            continue
        cells = [c.strip().replace("`", "") for c in line.strip().strip("|").split("|")]
        if set("".join(cells)) <= set("-: "):
            continue
        rows.append(cells)
    return rows[1:]  # drop the header row


def _flatten(d: Mapping, prefix: str = "") -> dict[str, object]:
    out: dict[str, object] = {}
    for k, v in d.items():
        key = f"{prefix}{k}"
        if isinstance(v, Mapping):
            out.update(_flatten(v, key + "."))
        else:
            out[key] = v
    return out


_STOP = {"a", "an", "the", "of", "and", "is", "are", "to", "in"}


def _tokens(s: str) -> set[str]:
    return {t for t in re.findall(r"[a-z0-9_.]+", s.lower().replace("`", "")) if t not in _STOP}


def _wps(s: str) -> set[str]:
    return set(re.findall(r"WP\d+[ab]?", s))


# -----------------------------------------------------------------------------------------------
# R-8 change control, and the document quoting the manifest
# -----------------------------------------------------------------------------------------------
def test_r8_contract_version_matches_document_and_change_log():
    version = MAN["contract_version"]
    assert isinstance(version, int) and version >= 1, msg(
        "R-8", "contract_version is an integer >= 1", "both"
    )
    m = re.search(r"^Contract version (\d+)\.", DOC, re.M)
    assert m, msg("R-8", "document states 'Contract version N.'", "both")
    assert int(m.group(1)) == version, msg(
        "R-8", f"document version {m.group(1)} differs from manifest {version}", "both"
    )
    rows = [r for r in _table_rows(_section(14)) if r and r[0].isdigit()]
    numbers = [int(r[0]) for r in rows]
    assert numbers == list(range(1, version + 1)), msg(
        "R-8",
        f"change log rows {numbers} must be one per version 1..{version}, last equals the version",
        "both",
    )


def test_r8_document_quotes_the_manifest():
    m = re.search(r"^## 2\. Quoted from the manifest.*?```toml\n(.*?)```", DOC, re.S | re.M)
    assert m, msg("R-8", "document section 2 holds a toml block of quoted facts", "both")
    quoted = _flatten(tomllib.loads(m.group(1)))
    assert quoted, msg("R-8", "the quoted block is empty", "both")
    manifest = _flatten(MAN)
    for key, value in quoted.items():
        assert key in manifest, msg("R-8", f"quoted key {key!r} is not in the manifest", "both")
        assert manifest[key] == value, msg(
            "R-8", f"quoted {key} = {value!r} differs from manifest {manifest[key]!r}", "both"
        )


def test_r8_floor_pinned_lists_in_the_document_are_not_lost():
    # Floor rule: the quoted block is asserted equal above, so the manifest grows only together
    # with the document; sorted order makes an addition visible in review.
    assert MAN["package"]["public_names"] == sorted(MAN["package"]["public_names"]), msg(
        "R-8", "package.public_names is kept sorted so additions are visible in review", "both"
    )


def test_r11_skip_and_gap_lists_match_the_manifest():
    skips = list(MAN["skips"].values())
    doc_skips = _table_rows(_section(18))
    assert len(doc_skips) == len(skips), msg(
        "R-5", f"document skip list has {len(doc_skips)} rows, manifest {len(skips)}", "both"
    )
    for row, s in zip(doc_skips, skips, strict=True):
        clause, file, reason, closed_by = row[:4]
        assert (clause, file, closed_by) == (s["clause"], s["file"], s["closed_by"]), msg(
            "R-5", f"skip row {row} differs from the manifest {s}", "both"
        )
        assert _tokens(reason) <= _tokens(s["reason"]), msg(
            "R-5", f"skip reason {reason!r} says more than the manifest {s['reason']!r}", "both"
        )
    gaps = list(MAN["gaps"].values())
    doc_gaps = _table_rows(_section(17))
    assert len(doc_gaps) == len(gaps), msg(
        "R-11", f"document gap list has {len(doc_gaps)} rows, manifest {len(gaps)}", "both"
    )
    for row, g in zip(doc_gaps, gaps, strict=True):
        assert _tokens(row[0]) <= _tokens(g["what"]), msg(
            "R-11", f"gap {row[0]!r} differs from the manifest {g['what']!r}", "both"
        )
        assert _wps(row[1]) == _wps(g["closed_by"]), msg(
            "R-11",
            f"gap closing package {row[1]!r} differs from manifest {g['closed_by']!r}",
            "both",
        )
        assert g["closed_by"].strip(), msg("R-11", "every gap names the closing package", "both")


def test_r9_ownership_table_in_document_lists_every_non_technical_path():
    section = _section(16)
    for side, spec in MAN["ownership"].items():
        if side in {"technical", "rule", "carve_outs"}:
            continue
        for p in spec["paths"]:
            assert f"`{p}`" in section, msg(
                "R-9", f"path {p!r} of side {side!r} is missing from document section 16", "both"
            )


# -----------------------------------------------------------------------------------------------
# R-1 package surface, R-2 version
# -----------------------------------------------------------------------------------------------
PKG = MAN["package"]


def _pkg():
    return importlib.import_module(PKG["import_name"])


def test_r1_names_and_distribution():
    assert (
        PKG["import_name"] == "hyperbolic_trade_space"
        and PKG["distribution_name"] == "hyperbolic-trade-space"
    ), msg("R-1", "import and distribution names are pinned")
    assert (ROOT / PKG["src_dir"] / "__init__.py").is_file(), msg(
        "R-1", f"{PKG['src_dir']} holds the package"
    )
    project = tomllib.loads(_read("pyproject.toml"))["project"]
    assert project["name"] == PKG["distribution_name"], msg(
        "R-1", "pyproject [project].name is the distribution name"
    )


def test_r1_public_names_in_all_and_importable():
    pkg = _pkg()
    for name in PKG["public_names"]:
        assert name in pkg.__all__, msg("R-1", f"public name {name!r} must be in __all__ (floor)")
        assert hasattr(pkg, name), msg(
            "R-1", f"public name {name!r} must be importable from the package"
        )


@pytest.mark.parametrize("sub", PKG["submodules"])
def test_r1_submodule_importable_with_pinned_names(sub):
    try:
        mod = importlib.import_module(f"{PKG['import_name']}.{sub}")
    except ImportError as exc:  # pragma: no cover - failure path
        pytest.fail(msg("R-1", f"submodule {sub!r} must be importable: {exc}"))
    for name in PKG["submodule_names"].get(sub, []):
        assert hasattr(mod, name), msg(
            "R-1", f"{PKG['import_name']}.{sub} must provide {name!r} (floor)"
        )


def test_r1_submodule_names_table_covers_only_pinned_submodules():
    unknown = set(PKG["submodule_names"]) - set(PKG["submodules"])
    assert not unknown, msg(
        "R-1", f"submodule_names lists unpinned submodules {sorted(unknown)}", "both"
    )


def test_r1_tolerances_pinned():
    solvers = importlib.import_module(f"{PKG['import_name']}.solvers")
    for name, value in PKG["tolerances"].items():
        assert getattr(solvers, name) == value, msg("R-1", f"solvers.{name} must equal {value!r}")


def test_r1_certificate_signatures_exact():
    solvers = importlib.import_module(f"{PKG['import_name']}.solvers")
    for fn, names in PKG["signatures"]["solvers"].items():
        assert _sig_names(getattr(solvers, fn)) == names, msg(
            "R-1", f"solvers.{fn} parameter names must be exactly {names}"
        )


def test_r1_termination_fields_statuses_and_report_fields():
    est = PKG["estimator"]
    mod_name, _, cls_name = est["termination_class"].rpartition(".")
    term = getattr(importlib.import_module(mod_name), cls_name)
    fields = {f.name for f in dataclasses.fields(term)}
    missing = set(est["termination_fields"]) - fields
    assert not missing, msg("R-1", f"Termination lacks fields {sorted(missing)} (floor)")
    doc = term.__doc__ or ""
    absent = [s for s in est["termination_statuses"] if f'``"{s}"``' not in doc]
    assert not absent, msg("R-1", f"Termination statuses {absent} are not documented on the record")
    mod_name, _, cls_name = est["report_class"].rpartition(".")
    rep = getattr(importlib.import_module(mod_name), cls_name)
    missing = set(est["report_fields"]) - {f.name for f in dataclasses.fields(rep)}
    assert not missing, msg("R-1", f"TensionReport lacks fields {sorted(missing)} (floor)")


def test_r1_estimator_methods_and_fitted_attributes():
    import numpy as np

    pkg = _pkg()
    est_spec = PKG["estimator"]
    cls = getattr(pkg, est_spec["class"])
    for method in est_spec["methods"]:
        assert callable(getattr(cls, method, None)), msg(
            "R-1", f"{est_spec['class']}.{method} must exist"
        )
    X, _ = pkg.make_frontier_data(60, 3, random_state=0)
    fitted = cls(temperature=5.0).fit(np.asarray(X))
    for attr in est_spec["fitted_attributes"]:
        assert hasattr(fitted, attr), msg("R-1", f"fitted attribute {attr!r} must exist after fit")
    assert isinstance(
        fitted.termination_, importlib.import_module("hyperbolic_trade_space.solvers").Termination
    ), msg("R-1", "termination_ is a Termination record")


def test_r1_docstring_style_pinned():
    assert PKG["docstrings"]["style"] == "numpydoc", msg(
        "R-1", "docstring style is numpydoc (OD2 source)", "both"
    )
    for name in ("HyperbolicTradeSpace", "select_temperature", "tension_report"):
        doc = inspect.getdoc(getattr(_pkg(), name)) or ""
        assert "----------" in doc or "Parameters" in doc or "Returns" in doc, msg(
            "R-1", f"{name} carries a numpydoc docstring (the API reference source)", "both"
        )


def test_r2_version_one_authority_pep440():
    pyproject = tomllib.loads(_read("pyproject.toml"))
    declared = pyproject["project"]["version"]
    pkg = _pkg()
    assert declared == pkg.__version__, msg(
        "R-2", f"pyproject version {declared!r} != __version__ {pkg.__version__!r}"
    )
    parsed = Version(declared)  # raises InvalidVersion if not PEP 440
    assert str(parsed) == declared and len(parsed.release) == 3, msg(
        "R-2", f"version {declared!r} must be PEP 440 MAJOR.MINOR.PATCH"
    )
    assert declared == PKG["version"], msg(
        "R-2",
        f"manifest version {PKG['version']!r} must equal {declared!r}; a bump edits both together",
        "both",
    )
    assert "pyproject.toml [project].version" in PKG["version_sources"], msg(
        "R-2", "pyproject is a version source"
    )
    assert PKG["version_changed_by"] == "WP8b", msg("R-2", "only WP8b changes the version", "both")


# -----------------------------------------------------------------------------------------------
# R-3a the boundary
# -----------------------------------------------------------------------------------------------
BOUNDARY = MAN["boundary"]


@runtime_checkable
class Oracle(Protocol):
    """The protocol of the document (section 3), restated for the toy below."""

    config_names: tuple[str, ...]
    attribute_names: tuple[str, ...]
    flag_names: tuple[str, ...]

    def __call__(self, configuration: Mapping[str, float | str]) -> dict[str, float | bool]: ...

    def evaluate(self, designs: pd.DataFrame) -> pd.DataFrame: ...


class ToyOracle:
    """A pure-Python oracle: two numeric configuration variables, two attributes, one flag."""

    config_names = ("x1", "x2")
    attribute_names = ("cost", "speed")
    flag_names = ("feasible",)

    def __call__(self, configuration):
        for name in self.config_names:
            if name not in configuration or not 0.0 < float(configuration[name]) <= 10.0:
                raise ValueError(f"configuration variable {name!r} is missing or out of range")
        x1, x2 = float(configuration["x1"]), float(configuration["x2"])
        return {"cost": x1 + 2.0 * x2, "speed": 10.0 / (1.0 + x1 * x2), "feasible": x1 + x2 < 12.0}

    def evaluate(self, designs):
        designs = designs.sort_values("design_id")
        rows = [self({k: r[k] for k in self.config_names}) for _, r in designs.iterrows()]
        out = pd.DataFrame(rows, index=designs.index)
        return pd.concat([designs[["design_id", *self.config_names]], out], axis=1).reset_index(
            drop=True
        )


def test_r3a_boundary_text_and_protocol_members():
    b = BOUNDARY["oracle"]
    for member in ("config_names", "attribute_names", "flag_names"):
        assert member in DOC, msg("R-3a", f"document states Oracle member {member!r}", "both")
    assert b["call"] in DOC and b["evaluate"] in DOC, msg(
        "R-3a", "document states __call__ and evaluate verbatim", "both"
    )
    assert BOUNDARY["identifier_columns"] == ["design_id", "seed"], msg(
        "R-3a", "identifier columns pinned", "both"
    )
    assert BOUNDARY["column_kinds"] == ["configuration", "attribute", "flag", "identifier"], msg(
        "R-3a", "table column kinds pinned", "both"
    )
    assert b["deterministic"] is True and b["batch_order"] == "rows in design_id order", msg(
        "R-3a", "oracle is deterministic and batch rows are in design_id order", "both"
    )


def test_r3a_toy_oracle_satisfies_protocol_and_table_shape():
    oracle = ToyOracle()
    assert isinstance(oracle, Oracle), msg("R-3a", "the toy satisfies the Oracle protocol")
    row = oracle({"x1": 1.0, "x2": 2.0})
    assert set(row) == set(oracle.attribute_names) | set(oracle.flag_names), msg(
        "R-3a", "__call__ returns the attributes and flags as keys"
    )
    assert oracle({"x1": 1.0, "x2": 2.0}) == row, msg("R-3a", "the oracle is deterministic")
    with pytest.raises(ValueError, match="x2"):
        oracle({"x1": 1.0, "x2": -1.0})
    designs = pd.DataFrame({"design_id": [2, 0, 1], "x1": [3.0, 1.0, 2.0], "x2": [1.0, 2.0, 2.0]})
    table = oracle.evaluate(designs)
    assert list(table["design_id"]) == [0, 1, 2], msg("R-3a", "batch rows come in design_id order")
    expected = ["design_id", *oracle.config_names, *oracle.attribute_names, *oracle.flag_names]
    assert list(table.columns) == expected, msg(
        "R-3a", "batch output has identifier, configuration, attribute, flag columns"
    )
    assert all(pd.api.types.is_float_dtype(table[c]) for c in oracle.attribute_names), msg(
        "R-3a", "attributes are float"
    )
    assert all(pd.api.types.is_bool_dtype(table[c]) for c in oracle.flag_names), msg(
        "R-3a", "flags are bool"
    )


def test_r3a_frozen_cubesat_pair():
    cubesat = importlib.import_module("cubesat_model")
    for fn, names in BOUNDARY["cubesat_instance"]["signatures"].items():
        assert _sig_names(getattr(cubesat, fn)) == names, msg(
            "R-3a", f"cubesat_model.{fn} parameter names must be exactly {names}"
        )
    assert (
        BOUNDARY["cubesat_instance"]["signatures"] == MAN["case"]["signatures"]["cubesat_model"]
    ), msg("R-3a", "the boundary and case tables agree on the frozen pair", "both")


def test_r3a_oracle_protocol_clause_until_wp15():
    _skip_unless_delivered("oracle_protocol")
    assert "class Oracle" in _read(MAN["skips"]["oracle_protocol"]["file"]), msg(
        "R-3a", "the delivered module defines the Oracle protocol"
    )


def test_r3a_no_modeling_tool_words_in_contract_text_or_public_surface():
    scanned = {rel: _read(rel).lower() for rel in BOUNDARY["scan_files"]}
    assert "work-packages/interface-contract.md" in scanned, msg(
        "R-3a", "the document is scanned", "both"
    )
    pkg = _pkg()
    surface = []
    for name in pkg.__all__:
        obj = getattr(pkg, name)
        surface.append(name)
        if callable(obj):
            with contextlib.suppress(TypeError, ValueError):
                surface.append(f"{name}{inspect.signature(obj)}")
    scanned["package __all__ and public signatures"] = "\n".join(surface).lower()
    for where, text in scanned.items():
        for word in FORBIDDEN:
            assert word not in text, msg(
                "R-3a", f"{word!r} (modeling-tool word) found in {where}", "both"
            )


# -----------------------------------------------------------------------------------------------
# R-3 case modules and data
# -----------------------------------------------------------------------------------------------
CASE = MAN["case"]


def test_r3_pythonpath_and_directory():
    cfg = tomllib.loads(_read("pyproject.toml"))["tool"]["pytest"]["ini_options"]
    assert cfg["pythonpath"] == CASE["pythonpath"], msg(
        "R-3", f"pyproject pythonpath must be {CASE['pythonpath']}"
    )
    for mod in CASE["modules"]:
        assert (ROOT / CASE["dir"] / f"{mod}.py").is_file(), msg(
            "R-3", f"case module {mod}.py under {CASE['dir']}"
        )


@pytest.mark.parametrize("module", list(CASE["signatures"]))
def test_r3_case_functions_and_parameter_names(module):
    mod = importlib.import_module(module)
    for fn, names in CASE["signatures"][module].items():
        assert callable(getattr(mod, fn, None)), msg("R-3", f"{module}.{fn} must exist")
        assert _sig_names(getattr(mod, fn)) == names, msg(
            "R-3", f"{module}.{fn} parameter names must be exactly {names}"
        )


def test_r3_regimes_and_files():
    k_terms = importlib.import_module("k_terms")
    assert list(k_terms.REGIMES) == CASE["regimes"], msg(
        "R-3", f"k_terms.REGIMES keys must be {CASE['regimes']}"
    )
    assert dict(k_terms.REGIMES) == CASE["regime_files"], msg(
        "R-3", "regime to data-file mapping is pinned"
    )


_DTYPE_CHECK = {
    "int": pd.api.types.is_integer_dtype,
    "float": pd.api.types.is_float_dtype,
    "bool": pd.api.types.is_bool_dtype,
    "str": lambda s: pd.api.types.is_object_dtype(s) or pd.api.types.is_string_dtype(s),
}


@pytest.mark.parametrize("filename", list(CASE["data"]))
def test_r3_data_file_header_dtypes_rows(filename):
    spec = CASE["data"][filename]
    path = ROOT / CASE["frozen_data_dir"] / filename
    assert path.is_file(), msg("R-3", f"data file {path.relative_to(ROOT)} must exist")
    df = pd.read_csv(path)
    assert list(df.columns) == list(spec["columns"]), msg(
        "R-3", f"{filename} header must match the pinned order"
    )
    for col, kind in spec["columns"].items():
        assert _DTYPE_CHECK[kind](df[col]), msg(
            "R-3", f"{filename}:{col} must be {kind}, found {df[col].dtype}"
        )
    assert len(df) == spec["rows"], msg(
        "R-3", f"{filename} must keep {spec['rows']} rows (frozen), found {len(df)}"
    )


@pytest.mark.parametrize("filename", list(CASE["v2"]["data"]))
def test_r3_v2_data_file_header_dtypes_rows(filename):
    """Amendment 12: the v2 files carry the frozen header less the slew-time columns."""
    spec = CASE["v2"]["data"][filename]
    path = ROOT / CASE["v2"]["dir"] / filename
    assert path.is_file(), msg("R-3", f"v2 data file {path.relative_to(ROOT)} must exist")
    df = pd.read_csv(path)
    assert list(df.columns) == list(spec["columns"]), msg(
        "R-3", f"v2 {filename} header must match the pinned order"
    )
    for col, kind in spec["columns"].items():
        assert _DTYPE_CHECK[kind](df[col]), msg(
            "R-3", f"v2 {filename}:{col} must be {kind}, found {df[col].dtype}"
        )
    assert len(df) == spec["rows"], msg(
        "R-3", f"v2 {filename} must keep {spec['rows']} rows, found {len(df)}"
    )
    frozen = CASE["data"][filename]["columns"]
    gone = {"slew_time_s", "slew_time_05deg_s"}
    rename = {"pred_std_slew_time_s": "pred_std_settling_time_s"}
    assert list(spec["columns"]) == [rename.get(c, c) for c in frozen if c not in gone], msg(
        "R-3", f"v2 {filename} pins the frozen columns less the slew-time columns, in order"
    )


def test_r3_v2_traded_metrics_are_the_oracles_attribute_names():
    """Amendment 12: the nine traded metrics of the v2 data are the case oracle's attributes."""
    oracle = importlib.import_module("experiments.cubesat_oracle")
    assert list(CASE["v2"]["traded_metrics"]) == list(oracle.ATTRIBUTE_NAMES), msg(
        "R-3", "case.v2.traded_metrics equals experiments.cubesat_oracle.ATTRIBUTE_NAMES"
    )
    assert CASE["v2"]["time_metric"] in CASE["v2"]["traded_metrics"]
    assert CASE["v2"]["settling_time_method"] == "events"


def test_r3_primary_and_stock_files_are_pinned_data():
    assert set(CASE["regime_files"].values()) <= set(CASE["data"]), msg(
        "R-3", "regime files carry data schemas"
    )


@pytest.fixture(scope="module")
def smoke(tmp_path_factory):
    import time

    k_terms = importlib.import_module("k_terms")
    t0 = time.perf_counter()
    out = k_terms.run_regime(
        CASE["regimes"][0], seeds=[0], figs=tmp_path_factory.mktemp("figs"), verbose=False
    )
    return out, time.perf_counter() - t0


@pytest.mark.slow
def test_r3_k_terms_smoke_run(smoke):
    out, seconds = smoke
    assert {"fits", "reports", "taus"} <= set(out), msg(
        "R-3", "run_regime returns fits, reports and taus"
    )
    assert set(out["fits"]) == {1, 2, 3}, msg("R-3", "run_regime fits K = 1, 2, 3")
    assert seconds < 120, msg("R-3", f"smoke run took {seconds:.0f}s: keep the contract test fast")


# -----------------------------------------------------------------------------------------------
# R-4 figures
# -----------------------------------------------------------------------------------------------
FIG = CASE["figures"]
PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"


@pytest.mark.parametrize("name", FIG["files"])
def test_r4_pinned_figure_is_a_valid_png(name):
    path = ROOT / FIG["dir"] / name
    assert path.is_file(), msg(
        "R-4", f"figure {path.relative_to(ROOT)} must exist (read-only for presentation)"
    )
    assert any(re.match(p, name) for p in FIG["patterns"]), msg(
        "R-4", f"{name} must match a pinned naming pattern"
    )
    with path.open("rb") as fh:
        assert fh.read(8) == PNG_SIGNATURE, msg("R-4", f"{name} must be a valid PNG")


def test_r4_directory_holds_only_pinned_naming_and_producers_exist():
    for path in (ROOT / FIG["dir"]).glob("*.png"):
        assert any(re.match(p, path.name) for p in FIG["patterns"]), msg(
            "R-4", f"{path.name} does not match the pinned figure naming {FIG['patterns']}"
        )
    assert (ROOT / FIG["produced_by_numbered"]).is_file(), msg(
        "R-4", "the notebook producing 01_ to 09_ exists"
    )
    assert FIG["produced_by_k3"] == CASE["producing_command"], msg(
        "R-4", "k3 figures come from the producing command"
    )
    script = ROOT / CASE["producing_command"].rsplit(" ", 1)[1]
    assert script.is_file() and '__name__ == "__main__"' in script.read_text(encoding="utf-8"), msg(
        "R-4", "the producing script has a CLI entry"
    )
    assert callable(importlib.import_module("k_terms").main), msg("R-4", "k_terms.main exists")


# -----------------------------------------------------------------------------------------------
# R-5 derivation ledger
# -----------------------------------------------------------------------------------------------
DER = MAN["derivation"]


def test_r5_run_module_chain_ordered_and_numbering_contiguous():
    run = importlib.import_module(DER["run_module"])
    for attr in DER["run_attributes"]:
        assert hasattr(run, attr), msg("R-5", f"{DER['run_module']}.{attr} must exist")
    axioms = importlib.import_module(DER["axioms_module"])
    for attr in DER["axioms_attributes"]:
        assert hasattr(axioms, attr), msg("R-5", f"{DER['axioms_module']}.{attr} must exist")
    assert run.CHAIN, msg("R-5", "CHAIN is non-empty")
    assert len(run.CHAIN_NAMES) >= DER["chain_length"], msg(
        "R-5", f"CHAIN_NAMES has >= {DER['chain_length']} lemmas (floor)"
    )
    numbers = [run.lemma_number(m) for m in run.CHAIN]
    assert numbers == sorted(numbers) and len(set(numbers)) == len(numbers), msg(
        "R-5", "CHAIN is ordered without duplicates"
    )
    pattern = re.compile(DER["module_pattern"])
    files = sorted(p.stem for p in (ROOT / DER["dir"]).glob("lemma_*.py"))
    bad = [f for f in files if not pattern.match(f)]
    assert not bad, msg("R-5", f"lemma modules {bad} do not match {DER['module_pattern']}")
    file_numbers = [int(pattern.match(f).group(1)) for f in files]
    assert file_numbers == list(range(1, len(files) + 1)), msg(
        "R-5", f"lemma numbering must be contiguous from 1 without duplicates, found {file_numbers}"
    )
    assert [pattern.match(n) is not None for n in run.CHAIN_NAMES] == [True] * len(
        run.CHAIN_NAMES
    ), msg("R-5", "every CHAIN_NAMES entry matches the module pattern")
    assert list(run.CHAIN_NAMES) == files[: len(run.CHAIN_NAMES)], msg(
        "R-5", "CHAIN_NAMES lists the lemma files in order"
    )


def test_r5_entry_command_and_generated_pages_names():
    assert DER["entry_cmd"] == "uv run python derivation/run.py", msg(
        "R-5", "entry command is pinned"
    )
    assert (ROOT / DER["entry_cmd"].rsplit(" ", 1)[1]).is_file(), msg(
        "R-5", "the entry script exists"
    )
    assert DER["entry_cmd"] in DOC, msg("R-5", "document states the entry command", "both")
    assert DER["generated_dir"] == "build/generated/" and DER["generated_pages"] == [
        "derivations.md",
        "verification.md",
    ], msg("R-5", "generated page names and location are pinned (names, not prose)", "both")
    assert not DER["generated_dir"].startswith(MAN["docs"]["dir"]), msg(
        "R-5", "derivations and verification are outside docs/ (the paper's build, not the docsite)"
    )
    ignore = _read(".gitignore").splitlines()
    assert "build/" in ignore and MAN["docs"]["generated_dir"] in ignore, msg(
        "R-5", "build/ and docs/generated/ are git-ignored, never committed", "presentation"
    )


def test_r5_generated_pages_script():
    text = _read(DER["generated_by"])
    for page in DER["generated_pages"] + DOCS["generated_pages"]:
        assert page in text, msg("R-5", f"{DER['generated_by']} must write {page}", "presentation")
    assert DOCS["generated_by"] == DER["generated_by"]
    assert '"build" / "generated"' in text and '"docs" / "generated"' in text, msg(
        "R-5",
        "script writes build/generated/ (paper) and docs/generated/ (glossary)",
        "presentation",
    )


def test_r6_glossary_source_and_paper_sources_pinned():
    assert (ROOT / DOCS["glossary_source"]).is_file(), msg(
        "R-6", "glossary.yaml is the single source of the Glossary", "presentation"
    )
    assert DOCS["glossary_source"] in MAN["ownership"]["wp8a"]["paths"]
    assert (ROOT / DOCS["paper_sources_dir"]).is_dir(), msg(
        "R-6", "the paper-sources directory exists", "both"
    )
    assert MAN["ownership"]["carve_outs"][DOCS["paper_sources_dir"]] == "wp8a"
    assert DOCS["generated_pages"] == ["glossary.md"] and DOCS["generated_dir"] == "docs/generated/"


# -----------------------------------------------------------------------------------------------
# R-6 documentation sources
# -----------------------------------------------------------------------------------------------
DOCS = MAN["docs"]


def _references_helper():
    spec = importlib.util.spec_from_file_location(
        "_contract_test_references", ROOT / "tests" / "test_references.py"
    )
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _check_citations(rel: str, bib_keys: set[str], helper, side: str) -> None:
    cited = helper._cited_keys(_read(rel))
    unknown = cited - bib_keys
    assert not unknown, msg(
        "R-6", f"{rel} cites keys missing from {DOCS['bibliography']}: {sorted(unknown)}", side
    )


@pytest.mark.parametrize("page", DOCS["pages"])
def test_r6_pinned_page_exists_and_citations_resolve(page):
    rel = f"{DOCS['dir']}{page}"
    assert page.endswith(".md") and (ROOT / rel).is_file(), msg(
        "R-6", f"pinned page {rel} must exist and be Markdown", "presentation"
    )
    helper = _references_helper()
    keys = {e["key"] for e in helper.parse_bib(_read(DOCS["bibliography"]))}
    _check_citations(rel, keys, helper, "presentation")


def test_r6_syntax_helper_and_notes_pinned():
    assert (ROOT / DOCS["bibliography"]).is_file(), msg("R-6", "the bibliography exists")
    assert (ROOT / DOCS["helper"]).is_file(), msg("R-6", "the citation helper test exists")
    assert DOCS["notes_in_navigation"] is False and (ROOT / DOCS["notes_dir"]).is_dir(), msg(
        "R-6", "notes exist and stay out of navigation", "both"
    )
    assert (DOCS["citation_syntax"], DOCS["math_inline"], DOCS["math_display"]) == (
        "[@key]",
        "$...$",
        "$$...$$",
    ), msg("R-6", "citation and math syntax are pinned", "both")


def test_r6_api_reference_page():
    rel = DOCS["api_reference_page"]
    assert rel.endswith(".md") and rel in DOCS["presentation_pages"], msg(
        "R-6", f"{rel} is a presentation-owned page", "presentation"
    )
    helper = _references_helper()
    keys = {e["key"] for e in helper.parse_bib(_read(DOCS["bibliography"]))}
    _check_citations(rel, keys, helper, "presentation")


def test_r6_no_technical_path_in_a_presentation_set():
    technical = MAN["ownership"]["technical"]["paths"]
    assert DOCS["presentation_pages"] == [f"{DOCS['dir']}{p}" for p in DOCS["pages"]] + [
        DOCS["api_reference_page"]
    ], msg("R-6", "presentation_pages is the pinned pages plus the API reference", "both")
    for page in DOCS["pages"]:
        rel = f"{DOCS['dir']}{page}"
        owner = [
            s
            for s, spec in MAN["ownership"].items()
            if isinstance(spec, dict) and any(_overlap(rel, q) for q in spec.get("paths", []))
        ]
        assert owner == ["wp8a"], msg(
            "R-6", f"pinned page {rel} must have WP8a as its only owner, found {owner}", "both"
        )
    for p in DOCS["presentation_pages"]:
        assert any(_overlap(p, q) for q in MAN["ownership"]["wp8a"]["paths"]), msg(
            "R-6", f"presentation page {p} belongs to WP8a", "presentation"
        )
        assert not any(_overlap(p, t) for t in technical), msg(
            "R-6", f"presentation page {p} lies in the technical side's set", "both"
        )


# -----------------------------------------------------------------------------------------------
# R-7 build and publish interface
# -----------------------------------------------------------------------------------------------
BUILD = MAN["build"]


def test_r7_dependency_groups_and_default_groups():
    pyproject = tomllib.loads(_read("pyproject.toml"))
    groups = set(pyproject["dependency-groups"])
    missing = set(BUILD["dependency_groups_required"]) - groups
    assert not missing, msg("R-7", f"pyproject lacks dependency groups {sorted(missing)}", "both")
    owners = BUILD["dependency_groups_owner"]
    assert set(BUILD["dependency_groups_required"]) <= set(owners), msg(
        "R-7", "every required group has an owner", "both"
    )
    assert [owners[g] for g in ("dev", "case", "notebooks")] == ["technical"] * 3, msg(
        "R-7", "dev, case, notebooks are technical"
    )
    assert owners["docs"] == "wp8a" and owners["paper"] == "wp10", msg(
        "R-7", "docs is WP8a's and paper WP10's", "presentation"
    )
    default = set(pyproject["tool"]["uv"]["default-groups"])
    assert set(BUILD["default_groups"]) <= default, msg(
        "R-7", f"default-groups must include {BUILD['default_groups']}", "both"
    )
    # A presentation-owned group in default-groups is the pending change recorded as a gap.
    extra = default - set(BUILD["default_groups"])
    assert all(owners.get(g) in {"wp8a", "wp10"} for g in extra), msg(
        "R-7", f"default-groups carries unexpected extra groups {sorted(extra)}", "both"
    )


def test_r7_python_version_and_branches():
    assert _read(".python-version").strip().startswith(BUILD["python"]), msg(
        "R-7", f".python-version must be {BUILD['python']}"
    )
    assert BUILD["branches"] == ["dev", "main"] and "release tag" in BUILD["workflow_deploys_on"], (
        msg("R-7", "branches dev and main; deployment on a release tag only", "both")
    )
    assert BUILD["workflow_never_deploys_from"] == "dev", msg("R-7", "dev never deploys", "both")
    assert (ROOT / BUILD["ci_workflow"]).is_file(), msg("R-7", "the technical CI workflow exists")


def test_r7_commands_are_pinned_strings():
    expected = {
        "tests_cmd": "uv run pytest",
        "lint_cmd": "uv run ruff check .",
        "format_cmd": "uv run ruff format --check .",
        "lock_cmd": "uv lock --check",
        "docs_cmd": "uv run --group docs mkdocs build --strict",
        "paper_cmd": "uv run myst build --html",
    }
    for key, value in expected.items():
        assert BUILD[key] == value, msg("R-7", f"build.{key} must be {value!r}", "both")
    assert (BUILD["docs_out"], BUILD["paper_out"], BUILD["root_index_out"]) == (
        "_site/docs/",
        "_site/paper/",
        "_site/index.html",
    ), msg("R-7", "outputs under _site/ are the stable public paths", "presentation")
    assert BUILD["public_paths"] == ["/", "/docs/", "/paper/"], msg(
        "R-7", "public paths are stable", "presentation"
    )
    for key in ("docs_cmd", "paper_cmd", "tests_cmd"):
        assert BUILD[key] in DOC, msg("R-7", f"document states build.{key}", "both")
    assert BUILD["paper_cwd"] == "paper/", msg(
        "R-7", "the paper command runs in paper/", "presentation"
    )


def test_r7_skips_name_the_manifest_build_files():
    skips = MAN["skips"]
    pairs = {
        "myst_config": BUILD["paper_config"],
    }
    for key, path in pairs.items():
        assert skips[key]["file"] == path, msg(
            "R-7", f"skip {key} names {skips[key]['file']!r}, manifest says {path!r}", "both"
        )
    for key, s in skips.items():
        assert s["reason"].strip() and s["closed_by"].strip(), msg(
            "R-7", f"skip {key} states a reason and a closing package", "both"
        )


def test_r7_delivered_clauses_left_the_skip_list():
    for key in (
        "build_generated",
        "mkdocs_config",
        "api_reference_page",
        "publish_workflow",
        "stage_site",
        "root_index",
    ):
        assert key not in MAN["skips"], msg("R-7", f"{key} is delivered and enforced", "both")
    assert set(MAN["skips"]) == {"myst_config", "oracle_protocol"}


def test_r7_docsite_configuration():
    assert _read(BUILD["docs_config"]).strip(), msg(
        "R-7", f"{BUILD['docs_config']} is not empty", "presentation"
    )


def test_r7_pages_workflow():
    text = _read(BUILD["workflow"])
    assert re.search(r"tags:\s*\[\s*[\"']v\*[\"']", text) and "workflow_dispatch" in text, msg(
        "R-7", "the Pages workflow triggers on a release tag v* and manual dispatch", "presentation"
    )
    assert not re.search(r"branches:\s*\[[^\]]*\bmain\b", text), msg(
        "R-7", "the Pages workflow never triggers on a push to main", "presentation"
    )
    assert not re.search(r"branches:\s*\[[^\]]*\bdev\b", text), msg(
        "R-7", "the Pages workflow never deploys from dev", "presentation"
    )


def test_r7_root_index():
    assert _read(BUILD["root_index_source"]).strip(), msg(
        "R-7", "the root index source is not empty", "presentation"
    )


def test_r7_paper_configuration_once_delivered():
    _skip_unless_delivered("myst_config")
    assert _read(BUILD["paper_config"]).strip(), msg(
        "R-7", "paper/myst.yml is not empty", "presentation"
    )


# -----------------------------------------------------------------------------------------------
# R-12 local staging
# -----------------------------------------------------------------------------------------------
STAGE = BUILD["stage"]


def test_r12_staging_command_named_in_manifest_document_and_readme():
    assert STAGE["command"] == f"uv run python {STAGE['script']} --serve", msg(
        "R-12", "staging command runs the staging script with --serve", "presentation"
    )
    assert STAGE["command"] in DOC, msg("R-12", "document names the staging command", "both")
    assert (
        STAGE["build_dir"],
        STAGE["url"],
        STAGE["network"],
        STAGE["kernel"],
        STAGE["default"],
    ) == (
        "_stage/",
        "http://127.0.0.1:8000",
        False,
        False,
        True,
    ), msg(
        "R-12",
        "staging builds into _stage/, serves on 127.0.0.1:8000, no network, no kernel, by default",
        "presentation",
    )
    readme = _read("work-packages/README.md")
    branching = re.search(r"\*\*Branching.*?(?=\n- \*\*)", readme, re.S)
    assert branching and "staged" in branching.group(0) and "localhost" in branching.group(0), msg(
        "R-12",
        "work-packages/README.md Branching bullet carries the staged-localhost review step",
        "both",
    )


def test_r12_staging_script():
    text = _read(STAGE["script"])
    assert "--serve" in text and STAGE["build_dir"].rstrip("/") in text, msg(
        "R-12", "stage_site.py offers --serve and builds into _stage/", "presentation"
    )


# -----------------------------------------------------------------------------------------------
# R-9 / R-10 ownership
# -----------------------------------------------------------------------------------------------
OWN = MAN["ownership"]
CARVE = OWN["carve_outs"]
SIDES = {s: spec["paths"] for s, spec in OWN.items() if isinstance(spec, dict) and "paths" in spec}


def _overlap(a: str, b: str) -> bool:
    return a == b or (a.endswith("/") and b.startswith(a)) or (b.endswith("/") and a.startswith(b))


def test_r10_entries_are_explicit_paths_not_globs():
    for side, paths in SIDES.items():
        for p in paths:
            assert not re.search(r"[*?\[]", p) and not p.startswith("/") and ".." not in p, msg(
                "R-10",
                f"{side} path {p!r} must be an explicit path or directory prefix (no globs)",
                "both",
            )


def test_r10_carve_outs_sit_in_their_named_side_inside_another_prefix():
    for path, side in CARVE.items():
        assert path in SIDES[side], msg(
            "R-10", f"carve-out {path} must be listed under side {side!r}", "both"
        )
        enclosing = [
            (s, q)
            for s, ps in SIDES.items()
            if s != side
            for q in ps
            if q.endswith("/") and path.startswith(q)
        ]
        assert enclosing, msg(
            "R-10", f"carve-out {path} must lie inside another side's directory prefix", "both"
        )


def test_r10_sides_pairwise_disjoint_respecting_carve_outs():
    names = list(SIDES)
    clashes = []
    for i, a in enumerate(names):
        for b in names[i + 1 :]:
            for p in SIDES[a]:
                for q in SIDES[b]:
                    if not _overlap(p, q):
                        continue
                    # carve-out: exempt only against the enclosing prefix of another side
                    if (p in CARVE and CARVE[p] == a and q.endswith("/") and q != p) or (
                        q in CARVE and CARVE[q] == b and p.endswith("/") and p != q
                    ):
                        continue
                    clashes.append((a, p, b, q))
    assert not clashes, msg("R-10", f"ownership sets overlap: {clashes}", "both")


def test_r10_technical_disjoint_from_every_presentation_set():
    technical = SIDES["technical"]
    for side in ("wp8a", "wp10", "wp12", "wp8b", "driver"):
        for p in SIDES[side]:
            for t in technical:
                if _overlap(p, t) and not (p in CARVE and CARVE[p] == side):
                    pytest.fail(
                        msg(
                            "R-10", f"{side} path {p!r} lies in the technical set via {t!r}", "both"
                        )
                    )


def test_r9_wp14_owns_exactly_its_three_files_and_they_exist():
    allowed = {
        "work-packages/interface-contract.md",
        "work-packages/interface-contract.toml",
        "tests/test_interface_contract.py",
    }
    assert set(SIDES["wp14"]) == allowed, msg(
        "R-9", f"WP14's set must be exactly {sorted(allowed)}", "both"
    )
    for p in allowed:
        assert (ROOT / p).is_file(), msg("R-9", f"WP14 file {p} exists", "both")
    assert not set(SIDES["wp14"]) & {
        "src/",
        "derivation/",
        "examples/",
        ".github/",
        "pyproject.toml",
        "uv.lock",
    }, msg("R-9", "WP14 must not own WP13's files, pyproject, uv.lock, examples or .github", "both")


def test_r6_glossary_schema_pinned_as_a_floor():
    """Contract version 4: the glossary's schema (entry fields, the list fields, the file's keys)
    is pinned; the build script's validator accepts at least what the manifest names."""
    import importlib.util as _u

    spec = _u.spec_from_file_location("_bg", ROOT / DOCS["generated_by"])
    bg = _u.module_from_spec(spec)
    spec.loader.exec_module(bg)
    fields = set(DOCS["glossary_entry_field_names"])
    required = set(DOCS["glossary_entry_required_field_names"])
    assert required == set(bg.GLOSSARY_REQUIRED), msg(
        "R-6", "required glossary entry fields differ from the build script", "presentation"
    )
    assert fields <= set(bg.GLOSSARY_REQUIRED) | set(bg.GLOSSARY_OPTIONAL), msg(
        "R-6", "a pinned glossary field is not accepted by the build script", "presentation"
    )
    assert {"aliases", "avoid"} <= set(DOCS["glossary_list_field_names"])
    assert set(DOCS["glossary_file_key_names"]) <= set(bg.GLOSSARY_FILE_KEYS)
    import yaml

    data = yaml.safe_load((ROOT / DOCS["glossary_source"]).read_text(encoding="utf-8"))
    assert set(data) <= set(DOCS["glossary_file_key_names"])
    for entry in data["entries"]:
        assert set(entry) <= fields, msg("R-6", f"{entry['id']}: field not pinned", "presentation")


def test_r1_term_aggregation_keyword_pinned():
    """Version 9 (WP21 D-2): the keyword, its default and its values; validated in ``fit``."""
    import numpy as np

    pkg = _pkg()
    spec = PKG["estimator"]
    cls = getattr(pkg, spec["class"])
    param = inspect.signature(cls).parameters["term_aggregation"]
    assert param.default == spec["term_aggregation_default"] == "sum", msg(
        "R-1", "term_aggregation defaults to the manifest's value 'sum'"
    )
    X, _ = pkg.make_frontier_data(40, 3, random_state=0)
    for value in spec["term_aggregation_values"]:
        cls(term_aggregation=value).fit(np.asarray(X))
    with pytest.raises(ValueError, match="term_aggregation"):
        cls(term_aggregation="not-a-value").fit(np.asarray(X))
    assert "term_aggregation" in DOC and "version 9" in DOC, msg(
        "R-8", "the document states the term aggregation amendment", "both"
    )


def test_r1_distinct_terms_field_and_names_pinned():
    """Version 10 (WP21 D-5): the record's count of distinct terms and the names that make it."""
    import numpy as np

    pkg = _pkg()
    solvers = importlib.import_module("hyperbolic_trade_space.solvers")
    assert "n_distinct_terms" in PKG["estimator"]["termination_fields"], msg(
        "R-1", "the manifest pins Termination.n_distinct_terms"
    )
    for name in ("distinct_terms", "DISTINCT_TERMS_DISTANCE"):
        assert name in PKG["submodule_names"]["solvers"] and hasattr(solvers, name), msg(
            "R-1", f"solvers.{name} is pinned and importable"
        )
    X, _ = pkg.make_frontier_data(60, 3, random_state=0)
    fitted = getattr(pkg, PKG["estimator"]["class"])(n_terms=2, random_state=0).fit(np.asarray(X))
    n = fitted.termination_.n_distinct_terms
    assert isinstance(n, int) and 1 <= n <= 2, msg("R-1", "n_distinct_terms is an int in 1..K")
    assert "version 10" in DOC and "n_distinct_terms" in DOC, msg(
        "R-8", "the document states the distinct-terms amendment", "both"
    )

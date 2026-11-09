"""Write the generated pages from running the code and from ``glossary.yaml``.

    uv run python scripts/build_generated.py [--out DIR] [--docs-out DIR]

Writes ``derivations.md`` (every lemma of the chain; the axiom ledger by tag) and
``verification.md`` (tests by area, conformance, lemma checks, what a human validated) into
``build/generated/`` (git-ignored, never committed, outside the docsite: the paper's build reads
them). Writes ``glossary.md``, compiled from ``glossary.yaml`` (term and short, grouped
alphabetically; no other text), into ``docs/generated/`` (git-ignored), which is the docsite's
generated page. The chain is executed through ``derivation.run.run_chain``; the exit status is
non-zero when any lemma fails or the glossary source is invalid. Output is pure Markdown and
deterministic for a given repository state.
"""

from __future__ import annotations

import argparse
import importlib.util
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

DEFAULT_OUT = ROOT / "build" / "generated"  # derivations.md, verification.md (paper's build)
DOCS_GENERATED = ROOT / "docs" / "generated"  # glossary.md (the docsite's generated page)
GLOSSARY_SOURCE = ROOT / "glossary.yaml"
GLOSSARY_REQUIRED = ("id", "term", "short", "register", "formal", "not")
GLOSSARY_OPTIONAL = ("symbol", "defined_in")
GAPS_LEDGER = "docs/superpowers/notes/abstraction-gaps.md"
SKLEARN_TEST_FILE = "tests/test_sklearn_compat.py"

DERIVATION_HEADINGS = ("Lemmas", "Axiom ledger")
VERIFICATION_HEADINGS = ("Tests by area", "Conformance", "Lemma checks", "Validated by a human")

# File (basename under tests/, or "src") -> area. Anything unlisted falls under "Other".
AREA_OF_FILE = {
    "test_derivation.py": "Derivation and ledger",
    "test_matches_derivation.py": "Derivation and ledger",
    "test_sklearn_compat.py": "scikit-learn conformance",
    "test_estimator.py": "Estimator and solvers",
    "test_solvers.py": "Estimator and solvers",
    "test_tensions.py": "Estimator and solvers",
    "test_tuning.py": "Estimator and solvers",
    "test_coordinates.py": "Estimator and solvers",
    "test_preconditioning.py": "Estimator and solvers",
    "test_predictive.py": "Estimator and solvers",
    "test_gaps.py": "Estimator and solvers",
    "test_datasets.py": "Estimator and solvers",
    "test_package.py": "Estimator and solvers",
    "test_plotting.py": "Estimator and solvers",
    "test_adcs_case.py": "Case study (ADCS and CubeSat)",
    "test_adcs_enrichment.py": "Case study (ADCS and CubeSat)",
    "test_check_designs.py": "Case study (ADCS and CubeSat)",
    "test_cubesat_model.py": "Case study (ADCS and CubeSat)",
    "test_k_terms_case.py": "Case study (ADCS and CubeSat)",
    "test_notebook.py": "Case study (ADCS and CubeSat)",
    "test_docs.py": "Documentation and site",
    "test_narrative.py": "Documentation and site",
    "test_references.py": "Documentation and site",
    "test_site.py": "Documentation and site",
    "test_build_generated.py": "Documentation and site",
    "src": "Package doctests",
}
AREA_ORDER = [
    "Derivation and ledger",
    "scikit-learn conformance",
    "Estimator and solvers",
    "Case study (ADCS and CubeSat)",
    "Documentation and site",
    "Package doctests",
    "Other",
]

# Modelling assumptions no machine check can establish (ledger ids as in derivation/axioms.py).
HUMAN_ITEMS = (
    "**Modelling assumptions.** The POSITED conditions A1 to A7 are declared, not derived. "
    "That a particular conditioning is log-affine and invertible (A4), that the noise is "
    "i.i.d. Gaussian (A5) and that the metrics are strictly positive and larger-is-better (A1) "
    "describe the analyst's data, and no test of the code can confirm them for that data.",
    "**Regularity conditions.** R1 (the balanced point lies in the relative interior of a facet "
    "with positive normal) and R2 (a positive assignment margin) are hypotheses about the "
    "fitted reference surface on a given data set. The lemmas state what each buys and what "
    "the reading loses when it fails.",
    "**Inherited theorems.** I1 to I9 are cited from the literature and used; they are not "
    "re-proved here. A reader who relies on a result checks the citation.",
    "**Abstraction gaps.** The step from a formal object to its implementation is recorded "
    "row by row in the gaps ledger, `" + GAPS_LEDGER + "`, with the bridging assumption, what "
    "cannot be proved, the sensitivity evidence and the interpretive consequence. The ledger is "
    "the record of what is validated by a human and not verified by a machine.",
    "**Fit to the system.** Whether the fitted reference surface, the supporting envelope or "
    "the Pareto boundary describes the system under study is a judgement about the designs "
    "evaluated and the evaluation behind them (G-1, G-12). The package reports the fit; the "
    "analyst validates that it answers the question asked.",
)


# ------------------------------------------------------------------------------ derivation


def _chain_results():
    """Run the chain; return (lemma modules, ledger tags) or raise the lemma's failure."""
    from derivation import axioms as AX
    from derivation import run as R

    R.run_chain(verbose=False)
    return list(R.CHAIN), AX


def _users_of(chain):
    users: dict[str, list[int]] = {}
    from derivation.run import lemma_number

    for mod in chain:
        for name in mod.AXIOMS_USED:
            users.setdefault(name, []).append(lemma_number(mod))
    return users


def _axiom_block(a, users):
    lines = [f"- **{a.name}** ({a.tag}): {a.statement}."]
    if a.citation:
        lines.append(f"  - Citation: {a.citation}.")
    if a.role:
        lines.append(f"  - Role: {a.role}.")
    if a.failure_mode:
        lines.append(f"  - Failure mode: {a.failure_mode}.")
    used = users.get(a.name)
    if used:
        lines.append("  - Used by: " + ", ".join(f"L{n}" for n in used) + ".")
    return lines


def derivations_page(chain, AX):
    """Markdown for the Derivations page from the executed chain and ``derivation.axioms``."""
    from derivation.run import lemma_number

    users = _users_of(chain)
    out = [
        "# Derivations",
        "",
        "This page is generated by `scripts/build_generated.py` from the executed derivation "
        "chain (`derivation/run.py`) and the axiom manifest (`derivation/axioms.py`). Each "
        "lemma is a plain SymPy script in `derivation/`; the chain runs for symbolic d, n and K, "
        "not at chosen sizes.",
        "",
        "## Lemmas",
        "",
        f"The chain has {len(chain)} lemmas. Every lemma below derived and verified in the "
        "run that produced this page.",
        "",
    ]
    for mod in chain:
        n = lemma_number(mod)
        axset = ", ".join(mod.AXIOMS_USED) if mod.AXIOMS_USED else "none (algebra only)"
        out += [
            f"### L{n}",
            "",
            f"- Title: `{mod.TITLE}`",
            f"- Statement: `{mod.STATEMENT}`",
            f"- Axioms used: {axset}",
            "",
        ]
    out += [
        "## Axiom ledger",
        "",
        "The ledger lists every condition the derivation rests on, by tag. POSITED conditions "
        "are modelling choices declared here. INHERITED conditions are external theorems used "
        "and cited, not proved here. REGULARITY conditions are hypotheses the interpretation "
        "rests on; each states what it buys and what the reading loses when it fails. "
        "Fallbacks are conditions introduced because a step resisted abstract simplification.",
        "",
    ]
    solver = set(AX.SOLVER_LEVEL)
    cited = set(AX.CITED_CONTEXT)
    fallbacks = {a.name for a in AX.fallbacks()}
    sections = [
        ("POSITED", [a for a in AX.by_tag(AX.POSITED) if a.name not in fallbacks]),
        (
            "INHERITED",
            [a for a in AX.by_tag(AX.INHERITED) if a.name not in solver | cited],
        ),
        ("INHERITED, solver level", [AX.get(n) for n in AX.SOLVER_LEVEL]),
        ("Cited context (no step depends on it)", [AX.get(n) for n in sorted(cited)]),
        ("REGULARITY", AX.by_tag(AX.REGULARITY)),
        ("Fallbacks", AX.fallbacks()),
    ]
    for title, entries in sections:
        out += [f"### {title}", ""]
        if not entries:
            out += ["None.", ""]
            continue
        for a in entries:
            out += _axiom_block(a, users)
            if a.name in cited:
                out.append(f"  - Why no step depends on it: {AX.CITED_CONTEXT[a.name]}.")
        out.append("")
    return "\n".join(out).rstrip() + "\n"


# ------------------------------------------------------------------------------ verification


def collect_tests(runner=None):
    """Return the ``pytest --collect-only -q`` node ids (lines containing ``::``)."""
    if runner is None:
        proc = subprocess.run(
            [sys.executable, "-m", "pytest", "--collect-only", "-q", "-p", "no:cacheprovider"],
            cwd=ROOT,
            capture_output=True,
            text=True,
        )
        if proc.returncode not in (0, 5):
            raise RuntimeError(f"pytest collection failed:\n{proc.stdout}\n{proc.stderr}")
        text = proc.stdout
    else:
        text = runner()
    return [line.strip() for line in text.splitlines() if "::" in line]


def area_of(node_id):
    path = node_id.split("::", 1)[0]
    parts = Path(path).parts
    key = "src" if parts and parts[0] == "src" else parts[-1]
    return AREA_OF_FILE.get(key, "Other")


def counts_by_area(node_ids):
    counts: dict[str, int] = {}
    for nid in node_ids:
        area = area_of(nid)
        counts[area] = counts.get(area, 0) + 1
    return counts


def load_expected_failures(path=None):
    """Return {dict name: {check: reason}} from the ``*EXPECTED_FAILURES`` dicts of the file."""
    path = Path(path) if path else ROOT / SKLEARN_TEST_FILE
    spec = importlib.util.spec_from_file_location("_sklearn_compat_for_pages", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return {
        name: dict(val)
        for name, val in sorted(vars(mod).items())
        if name.endswith("EXPECTED_FAILURES") and isinstance(val, dict)
    }


def conformance_counts(node_ids):
    """Collected conformance checks per test function in the sklearn conformance file."""
    counts: dict[str, int] = {}
    for nid in node_ids:
        if not nid.startswith(SKLEARN_TEST_FILE + "::"):
            continue
        func = re.split(r"[\[:]", nid.split("::", 1)[1])[0]
        if func.startswith("test_sklearn_compatible"):
            counts[func] = counts.get(func, 0) + 1
    return counts


def verification_page(chain, node_ids, expected):
    from derivation.run import lemma_number

    counts = counts_by_area(node_ids)
    areas = [a for a in AREA_ORDER if a in counts] + sorted(set(counts) - set(AREA_ORDER))
    out = [
        "# Verification and validation",
        "",
        "This page is generated by `scripts/build_generated.py` from a test collection, the "
        "conformance expected-failure dictionaries and the executed derivation chain. It states "
        "what a machine verified and what a human validated.",
        "",
        "## Tests by area",
        "",
        f"`pytest --collect-only -q` collects {len(node_ids)} tests (doctests included).",
        "",
        "| Area | Tests |",
        "|---|---|",
    ]
    out += [f"| {a} | {counts[a]} |" for a in areas]
    out.append("")

    conf = conformance_counts(node_ids)
    out += [
        "## Conformance",
        "",
        "The estimators follow the scikit-learn estimator contract and run the scikit-learn "
        "checks through `parametrize_with_checks` with `xfail_strict=True`. A documented "
        "expected failure carries a written reason; an expected failure that passes fails "
        "the run.",
        "",
        "| Check family | Checks collected |",
        "|---|---|",
    ]
    out += [f"| `{f}` | {n} |" for f, n in sorted(conf.items())]
    out += [f"| Total | {sum(conf.values())} |", ""]
    n_exp = sum(len(d) for d in expected.values())
    if n_exp == 0:
        out += ["Documented expected failures: none.", ""]
    else:
        out += [f"Documented expected failures: {n_exp}.", ""]
    for dict_name, entries in expected.items():
        if not entries:
            out += [f"- `{dict_name}`: empty.", ""]
            continue
        for check, reason in sorted(entries.items()):
            out += [f"- `{check}` (`{dict_name}`): {reason}", ""]

    out += [
        "## Lemma checks",
        "",
        f"The chain ran {len(chain)} lemmas for symbolic d, n and K. Each derived and verified "
        "in the run that produced this page.",
        "",
    ]
    out += [f"- L{lemma_number(m)} PASS: `{m.TITLE}`" for m in chain]
    out += [
        "",
        "## Validated by a human",
        "",
        "A passing run verifies the derivation and the code against the stated conditions. It "
        "does not establish the following; a person validates them.",
        "",
    ]
    out += [f"- {item}" for item in HUMAN_ITEMS]
    out.append("")
    return "\n".join(out)


# ------------------------------------------------------------------------------ glossary


def load_glossary(path=None):
    """Read and validate ``glossary.yaml``; return the entries as a list of dicts.

    Raises ``ValueError`` on a missing or unknown field, a non-string or empty value, a
    multi-line ``short``, or a repeated ``id`` or ``term``.
    """
    import yaml

    path = Path(path) if path else GLOSSARY_SOURCE
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict) or set(data) != {"entries"}:
        raise ValueError(f"{path.name}: the top level must be a single key 'entries'")
    entries = data["entries"]
    if not isinstance(entries, list) or not entries:
        raise ValueError(f"{path.name}: 'entries' must be a non-empty list")
    allowed = set(GLOSSARY_REQUIRED) | set(GLOSSARY_OPTIONAL)
    seen_ids, seen_terms = set(), set()
    for i, entry in enumerate(entries):
        where = f"{path.name}: entry {i + 1}"
        if not isinstance(entry, dict):
            raise ValueError(f"{where}: must be a mapping")
        missing = [f for f in GLOSSARY_REQUIRED if f not in entry]
        if missing:
            raise ValueError(f"{where}: missing field(s) {missing}")
        unknown = sorted(set(entry) - allowed)
        if unknown:
            raise ValueError(f"{where}: unknown field(s) {unknown}")
        for key, value in entry.items():
            if not isinstance(value, str) or not value.strip():
                raise ValueError(f"{where}: field '{key}' must be a non-empty string")
        if "\n" in entry["short"].strip() or "\n" in entry["term"].strip():
            raise ValueError(f"{where}: 'short' and 'term' are one line")
        if not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", entry["id"]):
            raise ValueError(f"{where}: id '{entry['id']}' must be a lower-case slug")
        if entry["id"] in seen_ids:
            raise ValueError(f"{where}: repeated id '{entry['id']}'")
        if entry["term"].casefold() in seen_terms:
            raise ValueError(f"{where}: repeated term '{entry['term']}'")
        seen_ids.add(entry["id"])
        seen_terms.add(entry["term"].casefold())
    return entries


def glossary_page(entries):
    """Markdown for the Glossary page: term and short only, grouped alphabetically."""
    ordered = sorted(entries, key=lambda e: (e["term"].casefold(), e["id"]))
    out = ["# Glossary", ""]
    letter = None
    for e in ordered:
        first = e["term"].strip()[0].upper()
        if first != letter:
            letter = first
            out += [f"## {letter}", ""]
        out.append(f"- **{e['term'].strip()}**: {e['short'].strip()}")
        out.append("")
    return "\n".join(out).rstrip() + "\n"


# ------------------------------------------------------------------------------ driver


def _write_atomic(path, text):
    """Write ``text`` to ``path`` through a temporary file and ``os.replace`` so that parallel
    builds in one checkout never expose a half-written page."""
    path = Path(path)
    fd, tmp = tempfile.mkstemp(dir=path.parent, prefix=path.name + ".", suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as fh:
            fh.write(text)
        os.replace(tmp, path)
    except BaseException:
        Path(tmp).unlink(missing_ok=True)
        raise


def build(
    out_dir=DEFAULT_OUT,
    collect_runner=None,
    expected_path=None,
    docs_out=DOCS_GENERATED,
    glossary_path=None,
):
    """Run the chain; write derivations and verification to ``out_dir`` and the glossary to
    ``docs_out``. Raises on a failed lemma or an invalid glossary. Returns the paths."""
    entries = load_glossary(glossary_path)
    chain, AX = _chain_results()
    node_ids = collect_tests(collect_runner)
    expected = load_expected_failures(expected_path)
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    pages = {
        "derivations.md": derivations_page(chain, AX),
        "verification.md": verification_page(chain, node_ids, expected),
    }
    paths = []
    for name, text in pages.items():
        path = out_dir / name
        _write_atomic(path, text)
        paths.append(path)
    docs_out = Path(docs_out)
    docs_out.mkdir(parents=True, exist_ok=True)
    path = docs_out / "glossary.md"
    _write_atomic(path, glossary_page(entries))
    paths.append(path)
    return paths


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "--out", default=str(DEFAULT_OUT), help="directory for derivations.md, verification.md"
    )
    parser.add_argument(
        "--docs-out", default=str(DOCS_GENERATED), help="directory for the docsite glossary.md"
    )
    args = parser.parse_args(argv)
    try:
        paths = build(args.out, docs_out=args.docs_out)
    except Exception as exc:  # a failed lemma or collection must stop the build
        print(f"build_generated: FAILED: {type(exc).__name__}: {exc}", file=sys.stderr)
        return 1
    for p in paths:
        print(f"wrote {p}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

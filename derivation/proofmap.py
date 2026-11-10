"""The proof-map checker: every proof step is a tagged line of a lemma script, and nothing drifts.

    uv run python -m derivation.proofmap            # check against the committed record
    uv run python -m derivation.proofmap --update   # rewrite the record (deliberate; prints a diff)
    uv run python -m derivation.proofmap --execute  # also run the chain (computed steps pass)

The rule (WP10 Amendment 1, R-28 and R-29). Each lemma script ``derivation/lemma_NN_*.py`` is one
file; each proof step is one line of it, carrying a tag comment::

    # [L2.1] one-line prose of the step          (a comment on the code line, or on the line above)

* The address of a step is its file and its tag (``lemma_02_shift.py`` and ``L2.1``). Tags are
  ``L<n>.<k>`` with ``n`` the lemma's number, ``k`` = 1, 2, ... without gaps, in the order the
  steps appear in the file. A file may hold two results (L14: Proposition 3 and the
  approximate-certificate corollary); it declares
  ``PROOF_RESULTS = (("Proposition 3", (1, 2, 3)), ...)``, step numbers that partition the
  file's steps, and each step is owned by one result.
* A step is of one of two kinds, found from its line, never declared apart from it:
  *by a declared axiom* (the line applies a ledger entry that the file imports by name from
  ``derivation.axioms``), or *computed* (the line is SymPy code: an assertion or a call).
  There is no prose-only kind.
* The ledger names a file imports, the ledger names its tagged lines apply and its ``AXIOMS_USED``
  are the same set. A ledger name used on an untagged line, an ``assert`` in ``verify`` without a
  tag, and a lemma with no tags are errors.
* Per step the checker computes a fingerprint (hash of tag, prose and the normalized code line,
  ``ast.unparse``, so formatting does not matter) and compares it with ``proof_map_record.json``.
  The record also carries every step's tag, prose and code (the appendix compiles from it) and the
  fingerprint of every ledger entry. Any difference exits non-zero, naming the step's address.

The set checks parse with ``ast`` and ``tokenize``; no lemma code is executed unless ``--execute``.
What the tool cannot check: that a sentence of prose means what its line computes. That reading
is the human validation; the tool guarantees there is always exactly one line to read it against.
"""

import argparse
import ast
import hashlib
import io
import json
import re
import sys
import tokenize
from pathlib import Path

HERE = Path(__file__).resolve().parent
RECORD_NAME = "proof_map_record.json"
RECORD_VERSION = 2
SIGN_KWARGS = ("positive", "nonnegative", "negative", "nonpositive")
SYMBOL_MAKERS = ("Symbol", "symbols", "IndexedBase", "Dummy")
HYPOTHESIS_MAKERS = ("hypothesis_symbol", "hypothesis_base")

TAG_RE = re.compile(r"^#\s*\[(L(\d+)\.(\d+))\]\s*(.*?)\s*$")
TAGLIKE_RE = re.compile(r"^#\s*\[L\d")
FILE_RE = re.compile(r"^lemma_(\d\d)_.*\.py$")
COMPOUND = (
    ast.FunctionDef,
    ast.AsyncFunctionDef,
    ast.ClassDef,
    ast.If,
    ast.For,
    ast.AsyncFor,
    ast.While,
    ast.With,
    ast.AsyncWith,
    ast.Try,
    ast.Match,
)


class Findings:
    """Collects errors, each with the address of the step (file and tag) it concerns."""

    def __init__(self):
        self.errors = []

    def add(self, file, tag, message, line=None):
        where = f"{file} {tag}" if tag else f"{file}"
        at = f" (line {line})" if line else ""
        self.errors.append(f"{where}{at}: {message}")


def _fingerprint(tag, prose, code):
    return hashlib.sha256(f"{tag}\n{prose}\n{code}".encode()).hexdigest()


def ledger_names(directory):
    """The ledger's entry names, read from the keys of the AXIOMS dict literal (no execution)."""
    tree = ast.parse((directory / "axioms.py").read_text())
    for node in tree.body:
        if isinstance(node, ast.Assign) and any(
            isinstance(t, ast.Name) and t.id == "AXIOMS" for t in node.targets
        ):
            return {k.value for k in node.value.keys if isinstance(k, ast.Constant)}
    raise SystemExit("derivation/axioms.py has no AXIOMS dict literal")


def chain_names(directory):
    """CHAIN_NAMES from run.py (a list literal; no execution)."""
    tree = ast.parse((directory / "run.py").read_text())
    for node in tree.body:
        if isinstance(node, ast.Assign) and any(
            isinstance(t, ast.Name) and t.id == "CHAIN_NAMES" for t in node.targets
        ):
            return ast.literal_eval(node.value)
    raise SystemExit("derivation/run.py has no CHAIN_NAMES list literal")


def _module_literal(tree, name):
    for node in tree.body:
        if isinstance(node, ast.Assign) and any(
            isinstance(t, ast.Name) and t.id == name for t in node.targets
        ):
            try:
                return ast.literal_eval(node.value)
            except ValueError:
                return None
    return None


def _statements(tree):
    return [n for n in ast.walk(tree) if isinstance(n, ast.stmt)]


def _comments(source):
    """(line, is_own_line, text) for every comment token."""
    out = []
    for tok in tokenize.generate_tokens(io.StringIO(source).readline):
        if tok.type == tokenize.COMMENT:
            own = tok.line.strip().startswith("#")
            out.append((tok.start[0], own, tok.string))
    return out


def parse_lemma(path, ledger, findings):
    """Parse one lemma file into its record entry; errors go to ``findings``."""
    name = path.name
    source = path.read_text()
    tree = ast.parse(source)
    number = int(FILE_RE.match(name).group(1))
    stmts = _statements(tree)

    # ---- imports from the ledger
    imported = set()
    for node in tree.body:
        if isinstance(node, ast.ImportFrom) and node.module == "derivation.axioms":
            for alias in node.names:
                if alias.name not in ledger:
                    findings.add(name, None, f"imports {alias.name}, which is not a ledger entry")
                elif alias.asname:
                    findings.add(name, None, f"ledger import {alias.name} must not be renamed")
                else:
                    imported.add(alias.name)

    # ---- imports of proved results (and only those) from other lemma scripts
    imported_results = _result_imports(name, path, tree, findings)
    own_export = f"L{number}_RESULT"
    exported, certified = _exports(path, own_export)
    if exported and not certified:
        findings.add(name, None, f"exports {own_export} but its verify never certifies it")

    # ---- tags and the statements they bind to
    simple = [s for s in stmts if not isinstance(s, COMPOUND)]
    bound = {}  # id(stmt) -> (tag, prose, tag_line)
    steps = []
    seen = set()
    for line, own, text in _comments(source):
        match = TAG_RE.match(text)
        if not match:
            if TAGLIKE_RE.match(text):
                findings.add(name, None, f"malformed tag comment {text!r}", line)
            continue
        tag, lemma_no, k, prose = (
            match.group(1),
            int(match.group(2)),
            int(match.group(3)),
            match.group(4),
        )
        if lemma_no != number:
            findings.add(name, tag, f"tag names lemma {lemma_no}, the file is lemma {number}", line)
        if tag in seen:
            findings.add(name, tag, "duplicate tag", line)
        seen.add(tag)
        if not prose:
            findings.add(name, tag, "the step's prose is empty", line)
        if own:  # binds to the next statement
            later = [s for s in stmts if s.lineno > line]
            target = min(later, key=lambda s: (s.lineno, s.col_offset), default=None)
        else:  # binds to the simple statement that holds the comment's line
            holders = [s for s in simple if s.lineno <= line <= s.end_lineno]
            target = holders[-1] if holders else None
        if target is None or isinstance(target, COMPOUND):
            findings.add(name, tag, "the tag is not on (or directly above) a line of code", line)
            continue
        if id(target) in bound:
            findings.add(
                name, tag, f"two tags on one line of code (also {bound[id(target)][0]})", line
            )
            continue
        bound[id(target)] = (tag, prose, line)
        steps.append((target, k, tag, prose, line))

    if not steps:
        findings.add(name, None, "the lemma has no tagged steps")

    # ---- order: k = 1, 2, ... in the order the steps appear in the file
    steps.sort(key=lambda s: (s[0].lineno, s[0].col_offset))
    for position, (stmt, k, tag, _prose, _line) in enumerate(steps, start=1):
        if k != position:
            findings.add(
                name, tag, f"out of order: step {position} in the file is tagged {k}", stmt.lineno
            )

    # ---- kinds, applied ledger names, code
    out_steps, applied, applied_results = [], set(), set()
    for stmt, _k, tag, prose, _line in steps:
        names = sorted(
            {n.id for n in ast.walk(stmt) if isinstance(n, ast.Name) and n.id in imported}
        )
        used_results = sorted(
            {n.id for n in ast.walk(stmt) if isinstance(n, ast.Name) and n.id in imported_results}
        )
        code = ast.unparse(stmt)
        if used_results:
            kind = "result"
        elif names:
            kind = "axiom"
        else:
            kind = "computed"
            carries = isinstance(stmt, ast.Assert) or any(
                isinstance(n, ast.Call) for n in ast.walk(stmt)
            )
            if not carries:
                findings.add(
                    name, tag, "a computed step must be an assertion or a call", stmt.lineno
                )
        applied.update(names)
        applied_results.update(used_results)
        out_steps.append(
            {
                "tag": tag,
                "kind": kind,
                "applies": names,
                "results": used_results,
                "prose": prose,
                "code": code,
                "fingerprint": _fingerprint(tag, prose, code),
                "_line": stmt.lineno,
            }
        )

    # ---- a ledger name used on an untagged line; an untagged assert in verify
    tagged_ids = {id(s) for s, *_ in steps}
    for stmt in simple:
        if id(stmt) in tagged_ids:
            continue
        used = sorted(
            {n.id for n in ast.walk(stmt) if isinstance(n, ast.Name) and n.id in imported}
        )
        if used:
            findings.add(
                name, None, f"ledger entry {', '.join(used)} used on an untagged line", stmt.lineno
            )
        used_res = sorted(
            {n.id for n in ast.walk(stmt) if isinstance(n, ast.Name) and n.id in imported_results}
        )
        if used_res and not isinstance(stmt, (ast.Import, ast.ImportFrom)):
            findings.add(
                name,
                None,
                f"proved result {', '.join(used_res)} used on an untagged line",
                stmt.lineno,
            )
    for fn in (n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == "verify"):
        for node in ast.walk(fn):
            if isinstance(node, ast.Assert) and id(node) not in tagged_ids:
                findings.add(
                    name, None, "untagged assert in verify (an untagged proof step)", node.lineno
                )

    # ---- principle 3: no premise hides in a symbol; principle 1: no do-nothing application
    hypotheses = _check_symbols(name, tree, findings)

    # ---- every imported proved result is applied by a step
    if set(imported_results) != applied_results:
        findings.add(
            name,
            None,
            f"imported proved results {sorted(imported_results)} differ from the results the "
            f"tagged steps apply {sorted(applied_results)}",
        )

    # ---- imports == applied == AXIOMS_USED
    used_decl = _module_literal(tree, "AXIOMS_USED")
    if used_decl is None:
        findings.add(name, None, "AXIOMS_USED is missing or not a literal list")
        used_decl = []
    declared = set(used_decl)
    if imported != applied:
        findings.add(
            name,
            None,
            f"imported ledger names {sorted(imported)} differ from the entries the tagged steps "
            f"apply {sorted(applied)}",
        )
    if applied != declared:
        findings.add(
            name,
            None,
            f"entries applied by the steps {sorted(applied)} differ from "
            f"AXIOMS_USED {sorted(declared)}",
        )

    # ---- results (L14 holds two): ranges that partition the steps
    results = _module_literal(tree, "PROOF_RESULTS")
    count = len(out_steps)
    if results is None:
        results = [(_module_literal(tree, "TITLE") or name, tuple(range(1, count + 1)))]
    covered = [k for _rname, ks in results for k in ks]
    if sorted(covered) != list(range(1, count + 1)):
        findings.add(
            name,
            None,
            f"PROOF_RESULTS {list(results)} do not partition the {count} steps exactly once",
        )
    owner = {k: rname for rname, ks in results for k in ks}
    for position, step in enumerate(out_steps, start=1):
        step["result"] = owner.get(position, "")

    return {
        "number": number,
        "axioms_used": sorted(declared),
        "hypotheses": hypotheses,
        "proved_results_imported": {k: v for k, v in sorted(imported_results.items())},
        "proved_results_exported": [own_export] if exported else [],
        "imports": sorted(imported),
        "results": [{"name": r, "steps": list(ks)} for r, ks in results],
        "steps": out_steps,
    }


def _exports(path, name):
    """(exported, certified): does ``path`` declare ``name = ProvedResult(...)`` at module level,
    and does its ``verify`` call ``name.certify(...)``?"""
    tree = ast.parse(path.read_text())
    exported = any(
        isinstance(n, ast.Assign)
        and any(isinstance(t, ast.Name) and t.id == name for t in n.targets)
        and isinstance(n.value, ast.Call)
        and _call_name(n.value) == "ProvedResult"
        for n in tree.body
    )
    certified = any(
        isinstance(c, ast.Call)
        and isinstance(c.func, ast.Attribute)
        and c.func.attr == "certify"
        and isinstance(c.func.value, ast.Name)
        and c.func.value.id == name
        for fn in tree.body
        if isinstance(fn, ast.FunctionDef) and fn.name == "verify"
        for c in ast.walk(fn)
    )
    return exported, certified


def _result_imports(name, path, tree, findings):
    """Imports between lemma scripts: only a proved result of an earlier lemma may be imported."""
    chain = chain_names(path.parent)
    me = path.stem
    found = {}
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                if "lemma_" in alias.name.split(".")[-1]:
                    findings.add(name, None, f"imports the lemma script {alias.name}", node.lineno)
        elif isinstance(node, ast.Call) and _call_name(node) in ("import_module", "__import__"):
            if any(isinstance(a, ast.Constant) and "lemma_" in str(a.value) for a in node.args):
                findings.add(name, None, "imports a lemma script by name", node.lineno)
        elif isinstance(node, ast.ImportFrom):
            module = node.module or ""
            if node.level and any("lemma_" in a.name for a in node.names):
                findings.add(name, None, "relative import of a lemma script", node.lineno)
            if module == "derivation":
                for alias in node.names:
                    if alias.name.startswith("lemma_"):
                        findings.add(
                            name, None, f"imports the lemma script {alias.name}", node.lineno
                        )
            if not module.startswith("derivation.lemma_"):
                continue
            source = module.split(".")[1]
            expected = f"L{int(source.split('_')[1])}_RESULT"
            for alias in node.names:
                if alias.name != expected or alias.asname:
                    findings.add(
                        name,
                        None,
                        f"imports {alias.name} from {source}: a lemma script may import from "
                        f"another lemma script only its proved result, {expected}",
                        node.lineno,
                    )
                elif (
                    source not in chain or me not in chain or chain.index(source) >= chain.index(me)
                ):
                    findings.add(
                        name,
                        None,
                        f"imports {expected}, but {source} is not earlier in the chain",
                        node.lineno,
                    )
                else:
                    exported, certified = _exports(path.parent / f"{source}.py", expected)
                    if not exported:
                        findings.add(
                            name, None, f"{source} does not export {expected}", node.lineno
                        )
                    elif not certified:
                        findings.add(
                            name, None, f"{source} never certifies {expected}", node.lineno
                        )
                    else:
                        found[alias.name] = source
    return found


def _call_name(node):
    f = node.func
    return f.attr if isinstance(f, ast.Attribute) else getattr(f, "id", None)


def _normalized(text):
    return " ".join(text.split())


def _check_symbols(name, tree, findings):
    """Rules 1 and 3 of WP10 Amendment 2, found from the syntax tree.

    * A symbol or family created with a sign assumption (positive, nonnegative, ...) stands for a
      premise.  Direct creation is an error: the symbol comes from a ledger entry's factory (a
      tagged line, so it is a step), from an earlier lemma's proved result, or is declared at
      module level as a hypothesis of the statement (``hypothesis_symbol`` / ``hypothesis_base``)
      whose quoted claim must occur in the lemma's STATEMENT or docstring.  A real-valued
      ``IndexedBase`` is a premise too.
    * ``Axiom.invoke`` (an application that does nothing) is an error.
    """
    doc = ast.get_docstring(tree) or ""
    statement = _module_literal(tree, "STATEMENT") or ""
    source = _normalized(doc + " " + (statement if isinstance(statement, str) else ""))
    module_level = {id(n.value): n for n in tree.body if isinstance(n, ast.Assign)}
    hypotheses = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        called = _call_name(node)
        if called == "invoke":
            findings.add(name, None, "a do-nothing application: Axiom.invoke", node.lineno)
        if called in SYMBOL_MAKERS:
            for kw in node.keywords:
                signed = (
                    kw.arg in SIGN_KWARGS and isinstance(kw.value, ast.Constant) and kw.value.value
                )
                real_family = called == "IndexedBase" and kw.arg == "real"
                if signed or real_family:
                    findings.add(
                        name,
                        None,
                        f"unlicensed assuming symbol ({kw.arg}=True on {called}): a premise hidden "
                        "in a symbol; take it from a ledger entry, an earlier result, or declare "
                        "a hypothesis of the statement",
                        node.lineno,
                    )
        if called in HYPOTHESIS_MAKERS:
            args = [a.value for a in node.args if isinstance(a, ast.Constant)]
            if id(node) not in module_level:
                findings.add(
                    name, None, "a hypothesis must be declared at module level", node.lineno
                )
            elif len(args) != 3 or args[1] not in ("positive", "nonnegative"):
                findings.add(
                    name, None, "a hypothesis names a symbol, a sign and a claim", node.lineno
                )
            else:
                symbol, sign, claim = args
                if _normalized(claim) not in source:
                    findings.add(
                        name,
                        None,
                        f"hypothesis {symbol!r} quotes {claim!r}, which is not in the lemma's "
                        "STATEMENT or docstring",
                        node.lineno,
                    )
                hypotheses.append(
                    {
                        "symbol": symbol,
                        "kind": "family" if called == "hypothesis_base" else "symbol",
                        "sign": sign,
                        "claim": claim,
                    }
                )
    return hypotheses


def build(directory, findings):
    """The full proof map of the lemma files in ``directory`` (the static part)."""
    ledger = ledger_names(directory)
    files = {p.name: p for p in sorted(directory.glob("lemma_*.py")) if FILE_RE.match(p.name)}
    for module in chain_names(directory):
        if f"{module}.py" not in files:
            findings.add(f"{module}.py", None, "lemma file named in CHAIN_NAMES is missing")
    lemmas = {}
    for fname, path in files.items():
        lemmas[fname] = parse_lemma(path, ledger, findings)
    return {"version": RECORD_VERSION, "lemmas": lemmas}


def ledger_check(directory, findings):
    """Dynamic part: every entry declares a SymPy form or is a named proposition; fingerprints."""
    sys.path.insert(0, str(directory.parent))
    try:
        from derivation import axioms
    finally:
        sys.path.pop(0)
    prints = {}
    for name, entry in axioms.AXIOMS.items():
        if not entry.has_form():
            findings.add(
                "axioms.py", name, "ledger entry has no SymPy form and is not a named proposition"
            )
        prints[name] = entry.fingerprint()
    return prints


def _strip(proof_map):
    clean = json.loads(json.dumps(proof_map))
    for lemma in clean["lemmas"].values():
        for step in lemma["steps"]:
            step.pop("_line", None)
    return clean


def compare(new, old, findings):
    """Differences between the freshly computed map and the committed record."""
    new_l, old_l = new["lemmas"], old.get("lemmas", {})
    for fname in sorted(set(new_l) | set(old_l)):
        if fname not in old_l:
            findings.add(fname, None, "lemma file is not in the record")
            continue
        if fname not in new_l:
            findings.add(fname, None, "lemma file in the record is gone")
            continue
        n_steps = {s["tag"]: s for s in new_l[fname]["steps"]}
        o_steps = {s["tag"]: s for s in old_l[fname]["steps"]}
        for tag in sorted(set(n_steps) | set(o_steps), key=lambda t: int(t.split(".")[1])):
            if tag not in o_steps:
                findings.add(fname, tag, "step is not in the record", n_steps[tag].get("_line"))
            elif tag not in n_steps:
                findings.add(fname, tag, "step in the record is gone from the script")
            else:
                a, b = n_steps[tag], o_steps[tag]
                if a["fingerprint"] == b["fingerprint"] and a["result"] == b.get("result"):
                    continue
                what = []
                if a["prose"] != b["prose"]:
                    what.append("prose")
                if a["code"] != b["code"]:
                    what.append("script line")
                if a["result"] != b.get("result"):
                    what.append("owning result")
                findings.add(
                    fname,
                    tag,
                    f"{' and '.join(what) or 'content'} changed since the record",
                    a["_line"],
                )
        keys = ("axioms_used", "imports", "results", "hypotheses")
        for key in (*keys, "proved_results_imported", "proved_results_exported"):
            if new_l[fname][key] != old_l[fname].get(key):
                findings.add(fname, None, f"{key} changed since the record")
    for name in sorted(set(new.get("ledger", {})) | set(old.get("ledger", {}))):
        if new.get("ledger", {}).get(name) != old.get("ledger", {}).get(name):
            findings.add(
                "axioms.py", name, "ledger entry (statement, citation or SymPy form) changed"
            )


def run_chain_check(findings):
    sys.path.insert(0, str(HERE.parent))
    try:
        from derivation.run import run_chain

        run_chain(verbose=False)
    except AssertionError as exc:
        findings.add("run.py", None, f"a computed step fails: {exc}")
    finally:
        sys.path.pop(0)


def main(argv=None):
    ap = argparse.ArgumentParser(
        prog="python -m derivation.proofmap", description=__doc__.split("\n")[0]
    )
    ap.add_argument("--update", action="store_true", help="rewrite the committed record")
    ap.add_argument(
        "--execute", action="store_true", help="also run the chain (computed steps pass)"
    )
    args = ap.parse_args(argv)

    findings = Findings()
    new = build(HERE, findings)
    new["ledger"] = ledger_check(HERE, findings)
    record_path = HERE / RECORD_NAME

    if args.update:
        old = json.loads(record_path.read_text()) if record_path.exists() else {"lemmas": {}}
        diff = Findings()
        compare(new, old, diff)
        if findings.errors:
            print("not updated; fix first:")
            print("\n".join(f"  {e}" for e in findings.errors))
            return 1
        record_path.write_text(json.dumps(_strip(new), indent=1, ensure_ascii=False) + "\n")
        moved = diff.errors or ["no step moved"]
        print(f"record rewritten: {record_path}")
        print("\n".join(f"  {e}" for e in moved))
        return 0

    if not record_path.exists():
        findings.add(RECORD_NAME, None, "no committed record (run with --update)")
    else:
        compare(new, json.loads(record_path.read_text()), findings)
    if args.execute:
        run_chain_check(findings)

    if findings.errors:
        print(f"PROOF MAP FAILED ({len(findings.errors)} problem(s)):")
        print("\n".join(f"  {e}" for e in findings.errors))
        return 1
    n_steps = sum(len(v["steps"]) for v in new["lemmas"].values())
    per = ", ".join(f"L{v['number']}:{len(v['steps'])}" for v in new["lemmas"].values())
    print(f"PROOF MAP OK: {len(new['lemmas'])} lemma files, {n_steps} tagged steps ({per})")
    return 0


if __name__ == "__main__":
    sys.exit(main())

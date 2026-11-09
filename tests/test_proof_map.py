"""The proof-map checker (derivation/proofmap.py) and the tagged lemma scripts (WP10, R-28, R-29).

Every proof step is a tagged line of a lemma script; the checker fails on any drift. These tests
check the committed record, the equality of imported, applied and declared ledger names, and (on a
scratch copy of ``derivation/``, so the repository is never touched) that breaking a script step,
a prose step or the order, an untagged proof step and an unmatched import each make the checker
fail, naming the step.
"""

import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

from derivation import axioms as AX
from derivation import proofmap
from derivation.run import CHAIN, CHAIN_NAMES, lemma_number

ROOT = Path(__file__).resolve().parent.parent
DERIVATION = ROOT / "derivation"


def _record():
    return json.loads((DERIVATION / proofmap.RECORD_NAME).read_text())


@pytest.fixture
def scratch(tmp_path):
    """A scratch copy of derivation/ (the repository is untouched); returns its package dir."""
    dest = tmp_path / "derivation"
    shutil.copytree(DERIVATION, dest, ignore=shutil.ignore_patterns("__pycache__"))
    return dest


def run_checker(scratch_pkg, *args):
    """Run ``python -m derivation.proofmap`` from the scratch copy's parent directory."""
    env = {k: v for k, v in os.environ.items() if k != "PYTHONPATH"}
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    proc = subprocess.run(
        [sys.executable, "-m", "derivation.proofmap", *args],
        cwd=scratch_pkg.parent,
        env=env,
        capture_output=True,
        text=True,
        timeout=300,
    )
    return proc.returncode, proc.stdout + proc.stderr


def edit(scratch_pkg, filename, old, new, count=1):
    path = scratch_pkg / filename
    text = path.read_text()
    assert text.count(old) == count, f"{filename}: expected {count} of {old!r}"
    path.write_text(text.replace(old, new))


# ---------------------------------------------------------------- the committed record passes


def test_checker_passes_on_the_committed_record(capsys):
    assert proofmap.main([]) == 0
    assert "PROOF MAP OK" in capsys.readouterr().out


def test_checker_passes_on_an_untouched_scratch_copy(scratch):
    code, out = run_checker(scratch)
    assert code == 0, out
    assert "PROOF MAP OK" in out


def test_record_holds_every_step_with_tag_prose_and_code():
    rec = _record()
    assert len(rec["lemmas"]) == len(CHAIN_NAMES)
    for fname, lemma in rec["lemmas"].items():
        assert lemma["steps"], fname
        for pos, step in enumerate(lemma["steps"], start=1):
            assert step["tag"] == f"L{lemma['number']}.{pos}"
            assert step["prose"].strip() and step["code"].strip()
            assert step["kind"] in ("computed", "axiom")
            assert (step["kind"] == "axiom") == bool(step["applies"])
            assert len(step["fingerprint"]) == 64
            assert step["result"]
    assert set(rec["ledger"]) == set(AX.AXIOMS)


def test_every_lemma_file_is_in_the_record_in_chain_order():
    assert [f"{n}.py" for n in CHAIN_NAMES] == list(_record()["lemmas"])


# ------------------------------------- imports == applied == AXIOMS_USED (and the ledger itself)


def test_imported_applied_and_declared_ledger_names_are_the_same_set():
    rec = _record()["lemmas"]
    for mod in CHAIN:
        lemma = rec[f"{mod.__name__.split('.')[-1]}.py"]
        assert lemma["number"] == lemma_number(mod)
        applied = {name for step in lemma["steps"] for name in step["applies"]}
        assert set(lemma["imports"]) == applied == set(mod.AXIOMS_USED) == set(lemma["axioms_used"])
        for name in lemma["imports"]:
            assert name in AX.AXIOMS


def test_every_ledger_entry_is_an_importable_name_with_a_form_or_a_named_proposition():
    for name, entry in AX.AXIOMS.items():
        assert getattr(AX, name) is entry, f"{name} is not exposed as a module-level name"
        assert entry.has_form(), f"{name} has neither a SymPy form nor a named proposition"
        assert entry.relations() or entry.objects or entry.proposition
        if entry.proposition:
            assert not entry.relations() and entry.statement.strip()
        if entry.tag == AX.INHERITED:
            assert entry.citation.strip()


def test_ledger_fingerprints_are_stable_text_hashes():
    first, second = AX.fingerprints(), AX.fingerprints()
    assert first == second and set(first) == set(AX.AXIOMS)
    assert all(re.fullmatch(r"[0-9a-f]{64}", h) for h in first.values())
    assert len(set(first.values())) == len(first)  # distinct entries, distinct hashes


def test_a_result_sharing_a_file_owns_its_own_steps():
    """L14 proves Proposition 3 and Corollary 4 in one file: one tag sequence, two owners."""
    lemma = _record()["lemmas"]["lemma_14_assignment_stable.py"]
    owners = {s["tag"]: s["result"] for s in lemma["steps"]}
    assert set(owners.values()) == {"Proposition 3", "Corollary 4"}
    assert len({s["tag"] for s in lemma["steps"]}) == len(lemma["steps"])
    assert owners["L14.9"] == owners["L14.10"] == "Corollary 4"
    assert owners["L14.5"] == "Proposition 3"


# ----------------------------------- each kind of breakage makes the checker fail, naming the step


def test_a_changed_script_step_fails_naming_the_step(scratch):
    edit(scratch, "lemma_02_shift.py", 'assert r["term_diff"] == 0,', 'assert r["term_diff"] == 1,')
    code, out = run_checker(scratch)
    assert code != 0
    assert "lemma_02_shift.py L2.3" in out and "script line changed" in out
    assert "L2.4" not in out  # only the broken step is named


def test_a_changed_prose_step_fails_naming_the_step(scratch):
    edit(
        scratch,
        "lemma_02_shift.py",
        "# [L2.3] per term, tau sum_j w_j (u_ij + c) - (tau s_i + tau c) is 0",
        "# [L2.3] per term, the shift is absorbed",
    )
    code, out = run_checker(scratch)
    assert code != 0
    assert "lemma_02_shift.py L2.3" in out and "prose changed" in out


def test_swapped_tags_fail_naming_the_steps(scratch):
    edit(scratch, "lemma_02_shift.py", "# [L2.3] per term", "# [L2.4] per term")
    edit(scratch, "lemma_02_shift.py", "# [L2.4] J_tau(U", "# [L2.3] J_tau(U")
    code, out = run_checker(scratch)
    assert code != 0
    assert "lemma_02_shift.py L2.4" in out and "out of order" in out
    assert "lemma_02_shift.py L2.3" in out


def test_a_duplicate_tag_fails(scratch):
    edit(scratch, "lemma_02_shift.py", "# [L2.4] J_tau(U", "# [L2.3] J_tau(U")
    code, out = run_checker(scratch)
    assert code != 0 and "lemma_02_shift.py L2.3" in out and "duplicate tag" in out


def test_a_gap_in_the_numbering_fails(scratch):
    edit(scratch, "lemma_02_shift.py", "# [L2.4] J_tau(U", "# [L2.5] J_tau(U")
    code, out = run_checker(scratch)
    assert code != 0 and "lemma_02_shift.py L2.5" in out and "out of order" in out


def test_a_lemma_with_zero_tags_fails(scratch):
    path = scratch / "lemma_02_shift.py"
    path.write_text(re.sub(r"^\s*# \[L2\.\d+\].*\n", "", path.read_text(), flags=re.M))
    code, out = run_checker(scratch)
    assert code != 0
    assert "lemma_02_shift.py: the lemma has no tagged steps" in out


def test_an_untagged_assert_in_verify_fails(scratch):
    edit(
        scratch,
        "lemma_02_shift.py",
        '    S = ctx["S"]\n    r = ctx["L2"]\n',
        '    S = ctx["S"]\n    r = ctx["L2"]\n    assert S.d.is_integer\n',
    )
    code, out = run_checker(scratch)
    assert code != 0
    assert "lemma_02_shift.py" in out and "untagged assert in verify" in out


def test_removing_a_tag_from_a_step_fails(scratch):
    """An assert in verify that lost its tag is an untagged proof step, detected by name."""
    edit(
        scratch,
        "lemma_02_shift.py",
        "    # [L2.3] per term, tau sum_j w_j (u_ij + c) - (tau s_i + tau c) is 0\n",
        "",
    )
    code, out = run_checker(scratch)
    assert code != 0 and "untagged assert in verify" in out


def test_a_ledger_import_that_no_step_applies_fails(scratch):
    edit(
        scratch,
        "lemma_02_shift.py",
        "from derivation.axioms import A2, A3",
        "from derivation.axioms import A2, A3, I1",
    )
    code, out = run_checker(scratch)
    assert code != 0 and "lemma_02_shift.py" in out and "imported ledger names" in out


def test_a_ledger_entry_applied_but_not_listed_in_axioms_used_fails(scratch):
    edit(scratch, "lemma_02_shift.py", 'AXIOMS_USED = ["A2", "A3"]', 'AXIOMS_USED = ["A2"]')
    code, out = run_checker(scratch)
    assert code != 0 and "differ from AXIOMS_USED" in out


def test_a_ledger_entry_used_on_an_untagged_line_fails(scratch):
    edit(
        scratch,
        "lemma_02_shift.py",
        "    s_i = sp.Sum(w[j] * u[i, j], (j, 1, d))\n",
        "    s_i = sp.Sum(w[j] * u[i, j], (j, 1, d))\n    _unused = A2.relations()\n",
    )
    code, out = run_checker(scratch)
    assert code != 0 and "used on an untagged line" in out


def test_importing_a_name_that_is_not_a_ledger_entry_fails(scratch):
    edit(
        scratch,
        "lemma_02_shift.py",
        "from derivation.axioms import A2, A3",
        "from derivation.axioms import A2, A3, A99",
    )
    code, out = run_checker(scratch)
    assert code != 0 and "A99" in out and "not a ledger entry" in out


def test_a_changed_ledger_entry_fails(scratch):
    edit(
        scratch,
        "axioms.py",
        "the soft-maximum temperature is positive: tau > 0",
        "the soft-maximum temperature is nonnegative: tau >= 0",
    )
    code, out = run_checker(scratch)
    assert code != 0 and "axioms.py A3" in out and "ledger entry" in out


def test_a_ledger_entry_without_a_form_fails(scratch):
    """Dropping a named proposition's declaration leaves an entry with no form at all."""
    edit(
        scratch,
        "axioms.py",
        'not at chosen sizes)",\n        proposition=True,\n',
        'not at chosen sizes)",\n',
    )
    code, out = run_checker(scratch)
    assert code != 0 and "axioms.py A0" in out and "no SymPy form" in out


def test_the_order_of_steps_in_the_file_is_the_tag_order(scratch):
    """Moving a tagged line past its successor reorders the steps, so the tags are out of order."""
    path = scratch / "lemma_02_shift.py"
    text = path.read_text()
    a = re.search(r"    # \[L2\.3\].*\n.*\n.*\n.*\n", text)  # the L2.3 comment and its assert
    assert a
    block3 = a.group(0)
    text = text.replace(block3, "", 1)
    marker = '    assert diff == 0, f"L2 FAIL'
    # put the L2.3 block after the L2.4 assert block
    idx = text.index(marker)
    end = text.index("\n", idx) + 1
    path.write_text(text[:end] + block3 + text[end:])
    code, out = run_checker(scratch)
    assert code != 0 and "lemma_02_shift.py" in out


# --------------------------------------------------------------------- refreshing is explicit


def test_update_rewrites_the_record_and_prints_the_steps_that_moved(scratch):
    edit(
        scratch,
        "lemma_02_shift.py",
        'assert r["term_diff"] == 0,',
        'assert r["term_diff"] == 0 and True,',
    )
    code, _ = run_checker(scratch)
    assert code != 0  # drift is not silent
    code, out = run_checker(scratch, "--update")
    assert code == 0 and "lemma_02_shift.py L2.3" in out  # the diff names exactly the moved step
    assert "L2.4" not in out
    code, out = run_checker(scratch)
    assert code == 0, out


def test_update_refuses_a_broken_proof_map(scratch):
    edit(scratch, "lemma_02_shift.py", "# [L2.4] J_tau(U", "# [L2.3] J_tau(U")
    code, out = run_checker(scratch, "--update")
    assert code != 0 and "not updated" in out

"""Licences: a forced logarithm or power is taken only on the positivity a ledger entry declares.

A step that needs ``x > 0`` (a log of a product, a power of a positive base) gives the entries that
declare it; ``log_expand`` and ``licensed_power`` check every logarithm or power against them and
raise ``LicenceError`` otherwise, so a premise cannot be assumed on the caller's word. An entry
declares positivity through its ``x > 0`` relations (and the symbols registered under it in
``derivation.symbols.SYMBOL_ASSUMPTIONS``), and reality through its ordering relations and its
log-equations (``Axiom.positive_sigs`` and ``Axiom.real_sigs``).
"""

import sympy as sp

from derivation.symbols import SYMBOL_ASSUMPTIONS


class LicenceError(ValueError):
    """An operation that needs a premise was given no ledger entry that declares it."""


def _sig(expr):
    """The signature of a declared atom: a family (any index), a symbol, or a sum of those."""
    if isinstance(expr, sp.Indexed):
        return ("idx", expr.base)
    if isinstance(expr, sp.IndexedBase):
        return ("idx", expr)
    if isinstance(expr, sp.Symbol):
        return ("sym", expr)
    if isinstance(expr, sp.Add):
        parts = [_sig(a) for a in expr.args if not a.is_number]
        return ("add", frozenset(parts)) if all(parts) else None
    return None


def _atoms_sigs(expr):
    out = set()
    for a in expr.atoms(sp.Indexed):
        out.add(_sig(a))
    for a in expr.atoms(sp.Symbol):
        if not a.is_integer:
            out.add(_sig(a))
    return out


def _registered_names():
    return {name: ax for (name, _a, ax) in SYMBOL_ASSUMPTIONS.values()}


def _is_real(z, lic):
    """Is ``z`` real, from the declared real atoms of the licensing entries?"""
    if z.is_number or z.is_integer:
        return z.is_real is not False
    if isinstance(z, (sp.Symbol, sp.Indexed, sp.IndexedBase)):
        sig = _sig(z)
        if any(sig in e.real_sigs() or sig in e.positive_sigs() for e in lic):
            return True
        if isinstance(z, sp.Symbol) and z.name in _registered_names():
            return _registered_names()[z.name] in {e.name for e in lic} | {"A0"}
        return z.is_real is True
    if isinstance(z, (sp.Sum, sp.Product)):
        return _is_real(z.function, lic)
    return bool(z.args) and all(_is_real(a, lic) for a in z.args)


def _is_positive(f, lic):
    """Is ``f`` positive, from the positivity the licensing entries declare?"""
    names = {e.name for e in lic}
    if f.is_number:
        return f.is_positive is True
    sig = _sig(f)
    if sig is not None and any(sig in e.positive_sigs() for e in lic):
        return True
    reg = _registered_names()
    if isinstance(f, sp.Symbol) and f.name in reg and f.is_positive:
        return reg[f.name] in names | {"A0"}
    if isinstance(f, sp.Indexed) and f.base.name in reg and f.is_positive:
        return reg[f.base.name] in names
    if isinstance(f, (sp.Symbol, sp.Indexed)):
        return False
    if isinstance(f, sp.exp):
        return _is_real(f.args[0], lic)
    if isinstance(f, sp.Pow):
        return _is_positive(f.base, lic)
    if isinstance(f, (sp.Mul, sp.Add)):
        return all(_is_positive(a, lic) for a in f.args)
    if isinstance(f, (sp.Sum, sp.Product)):
        return _is_positive(f.function, lic)
    return False


def licensed_logs(expr, *licences):
    """True iff every log inside ``expr`` has an argument the licences declare positive."""
    return all(_is_positive(lg.args[0], licences) for lg in expr.atoms(sp.log))


def log_expand(expr, *licences):
    """``expand_log(expr, force=True)``, licensed by ledger entries that declare the positivity.

    Every logarithm inside ``expr`` must have an argument built from factors the entries declare
    positive (or exponentials of quantities they declare real); otherwise ``LicenceError``.
    """
    if not licences:
        raise LicenceError("a forced log expansion needs a licensing ledger entry")
    for lg in expr.atoms(sp.log):
        if not _is_positive(lg.args[0], licences):
            names = ", ".join(e.name for e in licences)
            raise LicenceError(f"log({lg.args[0]}) is not licensed as positive by {names}")
    return sp.expand_log(expr, force=True)


def licensed_power(expr, *licences):
    """``powdenest(expr, force=True)``, licensed: every power's base must be declared positive."""
    for pw in expr.atoms(sp.Pow):
        if not pw.exp.is_number and not _is_positive(pw.base, licences):
            names = ", ".join(e.name for e in licences)
            raise LicenceError(f"the base of {pw} is not licensed as positive by {names}")
    return sp.powdenest(expr, force=True)


# ---------------------------------------------------------------------------------------------
# Hypotheses of a statement.  A symbol that carries a sign assumption stands for a premise. It is
# created by a ledger entry's factory (``A2.nonneg_base``, ``F12.nonneg_symbol``, ...), taken from
# an earlier lemma's proved result, or declared here as a hypothesis of the lemma's own statement:
# at module level, with the claim quoted from the lemma's STATEMENT or docstring (the checker
# verifies that the quotation is there and lists the hypothesis in the proof map).
# ---------------------------------------------------------------------------------------------
SIGNS = ("positive", "nonnegative")


def hypothesis_symbol(name, kind, claim):
    """A symbol with the sign ``kind`` that a hypothesis of the statement (``claim``) gives it."""
    if kind not in SIGNS or not claim.strip():
        raise ValueError("a hypothesis names its sign and quotes the statement's claim")
    return sp.Symbol(name, **{kind: True})


def hypothesis_base(name, kind, claim):
    """A family with the sign ``kind`` that a hypothesis of the statement (``claim``) gives it."""
    if kind not in SIGNS or not claim.strip():
        raise ValueError("a hypothesis names its sign and quotes the statement's claim")
    return sp.IndexedBase(name, **{kind: True})

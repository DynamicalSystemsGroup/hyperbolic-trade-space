"""Proved results: what a lemma script exports and a later script takes by import.

A lemma script that others build on declares, at module level, one export named ``L<n>_RESULT``
(``L3_RESULT = ProvedResult("L3", STATEMENT)``) and certifies it as the last line of its ``verify``
(``L3_RESULT.certify(ctx)``), which it reaches only when every assertion of the proof passed.  A
later script imports that name and nothing else from the earlier script::

    from derivation.lemma_03_gradient_kkt import L3_RESULT

and applies it in a tagged step (``a0, sv = L3_RESULT.take(ctx, "a0", "sv")``): the step is of the
kind *by a proved result*.  Taking from a result that has not been certified raises.  How the
symbolic objects travel at run time is the runner's shared dictionary ``ctx``; the checker
(``derivation/proofmap.py``) requires that the import is of an earlier lemma in the chain, that the
export exists and is certified, that the name is applied by a step, and that nothing else is
imported from a lemma script.
"""

import sympy as sp


class UnprovedResultError(RuntimeError):
    """A result was taken before its lemma was proved (or after it was re-derived)."""


class ProvedResult:
    """The result of lemma ``key`` (for example ``"L3"``), proved once the lemma certifies it."""

    def __init__(self, key, claim):
        self.key = key
        self.claim = claim

    def certify(self, ctx):
        """Mark the result proved: called at the end of the exporting lemma's ``verify``."""
        ctx[self.key]["_proved"] = True

    def proved(self, ctx):
        return bool(ctx.get(self.key, {}).get("_proved"))

    def _require(self, ctx):
        if not self.proved(ctx):
            raise UnprovedResultError(f"{self.key} is not proved: {self.claim}")

    def take(self, ctx, *names):
        """The proved objects ``names`` of the lemma (one name returns the object itself)."""
        self._require(ctx)
        values = tuple(ctx[self.key][name] for name in names)
        return values[0] if len(values) == 1 else values

    def holds(self, ctx, name):
        """True iff the result is proved and its fact ``name`` is established (is True)."""
        return self.proved(ctx) and ctx[self.key].get(name) is True

    def family(self, ctx, fact, name):
        """A nonnegative family ``name`` for a slack that the proved fact ``fact`` establishes."""
        self._require(ctx)
        if ctx[self.key].get(fact) is not True:
            raise UnprovedResultError(f"{self.key} does not establish {fact}")
        return sp.IndexedBase(name, nonnegative=True)

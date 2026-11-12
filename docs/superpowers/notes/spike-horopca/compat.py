"""One compatibility shim for the authors' repository, applied from outside (the clone is not edited).

The repository was written for PyTorch 1.8.1, where ``torch.solve(B, A)`` returned ``(solution, LU)``.
It was removed in PyTorch 1.13 (the error on torch 2.x: "`torch.solve` is deprecated in favor of
`torch.linalg.solve`"; on torch 1.12.1 the same).  This restores the old call with the same arithmetic.
"""
from collections import namedtuple
import torch

_Solve = namedtuple("solve", ["solution", "LU"])


def install():
    torch.solve = lambda B, A: _Solve(torch.linalg.solve(A, B), None)

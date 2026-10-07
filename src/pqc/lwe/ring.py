"""Ring-LWE en Z_q[x]/(x^n + 1)."""
from __future__ import annotations

from ..tareas import LWETask


def break_ring_key(task: LWETask) -> list[int]:
    """b = a*s + e. Recuperar s."""
    raise NotImplementedError  # TODO


def decrypt_ring(task: LWETask, s: list[int]) -> list[int]:
    """Palabra de bits a partir de (c1, c2):  c2 - c1*s  ~  bit * q/2."""
    raise NotImplementedError  # TODO

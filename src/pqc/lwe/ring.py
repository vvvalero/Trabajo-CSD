"""Ring-LWE en Z_q[x]/(x^n + 1)."""
from __future__ import annotations

from ..lector_tareas import TareaRingLWE


def break_ring_key(task: TareaRingLWE) -> list[int]:
    """b = a*s + e. Recuperar s."""
    raise NotImplementedError  # TODO


def decrypt_ring(task: TareaRingLWE, s: list[int]) -> list[int]:
    """Palabra de bits a partir de (c1, c2):  c2 - c1*s  ~  bit * q/2."""
    raise NotImplementedError  # TODO

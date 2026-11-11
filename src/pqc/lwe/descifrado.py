"""Descifrado de un bit con LWE (Ejemplo 6 del PDF)."""
from __future__ import annotations

from ..lector_tareas import TareaLWE


def decrypt_bit(task: TareaLWE, s: list[int]) -> int:
    """R = C . s mod q; bit 0 si R esta cerca de B, bit 1 si esta cerca de B + q/2."""
    raise NotImplementedError  # TODO

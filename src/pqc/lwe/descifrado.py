"""Descifrado de un bit con LWE (Ejemplo 6 del enunciado)."""
from __future__ import annotations

from ..lector_tareas import TareaLWE


def descifrar_bit(tarea: TareaLWE, s: list[int]) -> int:
    """R = C . s mod q; bit 0 si R esta cerca de B, bit 1 si esta cerca de B + q/2."""
    raise NotImplementedError  # TODO

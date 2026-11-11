"""Ring-LWE en Z_q[x]/(x^n + 1) (esquema del Tema 11)."""
from __future__ import annotations

from ..lector_tareas import TareaRingLWE


def romper_clave_ring(tarea: TareaRingLWE) -> list[int]:
    """Clave publica: b = a*s + e. Recuperar el secreto s."""
    raise NotImplementedError  # TODO


def descifrar_ring(tarea: TareaRingLWE, s: list[int]) -> list[int]:
    """Palabra de bits a partir de (c1, c2): d = c2 - s*c1, y cada coeficiente se asigna
    al polo mas cercano (0 -> bit 0, q/2 -> bit 1)."""
    raise NotImplementedError  # TODO

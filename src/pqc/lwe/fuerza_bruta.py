"""Fuerza bruta: probar los posibles errores (o secretos) y comprobar consistencia."""
from __future__ import annotations

from ..tareas import LWETask


def brute_force(task: LWETask, max_error: int) -> list[int] | None:
    """Idea: elegir n ecuaciones, probar e en [-max_error, max_error]^n, resolver y
    comprobar que el resto de ecuaciones salen con error acotado. Coste (2E+1)^n."""
    raise NotImplementedError  # TODO
